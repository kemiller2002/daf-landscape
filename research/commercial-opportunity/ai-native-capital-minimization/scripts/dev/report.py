import json, sys
S=[]
def sec(t,m): S.append({"section":t,"markdown":m.strip()})
sec("Summary (DEV group)", """
**Bottom line.** The Echelon portfolio is real, buildable, heavily tested software produced quickly by one human working with coding agents. But none of it is a DAF servicing product, and none of it has been measured in a way that supports a development cost lower than a conventional estimate. Echelon's measured output shows how much the agents wrote. It does not show the cost of an accepted capability. The software budget for a minimum servicing product (MSP) is about **$1.1m–$2.4m at the base effort estimate [D]**. The range runs from 5x to 1x nominal agent productivity on the compressible work. Neither Unbound's $5m nor the previous study's $0.72m has any derivation behind it. Below about **$1.0m**, no productivity multiple delivers a product that is safe to run with live money. Above that line, maintenance is set mostly by staffing, not by effort: once live, it costs about **$0.22m–$0.47m a year [D/A]** at any multiple.

| Finding | Value | Label |
|---|---|---|
| Echelon repos that built (scratch clones; 2 needed a scratch-only `global.json` roll-forward) | 26 of 26 attempted (24 with tests) | [M] |
| Test cases passed in the sweep | ~9,768; every failure traced to the environment or to timing | [M] |
| Licence | 21 of 26 PolyForm Noncommercial; Unbound clause CNV-GOV-009 bars these from release 1 without a commercial licence | [M]/[S] |
| Autonomous end-to-end build trial | Rehearsal 4: **1 of 108** P0 requirements passed; NOT ACCEPTED | [S] |
| Controlled agent-cost trial | $12–$27 of compute per feature mission; both agents' self-reports of test results were wrong | [S] |
| Human-time measurement anywhere | **none** | [S] |
| Unbound $5m build cost | `assumption`. The cited source is a peak-capital output, not a build estimate | [S] |
| Previous study $60k/month | integrator assumption with no decomposition | [S] |
| Unbound initial scope | 1,185 of 1,208 normative items (98%); no MSP is defined | [M] |
""")
sec("Component verification", """
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

\\* Causa pins SDK 10.0.402 with `rollForward: disable`, and Strata pins 8.0.0. Both failed SDK resolution as shipped and built only after a roll-forward edit in the scratch clone. That is reproducibility friction.

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
""")
sec("Observed throughput", """
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
""")
sec("$5M origin", """
**Trace [S]:**
1. `unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json:509-516` sets `build_capex`: value 5,000,000, low 3m, high 15m, label "A". Its source field reads *"assumption; FSM:150-154 peak capital $2.5-35.8m by path [S model output]"*.
2. FSM = `daf-landscape/research/ai-native-daf-enterprise/09-financial-models/financial-and-staffing-models.md:146-154`. That table gives the **peak capital need** of five 5-year ramp paths. These are cumulative operating losses: Engineering FTE (4–10, log scale) sit inside opex, and there is **no platform build line** (`Economics.fs:163`, `352-383`). The markdown values ($2.5m, $12.8m, $6.4m, $35.8m, $15.2m) also no longer match the committed `outputs/peak-capital.csv` ($2.95m, $14.8m, $7.4m, $38.3m, $17.7m).
3. The parameter was introduced in a single Claude-authored commit (`5aae42a`, 2026-11-24, "simplification mission: economics model") with no derivation [M `git log -S`].
4. It is then inherited by `simplification-economics/06-ECONOMIC-TARGET-ENGINEERING.md:92`, by `convergence/.../model/enterprise_economics.py:122-123,392` (5-year amortisation, $1.0m a year), by `08-ADVERSARIAL-ENTERPRISE-REVIEW.md:69` (ADV-B-002), and by the previous study's A-ECH-005 and A-ADV-003.

**Classification of the basis:**

| Basis type | Present? |
|---|---|
| Implementation experience | no |
| Engineering hours | no |
| Productivity | no |
| Compensation | no (the $165k loaded rate exists elsewhere in parameters.json but is not used) |
| Contract engineering | no |
| Requirement counts | no |
| Comparables | no |
| **Unsupported** | **yes**. It is an analyst assumption, anchored loosely to a capital figure that measures something else. |

Bottom-up context [E]: the MSP decomposition here comes to 132 conventional person-months after the reuse credit, about $2.1m of loaded labour at $120/h. By that measure $5m is plausible for MSP plus a substantial part of the broader 1,185-item Unbound initial scope. It is not a derived number for either.
""")
sec("$60k origin", """
`daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/Strategies.fs:7-12`: *"Product build outside the core team (contract engineers, design, security review)... Base $60k/month for 12 months ($0.72M); Unbound's own model assumes $3-15M... so the base deliberately assumes a narrow servicing-only scope. [A]"*. The `costlyBuild` sensitivity multiplies it by 2.5 over 18 months, giving $1.8m (`Strategies.fs:134-137`).

**This was an integrator assumption.** It has no hours, rate, scope list, requirement count or quote behind it, and it was set to look small next to Unbound's equally unsupported $5m. $60k a month buys about 500 contractor hours a month [D: 60,000 / ($120 × 1.3 contractor premium, parameters.json:518-525) ≈ 385 h; or 500 h at $120]. Over 12 months that is about 4,600–6,000 hours, against the 14,900 hours this model estimates for the mandatory MSP at 1x. **$0.72m delivers a safe MSP only if a nominal ≥10x multiple holds and the effort is at the low estimate (90 person-months).** At the base estimate, $0.72m covers about 50–60% of the mandatory set even at 5–10x. The $1.8m `costlyBuild` variant is close to this model's base-effort cost at 1.5x ($1.89m).
""")
sec("Scenarios", """
**Model** (`scripts/scenarios.py`, results in `dev-scenarios.csv`, 36 rows):
- MSP = 16 capability groups totalling 136 conventional person-months [E], less a 4 person-month Echelon reuse credit [E].
- 13 groups (116 person-months) are mandatory before live money.
- Human hours = conventional hours × (0.7/m + 0.3) [A], at $120/h [D].
- Agent compute = $20 per mission × 3 rework factor, one mission per 16 compressible hours [E, from measured $12–$27].
- Infrastructure $3k a month for at least 6 months [A]. External assurance of $75k (pen test, a11y audit, SOC readiness, sandboxes, tooling) is bought only once the mandatory set is complete [S/C].
- Groups are delivered greedily in dependency order.

| Budget | At 1x | At 2x | At 5x | At 10x | Safe with live money? |
|---|---|---|---|---|---|
| $100k | nothing beyond a spike | ARCH (5% of mandatory) | ARCH | ARCH + IAM (11%) | **No** at any multiple |
| $250k | ARCH + IAM (11%) | 11% | + LEDGER (27%) | 27% | **No** |
| $500k | 11% | through CHARDATA (38%) | through GRANTS (50%) | through NAVMIN (61%) | **No**: no statements, console, security controls or assurance |
| $1.0m | 50% | 73% | **100%, $0.98m** | 100%, $0.98m | **Conditional** only at ≥5x, and only at base effort |
| $1.8m | 86% (SECCTL and PRODUCT missing) | 100%, $1.62m | 100%, $1.14m | 100% | **Conditional** at ≥1.5x |
| $5.0m | 100%, $2.43m, about $2.6m unspent | 100% | 100% | 100% | **Conditional**; covers the high-effort case at about 1.3x |

The costs are split into human labour, agent compute and infrastructure/assurance in the CSV. **Agent compute is at most $46k (under 5%) in every scenario**, so the build cost is human hours.

"Conditional" means the software scope is complete but live operation still needs things money for software cannot buy:
- an executed bank or processor agreement and custodian file access;
- counsel opinions (money transmission, CNV-LEG-002);
- a SOC 1/SOC 2 observation period (Type II needs 6–12 months of operation; first sponsors may accept Type I plus a bridge letter) [A];
- a second qualified maintainer;
- a commercial licence for PolyForm-NC components (CNV-GOV-009), or replacement code.

Integrations per scenario:
- Banks and payments: an ACH/positive-pay file or API through the sponsor's bank, and a check-print vendor.
- Custodian: statement or CSV import only, because NAVFULL is deferred.
- IRS and charity data: public EO BMF, Pub 78 and auto-revocation files, plus OFAC SDN. These are cheap to acquire but need fuzzy matching; Unbound's replay missed 12 of 100 perturbed names.

None of these integrations exist in Echelon.

Commercial limitations at MSP: one sponsor, fixed-amount domestic grants only, cash and simple securities, manual NAV import, no API or widgets, no card contributions.

Maintenance: 12–25% of build effort a year [A], with a floor of 1–2 engineering FTE once live [A]. That gives $0.22m–$0.47m a year plus pen test and infrastructure. SOC audit fees are excluded as operating cost. **The floor, not productivity, sets maintenance.**
""")
sec("Productivity sensitivities", """
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
""")
sec("Deferrable capabilities", """
`deferrable-capabilities.csv` has 24 rows: 17 deferrable or partly deferrable, 7 explicitly not deferrable.
- **Deferrable with low control risk:** card contributions (CNV-PAY-008), donor-covered fees (CNV-PAY-006), UBIT accrual (CNV-FIN-010, with UBTI refusal kept), foreign and intermediary grants (CNV-GRT-007/008, hard-blocked), call recording and SMS (CNV-PLT-002), percentage grants (UNB-GFUND-*), public APIs and widgets (UNB-API-*, WG-*), the AI-native layer (AIN-*), and the knowledge graph beyond IRS/OFAC (UNB-KNOW-*).
- **Deferrable only under conditions, with work transferred rather than eliminated:**
  - Full custodian feeds and NAV engine: manual import, with labour moving to ops.
  - Multi-tenant white-label: single sponsor, but immutable tenant ID from day 1.
  - Migration tooling: scripted supervised load.
  - Continuous control monitoring: manual SOC evidence.
  - Delegated approvals: sponsor staff approve, so the labour sits with the sponsor.
- **Not deferrable:**
  - the append-only ledger;
  - MFA identity with scoped roles (bought IdP; Fides is unfit);
  - eligibility and OFAC screening before disbursement;
  - maker-checker and bank reconciliation;
  - §170(f)(8) acknowledgments;
  - WCAG 2.2 AA on donor surfaces;
  - an independent pen test and SOC readiness before live money.

Deferring scope is not eliminating cost: each deferral either moves labour to a person or comes back later at retrofit cost (tenancy especially).
""")
sec("Measurement methodology", """
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
""")
sec("What Echelon can genuinely reduce vs transfer", """
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
""")
sec("Evidence gaps", """
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
""")
with open(sys.argv[1],'w') as f:
    for s in S: f.write(json.dumps(s)+"\n")
print(len(S))
