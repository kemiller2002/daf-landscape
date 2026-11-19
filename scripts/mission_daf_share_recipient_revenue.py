#!/usr/bin/env python3
"""Independent (non-vendor) estimate of the DAF share of recipient contributions, FY2023-FY2024 (queue item P-B40N12-02).

Numerator   Top-50 DAF sponsors' Schedule I Part II grant lines (universe, return choice and line cache exactly as in
            mission_recipient_sectors.py / mission_exception_load.py: top-50 DAFRC sponsors by FY2024 DAF assets,
            94 itemising sponsor-years), filer totals rows dropped (mission_exception_load.drop_totals_rows),
            DAF-to-DAF lines dropped (mission_recipient_sectors.annotate: whitelist `include` EINs, self-lines and
            unique whitelisted-name matches). Summed by recipient EIN and sponsor fiscal year (year the tax period
            ends). Two bases: `schedule_i` (all filed lines) and `daf_weighted` (each sponsor-year's lines x its DAF
            share of grants from sponsor-cost-structure.csv, capped at 1; sponsor-years without a share keep weight 1).
Denominator Each recipient's own return for the same fiscal years (tax period ending in 2023 and 2024): Form 990
            Part VIII line 1h (TotalContributionsAmt) or, for 990-EZ filers, Part I line 1
            (ContributionsGiftsGrantsEtcAmt). Also kept: Part VIII line 1e government grants and total revenue.
            Returns located through the IRS TEOS e-file index (index_2023..2026.csv) and read from the
            GivingTuesday mirror of IRS TEOS XML (streamed; reading stops after the main form).
Share       per recipient: sum over FYs with a located return of numerator / sum of denominators over the same FYs.
Frame       recipient EINs with a positive numerator that are in the IRS EO BMF, excluding
              universities   NTEE B40-B43, B50, or name UNIVERSITY / COLLEGE
              hospitals      NTEE E20-E24, BMF FOUNDATION 12, or name HOSPITAL / MEDICAL CENTER / HEALTH SYSTEM
              foundations    NTEE T20-T31 (private and public grantmaking foundations, community foundations),
                             BMF FOUNDATION 02/03/04 (private foundations)
              DAF sponsors   every DAFRC 2025 panel EIN
              non-501(c)(3)  BMF SUBSECTION other than 03
Sample      certainty stratum: the --certainty largest recipients by numerator (schedule_i, FY2023-24);
            then a simple random sample of up to --per-stratum EINs in each NTEE major group x BMF revenue band,
            random.Random(--seed). Weights N_h / n_h over respondents (recipients with >= 1 located return and a
            positive denominator); non-respondents are assumed missing at random within stratum.
Stats       weighted P25 / median / P75 of per-recipient shares; pooled (combined ratio) share = sum(w x num) /
            sum(w x den); by NTEE major group and by revenue band.

Pure functions; I/O only in fetch/load helpers and `main`. Stdlib only.

Usage:
  python3 scripts/mission_daf_share_recipient_revenue.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRSDIR --f990-cache DIR [--fetch] [--seed 20261119] [--per-stratum 40] [--certainty 400]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, market, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import BMF_FILES, COST, MAJOR, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "daf-share-of-recipient-revenue-2026-11-19.csv")
NETTED_CSV = os.path.join(DATA, "dafrc-market-totals-netted.csv")
INDEX_YEARS = (2023, 2024, 2025, 2026)
F990_V = 1
UA = "research-script/1.0"
BANDS = ((0, 1e6, "a_lt_1m"), (1e6, 5e6, "b_1m_5m"), (5e6, 25e6, "c_5m_25m"), (25e6, 100e6, "d_25m_100m"),
         (100e6, float("inf"), "e_ge_100m"))
GROUPS = ("arts_culture", "education", "environment_animals", "health", "human_services", "international",
          "public_societal_benefit", "religion", "mutual_membership", "unknown_z", "no_ntee")
UNIV_NTEE = re.compile(r"^B(4[0-3]|50)")
HOSP_NTEE = re.compile(r"^E2[0-4]")
FDN_NTEE = re.compile(r"^T(2\d|30|31)")
UNIV_NAME = re.compile(r"\b(UNIVERSITY|UNIV|COLLEGE|REGENTS|INSTITUTE OF TECHNOLOGY)\b")
HOSP_NAME = re.compile(r"\b(HOSPITALS?|MEDICAL CENTER|HEALTH SYSTEM|HEALTHCARE SYSTEM)\b")
PF_CODES = frozenset({"02", "03", "04"})
SOURCE = ("Numerator: IRS Form 990 Schedule I Part II lines of the top-50 DAFRC sponsors (GivingTuesday mirror of IRS "
          "TEOS XML), net of DAF-to-DAF (daf-to-daf-recipient-whitelist.csv). Denominator: recipient Form 990 Part VIII "
          "line 1h / 990-EZ line 1 (same mirror; located via apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv). "
          "Sector and band: IRS EO BMF (www.irs.gov/pub/irs-soi/eo*.csv) NTEE_CD and REVENUE_AMT.")


# ----------------------------------------------------------------------------- numerator
def sponsor_weights(cost: Sequence[Mapping], keys: Iterable) -> dict:
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    return {k: min(1.0, max(0.0, share[k])) for k in keys if share.get(k) is not None}


def numerators(ann: Mapping, weights: Mapping) -> dict:
    """ann: (sponsor_ein, fy) -> annotated lines. -> recipient_ein -> {fy: {si, dw}, grantors}."""
    flat = ((r["ein"], k[1], k[0], r["amount"], r["amount"] * weights.get(k, 1.0))
            for k, rs in ann.items() for r in rs if r["ein"] and not r["d2d"] and r["amount"] > 0)
    return reduce(lambda acc, t: _merge(acc, *t), flat, {})


def _merge(acc: dict, e, fy, g, si, dw) -> dict:
    # accumulator-local mutation inside a reduce step (O(n)); the caller only sees the finished mapping
    cur = acc.setdefault(e, {"fy": {}, "grantors": set()})
    f = cur["fy"].setdefault(fy, {"si": 0.0, "dw": 0.0})
    f["si"] += si
    f["dw"] += dw
    cur["grantors"].add(g)
    return acc


def coverage_fy(ann: Mapping, weights: Mapping, fy: int) -> dict:
    kept = [(k, r) for k, rs in ann.items() if k[1] == fy for r in rs if not r["d2d"]]
    return {"sched_i_non_d2d": sum(r["amount"] for _, r in kept),
            "daf_weighted_non_d2d": sum(r["amount"] * weights.get(k, 1.0) for k, r in kept),
            "d2d_dropped": sum(r["amount"] for k, rs in ann.items() if k[1] == fy for r in rs if r["d2d"])}


# ----------------------------------------------------------------------------- frame (BMF)
def load_bmf(bmf_dir: str, eins: frozenset) -> dict:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple({"ein": ein9(r["EIN"]), "name": (r.get("NAME") or "").strip(),
                          "ntee": (r.get("NTEE_CD") or "").strip().upper(), "foundation": (r.get("FOUNDATION") or "").strip(),
                          "subsection": (r.get("SUBSECTION") or "").strip(), "revenue": num(r.get("REVENUE_AMT")),
                          "state": (r.get("STATE") or "").strip()}
                         for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    return {r["ein"]: r for f in BMF_FILES for r in rows(f)}


def group_of(ntee: str) -> str:
    return MAJOR.get(ntee[:1], "no_ntee") if ntee else "no_ntee"


def band_of(rev) -> str:
    v = max(0.0, rev or 0.0)
    return next(b for lo, hi, b in BANDS if lo <= v < hi)


def exclusion(b: Mapping, panel_eins: frozenset) -> str:
    nm = b["name"].upper()
    if b["ein"] in panel_eins:
        return "daf_sponsor"
    if b["subsection"] != "03":
        return "not_501c3"
    if UNIV_NTEE.match(b["ntee"]) or UNIV_NAME.search(nm):
        return "university"
    if HOSP_NTEE.match(b["ntee"]) or b["foundation"] == "12" or HOSP_NAME.search(nm):
        return "hospital"
    if FDN_NTEE.match(b["ntee"]) or b["foundation"] in PF_CODES:
        return "foundation"
    return ""


# ----------------------------------------------------------------------------- sample
def draw_sample(frame: Sequence[Mapping], certainty: int, per_stratum: int, seed: int) -> tuple[dict, ...]:
    ranked = sorted(frame, key=lambda r: (-r["num_si_total"], r["ein"]))
    cert = tuple({**r, "stratum": "certainty", "N_h": certainty} for r in ranked[:certainty])
    rest = ranked[certainty:]
    strata = _group_by_fast(rest, lambda r: f"{r['group']}|{r['band']}")
    rng = random.Random(seed)

    def pick(key):
        members = sorted(strata[key], key=lambda r: r["ein"])
        chosen = members if len(members) <= per_stratum else rng.sample(members, per_stratum)
        return tuple({**r, "stratum": key, "N_h": len(members)} for r in sorted(chosen, key=lambda r: r["ein"]))
    return cert + tuple(x for k in sorted(strata) for x in pick(k))


# ----------------------------------------------------------------------------- denominator (index + XML)
def load_index(index_dir: str, eins: frozenset) -> dict:
    def rows(y):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "return_type": d["RETURN_TYPE"],
                          "oid": d["OBJECT_ID"], "index_year": y}
                         for d in csv.DictReader(fh)
                         if d.get("RETURN_TYPE") in ("990", "990EZ") and ein9(d.get("EIN", "")) in eins)
    return {k: v for k, v in _group_by_fast((r for y in INDEX_YEARS for r in rows(y)), lambda r: r["ein"]).items()}


def choose_filings(filings: Sequence[Mapping]) -> dict:
    """-> fy -> filing. Latest object id per tax period (amendments supersede); per FY the latest tax period."""
    per_tp = {tp: max(v, key=lambda r: r["oid"]) for tp, v in _group_by_fast(filings, lambda r: r["tax_period"]).items()}
    by_fy = _group_by_fast(per_tp.values(), lambda r: int(r["tax_period"][:4]))
    return {fy: max(v, key=lambda r: r["tax_period"]) for fy, v in by_fy.items() if fy in FYS}


MAIN_FIELDS = {"TotalContributionsAmt": "contrib_1h", "ContributionsGiftsGrantsEtcAmt": "contrib_ez",
               "GovernmentGrantsAmt": "gov_grants_1e", "CYTotalRevenueAmt": "total_revenue",
               "TotalRevenueAmt": "total_revenue_alt", "CYContributionsGrantsAmt": "contrib_part_i_8"}


def parse_main(stream) -> dict:
    """Stream the return; stop at the end of IRS990 / IRS990EZ (schedules follow and are not needed)."""
    out = {}
    try:
        for _, el in ET.iterparse(stream, events=("end",)):
            tag = local(el.tag)
            if tag in MAIN_FIELDS and MAIN_FIELDS[tag] not in out and el.text:
                out[MAIN_FIELDS[tag]] = num(el.text)
            elif tag == "ReturnTypeCd" and el.text:
                out["return_type"] = el.text.strip()
            elif tag in ("IRS990", "IRS990EZ"):
                return {**out, "form": tag, "status": "ok"}
    except ET.ParseError:
        return {**out, "status": "parse_error"}
    return {**out, "status": "no_main_form"}


def fetch_main(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == F990_V:
            return c
    if not fetch:
        return {"status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                r = parse_main(resp)
            break
        except urllib.error.HTTPError as e:
            r = {"status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
            time.sleep(2 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            r = {"status": "error"}
            time.sleep(2 * (attempt + 1))
    obj = {**r, "oid": oid, "_v": F990_V}
    if r["status"] in ("ok", "http_404", "no_main_form", "parse_error"):
        os.makedirs(cache, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
    return obj


def denom_of(x: Mapping) -> float | None:
    return x.get("contrib_1h") if x.get("form") == "IRS990" else x.get("contrib_ez")


# ----------------------------------------------------------------------------- per-recipient
def recipient_row(s: Mapping, filings: Mapping, f990: Mapping) -> dict:
    yrs = tuple(fy for fy in FYS if fy in filings and f990.get(filings[fy]["oid"], {}).get("status") == "ok"
                and denom_of(f990[filings[fy]["oid"]]) is not None)
    nf = lambda fy, k: s["num"].get(fy, {}).get(k, 0.0)  # noqa: E731
    den = sum(denom_of(f990[filings[fy]["oid"]]) for fy in yrs)
    gov = sum(f990[filings[fy]["oid"]].get("gov_grants_1e") or 0.0 for fy in yrs)
    rev = sum((f990[filings[fy]["oid"]].get("total_revenue") or f990[filings[fy]["oid"]].get("total_revenue_alt") or 0.0)
              for fy in yrs)
    n_si = sum(nf(fy, "si") for fy in yrs)
    n_dw = sum(nf(fy, "dw") for fy in yrs)
    status = ("no_990_in_index" if not filings else "no_fy2023_2024_return" if not any(fy in filings for fy in FYS)
              else "xml_not_read" if not yrs else "zero_or_negative_contributions" if den <= 0 else "ok")
    ratio = lambda a, b: (a / b) if b and b > 0 else None  # noqa: E731
    return {"row_type": "recipient", "ein": s["ein"], "name": s["name"], "state": s["state"], "ntee_cd": s["ntee"],
            "ntee_major_group": s["group"], "revenue_band": s["band"], "bmf_revenue_amt": s["revenue"],
            "stratum": s["stratum"], "stratum_N": s["N_h"], "top50_grantors": s["grantors"],
            "num_sched_i_fy2023": round(nf(2023, "si")), "num_sched_i_fy2024": round(nf(2024, "si")),
            "num_sched_i_fy2023_2024_all": round(s["num_si_total"]),
            "years_matched": ";".join(map(str, yrs)), "forms": ";".join(f990[filings[fy]["oid"]]["form"] for fy in yrs),
            "object_ids": ";".join(filings[fy]["oid"] for fy in yrs),
            "num_sched_i_matched": round(n_si), "num_daf_weighted_matched": round(n_dw),
            "den_contributions_matched": round(den) if yrs else None, "den_gov_grants_1e_matched": round(gov) if yrs else None,
            "total_revenue_matched": round(rev) if yrs else None,
            "share_sched_i": ratio(n_si, den) if status == "ok" else None,
            "share_daf_weighted": ratio(n_dw, den) if status == "ok" else None,
            "share_of_private_contrib": ratio(n_dw, den - gov) if status == "ok" else None,
            "share_of_total_revenue": ratio(n_dw, rev) if status == "ok" else None,
            "status": status, "source": SOURCE}


# ----------------------------------------------------------------------------- weighted statistics
def wquantile(pairs: Sequence[tuple], q: float):
    xs = sorted((v, w) for v, w in pairs if v is not None)
    tot = sum(w for _, w in xs)
    if not xs or tot <= 0:
        return None
    cum = reduce(lambda acc, vw: acc + [acc[-1] + vw[1]], xs, [0.0])[1:]
    return next(v for (v, _), c in zip(xs, cum) if c >= q * tot)


def weights_of(rows: Sequence[Mapping]) -> dict:
    resp = _group_by_fast((r for r in rows if r["status"] == "ok"), lambda r: r["stratum"])
    return {k: v[0]["stratum_N"] / len(v) for k, v in resp.items()}


def pooled_of(ok: Sequence[Mapping], w: Mapping, num_key: str, den_fn=None, cap: bool = False):
    den_fn = den_fn or (lambda r: r["den_contributions_matched"])
    d = sum(w[r["stratum"]] * den_fn(r) for r in ok)
    n = sum(w[r["stratum"]] * (min(r[num_key], den_fn(r)) if cap else r[num_key]) for r in ok)
    return n / d if ok and d > 0 else None


def boot_ci(ok: Sequence[Mapping], w: Mapping, reps: int, seed: int) -> dict:
    """Stratified bootstrap (resample respondents with replacement within stratum, weights fixed at N_h / n_h)."""
    if len(ok) < 10:
        return {}
    by = _group_by_fast(ok, lambda r: r["stratum"])
    keys = sorted(by)
    rng = random.Random(seed)
    draws = tuple(tuple(x for k in keys for x in rng.choices(by[k], k=len(by[k]))) for _ in range(reps))
    pooled = sorted(p for p in (pooled_of(d, w, "num_daf_weighted_matched") for d in draws) if p is not None)
    med = sorted(m for m in (wquantile([(r["share_daf_weighted"], w[r["stratum"]]) for r in d], 0.5) for d in draws)
                 if m is not None)
    pct = lambda xs, q: xs[min(len(xs) - 1, int(q * len(xs)))] if xs else None  # noqa: E731
    return {"pooled_ci95_lo": pct(pooled, 0.025), "pooled_ci95_hi": pct(pooled, 0.975),
            "median_ci95_lo": pct(med, 0.025), "median_ci95_hi": pct(med, 0.975)}


def summarise(scope_type: str, scope: str, rows: Sequence[Mapping], w: Mapping, frame_n: int, frame_num: float,
              reps: int, seed: int) -> dict:
    ok = tuple(r for r in rows if r["status"] == "ok")
    wt = lambda r: w[r["stratum"]]  # noqa: E731
    priv = lambda r: r["den_contributions_matched"] - r["den_gov_grants_1e_matched"]  # noqa: E731
    q = lambda k, p: wquantile([(r[k], wt(r)) for r in ok], p)  # noqa: E731
    return {"row_type": "summary", "scope_type": scope_type, "scope": scope, "frame_recipients": frame_n,
            "frame_num_sched_i_fy2023_2024": round(frame_num), "sampled": len(rows), "respondents": len(ok),
            "weighted_recipients": round(sum(wt(r) for r in ok)),
            "p25_share_daf_weighted": q("share_daf_weighted", 0.25), "median_share_daf_weighted": q("share_daf_weighted", 0.5),
            "p75_share_daf_weighted": q("share_daf_weighted", 0.75), "median_share_sched_i": q("share_sched_i", 0.5),
            "pooled_share_sched_i": pooled_of(ok, w, "num_sched_i_matched"),
            "pooled_share_daf_weighted": pooled_of(ok, w, "num_daf_weighted_matched"),
            "pooled_share_daf_weighted_capped": pooled_of(ok, w, "num_daf_weighted_matched", cap=True),
            "pooled_share_of_private_contrib": pooled_of(ok, w, "num_daf_weighted_matched", priv),
            "share_gt_100pct": (sum(wt(r) for r in ok if (r["share_daf_weighted"] or 0) > 1) / sum(wt(r) for r in ok)) if ok else None,
            "share_ge_20pct": (sum(wt(r) for r in ok if (r["share_daf_weighted"] or 0) >= 0.2) / sum(wt(r) for r in ok)) if ok else None,
            **boot_ci(ok, w, reps, seed), "source": SOURCE}


INTERMEDIARY_NAME = re.compile(r"\b(FOUNDATION|FUND|TRUST|FDN)\b")


def view_of(f: Mapping, cert: frozenset) -> dict:
    return {"ntee_major_group": f["group"], "revenue_band": f["band"], "name": f["name"], "ntee_cd": f["ntee"],
            "stratum": "certainty" if f["ein"] in cert else "x"}


def build_summaries(rows: Sequence[Mapping], frame: Sequence[Mapping], scale: float | None, reps: int, seed: int) -> list:
    w = weights_of(rows)
    cert = frozenset(r["ein"] for r in rows if r["stratum"] == "certainty")
    not_interm = lambda r: not (r["ntee_cd"].startswith("T") or INTERMEDIARY_NAME.search(r["name"].upper()))  # noqa: E731
    scopes = ([("all", "all_ex_excluded", lambda r: True)]
              + [("sensitivity", "non_certainty_only", lambda r: r["stratum"] != "certainty")]
              + [("sensitivity", "ex_ntee_T_and_fund_foundation_trust_names", not_interm)]
              + [("ntee_major_group", g, (lambda r, g=g: r["ntee_major_group"] == g)) for g in GROUPS]
              + [("revenue_band", b, (lambda r, b=b: r["revenue_band"] == b)) for _, _, b in BANDS])
    views = tuple((f, view_of(f, cert)) for f in frame)

    def one(i, st, sc, pred):
        sub_f = tuple(f for f, v in views if pred(v))
        s = summarise(st, sc, [r for r in rows if pred(r)], w, len(sub_f), sum(f["num_si_total"] for f in sub_f),
                      reps, seed + i)
        inf = lambda k: (s[k] / scale) if s.get(k) is not None and scale else None  # noqa: E731
        return {**s, "scaled_pooled_share_inference": inf("pooled_share_daf_weighted"),
                "scaled_pooled_capped_inference": inf("pooled_share_daf_weighted_capped"),
                "scaled_median_share_inference": inf("median_share_daf_weighted")}
    return [one(i, *s) for i, s in enumerate(scopes)]


FIELDS = ("row_type", "scope_type", "scope", "frame_recipients", "frame_num_sched_i_fy2023_2024", "sampled", "respondents",
          "weighted_recipients", "p25_share_daf_weighted", "median_share_daf_weighted", "p75_share_daf_weighted",
          "median_ci95_lo", "median_ci95_hi", "median_share_sched_i", "pooled_share_sched_i", "pooled_share_daf_weighted",
          "pooled_ci95_lo", "pooled_ci95_hi", "pooled_share_daf_weighted_capped", "pooled_share_of_private_contrib",
          "share_gt_100pct", "share_ge_20pct", "scaled_pooled_share_inference", "scaled_pooled_capped_inference",
          "scaled_median_share_inference",
          "ein", "name", "state", "ntee_cd", "ntee_major_group", "revenue_band", "bmf_revenue_amt", "stratum", "stratum_N",
          "top50_grantors", "num_sched_i_fy2023", "num_sched_i_fy2024", "num_sched_i_fy2023_2024_all", "years_matched",
          "forms", "object_ids", "num_sched_i_matched", "num_daf_weighted_matched", "den_contributions_matched",
          "den_gov_grants_1e_matched", "total_revenue_matched", "share_sched_i", "share_daf_weighted",
          "share_of_private_contrib", "share_of_total_revenue", "status", "source")


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--f990-cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--seed", type=int, default=20261119)
    ap.add_argument("--per-stratum", type=int, default=40)
    ap.add_argument("--certainty", type=int, default=400)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--boot", type=int, default=500)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    present = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in present.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    weights = sponsor_weights(read_csv(COST), good)
    nums = numerators(ann, weights)

    bmf = load_bmf(a.bmf_dir, frozenset(nums))
    panel_eins = frozenset(panel)
    universe = tuple({**bmf[e], "group": group_of(bmf[e]["ntee"]), "band": band_of(bmf[e]["revenue"]),
                      "num": {fy: v for fy, v in n["fy"].items()}, "grantors": len(n["grantors"]),
                      "num_si_total": sum(v["si"] for v in n["fy"].values()),
                      "num_dw_total": sum(v["dw"] for v in n["fy"].values()),
                      "excl": exclusion(bmf[e], panel_eins)} for e, n in nums.items() if e in bmf)
    frame = tuple(u for u in universe if not u["excl"])
    sample = draw_sample(frame, a.certainty, a.per_stratum, a.seed)

    idx = load_index(a.index_dir, frozenset(s["ein"] for s in sample))
    filings = {s["ein"]: choose_filings(idx.get(s["ein"], ())) for s in sample}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values()})
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        f990 = dict(zip(oids, ex.map(lambda o: fetch_main(o, a.f990_cache, a.fetch), oids)))
    rec = [recipient_row(s, filings[s["ein"]], f990) for s in sample]

    cov24 = coverage_fy(ann, weights, 2024)
    cov23 = coverage_fy(ann, weights, 2023)
    mk = market(dafrc)
    net = {int(r["fiscal_year"]): num(r["netted_value"]) for r in read_csv(NETTED_CSV)
           if r["metric"] == "daf_grants" and r["tier"] == "central"}
    netted = net[2024]
    scale = cov24["daf_weighted_non_d2d"] / netted
    summ = build_summaries(rec, frame, scale, a.boot, a.seed)
    write_csv(a.out, summ + sorted(rec, key=lambda r: (r["stratum"] != "certainty", r["stratum"], r["ein"])), FIELDS)

    excl_mix = {k: {"recipients": len(v), "num_sched_i_fy2023_2024": round(sum(u["num_si_total"] for u in v))}
                for k, v in sorted(_group_by_fast(universe, lambda u: u["excl"] or "kept").items())}
    no_bmf = {e: n for e, n in nums.items() if e not in bmf}
    summary = {
        "sponsor_years_itemised_loaded": len(good), "daf_weight_coverage": f"{len(weights)}/{len(good)}",
        "recipient_eins_with_positive_numerator": len(nums),
        "numerator_total_sched_i_fy2023_2024": round(sum(sum(v["si"] for v in n["fy"].values()) for n in nums.values())),
        "numerator_total_daf_weighted_fy2023_2024": round(sum(sum(v["dw"] for v in n["fy"].values()) for n in nums.values())),
        "not_in_bmf": {"recipients": len(no_bmf), "num_sched_i": round(sum(sum(v["si"] for v in n["fy"].values()) for n in no_bmf.values()))},
        "exclusion_mix": excl_mix, "frame_recipients": len(frame),
        "frame_num_sched_i": round(sum(f["num_si_total"] for f in frame)),
        "certainty_num_share_of_frame": sum(s["num_si_total"] for s in sample if s["stratum"] == "certainty")
        / sum(f["num_si_total"] for f in frame),
        "certainty_min_num": round(min(s["num_si_total"] for s in sample if s["stratum"] == "certainty")),
        "sample": len(sample), "strata": len({s["stratum"] for s in sample}), "oids": len(oids),
        "f990_status": {k: len(v) for k, v in _group_by_fast(f990.values(), lambda x: x["status"]).items()},
        "recipient_status": {k: len(v) for k, v in _group_by_fast(rec, lambda r: r["status"]).items()},
        "status_by_stratum_kind": {k: {s: len(x) for s, x in _group_by_fast(v, lambda r: r["status"]).items()}
                                   for k, v in _group_by_fast(rec, lambda r: "certainty" if r["stratum"] == "certainty" else "random").items()},
        "coverage_fy2024": {**{k: round(v) for k, v in cov24.items()}, "dafrc_fy2024_total_daf_grants": round(mk[2024]["grants"]),
                            "netted_central_fy2024": round(netted), "top50_share_of_netted": scale,
                            "top50_sched_i_share_of_netted": cov24["sched_i_non_d2d"] / netted,
                            "top50_share_of_dafrc_raw": cov24["daf_weighted_non_d2d"] / mk[2024]["grants"]},
        "coverage_fy2023": {**{k: round(v) for k, v in cov23.items()}, "netted_central_fy2023": round(net[2023]),
                            "top50_share_of_netted": cov23["daf_weighted_non_d2d"] / net[2023],
                            "dafrc_fy2023_total_daf_grants": round(mk[2023]["grants"])},
        "form_mix_ok": {k: len(v) for k, v in _group_by_fast((r for r in rec if r["status"] == "ok"), lambda r: r["forms"]).items()},
        "summaries": [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in s.items() if k != "source"} for s in summ],
        "top_shares_certainty": sorted(({"name": r["name"][:40], "ntee": r["ntee_cd"], "share": round(r["share_daf_weighted"], 3),
                                         "num": r["num_daf_weighted_matched"], "den": r["den_contributions_matched"]}
                                        for r in rec if r["status"] == "ok" and r["stratum"] == "certainty"),
                                       key=lambda d: -d["share"])[:15],
        "largest_certainty": sorted(({"name": r["name"][:40], "ntee": r["ntee_cd"], "share": round(r["share_daf_weighted"] or 0, 3),
                                      "num": r["num_daf_weighted_matched"], "den": r["den_contributions_matched"], "status": r["status"]}
                                     for r in rec if r["stratum"] == "certainty"), key=lambda d: -(d["num"] or 0))[:15],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
