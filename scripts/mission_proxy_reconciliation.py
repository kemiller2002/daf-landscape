#!/usr/bin/env python3
"""Proxy reconciliation and parent-paid marketing (task b4427-03-b43n23): queue items P-B4427-03 and P-B43N23-01.

Stdlib only; functional style (pure transforms; file reads and the one CSV write sit at the edges).

(A) P-B4427-03 - reconcile the 990 balance-sheet proxy dR1 with audited fee margins at the five sponsors where both
    exist (Fidelity Charitable, Renaissance/RCF, NCF, JCF, CJP), FY2023 and FY2024 (FY = year the period ends).
    R1 = Form 990 Part X line 32 total net assets - Schedule D Part I line 4 column (a) DAF value (EOY), as in
    direction-sponsor-financial-resilience.md; dR1 = R1(t) - R1(t-1), each year from its own return.
    Sequential decomposition, every term read from the e-file XML except c4:
      c1  growth of Schedule D Part I column (b) "funds and other accounts" EOY value;
      c2  Schedule D Part V current-year endowment investment earnings (line 1c), counted only when the Part V
          endowment is NOT already the column (b) fund (EOY balances equal); otherwise reported as a memo;
      c3  change in Part X line 10c net PP&E;
      c4  the audited fee surplus as recorded in sponsor-fee-revenue-margin-2026-11-19.csv with the wave-38B
          corrections: Fidelity and RCF fee - opex; JCF fee - opex - the $2.0m operating-fund grant to UJA;
          NCF fee (NCCF column) - NCCF's own 990 operating cost; CJP not computable (0, flagged);
      residual = dR1 - (c1 + c2 + c3 + c4).
    Audit anchors locate the residual (e.g. JCF's reserve fund, NCF's operating net assets, CJP's functional
    areas). Each anchor figure is checked verbatim (label and numbers on one line) in the pdftotext output.

(B) P-B43N23-01 - who pays for marketing at the affiliated-commercial nationals (Fidelity, Schwab/DAFgiving360,
    Vanguard, Goldman Sachs [GS DAPF and GS Charitable Gift Fund], Morgan Stanley GIFT, BofA Charitable Gift Fund,
    Raymond James), TY2021-2024 returns (FY2022-2025). From the XML: Part IX line 11a (management fees) and line 12
    (advertising) by functional column, line 11g, "other expense" lines, Part VII Section B contractors and
    Schedule L business transactions naming the parent or administrator, Schedule O passages about the services
    agreement / workforce / fundraising / marketing, and whether Schedule R lists the parent. From audited
    statements (where posted and robots-allowed): the related-party / service-provider note, checked verbatim.

Usage: python3 scripts/mission_proxy_reconciliation.py . --xml-dir DIR --audit-text-dir DIR [--audit-text-dir DIR2]
"""
import argparse
import csv
import functools
import os
import re
import sys
import xml.etree.ElementTree as ET

MISSION = "data/mission-2026-11-14"
OUT = f"{MISSION}/proxy-reconciliation-parent-marketing-2026-11-19.csv"
RESILIENCE = f"{MISSION}/sponsor-financial-resilience-2021-2024.csv"
FEE_MARGIN = f"{MISSION}/sponsor-fee-revenue-margin-2026-11-19.csv"
MIRROR = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
COLUMNS = ("part", "sponsor", "ein", "fiscal_year", "tax_year_990", "object_id_990", "item", "value_usd",
           "value_text", "evidence", "source_ref", "note")

# ------------------------------------------------------------------------------------------------------------
# (A) sponsor-years: (fiscal_year, tax_year, object_id of that year, object_id of the prior year)
# ------------------------------------------------------------------------------------------------------------
SPONSORS_A = (
    dict(sponsor="Fidelity Charitable", ein="110303001", years=(
        (2023, 2022, "202441369349301334", "202430459349302913"),
        (2024, 2023, "202521349349310887", "202441369349301334"))),
    dict(sponsor="Renaissance Charitable Foundation (RCF)", ein="352129262", years=(
        (2023, 2023, "202443109349303629", "202303149349303205"),
        (2024, 2024, "202543189349301959", "202443109349303629"))),
    dict(sponsor="National Christian Charitable Foundation (NCF)", ein="581493949", years=(
        (2023, 2023, "202443169349306424", "202323179349311657"),
        (2024, 2024, "202513109349303201", "202443169349306424"))),
    dict(sponsor="Jewish Communal Fund (JCF)", ein="237174183", years=(
        (2023, 2022, "202410969349301036", "202330479349300013"),
        (2024, 2023, "202500369349300210", "202410969349301036"))),
    dict(sponsor="Combined Jewish Philanthropies (CJP)", ein="042103559", years=(
        (2023, 2022, "202421289349303727", "202321319349304847"),
        (2024, 2023, "202541259349302634", "202421289349303727"))),
)

