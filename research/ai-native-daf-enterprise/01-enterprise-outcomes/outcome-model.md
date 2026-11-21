# Enterprise outcome model

**Status:** design artifact, 2026-11-20. **Depends on:** existing repository research (cited by path) and the regulatory applicability map in [`../08-governance-and-compliance/`](../08-governance-and-compliance/).
**Rule:** no department, system or agent is defined in this file. Departments are derived later ([`../02-business-capabilities/`](../02-business-capabilities/)) and must trace back to an outcome here.

## 1. Method

Every outcome is decomposed into the same twelve fields: why it exists, who benefits, information required, decisions, decision type, completion condition, completion evidence, failure modes, detection and correction. Decision types:

| Code | Meaning | Who may make it |
|---|---|---|
| **D** | Deterministic: an explicit rule over structured data gives one answer | Versioned policy code, with the rule version recorded on the decision |
| **P** | Probabilistic: it needs interpretation, classification or estimation | An AI model or statistical method may *recommend*. It may raise a flag but never clear one ([`ai-governance-failure-modes.md`](../../mission-2026-11-14/ai-governance-failure-modes.md)) |
| **H** | Human-authorized: a material legal, fiduciary or financial judgment with personal accountability | A named, authorized person, with the evidence they saw recorded |

A decision gets the lowest code that is safe. **P** never stands alone for an action that moves money or changes legal state. It must resolve to **D** (the score is fed into a rule with a fixed threshold, and the threshold is human-approved policy) or to **H**.

## 2. The outcome set

There are eighteen outcomes. O-01 to O-14 are the ones the mission brief names. O-15 to O-18 were added because the evidence shows they are real obligations that the conventional model handles poorly:
- O-15, recipient service: nonprofits bear the cost of fragmented rails and thin donor data ([strategic synthesis §0 G4](../../mission-2026-11-14/strategic-synthesis.md)).
- O-16, continuity and portability: no top-12 sponsor publishes an outbound transfer policy, and AEF's migration kept two years of history ([industry report §4](../../DAF-INDUSTRY-REPORT-2026-11.md)).
- O-17, information protection.
- O-18, continuous improvement (addendum §21).

| ID | Outcome | Primary beneficiary | Legal basis or driver |
|---|---|---|---|
| O-01 | Accept eligible contributions and give a legally valid acknowledgment | Donor (deduction), sponsor (assets) | IRC §170(f)(8), §170(f)(18), §170(f)(11); acceptance policy |
| O-02 | Establish and administer donor-advised accounts | Donor, advisor | IRC §4966(d)(2) definition of a DAF; program agreement |
| O-03 | Maintain legal ownership and exclusive control of charitable assets | Charitable class, sponsor | §4966(d)(2)(A)(ii) "owned and controlled by" the sponsor; variance power |
| O-04 | Invest and safeguard charitable assets | Future grantees, donors | Board fiduciary duty; state prudent-investor / UPMIFA (applicability debated); §4943 excess business holdings |
| O-05 | Maintain accurate accounting and financial records | Board, auditors, regulators, donors | GAAP (ASC 958); Form 990; state audit thresholds |
| O-06 | Evaluate and execute grant recommendations | Nonprofits, donors | §4966 (taxable distributions), §4967 (prohibited benefits) |
| O-07 | Satisfy regulatory obligations | Sponsor (exemption), public | IRC Ch. 42; OFAC; state charity law |
| O-08 | Prevent fraud, misuse and prohibited benefits | Charitable class, donors | §4958, §4967; fiduciary duty |
| O-09 | Give donors and advisors accurate information | Donors, advisors | Program agreement; unfair and deceptive practice law; Reg BI at advisors' firms |
| O-10 | Maintain nonprofit governance and fiduciary oversight | Public, AGs, IRS | State nonprofit law; Form 990 Part VI |
| O-11 | Manage service providers and financial counterparties | Sponsor | Fiduciary duty of care; contracts |
| O-12 | Produce financial, operational, regulatory and tax reporting | Regulators, board, donors | Form 990 incl. Schedule D Part I (§6033(k)); audits; state filings |
| O-13 | Deliver measurable philanthropic value | Society, donors, nonprofits | Charitable purpose; donor intent |
| O-14 | Generate enough revenue to sustain operations | Sponsor's continuity | Economic necessity |
| O-15 | Deliver grants to recipients usefully: paid, identified, reconcilable | Nonprofits | Charitable purpose; recipient cost |
| O-16 | Preserve continuity: succession, inactivity, transfers, portability | Donors, successors, charitable class | Program agreement; inactivity policies |
| O-17 | Protect information, identity and access | Donors, sponsor | State breach and privacy laws; contracts; Schedule B confidentiality |
| O-18 | Learn and improve without weakening safeguards | All | Management duty; addendum §21 |

