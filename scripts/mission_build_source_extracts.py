#!/usr/bin/env python3
"""Build machine-readable DAF source extracts for mission 2026-11-14 (stdlib only).

Outputs (under data/mission-2026-11-14/):
  * dafrc-sponsor-schedule-d-fy2019-2024.csv  - every row of the DAFRC Spring 2026
    "Annual DAF Report 2025 Updated Analysis Dataset" (Form 990 Schedule D Part I),
    reproduced verbatim plus provenance columns.
  * sponsor-level-metrics.csv                 - long-format sponsor metrics for the
    named large sponsors, combining (a) DAFRC Schedule D rows, (b) ProPublica
    Nonprofit Explorer Form 990 extracts (whole-organisation totals) and
    (c) curated sponsor self-reports (constants below, each with a source URL).

Design: pure functions that map inputs -> rows; I/O only at the edges (main).

Usage:
  python3 scripts/mission_build_source_extracts.py \
      [--dafrc-xlsx PATH] [--propublica-cache DIR] [--out-dir DIR]
Without --dafrc-xlsx / --propublica-cache the sources are downloaded.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import urllib.request
import zipfile
from functools import reduce
from typing import Iterable, Mapping, Sequence
from xml.etree import ElementTree as ET

RETRIEVED = "2026-11-14"
DAFRC_DATASET_URL = (
    "https://www.dafresearchcollaborative.org/s/"
    "Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"
)
DAFRC_PAGE_URL = "https://www.dafresearchcollaborative.org/research/annual-daf-report"
PROPUBLICA_API = "https://projects.propublica.org/nonprofits/api/v2/organizations/{ein}.json"
PROPUBLICA_ORG = "https://projects.propublica.org/nonprofits/organizations/{ein}"

# Named sponsors (EIN -> display name). EINs verified via ProPublica search API.
NAMED_SPONSORS: Mapping[str, str] = {
    "110303001": "Fidelity Charitable (Fidelity Investments Charitable Gift Fund)",
    "311640316": "DAFgiving360 (formerly Schwab Charitable; legal name Donor Advised Charitable Giving Inc)",
    "232888152": "Vanguard Charitable Endowment Program",
    "237825575": "National Philanthropic Trust",
    "581493949": "National Christian Charitable Foundation (NCF)",
    "205205488": "Silicon Valley Community Foundation",
    "311774905": "Goldman Sachs Philanthropy Fund (GS Donor Advised Philanthropy Fund)",
    "527082731": "Morgan Stanley Global Impact Funding Trust (MS GIFT)",
    "046010342": "Bank of America Charitable Gift Fund",
    "341747398": "American Endowment Foundation",
    "352129262": "Renaissance Charitable Foundation",
    "863177440": "Daffy Charitable Fund",
    "812771871": "Charityvest Inc",
    "237174183": "Jewish Communal Fund",
    "593652538": "Raymond James Charitable Endowment Fund",
    "141782466": "Ayco Charitable Foundation",
    "311663020": "U.S. Charitable Gift Trust",
    "262048480": "ImpactAssets",
}

DAFRC_METRICS = (
    ("number_of_daf_accounts", "daf_accounts_eoy", "accounts", "source_number_of_accounts"),
    ("total_daf_contributions", "daf_contributions", "USD", "source_total_daf_contributions"),
    ("total_daf_grants", "daf_grants", "USD", "source_total_daf_grants"),
    ("eoy_daf_assets", "daf_assets_eoy", "USD", "source_eoy_daf_assets"),
)

PROPUBLICA_METRICS = (
    ("totcntrbgfts", "form990_total_contributions_gifts_grants", "USD"),
    ("totrevenue", "form990_total_revenue", "USD"),
    ("totfuncexpns", "form990_total_functional_expenses", "USD"),
    ("totassetsend", "form990_total_assets_eoy", "USD"),
)

SPONSOR_FIELDS = (
    "sponsor", "ein", "fiscal_year", "period_end", "period_basis", "metric", "value",
    "unit", "value_qualifier", "data_source_type", "value_provenance", "source_url",
    "retrieved", "notes",
)

# ---------------------------------------------------------------------------
# Curated sponsor self-reports (never invented; blank = not published).
# value_qualifier: exact | rounded | lower_bound | approximate
# ---------------------------------------------------------------------------
_FID = "https://www.fidelitycharitable.org/insights/2026-giving-report.html"
_D360 = "https://www.dafgiving360.org/press-release/fiscal-year-2026-results"
_VAN = "https://www.vanguardcharitable.org/2025annualreport"
_VAN_PR = "https://thenonprofittimes.com/npt_articles/vanguard-daf-granted-3-9-billion-for-2025/"
_NPT_AR = "https://www.nptrust.org/annual-reports/npt-annual-report/"
_NPT_PR = "https://thenonprofittimes.com/?p=215695"
_DAFFY25 = "https://daffy.org/resources/year-in-review-2025"
_DAFFY26 = "https://pulse2.com/daffy-surpasses-2-billion-in-charitable-assets/"
_CV = ("https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-"
       "charitable-giving-more-than-doubling-contributions-and-grants/")
_SVCF = ("https://www.svcf.org/about/news-media/press-releases/silicon-valley-community-foundation-"
         "granted-276-million-to-nonprofits-in-san-mateo-and-santa-clara-counties-in-2025")
_RCF990 = "https://renaissancecharitable.org/wp-content/uploads/2026/01/Form-990-Public-Disclosure-Copy-2024-RCF.pdf"
_GSPF = "https://www.causeiq.com/organizations/goldman-sachs-philanthropy-fund,311774905/"

SELF_REPORTS: Sequence[tuple] = (
    # sponsor, ein, FY, period_end, basis, metric, value, unit, qualifier, url, notes
    ("Fidelity Charitable", "110303001", 2025, "2025-12-31", "calendar_year_self_report", "grants_paid", 18251649877, "USD", "exact", _FID, "2026 Giving Report; page also shows an unexplained $7,236,358,731 widget value (ignored); period labelled 'In 2025'"),
    ("Fidelity Charitable", "110303001", 2025, "2025-12-31", "calendar_year_self_report", "grant_count", 3000000, "grants", "rounded", _FID, "Shown as '3M' grant volume; rounded"),
    ("Fidelity Charitable", "110303001", 2025, "2025-12-31", "calendar_year_self_report", "donors", 395515, "donors", "exact", _FID, "Donors excluding third-party contributors; NOT Giving Account count"),
    ("Fidelity Charitable", "110303001", 2025, "2025-12-31", "calendar_year_self_report", "charities_supported", 226823, "organizations", "exact", _FID, ""),
    ("DAFgiving360", "311640316", 2026, "2026-06-30", "fiscal_year_self_report", "grants_paid", 10000000000, "USD", "lower_bound", _D360, "'More than $10 billion', +22% YoY per press release (2026-07-28); homepage cites $10.85b - not reconciled"),
    ("DAFgiving360", "311640316", 2026, "2026-06-30", "fiscal_year_self_report", "grant_count", 1600000, "grants", "lower_bound", _D360, "'More than 1.6 million grants', >4,300/day, +21% YoY"),
    ("DAFgiving360", "311640316", 2026, "2026-06-30", "fiscal_year_self_report", "median_grant", 500, "USD", "exact", _D360, "Self-reported median grant"),
    ("DAFgiving360", "311640316", 2026, "2026-06-30", "fiscal_year_self_report", "charities_supported", 170000, "organizations", "lower_bound", _D360, "'More than 170,000 charities'"),
    ("Vanguard Charitable", "232888152", 2025, "2025-12-31", "calendar_year_self_report", "grants_paid", 3960000000, "USD", "rounded", _VAN, "Reused from data/expanded-sponsor-activity-benchmarks-2026.csv (U14); press coverage rounds to $3.9b, +27% vs 2024"),
    ("Vanguard Charitable", "232888152", 2025, "2025-12-31", "calendar_year_self_report", "grant_count", 267838, "grants", "exact", _VAN, "Reused from expanded-sponsor-activity-benchmarks-2026.csv (U14)"),
    ("Vanguard Charitable", "232888152", 2025, "2025-12-31", "calendar_year_self_report", "charities_supported", 67000, "organizations", "approximate", _VAN_PR, "'Nearly 67,000 nonprofits'"),
    ("Vanguard Charitable", "232888152", 2025, "2025-06-30", "fiscal_year_self_report", "grants_paid", 3500000000, "USD", "lower_bound", "https://www.mychesco.com/a/news/business/vanguard-charitable-donors-grant-record-3-5-billion-in-fiscal-2025/", "FY July 2024-June 2025 'more than $3.5 billion' (+14%); different period from CY2025 row"),
    ("National Philanthropic Trust", "237825575", 2025, "2025-06-30", "fiscal_year_self_report", "grants_paid", 6440000000, "USD", "rounded", _NPT_AR, "Reused from expanded-sponsor-activity-benchmarks-2026.csv (U02, annual report). CONFLICT: NPT press release reports $6.61b to 48,000+ charities (+20%) for same FY - definitions not reconciled"),
    ("National Philanthropic Trust", "237825575", 2025, "2025-06-30", "fiscal_year_self_report", "grants_paid_press_release", 6610000000, "USD", "rounded", _NPT_PR, "Press-release figure; conflicts with $6.44b annual report figure above"),
    ("National Philanthropic Trust", "237825575", 2025, "2025-06-30", "fiscal_year_self_report", "grant_count", 159543, "grants", "exact", _NPT_AR, "Reused (U02)"),
    ("National Philanthropic Trust", "237825575", 2025, "2025-06-30", "fiscal_year_self_report", "daf_accounts_eoy", 20561, "accounts", "exact", _NPT_AR, "Reused (U02); median account ~$79,700 vs mean ~$2.7m (market-demand M30/M31)"),
    ("Daffy Charitable Fund", "863177440", 2025, "2025-12-31", "calendar_year_self_report", "daf_contributions", 470000000, "USD", "lower_bound", _DAFFY25, "Unaudited; 'more than $470 million', ~2.2x prior year"),
    ("Daffy Charitable Fund", "863177440", 2025, "2025-12-31", "calendar_year_self_report", "grants_paid", 125000000, "USD", "lower_bound", _DAFFY25, "Unaudited; 'more than $125 million', 3.2x YoY"),
    ("Daffy Charitable Fund", "863177440", 2025, "2025-12-31", "calendar_year_self_report", "daf_assets_eoy", 720000000, "USD", "lower_bound", _DAFFY25, "Unaudited; 'above $720 million'"),
    ("Daffy Charitable Fund", "863177440", 2025, "2025-12-31", "calendar_year_self_report", "daf_accounts_eoy", 15700, "accounts", "lower_bound", _DAFFY25, "'over 15,700 unique DAF accounts'"),
    ("Daffy Charitable Fund", "863177440", 2026, "2026-10-11", "point_in_time_self_report", "daf_assets", 2000000000, "USD", "lower_bound", _DAFFY26, "'surpassed $2 billion' (Oct 2026 announcement, via secondary outlet); YTD grants >$350m, Jan-Sep contributions >$800m"),
    ("Charityvest Inc", "812771871", 2025, "2025-12-31", "calendar_year_self_report", "daf_contributions", 265000000, "USD", "rounded", _CV, "Reused (U43); self-reported, published by Foundation Source"),
    ("Charityvest Inc", "812771871", 2025, "2025-12-31", "calendar_year_self_report", "grants_paid", 119200000, "USD", "rounded", _CV, "Reused (U43)"),
    ("Charityvest Inc", "812771871", 2025, "2025-12-31", "calendar_year_self_report", "grant_count", 48744, "grants", "exact", _CV, "Reused (U43)"),
    ("Charityvest Inc", "812771871", 2025, "2025-12-31", "calendar_year_self_report", "daf_assets_eoy", 224600000, "USD", "rounded", _CV, "Reused (U43); 'assets under management'"),
    ("Silicon Valley Community Foundation", "205205488", 2025, "2025-12-31", "calendar_year_self_report", "grants_paid_all_fund_types", 2100000000, "USD", "approximate", _SVCF, "Whole-sponsor grants, NOT DAF-only (U41)"),
    ("Renaissance Charitable Foundation", "352129262", 2024, "2024-12-31", "form990_schedule_d_sponsor_copy", "daf_accounts_eoy", 25824, "accounts", "exact", _RCF990, "From repo rcf-ren-audited-admin-payments-2020-2024.csv; DAFRC dataset IMPUTES 22,366 for FY2024"),
    ("Goldman Sachs Philanthropy Fund", "311774905", 2023, "2023-12-31", "form990_narrative_via_aggregator", "grant_count", 24800, "grants", "approximate", _GSPF, "'approximately 24,800 grants totaling approximately $2,135,242,000' (CauseIQ summary of 2023 Form 990; not verified against PDF)"),
    ("Goldman Sachs Philanthropy Fund", "311774905", 2023, "2023-12-31", "form990_narrative_via_aggregator", "grants_paid", 2135242000, "USD", "approximate", _GSPF, "See grant_count row"),
)


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------
def col_index(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref).group(0)
    return reduce(lambda acc, ch: acc * 26 + (ord(ch) - 64), letters, 0) - 1


def parse_shared_strings(xml_bytes: bytes) -> tuple:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ET.fromstring(xml_bytes)
    return tuple("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t"))
                 for si in root.findall("m:si", ns))


def cell_value(cell: ET.Element, shared: tuple, ns: str):
    kind = cell.get("t")
    v = cell.find(f"{{{ns}}}v")
    if kind == "inlineStr":
        return "".join(t.text or "" for t in cell.iter(f"{{{ns}}}t"))
    if v is None or v.text is None:
        return None
    if kind == "s":
        return shared[int(v.text)]
    if kind in ("str", "b"):
        return v.text
    num = float(v.text)
    return int(num) if num.is_integer() else num


def parse_sheet(xml_bytes: bytes, shared: tuple) -> tuple:
    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    root = ET.fromstring(xml_bytes)

    def row_values(row: ET.Element) -> tuple:
        cells = {col_index(c.get("r")): cell_value(c, shared, ns) for c in row.findall(f"{{{ns}}}c")}
        width = max(cells) + 1 if cells else 0
        return tuple(cells.get(i) for i in range(width))

    return tuple(row_values(r) for r in root.iter(f"{{{ns}}}row"))


def read_xlsx_first_sheet(xlsx_bytes: bytes) -> tuple:
    with zipfile.ZipFile(io.BytesIO(xlsx_bytes)) as zf:
        shared = parse_shared_strings(zf.read("xl/sharedStrings.xml"))
        return parse_sheet(zf.read("xl/worksheets/sheet1.xml"), shared)


def rows_to_dicts(rows: tuple) -> tuple:
    header = rows[0]
    return tuple({h: (r[i] if i < len(r) else None) for i, h in enumerate(header)} for r in rows[1:])


def normalise_ein(ein) -> str:
    return str(ein).strip().zfill(9) if ein not in (None, "") else ""


def dafrc_record(r: Mapping) -> dict:
    return {**{k: ("" if v is None else v) for k, v in r.items()},
            "ein": normalise_ein(r.get("ein")),
            "dataset_edition": "DAFRC Annual DAF Report 2025 - Updated Analysis (Spring 2026)",
            "source_url": DAFRC_DATASET_URL}


def dafrc_sponsor_rows(records: Iterable[Mapping], names: Mapping[str, str]) -> tuple:
    def to_rows(r):
        return tuple({
            "sponsor": names[r["ein"]], "ein": r["ein"], "fiscal_year": r["fiscal_year_end"],
            "period_end": r["end_of_tax_period"], "period_basis": "form990_tax_year_DAFRC_label",
            "metric": metric, "value": r[field], "unit": unit,
            "value_qualifier": "exact" if r[field] != "" else "missing",
            "data_source_type": "dafrc_schedule_d_dataset", "value_provenance": r[src],
            "source_url": DAFRC_DATASET_URL, "retrieved": RETRIEVED,
            "notes": "DAF-only Schedule D Part I value; 'Imputed' = DAFRC estimate, not filed"
                     + ("; period_end field lags fiscal_year label (stale/imputed row)"
                        if str(r["end_of_tax_period"])[:4] not in ("", str(r["fiscal_year_end"])) else ""),
        } for field, metric, unit, src in DAFRC_METRICS)
    return tuple(row for r in records if r["ein"] in names for row in to_rows(r))


def propublica_rows(ein: str, payload: Mapping, name: str, min_year: int = 2018) -> tuple:
    filings = payload.get("filings_with_data", []) or []

    def to_rows(f):
        prd = str(f.get("tax_prd", ""))
        period_end = f"{prd[:4]}-{prd[4:6]}" if len(prd) == 6 else ""
        return tuple({
            "sponsor": name, "ein": ein, "fiscal_year": prd[:4], "period_end": period_end,
            "period_basis": "form990_tax_period_end_month", "metric": metric,
            "value": f.get(field, ""), "unit": unit, "value_qualifier": "exact",
            "data_source_type": "propublica_form990_extract",
            "value_provenance": f"IRS e-file via ProPublica (formtype {f.get('formtype')})",
            "source_url": PROPUBLICA_ORG.format(ein=ein), "retrieved": RETRIEVED,
            "notes": "Whole-organisation Form 990 total (includes non-DAF funds); API: "
                     + PROPUBLICA_API.format(ein=ein),
        } for field, metric, unit in PROPUBLICA_METRICS)
    return tuple(row for f in filings if int(str(f.get("tax_prd", "0"))[:4] or 0) >= min_year
                 for row in to_rows(f))


def self_report_rows(reports: Sequence[tuple]) -> tuple:
    return tuple({
        "sponsor": s, "ein": e, "fiscal_year": fy, "period_end": pe, "period_basis": basis,
        "metric": m, "value": v, "unit": u, "value_qualifier": q,
        "data_source_type": "sponsor_self_report" if "990" not in basis else "form990_other",
        "value_provenance": "self-reported" if "990" not in basis else "Form 990 / narrative",
        "source_url": url, "retrieved": RETRIEVED, "notes": n,
    } for (s, e, fy, pe, basis, m, v, u, q, url, n) in reports)


def to_csv(rows: Sequence[Mapping], fields: Sequence[str]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(fields), quoting=csv.QUOTE_ALL, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# I/O edges
# ---------------------------------------------------------------------------
def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "daf-research-script/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def load_propublica(ein: str, cache_dir: str | None) -> Mapping:
    path = os.path.join(cache_dir, f"{ein}.json") if cache_dir else None
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return json.loads(fetch_bytes(PROPUBLICA_API.format(ein=ein)))


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dafrc-xlsx")
    ap.add_argument("--propublica-cache")
    ap.add_argument("--out-dir", default=os.path.join(root, "data", "mission-2026-11-14"))
    args = ap.parse_args()

    xlsx = (open(args.dafrc_xlsx, "rb").read() if args.dafrc_xlsx else fetch_bytes(DAFRC_DATASET_URL))
    records = tuple(map(dafrc_record, rows_to_dicts(read_xlsx_first_sheet(xlsx))))
    dafrc_fields = tuple(records[0].keys())

    pp_rows = tuple(row for ein, name in NAMED_SPONSORS.items()
                    for row in propublica_rows(ein, load_propublica(ein, args.propublica_cache), name))
    sponsor_rows = (dafrc_sponsor_rows(records, NAMED_SPONSORS) + pp_rows + self_report_rows(SELF_REPORTS))

    os.makedirs(args.out_dir, exist_ok=True)
    outputs = {
        "dafrc-sponsor-schedule-d-fy2019-2024.csv": to_csv(records, dafrc_fields),
        "sponsor-level-metrics.csv": to_csv(sponsor_rows, SPONSOR_FIELDS),
    }
    for fname, text in outputs.items():
        with open(os.path.join(args.out_dir, fname), "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
        print(f"wrote {fname}: {text.count(chr(10)) - 1} rows")


if __name__ == "__main__":
    main()
