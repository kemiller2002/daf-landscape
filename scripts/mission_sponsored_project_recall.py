#!/usr/bin/env python3
"""Sponsored projects filed under the project's own name with the host's EIN (queue item P-G050303-01).

The de facto fiscal-sponsor detection (mission_de_facto_fiscal_sponsors.py, the "FBO-name rule") only sees lines whose
recipient name spells out the host, e.g. "TIDES CENTER FBO X". Many filers instead write the project's own name and
the host's EIN, e.g. a project name on a line carrying Fractured Atlas's EIN 11-3451703. This script measures that
second form on the keyed fiscal-sponsor hosts and its effect on the fiscal-sponsor figures.

Universe and lines: exactly those of mission_exception_refined.load_screened (top-50 DAFRC sponsors, 94 itemising
sponsor-years, FY2023-24, totals rows dropped). Both repo scripts are imported and NOT modified:
  - mission_exception_refined: line loader, keyed host index (fs_index over the Q-B15 and Fiscal Sponsor Directory
    rows, rebuilt exactly as in mission_de_facto_fiscal_sponsors.main), name_key, refined_flags;
  - mission_de_facto_fiscal_sponsors: detect (FBO-name rule), modal_plain, toks / tok_hit / ref_parts, WEAK,
    merge_projects, host_class, pooled.

Keyed host EINs: the distinct EINs of fs_index (Q-B15 hosts + directory hosts keyed to an EIN; 347 in the 2026-11-19
list). `counted` = keyed and not a community-foundation / United Way directory host (the refined flag counts every
top-50 line to these EINs); `grantmaker` = keyed but excluded from the refined flag.

Rule NP (new, "own-name project"), on lines whose recipient EIN is keyed:
  the filed name has at least one non-generic token (mission_de_facto_fiscal_sponsors.WEAK removed after
  mission_exception_refined.name_key) and NONE of them is present in the EIN's reference names (current EO BMF name and
  the modal plain filed name for that EIN), using the same presence test as the FBO rule's host-side match (tok_hit:
  exact, >= 3-character prefix, acronym or acronym prefix, >= 5-character run-together substring).
Diagnostic class HX ("host plus extra"): some non-generic tokens are present and some are not, and the line is not a
  valid FBO-rule detection. Not flagged; reported as an unsampled bound on lines that neither rule separates.
FBO-rule detections are disjoint from NP by construction (a valid detection needs a matching host side). NP lines
  that the DAF-to-DAF whitelist marks (`d2d`) are set aside as `np_d2d` (a grant to another DAF sponsor, not a project).

Distinct NP projects per EIN: name keys merged with merge_projects (same token set / >= 5-character prefix).

Sensitivity (outside the keyed set, reported separately): for non-keyed EINs with >= 1 valid FBO-rule detection in
the intermediary class, NP lines are added to the distinct-project count and the >= 3 de facto threshold is re-applied.

Own-name check: for each NP line, other EINs whose current EO BMF name has the same name key (any state) are listed
(`own_name_bmf_eins`); a hit suggests the project has, or had, its own exemption, or that the filer used the wrong EIN.

Names in the CSV: the filed name is written only when it contains an organisation word (ORG_NAME) or was hand-checked
as organisational (--hand CSV); otherwise it is withheld, so that no individual's name is recorded.

Pure functions; I/O only in `main` and `load_*`. Stdlib only.

Usage:
  python3 scripts/mission_sponsored_project_recall.py . --np-cache NP --lines-cache LINES --bmf-dir BMF --pub78 P78 \
      --fsd-html FSD.html [--hand HAND.csv] [--sample-n 60] [--out CSV] [--sample-out CSV]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_de_facto_fiscal_sponsors as mdf  # noqa: E402
import mission_exception_refined as mer  # noqa: E402
from mission_990_contractors import DATA, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402

mel = mer.mel
OUT = os.path.join(DATA, "sponsored-project-recall-2026-11-20.csv")
SAMPLE_N = 60
GOVERNING = (35.1e6, 114.6e6)  # governing range of the >= 3-project de facto addition (g0503-03 §2.4, wave 44B)
ORG_NAME = re.compile(
    r"\b(FUND|FOUNDATION|PROJECT|COALITION|TRUST|NETWORK|ALLIANCE|CAMPAIGN|INITIATIVE|COLLECTIVE|CENTER|CENTRE|PROGRAM|"
    r"INSTITUTE|CLINIC|HOUSE|COUNCIL|COMMITTEE|ASSOCIATION|SOCIETY|ACTION|JUSTICE|MEDIA|LAB|LABS|COOPERATIVE|FARM|LEAGUE|"
    r"MOVEMENT|PARTNERSHIP|THEATER|THEATRE|ENSEMBLE|ORCHESTRA|CHORUS|CHOIR|COMPANY|DANCE|FILM|FESTIVAL|GALLERY|MUSEUM|"
    r"SCHOOL|ACADEMY|CLUB|CORPS|FRIENDS|PRESS|RADIO|REVIEW|JOURNAL|MAGAZINE|STUDIO|STUDIOS|WORKS|ARTS|ART|MUSIC|"
    r"FELLOWSHIP|SCHOLARSHIP|SCHOLARS|CIRCLE|PARTNERS|GROUP|COLLABORATIVE|CONSORTIUM|FEDERATION|UNION|ORGANIZATION|"
    r"ORGANIZING|BRIGADE|SANCTUARY|RESCUE|GARDEN|GARDENS|KITCHEN|PANTRY|SHELTER|LIBRARY|ARCHIVE|TABLE|VOICES|RISING|"
    r"PROGRAMS|SERVICES|RESOURCE|RESOURCES|SOLUTIONS|ENTERPRISE|VENTURES|COMMONS|HUB|AID|RELIEF|WATCH|LEGAL|DEFENSE|"
    r"POWER|VOTE|VOTERS|YOUTH|KIDS|CHILDREN|WOMEN|SISTERS|BROTHERS|NATION|NATIONS|TRIBE|INC|CORP|CORPORATION)\b")


# ----------------------------------------------------------------------------- classification (pure)
def name_tokens(name: str) -> tuple:
    return tuple(t for t in mdf.toks(name) if t not in mdf.WEAK)


def classify(name: str, refs: Sequence[tuple], fbo_valid: bool) -> str:
    """'np' (no non-generic token shared with the reference names), 'hx' (some shared, some not), 'host' (all shared),
    'generic' (no non-generic token), or 'fbo' (valid FBO-rule detection)."""
    if fbo_valid:
        return "fbo"
    ts = name_tokens(name)
    if not ts:
        return "generic"
    flat, acr, compact = mdf.ref_parts(refs)
    hit = tuple(mdf.tok_hit(t, flat, acr, compact) for t in ts)
    return "np" if not any(hit) else "host" if all(hit) else "hx"


def d2d_cut(cls: str, d2d: bool) -> str:
    """NP lines that the DAF-to-DAF whitelist marks are grants to another DAF sponsor, not projects: 'np_d2d'."""
    return "np_d2d" if cls == "np" and d2d else cls


def refs_of(ein: str, bmf: Mapping, modal: Mapping) -> tuple:
    return tuple(r for r in (mdf.toks(bmf.get(ein, {}).get("name", "")), mdf.toks(modal.get(ein, ""))) if r)


def shown_name(name: str, hand_org: bool) -> str:
    return name if hand_org or ORG_NAME.search(mel.upname(name)) else "[withheld: no organisation word]"


def hkey(sp: str, fy, idx) -> str:
    return hashlib.sha1(f"{sp}|{fy}|{idx}|np".encode()).hexdigest()


def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    if not n:
        return (None, None)
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (round(c - h, 4), round(c + h, 4))


def recall(fbo_true: float, np_true: float) -> float | None:
    return round(fbo_true / (fbo_true + np_true), 4) if fbo_true + np_true else None


def post_stratified(np_lines: Sequence[Mapping], judged: Sequence[tuple], tp) -> dict:
    """Estimated true-project NP lines and $: per host EIN, its sampled precision (lines; $) times its NP lines / $;
    hosts without a sampled line take the pooled precision over sampled lines."""
    if not judged:
        return {"lines": None, "usd": None}
    sj = _group_by_fast(judged, lambda t: t[0]["ein"])
    p_l = {e: sum(1 for _, h in v if tp(h)) / len(v) for e, v in sj.items()}
    p_u = {e: (sum(x["amount"] for x, h in v if tp(h)) / sum(x["amount"] for x, _ in v)) if sum(x["amount"] for x, _ in v)
           else p_l[e] for e, v in sj.items()}
    pool_l = sum(1 for _, h in judged if tp(h)) / len(judged)
    tot_u = sum(x["amount"] for x, _ in judged)
    pool_u = sum(x["amount"] for x, h in judged if tp(h)) / tot_u if tot_u else pool_l
    g = _group_by_fast(np_lines, lambda x: x["ein"])
    return {"lines": round(sum(len(v) * p_l.get(e, pool_l) for e, v in g.items()), 1),
            "usd": round(sum(sum(x["amount"] for x in v) * p_u.get(e, pool_u) for e, v in g.items())),
            "eins_sampled": len(sj), "eins_unsampled": len(set(g) - set(sj)),
            "unsampled_lines": sum(len(v) for e, v in g.items() if e not in sj),
            "unsampled_usd": round(sum(x["amount"] for e, v in g.items() if e not in sj for x in v))}


def keyed_index(d: Mapping, fsd_html: str, bmf_dir: str) -> tuple:
    """fs_index (EIN -> {q19, fsd, grantmaker}) rebuilt exactly as mission_de_facto_fiscal_sponsors.main does."""
    with open(fsd_html, encoding="utf-8", errors="replace") as fh:
        entries = mer.fsd_entries(fh.read())
    screened = d["screened"]
    nkeys = frozenset(mer.name_key(re.split(r"\bdba\b", n, flags=re.I)[0]) for _, n, _ in entries)
    cities = frozenset((mer.state_of(l), mer.city_of(l)) for _, _, l in entries)
    q_eins = frozenset(e for e, b in d["bmf"].items() if mel.FISCAL_SPONSORS.search(mel.upname(b["name"])))
    exact, by_city, _ = mer.load_bmf_names(bmf_dir, nkeys, cities, q_eins)
    line_eins = {k: frozenset(e for e, _ in v) for k, v in _group_by_fast(
        ((r["ein"], mer.name_key(r["name"])) for rs in screened.values() for r in rs if r["ein"]), lambda t: t[1]).items()}
    fsd_rows = tuple(mer.key_from_lines(mer.match_entry(e, exact, by_city), line_eins, d["bmf"]) for e in entries)
    q19 = mer.q19_rows({e: d["bmf"][e] for e in q_eins})
    q19 = q19 + mer.q19_reported(((r["ein"], mel.upname(r["name"])) for rs in screened.values() for r in rs),
                                 frozenset(r["ein"] for r in q19))
    return mer.fs_index(q19 + fsd_rows), frozenset(mer.name_key(n) for _, n, _ in entries)


def load_hand(path: str | None) -> dict:
    """{(sponsor_ein, fy, idx): {hand_class, hand_org, hand_note}} from a hand-check CSV (optional)."""
    if not path or not os.path.exists(path):
        return {}
    return {(r["sponsor_ein"], str(r["fiscal_year"]), str(r["line_index"])): r for r in read_csv(path)}


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".")
    for f in ("--np-cache", "--lines-cache", "--bmf-dir", "--pub78", "--fsd-html"):
        ap.add_argument(f, required=True)
    ap.add_argument("--hand")
    ap.add_argument("--sample-n", type=int, default=SAMPLE_N)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--sample-out")
    a = ap.parse_args(argv)

    d = mer.load_screened(a)
    screened, period, present, good, panel, bmf = (d[k] for k in ("screened", "period", "present", "good", "panel", "bmf"))
    fsx, fsd_names = keyed_index(d, a.fsd_html, a.bmf_dir)
    keyed = frozenset(fsx)
    counted = frozenset(e for e, v in fsx.items() if not v["grantmaker"])
    modal = mdf.modal_plain((r["ein"], r["name"]) for rs in screened.values() for r in rs)

    # every line, with its FBO-rule status and NP class
    lines = tuple({"sponsor_ein": k[0], "fy": k[1], "idx": i, "ein": r["ein"], "name": r["name"], "amount": r["amount"],
                   "d2d": bool(r["d2d"]),
                   "det": det, "cls": d2d_cut(classify(r["name"], refs_of(r["ein"], bmf, modal), bool(det and det["status"] == "valid")),
                                               bool(r["d2d"]))
                   if r["ein"] else "blank_ein"}
                  for k, rs in screened.items() for i, r in enumerate(rs)
                  for det in (mdf.detect(r["name"], r["ein"], bmf.get(r["ein"], {}).get("name", ""), modal.get(r["ein"], ""))
                              if r["ein"] else None,))
    kl = tuple(x for x in lines if x["ein"] in keyed)
    by_cls = lambda xs: {c: {"lines": len(v), "usd": round(sum(x["amount"] for x in v)),  # noqa: E731
                             "eins": len({x["ein"] for x in v})} for c, v in sorted(_group_by_fast(xs, lambda x: x["cls"]).items())}
    np_lines = tuple(x for x in kl if x["cls"] == "np")
    fbo_lines = tuple(x for x in kl if x["cls"] == "fbo")

    # hand-check sample (deterministic SHA-1 order) and estimates
    smp = tuple(sorted(np_lines, key=lambda x: hkey(x["sponsor_ein"], x["fy"], x["idx"]))[:a.sample_n])
    smp_ids = frozenset((x["sponsor_ein"], str(x["fy"]), str(x["idx"])) for x in smp)
    hx_smp = tuple(sorted((x for x in kl if x["cls"] == "hx"), key=lambda x: hkey(x["sponsor_ein"], x["fy"], x["idx"]))[:15])
    hand = load_hand(a.hand)
    hid = lambda x: (x["sponsor_ein"], str(x["fy"]), str(x["idx"]))  # noqa: E731
    judged = tuple((x, hand[hid(x)]) for x in smp if hid(x) in hand)
    # hand classes: project_confirmed (host directory or filing text names the host), project_likely, project_own_ein
    # (a same-name BMF entity predates the grant year), host_alias (former name / dba / acronym / full legal name),
    # host_program (host's own publication or programme). TP = the three project classes.
    tp = lambda h: h["hand_class"] in ("project_confirmed", "project_likely", "project_own_ein")  # noqa: E731
    k_tp = sum(1 for _, h in judged if tp(h))
    k_strict = sum(1 for _, h in judged if h["hand_class"] in ("project_confirmed", "project_likely"))
    k_conf = sum(1 for _, h in judged if h["hand_class"] == "project_confirmed")
    usd_j = sum(x["amount"] for x, _ in judged)
    usd_tp = sum(x["amount"] for x, h in judged if tp(h))
    prec = k_tp / len(judged) if judged else None
    prec_usd = usd_tp / usd_j if usd_j else None
    hx_judged = tuple((x, hand[hid(x)]) for x in hx_smp if hid(x) in hand)
    hx_all = tuple(x for x in kl if x["cls"] == "hx")
    hx_rate = sum(1 for _, h in hx_judged if tp(h)) / len(hx_judged) if hx_judged else 0.0
    hx_usd_j = sum(x["amount"] for x, _ in hx_judged)
    hx_rate_usd = sum(x["amount"] for x, h in hx_judged if tp(h)) / hx_usd_j if hx_usd_j else 0.0
    n_hx, usd_hx = len(hx_all), sum(x["amount"] for x in hx_all)

    # recall of the FBO-name rule on keyed hosts: valid FBO detections vs estimated true NP projects (lines and $).
    # FBO detections are taken at the g0503-03 sponsorship precision for intermediary hosts (19/21) and at 1.0.
    n_np, usd_np = len(np_lines), sum(x["amount"] for x in np_lines)
    n_fbo, usd_fbo = len(fbo_lines), sum(x["amount"] for x in fbo_lines)
    fbo_p = 19 / 21
    rec = ({"lines_fbo_p1": recall(n_fbo, prec * n_np), "lines_fbo_p0905": recall(fbo_p * n_fbo, prec * n_np),
            "usd_fbo_p1": recall(usd_fbo, prec_usd * usd_np), "usd_fbo_p0905": recall(fbo_p * usd_fbo, prec_usd * usd_np),
            "lines_fbo_p1_recall_low": recall(n_fbo, wilson(k_tp, len(judged))[1] * n_np),
            "lines_fbo_p1_recall_high": recall(n_fbo, wilson(k_tp, len(judged))[0] * n_np),
            "lines_fbo_p1_incl_hx": recall(n_fbo, prec * n_np + hx_rate * n_hx),
            "usd_fbo_p1_incl_hx": recall(usd_fbo, prec_usd * usd_np + hx_rate_usd * usd_hx),
            "hx_project_rate_lines": round(hx_rate, 4), "hx_project_rate_usd": round(hx_rate_usd, 4),
            "np_plus_fbo_rule_recall_lines_vs_hx": recall(n_fbo + prec * n_np, hx_rate * n_hx)}
           if judged else {})

    # post-stratified by host EIN: each sampled EIN's own sample precision applies to its unsampled NP lines; EINs with
    # no sampled line take the pooled precision of the sampled EINs (lines and $ separately)
    strat = post_stratified(np_lines, judged, tp)
    rec_strat = ({"lines_fbo_p1": recall(n_fbo, strat["lines"]), "usd_fbo_p1": recall(usd_fbo, strat["usd"]),
                  "lines_fbo_p0905": recall(fbo_p * n_fbo, strat["lines"]), "usd_fbo_p0905": recall(fbo_p * usd_fbo, strat["usd"]),
                  "lines_fbo_p1_incl_hx": recall(n_fbo, strat["lines"] + hx_rate * n_hx),
                  "usd_fbo_p1_incl_hx": recall(usd_fbo, strat["usd"] + hx_rate_usd * usd_hx)} if judged else {})

    # distinct NP projects per keyed EIN; hosts reaching >= 3 with FBO + NP
    fbo_all = tuple(x for x in lines if x["cls"] == "fbo")
    proj_key = lambda x: (x["det"]["project_key"] if x["cls"] == "fbo" else " ".join(mdf.toks(x["name"])))  # noqa: E731
    def nproj(xs: Sequence[Mapping]) -> dict:
        g = _group_by_fast(xs, lambda x: x["ein"])
        return {e: len(set(mdf.merge_projects(proj_key(x) for x in v).values())) for e, v in g.items()}
    np_proj = nproj(np_lines)
    fbo_proj_all = nproj(fbo_all)
    both_proj = nproj(tuple(x for x in lines if x["cls"] in ("fbo", "np") and (x["ein"] in keyed or x["ein"] in fbo_proj_all)))
    per_ein = _group_by_fast((x for x in lines if x["ein"]), lambda x: x["ein"])
    usd_e = {e: sum(x["amount"] for x in v) for e, v in per_ein.items()}

    # sensitivity outside the keyed set: non-keyed intermediary EINs with >= 1 valid FBO detection
    cand = frozenset(e for e in fbo_proj_all if e not in counted)
    np_keys = frozenset(mer.name_key(x["name"]) for x in np_lines + hx_smp)
    own, _, ext = mer.load_bmf_names(a.bmf_dir, np_keys, frozenset(), cand | keyed)
    own_bmf = lambda x: ";".join(sorted(f"{r['EIN']}:{r['STATE']}" for r in own.get(mer.name_key(x["name"]), ())  # noqa: E731
                                        if r["EIN"] != x["ein"]))
    cls_e = {e: mdf.host_class(bmf.get(e, {}).get("name", "") or modal.get(e, ""), ext.get(e, {}).get("NTEE_CD", ""),
                               bmf.get(e, {}).get("foundation", ""), bmf.get(e, {}).get("group", "")) for e in cand}
    cand_int = frozenset(e for e in cand if cls_e[e] == "intermediary_other")
    was3 = frozenset(e for e in cand_int if fbo_proj_all.get(e, 0) >= 3)
    now3 = frozenset(e for e in cand_int if both_proj.get(e, 0) >= 3)
    promoted = now3 - was3
    np_cand = tuple(x for x in lines if x["ein"] in cand_int and x["cls"] == "np")

    # proxy denominator and refined fiscal-sponsor figure (fs part of refined_flags needs no ruling data)
    keys = tuple(k for k in present if k in good)
    sf_rows = {(ein9(r["ein"]), int(r["fiscal_year"])): r for r in read_csv(mel.SCHED_F_CSV) if r["row_type"] == "sponsor_year"}
    sf = {k: mel.sched_f_of(sf_rows.get(k)) for k in keys}
    fpart = {k: {**{x: sf[k][x] for x in ("f_usd", "f_recipients", "f_other_org_cnt")},
                 "f_total_grants": sf[k].get("f_total_grants", 0.0)} for k in keys}
    base = {k: tuple(mel.line_flags(r, period[k]["start"], period[k]["end"]) for r in screened[k]) for k in keys}
    denom = mdf.pooled(keys, screened, base, fpart)["denom_usd"]
    fs_usd = sum(r["amount"] for k in keys for r, f in zip(screened[k], base[k])
                 if "fiscal_sponsor_name" in mer.refined_flags(r, f, fsx, None, fsd_names)[0])
    np_counted = tuple(x for x in np_lines if x["ein"] in counted)
    np_gm = tuple(x for x in np_lines if x["ein"] not in counted)

    # --- CSV: one row per NP line on keyed EINs (+ the HX diagnostic sample)
    rows = sorted(({"sponsor_ein": x["sponsor_ein"], "sponsor_name": panel[x["sponsor_ein"]]["name"], "fiscal_year": x["fy"],
                    "line_index": x["idx"], "recipient_ein": x["ein"],
                    "host_bmf_name": bmf.get(x["ein"], {}).get("name", ""), "host_modal_filed_name": modal.get(x["ein"], ""),
                    "host_in_q19": fsx[x["ein"]]["q19"], "host_in_directory": fsx[x["ein"]]["fsd"],
                    "host_counted_in_refined_flag": x["ein"] in counted,
                    "filed_name": shown_name(x["name"], hand.get(hid(x), {}).get("hand_org", "") == "yes"),
                    "rule_class": x["cls"], "connector_status": (x["det"] or {}).get("status", ""),
                    "amount_usd": round(x["amount"]), "d2d": x["d2d"],
                    "in_sample": "np60" if hid(x) in smp_ids else ("hx15" if x in hx_smp else ""),
                    "own_name_bmf_eins": own_bmf(x),
                    "hand_class": hand.get(hid(x), {}).get("hand_class", ""),
                    "hand_note": hand.get(hid(x), {}).get("hand_note", "")}
                   for x in np_lines + hx_smp),
                  key=lambda r: (r["recipient_ein"], r["sponsor_ein"], str(r["fiscal_year"]), int(r["line_index"])))
    write_csv(a.out, rows, tuple(rows[0]))
    if a.sample_out:
        write_csv(a.sample_out, [{"sample": s, "sponsor_ein": x["sponsor_ein"], "fiscal_year": x["fy"], "line_index": x["idx"],
                                  "oid": present[(x["sponsor_ein"], x["fy"])]["oid"], "recipient_ein": x["ein"],
                                  "name": x["name"], "amount": round(x["amount"]),
                                  "host_bmf_name": bmf.get(x["ein"], {}).get("name", ""), "modal": modal.get(x["ein"], "")}
                                 for s, xs in (("np60", smp), ("hx15", hx_smp)) for x in xs],
                  ("sample", "sponsor_ein", "fiscal_year", "line_index", "oid", "recipient_ein", "name", "amount",
                   "host_bmf_name", "modal"))

    top_hosts = sorted(_group_by_fast(np_lines, lambda x: x["ein"]).items(), key=lambda kv: -sum(x["amount"] for x in kv[1]))[:15]
    summary = {
        "lines": len(lines), "sched_i_usd": round(sum(x["amount"] for x in lines)), "proxy_denom_usd": round(denom),
        "refined_fs_usd_check": round(fs_usd),
        "keyed_eins": len(keyed), "keyed_counted": len(counted), "keyed_grantmaker": len(keyed - counted),
        "keyed_eins_with_lines": len({x["ein"] for x in kl}),
        "keyed_lines": len(kl), "keyed_usd": round(sum(x["amount"] for x in kl)),
        "keyed_by_class": by_cls(kl),
        "keyed_counted_by_class": by_cls(tuple(x for x in kl if x["ein"] in counted)),
        "np_by_sponsor": {f"{panel[s]['name'][:35]} ({s})": {"lines": len(v), "usd": round(sum(x["amount"] for x in v))}
                          for s, v in sorted(_group_by_fast(np_lines, lambda x: x["sponsor_ein"]).items(), key=lambda kv: -len(kv[1]))},
        "np_top_hosts": [(e, bmf.get(e, {}).get("name", "") or modal.get(e, ""), len(v), round(sum(x["amount"] for x in v)),
                          np_proj.get(e, 0), e in counted) for e, v in top_hosts],
        "np_eins": len(np_proj), "np_eins_by_projects": {n: sum(1 for v in np_proj.values() if min(v, 5) == n) for n in range(1, 6)},
        "np_counted": {"lines": len(np_counted), "usd": round(sum(x["amount"] for x in np_counted))},
        "np_grantmaker_hosts": {"lines": len(np_gm), "usd": round(sum(x["amount"] for x in np_gm)), "eins": len({x["ein"] for x in np_gm})},
        "np_own_name_in_bmf": {"lines": sum(1 for x in np_lines if own_bmf(x)),
                               "usd": round(sum(x["amount"] for x in np_lines if own_bmf(x)))},
        "np_connector_status": {s: len(v) for s, v in _group_by_fast(np_lines, lambda x: (x["det"] or {}).get("status", "none")).items()},
        "sample": {"n": len(smp), "judged": len(judged), "tp": k_tp, "tp_strict": k_strict, "confirmed": k_conf,
                   "precision_confirmed": round(k_conf / len(judged), 4) if judged else None,
                   "precision_lines": round(prec, 4) if prec is not None else None, "wilson95": wilson(k_tp, len(judged)),
                   "precision_strict": round(k_strict / len(judged), 4) if judged else None,
                   "wilson95_strict": wilson(k_strict, len(judged)),
                   "precision_usd": round(prec_usd, 4) if prec_usd is not None else None,
                   "usd_sampled": round(usd_j), "by_class": {c: len(v) for c, v in _group_by_fast(judged, lambda t: t[1]["hand_class"]).items()},
                   "distinct_hosts": len({x["ein"] for x in smp}),
                   "by_sponsor": {s: len(v) for s, v in _group_by_fast(smp, lambda x: panel[x["sponsor_ein"]]["name"][:30]).items()}},
        "hx_sample": {"n": len(hx_smp), "judged": len(hx_judged),
                      "by_class": {c: len(v) for c, v in _group_by_fast(hx_judged, lambda t: t[1]["hand_class"]).items()}},
        "fbo_on_keyed": {"lines": n_fbo, "usd": round(usd_fbo), "eins": len({x["ein"] for x in fbo_lines})},
        "np_on_keyed": {"lines": n_np, "usd": round(usd_np)},
        "np_true_est": {"lines": round(prec * n_np, 1), "usd": round(prec_usd * usd_np)} if judged else None,
        "fbo_recall": rec,
        "np_true_est_post_stratified": strat, "fbo_recall_post_stratified": rec_strat,
        "keyed_hosts_ge3": {"fbo_only": sum(1 for e in keyed if fbo_proj_all.get(e, 0) >= 3),
                            "fbo_plus_np": sum(1 for e in keyed if both_proj.get(e, 0) >= 3),
                            "np_only_ge3": sum(1 for e in keyed if np_proj.get(e, 0) >= 3)},
        "added_to_refined_fs_flag_usd": 0,
        "added_note": "every top-50 line to a counted keyed EIN is already in the refined EIN-keyed flag",
        "grantmaker_np_share_of_denom": mel.ratio(sum(x["amount"] for x in np_gm), denom),
        "sensitivity_nonkeyed": {"cand_eins": len(cand), "cand_intermediary": len(cand_int), "was_ge3": len(was3),
                                 "now_ge3": len(now3), "promoted": len(promoted),
                                 "np_lines_on_cand_int": len(np_cand), "np_usd_on_cand_int": round(sum(x["amount"] for x in np_cand)),
                                 "promoted_list": sorted(((e, bmf.get(e, {}).get("name", "") or modal.get(e, ""),
                                                           fbo_proj_all.get(e, 0), both_proj.get(e, 0), round(usd_e.get(e, 0)),
                                                           len(per_ein.get(e, ()))) for e in promoted), key=lambda z: -z[4]),
                                 "promoted_usd": round(sum(usd_e.get(e, 0) for e in promoted)),
                                 "promoted_lines": sum(len(per_ein.get(e, ())) for e in promoted),
                                 "promoted_share_of_denom": mel.ratio(sum(usd_e.get(e, 0) for e in promoted), denom)},
        "governing_range_usd": GOVERNING,
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
