# AI agent architecture

**Status:** design artifact, 2026-11-20.

**Companion files:**
- [`agent-catalog.md`](agent-catalog.md) and [`agent-catalog.csv`](agent-catalog.csv): 19 agents.
- [`authority-boundaries.md`](authority-boundaries.md): the action matrix and the invariants the proof of concept tests.

**Governing decisions:**
- DD-002: P never moves money or legal state.
- DD-003: requests are not instructions.
- DD-005: AI may add flags, never clear them.
- DD-007: no autonomous investment discretion.
- DD-017: donor-side agents are delegated principals.

## 1. The five participation categories

| Cat. | Name | What it does | Examples | Who is accountable |
|---|---|---|---|---|
| 1 | **Deterministic automation** | Explicit rules over structured data; same input → same output; versioned | Eligibility evaluation for listed public charities, posting rules, fee engine, payment gate, rebalancer within bands, acknowledgment generation | Policy owner of the rule set |
| 2 | **AI-assisted analysis** | Interpretation, classification, summarization, scoring. Output is a *proposal*, a *flag* or a *dossier* | Recipient resolution from free text, benefit-risk flags, break triage, document extraction, SOC report analysis | Agent owner (CTO line) for quality; the decision owner for use |
| 3 | **Supervised agent execution** | Bounded actions in *non-authoritative* systems, under explicit tool scopes. Examples: drafting, sending templated communications, assembling packets, opening cases, scheduling | Service answer agent replying to donors from grounded state; post-grant ER tracker sending reminders; board pack narrator drafting | Agent owner + capability owner |
| 4 | **Human-authorized decisions** | Material financial, legal, fiduciary or high-risk decisions by a named person within delegated authority | Non-routine grants, sanctions true-match clearance, complex asset acceptance, write-offs, policy publication, agent permission changes | The named approver |
| 5 | **Prohibited autonomous actions** | Never delegated to an AI agent, whatever its confidence | See §5 | Board (sets the prohibition) |

### Placement test (apply in order; the first "yes" fixes the category)

1. Would an error move money, change legal title or control, change an authoritative record, or create a legal or fiduciary obligation, **and** is no deterministic rule able to decide it? Then **Category 4**. If the action is also on the §5 list, it is **Category 5** for agents.
2. Can an explicit rule decide it from structured inputs, with an error rate the policy owner accepts? Then **Category 1**. Prefer this whenever it offers better reliability, cost or auditability.
3. Does it act only in non-authoritative systems (drafts, messages from approved templates or grounded answers, cases, schedules), and are the effects reversible or low-harm? Then **Category 3**.
4. Otherwise it is interpretation that informs a D or H decision: **Category 2**.

## 2. Runtime architecture

```mermaid
flowchart LR
  EV[Events / cases] --> ORCH[Agent orchestrator<br/>(durable workflow step)]
  ORCH --> RT[Agent runtime<br/>model + prompt version pinned]
  RT <--> TB[Tool broker<br/>least-privilege scopes per agent version]
  TB --> RO[Read tools<br/>projections, docs, registry, policy text]
  TB --> PF[Propose / flag tools<br/>create Proposal, raise Flag, open Case, draft Document]
  TB -. no route .-> X[Authoritative writes<br/>GrantApproved · PaymentInstructed · TradeInstructed · Ledger · Policy publish · Flag clear]
  RT --> VAL[Output validator<br/>JSON schema + grounding check + policy lint]
  VAL -->|valid| OUT[AgentRunCompleted event<br/>proposals / flags / drafts]
  VAL -->|invalid| DLQ[Discard + retry ≤2 → disable on repeat]
  OUT --> DET[Deterministic gate or Human case]
  RT --> TEL[AgentRun record:<br/>inputs refs, tool calls, outputs, cost, latency]
```

### 2.1 Tool broker (enforcement point)

