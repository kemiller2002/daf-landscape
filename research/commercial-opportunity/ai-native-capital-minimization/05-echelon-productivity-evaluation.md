# 05: Echelon productivity evaluation

**Pass:** DEV (component verification, throughput, productivity sensitivity, measurement methodology, reduce vs transfer). **Data:**
- [`component-verification.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/component-verification.csv) (26 repos);
- [`throughput.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/throughput.csv) (31);
- [`loc.json`](../../../data/commercial-opportunity/ai-native-capital-minimization/loc.json);
- [`build-logs/`](../../../data/commercial-opportunity/ai-native-capital-minimization/build-logs/).

**Revisions examined:** 26 component repositories (praxis `12bf995`, ordo `db6d39e`, dokimos `6ea8624`, aegis `711e026`, vigila `feab755`, strata `c6a384e`, limen `743cdb9`, forma `c8f40b4`, folio `56a18e1`, conditor `cadd5c7` and 16 others; see [00](00-source-baseline.md)).

**Integrator conclusions**
- **Echelon is real, healthy software but contains no DAF capability** [M].
  - All 26 repos built and about 9,768 tests passed. Every failure was environmental or timing.
  - There is no ledger, payments, grants or reconciliation code. Fides is GitHub-only identity, Arca stores records in GitHub, and no repo runs SAST or dependency scanning.
  - 21 of 26 repos are PolyForm Noncommercial and two have no licence.
- **High output is demonstrated; the cost of an accepted capability is not** [S/M].
  - About 9,045 commits and about 1.12M lines added over 105 commit days, by one human author with 46.5% of commits agent-authored.
  - The only independent end-to-end trial (Rehearsal 4) passed 1 of 108 P0 requirements and was not accepted.
  - The ordo controlled trial cost $12-27 of compute per feature mission, and both agents' self-reported test results were wrong.
  - No human time is recorded anywhere.
- **Productivity sensitivity (1.5x, 2x, 3x, 5x, 10x) is bounded by Amdahl's law.**
  - With 30% of effort incompressible and compute at 5% of replaced construction, the savings ceiling is about 66% of conventional cost.
  - A nominal 10x is about 2.7x effective.
  - Agent compute is under 5% of build cost in every scenario: the cost is human review.
- **What Echelon can reduce** [D/E]:
  - Development: $0-1.1M on an MSP (UI and print markup, schema and fault tooling, and agent-written code if measured).
  - Operating cost: nothing yet. Echelon supplies no runtime.
  - Owner and Echelon time is a transfer and must be charged.
- **The measurement protocol below is the cheapest decisive evidence in the mission.** Run it on the next 3-5 Unbound capabilities: human hours per accepted capability, compute, cycle time, defect escape, rework and review overhead.
- **Threshold to replace conventional estimates:** effective 2x or better on accepted capabilities with no worse defect escape.
- **EDF applicability:** the Echelon development history and Rehearsal 4 are observed outcomes; ADV2 applied EDF to them (report 16). EDF was **not** executed on the hypothetical company.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Component verification

Method [M]: I cloned every repo into the scratchpad, read its README and LICENSE, and counted LOC per language with `scripts/loc.py` (non-blank lines, vendored paths excluded). I then built and ran tests with `scripts/runrepo.sh` and `scripts/pass2.sh`: `dotnet build <sln> -c Release` and then `dotnet test` or `dotnet run` per test project, with a 300 s cap each and `DOTNET_ROLL_FORWARD=Major` because only the .NET 10 runtime is installed. Node suites ran with `node --test` or `npm test`. Logs are in `dev/buildlogs/`. The full table is in `component-verification.csv`.

| Repo | LOC | Build | Tests [M] | Status for DAF use |
|---|---|---|---|---|
| praxis | 147k F# | pass | 1,074 pass / 0 fail before the 300 s cap (incomplete); Site 101/101 | process tooling, partially demonstrated |
| conditor | 34k | pass | 1,727 / 0 | install and upgrade tooling, demonstrated |
| ordo | 49k | pass | 806 pass; Sde.Core 95 fail (dist not built) | method and metrics; holds the only agent-cost trial |
| dokimos | 35k | pass | 597 / 0 | quality measurement, partial (no financial-invariant runner) |
| strata | 32k | pass* | 743 pass, 41 skip | PostgreSQL schema management only, partial |
| forma | 115k (JS/HTML/CSS) | pass | workflow 99/99; tokens 29/40 (dist not built); a11y Playwright not run | UI CSS, partial; no money input or app frame; WCAG evidence is a pilot |
| folio | 22k | n/a | 3/3, then browsers missing | print markup; no PDF engine or PDF/UA |
| limen | 93k | pass | 166 + runners pass | UI runtime, partial |
| fides | 6k | pass | 331 / 0 | GitHub-only IdP, so unfit for donors |
| arca | 19k | pass | 415 / 0 | records stored in GitHub repos, unfit for a ledger |
| aegis | 8k | pass | 349/349 alone; 2 timing failures under load | fault handling, not security |
| tutela | 3k | pass | 246/246 | security posture method; **no SAST or dependency scanning in any repo** |
| summa / signal / chrona | 46k / 56k / 39k | pass | 667 / 732 / 461 after `npm ci` | app pilots; the Summa ledger is planned only |
| causa | 33k | pass* | 350 pass; 131 blocked (credential, node_modules) | app pilot; **no LICENSE** |
| others (vigila, tekmerion, percepta, forma-studio, iter, vitium, project-administration, echelon-foundry) | 0.5–14k | pass | all pass except vitium 101/102 and Interop (needs service) | peripheral |
| echelon-registry, echelon-engineering-system | spec/docs | n/a | none / not run | described only; ees holds the rehearsal evidence |

