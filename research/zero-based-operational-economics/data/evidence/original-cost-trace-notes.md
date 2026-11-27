# Original cost trace: notes (previous DAF Unbound model, MD-5)

Last reviewed 2026-11-27. Companion register: [`../registers/original-cost-trace.csv`](../registers/original-cost-trace.csv) (OCT-001..OCT-132). Paths are relative to the repository root unless they are links. All arithmetic was re-run from the model inputs and outputs. Evidence classes follow [`../CONVENTIONS.md`](../CONVENTIONS.md).

**What this audits.** The previous model is `research/competitive-displacement/model` (revision 2). For MD-5 "AI-native administration" it gives break-even of **$1.924B** at 20 bps, a $250k balance and 5 sponsors:

- break-even = (F + 5·S) / (0.002 − v/250,000)
- F = $2,500,000 fixed
- S = $43,679 sponsor-level cost per sponsor
- v = $146.766 variable cost per account
- At break-even that is about 7,696 accounts and about $3.85M of opex.
- The fully loaded figure is **$2.326B**.

## 1. Reconciliation tables

### 1.1 fixed-2.5M (`research/competitive-displacement/data/model-inputs/enterprise-modes.csv` MD-5)

The basis text reads "PR87 lower-bound fixed ~$1.5M plus MSP platform $0.7M + AI ~$0.1M + REV2 $0.2M". "PR87" is `research/commercial-opportunity/ai-native-capital-minimization/`. Its "~$1.5M" is design **F3** ($1.46M), the "three core + $0.65M non-personnel + reviewers" in report 18 Q10. It is not F5 ($1.73M).

| Component | Amount | Source | OCT |
|---|---:|---|---|
| Founder / managing director, loaded | 200,142 | Designs.fs `founderLoaded`, CST-R01 | 001 |
| CTO, loaded | 222,482 | `ctoLoaded`, CST-R02 | 002 |
| Controller, loaded | 183,365 | `controllerLoaded`, CST-R06 | 003 |
| Independent fractional controller review, 200 h | 40,000 | `independentReviewer`, CST-C01 | 004 |
| Two contracted code approvers | 90,000 | `codeReviewers 2`, CNV-PLT-010 | 005 |
| Compliance owner floor: 0.25 FTE × 1.5 premium | 45,693 | pool `MinimumFte`, CST-R10 | 006 |
| Per-person overhead: 3 × $11.1k | 33,300 | `perPerson` | 007 |
| Non-personnel: 31 lines + 7.5% contingency | 645,789 | Designs.fs bundles; cost-register.csv | 009-040 |
| **F3 subtotal** | **1,460,771** | matches PR87 `model/out/results.md` §2 ($1.46M) | |
| Build amortisation: $1,940,117 / 5 | 388,023 | `Layers.servicingCost` Standalone | 041 |
| Echelon share: 45% × $300k | 135,000 | `baseLayers` | 042 |
| Echelon commercial licence | 60,000 | `baseLayers`, CNV-GOV-009 | 043 |
| Non-production environments | 24,000 | `baseLayers` | 044 |
| Maintenance gap: $300k − embedded engineering ($256,862) | 43,139 | `Layers.servicingCost` | 045 |
| Servicing-specific platform | 30,000 | `baseLayers` | 046 |
| **MSP platform subtotal** ("$0.7M") | **680,162** | | |
| REV1 AI evaluation and governance | 100,000 | enterprise-modes basis, ASM-045 | 047 |
| REV2 AI oversight and model-risk management (CHL-104) | 200,000 | adversarial-challenges.csv | 048 |
| **Itemised total** | **2,440,933** | | 050 |
| Unexplained residual | 59,067 | Rounding "1.46 + 0.68" up to "2.2" | 049 |
| **Model figure** | **2,500,000** | | |

The sum check needs the $59k residual. No source supports that residual.

The non-personnel subtotal of $645,789 is made up as follows:

