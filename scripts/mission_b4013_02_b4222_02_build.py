"""P-B40N13-02 / P-B42N22-02: build the grant-remittance and portal-feature CSVs.

Usage: python3 -I scripts/mission_b4013_02_b4222_02_build.py . [OUTDIR]
  root   repo root ('.')
  OUTDIR defaults to <root>/data/mission-2026-11-14

Rows are first-party evidence read on 2026-11-19 (quotes verbatim, checked against
the fetched pages by a separate verifier). FY2024 assets and ranks are joined from
repo CSVs so that every number is computed here, not typed. Prints the summary
tables used in the research note. Stdlib only, no mutable global state.
"""
import csv
import os
import sys
from collections import Counter
from functools import reduce

RETRIEVED = "2026-11-19"
LEAGUE = "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv"
CF_EXPORT = "data/mission-2026-11-14/donor-export-evidence-cf-2026.csv"

FC_FAQ = "https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html"
FC_FORM = "https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf"
FC_EFT = "https://www.fidelitycharitable.org/nonprofits/eft.html"
FC_STRIPE = "https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html"
NPT_GUIDE = "https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf"
NPT_ART = "https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/"
VC_NP = "https://www.vanguardcharitable.org/nonprofit-organizations"
PP_NEWS = "https://newsroom.paypal-corp.com/2023-12-PayPal-Grant-Payments"
MS_GIFT = "https://www.morganstanley.com/gift"
REN_PAY = "https://www.reninc.com/payments/"
REN_GRANTS = "https://intercom.help/rengiving/en/articles/6232128-charity-grants"
REN_OVR = "https://intercom.help/rengiving/en/articles/6229556-ren-for-charities-overview"
AEF_CH = "https://www.aefonline.org/charities/"
RCF_GUIDE = "https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf"
NCF_SUP = "https://ncfgiving.com/support"
NCF_GUIDE = "https://www.ncfgiving.com/guide-to-giving-at-NCF"
CH_ACCT = "https://help.givechariot.com/llms-full.txt"
CH_GIFTS = "https://docs.givechariot.com/v2026-04-01/guides/dafpay/integrate-dafpay/managing-gifts.md"
CH_WEB = "https://givechariot.com/resources/webinars/-powering-modern-daf-grants"
SVCF_R = "data/mission-2026-11-14/community-foundation-rails-portals-2026-v2.csv (SVCF row)"
DAF360_R = "data/mission-2026-11-14/sponsor-grant-payment-policies.csv (DAFgiving360 row)"

# --- Part A: one row per sponsor x electronic route (or context rail) ---------------------------
REMIT_COLS = ["row_id", "fy2024_rank", "sponsor", "ein", "fy2024_daf_assets_usd", "electronic_route",
              "route_operator", "ach_sec_code", "grant_id_in_addenda", "fund_name_in_addenda",
              "bank_statement_descriptor", "batching", "out_of_band_channel", "out_of_band_fields",
              "chariot_list_status", "key_quote", "source_url", "source_date", "access_status",
              "evidence_label", "notes", "retrieved"]

