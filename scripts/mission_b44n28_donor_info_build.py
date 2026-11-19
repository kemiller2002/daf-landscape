"""Build donor-info-defaults-top20 CSV and asset-weighted summary.
Usage: python3 -I build.py REPO_ROOT OUT_CSV SUMMARY_MD
Reads the FY2024 top-20 from data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv."""
import csv, sys, os
from functools import reduce

RET = "2026-11-19"
FID_ACK = "https://www.fidelitycharitable.org/faqs/all/account-holder-acknowledgements.html"
FID_NP = "https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html"
FID_GUIDE = "https://www.fidelitycharitable.org/giving-account-guide/recommending-a-grant.html"
DAFD = "https://www.dafdirect.org/about-daf-direct/index.html"
CH_SRC = "https://help.givechariot.com/getting-started/sources.md"

# One record per EIN. Fields: cat, detail, q/u/d per field.
R = {
 "110303001": dict(sponsor="Fidelity Charitable", cat="full contact",
  detail="Full acknowledgement (name, mailing address, Giving Account name) preselected on every grant; partial (Giving Account name only) or anonymous selectable per grant; account default changeable by phone",
  dq="Each time you recommend a grant, you will be automatically defaulted to this full acknowledgement option; however, you may also choose to grant partially anonymously or fully anonymously.", du=FID_ACK, dd="live page (undated), read 2026-11-19",
  mc="N (preselected default; donor may change)", mq="While the account default is full acknowledgement, all three acknowledgement options are generally available to choose from at the time of recommendation for each grant. You can call us to elect another acknowledgement option as the default.", mu=FID_ACK, md="live page (undated)",
  ea="address yes (default); donor email not stated", eq="Full acknowledgement - includes name, address, and Giving Account name ... defaulting to provide a name and mailing address when a donor recommends a grant.", eu=FID_ACK+" ; "+FID_NP, ed="live pages (undated)",
  sd="Y (charity may contact donor when name and address shared; DAF Direct widget lets donors recommend from the charity's site)", sq="Account Holders may alternatively request that their name and address be included along with the Giving Account name, in which case they may also receive direct acknowledgments from recipient charities", su=FID_GUIDE, sdd="live page (undated)",
  api="Y: DAF Direct (sponsor-run widget, 3 sponsors); Stripe and ACH EFT pass donor-permitted fields to the charity (Stripe dashboard export); Chariot lists Fidelity Charitable as a 'managed source' (charity-side reconciliation, paid plan)", aq="Both Stripe and ACH allow your organization to see any information the donor has chosen to share with the grant-receiving nonprofit. / DAF Direct currently facilitates grant recommendations from donors of Fidelity Charitable, DAFgiving360, and the BNY Mellon Charitable Gift Fund", au=FID_NP+" ; "+DAFD+" ; "+CH_SRC, ad="live pages, read 2026-11-19",
  access="allowed (fidelitycharitable.org robots 200)", label="F",
  outcome="2026 Giving Report: 2025 grants 80% donor name and address, 15% Giving Account name only, 5% anonymous (https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf, PDF 2026-04-21); nonprofit FAQ still says 4% anonymous",
  repo="A13 anonymity-data-flow-2026.csv / nonprofit-side-panel-2026-evidence.csv: 'donor-permitted only'; default not recorded", change="NEW: default is full contact (opt-out), not withheld"),
 "237825575": dict(sponsor="National Philanthropic Trust", cat="donor chooses; no default stated",
  detail="Donor picks any combination of fund name, primary/joint advisor names and primary advisor's address, or anonymous; NPT guide gives no default",
  dq="When you recommend a grant from your DAF, you can choose to be recognized by the fund name, the name(s) of the primary and joint advisors on file for the account, the donor address on file for the primary advisor, or any combination of those three. You may also request that the grant be sent anonymously.", du="https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf", dd="PDF created 2026-10-15",
  mc="Y? (acknowledgment preference is a step of each recommendation; whether the form preselects is not public)", mq="Specify grant purpose, timing, recurrence if any, and acknowledgment preference", mu="https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf", md="PDF created 2026-10-15",
  ea="address if donor selects it; email not offered in guide", eq="the donor address on file for the primary advisor, or any combination of those three", eu="https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf", ed="PDF created 2026-10-15",
  sd="not documented", sq="", su="", sdd="",
  api="Y: PayPal Grant Payments transmits donor-selected PII to the charity's PayPal dashboard", aq="all personally identifiable information selected by the donor to be shared with the nonprofit is securely transmitted", au="https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/", ad="2022-08-25",
  access="allowed (nptrust.org robots 200)", label="F", outcome="",
  repo="A15 anonymity-data-flow-2026.csv: donor chooses (same quote)", change="confirms repo; adds that no default is stated"),
 "311640316": dict(sponsor="DAFgiving360", cat="not determinable (live site blocked; 2024 policy lists options without a default)",
  detail="2024 Program Policies: grant award letter identifies account holder by name + special account name and/or address; name or account name only; or anonymously with explanatory note. No default stated. 2026 help pages not readable",
  dq="an account holder may choose to be identified to the charity in one of the following ways: By the account holder's name, the special account name (e.g., \"The Smith Family Fund\"), and/or an address; By the account holder's name or the special account name only, and/or no address; Anonymously with an explanatory note.", du="https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf", dd="2024 Program Policies (PDF modified 2024-12-12)",
  mc="unknown", mq="does not release the account holder's name and contact information to any recipient charity without the account holder's explicit consent", mu="https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf", md="PDF modified 2024-12-12",
  ea="address if chosen; email not stated", eq="the special account name ... and/or an address", eu="https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf", ed="PDF modified 2024-12-12",
  sd="N for enclosures (no personal letters with checks); Y via DAFpay where donor confirms contact details for the nonprofit", sq="DAFgiving360 cannot include with the grant checks and award letters any personal letters, cards, attachments, or enclosures from donors to recipient charities.", su="https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf", sdd="PDF modified 2024-12-12",
  api="Y: DAF Direct participant; Chariot DAFpay 'new access method' for DAFgiving360 (emailed code / passkey, sponsor confirms by phone), donor confirms 'gift and contact details for the nonprofit'", aq="The donor will confirm their gift and contact details for the nonprofit by submitting the request.", au="https://givechariot.com/resources/insights/new-access-method-for-dafgiving360-in-dafpay.md ; "+DAFD, ad="2026-05-31; DAF Direct live 2026-11-19",
  access="www.dafgiving360.org robots.txt 403 (blocked; not fetched); policy PDF on static1.squarespace.com (robots 404, fetched)", label="F (2024 policy); blocked (2026 site)", outcome="",
  repo="A12 anonymity-data-flow-2026.csv: three letter options (2024)", change="unchanged; default still unobserved"),
 "232888152": dict(sponsor="Vanguard Charitable", cat="fund name only",
  detail="Account name appears in grant distribution details unless anonymity requested; advisor may add personal information",
  dq="The account name will appear in letters and communications about the account, including grant distribution details, unless anonymity is requested.", du="https://www.vanguardcharitable.org/company-policies/policies-and-guidelines", dd="Policies & Guidelines (updated 2026-01-09 per repo), read 2026-11-19",
  mc="N (account name by default; personal information is an added choice)", mq="When recommending a grant, the account advisor or full access interested party may choose to include the fund name and/or their personal information in the details provided to the recipient charity, or to remain anonymous.", mu="https://www.vanguardcharitable.org/company-policies/policies-and-guidelines", md="read 2026-11-19",
  ea="only if donor elects personal information", eq="When donor contact information is provided, you may thank them", eu="https://www.vanguardcharitable.org/nonprofit-organizations", ed="live page, read 2026-11-19",
  sd="Y if donor elects personal information", sq="If a donor has chosen to give anonymously or only share the fund name, it indicates that they do not wish to receive an acknowledgment for that specific grant.", su="https://www.vanguardcharitable.org/nonprofit-organizations", sdd="live page",
  api="Y: PayPal Grant Payments (donor-selected PII to charity dashboard)", aq="Vanguard Charitable is now issuing Grant Payments with PayPal.", au="https://www.vanguardcharitable.org/nonprofit-organizations", ad="live page, read 2026-11-19",
  access="allowed", label="F", outcome="Nonprofit page states both 'Only 4% of grants are completely anonymous' and 'Only 5% of grants are completely anonymous'",
  repo="A14 / nonprofit-side-panel: 'account name appears by default unless anonymity requested'", change="confirms repo"),
 "311774905": dict(sponsor="Goldman Sachs Philanthropy Fund (GS DAF)", cat="not determinable (blocked)",
  detail="gspf.goldman.com robots.txt disallows all generic agents; only public circular is 2008 (excluded); no 2021+ public grant-letter text found",
  dq="", du="https://gspf.goldman.com/gspf/", dd="",
  mc="unknown", mq="", mu="", md="", ea="unknown", eq="", eu="", ed="", sd="unknown", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="gspf.goldman.com robots.txt 'User-agent: * Disallow: /' (blocked)", label="blocked", outcome="",
  repo="gap19-fee-and-delivery-refresh.md FR06 (same block)", change="gap persists"),
 "205205488": dict(sponsor="Silicon Valley Community Foundation", cat="set at account opening (advisor names as specified; address by election)",
  detail="Fund agreement asks how advisor names appear and requires a choice of home address, business address or no address on the custom grant award letter; fund-wide or per-grant anonymity",
  dq="Specify below how you would like the name(s) of the fund advisors to appear in the custom grant award letter ... Please indicate your contact preference for the custom grant letter. Choose one: Provide my home address. Provide my business address. Do not provide my address.", du="https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", dd="PDF modified 2025-08-22",
  mc="Y at account opening (address choice); per-grant anonymity optional", mq="Please make all grants from the fund anonymous. (Note: Anonymity can be customized on a grant-by-grant basis.)", mu="https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", md="PDF modified 2025-08-22",
  ea="address only if elected; email not offered", eq="Provide my home address. Provide my business address. Do not provide my address.", eu="https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", ed="PDF modified 2025-08-22",
  sd="Y (address election lets the charity write directly); SVCF does not forward mail", sq="An organization that has received grants from the fund may wish to send information to you directly. ... Mail received by SVCF for the fund will not be forwarded.", su="https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf", sdd="PDF modified 2025-08-22",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="",
  repo="nonprofit-side-panel-2026-cf-supplement.csv cf_svcf: 'Advisor name(s) by default; address only if requested'", change="refines: address is a required election ('Choose one'), not an opt-in request"),
 "527082731": dict(sponsor="Morgan Stanley GIFT", cat="fund name only",
  detail="Grant letter identifies the DAF name unless anonymity requested; donor may elect to add address",
  dq="the grant check and an accompanying letter sent to the recommended Grantee will identify the name of the donor advised fund from which the grant was made (unless the donor has requested anonymity). Donors may elect to have their address included in the grant letter", du="https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf", dd="PDF 2022-09-22",
  mc="N (fund name by default; address opt-in)", mq="The letter includes the name of the Account, or Donor as specified during the grant recommendation process.", mu="https://www.morganstanley.com/gift", md="live FAQ, read 2026-11-19",
  ea="address only if donor elects; email not stated", eq="Donors may elect to have their address included in the grant letter to the recipient organization for recognition purposes.", eu="https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf", ed="PDF 2022-09-22",
  sd="not documented", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="allowed (morganstanley.com robots 200; msgift.donorfirstx.com no robots.txt, 404). Donor Circular (Aug 2024) text is font-encoded and unreadable", label="F", outcome="",
  repo="not covered", change="NEW"),
 "341747398": dict(sponsor="American Endowment Foundation", cat="donor chooses; no default stated",
  detail="Letter recognises 'the donor or account name (per your instructions)'; anonymity on request; online form has fully and semi-anonymous options (search extract only)",
  dq="the accompanying letter will recognize the donor or account name (per your instructions) who recommended the particular grant. You may also remain anonymous if you wish.", du="https://www.aefonline.org/thought-leadership/faqs-individual-donors/", dd="live FAQ, read 2026-11-19",
  mc="unknown (form not public)", mq="If you request anonymity on the Grant Recommendation Form, AEF will make the grant without disclosing your identity to the grantee organization. This can be done selectively or for all grants.", mu="https://www.aefonline.org/thought-leadership/faqs-individual-donors/", md="live FAQ",
  ea="not stated", eq="A grant letter is sent to the charity, informing them of the grant and providing additional information if requested by the donor.", eu="https://www.aefonline.org/wp-content/uploads/2023/07/Grant-Recommendation-Process-for-Donors.pdf", ed="PDF 2021-12-09 (V.21-10)",
  sd="Y (additional information 'if requested by the donor'; Donor Purpose Statement field)", sq="providing additional information if requested by the donor", su="https://www.aefonline.org/wp-content/uploads/2023/07/Grant-Recommendation-Process-for-Donors.pdf", sdd="PDF 2021-12-09",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="",
  repo="nonprofit-side-panel-2026-evidence.csv aef: 'not found'", change="NEW: per-instruction recognition, anonymity opt-in; default still unstated"),
 "352129262": dict(sponsor="Renaissance Charitable Foundation", cat="full contact",
  detail="RCF donor portal (DFX) acknowledgement defaults to grant advisor's name, email and address; customisable to name, fund name, address, or anonymous",
  dq="Acknowledgements: Specify what information the charity sees when they receive the grant. By default, this includes the grant advisor's name, email, and address, but you can customize it to show only your name, fund name, and address, or remain anonymous.", du="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", dd="PDF 2026-10-06",
  mc="N (preselected default)", mq="By default, this includes the grant advisor's name, email, and address", mu="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", md="PDF 2026-10-06",
  ea="email and address yes (default)", eq="includes the grant advisor's name, email, and address", eu="https://rcf.donorfirstx.com/pdf/RCF/Donor%20User%20Guide.pdf", ed="PDF 2026-10-06",
  sd="Y (custom acknowledgement; special recognition)", sq="You may choose to have the letter acknowledge you, the account name or a special acknowledgment (for example, in memory of a person, group or event) or the grant may be made anonymously.", su="https://rcf.donorfirstx.com/pdf/RCF/RCF%20Program%20Circular.pdf", sdd="PDF 2026-06-01",
  api="partial: Chariot lists 'Ren (Pinkaloo)' as a managed source; no RCF-specific API sharing found", aq="Ren (Pinkaloo)", au=CH_SRC, ad="live 2026-11-19",
  access="rcf.donorfirstx.com no robots.txt (404); fetched", label="F", outcome="",
  repo="nonprofit-side-panel rcf_ren [S]: 'sub-fund name on letter unless anonymous' (Salvation Army program FAQ)", change="CHANGES repo: RCF's own 2026 guide defaults to name+email+address; the TSA FAQ describes one private-label program"),
 "581493949": dict(sponsor="National Christian Foundation", cat="full contact",
  detail="Fund name appears alongside donor name and address on the letter accompanying each grant unless anonymity requested",
  dq="This name appears alongside your name and address on correspondence, including the letter that accompanies each grant issued by the fund. If you request anonymity, the name will not be displayed on grant distributions.", du="https://ncfgiving.com/guide", dd="live page, read 2026-11-19",
  mc="N (named by default; anonymity on request)", mq="You can choose to include your name or remain anonymous.", mu="https://www.ncfgiving.com/giving-fund", md="live page",
  ea="address yes; email not stated", eq="alongside your name and address on correspondence, including the letter that accompanies each grant", eu="https://ncfgiving.com/guide", ed="live page",
  sd="not documented", sq="", su="", sdd="",
  api="none found (NCF not on Chariot partner lists per repo)", aq="", au="", ad="",
  access="allowed", label="F", outcome="",
  repo="nonprofit-side-panel ncf: anonymity signalled by missing name on Excel letter", change="NEW: default is name+address"),
 "046010342": dict(sponsor="Bank of America Charitable Gift Fund", cat="fund name only",
  detail="Ren DonorFirst portal guide: acknowledgement default is Fund Name Only; donor can choose anonymous or saved custom acknowledgements (name and address shown in example)",
  dq="Acknowledgement (to whom the charity might want to write a thank you note) - This will be displayed on the check - You can select to Remain Anonymous - You can create and save custom acknowledgements - The default is Fund Name Only", du="https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf", dd="PDF created 2025-11-14, modified 2026-02-23",
  mc="N (preselected default)", mq="The default is Fund Name Only", mu="https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf", md="PDF 2026-02-23",
  ea="only via custom acknowledgement (address shown in example); email not stated", eq="Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested.", eu="https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf", ed="PDF 2024-06-05",
  sd="Y (custom acknowledgements)", sq="You can create and save custom acknowledgements", su="https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf", sdd="PDF 2026-02-23",
  api="none found", aq="", au="", ad="",
  access="allowed (bankofamerica.com robots 200; bofa.donorfirst.org no robots.txt, 404)", label="F", outcome="Conflict: 2024 Program Guidelines say distributions carry account name and Donor/Advisor name; the 2025-26 portal guide says the default is fund name only. Portal guide used as the current default",
  repo="not covered (sponsor-data-feeds cites same guide for exports only)", change="NEW"),
 "362167000": dict(sponsor="The Chicago Community Trust", cat="name only",
  detail="Award letter names the DAF advisor unless anonymous; per-grant 'I wish to remain anonymous' box; fund-level default anonymity can be set at opening",
  dq="The letter will include the name of the DAF-advisor unless they choose to remain anonymous", du="https://www.cct.org/wp-content/uploads/2024/08/Donor-Advised-Fund-101-for-Nonprofits_August-2024.pdf", dd="Sept 2025 per repo (carried; cct.org robots 403 on 2026-11-19)",
  mc="N (named by default; anonymity opt-in per grant or fund-wide)", mq="Primary donors may indicate a default preference for anonymity when completing the fund agreement. Any current advisor may request anonymity on a per grant basis.", mu="https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf", md="PDF 2024-04-08",
  ea="not stated", eq="", eu="", ed="",
  sd="not documented", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="www.cct.org robots.txt 403 (blocked; quote carried from repo); donorportal.cct.org allowed", label="F (repo) + F", outcome="",
  repo="nonprofit-side-panel-2026-cf-supplement.csv cf_cct", change="confirms repo"),
 "262048480": dict(sponsor="ImpactAssets", cat="full contact",
  detail="Default acknowledgment includes primary donor and joint advisor name and address plus account name; paper form asks donor to select one of four options",
  dq="The default acknowledgment will include the Primary Donor's (and Joint Advisor, if one exists) name and address.", du="https://impactassets.freshdesk.com/support/solutions/articles/62000217339-are-grants-from-my-impactassets-donor-advised-fund-account-anonymous-or-can-i-be-recognized-for-my-g", dd="2021-05-27",
  mc="N online (default); Y on paper form ('Please select one')", mq="ImpactAssets grant payments are accompanied by a letter to the charity that includes the ImpactAssets Donor Advised Fund account name, as well as the name and address of the individual(s) named on the account. Please select one of the following acknowledgement options", mu="https://impactassets.org/ge535a_ia_daf_grant-recommendation-form", md="form March 2025 (PDF 2025-02-26)",
  ea="address yes; email not stated", eq="name and address of the individual(s) named on the account", eu="https://impactassets.org/ge535a_ia_daf_grant-recommendation-form", ed="PDF 2025-02-26",
  sd="Y ('Recognize the following individual(s)')", sq="Recognize the following individual(s):", su="https://impactassets.org/ge535a_ia_daf_grant-recommendation-form", sdd="PDF 2025-02-26",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="", repo="not covered", change="NEW"),
 "237174183": dict(sponsor="Jewish Communal Fund", cat="donor must choose (fund name always; names and addresses or anonymous)",
  detail="Grant Recommendation Form: letter includes fund name and either signers' names/addresses or named fundholders' names/addresses, or ANONYMOUS; no preselected option on the form",
  dq="GRANT ACKNOWLEDGEMENT Grants are sent with a letter that includes the name of your fund and: The name(s) and address(es) of the Fundholder(s)/Authorized Parties signing this form / The name(s) and address(es) of the following Fundholder(s) and Authorized Parties named on the fund / ANONYMOUS (fund name and fund participants are not listed)", du="https://jcfny.org/wp-content/uploads/2021/02/GRDec22.pdf", dd="form Dec 2022 (PDF 2022-12-12)",
  mc="Y (paper form has no preselected box; online portal not public)", mq="Grants are sent with a letter that includes the name of your fund and:", mu="https://jcfny.org/wp-content/uploads/2021/02/GRDec22.pdf", md="PDF 2022-12-12",
  ea="address yes unless anonymous; email not stated", eq="The name(s) and address(es) of the Fundholder(s)/Authorized Parties signing this form", eu="https://jcfny.org/wp-content/uploads/2021/02/GRDec22.pdf", ed="PDF 2022-12-12",
  sd="Y (grantee may notify a named individual not on the fund)", sq="The grantee may notify an individual not on the fund (optional)", su="https://jcfny.org/wp-content/uploads/2021/02/GRDec22.pdf", sdd="PDF 2022-12-12",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="", repo="not covered", change="NEW"),
 "566047886": dict(sponsor="Foundation For The Carolinas", cat="full contact",
  detail="Each grant includes Gift Fund name and Fund Advisor name and address unless fund-wide anonymity elected; per-grant anonymity on request",
  dq="Unless you indicate below that you wish for all grants from the Gift Fund to be made anonymously, each grant from the Gift Fund will include the name of the Gift Fund, and the name and address of the Fund Advisor(s) recommending the grant so that the nonprofit may send an acknowledgement.", du="https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf", dd="PDF 2026-11-03",
  mc="N (named with address by default)", mq="If you do not select an option below, you may still request a grant be made anonymously at the time of the grant recommendation.", mu="https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf", md="PDF 2026-11-03",
  ea="address yes (default); email not stated", eq="the name and address of the Fund Advisor(s) recommending the grant", eu="https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf", ed="PDF 2026-11-03",
  sd="Y (address shared 'so that the nonprofit may send an acknowledgement')", sq="so that the nonprofit may send an acknowledgement", su="https://fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf", sdd="PDF 2026-11-03",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="", repo="nonprofit-side-panel-2026-cf-supplement.csv cf_fftc", change="confirms repo"),
 "431152398": dict(sponsor="Greater Kansas City Community Foundation", cat="fund name only (donor contact encouraged, donor-chosen)",
  detail="Check shows fund name unless anonymous; donor decides what else to share and is encouraged to add name and email on the check stub",
  dq="Our grant checks include the name of the fund that directed the grant, and we encourage the donor to share their name, email and other contact information on the check stub.", du="https://www.growyourgiving.org/nonprofits/knowledge-hub/", dd="live page, read 2026-11-19",
  mc="unknown (donor 'decides what information they want to share'; whether the portal preselects is not public)", mq="The donor submits a grant request to the Community Foundation and decides what information they want to share with your nonprofit.", mu="https://growyourgiving.org/fueling-nonprofit-success-the-role-of-donor-advised-funds", md="live page",
  ea="email typically, if donor shares", eq="the check stub will likely include the donor's name and contact information (typically an email address).", eu="https://www.growyourgiving.org/nonprofits/knowledge-hub/", ed="live page",
  sd="Y", sq="we encourage the donor to share their name, email and other contact information on the check stub", su="https://www.growyourgiving.org/nonprofits/knowledge-hub/", sdd="live page",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="'It's rare for donors to choose to grant anonymously'", repo="nonprofit-side-panel-2026-cf-supplement.csv cf_gkccf", change="refines: fund name is the stated default; contact is donor-chosen"),
 "200849590": dict(sponsor="Greater Horizons", cat="not determinable (no public text)",
  detail="greaterhorizons.org home, open-a-fund and privacy pages read; no grant-letter or recognition text; donor portal is login-only",
  dq="", du="https://www.greaterhorizons.org/open-a-donor-advised-fund/", dd="read 2026-11-19",
  mc="unknown", mq="", mu="", md="", ea="unknown", eq="", eu="", ed="", sd="unknown", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="allowed; content absent", label="absent", outcome="Affiliate of GKCCF; GKCCF practice not assumed to apply", repo="not covered", change="gap"),
 "042103559": dict(sponsor="Combined Jewish Philanthropies (CJP)", cat="donor chooses; no default stated",
  detail="Donor chooses per grant how much to share (DAF name, name, address, email); anonymous grants say only 'from a CJP DAF'; address inclusion needs a per-signatory consent box at setup",
  dq="You can choose how much information about yourself to share on each grant with the recipient charity. This can include the name of your DAF, your name, your address, and your email, each at your direction. You can also choose to be anonymous, in which case the charity is only informed that the grant came from a CJP DAF.", du="https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf", dd="PDF 2026-04-29",
  mc="Y? ('each at your direction'; address requires consent box at setup)", mq="CJP is allowed to include this signatory's address in grant letters to organizations", mu="https://ma.cjp.org/hubfs/DAF/DAF%20Forms%20(Adobe%20web%20form%20version)%20-%20Updated%2010-01-24%20MG.pdf", md="PDF 2024-09-12",
  ea="address and email at donor direction", eq="your name, your address, and your email, each at your direction", eu="https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf", ed="PDF 2026-04-29",
  sd="Y", sq="each at your direction", su="https://ma.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf", sdd="PDF 2026-04-29",
  api="none found", aq="", au="", ad="",
  access="allowed", label="F", outcome="", repo="not covered", change="NEW"),
 "593652538": dict(sponsor="Raymond James Charitable", cat="not determinable (blocked)",
  detail="raymondjamescharitable.org and raymondjames.com robots.txt return 403; not fetched. Search snippet of an RJ advisor article: letter recognises the recommender or donor may remain anonymous [R, not verified]",
  dq="", du="https://www.raymondjamescharitable.org/", dd="",
  mc="unknown", mq="", mu="", md="", ea="unknown", eq="", eu="", ed="", sd="unknown", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="robots.txt 403 at raymondjamescharitable.org, www.raymondjamescharitable.org, www.raymondjames.com (blocked)", label="blocked", outcome="", repo="direction-donor-feature-census.md (same block)", change="gap persists"),
 "260724604": dict(sponsor="Dechomai Asset Trust", cat="not determinable (no public text)",
  detail="dechomai.org FAQ and Policies & Procedures read; no grant-letter or donor-recognition text; model grants noncash proceeds largely to the originating charity",
  dq="We accept the donation of the non-cash asset, provide administrative services, then grant the net proceeds of the sale of the asset to the originating charity.", du="https://dechomai.org/faqs/", dd="live page, read 2026-11-19",
  mc="unknown", mq="", mu="", md="", ea="unknown", eq="", eu="", ed="", sd="unknown", sq="", su="", sdd="",
  api="none found", aq="", au="", ad="",
  access="allowed; content absent", label="absent", outcome="", repo="not covered", change="gap"),
}