## 3. Outcome decomposition

### O-01 Accept eligible contributions and give a legally valid acknowledgment
- **Why it exists:** a DAF has no charitable function until assets arrive. The donor's deduction depends on a correct contemporaneous written acknowledgment, which for DAF contributions must state that the sponsor has exclusive legal control (§170(f)(18)(B)).
- **Who benefits:** the donor (deductibility), the sponsor (assets to administer), and grantees later.
- **Information required:** donor identity; asset identity (CUSIP or ISIN, crypto asset and chain, legal description, entity interest); quantity; transfer instruction; settlement confirmation from the custodian or bank; date of completed gift (the delivery rules differ by asset type); valuation basis (market close for listed securities; qualified appraisal for non-cash over $5,000, which the donor obtains); any donor restrictions or quid pro quo; source-of-funds risk indicators.
- **Decisions:**

| Decision | Type | Note |
|---|---|---|
| Is the asset class acceptable under policy? | D | Policy table |
| Is this specific complex asset acceptable (liabilities, liquidity, environmental, UBTI, excess business holdings)? | H | Specialist, with **P** analysis support |
| Is the gift complete, and on what date? | D | Settlement evidence plus asset-type rule |
| Valuation for the books | D (listed) / P→H (complex) | |
| Is the acknowledgment content correct? | D | Template plus facts; no human needed |
| Does it hit a sanctions or source-of-funds red flag? | D screen, P triage, H decision | |

- **Completion:** assets are in sponsor-controlled custody, booked to the account at the policy value, and the acknowledgment has been delivered and stored.
- **Evidence:** custodian settlement record ID; ledger entry referencing it; acknowledgment document hash and delivery receipt; acceptance decision record (rule version or approver).
- **Failure modes:** the acknowledgment omits the exclusive-control statement (the deduction is lost, per the *Keefer* strict-acknowledgment line in [`b50-01-daf-litigation.md`](../../mission-2026-11-14/b50-01-daf-litigation.md)); the wrong completed-gift date (year-end); an unsettled transfer booked as received; an unacceptable asset accepted (liability, excess business holding); a sanctioned donor; stock arrives without a donor identifier ("orphan" deposits).
- **Detection and correction:** three-way match of custodian, ledger and acknowledgment within one settlement cycle; acknowledgment content validated by a schema test on generation; unmatched deposits raised as exceptions at T+1; year-end cutoff rule tests.

### O-02 Establish and administer donor-advised accounts
- **Why:** §4966(d)(2) defines a DAF as a fund or account separately identified by reference to a donor's contributions, over which the donor or a person the donor appoints has (or reasonably expects) advisory privileges. Account structure is what makes the vehicle exist.
- **Who benefits:** donors, their advisors, and successors.
- **Information:** identity of each donor or advisor; relationships (spouse, successor, investment advisor, family member, a donor-controlled entity); agreements accepted, by version; privilege grants (who may recommend grants or investments); fee schedule; investment selection; communication preferences.
- **Decisions:**

| Decision | Type | Note |
|---|---|---|
| Is the identity verified to the required assurance level? | D | Rule plus identity-provider result; P for document-forgery scoring |
| Does the requested privilege structure fit policy? | D | |
| Is the account a special type (corporate DAF, scholarship-style, field-of-interest)? | D, H for exceptions | Different rules apply |
| Successor designation validity | D | |
| Does a relationship make someone a "disqualified person" for §4958/§4967 purposes? | D from declared relationships; P to detect undeclared ones; H to decide | |

- **Completion:** an account exists with verified parties, an accepted agreement version, a privilege map and a fee schedule.
- **Evidence:** identity verification result reference; agreement acceptance record (version, timestamp, E-SIGN consent); privilege grant events.
- **Failure modes:** an unverified advisor gains privileges; a stale agreement version is used; a relationship graph that is incomplete hides a disqualified person; an orphaned account (death, incapacity).
- **Detection:** privilege-grant events must reference a verification ID (enforced, not reviewed); relationship-graph completeness checks; inactivity monitors (see O-16).

