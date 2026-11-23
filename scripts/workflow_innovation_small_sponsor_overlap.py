#!/usr/bin/env python3
"""Small-sponsor recipient overlap (OUTSTANDING B2): do the ~1,450 DAF sponsors outside the top 50 gain more from a
shared verification record than the top 50 do?

Universe   every sponsor in data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv (all FY2024 DAFRC
           sponsors with a filed 990, 1,512 EINs) that is NOT a sponsor in the top-50 edge file
           (data/workflow-innovation/sponsor-recipient-edges-fy2023.csv). The two top-50 lists agree on 49 of 50 EINs;
           the boundary sponsor is treated as "small" here so no sponsor is counted twice.
Return     FY2023 return from that harvest; FY2024 when FY2023 is missing, unfetchable or has no itemised
           Schedule I Part II lines (same rule as the top-50 script).
Lines      Schedule I Part II RecipientTable lines from the public e-file XML (GivingTuesday mirror of IRS TEOS);
           exclusions and keys are exactly those of scripts/workflow_innovation_recipient_overlap.py (imported).
Questions  1. coverage_by_top50: share of a small sponsor's distinct recipients already on a top-50 Schedule I --
              what a small sponsor would reuse by joining a network the top 50 already seeded.
           2. coverage_by_any_other: share already on any other sponsor's Schedule I (top 50 or small).
           3. coverage_small_only: share on another SMALL sponsor's Schedule I (a network without the top 50).
           4. join curves: top 50 by rank first, then small sponsors by rank; and small sponsors only, by rank.
           5. costly subsets: EIN-keyed recipients absent from the current IRS EO BMF extract (--bmf-dir; a later
              snapshot than the FY2023 returns, so some absences are later revocations or terminations) and the
              433-EIN fiscal-sponsor list.
           All are reported per sponsor, per size band (FY2024 asset rank) and pooled.

Caveat     Only sponsors that ITEMISE Schedule I appear. Small sponsors that report grants under $5,000 per recipient
           or no grants are absent, and those are the smallest. Results describe itemising small sponsors.

Stdlib only; functional style (pure transforms; I/O at the edges).

Usage:
  python3 scripts/workflow_innovation_small_sponsor_overlap.py --xml-dir DIR --bmf-dir DIR [--fetch] [--workers 4]
"""
from __future__ import annotations

import argparse
import csv
import gzip
import os
import sys
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import workflow_innovation_recipient_overlap as top  # noqa: E402
from mission_990_contractors import XML_URL, ein9  # noqa: E402

ROOT = top.ROOT
HARVEST = os.path.join(ROOT, "data", "mission-2026-11-14", "form990-returns-schedule-d-harvest-full.csv")
FISCAL = os.path.join(ROOT, "data", "mission-2026-11-14", "fiscal-sponsor-ein-list-2026-11-19.csv")
OUT_DIR = top.OUT_DIR
EDGES = os.path.join(OUT_DIR, "sponsor-recipient-edges-small-fy2023.csv")
SUMMARY = os.path.join(OUT_DIR, "small-sponsor-overlap-summary.csv")
BANDS = (("rank 51-200", 51, 200), ("rank 201-500", 201, 500), ("rank 501+", 501, 10 ** 9))
FIELDS = ("section", "scope", "order", "k", "sponsor_ein", "sponsor_rank", "sponsor_name", "fiscal_year", "bucket",
          "metric", "value", "definition")


# ----------------------------------------------------------------------------- inputs (pure over rows)
def small_universe(rows: Iterable[Mapping], top50: frozenset) -> dict[str, dict]:
    """EIN -> {ein, rank, name, by_fy} for harvest sponsors outside the top-50 edge set."""
    out: dict[str, dict] = {}
    for r in rows:
        e = ein9(r["ein"])
        if e in top50 or not r["fy2024_asset_rank"]:
            continue
        s = out.setdefault(e, {"ein": e, "rank": int(r["fy2024_asset_rank"]), "name": r["sponsor_name"], "by_fy": {}})
        if r["return_object_id"] and r["xml_status"] == "ok":
            s["by_fy"][r["fiscal_year"]] = {"object_id": r["return_object_id"], "tax_period": r["tax_period"],
                                            "xml_url": r["xml_url"] or XML_URL.format(oid=r["return_object_id"])}
    return out


