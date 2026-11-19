#!/usr/bin/env python3
"""Resolve unlisted top-50 Schedule I recipients by name and state (queue item P-B41N17-01).

Two pools of FY2023-24 top-50 Schedule I lines from P-NEW-REC-01 (mission_recipient_compliance.py):

  ein_unlisted  the recipient EIN is in neither Pub 78 nor the EO BMF and the line carries none of the six
                explaining labels (government, church/religious, foreign, group subordinate, possible public
                university, LLC). P-NEW-REC-01: 12,265 lines, $818.7m.
  blank_ein     blank or placeholder EIN. P-NEW-REC-01: 5,013 lines, $644.0m, which includes Greater Horizons'
                FY2024 e-file totals rows (two lines, $212,187,406 + 3,282; dropped here as in
                mission_exception_load.drop_totals_rows).

Each distinct (filed EIN, normalised name, state) key is matched against every EO BMF and Pub 78 record by a
deterministic token matcher (published rules, `MATCH RULES` below):

  normalise     upper case; '&' -> AND; apostrophes removed; other non-alphanumerics -> space; abbreviations
                expanded (ABBR); stop and legal-form words dropped (STOP); the token SET is compared.
  score         Jaccard = |A & B| / |A | B| on those token sets.
  tiers         A  score == 1 and same state;
                B  score >= 0.80 and same state (targets with >= 2 tokens only), and the two token sets do not
                   differ by an entity-marking token (DISTINGUISH: FOUNDATION, ENDOWMENT, LEGACY, II, ...);
                C  score == 1, different state (targets with >= 2 tokens only).
                The best tier wins (A > B > C, then higher score). If more than one distinct EIN ties at the best
                (tier, score), the key is `ambiguous`.
  blocking      exact, not heuristic: a candidate must share one of the target's k rarest tokens (document
                frequency over BMF + Pub 78 names), k = floor(0.2 * n) + 1 for an n-token target. Any record with
                Jaccard >= 0.80 shares at least n - floor(0.2 n) of the target's tokens, so it cannot miss all k.

Classes (`resolution`):
  matched_listed_other_ein   tier A/B/C match to a listed charity (Pub 78, or BMF subsection 03) under a different
                             EIN. For ein_unlisted this is sponsor EIN misreporting; for blank_ein it is an
                             identifiable listed grantee whose EIN was omitted.
  matched_bmf_non_c3         best match is a BMF record with subsection other than 03 and not in Pub 78.
  ambiguous                  several EINs tie at the best tier.
  unmatched_*                no candidate passes: split by foreign address, the P-NEW-REC-01 explaining labels
                             (`labelled_*`, blank-EIN pool only), the filed EIN's revocation record (`revoked_ein`), extended public-body and religious name rules (wave 34B: BMF-absent
                             EINs are often subsidiaries and government bodies), no name, else `unmatched_other`
                             (genuinely unrecognised on 2026-11 lists).

A deterministic 40-key sample of matches (sha1 of the key; 20 per pool, stratified by tier) is flagged
`handcheck_sample`; the reviewer's verdicts are held in HANDCHECK and applied on output.

Pure functions over immutable inputs; I/O only in loaders and `main`. Stdlib only.

Usage:
  python3 scripts/mission_unlisted_recipients.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
      --pub78 data-download-pub78.txt --revocation data-download-revocation.txt [--out PATH]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, DATA, _group_by_fast, ein9, read_csv, write_csv  # noqa: E402
from mission_daf_to_daf import FYS, TOP_N, load_np, pick_returns, top_n  # noqa: E402
from mission_exception_load import is_totals_row, _amt  # noqa: E402
from mission_net_payout import itemized, norm_name, panel_from  # noqa: E402
from mission_recipient_compliance import (EXPLAINING, load_bmf_ext, load_pub78, load_revocations,  # noqa: E402
                                          period_of, screen)
from mission_recipient_sectors import BMF_FILES, WHITELIST, annotate, load_lines  # noqa: E402

OUT = os.path.join(DATA, "unlisted-recipients-resolution-2026-11-19.csv")
SOURCE = ("IRS Form 990 Schedule I Part II lines, top-50 DAFRC sponsors FY2023-24 (P-NEW-REC-01 line cache; e-file "
          "XML via GivingTuesday mirror of IRS TEOS) matched by name+state to IRS EO BMF (Last-Modified 2026-11-09) "
          "and Pub 78 (Last-Modified 2026-11-11); revocation list 2026-11-11")

# ----------------------------------------------------------------------------- MATCH RULES (published)
ABBR = {"FDN": "FOUNDATION", "FNDN": "FOUNDATION", "FOUND": "FOUNDATION", "FOUNDATIO": "FOUNDATION",
        "ASSN": "ASSOCIATION", "ASSOC": "ASSOCIATION", "CTR": "CENTER", "CENTRE": "CENTER", "CNTR": "CENTER",
        "INTL": "INTERNATIONAL", "NATL": "NATIONAL", "UNIV": "UNIVERSITY", "ST": "SAINT", "STE": "SAINT",
        "MT": "MOUNT", "SCH": "SCHOOL", "SVCS": "SERVICES", "SVC": "SERVICE", "DEPT": "DEPARTMENT",
        "COMM": "COMMUNITY", "CMNTY": "COMMUNITY", "AMER": "AMERICA", "AMERICAN": "AMERICA", "HOSP": "HOSPITAL",
        "MUS": "MUSEUM", "SOC": "SOCIETY", "COUN": "COUNCIL", "CNCL": "COUNCIL", "ORG": "ORGANIZATION",
        "BROS": "BROTHERS", "SCHS": "SCHOOLS", "ACAD": "ACADEMY", "INST": "INSTITUTE", "PROG": "PROGRAM",
        "USA": "US", "U": "US"}
STOP = frozenset({"THE", "OF", "AND", "FOR", "A", "AN", "IN", "AT", "TO", "ON", "BY", "INC", "INCORPORATED", "CORP",
                  "CORPORATION", "CO", "COMPANY", "LTD", "LIMITED", "LLC", "L", "C", "PC", "NFP", "NP", "NPC", "DBA",
                  "AKA", "FKA", "TRUST", "FUND"})
# TRUST and FUND are dropped because sponsors routinely append or omit them ("X Foundation Fund", "X Trust");
# FOUNDATION is kept because "X" and "X Foundation" are often distinct EINs.
J_MIN = 0.80
TIER_RANK = {"A": 3, "B": 2, "C": 1}
# Tier B may not differ by a token that usually marks a separate legal entity ("X" vs "X Foundation",
# "X Schools" vs "X Schools II", "X University" vs "X University Foundation").
DISTINGUISH = frozenset({"FOUNDATION", "ENDOWMENT", "LEGACY", "II", "III", "IV", "2", "3", "AUXILIARY", "ALUMNI",
                         "FRIENDS", "SUPPORTING", "PARENTS", "BOOSTER", "BOOSTERS", "GUILD", "ACTION", "PAC",
                         "VOTES", "INTERNATIONAL", "GLOBAL", "PROPERTY", "HOLDINGS", "CHARITABLE", "SCHOLARSHIP",
                         "MEMORIAL", "AFFILIATES", "ASSOCIATES", "CHAPTER", "AUXILLARY"})

PUBLIC_EXT = re.compile(r"\b(STATE OF|UNIVERSITY OF|STATE UNIVERSITY|MEDICAL CENTER|HEALTH SCIENCE CENTER|"
                        r"AUTHORITY|COMMISSION|DISTRICT|MUNICIPAL|COUNTY|CITY|PUBLIC|GOVERNMENT|NATION|TRIBE|"
                        r"BOARD|AGENCY|DEPARTMENT|POLICE|FIRE|SHERIFF|COURT|LIBRARY|SCHOOLS)\b")
RELIGIOUS_EXT = re.compile(r"\b(AHAVAS|AHAVAT|BETH|BAIS|BNEI|KEHILAT|KEHILLAT|KHAL|AGUDAS|AGUDATH|CHEVRA|MIKVAH|"
                           r"MIKVEH|OHEL|TIFERES|ZICHRON|KOLEL|BAPTIST|LUTHERAN|METHODIST|PRESBYTERIAN|"
                           r"EPISCOPAL|CATHOLIC|MINISTRY|MINISTRIES|GOSPEL|BIBLE|CHRISTIAN|EVANGELICAL|IGLESIA|"
                           r"MISSION|PARISH|SHRINE|DIOCESE|ORTHODOX|JEWISH|ISLAMIC|MUSLIM|HINDU|BUDDHIST|SIKH|"
                           r"GURDWARA|VEDANTA|MANDIR)\b")
LABEL_ORDER = ("government", "church_or_religious", "possible_public_university", "llc_possible_disregarded_entity",
               "group_subordinate", "foreign")
SUBSIDIARY_EXT = re.compile(r"\b(LLC|L L C|LP|TRUST|ENDOWMENT|SUPPORTING|AUXILIARY|FRIENDS OF|ALUMNI)\b")


def tokens(name: str) -> frozenset:
    s = (name or "").upper().replace("&", " AND ").replace("'", "").replace("’", "")
    raw = re.sub(r"[^A-Z0-9 ]", " ", s).split()
    return frozenset(t for t in (ABBR.get(x, x) for x in raw) if t not in STOP)


def jaccard(a: frozenset, b: frozenset) -> float:
    return len(a & b) / len(a | b) if a and b else 0.0


def block_tokens(toks: frozenset, df: Mapping) -> tuple:
    k = math.floor(0.2 * len(toks)) + 1
    return tuple(sorted(toks, key=lambda t: (df.get(t, 0), t))[:k])


def tier_of(a: frozenset, b: frozenset, same_state: bool):
    score, n = jaccard(a, b), len(a)
    if score >= 1.0 and same_state:
        return "A"
    if n >= 2 and score >= J_MIN and same_state and not ((a ^ b) & DISTINGUISH):
        return "B"
    if n >= 2 and score >= 1.0:
        return "C"
    return None


def best_match(target: Mapping, cands: Iterable[Mapping]) -> dict:
    """Pure: choose the best reference record for one target. cands are merged per-EIN reference records."""
    scored = tuple((tier_of(target["toks"], c["toks"], bool(target["state"]) and target["state"] == c["state"]),
                    jaccard(target["toks"], c["toks"]), c)
                   for c in cands if c["ein"] != target["ein"])
    ok = tuple(s for s in scored if s[0])
    if not ok:
        return {"tier": "", "score": max((s[1] for s in scored), default=0.0), "n_best": 0, "ref": None}
    top = max(ok, key=lambda s: (TIER_RANK[s[0]], s[1]))
    best = tuple(s for s in ok if (s[0], s[1]) == (top[0], top[1]))
    eins = sorted({s[2]["ein"] for s in best})
    # prefer a listed record if exactly one of the tied EINs is listed
    listed = sorted({s[2]["ein"] for s in best if s[2]["listed"]})
    pick = listed[0] if len(listed) == 1 else eins[0]
    ref = next(s[2] for s in best if s[2]["ein"] == pick)
    n_best = 1 if (len(eins) == 1 or len(listed) == 1) else len(eins)
    return {"tier": top[0], "score": top[1], "n_best": n_best, "ref": ref}


def ein_distance(a: str, b: str) -> str:
    """'transposition' (one adjacent swap), else Hamming distance over 9 digits."""
    if not a or not b:
        return ""
    if any(a[:i] + a[i + 1] + a[i] + a[i + 2:] == b for i in range(8)):
        return "transposition"
    return str(sum(x != y for x, y in zip(a, b)))


def typo_like(d: str) -> bool:
    return d == "transposition" or (d.isdigit() and int(d) <= 2)


def resolve(t: Mapping, m: Mapping, revoked: bool) -> str:
    ref = m["ref"]
    if ref is not None and m["n_best"] == 1:
        return "matched_listed_other_ein" if ref["listed"] else "matched_bmf_non_c3"
    if ref is not None:
        return "ambiguous"
    up = (t["name"] or "").upper()
    if not up.strip():
        return "unmatched_no_name"
    if t["where"].startswith("F:"):
        return "unmatched_foreign_address"
    lab = next((x for x in LABEL_ORDER if x in t["labels"]), "")
    if lab:  # blank-EIN pool only: the P-NEW-REC-01 explaining labels (the ein_unlisted pool has none by definition)
        return "unmatched_labelled_" + lab
    if revoked:
        return "unmatched_revoked_ein"
    if PUBLIC_EXT.search(up):
        return "unmatched_public_body_name"
    if RELIGIOUS_EXT.search(up):
        return "unmatched_religious_name"
    if SUBSIDIARY_EXT.search(up):
        return "unmatched_subsidiary_or_fund_name"
    return "unmatched_other"


def withhold(r: Mapping) -> dict:
    """Blank-EIN lines that match no IRS-listed organisation may name individuals (P-NEW-REC-01 kept blank-EIN
    lines out of its hit rows for this reason): their name and key are replaced by a hash; state and dollars stay."""
    if r["pool"] != "blank_ein" or r["resolution"].startswith("matched") or r["resolution"] == "ambiguous":
        return {**r, "name_withheld": 0}
    return {**r, "key": "blank_ein|withheld|" + sample_key(r["key"])[:16], "filed_name": "", "name_withheld": 1}


def sample_key(k: str) -> str:
    return hashlib.sha1(k.encode("utf-8")).hexdigest()


def draw_sample(rows: Sequence[Mapping], per_pool: int) -> frozenset:
    """Deterministic, tier-stratified: per pool, allocate per_pool across tiers in proportion to key counts
    (largest remainder; at least 1 per non-empty tier), then take the lowest sha1 keys."""
    def pool_pick(pool):
        m = [r for r in rows if r["pool"] == pool and r["resolution"] == "matched_listed_other_ein"]
        by = _group_by_fast(m, lambda r: r["match_tier"])
        tot = len(m)
        base = {t: max(1, math.floor(per_pool * len(v) / tot)) for t, v in by.items()} if tot else {}
        rem = per_pool - sum(base.values())
        order = sorted(by, key=lambda t: -(per_pool * len(by[t]) / tot - math.floor(per_pool * len(by[t]) / tot)))
        alloc = {t: base[t] + (1 if i < rem else 0) for i, t in enumerate(order)}
        return [r["key"] for t, v in by.items() for r in sorted(v, key=lambda r: sample_key(r["key"]))[:alloc[t]]]
    return frozenset(pool_pick("ein_unlisted") + pool_pick("blank_ein"))


# Reviewer verdicts on the 40 sampled keys (filled after inspection; see the research note, section 3.3).
# key -> (verdict, note). verdict: correct | wrong | unsure.
HANDCHECK: Mapping[str, tuple] = {
    'blank_ein||CATHOLIC CHURCH MATTHEWS SAINT|AZ': ('wrong', 'different state (MS); common parish name'),
    'blank_ein||CATHOLIC II JOHN PAUL SCHOOL|KS': ('wrong', 'different state (TX); common school name'),
    'blank_ein||CHURCH COMMUNITY LIVE OAKS|FL': ('correct', 'same name and state, unique listing'),
    'blank_ein||CHURCH HILL METHODIST PLEASANT UNITED|NC': ('wrong', 'different state (AL); common church name'),
    'blank_ein||CHURCH EDGE WATERS|NE': ('correct', "same name and state (apostrophe and 'The' only)"),
    'blank_ein||CHURCH CONGREGATIONAL PLYMOUTH|KS': ('correct', 'same name and state, unique listing'),
    'blank_ein||CHURCH GOOD METHODIST SHEPHERD UNITED|NC': ('wrong', "candidate is a truncated 'United Church of [Christ]' name; Methodist token missing"),
    'blank_ein||CENTER CRISIS LOMPOC PREGNANCY|CA': ('correct', 'distinctive name, same state'),
    'blank_ein||CHURCH COMMUNITY CREEK OAK|IN': ('correct', 'same name and state'),
    'blank_ein||BAPTIST BASEHOR CHURCH FIRST|KS': ('correct', 'same name, same town in name'),
    'blank_ein||CHURCH NORTHLAKE|WA': ('correct', 'same name and state, unique listing'),
    'blank_ein||CATHOLIC CHURCH DE FRANCIS SAINT SALES|OH': ('wrong', 'different state (CO); common parish name'),
    'blank_ein||CHURCH RESURRECTION|NC': ('unsure', 'generic church name; one NC listing but grantee town unknown'),
    'blank_ein||COLLEGE MARYS SAINT|IN': ('correct', "Saint Mary's College, Notre Dame IN"),
    'blank_ein||JOSEPHS PREPARATORY SAINT SCHOOL|PA': ('correct', "St Joseph's Prep, Philadelphia"),
    'blank_ein||ANDREWS CHURCH LUTHERAN SAINT|MN': ('correct', "same parish name plus 'Evangelical', same state"),
    'blank_ein||JEWISH METRO SERVICE VOCATIONAL WEST|NJ': ('correct', 'identical distinctive name and state'),
    'blank_ein||PROVIDENT|MO': ('correct', 'Provident Inc., St Louis; single listing'),
    'blank_ein||BAPTIST CHURCH PENINSULA|NC': ('wrong', 'different state (WI); common church name'),
    'blank_ein||BAPTIST CHURCH SMITHFIELD|VA': ('correct', 'same name and town'),
    'ein_unlisted|042121654|ACADEMY URSULINE|MA': ('wrong', 'different state (DE); Ursuline Academy Dedham MA is a different school'),
    'ein_unlisted|871190119|NOVA SCHOOL TERRA|CA': ('wrong', 'different state (MN)'),
    'ein_unlisted|900666071|MINISTRIES PERFECTING|NJ': ('wrong', 'different state (NM)'),
    'ein_unlisted|942495928|ELIZABETH SAINT SCHOOL SETON|CA': ('unsure', "'Elizabeth Ann Seton' vs 'Elizabeth Seton'; several CA schools"),
    'ein_unlisted|596033527|CATHOLIC LADY LOURDES OUR SCHOOL|FL': ('wrong', 'different state (GA)'),
    'ein_unlisted|591296888|CATHOLIC HEART SACRED SCHOOL|FL': ('unsure', 'generic school name; one FL listing'),
    'ein_unlisted|813674636|GULF LATIN POINTE SCHOOL|FL': ('correct', 'distinctive name, same state'),
    'ein_unlisted|853567178|DOLLAR MILLION WOMEN|NY': ('correct', 'same name and state; EINs differ by one digit'),
    'ein_unlisted|841878535|BC SPORTS|CT': ('wrong', 'different state (LA)'),
    'ein_unlisted|760520329|CATHOLIC CENTER CHARISMATIC|TX': ('wrong', 'different state (NM); the TX centre is in Houston'),
    'ein_unlisted|003425760|HEART SACRED SCHOOL|IL': ('unsure', 'generic school name; one IL listing'),
    'ein_unlisted|351168812|COMMUNITY HIGH SCHOOL ZIONSVILLE|IN': ('wrong', "candidate is the school's PTO, a separate entity"),
    'ein_unlisted|261420469|CHRIST KING SCHOOL|VT': ('correct', 'same name and state'),
    'ein_unlisted|300006089|COMMUNITY DEAF DIEGO SAN SERVICES|CA': ('correct', 'same name and state; EINs differ by one digit'),
    'ein_unlisted|411543466|CHAMBER ISLAND MADELINE MUSIC|MN': ('correct', 'distinctive name, same state'),
    'ein_unlisted|874387592|EYES MINISTRIES UP|CO': ('wrong', 'different state (FL)'),
    'ein_unlisted|150532164|LADY LOURDES OUR|NY': ('unsure', "candidate is a 'Fund Inc' (FUND is a stop word); may be a separate support fund"),
    'ein_unlisted|231381432|PENAFORT RAYMOND SAINT|PA': ('wrong', 'different state (VA)'),
    'ein_unlisted|800514202|CONFERENCE JOSEPH SAINT|WY': ('wrong', 'different state (OH)'),
    'ein_unlisted|264700149|ARTS HORIZON|VA': ('wrong', 'different state (UT) and different name order'),
}


# ----------------------------------------------------------------------------- loaders (I/O edge)
def iter_reference(bmf_dir: str, pub78: str):
    """Yield (source, ein, name, state, extra) for every BMF and Pub 78 record."""
    for f in BMF_FILES:
        p = os.path.join(bmf_dir, f)
        if not os.path.exists(p):
            continue
        with open(p, encoding="latin-1", newline="") as fh:
            for r in csv.DictReader(fh):
                yield ("bmf", ein9(r["EIN"]), r["NAME"], (r["STATE"] or "").strip(),
                       {"subsection": (r["SUBSECTION"] or "").strip(), "city": (r["CITY"] or "").strip()})
    with open(pub78, encoding="latin-1", newline="") as fh:
        for raw in fh:
            p = raw.rstrip("\r\n").split("|")
            if len(p) >= 6:
                yield ("pub78", ein9(p[0]), p[1], p[3].strip(), {"codes": p[5].strip(), "city": p[2].strip()})


def doc_freq(bmf_dir: str, pub78: str, vocab: frozenset) -> dict:
    df = {}
    for _, _, name, _, _ in iter_reference(bmf_dir, pub78):
        for t in tokens(name) & vocab:
            df[t] = df.get(t, 0) + 1
    return df


def collect_candidates(bmf_dir: str, pub78: str, index: Mapping, target_toks: Mapping) -> dict:
    """index: block token -> target ids. Keeps, per target, only reference records whose Jaccard score against
    the target is >= J_MIN (lower scores can never reach a tier). Returns target id -> {ein: merged record}."""
    out = {}
    for src, e, name, st, extra in iter_reference(bmf_dir, pub78):
        tk = tokens(name)
        hit = frozenset(i for t in tk if t in index for i in index[t])
        for i in (i for i in hit if jaccard(tk, target_toks[i]) >= J_MIN):
            d = out.setdefault(i, {})
            cur = d.get(e) or {"ein": e, "names": {}, "state": st, "in_pub78": False, "bmf_sub": "", "city": "",
                               "codes": ""}
            cur["names"][src] = name.strip()
            cur["state"] = cur["state"] or st
            cur["city"] = cur["city"] or extra.get("city", "")
            if src == "pub78":
                cur["in_pub78"], cur["codes"] = True, extra["codes"]
            else:
                cur["bmf_sub"] = extra["subsection"]
            d[e] = cur
    return out


def finalise_ref(c: Mapping) -> dict:
    name = c["names"].get("pub78") or c["names"].get("bmf", "")
    # score against both names; keep the better-scoring token set at match time via 'alt'
    return {"ein": c["ein"], "name": name, "state": c["state"], "city": c["city"], "in_pub78": c["in_pub78"],
            "bmf_sub": c["bmf_sub"], "codes": c["codes"], "listed": c["in_pub78"] or c["bmf_sub"] == "03",
            "src": "+".join(sorted(c["names"])), "all_names": tuple(c["names"].values())}


def expand(refs: Iterable[Mapping]) -> tuple:
    """One scoring row per (EIN, name variant) so that Pub 78 and BMF spellings are both tried."""
    return tuple({**r, "toks": tokens(n)} for r in refs for n in r["all_names"])


# ----------------------------------------------------------------------------- aggregation (pure)
def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    if not n:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 4), round(c + h, 4))


def summarise(rows: Sequence[Mapping]) -> list:
    def cell(pool, res, rs):
        return {"row_type": "summary", "pool": pool, "resolution": res, "keys": len(rs),
                "lines": sum(r["lines"] for r in rs), "usd": round(sum(r["usd"] for r in rs)),
                "typo_like_keys": sum(1 for r in rs if r.get("ein_typo_like") == 1),
                "typo_like_usd": round(sum(r["usd"] for r in rs if r.get("ein_typo_like") == 1))}
    pools = ("ein_unlisted", "blank_ein")
    res = sorted({r["resolution"] for r in rows})
    out = [cell(p, x, [r for r in rows if r["pool"] == p and r["resolution"] == x]) for p in pools for x in res]
    out += [cell(p, "ALL", [r for r in rows if r["pool"] == p]) for p in pools]
    out += [cell(p, "matched_tier_" + t, [r for r in rows if r["pool"] == p and r["match_tier"] == t
                                          and r["resolution"] == "matched_listed_other_ein"])
            for p in pools for t in "ABC"]
    return [c for c in out if c["keys"]]


FIELDS = ("row_type", "pool", "key", "filed_ein", "filed_name", "name_withheld", "filed_state", "lines", "usd", "n_sponsors",
          "sponsors", "fiscal_years", "d2d_line", "resolution", "match_tier", "match_score", "match_n_best",
          "matched_ein", "matched_name", "matched_state", "matched_city", "matched_source", "matched_pub78_codes",
          "matched_bmf_subsection", "ein_digit_distance", "ein_typo_like", "filed_ein_revocation_name",
          "handcheck_sample", "handcheck_verdict", "handcheck_note", "keys", "typo_like_keys", "typo_like_usd",
          "source")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", nargs="?", default=".", help="repo root (unused; repo CLI convention)")
    ap.add_argument("--np-cache", required=True)
    ap.add_argument("--lines-cache", required=True)
    ap.add_argument("--bmf-dir", required=True)
    ap.add_argument("--pub78", required=True)
    ap.add_argument("--revocation", required=True)
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)

    dafrc = read_csv(DAFRC_CSV)
    panel = panel_from(dafrc)
    rank = top_n(dafrc, TOP_N)
    chosen = pick_returns(load_np(a.np_cache))
    item = {(e, fy): chosen[(e, fy)] for e in rank for fy in FYS if (e, fy) in chosen and itemized(chosen[(e, fy)])}
    loaded = {k: load_lines(x["oid"], x.get("sched_i_lines") or 0, a.lines_cache, [], False) for k, x in item.items()}
    good = {k: v for k, v in loaded.items() if v["status"] == "ok"}
    sy = {k: dict(zip(("start", "end"), period_of(item[k]["tax_period_end"]))) for k in good}

    wl = read_csv(WHITELIST)
    wl_eins = frozenset(ein9(r["recipient_ein"]) for r in wl if r["decision"] == "include")
    names = _group_by_fast((panel[e] for e in wl_eins if e in panel), lambda p: norm_name(p["name"]))
    wl_names = {k: v[0]["ein"] for k, v in names.items() if k and len(v) == 1}
    ann = {k: annotate(k[0], v["lines"], {}, wl_eins, wl_names) for k, v in good.items()}
    irc = {k: tuple(l[3] for l in v["lines"]) for k, v in good.items()}
    totals = {k: (sum(map(_amt, [x for x in v["lines"] if x[1].strip()])), sum(1 for x in v["lines"] if x[1].strip()))
              for k, v in good.items()}
    is_tot = {k: tuple(is_totals_row(l, *totals[k]) for l in v["lines"]) for k, v in good.items()}
    eins = frozenset(r["ein"] for rs in ann.values() for r in rs if r["ein"])
    bmf = load_bmf_ext(a.bmf_dir, eins)
    p78, _ = load_pub78(a.pub78, eins, frozenset())
    scr = {k: tuple(screen(r, irc[k][i], sy[k], bmf, p78, {}, {}) for i, r in enumerate(ann[k])) for k in ann}

    def pool_of(r):
        if not r["ein"]:
            return "blank_ein"
        if "absent_pub78_and_bmf" in r["flags"] and not (set(r["labels"]) & EXPLAINING):
            return "ein_unlisted"
        return ""
    flat = tuple({**r, "_k": k, "_tot": is_tot[k][i], "_pool": pool_of(r)}
                 for k, rs in scr.items() for i, r in enumerate(rs))
    brief = {p: {"lines": sum(1 for r in flat if r["_pool"] == p), "usd": round(sum(r["amount"] for r in flat if r["_pool"] == p))}
             for p in ("ein_unlisted", "blank_ein")}
    totals_rows = [r for r in flat if r["_tot"]]
    work = tuple(r for r in flat if r["_pool"] and not r["_tot"])

    keyf = lambda r: f"{r['_pool']}|{r['ein']}|{' '.join(sorted(tokens(r['name'])))}|{r['where']}"  # noqa: E731
    groups = _group_by_fast(work, keyf)
    targets = {kk: {"id": kk, "pool": v[0]["_pool"], "ein": v[0]["ein"], "name": v[0]["name"], "where": v[0]["where"],
                    "state": v[0]["where"] if v[0]["where"] and not v[0]["where"].startswith("F:") else "",
                    "toks": tokens(v[0]["name"]), "labels": frozenset(l for x in v for l in x["labels"]) & EXPLAINING,
                    "lines": v} for kk, v in groups.items()}
    vocab = frozenset(t for x in targets.values() for t in x["toks"])
    print(f"targets {len(targets)} vocab {len(vocab)}", file=sys.stderr)
    df = doc_freq(a.bmf_dir, a.pub78, vocab)
    index = {t: tuple(p[1] for p in v) for t, v in _group_by_fast(
        ((t, x["id"]) for x in targets.values() if x["toks"] for t in block_tokens(x["toks"], df)),
        lambda p: p[0]).items()}
    cands = collect_candidates(a.bmf_dir, a.pub78, index, {i: x["toks"] for i, x in targets.items()})
    revs = load_revocations(a.revocation, frozenset(x["ein"] for x in targets.values() if x["ein"]))

    def row(t):
        m = best_match(t, expand(map(finalise_ref, cands.get(t["id"], {}).values())))
        ref = m["ref"]
        rv = revs.get(t["ein"], ())
        res = resolve(t, m, bool(rv))
        d = ein_distance(t["ein"], ref["ein"]) if ref is not None and t["ein"] else ""
        ls = t["lines"]
        sp = sorted({panel[x["_k"][0]]["name"] for x in ls})
        return {"row_type": "recipient", "pool": t["pool"], "key": t["id"], "filed_ein": t["ein"],
                "filed_name": t["name"], "filed_state": t["where"], "lines": len(ls),
                "usd": round(sum(x["amount"] for x in ls), 2), "n_sponsors": len(sp), "sponsors": "; ".join(sp[:5]),
                "fiscal_years": ";".join(sorted({str(x["_k"][1]) for x in ls})),
                "d2d_line": int(any(x["d2d"] for x in ls)), "resolution": res,
                "match_tier": m["tier"] if ref is not None else "", "match_score": round(m["score"], 3),
                "match_n_best": m["n_best"], "matched_ein": (ref or {}).get("ein", ""),
                "matched_name": (ref or {}).get("name", ""), "matched_state": (ref or {}).get("state", ""),
                "matched_city": (ref or {}).get("city", ""), "matched_source": (ref or {}).get("src", ""),
                "matched_pub78_codes": (ref or {}).get("codes", ""),
                "matched_bmf_subsection": (ref or {}).get("bmf_sub", ""), "ein_digit_distance": d,
                "ein_typo_like": (1 if typo_like(d) else 0) if d else "",
                "filed_ein_revocation_name": rv[-1]["name"] if rv else "", "source": SOURCE}
    rows = sorted(map(withhold, map(row, targets.values())), key=lambda r: (r["pool"], -r["usd"], r["key"]))
    samp = draw_sample(rows, 20)
    rows = [{**r, "handcheck_sample": int(r["key"] in samp),
             "handcheck_verdict": HANDCHECK.get(r["key"], ("", ""))[0] if r["key"] in samp else "",
             "handcheck_note": HANDCHECK.get(r["key"], ("", ""))[1] if r["key"] in samp else ""} for r in rows]
    summ = summarise(rows)
    write_csv(a.out, summ + rows, FIELDS)

    sampled = [r for r in rows if r["handcheck_sample"]]
    judged = [r for r in sampled if r["handcheck_verdict"] in ("correct", "wrong")]
    k = sum(1 for r in judged if r["handcheck_verdict"] == "correct")
    m_rows = [r for r in rows if r["resolution"] == "matched_listed_other_ein"]
    summary = {
        "pools_as_briefed_incl_totals_rows": brief,
        "totals_rows_dropped": [{"sponsor": panel[r["_k"][0]]["name"], "fy": r["_k"][1], "usd": r["amount"]} for r in totals_rows],
        "pools_resolved": {p: {"keys": sum(1 for r in rows if r["pool"] == p),
                               "lines": sum(r["lines"] for r in rows if r["pool"] == p),
                               "usd": round(sum(r["usd"] for r in rows if r["pool"] == p))} for p in ("ein_unlisted", "blank_ein")},
        "by_resolution": [{x: c[x] for x in ("pool", "resolution", "keys", "lines", "usd", "typo_like_keys", "typo_like_usd")} for c in summ],
        "handcheck": {"sampled": len(sampled), "judged": len(judged), "correct": k,
                      "precision": round(k / len(judged), 4) if judged else None, "wilson95": wilson(k, len(judged)),
                      "unsure": sum(1 for r in sampled if r["handcheck_verdict"] == "unsure"),
                      "by_tier": {t: {v: sum(1 for r in sampled if r["match_tier"] == t and r["handcheck_verdict"] == v)
                                      for v in ("correct", "wrong", "unsure")} for t in "ABC"},
                      "by_pool": {p: {v: sum(1 for r in sampled if r["pool"] == p and r["handcheck_verdict"] == v)
                                      for v in ("correct", "wrong", "unsure")} for p in ("ein_unlisted", "blank_ein")}},
        "sample": [{x: r[x] for x in ("key", "pool", "filed_name", "filed_state", "filed_ein", "usd", "match_tier",
                                      "match_score", "matched_name", "matched_state", "matched_city", "matched_ein",
                                      "ein_digit_distance", "handcheck_verdict")} for r in sampled],
        "top_matched": [{x: r[x] for x in ("pool", "filed_name", "filed_ein", "filed_state", "usd", "sponsors",
                                           "match_tier", "matched_name", "matched_ein", "matched_state",
                                           "ein_digit_distance")} for r in sorted(m_rows, key=lambda r: -r["usd"])[:25]],
        "top_unmatched_other": [{x: r[x] for x in ("pool", "filed_name", "filed_ein", "filed_state", "usd", "sponsors",
                                                   "match_score")}
                                for r in sorted((r for r in rows if r["resolution"] == "unmatched_other"
                                                 and not r["name_withheld"]),
                                                key=lambda r: -r["usd"])[:25]],
        "top_ambiguous": [{x: r[x] for x in ("pool", "filed_name", "filed_state", "usd", "match_tier", "match_n_best",
                                             "matched_name")}
                          for r in sorted((r for r in rows if r["resolution"] == "ambiguous"), key=lambda r: -r["usd"])[:10]],
    }
    print(json.dumps(summary, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