| Group | Lines | Amount |
|---|---|---:|
| Assurance | audit $35k, tax $10k, SOC 2 $35k, SOC 1 $40k, pen test $20k, GRC platform $20k, DR test $10k | $170,000 |
| Insurance | cyber $30k, E&O $25k, D&O $10k, crime $12k, EPLI $4k, GL $3k | $84,000 |
| Specialists | vCISO $48k, compliance consultant $25k, IR retainer $7.5k, counsel 100 h $45k, bookkeeping $24k, CFO review $8k | $157,500 |
| Platform and data | cloud $35,564, AI evaluation $12k, Candid $7,750, sanctions $8k, Persona $3k, bank treasury and Lob $6,720, e-sign and document generation $5k | $78,034 |
| Sales and G&A | conferences $40k, marketing $20k, CRM $2k, filings, bank fees, co-working ($6k office) and accounting software $13.2k | $75,200 |
| Agent compute | | $36,000 |
| Contingency (7.5%) | | $45,055 |

No line covers office rent, sales staff, recruiting or on-call.

### 1.2 build-1.94M

Source: `Designs.fs` `unboundBaseline`, `Development.minimumProductCost` at 1.5x.

| Component | Amount | OCT |
|---|---:|---|
| Non-compressible 30% of the $2.21M MSP scope | 663,000 | 061 |
| Construction 70% ÷ 1.5 | 1,031,333 | 062 |
| Agent compute: 5% of replaced construction | 25,783 | 063 |
| Safety floor: pen test $20k, SOC readiness $20k, accessibility $15k, bank/custodian certification and legal $65k, migration rehearsal $40k, independent code review $60k | 220,000 | 064-069 |
| **Sum** | **1,940,117** (sum check OK) | 073 |

The $2.21M scope comes from report 04 (DEV pass): 132 conventional person-months at $120/h, after a 4 person-month Echelon credit. It is an agent estimate [E]. It was scaled against Unbound's $5M figure, which report 04 itself shows has no derivation (`parameters.json:509-516`).

### 1.3 variable-147

Source: `data/model-outputs/event-costs-by-mode.csv` and `mode-summary.csv`, MD-5.

| Component | $/acct-yr | Source |
|---|---:|---|
| Labour, ops (19.77 min × $65.45 ÷ 0.75) | 28.754 | PAR-001 (CST-V01: $99,478 ÷ 1,520 h) |
| Labour, accounting (3.93 min × $61.48 ÷ 0.75) | 5.371 | PAR-002 (CST-R07 ÷ 1,800 h) |
| Labour, compliance (29.06 min × $67.69 ÷ 0.75) | 43.711 | PAR-003 (CST-R10 ÷ 1,800 h); EV-E10 is $38.06 of this |
| External, EV-E03 contributions | 10.625 | ACT-A04: $10 securities receipt fee [A] |
| External, other | 5.517 | ACT-A01/A05/A08/A23 etc. |
| AI per event | 2.303 | events.csv [A] |
| Prevention | 2.093 | events.csv [A] |
| Expected failure | 23.392 | events.csv [A]: E08 4.80, E10 3.63, E13 3.07, rest 11.89 |
| "Infrastructure" | 25.000 | PAR-011 |
| **Sum** | **146.766** (sum check OK) | |

The 0.75 utilisation divisor adds $19.46 of the $77.84 labour.

### 1.4 infra-25: how a placeholder became "infrastructure"

The $25 passed through four files:

1. **Origin.** `data/commercial-opportunity/servicing-economics/cost-to-serve-parameters.csv` `per_account_usd` $15/$25/$45. It is defined there as *"Account maintenance: statements, donor service contacts, identity/KYC refresh, data. Base chosen so base per-account total (~$75…) reconciles to the $75/fund-yr hypothesis."*
2. **The $75.** That figure is the superseded memo `research/commercial-opportunity/daf-servicer-bottom-up-operating-budget-2026-11-25.md`. The memo itself allots only **$5 to incremental cloud** within its $75.
3. **charity-network 20.** It reuses the $25 as "statements, contacts, contributions, infra share".
4. **The previous model.** `parameters.csv` PAR-011 relabels it `infra_per_account_owned` (ASSUMPTION, "SPN placeholder").

