#!/usr/bin/env python3
"""Schedule I grant-purpose panel: top-50 DAF sponsors, latest (FY2024) return (queue item P-B40N13-01).

Universe and return choice are those of scripts/mission_recipient_sectors.py (top-50 DAFRC sponsors by FY2024 DAF
assets; one FY2024 return per sponsor via mission_daf_to_daf.pick_returns over the netpayout990/ cache). The
Schedule I line cache written by that script ([ein, name, where, irc, cash, noncash]) has no purpose field, so this
script re-reads every Schedule I Part II RecipientTable of the same returns from the IRS e-file XML and keeps
PurposeOfGrantTxt. A local XML copy is used first; otherwise (with --fetch) the GivingTuesday mirror of IRS TEOS.
Each re-parse is checked against the line cache (line count and dollar total must match).

Purpose classification (ordered; first rule that fires wins; see RULES):
  blank                 empty purpose, or a placeholder ("0", "N/A", "NONE", "-")
  boiler_unrestricted   contains UNRESTRICTED
  boiler_aggregate      starts MULTIPLE / VARIOUS (grouped lines)
  specific_capital      scholarship, fellowship, endowment, capital, building, construction, renovation, facility,
                        equipment, chair/professorship, campaign (not "annual campaign")
  boiler_general        general support / general operating / operations / annual fund / bare "GENERAL" / highest need
  boiler_exempt         exempt purpose, charitable purpose/gift/contribution, support of mission, donation, gift
  category_label        every word is a sector-taxonomy word (NTEE-style labels such as "HUMAN SERVICES",
                        "RELIGION RELATED", "DAF - EDUCATION"); a sponsor's sector code, not a use restriction
  specific_program      program, project, research, initiative, event, gala, sponsorship, relief, memorial,
                        tribute, a named fund, "for the ..."
  other_descriptive     anything else (free text with no rule hit)
Also kept: every Schedule I narrative (SupplementalInformationDetail inside IRS990ScheduleI), flagged when it mentions
restriction (RESTRICT_RX).
Rollups: boilerplate = boiler_*; specific = specific_*; plus a `modal` overlay: a purpose string carried by more
than 90% of a sponsor's lines is counted as boilerplate whatever its class (boilerplate_incl_modal).

Stdlib only; functional style. Pure transforms; I/O at the edges.

Usage:
  python3 scripts/mission_grant_purpose_panel.py . --np-cache NPCACHE --lines-cache LC --xml-list ALLXML.txt \
      --xml-dir D [--xml-dir D2 ...] --purpose-cache PC [--fetch] [--audit AUDIT.csv] [--summary SUMMARY.json]
"""
from __future__ import annotations

import argparse
import collections
import csv
import itertools
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, XML_URL, ein9, local, num, read_csv  # noqa: E402
from mission_daf_to_daf import TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_net_payout import itemized, panel_from  # noqa: E402

FY = 2024
MODAL_CUT = 0.90
OUT_REL = os.path.join("data", "mission-2026-11-14", "grant-purpose-panel-2026-11-19.csv")
PURPOSE_V = 3
UA = "research-script/1.0"