REMIT = [
    dict(row_id="RA-01", ein="110303001", sponsor="Fidelity Charitable", electronic_route="ACH (EFT)",
         route_operator="Fidelity Charitable", ach_sec_code="not stated", grant_id_in_addenda="not stated",
         fund_name_in_addenda="not stated",
         bank_statement_descriptor="\"Fidelity Charitable\" as the source (FAQ)",
         batching="yes: one EFT can carry several grants",
         out_of_band_channel="email: encrypted Grant Details Report, daily, to up to 5 contacts",
         out_of_band_fields="grant amount; acknowledgement information; donor-recommended purpose (form text)",
         chariot_list_status="Chariot 'Sources Managed By Chariot' (paid plan)",
         key_quote="Each EFT is comprised of one or more donor-recommended grants.",
         source_url=FC_FORM, source_date="PDF created 2025-12-02, modified 2025-12-18",
         access_status="read", evidence_label="F",
         notes="Daily GDR and 'Fidelity Charitable' descriptor: " + FC_FAQ + ". EFT page: ACH grant details 'Sent with grant notice', notices 'Emailed daily' (" + FC_EFT + "). Primary GDR inbox must be one person's; 'A group shared inbox will not be accepted'. The FAQ links a sample GDR whose PDF dates from 2020 (pre-2021, not used)."),
    dict(row_id="RA-02", ein="110303001", sponsor="Fidelity Charitable", electronic_route="Stripe payout (EFT)",
         route_operator="Stripe (Express account)", ach_sec_code="not stated (Stripe payout)",
         grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="\"Fidelity grant\"",
         batching="yes: Stripe 'Payouts'",
         out_of_band_channel="Stripe dashboard and transaction export; weekly Monday notice (FAQ) - but a second Fidelity page says no email is sent",
         out_of_band_fields="donor contact information and special designations in the full export, 'not available in the dashboard'",
         chariot_list_status="Chariot managed source (Fidelity Charitable)",
         key_quote="Bank statements from grants made through Stripe will show up as “Fidelity grant”.",
         source_url=FC_FAQ, source_date="live (page (c)1998-2026)", access_status="read", evidence_label="F",
         notes="Conflict: FAQ 'grant notices are emailed each Monday'; " + FC_STRIPE + " says 'Fidelity Charitable does not currently send an email notifying nonprofits of grants distributed through Stripe'."),
    dict(row_id="RA-03", ein="237825575", sponsor="National Philanthropic Trust (NPT)",
         electronic_route="PayPal Grant Payments (EFT); wire for grants of $250,000+ and all international grants",
         route_operator="PayPal; NPT (wire)", ach_sec_code="n/a: NPT states it issues no ACH",
         grant_id_in_addenda="n/a (no ACH)", fund_name_in_addenda="n/a (no ACH)",
         bank_statement_descriptor="not stated (PayPal transfer to the charity's bank is a separate step)",
         batching="not stated",
         out_of_band_channel="PayPal Grant Payments dashboard notification; for wires, grant letter emailed separately",
         out_of_band_fields="'all relevant donor and grant details' (dashboard); letter: purpose and DAF account unless anonymous",
         chariot_list_status="Chariot managed source (PayPal Grant Payments)",
         key_quote="At this time, NPT does not issue payments via ACH transfer.",
         source_url=NPT_GUIDE, source_date="PDF created 2026-10-15 (URL path 2024/09)", access_status="read",
         evidence_label="F",
         notes="Same guide: grantee 'will receive a notification containing all relevant donor and grant details through a dedicated PayPal dashboard'; wire: 'the grant letter will be separately emailed to them'. NPT article (modified 2026-05-19): staff 'can export details for their fundraising records' (" + NPT_ART + ")."),
    dict(row_id="RA-04", ein="311640316", sponsor="DAFgiving360 (Schwab)", electronic_route="not documented",
         route_operator="", ach_sec_code="not determinable (site blocked)", grant_id_in_addenda="not determinable",
         fund_name_in_addenda="not determinable", bank_statement_descriptor="not determinable", batching="not determinable",
         out_of_band_channel="not determinable", out_of_band_fields="",
         chariot_list_status="not on Chariot's managed-source or disbursement-partner lists",
         key_quote="", source_url="https://www.dafgiving360.org/", source_date="", access_status="blocked: robots.txt 403 (www.dafgiving360.org, www.schwabcharitable.org)",
         evidence_label="B", notes="Repo: 2024 Program Policies document mailed checks only (" + DAF360_R + ")."),
    dict(row_id="RA-05", ein="232888152", sponsor="Vanguard Charitable", electronic_route="PayPal Grant Payments (EFT)",
         route_operator="PayPal", ach_sec_code="n/a: no sponsor ACH documented", grant_id_in_addenda="n/a",
         fund_name_in_addenda="n/a", bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="PayPal Grant Payments dashboard",
         out_of_band_fields="'all the information a donor has elected to share'",
         chariot_list_status="Chariot managed source (PayPal Grant Payments)",
         key_quote="Vanguard Charitable is now issuing Grant Payments with PayPal.",
         source_url=VC_NP, source_date="live", access_status="read", evidence_label="F",
         notes="Same page: 'The grant details contain all the information a donor has elected to share.' PayPal's own 2023 research note says Grant Payments consolidates payment and donor data 'rather than separating the payment from the donor information as happens with an ACH payment' (" + PP_NEWS + ")."),
    dict(row_id="RA-06", ein="311774905", sponsor="Goldman Sachs Philanthropy Fund (GS DAPF)", electronic_route="not documented",
         route_operator="Ren/Stellar iPhi (repo)", ach_sec_code="not determinable (site blocked)",
         grant_id_in_addenda="not determinable", fund_name_in_addenda="not determinable",
         bank_statement_descriptor="not determinable", batching="not determinable", out_of_band_channel="not determinable",
         out_of_band_fields="", chariot_list_status="not listed by name",
         key_quote="", source_url="https://gspf.goldman.com/", source_date="", access_status="blocked: robots.txt Disallow",
         evidence_label="B", notes="No other public nonprofit-facing page found."),
    dict(row_id="RA-07", ein="205205488", sponsor="Silicon Valley Community Foundation", electronic_route="check by default; ACH/wire reserved",
         route_operator="SVCF", ach_sec_code="not stated", grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="not stated", batching="not stated", out_of_band_channel="not stated", out_of_band_fields="",
         chariot_list_status="not listed",
         key_quote="", source_url=SVCF_R, source_date="2025 (repo)", access_status="repo row; svcf.org/nonprofits and /grants read this pass, no payment text",
         evidence_label="R", notes="Repo quotes: checks 'bearing the name and logo of SVCF'; agreement reserves '(e.g., check, wire, ACH, etc.)'."),
    dict(row_id="RA-08", ein="527082731", sponsor="Morgan Stanley GIFT", electronic_route="ACH via Ren (Ren for Charities)",
         route_operator="Ren", ach_sec_code="not stated", grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="grant letter; Ren for Charities portal grants report with CSV export",
         out_of_band_fields="letter: date, description, purpose, account or donor name; portal: Grant ID, amount, acknowledgement, ACH ID",
         chariot_list_status="Chariot managed source (Ren (Pinkaloo))",
         key_quote="The charity will receive a letter from the board of MS GIFT with the date, description, and purpose of the grant.",
         source_url=MS_GIFT, source_date="live", access_status="read", evidence_label="F",
         notes="Ren administers MS GIFT (repo; FAQ email msgift@reninc.com). Ren: 'Charities sign up for ACH once and are digitally enabled for every DAF program we support' (" + REN_PAY + ", modified 2026-11-04)."),
    dict(row_id="RA-09", ein="341747398", sponsor="American Endowment Foundation (AEF)", electronic_route="ACH via Ren charity portal (launched 2026)",
         route_operator="Ren", ach_sec_code="not stated", grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="Ren charity portal: current and historical grant letters",
         out_of_band_fields="grant letters (contents not listed on page)",
         chariot_list_status="Chariot managed source (Ren (Pinkaloo))",
         key_quote="Until your organization’s ACH information has been submitted and verified in the new portal, grant payments will arrive by check.",
         source_url=AEF_CH, source_date="live", access_status="read", evidence_label="F",
         notes="Same page: 'Powered by Ren, charities can claim their organization, provide ACH information, and prepare to manage upcoming Grant Letters.'"),
    dict(row_id="RA-10", ein="352129262", sponsor="Renaissance Charitable Foundation (RCF)", electronic_route="ACH via Ren (Ren for Charities)",
         route_operator="Ren", ach_sec_code="not stated", grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="Ren for Charities portal (grants report, CSV export, ACH ID); no grant letter for electronic grants per 2026 donor guide",
         out_of_band_fields="Grant ID, grant date, foundation, amount, acknowledgement; ACH ID once 'DELIVERED'",
         chariot_list_status="Chariot managed source (Ren (Pinkaloo))",
         key_quote="if the grant is sent to the organization electronically, no grant letter will be generated.",
         source_url=RCF_GUIDE, source_date="PDF 2026-10-06", access_status="read (cached in P-B4428-02 pass, same day)",
         evidence_label="F",
         notes="Conflict: RCF Program Circular (2026) says 'check or ACH accompanied by a grant letter'. Charity side: " + REN_GRANTS + " (modified 2026-05-04): report helps 'Match payments (Check/ACH) to specific grants'."),
    dict(row_id="RA-11", ein="581493949", sponsor="National Christian Foundation (NCF)", electronic_route="ACH or electronic transfer when available; wire on request",
         route_operator="NCF", ach_sec_code="not stated", grant_id_in_addenda="not stated", fund_name_in_addenda="not stated",
         bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="grant letter; egrants@ncfgiving.com for questions",
         out_of_band_fields="Giving Fund name and any grant purpose (letter)",
         chariot_list_status="not listed",
         key_quote="We often distribute grants via ACH or electronic transfer when available.",
         source_url=NCF_SUP, source_date="live", access_status="read", evidence_label="F",
         notes="Donor guide: grants 'include a letter identifying your Giving Fund and any grant purpose you’ve provided' (" + NCF_GUIDE + "). No public nonprofit EFT enrolment form found."),
    dict(row_id="RA-12", ein="", sponsor="Ren for Charities (rail serving RCF, MS GIFT, AEF and other Ren programs)",
         electronic_route="ACH", route_operator="Ren", ach_sec_code="not stated", grant_id_in_addenda="not stated",
         fund_name_in_addenda="not stated", bank_statement_descriptor="not stated", batching="not stated",
         out_of_band_channel="portal grants report; CSV export; grant-export email",
         out_of_band_fields="Grant ID, amount, acknowledgement (searchable); ACH ID, status, expected delivery date",
         chariot_list_status="Chariot managed source (Ren (Pinkaloo))",
         key_quote="You can also export grant details in a CSV by selecting the button in the upper right hand corner.",
         source_url=REN_GRANTS, source_date="modified 2026-05-04", access_status="read", evidence_label="F",
         notes="Overview (" + REN_OVR + ", modified 2026-07-08): enrol in ACH 'from 25+ donor-advised fund programs at once'. ACH ID appears only after status 'DELIVERED'."),
    dict(row_id="RA-13", ein="", sponsor="Chariot (receiving side, all sources)", electronic_route="ACH into a Chariot Deposit Account",
         route_operator="Chariot / Column N.A.", ach_sec_code="not stated", grant_id_in_addenda="not relied on",
         fund_name_in_addenda="not relied on", bank_statement_descriptor="source identified by a per-source account number, not by descriptor",
         batching="yes: 'One deposit → many donations'",
         out_of_band_channel="Chariot dashboard; donation export; for custom sources the nonprofit uploads files",
         out_of_band_fields="Chariot donation fields incl. External ID, purpose, note, fund name",
         chariot_list_status="managed sources: Fidelity Charitable, PayPal Grant Payments, Ren (Pinkaloo), Benevity, YourCause, CyberGrants, Pledger Charitable, The Donors Fund, OJC Fund, Frontstream, BrightFunds",
         key_quote="Custom Payment Sources only automate the movement of funds.",
         source_url=CH_ACCT, source_date="live (GitBook, undated)", access_status="read", evidence_label="F",
         notes="Account Numbers page: a per-source account number means teams need not 'rely on inconsistent descriptions to figure out where funds came from'. Webinar: ACH 'typically lands with a bank reference ID that has nothing to do with the grant ID' (" + CH_WEB + ")."),
    dict(row_id="RA-14", ein="", sponsor="Chariot DAFpay (any provider paying outside Chariot)", electronic_route="ACH or check",
         route_operator="DAF provider", ach_sec_code="not stated", grant_id_in_addenda="sometimes: Tracking ID in memo, provider-dependent",
         fund_name_in_addenda="fallback match field, location not stated", bank_statement_descriptor="not stated",
         batching="'Some providers batch several gifts into one payment'",
         out_of_band_channel="Chariot dashboard (DAFpay Tracking ID, External Grant ID)", out_of_band_fields="trackingId; externalGrantId",
         chariot_list_status="n/a",
         key_quote="Some DAF providers do not pass the Tracking ID through on their remittances",
         source_url=CH_GIFTS, source_date="API docs version 2026-04-01", access_status="read", evidence_label="F",
         notes="Same page: Tracking ID 'usually as \"Tracking ID {id} - Gift through DAFpay\". Wording varies by provider.' No provider is named, so this does not show any top-10 sponsor's addenda."),
]

