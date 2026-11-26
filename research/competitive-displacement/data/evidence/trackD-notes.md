# Track D: "Make onboarding boring". Cross-industry evidence extension

Date: 2026-11-26 (all URLs accessed 2026-11-26). Classes: VERIFIED-FACT / VENDOR-CLAIM / INFERENCE / UNKNOWN. Data: `trackD-techniques.csv` (23 rows).

**Scope.** This extends `charity-network-and-onboarding/10–18`, the cross-industry CSVs, `migration-integration-tooling/01-findings.md` and Transitus (branch `claude/transitus-research-architecture-42a96z`; PR #1 is unmerged, so its content is provisional). It does not repeat ACATS, CASS, TSB, Revlon, Stripe mapping-file and ramp, ERISA, Rev. Proc. 2004-53, ONC EHI or Workday foundation tenant. Before this work, no onboarding maturity model existed in the repo (grep, INFERENCE).

**Limits.** Some primary pages could not be read:
- Foundant support returned 403, so the claimed pre-contract PoC is still unconfirmed.
- The Loxo guarantee page returned 404.
- The Thieme full text was behind bot protection.

Figures taken from search snippets are marked as such in the CSV.

## A. New measured evidence (beyond prior work)

### Core banking: exit cost is real money, and it is priced

- **Jack Henry deconversion revenue** (FY2025 10-K):

  | Fiscal year | Deconversion revenue | Deconversion costs |
  |---|---|---|
  | FY2025 | $33.9m | $6.2m |
  | FY2024 | $16.6m | not stated |

  It comes "mostly" from clients agreeing to be acquired. VERIFIED-FACT, High.
- **Interagency TPRM guidance (2023).** Contracts should "provide termination and notification requirements with reasonable time frames to allow for the orderly transition … without prohibitive expense", "provide for the timely return or destruction of … data", and "assign all costs and obligations associated with transition and termination". VERIFIED-FACT, High.
- **No FDIC or OCC text sets deconversion fee levels.** UNKNOWN (not found).
- **Fee ranges.** Consultant estimates are $150k–$500k per bank. Some contracts default to 100% of the remaining-term fees, and unpublished fees can exceed 2 years of revenue. VENDOR-CLAIM, Low.
- **Litigation.** Polam FCU v. Fiserv survived a motion to dismiss on 2026-06-18. Four other credit unions are suing, and Fiserv has settled three. FiCare alleges "seven-figure" termination and deconversion fees. VERIFIED-FACT (trade press), Medium.
- **Practice norms.**
  - At least 2 mock conversions.
  - Go-live readiness criteria set in advance (Georgia DBF).
  - Contract re-evaluation starts 18–24 months before expiry.
  - Conversions run about 1 year.
  - Reusable conversion programs exist per source core. A first-ever source has to be written, not "pulled off a shelf" (snippet).

  VENDOR-CLAIM / anecdote, Medium.

### Payroll

- **Mid-year switch checklist (ADP):**
  1. Import YTD by employee and by quarter, plus current-year 941s.
  2. Verify the previous quarter's tax history.
  3. Run a parallel payroll before the first live run.
  4. Close the old provider only after the first live payroll succeeds.

  VENDOR-CLAIM.
- **Gusto import adapters.** Gusto parses named competitor reports: ADP Run Employee Summary and Payroll Details PDFs, QBO/QBD, and Paychex (beta). The import is available during onboarding only, and masked fields do not import. VENDOR-CLAIM, Medium.
- **Typical implementation.** 8–16 weeks, or 4–8 weeks for a simple move between major providers. Paycor runs parallel tests at about T-30 days. VENDOR-CLAIM.
- **No published parallel-match statistics.** UNKNOWN.

### Custody: Schwab–TDA wave

| Measure | Value |
|---|---|
| RIA firms | >7,000 |
| Accounts | 3.6m |
| Assets | $1.3T (Labor Day 2023) |
| Negative-consent notice | sent end of June |
| Credential set-up | opened June 21 |
| RIA attrition | 4–5% ("roughly as projected") |
| Residual issues | logons; account titles in third-party tools; "2 1099s" |

Trade press and Schwab claims, Medium.

FINRA RN 26-03 (Feb 2026) sets the negative-consent rules:
- at least 30 days' notice;
- an opt-out;
- disclosure of costs;
- no FINRA pre-review of letters from 2026-04-01.

VERIFIED-FACT (law-firm summaries plus the notice page), Medium.

### Payments: Stripe import

- **SLA.** 10 business days after *valid* data arrives. More than 1M records may take longer. Bacs takes 4–6 weeks.
- **Main delay.** The incumbent's export takes "days to months". Insisting on a Data Transfer Agreement "significantly lengthens" the timeline.
- **Approval step.** The customer approves a validation summary that includes a last-4 spot check on 2 customers.
- **Exclusions are published.** CVC, subscriptions and invoices do not move.
- **Exit.** Data can go to any PCI-compliant processor (AOC plus RSA-4096 PGP key).

VENDOR-CLAIM (Stripe docs), High.

### Healthcare EHR

- **Stanford / Lucile Packard (JAMIA 2016).** Statistical-sampling validation:
  - 98% confidence, 0.2–1% error limits.
  - Zero migrated-data errors reported in 12 months.
  - Estimated saving of 56k–115k person-hours versus 10–20% manual samples.

  VERIFIED-FACT, High (clinician under-reporting caveat).
- **GAO-22-103718 (VA).**
  - Allergy, medication and immunization migration errors created patient-safety risk.
  - GAO recommended measures and goals for migrated-data quality *before* deployment. The recommendation is still open.

  VERIFIED-FACT, High.
- **Literature review (Schreiber & Garber 2020).** The literature is thin, and convert, archive and hybrid are all used. In one survey, 11% of users wanted full conversion and 30% wanted selected categories. Keeping the legacy system up for lookups is ineffective. VERIFIED-FACT, Medium.

### Accounting / ERP

- **Typical scope.**
  - Opening balances.
  - Per-period trial balances: 2–3 years in partner guidance, 6–12 months in a Packt book.
  - Open items in detail.
  - Cut over at year end, or at least month end.
  - At least 2 test migrations, with a tie-out to the legacy trial balance.

  VENDOR-CLAIM, Low–Medium.
- **SAP migration cockpit.** Predefined migration objects come with templates and auto-mapping. SAP claims a 70% effort reduction. VENDOR-CLAIM, Low.

### Insurance

- **Andesa.** About 40k active plus 80k inactive UL/VUL policies were ready for conversion in under 12 months. The pre-conversion archive stays reportable. VENDOR-CLAIM, Low.
- **No public closed-block conversion statistics.** UNKNOWN.

### Mapping-suggestion accuracy

| Study | Finding |
|---|---|
| Valentine (ICDE 2021) | Schema-only matchers are weak and sensitive to noisy names. |
| BDIViz (2025) | Top-10 recall of 93%, but the LLM validator misclassifies up to 38%. |
| Monka et al. (arXiv 2608.24218, Aug 2026) | A constraint gate raises F1 from 0.08 to 0.66. Macro-F1 is 0.70 across 7 enterprise datasets, with about 7× less expert effort. |

Academic, Medium. Conclusion: **suggestions plus gates plus a human**, not autonomy. This is consistent with Transitus DF-TRN-0012.

### Pre-sale assessment and PoC as acquisition

- **Free migration offers are common in nonprofit CRM.** DonorPerfect, DataBank, Keela and Givebutter all offer them, usually time-limited and tied to a minimum term. VENDOR-CLAIM.
- **No measured lift is published.** UNKNOWN.
- **Presales benchmarks.**
  - PoCs average 33 days (Vivun).
  - PreSales Pulse 2026 reports median PoC win rates of 62% for horizontal SaaS, 44% for fintech and 38% for healthcare. Its method is unverified and selection-biased.
  - Overall B2B win rates are 20–47%.

  VENDOR-CLAIM, Low.
- **Paid assessment credited against the deal.** One ERP selection firm credits 60% of the fee to the first invoice. VENDOR-CLAIM.
- **Buyer concern (BCG 2025, via Univ. of Auckland).** 75% worry about technical migration cost, and 77% keep their own data model to preserve exit options. VENDOR-CLAIM, Low–Medium.

## 1. Techniques: transfer to DAF sponsor onboarding

| Technique | Transfer | Why / evidence |
|---|---|---|
| Published exit/deconversion price and format (inverse of core-banking fees) | High | JKHY $33.9m deconversion revenue; TPRM "without prohibitive expense"; Fiserv suits. Unbound can make exit cost a published number. |
| Competitor-report adapters (Gusto model) | High | Works with no incumbent cooperation. Consumes reports the sponsor can already download. Fits 13 §2a. |
| Clock-starts-on-valid-data SLA, validation summary approved by customer, published exclusions (Stripe) | High | 10 business days post-valid-data; dominant delay is the incumbent's export. |
| At least 2 mocks plus predefined go-live criteria | High | Georgia DBF; credit union practice. |
| YTD import plus prior-period verification; filing RACI | High | ADP/Gusto. Maps to the cutover-year acknowledgement and 1099 issuer. |
| Statistical-sampling validation for non-monetary fields | High (non-money only) | JAMIA 2016. Money stays on 100% control totals (16). |
| Pre-deployment migrated-data quality metrics | High | GAO-22-103718. |
| Pre-cutover credential/training window | High | Schwab: about 10 weeks before. |
| Parallel run; keep old contract until first live cycle | Medium | Payroll practice. DAF cycles are weekly or monthly, so cheap. |
| Opening balance plus 2–3 years of trial balances (ERP) | Medium | DAF needs per-fund full history; ERP is the floor, not the target. |
| Selective conversion plus archive (EHR) | Medium (fallback) | Donor expectation of full history (AEF/Ren). |
| Negative-consent bulk transfer | Low–Medium | No DAF statutory basis. Same-sponsor platform change needs no donor consent (INFERENCE; counsel). Pattern applies to ProgramTransfer notices only. |
| Closed-block TPA outsourcing | Low–Medium | Run-off programs only. |
| LLM mapping suggestions | High as assistant | F1 of about 0.7 with gates; never authoritative. |

## 2. Onboarding maturity model (conceptual; INFERENCE built from the cited practices)

| Level | Name | Observable criteria (all must hold) | Cross-industry exemplar |
|---|---|---|---|
| 0 | Ad hoc | No written method. Mapping lives in spreadsheets or individuals' heads. No control totals. Timeline unknown at signing. History depth decided late. | Pre-2018 TSB-style governance; many FIMS replacements (13) |
| 1 | Repeatable project | Written runbook. Dedicated PM. At least 1 mock conversion. Manual tie-out of grand totals. Go-live criteria exist but are informal. | Typical credit union conversion (Georgia DBF checklist) |
| 2 | Defined and gated | Predefined go-live criteria. **At least 2 mocks** with timed cutover. Per-fund opening balance tie-out at 100%. Parallel run of one grant cycle. Filing/acknowledgement RACI. Published exclusions list. | Payroll mid-year conversion (ADP/Gusto); ERP 2-test-migration practice |
| 3 | Productised | Reusable **source adapters** for named incumbent reports. Canonical migration package (CMM). Mapping is configuration, not code. Closed exception list. Deterministic replay. Statistical-sampling validation for attributes. Migrated-data quality metrics reported to the sponsor *before* go-live. | Gusto payroll transfer automation; SAP predefined migration objects; Stripe validation summary |
| 4 | Assured and measured | Published SLA whose clock starts on a conforming extract. Commitment terms (11 §5). Every migration reports cycle time, exceptions per 1k records, rework and post-go-live defects. Pre-contract T1 assessment standard. Published exit price and format (symmetric). | Stripe 10-day SLA; CASS 7-day guarantee and KPIs (11); JAMIA sampling with stated error bounds |
| 5 | Largely automated / self-service | Sponsor runs the profiler and adapter itself. AI mapping suggestions pass deterministic gates and need human approval only for exceptions. More than half of migrations need no Unbound engineering change. Rolling wave capacity. Statistics published across migrations. | ACATS/CASS utilities (standard plus clock); Gusto self-upload; no DAF exemplar exists |

**Level progression metrics:**
- % of fields mapped by reusable package versus sponsor-specific;
- engineering changes per migration;
- mock-to-live delta in control totals;
- days from conforming extract to go-live;
- post-go-live defects per 1k funds at 30/90 days.

Unbound should claim a level only from measured data (RECOMMENDATION).

## 3. Before contract signing: what is possible and the constraints

- **No data leaves the sponsor (NDA only).**
  - Extraction Plan: which named incumbent reports the sponsor can download.
  - Contract-expiry back-schedule. Core banking evaluation starts 18–24 months out, so the DAF assessment should start from the incumbent's end date.
  - Exit-fee and data-return clause review. The TPRM checklist is a ready template.
  - Schema/structural profile run locally (13 T1).
  - Gusto-style parsing of standard reports run inside the sponsor's own environment, emitting only field coverage, null rates, fund-type counts and k-suppressed aggregates.
- **Synthetic or structural profiling.**
  - A synthetic dataset generated from the sponsor's *schema plus suppressed distributions* can exercise the adapter and mapping end-to-end and produce a mock readiness report.
  - Do not use differential privacy where exact tie-outs are needed (13).
  - Format-preserving tokenization is still personal data (13).
  - INFERENCE, Medium.
- **Constraints.**
  1. Incumbent terms. Direct-login-only access and paid exports (13 §2a). Stripe notes that export takes "days to months" even in a regulated, portable market, and Data Transfer Agreements lengthen timelines.
  2. State privacy laws covering nonprofits, and the sponsor's donor privacy notice (13 §3).
  3. Benchmark/competitive-evaluation clauses in incumbent contracts (L20–L21).
  4. No negative-consent equivalent is needed or available for donors on a same-sponsor platform change. Program transfers between sponsors need sponsor-authorized grants, not bulk transfer (INFERENCE; counsel).
- **Pricing pattern.** T0–T1 free. T2–T3 as a paid assessment credited against implementation (the ERP-consulting 60% credit pattern), to limit unqualified use. RECOMMENDATION.

## 4. Reusable package vs customer-specific mapping

| Component | Reusable across sponsors? | Evidence |
|---|---|---|
| Target canonical package (CMM, import commands, validation rules, reconciliation gates) | Yes: one per Unbound version | SAP predefined migration objects (70% effort claim, VENDOR-CLAIM); Transitus DF-TRN-0014/0019 mapping packages |
| Source adapter per incumbent platform and report version | Yes: per source; first instance costly | Core banking "off the shelf" vs written conversion programs (snippet); Gusto named-report parsers |
| Value crosswalks (fund types, grant statuses, payment methods) | Partly: default per source, sponsor overrides | Symitar-to-Symitar still needed product surveys (trade press) |
| Sponsor policy/configuration (fees, spending policy, succession, anonymity defaults) | No: sponsor-specific, declarative (12) | Payroll: Gusto imports data but pay items/deductions are configured separately |
| Exceptions and data cleansing | No | Every source and practitioner says data cleanup is sponsor work |

- **Quantified reuse.** No public source gives a reusable share in percent. The only figure is SAP's vendor-claim 70% effort reduction. UNKNOWN. Unbound should measure "% of mapped fields from package defaults" per migration.
- **Expected pattern** (INFERENCE, Medium):
  - The second migration from the same incumbent costs far less than the first.
  - So sales targeting should cluster on one incumbent platform (for example, NPact or FIMS customers) to amortise one adapter.
  - This mirrors the core-banking practice where vendors keep conversion programs for known source cores.

## 5. Does a migration assessment work as a customer-acquisition mechanism?

- **Direct evidence: none found (UNKNOWN).**
  - No vendor publishes the conversion lift from pre-sale migration assessments or free migrations.
  - Foundant's pre-contract PoC remains a quality-C snippet. Foundant support was 403, and search shows only post-contract "outset migration".
- **Indirect evidence:**
  1. **Offers are common.** Free migration is widespread in nonprofit CRM (DonorPerfect, DataBank, Keela, Givebutter), so it is table stakes and not a differentiator (VENDOR-CLAIM).
  2. **PoCs correlate with high win rates.** Median 38–62% by vertical, versus overall B2B rates of 20–47%. This is confounded by selection: PoCs are offered to qualified deals (VENDOR-CLAIM, Low).
  3. **Buyers fear migration cost.** 75% cite technical migration cost (BCG via Auckland).
  4. **Some switches succeed despite friction.** Credit unions switch even with seven-figure exit fees (Fiserv suits), and 36% of banks had been on their core for 5 years or less in 2020, versus 13% in 2016.
- **Assessment (INFERENCE, Medium).** A migration assessment lowers *perceived* risk and shortens qualification. Its acquisition value is plausible but unproven.
- **Differentiators competitors do not offer:** the assessment outputs (history depth, an exit-price comparison, a dated plan tied to the incumbent's contract end) and an SLA whose clock starts on a valid extract.
- **Instrumentation (RECOMMENDATION):** log assessment tier reached → proposal → signed, with time-to-decision. Compare against non-assessed opportunities. Treat the number as Unbound's own evidence after 10 or more opportunities.

## Open gaps

- Foundant PoC terms.
- Actual DAF platform deconversion fees.
- Published mock-to-live defect statistics in any industry.
- Payroll parallel-run match rates.
- Insurance closed-block conversion durations.
- Independent measurement of package reuse share.

## Memory candidates

None. No user or project facts were learned beyond the repository content.