# ----------------------------------------------------------------------------- rules (published verbatim in the doc)
CATEGORY_WORDS = frozenset("""
ACADEMIC ADDICTION ADOPTION ADULT ADVANCING ADVOCACY AFFAIRS AGRICULTURAL AGRICULTURE AID ALLIANCE ALLIANCES ALUMNI
ANIMAL ANIMALS APOLOGETICS ARTS ASSISTANCE ATHLETICS AWARENESS BENEFIT BIBLE BUILDING CAMPING CAMPS CAMPUS CARE
CENTERS CHILD CHILDCARE CHILDHOOD CHILDREN'S CHILDRENS CHRISTIAN CHRISTIANITY CHURCH CIVIC CIVIL CLINICS COMMUNITY
CONNECTION CONSERVATION CRIME CULTURAL CULTURE DEVEL DEVELOPMENT DEVELOPMENTAL DISABILITIES DISASTER DISEASE
DISEASES DISORDER DISORDERS DOMESTIC EARLY ECONOMIC ECONOMICS EDUC EDUCATION EDUCATIONAL ELDER ELDERCARE EMERGENCY
EMPLOYMENT ENGAGEMENT ENTERTAINMENT ENTREPRENEURSHIP ENVIRONMENT ENVIRONMENTAL EQUESTRIANISM EVANGELISM
EXPLOITATION FAITH FAMILY FINANCIAL FIRE FIRST FOOD FOREIGN FOSTER FOUNDATIONS GENEROSITY GIVING GOVERNMENT
GRADUATE GRANTMAKING GRASSROOTS HEALTH HERITAGE HIGHER HISTORIC HISTORICAL HISTORY HOME HOMELESS HOMELESSNESS
HOSPITALS HOUSING HUMAN HUMANITARIAN HUMANITIES HUNGER IMMIGRANT IMMIGRATION IMPROVEMENT INDIV INSTITUTIONS INT
INTERFAITH INTERNATIONAL JEWISH JOB JOBS JUSTICE K12 LAW LEADERSHIP LEGAL LEISURE LIBRARIES LIFE LITERACY LITERARY
MARKETPLACE MARRIAGE MATH MEDIA MEDICAL MEDICINE MEMBERSHIP MEN'S MENS MENTAL MENTORING MICROFINANCE MILITARY
MINISTRY MISSIONS MOVEMENTS MUSEUMS MUSIC MUTUAL NATURAL NEIGHBORHOOD NONPROFIT NUTRITION ORGANIZATIONS ORPHAN
OST PARENTS PARKS PASTORAL PATIENT PEACE PERFORMING PERSECUTION PHILANTHROPY PHYSICAL PLANTING POLICE POLICY PRAYER
PREPAREDNESS PRESCHOOLS PRESERVATION PRE-K PRIMARY PRISON PROFESSIONAL PROTECTION PUBLIC PUBLISHING QUALITY
RECREATION REFUGEE REHAB REHABILITATIVE RELATIONS RELIEF RELIGION RELIGIOUS RESCUE RESEARCH RESOURCES RESPONDERS
RETREAT RIGHTS SAFETY SCHOLAR SCHOLARSHIPS SCHOOLS SCIENCE SCIENCES SECONDARY SECURITY SERVICE SERVICES SHELTER
SHELTERS SINGLE SLAVERY SOCIAL SOCIETAL SOCIETIES SOCIETY SPECIAL SPECIALTY SPIRITUAL SPORTS STUDENT SUBSTANCE
SUPPLY SUPPORT SYNAGOGUES TECHNOLOGY TRADE TRAFFICKING TRAINING TRANSLATION TRANSPORTATION TRUSTS UNCLASSIFIED
UNIVERSITIES UNKNOWN VETERANS VICTIM VIOLENCE VISUAL VOLUNTARISM WATER WEALTH WELFARE WELL WELLBEING WIDOWS WOMEN'S
WOMENS WORKFORCE WORKPLACE YOUNG YOUTH BEING BEAUTIFICATION BUILDING OTHER NEEDS COLLEGES PARTICIPATION OPPORTUNITY
ABUSE RESPONSE PREVENTION RACIAL HIGH ELEMENTARY CHILDREN PROTESTANT CATHOLIC ETHNIC DEVELOPMENTALLY DISABLED CHARITY
PROMOTION CAPACITY ACTION RIGHT K DEPARTMENT PROGRAMS INSTITUTES ANALYSIS CANCER MATCHING RESIDENTIAL DAY FEDERATED
""".split())
LABEL_STOP = frozenset({"AND", "OR", "OF", "THE", "&", "DAF", "DONOR", "ADVISED", "DONOR-ADVISED", "RELATED", "NEC",
                        "N.E.C.", "N", "E", "C", "GENERAL", "TO", "A", "W"})

