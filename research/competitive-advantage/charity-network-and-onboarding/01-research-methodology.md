# 01 - Research methodology

Status: research draft (2026-11-26). Not legal advice. This file defines the evidence classes used across the package.

## Summary

- Eleven independent research agents each owned a bounded set of deliverables and a separate source-register fragment. A second wave of independent adversarial agents challenged the findings without seeing the coordinator's conclusions, only the drafts.
- Every material claim carries one evidence class and a confidence level (below). An absent public record is reported as "not publicly documented", never as proof that a capability is missing.
- Only public sources were used: no logins, product sign-ups, outreach, impersonation, contract breaches or circumvention of technical restrictions.
- The research builds on more than 80 prior daf-landscape studies and the Unbound requirements baseline. It cites them instead of repeating them; the brief named the prior files each agent had to read first.
- Product decisions already ratified in Unbound (`CNV-*` convergence clauses) were treated as constraints. Where evidence appeared to contradict one, the conflict is recorded for owner resolution (22, 24), not resolved silently.
- Requirements derived from this research live in `kemiller2002/unbound` under `requirements/discovery/2026-11-26-charity-network-and-onboarding/` with status **proposed**. Nothing is marked implemented or validated.

## 1. Questions

The mission had two tracks.

- **Track A, charity network:** how much of an incumbent's charity directory, shared vetting and electronic payment network is reproducible from public data and standard services, and how much is accumulated operational history?
- **Track B, onboarding:** which parts of institutional onboarding and migration are unavoidable domain complexity, and which come from architecture, data quality, tooling or consulting-dependent business models?

Each track asks what Unbound would have to build, buy or partner for to neutralize the barrier, and at what cost.

## 2. Agent structure

| Code | Responsibility | Deliverables |
|---|---|---|
| REN | Competitor intelligence: Ren | 02, `data/ren-network-metrics.csv` |
| CMP | Competitor intelligence: other providers | 03, `data/competitor-capability-matrix.csv` |
| DAT | Public charity data | 04, `data/charity-data-sources.csv` |
| REG | Charity identity, eligibility and vetting | 05, 06, `data/vetting-state-model.json`, `data/identity-resolution-cases.csv` |
| PAY | Electronic payment networks and organic growth | 07, 08, `data/payment-provider-matrix.csv` |
| SEC | Security, fraud and compliance | 09, `data/charity-network-threat-model.csv` |
| ONB | Institutional onboarding (DAF industry) | 10, `data/onboarding-observations.csv` |
| XIN | Cross-industry migration | 11, `data/cross-industry-migration-techniques.csv`, `data/migration-failure-cases.csv` |
| CFG | Sponsor configuration, integration and participant onboarding | 12, 18, 19, `data/sponsor-config-schema-outline.json`, `data/integration-certification-suite.csv` |
| MIG | Financial data migration | 13-17, `data/canonical-migration-entities.csv`, `data/reconciliation-gates.csv`, `data/cutover-strategy-comparison.csv` |
| ECO | Economic modelling | 20, `scripts/economic_model.py`, `data/economic-*.csv` |
| ADV-A, ADV-B, ADV-X | Independent adversarial review: charity network; onboarding; economics and strategy | 22 |
| Coordinator | Synthesis, targets, recommendations, requirements | 00, 01, 21, 23, 24, 25 and the Unbound package |

The agents worked in parallel and did not see each other's drafts, so their findings are independent. The adversarial agents were asked to refute the drafts, not to improve them.

## 3. Evidence classes

| Class | Meaning | Typical sources |
|---|---|---|
| VERIFIED-FACT | Stated by a primary or authoritative source that the agent actually read | IRS, Treasury/OFAC, Nacha rules, regulator notices, Form 990, SEC filings, audited financials, technical documentation |
| VENDOR-CLAIM | Asserted by a vendor or interested party about itself and not independently verified | Marketing pages, press releases, case studies, sales decks |
| INFERENCE | Reasoned from cited facts; the reasoning is shown | |
| ASSUMPTION | A working assumption stated so it can be changed | Model parameters without direct evidence |
| HYPOTHESIS | An unverified, testable proposition | Competitive hypotheses, performance targets |
| RECOMMENDATION | A proposed course of action | Design and strategy sections |

Confidence is High, Medium or Low. High needs a primary source, or two independent secondary sources that agree, within the stated time window.

Further rules:

- **Absence.** "Not publicly documented" means only that. It is never evidence that a competitor lacks a capability.
- **Units.** Sponsor charitable assets, vendor ARR, platform-serviced assets and advisor AUM are different economic units. They are never divided into one another to produce market share. This rule is inherited from the daf-landscape README.
- **Dates.** Every number carries an as-of date. Fiscal years are kept as reported.
- **Licensing.** Public accessibility does not imply a right to redistribute. Each source's terms are recorded separately (04).
- **AI-produced analysis.** Agent output is research input. It is not legal advice, independent assurance, audit evidence or regulatory certification.

## 4. Source register

Each agent wrote `data/sources-<CODE>.csv` with the same columns:

```
source_id,title,publisher,url,publication_date,access_date,source_type,evidence_class,excerpt,used_in,confidence,limitations
```

[25-source-register.md](25-source-register.md) consolidates the fragments and records coverage statistics. `data/source-register.csv` is the merged, machine-readable register. Internal repository files are cited by path and are not registered.

## 5. Use of prior research

Before researching, each agent read the internal studies relevant to its scope, for example:

- Ren/TIFIN/Chariot deep dives
- batch-2a/2b vetting
- migration runbook
- switching-cost matrix
- charity-source inventories in `unbound/research/charity-sources`
- the 180-day decision record
- the servicing-economics package

New findings refine or contradict those studies explicitly and say so.

## 6. Requirements derivation and traceability

Requirements were derived only after the research and the adversarial review. Each proposed requirement records:

- identifier
- business rationale
- statement
- supporting research (file and section in this package)
- acceptance criteria
- dependencies
- security implications
- failure behaviour
- verification method
- existing requirements it refines

Identifiers are `UNB-CNET-*` for the charity network and `UNB-ONB-*` for onboarding. Neither prefix existed in `requirements/baseline/baseline.jsonl` on 2026-11-26.

Following the 2026-11-25 availability package, records are **proposed**. They do not amend the generated `AUTHORITATIVE-BASELINE.md` or any convergence clause. Adoption follows the owner ratification process.

## 7. Limitations

- No vendor demonstration, contract, implementation statement of work or customer interview was available. Implementation timelines and prices are mostly vendor claims or public-sector procurement records.
- Several vendors publish very little about their charity networks. Coverage figures for directory, active and verified-payment-destination counts are therefore often unknown. The registers record them as unknown and do not estimate them silently.
- The economic model is a parameterized scenario model. Most parameters are ASSUMPTION-class and are marked as such. Its outputs are decision aids, not forecasts.
- Web pages change. Access dates are recorded; the content of a page may differ after 2026-11-26.
