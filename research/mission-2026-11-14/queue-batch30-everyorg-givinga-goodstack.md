# Queue batch 30 B: Every.org's sponsor entity (P-QA3-07), Givinga's account count and partners (P-QA1-08), Goodstack US's 3 DAFs (P-BMG-04), Endaoment partner terms (P-AGA-03)

**Date:** 2026-11-15.

**Method:** Desk research from public sources only, 2021 onward. No accounts were created, no logins were used, no forms were submitted and nobody was contacted.

**Sources used:**
- IRS e-file index ([2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv), last modified 2026-10-21; earlier years from local copies).
- GivingTuesday mirror of IRS XML: `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<OBJECT_ID>_public.xml`.
- First-party help centres, read through their public Zendesk JSON (`/api/v2/help_center/en-us/articles.json`).
- First-party documents and PDFs.

**Builds on:**
- [queue-assurance-everyorg-givinga-monitoring.md](queue-assurance-everyorg-givinga-monitoring.md), including its wave-5 governing corrections. Those corrections make the Givinga account unit "undefined" (candidates: employer-provisioned employee accounts, or game/app-user records).
- [queue-bdc-coverage-migrations-goodstack.md](queue-bdc-coverage-migrations-goodstack.md) §4, including its wave-10 corrections. Goodstack US is "Goodstack-linked (service-provider relationship; not a subsidiary or affiliate)".

**Evidence tags:**
- **[F]** fact from a cited source.
- **[C]** calculation from cited inputs.
- **[I]** inference.

**Outputs:**
- [data/mission-2026-11-14/digital-sponsor-entities-2026.csv](../../data/mission-2026-11-14/digital-sponsor-entities-2026.csv): 4 entities.
- [data/mission-2026-11-14/relationship-graph-edges-additions-15.csv](../../data/mission-2026-11-14/relationship-graph-edges-additions-15.csv): edges EO001–EO015.
- [data/mission-2026-11-14/queue-proposals-batch30b.csv](../../data/mission-2026-11-14/queue-proposals-batch30b.csv): proposals P-B30B-01..03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-QA3-07** Every.org | **There is no separate DAF sponsor entity.** The legal recipient is Every.Org, Inc. (EIN 61-1913297), which filed Form 990-PF for CY2020–2024, so **no Schedule D DAF count or value exists for TY2021–2024** [F].<br>• Its audited statements (FY2021–FY2023), found through a link in the help centre, show **no DAF fund accounting**. Donations are unrestricted contributions "held with the intent to redistribute". Donor "giving credit" balances appear as **customer deposits**: $331,631 (2021), $296,194 (2022) and $112,808 (2023) [F].<br>• The CY2024 990-PF shows deferred revenue of $544,382 [F].<br>• The help centre says "we don't hold investments for individuals" [F].<br>• Terms: no platform fee; giving credit is treated "like a gift card"; unused credit is recognised as breakage after 2 years but can still be redeemed [F].<br>• Complaint and app signals: none found (see §1.4). | High on filings and statements; low on complaints. |
| **P-QA1-08** Givinga | **The 1,421,011 figure is real but was not paper-filed.** It comes from the **e-filed amended CY2024 return** (object 202503179349301975, ReturnTs 2025-11-13), which is in the IRS 2025 index (batch 2025_TEOS_XML_11A) [F]. DAFRC's "paper submission" label is wrong about the medium. The values match DAFRC exactly [F].<br>• The unit is still undefined (wave-5).<br>• New partner evidence:<br>  – **Janus Henderson Charitable Investment Accounts** (launched 2025-09), with **Givinga Foundation as the sponsor** and Givinga, Inc. as the technology provider [F];<br>  – **Ritmo** (2026-06), payments and disbursement [F];<br>  – EarthShare (2022), PlanSource (since 2020) and WeSpire (2019) [F].<br>• API: there is marketing for an "API-First Architecture", and a **docs.givinga.com portal behind a Redocly login**. No public API reference exists [F]. | High on the filing and on Janus Henderson; medium on the other partners (vendor-authored). |
| **P-BMG-04** Goodstack US | **Not identified from public sources.**<br>• The FY2025 XML has no Schedule D footnote on DAFs, and Schedule B names are restricted [F].<br>• The audited statements are released only "upon request via email" (FY2025 Part VI line 19 and the website), and outreach is barred [F].<br>• The 16 Schedule I grants of $48,550 or more sum to **$1,623,550**, against $1,660,000 of DAF grants [C]. So the 3 DAFs most plausibly made those large grants (Chicago, San Diego and travel/mobility themes) [I].<br>• Goodstack's own terms take **every** donation on a "Donor Advised Basis" [F]. That explains why the FY2024 return could count 7,268 "DAFs" [I].<br>• **Decision:** add it to the sponsor universe as a vendor-routed sponsor with `count_reliability = low`. Do not name the 3 funds. | Medium. |
| **P-AGA-03** Endaoment | **There is no public partner agreement or partner pricing page.** The fee schedule says "Endaoment API access pricing (contracted; not this App schedule)" and puts "Partner or revenue-share payments" out of scope [F].<br>• **Do partners hold funds?** Partners hold the **settlement leg**, but not legal ownership:<br>  – partner pledges are recorded only for donations that "already settled at a tech-platform partner" [F];<br>  – partner grants are submitted only after "the inbound custodian transfer settled on the partner side" [F];<br>  – for the Altruist programme, the DAF is an **"AUM in DAF account"** on Altruist Financial LLC's fee schedule, at 0.50% tiering down to 0.10% [F];<br>  – Altruist calls Endaoment "the legal owner of DAF assets" (edge ED006).<br>• **Review:** the API page documents no review step [F]. But each partner grant line creates an ordinary `asyncGrantTransfer`, and the submission status set includes **Stopped** [F]. The Fund Policies apply Endaoment due diligence to recommendations from "the applicable interface (or other channel Endaoment accepts)" [F]. The policy therefore covers partner grants; whether it is applied in practice cannot be seen [I]. | High on documents; low on actual practice. |

