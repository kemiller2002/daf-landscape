# AI-native DAF enterprise: research and architecture

This workstream designs, from first principles, a donor-advised fund enterprise in which AI, deterministic automation, APIs, structured knowledge and accountable human governance operate as one system. It then tests that design against the evidence in this repository.

It treats the claim that an AI-native DAF is better as a **hypothesis**. Executive conclusions are in [`14-executive-conclusions/`](14-executive-conclusions/).

## Reading order

1. [Executive report](14-executive-conclusions/executive-report.md): the whole organization on one path.
2. [Progress ledger](PROGRESS-LEDGER.md) and [decision log](DECISION-LOG.md).
3. [Research inventory](00-research-inventory/): what the existing repository already establishes, and what it does not.
4. [Outcome model](01-enterprise-outcomes/outcome-model.md): what the enterprise must accomplish, with decisions typed D/P/H.
5. [Capability map](02-business-capabilities/capability-map.md), [organization model](02-business-capabilities/organization-model.md) and [functional-area redesigns A–N](02-business-capabilities/).
6. [Workflows](03-workflow-redesign/), [APIs](04-enterprise-apis/), [agents](05-agent-architecture/), [data and events](06-data-and-knowledge/), [technology](07-technology-architecture/).
7. [Governance and compliance](08-governance-and-compliance/), [financial models](09-financial-models/), [market and business models A–D](10-market-and-business-model/).
8. [Scenarios and digital twin](11-scenarios-and-validation/), [roadmap](12-implementation-roadmap/), [Clarity/EDF analysis](13-clarity-edf-analysis/).

## Executable models

[`models/`](models/) is an F# (.NET 8) solution. It contains:
- the canonical domain types;
- the grant decision pipeline;
- an end-to-end reference journey;
- the staffing and cost model;
- the digital twin.

All of them are exercised by tests:

```
cd research/ai-native-daf-enterprise/models
dotnet test
```

## Evidence conventions

Labels follow the repository's existing conventions, as set out in the [industry report](../DAF-INDUSTRY-REPORT-2026-11.md) header:

| Label | Meaning |
|---|---|
| **[V]** | Validated |
| **[I]** | Inference |
| **[S]** | Scenario |
| **[A]** | Assumption, a new label introduced in this workstream for model parameters with no source |
| **EV-nnn** | Evidence register row |
| **GAP-nnn** | Gap register row |
| **DD-nnn** | Design decision |
| **REG-nnn** | Regulatory requirement |

This is research. It is not legal, tax or investment advice, and it is not authorization to operate a charitable organization.
