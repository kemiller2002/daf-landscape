#!/usr/bin/env python3
"""DAF-to-DAF (sponsor-to-sponsor) flows among the top-50 DAF sponsors, FY2023-FY2024 (queue items P-B29C-02, P-99F-06).

Pure transform of the Schedule I extracts cached by scripts/mission_net_payout.py (CACHE/netpayout990/{oid}.json).
That extractor kept every Schedule I Part II line whose recipient EIN is a DAFRC panel EIN (or, with a blank EIN,
whose normalised name matches exactly one panel name), with cash, non-cash and purpose text. No new parsing.

Universe and definitions
  top-50          DAFRC panel EINs ranked by FY2024 end-of-year DAF assets (dafrc-sponsor-schedule-d-fy2019-2024.csv,
                  filed or imputed as published).
  fiscal year     calendar year in which the tax period ends (DAFRC convention). FY2023-FY2024 covers tax years
                  2022 (June/other FYE filers) to 2024 (calendar-year filers).
  return choice   per (EIN, FY): latest object id per tax period; if a FY holds two periods, the one carrying
                  Schedule D DAF grants, then the larger |grants| (as in mission_net_payout.choose).
  edge            grantor (top-50) -> recipient (any DAFRC panel EIN), summed over Schedule I lines in one return.
                  Self-lines (recipient = grantor) are dropped.
  daf_primary     recipient segment is national (Standard), national donation processor or community foundation, or
                  the recipient is a top-50 sponsor that is not a university/hospital (adds NCF, Jewish Communal Fund,
                  Donors Trust, CJP, Thrivent and similar DAF-heavy single-issue sponsors). Other lines to
                  university/hospital, religious or single-issue sponsors are kept but flagged: most are grants to
                  those charities' own programmes, not to their DAFs.
  net flow        for a top-50 pair (a, b): a->b minus b->a in the same FY, and summed over FY2023-FY2024.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_daf_to_daf.py --np-cache CACHE   # CACHE holds netpayout990/
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_net_payout import itemized, panel_from  # noqa: E402

OUT = os.path.join(DATA, "daf-to-daf-flows-top50.csv")
FYS = (2023, 2024)
TOP_N = 50
DAF_PRIMARY = frozenset({"national", "processor", "community_foundation"})
SOURCE = ("IRS Form 990 Schedule I Part II (e-file XML, GivingTuesday mirror of IRS TEOS), lines cached by "
          "scripts/mission_net_payout.py; recipients classed via DAFRC 2025 panel by EIN")


def amt(l: Mapping) -> float:
    return (l.get("cash") or 0.0) + (l.get("noncash") or 0.0)


def load_np(cache: str) -> tuple[dict, ...]:
    d = os.path.join(cache, "netpayout990")

    def one(f):
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            return {**json.load(fh), "oid": f[:-5]}
    return tuple(one(f) for f in sorted(os.listdir(d)) if f.endswith(".json") and not f.endswith("_d.json"))


def pick_returns(exs: Sequence[Mapping]) -> dict:
    ok = tuple(x for x in exs if x.get("xml_status") == "ok" and x.get("tax_period_end"))
    per_period = {k: max(v, key=lambda x: x["oid"])
                  for k, v in _group_by_fast(ok, lambda x: (ein9(x.get("filer_ein") or ""), x["tax_period_end"])).items()}
    by_fy = _group_by_fast(per_period.values(), lambda x: (ein9(x["filer_ein"]), int(x["tax_period_end"][:4])))
    score = lambda x: (x.get("sched_d_daf_grants") is not None, abs(x.get("sched_d_daf_grants") or 0), x["tax_period_end"], x["oid"])  # noqa: E731
    return {k: max(v, key=score) for k, v in by_fy.items()}


def top_n(dafrc: Sequence[Mapping], n: int) -> dict:
    fy24 = sorted((r for r in dafrc if r["fiscal_year_end"] == "2024" and r["eoy_daf_assets"]),
                  key=lambda r: -float(r["eoy_daf_assets"]))
    return {ein9(r["ein"]): i + 1 for i, r in enumerate(fy24[:n])}


def edges_for(grantor: str, fy: int, ex: Mapping, panel: Mapping, rank: Mapping) -> tuple[dict, ...]:
    lines = tuple(l for l in ex.get("sched_i_panel_lines", ()) if l["matched_ein"] != grantor)
    by = _group_by_fast(lines, lambda l: l["matched_ein"])
    g = panel[grantor]

    def one(rec, ls):
        p = panel[rec]
        return {"grantor_ein": grantor, "grantor_name": g["name"], "grantor_rank_fy2024": rank[grantor],
                "grantor_segment": g["segment"], "fiscal_year": fy, "tax_period_end": ex["tax_period_end"],
                "recipient_ein": rec, "recipient_name_filed": ls[0]["recipient_name"], "recipient_panel_name": p["name"],
                "recipient_type": p["type"], "recipient_subtype": p["subtype"], "recipient_segment": p["segment"],
                "recipient_rank_fy2024": rank.get(rec, ""), "recipient_in_top50": int(rec in rank),
                "daf_primary_recipient": int(p["segment"] in DAF_PRIMARY or (rec in rank and p["segment"] != "university_hospital")),
                "match_method": ";".join(sorted({l["match_method"] for l in ls})), "schedule_i_lines": len(ls),
                "cash_usd": sum(l["cash"] for l in ls), "noncash_usd": sum(l["noncash"] for l in ls),
                "amount_usd": sum(amt(l) for l in ls), "largest_line_usd": max(amt(l) for l in ls),
                "purpose_text": " | ".join(sorted({(l.get("purpose") or "")[:60] for l in ls}))[:240],
                "grantor_sched_i_total": ex.get("sched_i_total"), "grantor_sched_i_itemized": int(itemized(ex)),
                "grantor_daf_grants_sched_d": ex.get("sched_d_daf_grants"),
                "share_of_grantor_daf_grants": (sum(amt(l) for l in ls) / ex["sched_d_daf_grants"])
                if ex.get("sched_d_daf_grants") else None,
                "return_object_id": ex["oid"], "xml_url": ex.get("xml_url") or XML_URL.format(oid=ex["oid"]), "source": SOURCE}
    return tuple(one(r, ls) for r, ls in by.items())


def add_net(edges: Sequence[Mapping], covered: frozenset) -> tuple[dict, ...]:
    """covered: (ein, fy) pairs whose return was parsed and itemises Schedule I."""
    idx = {(e["grantor_ein"], e["recipient_ein"], e["fiscal_year"]): e["amount_usd"] for e in edges}

    def one(e):
        a, b, fy = e["grantor_ein"], e["recipient_ein"], e["fiscal_year"]
        if not e["recipient_in_top50"]:
            return {**e, "reverse_return_covered": "", "reverse_amount_same_fy": None, "net_amount_same_fy": None,
                    "pair_a_to_b_fy2023_2024": None, "pair_b_to_a_fy2023_2024": None, "pair_net_fy2023_2024": None}
        rev = idx.get((b, a, fy), 0.0)
        ab = sum(idx.get((a, b, y), 0.0) for y in FYS)
        ba = sum(idx.get((b, a, y), 0.0) for y in FYS)
        return {**e, "reverse_return_covered": int((b, fy) in covered), "reverse_amount_same_fy": rev,
                "net_amount_same_fy": e["amount_usd"] - rev, "pair_a_to_b_fy2023_2024": ab,
                "pair_b_to_a_fy2023_2024": ba, "pair_net_fy2023_2024": ab - ba}
    return tuple(one(e) for e in edges)


def all_panel_totals(chosen: Mapping, panel: Mapping) -> dict:
    """P-99F-06: every panel grantor's Schedule I lines to panel recipients, by FY (DAF-primary vs all)."""
    def fy_tot(fy):
        rows = [(g, ex) for (g, y), ex in chosen.items() if y == fy and g in panel]
        lines = [(g, l) for g, ex in rows for l in ex.get("sched_i_panel_lines", ()) if l["matched_ein"] != g]
        dp = [amt(l) for g, l in lines if panel[l["matched_ein"]]["segment"] in DAF_PRIMARY]
        return {"grantor_returns": len(rows), "grantor_returns_itemized": sum(1 for _, ex in rows if itemized(ex)),
                "to_daf_primary": round(sum(dp)), "to_any_panel": round(sum(amt(l) for _, l in lines)),
                "lines_daf_primary": len(dp)}
    return {fy: fy_tot(fy) for fy in FYS}


