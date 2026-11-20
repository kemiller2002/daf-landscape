#!/usr/bin/env python3
"""Size distribution of DAF grants: Schedule I line sizes, top-50 sponsors FY2021-FY2024, plus published
grant-size statistics and average grant = DAF grants / stated grant count (queue item b51-03).

IMPORTANT: a Schedule I Part II line is a RECIPIENT-YEAR TOTAL (all grants from the filer to one recipient in the
tax year, summed), itemised only when that total exceeds $5,000. It is NOT a single grant. Line-size bins are
therefore bins of recipient-year totals; they overstate grant size and omit every recipient that received $5,000 or
less in the year.

Universe and return choice: those of scripts/mission_daf_to_daf.py / mission_recipient_sectors.py (top-50 DAFRC
sponsors by FY2024 DAF assets; one return per sponsor x DAFRC fiscal year via mission_daf_to_daf.pick_returns over
the netpayout990/ cache), extended here from FY2023-24 to FY2021-24. Returns whose Schedule I points to an
attachment instead of itemising (mission_net_payout.itemized == False: BofA CGF, RCF, ...) are excluded and listed.

Steps (pure transforms; I/O at the edges)
  1. Lines     every Schedule I Part II RecipientTable line ([ein, name, where, irc, cash, noncash]) from the line
               caches written by mission_recipient_sectors.py (read-only), else a local XML copy whose line count
               matches netpayout990's sched_i_lines, else (with --fetch) the GivingTuesday mirror of IRS TEOS. E-filed
               totals rows are dropped (mission_exception_load.drop_totals_rows).
  2. Bins      amount = cash + non-cash; bins <$10k, $10k-<$100k, $100k-<$1m, $1m-<$10m, >=$10m. Lines <= 0 are
               counted separately and left out of the bins. Basis `all_lines` and `excl_d2d` (lines to DAF sponsors
               in daf-to-daf-recipient-whitelist.csv `include`, and self-lines, removed).
  3. Scopes    all top-50 itemising sponsors; by DAFRC segment (national / processor / community_foundation /
               single_issue / university_hospital); FY2021..FY2024 and pooled; a fixed panel (sponsors itemising in
               all four years) for the trend.
  4. Sponsor   per sponsor-year: line count, dollars, mean and median line, share of dollars in >= $1m / >= $10m.
  5. Combine   for the 12 sponsors with a primary stated grant count (grant-count-denominators-2026-11-20.csv,
               is_primary == 1): avg grant = DAFRC FY2024 total DAF grants / count, and (where the count source
               states a dollar total) stated dollars / count; compared with the Schedule I mean/median line and
               with the published statistics in PUBLISHED.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_grant_size_distribution.py . --np-cache NPCACHE --lines-cache MYCACHE \
      [--read-cache DIR ...] [--xml-list FILE] [--fetch]
"""
from __future__ import annotations

import argparse
import os
import statistics
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import WHITELIST, load_lines  # noqa: E402

FYS = (2021, 2022, 2023, 2024)
OUT_REL = os.path.join("data", "mission-2026-11-14", "grant-size-distribution-2026-11-20.csv")
COUNTS_REL = os.path.join("data", "mission-2026-11-14", "grant-count-denominators-2026-11-20.csv")
GT = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
BINS = (("lt_10k", 0.0, 1e4), ("10k_100k", 1e4, 1e5), ("100k_1m", 1e5, 1e6), ("1m_10m", 1e6, 1e7),
        ("ge_10m", 1e7, float("inf")))
SEGMENTS = ("national", "processor", "community_foundation", "single_issue", "university_hospital")

# Dollar totals stated in the same source as the primary grant count (grant-count-denominators-2026-11-20.csv,
# `quote` / `notes` / URL slug of the row named). Only values that appear there are used.
STATED_USD = {
    "GC-001": (14.9e9, "$14.9B (CY2024; quote)"),
    "GC-005": (3.0e9, "over $3 billion (FY2024; quote; lower bound)"),
    "GC-007": (3_072_946_000.0, "approximately $3,072,946,000 (CY2024; quote)"),
    "GC-008": (1.54e9, "$1.54 billion, all SVCF grants, preliminary (CY2024; quote)"),
    "GC-009": (1.3e9, "$1.3B+ (CY2024; notes; lower bound)"),
    "GC-010": (1_302_541_225.0, "$1,302,541,225 sum of 51 state rows (CY2024; notes)"),
    "GC-015": (400e6, "close to $400 million (CY2024; quote)"),
    "GC-016": (1.0e9, "record-breaking $1 billion (FY2024; release URL slug)"),
    "GC-017": (911_535_342.0, "$911,535,342 granted by FFTC fundholders (CY2024; notes)"),
    "GC-004": (6.6e9, "more than $6.6B (FY2024; article URL slug; lower bound)"),
}

