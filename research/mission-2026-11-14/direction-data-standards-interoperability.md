# Direction: data standards and interoperability for DAFs and charity data (P-NEW-STD-01)

**Date:** 2026-11-15. **Status:** Desk research using public, first-party pages and public IRS XML. No logins, keyed API calls, form submissions or outreach. robots.txt was read on every host before fetching. Hosts whose robots.txt could not be read (candid.org returned 403) were not fetched; facts about them come from search snippets and are tagged [R]. Recency rule applied: current state is 2021–2026. The one older item is the 2021 IRS exit from AWS, which explains today's distribution.

**Tags:** [F] read first-hand in a primary source; [R] reported by a secondary source or search snippet, not verified; [I] inference; [C] computed here.

**Outputs:**
- `data/mission-2026-11-14/daf-data-standards-2026.csv` (32 rows, DS01–DS32)
- `data/mission-2026-11-14/queue-proposals-batch40-n13.csv` (P-B40N13-01 to -03)

**Read first, and respected:**
- [queue-batch36-agent-terms-controls.md](queue-batch36-agent-terms-controls.md), with the wave-21/22 corrections. Endaoment's T&C bars sharing API credentials. Its two sanctioned third-party tracks are OAuth clients and the Partner API.
- [queue-batch35-access-owners-faith.md](queue-batch35-access-owners-faith.md), with the wave-20 corrections.
- [ai-governance-failure-modes.md](ai-governance-failure-modes.md), with red-team correction 17. Remittance memos and purpose fields count as attacker-writable text (F15).

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| Is there an open, multi-sponsor DAF grant-request standard? | **No.** None was found. **DAF Direct** is a closed, sponsor-run widget with 3 sponsors and no public API or spec. **Chariot's DAFpay** sponsor guide is the nearest thing to a published grant-request spec, but it is vendor-governed: Chariot certifies each integration, and the guide says it "does not require you to implement an exact API specification". | High on absence within sources searched; medium that nothing exists privately |
| Do DAF grant metadata travel with the payment? | **Not in any documented case.** Fidelity's ACH grant details are "Sent with grant notice", by email daily, and Stripe grants are viewed in a dashboard. Chariot asks sponsors to put its ID on the "grant letter / remittance advice". ACH CCD allows one 80-character addenda; CTX allows up to 9,999. No DAF-specific addenda or ISO 20022 convention was found. | High on the cases read; not a census |
| What do public IRS data give on DAFs? | **Sponsor-year aggregates only.** Schedule D Part I gives 4 amounts plus 2 Yes/No items, and Part V lines 8–9b give 3 flags. **Schedule I** lists grants over $5,000 by recipient EIN, but in 2 of 3 sampled sponsors the purpose field holds one boilerplate string. There is no fund, donor, date or rail field. | High |
| Is there a US open grant-data standard like 360Giving? | **For private philanthropy, none found.** For federal grants there is: **Grants Data Standards v3.0 (2026-06-17)** under the GREAT Act, with HHS as the standards-setting agency, plus GSDM v1.2 for USAspending. | High (federal); medium (private absence) |
| Are charitable or DAF accounts in scope for FDX / §1033? | **Not as far as the evidence shows.** §1033 covers Reg E accounts, Reg Z credit cards and payment facilitation. The rule is enjoined, and a reconsideration NPRM was sent to OIRA in Aug 2026. FDX (CFPB-recognised standard setter, Jan 2025) keeps its spec behind membership. Chariot's FDX v6 API covers nonprofit deposit accounts, not DAFs. [I] A DAF is the sponsor's asset, so a donor probably has no §1033 right to its data. | Medium (spec not read; inference on Reg E) |

---

## 1. Public data rails (IRS and its redistributors)

### 1.1 IRS distribution today

- **Form 990-series XML** is distributed only from the IRS site, as monthly ZIP files with a yearly CSV index. Files run from 2019 to "2026_TEOS_XML_01A through 09A". The page was reviewed 2026-10-22 ([IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads)) [F].
  - The bulk-data page shows the "Latest data posting XML: August 20, 2026" and says "The data set files are updated monthly" ([IRS bulk data](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)) [F].
