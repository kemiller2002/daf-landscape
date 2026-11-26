# Scenario library and saturation tracking

**Data:** [scenarios.csv](scenarios.csv): 513 scenarios over four rounds. Columns: id, round, workflow, category, scenario, permitted and prohibited outcomes, governing rules, result, finding id, severity, finding description.

**Method.** All scenarios are *theoretical*: each was reasoned against written rules, not executed. Results:
- **covered-baseline**: decided by an existing baseline rule (round 1 only);
- **covered-refined**: decided by a rule from this program;
- **duplicate**: semantically the same as an earlier scenario;
- **new-finding**: the rules do not decide it, decide it wrongly, or conflict.

Round 1 was written by the program author against the baseline. Rounds 2–4 were generated in **separate model contexts** instructed to break the then-current model, then merged and deduplicated by the author. Same-model-family caveats apply ([charter §5](../00-program-charter.md#5-independence-statement)).

## 1. Rounds

| Round | Target model | Streams | Scenarios |
|---|---|---|---|
| 1 | Baseline (`docs/`, AI-native workstream) | Grant lifecycle + cross-cutting | TVS-001..102 |
| 2 | Revision 1 | Grants (TVS-201..283); cross-domain (TVS-301..381); security, partner and AI (TVS-401..488) | 252 |
| 3 | Revision 2 | Grants and rule interactions (TVS-501..556); security and cross-domain chains (TVS-601..656) | 112 |
| 4 | Revision 3 | Targeted security only: restore, external registers, third-party failure, waitable parameters, amendment interactions (TVS-701..747) | 47 |

Category coverage across rounds includes:
- normal operations, boundary, missing, invalid and conflicting data;
- concurrency, external failure, fraud and insider abuse;
- human error, policy change, market volatility, organization failure, high volume;
- disaster recovery, accessibility, partner failure;
- AI error, hallucination, model unavailability and prompt injection;
- corrupted evidence, delayed and duplicated events.

## 2. Discovery by round and stream

"New-row share" is the share of scenarios yielding a new finding. "Distinct" counts findings after deduplication, with severity taken as the maximum over the finding's scenarios.

| Round | Stream | Rows | New-row share | Distinct new | Sev 5 | Sev 4 | Sev ≤3 |
|---|---|---|---|---|---|---|---|
| 1 | Grant lifecycle + cross-cutting (vs baseline) | 102 | 52% | 45 | 8 | 18 | 19 |
| 2 | Grants | 83 | 76% | 32 | 0 | 8 | 24 |
| 2 | Cross-domain | 81 | 53% | 21 | 0 | 8 | 13 |
| 2 | Security, partner, AI | 88 | 45% | 22 | 4 | 12 | 6 |
| 3 | Grants and rule interactions | 56 | 73% | 24 | **0** | **0** | 24 |
| 3 | Security and cross-domain chains | 56 | 50% | 25 | 2 | 14 | 9 |
| 4 | Security, targeted | 47 | 70% | 29 | 1 | 12 | 16 |

## 3. Interpretation

**The new-row share is not a convergence signal here.** It stayed at 45–76% in every round, because each challenger was told to aim at the newest rules. Severity is the signal.

### 3.1 Grant and payment lifecycle: approaching saturation (severity), not saturated (count)

| Round | Severity-5 findings | Severity-4 findings |
|---|---|---|
| 1 | 8 | 18 |
| 2 | 0 | 8 |
| 3 | 0 | 0 |

Round 3's findings were mostly revision-2 rules not carried through every section. Revision 3 ([amendments A1–A23](../06-state-models/revision-3-amendments.md)) addresses them. A confirmation round after folding them into the base documents was **not run**. The saturation conditions (charter §6) are met for severity and not for count:
- critical transitions examined: yes;
- high-severity failure classes covered: yes;
- recent rounds few material findings: yes for severity ≥4;
- uncertainties recorded: yes;
- no concealed critical contradiction: the open contradictions are in the register.

### 3.2 Cross-domain (fund lifecycle, migration, custody, accounting): incomplete

These streams have one dedicated round (round 2, 21 findings) plus chains in round 3. Several workflows are still unspecified (CW-21..45). **Not saturated.** Most remaining findings are missing workflows rather than defects in existing rules.

### 3.3 Security and external dependencies: not saturated, and not converging under theoretical rounds

| Round | Severity-5 findings | Severity-4 findings |
|---|---|---|
| 2 | 4 | 12 |
| 3 | 2 | 14 |
| 4 | 1 | 12 |

In rounds 3 and 4, **each revision's new controls opened new paths**: 8 in round 3; 7 amendments with new paths in round 4. The frontier has moved *outward*:
- from platform rules (round 2);
- to restore and recovery, external registers and waitable parameters (round 3);
- to the independence and concentration of third-party evidence sources (round 4).

This pattern is a reason to stop **theoretical** expansion here (charter §6: progress now needs unavailable external evidence). What a provider can attest, what a custodian can report per movement, and what a bank portal logs are facts about real counterparties (GAP-002; TVA-005/006/024). Further rounds would mostly generate requirements whose feasibility is unknowable without them.

The round-4 findings (TVF-226..254) are **recorded but not yet converted into amendments** ([revision 3 §D](../06-state-models/revision-3-amendments.md#d-round-4-findings-open-revision-4-not-drafted)).

## 4. Saturation tracking

| Domain | Rounds | Saturation status | What would change it |
|---|---|---|---|
| Grant and payment lifecycle | 1–3 | Approaching saturation (no sev ≥4 in round 3) | A confirmation round after the rev-3 fold-in |
| Contributions | 1–3 | Partial; finality and gift-date rules depend on counsel | OD-04, TVF-115 |
| Fund lifecycle, migration, custody | 2–3 | Not saturated (missing workflows) | Specify CW-21..45 |
| Security, external registers, recovery | 2–4 | **Not saturated; not converging theoretically** | Provider, custodian and bank capability evidence, then a confirmation round on restore and registers |
| UX and status | 1–2 + review | Coherent proposal, untested with users | Usability tests |
| Economics | Review only | Blocked on measurement | GAP-001/034 shadow replay |
