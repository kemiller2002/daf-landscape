# 08 - Making onboarding boring

Status: research (2026-11-26). Starting point: Transitus research (branch `claude/transitus-research-architecture-42a96z`, PR #1 **not merged**, provisional; SRC-006) and PR #88 reports 10-18 (SRC-001). New cross-industry evidence: [trackD-techniques.csv](data/evidence/trackD-techniques.csv) (23 techniques with measured outcomes) and [trackD-notes.md](data/evidence/trackD-notes.md) (SRC-066).

## Answer in brief

Onboarding becomes boring when it has **a standard, a guarantee and a clock** (ACATS, CASS, Stripe; CLM-022), and when the receiving side owns **reusable adapters for named source systems** (Gusto, core-banking conversion programs). Everything else in onboarding (cleansing, sponsor policy, exceptions) remains sponsor-specific work that can be scheduled and measured but not eliminated.

## 1. What other industries do (measured where possible)

| Technique | Industry | Measured outcome | Transfer to DAF |
|---|---|---|---|
| Two or more mock conversions with predefined go-live criteria | Core banking (Georgia DBF) | Regulator guidance; reuse of conversion programs from known source cores | **High** |
| Deconversion fee disclosure; orderly transition "without prohibitive expense" | Banking (interagency guidance; Jack Henry $33.9M deconversion revenue) | Fee disputes litigated (Fiserv) | **High** (publish symmetric exit price) |
| Year-to-date balance import + parallel run; keep old contract until first live cycle | Payroll (ADP, Gusto, Paycor) | Standard practice | Medium-High (DAF cycles weekly/monthly; cheap to parallel) |
| Named competitor-report import adapters | Payroll (Gusto transfer automation) | Vendor documentation | **High**: closest model for DAF source adapters |
| ID mapping file; SLA clock starts on valid data; published exclusions; customer approves validation summary | Payments (Stripe PAN import: 10 business days) | VERIFIED terms | **High** |
| Negative-consent bulk transfer with 30-day notice | Brokerage (Schwab-TD: 3.6M accounts, $1.3T; 4-5% of advisor firms left) | VERIFIED | Low (same-sponsor platform change needs no donor consent; INFERENCE, counsel) |
| Pre-cutover credential provisioning window (~10 weeks) | Brokerage (Schwab-TD) | VERIFIED | **High** (removes forced re-registration, W03) |
| Statistical-sampling validation of migrated attributes | Healthcare (JAMIA 2016: no errors over 12 months; 56k-115k person-hours saved) | Peer-reviewed | High for non-money fields; money stays exact |
| Migrated-data quality measures before deployment | Federal (GAO-22-103718) | Recommendation | High |
| Opening balances + 2-3 years summary TB | ERP | Practice | Medium (DAF needs per-fund full history; floor not target) |
| Selective conversion + active archive | EHR | Practice | Medium (fallback where history is unavailable) |
| Predefined migration objects | SAP | 70% effort reduction (VENDOR-CLAIM) | Medium (only reuse figure found) |
| LLM/ML mapping suggestions with rule checks | Data integration research | F1 ~0.7 (CLM-034) | High **as assistant**; never authoritative |
| Free migration offers | Nonprofit CRM | Table stakes (CLM-021) | Not a differentiator |

## 2. Required capabilities and their state

| Capability | Status in existing research / Transitus | Gap |
|---|---|---|
| Canonical import format | Canonical migration model (PR #88 14); Transitus mapping packages (DF-TRN-2026-0014/0019) | Not rehearsed on a real export (OQ-005) |
| Configuration-driven onboarding | Declarative sponsor configuration with perimeter validation (PR #88 12) | — |
| Source data profiling | T1 local profiling (PR #88 13) | Specify k-suppressed outputs (XRI-010) |
| Automated mapping suggestions | Transitus phase 3 (AI) | Keep as suggestions behind deterministic gates |
| Deterministic transformations | Transitus TRN-REQ-TX-001..009 (pure, total, versioned) | — |
| Immutable staging | TRN-REQ-ST-001/005 (content-addressed raw; Merkle-sealed staging) | — |
| Reconciliation | Gates and per-fund roll-forward proofs (PR #88 16); generic primitives (DF-TRN-2026-0011) | Auditor acceptance (E14 in PR #88) |
| Rehearsals | Three rehearsals in PR #88 cost model | Adopt ≥2 timed mocks as a gate (XRI-009) |
| Parallel operation | One grant cycle (PR #88 17) | — |
| Historical preservation | Non-posting legacy partition; opening-balance epoch; gaps disclosed, never plugged | — |
| Cutover and rollback | PR #88 17 | Pre-provisioned credentials (Schwab pattern) |
| Customer acceptance | Validation summary approved by sponsor (Stripe pattern) | Add to Transitus (XRI-011) |
| Automated evidence generation | Transitus evidence stage | — |

## 3. How much can be done before contract signature?

Without any donor data leaving the sponsor (NDA only):
1. **Extraction plan**: which named incumbent reports the sponsor can download, and what they omit.
2. **Contract-end back-schedule**: core banking starts 18-24 months out; DAF assessments should start from the incumbent's notice date.
3. **Exit-clause review**: export rights, fees, windows (the TPRM checklist is a ready template).
4. **Local structural profile**: profiler runs in the sponsor's environment and emits only field coverage, null rates, fund-type counts and k-suppressed aggregates.
5. **Synthetic rehearsal**: a synthetic dataset generated from schema + suppressed distributions exercises adapter, mapping and reconciliation end to end and yields a readiness report.

Not possible before signature without a data processing agreement: loading real records, exact tie-out, and history-depth confirmation. Constraints: incumbent login-only access and paid exports; benchmark clauses in incumbent contracts; state privacy laws and the sponsor's donor privacy notice.

## 4. Reusable package versus customer-specific mapping

| Component | Reusable? |
|---|---|
| Target canonical package (entities, import commands, validation, reconciliation gates) | Yes, one per Unbound version |
| Source adapter per incumbent platform and report version | Yes, per source; the **first** instance is expensive |
| Value crosswalks (fund types, statuses, payment methods) | Partly: defaults per source, sponsor overrides |
| Sponsor policy and configuration | No (declarative, sponsor-specific) |
| Cleansing and exceptions | No |

No public source measures the reusable share (only SAP's vendor claim). Expected pattern (INFERENCE, Medium): the second migration from the same source costs far less than the first, so **sales should cluster on one incumbent source** (DEC-007; HYP-012).

## 5. Institutional onboarding maturity model (conceptual)

| Level | Name | Observable criteria | Exemplar |
|---|---|---|---|
| 0 | Ad hoc | No written method; spreadsheets; no control totals; timeline unknown at signing | Many FIMS replacements |
| 1 | Repeatable project | Runbook; PM; ≥1 mock; grand-total tie-out; informal go-live criteria | Typical CU core conversion |
| 2 | Defined and gated | Predefined go-live criteria; **≥2 timed mocks**; 100% per-fund opening balance tie-out; one parallel cycle; published exclusions | Payroll mid-year conversion |
| 3 | Productised | Reusable source adapters; canonical package; mapping as configuration; deterministic replay; sampling validation; quality metrics before go-live | Gusto transfer automation; Stripe validation summary |
| 4 | Assured and measured | SLA clock starts on conforming extract; outcome commitments; per-migration metrics (cycle time, exceptions per 1k, post-go-live defects); standard pre-contract T1; published symmetric exit price | Stripe SLA; CASS guarantee |
| 5 | Largely automated | Sponsor runs profiler and adapter; AI suggestions pass gates; >50% of migrations need no engineering change; statistics published | ACATS/CASS utilities; no DAF exemplar |

Progression metrics: share of fields mapped by package defaults; engineering changes per migration; mock-to-live control-total delta; days from conforming extract to go-live; post-go-live defects per 1k funds at 30/90 days. **Claim a level only from measured data.** Incumbents publish nothing that places them on this scale (CLM-020).

## 6. Migration assessment as an acquisition mechanism

- **Direct evidence: none** (CLM-021). Free migration is common in nonprofit CRM; PoC win-rate figures are confounded by selection.
- **Indirect**: 75% of buyers cite migration cost as a barrier (SRC-059); credit unions switch despite seven-figure exit fees; buyers ask for assurance (Foundant PoC snippet; quality C).
- **Assessment**: a structured assessment (extraction plan + exit-cost comparison + dated plan tied to the incumbent's contract end + SLA clock) plausibly lowers perceived risk and shortens qualification (HYP-004). Price T0-T1 free, T2-T3 paid and credited against implementation.
- **As a business on its own**: it does not pay for itself (route ER-2 never cash-positive in >99% of draws; CLM-028). Its value is pipeline and evidence, not margin.

## 7. What remains unavoidable

Data cleansing, sponsor policy decisions, history gaps the incumbent cannot supply, and the incumbent's own export behaviour. Onboarding can be made predictable; it cannot be made free.
