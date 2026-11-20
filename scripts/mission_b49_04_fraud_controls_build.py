"""Build data/mission-2026-11-14/fraud-diversion-controls-2026-11-20.csv and print the computed summary
used in research/mission-2026-11-14/b49-04-fraud-diversion-controls.md.

Usage: python3 -I scripts/mission_b49_04_fraud_controls_build.py . [--doj-hits FILE.jsonl ...]

Records are transcribed from first-party pages read on 2026-11-20 (robots checked; see the research note,
section 2). The FY2024 top-20 and asset figures are read from
data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv. Optional --doj-hits files are the
JSON-lines output of scripts/mission_b49_04_doj_scan.py; when given, the DOJ screen counts are recomputed.
Stdlib only; pure functions; no global mutable state.
"""
import csv, json, os, sys
from functools import reduce

RET = "2026-11-20"
OUT = "data/mission-2026-11-14/fraud-diversion-controls-2026-11-20.csv"
TOP20 = "data/mission-2026-11-14/donor-info-defaults-top20-2026-11-19.csv"

FIELDS = ["row_id", "record_type", "entity", "top20_rank", "entity_role", "risk_category", "audience",
          "control_or_finding", "stated", "key_quote", "figure_value", "figure_unit", "source_url",
          "source_date", "access_status", "evidence_label", "repo_link", "notes", "retrieved"]

FC = "https://www.fidelitycharitable.org"
SCAMS = FC + "/articles/security-tips-common-scams.html"
FC_SEC = FC + "/security.html"
FC_NPFAQ = FC + "/nonprofits/faqs.html"
VC_SEC = "https://www.vanguardcharitable.org/company-policies/security-center"
NPT22 = "https://www.nptrust.org/philanthropic-resources/philanthropist/how-npt-conducts-grantmaking-due-diligence-and-how-donors-can-avoid-charity-scams/"
NPT24 = "https://www.nptrust.org/?p=9117"
REN_CLAIM = "https://intercom.help/rengiving/en/articles/14285109-claiming-your-charity-step-by-step"
REN_ACH = "https://intercom.help/rengiving/en/articles/6232119-charity-ach-setup-step-by-step"
IC3_25 = "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf"
RL = "research/mission-2026-11-14/"
DL = "data/mission-2026-11-14/"


def rec(row_id, record_type, entity, top20_rank, entity_role, risk_category, audience, control_or_finding,
        stated, key_quote, source_url, source_date, access_status, evidence_label,
        figure_value="", figure_unit="", repo_link="", notes=""):
    """One CSV row as a dict (pure)."""
    return dict(row_id=row_id, record_type=record_type, entity=entity, top20_rank=top20_rank,
                entity_role=entity_role, risk_category=risk_category, audience=audience,
                control_or_finding=control_or_finding, stated=stated, key_quote=key_quote,
                figure_value=figure_value, figure_unit=figure_unit, source_url=source_url,
                source_date=source_date, access_status=access_status, evidence_label=evidence_label,
                repo_link=repo_link, notes=notes, retrieved=RET)


A = "allowed (robots 200; all listed agents allowed)"