# --- Part B: one row per tenant x feature -------------------------------------------------------
FEAT_COLS = ["row_id", "vendor_platform", "tenant", "segment", "rank_fy2024", "feature", "value", "detail",
             "quote", "source_url", "doc_date", "recency_2025_26", "evidence_label", "access_status", "notes", "retrieved"]

COLUMBUS = "https://columbusfoundation.org/media/p1za1dz4/csuite-fund-portal-donor-resources-2025.pdf"
OMAHA = "https://omahafoundation.org/myaccount/"
TAMPA = "https://www.cftampabay.org/portal-guide"
ATL = "https://cfgreateratlanta.org/wp-content/uploads/2025/03/Fund-Advisor-Portal-Guide.pdf"
SARA = "https://www.cfsarasota.org/files/galleries/CFSarasota_Giving_Portal_Manual.pdf"
TRI = "https://trianglecf.org/wp-content/uploads/2024/10/New-Donor-Portal-Guide-October-2024-.pdf"
FND_BLOG = "https://www.foundant.com/blog/the-portal-and-the-giving-hub-what-s-new/"
FND_IDEA = "https://idealab.foundant.com/forums/597718-communitysuite-idea-lab/suggestions/48688049-export-grants-or-grant-history-new-portal"
CCT = "https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf"
GWCF = "https://www.thecommunityfoundation.org/news/our-new-donor-portal-has-arrived"
BOFA = "https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf"
REN_Q1 = "https://intercom.help/rengiving/en/articles/13792235-2026-q1-release-notes"
GKCCF = "https://www.growyourgiving.org/news/7-tips-for-maximizing-your-online-giving-experience"
FC_DET = "https://www.fidelitycharitable.org/giving-account/giving-account-details.html"
MPLS = "https://www.minneapolisfoundation.org/wp-content/uploads/2023/11/DonorView-FAQs-Final.pdf"


