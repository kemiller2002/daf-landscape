#!/usr/bin/env python3
"""Queue items P-B40N14-03 (realised volumes of non-cash intake vendors) and P-B38C-03 (DAFpay Network classification).

Stdlib only, functional style: pure extract/transform functions, I/O at the edges.

P-B40N14-03  Reads every indexed Form 990/990-EZ (tax years 2021+) of the charities affiliated with nonprofit-side
             non-cash intake vendors and measures what they actually filed:
               * FreeWill Impact Fund (EIN 86-1218871), the receiving charity of FreeWill's Crypto for Charity;
               * DonateStock Charitable Inc (EIN 87-1569770), the receiving charity of DonateStock / GivingIQ;
               * GVNGorg (EIN 81-2446261), DonateStock's 2021 stock partner and Engiven's crypto partner;
               * Giving Block Foundation (EIN 92-3363254), The Giving Block's charity (IRS EO BMF only; no return yet).
             Per return: Part VIII contributions (1h) and non-cash (1g), Part IX grants and fees, Part IV line 6,
             Schedule D Part I, Schedule M categories (crypto vs securities, gift counts, Forms 8283), Form 8282
             count, Schedule I lines (recipient counts, concentration, grants to GVNG and to DAFRC-listed sponsors),
             Part VII-B contractors and Schedule O text. Vendor claims ("over 55,000 nonprofits", "thousands of
             organizations", "10,000+", "approximately 2,400 charities") are tested against filed gift counts.
             DAFRC panel values are compared with the filed lines (the DonateStock FY2023/FY2024 "zero" rows).
             Shift4: quotes on The Giving Block are verified against cached text of its 10-K/10-Q PDFs and press
             releases served by investors.shift4.com (sec.gov is not used), and all earnings releases are scanned.
P-B38C-03    DAFpay Network Inc (EIN 93-1372175) TY2024 and TY2025, with FreeWill Impact Fund and DonateStock as
             comparators, against the repo's classification rules: (R1) DAFRC selection = Schedule D Part I filed
             with DAF assets >= $1; (R2) Part IV line 6; (R3) DAFRC 'Donation Processor' type membership; (R4) the
             filer's own DAF wording; (R5) whether receipts are grants from DAF sponsors (double-count test).

Sources
  * IRS TEOS index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (local copies, --irs-dir, repeatable)
  * IRS EO BMF extracts eo1..eo4.csv (same dirs)
  * 990 XML, GivingTuesday mirror https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
  * 2026 filings not mirrored: TEOS zip range read (mission_batch35_screens.teos_fetch)
  * data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv and dafrc-corrected-market-totals.csv
  * Cached first-party pages/PDF text for quote checks (--web-dir), Shift4 earnings releases (--releases-dir)

Usage
  python3 -I scripts/mission_noncash_vendors.py . --irs-dir DIR [--irs-dir DIR2] --work-dir WORK \
          [--xml-dir DIR ...] [--web-dir DIR] [--releases-dir DIR] [--fetch]
Writes data/mission-2026-11-14/noncash-vendor-volumes-2026-11-20.csv and prints a JSON summary to stdout.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

UA = {"User-Agent": "research-script/1.0"}
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
OUT_CSV = "data/mission-2026-11-14/noncash-vendor-volumes-2026-11-20.csv"
DAFRC_CSV = "data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv"
TOTALS_CSV = "data/mission-2026-11-14/dafrc-corrected-market-totals.csv"
MIN_TAX_YEAR = 2021

ENTITIES = {
    "861218871": ("FreeWill Impact Fund", "FreeWill / Crypto for Charity"),
    "871569770": ("DonateStock Charitable Inc", "GivingIQ (formerly DonateStock)"),
    "812446261": ("GVNGorg", "GVNG (DonateStock stock partner 2021; Engiven crypto partner)"),
    "931372175": ("DAFpay Network Inc", "Chariot DAFpay"),
    "923363254": ("Giving Block Foundation", "The Giving Block (Shift4)"),
}
FIF, DS, GVNG, DPN, TGBF = "861218871", "871569770", "812446261", "931372175", "923363254"

COLUMNS = ("record_type", "entity", "ein", "tax_year", "tax_period_end", "object_id", "selected", "item", "category",
           "count", "amount_usd", "amount2_usd", "ratio", "text", "source_url")

# Vendor claims and the cached page each is verified against (web-dir file, URL, quote, numeric reading).
CLAIMS = (
    {"vendor": "FreeWill / Crypto for Charity", "ein": FIF, "file": "freewill_crypto.html",
     "url": "https://www.freewill.com/learn/how-to-donate-crypto-to-charity",
     "quote": "select your crypto and the nonprofit you’d like to support from the over 55,000 nonprofits and cause funds that use our tool",
     "claim_n": 55000, "reading": "55,000 = organisations able to receive; test = distinct gifts routed via FreeWill Impact Fund"},
    {"vendor": "GivingIQ (formerly DonateStock)", "ein": DS, "file": "givingiq_about.html", "url": "https://givingiq.com/about",
     "quote": "we will help thousands of organizations impact millions of lives",
     "claim_n": 2000, "reading": "'thousands' read as at least 2,000; test = gifts and Schedule I recipients at DonateStock Charitable"},
    {"vendor": "GivingIQ (formerly DonateStock)", "ein": DS, "file": "givingiq_home.html", "url": "https://givingiq.com/",
     "quote": "we're helping thousands of nonprofits impact millions of lives",
     "claim_n": 2000, "reading": "same claim on the home page"},
    {"vendor": "Engiven", "ein": GVNG, "file": "engiven_home.html", "url": "https://engiven.com/",
     "quote": "Serving 10,000+ World-Changing Organizations",
     "claim_n": 10000, "reading": "no affiliated charity; the only 990 touchpoint is crypto partner GVNGorg"},
    {"vendor": "Engiven", "ein": GVNG, "file": "engiven_home.html", "url": "https://engiven.com/",
     "quote": "1000+ Engiven customers",
     "claim_n": 1000, "reading": "conflicting count on the same page"},
    {"vendor": "Engiven", "ein": GVNG, "file": "engiven_nonprofits.html", "url": "https://engiven.com/nonprofits",
     "quote": "Our partnership with Engiven makes donating crypto seamless for GVNG users",
     "claim_n": None, "reading": "GVNG partnership quote (live)"},
    {"vendor": "The Giving Block (Shift4)", "ein": TGBF, "file": "shift4_0001794669-26-000010.txt",
     "url": "https://investors.shift4.com/sec-filings/all-sec-filings/content/0001794669-26-000010/0001794669-26-000010.pdf",
     "quote": "allows donors to easily gift a variety of cryptocurrencies to approximately 2,400 charities",
     "claim_n": 2400, "reading": "Shift4 FY2025 10-K (IR-site PDF); no affiliated-charity 990 filed yet"},
    {"vendor": "The Giving Block (Shift4)", "ein": TGBF, "file": "tgb_annual_report.html", "url": "https://thegivingblock.com/annual-report/",
     "quote": "In 2025, we processed over $100 million worth of cryptocurrency donations on behalf of our thousands of nonprofit clients",
     "claim_n": None, "reading": "self-reported 2025 crypto volume"},
    {"vendor": "The Giving Block (Shift4)", "ein": TGBF, "file": "tgb_annual_report.html", "url": "https://thegivingblock.com/annual-report/",
     "quote": "Crypto alone saw an average gift of $11,019 across 22,343 donations",
     "claim_n": None, "reading": "count x average checked against the $100m headline"},
    {"vendor": "The Giving Block (Shift4)", "ein": TGBF, "file": "tgb_annual_report.html", "url": "https://thegivingblock.com/annual-report/",
     "quote": "One in five nonprofits on The Giving Block raised over $100,000 in crypto in 2025",
     "claim_n": None, "reading": "implied floor with ~2,400 charities"},
    {"vendor": "GVNG", "ein": GVNG, "file": "gvng_home.html", "url": "https://gvng.org/",
     "quote": "GVNGorg: Empowering Change Through Fiscal Sponsorship",
     "claim_n": None, "reading": "current self-description (fiscal sponsor / corporate giving platform)"},
)

S4 = "https://investors.shift4.com/sec-filings/all-sec-filings/content/{a}/{a}.pdf"
SHIFT4_QUOTES = (
    ("FY2022 10-K", "0001794669-23-000006", "allows donors to easily gift a variety of cryptocurrencies to over 2,000 charities"),
    ("FY2022 10-K", "0001794669-23-000006", "alternative payment methods, including cryptocurrency donations, plus volume we route"),
    ("FY2022 10-K", "0001794669-23-000006", "crypto settlement liabilities was $1.8 million as of December 31, 2022"),
    ("FY2023 10-K", "0001794669-24-000007", "alternative payment methods, including cryptocurrency and stock donations, plus volume we route"),
    ("FY2023 10-K", "0001794669-24-000007", "calculated as a multiple of revenue earned by The Giving Block from March 1, 2022 to February 28, 2023"),
    ("FY2023 10-K", "0001794669-24-000007", "The final earnout was $10.4 million, comprised of $2.8 million of cash and $7.6 million of equity"),
    ("FY2023 10-K", "0001794669-24-000007", "The acquisition of The Giving Block did not have a material impact on the Company's consolidated financial statements"),
    ("FY2024 10-K", "0001794669-25-000011", "crypto settlement liabilities was $5.7 million and $3.5 million as of December 31, 2024 and 2023, respectively"),
    ("FY2024 10-K", "0001794669-25-000011", "beginning in 2025, the Company will no longer recognize crypto settlement assets and liabilities"),
    ("FY2025 10-K", "0001794669-26-000010", "alternative payment methods, including cryptocurrency, stored value, gift cards and stock donations, plus volume we route"),
    ("Q3 2026 10-Q", "0001794669-26-000051", "alternative payment methods, including cryptocurrency, stored value, gift cards and stock donations, plus volume we route"),
)
CRYPTO_RE = re.compile(r"(?i)cr[yi]p?t|bitcoin|digital asset|virtual currenc")
DAF_WORDS_RE = re.compile(r"(?i)donor[ -]advised fund|sponsor to donor advised|fiscal sponsor")


# ----------------------------------------------------------------------------- small pure helpers
def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def num(x) -> float | None:
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def fmt(x) -> str:
    if x is None or x == "":
        return ""
    if isinstance(x, float):
        return str(int(x)) if x == int(x) else f"{x:.6f}".rstrip("0").rstrip(".")
    return str(x)


def ratio(a, b) -> float | None:
    return (a / b) if (a is not None and b) else None


def truthy(v: str) -> bool | None:
    return None if v in ("", None) else v.strip().upper() in ("X", "1", "TRUE", "YES")


def first_leaf(el, name: str) -> str:
    if el is None:
        return ""
    return next(((e.text or "").strip() for e in el.iter() if local(e.tag) == name and len(e) == 0), "")


def child(el, name: str):
    return None if el is None else next((c for c in el if local(c.tag) == name), None)


def leaves(el) -> dict:
    return {local(c.tag): (c.text or "").strip() for c in el.iter() if len(c) == 0}


def norm(t: str) -> str:
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    t = t.replace("–", "-").replace("—", "-").replace("\xa0", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


def page_text(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".txt"):
        return raw
    raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
    return html.unescape(re.sub(r"<[^>]+>", " ", raw))


def row(**kw) -> dict:
    return {c: fmt(kw.get(c, "")) for c in COLUMNS}


# ----------------------------------------------------------------------------- I/O edges
def load_index(irs_dirs: Sequence[str], eins: frozenset[str]) -> tuple[dict, ...]:
    def rows_of(path: str) -> Iterable[dict]:
        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            yield from (r for r in csv.DictReader(fh) if r.get("EIN") in eins and r.get("RETURN_TYPE") in ("990", "990EZ"))
    paths = [os.path.join(d, f) for d in irs_dirs for f in sorted(os.listdir(d)) if re.fullmatch(r"index_20\d\d\.csv", f)]
    by_oid = reduce(lambda acc, r: {**acc, r["OBJECT_ID"]: r}, (r for p in paths for r in rows_of(p)), {})
    return tuple(sorted(by_oid.values(), key=lambda r: (r["EIN"], r["TAX_PERIOD"], r["OBJECT_ID"])))


def load_bmf(irs_dirs: Sequence[str], eins: frozenset[str]) -> dict:
    def rows_of(path: str) -> Iterable[dict]:
        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            yield from (r for r in csv.DictReader(fh) if r.get("EIN") in eins)
    paths = [os.path.join(d, f) for d in irs_dirs for f in sorted(os.listdir(d)) if re.fullmatch(r"eo\d\.csv", f)]
    return reduce(lambda acc, r: {**acc, r["EIN"]: r}, (r for p in paths for r in rows_of(p)), {})


def find_cached(oid: str, dirs: Sequence[str]) -> str | None:
    hits = (os.path.join(d, n) for d in dirs for n in (f"{oid}.xml", f"{oid}_public.xml"))
    return next((p for p in hits if os.path.exists(p) and os.path.getsize(p) > 2000), None)


def fetch_mirror(oid: str, dest_dir: str) -> str | None:
    req = urllib.request.Request(XML_URL.format(oid=oid), headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
    except urllib.error.HTTPError:
        return None
    if b"<Return" not in data[:3000]:
        return None
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, f"{oid}.xml")
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def fetch_teos(oid: str, label: str, work_dir: str) -> str | None:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mission_batch35_screens import teos_fetch  # noqa: E402  (2026 TEOS zip range reader)
    meta = teos_fetch(oid, label, work_dir)
    return os.path.join(work_dir, "teos", f"{oid}_public.xml") if meta.get("status") == "ok" else None


def source_url(oid: str, work_dir: str) -> str:
    meta = os.path.join(work_dir, "teos", f"{oid}_public.xml.meta.json")
    if os.path.exists(meta):
        m = json.load(open(meta, encoding="utf-8"))
        return f"{m.get('zip', '')}#{m.get('member', '')}"
    return XML_URL.format(oid=oid)


def locate(filing: Mapping, dirs: Sequence[str], work_dir: str, do_fetch: bool) -> str | None:
    oid = filing["OBJECT_ID"]
    cached = find_cached(oid, (*dirs, os.path.join(work_dir, "xml"), os.path.join(work_dir, "teos")))
    if cached or not do_fetch:
        return cached
    return fetch_mirror(oid, os.path.join(work_dir, "xml")) or fetch_teos(oid, filing.get("XML_BATCH_ID", ""), work_dir)


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8") as fh:
        return tuple(csv.DictReader(fh))


# ----------------------------------------------------------------------------- XML extraction (pure on a parsed tree)
def schedule(root, name: str):
    return next((e for e in root.iter() if local(e.tag) == name), None)


def extract(path: str) -> dict:
    root = ET.parse(path).getroot()
    main = next((e for e in (schedule(root, "IRS990"), schedule(root, "IRS990EZ")) if e is not None), None)
    is_ez = main is not None and local(main.tag) == "IRS990EZ"
    sd, sm, si, sa, so = (schedule(root, n) for n in ("IRS990ScheduleD", "IRS990ScheduleM", "IRS990ScheduleI",
                                                      "IRS990ScheduleA", "IRS990ScheduleO"))
    rd = child(root, "ReturnData")
    m = (lambda n: num(first_leaf(main, n)))
    grants_l1 = num(first_leaf(child(main, "GrantsToDomesticOrgsGrp"), "TotalAmt")) if not is_ez else None
    sm_groups = tuple(
        {"group": local(g.tag), **leaves(g)} for g in (sm if sm is not None else ())
        if len(g) and any(local(c.tag) in ("ContributionCnt", "NoncashContributionsRptF990Amt") for c in g))
    si_rows = tuple(leaves(t) for t in (si.iter() if si is not None else ()) if local(t.tag) == "RecipientTable")
    other_exp = tuple(leaves(g) for g in (main.iter() if main is not None else ()) if local(g.tag) == "OtherExpensesGrp")
    contractors = tuple(leaves(g) for g in (main.iter() if main is not None else ()) if local(g.tag) == "ContractorCompensationGrp")
    texts = tuple((e.text or "").strip() for e in root.iter()
                  if local(e.tag) in ("MissionDesc", "ActivityOrMissionDesc", "Desc", "ExplanationTxt", "PrimaryExemptPurposeTxt")
                  and (e.text or "").strip())
    return {
        "tax_period_end": first_leaf(root, "TaxPeriodEndDt"), "return_ts": first_leaf(root, "ReturnTs"),
        "return_type": first_leaf(root, "ReturnTypeCd"), "amended": truthy(first_leaf(root, "AmendedReturnInd")) or False,
        "schedules": ";".join(local(c.tag) for c in (rd if rd is not None else ())),
        "contributions": m("TotalContributionsAmt") if not is_ez else m("ContributionsGiftsGrantsEtcAmt"),
        "noncash": m("NoncashContributionsAmt"),
        "program_service_revenue": m("TotalProgramServiceRevenueAmt") if not is_ez else m("ProgramServiceRevenueAmt"),
        "total_revenue": m("CYTotalRevenueAmt") if not is_ez else m("TotalRevenueAmt"),
        "grants_paid": (grants_l1 if grants_l1 is not None else m("CYGrantsAndSimilarPaidAmt")) if not is_ez else m("GrantsAndSimilarAmountsPaidAmt"),
        "total_expenses": m("CYTotalExpensesAmt") if not is_ez else m("TotalExpensesAmt"),
        "net_assets_eoy": m("NetAssetsOrFundBalancesEOYAmt"), "total_assets_eoy": m("TotalAssetsEOYAmt"),
        "mgmt_fees": num(first_leaf(child(main, "FeesForServicesManagementGrp"), "TotalAmt")) if not is_ez else None,
        "line6": first_leaf(main, "DonorAdvisedFundInd") or first_leaf(main, "DonorAdvisedFndsInd"),
        "form8282_cnt": m("Form8282FiledCnt"), "form8282_ind": first_leaf(main, "Form8282PropertyDisposedOfInd"),
        "fs_audited": first_leaf(main, "FSAuditedInd"),
        "sched_d_present": sd is not None,
        "sched_d": {k: num(first_leaf(sd, k)) for k in ("DonorAdvisedFundsHeldCnt", "DonorAdvisedFundsContriAmt",
                                                         "DonorAdvisedFundsGrantsAmt", "DonorAdvisedFundsVlEOYAmt")},
        "sched_m": sm_groups, "form8283_cnt": num(first_leaf(sm, "Form8283ReceivedCnt")),
        "sched_i": si_rows, "si_501c3_cnt": num(first_leaf(si, "Total501c3OrgCnt")),
        "sched_a": {k: num(first_leaf(sa, k)) for k in ("SubstantialContributorsTotAmt", "TotalSupportAmt", "PublicSupportCY170Pct")},
        "other_expenses": other_exp, "contractors": contractors, "texts": texts,
        "sched_o_present": so is not None,
    }


# ----------------------------------------------------------------------------- derived measures (pure)
def si_amount(r: Mapping) -> float:
    return (num(r.get("CashGrantAmt")) or 0.0) + (num(r.get("NonCashAssistanceAmt")) or 0.0)


def si_name(r: Mapping) -> str:
    return " ".join(v for k, v in r.items() if k.startswith("BusinessNameLine")).strip()


def sm_class(g: Mapping) -> str:
    if g["group"] == "OtherNonCashContriTableGrp" and CRYPTO_RE.search(g.get("Desc", "")):
        return "crypto"
    return {"SecuritiesPubliclyTradedGrp": "public_securities"}.get(g["group"], "other")


def sm_totals(sm: Sequence[Mapping]) -> dict:
    def add(acc, g):
        c = sm_class(g)
        return {**acc, c: (acc.get(c, (0.0, 0.0))[0] + (num(g.get("ContributionCnt")) or 0.0),
                           acc.get(c, (0.0, 0.0))[1] + (num(g.get("NoncashContributionsRptF990Amt")) or 0.0))}
    return reduce(add, sm, {})


def vendor_fee(ex: Mapping, ein: str) -> tuple[float | None, str]:
    """Fees flowing to the vendor or its processors, as filed."""
    if ein == DS:
        saas = sum(num(o.get("TotalAmt")) or 0.0 for o in ex["other_expenses"] if re.search(r"(?i)saas|donation service", o.get("Desc", "")))
        to_dsi = next((num(c.get("CompensationAmt")) for c in ex["contractors"] if re.search(r"(?i)donatestock", si_name(c) or c.get("BusinessNameLine1Txt", ""))), None)
        fee = to_dsi if to_dsi is not None else (ex["mgmt_fees"] or 0.0) + saas
        return fee, ("Part VII-B contractor DonateStock Inc" if to_dsi is not None else "Part IX management fees + SaaS/donation-service fees (paid to DonateStock Inc per Schedule O)")
    if ein == FIF:
        proc = sum(num(o.get("TotalAmt")) or 0.0 for o in ex["other_expenses"] if re.search(r"(?i)processing", o.get("Desc", "")))
        return proc, "Part IX other expenses 'PROCESSING FEES'"
    return None, ""


def return_records(f: Mapping, ex: Mapping, src: str, selected: bool, dafrc_eins: frozenset[str]) -> tuple[dict, ...]:
    ein, oid = f["EIN"], f["OBJECT_ID"]
    ty = ex["tax_period_end"][:4]
    b = {"entity": ENTITIES[ein][0], "ein": ein, "tax_year": ty, "tax_period_end": ex["tax_period_end"], "object_id": oid,
         "selected": 1 if selected else 0, "source_url": src}
    lines = (("contributions_viii_1h", ex["contributions"]), ("noncash_viii_1g", ex["noncash"]),
             ("program_service_revenue", ex["program_service_revenue"]), ("total_revenue", ex["total_revenue"]),
             ("grants_paid_ix_1", ex["grants_paid"]), ("total_expenses", ex["total_expenses"]),
             ("net_assets_eoy", ex["net_assets_eoy"]), ("total_assets_eoy", ex["total_assets_eoy"]),
             ("mgmt_fees_ix_11a", ex["mgmt_fees"]), ("form8282_filed_cnt", ex["form8282_cnt"]),
             ("form8283_received_cnt", ex["form8283_cnt"]),
             *((f"sched_d_{k}", v) for k, v in ex["sched_d"].items()),
             *((f"sched_a_{k}", v) for k, v in ex["sched_a"].items() if v is not None))
    flags = (("header", json.dumps({"return_ts": ex["return_ts"], "return_type": ex["return_type"], "amended": ex["amended"]})),
             ("part_iv_line6", ex["line6"]), ("sched_d_present", str(ex["sched_d_present"])),
             ("form8282_part_v_7c", ex["form8282_ind"]), ("fs_audited", ex["fs_audited"]), ("schedules_filed", ex["schedules"]))
    sm_rows = tuple(row(record_type="sched_m", **b, item=g["group"], category=sm_class(g), count=num(g.get("ContributionCnt")),
                        amount_usd=num(g.get("NoncashContributionsRptF990Amt")),
                        text=(g.get("Desc", "") + " | " + g.get("MethodOfDeterminingRevenuesTxt", "")).strip(" |"))
                    for g in ex["sched_m"])
    si = ex["sched_i"]
    si_rows = tuple(row(record_type="sched_i", **b, item="grant", category=("DAFRC sponsor" if r.get("RecipientEIN") in dafrc_eins else ""),
                        amount_usd=num(r.get("CashGrantAmt")), amount2_usd=num(r.get("NonCashAssistanceAmt")),
                        text=f"{si_name(r)} | EIN {r.get('RecipientEIN', '')}")
                    for r in si)
    texts = tuple(row(record_type="narrative", **b, item="daf_or_sponsor_wording", text=t[:600])
                  for t in dict.fromkeys(ex["texts"]) if DAF_WORDS_RE.search(t) or re.search(r"(?i)liquidat|organizations in our|DSI", t))
    contr = tuple(row(record_type="contractor", **b, item=c.get("ServicesDesc", ""), amount_usd=num(c.get("CompensationAmt")),
                      text=c.get("BusinessNameLine1Txt", "")) for c in ex["contractors"])
    oexp = tuple(row(record_type="other_expense", **b, item=o.get("Desc", ""), amount_usd=num(o.get("TotalAmt"))) for o in ex["other_expenses"])
    return (*(row(record_type="return_line", **b, item=k, amount_usd=v) for k, v in lines if v is not None),
            *(row(record_type="return_flag", **b, item=k, text=v) for k, v in flags),
            *sm_rows, *si_rows, *texts, *contr, *oexp)


def recipient_floor(ex: Mapping) -> tuple[int, float]:
    """Minimum number of grant recipients: listed Schedule I lines plus unlisted grants at most $5,000 each."""
    si_total = sum(si_amount(r) for r in ex["sched_i"])
    unlisted = max((ex["grants_paid"] or 0.0) - si_total, 0.0)
    return len(ex["sched_i"]) + int(-(-unlisted // 5000)), unlisted


def vendor_year(f: Mapping, ex: Mapping, src: str, dafrc_eins: frozenset[str]) -> tuple[dict, ...]:
    ein = f["EIN"]
    b = {"entity": ENTITIES[ein][0], "ein": ein, "tax_year": ex["tax_period_end"][:4], "tax_period_end": ex["tax_period_end"],
         "object_id": f["OBJECT_ID"], "selected": 1, "source_url": src}
    smt = sm_totals(ex["sched_m"])
    gifts = sum(v[0] for v in smt.values())
    sm_amt = sum(v[1] for v in smt.values())
    si = ex["sched_i"]
    si_total = sum(si_amount(r) for r in si)
    top = max((si_amount(r) for r in si), default=0.0)
    top_name = next((si_name(r) for r in si if si_amount(r) == top), "") if si else ""
    to_gvng = sum(si_amount(r) for r in si if r.get("RecipientEIN") == GVNG) if ein != GVNG else None
    lb, unlisted = recipient_floor(ex)
    to_dafrc = sum(si_amount(r) for r in si if r.get("RecipientEIN") in dafrc_eins)
    fee, fee_basis = vendor_fee(ex, ein)
    contrib = ex["contributions"]
    out = [
        ("intake_contributions", None, contrib, None, None, "Part VIII line 1h"),
        ("intake_noncash", None, ex["noncash"], contrib, ratio(ex["noncash"], contrib), "Part VIII 1g; ratio = share of 1h"),
        ("sched_m_total", gifts, sm_amt, ex["noncash"], ratio(sm_amt, ex["noncash"]), "Schedule M total; amount2 = Part VIII 1g; ratio = coverage"),
        *((f"sched_m_{k}", v[0], v[1], sm_amt, ratio(v[1], sm_amt), "Schedule M class; ratio = share of Schedule M value")
          for k, v in sorted(smt.items())),
        ("avg_gift", gifts, ratio(sm_amt, gifts), None, None, "Schedule M value / Schedule M contribution count"),
        ("sched_i_recipients_over_5k", len(si), si_total, ex["grants_paid"], ratio(si_total, ex["grants_paid"]),
         "Schedule I lines (>$5,000 per recipient); amount2 = Part IX line 1; ratio = Schedule I share of grants"),
        ("sched_i_top_recipient", None, top, si_total, ratio(top, si_total), f"largest Schedule I line: {top_name}"),
        ("recipient_count_bounds", lb, unlisted, gifts or None, None,
         f"lower bound = Schedule I lines + ceil(unlisted grants / $5,000) = {lb}; amount = Part IX line 1 minus Schedule I total; "
         f"amount2 = Schedule M gift count ({fmt(gifts) if gifts else 'n/a'}), an indicative ceiling (one designated charity per gift) that is "
         f"not binding where it falls below the floor (incomplete or placeholder Schedule M counts, or grants of prior-year gifts)"),
        ("grants_to_gvng", None, to_gvng, si_total, ratio(to_gvng, si_total), "Schedule I lines with recipient EIN 81-2446261"),
        ("grants_to_dafrc_sponsors", None, to_dafrc, si_total, ratio(to_dafrc, si_total), "Schedule I lines to EINs in the DAFRC panel"),
    ]
    if fee is not None:
        out.append(("vendor_or_processing_fee", None, fee, contrib, ratio(fee, contrib), fee_basis))
    return tuple(row(record_type="vendor_year", **b, item=i, count=c, amount_usd=a, amount2_usd=a2, ratio=r, text=t)
                 for i, c, a, a2, r, t in out if a is not None or c is not None)


def select_latest(filings: Sequence[Mapping], exs: Mapping) -> frozenset[str]:
    keyed = reduce(lambda acc, f: {**acc, (f["EIN"], exs[f["OBJECT_ID"]]["tax_period_end"]):
                                    max(acc.get((f["EIN"], exs[f["OBJECT_ID"]]["tax_period_end"]), f), f,
                                        key=lambda x: exs[x["OBJECT_ID"]]["return_ts"])},
                   filings, {})
    return frozenset(f["OBJECT_ID"] for f in keyed.values())


def dafrc_compare(dafrc_rows: Sequence[Mapping], exs_sel: Mapping, totals: Sequence[Mapping]) -> tuple[dict, ...]:
    tot = {(t["fiscal_year"], t["metric"]): num(t["corrected_value"]) for t in totals}
    def one(d: Mapping) -> tuple[dict, ...]:
        ex = exs_sel.get((d["ein"], d["fiscal_year_end"]))
        if ex is None:
            return ()
        b = {"record_type": "dafrc_compare", "entity": ENTITIES.get(d["ein"], (d["name"],))[0], "ein": d["ein"],
             "tax_year": d["fiscal_year_end"], "tax_period_end": d["end_of_tax_period"], "selected": 1, "source_url": d["source_url"]}
        sdv = ex["sched_d"]
        pairs = (("contributions", d["total_daf_contributions"], sdv["DonorAdvisedFundsContriAmt"], ex["contributions"], "daf_contributions"),
                 ("grants", d["total_daf_grants"], sdv["DonorAdvisedFundsGrantsAmt"], ex["grants_paid"], "daf_grants"),
                 ("eoy_assets", d["eoy_daf_assets"], sdv["DonorAdvisedFundsVlEOYAmt"], ex["total_assets_eoy"], "daf_assets_eoy"),
                 ("accounts", d["number_of_daf_accounts"], sdv["DonorAdvisedFundsHeldCnt"], None, "daf_accounts_eoy"))
        return tuple(row(**b, item=f"dafrc_{k}", category=f"DAFRC {d['type']}/{d['subtype']}; source {d['source_total_daf_contributions']}",
                         amount_usd=num(dv), amount2_usd=filed_proxy,
                         ratio=ratio(filed_proxy, tot.get((d["fiscal_year_end"], m))) if filed_proxy is not None else None,
                         text=(f"Schedule D Part I value as filed: {'blank' if sdval is None else fmt(sdval)}; amount2 = 990 proxy "
                               f"(Part VIII 1h / Part IX 1 / total assets); ratio = proxy / DAFRC corrected FY total {fmt(tot.get((d['fiscal_year_end'], m)))}"))
                     for k, dv, sdval, filed_proxy, m in pairs)
    return tuple(r for d in dafrc_rows for r in one(d))


def quote_check(web_dir: str | None, file: str, quote: str) -> bool | None:
    if not web_dir or not os.path.exists(os.path.join(web_dir, file)):
        return None
    return norm(quote) in norm(page_text(os.path.join(web_dir, file)))


def claim_tests(exs_sel: Mapping, web_dir: str | None) -> tuple[dict, ...]:
    def latest(ein: str):
        yrs = sorted(ty for (e, ty) in exs_sel if e == ein)
        return (yrs[-1], exs_sel[(ein, yrs[-1])]) if yrs else (None, None)
    def one(c: Mapping) -> dict:
        ty, ex = latest(c["ein"])
        found = quote_check(web_dir, c["file"], c["quote"])
        if ex is None or c["claim_n"] is None:
            return row(record_type="claim_test", entity=c["vendor"], ein=c["ein"], item="claim", count=c["claim_n"],
                       text=f"{c['quote']} | {c['reading']} | quote_found={found}", source_url=c["url"])
        smt = sm_totals(ex["sched_m"])
        gifts = sum(v[0] for v in smt.values())
        crypto_gifts = smt.get("crypto", (0.0, 0.0))[0]
        test_n = crypto_gifts if c["ein"] == FIF and crypto_gifts else gifts
        basis = "crypto gifts (Crypto for Charity routes every crypto gift through the fund)" if c["ein"] == FIF and crypto_gifts else "all Schedule M gifts"
        lb, _ = recipient_floor(ex)
        return row(record_type="claim_test", entity=c["vendor"], ein=c["ein"], tax_year=ty, item="claim_vs_filed_gifts",
                   count=c["claim_n"], amount_usd=ex["contributions"], amount2_usd=test_n, ratio=ratio(test_n, c["claim_n"]),
                   text=(f"{c['quote']} | {c['reading']} | indicative ceiling on recipients via the charity = {fmt(test_n)} {basis}; "
                         f"Schedule I recipients >$5k = {len(ex['sched_i'])}; recipient floor (all grants) = {lb}; all Schedule M gifts = {fmt(gifts)}; filed $ per claimed org = {fmt(round(ex['contributions'] / c['claim_n'], 2))} | quote_found={found}"),
                   source_url=c["url"])
    return tuple(one(c) for c in CLAIMS)


def tgb_arithmetic(web_dir: str | None) -> tuple[dict, ...]:
    """Internal consistency of The Giving Block's 2025 report figures (all quoted in CLAIMS)."""
    implied = 22343 * 11019
    floor = 2400 / 5 * 100000
    ok = quote_check(web_dir, "tgb_annual_report.html", "Crypto alone saw an average gift of $11,019 across 22,343 donations")
    return (row(record_type="claim_test", entity="The Giving Block (Shift4)", ein=TGBF, tax_year="2025", item="count_x_average",
                count=22343, amount_usd=implied, amount2_usd=100000000, ratio=ratio(implied, 100000000),
                text=f"22,343 donations x $11,019 average = ${implied:,}; headline 'over $100 million' | quote_found={ok}",
                source_url="https://thegivingblock.com/annual-report/"),
            row(record_type="claim_test", entity="The Giving Block (Shift4)", ein=TGBF, tax_year="2025", item="one_in_five_floor",
                count=2400, amount_usd=floor, amount2_usd=100000000, ratio=ratio(floor, 100000000),
                text="'one in five' of ~2,400 charities (FY2025 10-K count) raising over $100,000 implies at least this much crypto",
                source_url="https://thegivingblock.com/annual-report/"))


