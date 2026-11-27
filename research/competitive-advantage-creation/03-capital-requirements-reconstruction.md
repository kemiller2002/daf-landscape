# 03 - Capital requirements reconstruction

Status: research (2026-11-26). Agent AB, Track A support. Every Phase II capital figure is traced to its inputs below. The figures were reproduced with a replica of `Routes.fs`, which matches the Phase II outputs exactly for ER-4, ER-5 and ER-7. Each line is marked by type: sunk vs incremental, conventional-organization assumption vs obligation, and double count. Nothing here changes Phase II's records; this report annotates them. Register rows: [capital-requirements.csv](data/fragments/AB/capital-requirements.csv) and [claims.csv](data/fragments/AB/claims.csv).

## 1. Figures reconstructed

| Phase II figure | Where stated | How it is built | Reproduced? |
|---|---|---|---|
| G0 $0.15-0.35M | [22](../competitive-displacement/22-commercial-validation-plan.md) §1; [15](../competitive-displacement/15-capital-and-break-even-reassessment.md) §3 | V-1 $10-30k + V-2 $20-60k + V-3 $30-80k + V-5 $5-15k + V-6 $5-15k + V-9 $0-30k = **$70-230k**, plus an implicit "buyer-access line" of **$80-120k** (founder selling time, conference presence, security and legal responses; CHL-020, CHL-099). The buyer-access line has no line items | Yes, by subtraction (P3-CLM-AB007) |
| Full evidence budget $0.35-0.75M | 22 §1 | G0 + V-4 $40-160k + V-7 $20-60k + V-8 $10-30k + PR #87 gates (licence terms $10-50k, counsel $15-100k) + SOC 2 Type 1 readiness ($10-40k) = **$255-790k** | High end yes. Low end is ≈$95k short of $0.35M, with no stated line (P3-CLM-AB010) |
| G1 $1.0-1.5M cumulative | 15 §3; 16 §3 | **No line-item derivation.** Stated basis: 9-24 month sales cycles (CHL-013), SOC 2 Type 1 and a privacy programme (CHL-014, CHL-040). Implied: G0 plus $0.65-1.15M over about 18 months, or **$36-64k a month**. That is between ER-6 burn ($70k/mo) and a lean structure | Not reproducible. Reconstructed below (P3-CLM-AB008) |
| ≈$6.5M P50 to a self-sustaining niche | 15 §3 | $1.0M (G0-G1) + ER-7 Monte Carlo P50 $5.96M − ≈$0.5M build reuse | Yes |
| ≈$9M P90 | 15 §3 | ER-7 P90 $8.0M + ≈$1.0M G0-G1 | Yes (approximately) |
| ER-7 base $5.66M | 15 §2 | Build $1.6M over 15 months + burn $110k × 51 months ($5.61M) + CAC $40k × 9 signings ($0.36M) − contribution $1.91M, at the month-51 trough | **Yes, exactly** (P3-CLM-AB001) |
| ER-5 ≈$10.3M full administration | 15 §2 | Build $1.94M + burn $190k/mo + CAC $125k; 0.6 customers a year at $2M; variable share 0.35 | Yes ($10,308,920) |
| PR #87 $4.5M founder-led | SRC-002 report 11 | Sequence F: F1 builds, F3 from the anchor's go-live, $1.0B anchor, below-market founder pay | Cited, not re-run |
| PR #87 $1.35-2.8M "if Unbound already exists" | SRC-002 report 11 §7 | Servicing company only; no build; Layer B engineering excluded | Cited; administration, not licensing |
| Build $1.1-2.4M MSP (base $1.94M); full scope $3.6M+ | SRC-002 report 04; CHL-057 | Market engineering hours at a 1-3x agent multiple (base 1.5x) | Cited. It is an **economic** valuation, not cash |
| Unbound `build_capex` $5M ($3-15M) | Unbound parameters.json | "FSM peak capital $2.5-35.8M by path". PR #87 found **no derivation** | Superseded by PR #87 |
| PR #87 Gate 1 $0.12-0.15M | SRC-002 report 11 | M-01..M-04 components sum to **$45-240k (base $120k)** | The stated range is the base, not the component range (P3-CLM-AB009) |
| PR #87 Gate 2 $0.6-0.75M cumulative | SRC-002 report 11 | Gate 1 + M-05 $0 + M-06 $100-300k + M-07 $150-450k = **$295-990k (base $620k)** | Same issue |
| ai-native-daf-enterprise roadmap $5.5-9.5M through Gate 5 | P3-SRC-AB003 | Phase budgets $0.4-0.8M, $0.9-1.4M, $1.0-1.6M, $1.8-3.0M, $2.2-3.4M; 4-20 FTE | Cited. A conventional team ramp (P3-CLM-AB003) |

