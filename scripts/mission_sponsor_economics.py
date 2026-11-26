#!/usr/bin/env python3
"""Sponsor economics (task b4014-b4427): queue items P-B40N14-04 and P-B44N27-02.

Stdlib only; functional style (pure transforms, I/O at the edges).

(A) P-B40N14-04 - Dechomai grants to each national sponsor as a share of that sponsor's DAF contributions
    (Form 990 Schedule D Part I line 2, column (a)), fiscal years matched.
    * Dechomai side: Schedule I lines (cash + non-cash) of Dechomai Asset Trust and Dechomai Foundation, read
      from data/mission-2026-11-14/dechomai-dafpay-2026-11-19.csv (record_type sched_i, selected=1).
      Attribution is name-first, as in the source study and confirmed by validation wave 37B (V37B-06..09);
      the one EIN/name conflict (DF TY2023 "SCHWAB CHARITABLE TRUST" filed under AEF's EIN) is also shown
      EIN-first as an alternative.
    * Sponsor side: Schedule D Part I line 2(a) read directly from each sponsor's e-file XML (--xml-dir), one
      return per sponsor x tax year (period >= 300 days; latest ReturnTs, so amendments supersede).
      Cross-checked against the DAFRC panel with the repo's applied corrections
      (dafrc-sponsor-schedule-d-fy2019-2024.csv + dafrc-corrections-itemized.csv applied=1; the r2 file only
      re-confirms those rows).
    * MATCHING RULE (primary): Dechomai calendar year t is matched to the sponsor return whose tax period
      BEGINS in calendar year t (IRS "tax year" t). Calendar-year sponsors: CY t exactly. June-year sponsors:
      FY July t - June t+1 (e.g. CY2022 -> FY6/23). Rationale: a Dechomai grant paid in the second half of
      t lands in that FY; Dechomai grants are lumpy and year-end heavy [I], and the rule gives every sponsor
      the same "starts in t" convention. Alternatives: the adjacent sponsor tax years t-1 and t+1, plus,
      for June-year sponsors, an overlap-weighted blend (0.5 x FY ending June t + 0.5 x FY ending June t+1),
      which assumes grants are spread evenly across CY t.
    * Recency: sponsor periods ending before 2021-01-01 are not used (shown blank, flagged).

(B) P-B44N27-02 - internal DAF administrative-fee revenue and the operating margin on it, top-25 sponsors
    (FY2023-2024; FY = year in which the fiscal period ends).
    * Audit side: values read by hand from audited (or summary) statements posted on sponsors' own sites,
      fetched with a robots.txt check (log in the research doc). They are embedded below (AUDIT) with the URL
      and the exact figures; with --audit-text-dir the script checks that every figure appears verbatim in the
      pdftotext output of the cited document (column `figures_verified_in_text`).
    * 990 side: change in non-DAF net assets (dR1 = Part X line 32 - Schedule D DAF value, year on year) and
      operating cost, from data/mission-2026-11-14/sponsor-financial-resilience-2021-2024.csv; plus, from
      the e-file XML, Part IX line 11g (fees for services - other), the audit indicator, and Schedule O
      explanation lines that mention fees / administrative services / reimbursement.

Usage: python3 scripts/mission_sponsor_economics.py . --xml-dir DIR [--audit-text-dir DIR]
"""
import argparse
import csv
import functools
import os
import re
import statistics
import sys

MISSION = "data/mission-2026-11-14"
OUT_A = f"{MISSION}/dechomai-share-of-sponsor-contributions-2026-11-19.csv"
OUT_B = f"{MISSION}/sponsor-fee-revenue-margin-2026-11-19.csv"
MIRROR = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{}_public.xml"
DAFRC_URL = "https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx"

# ---------------------------------------------------------------------------------------------------------
# (A) sponsor universe: Dechomai's six national groups (as in b40n14-b38c) plus Vanguard and BofA.
# 'group' = the sponsor_group label used by dechomai-dafpay-2026-11-19.csv; None = matched by EIN / name here.
# ---------------------------------------------------------------------------------------------------------
SPONSORS_A = (
    dict(sponsor="DAFgiving360", ein="311640316", group="DAFgiving360", fy_end_month=6, name_re=None),
    dict(sponsor="Fidelity Charitable", ein="110303001", group="Fidelity Charitable", fy_end_month=6, name_re=None),
    dict(sponsor="AEF", ein="341747398", group="AEF", fy_end_month=12, name_re=None),
    dict(sponsor="GS DAF (Goldman Sachs Philanthropy Fund)", ein="311774905", group="Goldman Sachs", fy_end_month=12,
         name_re=None),
    dict(sponsor="Morgan Stanley GIFT", ein="527082731", group="Morgan Stanley GIFT", fy_end_month=12, name_re=None),
    dict(sponsor="NPT", ein="237825575", group="NPT", fy_end_month=6, name_re=None),
    dict(sponsor="Vanguard Charitable", ein="232888152", group=None, fy_end_month=6, name_re=r"VANGUARD CHARITABLE"),
    dict(sponsor="Bank of America Charitable Gift Fund", ein="046010342", group=None, fy_end_month=12,
         name_re=r"BANK OF AMERICA"),
)
DECHOMAI_YEARS = (2021, 2022, 2023, 2024)


