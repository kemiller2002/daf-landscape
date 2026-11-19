#!/usr/bin/env python3
"""Complaint rates with denominators for the FY2024 top-15 DAF sponsors and top-5 donation processors (P-GAP19-13).

Stdlib only, functional style: pure transforms, I/O only in read_csv() and main().

Numerator   Records with valence 'complaint' or 'mixed' dated 2021-01-01 or later (first four-digit year >= 2021;
            ranges that start before 2021 are excluded) from
              data/mission-2026-11-14/daf-user-complaints-corpus.csv            (244 rows, 2026-11-14)
              data/mission-2026-11-14/daf-user-complaints-corpus-additions-2026-11-19.csv  (this task)
            A record counts once for each entity its `organization` matches (ENTITIES regex). Generic records
            ("DAF sponsors (generic)" etc.) count for nobody. "big three" = Fidelity Charitable, Vanguard
            Charitable, DAFgiving360 (as in scripts/mission_complaint_rates.py).
Scopes      all_venues     every in-window complaint/mixed record
            review_venues  venue_type app_store or review_site only (App Store, Google Play, Trustpilot, BBB pages)
            strict         review_venues, minus records whose attribution_confidence starts with 'low', minus
                           records flagged dup_of= in notes, minus reviewer country != US where notes give one
Denominator FY2024 number_of_daf_accounts and total_daf_grants from dafrc-sponsor-schedule-d-fy2019-2024.csv
            with the applied R1 'filed replaces imputed' corrections in dafrc-corrections-itemized.csv (metrics
            daf_accounts_eoy, daf_grants), i.e. the same corrected values as the league table. No other source.
Rate        n / FY2024 accounts x 10,000 over the whole window (not annualised), plus an annualised version
            (window 2021-01-01..2026-11-19 = WINDOW_YEARS) and n per $1bn of FY2024 DAF grants.
Interval    exact (Garwood) 95% Poisson interval on n, divided by the denominator. Zero counts get a lower bound
            of 0 and an upper bound; they are flagged, because absence from a convenience sample is not a zero rate.
Venue rows  Venue-reported aggregate counts (BBB Wise Giving Alliance '36-month' complaint counts) are added as
            scope 'venue_reported_aggregate' with their own window (VENUE_AGGREGATES).

Usage:  python3 scripts/mission_complaint_rates_gap19.py
Output: data/mission-2026-11-14/complaint-rates-2026-11-19.csv  (refuses to overwrite an existing file unless --force)
"""
from __future__ import annotations

import csv
import math
import os
import re
import sys
from datetime import date
from typing import Callable, Iterable, Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
CORPUS = os.path.join(DATA, "daf-user-complaints-corpus.csv")
ADDITIONS = os.path.join(DATA, "daf-user-complaints-corpus-additions-2026-11-19.csv")
DAFRC = os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")
CORR = os.path.join(DATA, "dafrc-corrections-itemized.csv")
OUT = os.path.join(DATA, "complaint-rates-2026-11-19.csv")

MIN_YEAR = 2021
WINDOW_START, WINDOW_END = date(2021, 1, 1), date(2026, 11, 19)
WINDOW_YEARS = round((WINDOW_END - WINDOW_START).days / 365.25, 3)
REVIEW_VENUES = ("app_store", "review_site")
Z_ALPHA = 0.05