## 2. ER-7 decomposition at the trough (month 51, base)

| Component | Amount | Type | Sunk vs incremental, if Unbound exists |
|---|---|---|---|
| Build | $1.60M | Up-front development | **Sunk for Echelon Foundry** at S3+. Not borne by the partner |
| Burn, months 1-15 (during build) | $1.65M | Conventional licensor organization at full run during the build | Incremental, but part duplicates the build labour (§3.1) |
| Burn, months 16-51 | $3.96M | Fixed licensor run (MD-6: platform, CEO/CTO, SOC 2, pen test, insurance, sales, support) | Incremental. The lean replacement is $0.17-1.07M a year |
| CAC | $0.36M | $40k per signing | Incremental; founder-led lean $15-60k for the first customer |
| Contribution (revenue × 0.7) | −$1.91M | Offsets the deficit | — |
| **Capital** | **$5.66M** | | **≈$4.06M without the build; ≈$1.27-1.47M lean** |

The Monte Carlo spread (P10 $4.70M, P90 $8.00M) comes mainly from burn, time to first revenue and customers per year, not from build. In Phase II's adverse case the build is $2.2M of a $19.2M floor.

## 3. Double counting and inconsistencies

1. **Build-period burn (P3-CLM-AB004; inferred).** `Routes.fs` adds `build/buildMonths` to the full `burn` in every month up to the first revenue month. MD-6's fixed cost (the source of the burn) includes "Platform 0.7-1.8M + CEO/CTO". If that platform team is the team that builds, both terms pay for the same people. Sensitivity: at a 40% run during the build, ER-7 base falls from $5.66M to **$4.67M**. This is a modelling choice rather than an arithmetic error, but it is not stated.
2. **Channel share (P3-CLM-AB005; hypothesized).** Revenue per customer is described as "~$81 per account less a 30% channel share", so it is already net. `variable_cost_share` is 0.30 for ER-7, against 0.15 for ER-4 (direct). If the additional 0.15 restates the channel share, ER-7 base is overstated by **$0.33M** (vs 0.15: $5.33M). If it represents partner-specific integration and support cost, it stands. Ask agent MOD to resolve it with the model owner's documentation; until then, report both.
3. **G0-G1 + ER-7 (P3-CLM-AB006; inferred).** ER-7 is simulated from month 0 with its own build and 15 months to revenue. The staged plan adds G0-G1 ($1.0M) and credits only $0.5M of build reuse. CHL-085 argued the sum is *under*stated because ER-7 starts later. The opposite reading also holds: if G1's partner pilot is ER-7's first go-live, the G1 spend and ER-7's first 18 months of burn overlap by up to about $1.0M. The defensible statement is that **$6.5M is an upper-middle estimate that combines two overlapping simulations**, not a sum of independent stages.
4. **G1 omits the build (P3-CLM-AB008).** A live module pilot at G1 needs a working ledger, migration and eligibility evidence. $1.0-1.5M cannot buy that plus G0 unless the platform already exists. G1 therefore embeds the existing-Unbound premise, while the $6.5M total charges the build again inside ER-7. For a completed Unbound, both should drop the build.
5. **Gate ranges (P3-CLM-AB009, AB010).** PR #87 Gate 1 and Gate 2, and Phase II's evidence budget, state ranges that do not match the sums of their components. The differences are $0.1-0.25M, small in money. But they make the "evidence budget" look more precise than it is.
6. **Assurance counted at two scales.** Unbound's sponsor-scale `legal_base` $200k, `audit_base` $120k and `insurance_base` $150k (scaled by log assets) enter the vendor floor behind Unbound's $217/fund break-even at 25k funds (05a §2b). PR #87 judged these "lower for servicer" (AR-LYR-043). For a licensor they overstate cost by roughly $0.2-0.4M a year.

