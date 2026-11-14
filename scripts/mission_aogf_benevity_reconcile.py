#!/usr/bin/env python3
"""P-PRC-01: reconcile AOGF's payments to Benevity with Benevity's published 2.99% Cause Support Fee.

American Online Giving Foundation (AOGF, EIN 81-0739440) is the US foundation behind Benevity's workplace-giving
platform. Its Form 990 lists Benevity, Inc. as its largest contractor (Part VII-B). This script reads, for FY3/2022 to
FY3/2025:
  - the AOGF rows of data/mission-2026-11-14/processor-vendor-economics-990.csv (Benevity, BlueSnap, PayPal, merchant
    fees, grants, contributions; already extracted from the 990 XML);
  - the four 990 XML returns themselves (Part VIII contributions / noncash / program-service revenue / investment
    income; Part IX lines 1, 3, 11a; Schedule D DAF counts; Schedule M presence; Schedule I recipient amounts;
    Schedule A five-year "administrative service fee" series);
and computes the effective Benevity rate on several bases plus the volume mixes that would reproduce it under the
published fee schedule (2.99% per donation, $500 cap per donation; the cap does not apply to matching transactions
or gifts of securities; client master agreements may set other rates).

No value is typed by hand except the published schedule parameters (FEE, CAP), which are cited in FEE_SOURCE.
Output: data/mission-2026-11-14/aogf-benevity-reconciliation.csv (long format)
Usage:  python3 scripts/mission_aogf_benevity_reconcile.py --xml-dir DIR [--fetch]
Stdlib only; functional style.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import urllib.request
from typing import Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
IN_CSV = os.path.join(DATA, "processor-vendor-economics-990.csv")
OUT_CSV = os.path.join(DATA, "aogf-benevity-reconciliation.csv")
EIN = "810739440"
FEE, CAP = 0.0299, 500.0
CARD_FEE = 0.0295  # AOGF merchant fee deducted from credit/debit card donations (same schedule, p.3)
FEE_SOURCE = ("Benevity Foundations Fees Schedule, last updated 2026-10-01, "
              "https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf (p.2)")
CAP_THRESHOLD = CAP / FEE  # donation size above which the $500 cap binds (~$16,722)


# ----------------------------------------------------------------------------- I/O edges
def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


def xml_text(xml_dir: str, url: str, fetch: bool) -> str:
    oid = re.search(r"(\d{18})_public\.xml", url).group(1)
    path = os.path.join(xml_dir, f"{oid}.xml")
    if not os.path.exists(path) and fetch:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-client"}), timeout=300) as r:
            raw = r.read()
        with open(path, "wb") as fh:
            fh.write(raw)
    with open(path, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


# ----------------------------------------------------------------------------- pure transforms
def first_num(text: str, tag: str):
    m = re.search(r"<(?:\w+:)?%s>\s*(-?[\d.]+)\s*<" % tag, text)
    return float(m.group(1)) if m else None


def grp_num(text: str, grp: str, tag: str = "TotalAmt"):
    m = re.search(r"<%s>(.*?)</%s>" % (grp, grp), text, re.S)
    return first_num(m.group(1), tag) if m else None


def schedule(text: str, name: str) -> str:
    m = re.search(r"<IRS990%s\b.*?</IRS990%s>" % (name, name), text, re.S)
    return m.group(0) if m else ""


def xml_facts(text: str) -> dict:
    si = schedule(text, "ScheduleI")
    rest = text.replace(si, "")
    amts = tuple(float(x) for x in re.findall(r"<CashGrantAmt>\s*([\d.]+)\s*<", si))
    admin_series = re.search(r"ADMINISTRATIVE SERVICE FEE - ([^<]+)<", rest)
    return {"contributions_total": first_num(rest, "TotalContributionsAmt"),
            "noncash_contributions": first_num(rest, "NoncashContributionsAmt"),
            "schedule_m_filed": 1.0 if schedule(rest, "ScheduleM") else 0.0,
            "program_service_revenue_admin_fee": first_num(rest, "TotalProgramServiceRevenueAmt"),
            "investment_income": grp_num(rest, "InvestmentIncomeGrp", "TotalRevenueColumnAmt"),
            "total_revenue": grp_num(rest, "TotalRevenueGrp", "TotalRevenueColumnAmt"),
            "grants_paid_part_i": first_num(rest, "CYGrantsAndSimilarPaidAmt"),
            "grants_domestic_l1": grp_num(rest, "GrantsToDomesticOrgsGrp"),
            "grants_foreign_l3": grp_num(rest, "ForeignGrantsGrp"),
            "fees_management_l11a": grp_num(rest, "FeesForServicesManagementGrp"),
            "daf_accounts": first_num(rest, "DonorAdvisedFundsHeldCnt"),
            "daf_contributions": first_num(rest, "DonorAdvisedFundsContriAmt"),
            "daf_grants": first_num(rest, "DonorAdvisedFundsGrantsAmt"),
            "sched_i_recipients": float(len(amts)),
            "sched_i_cash_total": sum(amts),
            "sched_i_cash_at_recipients_ge_cap_threshold": sum(a for a in amts if a >= CAP_THRESHOLD),
            "sched_i_recipients_ge_cap_threshold": float(sum(1 for a in amts if a >= CAP_THRESHOLD)),
            "_admin_series": admin_series.group(1).strip() if admin_series else ""}


def vendor_facts(rows: Sequence[Mapping], fy: str) -> dict:
    mine = tuple(r for r in rows if r["sponsor_ein"] == EIN and r["fiscal_year"] == fy)
    def amt(pred):
        v = tuple(float(r["amount_usd"]) for r in mine if pred(r))
        return sum(v) if v else None
    return {"benevity_payment": amt(lambda r: r["vendor_group"] == "Benevity"),
            "bluesnap_payment": amt(lambda r: r["vendor_group"] == "BlueSnap"),
            "paypal_payment": amt(lambda r: r["vendor_group"].startswith("PayPal")),
            "merchant_fees_part_ix": amt(lambda r: r["cost_line_type"] == "part_ix_line_24_other" and "MERCHANT" in r["payee_or_line"].upper()),
            "non_grant_expense": amt(lambda r: r["cost_line_type"] == "derived_non_grant_expense"),
            "_return_object_id": mine[0]["return_object_id"] if mine else "", "_xml_url": mine[0]["source_xml_url"] if mine else "",
            "_tax_period_end": mine[0]["tax_period_end"] if mine else ""}


def div(a, b):
    return a / b if a is not None and b else None


def derived(f: Mapping) -> dict:
    """Effective rates and the volume mixes that reproduce them under the published schedule.
    full_rate_equivalent_share = effective rate / 2.99%: share of volume that would have to bear the full fee if the
    rest bore none. min_share_capped_or_discounted = 1 - that share. Bound on capped volume from Schedule I: a donation
    above the cap threshold can only go to a recipient whose annual total is above the threshold, so domestic grant $
    at recipients >= threshold plus all foreign grants is an upper bound on capped-donation volume."""
    b, c, g, adm = f["benevity_payment"], f["contributions_total"], f["grants_paid_part_i"], f["program_service_revenue_admin_fee"]
    r_g, r_c = div(b, g), div(b, c)
    net_of_admin = (b - adm) if b is not None and adm is not None else None
    ub = div((f["sched_i_cash_at_recipients_ge_cap_threshold"] or 0) + (f["grants_foreign_l3"] or 0), g)
    return {"benevity_pct_of_grants": r_g, "benevity_pct_of_contributions": r_c,
            "benevity_pct_of_contributions_plus_admin_fee": div(b, (c or 0) + (adm or 0)),
            "benevity_less_admin_fee_revenue": net_of_admin,
            "benevity_less_admin_fee_pct_of_contributions": div(net_of_admin, c),
            "full_rate_equivalent_share_of_contributions": div(r_c, FEE),
            "min_share_capped_or_discounted_contributions": (1 - r_c / FEE) if r_c is not None else None,
            "full_rate_equivalent_share_if_admin_fee_funds_part": div(div(net_of_admin, c), FEE),
            "upper_bound_capped_volume_share_of_grants": ub,
            "merchant_fees_pct_of_grants": div(f["merchant_fees_part_ix"], g),
            "min_card_share_of_grants": div(div(f["merchant_fees_part_ix"], g), CARD_FEE),
            "benevity_less_admin_fee_and_investment_income": (b - adm - (f["investment_income"] or 0)) if b is not None and adm is not None else None,
            "admin_fee_pct_of_contributions": div(adm, c),
            "investment_income_pct_of_benevity": div(f["investment_income"], b),
            "noncash_pct_of_contributions": div(f["noncash_contributions"] or 0.0, c),
            "avg_contribution_per_daf_account": div(f["daf_contributions"], f["daf_accounts"])}


UNITS = {"pct": ("benevity_pct", "_pct_of", "_share", "noncash_pct"), "count": ("_accounts", "_recipients", "schedule_m_filed")}


def unit_of(k: str) -> str:
    if "cash" in k or k.endswith("_income") or "less_admin" in k and "pct" not in k:
        return "usd"
    if any(s in k for s in UNITS["count"]):
        return "count"
    if any(s in k for s in UNITS["pct"]):
        return "ratio"
    return "usd"


def long_rows(fy: str, f: Mapping) -> tuple[dict, ...]:
    src = f"990 XML {f['_return_object_id']} ({f['_xml_url']})"
    def basis(k):
        return ("processor-vendor-economics-990.csv (from 990 Part VII-B / Part IX)" if k in
                ("benevity_payment", "bluesnap_payment", "paypal_payment", "merchant_fees_part_ix", "non_grant_expense")
                else "computed" if k in DERIVED_KEYS else src)
    note = {"noncash_contributions": "tag absent in the return -> no noncash (securities) contributions reported",
            "full_rate_equivalent_share_of_contributions": f"Benevity / contributions / {FEE:.4f} ({FEE_SOURCE})",
            "min_share_capped_or_discounted_contributions": "1 - full-rate-equivalent share",
            "upper_bound_capped_volume_share_of_grants": f"(Sched I $ at recipients >= ${CAP_THRESHOLD:,.0f} + foreign grants) / grants",
            "min_card_share_of_grants": f"merchant fees / grants / {CARD_FEE} (processor share of the card fee <= {CARD_FEE}, so a lower bound)",
            "benevity_less_admin_fee_and_investment_income": "residual if both revenue lines funded the Benevity payment (not stated in the return)",
            "benevity_less_admin_fee_revenue": "only if the administrative service fee revenue funds part of the Benevity payment (not stated in the return)"}
    return tuple({"fiscal_year_end": f["_tax_period_end"], "fiscal_year": fy, "metric": k,
                  "value": (None if v is None else round(v, 6)), "unit": unit_of(k), "basis": basis(k),
                  "note": note.get(k, "")} for k, v in f.items() if not k.startswith("_"))


DERIVED_KEYS = tuple(derived({k: None for k in ("benevity_payment", "contributions_total", "grants_paid_part_i",
                                                 "program_service_revenue_admin_fee", "sched_i_cash_at_recipients_ge_cap_threshold",
                                                 "grants_foreign_l3", "merchant_fees_part_ix", "investment_income",
                                                 "noncash_contributions", "daf_contributions", "daf_accounts")}).keys())
# (derived() tolerates None inputs, so the key list is built from it once)


def series_rows(fy: str, f: Mapping) -> tuple[dict, ...]:
    """Schedule A five-year 'ADMINISTRATIVE SERVICE FEE - 2020 AMOUNT: $ x. ...' (tax years)."""
    pairs = re.findall(r"(\d{4}) AMOUNT:\s*\$\s*([\d,]+)", f["_admin_series"])
    return tuple({"fiscal_year_end": f["_tax_period_end"], "fiscal_year": fy, "metric": f"sched_a_admin_service_fee_tax_year_{y}",
                  "value": float(v.replace(",", "")), "unit": "usd",
                  "basis": f"990 XML {f['_return_object_id']} Schedule A support schedule", "note": "tax year = FYE March of the following year"}
                 for y, v in pairs)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    rows = read_csv(IN_CSV)
    years = sorted({r["fiscal_year"] for r in rows if r["sponsor_ein"] == EIN})
    facts = {fy: (lambda v: {**v, **xml_facts(xml_text(a.xml_dir, v["_xml_url"], a.fetch))})(vendor_facts(rows, fy)) for fy in years}
    facts = {fy: {**f, **derived(f)} for fy, f in facts.items()}
    out = tuple(r for fy in years for r in long_rows(fy, facts[fy])) + series_rows(years[-1], facts[years[-1]])
    out += ({"fiscal_year_end": "", "fiscal_year": "ALL", "metric": "published_cause_support_fee", "value": FEE, "unit": "ratio",
             "basis": FEE_SOURCE, "note": "per donation; may differ under a client's master agreement"},
            {"fiscal_year_end": "", "fiscal_year": "ALL", "metric": "published_cause_support_fee_cap", "value": CAP, "unit": "usd",
             "basis": FEE_SOURCE, "note": "per donation; the CAP does not apply to matching transactions or gifts of securities"},
            {"fiscal_year_end": "", "fiscal_year": "ALL", "metric": "cap_threshold_donation_size", "value": round(CAP_THRESHOLD, 2),
             "unit": "usd", "basis": "computed", "note": "500 / 0.0299"})
    cols = ("fiscal_year_end", "fiscal_year", "metric", "value", "unit", "basis", "note")
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    for fy in years:
        f = facts[fy]
        print(fy, " ".join(f"{k}={f[k]:.4f}" if isinstance(f[k], float) and abs(f[k]) < 10 else f"{k}={f[k]:,.0f}"
                           for k in ("benevity_payment", "contributions_total", "grants_paid_part_i",
                                     "program_service_revenue_admin_fee", "investment_income", "noncash_contributions",
                                     "benevity_pct_of_grants", "benevity_pct_of_contributions",
                                     "full_rate_equivalent_share_of_contributions", "full_rate_equivalent_share_if_admin_fee_funds_part",
                                     "upper_bound_capped_volume_share_of_grants", "avg_contribution_per_daf_account",
                                     "sched_i_recipients") if f.get(k) is not None))
    print(f"wrote {len(out)} rows -> {os.path.relpath(OUT_CSV, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