# Published grant-size statistics, quoted verbatim (filled from the sponsor reports; see the research doc §2).
# (stat_id, sponsor, ein, period, metric, value_usd_or_share, unit, quote, url, robots)
PUBLISHED: tuple = ()


# ----------------------------------------------------------------------------- pure helpers
def amount(l: Sequence) -> float:
    return float(l[4] or 0.0) + float(l[5] or 0.0)


def bin_of(a: float) -> str:
    return next(b for b, lo, hi in BINS if lo <= a < hi)


def median(xs: Sequence[float]) -> float | None:
    return statistics.median(xs) if xs else None


def r6(x):
    return None if x is None else round(x, 6)


def r2(x):
    return None if x is None else round(x, 2)


def annotate(key: tuple, lines: Sequence[Sequence], wl_eins: frozenset, wl_names: Mapping) -> tuple[dict, ...]:
    grantor = key[0]

    def one(l):
        e = l[0] if (l[0] or "").strip("0") else ""
        d2d = (e == grantor) or (e in wl_eins) or (not e and wl_names.get(norm_name(l[1] or ""), "") != "")
        return {"sy": key, "ein": grantor, "fy": key[1], "amount": amount(l), "d2d": d2d}
    return tuple(one(l) for l in lines)


def dist(rows: Sequence[Mapping]) -> dict:
    pos = tuple(r["amount"] for r in rows if r["amount"] > 0)
    tot_n, tot_usd = len(pos), sum(pos)
    by = _group_by_fast(pos, bin_of)
    bins = {b: (len(by.get(b, ())), sum(by.get(b, ()))) for b, _, _ in BINS}
    ge = lambda t: (sum(1 for a in pos if a >= t), sum(a for a in pos if a >= t))  # noqa: E731
    return {"n": tot_n, "usd": tot_usd, "nonpos": len(rows) - tot_n, "bins": bins,
            "le_5k": sum(1 for a in pos if a <= 5000), "ge_1m": ge(1e6), "ge_10m": ge(1e7),
            "mean": tot_usd / tot_n if tot_n else None, "median": median(sorted(pos))}


def dist_rows(scope: str, scope_type: str, segment: str, fy: str, basis: str, rows: Sequence[Mapping],
              n_sy: int) -> list[dict]:
    d = dist(rows)
    base = {"row_type": "line_size_bin", "scope": scope, "scope_type": scope_type, "segment": segment, "fy": fy,
            "basis": basis, "sponsor_years": n_sy, "unit": "Schedule I recipient-year line"}
    bin_rows = [{**base, "bin": b, "lines": n, "line_share": r6(n / d["n"]) if d["n"] else None, "usd": r2(u),
                 "usd_share": r6(u / d["usd"]) if d["usd"] else None} for b, (n, u) in d["bins"].items()]
    summ = {**base, "row_type": "line_size_summary", "bin": "all", "lines": d["n"], "usd": r2(d["usd"]),
            "mean_line_usd": r2(d["mean"]), "median_line_usd": r2(d["median"]),
            "lines_le_5k": d["le_5k"], "lines_nonpositive": d["nonpos"],
            "lines_ge_1m": d["ge_1m"][0], "usd_share_ge_1m": r6(d["ge_1m"][1] / d["usd"]) if d["usd"] else None,
            "line_share_ge_1m": r6(d["ge_1m"][0] / d["n"]) if d["n"] else None,
            "lines_ge_10m": d["ge_10m"][0], "usd_share_ge_10m": r6(d["ge_10m"][1] / d["usd"]) if d["usd"] else None,
            "line_share_ge_10m": r6(d["ge_10m"][0] / d["n"]) if d["n"] else None,
            "line_share_lt_100k": r6((d["bins"]["lt_10k"][0] + d["bins"]["10k_100k"][0]) / d["n"]) if d["n"] else None,
            "usd_share_lt_100k": r6((d["bins"]["lt_10k"][1] + d["bins"]["10k_100k"][1]) / d["usd"]) if d["usd"] else None}
    return bin_rows + [summ]


