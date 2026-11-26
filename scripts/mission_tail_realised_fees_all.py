#!/usr/bin/env python3
"""Realised admin-fee rates from Form 990 alone for all 641 tail community foundations (P-B4427B4501-04) and for the 29
non-CF sponsors of the long-tail fee census (P-B4427B4501-05). Task id b4427b-0405.

Imports the fee-line method of scripts/mission_npt_screen_fees.py (task b4427b-b4501) and does not modify it:
  - Part VIII revenue lines (program service revenue, other revenue) whose description names an administrative, management,
    philanthropic or fund fee, or "fee income"                                   (base.fee_lines / base.FEE_DESC)
  - Schedule D Part XI line 2d administrative-fee items                          (base.recon_fees / base.RECON_FEE)
  - Schedule D Part V line 1f administrative expenses on endowment funds         (base.parse_fee_xml)
  - the Licking County audit figures and the hand capture readings of b4427b-b4501 (base.FEE_AUDIT, base.SCOPE)
Additions here (wave-41B corrections and the larger sample):
  - pass-through fee lines (EITC / tax-credit grant fees) are excluded from fee income and reported separately (Greene);
  - Licking County is treated as a publisher (its audit note 1N states its schedule);
  - capture is classified for every sponsor from the filer's own wording (CAPTURE RULES below), with the b4427b-b4501 hand
    readings kept where they exist;
  - Part IX line 24 'other expenses' lines naming an administrative fee are read, to detect an interfund gross-up
    (fee revenue matched by a fee expense within 10%);
  - an extra denominator: funds held = Schedule D Part I line 4 columns (a) + (b) (DAFs plus other funds);
  - rates by DAF size band and by total-asset band, disclosure shares, and a realised-rate pool with a range.

CAPTURE RULES (sponsor level, first match wins; `capture_basis` quotes the wording):
  1. b4427b-b4501 hand reading (base.SCOPE) for the 10 EINs it covers.
  2. internal: any fee item worded as charged to the sponsor's own funds (INTERNAL_WORDS: internal, interfund, component,
     endowment, nonoperating funds, from funds, fund administration, funds held, designated, donor advised / DAF).
  3. internal: any Schedule D Part XI line 2d fee item not worded as agency/external (revenue in the audited statements but
     not on Part VIII: an eliminated interfund fee).
  4. internal: a Part VIII fee line matched in the same year by a Part IX line 24 administrative-fee expense within 10%.
  5. agency: fee items worded as agency, external, charged to others, third party, other organisations, property/rental.
  6. unknown: a visible fee whose base is not stated.   7. none visible: no fee item in FY2022-24.
  For the two-way split asked for, `capture2` = internal vs agency/unknown (none visible kept apart).

RATES (pooled over FY2022-24 years in which the relevant fee is visible; a blank year is non-disclosure, not zero):
  visible_bps_ta    = all visible fee income (less pass-through) / average (BOY, EOY) Part X total assets
  internal_bps_ta   = internal fee income / average total assets            (internal-capture sponsors only)
  internal_bps_na   = internal fee income / average net assets
  internal_bps_funds= internal fee income / average Sch D Part I line 4 (a)+(b)
  fee_per_daf_bps_upper = fee income / average Sch D line 4 (a): a ceiling on a DAF-only rate
  endow_admin_bps   = Sch D Part V line 1f / average of lines 1a and 1g

POOL (tail CF DAF assets FY2024 from daf-long-tail-sponsors-fy2021-2024.csv; [C on the stated assumption]):
  central  : each CF at its own internal_bps_ta where observed, else the median internal rate of its DAF size band
  low/high : the same with the band's lower/upper quartile for non-disclosers
  floor    : internal disclosers at their own rate, everyone else zero
  bootstrap: seeded resampling of the internal-fee CFs within band (90% interval of the central)
  Non-CF part ($3.08bn): zero / non-CF realised rate (if n >= 3) / CF central rate (the whole-tail assumption).

Usage (cache paths are outside the repo):
  python3 -I scripts/mission_tail_realised_fees_all.py . --task fetch --irs-dir IRS --irs-dir IRS_NEWER --xml-dir XMLDIR
          [--reuse-dir DIR ...] --fetch [--log FETCHLOG.tsv]
  python3 -I scripts/mission_tail_realised_fees_all.py . --task run --irs-dir IRS --irs-dir IRS_NEWER --xml-dir XMLDIR
          [--reuse-dir DIR ...] [--text-dir FEEDIR]
Outputs: data/mission-2026-11-14/tail-realised-fees-all-2026-11-20.csv and markdown tables on stdout
         (used by research/mission-2026-11-14/b4427b-0405-realised-tail-fees-all.md).
"""
from __future__ import annotations

import argparse
import os
import random
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.dont_write_bytecode = True  # importing the base script must not leave a .pyc in the repo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_npt_screen_fees as base  # noqa: E402