- **The broker is the only path from an agent to enterprise systems.** Agents have no network egress except to the model endpoint and the broker.
- **Tool scopes are versioned policy objects.** Changing a scope is an `AgentPermissionChanged` event and requires an independent evaluation plus H approval from the change board and the CRCO.
- **The tool catalog has only three classes:**
  - **read**: authorized projections only, filtered by the subject's tenant and the agent's data-access policy;
  - **propose and flag**: `CreateProposal`, `RaiseFlag`, `OpenCase`, `AttachDossier`;
  - **non-authoritative effect**: `DraftDocument`, `SendTemplatedMessage` within approved templates and rate limits, `ScheduleReminder`.
- **No tool exists that emits** `GrantApproved`, `PaymentInstructed`, `TradeInstructed`, `PolicyPublished`, `AgentPermissionChanged`, a ledger posting, or a flag clearance. The forbidden actions are *absent*, not merely denied, so prompt injection cannot reach them.
- **Arguments are validated by schema.** Identifiers must resolve within the agent's authorized subject set, which blocks cross-account confused-deputy attacks.

### 2.2 Inputs and untrusted content

- Content from donors, recipients, documents and the web is **untrusted data**, wrapped and labeled as such in the prompt. Instructions inside it carry no authority.
- Agents that read untrusted content (resolution, document extraction, service, regulatory monitor) have **no effect tools beyond flag and propose**. Effect-capable agents (service replies, reminders) receive only templated or grounded outputs. Their free text passes a grounding checker: every factual claim must cite a state field or an approved policy clause ID.

### 2.3 Output validation

- Every output must match its JSON schema. Free-text rationale is allowed only as an attachment to a structured proposal.
- **Grounding check:** citations must resolve to records the run actually read (from the tool-call log).
- **Policy lint:** for example, no tax-advice phrases in service answers, and no "approved" language in grant communications unless a `GrantApproved` exists.

### 2.4 AgentRun record and versioning

Every run writes an `AgentRun` record:
- agent ID and version;
- model ID and provider;
- prompt template hash;
- tool-scope version;
- input record references, not copies;
- the tool-call log;
- outputs;
- flags raised;
- tokens and cost;
- latency;
- validator results.

A model or prompt change is a new agent version. Activating it is a deployment that requires the evaluation gate (§3).

### 2.5 Kill switches and degradation

- **Per-agent switch** (agent owner or CRCO): the work routes to a human case or to the deterministic-only path. **Degrading must never auto-approve.**
- **Category kill switch:** for example, disable all Category 3 effects enterprise-wide.
- **Circuit breakers trip automatically on:**
  - validator failure rate,
  - flag-rate deviation from baseline (both a spike and a *drop*; a drop can mean the model has silently stopped flagging),
  - cost per run,
  - latency.

### 2.6 Cost metering

Cost per AgentRun is recorded, and cost per *completed outcome* is computed by the telemetry capability (C6.2) by joining runs to the outcome's correlation ID. Unit-cost figures are in [agent-catalog.md §Cost method](agent-catalog.md#cost-method).

## 3. Evaluation harness

