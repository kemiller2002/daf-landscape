#!/usr/bin/env python3
"""Private-foundation-to-DAF-sponsor flows, 990-PF tax years 2022-2024 (TASKID b49-01).

Question: how much money moves from private foundations (990-PF filers) into DAF sponsors, and how much of it comes
from foundations that are winding down (final returns / terminations) into DAF sponsors?

Stdlib only; functional style (pure transforms, I/O at the edges). Three stages:

  frame    IRS TEOS e-file index files (index_2023.csv .. index_2026.csv) -> one row per (EIN, TAX_PERIOD) for
           RETURN_TYPE 990PF with tax year 2022-2024; latest OBJECT_ID per (EIN, TAX_PERIOD) so an amended return
           supersedes the original. Tax year (the 990-PF TaxYr convention = year the period begins) is derived
           from TAX_PERIOD: month 12 -> same year, otherwise the year before. Census, not a sample.
  harvest  every frame return's XML is read from the GivingTuesday 990 data lake mirror of IRS TEOS
           (https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml), parsed in
           memory and discarded (nothing is stored but the extract). Per return: header flags (FinalReturnInd,
           InitialReturnInd, AmendedReturnInd, any element whose name contains '507', OrganizationDissolvedEtcInd),
           FMV of assets, Part I line 25 contributions paid, Part XV line 3a total, count and sum of itemised
           GrantOrContributionPdDurYrGrp lines. Per grant line: only *candidate* lines are kept (recipient name or
           purpose looks DAF-like, contains a 9-digit EIN, or the name's normalised first segment equals a DAF
           sponsor name key) so the cache stays small. Chunked and resumable (one gz file per chunk).
  build    candidate lines are matched to the DAF sponsor universe (DAFRC 2025 panel, 1,594 EINs, which contains
           the repo's top-50) in this order: EIN written in the line's text; exact normalised name (DAFRC or BMF
           name, unique in the panel; state must agree when both are known); exact normalised first segment of the
           name (text before ' - ', ' FBO ', '(', ',', '/', ' C/O ', ' FOR '); brand alias regex for national
           sponsors (ALIASES below). The 990-PF Part XV schema has no recipient-EIN field, so EIN matching only
           applies when a filer typed the EIN into a text field.

Outputs (build):
  data/mission-2026-11-14/pf-to-daf-flows-2026-11-20.csv   one row per (PF return, matched sponsor)
  <cache>/pf_to_daf_summary.json                           all aggregates quoted in the research note

Usage:
  python3 scripts/mission_pf_to_daf_flows.py . frame   --irs-dir DIR --cache CACHE
  python3 scripts/mission_pf_to_daf_flows.py . harvest --cache CACHE [--procs 40] [--limit N]
  python3 scripts/mission_pf_to_daf_flows.py . build   --cache CACHE --bmf-dir DIR
"""
from __future__ import annotations

import argparse
import csv
import glob
import gzip
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from multiprocessing import Pool
from typing import Iterable, Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mission_990_contractors import DAFRC_CSV, _group_by_fast, ein9, num, read_csv, write_csv  # noqa: E402
from mission_net_payout import norm_name, panel_from, segment_of  # noqa: E402

XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
UA = "research-script/1.0"
INDEX_YEARS = (2023, 2024, 2025, 2026)
TAX_YEARS = (2022, 2023, 2024)
CHUNK = 2000
OUT_NAME = "pf-to-daf-flows-2026-11-20.csv"
LEAGUE_CSV = "daf-sponsor-league-table-fy2021-2025.csv"
MARKET_CSV = "dafrc-corrected-market-totals.csv"
SOURCE = ("IRS Form 990-PF Part XV line 3a (GrantOrContributionPdDurYrGrp), e-file XML via GivingTuesday mirror of "
          "IRS TEOS; frame = IRS TEOS index 2023-2026; sponsors = DAFRC 2025 panel")

# DAF-primary tiers (same segment logic as mission_daf_to_daf.py / mission_net_payout.py)
DAF_PRIMARY = frozenset({"national", "processor", "community_foundation"})


# ----------------------------------------------------------------------------- frame (pure + edge)
def tax_year_of(period: str) -> int:
    y, m = int(period[:4]), int(period[4:6])
    return y if m == 12 else y - 1


def index_rows(path: str) -> Iterable[dict]:
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        yield from (r for r in csv.DictReader(fh) if (r.get("RETURN_TYPE") or "").strip() == "990PF")


def build_frame(rows: Iterable[Mapping]) -> tuple[dict, ...]:
    keep = (r for r in rows if len(r.get("TAX_PERIOD") or "") == 6 and tax_year_of(r["TAX_PERIOD"]) in TAX_YEARS)
    latest = _latest(keep)
    return tuple({"object_id": r["OBJECT_ID"], "ein": ein9(r["EIN"]), "tax_period": r["TAX_PERIOD"],
                  "tax_year": tax_year_of(r["TAX_PERIOD"]), "name": (r.get("TAXPAYER_NAME") or "").strip(),
                  "sub_date": r.get("SUB_DATE", ""), "index_year": r.get("_index_year", "")}
                 for _, r in sorted(latest.items()))