def f(row_id, vendor, tenant, segment, rank, feature, value, detail, quote, url, date, recent, label, access, notes=""):
    return dict(row_id=row_id, vendor_platform=vendor, tenant=tenant, segment=segment, rank_fy2024=rank,
                feature=feature, value=value, detail=detail, quote=quote, source_url=url, doc_date=date,
                recency_2025_26=recent, evidence_label=label, access_status=access, notes=notes, retrieved=RETRIEVED)


IMP, EXP, PAGE = "donor_impact_report", "self_serve_grant_export", "public_giving_page"
TOP, CFS, CFO, VEN = "top20 sponsor", "top20 sponsor (CF)", "community foundation", "vendor"

FEAT = [
    # Ren DFX "Giving Platform" (RCF and six RCF private labels)
    f("PF-01", "Ren DFX (Giving Platform)", "RCF and 6 RCF private labels", TOP, "9", IMP, "P",
      "Homepage 'Charitable Impact' widget groups grants into philanthropic categories; no outcome data",
      "Showcases your impact of giving by breaking grants into philanthropic categories.", RCF_GUIDE, "PDF 2026-10-06", "yes", "F", "read"),
    f("PF-02", "Ren DFX (Giving Platform)", "RCF and 6 RCF private labels", TOP, "9", EXP, "ND",
      "Guide covers statements, grant letters and contribution letters; no export or download of grant history described",
      "", RCF_GUIDE, "PDF 2026-10-06", "yes", "F", "read"),
    f("PF-03", "Ren DFX (Giving Platform)", "RCF and 6 RCF private labels", TOP, "9", PAGE, "ND",
      "No page for others to give to the fund; contributions are entered by the financial advisor", "", RCF_GUIDE, "PDF 2026-10-06", "yes", "F", "read"),
    f("PF-04", "Ren DFX (DonorFirst)", "Bank of America Charitable Gift Fund", TOP, "11", IMP, "P",
      "Landing page charts 'Charitable impact on different categories of Charities' and top 3 charities",
      "View your account activity by charitable sector, recent contributions and grants.", BOFA, "PDF modified 2026-02-23", "yes", "F",
      "read (cached in P-B4428-02 pass, same day)"),
    f("PF-05", "Ren DFX (DonorFirst)", "Bank of America Charitable Gift Fund", TOP, "11", EXP, "P",
      "Text describes Excel export of the contribution listing; the grant-listing screenshot also shows 'Export to Excel' (repo, batch 33B)",
      "You can export to Excel to sort and do analysis", BOFA, "PDF modified 2026-02-23", "yes", "F",
      "read (cached in P-B4428-02 pass, same day)", "Grant-listing button: research/mission-2026-11-14/queue-batch33-voids-exports-rails.md P-BNK-03 [R]"),
    f("PF-06", "Ren DFX (DonorFirst)", "Bank of America Charitable Gift Fund", TOP, "11", PAGE, "ND", "Not described", "", BOFA,
      "PDF modified 2026-02-23", "yes", "F", "read (cached in P-B4428-02 pass, same day)"),
    f("PF-07", "Ren platform (all DFX tenants)", "Giving Compass impact metrics", VEN, "", IMP, "N",
      "Charity-level impact metrics to be surfaced to donors and advisors; not a report on the donor's own grants",
      "Ren has partnered with Giving Compass", REN_Q1, "modified 2026-03-05", "yes", "F", "read"),
    f("PF-08", "Ren/Stellar iPhi", "GS DAPF; Raymond James Charitable", TOP, "5; 19", EXP, "B",
      "All iPhi tenant hosts and gspf.goldman.com disallow crawling", "", "https://rj.iphiview.com/", "", "n/a", "B",
      "blocked: robots.txt Disallow", "Same block applies to impact and giving-page features"),
    f("PF-09", "Ren/Stellar iPhi (DonorView)", "Minneapolis Foundation", CFO, "CF 19", EXP, "Y",
      "Fund activity export to Excel or PDF (2022 FAQ, outside the 2025-26 window)", "", MPLS, "PDF 2022-07-07", "no", "R",
      "repo row (donor-export-evidence-cf-2026.csv)"),
    # GivingPoint (NPT)
    f("PF-10", "NPT GivingPoint", "National Philanthropic Trust", TOP, "2", IMP, "ND",
      "Guide offers online quarterly statements and grant tracking; no impact report", "", NPT_GUIDE, "PDF 2026-10-15", "yes", "F", "read"),
    f("PF-11", "NPT GivingPoint", "National Philanthropic Trust", TOP, "2", EXP, "ND",
      "No export described in the 2026 guide; front-end code holds Excel export handlers (repo, batch 33B), availability to donors unverified",
      "", NPT_GUIDE, "PDF 2026-10-15", "yes", "F", "read", "research/mission-2026-11-14/queue-batch33-voids-exports-rails.md §4.3 [R]"),
    f("PF-12", "NPT GivingPoint", "National Philanthropic Trust", TOP, "2", PAGE, "P",
      "Third parties may contribute to a DAF, but each must sign a Contribution Agreement; no page or link",
      "Third parties may make charitable contributions to your DAF", NPT_GUIDE, "PDF 2026-10-15", "yes", "F", "read"),
    # DonorCentral (NPact)
    f("PF-13", "NPact DonorCentral", "all tenants", VEN, "", EXP, "U",
      "Vendor knowledge base not readable; tenant portals are script shells; no 2025-26 tenant guide found. Known tenants AEF (2026, to Ren) and Vermont CF (May 2025) have left",
      "", "https://npact.document360.io/fims-and-donorcentral/docs", "", "n/a", "B",
      "blocked: robots.txt redirect (document360); npact.com robots 403", "Same status for impact and giving-page features"),
    f("PF-14", "NPact Foundation Cloud", "Greater Washington Community Foundation", CFO, "CF 38", EXP, "Y",
      "Grant history and fund gift history export as CSV",
      "You can also export your grant history, or your fund’s gift history if your fund receives contributions from multiple donors, as a CSV",
      GWCF, "2026-09-21", "yes", "F", "read"),
    # GiftingNetwork
    f("PF-15", "GiftingNetwork", "The Chicago Community Trust", CFS, "12 (CF 2)", EXP, "Y",
      "CSV and chart-format gift and grant history reports",
      "You can however export CSV and chart-format gift history and grant history reports anytime.", CCT, "PDF 2025-12-02", "yes", "F", "read"),
    f("PF-16", "GiftingNetwork", "The Chicago Community Trust", CFS, "12 (CF 2)", IMP, "ND", "FAQ covers statements, grants, recurring grants, receipts; no impact report", "", CCT, "PDF 2025-12-02", "yes", "F", "read"),
    f("PF-17", "GiftingNetwork", "The Chicago Community Trust", CFS, "12 (CF 2)", PAGE, "ND",
      "Contributions described only from the donor (securities, wire, ACH, check, card)", "", CCT, "PDF 2025-12-02", "yes", "F", "read"),
    f("PF-18", "GiftingNetwork", "Foundation For The Carolinas", CFS, "15 (CF 3)", EXP, "U", "No public donor-portal guide found", "",
      "https://www.fftc.org/faqs", "live", "n/a", "F", "read; no portal text"),
    # Foundant CommunitySuite
    f("PF-19", "Foundant CommunitySuite", "vendor (Giving Hub)", VEN, "", PAGE, "Y",
      "Public 'Giving Hub' lets anyone give to funds a foundation makes public; whether a CF lists DAFs is its choice",
      "The Giving Hub is where anyone can donate to any fund you make publicly available.", FND_BLOG,
      "published 2024-08-30, modified 2026-04-22", "yes", "F", "read"),
    f("PF-20", "Foundant CommunitySuite", "vendor (fund-manager portal)", VEN, "", EXP, "Y",
      "Vendor reply (2024-08-27) records grant-history export added for fund managers",
      "Added donation and grant history export for fund managers", FND_IDEA, "2024-08-27", "no", "F", "read"),
    f("PF-21", "Foundant CommunitySuite", "The Columbus Foundation", CFO, "CF 5", EXP, "Y", "Grant history export to spreadsheet",
      "Gives you the option to export information on previous grants into a spreadsheet to save and/or print.", COLUMBUS,
      "PDF modified 2025-04-22", "yes", "F", "read"),
    f("PF-22", "Foundant CommunitySuite", "Community Foundation for Greater Atlanta", CFO, "CF 10", PAGE, "P",
      "Portal 'Donate' tab links to the public Giving Hub for public funds or causes; DAFs not stated to be listed",
      "To donate to a public fund or cause, click the Donate tab.", ATL, "PDF 2025-03-25", "yes", "F", "read"),
    f("PF-23", "Foundant CommunitySuite", "Community Foundation for Greater Atlanta", CFO, "CF 10", EXP, "ND",
      "Statements view and download only", "", ATL, "PDF 2025-03-25", "yes", "F", "read"),
    f("PF-24", "Foundant CommunitySuite", "Community Foundation Tampa Bay", CFO, "CF 21", EXP, "P",
      "CSV export documented for contribution history only", "Use the Export button to download a CSV file.", TAMPA,
      "live (new portal 2026)", "yes", "F", "read"),
    f("PF-25", "Foundant CommunitySuite", "Omaha Community Foundation", CFO, "CF 26", EXP, "Y", "Full grant list to Excel",
      "the system will create an Excel spreadsheet with the information", OMAHA, "page modified 2025-03-04 (repo)", "yes", "F", "read"),
    f("PF-26", "Foundant CommunitySuite", "Community Foundation of Sarasota County", CFO, "", EXP, "Y", "Grant history filter and export",
      "Grant History – lists the grants made by date. You can filter by date and export a list.", SARA, "PDF 2025-06-10", "yes", "F", "read"),
    f("PF-27", "Foundant CommunitySuite", "Community Foundation of Sarasota County", CFO, "", PAGE, "P",
      "Fundholder can give to own fund or another public fund; no page for others to give to the DAF",
      "You can make a secure gift to your Fund or donate to another fund managed at the", SARA, "PDF 2025-06-10", "yes", "F", "read"),
    f("PF-28", "Foundant CommunitySuite", "Triangle Community Foundation", CFO, "", PAGE, "N",
      "Donate tab exists, but the foundation will not support fundraising for its funds (2024 guide)",
      "Foundation is unable to support active fundraising or solicitation for contributions to any of the funds it holds.",
      TRI, "PDF 2024-10-07", "no", "F", "read"),
    # Sponsors on own portals
    f("PF-29", "own portal (MyGiving with NCF)", "National Christian Foundation", TOP, "10", PAGE, "Y",
      "Fundholder can share a donate button so others give directly to the Giving Fund online",
      "Including a donate button can make it easy for others to give directly to your fund online.", NCF_GUIDE, "live", "yes", "F", "read",
      "Use subject to the Program Agreement 'Donate button' section (not read)"),
    f("PF-30", "own portal (MyGiving with NCF)", "National Christian Foundation", TOP, "10", IMP, "ND", "Not described", "", NCF_GUIDE, "live", "yes", "F", "read"),
    f("PF-31", "own portal (Giving Account)", "Fidelity Charitable", TOP, "1", PAGE, "N",
      "Gift4Giving e-gift runs the other way: the account holder lets someone else pick a charity; no page for others to give in",
      "It lets the recipient support a charity of their choice using your Giving Account.", FC_DET, "live", "yes", "F", "read"),
    f("PF-32", "unidentified white-label portal", "Greater Kansas City Community Foundation", CFS, "16 (CF 4)", EXP, "P",
      "Granting history can be downloaded; format not stated", "You can also sort, filter, and download your granting history.", GKCCF,
      "published 2022-03-28, modified 2026-07-14 (repo)", "yes", "F", "read"),
]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def league_fy2024(root):
    rows = [r for r in read_csv(os.path.join(root, LEAGUE)) if r["row_type"] == "top50" and r["fiscal_year"] == "2024"]
    return {r["ein"]: r for r in rows}


