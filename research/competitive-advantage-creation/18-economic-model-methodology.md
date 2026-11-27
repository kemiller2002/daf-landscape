# 18 - Economic model methodology

Status: research (2026-11-26; revision 3 after the round-2 review, see section 9; revision 2 retained beside it). Agent MOD. Describes the F# model in [model/](model/README.md) that produces every number in reports 14, 15, 16 and 19, and records the corrections it makes to earlier figures. The model is a research tool, not product code. Claims P3-CLM-MOD001..MOD005, P3-CLM-MOD008; assumptions P3-ASM-MOD001..MOD012; evidence gaps P3-GAP-MOD001..MOD006. Generated register rows: P3-CAP-MOD001..MOD019 and P3-SEQ-MOD001..MOD009.

## 1. Structure and conventions

**Functional core, I/O shell.** All models are pure F# functions over immutable records; `Program.fs` alone reads and writes files. Every input row cites assumption, sequence or source IDs, and `validate` fails if a cited ID is not in a register. Ranges are validated on load (low <= base <= high, finite, non-negative unless allowed); invalid assumptions are rejected, not clamped.

**Cases.** Each parameter names its adverse end. The favourable case takes every favourable end, the adverse case every adverse end; these are joint bounds, not likely outcomes. One-at-a-time tornadoes and the Monte Carlo ([19](19-sensitivity-and-stress-analysis.md)) give the spread between them.

**Cash and fully loaded.** Cash is money leaving or entering Echelon Foundry's account. Fully loaded adds three non-cash items: development at market value instead of its cash cost, the founder's time at market instead of the founder's cash draw (P3-ASM-AB018), and a capital charge on the running cash deficit (P3-ASM-AB028). By construction, fully loaded = cash + non-cash for every category and month (tested). The founder's time is counted even when cash is zero.

**Entities.** Every stream, allocation and cost belongs to one of the five economic entities of echelon-organization-administration `strategy/daf-entry/02` (E1 Echelon Foundry, E2 Unbound, E3 customer programme, E4 servicing organization, E5 shared components). Programme economics (E3) are reported separately from vendor economics. Combining entities needs an explicit justification (`SharedInfra.combineEntities`).

**Revenue and channel.** Revenue is gross customer billing; for licensing streams it is accounts per customer x licence price, so revenue and the number of customers of that size (FY2024 sponsor panel, SRC-013) are linked. A partner share is deducted before the vendor recognizes revenue, so a channel share is never also a variable cost; variable cost is charged on gross volume per account (P3-ASM-MOD003) and does not fall when the share rises. Working capital is the receivable created by billing (P3-ASM-MOD002) or partner remittance (P3-ASM-MOD044) in arrears, plus an incident-retention reserve at the first go-live (P3-ASM-MOD039).

**Contingency and tax.** Contingency (P3-ASM-AB027) is applied on one base in every model: all Echelon cash cost except variable cost, the founder draw and wind-down. Income tax (P3-ASM-MOD048) is charged on cumulative pre-tax cash above its previous high-water mark (full loss carry-forward); SaaS sales tax is a pass-through and founder payroll tax sits inside the founder draw.

**Founder time.** During development months the share of founder time that is build work (P3-ASM-MOD037) is already inside development at market and is not charged again.

**Savings.** Savings are sequential residuals (P3-DEC-HI001): each step removes minutes from what the previous step left, transferred work is a cost to its recipient at an efficiency multiplier and never a saving, and automated and AI-accelerated work keep a residual cost (P3-ASM-MOD007, P3-ASM-MOD008). Claims from different models on the same cost base are combined sequentially (`Events.combineSequential`), never summed (P3-CLM-MOD008).

## 2. The eight models

