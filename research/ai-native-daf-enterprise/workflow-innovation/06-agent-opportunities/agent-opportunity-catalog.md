# Agent opportunity catalog

**Data:** [`agent-opportunities.csv`](agent-opportunities.csv) (12 new agent opportunities, AGO-01 to AGO-12).
**Builds on:** the parent's 19 agents ([`../../05-agent-architecture/agent-catalog.csv`](../../05-agent-architecture/agent-catalog.csv), AG-01 to AG-19) and their [authority boundaries](../../05-agent-architecture/authority-boundaries.md) (INV-A1 to INV-A8).
**Constraints:**
- Categories 2 and 3 only.
- Tool scopes come from the closed set `read`, `propose`, `raise-flag`, `open-case`, `draft`, `send-templated`. This set is the type enforced in [`../../models/Daf.Enterprise/Domain.fs`](../../models/Daf.Enterprise/Domain.fs) and tested by INV-A5.
- No agent moves money, writes authoritative records, clears flags, publishes policy or approves its own output (Category 5).

## 1. Where AI reasoning helps, and where it must not decide

| Process (top workflow) | AI reasoning helps with | Must stay deterministic | Must stay human |
|---|---|---|---|
| W1 recipient verification | Explaining source diffs; resolving free-text recipient names (AG-01) | Passport refresh, the block-never-release rule, the eligibility class | Clearing potential sanctions true matches |
| W2 non-routine review | Assembling dossiers and drafting determinations (AG-04, AGO-02); checking attestations (AGO-11) | Determination expiry and scope; routing | Issuing determinations; benefit decisions |
| W3 disbursement | Answering recipient questions (AGO-04) | Payee cooling-off, gate checks, netting, remittance formatting | Exceptions on payee changes |
| W4 complex assets | Extracting gift-document terms (AGO-03, AG-07, AG-08) | Underwriting rules | Acceptance; Form 8283 signature |
| W5 servicing | Grounded answers (AG-09) | State projections, notifications | Service recovery |
| W6 and W8 portability and migration | Assembling packets (AGO-05) | Eligibility of the receiving sponsor; export checksums | Transfer approval (the sending sponsor) |
| W7 advisor channel | Advisor copilot (AG-10) | Delegation tokens, mandate checks | — |
| W9 dormant capital | Planning options (AGO-06) | Inactivity clock | Charitable default distribution |
| W10 compliance evidence | Narrating evidence (AGO-07, AG-19); drafting policy (AGO-08, AG-13) | Evidence ledger, coverage tests, compiler and back-test | Filing sign-off; policy approval |

**Value mechanism, stated honestly:**
- In most rows **the work is eliminated by a deterministic mechanism**: passports, determinations reuse, registries, shared state.
- Agents mostly **accelerate** the human residual.
- The exceptions are AGO-04 (recipient status calls), AGO-05 (transfer paperwork) and AGO-09 (surge overtime), where an agent replaces a human-performed activity entirely.

This matches the parent finding that the redesign, not the AI, creates the value.

## 2. New agents (summary)

| ID | Agent | Category | Tool scopes | Human authorization point | Value |
|---|---|---|---|---|---|
| AGO-01 | Passport source-diff reviewer | 2 | read, draft, open-case, raise-flag | Hold release by grants compliance | accelerate |
| AGO-02 | Determination drafter | 2 | read, draft, open-case | Specialist issues every determination | accelerate (reuse eliminates) |
| AGO-03 | Asset underwriting extractor | 2 | read, propose, raise-flag, draft | Acceptance; Form 8283 | accelerate |
| AGO-04 | Recipient inbox concierge | 3 | read, send-templated, open-case | Payee changes | eliminate |
| AGO-05 | Transfer packet assembler | 3 | read, draft, send-templated | Transfer approval | eliminate |
| AGO-06 | Dormant capital planner | 2 | read, draft, send-templated | Donor choice; policy defaults | eliminate outreach labor (outcome effect unproven) |
| AGO-07 | Audit package narrator | 2 | read, draft | CRCO release | accelerate |
| AGO-08 | Policy compiler assistant | 2 | read, draft, propose | GC approval; change board | accelerate |
| AGO-09 | Surge load leveler | 2 | read, propose, send-templated | Donor and specialist acceptance | eliminate surge overtime |
| AGO-10 | Shared-pool case router assistant | 2 | read, draft, open-case | Specialist under that sponsor's delegation | accelerate |
| AGO-11 | Recipient attestation checker | 2 | read, raise-flag | Specialist | accelerate detection |
| AGO-12 | Network evidence curator | 2 | read, raise-flag, open-case | Network data steward | prevent propagation |

**Evaluation data:** no public labeled datasets exist for any of these (parent agent-architecture finding). Each needs a synthetic adversarial set plus a design partner's historical data. Acceptance thresholds are set as design targets, recall-first for flaggers, as in the parent harness. No accuracy figures are claimed.

**Failure detection specific to the new agents:**
- AGO-10 must show **zero** cross-tenant leakage on redaction tests.
- AGO-07 output is rejected if any sentence lacks an evidence citation.
- AGO-12 recall on seeded conflicting contributions.

## 3. Reconciliation of agent names used elsewhere

| Name used in parent functional areas or workflows | Maps to | Note |
|---|---|---|
| asset dossier | AG-07 Complex asset dossier | Same |
| break-triage | AG-06 Reconciliation break triage | Same |
| foreign-diligence | AG-04 Exception grant dossier preparer, plus AGO-02 Determination drafter | Foreign cases use AG-04 for the grant and AGO-02 for the reusable determination |
| compliance drafting | AG-13 Policy drafting and impact analysis, plus AGO-08 | AGO-08 adds compiler test generation |
| evidence extraction agent | AG-08 Document extraction | Same |
| identity-risk model | Not an agent: a deterministic-threshold **P** model in C1.1 (DEC-012) | Its score feeds a fixed threshold; it raises flags only |
| QA sampler | **Not an agent.** A deterministic sampling engine (CTL-046 and CTL-049; INN-06) | Sample selection must be unpredictable to reviewers and must not be model-chosen |
| fairness monitor | Deterministic metrics job plus AG-11 reporting | Fairness metrics are computed, not judged |
| sentiment/complaint classifier | AG-09 Service answer agent (classification sub-task) | Category 2; flags service recovery |
| partner due-diligence assistant | AG-15 SOC report analyzer (extended scope) | Vendor and partner diligence |
| manager due-diligence analyst | AG-15 scope extension, or new Category 2 under the investment committee | Investment committee decides |
| integration assistant | Developer tooling, not a production agent | Out of scope for the production authority model |
| proposal drafter | AG-10 Advisor copilot (drafting) | Commercial documents only |
| security triage assistant | Security tooling (SOC), not part of the business agent catalog | Governed by the security architecture |
| benefit-risk | AG-02 | Same |
| resolution | AG-01 | Same |
| post-grant | AG-12 | Same |
| service | AG-09 | Same |
| improvement | AG-16 | Same |
| document | AG-08 | Same |

**Result:** 19 parent agents plus 12 new opportunities give **31 agent families**. Four parent-referenced names are deliberately *not* agents (QA sampler, identity-risk model, fairness monitor, integration assistant). The parent cost model assumed 18 agent families. If all 31 reach production, agent-ownership FTE rises by about 2 at 6 families per owner. That is a small cost against the model's sensitivity ranges.