RULES = (
    ("blank", re.compile(r"^(|0|N/?A|NONE|-+|\.)$")),
    ("boiler_unrestricted", re.compile(r"\bUNRESTRICTED\b")),
    ("boiler_aggregate", re.compile(r"^(MULTIPLE|VARIOUS)\b")),
    ("specific_capital", re.compile(r"SCHOLARSHIP|FELLOWSHIP|\bENDOW|\bCAPITAL\b|\bBUILDING (FUND|CAMPAIGN|PROJECT)|"
                                    r"\bCONSTRUCTION\b|\bRENOVAT|\bFACILIT(Y|IES)\b|\bEQUIPMENT\b|\bPROFESSORSHIP\b|"
                                    r"\bCHAIR\b|(?<!ANNUAL )\bCAMPAIGN\b|\bTUITION\b|\bPRESERVATION OF\b")),
    ("boiler_general", re.compile(r"\bGENERAL (SUPPORT|OPERATING|OPERATIONS?|OPERATIONAL|PURPOSES?|FUND|NONPROFIT|USE|"
                                  r"CHARITABLE|PHILANTHROPY|GRANT)\b|^((DONOR-ADVISED|DAF)[ ,\-]+)?GENERAL\.?$|\bOPERATING\b|"
                                  r"\bOPERATIONS?\b|\bOPERATIONAL\b|\bANNUAL (FUND|GIVING|CAMPAIGN|APPEAL|SUPPORT|GIFT)\b|"
                                  r"^(FOR |TO )?(PROVIDE )?SUPPORT\.?$|WHERE (MOST )?NEEDED|(HIGHEST|GREATEST) NEED")),
    ("boiler_exempt", re.compile(r"EXEMPT|CHARITABLE (PURPOSE|GIFT|CONTRIBUTION|DONATION|GRANT|USE|ACTIVIT)|"
                                 r"^(IN |TO )?(SUPPORT )?(OF )?(THE )?(ORGANIZATION'?S? )?MISSION\.?$|\bMISSION SUPPORT\b|^(CHARITABLE|DONATION|CONTRIBUTION|GIFT|GRANT|DONOR ADVISED "
                                 r"GRANT|DAF GRANT|PHILANTHROPIC|PUBLIC CHARITY)\.?$")),
    ("category_label", None),  # word-list test, see is_label
    ("specific_program", re.compile(r"\bPROGRAMS?\b|\bPROJECTS?\b|\bRESEARCH\b|\bINITIATIVE|\bEVENT|\bGALA\b|"
                                    r"SPONSOR|\bTICKET|\bAUCTION|\bGOLF\b|\bTOURNAMENT|\bDINNER|\bLUNCHEON|"
                                    r"\bRELIEF\b|\bEMERGENCY\b|HURRICANE|WILDFIRE|\bFIRE\b|EARTHQUAKE|UKRAINE|ISRAEL|"
                                    r"GAZA|\bMEMORY\b|\bMEMORIAL\b|\bHONOR\b|\bTRIBUTE\b|\bFUND\b|^FOR THE\b|"
                                    r"\bAWARD\b|\bPRIZE\b|\bTRIP\b|\bCAMP\b|\bCONFERENCE\b|\bEXHIBIT")),
)
BOILER = frozenset({"boiler_unrestricted", "boiler_aggregate", "boiler_general", "boiler_exempt"})
SPECIFIC = frozenset({"specific_capital", "specific_program"})
CLASSES = ("blank", "boiler_unrestricted", "boiler_aggregate", "boiler_general", "boiler_exempt", "specific_capital",
           "specific_program", "category_label", "other_descriptive")


