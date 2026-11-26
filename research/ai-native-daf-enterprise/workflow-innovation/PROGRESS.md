# Workflow innovation: progress checkpoints

Resume by reading this file, then [`00-methodology/methodology.md`](00-methodology/methodology.md).

| Step (brief §18) | Status | Artifact |
|---|---|---|
| 1. Audit current research and architecture | done 2026-11-20 | [`01-existing-outcomes/audit-and-outcome-inventory.md`](01-existing-outcomes/audit-and-outcome-inventory.md) §1 |
| 2. Complete outcome inventory | done | same file §2; [`outcome-inventory.csv`](01-existing-outcomes/outcome-inventory.csv) |
| 3. Ten most expensive/complex/inefficient workflows (evidence-based) | done | same file §3; [`top-workflows.csv`](01-existing-outcomes/top-workflows.csv) |
| 4. ≥5 designs for each top workflow | done | [`03-alternative-designs/`](03-alternative-designs/) (105 designs) |
| 5. Adversarial evaluation | done (independent, non-author) | [`07-adversarial-reviews/`](07-adversarial-reviews/) |
| 6. Select candidates for experiments | done | [`10-prioritization/prioritization.md`](10-prioritization/prioritization.md) ranking 5 |
| 7. Executable or simulated tests | done; revised after audit | [`08-experiments/experiments.md`](08-experiments/experiments.md); F# E1–E10; E7/E7b public data; 75 tests |
| 8. Shared APIs and reusable capabilities | done | [`05-api-opportunities/`](05-api-opportunities/), [`06-agent-opportunities/`](06-agent-opportunities/), [`11-reference-architectures/`](11-reference-architectures/) |
| 9. Initial findings and unresolved questions | done | [`13-executive-synthesis/executive-synthesis.md`](13-executive-synthesis/executive-synthesis.md) |
| 10. Commit verified artifacts | done | git log |
| Remaining enterprise functions | done (≥5 designs each) | `03-alternative-designs/cap-*.md`, W11, W12 |

## Open items (next cycle)
- Wave 0 in [`12-implementation-proposals/implementation-roadmap.md`](12-implementation-proposals/implementation-roadmap.md): small-sponsor Schedule I harvest; the audit's missing adversarial experiment cases; policy compiler prototype; canary harness.
- Add proposed events and endpoints from 04- (about 40 events, about 20 endpoint families) to the parent catalogs, or reject them explicitly.
- Reconcile design-catalog maturity with the audit downgrades (verdicts.csv lists design-level downgrades).
- Experiments cited but not built (E5 complex-asset queue, E6 contact and liquidity, E2 back-test) are listed in `08-experiments/experiments.md`.

## Log
| Date | Work | Commit |
|---|---|---|
| 2026-11-20 | Methodology; framework repo inspected (empty at 57c53f7); outcome inventory; top-10; register | 2138f67 |
| 2026-11-20 | Designs, cross-enterprise workflows, catalogs, architecture; F# experiments; Schedule I harvest | de21c58, d82f23f |
| 2026-11-20 | Independent adversarial review; experiment fixes; claim softening; E7b; prioritization; implementation and framework proposals; synthesis | 0bed683 and this commit |
