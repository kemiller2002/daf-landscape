"""P-B4428-02: build ren-private-label-defaults CSV and the asset summary.

Usage: python3 -I scripts/mission_b4428_02_ren_defaults_build.py . OUT_CSV
Reads FY2024 corrected assets (row_type=top50) from
data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv.
Program evidence (quotes, URLs, PDF dates, SHA-1 prefixes) was read on 2026-11-19
with a robots-respecting fetcher (UA research-script/1.0). Assets are attached only
to sponsor-of-record rows (asset_row=Y) so private labels inside RCF are not double counted.
Stdlib only; pure functions.
"""
import csv, sys, os
from functools import reduce

RET = "2026-11-19"
LT = "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv"

# Shared documents
G26 = "Acknowledgements Specify what information the charity sees when they receive the grant. By default, this includes the grant advisor's name, email, and address, but you can customize it to show only your name, fund name, and address, or remain anonymous."
G26D = "PDF created/modified 2026-10-06 ('Giving Platform Donor User Guide')"
G26S = "93d97b49e84a"
G23 = "Acknowledgment RCF allows you to choose how you are recognized for the grant. Issue it in the name of the fund, the primary donors. Grants can also be issued anonymously. The default is “Fund Name Only”."
CIRC23 = "You may choose to have the letter acknowledge you, the account name or a special acknowledgment (for example, in memory of a person, group or event) or the grant may be made anonymously."
CIRCLEG = "A letter accompanying the grant will acknowledge the Fund and the Grant Advisor\u2019s involvement unless the Grant Advisor wishes to remain anonymous."
DFXROB = "host robots.txt 404 (no rules); fetched"

def P(**k):
    base = dict(program_id="", program="", sponsor_of_record="", sponsor_ein="", asset_row="N",
                ren_role="", portal_host="", platform_version="", default_category="", default_detail="",
                email_included="", default_quote="", default_url="", default_doc_date="", default_doc_sha1_12="",
                other_quote="", other_url="", other_doc_date="", other_reading="",
                access_robots="", evidence_label="F", repo_prior="", change_vs_repo="")
    return {**base, **k}