The result:

- The $25 is not infrastructure.
- Statements, contacts and identity are also priced as events (EV-E14, EV-E15, EV-E02).
- Cloud is a separate fixed line ($35.6k).

### 1.5 minutes-53 (OCT-093..100)

| Event | min/acct-yr |
|---|---:|
| EV-E10 grant approval | 25.30 (48%) |
| EV-E11 payment exceptions | 5.36 |
| EV-E15 contacts | 4.82 |
| EV-E08 vetting | 3.36 |
| EV-E13 breaks | 2.66 |
| 20 other events | 11.27 |
| **Sum** | **52.76** |

The native minutes per touch were calibrated at an AI factor of 0.6 and then rescaled to 0.85, which multiplies them by 1.42.

For comparison, PR87 report 06 gives:

- 50.7 minutes as the prior AI-native figure;
- about 30 minutes as a plausible steady state;
- 11.7 minutes as the floor.

### 1.6 sponsor-level-43.7k

| Event | Minutes | Rate (÷ 0.75) | $ |
|---|---:|---|---:|
| E13 close and sign-off | 9,000 | accounting | 12,296 |
| E20 incidents | 1,800 | compliance | 2,708 |
| E21 governance and regulatory reporting | 2,640 | controller | 5,976 |
| E22 audit preparation (held at conventional, CHL-105) | 7,200 | controller | 16,299 |
| E23 configuration upkeep | 3,600 | implementation | 6,400 |
| **Sum** | **24,240** | | **43,679** (OK) |

PR87 used 19,440 minutes. The previous model adds 3,600 minutes of audit preparation and 1,200 minutes of assumed regulatory reporting.

### 1.7 fully-loaded 2.33B

(2,500,000 + 218,396 + 388,023 build + 5·(125,000 CAC + 48,000 onboarding)/5) / (0.002 − (146.766 + 3.556/5)/250,000) = **$2.326B**. That is about 9,300 accounts and about $4.65M of opex. The sum check is OK.

The build amortisation is already inside the $2.5M (OCT-041), so it is **counted twice**. Without the duplicate, the fully loaded figure is **$2.05B**.

### 1.8 registry-316k and registry-min

- **RC-01..RC-10** sum to **$316,093**, which reproduces the charity-network 20 figure exactly.
- **RC-07** (1 FTE steward, $121,848) is 39% of the total. It is a staffing ratio, not a workload derivation.
- **RA-1 (change-driven, 1 sponsor)**:
  - At 5k charities: steward floor $30,461 + connectors $37,760 + counsel $13,500 + storage $4,254 + shared DB $3,118.5 = **$89,093**.
  - At 20k charities: steward workload $103,701 + the same lines = **$162,334**.
  - At 20k, evidence-expiry refresh (an assumption: 0.5 per charity-year × 5 min = 833 h) is the largest single labour item.
- **"charity-network 20" floor.** That report's low bound is $107k, not $90k. The $90-170k range comes from the previous model's report 05.
- **Not in MD-5 fixed.** Neither registry figure is included in MD-5 fixed cost.

## 2. Lineage (text diagram)

