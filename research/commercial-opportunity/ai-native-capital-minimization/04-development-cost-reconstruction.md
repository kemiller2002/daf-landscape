# 04: Development cost reconstruction

**Pass:** DEV (sections on the $5M origin, the $60k origin, scenarios and deferrable capabilities). **Data:**
- [`dev-scenarios.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/dev-scenarios.csv) (6 budgets × 6 multiples);
- [`deferrable-capabilities.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/deferrable-capabilities.csv) (24);
- model section 8 and [`development-scenarios-model.csv`](model/out/development-scenarios-model.csv).

**Integrator conclusions**
- **Unbound's $5M build has no derivation.**
  - It is labelled `assumption` in `parameters.json:509-516`.
  - Its cited source is a peak-capital output with no build line, and it entered through one agent commit (`5aae42a`).
  - The convergence vendor P&L and the previous study inherited it.
- **The previous study's $60k/month × 12 ($0.72M) was an integrator assumption**, deliberately narrow. It is **below** any safe minimum product found here. That is a correction to the previous study's minimum capital ($2.7-3.6M), which is understated (report 11).
- **A minimum servicing product (MSP) safe with live money costs about $1.1-2.4M** [E]:
  - $2.43M at 1x, $1.94M at 1.5x (the integrated base), $1.70M at 2x, $1.45M at 3x, $1.11M at 10x.
  - Bottom-up: 132 conventional person-months after a 4 person-month Echelon reuse credit, at $120/h.
  - 30% of the effort cannot be compressed.
- **No investment below about $1.0M is safe with live money** at any multiple.
  - $1.0M works only at 5x or more.
  - $1.8M works at 1.5x or more.
  - $5M covers the full conventional scope at about 1.3x or more.
- Even a funded MSP is only "conditional". It still needs:
  - a bank or processor agreement and custodian file access;
  - a counsel opinion on money transmission;
  - a SOC observation period;
  - a second maintainer;
  - a commercial licence for the PolyForm-NC components (CNV-GOV-009).
- **Unbound defines no minimum product:** 1,185 of its 1,208 normative items (98%) are initial scope. Requirements candidate RC-AN-010 and report 17 propose a scope gate.
- **Deferral moves cost rather than removing it.** Of 24 deferrable capabilities, several push labour back to operations or sponsors while deferred: manual custodian import, scripted migration, manual SOC evidence. The integrated sequences add a deferred-scope build tranche after the second go-live (ADV2-008).

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Summary (DEV group)

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

## $5M origin

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

## $60k origin

`daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/Strategies.fs:7-12`: *"Product build outside the core team (contract engineers, design, security review)... Base $60k/month for 12 months ($0.72M); Unbound's own model assumes $3-15M... so the base deliberately assumes a narrow servicing-only scope. [A]"*. The `costlyBuild` sensitivity multiplies it by 2.5 over 18 months, giving $1.8m (`Strategies.fs:134-137`).

**This was an integrator assumption.** It has no hours, rate, scope list, requirement count or quote behind it, and it was set to look small next to Unbound's equally unsupported $5m. $60k a month buys about 500 contractor hours a month [D: 60,000 / ($120 × 1.3 contractor premium, parameters.json:518-525) ≈ 385 h; or 500 h at $120]. Over 12 months that is about 4,600–6,000 hours, against the 14,900 hours this model estimates for the mandatory MSP at 1x. **$0.72m delivers a safe MSP only if a nominal ≥10x multiple holds and the effort is at the low estimate (90 person-months).** At the base estimate, $0.72m covers about 50–60% of the mandatory set even at 5–10x. The $1.8m `costlyBuild` variant is close to this model's base-effort cost at 1.5x ($1.89m).

## Scenarios

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

## Deferrable capabilities

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
