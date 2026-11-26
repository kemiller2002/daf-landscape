#!/usr/bin/env python3
"""Year-by-year recipient sector mix of DAF grant dollars, FY2021-FY2024, top-50 and all itemising DAFRC panel
sponsors (P-B51-01, task b51-01).

Builds on scripts/mission_sector_join_all.py (b39n4-01, validated byte-identical in wave 43A) and
scripts/mission_recipient_sectors.py (P-NEW-RCP-01); imports both, and mission_coverage_gap.py for the DAF weight,
and modifies none of them.

Universe   Every DAFRC 2025 panel sponsor-year FY2021-FY2024 in the netpayout990 cache, return chosen with
           mission_daf_to_daf.pick_returns, itemising Schedule I Part II (mission_net_payout.itemized and a non-zero
           line count), exactly the b40n1202-01 / b39n4-01 rule extended to FY2021-22. Top 50 = the fixed FY2024
           DAF-asset ranking (mission_daf_to_daf.top_n), as in b39n4-01. University/hospital sponsors are excluded
           from both headline scopes, as in b39n4-01.
Lines      FY2023-24: the committed caches rcp/lines (top 50) and q120201/lines (others), read with
           mission_recipient_sectors.load_lines (no fetch). FY2021-22: the same returns' Schedule I Part II lines are
           read in full from the GivingTuesday mirror of IRS TEOS e-file XML (one streamed pass that also reads Part IX
           lines 1-3, with mission_recipient_sectors.line_of and mission_coverage_gap.P9_TAGS), into a new gzip cache
           (--new-cache); a sponsor-year is used only when the parsed line count equals the cache's sched_i_lines.
           Filer totals rows dropped (mission_exception_load.drop_totals_rows).
Join       mission_recipient_sectors.load_bmf + annotate unchanged (DAF-to-DAF whitelist, NTEE major group, BMF
           FOUNDATION-code and name-rule fallbacks). One BMF snapshot (the rcp/bmf extract) for all years.
Weights    daf_weighted: w2 = min(1, corrected DAFRC DAF grants / (L1 + L3)). FY2023-24 from
           coverage-gap-decomposition-2026-11-20.csv; FY2021-22 from mission_coverage_gap.sponsor_row on the new
           Part IX extract, DAFRC raw DAF grants and applied dafrc-corrections-itemized.csv deltas.
Shares     mission_sector_join_all.sy_aggregate / scaled / scope_fy / vector, per FY: treatments t_a_base (primary),
           t_b_d2d_included, t_c_t_separate (NTEE T shown on its own); layers sched_i, plus_foreign,
           plus_foreign_sub5k (sub-$5,000 component allocated per FY and scope, b40n120201-01 / wave-41B rules).
Panels     changing: every itemising sponsor-year in the scope that FY; fixed: only sponsors itemising (lines ok) in
           all four FYs.
Variants   base; ex_cz: lines to Chan Zuckerberg LLC recipients (CZ Biohub SF / New York / Chicago, CZ Institute for
           Advanced Biological Imaging; name rule CZ_RX) removed, with the same dollars removed from Part IX line 1 so
           they do not re-enter as sub-$5,000 grants; ex_svcf: Silicon Valley Community Foundation dropped.
Contrib.   For FY pairs, each recipient's contribution to a sector's share change = a_r,1/T_1 - a_r,0/T_0 (t_a,
           daf_weighted, changing panel, base variant, T = the layer total); summed over a sector's recipients
           this equals the change in the sector's itemised share.

Stdlib only; pure functions, I/O only in the fetch/load helpers and main.

Usage:
  python3 scripts/mission_sector_mix_trend.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES \
      --lines-cache Q120201_LINES --bmf-dir BMF --new-cache NEW [--fetch] [--fetch-only] [--out CSV]
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_recipient_sectors as rs  # noqa: E402
import mission_sector_join_all as sja  # noqa: E402
import mission_coverage_gap as cg  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402

OUT = os.path.join(DATA, "sector-mix-trend-2026-11-20.csv")
FYS = (2021, 2022, 2023, 2024)
NEW_FYS = (2021, 2022)
CACHE_V = 1
UA = "research-script/1.0"
SVCF = rs.SVCF
CZ_RX = re.compile(r"\bBIOHUB\b|^CZ\b|\bCHAN ZUCKERBERG\b")
TREATMENTS = ("t_a_base", "t_b_d2d_included", "t_c_t_separate")
LAYERS = sja.LAYERS
BASES = ("daf_weighted", "schedule_i")
SCOPES = ("top50_ex_university_hospital", "all_ex_university_hospital")
PANELS = ("changing", "fixed")
VARIANTS = ("base", "ex_cz", "ex_svcf")
PAIRS = ((2021, 2024), (2021, 2022), (2022, 2023), (2023, 2024))
TOPK = 5
SOURCE = ("IRS Form 990 Schedule I Part II lines and Part IX lines 1 and 3 (GivingTuesday mirror of IRS TEOS e-file "
          "XML; FY2023-24 from caches rcp/lines and q120201/lines, FY2021-22 read for this study) of every itemising "
          "DAFRC 2025 panel sponsor-year, joined to IRS EO BMF NTEE_CD via mission_recipient_sectors.py; w2 DAF weight "
          "from DAFRC 2025 DAF grants with dafrc-corrections-itemized.csv")


# ----------------------------------------------------------------------------- fetch FY2021-22 (one pass per return)
def parse_return(stream) -> dict:
    """Schedule I Part II lines (mission_recipient_sectors.line_of) and Part IX lines 1-3 (column A) in one pass."""
    lines, p9, filer = [], {}, [""]
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "RecipientTable":
            lines.append(rs.line_of(el))
            el.clear()
        elif tag in cg.P9_TAGS and cg.P9_TAGS[tag] not in p9:
            p9[cg.P9_TAGS[tag]] = cg._amt(el, "TotalAmt")
        elif tag == "Filer" and not filer[0]:
            filer[0] = next((ein9(c.text) for c in el if local(c.tag) == "EIN" and c.text), "")
        elif tag.startswith("IRS990") and tag not in ("IRS990", "IRS990ScheduleI"):
            el.clear()
    return {"filer_ein": filer[0], "lines": lines, "p9": {k: p9.get(k) for k in ("l1", "l2", "l3")}}


def cache_path(cache: str, oid: str) -> str:
    return os.path.join(cache, f"{oid}.json.gz")


def read_cache(cache: str, oid: str) -> dict | None:
    p = cache_path(cache, oid)
    if not os.path.exists(p):
        return None
    try:
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            c = json.load(fh)
    except (OSError, json.JSONDecodeError, EOFError):
        return None
    return c if c.get("_v") == CACHE_V else None


def fetch_return(oid: str, expect: int, cache: str, fetch: bool) -> dict:
    c = read_cache(cache, oid)
    if c is not None:
        return c
    if not fetch:
        return {"status": "not_fetched", "lines": [], "p9": {}}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                r = parse_return(resp)
            st = "ok" if len(r["lines"]) == expect else f"count_mismatch:{len(r['lines'])}!={expect}"
            out = {**r, "status": st, "via": "mirror", "_v": CACHE_V}
            os.makedirs(cache, exist_ok=True)
            with gzip.open(cache_path(cache, oid) + ".tmp", "wt", encoding="utf-8") as fh:
                json.dump(out, fh)
            os.replace(cache_path(cache, oid) + ".tmp", cache_path(cache, oid))
            return out
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}", "lines": [], "p9": {}}
            time.sleep(3 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error", "lines": [], "p9": {}}


def robots_check(cache: str) -> str:
    host = "gt990datalake-rawdata.s3.amazonaws.com"
    req = urllib.request.Request(f"https://{host}/robots.txt", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            code, body = r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        code, body = e.code, ""
    os.makedirs(cache, exist_ok=True)
    with open(os.path.join(cache, "robots-log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{host}\t{code}\t{len(body)}\n")
    low = body.lower()
    bots = ("claudebot", "anthropic-ai", "claude-user", "claude-web", "claude-searchbot")
    blocked = code in (401, 403) or (code == 200 and ("disallow: /\n" in low + "\n" or any(b in low for b in bots)))
    return "blocked" if blocked else f"allowed_{code}"


# ----------------------------------------------------------------------------- universe
def universe(chosen: Mapping, panel: Mapping, rank: Mapping) -> dict:
    """(ein, fy) -> {x, tier, pre} for every panel sponsor-year FY2021-24 (n50.sponsor_years rule, more FYs)."""
    def pre(x):
        return "not_itemised" if not itemized(x) else "no_sched_i_lines" if not (x.get("sched_i_lines") or 0) else "itemised"
    return {k: {"x": x, "tier": "top50" if k[0] in rank else "other", "pre": pre(x)}
            for k, x in chosen.items() if k[0] in panel and k[1] in FYS}


def is_cz(r: Mapping) -> bool:
    return bool(CZ_RX.search((r["name"] or "").upper()))


def variant_inputs(ann: Sequence[Mapping], gap: Mapping, variant: str) -> tuple:
    """Remove CZ lines (and the same dollars from L1, so they do not re-enter as sub-$5k grants)."""
    if variant != "ex_cz":
        return ann, gap
    cz = sum(r["amount"] for r in ann if is_cz(r))
    return tuple(r for r in ann if not is_cz(r)), ({**gap, "l1": gap.get("l1", 0.0) - cz} if cz else gap)


# ----------------------------------------------------------------------------- shares
def scope_pred(scope: str, tiers: Mapping, seg: Mapping):
    if scope == "top50_ex_university_hospital":
        return lambda k: tiers[k] == "top50" and seg[k[0]] != "university_hospital"
    return lambda k: seg[k[0]] != "university_hospital"


def fixed_eins(keys: Sequence[tuple]) -> frozenset:
    by = _group_by_fast(keys, lambda k: k[0])
    return frozenset(e for e, ks in by.items() if {k[1] for k in ks} >= set(FYS))


def share_block(meta: Mapping, p: Mapping) -> list:
    out = []
    for t in TREATMENTS:
        cnt = sja.counts(p, t)
        for layer in LAYERS:
            v = sja.vector(p, t, layer)
            tot = sum(v.values())
            head = {**meta, "row_type": "share", "treatment": t, "layer": layer}
            out.append({**head, "sector": "ALL", "amount_usd": round(tot), "share": 1.0 if tot else None,
                        "lines": int(sum(cnt.values())), "sponsor_years": p["sponsor_years"], "sponsors": p["sponsors"],
                        "sched_i_total_usd": round(p["si_total"]), "d2d_usd": round(sum(p["d2d"].values())),
                        "ntee_t_non_d2d_usd": round(p["net"]["psb_t"]), "part_ix_l1_usd": round(p["l1"]),
                        "foreign_l3_usd": round(p["l3"]), "sub5k_full_usd": round(p["sub5k_full"]),
                        "sub5k_partial_usd": round(p["sub5k_partial"])})
            out.extend({**head, "sector": g, "amount_usd": round(v[g]), "share": v[g] / tot if tot else None,
                        "lines": int(cnt.get(g, 0)) if g != "foreign_schedule_f" else ""}
                       for g in sja.OUT_GROUPS if g in v)
    return out


def change_rows(share_rows: Sequence[Mapping]) -> list:
    key = lambda r: (r["scope"], r["panel"], r["variant"], r["basis"], r["treatment"], r["layer"], r["sector"])  # noqa: E731
    by = {(key(r), r["fiscal_year"]): r for r in share_rows}
    keys = sorted({key(r) for r in share_rows})

    def one(k, fy0, fy1):
        a, b = by.get((k, str(fy0))), by.get((k, str(fy1)))
        if not a or not b or a["share"] is None or b["share"] is None:
            return None
        return {"row_type": "change", **dict(zip(("scope", "panel", "variant", "basis", "treatment", "layer", "sector"), k)),
                "fiscal_year": f"{fy0}-{fy1}", "share_from": a["share"], "share": b["share"],
                "change_pp": round((b["share"] - a["share"]) * 100, 3), "amount_usd": b["amount_usd"] - a["amount_usd"]}
    return [r for r in (one(k, f0, f1) for k in keys for f0, f1 in PAIRS) if r]


def recipient_contrib(ann: Mapping, keys_by_fy: Mapping, w2: Mapping, totals: Mapping, scope: str) -> list:
    """t_a, daf_weighted: per sector, the recipients that moved its share most between each FY pair."""
    def amounts(fy):
        return reduce(lambda a, r: sja._acc(a, (r["key"], sja.ext_group(r)), r["amount"] * r["_w"]),
                      ({**r, "_w": w2[k]} for k in keys_by_fy[fy] for r in ann[k] if not r["d2d"]), {})
    am = {fy: amounts(fy) for fy in FYS}
    names = {r["key"]: (r["name"], r["ein"]) for ks in keys_by_fy.values() for k in ks for r in ann[k] if not r["d2d"]}
    sect = lambda eg: "public_societal_benefit" if eg in ("psb_t", "psb_other") else eg  # noqa: E731
    out = []
    for layer, tot in totals.items():
        for f0, f1 in PAIRS:
            t0, t1 = tot[f0], tot[f1]
            rec = {k: am[f1].get(k, 0.0) / t1 - am[f0].get(k, 0.0) / t0 for k in set(am[f0]) | set(am[f1])}
            by_s = _group_by_fast(rec.items(), lambda kv: sect(kv[0][1]))
            for s, items in sorted(by_s.items()):
                ranked = sorted(items, key=lambda kv: -abs(kv[1]))
                total = sum(v for _, v in items)
                head = {"row_type": "recipient_contribution", "scope": scope, "panel": "changing", "variant": "base",
                        "basis": "daf_weighted", "treatment": "t_a_base", "layer": layer, "fiscal_year": f"{f0}-{f1}",
                        "sector": s}
                out.append({**head, "rank": 0, "recipient_name": "SECTOR_ITEMISED_TOTAL",
                            "change_pp": round(total * 100, 4), "recipients": len(items),
                            "top1_pp": round(ranked[0][1] * 100, 4) if ranked else None,
                            "top5_pp": round(sum(v for _, v in ranked[:5]) * 100, 4),
                            "top10_pp": round(sum(v for _, v in ranked[:10]) * 100, 4)})
                out.extend({**head, "rank": i + 1, "recipient_name": names[kk[0]][0], "recipient_ein": names[kk[0]][1],
                            "amount_from_usd": round(am[f0].get(kk, 0.0)), "amount_usd": round(am[f1].get(kk, 0.0)),
                            "change_pp": round(v * 100, 4)} for i, (kk, v) in enumerate(ranked[:TOPK]))
    return out


def panel_rows(keys_ok: Sequence[tuple], sy: Mapping, loaded_status: Mapping, panel: Mapping, rank: Mapping,
               w2: Mapping, l13: Mapping, fixed: frozenset) -> list:
    """Per FY and tier: itemising status, sponsors entering or leaving the itemised set, and their DAF-weighted L1+L3."""
    seg = lambda e: panel[e]["segment"]  # noqa: E731
    out = []
    for scope, pred in (("top50_ex_university_hospital", lambda e: e in rank and seg(e) != "university_hospital"),
                        ("all_ex_university_hospital", lambda e: seg(e) != "university_hospital")):
        ok = {fy: frozenset(k[0] for k in keys_ok if k[1] == fy and pred(k[0])) for fy in FYS}
        for fy in FYS:
            in_panel = [k for k in sy if k[1] == fy and pred(k[0])]
            st = _group_by_fast(in_panel, lambda k: sy[k]["pre"] if sy[k]["pre"] != "itemised" else
                                ("itemised_ok" if loaded_status.get(k) == "ok" else "itemised_" + str(loaded_status.get(k))))
            prev = ok[fy - 1] if fy - 1 in ok else None
            dw = lambda es: round(sum(w2[(e, fy)] * l13[(e, fy)] for e in es if (e, fy) in w2))  # noqa: E731
            base = {"row_type": "panel", "scope": scope, "fiscal_year": str(fy)}
            out.extend({**base, "sector": f"status:{s}", "sponsor_years": len(v)} for s, v in sorted(st.items()))
            out.append({**base, "sector": "fixed_panel_sponsors", "sponsors": len(ok[fy] & fixed),
                        "amount_usd": dw(ok[fy] & fixed)})
            out.append({**base, "sector": "changing_only_sponsors", "sponsors": len(ok[fy] - fixed),
                        "amount_usd": dw(ok[fy] - fixed)})
            if prev is not None:
                out.append({**base, "sector": "entered_vs_prior_fy", "sponsors": len(ok[fy] - prev), "amount_usd": dw(ok[fy] - prev)})
                out.append({**base, "sector": "left_vs_prior_fy", "sponsors": len(prev - ok[fy])})
    return out


# ----------------------------------------------------------------------------- main
FIELDS = ("row_type", "scope", "panel", "variant", "basis", "fiscal_year", "treatment", "layer", "sector", "amount_usd",
          "share", "share_from", "change_pp", "lines", "sponsor_years", "sponsors", "sched_i_total_usd", "d2d_usd",
          "ntee_t_non_d2d_usd", "part_ix_l1_usd", "foreign_l3_usd", "sub5k_full_usd", "sub5k_partial_usd", "rank",
          "recipient_name", "recipient_ein", "amount_from_usd", "recipients", "top1_pp", "top5_pp", "top10_pp", "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache-top50", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--new-cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--fetch-only", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    sy = universe(pick_returns(load_np(a.np_cache)), panel, rank)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}
    keys = sorted(item)

    robots = robots_check(a.new_cache) if a.fetch else "not_checked_cache_only"
    if robots == "blocked":
        raise SystemExit("robots.txt disallows the mirror")

    def lines(k):
        v = item[k]
        if k[1] in NEW_FYS:
            return fetch_return(v["x"]["oid"], v["x"]["sched_i_lines"], a.new_cache, a.fetch)
        return rs.load_lines(v["x"]["oid"], v["x"]["sched_i_lines"],
                             a.lines_cache_top50 if v["tier"] == "top50" else a.lines_cache, [], False)
    # largest returns first so the long downloads overlap
    order = sorted(keys, key=lambda k: -(item[k]["x"]["sched_i_lines"] or 0))
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        loaded = dict(zip(order, ex.map(lines, order)))
    status = {k: v["status"] for k, v in loaded.items()}
    if a.fetch_only:
        print(json.dumps({"robots": robots, "status": {s: len(v) for s, v in _group_by_fast(status.values(), lambda s: s).items()}}))
        return 0
    good = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers = {k: item[k]["tier"] for k in good}
    seg = {e: p["segment"] for e, p in panel.items()}

    wl = read_csv(rs.WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    groups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in groups.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf = rs.load_bmf(a.bmf_dir, eins)
    ann = {k: rs.annotate(k[0], v["lines"], bmf, wl_eins, wl_names) for k, v in good.items()}

    # DAF weight w2 and Part IX L1/L3
    gap_csv = {(ein9(r["ein"]), int(r["fiscal_year"])): {"l1": num(r["l1"]) or 0.0, "l3": num(r["l3"]) or 0.0,
                                                         "w2": num(r["w2"]) if r["w2"] not in ("", None) else 1.0}
               for r in read_csv(sja.GAP_CSV) if r["row_type"] == "sponsor_itemised"}
    deltas = cg.corrected_deltas(read_csv(cg.CORR_CSV))
    d_raw = {(ein9(r["ein"]), int(r["fiscal_year_end"])): num(r.get("total_daf_grants")) or 0.0 for r in dafrc}

    def gap_new(k):
        p9 = {**loaded[k].get("p9", {}), "status": "ok" if loaded[k].get("p9", {}).get("l1") is not None else "missing"}
        r = cg.sponsor_row(k, p9, item[k]["x"], 1.0, d_raw.get(k, 0.0), d_raw.get(k, 0.0) + deltas.get(k, 0.0), ann[k])
        return {"l1": r["l1"], "l3": r["l3"], "w2": r["w2"], "p9_status": p9["status"]}
    gap = {k: (gap_new(k) if k[1] in NEW_FYS else gap_csv.get(k, {})) for k in good}
    w2 = {k: g.get("w2", 1.0) for k, g in gap.items()}
    l13 = {k: g.get("l1", 0.0) + g.get("l3", 0.0) for k, g in gap.items()}

    def agg_of(k, variant):
        lines_v, gap_v = variant_inputs(ann[k], gap[k], variant)
        return {**sja.sy_aggregate(lines_v, gap_v), "ein": k[0], "fy": k[1]}
    aggs = {(k, v): agg_of(k, v) for k in good for v in ("base", "ex_cz")}

    rows, parts = [], {}
    for scope in SCOPES:
        pred = scope_pred(scope, tiers, seg)
        in_scope = [k for k in good if pred(k)]
        fixed = fixed_eins(in_scope)
        for pnl in PANELS:
            for variant in VARIANTS:
                ks = [k for k in in_scope if (pnl == "changing" or k[0] in fixed) and not (variant == "ex_svcf" and k[0] == SVCF)]
                av = "ex_cz" if variant == "ex_cz" else "base"
                for basis in BASES:
                    for fy in FYS:
                        sel = tuple(sja.scaled(aggs[(k, av)], w2[k]) if basis == "daf_weighted" else aggs[(k, av)]
                                    for k in ks if k[1] == fy)
                        if not sel:
                            continue
                        p = sja.scope_fy(sel)
                        parts[(scope, pnl, variant, basis, fy)] = p
                        rows.extend(share_block({"scope": scope, "panel": pnl, "variant": variant, "basis": basis,
                                                 "fiscal_year": str(fy), "source": SOURCE}, p))
    changes = change_rows([r for r in rows if r["row_type"] == "share"])

    contrib = []
    for scope in SCOPES:
        pred = scope_pred(scope, tiers, seg)
        kb = {fy: [k for k in good if pred(k) and k[1] == fy] for fy in FYS}
        totals = {layer: {fy: sum(sja.vector(parts[(scope, "changing", "base", "daf_weighted", fy)], "t_a_base", layer).values())
                          for fy in FYS} for layer in ("sched_i", "plus_foreign_sub5k")}
        contrib.extend(recipient_contrib(ann, kb, w2, totals, scope))

    fixed_all = fixed_eins([k for k in good if seg[k[0]] != "university_hospital"])
    prow = panel_rows(sorted(good), sy, status, panel, rank, w2, l13, fixed_all)
    write_csv(a.out, rows + changes + contrib + prow, FIELDS)

    # ---------------------------------------------------------------- summary for the write-up
    def sh(scope, pnl="changing", variant="base", basis="daf_weighted", t="t_a_base", layer="plus_foreign_sub5k"):
        return {fy: {r["sector"]: (round(r["share"] * 100, 2) if r["share"] is not None else None)
                     for r in rows if r["scope"] == scope and r["panel"] == pnl and r["variant"] == variant
                     and r["basis"] == basis and r["treatment"] == t and r["layer"] == layer and r["fiscal_year"] == str(fy)
                     and r["sector"] != "ALL"} for fy in FYS}

    def tot(scope, pnl="changing", variant="base", basis="daf_weighted", t="t_a_base", layer="plus_foreign_sub5k"):
        return {fy: next((r for r in rows if r["scope"] == scope and r["panel"] == pnl and r["variant"] == variant
                          and r["basis"] == basis and r["treatment"] == t and r["layer"] == layer
                          and r["fiscal_year"] == str(fy) and r["sector"] == "ALL"), {}) for fy in FYS}
    cz_lines = sorted(((k[0], k[1], r["name"], r["ein"], round(r["amount"]), r["group"], r["method"])
                       for k in good for r in ann[k] if is_cz(r)), key=lambda t: -t[4])
    summary = {
        "robots": robots,
        "sponsor_years_panel_by_fy": {fy: sum(1 for k in sy if k[1] == fy) for fy in FYS},
        "itemised_by_fy": {fy: sum(1 for k in item if k[1] == fy) for fy in FYS},
        "lines_ok_by_fy": {fy: sum(1 for k in good if k[1] == fy) for fy in FYS},
        "load_problems": {f"{panel[k[0]]['name'][:40]} FY{k[1]}": s for k, s in status.items() if s != "ok"},
        "lines_by_fy": {fy: sum(len(good[k]["lines"]) for k in good if k[1] == fy) for fy in FYS},
        "bmf_matched": f"{len(bmf)}/{len(eins)}",
        "p9_missing_fy2021_22": sorted(f"{panel[k[0]]['name'][:40]} FY{k[1]}" for k in good if k[1] in NEW_FYS
                                       and gap[k].get("p9_status") != "ok"),
        "check_fy2023_24_vs_b39n4": "see doc",
        "fixed_panel_sponsors": {s: len(fixed_eins([k for k in good if scope_pred(s, tiers, seg)(k)])) for s in SCOPES},
        "cz_lines": cz_lines,
        "method_mix_by_fy": {fy: rs.method_mix({k: v for k, v in ann.items() if k[1] == fy}) for fy in FYS},
        "rows": len(rows) + len(changes) + len(contrib) + len(prow),
        **{f"shares|{s}|{p}|{v}|{b}|{t}|{l}": sh(s, p, v, b, t, l)
           for s in SCOPES for p in PANELS for v in VARIANTS for b in ("daf_weighted",) for t in TREATMENTS
           for l in ("plus_foreign_sub5k", "sched_i")},
        **{f"shares|{s}|changing|base|schedule_i|t_a_base|plus_foreign_sub5k": sh(s, basis="schedule_i") for s in SCOPES},
        **{f"totals|{s}|{p}|{v}": {fy: {c: r.get(c) for c in ("amount_usd", "sponsor_years", "sponsors", "d2d_usd",
                                                              "ntee_t_non_d2d_usd", "foreign_l3_usd", "sub5k_full_usd",
                                                              "sub5k_partial_usd", "lines")}
                                   for fy, r in tot(s, p, v).items()} for s in SCOPES for p in PANELS for v in VARIANTS},
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