```
BLS OEWS/ECEC, vendor pages ──► servicing-economics cost-register.csv (CST-R*, CST-C*, CST-I*, CST-T*) + role-compensation.csv
                                   │            └─► parameters.csv PAR-001..006 rates (÷1520/1800/1600 h)
superseded 5-FTE memo ($1.18M, $75/fund) ──► cost-to-serve-parameters.csv per_account_usd $25 ──► charity-network 20 ECO ──► PAR-011 "infra" $25
                                   │                                                             └─► MD-1 fixed $1.18M (stale)
servicing-economics activities.csv ACT-A01..S07 (minutes, frequencies, [A]) ──► events.csv EV-E01..E25 ──► 52.76 min, $121.77 + $25, $43.7k/sponsor
                                   │
PR87 ai-native-capital-minimization:
  report 04 DEV (132 PM @ $120/h vs unsupported $5M) ──► Designs.fs unboundBaseline ──► MSP build $1.94M @1.5x ──► build-1.94M
  Designs.fs F3 (3 core + non-personnel $0.65M) = $1.46M  ┐
  Layers.fs standalone MSP platform charge $0.68M (incl. $388k build amortisation) ├─► report 18 Q10 "$1.5M + $0.7M" ──► MD-3/4 $2.2M
                                                          ┘                                    + $0.1M AI (REV1) = $2.3M (ASM-045, still in register)
competitive-displacement report 20 CHL-104 (+$0.2M) ───────────────────────────────────────────► MD-5 $2.5M ──► Enterprise.fs ──► $1.92B / $2.33B
competitive-displacement CHL-024 ──► fully loaded adds build/5 again + CAC $125k (PR #86/#88) + onboarding
charity-network 20 §2 (ADVX-01) ──► registry-components.csv RC-01..10 = $316k ──► report 05 RA-1/RA-3 ──► $89-167k
```

## 3. Flagged problems ranked by impact on operating break-even (20 bps)

Each impact holds every other input at base. $100k of fixed cost is worth about $71M of break-even assets, and $1 per account is worth about $5.3M.

| # | Problem | OCT | Δ break-even |
|---|---|---|---:|
| 1 | **Build amortisation counted in fixed and again in fully loaded.** It is one-time capital. | 041, 107 | −$0.27B operating, or −$0.28B fully loaded |
| 2 | **$0.3M AI oversight on a flat basis.** It has no workload basis and leans on SR 11-7, which is bank guidance. At entry scale the AI step saves about $85k, so this makes MD-5 lose to MD-4 by construction. It also overlaps CST-T14 and agent compute. | 047, 048, 029, 039 | −$0.16 to −$0.21B |
| 3 | **Echelon share $135k and licence $60k charged to servicing as standalone costs.** These are group costs, and the licence cancels between commonly owned layers (Layers.fs). | 042, 043 | −$0.14B (group view) |
| 4 | **Core queue capacity paid twice.** The controller's 60% ($110k), founder's 15% ($30k) and compliance floor ($46k) are in fixed, and the same work is priced as event and sponsor-level minutes. That overlap is about $34.6k per sponsor of controller and accounting minutes. | 001, 003, 006, 101, 103, 104 | −$0.13B |
| 5 | **The $25 "infrastructure" is a mislabelled account-maintenance placeholder.** It double-counts statements, contacts, identity and fixed cloud. The memo's own decomposition allots $5. | 089 | −$0.10B |
| 6 | **Utilisation 0.75 sits on top of 1,520 productive hours and on top of fixed segregation-of-duties staff.** PR87 uses 0.9. | 090, 074 | −$0.09B |
| 7 | **Contribution receipt and rail fees are custodian or sponsor costs.** That is $10.6/acct ($10 securities fee "often custodian-absorbed"). | 077 | −$0.05B |
| 8 | **Unexplained $59k residual.** | 049 | −$0.04B |
| 9 | **Several small overlapping lines.** These are three independent-review lines, vCISO vs CTO, the compliance consultant, Persona vs EV-E02, the GRC licence vs Unbound CCM, and Candid vs free federal data. | 004, 022, 023, 027, 032, 079, 014, 030 | −$0.02 to −$0.05B together |
| 10 | **Register drift.** `economic-assumptions.csv` still shows MD-5 at $2.3M, build high at $2.43M and prevention at 1.0. | 130 | none (documentation) |
| 11 | **MD-1 comparator uses the superseded $1.18M memo** instead of the re-priced $1.66-1.74M. | 129 | flatters MD-1 |

If items 1-8 are all removed, the overstated amounts total about **$0.95-1.0M a year of fixed cost plus about $43 per account**.

