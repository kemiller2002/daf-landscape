# Bank programs and third-party EFT providers: P-QCAL-04 and P-STF-05

**Date:** 2026-11-14. **Author:** bank-programs agent.
**Queue items:** P-QCAL-04 (bank-program and NCF terms) and P-STF-05 (third-party EFT providers). Full text is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).
**Builds on:**
- [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md)
- [queue-state-filings-transfer-terms.md](queue-state-filings-transfer-terms.md)
- [queue-payment-rails-cluster.md](queue-payment-rails-cluster.md)
- [../goldman-sachs-two-daf-programs-2026-11-11.md](../goldman-sachs-two-daf-programs-2026-11-11.md)
- [../bofa-morgan-stanley-institutional-ren-evidence-2026-11-11.md](../bofa-morgan-stanley-institutional-ren-evidence-2026-11-11.md)

**Outputs:**
- [`bank-program-terms-2026.csv`](../../data/mission-2026-11-14/bank-program-terms-2026.csv): 64 rows
- [`sponsor-eft-providers-2026.csv`](../../data/mission-2026-11-14/sponsor-eft-providers-2026.csv): 22 rows
- [`queue-proposals-bank-programs.csv`](../../data/mission-2026-11-14/queue-proposals-bank-programs.csv): 5 proposals

**Method and limits.**
- **No outreach.** Nothing was submitted, requested or logged into. No accounts were created, and no forms were filled in, including NCF's EFT interest form.
- **Sources used:** public pages, publicly linked PDFs, public portal login pages, and IRS e-file XML. The XML came from the GivingTuesday mirror, located through the IRS TEOS index as in `scripts/mission_990_contractors.py`.
- **Encoded PDFs.** Two PDFs use font encodings that `pdftotext` cannot read: the MS GIFT Donor Circular and BofA's "Making the Most" sheet. I rendered their pages to images and read them, so quotes from them are transcriptions.
- **Access failures:**
  - dafgiving360.org, ghcf.org and jcfny.org/faqs returned 403 to curl. GHCF was read through the fetch tool. DAFgiving360 and JCF could not be read.
  - reninc.com/payments returned 403 to curl and was read through the fetch tool.
  - Ren's "How to Sign Up for ACH" PDF returns 404.
  - BofA `Program_Guidelines_2025.pdf` and `Program_Guidelines_2026.pdf` return 404.
- **Labels:**
  - **[F]** fetched first-party text, quoted.
  - **[X]** IRS e-file XML.
  - **[V]** vendor or sponsor marketing claim (capped at 2 under methodology §3).
  - **[I]** my inference.

---

## 1. Answers at a glance

