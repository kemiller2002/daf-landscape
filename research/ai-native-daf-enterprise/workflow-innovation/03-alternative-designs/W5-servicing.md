# W5: Donor and advisor servicing

This covers status, how-to questions, documents, changes and recovery.

**Outcomes:**
- BO-42: the donor knows status without asking.
- BO-43: accurate general tax information, including when *not* to use a DAF.
- BO-57: successors take over correctly.
- O-09: information accuracy.

**Evidence:**
- No top-20 sponsor publishes a response-time promise ([`direction-sponsor-accessibility-service.md`](../../../mission-2026-11-14/direction-sponsor-accessibility-service.md)).
- Review-venue complaints exist at Fidelity Charitable and RCF only among the top 15; Fidelity's rate is 1.32 per 10,000 accounts, and rates are unreliable as a quality measure ([`gap19-complaints-with-denominators.md`](../../../mission-2026-11-14/gap19-complaints-with-denominators.md)).
- Automated checks found critical accessibility failures on 7 of 37 pages (EV-127).
- **No contact-volume data** (GAP-006).

## 1. First principles

| Element | Necessary content |
|---|---|
| **Information** | Authoritative account and grant state; approved policy text; the donor's own documents |
| **Authority** | Factual answers need no authority (read state). Exceptions, goodwill credits and successor disputes need a person (outcome-decisions DEC-054 to DEC-056, DEC-072) |
| **Resources** | State projections; notifications; a grounded answer capability; a small recovery team |
| **Actions** | Tell people what changed, before they ask; answer questions from state and policy; resolve exceptions; recover from failures |

**Key observation:** a large share of servicing is **compensation for hidden state**. The workload is a symptom, not an outcome.

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate? | Status inquiries can be eliminated by shared state plus proactive events; their function (knowing status) is replaced by notifications and a visible grant timeline |
| No ticket? | Service can be a property of the operating system: every state change that affects a person produces a notification with the reason and the next step |
| Begin before the request? | Yes: anticipate predictable needs (year-end acknowledgments, grant returns, recipient status changes) |
| External partner? | Advisors already serve their clients; embedded status in advisor platforms (W7) removes a channel |

## 3. Designs

| # | Design | Mechanism | Who decides | When | Authoritative data | Human roles | Controls | Cost drivers | Experience | Maturity | INN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | **Conventional baseline** | Call center plus email queue; agents look up multiple systems; tickets | Service agent | After the donor asks | Several systems (copies) | Tier-1 and tier-2 staff | QA sampling | Contacts × handle time | Hold times; inconsistent answers | Observed (volumes unpublished) | — |
| D2 | **Automation-first** | Chatbot over FAQ; ticket routing; CRM integration | Agent; bot for FAQs | After asking | CRM copy | Fewer tier-1 | Bot deflection metrics | Lower handle time | Faster FAQs; bot frustration | L1 | — |
| D3 | **AI-native (parent)** | Grounded answer agent reads authoritative state and approved policy clauses (citations required); humans for exceptions | Rule (facts); person (exceptions) | After asking, instant | Event-ledger projections | Service recovery team | Grounding checks; no tax advice; QA sampling | Contacts reaching humans × minutes | Instant accurate answers | L1 | INN-14 |
| D4 | **Radical: zero-ticket, event-native service** | Service is redesigned as *outbound*. Every state change relevant to a donor, advisor or recipient emits a notification with the reason and the next action ("Grant G-123 held: recipient status changed on IRS list dated …; nothing for you to do; we will decide by …"). The shared grant timeline is the service channel. The only inbound channel is "something is wrong", which goes straight to a recovery specialist with full event history. FAQs are replaced by contextual explanations generated from policy clauses at the point of use | Rule (notifications from events); person (recovery) | Before the donor asks | Events | Small recovery team | Notification correctness tests; complaint taxonomy; accessibility conformance | Recovery cases × minutes | No need to ask; fewer, harder human cases | L1 | INN-14, INN-37 |
| D5 | **Externalized / ecosystem: advisor-embedded service** | The advisor's platform shows DAF status and actions via APIs; the advisor is the first line; the sponsor serves the advisor | Advisor (first line); sponsor (exceptions) | In the advisor's workflow | Sponsor APIs | Partner support | Delegation tokens (INN-16) | Partner support cost | Clients served by their advisor; sponsor invisible | L2 (channel premise; industry report §2.2) | INN-15, INN-16 |
| D6 | **Donor agents as the interface (extra)** | Donors' own AI assistants query and act through delegated, capped agent-principal tokens | Donor's delegation; sponsor rules | Whenever the donor's agent acts | Sponsor APIs | Donor confirms above caps | INV-A6 caps (tested) | Low | Natural-language self-service | L3 (parent PoC INV-A6) | INN-26 |

## 4. Constraint ledger

| Constraint | Dies | Modified | Survives |
|---|---|---|---|
| **Legal** (no individualized tax advice from the sponsor; accurate statements; accessibility law exposure) | "AI gives personalized tax recommendations" | Answers give general information with the direct-gift comparison and refer out; accessibility conformance required (EV-127) | D2–D6 |
| **Fiduciary** | — | — | All |
| **Accounting** | — | Statements generated from the ledger, not separate copies | D3–D6 |
| **Privacy / security** | Notifications revealing anonymous grants or donor identity | Notifications respect anonymity and channel authentication; step-up for changes | All modified |
| **Economic** | D1 at scale | — | D3–D6 |
| **Operational** | — | D4 needs disciplined event semantics; bad notifications create contacts | D4 modified |
| **Human acceptance** | — | Some donors want a person; D4 keeps a human recovery channel; elderly and less-digital donors need phone access | D4 with human channel |

## 5. Analogies

- T8: logistics track-and-trace.
- T6: airline operations notifications during disruption.
- T10: autonomous systems' fallback to a human.

## 6. Creative competition

| Perspective | Position |
|---|---|
| **Inventor** | Remove the inbound channel entirely for status; make "contact us" only for problems |
| **Enterprise architect** | D4 is mostly free once the event catalog exists; notifications are consumers. Requires a `Notification` projection with templates per event and a correctness test per template |
| **Economist** | Value depends on the status share of contacts (unmeasured, GAP-006). If status is 60% of contacts [A], D4 removes most volume; if 20%, little |
| **Regulatory specialist** | Watch the tax-advice line and accessibility. Notifications about holds should cite policy, not judgments about the recipient (defamation risk with discretionary holds) |
| **Adversarial reviewer** | Outbound notifications are a phishing template: attackers will imitate them. Over-notification creates contacts. Removing the human channel harms vulnerable donors |
| **Customer advocate** | Proactive explanations beat any queue. Keep a phone line for recovery and accessibility |
| **Commercial strategist** | D5 is where distribution happens; D4 is table stakes |

**Disagreements:** the Inventor wants no inbound channel; the Customer advocate and Adversarial reviewer reject that. **Resolution:** keep a recovery channel and remove status-only intake.

**Unresolved:** the status share of contacts; donor acceptance of notification-first service.

## 7. Forwarded to experiments

| Candidate | Experiment | Metric |
|---|---|---|
| D1 vs D3 vs D4 | **E6** contact model under varying status-share assumptions, with surge | Human contacts; recovery cases; SLA breaches |
| D6 safety | Parent PoC INV-A6 (already tested) | — |
| Cost | **E11** | |
