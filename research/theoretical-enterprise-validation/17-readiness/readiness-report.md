# Theoretical readiness report

**These classifications are not production readiness.** They describe the state of the *specification* after this program. Classifications:

| Code | Meaning |
|---|---|
| **C** | Theoretically coherent |
| **U** | Coherent with unresolved assumptions |
| **I** | Incomplete |
| **X** | Contradictory (an open contradiction remains) |
| **B** | Blocked by external evidence |
| **N** | Not yet evaluated |

No domain is classified **C** overall. Several *criteria* within domains are.

## 1. Matrix (18 criteria × 17 domains)

Criteria:
1. entities
2. lifecycle
3. workflows
4. financial invariants
5. authorization
6. exceptions
7. cross-domain consistency
8. UI behaviour
9. accessibility
10. integration boundaries
11. security threats
12. compliance evidence
13. operational resilience
14. economic sensitivity
15. traceability
16. contradiction resolution
17. scenario coverage
18. independent critique

For criterion 18, "U" means role-separated self-critique only; no independent human review has taken place anywhere.

| Domain | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | **Overall** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Grant decisioning | C | U | U | U | X | U | U | U | I | U | U | X | I | B | U | X | C | U | **Contradictory** (TVC-003, 025, 026, 044) |
| Payments / disbursement | C | U | U | U | C | U | U | U | I | B | U | I | I | B | U | U | C | U | **Blocked by external evidence** (provider idempotency, proof of non-receipt: TVA-005, GAP-002) |
| Reservation / funding / treasury | C | U | I | U | C | U | X | I | N | B | U | I | I | U | U | X | U | U | **Contradictory** (TVC-022, 043; OD-13 open) |
| Contributions | U | U | I | U | U | I | U | I | N | U | U | X | I | B | U | X | U | U | **Contradictory** (TVC-023 acknowledgment timing [C]) |
| Charity registry / eligibility | C | U | U | U | C | U | U | I | N | U | U | U | U | U | U | U | U | U | **Coherent with unresolved assumptions** (TVA-009, 028) |
| Fund establishment and lifecycle | U | U | I | U | U | I | U | I | N | U | U | I | I | N | U | U | U | U | **Incomplete** (merge/split, freeze, closure, migrated state, sponsor succession) |
| Parties, authority, succession | U | U | U | C | U | U | U | I | I | I | U | I | I | N | U | X | U | U | **Contradictory** (TVC-030/033 proposals pending; TVC-041) |
| Investments, custody, NAV | U | I | I | U | U | I | U | N | N | B | I | I | I | N | I | U | I | U | **Incomplete** (custodian transitions, NAV error policy, capital calls) |
| Accounting, reconciliation, reporting | U | U | I | U | X | U | U | I | N | B | U | I | I | U | U | X | U | U | **Contradictory** (TVC-028 SoD; OD-19 recognition [C]) |
| Fees | U | U | I | U | U | I | U | I | N | U | U | I | U | U | I | U | I | N | **Incomplete** |
| Compliance and sanctions | U | U | I | N | U | U | U | N | N | U | U | X | I | N | I | X | U | U | **Contradictory** (TVC-006, 015, 029; ~25 unmapped legal rows) |
| Security and identity | U | U | U | N | X | U | U | U | I | U | U | I | I | N | U | X | U | U | **Contradictory** (TVC-025; collusion and break-glass residual) |
| Embedded widgets and partners | U | U | U | N | U | U | U | U | I | U | U | I | U | I | U | U | U | U | **Coherent with unresolved assumptions** (TVA-013 partner contracts) |
| AI governance and agents | U | U | U | N | U | U | U | U | N | U | U | I | U | U | U | X | U | U | **Contradictory** (TVC-007 proposal pending; TVC-041 delegation) |
| Service and UX | I | U | I | N | U | U | U | U | I | U | U | N | I | B | I | U | U | U | **Incomplete** (charity flows, assisted channel, copy untested with users) |
| Operations and resilience | I | I | I | N | U | I | U | I | N | U | U | I | I | B | I | U | U | U | **Incomplete** (rota, degraded mode, DR consistency, bulk-Unknown procedure) |
| Migration | U | I | I | U | U | I | U | N | N | B | U | I | I | N | I | U | I | N | **Incomplete** (in-flight import, migrated state) |
| Organization and economics | U | — | — | — | U | — | U | — | — | — | U | I | I | B | U | X | U | U | **Blocked by external evidence** (exception rate, minutes, surge: GAP-001/034) |

## 2. Domain narratives (the most consequential)

### 2.1 Grant decisioning
- **Sufficiently specified:**
  - request ≠ instruction;
  - D/P/H typing;
  - flag-only AI;
  - recommendation and grant lifecycles (rev 2);
  - status dimensions.