| # | Model | Module | Inputs (agent) | Reproduces |
|---|---|---|---|---|
| 1 | Capital by Unbound state S1-S7, cash and fully loaded, by category; to first referenceable invoice and to self-sufficiency | `Capital`, `Cashflow` | `capital-states.csv` (AB) | AB's first-invoice figures for every state exactly |
| 2 | Event-level operating cost by work category | `Events` | `event-work.csv` (HI) | HI's category totals |
| 3 | Charity registry run cost by monitoring mode; marginal sponsor | `Registry` | `registry-components.csv` (HI) | HI's M3 and M5 base totals within a few dollars of rounding |
| 4 | Direct versus partner acquisition; break-even partner share | `Channel` | `parameters.csv` (FGJ) | FGJ's base present value and break-even share |
| 5 | Licence and migration revenue; minimum viable programme | `Licensing` | `mvp-grid.csv` (CD) | CD's 243-row grid |
| 6 | Shared infrastructure allocation by an explicit rule | `SharedInfra` | `shared-infra-*.csv` (AB, MOD) | Totals conserved under every rule |
| 7 | Incumbent response on licensing break-even | `Response` | `response-scenarios.csv` (EK) | EK's MD-6 break-even accounts |
| 8 | Commercial sequences, funding variants, kill rule | `Sequences`, `Cashflow` | `sequence-*.csv` (AB, CD, FGJ, MOD) | - |

The monthly engine (`Cashflow.flows`) is shared by models 1 and 8: customers sign at a rate after the first-signing month, go live after a lag, churn monthly, and pay recurring revenue; costs are development (spread over its months), one-time items (at the start or a set number of months before the first signing), pre-revenue and live run, founder draw, customer acquisition and implementation (first customer and later customers priced separately), and contingency on development, one-time and pre-revenue cash (P3-ASM-AB027).

## 3. Reuse of the Phase II model

The Phase II model in `../competitive-displacement/model/` is untouched; its `check` and `validate` still pass. `Csv.fs` was copied; `Sampling.fs` was adapted (same generator, triangular inverse CDF, nearest-rank percentile and seed; correlation applied per group instead of across all parameters). `Phase2Check.fs` ports `Routes.flows` and is tested to reproduce Phase II's ER-7 base capital to the cent, so the double-count corrections below are computed on Phase II's own arithmetic.

## 4. Double counts and corrections

### 4.1 Phase II ER-7 (agent AB's questions, report 03 section 3)

<!-- model-output: tables/phase2-double-count.md -->
| Route | Variant | Build-phase burn factor | Variable share | Capital (deepest deficit) |
|---|---|---|---|---|
| ER-4 | Phase II as modelled | 1.00 | 0.15 | $7.20M |
| ER-4 | build-phase burn at P3-ASM-MOD005 base | 0.40 | 0.15 | $5.74M |
| ER-7 | Phase II as modelled | 1.00 | 0.30 | $5.66M |
| ER-7 | build-phase burn at P3-ASM-MOD005 base | 0.40 | 0.30 | $4.67M |
| ER-7 | variable share = direct per-account cost (corrected) | 1.00 | 0.21 | $5.46M |
| ER-7 | variable share = direct share (AB alternative) | 1.00 | 0.15 | $5.33M |
| ER-7 | both corrections | 0.40 | 0.21 | $4.47M |
<!-- /model-output -->

1. **Full burn during build months: a real double count (P3-CLM-MOD002).** `Routes.fs` adds `Build / buildMonths` to the full monthly burn in every build month. The burn comes from MD-6 fixed cost, whose basis is "Platform 0.7-1.8M + CEO/CTO + ...": the platform team that would perform the build. At P3-ASM-MOD005's 40% build-phase run, ER-7 base capital falls by about a million dollars, matching AB's estimate. ER-4 has the same structure.
2. **Channel share and the 0.30 variable share: a partial double count (P3-CLM-MOD003).** ER-7's revenue per customer is documented as already net of a 30% channel share (entry-routes.csv basis), and its variable share is applied to that net revenue. Nothing in the inputs documents a partner-specific variable cost; the basis says the partner "sells and supports". Applying 0.30 to net revenue therefore raises the vendor's variable cost per account above the direct route's (0.15 of gross) although the partner carries first-line support. The defensible correction keeps the direct route's cost per account, a share of 0.15 / (1 - 0.30) of net revenue; AB's alternative (0.15 of net) treats the whole difference as duplication and is the lower bound. The corrected Phase II capital is in the table; the Phase III engine uses per-account variable cost throughout.
3. **G0-G1 plus ER-7 overlap and G1 omitting the build (AB items 3 and 4).** Not a code issue: they concern how Phase II report 15 summed separate simulations. The Phase III sequences start from a stated state and never add a separate gate budget to a simulation that already contains it.

