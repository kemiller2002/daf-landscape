#!/usr/bin/env python3
"""P-PE-02: lenders and debt terms behind DAF-ecosystem software companies, from BDC schedules of investments.

Business development companies (BDCs; SEC file numbers 814-xxxxx) list every portfolio loan in their 10-K/10-Q
Consolidated Schedule of Investments: borrower, instrument, reference rate + spread, maturity, par, cost and fair
value. This script:
  1. queries SEC EDGAR full-text search (efts.sec.gov/LATEST/search-index) for each borrower term in 10-K/10-Q
     filed 2021-01-01 onward, keeping hits from BDC filers (file_num starting "814-");
  2. per (term, BDC) keeps the latest and the earliest filing (so marks and spread changes are visible);
  3. downloads each filing document once (cache), finds <tr> rows whose first cell names the borrower plus
     continuation rows (instrument-only first cell), and parses cells into instrument / spread / maturity /
     par / cost / fair value with simple heuristics. Raw cells are kept for audit.
No numbers are typed by hand: everything in the output comes from the filing text.

Q-N15 fix (2026-11-14): 10-K/10-Q schedules print a prior-period comparative schedule (prior fiscal year-end) after
the current one, so stamping every row with the filing's period mislabels comparatives. Each row now carries its own
`period_ending` (= `row_period`), taken from (1) the inline-XBRL contexts referenced inside the row
(<xbrli:instant>/<xbrli:endDate>), else (2) the nearest preceding "Schedule(s) of Investments ... <date>" heading,
else (3) the filing period (flagged). The filing's own period moves to `filing_period_ending`. Rows that repeat the
same schedule line (same lender, borrower, instrument terms, par, fair value and row period) across filings are
deduplicated, preferring the filing whose own period equals the row period. A latest-mark-per-loan table is written
alongside (bdc-loans-latest-marks.csv).

Output: data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv (one row per schedule line per period, deduplicated)
        data/mission-2026-11-14/bdc-loans-latest-marks.csv (one row per loan tranche at the lender's latest period)
        CACHE/edgar_hits.json (search hits), CACHE/edgar_docs/*.htm (filing documents)
Usage:  python3 scripts/mission_bdc_loans.py --cache-dir CACHE [--fetch]
Stdlib only; functional style (pure transforms, I/O at the edges).
"""
from __future__ import annotations

import argparse
import bisect
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Mapping, Sequence

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mission_990_contractors as m990  # noqa: E402

DATA = m990.DATA
OUT = os.path.join(DATA, "bdc-loans-daf-ecosystem.csv")
OUT_LATEST = os.path.join(DATA, "bdc-loans-latest-marks.csv")
UA = {"User-Agent": "research-client contact@example.org"}
EFTS = "https://efts.sec.gov/LATEST/search-index"
START, END = "2021-01-01", "2026-11-14"
# (target company as named in the repo, EDGAR phrase, regex the borrower cell must match)
TARGETS = (
    ("Foundation Source", "Foundation Source", r"^Foundation Source"),
    ("Ren", "Renaissance Philanthropic", r"Renaissance Philanthropic"),
    ("Ren", "RenPSG", r"RenPSG"),
    ("Bonterra (Apax)", "Bonterra", r"^Bonterra"),
    ("Bonterra (Apax) - legacy EveryAction", "EveryAction", r"EveryAction"),
    ("Bonterra (Apax) - legacy CyberGrants", "CyberGrants", r"CyberGrants"),
    ("Bonterra (Apax) - legacy Social Solutions", "Social Solutions Global", r"Social Solutions Global"),
    ("Benevity (Hg)", "Benevity", r"Benevity"),
    ("Orion Advisor Solutions", "Orion Advisor", r"Orion Advisor"),
    ("Bloomerang", "Bloomerang", r"Bloomerang"),
    ("Foundant", "Foundant", r"Foundant"),
    ("Fundraise Up", "Fundraise Up", r"Fundraise Up"),
    ("Community Brands / Momentive", "Community Brands", r"Community Brands"),
    ("Community Brands / Momentive", "Momentive", r"Momentive Software"),
    ("Envestnet", "Envestnet", r"Envestnet"),
    ("OneCause", "OneCause", r"OneCause"),
    ("Neon One", "Neon One", r"Neon One"),
    ("Virtuous", "Virtuous Software", r"Virtuous Software"),
    ("GiveSmart", "GiveSmart", r"GiveSmart"),
    ("SofterWare (DonorPerfect)", "SofterWare", r"SofterWare"),
    ("Submittable", "Submittable", r"Submittable"),
)
INSTR = re.compile(r"(lien|revolv|term loan|delayed|unitranche|one stop|senior secured|second|subordinat|preferred|"
                   r"common|LP interest|units|warrant|equity|note|incremental|DDTL|first out|last out)", re.I)
