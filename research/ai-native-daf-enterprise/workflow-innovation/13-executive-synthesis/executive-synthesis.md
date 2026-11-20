# Workflow reinvention: executive synthesis

**Date:** 2026-11-20. **Status:** research. Every conclusion carries its evidence class. **Nothing here is operationally validated (L4).** The highest level reached is L3, meaning it works in a model, for 3 of 48 innovations.

**The question asked:** *Why does the organization perform this activity at all, what outcome does it actually produce, and what entirely different mechanism could produce a better result?* It was asked of 64 business outcomes, and in depth of the 10 workflows the evidence ranks as most costly or structurally inefficient.

## 1. What was produced

| Deliverable | Content |
|---|---|
| [Methodology](../00-methodology/methodology.md) | Six creative methods; maturity ladder L0–L4; ten evaluation criteria fixed before scoring |
| [Outcome inventory and top-10](../01-existing-outcomes/audit-and-outcome-inventory.md) | 64 business outcomes; 10 workflows ranked on evidence strength, not invented numbers |
| [Creative hypotheses](../02-creative-hypotheses/) | 48-innovation register (17 required fields plus audit columns); 16 cross-industry transfers; 16 contrarian hypotheses; inversion ledger |
| [Alternative designs](../03-alternative-designs/README.md) | 105 competing designs: ≥5 per workflow and capability, with constraint ledgers and seven-perspective competitions |
| [Cross-enterprise workflows](../04-cross-enterprise-workflows/README.md) | 31 redesigns (XW-01…XW-31) with events, D/P/H decisions, state, APIs, agents, controls and human interventions |
| [API](../05-api-opportunities/api-opportunity-catalog.md) and [agent](../06-agent-opportunities/agent-opportunity-catalog.md) opportunity catalogs | 16 API opportunities with visible reuse components; 12 new agents; name reconciliation |
| [Independent adversarial review](../07-adversarial-reviews/adversarial-review.md) | Non-author agent: 7 survive, 19 survive with modifications, 4 insufficient evidence, 2 do not survive; 8 innovation downgrades; experiments audited |
| [Experiments](../08-experiments/experiments.md) | E1–E10 in F# (75 tests passing) plus **E7 and E7b on public data**; revised after audit |
| [Economic validation](../09-economic-validation/economic-validation.md) | Designs and eight business models; network economics on the measured reuse curve |
| [Prioritization](../10-prioritization/prioritization.md) | Ten dimensions; five separate rankings |
| [Reference architecture](../11-reference-architectures/integrated-process-architecture.md) | Five layers; network attachment; trust boundaries |
| [Implementation proposals](../12-implementation-proposals/implementation-roadmap.md) and [framework proposals](../12-implementation-proposals/framework-feedback-proposals.md) | Evidence-ordered waves; 14 generalizable patterns (not applied to the empty framework repository) |

## 2. The answer, by evidence class

### What the public evidence shows (L2)

1. **Recipient verification is repeated across sponsors at scale.** In FY2023, 71.3% of top-50 Schedule I lines (77.2% of dollars) went to recipients another top-50 sponsor also funded. A shared record would have avoided 51.3% of sponsor-recipient checks (E7, 48 sponsors, 279,337 lines).
2. **The repetition is concentrated where verification is cheap,** in large, well-documented charities. **It is strongest where verification is costly only for fiscal-sponsor hosts:** 82.1% of host reviews are avoidable. **It is weak for unlisted recipients** (29.8%) (E7b). Foreign recipients cannot be tested from public filings.
3. **Network reuse is strongly order-dependent.** The second joiner reuses 69% if large sponsors join first, 4% if small sponsors do. Any shared network faces a cold start in which the largest sponsors create the value and gain least.

### What the models show (L3 in a model; parameter-dependent per the audit)

4. **Flag-only AI bounds the downside.** Under prompt injection, escapes rise only to about the level of reviewing everything manually. Auto-close and auto-clear go beyond that, and get worse after distribution shift (E2, E10).
5. **A silently broken deterministic rule is invisible to AI monitoring and to 2% sampling. Daily known-answer canaries catch it on day 1** (E2). This is a new required control.
6. **The recipient "passport" saves work only if it is driven by source changes (diffs);** a naive monthly refresh does *more* work than per-grant lookup (E1). Its real value is latency and consistent, dated evidence. Accuracy is bounded by the IRS publication cadence, whatever the architecture.
7. **Exactly-once payments need a durable outbox *and* counterparty deduplication** (E9, a specification). ACH lacks an end-to-end key, so bank API support becomes a counterparty-selection criterion.
8. **Correlated year-end surges defeat cross-sponsor pooling** (−3% to −6% FTE). **Deferral windows cut peak specialist FTE by about 29%,** if donors accept January execution, which is untested (E6).
9. **Netting grants per recipient per day cuts payments by 39%** at observed-style concentration, and widens each incident's blast radius (E3).