def market(dafrc: Sequence[Mapping]) -> dict:
    return {fy: {"grants": sum(num(r["total_daf_grants"]) or 0 for r in dafrc if r["fiscal_year_end"] == str(fy)),
                 "contributions": sum(num(r["total_daf_contributions"]) or 0 for r in dafrc if r["fiscal_year_end"] == str(fy))}
            for fy in FYS}


FIELDS = ("grantor_ein", "grantor_name", "grantor_rank_fy2024", "grantor_segment", "fiscal_year", "tax_period_end",
          "recipient_ein", "recipient_name_filed", "recipient_panel_name", "recipient_type", "recipient_subtype",
          "recipient_segment", "recipient_rank_fy2024", "recipient_in_top50", "daf_primary_recipient", "match_method",
          "schedule_i_lines", "cash_usd", "noncash_usd", "amount_usd", "largest_line_usd", "purpose_text",
          "reverse_return_covered", "reverse_amount_same_fy", "net_amount_same_fy", "pair_a_to_b_fy2023_2024",
          "pair_b_to_a_fy2023_2024", "pair_net_fy2023_2024", "grantor_sched_i_total", "grantor_sched_i_itemized",
          "grantor_daf_grants_sched_d", "share_of_grantor_daf_grants", "return_object_id", "xml_url", "source")


