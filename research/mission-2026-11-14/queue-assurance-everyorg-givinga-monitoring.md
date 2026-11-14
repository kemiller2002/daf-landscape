# Queue answers: vendor assurance scope (P-QA1-04), Every.org filings and rails (P-QA2-04), Givinga account count (P-INF-01), terms monitor (P-PAY-07)

**Date:** 2026-11-14.

**Status:** Desk research from public sources only:
- IRS e-file XML;
- first-party web pages and trust-center pages;
- public PDFs.

No reports were requested, no accounts were created and nobody was contacted. Trust-center documents behind "Request access" were **not** opened. Only the public metadata of those pages was read (titles, framework badges and auditor fields embedded in the page data).

**Data files:**
- [data/mission-2026-11-14/vendor-assurance-scope-2026.csv](../../data/mission-2026-11-14/vendor-assurance-scope-2026.csv): 13 vendors, one row each.
- [data/mission-2026-11-14/terms-monitor-urls.csv](../../data/mission-2026-11-14/terms-monitor-urls.csv): 19 monitored URLs.
- [scripts/mission_terms_monitor.py](../../scripts/mission_terms_monitor.py): the monitor (stdlib only).
- [data/terms-snapshots/](../../data/terms-snapshots/): baseline snapshots, `manifest.csv` and `reports/2026-11-14-terms-diff.md`.
- [data/mission-2026-11-14/queue-proposals-assurance-monitoring.csv](../../data/mission-2026-11-14/queue-proposals-assurance-monitoring.csv): proposals P-ASR-01..07.

**Evidence tags:**
- **[F]** is a fact from a cited source.
- **[C]** is a calculation from cited inputs.
- **[I]** is an inference.

