# 16 — Software development economics

Evidence: [echelon-shared-and-development-notes.md](data/evidence/echelon-shared-and-development-notes.md) §3 (measured from git history and Praxis telemetry), [`shared-capabilities.csv`](data/registers/shared-capabilities.csv), [`original-cost-trace.csv`](data/registers/original-cost-trace.csv) OCT-061..073. Model lines: FC-301..FC-304 and TECHOPS activities.

## 1. What has actually been recorded

| Record | Measured value | What it does **not** show |
|---|---|---|
| Unbound git history | 400 commits over **6 active days** (2026-11-21..26); 128 Claude-authored, 272 owner account; 287,796 lines inserted, mostly JSON/Markdown/CSV; **27,032 F# lines**, of which 22,092 are requirements/economics tooling and 2,558 runtime (`execution/`) | human hours; review depth; accepted capability; defect rate |
| Unbound product code | **No product application exists**; one incubating runtime library (Echelon.Execution) | — |
| Unbound engineering hygiene | **No CI, no Praxis installation, no licence file** | — |
| 11 Echelon repositories | 5,609 commits; 47% Claude-authored; **one human identity** | effort |
| Praxis execution telemetry | 1,017 records; **7 with token counts; 0 with cost or human time**; wall-clock includes idle sessions | effort or cost |
| Static analysis / dependency scanning | Absent in all 11 CI configurations inspected | — |

**Conclusion: there is no evidence on which to estimate Echelon's development cost from its own history.** Output is large and fast; effort, cost, and the share of output that becomes accepted, maintained capability are unmeasured. Commit counts are not effort.

## 2. The original $1.94M build

$663k non-compressible (30% of a $2.21M scope) + $1.031M construction (70% ÷ 1.5 AI compression) + $26k agent compute + $220k safety floor. The $2.21M scope is an agent estimate (132 conventional person-months at $120/h) scaled against Unbound's own $5M build figure, which has **no derivation** (`parameters.json` build_capex 5,000,000, range 3-15M, label "assumption"). Missing items flagged by the trace: a deferred-scope tranche (~$0.6M), startup legal and regulatory opinion (~$0.12M), and the scope gap between the costed MSP (one sponsor, manual NAV import) and the levers the AI-native mode assumed (high case ≥ $3.6M).

Neither the $1.94M nor any lower figure can be supported or refuted with current records. The defensible statement is a wide range with explicit dependence on measurement.

## 3. Zero-based treatment

| Category | Treatment | Lines |
|---|---|---|
| Initial product development (cash still to spend) | One-time; **$0.15M / $0.5M / $1.2M**. Cash is agent usage, contract testing/review, accessibility and security testing; founder labour is non-cash | FC-301 |
| Initial development at market replacement value (economic) | One-time; **$0.7M / $1.5M / $2.43M** (inside the baseline's $1.1-2.43M range) | FC-302 |
| Shared framework investment | Not charged to Unbound; Unbound's share of upkeep is allocated (35% driver) | FC-101 (View 2) |
| Assurance readiness | One-time $15-60k | FC-303 |
| Legal establishment | One-time $20-80k (conflicts with DF-ASR-2026-0D0F) | FC-304 |
| Sponsor-specific onboarding and migration | Activity hours per new sponsor (~790 h base) | OA-COM-* |
| New feature development | **Not in operating cost**; product investment decision | — |
| Defect correction, routine maintenance, dependency and security updates, regulatory change, integration maintenance, deployments, AI change control | **Recurring operating cost** as TECHOPS activities (≈ 1,700-1,900 engineering hours a year at small scale) | OA-TEC-001..021 |
| Operational incident response | Seeded incidents in the simulation plus TECHOPS rows | Simulation |

At small scale the recurring engineering load (~1,700 h) plus author-plus-two change approval (3 named engineers) produces **two dedicated engineers plus founder hours** — about $425k of View 1 cash. This is the largest single block of Unbound's minimum operating cost, and it exists because AI-generated software still has to be maintained, reviewed, secured and operated.

## 4. Do not assume AI-generated software is cheap to maintain

Arguments for caution, all recorded as findings:

- **Review is the bottleneck, not authorship.** CNV-PLT-010 requires two non-author approvers on control-relevant modules. With one human, it cannot be met; review hours scale with change volume, not with lines written.
- **Volume creates surface.** 288k lines in six days, much of it data and requirements, will need curation; drift between requirements, models and code is already visible (stale registers, superseded figures).
- **No safety net yet.** No CI, no static analysis, no dependency scanning in Unbound; these must exist before a regulated sponsor's due diligence.
- **Immature dependencies.** Transitus has no code; monitoring, hosting, donor identity and support are absent in Echelon; Limen does no identity; Folio has no PDF engine; Arca stores records in GitHub (unsuitable for a regulated ledger). Unbound will bear the cost of building or replacing these until they mature — a transfer, not an elimination, of cost.
- **Licensing.** Most shared components are PolyForm Noncommercial; a commercial Unbound needs a licensing decision (owner decision; not costed).

## 5. Cash break-even versus investment recovery

These are reported separately ([18](18-break-even-analysis.md)):

- **Cash break-even** covers View 1 recurring cost only.
- **Investment recovery** asks how long contribution margin takes to repay FC-301 (cash) or FC-301..304 (economic), and is shown as break-even "with investment" (amortised over 5 years) and as a payback period.

Historical development spend is treated as **sunk** for operating decisions and as **economic investment** for the allocated view.

## 6. What to measure

1. Engineering hours per accepted, reviewed change (by Praxis work item), and reviewer hours per change.
2. Agent token cost per work item (Praxis telemetry fields exist but are unpopulated).
3. Defect escape rate and incident rate after first production use.
4. Hours spent on shared components on Unbound's behalf (allocation driver for FC-101).
