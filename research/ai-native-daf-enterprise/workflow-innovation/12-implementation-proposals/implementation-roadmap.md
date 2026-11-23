# Prioritized implementation proposals

**Relationship to the parent roadmap:** this refines [`../../12-implementation-roadmap/implementation-roadmap.md`](../../12-implementation-roadmap/implementation-roadmap.md). That roadmap has six phases with gates, enters as Model C, and adds the partner sponsor-of-record (Model D) later. Here, the innovations that survived the audit are placed into those phases in **evidence order**: what must be measured before anything is built on it.

Nothing here authorizes live operation. Phases 1–3 involve no money movement.

## Wave 0: now, no partner needed (public data and synthetic work)

| # | Work | Closes | Acceptance criterion |
|---|---|---|---|
| 0.1 | Small-sponsor Schedule I harvest (outside the top 50) and rerun of E7/E7b | Long-tail network value | Overlap and costly-overlap curves for ≥200 additional sponsors. **Done 2026-11-23 (E7c): 1,285 sponsors** |
| 0.2 | Build the audit's missing adversarial cases: E1 poisoned refresh and name collision; E2 adaptive adversary, correlated AI misses, reviewer automation bias; E3 registry-compromise blast radius | Audit §5 gaps | Each case has a test that can fail. No tautological assertions |
| 0.3 | Policy compiler prototype: decision tables → tests → generated prose, with back-test on synthetic history | INN-21 L1 → L3 (synthetic) | A rule change produces a diff report on a replay corpus |
| 0.4 | Canary harness for every deterministic rule in the parent PoC | FP-04; CTL-046 | Disabling any rule fails a canary within one simulated day |

## Wave 1: parent Phase 1–3, one design partner, shadow mode, no money movement

| # | Work | Innovations | Closes | Acceptance criterion (design targets) | Kill or continue |
|---|---|---|---|---|---|
| 1.1 | **Shadow replay** of the partner's historical grants through the policy engine; timed human review of a stratified sample | INN-05, INN-21, INN-01/03/34 | GAP-001, GAP-004; E2's parameter dependence | Measured exception rate, minutes per exception, human catch rate per defect class; ≥99% agreement with past approvals on the routine tier, with every disagreement explained | Kill INN-05's routine-tier claim if rule approvals disagree materially with human decisions on substantive grounds |
| 1.2 | **Determination reuse factor** from partner exception history | INN-04, INN-02 | Largest unmeasured lever | Reuse share of ED and fiscal-sponsor reviews measured | Below ~20%, drop INN-04's economics |
| 1.3 | **Break-cost study** from partner reconciliation logs | INN-22/39 | GAP-005; E4's assumption | Minutes per break by age measured | If age has no cost, continuous close is justified only by detection, not labor |
| 1.4 | **Donor acceptance of execution windows** (survey, or A/B in partner communications) | INN-37 | Behavioral premise | Share of December recommenders accepting January execution | Below ~30%, drop the deferral lever |
| 1.5 | Evidence-by-construction export for the partner's auditor | INN-20 | Auditor acceptance | Auditor uses the package in fieldwork | — |

## Wave 2: parent Phase 4–5, three or more partners, supervised live routing under each sponsor's authority

| # | Work | Innovations | Precondition |
|---|---|---|---|
| 2.1 | Grant ID in remittance (CCD+/CTX addenda), electronic by default | INN-08 | Bank supports addenda; recipient-side measurement of matching time |
| 2.2 | Daily netting per recipient, with blast-radius limits (cap grants per netted payment) | INN-09 | Model 0.2 shows acceptable incident impact |
| 2.3 | Capped delegations for advisors and donor agents, with revocation, expiry and theft tests | INN-16/26 | L2 → L3 tests pass |
| 2.4 | Replay-based migration tooling for onboarding partners from incumbent recordkeepers | INN-18 | Partner export rights (GAP-002) |
| 2.5 | Publish operating metrics for the partner programs | INN-46 | Telemetry from Wave 1 |
| 2.6 | Board parameter-expiry and governance-by-exception portal | INN-32/48 | Board agreement |

## Wave 3: parent Phase 6, commercialization, gated

| # | Work | Gate evidence |
|---|---|---|
| 3.1 | Multi-tenant determination store and fiscal-sponsor host-diligence sharing among platform clients (the network inside Model C first) | E7b overlap holds on client data; counsel opinion on reliance (REG-019/020) |
| 3.2 | Shared compliance policy packs for sponsors on incumbent recordkeepers | ≥40 committed sponsors [A]; correlated-error controls (staged rollout, per-sponsor approval) |
| 3.3 | Advisor-embedded DAF integrations (program-as-code) | Market interviews (parent 10-); fee-disclosure review; proposed §4966 adviser rule watched |
| 3.4 | Spend-down horizon and charitable-default pilot with a mission-aligned partner sponsor | Partner board approval; donor research |

## Deferred or watch

- Neutral third-party verification network.
- Shared payee registry.
- Recipient inbox.
- Decision-rights market.
- Sponsor-owned record substrate.
- Continuous external assurance.
- ACATS-like transfer protocol.

Each needs either two-sided adoption or legal opinions that the waves above would produce first.

## Rejected

- INN-06: sampling replaces review.
- INN-35: pay-first.
- AI auto-clear of flags.
- Lead scoring on purchased wealth data (D-ACQ-2).

## Resourcing (indicative [A])

- **Wave 0:** 2–3 engineers for about 3 months.
- **Waves 1–2:** fit within the parent roadmap's $5.5m–$9.5m budget through Gate 5.
- **Wave 3:** new capability only after its gate evidence exists.