### 4.2 Agent AB's Phase III scripts

- **Later-customer implementation omitted (P3-CLM-MOD005).** `data/evidence/AB/staged.py` charges implementation only in the first customer's one-time lump; customers after the first need AB's own S6 range (P3-ASM-AB020). The corrected variant adds it.
- **Contingency on the run.** The same script multiplies every month's run by (1 + contingency), while AB's first-invoice method applies contingency once to a subtotal that includes the founder draw. Revision 2 uses one base everywhere: all Echelon cash cost including the live run, excluding variable cost, the founder draw and wind-down (REV2003).
- **Working capital.** AB's one-time working-capital line is replaced by the receivable the engine produces from billing in arrears, so working capital is not counted twice.

### 4.3 GAP-HI010: the charity registry and enterprise totals

Phase II mode fixed costs already include registry engineering (PR #87 layer B: platform engineering team and charity-data subscriptions), and EV-E08 already prices vetting labour, so registry cost is never added to a Phase II mode. Agent AB's lean licensor run includes no registry, so the registry's labour and the unabsorbed share of its engineering and counsel are added to it (P3-CLM-MOD004, P3-ASM-MOD010). Trace in [15](15-shared-infrastructure-economics.md) section 2.

### 4.4 Event savings across models

<!-- model-output: tables/events-double-count.md -->
| Claim on EV-E08 vetting labour (10k-account sponsor, base) | Saving if applied sequentially |
|---|---|
| event model EV-E08 removal (HI decomposition) | $677k |
| registry change-driven monitoring (CLM-005, 1 - 1/3) | $33k |
| **Sequential total** | $710k |
| Naive sum of the two claims | $1.16M |
<!-- /model-output -->

The event model and the registry model each claim savings on the same vetting labour. Summed, the claims exceed the labour itself; sequentially, they cannot (P3-CLM-MOD008).

Event categories and the sequential waterfall (agent HI's decomposition, per account-year):

<!-- model-output: tables/events-categories.md -->
| Scenario | Conventional min | Eliminated | Automated | Accelerated | To customer | To partner | Mandatory | Other residual | System cost $/acct-yr | Conventional $/acct-yr |
|---|---|---|---|---|---|---|---|---|---|---|
| opt | 183.3 | 47.0 | 112.3 | 5.3 | 2.0 | 2.7 | 9.1 | 4.9 | $31 | $190 |
| base | 183.3 | 36.9 | 82.2 | 9.3 | 1.7 | 7.3 | 28.3 | 17.7 | $118 | $267 |
| pess | 183.3 | 24.5 | 29.4 | 15.4 | 1.2 | 15.3 | 59.2 | 38.4 | $303 | $367 |
<!-- /model-output -->

<!-- model-output: tables/events-waterfall.md -->
| Step (base, sequential) | Minutes before | Removed | After | Residual cost created $ | System saving $ |
|---|---|---|---|---|---|
| eliminated | 183.3 | 36.9 | 146.5 | $0 | $54 |
| automated | 146.5 | 82.2 | 64.2 | $30 | $90 |
| accelerated (AI) | 64.2 | 9.3 | 54.9 | $3 | $11 |
| transferred to customer | 54.9 | 1.7 | 53.3 | $3 | -$1 |
| transferred to partner | 53.3 | 7.3 | 46.0 | $15 | -$4 |
<!-- /model-output -->

## 5. Kill rule and funding variants

The kill rule, the operational definition of the cost-center month (OD-P3-03, OD-P3-04; P3-ASM-MOD017) and the Transitus exemption (OD-P3-02) are specified in [14](14-commercial-sequencing.md) section 7 and implemented in `Sequences.killDecision`, `Sequences.namedInTime`, `Sequences.pilotMonth`, `Sequences.derivedCostCenter` and the `KillExempt` stream flag. The pilot is one whole live Unbound customer. A paused stream stops cost and revenue after the pause month, pays a wind-down if any customer has signed (P3-ASM-MOD038), and writes off receivables (conservative). In the Monte Carlo, partner-delivered sequences also face a partner termination hazard (P3-ASM-FGJ016). Funding variants are transformations of the streams (`Sequences.applyFunding`); the externally funded variant changes only the raise cost and the rate of the capital charge.

## 6. Reproducibility and tests

- `run` writes `data/model-outputs/` (CSV files, `results.md`, and one Markdown table per file under `tables/`); `check` regenerates everything and compares byte for byte.
- Reports quote tables between `<!-- model-output: tables/NAME.md -->` markers; `quote` refreshes them and `validate` fails on any drift, so report tables are never hand-typed.
- `fragments` copies the generated P3-CAP-MOD and P3-SEQ-MOD rows into `data/fragments/MOD/`; `validate` fails if they differ from the model.
- `merge` builds `data/registers/` from all fragments, including `adversarial-challenges.csv`: exact REGISTERS.md headers, width checks, unique IDs, rows sorted by ID (ordinal), header-only files where no fragment exists; disposition overlay files (`adversarial-challenges-dispositions.csv`) are applied in agent order, joining rationales and rejecting conflicting dispositions; the result is independent of fragment order (tested). `validate` accepts four-digit suffixes (P3-CHL-REV1001) and requires dispositions once `require_dispositions` is set in `settings.csv`.
- Tests (xUnit, `tests/CompetitiveAdvantageCreation.Tests`) cover accounting identities, category sums, cash versus economic cost, sequential savings, transferred versus eliminated work, invalid assumptions, zero customers and full partner share, extreme scenarios, the kill rule and the Transitus exemption, entity attribution and allocation conservation, the GAP-HI010 rule, the Phase II and agent reproductions, output and sampling determinism, merge determinism and error handling, and validator detection of bad IDs, vocabularies, references, links, decision status and quoted-table drift.

## 7. Limits

- Every input is an assumption, an inference from public prices or a Phase II parameter; nothing is measured. The decisive inputs (revenue per customer, named-partner timing, conversion from narrow tools) have no evidence (P3-GAP-MOD002, P3-GAP-MOD003).
- Customers are fractional (signing rates), as in Phase II; results for one or two customers are expected values, not lumpy outcomes.
- The Monte Carlo draws each range independently except inside two correlation groups ([19](19-sensitivity-and-stress-analysis.md)); registry component costs are held at base in the draws (charities in use and sponsors vary).
- The model is built and reviewed within the same model family as the research agents; it is not independent validation.

## 8. Revision 2 (adversarial review)

Each fix has a test in `tests/CompetitiveAdvantageCreation.Tests` (named "fix N").

| # | Change | File | Challenge IDs |
|---|---|---|---|
| 1 | Pilot = one whole live Unbound customer (cumulative go-live >= 1 on a dedicated E2 stream) | `Sequences.pilotMonth`, `Cashflow` (`CumGoLive`) | REV2001, REV2044 |
| 2 | Inclusive named-partner test `namedInTime`; results at months 3, 6, median, 12 | `Sequences`, `Analysis.killSensitivity` | REV2002 |
| 3 | One contingency base including the live run | `Cashflow.flows`, `Capital.Corrections` | REV2003 |
| 4 | Variable cost on gross volume | `Cashflow.flows` | REV2010 |
| 5 | Registry cost a function of live sponsors and charities per sponsor | `Cashflow.RegistryAnnualOf`, `Sequences.toStream` | REV2034 |
| 6 | Founder build time netted from founder economic cost | `Cashflow`, `Capital` | REV2035 |
| 7 | Wind-down at a pause; incident reserve; income tax with loss carry-forward | `Cashflow` | REV2004, REV2005 |
| 8 | Ranking against a do-nothing baseline on kill-rule Monte Carlo medians | `Render.sequenceTables` | REV2043, REV2018 |
| 9 | Nacha TPSP audit and fraud monitoring in the base live run | inputs, `Sequences.toStream` | REV3019, REV1026 |
| 10 | Registry M1 governing; M5 conditional on OD-CDD-02 | `settings.csv`, `Analysis` | REV3010, REV3020 |
| 11 | Revenue per customer from sponsor size; reachable customers from the FY2024 panel; break-even size | `Sequences.toStream`, `Analysis.sizeTable`, `breakEvenAccounts` | REV1001, REV2011, REV2012, REV3030 |
| 12 | Control operations in base; conventional maintenance stress | inputs, `Analysis` | REV3004, REV3022, REV2029, REV2030 |
| 13 | First conversion $75-325k; first three customers at that rate; go-live lag 6-12; sponsor conversion labour reported as transferred | inputs, `Cashflow` | REV3037, REV3038, REV3039, REV3040 |
| 14 | A3B and A3X sequences carry the S2-to-S3 build inside or outside the cost center | inputs | REV1046, REV2038 |
| 15 | Four-digit IDs; adversarial-challenges register; disposition overlays and requirement flag | `Validate`, `Registers` | coordinator item 15 |

Also: SOC 2 Type 2 lag before first regulated signing (REV1021, REV3021); partner remittance lag (REV2007); customer-funded variant limited to direct billing (REV3031); discounted payback (REV2009); partner termination hazard in the Monte Carlo (REV2016, REV1002).

## 9. Revision 3 (round-2 review)

**Two bases.** Each round-2 correction is a switch in `Cashflow.Basis` or `Analysis.ModelBasis`. `revision2` reproduces the published revision-2 results (tested: A3 base peak); `revision3` (CFO-corrected) applies all corrections and drives the sequence tables (setting `basis`). Registry configurations (mode x who performs the deep review x demand-driven or tiered) are a separate dimension (`Analysis.registryConfig`). The decision-relevant comparison is the bases table in [16](16-capital-efficient-market-entry.md) section 1b.

<!-- model-output: tables/bases.md -->
| Basis | Registry configuration | S3 cash / fully loaded to first invoice | A3 peak / m120 / payback | A3 kill rule | A peak / m120 / payback | A kill rule | Partner book peak / m120 / payback | Partner book kill rule |
|---|---|---|---|---|---|---|---|---|
| Revision 2 (conservative) | M1, Echelon performs the deep review, 2 reviews a year (revision 2) | $2.12M / $2.89M | $8.70M / -$8.70M / none in 120 | paused at 24 ($1.81M) | $8.98M / -$8.98M / none in 120 | paused at 24 ($1.46M) | $27.17M / -$27.17M / none in 120 | paused at 24 ($1.64M) |
| Revision 2 (conservative) | M5 hybrid (conditional on OD-CDD-02) | $1.81M / $2.54M | $3.46M / -$340k / none in 120 | paused at 24 ($1.81M) | $4.28M / -$1.41M / none in 120 | paused at 24 ($1.46M) | $3.69M / -$63k / none in 120 | paused at 24 ($1.64M) |
| Revision 3 (CFO-corrected) | M1, Echelon performs the deep review, 2 reviews a year (revision 2) | $1.97M / $2.72M | $12.31M / -$12.31M / none in 120 | paused at 24 ($1.38M) | $12.11M / -$12.11M / none in 120 | paused at 24 ($1.33M) | $33.01M / -$33.01M / none in 120 | paused at 24 ($1.32M) |
| Revision 3 (CFO-corrected) | M1, Echelon performs the deep review, demand-driven | $1.83M / $2.57M | $8.26M / -$8.26M / none in 120 | paused at 24 ($1.38M) | $8.46M / -$8.46M / none in 120 | paused at 24 ($1.33M) | $17.58M / -$17.58M / none in 120 | paused at 24 ($1.32M) |
| Revision 3 (CFO-corrected) | M1 risk-tiered attested review, Echelon performs, demand-driven (subject to counsel and V-9) | $1.71M / $2.44M | $4.61M / -$4.61M / none in 120 | paused at 24 ($1.38M) | $5.17M / -$5.17M / none in 120 | paused at 24 ($1.33M) | $4.33M / -$3.68M / none in 120 | paused at 24 ($1.32M) |
| Revision 3 (CFO-corrected) | M1, sponsor performs the deep review (transferred; P3-DEC-MOD005) | $1.63M / $2.35M | $2.49M / -$2.17M / none in 120 | paused at 24 ($1.38M) | $3.26M / -$2.98M / none in 120 | paused at 24 ($1.33M) | $2.43M / $4.18M / 76 | paused at 24 ($1.32M) |
| Revision 3 (CFO-corrected) | M5 hybrid (conditional on OD-CDD-02) | $1.64M / $2.35M | $2.52M / -$2.38M / none in 120 | paused at 24 ($1.38M) | $3.29M / -$3.16M / none in 120 | paused at 24 ($1.33M) | $2.60M / $3.48M / 80 | paused at 24 ($1.32M) |
<!-- /model-output -->

| # | Change | File | Test | Challenge IDs |
|---|---|---|---|---|
| 1 | Contingency on one-time and pre-revenue cash and the first 12 live months (P3-ASM-AB027 basis) | `Cashflow.flows` | r3 fix 1 | REV4002 |
| 2 | Wind-down at the pre-revenue run when nothing is live | `Cashflow.flows` | r3 fix 2 | REV4010 |
| 3 | Sponsor platform classification (P3-ASM-MOD056) and plausible-sponsor cap; cap sensitivity | `Inputs.platformClass`, `Analysis.inCapSet` | r3 fix 3 | REV4006, REV4017 |
| 4 | Cap on live customers plus pipeline; static panel stated | `Cashflow.signingsAt` | r3 fix 4 | REV4007 |
| 5 | Whole first signing; kill-timing table | `Cashflow.signingsAt`, `Analysis.killTiming` | r3 fix 5 | REV4009 |
| 6 | Deep review demand-driven, tiered option, performer allocation, per sponsor-charity | `Registry.runCostWith`, `Registry.addableBy`, `Analysis.registryOptions` | r3 fix 6 | REV4001, REV4003, REV4004, REV4014, REV4018 |
| 7 | Control operations net of maintenance approvers; adverse TPSP overlap | `Sequences.toStream` | r3 fix 7 | REV4005 |
| 8 | Partner-book sequence (P3-SEQ-MOD012) | inputs | r3 fix 8 | REV4008 |
| 9 | Gate break-even in single-sponsor and partner-book accounts | `Analysis.breakEvenFor` | r3 fix 9 | REV4011 |
| 10 | Bases published side by side | `Render.revision3Tables` | r3 fix 10 | REV4019 |
| 11 | H failure band high | inputs | r3 fix 11 | REV4016 |
| 12 | REV4 agent key; overlay files `adversarial-challenges-dispositions*.csv` | `Validate`, `Registers` | r3 fix 12 | coordinator items 12 |

Not changed: the event-model platform residual is not carried into the licensor base (it is the administrator's automation upkeep; the licensor's equivalent is maintenance, with conventional maintenance as a stress) (REV4015); the Nacha base amount remains unquoted (REV4005).