def shift4_records(web_dir: str | None, releases_dir: str | None) -> tuple[dict, ...]:
    q = tuple(row(record_type="shift4_disclosure", entity="Shift4 Payments", item=label, text=f"{quote} | quote_found={quote_check(web_dir, f'shift4_{acc}.txt', quote)}",
                  source_url=S4.format(a=acc)) for label, acc, quote in SHIFT4_QUOTES)
    vol = ()
    p = os.path.join(web_dir or "", "shift4_0001794669-26-000010.txt")
    if web_dir and os.path.exists(p):
        mm = re.search(r"Volume \(in billions\)\s+\$\s+(\d+)\s+\$\s+(\d+)", page_text(p))
        if mm:
            v25, v24 = float(mm.group(1)) * 1e9, float(mm.group(2)) * 1e9
            vol = (row(record_type="shift4_disclosure", entity="Shift4 Payments", tax_year="2025", item="volume_fy2025_vs_tgb_crypto_claim",
                       amount_usd=v25, amount2_usd=1e8, ratio=ratio(1e8, v25),
                       text=f"FY2025 volume ${mm.group(1)}bn (FY2024 ${mm.group(2)}bn, 'Volume (in billions)' table); ratio = TGB self-reported >$100m crypto / volume",
                       source_url=S4.format(a="0001794669-26-000010")),)
    scan = ()
    if releases_dir and os.path.isdir(releases_dir):
        files = sorted(f for f in os.listdir(releases_dir) if re.search(r"announces-.*quarter.*results", f))
        hits = tuple((f, len(re.findall(r"(?i)giving block|stock donation|crypto", page_text(os.path.join(releases_dir, f))))) for f in files)
        scan = (row(record_type="shift4_disclosure", entity="Shift4 Payments", item="earnings_release_scan", count=len(files),
                    amount_usd=sum(h for _, h in hits),
                    text="earnings releases 2020-Q2..2026-Q3 on investors.shift4.com; amount = mentions of 'Giving Block'/'stock donation'/'crypto' | "
                         + "; ".join(f"{f.split('_', 1)[0]}:{h}" for f, h in hits),
                    source_url="https://investors.shift4.com/news-events/press-releases"),)
    return (*q, *vol, *scan)