def _latest(rows: Iterable[Mapping]) -> dict:
    # single pass; local accumulator only (a reduce over 375k dict copies would be quadratic)
    acc: dict = {}
    for r in rows:
        k = (ein9(r["EIN"]), r["TAX_PERIOD"])
        if k not in acc or r["OBJECT_ID"] > acc[k]["OBJECT_ID"]:
            acc[k] = r
    return acc


# ----------------------------------------------------------------------------- name keys (pure)
ABBR = {"FDN": "FOUNDATION", "FNDN": "FOUNDATION", "FOUND": "FOUNDATION", "FOUNDATIO": "FOUNDATION",
        "CMNTY": "COMMUNITY", "COMM": "COMMUNITY", "CMTY": "COMMUNITY", "NATL": "NATIONAL", "GRTR": "GREATER",
        "CHAR": "CHARITABLE", "CHARITABL": "CHARITABLE", "ASSN": "ASSOCIATION", "FD": "FUND", "SAN": "SAN"}


def key(s: str) -> str:
    return " ".join(ABBR.get(t, t) for t in norm_name(html.unescape(s or "")).split())


SPLIT_RX = re.compile(r"\s+-+\s+|\s+F/?B/?O\b|\bC/O\b|\(|,|/|;|:|\s+FOR THE BENEFIT\b|\s+DONOR ADVISED\b|\s+DAF\b|"
                      r"\s+FOR\s+(?:THE\s+)?[A-Z]+\s+(?:FAMILY|FUND)\b", re.I)


def first_segment(s: str) -> str:
    return SPLIT_RX.split(html.unescape(s or ""), maxsplit=1)[0]


EIN_RX = re.compile(r"(?<!\d)(\d{2})-?(\d{7})(?!\d)")
CAND_RX = re.compile(r"DONOR[\s-]*ADVISED|\bDAF\b|ADVISED FUND|CHARITABLE GIFT|GIFT FUND|GIVING FUND|COMMUNITY FOUND|"
                     r"COMMUNITY TRUST|PHILANTHROP|CHARITABLE FUND|CHARITABLE TRUST|ENDOWMENT|COMMUNAL|FIDELITY|"
                     r"SCHWAB|VANGUARD|GOLDMAN|MORGAN STANLEY|RENAISSANCE|IMPACT ?ASSETS|DONORS|DAFFY|CHARITYVEST|"
                     r"SIGNATRY|SERVANT|NATIONAL CHRISTIAN|AYCO|BESSEMER|HORIZONS|DECHOMAI|RAYMOND JAMES|ROWE PRICE|"
                     r"THRIVENT|ONLINE GIVING|PAYPAL|BLACKBAUD|NETWORK FOR GOOD|GIVINGA|STIFEL|DAFGIVING|\bNPT\b|"
                     r"\bNCF\b|FOUNDATION FOR THE|COMMUNITY FDN|CMNTY", re.I)

