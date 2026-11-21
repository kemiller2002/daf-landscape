# W2: Non-routine grant review

This covers grants to foreign recipients, grants requiring expenditure responsibility (ER), grants through fiscal sponsors, grants to new organizations, benefit and related-party cases, and discretionary holds.

**Outcomes:**
- BO-24: no prohibited benefit.
- BO-25: foreign grants meet equivalency determination (ED) or ER.
- BO-26: non-charity grants meet ER.
- BO-27: the charitable purpose of fiscal-sponsor grants is confirmed.
- BO-29: holds are decided on policy.

**Evidence:**
- The like-for-like non-standard share is about 4.2% of dollars at the four largest nationals (EV-080).
- The core proxy is 7.76% of lines and 11.61% of dollars across the top 50 (EV-079), and about 7–8.5% of grants (EV-081).
- Foreign grants are 1.46% of dollars across four nationals (NPT 4.84%).
- **No handling-minute data exists** (GAP-001).

## 1. First principles

| Element | Necessary content |
|---|---|
| **Information** | The legal character of the recipient and of the arrangement (foreign entity, fiscal-sponsorship terms, ER pre-grant inquiry, reports); relationships between account parties and the recipient; purpose and benefit indicators |
| **Authority** | A named, delegated person for ER and ED decisions, benefit cases, sanctions true matches and holds (regulatory map §12); the board for hold *policy* |
| **Resources** | Specialists; foreign legal documents; translation; prior determinations |
| **Actions** | Determine (ED, ER, fiscal-sponsor review); attach the determination to the grant; track ER reports; decide benefit and related-party cases |

