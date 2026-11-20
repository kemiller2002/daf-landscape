# A minimal open DAF grant record, and what processor "accounts" measure (P-B40N13-03, P-G1913-03)

- **Queue items:**
  - P-B40N13-03 (grant-data schema map), from [direction-data-standards-interoperability.md](direction-data-standards-interoperability.md) §2.3 and `queue-proposals-batch40-n13.csv`;
  - P-G1913-03 (processor account counts), from [gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md) §4.3 and `queue-proposals-gap19-13.csv`.
- **Date:** 2026-11-19. Every page and return was read on that date. Public pages and public IRS XML only: no logins, no forms, no keyed API calls, no outreach.
- **Read first:**
  - [b4013-02-b4222-02-remittance-and-portal-features.md](b4013-02-b4222-02-remittance-and-portal-features.md), with the wave-39A corrections in [validation-wave39a-report.md](validation-wave39a-report.md). The corrected scope is kept here: no public page read for the eight readable top-10 sponsors states an ACH SEC code or a grant ID in addenda.
  - The research files that mention "data standard" (8 files; the substantive ones are the direction note above, `DAF-INDUSTRY-REPORT-2026-11.md` §(c) and `gap19-clarity-edf-new-findings.md`). None of them maps 360Giving or the federal standard field by field.
  - Processor account work already in the repo: [queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md) (A1/A2/A3 variants), [queue-batch38-data-followups.md](queue-batch38-data-followups.md) §1, [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md), [regulation-market-structure-portability.md](regulation-market-structure-portability.md) Q-B02.
- **Files written:**
  - [`data/mission-2026-11-14/daf-grant-schema-map-2026-11-19.csv`](../../data/mission-2026-11-14/daf-grant-schema-map-2026-11-19.csv): 12 rows (8 core fields of the draft record, 4 supporting), 26 columns.
  - [`data/mission-2026-11-14/processor-account-counts-2026-11-19.csv`](../../data/mission-2026-11-14/processor-account-counts-2026-11-19.csv): 12 rows (one per processor return), 28 columns.
  - [`data/mission-2026-11-14/queue-proposals-b40n13-03-g1913-03.csv`](../../data/mission-2026-11-14/queue-proposals-b40n13-03-g1913-03.csv): 6 rows.
  - [`scripts/mission_b40n13_03_g1913_03_build.py`](../../scripts/mission_b40n13_03_g1913_03_build.py): builds both CSVs, reads every Schedule D value from the XML, verifies every quote against the cached source and prints every figure below. Run `python3 -I scripts/mission_b40n13_03_g1913_03_build.py . <cache logs>`; without cache logs it fetches the XML from the GivingTuesday mirror and skips the web-quote check.
- **Labels:** [F] first-party text or filing read this pass. [R] carried from a repo file. [S] search-index text only. [B] blocked (robots.txt or unverifiable TLS). [C] computed by the script. [I] inference.

---

## 0. Answers

### (A) P-B40N13-03: a minimal open DAF grant record