- **Incomplete:** the TVCTL-05 fallback screen content; the benefit-detection evaluation set.
- **Contradictions:** TVC-003 (is policy approval legal approval?), TVC-025/026 (assurance vs auto-approval), TVC-044 (giving-plan grooming).
- **Most dangerous assumption:** TVA-001 (board-delegated policy = approval).
- **Evidence that would change the conclusion:** a counsel opinion (OD-01); shadow replay of past grants (GAP-001/034).
- **Essential future tests:** a canary to a revoked recipient at release; an auto-approval attempt from a phishable session to a new recipient; giving-plan re-confirmation at execution.
- **Do not implement until resolved:** the **no-touch routine approval path**. Build the human-batch-approval path first; it is the fallback in every option.

### 2.2 Payments and disbursement
- **Sufficiently specified:** the attempt machine rev 2 (cumulative PA-1, two-source NotReceived, contradicting evidence, Lost, checks), as amended by rev 3 A1–A23. Round 3 found no new severity-4 or 5 issue in this lifecycle: **approaching saturation** after fold-in.
- **Incomplete:** the bulk-Unknown procedure (TVF-164); the per-provider observation-implication table (PA-6).
- **Most dangerous assumption:** TVA-005 (providers can prove non-receipt and honour keys).
- **Evidence:** executed provider contracts (GAP-002); vendor confirmations (OUTSTANDING C7).
- **Essential tests:** crash injection at every attempt transition (core G5); a restore from backup with provider-accepted attempts (TVF-144).
- **Do not implement:** live money movement on any rail without contracted idempotency and a query capability. Do not build any off-platform payment path (TVR-PAY-004).

### 2.3 Reservation, funding and treasury
- **Specified:** FI-05..16 capacity, fixing and over-commitment; GR-10 single ordering key.
- **Open:** the funding mechanism (OD-13); haircut rates (OD-05); pool liquidity at year-end; the review dispute on cash sleeve vs pool buffer.
- **Dangerous assumption:** TVA-006 (custodian redemption mechanics).
- **Do not implement:** any unit earmark (TVC-022) until the funding mechanism is chosen.

### 2.4 Contributions
- **Specified:** Provisional/Final states (CON-1..3), the reversed-contribution path, FI-22..24.
- **Blocked:** acknowledgment timing and gift date per rail [C] (OD-04, TVF-115).
- **Do not implement:** acknowledgments generated from bank settlement events for reversible rails.

### 2.5 Accounting, reconciliation and reporting
- **Specified:** FI-01..04, FI-17, FI-28 (NAV error), FI-36..38.
- **Contradictory:** reconciliation independence (TVC-028).
- **Blocked:** grant recognition point (OD-19 [C]); break rates (GAP-005).
- **Do not implement:** a reconciliation function reporting to the Controller who releases payments.

### 2.6 Compliance and sanctions
- **Specified:** authority classes; control template (TVR-CMP-001); TVCTL-01..14.
- **Incomplete:** ~25 legal rows unmapped (TVF-045); retention (OD-12).
- **Contradictory:** coverage overclaims (TVC-015, 029).
- **Dangerous assumption:** TVA-028 (sanctions recall on transliterated names).
- **Do not claim:** any SOC 1/SOC 2 status. Do not label controls "operating" without independent tests.

### 2.7 Security and identity
- **Specified:** the authorization formula with tenant terms; AUTH-I1..I8; TVCTL-06/10.
- **Residual (catastrophic, severity 5):**
  - destination substitution at a provider, invisible to the sponsor (TVF-222; amendment B18);
  - movements in external registers (custodian deliveries, identity-provider admin actions) with no matching command (TVF-223; B19);
  - two-person collusion (TVF-077, 131).
- **Residual (severity 4):**
  - break-glass data edits (OD-22);
  - edit-then-revert (TVF-209);
  - restore consistency (TVF-144, 207, 216).
- **Saturation:** not reached after round 3 (see the scenario library).
- **Do not implement:**
  - any human write path to payee, authority, ledger or policy data that bypasses domain commands;
  - any payment to a provider-tokenized destination without per-payment destination confirmation (B18).

### 2.8 Organization and economics
- **Specified:** the allocation rule (H/D/P/agent); SoD pairs; closed-form staffing and surge model.
- **Blocked:** e, m, k (GAP-001/034, TVA-002..004).
- **Unresolved disagreement:** the minimum staffing floor (~10 vs 8–10).
- **Do not commit to:** headcount plans or pricing derived from the average-volume model.

## 3. Readiness gates proposed before any implementation phase

| Gate | Condition |
|---|---|
| TR-1 | OD-01, OD-03, OD-04, OD-12, OD-19 answered by counsel or CPA |
| TR-2 | One requirements body (OD-15) with a single status vocabulary (TVC-008) |
| TR-3 | Every P0 workflow (CW-01..12, 21, 24..27) specified to the 18-field template |
| TR-4 | Provider and custodian capability evidence for every rail and custodian in scope (TVA-005/006) |
| TR-5 | Shadow-replay measurement of e and m (GAP-001/034) before staffing or pricing commitments |
| TR-6 | Every control row carries all TVR-CMP-001 fields with REG links |