BUCKET = lambda c: ("full contact" if c.startswith("full contact") else
                    "name only" if c.startswith("name only") else
                    "fund name only" if c.startswith("fund name only") else
                    "anonymous" if c.startswith("anonymous") else
                    "donor must choose / no default stated" if c.startswith(("donor", "set at")) else
                    "not determinable")


def top20(root):
    rows = csv.DictReader(open(os.path.join(root, "data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv")))
    sel = [r for r in rows if r["fiscal_year"] == "2024" and r["row_type"] == "top50"]
    return sorted(sel, key=lambda r: int(r["rank_assets"]))[:20]


COLS = ["rank_fy2024", "sponsor", "ein", "fy2024_daf_assets_usd", "share_of_top20_assets",
        "default_category", "default_bucket", "default_detail", "default_quote", "default_url", "default_source_date",
        "donor_must_choose", "must_choose_quote", "must_choose_url", "must_choose_source_date",
        "charity_gets_email_or_address", "email_address_quote", "email_address_url", "email_address_source_date",
        "donor_can_share_directly", "share_direct_quote", "share_direct_url", "share_direct_source_date",
        "api_data_sharing", "api_quote", "api_url", "api_source_date",
        "access_robots", "evidence_label", "observed_outcome_data", "repo_prior", "change_vs_repo", "retrieved"]