# Audit anchors: (doc file stem, line-label regex, numbers that must appear on the same line).
# 'values' are the USD figures used below (thousands converted where the source prints thousands).
AUDIT_ANCHORS = (
    # RCF 2024 statements (2023 comparative): total assets and total liabilities
    dict(key="rcf_total_liabilities", ein="352129262", doc="e6cf79_2024RCFAuditedFinancialStatements",
         label=r"^\s*Total liabilities\s", nums=("16,914,399", "35,722,351"), values={2024: 16914399, 2023: 35722351}),
    dict(key="rcf_total_assets", ein="352129262", doc="e6cf79_2024RCFAuditedFinancialStatements",
         label=r"^\s*Total assets\s", nums=("5,913,566,776", "4,181,391,517"), values={2024: 5913566776, 2023: 4181391517}),
    # NCF consolidating statement of financial position, NCCF column (thousands): operating and fund net assets
    dict(key="ncf_nccf_operating_na", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"^\s*Operating\s+24,666\s", nums=("24,666", "45,267"), values={2024: 24666000}),
    dict(key="ncf_nccf_operating_na", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"^\s*Operating\s+29,463\s", nums=("29,463", "40,545"), values={2023: 29463000}),
    dict(key="ncf_nccf_daf_and_charitable_funds", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"Donor-advised or charitable funds\s+6,002,757", nums=("6,002,757", "8,057,882"), values={2024: 6002757000}),
    dict(key="ncf_nccf_daf_and_charitable_funds", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"Donor-advised or charitable funds\s+5,205,522", nums=("5,205,522", "7,284,662"), values={2023: 5205522000}),
    dict(key="ncf_nccf_net_assets_with_restrictions", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"^\s*With donor restrictions\s+2,420\s", nums=("2,420", "6,522"), values={2024: 2420000}),
    dict(key="ncf_nccf_net_assets_with_restrictions", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"^\s*With donor restrictions\s+2,355\s", nums=("2,355", "8,261"), values={2023: 2355000}),
    dict(key="ncf_nccf_annuity_reserves", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"Board designated.annuity reserves\s+527\s", nums=("527",), values={2024: 527000}),
    dict(key="ncf_nccf_annuity_reserves", ein="581493949", doc="61d908_NCF-24-Consolidated-FS-Final",
         label=r"Board designated.annuity reserves\s+526\s", nums=("526",), values={2023: 526000}),
    # JCF FY2024 statements (FY2023 comparative): classes of net assets without donor restrictions
    dict(key="jcf_reserve_fund", ein="237174183", doc="a70af0_JCF-FINAL-FS-FY2024",
         label=r"^\s*Reserve fund\s", nums=("2,681,442", "2,558,752"), values={2024: 2681442, 2023: 2558752}),
    dict(key="jcf_functioning_as_endowment", ein="237174183", doc="a70af0_JCF-FINAL-FS-FY2024",
         label=r"^\s*Functioning as endowment\s", nums=("24,202,416", "21,302,379"), values={2024: 24202416, 2023: 21302379}),
    dict(key="jcf_undesignated_available_for_operations", ein="237174183", doc="a70af0_JCF-FINAL-FS-FY2024",
         label=r"Undesignated - available for operations", nums=("2,846,942,795", "2,696,202,788"),
         values={2024: 2846942795, 2023: 2696202788}),
    dict(key="jcf_designated_and_semi_designated", ein="237174183", doc="a70af0_JCF-FINAL-FS-FY2024",
         label=r"^\s*Designated and semi-designated\s", nums=("23,627,772", "20,832,064"), values={2024: 23627772, 2023: 20832064}),
    dict(key="jcf_endowment_net_investment_income", ein="237174183", doc="a70af0_JCF-FINAL-FS-FY2024",
         label=r"^\s*Net investment income\s", nums=("4,507,348", "3,389,699"), values={2024: 4507348, 2023: 3389699}),
    # CJP consolidating schedule of activities by functional area (thousands)
    dict(key="cjp_change_in_na_operations", ein="042103559", doc="c94784_Audited Financial Statements 2023–2024",
         label=r"CHANGE IN NET ASSETS\s+47,104", nums=("47,104", "27,414", "88,331", "254"), values={2024: 47104000}),
    dict(key="cjp_change_in_na_endowment_reserves", ein="042103559", doc="c94784_Audited Financial Statements 2023–2024",
         label=r"CHANGE IN NET ASSETS\s+47,104", nums=("27,414",), values={2024: 27414000}),
    dict(key="cjp_change_in_na_jcep_and_funds_for_others", ein="042103559", doc="c94784_Audited Financial Statements 2023–2024",
         label=r"CHANGE IN NET ASSETS\s+47,104", nums=("254",), values={2024: 254000}),
    dict(key="cjp_israel_emergency_fund_receipts", ein="042103559", doc="c94784_Audited Financial Statements 2023–2024",
         label=r"Israel Emergency Fund, net\s", nums=("55,997",), values={2024: 55997000}),
    dict(key="cjp_change_in_na_operations", ein="042103559", doc="cjp2023",
         label=r"CHANGE IN NET ASSETS\s+1,849", nums=("1,849", "18,158", "132,956", "81"), values={2023: 1849000}),
    dict(key="cjp_change_in_na_endowment_reserves", ein="042103559", doc="cjp2023",
         label=r"CHANGE IN NET ASSETS\s+1,849", nums=("18,158",), values={2023: 18158000}),
    dict(key="cjp_change_in_na_jcep_and_funds_for_others", ein="042103559", doc="cjp2023",
         label=r"CHANGE IN NET ASSETS\s+1,849", nums=("81",), values={2023: 81000}),
)