def band_of(rank: int) -> str:
    return next(b for b, lo, hi in BANDS if lo <= rank <= hi)


def key_set(path: str, col: str) -> frozenset:
    return frozenset("E:" + ein9(r[col]) for r in top.read_csv(path) if r.get(col, "").strip())


def bmf_eins(bmf_dir: str) -> frozenset:
    """EINs in the IRS EO Business Master File extract files (eo*.csv) in bmf_dir."""
    files = sorted(f for f in os.listdir(bmf_dir) if f.startswith("eo") and f.endswith(".csv"))
    return frozenset("E:" + ein9(r["EIN"]) for f in files for r in top.read_csv(os.path.join(bmf_dir, f)))


def absent_from_bmf(bys: Mapping, bmf: frozenset) -> frozenset:
    """EIN-keyed recipients not in the BMF (identity or status needs a person). Name-only keys are excluded."""
    return frozenset(k for m in bys.values() for k in m if k.startswith("E:") and k not in bmf)


# ----------------------------------------------------------------------------- metrics (pure)
def coverage(m: Mapping, ref: frozenset) -> dict:
    """Shares of a sponsor's recipients / lines / dollars whose key is in ref."""
    L = sum(l for l, _ in m.values()) or 1
    A = sum(a for _, a in m.values()) or 1
    hit = [k for k in m if k in ref]
    return {"recipient_share": len(hit) / (len(m) or 1), "line_share": sum(m[k][0] for k in hit) / L,
            "dollar_share": sum(m[k][1] for k in hit) / A}


def others_index(bys: Mapping[str, Mapping]) -> dict[str, frozenset]:
    """recipient key -> sponsors funding it."""
    idx: dict[str, set] = defaultdict(set)
    for s, m in bys.items():
        for k in m:
            idx[k].add(s)
    return {k: frozenset(v) for k, v in idx.items()}


def covered_by_others(s: str, m: Mapping, idx: Mapping, pool: frozenset) -> frozenset:
    """Keys of sponsor s also funded by some OTHER sponsor in pool."""
    return frozenset(k for k in m if any(o != s and o in pool for o in idx[k]))


def pooled(rows: Sequence[Mapping], metric: str) -> float:
    """Recipient-weighted pooled share across sponsors."""
    n = sum(r["distinct_recipients"] for r in rows) or 1
    return sum(r[metric] * r["distinct_recipients"] for r in rows) / n


def row(section, metric, value, **kw) -> dict:
    v = round(value, 6) if isinstance(value, float) else value
    return {**{f: "" for f in FIELDS}, "section": section, "metric": metric, "value": v,
            "definition": kw.pop("definition", ""), **kw}


DEFS = {
    "cov_top50": "share of the sponsor's distinct recipients already on >=1 top-50 sponsor's FY2023/24 Schedule I",
    "cov_any": "share already on >=1 other sponsor's Schedule I (top 50 or small)",
    "cov_small": "share already on >=1 other SMALL sponsor's Schedule I (network without the top 50)",
    "cov_top50_lines": "as cov_top50, weighted by Schedule I lines",
    "cov_top50_dollars": "as cov_top50, weighted by dollars",
}


def sponsor_metrics(small: Mapping, sbys: Mapping, tbys: Mapping) -> list[dict]:
    allb = {**tbys, **sbys}
    idx = others_index(allb)
    top_keys = frozenset(k for m in tbys.values() for k in m)
    small_pool, all_pool = frozenset(sbys), frozenset(allb)
    out = []
    for s, m in sbys.items():
        n = len(m) or 1
        ct = coverage(m, top_keys)
        out.append({"ein": s, "rank": small[s]["rank"], "name": small[s]["name"], "band": band_of(small[s]["rank"]),
                    "distinct_recipients": len(m), "lines": sum(l for l, _ in m.values()),
                    "amount_usd": sum(a for _, a in m.values()),
                    "cov_top50": ct["recipient_share"], "cov_top50_lines": ct["line_share"],
                    "cov_top50_dollars": ct["dollar_share"],
                    "cov_any": len(covered_by_others(s, m, idx, all_pool)) / n,
                    "cov_small": len(covered_by_others(s, m, idx, small_pool)) / n})
    return sorted(out, key=lambda r: r["rank"])


