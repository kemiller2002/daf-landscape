#!/usr/bin/env python3
"""Scale-normalised complaint rates for adviser-channel (A3) and consumer (A4) DAF sponsors (queue item P-QA3-04).

Stdlib only, functional style (pure transforms; I/O at the edges).

Numerator   data/mission-2026-11-14/daf-user-complaints-corpus.csv: records with valence 'complaint' or 'mixed'
            dated 2021 or later (first four-digit year in `date` >= 2021; undated records and ranges that start before
            2021, e.g. 'c.2018-2022', are excluded). Counted by severity, with and without App Store records.
Attribution A record counts once for each named A3/A4 sponsor (ORG_PATTERNS). Generic records ('DAF sponsors
            (generic)', 'Multiple sponsors', 'Commercial sponsors (generic)') are attributed to nobody. CMP-220's
            "big three" is read as Fidelity Charitable, Vanguard Charitable and DAFgiving360, the three sponsors the
            corpus (CMP-215..219) names for the 2026 SPLC holds.
Denominator DAFRC FY2024 number_of_daf_accounts (dafrc-sponsor-schedule-d-fy2019-2024.csv) with the R1
            'filed replaces imputed' corrections from dafrc-corrections-itemized.csv (the corrected-totals pipeline).
Rate        complaints per 10,000 FY2024 accounts over the whole 2021-2026 window (not annualised).

The corpus is a convenience sample, not a sampling frame: venue access drove which sponsors have records (see the
venue_coverage column and research/mission-2026-11-14/queue-batch29-complaints-voids.md). Rates are descriptive of
the corpus only.

Usage: python3 scripts/mission_complaint_rates.py
Output: data/mission-2026-11-14/complaint-rates-normalised.csv
"""
from __future__ import annotations

import csv
import os
import re
from typing import Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
CORPUS = os.path.join(DATA, "daf-user-complaints-corpus.csv")
DAFRC = os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")
CORR = os.path.join(DATA, "dafrc-corrections-itemized.csv")
OUT = os.path.join(DATA, "complaint-rates-normalised.csv")
SEVERITIES = ("low", "medium", "high", "critical")
MIN_YEAR = 2021

# (sponsor, EIN, quadrant areas, corpus `organization` regex)
SPONSORS: tuple[tuple[str, str, str, str], ...] = (
    ("Fidelity Charitable", "110303001", "A3;A4", r"Fidelity Charitable|big three"),
    ("DAFgiving360 (Schwab Charitable)", "311640316", "A3;A4", r"DAFgiving360|Schwab Charitable|big three"),
    ("Vanguard Charitable", "232888152", "A3", r"Vanguard Charitable|big three"),
    ("National Philanthropic Trust", "237825575", "A3", r"National Philanthropic Trust|\bNPT\b"),
    ("Renaissance Charitable Foundation", "352129262", "A3", r"Renaissance Charitable|\bRCF\b"),
    ("American Endowment Foundation", "341747398", "A3", r"American Endowment|\bAEF\b"),
    ("GiveClear Foundation", "813222963", "A3", r"GiveClear"),
    ("Charityvest", "812771871", "A3;A4", r"Charityvest"),
    ("Morgan Stanley GIFT", "527082731", "A3", r"Morgan Stanley GIFT"),
    ("National Christian Foundation", "581493949", "A3", r"National Christian Foundation"),
    ("Goldman Sachs Philanthropy Fund (GS DAPF)", "311774905", "A3", r"GS DAF Philanthropy Fund|Goldman Sachs Philanthropy"),
    ("BofA Charitable Gift Fund", "046010342", "A3", r"Bank of America Charitable|BofA"),
    ("Daffy", "863177440", "A4", r"\bDaffy\b"),
    ("Endaoment", "844661797", "A4", r"Endaoment"),
    ("Givinga", "474172718", "A4", r"Givinga"),
    ("Every.org", "", "A4", r"Every\.org"),
)


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


def first_year(date: str) -> int | None:
    m = re.search(r"(19|20)\d\d", date or "")
    return int(m.group(0)) if m else None


def in_scope(rec: Mapping) -> bool:
    y = first_year(rec["date"])
    return rec["valence"] in ("complaint", "mixed") and y is not None and y >= MIN_YEAR


def accounts_fy2024(dafrc: Sequence[Mapping], corr: Sequence[Mapping]) -> dict[str, tuple[float, float, str]]:
    """EIN -> (accounts as published, corrected accounts, source note). Pure."""
    fix = {c["ein"].zfill(9): float(c["corrected_value"]) for c in corr
           if c["fiscal_year"] == "2024" and c["metric"] == "daf_accounts_eoy" and c.get("applied") == "1"}
    return {r["ein"].zfill(9): (float(r["number_of_daf_accounts"]), fix.get(r["ein"].zfill(9), float(r["number_of_daf_accounts"])),
                                f"DAFRC FY2024 ({r['source_number_of_accounts']})"
                                + ("; R1 corrected to filed 990" if r["ein"].zfill(9) in fix else ""))
            for r in dafrc if r["fiscal_year_end"] == "2024" and r["number_of_daf_accounts"]}