## 4. Conventional-organization assumptions embedded in the figures

| Figure | Conventional assumption | Kept, replaced or obligation |
|---|---|---|
| ER-7 burn $80-160k/mo | CEO + CTO at market; sales lead; 1 support FTE; full assurance from month 1 | **Replaced** with a lean run plus founder economic cost (02 §2) |
| MD-6 fixed $1.35-2.75M/yr | As above, plus $0.15M AI oversight and a $50k TPSP audit | AI oversight is small for a licensor with no AI-authoritative functions (DEC-005). TPSP **kept as a base obligation**: ratified CNV-PAY-001 makes Unbound a Nacha TPSP, and the Nacha Rules require an annual Rules compliance audit by 31 December (Article One §1.2.2). **Revision 2 (P3-CHL-REV3019):** previously "TPSP kept if the vendor creates ACH files" |
| ai-native roadmap 4-20 FTE | Team ramp ahead of revenue | Replaced: hire only after elimination tests (Echelon business plan §11, P3-SRC-AB009) |
| Direct CAC $125k | Sales org | Replaced by partner, plus a founder-led first customer |
| Onboarding $105k | Professional services | Reduced at S6 |
| SOC 1 + SOC 2 + pen test + insurance before customers | Premature compliance | Deferred to term sheet, not removed |
| Market-rate founder | Shown in the economic column | **Kept**: shown even when cash is $0 |

## 5. Sunk vs incremental: Echelon Foundry vs a partner

| Item | Echelon Foundry (S3+) | Channel partner |
|---|---|---|
| Unbound build | Sunk (economic $1.35-4.6M; cash $0.25-1.2M, assumption) | Not borne. It is a reason the partner pays a licence instead of building |
| Hardening, partner integration | Incremental $50-370k cash | Its own integration team (unknown) |
| Assurance (SOC 2, pen test) | Incremental, recurring | Relies on the vendor's report; runs its own vendor due diligence |
| Insurance | Incremental, recurring | May require additional insured status and limits |
| Sales and acquisition | Founder time + $15-60k | Bears its own sales cost; takes 30-50% of revenue |
| Implementation | Incremental per customer (falls at S6) | Project management and first line |
| First-line support | Second line only | Bears first line (to be tested, P3-HYP-AB002) |
| Echelon licence | Transfer within the same owner (Echelon Foundry owns all property it makes, OD-P3-01); cash ≈ $0, but written terms, escrow and a second maintainer are needed | Escrow or step-in rights requested |
| Working capital | Arrears billing | Collects from the customer, then remits |

## 6. Reconstructed G1 (existing-Unbound basis)

| Line | Low | Base | High | Basis |
|---|---|---|---|---|
| G0 | $0.15M | $0.25M | $0.35M | Phase II (to be reduced; see [04](04-low-cost-commercial-validation.md)) |
| Hardening (S3 to S4) | $0.04M | $0.12M | $0.25M | P3-ASM-AB002/003 |
| SOC 2 Type 1, pen test, policies | $0.02M | $0.05M | $0.10M | P3-ASM-AB021 |
| Legal (MSA/DPA, payments opinion, licence terms) | $0.02M | $0.06M | $0.15M | P3-ASM-AB022 |
| First-customer acquisition and implementation | $0.05M | $0.11M | $0.21M | P3-ASM-AB019/020 |
| Run until first invoice (pre-contract + go-live lag, incl. founder cash draw) | $0.06M | $0.39M | $1.59M | P3-ASM-AB024, P3-ASM-AB018 and the recurring rows |
| Working capital + contingency | $0.06M | $0.27M | $1.20M | P3-ASM-AB023/027 |
| **G1 cumulative, cash** | **≈$0.4M** | **≈$1.25M** | **≈$3.9M** | = G0 + S3 cash to first invoice (02 §1) |

The base lands inside Phase II's $1.0-1.5M. The difference is that the reconstruction is itemized, assumes the platform exists, and shows a much wider adverse tail, driven by sales-cycle length.
