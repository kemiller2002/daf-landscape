#!/usr/bin/env python3
"""Queue items P-B40N14-01 (Dechomai deep read) and P-B38C-01 (DAFpay Network fee booking).

Stdlib only, functional style: pure extract/transform functions, I/O at the edges.

P-B40N14-01  Dechomai Asset Trust (EIN 26-0724604) and Dechomai Foundation Inc (EIN 06-1676688), Form 990 for
             tax years 2021-2024. Each return is decomposed into Schedule M non-cash categories and counts, Schedule I
             recipients, Form 8282 indicators (Part V line 7c/7d plus any '8282' text), Part VII-B contractors,
             Schedule R related-organisation transactions and Part VIII/IX lines. Routing of complex-asset volume
             through Dechomai is measured two ways:
               (a) Dechomai's own Schedule I grants to the six national sponsor groups (DAFgiving360, Fidelity Charitable,
                   AEF, Goldman Sachs, Morgan Stanley GIFT, NPT), plus all DAFRC-listed sponsors as context;
               (b) the sponsors' own Schedule I grants to either Dechomai entity, read from every indexed sponsor
                   Form 990 with a tax period ending 2021-06 .. 2025-06 (Schedule B is redacted in public XML).
             Effective take = fees paid out of the two entities (Part VII-B Charitable Solutions LLC; Part IX
             management/other fees; all non-grant expenses) over external non-cash contributions, compared with the
             published "1-3% with minimum fee of $10,000".
P-B38C-01    DAFpay Network Inc (EIN 93-1372175): every indexed Form 990 (TY2024, TY2025). Parts VIII-IX, Schedule I,
             Schedule O, Part VII-B. Tests whether a 2.9% DAFpay fee shows as DPN revenue, as an expense named to
             Chariot Giving Inc, as an unnamed expense of about 2.9% of receipts, or nowhere.

Sources
  * IRS TEOS index https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (local copies in --irs-dir)
  * IRS e-file XML, GivingTuesday mirror https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OID}_public.xml
  * Fallback for 2026 filings: TEOS zip range read (mission_batch35_screens.teos_fetch)
  * DAFRC sponsor list data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv (sponsor classification by EIN)

Usage
  python3 scripts/mission_dechomai_dafpay.py . --irs-dir IRS_DIR --work-dir WORK [--xml-dir DIR ...] [--fetch]
Writes data/mission-2026-11-14/dechomai-dafpay-2026-11-19.csv and prints a JSON summary to stdout.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

OUT_NAME = "dechomai-dafpay-2026-11-19.csv"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
PP_URL = "https://projects.propublica.org/nonprofits/organizations/{ein}/{oid}/full"
UA = {"User-Agent": "research-script/1.0"}
INDEX_YEARS = tuple(range(2021, 2027))

DAT, DF, DPN = "260724604", "061676688", "931372175"
DECHOMAI = {DAT: "Dechomai Asset Trust", DF: "Dechomai Foundation Inc"}
DECHOMAI_YEARS = (2021, 2022, 2023, 2024)
SPONSOR_GROUPS = {
    "311640316": "DAFgiving360",
    "110303001": "Fidelity Charitable",
    "341747398": "AEF",
    "311774905": "Goldman Sachs",          # GS Donor Advised Philanthropy Fund for Wealth Management
    "113813663": "Goldman Sachs",          # The Goldman Sachs Charitable Gift Fund
    "527082731": "Morgan Stanley GIFT",
    "237825575": "NPT",
}
GROUP_NAME_RX = (
    ("DAFgiving360", re.compile(r"schwab|dafgiving|donor advised charitable giving", re.I)),
    ("Fidelity Charitable", re.compile(r"fidelity", re.I)),
    ("AEF", re.compile(r"american endowment", re.I)),
    ("Goldman Sachs", re.compile(r"goldman|\bGS\b", re.I)),
    ("Morgan Stanley GIFT", re.compile(r"morgan stanley", re.I)),
    ("NPT", re.compile(r"national philanthropic", re.I)),
)
SPONSOR_TAX_PERIODS = ("202106", "202506")            # inclusive range of TAX_PERIOD (yyyymm) read for sponsors
PUBLISHED_FEE = {"low": 0.01, "high": 0.03, "min_usd": 10000.0}
DAFPAY_RATE = 0.029
DAFPAY_BAND = 0.005                                   # +/- 0.5 pp counts as "about 2.9%"
CHARIOT_RX = re.compile(r"chariot", re.I)
FORM8282_RX = re.compile(r"8282")

SCHED_M_GROUPS = {
    "ArtWorksOfArtGrp": "Art - works of art", "ArtHistoricalTreasuresGrp": "Art - historical treasures",
    "ArtFractionalInterestGrp": "Art - fractional interests", "BooksAndPublicationsGrp": "Books and publications",
    "ClothingAndHouseholdGoodsGrp": "Clothing and household goods", "CarsAndOtherVehiclesGrp": "Cars and other vehicles",
    "BoatsAndPlanesGrp": "Boats and planes", "IntellectualPropertyGrp": "Intellectual property",
    "SecuritiesPubliclyTradedGrp": "Securities - publicly traded", "SecuritiesCloselyHeldStockGrp":
    "Securities - closely held stock", "SecurPrtnrshpTrustIntrstsGrp": "Securities - partnership, LLC, trust interests",
    "SecuritiesMiscellaneousGrp": "Securities - miscellaneous", "QualifiedContribHistStructGrp":
    "Qualified conservation - historic structures", "QualifiedContribOtherGrp": "Qualified conservation - other",
    "RealEstateResidentialGrp": "Real estate - residential", "RealEstateCommercialGrp": "Real estate - commercial",
    "RealEstateOtherGrp": "Real estate - other", "CollectiblesGrp": "Collectibles", "FoodInventoryGrp": "Food inventory",
    "DrugsAndMedicalSuppliesGrp": "Drugs and medical supplies", "TaxidermyGrp": "Taxidermy",
    "HistoricalArtifactsGrp": "Historical artifacts", "ScientificSpecimensGrp": "Scientific specimens",
    "ArcheologicalArtifactsGrp": "Archeological artifacts", "OtherNonCashContriTableGrp": "Other",
}
ASSET_CLASS = (("Securities - closely held", "private business interests"), ("Securities - partnership", "private business interests"),
               ("Securities - publicly", "public securities"), ("Securities - misc", "other securities"),
               ("Real estate", "real estate"), ("crypto", "cryptocurrency"))
PART_VIII = ("TotalContributionsAmt", "NoncashContributionsAmt", "ProgramServiceRevenueAmt", "CYProgramServiceRevenueAmt",
             "CYOtherRevenueAmt", "CYInvestmentIncomeAmt", "CYTotalRevenueAmt", "GrossReceiptsAmt")
PART_IX = ("FeesForServicesManagementGrp", "FeesForServicesLegalGrp", "FeesForServicesAccountingGrp",
           "FeesForServicesOtherGrp", "FeesForServicesInvstMgmntFeesGrp", "FeesForServicesLobbyingGrp",
           "FeesForSrvcProfFundraisingGrp", "InformationTechnologyGrp", "GrantsToDomesticOrgsGrp",
           "TotalFunctionalExpensesGrp")
FIELDS = ("record_type", "entity", "ein", "tax_year", "tax_period_end", "object_id", "selected", "item", "category",
          "count", "amount_usd", "amount2_usd", "ratio", "counterparty", "counterparty_ein", "sponsor_group", "text",
          "source_url")


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
        return str(int(x)) if x == int(x) else f"{x:.6g}"
    return str(x)


def ein9(x: str) -> str:
    d = re.sub(r"\D", "", x or "")
    return d.zfill(9) if d else ""


def ratio(a, b) -> float | None:
    return (a / b) if (a is not None and b) else None


def find(el, path: str):
    return el.find(path) if el is not None else None


def text(el, path: str) -> str:
    e = find(el, path)
    return (e.text or "").strip() if e is not None else ""


def leaf_texts(el) -> tuple[str, ...]:
    return tuple((e.text or "").strip() for e in el.iter() if len(e) == 0 and (e.text or "").strip())


def group_by(items: Iterable, key) -> dict:
    return reduce(lambda acc, x: {**acc, key(x): acc.get(key(x), ()) + (x,)}, items, {})


def total(rows: Iterable[Mapping], field: str = "amount_usd") -> float:
    return sum(num(r.get(field)) or 0.0 for r in rows)


def row(**kw) -> dict:
    return {f: fmt(kw.get(f, "")) for f in FIELDS}


# ----------------------------------------------------------------------------- index and fetch (I/O edge)
def load_index(irs_dir: str, eins: frozenset[str]) -> tuple[dict, ...]:
    def rows_of(path: str):
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("EIN", "").zfill(9) in eins:
                    yield {**r, "EIN": r["EIN"].zfill(9), "index_file": os.path.basename(path)}
    paths = tuple(p for p in (os.path.join(irs_dir, f"index_{y}.csv") for y in INDEX_YEARS) if os.path.exists(p))
    return tuple(r for p in paths for r in rows_of(p))


def find_cached(oid: str, dirs: Sequence[str]) -> str | None:
    names = (f"{oid}.xml", f"{oid}_public.xml")
    hits = (os.path.join(d, n) for d in dirs for n in names)
    return next((p for p in hits if os.path.exists(p) and os.path.getsize(p) > 2000), None)


def fetch_mirror(oid: str, dest_dir: str) -> str | None:
    path = os.path.join(dest_dir, f"{oid}.xml")
    req = urllib.request.Request(XML_URL.format(oid=oid), headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = r.read()
    except urllib.error.HTTPError:
        return None
    if not data.lstrip().startswith(b"<?xml") or b"<Return" not in data[:2000]:
        return None
    os.makedirs(dest_dir, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def fetch_teos(oid: str, label: str, work_dir: str) -> tuple[str | None, str]:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from mission_batch35_screens import teos_fetch  # noqa: E402  (2026 TEOS zip range reader)
    meta = teos_fetch(oid, label, work_dir)
    path = os.path.join(work_dir, "teos", f"{oid}_public.xml")
    return (path if meta.get("status") == "ok" else None), meta.get("zip", "")


def locate(filing: Mapping, dirs: Sequence[str], work_dir: str, do_fetch: bool) -> tuple[str | None, str]:
    oid = filing["OBJECT_ID"]
    cached = find_cached(oid, (*dirs, os.path.join(work_dir, "xml"), os.path.join(work_dir, "teos")))
    if cached or not do_fetch:
        teos_meta = os.path.join(work_dir, "teos", f"{oid}_public.xml.meta.json")
        src = json.load(open(teos_meta, encoding="utf-8")).get("zip", "") if (cached and os.path.exists(teos_meta)
                                                                              and cached.endswith("_public.xml")) else ""
        return cached, src or XML_URL.format(oid=oid)
    mirrored = fetch_mirror(oid, os.path.join(work_dir, "xml"))
    if mirrored:
        return mirrored, XML_URL.format(oid=oid)
    return fetch_teos(oid, filing.get("XML_BATCH_ID", "") or "", work_dir)


def robots_status(host: str) -> dict:
    req = urllib.request.Request(f"https://{host}/robots.txt", headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8", "replace")
            return {"host": host, "status": r.status, "disallow_all": bool(re.search(r"(?m)^Disallow:\s*/\s*$", body))}
    except urllib.error.HTTPError as e:
        return {"host": host, "status": e.code, "disallow_all": False}
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return {"host": host, "status": f"error {type(e).__name__}", "disallow_all": False}


# ----------------------------------------------------------------------------- XML extraction (pure on a parsed tree)
def header(root) -> dict:
    return {"return_ts": text(root, ".//{*}ReturnHeader/{*}ReturnTs"),
            "tax_period_end": text(root, ".//{*}ReturnHeader/{*}TaxPeriodEndDt"),
            "amended": text(root, ".//{*}IRS990/{*}AmendedReturnInd") or "",
            "filer_name": text(root, ".//{*}ReturnHeader/{*}Filer/{*}BusinessName/{*}BusinessNameLine1Txt")}


def schedule(root, name: str):
    return root.find(f".//{{*}}ReturnData/{{*}}{name}")


def part_viii_ix(f990) -> dict:
    direct = {k: num(text(f990, f"{{*}}{k}")) for k in PART_VIII}
    expenses = {k: num(text(f990, f"{{*}}{k}/{{*}}TotalAmt")) for k in PART_IX}
    other_exp = tuple((text(e, "{*}Desc"), num(text(e, "{*}TotalAmt"))) for e in f990.findall("{*}OtherExpensesGrp"))
    sales = {k: num(text(f990, f"{{*}}{k}/{{*}}SecuritiesAmt")) for k in
             ("GrossAmountSalesAssetsGrp", "LessCostOthBasisSalesExpnssGrp", "GainOrLossGrp")}
    sales_other = {k + "_other": num(text(f990, f"{{*}}{k}/{{*}}OtherAmt")) for k in
                   ("GrossAmountSalesAssetsGrp", "LessCostOthBasisSalesExpnssGrp", "GainOrLossGrp")}
    return {**direct, **expenses, **sales, **sales_other, "other_expenses": other_exp,
            "CYGrantsAndSimilarPaidAmt": num(text(f990, "{*}CYGrantsAndSimilarPaidAmt")),
            "CYTotalExpensesAmt": num(text(f990, "{*}CYTotalExpensesAmt")),
            "TotalAssetsEOYAmt": num(text(f990, "{*}TotalAssetsEOYAmt")),
            "NetAssetsOrFundBalancesEOYAmt": num(text(f990, "{*}NetAssetsOrFundBalancesEOYAmt")),
            "DonorAdvisedFundInd": text(f990, "{*}DonorAdvisedFundInd"),
            "GrantsToOrganizationsInd": text(f990, "{*}GrantsToOrganizationsInd"),
            "Form8282PropertyDisposedOfInd": text(f990, "{*}Form8282PropertyDisposedOfInd"),
            "Form8282FiledCnt": text(f990, "{*}Form8282FiledCnt"),
            "DeductibleNonCashContriInd": text(f990, "{*}DeductibleNonCashContriInd"),
            "mission": text(f990, "{*}ActivityOrMissionDesc") or text(f990, "{*}MissionDesc"),
            "program_desc": " ".join(t for t in (text(e, "{*}Desc") for e in f990.findall("{*}ProgSrvcAccomActy2Grp")) if t)}


def contractors(f990) -> tuple[dict, ...]:
    def one(e):
        return {"name": text(e, ".//{*}BusinessNameLine1Txt") or text(e, ".//{*}PersonNm"),
                "services": text(e, "{*}ServicesDesc"), "amount": num(text(e, "{*}CompensationAmt"))}
    return tuple(one(e) for e in f990.findall("{*}ContractorCompensationGrp"))


def schedule_m(sm) -> dict:
    def cat(e):
        tag = local(e.tag)
        desc = text(e, "{*}Desc")
        return {"category": SCHED_M_GROUPS.get(tag, tag) + (f": {desc}" if desc else ""), "tag": tag,
                "count": num(text(e, "{*}ContributionCnt")), "amount": num(text(e, "{*}NoncashContributionsRptF990Amt")),
                "method": text(e, "{*}MethodOfDeterminingRevenuesTxt")}
    cats = tuple(cat(e) for e in sm if local(e.tag) in SCHED_M_GROUPS) if sm is not None else ()
    notes = tuple((text(d, "{*}FormAndLineReferenceDesc"), text(d, "{*}ExplanationTxt"))
                  for d in sm.findall("{*}SupplementalInformationDetail")) if sm is not None else ()
    flags = {k: text(sm, f"{{*}}{k}") for k in ("Form8283ReceivedCnt", "AnyPropertyThatMustBeHeldInd",
                                                "ReviewProcessUnusualNCGiftsInd", "ThirdPartiesUsedInd")}
    return {"categories": cats, "notes": notes, **flags}


def schedule_i(si) -> tuple[dict, ...]:
    def one(t):
        return {"name": " ".join(x for x in (text(t, "{*}RecipientBusinessName/{*}BusinessNameLine1Txt"),
                                             text(t, "{*}RecipientBusinessName/{*}BusinessNameLine2Txt")) if x)
                or text(t, "{*}RecipientNameBusiness/{*}BusinessNameLine1Txt"),
                "ein": ein9(text(t, "{*}RecipientEIN")), "cash": num(text(t, "{*}CashGrantAmt")) or 0.0,
                "noncash": num(text(t, "{*}NonCashAssistanceAmt")) or 0.0,
                "noncash_desc": text(t, "{*}NonCashAssistanceDesc"), "purpose": text(t, "{*}PurposeOfGrantTxt")}
    return tuple(one(t) for t in si.findall("{*}RecipientTable")) if si is not None else ()


def schedule_r(sr) -> tuple[dict, ...]:
    def one(t):
        return {"name": text(t, ".//{*}BusinessNameLine1Txt"), "type": text(t, "{*}TransactionTypeTxt"),
                "amount": num(text(t, "{*}InvolvedAmt")), "method": text(t, "{*}MethodOfAmountDeterminationTxt")}
    return tuple(one(t) for t in sr.findall("{*}TransactionsRelatedOrgGrp")) if sr is not None else ()


def schedule_d(sd) -> dict:
    keys = ("DonorAdvisedFundsHeldCnt", "DonorAdvisedFundsContriAmt", "DonorAdvisedFundsGrantsAmt",
            "DonorAdvisedFundsVlEOYAmt")
    return {k: num(text(sd, f"{{*}}{k}")) for k in keys} if sd is not None else {}


def schedule_o(so) -> tuple[tuple[str, str], ...]:
    return tuple((text(d, "{*}FormAndLineReferenceDesc"), text(d, "{*}ExplanationTxt"))
                 for d in so.findall("{*}SupplementalInformationDetail")) if so is not None else ()


def extract_return(path: str) -> dict:
    root = ET.parse(path).getroot()
    f990 = schedule(root, "IRS990")
    sched_b = schedule(root, "IRS990ScheduleB")
    all_text = " ".join(leaf_texts(root))
    return {**header(root), "p": part_viii_ix(f990), "contractors": contractors(f990),
            "sched_m": schedule_m(schedule(root, "IRS990ScheduleM")),
            "sched_i": schedule_i(schedule(root, "IRS990ScheduleI")),
            "sched_r": schedule_r(schedule(root, "IRS990ScheduleR")),
            "sched_d": schedule_d(schedule(root, "IRS990ScheduleD")),
            "sched_o": schedule_o(schedule(root, "IRS990ScheduleO")),
            "sched_b_restricted": bool(sched_b is not None and "RESTRICTED" in " ".join(leaf_texts(sched_b))),
            "schedules": tuple(local(c.tag) for c in root.find("{*}ReturnData")),
            "mentions_8282": tuple(sorted({m.group(0) for m in re.finditer(r".{0,80}8282.{0,80}", all_text)})),
            "mentions_chariot": tuple(sorted({m.group(0) for m in re.finditer(r".{0,60}[Cc][Hh][Aa][Rr][Ii][Oo][Tt].{0,60}",
                                                                              all_text)}))}


def sponsor_lines_to(path: str, target_eins: frozenset[str]) -> tuple[dict, ...]:
    """Stream a (possibly very large) sponsor return; keep Schedule I lines whose EIN or name is a target."""
    def keep(t) -> bool:
        return ein9(text(t, "{*}RecipientEIN")) in target_eins or bool(re.search(r"dechomai", " ".join(leaf_texts(t)), re.I))
    def lines():
        for _, el in ET.iterparse(path, events=("end",)):
            if local(el.tag) == "RecipientTable":
                if keep(el):
                    yield schedule_i_line(el)
                el.clear()
    return tuple(lines())


def schedule_i_line(t) -> dict:
    return {"name": text(t, "{*}RecipientBusinessName/{*}BusinessNameLine1Txt"), "ein": ein9(text(t, "{*}RecipientEIN")),
            "cash": num(text(t, "{*}CashGrantAmt")) or 0.0, "noncash": num(text(t, "{*}NonCashAssistanceAmt")) or 0.0,
            "noncash_desc": text(t, "{*}NonCashAssistanceDesc"), "purpose": text(t, "{*}PurposeOfGrantTxt")}


# ----------------------------------------------------------------------------- classification
def name_group(name: str) -> str:
    return next((g for g, rx in GROUP_NAME_RX if rx.search(name or "")), "")


def sponsor_group(ein: str, name: str) -> str:
    """Name wins over EIN when both point to a (different) target group: Dechomai's TY2023 return files
    'SCHWAB CHARITABLE TRUST' under AEF's EIN 34-1747398."""
    return name_group(name) or SPONSOR_GROUPS.get(ein, "")