def sponsor_rows():
    """Rows for the FY2024 top-20 sponsors (notices and controls)."""
    return [
        rec("FDC-01", "sponsor_notice", "Fidelity Charitable", "1", "sponsor", "payment_redirection_BEC", "donor",
            "donor-facing warning about messages asking for changed payment details; advises out-of-band confirmation", "Y",
            "Donors may receive messages that appear to come from known nonprofits, vendors, or advisors requesting updated payment details or directing funds to a new account. These messages are often associated with phishing attempts or business email compromise ... Avoid acting on unexpected payment detail changes communicated through a single channel. Instead, independently confirm requests using the known information of a contact at the organization",
            SCAMS, "live page (undated; (c)1998-2026)", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR07",
            notes="Same page as PR07; confirmed live on this pass"),
        rec("FDC-02", "sponsor_notice", "Fidelity Charitable", "1", "sponsor", "credential_sharing_third_party", "donor",
            "warns against giving DAF credentials to third-party payment processors or tools", "Y",
            "third-party payment processors or tools may request your financial or charitable giving account credentials when you are making a donation ... it can also increase the risk of unauthorized access, account compromise, or misuse of your credentials ... always access their account directly through the Fidelity Charitable website or an approved mobile application",
            SCAMS, "live page (undated)", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR08",
            notes="Names no processor"),
        rec("FDC-03", "sponsor_notice", "Fidelity Charitable", "1", "sponsor", "charity_impersonation", "donor",
            "warns of look-alike charities (AI-made sites and messages), social-media appeals and follow-up outreach after public giving", "Y",
            "Fraudulent appeals can sometimes resemble legitimate organizations in name, branding, or mission, as artificial intelligence and other modern technologies make it easier to create polished websites, emails, or messages.",
            SCAMS, "live page (undated)", A, "F"),
        rec("FDC-04", "sponsor_control", "Fidelity Charitable", "1", "sponsor", "account_takeover", "donor",
            "MFA at login; voice biometrics on phone service; review and verification of every grant and recipient; warns some transactions may get extra verification time", "Y",
            "Your Giving Account is protected by multi-factor authentication at login, strong encryption, and firewalls. ... Our teams use biometric technology to verify your voice over the phone ... Our team of dedicated experts review and verify every grant recommendation and recipient ... These evolving risks may require additional verification and processing time for certain transactions",
            FC_SEC, "live page (undated)", A, "F",
            notes="Page heading: 'Fraud is on the rise across the charitable sector'"),
        rec("FDC-05", "sponsor_control", "Fidelity Charitable", "1", "sponsor", "account_takeover", "donor",
            "step-up one-time code for named critical transactions (new bank instructions; contact-information changes); MFA at login and on new device or location", "Y",
            "The Second Factor Authentication (2FA) is an additional layer of security used by Fidelity Charitable to verify the user's online identity for critical transactions. While we continue to identify key transactions, setting up new bank instructions or modifying a user's contact information have been identified.",
            FC + "/help/security-codes.html ; " + FC + "/faqs/all/when-asked-to-complete-mfa.html", "live pages (undated)", A, "F",
            notes="Code by text or voice call; alternate number recommended. The older FAQ URL what-is-the-benefit-of-two-factor-authentication.html returns 404"),
        rec("FDC-06", "sponsor_control", "Fidelity Charitable", "1", "sponsor", "account_takeover", "advisor",
            "new MFA requirements for advisor portal (GivingCentral); expanded due diligence on qualifying grants and contributions that may lengthen processing", "Y",
            "New MFA requirements for logging in to GivingCentral have strengthened access controls ... Expanded due diligence for processing qualifying grants and contributions to ensure charitable assets are distributed without risk of fraud. In some cases, additional review may extend processing timelines.",
            FC + "/content/dam/fc-public/vessel/enhancements-to-the-advisor-experience.pdf", "PDF created 2026-10-06, modified 2026-10-07", A, "F",
            notes="'Qualifying' is not defined"),
        rec("FDC-07", "sponsor_control", "Fidelity Charitable", "1", "sponsor", "payment_redirection_BEC", "charity",
            "ACH enrolment and bank-detail updates: discretionary callback to the charity's publicly available number; enrolment needs a voided check OR a bank letter dated within 12 months", "partial",
            "we may call your organization's publicly available phone number to verify banking and/or contact information ... Enrollment requires you to provide your organization's Employer Identification Number (EIN), bank account number and routing number, a primary and secondary contact, and a voided check or bank letter dated within the last 12 months.",
            FC_NPFAQ, "live page (undated)", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR01-PR05; " + RL + "queue-batch37-controls-education.md wave-22 corrections",
            notes="NEW vs PR01: the FAQ now accepts a bank letter as an alternative to the voided check; PR01 quotes the form (PDF 2025-12-18) as requiring a voided check. Not reconciled"),
        rec("FDC-08", "sponsor_control", "Fidelity Charitable", "1", "sponsor", "check_theft_alteration", "charity",
            "grant-check control: a check is reissued only at the recommending donor's request; the sponsor can void a check at the charity's request", "Y",
            "Fidelity Charitable cannot reissue a grant check unless requested by the recommending donor. At the request of the receiving organization, we can void a grant check and notify the recommending donor",
            FC_NPFAQ, "live page (undated)", A, "F", repo_link=DL + "sponsor-grant-payment-policies.csv"),
        rec("FDC-09", "sponsor_notice", "Fidelity Charitable", "1", "sponsor", "check_theft_alteration", "charity",
            "promotes EFT over paper checks citing mail fraud; the statistic's source is not given", "Y",
            "With 1 in 5 organizations reporting mail fraud, EFT helps protect grants recommended by your donors",
            FC + "/nonprofits/eft.html", "live page (undated)", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR09",
            figure_value="0.2", figure_unit="share of organizations reporting mail fraud (sponsor claim, unsourced)"),
        rec("FDC-10", "sponsor_notice", "National Philanthropic Trust", "2", "sponsor", "charity_impersonation", "donor",
            "donor-facing scam-avoidance article (fake or look-alike charities; pressure for cash, gift cards or wires); says DAF grants are a safer channel", "Y",
            "Scam charities often have names that are close (but not quite exactly the same) as legitimate national charities. ... Donating via your donor-advised fund, or with a credit card or check is more secure.",
            NPT22, "2022-09-23", A, "F",
            notes="Also cites an FTC loss figure for 2021; not used here because ftc.gov was unreadable (see limits)"),
        rec("FDC-11", "sponsor_notice", "National Philanthropic Trust", "2", "sponsor", "charity_impersonation", "donor",
            "donor due-diligence article: fraudulent charities use names of established nonprofits; rely on EIN; avoid links", "Y",
            "Fraudulent charities will often falsely use the name of—or present themselves as—well-known or established nonprofit organizations. If giving online, always go directly to an organization's website rather than clicking through links. Be sure to rely on the organization's unique EIN or tax ID number.",
            NPT24, "2024-05-01", A, "F"),
        rec("FDC-12", "sponsor_control", "National Philanthropic Trust", "2", "sponsor", "account_takeover", "donor",
            "one-time verification code (text or voice) during online account opening in NPT GivingPoint", "Y",
            "Indicate your preference to receive a Verification Code either by text, or by phone via an automated voice call reading off your code.",
            "https://www.nptrust.org/wp-content/uploads/2021/01/How-to-Open-a-DAF-Account-Online-NPT.pdf", "PDF modified 2025-04-29", A, "F",
            notes="Registration-time code only; whether every login requires a second factor is not stated on pages read"),
        rec("FDC-13", "sponsor_control", "National Philanthropic Trust", "2", "sponsor", "payment_redirection_BEC", "charity",
            "charity-facing page explains checks and grant letters; no item on bank-change or redirection fraud (links a generic 'Tips To Avoid Fraud')", "N",
            "The letter accompanying the grant you receive should contain any information the donor has elected to share",
            "https://www.nptrust.org/for-nonprofits/", "live page", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR13",
            notes="Electronic grants go through PayPal Grant Payments (repo PR13)"),
        rec("FDC-14", "sponsor_notice", "DAFgiving360", "3", "sponsor", "all", "all",
            "not read", "blocked", "", "https://www.dafgiving360.org/", "", "blocked (robots.txt HTTP 403)", "B",
            repo_link=DL + "payment-redirection-controls-2026.csv PR23"),
        rec("FDC-15", "sponsor_notice", "Vanguard Charitable", "4", "sponsor", "grant_offer_scam", "both",
            "security center lists scams aimed at donors and at grantees (fake grants to individuals, deposit-and-forward checks, fee-for-grant, lotteries, gift-card or crypto requests, social-media solicitations)", "Y",
            "Numerous scams and fraudulent efforts are currently circulating on the internet, deliberately targeting both donors and grantees. ... Grants given to individuals on behalf of Vanguard Charitable. Requests to deposit a check, purchase a gift card, or virtual currency, and send some portion of the money elsewhere.",
            VC_SEC, "live page ((c) 2026)", A, "F", repo_link=DL + "payment-redirection-controls-2026.csv PR11",
            notes="No item on bank-change requests to charities (confirms PR11)"),
        rec("FDC-16", "sponsor_control", "Vanguard Charitable", "4", "sponsor", "account_takeover", "donor",
            "MFA required for all web-registered users; never asks for password, full SSN or MFA codes; confirmation letters or emails on account changes; account hold on suspected fraud; advises against linking accounts to donor-tracking apps", "Y",
            "MFA is now required for all web-registered Vanguard Charitable users. ... Vanguard Charitable will never ask for your password, full Social Security number, or MFA codes via email, phone, or text. ... Vanguard Charitable sends confirmation letters or emails when changes occur with your philanthropic account. ... Do not connect your philanthropic accounts to donor-tracking apps.",
            VC_SEC + " ; https://www.vanguardcharitable.org/faq/how-do-i-register-my-vanguard-charitable-account-online", "live pages", A, "F",
            repo_link=DL + "payment-redirection-controls-2026.csv PR12"),
        rec("FDC-17", "sponsor_notice", "Goldman Sachs Philanthropy Fund (GS DAF)", "5", "sponsor", "all", "all",
            "not read", "blocked", "", "https://gspf.goldman.com/", "", "blocked (robots.txt Disallow for * and all listed AI agents)", "B"),
        rec("FDC-18", "sponsor_notice", "Silicon Valley Community Foundation", "6", "sponsor", "all", "all",
            "no fraud, phishing or security notice found (homepage, 93 sitemap URLs, donor-portal-login page, nonprofit grant FAQ)", "absent",
            "", "https://www.svcf.org/sitemap.xml", "sitemap read 2026-11-20", A, "absent"),
        rec("FDC-19", "sponsor_notice", "Morgan Stanley GIFT", "7", "sponsor_parent", "payment_redirection_BEC", "donor",
            "parent-level (Morgan Stanley) cybersecurity page: impersonation, phishing, BEC; advises call-back verification of payment instructions and MFA; not GIFT-specific", "parent only",
            "Generally, payment instructions should be authenticated using a separate more secure channel. For example, in addition to email verification, details may be confirmed verbally by calling a trusted phone number (i.e., a call-back verification).",
            "https://www.morganstanley.com/about-us/cybersecurity-and-fraud-awareness", "live page", A, "F",
            notes="Advisor-branded 'Charity Fraud' articles on advisor.morganstanley.com could not be read (robots.txt unreachable)"),
        rec("FDC-20", "sponsor_control", "American Endowment Foundation", "8", "sponsor", "payment_redirection_BEC", "charity",
            "charity portal (powered by Ren): charities claim their organization and submit ACH that must be verified before electronic payment; until then grants go by check; check carries a QR code to the portal", "Y",
            "Until your organization's ACH information has been submitted and verified in the new portal, grant payments will arrive by check.",
            "https://www.aefonline.org/charities/", "live page (portal launch 'Q2 2026')", A, "F",
            repo_link=RL + "b4013-02-b4222-02-remittance-and-portal-features.md",
            notes="Same page still carries an older 'Share your ACH information ... Email Us' prompt; no fraud notice found in 211 sitemap URLs. Ren's verification steps: FDC-34, FDC-35"),
        rec("FDC-21", "sponsor_notice", "Renaissance Charitable Foundation", "9", "sponsor", "all", "all",
            "no fraud or security notice found on renaissancecharitable.org (homepage, 18 sitemap URLs, login page); charity-side controls are Ren's (FDC-34 to FDC-36)", "absent",
            "", "https://renaissancecharitable.org/sitemap_index.xml", "sitemap read 2026-11-20", A, "absent"),
        rec("FDC-22", "sponsor_notice", "National Christian Foundation", "10", "sponsor", "all", "all",
            "not fetched: site terms ban automated extraction (shared rules); owner to read manually", "not read",
            "", "https://www.ncfgiving.com/", "", "not fetched (site terms)", "B"),
        rec("FDC-23", "sponsor_notice", "Bank of America Charitable Gift Fund", "11", "sponsor_parent", "credential_sharing_third_party; payment_redirection_BEC", "donor",
            "parent private-bank article warns that charity-site widgets may solicit DAF login credentials, and that donations can be intercepted by 'changed account' messages", "parent only",
            "Charities may add widgets or apps to the fundraising sections of their websites that solicit your login credentials to your donor-advised fund (DAF) and other giving accounts. Those should be avoided at all costs. ... You may get a message like \"We've changed our account. Please send your donations here.\"",
            "https://www.privatebank.bankofamerica.com/articles/online-charity-scams.html", "article cites IRS release of 2025-02-27; page code expires 2026-11-28", A, "F",
            notes="Same text on https://www.ml.com/articles/online-charity-scams.html (Merrill). Not a BofA CGF program document"),
        rec("FDC-24", "sponsor_control", "The Chicago Community Trust", "12", "sponsor", "account_takeover", "donor",
            "withdrawn 2026-11-20: donorportal.cct.org robots.txt evidently disallows all paths except /index.html, so the portal guide is off-limits; www.cct.org returned HTTP 403", "not read",
            "", "https://www.cct.org/", "", "not read (robots)", "B",
            notes="Earlier draft cited the donor-portal guide; withdrawn on robots grounds per shared rules"),
        rec("FDC-25", "sponsor_notice", "ImpactAssets", "13", "sponsor", "all", "all",
            "no fraud or security notice found (homepage; 369 sitemap URLs incl. FAQ sitemap)", "absent",
            "", "https://impactassets.org/sitemap_index.xml", "sitemap read 2026-11-20", A, "absent"),
        rec("FDC-26", "sponsor_notice", "Jewish Communal Fund", "14", "sponsor", "all", "all",
            "no DAF fraud notice found (397 sitemap URLs; FAQ). Wire grants are followed by an email to the charity contact with grant details", "absent",
            "We are so pleased that you have received a wire from the Jewish Communal Fund. The contact person you provided will receive an email with details about the contributor and purpose of the grant.",
            "https://jcfny.org/faqs/", "live page", A, "absent",
            notes="Security pages in the sitemap concern physical security grants to Jewish organizations"),
        rec("FDC-27", "sponsor_notice", "Foundation For The Carolinas", "15", "sponsor", "all", "all",
            "no fraud or security notice found (homepage; 54 sitemap URLs)", "absent", "", "https://fftc.org/sitemap.xml", "sitemap read 2026-11-20", A, "absent"),
        rec("FDC-28", "sponsor_control", "Greater Kansas City Community Foundation", "16", "sponsor", "account_takeover", "donor",
            "donor portal MFA is optional after first login; privacy policy asks donors to report compromised accounts", "optional",
            "Choose your new password and log in. Once logged in, you have the option to set up multi-factor authentication for additional security.",
            "https://www.growyourgiving.org/access-fund-online/ ; https://www.growyourgiving.org/privacy-policy/", "live pages", A, "F"),
        rec("FDC-29", "sponsor_control", "Greater Horizons", "17", "sponsor", "account_takeover", "donor",
            "donor portal MFA is optional (same wording as GKCCF)", "optional",
            "Choose your new password and log in. Once logged in, you have the option to set up multi-factor authentication for additional security.",
            "https://www.greaterhorizons.org/access-fund-online/", "live page", A, "F"),
        rec("FDC-30", "sponsor_notice", "Combined Jewish Philanthropies (CJP)", "18", "sponsor", "all", "all",
            "no DAF fraud notice found (372 sitemap URLs); security pages concern communal physical security and nonprofit cybersecurity training", "absent",
            "", "https://www.cjp.org/sitemap.xml", "sitemap read 2026-11-20", A, "absent"),
        rec("FDC-31", "sponsor_notice", "Raymond James Charitable", "19", "sponsor", "all", "all",
            "not read", "blocked", "", "https://www.raymondjamescharitable.org/", "", "blocked (robots.txt unreachable: connection failed)", "B"),
        rec("FDC-32", "sponsor_notice", "Dechomai Asset Trust", "20", "sponsor", "all", "all",
            "no fraud or security notice found (homepage; 72 sitemap URLs)", "absent", "", "https://dechomai.org/sitemap.xml", "sitemap read 2026-11-20", A, "absent"),
    ]