| Question | Answer | Confidence |
|---|---|---|
| **Field overlap of the four schemas** | **Chariot and Endaoment each carry all eight core fields in some form, and six map one-to-one** (grant ID, fund ID, recipient, amount, purpose, status). Anonymity is a different boolean in each, and the payment reference is Chariot's copied id against Endaoment's transaction hash [C]. 360Giving 1.4 carries grant ID, recipient, amount, a coded purpose (`classifications`) and a payment ID (`disbursementTransaction/0/id`), but **no fund, donor-disclosure or status field**. The federal core elements (GSDM v1.3 FABS, the lineage of Grants Data Standards v3.0) carry award ID (FAIN), recipient (UEI, not EIN), amount, a programme code and an action type, but **no fund or payment reference** [F]. | High for Chariot, Endaoment, 360Giving and GSDM; **medium for GDS v3.0 itself, which could not be read** (§2) |
| **The draft record** | Eight core fields: `grant_id`, `fund_id`, `recipient_ein`, `amount` (integer cents + currency), `purpose_code` ({vocabulary, code}, with free text kept apart), `anonymity` (full_contact / name_only / anonymous), `status` (Chariot's five values + `returned`), `payment_reference` ({rail, reference, paid_date}); plus `sponsor_id`, `idempotency_key`, dates and `restriction_text` (§3.2). | Design [I] |
| **What Form 990 already requires** | **Only the recipient EIN in full; the amount and purpose in part.** Schedule I Part II asks for the recipient's EIN (column b), the year's total cash grants to that recipient (d), and a description of purpose (h), and only for recipients that got "more than $5,000 aggregate" in the year. Grant ID, fund ID, anonymity, status and payment reference appear nowhere on the public return [F]. | High |
| **Two corrections to the repo's earlier map** (§2.3 of the direction note) | Endaoment's OpenAPI is now **4.88.0** (the repo has 4.87.0), and `requestedAmount` is **USDC in its smallest unit (1000000 = 1 USD)**, not cents. Endaoment's `status` is deprecated; `asyncStatus` holds `PendingLiquidation`, `Liquidated` and `Cancelled`, which describe liquidation, not approval or payment [F]. | High |

### (B) P-G1913-03: what DAFRC's `number_of_daf_accounts` measures at processors

DAFRC's field is Schedule D Part I line 1, column (a). The IRS instruction is: "Report in column (a) the total number of donor advised funds and in column (b) the total number of other similar funds or accounts held by the organization at the end of the year" [F]. At the five processors that one line counts **three different units**, and in one case nothing was filed:

| Processor | DAFRC FY2024 value (source flag) | Filed Sched D Part I line 1 (col a / col b) | What the count measures | Count in account statistics? |
|---|---|---|---|---|
| **AOGF (Benevity)** | 720,545 (IRS 990) | **720,545 / 3**, year ended 2024-03-31. The filer's own note: "AOGF HAS A MICRODONATION DAF MODEL VERSUS A CONVENTIONAL DAF ENDOWMENT MODEL." | **Individual workplace donor accounts**, plus a few corporate DAFs in the same column. Its FYE 2026 return splits the same population into **695 DAFs and 751,746 other accounts**, whose individual donors recommend grants "AT OR NEAR THE TIME OF DONATION, WITHOUT ONGOING ADVISORY PRIVILEGES" [F] | **No.** Use 695 (AOGF's own DAF count) at most |
| **PayPal Charitable Giving Fund** | 694,979 (Imputed) | **380,644 / blank**, CY2024 (filed 2025-11-03) | **Consumer donor accounts** created by giving on partner sites and apps ("ON THE WEBSITES AND APPS THEY USE EVERY DAY"). Average year-end value $254.87; grants $2,090.35 per account [C]. Whether donors keep ongoing advice rests on a policy page that answered 403 [B]; the repo's reading is [S] | **No** for comparable totals; report in a processor series |
| **Givinga** | 1,421,011 (paper submission) | Original CY2024 return (2025-08-25): **Part I blank**. Amended return (2025-11-13): **1,421,011 / blank**. DAFRC's "paper" value equals the e-filed amendment [F] | **Individual and employee giving accounts on employer programs**: "INDIVIDUAL ACCOUNT HOLDERS" (Part III) and "Optional individual employee accounts" (website). **$1.37 of year-end value and $8.74 of grants per account** [C]: enrolment, not active advising [I] | **No**; low reliability |
| **Blackbaud Giving Fund** | 460 (Imputed) | **Blank** for CY2023 (return 202402119349300860, read by wave 40A), CY2024 and CY2025; last filed **359** (CY2022) [V wave 40A]. DAF amounts are filed | **Employer and campaign programs, not donor accounts** [I]: the fund "HARNESSES THE POWER OF CORPORATE GIVING" and makes grants from DAFs "THAT SUPPORT PEER TO PEER CHARITABLE GIVING CAMPAIGNS". A few hundred funds against $0.55bn of grants. In CY2025 it decided that CSRconnect employee donations "SHOULD NOT BE TREATED BY BBGF AS CONTRIBUTIONS TO DONOR ADVISED FUNDS" [F] | **No**: no filed count |
| **Network for Good / For Good** | 1 (Imputed) | **1 / 0**, CY2024; DAFRC's imputed value equals the filed value | **One pooled donor-advised fund** that every donor gives through: "you are contributing to a donor-advised fund at ForGood" [F]. Right for what line 1 asks (number of funds); not an account count | **No**: the unit is a fund, not donors |

**Bottom line (B).**
- **None of the five counts measures what sponsor counts measure** (one fund per donor or family with ongoing advice). Three count individual donors at a checkout or workplace (AOGF, PPGF, Givinga), one counts employer or campaign programs and has filed nothing since CY2022 (BBGF), and one counts a single pooled fund (For Good).
- **Processors should not be pooled with sponsors in account-level statistics** (account totals, accounts per sponsor, average balance per account, per-account complaint rates). They should be shown as a separate, labelled "processor accounts as filed" series. For dollar statistics (contributions, grants, assets) they stay in.
- **Effect [C]:** the five processors hold **2,522,661** of the **3,309,483** corrected FY2024 accounts (**76.2%**), using filed values where they exist and DAFRC's 460 for Blackbaud. Without them the comparable series is **786,822** accounts (it still includes 16,037 corrected accounts at the other 17 DAFRC processors; 770,785 without any processor) [V wave 40A], or **787,517** with AOGF's 695 corporate DAFs added back. That is within 461 of the repo's A2 variant (787,978), which still keeps Blackbaud's imputed 460 and For Good's 1.
- **Per-account complaint rates** for processors (gap19 §4.1) compare different units and should be dropped in favour of per-dollar or per-grant rates. Corrections are in §6.

---

## 1. Method

1. **Part A sources.**
   - **Chariot DAFpay OAuth sponsor spec** (API v2026-04-01): the API-endpoints page, the overview and the integration checklist, read as Markdown from docs.givechariot.com.
   - **Endaoment** "Create async grant" page, which embeds the OpenAPI document (`https://api.endaoment.org/oas-json`, version 4.88.0).
   - **360Giving Data Standard**: the technical reference page on standard.threesixtygiving.org (column titles, field names, required flags, the "10 required fields" text).
   - **Federal Grants Data Standards v3.0** at grants.gov could not be read (§2). The federal column therefore uses the **GSDM v1.3 Reporting Submission Specification, FABS tab** (Treasury, November 2026). The Data Foundation's fact sheet says the GREAT Act standards' initial core elements are "drawn from USAspending.gov and Treasury's GSDM", and the GSDM domain-value tab names grants.gov/data-standards as "The authoritative source for these codes" [F]. Element names may differ in v3.0 itself (P-B4013-03-01).
   - **IRS**: Instructions for Schedule I (Form 990) (Rev. 12/2024) and Instructions for Schedule D (Rev. 12/2024), HTML on irs.gov.