## 4. Items possibly underestimated or missing

| Item | OCT | Placeholder | Δ break-even |
|---|---|---:|---:|
| PR87's own steady-state adjustments, omitted: sales to $250k (+$188k), turnover ($35k), replacement onboarding ($45k) | 051 | $268k | +$0.19B |
| December release capacity and integer staffing by pool (CHL-109 deferred) | 053 | $50-300k | +$0.04 to +$0.21B |
| Per-tenant infrastructure floors (CHL-064; UNKNOWN) | 055 | $0-250k | up to +$0.18B |
| Registry run cost not in MD-5. The non-overlapping part is about $51k (connectors and counsel); RA-1 runs $89-162k. | 056 | $51-162k | +$0.04 to +$0.11B |
| 24x7 on-call for payment release (CHL-057; UNKNOWN) | 054 | $30-150k | +$0.02 to +$0.11B |
| Per-person overhead for about 5.8 FTE of variable labour | 007 | ~$64k | +$0.05B |
| Coordination beyond six pairs, at about 9 heads | 008 | ~$57k | +$0.04B |
| Nacha TPSP audit. It was added to MD-6/7 but not MD-5, which runs the same ACH platform. | 052 | $50k | +$0.035B |
| Insurance limits: cyber and E&O at $5M, crime sublimits, no fidelity bond (no quotes) | 016, 017, 019, 058 | +$20-100k | +$0.01 to +$0.07B |
| SOC 2/SOC 1 internal evidence time, and counsel above 100 h in years 1-3 | 011, 012, 025 | not costed | — |
| Onboarding at $48k per sponsor, against $757k for a 10k-account sponsor in charity-network 20 (including pre-delegation labour) | 109 | — | fully loaded only |

Missing build items:

- the deferred-scope tranche of about $0.6M (OCT-070);
- startup legal and the regulatory opinion, about $0.12M (OCT-071);
- the scope gap between the MSP (one sponsor, manual NAV import) and the levers MD-5 assumes (OCT-060). The high case is $3.6M or more.

Custody, trust-partner fees and bonds are UNKNOWN (OCT-057).

Founder opportunity cost is **already included**: the founder is at market pay in F3.

The underestimates total about **$0.65-1.1M a year** of omitted recurring cost.

## 5. What would have to be true for $1.9B to stand

The $1.92B is not derived from the components. It survives only because errors in opposite directions offset each other. For it to stand:

1. **Fixed cost really is about $2.5M a year of recurring operating cost**, excluding build amortisation. The itemised recurring content after the double counts is about $1.6-1.8M. So about **$0.7-0.9M of currently unlisted recurring cost** must exist:
   - sales to about $250k;
   - December release capacity;
   - on-call;
   - TPSP audit;
   - registry operation;
   - coordination and per-person overhead;
   - adequate insurance.

   Section 4 suggests that is plausible, but none of it is evidenced.
2. **Variable cost is about $147 per account.** That requires a mix of conditions:
   - the 0.75 utilisation is real slack, not integer staffing already in fixed;
   - per-tenant floors make up the gap between $5 and $25 of infrastructure;
   - EV-E10 touch rates of about 7.9% at about 36 minutes hold. That is roughly twice PR87's ~3-4% effective rate with determination reuse.
3. **Sponsor-level work is about 24,240 minutes on top of a fixed controller.** The controller's capacity must be fully consumed by unmodelled work.
4. **Other inputs hold:** a $250k average balance (the industry is about $141k; CHL-083), 20 bps realised and 5 equal sponsors.

**Corrected recomputation.** Remove the double counts (items 1, 4, 5, 6, 8) and add the evidenced omissions (sales adjustments, TPSP, the registry non-overlap, December at $150k). Operating break-even lands at roughly **$1.6-1.8B**. Fully loaded lands at about **$2.0-2.2B** before the scope gap in the build. Treat this as a directional range, not a replacement estimate.

## 6. Conventional-administrator benchmarks held in the repository