def rail_rows():
    """Payment rails, vendors and a peer benchmark."""
    return [
        rec("FDC-33", "vendor_notice", "Chariot", "", "payment_rail_vendor", "payment_redirection_BEC", "charity",
            "vendor article names three DAF-grant diversion patterns at the level of public reporting: impersonating a charity to a DAF provider to change contact or address details; enrolling a charity in a digital payment system with falsified bank documents; mail theft and check alteration", "Y",
            "Scammers are finding new ways to target nonprofits through Donor-Advised Fund (DAF) giving. ... They don't require a breach of your internal systems. Instead, they rely on manipulation and exploitation of weak points in third party systems that you rely on for funding.",
            "https://www.givechariot.com/post/behind-the-scenes-risks-how-daf-giving-is-being-exploited-and-what-you-can-do-about-it", "live page (undated)", A, "F",
            repo_link=DL + "payment-redirection-controls-2026.csv PR16-PR19",
            notes="Commercial interest: Chariot sells the receiving-account product it recommends. No incident counts or named sponsors"),
        rec("FDC-34", "rail_control", "Ren for Charities", "", "payment_rail_vendor", "payment_redirection_BEC", "charity",
            "charity claim requires one of three verifications: postcard to the IRS-filed address, automated call to the phone number on the latest e-filed Form 990, or officer identity check through Stripe with government photo ID", "Y",
            "Address Verification: A postcard with instructions will be mailed to your charity's IRS address. Telephone Verification: A phone call with an authorization code will be sent to the phone number on your organization's 990 form ... Officer Identity Verification: A proven officer of the organization can verify their identity",
            REN_CLAIM, "live help article", A, "F",
            notes="Ren platforms serve RCF, AEF (FDC-20) and Ren-hosted programs such as MS GIFT and BofA CGF (repo: grant-remittance-2026-11-19.csv)"),
        rec("FDC-35", "rail_control", "Ren for Charities", "", "payment_rail_vendor", "payment_redirection_BEC", "charity",
            "bank link by Plaid or manual review; rejected if ownership cannot be verified; bank statement upload when pending; email notice of status", "Y",
            "If we are unable to verify that the bank account belongs to your organization based on our very rigorous review requirements, we have to reject the ACH connection. ... Our verification process is very strict to avoid fraudulent connections.",
            REN_ACH, "live help article", A, "F",
            notes="No callback or cooling-off period stated for later bank changes"),
        rec("FDC-36", "rail_control", "Ren for Charities", "", "payment_rail_vendor", "check_theft_alteration", "charity",
            "grant tracking in the charity portal: ACH delivery confirmation; USPS scan events for checks", "Y",
            "For check distributions, tracking details will include USPS scanning events",
            "https://intercom.help/rengiving/en/articles/9970231-where-is-our-grant", "live help article", A, "F"),
        rec("FDC-37", "peer_benchmark", "Greater Houston Community Foundation", "", "sponsor (outside top 20)", "phishing_impersonation", "donor",
            "explicit donor guidance: verify transfer and grant instructions through a known phone number, not email replies; enable MFA; never share portal credentials with external tools", "Y",
            "For your safety, only log in through our website and never share your DonorSphere credentials with external websites or unfamiliar tools.",
            "https://ghcf.org/articles/how-to-avoid-impersonation-fraud-donor-security-tips/", "live article (2026, per search listing)", A, "F",
            notes="Shown as a benchmark of what a sponsor notice can cover; not in the FY2024 top 20"),
    ]