def bmf_records(bmf: Mapping) -> tuple[dict, ...]:
    return tuple(row(record_type="bmf", entity=ENTITIES[e][0], ein=e, tax_year=r.get("TAX_PERIOD", "")[:4],
                     tax_period_end=r.get("TAX_PERIOD", ""), item="eo_bmf", amount_usd=num(r.get("REVENUE_AMT")),
                     amount2_usd=num(r.get("ASSET_AMT")),
                     text=f"ruling {r.get('RULING')}; foundation code {r.get('FOUNDATION')}; NTEE {r.get('NTEE_CD')}; income {r.get('INCOME_AMT')}; amount = REVENUE_AMT, amount2 = ASSET_AMT; ICO {r.get('ICO')}",
                     source_url="https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf")
                 for e, r in sorted(bmf.items()))


def classification(exs_sel: Mapping, srcs: Mapping, dafrc_by_ein: Mapping, totals: Sequence[Mapping]) -> tuple[dict, ...]:
    """P-B38C-03: apply the repo's rules to DPN and to the self-described DAF comparators."""
    tot = {(t["fiscal_year"], t["metric"]): num(t["corrected_value"]) for t in totals}
    def verdict(ein: str, ty: str, ex: Mapping) -> dict:
        sd = ex["sched_d"]
        r1 = ex["sched_d_present"] and (sd["DonorAdvisedFundsVlEOYAmt"] or 0) >= 1
        r2 = truthy(ex["line6"])
        d = dafrc_by_ein.get(ein, ())
        r3 = next((x["type"] for x in d if x["type"] == "Donation Processor"), "")
        in_dafrc = bool(d)
        r4 = any(DAF_WORDS_RE.search(t) for t in ex["texts"])
        r5 = ein == DPN  # receipts are grants from DAF sponsors (DPN website; Chariot help) -> double count if added
        bucket = ("sponsor totals (Schedule D values only)" if r1 and not r3 else
                  "processor series (Schedule D values; separate account series)" if r1 and r3 else
                  "neither: intermediary memo line (no Schedule D, no DAF dollars)")
        ref = tot.get(("2024", "daf_grants"))
        return row(record_type="dpn_classification", entity=ENTITIES[ein][0], ein=ein, tax_year=ty, tax_period_end=ex["tax_period_end"],
                   selected=1, item="classification", category=bucket, amount_usd=ex["contributions"], amount2_usd=ex["grants_paid"],
                   ratio=ratio(ex["contributions"], ref),
                   text=(f"R1 Sched D Part I with DAF assets>=1: {r1}; R2 Part IV line 6: {ex['line6'] or 'blank'}; "
                         f"R3 DAFRC Donation Processor: {bool(r3)}; in DAFRC panel FY2019-24: {in_dafrc}; R4 self-described DAF/fiscal sponsor wording: {r4}; "
                         f"R5 receipts are DAF-sponsor grants (double count if added): {r5}; ratio = contributions / DAFRC corrected FY2024 DAF grants {fmt(ref)}"),
                   source_url=srcs[(ein, ty)])
    keys = sorted(k for k in exs_sel if k[0] in (DPN, FIF, DS))
    return tuple(verdict(e, ty, exs_sel[(e, ty)]) for e, ty in keys)


