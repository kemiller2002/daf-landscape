#!/usr/bin/env python3
"""b49-03: bequests and estate flows into and out of DAFs at the FY2024 top-20 sponsors.

Builds data/mission-2026-11-14/bequests-legacy-dafs-2026-11-20.csv from two inputs:

  1. POLICY: hand-coded readings of sponsor policy documents (quotes copied from the
     documents). Each quote is re-checked against the saved text of the document
     (--web-dir); the CSV column quote_verified records the result.
  2. FILINGS: the latest Form 990 e-file XML per sponsor (IRS TEOS index, GivingTuesday
     mirror of the XML). Extracts Part VIII contributions, Schedule D Part I line 2,
     Schedule M lines by type, Form 8283 count, and every free-text element that
     mentions bequest/estate/IRA/insurance/remainder-trust words.

Usage (pass '.' as root):
  python3 -I scripts/mission_b49_03_estate_flows.py . --web-dir W --irs-dir D [--irs-dir D2]
        --xml-cache C [--xml-cache C2] --xml-dir X [--fetch]

Stdlib only; functional style (no mutable globals).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from functools import reduce
from typing import Iterable, Mapping, Sequence

UA = {"User-Agent": "research-script/1.0"}
XML_URL = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
OUT = "data/mission-2026-11-14/bequests-legacy-dafs-2026-11-20.csv"
RETRIEVED = "2026-11-20"

SPONSORS = (
    (1, "Fidelity Charitable", "110303001"),
    (2, "National Philanthropic Trust", "237825575"),
    (3, "DAFgiving360 (formerly Schwab Charitable)", "311640316"),
    (4, "Vanguard Charitable", "232888152"),
    (5, "GS DAF (Goldman Sachs Philanthropy Fund)", "311774905"),
    (6, "Silicon Valley Community Foundation", "205205488"),
    (7, "American Endowment Foundation", "341747398"),
    (8, "Morgan Stanley GIFT", "527082731"),
    (9, "Renaissance Charitable Foundation", "352129262"),
    (10, "National Christian Foundation", "581493949"),
    (11, "Bank of America Charitable Gift Fund", "046010342"),
    (12, "The Chicago Community Trust", "362167000"),
    (13, "ImpactAssets", "262048480"),
    (14, "Foundation For The Carolinas", "566047886"),
    (15, "Jewish Communal Fund", "237174183"),
    (16, "Greater Kansas City Community Foundation", "431152398"),
    (17, "Greater Horizons", "200849590"),
    (18, "Dechomai Asset Trust", "260724604"),
    (19, "Combined Jewish Philanthropies (CJP)", "042103559"),
    (20, "Raymond James Charitable", "593652538"),
)

# Documents: key -> (url, saved text path relative to --web-dir, document date, robots status)
DOCS = {
    "FID_PG": ("https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf", "dl/86f1176fe6b3.pdf.txt", "2026-09 (PDF created 2026-09-11)", "allowed"),
    "FID_FAQ": ("https://www.fidelitycharitable.org/faqs/all/who-can-be-successor.html", "dl/48e6b65ecabb.html.txt", "live 2026-11-20", "allowed"),
    "NPT_GUIDE": ("https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf", "dl/b869fd9e987e.pdf.txt", "2026-10 (PDF created 2026-10-15)", "allowed"),
    "VC_PG": ("https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf", "dl/2f93e985dbc3.pdf.txt", "2026-01", "allowed"),
    "VC_DEF": ("https://www.vanguardcharitable.org/contributions/deferred-giving", "dl/4d8a922534a4.html.txt", "live 2026-11-20", "allowed"),
    "SVCF_AGR": ("https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", "dl/13c884fae3d3.pdf.txt", "2025 (PDF modified 2025-08-22)", "allowed"),
    "AEF_BOOK": ("https://advisorwelcome.aefonline.org/wp-content/uploads/2026/01/AEF-DAF-Giving-Guide-Booklet_General_FINAL-1.pdf", "dl/7c71cbf74e38.pdf.txt", "2026-01 (upload path)", "allowed"),
    "AEF_BEQ": ("https://www.aefonline.org/bequests", "dl/758bd80eaf64.html.txt", "live 2026-11-20", "allowed"),
    "AEF_FACT": ("https://www.aefonline.org/wp-content/uploads/2026/04/AEF_Difference_Fact-Sheet_2026.pdf", "dl/77a4d33a3ee8.pdf.txt", "2026-04", "allowed"),
    "MS_CIRC": ("https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf", "ocr/ms_circular.txt", "2024-08 (PDF created 2024-08-22; text by OCR)", "robots.txt 404 (no rules)"),
    "MS_DCA": ("https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Contribution%20Agreement.pdf", "dl/e72b6ac329a7.pdf.txt", "2024-07 (form CGPCDOCA 07/2024)", "robots.txt 404 (no rules)"),
    "RCF_LPL": ("https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf", "dl/17f256f74ba0.pdf.txt", "2026-05 (upload path; LPL-channel circular)", "allowed"),
    "RCF_FAQ": ("https://renaissancecharitable.org/faqs/", "dl/e134c39fa246.html.txt", "live 2026-11-20", "allowed"),
    "BOFA_PG": ("https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf", "ocr/bofa_2025.txt", "Version 8.2025 (text by OCR)", "robots.txt 404 (no rules)"),
    "CCT_APP": ("https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf", "dl/8b21b28c1375.pdf.txt", "2024-02 ('As of February, 2024')", "allowed"),
    "IA_SP": ("https://impactassets.org/ge534a_ia_daf_succession-plan", "dl/3ea467996a60.pdf.txt", "2025-03 (form GE534A March 2025)", "allowed"),
    "FFTC_CGG": ("https://www.fftc.org/sites/default/files/documents/charitable_giving_guide.pdf", "dl/51b3baac1249.pdf.txt", "2026-10 (PDF created 2026-10-21)", "allowed"),
    "JCF_PG": ("https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf", "dl/300cde8608fe.pdf.txt", "2024-08", "allowed"),
    "GKCCF_AGR": ("https://www.growyourgiving.org/open-a-donor-advised-fund/", "dl/a6a8f84366b1.html.txt", "live 2026-11-20 (online fund agreement)", "allowed"),
    "GKCCF_LEG": ("https://www.growyourgiving.org/documents/Your-Philanthropic-Legacy.pdf", "dl/a6e44ea5767f.html.txt", "live 2026-11-20 (URL serves an HTML page)", "allowed"),
    "GH_CONTRIB": ("https://www.greaterhorizons.org/individual-family-giving/contribute-to-your-fund/", "dl/c2afe378ddf7.html.txt", "live 2026-11-20", "allowed"),
    "CJP_PP": ("https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en", "dl/a72ad09d6474.pdf.txt", "2026-04 (PDF created 2026-04-29)", "allowed"),
    "REPO_TRANSFER": ("research/mission-2026-11-14/queue-state-filings-transfer-terms.md", None, "repo file (sources read 2026-11-14)", "carried from repo; host not fetched in this pass"),
}

# (rank, dimension, value, quote fragments joined by ' ... ', doc key, notes)
POLICY = (
    # 1 Fidelity
    (1, "inflow_bequest", "Y", "Donors may designate Fidelity Charitable as a beneficiary of ... estates gifts such as: Trusts, Wills, and Retirement Plans", "FID_PG", "Estate and Legacy Gifts 'may require a case-by-case analysis'"),
    (1, "inflow_retirement_beneficiary", "Y", "estates gifts such as: Trusts, Wills, and Retirement Plans", "FID_PG", ""),
    (1, "inflow_life_insurance", "Y", "items, life insurance, IRAs, trusts, and wills", "FID_PG", "Named in the fee clause for testamentary transfers, not in the contribution list"),
    (1, "inflow_crt_remainder", "NS", "", "FID_PG", "Only generic 'Trusts' named; no explicit charitable remainder trust wording in the guidelines"),
    (1, "estate_gift_handling", "supporting-organization intake; extra fee possible", "will generally handle the initial ... transfer from estates and other testimonial instruments through its ... Fidelity Charitable may assess", "FID_PG", "Guidelines name 'Fidelity Investments Charitable Gift Fund, Inc.' as the 'supporting organization'; that is also Fidelity Charitable's own legal name (EIN 11-0303001), so the reference is ambiguous as published"),
    (1, "default_no_successor", "sponsor_general_fund", "any remaining balance will become part of the unrestricted funds ... of Fidelity Charitable", "FID_PG", "Same outcome if no named Successor responds within 90 days"),
    (1, "successor_nonresponse_rule", "90 days", "If no nominated Successor responds to the notification within 90", "FID_PG", ""),
    (1, "named_charity_option", "Y", "Successor Charitable Organization", "FID_PG", ""),
    (1, "legacy_program_fixed_years", "Endowed Giving Program: not less than 5 years after death; $100,000 minimum", "over a period of time not less than ... five years following the Account Holder", "FID_PG", "Below $100,000 at death Fidelity may make a one-time lump-sum grant instead"),
    (1, "successor_generation_limit", "no stated limit (implied: successor becomes an Account Holder, and any Account Holder may add Successors)", "and shall become an Account Holder ... Any Account Holder may at any time add or remove any", "FID_PG", "No explicit perpetuity or cap language"),
    (1, "successor_options", "individual / charity / Endowed Giving Program, any combination", "Account Holders can elect one successor option or any combination of the three", "FID_FAQ", ""),
    # 2 NPT
    (2, "inflow_bequest", "Y", "Your DAF can be the beneficiary of a bequest", "NPT_GUIDE", ""),
    (2, "inflow_retirement_beneficiary", "Y", "Retirement plan such as an individual retirement", "NPT_GUIDE", "IRA or 401(k)"),
    (2, "inflow_life_insurance", "Y", "Life insurance policy", "NPT_GUIDE", ""),
    (2, "inflow_crt_remainder", "Y", "Charitable remainder trust or charitable lead", "NPT_GUIDE", "Also transfer-on-death (TOD) accounts"),
    (2, "default_no_successor", "sponsor_general_fund (NPT Giving Fund)", "NPT will consider your account abandoned once ... Fund. You may update your Legacy Plan at any time", "NPT_GUIDE", "Table: 'NPT Giving Fund is the default Legacy Plan option. 100% of your DAF account balance will be paid to the NPT Giving Fund'"),
    (2, "named_charity_option", "Y", "CHARITABLE ... BENEFICIARIES", "NPT_GUIDE", "Not via ER/ED, so most non-US charities excluded"),
    (2, "legacy_program_fixed_years", "Endowment Program: annual grants until spent down; $100,000 minimum at activation; lump sum when balance reaches $25,000 (no fixed term)", "annual grants until the ... account is spent down", "NPT_GUIDE", ""),
    (2, "successor_generation_limit", "none (perpetual)", "The process of assigning successor advisors can continue in perpetuity.", "NPT_GUIDE", "Successor sub-accounts under $10,000 subject to fee minimums"),
    # 4 Vanguard
    (4, "inflow_bequest", "Y", "Bequest of cash equivalents or securities", "VC_PG", "Intent to Give form requested"),
    (4, "inflow_retirement_beneficiary", "Y", "Individual retirement account (IRA)", "VC_PG", "Also 401(k)"),
    (4, "inflow_life_insurance", "Y", "Life insurance policy", "VC_PG", ""),
    (4, "inflow_crt_remainder", "Y", "charitable beneficiary of a charitable lead or charitable remainder trust", "VC_DEF", "Web page, not the guidelines PDF"),
    (4, "default_no_successor", "sponsor_general_fund (Philanthropic Impact Fund)", "can no longer serve, the account ... transferred to the Philanthropic Impact Fund", "VC_PG", "'may be' transferred; abandonment path also allows the Sustainable Disaster-Relief Fund"),
    (4, "named_charity_option", "Y", "Recommend Final Grants to Charity", "VC_PG", ""),
    (4, "legacy_program_fixed_years", "Endowed Grant Plan: minimum term 5 years, at least 5% a year", "The minimum term for an EGP is five years.", "VC_PG", ""),
    (4, "successor_generation_limit", "none 'under present guidelines' (perpetual)", "Under present guidelines, this succession process ... can continue in perpetuity as the successor advisors", "VC_PG", "Max two advisors per account; split accounts need $25,000 each"),
    # 6 SVCF
    (6, "inflow_bequest", "Y", "PROPERTY, REAL ESTATE, TESTAMENTARY", "SVCF_AGR", "Testamentary listed as a gift type on the fund agreement"),
    (6, "inflow_retirement_beneficiary", "NS", "", "SVCF_AGR", "Not stated in the fund agreement"),
    (6, "inflow_life_insurance", "NS", "", "SVCF_AGR", ""),
    (6, "inflow_crt_remainder", "NS", "", "SVCF_AGR", ""),
    (6, "default_no_successor", "sponsor_general_fund (Community Endowment Fund)", "balance to support SVCF", "SVCF_AGR", "'SVCF will use the fund's balance to support SVCF's Community Endowment Fund'"),
    (6, "successor_generation_limit", "capped: three successor advisors in aggregate", "Successor advisors may appoint further successors (up to ... a total of three successor advisors in aggregate)", "SVCF_AGR", "Also max three fund advisors at a time"),
    # 7 AEF
    (7, "inflow_bequest", "Y", "You may direct your bequest to the American Endowment Foundation by funding a Donor-Advised Fund in advance ($25,000 minimum contribution)", "AEF_BEQ", ""),
    (7, "inflow_retirement_beneficiary", "Y", "Ask your IRA, 401(k) or 403(b) administrator for a change of beneficiary form.", "AEF_BOOK", ""),
    (7, "inflow_life_insurance", "Y (case by case)", "Life insurance", "AEF_BOOK", "Listed under complex assets: contact AEF"),
    (7, "inflow_crt_remainder", "NS", "", "AEF_BOOK", "AEF CRT page (aefonline.org/?p=9736) returned 404"),
    (7, "default_no_successor", "NF", "", "AEF_BOOK", "No AEF document read states the no-successor default"),
    (7, "successor_generation_limit", "no stated limit (marketing: 'generationally')", "AEF allows successor donor advisors to be ... on generationally.", "AEF_FACT", "Fact sheet, not a policy"),
    # 8 MS GIFT
    (8, "inflow_bequest", "Y", "Donors may contribute to an Account by naming MS GIFT, Inc. as the beneficiary of a bequest of cash", "MS_CIRC", ""),
    (8, "inflow_retirement_beneficiary", "Y", "beneficiary of a qualified retirement plan, individual retirement account (IRA)", "MS_CIRC", ""),
    (8, "inflow_life_insurance", "Y", "insurance policy or a revocable or irrevocable trust", "MS_CIRC", ""),
    (8, "inflow_crt_remainder", "Y", "including a charitable remainder trust or a charitable lead trust", "MS_CIRC", ""),
    (8, "default_no_successor", "sponsor_general_fund (Undesignated Fund, Board discretion)", "the Board may, upon notification of the donor's death or incapacity, transfer assets from the Account to", "MS_CIRC", "Followed by 'the Undesignated Fund'"),
    (8, "named_charity_option", "Y (ultimate charitable beneficiary)", "Grant to Charity at Death", "MS_CIRC", ""),
    (8, "legacy_program_fixed_years", "No term programme; named charities receive grants automatically if successors make no grant for 5 consecutive years", "fail(s) to recommend (upon your death) a grant for five (5) consecutive years", "MS_DCA", "Also a 'NextGen Legacy Account' for lineal descendants ($5,000 minimum)"),
    (8, "successor_generation_limit", "allowed, but sponsor reserves right to cap generations and/or years", "Successors may designate their ... own Successors ... reserves the right to limit overall succession ... specific number of generations", "MS_CIRC", "No cap figure published"),
    # 9 RCF
    (9, "inflow_bequest", "Y", "charitable bequest, charitable remainder", "RCF_LPL", "LPL-channel circular; other RCF programmes may differ"),
    (9, "inflow_retirement_beneficiary", "Y", "trust, charitable lead trust, qualified retirement plan or private", "RCF_LPL", ""),
    (9, "inflow_life_insurance", "NS", "", "RCF_LPL", ""),
    (9, "inflow_crt_remainder", "Y", "charitable bequest, charitable remainder", "RCF_LPL", ""),
    (9, "default_no_successor", "sponsor_discretion (written instructions or internal policies)", "If no successor is named, Renaissance Charitable will distribute the remaining assets according to your written instructions or its internal policies", "RCF_FAQ", "Circular asks donors to name a charity or area of interest as fallback"),
    (9, "named_charity_option", "Y (lump sum or a percentage annually; not combined with individual successors)", "individual successor(s) or charitable beneficiary(ies), but not", "RCF_LPL", ""),
    (9, "successor_generation_limit", "no stated limit (successors may name future successors)", "make contributions, recommend grants and name advisors ... and future successors", "RCF_LPL", ""),
    # 11 BofA
    (11, "inflow_bequest", "Y", "be named the beneficiary of a bequest of cash or securities, including mutual fund shares", "BOFA_PG", ""),
    (11, "inflow_retirement_beneficiary", "Y", "charitable lead trust, Individual Retirement Account", "BOFA_PG", ""),
    (11, "inflow_life_insurance", "Y", "(IRA) or life insurance policy", "BOFA_PG", ""),
    (11, "inflow_crt_remainder", "Y", "may also be named the beneficiary of a charitable remainder trust", "BOFA_PG", ""),
    (11, "default_no_successor", "sponsor_general_fund (General Fund = CGF endowment fund)", "the Trustee will distribute the remaining account balance to the General", "BOFA_PG", ""),
    (11, "named_charity_option", "Y", "the Donor may recommend that one or more qualified charitable", "BOFA_PG", ""),
    (11, "successor_generation_limit", "no stated limit (successor may name a subsequent Successor)", "including the ability to recommend grants and name a subsequent Successor", "BOFA_PG", ""),
    (11, "succession_by_will", "N", "The Charitable Gift Fund cannot honor succession or beneficiary plans outlined in a will, trust, or other estate", "BOFA_PG", ""),
    # 12 CCT
    (12, "inflow_bequest", "Y", "Will or Revocable Trust", "CCT_APP", "Checkbox list of estate-plan commitments on the DAF application"),
    (12, "inflow_retirement_beneficiary", "Y", "IRA or other retirement plan assets", "CCT_APP", ""),
    (12, "inflow_life_insurance", "Y", "Life insurance", "CCT_APP", ""),
    (12, "inflow_crt_remainder", "Y", "Charitable remainder trust", "CCT_APP", ""),
    (12, "default_no_successor", "sponsor_general_fund (converted to unrestricted fund, or general endowment if small)", "converted to an unrestricted fund, or if the balance of the fund is below the", "CCT_APP", "After all advisors, unnamed balance goes to 'the permanent unrestricted endowment of The Chicago Community Foundation'"),
    (12, "named_charity_option", "Y (post-death charitable beneficiaries)", "UPDATE POST-DEATH CHARITABLE BENEFICIARIES", "CCT_APP", ""),
    (12, "successor_generation_limit", "capped: two generations of successor advisors", "maximum of two generations of successor advisors can be named", "CCT_APP", ""),
    # 13 ImpactAssets
    (13, "default_no_successor", "sponsor_general_fund (ImpactAssets permanent fund)", "If no option is selected, the succession ... plan will default to Option (1)", "IA_SP", "Option 1 = 'name ImpactAssets as the beneficiary'; supports 'ImpactAssets' permanent fund'"),
    (13, "named_charity_option", "Y", "recommending charitable organizations to receive the remaining assets", "IA_SP", ""),
    (13, "successor_generation_limit", "NS (program circular returned 403)", "", "IA_SP", ""),
    # 14 FFTC
    (14, "inflow_bequest", "Y", "A charitable bequest of cash, securities, real property and other assets can be made to", "FFTC_CGG", ""),
    (14, "inflow_retirement_beneficiary", "Y", "Assets held in qualified retirement accounts, individual retirement accounts (IRAs) or other banking and", "FFTC_CGG", ""),
    (14, "inflow_life_insurance", "Y", "Donor(s) may make a gift of life insurance to FFTC", "FFTC_CGG", "Premium-paying policies only if valued at $250,000 or more"),
    (14, "inflow_crt_remainder", "Y (to an endowed Gift Fund, FFTC as trustee)", "at the end of the term, the assets of the trust are distributed to FFTC generally or to an endowed Gift Fund", "FFTC_CGG", "CRT minimum funding $250,000"),
    (14, "default_no_successor", "sponsor_general_fund (FFTC policies for undirected Gift Funds)", "distributed pursuant to FFTC", "FFTC_CGG", ""),
    (14, "named_charity_option", "Y", "Support a Public Charity other than FFTC", "FFTC_CGG", ""),
    (14, "legacy_program_fixed_years", "Option to endow the fund when successors take over (perpetual, spendable amount only)", "FFTC to permanently endow the Fund at such time when successor advisors assume advisory", "FFTC_CGG", ""),
    (14, "successor_generation_limit", "one generation by default; further generations only if opening donor expressly authorises", "In the absence of written authorization by the opening donor(s), surviving advisors and successor advisors ... will not have the ability to appoint additional or successor advisors", "FFTC_CGG", ""),
    # 15 JCF
    (15, "inflow_bequest", "Y", "as the charitable beneficiary of a will, an IRA,", "JCF_PG", ""),
    (15, "inflow_retirement_beneficiary", "Y", "a 401(k) plan, a charitable remainder trust, or", "JCF_PG", "No lifetime IRA distributions"),
    (15, "inflow_life_insurance", "Y", "a life insurance policy", "JCF_PG", ""),
    (15, "inflow_crt_remainder", "Y", "a 401(k) plan, a charitable remainder trust, or", "JCF_PG", ""),
    (15, "default_no_successor", "sponsor_general_fund (JCF Special Gifts Fund)", "any remaining assets in the fund to the JCF ... Special Gifts Fund upon receiving notification of", "JCF_PG", ""),
    (15, "successor_nonresponse_rule", "1 year", "a Successor Transition form within one year of", "JCF_PG", ""),
    (15, "named_charity_option", "Y", "Successor charities may be named in lieu of", "JCF_PG", ""),
    (15, "successor_generation_limit", "none (number of successors may be limited)", "There is no limit to ... succession on JCF funds as long as there are still", "JCF_PG", ""),
    (15, "succession_by_will", "N", "they may not establish ... a succession plan for an existing donor advised", "JCF_PG", ""),
    # 16 GKCCF
    (16, "inflow_bequest", "Y", "To name a donor-advised fund at the Community Foundation as a beneficiary of a will, trust, life insurance policy or retirement plan account", "GKCCF_AGR", ""),
    (16, "inflow_retirement_beneficiary", "Y", "life insurance policy or retirement plan account", "GKCCF_AGR", ""),
    (16, "inflow_life_insurance", "Y", "life insurance policy or retirement plan account", "GKCCF_AGR", ""),
    (16, "inflow_crt_remainder", "NS", "", "GKCCF_AGR", ""),
    (16, "estate_gift_handling", "3% one-time fee on pass-through bequests", "the Community Foundation will assess a one-time 3% fee on such bequest", "GKCCF_AGR", "Agreement also offers 'The contribution will be made upon my death'"),
    (16, "default_no_successor", "sponsor_discretion (charitable purposes)", "the Community Foundation shall use the principal and income from the Fund for charitable purposes", "GKCCF_AGR", ""),
    (16, "successor_generation_limit", "NS", "Name children, grandchildren or other trusted individuals who will recommend grants", "GKCCF_LEG", "No cap or perpetuity statement in pages read"),
    # 17 Greater Horizons
    (17, "inflow_bequest", "Y", "To name a Greater Horizons fund as a beneficiary of a will, trust, life insurance policy or retirement plan account", "GH_CONTRIB", ""),
    (17, "inflow_retirement_beneficiary", "Y", "life insurance policy or retirement plan account", "GH_CONTRIB", ""),
    (17, "inflow_life_insurance", "Y", "life insurance policy or retirement plan account", "GH_CONTRIB", ""),
    (17, "default_no_successor", "NF", "", "GH_CONTRIB", "No public succession terms found"),
    # 19 CJP
    (19, "default_no_successor", "sponsor_general_fund (CJP Unrestricted Endowment Fund)", "Fund shall be added to CJP", "CJP_PP", "'...Unrestricted Endowment Fund, unless alternative recommendations exist'"),
    (19, "named_charity_option", "Y", "Donors can designate charitable beneficiaries", "CJP_PP", ""),
    (19, "successor_generation_limit", "one generation (children and spouses) by default; further successors at CJP discretion", "may designate a Donor ... child or children when of age ... Amendments adding further successors will be considered by CJP.", "CJP_PP", ""),
    # 3 DAFgiving360 / 10 NCF carried from repo
    (3, "default_no_successor", "granting_history (carried from repo)", "", "REPO_TRANSFER", "Repo quotes the Dec-2024 Program Policies: dormant account with no succession plan 'will be closed and assets will be transferred to eligible charities based on the account granting history'. dafgiving360.org on the task blocked list; not re-read"),
    (10, "default_no_successor", "granting_history (carried from repo)", "", "REPO_TRANSFER", "Repo row: 'Succession plan; otherwise distributed by grantmaking history'. ncfgiving.com terms bar automated extraction; secure.ncfgiving.com robots disallow all"),
    (10, "successor_generation_limit", "succession funds restricted to NCF (carried from repo)", "", "REPO_TRANSFER", "Repo quote: succession funds 'may not make grants to or transfer assets to another donor-advised fund sponsor'"),
    # blocked / not found
    (5, "default_no_successor", "BLOCKED", "", None, "gspf.goldman.com robots.txt disallows the circular path; repo copy is a 2008 circular (pre-2021, not used)"),
    (18, "default_no_successor", "NF", "", None, "dechomai.org policies page read; no succession terms"),
    (20, "default_no_successor", "BLOCKED", "", None, "raymondjames.com robots.txt returned 403; raymondjamescharitable.org unreachable"),
)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def read_text(web_dir: str, rel: str | None) -> str | None:
    if not rel:
        return None
    path = os.path.join(web_dir, rel)
    return open(path, encoding="utf-8", errors="replace").read() if os.path.exists(path) else None


def quote_ok(text: str | None, quote: str) -> str:
    if not quote:
        return "n/a"
    if text is None:
        return "doc_missing"
    hay = norm(text)
    return "yes" if all(norm(f) in hay for f in quote.split(" ... ") if f.strip()) else "no"


def policy_rows(web_dir: str) -> tuple[dict, ...]:
    by_rank = {r: (n, e) for r, n, e in SPONSORS}
    texts = {k: read_text(web_dir, v[1]) for k, v in DOCS.items()}

    def one(i_p):
        i, (rank, dim, value, quote, doc, notes) = i_p
        name, ein = by_rank[rank]
        url, _, ddate, robots = DOCS[doc] if doc else ("", None, "", "")
        label = ("carried_from_repo" if doc == "REPO_TRANSFER" else
                 "not_found" if value == "NF" else "blocked" if value == "BLOCKED" else "primary_doc")
        return dict(record_id=f"B4903-P{i + 1:03d}", rank_fy2024=rank, sponsor=name, ein=ein,
                    record_type="policy", dimension=dim, value=value, quote=quote,
                    quote_verified=quote_ok(texts.get(doc), quote) if doc != "REPO_TRANSFER" else "repo",
                    source_url=url, source_date=ddate, robots=robots, evidence_label=label,
                    retrieved=RETRIEVED, notes=notes)
    return tuple(map(one, enumerate(POLICY)))


# ---------------- filings ----------------

def index_rows(irs_dirs: Sequence[str], eins: frozenset[str]) -> tuple[dict, ...]:
    def rows_of(path):
        with open(path, newline="", encoding="utf-8", errors="replace") as fh:
            return tuple(r for r in csv.DictReader(fh) if r.get("EIN") in eins and r.get("RETURN_TYPE") == "990")
    files = sorted({os.path.realpath(os.path.join(d, f)) for d in irs_dirs if os.path.isdir(d)
                    for f in os.listdir(d) if re.fullmatch(r"index_20(2[1-6])\.csv", f)})
    return tuple(r for p in files for r in rows_of(p))


def latest(rows: Iterable[Mapping]) -> dict:
    def better(acc, r):
        key = lambda x: (x["TAX_PERIOD"], x["OBJECT_ID"])
        cur = acc.get(r["EIN"])
        return {**acc, r["EIN"]: r} if cur is None or key(r) > key(cur) else acc
    return reduce(better, rows, {})


def locate_xml(oid: str, caches: Sequence[str], xml_dir: str, fetch: bool) -> tuple[str | None, str]:
    name = f"{oid}_public.xml"
    found = next((os.path.join(c, name) for c in (xml_dir, *caches) if os.path.exists(os.path.join(c, name))), None)
    if found or not fetch:
        return found, "cache" if found else "missing"
    try:
        with urllib.request.urlopen(urllib.request.Request(XML_URL.format(oid=oid), headers=UA), timeout=60) as r:
            body = r.read()
        dest = os.path.join(xml_dir, name)
        with open(dest, "wb") as fh:
            fh.write(body)
        return dest, "fetched"
    except Exception as exc:  # noqa: BLE001
        return None, f"fetch_error:{exc}"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def num(s: str | None) -> float | None:
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


# Narrative elements only (Schedule O/M/D explanations, mission and programme text);
# names, addresses and grant-purpose lines are excluded because they match words like ESTATE.
NARRATIVE_TAGS = frozenset({"ExplanationTxt", "Desc", "ActivityOrMissionDesc", "MissionDesc",
                            "PrimaryActivitiesTxt", "DescriptionProgramSrvcAccomTxt", "OtherRevenueDescriptionTxt"})
KEYWORDS = re.compile(r"\b(BEQUESTS?|ESTATES?|DECEDENTS?|IRAS?|RETIREMENT|LIFE INSURANCE|INSURANCE|REMAINDER|TESTAMENTARY|LEGACY|SPLIT[- ]INTEREST|LEAD TRUSTS?)\b", re.I)


def extract(path: str) -> dict:
    root = ET.parse(path).getroot()
    f990 = next((e for e in root.iter() if local(e.tag) == "IRS990"), None)
    child = lambda el, n: next((c.text for c in el if local(c.tag) == n), None) if el is not None else None
    sched = lambda n: next((e for e in root.iter() if local(e.tag) == n), None)
    sm, sd = sched("IRS990ScheduleM"), sched("IRS990ScheduleD")
    lines = tuple(
        dict(line=local(g.tag), desc=child(g, "Desc") or "", cnt=num(child(g, "ContributionCnt")),
             amt=num(child(g, "NoncashContributionsRptF990Amt")) or 0.0)
        for g in (sm if sm is not None else ()) if len(list(g)) and any(local(c.tag) == "NoncashContributionsRptF990Amt" for c in g))
    texts = tuple((local(e.tag), (e.text or "").strip()) for e in root.iter()
                  if local(e.tag) in NARRATIVE_TAGS and (e.text or "").strip() and KEYWORDS.search(e.text))
    return dict(
        total_contrib=num(child(f990, "TotalContributionsAmt")),
        noncash_contrib=num(child(f990, "NoncashContributionsAmt")),
        daf_contrib=num(child(sd, "DonorAdvisedFundsContriAmt")),
        daf_count=num(child(sd, "DonorAdvisedFundsHeldCnt")),
        f8283=num(child(sm, "Form8283ReceivedCnt")),
        gift_policy=child(sm, "ReviewProcessUnusualNCGiftsInd"),
        sched_m_lines=lines,
        keyword_texts=texts,
    )


def filing_rows(irs_dirs, caches, xml_dir, fetch) -> tuple[tuple[dict, ...], tuple[dict, ...]]:
    eins = frozenset(e for _, _, e in SPONSORS)
    pick = latest(index_rows(irs_dirs, eins))
    def per_sponsor(s):
        rank, name, ein = s
        f = pick.get(ein)
        if not f:
            return (), dict(ein=ein, status="no_filing")
        path, how = locate_xml(f["OBJECT_ID"], caches, xml_dir, fetch)
        if not path:
            return (), dict(ein=ein, oid=f["OBJECT_ID"], status=how)
        ex = extract(path)
        url = XML_URL.format(oid=f["OBJECT_ID"])
        base = dict(rank_fy2024=rank, sponsor=name, ein=ein, record_type="filing", quote="", quote_verified="n/a",
                    source_url=url, source_date=f"tax period {f['TAX_PERIOD']}", robots="robots.txt 404 (no rules)",
                    evidence_label="computed_from_990_xml", retrieved=RETRIEVED)
        def row(dim, value, notes=""):
            return {**base, "dimension": dim, "value": "" if value is None else (f"{value:.0f}" if isinstance(value, float) else str(value)), "notes": notes}
        sm_total = sum(l["amt"] for l in ex["sched_m_lines"])
        trust = sum(l["amt"] for l in ex["sched_m_lines"] if l["line"] == "SecurPrtnrshpTrustIntrstsGrp")
        others = tuple(l for l in ex["sched_m_lines"] if l["line"] == "OtherNonCashContriTableGrp")
        estate_like = tuple(l for l in others if KEYWORDS.search(l["desc"]))
        share = (ex["noncash_contrib"] / ex["total_contrib"]) if ex["noncash_contrib"] is not None and ex["total_contrib"] else None
        kw = tuple(f"{t}: {x[:160]}" for t, x in ex["keyword_texts"])
        rows = (
            row("f990_total_contributions_usd", ex["total_contrib"], "Part VIII line 1h"),
            row("f990_noncash_contributions_usd", ex["noncash_contrib"], "Part VIII line 1g"),
            row("f990_noncash_share_of_contributions", None if share is None else f"{share:.4f}", "computed: line 1g / line 1h"),
            row("schd_daf_contributions_usd", ex["daf_contrib"], "Schedule D Part I line 2 col (a)"),
            row("schm_total_reported_usd", sm_total, "sum of Schedule M column (c) lines"),
            row("schm_trust_interests_usd", trust, "Schedule M line 11 'Securities - partnership, LLC, or trust interests' (trust interests not separable from partnerships/LLCs)"),
            row("schm_other_lines", "; ".join(f"{l['desc']} ({l['cnt'] or 0:.0f}; ${l['amt']:,.0f})" for l in others) or "none", "Schedule M lines 25-28 descriptions"),
            row("schm_other_lines_estate_keyword_usd", sum(l["amt"] for l in estate_like), "Other lines whose description matches an estate keyword"),
            row("schm_form8283_count", ex["f8283"], "Schedule M line 29"),
            row("estate_keyword_text_hits", len(kw), " | ".join(kw)[:1500]),
        )
        return rows, dict(ein=ein, oid=f["OBJECT_ID"], tax_period=f["TAX_PERIOD"], status=how)
    results = tuple(map(per_sponsor, SPONSORS))
    rows = tuple(r for rs, _ in results for r in rs)
    numbered = tuple({**r, "record_id": f"B4903-F{i + 1:03d}"} for i, r in enumerate(rows))
    return numbered, tuple(m for _, m in results)


FIELDS = ("record_id", "rank_fy2024", "sponsor", "ein", "record_type", "dimension", "value", "quote",
          "quote_verified", "source_url", "source_date", "robots", "evidence_label", "retrieved", "notes")


def summarise(policy: Sequence[Mapping], filings: Sequence[Mapping]) -> dict:
    pick = lambda dim: {r["rank_fy2024"]: r["value"] for r in policy if r["dimension"] == dim}
    defaults = pick("default_no_successor")
    gens = pick("successor_generation_limit")
    inflow = {d: sum(1 for v in pick(d).values() if v.startswith("Y")) for d in
              ("inflow_bequest", "inflow_retirement_beneficiary", "inflow_life_insurance", "inflow_crt_remainder")}
    cat = lambda v: ("sponsor_general_fund" if v.startswith("sponsor_general_fund") else
                     "granting_history" if v.startswith("granting_history") else
                     "sponsor_discretion" if v.startswith("sponsor_discretion") else v)
    default_counts = reduce(lambda a, v: {**a, cat(v): a.get(cat(v), 0) + 1}, defaults.values(), {})
    fixed = {r: v for r, v in pick("legacy_program_fixed_years").items()}
    fval = lambda dim: {r["rank_fy2024"]: r["value"] for r in filings if r["dimension"] == dim}
    tot, nc, trust = fval("f990_total_contributions_usd"), fval("f990_noncash_contributions_usd"), fval("schm_trust_interests_usd")
    fl = lambda d: sum(float(v) for v in d.values() if v not in ("", None))
    return dict(
        sponsors=len(SPONSORS),
        policy_records=len(policy),
        quotes_verified=sum(1 for r in policy if r["quote_verified"] == "yes"),
        quotes_failed=[r["record_id"] for r in policy if r["quote_verified"] in ("no", "doc_missing")],
        inflow_yes_counts=inflow,
        default_counts=default_counts,
        generation_limits=gens,
        legacy_programs=fixed,
        filings_sponsors=len(tot),
        sum_total_contrib=fl(tot), sum_noncash=fl(nc), sum_trust_interests=fl(trust),
        estate_keyword_hits={r["rank_fy2024"]: r["value"] for r in filings if r["dimension"] == "estate_keyword_text_hits"},
        other_line_estate_usd={r["rank_fy2024"]: r["value"] for r in filings if r["dimension"] == "schm_other_lines_estate_keyword_usd"},
    )


def main(argv: Sequence[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--web-dir", required=True)
    ap.add_argument("--irs-dir", action="append", default=[])
    ap.add_argument("--xml-cache", action="append", default=[])
    ap.add_argument("--xml-dir", required=True)
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args(argv)
    policy = policy_rows(a.web_dir)
    filings, meta = filing_rows(a.irs_dir, a.xml_cache, a.xml_dir, a.fetch)
    out = os.path.join(a.root, OUT)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(policy + filings)
    print(json.dumps(dict(summary=summarise(policy, filings), filings=meta, out=out), indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