def regulator_rows(doj):
    """Enforcement, regulator and federal-report rows. doj is the computed DOJ screen summary."""
    return [
        rec("FDC-38", "federal_report", "FBI IC3", "", "regulator", "charity_fraud", "public",
            "PSA on charity fraud after mass-casualty events and disasters; 2024 complaint count and losses for fraudulent charities, crowdfunding and disaster relief", "Y",
            "In 2024, the FBI Internet Crime Complaint Center (IC3) received more than 4,500 complaints reporting approximately $96 million in losses to fraudulent charities, crowdfunding accounts, and disaster relief campaigns.",
            "https://www.ic3.gov/PSA/2025/PSA250116", "2025-01-16 (Alert I-011625-PSA)", A, "F",
            figure_value="4500; 96000000", figure_unit="complaints (more than); USD losses (approx.), 2024",
            notes="Broader than the annual report's 'Charity' crime type; does not mention DAFs"),
        rec("FDC-39", "federal_report", "FBI IC3", "", "regulator", "charity_fraud", "public",
            "2025 annual report adds 'Charity' as a crime type: 662 complaints and $7,907,609 losses; 2024 and 2023 marked '*' (not captured)", "Y",
            "Charity: Using deception to get money from individuals believing they are making donations to legitimate charities and/or charities representing victims of natural disasters shortly after the incident occurs.",
            IC3_25, "2025 Internet Crime Report", A, "F", figure_value="662; 7907609", figure_unit="complaints; USD losses, 2025",
            notes="'* Crime Type or Descriptor was not captured in these years.' The 2021-2024 reports' text has no 'Charity' crime type (pdftotext search)"),
        rec("FDC-40", "federal_report", "FBI IC3", "", "regulator", "charity_fraud", "public",
            "2025 report, complainants aged 60+: Charity 126 complaints, $3,474,668 losses", "Y",
            "Crime Types Reported by 60+", IC3_25, "2025 Internet Crime Report", A, "F",
            figure_value="126; 3474668", figure_unit="complaints; USD losses, age 60+, 2025"),
        rec("FDC-41", "federal_report", "FBI IC3", "", "regulator", "payment_redirection_BEC", "public",
            "context: BEC complaints and losses (all sectors), 2023-2025", "Y",
            "BEC 24,768 / 21,442 / 21,489 complaints; $3,046,598,558 / $2,770,151,146 / $2,946,830,270 losses (2025 / 2024 / 2023)",
            IC3_25, "2025 Internet Crime Report", A, "F", figure_value="24768; 3046598558", figure_unit="complaints; USD losses, 2025",
            notes="Not charity-specific; the category that covers bank-detail-change fraud"),
        rec("FDC-42", "federal_report", "FinCEN (with USPIS)", "", "regulator", "check_theft_alteration", "financial_institutions",
            "Financial Trend Analysis of mail-theft check fraud: 15,417 BSA reports from 841 institutions, more than $688m, in the six months after the Feb-2023 alert; 44% altered and deposited, 26% used as counterfeit templates, 20% fraudulently signed", "Y",
            "During the review period, FinCEN received 15,417 BSA reports from 841 financial institutions on mail theft-related check fraud, amounting to more than $688 million in reported suspicious activity.",
            "https://www.fincen.gov/news/news-releases/fincen-issues-depth-analysis-check-fraud-related-mail-theft", "2024-09-09", A, "F",
            figure_value="15417; 688000000", figure_unit="BSA reports; USD reported suspicious activity (2023-02-27 to 2023-08-31)",
            notes="Not charity-specific. The alert PDF and FTA PDF returned HTTP 404 to the generic client; the release page was read"),
        rec("FDC-43", "enforcement_or_regulator", "Hawaii Department of the Attorney General", "", "state_regulator", "overpayment_refund", "charity",
            "warning to nonprofits: counterfeit donation checks followed by partial-refund requests; verify donors and donations", "Y",
            "Fraudulent donors are reportedly sending counterfeit checks and later requesting a portion of the funds be refunded, before the nonprofit discovers that the check is fake.",
            "https://ag.hawaii.gov/wp-content/uploads/2025/08/News-Release-2025-81.pdf", "2025-08-19 (News Release 2025-81)", A, "F",
            notes="Not DAF-specific. Vanguard Charitable lists the same pattern among scams using its name (FDC-15). Names used by the scammers are not stored"),
        rec("FDC-44", "enforcement_or_regulator", "Nebraska Attorney General", "", "state_regulator", "overpayment_refund", "charity",
            "warning to nonprofits: large fraudulent first-time donor checks with refund requests; card-refund variant; verify refund requests directly", "Y",
            "These scammers, posing as wealthy, interested, first-time donors, are sending large fraudulent checks, often five figures or more. They then request a partial refund from the charity, claiming a mistake.",
            "https://ago.nebraska.gov/node/2215", "2024-06-25", A, "F", notes="Not DAF-specific"),
        rec("FDC-45", "enforcement_or_regulator", "U.S. Dept of Commerce OIG", "", "federal_regulator", "payment_redirection_BEC", "grant_makers",
            "benchmark controls for bank-change requests: independent verification with a known contact; dual approval; sender inspection", "Y",
            "Independently verify every request to change banking or payment information by calling/videoconferencing a known contact",
            "https://www.oig.doc.gov/wp-content/OIGPublications/DOC-OIG-Fraud-Alert-July-2026-Approved.pdf", "PDF created 2026-07-27", "allowed (robots.txt 404 = no restriction)", "F",
            repo_link=DL + "payment-redirection-controls-2026.csv PR24", notes="Re-read on this pass; used as the scoring benchmark, as in batch 37C"),
        rec("FDC-46", "enforcement_or_regulator", "U.S. DOJ press releases (all components)", "", "federal_prosecutor", "all", "public",
            "systematic screen of DOJ press releases 2021-01-01 to 2026-11-20 for DAF and top-sponsor terms", doj["stated"],
            doj["quote"], "https://www.justice.gov/api/v1/press_releases.json", "API read 2026-11-20", "allowed (robots 200; public API; HTML pages return a bot interstitial, not bypassed)", "C",
            figure_value=doj["value"], figure_unit=doj["unit"], notes=doj["notes"]),
        rec("FDC-47", "enforcement_or_regulator", "Georgia SDG Impact Fund matter", "", "state_regulator", "internal_misappropriation", "donor",
            "repo record: state action alleging a DAF-style sponsor misappropriated donor funds (see LIT-04)", "repo",
            "", DL + "daf-litigation-2021plus.csv", "see repo row", "repo", "R", repo_link=DL + "daf-litigation-2021plus.csv LIT-04",
            notes="Not re-read on this pass; carried for completeness"),
        rec("FDC-48", "enforcement_or_regulator", "SEC litigation releases", "", "federal_regulator", "all", "public",
            "not searched: sec.gov is excluded by the shared rules", "not read", "", "https://www.sec.gov/", "", "excluded by rule", "B"),
        rec("FDC-49", "enforcement_or_regulator", "CourtListener", "", "court_records", "all", "public",
            "not searched", "blocked", "", "https://www.courtlistener.com/robots.txt", "", "blocked (robots.txt HTTP 403)", "B"),
        rec("FDC-50", "federal_report", "FTC (Consumer Sentinel, consumer alerts)", "", "regulator", "charity_fraud", "public",
            "not read: ftc.gov and consumer.ftc.gov returned HTTP 404 for robots.txt and every page tried (including the 2024 Data Book PDF)", "not read",
            "", "https://www.ftc.gov/", "", "unreadable (HTTP 404 to generic client; not bypassed)", "B"),
        rec("FDC-51", "enforcement_or_regulator", "Florida Attorney General", "", "state_regulator", "charity_fraud", "charity",
            "release found by search ('Nearly Half a Million Dollars Secured for Nonprofits Following Charity Scam') not read", "blocked",
            "", "https://www.myfloridalegal.com/newsrelease/nearly-half-million-dollars-secured-nonprofits-following-charity-scam", "", "blocked (robots.txt HTTP 403)", "B"),
    ]