### O-03 Maintain legal ownership and exclusive control
- **Why:** if the donor retains control, the gift is not complete and the vehicle fails. The sponsor's variance power and its final say over every grant and investment is the legal heart of a DAF.
- **Beneficiaries:** the charitable class, and the sponsor's exemption.
- **Information:** the authoritative position and title record per asset; the legal-control chain (custody account titled to the sponsor); the decision record for every grant and investment instruction showing the sponsor, not the donor, made it.
- **Decisions:** does every movement of assets carry a sponsor decision record (D, enforced structurally); variance-power exercise (H, board-delegated, rare).
- **Completion:** continuous. Assets are titled to the sponsor, and every state change has a sponsor-attributed decision.
- **Evidence:** custody account titling evidence; decision records with authority references; no direct donor-to-custodian instruction path.
- **Failure modes:** an API lets a donor or advisor instruct a custodian or payment rail directly (the design must make that structurally impossible); "rubber-stamp" practice that, if litigated, looks like donor control. In the cases studied, courts upheld sponsor control: *Fairbairn* and *Pinkert* ([`b50-01-daf-litigation.md`](../../mission-2026-11-14/b50-01-daf-litigation.md)).
- **Detection:** architecture invariant tests (no credential held by donor-facing components can call the money-movement capability); a periodic reconciliation of decision records to movements, where any movement without a decision is a critical incident.

**Design implication (DD-003):** every recommendation from a donor, an advisor or an agent acting for them is a *request*. Only the sponsor's policy engine or an authorized sponsor human turns a request into an *instruction*. This holds even for the "instant" path: an instant approval is a sponsor decision made by sponsor-owned code under sponsor-approved policy, recorded as such.

### O-04 Invest and safeguard charitable assets
- **Why:** assets must keep their value until granted. Investment policy is a board fiduciary act.
- **Beneficiaries:** future grantees and donors.
- **Information:** the investment policy statement (IPS); the model portfolio and pool definitions; positions and prices; liquidity requirements (forecast grant outflows); advisor mandates for advisor-managed accounts; excess business holdings tests (§4943 as applied to DAFs by §4943(e)).
- **Decisions:**

| Decision | Type | Note |
|---|---|---|
| IPS adoption and changes | H | Board or investment committee |
| Manager and pool selection | H | Investment committee, with **P** due-diligence analysis |
| Rebalancing to target within bands | D | Rule-based, executed through custodian orders after a deterministic pre-trade check |
| Donor investment-option selection | D | Validate against the menu |
| Advisor-managed trading within the mandate | D | Validate against mandate constraints; the advisor is a third-party fiduciary |
| Liquidity buffer sizing | D model + H approval of parameters | |
| Market-disruption response | H | Pre-approved playbooks may permit D actions within bounds |

- **Completion:** positions conform to the IPS and mandates; liquidity covers forecast outflows at the policy confidence level.
- **Evidence:** daily compliance check results (rule version, positions snapshot hash); trade records with pre-trade check IDs; committee minutes for H decisions.
- **Failure modes:** a breach of policy bands; a liquidity shortfall in a market crash, with grants unpayable; an advisor exceeding the mandate; excess business holdings from a gift of private stock; fee layering (the 990 does not show fund and adviser fees, per [strategic synthesis §0 G5](../../mission-2026-11-14/strategic-synthesis.md)).
- **Detection:** continuous position-versus-policy evaluation; liquidity forecast versus actual; advisor-fee reasonableness tests against a published cap.

**Hard boundary (DD-007):** no autonomous agent holds discretionary investment authority. Agents may analyse and draft. Execution is a deterministic rebalancer acting within human-approved parameters, or an external fiduciary acting within a mandate.

### O-05 Maintain accurate accounting and financial records
- **Why:** fund-level balances are what donors rely on, and the sponsor's audited statements are what regulators rely on.
- **Information:** every economic event (contribution settled, trade, income, fee accrual, grant approved, payment settled or returned, transfer), with the external evidence for each.
- **Decisions:** posting rules (D); unitization and NAV (D); fee calculation (D); accrual-versus-cash policies (H, adopted once); reconciliation-break resolution (D for known patterns, P triage, H for write-offs and adjustments above threshold).
- **Completion:** the sub-ledger (fund-level) and general ledger agree; the books agree with custodian and bank records each business day; close is a check rather than a project.
- **Evidence:** reconciliation results per day per account (match counts, breaks, aging); immutable journal with links to source events.
- **Failure modes:** unit-price errors; fee mis-accrual; reconciliation breaks left unaged; history lost in a platform migration ([industry report §4](../../DAF-INDUSTRY-REPORT-2026-11.md), AEF).
- **Detection:** daily three-way reconciliation; invariants (sum of fund balances equals pool NAV × units; cash in transit is explained); break aging service-level objectives.