- **AWS exit.** The AWS Open Data Registry marks the IRS 990 dataset **Deprecated**. It says "On December 16, 2021 the IRS announced that it would discontinue updates … starting December 31, 2021" ([registry.opendata.aws/irs990](https://registry.opendata.aws/irs990/)) [F].
- **Publication 78** was last updated 2026-09-10. It excludes "doing business as" names [F]. The **auto-revocation list** was updated 2026-09-08, and the IRS warns that some 2020 revocation dates are wrong [F]. Both are on the [bulk-data page](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads).
- **EO BMF** is a cumulative CSV split by state and region, with 1,984,891 records, "Updated data posting date: 11/10/2026". Field codes are documented in a separate PDF ([IRS EO BMF](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf)) [F].
- **Implication [I]:** eligibility data come as monthly snapshots, not as an event feed. Every sponsor and vendor diffs the files itself. This is the "continuous charity-status subscription" utility identified in `ai-economics-replacement-analysis.md`.

### 1.2 Schema access is two-tier

- **Full MeF schemas** are distributed through the e-services mailbox: "This mailbox is part of the Secure Object Repository (SOR)." The latest memo read (2024-12-16) released "Form 990x (990, 990-EZ, 990-PF): TY2024v5.0" ([IRS release memo](https://www.irs.gov/node/142836)) [F]. The current valid tax years are 2023–2026 ([IRS current valid schemas](https://www.irs.gov/e-file-providers/current-valid-xml-schemas-and-business-rules-for-exempt-organizations-modernized-e-file), page dated 2026-06-27) [F]. The 2025–2026 memos were not read.
- **Public "redacted" TEOS schemas** are "a self-service option … designed for non-software developers". The latest 990X package listed is **2024v5.0** ([TEOS schemas](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-teos-schemas)) [F].
  - A filed FY2025 return (JCF, object 202640629349300234) declares `returnVersion="2024v5.5"` [F]. The public schema therefore lags the versions actually filed [I].
- **Crosswalks across schema versions are community-made.** The Nonprofit Open Data Collective master concordance is ODC-By 1.0, has 188 commits and is marked **deprecated** in favour of "concordance990" ([GitHub](https://github.com/Nonprofit-Open-Data-Collective/irs-efile-master-concordance-file)) [F]. The successor's state was not checked.

### 1.3 DAF fields in the return (verified in XML)

| Form location | XML element(s) | Content |
|---|---|---|
| Form 990 Part IV line 6 | `DonorAdvisedFundInd` | Yes/No: maintains DAFs |
| Sched D Part I lines 1–4, col (a) | `DonorAdvisedFundsHeldCnt`, `DonorAdvisedFundsContriAmt`, `DonorAdvisedFundsGrantsAmt`, `DonorAdvisedFundsVlEOYAmt` | Count, contributions, grants and end-of-year value |
| Sched D Part I lines 1–4, col (b) | `FundsAndOtherAccountsHeldCnt`, `…GrantsAmt`, `…VlEOYAmt` | The same for "funds and other accounts" |
| Sched D Part I line 5 | `DisclosedOrgLegCtrlInd` | Donors told the assets are under the sponsor's legal control |
| Sched D Part I line 6 | `DisclosedForCharitablePrpsInd` | Donors and grantees told the funds are for charitable purposes only |
| Form 990 Part V lines 8, 9a, 9b | `DAFExcessBusinessHoldingsInd`, `TaxableDistributionsInd`, `DistributionToDonorInd` | Compliance flags under §4943, §4966 and §4967 |
| Sched I Part II (grants over $5,000) | `RecipientTable` → `RecipientEIN`, `IRCSectionDesc`, `CashGrantAmt`, `NonCashAssistanceAmt`, `PurposeOfGrantTxt` | Recipient-level annual totals |

Sources:
- Line wording: [Schedule D (Rev. Dec 2024)](https://www.irs.gov/pub/irs-pdf/f990sd.pdf), [Form 990 (2025)](https://www.irs.gov/pub/irs-pdf/f990.pdf) and [Schedule I (Rev. Dec 2024)](https://www.irs.gov/pub/irs-pdf/f990si.pdf) [F].
- Element names were checked in the JCF FY2025 XML: [GT lake object 202640629349300234](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640629349300234_public.xml) [F].

**Schedule I purpose text, three sponsors [C]:**

| Return | Schema | Sched I rows | Distinct purpose strings | Most common |
|---|---|---|---|---|
| [Jewish Communal Fund FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640629349300234_public.xml) | 2024v5.5 | 4,976 | 1 | "IN FURTHERANCE OF GRANTEE'S TAX-EXEMPT PURPOSE" |
| [Vanguard Charitable FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml) | 2023v6.0 | 24,269 | 1 | "FOR RECIPIENT'S EXEMPT PURPOSE" |
| [Schwab Charitable FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411039349301716_public.xml) | 2022v5.0 | 48,202 | 10 | "RELIGION RELATED" (15,063), "HUMAN SERVICES" (8,472) |

Reading [I]: grant-level public data carry recipient EIN and annual amount, and at best a sector label. They carry no donor intent, fund, date or rail. Purpose analytics need licensed data (Candid) or the sponsor's own records. Three returns are not a panel; P-B40N13-01 proposes one.

### 1.4 Redistributors

| Source | Access | DAF relevance | Evidence |
|---|---|---|---|
| **GivingTuesday 990 Data Lake** (bucket `gt990datalake-rawdata`) | Raw XML on S3 with no sign-in, used throughout this repo. Data marts and an API exist; the API is reported as open with a limit of 300 requests per 5 minutes. | Full returns | [F] bucket used directly; [R] for API and terms. The [portal](https://990data.givingtuesday.org/) returned a bot-verification page. |
| **ProPublica Nonprofit Explorer API v2** | No key; "Usage constitues agreement to our Data Terms of Use"; v1 removed 2023-07-13; 25 results per page since 2023-09-12. robots.txt disallows `/nonprofits/search*` for crawlers. | Org profiles and summary financials from EO BMF, the annual extract and XML; no DAF-specific fields documented | [F] [API page](https://projects.propublica.org/nonprofits/api), updated 2026-10-22 |
| **Candid APIs**: Essentials and Premier v4 (2026-03-25), Charity Check (+Bulk, PDF v2), Grants, Taxonomy, Demographics; Snowflake since 2025-04-01 | `Subscription-Key` header. Free trial "on request". "For production-level API subscriptions, please contact your business development representative." | Charity Check is the commercial eligibility service. The Grants API carries funder and recipient transactions. | [F] [developer.candid.org](https://developer.candid.org/) and [getting access](https://developer.candid.org/reference/getting-access). Price ("starting at $4,800" for Essentials) is [R] from a search snippet only. |
| **Candid PCS taxonomy** | Reported moved to **CC BY 4.0** in Nov 2025, with an NTEE→PCS crosswalk announced | A possible open purpose code list for a DAF grant record | [R]. The [developer page](https://developer.candid.org/docs/candids-taxonomy) states no licence. |

---

## 2. Shared rails and published grant-request specs

### 2.1 DAF Direct: closed, sponsor-run, initiation only

- **Sponsors and fees.** The home page lists three sponsors: **Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable**. It says "Neither you nor your donors will incur any download or transaction fees." The footer reads "© 2013 – DAF Direct" and the contact is `DAFDirect@fmr.com` ([dafdirect.org](https://www.dafdirect.org/)) [F].
- **Registration.** A nonprofit registers by EIN, accepts a User Agreement and receives either a **JavaScript widget** (160×273 or 250×327 pixels) or a **hyperlink**. The designation can be preset (up to 100 characters), and a suggested amount (at least $50 recommended) can be set ([Get DAF Direct](https://www.dafdirect.org/DAFDirect/)) [F].
- **No public spec.** No API, open spec or developer documentation is published, and the User Agreement text could not be read (it is a pop-up) [F].
- The operator ("DAF Direct Trust", run day to day by Fidelity on technical evidence) is covered in `queue-infrastructure-nonprofit-costs-emerging.md` §Q-B18 and not repeated here.

### 2.2 Chariot DAFpay: the de facto published spec, vendor-governed

**OAuth Integration (for sponsors with their own identity provider)** ([overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md), [API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md), [checklist](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/integration-checklist.md); API v2026-04-01) [F]
- The donor signs in on the sponsor's OIDC login page, and Chariot holds scoped, revocable tokens (`openid profile email offline_access`).
- Tokens must be "scoped to DAF granting only — never to investment, banking, or brokerage systems".
- Resource APIs: `GET /customers/current`, `GET /funds` (with `grantable_balance`), `POST /grants` and `GET /grants/{id}`. An EIN search is needed only if the grant API cannot take an EIN.
- Grant request fields: `fund_id`, `organization_id` or `ein`, `amount` (integer cents), `purpose`, `note` and `anonymous`. The Chariot Grant Request ID goes in `note` and "must appear on the grant letter / remittance advice sent to the nonprofit".
- `Idempotency-Key` is required. Status values are `pending`, `approved`, `paid`, `rejected` and `canceled`.
- Service targets: 99.9% availability, P95 latency under about 3.5 seconds, at least 10 requests per second.
- Governance: "Chariot does not require you to implement an exact API specification." Chariot runs a **certification** pass and then launches the sponsor "behind a flag". The typical sponsor build is 2–4 weeks with an existing IdP, or 1–2 months from scratch.

**Donor Accounts (for sponsors without APIs)** ([grant request lifecycle](https://docs.givechariot.com/v2026-04-01/guides/dafpay/donor-accounts/grant-request-lifecycle.md)) [F]
- The sponsor pulls Grant Requests from Chariot and calls submit or reject. An optional `external_grant_id` links the request to the sponsor's ledger.
- Statuses are `awaiting_account_decision`, `pending`, `submitted` and `rejected`. There is no bulk endpoint.

**Unintegrated grants (nonprofit side)** ([object](https://docs.givechariot.com/v2026-04-01/api/unintegrated-grants/get.md)) [F]
- Fields include `trackingId`, `paymentChannel: offline` and the deprecated `userFriendlyId` ("the 'Chariot ID', … included in the payment from the DAF provider").

**Reading [I].** This is a de facto open-*documented* but not open-*governed* spec. The correlation key that makes reconciliation work is Chariot's own ID, which the sponsor has to copy onto its remittance.

### 2.3 Sponsor APIs converge on a common grant record [C/I]

| Field | Chariot sponsor spec | Endaoment async grant (OpenAPI 4.87.0) | Form 990 Sched I |
|---|---|---|---|
| Idempotency key | `Idempotency-Key` header (required) | `idempotencyKey` (required) | — |
| Source fund | `fund_id` | `originFundId` (required) | — (no fund field) |
| Recipient | `ein` or sponsor org ID | `destinationOrgId` (Endaoment UUID, required); optional `destinationSubprojectId` | `RecipientEIN` |
| Amount | integer cents | `requestedAmount` (required) | `CashGrantAmt` (annual total) |
| Purpose | `purpose` (free text) | `purpose` (required, free text) | `PurposeOfGrantTxt` |
| Donor disclosure | `anonymous` | `shareMyEmail` | — |
| Notes | `note` (carries the Chariot ID) | `specialInstructions` | — |
| Status | pending / approved / paid / rejected / canceled | `asyncStatus` | — |

Source: [Endaoment create async grant](https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md), where the required list is `idempotencyKey, originFundId, destinationOrgId, requestedAmount, purpose` [F].

The overlap is large enough that a minimal open DAF grant record is feasible (P-B40N13-03). Both purpose fields are free text, which raises the F15 injection concern in `ai-governance-failure-modes.md`.

### 2.4 Payment standards: metadata does not travel with the money

- **Nacha ACH.** The Payment Related Information field is 80 characters (positions 04–83), "an optional freeform text field that will travel with the payment instruction to the RDFI". It "may or may not be displayed to the recipient, based on the bank's capabilities". "PPD, CCD and WEB only allow for one addenda per record", and CTX "supports up to 9,999 addenda records" ([Nacha ACH Guide for Developers](https://achdevguide.nacha.org/ach-file-details)) [F].
- **Fidelity Charitable (largest sponsor).** ACH grant details are "Sent with grant notice", and notices are "Emailed daily". Stripe grants use an "On-demand dashboard" with notices "Emailed weekly" ([Fidelity Charitable EFT](https://www.fidelitycharitable.org/nonprofits/eft.html)) [F].
  - The enrolment form reportedly lists grant amount, acknowledgement information and donor-recommended purpose in the report [R].
  - The repo's [grant-rail-shares-panel-2026.csv](../../data/mission-2026-11-14/grant-rail-shares-panel-2026.csv) (S01–S02) puts Fidelity's EFT share at over 50% of grants.
- **ISO 20022.** Fedwire Funds moved to ISO 20022 on 2025-07-14 ([FRB press release 2025-07-15](https://frbservices.org/news/press-releases/071525-iso20022-migration-announcement)) [F]. The Fed's FAQ says the format supports structured remittance [R]. ASC X9's ISO 20022 Market Practices Forum published a *Remittance Content Market Guide* covering FedNow, RTP, Fedwire and CHIPS ([FedPayments Improvement](https://fedpaymentsimprovement.org/news/blog/new-guide-provides-clarity-on-use-of-iso-20022-remittance-information/)) [F]. The external purpose code **CHAR** ("Charity Payment") exists [R].
- **Gap.** No DAF sponsor was found that documents ISO 20022, CTX or a grant ID in ACH addenda. Remittance stays out-of-band (email, dashboard, letter). Chariot's gift-processing AI (see `ai-economics-replacement-analysis.md`) is effectively compensating for the missing standard [I].

---

## 3. Open grant-data schemas (non-DAF analogues)

| Standard | Steward and licence | Version | Adoption evidence | DAF fit |
|---|---|---|---|---|
| **360Giving** (UK) | 360Giving, a trading name of Funders Together, charity 1116201. Schema CC BY 4.0 ([governance](https://standard.threesixtygiving.org/en/latest/governance/)) [F] | **1.4**, announced 2024-03-26 ([forum](https://forum.threesixtygiving.org/t/minor-final-review-of-extensions-mechanism-update-available-for-comment/417/3)) [F]. No later release found. | Homepage shows 355 funders, 2m grants and £339bn, undated ([360giving.org](https://www.360giving.org/)). GOV.UK says to "Use the 360Giving Data Standard for disclosing grant data in government organisations", page updated 2026-01-29 ([GOV.UK](https://www.gov.uk/government/publications/open-standards-for-government/data-standard-for-grant-making)) [F]. | 10 required fields ([reference](https://standard.threesixtygiving.org/en/latest/technical/reference/)). The `regrantType` codelist runs FRG010–FRG070 and includes FRG050 "Fiscal sponsor", but has **no DAF/donor-directed code** ([codelists](https://standard.threesixtygiving.org/en/latest/technical/codelists/)) [F]. |
| **IATI** | Members; Secretariat hosted by UNDP with UNOPS since July 2023 [R]. Publishers must use an open licence (guidance) [R]. | 2.03 [I from the docs path] | 1,846 publishers and 1,038,446 activities, undated ([iatistandard.org](https://iatistandard.org/en/)) [F] | Aid activities and transactions; not used by US DAFs |
| **OCDS** | Open Contracting Partnership; Apache 2.0 | 1.1.5 ([standard](https://standard.open-contracting.org/latest/en/)) [F] | — | An analogue only: `ocid`-keyed releases compiled into records fit a grant lifecycle of request → approval → payment |
| **US federal Grants Data Standards** | HHS as standards-setting agency, under OMB M-24-11 and the GREAT Act | **v3.0, 2026-06-17**. Earlier: v1.0 2024-06-06, v2.0 2025-07-14, v2.1 2025-08-27 ([grants.gov](https://www.grants.gov/data-standards)) [F] | Format is XLSX plus JSON schemas. GSDM v1.2 (2025-12-19) aligns its financial assistance elements to v2.1 ([Treasury release notes](https://tfx.treasury.gov/system/files/2025-12/GSDM%20v1.2%20Annual%20Release%20Notes.pdf)) [F]. The USAspending API "is in V2" ([api.usaspending.gov](https://api.usaspending.gov/)) [F]. | Federal only, but the closest US template for a governed grant schema [I] |
| **US private philanthropy** | — | — | **No US equivalent of 360Giving was found** in two searches, one of them extended. The only DAF-sector data body found is DAFRC (reporting, not technical standards) [R]. | The gap |

---

## 4. Donor-data access: FDX and §1033

- **FDX.** Financial Data Exchange is "a collaborative consortium of over 200" firms. Its API is **v6.4 (Spring 2025)**. The developer portal is "Members Only", and the spec is obtainable via an observer membership under an FDX API License Agreement ([financialdataexchange.org](https://financialdataexchange.org/)) [F]. The CFPB recognised FDX as the first standard-setting body by decision and order in January 2025 ([CFPB order](https://files.consumerfinance.gov/f/documents/cfpb_standard-setter-decision-and-order-of-recognition-fdx_2025-01.pdf); [ABA Banking Journal](https://bankingjournal.aba.com/2025/01/cfpb-recognizes-fdx-as-open-banking-standard-setting-body/)) [F/R].
- **§1033.**
  - The final rule was released 2024-10-22 ([CFPB](https://www.consumerfinance.gov/personal-financial-data-rights/)) [F]. It covers Reg E accounts, Reg Z credit cards and payment facilitation ([12 CFR 1033.111](https://www.consumerfinance.gov/rules-policy/regulations/1033/111/)) [F/R].
  - An ANPR on reconsideration followed on 2025-08-22 [F]. The rule is **enjoined** by the E.D. Ky. ([Cozen, 2026-04-09](https://www.cozen.com/news-resources/publications/2026/section-1033-compliance-date-open-banking-rule-enjoined-and-under-reconsideration)) [R].
  - The "Personal Financial Data Rights Reconsideration" NPRM went to OIRA ([Consumer Finance Monitor, 2026-08-06](https://www.consumerfinancemonitor.com/2026/08/06/cfpb-sends-new-section-1033-open-banking-proposal-to-oira-for-review/)) [R]. Publication was not found.
- **Charitable accounts.** [I] A DAF is an irrevocable gift held as the sponsor's property (Schedule D line 5 is literally the "exclusive legal control" notice). It is unlikely to be a consumer "account" under Reg E, so neither §1033 nor FDX gives donors a portability right to DAF data. Whether FDX defines any charitable account type was **not verified**, because the spec is behind membership.
- **The one charity-side FDX implementation found** is Chariot's read-only FDX v6 API over **nonprofit deposit accounts**, still beta. It has a 24-month window and statements in PDF, CSV or BAI2 ([Chariot FDX](https://docs.givechariot.com/v2026-04-01/fdx/introduction.md)) [F].
- **Practical consequence [I].** Donor-side data portability depends on each sponsor's export terms (see `donor-data-export-top10-2026.csv`) and on the delegation routes in batch 35/36, not on any open-banking rail.

---

## 5. Comparison table: governance, licence, adoption, gaps

| # | Standard / rail | Maintainer | Openness | DAF adoption | Main gap for an AI-native entrant |
|---|---|---|---|---|---|
| DS01–06 | IRS 990 XML and DAF fields | IRS | Public data; full XSDs need an e-Services login; public schemas lag | Universal (filing) | Annual and aggregate. No fund or donor link. Boilerplate purpose. 12–24 month lag. |
| DS07–09 | Pub 78, EO BMF, revocations | IRS | Public, monthly | Universal input | Snapshots, not events. No DBA names. Known date errors. |
| DS11–12 | GT data lake; NODC concordance | GivingTuesday; volunteers | Free; licence of the lake not confirmed; concordance deprecated | Research and vendors | No governed cross-version crosswalk |
| DS13 | ProPublica API | ProPublica | Free, no key, terms of use | Research | No DAF fields; not for bulk use |
| DS14–15 | Candid APIs; PCS | Candid | Paid, licensed; PCS reportedly CC BY | Not verified among sponsors | Cost and licence of eligibility and grants data |
| DS16 | DAF Direct | DAF Direct Trust / Fidelity [I] | Closed | 3 sponsors | No API, no spec, closed membership |
| DS17–19 | Chariot DAFpay specs | Chariot | Documented, vendor-certified | Many sponsors (see repo rail files) | Vendor controls the spec and the correlation ID |
| DS20 | Endaoment API | Endaoment | Public OpenAPI; credentials personal (batch 36) | 1 sponsor | Sponsor-specific IDs |
| DS21–24 | ACH, ISO 20022, X9 guide | Nacha; Fed/ISO; X9 | Rules licensed; specs public | No DAF convention found | Remittance travels out-of-band |
| DS25–27 | 360Giving, IATI, OCDS | UK charity; IATI; OCP | Open (CC BY / Apache) | None in US DAFs | No DAF code; no US publisher base |
| DS28–29 | Federal grants standards, GSDM | HHS/OMB; Treasury | Open | Not applicable | Federal only |
| DS30–32 | FDX; §1033; Chariot FDX | FDX; CFPB; Chariot | Spec members-only; rule enjoined | None for DAFs | DAF accounts likely out of scope |

---

## 6. Gaps an AI-native entrant would face [I]

1. **No neutral grant-request rail.** An entrant can integrate sponsor by sponsor (Endaoment's API; Chariot OAuth if Chariot certifies it) or ride Chariot. DAF Direct is closed. Per batch 36, credential hand-off is barred at Endaoment and silent elsewhere.
2. **No neutral correlation ID.** Matching a grant to a payment depends on a vendor ID (Chariot) or on emailed reports (Fidelity). A cross-sponsor reconciliation product (entry option S2 in `ai-native-entrant-simulation.md`) must parse many formats, which is exactly the free-text attack surface flagged as F15.
3. **Eligibility data come as monthly snapshots.** Pub 78, BMF and revocations are monthly files. Continuous status has to be built, or bought from Candid.
4. **Public data are too coarse for grant-level analytics.** Schedule I gives recipient-year totals with boilerplate purpose at 2 of 3 sampled sponsors.
5. **Donor-data portability has no regulatory rail.** It rests on sponsor terms, not on §1033 or FDX.
6. **Opening.** No one owns a US open DAF grant record. The 360Giving and federal Grants Data Standards governance models (CC BY schema, stewardship committee, SemVer) show what one would take. The Chariot and Endaoment fields already overlap (§2.3).

---

## 7. Source register

| ID | Source | Date shown | Used for |
|---|---|---|---|
| SR01 | [IRS bulk data downloads](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads) | reviewed 2026-09-16 | DS01, DS07, DS09 |
| SR02 | [IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads) | 2026-10-22 | DS01 |
| SR03 | [IRS EO BMF](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) | posting 2026-11-10 | DS08 |
| SR04 | [IRS current valid EO schemas](https://www.irs.gov/e-file-providers/current-valid-xml-schemas-and-business-rules-for-exempt-organizations-modernized-e-file) | 2026-06-27 | DS02 |
| SR05 | [IRS MeF release memo 2024-12-16](https://www.irs.gov/node/142836) | 2024-12-16 | DS02 |
| SR06 | [IRS TEOS schemas](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-teos-schemas) | 2026-06-27 | DS03 |
| SR07 | [Form 990 (2025)](https://www.irs.gov/pub/irs-pdf/f990.pdf); [Sched D](https://www.irs.gov/pub/irs-pdf/f990sd.pdf); [Sched I](https://www.irs.gov/pub/irs-pdf/f990si.pdf) | 2025 / Rev. 12-2024 | DS04–06 |
| SR08 | GT lake XML: [JCF FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640629349300234_public.xml), [Vanguard FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml), [Schwab FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411039349301716_public.xml) | filed 2024–2026 | §1.3 counts |
| SR09 | [AWS registry irs990](https://registry.opendata.aws/irs990/) | — | DS10 |
| SR10 | [GivingTuesday 990 data](https://990data.givingtuesday.org/) (bot-blocked; search snippets) | — | DS11 [R] |
| SR11 | [NODC concordance](https://github.com/Nonprofit-Open-Data-Collective/irs-efile-master-concordance-file) | — | DS12 |
| SR12 | [ProPublica API](https://projects.propublica.org/nonprofits/api) | 2026-10-22 | DS13 |
| SR13 | [Candid developer](https://developer.candid.org/); [getting access](https://developer.candid.org/reference/getting-access); [taxonomy](https://developer.candid.org/docs/candids-taxonomy) | changelog to 2026-03-25 | DS14–15 |
| SR14 | [dafdirect.org](https://www.dafdirect.org/); [Get DAF Direct](https://www.dafdirect.org/DAFDirect/) | (c) 2013 | DS16 |
| SR15 | Chariot docs v2026-04-01: [OAuth overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md), [endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md), [checklist](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/integration-checklist.md), [grant requests](https://docs.givechariot.com/v2026-04-01/guides/dafpay/donor-accounts/grant-request-lifecycle.md), [unintegrated grant](https://docs.givechariot.com/v2026-04-01/api/unintegrated-grants/get.md), [FDX](https://docs.givechariot.com/v2026-04-01/fdx/introduction.md) | 2026-04-01 | DS17–19, DS32 |
| SR16 | [Endaoment async grant](https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md) | OpenAPI 4.87.0 | DS20 |
| SR17 | [Fidelity Charitable EFT](https://www.fidelitycharitable.org/nonprofits/eft.html) | (c) 1998–2026 | DS21 |
| SR18 | [Nacha ACH dev guide](https://achdevguide.nacha.org/ach-file-details) | undated | DS22 |
| SR19 | [FRB Fedwire ISO 20022 completion](https://frbservices.org/news/press-releases/071525-iso20022-migration-announcement); [X9 remittance guide note](https://fedpaymentsimprovement.org/news/blog/new-guide-provides-clarity-on-use-of-iso-20022-remittance-information/) | 2025-07-15 | DS23–24 |
| SR20 | 360Giving: [home](https://www.360giving.org/), [reference](https://standard.threesixtygiving.org/en/latest/technical/reference/), [codelists](https://standard.threesixtygiving.org/en/latest/technical/codelists/), [governance](https://standard.threesixtygiving.org/en/latest/governance/), [1.4 forum](https://forum.threesixtygiving.org/t/minor-final-review-of-extensions-mechanism-update-available-for-comment/417/3), [GOV.UK](https://www.gov.uk/government/publications/open-standards-for-government/data-standard-for-grant-making) | 2024-03-26; GOV.UK 2026-01-29 | DS25 |
| SR21 | [IATI](https://iatistandard.org/en/); [IATI Standard](https://iatistandard.org/en/iati-standard/) | news to 2026-11-04 | DS26 |
| SR22 | [OCDS](https://standard.open-contracting.org/latest/en/) | v1.1.5 | DS27 |
| SR23 | [Grants.gov data standards](https://www.grants.gov/data-standards); [GSDM v1.2 notes](https://tfx.treasury.gov/system/files/2025-12/GSDM%20v1.2%20Annual%20Release%20Notes.pdf); [USAspending API](https://api.usaspending.gov/) | 2026-06-17; 2025-12-19 | DS28–29 |
| SR24 | [FDX](https://financialdataexchange.org/); [CFPB FDX order](https://files.consumerfinance.gov/f/documents/cfpb_standard-setter-decision-and-order-of-recognition-fdx_2025-01.pdf) | 2025-01 | DS30 |
| SR25 | [CFPB PFDR](https://www.consumerfinance.gov/personal-financial-data-rights/); [1033.111](https://www.consumerfinance.gov/rules-policy/regulations/1033/111/); [Cozen](https://www.cozen.com/news-resources/publications/2026/section-1033-compliance-date-open-banking-rule-enjoined-and-under-reconsideration); [CFM](https://www.consumerfinancemonitor.com/2026/08/06/cfpb-sends-new-section-1033-open-banking-proposal-to-oira-for-review/) | 2025-08-27; 2026-04-09; 2026-08-06 | DS31 |

**Not done, and why:**
- candid.org pages: robots.txt returned 403, so they were not fetched.
- GivingTuesday portal: bot verification blocked it.
- FDX spec: members-only.
- DAF Direct User Agreement: a pop-up that could not be read.
- IRS 2025–2026 MeF memos: not located.
- GitHub API: not enabled in this session.
- No keyed API calls were made (Candid, Chariot or Endaoment).

---

## Data dictionary

### `data/mission-2026-11-14/daf-data-standards-2026.csv` (one row per standard, dataset, spec or rail)

| Column | Meaning |
|---|---|
| std_id | DS01–DS32 |
| name | Standard, dataset, spec or rail |
| category | `public_data`, `schema`, `schema_crosswalk`, `form_fields`, `api`, `taxonomy`, `shared_rail`, `sponsor_api`, `sponsor_remittance`, `payment_standard`, `open_grant_schema`, `open_schema_analogue`, `federal_grant_schema`, `data_access_standard`, `regulation` |
| layer | `reporting`, `identity`, `transaction_initiation`, `reconciliation`, `payment`, `grants`, `donor_data_access`, `nonprofit_data_access`, etc. |
| jurisdiction | US, UK, International, US federal, US/Canada |
| steward, steward_type | Who maintains it; government, nonprofit, vendor, sponsor, industry association, etc. |
| access_terms | Licence or access conditions as stated |
| cost_to_access | free / paid / not stated |
| current_version, version_date | As shown by the source; "n/a" where none applies |
| format | Technical format |
| auth_required | Credentials needed to read or use it |
| daf_relevant_content | Fields or objects relevant to DAF grants |
| granularity | Unit of record (grant, organisation, sponsor-year, account, etc.) |
| adoption_evidence | Observed adoption with figures where published |
| daf_sponsor_use_found | Whether DAF-sponsor use was found (Y / n/a / not verified / none found) |
| gap_for_ai_entrant | Main limitation for an AI-native entrant [I] |
| evidence_label | F or R (see tags) |
| source_url | Primary URL |
| retrieved | Access date |
| notes | Quotes, caveats, cross-references |

### `data/mission-2026-11-14/queue-proposals-batch40-n13.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). IDs run P-B40N13-01 to -03, state is `open`, and the parent is P-NEW-STD-01.

## Proposals

- **P-B40N13-01:** Schedule I purpose-text panel for the top 50 sponsors. Can public 990 data support purpose analytics?
- **P-B40N13-02:** Remittance census of the top 10 sponsors: ACH SEC code, addenda content and out-of-band channel.
- **P-B40N13-03:** Field-by-field map and draft of a minimal open DAF grant record (Chariot, Endaoment, 360Giving 1.4, federal GDS v3.0).