DATE = re.compile(r"^(\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}/\d{4}|[A-Z][a-z]{2,8}\.? \d{4}|[A-Z][a-z]{2,8}\.? \d{1,2}, \d{4}|\d{4}-\d{2}-\d{2})$")
SPREAD = re.compile(r"(SOFR|S|SF|L|LIBOR|E|Prime|P|Base|CDOR|SONIA|BSBY)\s*\+\s*([\d.]+)\s*%?", re.I)
PCT = re.compile(r"^\(?([\d.]+)\s*%\)?$")
NUMC = re.compile(r"^\(?[\d,]+(\.\d+)?\)?$")


# ----------------------------------------------------------------------------- I/O edges
def http_get(url: str, retries: int = 3) -> bytes:
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            time.sleep(2 + 3 * attempt)
    return b""


def efts_url(phrase: str, frm: int) -> str:
    return EFTS + "?" + urllib.parse.urlencode({"q": f'"{phrase}"', "forms": "10-K,10-Q", "dateRange": "custom",
                                                "startdt": START, "enddt": END, "from": frm})


def search(phrase: str) -> tuple[dict, ...]:
    def page(frm):
        time.sleep(0.25)
        raw = http_get(efts_url(phrase, frm))
        try:
            return json.loads(raw or b"{}").get("hits", {})
        except json.JSONDecodeError:
            return {}
    first = page(0)
    total = (first.get("total") or {}).get("value", 0)
    rest = tuple(page(f).get("hits", []) for f in range(100, min(total, 1000), 100))
    hits = tuple(first.get("hits", [])) + tuple(h for p in rest for h in p)
    return tuple(hit_row(phrase, h) for h in hits)


def hit_row(phrase: str, h: Mapping) -> dict:
    s = h["_source"]
    adsh, fname = h["_id"].split(":", 1)
    cik = s["ciks"][0].lstrip("0")
    return {"phrase": phrase, "cik": cik, "entity": re.sub(r"\s+\(.*$", "", s["display_names"][0]).strip(),
            "file_num": (s.get("file_num") or [""])[0], "form": s["form"], "file_date": s["file_date"],
            "period_ending": s.get("period_ending") or "", "adsh": adsh, "fname": fname,
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{adsh.replace('-', '')}/{fname}",
            "query_url": efts_url(phrase, 0)}


def cached_hits(cache_dir: str, fetch: bool) -> tuple[dict, ...]:
    path = os.path.join(cache_dir, "edgar_hits.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return tuple(json.load(fh))
    if not fetch:
        return ()
    hits = tuple(h for _, phrase, _ in dict.fromkeys(TARGETS) for h in search(phrase))
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(hits, fh)
    return hits


def doc_text(cache_dir: str, url: str, fetch: bool) -> str:
    path = os.path.join(cache_dir, "edgar_docs", re.sub(r"[^\w.]", "_", url.split("/data/")[-1]))
    if not os.path.exists(path):
        if not fetch:
            return ""
        time.sleep(0.2)
        raw = http_get(url)
        if not raw:
            return ""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(raw)
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


# ----------------------------------------------------------------------------- pure transforms
def select_filings(hits: Sequence[Mapping]) -> tuple[dict, ...]:
    """BDC hits only; per (phrase, cik) keep earliest and latest filing (main document only)."""
    bdc = tuple(h for h in hits if h["file_num"].startswith("814-") and h["fname"].lower().endswith((".htm", ".html")))
    keys = sorted({(h["phrase"], h["cik"]) for h in bdc})
    def pick(k):
        hs = sorted((h for h in bdc if (h["phrase"], h["cik"]) == k), key=lambda h: (h["file_date"], h["fname"]))
        return (hs[0], hs[-1]) if hs[0]["adsh"] != hs[-1]["adsh"] else (hs[-1],)
    return tuple({**h, "which": "latest" if i == len(p) - 1 else "earliest"} for k in keys for p in (pick(k),)
                 for i, h in enumerate(p))


def cells_of(tr: str) -> tuple[str, ...]:
    raw = (html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c))).replace("​", "").strip()
           for c in re.split(r"</t[dh]>", tr, flags=re.I))
    return tuple(c for c in raw if c and c not in ("$", "%", ")", "(", "€", "£", "C$"))


