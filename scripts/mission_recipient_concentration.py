#!/usr/bin/env python3
"""Recipient concentration of DAF grant dollars, and fastest-growing recipients: top-50 sponsors, FY2021-FY2024 (b51-02).

Universe, return choice, line parsing, DAF-to-DAF netting and DAF weighting are those of the repo, imported unchanged:
  * sponsors     top-50 DAFRC sponsors by FY2024 DAF assets (mission_daf_to_daf.top_n);
  * returns      one return per sponsor x fiscal year (mission_daf_to_daf.pick_returns over the netpayout990/ cache),
                 itemising Schedule I only (mission_net_payout.itemized);
  * lines        every Schedule I Part II line (mission_recipient_sectors.load_lines; e-file XML, GivingTuesday mirror
                 of IRS TEOS when not cached);
  * netting      mission_recipient_sectors.annotate: lines to an EIN whose decision is `include` in
                 daf-to-daf-recipient-whitelist.csv, self-lines, and blank-EIN lines whose normalised name matches
                 exactly one whitelisted panel name are dropped;
  * weighting    `daf_weighted` = each sponsor-year's lines x daf_share_of_grants (sponsor-cost-structure.csv, capped
                 at 1). That file has no FY2021 shares, so daf_weighted rows are written only for FY2022-FY2024.
Fiscal year = calendar year in which the sponsor's tax period ends (DAFRC convention).

Outputs (one CSV, row_type column):
  concentration  per scope x basis x FY: recipients, top-10/100/1,000 shares, Gini (over recipients with a positive
                 total) and HHI (0-10,000). Scopes: `all_itemising` (every itemising top-50 sponsor-year that FY) and
                 `balanced_panel` (sponsors itemising in all four FYs; the trend basis), plus a sensitivity that
                 merges the four Chan Zuckerberg LLC EINs into CZ Biohub Inc (disregarded entities, per
                 non-bmf-recipients-2026-11-20.csv and its note).
  grower         balanced panel, Schedule I (filed) basis: P1 = FY2021+FY2022, P2 = FY2023+FY2024; recipients with
                 P2 >= $5m; top 50 by absolute growth (`abs`), top 50 by percentage growth among P1 > 0 (`pct`), and
                 every recipient with P1 = 0 (`entrant`). Each row carries IRS EO BMF NTEE, subsection, ruling date
                 and a rule-based type (org_type; first match wins, see type_of) plus flags.

Stdlib only; functional style (pure transforms, I/O at the edges).

Usage:
  python3 scripts/mission_recipient_concentration.py . --np-cache NPCACHE --bmf-dir BMF \
      --lines-cache LC [--lines-cache LC2 ...] [--fetch] [--summary JSON]
  `.` is the repo root (accepted for the repo convention; paths resolve from the script location).
  Cached lines are looked up in each --lines-cache in turn; with --fetch, missing returns are read from the mirror
  and saved in the last --lines-cache.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_sectors import BMF_FILES, COST, MAJOR, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "recipient-concentration-growth-2026-11-20.csv")
FS_LIST = os.path.join(DATA, "fiscal-sponsor-ein-list-2026-11-19.csv")
DE_FACTO = os.path.join(DATA, "de-facto-fiscal-sponsors-2026-11-20.csv")
PASS_THROUGH = os.path.join(DATA, "pass-through-recipients-2026-11-20.csv")
NON_BMF = os.path.join(DATA, "non-bmf-recipients-2026-11-20.csv")
FYS = (2021, 2022, 2023, 2024)
P1, P2 = (2021, 2022), (2023, 2024)
FLOOR = 5_000_000.0
N_LIST = 50
CZ_BIOHUB = "811669175"  # Chan Zuckerberg Biohub Inc (BMF 501(c)(3)); parent of the CZ LLCs per Schedule R (b40n1202-b43n26-03)
CZ_LLC = re.compile(r"^CZ (BIOHUB|INSTITUTE)")
NEW_RULING = 202001  # ruling year 2020 or later = "new organisation"
POLICY_W = frozenset({"W01", "W02", "W03", "W05", "W20", "W22", "W24"})
SOURCE = ("IRS Form 990 Schedule I Part II (e-file XML, GivingTuesday mirror of IRS TEOS), top-50 DAFRC sponsors, "
          "itemising returns FY2021-FY2024; DAF-to-DAF netted via daf-to-daf-recipient-whitelist.csv; recipients joined "
          "to IRS EO BMF (eo1-4, eo_pr, eo_xx; cached 2026-11-14) NTEE_CD/SUBSECTION/RULING/FOUNDATION")


# ----------------------------------------------------------------------------- I/O helpers
def lines_for(item: Mapping, caches: Sequence[str], xml_dirs: Sequence[str], fetch: bool, workers: int) -> dict:
    """(ein, fy) -> load_lines result; first cache that holds the return wins, fetches land in the last cache."""
    def one(kv):
        k, x = kv
        hits = (load_lines(x["oid"], x.get("sched_i_lines") or 0, c, xml_dirs, False) for c in caches)
        got = next((h for h in hits if h.get("status") == "ok"), None)
        return k, got or load_lines(x["oid"], x.get("sched_i_lines") or 0, caches[-1], xml_dirs, fetch)
    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(ex.map(one, sorted(item.items(), key=lambda kv: -(kv[1].get("sched_i_lines") or 0))))


def load_bmf_full(bmf_dir: str, eins: frozenset) -> dict:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple(r for r in csv.DictReader(fh) if ein9(r["EIN"]) in eins)
    pick = lambda r: {"ntee": (r.get("NTEE_CD") or "").strip().upper(), "foundation": (r.get("FOUNDATION") or "").strip(),  # noqa: E731
                      "subsection": (r.get("SUBSECTION") or "").strip(), "bmf_name": (r.get("NAME") or "").strip(),
                      "bmf_state": (r.get("STATE") or "").strip(), "ruling": (r.get("RULING") or "").strip()}
    return {ein9(r["EIN"]): pick(r) for f in BMF_FILES for r in rows(f)}


# ----------------------------------------------------------------------------- pure: metrics
def totals_by_key(rows: Sequence[Mapping], weight: Mapping, merge: Mapping) -> dict:
    acc: dict = {}
    for r in rows:
        k = merge.get(r["key"], r["key"])
        acc[k] = acc.get(k, 0.0) + r["amount"] * weight.get(r["_sy"], 1.0)
    return acc


def gini(vals: Sequence[float]) -> float | None:
    xs = sorted(vals)
    n, s = len(xs), sum(xs)
    return (2 * sum((i + 1) * x for i, x in enumerate(xs)) / (n * s) - (n + 1) / n) if n and s else None


def metrics(by: Mapping) -> dict:
    vals = sorted((v for v in by.values() if v > 0), reverse=True)
    tot = sum(vals)
    sh = lambda n: sum(vals[:n]) / tot if tot else None  # noqa: E731
    return {"recipients": len(vals), "total_usd": tot, "top10_share": sh(10), "top100_share": sh(100),
            "top1000_share": sh(1000), "gini": gini(vals), "hhi": sum((v / tot * 100) ** 2 for v in vals) if tot else None,
            "top1_key": next((k for k, v in sorted(by.items(), key=lambda kv: -kv[1])), "")}


def conc_rows(ann: Mapping, scopes: Mapping, weights: Mapping, merge_cz: Mapping) -> tuple[dict, ...]:
    def one(scope, sy_keys, fy, basis, wt, merge):
        keys = tuple(k for k in sy_keys if k[1] == fy)
        if basis == "daf_weighted" and not all(k in wt for k in keys):
            return None
        rows = tuple(r for k in keys for r in ann[k])
        kept = tuple(r for r in rows if not r["d2d"])
        w = lambda r: r["amount"] * wt.get(r["_sy"], 1.0)  # noqa: E731
        gross = sum(w(r) for r in rows)
        m = metrics(totals_by_key(kept, wt, merge))
        return {"row_type": "concentration", "scope": scope, "basis": basis, "fiscal_year": fy, "sponsor_years": len(keys),
                "gross_sched_i_usd": round(gross), "d2d_excluded_usd": round(gross - m["total_usd"]),
                **{k: v for k, v in m.items() if k != "top1_key"}, "total_usd": round(m["total_usd"]),
                "top1_recipient": m["top1_key"], "source": SOURCE}
    specs = [(s, keys, fy, b, wt, {}) for s, keys in scopes.items() for fy in FYS
             for b, wt in (("schedule_i", {}), ("daf_weighted", weights))]
    specs += [(s + "_cz_merged", keys, fy, "schedule_i", {}, merge_cz) for s, keys in scopes.items() for fy in FYS]
    return tuple(r for r in (one(*s) for s in specs) if r)


# ----------------------------------------------------------------------------- pure: growth
def recipient_panel(ann: Mapping, keys: Sequence) -> dict:
    """recipient key -> {fy: usd, grantors per period, top P2 grantor}."""
    acc: dict = {}
    for k in keys:
        for r in ann[k]:
            if r["d2d"]:
                continue
            d = acc.setdefault(r["key"], {"ein": r["ein"], "names": {}, "fy": {}, "g": {}})
            d["fy"][k[1]] = d["fy"].get(k[1], 0.0) + r["amount"]
            d["g"][(k[0], k[1])] = d["g"].get((k[0], k[1]), 0.0) + r["amount"]
            d["names"][r["name"]] = d["names"].get(r["name"], 0.0) + r["amount"]
    return acc


def type_of(ein: str, name: str, b: Mapping, fs: Mapping, pt: Mapping, nonbmf: Mapping, panel: Mapping) -> tuple[str, str]:
    """-> (org_type, basis). First match wins. Rule-based on IRS BMF fields, repo lists and filed name."""
    ntee, fnd, up = (b or {}).get("ntee", ""), (b or {}).get("foundation", ""), (name or "").upper()
    nb = nonbmf.get(ein, "")
    rules: tuple[tuple[str, Callable[[], bool], str], ...] = (
        ("blank_ein_name_keyed", lambda: not ein, "Schedule I line has no recipient EIN; keyed by normalised name"),
        ("disregarded_entity_llc", lambda: nb == "subsidiary_or_disregarded", "non-bmf-recipients category"),
        ("not_in_bmf_" + (nb or "other"), lambda: not b and bool(ein), "absent from EO BMF"),
        ("fiscal_sponsor", lambda: ein in fs, "fiscal-sponsor list / de-facto file: " + fs.get(ein, "")),
        ("intermediary_pass_through", lambda: pt.get(ein, ("", ""))[0] == "regranting_intermediary",
         "pass-through-recipients: " + pt.get(ein, ("", ""))[1]),
        ("daf_sponsor_not_netted", lambda: ein in panel and panel[ein]["segment"] in ("national", "processor", "community_foundation"),
         "DAFRC panel EIN, whitelist decision not include"),
        ("university_college", lambda: ntee[:2] in ("B4", "B5") or (fnd == "11" and re.search(r"UNIVERSITY|COLLEGE", up) is not None)
         or (not ntee and re.search(r"\b(UNIVERSITY|COLLEGE)\b", up) is not None), "NTEE B4x/B5x or name"),
        ("hospital_health_system", lambda: ntee[:2] in ("E2",) or fnd == "12" or (not ntee and "HOSPITAL" in up), "NTEE E2x / foundation 12"),
        ("grantmaking_intermediary_ntee_t", lambda: ntee[:1] == "T" and ntee[:3] not in ("T40",), "NTEE T (philanthropy, grantmaking)"),
        ("policy_or_advocacy_ntee", lambda: ntee[:1] == "R" or ntee[:3] in POLICY_W or ntee[1:3] == "01",
         "NTEE R (civil rights, social action, advocacy), W01-W05/W20-W24 (public policy, government, civic "
         "participation) or common code 01 (alliances & advocacy)"),
        ("research_institute_ntee_u_v", lambda: ntee[:1] in ("U", "V"), "NTEE U (science & technology) / V (social science)"),
        ("school_or_other_education", lambda: ntee[:1] == "B", "NTEE B (not B4x/B5x)"),
        ("religious", lambda: ntee[:1] == "X" or fnd == "10", "NTEE X / foundation 10"),
        ("medical_research_or_health", lambda: ntee[:1] in "EFGH" and ntee != "", "NTEE E-H"),
        ("international", lambda: ntee[:1] == "Q", "NTEE Q"),
        ("operating_" + MAJOR.get(ntee[:1], "unclassified"), lambda: True, "NTEE major group"),
    )
    return next((t, why) for t, test, why in rules if test())


def grower_rows(ann: Mapping, keys: Sequence, bmf: Mapping, fs: Mapping, pt: Mapping, nonbmf: Mapping,
                panel: Mapping, names: Mapping) -> tuple[dict, ...]:
    rp = recipient_panel(ann, keys)

    def enrich(key, d):
        p1, p2 = sum(d["fy"].get(y, 0.0) for y in P1), sum(d["fy"].get(y, 0.0) for y in P2)
        ein, b = d["ein"], bmf.get(d["ein"])
        name = max(d["names"].items(), key=lambda kv: kv[1])[0]
        g2 = _group_by_fast(((g, v) for (g, y), v in d["g"].items() if y in P2), lambda gv: gv[0])
        g2s = sorted(((g, sum(v for _, v in xs)) for g, xs in g2.items()), key=lambda gv: -gv[1])
        typ, why = type_of(ein, name, b, fs, pt, nonbmf, panel)
        ruling = (b or {}).get("ruling", "")
        return {"ein": ein, "name_as_filed": name, "bmf_name": (b or {}).get("bmf_name", ""), "state": (b or {}).get("bmf_state", ""),
                "ntee_cd": (b or {}).get("ntee", ""), "ntee_major": MAJOR.get((b or {}).get("ntee", "")[:1], "unclassified"),
                "subsection": (b or {}).get("subsection", ""), "foundation_code": (b or {}).get("foundation", ""),
                "ruling": ruling, "is_new_org": int(bool(ruling) and int(ruling) >= NEW_RULING),
                "is_fiscal_sponsor": int(ein in fs), "fs_source": fs.get(ein, ""),
                "pass_through_class": pt.get(ein, ("", ""))[0], "pass_through_subtype": pt.get(ein, ("", ""))[1],
                "is_intermediary": int(ein in fs or pt.get(ein, ("", ""))[0] in ("fiscal_sponsor", "regranting_intermediary")
                                       or typ in ("grantmaking_intermediary_ntee_t", "intermediary_pass_through", "fiscal_sponsor")),
                "org_type": typ, "org_type_basis": why, "non_bmf_category": nonbmf.get(ein, ""),
                **{f"usd_fy{y}": round(d["fy"].get(y, 0.0)) for y in FYS},
                "usd_p1": round(p1), "usd_p2": round(p2), "growth_usd": round(p2 - p1),
                "growth_pct": (p2 / p1 - 1) if p1 > 0 else None,
                "grantors_p1": len({g for (g, y) in d["g"] if y in P1}), "grantors_p2": len(g2s),
                "top_grantor_p2": names.get(g2s[0][0], g2s[0][0]) if g2s else "",
                "top_grantor_share_p2": (g2s[0][1] / p2) if g2s and p2 else None, "_p1": p1, "_p2": p2}
    elig = tuple(enrich(k, d) for k, d in rp.items() if sum(d["fy"].get(y, 0.0) for y in P2) >= FLOOR)
    by_abs = sorted(elig, key=lambda r: -(r["_p2"] - r["_p1"]))[:N_LIST]
    by_pct = sorted((r for r in elig if r["_p1"] > 0), key=lambda r: -(r["_p2"] / r["_p1"]))[:N_LIST]
    entr = sorted((r for r in elig if r["_p1"] <= 0), key=lambda r: -r["_p2"])
    tag = lambda lst, rows: tuple({**r, "row_type": "grower", "scope": "balanced_panel", "basis": "schedule_i",  # noqa: E731
                                   "rank_list": lst, "rank": i + 1, "source": SOURCE} for i, r in enumerate(rows))
    return tag("abs", by_abs) + tag("pct", by_pct) + tag("entrant", entr)


def grower_summary(gr: Sequence[Mapping], elig_n: int) -> dict:
    def s(lst):
        rs = [r for r in gr if r["rank_list"] == lst]
        cnt = lambda f: sum(1 for r in rs if f(r))  # noqa: E731
        types = _group_by_fast(rs, lambda r: r["org_type"])
        return {"n": len(rs), "new_org_ruling_2020plus": cnt(lambda r: r["is_new_org"]),
                "fiscal_sponsor": cnt(lambda r: r["is_fiscal_sponsor"]), "intermediary_any": cnt(lambda r: r["is_intermediary"]),
                "pass_through_listed": cnt(lambda r: r["pass_through_class"] != ""),
                "growth_usd_sum": sum(r["growth_usd"] for r in rs),
                "by_type": {t: {"n": len(v), "growth_usd": sum(r["growth_usd"] for r in v)}
                            for t, v in sorted(types.items(), key=lambda kv: -len(kv[1]))},
                "by_ntee_major": {k: len(v) for k, v in sorted(_group_by_fast(rs, lambda r: r["ntee_major"]).items(), key=lambda kv: -len(kv[1]))}}
    return {"eligible_p2_ge_5m": elig_n, **{lst: s(lst) for lst in ("abs", "pct", "entrant")}}


FIELDS = ("row_type", "scope", "basis", "fiscal_year", "sponsor_years", "gross_sched_i_usd", "d2d_excluded_usd", "total_usd",
          "recipients", "top10_share", "top100_share", "top1000_share", "gini", "hhi", "top1_recipient",
          "rank_list", "rank", "ein", "name_as_filed", "bmf_name", "state", "ntee_cd", "ntee_major", "subsection",
          "foundation_code", "ruling", "is_new_org", "org_type", "org_type_basis", "is_fiscal_sponsor", "fs_source",
          "is_intermediary", "pass_through_class", "pass_through_subtype", "non_bmf_category",
          "usd_fy2021", "usd_fy2022", "usd_fy2023", "usd_fy2024", "usd_p1", "usd_p2", "growth_usd", "growth_pct",
          "grantors_p1", "grantors_p2", "top_grantor_p2", "top_grantor_share_p2", "source")


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--lines-cache", action="append", required=True)
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--summary", default="")
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, 50)
    chosen = pick_returns(load_np(a.np_cache))
    sy = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in sy.items() if itemized(x)}
    loaded = lines_for(item, a.lines_cache, a.xml_dir, a.fetch, a.workers)
    bad = {f"{panel[k[0]]['name']} FY{k[1]}": v["status"] for k, v in loaded.items() if v["status"] != "ok"}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    nm = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in nm.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf = load_bmf_full(a.bmf_dir, eins | {CZ_BIOHUB})

    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    weights = {k: min(1.0, max(0.0, share[k])) for k in good if share.get(k) is not None}

    ann = {k: tuple({**r, "_sy": k} for r in annotate(k[0], v["lines"], bmf, wl_eins, wl_names)) for k, v in good.items()}
    sponsors_by_fy = {fy: frozenset(e for (e, y) in good if y == fy) for fy in FYS}
    balanced = frozenset.intersection(*sponsors_by_fy.values())
    scopes = {"all_itemising": tuple(sorted(good)), "balanced_panel": tuple(k for k in sorted(good) if k[0] in balanced)}

    nonbmf_rows = read_csv(NON_BMF)
    nonbmf = {ein9(r["ein"]): r["category"] for r in nonbmf_rows if r["row_type"] == "recipient"}
    cz_eins = frozenset(ein9(r["ein"]) for r in nonbmf_rows if r["row_type"] == "recipient" and CZ_LLC.search((r["name_as_filed"] or "").upper()))
    merge_cz = {e: CZ_BIOHUB for e in cz_eins}

    fs_dir = {ein9(r["ein"]): "directory" if r["source"] == "fiscalsponsordirectory" else "q_b15"
              for r in read_csv(FS_LIST) if r["grantmaker_host"] != "True"}
    fs_df = {ein9(r["ein"]): "de_facto_intermediary" for r in read_csv(DE_FACTO) if r["de_facto_intermediary"] == "True"}
    fs = {**fs_df, **fs_dir}
    pt = {ein9(r["ein"]): (r["pass_through_class"], r["hand_subtype"]) for r in read_csv(PASS_THROUGH)}

    conc = conc_rows(ann, scopes, weights, merge_cz)
    gr = grower_rows(ann, scopes["balanced_panel"], bmf, fs, pt, nonbmf, panel, {e: panel[e]["name"] for e in panel})
    write_csv(OUT, conc + gr, FIELDS)

    elig = sum(1 for d in recipient_panel(ann, scopes["balanced_panel"]).values()
               if sum(d["fy"].get(y, 0.0) for y in P2) >= FLOOR)
    tops = lambda keys, fy, n: [(k, round(v), bmf.get(k, {}).get("bmf_name", "")) for k, v in sorted(  # noqa: E731
        totals_by_key(tuple(r for kk in keys if kk[1] == fy for r in ann[kk] if not r["d2d"]), {}, {}).items(), key=lambda kv: -kv[1])[:n]]
    summary = {
        "sponsor_years_by_fy": {fy: sum(1 for k in sy if k[1] == fy) for fy in FYS},
        "itemising_loaded_by_fy": {fy: len(sponsors_by_fy[fy]) for fy in FYS},
        "load_problems": bad, "balanced_panel_sponsors": len(balanced),
        "not_in_balanced": sorted(panel[e]["name"] for e in set().union(*sponsors_by_fy.values()) - balanced),
        "daf_weight_coverage": {fy: f"{sum(1 for k in weights if k[1] == fy)}/{len(sponsors_by_fy[fy])}" for fy in FYS},
        "fs_set": len(fs), "cz_llc_eins": sorted(cz_eins), "lines_total": sum(len(v["lines"]) for v in good.values()),
        "concentration": [{k: r[k] for k in ("scope", "basis", "fiscal_year", "sponsor_years", "total_usd", "d2d_excluded_usd",
                                             "recipients", "top10_share", "top100_share", "top1000_share", "gini", "hhi", "top1_recipient")}
                          for r in conc],
        "top10_balanced_by_fy": {fy: tops(scopes["balanced_panel"], fy, 10) for fy in FYS},
        "growers": grower_summary(gr, elig),
    }
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1, default=str)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("concentration", "top10_balanced_by_fy")}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