def group_conflict(ein: str, name: str) -> bool:
    return bool(name_group(name) and ein in SPONSOR_GROUPS and SPONSOR_GROUPS[ein] != name_group(name))


def asset_class(category: str) -> str:
    return next((c for k, c in ASSET_CLASS if k.lower() in category.lower()), "other non-cash")


def return_ts(path: str) -> str:
    with open(path, "rb") as fh:
        head = fh.read(8192).decode("utf-8", "replace")
    m = re.search(r"<ReturnTs>([^<]+)</ReturnTs>", head)
    return m.group(1) if m else ""


def select_latest(filings: Sequence[Mapping]) -> tuple[dict, ...]:
    """One return per (EIN, TAX_PERIOD): the latest ReturnTs (object ids are not in filing order)."""
    groups = group_by(filings, lambda f: (f["EIN"], f["TAX_PERIOD"]))
    return tuple(max(g, key=lambda f: (f.get("return_ts", ""), f["OBJECT_ID"])) for g in groups.values())


def dedupe_filings(filings: Iterable[Mapping]) -> tuple[dict, ...]:
    return tuple({f["OBJECT_ID"]: f for f in filings}.values())


# ----------------------------------------------------------------------------- record builders (pure)
def base(f: Mapping, ex: Mapping, src: str, selected: bool) -> dict:
    return {"entity": DECHOMAI.get(f["EIN"], f.get("TAXPAYER_NAME", "")), "ein": f["EIN"],
            "tax_year": f["TAX_PERIOD"][:4], "tax_period_end": ex.get("tax_period_end", ""), "object_id": f["OBJECT_ID"],
            "selected": "1" if selected else "0", "source_url": src}