def tr_matches(text: str) -> tuple:
    return tuple(re.finditer(r"<tr[\s>].*?</tr>", text, flags=re.I | re.S))


def table_rows(text: str) -> tuple[tuple[str, ...], ...]:
    return tuple(cells_of(m.group(0)) for m in tr_matches(text))


# ----------------------------------------------------------------------------- row period (Q-N15)
MONTHS = {m: i + 1 for i, m in enumerate(("january", "february", "march", "april", "may", "june", "july", "august",
                                          "september", "october", "november", "december"))}
LONGDATE = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December)"
                      r"\s+(\d{1,2})\s*,\s*(\d{4})", re.I)
SOI_HEAD = re.compile(r"Schedules?(?:\s|&#160;|&nbsp;|<[^>]+>)+of(?:\s|&#160;|&nbsp;|<[^>]+>)+Investments", re.I)


def plain_text(raw: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).replace("\xa0", " ").strip()


def iso_date(m) -> str:
    return f"{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"


def xbrl_context_dates(text: str) -> dict:
    """Inline-XBRL context id -> period date (instant, else duration end date)."""
    ctx = re.finditer(r"<xbrli:context\b[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</xbrli:context>", text, flags=re.I | re.S)
    return {m.group(1): d.group(1) for m in ctx
            for d in (re.search(r"<xbrli:(?:instant|endDate)>\s*(\d{4}-\d{2}-\d{2})", m.group(2), re.I),) if d}


def schedule_headings(text: str) -> tuple[tuple[int, str], ...]:
    """(position, ISO date) for each 'Schedule(s) of Investments' heading followed by exactly one date within
    ~160 characters of plain text (headings that list two dates, e.g. table-of-contents or note text, are skipped)."""
    def one(m):
        tail = plain_text(text[m.end():m.end() + 3000])[:160]
        d = LONGDATE.search(tail)
        two = d is not None and re.match(r"\s*(?:and|,)\s*(?:\w+\s+\d{1,2},\s*)?\d{4}", tail[d.end():])
        return (m.start(), iso_date(d)) if d is not None and d.start() < 60 and not two else None
    return tuple(h for h in (one(m) for m in SOI_HEAD.finditer(text)) if h)


def row_period(raw_row: str, start: int, ctx: Mapping, heads: Sequence, filing_period: str) -> dict:
    """Own period of a schedule row: XBRL contexts in the row > preceding schedule heading > filing period."""
    refs = re.findall(r"contextRef=\"([^\"]+)\"", raw_row, flags=re.I)
    xd = tuple(sorted({ctx[r] for r in refs if r in ctx}))
    x = xd[-1] if xd else ""  # rows with current + prior columns (commitment notes): take the current (latest) date
    k = bisect.bisect_right(tuple(p for p, _ in heads), start) - 1
    h = heads[k][1] if k >= 0 else ""
    src = "xbrl_context" if x else ("schedule_heading" if h else "filing_period_fallback")
    return {"period_ending": x or h or filing_period, "row_period_source": src, "row_period_xbrl": x,
            "row_period_heading": h, "row_period_conflict": ";".join(c for c in ("xbrl_vs_heading" if x and h and x != h else "",
                                                       "multi_xbrl_dates:" + "|".join(xd) if len(xd) > 1 else "") if c)}