\* Causa pins SDK 10.0.402 with `rollForward: disable`, and Strata pins 8.0.0. Both failed SDK resolution as shipped and built only after a roll-forward edit in the scratch clone. That is reproducibility friction.

**Capability classification for building and running a DAF servicer:**

| Capability | Status | Evidence |
|---|---|---|
| Automated requirements refinement | partially demonstrated: artefacts exist (Unbound RR-* refinements, Praxis manifests) but none have been validated by acceptance | baseline.jsonl status counts (106 adopted-provisional, 70 proposed, 32 unvalidated) |
| Autonomous implementation | **not demonstrated**: Rehearsal 4 passed 1 of 108 P0 requirements; Rehearsal 5 not run | echelon-engineering-system/docs/rehearsal-evidence.md:6-29 |
| Automated testing | demonstrated for Echelon's own code (~9.8k tests) | buildlogs |
| Continuous verification | demonstrated in CI (Praxis/Dokimos/Percepta gates) | .github/workflows |
| Agent-generated documentation | demonstrated (372k Markdown lines, mostly agent-authored); quality not independently assessed | loc.json |
| Automated code review | partially demonstrated: Dokimos and Ordo metrics; same-model review is not independent | dokimos, ordo |
| Automated security analysis | **described only**: Tutela is a posture model; there is no SAST, DAST or dependency-scanning workflow; a token leaked during Rehearsal 4 | tutela/README.md; rehearsal-evidence.md:28-29 |
| Automated deployment | partially demonstrated: package releases and static Pages only; no deployment of a stateful service with live data | workflows |
| Reusable UI components | partially demonstrated (Forma, Folio) | Unbound 07:44-56 |
| Reusable data access | absent for a ledger (Arca is GitHub-backed; Strata manages schema only) | Unbound 07:125 |
| Reusable financial/workflow capabilities | **absent** (no ledger, payments, grants or reconciliation code in any repo) | registry lists Summa ledger as planned only |
| Automated defect detection | partially demonstrated (Dokimos regressions, Vitium reporting) | buildlogs |
| Automated maintenance | partially demonstrated (Conditor/Praxis upgrade tooling); it causes churn of its own | conditor tests 1,727 |

## Observed throughput

Method [M]: I ran `git fetch --unshallow` on all 26 component repos and then `scripts/throughput.py`. It parses `git log --numstat`. "Code" means source extensions only, excluding Markdown and JSON. Commits are classified by author identity and by `Co-Authored-By`/`Claude-Session` trailers. Output: `throughput.csv`.

| Metric (26 Echelon repos) | Value [M] |
|---|---|
| Span | 2025-07-07 to 2026-11-25; **105 distinct commit days** (90 since 2026-07-20) |
| Commits | 9,045: agent-authored 4,210 (46.5%); human-authored with an agent trailer 191; human-authored with no agent signal 4,456 (includes 1,560 merges); bots 188 |
| Human author identities | **1** (the owner) |
| Distinct Claude Code sessions in trailers | 230 |
| Code lines added / deleted | 1,124,995 / 214,842; HEAD holds ~799k non-blank code lines and 372k Markdown lines |
| Approximate rate | ~8,600 net code lines per portfolio commit day [D: (1,124,995 − 214,842) / 105]; per repo 88–7,250 net lines per active day (median ~1,260) |
| Telemetry | 1,687 Praxis execution records; **3** carry token counts (Opus 5.5: 35–62 min wall clock, 72–94k output tokens, 20–28M cache-read tokens, about $6.7–$8.8 per work item [D at $4/$20/$0.20 per MTok; cache-write multipliers assumed]); **0** carry cost or human time |
| Controlled cost trial (ordo EX-SDE-2026-0001/0002) | 11 runs of one frozen feature, $12.00–$27.15 each; 5 verified; 6 void because of telemetry or session restarts; both agents' self-reported test results were wrong |
| Autonomous greenfield build (Rehearsal 4) | 296 of 420 minutes used; 1 of 108 P0 requirements passed; NOT ACCEPTED |
| AI-Engineering evaluation programme | "No model, agent, harness, stochastic run, token cost, or human-time baseline was measured" (05-experiment-registry.md:33) |

