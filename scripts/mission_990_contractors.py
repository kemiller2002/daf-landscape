#!/usr/bin/env python3
"""Form 990 contractor and Schedule D harvest for DAF sponsors (queue items P-VEN-06, P-MOR-03).

Stdlib only; written in a functional style (pure transforms, I/O at the edges).

Sources (documented in research/mission-2026-11-14/vendor-footprint-990-harvest.md):
  * Sponsor universe: DAFRC panel  data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv
  * Return locator:   IRS TEOS e-file index  https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv
                      (one CSV per processing year: EIN, TAX_PERIOD, RETURN_TYPE, OBJECT_ID)
  * Return content:   IRS e-file XML as mirrored per object id by the GivingTuesday 990 data lake
                      https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml
                      (ProPublica's XML download returns HTTP 403 to scripts; the IRS publishes XML only
                      inside multi-GB monthly ZIP batches and does not honour HTTP range requests.)

What is parsed from each Form 990 (streamed; parsing stops after Schedule D so Schedule I grant
lists of the largest sponsors are never downloaded in full):
  * header: TaxYr, TaxPeriodBeginDt/EndDt, ReturnTs, ReturnTypeCd, filer name, AmendedReturnInd
  * Part VII Section B: every ContractorCompensationGrp (name, ServicesDesc, CompensationAmt) and
    CntrctRcvdGreaterThan100KCnt (how many contractors were paid > $100k in total)
  * Part IV line 6 DonorAdvisedFundInd; Part IX line 11g/line 14 totals (other fees, IT)
  * Schedule D Part I: DonorAdvisedFundsHeldCnt, DonorAdvisedFundsContriAmt,
    DonorAdvisedFundsGrantsAmt, DonorAdvisedFundsVlEOYAmt

Tasks:
  contractors  top-N sponsor harvest -> form990-contractors-harvest.csv,
               form990-returns-schedule-d-harvest.csv, vendor-footprint-from-990.csv
  gaps         DAFRC closed / imputed sponsor-years checked against filed 990s -> dafrc-processing-gaps.csv
  outside      (P-MOR-01) 990 filers answering Part IV line 6 'Yes' in the IRS SOI annual extracts whose EIN is not in
               the DAFRC panel, FY2020-2025; Schedule D Part I parsed from each return ->
               non-dafrc-daf-filers-990.csv, non-dafrc-daf-filers-summary.csv
  --n-sponsors 0 --out-tag=-full harvests every FY2024 DAFRC sponsor (P-990-04) into *-full.csv files.

Usage:
  python3 scripts/mission_990_contractors.py --irs-dir DIR --cache-dir CACHE --fetch [--task all]
  DIR must hold index_2021.csv .. index_2026.csv (downloaded automatically into DIR with --fetch).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from typing import Callable, Iterable, Mapping, Sequence

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "mission-2026-11-14")
DAFRC_CSV = os.path.join(DATA, "dafrc-sponsor-schedule-d-fy2019-2024.csv")
EDGES_OUT = "relationship-graph-edges-additions-3.csv"      # written by task 'edges' (P-990-05); never read back as input
GRAPH_EDGES = (os.path.join(DATA, "relationship-graph-edges.csv"),
               os.path.join(DATA, "relationship-graph-edges-additions.csv"),
               os.path.join(DATA, "relationship-graph-edges-additions-2.csv"))
MANUAL_CSV = os.path.join(DATA, "form990-top-contractors.csv")

DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"
INDEX_URL = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/index_{y}.csv"
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
PP_FILING_URL = "https://projects.propublica.org/nonprofits/organizations/{ein}/{oid}/full"
INDEX_YEARS = tuple(range(2021, 2027))
HARVEST_FYS = (2022, 2023, 2024, 2025)          # fiscal year = calendar year in which the tax period ends
GAP_FYS = (2021, 2022, 2023, 2024)
FILED_SOURCES = frozenset({"IRS 990", "NPT historical data", "paper submission"})
NS = "{http://www.irs.gov/efile}"
EXTRACT_VERSION = 2


# ----------------------------------------------------------------------------- small pure helpers
def num(x) -> float | None:
    try:
        return float(str(x).replace(",", "")) if x not in (None, "") else None
    except ValueError:
        return None


def fmt(x) -> str:
    if x is None or x == "":
        return ""
    if isinstance(x, float):
        return str(int(x)) if x.is_integer() else f"{x:.6g}"
    return str(x)


def ein9(x: str) -> str:
    return re.sub(r"\D", "", x or "").zfill(9)


def _group_by_fast(items: Iterable, key: Callable) -> dict:
    # dict-of-tuples built with a local accumulator (O(n)); callers only see an immutable-style result
    acc = defaultdict(list)
    for it in items:
        acc[key(it)].append(it)
    return {k: tuple(v) for k, v in acc.items()}


def write_csv(path: str, rows: Sequence[Mapping], fields: Sequence[str]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows({k: fmt(r.get(k)) for k in fields} for r in rows)


def read_csv(path: str) -> tuple[dict, ...]:
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return tuple(csv.DictReader(fh))


# ----------------------------------------------------------------------------- sponsor universe
def load_dafrc(path: str = DAFRC_CSV) -> tuple[dict, ...]:
    return tuple({**r, "ein": ein9(r["ein"]), "fy": int(r["fiscal_year_end"])} for r in read_csv(path))


def select_targets(rows: Sequence[Mapping], n_total: int = 250) -> tuple[dict, ...]:
    """All National sponsors present in FY2024 plus the largest Community / Single Issue sponsors by
    FY2024 DAFRC eoy_daf_assets until n_total EINs are reached. n_total <= 0 selects every FY2024
    DAFRC sponsor (full universe, P-990-04). Pure."""
    fy24 = sorted((r for r in rows if r["fy"] == 2024), key=lambda r: -(num(r["eoy_daf_assets"]) or 0))
    national = tuple(r for r in fy24 if r["type"] == "National")
    non_nat = tuple(r for r in fy24 if r["type"] != "National")
    others = non_nat if n_total <= 0 else non_nat[: max(0, n_total - len(national))]
    rank = {r["ein"]: i + 1 for i, r in enumerate(fy24)}
    return tuple({"ein": r["ein"], "sponsor_name": r["name"], "type": r["type"], "subtype": r["subtype"],
                  "fy2024_daf_assets": num(r["eoy_daf_assets"]), "fy2024_assets_source": r["source_eoy_daf_assets"],
                  "fy2024_asset_rank": rank[r["ein"]],
                  "selection": "national_all" if r["type"] == "National" else
                  ("all_fy2024_dafrc" if n_total <= 0 else "top_non_national_by_fy2024_assets")}
                 for r in national + others)


# ----------------------------------------------------------------------------- IRS e-file index
def ensure_indexes(irs_dir: str, fetch: bool) -> tuple[str, ...]:
    os.makedirs(irs_dir, exist_ok=True)
    paths = tuple(os.path.join(irs_dir, f"index_{y}.csv") for y in INDEX_YEARS)
    for y, p in zip(INDEX_YEARS, paths):
        if not os.path.exists(p) and fetch:
            print(f"downloading {INDEX_URL.format(y=y)}", file=sys.stderr)
            urllib.request.urlretrieve(INDEX_URL.format(y=y), p)
    return tuple(p for p in paths if os.path.exists(p))


def load_index(paths: Sequence[str], eins: frozenset[str]) -> dict[str, tuple[dict, ...]]:
    def recs(p):
        year = re.search(r"index_(\d{4})", p).group(1)
        with open(p, newline="", encoding="latin-1") as fh:
            return tuple({"ein": ein9(d["EIN"]), "tax_period": d["TAX_PERIOD"], "return_type": d["RETURN_TYPE"],
                          "object_id": d["OBJECT_ID"], "taxpayer_name": d["TAXPAYER_NAME"], "index_year": year,
                          "index_url": INDEX_URL.format(y=year)}
                         for d in csv.DictReader(fh) if ein9(d.get("EIN", "")) in eins)
    allrecs = tuple(r for p in paths for r in recs(p))
    dedup = {r["object_id"]: r for r in sorted(allrecs, key=lambda r: r["index_year"])}  # one row per object id
    return {e: tuple(sorted(v, key=lambda r: (r["tax_period"], r["object_id"])))
            for e, v in _group_by_fast(dedup.values(), lambda r: r["ein"]).items()}


def latest_per_period(filings: Sequence[Mapping], fys: Sequence[int], types=("990",)) -> tuple[dict, ...]:
    """Newest submission (max OBJECT_ID, i.e. amended return supersedes) per tax period whose end year is in fys."""
    keep = tuple(f for f in filings if f["return_type"] in types and int(f["tax_period"][:4]) in fys)
    by = _group_by_fast(keep, lambda f: f["tax_period"])
    return tuple(max(v, key=lambda f: f["object_id"]) for _, v in sorted(by.items()))


def latest_for_fy(filings: Sequence[Mapping], fy: int, types: Sequence[str]) -> dict | None:
    cand = latest_per_period(filings, (fy,), types)
    return cand[-1] if cand else None


# ----------------------------------------------------------------------------- XML extract (streamed)
def local(tag: str) -> str:
    return tag[len(NS):] if tag.startswith(NS) else tag.split("}")[-1]


def text_of(el, path: Sequence[str]) -> str:
    node = reduce(lambda n, t: None if n is None else n.find(NS + t), path, el)
    return (node.text or "").strip() if node is not None and node.text else ""


def contractor_from(el) -> dict:
    name_el = el.find(NS + "ContractorName")
    parts = () if name_el is None else tuple(
        (x.text or "").strip() for x in name_el.iter()
        if local(x.tag) in ("BusinessNameLine1Txt", "BusinessNameLine2Txt", "PersonNm",
                            "BusinessNameLine1", "BusinessNameLine2") and x.text)
    addr = el.find(NS + "ContractorAddress")
    city = "" if addr is None else next((x.text.strip() for x in addr.iter() if local(x.tag) in ("CityNm", "City") and x.text), "")
    state = "" if addr is None else next((x.text.strip() for x in addr.iter()
                                          if local(x.tag) in ("StateAbbreviationCd", "ProvinceOrStateNm", "CountryCd") and x.text), "")
    return {"contractor_name": " ".join(parts), "services": text_of(el, ("ServicesDesc",)),
            "compensation": num(text_of(el, ("CompensationAmt",))), "contractor_city": city, "contractor_state": state}


def summarise_irs990(el) -> dict:
    return {"contractors": tuple(contractor_from(c) for c in el.iter(NS + "ContractorCompensationGrp")),
            "contractors_over_100k_cnt": num(text_of(el, ("CntrctRcvdGreaterThan100KCnt",))),
            "daf_ind_part_iv": text_of(el, ("DonorAdvisedFundInd",)),
            "amended_ind": text_of(el, ("AmendedReturnInd",)),
            "part_ix_it_total": num(text_of(el, ("InformationTechnologyGrp", "TotalAmt"))),
            "part_ix_fees_other_total": num(text_of(el, ("FeesForServicesOtherGrp", "TotalAmt"))),
            "part_ix_fees_mgmt_total": num(text_of(el, ("FeesForServicesManagementGrp", "TotalAmt"))),
            "part_ix_fees_invest_total": num(text_of(el, ("FeesForSrvcInvstMgmntFeesGrp", "TotalAmt"))),
            "total_assets_eoy": num(text_of(el, ("TotalAssetsGrp", "EOYAmt")))}


def summarise_sched_d(el) -> dict:
    return {"sched_d_present": 1,
            "sched_d_daf_count": num(text_of(el, ("DonorAdvisedFundsHeldCnt",))),
            "sched_d_daf_contributions": num(text_of(el, ("DonorAdvisedFundsContriAmt",))),
            "sched_d_daf_grants": num(text_of(el, ("DonorAdvisedFundsGrantsAmt",))),
            "sched_d_daf_eoy_value": num(text_of(el, ("DonorAdvisedFundsVlEOYAmt",))),
            "sched_d_other_funds_count": num(text_of(el, ("FundsAndOtherAccountsHeldCnt",))),
            "sched_d_other_funds_eoy_value": num(text_of(el, ("FundsAndOtherAccountsVlEOYAmt",)))}


LATE_SCHEDULE = re.compile(r"IRS990Schedule([E-Z])$")


def extract_stream(stream) -> dict:
    """Stream-parse one return. Stops after Schedule D (or at the first later schedule). Returns a
    plain dict; element objects are discarded as they close."""
    header, form, sched_d = {}, {}, {"sched_d_present": 0}
    ctx = ET.iterparse(stream, events=("start", "end"))
    for event, el in ctx:
        tag = local(el.tag)
        if event == "start":
            if LATE_SCHEDULE.match(tag) and form:
                break
            continue
        if tag == "ReturnHeader":
            header = {"tax_year": text_of(el, ("TaxYr",)) or text_of(el, ("TaxYear",)),
                      "tax_period_begin": text_of(el, ("TaxPeriodBeginDt",)),
                      "tax_period_end": text_of(el, ("TaxPeriodEndDt",)),
                      "return_ts": text_of(el, ("ReturnTs",)),
                      "return_type": text_of(el, ("ReturnTypeCd",)),
                      "filer_name": " ".join(filter(None, (text_of(el, ("Filer", "BusinessName", "BusinessNameLine1Txt")),
                                                           text_of(el, ("Filer", "BusinessName", "BusinessNameLine2Txt"))))),
                      "filer_ein": text_of(el, ("Filer", "EIN"))}
            el.clear()
        elif tag == "IRS990":
            form = summarise_irs990(el)
            el.clear()
        elif tag == "IRS990ScheduleD":
            sched_d = summarise_sched_d(el)
            el.clear()
            break
        elif tag.startswith("IRS990Schedule") or tag in ("IRS990EZ", "IRS990PF"):
            el.clear()
    return {**header, **form, **sched_d}


def fetch_extract(oid: str, cache_dir: str, fetch: bool, retries: int = 2) -> dict:
    """Cached extract for one object id. Caches parsed JSON (not raw XML) and definitive HTTP errors."""
    path = os.path.join(cache_dir, "extract990", f"{oid}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            cached = json.load(fh)
        if cached.get("_v") == EXTRACT_VERSION:
            return cached
    if not fetch:
        return {"xml_status": "not_fetched"}
    url = XML_URL.format(oid=oid)
    req = urllib.request.Request(url, headers={"User-Agent": "research-script/1.0 (stdlib urllib)"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                out = {**extract_stream(resp), "xml_status": "ok"}
            break
        except urllib.error.HTTPError as e:
            out = {"xml_status": f"http_{e.code}"}
            if e.code in (403, 404):
                break
        except (urllib.error.URLError, TimeoutError, ET.ParseError, ConnectionError, OSError) as e:
            out = {"xml_status": f"error:{type(e).__name__}"}
            time.sleep(2 * (attempt + 1))
    result = {**out, "_v": EXTRACT_VERSION, "xml_url": url,
              "contractors": [dict(c) for c in out.get("contractors", ())]}
    if not result["xml_status"].startswith("error"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(result, fh)
    return result


WORKERS = int(os.environ.get("MISSION990_WORKERS", "8"))


def fetch_all(oids: Sequence[str], cache_dir: str, fetch: bool, workers: int | None = None) -> dict[str, dict]:
    workers = workers or WORKERS
    uniq = tuple(dict.fromkeys(oids))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = tuple(ex.map(lambda o: fetch_extract(o, cache_dir, fetch), uniq))
    return dict(zip(uniq, res))


# ----------------------------------------------------------------------------- vendor normaliser
# (pattern, vendor_group, vendor_entity, category). Ordered: first match wins. Applied to the
# contractor name only (never to the services text) so a match is always the payee's own name.
VENDOR_RULES: tuple[tuple[str, str, str, str], ...] = (
    (r"stellar\s+tech|\bstellar\s+technology|\biphi\b", "Ren (incl. Stellar/iPhi)", "Stellar Technology Solutions (iPhi)", "daf_tech_admin_vendor"),
    (r"renaissance\s+admin", "Ren (incl. Stellar/iPhi)", "Renaissance Administration LLC", "daf_tech_admin_vendor"),
    (r"renaissance\s+philanthropic|renpsg|ren\s*psg|^ren\b|^ren[\s,]+(inc|llc)", "Ren (incl. Stellar/iPhi)", "Ren / RenPSG", "daf_tech_admin_vendor"),
    (r"renaissance\s+acquisition", "Ren (incl. Stellar/iPhi)", "Renaissance Acquisition Company LLC", "daf_tech_admin_vendor"),
    (r"renaissance\s+charitable", "Renaissance Charitable Foundation", "Renaissance Charitable Foundation", "daf_sponsor_as_contractor"),
    (r"foundation\s+source", "Foundation Source", "Foundation Source", "daf_tech_admin_vendor"),
    (r"give\s*interactive", "Give Interactive", "Give Interactive", "daf_tech_vendor"),
    (r"\btifin\b", "TIFIN", "TIFIN", "daf_tech_vendor"),
    (r"foundant", "Foundant Technologies", "Foundant Technologies", "daf_tech_vendor"),
    (r"\bnpact\b|n\s*pact\s+(llc|inc)", "NPact", "NPact", "daf_tech_vendor"),
    (r"blackbaud|microedge", "Blackbaud", "Blackbaud", "daf_tech_vendor"),
    (r"community\s*suite|\bcsuite\b", "CSuite (CommunitySuite)", "CSuite (CommunitySuite)", "daf_tech_vendor"),
    (r"crown\s+philanthropic|donorfirst", "Crown Philanthropic Solutions", "Crown Philanthropic Solutions", "daf_tech_admin_vendor"),
    (r"pinkaloo", "Pinkaloo", "Pinkaloo", "daf_tech_vendor"),
    (r"groundswell", "Groundswell", "Groundswell", "daf_tech_vendor"),
    (r"\bchariot\b", "Chariot", "Chariot", "payment_processor"),
    (r"cybergrants|bonterra|network\s+for\s+good|everyaction|social\s+solutions", "Bonterra (CyberGrants/Network for Good)", "Bonterra", "daf_tech_vendor"),
    (r"benevity", "Benevity", "Benevity", "daf_tech_vendor"),
    (r"fluxx", "Fluxx", "Fluxx", "daf_tech_vendor"),
    (r"smartsimple", "SmartSimple", "SmartSimple", "daf_tech_vendor"),
    (r"kindsight|iwave", "Kindsight", "Kindsight", "daf_tech_vendor"),
    (r"donorperfect|softerware", "DonorPerfect", "DonorPerfect", "daf_tech_vendor"),
    (r"advent\s+software|ss&c|\bssc\s+tech", "SS&C (incl. Advent)", "SS&C (incl. Advent)", "investment_accounting_software"),
    (r"clearwater\s+analytics", "Clearwater Analytics", "Clearwater Analytics", "investment_accounting_software"),
    (r"excellence\s+in\s+giving", "Excellence in Giving", "Excellence in Giving", "philanthropic_advisory"),
    (r"philanthrocorp", "PhilanthroCorp", "PhilanthroCorp", "philanthropic_advisory"),
    (r"salesforce|tableau", "Salesforce", "Salesforce", "enterprise_software"),
    (r"microsoft", "Microsoft", "Microsoft", "enterprise_software"),
    (r"workday", "Workday", "Workday", "enterprise_software"),
    (r"netsuite|oracle", "Oracle", "Oracle", "enterprise_software"),
    (r"paypal(?!\s+(charitable|giving))", "PayPal", "PayPal", "payment_processor"),
    (r"stripe", "Stripe", "Stripe", "payment_processor"),
    (r"braintree", "PayPal", "Braintree (PayPal)", "payment_processor"),
    (r"bluesnap", "BlueSnap", "BlueSnap", "payment_processor"),
    (r"frontstream", "FrontStream", "FrontStream", "giving_platform_or_outsourced_admin"),
    (r"mightycause", "Mightycause", "Mightycause", "giving_platform_or_outsourced_admin"),
    (r"civicore", "CiviCore", "CiviCore", "giving_platform_or_outsourced_admin"),
    (r"^gloo\b", "Gloo", "Gloo", "giving_platform_or_outsourced_admin"),
    (r"charitable\s+solutions", "Charitable Solutions", "Charitable Solutions", "giving_platform_or_outsourced_admin"),
    (r"northeast\s+retirement\s+services", "Northeast Retirement Services", "Northeast Retirement Services", "giving_platform_or_outsourced_admin"),
    (r"\bgivegab\b", "GiveGab", "GiveGab", "giving_platform_or_outsourced_admin"),
    (r"total\s+administrative\s+services", "Total Administrative Services Corp (TASC)", "Total Administrative Services Corp (TASC)", "giving_platform_or_outsourced_admin"),
    (r"daf\s*direct", "DAF Direct", "DAF Direct", "payment_processor"),
    (r"charities\s+aid\s+foundation|caf\s+america", "CAF America", "CAF America", "grant_admin_due_diligence"),
    (r"\bcandid\b|guidestar|foundation\s+center", "Candid", "Candid", "charity_data_vendor"),
    (r"\bfmr\b|fidelity", "Fidelity (FMR affiliates)", "Fidelity (FMR affiliates)", "financial_firm"),
    (r"schwab", "Charles Schwab", "Charles Schwab", "financial_firm"),
    (r"vanguard\s+group|^vanguard\b", "Vanguard Group", "Vanguard Group", "financial_firm"),
    (r"goldman|\bayco\b", "Goldman Sachs (incl. Ayco)", "Goldman Sachs (incl. Ayco)", "financial_firm"),
    (r"morgan\s+stanley|graystone", "Morgan Stanley (incl. Graystone)", "Morgan Stanley (incl. Graystone)", "financial_firm"),
    (r"\bubs\b", "UBS", "UBS", "financial_firm"),
    (r"merrill|bank\s+of\s+america|\bbofa\b|u\.?s\.?\s+trust", "Bank of America / Merrill", "Bank of America / Merrill", "financial_firm"),
    (r"j\.?\s*p\.?\s*morgan|jpmorgan|chase\s+bank", "J.P. Morgan", "J.P. Morgan", "financial_firm"),
    (r"wells\s+fargo", "Wells Fargo", "Wells Fargo", "financial_firm"),
    (r"\bbny\b|bank\s+of\s+new\s+york|mellon|pershing", "BNY (incl. Pershing)", "BNY (incl. Pershing)", "financial_firm"),
    (r"northern\s+trust", "Northern Trust", "Northern Trust", "financial_firm"),
    (r"state\s+street", "State Street", "State Street", "financial_firm"),
    (r"raymond\s+james", "Raymond James", "Raymond James", "financial_firm"),
    (r"edward\s+jones", "Edward Jones", "Edward Jones", "financial_firm"),
    (r"ameriprise", "Ameriprise", "Ameriprise", "financial_firm"),
    (r"\blpl\b", "LPL Financial", "LPL Financial", "financial_firm"),
    (r"\bsei\b", "SEI", "SEI", "financial_firm"),
    (r"stifel", "Stifel", "Stifel", "financial_firm"),
    (r"thrivent", "Thrivent", "Thrivent", "financial_firm"),
    (r"\bpnc\b", "PNC", "PNC", "financial_firm"),
    (r"\bu\.?s\.?\s+bank|u\.?s\.?\s+bancorp", "U.S. Bank", "U.S. Bank", "financial_firm"),
    (r"\btruist\b|suntrust|\bbb&t\b", "Truist", "Truist", "financial_firm"),
    (r"blackrock", "BlackRock", "BlackRock", "investment_manager"),
    (r"iconiq", "ICONIQ Capital", "ICONIQ Capital", "investment_manager"),
    (r"cambridge\s+associates", "Cambridge Associates", "Cambridge Associates", "investment_consultant"),
    (r"mercer\b", "Mercer", "Mercer", "investment_consultant"),
    (r"slalom", "Slalom", "Slalom", "technology_services"),
    (r"\bust\s+global|\bust\b", "UST Global", "UST Global", "technology_services"),
    (r"sapient", "Publicis Sapient", "Publicis Sapient", "technology_services"),
    (r"accenture", "Accenture", "Accenture", "technology_services"),
    (r"mckinsey", "McKinsey", "McKinsey", "consulting"),
    (r"deloitte", "Deloitte", "Deloitte", "audit_tax"),
    (r"pricewaterhouse|\bpwc\b", "PwC", "PwC", "audit_tax"),
    (r"ernst\s*&?\s*young|\bey\b", "EY", "EY", "audit_tax"),
    (r"\bkpmg\b", "KPMG", "KPMG", "audit_tax"),
    (r"\brsm\b", "RSM", "RSM", "audit_tax"),
    (r"grant\s+thornton", "Grant Thornton", "Grant Thornton", "audit_tax"),
    (r"\bbdo\b", "BDO", "BDO", "audit_tax"),
    (r"clifton\s*larson|\bcla\b", "CliftonLarsonAllen", "CliftonLarsonAllen", "audit_tax"),
    (r"plante\s*(&|and)?\s*moran", "Plante Moran", "Plante Moran", "audit_tax"),
    (r"baker\s+tilly", "Baker Tilly", "Baker Tilly", "audit_tax"),
    (r"moss\s+adams", "Moss Adams", "Moss Adams", "audit_tax"),
    (r"\bcrowe\b", "Crowe", "Crowe", "audit_tax"),
    (r"marcum", "Marcum", "Marcum", "audit_tax"),
)
COMPILED_RULES = tuple((re.compile(p, re.I), g, e, c) for p, g, e, c in VENDOR_RULES)

SERVICE_CATEGORIES = (
    (r"audit|tax|account", "audit_tax"),
    (r"legal|law|attorney|lobby", "legal"),
    (r"invest|asset\s*man|portfolio|advis|custod|brokerage|wealth|trust\s+serv", "investment_or_financial"),
    (r"software|technolog|\bit\b|systems|data|web|digital|platform|programming|computer", "technology_services"),
    (r"admin|recordkeep|back\s*office|fund\s+serv|donor\s+serv|grant\s+admin|processing", "administration"),
    (r"market|advertis|media|communicat|public\s+rel|design|creative|brand", "marketing_communications"),
    (r"fundrais|campaign|development\s+couns", "fundraising"),
    (r"staff|payroll|personnel|recruit|\bpeo\b|temporary|employ", "staffing"),
    (r"consult", "consulting"),
    (r"construct|build|architect|contractor|engineer|roof|renovat", "construction_facilities"),
    (r"grant|program|scholar|research|medical|clinical|health|educat|service", "program_services"),
)
COMPILED_SERVICES = tuple((re.compile(p, re.I), c) for p, c in SERVICE_CATEGORIES)
NAME_NOISE = re.compile(r"\b(inc|incorporated|llc|l\s*l\s*c|llp|lp|ltd|co|corp|corporation|company|the|na|n\s*a|pllc|pc|plc|dba)\b\.?", re.I)


def clean_name(name: str) -> str:
    base = re.sub(r"\(.*?\)", " ", name or "")
    base = re.sub(r"[^A-Za-z0-9& ]+", " ", base)
    base = NAME_NOISE.sub(" ", base)
    return re.sub(r"\s+", " ", base).strip().upper()


# Bare "Renaissance" / "Stellar" payees are Ren only when the payee address is Ren's home city
# (Ren: 8910 Purdue Rd and 8888 Keystone Crossing, Indianapolis). Elsewhere they stay unmatched,
# so e.g. Renaissance Technologies (an investment manager) is never folded into Ren.
ADDRESS_RULES = (
    (re.compile(r"^renaissance\b(?!\s+charitable)", re.I), "INDIANAPOLIS", "Ren (incl. Stellar/iPhi)", "Ren / RenPSG (bare 'Renaissance', Indianapolis address)", "daf_tech_admin_vendor"),
    (re.compile(r"^stellar\b", re.I), "INDIANAPOLIS", "Ren (incl. Stellar/iPhi)", "Stellar Technology Solutions (iPhi)", "daf_tech_admin_vendor"),
)


def normalize_vendor(name: str, services: str = "", city: str = "") -> dict:
    """Pure. Returns vendor_group / vendor_entity / vendor_category / match_method for a contractor name."""
    hit = next(((g, e, c) for rx, g, e, c in COMPILED_RULES if rx.search(name or "")), None) or \
        next(((g, e, c) for rx, cty, g, e, c in ADDRESS_RULES if rx.search(name or "") and (city or "").upper() == cty), None)
    if hit:
        return {"vendor_group": hit[0], "vendor_entity": hit[1], "vendor_category": hit[2], "match_method": "rule"}
    cat = next((c for rx, c in COMPILED_SERVICES if rx.search(services or "")), "unclassified")
    cleaned = clean_name(name)
    return {"vendor_group": cleaned, "vendor_entity": cleaned, "vendor_category": cat, "match_method": "cleaned_name"}


DAF_VENDOR_CATEGORIES = frozenset({"daf_tech_admin_vendor", "daf_tech_vendor", "payment_processor", "giving_platform_or_outsourced_admin",
                                   "grant_admin_due_diligence", "charity_data_vendor", "enterprise_software"})


# ----------------------------------------------------------------------------- harvest assembly
def fiscal_year(period_end: str, tax_period: str) -> int:
    return int((period_end or tax_period)[:4])


def return_row(sponsor: Mapping, filing: Mapping, ex: Mapping, dafrc_by_key: Mapping | None = None) -> dict:
    fy = fiscal_year(ex.get("tax_period_end", ""), filing["tax_period"])
    d = (dafrc_by_key or {}).get((filing["ein"], fy), {})
    return {"dafrc_eoy_daf_assets_same_fy": num(d.get("eoy_daf_assets")), "dafrc_assets_source_same_fy": d.get("source_eoy_daf_assets", ""),
            **{k: sponsor[k] for k in ("ein", "sponsor_name", "type", "subtype", "fy2024_daf_assets", "fy2024_asset_rank", "selection")},
            "fiscal_year": fiscal_year(ex.get("tax_period_end", ""), filing["tax_period"]),
            "tax_year": ex.get("tax_year", ""), "tax_period": filing["tax_period"],
            "tax_period_end": ex.get("tax_period_end", ""), "return_ts": ex.get("return_ts", ""),
            "return_object_id": filing["object_id"], "return_type": filing["return_type"],
            "amended_ind": ex.get("amended_ind", ""), "xml_status": ex.get("xml_status", ""),
            "filer_name_990": ex.get("filer_name", "") or filing["taxpayer_name"],
            "contractors_listed": len(ex.get("contractors", ()) or ()),
            **{k: ex.get(k) for k in ("contractors_over_100k_cnt", "daf_ind_part_iv", "sched_d_present", "sched_d_daf_count",
                                      "sched_d_daf_contributions", "sched_d_daf_grants", "sched_d_daf_eoy_value",
                                      "part_ix_it_total", "part_ix_fees_other_total", "part_ix_fees_mgmt_total",
                                      "part_ix_fees_invest_total", "total_assets_eoy")},
            "xml_url": XML_URL.format(oid=filing["object_id"]), "index_url": filing["index_url"],
            "source_url": PP_FILING_URL.format(ein=filing["ein"], oid=filing["object_id"])}


def contractor_rows(ret: Mapping, ex: Mapping) -> tuple[dict, ...]:
    return tuple({"ein": ret["ein"], "sponsor_name": ret["sponsor_name"], "sponsor_type": ret["type"],
                  "tax_year": ret["tax_year"], "fiscal_year": ret["fiscal_year"], "tax_period_end": ret["tax_period_end"],
                  "return_object_id": ret["return_object_id"], "contractor_name": c["contractor_name"],
                  "services": c["services"], "compensation": c["compensation"],
                  "contractor_city": c.get("contractor_city", ""), "contractor_state": c.get("contractor_state", ""),
                  **normalize_vendor(c["contractor_name"], c["services"], c.get("contractor_city", "")),
                  "source_url": ret["xml_url"], "filing_page_url": ret["source_url"]}
                 for c in ex.get("contractors", ()) or ())


def coverage_stats(targets: Sequence[Mapping], index: Mapping, returns: Sequence[Mapping]) -> dict:
    eins = tuple(t["ein"] for t in targets)
    ok = tuple(r for r in returns if r["xml_status"] == "ok")
    by_fy = _group_by_fast(ok, lambda r: r["fiscal_year"])
    return {"targets": len(eins), "targets_in_index_any_990": sum(1 for e in eins if any(f["return_type"] == "990" for f in index.get(e, ()))),
            "targets_with_fy2022_25_990_in_index": len({r["ein"] for r in returns}),
            "targets_with_parsed_xml": len({r["ein"] for r in ok}),
            "returns_located": len(returns), "returns_parsed": len(ok),
            "returns_not_mirrored": sum(1 for r in returns if r["xml_status"].startswith("http")),
            "returns_with_contractors": sum(1 for r in ok if r["contractors_listed"]),
            "parsed_by_fiscal_year": {fy: len(v) for fy, v in sorted(by_fy.items())},
            "eins_by_fiscal_year": {fy: len({r['ein'] for r in v}) for fy, v in sorted(by_fy.items())}}


# ----------------------------------------------------------------------------- vendor footprint
def footprint(contractors: Sequence[Mapping], returns: Sequence[Mapping], targets: Sequence[Mapping],
              graph_pairs: frozenset, graph_vendors: frozenset) -> tuple[dict, ...]:
    tmap = {t["ein"]: t for t in targets}
    latest_sd = {e: max(v, key=lambda r: r["fiscal_year"]).get("sched_d_daf_eoy_value")
                 for e, v in _group_by_fast((r for r in returns if r["xml_status"] == "ok" and r.get("sched_d_daf_eoy_value") is not None),
                                            lambda r: r["ein"]).items()}

    def one(group: str, rows: Sequence[Mapping]) -> dict:
        eins = tuple(sorted({r["ein"] for r in rows}))
        new_pairs = tuple(e for e in eins if (group, e) not in graph_pairs)
        return {"vendor": group, "vendor_category": rows[0]["vendor_category"],
                "vendor_entities": " | ".join(sorted({r["vendor_entity"] for r in rows})),
                "sponsors_paying": len(eins),
                "sponsor_names": " | ".join(sorted({tmap[e]["sponsor_name"] for e in eins})),
                "sponsor_eins": " ".join(eins),
                "total_compensation": sum(r["compensation"] or 0 for r in rows),
                "max_annual_compensation_one_sponsor": max((r["compensation"] or 0) for r in rows),
                "contractor_lines": len(rows),
                "sponsor_daf_assets_fy2024_dafrc": sum(tmap[e]["fy2024_daf_assets"] or 0 for e in eins),
                "sponsor_daf_assets_latest_990_sched_d": sum(latest_sd.get(e) or 0 for e in eins),
                "tax_years": " ".join(sorted({str(r["tax_year"]) for r in rows})),
                "fiscal_years": " ".join(sorted({str(r["fiscal_year"]) for r in rows})),
                "raw_names_seen": " | ".join(sorted({r["contractor_name"] for r in rows}))[:600],
                "services_seen": " | ".join(sorted({r["services"] for r in rows}))[:400],
                "vendor_in_existing_graph": int(group in graph_vendors),
                "sponsor_links_not_in_graph": len(new_pairs) if rows[0]["match_method"] == "rule" else "",
                "new_link_sponsors": " | ".join(tmap[e]["sponsor_name"] for e in new_pairs) if rows[0]["match_method"] == "rule" else ""}

    groups = _group_by_fast(contractors, lambda r: r["vendor_group"])
    out = tuple(one(g, v) for g, v in groups.items())
    return tuple(sorted(out, key=lambda r: (-(r["sponsors_paying"]), -r["total_compensation"])))


# ----------------------------------------------------------------------------- graph comparison
SPONSOR_STOP = frozenset("inc the of fund funds foundation charitable charity gift giving program trust endowment "
                         "community and for donor advised daf corp corporation co llc".split())
# Graph sponsor labels whose wording shares no distinctive token with the DAFRC legal name.
GRAPH_SPONSOR_ALIASES = {"DAFgiving360": "311640316", "Schwab Charitable": "311640316",
                         "Fidelity Charitable": "110303001", "Vanguard Charitable": "232888152",
                         "ImpactAssets": "262048480", "Thrivent Charitable": "411802412",
                         "National Philanthropic Trust": "237825575", "NPT": "237825575",
                         "National Christian Foundation": "581493949"}


def sponsor_tokens(name: str) -> frozenset[str]:
    return frozenset(t for t in re.findall(r"[a-z0-9]+", (name or "").lower()) if t not in SPONSOR_STOP and len(t) > 1)


def graph_links(edge_paths: Sequence[str], targets: Sequence[Mapping]) -> tuple[frozenset, frozenset, tuple]:
    """Map existing graph edges to (vendor_group, sponsor_ein) pairs via the same normaliser plus
    sponsor-name token matching. Returns (pairs, vendor_groups_in_graph, unmatched_sponsor_names)."""
    edges = tuple(e for p in edge_paths if os.path.exists(p) for e in read_csv(p))
    tok = {t["ein"]: sponsor_tokens(t["sponsor_name"]) for t in targets}

    def ein_for(name: str) -> str | None:
        if name in GRAPH_SPONSOR_ALIASES and GRAPH_SPONSOR_ALIASES[name] in tok:
            return GRAPH_SPONSOR_ALIASES[name]
        nt = sponsor_tokens(re.sub(r"\(.*?\)", " ", name))   # drop '(dba ...)' / '(unconfirmed)' qualifiers
        scored = sorted(((len(nt & v) / len(nt | v), e) for e, v in tok.items() if nt and v and (nt <= v or v <= nt or len(nt & v) >= 2)), reverse=True)
        return scored[0][1] if scored and scored[0][0] >= 0.5 else None

    def vendor_side(e: Mapping) -> tuple[str, str] | None:
        for s, st, o in (("source_entity", "source_type", "target_entity"), ("target_entity", "target_type", "source_entity")):
            nv = normalize_vendor(e[s])
            if nv["match_method"] == "rule" and e[st] != "daf_sponsor":
                return nv["vendor_group"], e[o]
        return None

    sides = tuple(v for v in map(vendor_side, edges) if v)
    pairs = frozenset((g, ein_for(s)) for g, s in sides if ein_for(s))
    return pairs, frozenset(g for g, _ in sides), tuple(sorted({s for g, s in sides if not ein_for(s)}))


# ----------------------------------------------------------------------------- DAFRC processing gaps
def gap_universe(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    """Sponsor-years to test: (a) every FY after a DAFRC 'Assume Sponsor Closed' EIN's last panel row
    up to FY2024; (b) every imputed row in GAP_FYS."""
    by = _group_by_fast(rows, lambda r: r["ein"])

    def last_filed(v):
        f = [r for r in v if r["source_eoy_daf_assets"] in FILED_SOURCES and (num(r["eoy_daf_assets"]) or 0) > 0]
        return max(f, key=lambda r: r["fy"]) if f else None

    closed = tuple({"ein": e, "name": v[0]["name"], "type": v[0]["type"], "subtype": v[0]["subtype"], "dafrc_fy": fy,
                    "gap_kind": "dafrc_closed_no_row", "dafrc_operating_status": v[-1]["operating_status"],
                    "dafrc_eoy_daf_assets": None, "dafrc_daf_accounts": None,
                    "last_filed_fy": (last_filed(v) or {}).get("fy"),
                    "last_filed_daf_assets": num((last_filed(v) or {}).get("eoy_daf_assets"))}
                   for e, v in by.items() if "Closed" in v[-1]["operating_status"]
                   for fy in range(max(r["fy"] for r in v) + 1, 2025))
    imputed = tuple({"ein": r["ein"], "name": r["name"], "type": r["type"], "subtype": r["subtype"], "dafrc_fy": r["fy"],
                     "gap_kind": "dafrc_imputed_row", "dafrc_operating_status": r["operating_status"],
                     "dafrc_eoy_daf_assets": num(r["eoy_daf_assets"]), "dafrc_daf_accounts": num(r["number_of_daf_accounts"]),
                     "dafrc_end_of_tax_period": r["end_of_tax_period"],
                     "last_filed_fy": (last_filed([x for x in by[r["ein"]] if x["fy"] < r["fy"]]) or {}).get("fy"),
                     "last_filed_daf_assets": num((last_filed([x for x in by[r["ein"]] if x["fy"] < r["fy"]]) or {}).get("eoy_daf_assets"))}
                    for r in rows if r["source_eoy_daf_assets"] == "Imputed" and r["fy"] in GAP_FYS)
    return closed + imputed


def classify_gap(g: Mapping, f990: Mapping | None, other: Mapping | None, ex: Mapping) -> str:
    if f990 is None:
        return "no_990_in_irs_index" + (f"_filed_{other['return_type']}" if other else "")
    if ex.get("xml_status") != "ok":
        return "990_in_index_xml_not_mirrored"
    cnt, val = ex.get("sched_d_daf_count") or 0, ex.get("sched_d_daf_eoy_value") or 0
    pre = "closed" if g["gap_kind"] == "dafrc_closed_no_row" else "imputed"
    if val > 0:
        return f"{pre}_but_990_reports_daf_value"
    if cnt > 0:
        return f"{pre}_990_reports_daf_count_value_blank_or_zero"
    return f"{pre}_990_filed_no_dafs"


def implausible_count(cnt: float | None, val: float | None) -> int:
    """Flag Schedule D counts that look like dollar amounts keyed into the count box:
    > 1m accounts, > 100k accounts with no value, or < $100 average value per account."""
    c, v = cnt or 0, val or 0
    return int(c > 1_000_000 or (v > 0 and c > 0 and v / c < 100) or (v == 0 and c > 100_000))


def gap_row(g: Mapping, index: Mapping, extracts: Mapping) -> dict:
    fl = index.get(g["ein"], ())
    f990 = latest_for_fy(fl, g["dafrc_fy"], ("990",))
    other = latest_for_fy(fl, g["dafrc_fy"], ("990EZ", "990PF"))
    ex = extracts.get(f990["object_id"], {}) if f990 else {}
    cls = classify_gap(g, f990, other, ex)
    filed_v = ex.get("sched_d_daf_eoy_value")
    ts = ex.get("return_ts", "")[:10]
    return {**g, "return_object_id": (f990 or {}).get("object_id", ""), "tax_period": (f990 or {}).get("tax_period", ""),
            "tax_period_end": ex.get("tax_period_end", ""), "return_ts": ts,
            "index_year": (f990 or {}).get("index_year", ""), "xml_status": ex.get("xml_status", ""),
            "other_return_type_same_fy": (other or {}).get("return_type", ""),
            "filed_daf_count": ex.get("sched_d_daf_count"), "filed_daf_eoy_value": filed_v,
            "filed_daf_contributions": ex.get("sched_d_daf_contributions"), "filed_daf_grants": ex.get("sched_d_daf_grants"),
            "gap_class": cls,
            "implausible_daf_count_flag": implausible_count(ex.get("sched_d_daf_count"), filed_v),
            "submitted_before_2026": (int(ts < "2026-01-01") if ts else ""),
            "value_delta_filed_minus_dafrc": (filed_v - (g["dafrc_eoy_daf_assets"] or 0)) if filed_v is not None else None,
            "source_urls": " ; ".join(filter(None, (DAFRC_URL, (f990 or {}).get("index_url"),
                                                     XML_URL.format(oid=f990["object_id"]) if f990 else "")))}


def gap_summary(rows: Sequence[Mapping]) -> tuple[dict, ...]:
    def agg(key_fn):
        return {k: {"n": len(v), "eins": len({r["ein"] for r in v}),
                    "dafrc_value": sum(r["dafrc_eoy_daf_assets"] or 0 for r in v),
                    "filed_value": sum(r["filed_daf_eoy_value"] or 0 for r in v),
                    "filed_accounts": sum(r["filed_daf_count"] or 0 for r in v)}
                for k, v in sorted(_group_by_fast(rows, key_fn).items(), key=lambda kv: str(kv[0]))}
    return ({"by_kind_fy_class": agg(lambda r: (r["gap_kind"], r["dafrc_fy"], r["gap_class"]))},)


# ----------------------------------------------------------------------------- P-990-05: new graph edges from Part VII-B
DAF_SPECIALIST_GROUPS = frozenset({"Ren (incl. Stellar/iPhi)", "Foundation Source", "Give Interactive", "TIFIN", "Foundant Technologies",
                                   "NPact", "CSuite (CommunitySuite)", "Crown Philanthropic Solutions", "Pinkaloo", "Groundswell",
                                   "Chariot", "DAF Direct", "CAF America"})
EDGE_TYPES = {"daf_tech_admin_vendor": ("technology_admin_vendor", "technology_provider"),
              "daf_tech_vendor": ("technology_vendor", "technology_provider"),
              "payment_processor": ("payment_processor", "payment_processor"),
              "giving_platform_or_outsourced_admin": ("administrator", "technology_provider"),
              "grant_admin_due_diligence": ("charity_data_vendor", "charity_verification"),
              "charity_data_vendor": ("charity_data_vendor", "charity_verification")}
OUTSOURCED_ADMIN_SERVICE = re.compile(r"admin|donor\s+serv|fd\s+acct|fund\s+acc|managed\s+serv|grant\s+process|ops\s+system|"
                                      r"operational|donor\s+account|grant\s+admin|fiduciary|unitization|fund\s+accounting", re.I)
GRAPH_VENDOR_LABEL = {"Ren (incl. Stellar/iPhi)": "Ren", "TIFIN": "TIFIN Give", "Bonterra (CyberGrants/Network for Good)": "Bonterra",
                      "Total Administrative Services Corp (TASC)": "Total Administrative Services Corp (TASC)"}


def edge_eligible(c: Mapping) -> bool:
    """DAF-specialist vendors at any sponsor; general donor-tech / payments vendors only at National and Community
    sponsors (at universities and hospitals they evidence fundraising CRM, not DAF administration). Pure."""
    if c["match_method"] != "rule" or c["vendor_category"] not in EDGE_TYPES:
        return False
    return c["vendor_group"] in DAF_SPECIALIST_GROUPS or c["vendor_category"] in ("daf_tech_admin_vendor", "giving_platform_or_outsourced_admin") \
        or c["sponsor_type"] in ("National", "Community Foundation")


ENTITY_LABEL = {"Stellar Technology Solutions (iPhi)": "Stellar Technology Solutions (iPhi)"}


def edge_rows(contractors: Sequence[Mapping], pairs: frozenset, names: Mapping | None = None,
              accessed: str = "2026-11-14", prefix: str = "EC") -> tuple[dict, ...]:
    """One edge per (vendor group, sponsor EIN) Part VII-B relationship absent from the existing graph. Status is
    'confirmed' because the filed 990 names the vendor as payee; ordering by sponsor DAF assets is not used. Pure."""
    elig = tuple(c for c in contractors if edge_eligible(c) and (c["vendor_group"], c["ein"]) not in pairs)
    groups = sorted(_group_by_fast(elig, lambda c: (c["vendor_group"], c["ein"])).items(),
                    key=lambda kv: (kv[0][0], -sum(float(c["compensation"] or 0) for c in kv[1])))

    def one(i, key, cs):
        latest = max(cs, key=lambda c: (int(c["fiscal_year"]), float(c["compensation"] or 0)))
        src_type, rel = EDGE_TYPES[latest["vendor_category"]]
        if latest["vendor_category"] in ("daf_tech_admin_vendor", "giving_platform_or_outsourced_admin") \
                and OUTSOURCED_ADMIN_SERVICE.search(latest["services"]):
            rel = "administers"
        by_fy = sorted({(int(c["fiscal_year"]), c["contractor_name"].strip(), c["services"].strip(), float(c["compensation"] or 0)) for c in cs})
        amounts = "; ".join(f"FY{fy} {nm} '{sv}' ${amt:,.0f}" for fy, nm, sv, amt in by_fy)
        return {"edge_id": f"{prefix}{i:03d}",
                "source_entity": ENTITY_LABEL.get(latest["vendor_entity"]) or GRAPH_VENDOR_LABEL.get(key[0], key[0]), "source_type": src_type,
                "target_entity": (names or {}).get(key[1]) or latest["sponsor_name"], "target_type": "daf_sponsor", "relationship_type": rel, "status": "confirmed",
                "evidence_summary": f"Form 990 Part VII-B (EIN {key[1]}) names payee: {amounts}"[:900],
                "source_url": latest["source_url"], "source_date": f"FY{latest['fiscal_year']} (tax period end {latest['tax_period_end']})",
                "accessed_date": accessed,
                "notes": (f"Vendor group: {key[0]}; entities seen: {' / '.join(sorted({c['vendor_entity'] for c in cs}))}. "
                          f"DAFRC name: {latest['sponsor_name']}; DAFRC type: {latest['sponsor_type']}. Filing page: {latest['filing_page_url']}. "
                          "Part VII-B lists only the five largest contractors >$100k, so scope and absence elsewhere are not implied.")}
    return tuple(one(i + 1, k, v) for i, (k, v) in enumerate(groups))


EDGE_FIELDS = ("edge_id", "source_entity", "source_type", "target_entity", "target_type", "relationship_type", "status",
               "evidence_summary", "source_url", "source_date", "accessed_date", "notes")


# ----------------------------------------------------------------------------- P-MOR-01: DAF filers outside DAFRC
SOI_URL = "https://www.irs.gov/pub/irs-soi/{yy}eoextract990.zip"
SOI_PAGE = "https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data"
SOI_YEARS = (20, 21, 22, 23, 24, 25)               # SOI extract (processing) years 2020..2025
OUTSIDE_FYS = tuple(range(2020, 2026))
OUTSIDE_INDEX_YEARS = tuple(range(2020, 2027))


def ensure_soi(soi_dir: str, fetch: bool) -> tuple[str, ...]:
    """Locate (and with --fetch download/unzip) the IRS SOI annual Form 990 extracts."""
    import zipfile
    os.makedirs(soi_dir, exist_ok=True)
    out = []
    for yy in SOI_YEARS:
        csv_p, zip_p = (os.path.join(soi_dir, f"{yy}eoextract990.{x}") for x in ("csv", "zip"))
        if not os.path.exists(csv_p) and not os.path.exists(zip_p) and fetch:
            print(f"downloading {SOI_URL.format(yy=yy)}", file=sys.stderr)
            urllib.request.urlretrieve(SOI_URL.format(yy=yy), zip_p)
        if not os.path.exists(csv_p) and os.path.exists(zip_p):
            with zipfile.ZipFile(zip_p) as z:
                z.extract(next(n for n in z.namelist() if n.lower().endswith(".csv")), soi_dir)
        if os.path.exists(csv_p):
            out.append(csv_p)
    return tuple(out)


def soi_yes_rows(paths: Sequence[str], fys: Sequence[int] = OUTSIDE_FYS) -> tuple[dict, ...]:
    """Every SOI extract row answering Part IV line 6 (dnradvisedfundscd) 'Y' for a tax period ending in fys.
    One row per (EIN, tax_pd); a later processing-year extract supersedes an earlier one."""
    def rows(p):
        yy = re.search(r"(\d{2})eoextract990", os.path.basename(p)).group(1)
        with open(p, newline="", encoding="latin-1") as fh:
            rd = csv.reader(fh)
            hdr = [h.replace("\ufeff", "").replace("\xef\xbb\xbf", "").strip().lower() for h in next(rd)]
            ix = {h: i for i, h in enumerate(hdr)}
            for r in rd:
                if len(r) > ix["dnradvisedfundscd"] and r[ix["dnradvisedfundscd"]] == "Y" and r[ix["tax_pd"]][:4].isdigit() \
                        and int(r[ix["tax_pd"]][:4]) in fys:
                    yield {"ein": ein9(r[ix["ein"]]), "tax_pd": r[ix["tax_pd"]], "fiscal_year": int(r[ix["tax_pd"]][:4]),
                           "soi_extract_year": 2000 + int(yy), "soi_total_assets_eoy": num(r[ix["totassetsend"]]),
                           "soi_url": SOI_URL.format(yy=yy)}
    allr = tuple(r for p in sorted(paths) for r in rows(p))
    return tuple({(r["ein"], r["tax_pd"]): r for r in allr}.values())


def outside_status(ex: Mapping) -> str:
    if ex.get("xml_status") != "ok":
        return "xml_" + (ex.get("xml_status") or "missing")
    v, c = ex.get("sched_d_daf_eoy_value") or 0, ex.get("sched_d_daf_count") or 0
    if implausible_count(ex.get("sched_d_daf_count"), ex.get("sched_d_daf_eoy_value")):
        return "reports_daf_data_implausible"
    if v > 0:
        return "reports_daf_value"
    if c > 0:
        return "reports_daf_count_value_blank_or_zero"
    if (ex.get("sched_d_other_funds_eoy_value") or 0) > 0 or (ex.get("sched_d_other_funds_count") or 0) > 0:
        return "flag_yes_other_funds_column_only"
    return "flag_yes_but_no_sched_d_daf_data"


def outside_row(y: Mapping, filing: Mapping | None, ex: Mapping, bmf_name: str) -> dict:
    v = ex.get("sched_d_daf_eoy_value")
    ta = ex.get("total_assets_eoy") or y["soi_total_assets_eoy"]
    return {**y, "name": ex.get("filer_name") or (filing or {}).get("taxpayer_name") or bmf_name,
            "return_object_id": (filing or {}).get("object_id", ""), "index_year": (filing or {}).get("index_year", ""),
            "return_ts": (ex.get("return_ts") or "")[:10], "daf_ind_part_iv_xml": ex.get("daf_ind_part_iv", ""),
            "sched_d_daf_count": ex.get("sched_d_daf_count"), "sched_d_daf_contributions": ex.get("sched_d_daf_contributions"),
            "sched_d_daf_grants": ex.get("sched_d_daf_grants"), "sched_d_daf_eoy_value": v,
            "sched_d_other_funds_count": ex.get("sched_d_other_funds_count"),
            "sched_d_other_funds_eoy_value": ex.get("sched_d_other_funds_eoy_value"),
            "total_assets_eoy": ta, "daf_value_share_of_total_assets": (v / ta) if v and ta else None,
            "status": outside_status(ex) if filing else "no_990_object_in_irs_index",
            "xml_url": XML_URL.format(oid=filing["object_id"]) if filing else "",
            "index_url": (filing or {}).get("index_url", "")}


def outside_summary(rows: Sequence[Mapping], dafrc: Sequence[Mapping], soi_in: Sequence[Mapping]) -> tuple[dict, ...]:
    """Per fiscal year: non-DAFRC 'Y' filers and their Schedule D DAF totals vs the DAFRC panel."""
    d_by_fy = _group_by_fast(dafrc, lambda r: r["fy"])
    in_by_fy = _group_by_fast(soi_in, lambda r: r["fiscal_year"])

    def one(fy, rs):
        val = tuple(r for r in rs if r["status"] == "reports_daf_value")
        big = tuple(r for r in val if (r["sched_d_daf_eoy_value"] or 0) >= 1e9)
        d = d_by_fy.get(fy, ())
        d_tot = sum(num(r["eoy_daf_assets"]) or 0 for r in d)
        v = sum(r["sched_d_daf_eoy_value"] or 0 for r in val)
        return {"fiscal_year": fy, "soi_yes_returns_dafrc_eins": len(in_by_fy.get(fy, ())),
                "soi_yes_returns_non_dafrc": len(rs),
                **{f"n_{k}": sum(1 for r in rs if r["status"] == k) for k in
                   ("reports_daf_value", "reports_daf_count_value_blank_or_zero", "reports_daf_data_implausible",
                    "flag_yes_other_funds_column_only", "flag_yes_but_no_sched_d_daf_data", "no_990_object_in_irs_index")},
                "n_xml_not_mirrored": sum(1 for r in rs if r["status"].startswith("xml_")),
                "non_dafrc_daf_assets": v, "non_dafrc_daf_accounts": sum(r["sched_d_daf_count"] or 0 for r in val),
                "non_dafrc_daf_contributions": sum(r["sched_d_daf_contributions"] or 0 for r in val),
                "non_dafrc_daf_grants": sum(r["sched_d_daf_grants"] or 0 for r in val),
                "non_dafrc_daf_assets_excl_ge_1bn": v - sum(r["sched_d_daf_eoy_value"] or 0 for r in big),
                "filers_ge_1bn": " | ".join(f"{r['name']} ({r['ein']}) {r['sched_d_daf_eoy_value']:.0f}" for r in big),
                "dafrc_sponsors_fy": len(d), "dafrc_daf_assets_fy": d_tot,
                "non_dafrc_assets_pct_of_dafrc": (v / d_tot) if d_tot else None,
                "fy_complete_in_soi": int(fy <= 2023)}
    return tuple(one(fy, rs) for fy, rs in sorted(_group_by_fast(rows, lambda r: r["fiscal_year"]).items()))


OUTSIDE_FIELDS = ("ein", "name", "fiscal_year", "tax_pd", "soi_extract_year", "status", "sched_d_daf_count",
                  "sched_d_daf_contributions", "sched_d_daf_grants", "sched_d_daf_eoy_value", "sched_d_other_funds_count",
                  "sched_d_other_funds_eoy_value", "total_assets_eoy",
                  "daf_value_share_of_total_assets", "daf_ind_part_iv_xml", "return_object_id", "return_ts", "index_year",
                  "soi_total_assets_eoy", "xml_url", "index_url", "soi_url")
OUTSIDE_SUMMARY_FIELDS = ("fiscal_year", "fy_complete_in_soi", "soi_yes_returns_dafrc_eins", "soi_yes_returns_non_dafrc",
                          "n_reports_daf_value", "n_reports_daf_count_value_blank_or_zero", "n_reports_daf_data_implausible",
                          "n_flag_yes_other_funds_column_only", "n_flag_yes_but_no_sched_d_daf_data", "n_no_990_object_in_irs_index", "n_xml_not_mirrored",
                          "non_dafrc_daf_assets", "non_dafrc_daf_assets_excl_ge_1bn", "non_dafrc_daf_accounts",
                          "non_dafrc_daf_contributions", "non_dafrc_daf_grants", "dafrc_sponsors_fy", "dafrc_daf_assets_fy",
                          "non_dafrc_assets_pct_of_dafrc", "filers_ge_1bn")


def run_outside(dafrc, irs_dir, soi_dir, cache_dir, fetch, out_dir) -> dict:
    d_eins = frozenset(r["ein"] for r in dafrc)
    yes = soi_yes_rows(ensure_soi(soi_dir, fetch))
    soi_in = tuple(r for r in yes if r["ein"] in d_eins)
    out = tuple(r for r in yes if r["ein"] not in d_eins)
    idx_paths = tuple(p for p in (os.path.join(irs_dir, f"index_{y}.csv") for y in OUTSIDE_INDEX_YEARS) if os.path.exists(p))
    index = load_index(idx_paths, frozenset(r["ein"] for r in out))
    pick = {(r["ein"], r["tax_pd"]): next((f for f in reversed(index.get(r["ein"], ()))
                                           if f["return_type"] == "990" and f["tax_period"] == r["tax_pd"]), None) for r in out}
    ex = fetch_all(tuple(f["object_id"] for f in pick.values() if f), cache_dir, fetch)
    rows = tuple(outside_row(r, pick[(r["ein"], r["tax_pd"])], ex.get((pick[(r["ein"], r["tax_pd"])] or {}).get("object_id"), {}), "")
                 for r in out)
    summ = outside_summary(rows, dafrc, soi_in)
    write_csv(os.path.join(out_dir, "non-dafrc-daf-filers-990.csv"),
              sorted(rows, key=lambda r: (-r["fiscal_year"], -(r["sched_d_daf_eoy_value"] or 0))), OUTSIDE_FIELDS)
    write_csv(os.path.join(out_dir, "non-dafrc-daf-filers-summary.csv"), summ, OUTSIDE_SUMMARY_FIELDS)
    dafrc_fy = {(r["ein"], r["fy"]) for r in dafrc}
    return {"soi_yes_rows": len(yes), "soi_yes_dafrc_ein_rows": len(soi_in), "soi_yes_non_dafrc_rows": len(out),
            "non_dafrc_eins": len({r["ein"] for r in out}),
            "dafrc_fy2020_2024_rows_flagged_yes_same_fy": sum(1 for r in soi_in if (r["ein"], r["fiscal_year"]) in dafrc_fy),
            "by_fy": summ}


# ----------------------------------------------------------------------------- orchestration
HARVEST_FIELDS = ("ein", "sponsor_name", "sponsor_type", "tax_year", "fiscal_year", "tax_period_end", "return_object_id",
                  "contractor_name", "services", "compensation", "contractor_city", "contractor_state",
                  "vendor_group", "vendor_entity", "vendor_category", "match_method", "source_url", "filing_page_url")
RETURN_FIELDS = ("ein", "sponsor_name", "type", "subtype", "selection", "fy2024_asset_rank", "fy2024_daf_assets", "fiscal_year",
                 "tax_year", "tax_period", "tax_period_end", "return_ts", "return_object_id", "return_type", "amended_ind",
                 "xml_status", "filer_name_990", "contractors_listed", "contractors_over_100k_cnt", "daf_ind_part_iv",
                 "sched_d_present", "sched_d_daf_count", "sched_d_daf_contributions", "sched_d_daf_grants", "sched_d_daf_eoy_value",
                 "part_ix_it_total", "part_ix_fees_other_total", "part_ix_fees_mgmt_total", "part_ix_fees_invest_total",
                 "total_assets_eoy", "dafrc_eoy_daf_assets_same_fy", "dafrc_assets_source_same_fy", "xml_url", "index_url", "source_url")
FOOTPRINT_FIELDS = ("vendor", "vendor_category", "vendor_entities", "sponsors_paying", "total_compensation",
                    "max_annual_compensation_one_sponsor", "contractor_lines", "sponsor_daf_assets_fy2024_dafrc",
                    "sponsor_daf_assets_latest_990_sched_d", "tax_years", "fiscal_years", "sponsor_names", "sponsor_eins",
                    "vendor_in_existing_graph", "sponsor_links_not_in_graph", "new_link_sponsors", "raw_names_seen", "services_seen")
GAP_FIELDS = ("ein", "name", "type", "subtype", "gap_kind", "dafrc_fy", "dafrc_operating_status", "dafrc_end_of_tax_period",
              "dafrc_eoy_daf_assets", "dafrc_daf_accounts", "last_filed_fy", "last_filed_daf_assets", "gap_class",
              "return_object_id", "tax_period", "tax_period_end", "return_ts", "submitted_before_2026", "index_year",
              "xml_status", "other_return_type_same_fy", "filed_daf_count", "filed_daf_eoy_value", "filed_daf_contributions",
              "filed_daf_grants", "implausible_daf_count_flag", "value_delta_filed_minus_dafrc", "source_urls")
UNIVERSE_FIELDS = ("ein", "sponsor_name", "type", "subtype", "selection", "fy2024_asset_rank", "fy2024_daf_assets",
                   "fy2024_assets_source", "returns_fy2022_2025_in_index", "returns_parsed", "fiscal_years_parsed")


def out_names(tag: str, footprint_name: str = "") -> dict:
    """File names for a harvest run. tag '' reproduces the original top-250 names; a tag such as
    '-full' writes side-by-side files so earlier outputs are not overwritten. Pure."""
    return {"harvest": f"form990-contractors-harvest{tag}.csv", "returns": f"form990-returns-schedule-d-harvest{tag}.csv",
            "universe": f"form990-harvest-sponsor-universe{tag}.csv",
            "footprint": footprint_name or f"vendor-footprint-from-990{tag}.csv",
            "edges": EDGES_OUT if tag == "-full" else ""}


def run_contractors(dafrc, index, cache_dir, fetch, n_total, out_dir, names: Mapping | None = None) -> dict:
    names = names or out_names("")
    targets = select_targets(dafrc, n_total)
    filings = tuple((t, f) for t in targets for f in latest_per_period(index.get(t["ein"], ()), HARVEST_FYS))
    ex = fetch_all(tuple(f["object_id"] for _, f in filings), cache_dir, fetch)
    dkey = {(r["ein"], r["fy"]): r for r in dafrc}
    returns = tuple(return_row(t, f, ex[f["object_id"]], dkey) for t, f in filings)
    contractors = tuple(c for (t, f), r in zip(filings, returns) for c in contractor_rows(r, ex[f["object_id"]]))
    pairs, gvendors, unmatched = graph_links(GRAPH_EDGES, targets)
    fp = footprint(contractors, returns, targets, pairs, gvendors)
    by_ein = _group_by_fast(returns, lambda r: r["ein"])
    universe = tuple({**t, "returns_fy2022_2025_in_index": len(by_ein.get(t["ein"], ())),
                      "returns_parsed": sum(1 for r in by_ein.get(t["ein"], ()) if r["xml_status"] == "ok"),
                      "fiscal_years_parsed": " ".join(sorted({str(r["fiscal_year"]) for r in by_ein.get(t["ein"], ()) if r["xml_status"] == "ok"}))}
                     for t in targets)
    write_csv(os.path.join(out_dir, names["harvest"]),
              sorted(contractors, key=lambda r: (r["sponsor_name"], -int(r["fiscal_year"]), -(r["compensation"] or 0))), HARVEST_FIELDS)
    write_csv(os.path.join(out_dir, names["returns"]),
              sorted(returns, key=lambda r: (r["fy2024_asset_rank"], -r["fiscal_year"])), RETURN_FIELDS)
    write_csv(os.path.join(out_dir, names["universe"]), universe, UNIVERSE_FIELDS)
    write_csv(os.path.join(out_dir, names["footprint"]), fp, FOOTPRINT_FIELDS)
    if names.get("edges"):
        names990 = {e: max(v, key=lambda r: r["fiscal_year"])["filer_name_990"] for e, v in by_ein.items()}
        edges = edge_rows(tuple({**c, "compensation": c["compensation"] or 0} for c in contractors), pairs, names990)
        write_csv(os.path.join(out_dir, names["edges"]), edges, EDGE_FIELDS)
    return {"coverage": coverage_stats(targets, index, returns), "graph_sponsors_unmatched": unmatched,
            "graph_pairs_matched": len(pairs), "contractor_lines": len(contractors)}


def run_gaps(dafrc, index, cache_dir, fetch, out_dir) -> dict:
    uni = gap_universe(dafrc)
    want = tuple(f["object_id"] for g in uni for f in (latest_for_fy(index.get(g["ein"], ()), g["dafrc_fy"], ("990",)),) if f)
    ex = fetch_all(want, cache_dir, fetch)
    rows = tuple(gap_row(g, index, ex) for g in uni)
    write_csv(os.path.join(out_dir, "dafrc-processing-gaps.csv"),
              sorted(rows, key=lambda r: (r["gap_kind"], r["dafrc_fy"], -(r["filed_daf_eoy_value"] or 0))), GAP_FIELDS)
    return gap_summary(rows)[0]


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--irs-dir", required=True)
    ap.add_argument("--cache-dir", default=os.path.expanduser("~/.cache/daf-landscape"))
    ap.add_argument("--fetch", action="store_true")
    ap.add_argument("--task", choices=("contractors", "gaps", "outside", "all"), default="all")
    ap.add_argument("--soi-dir", default="", help="dir for IRS SOI {yy}eoextract990.csv (task outside); default <irs-dir>/../soi")
    ap.add_argument("--n-sponsors", type=int, default=250, help="0 = every FY2024 DAFRC sponsor")
    ap.add_argument("--out-tag", default="", help="suffix for harvest output files, e.g. -full")
    ap.add_argument("--footprint-name", default="", help="override vendor footprint file name")
    ap.add_argument("--out-dir", default=DATA)
    ap.add_argument("--summary-json", default="")
    a = ap.parse_args(argv)
    dafrc = load_dafrc()
    eins = frozenset(r["ein"] for r in dafrc)
    if a.task == "outside":
        summary = {"outside": run_outside(dafrc, a.irs_dir, a.soi_dir or os.path.join(os.path.dirname(os.path.abspath(a.irs_dir)), "soi"),
                                          a.cache_dir, a.fetch, a.out_dir)}
        txt = json.dumps(summary, indent=1, default=str)
        print(txt)
        if a.summary_json:
            with open(a.summary_json, "w", encoding="utf-8") as fh:
                fh.write(txt)
        return 0
    index = load_index(ensure_indexes(a.irs_dir, a.fetch), eins)
    summary = {**({"contractors": run_contractors(dafrc, index, a.cache_dir, a.fetch, a.n_sponsors, a.out_dir,
                                                             out_names(a.out_tag, a.footprint_name))}
                  if a.task in ("contractors", "all") else {}),
               **({"gaps": {str(k): v for k, v in run_gaps(dafrc, index, a.cache_dir, a.fetch, a.out_dir)["by_kind_fy_class"].items()}}
                  if a.task in ("gaps", "all") else {})}
    txt = json.dumps(summary, indent=1, default=str)
    print(txt)
    if a.summary_json:
        with open(a.summary_json, "w", encoding="utf-8") as fh:
            fh.write(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