# ------------------------------------------------------------------------------------------------------------
# (B) affiliated-commercial nationals, TY2021-2024 returns (object ids as selected by the resilience study)
# ------------------------------------------------------------------------------------------------------------
SPONSORS_B = (
    dict(sponsor="Fidelity Charitable", ein="110303001", parent_re=r"\bFMR\b", admin_re=r"\bFMR\b",
         oids=("202430459349302913", "202441369349301334", "202521349349310887", "202601389349301700")),
    dict(sponsor="DAFgiving360 (Schwab)", ein="311640316", parent_re=r"SCHWAB", admin_re=r"SCHWAB",
         oids=("202330939349300403", "202411039349301716", "202541069349300729", "202611199349300601")),
    dict(sponsor="Vanguard Charitable", ein="232888152", parent_re=r"VANGUARD", admin_re=r"VANGUARD",
         oids=("202331359349303108", "202441359349309439", "202511349349313096", "202621329349306657")),
    dict(sponsor="GS DAF (Goldman Sachs Philanthropy Fund)", ein="311774905", parent_re=r"GOLDMAN|AYCO",
         admin_re=r"AYCO", oids=("202243089349301314", "202312859349302266", "202413109349303336", "202503109349303645")),
    dict(sponsor="Goldman Sachs Charitable Gift Fund", ein="113813663", parent_re=r"GOLDMAN",
         admin_re=r"CHARITIES AID", oids=("202311099349301951", "202421169349301122", "202511119349301416", "202611249349302616")),
    dict(sponsor="Morgan Stanley GIFT", ein="527082731", parent_re=r"MORGAN STANLEY", admin_re=r"RENPSG",
         oids=("202203199349314745", "202302999349301010", "202403209349313980", "202503239349300435")),
    dict(sponsor="BofA Charitable Gift Fund", ein="046010342", parent_re=r"BANK OF AMERICA", admin_re=r"BANK OF AMERICA",
         oids=("202222869349300202", "202441809349301264", "202520169349301042", "202503219349318170")),
    dict(sponsor="Raymond James Charitable", ein="593652538", parent_re=r"RAYMOND JAMES", admin_re=r"RAYMOND JAMES TRUST",
         oids=("202320469349302162", "202430469349302713", "202520499349301607", "202630489349300743")),
)

# Audit statements read for (B): verbatim quotes checked in the pdftotext output (whitespace-normalised).
AUDIT_QUOTES_B = (
    dict(ein="110303001", fys="FY2022-FY2023", doc="fid2023",
         url="https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf",
         quote="Under this contract, the Gift Fund paid FMR at amounts equal to the administrative fee the Gift Fund charged its donors."),
    dict(ein="110303001", fys="FY2023-FY2024", doc="802fbe_audited-financial-statements-2024-2023",
         url="https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf",
         quote="Under this contract, the Gift Fund paid FMR at amounts equal to the administrative fee the Gift Fund charged its donors."),
    dict(ein="110303001", fys="FY2024-FY2025", doc="735158_audited-financial-statements-2025-2024",
         url="https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf",
         quote="the Gift Fund paid FMR at amounts equal to the administrative fee the Gift Fund charged its donors, net of any tier price credits described in Note 2."),
    dict(ein="232888152", fys="FY2024-FY2025", doc="e6c8c5_vanguard-charitable-2025-financial-statements",
         url="https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf",
         quote="Vanguard Charitable has contracted Vanguard to provide certain support services including investment recordkeeping and administrative services. Vanguard provides such services in exchange for a fee. The fees incurred for the years ended June 30, 2025 and 2024 were $4,014,052 and $3,916,396, respectively."),
    dict(ein="232888152", fys="FY2024-FY2025", doc="e6c8c5_vanguard-charitable-2025-financial-statements",
         url="https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf",
         quote="In-kind contributions of professional services received from Vanguard for the years ended June 30, 2025 and 2024 were $1,000,342 and $788,129, respectively."),
    dict(ein="232888152", fys="FY2024-FY2025", doc="e6c8c5_vanguard-charitable-2025-financial-statements",
         url="https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf",
         quote="Fundraising expenses 4,091,664 3,833,010"),
)
# Audit status for sponsors without a readable statement (from b4014-b4427 §3.2 / §4.2 and this pass's log).
AUDIT_STATUS_B = {
    "110303001": "read: FY2022-FY2025 statements (three PDFs)",
    "311640316": "blocked: www.dafgiving360.org and www.schwabcharitable.org return HTTP 403 to a generic client; not bypassed",
    "232888152": "read: FY2025/FY2024 statements; FY2022-FY2023 statements not located (guessed paths 404)",
    "311774905": "not posted (b4014-b4427 §3.2); www.gsphilanthropyfund.org unreachable",
    "113813663": "not posted; no public statement located",
    "527082731": "not posted (www.morganstanley.com/gift page read, no statements)",
    "046010342": "not posted; Schedule O says audited statements are filed with the Massachusetts Attorney General",
    "593652538": "blocked: robots.txt unreachable on raymondjamescharitable.com, rjcef.com and raymondjames.com (treated as disallow)",
}
MARKETING_RE = re.compile(r"MARKETING|ADVERTIS|PROMOTION|\bBRAND", re.I)
SCHED_O_RE = re.compile(r"SERVICES? AGREEMENT|ADMINISTRATIVE SERVICES|EMPLOYEES OF|CORPORATE TRUSTEE|"
                        r"DOES NOT HAVE ANY EMPLOYEES|SENIOR EXECUTIVES AT|MARKETING|ADVERTIS|PROMOTION|\bBRAND", re.I)
OTHER_EXP_RE = re.compile(r"ADMIN|AGENCY|COMMISSION|MARKET|ADVERT|PROMOT|FUNDRAIS", re.I)


# ------------------------------------------------------------------------------------------------------------
# small pure helpers
# ------------------------------------------------------------------------------------------------------------
def num(s):
    try:
        return float(s) if s not in (None, "") else None
    except ValueError:
        return None


