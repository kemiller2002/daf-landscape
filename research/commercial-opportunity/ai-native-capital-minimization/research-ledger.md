# Research ledger

| Checkpoint | Commit | What | Verification |
|---|---|---|---|
| 0 | `97dddb7` (main) | Start of mission; previous study merged | — |
| 1 | `3388169` | Extension model scaffold: designs, layers, development, sequences, failures | 19 tests pass; baseline anchor $3.56M reproduced |
| 2 | `19b03bc` | Scenario matrix, cost bridge, CAC, value-based tariffs; verbatim mission brief | build + run |
| 3 | `d17e668` | OPS calibration: compliance owner floor, December release premium, two-approver code review, outcome-designed minutes | 19 tests |
| 4 | `16c14d6` | LYR full-scope platform base | 19 tests |
| 5 | `e6f2b2c` | DEV calibration: MSP $2.43M at 1x, 30% incompressible, maintenance floor | 20 tests |
| 6 | `8d7050e` | Pass datasets (DEV, OPS, COM, LYR), pass scripts, combined registers (local paths rewritten) | JSONL parse; CSV widths (passes) |
| 7 | `c6d9b0c` | ADV2 review data; model fixes for 22 of 27 findings (see report 16) | 23 tests pass |
| 8 | this commit | Existing-Unbound variant; reports 00-18, README, decision register, commercial milestones | 23 tests; results.md sha256 prefix recorded in report 14 |

## Test runs

- `dotnet test tests/CapitalMinimization.Tests`: 23/23 pass (2026-11-25).
- The previous model's 28 tests are untouched; the extension references the project read-only.

## Open items

- ADV2-025: schedule assurance and insurance lines by month before go-live.
- ADV2-026: reconcile sponsor-retained minutes (OPS 2.7, COM 7.0).
- No measured inputs. The gates in `commercial-milestones.csv` are the next evidence steps.