# (entity, group, rank note, EIN, corpus `organization` regex, venue check summary)
ENTITIES: tuple[tuple[str, str, str, str, str, str], ...] = (
    ("Fidelity Charitable", "top15_sponsor", "assets #1", "110303001", r"Fidelity Charitable|big three",
     "TP: no profile (404); BBB: no profile found; GP: com.fidelity.charitable (3 visible reviews)"),
    ("National Philanthropic Trust", "top15_sponsor", "assets #2", "237825575", r"National Philanthropic Trust|\bNPT\b",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("DAFgiving360 (Schwab Charitable)", "top15_sponsor", "assets #3", "311640316", r"DAFgiving360|Schwab Charitable|big three",
     "TP: no profile (dafgiving360.org, schwabcharitable.org); BBB: no profile found; GP: no app found"),
    ("Vanguard Charitable", "top15_sponsor", "assets #4", "232888152", r"Vanguard Charitable|big three",
     "TP: no profile; BBB: no profile found (Vanguard Group brokerage profile out of scope); GP: no app found"),
    ("Goldman Sachs Philanthropy Fund", "top15_sponsor", "assets #5", "311774905", r"GS DAF Philanthropy Fund|Goldman Sachs Philanthropy",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("Silicon Valley Community Foundation", "top15_sponsor", "assets #6", "205205488", r"Silicon Valley Community Foundation|\bSVCF\b",
     "TP: profile with 0 reviews; BBB: no profile found; GP: no app found"),
    ("Morgan Stanley GIFT", "top15_sponsor", "assets #7", "527082731", r"Morgan Stanley GIFT",
     "TP/BBB: only parent-firm profiles (out of scope); GP: no app found"),
    ("American Endowment Foundation", "top15_sponsor", "assets #8", "341747398", r"American Endowment|\bAEF\b",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("Renaissance Charitable Foundation", "top15_sponsor", "assets #9", "352129262", r"Renaissance Charitable|\bRCF\b|Renaissance \(Ren",
     "TP: www.reninc.com profile (2 reviews; administrator, not RCF); BBB: no profile found; GP: no app found"),
    ("National Christian Foundation", "top15_sponsor", "assets #10", "581493949", r"National Christian Foundation",
     "TP: no profile; BBB: no profile found; GP: no app (mobile web only)"),
    ("BofA Charitable Gift Fund", "top15_sponsor", "assets #11", "046010342", r"Bank of America Charitable|BofA Charitable",
     "TP/BBB: only parent-bank profiles (out of scope); GP: no app found"),
    ("The Chicago Community Trust", "top15_sponsor", "assets #12", "362167000", r"Chicago Community Trust",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("ImpactAssets", "top15_sponsor", "assets #13", "262048480", r"ImpactAssets",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("Jewish Communal Fund", "top15_sponsor", "assets #14", "237174183", r"Jewish Communal Fund",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("Foundation For The Carolinas", "top15_sponsor", "assets #15", "566047886", r"Foundation For The Carolinas",
     "TP: no profile; BBB: no profile found; GP: no app found"),
    ("AOGF (Benevity)", "processor", "processor grants #1", "810739440", r"Benevity|American Online Giving",
     "TP: benevity.com (87 reviews listed); BBB: no profile found; GP: org.benevity.app (3 visible reviews)"),
    ("PayPal Charitable Giving Fund", "processor", "processor grants #2", "450931286", r"PayPal Giving Fund|PayPal Charitable|GoFundMe / PayPal",
     "TP: no profile (paypalgivingfund.org); BBB: no PPGF profile found (give.org report read); GP: no separate app"),
    ("Blackbaud Giving Fund (YourCause)", "processor", "processor grants #3", "460942102", r"YourCause|Blackbaud Giving Fund",
     "TP: blackbaud.com company profile (17 listed; 2 giving-fund items); BBB: Blackbaud Inc profile (24 in 3 yrs; 1 giving item); GP: none"),
    ("Dechomai Asset Trust", "processor", "processor grants #4", "260724604", r"Dechomai",
     "TP: no profile; BBB: no profile found; GP: none"),
    ("Network for Good (For Good)", "processor", "processor grants #5", "680480736", r"Network for Good|For Good \(|\bForGood\b",
     "TP: networkforgood.com (17 listed; 3 giving-fund items); BBB: Bonterra Tech (17 in 3 yrs; 5 giving items); give.org report read"),
)

# Venue-reported aggregate counts: (EIN, label, n, window_years, source)
VENUE_AGGREGATES: tuple[tuple[str, str, int, float, str], ...] = (
    ("680480736", "BBB Wise Giving Alliance: complaints processed by BBB in last 36 months (check disbursement)", 2, 3.0,
     "https://give.org/charity-reviews/other/forgood-in-washington-dc-9999-1290"),
)


# ---------- I/O edge ----------
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


# ---------- pure helpers ----------
def first_year(d: str) -> int | None:
    m = re.search(r"(19|20)\d\d", d or "")
    return int(m.group(0)) if m else None


def in_window(rec: Mapping) -> bool:
    y = first_year(rec["date"])
    return rec["valence"] in ("complaint", "mixed") and y is not None and y >= MIN_YEAR


def note_value(rec: Mapping, key: str) -> str:
    m = re.search(rf"\b{key}=([A-Za-z0-9-]+)", rec.get("notes", ""))
    return m.group(1) if m else ""


def is_strict(rec: Mapping) -> bool:
    return (rec["venue_type"] in REVIEW_VENUES
            and not rec.get("attribution_confidence", "").lower().startswith("low")
            and not note_value(rec, "dup_of")
            and note_value(rec, "country") in ("", "US"))


def is_distinct(rec: Mapping) -> bool:
    """Drop records flagged dup_of= in every scope, so one event is never counted twice [V wave 32B]."""
    return not note_value(rec, "dup_of")


SCOPES: tuple[tuple[str, Callable[[Mapping], bool]], ...] = (
    ("all_venues", is_distinct),
    ("review_venues", lambda r: r["venue_type"] in REVIEW_VENUES and is_distinct(r)),
    ("strict", is_strict),
)


def corrected_fy2024(dafrc: Sequence[Mapping], corr: Sequence[Mapping]) -> dict[str, dict]:
    """EIN -> {'accounts', 'accounts_src', 'grants', 'grants_src'} for FY2024, R1 corrections applied. Pure."""
    fix = {(c["ein"].zfill(9), c["metric"]): float(c["corrected_value"]) for c in corr
           if c["fiscal_year"] == "2024" and c.get("applied") == "1" and c["metric"] in ("daf_accounts_eoy", "daf_grants")}

    def one(r: Mapping) -> dict:
        ein = r["ein"].zfill(9)
        acc = fix.get((ein, "daf_accounts_eoy"), float(r["number_of_daf_accounts"] or "nan"))
        gr = fix.get((ein, "daf_grants"), float(r["total_daf_grants"] or "nan"))
        return {"accounts": acc, "grants": gr,
                "accounts_src": "R1 filed 990 (replaces DAFRC imputed)" if (ein, "daf_accounts_eoy") in fix
                else f"DAFRC FY2024 ({r['source_number_of_accounts']})",
                "grants_src": "R1 filed 990 (replaces DAFRC imputed)" if (ein, "daf_grants") in fix
                else f"DAFRC FY2024 ({r['source_total_daf_grants']})"}

    return {r["ein"].zfill(9): one(r) for r in dafrc if r["fiscal_year_end"] == "2024"}


def accounts_quality(acc: float, src: str) -> str:
    if not acc or math.isnan(acc) or acc < 10:
        return "implausible (not used)"
    return "imputed (DAFRC estimate)" if "Imputed" in src else "filed or paper submission"


def poisson_cdf(k: int, mu: float) -> float:
    if mu <= 0:
        return 1.0
    return math.fsum(math.exp(i * math.log(mu) - mu - math.lgamma(i + 1)) for i in range(k + 1))


def bisect(f: Callable[[float], float], lo: float, hi: float, n: int = 200) -> float:
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


def poisson_ci(k: int, alpha: float = Z_ALPHA) -> tuple[float, float]:
    """Exact (Garwood) two-sided interval for a Poisson count k."""
    hi_cap = k + 20 + 10 * math.sqrt(k + 1)
    upper = bisect(lambda mu: poisson_cdf(k, mu) - alpha / 2, 0.0, hi_cap)
    lower = 0.0 if k == 0 else bisect(lambda mu: alpha / 2 - (1 - poisson_cdf(k - 1, mu)), 1e-12, hi_cap)
    return lower, upper


def fmt(x: float | None, nd: int = 3) -> str:
    return "" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def rate_block(n: int, accounts: float | None, grants: float | None, years: float) -> dict:
    lo, hi = poisson_ci(n)
    per10k = (lambda v: v / accounts * 10000) if accounts else (lambda v: None)
    perbn = (lambda v: v / (grants / 1e9)) if grants else (lambda v: None)
    return {"rate_per_10k_accounts": fmt(per10k(n)), "rate_per_10k_ci95_low": fmt(per10k(lo)),
            "rate_per_10k_ci95_high": fmt(per10k(hi)),
            "annual_rate_per_10k_accounts": fmt(per10k(n / years) if accounts else None),
            "annual_rate_per_10k_ci95_low": fmt(per10k(lo / years) if accounts else None),
            "annual_rate_per_10k_ci95_high": fmt(per10k(hi / years) if accounts else None),
            "rate_per_1bn_grants": fmt(perbn(n)), "rate_per_1bn_ci95_low": fmt(perbn(lo)),
            "rate_per_1bn_ci95_high": fmt(perbn(hi))}


def interpretable(n: int, quality: str, scope: str) -> str:
    if n == 0:
        return "no (zero records; upper bound only; absence from a convenience sample is not a zero rate)"
    if quality.startswith("implausible"):
        return "accounts denominator implausible; use per-$bn grants only"
    if quality.startswith("imputed"):
        return "weak (imputed account count; per-10k rate unreliable, prefer per-$bn grants)"
    if n < 5:
        return "weak (<5 records)"
    return "descriptive only (convenience sample)" + ("; venue-selected" if scope == "all_venues" else "")


def entity_rows(ent: tuple, recs: Sequence[Mapping], den: Mapping[str, dict]) -> tuple[dict, ...]:
    name, group, rank, ein, rx, venues = ent
    d = den.get(ein, {})
    acc, gr = d.get("accounts"), d.get("grants")
    q = accounts_quality(acc or 0.0, d.get("accounts_src", ""))
    acc_used = acc if acc and not q.startswith("implausible") else None
    mine = tuple(r for r in recs if re.search(rx, r["organization"], re.I))

    def row(scope: str, keep: Callable[[Mapping], bool]) -> dict:
        sel = tuple(r for r in mine if keep(r))
        n = len(sel)
        return {"entity": name, "entity_group": group, "rank_basis": rank, "ein": ein,
                "fy2024_accounts": fmt(acc, 0), "accounts_source": d.get("accounts_src", "no DAFRC FY2024 row"),
                "accounts_quality": q, "fy2024_daf_grants_usd": fmt(gr, 0),
                "grants_source": d.get("grants_src", ""), "scope": scope,
                "window": f"{WINDOW_START.isoformat()}..{WINDOW_END.isoformat()}", "window_years": WINDOW_YEARS,
                "n_complaint_mixed": n,
                "n_high_critical": sum(1 for r in sel if r["severity"] in ("high", "critical")),
                "n_from_additions": sum(1 for r in sel if r["record_id"].startswith("CMP-G1913")),
                **rate_block(n, acc_used, gr, WINDOW_YEARS),
                "venue_coverage": ";".join(sorted({r["venue_type"] for r in sel})) or "none",
                "venues_checked_2026_11_19": venues,
                "record_ids": ";".join(r["record_id"] for r in sel),
                "interpretable": interpretable(n, q, scope)}

    return tuple(row(s, k) for s, k in SCOPES)


def aggregate_rows(den: Mapping[str, dict]) -> tuple[dict, ...]:
    by_ein = {e[3]: e for e in ENTITIES}

    def row(agg: tuple) -> dict:
        ein, label, n, yrs, src = agg
        name, group, rank, _, _, venues = by_ein[ein]
        d = den.get(ein, {})
        acc, gr = d.get("accounts"), d.get("grants")
        q = accounts_quality(acc or 0.0, d.get("accounts_src", ""))
        acc_used = acc if acc and not q.startswith("implausible") else None
        return {"entity": name, "entity_group": group, "rank_basis": rank, "ein": ein,
                "fy2024_accounts": fmt(acc, 0), "accounts_source": d.get("accounts_src", ""),
                "accounts_quality": q, "fy2024_daf_grants_usd": fmt(gr, 0), "grants_source": d.get("grants_src", ""),
                "scope": "venue_reported_aggregate", "window": f"{label} [{src}]", "window_years": yrs,
                "n_complaint_mixed": n, "n_high_critical": "", "n_from_additions": "",
                **rate_block(n, acc_used, gr, yrs), "venue_coverage": "bbb_wise_giving_alliance",
                "venues_checked_2026_11_19": venues, "record_ids": "",
                "interpretable": interpretable(n, q, "venue_reported_aggregate")}

    return tuple(row(a) for a in VENUE_AGGREGATES)


def pooled_rows(rows: Sequence[Mapping], recs: Sequence[Mapping], den: Mapping[str, dict], group: str) -> tuple[dict, ...]:
    """Pooled over entities of a group that have >=1 record in the scope; each record counted once."""
    def one(scope: str, keep: Callable[[Mapping], bool]) -> dict:
        eins = {r["ein"] for r in rows if r["entity_group"] == group and r["scope"] == scope and r["n_complaint_mixed"]}
        ents = tuple(e for e in ENTITIES if e[3] in eins)
        rx = "|".join(e[4] for e in ents) or r"^$"
        sel = tuple(r for r in recs if keep(r) and re.search(rx, r["organization"], re.I))
        usable = tuple(e for e in ents if not accounts_quality(den[e[3]]["accounts"], den[e[3]]["accounts_src"]).startswith("implausible"))
        acc = sum(den[e[3]]["accounts"] for e in usable) or None
        gr = sum(den[e[3]]["grants"] for e in ents) or None
        n = len(sel)
        # accounts rate only meaningful if every pooled entity has a usable account count
        acc_used = acc if len(usable) == len(ents) else None
        return {"entity": f"POOLED {group} (entities with >=1 record in scope)", "entity_group": group, "rank_basis": "",
                "ein": "", "fy2024_accounts": fmt(acc, 0), "accounts_source": "sum over " + "; ".join(e[0] for e in ents),
                "accounts_quality": "sum" if acc_used else "not computed (an entity lacks a usable account count)",
                "fy2024_daf_grants_usd": fmt(gr, 0), "grants_source": "sum", "scope": scope,
                "window": f"{WINDOW_START.isoformat()}..{WINDOW_END.isoformat()}", "window_years": WINDOW_YEARS,
                "n_complaint_mixed": n, "n_high_critical": sum(1 for r in sel if r["severity"] in ("high", "critical")),
                "n_from_additions": sum(1 for r in sel if r["record_id"].startswith("CMP-G1913")),
                **rate_block(n, acc_used, gr, WINDOW_YEARS),
                "venue_coverage": ";".join(sorted({r["venue_type"] for r in sel})) or "none",
                "venues_checked_2026_11_19": "", "record_ids": "", "interpretable": "descriptive only (convenience sample)"}

    return tuple(one(s, k) for s, k in SCOPES)


def build(corpus: Iterable[Mapping], additions: Iterable[Mapping], dafrc: Sequence[Mapping],
          corr: Sequence[Mapping]) -> tuple[dict, ...]:
    recs = tuple(r for r in (*corpus, *additions) if in_window(r))
    den = corrected_fy2024(dafrc, corr)
    rows = tuple(row for e in ENTITIES for row in entity_rows(e, recs, den))
    return (rows + aggregate_rows(den) + pooled_rows(rows, recs, den, "top15_sponsor")
            + pooled_rows(rows, recs, den, "processor"))


def main(argv: Sequence[str]) -> int:
    if os.path.exists(OUT) and "--force" not in argv:
        print(f"{OUT} exists; pass --force to rebuild it", file=sys.stderr)
        return 1
    rows = build(read_csv(CORPUS), read_csv(ADDITIONS), read_csv(DAFRC), read_csv(CORR))
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