def summary(edges: Sequence[Mapping], chosen: Mapping, panel: Mapping, rank: Mapping, dafrc: Sequence[Mapping]) -> dict:
    cov = {fy: {"returns": sum(1 for e in rank if (e, fy) in chosen),
                "itemized": sum(1 for e in rank if (e, fy) in chosen and itemized(chosen[(e, fy)])),
                "missing": sorted(panel[e]["name"] for e in rank if (e, fy) not in chosen),
                "not_itemized": sorted(panel[e]["name"] for e in rank if (e, fy) in chosen and not itemized(chosen[(e, fy)]))}
           for fy in FYS}
    mk = market(dafrc)

    def tot(pred):
        return {fy: round(sum(e["amount_usd"] for e in edges if e["fiscal_year"] == fy and pred(e))) for fy in FYS}
    t50 = tot(lambda e: e["recipient_in_top50"] and e["daf_primary_recipient"])
    t50_all = tot(lambda e: e["recipient_in_top50"])
    any_dp = tot(lambda e: e["daf_primary_recipient"])
    any_all = tot(lambda e: True)
    by_seg = {s: tot(lambda e, s=s: e["recipient_segment"] == s) for s in sorted({e["recipient_segment"] for e in edges})}
    covered = frozenset(k for k, ex in chosen.items() if itemized(ex))
    both = lambda e: (e["grantor_ein"], e["fiscal_year"]) in covered and (e["recipient_ein"], e["fiscal_year"]) in covered  # noqa: E731
    g_ok = lambda e: panel[e["grantor_ein"]]["segment"] != "university_hospital"  # noqa: E731
    pairs = {}
    for e in edges:
        if e["recipient_in_top50"] and e["daf_primary_recipient"] and g_ok(e) and both(e):
            k = tuple(sorted((e["grantor_ein"], e["recipient_ein"])))
            pairs.setdefault(k, {"a": k[0], "b": k[1], "a_to_b": 0.0, "b_to_a": 0.0})
            pairs[k]["a_to_b" if e["grantor_ein"] == k[0] else "b_to_a"] += e["amount_usd"]
    pl = sorted(({"pair": f"{panel[p['a']]['name']} <-> {panel[p['b']]['name']}", "a_to_b": round(p["a_to_b"]),
                  "b_to_a": round(p["b_to_a"]), "gross": round(p["a_to_b"] + p["b_to_a"]),
                  "net_abs": round(abs(p["a_to_b"] - p["b_to_a"])), "two_way": int(p["a_to_b"] > 0 and p["b_to_a"] > 0)}
                 for p in pairs.values()), key=lambda d: -d["gross"])
    net_in = {}
    for e in edges:
        if e["recipient_in_top50"] and e["daf_primary_recipient"] and g_ok(e) and both(e):
            net_in[e["recipient_ein"]] = net_in.get(e["recipient_ein"], 0.0) + e["amount_usd"]
            net_in[e["grantor_ein"]] = net_in.get(e["grantor_ein"], 0.0) - e["amount_usd"]
    return {"top50_coverage": cov,
            "top50_to_top50_daf_primary": t50, "top50_to_top50_all_segments": t50_all,
            "top50_to_any_panel_daf_primary": any_dp, "top50_to_any_panel_all": any_all, "top50_to_panel_by_segment": by_seg,
            "dafrc_market": mk,
            "share_top50_daf_primary_of_market_grants": {fy: any_dp[fy] / mk[fy]["grants"] for fy in FYS},
            "share_top50_to_top50_of_market_grants": {fy: t50[fy] / mk[fy]["grants"] for fy in FYS},
            "all_panel_grantors": all_panel_totals(chosen, panel),
            "edges": len(edges), "edges_top50_pairs": sum(e["recipient_in_top50"] for e in edges),
            "name_matched_edges": sum(1 for e in edges if "name" in e["match_method"]),
            "pairs_daf_primary": len(pl), "pairs_two_way": sum(p["two_way"] for p in pl),
            "two_way_gross": sum(p["gross"] for p in pl if p["two_way"]),
            "two_way_net_abs": sum(p["net_abs"] for p in pl if p["two_way"]),
            "all_pairs_gross": sum(p["gross"] for p in pl), "all_pairs_net_abs": sum(p["net_abs"] for p in pl),
            "pair_basis": "top-50 pairs, neither a university/hospital, both returns parsed and itemised in that FY",
            "excluded_uncovered_pair_flows": {fy: round(sum(e["amount_usd"] for e in edges if e["fiscal_year"] == fy and e["recipient_in_top50"]
                                                            and e["daf_primary_recipient"] and g_ok(e) and not both(e))) for fy in FYS},
            "top_pairs": pl[:25],
            "net_position_fy2023_2024": sorted(({"sponsor": panel[k]["name"], "net_in": round(v)} for k, v in net_in.items()),
                                               key=lambda d: -d["net_in"])}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True, help="cache dir holding netpayout990/ (mission_net_payout.py)")
    a = ap.parse_args(argv)
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    raw = tuple(e for g in rank for fy in FYS if (g, fy) in chosen for e in edges_for(g, fy, chosen[(g, fy)], panel, rank))
    covered = frozenset(k for k, ex in chosen.items() if itemized(ex))
    edges = tuple(sorted(add_net(raw, covered), key=lambda e: (e["fiscal_year"], -e["amount_usd"])))
    write_csv(OUT, edges, FIELDS)
    print(json.dumps({"top50": [{"rank": r, "ein": e, "name": panel[e]["name"], "segment": panel[e]["segment"]}
                                for e, r in sorted(rank.items(), key=lambda kv: kv[1])],
                      **summary(edges, chosen, panel, rank, dafrc)}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