def row(lt, total):
    r = R[lt["ein"]]
    a = float(lt["daf_assets_eoy"])
    vals = [lt["rank_assets"], r["sponsor"], lt["ein"], str(int(a)), f"{a/total:.4f}",
            r["cat"], BUCKET(r["cat"]), r["detail"], r["dq"], r["du"], r["dd"],
            r["mc"], r["mq"], r["mu"], r["md"], r["ea"], r["eq"], r["eu"], r["ed"],
            r["sd"], r["sq"], r["su"], r["sdd"], r["api"], r["aq"], r["au"], r["ad"],
            r["access"], r["label"], r["outcome"], r["repo"], r["change"], RET]
    return dict(zip(COLS, vals))


def summary(rows):
    order = ["full contact", "name only", "fund name only", "anonymous", "donor must choose / no default stated", "not determinable"]
    agg = reduce(lambda acc, r: {**acc, r["default_bucket"]: (acc.get(r["default_bucket"], (0, 0.0, []))[0] + 1,
                                                             acc.get(r["default_bucket"], (0, 0.0, []))[1] + float(r["fy2024_daf_assets_usd"]),
                                                             acc.get(r["default_bucket"], (0, 0.0, []))[2] + [r["sponsor"]])}, rows, {})
    total = sum(float(r["fy2024_daf_assets_usd"]) for r in rows)
    det = total - agg.get("not determinable", (0, 0.0, []))[1]
    lines = ["| Default bucket | Sponsors (n) | FY2024 DAF assets ($bn) | Share of top-20 assets | Share of determinable assets | Sponsors |",
             "|---|---|---|---|---|---|"]
    body = [f"| {b} | {agg.get(b,(0,0,[]))[0]} | {agg.get(b,(0,0.0,[]))[1]/1e9:.2f} | {agg.get(b,(0,0.0,[]))[1]/total:.1%} | "
            + (f"{agg.get(b,(0,0.0,[]))[1]/det:.1%}" if b != "not determinable" else "n/a") + f" | {'; '.join(agg.get(b,(0,0,[]))[2])} |"
            for b in order]
    tail = [f"| **Total** | {len(rows)} | {total/1e9:.2f} | 100.0% | determinable = {det/1e9:.2f} ({det/total:.1%}) | |"]
    contact = sum(float(r["fy2024_daf_assets_usd"]) for r in rows if r["default_bucket"] == "full contact")
    withheld = sum(float(r["fy2024_daf_assets_usd"]) for r in rows if r["default_bucket"] in ("name only", "fund name only", "anonymous"))
    nfc = sum(1 for r in rows if r["default_bucket"] == "full contact")
    ndet = sum(1 for r in rows if r["default_bucket"] != "not determinable")
    extra = [f"", f"- Count basis: {nfc} of {ndet} determinable sponsors ({nfc/ndet:.0%}) default to full contact.",
             f"- Asset basis: full contact {contact/total:.1%} of top-20 assets; contact withheld by default (name only, fund name only or anonymous) {withheld/total:.1%}; {withheld/det:.1%} and {contact/det:.1%} of determinable assets."]
    return "\n".join(lines + body + tail + extra)


def main(root, out_csv, out_md):
    lt = top20(root)
    total = sum(float(r["daf_assets_eoy"]) for r in lt)
    rows = [row(r, total) for r in lt]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    open(out_md, "w").write(summary(rows) + "\n")
    print(summary(rows))


if __name__ == "__main__":
    main(*sys.argv[1:4])
