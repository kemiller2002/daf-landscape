# Executive findings: DAF theoretical enterprise validation

**Date:** 2026-11-22. **Status:** theoretical.
- Nothing has been implemented.
- No counsel, CPA, auditor, sponsor or user has reviewed these findings.
- Reviews were **role-separated self-critique by one AI model family**, not independent validation ([charter §5](../00-program-charter.md#5-independence-statement)).
- No production-readiness or SOC 1/SOC 2 claim is made.

## 1. Executive assessment

The DAF requirements are **strong in principle and weak at the seams**. The baseline gets the hard *legal and governance principles* right:
- a recommendation is a request, not an instruction;
- AI may add flags but never clear them, and holds no financial authority;
- a timeout means "unknown", not "failed";
- ledger, custody and legal ownership are separate records;
- the sponsor never self-custodies assets.

Where it is wrong or incomplete is the **mechanics between those principles**:
- how approved grants meet cash;
- how payments are proven, or proven not to have happened;
- when contributed money is really final;
- who may act when authority changes;
- how controls are evidenced.

**Quantified result:**

| Measure | Count |
|---|---|
| Scenarios analysed, rounds 1–4 | 513 ([library](../11-scenarios/scenario-library.md)) |
| Findings registered | 242: 17 at severity 5, 96 at severity 4 |
| Contradictions recorded | 44, none silently resolved |
| Owner decisions required | 22 |
| New traceable requirements | 61 |
| Domains rated "theoretically coherent" overall | **None** |

The grant and payment lifecycle is **approaching saturation**: round 3 found no new severity-4 or 5 issue there. Security and cross-domain failure chains are **not saturated**. Four rounds found 4 → 2 → 1 new severity-5 paths per round, and each revision's controls opened new paths. Theoretical expansion stopped because the remaining questions depend on real counterparty capabilities ([scenario library §3.3](../11-scenarios/scenario-library.md#33-security-and-external-dependencies-not-saturated-and-not-converging-under-theoretical-rounds)).

**The single most important conclusion.** The no-human-touch routine approval path (DD-004) is the economic heart of the AI-native design, and it is the least settled element legally and in its security posture:
- Whether board-delegated policy approval counts as the sponsor's approval of each grant is a matter of interpretation, not verified law ([TVC-003](../16-registers/contradiction-register.md); [review correction](../13-adversarial-reviews/role-reviews.md)).
- Phishable sessions and donor agents can currently reach that path ([TVC-025/026](../16-registers/contradiction-register.md)).
- A giving-plan variant opens a grooming attack ([TVF-153](../16-registers/findings.csv)).

**Build the human-batch-approval path first.** Every option falls back to it.

## 2. Enterprise completeness

| Area | Assessment | Evidence |
|---|---|---|
| Ontology | Two partial ontologies merged. Several facts have competing authoritative claimants with no field-level rule. | [ontology §3](../02-ontology/enterprise-ontology.md) |
| Workflows | 44 identified. The baseline does not define 18 of them, and 14 of those are below one-third specified. The missing ones include fund closure, freeze, merge/split, contribution reversal, custodian correction, transfer-in, sponsor succession and bank failure. | [workflow catalog](../05-workflows/workflow-catalog.md) |
| State machines | The baseline grant machine lacked reservation, funding, Unknown, post-settlement return and correct cancellation semantics. Corrected in three revisions. | [state models](../06-state-models/state-models.md), [rev 3](../06-state-models/revision-3-amendments.md) |
| Requirements governance | Two requirement bodies specify the same enterprise without cross-references. There are seven grant-status vocabularies, three gate schemes and colliding test IDs. | [inventory §3](../01-discovery/requirements-inventory.md) |

## 3. Most consequential missing requirements

1. **Grant funding mechanics.** There was no reservation, funding or fixing rule. A fall in investment values could leave approved grants underfunded. → FI-05..16, GR-1/10, OD-07/13. ([TVF-001](../16-registers/findings.csv), TVF-009, TVC-022)
2. **Payment proof.** The baseline had no Unknown state and no two-source proof of non-receipt. Rails without end-to-end keys cannot satisfy the core's own idempotency invariant. → PA-1..9 rev 2/3, TVR-PAY-002. (TVF-003, TVF-024, TVC-024)
3. **Contribution finality.** Reversible ACH debits are spendable and acknowledged on settlement. Unauthorized consumer debits may return for about 60 days [S: Nacha summaries]. → CON-1..3, FI-22/23, OD-04. (TVF-006, TVC-023)
4. **Authority-change propagation.** No stated window for sessions, widgets, tokens, recurring templates or third-party registers. → AUTH-I1..I8, TVCTL-10, B2/B19. (TVF-015, TVF-223)
5. **Destination integrity outside the platform.** Provider-held tokens and external registers can change with no sponsor-visible command. → amendments B18/B19. (TVF-222, TVF-223)
6. **Control evidence fields.** No retention, failure response, independent verification or escalation fields, and no REG links; about 25 legal rows have no control. → TVR-CMP-001/002, TVCTL-01..14. (TVF-040, TVF-045)
7. **OFAC blocking and reporting**; a disqualified-recipient and §4958 payee gate. → TVCTL-13/14. (TVF-171, TVF-172, TVF-175)

## 4. Critical contradictions

Full list: [contradiction register](../16-registers/contradiction-register.md). Severity 5:

| ID | Conflict |
|---|---|
| TVC-003 | No-touch routine approval vs the per-grant sponsor approval reading of REG-001 (an interpretation conflict) |
| TVC-006 | Sanctions guidance wording permits automated clearing of low-score matches vs "AI never clears" |
| TVC-021 | Baseline grant machine vs real return, cancel and correction events |
| TVC-022 | Unit earmark vs currency reservation |
| TVC-023 | ACH contribution "settled" vs reversible |
| TVC-024 | Core idempotency invariant vs rails without end-to-end keys |
| TVC-025 | Phishable sessions vs auto-approval ceilings |
| TVC-044 | Giving-plan pre-clearance vs request-time assurance |

## 5. Highest-severity failure scenarios

| Scenario | Path | Status |
|---|---|---|
| Duplicate payment after a provider timeout | [FT-1](../12-failure-analysis/failure-analysis.md#ft-1-money-leaves-the-sponsor-twice-for-one-grant). Single-failure cut sets are **organizational**: off-platform payment, and provider double-processing. | Designed controls; blocked on provider contracts |
| Account takeover → auto-approved grant to an attacker's real charity | TVS-025, TVS-026, TVF-153 | TVCTL-06, REC-7, B2/B3/B20 proposed |
| Destination substitution at a provider, or at the custodian/bank settlement-instruction level | TVF-222, TVF-233 | B18 proposed; round 4 found the provider-computed fingerprint insufficient (TVF-234). **Open.** |
| Insider standing-data edit or two-person collusion | TVF-131, TVF-139, TVF-209 | OD-22, B8, TVR-SEC-006. **Residual.** |
| Lossy disaster-recovery restore → payments without approval, or re-payment | TVF-144, TVF-216 | B6 proposed |
| Year-end conjunction: surge + market drop + provider timeout + IRS revocation publication | [failure analysis §4](../12-failure-analysis/failure-analysis.md#4-event-storming-of-a-high-stress-day-narrative-check) | TVR-OPS-003 drill; no model exists |

## 6. Cross-domain weaknesses

- **Shared scarce people.** Specialists, payment operations and the contact channel all degrade on the same year-end day (failure analysis §4).
- **External registers** (custodian, bank portals, identity provider, provider tokens) sit outside every platform control (TVF-223).
- **Status semantics** cross grants, payments, widgets and service. One word ("Accepted") means three things (TVC-008).
- **Migration** imports in-flight items that the state machines cannot represent (TVF-110, TVF-111).
- **Multi-sponsor (Model C/D) correlated error.** One policy pack or registry error affects every tenant. This is unquantified (TVF-062).

## 7. Recommended operating-model changes

These are **recommendations, not decisions.** See [alternatives](../14-alternative-operating-models/alternatives.md).
1. **Reconciliation independent of payment release** (TVC-028, TVCTL-07).
2. **Move controls earlier:**
   - giving plans, with confirmation at clearance (2D + B10);
   - pre-verified successors (5C);
   - deterministic list re-evaluation, never agent re-runs (TVR-ECON-002).
3. **Proactive five-dimension status** to remove "where is my grant" contacts (6C, [status vocabulary](../09-ux/status-vocabulary.md)).
4. **Funding mechanism: open (OD-13).** The program's original cash-sleeve recommendation was **withdrawn** after the reviews preferred a pool-level buffer with currency reservation. The disagreement is preserved.
5. **Thin-sponsor shape (7D)** is plausible only if providers publish scoped SOC reports. None of the 13 studied does (GAP-025).

## 8. UI and accessibility findings

- The status vocabulary needs five dimensions and a headline priority rule. Revision 2 fixed headline errors found in review: a hold hiding money in flight; "Returned" showing forever on canceled grants; Unknown copy that invited duplicate grants.
- There was no persona for users with disabilities, auditors, charities, executors or board members; 21 personas are now defined.
- **Charities are users with no flows.** Return copy must not prime bank-detail phishing.
- WCAG 2.2 criteria that matter for financial flows are unnamed:
  - 3.3.7 Redundant Entry;
  - 3.3.8 Accessible Authentication;
  - 2.4.11 Focus Not Obscured.
- Accessible step-up must not become a social-engineering bypass (TVF-156).
- Conversational AI should be an *entry point* into a deterministic review screen, never the submission itself ([interaction models §3](../09-ux/personas-and-interaction-models.md)).

## 9. Financial and compliance concerns

- Accounting questions needing a CPA [C]:
  - the recognition point for grants (OD-19);
  - the NAV-differential loss on reversed contributions (FI-23);
  - the NAV-error restatement policy (FI-28);
  - fund charges and UBIT (FI-37).
- Compliance:
  - coverage is overclaimed in the specification itself (TVC-015);
  - CTL-037 cannot fail on guidance or conditional legal rows (TVC-029);
  - retention is unverified except the OFAC 10-year floor (TVC-016);
  - SOC 1, not only SOC 2, is relevant where fund accounting is a service-organization function (TVC-027).
- Every TVCTL is **designed only**.

## 10. Economic sensitivities

From the [economic model](../15-economics/economic-model.md), corrected after review:
- **Exception specialist cost** has elasticity 1 in exception rate *e* and minutes *m*. The high case (~$768 per account) **approaches** the conventional frontier (~$790). The flip point is at e·m ≈ 24 under pessimistic labour costs, or ≈ 41 at base.
- **Surge.** Average-volume staffing gives a December backlog that takes **~223 working days** to clear. Service-level staffing needs ~54–63 FTE at peak against 30 on average (expected case).
- **AI inference** is immaterial below ~$4 per exception dossier, but per-grant agents become material at ~$0.31 per run.
- **Correlated failure and incident costs are unmodelled**, and they are decisive for multi-sponsor models.
- Every parameter is an assumption. The repository has no operational measurement.

## 11. Assumptions requiring external validation

The P0 rows of the [assumption register](../16-registers/assumption-register.csv):

| Assumption | Statement | How to validate |
|---|---|---|
| TVA-001 | Board-delegated policy counts as approval | Counsel |
| TVA-002/003/004 | Exception rate, minutes per exception, surge multiplier | Sponsor shadow replay: GAP-001/034 |
| TVA-005 | Providers can prove non-receipt and honour keys | Contracts: GAP-002 |
| TVA-009 | Sham-charity detection is adequate | Red team |
| TVA-011 | Automation bias is controllable | Seeded-error measurement |
| TVA-028 | Sanctions recall on transliterated names | OUTSTANDING B6 |

## 12. Theoretical readiness by domain

See the [readiness report](../17-readiness/readiness-report.md).

| Classification | Domains |
|---|---|
| **Contradictory** | Grant decisioning; reservation/treasury; contributions; parties and authority; accounting; compliance; security; AI governance |
| **Blocked by external evidence** | Payments; organization and economics |
| **Incomplete** | Fund lifecycle; investments and custody; fees; service and UX; operations; migration |
| **Coherent with unresolved assumptions** | Charity registry; embedded widgets and partners |

## 13. Prioritized requirements changes

| Priority | Change | Link |
|---|---|---|
| P0 | Adopt the grant, recommendation and payment-attempt machines (rev 2 + rev 3) and the single ordering key | state models, rev 3 |
| P0 | Contribution Provisional/Final; acknowledgment timing per counsel | TVR-CON-001..003 |
| P0 | Release-time re-check including decision-snapshot verification; per-payment destination confirmation | TVCTL-04, B8, B18 |
| P0 | Assurance-bound auto-approval; recipient novelty measured by channel, not clock | TVCTL-06, B2, B20 |
| P0 | OD-22 standing-data rule extended to external registers | B19 |
| P0 | Control template fields and REG mapping | TVR-CMP-001/002 |
| P1 | One requirements body, one status vocabulary, technology-neutral text | OD-15/16, TVR-ARC-001 |
| P1 | Specify CW-21..45 | TVR-WF-001 |
| P1 | Restore-consistency rules | B6 |
| P1 | Surge-aware staffing and conjunction drills | economics §3, TVR-OPS-003 |
| P2 | Charity-facing flows; accessibility persona and WCAG 2.2 criteria | TVR-UX-004, UXA-1..6 |

## 14. Questions requiring owner decisions

22 items in the [owner decisions register](../16-registers/owner-decisions.md). The first five block the most work:

| ID | Question |
|---|---|
| OD-01 | Delegated approval legality |
| OD-04 | Provisional credit and acknowledgment timing |
| OD-13 | Funding mechanism |
| OD-19 | Grant recognition point |
| OD-22 | No direct standing-data edits, including external registers |

## 15. Recommended future implementation verification

When implementation is eventually authorized, these tests are essential. None has been run.
1. **Crash injection** at every payment-attempt transition, including a restore from backup with provider-accepted attempts (core G5; B6).
2. **Concurrency properties:** two-advisor capacity contention, cancel vs submit, recurring vs extraordinary grants (FI-08, GR-3, GR-10).
3. **Return fixtures** per rail, including after reconciliation and after closure (SM-0, A22/A23).
4. **Canary grants** to revoked or listed test recipients at release time (TVCTL-04), kept in a sealed register excluded from regulatory populations (TVF-145).
5. **Red team:**
   - phishable-session and agent new-recipient attempts;
   - giving-plan grooming;
   - destination substitution;
   - partner self-confirmation (TVCTL-06, B2, B18, TVF-136).
6. **Seeded-error reviewer tests** with and without AI summaries (TVR-UX-006).
7. **Authority-revocation propagation timing** across sessions, widgets, tokens and third-party registers (TVCTL-10, B19).
8. **Usability tests of status copy** with donors who have low technical familiarity, screen-reader users, bereaved users and charity finance staff.
9. **Shadow replay** of a sponsor's historical grants to measure *e* and *m* before any staffing or pricing commitment.
