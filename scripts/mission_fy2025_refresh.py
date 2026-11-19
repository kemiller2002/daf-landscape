#!/usr/bin/env python3
"""FY2025 filing refresh for the 1,512 DAFRC sponsors (queue item P-GAP19-01).

Stdlib only; functional style (pure transforms, I/O at the edges). The parsing, league-table, R5-netting and vendor
rules are the repository's own functions, imported unchanged:
  * scripts/mission_990_contractors.py  return selection, Part VII-B / Schedule D extract, vendor normaliser
  * scripts/mission_net_payout.py       Schedule I extract (every line to a DAFRC panel EIN), itemisation test
  * scripts/mission_league_table.py     build() (ranks, shares, CRn/HHI, FY2025 coverage and churn rows)
  * scripts/mission_market_netting.py   R5 whitelist, weights and caps (applied to the FY2025 label only)

Steps
  1. locate   every Form 990 whose tax period ends in 2025 (FY2025, DAFRC convention) for the FY2024 DAFRC sponsors,
              in IRS TEOS index_2025.csv + index_2026.csv; newest OBJECT_ID per tax period (amended supersedes).
  2. harvest  each return once: --local-xml-dir members first (IRS TEOS monthly zips, extracted beforehand), else the
              GivingTuesday per-object mirror. Two extracts are cached per object id in --work:
              extract990/{oid}.json (contractors + Schedule D) and netpayout990/{oid}.json (Schedule I, full).
  3. assemble the -fy2025-refresh outputs, compared with the as-built FY2025 inputs
              (form990-returns-schedule-d-harvest-full.csv FY2025 rows + form990-harvest-2026-fill.csv).

FY2025 values are filed and uncorrected; shares, CRs, HHI and R5 are over covered filers only and are never
extrapolated to the market.

Usage
  python3 scripts/mission_fy2025_refresh.py --irs-dir IRS --work WORK [--fetch] \
      [--local-xml-dir 2026_TEOS_XML_10A=DIR ...] [--index-lastmod 2025=2026-01-21,2026=2026-11-18]
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as cn  # noqa: E402
import mission_league_table as lt  # noqa: E402
import mission_market_netting as mn  # noqa: E402
import mission_net_payout as npo  # noqa: E402
from mission_990_contractors import DATA, _group_by_fast, ein9, fmt, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import load_np, pick_returns  # noqa: E402

FY = 2025
REN = "Ren (incl. Stellar/iPhi)"
NAMED = (REN, "Give Interactive", "Foundation Source", "Foundant Technologies")
SD = ("sched_d_daf_count", "sched_d_daf_contributions", "sched_d_daf_grants", "sched_d_daf_eoy_value")
TEOS_ZIP = "https://apps.irs.gov/pub/epostcard/990/xml/2026/{z}.zip#{oid}_public.xml"
OUT = {"harvest": "form990-harvest-fy2025-refresh.csv", "league": "daf-sponsor-league-table-fy2025-refresh.csv",
       "conc": "daf-concentration-fy2025-refresh.csv", "net": "dafrc-market-totals-netted-fy2025-refresh.csv",
       "contractors": "form990-contractors-fy2025-refresh.csv", "vendors": "vendor-footprint-990-fy2025-refresh.csv"}
SRC_H = "form990-harvest-fy2025-refresh.csv (FY2025 returns in IRS index_2025 + index_2026)"


# ----------------------------------------------------------------------------- 1. locate
def read_batches(irs_dir: str) -> dict:
    import csv
    with open(os.path.join(irs_dir, "index_2026.csv"), newline="", encoding="latin-1") as fh:
        return {d["OBJECT_ID"]: d.get("XML_BATCH_ID", "") for d in csv.DictReader(fh)}


def locate(irs_dir: str, targets: Mapping) -> tuple[dict, ...]:
    idx = cn.load_index([os.path.join(irs_dir, f"index_{y}.csv") for y in (2025, 2026)], frozenset(targets))
    return tuple({**targets[e], **f} for e in targets for f in cn.latest_per_period(idx.get(e, ()), (FY,)))


# ----------------------------------------------------------------------------- 2. harvest
def cache_paths(work: str, oid: str) -> tuple[str, str]:
    return os.path.join(work, "extract990", f"{oid}.json"), os.path.join(work, "netpayout990", f"{oid}.json")


def save(path: str, d: Mapping) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(d, fh)


def parse_file(fp: str, oid: str, src: str, url: str, work: str, eins: frozenset, names: Mapping) -> str:
    with open(fp, "rb") as fh:
        a = cn.extract_stream(fh)
    with open(fp, "rb") as fh:
        b = npo.extract_stream(fh, eins, names, True)
    p1, p2 = cache_paths(work, oid)
    save(p1, {**a, "xml_status": "ok", "_v": cn.EXTRACT_VERSION, "xml_url": url, "xml_source": src,
              "contractors": [dict(c) for c in a.get("contractors", ())]})
    save(p2, {**b, "xml_status": "ok", "_v": npo.EXTRACT_VERSION, "xml_url": url, "xml_source": src})
    return "ok"


def harvest_one(oid: str, work: str, fetch: bool, local: Mapping, eins: frozenset, names: Mapping) -> str:
    p1, p2 = cache_paths(work, oid)
    if os.path.exists(p1) and os.path.exists(p2):
        with open(p1, encoding="utf-8") as fh:
            if json.load(fh).get("xml_status") == "ok":
                return "cached_ok"
    lp = next(((z, os.path.join(d, f"{oid}_public.xml")) for z, d in local.items()
               if os.path.exists(os.path.join(d, f"{oid}_public.xml"))), None)
    if lp:
        return parse_file(lp[1], oid, "teos_zip", TEOS_ZIP.format(z=lp[0], oid=oid), work, eins, names)
    if not fetch:
        return "not_fetched"
    url, tmp = cn.XML_URL.format(oid=oid), os.path.join(work, "xmltmp", f"{oid}.xml")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    err = "error"
    for att in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as fh:
                shutil.copyfileobj(r, fh, 1 << 20)
            return parse_file(tmp, oid, "gt_mirror", url, work, eins, names)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                save(p1, {"xml_status": f"http_{e.code}", "_v": cn.EXTRACT_VERSION, "xml_url": url, "contractors": []})
                return f"http_{e.code}"
            err = f"http_{e.code}"
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            err = f"error:{type(e).__name__}"
            time.sleep(3 * (att + 1))
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
    return err


# ----------------------------------------------------------------------------- 3. assemble (pure given inputs)
def prior_status(oid: str, ein: str, prior25: Mapping, fill: Mapping, prior_eins: set) -> str:
    if oid in prior25 and prior25[oid]["xml_status"] == "ok":
        return "in_prior_harvest_ok"
    if oid in fill:
        return "in_prior_2026_fill"
    return "new_since_prior_supersedes_earlier_fy2025_return" if ein in prior_eins else "new_since_prior_ein_new_to_fy2025"


def prior_check(oid: str, x: Mapping, prior25: Mapping, fill: Mapping) -> str:
    p = prior25[oid] if oid in prior25 and prior25[oid]["xml_status"] == "ok" else fill.get(oid)
    if not p:
        return ""
    return "match" if all((num(p[k]) or 0) == (x.get(k) or 0) for k in SD) else "differs"


def harvest_rows(loc, ex, npx, batch, lastmod, prior25, fill, dkey):
    prior_eins = {ein9(r["ein"]) for r in prior25.values() if r["xml_status"] == "ok"} | {ein9(r["ein"]) for r in fill.values()}

    def one(l):
        oid, x, n = l["object_id"], ex[l["object_id"]], npx.get(l["object_id"], {})
        filing = {k: l[k] for k in ("ein", "tax_period", "object_id", "return_type", "taxpayer_name", "index_url")}
        r = cn.return_row(l, filing, x, dkey)
        return {**r, "xml_url": x.get("xml_url") if x.get("xml_source") == "teos_zip" else cn.XML_URL.format(oid=oid),
                "xml_source": x.get("xml_source", ""), "xml_batch_id": batch.get(oid, ""), "index_year": l["index_year"],
                "index_last_modified": lastmod.get(l["index_year"], ""),
                "prior_status": prior_status(oid, l["ein"], prior25, fill, prior_eins),
                "prior_values_check": prior_check(oid, x, prior25, fill),
                "sched_d_other_funds_count": x.get("sched_d_other_funds_count"),
                "sched_d_other_funds_eoy_value": x.get("sched_d_other_funds_eoy_value"),
                "part_ix_line1_grants_domestic_orgs": n.get("part_ix_line1_grants_domestic_orgs"),
                "sched_i_lines": n.get("sched_i_lines"), "sched_i_total": n.get("sched_i_total"),
                "sched_i_panel_lines": len(n.get("sched_i_panel_lines", ())) if n else None,
                "sched_i_itemised": int(npo.itemized(n)) if n else None}
    return tuple(one(l) for l in loc)


def netting_fy2025(dafrc_raw, f25, work):
    """R5 rule functions of mission_market_netting applied to FY2025 Schedule I lines. Market membership and caps use
    filed FY2025 Schedule D values of covered filers (there are no corrected FY2025 values)."""
    panel = npo.panel_from(dafrc_raw)
    corr = {**{(e, FY, "daf_grants"): (v["daf_grants"] or 0.0) for e, v in f25.items()},
            **{(e, FY, "daf_contributions"): (v["daf_contributions"] or 0.0) for e, v in f25.items()}}
    shares = mn.cost_shares(read_csv(mn.COST))
    seg_med = lambda seg, k: mn.med([mn.clip01(shares[e][k]) for e in panel if panel[e]["segment"] == seg  # noqa: E731
                                     and e in shares and shares[e][k] is not None]) or 1.0
    defaults = {k: {s: seg_med(s, k) for s in {p["segment"] for p in panel.values()}} for k in ("assets", "grants")}
    chosen = pick_returns(load_np(work))
    mn.FYS = (FY,)  # the batch-34 rule implementation, unchanged, on the FY2025 label
    lines = mn.panel_lines(chosen, panel)
    decision = {r: mn.recipient_decision(panel[r], shares.get(r)) for r in {l["recipient"] for l in lines}}
    wl = tuple({**l, "w": mn.weights(l, panel, decision, shares, defaults)} for l in lines)
    net = {t: mn.capped(wl, t, corr) for t in mn.TIERS}
    agg = lambda xs, side: {k: sum(x["net_amt"] for x in v) for k, v in _group_by_fast(xs, lambda x: x[side]).items()}  # noqa: E731
    pend = tuple(l for l in wl if l["w"]["central"] > 0 and corr.get((l["grantor"], FY, "daf_grants"), 0) > 0 and l["recipient"] not in f25)
    attach = sum(corr.get((g, FY, "daf_grants"), 0) for (g, _), x in chosen.items() if not npo.itemized(x))
    return {"panel": panel, "lines": lines, "net": net, "out": {t: agg(net[t], "grantor") for t in mn.TIERS},
            "in": {t: agg(net[t], "recipient") for t in mn.TIERS}, "pending": pend, "attach": attach, "chosen": chosen}


def net_rows(nt, cov_g, cov_c):
    def one(m, cv, t):
        xs = nt["net"][t]
        n = sum(x["net_amt"] for x in xs)
        return {"fiscal_year": FY, "metric": m, "tier": t, "basis": "fy2025_filed_covered_only", "covered_filed_value": round(cv),
                "r5_netting_amount": round(n), "netted_value": round(cv - n), "netting_share_of_covered": n / cv,
                "weighted_before_caps": round(sum(x["w_amt"] for x in xs)), "gross_lines_in_tier": round(sum(x["amount"] for x in xs)),
                "lines": len(xs), "grantors": len({x["grantor"] for x in xs}), "recipients": len({x["recipient"] for x in xs}),
                "all_panel_lines_gross": round(sum(l["amount"] for l in nt["lines"])),
                "central_weighted_lines_to_recipients_not_yet_filed": round(sum(l["amount"] * l["w"]["central"] for l in nt["pending"])),
                "grantor_daf_grants_sched_i_not_itemised": round(nt["attach"]),
                "sources": "FY2025 Schedule I lines of the form990-harvest-fy2025-refresh.csv returns; scripts/mission_market_netting.py "
                           "rule functions; caps and membership on filed FY2025 Schedule D values of covered filers"}
    return tuple(one(m, cv, t) for m, cv in (("daf_grants", cov_g), ("daf_contributions", cov_c)) for t in mn.TIERS)


def netted_conc(nt, f25, ids, cov_g, cov_c, tier):
    tg, tc = cov_g - sum(x["net_amt"] for x in nt["net"][tier]), cov_c - sum(x["net_amt"] for x in nt["net"][tier])
    vg = {e: (v["daf_grants"] or 0) - nt["out"][tier].get(e, 0) for e, v in f25.items()}
    vc = {e: (v["daf_contributions"] or 0) - nt["in"][tier].get(e, 0) for e, v in f25.items()}

    def one(m, vals, tot):
        c = lt.conc(vals, tot)
        return {"fiscal_year": FY, "metric": m, "basis": f"fy2025_filed_covered_only_netted_r5_{tier}", "market_total": tot, **c,
                "top1_name": ids.get(c["top1_ein"], {}).get("name", ""), "source": "covered FY2025 filers; R5 rule functions on FY2025 Schedule I"}
    return (one("daf_grants", vg, tg), one("daf_contributions", vc, tc))


def league_rows(league_new, league_old, f25, nt, ng_tot):
    old25 = {r["ein"]: r for r in league_old if r["fiscal_year"] == FY}

    def change(r, o):
        if not o:
            return f"new_row:{r['row_type']}"
        if o["row_type"] != r["row_type"]:
            return f"{o['row_type']}->{r['row_type']}"
        return "unchanged" if o["fy2025_return_object_id"] == r["fy2025_return_object_id"] else "superseding_return"

    def one(r):
        e, v, o = r["ein"], f25.get(r["ein"]), old25.get(r["ein"])
        g = (v["daf_grants"] or 0) - nt["out"]["central"].get(e, 0) if v and v["daf_grants"] is not None else None
        return {**r, "daf_grants_netted_central": g, "share_daf_grants_netted_central": g / ng_tot if g is not None else None,
                "daf_contributions_netted_central": ((v["daf_contributions"] or 0) - nt["in"]["central"].get(e, 0))
                if v and v["daf_contributions"] is not None else None,
                "r5_outbound_central": nt["out"]["central"].get(e, 0.0) if v else None,
                "r5_inbound_central": nt["in"]["central"].get(e, 0.0) if v else None,
                "share_basis": r["share_basis"] + ("; netted share of the covered netted total" if v else ""),
                "as_built_row_type": o["row_type"] if o else "", "as_built_rank_assets": o["rank_assets"] if o else None,
                "as_built_daf_assets_eoy": o["daf_assets_eoy"] if o else None, "change_vs_as_built": change(r, o),
                "source": "IRS Form 990 Schedule D Part I as filed: " + SRC_H}
    return tuple(one(r) for r in league_new if r["fiscal_year"] == FY), tuple(o for e, o in old25.items()
                                                                              if e not in {r["ein"] for r in league_new if r["fiscal_year"] == FY})


def vend_stats(cs, fy=None):
    xs = [c for c in cs if fy is None or str(c["fiscal_year"]) == str(fy)]
    return {k: {"sponsors": sorted({ein9(c["ein"]) for c in v}), "comp": sum(num(c["compensation"]) or 0 for c in v),
                "lines": len(v), "category": v[0]["vendor_category"]} for k, v in _group_by_fast(xs, lambda c: c["vendor_group"]).items()}


def vendor_rows(con25, prior_con, fy25_eins, corr24, names, market24):
    v25, v25p, v24 = vend_stats(con25), vend_stats(prior_con, FY), vend_stats(prior_con, 2024)
    groups = sorted({k for k, v in {**v25, **v24}.items() if v["category"] in cn.DAF_VENDOR_CATEGORIES} | set(NAMED))
    a24 = lambda es: sum(corr24.get(e) or 0 for e in es)  # noqa: E731

    def one(g):
        n, p, o = v25.get(g, {}), v25p.get(g, {}), v24.get(g, {})
        s25, s24 = set(n.get("sponsors", ())), set(o.get("sponsors", ()))
        both = {e for e in s24 if e in fy25_eins}
        return {"vendor": g, "vendor_category": (n or o or {"category": ""})["category"],
                "fy2025_refresh_sponsors": len(s25), "fy2025_refresh_compensation": n.get("comp", 0), "fy2025_refresh_lines": n.get("lines", 0),
                "fy2025_refresh_payers_fy2024_corrected_assets": a24(s25),
                "fy2025_refresh_payers_share_of_fy2024_corrected_market": a24(s25) / market24,
                "fy2025_prior_harvest_sponsors": len(p.get("sponsors", ())), "fy2025_prior_harvest_compensation": p.get("comp", 0),
                "fy2024_sponsors": len(s24), "fy2024_compensation": o.get("comp", 0), "fy2024_payers_fy2024_corrected_assets": a24(s24),
                "fy2024_payers_with_fy2025_return_parsed": len(both), "fy2024_payers_named_again_fy2025": len(both & s25),
                "fy2024_payers_not_named_fy2025": " | ".join(sorted(names[e] for e in both - s25)),
                "fy2025_new_payers_vs_fy2024": " | ".join(sorted(names[e] for e in s25 - s24)),
                "fy2025_sponsors": " | ".join(sorted(names[e] for e in s25)),
                "source": "Part VII-B: FY2025 from " + OUT["contractors"] + "; FY2024 from form990-contractors-harvest-full.csv"}
    return tuple(sorted((one(g) for g in groups), key=lambda r: (-r["fy2025_refresh_sponsors"], -r["fy2025_refresh_compensation"])))


def ren_panel(prior_con, con25, prior_all, rows, corr24, dafrc24, names):
    allc = [c for c in prior_con if c["fiscal_year"] != str(FY)] + list(con25)
    by = _group_by_fast([c for c in allc if c["vendor_group"] == REN], lambda c: ein9(c["ein"]))
    latest = {}
    for r in [r for r in prior_all if r["xml_status"] == "ok" and r["fiscal_year"] != str(FY)] + [r for r in rows if r["xml_status"] == "ok"]:
        latest[ein9(r["ein"])] = max(latest.get(ein9(r["ein"]), 0), int(r["fiscal_year"]))
    in_latest = sorted(e for e, cs in by.items() if any(int(c["fiscal_year"]) == latest.get(e) for c in cs))
    fy25 = {r["ein"] for r in rows if r["xml_status"] == "ok"}
    panel = tuple({"ein": e, "sponsor": names[e], "fy2024_corrected_assets": corr24.get(e),
                   **{f"ren_fy{fy}": sum(num(c["compensation"]) or 0 for c in cs if int(c["fiscal_year"]) == fy) or None for fy in (2022, 2023, 2024, 2025)},
                   "entities": " | ".join(sorted({c["vendor_entity"] for c in cs})), "fy2025_return_parsed": e in fy25,
                   "latest_parsed_fy": latest.get(e), "named_in_latest_parsed_return": e in in_latest}
                  for e, cs in sorted(by.items(), key=lambda t: -(corr24.get(t[0]) or 0)))
    return {"any_year_sponsors": len(by), "any_year_assets_corrected_fy2024": sum(corr24.get(e) or 0 for e in by),
            "any_year_assets_dafrc_fy2024": sum(dafrc24.get(e, 0) for e in by),
            "latest_return_sponsors": len(in_latest), "latest_return_assets_corrected_fy2024": sum(corr24.get(e) or 0 for e in in_latest),
            "latest_return_assets_dafrc_fy2024": sum(dafrc24.get(e, 0) for e in in_latest), "panel": panel}


# ----------------------------------------------------------------------------- main
HF = (*cn.RETURN_FIELDS[:16], "xml_source", "xml_batch_id", "index_year", "index_last_modified", "prior_status", "prior_values_check",
      *cn.RETURN_FIELDS[16:31], "sched_d_other_funds_count", "sched_d_other_funds_eoy_value", "part_ix_line1_grants_domestic_orgs",
      "sched_i_lines", "sched_i_total", "sched_i_panel_lines", "sched_i_itemised", "fy2024_corrected_daf_assets", *cn.RETURN_FIELDS[31:])
LF = (*lt.FIELDS_L[:-2], "as_built_row_type", "as_built_rank_assets", "as_built_daf_assets_eoy", "change_vs_as_built", *lt.FIELDS_L[-2:])


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True, help="holds index_2025.csv and index_2026.csv")
    ap.add_argument("--work", required=True, help="extract cache (extract990/, netpayout990/)")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--local-xml-dir", action="append", default=[], help="ZIPNAME=DIR of extracted TEOS zip members")
    ap.add_argument("--index-lastmod", default="2025=2026-01-21,2026=2026-11-18")
    ap.add_argument("--out-dir", default=DATA)
    ap.add_argument("--summary-json", default="")
    a = ap.parse_args(argv)
    local = dict(x.split("=", 1) for x in a.local_xml_dir)
    lastmod = dict(x.split("=", 1) for x in a.index_lastmod.split(","))

    dafrc_raw, dafrc = read_csv(cn.DAFRC_CSV), cn.load_dafrc()
    targets = {t["ein"]: t for t in cn.select_targets(dafrc, 0)}
    loc = locate(a.irs_dir, targets)
    batch = read_batches(a.irs_dir)
    panel0 = npo.panel_from(dafrc_raw)
    eins0, names0 = frozenset(panel0), npo.name_map(panel0)
    with ThreadPoolExecutor(8) as pool:
        status = dict(zip((l["object_id"] for l in loc), pool.map(
            lambda l: harvest_one(l["object_id"], a.work, a.fetch, local, eins0, names0), loc)))
    load = lambda p: json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}  # noqa: E731
    ex = {o: load(cache_paths(a.work, o)[0]) for o in status}
    npx = {o: load(cache_paths(a.work, o)[1]) for o in status}

    prior_all = read_csv(os.path.join(DATA, "form990-returns-schedule-d-harvest-full.csv"))
    prior25 = {r["return_object_id"]: r for r in prior_all if r["fiscal_year"] == str(FY)}
    fill = {r["return_object_id"]: r for r in read_csv(lt.FILL)}
    dkey = {(r["ein"], r["fy"]): r for r in dafrc}
    rows = harvest_rows(loc, ex, npx, batch, lastmod, prior25, fill, dkey)
    rows_s = tuple({k: fmt(v) for k, v in r.items()} for r in rows if r["xml_status"] == "ok")

    items, totals, netted = read_csv(lt.CORR_ITEMS), read_csv(lt.CORR_TOTALS), read_csv(lt.NETTED)
    league_new, conc_new, check, churn_new, cov_new, tops, yv, ids, _ = lt.build(dafrc_raw, items, totals, netted, rows_s, (), None)
    league_old, conc_old, _, churn_old, cov_old, *_ = lt.build(dafrc_raw, items, totals, netted, read_csv(lt.HARVEST), read_csv(lt.FILL), None)
    assert all(v["match"] for v in check.values()), "corrected totals rebuild failed"
    corr24 = {e: v["daf_assets_eoy"] for e, v in yv[2024].items()}
    market24 = sum(v["daf_assets_eoy"] for v in yv[2024].values())
    rows = tuple({**r, "fy2024_corrected_daf_assets": corr24.get(r["ein"])} for r in rows)

    f25 = lt.fy2025_filed(rows_s, ())
    cov_g = sum(max(v["daf_grants"] or 0, 0) for v in f25.values())
    cov_c = sum(max(v["daf_contributions"] or 0, 0) for v in f25.values())
    nt = netting_fy2025(dafrc_raw, f25, a.work)
    nrows = net_rows(nt, cov_g, cov_c)
    conc25 = tuple(r for r in conc_new if r["fiscal_year"] == FY) + tuple(r for t in mn.TIERS for r in netted_conc(nt, f25, ids, cov_g, cov_c, t))
    league25, dropped = league_rows(league_new, league_old, f25, nt, cov_g - sum(x["net_amt"] for x in nt["net"]["central"]))

    con25 = tuple(c for r in rows if r["xml_status"] == "ok" for c in cn.contractor_rows(r, ex[r["return_object_id"]]))
    prior_con = read_csv(os.path.join(DATA, "form990-contractors-harvest-full.csv"))
    names = {e: t["sponsor_name"] for e, t in targets.items()}
    vrows = vendor_rows(con25, prior_con, {r["ein"] for r in rows if r["xml_status"] == "ok"}, corr24, names, market24)
    dafrc24 = {r["ein"]: num(r["eoy_daf_assets"]) or 0 for r in dafrc if r["fy"] == 2024}
    ren = ren_panel(prior_con, con25, prior_all, rows, corr24, dafrc24, names)

    out = lambda k: os.path.join(a.out_dir, OUT[k])  # noqa: E731
    write_csv(out("harvest"), sorted(rows, key=lambda r: (r["fy2024_asset_rank"], r["return_object_id"])), HF)
    write_csv(out("league"), league25, LF)
    write_csv(out("conc"), conc25, lt.FIELDS_C)
    write_csv(out("net"), nrows, tuple(nrows[0].keys()))
    write_csv(out("contractors"), sorted(con25, key=lambda r: (r["sponsor_name"], -(r["compensation"] or 0))), cn.HARVEST_FIELDS)
    write_csv(out("vendors"), vrows, tuple(vrows[0].keys()))

    panel = nt["panel"]
    pairs = sorted(((k, sum(x["net_amt"] for x in v)) for k, v in _group_by_fast(nt["net"]["central"], lambda x: (x["grantor"], x["recipient"])).items()),
                   key=lambda t: -t[1])[:10]
    keep = ("fy2025_sponsors_with_parsed_return", "fy2024_corrected_assets_covered_share", "fy2024_corrected_grants_covered_share",
            "fy2024_top50_with_fy2025_return", "fy2024_top50_assets_covered_share", "fy2024_top50_missing_fy2025",
            "fy2025_filed_totals_covered", "fy2024_top50_filers_same_sponsor_change", "fy2025_accounts_screened_out")
    summary = {
        "fetch_status": collections.Counter(status.values()), "located_fy2025_returns": len(rows), "eins": len({r["ein"] for r in rows}),
        "by_prior_status": collections.Counter(r["prior_status"] for r in rows), "by_source": collections.Counter(r["xml_source"] for r in rows),
        "prior_values_check": collections.Counter(r["prior_values_check"] for r in rows),
        "new_returns": [(r["ein"], r["sponsor_name"], r["tax_period_end"], r["return_ts"][:10], r["fy2024_asset_rank"], r["sched_d_daf_eoy_value"],
                         r["prior_status"]) for r in sorted(rows, key=lambda r: r["fy2024_asset_rank"]) if r["prior_status"].startswith("new")],
        "coverage_refresh": {k: cov_new[k] for k in keep}, "coverage_as_built": {k: cov_old[k] for k in keep},
        "churn_fy2025_refresh": churn_new[FY], "churn_fy2025_as_built": churn_old[FY],
        "league_changes": collections.Counter(r["change_vs_as_built"] for r in league25), "league_dropped": [o["name"] for o in dropped],
        "conc25": [(r["metric"], r["basis"], r["market_total"], r["cr1"], r["cr3"], r["cr5"], r["cr10"], r["cr50"], r["hhi"]) for r in conc25],
        "conc25_as_built": [(r["metric"], r["basis"], r["market_total"], r["cr5"], r["hhi"]) for r in conc_old if r["fiscal_year"] == FY],
        "netting": [{k: r[k] for k in r if k != "sources"} for r in nrows],
        "netting_top_pairs_central": [(panel[g]["name"], panel[r]["name"], round(v)) for (g, r), v in pairs],
        "netting_by_recipient_segment_central": {s: round(sum(x["net_amt"] for x in nt["net"]["central"] if panel[x["recipient"]]["segment"] == s))
                                                 for s in npo.SEGMENTS},
        "vendors_named": [r for r in vrows if r["vendor"] in NAMED], "ren": ren,
        "contractor_lines_fy2025_refresh": len(con25),
        "contractor_lines_fy2025_prior": sum(1 for c in prior_con if c["fiscal_year"] == str(FY))}
    txt = json.dumps(summary, indent=1, default=str)
    print(txt)
    if a.summary_json:
        with open(a.summary_json, "w", encoding="utf-8") as fh:
            fh.write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