def fmt(x, nd=0):
    if x is None:
        return ""
    if isinstance(x, bool):
        return "true" if x else "false"
    return f"{x:.{nd}f}" if nd else str(int(round(x)))


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def row(part, sponsor, ein, item, value=None, text="", evidence="", source="", note="", fy="", ty="", oid="", nd=0):
    return dict(part=part, sponsor=sponsor, ein=ein, fiscal_year=fy, tax_year_990=ty, object_id_990=oid, item=item,
                value_usd=fmt(value, nd) if not isinstance(value, str) else value, value_text=text,
                evidence=evidence, source_ref=source, note=note)


# ------------------------------------------------------------------------------------------------------------
# XML extraction (pure on the parsed tree)
# ------------------------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def load_xml(path: str):
    return ET.parse(path).getroot()


def first(el, name: str):
    return next((e for e in el.iter() if local(e.tag) == name), None)


def child_text(el, name: str):
    c = None if el is None else next((e for e in el.iter() if local(e.tag) == name), None)
    return None if c is None or c.text is None else c.text.strip()


def grp_amounts(root, grp: str) -> dict:
    g = first(root, grp)
    return {k: num(child_text(g, t)) for k, t in (("total", "TotalAmt"), ("program", "ProgramServicesAmt"),
                                                   ("mgmt", "ManagementAndGeneralAmt"), ("fundraising", "FundraisingAmt"))} \
        if g is not None else {}


def balance(root, grp: str, when: str = "EOYAmt"):
    return num(child_text(first(root, grp), when))


def schedule(root, name: str):
    return first(root, name)


def facts_a(root) -> dict:
    sd = schedule(root, "IRS990ScheduleD")
    cy = first(sd, "CYEndwmtFundGrp") if sd is not None else None
    na = balance(root, "TotalNetAssetsFundBalanceGrp")
    return dict(na_total=na if na is not None else num(child_text(root, "NetAssetsOrFundBalancesEOYAmt")),
                total_assets=balance(root, "TotalAssetsGrp"), total_liabilities=balance(root, "TotalLiabilitiesGrp"),
                ppe=balance(root, "LandBldgEquipBasisNetGrp"),
                daf_value=num(child_text(sd, "DonorAdvisedFundsVlEOYAmt")) if sd is not None else None,
                colb_value=num(child_text(sd, "FundsAndOtherAccountsVlEOYAmt")) if sd is not None else None,
                endow_earnings=num(child_text(cy, "InvestmentEarningsOrLossesAmt")) if cy is not None else None,
                endow_eoy=num(child_text(cy, "EndYearBalanceAmt")) if cy is not None else None)


def r1(f: dict):
    return None if f["na_total"] is None or f["daf_value"] is None else f["na_total"] - f["daf_value"]


def zero(x):
    return 0.0 if x is None else x


# ------------------------------------------------------------------------------------------------------------
# audit-text checks
# ------------------------------------------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def read_text(dirs: tuple, stem: str):
    path = next((os.path.join(d, stem + ".txt") for d in dirs if os.path.exists(os.path.join(d, stem + ".txt"))), None)
    return None if path is None else open(path, encoding="utf-8", errors="replace").read()


def anchor_ok(dirs: tuple, a: dict) -> bool:
    txt = read_text(dirs, a["doc"])
    return bool(txt) and any(re.search(a["label"], ln) and all(n in ln for n in a["nums"]) for ln in txt.splitlines())


def quote_ok(dirs: tuple, q: dict) -> bool:
    txt = read_text(dirs, q["doc"])
    return bool(txt) and norm_ws(q["quote"]) in norm_ws(txt)


def anchor_value(dirs: tuple, ein: str, key: str, fy: int):
    hits = tuple(a for a in AUDIT_ANCHORS if a["ein"] == ein and a["key"] == key and fy in a["values"])
    return (hits[0]["values"][fy], anchor_ok(dirs, hits[0]), hits[0]["doc"]) if hits else (None, False, "")


# ------------------------------------------------------------------------------------------------------------
# (A) decomposition
# ------------------------------------------------------------------------------------------------------------
def fee_surplus(ein: str, fy: int, margin_rows: dict):
    m = margin_rows.get((ein, str(fy)), {})
    fee, less, other, opc = (num(m.get(k)) for k in ("internal_daf_fee_usd", "audit_fee_less_opex_usd",
                                                     "audit_other_figure_usd", "operating_cost_990_usd"))
    if ein == "237174183":
        return (less - other if less is not None and other is not None else None,
                "fee - opex - $2.0m operating-fund grant to UJA (post-grant surplus; wave 38B like-for-like)")
    if ein == "581493949":
        return (fee - opc if fee is not None and opc is not None else None,
                "NCCF-column fee - NCCF 990 operating cost (wave 38B correction; NCCF-column G&A includes intra-group fees)")
    if ein == "042103559":
        return (None, "not computable: CJP Operations is the federation's whole budget; fee $%s" % fmt(fee))
    return (less, "audited fee - audited operating expenses (b4014-b4427 Part B)")