# ----------------------------------------------------------------------------- main
def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--irs-dir", action="append", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--xml-dir", action="append", default=[])
    ap.add_argument("--web-dir")
    ap.add_argument("--releases-dir")
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    eins = frozenset(ENTITIES)
    filings = tuple(f for f in load_index(a.irs_dir, eins) if int(f["TAX_PERIOD"][:4]) >= MIN_TAX_YEAR)
    paths = {f["OBJECT_ID"]: locate(f, a.xml_dir, a.work_dir, a.fetch) for f in filings}
    missing = sorted(o for o, p in paths.items() if not p)
    found = tuple(f for f in filings if paths[f["OBJECT_ID"]])
    exs = {f["OBJECT_ID"]: extract(paths[f["OBJECT_ID"]]) for f in found}
    srcs = {o: source_url(o, a.work_dir) for o in exs}
    sel = select_latest(found, exs)
    dafrc_rows = read_csv(os.path.join(root, DAFRC_CSV))
    dafrc_eins = frozenset(r["ein"] for r in dafrc_rows)
    dafrc_by_ein = reduce(lambda acc, r: {**acc, r["ein"]: (*acc.get(r["ein"], ()), r)}, dafrc_rows, {})
    totals = read_csv(os.path.join(root, TOTALS_CSV))
    exs_sel = {(f["EIN"], exs[f["OBJECT_ID"]]["tax_period_end"][:4]): exs[f["OBJECT_ID"]] for f in found if f["OBJECT_ID"] in sel}
    srcs_sel = {(f["EIN"], exs[f["OBJECT_ID"]]["tax_period_end"][:4]): srcs[f["OBJECT_ID"]] for f in found if f["OBJECT_ID"] in sel}
    bmf = load_bmf(a.irs_dir, eins)
    records = (
        *(r for f in found for r in return_records(f, exs[f["OBJECT_ID"]], srcs[f["OBJECT_ID"]], f["OBJECT_ID"] in sel, dafrc_eins)),
        *(r for f in found if f["OBJECT_ID"] in sel and f["EIN"] in (FIF, DS, GVNG)
          for r in vendor_year(f, exs[f["OBJECT_ID"]], srcs[f["OBJECT_ID"]], dafrc_eins)),
        *dafrc_compare(tuple(d for d in dafrc_rows if d["ein"] in eins), exs_sel, totals),
        *claim_tests(exs_sel, a.web_dir), *tgb_arithmetic(a.web_dir),
        *shift4_records(a.web_dir, a.releases_dir), *bmf_records(bmf),
        *classification(exs_sel, srcs_sel, dafrc_by_ein, totals),
    )
    out = os.path.join(root, OUT_CSV)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(records)
    vy = {(r["ein"], r["tax_year"], r["item"]): r for r in records if r["record_type"] == "vendor_year"}
    summary = {
        "filings_indexed": len(filings), "filings_read": len(found), "selected": len(sel), "missing": missing,
        "rows": len(records), "by_type": reduce(lambda acc, r: {**acc, r["record_type"]: acc.get(r["record_type"], 0) + 1}, records, {}),
        "vendor_year": {f"{ENTITIES[e][0]} {ty}": {k: {"count": r["count"], "amount": r["amount_usd"], "ratio": r["ratio"]}
                                                    for (e2, ty2, k), r in vy.items() if e2 == e and ty2 == ty}
                        for (e, ty, _) in sorted(vy)},
        "claims": [(r["entity"], r["item"], r["count"], r["amount2_usd"], r["ratio"], r["text"].rsplit("quote_found=", 1)[-1])
                   for r in records if r["record_type"] == "claim_test"],
        "shift4": [(r["item"], r["count"], r["amount_usd"], r["ratio"], r["text"].rsplit("quote_found=", 1)[-1][:12])
                   for r in records if r["record_type"] == "shift4_disclosure"],
        "dafrc_compare": [(r["entity"], r["tax_year"], r["item"], r["amount_usd"], r["amount2_usd"], r["ratio"], r["text"][:60])
                          for r in records if r["record_type"] == "dafrc_compare"],
        "classification": [(r["entity"], r["tax_year"], r["category"], r["amount_usd"], r["amount2_usd"], r["ratio"], r["text"])
                           for r in records if r["record_type"] == "dpn_classification"],
        "bmf": [(r["entity"], r["tax_period_end"], r["amount_usd"], r["amount2_usd"], r["text"]) for r in records if r["record_type"] == "bmf"],
    }
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