def matched_rows(rows: Sequence[tuple], rx: str) -> tuple[tuple[int, tuple], ...]:
    """Rows whose first cell names the borrower, plus following continuation rows (first cell is an instrument)."""
    pat = re.compile(rx, re.I)
    starts = tuple(i for i, r in enumerate(rows) if r and pat.search(r[0]))
    def cont(i):
        j = i + 1
        out = ()
        while j < len(rows) and rows[j] and INSTR.match(rows[j][0]) and len(out) < 8:
            out += ((j, rows[j]),)
            j += 1
        return out
    seen = {}
    for i in starts:
        seen.setdefault(i, rows[i])
        for j, r in cont(i):
            seen.setdefault(j, r)
    return tuple(sorted(seen.items()))


REF = re.compile(r"^(SOFR|S|SF|L|LIBOR|E|EURIBOR|Prime|P|Base|CDOR|SONIA|BSBY)(\s*\(\w\))?\s*\+?\s*([\d.]+\s*%?)?$", re.I)


def to_num(c: str):
    """'1,234' -> 1234.0; '(12)' -> -12.0; dash -> 0.0; else None."""
    c = c.replace(" ", "")
    if c in ("—", "–", "-"):
        return 0.0
    if NUMC.match(c):
        v = float(c.strip("()").replace(",", ""))
        return -v if c.startswith("(") else v
    return None


def amounts_after(cells: Sequence[str], k: int) -> tuple[float, ...]:
    """Numeric cells after index k; small decimals (percent of net assets) dropped when 4+ values present."""
    vals = tuple((c, to_num(c)) for c in cells[k + 1:])
    vals = tuple((c, v) for c, v in vals if v is not None)
    vals = vals[:-1] if len(vals) >= 4 and re.fullmatch(r"\(\s*\d{1,2}\s*\)", vals[-1][0]) else vals  # trailing footnote "(15)"
    keep = vals if len(vals) < 4 else tuple((c, v) for c, v in vals if not ("." in c and abs(v) < 100))
    return tuple(v for _, v in keep)


def rate_terms(cells: Sequence[str], end: int) -> tuple[str, str, str]:
    """(reference rate, spread %, floor %) from cells before index end."""
    k = next((i for i, c in enumerate(cells[:end]) if REF.match(c.replace("%", "% ").strip())), None)
    inl = next((m for c in cells[:end] for m in (re.search(r"\b(SOFR|SF|S|LIBOR|L|E|Prime|P)\s*(\(\w\))?\s*\+\s*([\d.]+)", c),) if m), None)
    if inl is not None and (k is None or not (REF.match(cells[k].strip()).group(3) or "")):
        v = float(inl.group(3))
        if k is None or v > 0:
            return inl.group(1), (f"{v / 100:.2f}" if v > 20 else inl.group(3)), ""
    if k is None:
        return "", "", ""
    m = REF.match(cells[k].strip())
    ref = m.group(1)
    inline = (m.group(3) or "").replace("%", "").strip()
    nxt = tuple(PCT.match(c.replace(" ", "")).group(1) for c in cells[k + 1:end] if PCT.match(c.replace(" ", "")))
    nxt = tuple(re.match(r"([\d.]+)", c).group(1) for c in cells[k + 1:end]
                if re.match(r"^[\d.]+\s*%?(\s*PIK)?$", c.strip())) if not nxt else nxt
    cand = ((inline,) if inline else ()) + nxt
    if not cand:
        return ref, "", ""
    cand = tuple(f"{float(c) / 100:.2f}" if float(c) > 20 else c for c in cand if c not in ("", "."))
    if not cand:
        return ref, "", ""
    if len(cand) >= 2 and float(cand[0]) <= 1.0 < float(cand[1]):
        return ref, cand[1], cand[0]
    return ref, cand[0], (cand[1] if len(cand) >= 2 and float(cand[1]) <= 1.0 else "")