def counts(recs: Sequence[Mapping]) -> dict:
    return {**{f"n_{s}": sum(1 for r in recs if r["severity"] == s) for s in SEVERITIES}, "n_total": len(recs),
            "n_high_critical": sum(1 for r in recs if r["severity"] in ("high", "critical"))}


def per10k(n: int, denom: float | None) -> str:
    """Blank when there is no denominator or no record: a zero count in a convenience sample is not a zero rate."""
    return f"{n / denom * 10000:.3f}" if denom and n else ""


def sponsor_row(sp: tuple, recs: Sequence[Mapping], accts: Mapping) -> dict:
    name, ein, areas, rx = sp
    mine = tuple(r for r in recs if re.search(rx, r["organization"], re.I))
    no_app = tuple(r for r in mine if r["venue_type"] != "app_store")
    pub, corr, src = accts.get(ein, (None, None, "no DAFRC FY2024 row"))
    c_all, c_noapp = counts(mine), counts(no_app)
    venues = sorted({r["venue_type"] for r in mine})
    return {"sponsor": name, "ein": ein, "quadrant_areas": areas,
            "fy2024_accounts_dafrc_published": f"{pub:.0f}" if pub else "",
            "fy2024_accounts_corrected": f"{corr:.0f}" if corr else "", "accounts_source": src,
            **{f"all_{k}": v for k, v in c_all.items()},
            "all_rate_per_10k": per10k(c_all["n_total"], corr),
            "all_high_critical_rate_per_10k": per10k(c_all["n_high_critical"], corr),
            **{f"noapp_{k}": v for k, v in c_noapp.items()},
            "noapp_rate_per_10k": per10k(c_noapp["n_total"], corr),
            "noapp_high_critical_rate_per_10k": per10k(c_noapp["n_high_critical"], corr),
            "n_app_store": c_all["n_total"] - c_noapp["n_total"],
            "n_multi_sponsor_records": sum(1 for r in mine if re.search(r";|/|big three", r["organization"], re.I)),
            "venue_coverage": ";".join(venues) if venues else "none",
            "record_ids": ";".join(r["record_id"] for r in mine),
            "interpretable": ("no (zero records; absence from a convenience sample is not evidence of no complaints)" if not mine else
                              "no (no account denominator)" if not corr else
                              "weak (<5 records)" if len(mine) < 5 else "descriptive only (convenience sample)")}


def pooled_row(rows: Sequence[Mapping], recs: Sequence[Mapping], accts: Mapping) -> dict:
    """Pooled rate: distinct records attributed to any sponsor that has at least one record / sum of those
    sponsors' corrected accounts (sponsors with zero records are left out of numerator and denominator)."""
    with_recs = {r["ein"] for r in rows if r["all_n_total"] and r["ein"]}
    pool = tuple(sp for sp in SPONSORS if sp[1] in with_recs)
    rx = "|".join(sp[3] for sp in pool)
    mine = tuple(r for r in recs if re.search(rx, r["organization"], re.I))
    no_app = tuple(r for r in mine if r["venue_type"] != "app_store")
    denom = sum(accts[sp[1]][1] for sp in pool if sp[1] in accts)
    c_all, c_noapp = counts(mine), counts(no_app)
    return {"sponsor": "POOLED (A3/A4 sponsors with >=1 record; each record once)", "ein": "", "quadrant_areas": "A3;A4",
            "fy2024_accounts_dafrc_published": f"{sum(accts[sp[1]][0] for sp in pool if sp[1] in accts):.0f}",
            "fy2024_accounts_corrected": f"{denom:.0f}", "accounts_source": "sum over " + "; ".join(sp[0] for sp in pool),
            **{f"all_{k}": v for k, v in c_all.items()},
            "all_rate_per_10k": per10k(c_all["n_total"], denom),
            "all_high_critical_rate_per_10k": per10k(c_all["n_high_critical"], denom),
            **{f"noapp_{k}": v for k, v in c_noapp.items()},
            "noapp_rate_per_10k": per10k(c_noapp["n_total"], denom),
            "noapp_high_critical_rate_per_10k": per10k(c_noapp["n_high_critical"], denom),
            "n_app_store": c_all["n_total"] - c_noapp["n_total"],
            "n_multi_sponsor_records": sum(1 for r in mine if re.search(r";|/|big three", r["organization"], re.I)),
            "venue_coverage": ";".join(sorted({r["venue_type"] for r in mine})), "record_ids": "",
            "interpretable": "descriptive only (convenience sample)"}


def main() -> int:
    recs = tuple(r for r in read_csv(CORPUS) if in_scope(r))
    accts = accounts_fy2024(read_csv(DAFRC), read_csv(CORR))
    rows = tuple(sponsor_row(sp, recs, accts) for sp in SPONSORS)
    rows = rows + (pooled_row(rows, recs, accts),)
    fields = list(rows[0].keys())
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(recs)} in-scope corpus records (complaint/mixed, {MIN_YEAR}+); wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