### O-06 Evaluate and execute grant recommendations
- **Why:** grants are the charitable output. The law requires that DAF distributions be for charitable purposes to eligible recipients (§4966) and not confer more than incidental benefit on donors or advisors (§4967).
- **Information:** the recommendation (recipient, amount, purpose, restrictions, recognition preferences); recipient identity resolved to an EIN or foreign entity record; recipient status (Pub 78 / BMF public-charity class, revocation status, Type III supporting organization status, private foundation status); OFAC and other sanctions results; donor relationships to the recipient; prior grants; purpose text; any benefit indicators (tickets, tuition, pledge language, memberships).
- **Decisions:**

| Decision | Type | Note |
|---|---|---|
| Recipient resolution (which legal entity is meant) | D on an exact EIN; P on name-only input, with the donor confirming | |
| Eligibility class | D (IRS data, with the reliance rules of Rev. Proc. 2018-32) | |
| Sanctions | D screen; P triage of near-matches; **H** to clear a true potential match | |
| Benefit and private-benefit risk | P flag; **H** decides | |
| Routine approval for a listed public charity under threshold with no flags | D | Policy approves |
| Non-routine (foreign, non-public-charity requiring expenditure responsibility, fiscal sponsor, new organization, large, flagged) | H | With P-prepared dossier |
| Discretionary sponsor policy holds (for example the 2026 SPLC holds in [industry report §4](../../DAF-INDUSTRY-REPORT-2026-11.md)) | H, board-level policy | |

- **Completion:** funds are delivered to the recipient, the recipient is identified to the payment, and the grant has reconciled.
- **Evidence:** decision record (rule version, data snapshot dates for the BMF, Pub 78, revocation and OFAC lists, flags raised, approver if H); payment settlement reference; remittance delivered; ledger entries.
- **Failure modes:** a grant to a revoked or ineligible entity; a sanctions miss; a prohibited benefit (a pledge payment, tickets); the wrong entity paid (name ambiguity); a payment to a hijacked bank account; an uncashed check; review delays on routine grants.
- **Detection:** pre-payment gates; post-payment eligibility re-checks (status changes); payee-bank verification with change-of-bank cooling-off; uncashed-check aging; latency SLOs per path.

### O-07 Satisfy regulatory obligations
- **Why:** loss of exemption or excise tax liability ends or damages the enterprise. Managers face personal excise taxes for knowing violations (§4966(a)(2), §4967(a)(2)).
- **Information:** an obligation register (machine-readable requirements with citations; see the regulatory map); the evidence produced by every operating outcome; filing calendars; state registrations.
- **Decisions:** interpretation of law into policy (H, counsel); applying policy (D); filing sign-off (H, an officer); responding to an inquiry (H).
- **Completion:** every obligation in the register maps to a control, every control produces evidence continuously, and every filing is made on time.
- **Evidence:** control-evidence ledger; filing receipts; registration status per state.
- **Failure modes:** a requirement nobody owns; a policy that drifts from law; a missed state renewal; evidence that cannot be produced on request.
- **Detection:** the register's coverage test (an obligation without a control is a failing test); deadline monitors; evidence-sampling self-audits.

### O-08 Prevent fraud, misuse and prohibited benefits
- **Why:** charitable assets are a target: account takeover, payee bank hijack, insider diversion, sham charities, benefit schemes. The repository found no public DAF diversion case since 2021, but published MFA at only some sponsors ([`b49-04-fraud-diversion-controls.md`](../../mission-2026-11-14/b49-04-fraud-diversion-controls.md)).
- **Information:** login and device signals; behavioral baselines; payee bank changes; relationship graphs; grant patterns (circular flows, round-tripping to donor-controlled entities); employee access logs.
- **Decisions:** step-up authentication (D on risk score bands); hold or release a transaction (D for rule hits; P scoring; **H** to release a high-risk hold); report to law enforcement or a regulator (H).
- **Completion:** continuous. Losses stay within risk appetite, and every alert is closed with a reason.
- **Evidence:** alert ledger (raised by, closed by, reason, time); access reviews.
- **Failure modes:** authorized-push fraud (social engineering of the donor); an insider with both create-payee and approve-payment rights; an AI agent manipulated by prompt injection into recommending a fraudulent payee.
- **Detection:** segregation-of-duties invariants enforced in the authorization model; a payee-change cooling period; anomaly detection; red-team exercises.

