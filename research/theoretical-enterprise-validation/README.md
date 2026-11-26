# DAF theoretical enterprise validation

This program tests the DAF enterprise requirements for gaps, contradictions, fragile economics and real-world failure, **without implementing anything**. It contains Markdown, Mermaid diagrams and CSV registers only.

**Start here:**
- [Executive findings](18-executive/executive-findings.md)
- [Theoretical readiness](17-readiness/readiness-report.md)
- [Owner decisions](16-registers/owner-decisions.md)
- [All open questions and data](19-questions/all-open-questions.md): 183 questions in one CSV

**Status:** theoretical. Nothing here is implemented, legally reviewed or independently validated, and it does not claim production readiness or SOC 1/SOC 2 compliance. Reviews were role-separated self-critique by one AI model family ([independence statement](00-program-charter.md#5-independence-statement)).

## Index

| # | Artifact | What it holds |
|---|---|---|
| 00 | [Program charter](00-program-charter.md) | Scope, governance mapping, evidence labels, ID scheme, stopping rules |
| 01 | [Requirements inventory](01-discovery/requirements-inventory.md) | Phase A: corpus, structural problems, domain coverage |
| 02 | [Enterprise ontology](02-ontology/enterprise-ontology.md) | Entities, ownership, authority conflicts, source-of-truth rules |
| 03 | [Domains, organization, authority](03-organization/organization-and-authority.md) | Domain partitions reconciled, function challenge, H/D/AI/agent allocation, SoD, authority evaluation |
| 05 | [Workflow catalog](05-workflows/workflow-catalog.md) | 44 workflows; 18-field specs for critical ones |
| 06 | [State models](06-state-models/state-models.md) | Recommendation, grant, payment attempt, reservation, contribution, fund, authority, flag, widget session, time basis (rev 2) |
| 07 | [Financial invariants](07-financial-invariants/financial-invariants.md) | Twelve financial facts; FI-01..39; concurrency table (rev 2) |
| 08 | [Compliance and controls](08-compliance/compliance-and-controls.md) | Authority classes, control-template gaps, TVCTL-01..14 |
| 09 | [Status vocabulary](09-ux/status-vocabulary.md), [personas and interaction models](09-ux/personas-and-interaction-models.md) | Five-dimension status; 21 personas; alternative interaction models; accessibility findings |
| 10 | [Widget integration model](10-widgets/widget-integration-model.md) | Trust boundaries, unspecified behaviours, cross-system trace |
| 11 | [Scenario library](11-scenarios/scenario-library.md), [scenarios.csv](11-scenarios/scenarios.csv) | Rounds 1–4, saturation tracking |
| 12 | [Failure analysis](12-failure-analysis/failure-analysis.md) | FMEA, fault trees, STRIDE, conjunction day, counterfactuals |
| 13 | [Role-separated reviews](13-adversarial-reviews/role-reviews.md) | Dispositions; [raw records](13-adversarial-reviews/raw/) |
| 14 | [Alternative operating models](14-alternative-operating-models/alternatives.md) | Funding, review, finality, reconciliation, succession, service, enterprise shape |
| 15 | [Economic model](15-economics/economic-model.md) | Specialist demand, surge, AI cost thresholds, correlated failure, sensitivity |
| 16 | Registers | [Findings](16-registers/findings.csv), [contradictions](16-registers/contradiction-register.md), [assumptions](16-registers/assumption-register.csv), [requirements graph](16-registers/requirements.csv), [owner decisions](16-registers/owner-decisions.md) |
| 17 | [Readiness report](17-readiness/readiness-report.md) | 18 criteria × domains; what not to implement yet |
| 18 | [Executive findings](18-executive/executive-findings.md) | The 15-section final report |
| 19 | [All open questions and data](19-questions/all-open-questions.md) | 183 questions consolidated from all registers; data inventory |
| — | [Ledger](LEDGER.md) | Checkpoints, metrics, continuation plan |

## How this relates to existing work

The program **reads** [`docs/`](../../docs/) and [`research/ai-native-daf-enterprise/`](../ai-native-daf-enterprise/) and does not edit them. New IDs use the `TV` prefix. Where it proposes to change a baseline rule, the conflict goes in the contradiction register for an owner decision.