def num(s):
    s = (s or "").strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, lineterminator="\n")
        w.writeheader()
        tuple(map(w.writerow, rows))
    return len(rows)


def fmt(v, nd=0):
    if v is None:
        return ""
    return f"{v:.{nd}f}" if nd else str(int(round(v)))


# ---------------------------------------------------------------------------------------------------------
# XML extraction (regex on leaf elements; namespaces optional)
# ---------------------------------------------------------------------------------------------------------
def leaf(text, tag):
    m = re.search(r"<(?:\w+:)?%s>([^<]*)</" % tag, text)
    return m.group(1).strip() if m else ""


def block(text, tag):
    i = text.find("<" + tag)
    if i < 0:
        return ""
    j = text.find("</" + tag + ">", i)
    return text[i:j] if j > 0 else ""


def unescape(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
            .replace("&apos;", "'"))


SCHED_O_RE = re.compile(r"\bfees?\b|administrative serv|reimburs|services agreement|administrator", re.I)


def parse_return(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        t = f.read()
    oid = os.path.basename(path).split("_")[0].split(".")[0]
    sched_d = block(t, "IRS990ScheduleD")
    sched_o = block(t, "IRS990ScheduleO")
    fee11g = block(t, "FeesForServicesOtherGrp")
    o_lines = tuple(
        (unescape(m.group(1)).strip(), unescape(m.group(2)).strip())
        for m in re.finditer(r"<FormAndLineReferenceDesc>([^<]*)</FormAndLineReferenceDesc>\s*"
                             r"<ExplanationTxt>([^<]*)</ExplanationTxt>", sched_o))
    return dict(
        object_id=oid,
        ein=leaf(t, "EIN"),
        begin=leaf(t, "TaxPeriodBeginDt"),
        end=leaf(t, "TaxPeriodEndDt"),
        return_ts=leaf(t, "ReturnTs"),
        is_990=bool(re.search(r"<(?:\w+:)?ReturnTypeCd>990<", t)),
        amended=leaf(t, "AmendedReturnInd") in ("X", "1", "true"),
        daf_contrib=num(leaf(sched_d, "DonorAdvisedFundsContriAmt")) if sched_d else None,
        fs_audited=leaf(t, "FSAuditedInd"),
        part_ix_11g=num(leaf(fee11g, "TotalAmt")) if fee11g else None,
        sched_o_fee_lines=tuple(x for x in o_lines if SCHED_O_RE.search(x[1])),
    )


def days(b, e):
    import datetime as dt
    try:
        return (dt.date.fromisoformat(e) - dt.date.fromisoformat(b)).days + 1
    except ValueError:
        return 0


def select_returns(parsed):
    """One full-year 990 per (EIN, tax year = begin year); latest ReturnTs wins (amendments supersede)."""
    full = tuple(p for p in parsed if p["is_990"] and days(p["begin"], p["end"]) >= 300)
    keyed = functools.reduce(
        lambda acc, p: {**acc, (p["ein"], int(p["begin"][:4])): max(
            (acc.get((p["ein"], int(p["begin"][:4]))) or p, p), key=lambda r: r["return_ts"])},
        full, {})
    dropped = tuple(p for p in parsed if p not in keyed.values())
    return keyed, dropped


# ---------------------------------------------------------------------------------------------------------
# DAFRC panel with applied corrections
# ---------------------------------------------------------------------------------------------------------
def dafrc_contrib(root):
    panel = read_csv(os.path.join(root, MISSION, "dafrc-sponsor-schedule-d-fy2019-2024.csv"))
    corr = read_csv(os.path.join(root, MISSION, "dafrc-corrections-itemized.csv"))
    base = {(r["ein"], int(r["fiscal_year_end"])): (num(r["total_daf_contributions"]), r["source_total_daf_contributions"])
            for r in panel}
    fixes = {(r["ein"], int(r["fiscal_year"])): (num(r["corrected_value"]), "corrected: " + r["rule"])
             for r in corr if r["metric"] == "daf_contributions" and r["applied"] == "1"}
    return {**base, **fixes}


# ---------------------------------------------------------------------------------------------------------
# Dechomai grants by sponsor x year
# ---------------------------------------------------------------------------------------------------------
def dechomai_lines(root):
    rows = read_csv(os.path.join(root, MISSION, "dechomai-dafpay-2026-11-19.csv"))
    return tuple(r for r in rows if r["record_type"] == "sched_i" and r["selected"] == "1"
                 and r["category"] != "DECHOMAI_INTRA")


def line_amount(r):
    return (num(r["amount_usd"]) or 0.0) + (num(r["amount2_usd"]) or 0.0)


def matches(sp, r, attribution):
    if attribution == "ein":
        return r["counterparty_ein"] == sp["ein"]
    if sp["group"]:
        return r["sponsor_group"] == sp["group"]
    return r["counterparty_ein"] == sp["ein"] or bool(re.search(sp["name_re"], r["counterparty"].upper()))


def grants(lines, sp, year, attribution):
    sel = tuple(r for r in lines if int(r["tax_year"]) == year and matches(sp, r, attribution))
    return sum(map(line_amount, sel)), len(sel)


def routing_check(root, lines):
    """Reproduce the source study's group totals (routing_dechomai_to_sponsor rows)."""
    rows = read_csv(os.path.join(root, MISSION, "dechomai-dafpay-2026-11-19.csv"))
    ref = {(r["sponsor_group"], r["tax_year"]): num(r["amount_usd"]) for r in rows
           if r["record_type"] == "routing_dechomai_to_sponsor" and r["tax_year"].isdigit()}
    mine = {(sp["group"], str(y)): grants(lines, sp, y, "name")[0]
            for sp in SPONSORS_A if sp["group"] for y in DECHOMAI_YEARS}
    return tuple((k, ref.get(k), v) for k, v in sorted(mine.items()) if abs((ref.get(k) or 0) - v) > 0.5)


# ---------------------------------------------------------------------------------------------------------
# (A) rows
# ---------------------------------------------------------------------------------------------------------
HEAD_A = ("row_type", "sponsor", "sponsor_ein", "sponsor_fy_end_month", "dechomai_year", "attribution",
          "match_variant", "sponsor_tax_year", "sponsor_period_begin", "sponsor_period_end", "sponsor_object_id",
          "dechomai_grants_usd", "dechomai_schedule_i_lines", "sponsor_daf_contributions_sched_d_usd",
          "dafrc_fy", "dafrc_corrected_daf_contributions_usd", "dafrc_value_source", "sched_d_minus_dafrc_usd",
          "share_of_sponsor_daf_contributions", "flags", "source_url")


def sponsor_value(returns, ein, ty):
    r = returns.get((ein, ty))
    if not r:
        return None, None
    if r["end"] < "2021-01-01":
        return r, "pre_2021_period_excluded"
    return r, None


def variant_rows(sp, year, attribution, g, nlines, returns, dafrc):
    def one(variant, ty):
        r, flag = sponsor_value(returns, sp["ein"], ty)
        contrib = r["daf_contrib"] if r and not flag else None
        dfy = int(r["end"][:4]) if r else None
        dv, dsrc = dafrc.get((sp["ein"], dfy), (None, "")) if r else (None, "")
        flags = ";".join(x for x in (
            flag or ("" if r else "pre_2021_period_excluded_not_read" if sp["fy_end_month"] == 12 and ty < 2021
                     else "no_return_filed_or_not_yet_public"),
            "amended_return" if r and r["amended"] else "",
            "sched_d_ne_dafrc" if contrib is not None and dv is not None and abs(contrib - dv) > 0.5 else "",
        ) if x)
        return dict(row_type="year", sponsor=sp["sponsor"], sponsor_ein=sp["ein"],
                    sponsor_fy_end_month=sp["fy_end_month"], dechomai_year=year, attribution=attribution,
                    match_variant=variant, sponsor_tax_year=ty,
                    sponsor_period_begin=r["begin"] if r else "", sponsor_period_end=r["end"] if r else "",
                    sponsor_object_id=r["object_id"] if r else "", dechomai_grants_usd=fmt(g),
                    dechomai_schedule_i_lines=nlines,
                    sponsor_daf_contributions_sched_d_usd=fmt(contrib),
                    dafrc_fy=dfy or "", dafrc_corrected_daf_contributions_usd=fmt(dv) if r and not flag else "",
                    dafrc_value_source=dsrc if r and not flag else "",
                    sched_d_minus_dafrc_usd=fmt(contrib - dv) if contrib is not None and dv is not None else "",
                    share_of_sponsor_daf_contributions=fmt(g / contrib, 6) if contrib else "",
                    flags=flags, source_url=MIRROR.format(r["object_id"]) if r else "")

    base = (one("primary_ty_t", year), one("alt_ty_t_minus_1", year - 1), one("alt_ty_t_plus_1", year + 1))
    if sp["fy_end_month"] != 12:
        a, b = base[1], base[0]
        ca, cb = num(a["sponsor_daf_contributions_sched_d_usd"]), num(b["sponsor_daf_contributions_sched_d_usd"])
        blend = 0.5 * ca + 0.5 * cb if ca is not None and cb is not None else None
        base = base + (dict(b, match_variant="overlap_weighted_fy_end_t_and_t_plus_1", sponsor_tax_year="",
                            sponsor_period_begin=a["sponsor_period_begin"], sponsor_object_id=
                            a["sponsor_object_id"] + ";" + b["sponsor_object_id"],
                            sponsor_daf_contributions_sched_d_usd=fmt(blend), dafrc_fy="",
                            dafrc_corrected_daf_contributions_usd="", dafrc_value_source="",
                            sched_d_minus_dafrc_usd="", share_of_sponsor_daf_contributions=
                            fmt(g / blend, 6) if blend else "", flags="0.5 x each FY overlapping CY t",
                            source_url=a["source_url"] + " ; " + b["source_url"]),)
    return base


def pooled_rows(year_rows):
    """Pooled 2021-2024 (all four years, blank if any sponsor year is missing) and, for every variant, the same
    ratio over only the Dechomai years whose matched sponsor return exists (years listed in `flags`)."""
    keys = sorted({(r["sponsor"], r["attribution"], r["match_variant"]) for r in year_rows})

    def pool(k, kind):
        rs_all = tuple(sorted((r for r in year_rows if (r["sponsor"], r["attribution"], r["match_variant"]) == k),
                              key=lambda r: int(r["dechomai_year"])))
        rs = rs_all if kind == "all" else tuple(r for r in rs_all if r["sponsor_daf_contributions_sched_d_usd"])
        complete = all(r["sponsor_daf_contributions_sched_d_usd"] for r in rs) and bool(rs)
        g = sum(num(r["dechomai_grants_usd"]) for r in rs)
        c = sum(num(r["sponsor_daf_contributions_sched_d_usd"]) or 0 for r in rs)
        yrs = ",".join(str(r["dechomai_year"]) for r in rs)
        return dict(rs_all[0], row_type="pooled_2021_2024" if kind == "all" else "pooled_available_years",
                    dechomai_year="2021-2024" if kind == "all" else yrs, sponsor_tax_year="",
                    sponsor_period_begin="", sponsor_period_end="", sponsor_object_id="",
                    dechomai_grants_usd=fmt(g), dechomai_schedule_i_lines=sum(int(r["dechomai_schedule_i_lines"])
                                                                               for r in rs),
                    sponsor_daf_contributions_sched_d_usd=fmt(c) if complete else "",
                    dafrc_fy="", dafrc_corrected_daf_contributions_usd="", dafrc_value_source="",
                    sched_d_minus_dafrc_usd="", share_of_sponsor_daf_contributions=fmt(g / c, 6)
                    if complete and c else "",
                    flags=("" if complete else "incomplete: a sponsor year is missing or pre-2021")
                    if kind == "all" else f"Dechomai years with a matched sponsor return: {yrs}",
                    source_url="sum of the year rows above")
    full = tuple(pool(k, "all") for k in keys)
    part = tuple(pool(k, "available") for k in keys
                 if any(not r["sponsor_daf_contributions_sched_d_usd"] for r in year_rows
                        if (r["sponsor"], r["attribution"], r["match_variant"]) == k))
    return full + part


def build_a(root, returns):
    lines = dechomai_lines(root)
    dafrc = dafrc_contrib(root)
    mism = routing_check(root, lines)
    year_rows = tuple(
        row
        for sp in SPONSORS_A
        for year in DECHOMAI_YEARS
        for attribution in ("name", "ein")
        for g, n in (grants(lines, sp, year, attribution),)
        if attribution == "name" or (g, n) != grants(lines, sp, year, "name")
        for row in variant_rows(sp, year, attribution, g, n, returns, dafrc))
    # an EIN-attribution variant exists only for sponsor-years whose total changes; carry the name rows for the
    # other years so the pooled EIN total is complete
    ein_keys = {(r["sponsor"], r["dechomai_year"]) for r in year_rows if r["attribution"] == "ein"}
    ein_sponsors = {s for s, _ in ein_keys}
    filler = tuple(dict(r, attribution="ein") for r in year_rows
                   if r["attribution"] == "name" and r["sponsor"] in ein_sponsors
                   and (r["sponsor"], r["dechomai_year"]) not in ein_keys)
    order = {sp["sponsor"]: i for i, sp in enumerate(SPONSORS_A)}
    all_years = tuple(sorted(year_rows + filler, key=lambda r: (order[r["sponsor"]], r["attribution"] != "name",
                                                                 r["attribution"], int(r["dechomai_year"]))))
    return all_years + pooled_rows(all_years), mism


# ---------------------------------------------------------------------------------------------------------
# (B) audited statements: figures as reported (USD; documents in thousands are converted x1000 and flagged)
# fee_recognition: revenue_line | expense_passthrough | eliminated_interfund | netted_not_disclosed |
#                  not_disclosed | n/a
# ---------------------------------------------------------------------------------------------------------
U = dict(
    fid24="https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf",
    van25="https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf",
    rcf24="https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf",
    jcf24="https://jcfny.org/app/uploads/2025/07/JCF-FINAL-FS-FY2024.pdf",
    cjp24="https://www.cjp.org/hubfs/Financial%20Statements/2024/Audited%20Financial%20Statements%202023%E2%80%932024.pdf",
    cjp23="https://www.cjp.org/hubfs/Financial%20Statements/2023/Audited%20Financial%20Statements%202022%E2%80%932023.pdf",
    ncf24="https://site.ncfgiving.com/wp-content/uploads/2026/07/NCF-24-Consolidated-FS-Final.pdf",
    fftc24="https://www.fftc.org/sites/default/files/2025-09/Foundation_For_The_Carolinas_12-31-24_Audited_Financials.pdf",
    gkc24="https://growyourgiving.org/wp-content/uploads/2025/11/Audit-Report-2024.pdf",
    svcf24="https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf",
    col24="https://columbusfoundation.org/media/lnobyvu5/2024-columbus-foundation-combined-final-financial-statements-12-31-24.pdf",
    nyct24="https://thenytrust.org/wp-content/uploads/2025/11/2024-Issued-Audited-Financial-Statements.pdf",
    cct24="https://www.cct.org/wp-content/uploads/2025/03/2024_TheChicagoCommunityTrust_FS.pdf",
    npt24="https://www.nptrust.org/consolidated-statements-2024-npt",
)
# text file stems (pdftotext -layout output names used in this run; checked only when --audit-text-dir is given)
TXT = dict(fid24="802fbe_audited-financial-statements-2024-2023", van25="e6c8c5_vanguard-charitable-2025-financial-statements",
           rcf24="e6cf79_2024RCFAuditedFinancialStatements", jcf24="a70af0_JCF-FINAL-FS-FY2024",
           cjp24="c94784_Audited Financial Statements 2023–2024", cjp23="cjp2023",
           ncf24="61d908_NCF-24-Consolidated-FS-Final",
           fftc24="bd8474_Foundation_For_The_Carolinas_12-31-24_Audited_Financials", gkc24="ea0e3b_Audit-Report-2024",
           svcf24="3557af_svcf-financial-statement-audit-2024",
           col24="7738d8_2024-columbus-foundation-combined-final-financial-statements-12-31-24",
           nyct24="a2c2e0_2024-Issued-Audited-Financial-Statements", cct24="f312a0_2024_TheChicagoCommunityTrust_FS",
           npt24="e83db1_Consolidated-Statements-2024-NPT")


def A(doc, fy, recog, fee=None, ext=None, opex=(), thousands=False, liq=None, other=None, other_label="",
      note=""):
    """opex: tuple of (label, amount) components as printed; fee/ext/liq/other as printed."""
    k = 1000 if thousands else 1
    return dict(doc=doc, fy=fy, recog=recog, fee=fee, ext=ext, opex=opex, k=k, liq=liq, other=other,
                other_label=other_label, note=note)


AUDIT = {
    "110303001": (
        A("fid24", 2024, "expense_passthrough", fee=139686600,
          opex=(("Administrative fees", 139686600), ("Professional fees", 1216669), ("Other expenses", 20670116)),
          liq=59520504856,
          note="Statement of activities expense 'Administrative fees'; Note 7: Gift Fund paid FMR 'amounts equal to "
               "the administrative fee the Gift Fund charged its donors'. Fee is never revenue; sponsor-level margin "
               "on it is zero by contract. Excludes investment management fees ($67,308,635)."),
        A("fid24", 2023, "expense_passthrough", fee=121190522,
          opex=(("Administrative fees", 121190522), ("Professional fees", 1308861), ("Other expenses", 9982465)),
          liq=50198224585, note="As FY2024. Excludes investment management fees ($53,687,639)."),
    ),
    "232888152": (
        A("van25", 2024, "netted_not_disclosed",
          opex=(("Management and general", 6513666), ("Program", 26465388), ("Fundraising", 3833010)),
          note="Note 7: 0.60% base fee 'is wrapped in with investment income'; amount not disclosed. Fee paid to "
               "Vanguard for recordkeeping/administration $3,916,396 (FY2024), inside the expense lines. FY2023 "
               "statements not found on the sponsor's site (FY2025 statements read; FY2026 in repo)."),
    ),
    "352129262": (
        A("rcf24", 2024, "revenue_line", fee=19617095,
          opex=(("Management and general", 19454266), ("Fundraising", 13321)),
          note="Revenue line 'Administrative fees'. Note 9: Ren is paid 98% of administrative fee revenue "
               "($19,225,546 in 2024). Program services ($770.8m) are grants."),
        A("rcf24", 2023, "revenue_line", fee=16097870,
          opex=(("Management and general", 15807861), ("Fundraising", 10204)),
          note="Comparative column of the 2024 statements. Ren paid $15,543,682 (98% of fee revenue)."),
    ),
    "237174183": (
        A("jcf24", 2024, "eliminated_interfund", fee=11789740,
          opex=(("Program subtotal less grants to philanthropic institutions", 978812021 - 977404828),
                ("Management and general", 4578533), ("Fund-raising", 1958832)),
          liq=2776336368, other=2000000, other_label="grant to UJA from operating fund",
          note="Note C: fee 'reduces the value of the donor-advised funds and increases the value of JCF's "
               "operating fund'; total administrative fees $11,789,740. Fees and interest in excess of operating "
               "expenses go to UJA, the Special Gifts Fund or a capital reserve."),
        A("jcf24", 2023, "eliminated_interfund", fee=11032543,
          opex=(("Program subtotal less grants to philanthropic institutions", 883131609 - 881794242),
                ("Management and general", 5480386), ("Fund-raising", 1977005)),
          liq=2707811127, other=2000000, other_label="grant to UJA from operating fund",
          note="Comparative year in the FY2024 statements."),
    ),
    "042103559": (
        A("cjp24", 2024, "eliminated_interfund", fee=1642, thousands=True,
          note="Consolidating schedule: 'Administrative service fees' (1,642) paid by the Donor Advised Funds area "
               "to CJP Operations; eliminated in consolidation. CJP Operations is the federation's whole operating "
               "budget, so no DAF-programme margin can be computed."),
        A("cjp23", 2023, "eliminated_interfund", fee=1582, thousands=True,
          note="FY2023 consolidating schedule (2022-2023 statements); DAF area column (1,582)."),
    ),
    "581493949": (
        A("ncf24", 2024, "eliminated_interfund", fee=47411, thousands=True,
          opex=(("General and administrative (NCCF column)", 106619), ("Fund-raising activities (NCCF column)", 17572)),
          other=61122, other_label="ministry support fees and assessments eliminated in consolidation (all entities)",
          note="Consolidating statement, NCCF column, 'Administrative fees and assessments'. Ministry support fees "
               "move to the operating fund when assets are sold or income received; a portion goes to Affiliates. "
               "NCCF 'Program activities' ($2,589m) mix grants and programme cost, so opex here is G&A + "
               "fund-raising only."),
        A("ncf24", 2023, "eliminated_interfund", fee=42004, thousands=True,
          opex=(("General and administrative (NCCF column)", 95570), ("Fund-raising activities (NCCF column)", 15908)),
          other=55165, other_label="ministry support fees and assessments eliminated in consolidation (all entities)",
          note="2023 consolidating statement in the 2024 report."),
    ),
    "566047886": (
        A("fftc24", 2024, "not_disclosed", ext=3979826,
          opex=(("Other program services", 23318554), ("Management and general", 26818007),
                ("Fundraising and development", 2040179)),
          note="'Administrative fees received' is a revenue line for funds administered for others; internal "
               "DAF fees are eliminated and not disclosed. Endowment roll-forward shows 'Administrative fees and "
               "expenses' of $4,358,499 charged to endowment."),
        A("fftc24", 2023, "not_disclosed", ext=4035907,
          opex=(("Other program services", 22166571), ("Management and general", 24725133),
                ("Fundraising and development", 1880312)),
          note="2023 statement in the 2024 report. Endowment admin fees and expenses $3,490,979."),
    ),
    "431152398": (
        A("gkc24", 2024, "not_disclosed", ext=1806759,
          opex=(("Donor services expenses", 6029221), ("Program direct fund expenses", 10828572),
                ("Administrative expenses", 4346236), ("Development expenses", 2092062)),
          other=8687500, other_label="operating reserve balance",
          note="Consolidated with Greater Horizons (rank 17). 'Income from services' is back-office and pooled-"
               "investment fees from other entities. Operating fund pays all operating expenses; reserve target "
               ">= 50% of annual operating expenses. Internal DAF fee not disclosed."),
        A("gkc24", 2023, "not_disclosed", ext=1915649,
          opex=(("Donor services expenses", 5612380), ("Program direct fund expenses", 10429204),
                ("Administrative expenses", 3424768), ("Development expenses", 1929281)),
          other=8082783, other_label="operating reserve balance", note="Comparative year."),
    ),
    "205205488": (
        A("svcf24", 2024, "not_disclosed", thousands=True,
          opex=(("Program", 45395), ("General and administrative", 20313), ("Fundraising and development", 3245)),
          note="Statements in thousands; consolidated with supporting organizations (net assets $14.35bn vs 990 "
               "Part X $10.5bn). Only the endowed-fund 'support fee' policy (0.5-1.5%) is described; DAF fee "
               "revenue not disclosed."),
        A("svcf24", 2023, "not_disclosed", thousands=True,
          opex=(("Program", 48685), ("General and administrative", 19631), ("Fundraising and development", 4255)),
          note="Comparative year."),
    ),
    "316044264": (
        A("col24", 2024, "not_disclosed",
          opex=(("Columbus Foundation operating expenses", 15461713), ("Fund expenses", 1813091)),
          note="Combined statements (all funds incl. supporting organizations). Fund charges are internal and not "
               "disclosed."),
        A("col24", 2023, "not_disclosed",
          opex=(("Columbus Foundation operating expenses", 14800397), ("Fund expenses", 1402923)),
          note="2023 statement in the 2024 report."),
    ),
    "133062214": (
        A("nyct24", 2024, "not_disclosed", ext=993322,
          opex=(("Administrative", 11372348), ("Development", 4703123)),
          note="'Program' revenue $993,322 is external. Program expenses ($213.5m) include grants and cannot be "
               "split on the face of the statement, so opex here is administrative + development only."),
        A("nyct24", 2023, "not_disclosed", ext=954389,
          opex=(("Administrative", 9389165), ("Development", 3886470)), note="Comparative year."),
    ),
    "362167000": (
        A("cct24", 2024, "not_disclosed",
          opex=(("Program-related expenses", 6842833), ("Administrative expenses", 25047150), ("Other expenses", 107042)),
          other=152216654, other_label="excess of operating support, revenue and transfers over expenses (as reported)",
          note="FY ends 30 Sep. Operating/nonoperating split: $1.49bn transferred from nonoperating (mainly DAFs) to "
               "match committed grants. The reported operating excess is not a fee margin. DAF fee not disclosed."),
        A("cct24", 2023, "not_disclosed",
          opex=(("Program-related expenses", 10929328), ("Administrative expenses", 23650203), ("Other expenses", 53998)),
          other=106967896, other_label="excess of operating support, revenue and transfers over expenses (as reported)",
          note="Comparative year."),
    ),
    "237825575": (
        A("npt24", 2024, "not_disclosed", ext=994, thousands=True,
          opex=(("Program services", 94289), ("Fundraising", 12025), ("General and administrative", 28661)),
          note="Summary consolidated statements (in thousands) without an auditor's report or notes. "
               "'Administrative and maintenance fees' ($994k) is the only fee line; internal DAF fee not shown."),
        A("npt24", 2023, "not_disclosed", ext=897, thousands=True,
          opex=(("Program services", 71021), ("Fundraising", 10264), ("General and administrative", 24422)),
          note="Comparative year."),
    ),
}

# sponsors without a readable audit (status, url, note)
NO_AUDIT = {
    "311640316": ("blocked_http_403", "https://www.dafgiving360.org/about-schwab-charitable/financials",
                  "Financials page lists 'Financial Statements' (search snippet) but robots.txt and the page both return "
                  "HTTP 403 to a generic client; not bypassed."),
    "311774905": ("not_public", "", "No statements on a sponsor site; gsphilanthropyfund.org robots.txt unreachable. "
                  "990: FSAuditedInd true."),
    "341747398": ("on_request", "https://www.aefonline.org/about-aef/", "Audited statements available on request "
                  "only (repo sponsor-audit-notes.csv); not requested (no outreach)."),
    "527082731": ("not_public", "https://www.morganstanley.com/gift", "Page shows '*Audited figures as of Q4 2024' "
                  "for headline figures only; no statements posted."),
    "046010342": ("not_public", "", "No statements on a sponsor site (repo sponsor-audit-notes.csv)."),
    "262048480": ("on_request", "https://impactassets.org/required-state-disclosures/",
                  "Information 'may be obtained, without cost, by writing to its principal place of business'; not "
                  "requested."),
    "200849590": ("consolidated_in_gkccf", "https://growyourgiving.org/wp-content/uploads/2025/11/Audit-Report-2024.pdf",
                  "Greater Horizons is consolidated in the GKCCF audit (rank 16 row)."),
    "260724604": ("not_public", "https://dechomai.org/faqs/", "No statements posted; consolidated audit not obtained "
                  "(b40n14-b38c §5)."),
    "593652538": ("blocked_robots_unreachable", "https://www.rjcef.com/", "robots.txt could not be read (connection "
                  "error), so nothing was fetched."),
    "141782466": ("blocked_robots_unreachable", "https://www.aycocharitable.com/", "robots.txt could not be read; "
                  "nothing fetched."),
    "311663020": ("blocked_http_403", "https://www.uscharitablegifttrust.org/", "Site returns HTTP 403 to a generic "
                  "client; not bypassed."),
    "237315673": ("blocked_robots_disallow",
                  "https://oregoncf.org/assets/PDFs-and-Docs/PDFs/Financial/OCF-FY-2024-Financial-Statements-Final.pdf",
                  "Statements are posted, but robots.txt has 'Disallow: /assets', so the PDF was not fetched."),
}

HEAD_B = ("rank_fy2024_daf_assets", "ein", "sponsor_name", "sponsor_group", "fiscal_year", "fy_end",
          "audit_status", "audit_document_url", "reported_in_thousands", "fee_recognition",
          "internal_daf_fee_usd", "external_fee_revenue_usd", "audit_operating_expenses_usd",
          "audit_operating_expenses_components", "audit_fee_less_opex_usd", "audit_fee_margin_pct",
          "internal_fee_bps_of_avg_daf_value",
          "audit_other_figure_usd", "audit_other_figure_label", "liquidity_available_1yr_usd",
          "figures_verified_in_text", "tax_year_990", "object_id_990", "fs_audited_ind_990",
          "r1_nondaf_na_eoy_990_usd", "delta_r1_990_usd", "operating_cost_990_usd", "delta_r1_per_opcost_990",
          "part_ix_11g_other_fees_990_usd", "sched_o_fee_lines_n", "sched_o_fee_line_refs",
          "delta_r1_minus_audit_fee_less_opex_usd", "note", "source_990_url")


def verify(a, text_dir):
    if not text_dir:
        return ""
    p = os.path.join(text_dir, TXT[a["doc"]] + ".txt")
    if not os.path.exists(p):
        return "text_missing"
    with open(p, encoding="utf-8", errors="replace") as f:
        t = re.sub(r"\s+", " ", f.read())
    figs = tuple(v for v in (a["fee"], a["ext"], a["liq"], a["other"]) if v) + tuple(
        v for lbl, v in a["opex"] if "less grants" not in lbl)
    found = tuple(f"{int(v):,}" in t for v in figs)
    return f"{sum(found)}/{len(found)}"


def audit_row(base, a, text_dir):
    k = a["k"]
    opex = sum(v for _, v in a["opex"]) * k if a["opex"] else None
    fee = a["fee"] * k if a["fee"] is not None else None
    margin_ok = fee is not None and opex is not None and a["recog"] in ("revenue_line", "eliminated_interfund",
                                                                        "expense_passthrough")
    less = fee - opex if margin_ok else None
    return dict(base, audit_status="read" if a["doc"] != "npt24" else "summary_only_no_auditor_report",
                audit_document_url=U[a["doc"]], reported_in_thousands="yes" if k == 1000 else "no",
                fee_recognition=a["recog"], internal_daf_fee_usd=fmt(fee),
                external_fee_revenue_usd=fmt(a["ext"] * k if a["ext"] is not None else None),
                audit_operating_expenses_usd=fmt(opex),
                audit_operating_expenses_components="; ".join(f"{lbl}={v}" for lbl, v in a["opex"]),
                audit_fee_less_opex_usd=fmt(less), audit_fee_margin_pct=fmt(100 * less / fee, 2) if less is not None
                and fee else "", audit_other_figure_usd=fmt(a["other"] * k if a["other"] is not None else None),
                audit_other_figure_label=a["other_label"], liquidity_available_1yr_usd=fmt(a["liq"]),
                figures_verified_in_text=verify(a, text_dir), note=a["note"])


def build_b(root, parsed_by_oid, text_dir):
    res = read_csv(os.path.join(root, MISSION, "sponsor-financial-resilience-2021-2024.csv"))
    top = tuple(r for r in res if r["row_type"] == "sponsor_year" and r["fy2024_asset_rank"]
                and int(r["fy2024_asset_rank"]) <= 25)
    by_fy = {(r["ein"], int(r["tax_period_end"][:4])): r for r in top}
    sponsors = sorted({(int(r["fy2024_asset_rank"]), r["ein"], r["sponsor_name"], r["sponsor_group"]) for r in top})

    def row(rank, ein, name, grp, fy):
        r = by_fy.get((ein, fy), {})
        x = parsed_by_oid.get(r.get("object_id"), {})
        o = x.get("sched_o_fee_lines", ())
        vals = dict(rank_fy2024_daf_assets=rank, ein=ein, sponsor_name=name, sponsor_group=grp, fiscal_year=fy,
                    fy_end=r.get("tax_period_end", ""), tax_year_990=r.get("tax_year", ""),
                    object_id_990=r.get("object_id", ""), fs_audited_ind_990=x.get("fs_audited", ""),
                    r1_nondaf_na_eoy_990_usd=r.get("r1_nondaf_na", ""), delta_r1_990_usd=r.get("r1_change_yoy", ""),
                    operating_cost_990_usd=r.get("operating_cost", ""),
                    delta_r1_per_opcost_990=r.get("r1_change_per_opcost", ""),
                    part_ix_11g_other_fees_990_usd=fmt(x.get("part_ix_11g")),
                    sched_o_fee_lines_n=len(o), sched_o_fee_line_refs=" | ".join(
                        f"{ref[:60]}: {txt[:160]}" for ref, txt in o[:3]),
                    source_990_url=MIRROR.format(r["object_id"]) if r.get("object_id") else "")
        base = {**{k: "" for k in HEAD_B}, **vals}
        a = next((a for a in AUDIT.get(ein, ()) if a["fy"] == fy), None)
        if a:
            out = audit_row(base, a, text_dir)
        elif ein in AUDIT:
            out = dict(base, audit_status="year_not_found",
                       note=f"Sponsor statements read for another year only; FY{fy} statements not located.")
        else:
            st, url, note = NO_AUDIT.get(ein, ("not_searched", "", ""))
            out = dict(base, audit_status=st, audit_document_url=url, note=note)
        d = num(out.get("delta_r1_990_usd")), num(out.get("audit_fee_less_opex_usd"))
        dv = num(r.get("daf_value_eoy")), num(by_fy.get((ein, fy - 1), {}).get("daf_value_eoy"))
        fee = num(out.get("internal_daf_fee_usd"))
        bps = 1e4 * fee / ((dv[0] + dv[1]) / 2) if fee and None not in dv and dv[0] + dv[1] > 0 else None
        return dict(out, delta_r1_minus_audit_fee_less_opex_usd=fmt(d[0] - d[1]) if None not in d else "",
                    internal_fee_bps_of_avg_daf_value=fmt(bps, 1) if bps is not None else "")

    return tuple(row(*s, fy) for s in sponsors for fy in (2023, 2024))


def summary_b(rows):
    read = tuple(r for r in rows if r["audit_status"] in ("read", "summary_only_no_auditor_report"))
    fee = tuple(r for r in read if r["internal_daf_fee_usd"])
    marg = tuple(r for r in fee if r["audit_fee_margin_pct"])
    return dict(sponsor_years=len(rows), sponsors=len({r["ein"] for r in rows}),
                sponsor_years_with_statement=len(read),
                sponsors_with_statement=len({r["ein"] for r in read}),
                sponsor_years_with_internal_fee=len(fee), sponsors_with_internal_fee=len({r["ein"] for r in fee}),
                margins=tuple((r["sponsor_name"], r["fiscal_year"], r["audit_fee_margin_pct"],
                               r["delta_r1_990_usd"], r["audit_fee_less_opex_usd"]) for r in marg),
                statuses=dict(sorted({s: sum(1 for r in rows if r["audit_status"] == s and r["fiscal_year"] == 2024)
                                      for s in {r["audit_status"] for r in rows}}.items())))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--audit-text-dir", default="")
    ap.add_argument("--out-a", default=OUT_A)
    ap.add_argument("--out-b", default=OUT_B)
    a = ap.parse_args(argv)
    files = sorted(os.path.join(a.xml_dir, f) for f in os.listdir(a.xml_dir) if f.endswith(".xml"))
    parsed = tuple(map(parse_return, files))
    returns, dropped = select_returns(parsed)
    rows_a, mism = build_a(a.root, returns)
    n_a = write_csv(os.path.join(a.root, a.out_a), HEAD_A, rows_a)
    rows_b = build_b(a.root, {p["object_id"]: p for p in parsed}, a.audit_text_dir)
    n_b = write_csv(os.path.join(a.root, a.out_b), HEAD_B, rows_b)
    print(f"xml files {len(files)}; selected returns {len(returns)}; not selected "
          f"{[(p['object_id'], p['begin'], p['end']) for p in dropped if p['ein'] in {s['ein'] for s in SPONSORS_A}]}")
    print(f"routing check vs source study: {'all group-years reproduced' if not mism else mism}")
    print(f"A rows {n_a} -> {a.out_a}; B rows {n_b} -> {a.out_b}")
    prim = tuple(r for r in rows_a if r["match_variant"] == "primary_ty_t" and r["attribution"] == "name")
    tuple(print("A", r["sponsor"], r["dechomai_year"], r["dechomai_grants_usd"],
                r["sponsor_daf_contributions_sched_d_usd"], r["share_of_sponsor_daf_contributions"]) for r in prim)
    print("B summary", summary_b(rows_b))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