def decompose_year(spec: dict, yr: tuple, xml_dir: str, dirs: tuple, margin_rows: dict, res_rows: dict) -> list:
    fy, ty, oid, prior = yr
    ein, name = spec["ein"], spec["sponsor"]
    cur, pre = facts_a(load_xml(os.path.join(xml_dir, oid + ".xml"))), facts_a(load_xml(os.path.join(xml_dir, prior + ".xml")))
    d_r1 = r1(cur) - r1(pre)
    res_d_r1 = num(res_rows.get((ein, str(ty)), {}).get("r1_change_yoy"))
    c1 = zero(cur["colb_value"]) - zero(pre["colb_value"])
    inside = cur["endow_eoy"] is not None and cur["colb_value"] is not None and abs(cur["endow_eoy"] - cur["colb_value"]) < 1
    c2 = 0.0 if inside else zero(cur["endow_earnings"])
    c3 = zero(cur["ppe"]) - zero(pre["ppe"])
    c4, c4_basis = fee_surplus(ein, fy, margin_rows)
    resid = d_r1 - c1 - c2 - c3 - zero(c4)
    src = MIRROR.format(oid)
    base = dict(fy=fy, ty=ty, oid=oid)
    rows = [
        row("A", name, ein, "delta_r1", d_r1, evidence="C", source=src,
            note=f"R1 = Part X line 32 - Sched D DAF value; prior year {prior}; resilience CSV r1_change_yoy = {fmt(res_d_r1)}"
                 f" ({'match' if res_d_r1 is not None and abs(res_d_r1 - d_r1) < 1 else 'MISMATCH'})", **base),
        row("A", name, ein, "c1_other_funds_growth_sched_d_col_b", c1, evidence="C", source=src,
            note=f"Sched D Part I col (b) EOY {fmt(cur['colb_value'])} vs {fmt(pre['colb_value'])}", **base),
        row("A", name, ein, "c2_endowment_returns_outside_col_b", c2, evidence="C", source=src,
            note=("Part V endowment equals the col (b) fund, so its returns are inside c1" if inside else
                  f"Sched D Part V line 1c current year; EOY endowment {fmt(cur['endow_eoy'])}" if cur["endow_eoy"] is not None
                  else "no Sched D Part V endowment"), **base),
        row("A", name, ein, "c2_memo_endowment_returns_inside_col_b", zero(cur["endow_earnings"]) if inside else None,
            evidence="F", source=src, note="memo only; already counted in c1" if inside else "", **base),
        row("A", name, ein, "c3_ppe_change", c3, evidence="C", source=src,
            note=f"Part X line 10c EOY {fmt(cur['ppe'])} vs {fmt(pre['ppe'])}", **base),
        row("A", name, ein, "c4_audit_fee_surplus", c4, evidence="F/C", source=FEE_MARGIN, note=c4_basis, **base),
        row("A", name, ein, "residual_after_c1_to_c4", resid, evidence="C", source=src,
            note="dR1 - (c1 + c2 + c3 + c4); c4 taken as 0 where not computable", **base),
        row("A", name, ein, "share_of_delta_r1_from_c1_c2_c3", (c1 + c2 + c3) / d_r1 if d_r1 else None, evidence="C",
            source=src, note="non-fee balance-sheet items / dR1", nd=4, **base),
        row("A", name, ein, "delta_r1_less_fee_surplus", d_r1 - c4 if c4 is not None else None, evidence="C",
            source=src, note="error if dR1 were read as the fee surplus", **base),
    ]
    return rows + anchors_for(spec, yr, cur, pre, dirs)