### What does *not* survive

- **Acceptance sampling as a replacement for review** (INN-06): it lets more defects escape than reviewing everything.
- **Pay first, assure later** (INN-35): the sponsor's decision must precede payment.
- **AI auto-clearing flags.**
- **The claim that AI-native approval dominates manual review on both cost and control.** The audit's sensitivity reruns show it wins on *one* criterion under each assumption set. That is not robust.
- **Continuous close as a labor saving:** the whole saving came from one assumption (E4). Only earlier detection holds.
- **Routine eligibility verification as a standalone business,** and the verification network as a business built on routine checks. Members save about $2.9m a year across the top 48, and an operator never breaks even (09 §4).

### Invented and plausible (L0–L1), and why they are still worth testing

- Execution-window deferral (INN-37).
- Spend-down horizons and charitable defaults (INN-19).
- Advisor-embedded invisible DAF (INN-15).
- Policy compiler (INN-21).
- Reusable determinations (INN-04).
- Sponsor-owned record substrate (INN-44).
- Two-sided recipient registry and inbox (INN-07/38).

Each has a stated mechanism and a test in [ranking 5](../10-prioritization/prioritization.md).

## 3. Activities that need not exist, and what replaces their function

| Activity eliminated (in model) | What replaces the underlying function | Evidence class |
|---|---|---|
| Per-grant eligibility and sanctions lookups | Diff-driven recipient record plus list-change rescreen; a decision reads pinned evidence | L3 (model) |
| Manual review of routine grants | Board-approved policy-as-code plus canaries plus exception routing | L3 (parent PoC); ranking against manual parameter-dependent |
| Repeated host diligence on fiscal sponsors across sponsors | Shared host-diligence record (each sponsor still decides) | L2 (E7b overlap); value and reliance unproven |
| Recipient-side matching of grants to deposits | Grant ID carried in remittance | L1–L2 (problem evidenced; benefit assumed) |
| Platform-migration history loss | Event-log replay | L2–L3 (by construction) |
| Year-end overtime and peak hiring | Deferral windows | L1 (behavior untested) |
| Status inquiries | Shared state plus proactive events | L1 |
| Annual evidence reconstruction for auditors | Evidence emitted by operating controls | L2–L3 partial |

## 4. How the reinvented enterprise differs from the parent design

The parent architecture (`research/ai-native-daf-enterprise/`) had already removed departments and per-grant manual review. This program **challenged that design and changed it**:
- **Canaries added** for every deterministic rule (FP-04).
- **Passport made diff-driven.**
- **Pooling deprioritized** in favor of deferral.
- **The network reframed** from a broad "charity verification network" to *shared costly-determination evidence, inside a multi-tenant platform first*.
- **Pricing.** Per-account administration pricing, the RCF→Ren reference, was preferred over per-grant API pricing.
- **Rail selection.** Bank API idempotency became a rail-selection criterion.
- **Overclaims retracted** after an independent audit.

## 5. Business models (brief §7)

**Do different operating models make workflows unnecessary?** Yes, for the operator:
- An infrastructure provider (Model C) never performs board, investment-committee or fundraising work.
- A verification network removes duplicate host diligence.
- An advisor-embedded platform removes branded acquisition.

**Do network effects exist?** The mechanism is demonstrated (E7, E7b). The value is thin on routine checks and plausible on costly determinations. The cold start is quantified. **The strongest risk-adjusted route still matches the parent conclusion:** a multi-tenant AI-native operating platform (C) that accumulates determination evidence across its own clients, earns a partner sponsor-of-record hybrid (D), and keeps a new sponsoring charity (B) as an option. A standalone neutral network or registry is a later, two-sided bet.

## 6. Most important next evidence

In order (see the implementation proposals):
1. A design-partner **shadow replay with timed human review**. It resolves GAP-001 and GAP-004, on which every cost and control ranking depends.
2. The **determination reuse factor**.
3. A **small-sponsor Schedule I harvest**, rerunning E7 and E7b. Public data; can be done now.
4. **Donor acceptance of execution windows**.
5. **Break cost by age**.
6. A **red-team of the AI flagger**, including an adaptive adversary and automation bias.

## 7. Unresolved questions

- Can a sponsor lawfully rely on another sponsor's host diligence or equivalency determination (REG-019/020; counsel)?
- Will large sponsors anchor a shared network, and on what governance terms?
- Do human reviewers in fact catch related-party and benefit defects at the low rates assumed? This is the crux of E2.
- Will donors accept execution windows and spend-down defaults?
- Do banks used by sponsors offer idempotent payment APIs?
- Does the proposed §4966 treatment of advisers, if finalized, change the advisor-embedded model?