# Brand aliases for national/processor sponsors, applied only after EIN and exact-name matching failed.
ALIASES = (
    (r"\bFIDELITY\s+(INVESTMENTS?\s+)?(CHARITABLE|GIFT\s+FUND)", "110303001"),
    (r"NATIONAL\s+PHILANTHROPIC\s+TRUST|^NPT\b", "237825575"),
    (r"SCHWAB\s+CHARITABLE|DAF\s*GIVING\s*360|DONOR\s+ADVISED\s+CHARITABLE\s+GIVING", "311640316"),
    (r"VANGUARD\s+CHARITABLE", "232888152"),
    (r"GOLDMAN\s+SACHS\s+PHILANTHROPY\s+FUND|GS\s+DONOR\s+ADVISED|GOLDMAN\s+SACHS\s+DONOR\s+ADVISED", "311774905"),
    (r"GOLDMAN\s+SACHS\s+CHARITABLE\s+GIFT", "113813663"),
    (r"MORGAN\s+STANLEY\s+(GLOBAL\s+IMPACT|GIFT\b|CHARITABLE\s+GIFT)", "527082731"),
    (r"AMERICAN\s+ENDOWMENT\s+FOUNDATION", "341747398"),
    (r"RENAISSANCE\s+CHARITABLE", "352129262"),
    (r"^(THE\s+)?NATIONAL\s+CHRISTIAN\s+(CHARITABLE\s+)?FOUNDATION(\s+INC\.?)?$|^NCF(\s+GIVING)?(\s+INC\.?)?$", "581493949"),
    (r"BANK\s+OF\s+AMERICA\s+CHARITABLE\s+GIFT|BOFA\s+CHARITABLE\s+GIFT", "046010342"),
    (r"IMPACT\s*ASSETS", "262048480"),
    (r"JEWISH\s+COMMUNAL\s+FUND", "237174183"),
    (r"RAYMOND\s+JAMES\s+CHARITABLE", "593652538"),
    (r"DECHOMAI", "260724604"),
    (r"^(THE\s+)?DONORS\s*TRUST", "522166327"),
    (r"DONORS\s+CAPITAL\s+FUND", "541934032"),
    (r"U\.?\s*S\.?\s+CHARITABLE\s+GIFT\s+TRUST", "311663020"),
    (r"AYCO\s+CHARITABLE", "141782466"),
    (r"SERVANT\s+FOUNDATION", "431890105"),
    (r"SIGNATRY", "825070897"),
    (r"BESSEMER\s+GIVING", "137111099"),
    (r"GREATER\s+HORIZONS", "200849590"),
    (r"AMERICAN\s+GIFT\s+FUND", "516506426"),
    (r"T\.?\s*ROWE\s+PRICE\s+(PROGRAM|CHARITABLE)", "311709466"),
    (r"THRIVENT\s+CHARITABLE", "411802412"),
    (r"DAFFY", "863177440"),
    (r"CHARITYVEST", "812771871"),
    (r"AMERICAN\s+ONLINE\s+GIVING", "810739440"),
    (r"PAYPAL\s+(CHARITABLE\s+)?GIVING\s+FUND", "450931286"),
    (r"BLACKBAUD\s+GIVING\s+FUND", "460942102"),
    (r"NETWORK\s+FOR\s+GOOD", "680480736"),
    (r"GIVINGA", "474172718"),
    (r"BNY\s+MELLON\s+CHARITABLE\s+GIFT", "300748315"),
    (r"STIFEL\s+CHARITABLE", "842049692"),
    (r"^(THE\s+)?DONORS\s+FUND", "474844275"),
    (r"SILICON\s+VALLEY\s+COMMUNITY\s+FOUNDATION", "205205488"),
    (r"NEW\s+YORK\s+COMMUNITY\s+TRUST", "133062214"),
    (r"CHICAGO\s+COMMUNITY\s+TRUST", "362167000"),
)
ALIAS_RX = tuple((re.compile(p, re.I), e) for p, e in ALIASES)
DAF_PURPOSE_RX = re.compile(r"DONOR[\s-]*ADVISED|\bDAF\b|ADVISED\s+FUND|\bD\.A\.F\b", re.I)


def panel_keys(panel: Mapping, bmf: Mapping) -> dict[str, tuple]:
    """normalised name -> tuple of panel EINs carrying that name (DAFRC names, all years, plus BMF NAME)."""
    pairs = tuple((key(n), e) for e, p in panel.items()
                  for n in {p["name"], *(r["name"] for r in p["fy"].values()), bmf.get(e, {}).get("NAME", "")} if n)
    by = _group_by_fast((pr for pr in pairs if len(pr[0]) >= 6), lambda pr: pr[0])
    return {k: tuple(sorted({e for _, e in v})) for k, v in by.items()}


def dedup_name(s: str) -> str:
    """'X INC X INC' (BusinessNameLine1 repeated in Line2) -> 'X INC'; trailing one-letter token dropped."""
    t = key(s).split()
    t = t[: len(t) // 2] if len(t) % 2 == 0 and t and t[: len(t) // 2] == t[len(t) // 2:] else t
    return " ".join(t[:-1] if len(t) > 2 and len(t[-1]) == 1 else t)


# ----------------------------------------------------------------------------- XML extract (pure on text)
def _tag(t: str, name: str) -> str | None:
    m = re.search(r"<(?:\w+:)?%s\b[^>]*>([^<]*)<" % name, t)
    return html.unescape(m.group(1).strip()) if m else None


def _tags(t: str, rx: str) -> dict:
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"<(?:\w+:)?(%s)\b[^>]*>([^<]*)<" % rx, t)}


GRANT_RX = re.compile(r"<(?:\w+:)?GrantOrContributionPdDurYrGrp\b[^>]*>(.*?)</(?:\w+:)?GrantOrContributionPdDurYrGrp>", re.S)


def grant_line(b: str) -> dict:
    nm = " ".join(x for x in (_tag(b, "BusinessNameLine1Txt"), _tag(b, "BusinessNameLine2Txt")) if x) \
        or _tag(b, "RecipientPersonNm") or ""
    return {"name": nm, "person": int(_tag(b, "RecipientPersonNm") is not None and not _tag(b, "BusinessNameLine1Txt")),
            "city": _tag(b, "CityNm") or _tag(b, "CityTxt") or "", "state": _tag(b, "StateAbbreviationCd") or "",
            "country": _tag(b, "CountryCd") or "", "rel": (_tag(b, "RecipientRelationshipTxt") or "")[:60],
            "status": (_tag(b, "RecipientFoundationStatusTxt") or "")[:40],
            "purpose": (_tag(b, "GrantOrContributionPurposeTxt") or "")[:160],
            "ein_field": _tag(b, "RecipientEIN") or "", "amt": num(_tag(b, "Amt")) or 0.0}


def is_candidate(g: Mapping, keys: Mapping) -> bool:
    if g["person"]:
        return False
    text = " ".join((g["name"], g["purpose"], g["status"]))
    return bool(g["ein_field"] or CAND_RX.search(text) or EIN_RX.search(text)
                or key(g["name"]) in keys or key(first_segment(g["name"])) in keys or dedup_name(g["name"]) in keys)