def parse_row(cells: Sequence[str], name_cell: str) -> dict:
    joined = " | ".join(cells)
    date_idx = tuple(i for i, c in enumerate(cells) if DATE.match(c.strip()))
    instr = next((c for c in cells if INSTR.search(c) and not REF.match(c) and len(c) < 80), "")
    if not instr and re.search(r"\((Revolver|Delayed Draw)\)", name_cell):
        instr = re.search(r"\((Revolver|Delayed Draw)\)", name_cell).group(1)
    is_equity = bool(re.search(r"common|preferred|LP interest|units|warrant|equity|shares", instr, re.I))
    end = date_idx[-1] if date_idx else len(cells)
    ref, spread, floor = rate_terms(cells, end)
    is_equity = is_equity and not spread
    amts = amounts_after(cells, end) if date_idx else amounts_after(cells, 0 if len(cells) < 2 else
                                                                     max(i for i, c in enumerate(cells) if to_num(c) is None))
    par, cost, fv = ((amts[0], amts[1], amts[-1]) if len(amts) >= 3 else
                     (amts[0], None, amts[1]) if len(amts) == 2 else (None, None, amts[0] if amts else None))
    rtype = ("equity" if is_equity else
             "name_or_subtotal_row" if not spread and not date_idx else
             "possible_unfunded_commitment" if len(amts) <= 2 and date_idx else
             "unfunded_or_zero_position" if not par and fv is not None and abs(fv) < 50 else
             "revolver_or_ddtl_commitment_basis" if (re.search(r"revolv|delayed|DDTL", instr + name_cell, re.I)
                                                       and par and fv is not None and fv < 0.9 * par) else "debt")
    return {"borrower_name_as_listed": name_cell, "instrument": instr, "ref_rate": ref, "spread_pct": spread,
            "floor_pct": floor, "pik_flag": "PIK" if "PIK" in joined.upper() else "",
            "dates_in_row": ";".join(cells[i] for i in date_idx),
            "maturity": cells[date_idx[-1]] if date_idx and not is_equity else "",
            "par_or_principal": par, "amortized_cost": cost, "fair_value": fv,
            "fv_pct_of_par": round(100 * fv / par, 2) if par and fv is not None and rtype == "debt" else None,
            "fv_pct_of_cost": round(100 * fv / cost, 2) if cost and fv is not None and rtype in ("debt", "equity") else None,
            "row_type": rtype, "row_cells_raw": joined[:600]}


def units_hint(text: str) -> str:
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))
    hits = tuple(plain[m.end():m.end() + 400].lower() for m in re.finditer(r"Schedules? of Investments", plain, re.I))
    th = sum("thousand" in h for h in hits)
    mi = sum("in millions" in h for h in hits)
    return "thousands" if th > mi and th else ("millions" if mi else "dollars_or_unstated")


def rows_for_filing(f: Mapping, text: str) -> tuple[dict, ...]:
    target, rx = next((t, r) for t, p, r in TARGETS if p == f["phrase"])
    trs = tr_matches(text)
    rows = tuple(cells_of(m.group(0)) for m in trs)
    hint = units_hint(text)
    hits = matched_rows(rows, rx)
    ctx = xbrl_context_dates(text) if hits else {}
    heads = schedule_headings(text) if hits else ()
    def name_for(i, r):
        return r[0] if re.search(rx, r[0], re.I) else next((rows[k][0] for k in range(i, -1, -1) if rows[k] and re.search(rx, rows[k][0], re.I)), "")
    out = tuple({"target_company": target, "edgar_phrase": f["phrase"], "lender_bdc": f["entity"], "lender_cik": f["cik"],
                 "file_num": f["file_num"], "form": f["form"], "filing_date": f["file_date"],
                 "filing_period_ending": f["period_ending"], "adsh": f["adsh"], "which_filing": f["which"], "units_hint": hint,
                 "table_row_index": i, **parse_row(r, name_for(i, r)),
                 **row_period(trs[i].group(0), trs[i].start(), ctx, heads, f["period_ending"]),
                 "filing_url": f["url"], "efts_query_url": f["query_url"]}
                for i, r in hits)
    return out if out else ({"target_company": target, "edgar_phrase": f["phrase"], "lender_bdc": f["entity"],
                             "lender_cik": f["cik"], "file_num": f["file_num"], "form": f["form"],
                             "filing_date": f["file_date"], "period_ending": f["period_ending"],
                             "filing_period_ending": f["period_ending"], "adsh": f["adsh"],
                             "row_period_source": "filing_period_fallback", "which_filing": f["which"], "units_hint": hint, "row_type": "text_hit_no_table_row",
                             "filing_url": f["url"], "efts_query_url": f["query_url"]},)


