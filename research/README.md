# DAF security and technology assurance research

**Baseline:** November 11, 2026. This is a dedicated extension to the general DAF landscape research foundation.

## Research
- [SOC 2 public-assurance assessment](soc2-assessment-2026-11-11.md)
- [Capability comparison](capabilities-2026-11-11.md)
- [Technology and control map](technology-control-map.md)
- [Prioritized diligence plan](next-steps.md)
- [Assurance-specific methodology](../docs/assurance-methodology.md)
- [Assurance matrix](../data/assurance.csv), [capability data](../data/capabilities.csv), [assurance-specific sources](../data/assurance-sources.csv)

The general market research data and source taxonomy are maintained in the root README and data/source-register.csv in the independent foundational project. This package uses its own S01-S21 IDs in `data/assurance-sources.csv`; these IDs **are not** the IDs from the general market source-register.csv.


## Competitive platform investigation (2026-11-11)

- [Ren vs. TIFIN Give, with Chariot as infrastructure](ren-tifin-chariot-deep-dive-2026-11-11.md): verified organizational roles, capabilities, Chariot's confirmed TIFIN integration, operating-model tradeoffs and falsifiable competitive hypotheses.
- [Buyer-neutral evaluation protocol](platform-evaluation-protocol.md): sponsor, wealth institution and payments test scenarios; consistent timing definitions, control test fixtures and procurement questions.
- [Capability comparison dataset](../data/platform-comparison-2026-11-11.csv): 25 evidence-classified comparison dimensions, no invented winner scores.
- [Comparison source register](../data/platform-deep-dive-sources.csv): separate C001–C028 references with publication dates and limitations.

The clearest documented distinction is **Ren's integrated fund-accounting/administration and payments offering vs. TIFIN Give's advisor-oriented stack with GiveClear as sponsor and Chariot as an actual disbursements partner**. This is a public-source structural observation, not an audited performance comparison. Actual implementation and security maturity remain unverified.


## Donor tax-fit segmentation (2026)

- [DAF donor tax personas, 2026](donor-tax-personas-2026.md): 14 candidate and exclusion personas, 2026 income-tax rule changes, eligibility decision tree and an illustrative three-year bunching calculation that includes the new direct-giving nonitemizer deduction.
- [Persona dataset](../data/donor-tax-personas-2026.csv) and [tax source register](../data/donor-tax-sources-2026.csv): machine-readable targeting triggers, prerequisites, counterexamples and 12 cited sources.

**Critical 2026 distinction:** A cash donation to a DAF is **not** eligible for the new $1,000/$2,000 nonitemizer deduction, while a cash gift directly to an eligible charity may qualify. Do not imply DAFs are uniformly tax-efficient for every donor.


## Proactive donor tax-opportunity research (2026)

- [Ren vs TIFIN Give donor identification, planning, and execution](tax-opportunity-lifecycle-2026-11-11.md): a source-based life-cycle analysis that distinguishes Ren's public Benefit Estimator from TIFIN's announced Tax Intelligence and Single-Charity Funds, and correctly places Chariot downstream.
- [Tax opportunity comparison matrix](../data/tax-opportunity-capability-matrix-2026.csv): 22 lifecycle dimensions, classified by what public evidence actually establishes.
- [Synthetic evaluation protocol](tax-opportunity-evaluation-protocol-2026.md) and [18 cases](../data/tax-opportunity-test-cases-2026.csv): adversarial donor examples with **all vendor test outcomes unexecuted**, intended for independent tax-professional review and authorized demos.
- [Public source register](../data/tax-opportunity-sources-2026.csv): 22 primary references, with publication dates and scope limitations.

**Summary:** TIFIN Give announced portfolio-level Tax Intelligence in September 2025; Ren has a public DAF Benefit Estimator and documented advisor tax-planning guidance. This is an **evidence coverage difference**, not verified relative prediction accuracy. The required product test must compare DAF and direct giving, include 2026 tax rule changes, and sometimes recommend **no DAF**.


## Actual evaluation status (2026-11-11)

- [Execution report: what was checked, calculated, and blocked](vendor-test-execution-2026-11-11.md). **No live Ren, TIFIN Give or Chariot vendor test was executed**; no vendor may be scored as pass/fail.
- [Independent reference-case results](../data/reference-check-results-2026-11-11.csv): five synthetic arithmetic sanity checks executed, 13 rule or escalation expectations documented, not CPA-validated.
- [Per-case vendor access review](../data/vendor-test-access-2026-11-11.csv): 36 Ren/TIFIN cases and one Chariot downstream case, all live tests not executed, with public UI input gaps recorded.
- [Prepared vendor access requests](vendor-access-request-2026.md): ready for approved outreach; not sent.

**Fixture correction:** X03 had inconsistent high-rate/AGI assumptions. Corrected to 2026 single filing, $900,000 AGI, assumed $800,000 taxable income; the 0.5%-AGI floor is $4,500 and a $20,000 eligible cash gift leaves $15,500 before other restrictions. Original 18-case evaluation now uses that corrected fixture.

## Principal findings

- Ren's `reninc.com` April 2026 announcement states **SOC 2 Type I**. The Type II claim from `tryren.com` belongs to an unrelated AI coaching company.
- Chariot markets **SOC 2 Type II**.
- TIFIN Give markets **SOC 2 security compliance**, but public evidence reviewed does not specify type.
- **No independent auditor report was inspected.** All other organizations remain unverified in this scoped review; no negative assurance conclusion follows.

No confidential or client-specific material is included.