def extract(text: str, keys: Mapping) -> tuple[dict, tuple]:
    head = text[: text.find("</ReturnHeader>") + 1 or 20000]
    grants = tuple(grant_line(b) for b in GRANT_RX.findall(text))
    flags = _tags(text, r"\w*507\w*|FinalReturnInd|InitialReturnInd|AmendedReturnInd|OrganizationDissolvedEtcInd|"
                        r"InitialReturnFormerPubChrtyInd")
    summ = {"tax_yr": _tag(head, "TaxYr"), "period_end": _tag(head, "TaxPeriodEndDt"),
            "rtype": _tag(head, "ReturnTypeCd"), "filer_ein": _tag(head, "EIN"),
            "filer_name": _tag(head, "BusinessNameLine1Txt"), "flags": flags,
            "fmv_eoy": num(_tag(text, "FMVAssetsEOYAmt")), "assets_boy": num(_tag(text, "TotalAssetsBOYAmt")),
            "assets_eoy": num(_tag(text, "TotalAssetsEOYAmt")),
            "contrib_paid_l25": num(_tag(text, "ContriPaidRevAndExpnssAmt")),
            "xv_total_3a": num(_tag(text, "TotalGrantOrContriPdDurYrAmt")),
            "n_lines": len(grants), "sum_lines": sum(g["amt"] for g in grants),
            "n_person_lines": sum(g["person"] for g in grants)}
    return summ, tuple(g for g in grants if is_candidate(g, keys))


# ----------------------------------------------------------------------------- harvest (edge)
_KEYS: dict = {}


def _init(keys: Mapping) -> None:
    _KEYS.update(keys)