def scope_rows(ann: Mapping, seg_of: Mapping, fixed: frozenset) -> list[dict]:
    keys = tuple(sorted(ann))
    pick = lambda pred: tuple(r for k in keys if pred(k) for r in ann[k])  # noqa: E731
    nsy = lambda pred: sum(1 for k in keys if pred(k))  # noqa: E731
    fys = tuple((str(f), (lambda f: lambda k: k[1] == f)(f)) for f in FYS) + (("2021-2024", lambda k: True),)
    scopes = (("all_top50", "all", "", lambda k: True), ("fixed_panel", "fixed_panel", "", lambda k: k[0] in fixed)) + \
        tuple((f"segment:{s}", "segment", s, (lambda s: lambda k: seg_of[k[0]] == s)(s)) for s in SEGMENTS)
    bases = (("all_lines", lambda r: True), ("excl_d2d", lambda r: not r["d2d"]))
    return [row for sc, st, seg, sp in scopes for fy, fp in fys for b, bp in bases
            for row in dist_rows(sc, st, seg, fy, b, tuple(r for r in pick(lambda k: sp(k) and fp(k)) if bp(r)),
                                 nsy(lambda k: sp(k) and fp(k)))
            if nsy(lambda k: sp(k) and fp(k))]


def sponsor_rows(ann: Mapping, panel: Mapping, rank: Mapping, oid_of: Mapping) -> list[dict]:
    def one(k):
        d = dist(ann[k])
        return {"row_type": "sponsor_year", "scope": f"sponsor:{k[0]}", "scope_type": "sponsor",
                "segment": panel[k[0]]["segment"], "sponsor": panel[k[0]]["name"], "ein": k[0], "rank_fy2024": rank[k[0]],
                "fy": str(k[1]), "basis": "all_lines", "bin": "all", "unit": "Schedule I recipient-year line",
                "lines": d["n"], "usd": r2(d["usd"]), "mean_line_usd": r2(d["mean"]), "median_line_usd": r2(d["median"]),
                "lines_le_5k": d["le_5k"], "lines_ge_1m": d["ge_1m"][0], "lines_ge_10m": d["ge_10m"][0],
                "usd_share_ge_1m": r6(d["ge_1m"][1] / d["usd"]) if d["usd"] else None,
                "usd_share_ge_10m": r6(d["ge_10m"][1] / d["usd"]) if d["usd"] else None,
                "line_share_lt_100k": r6((d["bins"]["lt_10k"][0] + d["bins"]["10k_100k"][0]) / d["n"]) if d["n"] else None,
                "usd_share_lt_100k": r6((d["bins"]["lt_10k"][1] + d["bins"]["10k_100k"][1]) / d["usd"]) if d["usd"] else None,
                "source_url": GT.format(oid_of[k])}
    return [one(k) for k in sorted(ann, key=lambda k: (rank[k[0]], k[1]))]


def excluded_rows(excl: Sequence[tuple], panel: Mapping, rank: Mapping) -> list[dict]:
    return [{"row_type": "excluded_return", "scope": f"sponsor:{e}", "scope_type": "sponsor", "ein": e,
             "segment": panel[e]["segment"], "sponsor": panel[e]["name"], "rank_fy2024": rank[e], "fy": str(fy),
             "note": why, "source_url": GT.format(oid) if oid else ""} for e, fy, oid, why in excl]


def combine_rows(counts: Sequence[Mapping], dafrc: Sequence[Mapping], sp_rows: Sequence[Mapping]) -> list[dict]:
    grants24 = {ein9(r["ein"]): r for r in dafrc if r["fiscal_year_end"] == "2024"}
    sp24 = {r["ein"]: r for r in sp_rows if r["fy"] == "2024"}

    def one(c):
        e = ein9(c["ein"])
        g = float(c["grant_count"])
        d = grants24.get(e, {})
        dg = float(d["total_daf_grants"]) if d.get("total_daf_grants") else None
        st = STATED_USD.get(c["row_id"])
        s = sp24.get(e, {})
        return {"row_type": "avg_grant_from_count", "scope": f"sponsor:{e}", "scope_type": "sponsor", "ein": e,
                "sponsor": c["entity"], "fy": c["period_label"], "basis": "stated_count", "unit": "grant",
                "count_row_id": c["row_id"], "grant_count": int(g), "count_qualifier": c["count_qualifier"],
                "period_match": c["period_match"],
                "dafrc_fy2024_daf_grants_usd": r2(dg), "avg_grant_dafrc_usd": r2(dg / g) if dg else None,
                "stated_usd": r2(st[0]) if st else None, "stated_usd_note": st[1] if st else "",
                "avg_grant_stated_usd": r2(st[0] / g) if st else None,
                "lines": s.get("lines"), "mean_line_usd": s.get("mean_line_usd"), "median_line_usd": s.get("median_line_usd"),
                "grants_per_line": r2(g / s["lines"]) if s.get("lines") else None,
                "source_url": c["url"], "note": c["scope_note"]}
    return [one(c) for c in counts if c["is_primary"] == "1" and c["grant_count"]]