TAIL = "data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv"
PRIOR = "data/mission-2026-11-14/tail-realised-fee-rates-2026-11-20.csv"
OUT_CSV = "data/mission-2026-11-14/tail-realised-fees-all-2026-11-20.csv"
TAIL_BANDS = ("t10_50", "t1_10", "t0_1", "zero")
BAND_LABEL = {"t10_50": "$10m–50m DAF", "t1_10": "$1m–10m DAF", "t0_1": "under $1m DAF", "zero": "zero DAF"}
TA_BANDS = ((0, 10e6, "TA < $10m"), (10e6, 25e6, "TA $10m–25m"), (25e6, 50e6, "TA $25m–50m"),
            (50e6, 100e6, "TA $50m–100m"), (100e6, float("inf"), "TA ≥ $100m"))
READ_FYS = (2021, 2022, 2023, 2024)
FEE_YEARS = base.FEE_YEARS
SCHEDULE_POOL = {"cf_only_central": 89.9e6, "whole_tail_central": 138e6}  # b4501-04 as corrected by wave 35A
PUBLISHER_OVERRIDE = {"311760702": "Licking audit note 1N states its schedule ($250 minimum, 1% graduated to 0.1%) [V wave 41B]"}
PASS_THROUGH = re.compile(r"(?i)\bEITC\b|tax\s+credit")
INTERNAL_WORDS = re.compile(r"(?i)internal|inter-?fund|component|endow|non-?operating\s+funds|from\s+(?:the\s+)?funds|"
                            r"fund\s+admin|funds?\s+held|designated|donor[\s-]+advised|\bDAFs?\b")
AGENCY_WORDS = re.compile(r"(?i)agency|external|charged\s+to\s+others|third[\s-]+party|other\s+(?:organi[sz]ations|charities|"
                          r"nonprofits|entities)|fiscal\s+spons|\bsponsored\b|property|rental")
EXP_FEE = re.compile(r"(?i)\badmin\w*\.?\s.*\bfees?\b|\bfund\s+fees?\b")
MATCH_TOL = 0.10
SEED, N_BOOT = 20261120, 2000


# ----------------------------------------------------------------------------- parse (pure)
def parse_all(data: bytes) -> dict | None:
    """base.parse_fee_xml plus Part IX line 24 fee-named expenses, Sch D other funds and DAF count."""
    try:
        core = base.parse_fee_xml(data)
        root = ET.fromstring(data)
    except ET.ParseError:
        return None
    sd = root.find(f".//{base.NS}IRS990ScheduleD")
    exp = tuple({"desc": base.first(g, ("Desc",)), "amt": base.num(base.first(g, ("TotalAmt",))) or 0.0}
                for g in root.iter(f"{base.NS}OtherExpensesGrp") if EXP_FEE.search(base.first(g, ("Desc",)) or ""))
    return {**core, "fee_exp": exp, "other_funds_eoy": base.num(base.first(sd, ("FundsAndOtherAccountsVlEOYAmt",))),
            "daf_count": base.num(base.first(sd, ("DonorAdvisedFundsHeldCnt",)))}


def item_class(desc: str) -> str:
    return ("pass" if PASS_THROUGH.search(desc) else "agency" if AGENCY_WORDS.search(desc) else
            "internal" if INTERNAL_WORDS.search(desc) else "plain")


def items_of(ein: str, fy: int, px: Mapping) -> tuple[dict, ...]:
    viii = ({"src": "VIII", "desc": x["desc"], "amt": x["amt"] or 0.0} for x in px["fee_lines"])
    xi = ({"src": "XI", "desc": x["label"], "amt": x["amt"] or 0.0} for x in px["recon"])
    aud = ({"src": "audit", "desc": a["quote"], "amt": a["amount"]} for a in base.FEE_AUDIT
           if a["ein"] == ein and a["fiscal_year"] == fy)
    return tuple({**i, "cls": item_class(i["desc"])} for i in (*viii, *xi, *aud))


def avg(a, b):
    return (a + b) / 2 if a is not None and b is not None else None


def year_rec(ein: str, fy: int, ret: Mapping | None, px: Mapping | None, prev: Mapping | None) -> dict | None:
    if not px:
        return None
    its = items_of(ein, fy, px)
    s = lambda pred: sum(i["amt"] for i in its if pred(i))  # noqa: E731
    viii = s(lambda i: i["src"] == "VIII" and i["cls"] != "pass")
    exp = sum(e["amt"] for e in px["fee_exp"] if not AGENCY_WORDS.search(e["desc"] or ""))
    funds = lambda p: (p["daf_eoy"] or 0) + (p["other_funds_eoy"] or 0) if p and (p.get("daf_eoy") is not None or  # noqa: E731
                                                                              p.get("other_funds_eoy") is not None) else None
    return {"fiscal_year": fy, "object_id": ret["object_id"], "fallback": ret.get("fallback", 0), "items": its,
            "fee_visible": s(lambda i: i["cls"] != "pass"), "fee_pass": s(lambda i: i["cls"] == "pass"),
            "fee_internal_cand": s(lambda i: i["cls"] not in ("pass", "agency")),
            "fee_rev_990": s(lambda i: i["src"] == "VIII" and i["cls"] != "pass"),
            "fee_recon_990": s(lambda i: i["src"] == "XI" and i["cls"] != "pass"), "fee_audit": s(lambda i: i["src"] == "audit"),
            "matched_exp": int(viii > 0 and exp > 0 and abs(exp - viii) <= MATCH_TOL * viii),
            "fee_exp_desc": "; ".join(f"{e['desc']} {e['amt']:,.0f}" for e in px["fee_exp"]),
            "avg_ta": avg(px["ta_boy"], px["ta_eoy"]), "avg_na": avg(px["na_boy"], px["na_eoy"]),
            "avg_daf": avg((prev or {}).get("daf_eoy"), px["daf_eoy"]), "avg_funds": avg(funds(prev), funds(px)),
            "endow_admin": px["endow_admin"], "avg_endow": avg(px["endow_boy"], px["endow_eoy"]),
            "ta_eoy": px["ta_eoy"], "daf_eoy": px["daf_eoy"]}