def enrich(league, row):
    hit = league.get(row["ein"], {})
    return {**row, "fy2024_rank": hit.get("rank_assets", ""), "fy2024_daf_assets_usd": hit.get("daf_assets_eoy", ""),
            "retrieved": RETRIEVED}


def write(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        list(map(w.writerow, rows))
    return path


def market_total(league):
    shares = [(float(r["daf_assets_eoy"]), float(r["share_daf_assets_eoy"])) for r in league.values()
              if r["share_daf_assets_eoy"] not in ("", "0")]
    return shares[0][0] / shares[0][1]


def share_table(rows, key, total):
    sponsor_rows = [r for r in rows if r["fy2024_rank"] and int(r["fy2024_rank"]) <= 10]
    first = reduce(lambda acc, r: acc if r["ein"] in acc else {**acc, r["ein"]: r}, sponsor_rows, {})
    groups = reduce(lambda acc, r: {**acc, key(r): acc.get(key(r), 0.0) + float(r["fy2024_daf_assets_usd"])}, first.values(), {})
    top10 = sum(groups.values())
    return [(k, v / 1e9, v / top10, v / total) for k, v in sorted(groups.items(), key=lambda kv: -kv[1])], top10


def sec_class(r):
    return "no ACH (PayPal/wire)" if r["ach_sec_code"].startswith("n/a") else (
        "blocked" if "blocked" in r["access_status"] else "SEC code not stated")


def oob_class(r):
    c = r["out_of_band_channel"]
    return ("not determinable" if c.startswith("not determinable") else
            "not stated" if c in ("not stated", "") else
            "letter only" if c.startswith("grant letter;") and "portal" not in c else
            "portal/dashboard" if any(k in c for k in ("dashboard", "portal")) and "email" not in c else
            "email report + dashboard")


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    out = argv[2] if len(argv) > 2 else os.path.join(root, "data/mission-2026-11-14")
    league = league_fy2024(root)
    remit = [enrich(league, r) for r in REMIT]
    feat = FEAT
    pa = write(os.path.join(out, "grant-remittance-2026-11-19.csv"), REMIT_COLS, remit)
    pb = write(os.path.join(out, "portal-features-2026-11-19.csv"), FEAT_COLS, feat)
    total = market_total(league)
    print(f"wrote {pa} ({len(remit)} rows) and {pb} ({len(feat)} rows)")
    print(f"corrected FY2024 market total ${total/1e9:.2f}bn")
    for name, keyf in (("ACH SEC code", sec_class), ("out-of-band channel", oob_class)):
        table, top10 = share_table(remit, keyf, total)
        print(f"\n{name} by FY2024 top-10 assets (top-10 = ${top10/1e9:.2f}bn, {top10/total:.1%} of market)")
        print("\n".join(f"  {k:28s} ${b:6.2f}bn  {s:6.1%} of top-10  {m:6.1%} of market" for k, b, s, m in table))
    sec_stated = sum(1 for r in remit if r["ach_sec_code"] not in ("not stated",) and not r["ach_sec_code"].startswith(("n/a", "not")))
    addenda = sum(1 for r in remit if r["fy2024_rank"] and r["grant_id_in_addenda"].startswith(("yes", "sometimes")))
    print(f"\nrows stating an SEC code: {sec_stated}; top-10 sponsor rows documenting a grant ID in addenda: {addenda}")
    counts = Counter((r["feature"], r["value"]) for r in feat)
    print("\nportal feature rows by feature x value:")
    print("\n".join(f"  {k[0]:26s} {k[1]:3s} {v}" for k, v in sorted(counts.items())))
    print(f"recency 2025-26 rows: {sum(r['recency_2025_26'] == 'yes' for r in feat)} of {len(feat)}")


if __name__ == "__main__":
    main(sys.argv)
