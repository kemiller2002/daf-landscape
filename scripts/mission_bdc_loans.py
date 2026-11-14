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

Output: data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv (one row per schedule line)
        CACHE/edgar_hits.json (search hits), CACHE/edgar_docs/*.htm (filing documents)
Usage:  python3 scripts/mission_bdc_loans.py --cache-dir CACHE [--fetch]
Stdlib only; functional style (pure transforms, I/O at the edges).
"""
from __future__ import annotations

import argparse
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


def table_rows(text: str) -> tuple[tuple[str, ...], ...]:
    return tuple(cells_of(m.group(0)) for m in re.finditer(r"<tr[\s>].*?</tr>", text, flags=re.I | re.S))


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
    keep = vals if len(vals) < 4 else tuple((c, v) for c, v in vals if not ("." in c and abs(v) < 100))
    return tuple(v for _, v in keep)


def rate_terms(cells: Sequence[str], end: int) -> tuple[str, str, str]:
    """(reference rate, spread %, floor %) from cells before index end."""
    k = next((i for i, c in enumerate(cells[:end]) if REF.match(c.replace("%", "% ").strip())), None)
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
    rows = table_rows(text)
    hint = units_hint(text)
    hits = matched_rows(rows, rx)
    def name_for(i, r):
        return r[0] if re.search(rx, r[0], re.I) else next((rows[k][0] for k in range(i, -1, -1) if rows[k] and re.search(rx, rows[k][0], re.I)), "")
    out = tuple({"target_company": target, "edgar_phrase": f["phrase"], "lender_bdc": f["entity"], "lender_cik": f["cik"],
                 "file_num": f["file_num"], "form": f["form"], "filing_date": f["file_date"],
                 "period_ending": f["period_ending"], "which_filing": f["which"], "units_hint": hint,
                 "table_row_index": i, **parse_row(r, name_for(i, r)), "filing_url": f["url"], "efts_query_url": f["query_url"]}
                for i, r in hits)
    return out if out else ({"target_company": target, "edgar_phrase": f["phrase"], "lender_bdc": f["entity"],
                             "lender_cik": f["cik"], "file_num": f["file_num"], "form": f["form"],
                             "filing_date": f["file_date"], "period_ending": f["period_ending"],
                             "which_filing": f["which"], "units_hint": hint, "row_type": "text_hit_no_table_row",
                             "filing_url": f["url"], "efts_query_url": f["query_url"]},)


def below_par(r: Mapping) -> str:
    v = r.get("fv_pct_of_par")
    return "" if v is None or r.get("row_type") != "debt" else ("yes_lt_97" if v < 97 else ("slight_97_99.5" if v < 99.5 else "no"))


FIELDS = ("target_company", "edgar_phrase", "borrower_name_as_listed", "lender_bdc", "lender_cik", "file_num", "form",
          "filing_date", "period_ending", "which_filing", "row_type", "instrument", "ref_rate", "spread_pct",
          "floor_pct", "pik_flag", "dates_in_row", "maturity", "par_or_principal", "amortized_cost", "fair_value",
          "units_hint", "fv_pct_of_par", "fv_pct_of_cost", "below_par_signal", "table_row_index", "row_cells_raw",
          "filing_url", "efts_query_url")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    hits = cached_hits(a.cache_dir, a.fetch)
    filings = select_filings(hits)
    rows = tuple({**r, "below_par_signal": below_par(r)} for f in filings
                 for r in rows_for_filing(f, doc_text(a.cache_dir, f["url"], a.fetch)))
    m990.write_csv(OUT, rows, FIELDS)
    print(f"hits={len(hits)} bdc_filings={len(filings)} rows={len(rows)}")
    by = {}
    for h in hits:
        by.setdefault(h["phrase"], set()).add((h["entity"], h["file_num"].startswith("814-")))
    for p, s in by.items():
        print(p, "| BDC:", sorted(e for e, b in s if b)[:12], "| non-BDC:", len([e for e, b in s if not b]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