def repo_rows():
    """Links to earlier repo work."""
    return [
        rec("FDC-52", "repo_link", "State breach registers (MA, VT)", "", "repo", "account_takeover", "donor",
            "no breach-register entry 2021-2026 names a charitable or DAF entity; all DAF-adjacent notices are filed by parents or vendors", "repo",
            "No register entry names a charitable or DAF entity.", RL + "b39n1-03-b39n2-02-lobbying-and-breaches.md", "2026-11-20", "repo", "R",
            repo_link=DL + "breach-notices-daf-parents-2026-11-20.csv; " + DL + "daf-security-incidents-2021plus.csv"),
        rec("FDC-53", "repo_link", "Form 990 fraud-loss lines (1,512-sponsor universe)", "", "repo", "payment_redirection_BEC", "sponsor",
            "three of seven Part VI line-5 disclosures are payment redirection or BEC; one DAF processor (Givinga) booked a $316,184 'external bank fraud loss' in CY2024", "repo",
            "", DL + "sponsor-fraud-loss-disclosures.csv", "FY2022-FY2025 returns", "repo", "R",
            figure_value="316184", figure_unit="USD (Givinga CY2024)", repo_link=RL + "queue-batch37-controls-education.md section 1"),
        rec("FDC-54", "repo_link", "Grant remittance (top-10 sponsors)", "", "repo", "payment_redirection_BEC", "charity",
            "every documented electronic route sends grant detail out-of-band (email report, portal or letter); no sponsor documents a grant ID in ACH addenda", "repo",
            "", DL + "grant-remittance-2026-11-19.csv", "2026-11-19", "repo", "R",
            repo_link=RL + "b4013-02-b4222-02-remittance-and-portal-features.md"),
    ]