def return_records(f: Mapping, ex: Mapping, src: str, selected: bool, dafrc: Mapping) -> tuple[dict, ...]:
    b = base(f, ex, src, selected)
    p = ex["p"]
    summary_items = (("total_contributions", p["TotalContributionsAmt"]), ("noncash_contributions", p["NoncashContributionsAmt"]),
                     ("program_service_revenue", p["CYProgramServiceRevenueAmt"]), ("other_revenue", p["CYOtherRevenueAmt"]),
                     ("investment_income_line_summary", p["CYInvestmentIncomeAmt"]), ("total_revenue", p["CYTotalRevenueAmt"]),
                     ("grants_paid", p["CYGrantsAndSimilarPaidAmt"]), ("total_expenses", p["CYTotalExpensesAmt"]),
                     ("securities_sales_gross", p["GrossAmountSalesAssetsGrp"]),
                     ("securities_sales_cost_basis", p["LessCostOthBasisSalesExpnssGrp"]),
                     ("securities_sales_gain", p["GainOrLossGrp"]), ("other_asset_sales_gross", p["GrossAmountSalesAssetsGrp_other"]),
                     ("total_assets_eoy", p["TotalAssetsEOYAmt"]), ("net_assets_eoy", p["NetAssetsOrFundBalancesEOYAmt"]),
                     *((f"part_ix_{k}", p[k]) for k in PART_IX),
                     *((f"part_ix_other_expense:{d}", a) for d, a in p["other_expenses"]),
                     *((f"sched_d_{k}", v) for k, v in ex["sched_d"].items()),
                     ("sched_m_form8283_received_cnt", num(ex["sched_m"].get("Form8283ReceivedCnt"))),
                     ("sched_i_lines", float(len(ex["sched_i"]))),
                     ("sched_i_total", sum(r["cash"] + r["noncash"] for r in ex["sched_i"])))
    summary = tuple(row(record_type="return_line", item=k, amount_usd=v, **b) for k, v in summary_items if v is not None)
    flags = (row(record_type="return_flag", item="header", text=json.dumps({k: ex[k] for k in
             ("return_ts", "amended", "filer_name")}), **b),
             row(record_type="return_flag", item="part_iv_line6_DonorAdvisedFundInd", text=p["DonorAdvisedFundInd"], **b),
             row(record_type="return_flag", item="part_iv_line21_GrantsToOrganizationsInd", text=p["GrantsToOrganizationsInd"], **b),
             row(record_type="return_flag", item="mission", text=p["mission"], **b),
             row(record_type="return_flag", item="sched_b_restricted", text=str(ex["sched_b_restricted"]), **b),
             row(record_type="return_flag", item="schedules_filed", text=";".join(ex["schedules"]), **b))
    form8282 = (row(record_type="form8282", item="part_v_7c_Form8282PropertyDisposedOfInd",
                    text=p["Form8282PropertyDisposedOfInd"], count=num(p["Form8282FiledCnt"]), **b),
                row(record_type="form8282", item="text_mentions_8282", count=float(len(ex["mentions_8282"])),
                    text=" || ".join(ex["mentions_8282"])[:1000], **b))
    sm = tuple(row(record_type="sched_m", item=c["tag"], category=c["category"], count=c["count"], amount_usd=c["amount"],
                   counterparty=asset_class(c["category"]), text=c["method"], **b) for c in ex["sched_m"]["categories"])
    sm_flags = tuple(row(record_type="sched_m_flag", item=k, text=ex["sched_m"].get(k, ""), **b)
                     for k in ("AnyPropertyThatMustBeHeldInd", "ReviewProcessUnusualNCGiftsInd", "ThirdPartiesUsedInd"))
    sm_notes = tuple(row(record_type="sched_m_note", item=ref, text=t, **b) for ref, t in ex["sched_m"]["notes"])
    si = tuple(row(record_type="sched_i", item=r["purpose"], amount_usd=r["cash"], amount2_usd=r["noncash"],
                   counterparty=r["name"], counterparty_ein=r["ein"], sponsor_group=sponsor_group(r["ein"], r["name"]),
                   category=("DECHOMAI_INTRA" if r["ein"] in DECHOMAI else
                             dafrc.get(r["ein"], "") or ("DAFRC National" if name_group(r["name"]) else "")),
                   text=r["noncash_desc"] + (" | EIN/name conflict: name used" if group_conflict(r["ein"], r["name"])
                                             else ""), **b) for r in ex["sched_i"])
    ctr = tuple(row(record_type="contractor", counterparty=c["name"], item=c["services"], amount_usd=c["amount"], **b)
                for c in ex["contractors"])
    sr = tuple(row(record_type="sched_r_txn", counterparty=t["name"], item=t["type"], amount_usd=t["amount"],
                   text=t["method"], **b) for t in ex["sched_r"])
    so = tuple(row(record_type="sched_o", item=ref, text=t, **b) for ref, t in ex["sched_o"])
    chariot = (row(record_type="return_flag", item="text_mentions_chariot", count=float(len(ex["mentions_chariot"])),
                   text=" || ".join(ex["mentions_chariot"])[:1000], **b),)
    return summary + flags + form8282 + sm + sm_flags + sm_notes + si + ctr + sr + so + chariot