The 990 XML links below point to the GivingTuesday 990 data-lake mirror of each IRS e-file object (`https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/<OBJECT_ID>_public.xml`). Object IDs come from the [IRS e-file index 2021-2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (the 2026 index was last modified 2026-10-21).

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-QA1-04** | **None of the 13 vendors publishes a scoped SOC report.**<br>• Five list a SOC 2 Type 2 (Type II) in a trust center or on their own security page, but give no public period or system scope: Foundant, Give Interactive, Chariot, Blackbaud, Benevity.<br>• Three rest on marketing claims only: Ren, TIFIN Give, Candid.<br>• Five show no claim at all: Foundation Source, Givinga, Daffy, Endaoment, NPact. NPact points customers to **Microsoft Azure's** reports.<br>• Give Interactive's SOC 3 exists but is **gated**, so it is not public.<br>• ISO 27001 appears only for Foundant's **SmartSimple** product (certification body BSI). Benevity says its program is "based on" ISO 27001. | High on what is public. Says nothing about whether controls work. |
| **P-QA2-04** | Every.org (EIN 61-1913297) filed **Form 990-PF for CY2020-2024**. That form has no Schedule D DAF section, so **no DAF account count or DAF balance has ever been publicly reported**.<br>• Grants paid: $0.96m (2020), $5.81m (2021), $17.43m (2022), $16.78m (2023), $44.93m (2024).<br>• Itemized grants to Network for Good (ForGood): $713k, $2.38m, $2.91m, $2.45m, $0.47m. That is **73.9% of grants paid in 2020, falling to 1.1% in 2024** [C].<br>• Current rails: Stripe Connect weekly at 0%; PayPal Grants every 4-5 weeks at 0%; ForGood every 4-6 weeks at 1.5%.<br>• No volume by rail is published.<br>• Every.org says the IRS confirmed public-charity status on 2025-10-23. No CY2025 Form 990 is in the IRS index yet. | High on the filings. Low on rail volumes. |
| **P-INF-01** | **The account count is not a stable unit.**<br>• Givinga Foundation's Schedule D series is 26,557 → 3,459 (CY2020 original → amended), 42,307 (CY2021, added only by amendment), **1,543,203 (CY2022)**, 955,569 (CY2023), and 1,421,011 (CY2024, added only by amendment).<br>• The CY2024 original omitted the entire Part IV checklist, not just the DAF line. The amendment says only "change in financial information… Schedule D Part I". The same omit-then-amend pattern happened for CY2021.<br>• Givinga's documents describe employer-created employee accounts, "optional individual employee accounts", no minimum to open, and per-employee-per-month pricing.<br>• **[I]** The 1.4m most plausibly counts employee accounts provisioned by employer programs, most with near-zero balances ($1.37 average). | High on the series. Medium on the explanation. No primary definition found. |
| **P-PAY-07** | Monitor built and baseline run.<br>• **18 of 19 URLs were snapshotted** with sha256 hashes.<br>• NPact Standard Terms: the connection was closed (`RemoteDisconnected`). It was recorded and not retried.<br>• **[F]** The Daffy Member Agreement (updated 2025-11-11) contains no "MCP" or "artificial intelligence" term, although Daffy's MCP server has been live since 2026-09-28. | High |

---

## 1. P-QA1-04: public assurance scope for 13 vendors

### 1.1 Method and classification

For each vendor I checked:
- `trust.` and `security.` subdomains (with a headless browser for JavaScript trust centers);
- first-party security pages and help centers;
- the vendor's own and partner press releases;
- web search, filtering out name collisions.

Each vendor gets one of four classes:

| Class | Rule |
|---|---|
| `scoped_report_public` | A SOC 3 or SOC 2 report, or a certificate, can be downloaded without an access request, and it states the period and system |
| `type_stated_without_scope` | A first-party trust center or security page names the report type (e.g. "SOC 2 Type 2"), but the period and system scope are not public |
| `vendor_claim_only` | The claim appears only in marketing or press material, sometimes with a type, and there is no trust center or report listing |
| `none_found` | No assurance claim found in first-party material |

Absence is **not** evidence that a report does not exist (per [quadrant-calibration.md](quadrant-calibration.md): absence = U).

### 1.2 Results

| Vendor | Class | What is public | Auditor named | Subservice orgs | Contradiction |
|---|---|---|---|---|---|
| Ren | vendor_claim_only | "SOC 2 Type 2" in the [AEF release of 2025-07-23](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/). "SOC 2 Type 1" in the [AEF release of 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/) and the [Giving Compass release of 2026-05-13](https://www.givingcompass.org/giving-compass-and-ren-accelerate-nonprofit-impact-discovery-for-daf-advisors/). No trust center. | no | none | **Yes:** a Type 2 claim followed by Type 1 claims |
| Foundation Source | none_found | [DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/) markets "audit-ready reporting" (a product feature) | no | none | no |
| TIFIN Give | vendor_claim_only | [2024 release](https://tifin.com/news/tifin-give-expands-its-reach-as-a-leading-technology-powered-philanthropy-platform-for-wealth-enterprises-2/): "SOC-2 security compliance". The [trust.tifin.com](https://trust.tifin.com/) page is titled "TIFIN HoldCo" and shows only an access form. | no | none | Minor: holding-company trust center; product scope unknown |
| Foundant | type_stated_without_scope | [trust.foundant.com](https://trust.foundant.com/) lists SOC 2 Type 2 for "Foundant Technologies", plus separate SmartSimple and GivingData entries | Linford & Co LLP (Foundant, SmartSimple); Pease Bell CPAs (GivingData); BSI (ISO, SmartSimple) | Azure (GivingData); AWS (SmartSimple) | **Yes:** ISO 27001 and SOC 1 Type 2 appear under SmartSimple only |
| Givinga | none_found | Marketing only: "financial-grade", "audit-ready compliance" ([givinga.com/solutions](https://www.givinga.com/solutions)) | no | none | no |
| Give Interactive | type_stated_without_scope | [Trust center](https://trust.giveinteractive.com/resources): "Give Interactive LLC SOC 2 Type 2" and "Give Interactive LLC SOC 3 Report", **both behind Request access**. [BD Emerson case study](https://www.bdemerson.com/case-studies/give-interactive): both issued together in September 2025. | No. BD Emerson ran the program; the issuing CPA firm is unnamed | not disclosed | **Yes:** queue item said "public SOC 3"; it is gated |
| Chariot | type_stated_without_scope | [Trust center](https://trust.givechariot.com/) lists "2024-10 Chariot SOC 2 Type 2 Report" and "2025-12 Chariot SOC 2 Type 2 Report" (gated), plus a Q3 2026 pentest. [Security page](https://help.givechariot.com/onboarding/trust-and-safety/security): "SOC 2 Type II compliant". | no | AWS (US); program of Column N.A. | no |
| Daffy | none_found | Nothing on its site, docs or help center | no | none (Chariot disburses grants) | no |
| Endaoment | none_found | Financial-statement audits and a 2022 smart-contract audit only; the [docs corpus](https://docs.endaoment.org/llms-full.txt) has no SOC or ISO string | no | none | no |
| Blackbaud | type_stated_without_scope | [trust.blackbaud.com](https://trust.blackbaud.com/) badges: SOC 2 Type II, SOC 1 Type II, PCI, HECVAT, TX-RAMP, GovRAMP and others. 19 documents, gated. The [compliance page](https://www.blackbaud.com/compliance-certifications) has no product scope. | no | subprocessor list gated | Minor: older datasheets said SOC 1 Type 1 (search summary only) |
| NPact | none_found | [KB article](https://npact.document360.io/fims-and-donorcentral/docs/how-to-obtain-a-soc-report-for-hosted-fims-and-donorcentral) answers "how to obtain a SOC report" by pointing to Microsoft Azure's SOC 1/SOC 2 | n/a | Microsoft Azure | **Yes:** a subservice organisation's report is offered in place of an NPact report |
| Benevity | type_stated_without_scope | [Security page](https://benevity.com/security): "currently issues SOC 1 Type II and SOC 2 Type II reports". CSA STAR Level 1. PCI SAQ-A. [trust.benevity.com](https://trust.benevity.com/) was offline. | no | AWS (US); DPA sub-processor list | **Yes:** the program is "based on" ISO 27001, which is not a certificate |
| Candid | vendor_claim_only | [2023 blog](https://candid.org/blogs/building-a-culture-of-nonprofit-compliance-at-candid/): "first external SOC 2 audit". [2025 blog](https://candid.org/blogs/how-candid-ensures-data-security-safeguards/) repeats it with no type. | no | none | Minor: name collision with Candid Health |

**Notes on the table:**
- **[F]** Foundant's auditor names come from the `auditor` field of each compliance item in the SafeBase page data, which is embedded in the public HTML. They are not from opened reports.
- **[C]** Give Interactive's two trust-center resource IDs decode to an upload on 2025-10-08 (MongoDB ObjectId timestamp). This fits the September 2025 issuance.

### 1.3 Implications

1. **X3 scoring stays capped.** No vendor reaches "scoped report public".
   - Five vendors (Foundant, Give Interactive, Chariot, Blackbaud, Benevity) give named report types in first-party trust infrastructure. For Foundant and Give Interactive the issuing entity is also named.
   - **[I]** That is stronger evidence than a press-release claim, and could justify a one-step difference versus Ren and TIFIN under the calibration rules. It still does not show what the reports cover.
2. **Ren's most recent dated claim is Type 1** (2026-05-13).
   - The 2025 Type 2 claim stays unexplained.
   - Ren's public MSA templates (RAC, RCF, iPhi) contain no SOC commitment. I checked the PDF and DOCX text.
3. **Do not transfer ISO 27001 across Foundant products.** Only SmartSimple lists it. Foundant's DAF and community-foundation software lists SOC 2 Type 2 only.
4. **NPact's assurance answer is the cloud provider's.** **[I]** Under a carve-out model, Azure's report covers only the infrastructure. It does not cover NPact's FIMS or DonorCentral application controls, change management or support access.
5. **Correction to queue wording:** Give Interactive has a SOC 3, but as of 2026-11-14 it is behind an access request. A SOC 3 is a general-use report, so this is the vendor's choice, not an audit restriction.

---

## 2. P-QA2-04: Every.org's filings and disbursement rails

### 2.1 Entity and filing type

- **[F]** Every.org (EIN 61-1913297) is the legal recipient of all platform donations. It regrants to nonprofits.
- **[F]** The Every.org [tax-status article](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org) (updated 2026-08-21) says it "initially formed as a private foundation but [has] since terminated our private foundation status". It cites an IRS letter dated 2025-10-23 confirming public-charity status under 509(a)(2) / 170(b)(1)(A)(vi).
- **[F]** Every.org filed **Form 990-PF** for CY2020-2024 (IRS index rows below). Form 990-PF has **no Schedule D Part I** (DAF counts and values). So the "Schedule D DAF data" asked for in P-QA2-04 **does not exist** for any filed year.
- **[F]** The IRS 2026 index (as of 2026-10-21) has no CY2025 return for this EIN. The first Form 990 with Schedule D is still pending (P-ASR-01).
- **[F]** The help center calls donor account balances a "DAF structure": "you can make multiple smaller donations from your account balance thanks to our DAF structure" ([asset donation article](https://support.every.org/hc/en-us/articles/360058166014-How-can-I-donate-stocks-cryptocurrency-or-other-assets)). A funded balance is described as "a giving credit balance… think of it like a gift card" ([DAF article](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF)).
- **[I]** Whether these balances will be reported as DAFs on Schedule D is an open question.

### 2.2 Form 990-PF figures (IRS e-file XML)

| Tax year | Object (XML) | Revenue | Contributions received | Grants paid | Total expenses | Year-end assets (FMV) | Part XV grant rows | To Network for Good | NFG share of grants [C] |
|---|---|---|---|---|---|---|---|---|---|
| 2020 | [202141729349100004](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202141729349100004_public.xml) | $4,376,111 | $4,367,035 | $964,640 | $2,583,212 | $3,921,893 | 10 | $713,148 | 73.9% |
| 2021 | [202201479349100500](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202201479349100500_public.xml) | $8,801,096 | $8,801,096 | $5,806,498 | $7,881,911 | $5,202,463 | 52 | $2,375,859 | 40.9% |
| 2022 | [202333179349100048](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333179349100048_public.xml) | $18,478,847 | $18,459,824 | $17,427,495 | $19,354,345 | $4,245,377 | 98 | $2,905,359 | 16.7% |
| 2023 | [202423199349106002](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423199349106002_public.xml) | $20,802,349 | $20,708,532 | $16,782,740 | $18,847,697 | $6,425,934 | 223 | $2,446,497 | 14.6% |
| 2024 | [202502749349100700](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml) | $51,383,000 | $50,455,689 | $44,931,032 | $47,461,701 | $9,663,375 | 210 | $474,870 | 1.1% |

**Notes on the 990-PF figures:**
- **[F]** Network for Good is listed in Part XV with the purpose "ONLINE SUPPORT FOR CHARITABLE PURPOSES" (2024: "GENERAL SUPPORT").
- **[F]** Part XV also carries aggregate lines:
  - "GRANTS TO ALL OTHER ORGANIZATIONS" ($277,514, 2021);
  - "TOTAL PAID TO OTHER ORGANIZATIONS UNDER 5K" ($363,248, 2023);
  - "UNDER 25K" ($6,580,200, 2024).
- **[F]** PayPal Giving Fund is itemized only in 2023, at $6,201.
- **[F]** In the 2024 Schedule B, Network for Good is also a *contributor* to Every.org ($75,000). Money flows both ways.
- **[F]** Bookkeeper on all five returns: Easy Office dba Jitasa.
- **[I]** The NFG share collapses from 74% to 1% while total grants rise 47x. This fits the help center's push to "connect a bank account" (Stripe Connect, weekly, 0% fee). But Part XV itemization changed between years (thresholds of $5k, then $25k), so rail shares **cannot** be computed from the 990-PF. The table shows only itemized NFG grants.
- **[C]** Expenses other than grants (total expenses minus grants paid): $1.62m (2020), $2.08m, $1.93m, $2.06m, $2.53m (2024).

### 2.3 Inbound DAF grants (Schedule B, contributors of $5,000 or more)

990-PF Schedule B names contributors. Sums of named DAF sponsors and giving-platform funds, matched by name pattern [C]:

| Year | Total Schedule B listed | Named sponsor funds | Examples |
|---|---|---|---|
| 2020 | $3,087,398 | $65,438 | BMO Charitable Fund $30,000; Benevity Community Impact Fund $29,938; Vanguard Charitable $5,500 |
| 2021 | $6,137,577 | $595,723 | Fidelity Charitable $158,314; NPT Transatlantic $150,000; AEF $100,000; Schwab Charitable $56,600 |
| 2022 | $7,561,645 | $0 named | Top contributors are Camp.org LLC $2.08m and Block Inc $1.74m |
| 2023 | $12,631,177 | $2,260,299 | Fidelity Charitable $1,014,836; NPT Transatlantic $636,295; Schwab Charitable $210,115 |
| 2024 | $22,839,968 | $425,000 (Fidelity Charitable) | $4,022,129 is listed as "ANONYMOUS DONOR" |

**[I]** These are lower bounds on DAF-sourced revenue, and the naming practice varies by year. Do not trend them.

### 2.4 Disbursement rails (current, first-party)

| Rail | Frequency | Fee to nonprofit | Source |
|---|---|---|---|
| Stripe Connect (bank account connected) | Weekly | 0% | [Disbursements overview](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview) (updated 2026-10-23) |
| PayPal Grants (PayPal Giving Fund) | Every 4-5 weeks ("monthly… where possible") | 0% | same; [timing article](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit) |
| ForGood, Inc (Network for Good) | Every 4-6 weeks, paid on the 15th of the following month; $10 minimum | 1.50% | same; [third-party fees](https://support.every.org/hc/en-us/articles/360059998533-What-are-the-third-party-processing-fees) |

**Rail volumes:** Every.org publishes no volume by rail. No annual report was found (search 2026-11-14), and [every.org/pricing](https://www.every.org/pricing) returned 403.

**Scoring note:**
- **[I]** For A2 X1/X5, the filings now support scale: $44.9m granted in CY2024, 2.7x CY2023.
- **[I]** Durability evidence is mixed. There are strong philanthropic backers (Camp.org, Gates, Fidelity Charitable Catalyst Fund). There is no DAF-balance disclosure. The structure is a young public charity with an IRS reclassification in October 2025.

---

## 3. P-INF-01: what counts as a Givinga Foundation "account"?

### 3.1 Every Givinga Foundation return, CY2020-2024 (IRS e-file XML)

| Tax year | Filed | Amended? | Object | Sch D accounts | Sch D contributions | Sch D grants | Sch D value at year end | Org contributions (Part I) | Org grants paid | Total assets at year end | Avg value per account [C] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | 2021-11-15 | no | [202123199349306837](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202123199349306837_public.xml) | 26,557 | $4,032,088 | $2,578,426 | $939,201 | $4,032,088 | $2,893,419 | $1,364,296 | $35.37 |
| 2020 | 2023-04-07 | **yes** | [202320979349301202](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202320979349301202_public.xml) | **3,459** | $4,572,784 | $2,466,425 | $2,106,359 | $4,572,784 | $2,466,425 | $1,746,335 | $608.95 |
| 2021 | 2022-11-15 | no | [202243199349323204](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243199349323204_public.xml) | — (Part IV line 6 answered **No**; no Sch D) | — | — | — | $15,746,697 | $8,583,069 | $2,890,836 | — |
| 2021 | 2023-04-07 | **yes** | [202330979349300728](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202330979349300728_public.xml) | 42,307 | $15,846,697 | $9,358,734 | $2,523,016 | $15,846,697 | $9,358,734 | $2,876,364 | $59.64 |
| 2022 | 2023-11-15 | no | [202333199349323323](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333199349323323_public.xml) | **1,543,203** | $34,461,745 | $13,644,018 | $5,243,806 | $34,461,745 | $13,644,018 | $5,243,806 | $3.40 |
| 2022 | 2024-02-05 | yes | [202420369349301017](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202420369349301017_public.xml) | 1,543,203 | same | same | same | same | same | same | $3.40 |
| 2023 | 2024-11-08 | no | [202403139349303260](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml) | 955,569 | $17,717,457 | $13,513,967 | $2,171,271 | $18,779,903 | $13,644,252 | $2,336,575 | $2.27 |
| 2024 | 2025-08-25 | no | [202522379349301497](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202522379349301497_public.xml) | — (Part IV checklist absent; Sch D without Part I) | — | — | — | $13,040,889 | $11,091,205 | $2,917,533 | — |
| 2024 | 2025-11-13 | **yes** | [202503179349301975](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml) | **1,421,011** | $12,300,836 | $12,417,069 | $1,949,239 | $13,040,889 | $11,091,205 | $2,917,533 | $1.37 |

**Stated amendment reasons [F] (Schedule O):**

| Return | Stated reason |
|---|---|
| CY2020 amended | "AMEND TO AGREE TO THE AUDITED FINANCIAL STATEMENTS. PAGES 1-12, SCHEDULES A, D, AND O HAVE CHANGED" |
| CY2021 amended | "PART I, PART III, PART VIII, PART IX, PART X, PART XI, AND SCHEDULE A" |
| CY2022 amended | "TO AGREE WITH [T]HE AUDITED FINANCIAL STATEMENTS… PART I, PART IX, PART X, PART XI AND SCHEDULE D PART XI" |
| CY2024 amended | "CHANGE IN FINANCIAL INFORMATION. THEREFORE, THE FOLLOWING FORM HAS CHANGES: SCHEDULE D PART I" |

**What an XML diff of the two CY2024 returns shows [F]:**
- The original lacks the **whole Part IV checklist**. That includes line 6 (DAF), and also lines on audited statements, Schedule I grants, Schedule M non-cash gifts and Schedule R related entities.
- The original lacks Schedule D Part I values.
- The amendment adds those items and a Schedule O note.
- All financial totals are unchanged.

### 3.2 What Givinga's own documents say an account is

| Source | Statement [F] |
|---|---|
| [Account Holder Handbook](https://cdn.prod.website-files.com/67f91b19ba41ea3a5732646b/68502b601729bb5f3c1a7c75_Givinga-Foundation-Account-Holder-Handbook.pdf) (PDF created 2020-04-30) | Givinga, Inc. lets the Foundation "Establish and Administer Corporate, Individual and Pooled Accounts"<br>It provides "companies with the ability to make donations to their employees' Accounts"<br>"There are no minimums and no fees to establish additional Accounts"<br>A "$10 minimum balance [is] required to maintain an active grant making Account"<br>An account "below $10 and inactive for 12 months may be closed" |
| [Policies and Procedures](https://cdn.prod.website-files.com/67f91b19ba41ea3a5732646b/68502b2e2476ee92f72652ea_Givinga-Foundation-Policies-and-Procedures.pdf) (PDF created 2020-04-30) | Individuals open an account with "an initial irrevocable contribution… of $10 or more"; corporations with $1,000<br>"An Account must maintain an annual minimum balance of $100" (this conflicts with the Handbook's $10) |
| [PRWeb release, 2019-03-25](https://www.prweb.com/releases/Drive_Employee_Engagement_Through_Corporate_Philanthropy/prweb16186009.htm) | The platform "allows employers to create individual giving accounts for their employees" |
| [givinga.com/solutions](https://www.givinga.com/solutions) | "Optional individual employee accounts"; "Separate corporate and employee accounts"; "Prefunded accounts" |
| [givinga.com/why-givinga](https://www.givinga.com/why-givinga) | Charitable Savings Accounts: "Employees use them like personal giving wallets" |
| [givinga.com/pricing](https://www.givinga.com/pricing) | "Starts at $12,500 annually + PEPM (per-employee-per-month)" |
| [givingafoundation.org](https://www.givingafoundation.org/) (2026) | Products: Charitable Savings Account, Charitable Foundation Account, fiscal sponsorship (ProjectFS) and a nonprofit portal; "client giving accounts" for institutions |

### 3.3 Answer

1. **Why was CY2024 amended?**
   - **[F]** The original return was missing the Part IV checklist and all Schedule D Part I values. The financial totals did not change.
   - **[I]** The amendment most plausibly *completed an omitted section* rather than *adding newly discovered accounts*.
   - **[I]** The pattern is not new. The CY2021 original answered "No" to the DAF question and had no Schedule D. A 2023 amendment added 42,307 accounts.
   - No first-party explanation was found. No one was contacted, per scope.
2. **What counts as an account?**
   - No public definition exists.
   - **[C]** The count is 36x higher in CY2022 than CY2021, while Schedule D contributions rose only 2.2x.
   - **[C]** The average year-end value falls from $59.64 (CY2021) to $3.40, $2.27 and $1.37.
   - **[C]** Under the Foundation's own $10 active-account minimum, the average account in CY2022-2024 could not be "active".
   - **[I]** The best-supported reading is that from CY2022 the count includes accounts provisioned for every enrolled employee of client companies (employer-created, no opening minimum, priced per employee), most never funded or nearly empty. Corporate and pooled accounts may also be counted. An alternative is a reporting-system change (for example, counting user records rather than funded DAFs). The public record cannot tell these apart.
3. **Data-quality flags [C]:**
   - **Schedule D Part I has repeatedly equalled whole-organisation totals.** In CY2020 (amended), CY2021 (amended) and CY2022, Schedule D contributions and grants exactly equal the Part I totals. In CY2022, Schedule D year-end value equals total assets.
   - **Schedule D values exceed organisation totals in two years.** In CY2020 (amended), DAF value is $2,106,359 against total assets of $1,746,335. In CY2024, DAF grants are $12,417,069 against total grants paid of $11,091,205.
   - **[I]** Treat Givinga's Schedule D lines as low-reliability in any national total.

**Consequence for repo statistics [I]:**
- Any FY2022-2024 national DAF *account* total or processor-share figure that includes Givinga moves by about 1.0-1.5m accounts on an undefined unit.
- Report figures with and without Givinga (P-ASR-03).
- The existing note that "the 1.42m figure enters the record only via the November 2025 amendment" ([queue-infrastructure-nonprofit-costs-emerging.md](queue-infrastructure-nonprofit-costs-emerging.md)) is correct. It should add that **CY2022 reported 1.54m in an original, unamended filing**, so the order of magnitude is not an artefact of the 2025 amendment alone.

---

## 4. P-PAY-07: terms monitor

### 4.1 What was built

[`scripts/mission_terms_monitor.py`](../../scripts/mission_terms_monitor.py) is stdlib only, written in a functional style (pure transforms, I/O at the edges). It reads [terms-monitor-urls.csv](../../data/mission-2026-11-14/terms-monitor-urls.csv) and, for each URL:

1. **Fetches** with one honest browser-style User-Agent. It does not retry with other identities. A blocked URL is recorded and skipped, as instructed.
2. **Extracts text:**
   - HTML through `html.parser`, skipping script, style and nav;
   - PDF through `pdftotext` when installed, otherwise a stdlib FlateDecode fallback;
   - DOCX from `word/document.xml`;
   - Markdown as is.
3. **Normalizes:** unescape, unify quotes and dashes, collapse whitespace, drop empty or volatile lines (such as "Updated N minutes ago"), plus an optional per-URL `ignore_regex`.
4. **Stores** `data/terms-snapshots/<slug>/<date>.txt` and `<date>.meta.json`. The metadata holds the raw sha256, the text sha256, sizes, the extractor and watch-term counts.
5. **Compares** with the latest earlier snapshot and writes `data/terms-snapshots/reports/<date>-terms-diff.md`. The report has a status table, skipped URLs, watch-term counts, and unified diffs capped at 120 lines.
6. **Upserts** `data/terms-snapshots/manifest.csv` (one row per URL per date). Re-runs on the same date are idempotent.

Watch terms are tripwires, not semantic tests: third party, automated, agent, AI, bot/scrape, initiate, on behalf of, pass-through, aggregator, API, MCP. A change in counts is flagged even when the diff is long.

I also tested the diff path on a synthetic earlier snapshot in the scratchpad, using `--report-only`. It produced the expected unified diff and a `third_party 5->0` flag.

### 4.2 Baseline run (2026-11-14)

- **[F]** 19 URLs; **18 snapshots written** (all HTTP 200).
- **[F]** NPact Standard Terms failed with `RemoteDisconnected`: npact.com closed the connection for this client. It is recorded in the manifest and was not retried. P-ASR-04 proposes a public archive copy as the baseline.

Watch-term counts per document are in the [report](../../data/terms-snapshots/reports/2026-11-14-terms-diff.md). Notable baseline facts:

| Document | Observation |
|---|---|
| Daffy Member Agreement ("Updated November 11, 2025") | 0 matches for "MCP" and for "artificial intelligence"/AI. The 5 "agent" matches use the legal-agency sense: personal representative, "the member or their agent" in crypto-transfer risk allocation, and indemnity of "affiliates and agents". Daffy's MCP and agents docs have 7 and 12 MCP mentions. **[I]** Agent safeguards live in docs, not in the member contract (P-ASR-05). |
| Chariot nonprofit terms ("Updated: October 14, 2026") | 15 "initiate" and 8 "on behalf of" matches: payment-initiation language central to DAFpay. Baseline for future diffs. |
| Blackbaud AI Terms 2026 | 65 AI matches; 9 "third party" matches |
| Endaoment Terms and Conditions | 24 API matches. Governs "API Access" and "Partner Interfaces" |
| Fidelity Charitable EFT page and FAQs | Effectively no watch terms. These are monitored for wording changes on EFT enrollment |

**Cadence:** quarterly, as in P-PAY-07. Run `python3 scripts/mission_terms_monitor.py`; dated outputs accumulate automatically.

---

## 5. Corrections and updates to repo claims

1. **[data/assurance.csv](../../data/assurance.csv) and [soc2-assessment-2026-11-11.md](../soc2-assessment-2026-11-11.md):**
   - Chariot now has two dated Type 2 report titles (2024-10, 2025-12) in its trust center.
   - Ren's latest claim (2026-05-13) is Type 1.
   - TIFIN's trust center is a gated "TIFIN HoldCo" Vanta page.
   - Daffy: still no claim.
2. **Queue item P-QA1-04 wording:** Give Interactive's SOC 3 is not public; it is gated.
3. **Foundant:** ISO 27001 belongs to SmartSimple, not to Foundant's DAF and community-foundation product.
4. **Givinga:** the million-scale account count first appears in the **original CY2022 return** (1,543,203), not only the 2025 amendment. Four of five tax years were amended.
5. **Every.org:**
   - No Schedule D data exists for CY2020-2024 because the filings are 990-PF.
   - Public-charity status is confirmed by an IRS letter dated 2025-10-23 (per Every.org).
   - Itemized Network for Good grants fell to $474,870 in CY2024.

## 6. Limits

- Trust-center content behind access requests was not viewed. Auditor names, where given, come from public page data.
- Givinga's account definition is inferred. Massachusetts AG filings (audited statements) were not retrieved (P-ASR-02).
- Every.org rail volumes are unknown, and 990-PF itemization thresholds changed by year.
- The terms monitor's PDF extraction depends on `pdftotext` being present. The stdlib fallback is for change detection only.
- reninc.com HTML pages returned 403 to curl. The Ren PDF and DOCX templates downloaded normally.

---

## 7. Source register

| ID | Source | Used for |
|---|---|---|
| S1 | IRS e-file index [2021](https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv)-[2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | Locating Givinga Foundation (EIN 47-4172718) and Every.org (EIN 61-1913297) returns |
| S2 | IRS e-file XML via the GivingTuesday mirror: Givinga objects 202123199349306837, 202320979349301202, 202243199349323204, 202330979349300728, 202333199349323323, 202420369349301017, 202403139349303260, 202522379349301497, 202503179349301975 (links in §3.1) | Givinga series, amendment reasons, CY2024 diff |
| S3 | IRS e-file XML: Every.org objects 202141729349100004, 202201479349100500, 202333179349100048, 202423199349106002, 202502749349100700 (links in §2.2) | 990-PF financials, Part XV grants, Schedule B contributors |
| S4 | Every.org help center: [tax status](https://support.every.org/hc/en-us/articles/5715755336083-What-is-the-501-c-3-tax-exempt-status-of-Every-org), [disbursements overview](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview), [timing](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit), [fees](https://support.every.org/hc/en-us/articles/360059998533-What-are-the-third-party-processing-fees), [DAF](https://support.every.org/hc/en-us/articles/360059998953-How-can-I-donate-using-a-Donor-Advised-Fund-DAF), [assets](https://support.every.org/hc/en-us/articles/360058166014-How-can-I-donate-stocks-cryptocurrency-or-other-assets), [funding](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded) | Every.org status, rails, account model |
| S5 | Givinga Foundation [Account Holder Handbook](https://cdn.prod.website-files.com/67f91b19ba41ea3a5732646b/68502b601729bb5f3c1a7c75_Givinga-Foundation-Account-Holder-Handbook.pdf), [Policies and Procedures](https://cdn.prod.website-files.com/67f91b19ba41ea3a5732646b/68502b2e2476ee92f72652ea_Givinga-Foundation-Policies-and-Procedures.pdf), [givingafoundation.org](https://www.givingafoundation.org/) | Account rules and minimums |
| S6 | [givinga.com](https://www.givinga.com/), [/solutions](https://www.givinga.com/solutions), [/why-givinga](https://www.givinga.com/why-givinga), [/pricing](https://www.givinga.com/pricing), [PRWeb 2019-03-25](https://www.prweb.com/releases/Drive_Employee_Engagement_Through_Corporate_Philanthropy/prweb16186009.htm) | Employee-account product model; absence of assurance claim |
| S7 | Trust centers (public metadata, retrieved 2026-11-14): [Foundant](https://trust.foundant.com/), [Give Interactive](https://trust.giveinteractive.com/resources), [Chariot](https://trust.givechariot.com/), [Blackbaud](https://trust.blackbaud.com/), [TIFIN](https://trust.tifin.com/), [Benevity (offline)](https://trust.benevity.com/) | P-QA1-04 classification |
| S8 | [BD Emerson Give Interactive case study](https://www.bdemerson.com/case-studies/give-interactive) | SOC 2 Type 2 + SOC 3, September 2025 |
| S9 | Ren claims: [AEF 2025-07-23](https://www.aefonline.org/thought-leadership/american-endowment-foundation-selects-ren-as-a-strategic-partner-to-expand-philanthropy-drive-innovation-and-foster-growth-in-financial-services/), [AEF 2026-04-08](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/), [Giving Compass 2026-05-13](https://www.givingcompass.org/giving-compass-and-ren-accelerate-nonprofit-impact-discovery-for-daf-advisors/); templates [RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf), [RCF MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RCF-MSA_v1.pdf), [iPhi MSA](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx) | Ren contradiction; no SOC terms in templates |
| S10 | [TIFIN 2024 announcement](https://tifin.com/news/tifin-give-expands-its-reach-as-a-leading-technology-powered-philanthropy-platform-for-wealth-enterprises-2/) | TIFIN claim |
| S11 | [Chariot security page](https://help.givechariot.com/onboarding/trust-and-safety/security) | Chariot claim, AWS, Column N.A. |
| S12 | [Benevity security](https://benevity.com/security), [trust and security](https://benevity.com/trust-and-security) | Benevity SOC 1/2 Type II, ISO wording, AWS |
| S13 | [NPact SOC KB article](https://npact.document360.io/fims-and-donorcentral/docs/how-to-obtain-a-soc-report-for-hosted-fims-and-donorcentral) | Azure reports offered in place of an NPact report |
| S14 | [Blackbaud compliance page](https://www.blackbaud.com/compliance-certifications) | No product scope |
| S15 | Candid blogs: [2023-11-29](https://candid.org/blogs/building-a-culture-of-nonprofit-compliance-at-candid/), [2025-04-24](https://candid.org/blogs/how-candid-ensures-data-security-safeguards/) | Candid claim |
| S16 | [Foundation Source DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/); [Endaoment docs corpus](https://docs.endaoment.org/llms-full.txt); [Daffy docs](https://docs.daffy.org/) and [help center](https://help.daffy.org/en/) | Absence checks |
| S17 | The 19 monitored URLs in [terms-monitor-urls.csv](../../data/mission-2026-11-14/terms-monitor-urls.csv) | P-PAY-07 baseline |

---

## 8. Data dictionary

### vendor-assurance-scope-2026.csv (one row per vendor)

| Column | Meaning |
|---|---|
| vendor | Vendor as studied |
| assurance_entity_named | Legal or product entity named in assurance material, if any |
| public_trust_center_url | Trust center URL, or "none found" with what was checked |
| trust_center_platform | SafeBase / Vanta / Oneleet / Conveyor / SecurityPal, and gating status |
| soc3_public | Whether a SOC 3 can be downloaded without an access request |
| soc2_type_stated / soc1_type_stated | Report type as publicly stated, with source context |
| report_dates_or_periods_public | Any public report date or observation period |
| system_scope_public | Whether in-scope systems or products are public |
| auditor_named | CPA firm or certification body, if named publicly |
| iso27001 | ISO/IEC 27001 status as stated (certificate vs "based on") |
| other_frameworks_listed | Other badges and frameworks |
| subservice_orgs_disclosed | Hosting, bank or subprocessor parties named publicly |
| classification | `scoped_report_public` / `type_stated_without_scope` / `vendor_claim_only` / `none_found` (rules in §1.1) |
| contradiction_flag / contradiction_note | yes / minor / no, with explanation |
| evidence_urls | Sources, separated by ` ; ` |
| evidence_kind | Kind of evidence (trust-center metadata, press boilerplate, first-party page, etc.) |
| retrieved_date | 2026-11-14 |
| notes | Caveats |

### terms-monitor-urls.csv (monitor configuration)

| Column | Meaning |
|---|---|
| slug | Snapshot folder name under `data/terms-snapshots/` |
| vendor, document | What the URL is |
| url | Fetched URL |
| format_hint | html / pdf / docx / markdown (content is also sniffed) |
| watch_reason | Why it is monitored |
| ignore_regex | Optional regex; matching lines are dropped before hashing (for volatile content) |
| source_of_url | Where the URL came from in the repo or on the site |

### data/terms-snapshots/manifest.csv (one row per URL per run date)

| Column | Meaning |
|---|---|
| date, slug, vendor, url, final_url | Run date and target (`final_url` after redirects) |
| http_status | HTTP code, or the error class (e.g. `RemoteDisconnected`) |
| outcome | `snapshot_written` / `fetch_failed` / `too_little_text` |
| state | `baseline` / `unchanged` / `changed` / `skipped` |
| previous_date | Date of the snapshot compared against |
| format, extractor | Detected format and the extractor used |
| text_chars | Normalized text length |
| raw_sha256, text_sha256 | Hash of fetched bytes; hash of normalized text (the text hash is the change signal) |
| added, removed | Diff line counts versus the previous snapshot |
| error | Error message, for failures |

### `<slug>/<date>.meta.json`

Holds the same fields as the manifest row, plus `document`, `content_type`, `raw_bytes`, `watch_counts` (a dict of watch term to count) and `fetched_at_utc`.

### queue-proposals-assurance-monitoring.csv

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). IDs are P-ASR-01..07.

## Validation corrections (wave 5, 2026-11-14) — governing
Source: [validation-wave5-report.md](validation-wave5-report.md). Where these conflict with the text above, these govern.

4. **`research/mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md`, P-INF-01.**
   - Replace: "**[I]** The 1.4m most plausibly counts employee accounts provisioned by employer programs, most with near-zero balances ($1.37 average)."
   - With: "**[I]** The unit is undefined. Candidates are employer-provisioned employee accounts and game/app-user records from Schedule G fundraisers (Golden Hearts Games, SoftGiving/Brandfluence; see sponsor-cost-structure-and-sensitivities.md §6). Average balance is $1.37."
10. **`queue-assurance-everyorg-givinga-monitoring.md`, P-QA2-04.** After "falling to 1.1% in 2024 [C]", add: "This is a floor, because CY2024 reports $6.58m in aggregate to recipients under $25k."
11. **`queue-assurance-everyorg-givinga-monitoring.md`, P-QA1-04.** After "Foundant, Give Interactive, Chariot, Blackbaud, Benevity", add: "(Foundant names its auditor, Linford & Co, and all five Trust Services Criteria, but not the period)". Also add: "reninc.com, candid.org and tifin.com returned 403 to the wave-5 validator."

No corrections are needed for V5-02, V5-04, V5-06 (numbers), V5-07, V5-08, V5-09 or V5-10 (numbers).