| Item | Answer |
|---|---|
| **P-QCAL-04: are public terms available for the bank programs?** | **Yes for three of five, more than earlier repo work found.**<br>- **MS GIFT's Donor Circular (Aug 2024) is public.** It is linked from the MS GIFT DFX portal home page ([portal](https://msgift.donorfirstx.com/)) [F]. Earlier repo work recorded it as "not public".<br>- **BofA:** the CGF guidelines (v3.2024) plus two portal guides from 2024 and 2025 are public.<br>- **NCF:** its live Guide to giving is public.<br>- **Goldman Sachs Philanthropy Fund (PWM):** the only public program document is a Program Circular **last revised August 2008** ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) [F].<br>- **GS Gives:** no public terms. |
| **Ren DFX/iPhi features visible** | - **BofA CGF and MS GIFT run on Ren DonorFirst/DFX portals.** The evidence is the hosts, a `dfx.css` stylesheet, Ren mailboxes and Ren Terms of Service ([BofA portal](https://bofa.donorfirst.org/); [MS portal](https://msgift.donorfirstx.com/)) [F].<br>- **The GS PWM donor web runs on Ren iPhi.** Its footer reads "iPhi™ ::: Copyright © 2001 - 2026 Stellar Technology Solutions, LLC" ([GS donor web](https://gspf.goldman.com/gspf/)) [F].<br>- **GS Gives pays Stellar** $172,604 for IT in FY2025 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml)) [X].<br>- **NCF's donor login is Salesforce/Skuid**, with no Ren marker ([login](https://secure.ncfgiving.com/grant)) [F]. |
| **Grant payment rails** | - **BofA:** check only.<br>- **GS PF:** check, per the 2008 circular; the 2026 rail is unknown.<br>- **MS GIFT:** "validated mailing address or banking details", plus a claim of ACH "rapid disbursement" [V].<br>- **NCF:** electronic first, through its in-house "NCF eGrants". |
| **Transfer-out** | - **NCF:** standard Giving Funds may grant to other DAF sponsors; succession funds may not.<br>- **BofA:** a donor may "grant the remaining assets to another donor-advised fund", but the clause covers only a termination of advisory rights.<br>- **MS GIFT and GS PF:** no outbound clause. |
| **Data export** | - **BofA:** the 2025 portal guide shows "export to Excel" on the **contribution** listing ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) [F].<br>- **The others:** they describe viewing or statements only.<br>- **No sponsor grants a contractual export or portability right.** |
| **Adviser data feeds** | - **BofA:** CGF balances, top charities and recent grants appear inside MyMerrill, Private Bank Account Access and BofA Online (single sign-on into the portal).<br>- **MS GIFT:** Financial Advisors may submit grants "upon ... verbal direction".<br>- **No sponsor documents an API or file feed.** |
| **P-STF-05: who uses a third-party EFT provider in 2026?** | - **PayPal Grant Payments:** NPT (up to $250,000) and Vanguard (whose policies say "third-party electronic fund transfer provider" and whose nonprofit page names PayPal).<br>- **Chariot Disbursements:** Daffy, Charityvest (from Aug 2026, replacing PayPal), TIFIN Give/AssetMark, Endaoment and seven community foundations. All are on Chariot's own list [V].<br>- **Stripe:** Fidelity uses Stripe plus its own ACH.<br>- **Own or administrator ACH:**<br>&nbsp;&nbsp;- AEF uses the Ren portal and ACH.<br>&nbsp;&nbsp;- NCF uses its own eGrants.<br>&nbsp;&nbsp;- GHCF, Oregon CF and CF Greater New Haven run their own ACH.<br>&nbsp;&nbsp;- MS GIFT claims ACH; the provider is not named.<br>- **Check only:** BofA CGF, DAFgiving360 (as documented) and GS PF (2008).<br>- **Not found:** SVCF, Chicago CT, JCF (NY), GS Gives. |

---

## 2. Goldman Sachs Philanthropy Fund (PWM; EIN 31-1774905)

**Which document governs.**
- **The only public Program Circular is dated 2008.** It ends "Last Revised: August 2008" and is served from the GS DAF donor-web domain ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) [F].
- **The 2008 name is the same entity.** The CY2022 return for the same EIN carries the name "GOLDMAN SACHS PHILANTHROPY FUND" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202312859349302266_public.xml)) [X]. The CY2024 return uses "GS DONOR ADVISED PHILANTHROPY FUND FOR WEALTH MANAGEMENT INC" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml)) [X].
- **The address is unchanged.** The circular's P.O. Box 15203, Albany is still the mailing address on the live contact page ([contact](https://gspf.goldman.com/gspf/ContactUs/tabid/112/Default.aspx)) [F].
- **The live login page binds users to an undated circular:** "you acknowledge that you have read GS DAF's Program Circular" ([donor web](https://gspf.goldman.com/gspf/)) [F]. Which version applies is not stated.

**Terms in the 2008 circular** ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) [F]:
- **Rail.** Approved grants are paid "in the form of a check", with "An accompanying letter" naming the donor unless anonymous.
- **Grant size and timing.** The minimum is $250, in $50 increments. Grants are reviewed each business day and are "typically within a two week time frame".
- **Data access.** The donor web lets donors view "transaction (grant, contribution, fees, etc.) histories as well as current, real-time statuses of pending transactions" and set recurring grants. Quarterly statements are sent. There is **no download or export clause**.
- **Closing.** A full-balance grant is allowed: "Grants of the entire balance of your account will be subject to a pro-rated administrative fee." **No clause names other DAF sponsors.**
- **Minimum activity.** GS PF "reserves the right to transfer up to 5% of assets" from an under-granting account to the Directors' Philanthropy Fund.
- **Succession.** A successor, or up to four charities, may be named. Otherwise GS PF "will close your named account and reallocate the remaining units" to the Directors' Philanthropy Fund.
- **Administrator in 2008:** Ayco, a Goldman subsidiary, for "grant and disbursement processing".

**What is true in 2026.**
- **The donor web is Ren iPhi.** The footer shows Stellar Technology Solutions, LLC, © 2001–2026.
- **There is a Goldman.com single sign-on button:** "Click here to Login with Goldman.com account for increased security" ([donor web](https://gspf.goldman.com/gspf/)) [F].
- **The CY2024 Part VII-B contractors do not include Stellar.** They are:
  - Goldman Sachs Trust Co: $14.60m, investment/advisory
  - Goldman Sachs & Co: $8.08m, "TECH & INV ADV FEES"
  - Oak Hill Advisors: $2.31m
  - Ayco: $1.03m, admin services
  - Sapient: $0.82m, technology services

  ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml)) [X]. **[I]** The iPhi licence may be paid through Goldman Sachs & Co or fall below the $100k reporting threshold.
- **Outbound flows happen in practice.** CY2024 Schedule I shows $446.0m granted to national DAF sponsors ([transfer terms v2](../../data/mission-2026-11-14/sponsor-transfer-portability-terms-v2.csv)).

**Correction to the repo.**
- **[goldman-sachs-two-daf-programs-2026-11-11.md](../goldman-sachs-two-daf-programs-2026-11-11.md)** says "No verified Ren relationship found". That is superseded for the PWM program: the live donor web is Ren iPhi.
- **The A3 v1.1 consensus X1 row** says "No filed CY2024 return in harvest". The IRS 2025 index lists object 202503109349303645, filed 2025-11-06, with Schedule D year-end value $12.64bn. X1 can therefore cite a filed return. The score stays 3.

## 3. Goldman Sachs Gives (EIN 11-3813663)

- **No public terms.** No circular, donor guide or FAQ was found. The public page describes an employee DAF only: "Goldman Sachs’ senior employees work together to recommend grants" ([GS Gives](https://www.goldmansachs.com/community-transformation/goldman-sachs-gives)) [F].
- **The FY2025 return (FYE 2025-06-30, filed 2026-05-04) names Stellar Technology Solutions LLC** for "INFORMATION TECHNOLOGY" at $172,604. Other contractors and Schedule O:
  - Charities Aid Foundation America: $875,665, "GRANT ADMINISTRATION".
  - PwC: audit services.
  - Schedule O names Stellar among the parties with agreements "TO PROCESS AND SELL ANY PUBLICLY TRADED SECURITIES" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml)) [X].
- **The FY2024 return also lists Stellar**, at $139,000 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml)) [X].
- **This corrects the repo note** that FY2024 IT spend was "not a named technology vendor payment".
- **FY2025 Schedule D:** 763 DAFs, $324.0m contributions, $237.1m grants and $636.4m year-end value [X].
- **Not found:** grant rail, export, transfer and succession terms. GS Gives is not scored in A3.

