#!/usr/bin/env python3
"""DAF money reaching abroad through large recipients outside the NTEE Q / friends-of frame, FY2023-FY2024 (P-B4531-01-03).

Runs the Schedule F Part I / Part IX line 3 parse of scripts/mission_daf_money_abroad.py (imported, not modified) on
the largest net Schedule I recipients of top-50 sponsors of ANY NTEE code, after removing the 150 Q/friends recipients
already counted there.

Steps (pure transforms; I/O only in `main` and the cached fetchers it calls)
  1. Lines     identical to mission_daf_money_abroad.main: top-50 DAFRC sponsors, one return per sponsor x FY,
               itemising sponsor-years, main scope (university/hospital sponsors out), totals rows dropped,
               DAF-to-DAF lines (batch-34 whitelist, self-lines) dropped.
  2. Frame     the Q/friends top 150 is rebuilt with the base script's own functions (target_lines, inbound, ranking)
               and checked EIN-for-EIN against the recipient rows of daf-money-abroad-2026-11-19.csv. Every other
               recipient with an EIN is ranked by pooled FY2023-24 net inbound; the largest --top (500) are kept.
  3. Groups    each of the 500 is put in exactly one group:
                 dafrc_sponsor   EIN (or unique normalised Schedule I / BMF name) is in the DAFRC sponsor panel (any
                                 segment): it holds DAFs itself, so some of its inbound may sit in a DAF before moving
                                 on. Reported separately, never in the headline.
                 q_friends_rest  Q or friends-of recipient ranked 151+ in the base frame. Measured here, and taken out
                                 of the base [I] extrapolation base so it is not counted twice.
                 non_q           everything else. This is the new money abroad.
  4. Returns   recipients' Form 990s (TEOS index, latest object id per tax period, FY = year the period ends), parsed
               with mission_foreign_grants.load_extract into the extract cache; shares by
               mission_daf_money_abroad.measures / estimate (central "expense", floor "l3_of_exp", high "grant_mix").
               Allocation of DAF dollars at each recipient-year's own foreign share is an assumption [I-alloc].
               Second DAF-sponsor test: the recipient's own Form 990 Part IV line 6 (DonorAdvisedFundInd), read
               from the same e-file XML into a small side cache (--daf-cache); non_q recipients answering Yes are
               flagged (own_daf_ind) and shown as a strict variant that drops them.
  5. Output    by NTEE major group (EO BMF NTEE_CD first letter), by region (Schedule F Part I, fallback Part II+III),
               NTEE major x region, combined regions (direct + top 150 + new), and the combined share of total grants
               with filed/measured parts and extrapolated [I-extrap] parts in separate rows.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_non_q_foreign.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --index-dir IRS --extract-cache EC --daf-cache DC [--fetch] [--workers 6] [--top 500]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_money_abroad import FIELDS as BASE_FIELDS  # noqa: E402
from mission_daf_money_abroad import METHODS, MAIN, SCHED_F_CSV, basis_of, estimate, inbound, measures  # noqa: E402
from mission_daf_money_abroad import OUT as BASE_CSV  # noqa: E402
from mission_daf_money_abroad import recipient_row, region_rows, sponsor_rows, summary_row, target_lines  # noqa: E402
from mission_daf_share_recipient_revenue import choose_filings, load_index  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_foreign_grants import INTERMEDIARIES, load_all  # noqa: E402
from mission_net_payout import itemized, name_map, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import COST, WHITELIST, annotate, load_bmf, load_lines  # noqa: E402

OUT = os.path.join(DATA, "non-q-foreign-spending-2026-11-19.csv")
SOURCE = ("Sponsors: IRS Form 990 Schedule I Part II lines (line cache of mission_recipient_sectors.py; DAF-to-DAF and "
          "totals rows dropped); recipients: IRS EO BMF NTEE_CD (2026-11 snapshot) and own Form 990 Part IX lines 1-3, 25 "
          "and Schedule F Parts I-III (e-file XML, GivingTuesday mirror of IRS TEOS; IRS TEOS index CSVs); frame and "
          "direct route from daf-money-abroad-2026-11-19.csv and daf-foreign-grants-schedule-f-2023-2024.csv")
# NCCS NTEE major groups (https://urbaninstitute.github.io/nccs-legacy/ntee/ntee.html).
NTEE_MAJOR = {"A": "Arts, Culture and Humanities", "B": "Education", "C": "Environment", "D": "Animal-Related",
              "E": "Health Care", "F": "Mental Health and Crisis Intervention", "G": "Diseases, Disorders, Medical Disciplines",
              "H": "Medical Research", "I": "Crime and Legal-Related", "J": "Employment", "K": "Food, Agriculture and Nutrition",
              "L": "Housing and Shelter", "M": "Public Safety, Disaster Preparedness and Relief", "N": "Recreation and Sports",
              "O": "Youth Development", "P": "Human Services", "Q": "International, Foreign Affairs and National Security",
              "R": "Civil Rights, Social Action and Advocacy", "S": "Community Improvement and Capacity Building",
              "T": "Philanthropy, Voluntarism and Grantmaking Foundations", "U": "Science and Technology",
              "V": "Social Science", "W": "Public and Societal Benefit", "X": "Religion-Related",
              "Y": "Mutual and Membership Benefit", "Z": "Unknown"}
GROUPS = ("non_q", "q_friends_rest", "dafrc_sponsor")
FIELDS = (BASE_FIELDS[:3] + ("group", "ntee_major", "ntee_major_name", "own_daf_ind", "cap_bound_fys",
                              "abroad_expense_cap_adj_usd", "evidence") + BASE_FIELDS[3:])


# ----------------------------------------------------------------------------- Part IV line 6 (I/O edge)
def parse_daf_ind(stream) -> dict:
    """Stream the return; stop at the end of IRS990. -> {'daf_ind': '1'/'0'/''}."""
    for _, el in ET.iterparse(stream, events=("end",)):
        tag_ = local(el.tag)
        if tag_ == "DonorAdvisedFundInd":
            return {"daf_ind": (el.text or "").strip().lower() in ("1", "true") and "1" or "0"}
        if tag_ == "IRS990":
            return {"daf_ind": ""}
        el.clear()
    return {"daf_ind": ""}


def load_daf_ind(oid: str, cache: str, fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    if not fetch:
        return {"daf_ind": "", "status": "not_fetched"}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                out = {**parse_daf_ind(resp), "status": "ok"}
            os.makedirs(cache, exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(out, fh)
            return out
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"daf_ind": "", "status": f"http_{e.code}"}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"daf_ind": "", "status": "error"}


# ----------------------------------------------------------------------------- frame (pure)
def all_lines(ann: Mapping, bmf: Mapping) -> tuple:
    """Every net (non DAF-to-DAF) line, basis 'q'/'friends'/'q+friends' or 'other'."""
    return tuple((k[0], k[1], r["key"], r["ein"], r["name"], r["amount"], basis_of(r, bmf) or "other")
                 for k, rs in ann.items() for r in rs if not r["d2d"])


def ranked(recs: Mapping) -> tuple:
    """Base-script ordering: EIN-bearing keys by pooled inbound desc, then key."""
    return tuple(sorted(((k, v) for k, v in recs.items() if v["ein"]), key=lambda kv: (-sum(kv[1]["si"].values()), kv[0])))


def in_panel(rec: Mapping, panel: Mapping, pnames: Mapping, bmf: Mapping) -> bool:
    names = (rec["name"], bmf.get(rec["ein"], {}).get("bmf_name", ""))
    return rec["ein"] in panel or any(norm_name(n) in pnames for n in names if n)


def group_of(rec: Mapping, panel: Mapping, pnames: Mapping, bmf: Mapping) -> str:
    return ("dafrc_sponsor" if in_panel(rec, panel, pnames, bmf) else
            "q_friends_rest" if rec["basis"] != "other" else "non_q")


def major_of(ein: str, bmf: Mapping, fallback: str) -> str:
    n = (bmf.get(ein, {}).get("ntee") or "")[:1]
    return n if n in NTEE_MAJOR else f"(no NTEE: {fallback})"


# ----------------------------------------------------------------------------- line-25 cap check (pure)
def capped(m: Mapping) -> bool:
    """Schedule F Part I non-investment rows (or line 3) exceed total expenses: the central share is capped at 100%."""
    return m["l25"] > 0 and max(m["l3"], m["p1_noninv"]) > m["l25"]


def src_for(meas: Mapping, fy: int) -> Mapping | None:
    """The recipient-year whose central share mission_daf_money_abroad.share_for uses (own FY, else the other)."""
    own = meas.get(fy)
    return own if own and own.get("expense") is not None else next(
        (meas[f] for f in FYS if f != fy and meas.get(f) and meas[f].get("expense") is not None), None)


def cap_adjusted(rec: Mapping, meas: Mapping) -> float:
    """Central estimate with every capped recipient-year at line 3 / line 25 instead (sensitivity)."""
    return sum(rec["si"].get(fy, 0.0) * (m["l3_of_exp"] if capped(m) else m["expense"])
               for fy in FYS for m in (src_for(meas, fy),) if m)


# ----------------------------------------------------------------------------- rows (pure)
def tag(rows: Sequence[Mapping], **kw) -> list:
    return [{**r, **kw} for r in rows]


def grouped(row_type: str, rows: Sequence[Mapping], keyf, **kw) -> list:
    return [{**summary_row(k, v, row_type_detail=row_type), **kw} for k, v in
            sorted(_group_by_fast(rows, keyf).items(), key=lambda kv: -sum(r["abroad_expense_usd"] for r in kv[1]))]


def region_by(rows: Sequence[Mapping], ests: Mapping, keyf, row_type: str, group: str) -> list:
    return [r for k, v in sorted(_group_by_fast(rows, keyf).items())
            for r in tag(region_rows(k, [ests[x["_key"]] for x in v]), row_type=row_type, group=group)]


def combine_regions(base_comb: Mapping, new: Sequence[Mapping]) -> list:
    """Base region_combined (direct Part II + top 150) plus the new non-Q central dollars."""
    nr = {r["category"]: float(r["abroad_expense_usd"]) for r in new}
    comb = {k: base_comb.get(k, 0.0) + nr.get(k, 0.0) for k in set(base_comb) | set(nr)}
    t = sum(comb.values())
    return [{"row_type": "region_combined", "scope": "direct_part2_plus_top150_plus_non_q", "category": k,
             "abroad_expense_usd": round(v), "region_share": v / t if t else None, "group": "non_q",
             "note": f"base direct+top150 {round(base_comb.get(k, 0.0))}; new non_q {round(nr.get(k, 0.0))}",
             "evidence": "F (direct) + I-alloc (pass-through)", "source": SOURCE}
            for k, v in sorted(comb.items(), key=lambda kv: -kv[1])]


def compare_rows(d: Mapping) -> list:
    """Combined share of total grants. Each row adds one component; [I-alloc] and [I-extrap] stay separate."""
    tg, base_i = d["lines_1_3"], d["net_si_plus_l3"]
    steps = (
        ("direct_line3", d["direct_l3"], "F", "sponsors' own Part IX line 3 (P-NEW-FGN-01)"),
        ("plus_top150_q_friends", d["top150"], "I-alloc", "base run central estimate (V wave 37A: $1.868bn)"),
        ("plus_non_q_measured", d["non_q"], "I-alloc", "new: non-Q recipients among the 500 with a Form 990"),
        ("plus_q_friends_rest_measured", d["qf_rest"], "I-alloc", "Q/friends ranks 151+ that fell in the 500"),
    )
    extrap = (
        ("plus_q_friends_remainder_extrap", d["qf_remainder_extrap"], "I-extrap",
         f"remaining Q/friends inbound {round(d['qf_remainder_inb'])} (base rest + top-150 no-990, less the "
         f"Q/friends recipients in the 500) x base top-150 share {d['avg_share']:.4f}"),
        ("plus_non_q_no990_extrap", d["non_q_no990_extrap"], "I-extrap",
         f"non-Q recipients in the 500 with no Form 990 ({round(d['non_q_no990_inb'])} inbound) x non-Q "
         f"dollar-weighted share {d['non_q_share']:.4f}"),
        ("plus_non_q_beyond_top_extrap", d["non_q_beyond_extrap"], "I-extrap",
         f"non-Q inbound beyond the 500 ({round(d['non_q_beyond_inb'])}) x share of the last 100 non-Q ranks "
         f"{d['non_q_tail_share']:.4f}"),
    )
    cum = lambda xs: reduce(lambda acc, s: acc + [(s, (acc[-1][1] if acc else 0.0) + s[1])], xs, [])  # noqa: E731
    meas = cum(steps)
    full = cum(steps + extrap)
    sens = (("sensitivity_plus_dafrc_sponsors", meas[-1][1] + d["sponsors"], "I-alloc",
             "measured total + the DAFRC-sponsor recipients in the 500 (excluded from the headline)"),
            ("sensitivity_non_q_capped_years_at_line3", meas[-1][1] - d["non_q"] + d["non_q_cap_adj"], "I-alloc",
             "measured total with non-Q recipient-years whose Part I or line 3 exceeds line 25 re-scored at line 3 / line 25"),
            ("sensitivity_strict_excl_own_daf_holders", meas[-1][1] - d["non_q_own_daf"], "I-alloc",
             "measured total less non-Q recipients whose own 990 Part IV line 6 says they maintain DAFs"))
    rows = [(f"cum_{s[0]}", v, s[2], s[3]) for s, v in full] + [(n, v, e, nt) for n, v, e, nt in sens]
    comp = [{"row_type": "comparison", "scope": n, "abroad_expense_usd": round(v), "denominator_usd": round(tg),
             "share_of_denominator": v / tg, "evidence": e, "note": nt + " | base: sponsors' Part IX lines 1-3",
             "source": SOURCE} for n, v, e, nt in rows]
    item = [{"row_type": "comparison", "scope": f"itemising_{n}", "abroad_expense_usd": round(v - d["direct_l3"] + d["direct_l3_item"]),
             "denominator_usd": round(base_i), "share_of_denominator": (v - d["direct_l3"] + d["direct_l3_item"]) / base_i,
             "evidence": e, "note": "base: itemising net Schedule I + line 3 (P-NEW-FGN-01)", "source": SOURCE}
            for n, v, e, _ in rows]
    parts = [{"row_type": "component", "scope": s[0], "abroad_expense_usd": round(s[1]), "denominator_usd": round(tg),
              "share_of_denominator": s[1] / tg, "evidence": s[2], "note": s[3], "source": SOURCE} for s in steps + extrap]
    return parts + comp + item


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--extract-cache", required=True)
    ap.add_argument("--daf-cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--top", type=int, default=500)
    ap.add_argument("--q-top", type=int, default=150)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    # 1. lines, exactly as mission_daf_money_abroad.main
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    pnames = name_map(panel)
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
    sector = {r["key"]: r["group"] for rs in ann.values() for r in rs}

    # 2. frame: rebuild the Q/friends top 150 and check it against the base CSV
    qf_rank = ranked(inbound(target_lines(ann, bmf), weights))
    q150 = frozenset(v["ein"] for _, v in qf_rank[:a.q_top])
    base = read_csv(BASE_CSV)
    base_eins = frozenset(ein9(r["ein"]) for r in base if r["row_type"] == "recipient")
    recs = inbound(all_lines(ann, bmf), weights)
    pool = tuple((k, v) for k, v in ranked(recs) if v["ein"] not in q150 | base_eins)
    top = pool[:a.top]
    beyond = pool[a.top:]
    no_ein_inb = sum(sum(v["si"].values()) for v in recs.values() if not v["ein"] and v["basis"] == "other")

    # 4. returns and shares
    idx = load_index(a.index_dir, frozenset(v["ein"] for _, v in top))
    filings = {k: choose_filings(idx.get(v["ein"], ())) for k, v in top}
    oids = sorted({f["oid"] for fs in filings.values() for f in fs.values() if f["return_type"] == "990"})
    ex = load_all(oids, a.extract_cache, {}, a.fetch, a.workers)
    meas = {k: {fy: ({**measures(ex[f["oid"]]), "_status": "ok"} if f["return_type"] == "990" and ex.get(f["oid"], {}).get("status") == "ok"
                     else {"_status": f["return_type"] if f["return_type"] != "990" else ex.get(f["oid"], {}).get("status", "missing")})
                for fy, f in fs.items()} for k, fs in filings.items()}
    meas_ok = {k: {fy: m for fy, m in v.items() if m["_status"] == "ok"} for k, v in meas.items()}
    filer_mismatch = sorted(f"{v['name']} {f['oid']}" for k, v in top for f in filings[k].values()
                            if ex.get(f["oid"], {}).get("status") == "ok" and ex[f["oid"]].get("filer_ein") != v["ein"])
    ests = {k: estimate(v, meas_ok[k]) for k, v in top}
    with cf.ThreadPoolExecutor(max_workers=a.workers) as pool_:
        dind = dict(zip(oids, pool_.map(lambda o: load_daf_ind(o, a.daf_cache, a.fetch), oids)))
    own_daf = {k: ("1" if any(dind.get(f["oid"], {}).get("daf_ind") == "1" for f in fs.values()) else
                   "0" if any(dind.get(f["oid"], {}).get("daf_ind") == "0" for f in fs.values()) else "")
               for k, fs in filings.items()}
    seg = lambda v: panel.get(v["ein"], panel.get(next((pnames[norm_name(n)] for n in (v["name"], bmf.get(v["ein"], {}).get("bmf_name", ""))  # noqa: E731
                                                       if n and norm_name(n) in pnames), ""), {})).get("segment", "")
    rrows = [{**recipient_row(i + 1, k, v, filings[k], {**meas_ok[k], **{fy: {**(meas_ok[k].get(fy) or {}), "_status": m["_status"]}
                                                                          for fy, m in meas[k].items()}}, ests[k], bmf),
              "group": group_of(v, panel, pnames, bmf), "segment": seg(v), "own_daf_ind": own_daf[k],
              "cap_bound_fys": ";".join(str(fy) for fy in FYS if meas_ok[k].get(fy) and capped(meas_ok[k][fy])),
              "abroad_expense_cap_adj_usd": round(cap_adjusted(v, meas_ok[k])),
              "ntee_major": major_of(v["ein"], bmf, sector.get(k, "")),
              "ntee_major_name": NTEE_MAJOR.get(major_of(v["ein"], bmf, ""), ""),
              "evidence": "F (inbound, Part IX, Sched F) / I-alloc (abroad_*)", "_key": k}
             for i, (k, v) in enumerate(top)]
    by_g = {g: [r for r in rrows if r["group"] == g] for g in GROUPS}
    parsed = lambda rs: [r for r in rs if r["expense_share"] is not None]  # noqa: E731
    s = lambda rs, f: sum(r[f] or 0 for r in rs)  # noqa: E731

    # base figures read from the base CSV and the direct-route CSV (not recomputed)
    bsum = {r["scope"]: r for r in base if r["row_type"] == "summary" and not r["row_type_detail"]}
    top150_ab = float(bsum["top150"]["abroad_expense_usd"])
    avg_share = top150_ab / float(bsum["top150_with_form990"]["inbound_usd"])
    qf_rest_inb = float(bsum["all_q_or_friends_targets_net"]["inbound_usd"]) - float(bsum["top150"]["inbound_usd"])
    top150_no990 = float(bsum["top150_no_form990"]["inbound_usd"])
    base_comb = {r["category"]: float(r["abroad_expense_usd"]) for r in base if r["row_type"] == "region_combined"}
    sf = read_csv(SCHED_F_CSV)
    dt = next(r for r in sf if r["row_type"] == "scope_total" and r["scope"] == MAIN and r["fiscal_year"] == "2023-2024")
    direct_sp = reduce(lambda acc, r: {**acc, ein9(r["ein"]): acc.get(ein9(r["ein"]), 0.0) + float(r["part_ix_l3_foreign_usd"] or 0)},
                       (r for r in sf if r["row_type"] == "sponsor_year"), {})

    nq, nq_p = by_g["non_q"], parsed(by_g["non_q"])
    div = lambda n, m: n / m if m else 0.0  # noqa: E731
    nq_share = div(s(nq_p, "abroad_expense_usd"), s(nq_p, "inbound_usd"))
    nq_tail = nq_p[-100:]
    nq_tail_share = div(s(nq_tail, "abroad_expense_usd"), s(nq_tail, "inbound_usd"))
    beyond_nonq = tuple(v for _, v in beyond if group_of(v, panel, pnames, bmf) == "non_q")
    beyond_nonq_inb = sum(sum(v["si"].values()) for v in beyond_nonq) + no_ein_inb
    qf_in_500_inb = s(by_g["q_friends_rest"], "inbound_usd") + s([r for r in by_g["dafrc_sponsor"] if r["selection_basis"] != "other"], "inbound_usd")
    qf_rem_inb = qf_rest_inb + top150_no990 - qf_in_500_inb
    nq_no990_inb = s([r for r in nq if r["expense_share"] is None], "inbound_usd")
    qf_no990_inb = s([r for r in by_g["q_friends_rest"] if r["expense_share"] is None], "inbound_usd")
    d = {"lines_1_3": float(dt["total_grants_usd"]), "net_si_plus_l3": float(dt["sched_i_net_usd"]) + float(dt["itemising_part_ix_l3_foreign_usd"]),
         "direct_l3": float(dt["part_ix_l3_foreign_usd"]), "direct_l3_item": float(dt["itemising_part_ix_l3_foreign_usd"]),
         "top150": top150_ab, "non_q": s(nq, "abroad_expense_usd"), "qf_rest": s(by_g["q_friends_rest"], "abroad_expense_usd"),
         "sponsors": s(by_g["dafrc_sponsor"], "abroad_expense_usd"),
         "non_q_own_daf": s([r for r in nq if r["own_daf_ind"] == "1"], "abroad_expense_usd"),
         "non_q_cap_adj": s(nq, "abroad_expense_cap_adj_usd"),
         "avg_share": avg_share, "qf_remainder_inb": qf_rem_inb + qf_no990_inb,
         "qf_remainder_extrap": (qf_rem_inb + qf_no990_inb) * avg_share,
         "non_q_share": nq_share, "non_q_no990_inb": nq_no990_inb, "non_q_no990_extrap": nq_no990_inb * nq_share,
         "non_q_tail_share": nq_tail_share, "non_q_beyond_inb": beyond_nonq_inb,
         "non_q_beyond_extrap": beyond_nonq_inb * nq_tail_share}

    summ = ([{**summary_row(f"top{a.top}_all_groups", rrows), "group": "all"}]
            + [{**summary_row(g, rs), "group": g} for g, rs in by_g.items()]
            + [{**summary_row(f"{g}_with_form990", parsed(rs)), "group": g} for g, rs in by_g.items()]
            + [{**summary_row("non_q_own_part_iv_l6_yes", [r for r in nq if r["own_daf_ind"] == "1"]), "group": "non_q"},
               {**summary_row("non_q_excl_own_part_iv_l6_yes", [r for r in nq if r["own_daf_ind"] != "1"]), "group": "non_q"}]
            + grouped("ntee_major", nq, lambda r: r["ntee_major"], group="non_q")
            + grouped("ntee_subgroup", nq, lambda r: r["ntee_cd"][:3] or "(none)", group="non_q")
            + grouped("dafrc_segment", by_g["dafrc_sponsor"], lambda r: r["segment"], group="dafrc_sponsor")
            + grouped("ntee_major", by_g["q_friends_rest"], lambda r: r["ntee_major"], group="q_friends_rest")
            + grouped("share_band", nq, lambda r: ("unparsed" if r["expense_share"] is None else
                                                   "a_<10%" if r["expense_share"] < 0.10 else "b_10-50%" if r["expense_share"] < 0.5 else
                                                   "c_50-90%" if r["expense_share"] < 0.9 else "d_>=90%"), group="non_q"))
    reg = (tag(region_rows("non_q", [ests[r["_key"]] for r in nq]), group="non_q", evidence="I-alloc")
           + tag(region_rows("q_friends_rest", [ests[r["_key"]] for r in by_g["q_friends_rest"]]), group="q_friends_rest", evidence="I-alloc")
           + tag(region_rows("dafrc_sponsor", [ests[r["_key"]] for r in by_g["dafrc_sponsor"]]), group="dafrc_sponsor", evidence="I-alloc")
           + region_by(nq, ests, lambda r: r["ntee_major"], "region_by_ntee", "non_q"))
    comb = combine_regions(base_comb, [r for r in reg if r["row_type"] == "region" and r["group"] == "non_q"])
    comp = compare_rows(d)
    sp = tag(sponsor_rows(tuple((k, v) for k, v in top if group_of(v, panel, pnames, bmf) == "non_q"), ests, panel, rank, direct_sp), group="non_q")
    out_rows = [{k: v for k, v in r.items() if k != "_key"} for r in summ + comp + reg + comb + sp + rrows]
    write_csv(a.out, out_rows, FIELDS)

    slim = lambda r, ks: {k: (round(r[k], 4) if isinstance(r.get(k), float) else r.get(k)) for k in ks}  # noqa: E731
    print(json.dumps({
        "sponsor_years_itemising_main": len(good), "net_sched_i_usd": round(net_si),
        "frame_check": {"rebuilt_q150_eq_base_csv": q150 == base_eins, "rebuilt_minus_base": sorted(q150 - base_eins),
                        "base_minus_rebuilt": sorted(base_eins - q150)},
        "recipient_keys": len(recs), "pool_with_ein_outside_q150": len(pool), "top_n": len(top),
        "rank_cutoff_inbound_usd": round(sum(top[-1][1]["si"].values())) if top else None,
        "top_inbound_usd": round(sum(sum(v["si"].values()) for _, v in top)),
        "beyond_inbound_usd": round(sum(sum(v["si"].values()) for _, v in beyond)), "no_ein_inbound_usd": round(no_ein_inb),
        "groups": {g: len(rs) for g, rs in by_g.items()},
        "named_intermediaries": {nm: next(({"pool_rank": i + 1, "inbound_usd": round(sum(v["si"].values())),
                                            "group": group_of(v, panel, pnames, bmf)} for i, (_, v) in enumerate(pool) if v["ein"] == e),
                                          "in Q/friends top 150" if e in q150 else "not a net recipient (DAF-to-DAF whitelist or no lines)")
                                 for e, nm in INTERMEDIARIES.items()},
        "filings": {st: sum(1 for k in meas for m in meas[k].values() if m["_status"] == st)
                    for st in sorted({m["_status"] for k in meas for m in meas[k].values()})},
        "no_filing_any_fy": sum(1 for k, _ in top if not filings[k]),
        "filer_mismatch": filer_mismatch,
        "cap_bound": [f"{r['scope']} ({r['group']}) FY{r['cap_bound_fys']}: {r['abroad_expense_usd']} -> {r['abroad_expense_cap_adj_usd']}"
                      for r in rrows if r["cap_bound_fys"]], "inputs": {k: (round(v, 4) if v < 10 else round(v)) for k, v in d.items()},
        "summary": [slim(r, ("scope", "group", "row_type_detail", "recipients", "inbound_usd", "abroad_expense_usd", "abroad_share_of_inbound",
                             "abroad_l3_of_exp_usd", "abroad_grant_mix_usd", "abroad_expense_daf_weighted_usd", "abroad_expense_fy2023_usd",
                             "abroad_expense_fy2024_usd")) for r in summ],
        "comparison": [slim(r, ("row_type", "scope", "evidence", "abroad_expense_usd", "denominator_usd", "share_of_denominator")) for r in comp],
        "regions": [slim(r, ("row_type", "group", "scope", "category", "abroad_expense_usd", "region_share")) for r in reg + comb],
        "sponsors": [slim(r, ("scope", "inbound_usd", "abroad_expense_usd", "direct_l3_usd")) for r in sp[:12]],
        "recipients": [slim(r, ("rank", "scope", "group", "segment", "own_daf_ind", "ntee_cd", "inbound_usd", "expense_share", "l3_of_exp_share",
                                "grant_mix_share", "abroad_expense_usd", "abroad_l3_of_exp_usd", "abroad_grant_mix_usd", "share_basis",
                                "sched_f_present", "top_region", "part_ix_l3_foreign_usd", "sched_f_part1_noninv_usd",
                                "sched_f_part1_investments_usd", "return_status")) for r in rrows],
    }, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