def line(records: Sequence[Mapping], ein: str, year: str, item: str) -> float | None:
    hit = next((r for r in records if r["record_type"] == "return_line" and r["selected"] == "1" and r["ein"] == ein
                and r["tax_year"] == year and r["item"] == item), None)
    return num(hit["amount_usd"]) if hit else None


def sel(records: Sequence[Mapping], rtype: str, ein: str | None = None, year: str | None = None) -> tuple[dict, ...]:
    return tuple(r for r in records if r["record_type"] == rtype and r["selected"] == "1"
                 and (ein is None or r["ein"] == ein) and (year is None or r["tax_year"] == year))


def grant_amt(r: Mapping) -> float:
    return (num(r["amount_usd"]) or 0.0) + (num(r["amount2_usd"]) or 0.0)


def dechomai_year_metrics(records: Sequence[Mapping], year: str) -> tuple[dict, ...]:
    """Combined DAT+DF metrics for one tax year: external flows, asset mix, routing to sponsor groups, effective take."""
    b = {"entity": "Dechomai combined (DAT+DF)", "ein": f"{DAT};{DF}", "tax_year": year, "selected": "1",
         "source_url": "computed from the selected returns in this file"}
    si = sel(records, "sched_i", year=year)
    si = tuple(r for r in si if r["ein"] in DECHOMAI)
    intra = sum(grant_amt(r) for r in si if r["counterparty_ein"] in DECHOMAI)
    contrib = sum(line(records, e, year, "total_contributions") or 0.0 for e in DECHOMAI)
    noncash = sum(line(records, e, year, "noncash_contributions") or 0.0 for e in DECHOMAI)
    grants_ext = sum(grant_amt(r) for r in si if r["counterparty_ein"] not in DECHOMAI)
    grants_p9 = sum(line(records, e, year, "grants_paid") or 0.0 for e in DECHOMAI)
    df_contrib = line(records, DF, year, "total_contributions") or 0.0
    intra_booked = intra if df_contrib >= intra else 0.0      # TY2021-22: DF did not book DAT's grants as revenue
    ext_contrib = contrib - intra_booked
    reimb = sum(num(r["amount_usd"]) or 0.0 for r in sel(records, "sched_r_txn", DAT, year)
                if re.search(r"administrative|admin", r["text"], re.I))
    sm = tuple(r for r in sel(records, "sched_m", year=year) if r["ein"] in DECHOMAI)
    sm_total = total(sm)
    sm_count = sum(num(r["count"]) or 0.0 for r in sm)
    mix = group_by(sm, lambda r: r["counterparty"])
    mix_rows = tuple(row(record_type="asset_mix", item=cls, count=sum(num(r["count"]) or 0 for r in rs),
                         amount_usd=total(rs), ratio=ratio(total(rs), sm_total), **b) for cls, rs in sorted(mix.items()))
    by_group = group_by(tuple(r for r in si if r["sponsor_group"]), lambda r: r["sponsor_group"])
    route_rows = tuple(row(record_type="routing_dechomai_to_sponsor", sponsor_group=g, count=float(len(rs)),
                           amount_usd=sum(grant_amt(r) for r in rs), ratio=ratio(sum(grant_amt(r) for r in rs), grants_ext),
                           text="share = amount / Dechomai external Schedule I grants", **b)
                       for g, rs in sorted(by_group.items()))
    six = sum(grant_amt(r) for r in si if r["sponsor_group"])
    dafrc_any = sum(grant_amt(r) for r in si if r["category"] not in ("", "DECHOMAI_INTRA"))
    other_dafrc = tuple(r for r in si if r["category"] not in ("", "DECHOMAI_INTRA") and not r["sponsor_group"])
    route_rows = route_rows + (row(record_type="routing_dechomai_to_sponsor", sponsor_group="other DAFRC-listed sponsors",
                                   count=float(len(other_dafrc)), amount_usd=sum(grant_amt(r) for r in other_dafrc),
                                   ratio=ratio(sum(grant_amt(r) for r in other_dafrc), grants_ext),
                                   text="share = amount / Dechomai external Schedule I grants", **b),)
    cs = sum(num(r["amount_usd"]) or 0.0 for r in sel(records, "contractor", year=year)
             if r["ein"] in DECHOMAI and re.search(r"charitable solutions", r["counterparty"], re.I))
    fee_keys = ("part_ix_FeesForServicesManagementGrp", "part_ix_FeesForServicesOtherGrp",
                "part_ix_FeesForServicesLegalGrp", "part_ix_FeesForServicesAccountingGrp")
    mgmt_other = sum(line(records, e, year, k) or 0.0 for e in DECHOMAI for k in fee_keys[:2])
    all_fees = sum(line(records, e, year, k) or 0.0 for e in DECHOMAI for k in fee_keys)
    nongrant = sum((line(records, e, year, "total_expenses") or 0.0) - (line(records, e, year, "grants_paid") or 0.0)
                   for e in DECHOMAI)
    take = (("take_charitable_solutions_partVIIB", cs), ("take_partIX_mgmt_plus_other_fees", mgmt_other),
            ("take_partIX_all_fees_for_services", all_fees), ("take_all_nongrant_expenses", nongrant))
    take_rows = tuple(row(record_type="effective_take", item=k, amount_usd=v, amount2_usd=sm_total, ratio=ratio(v, sm_total),
                          text="ratio = amount / combined Schedule M non-cash total (amount2)", **b) for k, v in take) + \
        (row(record_type="effective_take", item="unreconciled_schedR_DAT_admin_reimbursement_to_DF", amount_usd=reimb,
             amount2_usd=sm_total, ratio=ratio(reimb, sm_total),
             text="DAT Schedule R Part V 'reimbursement for administrative services' to DF; not matched on DF's "
                  "Schedule R or in either Part IX, so not a confirmed fee", **b),)
    published = (("published_fee_1pct_of_schedM", PUBLISHED_FEE["low"] * sm_total),
                 ("published_fee_3pct_of_schedM", PUBLISHED_FEE["high"] * sm_total),
                 ("published_min_fee_x_schedM_count", PUBLISHED_FEE["min_usd"] * sm_count))
    pub_rows = tuple(row(record_type="effective_take", item=k, amount_usd=v, amount2_usd=sm_total, count=sm_count,
                         ratio=ratio(v, sm_total), text="benchmark from the published fee one-pager", **b)
                     for k, v in published)
    totals = (("contributions_gross", contrib), ("intra_group_grants", intra), ("intra_group_booked_by_DF", intra_booked),
              ("contributions_external", ext_contrib),
              ("noncash_contributions", noncash), ("schedM_total", sm_total), ("schedM_count", sm_count),
              ("grants_partIX", grants_p9), ("grants_external_schedI", grants_ext),
              ("grants_to_six_sponsor_groups", six), ("grants_to_any_dafrc_sponsor", dafrc_any))
    tot_rows = tuple(row(record_type="dechomai_year", item=k, amount_usd=v,
                         ratio=(ratio(v, grants_ext) if k.startswith("grants_to") else None), **b) for k, v in totals)
    return tot_rows + mix_rows + route_rows + take_rows + pub_rows