def read_top20(root):
    with open(os.path.join(root, TOP20), newline="") as f:
        return [dict(rank=r["rank_fy2024"], sponsor=r["sponsor"], assets=float(r["fy2024_daf_assets_usd"])) for r in csv.DictReader(f)]


def load_hits(paths):
    """Deduplicated DOJ hits (by URL) from JSON-lines files."""
    rows = [json.loads(l) for p in paths for l in open(p) if l.strip()]
    return list({r["url"]: r for r in rows}.values())


# Judgement made by reading each screen hit (research note section 3.2). Keys are release URLs.
J = "https://www.justice.gov/"
JUDGED = {
    J + "archives/opa/pr/dar-al-farooq-mosque-bomber-sentenced-53-years-prison": "false_positive",
    J + "usao-mn/pr/dar-al-farooq-mosque-bomber-sentenced-53-years-prison": "false_positive",
    J + "usao-mn/pr/two-illinois-men-sentenced-prison-their-roles-bombing-dar-al-farooq-islamic-center": "false_positive",
    J + "archives/opa/pr/two-illinois-men-sentenced-prison-their-roles-bombing-dar-al-farooq-islamic-center-and": "false_positive",
    J + "usao-sdil/pr/transportation-company-agrees-settle-allegations-impersonating-military-members-obtain": "false_positive",
    J + "usao-wdmi/pr/2021_0128_PSN": "incidental_mention",
    J + "Usao-wdmi/pr/2021_1209_PSN": "incidental_mention",
    J + "usao-ak/pr/s-lane-tucker-appointed-us-attorney-district-alaska": "incidental_mention",
    J + "usao-ak/pr/s-lane-tucker-confirmed-us-attorney-district-alaska": "incidental_mention",
    J + "usao-mt/pr/kurt-alme-serve-interim-us-attorney-district-montana": "incidental_mention",
    J + "usao-sdny/pr/idaho-it-professional-charged-misappropriating-pre-publication-investment": "daf_mentioned_not_diversion",
    J + "usao-ndtx/pr/stamford-mayor-indicted-diverting-more-300000-community-and-estate-funds": "community_foundation_accounts_diverted_alleged",
}
# Recorded output of scripts/mission_b49_04_doj_scan.py run 2026-11-20 (2,362 API pages of 50, newest first, to 2021-01-01).
DOJ_RECORDED = dict(pages=2362, scanned=118050, hit_urls=12)