def anchors_for(spec: dict, yr: tuple, cur: dict, pre: dict, dirs: tuple) -> list:
    """Sponsor-specific audit anchors that locate the residual."""
    fy, ty, oid, prior = yr
    ein, name = spec["ein"], spec["sponsor"]
    base = dict(fy=fy, ty=ty, oid=oid)
    src = MIRROR.format(oid)
    if ein == "110303001":
        r6c, r6p = r1(cur) - zero(cur["colb_value"]), r1(pre) - zero(pre["colb_value"])
        return [row("A", name, ein, "anchor_r1_minus_col_b_eoy", r6c, evidence="C", source=src,
                    note=f"R6 = R1 - col (b): {fmt(r6c)} (prior {fmt(r6p)}); R1 is the col (b) 'other funds' column; "
                         "audit Note 7 pays FMR an amount equal to the fee, so no fee surplus can accumulate", **base)]
    if ein == "352129262":
        gap_c, gap_p = cur["total_assets"] - cur["daf_value"], pre["total_assets"] - pre["daf_value"]
        liab, ok_l, doc_l = anchor_value(dirs, ein, "rcf_total_liabilities", fy)
        ta, ok_t, _ = anchor_value(dirs, ein, "rcf_total_assets", fy)
        return [
            row("A", name, ein, "anchor_minus_change_in_total_liabilities",
                -(cur["total_liabilities"] - pre["total_liabilities"]), evidence="C", source=src,
                note=f"Part X line 26 EOY {fmt(cur['total_liabilities'])} vs {fmt(pre['total_liabilities'])}; audit total "
                     f"liabilities {fmt(liab)} verified={fmt(ok_l)} ({doc_l})", **base),
            row("A", name, ein, "anchor_change_in_total_assets_less_sched_d_daf_value", gap_c - gap_p, evidence="C",
                source=src, note=f"(Part X total assets - Sched D DAF value) EOY {fmt(gap_c)} vs {fmt(gap_p)}; audit total "
                                 f"assets {fmt(ta)} verified={fmt(ok_t)}; identity R1 = (TA - DAF value) - liabilities", **base)]
    if ein == "581493949":
        op, ok_op, doc = anchor_value(dirs, ein, "ncf_nccf_operating_na", fy)
        op_p, ok_op_p, _ = anchor_value(dirs, ein, "ncf_nccf_operating_na", fy - 1)
        funds, ok_f, _ = anchor_value(dirs, ein, "ncf_nccf_daf_and_charitable_funds", fy)
        funds_p, ok_fp, _ = anchor_value(dirs, ein, "ncf_nccf_daf_and_charitable_funds", fy - 1)
        beyond = funds - cur["daf_value"] - zero(cur["colb_value"]) if funds is not None else None
        beyond_p = funds_p - pre["daf_value"] - zero(pre["colb_value"]) if funds_p is not None else None
        small = [(k, anchor_value(dirs, ein, k, fy), anchor_value(dirs, ein, k, fy - 1))
                 for k in ("ncf_nccf_net_assets_with_restrictions", "ncf_nccf_annuity_reserves")]
        return [row("A", name, ein, f"anchor_{k[4:]}_change", c[0] - p[0], evidence="C", source=doc,
                    note=f"NCCF column, thousands x 1000; verified={fmt(c[1] and p[1])}", **base)
                for k, c, p in small if c[0] is not None and p[0] is not None] + [
            row("A", name, ein, "anchor_nccf_audit_operating_net_assets_eoy", op, evidence="F", source=doc,
                note=f"NCCF column, thousands x 1000; verified={fmt(ok_op)}", **base),
            row("A", name, ein, "anchor_nccf_audit_operating_net_assets_change",
                op - op_p if op is not None and op_p is not None else None, evidence="C", source=doc,
                note="blank for FY2023: the FY2022 NCCF operating figure is not in the statements read"
                if op_p is None else f"verified={fmt(ok_op and ok_op_p)}", **base),
            row("A", name, ein, "anchor_nccf_funds_beyond_sched_d_col_a_and_b_eoy", beyond, evidence="C", source=doc,
                note=f"audit NCCF 'donor-advised or charitable funds' {fmt(funds)} - Sched D col (a) - col (b); verified={fmt(ok_f)}",
                **base),
            row("A", name, ein, "anchor_nccf_funds_beyond_sched_d_change",
                beyond - beyond_p if beyond is not None and beyond_p is not None else None, evidence="C", source=doc,
                note="blank for FY2023 (FY2022 split not read)" if beyond_p is None else f"verified={fmt(ok_f and ok_fp)}",
                **base)]
    if ein == "237174183":
        res, ok_r, doc = anchor_value(dirs, ein, "jcf_reserve_fund", fy)
        und, ok_u, _ = anchor_value(dirs, ein, "jcf_undesignated_available_for_operations", fy)
        des, ok_d, _ = anchor_value(dirs, ein, "jcf_designated_and_semi_designated", fy)
        end, ok_e, _ = anchor_value(dirs, ein, "jcf_functioning_as_endowment", fy)
        r6 = r1(cur) - zero(cur["colb_value"])
        return [
            row("A", name, ein, "anchor_r1_minus_col_b_equals_audit_reserve_fund", r6, evidence="C", source=doc,
                note=f"audit reserve fund {fmt(res)}; equal={fmt(res is not None and abs(r6 - res) < 1)}; verified={fmt(ok_r)}", **base),
            row("A", name, ein, "anchor_col_b_equals_audit_endowment", cur["colb_value"], evidence="C", source=doc,
                note=f"audit 'functioning as endowment' {fmt(end)}; equal={fmt(end is not None and abs(cur['colb_value'] - end) < 1)}; "
                     f"verified={fmt(ok_e)}", **base),
            row("A", name, ein, "anchor_sched_d_daf_value_equals_undesignated_plus_designated", cur["daf_value"], evidence="C",
                source=doc, note=f"audit undesignated (incl. the operating fund) {fmt(und)} + designated/semi-designated {fmt(des)}"
                                 f" = {fmt(zero(und) + zero(des))}; equal={fmt(abs(cur['daf_value'] - zero(und) - zero(des)) < 1)};"
                                 f" verified={fmt(ok_u and ok_d)}", **base)]
    if ein == "042103559":
        ops, ok1, doc = anchor_value(dirs, ein, "cjp_change_in_na_operations", fy)
        endw, ok2, _ = anchor_value(dirs, ein, "cjp_change_in_na_endowment_reserves", fy)
        jcep, ok3, _ = anchor_value(dirs, ein, "cjp_change_in_na_jcep_and_funds_for_others", fy)
        isr, ok4, _ = anchor_value(dirs, ein, "cjp_israel_emergency_fund_receipts", fy)
        tot = sum(zero(x) for x in (ops, endw, jcep))
        rows = [
            row("A", name, ein, "anchor_audit_non_daf_areas_change", tot, evidence="C", source=doc,
                note=f"CJP Operations {fmt(ops)} + Endowment and Reserves {fmt(endw)} + JCEP/funds for others {fmt(jcep)} "
                     f"(thousands x 1000); verified={fmt(ok1 and ok2 and ok3)}", **base),
            row("A", name, ein, "anchor_audit_cjp_operations_change", ops, evidence="F", source=doc,
                note="includes campaign receipts not yet granted", **base)]
        return rows + ([row("A", name, ein, "anchor_audit_israel_emergency_fund_receipts", isr, evidence="F", source=doc,
                            note=f"verified={fmt(ok4)}", **base)] if isr is not None else [])
    return []


def part_a(xml_dir: str, dirs: tuple, margin_rows: dict, res_rows: dict) -> list:
    return [r for spec in SPONSORS_A for yr in spec["years"]
            for r in decompose_year(spec, yr, xml_dir, dirs, margin_rows, res_rows)]