def sponsor_records(f: Mapping, lines_: Sequence[Mapping], src: str, selected: bool) -> tuple[dict, ...]:
    b = {"entity": SPONSOR_GROUPS.get(f["EIN"], f.get("TAXPAYER_NAME", "")), "ein": f["EIN"],
         "tax_year": f["TAX_PERIOD"][:4], "tax_period_end": f["TAX_PERIOD"], "object_id": f["OBJECT_ID"],
         "selected": "1" if selected else "0", "source_url": src, "sponsor_group": SPONSOR_GROUPS.get(f["EIN"], "")}
    scanned = row(record_type="sponsor_scan", item="schedule_i_lines_to_dechomai", count=float(len(lines_)),
                  amount_usd=sum(l["cash"] + l["noncash"] for l in lines_), text=f.get("TAXPAYER_NAME", ""), **b)
    hits = tuple(row(record_type="sponsor_to_dechomai", counterparty=l["name"], counterparty_ein=l["ein"],
                     amount_usd=l["cash"], amount2_usd=l["noncash"], item=l["purpose"], text=l["noncash_desc"], **b)
                 for l in lines_)
    return (scanned,) + hits


def dpn_tests(records: Sequence[Mapping]) -> tuple[dict, ...]:
    years = sorted({r["tax_year"] for r in records if r["ein"] == DPN and r["selected"] == "1"})
    def one(y: str) -> tuple[dict, ...]:
        b = {"entity": "DAFpay Network Inc", "ein": DPN, "tax_year": y, "selected": "1",
             "source_url": next((r["source_url"] for r in records if r["ein"] == DPN and r["tax_year"] == y
                                 and r["selected"] == "1"), "")}
        contrib = line(records, DPN, y, "total_contributions") or 0.0
        psr = line(records, DPN, y, "program_service_revenue") or 0.0
        other_rev = line(records, DPN, y, "other_revenue") or 0.0
        fees_other = line(records, DPN, y, "part_ix_FeesForServicesOtherGrp") or 0.0
        grants = line(records, DPN, y, "grants_paid") or 0.0
        schedi = sel(records, "sched_i", DPN, y)
        named = tuple(r for r in records if r["ein"] == DPN and r["tax_year"] == y and r["selected"] == "1"
                      and CHARIOT_RX.search(" ".join((r["counterparty"], r["text"] if r["item"] != "text_mentions_chariot"
                                                      else ""))))
        chariot_txt = next((r for r in records if r["ein"] == DPN and r["tax_year"] == y and r["selected"] == "1"
                            and r["item"] == "text_mentions_chariot"), {})
        r_fee = ratio(fees_other, contrib)
        consistent = r_fee is not None and abs(r_fee - DAFPAY_RATE) <= DAFPAY_BAND
        verdict = ("revenue" if (psr or other_rev) else
                   "expense named to Chariot" if (named or (num(chariot_txt.get("count")) or 0) > 0) else
                   "unnamed expense about 2.9% of receipts" if consistent else
                   "not visible at 2.9% (netted before receipt or outside DPN), partial unnamed fee expense")
        items = (("contributions", contrib, None), ("program_service_revenue", psr, None), ("other_revenue", other_rev, None),
                 ("fees_for_services_other", fees_other, r_fee), ("dafpay_2.9pct_of_contributions", DAFPAY_RATE * contrib, DAFPAY_RATE),
                 ("fees_other_minus_2.9pct", fees_other - DAFPAY_RATE * contrib, None), ("grants_partIX", grants, ratio(grants, contrib)),
                 ("schedI_total", sum(grant_amt(r) for r in schedi), ratio(sum(grant_amt(r) for r in schedi), grants)),
                 ("schedI_lines", float(len(schedi)), None),
                 ("chariot_named_anywhere", float(len(named) + int(num(chariot_txt.get("count")) or 0)), None))
        return tuple(row(record_type="dpn_fee_test", item=k, amount_usd=v, ratio=rt, **b) for k, v, rt in items) + \
            (row(record_type="dpn_fee_test", item="verdict", text=verdict, **b),)
    return tuple(r for y in years for r in one(y))