### O-09 Give donors and advisors accurate information
- **Why:** donors decide, and advisors advise, on what the sponsor tells them. Incorrect tax implications cause harm. The repository shows DAFs are *not* tax-superior to direct giving for itemizers and lose for non-itemizers from 2026 ([`direction-donor-tax-scenarios-2026.md`](../../mission-2026-11-14/direction-donor-tax-scenarios-2026.md), via strategic synthesis §0 A).
- **Information:** account state (authoritative, real-time); grant status; policies; educational content with citations; donor's own data (with consent).
- **Decisions:** answering a factual account question (D, read from the authoritative state); answering a policy question (P, retrieval over approved policy text with citations, constrained); individualized tax advice (**excluded**: the sponsor gives general information only and refers out); service exceptions and goodwill credits (H above threshold).
- **Completion:** questions answered correctly, with sources, and escalations resolved.
- **Evidence:** conversation logs with retrieval citations and the state snapshot used; QA sampling results.
- **Failure modes:** a hallucinated policy; implied tax advice; stale status; an over-promised grant timeline.
- **Detection:** grounded-answer checks (every factual claim must cite a state field or policy clause); continuous QA sampling; complaint taxonomy.

### O-10 Maintain nonprofit governance and fiduciary oversight
- **Why:** the board is legally accountable. Its oversight has to be real, and it has to be shown.
- **Information:** a delegation-of-authority matrix; risk appetite; control health; financials; exceptions; conflicts.
- **Decisions:** strategy, policy, risk appetite, delegations, auditor appointment, CEO oversight, conflicted-transaction approval. All are H, and all belong to the board or a committee.
- **Completion:** decisions are recorded with the evidence considered; conflicts are disclosed and recused.
- **Evidence:** minutes, the delegation register, the conflict register, continuously refreshed control dashboards.
- **Failure modes:** the board sees only management-curated reports; vendor-related directors (for example Charityvest's president paid by Foundation Source, [industry report §2.3](../../DAF-INDUSTRY-REPORT-2026-11.md)); an AI system effectively setting policy through thresholds no one approved.
- **Detection:** policy parameters (thresholds, model cut-offs) are themselves governed objects with an approval record; an independent internal-audit line.

### O-11 Manage service providers and financial counterparties
- **Why:** custody, banking, payment rails, data providers and the cloud are outsourced. The sponsor remains accountable.
- **Information:** contracts (SLAs, data rights, exit terms, API rights); SOC reports; incident history; concentration.
- **Decisions:** selection and termination (H); ongoing monitoring (D on SLA telemetry, P on SOC-report analysis, H for acceptance of exceptions).
- **Evidence:** vendor register with control mappings; SLA telemetry.
- **Failure modes:** single points of failure ([industry report §2.7](../../DAF-INDUSTRY-REPORT-2026-11.md): RCF–Ren, Chariot on Column N.A., the IRS master file); data lock-in; no exit path.
- **Detection:** concentration metrics; an exit-readiness test (periodically export and restore all data into a cold standby format).

### O-12 Produce financial, operational, regulatory and tax reporting
- **Why:** law and governance require it.
- **Information:** derived entirely from the event ledger and the decision records.
- **Decisions:** report generation (D); judgments in financial statements (H); filing sign-off (H).
- **Completion:** reports regenerate from source deterministically, with lineage.
- **Failure modes:** reports assembled by hand from inconsistent extracts; mismatches between 990 Schedule D and the books.
- **Detection:** cross-report consistency tests (the Schedule D aggregates must equal the ledger aggregates).

### O-13 Deliver measurable philanthropic value
- **Why:** the reason the vehicle is tax-favored. It is distinct from processing volume.
- **Information:** donor goals (elicited, not inferred covertly); recipient information; evidence-quality grades for impact claims; grant outcomes where recipients choose to report them.
- **Decisions:** what information to present (P, with disclosed ranking criteria); recommendations to donors are informational, never sponsor-directed steering that conflicts with neutrality (H policy); dormant-capital nudges (D triggers, policy-approved).
- **Completion (measurable):** time from contribution to grant; share of accounts with activity; donor-stated goal attainment; recipient-side cost reduction; never "impact" claimed from outputs alone.
- **Failure modes:** confusing reported outputs with impact; nudging that benefits the sponsor (fee retention) rather than charity; ranking bias against small, local, faith-based recipients. Congregations take about 8.3% of top-50 DAF dollars and few have 990 data ([strategic synthesis §0 G4](../../mission-2026-11-14/strategic-synthesis.md)).
- **Detection:** fairness audits of recommendations by recipient segment; an evidence-grade label shown on every impact claim.

### O-14 Generate enough revenue to sustain operations
- **Why:** an unsustainable sponsor harms donors at exit.
- **Information:** fee revenue by source; cost to serve per outcome; partner economics.
- **Decisions:** fee schedule (H, board); pricing for institutional partners (H); cost-to-serve analytics (D).
- **Failure modes:** asset-based fees creating retention incentives counter to payout (documented incentive; the effect is unsupported, per [industry report §3](../../DAF-INDUSTRY-REPORT-2026-11.md)); price wars; dependence on a few distribution partners.
- **Detection:** unit economics per outcome (see [`../09-financial-models/`](../09-financial-models/)).

### O-15 Deliver grants to recipients usefully
- **Why:** a grant the nonprofit cannot identify, attribute or thank costs the nonprofit money. Processor complaints concentrate on payout rules and check handling ([strategic synthesis §0 G4](../../mission-2026-11-14/strategic-synthesis.md)).
- **Information:** recipient payment profile (verified bank account or rail enrollment); remittance data (grant ID, donor-shared information per the donor's choice, purpose); recipient contacts.
- **Decisions:** rail selection (D); bank verification (D using third-party account-verification evidence, H for exceptions); donor-information sharing (D from the donor's choice).
- **Completion:** settled payment with machine-readable remittance delivered.
- **Evidence:** settlement plus remittance acknowledgment.
- **Failure modes:** checks lost or uncashed; remittance out of band; grants misattributed.

### O-16 Preserve continuity and portability
- **Why:** donors die or become incapacitated; accounts go dormant; donors leave; sponsors migrate platforms or wind down.
- **Decisions:** successor activation (D on documentation, H on disputes); inactivity policy actions (D trigger, H for the charitable default distribution); outbound transfer (D for eligibility, H for the variance case).
- **Evidence:** full-fidelity export of the account's history in an open format (a design commitment: [`standards/daf-grant-record/schema-v0.1.json`](../../../standards/daf-grant-record/schema-v0.1.json) is the starting point).

### O-17 Protect information, identity and access
- **Why:** donor confidentiality (Schedule B is confidential at the IRS; anonymity choices for grants) and the assets themselves depend on it.
- **Decisions:** access grants (D from role and attributes, H for privileged access); incident declaration (H).
- **Evidence:** access logs; access reviews; key management records.

### O-18 Learn and improve without weakening safeguards
- **Why:** addendum §21.
- **Decisions:** detect improvement opportunities (P); simulate (D, digital twin); approve (H, for any change to financial controls, regulatory policy, agent permissions or material processes); verify (D).
- **Evidence:** a change ledger linking hypothesis, simulation, test, approval, deployment and verification.

## 4. Decision census

Counting the decisions enumerated above gives this split (full table in [`outcome-decisions.csv`](outcome-decisions.csv); the counts are computed by `models/` tests from that CSV):

- Most *volume* is deterministic: eligibility for listed public charities, posting, fees, acknowledgments, reconciliation matching, rebalancing within bands.
- Probabilistic analysis is concentrated in identity resolution, risk triage, document understanding, service answers and recommendation ranking. It resolves to D or H in every case where it could change money or legal state.
- Human authority is concentrated in a small set of *decision types*: policy, fiduciary investment choices, non-routine grants, sanctions true-match clearance, complex asset acceptance, write-offs, filings, governance. These are low in volume and high in consequence.

This shape, a large deterministic volume around a small accountable judgment core, is the basis of the organizational design in [`../02-business-capabilities/organization-model.md`](../02-business-capabilities/organization-model.md).