# ----------------------------------------------------------------------------- classify and summarise (pure)
def capture(ein: str, ys: Sequence[Mapping]) -> tuple[str, str]:
    its = [i for y in ys for i in y["items"] if i["cls"] != "pass" and i["amt"] > 0]
    if ein in base.SCOPE:
        sc, why = base.SCOPE[ein]
        return ("agency" if sc == "external" else sc), "b4427b-b4501 reading: " + why
    if not its:
        return "none visible", ""
    hit = lambda pred: next((i for i in its if pred(i)), None)  # noqa: E731
    q = lambda i: f"{'Part VIII' if i['src'] == 'VIII' else 'Sch D Part XI 2d' if i['src'] == 'XI' else 'audit'} '{i['desc']}'"  # noqa: E731
    if (i := hit(lambda i: i["cls"] == "internal")):
        return "internal", "own-fund wording: " + q(i)
    if (i := hit(lambda i: i["src"] == "XI" and i["cls"] != "agency")):
        return "internal", "in audited revenue but not on Part VIII (interfund): " + q(i)
    if (y := next((y for y in ys if y["matched_exp"]), None)):
        return "internal", (f"FY{y['fiscal_year']} Part VIII fee {y['fee_rev_990']:,.0f} matched by Part IX 24 expense "
                            f"'{y['fee_exp_desc']}' (within 10%)")
    if (i := hit(lambda i: i["cls"] == "agency")):
        return "agency", "agency/external wording: " + q(i)
    return "unknown", "base not stated: " + q(its[0])


def partial(internal: float | None, endow: float | None) -> int | str:
    """1 when the internal fee rate is under half the Part V endowment admin rate (capture looks partial, as at
    Central Florida in b4427b-b4501); blank when either is missing."""
    return "" if not internal or not endow or endow <= 0 else int(internal < 0.5 * endow)


def complete(r: Mapping) -> Mapping:
    """The row with a partial-capture internal rate set aside (used for the complete-capture pool)."""
    return {**r, "internal_bps_ta": None} if r.get("partial_flag") == 1 else r


def ta_band(x: float | None) -> str:
    return "" if x is None else next(lbl for lo, hi, lbl in TA_BANDS if lo <= x < hi)


def summarise(s: Mapping, ys: Sequence[Mapping]) -> dict:
    fy = [y for y in ys if y["fiscal_year"] in FEE_YEARS]
    vis = [y for y in fy if y["fee_visible"] > 0]
    cap, basis = capture(s["ein"], fy)
    internal_amt = (lambda y: y["fee_visible"]) if s["ein"] in base.SCOPE else (lambda y: y["fee_internal_cand"])
    intl = [{**y, "fee_int": internal_amt(y)} for y in fy if cap == "internal" and internal_amt(y) > 0]
    endow = [y for y in fy if y.get("endow_admin") is not None and y.get("avg_endow")]
    tas = [y["avg_ta"] for y in fy if y.get("avg_ta")]
    avg_ta = sum(tas) / len(tas) if tas else None
    b = lambda rows, n, d: base.bps(base.pooled(rows, n, d)) if rows else None  # noqa: E731
    lines = sorted({f"{i['src']}: {i['desc'][:60]} {i['amt']:,.0f}" for y in fy for i in y["items"] if i["src"] != "audit"})
    return {**s, "years_read": len(fy), "years_with_fee": len(vis), "fee_years": ";".join(str(y["fiscal_year"]) for y in vis),
            "fee_visible_fy22_24": sum(y["fee_visible"] for y in fy), "fee_rev_990_fy22_24": sum(y["fee_rev_990"] for y in fy),
            "fee_recon_990_fy22_24": sum(y["fee_recon_990"] for y in fy), "fee_audit_fy22_24": sum(y["fee_audit"] for y in fy),
            "fee_passthrough_fy22_24": sum(y["fee_pass"] for y in fy), "fee_internal_fy22_24": sum(y["fee_int"] for y in intl),
            "capture": cap, "capture2": cap if cap in ("internal", "none visible") else "agency_or_unknown",
            "capture_basis": basis[:300], "avg_total_assets": avg_ta, "ta_band": ta_band(avg_ta),
            "visible_bps_ta": b(vis, "fee_visible", "avg_ta"), "internal_bps_ta": b(intl, "fee_int", "avg_ta"),
            "internal_bps_na": b(intl, "fee_int", "avg_na"), "internal_bps_funds": b(intl, "fee_int", "avg_funds"),
            "fee_per_daf_bps_upper": b(intl or vis, "fee_int" if intl else "fee_visible", "avg_daf"),
            "endow_admin_bps": b(endow, "endow_admin", "avg_endow"), "endow_years": len(endow),
            "partial_flag": partial(b(intl, "fee_int", "avg_ta"), b(endow, "endow_admin", "avg_endow")),
            "fallback_returns": sum(y["fallback"] for y in fy),
            "fee_lines_seen": " | ".join(lines)[:500],
            "fee_expense_lines_seen": " | ".join(sorted({y["fee_exp_desc"] for y in fy if y["fee_exp_desc"]}))[:300],
            "return_object_ids": ";".join(y["object_id"] for y in fy)}