def top50_reference(tbys: Mapping) -> dict:
    """Same 'covered by any other top-50 sponsor' metric for the top 50, for comparison."""
    idx = others_index(tbys)
    pool = frozenset(tbys)
    rows = [{"distinct_recipients": len(m), "cov": len(covered_by_others(s, m, idx, pool)) / (len(m) or 1)}
            for s, m in tbys.items()]
    return {"sponsors": len(rows), "pooled": pooled(rows, "cov"),
            "median": sorted(r["cov"] for r in rows)[len(rows) // 2] if rows else 0.0}


def costly_rows(sbys: Mapping, tbys: Mapping, cls: str, keys: frozenset) -> list[dict]:
    """For a costly-recipient class: small-sponsor recipients in it, and the share already on a top-50 record."""
    top_keys = frozenset(k for m in tbys.values() for k in m)
    pairs = [(s, k) for s, m in sbys.items() for k in m if k in keys]
    distinct = frozenset(k for _, k in pairs)
    hit = sum(1 for _, k in pairs if k in top_keys)
    return [row("costly", "small_sponsor_pairs", len(pairs), scope=cls,
                definition="small sponsor x recipient pairs in this costly class"),
            row("costly", "distinct_recipients", len(distinct), scope=cls),
            row("costly", "share_pairs_on_top50_record", hit / (len(pairs) or 1), scope=cls,
                definition="share of those pairs whose recipient is already on a top-50 Schedule I")]


def summary(small: Mapping, chosen: Mapping, sbys: Mapping, tbys: Mapping, costly: Mapping) -> list[dict]:
    per = sponsor_metrics(small, sbys, tbys)
    ref = top50_reference(tbys)
    rows = [row("coverage", "small_sponsors_in_universe", len(small)),
            row("coverage", "small_sponsors_with_itemised_schedule_i", len(sbys)),
            row("coverage", "small_sponsors_fy2023", sum(1 for c in chosen.values() if c["fy"] == "2023")),
            row("coverage", "small_sponsors_fy2024_fallback", sum(1 for c in chosen.values() if c["fy"] == "2024")),
            row("coverage", "small_distinct_recipients", len(frozenset(k for m in sbys.values() for k in m))),
            row("coverage", "small_edges", sum(len(m) for m in sbys.values())),
            row("reference", "top50_pooled_cov_by_other_top50", ref["pooled"], scope="top 50",
                definition="top-50 sponsors: recipient-weighted share of recipients also on another top-50 Schedule I"),
            row("reference", "top50_median_cov_by_other_top50", ref["median"], scope="top 50")]
    groups = [("all small", per)] + [(b, [r for r in per if r["band"] == b]) for b, _, _ in BANDS]
    for name, rs in groups:
        rows.append(row("band", "sponsors", len(rs), scope=name))
        rows.append(row("band", "distinct_recipients_sum", sum(r["distinct_recipients"] for r in rs), scope=name))
        rows.append(row("band", "median_distinct_recipients",
                        sorted(r["distinct_recipients"] for r in rs)[len(rs) // 2] if rs else 0, scope=name))
        for m in ("cov_top50", "cov_any", "cov_small", "cov_top50_lines", "cov_top50_dollars"):
            rows.append(row("band", f"pooled_{m}", pooled(rs, m), scope=name, definition=DEFS[m]))
            rows.append(row("band", f"median_{m}", sorted(r[m] for r in rs)[len(rs) // 2] if rs else 0.0,
                            scope=name, definition=DEFS[m]))
    for r in per:
        for m in ("distinct_recipients", "lines", "amount_usd", "cov_top50", "cov_any", "cov_small"):
            rows.append(row("sponsor", m, float(r[m]) if m.startswith("cov") else r[m], sponsor_ein=r["ein"],
                            sponsor_rank=r["rank"], sponsor_name=r["name"], bucket=r["band"],
                            fiscal_year=chosen[r["ein"]]["fy"], definition=DEFS.get(m, "")))
    allb = {**tbys, **sbys}
    rank_of = {**{s: 0 for s in tbys}, **{s: small[s]["rank"] for s in sbys}}
    orders = {"top50_then_small_by_rank": TOP_ORDER(tbys) + sorted(sbys, key=lambda s: small[s]["rank"]),
              "small_only_by_rank": sorted(sbys, key=lambda s: small[s]["rank"])}
    for o, seq in orders.items():
        for c in top.reuse_curve(seq, allb):
            for m in ("recipient_share", "line_share", "dollar_share", "cum_verifications_avoided"):
                rows.append(row("reuse_curve", m, c[m], order=o, k=c["k"], sponsor_ein=c["sponsor_ein"],
                                sponsor_rank=rank_of[c["sponsor_ein"]],
                                definition=top.METRIC_DEFS["reuse_curve"]))
    for cls, keys in costly.items():
        rows.extend(costly_rows(sbys, tbys, cls, keys))
    return rows


TOP_RANKS: dict[str, int] = {}


def TOP_ORDER(tbys: Mapping) -> list[str]:  # noqa: N802
    return sorted(tbys, key=lambda s: TOP_RANKS.get(s, 10 ** 6))


# ----------------------------------------------------------------------------- I/O
def read_top50_edges() -> tuple[dict, dict]:
    path = top.EDGES if os.path.exists(top.EDGES) else top.EDGES + ".gz"
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt", encoding="utf-8", newline="") as fh:
        edges = [{**e, "lines": int(e["lines"]), "amount_usd": float(e["amount_usd"])} for e in csv.DictReader(fh)]
    ranks = {e["sponsor_ein"]: int(e["sponsor_rank"]) for e in edges}
    return top.by_sponsor(edges), ranks


def write_csv(path: str, fields: Sequence[str], rows: Iterable[Mapping]) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    if os.path.getsize(path) <= top.MAX_EDGES_BYTES:
        return path
    with open(path, "rb") as src, gzip.open(path + ".gz", "wb", compresslevel=9) as dst:
        dst.write(src.read())
    os.remove(path)
    return path + ".gz"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--bmf-dir", required=True, help="directory with IRS EO BMF extracts eo1.csv..eo4.csv")
    a = ap.parse_args(argv)
    os.makedirs(a.xml_dir, exist_ok=True)
    tbys, ranks = read_top50_edges()
    TOP_RANKS.update(ranks)
    small = small_universe(top.read_csv(HARVEST), frozenset(tbys))
    wl_eins, wl_names = top.whitelist_from(top.read_csv(top.WHITELIST))
    chosen, log = top.choose_and_parse(small, a.xml_dir, a.fetch, a.workers)
    built = {s: top.edges_for(small[s], c["fy"], c["parsed"], wl_eins, wl_names) for s, c in chosen.items()}
    edges = tuple(e for s in sorted(built, key=lambda s: small[s]["rank"]) for e in built[s][0])
    sbys = {s: m for s, m in top.by_sponsor(edges).items()}
    bmf = bmf_eins(a.bmf_dir)
    costly = {"EIN absent from current IRS EO BMF": absent_from_bmf({**tbys, **sbys}, bmf),
              "fiscal sponsors (433-EIN list)": key_set(FISCAL, "ein")}
    path = write_csv(EDGES, ("sponsor_ein", "sponsor_rank", "fiscal_year", "recipient_key", "key_type", "lines",
                             "amount_usd"), edges)
    rows = summary(small, {s: chosen[s] for s in sbys}, sbys, tbys, costly)
    status = Counter(at["status"].split(":")[0] for s in log for at in log[s])
    rows.extend(row("attempt", "return_status_count", n, scope=st) for st, n in sorted(status.items()))
    write_csv(SUMMARY, FIELDS, rows)
    print(f"small sponsors {len(small)}; parsed {len(chosen)}; with kept lines {len(sbys)}; edges {len(edges)} -> {path}")
    print("attempt statuses:", dict(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