ROWS = (
 P(program_id="RCF-01", program="Renaissance Charitable Foundation DAF (core RCF portal)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262", asset_row="Y",
   ren_role="administers (RCF's administrator)", portal_host="rcf.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Grant advisor name, email and address by default; customisable to name, fund name, address, or anonymous",
   email_included="Y (default)", default_quote=G26, default_url="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote="Once your recommended grant has been approved, a distribution via check or ACH accompanied by a grant letter will be sent directly to the charity. You may choose to have the letter acknowledge you, the account name or a special acknowledgment ... or the grant may be made anonymously.",
   other_url="https://rcf.donorfirstx.com/pdf/RCF/RCF%20Program%20Circular.pdf", other_doc_date="PDF created 2026-06-01, modified 2026-07-23", other_reading="options, no default stated; email not mentioned",
   access_robots=DFXROB, repo_prior="donor-info-defaults-top20 RCF row (same 2026-10 guide); V34A-28 'upper bound'", change_vs_repo="confirms; adds that the same file is the guide on 7 RCF portals and that the 2023-24 RCF guide said 'Fund Name Only'"),
 P(program_id="RCF-02", program="RCF DAF Program for Ameriprise clients", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="ampf.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Same file as RCF-01", email_included="Y (default)", default_quote=G26,
   default_url="https://ampf.donorfirstx.com/pdf/AMPF/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=CIRC23, other_url="https://ampf.donorfirstx.com/pdf/AMPF/Program%20Circular.pdf", other_doc_date="PDF created 2023-11-08, modified 2025-03-14 (form 2309-RCF-FRM-DAF-CIRC)", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="relationship-graph CE0015-CE0018", change_vs_repo="NEW"),
 P(program_id="RCF-03", program="RCF DAF Program for RBC Wealth Management clients", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="rbcrcf.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Same file as RCF-01", email_included="Y (default)", default_quote=G26,
   default_url="https://rbcrcf.donorfirstx.com/pdf/RBC/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=CIRC23, other_url="https://rbcrcf.donorfirstx.com/pdf/RBC/Program%20Circular.pdf", other_doc_date="PDF created 2023-09-25, modified 2025-07-08", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="CE0019-CE0021", change_vs_repo="NEW"),
 P(program_id="RCF-04", program="Global Gift Fund (MDRT Foundation)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="mdrt.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Same file as RCF-01; the program circular instead says fund + grant advisor named unless anonymous", email_included="Y (default)", default_quote=G26,
   default_url="https://mdrt.donorfirstx.com/pdf/mdrt/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=CIRCLEG, other_url="https://mdrt.donorfirstx.com/pdf/mdrt/Program%20Circular.pdf", other_doc_date="PDF created 2016-05-17, modified 2024-04-12", other_reading="name only (fund + advisor named; no address or email)",
   access_robots=DFXROB, repo_prior="CE0060-CE0062", change_vs_repo="NEW"),
 P(program_id="RCF-05", program="RCF Giving Fund (TIAA investment options)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="rcfgivingfund.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Same file as RCF-01; circular says fund + grant advisor named unless anonymous", email_included="Y (default)", default_quote=G26,
   default_url="https://rcfgivingfund.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=CIRCLEG, other_url="https://rcfgivingfund.donorfirstx.com/pdf/RCFGF/RCF%20Giving%20Fund%20Circular.pdf", other_doc_date="PDF created 2021-02-25, modified 2025-06-28 (code RCF_GF_031221)", other_reading="name only (fund + advisor named)",
   access_robots=DFXROB, repo_prior="none (portal not in graph)", change_vs_repo="NEW"),
 P(program_id="RCF-06", program="RCF DAF option for UBS clients", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="ubs.donorfirstx.com", platform_version="both: Giving Platform guide (2026-10) and DFX guide 2309 (2024-06)",
   default_category="full contact", default_detail="Portal links two guides with opposite defaults; newest coded. Older 'UBS Donor User Guide' says Fund Name Only", email_included="Y (default, 2026 guide)", default_quote=G26,
   default_url="https://ubs.donorfirstx.com/pdf/UBS/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=G23, other_url="https://ubs.donorfirstx.com/pdf/UBS/UBS%20Donor%20User%20Guide.pdf", other_doc_date="PDF created 2023-09-06, modified 2024-06-14 (2309-RCF-FRM-DAF-DONORGUIDE, (c) 2023)", other_reading="fund name only (default stated)",
   access_robots=DFXROB, repo_prior="CE0034-CE0036", change_vs_repo="NEW: same program, two guide vintages, two defaults"),
 P(program_id="RCF-07", program="RCF DAF program for Northwestern Mutual advisors", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="sponsor RCF; Ren administers", portal_host="northwesternmutual.donorfirstx.com", platform_version="Giving Platform guide (2026-10)",
   default_category="full contact", default_detail="Same file as RCF-01", email_included="Y (default)", default_quote=G26,
   default_url="https://northwesternmutual.donorfirstx.com/pdf/NWM/Donor%20User%20Guide.pdf", default_doc_date=G26D, default_doc_sha1_12=G26S,
   other_quote=CIRC23, other_url="https://northwesternmutual.donorfirstx.com/pdf/NWM/Program%20Circular.pdf", other_doc_date="PDF created 2023-09-25, modified 2024-07-02", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="CE0032", change_vs_repo="NEW"),
 P(program_id="RCF-08", program="RCF TDA-coded portal (legacy TD Ameritrade channel)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="tda.donorfirstx.com", platform_version="DFX guide 2309 (2024-07)",
   default_category="fund name only", default_detail="Only guide on the portal is the 2023 RCF template: default 'Fund Name Only'", email_included="N (not offered in guide)", default_quote=G23,
   default_url="https://tda.donorfirstx.com/pdf/tda/RCF%20Donor%20User%20Guide.pdf", default_doc_date="PDF created 2023-09-06, modified 2024-07-12 (2309-RCF-FRM-DAF-DONORGUIDE)", default_doc_sha1_12="789efac9bf3b",
   other_quote=CIRC23, other_url="https://tda.donorfirstx.com/pdf/tda/RCF%20Program%20Circular.pdf", other_doc_date="PDF created 2023-09-25, modified 2024-06-28", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="CE0063-CE0064", change_vs_repo="NEW"),
 P(program_id="RCF-09", program="Commonwealth Charitable Fund (LPL / Commonwealth Financial Network)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers (RenPSG per circular)", portal_host="cfndaf.donorfirstx.com", platform_version="DFX guide 5/2022 (2023-04) + circular (2024-12)",
   default_category="name only", default_detail="Circular: letter acknowledges the fund and the grant advisor unless anonymous; the 2022 guide lists fund name / primary donors / anonymous with no default", email_included="N (not mentioned)", default_quote=CIRCLEG.replace("Fund", "fund").replace("Grant Advisor", "grant advisor"),
   default_url="https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf", default_doc_date="PDF created 2021-07-06, modified 2024-12-13", default_doc_sha1_12="d647c6e73c83",
   other_quote="Acknowledgment RCF allows you to choose how you are recognized for the grant. Issue it in the name of the fund, the primary donors. Grants can also be issued anonymously.", other_url="https://cfndaf.donorfirstx.com/pdf/cfndaf/CFNDAF%20Donor%20User%20Guide.pdf", other_doc_date="PDF created 2022-04-25, modified 2023-04-10 ('DFX User Guide CFN 5/2022')", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="CE0029-CE0030, CE0245-CE0246", change_vs_repo="NEW"),
 P(program_id="RCF-10", program="SEI Giving Fund", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="sei.donorfirstx.com", platform_version="DFX guide 4/2022 (2023-03) + brochure (2025-03)",
   default_category="name only", default_detail="Brochure: letter acknowledges the fund and the grant advisor unless anonymous; 2022 guide lists options with no default", email_included="N (not mentioned)",
   default_quote="A letter accompanying the grant will acknowledge the fund and the grant advisor\u2019s involvement unless the grant advisor wishes to remain anonymous.",
   default_url="https://sei.donorfirstx.com/pdf/SEI/SEI%20Giving%20Fund%20Brochure.pdf", default_doc_date="PDF created 2025-03-18", default_doc_sha1_12="1d0dc59ec64c",
   other_quote="Acknowledgment RCF allows you to choose how you are recognized for the grant. Issue it in the name of the fund, the primary donors. Grants can also be issued anonymously.", other_url="https://sei.donorfirstx.com/pdf/SEI/SEI%20Donor%20User%20Guide.pdf", other_doc_date="PDF created 2022-04-12, modified 2023-03-15 ('DFX User Guide SEI 4/2022')", other_reading="options, no default stated",
   access_robots=DFXROB, repo_prior="CE0040-CE0042", change_vs_repo="NEW"),
 P(program_id="RCF-11", program="Franklin Charitable Giving Program", sponsor_of_record="Renaissance Charitable Foundation (servicer; sponsor status 'unknown' in graph CE0053)", sponsor_ein="352129262",
   ren_role="RCF services; Ren platform", portal_host="ft.donorfirstx.com", platform_version="circular (2026-09)",
   default_category="fund name only", default_detail="Account name on every grant (stated floor); donor name or special acknowledgement per donor preference; no preselection stated", email_included="N (not mentioned)",
   default_quote="Each grant will include the name of the Franklin Templeton Charitable Giving Program account and a letter will be provided reflecting the donor\u2019s preference, which could include the account name and the donor\u2019s name, a special acknowledgment (e.g. in memory of, in honor of) or no donor information, if preferred.",
   default_url="https://ft.donorfirstx.com/pdf/ft/Donor%20Program%20Circular.pdf", default_doc_date="PDF created 2026-09-04", default_doc_sha1_12="b4dce776181a",
   other_quote="", other_url="", other_doc_date="", other_reading="", access_robots=DFXROB, evidence_label="F (floor read as default; medium)", repo_prior="CE0052-CE0056", change_vs_repo="NEW"),
 P(program_id="RCF-12", program="Salvation Army DAF (RCF-sponsored sub-funds)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="RCF sponsor; Ren administers (Ren mailbox in FAQ)", portal_host="not identified (FAQ on TSA CDN)", platform_version="FAQ (2025-04)",
   default_category="fund name only", default_detail="Sub-fund name always stated; recommender names 'you choose to include'; address only if selected; no email", email_included="N",
   default_quote="The grant check will be accompanied by a letter that states your Sub-Fund name, the recommender names you choose to include, as well as the grant purpose listed on your request. ... You have the ability to select whether or not to share your address with the charity.",
   default_url="https://8hxvw8tw.media.zestyio.com/-2025--TSA_Grants-FAQ.pdf", default_doc_date="PDF created 2023-01-19, modified 2025-04-14", default_doc_sha1_12="d9ba93ccb791",
   other_quote="", other_url="", other_doc_date="", other_reading="", access_robots="media.zestyio.com robots 404; fetched", evidence_label="F (floor read as default; medium)",
   repo_prior="nonprofit-side-panel rcf_ren (search extract [S], not opened)", change_vs_repo="confirms the [S] extract first-hand; adds address opt-in"),
 P(program_id="RCF-13", program="LPL RCF DAF channel", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="rcf.donorfirstx.com (circular names RCF portal)", platform_version="circular 2309 (2023-10)",
   default_category="no default stated", default_detail="Letter may acknowledge donor, account name, special acknowledgement, or anonymous", email_included="N (not mentioned)",
   default_quote=CIRC23, default_url="https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf", default_doc_date="PDF created 2023-10-11 (same file also at /2025/09/)", default_doc_sha1_12="52c2416fe6bb",
   access_robots="www.reninc.com robots 200, allowed", repo_prior="CE0026-CE0027", change_vs_repo="NEW"),
 P(program_id="RCF-14", program="Edward Jones Charitable Gift Fund", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="RCF manages and administers; Ren DFX portal", portal_host="edwardjones.donorfirstx.com", platform_version="n/a",
   default_category="not determinable", default_detail="Portal links no guide or circular; edwardjones.com DAF page has no acknowledgement text", email_included="unknown",
   default_url="https://edwardjones.donorfirstx.com/ ; https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds", default_doc_date="live pages read 2026-11-19",
   access_robots="both hosts allowed", evidence_label="absent", repo_prior="CE0011, CE0915, CE1045", change_vs_repo="gap"),
 P(program_id="RCF-15", program="First Citizens Donor Advised Fund", sponsor_of_record="FCDAF (RCF provides administrative services)", sponsor_ein="",
   ren_role="RCF administers; Ren DFX portal", portal_host="firstcitizensdaf.donorfirstx.com", platform_version="n/a",
   default_category="not determinable", default_detail="Portal links only a year-end deadlines PDF", email_included="unknown",
   default_url="https://firstcitizensdaf.donorfirstx.com/", default_doc_date="live page read 2026-11-19", access_robots=DFXROB, evidence_label="absent", repo_prior="CE0057-CE0059", change_vs_repo="gap"),
 P(program_id="RCF-16", program="Janney Charitable Giving Fund", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="janney.donorfirstx.com", platform_version="n/a",
   default_category="not determinable", default_detail="Portal links only a 2025 year-end timeline", email_included="unknown",
   default_url="https://janney.donorfirstx.com/", default_doc_date="live page read 2026-11-19", access_robots=DFXROB, evidence_label="absent", repo_prior="CE0022-CE0024", change_vs_repo="gap"),
 P(program_id="RCF-17", program="Fisher Investments and Pershing RCF DAF channels", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="administers", portal_host="reninc.com channel pages", platform_version="n/a",
   default_category="not determinable", default_detail="Channel pages carry no acknowledgement text", email_included="unknown",
   default_url="https://www.reninc.com/rcf-fisher-daf/ ; https://www.reninc.com/rcf-pershing-daf/", default_doc_date="live pages read 2026-11-19", access_robots="www.reninc.com robots 200, allowed", evidence_label="absent", repo_prior="CE0065-CE0069", change_vs_repo="gap"),
 P(program_id="RCF-18", program="Azzad Asset Management (RCF program on iPhi)", sponsor_of_record="Renaissance Charitable Foundation", sponsor_ein="352129262",
   ren_role="Ren iPhi platform", portal_host="rcf.iphiview.com/azzad", platform_version="iPhi",
   default_category="not determinable", default_detail="iPhi host disallows all generic agents", email_included="unknown",
   default_url="https://rcf.iphiview.com/azzad/", access_robots="iphiview.com robots 'User-agent: * Disallow: /' (blocked)", evidence_label="blocked", repo_prior="CE0176", change_vs_repo="gap"),
 P(program_id="MSG-01", program="Morgan Stanley GIFT", sponsor_of_record="Morgan Stanley Global Impact Funding Trust", sponsor_ein="527082731", asset_row="Y",
   ren_role="administers (990) + DFX portal", portal_host="msgift.donorfirstx.com", platform_version="Grantee Guidelines (2022-09)",
   default_category="fund name only", default_detail="Letter identifies the DAF name unless anonymous; address only if donor elects", email_included="N",
   default_quote="the grant check and an accompanying letter sent to the recommended Grantee will identify the name of the donor advised fund from which the grant was made (unless the donor has requested anonymity). Donors may elect to have their address included in the grant letter to the recipient organization for recognition purposes.",
   default_url="https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf", default_doc_date="PDF created 2022-09-21, modified 2022-09-22", default_doc_sha1_12="52606958424b",
   other_quote="The letter includes the name of the Account, or Donor as specified during the grant recommendation process.", other_url="https://www.morganstanley.com/gift", other_doc_date="live page (Last-Modified header 2026-11-19)", other_reading="account or donor as specified; no default stated",
   access_robots=DFXROB + "; www.morganstanley.com robots 200, allowed", evidence_label="F (medium: live FAQ weaker, V34A-26)", repo_prior="donor-info-defaults-top20 MS GIFT row", change_vs_repo="confirms"),
 P(program_id="BOA-01", program="Bank of America Charitable Gift Fund", sponsor_of_record="Bank of America Charitable Gift Fund", sponsor_ein="046010342", asset_row="Y",
   ren_role="technology provider (confirmed); administers (inferred, weakened E083)", portal_host="bofa.donorfirst.org", platform_version="BofA DonorFirst guide (2026-02); BofA-specific front-end hosts per repo CE0169",
   default_category="fund name only", default_detail="Portal guide: acknowledgement shown on the check; default Fund Name Only; custom acknowledgements and anonymity selectable", email_included="N",
   default_quote="Acknowledgement (to whom the charity might want to write a thank you note) • This will be displayed on the check • You can select to Remain Anonymous • You can create and save custom acknowledgements • The default is Fund Name Only",
   default_url="https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf", default_doc_date="PDF created 2025-11-14, modified 2026-02-23", default_doc_sha1_12="8c6c6bc5fdd9",
   other_quote="Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested.", other_url="https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf", other_doc_date="PDF created 2024-06-05, modified 2024-09-18", other_reading="name only (account + donor/advisor name)",
   access_robots="bofa.donorfirst.org robots 404; www.bankofamerica.com robots 200, allowed", repo_prior="donor-info-defaults-top20 BofA row; V34A-30", change_vs_repo="confirms"),
 P(program_id="AEF-01", program="American Endowment Foundation", sponsor_of_record="American Endowment Foundation", sponsor_ein="341747398", asset_row="Y",
   ren_role="administers + technology (2026 migration; aef.donorfirstx.com redirects to AEF maintenance page)", portal_host="portal.aefonline.org (aef.donorfirstx.com)", platform_version="AEF FAQ (modified 2026-02-19), before or during migration",
   default_category="no default stated", default_detail="Letter recognises donor or account name per donor's instructions; anonymity on request", email_included="N (not mentioned)",
   default_quote="the accompanying letter will recognize the donor or account name (per your instructions) who recommended the particular grant. You may also remain anonymous if you wish.",
   default_url="https://www.aefonline.org/thought-leadership/faqs-individual-donors/", default_doc_date="page published 2022-01-19, modified 2026-02-19",
   other_quote="Our Charity Portal is now live. Powered by Ren, charities can claim their organization, provide ACH information, and prepare to manage upcoming Grant Letters.", other_url="https://www.aefonline.org/charities/", other_doc_date="live page read 2026-11-19", other_reading="confirms Ren platform",
   access_robots="www.aefonline.org robots 200, allowed; aef.donorfirstx.com robots 404", repo_prior="donor-info-defaults-top20 AEF row; CE0078-CE0079", change_vs_repo="confirms; adds that AEF is now Ren-administered"),
 P(program_id="CJP-01", program="Combined Jewish Philanthropies DAF", sponsor_of_record="Combined Jewish Philanthropies of Greater Boston", sponsor_ein="042103559", asset_row="Y",
   ren_role="technology provider (DFX portal)", portal_host="cjp.donorfirstx.com", platform_version="CJP policies (2026-04)",
   default_category="fund name only", default_detail="Policy section: distribution identifies the DAF name unless otherwise requested; name, address and email added at donor direction", email_included="elected (at donor direction)",
   default_quote="Any distribution from a Donor Advised Fund shall identify to the grantee organization by the name of the Donor Advised Fund from which the distribution is made unless otherwise requested by the Donor of the Donor Advised Fund.",
   default_url="https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf", default_doc_date="PDF created 2026-04-29", default_doc_sha1_12="37f74e6d953a",
   other_quote="This can include the name of your DAF, your name, your address, and your email, each at your direction.", other_url="https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf", other_doc_date="same PDF", other_reading="options at donor direction",
   access_robots="ma.cjp.org robots 200, allowed; cjp.donorfirstx.com robots 404", evidence_label="F (medium)", repo_prior="donor-info-defaults-top20 CJP row: 'donor chooses; no default stated'", change_vs_repo="CHANGES: same PDF also states a fund-name rule (section 4.5)"),
 P(program_id="TRP-01", program="T. Rowe Price Program for Charitable Giving", sponsor_of_record="T Rowe Price Program for Charitable Giving", sponsor_ein="311709466", asset_row="Y",
   ren_role="technology provider (990; DFX portal)", portal_host="pcg.donorfirstx.com", platform_version="FAQ (live) + brochure (2026-11)",
   default_category="no default stated", default_detail="Donor may request advisor name, account name and address, or anonymity; 'If no address is provided ... they do not expect a thank-you'", email_included="N (not offered)",
   default_quote="You can request that the grant recognition include your name as the advisor for the grant, the name of the account, and the address. Or you can remain anonymous.",
   default_url="https://www.trowepricecharitable.org/information/frequently-asked-questions.html", default_doc_date="live page read 2026-11-19",
   other_quote="Grants you make through T. Rowe Price Charitable can identify you as the donor, include your address, and provide the name of your account. ... If you prefer, grants can also be made anonymously.", other_url="https://www.trowepricecharitable.org/content/dam/pcg-site/pdfs/GIVE%20Brochure.pdf", other_doc_date="PDF created 2026-11-10", other_reading="options, no default stated",
   access_robots="www.trowepricecharitable.org robots 404; pcg.donorfirstx.com robots 404", repo_prior="CE0212", change_vs_repo="NEW"),
 P(program_id="GCCF-01", program="Gulf Coast Community Foundation DAFs", sponsor_of_record="Gulf Coast Community Foundation", sponsor_ein="570908490",
   ren_role="technology provider (DFX portal)", portal_host="gccf.donorfirstx.com", platform_version="n/a",
   default_category="not determinable", default_detail="Portal links no guide; www.gulfcoastcf.org home page has no acknowledgement text", email_included="unknown",
   default_url="https://gccf.donorfirstx.com/ ; https://www.gulfcoastcf.org/", default_doc_date="live pages read 2026-11-19", access_robots=DFXROB, evidence_label="absent", repo_prior="CE0081", change_vs_repo="gap"),
 P(program_id="OAK-01", program="Oak Foundation DAF portal (oak.donorfirst.org)", sponsor_of_record="not identified", sponsor_ein="",
   ren_role="technology provider (DonorFirst portal)", portal_host="oak.donorfirst.org", platform_version="n/a",
   default_category="not determinable", default_detail="Portal links an application and two PDFs; all three return 404", email_included="unknown",
   default_url="https://oak.donorfirst.org/", default_doc_date="live page read 2026-11-19", access_robots="robots 404; PDFs 404", evidence_label="absent", repo_prior="host listed only", change_vs_repo="NEW host, gap"),
 P(program_id="GS-01", program="Goldman Sachs Philanthropy Fund (GS DAF)", sponsor_of_record="GS Donor Advised Philanthropy Fund", sponsor_ein="311774905", asset_row="Y",
   ren_role="technology provider (CE0163)", portal_host="gspf.goldman.com", platform_version="n/a",
   default_category="not determinable", default_detail="robots.txt disallows all generic agents", email_included="unknown", default_url="https://gspf.goldman.com/gspf/",
   access_robots="gspf.goldman.com robots 200 'User-agent: * Disallow: /' (blocked)", evidence_label="blocked", repo_prior="donor-info-defaults-top20 GS row", change_vs_repo="gap persists"),
 P(program_id="RJ-01", program="Raymond James Charitable Endowment Fund", sponsor_of_record="Raymond James Charitable Endowment Fund", sponsor_ein="593652538", asset_row="Y",
   ren_role="technology provider (iPhi tenant rj.iphiview.com, CE0755)", portal_host="rj.iphiview.com", platform_version="iPhi",
   default_category="not determinable", default_detail="iPhi host disallows all generic agents; www.raymondjamescharitable.org robots.txt not retrievable (connection failure today; 403 in b44n28-01)", email_included="unknown",
   default_url="https://rj.iphiview.com/rj/ ; https://www.raymondjamescharitable.org/",
   access_robots="rj.iphiview.com robots 'User-agent: * Disallow: /'; raymondjamescharitable.org robots fetch failed", evidence_label="blocked", repo_prior="donor-info-defaults-top20 RJ row", change_vs_repo="gap persists; Ren link is iPhi (technology), not administration"),
 P(program_id="IPHI-00", program="Other iPhi / Stellar tenants (CF and faith-based sponsors; 13 tenant URLs tried)", sponsor_of_record="various (see ren-iphi-tenant-census.csv)", sponsor_ein="",
   ren_role="technology provider (iPhi)", portal_host="*.iphiview.com; iphi.stellartechsol.com", platform_version="iPhi",
   default_category="not determinable", default_detail="Every iPhi host tried serves robots.txt ending 'User-agent: * Disallow: /'", email_included="unknown",
   default_url="https://rj.iphiview.com/robots.txt ; https://iphi.stellartechsol.com/robots.txt",
   access_robots="blocked (13 tenant URLs, 0 fetched)", evidence_label="blocked", repo_prior="ren-iphi-tenant-census.csv", change_vs_repo="gap"),
)

CATS = ("full contact", "name only", "fund name only", "anonymous", "no default stated", "not determinable")

def assets(root):
    with open(os.path.join(root, LT), newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["fiscal_year"] == "2024" and r["row_type"] == "top50"]
    by = {r["ein"]: float(r["daf_assets_eoy"]) for r in rows}
    market = float(rows[0]["daf_assets_eoy"]) / float(rows[0]["share_daf_assets_eoy"])
    return by, market

def enrich(row, by, market, ren_total):
    a = by.get(row["sponsor_ein"]) if row["asset_row"] == "Y" else None
    return {**row,
            "fy2024_daf_assets_usd": "" if a is None else f"{a:.0f}",
            "share_of_ren_linked_assets": "" if a is None else f"{a/ren_total:.4f}",
            "share_of_market_fy2024": "" if a is None else f"{a/market:.4f}",
            "retrieved": RET}

def bucket_table(key_rows, total, market):
    sums = {c: reduce(lambda s, r: s + float(r["fy2024_daf_assets_usd"]), [r for r in key_rows if r["default_category"] == c], 0.0) for c in CATS}
    names = {c: "; ".join(r["program_id"] for r in key_rows if r["default_category"] == c) for c in CATS}
    return [(c, names[c], sums[c], sums[c] / total, sums[c] / market) for c in CATS]

def fmt(tbl, total, market, title):
    head = f"\n{title}\n| Default | Sponsors | FY2024 $bn | Share of set | Share of market |\n|---|---|---|---|---|\n"
    body = "".join(f"| {c} | {n} | {s/1e9:.2f} | {s/total:.1%} | {s/market:.2%} |\n" for c, n, s, _, _ in tbl)
    return head + body + f"| **Total** | | {total/1e9:.2f} | 100.0% | {total/market:.2%} |\n"

def main(root, out_csv):
    by, market = assets(root)
    sponsor_rows = [r for r in ROWS if r["asset_row"] == "Y"]
    ren_total = sum(by[r["sponsor_ein"]] for r in sponsor_rows)
    rows = [enrich(r, by, market, ren_total) for r in ROWS]
    cols = list(rows[0].keys())
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader(); w.writerows(rows)
    keyed = [r for r in rows if r["asset_row"] == "Y"]
    admin = [r for r in keyed if r["program_id"] in ("RCF-01", "MSG-01", "BOA-01", "AEF-01")]
    at = sum(float(r["fy2024_daf_assets_usd"]) for r in admin)
    alt = [{**r, "default_category": "fund name only"} if r["program_id"] == "RCF-01" else r for r in keyed]
    print(f"rows={len(rows)} market_total_bn={market/1e9:.2f} ren_linked_total_bn={ren_total/1e9:.2f} ren_admin_total_bn={at/1e9:.2f}")
    print(fmt(bucket_table(admin, at, market), at, market, "A. Ren-administered sponsors (RCF, MS GIFT, BofA CGF, AEF); RCF coded by its 2026-10 guide"))
    print(fmt(bucket_table(keyed, ren_total, market), ren_total, market, "B. All Ren-linked sponsors in the FY2024 top 50 (A + CJP, T. Rowe, GS DAF, Raymond James)"))
    alt_admin = [r for r in alt if r["program_id"] in ("RCF-01", "MSG-01", "BOA-01", "AEF-01")]
    print(fmt(bucket_table(alt_admin, at, market), at, market, "C. As A, with RCF coded by its 2023-24 DFX guide (Fund Name Only)"))
    print(fmt(bucket_table(alt, ren_total, market), ren_total, market, "D. As B, with RCF coded by its 2023-24 DFX guide (Fund Name Only)"))
    print("RCF program rows by category:", {c: sum(1 for r in rows if r["program_id"].startswith("RCF") and r["default_category"] == c) for c in CATS})
    print("all rows by category:", {c: sum(1 for r in rows if r["default_category"] == c) for c in CATS})

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