**Ren / staffed administration payments (990 Part VII-B)**

Source: `research/commercial-opportunity/servicing-economics/01-pricing-and-scope.md`, with `data/commercial-opportunity/servicing-economics/price-observations.csv` (PRC-O-*).

- **Ren to MS GIFT, CY2024: $14.93M.** That is 18.46 bps of average assets, or $737 per account. MS GIFT has $9.1B, 21,800 accounts and 0 employees. CY2022-23 were 18.4-18.8 bps ($685-714).
- **Ren to U.S. Charitable Gift Trust: $4.43M.** That is 39-40 bps, or $389-429 per account.
- **Ren to RCF, FY2024: $19.2M.** That is 38.7 bps of admin revenue.
- **Ren to Stifel: $801k**, plus Stifel Trust staffing of $723k.
- **Ren/Stellar software-only:** $118k-$2.50M, or 0.5-9 bps ($34-611 per account), with a floor of about $120-175k.
- **TIFIN Give to GiveClear: $185,921.** That is $815 per account; the ADV lists 30 bps up to $1M.
- **Captive administrators:** FMR is paid 23.7 bps ($179.9M); BofA trustee 56 bps bundled; RJ Trust 67 bps including investment management.
- The observed staffed band is **18-40 bps, or $390-815 per account-year**.

**Sponsor expense ratios and staffing**

Source: `research/mission-2026-11-14/sponsor-cost-structure-and-sensitivities.md`, with data in `data/mission-2026-11-14/sponsor-cost-structure.csv` and `sponsor-cost-structure-summary.csv`. All FY2024 990s.

| Group | Operating cost bps | Per account | Notes |
|---|---|---|---|
| All sponsors (DAF-allocated) | 67 | | |
| Standard nationals | 32 (25 excluding Servant) | about $2.6k | median 0 employees |
| Community foundations | 127-177 | $3.8-5.6k | staff 54% of cost |
| Processors | 456-805 | $82-146 | PayPal $36; AOGF $87 |

Community foundations by DAF-asset band:

| DAF assets | Operating cost bps | Median employees |
|---|---:|---:|
| <$10m | 243 | 3 |
| $10-50m | 189 | 9 |
| $50-250m | 162 | 21 |
| $250m-1bn | 119 | 54 |
| $1-10bn | 84 | 124 |

National sponsors over $10bn:

| Sponsor | Operating cost bps (ex-11f) | Employees |
|---|---:|---:|
| Fidelity Charitable | 26 | 0 |
| NPT | 17 | 286 |
| DAFgiving360 | 21 | 194 |
| Vanguard Charitable | 18 | 119 |
| GS DAF Philanthropy Fund | 12 | 0 |

Cost elasticity to assets is 0.41 for nationals and 0.84 for community foundations.

**Servicer budget benchmarks**

- `research/commercial-opportunity/servicing-economics/03-organization-and-budget.md`:
  - Model A (founder-led, 3 core): $1.31M economic, $1.12M cash.
  - Model B (5 core): $1.66M.
  - Model C (12 FTE): $2.84M.
  - The non-personnel floor is about $0.61-0.65M at any headcount.
- PR87 `model/out/results.md` §1: previous Model B fixed $1.74M; fully loaded break-even $2.09B.

**Unit price and set-up anchors**

- `research/competitive-advantage/charity-network-and-onboarding/20-economic-analysis.md`:
  - Unbound C0 break-even is $101-120 per account at 10k+ accounts.
  - First-sponsor platform fixed cost is $3.04M a year (organisation $1.66M + build $1.0M + registry $0.38M).
  - Ren markets set-up at about $50k and 90-120 days (vendor claim).

**Comparison.** MD-5 opex at its own break-even is about $3.85M across 7,696 accounts, or about **$500 per account-year (20 bps)**. That sits inside the staffed band ($390-815) and above Ren's USCGT take ($389-429).

## 7. Memory and provenance

No user memory notes bore on this task. Every figure above comes from repository files read in this session.