## 4. Morgan Stanley GIFT (EIN 52-7082731)

**Documents.** The DFX portal home page links five documents ([portal](https://msgift.donorfirstx.com/)) [F]:
- the "Donor Circular and Disclosure Statement" (Aug 2024)
- the Donor Contribution Agreement (Jul 2024)
- a Primer (modified Jan 2026)
- the 2024 Impact Report
- Grantee Guidelines (2022)

**Administrator and platform.**
- **The circular gives the third-party administrator** "provision of an online contribution and grant-making platform, located at https://msgift.donorfirstx.com/ (the "Online Portal"); grantmaking due diligence; grant disbursement; and performance of certain accounting and record-keeping functions" ([circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)) [F].
- **The Primer names Ren:** "Back office administration provided by Ren, an unaffiliated charitable gift [administrator]" ([primer](https://msgift.donorfirstx.com/pdf/MSGIFT/MSGIFTPrimer.pdf)) [F].
- **The CY2024 Part VII-B** lists RenPSG at $14.93m for "ADMIN & LEGAL" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml)) [X].
- **Under the entity-scope rule, the portal features below are sponsor evidence**, because MS GIFT's own circular ties them to its program.

**Grant rail.**
- **The circular allows mail or bank payment.** Grants are "sent to the organization utilizing its validated mailing address or banking details. Each grant must be at least $250", "generally ... within 10 business days" ([circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)) [F].
- **The 2025 brochure claims** "Direct-to-charity digital payments" and "Rapid disbursement technology with ACH granting capabilities" ([brochure](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf)) [V].
- **The 2022 Grantee Guidelines still say** "the grant check and an accompanying letter" ([grantee guidelines](https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf)) [F].
- **No EFT provider, limit or charity enrolment path is published.** **[I]** Disbursement sits with Ren, so Ren's ACH ("Charities sign up for ACH once", [Ren payments](https://www.reninc.com/payments/)) is the likely rail. No MS GIFT source confirms it.
- **Remittance.** A "physical or electronic letter" names the account unless anonymous, and the donor may add an address [F].

**Data and statements.** "The donor may view grant disbursements out of the Account via the Online Portal, including within the quarterly Account statements accessible thereon" [F].
- **No download, export or history clause** was found.
- **The brochure claims more** [V]: "consolidated views across accounts and real-time tracking", and "Comprehensive dashboards".

**Transfer-out, dormancy and succession** ([circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)) [F]:
- **Eligible grantees.** Grants may go to "(1) domestic public charities, (2) domestic organizations, (3) private operating foundations, and (4) foreign organizations". Grants to "Other Grantee Organizations" carry extra fees. **Other DAF sponsors are not mentioned.**
- **Dormancy.** Accounts with no activity for five years may be distributed, or moved to the undesignated fund.
- **Succession.** Successors may be named, but MS GIFT "reserves the right to limit overall succession on Accounts to a specific number of generations and/or years". With no successor, the account becomes a "Terminated Account".
- **Inbound transfers.** The portal advertises the ability to "transfer a private foundation to a simpler gifting solution" ([portal](https://msgift.donorfirstx.com/)) [F].

**Adviser access.**
- **Advisers can act on verbal direction.** "Financial Advisors (and assistants and other Morgan Stanley branch-related personnel acting at their direction) are given the authority to submit grant recommendations for Accounts upon the donor's or Grant Advisor's verbal direction" [F]. They may also "access other information regarding the donor's Account".
- **No data feed is documented.** The Morgan Stanley Online link comes from a Ren FAQ already in the repo, not from MS GIFT terms.

**Visible DFX/Ren features:**
- recurring grants
- recoverable grants
- grants to non-501(c)(3) "Other Grantee Organizations"
- NextGen Legacy Accounts ($5,000 minimum)
- "Automatic charity vetting" [V], with Board approval of each grant kept in the circular
- a "Powered by Ren" image, msgift@reninc.com support, and Ren Terms of Service (Renaissance Acquisition Company LLC, May 2025; [ToS](https://msgift.donorfirstx.com/Terms%20of%20Service.pdf)) [F]

## 5. Bank of America Charitable Gift Fund (EIN 04-6010342)

**Documents.**
- Program Guidelines v3.2024 (modified 2024-09; [guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)). Filenames for 2025 and 2026 at the same path return 404.
- "Making the Most of Your ... CGF Account", dated 8/2024 ([sheet](https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf)).
- "Guide to Navigating Your Donor-Advised Fund", dated 9/2025, file modified 2026-02-23 ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)).

**Grant rail: check only, confirmed three times.**
- **2024 guidelines:** "Grants are issued via checks bearing the name of Bank of America Charitable Gift Fund", delivered by USPS first class to the legal address only [F].
- **2024 sheet:** "the Charitable Gift Fund sends all grant checks via USPS first class mail", and "95% of grants are mailed within 7-10 business days; among those, the average is 5 days" [F].
- **2025 guide:** grant details include "check number and date cleared" [F].
- **Remittance:** "the account name and the name of the Donor or Advisor, unless anonymity is requested" [F]. Custom acknowledgements print on the check, and an attention-to name appears on the memo line [F].

**Statements and export.**
- **Quarterly statements and confirmations.** These come as paperless e-delivery. The Documents tab holds "quarterly reports, gift receipts, grant letters and account correspondence" ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) [F].
- **Export.** The **contribution** listing has "You can export to Excel to sort and do analysis" [F]. The grant-listing pages show no export statement.
- **No contractual export or portability right** appears in the guidelines.

**Transfer-out and closing** ([guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)) [F]:
- **Termination.** If CGF terminates advisory rights, "the Donor or the Advisor may make a grant recommendation to a Qualified Organization or grant the remaining assets to another donor-advised fund". This is the **first explicit outbound DAF-to-DAF clause found in BofA terms**. It applies to the termination case only. The repo's transfer file v2 recorded "none_found".
- **Closing.** A month-end closing grant waits for that month's fees. A residual over $250 goes to the last grantee, and "The account will be closed after the quarter in which the final grant was made".
- **Dormancy.** After five years with no activity and attempted contact, the balance may move to the General Fund.
- **Succession.** "The Charitable Gift Fund cannot honor succession or beneficiary plans outlined in a will, trust, or other estate planning documents." Without a successor or charitable beneficiary, the balance goes to the General Fund.

**Adviser access and data integration.**
- **Bank portals show CGF data.** "Balances for Charitable Gift Fund accounts are now available on MyMerrill and Private Bank Account Access" ([portal](https://bofa.donorfirst.org/)) [F].
- **Bank portals show more than balances.** The 2025 guide shows MyMerrill and Private Bank summaries with "Top 3 charities", "A list of recent grants" and links to "Go to Donor Portal" and "Recommend a Donation" [F]. BofA Online labels the hand-off "Vendor Donor Portal" [F].
- **Advisers have view access.** The sheet says "Your financial advisor has access to view your account". Advisers can initiate transfers and review statements and performance reporting [F].
- **[I]** This is a bank-portal data integration. No API or file feed is documented.

**Ren DFX evidence and visible features.**
- **Ren hosts the portal.** The portal sits on donorfirst.org with a `dfx.css` stylesheet and a "DonorFirstX Portal Registration" link [F].
- **Ren mailboxes handle operations:**
  - advisers use charitablegiftfund@reninc.com, as does access reactivation [F];
  - paper grants under $250,000 "may be mailed or scanned and emailed to donations_cgf@reninc.com" (2025 guide) [F].
- **The Terms of Service file is byte-identical to MS GIFT's Ren ToS** [F].
- **Features shown in the 2025 guide:**
  - "search the GuideStar database" by name or EIN
  - suggest a new charity
  - recurring grants: monthly, quarterly, semi-annual, annual
  - future grants at least 5 days out
  - grant purpose with attestation
  - custom acknowledgements
  - Grant ID
  - "Grant Paid" email notifications
  - account roles that include financial advisers
  - investment reallocation up to four times a year

**990.** CY2024 Schedule O says the audited statements exist "TO SATISFY THE MA ATTORNEY GENERAL FILING REQUIREMENTS" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml)) [X]. They were not read, so X3 stays U.

## 6. National Christian Foundation (NCCF; EIN 58-1493949)

**Rail: electronic first, run in-house.**
- **Guide:** "Most grants are distributed electronically when possible." Approved grants go "by electronic funds transfer or check" with a letter "identifying your Giving Fund and any grant purpose you’ve provided" ([guide](https://www.ncfgiving.com/guide-to-giving-at-NCF)) [F].
- **Support FAQ:** "We often distribute grants via ACH or electronic transfer when available." A wire carries bank fees of "usually about $25" ([support](https://www.ncfgiving.com/support)) [F].
- **Enrolment is NCF's own "NCF eGrants".** The charity fills in an interest form, and "you will be contacted by an NCF representative". At peak times this "may take your charity up to six weeks" ([EFT sign-up](https://www.ncfgiving.com/eft-charity-sign-up)) [F]. Charities reach the form by scanning a QR code on a grant, through a referral from an NCF team member, or because a fundholder fills it in for them.
- **No third-party EFT provider is named.**
- **The grant terms on that page refer to an "attached excel letter"** [F].
- **Recurring grants** run weekly to annually: "NCF sends the grants as physical checks or electronic funds transfers (EFTs)" ([story, 2023-05-10](https://www.ncfgiving.com/stories/automate-your-giving-with-recurring-schedules)) [F].

**Statements and data.** "Quarterly and annual fund statements", plus "our secure online site" [F]. No download or export clause was found.

**Transfer-out and succession.**
- **Succession funds are restricted:** "Succession funds ... may not make grants to or transfer assets to another donor-advised fund sponsor or Giving Fund at NCF" [F].
- **Standard funds are not:** "If you choose to allow grants to other donor-advised fund sponsors, your successors will receive a standard Giving Fund with the flexibility to recommend those grants" [F].
- **Fund transfers inside NCF:** advisory access includes "request fund transfers" [F].

**Adviser access.**
- **A "Professional advisor" role exists:** "attorneys, accountants, or financial advisors, who have been invited", with either advisory access or view-only reviewer access [F].
- **No data feed is documented.**

**Platform.**
- **The login page is Salesforce/Skuid.** secure.ncfgiving.com loads `sfdc` and `skuid` resources, and the page is titled "MyGiving with NCF" [F]. No Ren DFX or iPhi marker is visible.
- **Stellar is still paid.** CY2024 Part VII-B pays Stellar Technology Solutions $2.50m for "SOFTWARE/CONSULTING", alongside Intellinet $4.63m, F7 NWO $1.78m, Salesforce $1.36m and SolTech $1.08m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml)) [X].
- **[I]** Ren's role at NCF is not visible from public pages.

---

## 7. P-STF-05: third-party EFT providers in 2026

### 7.1 PayPal Grant Payments

- **NPT:** "Grants of up to $250,000 will be processed via Grant Payments (electronic funds transfer via PayPal) or check." An unaccepted PayPal grant expires after 14 days and is reissued as a check ([NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf)) [F], as carried from [queue-state-filings-transfer-terms.md](queue-state-filings-transfer-terms.md).
- **Vanguard Charitable:**
  - **Policies:** grants are paid "through a third-party electronic fund transfer provider or by a check" ([policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines)) [F].
  - **Nonprofit page:** it names the provider. "Vanguard Charitable is now issuing Grant Payments with PayPal", and charities sign up at paypal.com/charities or confirm a PayPal account "that has confirmed charity status" ([nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations)) [F].
  - **2023 release:** "grants up to $10 million at no cost to the charity or grantmaker" ([Vanguard release, 2023-09-20](https://www.vanguardcharitable.org/news/vanguard-charitable-launches-electronic-grants)) [F]. **This limit is larger than NPT's $250,000** and comes from the 2023 release, not current policies.
  - **Grant minimum:** $500 [F].
- **Charityvest:** it used PayPal and is moving to Chariot from August 2026 (repo, [Chariot](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner)).
- **PayPal's current partner page** names no sponsors. It says only that "PayPal's Grant Payments can help you distribute charitable grants" and that "Each charity is vetted by PayPal" ([PayPal](https://www.paypal.com/us/webapps/mpp/givingfund/partner)) [F].
- **No 2025–26 source names a new PayPal Grant Payments sponsor.**

### 7.2 Chariot Disbursements

- **Chariot's default-source list** ([Chariot sources](https://help.givechariot.com/getting-started/sources.md)) [V] names Groundswell, Daffy, Founders Pledge, DAFShare, Endaoment, GoodToday, phil, EarthShare and TIFIN.
- **It also lists community foundations:** Saint Paul & Minnesota Foundation, Brooklyn Org, Dallas Jewish Community Foundation, Community Foundation of South Puget Sound, CF of Northwest Mississippi and CF of East Mississippi. Jewish Federation of Northern New Jersey is listed too.
- **Charityvest** appears in a separate Chariot article.
- **Chariot's "managed sources", a paid plan, include "PayPal Grant Payments" and "Fidelity Charitable".** These are reconciliation feeds, not disbursement partnerships.
- **Terms of Groundswell, one listed partner:** "There is no cost to receive disbursements on Chariot or transfer funds to an external financial account up to twice per month" ([Groundswell help](https://helpcenter.groundswell.io/hc/en-us/articles/42844007345812)) [F].
- **Chariot Deposit Accounts are offered "in partnership with Column N.A."** ([Chariot FAQ](https://help.givechariot.com/getting-started/disbursements-faqs.md)) [F].

### 7.3 Administrator and own-ACH rails

- **Ren.** "Charities sign up for ACH once and are digitally enabled for every DAF program we support". Payments "flow directly from your existing accounts, not through pooled third-party accounts" ([Ren payments](https://www.reninc.com/payments/)) [V]. Ren does not name the programs.
- **AEF is the only sponsor confirmation found:**
  - "Powered by Ren, charities can claim their organization, provide ACH information".
  - "Until your organization's ACH information has been submitted and verified in the new portal, grant payments will arrive by check" ([AEF charities](https://www.aefonline.org/charities/)) [F].
  - AEF's guidelines call ACH "the quickest and most secure" method ([AEF guidelines V1.6](https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf)) [F].
- **The BofA CGF portal is Ren's, yet its terms are check only (§5).** **[I]** Ren's ACH network therefore does not cover every Ren-administered sponsor (proposal P-BNK-02).
- **Fidelity Charitable:** Stripe and its own ACH. EFT is not currently required (repo [sponsor-grant-payment-policies.csv](../../data/mission-2026-11-14/sponsor-grant-payment-policies.csv)).
- **NCF:** in-house eGrants (§6).

### 7.4 Large community foundations (sample)

- **Greater Houston CF** (page "Last Updated: Apr. 17, 2026"). Charities submit banking information "using our secure process" with a voided check or bank letter, and staff confirm it. No provider is named ([GHCF](https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/)) [F].
- **Oregon CF.** "direct deposit ... on some grants". Charities need "a bank letter or voided check, and access to email" and complete an online form ([OCF](https://oregoncf.org/ach-grant-payments)) [F].
- **CF Greater New Haven.** "grant program recipients will receive grant payments only via an ACH", and the foundation pays the fees ([CFGNH](https://www.cfgnh.org/strengthening-nonprofits/grant-reporting)) [F]. The page covers competitive grants. DAF grants are not addressed.
- **Not found:** SVCF, Chicago Community Trust and JCF (NY). JCF's FAQ returned 403. Its August 2024 policy guide describes ACH and wire only for **contributions** ([JCF guide](https://jcfny.org/app/uploads/2018/06/10PolicyGuide.pdf)) [F].

### 7.5 Bank programs

- **BofA CGF:** check only (§5).
- **GS PF:** check (2008); the 2026 rail is unknown.
- **MS GIFT:** ACH claimed with no provider named (§4).
- **GS Gives:** not found.
- **J.P. Morgan, Wells Fargo and UBS** use NPT as sponsor or administrator (repo edges). No public page ties NPT's PayPal rail to those programs, so under the entity-scope rule **they are not recorded as PayPal users**.

---

## 8. Corrections and qualifications to earlier repo statements

1. **MS GIFT Donor Circular "not public"** ([transfer terms v2](../../data/mission-2026-11-14/sponsor-transfer-portability-terms-v2.csv); [queue-state-filings-transfer-terms.md](queue-state-filings-transfer-terms.md) §3). **Now public.** It is linked from the MS GIFT DFX portal.
2. **BofA CGF `outbound_policy_found = none_found`.** **Qualify.** The 2024 guidelines allow a grant of the remaining assets "to another donor-advised fund" when advisory rights are terminated.
3. **GS PF "No verified Ren relationship"** ([Goldman file](../goldman-sachs-two-daf-programs-2026-11-11.md)). **Superseded.** The PWM donor web is Ren iPhi (Stellar footer, 2026). GS Gives also pays Stellar directly (FY2024 and FY2025 990s).
4. **A3 v1.1 consensus GS PF X1** ("No filed CY2024 return in harvest"). **Correct the evidence pointer** to the filed return, object 202503109349303645, $12.64bn. The score stays 3.
5. **A3 v1.1 consensus NCF Y5** ("No transfer page found"). **NCF's published outbound term** was already in [queue-state-filings-transfer-terms.md](queue-state-filings-transfer-terms.md) and is reconfirmed here.

---

## Evidence for quadrant re-scoring

Rubric: [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §2 and §7 (v1.1). Current values are from [`quadrant-scores-A3-v11consensus.csv`](../../data/mission-2026-11-14/quadrant-scores-A3-v11consensus.csv). **No quadrant-scores file was edited.** The levels below are recommendations for the next re-score.

| Sponsor | Criterion | v1.1 consensus | Supported level | Evidence class | Basis |
|---|---|---|---|---|---|
| **BofA CGF** | X4 | 2 | 2 (stronger basis) | primary | Merrill, Private Bank and BofA Online portal integration; Ren-hosted DFX portal ([portal](https://bofa.donorfirst.org/); [guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) |
| BofA CGF | Y1 | U | **1** | primary | Documented Excel export of the contribution listing and downloadable statements; no API and no contractual export right ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) |
| BofA CGF | Y2 | U | **1** (floor 0) | primary | Check-only rail by its own 2024 and 2025 terms; online recommendation, recurring grants and check-cleared tracking lift it above 0 ([guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf); [sheet](https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf)) |
| BofA CGF | Y3 | U | U | — | No automation claim found |
| BofA CGF | Y4 | 1 | 1–2 (scorer judgment) | primary | Online applications from donors "not affiliated with a Merrill or Bank of America Private Bank associate" ([guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)): a direct segment beside the wealth channel |
| BofA CGF | Y5 | U | **2** | primary | A published outbound clause (termination case) plus closing terms. Not 3, because the export covers contributions only ([guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)) |
| **MS GIFT** | X3 | U | U | — | The 990 shows only EY "Tax & Audit services" ($185k); no audit was read |
| MS GIFT | X4 | 2 | 2 (stronger basis) | primary | The circular names the DFX portal and the administrator's scope; the Primer names Ren ([circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf)) |
| MS GIFT | Y1 | U | U | — | Statements are view-only; no export clause |
| MS GIFT | Y2 | U | **2** | vendor_claim (cap 2) | "banking details" in the circular; ACH "rapid disbursement" and digital payments in the brochure ([brochure](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf)) |
| MS GIFT | Y3 | U | **1** | vendor_claim | "Charity Vetting Automated with advanced tech", with Board approval of every grant kept; no controls documented |
| MS GIFT | Y4 | 1 | 1 | primary | NextGen and employee accounts are still Morgan Stanley clients |
| MS GIFT | Y5 | U | **≤1** (or keep U) | primary | Inbound private-foundation transfer advertised; no outbound terms. The §7 inbound-only cap applies ([portal](https://msgift.donorfirstx.com/)) |
| **GS PF** | X1 | 3 | 3 | primary | Pointer correction: filed CY2024 return, $12.64bn ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml)) |
| GS PF | X4 | 2 | 2 | primary | Ren iPhi donor web added to the GS Trust Co, Ayco and Sapient edges ([donor web](https://gspf.goldman.com/gspf/)) |
| GS PF | Y1, Y2, Y5 | U | **U** | — | The only terms date from 2008 (check rail, view-only history, no outbound clause). Scoring 2026 capability from them would break the bounded-truth rule. If a scorer accepts the 2008 text, it supports Y2 = 1 and Y1 = U at most (P-BNK-01) |
| GS PF | Y3 / Y4 | U / 1 | U / 1 | — | No change |
| **NCF** | X3 / X4 | 3 / 2 | 3 / 2 | primary | No change. Stellar ($2.50m) and Salesforce reconfirmed |
| NCF | Y1 | U | U | — | Statements plus a secure site; no export |
| NCF | Y2 | U | **2** | primary | "Most grants are distributed electronically when possible"; in-house eGrants enrolment with QR-code prompts; recurring EFT schedules. No state is shared with nonprofits, so not 3 ([guide](https://www.ncfgiving.com/guide-to-giving-at-NCF); [EFT sign-up](https://www.ncfgiving.com/eft-charity-sign-up)) |
| NCF | Y3 | U | U | — | None |
| NCF | Y4 | 1.5 | 1.5 | primary | No change |
| NCF | Y5 | U | **2** | primary | Published outbound term (standard funds may grant to other DAF sponsors); no history export ([guide](https://www.ncfgiving.com/guide-to-giving-at-NCF)) |
| **GS Gives** | — | not scored | — | primary | Out of A3 scope. Its Stellar payments are evidence for A1 Ren X4 (a customer edge) |

**A1 scope rule (§7).**
- **Customer edges to add for Ren:**
  - GS PF (iPhi donor web)
  - GS Gives (Stellar contractor)
  - BofA CGF (DFX portal; Ren mailboxes in sponsor documents)
  - MS GIFT (already recorded)
- **NCF stays "sponsor-built (Salesforce)" in A1** for the donor portal. The Stellar fee is noted but its scope is not visible.

**Indicative effect on Y-axis coverage** (scored weight ÷ 1.0; weights Y1 .25, Y2 .25, Y3 .15, Y4 .15, Y5 .20). This is for orientation only; positions are computed by `scripts/mission_quadrants.py`.

| Sponsor | Y coverage now | Y coverage if adopted | Indicative Y point |
|---|---|---|---|
| **BofA CGF** | 0.15 | **0.85** (Y1, Y2, Y4, Y5) | about 1.2–1.4. Leaves the "insufficient evidence" group |
| **NCF** | 0.15 | **0.60** (Y2, Y4, Y5) | about 1.9 |
| **MS GIFT** | 0.15 | 0.40–0.75 (Y2, Y4; plus Y3 and Y5 if accepted) | about 1.3–1.6 |
| **GS PF** | 0.15 | 0.15 | Stays "insufficient evidence" |

**AI overlay:** none of the five documents an AI capability. MS GIFT's "automated vetting" is not described as AI. No flag.

---

## Source register

| # | Source | Type | Source date | Retrieved | URL |
|---|---|---|---|---|---|
| S1 | GS PF Program Circular | sponsor terms | 2008-08 | 2026-11-14 | https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111 |
| S2 | GS DAF Donor Web login (iPhi) | portal login page | 2026 | 2026-11-14 | https://gspf.goldman.com/gspf/ |
| S3 | GS DAF Donor Web contact page | portal page | 2026 | 2026-11-14 | https://gspf.goldman.com/gspf/ContactUs/tabid/112/Default.aspx |
| S4 | GS PF Form 990 TY2024 | IRS XML | filed 2025-11-06 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml |
| S5 | GS PF Form 990 TY2022 (old name) | IRS XML | TY2022 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202312859349302266_public.xml |
| S6 | GS Gives Form 990 FY2025 | IRS XML | filed 2026-05-04 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml |
| S7 | GS Gives Form 990 FY2024 | IRS XML | filed 2025-04-21 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml |
| S8 | Goldman Sachs Gives page | sponsor web | 2026 | 2026-11-14 | https://www.goldmansachs.com/community-transformation/goldman-sachs-gives |
| S9 | MS GIFT DFX portal home | portal login page | 2026 | 2026-11-14 | https://msgift.donorfirstx.com/ |
| S10 | MS GIFT Donor Circular and Disclosure Statement | sponsor terms | 2024-08 | 2026-11-14 | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf |
| S11 | MS GIFT Donor Contribution Agreement | sponsor form | 2024-07 | 2026-11-14 | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Contribution%20Agreement.pdf |
| S12 | MS GIFT Primer | sponsor brochure | 2026-01 (modified) | 2026-11-14 | https://msgift.donorfirstx.com/pdf/MSGIFT/MSGIFTPrimer.pdf |
| S13 | MS GIFT "Donor Advised Funds with MS GIFT" brochure | sponsor brochure | 2025-10 | 2026-11-14 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-how-it-works.pdf |
| S14 | MS GIFT Grantee Guidelines | sponsor terms | 2022 | 2026-11-14 | https://msgift.donorfirstx.com/pdf/MSGIFT/Grantee%20Guidelines.pdf |
| S15 | MS GIFT grant-making do's and don'ts | sponsor guide | 2024-10 | 2026-11-14 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf |
| S16 | Ren Terms of Service (MS GIFT and BofA portals; identical file) | vendor terms | 2025-05 | 2026-11-14 | https://msgift.donorfirstx.com/Terms%20of%20Service.pdf |
| S17 | MS GIFT Form 990 TY2024 | IRS XML | filed 2025-11-19 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml |
| S18 | BofA CGF Program Guidelines v3.2024 | sponsor terms | 2024-09 | 2026-11-14 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |
| S19 | BofA CGF portal home | portal login page | 2026 | 2026-11-14 | https://bofa.donorfirst.org/ |
| S20 | BofA "Making the Most of Your CGF Account" | sponsor guide | 2024-08 | 2026-11-14 | https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf |
| S21 | BofA "Guide to Navigating Your Donor-Advised Fund" | portal guide | 2025-09 | 2026-11-14 | https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf |
| S22 | BofA CGF Form 990 TY2024 | IRS XML | filed 2025-11-17 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml |
| S23 | NCF Guide to giving | sponsor terms | 2026 (live) | 2026-11-14 | https://www.ncfgiving.com/guide-to-giving-at-NCF |
| S24 | NCF support / grantmaking FAQ | sponsor web | 2026 | 2026-11-14 | https://www.ncfgiving.com/support |
| S25 | NCF EFT charity sign-up (eGrants) | sponsor web | 2026 | 2026-11-14 | https://www.ncfgiving.com/eft-charity-sign-up |
| S26 | NCF recurring schedules story | sponsor web | 2023-05-10 | 2026-11-14 | https://www.ncfgiving.com/stories/automate-your-giving-with-recurring-schedules |
| S27 | NCF donor login | portal login page | 2026 | 2026-11-14 | https://secure.ncfgiving.com/grant |
| S28 | NCF Form 990 TY2024 | IRS XML | filed 2025-11-06 | 2026-11-14 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513109349303201_public.xml |
| S29 | Vanguard Charitable Policies & Guidelines | sponsor terms | 2026-01-09 | 2026-11-14 | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| S30 | Vanguard Charitable nonprofits page | sponsor web | 2026 | 2026-11-14 | https://www.vanguardcharitable.org/nonprofit-organizations |
| S31 | Vanguard Charitable PayPal launch release | press release | 2023-09-20 | 2026-11-14 | https://www.vanguardcharitable.org/news/vanguard-charitable-launches-electronic-grants |
| S32 | NPT DAF guide | sponsor terms | 2026-10 (PDF) | 2026-11-14 (repo) | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf |
| S33 | PayPal Giving Fund partner page | vendor web | 2026 | 2026-11-14 | https://www.paypal.com/us/webapps/mpp/givingfund/partner |
| S34 | PayPal "How Philanthropic Dollars Move" | vendor paper | 2023 | 2026-11-14 (repo) | https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf |
| S35 | Ren payments page | vendor web | 2026 | 2026-11-14 | https://www.reninc.com/payments/ |
| S36 | AEF charities page | sponsor web | 2026 | 2026-11-14 | https://www.aefonline.org/charities/ |
| S37 | AEF Granting Guidelines V1.6 | sponsor terms | 2024-02 | 2026-11-14 | https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf |
| S38 | Chariot Sources (disbursement partners) | vendor docs | 2026 | 2026-11-14 | https://help.givechariot.com/getting-started/sources.md |
| S39 | Chariot Disbursements FAQ | vendor docs | 2026 | 2026-11-14 | https://help.givechariot.com/getting-started/disbursements-faqs.md |
| S40 | Groundswell: "We Partner with Chariot" | grantmaker help | 2026 | 2026-11-14 | https://helpcenter.groundswell.io/hc/en-us/articles/42844007345812 |
| S41 | Greater Houston CF ACH article | community foundation | 2026-04-17 | 2026-11-14 | https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/ |
| S42 | Oregon CF ACH page | community foundation | 2026 | 2026-11-14 | https://oregoncf.org/ach-grant-payments |
| S43 | CF Greater New Haven grant reporting / electronic payment | community foundation | 2026 | 2026-11-14 | https://www.cfgnh.org/strengthening-nonprofits/grant-reporting |
| S44 | JCF (NY) Policies & Procedures | sponsor terms | 2024-08 | 2026-11-14 | https://jcfny.org/app/uploads/2018/06/10PolicyGuide.pdf |
| S45 | Fidelity Charitable nonprofit FAQ (via repo) | sponsor web | 2026 | 2026-11-14 (repo) | https://www.fidelitycharitable.org/nonprofits/faqs.html |
| S46 | DAFgiving360 2024 Program Policies (via repo) | sponsor terms | 2024-12 | 2026-11-14 (repo) | https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf |
| S47 | IRS TEOS e-file index 2025 and 2026 | IRS index | 2026 | 2026-11-14 | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv |

## Data dictionary

**`data/mission-2026-11-14/bank-program-terms-2026.csv`**

| Column | Meaning |
|---|---|
| `sponsor` | Legal or program name with EIN |
| `item` | One of:<br>- `document_identity`, `grant_payment_rail`, `grant_minimum_timing`, `remittance_fields`<br>- `statements_data_access`, `data_export`<br>- `transfer_out_and_closing`, `dormancy`, `minimum_activity`, `succession`<br>- `adviser_access_data_feed`, `platform_vendor_visible`, `feature_visible`, `administrator_scope`<br>- `contractors_990`, `scale_990`, `assurance_990`, `entity_name_check`, `program_terms` |
| `finding` | Plain-language finding; "not found" when the source is silent |
| `quote` | Verbatim text of 40 words or fewer (blank when not found). XML rows elide with "..." between field values. Encoded-font PDFs (MS circular, BofA sheet) are transcribed from rendered pages |
| `source_url` | The primary source the quote comes from |
| `source_date` | Document date, revision label or filing timestamp; "2026" for live pages with no date |
| `retrieved` | Date fetched (2026-11-14) |

**`data/mission-2026-11-14/sponsor-eft-providers-2026.csv`**

| Column | Meaning |
|---|---|
| `sponsor` | Sponsor or grantmaker. Provider-level rows are labelled "(provider)". Grouped rows list several foundations that share one vendor-list source |
| `eft_provider` | Named third-party provider (PayPal Grant Payments, Chariot, Stripe), administrator rail (Ren), "own ACH", "None", or "not found" |
| `limits` | Per-grant limits, minimums or fees as stated; "Not stated" when silent |
| `enrollment_requirement` | What the charity must do to receive electronically |
| `check_fallback` | Whether and when a check is sent instead |
| `source_url` | One or more primary URLs, separated by " ; " |
| `retrieved` | Date fetched |

**`data/mission-2026-11-14/queue-proposals-bank-programs.csv`** follows [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). The prefix is `P-BNK-`.
