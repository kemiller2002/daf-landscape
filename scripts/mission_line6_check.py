#!/usr/bin/env python3
"""Form 990 Part IV line 6 ("did the organization maintain any donor advised funds?") against Schedule D Part I
(task g1915b-04, queue item P-G1915B-04).

Two disagreements are counted on every Form 990 already parsed in the repo's harvests and caches:

  forward   line 6 is not "Yes" (No or blank) but Schedule D Part I reports DAF accounts > 0
            (DonorAdvisedFundsHeldCnt). These returns are invisible to any screen that keys on line 6, such as the
            IRS SOI annual extract (field dnradvisedfundscd; the extract carries no Schedule D field).
  reverse   line 6 is "Yes" but Schedule D Part I DAF accounts are missing (no Schedule D, or the Part I DAF column
            blank) or zero.

Return-level inputs (one record per OBJECT_ID; nothing is fetched, every input is a cache or CSV made by an earlier,
validated repo run):
  harvest   data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv, form990-harvest-fy2025-refresh.csv
            and form990-harvest-2026-fill.csv: all 1,512 DAFRC FY2024 sponsors, FY2022-FY2025 returns
  extract   DAFRC-sponsor extract cache of mission_990_contractors.py (--extract-cache; returns filed 2020-2026)
  nondafrc  data/mission-2026-11-14/non-dafrc-daf-filers-990.csv: every non-DAFRC (EIN, tax period) answering line 6
            "Y" in the SOI extracts 20-25, with Schedule D Part I parsed (P-MOR-01)
  frames    gap1915-b4011 full-read cache (--frames-cache): frame A (new 501(c)(3)s ruled 2021+, all 990s 2022-2026)
            and frame B (CF-named or NTEE T31 filers, all 990/990-EZ 2021-2026)
  l6        batch-37 line-6 screen cache (--l6-cache): newest FY2022+ return of 9,566 T30/T31/T70/DAF-named EINs
  ft        batch-38 full-text screen cache (--ft-cache): newest FY2022+ return of 126,736 501(c)(3) EINs that answer
            line 6 "N" in the SOI extract with >= $1m of assets
The IRS TEOS index (--irs-dir, index_2019..2026.csv) supplies EIN, tax period and return type where a cache lacks
them, the count of all Form 990 returns per fiscal year (coverage denominator), and later returns for the same
EIN and period that were not read. The SOI extracts (--soi-dir, {yy}eoextract990.csv, yy=20..25) supply the line 6
value as the SOI file carries it. The DAFRC sponsor dataset (dafrc-sponsor-schedule-d-fy2019-2024.csv) supplies
panel membership and the value DAFRC published for the same fiscal year.

Fiscal year (FY) = calendar year of the tax-period end, as in DAFRC. Scope: Form 990 only (990-EZ has no Schedule
D Part I), FY 2021 onward. Per (EIN, tax period) the newest return read is the effective return (highest OBJECT_ID,
which leads with the IRS processing year, so an amended return filed later supersedes the original); counts are given for effective returns and, separately, for all returns read.

Usage:
  python3 scripts/mission_line6_check.py . --irs-dir IRS --soi-dir SOI --frames-cache DIR --ft-cache DIR
         --l6-cache DIR --extract-cache DIR [--summary OUT.json]

Writes data/mission-2026-11-14/line6-vs-schedule-d-2026-11-19.csv and prints a JSON summary. Stdlib only;
functional style (pure transforms, I/O at the edges).
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from collections import Counter, defaultdict
from functools import reduce
from typing import Iterable, Mapping, Sequence

DATA = "data/mission-2026-11-14"
OUT = f"{DATA}/line6-vs-schedule-d-2026-11-19.csv"
HARVESTS = (f"{DATA}/form990-harvest-fy2025-refresh.csv", f"{DATA}/form990-harvest-2026-fill.csv",
            f"{DATA}/form990-returns-schedule-d-harvest-full.csv")
NONDAFRC = f"{DATA}/non-dafrc-daf-filers-990.csv"
DAFRC = f"{DATA}/dafrc-sponsor-schedule-d-fy2019-2024.csv"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
SOI_URL = "https://www.irs.gov/pub/irs-soi/{yy}eoextract990.zip"
MIN_FY = 2021
# Source priority when two sources parse the same OBJECT_ID (sources that keep blank distinct from 0 come first).
PRIORITY = ("harvest", "extract", "l6", "ft", "nondafrc", "frames")
FIELDS = ("case", "subcase", "ein", "name", "fiscal_year", "tax_period", "return_object_id", "amended", "return_ts",
          "line6_raw", "line6", "soi_line6", "soi_extract_file", "sched_d_present", "daf_count", "daf_eoy",
          "daf_contributions", "daf_grants", "total_assets_eoy", "plausible", "in_dafrc_panel", "dafrc_row_same_fy",
          "dafrc_source_eoy_same_fy", "dafrc_eoy_same_fy", "dafrc_accounts_same_fy", "dafrc_status_same_fy",
          "line6_screen_drops", "dafrc_captures_same_fy", "prior_positive_period", "prior_positive_daf_count",
          "prior_positive_daf_eoy", "ein_line6_yes_in_any_return_read", "returns_read_same_period", "unread_later_return_in_index", "sources", "xml_url")


# ----------------------------------------------------------------------------- small pure helpers
def num(v) -> float | None:
    if v is None:
        return None
    s = str(v).strip().replace(",", "")
    if s == "" or s.lower() in ("none", "null", "nan"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def ein9(v) -> str:
    s = "".join(ch for ch in str(v or "") if ch.isdigit())
    return s.zfill(9) if s else ""


def line6_of(raw) -> str:
    s = str(raw if raw is not None else "").strip().lower()
    return "Y" if s in ("1", "true", "x", "y", "yes") else "N" if s in ("0", "false", "n", "no") else ""


def period_of(tax_period_end: str) -> str:
    s = (tax_period_end or "").replace("-", "")
    return s[:6] if len(s) >= 6 and s[:6].isdigit() else ""


def read_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else f"{v:.6g}"
    return str(v)


# ----------------------------------------------------------------------------- source readers -> normalised records
def rec(src, oid, ein="", name="", form="", period="", ts="", amended="", line6_raw=None, sd=None, cnt=None,
        eoy=None, contri=None, grants=None, assets=None) -> dict:
    return {"src": src, "oid": str(oid), "ein": ein9(ein), "name": name or "", "form": form or "", "period": period,
            "ts": ts or "", "amended": amended or "", "line6_raw": "" if line6_raw is None else str(line6_raw),
            "sd": sd, "cnt": num(cnt), "eoy": num(eoy), "contri": num(contri), "grants": num(grants),
            "assets": num(assets)}


def from_harvest(rows: Iterable[Mapping]) -> list[dict]:
    return [rec("harvest", r["return_object_id"], r["ein"], r.get("filer_name_990") or r.get("sponsor_name"),
                r.get("return_type"), period_of(r.get("tax_period_end", "")) or r.get("tax_period", ""),
                r.get("return_ts"), r.get("amended_ind"), r.get("daf_ind_part_iv"),
                num(r.get("sched_d_present")), r.get("sched_d_daf_count"), r.get("sched_d_daf_eoy_value"),
                r.get("sched_d_daf_contributions"), r.get("sched_d_daf_grants"), r.get("total_assets_eoy"))
            for r in rows if r.get("return_object_id") and (r.get("xml_status") or "").startswith("ok")]


def from_nondafrc(rows: Iterable[Mapping]) -> list[dict]:
    return [rec("nondafrc", r["return_object_id"], r["ein"], r.get("name"), "990", r.get("tax_pd", ""),
                r.get("return_ts"), "", r.get("daf_ind_part_iv_xml"), None, r.get("sched_d_daf_count"),
                r.get("sched_d_daf_eoy_value"), r.get("sched_d_daf_contributions"), r.get("sched_d_daf_grants"),
                r.get("total_assets_eoy"))
            for r in rows if r.get("return_object_id")]


def from_extract(path: str) -> dict | None:
    d = read_json(path)
    oid = os.path.basename(path)[:-5]
    return (rec("extract", oid, d.get("filer_ein"), d.get("filer_name"), d.get("return_type"),
                period_of(d.get("tax_period_end", "")), d.get("return_ts"), d.get("amended_ind"),
                d.get("daf_ind_part_iv"), d.get("sched_d_present"), d.get("sched_d_daf_count"),
                d.get("sched_d_daf_eoy_value"), d.get("sched_d_daf_contributions"), d.get("sched_d_daf_grants"),
                d.get("total_assets_eoy"))
            if d.get("xml_status") == "ok" else None)


def from_ft(path: str, src: str) -> dict | None:
    d = read_json(path)
    return (rec(src, d.get("object_id") or os.path.basename(path)[:-5], d.get("filer_ein", ""), d.get("filer_name"),
                d.get("return_type"), period_of(d.get("tax_period_end", "")), d.get("return_ts"), d.get("amended"),
                d.get("daf_ind_part_iv"), d.get("sched_d_present"), d.get("sd_daf_count"), d.get("sd_daf_eoy"),
                d.get("sd_daf_contributions"), d.get("sd_daf_grants"), d.get("total_assets_eoy"))
            if d.get("xml_status") == "ok" else None)


def from_frames(path: str) -> dict | None:
    d = read_json(path)
    # The frames extract stores 0.0 for an absent tag, so blank and zero are not separable there.
    return (rec("frames", d.get("oid") or os.path.basename(path)[:-5], d.get("filer_ein"), d.get("filer_name"),
                d.get("form"), period_of(d.get("tax_period_end", "")), "", d.get("amended_ind"), d.get("daf_ind"),
                1.0 if d.get("has_sched_d") else 0.0, d.get("daf_count"), d.get("daf_value_eoy"),
                d.get("daf_contributions"), d.get("daf_grants"), d.get("total_assets_eoy"))
            if d.get("status") == "ok" else None)


def load_dir(pattern: str, fn) -> list[dict]:
    return [r for r in map(fn, sorted(glob.glob(pattern, recursive=True))) if r]


# ----------------------------------------------------------------------------- merge
def merge(recs: Sequence[Mapping]) -> dict:
    """One OBJECT_ID read by several sources: first non-empty value by source priority; record conflicts."""
    ordered = sorted(recs, key=lambda r: PRIORITY.index(r["src"]))
    pick = lambda k: next((r[k] for r in ordered if r[k] not in (None, "")), ordered[0][k])
    l6s = {line6_of(r["line6_raw"]) for r in ordered if r["line6_raw"] != ""}
    cnts = {r["cnt"] for r in ordered if r["cnt"] is not None and r["src"] != "frames"}
    base = {k: pick(k) for k in ordered[0] if k != "src"}
    # Prefer the count of a blank-aware source: if one says blank (None) keep None rather than the frames' 0.0.
    aware = [r for r in ordered if r["src"] != "frames"]
    if aware and all(r["cnt"] is None for r in aware) and base["cnt"] == 0.0:
        base = {**base, "cnt": None}
    return {**base, "sources": "+".join(sorted({r["src"] for r in ordered}, key=PRIORITY.index)),
            "conflict_line6": len(l6s) > 1, "conflict_count": len(cnts) > 1}


def by_key(items: Iterable[Mapping], key) -> dict:
    return reduce(lambda acc, r: (acc[key(r)].append(r), acc)[1], items, defaultdict(list))


# ----------------------------------------------------------------------------- index, SOI, DAFRC
def read_index(irs_dir: str, oids: frozenset, eins: frozenset) -> tuple[dict, dict, Counter]:
    """oid -> index row; (ein, period) -> list of (oid, sub_date) for 990s; Counter of 990 (ein, period) per FY."""
    def rows():
        for y in range(2019, 2027):
            p = os.path.join(irs_dir, f"index_{y}.csv")
            if os.path.exists(p):
                with open(p, newline="", encoding="utf-8", errors="replace") as fh:
                    yield from ((y, r) for r in csv.DictReader(fh))
    by_oid, by_ep, seen = {}, defaultdict(list), set()
    for y, r in rows():
        oid, ein, pd, rt = r.get("OBJECT_ID", ""), ein9(r.get("EIN")), r.get("TAX_PERIOD", ""), r.get("RETURN_TYPE")
        if oid in oids:
            by_oid[oid] = {"ein": ein, "period": pd, "form": rt, "name": r.get("TAXPAYER_NAME", ""), "index_year": y}
        if rt == "990":
            seen.add((ein, pd))
            if ein in eins:
                by_ep[(ein, pd)].append(oid)
    per_fy = Counter(int(pd[:4]) for _, pd in seen if pd[:4].isdigit())
    return by_oid, dict(by_ep), per_fy


def read_soi(soi_dir: str, eins: frozenset | None) -> dict:
    """(ein, tax_pd) -> (dnradvisedfundscd, file); the later extract file wins. eins=None keeps every "Y" row."""
    def rows():
        for yy in range(20, 26):
            p = os.path.join(soi_dir, f"{yy}eoextract990.csv")
            if os.path.exists(p):
                with open(p, newline="", encoding="utf-8-sig", errors="replace") as fh:
                    rd = csv.reader(fh)
                    hdr = [h.lstrip("\ufeff").strip().lower() for h in next(rd)]
                    i_e, i_p, i_d = hdr.index("ein"), hdr.index("tax_pd"), hdr.index("dnradvisedfundscd")
                    yield from ((yy, r[i_e], r[i_p], r[i_d]) for r in rd if len(r) > i_d)
    keep = (lambda e, d: d.strip() == "Y") if eins is None else (lambda e, d: ein9(e) in eins)
    return {(ein9(e), p): (d.strip(), f"{yy}eoextract990") for yy, e, p, d in rows() if keep(e, d)}


def read_dafrc(path: str) -> dict:
    return {(ein9(r["ein"]), int(r["fiscal_year_end"])): r for r in read_csv(path)}


# ----------------------------------------------------------------------------- classification
def fy_of(period: str) -> int:
    return int(period[:4]) if period[:4].isdigit() else 0


def plausible(r: Mapping) -> bool:
    """Positive count with positive value and at least $1 per account (rules out dollar amounts in the count)."""
    c, v = r["cnt"] or 0, r["eoy"] or 0
    return c > 0 and v > 0 and v >= c


def case_of(r: Mapping) -> tuple[str, str]:
    l6, c, v = line6_of(r["line6_raw"]), r["cnt"], r["eoy"]
    if l6 != "Y" and (c or 0) > 0:
        return "forward", "line6_no" if l6 == "N" else "line6_blank"
    if l6 == "Y" and not (c or 0) > 0:
        if r["sd"] == 0:
            return "reverse", "no_schedule_d"
        if c is None and v is None:
            return "reverse", "part_i_daf_blank"
        if (v or 0) > 0:
            return "reverse", "count_missing_or_zero_value_positive"
        return "reverse", "count_and_value_zero_or_blank"
    return "", ""


def effective(returns: Sequence[Mapping]) -> dict:
    return max(returns, key=lambda r: r["oid"])


def prior_positive(hist: Sequence[Mapping], period: str) -> dict | None:
    pos = [h for h in hist if h["period"] < period and (h["cnt"] or 0) > 0 and (h["eoy"] or 0) > 0]
    return max(pos, key=lambda h: h["period"]) if pos else None


def out_row(r: Mapping, case: str, sub: str, soi: Mapping, dafrc: Mapping, panel: frozenset, hist: Sequence,
            n_read: int, unread_later: bool) -> dict:
    fy = fy_of(r["period"])
    s = soi.get((r["ein"], r["period"]))
    d = dafrc.get((r["ein"], fy))
    pp = prior_positive(hist, r["period"]) if case == "reverse" else None
    soi_l6 = s[0] if s else ""
    l6 = line6_of(r["line6_raw"])
    drops = ("yes" if (soi_l6 or l6) != "Y" else "no") if case == "forward" else ""
    captures = ("" if case != "forward" else
                "outside_panel" if r["ein"] not in panel else
                "panel_no_row_same_fy" if not d else
                "panel_row_" + (d.get("source_eoy_daf_assets") or "NA").lower().replace(" ", "_"))
    return {"case": case, "subcase": sub, "ein": r["ein"], "name": r["name"], "fiscal_year": fy,
            "tax_period": r["period"], "return_object_id": r["oid"], "amended": r["amended"], "return_ts": r["ts"],
            "line6_raw": r["line6_raw"], "line6": l6 or "blank", "soi_line6": soi_l6 or ("not_in_soi" if not s else ""),
            "soi_extract_file": s[1] if s else "", "sched_d_present": fmt(r["sd"]), "daf_count": fmt(r["cnt"]),
            "daf_eoy": fmt(r["eoy"]), "daf_contributions": fmt(r["contri"]), "daf_grants": fmt(r["grants"]),
            "total_assets_eoy": fmt(r["assets"]), "plausible": ("yes" if plausible(r) else "no") if case == "forward" else "",
            "in_dafrc_panel": "yes" if r["ein"] in panel else "no", "dafrc_row_same_fy": "yes" if d else "no",
            "dafrc_source_eoy_same_fy": (d or {}).get("source_eoy_daf_assets", ""),
            "dafrc_eoy_same_fy": (d or {}).get("eoy_daf_assets", ""),
            "dafrc_accounts_same_fy": (d or {}).get("number_of_daf_accounts", ""),
            "dafrc_status_same_fy": (d or {}).get("operating_status", ""),
            "line6_screen_drops": drops, "dafrc_captures_same_fy": captures,
            "prior_positive_period": pp["period"] if pp else "", "prior_positive_daf_count": fmt(pp["cnt"]) if pp else "",
            "prior_positive_daf_eoy": fmt(pp["eoy"]) if pp else "",
            "ein_line6_yes_in_any_return_read": "yes" if any(line6_of(h["line6_raw"]) == "Y" for h in hist) else "no",
            "returns_read_same_period": n_read,
            "unread_later_return_in_index": "yes" if unread_later else "no", "sources": r["sources"],
            "xml_url": XML_URL.format(oid=r["oid"])}


# ----------------------------------------------------------------------------- summaries
def tally(rows: Sequence[Mapping], key) -> dict:
    g = by_key(rows, key)
    return {str(k): {"returns": len(v), "eins": len({r["ein"] for r in v}),
                     "daf_accounts": int(sum(num(r["daf_count"]) or 0 for r in v)),
                     "daf_eoy": int(sum(num(r["daf_eoy"]) or 0 for r in v))}
            for k, v in sorted(g.items(), key=lambda kv: str(kv[0]))}


def summarise(eff: Sequence[Mapping], allret: Sequence[Mapping], rows: Sequence[Mapping], per_fy: Counter,
              conflicts: Mapping) -> dict:
    fwd = [r for r in rows if r["case"] == "forward"]
    rev = [r for r in rows if r["case"] == "reverse"]
    fwd_pl = [r for r in fwd if r["plausible"] == "yes"]
    fwd_out = [r for r in fwd_pl if r["dafrc_captures_same_fy"] != "panel_row_irs_990"]
    pos = [r for r in eff if (r["cnt"] or 0) > 0]
    yes = [r for r in eff if line6_of(r["line6_raw"]) == "Y"]
    all_fwd = [r for r in allret if case_of(r)[0] == "forward"]
    return {
        "coverage": {"form990_returns_read_fy2021plus": len(allret), "effective_returns": len(eff),
                     "eins": len({r["ein"] for r in eff}),
                     "effective_by_fy": dict(sorted(Counter(fy_of(r["period"]) for r in eff).items())),
                     "index_990_ein_periods_by_fy": {k: per_fy[k] for k in sorted(per_fy) if k >= MIN_FY},
                     "effective_by_source": dict(Counter(r["sources"] for r in eff).most_common()),
                     "conflicts": conflicts},
        "holders": {"effective_returns_count_gt0": len(pos), "eins": len({r["ein"] for r in pos}),
                    "line6_yes_effective_returns": len(yes), "line6_yes_eins": len({r["ein"] for r in yes})},
        "forward": {"all_returns_read": len(all_fwd), "effective": tally(fwd, lambda r: "all"),
                    "share_of_holder_returns": round(len(fwd) / len(pos), 4) if pos else None,
                    "by_subcase": tally(fwd, lambda r: r["subcase"]),
                    "by_fy": tally(fwd, lambda r: r["fiscal_year"]),
                    "by_plausible": tally(fwd, lambda r: r["plausible"]),
                    "plausible_by_fy": tally(fwd_pl, lambda r: r["fiscal_year"]),
                    "by_dafrc_capture": tally(fwd, lambda r: r["dafrc_captures_same_fy"]),
                    "by_soi_line6": tally(fwd, lambda r: r["soi_line6"]),
                    "by_ein_ever_yes": tally(fwd, lambda r: r["ein_line6_yes_in_any_return_read"]),
                    "plausible_by_ein_ever_yes": tally(fwd_pl, lambda r: r["ein_line6_yes_in_any_return_read"]),
                    "plausible_not_captured_by_dafrc_by_fy": tally(fwd_out, lambda r: r["fiscal_year"]),
                    "plausible_by_fy_dafrc_capture": tally(fwd_pl, lambda r: f'{r["fiscal_year"]}|{r["dafrc_captures_same_fy"]}'),
                    "unread_later_return": sum(r["unread_later_return_in_index"] == "yes" for r in fwd)},
        "reverse": {"effective": tally(rev, lambda r: "all"),
                    "share_of_line6_yes": round(len(rev) / len(yes), 4) if yes else None,
                    "by_subcase": tally(rev, lambda r: r["subcase"]),
                    "by_fy": tally(rev, lambda r: r["fiscal_year"]),
                    "by_panel": tally(rev, lambda r: r["in_dafrc_panel"]),
                    "by_subcase_panel": tally(rev, lambda r: f'{r["subcase"]}|{r["in_dafrc_panel"]}'),
                    "by_soi_line6": tally(rev, lambda r: r["soi_line6"]),
                    "top_carry_forward": [{k: r[k] for k in ("ein", "name", "fiscal_year", "subcase", "daf_count", "daf_eoy",
                                                             "prior_positive_period", "prior_positive_daf_eoy",
                                                             "in_dafrc_panel", "dafrc_source_eoy_same_fy")}
                                          for r in sorted(rev, key=lambda r: -(num(r["prior_positive_daf_eoy"]) or 0))[:12]],
                    "by_fy_panel": tally(rev, lambda r: f'{r["fiscal_year"]}|{r["in_dafrc_panel"]}'),
                    "carry_forward_prior_positive_by_fy": {
                        str(k): {"returns": len(v), "eins": len({r["ein"] for r in v}),
                                 "prior_daf_accounts": int(sum(num(r["prior_positive_daf_count"]) or 0 for r in v)),
                                 "prior_daf_eoy": int(sum(num(r["prior_positive_daf_eoy"]) or 0 for r in v))}
                        for k, v in sorted(by_key([r for r in rev if r["prior_positive_period"]],
                                                  lambda r: r["fiscal_year"]).items())},
                    "unread_later_return": sum(r["unread_later_return_in_index"] == "yes" for r in rev)},
        "forward_rows": [{k: r[k] for k in ("ein", "name", "fiscal_year", "line6_raw", "soi_line6", "daf_count",
                                            "daf_eoy", "plausible", "dafrc_captures_same_fy", "amended",
                                            "return_object_id")}
                         for r in sorted(fwd, key=lambda r: -(num(r["daf_eoy"]) or 0))],
    }


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root")
    for a in ("--irs-dir", "--soi-dir", "--frames-cache", "--ft-cache", "--l6-cache", "--extract-cache"):
        ap.add_argument(a, required=True)
    ap.add_argument("--summary", default="")
    a = ap.parse_args(argv)
    P = lambda p: os.path.join(a.root, p)

    raw = (sum((from_harvest(read_csv(P(h))) for h in HARVESTS), [])
           + from_nondafrc(read_csv(P(NONDAFRC)))
           + load_dir(os.path.join(a.extract_cache, "*.json"), from_extract)
           + load_dir(os.path.join(a.l6_cache, "*.json"), lambda p: from_ft(p, "l6"))
           + load_dir(os.path.join(a.ft_cache, "**", "*.json"), lambda p: from_ft(p, "ft"))
           + load_dir(os.path.join(a.frames_cache, "full", "*.json"), from_frames))
    merged0 = [merge(v) for v in by_key(raw, lambda r: r["oid"]).values()]
    eins0 = frozenset(r["ein"] for r in merged0 if r["ein"])
    idx, by_ep, per_fy = read_index(a.irs_dir, frozenset(r["oid"] for r in merged0), eins0)
    fill = lambda r: {**r, "ein": r["ein"] or idx.get(r["oid"], {}).get("ein", ""),
                      "period": r["period"] or idx.get(r["oid"], {}).get("period", ""),
                      "form": r["form"] or idx.get(r["oid"], {}).get("form", ""),
                      # ft/l6 extracts took the first BusinessNameLine1Txt, which can be the paid preparer's firm
                      "name": idx.get(r["oid"], {}).get("name", "") or r["name"]}
    merged = [fill(r) for r in merged0]
    allret = [r for r in merged if r["form"] == "990" and r["ein"] and fy_of(r["period"]) >= MIN_FY]
    # One EIN reaching the index pass late (EIN known only from the index) still needs its (ein, period) list.
    missing = frozenset(r["ein"] for r in allret) - eins0
    if missing:
        _, extra, _ = read_index(a.irs_dir, frozenset(), missing)
        by_ep = {**by_ep, **extra}
    groups = by_key(allret, lambda r: (r["ein"], r["period"]))
    eff = [effective(v) for v in groups.values()]
    hist = by_key(eff, lambda r: r["ein"])
    flagged = [(r, *case_of(r)) for r in eff]
    flagged = [(r, c, s) for r, c, s in flagged if c]
    soi = read_soi(a.soi_dir, frozenset(r["ein"] for r, _, _ in flagged))
    dafrc = read_dafrc(P(DAFRC))
    panel = frozenset(e for e, _ in dafrc)
    later = lambda r: any(o > r["oid"] and o not in {x["oid"] for x in groups[(r["ein"], r["period"])]}
                          for o in by_ep.get((r["ein"], r["period"]), ()))
    rows = [out_row(r, c, s, soi, dafrc, panel, hist[r["ein"]], len(groups[(r["ein"], r["period"])]), later(r))
            for r, c, s in flagged]
    rows = sorted(rows, key=lambda r: (r["case"], r["ein"], r["tax_period"]))
    os.makedirs(os.path.dirname(P(OUT)), exist_ok=True)
    with open(P(OUT), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    conflicts = {"line6": sum(r["conflict_line6"] for r in allret), "count": sum(r["conflict_count"] for r in allret)}
    summ = summarise(eff, allret, rows, per_fy, conflicts)
    soi_yes = [k for k in read_soi(a.soi_dir, None) if fy_of(k[1]) >= MIN_FY]
    eff_keys = frozenset((r["ein"], r["period"]) for r in eff)
    summ["coverage"]["soi_line6_yes_ein_periods_fy2021plus"] = {
        str(fy): {"soi_yes": len(v), "read_here": sum(k in eff_keys for k in v)}
        for fy, v in sorted(by_key(soi_yes, lambda k: fy_of(k[1])).items())}
    txt = json.dumps(summ, indent=1, default=str)
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            fh.write(txt)
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
