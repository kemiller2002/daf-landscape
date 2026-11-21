# B. Donor onboarding

**Capabilities:** C1.1 (party and identity), C1.2 (delegated authority), C2.1 (contribution intake, first gift), C2.4 (initial investment selection). **Outcomes:** O-01, O-02, O-08, O-17. **Accountable:** Head of Client and Partner Operations.

## 1 Existing industry operating model

- **The account-opening feature set is table stakes across sponsors.** The donor feature census lists stock, complex-asset and crypto acceptance, recurring grants, search and vetting, family roles and adviser access ([industry report §11.25 quote at line 845](../../../DAF-INDUSTRY-REPORT-2026-11.md)).
- **Onboarding is generally application-based, and data is re-entered across systems.** No sponsor publishes onboarding latency or abandonment. The repository's experience diagnostic is the best qualitative source ([`daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md`](../../../daf-end-to-end-experience-comparative-diagnostic-2026-11-11.md)) [I].
- **Advisor access is often established by letter of authorization or a program-specific adviser form.** Six of the top 20 sponsors (about $84bn) contractually limit automated or third-party access, and several bar credential sharing ([strategic synthesis §0 D](../../../mission-2026-11-14/strategic-synthesis.md)).
- **Security disclosure is thin.** MFA is published at only some sponsors ([`b49-04-fraud-diversion-controls.md`](../../../mission-2026-11-14/b49-04-fraud-diversion-controls.md); industry report §11.74).
- **History portability is poor.** AEF's migration kept two years of directly accessible history ([industry report §4](../../../DAF-INDUSTRY-REPORT-2026-11.md)). That matters for donors transferring in.

## 2 Actual required business outcomes

1. A verified party, or parties, with a legally valid acceptance of the current program agreement (O-02).
2. A correct privilege map: donor, joint donors, successors, advisor, family members, agent principals (O-02, O-17).
3. Relationship facts sufficient for disqualified-person and prohibited-benefit tests (O-08).
4. An initial investment selection valid against the program menu (O-04).
5. The first contribution intent, with a unique reference so the gift can be matched on arrival (O-01).

## 3 Legal and risk constraints

- **The program agreement is a contract.** E-SIGN and UETA permit electronic formation with consumer consent; see the [regulatory map](../../08-governance-and-compliance/regulatory-applicability-map.md).
- **Sanctions screening applies to all U.S. persons.** OFAC does not prescribe a KYC method.
- **Whether a bank-style Customer Identification Program applies to a charity is a counsel question, not an assumption.** The repository's working position is that a charity is not a BSA "financial institution" (ACT-048), but this must be confirmed in the regulatory map. The sponsor still needs identity assurance proportional to fraud and sanctions risk (internal risk control, not law).
- **Privacy.** Data minimization; state privacy laws that reach nonprofits.
- **DAF definition (§4966(d)(2)).** Advisory privileges must be ones the sponsor grants. Privilege structure is therefore a sponsor policy decision (D).

## 4 Proposed AI-native operating model

**There is no "application form."** Onboarding is a **progressive, structured exchange**, finished when the policy's required facts are present and verified. Three channels feed the same intake API:

| Channel | How facts arrive | What the donor does |
|---|---|---|
| **Advisor or institution API** | The partner pushes facts it has *already verified* (name, DOB, address, tax ID token, KYC reference) with a donor consent token. The enterprise records the partner's assurance level and evidence reference | Confirms and accepts the agreement |
| **Conversational** | The service agent asks only for missing required facts, in plain language. Each answer is converted to a structured field and shown back for confirmation | Answers, confirms, e-signs |
| **Self-service screen** | A short dynamic screen that shows only fields the policy still needs | Fills, confirms, e-signs |

**Rules of the model:**
- **Verified data reuse.** A fact verified once is not re-collected. It gets a provenance (source, assurance level, date) and is re-verified only on a risk trigger.
- **Progressive.** A donor may open an account with minimum facts and add successors or family later. Privileges that need more facts stay unavailable until those facts exist (D).
- **Identity assurance is risk-tiered.**
  - The identity provider result plus rules decide (D).
  - Document-forgery or synthetic-identity scoring is P and feeds a D threshold.
  - Ambiguous results go to a case (H).
- **The agreement is versioned and hashed.** Acceptance is an event (`AgreementAccepted`) carrying the E-SIGN consent.
- **Investment selection** is validated against the menu (D). For advisor-managed programs, the advisor's mandate is attached (see area E).
- **The first contribution intent** is created in the same session, with a unique reference (feeds area C).

## 5 Eliminated activities

- ACT-005: paper or PDF application forms.
- ACT-006: re-keying application data.
- ACT-009: welcome kit mailing.
- ACT-056: advisor access by paper letter of authorization (now delegated grants via API with donor consent).
- ACT-007: manual identity review for every applicant (now **automated deterministic**, with humans for exceptions).

## 6 New workflows

**WF-B1 Progressive opening.**
1. `PartyRegistered`.
2. Facts collected through any channel.
3. `IdentityVerified` (IdP reference plus rule version).
4. Screening (`ScreeningCompleted` on the party).
5. `AgreementAccepted`.
6. `AccountOpened`.
7. `PrivilegeGranted` (donor, advisor).
8. `ContributionIntentDeclared`.

**WF-B2 Partner-verified opening.** As WF-B1, with steps 2–3 replaced by a partner assertion. The partner's assurance level must meet the policy minimum, or a step-up is triggered.

