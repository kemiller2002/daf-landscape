# Enterprise ontology

**Status:** conceptual [T]. This merges the administration object list (ADM-01..30, PARTY, AUTH) with the 35-entity [canonical data model](../ai-native-daf-enterprise/06-data-and-knowledge/canonical-data-model.md). It is not a schema. Retention periods are **not** stated: the legal basis is unverified (REG-026 is [K]; TVC-016). Each entity gets a retention *class*, to be filled by counsel (OD-12).

Retention classes:
- **R-TAX**: tax substantiation and returns.
- **R-OFAC**: sanctions records.
- **R-CORP**: corporate and governance records.
- **R-AGR**: governing agreements, for the life of the fund plus a tail.
- **R-FIN**: books and records.
- **R-PII**: personal data, subject to deletion rights unless a legal hold or other retention applies.
- **R-OPS**: operational.
- **R-EVD**: control evidence for the audit period.

## 1. Entity catalog

Column "Authority conflict" names other systems or parties that could claim to be authoritative for the same fact. Each needs a field-level source-of-truth rule (DATA-07).

| Entity | Identity | Owner (intended sole writer; see note) | Lifecycle | Key relationships | Authority boundary | Retention | Authority conflict / known risk |
|---|---|---|---|---|---|---|---|
| Sponsoring organization | EIN; legal entity ID | Sponsor governance (C5.4) | Formed → registered (states) → operating → dissolved/merged | Has legal entities, programs, policies, board | Holds exclusive legal control of fund assets (§170(f)(18) acknowledgment language, REG-008 [F]; §4966(d)(2) definition [unverified]) | R-CORP | **Model C/D infrastructure operator** may appear to control policy and payments; legal control must remain with the sponsor (DD-016; adversarial objection 5) |
| Legal entity | Internal ID + EIN/jurisdiction | Sponsor governance | Effective-dated | Owns custodial accounts; issues acknowledgments | Tenant ≠ legal entity (core invariant 2) | R-CORP | Program branding can hide which entity is the sponsor (ADM distinction 10; admin scenario 22) |
| Program / brand | Program ID | Sponsor | Versioned | Distribution partner, fee schedule, investment menu | No legal authority of its own | R-CORP | Partner may present program as its own product |
| Donor | PartyId (person or org) | Party service (C1.1) | Registered → verified → active → deceased/dissolved | Contributes to funds; may hold advisory privileges | Contributor role confers **no** control over assets after the gift | R-PII + R-TAX | "Fund owner" label (admin scenario 1); CRM at a wealth firm holds a competing client record |
| Fund (DAF account) | AccountId (immutable across rename) | Account service + ledger (C1.1/C4.1) | [State models §6](../06-state-models/state-models.md#6-fund-account) | Sponsor, program, agreements, parties via relationships, positions, grants | Sponsor-administered arrangement; not donor-owned | R-AGR + R-FIN | **Custodian sub-account** and **wealth-firm "account"** may each be seen as the fund. A fund may map to several custody accounts and pools (ADM distinction 2). |
| Advisor (donor-advisor) | PartyId + relationship edge | Authorization service (C1.2) | Authority grant machine | Advisory privileges on a fund | Recommends only | R-PII | Advisor's own firm SSO claims roles that the sponsor has not granted (DD-021 orders relationship check before assurance) |
| Investment advisor (professional) | PartyId + firm ID | C1.2 + C2.4 | Engaged → active → terminated | Manages a pool or fund mandate; may be a disqualified person (REG-005) | Within mandate only (DD-007); never grant authority by virtue of the role | R-CORP | **Wealth firm** is also a distribution partner and fee recipient; conflicts (FEE-12) |
| Authorized representative (POA, trustee, executor, guardian) | PartyId + capacity + instrument | C1.2 | Evidence → verified → active → expired | Acts for a donor or advisor | Bounded by instrument; not the same as successor | R-PII + R-AGR | Missing from UI personas (TVF-050); instrument validity is a legal question [C] |
| Successor / beneficiary | PartyId + successor plan | C1.2 | [Succession machine](../06-state-models/state-models.md#7-authority-grant-and-succession) | Nominated on a fund; beneficiary *organizations* receive grants | Nomination ≠ activation (AUTH-07) | R-AGR | Family claims vs agreement terms; estate executor vs successor advisor |
| Charitable organization (recipient) | EIN or foreign ID + internal RecipientId | Registry (C3.1) | Versioned; eligibility facts bitemporal | Eligibility facts, payment profiles, fiscal-sponsor links | Receives grants; no authority over the fund | R-TAX (via grant) | **IRS BMF / Pub 78**, **Candid**, **charity rail directory**, and the charity itself all assert identity and status. Rev. Proc. 2018-32 reliance attaches to IRS sources (REG-019). Name collisions (B5, E1 open cases). |
| Eligibility fact | Source + version + recipient | Registry | Immutable per source version | Recipient | Input to decisions | R-TAX + R-EVD | IRS publication timing vs effective date of revocation (bitemporal) |
| Payment profile | Profile ID; tokenized account | Payment gate (C3.4) | [WF-10 machine](../ai-native-daf-enterprise/03-workflow-redesign/wf-grants.md) | Recipient | Endpoint only | R-FIN + R-PII | **Rail directory** (e.g. a charity-payment network) vs recipient-entered details vs bank verification service. Shared payee registries (INN-07) move this outside the sponsor (conflicts with CTL-004/006). |
| Investment account (custodial) | Custodian account number (tokenized) + internal ID | Custodian (external) mirrored by C2.3 | Opened → active → closed | Legal entity; holds positions | Custodian is authoritative for holdings, **not** for fund allocation | R-FIN | Custodian vs internal position mirror vs ledger (core invariant 1; FI-29) |
| Holding / position | Account + instrument + date | Custodian (external); mirror C2.3 | Bitemporal | Pools; unitized funds | Observation until reconciled | R-FIN | Custodian corrections (FI-28) |
| Pool / portfolio | Pool ID | Investment governance (C2.4) | Versioned (IPS) | Units held by funds | Committee-approved parameters only | R-FIN | Outsourced CIO vs Investment Committee |
| Unit / NAV | Pool + strike date | Valuation (C4.1) | Immutable per strike; restatable by NAV-error process | Funds' unit balances | Derived | R-FIN | Pricing vendor vs custodian price |
| Contribution | Contribution ID + intent reference | Intake (C2.1) | [State models §5](../06-state-models/state-models.md#5-contribution) | Donor, fund, asset, acknowledgment | Completed gift date is a legal fact [C] | R-TAX | **Bank/custodian** reports receipt; **donor** claims gift date; **appraiser** values non-cash gifts |
| Gift acceptance decision | Decision ID | Sponsor (C2.2 + H) | Immutable | Contribution, asset diligence | Sponsor discretion | R-TAX | — |
| Acknowledgment | Document ID | Intake (C2.1) | Draft → issued → corrected | Contribution | Must contain §170(f)(18) statement (REG-008) | R-TAX | Partner-branded acknowledgment may omit mandatory text (admin scenario 22) |
| Recommendation | Recommendation ID | Intake (C3.2) | [State models §1](../06-state-models/state-models.md#1-grant-recommendation-donoradvisor-side) | Fund, requester, recipient candidate | Request, not instruction (DD-003) | R-TAX (Schedule D support) [C] | Partner widget, donor agent and portal are all channels; **channel** must never be the record of intent |
| Grant | Grant ID | Decisioning (C3.3) | [State models §2](../06-state-models/state-models.md#2-grant-sponsor-side) | Recommendation, decision, reservation, payment attempts | Sponsor's legal act | R-TAX + R-FIN | **Open grant record** projection is lossy by design; partners must not treat it as authoritative |
| Restriction / donor intent | Restriction ID + source class | Policy (C5.1) | Proposed → accepted → effective → amended/expired | Fund, grant, agreement | Hierarchy: law > governing agreement > accepted donor intent > sponsor policy > preference [P][C] (ADM distinction 8) | R-AGR | Letter of wishes (AG-07) is non-binding; UI must not render it as a restriction |
| Agreement / governing document | Template version + execution ID + hash | Legal (C5.1) | [AG-01..08] | Fund, parties, restrictions | Legal text authoritative; structured terms need approval (AG-03) | R-AGR | E-signature provider evidence vs legal sufficiency (AG-02; ESIGN consent open, REG-064) |
| Fee schedule / fee assessment / fee posting | Schedule version; assessment ID | Fee engine (C4.3) | Accrual → assessment → posting → collection → refund (FEE-04) | Fund, partner share | Deterministic, reproducible (DEC-ADM-05) | R-FIN | **Partner** may calculate its own share; disagreement needs a single source (FEE-07) |
| Reservation | Reservation ID | Ledger/treasury | [State models §4](../06-state-models/state-models.md#4-reservation-encumbrance) | Grant, fund, ancestors | Internal only | R-FIN | UI "available" projection may disagree (FI-06) |
| Payment instruction / attempt | Attempt ID + provider idempotency key | Payment gate (C3.4) | [State models §3](../06-state-models/state-models.md#3-payment-attempt) | Grant, profile, provider | Sponsor order; provider's obligation once accepted | R-FIN + R-OFAC | **Provider** is authoritative for receipt and settlement, not for whether the sponsor authorized it |
| Journal entry / reconciliation record | Entry ID; break ID | Ledger (C4.1/C4.2) | Immutable; break lifecycle | Source events | Corrections only by new entries | R-FIN | Three-way: ledger, custodian, bank (FI-29) |
| Compliance determination (ED, ER, eligibility, sanctions clearance) | Determination ID | Grants compliance / sanctions officer (H) or rule | Valid-from/valid-to | Recipient, grant(s) | Human or rule; never a model (DD-005) | R-TAX / R-OFAC | **Shared determinations** across sponsors (INN-02, network) raise reliance questions [C] (GAP-012) |
| Case / investigation / exception | Case ID | Exception queue (C5.3) | Opened → assigned → decided → closed/reopened | Subject objects, flags | Delegated authority required per case type | R-OPS + R-EVD | Departmental inboxes (rejected, DD-013) |
| Employee / agent (human staff) | Workforce identity | HR + IAM | Hired → roles → terminated | Roles, approvals | Delegation-of-authority table | R-CORP + R-PII | — |
| AI agent (software) | Agent ID + version | Agent owner (CTO line) | Designed → evaluated → active → retired | Tool scopes; AgentRun records | Read/propose/flag/draft only (INV-A5) | R-EVD | **External donor agent** is a delegated *principal*, not one of these (DD-017) |
| Service provider / vendor | Vendor ID | Vendor risk (C5.5) | Onboarded → active → exit | Capabilities, contracts | Contract-defined | R-CORP | Capability claimed vs verified per contract (INT-02) |
| Partner organization (distribution) | PartnerId | Partner management (ADM-23) | [Partner lifecycle](../../docs/ui/widgets/04-partner-developer-operations-and-economics-v0.2.md) | Users, origins, widgets, program | Distribution and identity federation only | R-CORP | Partner's identity provider asserts user roles; sponsor must still grant fund privileges (DD-021) |
| Embedded application / widget instance | WidgetId + InstanceId | Widget platform | [Session machine](../06-state-models/state-models.md#9-widget-session-embedded) | Partner, principal, fund scope | Presentation + command submission; never authority | R-OPS + R-EVD | **Host application** is a separate trust boundary that may display stale or false data around the widget |
| Policy | Policy ID + version | Policy registry (C5.1) | Draft → back-tested → approved → published → superseded | Rules, decisions | Author ≠ publisher (DD-011) | R-CORP + R-EVD | Shared policy packs across sponsors (INN-36) create correlated error |
| Decision / approval / flag | Decision ID | Issuing capability | Immutable | Subject, policy version, evidence | Actor kind ∈ {Rule, Person} for state-changing decisions (INV-A1) | R-EVD | — |
| Audit event / control evidence | Event ID + hash | Evidence ledger (C4.5) | Immutable; retention-bound | Control, subject | Evidence of execution, not of policy existence | R-EVD | Evidence ledger owned by the same function it assures (CRCO; TVF-041) |

**Review note (architecture A3/A4).** Donor, advisor, successor and authorized representative are listed as rows for readability. Under ONT-1 they are **capacities of a Party** (relationship edges), not separate entities. Where the owner column names a human, an external party or two writers, the ownership is split: the external party is authoritative for the observation, and the named capability is the sole *internal* writer.

## 2. Relationship rules

| ID | Rule |
|---|---|
| ONT-1 | Party ≠ relationship ≠ authority. A person may be donor, advisor, successor and employee at once. Each capacity is a separate edge with its own evidence (PARTY-04). |
| ONT-2 | A household or family group is presentation only. It confers no access (PARTY-05, SVC-06). |
| ONT-3 | A fund relates to ≥1 legal entity, ≥0 custody accounts, ≥0 pools. Many-to-many with pools is normal (unitized pooled investing). |
| ONT-4 | Every grant references exactly one fund. A grant from several funds is several grants (avoids ambiguous restriction and reservation semantics). Proposed [P]. |
| ONT-5 | A recipient may be several legal identities over time (merger, EIN change). Identity changes create a new identity edge. They never rewrite past grants (admin scenario 12). |
| ONT-6 | Channel (portal, widget, API, agent, staff entry) is an attribute of a request. It is never an entity with authority. |

## 3. Where multiple systems claim the same information

| Fact | Claimants | Proposed authoritative source | Rule when they disagree |
|---|---|---|---|
| Who may recommend on fund F | Sponsor authorization service; partner IdP roles; wealth-firm CRM | Sponsor authorization service | Partner claims are inputs to authentication only |
| Fund holdings | Custodian; internal mirror; ledger | Custodian for quantities; ledger for fund allocation | Break (FI-29) |
| Recipient status | IRS sources; data vendors; recipient | IRS sources for reliance (REG-019) | Vendor data may add flags, not clear them |
| Payee bank details | Recipient session; rail directory; verification service | Verified profile after cooling-off (WF-10) | Any mismatch → hold |
| Payment outcome | Provider; bank statement; recipient | Provider + bank statement (two-source) | Unknown until both agree or a human decides |
| Gift date and value | Bank/custodian; donor; appraiser | Custodian/bank for receipt; appraiser for non-cash value | Acknowledgment states what the sponsor knows [C] |
| Fee amount | Fee engine; partner billing | Fee engine | Partner disputes become a case |
| Donor identity attributes | Party vault; partner; KYC vendor | Party vault with provenance | Corrections are events (PARTY-07) |