# ------------------------------------------------------------------------------------------------------------
# (B) parent-paid marketing
# ------------------------------------------------------------------------------------------------------------
def header(root) -> dict:
    return dict(ty=child_text(root, "TaxYr"), end=child_text(root, "TaxPeriodEndDt"))


def contractors(root, pat: str) -> list:
    groups = (g for g in root.iter() if local(g.tag) == "ContractorCompensationGrp")
    out = ((norm_ws(" ".join(t for t in (child_text(g, "BusinessNameLine1Txt"), child_text(g, "PersonNm")) if t)),
            child_text(g, "ServicesDesc") or "", num(child_text(g, "CompensationAmt"))) for g in groups)
    return [c for c in out if re.search(pat, c[0], re.I)]


def schedule_l(root, pat: str) -> list:
    sl = schedule(root, "IRS990ScheduleL")
    groups = () if sl is None else (g for g in sl.iter() if local(g.tag) == "BusTrInvolveInterestedPrsnGrp")
    out = ((norm_ws(" ".join(t for t in (child_text(g, "BusinessNameLine1Txt"), child_text(g, "PersonNm")) if t)),
            child_text(g, "TransactionDesc") or "", num(child_text(g, "TransactionAmt"))) for g in groups)
    return [c for c in out if re.search(pat, c[0], re.I)]


def other_expenses(root) -> list:
    groups = (g for g in root.iter() if local(g.tag) == "OtherExpensesGrp")
    out = ((child_text(g, "Desc") or "", num(child_text(g, "TotalAmt")), num(child_text(g, "FundraisingAmt"))) for g in groups)
    return [o for o in out if OTHER_EXP_RE.search(o[0])]


def sched_o_passages(root) -> list:
    so = schedule(root, "IRS990ScheduleO")
    if so is None:
        return []
    refs = [e for e in so.iter() if local(e.tag) in ("FormAndLineReferenceDesc", "ExplanationTxt")]
    pairs = [(norm_ws(refs[i].text or ""), norm_ws(refs[i + 1].text or "")) for i in range(len(refs) - 1)
             if local(refs[i].tag) == "FormAndLineReferenceDesc" and local(refs[i + 1].tag) == "ExplanationTxt"]
    keep = [(r, t) for r, t in pairs if SCHED_O_RE.search(t) and not re.search(r"COMPENSATION COMMITTEE", t[:120], re.I)]
    return list(dict.fromkeys(keep))


CHARITY_NAME_RE = re.compile(r"CHARIT|FOUNDATION|GIFT FUND|GIFT FND|GIVES|PHILANTHROPY|ENDOWMENT|TRUSTS", re.I)


def sched_r_names(root) -> list:
    sr = schedule(root, "IRS990ScheduleR")
    return [] if sr is None else [norm_ws(e.text or "") for e in sr.iter() if local(e.tag) == "BusinessNameLine1Txt"]


def sched_r_part_v_names(root) -> list:
    sr = schedule(root, "IRS990ScheduleR")
    groups = () if sr is None else (g for g in sr.iter() if local(g.tag) == "TransactionsRelatedOrgGrp")
    return [norm_ws(child_text(g, "BusinessNameLine1Txt") or "") for g in groups]


def year_rows_b(spec: dict, oid: str, xml_dir: str) -> list:
    root = load_xml(os.path.join(xml_dir, oid + ".xml"))
    h = header(root)
    ein, name = spec["ein"], spec["sponsor"]
    base = dict(fy=(h["end"] or "")[:7], ty=h["ty"] or "", oid=oid)
    src = MIRROR.format(oid)
    l11a, l12, l11g, l11f = (grp_amounts(root, g) for g in ("FeesForServicesManagementGrp", "AdvertisingGrp",
                                                             "FeesForServicesOtherGrp", "FeesForSrvcInvstMgmntFeesGrp"))
    ctr, sl, oth = contractors(root, spec["parent_re"] + "|" + spec["admin_re"]), schedule_l(root, spec["parent_re"]), other_expenses(root)
    sop = sched_o_passages(root)
    srn = [n for n in sched_r_names(root) if re.search(spec["parent_re"], n, re.I) and not CHARITY_NAME_RE.search(n)]
    srv = [n for n in sched_r_part_v_names(root) if re.search(spec["parent_re"], n, re.I) and not CHARITY_NAME_RE.search(n)]
    sa_fund = [t for _, t in sop if re.search(r"AGREEMENT", t, re.I) and re.search(r"FUNDRAISING", t, re.I)]
    mkt = [t for _, t in sop if MARKETING_RE.search(t)]
    return ([row("B", name, ein, "part_ix_11a_management_fees_total", l11a.get("total"), evidence="F", source=src,
                 note=f"program {fmt(l11a.get('program'))}; M&G {fmt(l11a.get('mgmt'))}; fundraising {fmt(l11a.get('fundraising'))}"
                 if l11a else "line blank", **base),
             row("B", name, ein, "part_ix_11a_fundraising_column", l11a.get("fundraising"), evidence="F", source=src, **base),
             row("B", name, ein, "part_ix_12_advertising_total", l12.get("total"), evidence="F", source=src,
                 note=f"fundraising column {fmt(l12.get('fundraising'))}" if l12 else "line blank", **base),
             row("B", name, ein, "part_ix_11g_other_fees_total", l11g.get("total"), evidence="F", source=src, **base),
             row("B", name, ein, "part_ix_11f_investment_mgmt_fees_total", l11f.get("total"), evidence="F", source=src, **base)]
            + [row("B", name, ein, "part_vii_b_contractor_parent_or_administrator", amt, text=f"{n} | {d}", evidence="F",
                   source=src, **base) for n, d, amt in ctr]
            + [row("B", name, ein, "schedule_l_business_transaction_parent", amt, text=f"{n} | {d}", evidence="F",
                   source=src, **base) for n, d, amt in sl]
            + [row("B", name, ein, "part_ix_24_other_expense_line", amt, text=d, evidence="F", source=src,
                   note=f"fundraising column {fmt(fr)}", **base) for d, amt, fr in oth]
            + [row("B", name, ein, "schedule_o_passage", None, text=f"{r} :: {t[:900]}", evidence="F", source=src, **base)
               for r, t in sop]
            + [row("B", name, ein, "schedule_o_services_agreement_includes_fundraising", "true" if sa_fund else "false",
                   evidence="F", source=src, **base),
               row("B", name, ein, "schedule_o_mentions_marketing_advertising_brand", "true" if mkt else "false",
                   evidence="F", source=src, **base),
               row("B", name, ein, "schedule_r_filed", "true" if schedule(root, "IRS990ScheduleR") is not None else "false",
                   evidence="F", source=src, **base),
               row("B", name, ein, "schedule_r_names_parent_company", "true" if srn else "false", evidence="F", source=src,
                   text="; ".join(dict.fromkeys(srn))[:300],
                   note="parent-group company named anywhere in Schedule R (charities excluded)", **base),
               row("B", name, ein, "schedule_r_part_v_transaction_with_parent_company", "true" if srv else "false",
                   evidence="F", source=src, text="; ".join(dict.fromkeys(srv))[:300], **base)])