def load_dafrc(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["ein"].zfill(9): f"DAFRC {r['type']}" for r in csv.DictReader(fh)}


# ----------------------------------------------------------------------------- main (I/O edge)
def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("root", help="repo root ('.')")
    ap.add_argument("--irs-dir", required=True, help="folder holding TEOS index_YYYY.csv files")
    ap.add_argument("--work-dir", required=True, help="cache folder for fetched XML (outside the repo)")
    ap.add_argument("--xml-dir", action="append", default=[], help="extra folders already holding {oid}.xml")
    ap.add_argument("--fetch", action="store_true", help="fetch XML not found locally (mirror, then 2026 TEOS zip)")
    a = ap.parse_args(argv)
    data_dir = os.path.join(a.root, "data", "mission-2026-11-14")
    dafrc = load_dafrc(os.path.join(data_dir, "dafrc-sponsor-schedule-d-fy2019-2024.csv"))
    robots = tuple(robots_status(h) for h in ("gt990datalake-rawdata.s3.amazonaws.com", "apps.irs.gov")) if a.fetch else ()

    idx = load_index(a.irs_dir, frozenset((DAT, DF, DPN, *SPONSOR_GROUPS)))
    f990 = dedupe_filings(r for r in idx if r.get("RETURN_TYPE") == "990")
    dech = tuple(f for f in f990 if f["EIN"] in DECHOMAI and int(f["TAX_PERIOD"][:4]) in DECHOMAI_YEARS)
    dpn = tuple(f for f in f990 if f["EIN"] == DPN)
    spons = tuple(f for f in f990 if f["EIN"] in SPONSOR_GROUPS
                  and SPONSOR_TAX_PERIODS[0] <= f["TAX_PERIOD"] <= SPONSOR_TAX_PERIODS[1])
    located = {f["OBJECT_ID"]: locate(f, a.xml_dir, a.work_dir, a.fetch) for f in dech + dpn + spons}
    with_ts = tuple({**f, "return_ts": return_ts(located[f["OBJECT_ID"]][0]) if located[f["OBJECT_ID"]][0] else ""}
                    for f in dech + dpn + spons)
    chosen = frozenset(f["OBJECT_ID"] for f in select_latest(with_ts))

    def own(f):
        path, src = located[f["OBJECT_ID"]]
        if not path:
            return (row(record_type="missing", entity=f.get("TAXPAYER_NAME", ""), ein=f["EIN"], tax_year=f["TAX_PERIOD"][:4],
                        object_id=f["OBJECT_ID"], text="XML not found locally or in mirror/TEOS zip"),)
        return return_records(f, extract_return(path), src, f["OBJECT_ID"] in chosen, dafrc)

    def sponsor(f):
        path, src = located[f["OBJECT_ID"]]
        if not path:
            return (row(record_type="missing", entity=f.get("TAXPAYER_NAME", ""), ein=f["EIN"], tax_year=f["TAX_PERIOD"][:4],
                        object_id=f["OBJECT_ID"], text="XML not found locally or in mirror"),)
        return sponsor_records(f, sponsor_lines_to(path, frozenset(DECHOMAI)), src, f["OBJECT_ID"] in chosen)

    base_records = tuple(r for f in sorted(dech + dpn, key=lambda f: (f["EIN"], f["TAX_PERIOD"], f["OBJECT_ID"]))
                         for r in own(f))
    sponsor_recs = tuple(r for f in sorted(spons, key=lambda f: (f["EIN"], f["TAX_PERIOD"], f["OBJECT_ID"]))
                         for r in sponsor(f))
    derived = tuple(r for y in DECHOMAI_YEARS for r in dechomai_year_metrics(base_records, str(y))) + dpn_tests(base_records)
    four_year = four_year_rows(derived)
    sponsor_summary = sponsor_inbound_summary(sponsor_recs)
    out_rows = base_records + sponsor_recs + derived + four_year + sponsor_summary
    out = os.path.join(data_dir, OUT_NAME)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(out_rows)
    summary = {"out": out, "rows": len(out_rows), "robots": robots,
               "filings": {"dechomai": len(dech), "dpn": len(dpn), "sponsors": len(spons)},
               "missing": [r["object_id"] for r in out_rows if r["record_type"] == "missing"]}
    print(json.dumps(summary, indent=1))
    return 0


