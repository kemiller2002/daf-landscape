# Mission 2026-11-14: baseline inventory, coverage accounting and execution plan

**Date:** 2026-11-14 (Saturday). **Deadline:** Sunday 2026-11-15, 11:00 PM Eastern.
**Repository:** `kemiller2002/daf-landscape`. **Working branch:** `claude/daf-landscape-research-tdxdiq` (session-authorized branch; merged to `main` through a pull request, never force-pushed).
**Scope of this file:** what existed before this mission, how coverage is measured, and how the next research task is chosen. It does not restate earlier findings; it points to them.

## 1. Repository state at mission start (verified by `git` and `scripts/mission_inventory.py`)

| Item | Value at start | How measured |
|---|---|---|
| Commits on `main` | 50 (head `8f376fd`, "Model DAF exception unit economics…") | `git rev-list --count main` |
| Markdown research documents (research/, docs/, README) | 81 documents, ~105,800 words | `scripts/mission_inventory.py` |
| Datasets (data/*.csv, *.json) | 60 files, 1,119 data rows | same |
| Unique URLs cited anywhere in the repository | 431 URLs across 147 domains | same (a cited URL is a source *referenced*, not proof it was read in full) |
| Organizations (from a fixed 66-name list) mentioned in at least one file | 60 | same (a mention is not an investigation) |
| Pull requests | 19 total; #1 (initial foundation) and #16 (F# decision-intelligence validator) still **open**; 17 merged | GitHub API |
| Execution register (research-execution-register-2026-11-12.md) | 56 items: 51 marked BACKLOG, 5 FOUNDATION | parsed from file |

**Register drift:** several register items marked BACKLOG were partly executed in the batch 1A–3B files of 2026-11-12, but the register's status labels were never updated. This mission doesn't rewrite that register. Instead it adds a new coverage matrix and priority queue (below) that supersede it as the working queue. The original register stays as history.

Raw inventory: [`data/mission-2026-11-14/repo-inventory-baseline.json`](../../data/mission-2026-11-14/repo-inventory-baseline.json).

## 2. What is completed, incomplete and unverified

### Completed to a documented public-evidence standard (still not independently validated)
- **RCF → Ren audited payments 2020–2024** ($7.51m in 2020 rising to $19.23m in FY2024; the fee basis is 95% of fundholder fees in 2020–22 and 98% in 2023–24). Source: RCF audited statements, `data/rcf-ren-audited-admin-payments-2020-2024.csv`.
- **Edward Jones Charitable Gift Fund:** RCF is the legal sponsor and the donor portal is a branded DonorFirstX site. The Ren role is described by RCF as "technology and operational support". See `edward-jones-ren-*.md`.
- **Foundation Source acquisitions** of Vennfi (2024) and TIFIN's Giving Place (2025). **Charityvest** remains an independent sponsor. **TIAA's Sept 2026 DAF** is sponsored by Charityvest and powered by Foundation Source.
- **DAFRC revised FY2024 baseline:** 3.59m accounts, $327.87bn assets, $90.57bn contributed, $64.60bn granted.
- **Affiliated-provider fee tracing** for Fidelity Charitable and Vanguard Charitable (batch 1C/1D).

### Incomplete (foundation exists, decisive evidence missing)
- Ren's total revenue, customer concentration and contract terms with institutional channels other than RCF.
- Technology and administration providers for Goldman Sachs and Morgan Stanley GIFT, and for the Edward Jones *private* DAF.
- Actual grant turnaround times and exception rates at any sponsor. Every operational metric in the repo is either self-reported or a scenario.
- Retention effect of DAFs on adviser households (study design only).
- Vendor tests: **none executed** (vendor-test-execution-2026-11-11.md).

### Unverified or contradictory
- Ren/AEF SOC 2 type: AEF's July 2025 wording says Type II, while its April 2026 wording says Type I.
- The Stellar/iPhi "175 clients" claim is still only a lead.
- AI capability claims (TIFIN Give Tax Intelligence and others) were announced, but delivery has not been assessed.

## 3. Coverage matrix (new)

`scripts/mission_coverage.py` produces [`coverage-matrix-entities.csv`](../../data/mission-2026-11-14/coverage-matrix-entities.csv). It covers 29 entities against a **12-item minimum evidence checklist**: legal role, financials, fees, technology/admin provider, custody/investment, distribution, grant workflow, assurance, ownership/funding, dated timeline, AI claims, and operating evidence.

Statuses use the mission's eight-state scale: Not investigated, Discovery started, Evidence collected, Partially validated, Independently corroborated, Contradictory evidence, Insufficient public information, and Research completed to current evidence standard. The rule is **"Independently corroborated" can only be set by the separate validation register**, never by the original researcher.

Baseline result (before this mission's agents report):

| Status | Cells | Share |
|---|---|---|
| Not investigated | 156 | 44.8% |
| Discovery started | 81 | 23.3% |
| Evidence collected | 86 | 24.7% |
| Partially validated | 12 | 3.4% |
| Contradictory evidence | 2 | 0.6% |
| Insufficient public information | 11 | 3.2% |
| Independently corroborated / Completed | 0 | 0% |

**55% of entity-checklist cells have any investigation; only 3.4% are partially validated or better.** Fourteen of the 29 entities have a majority of cells not investigated. They are concentrated in wealth channels other than Edward Jones, faith and community sponsors, and infrastructure (Givinga, DAF Direct, Candid).

**About the denominator:** the known universe is about 1,500 legal sponsors (DAFRC), plus vendors and channels. The matrix is a *purposive* sample of the most strategically relevant entities, so these percentages measure depth on that sample. They don't measure coverage of the industry.

### Topic dimensions (coverage outside the company axis)

| Dimension | Strong existing coverage | Thin or absent before this mission |
|---|---|---|
| Market segment | National sponsors, white-label vendors, wealth channels | Community foundations, faith sponsors, pass-through processors |
| Technology capability | Grant tracking, payments, SOC 2, DNS reconnaissance | Data portability *tested*, APIs actually exercised |
| AI application | Grant vetting benchmark design, tax-opportunity claims | AI economics per process, AI adoption evidence, AI failure modes |
| Grant workflow stage | Intake, eligibility, approval, payment, reconciliation | Exception frequency, non-standard grantee share |
| Financial model | Admin fee scenarios, affiliated investment flows, RCF→Ren | Vendor P&L, challenger unit economics, entrant capital needs |
| Regulatory jurisdiction | Federal tax (2026 personas) | Status of 2023 proposed regs, state laws, adviser regulation |
| Customer type | Donors, advisers, sponsors | Nonprofits as payers, community foundations as buyers |
| Evidence quality | Explicit labels throughout | No independent validation register before this mission |

## 4. Prioritization method

`scripts/mission_prioritize.py` ranks [`research-priority-inputs.csv`](../../data/mission-2026-11-14/research-priority-inputs.csv) by expected information value:

`eiv = importance × P(changes a conclusion) × evidence gap × commercial impact × source availability ÷ effort`

Two modifiers apply. Open dependencies multiply the score by 0.6, and questions covering a segment whose coverage is mostly "Not investigated" get a ×1.25 breadth bonus, so that depth does not crowd out breadth. Every input is a recorded judgement that a reviewer can dispute line by line. The ranked output is [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

## 5. Execution plan for this mission

| Wave | Workstream | Output (research/mission-2026-11-14/) | Directive section |
|---|---|---|---|
| 1 | AI economics + replacement analysis; AI governance and failure modes | `ai-economics-replacement-analysis.md`, `ai-governance-failure-modes.md` | 3, 6 |
| 1 | AI-native entrant simulation | `ai-native-entrant-simulation.md` | 4 |
| 1 | Vendor dependency graph and concentration | `vendor-dependency-concentration.md` | 5 |
| 1 | Industry incentives (Clarity/EDF) | `industry-incentives-structural-analysis.md` | 7 |
| 1 | Company histories, announced vs delivered | `competitive-history-timelines.md` | 8 |
| 1 | Quantitative datasets + reproducible script | `quantitative-datasets-and-data-dictionary.md` | 10 |
| 1b | Regulation, processor share, vendor market share, portability | `regulation-market-structure-portability.md` | 11 (top-ranked open questions) |
| 1b | Breadth: community, faith, infrastructure, emerging AI entrants | `breadth-community-faith-infrastructure-emerging.md` | 2, 13 |
| 2 | Independent validation and red team (separate agents that are **not** given the researchers' conclusions) | `validation-register.csv`, `red-team-review.md` | 9 |
| 3 | Strategic synthesis A–G and consolidated report | `strategic-synthesis.md`, `COMPREHENSIVE-REPORT.md` | 12 |
| 3 | Final status report | `FINAL-STATUS.md` | 13 |

The persistent backlog is the priority queue CSV. Findings are deduplicated against existing files: each agent was told which prior files to read and not repeat.