def sponsors(tail: Sequence[Mapping], census: Sequence[Mapping]) -> tuple[dict, ...]:
    cen = {c["ein"]: c for c in census}
    def row(t, part):
        c = cen.get(t["ein"], {})
        pub = (("yes", PUBLISHER_OVERRIDE[t["ein"]]) if t["ein"] in PUBLISHER_OVERRIDE else
               ("yes" if c.get("in_2021plus_distribution") == "yes" else "no", "census") if c else ("", ""))
        return {"ein": t["ein"], "name": t["name"], "part": part, "sponsor_category": t["sponsor_category"],
                "census_type4": c.get("type4", ""), "size_band_fy2024": t["size_band_fy2024"],
                "daf_assets_fy2024": base.num(t["daf_assets_fy2024"]) or 0.0, "in_census_sample": int(bool(c)),
                "census_fee_status": c.get("fee_status", ""), "publisher": pub[0], "publisher_basis": pub[1],
                "published_bps_100k": base.num(c.get("admin_bps_100k"))}
    tail_cf = (row(t, "B_tail_cf") for t in tail if t["sponsor_category"] == "community_foundation" and t["size_band_fy2024"] in TAIL_BANDS)
    tmap = {t["ein"]: t for t in tail}
    noncf = (row(tmap[c["ein"]], "A_noncf_sample") for c in census if c["type4"] != "cf")
    return (*tail_cf, *noncf)


# ----------------------------------------------------------------------------- selection and fetch
def candidates(index: Mapping[str, Sequence[Mapping]], eins: Sequence[str]) -> dict[tuple[str, int], tuple[dict, ...]]:
    return {(e, fy): c for e in eins for fy in READ_FYS for c in (base.fy_candidates(index.get(e, ()), fy),) if c}


def pick_local(cands: Mapping[tuple[str, int], Sequence[Mapping]], local: Mapping[str, str]) -> dict[tuple[str, int], dict]:
    """Newest return for (EIN, FY) with a local XML; the next-newest stands in (flagged) when the newest is not on the mirror."""
    def pick(cs):
        ok = [c for c in cs if c["object_id"] in local]
        return {**ok[0], "fallback": int(ok[0]["object_id"] != cs[0]["object_id"])} if ok else None
    return {k: p for k, cs in cands.items() for p in (pick(cs),) if p}


def fetch_key(cs: Sequence[Mapping], local: Mapping[str, str], xml_dir: str, fetch: bool) -> tuple[str, str]:
    """Try the candidates newest first; save the first one obtained. Returns (object id, status)."""
    for c in cs:
        data, how = base.get_xml(c["object_id"], local, fetch)
        if data and how == "mirror":
            with open(os.path.join(xml_dir, f"{c['object_id']}.xml"), "wb") as fh:
                fh.write(data)
        if data:
            return c["object_id"], how
        if how != "http_404":
            return c["object_id"], how
    return cs[0]["object_id"], "http_404_all"


# ----------------------------------------------------------------------------- statistics and pool (pure)
def stats(vals: Sequence[float]) -> tuple:
    v = [x for x in vals if x is not None and x > 0]
    q1, q3 = base.quartiles(v)
    return len(v), base.median(v), q1, q3


def fq(st: tuple) -> str:
    return "–" if not st[0] else f"{st[1]:.0f} ({st[2]:.0f}–{st[3]:.0f}; n={st[0]})"


def band_rates(rows: Sequence[Mapping], key: str = "internal_bps_ta") -> dict[str, tuple]:
    allv = [r[key] for r in rows if r[key]]
    per = {b: stats([r[key] for r in rows if r["size_band_fy2024"] == b and r[key]]) for b in TAIL_BANDS}
    whole = stats(allv)
    # a band with fewer than 3 internal rates borrows the whole-tail distribution (flagged in the report)
    return {**{b: (st if st[0] >= 3 else whole) + (st[0] >= 3,) for b, st in per.items()}, "all": whole + (True,)}


