# Role-separated adversarial reviews

**Independence statement.** Every pass below ran in a **separate model context** from the author's. Each received the artifacts and the baseline files, not the author's reasoning, and was told to find faults. All passes used the **same model family** as the author, so shared blind spots are likely. These are **role-separated self-critique, not independent validation**. No pass declared its own findings validated. The author has accepted, rejected or deferred each objection below; those dispositions are themselves unreviewed.

The raw review records are kept verbatim in [`raw/`](raw/). They include objections the author did not accept (minority findings).

| Pass | Directive roles | Objections | Raw record |
|---|---|---|---|
| R-1 | Financial Controls Reviewer; Operations Reviewer | 14 + 10 | [review-fin-ops.md](raw/review-fin-ops.md) |
| R-2 | Compliance Reviewer; Independent Evidence Reviewer | 20 + 17, with a 48-row citation table | [review-compliance-evidence.md](raw/review-compliance-evidence.md) |
| R-3 | Enterprise Architect; Economics Reviewer | 19 + 15 | [review-arch-econ.md](raw/review-arch-econ.md) |
| R-4 | User Experience Reviewer; Adversarial Red Team | 16 + 11 | [review-ux-redteam.md](raw/review-ux-redteam.md) |
| S-2 | Security Reviewer | Round-2 red-team scenarios (88 rows, 22 findings) | [scenarios.csv](../11-scenarios/scenarios.csv) rows TVS-401..488 |

## 1. Objections that changed a conclusion

| Objection | Was | Now | Where |
|---|---|---|---|
| R-3 B1 | "AI-native cost advantage disappears; flips at e ≥ 15% and m ≥ 120" | Advantage **approaches parity** in the high case (~$768 vs ~$790). The flip condition is e·m ≈ 24 or 41 | [economics §2](../15-economics/economic-model.md) |
| R-1 B-1, R-3 B7, R-2 B5 | "Backlog ≈ 37 days; matches the twin" | Clearance takes **~223 working days** under average staffing. The agreement with the twin is circular | economics §3 |
| R-3 A1 | "Graph-colouring ⇒ ≥ 4 people" | The constraint graph is bipartite (2). The floor comes from absence coverage. Disagreement preserved: ~10 people (R-1) vs 8–10 (org model) | [organization §4](../03-organization/organization-and-authority.md) |
| R-2 B1 | "No cancel transition in WF-01" | WF-01 *has* `Approved → Canceled` (donor). The defect is who cancels, and cancellation after release | TVC-021, TVF-005 |
| R-2 B3 | "E9 assumes bank deduplication" | E9 *states* that ACH lacks an end-to-end key | TVC-024 |
| R-2 A1 | REG-001 treated as verified law | Only the statute text is verified. Per-grant approval is interpretation | TVC-003, compliance §1 |
| R-2 A11, R-4 B3, R-1 A-6 | Nacha R10 window applied to grant payments; labelled [V] | Applies to contributions (debits) only. Downgraded to [S] | compliance §1, PA-9 |
| R-1 A-3 | Per-grant liquidation | Unitized pools redeem internally and trade net | FI-14 rev 2, TVC-043 |
| R-3 A10–12, B12 | Cash sleeve recommended | **Open** (OD-13). Reviewers prefer a pool buffer with currency reservation | alternatives §1 |
| R-4 B1 | Giving plan as a safe surge lever | Creates the TVF-153 grooming chain. Allowed only with REC-7 and AUTH-I7 | alternatives §2 |

## 2. Objections that corrected a rule (state-model and invariant revision 2)

These were accepted and applied as *proposals*:
- check void path (R-1 A-1, R-3 A6, R-4 B2, round 2 G-11);
- cumulative PA-1;
- two-source NotReceived;
- PA-2 decision state;
- Unknown deadline (R-4 B9);
- Abandoned attempt exits;
- contradicting-evidence case;
- provider deduplication window;
- funds in transit;
- `Lost` claim;
- FI-03 buckets and break-blocking scope (R-1 A-2, A-11);
- single ordering key GR-10 (R-1 A-4);
- reversed-contribution NAV differential (R-1 A-5);
- residue release (R-1 A-8);
- FI-36..39;
- model-raised flags never supersede themselves (R-4 B6);
- unauthenticated death notices (R-4 B7);
- headline priority and Unknown copy (R-4 A1–A3);
- OFAC blocking (R-2 A5 → TVCTL-13);
- disqualified supporting organizations and §4958 payee block (R-2 A8, A18 → TVCTL-14);
- external auditor not cited as a control (R-2 A14).

## 3. Objections recorded but not acted on (minority or deferred)

| Objection | Reason not acted on |
|---|---|
| R-3 A13/A14: moving the evidence ledger and telemetry relocates the self-assurance problem rather than removing it | Partly accepted. TVCTL-11 now names internal audit as accountable. The org-design question is left to the owner. |
| R-3 A17: the program over-specifies mechanisms (revisions, hashes, ~40 states) | **Accepted as valid and unresolved.** The state models are a requirements *checklist*, not a design. Implementers may collapse states that preserve the invariants. This tension with the program's own TVR-DATA-001 stance is recorded. |
| R-2 A15: privacy vs retention conflict overstated | Deferred to counsel (OD-12) |
| R-2 A7: TVC-006 severity should be 4 | Noted in the register. Severity left at 5 pending CRCO and GC review of the qualifier. |
| R-1 B-5: over-commitment case-by-case CFO handling infeasible at volume | Accepted as a finding. The policy rule (OD-08) is the remedy; no automation proposed. |
| R-3 B5: no determination-reuse term in any case | Accepted; it biases costs upward. Not modelled (baseline OUTSTANDING B1). |
| R-2 B12: conclusions resting only on the program's own artifacts | Accepted as a standing caveat. Such conclusions are labelled [T]. |

## 4. Points that two or more reviewers could not fault

- SM-0 child correction records.
- Unknown never treated as failure.
- No reservation release on timeout.
- PA-3 per-attempt keys.
- Economics arithmetic (all closed forms).
- Contradiction-register counts.
- FT-1's conclusion that double-payment paths are mainly organizational.
- The widget trust-boundary table.
- No SOC compliance claim anywhere.

**This does not make them correct.** It means these role passes did not find a counterexample.
