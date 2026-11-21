# W6: sponsor-to-sponsor transfers and portability

**Outcome (BO-58):** a donor can move advisory privileges and the assets of a DAF to another eligible sponsor, quickly and at low cost, with the account's history intact. The sending sponsor keeps exclusive legal control until it makes the transfer grant.

**Why it matters (evidence):**
- None of 12 sponsors reviewed publishes an outbound transfer policy. Transfers take 10 business days to 4 weeks and are liquidated to cash (EV-121).
- AEF's migration kept only two years of history (EV-037).
- DAF-to-DAF flows netted out of FY2024 grants total $8.03bn (industry report §4).
- Incumbents earn asset-based fees, so their incentive points against easy exit (industry report §3, an incentive classified as structural).

## 1. First-principles decomposition

| Necessary element | Why | Not necessary (inherited) |
|---|---|---|
| A **grant decision** by the sending sponsor to an eligible receiving sponsor (§4966: a grant to a §170(b)(1)(A) public charity is not a taxable distribution; REG-001) | Legal control and charitable purpose | Paper request forms, wet signatures, phone confirmation |
| **Identity** of the donor requesting, and of the receiving sponsor and its account | Fraud control: transfer-out is a high-value takeover target | Re-verifying the donor from scratch at the receiving sponsor (an upstream attestation can be relied on; INN-24) |
| **Asset movement:** cash, or in-kind securities where both sponsors' custody allows | Value transfer | Mandatory liquidation. It is a convention plus operational simplicity, not law |
| **Account history** that the donor and receiving sponsor can use: grants, contributions, acknowledgments | Donor records, tax substantiation, advisor continuity | One-off spreadsheets |
| **Sending-sponsor closure:** final statement, fee proration, ledger closure | Accounting integrity | Manual reconciliation |

## 2. Inversion findings

| Prompt | Finding |
|---|---|
| Eliminate the process? | Not the *grant*: legal control requires a sponsor decision. Everything else can be standardized away |
| Make it unnecessary? | If accounts were portable records hosted on a neutral rail, the "transfer" would be a change of the sponsor-of-record pointer plus a grant. This is radical design D-W6-4 |
| No employee touch? | Feasible for clean cases: an eligible receiving sponsor on the IRS list, verified donor, no open flags, cash or standard pools |
| No form? | Yes. The receiving sponsor initiates through a protocol message carrying the donor's signed consent token (INN-16) |
| Begin before the request? | Pre-verify the eligibility of all known DAF sponsors (the ~1,512 FY2024 sponsor universe, EV-004) so the receiving-sponsor check is a lookup |
| External partner does it? | A neutral transfer utility, as in ACATS for brokerage (D-W6-5) |

## 3. Competing designs