def pool(rows: Sequence[Mapping], rates: Mapping[str, tuple], which: int, own: bool = True) -> float:
    """which: 1 median, 2 Q1, 3 Q3 of the band's internal rates for CFs without their own internal rate."""
    rate = lambda r: (r["internal_bps_ta"] if own and r["internal_bps_ta"] else rates[r["size_band_fy2024"]][which])  # noqa: E731
    return sum(r["daf_assets_fy2024"] * (rate(r) or 0) / 1e4 for r in rows)


def floor_pool(rows: Sequence[Mapping], key: str = "internal_bps_ta") -> float:
    return sum(r["daf_assets_fy2024"] * (r[key] or 0) / 1e4 for r in rows)


def bootstrap(rows: Sequence[Mapping], seed: int, n: int) -> tuple[float, float]:
    rng = random.Random(seed)  # local generator: no global state
    donors = {b: [r for r in rows if r["size_band_fy2024"] == b and r["internal_bps_ta"]] for b in TAIL_BANDS}
    alld = [r for r in rows if r["internal_bps_ta"]]
    def one(_):
        res = {b: [rng.choice(d) for _ in d] if len(d) >= 3 else [rng.choice(alld) for _ in alld] for b, d in donors.items()}
        rates = {b: (None, base.median([r["internal_bps_ta"] for r in v])) for b, v in res.items()}
        return sum(r["daf_assets_fy2024"] * (r["internal_bps_ta"] or rates[r["size_band_fy2024"]][1] or 0) / 1e4 for r in rows)
    draws = sorted(map(one, range(n)))
    return draws[int(0.05 * n)], draws[int(0.95 * n) - 1]


# ----------------------------------------------------------------------------- report (pure)
M = base.m


def disclosure_table(rows: Sequence[Mapping], keyf, keys: Sequence[str], label) -> str:
    def line(k):
        rs = [r for r in rows if keyf(r) == k]
        n = len(rs)
        read = [r for r in rs if r["years_read"]]
        sh = lambda pred: f"{sum(1 for r in read if pred(r))} ({100 * sum(1 for r in read if pred(r)) / len(read):.0f}%)" if read else "–"  # noqa: E731
        return (label(k), n, len(read), sh(lambda r: r["years_with_fee"] > 0), sh(lambda r: r["capture"] == "internal"),
                sh(lambda r: r["capture"] in ("agency", "unknown")),
                fq(stats([r["visible_bps_ta"] for r in read])), fq(stats([r["internal_bps_ta"] for r in read])),
                fq(stats([r["endow_admin_bps"] for r in read])),
                f"{sum(r['daf_assets_fy2024'] for r in rs) / 1e6:,.0f}")
    return base.md_table(("Group", "Sponsors", "With FY22–24 990 read", "Any fee visible", "Internal fee disclosed",
                          "Agency/unknown only", "Visible fee ÷ avg TA", "Internal ÷ avg TA",
                          "Part V admin ÷ endowment", "DAF assets FY2024 $m"), map(line, keys))