def fetch(oid: str) -> tuple[str, str | None]:
    req = urllib.request.Request(XML_URL.format(oid=oid), headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return "ok", r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                return f"http_{e.code}", None
            time.sleep(1 + 2 * i)
        except Exception:  # noqa: BLE001  (network errors -> retry)
            time.sleep(1 + 2 * i)
    return "error", None


def work(row: Mapping) -> dict:
    status, text = fetch(row["object_id"])
    if text is None:
        return {**row, "xml_status": status}
    try:
        summ, lines = extract(text, _KEYS)
    except Exception as e:  # noqa: BLE001
        return {**row, "xml_status": f"parse_error:{type(e).__name__}"}
    return {**row, "xml_status": "ok", **summ, "lines": lines}


def harvest(frame: Sequence[Mapping], cache: str, keys: Mapping, procs: int) -> None:
    out = os.path.join(cache, "harvest")
    os.makedirs(out, exist_ok=True)
    done = frozenset(r["object_id"] for r in load_harvest(cache))
    rest = tuple(r for r in frame if r["object_id"] not in done)
    start = len(glob.glob(os.path.join(out, "c*.jsonl.gz")))
    chunks = {start + j: rest[j * CHUNK:(j + 1) * CHUNK] for j in range((len(rest) + CHUNK - 1) // CHUNK)}
    print(f"done {len(done)} todo {len(rest)} new chunks {len(chunks)}", flush=True)
    with Pool(procs, initializer=_init, initargs=(keys,)) as pool:
        for i in sorted(chunks):
            t0 = time.time()
            res = pool.map(work, chunks[i], chunksize=4)
            tmp = os.path.join(out, f"c{i:04d}.tmp")
            with gzip.open(tmp, "wt", encoding="utf-8") as fh:
                fh.writelines(json.dumps(r, separators=(",", ":")) + "\n" for r in res)
            os.replace(tmp, os.path.join(out, f"c{i:04d}.jsonl.gz"))
            print(f"chunk {i} ok={sum(r['xml_status'] == 'ok' for r in res)}/{len(res)} {time.time() - t0:.0f}s", flush=True)


def load_harvest(cache: str) -> tuple[dict, ...]:
    def one(p):
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            return tuple(json.loads(l) for l in fh)
    return tuple(r for p in sorted(glob.glob(os.path.join(cache, "harvest", "c*.jsonl.gz"))) for r in one(p))


def latest_per_period(h: Sequence[Mapping]) -> tuple[dict, ...]:
    """after 'extend', an (EIN, TAX_PERIOD) can appear twice; keep the latest object id (amended supersedes)."""
    by = _group_by_fast(h, lambda r: (r["ein"], r["tax_period"]))
    return tuple(max(v, key=lambda r: r["object_id"]) for _, v in sorted(by.items()))


# ----------------------------------------------------------------------------- matching (pure)
def match_line(g: Mapping, keys: Mapping, panel: Mapping, bmf: Mapping) -> tuple[str, str]:
    text = " ".join((g["name"], g["purpose"], g["status"], g.get("ein_field", "")))
    eins = tuple(ein9(a + b) for a, b in EIN_RX.findall(text))
    hit = next((e for e in eins if e in panel), None)
    if hit:
        return hit, "ein_in_text"
    foreign = bool(g["country"]) and g["country"] != "US"
    st = lambda e: bmf.get(e, {}).get("STATE", "")  # noqa: E731

    def resolve(es, k):
        """one EIN: accept unless both states are known and differ; several EINs: keep the one in the line's state,
        then the one whose current BMF legal name carries the key."""
        if len(es) == 1:
            return es[0] if not g["state"] or not st(es[0]) or st(es[0]) == g["state"] else ""
        same = tuple(e for e in es if g["state"] and st(e) == g["state"])
        legal = tuple(e for e in same if key(bmf.get(e, {}).get("NAME", "")) == k)
        return same[0] if len(same) == 1 else (legal[0] if len(legal) == 1 else "")
    for k, how in ((key(g["name"]), "name_exact"), (dedup_name(g["name"]), "name_exact"),
                   (key(first_segment(g["name"])), "name_first_segment")):
        e = resolve(keys.get(k, ()), k) if not foreign else ""
        if e:
            return e, how
    nm = re.sub(r"\s+", " ", html.unescape(g["name"]).upper()).strip()
    hit = next((e for rx, e in ALIAS_RX if rx.search(nm) and e in panel), None)
    return (hit, "alias") if hit and not foreign else ("", "")


# Top-50 single-issue sponsors whose activity is overwhelmingly DAF administration (judgment, listed so it can be
# challenged): National Christian Foundation, Jewish Communal Fund, DonorsTrust, Thrivent Charitable Impact & Investing.
CORE_SINGLE_ISSUE = frozenset({"581493949", "237174183", "522166327", "411802412"})
TIERS = {"T1": ("T1_core_top50",), "T12": ("T1_core_top50", "T2_national_other"),
         "T123": ("T1_core_top50", "T2_national_other", "T3_community"),
         "ALL": ("T1_core_top50", "T2_national_other", "T3_community", "T4_single_issue")}


def tier_of(ein: str, seg: str, rank: Mapping) -> str:
    """T1 core: FY2024 top-50 national/processor sponsors plus CORE_SINGLE_ISSUE; T2: other national sponsors and
    processors (includes fiscal sponsors such as Rockefeller Philanthropy Advisors); T3: community foundations;
    T4: other single-issue sponsors (universities, hospitals, federations, religious and other charities)."""
    if (ein in rank and seg in ("national", "processor")) or ein in CORE_SINGLE_ISSUE:
        return "T1_core_top50"
    return {"national": "T2_national_other", "processor": "T2_national_other",
            "community_foundation": "T3_community"}.get(seg, "T4_single_issue")


def matched_rows(h: Sequence[Mapping], keys: Mapping, panel: Mapping, bmf: Mapping, rank: Mapping) -> tuple[dict, ...]:
    def per_return(r):
        hits = tuple((g, *match_line(g, keys, panel, bmf)) for g in r.get("lines", ()))
        hits = tuple(x for x in hits if x[1] and x[1] != r["ein"])
        by = _group_by_fast(hits, lambda x: x[1])
        return tuple(row(r, e, xs) for e, xs in by.items())

    def row(r, e, xs):
        p = panel[e]
        seg = segment_of(p["type"], p["subtype"])
        amt = sum(g["amt"] for g, _, _ in xs)
        daf_amt = sum(g["amt"] for g, _, _ in xs if DAF_PURPOSE_RX.search(g["purpose"] + " " + g["name"]))
        return {"pf_ein": r["ein"], "pf_name": r.get("filer_name") or r["name"], "tax_year": r["tax_year"],
                "tax_period": r["tax_period"], "return_object_id": r["object_id"],
                "pf_final_return": int(is_final(r)), "pf_507b1a": int(f507a(r)), "pf_507b1b_60month": int(f507b(r)),
                "pf_dissolved_ind": int(dissolved(r)), "pf_terminating": int(terminating(r)),
                "pf_fmv_assets_eoy": r.get("fmv_eoy"), "pf_book_assets_boy": r.get("assets_boy"),
                "pf_total_grants_paid": grants_paid(r),
                "sponsor_ein": e, "sponsor_name": p["name"], "sponsor_type": p["type"], "sponsor_subtype": p["subtype"],
                "sponsor_segment": seg, "sponsor_tier": tier_of(e, seg, rank), "sponsor_rank_fy2024": rank.get(e, ""),
                "match_method": ";".join(sorted({m for _, _, m in xs})), "lines": len(xs), "amount_usd": amt,
                "daf_purpose_amount_usd": daf_amt, "largest_line_usd": max(g["amt"] for g, _, _ in xs),
                "recipient_name_filed": xs[0][0]["name"][:80],
                "purpose_text": " | ".join(sorted({g["purpose"][:60] for g, _, _ in xs}))[:200],
                "share_of_pf_grants_paid": amt / grants_paid(r) if grants_paid(r) else None,
                "xml_url": XML_URL.format(oid=r["object_id"]), "source": SOURCE}
    return tuple(x for r in h if r.get("xml_status") == "ok" for x in per_return(r))


# ----------------------------------------------------------------------------- flags (pure)
def _x(v) -> bool:
    return str(v or "").strip().upper() in ("X", "1", "TRUE", "YES")


def is_final(r) -> bool:
    return _x(r.get("flags", {}).get("FinalReturnInd"))


def f507a(r) -> bool:
    return any(_x(v) for k, v in r.get("flags", {}).items() if "507b1A" in k or "507b1a" in k)


def f507b(r) -> bool:
    return any(_x(v) for k, v in r.get("flags", {}).items() if "507b1B" in k or "507b1b" in k)


def dissolved(r) -> bool:
    return _x(r.get("flags", {}).get("OrganizationDissolvedEtcInd"))


def terminating(r) -> bool:
    """Winding down: final return (Heading item G) or section 507(b)(1)(A) termination (item E, all net assets
    distributed to public charities). Item F (60-month 507(b)(1)(B)) is a conversion to public-charity status, not a
    wind-down, and is counted separately."""
    return is_final(r) or f507a(r)


def grants_paid(r) -> float:
    """Best available total of grants paid: Part XV 3a, else Part I line 25, else sum of itemised lines."""
    return next((v for v in (r.get("xv_total_3a"), r.get("contrib_paid_l25"), r.get("sum_lines")) if v), 0.0) or 0.0


# ----------------------------------------------------------------------------- aggregation (pure)
def _r(x):
    return round(x) if isinstance(x, (int, float)) else x


UNMATCHED_RX = re.compile(r"DONOR[\s-]*ADVISED|\bDAF\b|ADVISED\s+FUND|CHARITABLE\s+GIFT|GIVING\s+FUND|GIFT\s+FUND|"
                          r"CHARITABLE\s+FUND|PHILANTHROPIC|COMMUNITY\s+FOUNDATION|COMMUNITY\s+TRUST", re.I)


def unmatched_review(h: Sequence[Mapping], keys: Mapping, panel: Mapping, bmf: Mapping, n: int = 60) -> list:
    """Recall check: DAF-looking candidate lines that matched no panel sponsor, grouped by normalised first segment."""
    ls = tuple(g for r in h if r.get("xml_status") == "ok" for g in r.get("lines", ())
               if not match_line(g, keys, panel, bmf)[0] and UNMATCHED_RX.search(g["name"] + " " + g["purpose"]))
    by = _group_by_fast(ls, lambda g: key(first_segment(g["name"])))
    return sorted(({"name_key": k, "usd": _r(sum(g["amt"] for g in v)), "lines": len(v), "example": v[0]["name"][:70],
                    "state": v[0]["state"]} for k, v in by.items()), key=lambda d: -d["usd"])[:n]


def summarise(h: Sequence[Mapping], rows: Sequence[Mapping], panel: Mapping, league: Sequence[Mapping],
              market: Sequence[Mapping]) -> dict:
    ok = tuple(r for r in h if r.get("xml_status") == "ok")
    tiers = TIERS

    def year_block(ty):
        rs = tuple(r for r in ok if r["tax_year"] == ty)
        mr = tuple(m for m in rows if m["tax_year"] == ty)
        term = tuple(r for r in rs if terminating(r))
        term_e = frozenset(r["object_id"] for r in term)

        def t(sel, pred=lambda m: True):
            ms = tuple(m for m in mr if m["sponsor_tier"] in sel and pred(m))
            return {"usd": _r(sum(m["amount_usd"] for m in ms)), "pf_returns": len({m["return_object_id"] for m in ms}),
                    "pfs": len({m["pf_ein"] for m in ms}), "lines": sum(m["lines"] for m in ms),
                    "daf_purpose_usd": _r(sum(m["daf_purpose_amount_usd"] for m in ms))}
        return {"frame_returns": sum(1 for r in h if r["tax_year"] == ty), "parsed_returns": len(rs),
                "pf_grants_paid_total": _r(sum(grants_paid(r) for r in rs)),
                "pf_itemised_lines_total": _r(sum(r["sum_lines"] for r in rs)),
                "pf_fmv_assets_eoy_total": _r(sum(r.get("fmv_eoy") or 0 for r in rs)),
                "by_tier": {k: t(v) for k, v in tiers.items()},
                "by_tier_alias_or_ein_only": {k: t(v, lambda m: "name" not in m["match_method"]) for k, v in tiers.items()},
                "terminating_returns": len(term), "final_returns": sum(is_final(r) for r in rs),
                "f507b1a": sum(f507a(r) for r in rs), "f507b1b": sum(f507b(r) for r in rs),
                "dissolved_ind": sum(dissolved(r) for r in rs),
                "terminating_grants_paid": _r(sum(grants_paid(r) for r in term)),
                "terminating_fmv_boy_assets": _r(sum(r.get("assets_boy") or 0 for r in term)),
                "terminating_to_sponsor": {k: t(v, lambda m: m["return_object_id"] in term_e) for k, v in tiers.items()},
                "terminating_with_sponsor_grant": {k: len({m["return_object_id"] for m in mr if m["sponsor_tier"] in v and m["return_object_id"] in term_e})
                                                   for k, v in tiers.items()},
                "returns_with_grants_but_no_itemised_lines": sum(1 for r in rs if grants_paid(r) > 0 and not r["n_lines"]),
                "grants_paid_on_returns_without_itemised_lines": _r(sum(grants_paid(r) for r in rs if not r["n_lines"])),
                "conversion_signatures": {k: conv(mr, v, term_e) for k, v in tiers.items()},
                "status_counts": {s: sum(1 for r in h if r["tax_year"] == ty and r["xml_status"] == s)
                                  for s in sorted({r["xml_status"] for r in h})}}

    def conv(mr, sel, term_e):
        """Per PF return: sponsor receipts in the tier vs grants paid and vs beginning-of-year book assets."""
        by = _group_by_fast((m for m in mr if m["sponsor_tier"] in sel), lambda m: m["return_object_id"])
        per = tuple({"usd": sum(m["amount_usd"] for m in v), "paid": v[0]["pf_total_grants_paid"] or 0,
                     "boy": v[0]["pf_book_assets_boy"] or 0, "term": k in term_e} for k, v in by.items())
        maj = tuple(x for x in per if x["paid"] and x["usd"] >= 0.5 * x["paid"])
        big = tuple(x for x in per if x["boy"] >= 100000 and x["usd"] >= 0.5 * x["boy"])
        return {"returns_sponsor_ge50pct_of_grants": len(maj), "usd_sponsor_ge50pct_of_grants": _r(sum(x["usd"] for x in maj)),
                "of_which_terminating": sum(x["term"] for x in maj),
                "returns_sponsor_ge50pct_of_boy_assets": len(big), "usd_sponsor_ge50pct_of_boy_assets": _r(sum(x["usd"] for x in big)),
                "of_which_terminating_boy": sum(x["term"] for x in big),
                "usd_terminating_boy": _r(sum(x["usd"] for x in big if x["term"]))}

    def conc(ty, sel):
        mr = tuple(m for m in rows if m["sponsor_tier"] in sel and (ty is None or m["tax_year"] == ty))
        by = _group_by_fast(mr, lambda m: m["pf_ein"])
        tots = sorted(((sum(m["amount_usd"] for m in v), k, v[0]["pf_name"], max(x["pf_terminating"] for x in v)) for k, v in by.items()), reverse=True)
        total = sum(x[0] for x in tots) or 1
        cum = lambda n: sum(x[0] for x in tots[:n]) / total  # noqa: E731
        return {"pfs": len(tots), "total_usd": _r(total), "top1_share": cum(1), "top10_share": cum(10), "top50_share": cum(50),
                "top100_share": cum(100), "top_pfs": [{"pf_ein": k, "pf_name": n, "usd": _r(v), "terminating_any_year": tm}
                                                     for v, k, n, tm in tots[:20]]}

    def sponsor_shares():
        lg = {(r["ein"], int(r["fiscal_year"])): r for r in league if r["row_type"] == "top50"}
        def one(e, rk):
            p = panel[e]
            out = {"sponsor_ein": e, "sponsor_name": p["name"], "rank_fy2024": rk, "segment": segment_of(p["type"], p["subtype"])}
            for ty in TAX_YEARS:
                pf = sum(m["amount_usd"] for m in rows if m["sponsor_ein"] == e and m["tax_year"] == ty)
                c = num((lg.get((e, ty)) or {}).get("daf_contributions")) or num((p["fy"].get(ty) or {}).get("total_daf_contributions"))
                out[f"pf_usd_ty{ty}"] = _r(pf)
                out[f"daf_contrib_fy{ty}"] = _r(c)
                out[f"share_{ty}"] = pf / c if c else None
            return out
        rank = {r["ein"]: int(r["rank_assets"]) for r in league if r["fiscal_year"] == "2024" and r["row_type"] == "top50"}
        return [one(e, rk) for e, rk in sorted(rank.items(), key=lambda x: x[1])]

    mk = {int(r["fiscal_year"]): num(r["corrected_value"]) for r in market if r["metric"] == "daf_contributions"}
    yb = {ty: year_block(ty) for ty in TAX_YEARS}
    return {"by_year": yb,
            "market_daf_contributions_corrected": {ty: _r(mk.get(ty)) for ty in TAX_YEARS},
            "share_of_market_contributions": {ty: {k: (yb[ty]["by_tier"][k]["usd"] / mk[ty]) if mk.get(ty) else None for k in TIERS}
                                              for ty in TAX_YEARS},
            "concentration_T1_all_years": conc(None, TIERS["T1"]),
            "concentration_T123_all_years": conc(None, TIERS["T123"]),
            "concentration_T1_by_year": {ty: {k: v for k, v in conc(ty, TIERS["T1"]).items() if k != "top_pfs"} for ty in TAX_YEARS},
            "concentration_T123_by_year": {ty: {k: v for k, v in conc(ty, TIERS["T123"]).items() if k != "top_pfs"} for ty in TAX_YEARS},
            "sponsor_shares_top50": sponsor_shares(),
            "match_methods": {m: sum(1 for r in rows if r["match_method"] == m) for m in sorted({r["match_method"] for r in rows})},
            "by_sponsor_all_years": sorted(({"sponsor_ein": e, "sponsor_name": v[0]["sponsor_name"], "tier": v[0]["sponsor_tier"],
                                             "usd": _r(sum(m["amount_usd"] for m in v)), "pf_returns": len(v)}
                                            for e, v in _group_by_fast(rows, lambda m: m["sponsor_ein"]).items()),
                                           key=lambda d: -d["usd"])[:40]}


FIELDS = ("pf_ein", "pf_name", "tax_year", "tax_period", "return_object_id", "pf_final_return", "pf_507b1a",
          "pf_507b1b_60month", "pf_dissolved_ind", "pf_terminating", "pf_fmv_assets_eoy", "pf_book_assets_boy", "pf_total_grants_paid",
          "sponsor_ein", "sponsor_name", "sponsor_type", "sponsor_subtype", "sponsor_segment", "sponsor_tier",
          "sponsor_rank_fy2024", "match_method", "lines", "amount_usd", "daf_purpose_amount_usd", "largest_line_usd",
          "share_of_pf_grants_paid", "recipient_name_filed", "purpose_text", "xml_url", "source")


# ----------------------------------------------------------------------------- edges
def load_bmf(d: str, eins: frozenset) -> dict:
    def rows(p):
        with open(p, newline="", encoding="utf-8", errors="replace") as fh:
            yield from (r for r in csv.DictReader(fh) if r["EIN"] in eins)
    return {r["EIN"]: r for p in sorted(glob.glob(os.path.join(d, "eo[1-4].csv"))) for r in rows(p)}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("task", choices=("frame", "extend", "harvest", "build"))
    ap.add_argument("--irs-dir")
    ap.add_argument("--index-2026", help="newer copy of index_2026.csv (task extend)")
    ap.add_argument("--bmf-dir")
    ap.add_argument("--cache", required=True)
    ap.add_argument("--procs", type=int, default=40)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)
    data = os.path.join(os.path.abspath(a.root), "data", "mission-2026-11-14")
    frame_p = os.path.join(a.cache, "frame.csv")
    panel = panel_from(read_csv(DAFRC_CSV))
    bmf = load_bmf(a.bmf_dir, frozenset(panel)) if a.bmf_dir else {}
    keys = panel_keys(panel, bmf)
    if a.task == "frame":
        def tagged(y):
            return ({**r, "_index_year": str(y)} for r in index_rows(os.path.join(a.irs_dir, f"index_{y}.csv")))
        fr = build_frame(r for y in INDEX_YEARS for r in tagged(y))
        write_csv(frame_p, fr, ("object_id", "ein", "tax_period", "tax_year", "name", "sub_date", "index_year"))
        print(json.dumps({ty: sum(1 for r in fr if r["tax_year"] == ty) for ty in TAX_YEARS}))
        return 0
    if a.task == "extend":
        # append returns found in a newer index_2026.csv; existing frame order (and so harvest chunks) is unchanged
        old = read_csv(frame_p)
        seen = frozenset(r["object_id"] for r in old)
        src = lambda y: a.index_2026 if y == 2026 else os.path.join(a.irs_dir, f"index_{y}.csv")  # noqa: E731
        fr = build_frame({**r, "_index_year": str(y)} for y in INDEX_YEARS for r in index_rows(src(y)))
        add = tuple(r for r in fr if r["object_id"] not in seen)
        write_csv(frame_p, (*old, *add), ("object_id", "ein", "tax_period", "tax_year", "name", "sub_date", "index_year"))
        print(json.dumps({"added": len(add), "by_tax_year": {ty: sum(1 for r in add if r["tax_year"] == ty) for ty in TAX_YEARS}}))
        return 0
    if a.task == "harvest":
        fr = tuple({**r, "tax_year": int(r["tax_year"])} for r in read_csv(frame_p))
        harvest(fr[: a.limit] if a.limit else fr, a.cache, keys, a.procs)
        return 0
    h = latest_per_period(load_harvest(a.cache))
    league = read_csv(os.path.join(data, LEAGUE_CSV))
    rank = {r["ein"]: int(r["rank_assets"]) for r in league if r["fiscal_year"] == "2024" and r["row_type"] == "top50"}
    rows = sorted(matched_rows(h, keys, panel, bmf, rank), key=lambda m: (m["tax_year"], -m["amount_usd"]))
    write_csv(os.path.join(data, OUT_NAME), rows, FIELDS)
    s = {**summarise(h, rows, panel, league, read_csv(os.path.join(data, MARKET_CSV))),
         "unmatched_review": unmatched_review(h, keys, panel, bmf)}
    with open(os.path.join(a.cache, "pf_to_daf_summary.json"), "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=1, default=str)
    print(json.dumps({ty: {"parsed": v["parsed_returns"], "T1": v["by_tier"]["T1"], "T123": v["by_tier"]["T123"]["usd"],
                           "term": v["terminating_returns"]} for ty, v in s["by_year"].items()}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
