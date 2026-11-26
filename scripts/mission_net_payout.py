#!/usr/bin/env python3
"""Payout net of DAF-to-DAF (sponsor-to-sponsor) transfers, by sponsor segment (queue item Q-N06).

Stdlib only; functional style (pure transforms, I/O at the edges). Reuses the index/return-selection
helpers of scripts/mission_990_contractors.py.

Sources (documented in research/mission-2026-11-14/queue-net-payout-fidelity-outliers.md):
  * Sponsor universe and segments: DAFRC panel data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv
    (DAFRC Annual DAF Report 2025 - Updated Analysis dataset)
  * Return locator: IRS TEOS e-file index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv
  * Return content: IRS e-file XML via the GivingTuesday mirror
    https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml

What is parsed from each Form 990 (FY2021-FY2024 in full; FY2020 only through Schedule D for beginning assets):
  * Schedule D Part I: DAF count, contributions, grants (I-3), end-of-year value (I-4)
  * Part IX line 1 (GrantsToDomesticOrgsGrp/TotalAmt): all grants to domestic organisations, any size
  * Schedule I Part II RecipientTable: every line (recipient EIN, name, cash, non-cash, purpose). Lines whose
    recipient EIN is a DAFRC panel EIN (or, when the EIN is blank, whose normalised name matches one panel
    name uniquely) are kept individually; the rest only enter totals. The 25 largest lines are kept too.

Definitions (fiscal year = calendar year in which the tax period ends, as in the rest of the repo):
  gross_payout      = Sch D I-3 DAF grants_t / Sch D I-4 DAF assets_{t-1}
  sponsor_transfers = Schedule I grants_t to recipients in the DAFRC panel, three nested tiers:
                        tier_a  national sponsors, subtype Standard
                        tier_b  tier_a + national donation processors + community foundations
                        tier_c  every DAFRC panel EIN (adds single-issue, religious, university/hospital sponsors)
  net_payout_<tier> = (DAF grants_t - min(sponsor_transfers_<tier>, DAF grants_t)) / DAF assets_{t-1}

Usage:
  python3 scripts/mission_net_payout.py --irs-dir DIR --cache-dir CACHE [--fetch] [--workers 16]
  DIR holds index_2020.csv .. index_2026.csv.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import (  # noqa: E402  (reuse, no duplication)
    DAFRC_CSV, DATA, INDEX_URL, NS, XML_URL, ein9, load_index, local, num, read_csv, text_of, write_csv,
    _group_by_fast)

PAYOUT_FYS = (2021, 2022, 2023, 2024)
BOY_FY = 2020
INDEX_YEARS = tuple(range(2020, 2027))
EXTRACT_VERSION = 1
MIN_BOY = 1_000_000
COVERAGE_OK = 0.5
SEGMENTS = ("national", "processor", "community_foundation", "single_issue", "university_hospital")
TIERS = ("tier_a", "tier_b", "tier_c")
FILED_SOURCES = frozenset({"IRS 990", "NPT historical data", "paper submission"})


# ----------------------------------------------------------------------------- pure helpers
def segment_of(dtype: str, subtype: str) -> str:
    if dtype == "National":
        return "processor" if subtype == "Donation Processor" else "national"
    if dtype == "Community Foundation":
        return "community_foundation"
    return "university_hospital" if subtype == "Universities and Healthcare" else "single_issue"


def tier_of(segment: str) -> str:
    """Narrowest tier a recipient belongs to (tiers are nested)."""
    return {"national": "tier_a", "processor": "tier_b", "community_foundation": "tier_b"}.get(segment, "tier_c")


def in_tier(recipient_tier: str, tier: str) -> bool:
    return TIERS.index(recipient_tier) <= TIERS.index(tier)


STOP = frozenset({"THE", "INC", "INCORPORATED", "CORP", "CORPORATION", "CO", "OF", "AND", "A", "LTD", "TRUST"})


def norm_name(s: str) -> str:
    toks = re.sub(r"[^A-Z0-9 ]", " ", (s or "").upper().replace("&", " AND ")).split()
    return " ".join(t for t in toks if t not in STOP)


def panel_from(rows: Sequence[Mapping]) -> dict[str, dict]:
    """EIN -> latest DAFRC name/type/subtype/segment plus per-FY values."""
    by = _group_by_fast(rows, lambda r: ein9(r["ein"]))

    def one(ein, rs):
        latest = max(rs, key=lambda r: r["fiscal_year_end"])
        return {"ein": ein, "name": latest["name"], "type": latest["type"], "subtype": latest["subtype"],
                "segment": segment_of(latest["type"], latest["subtype"]),
                "fy": {int(r["fiscal_year_end"]): r for r in rs}}
    return {e: one(e, rs) for e, rs in by.items()}


def name_map(panel: Mapping) -> dict[str, str]:
    by = _group_by_fast(panel.values(), lambda p: norm_name(p["name"]))
    return {k: v[0]["ein"] for k, v in by.items() if k and len(v) == 1}


def candidates(filings: Sequence[Mapping], fy: int) -> tuple[dict, ...]:
    """Latest submission (amended supersedes original) for each tax period ending in fy."""
    c = tuple(f for f in filings if f["return_type"] == "990" and int(f["tax_period"][:4]) == fy)
    by = _group_by_fast(c, lambda f: f["tax_period"])
    return tuple(max(v, key=lambda f: f["object_id"]) for _, v in sorted(by.items()))


def choose(cands: Sequence[Mapping], extracts: Mapping) -> dict | None:
    """When a fiscal year holds more than one tax period (short years, FYE changes), keep the return that
    carries Schedule D DAF values; among those the largest |DAF grants|; else the latest tax period."""
    if not cands:
        return None
    scored = tuple((extracts.get(c["object_id"], {}).get("sched_d_daf_grants") is not None,
                    abs(extracts.get(c["object_id"], {}).get("sched_d_daf_grants") or 0), c["tax_period"], c["object_id"], c)
                   for c in cands)
    return max(scored, key=lambda t: t[:4])[-1]


NOT_ITEMIZED = re.compile(r"\b(SEE|VIEW)\b.*\b(ATTACH|STATEMENT|SCHEDULE|LIST|REPORT)|ATTACHED", re.I)


def itemized(ex: Mapping) -> bool:
    """False when Schedule I points to an attachment instead of itemising recipients (e.g. RCF, BofA CGF)."""
    top = ex.get("sched_i_top_lines", ())
    total = ex.get("sched_i_total") or 0
    attach = sum(l["cash"] + l["noncash"] for l in top if NOT_ITEMIZED.search(l["recipient_name"] or ""))
    return not (total and attach >= 0.5 * total)


# ----------------------------------------------------------------------------- XML extract (streamed)
def recipient_line(el) -> dict:
    g = {local(c.tag): c for c in el.iter()}
    name = " ".join((c.text or "").strip() for c in el.iter()
                    if local(c.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt") and c.text)
    t = lambda k: (g[k].text or "").strip() if k in g and g[k].text else ""  # noqa: E731
    return {"recipient_ein": ein9(t("RecipientEIN")) if t("RecipientEIN") else "", "recipient_name": name,
            "cash": num(t("CashGrantAmt")) or 0.0, "noncash": num(t("NonCashAssistanceAmt")) or 0.0,
            "purpose": t("PurposeOfGrantTxt")[:120]}


def extract_stream(stream, panel_eins: frozenset, names: Mapping, full: bool) -> dict:
    head, sd, ix = {}, {}, {}
    lines_n, total, kept, top = 0, 0.0, [], []
    for event, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "ReturnHeader":
            head = {"tax_period_end": text_of(el, ("TaxPeriodEndDt",)), "return_ts": text_of(el, ("ReturnTs",)),
                    "filer_ein": text_of(el, ("Filer", "EIN")),
                    "filer_name": text_of(el, ("Filer", "BusinessName", "BusinessNameLine1Txt"))}
            el.clear()
        elif tag == "IRS990":
            ix = {"part_ix_line1_grants_domestic_orgs": num(text_of(el, ("GrantsToDomesticOrgsGrp", "TotalAmt"))),
                  "amended_ind": text_of(el, ("AmendedReturnInd",))}
            el.clear()
        elif tag == "IRS990ScheduleD":
            sd = {"sched_d_daf_count": num(text_of(el, ("DonorAdvisedFundsHeldCnt",))),
                  "sched_d_daf_contributions": num(text_of(el, ("DonorAdvisedFundsContriAmt",))),
                  "sched_d_daf_grants": num(text_of(el, ("DonorAdvisedFundsGrantsAmt",))),
                  "sched_d_daf_eoy_value": num(text_of(el, ("DonorAdvisedFundsVlEOYAmt",)))}
            el.clear()
            if not full:
                break
        elif tag == "RecipientTable":
            ln = recipient_line(el)
            amt = ln["cash"] + ln["noncash"]
            lines_n, total = lines_n + 1, total + amt
            match = ln["recipient_ein"] if ln["recipient_ein"] in panel_eins else (
                names.get(norm_name(ln["recipient_name"]), "") if not ln["recipient_ein"] else "")
            if match:
                kept.append({**ln, "matched_ein": match, "match_method": "ein" if ln["recipient_ein"] else "name"})
            top = sorted(top + [ln], key=lambda x: -(x["cash"] + x["noncash"]))[:25]
            el.clear()
        elif tag.startswith("IRS990Schedule"):
            el.clear()
    return {**head, **ix, **sd, "sched_i_lines": lines_n, "sched_i_total": total,
            "sched_i_panel_lines": kept, "sched_i_top_lines": top, "parsed_sched_i": int(full)}


def fetch_extract(oid: str, cache_dir: str, fetch: bool, panel_eins: frozenset, names: Mapping,
                  full: bool, local_dirs: Sequence[str] = (), retries: int = 2) -> dict:
    path = os.path.join(cache_dir, "netpayout990", f"{oid}{'' if full else '_d'}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == EXTRACT_VERSION:
            return c
    url = XML_URL.format(oid=oid)
    localp = next((p for d in local_dirs for p in (os.path.join(d, f"{oid}.xml"), os.path.join(d, f"{oid}_public.xml"))
                   if os.path.exists(p)), "")
    if localp:
        with open(localp, "rb") as fh:
            out = {**extract_stream(fh, panel_eins, names, full), "xml_status": "ok"}
    elif not fetch:
        return {"xml_status": "not_fetched", "xml_url": url}
    else:
        req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
        out = {"xml_status": "error"}
        for attempt in range(retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    out = {**extract_stream(resp, panel_eins, names, full), "xml_status": "ok"}
                break
            except urllib.error.HTTPError as e:
                out = {"xml_status": f"http_{e.code}"}
                if e.code in (403, 404):
                    break
            except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
                out = {"xml_status": f"error:{type(e).__name__}"}
                time.sleep(2 * (attempt + 1))
    res = {**out, "_v": EXTRACT_VERSION, "xml_url": url}
    if not res["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(res, fh)
    return res


# ----------------------------------------------------------------------------- sponsor-year rows
def transfers_by_tier(lines: Sequence[Mapping], grantor_ein: str, panel: Mapping) -> dict:
    valid = tuple(l for l in lines if l["matched_ein"] != grantor_ein)
    amt = lambda l: l["cash"] + l["noncash"]  # noqa: E731
    rt = lambda l: tier_of(panel[l["matched_ein"]]["segment"])  # noqa: E731
    by_seg = {s: sum(amt(l) for l in valid if panel[l["matched_ein"]]["segment"] == s) for s in SEGMENTS}
    top = max(valid, key=amt, default=None)
    return {**{f"transfers_{t}": sum(amt(l) for l in valid if in_tier(rt(l), t)) for t in TIERS},
            **{f"transfers_to_{s}": v for s, v in by_seg.items()},
            "transfers_noncash_tier_c": sum(l["noncash"] for l in valid),
            "transfer_recipients_tier_c": len({l["matched_ein"] for l in valid}),
            "name_matched_lines": sum(1 for l in valid if l["match_method"] == "name"),
            "largest_transfer_recipient": "" if top is None else panel[top["matched_ein"]]["name"],
            "largest_transfer_usd": 0 if top is None else amt(top)}


def capped(t, grants):
    return min(max(t or 0, 0), max(grants or 0, 0))


def ratio(n, d):
    return None if n is None or not d else n / d


def sponsor_year(p: Mapping, fy: int, ret: Mapping | None, ex: Mapping, prev_ex: Mapping | None, panel: Mapping) -> dict:
    dafrc = p["fy"].get(fy, {})
    dprev = p["fy"].get(fy - 1, {})
    boy_990 = (prev_ex or {}).get("sched_d_daf_eoy_value")
    dprev_filed = dprev.get("source_eoy_daf_assets") in FILED_SOURCES
    boy, boy_src = ((boy_990, "990_prior_fy_sched_d") if boy_990 is not None else
                    (num(dprev.get("eoy_daf_assets")), f"dafrc_{'filed' if dprev_filed else 'imputed'}")
                    if dprev.get("eoy_daf_assets") else (None, "missing"))
    grants = ex.get("sched_d_daf_grants")
    neg = grants is not None and grants < 0
    tr = transfers_by_tier(ex.get("sched_i_panel_lines", ()), p["ein"], panel) if ex.get("xml_status") == "ok" else {}
    six, p9 = ex.get("sched_i_total"), ex.get("part_ix_line1_grants_domestic_orgs")
    cov = ratio(six, p9)
    item = int(ex.get("xml_status") == "ok" and itemized(ex) and cov is not None and cov >= COVERAGE_OK)
    net = {t: (None if grants is None or not tr or not item else grants - capped(tr[f"transfers_{t}"], grants)) for t in TIERS}
    usable = (grants is not None and not neg and boy is not None and boy >= MIN_BOY and boy_src != "dafrc_imputed"
              and ex.get("xml_status") == "ok")
    excl = ("" if usable else "; ".join(filter(None, (
        "no_return_parsed" if ex.get("xml_status") != "ok" else "",
        "sched_d_grants_missing" if grants is None else "", "sched_d_grants_negative" if neg else "",
        "boy_missing" if boy is None else "", "boy_lt_1m" if boy is not None and boy < MIN_BOY else "",
        "boy_dafrc_imputed" if boy_src == "dafrc_imputed" else ""))))
    return {"ein": p["ein"], "sponsor_name": p["name"], "dafrc_type": p["type"], "dafrc_subtype": p["subtype"],
            "segment": p["segment"], "fiscal_year": fy,
            "tax_period_end": ex.get("tax_period_end", ""), "object_id": (ret or {}).get("object_id", ""),
            "xml_status": ex.get("xml_status", "no_990_in_index"),
            "boy_daf_assets": boy, "boy_source": boy_src,
            "daf_grants_sched_d": grants, "daf_eoy_assets_sched_d": ex.get("sched_d_daf_eoy_value"),
            "daf_contributions_sched_d": ex.get("sched_d_daf_contributions"),
            "dafrc_total_daf_grants": num(dafrc.get("total_daf_grants")), "dafrc_grants_source": dafrc.get("source_total_daf_grants", ""),
            "part_ix_line1_grants": p9, "sched_i_lines": ex.get("sched_i_lines"), "sched_i_total": six,
            "sched_i_coverage_of_part_ix": cov,
            "sched_i_itemized_ok": item, "sched_i_points_to_attachment": int(ex.get("xml_status") == "ok" and not itemized(ex)),
            **{k: tr.get(k) for k in [f"transfers_{t}" for t in TIERS] + [f"transfers_to_{s}" for s in SEGMENTS]
               + ["transfers_noncash_tier_c", "transfer_recipients_tier_c", "name_matched_lines",
                  "largest_transfer_recipient", "largest_transfer_usd"]},
            "transfer_share_of_daf_grants_tier_a": ratio(tr.get("transfers_tier_a"), grants),
            "transfer_share_of_daf_grants_tier_c": ratio(tr.get("transfers_tier_c"), grants),
            "gross_payout": ratio(grants, boy),
            **{f"net_payout_{t}": ratio(net[t], boy) for t in TIERS},
            "in_payout_sample": int(usable), "exclusion_reason": excl,
            "xml_url": ex.get("xml_url", ""), "boy_xml_url": (prev_ex or {}).get("xml_url", "")}


# ----------------------------------------------------------------------------- aggregation
def pct(xs: Sequence[float], q: float):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def summarise(rows: Sequence[Mapping], label: str, segment: str, fy, itemized_only: bool) -> dict:
    s = tuple(r for r in rows if r["in_payout_sample"] and (not itemized_only or r["sched_i_itemized_ok"]))
    s_net = tuple(r for r in s if r["sched_i_itemized_ok"])
    boy = sum(r["boy_daf_assets"] for r in s)
    g = sum(r["daf_grants_sched_d"] for r in s)
    trc = {t: sum(capped(r[f"transfers_{t}"], r["daf_grants_sched_d"]) for r in s_net) for t in TIERS}
    gp = tuple(r["gross_payout"] for r in s)
    na = tuple(r["net_payout_tier_a"] for r in s_net)
    nc = tuple(r["net_payout_tier_c"] for r in s_net)
    return {"segment": segment, "fiscal_year": fy, "sample": label, "sponsor_years": len(s),
            "sponsors": len({r["ein"] for r in s}), "sponsor_years_not_itemized": len(s) - len(s_net),
            "boy_daf_assets": boy, "daf_grants": g,
            **{f"transfers_{t}": trc[t] for t in TIERS},
            "transfer_share_tier_a": ratio(trc["tier_a"], g), "transfer_share_tier_c": ratio(trc["tier_c"], g),
            "agg_gross_payout": ratio(g, boy),
            **{f"agg_net_payout_{t}": ratio(g - trc[t], boy) for t in TIERS},
            "median_gross_payout": pct(gp, .5), "median_net_payout_tier_a": pct(na, .5),
            "median_net_payout_tier_c": pct(nc, .5),
            "p25_gross_payout": pct(gp, .25), "p75_gross_payout": pct(gp, .75),
            "share_below_5pct_gross": ratio(sum(1 for x in gp if x < .05), len(gp)),
            "share_below_5pct_net_tier_c": ratio(sum(1 for x in nc if x < .05), len(nc)),
            "sponsors_with_any_tier_c_transfer": sum(1 for r in s if (r["transfers_tier_c"] or 0) > 0)}


def summary_rows(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    keys = [(seg, fy) for seg in SEGMENTS + ("all_ex_processor", "all") for fy in PAYOUT_FYS + ("FY2021-2024",)]
    segok = lambda seg, r: seg == "all" or r["segment"] == seg or (seg == "all_ex_processor" and r["segment"] != "processor")  # noqa: E731
    pick = lambda seg, fy: tuple(r for r in rows if segok(seg, r)  # noqa: E731
                                 and (fy == "FY2021-2024" or r["fiscal_year"] == fy))
    return tuple(summarise(pick(seg, fy), lab, seg, fy, io) for seg, fy in keys
                 for lab, io in (("itemized_only", True), ("all_in_sample", False)))


def fmt(v):
    if isinstance(v, float):
        return f"{v:.6f}" if abs(v) < 10 else f"{v:.0f}"
    return "" if v is None else v


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/daf-landscape"))
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--local-xml-dir", action="append", default=[], help="dirs holding already-downloaded {oid}.xml")
    ap.add_argument("--out-dir", default=DATA)
    a = ap.parse_args(argv)

    panel = panel_from(read_csv(DAFRC_CSV))
    eins, names = frozenset(panel), name_map(panel)
    idx_paths = tuple(p for y in INDEX_YEARS for p in (os.path.join(a.irs_dir, f"index_{y}.csv"),) if os.path.exists(p))
    index = load_index(idx_paths, eins)
    # sponsors in scope: any DAFRC row FY2021-2024
    scope = tuple(p for p in panel.values() if any(fy in p["fy"] for fy in PAYOUT_FYS))
    cands = {(p["ein"], fy): candidates(index.get(p["ein"], ()), fy) for p in scope for fy in (BOY_FY,) + PAYOUT_FYS}
    jobs = tuple(dict.fromkeys((c["object_id"], fy != BOY_FY) for (e, fy), cs in cands.items() for c in cs))
    print(f"{len(scope)} sponsors; {len(jobs)} returns to parse", file=sys.stderr)
    t0 = time.time()

    def job(j):
        return j, fetch_extract(j[0], a.cache_dir, a.fetch, eins, names, j[1], a.local_xml_dir)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = dict(ex.map(job, sorted(jobs, key=lambda j: j[0])))
    print(f"parsed in {time.time() - t0:.0f}s", file=sys.stderr)
    rets = {(e, fy): choose(cs, {c["object_id"]: res.get((c["object_id"], fy != BOY_FY), {}) for c in cs})
            for (e, fy), cs in cands.items()}
    get = lambda e, fy: res.get((rets[(e, fy)]["object_id"], fy != BOY_FY), {}) if rets.get((e, fy)) else {}  # noqa: E731

    rows = tuple(sponsor_year(p, fy, rets.get((p["ein"], fy)), get(p["ein"], fy), get(p["ein"], fy - 1) or None, panel)
                 for p in sorted(scope, key=lambda p: p["ein"]) for fy in PAYOUT_FYS
                 if fy in p["fy"] or rets.get((p["ein"], fy)))
    fields = list(rows[0].keys())
    write_csv(os.path.join(a.out_dir, "net-payout-by-sponsor.csv"), [{k: fmt(v) for k, v in r.items()} for r in rows], fields)
    summ = summary_rows(rows)
    write_csv(os.path.join(a.out_dir, "net-payout-summary.csv"), [{k: fmt(v) for k, v in r.items()} for r in summ],
              list(summ[0].keys()))
    # side outputs for the report (scratch): top lines of selected filers
    side = {oid: {"top": x.get("sched_i_top_lines", []), "tp": x.get("tax_period_end"), "lines": x.get("sched_i_lines"),
                  "total": x.get("sched_i_total"), "panel": x.get("sched_i_panel_lines", [])}
            for (oid, full), x in res.items() if full}
    with open(os.path.join(a.cache_dir, "netpayout-side.json"), "w") as fh:
        json.dump({"rets": {f"{e}|{fy}": r for (e, fy), r in rets.items() if r}, "side": side}, fh)
    st = _group_by_fast(rows, lambda r: r["xml_status"])
    print(json.dumps({k: len(v) for k, v in st.items()}), file=sys.stderr)
    print(f"rows={len(rows)} in_sample={sum(r['in_payout_sample'] for r in rows)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