def report(cf: Sequence[Mapping], ncf: Sequence[Mapping], prior: Sequence[Mapping], qcheck: Mapping, sel_stats: Mapping) -> str:
    out = [f"Returns: {sel_stats}", "Audit quote check (Licking): " + "; ".join(f"{k} {v}" for k, v in qcheck.items()), ""]
    # reproduction check against b4427b-b4501 for the 31 census CFs
    pm = {p["ein"]: p for p in prior}
    rep = [(r["name"], base.num(pm[r["ein"]]["realised_bps_total_assets"]),
            r["internal_bps_ta"] if r["capture"] == "internal" else r["visible_bps_ta"], r["capture"], pm[r["ein"]]["scope"])
           for r in cf if r["ein"] in pm]
    diff = [x for x in rep if (x[1] or 0) and abs((x[1] or 0) - (x[2] or 0)) > 0.05]
    out += ["## R0 Reproduction of b4427b-b4501 on its 31 census CFs",
            f"{len(rep)} matched; {len(rep) - len(diff)} reproduce the prior realised rate to 0.05 bps; differences:",
            base.md_table(("Sponsor", "Prior bps", "This run bps", "Capture now", "Prior scope"), diff), ""]
    out += ["## B1 Disclosure and realised rates by DAF size band, all 641 tail CFs (bps; median (IQR; n))",
            disclosure_table(cf, lambda r: r["size_band_fy2024"], TAIL_BANDS, lambda k: BAND_LABEL[k]), "",
            disclosure_table(cf, lambda r: "all", ("all",), lambda k: "All tail CFs"), ""]
    tab = [lbl for _, _, lbl in TA_BANDS]
    out += ["## B2 By total-asset band (average FY2022–24 Part X total assets)",
            disclosure_table([r for r in cf if r["ta_band"]], lambda r: r["ta_band"], tab, lambda k: k), ""]
    pubs = [r for r in cf if r["in_census_sample"]]
    out += ["## B3 Census CFs: publishers vs non-publishers (Licking counted as a publisher, wave 41B)",
            disclosure_table(pubs, lambda r: r["publisher"], ("yes", "no"), lambda k: {"yes": "Publishers", "no": "Non-publishers"}[k]), ""]
    # capture basis tally
    basis_kind = lambda r: (("matched Part IX fee expense" if "matched by Part IX" in r["capture_basis"] else  # noqa: E731
                              r["capture_basis"].split(":")[0]) if r["capture"] == "internal" else r["capture"])
    kinds = sorted({basis_kind(r) for r in cf if r["years_read"]})
    out += ["## B4 How capture was classified (tail CFs with a return read)",
            base.md_table(("Class / basis", "CFs"), ((k, sum(1 for r in cf if r["years_read"] and basis_kind(r) == k)) for k in kinds)), ""]
    # internal rate vs size: correlation by rank
    intl = sorted((r for r in cf if r["internal_bps_ta"] and r["avg_total_assets"]), key=lambda r: r["avg_total_assets"])
    rs = spearman([r["avg_total_assets"] for r in intl], [r["internal_bps_ta"] for r in intl])
    out += [f"Spearman rank correlation, average total assets vs internal_bps_ta, internal-fee CFs: {rs:.2f} (n={len(intl)})"
            if rs is not None else "", ""]
    # pool
    cfc = [complete(r) for r in cf]  # partial-capture internal rates set aside
    n_partial = sum(1 for r in cf if r.get("partial_flag") == 1)
    rates_all, rates = band_rates(cf), band_rates(cfc)
    cf_daf = sum(r["daf_assets_fy2024"] for r in cf)
    lo_b, hi_b = bootstrap(cfc, SEED, N_BOOT)
    central, low, high = pool(cfc, rates, 1), pool(cfc, rates, 2), pool(cfc, rates, 3)
    a_central, a_low = pool(cf, rates_all, 1), pool(cf, rates_all, 2)
    flat = cf_daf * rates["all"][1] / 1e4
    floor_ = floor_pool(cf)
    vis_floor = floor_pool(cf, "visible_bps_ta")
    endow = band_rates(cf, "endow_admin_bps")
    endow_pool = pool([{**r, "internal_bps_ta": None} for r in cf], endow, 1, own=False)
    bp = lambda x: f"{1e4 * x / cf_daf:.1f}"  # noqa: E731
    rate_tab = lambda rs: base.md_table(("Band", "n", "Median", "Q1", "Q3", "Own band"),  # noqa: E731
                                        ((BAND_LABEL.get(b, "All tail CFs"), rs[b][0], f"{rs[b][1]:.1f}", f"{rs[b][2]:.1f}",
                                          f"{rs[b][3]:.1f}", "yes" if rs[b][4] else "no (all-tail)") for b in (*TAIL_BANDS, "all")))
    out += [f"Partial-capture flag (internal rate < half the Part V endowment admin rate): {n_partial} of "
            f"{sum(1 for r in cf if r['internal_bps_ta'])} internal-fee CFs: "
            + "; ".join(f"{r['name']} {r['internal_bps_ta']} vs {r['endow_admin_bps']}" for r in cf if r.get("partial_flag") == 1), "",
            "## B5a Band rates, complete-capture internal-fee CFs (used for the central pool; bands with n < 3 borrow the all-tail set)",
            rate_tab(rates), "", "## B5b Band rates, all internal-fee CFs (partial captures included; sensitivity)", rate_tab(rates_all), "",
            f"## B6 Realised-rate CF pool (tail CF DAF assets ${cf_daf / 1e9:,.3f}bn)",
            base.md_table(("Scenario", "Pool $m", "Implied bps on DAF assets"),
                          (("Central: own complete-capture internal rate, else band median", M(central), bp(central)),
                           ("Low: own rate, else band Q1", M(low), bp(low)),
                           ("High: own rate, else band Q3", M(high), bp(high)),
                           (f"Bootstrap 90% interval of central (seed {SEED}, {N_BOOT} draws)", f"{M(lo_b)}–{M(hi_b)}", ""),
                           ("Sensitivity: partial captures kept, band median", M(a_central), bp(a_central)),
                           ("Sensitivity: partial captures kept, band Q1", M(a_low), bp(a_low)),
                           ("Flat all-tail complete-capture median", M(flat), f"{rates['all'][1]:.1f}"),
                           ("Floor: internal disclosers only at own rate, others zero", M(floor_), bp(floor_)),
                           ("Floor: any visible fee at own visible rate, others zero", M(vis_floor), bp(vis_floor)),
                           ("Proxy: band median Part V endowment admin rate", M(endow_pool), bp(endow_pool)),
                           ("Schedule-based CFs-only central (b4501-04, wave 35A)", M(SCHEDULE_POOL["cf_only_central"]),
                            bp(SCHEDULE_POOL["cf_only_central"])))), ""]
    # part A
    by_cat = sorted({r["sponsor_category"] for r in ncf})
    out += ["## A1 Non-CF census sponsors (29): disclosure and rates by category",
            disclosure_table(ncf, lambda r: r["sponsor_category"], by_cat, lambda k: k), "",
            disclosure_table(ncf, lambda r: "all", ("all",), lambda k: "All 29 non-CFs"), "",
            "Census CFs on the same basis (31):", disclosure_table(pubs, lambda r: "all", ("all",), lambda k: "All 31 census CFs"), "",
            "## A2 Each non-CF sponsor",
            base.md_table(("Sponsor", "Category", "Band", "DAF FY2024 $m", "Years", "Fee $ FY22–24", "Capture", "Visible ÷ TA",
                           "Internal ÷ TA", "Internal ÷ funds held", "Part V admin", "Basis / lines"),
                          ((r["name"], r["sponsor_category"], r["size_band_fy2024"], M(r["daf_assets_fy2024"]),
                            f"{r['years_with_fee']}/{r['years_read']}", f"{r['fee_visible_fy22_24']:,.0f}", r["capture"],
                            r["visible_bps_ta"] or "–", r["internal_bps_ta"] or "–", r["internal_bps_funds"] or "–",
                            r["endow_admin_bps"] or "–", (r["capture_basis"] or r["fee_lines_seen"])[:110].replace("|", "/"))
                           for r in sorted(ncf, key=lambda r: (r["sponsor_category"], -r["daf_assets_fy2024"])))), ""]
    n_int = stats([r["internal_bps_ta"] for r in ncf])
    n_funds = stats([r["internal_bps_funds"] for r in ncf])
    out += [f"Non-CF internal-fee rate (÷ TA): {fq(n_int)}; (÷ funds held): {fq(n_funds)}"]
    share = lambda rs: sum(1 for r in rs if r["years_with_fee"] > 0) / len(rs)  # noqa: E731
    return "\n".join(out), {"central": central, "low": low, "high": high, "floor": floor_, "cf_daf": cf_daf,
                            "rates": rates, "boot": (lo_b, hi_b), "ncf_int": n_int, "ncf_funds": n_funds,
                            "share_ncf": share(ncf), "share_cen_cf": share(pubs)}