def four_year_rows(derived: Sequence[Mapping]) -> tuple[dict, ...]:
    b = {"entity": "Dechomai combined (DAT+DF)", "ein": f"{DAT};{DF}", "tax_year": "2021-2024", "selected": "1",
         "source_url": "sum of the tax-year rows in this file"}
    def s(rtype, item, field="amount_usd"):
        return sum(num(r[field]) or 0.0 for r in derived if r["record_type"] == rtype and r["item"] == item
                   and r["tax_year"] in tuple(str(y) for y in DECHOMAI_YEARS))
    noncash = s("dechomai_year", "schedM_total")
    grants_ext = s("dechomai_year", "grants_external_schedI")
    takes = tuple(row(record_type="effective_take", item=k, amount_usd=s("effective_take", k), amount2_usd=noncash,
                      ratio=ratio(s("effective_take", k), noncash), **b)
                  for k in ("take_charitable_solutions_partVIIB", "take_partIX_mgmt_plus_other_fees",
                            "take_partIX_all_fees_for_services", "take_all_nongrant_expenses",
                            "unreconciled_schedR_DAT_admin_reimbursement_to_DF",
                            "published_fee_1pct_of_schedM", "published_fee_3pct_of_schedM",
                            "published_min_fee_x_schedM_count"))
    groups = sorted({r["sponsor_group"] for r in derived if r["record_type"] == "routing_dechomai_to_sponsor"})
    routes = tuple(row(record_type="routing_dechomai_to_sponsor", sponsor_group=g,
                       amount_usd=sum(num(r["amount_usd"]) or 0 for r in derived
                                      if r["record_type"] == "routing_dechomai_to_sponsor" and r["sponsor_group"] == g),
                       ratio=ratio(sum(num(r["amount_usd"]) or 0 for r in derived
                                       if r["record_type"] == "routing_dechomai_to_sponsor" and r["sponsor_group"] == g),
                                   grants_ext), **b) for g in groups)
    mix_classes = sorted({r["item"] for r in derived if r["record_type"] == "asset_mix"})
    sm_total = s("dechomai_year", "schedM_total")
    mix = tuple(row(record_type="asset_mix", item=c, count=s("asset_mix", c, "count"), amount_usd=s("asset_mix", c),
                    ratio=ratio(s("asset_mix", c), sm_total), **b) for c in mix_classes)
    tots = tuple(row(record_type="dechomai_year", item=k, amount_usd=s("dechomai_year", k),
                     ratio=(ratio(s("dechomai_year", k), grants_ext) if k.startswith("grants_to") else None), **b)
                 for k in ("contributions_gross", "intra_group_grants", "intra_group_booked_by_DF", "contributions_external", "noncash_contributions",
                           "schedM_total", "schedM_count", "grants_partIX", "grants_external_schedI",
                           "grants_to_six_sponsor_groups", "grants_to_any_dafrc_sponsor"))
    return tots + mix + routes + takes


def sponsor_inbound_summary(recs: Sequence[Mapping]) -> tuple[dict, ...]:
    hits = tuple(r for r in recs if r["record_type"] == "sponsor_to_dechomai" and r["selected"] == "1")
    groups = group_by(hits, lambda r: (r["sponsor_group"], r["counterparty_ein"]))
    return tuple(row(record_type="routing_sponsor_to_dechomai_total", sponsor_group=g, counterparty_ein=e,
                     counterparty=DECHOMAI.get(e, ""), tax_year="FY2021-FY2025", count=float(len(rs)),
                     amount_usd=sum(grant_amt(r) for r in rs), amount2_usd=sum(num(r["amount2_usd"]) or 0 for r in rs),
                     text="sum of selected sponsor returns, tax periods 2021-06..2025-06; amount2 = non-cash part",
                     selected="1", source_url="sponsor_to_dechomai rows in this file")
                 for (g, e), rs in sorted(groups.items()))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
