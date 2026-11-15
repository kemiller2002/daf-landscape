#!/usr/bin/env python3
"""Which charities and sectors receive DAF grants: top-50 DAF sponsors, FY2023-FY2024 (queue item P-NEW-RCP-01).

Universe and return choice are those of scripts/mission_daf_to_daf.py (top-50 DAFRC sponsors by FY2024 DAF assets;
one return per sponsor x fiscal year via mission_daf_to_daf.pick_returns over the netpayout990/ cache).
The netpayout990/ cache keeps only panel-recipient lines and the 25 largest lines, so this script re-reads the
same returns' Schedule I Part II in full (every RecipientTable line) from the IRS e-file XML. A local XML copy is
used only when it parses to the same line count as the cache; otherwise the GivingTuesday mirror of IRS TEOS is read.

Steps (pure transforms; I/O at the edges)
  1. Lines      every Schedule I Part II line: recipient EIN, name, state/country, IRC section, cash, non-cash.
  2. DAF-to-DAF lines to a recipient EIN whose decision is `include` in daf-to-daf-recipient-whitelist.csv
                (batch 34, P-NPO-04) are excluded, as are self-lines; a blank-EIN line is excluded when its
                normalised name matches exactly one whitelisted panel name.
  3. Sector     recipient EIN -> IRS EO BMF (eo1..eo4, eo_pr, eo_xx). NTEE_CD first letter -> NTEE major group.
                Fallbacks, flagged in `method`: BMF FOUNDATION code 10 (church) -> religion, 11 (school) ->
                education, 12 (hospital/medical research) -> health; then, for lines still unclassified,
                a recipient-name keyword rule (`name_rule`). Shares are reported on both bases.
  4. Shares     dollar shares by NTEE major group, for all top-50 itemising sponsors, by DAFRC segment and by
                sponsor; basis `schedule_i` (filed lines) and `daf_weighted` (each sponsor-year's lines x its
                DAF share of grants from sponsor-cost-structure.csv, capped at 1).
  5. Concentr.  distinct recipients, top-10 / top-100 recipient share, HHI (0-10,000) on recipient shares.

Stdlib only; functional style.

Usage:
  python3 scripts/mission_recipient_sectors.py --np-cache NPCACHE --bmf-dir BMF --lines-cache LC \
      [--xml-dir D ...] [--fetch]
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, XML_URL, _group_by_fast, ein9, local, num, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402

OUT = os.path.join(DATA, "daf-grant-recipient-sectors-top50.csv")
WHITELIST = os.path.join(DATA, "daf-to-daf-recipient-whitelist.csv")
COST = os.path.join(DATA, "sponsor-cost-structure.csv")
SVCF = "205205488"  # Silicon Valley Community Foundation (CZ Biohub lines dominate its FY2023 Schedule I)
BMF_FILES = ("eo1.csv", "eo2.csv", "eo3.csv", "eo4.csv", "eo_pr.csv", "eo_xx.csv")
LINES_V = 1
SOURCE = ("IRS Form 990 Schedule I Part II (e-file XML, GivingTuesday mirror of IRS TEOS), all lines; recipients "
          "joined to IRS EO BMF (www.irs.gov/pub/irs-soi/eo*.csv, Last-Modified 2026-11-09) NTEE_CD; DAF-to-DAF "
          "lines excluded via daf-to-daf-recipient-whitelist.csv; universe per mission_daf_to_daf.py")

MAJOR = {**{"A": "arts_culture"}, **{"B": "education"}, **{k: "environment_animals" for k in "CD"},
         **{k: "health" for k in "EFGH"}, **{k: "human_services" for k in "IJKLMNOP"}, **{"Q": "international"},
         **{k: "public_societal_benefit" for k in "RSTUVW"}, **{"X": "religion"}, **{"Y": "mutual_membership"},
         **{"Z": "unknown_z"}}
GROUPS = ("education", "religion", "human_services", "health", "arts_culture", "international", "environment_animals",
          "public_societal_benefit", "mutual_membership", "unknown_z", "unclassified")
FOUNDATION_FALLBACK = {"10": "religion", "11": "education", "12": "health"}
NAME_RULES = (
    ("religion", re.compile(r"\b(CHURCH|PARISH|DIOCESE|ARCHDIOCESE|MINISTR(Y|IES)|SYNAGOGUE|CONGREGATION|TEMPLE|"
                            r"CHABAD|MOSQUE|ISLAMIC CENTER|YESHIVA|BAPTIST|LUTHERAN|METHODIST|PRESBYTERIAN|"
                            r"EPISCOPAL|CATHOLIC|EVANGELICAL|BIBLE|GOSPEL|JESUIT|SOCIETY OF JESUS)\b")),
    ("education", re.compile(r"\b(UNIVERSITY|COLLEGE|SCHOOL|ACADEMY|PTA|PTO|SCHOOLS|INSTITUTE OF TECHNOLOGY)\b")),
    ("health", re.compile(r"\b(HOSPITAL|MEDICAL CENTER|HEALTH SYSTEM|CLINIC|CANCER|HOSPICE|BIOHUB|BIOLOGICAL|"
                          r"MEDICAL RESEARCH)\b")),
    ("human_services", re.compile(r"\b(FOOD BANK|FOOD PANTRY|SHELTER|YMCA|YWCA|BOYS AND GIRLS CLUB|HABITAT FOR "
                                  r"HUMANITY|SALVATION ARMY|RED CROSS|SCOUTS)\b")),
    ("arts_culture", re.compile(r"\b(MUSEUM|SYMPHONY|ORCHESTRA|OPERA|THEATRE|THEATER|BALLET|PUBLIC RADIO|LIBRARY)\b")),
    ("environment_animals", re.compile(r"\b(HUMANE SOCIETY|SPCA|ANIMAL|CONSERVANCY|WILDLIFE|ZOO|LAND TRUST|"
                                       r"ENVIRONMENTAL)\b")),
)


# ----------------------------------------------------------------------------- parse (streamed)
def line_of(el) -> list:
    g = {local(c.tag): c for c in el.iter()}
    t = lambda k: (g[k].text or "").strip() if k in g and g[k].text else ""  # noqa: E731
    name = " ".join((c.text or "").strip() for c in el.iter()
                    if local(c.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt") and c.text)
    where = t("StateAbbreviationCd") or ("F:" + t("CountryCd") if t("CountryCd") else "")
    e = ein9(t("RecipientEIN")) if t("RecipientEIN") else ""
    return [e if e.strip("0") else "", name[:90], where, t("IRCSectionDesc")[:30],
            num(t("CashGrantAmt")) or 0.0, num(t("NonCashAssistanceAmt")) or 0.0]


def parse_sched_i(stream) -> dict:
    lines, filer = [], ""
    for _, el in ET.iterparse(stream, events=("end",)):
        tag = local(el.tag)
        if tag == "RecipientTable":
            lines.append(line_of(el))
            el.clear()
        elif tag == "Filer" and not filer:
            filer = next((ein9(c.text) for c in el if local(c.tag) == "EIN" and c.text), "")
        elif tag.startswith("IRS990") and tag != "IRS990ScheduleI":
            el.clear()
    return {"filer_ein": filer, "lines": lines}


def load_lines(oid: str, expect: int, cache: str, xml_dirs: Sequence[str], fetch: bool) -> dict:
    path = os.path.join(cache, f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == LINES_V:
            return c
    tried = []
    for p in (os.path.join(d, f"{oid}{s}") for d in xml_dirs for s in (".xml", "_public.xml")):
        if not os.path.exists(p):
            continue
        try:
            with open(p, "rb") as fh:
                r = parse_sched_i(fh)
        except ET.ParseError:
            tried.append(f"{p}:parse_error")
            continue
        if len(r["lines"]) == expect:
            return save(path, {**r, "status": "ok", "via": "local", "_v": LINES_V})
        tried.append(f"{p}:{len(r['lines'])}!={expect}")
    if not fetch:
        return {"status": "not_fetched", "lines": [], "tried": tried}
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                r = parse_sched_i(resp)
            st = "ok" if len(r["lines"]) == expect else f"count_mismatch:{len(r['lines'])}!={expect}"
            return save(path, {**r, "status": st, "via": "mirror", "_v": LINES_V})
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return {"status": f"http_{e.code}", "lines": []}
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError):
            time.sleep(3 * (attempt + 1))
    return {"status": "error", "lines": []}


def save(path: str, obj: dict) -> dict:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return obj


def load_bmf(bmf_dir: str, eins: frozenset) -> dict:

    out = {}
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                e = ein9(r["EIN"])
                if e in eins:
                    out[e] = {"ntee": (r.get("NTEE_CD") or "").strip().upper(), "foundation": (r.get("FOUNDATION") or "").strip(),
                              "subsection": (r.get("SUBSECTION") or "").strip(), "bmf_name": r.get("NAME", "").strip(),
                              "bmf_state": r.get("STATE", "").strip()}
    return out


# ----------------------------------------------------------------------------- classify
def classify(ein: str, name: str, irc: str, bmf: Mapping) -> tuple[str, str, str]:
    """-> (major_group, ntee_cd, method)."""
    b = bmf.get(ein) if ein else None
    if b and b["ntee"][:1] in MAJOR:
        return MAJOR[b["ntee"][:1]], b["ntee"], "ntee"
    if b and b["foundation"] in FOUNDATION_FALLBACK:
        return FOUNDATION_FALLBACK[b["foundation"]], "", f"bmf_foundation_{b['foundation']}"
    nm = norm_name(name) if name else ""
    up = (name or "").upper()
    hit = next((g for g, rx in NAME_RULES if rx.search(up) or rx.search(nm)), "")
    base = "in_bmf_no_ntee" if b else ("blank_ein" if not ein else "ein_not_in_bmf")
    if "GOV" in (irc or "").upper():
        base += "_government"
    return ("unclassified", "", base) if not hit else (hit, "", f"name_rule:{base}")


def amt(l: Sequence) -> float:
    return l[4] + l[5]


def annotate(grantor: str, lines: Sequence[Sequence], bmf: Mapping, wl_eins: frozenset, wl_names: Mapping) -> tuple[dict, ...]:
    def one(l):
        e, name, where, irc = (l[0] if l[0].strip("0") else ""), l[1], l[2], l[3]
        d2d = (e == grantor) or (e in wl_eins) or (not e and wl_names.get(norm_name(name), "") != "")
        g, ntee, m = classify(e, name, irc, bmf)
        return {"ein": e, "name": name, "where": where, "amount": amt(l), "d2d": d2d, "group": g, "ntee": ntee,
                "method": m, "key": e or "N:" + norm_name(name)}
    return tuple(one(l) for l in lines)


# ----------------------------------------------------------------------------- aggregate
def concentration(rows: Sequence[Mapping], weight: Mapping) -> dict:
    by = {}
    for r in rows:
        by[r["key"]] = by.get(r["key"], 0.0) + r["amount"] * weight.get(r["_sy"], 1.0)
    vals = sorted((v for v in by.values() if v > 0), reverse=True)
    tot = sum(vals)
    return {"recipients": len(vals), "top10_share": sum(vals[:10]) / tot if tot else None,
            "top100_share": sum(vals[:100]) / tot if tot else None,
            "hhi": sum((v / tot * 100) ** 2 for v in vals) if tot else None}


def group_rows(scope: str, scope_type: str, fy: str, basis: str, rows: Sequence[Mapping], weight: Mapping,
               n_sy: int, meta: Mapping) -> tuple[dict, ...]:
    w = lambda r: r["amount"] * weight.get(r["_sy"], 1.0)  # noqa: E731
    kept = tuple(r for r in rows if not r["d2d"])
    total_all = sum(w(r) for r in rows)
    d2d = total_all - sum(w(r) for r in kept)
    tot = sum(w(r) for r in kept)
    ntee_only = lambda r: r["method"] == "ntee" or r["method"].startswith("bmf_foundation")  # noqa: E731
    cls_tot = sum(w(r) for r in kept if ntee_only(r) and r["group"] != "unclassified")
    by = _group_by_fast(kept, lambda r: r["group"])
    conc = concentration(kept, weight)

    def row(g):
        rs = by.get(g, ())
        a = sum(w(r) for r in rs)
        a_ntee = sum(w(r) for r in rs if ntee_only(r))
        return {"scope": scope, "scope_type": scope_type, "fiscal_year": fy, "basis": basis, "ntee_major_group": g,
                "amount_usd": round(a), "share_of_non_d2d": a / tot if tot else None,
                "amount_ntee_or_bmf_only_usd": round(a_ntee) if g != "unclassified" else "",
                "share_of_bmf_classified": (a_ntee / cls_tot) if cls_tot and g != "unclassified" else None,
                "lines": len(rs), "recipients": len({r["key"] for r in rs}),
                "public_benefit_T_philanthropy_usd": round(sum(w(r) for r in rs if r["ntee"][:1] == "T"))
                if g == "public_societal_benefit" else "",
                "name_rule_usd": round(sum(w(r) for r in rs if r["method"].startswith("name_rule"))),
                **{k: "" for k in ("total_sched_i_usd", "d2d_excluded_usd", "d2d_share", "top10_share", "top100_share",
                                   "hhi", "sponsor_years", "segment", "sponsor_rank_fy2024")},
                **meta, "source": SOURCE}
    all_row = {**row("ALL"), "amount_usd": round(tot), "share_of_non_d2d": 1.0 if tot else None,
               "amount_ntee_or_bmf_only_usd": round(cls_tot), "share_of_bmf_classified": cls_tot / tot if tot else None,
               "lines": len(kept), "recipients": conc["recipients"], "total_sched_i_usd": round(total_all),
               "d2d_excluded_usd": round(d2d), "d2d_share": d2d / total_all if total_all else None,
               "top10_share": conc["top10_share"], "top100_share": conc["top100_share"],
               "hhi": round(conc["hhi"], 1) if conc["hhi"] is not None else None, "sponsor_years": n_sy,
               "name_rule_usd": round(sum(w(r) for r in kept if r["method"].startswith("name_rule"))),
               "public_benefit_T_philanthropy_usd": round(sum(w(r) for r in kept if r["ntee"][:1] == "T"))}
    return (all_row,) + tuple(row(g) for g in GROUPS)


FIELDS = ("scope", "scope_type", "segment", "sponsor_rank_fy2024", "fiscal_year", "basis", "ntee_major_group",
          "amount_usd", "share_of_non_d2d", "amount_ntee_or_bmf_only_usd", "share_of_bmf_classified", "lines",
          "recipients", "public_benefit_T_philanthropy_usd", "name_rule_usd", "total_sched_i_usd", "d2d_excluded_usd",
          "d2d_share", "top10_share", "top100_share", "hhi", "sponsor_years", "source")


def build_rows(ann: Mapping, panel: Mapping, rank: Mapping, weights: Mapping) -> tuple[dict, ...]:
    """ann: (ein, fy) -> annotated lines (each tagged _sy)."""
    seg_of = lambda e: panel[e]["segment"]  # noqa: E731
    scopes = ([("all_top50_itemising", "all", lambda e: True, {})]
              + [("all_ex_university_hospital", "all", lambda e: seg_of(e) != "university_hospital", {})]
              + [(s, "segment", (lambda e, s=s: seg_of(e) == s), {"segment": s})
                 for s in ("national", "processor", "community_foundation", "single_issue", "university_hospital")]
              + [("community_foundation_ex_svcf", "segment",
                  lambda e: seg_of(e) == "community_foundation" and e != SVCF, {"segment": "community_foundation"})]
              + [(panel[e]["name"], "sponsor", (lambda x, e=e: x == e), {"segment": seg_of(e), "sponsor_rank_fy2024": r})
                 for e, r in sorted(rank.items(), key=lambda kv: kv[1])])
    fyk = [(str(fy), (fy,)) for fy in FYS] + [("2023-2024", FYS)]
    out = []
    for name, stype, pred, meta in scopes:
        for fy_label, fys in fyk:
            keys = [k for k in ann if pred(k[0]) and k[1] in fys]
            if not keys:
                continue
            rows = tuple(r for k in keys for r in ann[k])
            for basis, wt in (("schedule_i", {}), ("daf_weighted", weights)):
                out.extend(group_rows(name, stype, fy_label, basis, rows, wt, len(keys), meta))
    return tuple(out)


def top_recipients(ann: Mapping, pred, n: int, bmf: Mapping) -> list:
    by = {}
    for k, rs in ann.items():
        if not pred(k[0]):
            continue
        for r in rs:
            if r["d2d"]:
                continue
            d = by.setdefault(r["key"], {"name": r["name"], "ein": r["ein"], "group": r["group"], "ntee": r["ntee"],
                                         "amount": 0.0, "grantors": set()})
            d["amount"] += r["amount"]
            d["grantors"].add(k[0])
    top = sorted(by.values(), key=lambda d: -d["amount"])[:n]
    return [{**{k: v for k, v in d.items() if k != "grantors"}, "amount": round(d["amount"]), "grantors": len(d["grantors"]),
             "bmf_name": bmf.get(d["ein"], {}).get("bmf_name", "")} for d in top]


def method_mix(ann: Mapping) -> dict:
    tot = {}
    for rs in ann.values():
        for r in rs:
            if r["d2d"]:
                continue
            m = r["method"].split(":")[0] if r["method"].startswith("name_rule") else r["method"]
            tot[m] = tot.get(m, 0.0) + r["amount"]
    s = sum(tot.values())
    return {k: {"usd": round(v), "share": round(v / s, 4)} for k, v in sorted(tot.items(), key=lambda kv: -kv[1])}


def d2d_by_segment(ann: Mapping, panel: Mapping) -> dict:
    out = {}
    for (e, fy), rs in ann.items():
        for r in rs:
            if r["d2d"]:
                k = (panel[r["ein"]]["segment"] if r["ein"] in panel else "name_match_or_self")
                out[k] = out.get(k, 0.0) + r["amount"]
    return {k: round(v) for k, v in out.items()}


def kept_to_panel(ann: Mapping, panel: Mapping) -> dict:
    """Non-excluded lines whose recipient is still a DAFRC panel EIN (whitelist `exclude`), by segment."""
    out = {}
    for rs in ann.values():
        for r in rs:
            if not r["d2d"] and r["ein"] in panel:
                s = panel[r["ein"]]["segment"]
                out[s] = out.get(s, 0.0) + r["amount"]
    return {k: round(v) for k, v in out.items()}


def ntee_detail(ann: Mapping, prefix: str, n: int = 12) -> list:
    by = {}
    for rs in ann.values():
        for r in rs:
            if not r["d2d"] and r["ntee"].startswith(prefix):
                by[r["ntee"][:3]] = by.get(r["ntee"][:3], 0.0) + r["amount"]
    return sorted(((k, round(v)) for k, v in by.items()), key=lambda kv: -kv[1])[:n]


def coverage(item: Mapping, panel: Mapping) -> dict:
    """Schedule I itemised total (grants > $5,000 per recipient) vs Part IX line 1 (all grants to domestic orgs)
    and vs Schedule D DAF grants, itemising sponsor-years, excluding university/hospital sponsors."""
    def one(pred):
        xs = [x for (e, _), x in item.items() if pred(panel[e]["segment"]) and panel[e]["segment"] != "university_hospital"]
        si = sum(x.get("sched_i_total") or 0 for x in xs)
        ix = sum(x.get("part_ix_line1_grants_domestic_orgs") or 0 for x in xs)
        sd = sum(x.get("sched_d_daf_grants") or 0 for x in xs)
        return {"sched_i_total": round(si), "part_ix_line1": round(ix), "sched_d_daf_grants": round(sd),
                "sched_i_over_part_ix": round(si / ix, 4) if ix else None, "sched_i_over_daf_grants": round(si / sd, 4) if sd else None}
    return {"all_ex_uh": one(lambda s: True), **{s: one(lambda g, s=s: g == s)
                                                 for s in ("national", "community_foundation", "single_issue")}}


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    sy = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen}
    item = {k: x for k, x in sy.items() if itemized(x)}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, a.xml_dir, a.fetch) for k, x in item.items()}
    bad = {f"{panel[k[0]]['name']} FY{k[1]}": v["status"] for k, v in loaded.items() if v["status"] != "ok"}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    eins = frozenset(l[0] for v in good.values() for l in v["lines"] if l[0])
    bmf = load_bmf(a.bmf_dir, eins)

    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    weights = {k: min(1.0, max(0.0, share[k])) for k in good if share.get(k) is not None}

    ann = {k: tuple({**r, "_sy": k} for r in annotate(k[0], v["lines"], bmf, wl_eins, wl_names)) for k, v in good.items()}
    rows = build_rows(ann, panel, rank, weights)
    write_csv(OUT, rows, FIELDS)

    def pick(scope, fy="2023-2024", basis="schedule_i"):
        return {r["ntee_major_group"]: {k: r[k] for k in ("amount_usd", "share_of_non_d2d", "share_of_bmf_classified",
                                                          "top10_share", "top100_share", "hhi", "recipients",
                                                          "d2d_excluded_usd", "d2d_share", "total_sched_i_usd",
                                                          "public_benefit_T_philanthropy_usd", "name_rule_usd") if r[k] not in ("", None)}
                for r in rows if r["scope"] == scope and r["fiscal_year"] == fy and r["basis"] == basis}
    seg = lambda s: (lambda e: panel[e]["segment"] == s)  # noqa: E731
    summary = {
        "sponsor_years_top50": len(sy), "itemising": len(item), "lines_loaded_ok": len(good), "load_problems": bad,
        "not_itemised": sorted(f"{panel[k[0]]['name']} FY{k[1]}" for k in sy if k not in item),
        "missing_returns": sorted(f"{panel[e]['name']} FY{fy}" for e in rank for fy in FYS if (e, fy) not in sy),
        "via": {s: sum(1 for v in good.values() if v.get("via") == s) for s in ("local", "mirror")},
        "coverage_itemising_fy2023_2024": coverage(item, panel),
        "lines_total": sum(len(v["lines"]) for v in good.values()),
        "bmf_matched_eins": len(bmf), "distinct_eins": len(eins),
        "daf_weight_coverage": f"{len(weights)}/{len(good)}",
        "method_mix_non_d2d": method_mix(ann),
        "d2d_excluded_by_recipient_segment": d2d_by_segment(ann, panel),
        "kept_lines_to_other_panel_eins_by_segment": kept_to_panel(ann, panel),
        "pooled": {s: pick(s) for s in ("all_top50_itemising", "all_ex_university_hospital", "national", "processor",
                                        "community_foundation", "community_foundation_ex_svcf", "single_issue",
                                        "university_hospital")},
        "pooled_daf_weighted": {s: pick(s, basis="daf_weighted") for s in ("all_ex_university_hospital", "national",
                                                                           "community_foundation",
                                                                           "community_foundation_ex_svcf", "single_issue")},
        "by_fy_all_ex_uh": {fy: pick("all_ex_university_hospital", fy) for fy in ("2023", "2024")},
        "T_detail": ntee_detail(ann, "T"), "X_detail": ntee_detail(ann, "X", 8), "B_detail": ntee_detail(ann, "B", 8),
        "Q_detail": ntee_detail(ann, "Q", 8),
        "top25_recipients_all_ex_uh": top_recipients(ann, lambda e: panel[e]["segment"] != "university_hospital", 25, bmf),
        "top10_national": top_recipients(ann, seg("national"), 10, bmf),
        "top10_cf": top_recipients(ann, seg("community_foundation"), 10, bmf),
        "foreign_lines_usd": round(sum(r["amount"] for rs in ann.values() for r in rs if not r["d2d"] and r["where"].startswith("F:"))),
        "sponsor_shares": [{"rank": r["sponsor_rank_fy2024"], "sponsor": r["scope"][:40], "segment": r["segment"],
                            **{g: round(x["share_of_non_d2d"], 3) for g, x in pick(r["scope"]).items()
                               if g in ("education", "religion", "human_services", "health", "public_societal_benefit")},
                            "top100": round(pick(r["scope"])["ALL"].get("top100_share") or 0, 3)}
                           for r in rows if r["scope_type"] == "sponsor" and r["ntee_major_group"] == "ALL"
                           and r["fiscal_year"] == "2023-2024" and r["basis"] == "schedule_i"],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