| Component | Purpose | Status of data |
|---|---|---|
| **Golden datasets** per agent | Labeled cases with expected proposals or flags | **None exist publicly.** They must be built during Phase 3–5 from four sources: (a) synthetic cases (the repository's 18 synthetic tax cases are a format precedent: `data/tax-opportunity-test-cases-2026.csv`); (b) public filings (Schedule I/F recipients, the IRS revocation list, OFAC SDN) for eligibility, sanctions and resolution; (c) de-identified operating history once operating; (d) expert-labeled samples |
| **Adversarial sets** | Prompt injection in recommendation purpose text, recipient names, uploaded documents and web pages; look-alike charity names; homoglyph EINs; sanctions-evasion transliterations | Must be built; red team owns them |
| **Regression gate** | A new agent version must equal or beat the incumbent on recall of risk flags (the primary metric) and stay within the precision and cost bands | Design targets in the catalog; *no accuracy figures are claimed* |
| **Shadow mode** | A new agent runs alongside the incumbent with outputs not used, for N cases, before activation | Phase 5 |
| **Drift monitoring** | Input distribution shift (new recipient types, new document templates); flag-rate drift; human-override rate (how often humans disagree with the proposal) | Continuous |
| **Independent validation** | The evaluation lead reports to the CTO with a dotted line to the CRCO. Model-risk sign-off belongs to the CRCO, not the agent owner | Organizational |

**Primary metric for flag agents: recall (missed-risk rate), not precision.** The flag-only rule makes false positives a cost (human time), while false negatives are risk escaping. Acceptance targets are therefore stated as *recall floors on the adversarial and golden sets* plus *precision floors that keep human queues within SLA*.

## 4. Agent-to-agent coordination rules

1. **No direct delegation chains.** An agent cannot invoke another agent. Coordination happens through events and cases: agent A's `AgentRunCompleted` carrying a proposal is an event the orchestrator may route to agent B, and each hop is a recorded workflow step.
2. **Causation-depth limit.** The default limit is 8 hops ([event catalog §4](../06-data-and-knowledge/event-catalog.md)). A chain exceeding it without a deterministic or human checkpoint is quarantined.
3. **No consensus-as-authority.** Two agents agreeing does not clear a flag or approve anything. Agent agreement is still P.
4. **No self-review.** An agent's output cannot be validated by the same agent version. Cross-checks use a deterministic validator or a different agent with a different prompt (and ideally a different model family), and the result is still only P.
5. **Shared context only through records.** Agents do not share memory. Everything they know is a record in the enterprise, which makes it auditable and replayable.

## 5. Category 5: prohibited autonomous actions

| # | Prohibited for any AI agent | Reason |
|---|---|---|
| P1 | Approve, release or instruct any grant, payment, transfer or trade | §4966/§4967 manager liability is personal; O-03 exclusive control; DD-002/DD-003 |
| P2 | Clear, downgrade or suppress a flag, alert or sanctions hit | DD-005; it converts risk-reduction into risk creation |
| P3 | Create, edit or delete authoritative records (ledger, positions, eligibility facts, parties' verified identity, privileges) | DD-006; replay and audit integrity |
| P4 | Publish or change policy, thresholds, model cut-offs, or its own or another agent's tool scope | DD-011; governance (O-10, O-18) |
| P5 | Add or change a payee's bank details, or verify a payment profile | Payee hijack is the main payment-fraud path (O-08) |
| P6 | Exercise investment discretion | DD-007 |
| P7 | Give individualized tax, legal or investment advice | O-09; DAF tax claims are often wrong ([`direction-donor-tax-scenarios-2026.md`](../../mission-2026-11-14/direction-donor-tax-scenarios-2026.md)) |
| P8 | Make, or communicate as made, a decision on a donor dispute, complaint resolution or goodwill credit | Human recourse (O-09) |
| P9 | File, sign or attest to any regulatory filing, acknowledgment signature (Form 8283 Part V) or audit representation | Officer accountability |
| P10 | Contact regulators, law enforcement or the media | GC accountability |
| P11 | Access raw secrets, credentials or unredacted bank account numbers | Least privilege (O-17) |
| P12 | Invoke another agent directly or extend its own run beyond the orchestrator's step budget | §4 |

These prohibitions are enforced structurally: the corresponding tools do not exist in the broker. They are **tested as invariants** in the F# proof of concept ([`authority-boundaries.md`](authority-boundaries.md) §3). They may be revisited only through the change process, with legal authority, validated controls and board approval (addendum §7 Category 5).

## Update (2026-11-21): public evaluation datasets now exist for two agent roles

The statement that no public evaluation datasets exist still holds for DAF-specific vetting judgments. It no longer holds for:
- **sanctions entity matching:** OpenSanctions Pairs, 755,540 labelled pairs (landscape LS-049);
- **charity-recipient resolution:** a labelled benchmark built from public Schedule I lines, [`data/charity-vetting-ai/resolution-eval-sample.csv`](../../../data/charity-vetting-ai/resolution-eval-sample.csv). See the [charity-vetting deep dive](../charity-vetting-ai/README.md) §3 and §7.

The sanctions near-match triage agent and the recipient-resolution agent should be evaluated on these sets before shadow deployment.