def published_rows() -> list[dict]:
    return [{"row_type": "published_stat", "scope": f"sponsor:{ein}" if ein else "industry", "scope_type": "published",
             "sponsor": sp, "ein": ein, "fy": per, "basis": metric, "unit": unit, "stat_id": sid, "value": val,
             "quote": q, "source_url": url, "note": rob} for sid, sp, ein, per, metric, val, unit, q, url, rob in PUBLISHED]


FIELDS = ("row_type", "scope", "scope_type", "segment", "sponsor", "ein", "rank_fy2024", "fy", "basis", "bin", "unit",
          "sponsor_years", "lines", "line_share", "usd", "usd_share", "mean_line_usd", "median_line_usd",
          "lines_le_5k", "lines_nonpositive", "lines_ge_1m", "line_share_ge_1m", "usd_share_ge_1m", "lines_ge_10m",
          "line_share_ge_10m", "usd_share_ge_10m", "line_share_lt_100k", "usd_share_lt_100k",
          "count_row_id", "grant_count", "count_qualifier", "period_match", "dafrc_fy2024_daf_grants_usd",
          "avg_grant_dafrc_usd", "stated_usd", "stated_usd_note", "avg_grant_stated_usd", "grants_per_line",
          "stat_id", "value", "quote", "source_url", "note")


# ----------------------------------------------------------------------------- I/O edge
def get_lines(oid: str, expect: int, read_caches: Sequence[str], cache: str, xml_paths: Mapping, fetch: bool) -> dict:
    hit = next((c for c in read_caches if os.path.exists(os.path.join(c, f"{oid}.json"))), None)
    if hit:
        return load_lines(oid, expect, hit, [], False)
    dirs = tuple(sorted({os.path.dirname(p) for p in xml_paths.get(oid, ())}))
    return load_lines(oid, expect, cache, dirs, fetch)


def xml_index(path: str) -> dict:
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        ps = tuple(p.strip() for p in fh if p.strip())
    key = lambda p: os.path.basename(p).replace("_public.xml", "").replace(".xml", "")  # noqa: E731
    return {k: tuple(v) for k, v in _group_by_fast(ps, key).items()}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--read-cache", action="append", default=[])
    ap.add_argument("--xml-list", default="")
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    dafrc = read_csv(DAFRC_CSV)
    rank, panel = top_n(dafrc, TOP_N), panel_from(dafrc)
    chosen = pick_returns(load_np(a.np_cache))
    inscope = {k: x for k, x in chosen.items() if k[0] in rank and k[1] in FYS}
    item = {k: x for k, x in inscope.items() if itemized(x)}
    xp = xml_index(a.xml_list)
    loaded = {k: get_lines(x["oid"], x.get("sched_i_lines") or 0, a.read_cache, a.lines_cache, xp, a.fetch)
              for k, x in sorted(item.items())}
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    missing = tuple((e, fy) for e in rank for fy in FYS if (e, fy) not in inscope)
    excl = tuple((k[0], k[1], x["oid"], "schedule_i_not_itemised (attachment)") for k, x in inscope.items() if k not in item) + \
        tuple((k[0], k[1], item[k]["oid"], f"lines_{v['status']}") for k, v in loaded.items() if v["status"] != "ok") + \
        tuple((e, fy, "", "no_return_in_netpayout990_cache") for e, fy in missing)
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    ann = {k: annotate(k, v["lines"], wl_eins, wl_names) for k, v in good.items()}
    seg_of = {e: panel[e]["segment"] for e in rank}
    fixed = frozenset(e for e in rank if all((e, f) in ann for f in FYS))
    oid_of = {k: item[k]["oid"] for k in ann}
    sp = sponsor_rows(ann, panel, rank, oid_of)
    counts = read_csv(os.path.join(a.root, COUNTS_REL))
    rows = scope_rows(ann, seg_of, fixed) + sp + combine_rows(counts, dafrc, sp) + published_rows() + \
        excluded_rows(sorted(excl), panel, rank)
    out = os.path.join(a.root, OUT_REL)
    write_csv(out, rows, FIELDS)
    print(f"sponsor-years in scope {len(inscope)}; itemised {len(item)}; parsed {len(good)}; fixed panel {len(fixed)} "
          f"sponsors; lines {sum(len(v) for v in ann.values())}; rows {len(rows)} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