**Why this is weak evidence.**
1. LOC is output, not value. Much of it is tests, generated code, scaffolding and repeated Praxis installations.
2. The denominator is unknown: the owner's hours are not recorded anywhere. Commit days are not working days, and session wall clock includes idle time.
3. No repo is a regulated product in production with external users, so defect escape, rework and maintenance cost after acceptance are unobserved.
4. There is no comparator: the same scope has never been built conventionally or by another team.
5. Selection effects: greenfield, self-specified and self-accepted work with no external customer, auditor or bank integration.
6. Attribution is unclear. Commits marked "human, no agent signal" may still be agent-written, and agent-authored commits are steered and reviewed by the human.
7. The single public test of autonomous delivery against an independent verifier failed.

**What would make it strong:** on the DAF codebase, pre-register 3–5 capabilities with a frozen acceptance oracle. Log human minutes per task with a timer (not commit timestamps) and agent cost from the platform. Use an independent reviewer. Track escaped defects for 90 days after acceptance. Compare against a conventional estimate or a contractor quote for the same scope (see the measurement methodology section).

## Productivity sensitivities

**Conventional baseline:** 132 person-months (17,600 h) for the full MSP after the reuse credit [E]. This is a bottom-up decomposition by this agent. No public cost-per-function-point or developer-productivity study was read in this run, so the baseline is **labelled an assumption**, and validating it is an evidence gap. Rate: $120/h [D from CST-R03, O*NET/BLS].

Required total MSP cost (human + agent + $75k assurance + infrastructure) [D]:

| Effort case | 1x | 1.5x | 2x | 3x | 5x | 10x |
|---|---|---|---|---|---|---|
| Low (90 pm) | $1.68m / 12,000 h | $1.31m | $1.13m | $0.95m | $0.80m | $0.69m / 4,440 h |
| **Base (132 pm)** | **$2.43m / 17,600 h** | $1.89m | $1.62m | $1.35m | $1.14m | **$0.98m / 6,512 h** |
| High (216 pm) | $3.93m / 28,800 h | $3.05m | $2.61m | $2.17m | $1.81m | $1.55m / 10,656 h |

**Amdahl limit.** With 30% of effort incompressible [A], a nominal 10x becomes **2.7x effective**, and no multiple can exceed 3.3x. The incompressible part is product and financial-control decisions, review of agent output, bank and custodian coordination, manual assistive-technology testing, and security remediation verification. If that share were only 10%, 10x would become 5.3x. The incompressible share is the parameter most worth measuring, and it has never been measured.

**Evidence status of the multiples.**
- 1x–1.5x: plausible but unmeasured.
- 2x–3x: consistent with Echelon's raw output, but not with any measured accepted-capability rate.
- 5x–10x: contradicted by the only independent end-to-end trial (Rehearsal 4).

A sound planning range is 1.5x–3x nominal, with 1x as the downside. That puts the base MSP at **$1.35m–$1.89m**, with $2.43m downside. The prior study's S1 (1.5–2x) and S2 (≥2x) remain undemonstrated.

## Measurement methodology

Apply this to the next 3–5 Unbound capabilities. Candidates:
- LEDGER posting with append-only corrections (ACC-MDL-001/002);
- charity eligibility and OFAC screening (UNB-EXT-001, CNV-GRT-002);
- grant maker-checker and disbursement file (UNB-PAY-001);
- contribution acknowledgment (UNB-LS-001);
- statement rendering (CNV-EXP-001).

**Protocol.**
1. Freeze the requirement IDs and Given/When/Then acceptance before work starts, using Praxis manifest plus Dokimos evidence.
2. Have the independent oracle and test written by someone other than the implementing agent and human.
3. Get a conventional estimate for the same scope from an outside contractor quote or a second engineer, blind to the agent results.
4. Record human time with an explicit timer per activity category (spec, prompting, review, debugging, integration, approvals), not from commit timestamps.
5. Record agent cost from platform usage readings with start and close markers, as ordo did.
6. Follow up for 90 days after acceptance.