def norm_purpose(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").upper().replace("’", "'")).strip()


def is_label(p: str) -> bool:
    toks = tuple(t for t in re.split(r"[\s,/&()\-:;.]+", p) if t and t not in LABEL_STOP and not re.fullmatch(r"X?\d+|\(?X\d+\)?", t))
    return 0 < len(toks) <= 10 and all(t in CATEGORY_WORDS for t in toks)


def classify(p: str) -> str:
    return next((name for name, rx in RULES if (is_label(p) if rx is None else bool(rx.search(p)))), "other_descriptive")


# ----------------------------------------------------------------------------- parse (I/O edge)
def line_of(el) -> list:
    g = {local(c.tag): (c.text or "").strip() for c in el.iter()}
    return [ein9(g["RecipientEIN"]) if g.get("RecipientEIN") else "", num(g.get("CashGrantAmt", "")) or 0.0,
            num(g.get("NonCashAssistanceAmt", "")) or 0.0, g.get("PurposeOfGrantTxt", "")]


def notes_of(sched_i_el) -> list:
    """Every SupplementalInformationDetail inside IRS990ScheduleI (its Part IV / Part I line 2 narratives)."""
    def one(d):
        g = {local(c.tag): (c.text or "").strip() for c in d.iter()}
        return [g.get("FormAndLineReferenceDesc", ""), g.get("ExplanationTxt", "")]
    return [one(d) for d in sched_i_el.iter() if local(d.tag) == "SupplementalInformationDetail"]


def parse_purposes(stream) -> dict:
    """-> {"lines": [[ein, cash, noncash, purpose], ...], "notes": [[ref, text], ...]} (Schedule I narratives)."""
    keep = ("RecipientTable", "IRS990ScheduleI")
    evs = filter(lambda te: te[0] in keep, ((local(el.tag), el) for _, el in ET.iterparse(stream, events=("end",))))
    # line_of runs before el.clear() (tuple items evaluate left to right), which keeps memory flat
    items = tuple(("L", line_of(el), el.clear()) if t == "RecipientTable" else ("N", notes_of(el), None) for t, el in evs)
    return {"lines": [i[1] for i in items if i[0] == "L"], "notes": [n for i in items if i[0] == "N" for n in i[1]]}


RESTRICT_RX = re.compile(r"RESTRICT|DESIGNAT|SPECIFIC PURPOSE|PURPOSE OF THE GRANT|GRANT PURPOSE|INTENDED USE|EARMARK", re.I)


def monitoring_note(notes: Sequence) -> dict:
    txt = " | ".join(f"{r}: {t}" for r, t in notes)
    hit = RESTRICT_RX.search(txt)
    return {"sched_i_note_mentions_restriction": "yes" if hit else ("no" if txt else "no_note"),
            "sched_i_note_excerpt": (txt[max(0, hit.start() - 120): hit.end() + 120] if hit else txt[:240]).replace("\n", " ")}


def xml_path(oid: str, listed: Mapping, dirs: Sequence[str]) -> str:
    cands = ([listed[oid]] if oid in listed else []) + [os.path.join(d, f"{oid}{s}") for d in dirs for s in ("_public.xml", ".xml")]
    return next((p for p in cands if os.path.exists(p)), "")


def fetch(oid: str, dest_dir: str) -> str:
    os.makedirs(dest_dir, exist_ok=True)
    dst = os.path.join(dest_dir, f"{oid}_public.xml")
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as resp, open(dst + ".part", "wb") as fh:
        fh.write(resp.read())
    os.replace(dst + ".part", dst)
    return dst


def load_purposes(oid: str, listed: Mapping, dirs: Sequence[str], cache: str, do_fetch: bool) -> dict:
    cp = os.path.join(cache, f"{oid}.json")
    if os.path.exists(cp):
        with open(cp, encoding="utf-8") as fh:
            c = json.load(fh)
        if c.get("_v") == PURPOSE_V:
            return c
    p = xml_path(oid, listed, dirs)
    via = "local"
    if not p and do_fetch:
        try:
            p, via = fetch(oid, dirs[0]), "mirror"
        except (urllib.error.URLError, OSError) as e:
            return {"status": f"fetch_error:{e}", "lines": []}
    if not p:
        return {"status": "no_xml", "lines": []}
    with open(p, "rb") as fh:
        parsed = parse_purposes(fh)
    out = {"status": "ok", "via": via, "xml": p, **parsed, "_v": PURPOSE_V}
    os.makedirs(cache, exist_ok=True)
    with open(cp, "w", encoding="utf-8") as fh:
        json.dump(out, fh)
    return out


def cache_check(oid: str, lines: Sequence, lines_cache: str) -> dict:
    p = os.path.join(lines_cache, f"{oid}.json")
    if not os.path.exists(p):
        return {"cache_lines": "", "cache_usd": "", "match": "no_cache"}
    with open(p, encoding="utf-8") as fh:
        cl = json.load(fh)["lines"]
    cu, pu = round(sum(l[4] + l[5] for l in cl)), round(sum(l[1] + l[2] for l in lines))
    return {"cache_lines": len(cl), "cache_usd": cu, "match": "yes" if (len(cl) == len(lines) and cu == pu) else "no"}


# ----------------------------------------------------------------------------- metrics (pure)
def annotate(lines: Sequence) -> tuple[dict, ...]:
    rows = tuple({"p": norm_purpose(l[3]), "usd": l[1] + l[2]} for l in lines)
    cnt = collections.Counter(r["p"] for r in rows)
    n = len(rows) or 1
    modal = {p for p, k in cnt.items() if k / n > MODAL_CUT and p}
    return tuple({**r, "cls": classify(r["p"]), "modal": r["p"] in modal} for r in rows)


def shares(rows: Sequence[Mapping], pred) -> tuple[float, float]:
    n, u = len(rows), sum(r["usd"] for r in rows)
    k = tuple(r for r in rows if pred(r))
    return (len(k) / n if n else 0.0, sum(r["usd"] for r in k) / u if u else 0.0)


def regime(m: Mapping) -> str:
    if m["top_purpose_line_share"] > MODAL_CUT:
        return "single_string_" + ("boilerplate" if m["top_purpose_class"] in BOILER or m["top_purpose_class"] == "other_descriptive" else m["top_purpose_class"])
    if m["share_lines_category_label"] >= 0.6:
        return "sector_taxonomy"
    if m["share_lines_boilerplate"] >= 0.5:
        return "mostly_boilerplate_with_free_text"
    return "free_text_mixed"


def metrics(rows: Sequence[Mapping]) -> dict:
    cnt = collections.Counter(r["p"] for r in rows)
    top, topn = (cnt.most_common(1)[0] if cnt else ("", 0))
    preds = {"boilerplate": lambda r: r["cls"] in BOILER, "boilerplate_incl_modal": lambda r: r["cls"] in BOILER or r["modal"],
             "specific": lambda r: r["cls"] in SPECIFIC, "category_label": lambda r: r["cls"] == "category_label",
             "other_descriptive": lambda r: r["cls"] == "other_descriptive", "blank": lambda r: r["cls"] == "blank",
             **{c: (lambda r, c=c: r["cls"] == c) for c in CLASSES if c not in ("blank", "category_label", "other_descriptive")}}
    sh = {k: shares(rows, f) for k, f in preds.items()}
    m = {"lines": len(rows), "usd": round(sum(r["usd"] for r in rows)),
         "distinct_purposes": len([p for p in cnt if p]),
         "top_purpose": top[:90], "top_purpose_class": classify(top) if rows else "",
         "top_purpose_line_share": round(topn / len(rows), 4) if rows else 0.0,
         "modal_gt90": "yes" if any(r["modal"] for r in rows) else "no",
         **{f"share_lines_{k}": round(v[0], 4) for k, v in sh.items()},
         **{f"share_usd_{k}": round(v[1], 4) for k, v in sh.items()}}
    return {**m, "purpose_regime": regime(m)}


def median(xs: Sequence[float]) -> float:
    s = sorted(xs)
    n = len(s)
    return 0.0 if not n else (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)


FIELDS = ("scope_type", "rank_fy2024", "ein", "sponsor", "segment", "object_id", "tax_period_end", "lines", "usd",
          "distinct_purposes", "top_purpose", "top_purpose_class", "top_purpose_line_share", "modal_gt90",
          "share_lines_boilerplate", "share_usd_boilerplate", "share_lines_boilerplate_incl_modal",
          "share_usd_boilerplate_incl_modal", "share_lines_specific", "share_usd_specific",
          "share_lines_category_label", "share_usd_category_label", "share_lines_other_descriptive",
          "share_usd_other_descriptive", "share_lines_blank", "share_usd_blank",
          *[f"share_{b}_{c}" for c in CLASSES if c not in ("blank", "category_label", "other_descriptive") for b in ("lines", "usd")],
          "purpose_regime", "sponsors", "median_sponsor_share_lines_boilerplate_incl_modal",
          "median_sponsor_share_lines_specific", "sched_i_note_mentions_restriction", "sched_i_note_excerpt",
          "cache_check", "source_url")


def group_row(scope: str, label: str, sponsor_rows: Sequence[Mapping], ann: Mapping) -> dict:
    rows = tuple(r for s in sponsor_rows for r in ann[s["object_id"]])
    m = metrics(rows)
    return {**m, "scope_type": scope, "segment": label, "sponsor": f"{label} ({len(sponsor_rows)} sponsors, pooled lines)",
            "top_purpose": "", "top_purpose_class": "", "top_purpose_line_share": "", "modal_gt90": "", "purpose_regime": "",
            "sponsors": len(sponsor_rows),
            "median_sponsor_share_lines_boilerplate_incl_modal": round(median([s["share_lines_boilerplate_incl_modal"] for s in sponsor_rows]), 4),
            "median_sponsor_share_lines_specific": round(median([s["share_lines_specific"] for s in sponsor_rows]), 4)}


def write_csv(path: str, rows: Iterable[Mapping], fields: Sequence[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def audit_rows(sponsor_rows: Sequence[Mapping], ann: Mapping) -> list:
    def one(s):
        rows = ann[s["object_id"]]
        srt = sorted(rows, key=lambda r: r["p"])
        by = {p: (len(g), sum(r["usd"] for r in g)) for p, g in ((k, tuple(v)) for k, v in itertools.groupby(srt, key=lambda r: r["p"]))}
        return [{"rank_fy2024": s["rank_fy2024"], "sponsor": s["sponsor"], "segment": s["segment"], "purpose": p,
                 "class": classify(p), "lines": v[0], "usd": round(v[1])} for p, v in sorted(by.items(), key=lambda kv: -kv[1][0])]
    return [r for s in sponsor_rows for r in one(s)]


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--xml-list", default="")
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--purpose-cache", required=True)
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--audit", default="")
    ap.add_argument("--summary", default="")
    a = ap.parse_args(argv)

    listed = {}
    if a.xml_list and os.path.exists(a.xml_list):
        with open(a.xml_list, encoding="utf-8") as fh:
            listed = {os.path.basename(l.strip()).split(".")[0].replace("_public", ""): l.strip() for l in fh if l.strip()}
    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    sy = {e: chosen[(e, FY)] for e in rank if (e, FY) in chosen}
    item = {e: x for e, x in sy.items() if itemized(x)}
    loaded = {e: load_purposes(x["oid"], listed, a.xml_dir, a.purpose_cache, a.fetch) for e, x in item.items()}
    ok = {e: v for e, v in loaded.items() if v["status"] == "ok"}
    ann = {item[e]["oid"]: annotate(v["lines"]) for e, v in ok.items()}

    def sponsor_row(e):
        x, chk = item[e], cache_check(item[e]["oid"], ok[e]["lines"], a.lines_cache)
        return {**metrics(ann[x["oid"]]), "scope_type": "sponsor", "rank_fy2024": rank[e], "ein": e,
                "sponsor": panel[e]["name"], "segment": panel[e]["segment"], "object_id": x["oid"],
                "tax_period_end": x["tax_period_end"], "sponsors": 1,
                "cache_check": f"{chk['match']} (cache {chk['cache_lines']} lines / ${chk['cache_usd']})",
                **monitoring_note(ok[e].get("notes", [])), "source_url": XML_URL.format(oid=x["oid"])}
    srows = sorted((sponsor_row(e) for e in ok), key=lambda r: r["rank_fy2024"])
    segs = sorted({r["segment"] for r in srows})
    grows = ([group_row("all", "all_top50_itemising", srows, ann),
              group_row("all", "all_ex_university_hospital", [r for r in srows if r["segment"] != "university_hospital"], ann)]
             + [group_row("segment", s, [r for r in srows if r["segment"] == s], ann) for s in segs])
    out = os.path.join(a.root, OUT_REL)
    write_csv(out, srows + grows, FIELDS)
    if a.audit:
        write_csv(a.audit, audit_rows(srows, ann), ("rank_fy2024", "sponsor", "segment", "purpose", "class", "lines", "usd"))
    summ = {"fy": FY, "top_n": len(rank), "with_fy2024_return": len(sy), "itemising": len(item), "parsed_ok": len(ok),
            "not_itemising": sorted(panel[e]["name"] for e in sy if e not in item),
            "load_problems": {panel[e]["name"]: v["status"] for e, v in loaded.items() if v["status"] != "ok"},
            "via": dict(collections.Counter(v.get("via", "") for v in ok.values())),
            "cache_mismatch": [r["sponsor"] for r in srows if not r["cache_check"].startswith("yes")],
            "regimes": dict(collections.Counter(r["purpose_regime"] for r in srows)),
            "regime_by_segment": {s: dict(collections.Counter(r["purpose_regime"] for r in srows if r["segment"] == s)) for s in segs},
            "class_rollup_all": {k: grows[0][k] for k in grows[0] if k.startswith("share_")},
            "groups": [{k: g[k] for k in ("segment", "sponsors", "lines", "usd", "distinct_purposes", "share_lines_boilerplate",
                                          "share_usd_boilerplate", "share_lines_boilerplate_incl_modal", "share_usd_boilerplate_incl_modal",
                                          "share_lines_specific", "share_usd_specific", "share_lines_category_label",
                                          "share_usd_category_label", "share_lines_other_descriptive", "share_lines_blank",
                                          "share_usd_blank", "median_sponsor_share_lines_boilerplate_incl_modal",
                                          "median_sponsor_share_lines_specific")} for g in grows],
            "out": out}
    if a.summary:
        with open(a.summary, "w", encoding="utf-8") as fh:
            json.dump(summ, fh, indent=1)
    print(json.dumps({k: summ[k] for k in ("itemising", "parsed_ok", "not_itemising", "load_problems", "via", "cache_mismatch", "regimes")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