def doj_summary(hits):
    """Summarise the DOJ screen from hit records (or the recorded run when hits is None)."""
    urls = [h["url"] for h in hits] if hits is not None else list(JUDGED)
    cats = [JUDGED.get(u, "unjudged") for u in urls]
    count = lambda c: sum(1 for x in cats if x == c)
    diversion = count("daf_diversion")
    return dict(stated="Y" if diversion else "N",
                quote="0 releases describe diversion or misuse of a DAF grant or DAF account. Adjacent: " +
                      J + "usao-ndtx/pr/stamford-mayor-indicted-diverting-more-300000-community-and-estate-funds (2026-08-14; indictment alleges a trustee with account access moved about $133,000 from a community foundation's accounts; DAF status not stated)",
                value=f"{DOJ_RECORDED['scanned']}; {len(urls)}; {count('false_positive')}; {count('incidental_mention')}; {count('daf_mentioned_not_diversion')}; {count('community_foundation_accounts_diverted_alleged')}; {diversion}; {count('unjudged')}",
                unit="releases dated 2021-01-01 to 2026-11-20 screened (sum over API pages); hit URLs; false positives (DAF = other acronym); incidental mentions (biographies, grant notices); DAF mentioned but no diversion; community-foundation accounts allegedly diverted; DAF grant or account diversion; unjudged",
                notes="Terms: donor advised, DAF(s), charitable gift fund, eight sponsor names, community foundation. The 12 hit URLs are 10 distinct releases (two OPA/USAO duplicates). Defendants are not named here")