| Metric | Definition | How to capture | Threshold to replace conventional estimates |
|---|---|---|---|
| Human hours per accepted capability | timer hours from start to independent acceptance | timer log per Praxis work item | ≤ 0.5 × blind conventional estimate on ≥3 of 5 capabilities (supports ≥2x) |
| Agent compute per accepted capability | platform cost including void and retried runs | usage API markers | report only; decision-relevant if over 10% of human cost |
| Requirements-to-implementation cycle time | frozen acceptance to independent pass | Praxis telemetry events | ≤ 0.5 × conventional, with no skipped gates |
| Defect escape rate | defects found after acceptance per capability (90 days), severity-weighted | Vitium/issue tracker | ≤ conventional benchmark or ≤ 1 high-severity per 5 capabilities; **zero financial-misstatement defects** |
| Rework | share of accepted lines changed within 90 days for defects (not features) | git blame and churn (Ordo.Churn) | ≤ 20% |
| Maintenance effort | hours a month per live capability over 6–12 months | timer | ≤ 0.6 × the conventional 15–25%/yr rule |
| Human review overhead | review hours / total human hours | timer category | measured; if over 40%, the effective multiple is capped |
| Security remediation | findings from independent pen test and SAST per capability, and time to fix | external report | no critical or high open at release; fix time ≤ 2 weeks |
| Integration effort | hours spent with bank, custodian or processor, and calendar lead time | timer + log | report separately; never multiplied by a productivity factor |
| Lifecycle cost | build + 12-month maintenance + assurance per capability | sum | ≤ 0.6 × conventional over 3 years |

**Decision rule:** replace conventional estimates only if ≥3 of 5 capabilities meet the human-hours and defect thresholds with an independent reviewer, and the incompressible share is measured. Otherwise budget at 1x–1.5x.

## What Echelon can genuinely reduce vs transfer

**Development (conditional ranges, base MSP $2.43m at 1x):**

| Item | Effect | Range [D/E] | Condition |
|---|---|---|---|
| UI styling and print markup (Forma, Folio) | reduce | $0–$60k (0–4 person-months) | pin tagged releases; Unbound supplies money input, app frame and PDF engine; a11y still verified per surface |
| Schema management, fault handling, install and pinning tooling (Strata, Aegis, Conditor) | reduce | $0–$40k | PG16 constraint; commercial licence |
| Process and verification tooling (Praxis, Dokimos, Percepta) | reduce coordination effort; unmeasured | 0–10% of build | only if it lowers review and rework hours, which is unmeasured |
| Agent-written code and tests | reduce compressible labour | $0.5m–$1.4m (1.5x–10x on 70% of effort) | needs the measurement above; 5x–10x contradicted so far |
| Review of agent output, product and financial decisions, integrations, a11y and security verification | **not reduced** | about 30% of conventional effort ($0.6m–$0.75m) | — |
| External assurance (pen test, a11y audit, SOC) | **not reduced** | $75k + $35–$190k a year | — |
| Licence for PolyForm-NC components | **new cost or transfer** | unknown (no published terms) | CNV-GOV-009 blocks release 1 without it |
| Owner's or Echelon's own time | **transfer, not elimination** | must be charged at loaded cost | intercompany agreement |

**Operating:**
- Echelon supplies no runtime infrastructure, ledger, payments, identity for donors, or monitoring.
- Maintenance is floored at 1–2 engineering FTE once live, whatever the multiple.
- Echelon's fast churn (0.x and minor releases weekly) adds upgrade work and transfers integration risk to the DAF business.
- One human maintainer across 26 repos is a bus-factor risk that a regulated sponsor's diligence will flag.

**Net:** the credible saving against a conventional MSP build is **$0–$1.1m** (base $1.35m–$1.89m versus $2.43m). It depends on measurement. Shared Echelon resources must be charged. No saving yet applies to operating cost.

## Evidence gaps

1. **No human-time data** anywhere (owner hours, review minutes). This is the single largest gap.
2. **No accepted DAF capability has been built**, so the cost per accepted capability, defect escape and maintenance are unobserved.
3. **The conventional baseline is this agent's own decomposition.** It was not checked against function-point or industry productivity data, and it is not independent (same-model reasoning).
4. Only one controlled agent-cost trial exists: one mission, one codebase, 5 verified runs.
5. Only one autonomous end-to-end trial exists, and it failed. Rehearsal 5 has no evidence.
6. Incompressible-share and integration lead times (bank, custodian, processor onboarding) are not measured.
7. There are no published commercial licence terms for PolyForm-NC components, and Causa and echelon-engineering-system have no licence file.
8. The Praxis test suite did not finish inside the 5-minute time-box. Forma a11y, Folio print and Playwright suites were not run (browsers absent). These are the test layers most relevant to the WCAG claims.
9. The FSM peak-capital markdown and csv disagree. Unbound's $5m inherits neither consistently.
10. SOC 1/2 readiness for an AI-authored codebase: there is no auditor view on reliance over agent-made changes.
