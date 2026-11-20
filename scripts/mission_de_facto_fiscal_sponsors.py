#!/usr/bin/env python3
"""De facto fiscal sponsors derived from the filings themselves (queue item P-G0503-03).

A Schedule I line whose recipient name has the form "X FBO Y", "Y c/o X", "X on behalf of Y" or "Y, a project of X"
names a host X (whose EIN is reported) and a distinct beneficiary Y. A recipient EIN that appears in such lines for at
least three distinct beneficiaries ("projects") across the top-50 sponsors' FY2023-24 Schedule I lines is a de facto
fiscal sponsor (or pass-through host) on the filers' own evidence.

Universe and lines: exactly those of mission_exception_refined.load_screened (mission_exception_load pipeline: top-50
DAFRC sponsors, 94 itemising sponsor-years, totals rows dropped by mission_exception_load.drop_totals_rows, DAF-to-DAF
lines marked by the whitelist). mission_exception_refined.py is imported and NOT modified; its refined flags are
rebuilt here with its own functions so that the core and broad unions can be re-cut with the de facto hosts added.

Detection rules (deterministic; applied to mission_exception_load.upname(name), i.e. upper case, '&' -> AND, every
non-alphanumeric character -> space; IRS e-file business names cannot contain '/', so "c/o" and "f/b/o" are filed as
"CO", "C O", "FBO", "F B O"):
  R1 fbo           \\bF ?B ?O\\b | \\bFOR (THE )?BENEFIT OF\\b                       default host side: left
  R2 care_of       \\bIN CARE OF\\b | \\bC O\\b | \\bCO\\b   (bare "CARE OF" is a legal-name phrase: HOSPICE AND
                   PALLIATIVE CARE OF ...)                                         default host side: right
  R3 on_behalf_of  \\bON BEHALF OF\\b | \\bO B O\\b | \\bOBO\\b                       default host side: left
  R4 project_of    \\bA PROJECT OF\\b | \\bFISCALLY SPONSORED BY\\b | \\bFISCAL SPONSOR (FOR|OF)\\b   host: right
  The first connector match (leftmost; ties by rule order) splits the name into a left and a right side.
Name rules for a valid detection (all must hold):
  N1 the line has a recipient EIN (blank / placeholder EINs are skipped);
  N2 legal-name guard: the connector rule does not also match the EIN's current EO BMF name (e.g. LIBRARY FOUNDATION
     FOR THE BENEFIT OF ..., CARE OF CREATION INC);
  N3 host side: a side "matches" the EIN when >= half of its non-generic name tokens are present in the EIN's
     reference names (current BMF name plus the modal plain filed name for that EIN): exactly, as a >= 3-character
     prefix of a reference token (truncation), as the acronym of a reference name or a >= 3-character prefix of it
     (TSNE, MCV), or as a >= 5-character run-together substring (SOCIALGOOD). If exactly one side matches, it is the
     host; if both, the rule's default host side; if neither, the detection is `unverified` and does not count;
  N4 project side: its name key (mission_exception_refined.name_key; THE/INC/CORP/... dropped) has at least one token
     of >= 2 letters and is not wholly made of host-reference tokens (N3 test per token); for R2's bare "CO" form the
     token before the connector is not OF / AND / THE / IN / FOR (county / state abbreviations: "... OF CO SPRINGS"),
     the raw name has no "(" (parenthetical legal names: "... (TIPPECANOE CO CHILD CARE INC)") and the project side
     has a non-generic token; for R2 with the host on the LEFT ("X c/o Z"), Z must contain an organisation word
     (FUND, PROJECT, COALITION, TRUST, NETWORK, ...) and no addressee marker (LLP, LLC, ESQ, TREASURER, MANAGEMENT,
     OFFICE, ...), since such lines usually give a mailing addressee, not a project;
  N5 distinct projects per EIN: project keys are merged when they have the same token set or one is a >= 5-character
     prefix of a longer key for the same EIN (filers truncate names at 35-75 characters).
De facto host: >= 3 distinct projects (N5) from valid detections (N1-N4).
Host class (precedence order; BMF NTEE / FOUNDATION codes, else name regex): university_college, hospital_health,
  school_k12, religious_body, community_foundation_united_way, federated_national (name says NATIONAL/AMERICAN ...
  ASSOCIATION/SOCIETY with group exemption), else intermediary_other. Only intermediary_other hosts enter the
  headline "added" set; all classes are reported.

Weights: Schedule I dollars as filed (the exception-proxy basis), and `daf_weighted` = each sponsor-year's lines x its
DAF share of grants from sponsor-cost-structure.csv, capped at 1, as in mission_recipient_sectors.py. (Note:
mission_exception_load.py itself applies no DAF weighting; it drops totals rows and reports DAF-to-DAF lines.)

Pure functions; I/O only in `main`. Stdlib only.

Usage:
  python3 scripts/mission_de_facto_fiscal_sponsors.py . --np-cache NP --lines-cache LINES --bmf-dir BMF --pub78 P78 \
      --revocation REV --efile-index-dir IRS --bmf-archive-dir ARCH --fsd-html FSD.html [--out CSV] [--sample-out CSV]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from functools import reduce
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_exception_refined as mer  # noqa: E402
from mission_990_contractors import DATA, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_recipient_sectors import COST  # noqa: E402

mel = mer.mel
OUT = os.path.join(DATA, "de-facto-fiscal-sponsors-2026-11-20.csv")
FS_LIST = os.path.join(DATA, "fiscal-sponsor-ein-list-2026-11-19.csv")
MIN_PROJECTS = 3
SAMPLE_N = 30

RULES = (("fbo", re.compile(r"\bF ?B ?O\b|\bFOR (THE )?BENEFIT OF\b"), "left"),
         ("care_of", re.compile(r"\bIN CARE OF\b|\bC O\b|\bCO\b"), "right"),
         ("on_behalf_of", re.compile(r"\bON BEHALF OF\b|\bO B O\b|\bOBO\b"), "left"),
         ("project_of", re.compile(r"\bA PROJECT OF\b|\bFISCALLY SPONSORED BY\b|\bFISCAL SPONSOR (FOR|OF)\b"), "right"))
WEAK = mer.GENERIC | {"OF", "AND", "THE", "FOR", "IN", "AT", "TO", "ON", "INC", "CORP", "CO", "FDN", "FND", "ORG"}
BARE_CO_BLOCK = frozenset({"OF", "AND", "THE", "IN", "FOR"})
# "X c/o Z" with the host on the left usually names an addressee (a person, law firm or office), not a project: it
# counts only when Z carries an organisation word and no addressee marker.
ORG_WORD = re.compile(r"\b(FUND|PROJECT|COALITION|TRUST|NETWORK|ALLIANCE|CAMPAIGN|INITIATIVE|TABLE|COLLECTIVE|CENTER|"
                      r"CENTRE|PROGRAM|FOUNDATION|INSTITUTE|CLINIC|HOUSE|COUNCIL|COMMITTEE|ASSOCIATION|SOCIETY|ACTION|"
                      r"JUSTICE|MEDIA|LAB|LABS|COOPERATIVE|FARM|FARMERS|LEAGUE|MOVEMENT|PARTNERSHIP)\b")
ADDRESSEE = re.compile(r"\b(LLP|LLC|PC|PLLC|ESQ|CPA|TREASURER|MANAGEMENT|MANAGEMEN|MANAGE|MANA|OFFICE|ATTN|DEPT|"
                       r"BANK|NA|TRUSTEE|ADVISORS|FINANCIAL)\b")

HOST_CLASSES = (
    ("university_college", r"^B4|^B5", r"\bUNIVERSITY\b|\bCOLLEGE\b|\bUNIV\b"),
    ("hospital_health", r"^E2|^E3", r"\bHOSPITAL|\bHEALTH SYSTEM\b|\bMEDICAL CENTER\b|\bHEALTHCARE\b|\bCLINIC\b"),
    ("school_k12", r"^B2|^B3", r"\bSCHOOL\b|\bACADEMY\b|\bYESHIVA"),
    ("religious_body", r"^X", r"\bCHURCH\b|\bDIOCESE\b|\bARCHDIOCESE\b|\bSYNAGOGUE\b|\bCONGREGATION\b|\bTEMPLE\b|"
                               r"\bMINISTR(Y|IES)\b|\bPARISH\b|\bJUDAISM\b|\bCHABAD\b|\bMOSQUE\b|\bCONFERENCE\b"),
    ("community_foundation_united_way", r"^T31|^T70", r"\bCOMMUNITY FOUNDATION\b|\bUNITED WAY\b"),
)


# ----------------------------------------------------------------------------- detection (pure)
def toks(s: str) -> tuple:
    return tuple(mer.name_key(s).split())


def acronym(ws: Sequence[str]) -> str:
    return "".join(w[0] for w in ws if w not in ("OF", "AND", "THE", "FOR"))


def tok_hit(t: str, flat: frozenset, acr: frozenset, compact: frozenset) -> bool:
    """Token present in the reference names: exact, >= 3-character prefix of a reference token (truncation), the
    acronym (or a >= 3-character prefix of it) of a reference name, or a >= 5-character run-together substring."""
    return (t in flat or (len(t) >= 3 and (any(r.startswith(t) for r in flat) or any(a.startswith(t) for a in acr)))
            or (len(t) >= 5 and any(t in c for c in compact)))


def ref_parts(ref_sets: Sequence[tuple]) -> tuple:
    return (frozenset(t for r in ref_sets for t in r), frozenset(acronym(r) for r in ref_sets if len(r) >= 2),
            frozenset("".join(r) for r in ref_sets))


def side_matches(side: str, ref_sets: Sequence[tuple]) -> bool:
    ts = tuple(t for t in toks(side) if t not in WEAK)
    if not ts:
        return False
    flat, acr, compact = ref_parts(ref_sets)
    return 2 * sum(1 for t in ts if tok_hit(t, flat, acr, compact)) >= len(ts)


def first_connector(nm: str):
    hits = tuple((m.start(), i, rid, m, dflt) for i, (rid, rx, dflt) in enumerate(RULES) for m in (rx.search(nm),) if m)
    return min(hits, key=lambda h: (h[0], h[1])) if hits else None


def detect(name: str, ein: str, bmf_name: str, modal_name: str) -> dict | None:
    """One line -> detection dict (status valid / unverified / rejected:*) or None when no connector is present."""
    nm = mel.upname(name)
    c = first_connector(nm)
    if not c:
        return None
    _, _, rid, m, dflt = c
    left, right = nm[:m.start()].strip(), nm[m.end():].strip()
    base = {"rule": rid, "connector": m.group(0), "left": left, "right": right}
    rx = dict((r[0], r[1]) for r in RULES)[rid]
    if not ein:
        return {**base, "status": "rejected:blank_ein", "host": "", "project": "", "project_key": ""}
    if bmf_name and rx.search(mel.upname(bmf_name)):
        return {**base, "status": "rejected:legal_name", "host": "", "project": "", "project_key": ""}
    refs = tuple(r for r in (toks(bmf_name), toks(modal_name)) if r)
    ml, mr = side_matches(left, refs), side_matches(right, refs)
    host_side = ("left" if ml and not mr else "right" if mr and not ml else dflt)
    host, proj = (left, right) if host_side == "left" else (right, left)
    pk = " ".join(toks(proj))
    flat, acr, compact = ref_parts(refs)
    bare_co = rid == "care_of" and m.group(0) == "CO"
    prev = left.split()[-1] if left.split() else ""
    bad = ("empty_project" if not any(len(re.sub(r"[^A-Z]", "", t)) >= 2 for t in pk.split()) else
           "project_is_host" if all(tok_hit(t, flat, acr, compact) for t in pk.split()) else
           "bare_co_place" if bare_co and (prev in BARE_CO_BLOCK or "(" in name
                                           or not [t for t in pk.split() if t not in WEAK]) else
           "care_of_addressee" if rid == "care_of" and host_side == "left" and (
               not ORG_WORD.search(proj) or ADDRESSEE.search(proj)) else "")
    status = ("rejected:" + bad if bad else "valid" if (ml or mr) else "unverified")
    return {**base, "status": status, "host": host, "project": proj, "project_key": pk if not bad else ""}


def merge_projects(keys: Iterable[str]) -> dict:
    """{key: canonical key}: a key with the same token set as a longer-or-equal key, or that is a >= 5-character
    prefix of a longer key, maps to the first such key in (length desc, alphabetical) order."""
    ks = sorted(frozenset(keys), key=lambda k: (-len(k), k))
    def step(acc: dict, k: str) -> dict:
        tgt = next((c for c in dict.fromkeys(acc.values()) if c != k and (
            (len(k) >= 5 and c.startswith(k)) or frozenset(c.split()) == frozenset(k.split()))), k)
        return {**acc, k: tgt}
    return reduce(step, ks, {})


def modal_plain(lines: Iterable[tuple]) -> dict:
    """{ein: most frequent filed name among that EIN's lines with no connector} (ties: alphabetical)."""
    g = _group_by_fast(((e, mel.upname(n)) for e, n in lines if e and not first_connector(mel.upname(n))), lambda t: t[0])
    cnt = lambda v: _group_by_fast((n for _, n in v), lambda n: n)  # noqa: E731
    return {e: min(cnt(v).items(), key=lambda kv: (-len(kv[1]), kv[0]))[0] for e, v in g.items()}


def host_class(name: str, ntee: str, foundation: str, group: str) -> str:
    nm = mel.upname(name)
    if foundation == "10":
        return "religious_body"
    if foundation == "11":
        return "school_k12"
    if foundation == "12":
        return "hospital_health"
    return next((c for c, nt, rx in HOST_CLASSES if (ntee and re.match(nt, ntee)) or re.search(rx, nm)),
                "federated_national" if group not in ("", "0", "0000") and re.search(
                    r"\b(NATIONAL|AMERICAN|INTERNATIONAL)\b", nm) else "intermediary_other")


def sample(dets: Sequence[Mapping], n: int) -> tuple:
    h = lambda d: hashlib.sha1(f"{d['sponsor_ein']}|{d['fy']}|{d['idx']}".encode()).hexdigest()  # noqa: E731
    return tuple(sorted(dets, key=h)[:n])


# ----------------------------------------------------------------------------- re-cut of unions (pure)
def recut(flags: frozenset, ein: str, added: frozenset) -> frozenset:
    return flags | {"fiscal_sponsor_name", "any_si", "any_core_si"} if ein in added else flags


def pooled(keys: Sequence, screened: Mapping, fl: Mapping, fpart: Mapping) -> dict:
    t = reduce(mel.add, ({**mel.tally((r["amount"], f, r["d2d"]) for r, f in zip(screened[k], fl[k])), **fpart[k]}
                         for k in keys), {})
    s = mel.shares(t)
    return {k: s[k] for k in ("denom_lines", "denom_usd", "fiscal_sponsor_name_lines", "fiscal_sponsor_name_usd",
                              "fiscal_sponsor_name_count_share", "fiscal_sponsor_name_usd_share", "any_core_lines",
                              "any_core_usd", "any_core_count_share", "any_core_usd_share", "any_lines", "any_usd",
                              "any_count_share", "any_usd_share")}


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    for f in ("--np-cache", "--lines-cache", "--bmf-dir", "--pub78", "--revocation", "--efile-index-dir",
              "--bmf-archive-dir", "--fsd-html"):
        ap.add_argument(f, required=True)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--sample-out")
    a = ap.parse_args(argv)

    d = mer.load_screened(a)
    screened, period, item, present, panel, rank, good = (d[k] for k in ("screened", "period", "item", "present",
                                                                          "panel", "rank", "good"))
    base_flags = {k: tuple(mel.line_flags(r, period[k]["start"], period[k]["end"]) for r in rs) for k, rs in screened.items()}

    # --- refined fiscal-sponsor index and flags, rebuilt with mission_exception_refined's own functions (as its main)
    with open(a.fsd_html, encoding="utf-8", errors="replace") as fh:
        entries = mer.fsd_entries(fh.read())
    nkeys = frozenset(mer.name_key(re.split(r"\bdba\b", n, flags=re.I)[0]) for _, n, _ in entries)
    cities = frozenset((mer.state_of(l), mer.city_of(l)) for _, _, l in entries)
    q_eins = frozenset(e for e, b in d["bmf"].items() if mel.FISCAL_SPONSORS.search(mel.upname(b["name"])))
    exact, by_city, _ = mer.load_bmf_names(a.bmf_dir, nkeys, cities, q_eins)
    line_eins = {k: frozenset(e for e, _ in v) for k, v in _group_by_fast(
        ((r["ein"], mer.name_key(r["name"])) for rs in screened.values() for r in rs if r["ein"]), lambda t: t[1]).items()}
    fsd_rows = tuple(mer.key_from_lines(mer.match_entry(e, exact, by_city), line_eins, d["bmf"]) for e in entries)
    q19 = mer.q19_rows({e: d["bmf"][e] for e in q_eins})
    q19 = q19 + mer.q19_reported(((r["ein"], mel.upname(r["name"])) for rs in screened.values() for r in rs),
                                 frozenset(r["ein"] for r in q19))
    fsx = mer.fs_index(q19 + fsd_rows)
    fsd_names = frozenset(mer.name_key(n) for _, n, _ in entries)
    rr_eins = frozenset(r["ein"] for k, rs in screened.items() for r, f in zip(rs, base_flags[k]) if "recent_ruling_24m" in f)
    arch, sizes, groups = mer.load_archives(a.bmf_archive_dir, rr_eins)
    months = mer.complete_months({m: n for m, n in sizes.items() if not m.startswith("L")})
    legacy = tuple(sorted(m for m in arch if m.startswith("L")))
    revs = mer.load_revocations(a.revocation, rr_eins)
    efile = mer.load_efile_first(a.efile_index_dir, rr_eins)
    rr = {k: tuple(mer.classify(r["ein"], mer.ym(r["bmf_ruling"]), period[k]["start"], period[k]["end"], arch, months,
                                legacy, revs, efile, groups.get(r["ein"], ""), "church_or_religious" in r["labels"])
                   if "recent_ruling_24m" in f else None for r, f in zip(rs, base_flags[k]))
          for k, rs in screened.items()}
    ref_flags = {k: tuple(mer.refined_flags(r, f, fsx, x, fsd_names)[0] for r, f, x in zip(rs, base_flags[k], rr[k]))
                 for k, rs in screened.items()}

    # --- detections
    bmf = d["bmf"]
    modal = modal_plain((r["ein"], r["name"]) for rs in screened.values() for r in rs)
    raw = tuple({"sponsor_ein": k[0], "fy": k[1], "idx": i, "ein": r["ein"], "name": r["name"], "amount": r["amount"],
                 "d2d": r["d2d"], **x}
                for k, rs in screened.items() for i, r in enumerate(rs)
                for x in (detect(r["name"], r["ein"], bmf.get(r["ein"], {}).get("name", ""), modal.get(r["ein"], "")),) if x)
    valid = tuple(x for x in raw if x["status"] == "valid")
    canon = {e: merge_projects(x["project_key"] for x in v) for e, v in _group_by_fast(valid, lambda x: x["ein"]).items()}
    valid = tuple({**x, "project_canon": canon[x["ein"]][x["project_key"]]} for x in valid)
    by_ein = _group_by_fast(valid, lambda x: x["ein"])
    nproj = {e: len({x["project_canon"] for x in v}) for e, v in by_ein.items()}
    unver = {e: len(v) for e, v in _group_by_fast((x for x in raw if x["status"] == "unverified"), lambda x: x["ein"]).items()}

    det_eins = frozenset(by_ein)
    _, _, ext = mer.load_bmf_names(a.bmf_dir, frozenset(), frozenset(), det_eins | frozenset(fsx))
    cls = {e: host_class(bmf.get(e, {}).get("name", "") or modal.get(e, ""), ext.get(e, {}).get("NTEE_CD", ""),
                         bmf.get(e, {}).get("foundation", ""), bmf.get(e, {}).get("group", "")) for e in det_eins}
    de_facto = frozenset(e for e in det_eins if nproj[e] >= MIN_PROJECTS)
    de_facto_int = frozenset(e for e in de_facto if cls[e] == "intermediary_other")
    counted = frozenset(e for e, v in fsx.items() if not v["grantmaker"])
    fsd_eins = frozenset(e for e, v in fsx.items() if v["fsd"])
    q19_eins = frozenset(e for e, v in fsx.items() if v["q19"])
    added_int = de_facto_int - counted
    added_all = de_facto - counted

    # --- weights and per-EIN totals
    cost = read_csv(COST)
    share = {(ein9(r["ein"]), int(r["fiscal_year"])): num(r["daf_share_of_grants"]) for r in cost if r["daf_share_of_grants"]}
    wts = {k: min(1.0, max(0.0, share[k])) for k in good if share.get(k) is not None}
    flat = tuple((k, r) for k, rs in screened.items() for r in rs)
    tot = lambda pred, w=False: sum(r["amount"] * (wts.get(k, 1.0) if w else 1.0) for k, r in flat if pred(k, r))  # noqa: E731
    per = _group_by_fast(((k, r) for k, r in flat if r["ein"] in det_eins | fsd_eins | q19_eins), lambda t: t[1]["ein"])
    usd = {e: sum(r["amount"] for _, r in v) for e, v in per.items()}
    usd_w = {e: sum(r["amount"] * wts.get(k, 1.0) for k, r in v) for e, v in per.items()}

    # --- union re-cut
    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(mel.SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    keys = tuple(k for k in present if k in good)
    sf = {k: mel.sched_f_of(sf_rows.get(k)) for k in keys}
    fpart = {k: {**{x: sf[k][x] for x in ("f_usd", "f_recipients", "f_other_org_cnt")},
                 "f_total_grants": sf[k].get("f_total_grants", 0.0)} for k in keys}
    st = lambda k: mel.sponsor_type(k[0], panel[k[0]]["segment"])  # noqa: E731
    scopes = {"all_top50_itemising": keys, "big4_nationals": tuple(k for k in keys if k[0] in mel.BIG4),
              "national": tuple(k for k in keys if st(k) == "national"),
              "community_foundation": tuple(k for k in keys if st(k) == "community_foundation"),
              "faith": tuple(k for k in keys if st(k) == "faith")}
    cut = lambda added: {k: tuple(recut(f, r["ein"], added) for r, f in zip(screened[k], ref_flags[k])) for k in keys}  # noqa: E731
    variants = {"refined_as_published": ref_flags, "plus_de_facto_intermediary": cut(added_int),
                "plus_de_facto_all_classes": cut(added_all)}
    unions = {v: {s: pooled(ks, screened, fl, fpart) for s, ks in scopes.items()} for v, fl in variants.items()}
    si_usd = tot(lambda k, r: True)
    si_usd_w = tot(lambda k, r: True, True)
    denom = unions["refined_as_published"]["all_top50_itemising"]["denom_usd"]
    proj_lines_usd = lambda es: sum(x["amount"] for x in valid if x["ein"] in es)  # noqa: E731

    # --- outputs
    ex = lambda e: "; ".join(sorted({x["project_canon"] for x in by_ein.get(e, ())})[:6])  # noqa: E731
    rows = sorted(({"ein": e, "bmf_name": bmf.get(e, {}).get("name", ""), "modal_filed_name": modal.get(e, ""),
                    "bmf_state": bmf.get(e, {}).get("state", ""), "bmf_ntee": ext.get(e, {}).get("NTEE_CD", ""),
                    "bmf_foundation": bmf.get(e, {}).get("foundation", ""), "host_class": cls[e],
                    "distinct_projects": nproj[e], "project_style_lines": len(by_ein[e]),
                    "project_style_usd": round(sum(x["amount"] for x in by_ein[e])),
                    "unverified_lines": unver.get(e, 0),
                    "rules_hit": ";".join(sorted({x["rule"] for x in by_ein[e]})),
                    "sponsors": len({x["sponsor_ein"] for x in by_ein[e]}), "example_projects": ex(e),
                    "top50_lines": len(per.get(e, ())), "top50_usd": round(usd.get(e, 0)),
                    "top50_usd_daf_weighted": round(usd_w.get(e, 0)),
                    "in_directory": e in fsd_eins, "in_q19": e in q19_eins,
                    "in_refined_fs_flag": e in counted, "grantmaker_host": bool(fsx.get(e, {}).get("grantmaker")),
                    "de_facto_ge3": e in de_facto, "de_facto_intermediary": e in de_facto_int,
                    "added_headline": e in added_int} for e in det_eins),
                  key=lambda r: (-r["distinct_projects"], -r["top50_usd"], r["ein"]))
    write_csv(a.out, rows, tuple(rows[0]))
    smp = sample(valid, SAMPLE_N)
    if a.sample_out:
        sf_fields = ("sponsor_ein", "fy", "idx", "ein", "name", "amount", "rule", "host", "project", "project_canon")
        write_csv(a.sample_out, [{**{k: x[k] for k in sf_fields}, "bmf_name": bmf.get(x["ein"], {}).get("name", ""),
                                  "host_class": cls[x["ein"]]} for x in smp], sf_fields + ("bmf_name", "host_class"))
    miss = lambda es: sorted(({"ein": e, "name": bmf.get(e, {}).get("name", "") or modal.get(e, ""), "class": cls[e],  # noqa: E731
                               "projects": nproj[e], "top50_usd": round(usd.get(e, 0)), "in_q19": e in q19_eins,
                               "grantmaker_host": bool(fsx.get(e, {}).get("grantmaker"))} for e in es),
                             key=lambda z: -z["top50_usd"])
    fsd_with_lines = frozenset(e for e in fsd_eins if per.get(e))
    status_counts = {s: {"lines": len(v), "usd": round(sum(x["amount"] for x in v))}
                     for s, v in sorted(_group_by_fast(raw, lambda x: x["status"]).items())}
    summary = {
        "lines": sum(len(v) for v in screened.values()), "sched_i_usd": round(si_usd),
        "sched_i_usd_daf_weighted": round(si_usd_w), "daf_weight_coverage": f"{len(wts)}/{len(good)}",
        "connector_lines": len(raw), "status": status_counts,
        "valid_by_rule": {rid: {"lines": len(v), "usd": round(sum(x["amount"] for x in v))}
                          for rid, v in sorted(_group_by_fast(valid, lambda x: x["rule"]).items())},
        "eins_with_valid_detection": len(det_eins),
        "eins_by_projects": {n: sum(1 for e in det_eins if (nproj[e] if nproj[e] < 5 else 5) == n) for n in range(1, 6)},
        "de_facto_ge3": len(de_facto), "de_facto_ge2": sum(1 for e in det_eins if nproj[e] >= 2),
        "de_facto_by_class": {c: sum(1 for e in de_facto if cls[e] == c) for c in sorted({cls[e] for e in de_facto})},
        "de_facto_intermediary": len(de_facto_int),
        "de_facto_in_directory": len(de_facto & fsd_eins), "de_facto_in_q19": sorted(de_facto & q19_eins),
        "de_facto_intermediary_in_directory": len(de_facto_int & fsd_eins),
        "de_facto_intermediary_in_q19": len(de_facto_int & q19_eins),
        "de_facto_intermediary_already_counted": len(de_facto_int & counted),
        "directory_misses_intermediary": miss(de_facto_int - fsd_eins),
        "directory_misses_other_classes": miss((de_facto - de_facto_int) - fsd_eins),
        "q19_not_de_facto": sorted((e, bmf.get(e, {}).get("name", ""), nproj.get(e, 0)) for e in q19_eins - de_facto),
        "directory_eins": len(fsd_eins), "directory_eins_with_top50_lines": len(fsd_with_lines),
        "directory_eins_no_project_style_line": len(fsd_eins - det_eins),
        "directory_eins_with_lines_no_project_style_line": len(fsd_with_lines - det_eins),
        "directory_eins_with_lines_no_project_style_usd": round(sum(usd.get(e, 0) for e in fsd_with_lines - det_eins)),
        "directory_eins_with_project_style_line": len(fsd_eins & det_eins),
        "directory_top_no_project_style": miss_names(fsd_with_lines - det_eins, bmf, usd, 15),
        "added": {nm: {"eins": len(es), "lines": sum(len(per.get(e, ())) for e in es),
                       "usd": round(sum(usd.get(e, 0) for e in es)),
                       "usd_share_of_proxy_denom": mel.ratio(sum(usd.get(e, 0) for e in es), denom),
                       "usd_share_of_sched_i": mel.ratio(sum(usd.get(e, 0) for e in es), si_usd),
                       "usd_daf_weighted": round(sum(usd_w.get(e, 0) for e in es)),
                       "usd_share_daf_weighted": mel.ratio(sum(usd_w.get(e, 0) for e in es), si_usd_w),
                       "usd_ex_d2d": round(sum(r["amount"] for _, r in flat if r["ein"] in es and not r["d2d"])),
                       "project_style_lines_only_usd": round(proj_lines_usd(es)),
                       "project_style_lines_only_share": mel.ratio(proj_lines_usd(es), denom)}
                  for nm, es in (("intermediary", added_int), ("all_classes", added_all))},
        "added_intermediary_list": miss(added_int),
        "unions": unions,
        "sample_status": {s: sum(1 for x in smp if x["rule"] == s) for s in ("fbo", "care_of", "on_behalf_of", "project_of")},
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


def miss_names(es: Iterable[str], bmf: Mapping, usd: Mapping, n: int) -> list:
    return sorted(((e, bmf.get(e, {}).get("name", ""), round(usd.get(e, 0))) for e in es), key=lambda z: -z[2])[:n]


if __name__ == "__main__":
    raise SystemExit(main())