| ID | Type | Mechanism | Who decides / when | Authoritative data | Human roles | Controls | Cost drivers | Experience (donor / advisor / nonprofit) | INN | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| D-W6-1 | Conventional baseline | Donor submits a form to the receiving sponsor, which sends a letter of request. The sending sponsor reviews manually, liquidates, wires cash, and mails a closing statement | Sending-sponsor staff, after the form arrives | Each sponsor's own system; history is not transferred | Ops staff at both sponsors | Callbacks; manual eligibility check | Staff time at two organizations; out-of-market time during liquidation | Weeks; out of market; history lost / advisor re-keys / none | — | Observed (EV-121) |
| D-W6-2 | Automation-first | Same sequence. E-signature, automated eligibility lookup and an automated wire; history exported as PDF | Sending-sponsor rules plus staff approval | Same | Approver | E-sign audit; IRS lookup | Lower staff time | Days to weeks; PDF history | INN-16 (partial) | L1 |
| D-W6-3 | AI-native | Receiving sponsor sends a structured transfer intent through the API. Sending-sponsor policy engine: donor consent token valid; receiving sponsor eligible (pre-verified sponsor list); no open flags. Deterministic approval → payment gate. History is exported as an **open grant record** bundle, and the agent drafts the closing statement | Sending sponsor's policy (D); human only on flags | Event ledger; open grant record | Specialist on flags only | Step-up auth; cooling-off on a new destination; amount caps; fraud screen | Near zero per clean case | 1–3 business days (cash rails); full history / advisor continuity / — | INN-16, INN-18 | L2 (PoC payment gate and open record schema exist) |
| D-W6-4 | **Radical: portable account, sponsor-of-record switch** | The account's ledger and history live on a neutral, shared record substrate. Pool units are held in a common qualified-custody omnibus structure with sub-accounting per sponsor. A transfer is (a) the sending sponsor's grant decision and (b) an atomic re-titling of units from the sending sponsor's sub-account to the receiving sponsor's. Nothing is liquidated and no history moves, because history never lived in one sponsor's system | Sending sponsor still decides the grant (the legal core). *Timing* changes from liquidate-then-move to atomic re-title. *Authoritative data* moves from each sponsor to a shared record | Shared ledger operator plus custodian | None in clean cases | Two-sponsor atomic commit; custody segregation per sponsor; independent reconciliation | Shared-substrate operating cost; very low per transfer | Minutes to a day; never out of market | INN-17, INN-18 | L0 |
| D-W6-5 | Externalized / ecosystem: transfer protocol utility (ACATS-like) | A neutral utility defines standard transfer messages (intent, consent, eligibility attestations, in-kind asset list, history bundle, SLA timers) that sponsors and their vendors implement. The utility matches messages and tracks SLAs; it holds no funds | Each sponsor decides; the utility enforces timelines and data completeness | Each sponsor's system plus standard messages | Exceptions at either side | Message signatures; SLA breach reporting; no fund holding (REG-043 avoided) | Utility membership fee; integration once per vendor | Days; history preserved; public SLA statistics | INN-17 | L1 |
| D-W6-6 | Contrarian: transfer-in as acquisition channel | The receiving AI-native sponsor bears all friction: it drafts the request, pre-fills consent, tracks the sending sponsor and reports delays to the donor and advisor | Receiving sponsor orchestrates; sending sponsor still decides | Receiving sponsor's case record | Receiving-side concierge for stuck cases | Donor consent only | Paid by the receiving sponsor as CAC | Donor does little; still slow at incumbent senders | INN-14 | L1 (commercially plausible; does not fix sender friction) |

**Meaningful-difference check:**
- D-W6-3 vs D-W6-4 differ in the *authoritative data location* and the *timing of asset movement*.
- D-W6-5 differs in the *performing organization*: a utility rather than either sponsor.
- D-W6-6 differs in *who orchestrates*.

## 4. Constraint removal and reintroduction ledger

Constraints removed for ideation: incumbent incentives, custodian silos, record-format diversity, liquidation convention.

| Constraint reintroduced | D-W6-3 | D-W6-4 (radical) | D-W6-5 | Modification that revives |
|---|---|---|---|---|
| Legal: sending sponsor must make a grant to an eligible sponsor (REG-001); exclusive control until then | Survives | Survives *only if* re-titling occurs after the sending sponsor's decision and the units are clearly the sending sponsor's property until then | Survives | D-W6-4: units sit in sponsor-segregated sub-accounts at the custodian, never pooled across sponsors |
| Fiduciary: prudent handling; no forced sale at bad prices | Survives (cash) | Strengthened (in-kind) | Survives | — |
| Accounting: each sponsor's books close and open correctly; Schedule D counts | Survives | Requires both sponsors to accept the shared ledger's sub-ledger as authoritative | Survives | D-W6-4: shared ledger with each sponsor holding an independently verifiable copy (hash-chained) |
| Privacy / security: donor data minimization; takeover risk | Survives with step-up and cooling-off | Concentration risk: one substrate holds many sponsors' records | Survives | D-W6-4: strict tenant isolation; independent audit of the operator |
| Economic: who pays? | Sending sponsor bears cost and loses AUM, so it has little incentive | Operator fee; incumbents lose lock-in, so they will not join | Utility fee; incumbents will not join voluntarily | Regulation or market pressure would be needed. The receiving sponsor pays (D-W6-6) |
| Operational: different pool menus at the two sponsors | Cash default | In-kind only where the receiving sponsor offers the same pool or accepts the securities | Same | Fallback to cash |
| Human acceptance: donors, advisors, incumbents | Donors and advisors favor it | Sponsors fear disintermediation | Sponsors resist; vendors may like it | Start with sponsors that *gain* inbound flow (challengers, community foundations) |

