# Ledger: theoretical enterprise validation

**Branch:** `claude/daf-theoretical-validation-4zbxfh`. **PR:** kemiller2002/daf-landscape#85 (draft). **Session date:** 2026-11-22.

## 1. How to resume

1. Read the [README](README.md), then the [executive findings](18-executive/executive-findings.md) and this ledger's §4 continuation plan.
2. The scenario library is `11-scenarios/scenarios.csv`. Scenario IDs by round:

   | Round | Scenario IDs |
   |---|---|
   | 1 | TVS-0xx |
   | 2 | TVS-2xx–4xx |
   | 3 | TVS-5xx–6xx |
   | 4 | TVS-7xx |

   Finding IDs are TVF-nnn. The `finding_id` column links scenarios to findings.
3. When a challenger round runs in a separate context, it writes to a scratch CSV with the same 12-column header. The author merges it with ID remapping:

   | Round | Source scenario IDs | Mapped to |
   |---|---|---|
   | 2 | R2G / R2X / R2S | TVS-200 / 300 / 400 + n |
   | 3 | R3G / R3S | TVS-500 / 600 + n |
   | 4 | R4S | TVS-700 + n |

   | Source finding prefix | Mapped to |
   |---|---|
   | G | TVF-077 + n |
   | X | TVF-109 + n |
   | S | TVF-130 + n |
   | H | TVF-176 + n |
   | K | TVF-200 + n |
   | M | TVF-225 + n |

   Review-derived findings are TVF-153..176.
4. Never edit `docs/` or `research/ai-native-daf-enterprise/` from this program. Record conflicts in the [contradiction register](16-registers/contradiction-register.md).

## 2. Checkpoints

| Commit | Content |
|---|---|
| ac24356 | Charter, discovery inventory, state models, financial invariants, contradiction register |
| c23d223 | Ontology, organization and authority, workflows, UX, widgets, controls, round-1 scenarios |
| dc1044a | Alternatives, economics, failure analysis |
| 3b60373 | Findings, assumption, owner-decision and requirements registers |
| 6ecb2d1 | Round 2 + role-separated reviews integrated (revision 2) |
| (next) | Index, readiness draft |
| 887e599 | Round 3 + revision-3 amendments |
| 0c83b9e | Executive findings, readiness update, P0 rev-3 requirements |
| (this) | Round 4, scenario library and saturation, ledger |

No executable artifacts were created, and no existing file outside this directory was modified.

## 3. Metrics

**Telemetry.** Only sub-agent token counts and durations were reported by the harness. The main session's own token use and cost were **not available** and are not estimated here.

| Pass | Kind | Sub-agent tokens (reported) | Output |
|---|---|---|---|
| Inventory: UI and widgets | Read-only inventory | 111,970 | Vocabulary and contradiction inventory |
| Inventory: governance and regulatory | Read-only inventory | 158,822 | REG/CTL inventory |
| Inventory: reviews, economics, org | Read-only inventory | 177,520 | Economics and assumptions inventory |
| Round 2: grants | Challenger | 147,184 | 83 scenarios, 32 findings |
| Round 2: cross-domain | Challenger | 177,046 | 81 scenarios, 21 findings |
| Round 2: security | Challenger | 189,161 | 88 scenarios, 22 findings |
| Review: financial controls + operations | Role-separated | 144,854 | 24 objections |
| Review: compliance + evidence | Role-separated | 233,464 | 37 objections, 48 citation checks |
| Review: architecture + economics | Role-separated | 155,449 | 34 objections |
| Review: UX + red team | Role-separated | 131,493 | 27 objections |
| Round 3: grants | Challenger | 155,162 | 56 scenarios, 24 findings |
| Round 3: security and cross-domain | Challenger | 160,322 | 56 scenarios, 25 findings |
| Round 4: security, targeted | Challenger | 144,670 | 47 scenarios, 29 findings |
| **Sub-agent total** | | **2,087,117** | |

**Analytical output:**

| Measure | Value |
|---|---|
| Scenarios | 513 |
| Findings | 242: sev 5 × 17, sev 4 × 96, sev 3 × 99, sev 2 × 29, sev 1 × 1 |
| Contradictions | 44 |
| Assumptions | 30 |
| Owner decisions | 22 |
| Requirements in graph | 61 |
| Proposed controls | 14 |
| Revision-3 amendments | 44 |

**Duplicates.** 38 scenario rows were classed as duplicates and excluded from finding counts.

**Errors caught in review.** 12 corrections were made to the program's own text: arithmetic presentation, citations, legal-label inflation, and SoD derivation ([role reviews §1](13-adversarial-reviews/role-reviews.md)).

**Cost per useful finding.** Not computed: main-session cost is unknown. In sub-agent tokens alone, about 8.6k tokens per registered finding across all passes. Inventory and review passes produced corrections rather than registered findings, so this ratio understates them.

**Where effort paid off.** Round 1 and the role reviews produced the highest-severity and most corrective output. Rounds 3–4 on the grant lifecycle produced low-severity consistency findings, which is diminishing returns. Rounds 3–4 on security still produced severity-5 paths, but each new control created new attack surface.

## 4. Continuation plan

Ordered by value; none of it has started.
1. **Fold in revision 3** (A1–A23, B1–B21) to the base state models, invariants and status vocabulary. Then run one confirmation round on the grant lifecycle (~40 scenarios). The expected outcome is mainly covered-refined rows.
2. **Collect counterparty capability evidence** (GAP-002, OUTSTANDING C3/C6/C7):
   - provider idempotency and deduplication windows;
   - per-item observability;
   - destination fingerprints;
   - custodian per-movement reporting;
   - bank-portal logging.

   Then draft revision 4 for round-4 findings TVF-226..254, and run a confirmation round on restore and external registers.
3. **Specify missing workflows** CW-21..45 to the 18-field template, starting with CW-21 closure, CW-26 custodian correction, CW-27 contribution reversal, CW-36/43 migration and CW-45 bank failure.
4. **Owner and counsel actions:** OD-01, OD-04, OD-12, OD-19, OD-20, OD-22 first.
5. **Requirements hygiene:**
   - cross-reference map between `docs/` and AI-native IDs (OD-15);
   - single status vocabulary;
   - control template fields in `controls.csv` (outside this directory; needs owner approval).
6. **Economics:** add determination reuse and pessimistic labour for all staff; model the complex-asset surge. Replace all parameters with shadow-replay measurements when available.