def below_par(r: Mapping) -> str:
    v = r.get("fv_pct_of_par")
    return "" if v is None or r.get("row_type") != "debt" else ("yes_lt_97" if v < 97 else ("slight_97_99.5" if v < 99.5 else "no"))


def parse_check(r: Mapping) -> str:
    """Flags rows whose parsed values are implausible; row_cells_raw then governs."""
    sp, fp = num(r.get("spread_pct")), r.get("fv_pct_of_par")
    par, fv = r.get("par_or_principal"), r.get("fair_value")
    bad = ((sp is not None and sp > 10) or (fp is not None and (fp > 110 or fp < 50))
           or (par and fv is not None and fv < 0 and r.get("row_type") == "debt"))
    return "check_raw" if bad else ""


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def identity_note(r: Mapping) -> str:
    """How sure the borrower-as-listed is the target company (rules stated here, not judged row by row)."""
    t, raw, mat = r.get("target_company", ""), r.get("row_cells_raw", ""), r.get("maturity", "") + r.get("dates_in_row", "")
    if t.startswith("Bonterra"):
        if re.search(r"cybergrants|everyaction", raw + r.get("borrower_name_as_listed", ""), re.I) or "2027" in mat:
            return "linked: CyberGrants/EveryAction lineage facility (Apax; CyberGrants Holdings renamed Bonterra LLC)"
        if "2032" in mat:
            return ("probable: 2025 refinancing of Apax Bonterra (AB 'Software & Tech Services' label; "
                    "2027 holders exited 2025)")
        return "unconfirmed: name match only"
    return {"Foundation Source": "probable: exact name; Audax was the 2020 lender; 9/6/2030 maturity fits the Sept-2023 GTCR buyout",
            "Orion Advisor Solutions": "confirmed: exact legal name",
            "Bloomerang": "confirmed: exact name (Bloomerang, LLC)",
            "Community Brands / Momentive": "linked: Community Brands ParentCo (renamed Momentive Software 2024); 2031 maturities match the July-2024 refinancing",
            "Envestnet": "confirmed: Envestnet or BCPE Pequod Buyer (dba Envestnet), Bain take-private vehicle"}.get(t, "name match only")


def no_hit_rows(hits: Sequence[Mapping]) -> tuple[dict, ...]:
    """Targets with no BDC 10-K/10-Q hit at all: one auditable row each."""
    bdc_phrases = {h["phrase"] for h in hits if h["file_num"].startswith("814-")}
    return tuple({"target_company": t, "edgar_phrase": p, "row_type": "no_bdc_hit",
                  "row_cells_raw": f"EDGAR FTS total hits (all filers) = {sum(1 for h in hits if h['phrase'] == p)}; none from an 814- filer",
                  "efts_query_url": efts_url(p, 0)} for t, p, _ in TARGETS if p not in bdc_phrases)


FIELDS = ("target_company", "identity_note", "edgar_phrase", "borrower_name_as_listed", "lender_bdc", "lender_cik", "file_num", "form",
          "filing_date", "adsh", "period_ending", "filing_period_ending", "is_comparative", "row_period_source", "row_period_xbrl",
          "row_period_heading", "row_period_conflict", "dup_count", "dup_filings", "also_matched_phrases", "which_filing", "row_type", "instrument", "ref_rate", "spread_pct",
          "floor_pct", "pik_flag", "dates_in_row", "maturity", "par_or_principal", "amortized_cost", "fair_value",
          "units_hint", "fv_pct_of_par", "fv_pct_of_cost", "below_par_signal", "parse_check", "table_row_index", "row_cells_raw",
          "filing_url", "efts_query_url")


# ----------------------------------------------------------------------------- dedupe + latest marks (Q-N15)
LOAN_TYPES = ("debt", "revolver_or_ddtl_commitment_basis", "unfunded_or_zero_position", "possible_unfunded_commitment", "equity")


def norm_name(x: str) -> str:
    return re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|\b(llc|inc|corp|lp|l\.p|ltd|co)\b\.?", "", (x or "").lower()))


def fnum(x) -> str:
    v = num(x)
    return "" if v is None else f"{v:.4f}"


