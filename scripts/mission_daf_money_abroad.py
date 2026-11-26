#!/usr/bin/env python3
"""DAF money that ends up abroad through US-registered recipients, top-50 sponsors, FY2023-FY2024 (P-B45N31-01).

Extends the nine-intermediary pass-through of P-NEW-FGN-01 (scripts/mission_foreign_grants.py) to the 150 largest
NTEE-Q or "American/US friends of" recipients of top-50 sponsors' Schedule I dollars.

Steps (pure transforms; I/O only in `main` and the cached fetchers it calls)
  1. Lines     Universe, return choice and Schedule I lines exactly as scripts/mission_exception_load.py: top-50
               DAFRC sponsors by FY2024 DAF assets; one return per sponsor x FY (mission_daf_to_daf.pick_returns);
               itemising sponsor-years only; filer totals rows dropped (`drop_totals_rows`); DAF-to-DAF lines
               flagged by mission_recipient_sectors.annotate (batch-34 whitelist, self-lines) and excluded.
               Main scope excludes the two university/hospital sponsors, as in P-NEW-FGN-01.
  2. Targets   recipient EIN with EO BMF NTEE_CD major group Q, or a Schedule I or BMF name matching the FRIENDS
               pattern of mission_foreign_grants.py. Ranked by pooled FY2023-24 net Schedule I dollars; top 150.
  3. Returns   each target's Form 990 for tax periods ending in 2023 and 2024 (IRS TEOS index CSVs, latest object
               id per tax period), parsed with mission_foreign_grants.load_extract (Part IX lines 1-3 and 25,
               Schedule F Parts I-III). Streamed from the GivingTuesday mirror of IRS TEOS when not cached.
  4. Shares    per recipient-year:
                 grant_mix   = line 3 / lines 1-3               (P-NEW-FGN-01 intermediary basis)
                 l3_of_exp   = line 3 / line 25                  (floor: foreign grants only)
                 expense     = min(line 25, max(line 3, Sched F Part I non-investment expenditures)) / line 25
                               (central: grants plus programme spending abroad)
               Inbound DAF dollars of the same FY x share = dollars estimated to reach abroad; a missing year
               borrows the other year's share (flagged).
  5. Regions   central estimate allocated by the recipient-year's Schedule F Part I non-investment rows (fallback
               Part II + III), regions normalised by mission_foreign_grants.region_of.
  6. Compare   with the direct route (Part IX line 3 of the sponsors, daf-foreign-grants-schedule-f-2023-2024.csv
               scope_total rows); extrapolation to targets outside the top 150 is labelled [I].

Stdlib only; functional style.

Usage:
  python3 scripts/mission_daf_money_abroad.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRS --extract-cache EC [--fetch] [--workers 6] [--top 150]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_share_recipient_revenue import choose_filings, load_index  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_foreign_grants import FRIENDS, INTERMEDIARIES, amt, load_all, region_of  # noqa: E402
from mission_foreign_grants import activity_of as _activity_of  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_bmf, load_lines  # noqa: E402

OUT = os.path.join(DATA, "daf-money-abroad-2026-11-19.csv")
SCHED_F_CSV = os.path.join(DATA, "daf-foreign-grants-schedule-f-2023-2024.csv")
MAIN = "all_ex_university_hospital"
SOURCE = ("Sponsors: IRS Form 990 Schedule I Part II lines (mission_recipient_sectors.py line cache; DAF-to-DAF and "
          "totals rows dropped as in mission_exception_load.py); recipients: IRS EO BMF NTEE_CD (2026-11 snapshot) and "
          "own Form 990 Part IX lines 1-3, 25 and Schedule F Parts I-III (e-file XML, GivingTuesday mirror of IRS TEOS; "
          "IRS TEOS index CSVs); direct route from daf-foreign-grants-schedule-f-2023-2024.csv")
METHODS = ("expense", "l3_of_exp", "grant_mix")


# ----------------------------------------------------------------------------- targets (pure)
def activity_of(txt: str) -> str:
    """mission_foreign_grants.activity_of, except that program-related investments count as programme activity."""
    up = (txt or "").upper()
    return "program_or_other" if "PROGRAM RELATED INVEST" in up or "PROGRAM-RELATED INVEST" in up else _activity_of(txt)



def is_friends(r: Mapping, bmf: Mapping) -> bool:
    return bool(FRIENDS.search((r["name"] or "").upper())
                or FRIENDS.search((bmf.get(r["ein"], {}).get("bmf_name") or "").upper()))


def basis_of(r: Mapping, bmf: Mapping) -> str:
    q, f = r["ntee"][:1] == "Q", is_friends(r, bmf)
    return "q+friends" if q and f else "q" if q else "friends" if f else ""


def target_lines(ann: Mapping, bmf: Mapping) -> tuple:
    """(sponsor_ein, fy, recipient_key, ein, name, amount, basis) for net lines to Q / friends-of recipients."""
    return tuple((k[0], k[1], r["key"], r["ein"], r["name"], r["amount"], b)
                 for k, rs in ann.items() for r in rs if not r["d2d"]
                 for b in (basis_of(r, bmf),) if b)


def inbound(tl: Sequence[tuple], weights: Mapping) -> dict:
    """recipient key -> {ein, name, basis, si: {fy: usd}, dw: {fy: usd}, grantors, by_sponsor: {(sp, fy): usd}}."""
    def step(acc, t):
        sp, fy, key, e, nm, a, b = t
        cur = acc.get(key, {"ein": e, "name": nm, "basis": b, "si": {}, "dw": {}, "grantors": frozenset(), "by_sponsor": {}})
        w = weights.get((sp, fy), 1.0)
        return {**acc, key: {**cur, "si": {**cur["si"], fy: cur["si"].get(fy, 0.0) + a},
                             "dw": {**cur["dw"], fy: cur["dw"].get(fy, 0.0) + a * w},
                             "grantors": cur["grantors"] | {sp},
                             "by_sponsor": {**cur["by_sponsor"], (sp, fy): cur["by_sponsor"].get((sp, fy), 0.0) + a}}}
    by_key = _group_by_fast(tl, lambda t: t[2])
    return {k: reduce(step, v, {}).get(k) for k, v in by_key.items()}


# ----------------------------------------------------------------------------- recipient measures (pure)
def measures(ex: Mapping) -> dict:
    ix = ex.get("ix", {})
    l1, l2, l3, l25 = (ix.get(k) or 0.0 for k in ("l1", "l2", "l3", "l25"))
    p1 = ex.get("part1", ())
    act = tuple((activity_of(g.get("TypeOfActivitiesConductedTxt")), region_of(g.get("RegionTxt")),
                 num(g.get("RegionTotalExpendituresAmt")) or 0.0) for g in p1)
    noninv = tuple(a for a in act if a[0] != "investments")
    p1_noninv = sum(a[2] for a in noninv)
    p23 = tuple((region_of(g.get("RegionTxt")), amt(g)) for p in ("part2", "part3") for g in ex.get(p, ()))
    grants = l1 + l2 + l3
    foreign_exp = min(l25, max(l3, p1_noninv)) if l25 > 0 else 0.0
    reg_src = tuple((r, v) for _, r, v in noninv) if p1_noninv > 0 else p23
    reg_tot = sum(v for _, v in reg_src)
    regions = {r: sum(v for _, v in g) / reg_tot for r, g in _group_by_fast(reg_src, lambda t: t[0]).items()} if reg_tot else {}
    sf = ex.get("sf", {})
    return {"l1": l1, "l2": l2, "l3": l3, "l25": l25, "grants": grants,
            "sched_f": int(bool(sf.get("present"))), "p1_total": sum(a[2] for a in act), "p1_noninv": p1_noninv,
            "p1_grantmaking": sum(a[2] for a in act if a[0] == "grantmaking"),
            "p1_investments": sum(a[2] for a in act if a[0] == "investments"),
            "p1_spent_reported": num(sf.get("TotalSpentAmt")) or 0.0, "p2_p3": sum(v for _, v in p23),
            "foreign_exp": foreign_exp,
            "expense": foreign_exp / l25 if l25 > 0 else None,
            "l3_of_exp": min(1.0, l3 / l25) if l25 > 0 else None,
            "grant_mix": l3 / grants if grants > 0 else (0.0 if l25 > 0 else None),
            "regions": regions, "region_basis": "part1_noninv" if p1_noninv > 0 else ("part2_3" if reg_tot else "none")}


def share_for(meas: Mapping, fy: int, method: str) -> tuple:
    """-> (share, basis) for FY `fy`, borrowing the other FY when the return or the ratio is missing."""
    own = meas.get(fy)
    if own and own.get(method) is not None:
        return own[method], "same_fy"
    other = next((meas[f] for f in FYS if f != fy and meas.get(f) and meas[f].get(method) is not None), None)
    return (other[method], "other_fy") if other else (None, "none")


def estimate(rec: Mapping, meas: Mapping) -> dict:
    """Per recipient: inbound, abroad by method and FY, region dollars (central method)."""
    out = {}
    for m in METHODS:
        for fy in FYS:
            s, b = share_for(meas, fy, m)
            out[f"{m}_share_fy{fy}"] = s
            out[f"{m}_basis_fy{fy}"] = b
            out[f"abroad_{m}_fy{fy}"] = rec["si"].get(fy, 0.0) * s if s is not None else None
            out[f"abroad_{m}_dw_fy{fy}"] = rec["dw"].get(fy, 0.0) * s if s is not None else None
    regions = {}
    for fy in FYS:
        src = meas.get(fy) if meas.get(fy) and meas[fy]["regions"] else next(
            (meas[f] for f in FYS if meas.get(f) and meas[f]["regions"]), None)
        a = out[f"abroad_expense_fy{fy}"] or 0.0
        regions = reduce(lambda acc, kv: {**acc, kv[0]: acc.get(kv[0], 0.0) + a * kv[1]},
                         (src["regions"].items() if src else (("(no region rows)", 1.0),)) if a else (), regions)
    return {**out, "regions": regions}


# ----------------------------------------------------------------------------- rows (pure)
def fsum(xs) -> float:
    return sum(x for x in xs if x is not None)


def recipient_row(rank_: int, key: str, rec: Mapping, filings: Mapping, meas: Mapping, est: Mapping, bmf: Mapping) -> dict:
    b = bmf.get(rec["ein"], {})
    si = fsum(rec["si"].get(fy) for fy in FYS)
    ab = {m: fsum(est[f"abroad_{m}_fy{fy}"] for fy in FYS) for m in METHODS}
    m24, m23 = meas.get(2024) or {}, meas.get(2023) or {}
    pooled = lambda k: fsum(x.get(k) for x in (m23, m24))  # noqa: E731
    return {"row_type": "recipient", "scope": rec["name"], "rank": rank_, "ein": rec["ein"],
            "bmf_name": b.get("bmf_name", ""), "ntee_cd": b.get("ntee", ""), "selection_basis": rec["basis"],
            "named_intermediary": int(rec["ein"] in INTERMEDIARIES), "grantors": len(rec["grantors"]),
            "inbound_fy2023_usd": round(rec["si"].get(2023, 0.0)), "inbound_fy2024_usd": round(rec["si"].get(2024, 0.0)),
            "inbound_usd": round(si), "inbound_daf_weighted_usd": round(fsum(rec["dw"].values())),
            "object_id_fy2023": filings.get(2023, {}).get("oid", ""), "object_id_fy2024": filings.get(2024, {}).get("oid", ""),
            "tax_period_fy2023": filings.get(2023, {}).get("tax_period", ""),
            "tax_period_fy2024": filings.get(2024, {}).get("tax_period", ""),
            "return_status": ";".join(f"{fy}:{(meas.get(fy) or {}).get('_status', 'no_filing')}" for fy in FYS),
            "part_ix_l1_usd": round(pooled("l1")), "part_ix_l2_usd": round(pooled("l2")),
            "part_ix_l3_foreign_usd": round(pooled("l3")), "part_ix_l25_total_expenses_usd": round(pooled("l25")),
            "sched_f_present": "".join(str((meas.get(fy) or {}).get("sched_f", "-")) for fy in FYS),
            "sched_f_part1_total_usd": round(pooled("p1_total")), "sched_f_part1_noninv_usd": round(pooled("p1_noninv")),
            "sched_f_part1_grantmaking_usd": round(pooled("p1_grantmaking")),
            "sched_f_part1_investments_usd": round(pooled("p1_investments")),
            "sched_f_part1_spent_reported_usd": round(pooled("p1_spent_reported")),
            "sched_f_part2_3_usd": round(pooled("p2_p3")),
            "foreign_expense_usd": round(pooled("foreign_exp")),
            "grant_mix_share": pooled("l3") / pooled("grants") if pooled("grants") else None,
            "l3_of_exp_share": pooled("l3") / pooled("l25") if pooled("l25") else None,
            "expense_share": pooled("foreign_exp") / pooled("l25") if pooled("l25") else None,
            "share_basis": ";".join(f"{fy}:{est[f'expense_basis_fy{fy}']}" for fy in FYS),
            "region_basis": ";".join(f"{fy}:{(meas.get(fy) or {}).get('region_basis', 'none')}" for fy in FYS),
            **{f"abroad_{m}_usd": round(ab[m]) for m in METHODS},
            "abroad_expense_daf_weighted_usd": round(fsum(est[f"abroad_expense_dw_fy{fy}"] for fy in FYS)),
            "abroad_expense_fy2023_usd": round(est["abroad_expense_fy2023"] or 0),
            "abroad_expense_fy2024_usd": round(est["abroad_expense_fy2024"] or 0),
            "abroad_share_of_inbound": ab["expense"] / si if si else None,
            "top_region": max(est["regions"].items(), key=lambda kv: kv[1])[0] if est["regions"] else "",
            "source": SOURCE}


def summary_row(scope: str, rows: Sequence[Mapping], **kw) -> dict:
    s = lambda k: sum(r[k] or 0 for r in rows)  # noqa: E731
    inb = s("inbound_usd")
    return {"row_type": "summary", "scope": scope, "recipients": len(rows), "inbound_usd": round(inb),
            "inbound_fy2023_usd": s("inbound_fy2023_usd"), "inbound_fy2024_usd": s("inbound_fy2024_usd"),
            "inbound_daf_weighted_usd": s("inbound_daf_weighted_usd"),
            **{f"abroad_{m}_usd": s(f"abroad_{m}_usd") for m in METHODS},
            "abroad_expense_fy2023_usd": s("abroad_expense_fy2023_usd"), "abroad_expense_fy2024_usd": s("abroad_expense_fy2024_usd"),
            "abroad_expense_daf_weighted_usd": s("abroad_expense_daf_weighted_usd"),
            "abroad_share_of_inbound": s("abroad_expense_usd") / inb if inb else None,
            "l3_of_exp_share": s("abroad_l3_of_exp_usd") / inb if inb else None,
            "grant_mix_share": s("abroad_grant_mix_usd") / inb if inb else None,
            **kw, "source": SOURCE}


def region_rows(scope: str, ests: Sequence[Mapping]) -> list:
    tot = reduce(lambda acc, e: reduce(lambda a, kv: {**a, kv[0]: a.get(kv[0], 0.0) + kv[1]}, e["regions"].items(), acc), ests, {})
    t = sum(tot.values())
    return [{"row_type": "region", "scope": scope, "category": r, "abroad_expense_usd": round(v),
             "region_share": v / t if t else None, "source": SOURCE}
            for r, v in sorted(tot.items(), key=lambda kv: -kv[1])]


def group_rows(row_type: str, rows: Sequence[Mapping], keyf) -> list:
    return [summary_row(k, v, row_type_detail=row_type) for k, v in
            sorted(_group_by_fast(rows, keyf).items(), key=lambda kv: -sum(r["inbound_usd"] for r in kv[1]))]


def sponsor_rows(top: Sequence[tuple], ests: Mapping, panel: Mapping, rank: Mapping, direct: Mapping) -> list:
    """Indirect (via the top-150) vs direct foreign dollars per sponsor, FY2023-24 pooled, central method."""
    flat = tuple((sp, fy, a * (ests[k][f"expense_share_fy{fy}"] or 0.0), a)
                 for k, rec in top for (sp, fy), a in rec["by_sponsor"].items())
    by = _group_by_fast(flat, lambda t: t[0])
    return [{"row_type": "sponsor", "scope": panel[sp]["name"], "ein": sp, "rank": rank[sp], "segment": panel[sp]["segment"],
             "inbound_usd": round(sum(t[3] for t in v)), "abroad_expense_usd": round(sum(t[2] for t in v)),
             "direct_l3_usd": round(direct.get(sp, 0.0)),
             "indirect_to_direct_ratio": sum(t[2] for t in v) / direct[sp] if direct.get(sp) else None,
             "source": SOURCE}
            for sp, v in sorted(by.items(), key=lambda kv: -sum(t[2] for t in kv[1]))]


FIELDS = ("row_type", "row_type_detail", "scope", "rank", "ein", "bmf_name", "ntee_cd", "segment", "selection_basis",
          "named_intermediary", "grantors", "recipients", "category", "inbound_fy2023_usd", "inbound_fy2024_usd",
          "inbound_usd", "inbound_daf_weighted_usd", "object_id_fy2023", "object_id_fy2024", "tax_period_fy2023",
          "tax_period_fy2024", "return_status", "part_ix_l1_usd", "part_ix_l2_usd", "part_ix_l3_foreign_usd",
          "part_ix_l25_total_expenses_usd", "sched_f_present", "sched_f_part1_total_usd", "sched_f_part1_noninv_usd",
          "sched_f_part1_grantmaking_usd", "sched_f_part1_investments_usd", "sched_f_part1_spent_reported_usd",
          "sched_f_part2_3_usd", "foreign_expense_usd", "grant_mix_share", "l3_of_exp_share", "expense_share",
          "share_basis", "region_basis", "abroad_expense_usd", "abroad_l3_of_exp_usd", "abroad_grant_mix_usd",
          "abroad_expense_daf_weighted_usd", "abroad_expense_fy2023_usd", "abroad_expense_fy2024_usd",
          "abroad_share_of_inbound", "top_region", "region_share", "direct_l3_usd", "indirect_to_direct_ratio",
          "denominator_usd", "share_of_denominator", "note", "source")


def compare_rows(direct_tot: Mapping, est150: float, est_ext: Mapping, caf: float, net_si_mine: float) -> list:
    """Combined international share on the two bases used by P-NEW-FGN-01 [C]; extrapolations [I]."""
    l3, tg = float(direct_tot["part_ix_l3_foreign_usd"]), float(direct_tot["total_grants_usd"])
    l3i, nsi = float(direct_tot["itemising_part_ix_l3_foreign_usd"]), float(direct_tot["sched_i_net_usd"])
    rows = (("direct_line3", l3, tg, "Part IX line 3 / lines 1-3, main scope [F/C]"),
            ("direct_plus_top150", l3 + est150, tg, "line 3 + top-150 central estimate, on lines 1-3 [C]"),
            ("direct_plus_top150_plus_other_named", l3 + est150 + caf, tg,
             "adds P-NEW-FGN-01 pass-through of named intermediaries outside the Q/friends set (CAF America, "
             "Global Greengrants, Global Fund for Children) [C/I]"),
            ("direct_plus_all_targets_avg_share", l3 + est150 + est_ext["avg"], tg,
             "[I] remaining Q/friends inbound x top-150 dollar-weighted share"),
            ("direct_plus_all_targets_tail_share", l3 + est150 + est_ext["tail"], tg,
             "[I] remaining Q/friends inbound x share of ranks 101-150"),
            ("direct_line3_itemising", l3i, nsi + l3i, "line 3 / (net Schedule I + line 3), itemising [C]"),
            ("direct_plus_top150_itemising", l3i + est150, nsi + l3i, "same base, + top-150 central estimate [C]"),
            ("direct_plus_all_targets_avg_share_itemising", l3i + est150 + est_ext["avg"], nsi + l3i, "[I] same base"),
            ("this_run_net_sched_i", net_si_mine, nsi, "net Schedule I after totals-row drop vs P-NEW-FGN-01 net [C]"))
    return [{"row_type": "comparison", "scope": n, "abroad_expense_usd": round(a), "denominator_usd": round(d),
             "share_of_denominator": a / d if d else None, "note": note, "source": SOURCE} for n, a, d, note in rows]


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--extract-cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--top", type=int, default=150)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    present = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in present.items() if itemized(x) and panel[k[0]]["segment"] != "university_hospital"}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0].strip("0"))
    bmf = load_bmf(a.bmf_dir, eins)
    ann = {k: annotate(k[0], v["lines"], bmf, wl_eins, wl_names) for k, v in good.items()}
    net_si = sum(r["amount"] for rs in ann.values() for r in rs if not r["d2d"])

    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    weights = {k: min(1.0, max(0.0, share[k])) for k in ann if share.get(k) is not None}

    tl = target_lines(ann, bmf)
    recs = inbound(tl, weights)
    with_ein = {k: v for k, v in recs.items() if v["ein"]}
    ranked = sorted(with_ein.items(), key=lambda kv: (-sum(kv[1]["si"].values()), kv[0]))
    top = tuple(ranked[:a.top])
    rest = tuple(ranked[a.top:])
    no_ein = {k: v for k, v in recs.items() if not v["ein"]}

    idx = load_index(a.index_dir, frozenset(v["ein"] for _, v in top))
    filings = {k: choose_filings(idx.get(v["ein"], ())) for k, v in top}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values() if f["return_type"] == "990"})
    ex = load_all(oids, a.extract_cache, {}, a.fetch, a.workers)
    meas = {k: {fy: ({**measures(ex[f["oid"]]), "_status": "ok"} if f["return_type"] == "990" and ex.get(f["oid"], {}).get("status") == "ok"
                     else {"_status": f["return_type"] if f["return_type"] != "990" else ex.get(f["oid"], {}).get("status", "missing")})
                for fy, f in fs.items()} for k, fs in filings.items()}
    meas_ok = {k: {fy: {**m, "_name": f"{dict(top)[k]['name']} FY{fy}"} for fy, m in v.items() if m["_status"] == "ok"}
               for k, v in meas.items()}
    filer_mismatch = sorted(f"{v['name']} {o}" for k, v in top for fy, f in filings[k].items()
                            for o in (f["oid"],) if ex.get(o, {}).get("status") == "ok" and ex[o].get("filer_ein") != v["ein"])
    ests = {k: estimate(v, meas_ok[k]) for k, v in top}
    rrows = [{**recipient_row(i + 1, k, v, filings[k], {**meas_ok[k], **{fy: {**(meas_ok[k].get(fy) or {}), "_status": m["_status"]}
                                                                           for fy, m in meas[k].items()}}, ests[k], bmf)}
             for i, (k, v) in enumerate(top)]

    parsed = [r for r in rrows if r["expense_share"] is not None]
    unparsed = [r for r in rrows if r["expense_share"] is None]
    est150 = sum(r["abroad_expense_usd"] for r in rrows)
    inb_parsed = sum(r["inbound_usd"] for r in parsed)
    tail = [r for r in parsed if r["rank"] > 100]
    tail_share = sum(r["abroad_expense_usd"] for r in tail) / sum(r["inbound_usd"] for r in tail)
    avg_share = est150 / inb_parsed
    no_ein_inb = sum(sum(v["si"].values()) for v in no_ein.values())
    rest_inb = sum(sum(v["si"].values()) for _, v in rest) + no_ein_inb
    unparsed_inb = sum(r["inbound_usd"] for r in unparsed)
    est_ext = {"avg": (rest_inb + unparsed_inb) * avg_share, "tail": rest_inb * tail_share + unparsed_inb * avg_share}
    checks = [m for k in meas_ok for m in meas_ok[k].values()]
    xcheck = {"recipient_years_parsed": len(checks),
              "with_sched_f": sum(1 for m in checks if m["sched_f"]),
              "line3_positive": sum(1 for m in checks if m["l3"] > 0),
              "part2_3_within_5pct_or_0.5m_of_line3": sum(1 for m in checks if m["l3"] > 0 and abs(m["p2_p3"] - m["l3"]) <= max(5e5, 0.05 * m["l3"])),
              "part1_grantmaking_ge_95pct_line3": sum(1 for m in checks if m["l3"] > 0 and m["p1_grantmaking"] >= 0.95 * m["l3"]),
              "part1_noninv_ge_line3": sum(1 for m in checks if m["l3"] > 0 and m["p1_noninv"] >= m["l3"] - 1),
              "part1_noninv_below_95pct_line3": sorted(f"{m.get('_name', '')}" for m in checks if m["l3"] > 0 and m["p1_noninv"] < 0.95 * m["l3"]),
              "part1_rows_sum_eq_total_spent": sum(1 for m in checks if m["sched_f"] and abs(m["p1_total"] - m["p1_spent_reported"]) < 1),
              "part1_investments_usd": round(sum(m["p1_investments"] for m in checks)),
              "foreign_exp_from_part1": sum(1 for m in checks if m["p1_noninv"] > m["l3"]),
              "foreign_exp_capped_at_l25": sum(1 for m in checks if m["l25"] > 0 and max(m["l3"], m["p1_noninv"]) > m["l25"])}

    sf = read_csv(SCHED_F_CSV)
    direct_tot = next(r for r in sf if r["row_type"] == "scope_total" and r["scope"] == MAIN and r["fiscal_year"] == "2023-2024")
    inter_pt = {ein9(r["ein"]): float(r["est_foreign_pass_through_usd"] or 0) for r in sf
                if r["row_type"] == "intermediary" and r["fiscal_year"] == "2023-2024"}
    top_eins = frozenset(v["ein"] for _, v in top) | frozenset(v["ein"] for _, v in rest)
    outside = {e: v for e, v in inter_pt.items() if e not in top_eins}  # named intermediaries outside the Q/friends set
    caf = sum(outside.values())
    direct_reg = {r["category"]: float(r["amount_usd"]) for r in sf if r["row_type"] == "region_part2"
                  and r["scope"] == MAIN and r["fiscal_year"] == "2023-2024"}
    direct_sp = reduce(lambda acc, r: {**acc, ein9(r["ein"]): acc.get(ein9(r["ein"]), 0.0) + float(r["part_ix_l3_foreign_usd"] or 0)},
                       (r for r in sf if r["row_type"] == "sponsor_year"), {})

    all_targets_row = {"row_type": "summary", "scope": "all_q_or_friends_targets_net", "recipients": len(recs),
                       "inbound_usd": round(sum(sum(v["si"].values()) for v in recs.values())),
                       "inbound_fy2023_usd": round(sum(v["si"].get(2023, 0.0) for v in recs.values())),
                       "inbound_fy2024_usd": round(sum(v["si"].get(2024, 0.0) for v in recs.values())),
                       "note": f"outside top {a.top}: {round(rest_inb)} USD incl. {round(no_ein_inb)} on blank-EIN lines; top-{a.top} "
                               f"recipients with no Form 990: {round(unparsed_inb)} USD; [I] extrapolated abroad for both: "
                               f"avg-share {round(est_ext['avg'])} (share {avg_share:.4f}), tail-share {round(est_ext['tail'])} "
                               f"(ranks 101-{a.top} share {tail_share:.4f})",
                       "source": SOURCE}
    summ = ([summary_row(f"top{a.top}", rrows), summary_row(f"top{a.top}_with_form990", parsed),
             summary_row(f"top{a.top}_no_form990", unparsed), all_targets_row]
            + group_rows("selection_basis", rrows, lambda r: r["selection_basis"])
            + group_rows("ntee_subgroup", rrows, lambda r: (r["ntee_cd"][:3] or "(none)"))
            + group_rows("named_intermediary", rrows, lambda r: "named_intermediary" if r["named_intermediary"] else "other")
            + group_rows("share_band", rrows, lambda r: ("unparsed" if r["expense_share"] is None else
                                                         "a_<10%" if r["expense_share"] < 0.10 else
                                                         "b_10-50%" if r["expense_share"] < 0.5 else
                                                         "c_50-90%" if r["expense_share"] < 0.9 else "d_>=90%")))
    reg = region_rows(f"top{a.top}", list(ests.values()))
    ind_reg = {r["category"]: r["abroad_expense_usd"] for r in reg}
    comb = {k: direct_reg.get(k, 0.0) + ind_reg.get(k, 0.0) for k in set(direct_reg) | set(ind_reg)}
    ctot = sum(comb.values())
    reg = reg + [{"row_type": "region_combined", "scope": f"direct_part2_plus_top{a.top}", "category": k,
                  "abroad_expense_usd": round(v), "region_share": v / ctot if ctot else None,
                  "direct_l3_usd": round(direct_reg.get(k, 0.0)), "source": SOURCE}
                 for k, v in sorted(comb.items(), key=lambda kv: -kv[1])]
    sp = sponsor_rows(top, ests, panel, rank, direct_sp)
    comp = compare_rows(direct_tot, est150, est_ext, caf, net_si)
    write_csv(a.out, summ + comp + reg + sp + rrows, FIELDS)

    slim = lambda r, ks: {k: (round(r[k], 4) if isinstance(r.get(k), float) else r.get(k)) for k in ks}  # noqa: E731
    print(json.dumps({
        "sponsor_years_itemising_main": len(good), "net_sched_i_usd": round(net_si),
        "targets": len(recs), "targets_with_ein": len(with_ein), "top_n": len(top),
        "filings": {s: sum(1 for k in meas for m in meas[k].values() if m["_status"] == s)
                    for s in sorted({m["_status"] for k in meas for m in meas[k].values()})},
        "recipients_without_any_990": [v["name"] for k, v in top if not meas_ok[k]],
        "filer_mismatch": filer_mismatch, "cross_checks": xcheck,
        "extrapolation": {"rest_inbound": round(rest_inb), "no_ein_inbound": round(no_ein_inb), "unparsed_inbound": round(unparsed_inb),
                          "avg_share": avg_share, "tail_share": tail_share, **{k: round(v) for k, v in est_ext.items()}},
        "summary": [slim(r, ("scope", "row_type_detail", "recipients", "inbound_usd", "abroad_expense_usd", "abroad_share_of_inbound",
                             "abroad_l3_of_exp_usd", "abroad_grant_mix_usd", "abroad_expense_daf_weighted_usd",
                             "inbound_daf_weighted_usd", "abroad_expense_fy2023_usd", "abroad_expense_fy2024_usd",
                             "inbound_fy2023_usd", "inbound_fy2024_usd", "note")) for r in summ],
        "comparison": [slim(r, ("scope", "abroad_expense_usd", "denominator_usd", "share_of_denominator")) for r in comp],
        "regions": [slim(r, ("row_type", "category", "abroad_expense_usd", "region_share", "direct_l3_usd")) for r in reg],
        "named_outside_target_set": {e: round(v) for e, v in outside.items()},
        "sponsors": [slim(r, ("scope", "inbound_usd", "abroad_expense_usd", "direct_l3_usd", "indirect_to_direct_ratio")) for r in sp[:12]],
        "recipients": [slim(r, ("rank", "scope", "ntee_cd", "selection_basis", "inbound_usd", "expense_share", "grant_mix_share",
                                "l3_of_exp_share", "abroad_expense_usd", "share_basis", "sched_f_present", "top_region",
                                "part_ix_l3_foreign_usd", "sched_f_part1_noninv_usd", "sched_f_part2_3_usd",
                                "sched_f_part1_spent_reported_usd", "sched_f_part1_total_usd", "return_status")) for r in rrows],
    }, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
