#!/usr/bin/env python3
"""Add faith DAF sponsors outside the top-50 frame to the church block and re-estimate the faith-sponsor share of
church DAF dollars (P-B4026-06-01).

Base study  scripts/mission_church_recipients.py (b4026-06, with its wave-35C corrections): the church block is every
            recipient whose first failing Charity Navigator rule in scripts/mission_recipient_basis_eligibility.py is
            `no_efiled_990_church` (BMF SUBSECTION 03, FOUNDATION 10, not a private foundation, not a national or
            processor panel sponsor, no 990/990-EZ/990-PF in the IRS TEOS index 2019-2026). Top-50 frame: 29,469
            recipients, $6,177.5m DAF-weighted, faith share 22.1% (block) and 25.7% (all church-coded).

Sponsor tiers (all FY2023-24, Schedule I Part II lines, totals rows dropped, DAF-to-DAF lines dropped, DAF-weighted):
  top50          the base frame (lines from the committed rcp/lines cache);
  panel_other    every other itemising DAFRC 2025 panel sponsor (lines from the q120201/lines cache, b40n1202-01);
  nonpanel_faith faith DAF sponsors that are not in the DAFRC panel at all (NCF affiliates, Jewish federations, Catholic
                 and Christian foundations). Candidates come from a BMF name rule (FAITH_NONPANEL_RX, minus
                 NONPANEL_EXCLUDE_RX for hospital, school and service names); a candidate is kept only if a FY2023-24
                 Form 990 in the TEOS index reports Schedule D DAF grants > 0 and itemises Schedule I. Returns are read
                 from the GivingTuesday mirror of IRS TEOS with the repo's own extract and line parsers.

Faith sponsors  panel: DAFRC subtype "Religiously-Affiliated", plus National / Community Foundation panel sponsors whose
                name matches FAITH_NAME_RX (adds Servant Foundation, as the base study did, The Signatry Charitable
                Trust and The Catholic Foundation of North Georgia). Non-panel: every kept candidate. Each is assigned
                christian / catholic / jewish / other_faith by name (FAITH_KIND). The base study's seven keep their
                base labels.

Weights   The b40n1202-01 rule (mission_non_top50_numerator.weight_fallback): sponsor-cost-structure.csv DAF share of
          grants, capped; else Schedule D DAF grants / Part IX line 1, capped; else 1.
Netting   As the base: annotate() marks lines to the grantor itself, whitelisted DAF sponsors (EIN or unique name) as
          DAF-to-DAF. Extension: lines to a kept non-panel faith sponsor are also netted (they are DAF-to-DAF transfers
          once those sponsors are in the frame). Church recipients are never sponsors, so netting changes only totals.

Scenarios  S0 top-50 (reproduces the base); S1 + panel faith sponsors outside the top 50; S2 + non-panel faith
           sponsors; S3 all panel sponsors + non-panel faith sponsors (the like-for-like frame: non-faith sponsors
           outside the top 50 are added too); S3p all panel sponsors without non-panel faith sponsors.

Pure functions; I/O only in load/fetch helpers and `main`. Stdlib only. The base scripts are imported, not modified.

Usage:
  python3 scripts/mission_faith_sponsors_outside.py . --np-cache NPCACHE --lines-cache-top50 RCP_LINES \
      --lines-cache Q120201_LINES --bmf-dir BMF --index-dir IRSDIR --outreach-dir OUTREACH --work DIR [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_church_recipients as mcr  # noqa: E402
import mission_daf_share_recipient_revenue as base  # noqa: E402
import mission_non_top50_numerator as ntn  # noqa: E402
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import drop_totals_rows  # noqa: E402
from mission_net_payout import fetch_extract, itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_basis_eligibility import load_bmf_extra, load_history, units_b  # noqa: E402
from mission_recipient_sectors import BMF_FILES, COST, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "faith-sponsors-church-dollars-2026-11-20.csv")
BLOCK = mcr.BLOCK
BASE_FAITH = {**{e: ("christian", n) for e, n in mcr.FAITH_CHRISTIAN.items()},
              **{e: ("jewish", n) for e, n in mcr.FAITH_JEWISH.items()}}
FAITH_NAME_RX = re.compile(r"\b(CHRISTIAN|CATHOLIC|JEWISH|SIGNATRY|SERVANT FOUNDATION|LUTHERAN|METHODIST|BAPTIST|"
                           r"PRESBYTERIAN|EPISCOPAL|MUSLIM|ISLAMIC|ARCHDIOCESE|DIOCESE)\b")
FAITH_NONPANEL_RX = re.compile(
    r"^(THE )?(NATIONAL CHRISTIAN (CHARITABLE )?FOUNDATION|NATL CHRISTIAN|NCF )|CHRISTIAN (COMMUNITY )?FOUNDATION|"
    r"JEWISH (COMMUNITY |COMMUNAL |ENDOWMENT )?(FOUNDATION|FEDERATION|FUND)|\bUJA\b|JEWISH UNITED FUND|UNITED JEWISH|"
    r"JEWISH PHILANTHROP|CATHOLIC (COMMUNITY |CHARITIES )?FOUNDATION|(METHODIST|LUTHERAN|BAPTIST|PRESBYTERIAN|"
    r"EPISCOPAL|MENNONITE|ADVENTIST|BRETHREN|NAZARENE|MUSLIM|ISLAMIC) (\w+ )?FOUNDATION")
NONPANEL_EXCLUDE_RX = re.compile(r"HOSPITAL|MEDICAL|HEALTH|COLLEGE|UNIVERSITY|SCHOOL|ACADEMY|SEMINARY|HOMES?\b|"
                                 r"HOME ATTENDANT|SENIOR|NURSING|RETIREMENT|VILLAGE|CEMETER|MUSEUM|CAMP\b")
FAITH_KIND = (("jewish", re.compile(r"JEWISH|\bUJA\b|HEBREW|ISRAEL|TORAH|\bOJC\b|AGUDATH|MOSDOT|EMANU|CONGREGATION|"
                                    r"LEVY FAMILY CAMPUS")),
              ("catholic", re.compile(r"CATHOLIC|ARCHDIOCESE|DIOCESE|KNIGHTS OF COLUMBUS")),
              ("other_faith", re.compile(r"MUSLIM|ISLAMIC")))
GROUPS = ("faith_christian", "faith_catholic", "faith_jewish", "faith_other_faith", "national", "community_foundation",
          "other")
FAITH_GROUPS = frozenset(g for g in GROUPS if g.startswith("faith_"))
SCENARIOS = (("S0_top50", frozenset({"top50"}), "faith_only_outside"),
             ("S1_top50_plus_panel_faith", frozenset({"top50", "panel_other"}), "faith_only_outside"),
             ("S2_top50_plus_all_faith", frozenset({"top50", "panel_other", "nonpanel_faith"}), "faith_only_outside"),
             ("S3p_all_panel", frozenset({"top50", "panel_other"}), "all"),
             ("S3_all_panel_plus_nonpanel_faith", frozenset({"top50", "panel_other", "nonpanel_faith"}), "all"))
UA = "research-script/1.0"
SRC = ("IRS Form 990 Schedule I Part II FY2023-24 (GivingTuesday mirror of IRS TEOS e-file XML, "
       "gt990datalake-rawdata.s3.amazonaws.com; index apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv), net of "
       "DAF-to-DAF, DAF-weighted. Sponsor types: DAFRC Annual DAF Report 2025 dataset (dafresearchcollaborative.org). "
       "Church status: IRS EO BMF FOUNDATION 10 (www.irs.gov/pub/foia/ig/tege/eo-info.pdf).")
FIELDS = ("section", "scenario", "key", "label", "detail", "tier", "sponsor_group", "recipients", "lines",
          "usd_daf_weighted", "usd_schedule_i", "share", "value", "note", "source")


# ----------------------------------------------------------------------------- pure: classification
def faith_kind(name: str) -> str:
    u = name.upper()
    return next((k for k, rx in FAITH_KIND if rx.search(u)), "christian")


def panel_faith(panel: Mapping, dafrc_last: Mapping) -> dict:
    """panel EIN -> (kind, rule) for faith sponsors in the DAFRC panel."""
    def rule(e):
        r = dafrc_last.get(e, {})
        if e in BASE_FAITH:
            return "base_study"
        if r.get("subtype") == "Religiously-Affiliated":
            return "dafrc_religiously_affiliated"
        if r.get("type") in ("National", "Community Foundation") and FAITH_NAME_RX.search(panel[e]["name"].upper()):
            return "name_rule"
        return ""
    tagged = ((e, rule(e)) for e in panel)
    return {e: ((BASE_FAITH[e][0] if e in BASE_FAITH else faith_kind(panel[e]["name"])), r) for e, r in tagged if r}


def sponsor_group(e: str, panel: Mapping, faith: Mapping) -> str:
    if e in faith:
        return "faith_" + faith[e][0]
    seg = panel[e]["segment"] if e in panel else ""
    return {"national": "national", "community_foundation": "community_foundation"}.get(seg, "other")


def nonpanel_candidates(bmf_rows: Sequence[Mapping], panel_eins: frozenset) -> dict:
    return {r["ein"]: r for r in bmf_rows
            if r["subsection"] == "03" and r["ein"] not in panel_eins and FAITH_NONPANEL_RX.search(r["name"].upper())
            and not NONPANEL_EXCLUDE_RX.search(r["name"].upper())}


def pick_index_returns(rows: Sequence[Mapping]) -> dict:
    """(ein, fy) -> latest-object-id Form 990 per tax period, latest period per FY (FY = year the period ends)."""
    per = {k: max(v, key=lambda r: r["oid"]) for k, v in _group_by_fast(rows, lambda r: (r["ein"], r["tax_period"])).items()}
    by = _group_by_fast(per.values(), lambda r: (r["ein"], int(r["tax_period"][:4])))
    return {k: max(v, key=lambda r: (r["tax_period"], r["oid"])) for k, v in by.items() if k[1] in FYS}


def flat_lines(ann: Mapping, weights: Mapping, tiers: Mapping, extra_d2d: frozenset) -> tuple[dict, ...]:
    """Non-DAF-to-DAF positive lines. `to_np` flags lines to a kept non-panel faith sponsor, netted only in scenarios
    that include that tier (so S0 reproduces the base frame exactly)."""
    return tuple({"rec": r["ein"], "sponsor": k[0], "fy": k[1], "tier": tiers[k], "si": r["amount"],
                  "dw": r["amount"] * weights.get(k, 1.0), "to_np": r["ein"] in extra_d2d}
                 for k, rs in ann.items() for r in rs if not r["d2d"] and r["amount"] > 0)


def in_scenario(l: Mapping, tiers: frozenset, mode: str, faith: Mapping) -> bool:
    return (l["tier"] in tiers and (mode == "all" or l["tier"] == "top50" or l["sponsor"] in faith)
            and not (l["to_np"] and "nonpanel_faith" in tiers))


# ----------------------------------------------------------------------------- pure: rows
def mk(section, scenario, key, label="", detail="", tier="", group="", recipients="", lines="", dw="", si="", share="",
       value="", note=""):
    r = lambda x, n=0: round(x, n) if isinstance(x, float) else x  # noqa: E731
    return {"section": section, "scenario": scenario, "key": key, "label": label, "detail": detail, "tier": tier,
            "sponsor_group": group, "recipients": recipients, "lines": lines, "usd_daf_weighted": r(dw),
            "usd_schedule_i": r(si), "share": r(share, 5), "value": r(value, 5) if isinstance(value, float) else value,
            "note": note, "source": SRC}


def scope_rows(scn: str, scope: str, ls: Sequence[Mapping], frame_dw: float) -> list:
    tot = sum(l["dw"] for l in ls)
    recs = {l["rec"] for l in ls}
    by_g = _group_by_fast(ls, lambda l: l["group"])
    by_t = _group_by_fast(ls, lambda l: l["tier"])
    faith = sum(l["dw"] for l in ls if l["group"] in FAITH_GROUPS)
    head = [mk(f"{scope}:summary", scn, "recipients", recipients=len(recs), value=len(recs)),
            mk(f"{scope}:summary", scn, "usd_daf_weighted", dw=tot, si=sum(l["si"] for l in ls), value=tot),
            mk(f"{scope}:summary", scn, "share_of_frame_dw", value=tot / frame_dw if frame_dw else "",
               note="denominator: all non-DAF-to-DAF DAF-weighted $ of the scenario's sponsors (incl. blank-EIN lines)"),
            mk(f"{scope}:summary", scn, "faith_share", dw=faith, share=faith / tot if tot else "", value=faith / tot if tot else "",
               note="share of the scope's DAF-weighted $ sent by faith sponsors")]
    grp = [mk(f"{scope}:sponsor_group", scn, g, group=g, recipients=len({l["rec"] for l in v}), lines=len(v),
              dw=sum(l["dw"] for l in v), si=sum(l["si"] for l in v), share=sum(l["dw"] for l in v) / tot,
              value=sum(l["dw"] for l in v) / tot, note="value = group's share of the scope's DAF-weighted $")
           for g in GROUPS for v in [by_g.get(g, ())] if v]
    tie = [mk(f"{scope}:sponsor_tier", scn, t, tier=t, recipients=len({l["rec"] for l in v}), lines=len(v),
              dw=sum(l["dw"] for l in v), si=sum(l["si"] for l in v), share=sum(l["dw"] for l in v) / tot,
              value=sum(l["dw"] for l in v) / tot)
           for t in ("top50", "panel_other", "nonpanel_faith") for v in [by_t.get(t, ())] if v]
    return head + grp + tie


def sponsor_rows(scn: str, block_ls: Sequence[Mapping], own: Mapping, names: Mapping, faith: Mapping,
                 rule: Mapping, block_tot: float) -> list:
    by = _group_by_fast(block_ls, lambda l: l["sponsor"])
    ordered = sorted(by.items(), key=lambda kv: -sum(l["dw"] for l in kv[1]))
    return [mk("block:sponsor", scn, e, names.get(e, ""), f"faith rule: {rule.get(e, '-')}", v[0]["tier"], v[0]["group"],
               len({l["rec"] for l in v}), len(v), sum(l["dw"] for l in v), sum(l["si"] for l in v),
               sum(l["dw"] for l in v) / block_tot, (sum(l["dw"] for l in v) / own[e]) if own.get(e) else "",
               "value = share of this sponsor's own DAF-weighted non-DAF-to-DAF $ that goes to the church block")
            for e, v in ordered if v[0]["tier"] != "top50" or e in faith]


# ----------------------------------------------------------------------------- I/O
def load_bmf_rows(bmf_dir: str, keep) -> tuple[dict, ...]:
    def rows(f):
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            return ()
        with open(p, encoding="latin-1", newline="") as fh:
            return tuple({"ein": ein9(r["EIN"]), "name": (r.get("NAME") or "").strip(), "city": (r.get("CITY") or "").strip(),
                          "state": (r.get("STATE") or "").strip(), "subsection": (r.get("SUBSECTION") or "").strip(),
                          "foundation": (r.get("FOUNDATION") or "").strip(), "revenue": r.get("REVENUE_AMT") or ""}
                         for r in csv.DictReader(fh) if keep(r))
    return tuple(x for f in BMF_FILES for x in rows(f))


def index_990s(index_dir: str, eins: frozenset, years=(2023, 2024, 2025, 2026)) -> tuple[dict, ...]:
    def rows(y):
        p = os.path.join(index_dir, f"index_{y}.csv")
        if not os.path.exists(p):
            return ()
        with open(p, encoding="utf-8", errors="replace", newline="") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "oid": d["OBJECT_ID"], "index_year": y,
                          "name": d.get("TAXPAYER_NAME", "")}
                         for d in csv.DictReader(fh)
                         if (d.get("DLN") or "")[:5] == "93493" and ein9(d.get("EIN", "")) in eins
                         and (d.get("TAX_PERIOD") or "")[:4] in ("2023", "2024"))
    return tuple(r for y in years for r in rows(y))


def robots_log(work: str) -> dict:
    url = XML_URL.format(oid="202301949349301960")
    ok, why = mcr.robots_ok(url)
    os.makedirs(os.path.join(work, "robots"), exist_ok=True)
    with open(os.path.join(work, "robots", "log.tsv"), "a", encoding="utf-8") as fh:
        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{url.split('/')[2]}\t{why}\t{'allowed' if ok else 'blocked'}\n")
    return {"host": url.split("/")[2], "robots": why, "allowed": ok}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache-top50", required=True)
    ap.add_argument("--lines-cache", required=True, help="q120201 line cache (non-top-50 panel sponsor-years)")
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--index-dir", required=True)
    ap.add_argument("--outreach-dir", required=True)
    ap.add_argument("--work", required=True, help="cache for non-panel extracts and lines")
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    robots = robots_log(a.work) if a.fetch else {"skipped": "no --fetch"}
    if a.fetch and not robots["allowed"]:
        raise SystemExit("robots.txt disallows the mirror")

    dafrc = read_csv(DAFRC_CSV)
    dafrc_last = {ein9(r["ein"]): r for r in sorted(dafrc, key=lambda r: r["fiscal_year_end"])}
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    faith_p = panel_faith(panel, dafrc_last)

    # panel sponsor-years (as b40n1202-01)
    sy = ntn.sponsor_years(pick_returns(load_np(a.np_cache)), panel, rank)
    item = {k: v for k, v in sy.items() if v["pre"] == "itemised"}
    keys = sorted(item)
    loaded = {k: load_lines(item[k]["x"]["oid"], item[k]["x"]["sched_i_lines"],
                            a.lines_cache_top50 if item[k]["tier"] == "top50" else a.lines_cache, [], False) for k in keys}
    good_p = {k: drop_totals_rows(v) for k, v in loaded.items() if v["status"] == "ok"}
    tiers_p = {k: ("top50" if item[k]["tier"] == "top50" else "panel_other") for k in good_p}

    # non-panel faith candidates
    cand = nonpanel_candidates(load_bmf_rows(a.bmf_dir, lambda r: (r.get("SUBSECTION") or "").strip() == "03"
                                             and FAITH_NONPANEL_RX.search((r.get("NAME") or "").upper())),
                               frozenset(panel))
    picks = pick_index_returns(index_990s(a.index_dir, frozenset(cand)))
    pk = sorted(picks)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        sd = dict(zip(pk, ex.map(lambda k: fetch_extract(picks[k]["oid"], a.work, a.fetch, frozenset(), {}, False), pk)))
    daf_keys = [k for k in pk if sd[k].get("xml_status") == "ok" and (sd[k].get("sched_d_daf_grants") or 0) > 0]
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        full = dict(zip(daf_keys, ex.map(lambda k: fetch_extract(picks[k]["oid"], a.work, a.fetch, frozenset(), {}, True),
                                         daf_keys)))
    np_item = {k: x for k, x in full.items() if x.get("xml_status") == "ok" and (x.get("sched_i_lines") or 0) > 0 and itemized(x)}
    nk = sorted(np_item)
    lc = os.path.join(a.work, "lines")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        np_loaded = dict(zip(nk, ex.map(lambda k: load_lines(np_item[k]["oid"] if "oid" in np_item[k] else picks[k]["oid"],
                                                             np_item[k]["sched_i_lines"], lc, [], a.fetch), nk)))
    good_n = {k: drop_totals_rows(v) for k, v in np_loaded.items() if v["status"] == "ok"}
    np_faith = {e: (faith_kind(cand[e]["name"]), "nonpanel_bmf_name_and_sched_d") for e in {k[0] for k in good_n}}
    faith = {**faith_p, **np_faith}
    names = {**{e: p["name"] for e, p in panel.items()}, **{e: cand[e]["name"] for e in np_faith}}

    # annotate, weight, net (as the base; non-panel faith sponsors added to the netting set)
    good = {**good_p, **good_n}
    tiers = {**tiers_p, **{k: "nonpanel_faith" for k in good_n}}
    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    wgroups = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in wgroups.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    sy_all = {**{k: item[k] for k in good_p}, **{k: {"x": np_item[k]} for k in good_n}}
    weights, wsrc = ntn.weight_fallback(base.sponsor_weights(read_csv(COST), good), sy_all, 1.0)
    flat = flat_lines(ann, weights, tiers, frozenset(np_faith))
    flat = tuple({**l, "group": sponsor_group(l["sponsor"], panel, faith)} for l in flat)

    # recipients: church status and filing history over the union
    rec_eins = frozenset(l["rec"] for l in flat if l["rec"])
    bmf = base.load_bmf(a.bmf_dir, rec_eins)
    extra = load_bmf_extra(a.bmf_dir, frozenset(bmf))
    hist = load_history(a.index_dir, rec_eins)
    church = frozenset(e for e, b in bmf.items() if b["foundation"] == "10")
    nums_stub = {e: {"fy": {}, "grantors": set()} for e in church}
    reason = {u["key"]: u["reason"] for u in units_b(nums_stub, {}, bmf, extra, hist, panel)}
    block = frozenset(e for e in church if reason.get(e) == BLOCK)

    # recipient type (base name rules + Outreach 100 override, as in the base study)
    info = {r["ein"]: r for r in load_bmf_rows(a.bmf_dir, lambda r: ein9(r["EIN"]) in church)}
    dw_by = {e: sum(l["dw"] for l in v) for e, v in _group_by_fast((l for l in flat if l["rec"] in church),
                                                                   lambda l: l["rec"]).items()}
    outreach = mcr.read_outreach(a.outreach_dir, mcr.OUTREACH_YEARS)
    out_rows = tuple(r for y in mcr.OUTREACH_YEARS for r in outreach[y])

    def rtypes(eins, dw_map):
        cands = tuple({**info[e], "tokens": mcr.norm_tokens(info[e]["name"]), "dw": dw_map.get(e, 0.0)} for e in eins if e in info)
        mega = frozenset(x["match"]["ein"] for x in mcr.match_outreach(out_rows, cands) if x["match"])
        return {c["ein"]: mcr.rtype_of(c["name"], c["ein"] in mega) for c in cands}

    out, diag = [], {}
    for scn, tset, mode in SCENARIOS:
        ls = tuple(l for l in flat if in_scenario(l, tset, mode, faith))
        frame_dw = sum(l["dw"] for l in ls)
        own = {e: sum(l["dw"] for l in v) for e, v in _group_by_fast(ls, lambda l: l["sponsor"]).items()}
        bl = tuple(l for l in ls if l["rec"] in block)
        sdw = {e: sum(l["dw"] for l in v) for e, v in _group_by_fast(bl, lambda l: l["rec"]).items()}
        rt = rtypes(frozenset(sdw), sdw)
        cong = tuple(l for l in bl if rt.get(l["rec"]) == "congregation")
        cc = tuple(l for l in ls if l["rec"] in church)
        btot = sum(l["dw"] for l in bl)
        out += (scope_rows(scn, "block", bl, frame_dw) + scope_rows(scn, "block_congregations", cong, frame_dw)
                + scope_rows(scn, "church_coded_all", cc, frame_dw)
                + [mk("frame:sponsor_group", scn, g, group=g, dw=v, share=v / frame_dw, value=v / frame_dw,
                      note="group's share of all the scenario's DAF-weighted $")
                   for g in GROUPS for v in [sum(l["dw"] for l in ls if l["group"] == g)] if v]
                + sponsor_rows(scn, bl, own, names, faith, {e: r for e, (_, r) in faith.items()}, btot)
                + [mk("block:rtype_x_faith", scn, f"{t}|{'faith' if f else 'non_faith'}|{tier}", tier=tier,
                      recipients=len({l["rec"] for l in v}), lines=len(v), dw=sum(l["dw"] for l in v),
                      share=sum(l["dw"] for l in v) / btot, value=sum(l["dw"] for l in v) / btot,
                      note="recipient type (base name rules) x faith sponsor flag x sponsor tier; value = share of block $")
                   for (t, f, tier), v in sorted(_group_by_fast(bl, lambda l: (rt.get(l["rec"], "unclassified"),
                                                                               l["group"] in FAITH_GROUPS, l["tier"])).items())]
                + [mk("block:top_recipient_outside_faith", scn, e, info[e]["name"], f"{info[e]['city']}, {info[e]['state']}; {rt.get(e, '')}",
                      recipients=1, lines=len(v), dw=sum(l["dw"] for l in v), share=sum(l["dw"] for l in v) / btot,
                      value=sdw[e], note="dw = $ from faith sponsors outside the top 50; value = recipient's total block $ in this scenario")
                   for e, v in sorted(_group_by_fast((l for l in bl if l["tier"] != "top50" and l["group"] in FAITH_GROUPS),
                                                     lambda l: l["rec"]).items(), key=lambda kv: -sum(l["dw"] for l in kv[1]))[:30]])
        fs = lambda xs: (sum(l["dw"] for l in xs if l["group"] in FAITH_GROUPS) / sum(l["dw"] for l in xs)) if xs else None  # noqa: E731
        diag[scn] = {"block_recipients": len(sdw), "block_dw": round(btot), "frame_dw": round(frame_dw),
                     "faith_share_block": fs(bl), "faith_share_congregations": fs(cong), "faith_share_church_coded": fs(cc),
                     "national_share_block": sum(l["dw"] for l in bl if l["group"] == "national") / btot,
                     "national_share_congregations": sum(l["dw"] for l in cong if l["group"] == "national") / sum(l["dw"] for l in cong),
                     "faith_share_frame": sum(l["dw"] for l in ls if l["group"] in FAITH_GROUPS) / frame_dw,
                     "congregation_recipients": len({l["rec"] for l in cong}), "congregation_dw": round(sum(l["dw"] for l in cong))}

    # sponsor register: every faith sponsor considered, with status
    np_status = [mk("sponsor_register", "", e, cand[e]["name"], f"{cand[e]['city']}, {cand[e]['state']}; BMF FOUNDATION {cand[e]['foundation']}",
                    "nonpanel_candidate", "faith_" + faith_kind(cand[e]["name"]),
                    value=("kept" if e in np_faith else "no_sched_i_lines_or_not_itemised" if any(k[0] == e for k in daf_keys)
                           else "no_daf_grants_on_sched_d" if any(k[0] == e and sd[k].get("xml_status") == "ok" for k in pk)
                           else "xml_not_read" if any(k[0] == e for k in pk) else "no_fy2023_24_990_in_index"),
                    note="; ".join(f"FY{k[1]} oid {picks[k]['oid']} schedD_daf_grants {sd[k].get('sched_d_daf_grants')} "
                                   f"w {weights.get(k, '') if k in good_n else ''} ({wsrc.get(k, '') if k in good_n else ''})"
                                   for k in pk if k[0] == e))
                 for e in sorted({k[0] for k in pk})]
    p_status = [mk("sponsor_register", "", e, panel[e]["name"], dafrc_last.get(e, {}).get("type", "") + " / " + dafrc_last.get(e, {}).get("subtype", ""),
                   "top50" if e in rank else "panel_other", "faith_" + faith[e][0], value=faith[e][1],
                   note="sponsor-years with lines: " + str(sum(1 for k in good_p if k[0] == e)))
                for e in sorted(faith_p)]
    write_csv(a.out, out + p_status + np_status, FIELDS)

    print(json.dumps({
        "robots": robots, "panel_faith": {r: len(v) for r, v in _group_by_fast(faith_p.items(), lambda kv: kv[1][1]).items()},
        "panel_sponsor_years_with_lines": {t: sum(1 for k in good_p if tiers_p[k] == t) for t in ("top50", "panel_other")},
        "panel_faith_sponsor_years_outside_top50": sum(1 for k in good_p if tiers_p[k] == "panel_other" and k[0] in faith_p),
        "nonpanel": {"bmf_candidates": len(cand), "candidates_with_fy_990": len({k[0] for k in pk}), "returns": len(pk),
                     "extract_status": {s: len(v) for s, v in _group_by_fast(sd.values(), lambda x: x.get("xml_status")).items()},
                     "returns_with_daf_grants": len(daf_keys), "returns_itemised": len(nk),
                     "line_status": {s: len(v) for s, v in _group_by_fast(np_loaded.values(), lambda x: x["status"]).items()},
                     "sponsors_kept": len(np_faith), "weight_source": {s: sum(1 for k in good_n if wsrc[k] == s) for s in set(wsrc.values())}},
        "block_union": len(block), "church_union": len(church), "scenarios": diag}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
