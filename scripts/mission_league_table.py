#!/usr/bin/env python3
"""League table of DAF sponsors and market concentration, FY2021-FY2025 (queue item P-NEW-LGT-01).

Stdlib only; functional style (pure transforms, I/O at the edges). Nothing is fetched or parsed anew.

Inputs (all repository data)
  * data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv  DAFRC 2025 panel, as published
  * data/mission-2026-11-14/dafrc-corrections-itemized.csv           rules R1-R4 (applied = 1 rows override DAFRC)
  * data/mission-2026-11-14/dafrc-corrected-market-totals.csv        check: rebuilt sums must equal corrected totals
  * data/mission-2026-11-14/dafrc-market-totals-netted.csv           R5 DAF-to-DAF netting, market level (3 tiers)
  * data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv + form990-harvest-2026-fill.csv
                                                                      FY2025 filed Schedule D Part I (partial year)
  * optional --np-cache: the netpayout990/ Schedule I cache of scripts/mission_net_payout.py. With it, the R5 lines
    are rebuilt exactly as in scripts/mission_market_netting.py and attributed to each grantor (netted grants) and
    recipient (netted contributions); the rebuild is checked against dafrc-market-totals-netted.csv.

Conventions
  * FY = calendar year in which the tax period ends (DAFRC convention). FY2020 is used only as the baseline for
    FY2021 entrants/exits (recency rule).
  * FY2021-24 values are the corrected sponsor-year values (DAFRC as published, overridden by applied R1-R4 rows,
    plus R4 additions). FY2025 values are filed Schedule D Part I values for the sponsors whose FY2025 return is
    parsed; they are NOT corrected, NOT a market total and NOT extrapolated.
  * Rank = rank by EOY DAF assets (ties broken by EIN). Shares are of the corrected market total (FY2021-24); FY2025
    shares are of the covered (filed) total only and are labelled so.
  * HHI = sum over sponsors of (100 x share)^2, 0-10,000 scale; negative sponsor values count as 0 in the numerator.

Usage
  python3 scripts/mission_league_table.py [--np-cache DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402

CORR_ITEMS = os.path.join(DATA, "dafrc-corrections-itemized.csv")
CORR_TOTALS = os.path.join(DATA, "dafrc-corrected-market-totals.csv")
NETTED = os.path.join(DATA, "dafrc-market-totals-netted.csv")
HARVEST = os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv")
FILL = os.path.join(DATA, "form990-harvest-2026-fill.csv")
OUT_LEAGUE = os.path.join(DATA, "daf-sponsor-league-table-fy2021-2025.csv")
OUT_CONC = os.path.join(DATA, "daf-concentration-fy2021-2025.csv")

FYS_CORR = (2020, 2021, 2022, 2023, 2024)
FYS_OUT = (2021, 2022, 2023, 2024, 2025)
TOP = 50
METRICS = {"daf_assets_eoy": ("eoy_daf_assets", "source_eoy_daf_assets", "sched_d_daf_eoy_value"),
           "daf_contributions": ("total_daf_contributions", "source_total_daf_contributions", "sched_d_daf_contributions"),
           "daf_grants": ("total_daf_grants", "source_total_daf_grants", "sched_d_daf_grants"),
           "daf_accounts_eoy": ("number_of_daf_accounts", "source_number_of_accounts", "sched_d_daf_count")}
CR_N = (1, 3, 5, 10, 50)
SRC_CORR = ("DAFRC 2025 sponsor dataset (dafrc-sponsor-schedule-d-fy2019-2024.csv) + rules R1-R4 "
            "(dafrc-corrections-itemized.csv); totals = dafrc-corrected-market-totals.csv")
SRC_25 = ("IRS Form 990 Schedule D Part I as filed: form990-returns-schedule-d-harvest-full.csv (FY2025 ok rows) "
          "+ form990-harvest-2026-fill.csv (144 TEOS 2026 zip rows)")
SRC_NET = "R5 netting: dafrc-market-totals-netted.csv; per-sponsor attribution rebuilt with scripts/mission_market_netting.py functions"

# Known structural events behind top-50 churn. Each entry cites the repository report that documents it.
EVENTS = {
    "141782466": ("merger", "Ayco Charitable Foundation merged into Goldman Sachs Philanthropy Fund (GS DAPF) on 2025-07-01; "
                  "final FY6/2025 return reports 0 DAFs and $0 EOY and a $1,162.2m Schedule I/N transfer to GS DAPF "
                  "(queue-batch34-netting-filings.md P-990-03; queue-batch35-panel-screens.md)"),
    "300748315": ("termination", "BNY Mellon Charitable Gift Fund terminated in December 2024 and was wound into "
                  "Renaissance Charitable Foundation (RCF), granting $619.8m to RCF; FY2024 EOY $4.7m after R1 "
                  "(queue-state-filings-transfer-terms.md; queue-batch34-netting-filings.md top pairs)"),
    "472088631": ("termination", "Jasper Ridge Charitable Fund: FY2022 final DAF year, 0 EOY after Schedule N transfers of about "
                  "$1.32bn mostly to Schwab and Fidelity; R2 removes the $1.49bn DAFRC imputation; 990-PF from 2023 "
                  "(full-universe-990-harvest-and-corrected-totals.md §5; queue-batch35-panel-screens.md §3)"),
    "472199684": ("termination", "TIAA Charitable: final short-year FY2021 return reports 0 after a $138.5m transfer to RCF "
                  "(2021-03-09); R2 removes the $0.26bn imputation (full-universe-990-harvest-and-corrected-totals.md §5)"),
    "474844275": ("late_filer_r4", "Donors Fund Inc: no DAFRC FY2023-24 rows; FY2024 added by R4 from the amended TY2024 "
                  "return filed 2026-03-12 (full-universe-990-harvest-and-corrected-totals.md §5)"),
    "810739440": ("reclassification", "AOGF (Benevity): FYE 2026-03 return moves micro-donor accounts from the Schedule D "
                  "DAF column to the other-funds column (710,352 -> 695 DAFs); outside FY2021-25 but changes the "
                  "account metric from FY2026 (queue-batch35-panel-screens.md §2)"),
}


# ----------------------------------------------------------------------------- pure transforms
def identity(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict:
    """ein -> latest name/type/subtype (DAFRC row, else the corrections file for R4-only EINs)."""
    by = _group_by_fast(dafrc, lambda r: ein9(r["ein"]))
    ids = {e: (lambda r: {"name": r["name"], "type": r["type"], "subtype": r["subtype"]})(max(rs, key=lambda r: r["fiscal_year_end"]))
           for e, rs in by.items()}
    extra = {ein9(r["ein"]): {"name": r["name"], "type": r["type"], "subtype": ""} for r in items if ein9(r["ein"]) not in ids}
    return {**extra, **ids}


def corrected(dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict:
    """(ein, fy) -> {metric: value, metric+'_imputed_kept': bool}; DAFRC overridden by applied R1-R4 rows."""
    base = {(ein9(r["ein"]), int(r["fiscal_year_end"])): {
        **{m: num(r[c[0]]) or 0.0 for m, c in METRICS.items()},
        **{f"{m}_imputed": r[c[1]] == "Imputed" for m, c in METRICS.items()}}
        for r in dafrc if int(r["fiscal_year_end"]) in FYS_CORR}
    over = _group_by_fast((r for r in items if r["applied"] == "1" and int(r["fiscal_year"]) in FYS_CORR),
                          lambda r: (ein9(r["ein"]), int(r["fiscal_year"])))

    def merge(k):
        b = base.get(k, {**{m: 0.0 for m in METRICS}, **{f"{m}_imputed": False for m in METRICS}})
        o = {r["metric"]: num(r["corrected_value"]) or 0.0 for r in over.get(k, ())}
        rules = sorted({r["rule"] for r in over.get(k, ())})
        return {**b, **o, **{f"{m}_imputed": b[f"{m}_imputed"] and m not in o for m in METRICS},
                "rules": ";".join(rules), "in_dafrc": k in base}
    return {k: merge(k) for k in set(base) | set(over)}


def fy2025_filed(harvest: Sequence[Mapping], fill: Sequence[Mapping]) -> dict:
    """ein -> filed FY2025 values; latest submission per EIN (amended supersedes); fill rows replace http_404 rows."""
    rows = [r for r in harvest if r["fiscal_year"] == "2025" and r["xml_status"] == "ok"] + \
           [r for r in fill if r["fiscal_year"] == "2025" and r["xml_status"].startswith("ok")]
    by = _group_by_fast(rows, lambda r: ein9(r["ein"]))
    pick = {e: max(rs, key=lambda r: (r["return_ts"], r["return_object_id"])) for e, rs in by.items()}
    return {e: {**{m: num(r[c[2]]) for m, c in METRICS.items()},
                **({"daf_accounts_eoy": None, "flags": "accounts_implausible_avg_lt_5usd"} if implausible_count(r) else {"flags": ""}),
                "tax_period_end": r["tax_period_end"], "return_object_id": r["return_object_id"],
                "amended": r["amended_ind"], "name_990": r["filer_name_990"] or r["sponsor_name"]}
            for e, r in pick.items()}


def implausible_count(r: Mapping) -> bool:
    """FY2025 filed count screen (same spirit as the corrected-totals 'implausible count'): >1,000 DAFs averaging < $5."""
    n, v = num(r["sched_d_daf_count"]), num(r["sched_d_daf_eoy_value"])
    return bool(n and n > 1000 and v is not None and v < 5 * n)


def ranked(vals: Mapping[str, float]) -> list[tuple[str, float]]:
    return sorted(((e, v) for e, v in vals.items() if v is not None), key=lambda t: (-t[1], t[0]))


def conc(vals: Mapping[str, float], total: float) -> dict:
    r = ranked(vals)
    pos = [max(v, 0.0) for _, v in r]
    cr = {f"cr{n}": (sum(pos[:n]) / total if total else None) for n in CR_N}
    hhi = sum((100 * v / total) ** 2 for v in pos) if total else None
    return {**cr, "hhi": hhi, "n_sponsors_positive": sum(1 for v in pos if v > 0),
            "top1_ein": r[0][0] if r else "", "sum_values": sum(v for _, v in r)}


def netting_by_sponsor(np_cache: str | None, dafrc: Sequence[Mapping], items: Sequence[Mapping]) -> dict | None:
    """{tier: {'out': {(ein, fy): $}, 'in': {(ein, fy): $}}} rebuilt with mission_market_netting, or None."""
    if not np_cache:
        return None
    import mission_market_netting as mn  # noqa: E402  (reuses the batch-34 rule implementation unchanged)
    from mission_daf_to_daf import load_np, pick_returns  # noqa: E402
    from mission_net_payout import panel_from  # noqa: E402
    panel = panel_from(dafrc)
    corr = mn.corrected_values(dafrc, items)
    shares = mn.cost_shares(read_csv(mn.COST))
    seg_med = lambda seg, k: mn.med([mn.clip01(shares[e][k]) for e in panel if panel[e]["segment"] == seg  # noqa: E731
                                     and e in shares and shares[e][k] is not None]) or 1.0
    defaults = {k: {s: seg_med(s, k) for s in {p["segment"] for p in panel.values()}} for k in ("assets", "grants")}
    lines = mn.panel_lines(pick_returns(load_np(np_cache)), panel)
    decision = {r: mn.recipient_decision(panel[r], shares.get(r)) for r in {l["recipient"] for l in lines}}
    wl = tuple({**l, "w": mn.weights(l, panel, decision, shares, defaults)} for l in lines)
    net = {t: mn.capped(wl, t, corr) for t in mn.TIERS}
    agg = lambda xs, side: {k: sum(x["net_amt"] for x in v) for k, v in _group_by_fast(xs, lambda x: (x[side], x["fy"])).items()}  # noqa: E731
    return {t: {"out": agg(net[t], "grantor"), "in": agg(net[t], "recipient")} for t in mn.TIERS}


def churn(prev_top: Sequence[str], cur_top: Sequence[str]) -> tuple[set, set]:
    return set(cur_top) - set(prev_top), set(prev_top) - set(cur_top)


def churn_reason(e: str, fy: int, kind: str, prev_rank: dict, cur_rank: dict, cur: Mapping | None, prev: Mapping | None,
                 fy25_cov: set | None) -> tuple[str, str]:
    ev = EVENTS.get(e)
    if kind == "exit":
        if fy == 2025 and fy25_cov is not None and e not in fy25_cov:
            return ("not_yet_filed", "No parsed FY2025 return yet (coverage gap, not an exit)")
        if ev and ev[0] in ("merger", "termination"):
            return ev
        if cur is None:
            return ("no_row", "No sponsor-year row in this FY (no DAFRC row and no R4 addition)")
        if (cur.get("daf_assets_eoy") or 0) <= 0:
            return ("zero_daf_assets", f"EOY DAF assets {cur.get('daf_assets_eoy'):.0f} in this FY")
        a0, a1 = (prev or {}).get("daf_assets_eoy") or 0, cur.get("daf_assets_eoy") or 0
        g = f"{(a1 / a0 - 1) * 100:+.1f}%" if a0 else "n/a"
        return ("rank_drift", f"Fell from rank {prev_rank.get(e)} to {cur_rank.get(e)} (assets {g})")
    if ev and ev[0] == "late_filer_r4":
        return ev
    if prev is None or (prev.get("daf_assets_eoy") or 0) <= 0:
        return ("new_to_panel", f"No FY{fy - 1} sponsor-year row with positive assets (first panel year in the window)")
    a0, a1 = prev.get("daf_assets_eoy") or 0, (cur or {}).get("daf_assets_eoy") or 0
    return ("rank_drift", f"Rose from rank {prev_rank.get(e)} to {cur_rank.get(e)} (assets {(a1 / a0 - 1) * 100:+.1f}%)")


# ----------------------------------------------------------------------------- assembly
def build(dafrc, items, totals, netted_rows, harvest, fill, nets):
    ids = identity(dafrc, items)
    corr = corrected(dafrc, items)
    f25 = fy2025_filed(harvest, fill)
    tot = {(int(r["fiscal_year"]), r["metric"]): float(r["corrected_value"]) for r in totals}
    net_tot = {(int(r["fiscal_year"]), r["metric"], r["tier"]): float(r["netted_value"]) for r in netted_rows}

    def year_vals(fy):  # ein -> metric dict
        if fy == 2025:
            return {e: v for e, v in f25.items()}
        return {e: v for (e, y), v in corr.items() if y == fy}
    yv = {fy: year_vals(fy) for fy in (*FYS_CORR, 2025)}
    check = {f"{fy}_{m}": {"rebuilt": round(sum(v[m] for v in yv[fy].values())), "corrected_total": round(tot[(fy, m)]),
                           "match": round(sum(v[m] for v in yv[fy].values())) == round(tot[(fy, m)])}
             for fy in FYS_CORR for m in METRICS}

    def rank_of(fy, m="daf_assets_eoy"):
        return {e: i + 1 for i, (e, _) in enumerate(ranked({e: v.get(m) for e, v in yv[fy].items()}))}
    ranks = {fy: {m: rank_of(fy, m) for m in METRICS} for fy in yv}
    tops = {fy: [e for e, _ in ranked({e: v.get("daf_assets_eoy") for e, v in yv[fy].items()})[:TOP]] for fy in yv}
    cov25 = set(f25)

    def market(fy, m):
        if fy == 2025:
            return sum(max(v.get(m) or 0, 0) for v in yv[2025].values())
        return tot[(fy, m)]

    def net_vals(fy, side, tier="central"):
        if not nets or fy == 2025:
            return None
        metric = "daf_grants" if side == "out" else "daf_contributions"
        return {e: v[metric] - nets[tier][side].get((e, fy), 0.0) for e, v in yv[fy].items()}

    def row(fy, e, rtype, status, reason):
        v = yv[fy].get(e)
        prev = yv[fy - 1].get(e)
        mk = {m: market(fy, m) for m in METRICS}
        ng, nc = net_vals(fy, "out"), net_vals(fy, "in")
        ng_tot = net_tot.get((fy, "daf_grants", "central"))
        nc_tot = net_tot.get((fy, "daf_contributions", "central"))
        pr = ranks[fy - 1]["daf_assets_eoy"].get(e)
        cr = ranks[fy]["daf_assets_eoy"].get(e)
        idn = ids.get(e, {"name": (v or {}).get("name_990", ""), "type": "", "subtype": ""})
        imputed = ";".join(m for m in METRICS if v and v.get(f"{m}_imputed")) if fy < 2025 else ""
        return {"fiscal_year": fy, "row_type": rtype, "rank_assets": cr, "ein": e, "name": idn["name"],
                "type": idn["type"], "subtype": idn["subtype"],
                **{m: (v or {}).get(m) for m in METRICS},
                **{f"share_{m}": ((v or {}).get(m) / mk[m] if v and v.get(m) is not None and mk[m] else None) for m in METRICS},
                "share_basis": "fy2025_filed_covered_total_only" if fy == 2025 else "corrected_market_total_R1_R4",
                "rank_contributions": ranks[fy]["daf_contributions"].get(e), "rank_grants": ranks[fy]["daf_grants"].get(e),
                "prev_rank_assets": pr, "rank_change": (pr - cr) if pr and cr else None,
                "assets_growth_yoy": ((v["daf_assets_eoy"] / prev["daf_assets_eoy"] - 1) if v and prev and v.get("daf_assets_eoy") is not None
                                      and (prev.get("daf_assets_eoy") or 0) > 0 else None),
                "churn_status": status, "churn_reason_class": reason[0], "churn_reason": reason[1],
                "daf_grants_netted_central": ng.get(e) if ng and e in ng else None,
                "share_daf_grants_netted_central": (ng[e] / ng_tot if ng and e in ng and ng_tot else None),
                "daf_contributions_netted_central": nc.get(e) if nc and e in nc else None,
                "r5_outbound_central": (nets["central"]["out"].get((e, fy), 0.0) if nets and fy < 2025 else None),
                "r5_inbound_central": (nets["central"]["in"].get((e, fy), 0.0) if nets and fy < 2025 else None),
                "corrections_applied": (v or {}).get("rules", "") if fy < 2025 else "",
                "imputed_kept_metrics": imputed,
                "fy2025_tax_period_end": (v or {}).get("tax_period_end", "") if fy == 2025 else "",
                "fy2025_return_object_id": (v or {}).get("return_object_id", "") if fy == 2025 else "",
                "fy2025_flags": (v or {}).get("flags", "") if fy == 2025 else "",
                "value_basis": "filed_fy2025_uncorrected" if fy == 2025 else "corrected_R1_R4",
                "source": SRC_25 if fy == 2025 else SRC_CORR}

    def year_rows(fy):
        """(rows, churn summary) for one FY. FY2025 is partial: it is not re-ranked against FY2024 (see docstring)."""
        pr, cr = ranks[fy - 1]["daf_assets_eoy"], ranks[fy]["daf_assets_eoy"]
        if fy == 2025:
            thr = yv[2024][tops[2024][-1]]["daf_assets_eoy"]
            members = [e for e in tops[2024] if e in cov25]
            cands = [e for e in tops[2025] if e not in tops[2024] and (yv[2025][e]["daf_assets_eoy"] or 0) >= thr]
            missing = [e for e in tops[2024] if e not in cov25]

            def status(e):
                ev = EVENTS.get(e)
                if ev and ev[0] == "merger" and (yv[2025][e]["daf_assets_eoy"] or 0) <= 0:
                    return "exit", ev
                g = yv[2025][e]["daf_assets_eoy"] / yv[2024][e]["daf_assets_eoy"] - 1
                return "filed_fy2025", ("filed", f"FY2024 rank {pr.get(e)}; FY2025 filed assets {g * 100:+.1f}% vs FY2024 corrected")
            rows = ([row(fy, e, "fy2025_filed_fy2024_top50", *status(e)) for e in members]
                    + [row(fy, e, "fy2025_filed_above_fy2024_cutoff", "provisional_entrant",
                           ("provisional", f"Not in FY2024 top 50 (rank {pr.get(e)}); FY2025 filed assets above the FY2024 "
                                           f"rank-50 value ${thr / 1e9:.3f}bn; provisional until all FY2025 returns are filed"))
                       for e in cands]
                    + [row(fy, e, "fy2025_not_yet_filed", "not_yet_filed",
                           ("not_yet_filed", "FY2024 top-50 sponsor with no parsed FY2025 return (coverage gap, not an exit)"))
                       for e in missing])
            return rows, {"fy2024_top50_filed": len(members), "fy2024_top50_not_filed": len(missing),
                          "provisional_entrants": len(cands), "confirmed_exits": sum(1 for r in rows if r["churn_status"] == "exit"),
                          "fy2024_rank50_assets": thr}
        ent, ext = churn(tops[fy - 1], tops[fy])
        rs = {e: churn_reason(e, fy, "entrant", pr, cr, yv[fy].get(e), yv[fy - 1].get(e), None) for e in ent}
        xs = {e: churn_reason(e, fy, "exit", pr, cr, yv[fy].get(e), yv[fy - 1].get(e), None) for e in ext}
        rows = ([row(fy, e, "top50", "entrant" if e in ent else "stayed", rs.get(e, ("", ""))) for e in tops[fy]]
                + [row(fy, e, "exit", "exit", xs[e]) for e in sorted(ext, key=lambda e: pr.get(e, 9999))])
        return rows, {"entrants": len(ent), "exits": len(ext),
                      "exit_classes": {c: sum(1 for x in xs.values() if x[0] == c) for c in {x[0] for x in xs.values()}}}
    per_year = {fy: year_rows(fy) for fy in FYS_OUT}
    league = [r for fy in FYS_OUT for r in per_year[fy][0]]
    churn_out = {fy: per_year[fy][1] for fy in FYS_OUT}

    def conc_rows(fy):
        out = []
        for m in METRICS:
            vals = {e: v.get(m) for e, v in yv[fy].items()}
            mk = market(fy, m)
            c = conc(vals, mk)
            out.append({"fiscal_year": fy, "metric": m, "basis": "fy2025_filed_covered_only" if fy == 2025 else "gross_corrected",
                        "market_total": mk, **c, "top1_name": ids.get(c["top1_ein"], {}).get("name", ""),
                        "source": SRC_25 if fy == 2025 else SRC_CORR})
        if nets and fy < 2025:
            for tier in ("lower", "central", "upper"):
                for side, m in (("out", "daf_grants"), ("in", "daf_contributions")):
                    vals = net_vals(fy, side, tier)
                    mk = net_tot[(fy, m, tier)]
                    c = conc(vals, mk)
                    out.append({"fiscal_year": fy, "metric": m, "basis": f"netted_r5_{tier}", "market_total": mk, **c,
                                "top1_name": ids.get(c["top1_ein"], {}).get("name", ""), "source": SRC_NET})
        return out
    conc_all = [r for fy in FYS_OUT for r in conc_rows(fy)]

    # FY2025 coverage relative to FY2024 corrected values (no extrapolation)
    t24 = tops[2024]
    cov = {"fy2025_sponsors_with_parsed_return": len(f25),
           "fy2024_sponsor_rows": len(yv[2024]),
           "fy2024_corrected_assets_covered_share": sum(yv[2024][e]["daf_assets_eoy"] for e in f25 if e in yv[2024]) / tot[(2024, "daf_assets_eoy")],
           "fy2024_corrected_grants_covered_share": sum(yv[2024][e]["daf_grants"] for e in f25 if e in yv[2024]) / tot[(2024, "daf_grants")],
           "fy2024_top50_with_fy2025_return": sum(1 for e in t24 if e in f25),
           "fy2024_top50_assets_covered_share": sum(yv[2024][e]["daf_assets_eoy"] for e in t24 if e in f25) / sum(yv[2024][e]["daf_assets_eoy"] for e in t24),
           "fy2024_top50_missing_fy2025": [ids[e]["name"] for e in t24 if e not in f25],
           "fy2025_filed_totals_covered": {m: market(2025, m) for m in METRICS},
           "fy2025_accounts_screened_out": [(e, v["name_990"]) for e, v in f25.items() if v["flags"]],
           "fy2024_top50_filers_same_sponsor_change": {
               m: {"fy2024_corrected": sum(yv[2024][e][m] for e in t24 if e in f25),
                   "fy2025_filed": sum(f25[e][m] or 0 for e in t24 if e in f25)} for m in METRICS}}
    return league, conc_all, check, churn_out, cov, tops, yv, ids, ranks


FIELDS_L = ("fiscal_year", "row_type", "rank_assets", "ein", "name", "type", "subtype", *METRICS,
            *(f"share_{m}" for m in METRICS), "share_basis", "rank_contributions", "rank_grants", "prev_rank_assets",
            "rank_change", "assets_growth_yoy", "churn_status", "churn_reason_class", "churn_reason",
            "daf_grants_netted_central", "share_daf_grants_netted_central", "daf_contributions_netted_central",
            "r5_outbound_central", "r5_inbound_central", "corrections_applied", "imputed_kept_metrics",
            "fy2025_tax_period_end", "fy2025_return_object_id", "fy2025_flags", "value_basis", "source")
FIELDS_C = ("fiscal_year", "metric", "basis", "market_total", "sum_values", "n_sponsors_positive",
            *(f"cr{n}" for n in CR_N), "hhi", "top1_ein", "top1_name", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", default=None, help="dir holding netpayout990/ (optional; enables per-sponsor R5)")
    a = ap.parse_args(argv)
    dafrc, items = read_csv(DAFRC_CSV), read_csv(CORR_ITEMS)
    nets = netting_by_sponsor(a.np_cache, dafrc, items)
    netted_rows = read_csv(NETTED)
    league, conc_all, check, ch, cov, tops, yv, ids, ranks = build(
        dafrc, items, read_csv(CORR_TOTALS), netted_rows, read_csv(HARVEST), read_csv(FILL), nets)
    net_check = None
    if nets:
        net_check = {f"{r['fiscal_year']}_{r['metric']}_{r['tier']}": {
            "rebuilt": round(sum(v for (e, fy), v in nets[r["tier"]]["out"].items() if fy == int(r["fiscal_year"]))),
            "published": int(r["r5_netting_amount"])} for r in netted_rows if r["metric"] == "daf_grants"}
    write_csv(OUT_LEAGUE, league, FIELDS_L)
    write_csv(OUT_CONC, conc_all, FIELDS_C)
    persist = {"in_top50_all_fy2021_2024": sum(1 for e in tops[2021] if all(e in tops[fy] for fy in (2022, 2023, 2024)))}
    top10 = {fy: [(ranks[fy]["daf_assets_eoy"][e], ids.get(e, {}).get("name", e), round(yv[fy][e]["daf_assets_eoy"] or 0))
                  for e in tops[fy][:10]] for fy in FYS_OUT}
    print(json.dumps({"corrected_totals_rebuild_check": check, "netting_rebuild_check": net_check, "churn": ch,
                      "fy2025_coverage": cov, "persistence": persist, "top10": top10,
                      "league_rows": len(league), "concentration_rows": len(conc_all)}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