---

## 1. P-QA3-07: Every.org

### 1.1 Entity and filings [F]

- Every.Org, Inc., EIN 61-1913297, a California nonprofit "established in 2019" ([FY2023 audited FS](https://drive.google.com/file/d/1OJ7qglomTKL3QajTjgi05j6DGnvnI8cW/view), Note A).
- It is the only legal recipient: "Each donation you make goes to Every.org first and we immediately issue a receipt" ([how donations work](https://support.every.org/hc/en-us/articles/360059359213-How-does-making-a-donation-on-Every-org-work), updated 2026-11-05).
- Status: public charity under 509(a)(2), per an IRS letter dated 2025-10-23 ([tax status](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org); the [letter PDF](https://drive.google.com/file/d/1WLPWnCJ1--p6qQTu7gInxuj8rHUvD4CJ/view) is image-only and was not OCR'd).
- The same page says: "we don't hold investments for individuals."
- IRS index (checked 2026-11-15; 2026 file last modified 2026-10-21): the latest return is the [CY2024 990-PF](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml). There is **no CY2025 Form 990 yet**, so TY2021+ Schedule D DAF counts and assets are **not available**. The 990-PF has no Schedule D Part I.

### 1.2 Audited financial statements (new to the repo) [F]

The help article on [regulatory risk](https://support.every.org/hc/en-us/articles/5671184423187-How-does-using-Every-org-reduce-regulatory-risk) says "We also undergo an annual financial audit… Our latest 990 and audit report is available here". It links a public [Google Drive folder](https://drive.google.com/drive/folders/1gZ7gc8m2pZFPLP9zkcdUI4rgv4RhKD8m), which holds FY2021–FY2023 statements and governance letters plus the 2021–2022 990-PFs.

- **Auditor:** reports are on harriscpas.com letterhead (Meridian, Idaho). The FY2023 opinion is unmodified and dated 2024-07-10; the FY2022 report is dated 2023-07-18. The FY2023 governance letter says "All identified misstatements have been corrected by management".

| Item (Statement of financial position / activities) | 2020 | 2021 | 2022 | 2023 | 2024 (990-PF) |
|---|---|---|---|---|---|
| Customer deposits (unredeemed giving credits) | $30,685 | $331,631 | $296,194 | $112,808 | n/a. Part II deferred revenue: **$544,382** |
| Gift card sales (revenue) | — | $886,654 | $2,163,782 | $2,203,471 | — |
| Total assets | — | $5,202,463 | $4,245,377 | $6,425,934 | $9,663,375 |
| Net assets without donor restrictions | — | $4,774,840 | $3,899,342 | $5,733,070 | — |
| Grants and direct assistance | — | — | $17,493,434 | $16,782,740 | $44,931,032 (grants paid) |

- **Accounting policy:** "Donors can purchase donation credits… Customer Deposits… represent credits purchased but not yet redeemed. Revenue is recognized and the matching funds are expensed when the credit is redeemed" (FY2023 Note A).
- **Programme:** "These donations are held with the intent to redistribute the donated funds to other not-for-profit entities, based on the donors preferred choice" (same note).
- **[I]** Every.org's "DAF structure" is a pass-through intermediary with variance power. The disclosures read [F]: "we may, in our sole discretion, select a similar alternate charity" ([state disclosures](https://support.every.org/hc/en-us/articles/5968895910291-What-are-your-Nonprofit-State-Disclosures)); undeliverable gifts are refunded "with gift card credit" ([undeliverable](https://support.every.org/hc/en-us/articles/360058165694-What-happens-if-Every-org-can-t-deliver-a-donation-to-a-nonprofit)). It is not a fund-accounted DAF book. The stock of donor balances is small: $0.11m–$0.54m against $17m–$45m of annual grants [C]. If the first Form 990 reports anything on Schedule D, expect a balance in this range rather than a large DAF asset base [I].
- **[C]** Grants in 2023 were 148.8 times year-end customer deposits ($16,782,740 / $112,808).

### 1.3 Terms [F]

| Term | Source |
|---|---|
| No Every.org fees to donors or nonprofits; third-party processing only; optional tip | [Does Every.org charge fees?](https://support.every.org/hc/en-us/articles/360061886773-Does-Every-org-charge-fees) |
| Charity API: free for non-commercial use; "for-profit enterprise plans" by contact | same |
| Giving credit: "think of it like a gift card"; DAF grants can fund the account balance | [DAF article](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF) (updated 2026-11-03) |
| Gift cards never expire; unused credit after 2 years is recognised as "breakage" and may fund operations, but remains redeemable | [Gift card / giving credit](https://support.every.org/hc/en-us/articles/360057502334-How-do-I-use-a-gift-card-or-giving-credit) (updated 2026-11-03) |
| Unattributed wires: "we will apply it towards running Every.org" | [Wire/ACH](https://support.every.org/hc/en-us/articles/4405839531411-How-can-I-donate-via-wire-or-ACH-transfer) (updated 2026-10-16) |
| Payout rails: Stripe Connect weekly at 0%, PayPal Grants at 0%, ForGood at 1.5% | [Disbursements overview](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview) (updated 2026-10-23) |

- `www.every.org/terms`, `/donor-advised-fund` and `/charity-api` returned **403/429** on 2026-11-15, so the site terms of use were **not read**.

### 1.4 Complaint and app signals

- No US App Store app from Every.org was returned by the [iTunes Search API](https://itunes.apple.com/search?term=every.org&entity=software&country=us) [F].
- `trustpilot.com/review/every.org` returned 403. Search engines surfaced only the unrelated everyone.org.
- [G2](https://www.g2.com/products/every-org/reviews) shows 0 reviews.
- The repo corpus has 0 records ([complaint-rates-normalised.csv](../../data/mission-2026-11-14/complaint-rates-normalised.csv)).
- **[I]** Absence is not evidence. Coverage stays at "insufficient".

---

## 2. P-QA1-08: Givinga Foundation

### 2.1 The "paper-filed" 1,421,011 [F]

| Check | Result |
|---|---|
| IRS index 2025 rows for EIN 47-4172718, tax period 202412 | Two e-filed returns: original 202522379349301497 and amended **[202503179349301975](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml)** (batch 2025_TEOS_XML_11A) |
| Amended XML | `AmendedReturnInd` = X; `ReturnTs` = 2025-11-13; `DonorAdvisedFundsHeldCnt` = 1,421,011; contributions $12,300,836; grants $12,417,069; EOY value $1,949,239 |
| DAFRC row (dafrc-sponsor-schedule-d-fy2019-2024.csv) | Same four values; source columns say "paper submission" |
| Schedule O reason | "THE 2024 990 RETURN IS BEING AMENDED DUE TO A CHANGE IN FINANCIAL INFORMATION. THEREFORE, THE FOLLOWING FORM HAS CHANGES: SCHEDULE D PART I" |

- **Conclusion:** the count is validated against the e-file. The "paper" label is a DAFRC source-coding issue.
- **[I]** DAFRC may have taken the values from a paper or PDF copy before the XML was released.
- **Unit reliability is unchanged: low.**
  - Schedule D grants ($12.42m) exceed organisation grants paid ($11.09m) [F].
  - The average balance is $1.37 [C].
- **Other CY2024 facts from the same XML [F]:**
  - Part IX includes "EXTERNAL BANK FRAUD LOS[S]" **$316,184** (management and general) and "COST OF SERVICE" $1,123,082.
  - Schedule R lists **Givinga Inc, EIN 47-5498882**, as a related taxable corporation, with all Part V transaction lines "No".
  - No Schedule G or Schedule L is filed.
- The CY2025 return is not yet in the index.

### 2.2 Partners and white-label evidence (2021+)

| Partner | What Givinga does | Who is the sponsor | Source | Date |
|---|---|---|---|---|
| **Janus Henderson Charitable Investment Accounts** | Technology: "Givinga is the technology partner chosen to deploy the Charitable Investment Account… integrated directly with Janus Henderson Investors". Terms of Use cover "the Givinga, Inc. hosted software and service" at cia.janushenderson.app | **Givinga Foundation** [F]: checks "payable to Givinga Foundation… 198 Tremont St., Suite 406 Boston"; statuses "processed by the Givinga Foundation"; closures handled by "Givinga Foundation Support" | [Programme page](https://www.janushendersoncharitable.org/); [contribution methods](https://support.janushenderson.app/hc/en-us/articles/32175748584980); [closing](https://support.janushenderson.app/hc/en-us/articles/32380376838420); [Givinga blog](https://www.givinga.com/insights/blog/partner-spotlight-janus-henderson-launches-charitable-investment-accounts-powered-by-givinga) | Launched 2025-09; terms 2024-11-13 |
| Ritmo (daily-giving app) | "Givinga's technology powers the charitable payment processing and disbursement" | Not stated | [Givinga blog](https://www.givinga.com/insights/blog/giving-should-be-effortless.-ritmo-a-daily-giving-app-makes-generosity-a-one-tap-habit) | 2026-06-22 |
| EarthShare | Workplace-giving platform "powered by Givinga" | Not stated | [Givinga news](https://www.givinga.com/insights/news/earthshare-unveils-modernized-platform-powered-by-givinga) | 2022-04-05 |
| PlanSource | Benefits-marketplace channel; "introduced Givinga as a partner in 2020" | n/a | [Case study](https://www.givinga.com/insights/philantech-in-action/plansource) | undated |
| WeSpire / Novo Nordisk | Giving and matching engine inside WeSpire | n/a | [Blog](https://www.givinga.com/insights/blog/partnership-with-wespire) | 2019-11-25 (pre-2021; context only) |

**Janus Henderson programme terms [F]:**
- Flat 0.30% fee, "calculated daily and deducted monthly", with investments auto-liquidated to pay it.
- No account minimum; $5 minimum donation; grants from $50.
- Investments: Janus Henderson Government Money Market Fund (ACS Support Shares) plus three Global Allocation Funds. Crypto is out of scope.
- Disclosure: "the charitable organization facilitating the donor advised fund has exclusive legal control".
- Disbursements: a 7-day "mandatory cooling period"; US payments by ACH or check in 7–9 business days; international grants via GlobalGiving ($250 minimum) and CanadaHelps, monthly ([disbursements](https://support.janushenderson.app/hc/en-us/articles/32357696520340-How-Disbursements-Are-Made)).
- The old janushenderson.com article URL [returns 410](https://www.janushenderson.com/en-us/investor/article/one-big-beautiful-bill-act-and-charitable-giving), and the corporate CIA page 301-redirects to janushendersoncharitable.org [F].

**[I] Reading:**
- This is Givinga Foundation acting as a white-label sponsor for a public asset manager's investment DAF. That is a different product from the $1.37-average account base.
- It should raise the average balance from CY2025 onward, which P-B30B-03 tests.

**API evidence [F]:**
- [givinga.com/solutions](https://www.givinga.com/solutions) advertises "API-First Architecture… Integrate Givinga directly into your platform" and "white-labeled giving portals".
- `docs.givinga.com` redirects to `/redocly-login`, so the docs portal exists but is gated. It was not accessed.
- `api.`, `developer.` and `app.givinga.com` did not resolve through the proxy.
- No public endpoint reference was found.

---

## 3. P-BMG-04: Goodstack Impact Foundation US (EIN 87-3165286)

### 3.1 What the filings show [F]

| | FY2024 ([202522489349301512](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522489349301512_public.xml)) | FY2025 ([202602459349300235](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml)) |
|---|---|---|
| Schedule D DAFs | 7,268 | **3** |
| Contributions / grants / EOY value | $2,945,016 / $1,210,123 / $1,812,959 | $11,582,483 / $1,660,000 / $10,772,483 |
| Schedule D footnote | Part X line 2 tax note only | Part X line 2 tax note only (no DAF note) |
| Part VI line 19 (Schedule O) | "financial statements are available to the public on our website and upon reasonable request" | "makes its documents available to the public upon request via email" |
| Schedule I | — | 54 US grantees, $2,078,401; 16 grants of $48,550 or more total **$1,623,550** [C] |

**FY2025 grants of $48,550 or more [F]:**
- $200,000 each: Untours Foundation (PA), Latino Policy Forum (IL), Chicago Urban League (IL).
- $150,000: Global Glimpse (CA).
- $100,000 each: Unbound Now (TX), San Diego River Park Foundation, San Diego Parks Foundation, Jewish Family Service of San Diego, City Heights CDC.
- $75,000: Girls Going Global (GA).
- $50,000 each: Venture Out Project (MA), Rainbow Railroad USA (NY), Paso del Norte Center of Hope (TX), IGLTA Foundation (FL), All Wheels Up (TX).
- $48,550: Blue Star Families (CA).

### 3.2 Website and terms [F]

- The [US page](https://www.giftall.org/united-states) offers a financial report "by emailing pif-us@intelligentfoundation.org". **No audited statements are posted**, which contradicts the FY2024 Schedule O wording.
- Goodstack's [Global Charity Donation Terms](https://goodstack.org/legal/global-charity-donation-terms) (effective 2026-06-22):
  - define "Donor Advised Basis" as "the Donor will advise the Foundation of the charity… The Donation is an outright donation to the Foundation";
  - name the US Foundation as "Percent Impact Foundation… Federal Tax ID: 87-3165286 **or such other charitable entity registered with the Internal Revenue Service selected by Us**".
- The [Donation Delivery Policy](https://goodstack.org/legal/donation-delivery-policy) (effective 2024-11-15) and the [Employee Donation terms](https://goodstack.org/legal/employee-donation-additional-terms) (2024-10-15) both say "the Foundation retains exclusive control".

### 3.3 Reading and decision

- **[I]** All Goodstack-routed donations are legally donor-advised gifts. FY2024 seems to have counted each donor or partner balance as a DAF. FY2025 seems to have counted only a few named advised funds (most plausibly corporate), with the checkout and workplace flow (about $4.76m in, $5.28m out; see the prior §4.3) left outside Schedule D.
- **[I]** The large FY2025 grants cluster around Chicago, San Diego and travel/mobility/LGBTQ-travel causes. This fits 1–3 corporate or major-donor funds. **No company is named, because no source ties one to these grants.** A web search pairing the grantee names with Goodstack or Percent returned nothing.
- **[I]** The "or such other charitable entity… selected by Us" clause means Goodstack can re-route US flows away from this EIN. Volume through the foundation is therefore not a stable measure of Goodstack's US volume.
- **Decision:** include it in [digital-sponsor-entities-2026.csv](../../data/mission-2026-11-14/digital-sponsor-entities-2026.csv) as a `vendor_routed_sponsor` with low count reliability. Resolving which funds these are needs the audited statements from a state registry (P-B30B-01).

---

## 4. P-AGA-03: Endaoment partner terms and fund custody

### 4.1 Public pricing or agreement [F]

- [Fee Schedule](https://docs.endaoment.org/donors/resources/fee-schedule.md) is the "canonical public fee schedule for Endaoment App". In its "What this schedule is (and is not)" table, these are **out of scope**:
  - "Embedded / advisor-managed AUM partner programs (separate product lane; contracted)";
  - "Endaoment API access pricing (contracted; not this App schedule)";
  - "Partner or revenue-share payments".
- It adds: "Endaoment API programs are contracted separately. They are not a second public App schedule."
- It sends Altruist users to the [Altruist Financial LLC fee schedule](https://cdn.prod.altruistnet.tech/wp-content/uploads/2026/05/Altruist-Fee-Schedule-Sep-25-2026.pdf) (dated Sep 25 2026). That schedule's "Donor Advised Fund Administration (Basis Points on AUM in DAF account)" is 0.50% on the first $500K, then 0.30%, 0.20%, 0.15%, 0.13%, 0.12%, and 0.10% above $15M.
- **Conclusion:** no partner agreement or partner price list is public. Altruist's donor-facing DAF fee is the only partner-programme price found. How it is split with Endaoment is not disclosed.

### 4.2 Do partners hold funds? [F]

- [Partner Journey](https://docs.endaoment.org/developers/quickstart/partner-journey.md), step 3: "Call after the donation has already settled on your platform." Step 4: grant intake "after inbound custodian transfer has settled". Its common mistakes include "Submitting partner grants before custodian settlement completes".
- [Create cash donation pledge](https://docs.endaoment.org/developers/api/partner-endpoints/create-cash-donation-pledge.md): "Creates a liquidated cash donation pledge for a donation that has already settled at a tech-platform partner."
- [Submit settled grant](https://docs.endaoment.org/developers/api/partner-endpoints/submit-settled-grant.md) (OpenAPI v4.87.0):
  - `inboundCustodianTransfer.settledAtUtc` is described as "UTC timestamp when the inbound custodian transfer settled on the partner side";
  - `sourcePartnerAccountIdentifier` is described as "Opaque partner correlation identifier for the source DAF. Not a custodial account number";
  - the example `partnerFundingTransferId` is "alt-journal-987654".
- **[I] Reading:**
  - In the partner lane, assets sit at the partner's custodian (for Altruist, an "AUM in DAF account" at Altruist Financial). Endaoment records settled inflows as pledges and receives a custodian transfer before paying grants.
  - Endaoment remains legal owner, as Altruist's page says (ED006). So partners hold custody and the settlement timing, not ownership.
  - The "alt-journal" example suggests an Altruist journal entry, but this is not confirmed.

### 4.3 Is there review on partner grants?

- **[F]** The API page lists no review step. The tech-platform key alone authorises it, and 403 is returned if the partner "is not configured for settled operations or does not own the origin fund".
- **[F]** The response status values are `Accepted`, `Funding`, `Stopped`, `Funded`, `Failed` and `Cancelled`. Each grant line returns an `asyncGrantTransferId` with status `PendingLiquidation`, `Liquidated` or `Cancelled`, which is the same transfer type as donor `POST /v1/transfers/async-grants` ([Overview](https://docs.endaoment.org/developers/quickstart/overview.md)).
- **[F]** [Fund Policies](https://docs.endaoment.org/governance/documentation/policies-and-procedures.md) (last updated 2026-08-14):
  - "All grant recommendations must be submitted through the applicable interface (or other channel Endaoment accepts)…";
  - "Endaoment will perform due diligence to ensure that Funds are directed to a qualified charitable organization";
  - integration partners must notify Endaoment of new funds, closures and migrations, and changes of advisor.
- **[F]** [Going to Production](https://docs.endaoment.org/developers/quickstart/going-to-prod.md) requires only a joint validation on dev or staging.
- **[I] Answer:** by policy, partner grants are in scope for due diligence. They use the same async-grant pipeline, and a `Stopped` state exists. Whether a human or rules review actually runs on partner submissions is not documented. That is a documentation gap, not evidence that no review happens. Update the agentic-audits row from "no review documented" to "policy-level review applies; API-level step undocumented".

### 4.4 Side finding: Endaoment Schedule D [F]

| FY (June year-end) | Object | DAFs | Contributions | Grants | EOY value |
|---|---|---|---|---|---|
| 2022 | [202323209349303992](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323209349303992_public.xml) | 331 | $43,237,525 | $24,976,644 | $15,309,881 |
| 2023 | [202411369349317486](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349317486_public.xml) | **not reported** (no Schedule D Part I values) | — | — | — |
| 2024 | [202542899349300104](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml) (filed 2025-10-15) | **6,000** | $36,361,819 | $34,818,019 | $17,112,374 |
| 2025 | 202631359349315978 (in the IRS index; **404 on the mirror**) | — | — | — | — |

- DAFRC's FY2023–2024 Endaoment rows are "Imputed" (407 and 425 DAFs). The e-filed FY2024 return says 6,000 [F].
- **[I]** The round number suggests an estimate. Use 6,000 with a flag (P-B30B-02).

---

## 5. Limits

- Every.org's site pages (terms, DAF page, API page) were blocked (403/429). Terms come from the help centre only.
- The IRS letter PDF is image-only.
- Givinga's account unit and the share of Janus Henderson CIA assets are unknown until CY2025 returns are filed.
- Goodstack's 3 DAFs are unidentified (no outreach, and no public audited statements).
- Endaoment's partner contracts, revenue share and actual review practice are not public. The FY2025 XML was not retrievable from the mirror.
- Givinga partner pages are vendor-authored [V]. They show partnerships, not volumes.

---

## Source register

| ID | Source | Used for |
|---|---|---|
| S1 | IRS e-file index [2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (last modified 2026-10-21); 2022–2025 local copies | Return inventory for EINs 61-1913297, 47-4172718, 87-3165286 and 84-4661797 |
| S2 | GivingTuesday XML mirror: [202502749349100700](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml), [202503179349301975](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml), [202522489349301512](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522489349301512_public.xml), [202602459349300235](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml), [202323209349303992](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202323209349303992_public.xml), [202411369349317486](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349317486_public.xml), [202542899349300104](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml) | Schedule D, Part IX, Schedules I, O and R |
| S3 | Every.org audited FS FY2021–2023 and governance letter FY2023 ([Drive folder](https://drive.google.com/drive/folders/1gZ7gc8m2pZFPLP9zkcdUI4rgv4RhKD8m), linked from the [support article](https://support.every.org/hc/en-us/articles/5671184423187-How-does-using-Every-org-reduce-regulatory-risk)) | Customer deposits, accounting policy, auditor |
| S4 | Every.org help centre (Zendesk API listing of 94 articles, 2026-11-15): [tax status](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org), [fees](https://support.every.org/hc/en-us/articles/360061886773-Does-Every-org-charge-fees), [DAF](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF), [gift card](https://support.every.org/hc/en-us/articles/360057502334-How-do-I-use-a-gift-card-or-giving-credit), [wire](https://support.every.org/hc/en-us/articles/4405839531411-How-can-I-donate-via-wire-or-ACH-transfer), [state disclosures](https://support.every.org/hc/en-us/articles/5968895910291-What-are-your-Nonprofit-State-Disclosures), [disbursements](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview), [undeliverable](https://support.every.org/hc/en-us/articles/360058165694-What-happens-if-Every-org-can-t-deliver-a-donation-to-a-nonprofit), [how donations work](https://support.every.org/hc/en-us/articles/360059359213-How-does-making-a-donation-on-Every-org-work) | Terms and rails |
| S5 | [iTunes Search API](https://itunes.apple.com/search?term=every.org&entity=software&country=us); [G2](https://www.g2.com/products/every-org/reviews) | App and complaint signals |
| S6 | Givinga: [sitemap](https://www.givinga.com/sitemap.xml), [partners](https://www.givinga.com/partners), [solutions](https://www.givinga.com/solutions), JH, Ritmo, EarthShare, PlanSource and WeSpire posts (links in §2.2); docs.givinga.com (login redirect observed) | Partners and API evidence |
| S7 | Janus Henderson: [programme page](https://www.janushendersoncharitable.org/); help centre ([contributions](https://support.janushenderson.app/hc/en-us/articles/32175748584980), [disbursements](https://support.janushenderson.app/hc/en-us/articles/32357696520340-How-Disbursements-Are-Made), [closing](https://support.janushenderson.app/hc/en-us/articles/32380376838420), [Terms of Use](https://support.janushenderson.app/hc/en-us/articles/32913591667092)) | Sponsor identity and terms |
| S8 | GIFT [US page](https://www.giftall.org/united-states) and [FAQ](https://www.giftall.org/); Goodstack [Global Charity Donation Terms](https://goodstack.org/legal/global-charity-donation-terms), [Donation Delivery Policy](https://goodstack.org/legal/donation-delivery-policy), [Employee Donation terms](https://goodstack.org/legal/employee-donation-additional-terms), [Hosted Gateway terms](https://goodstack.org/legal/end-user-hosted-donation-gateway-terms) | Goodstack routing and "Donor Advised Basis" |
| S9 | Endaoment docs: [llms.txt](https://docs.endaoment.org/llms.txt), [Partner Journey](https://docs.endaoment.org/developers/quickstart/partner-journey.md), [Submit settled grant](https://docs.endaoment.org/developers/api/partner-endpoints/submit-settled-grant.md), [Create cash pledge](https://docs.endaoment.org/developers/api/partner-endpoints/create-cash-donation-pledge.md), [Overview](https://docs.endaoment.org/developers/quickstart/overview.md), [Going to Production](https://docs.endaoment.org/developers/quickstart/going-to-prod.md), [Fee Schedule](https://docs.endaoment.org/donors/resources/fee-schedule.md), [Fund Policies](https://docs.endaoment.org/governance/documentation/policies-and-procedures.md), [Fund Agreement](https://docs.endaoment.org/governance/documentation/fund-agreement.md) | P-AGA-03 |
| S10 | [Altruist Fee Schedule Sep 25 2026](https://cdn.prod.altruistnet.tech/wp-content/uploads/2026/05/Altruist-Fee-Schedule-Sep-25-2026.pdf) (via [legal page](https://altruist.com/legal/altruist-financial-llc-fee-schedule/)) | Partner-programme DAF fee |
| S11 | [data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | DAFRC comparison (Givinga "paper submission"; Endaoment "Imputed") |

## Data dictionary

### digital-sponsor-entities-2026.csv

One row per digital or vendor-linked DAF sponsor entity.

| Column | Meaning |
|---|---|
| entity_id | DSE-NN |
| legal_name, ein | Legal entity receiving donations |
| entity_role | `platform_sponsor_pass_through`, `sponsor_with_affiliated_vendor`, `vendor_routed_sponsor` or `platform_sponsor_with_partner_api` |
| technology_partner | Vendor or custodian relationships, as stated in sources |
| latest_return_period, return_form, object_id | Latest IRS e-file return (YYYY-MM) used |
| schedule_d_daf_count, schedule_d_contributions_usd, schedule_d_grants_usd, schedule_d_eoy_value_usd | Schedule D Part I lines 1–4 (column a). `not_reported` when the form has no Schedule D |
| avg_value_per_account_usd | [C] EOY value ÷ count |
| count_reliability | Analyst grade, with the reason |
| balance_proxy_label, balance_proxy_usd, balance_proxy_source | For non-Schedule-D filers, the closest audited or 990 balance measure |
| public_fee_terms | Donor-facing fees found |
| partner_or_white_label_programs | Named partner programmes |
| complaint_app_signal | What was checked and the result |
| evidence_tags | F/C/I |
| primary_source_url, accessed_date, notes | Provenance |

### relationship-graph-edges-additions-15.csv

- Same columns as `relationship-graph-edges.csv`. IDs are EO001–EO015.
- New `relationship_type` values used: `disbursement_partner`, `channel_partner`, `auditor`, `donation_channel`, `fee_charger`, `investment_manager`.

### queue-proposals-batch30b.csv

- Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- IDs are P-B30B-01..03.

## Validation corrections (wave 15, 2026-11-15) — governing
Source: [validation-wave15-report.md](validation-wave15-report.md); register `data/mission-2026-11-14/validation-register-wave15.csv`.

1. **Line 33 (§0, P-QA3-07 cell), the bullet "The CY2024 990-PF shows deferred revenue of $544,382 [F]".**
   - Replace with: "The CY2024 990-PF shows deferred revenue of $544,382 (BOY $514,058) [F]. This is a broader measure than audited customer deposits: at 2023-12-31 the 990-PF shows $514,058, while the audit shows $112,808."
2. **Line 66 (§1.2 [I]).**
   - Replace: "The stock of donor balances is small: $0.11m–$0.54m against $17m–$45m of annual grants [C]."
   - With: "The stock of donor balances is small: audited customer deposits were $0.11m–$0.33m (2021–2023), against $17m–$45m of annual grants [C]. The 990-PF deferred revenue ($0.51m BOY, $0.54m EOY 2024) is not like-for-like with those deposits [V wave 15]."
3. **Line 58 (§1.2 table, 2024 column).** Replace "n/a. Part II deferred revenue: **$544,382**" with "n/a. Part II deferred revenue: **$544,382** (BOY $514,058; not comparable with audited customer deposits)".
4. **Line 103 (§2.1 Conclusion).** Append: "The original CY2024 return (202522379349301497, ReturnTs 2025-08-25) included Schedule D but no DAF Part I values. The amended return added them, which is consistent with DAFRC sourcing the figures outside its XML pipeline [V wave 15]."
5. **Line 118 (§2.2, Janus Henderson row, "Who is the sponsor" cell).** Replace "**Givinga Foundation** [F]:" with "**Givinga Foundation** ([F] operating text; the sponsor role is read from it, since no JH page uses the word 'sponsor'):".