def line_key(r: Mapping) -> tuple:
    """(lender, borrower, instrument, period) - instrument identity includes the terms, par and fair value, because
    the instrument label alone ('One stop', 'First Lien Term Loan') does not distinguish tranches of one facility."""
    return (r.get("lender_cik", ""), norm_name(r.get("borrower_name_as_listed", "")), (r.get("instrument") or "").lower(),
            r.get("ref_rate", ""), fnum(r.get("spread_pct")), r.get("pik_flag", ""), r.get("maturity", ""),
            fnum(r.get("par_or_principal")), fnum(r.get("fair_value")), r.get("row_type", ""), r.get("period_ending", ""))


def dedupe(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Keep every table row of ONE filing per line_key (rows of a single filing are distinct schedule lines);
    prefer the filing whose own period equals the row period, then the earliest filing date. Rows without a table
    row (no-hit / text-hit rows) pass through. Output order follows the input order."""
    seen, tab, also = set(), (), {}
    for r in rows:  # stage 1: one filing row matched by two EDGAR phrases (e.g. Bonterra + CyberGrants) -> first target wins
        if r.get("table_row_index") in (None, ""):
            continue
        k = (r["adsh"], r["table_row_index"])
        if k in seen:
            also[k] = also.get(k, ()) + (r["edgar_phrase"],)
        else:
            seen.add(k)
            tab += (r,)
    rows = tuple(r for r in rows if r.get("table_row_index") in (None, "") or any(r is t for t in tab))
    groups = {}
    for r in tab:
        groups.setdefault(line_key(r), []).append(r)
    def pick(rs):
        best = min(rs, key=lambda r: (r.get("filing_period_ending") != r.get("period_ending"), r.get("filing_date", ""), r.get("adsh", "")))
        return best["adsh"]
    keep = {k: pick(v) for k, v in groups.items()}
    meta = {k: (len({r["adsh"] for r in v}), ";".join(sorted({r["adsh"] for r in v}))) for k, v in groups.items()}
    def tabular(r):
        return r.get("table_row_index") not in (None, "")
    return tuple({**r, "is_comparative": "yes" if r.get("period_ending") != r.get("filing_period_ending") else "",
                  "dup_count": meta[line_key(r)][0], "dup_filings": meta[line_key(r)][1],
                  "also_matched_phrases": ";".join(also.get((r["adsh"], r["table_row_index"]), ()))} if tabular(r) else
                 {**r, "is_comparative": "", "dup_count": 1, "dup_filings": r.get("adsh", "")}
                 for r in rows if not tabular(r) or r["adsh"] == keep[line_key(r)])


def target_group(r: Mapping) -> str:
    """Legacy-name phrases (e.g. 'Bonterra (Apax) - legacy CyberGrants') belong to the same company group."""
    return (r.get("target_company") or "").split(" - legacy")[0]


def maturity_month(m: str) -> str:
    """'9/8/2027', '09/08/2027', '09/2027', '03/2032' -> 'YYYY-MM' (facility identity; the day is printed inconsistently)."""
    a = re.fullmatch(r"(\d{1,2})/(?:\d{1,2}/)?(\d{2,4})", (m or "").strip())
    if not a:
        return (m or "").strip()
    y = int(a.group(2))
    return f"{y + 2000 if y < 100 else y:04d}-{int(a.group(1)):02d}"


def facility_key(r: Mapping) -> tuple:
    """(lender, company group, maturity month) for debt; instrument label for equity / undated rows. The borrower name
    is not in the key because lenders rename it over time (CyberGrants Holdings -> Bonterra LLC (fka ...))."""
    return (r.get("lender_cik", ""), target_group(r), maturity_month(r.get("maturity", "")) or
            "instr:" + (r.get("instrument") or "").lower())


def latest_marks(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Per (lender, target, borrower, maturity) facility: all tranche rows at the facility's latest row period, plus
    the lender's latest schedule date for that target (latest filing period searched) and a status flag. Rows whose
    cells reference two XBRL periods (unfunded-commitment notes printing current | prior columns) are excluded."""
    loans = tuple(r for r in rows if r.get("row_type") in LOAN_TYPES  # two-period commitment-note rows are not marks
                  and "multi_xbrl_dates" not in (r.get("row_period_conflict") or ""))
    lender_latest = {}
    for r in rows:
        k = (r.get("lender_cik", ""), target_group(r))
        lender_latest[k] = max(lender_latest.get(k, ""), r.get("filing_period_ending") or "")
    fac_latest = {}
    for r in loans:
        fac_latest[facility_key(r)] = max(fac_latest.get(facility_key(r), ""), r["period_ending"])
    at = tuple(r for r in loans if r["period_ending"] == fac_latest[facility_key(r)])
    def agg(k):
        rs = tuple(r for r in at if facility_key(r) == k and r.get("row_type") == "debt")
        par = sum(num(r.get("par_or_principal")) or 0 for r in rs)
        fv = sum(num(r.get("fair_value")) or 0 for r in rs)
        return (round(par, 4), round(fv, 4), round(100 * fv / par, 2) if par else None)
    aggs = {k: agg(k) for k in {facility_key(r) for r in at}}
    def status(r):
        ll = lender_latest[(r.get("lender_cik", ""), target_group(r))]
        return "held_at_lender_latest_period" if r["period_ending"] >= ll else f"not_in_schedule_at_{ll}"
    out = tuple({**r, "company_group": target_group(r), "maturity_month": maturity_month(r.get("maturity", "")),
                 "lender_latest_schedule_period": lender_latest[(r.get("lender_cik", ""), target_group(r))],
                 "status": status(r), "facility_debt_par": aggs[facility_key(r)][0],
                 "facility_debt_fv": aggs[facility_key(r)][1], "facility_fv_pct_of_par": aggs[facility_key(r)][2]} for r in at)
    return tuple(sorted(out, key=lambda r: (r["company_group"], r["lender_bdc"], r["maturity_month"], r["period_ending"],
                                            int(r["table_row_index"]))))


LATEST_FIELDS = ("company_group", "target_company", "identity_note", "borrower_name_as_listed", "lender_bdc", "lender_cik", "period_ending",
                 "row_period_source", "lender_latest_schedule_period", "status", "row_type", "instrument", "ref_rate",
                 "spread_pct", "floor_pct", "pik_flag", "maturity", "maturity_month", "par_or_principal", "amortized_cost",
                 "fair_value", "units_hint", "fv_pct_of_par", "fv_pct_of_cost", "below_par_signal", "parse_check",
                 "facility_debt_par", "facility_debt_fv", "facility_fv_pct_of_par", "form", "filing_date",
                 "filing_period_ending", "is_comparative", "table_row_index", "row_cells_raw", "filing_url")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    hits = cached_hits(a.cache_dir, a.fetch)
    filings = select_filings(hits)
    raw = tuple({**r, "below_par_signal": below_par(r), "identity_note": identity_note(r), "parse_check": parse_check(r)} for f in filings
                for r in rows_for_filing(f, doc_text(a.cache_dir, f["url"], a.fetch))) + no_hit_rows(hits)
    rows = dedupe(raw)
    latest = latest_marks(rows)
    m990.write_csv(OUT, rows, FIELDS)
    m990.write_csv(OUT_LATEST, latest, LATEST_FIELDS)
    cnt = lambda rs, f: sum(1 for r in rs if f(r))
    print(f"hits={len(hits)} bdc_filings={len(filings)} rows_before_dedupe={len(raw)} rows_after_dedupe={len(rows)} "
          f"latest_mark_rows={len(latest)}")
    print("comparative rows (row period != filing period):", cnt(raw, lambda r: r.get("filing_period_ending") and r["period_ending"] != r["filing_period_ending"]),
          "| row_period_source:", {k: cnt(raw, lambda r, k=k: r.get("row_period_source") == k) for k in
                                   ("xbrl_context", "schedule_heading", "filing_period_fallback")},
          "| period conflicts flagged:", cnt(raw, lambda r: bool(r.get("row_period_conflict"))))
    by = {}
    for h in hits:
        by.setdefault(h["phrase"], set()).add((h["entity"], h["file_num"].startswith("814-")))
    for p, s in by.items():
        print(p, "| BDC:", sorted(e for e, b in s if b)[:12], "| non-BDC:", len([e for e, b in s if not b]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