def coverage(top20, rows, predicate):
    """Asset share of the top 20 for sponsors with at least one row satisfying predicate."""
    ranks = {r["top20_rank"] for r in rows if r["top20_rank"] and predicate(r)}
    hit = [t for t in top20 if t["rank"] in ranks]
    total = reduce(lambda a, t: a + t["assets"], top20, 0.0)
    return len(hit), reduce(lambda a, t: a + t["assets"], hit, 0.0) / total, [t["sponsor"] for t in hit]


def main(argv):
    root = argv[1] if len(argv) > 1 else "."
    hit_files = argv[argv.index("--doj-hits") + 1:] if "--doj-hits" in argv else None
    hits = load_hits(hit_files) if hit_files else None
    rows = sponsor_rows() + rail_rows() + regulator_rows(doj_summary(hits)) + repo_rows()
    with open(os.path.join(root, OUT), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    top20 = read_top20(root)
    sp = [r for r in rows if r["top20_rank"]]
    tests = [
        ("own donor-facing fraud/scam notice (sponsor's own site)", lambda r: r["record_type"] == "sponsor_notice" and r["stated"] == "Y"),
        ("any donor-facing notice incl. parent-only pages", lambda r: r["record_type"] == "sponsor_notice" and r["stated"] in ("Y", "parent only")),
        ("published login MFA or one-time code (required or prompted)", lambda r: r["record_type"] == "sponsor_control" and r["risk_category"] == "account_takeover" and r["stated"] == "Y"),
        ("published MFA that is only optional", lambda r: r["risk_category"] == "account_takeover" and r["stated"] == "optional"),
        ("notice names payment redirection / BEC (own or parent)", lambda r: "payment_redirection_BEC" in r["risk_category"] and r["record_type"] == "sponsor_notice" and r["stated"] in ("Y", "parent only")),
        ("charity-facing bank-change verification published", lambda r: r["record_type"] == "sponsor_control" and r["risk_category"] == "payment_redirection_BEC" and r["audience"] == "charity" and r["stated"] in ("Y", "partial")),
        ("blocked or not read", lambda r: r["stated"] in ("blocked", "not read")),
        ("searched, nothing found", lambda r: r["stated"] == "absent"),
    ]
    print(f"rows: {len(rows)}; top-20 sponsor rows: {len(sp)}")
    for label, pred in tests:
        n, share, names = coverage(top20, sp, pred)
        print(f"{label}: {n} sponsors, {share:.1%} of FY2024 top-20 DAF assets: {'; '.join(names)}")
    # [I] sensitivity: sponsors whose charity payments run on Ren for Charities per grant-remittance-2026-11-19.csv
    # (RA-08 MS GIFT, RA-09 AEF, RA-10 RCF) inherit the published Ren claim and bank-link checks (FDC-34, FDC-35).
    ren = {"7", "8", "9"}
    pub = {r["top20_rank"] for r in sp if r["record_type"] == "sponsor_control" and "payment_redirection_BEC" in r["risk_category"]
           and r["audience"] == "charity" and r["stated"] in ("Y", "partial")} | ren
    total = reduce(lambda a, t: a + t["assets"], top20, 0.0)
    share = reduce(lambda a, t: a + t["assets"], [t for t in top20 if t["rank"] in pub], 0.0) / total
    print(f"charity-side bank verification published by sponsor or its Ren rail [I]: {len(pub)} sponsors, {share:.1%}: "
          + "; ".join(t["sponsor"] for t in top20 if t["rank"] in pub))
    payee_custody = {"2", "4"}  # NPT and Vanguard pay through PayPal Grant Payments (repo PR10, PR13)
    share_pp = reduce(lambda a, t: a + t["assets"], [t for t in top20 if t["rank"] in payee_custody], 0.0) / total
    print(f"bank details held by PayPal, not the sponsor (repo PR10, PR13): {share_pp:.1%}")
    s = doj_summary(hits)
    print("DOJ screen:", s["value"], "|", s["unit"])


if __name__ == "__main__":
    main(sys.argv)