**Key observation:** most of the legal judgment attaches to the **organization or arrangement** (an ED of a foreign charity, or a fiscal sponsor's program agreement), not to the individual grant. Only benefit and related-party questions are genuinely per-grant.

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate? | No. The legal judgment is irreducible. But *repetition* of judgment can be eliminated: a determination is made once, scoped and given an expiry |
| Begin before the request? | Yes. Pre-qualify foreign and fiscal-sponsor recipients that donors frequently use; pre-clear in November (twin surge finding) |
| External partner? | Yes, for *preparation*: ED providers and shared specialist pools. Not for the *decision* |
| No approval queue? | Not for this tier. The queue can become skill-routed cases with dossiers (parent C5.3) |

## 3. Designs

| # | Design | Mechanism | Who decides | When | Authoritative data | Human roles | Controls | Cost drivers | Experience | Maturity | INN |
|---|---|---|---|---|---|---|---|---|---|---|---|
| D1 | **Conventional baseline** | Grant enters a manual queue; specialist researches from scratch; documents emailed | Specialist per grant | At request | Specialist's file | Specialist per grant | Supervisor review (inferred) | Minutes × non-routine grants | Weeks for foreign grants; opaque | Observed practice (minutes unpublished) | — |
| D2 | **Automation-first** | Same queue; document collection portal; checklists; reminders for ER reports | Specialist per grant | At request | Case file | Specialist per grant | Checklist completion | Same, slightly lower | Portal visibility | L1 | — |
| D3 | **AI-native (parent design)** | Flags route to one skill-routed queue; an agent prepares a dossier (sources, prior grants, risk notes); the specialist decides; AI never clears | Specialist (H) | At request | Decision record with evidence viewed | Specialist decides; agent owner supervises dossier quality | Flag-only AI; seeded errors (CTL-046); role-based clearance (tested) | Minutes per case reduced by dossier [A] | Status visible; faster | L3 (parent PoC: role and authority limits tested) | INN-05 |
| D4 | **Radical: determinations as reusable, expiring assets** | The unit of work changes from *grant* to *determination*. An ED, ER pre-qualification or fiscal-sponsor review is a versioned artifact with scope (which purposes and amounts), expiry and triggers (filing changes, sanctions events). Grants that fall inside a valid determination's scope are decided by rule plus the determination reference. Only out-of-scope or expired cases reach a person. Benefit and related-party flags remain per-grant | Specialist decides each *determination* (H); rule applies it to grants | When the first grant arrives or proactively (pre-qualification); on expiry or trigger | Determination store | Specialist makes and renews determinations | Expiry monitor; scope check; change triggers revoke scope | Determinations × minutes (falls with the reuse factor) | Repeat foreign grants become fast; first one still slow | L2 (clustering premise: 12.5 grants/recipient; reuse factor unmeasured) | INN-04 |
| D5 | **Externalized / ecosystem: shared specialist pool plus ED provider** | Multiple sponsors route cases to a shared, pooled specialist team operating under *each sponsor's* delegated authority; ED preparation is bought from specialist providers; determinations may be shared where counsel approves | Each sponsor's delegate (pooled staff acting under that sponsor's DOA) | At request; pooled capacity absorbs surges | Each sponsor's decision record | Pooled specialists; each sponsor's CRCO oversees | Tenant isolation; consistency audits; conflict checks | Pool utilization; lower per case | Faster in surges | L1 | INN-28 |
| D6 | **Counterparty evidence: recipient attestation (extra)** | For benefit-risk flags, the recipient attests (no goods or services, no pledge satisfaction); attestation adds evidence; the specialist decides conflicts | Specialist | At recipient enrollment and on flag | Attestation plus decision | Specialist for conflicts | False-attestation consequences in recipient terms | Recipient time | Burden moves partly to nonprofit | L0 | INN-29 |

## 4. Constraint ledger

| Constraint | Dies | Modified | Survives |
|---|---|---|---|
| **Legal** (§4966(c)(1)(B), §4945(h) ER; §4967; ED rules; reliance on others' EDs unverified, Notice 2006-109) | Any design where AI or a rule *makes* a determination | D4: determinations made only by a person; D5: sharing of determinations across sponsors only with counsel approval; within-sponsor reuse is the base case | D2–D6 |
| **Fiduciary** | — | D5: the decision stays with each sponsor's delegate | All |
| **Accounting** | — | ER grant reporting and follow-up must be tracked | All |
| **Privacy / security** | — | D5: cross-sponsor case data needs tenant isolation | D5 modified |
| **Economic** | D1 at scale | D4's value depends on the reuse factor | D3, D4, D5 |
| **Operational** | — | D4: expiry and trigger monitors are essential, or stale determinations are reused | D4 modified |
| **Human acceptance** | — | D6: recipient burden; small charities may decline | D6 weak |

## 5. Analogies

- T3: insurance underwriting by class.
- T4: reinsurance and shared services.
- T12: policy compiler, where a determination is like a compiled module with a version.

## 6. Creative competition

| Perspective | Position |
|---|---|
| **Inventor** | Make determinations portable: an ED travels with the foreign charity like a passport, published by the charity itself |
| **Enterprise architect** | D4 needs a new entity, `Determination(scope, expiry, triggers)`, plus an evaluation step in `Policy.decide`. This is the "shared-determination entity" gap noted by the workflows fork |
| **Economist** | D4's benefit is reuse factor × minutes. With 12.5 grants per recipient, even modest recurrence of non-routine recipients could cut specialist load by half or more. **Unmeasured** |
| **Regulatory specialist** | Within-sponsor reuse of an ED for a defined period is standard foundation practice [I]. Cross-sponsor reliance is uncertain. ER requires *per-grant* reports from the grantee, which reuse does not remove |
| **Adversarial reviewer** | D4 risks stale determinations when facts change (new officers, sanctions designations, purpose drift). The "triggers" depend on data that foreign entities rarely publish. D5 risks inconsistent decisions across tenants |
| **Customer advocate** | Donors supporting overseas causes face the longest waits today; D4 helps repeat donors most. First-time foreign grants remain slow |
| **Commercial strategist** | D4 within a multi-sponsor platform (Model C) accumulates determinations; if sharing is lawful, that becomes a cross-sponsor asset |

**Disagreements:** the Regulatory specialist and the Inventor disagree on portable EDs. Unresolved; it needs counsel and the content of the §§4966/6033 guidance (GAP-008).

**Unresolved:** the reuse factor; legal reliance across sponsors; the share of non-routine cases that are benefit cases (inherently per-grant).

## 7. Forwarded to experiments

| Candidate | Experiment | Metric |
|---|---|---|
| D3 vs D4 vs D5 | **E2** approval architectures with determination reuse; **E6** pooled vs separate specialist capacity under surge | Specialist hours; SLA breaches; stale-determination escapes |
| D3 dossier | **E10** AI exception classification: flag-only vs auto-clear on a noisy classifier | Escaped defects; workload |
| Cost | **E11** | |