def spearman(x: Sequence[float], y: Sequence[float]) -> float | None:
    if len(x) < 3:
        return None
    rk = lambda v: {i: r for r, i in enumerate(sorted(range(len(v)), key=lambda i: v[i]))}  # noqa: E731
    rx, ry = rk(x), rk(y)
    n = len(x)
    return 1 - 6 * sum((rx[i] - ry[i]) ** 2 for i in range(n)) / (n * (n * n - 1))


def whole_tail(res: Mapping, ncf_daf: float) -> str:
    c, (n_int, n_med) = res["central"], (res["ncf_int"][0], res["ncf_int"][1])
    cf_rate = 1e4 * c / res["cf_daf"]
    rows = (("Non-CFs charge nothing", M(c), M(res["low"]), M(res["high"])),
            (f"Non-CFs at the non-CF realised internal median ({n_med:.1f} bps; n={n_int})" if n_int >= 3 and n_med else
             "Non-CFs at a non-CF realised rate (n < 3: not estimable)",
             M(c + ncf_daf * n_med / 1e4) if n_int >= 3 and n_med else "–",
             M(res["low"] + ncf_daf * res["ncf_int"][2] / 1e4) if n_int >= 3 and n_med else "–",
             M(res["high"] + ncf_daf * res["ncf_int"][3] / 1e4) if n_int >= 3 and n_med else "–"),
            (f"Non-CFs at the CF central implied rate ({cf_rate:.1f} bps; the whole-tail assumption)",
             M(c + ncf_daf * cf_rate / 1e4), M(res["low"] * (1 + ncf_daf / res["cf_daf"])), M(res["high"] * (1 + ncf_daf / res["cf_daf"]))))
    adj = res["share_ncf"] / res["share_cen_cf"] if res["share_cen_cf"] else 0
    k = ncf_daf / res["cf_daf"]
    rows += ((f"[I] Non-CFs at the CF implied rate × disclosure ratio ({100 * res['share_ncf']:.0f}% of sampled non-CFs vs "
              f"{100 * res['share_cen_cf']:.0f}% of census CFs show any fee line; factor {adj:.2f})",
              M(c * (1 + k * adj)), M(res["low"] * (1 + k * adj)), M(res["high"] * (1 + k * adj))),)
    return "\n".join([f"## W1 Whole-tail realised-rate pool (non-CF DAF assets ${ncf_daf / 1e9:,.3f}bn); schedule-based whole-tail "
                      f"central was {M(SCHEDULE_POOL['whole_tail_central'])}m",
                      base.md_table(("Non-CF assumption", "Central $m", "Low $m", "High $m"), rows)])


# ----------------------------------------------------------------------------- tasks (I/O)
FIELDS = ("ein", "name", "part", "sponsor_category", "census_type4", "size_band_fy2024", "daf_assets_fy2024", "in_census_sample",
          "census_fee_status", "publisher", "publisher_basis", "published_bps_100k", "years_read", "years_with_fee", "fee_years",
          "fee_visible_fy22_24", "fee_rev_990_fy22_24", "fee_recon_990_fy22_24", "fee_audit_fy22_24", "fee_passthrough_fy22_24",
          "fee_internal_fy22_24", "capture", "capture2", "capture_basis", "avg_total_assets", "ta_band", "visible_bps_ta",
          "internal_bps_ta", "internal_bps_na", "internal_bps_funds", "fee_per_daf_bps_upper", "endow_admin_bps", "endow_years",
          "partial_flag", "pool_rate_bps", "pool_rate_basis", "pool_central_usd", "fallback_returns", "fee_lines_seen", "fee_expense_lines_seen",
          "return_object_ids")