def audit_rows_b(spec: dict, dirs: tuple) -> list:
    ein, name = spec["ein"], spec["sponsor"]
    qs = [q for q in AUDIT_QUOTES_B if q["ein"] == ein]
    mk = [(q["doc"], len(MARKETING_RE.findall(read_text(dirs, q["doc"]) or ""))) for q in qs]
    return ([row("B", name, ein, "audit_status", None, text=AUDIT_STATUS_B[ein], evidence="F")]
            + [row("B", name, ein, "audit_related_party_quote", None, text=q["quote"], evidence="F", source=q["url"],
                   note=f"{q['fys']}; verified_in_text={fmt(quote_ok(dirs, q))}") for q in qs]
            + [row("B", name, ein, "audit_marketing_term_count", float(n), text=d, evidence="C",
                   note="matches of marketing|advertis|promotion|brand in the whole statement text")
               for d, n in dict.fromkeys(mk)])


def part_b(xml_dir: str, dirs: tuple) -> list:
    return [r for spec in SPONSORS_B for r in audit_rows_b(spec, dirs) + [x for o in spec["oids"] for x in year_rows_b(spec, o, xml_dir)]]


def fidelity_11a_check(xml_dir: str, dirs: tuple) -> list:
    """Fidelity: Part IX 11a equals the audited 'Administrative fees' paid to FMR in each FY2022-FY2025."""
    audit = ((2022, "202430459349302913", 124608555, "fid2023"), (2023, "202441369349301334", 121190522, "fid2023"),
             (2024, "202521349349310887", 139686600, "802fbe_audited-financial-statements-2024-2023"),
             (2025, "202601389349301700", 179875837, "735158_audited-financial-statements-2025-2024"))
    def one(fy, oid, fee, doc):
        l11a = grp_amounts(load_xml(os.path.join(xml_dir, oid + ".xml")), "FeesForServicesManagementGrp").get("total")
        txt = read_text(dirs, doc) or ""
        seen = any("Administrative fees" in ln and f"{fee:,}" in ln for ln in txt.splitlines())
        return row("B", "Fidelity Charitable", "110303001", "check_11a_equals_audited_fee_paid_to_fmr", l11a,
                   text=f"audit {fee:,}", evidence="C", source=doc,
                   note=f"equal={fmt(l11a is not None and abs(l11a - fee) < 1)}; audit figure verified={fmt(seen)}",
                   fy=fy, oid=oid)
    return [one(*a) for a in audit]


def read_csv(path: str) -> list:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--audit-text-dir", action="append", default=[])
    a = ap.parse_args(argv)
    dirs = tuple(a.audit_text_dir)
    margin = {(r["ein"], r["fiscal_year"]): r for r in read_csv(os.path.join(a.root, FEE_MARGIN))}
    res = {(r["ein"], r["tax_year"]): r for r in read_csv(os.path.join(a.root, RESILIENCE)) if r.get("row_type") == "sponsor_year"}
    rows = part_a(a.xml_dir, dirs, margin, res) + part_b(a.xml_dir, dirs) + fidelity_11a_check(a.xml_dir, dirs)
    out = os.path.join(a.root, OUT)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    unverified = [r for r in rows if re.search(r"verified(_in_text)?=false", r["note"]) or "MISMATCH" in r["note"]]
    print(f"wrote {out}: {len(rows)} rows ({sum(r['part'] == 'A' for r in rows)} part A, "
          f"{sum(r['part'] == 'B' for r in rows)} part B); unverified/mismatch rows: {len(unverified)}")
    for r in unverified:
        print("  CHECK", r["sponsor"], r["fiscal_year"], r["item"], r["note"][:160])
    return 0


if __name__ == "__main__":
    sys.exit(main())