**WF-B3 Add family or successor.**
1. The donor proposes.
2. The invitee verifies themselves.
3. `RelationshipDeclared`.
4. `PrivilegeGranted` with scope limits.

**WF-B4 Donor agent enrolment (DD-017).**
1. The donor authorizes an AI agent as a delegated principal.
2. The scope is set (for example: recommend grants up to $X a month to listed public charities, with donor confirmation above $Y).
3. `PrivilegeGranted` (agent kind).
4. Tokens are bound to that scope.

**WF-B5 Transfer-in onboarding.** A donor moves from another sponsor:
1. The receiving account is opened.
2. The transfer intent is recorded.
3. Prior grant history is imported in the open grant-record format where available (`standards/daf-grant-record`), so history is not lost.

## 7 Required data

- Party core: legal name, DOB, residential address, tax ID (tokenized), contact channels.
- Assurance level and evidence references.
- Relationships (declared).
- Agreement version and hash.
- Privilege grants.
- Investment selection.
- Communication and anonymity defaults.
- Partner assertion records.
- Consent records.

## 8 Required APIs

- `/v1/parties`: create, update, assert-verification.
- `/v1/accounts`: open.
- `/v1/privileges`: grant, revoke, list.
- `/v1/documents`: agreement retrieval and acceptance.
- `/v1/contribution-intents`.
- `/v1/positions` and `/v1/investment-requests`: initial allocation.
- `/v1/policies/{onboarding}/evaluate`: which facts are still required.

## 9 Event triggers

- Produced: `PartyRegistered`, `IdentityVerified`, `RelationshipDeclared`, `AgreementAccepted`, `AccountOpened`, `PrivilegeGranted`, `ContributionIntentDeclared`.
- Consumed: `SanctionsListUpdated`, which re-screens existing parties; `PolicyPublished`, which re-evaluates required facts. New required facts become tasks for existing donors; they do not freeze accounts unless the policy says so.

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Service answer agent (onboarding mode) | 3 (supervised execution: it can write *draft* party facts that the donor confirms) | Ask for missing facts; explain the agreement in plain language with clause citations | Accepting the agreement on the donor's behalf; setting privileges; any verification decision |
| Document extraction agent | 2 | Extract fields from uploaded trust documents, entity documents and death certificates into a schema, with confidence | Writing to the Party record without a confirmation step |
| Identity-risk model | 2 | Score document forgery and synthetic-identity risk | Clearing a failed verification |
| Related-party detector | 2 | Propose undeclared relationships (shared addresses, entity officers) as flags | Writing `Relationship`; it emits `RelationshipInferred` proposals only |

## 11 Deterministic automation responsibilities

- Required-facts evaluation per policy version.
- The verification decision from IdP results.
- Sanctions screening.
- Privilege-scope validation.
- Agreement version binding.
- Investment menu validation.
- Creation of a unique contribution reference.

## 12 Human oversight requirements

- Identity exceptions (ambiguous or failed verification with a plausible explanation): client operations specialist (H).
- Entity or trust donors with complex control structures: client operations plus compliance (H).
- Sanctions potential true match: sanctions officer only (H).
- Policy for required facts and assurance levels: approved by CRCO and GC (H).

## 13 Exception management

All exceptions open a single `ExceptionCase` (C5.3) with an SLA. The case carries the dossier: IdP response, extracted documents, flags.

| Exception | Default handling |
|---|---|
| Verification fail | Offer an alternate method; then a human |
| Partner assertion below the assurance minimum | Step-up via the IdP |
| Undeclared relationship flag | Ask the donor to confirm; compliance decides on dispute |

## 14 Security and compliance controls

- Phishing-resistant MFA (passkeys) by default [A design choice].
- Step-up authentication for privilege changes.
- Consent tokens for partner prefill.
- Tax IDs tokenized in the party vault.
- Agreement hashes in the evidence ledger.
- Staff cannot view a full tax ID without a just-in-time grant.
- Agent principals receive scoped tokens; credential sharing is not supported (DD-017).

## 15 Estimated staffing implications

**Drivers:**
- the identity-exception rate (share of openings needing a human; a design target of ≤3% [A]);
- the volume of entity and trust openings;
- successor and family-change volume.

**Direction:** conventional onboarding staff who key and review applications are mostly removed. A small client-operations exception team remains, shared with servicing (area H). Numeric FTE is in [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:** IdP fees per verification [A; vendor pricing not in repo], exception handling minutes, and e-sign costs.

**Design targets [A]:**

| Path | Target |
|---|---|
| Partner-verified path | Median time to an opened account under 5 minutes |
| Self-service path | Under 15 minutes |
| Partner-verified path | Zero re-keyed fields |
| All paths | 100% of accounts bound to a hashed agreement version |

## 17 Implementation dependencies

- IdP selection.
- E-sign implementation.
- Partner consent and assertion standard (area I).
- Program agreement drafted by GC.
- Onboarding policy (`onboarding@v1`).
- Sanctions screening service (area G).

## 18 Measurable success criteria

1. Median and P90 time to an opened account, by channel.
2. Fields requested per opening, compared with the policy minimum.
3. Identity exception rate and exception SLA attainment.
4. Fraudulent openings detected after opening. Target: trending down; measured from fraud-case outcomes.
5. Share of advisor grants created by delegated API grant rather than paper.
6. Donor-reported effort score at opening.