2. **Part B sources.**
   - The DAFRC panel (`dafrc-sponsor-schedule-d-fy2019-2024.csv`) and the R1–R4 corrections (`dafrc-corrections-itemized.csv`, `dafrc-corrected-market-totals.csv`, `dafrc-market-accounts-restated.csv`) [R].
   - 12 Form 990 XML returns from the GivingTuesday mirror (bucket `gt990datalake-rawdata`), chosen from the repo harvest files and checked against the IRS e-file index `index_2025.csv` (all seven 2025 index rows for the five EINs were found, including Givinga's two CY2024 returns) [F].
   - First-party processor pages: For Good's charitable-solicitation disclosures, Givinga's Solutions page, Blackbaud's NPOconnect and GrantsConnect help pages on the Blackbaud Giving Fund, Benevity's Software and Service Information (Disbursements) PDF (© 2024), and Microsoft's Give with Bing help page (which describes the AOGF route).
3. **Fetching.** A stdlib fetcher (scratchpad `q1303/scripts/get.py`, user agent `research-script/1.0`, never changed) read each host's robots.txt first and fetched a URL only if both `*` and that agent were allowed. A 404 robots.txt counted as no rules. Any other failure to read robots.txt counted as blocked. Three web searches were used to find URLs only; nothing quoted comes from a search snippet except where tagged [S].
4. **Extraction and checks.** The build script reads Schedule D Part I lines 1–4 (columns a and b), the return header and the amended flag from each XML. It checks **60 quotes** in the two CSVs against the cached sources after normalising whitespace and quote marks: **60 found, 0 missing** [C]. Two runs give byte-identical CSVs (md5 `784e7dab…` for the schema map, `9164a0e6…` for the processor file).
5. **Coding (Part A).** For each schema and field, `*_status` records whether the field is required, optional, returned or absent. `form990_requires` is `yes`, `partial` or `no`, with the instruction quoted.
6. **Coding (Part B).** `account_unit` describes what one counted item is, from the filer's own words first and the processor's site second. Units inferred from size alone are tagged [I]. `count_in_account_stats` answers the queue question per row.

## 2. Robots and access log (2026-11-19)

39 requests: 32 fetched with 200; 3 not fetched because robots.txt could not be read; 2 allowed but answered 403; 2 allowed or rule-free but answered 404 [C].

| Host | robots.txt | Result |
|---|---|---|
| docs.givechariot.com | 200, allowed | 3 × 200 |
| docs.endaoment.org | 200, allowed | 200 |
| standard.threesixtygiving.org | 200, allowed | 2 × 200 |
| **www.grants.gov, grants.gov** | **not readable**: TLS verification failed through the session proxy ("unable to get local issuer certificate") | **not fetched [B]**. TLS checking was not disabled |
| tfx.treasury.gov; fiscal.treasury.gov | 200, allowed | GSDM RSS v1.3 (200); GSDM page (200); one wrong-host link (404) |
| datafoundation.org | 200, allowed | 200 (GDS v3.0 fact sheet) |
| api.usaspending.gov | 404 | 200 (data dictionary; not used in the map) |
| www.irs.gov | 200, allowed | i990si (HTML and PDF), i990sd: 3 × 200 |
| apps.irs.gov | 404 | 200 (`index_2025.csv`) |
| gt990datalake-rawdata.s3.amazonaws.com | 404 | 12 × 200 (990 XML) |
| www.forgood.org, www.givinga.com, go.benevity.com, support.microsoft.com | 200, allowed | 200 |
| webfiles-sc1.blackbaud.com | 404 | 2 × 200; 1 × 404 (guessed URL) |
| **causeshelp.benevity.org** | 200, allowed | **403** |
| **www.paypal.com** | 200, allowed | **403** (Donor Account Policy), not retried |

crt.sh, certspotter and sec.gov were not used.

---

## 3. Results (A): the schema map

### 3.1 Field by field

Full rows, with every quote, are in the CSV. "—" means the schema has no such field.

| Core field | Chariot DAFpay (sponsor spec) | Endaoment async grant (OAS 4.88.0) | 360Giving 1.4 | Federal core (GSDM v1.3 FABS) | Form 990 |
|---|---|---|---|---|---|
| **grant_id** | sponsor returns `id` (e.g. `grant_3kd02`); Chariot's own id goes in `note` | `id` (uuid) returned | `id`, required | `FAIN` (conditional) | — |
| **fund_id** | `fund_id` (from `GET /funds`) | `originFundId`, required | — (funder and `grantProgramme` only) | — (agency, office, `AssistanceListingNumber`) | — (Sched D line 1 counts funds) |
| **recipient** | `ein`, or an org id resolved from EIN: "Chariot identifies every nonprofit by its EIN." | `destinationOrgId` (Endaoment uuid), required; EIN in responses | `recipientOrganization/0/id` (org-id), required | `AwardeeOrRecipientUEI` (UEI, not EIN) | **Sched I col (b) EIN** |
| **amount** | `amount`, "integer cents in USD" | `requestedAmount`, required, **USDC smallest unit** | `amountAwarded` + `currency`, required | `FederalActionObligation` | **Sched I col (d)**: annual total per recipient |
| **purpose_code** | `purpose` (free text) | `purpose`, required, free text, maxLength 511 | `classifications/0/{vocabulary, code}` | `AssistanceListingNumber` + `AwardDescription` | **Sched I col (h)**: free text |
| **anonymity** | `anonymous` (boolean) | `shareMyEmail` (boolean, default false); optional `recommender` name | — (recipient individuals are anonymised; no donor) | — (`RecordType` 3 redacts *recipient* PII) | — |
| **status** | `pending`, `approved`, `paid`, `rejected`, `canceled` | `asyncStatus`: `PendingLiquidation`, `Liquidated`, `Cancelled` (`status` deprecated) | — (dates and transactions only) | `ActionType` (new, continuation, termination, closeout…) | — |
| **payment_reference** | Chariot id in `note` "must appear on the grant letter / remittance advice sent to the nonprofit" | `transactionHash` (nullable) | `disbursementTransaction/0/id` | — | — |

**Counts [C]** (core fields present as a field, not implied):
- Chariot 8 of 8 (payment reference only as a copied id); Endaoment 8 of 8 (anonymity partial); 360Giving 5 of 8; federal core 5 of 8; Form 990 public return 1 full (EIN) and 2 partial (annual amount, free-text purpose).
- **Recipient identity is the main incompatibility.** Chariot and Form 990 key on EIN; Endaoment on its own uuid (EIN returned); 360Giving on an org-id scheme; the federal standard on UEI. An open DAF record should use EIN, written as an org-id (`US-EIN-#########`) so that it can sit beside 360Giving data.
- **Purpose is coded only outside the DAF world.** Both DAF APIs and Schedule I carry free text. Schedule I asks for specifics ("Don’t use general terms, such as charitable, educational, religious, or scientific"), yet the repo's Schedule I panel found one boilerplate string across whole sponsors ([b40n13-01-grant-purpose-panel.md](b40n13-01-grant-purpose-panel.md)) [R].

### 3.2 Draft minimal open DAF grant record [I]

```json
{
  "schema_version": "0.1",
  "grant_id": "US-EIN-000000000:G-2026-000123",
  "sponsor_id": "US-EIN-000000000",
  "fund_id": "F-7Q2K9",
  "recipient_ein": "000000000",
  "amount": {"value": 25000, "currency": "USD"},
  "purpose_code": {"vocabulary": "<open purpose vocabulary>", "code": "<code>"},
  "purpose_text": "Wherever needed most",
  "anonymity": "name_only",
  "status": "paid",
  "payment_reference": {"rail": "ach", "reference": "<ACH trace or check number>", "paid_date": "2026-06-12"},
  "dates": {"recommended_at": "2026-06-10T14:30:00Z", "approved_at": "2026-06-11T09:12:00Z"}
}
```

Design notes:
- **Identifiers.** `grant_id` and `fund_id` are sponsor-scoped and opaque, so a record can be shared with a charity without naming the donor. Prefixing with the sponsor's EIN follows 360Giving's prefix rule ("Made up of your 360Giving prefix, and an identifier from your records").
- **Amount.** Integer minor units with an explicit currency avoid the three unit conventions found (cents, USDC micro-units, whole currency).
- **Anonymity.** Three values, because the published disclosure outcomes are three-way (Fidelity's 80/15/5 split; [b4013-b4428-sponsor-published-grant-stats.md](b4013-b4428-sponsor-published-grant-stats.md)) [R]. Neither API boolean can express "name only".
- **Status.** Chariot's five values plus `returned`, because the repo's complaint corpus shows voided and reissued checks as a distinct state ([gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md) §5.2) [R].
- **Payment reference.** The rail's own reference is the field the remittance study found missing everywhere: no top-10 sponsor documents a grant id in ACH addenda (wave-39A scope). With `grant_id` in an ACH CCD addenda record (80 characters, per Nacha; repo DS22) or the rail reference in the record, a bank line could be matched without an out-of-band file [I].
- **Free text is untrusted.** `purpose_text` and `restriction_text` are attacker-writable fields (F15 in [ai-governance-failure-modes.md](ai-governance-failure-modes.md)) [R], so the coded field is the one systems should act on.

### 3.3 What Form 990 Schedule I already requires (IRS Instructions for Schedule I, Rev. 12/2024)

| Draft field | Required on Form 990? | IRS instruction text [F] |
|---|---|---|
| recipient_ein | **Yes**, per recipient over the threshold | Column (b): "Enter the employer identification number (EIN) of the grant recipient." |
| amount | **Partly**: one annual total per recipient, cash and noncash separately | Column (d): "Enter the total dollar amount of cash grants to each recipient organization or entity for the tax year. Cash grants include grants and allocations paid by cash, check, money order, electronic fund or wire transfer, and other charges against funds on deposit at a financial institution." |
| purpose_code | **Partly**: free-text description, no code list | Column (h): "Describe the purpose or ultimate use of the grant funds or other assistance. Don’t use general terms, such as charitable, educational, religious, or scientific." |
| grant_id, fund_id, anonymity, status, payment_reference | **No** | No column asks for them. Schedule D Part I line 1 counts funds ("Report in column (a) the total number of donor advised funds"), but does not identify them. |

Scope limits in the same instructions: "Enter information only for each recipient domestic organization or domestic government that received more than $5,000 aggregate of grants or assistance from the organization during the tax year", and "Don’t report on this schedule foreign grants or assistance" [F]. So even the three Schedule I fields cover only domestic recipients above $5,000 a year, aggregated by recipient, not by grant.

---

## 4. Results (B): processor account counts

### 4.1 Reconciliation, return by return

From the CSV [C/F]. Values per account divide filed Schedule D dollars by the filed line 1 count (for Blackbaud CY2024, by DAFRC's imputed 460).

| Row | Processor, period end | DAFRC value (flag) | Filed col (a) / col (b) | Grants per account | Year-end value per account | Return (filed) |
|---|---|---|---|---|---|---|
| PA-01 | AOGF, 2024-03-31 | 720,545 (IRS 990) | 720,545 / 3 | $2,706.60 | $368.60 | 202530159349302758 (2025-01-15) |
| PA-02 | AOGF, 2025-03-31 (amended) | — | 710,352 / 1 | $2,990.23 | $225.63 | 202641969349302754 (2026-07-15) |
| PA-03 | AOGF, 2026-03-31 | — | **695 / 751,746** | $2,000,031.51 (col a) | $295,929.98 (col a) | 202642259349301349 (2026-08-13) |
| PA-04 | PPGF, 2023-12-31 | 665,764 (IRS 990) | 665,764 / — | $744.83 | $170.15 | 202422999349301487 |
| PA-05 | PPGF, 2024-12-31 | **694,979 (Imputed)** | **380,644** / — | $2,090.35 | $254.87 | 202533079349301308 (2025-11-03) |
| PA-06 | Givinga, 2023-12-31 | 955,569 (IRS 990) | 955,569 / — | $14.14 | $2.27 | 202403139349303260 |
| PA-07 | Givinga, 2024-12-31 (original) | 1,421,011 (paper submission) | **blank** | — | — | 202522379349301497 (2025-08-25) |
| PA-08 | Givinga, 2024-12-31 (amended) | 1,421,011 (paper submission) | **1,421,011** / — | $8.74 | $1.37 | 202503179349301975 (2025-11-13) |
| PA-09 | Blackbaud GF, 2022-12-31 | 359 (IRS 990) | 359 / — | $1,899,772.93 | $196,682.80 | 202312409349300046 |
| PA-10 | Blackbaud GF, 2024-12-31 | **460 (Imputed)** | **blank** | $1,201,279.18 (on 460) | $127,714.97 (on 460) | 202542169349301664 (2025-08-04) |
| PA-11 | Blackbaud GF, 2025-12-31 | — | blank | — | — | 202622529349301602 (2026-09-09) |
| PA-12 | For Good, 2024-12-31 | 1 (Imputed) | **1 / 0** | $199,763,919 | $50,424,312 | 202513039349301631 (2025-10-30) |

What the reconciliation shows:
- **AOGF:** DAFRC equals the filing. The DAFRC "FY2024" row is the year ended **31 March 2024**, not March 2025.
- **PPGF:** DAFRC's imputed 694,979 is superseded by the filed 380,644. The repo's R1 rule already applies this ([`dafrc-corrections-itemized.csv`](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv)) [R]. The filed series jumps around: 275,052, then 665,764, then 380,644 for CY2022–24.
- **Givinga:** DAFRC's "paper submission" value equals an **e-filed amended return**. The original return left Part I blank. The amendment changes only Schedule D Part I ([queue-batch36-metrics-rails.md](queue-batch36-metrics-rails.md)) [R].
- **Blackbaud:** no count has been filed since CY2022, while the DAF dollar lines are filed every year. DAFRC's 460 is an imputation. The R1 corrections keep it because there is no filed value to replace it with [R].
- **For Good:** filed 1 in every year 2019–2023 (DAFRC panel) and in its CY2024 return (202513039349301631); DAFRC’s FY2024 row is imputed from the 2023 return [V wave 40A] DAFRC's imputed FY2024 value equals the filing.

### 4.2 The processors' own descriptions [F]

- **AOGF (Benevity).**
  - FYE 2024 Schedule D note: "AOGF HAS A MICRODONATION DAF MODEL VERSUS A CONVENTIONAL DAF ENDOWMENT MODEL."
  - FYE 2025 (amended): "AOGF HAS A WORKPLACE GIVING MODEL, WHICH INCLUDES CORPORATE AND INDIVIDUAL DONATIONS (INCLUDING MICRO-DONATIONS) AND VARIOUS FUND STRUCTURES THAT ARE NOT CONVENTIONAL DAF MODELS."
  - FYE 2026 Schedule O: corporate donors "PROVIDE ONGOING ADVICE"; individual donors give "WITHOUT ONGOING ADVISORY PRIVILEGES".
  - Benevity's Software and Service Information lists "American Online Giving Foundation, Inc." as its United States foundation. It defines a "Corporate Donor Advised Fund" as a client's advance payment to the Foundation "on account of future Donation Funding Amounts". This closes the repo's open point that AOGF's link to Benevity was "commonly reported" but not verified.
  - Microsoft's Give with Bing page: "Your donation will be made to a donor advised fund at America Online Giving Foundation (AOGF), through the services of Benevity, with a recommendation that they make a corresponding grant to the nonprofit you choose."
- **PayPal Charitable Giving Fund.**
  - CY2024 Part III: "THROUGH OUR PARTNERSHIPS, WE MAKE IT EASY FOR DONORS TO SUPPORT THE CHARITIES THEY CARE ABOUT ON THE WEBSITES AND APPS THEY USE EVERY DAY."
  - The return has no wording on the account basis. The Donor Account Policy returned 403 [B].
- **Givinga.**
  - CY2024 Part III: "THE GIVINGA FOUNDATION IS A SPONSORING ORGANIZATION BUILT AND DESIGNED TO SUPPORT THE CHARITABLE GIVING ACTIVITIES OF ALL ITS INDIVIDUAL ACCOUNT HOLDERS EQUALLY."
  - Solutions page: "Separate corporate and employee accounts."; "Optional individual employee accounts"; "Employees can view live balances"; "Built on proprietary DAFs".
- **Blackbaud Giving Fund.**
  - CY2024 Part III: "THE BLACKBAUD GIVING FUND HARNESSES THE POWER OF CORPORATE GIVING TO MAKE GRANTS FROM DONOR ADVISED FUNDS" and "ALSO MAKES GRANTS FROM DONOR ADVISED FUNDS THAT SUPPORT PEER TO PEER CHARITABLE GIVING CAMPAIGNS."
  - Blackbaud help: "a 501(c)(3) that disburses charitable donations from individuals and companies directly to nonprofit organizations around the world."
  - CY2025 Schedule O: employee donations through CSRconnect "SHOULD NOT BE TREATED BY BBGF AS CONTRIBUTIONS TO DONOR ADVISED FUNDS". The CY2025 return still reports $543.8m of DAF contributions in column (a) [F], so which flows moved is not visible.
- **For Good.**
  - Disclosures: "By donating on our website or partner sites, you are contributing to a donor-advised fund at ForGood, Inc., d/b/a ForGood (“ForGood”)". Also: "Donations to a ForGood donor advised fund can only be used for charitable purposes".
  - CY2024 Part III: "GIVING TO AND RECOMMENDING GRANTS FROM OUR DONOR ADVISED FUND".

### 4.3 Should processors count in account-level statistics?

**No, not pooled with sponsors.** Line 1 asks for "the total number of donor advised funds". The IRS definition requires a fund "separately identified by reference to contributions of a donor or donors" with advisory privileges "because of the donor's status as a donor" (i990sd) [F]. Each processor answers that differently:

| Unit counted | Processors | Comparable with sponsor accounts? |
|---|---|---|
| One account per individual donor at a checkout or workplace | AOGF (FYE 2024–25), PPGF, Givinga | No. AOGF itself says its individuals lack ongoing advice; Givinga's averages ($1.37) show enrolment; PPGF's advice basis is unverified |
| One fund per employer or campaign program | Blackbaud [I]; AOGF FYE 2026 column (a) (695) | Closer to sponsors' corporate DAFs, but Blackbaud files no count |
| One pooled fund for all donors | For Good (1) | No. It is a fund count; the donor count is not filed |

Recommended treatment [I]:
1. **Market account totals:** report sponsors and processors separately. The comparable FY2024 sponsor series is **786,822** (corrected total less the five processors), or **787,517** with AOGF's 695 corporate DAFs [C]. The other 17 DAFRC processors (15,912 FY2024 accounts as published; 16,037 after the R1 corrections, mainly Dechomai Asset Trust 181 → 314) are not yet classified (P-G1913-03-02). Removing all 22 processors (2,538,698 accounts, 76.7%) leaves 770,785 [V wave 40A]
2. **Averages and growth:** compute them on the sponsor series only. Processor counts swing with reporting choices (Givinga 42,307 → 1,543,203 → 955,569 → 1,421,011 for CY2021–24; PPGF 483,095 → 275,052 → 665,764 → 380,644) [R/C].
3. **Complaint rates:** use per-$ granted, or per grant where a count exists, for processors. Do not use per-account rates.
4. **Dollars:** keep processors in contribution, grant and asset totals. Flag AOGF's FYE 2026 and BBGF's CY2025 basis changes as breaks in the series (P-G1913-03-03).

---

## 5. Limits

- **The federal standard itself was not read.** grants.gov failed TLS verification through the proxy, so its robots.txt and the v3.0 JSON schemas were not fetched. The federal column rests on GSDM v1.3 FABS. Element names are exact for GSDM; equivalence with GDS v3.0 is [I], supported by the Data Foundation fact sheet and GSDM's pointer to grants.gov as the authority for codes.
- **Chariot's shapes are recommendations.** The page says "Chariot does not require you to implement an exact API specification", so a sponsor's live fields may differ.
- **Endaoment fields are from the published OpenAPI**, not from calls. The OpenAPI version changed between 2026-11-15 (4.87.0, repo) and today (4.88.0).
- **360Giving 1.4.** The reference page read is the "latest" docs. That 1.4 is current rests on the repo's forum citation (DS25) [R]. No version string was found on the two pages read.
- **Processor units are partly inferred.** Blackbaud's unit (employer and campaign programs) is [I] from its own text and from the ratio of dollars to funds. PPGF's ongoing-advice status rests on a 403 page ([S] in the repo). Which Givinga population the 1.42m covers (employees, app users, other) is not stated in any filing.
- **Five of 22 processors.** The remaining 17 DAFRC processors were not classified. The 786,822 comparable figure removes only the five; the other 17 hold 16,037 corrected FY2024 accounts. The sponsor side also holds mass low-balance accounts: the repo’s A3 variant (AOGF restated, then sponsor-years with at least 5,000 accounts and average year-end value under $500 removed) gives 750,473, so a unit-based screen should accompany the DAFRC type label [V wave 40A]
- **No new market totals were published.** The corrected FY2024 total (3,309,483) is the repo's R1–R4 value [R]. The script only subtracts.

---

## 6. Exact corrections

### `research/mission-2026-11-14/gap19-complaints-with-denominators.md`

- **Find:** "AOGF's 720,545 (IRS 990) almost certainly counts workplace donor accounts."
- **Replace with:** "AOGF’s 720,545 is its filed Schedule D Part I line 1 for the year ended 31 March 2024, where its own note says “AOGF HAS A MICRODONATION DAF MODEL VERSUS A CONVENTIONAL DAF ENDOWMENT MODEL.” Its FYE 2026 return splits the same population into 695 DAFs and 751,746 other accounts whose individual donors recommend grants “WITHOUT ONGOING ADVISORY PRIVILEGES”, so the 720,545 are individual workplace donor accounts. Blackbaud Giving Fund filed no line 1 count for CY2023–CY2025 (DAFRC’s 460 is imputed; the last filed count is 359 for CY2022), and its funds are employer and campaign programs [I]. For Good’s 1 is filed and counts one pooled fund that every donor gives through, so its per-account rate is undefined rather than implausible (b40n13-03-g1913-03 §4) [g1913-03]"

- **Find:** "- **DAFRC FY2024 timing** means fiscal years ending in 2024 or early 2025 (AOGF's year ends 31 March)."
- **Replace with:** "- **DAFRC FY2024 timing** means fiscal years ending in calendar 2024; imputed rows carry the prior year’s end date. AOGF’s year ends 31 March, so its FY2024 row is the year ended 31 March 2024 (return 202530159349302758), not a year ending in early 2025 [g1913-03]"

- **Find:** "| PPGF | 380,644 | 0.10 | 4.64 |"
- **Replace with:** "| PPGF | 380,644 (consumer donor accounts; not comparable with sponsor accounts) | n/c | 4.64 [g1913-03]"

- **Find:** "- **Denominator quality.** Two of the five processor account counts are imputed or implausible."
- **Replace with:** "- **Denominator quality.** One of the five processor account counts has no filed value (Blackbaud Giving Fund, DAFRC-imputed 460), and none of the five counts the same unit as sponsors: AOGF, PPGF and Givinga count individual donor accounts, Blackbaud counts employer and campaign programs [I], and For Good’s filed 1 is one pooled fund. Per-account rates for processors should be read as not comparable (b40n13-03-g1913-03 §4.3) [g1913-03]"

### `research/mission-2026-11-14/queue-batch38-data-followups.md`

- **Find:** "Givinga's 1,421,011 accounts average $8.73 (EOY $12.4m)."
- **Replace with:** "Givinga’s 1,421,011 accounts average $8.74 of CY2024 DAF grants ($12.4m) and $1.37 of year-end value ($1.95m); the $12.4m is grants, not EOY value [g1913-03]"

### `research/mission-2026-11-14/regulation-market-structure-portability.md`

- **Find:** "| Givinga Foundation (47-4172718) | 1,421,011 | $1.95M | paper submission |"
- **Replace with:** "| Givinga Foundation (47-4172718) | 1,421,011 | $1.95M | DAFRC: paper submission. The same count is in the e-filed amended CY2024 return of 2025-11-13 (202503179349301975); the original of 2025-08-25 left Part I blank [g1913-03]"

- **Find:** "| 694,979 | $151.2M | **Imputed** (last FYE Dec 2023) |"
- **Replace with:** "| 694,979 | $151.2M | **Imputed** (last FYE Dec 2023). The filed CY2024 return (202533079349301308) reports 380,644 accounts and $97.0M, which replace the imputation under R1 [g1913-03]"

- **Find:** "- **Sensitivity 2: also drop PayPal's imputed count.**"
- **Replace with:** "- **Sensitivity 2: also drop PayPal’s count** (imputed 694,979 as published; corrected work should use the filed 380,644) [g1913-03]"

- **Find:** "We did not verify that American Online Giving Foundation is the Benevity-affiliated entity; it is commonly reported as such."
- **Replace with:** "Benevity’s Software and Service Information lists “American Online Giving Foundation, Inc.” as its United States foundation, and AOGF’s FYE 2024 return calls its model a “MICRODONATION DAF MODEL” (b40n13-03-g1913-03 §4.2) [g1913-03]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "   - **Uncertainty:** Givinga's account unit is undefined **[V wave 5]**;"
- **Replace with:** "   - **Uncertainty:** Givinga describes its accounts only as those of “INDIVIDUAL ACCOUNT HOLDERS” and offers employers “Optional individual employee accounts”; at $1.37 of year-end value per account (CY2024), the count measures enrolment, not active advising [g1913-03]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "about 66% (59.2% on corrected data) if Givinga, whose account unit is undefined, is excluded (§11.1)"
- **Replace with:** "about 66% (59.2% on corrected data) if Givinga, whose 1.42m self-described individual and employee accounts average $1.37 of year-end value, is excluded (§11.1). None of the five largest processors counts the same unit as sponsors, so processor accounts belong in a separate series (b40n13-03-g1913-03 §4.3) [g1913-03]"

- **Find:** "- Givinga's account unit is undefined [V wave 5]."
- **Replace with:** "- Givinga’s filings define its account unit only as “INDIVIDUAL ACCOUNT HOLDERS” (CY2024 990 Part III), and its site offers employers “Optional individual employee accounts”; which population the 1,421,011 count covers is still unconfirmed [g1913-03]"

### `research/mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md`

- **Find:** "- Any FY2022-2024 national DAF *account* total or processor-share figure that includes Givinga moves by about 1.0-1.5m accounts on an undefined unit."
- **Replace with:** "- Any FY2022-2024 national DAF *account* total or processor-share figure that includes Givinga moves by about 1.0-1.5m accounts of a unit Givinga describes only as individual (and optional employee) giving accounts, averaging $1.37 of year-end value in CY2024 [g1913-03]"

---

## 7. Data dictionaries

### 7.1 `daf-grant-schema-map-2026-11-19.csv` (12 rows)

| Column | Meaning |
|---|---|
| `row_id` | SM-01 to SM-12 |
| `record_field` | Field of the draft open DAF grant record |
| `tier` | `core` (the eight fields in the queue item) or `supporting` |
| `proposed_type`, `proposed_definition` | Draft type and definition [I] |
| `chariot_field`, `chariot_status` | Field in Chariot's DAFpay OAuth sponsor spec (v2026-04-01) and whether it is required, returned or absent |
| `endaoment_field`, `endaoment_status` | Field in Endaoment's async-grant OpenAPI (4.88.0) |
| `g360_field`, `g360_status` | Field name (JSON path) in the 360Giving standard and its required flag |
| `federal_field`, `federal_status` | GSDM v1.3 FABS element (core lineage of Grants Data Standards v3.0) and its Required/Optional value |
| `form990_location`, `form990_requires` | Where Form 990 asks for the field; `yes`, `partial` or `no` |
| `form990_quote`, `form990_source` | Verbatim IRS instruction text, and the instructions page it is from (i990si or i990sd) |
| `gap_note` | Main incompatibility across schemas |
| `chariot_quote`, `endaoment_quote`, `g360_quote`, `federal_quote` | Verbatim evidence for the field (verified against the cached source; for the federal column, the element label in the GSDM workbook) |
| `source_urls`, `retrieved` | Sources and read date |

### 7.2 `processor-account-counts-2026-11-19.csv` (12 rows)

| Column | Meaning |
|---|---|
| `row_id`, `entity`, `ein`, `role` | Row id (PA-01 to PA-12), processor, EIN, and why the return is in the file |
| `tax_period_end`, `return_object_id`, `return_ts`, `amended` | From the XML header |
| `dafrc_fiscal_year`, `dafrc_number_of_daf_accounts`, `dafrc_source_number_of_accounts` | The matching DAFRC panel row (blank for context rows) |
| `filed_l1_col_a_daf_count`, `filed_l1_col_b_other_count` | Schedule D Part I line 1, columns (a) and (b) (`DonorAdvisedFundsHeldCnt`, `FundsAndOtherAccountsHeldCnt`); blank = not filed |
| `filed_daf_contributions`, `filed_daf_grants`, `filed_daf_eoy_value` | Lines 2–4, column (a), US$ |
| `dafrc_minus_filed` | DAFRC value less filed column (a) |
| `grants_per_account`, `eoy_value_per_account` | Filed column (a) dollars ÷ filed count; for PA-10, ÷ DAFRC's imputed 460 |
| `account_unit`, `unit_basis` | What one counted item is, and what that rests on |
| `self_description_quote`, `self_description_source` | Verbatim processor text (XML or web page) |
| `count_in_account_stats`, `recommended_treatment` | Answer to the queue question for this row |
| `evidence_label`, `xml_url`, `retrieved` | F/I label, GivingTuesday mirror URL, read date |

---

## 8. Source register

| ID | Source | Read | Used for |
|---|---|---|---|
| S1 | [Chariot DAFpay OAuth: API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md); [overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md); [integration checklist](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/integration-checklist.md) | 2026-11-19 | §3 |
| S2 | [Endaoment: Create async grant](https://docs.endaoment.org/developers/api/transfers/create-an-async-grant-request.md) (embeds `https://api.endaoment.org/oas-json`, version 4.88.0) | 2026-11-19 | §3 |
| S3 | [360Giving Data Standard: technical reference](https://standard.threesixtygiving.org/en/latest/technical/reference/); [home](https://standard.threesixtygiving.org/en/latest/) | 2026-11-19 | §3 |
| S4 | [Grants.gov data standards](https://www.grants.gov/data-standards) | not read (TLS) [B] | §2, §5 |
| S5 | [GSDM v1.3 Reporting Submission Specification (xlsx)](https://tfx.treasury.gov/system/files/2026-11/gsdm-rss-v1.3.xlsx); [GSDM page](https://fiscal.treasury.gov/data-transparency/GSDM-current.html) | 2026-11-19 | §3 federal column |
| S6 | [Data Foundation, Fact sheet: Grants Data Standards under the GREAT Act](https://datafoundation.org/news/blogs/870/870-FACT-SHEET-Grants-Data-Standards-Under-the-GREAT-Act) | 2026-11-19 | §1, §5 |
| S7 | [IRS Instructions for Schedule I (Form 990), Rev. 12/2024](https://www.irs.gov/instructions/i990si) ([PDF](https://www.irs.gov/pub/irs-pdf/i990si.pdf)) | 2026-11-19 | §3.3 |
| S8 | [IRS Instructions for Schedule D (Form 990), Rev. 12/2024](https://www.irs.gov/instructions/i990sd) | 2026-11-19 | §0 B, §4.3 |
| S9 | [IRS e-file index 2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv) | 2026-11-19 | §1 |
| S10 | 990 XML, GivingTuesday mirror: AOGF [202530159349302758](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202530159349302758_public.xml), [202641969349302754](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml), [202642259349301349](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml); PPGF [202422999349301487](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202422999349301487_public.xml), [202533079349301308](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml); Givinga [202403139349303260](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml), [202522379349301497](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522379349301497_public.xml), [202503179349301975](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml); Blackbaud GF [202312409349300046](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202312409349300046_public.xml), [202542169349301664](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542169349301664_public.xml), [202622529349301602](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml); For Good [202513039349301631](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml) | 2026-11-19 | §4 |
| S11 | [For Good: charitable solicitation disclosures](https://www.forgood.org/legal-pages/charitable-solicitation-disclosures) | 2026-11-19 | §4.2 |
| S12 | [Givinga: Solutions](https://www.givinga.com/solutions) | 2026-11-19 | §4.2 |
| S13 | [Blackbaud NPOconnect: About the Blackbaud Giving Fund](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-about-blackbaud-giving-fund-bbgf.html); [GrantsConnect page](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-resources-payment-bbgf.html) | 2026-11-19 | §4.2 |
| S14 | [Benevity Software and Service Information: Disbursements (PDF, © 2024)](https://go.benevity.com/hubfs/website/legal/Benevity-SSI-Disbursements.pdf) | 2026-11-19 | §4.2 |
| S15 | [Microsoft: Cash donations on Bing](https://support.microsoft.com/en-us/bing/cash-donations-on-bing) | 2026-11-19 | §4.2 |
| S16 | [PayPal Giving Fund Donor Account Policy](https://www.paypal.com/us/webapps/mpp/givingfund/policies/donor-account-policy): 403 [B]; [causeshelp.benevity.org article](https://causeshelp.benevity.org/hc/articles/360001149426): 403 [B] | 2026-11-19 | §2 |
| S17 | [DAFRC Updated Analysis dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx), via repo `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrections-itemized.csv`, `dafrc-corrected-market-totals.csv`, `dafrc-market-accounts-restated.csv` [R] | repo | §4 |