def load_inputs(root: str, args):
    tail = base.read_csv(os.path.join(root, TAIL))
    census = base.read_csv(os.path.join(root, base.CENSUS))
    sp = sponsors(tail, census)
    eins = frozenset(s["ein"] for s in sp)
    index = base.load_index(base.index_paths(args.irs_dir), eins)
    return sp, candidates(index, sorted(eins))


def task_fetch(root: str, args) -> int:
    sp, cands = load_inputs(root, args)
    os.makedirs(args.xml_dir, exist_ok=True)
    local = base.cached_xml_paths([args.xml_dir, *args.reuse_dir])
    print(f"sponsors {len(sp)}; sponsor-years with a filed 990 {len(cands)}; already local "
          f"{sum(1 for cs in cands.values() if cs[0]['object_id'] in local)}", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        res = list(ex.map(lambda kv: (kv[0], *fetch_key(kv[1], local, args.xml_dir, args.fetch)), sorted(cands.items())))
    if args.log:
        with open(args.log, "w", encoding="utf-8") as fh:
            fh.write("ein\tfy\tobject_id\tstatus\n" + "".join(f"{k[0]}\t{k[1]}\t{o}\t{s}\n" for k, o, s in res))
    tally = {}
    for _, _, s in res:  # local tally only
        tally[s] = tally.get(s, 0) + 1
    print(f"fetch status: {tally}", file=sys.stderr)
    return 0


def task_run(root: str, args) -> int:
    sp, cands = load_inputs(root, args)
    local = base.cached_xml_paths([args.xml_dir, *args.reuse_dir])
    sel = pick_local(cands, local)

    def load(oid):
        with open(local[oid], "rb") as fh:
            return oid, parse_all(fh.read())
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        px = dict(ex.map(load, sorted({r["object_id"] for r in sel.values()})))
    get = lambda e, fy: px.get((sel.get((e, fy)) or {}).get("object_id"))  # noqa: E731
    years = {s["ein"]: [y for fy in FEE_YEARS for y in (year_rec(s["ein"], fy, sel.get((s["ein"], fy)), get(s["ein"], fy),
                                                                   get(s["ein"], fy - 1)),) if y] for s in sp}
    summ = [summarise(s, years[s["ein"]]) for s in sp]
    cf = [r for r in summ if r["part"] == "B_tail_cf"]
    ncf = [r for r in summ if r["part"] == "A_noncf_sample"]
    sel_stats = {"sponsor_years_filed_FY2021_24": len(cands), "selected_with_xml": len(sel),
                 "parse_failed": sum(1 for v in px.values() if v is None),
                 "fallback_next_newest": sum(1 for r in sel.values() if r.get("fallback")),
                 "tail_cfs_with_a_FY22_24_return": sum(1 for r in cf if r["years_read"]),
                 "noncf_with_a_FY22_24_return": sum(1 for r in ncf if r["years_read"])}
    qcheck = base.verify_quotes(base.FEE_AUDIT, os.path.join(args.text_dir, "audit_txt")) if args.text_dir else {}
    text, res = report(cf, ncf, base.read_csv(os.path.join(root, PRIOR)), qcheck, sel_stats)
    ncf_daf = sum(base.num(t["daf_assets_fy2024"]) or 0 for t in base.read_csv(os.path.join(root, TAIL))
                  if t["sponsor_category"] != "community_foundation" and t["size_band_fy2024"] in TAIL_BANDS)
    rates = res["rates"]
    with_pool = [{**r, **pool_fields(complete(r), rates)} for r in cf] + [{**r, "pool_rate_basis": "not in CF pool"} for r in ncf]
    base.write_csv(os.path.join(root, args.out), with_pool, FIELDS)
    print(text)
    print(whole_tail(res, ncf_daf))
    return 0


def pool_fields(r: Mapping, rates: Mapping) -> dict:
    own = r["internal_bps_ta"]
    b = rates[r["size_band_fy2024"]]
    rate, basis = (own, "own internal rate") if own else (b[1], f"band median ({'own band' if b[4] else 'all-tail set'})")
    return {"pool_rate_bps": rate, "pool_rate_basis": basis, "pool_central_usd": r["daf_assets_fy2024"] * (rate or 0) / 1e4}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    ap.add_argument("--task", choices=("fetch", "run"), required=True)
    ap.add_argument("--irs-dir", action="append", default=[])
    ap.add_argument("--xml-dir", required=True, help="where fetched XMLs are kept (outside the repo)")
    ap.add_argument("--reuse-dir", action="append", default=[], help="earlier XML copies to reuse")
    ap.add_argument("--text-dir", default="", help="b4427b-b4501 fee text dir (audit_txt/ for the Licking quote check)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--log", default="")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default=OUT_CSV)
    args = ap.parse_args(argv)
    return {"fetch": task_fetch, "run": task_run}[args.task](os.path.abspath(args.root), args)


if __name__ == "__main__":
    sys.exit(main())