**Survivors:** D-W6-3 inside the enterprise; D-W6-5 as an ecosystem proposal. D-W6-4 survives legally only with heavy modification, and dies on economics (incumbent participation). It is held as a long-term option that only becomes relevant if the platform hosts several sponsors itself (Model C/D). Within one multi-tenant platform, D-W6-4 is almost free.

## 5. Cross-industry analogies

| Source | Transfer | Why it might work | Where it breaks |
|---|---|---|---|
| Brokerage ACATS (NSCC) | Standard transfer messages, timelines and in-kind moves | Turned brokerage transfers from weeks into a routine | It is FINRA-mandated. Nothing compels DAF sponsors, and the receiving firm initiates in a regulated context |
| Telecom number portability | Identifier persists across providers | Removes switching cost and changes competition | Needs regulatory mandate; no regulator here (EV-093: no state DAF mandates) |
| Health records (FHIR export) | Standard patient record export | Open schema enables movement | Adoption required regulation (21st Century Cures Act) |
| Payment netting | Atomic delivery-versus-payment | D-W6-4 atomic re-title | Two independent legal owners must both sign |

## 6. Seven-perspective competition

| Perspective | Position |
|---|---|
| Inventor | D-W6-4 is the real reinvention: stop moving accounts and move the sponsor-of-record pointer |
| Enterprise architect | D-W6-3 is buildable now on the event ledger and open grant record. D-W6-4 is natural *inside* a multi-sponsor platform (DD-016), so build tenancy so it is possible later |
| Economist | Portability transfers surplus from incumbents to donors. Nobody voluntarily funds D-W6-5. The receiving side's willingness to pay (D-W6-6) is the realistic funding |
| Regulatory specialist | The transfer is a grant. The sending sponsor must decide, after checking that the receiving sponsor is eligible. In-kind is lawful but needs custody coordination. Watch the pending §4966/6033 guidance on "certain DAF arrangements" (REG-022) |
| Adversarial reviewer | Transfer-out is a prime account-takeover and authorized-push-fraud path: drain to a fraudster-controlled "sponsor" account. Requires a sponsor allow-list, step-up auth, a cooling-off period and notification to the prior contact channel |
| Customer advocate | The donor pain is time out of market and lost history. D-W6-3 fixes history; only in-kind fixes market exposure |
| Commercial strategist | Portability is a wedge: a challenger that *offers* it attracts inbound transfers, and incumbents cannot copy it without weakening retention |

**Disagreements:**
- The economist vs the inventor on whether D-W6-4 is worth designing for at all.
- The regulatory specialist flags that the IRS 2026–27 guidance may touch DAF-to-DAF arrangements. That is unresolved.

**Unresolved questions:**
- Do custodians support sponsor-to-sponsor in-kind moves of pool shares, or only underlying securities?
- Would a utility attract any incumbent?

## 7. Forwarded to experiments
- **E8 (transfer/migration replay):** an open-grant-record bundle round-trips an account's full history with zero loss. Test that replay into a fresh ledger reproduces balances and grant history.
- **E9 (crash recovery):** a transfer interrupted between grant approval and payment does not double-pay and resumes.
- **E2:** transfer-out fraud cases in the adversarial set (destination not on the allow-list; new destination inside cooling-off).

**Recommendation:**
- **Adopt D-W6-3** in the enterprise (L2 → L3 after E8 and E9).
- **Propose D-W6-5** as an industry proposal using the open grant record.
- **Hold D-W6-4.** Its natural home is intra-platform tenant transfer once Model C/D hosts several sponsors.
