# 02 - Existing-Unbound economics

Status: research (2026-11-26). Track A, the priority track. Agent AB. This is not an investment recommendation, an approved budget or an authorization to spend (DEC-008). Every figure is an assumption, an arithmetic result from labelled assumptions, or a cited public price. **No figure here is measured business performance.** The authors, the reviewers of Phase II and this agent all come from the same model family, so nothing here is independent validation.

Inputs:
- Phase II package [15](../competitive-displacement/15-capital-and-break-even-reassessment.md), [16](../competitive-displacement/16-commercial-entry-strategy.md), [10](../competitive-displacement/10-zero-touch-administration-economics.md) and [14](../competitive-displacement/14-alternative-enterprise-models.md);
- the Phase II route model (`model/src/CompetitiveDisplacement/Routes.fs`, inputs `data/model-inputs/entry-routes.csv` and `enterprise-modes.csv`);
- PR #87 (SRC-002) layer costs and gates (P3-SRC-AB001, P3-SRC-AB002);
- the PR #86 cost register (SRC-003);
- Unbound reports 05, 05a, 07, 14 and 16 (P3-SRC-AB005..AB008);
- the Echelon business plan sections 06, 11 and 15 (P3-SRC-AB009).

Machine-readable outputs:
- [model-capital-states.csv](data/fragments/AB/model-capital-states.csv): one row per state × cost category, cash and economic, low/base/high;
- [capital-requirements.csv](data/fragments/AB/capital-requirements.csv);
- [assumptions.csv](data/fragments/AB/assumptions.csv).

The working scripts are in [data/evidence/AB/](data/evidence/AB/routes.py). They are a Python replica of the Phase II F# route model and reproduce its ER-4, ER-5 and ER-7 capital figures exactly. They are scratch tools; the durable F# model belongs to agent MOD.

## Answer in brief

1. **Once Unbound is functionally complete (S3), the minimum incremental *cash* to commercialize it through a partner is about $0.25M (low), $1.0M (base) and $3.5M (high) to the first invoice from a referenceable paying customer.** To cash self-sufficiency it is **about $1.5M (base)**, with $0.3M in the favourable case, on Phase II's own channel-revenue assumptions (P3-CLM-AB011, P3-CLM-AB012).

   **Revision 2 (2026-11-26, round-1 review P3-CHL-REV1038).** The figures in items 1-2 are this agent's published method and are kept as history. They are superseded by the model's corrected figures (registry run added, variable cost per account, implementation for later customers), which are generated in [16](16-capital-efficient-market-entry.md) §1 "Key figures". Quote 16, not this item. After model revision 3 (CFO-corrected basis), S3 cash to the first invoice is **$384k / $1.83M / $6.63M** with Echelon performing the M1 deep review on demand, and $1.64M base under M5, which is conditional on OD-CDD-02. To cash self-sufficiency there is no base-case payback within 120 months: A3's uninterrupted peak is $8.26M (`key-figures.md`). Only the partner-book sequence pays back, and only when the sponsor performs the deep review (`bases.md`). Revision 3 note: revision 2 gave $542k / $2.12M / $7.12M, $1.81M and $8.70M. The "$1.5M base to self-sufficiency" in item 1 therefore no longer holds.
2. **Fully loaded economic cost** adds the founder's time at market ($0.19-0.27M a year, CST-R02) and a capital charge. To first invoice it is $0.56M / $1.7M / $5.1M. To self-sufficiency it is about **$2.2M (base)**.
3. **Phase II's $6.5M P50 / ≈$9M P90 is mostly not a build number.** In ER-7 base, $5.61M of the $5.66M deficit is fixed burn over 51 months, against a $1.6M build offset by $1.9M of contribution. Removing the build alone (Unbound exists) cuts ER-7 base only to **$4.06M (−28%)**. The rest comes from replacing a conventional licensor organization ($0.96-1.92M a year of burn from month 1) with a lean one ($0.17-1.07M a year) (P3-CLM-AB001..AB003).
4. **When revenue is adverse, no cost structure is self-sustaining**: Phase II's adverse case is one customer a year at $150k. Capital is then bounded only by the kill rule, about $1.2-1.7M cash at month 24 (P3-CLM-AB013). Lean operation lowers the entry ticket; it does not create demand.
5. **The three largest drivers**:
   - (i) time to first revenue and partner throughput (9-24 months; 1-5 customers a year);
   - (ii) the fixed annual run rate, mostly assurance, insurance and engineering maintenance;
   - (iii) net revenue per customer after the channel share, which includes a possible double-count of channel economics (P3-CLM-AB005).

   Build cost is fourth once Unbound exists.
6. **Costs do not vanish.** Each removed conventional cost has a replacement mechanism, a residual risk and an evidence requirement (§5). The founder's economic cost stays even when cash is $0.

## 1. States and what each one leaves to spend

S2 is today's state:
- Unbound has requirements, architecture, an F# public-data replay tool and a first `Echelon.Execution` slice (P3-SRC-AB016);
- there is no production code for the ledger, payments or the portals;
- the Echelon components are PolyForm Noncommercial (P3-SRC-AB006). Echelon Foundry owns all of them and Unbound (OD-P3-01, 2026-11-26), so commercializing Unbound needs no licence from a third party; buyers will still ask for written commercial terms, escrow and continuity (§5).

**Revision 2 (2026-11-26; P3-CHL-REV3001, P3-CHL-REV3002).** S3 has no acceptance definition in this report. Until one exists, treat S3 as reached only when testable exit criteria pass: the PR #87 MSP scope delivered; the CNV-ARC-001 benchmark run on a managed instance; negative tenant-isolation tests passing; a ledger replay proof; and a synthetic migration rehearsal reconciled. The S2→S3 cash ($0.25-1.2M, base $0.60M) rests on an unledgered agent-productivity assumption (P3-ASM-AB002). Until build hours and cash are ledgered (P3-GAP-AB002), treat S2 cash as unknown. The economic floor is the PR #87 MSP valuation of $1.35M or more (SRC-002 report 04).

| State | Definition used | Remaining development (cash / economic, base) | Months to first contract (low/base/high) | Incremental cash to first invoice (low / base / high) | Fully loaded economic to first invoice (low / base / high) |
|---|---|---|---|---|---|
| S1 | Nothing exists | $0.70M / $2.15M | 18 / 27 / 42 | $0.58M / $1.86M / $5.83M | $2.1M / $4.1M / $11.1M |
| S2 | Requirements and architecture (today) | $0.60M / $1.94M | 15 / 24 / 36 | $0.51M / $1.70M / $5.31M | $1.9M / $3.8M / $9.9M |
| **S3** | **Functionally complete, not production-hardened** | **$0.12M / $0.35M** (hardening) | **9 / 15 / 24** | **$0.25M / $1.00M / $3.51M** | **$0.56M / $1.68M / $5.10M** |
| S4 | Production-ready, no customers | $0.04M / $0.10M (partner integration) | 9 / 15 / 24 | $0.22M / $0.90M / $3.33M | $0.43M / $1.40M / $4.66M |
| S5 | Successful pilot (one referenceable live sponsor) | $0.06M / $0.30M (partner-requested scope) | 0 | per further customer: see note | — |
| S6 | Reusable onboarding packages | $0.04M / $0.20M | 0 | implementation $10-80k per customer (vs $35-150k) | — |
| S7 | On Echelon shared infrastructure | as S6 | 0 | security, compliance and infrastructure × 0.6 **only if another revenue-bearing product shares them** | — |

The base column of the two cumulative columns adds:
- one-time items (development, first-customer acquisition, implementation, compliance readiness, legal, working capital);
- the pre-contract run rate;
- the live run between go-live and first invoice (3/6/9 months);
- founder cash draw;
- contingency of 15/25/40%.

The economic column adds founder time at market and a 5/10/15% capital charge on the cash deployed. For S5-S7 the CSV's one-time rows mean "per further customer". Their recurring rows are the annual fixed run that revenue must cover. The contingency and capital-charge rows computed for S5-S7 are indicative only.

**Finding (P3-CLM-AB014).** From S3 onwards, time to revenue depends on sales and partner cycles, not on build. S3 and S4 differ by only about $0.1M. The 9-24 month sales cycles in the target segments (CHL-013) dominate. **Production readiness bought before a named partner exists is inventory, not progress.**

## 2. Cost categories, separated (S3 → first customer, base unless stated)

Units: "/yr" means USD per year; anything else is USD one-time.

| Category | Cash low / base / high | Economic base | Basis (assumption IDs) | Phase II or PR #87 conventional equivalent |
|---|---|---|---|---|
| Sunk cost (build, requirements) | $0.26M / $0.63M / $1.26M | $2.14M | P3-ASM-AB001; PR #87 M-08 MSP $1.35-2.43M at market | Treated as up-front capital in every ER route |
| Incremental development (hardening) | $40k / $120k / $250k | $350k | P3-ASM-AB002/003 | Inside $1.6M build |
| Maintenance /yr | $40k / $120k / $250k | $120k | Agent compute (A02 $6-60k), contracted second maintainer or code approvers (A03 $79-220k; CNV-PLT-010); P3-ASM-AB010/011 | 1-2 engineers $0.22-0.47M/yr (PR #87) |
| Security /yr | $20k / $50k / $120k | $50k | Pen test $5-35k (P3-SRC-AB012, 2026 vendor guides); fractional vCISO $24-96k (CST-C03, ASSUMPTION); P3-ASM-AB012 | vCISO + security engineer |
| Compliance /yr | $30k / $80k / $180k | $80k | SOC 2 Type 2 $15-70k (CST-C11); compliance automation $8-40k (unpublished prices, P3-SRC-AB014); high adds SOC 1 ($20-120k) and Nacha TPSP audit ($50k, Phase II); P3-ASM-AB013. **Revision 2:** the TPSP audit is a base obligation, not a high case. Ratified CNV-PAY-001 makes Unbound a Nacha Third-Party Service Provider that accepts TPSP obligations, including fraud monitoring, and the Nacha Rules require an annual Rules compliance audit by 31 December (Article One §1.2.2). The model now carries it in the base live run at $30k / $75k / $130k a year (P3-ASM-MOD040; P3-CHL-REV3019) | SOC 1 + SOC 2 + TPSP from month 1 |
| Compliance one-time | $20k / $45k / $100k | $45k | Readiness $10-40k (CST-C13); Type 1 audit fee $5-25k (P3-SRC-AB011); P3-ASM-AB021 | — |
| Infrastructure /yr | $20k / $45k / $110k | $45k | Managed PostgreSQL HA $3-12k + DR $1.6-6k (Azure retail API, CST-T01/T02, accessed 2026-11-25), hosting $12-60k, non-prod $3-20k; per-tenant floors (CHL-064) in high; P3-ASM-AB014 | Unbound `infra_base` $150-600k/yr |
| Customer acquisition (first customer) | $15k / $30k / $60k | $30k | Founder-led: travel, events, term-sheet review, partner diligence responses; P3-ASM-AB019 | $40k/customer (ER-7); $125k/sponsor (direct) |
| Implementation (first customer) | $35k / $75k / $150k | $75k | Transitus phase 1 plus partner first line; PR #86 onboarding $35-325k; P3-ASM-AB020. **Revision 2:** Transitus phase 1 packages are target-side or public-specification only (TRN-REQ-MP-006); incumbent vendor packages are phase 3. A first conversion from an incumbent is therefore hand-mapped. The model now uses $75k / $150k / $325k for the first conversion and charges the first three customers per incumbent cluster at that rate (P3-ASM-MOD042; P3-CHL-REV3037, REV3038) | $105k/sponsor |
| Support /yr | $0 / $40k / $100k | $40k | Partner first line; vendor second line up to 1 FTE (CST-R13 $58-97k); P3-ASM-AB015 | 1 support FTE in MD-6 |
| Insurance /yr | $30k / $70k / $160k | $70k | ASSUMPTION: $5M cyber, tech E&O, D&O, crime. Broker averages of about $1.5k/yr apply to $1M limits and are not adequate (P3-SRC-AB013, P3-CLM-AB023); P3-ASM-AB016. **Revision 2:** no quote supports the $30k low case for four lines at $5M for a pre-revenue vendor, and buyers may also require funds-transfer-fraud and social-engineering cover. Gather indicative broker quotes ($0) before reusing the range (P3-CHL-REV1024) | Unbound `insurance_base` $100-400k scaled |
| Corporate admin /yr | $25k / $60k / $150k | $60k | Books, tax, own audit, counsel retainer (S01, S03); P3-ASM-AB017 | Legal $200k + audit $120k (Unbound sponsor-scale) |
| Legal one-time | $20k / $60k / $150k | $60k | Payments opinion $15-100k (CST-C08); MSA/DPA; Echelon licence terms (A08 $7-60k); P3-ASM-AB022 | Startup legal $40-150k |
| Working capital | $25k / $75k / $200k | $75k | Billing in arrears plus collection lag; incident retention; P3-ASM-AB023 | Not separated in Phase II |
| Contingency | 15% / 25% / 40% | same | P3-ASM-AB027 | 7.5% on opex (PR #87) |
| Founder compensation /yr | $0 / $0 pre-revenue, $60k live / $150k live | **$222k** | Cash is the founder's choice; economic is the market-loaded CTO rate (CST-R02 $190-273k); P3-ASM-AB018 | CEO + CTO at market from month 1 |
| Economic opportunity cost /yr | $0 | 10% of cash deployed | P3-ASM-AB028 | Not modelled |
| **Live fixed run, total /yr** | **$165k / $465k / $1.07M** (+ founder draw) | **$687k** | Sum of the recurring rows | **MD-6 fixed $1.35-2.75M; ER-7 burn $0.96-1.92M** |

**Implication.** At $81 per account gross, with a 30% channel share and Phase II's 30% variable share, the lean base breaks even at about **23.1k licensed accounts in cash** on the model's revision-3 lean cost base: $1.03M a year fixed, including TPSP obligations, control operations, founder draw and the registry, plus $12.15 variable per account, at a net price of $56.70 ([16](16-capital-efficient-market-entry.md) response table). Revision 3 note: revision 2 gave ≈28.1k on a $1.25M base. An earlier Revision 2 note quoted ≈13.7k on the revision-1 lean base ($612k fixed); that figure is superseded. Phase II's figure at $81 with no channel share is about 36k (MD-6). Viability thresholds depend on the cost base: report 13's ~43k accounts at $73 net are on MD-6, not on this base.

**Revision 2 (2026-11-26; P3-CHL-REV3009).** This paragraph previously read "about 13k licensed accounts in cash and about 17k fully loaded, with a range of 4k-34k ... If the extra variable share is a double count (§4), the base is 11k and 14k". Those figures used AB's share-of-revenue variable cost and omitted the registry run. The fully loaded and range figures have not been recomputed on the model's cost base; use [16](16-capital-efficient-market-entry.md).

## 3. Which prior assumptions were conventional-organization assumptions

| Test (owner brief) | Where it sits | Verdict | Size |
|---|---|---|---|
| Conventional teams and market-rate staffing from inception | ER-7 burn $110k/mo and MD-6 fixed "CEO/CTO + sales + 1 support FTE" (ASM-047, ASM-076); Unbound `loaded_cost_per_fte` $165k for every role | **Yes.** Burn runs at full rate from month 1, including during the 15 build months | ≈$1.0M of ER-7 base capital is build-period burn above a 40% build-phase run (P3-CLM-AB004) |
| Full-time departments and management layers | PR #87 already removed most of them (F3 three core) | Already challenged in PR #87; the effect is small (~3%) | Small |
| Dedicated infrastructure per capability | Unbound `infra_base` $150-600k/yr; per-tenant floors | Partly. Shared Echelon hosting does not exist yet (Unbound 07; PR #87 A06 $0-10k) | $0.1-0.5M/yr |
| Premature compliance spend | SOC 2, insurance and TPSP audit inside burn from month 1 | **Yes.** A buyer requires SOC 2 at contract, not before a partner exists (CHL-014). The TPSP audit is deferrable only until Unbound first processes a sponsor's payment instructions. From then on it is an annual obligation under CNV-PAY-001 (Revision 2) | $0.1-0.3M before the first contract |
| Large sales organization | Direct CAC $125k/sponsor; ER-4 burn $135k/mo | Partly. The partner-first design already lowered it to $40k | $0.05-0.1M |
| Traditional professional services | Onboarding $105k/sponsor ($35-325k) | Partly, until reusable packages (S6) exist | $40-100k per customer |
| Build treated as an un-amortized up-front cash lump | ER routes spread the build over pre-revenue months | Not wrong for S1/S2; **irrelevant for S3+**, where it is sunk | $1.6M base in ER-7 |
| Unbound vendor P&L ($5.44M/yr at 25k funds, of which ≈$4.4M is run cost) | 05a §2b | Conventional vendor floor (legal $200k, audit $120k, insurance $150k at sponsor scale) | Explains Unbound's $217/fund break-even at 25k funds |

**What is *not* a conventional-organization artefact, and stays:**
- SOC 2 at contract;
- a second maintainer or contracted code approvers before regulated reliance (CNV-PLT-010, CNV-GOV-009). Segregation of duties under CNV-PLT-010 (two approvers, neither the author; two-person break-glass) cannot be evidenced by a one-founder operator. The lean run as modelled is not SOC-compliant unless it pays for contracted approvers year-round. The cost is pending in the model (P3-CHL-REV3004, P3-CHL-REV3022);
- insurance limits that buyers set;
- Nacha TPSP obligations under ratified CNV-PAY-001: the annual Rules compliance audit and risk-based fraud monitoring, once Unbound processes a sponsor's payment instructions;
- counsel on the payment functions Unbound performs (the TPSP role itself is set by CNV-PAY-001; Revision 2: this line previously read "counsel on payments and TPSP status");
- the sponsor's reserved decisions;
- the founder's time.

PR #87 reached the same conclusion: the binding constraints are legal and assurance obligations and buyer price, not organizational habits (SRC-002 report 01).

## 4. Double-counting and modelling issues found (detail in [03](03-capital-requirements-reconstruction.md))

1. **Build-period burn.** ER-7 charges the full $110k/month during the 15 build months as well as the $1.6M build ($1.65M + $1.6M). If the build is done by the same people the burn pays for, part of it is counted twice. At a 40% build-phase run, base capital falls to $4.67M.
2. **Channel share counted twice (possible).** ER-7 revenue per customer ($300k) is already net of a 30% channel share. Yet ER-7's variable-cost share is 0.30, against 0.15 for direct licensing (ER-4). If the extra 0.15 duplicates the channel share, ER-7 base is overstated by $0.33M ($5.33M). The intent is not documented (P3-CLM-AB005, hypothesized).
3. **G0-G1 added to ER-7.** $6.5M = $1.0M (G0-G1) + ER-7 P50 $6.0M − $0.5M build reuse. If the G1 pilot is ER-7's first customer, more than $0.5M overlaps. If ER-7 starts only after G1, CHL-085's sequential reading holds. Both readings are defensible; the report does not show which one applies.
4. **G1 $1.0-1.5M cannot contain the build.** A live pilot of the ledger, migration and eligibility module needs most of the $1.1-2.4M MSP. So G1 implicitly assumes a working module, which is the S3 premise of this track.

## 5. Every removed cost: replacement mechanism, residual risk, evidence required

| Removed or reduced cost | Replacement mechanism | Residual risk | Evidence required |
|---|---|---|---|
| Build capital (S3+) | Sunk. Shown in the economic view and excluded from incremental cash | Hidden scope: the MSP excludes deferred scope ($0.6M) and full scope ($3.6-5.2M) | A ledger of hours and cash actually spent (P3-GAP-AB002); an acceptance test of the MSP scope |
| Market-rate CEO/CTO from month 1 | Founder unpaid or below-market cash; economic cost shown | Key-person risk; founder burnout; buyer vendor-viability objection (CHL-015) | Second maintainer contracted; escrow; owner's runway statement (P3-GAP-AB006) |
| Sales organization | Founder-led selling plus the partner's sales force | Partner captures margin (30-50%, CHL-084); channel conflict | V-6 term sheet with share, exclusivity and support split |
| Support FTE | Partner first line; vendor second line | Partner refuses first line or demands 24x7 SLAs | Partner term sheet (P3-HYP-AB002) |
| SOC 2, insurance and TPSP audit before contract | Bind at a signed term sheet; automated evidence collection before it | A procurement delay of 3-12 months at contract (Type 2 needs ≥3 months of observation) | Partner procurement checklist; broker indications (P3-GAP-AB001) |
| Dedicated infrastructure per capability | Managed PostgreSQL modular monolith (CNV-ARC-001); S7 sharing | Per-tenant isolation floors (CHL-064); sharing saves cash only with a second paying product | Tenant-profile cost test; a second Echelon product with revenue |
| Professional-services implementation | Transitus phase 1 + reusable packages (S6) + prepaid implementation | Incumbent exports not obtainable (V-4); private-benefit risk in prepaid fees | V-4 rehearsal; second implementation at ≤40% of the first's hours (P3-HYP-AB004) |
| Echelon commercial licence | Intra-owner grant, so cash ≈ $0. Echelon Foundry owns all property it makes (OD-P3-01), so the licence chain is internal | Buyers still require written terms, escrow and a second maintainer (A03, A08) | Executed licence terms (PR #87 M-02) |
| Management and coordination layers | One operational model (PR #87) | Small effect; December capacity still binds once live administration exists (not in licensing) | Not material for licensing |

## 6. Minimum capital to commercialize an already completed Unbound

The numbers below assume S3, partner channel and the lean structure. They come from the staged scripts in [data/evidence/AB/staged.py](data/evidence/AB/staged.py), on Phase II ER-7 revenue (3 customers a year at $300k net of channel; 8% churn).

| Measure | Low | Base | High | Comment |
|---|---|---|---|---|
| Cash to first invoice | $0.25M | $1.00M | $3.51M | High = 24 months to contract, full assurance stack, 40% contingency |
| Cash to self-sufficiency (deepest deficit) | $0.28M (payback month 20) | **$1.47M** (payback month 64) | not finite in 120 months | High revenue case; bounded by kill rule. **Revision 2:** superseded by the model's corrected figure in [16](16-capital-efficient-market-entry.md) §1 (P3-CHL-REV1038) |
| Fully loaded (economic) to self-sufficiency | $0.53M | **$2.20M** (payback month 75) | not finite | Founder at market |
| Base costs with 1 customer a year | — | $2.2M; no payback | — | Throughput is the dominant driver |
| High costs with base revenue | — | — | $6.6M; no payback | Conventional-scale run rates bring back Phase II magnitudes |
| Capital at risk under the month-24 kill rule (adverse) | — | ≈$0.7M | ≈$1.2-1.7M | Development, compliance, legal and 24 months of pre-contract run plus contingency. **Revision 2:** superseded by the model's kill-rule results ("cash at risk if paused") in [14](14-commercial-sequencing.md) §6 and [19](19-sensitivity-and-stress-analysis.md). The clock now starts at the cost-center month (OD-P3-03, OD-P3-04) and the definition is open (P3-DEC-MOD001) |

**Revision 2 (model revision 2).** The paybacks in this table (months 20, 64 and 75) come from AB's staged scripts and are superseded. In the revised model the base case has no cash payback within 120 months under either registry mode, and A3 pays back only in the favourable case, at month 26 (`key-figures.md`).

**Drivers, in order:**
1. Time to first contract and customers per year: partner existence, V-6.
2. Fixed run rate: assurance, insurance and engineering maintenance.
3. Net revenue per customer after channel share and variable cost.
4. Founder cash draw.
5. Hardening scope.

The build is not among the top three once it is sunk.

**Comparison with Phase II.**
- ER-7 base, with the build: $5.66M.
- Without the build, at Phase II burn: $4.06M.
- Without the build, at lean burn: $1.27-1.47M.
- With PR #87's "Unbound exists" servicing view: $1.35-2.8M. That figure is for administration, not licensing (SRC-002 report 11 §7).

The two independent reconstructions agree on order of magnitude: **low single-digit millions fully loaded, about $1-1.5M cash in the base case, and well under $0.5M only if a partner signs early and pays.**

**Revision 2 (model revision 2).** This conclusion no longer holds. The model now adds TPSP obligations, control operations, the governing M1 registry, a 6-12 month go-live lag and a $75-325k first conversion. On that basis S3 cash to the first invoice is $1.83M base ($384k-$6.63M; revision 3; revision 2 gave $2.12M), and no sequence reaches cash self-sufficiency within 120 months in the base case unless the sponsor performs the deep review (partner-book sequence only) ([16](16-capital-efficient-market-entry.md); [14](14-commercial-sequencing.md)).

## 7. Cash versus fully loaded

**Cash** is what leaves Echelon Foundry's bank account. **Fully loaded** adds three things:
- the founder's time at market ($190-273k a year);
- a capital charge (5-15% of cash deployed);
- the sunk build, when the question is "was it worth it" rather than "what more must be spent".

On the base path from S3, the founder's economic cost over the 21 months to first invoice is about $0.39M, roughly a quarter of the fully loaded total. Across the cases the founder's share is 15-35%. **Fully loaded cost is about 1.5-2.2 times cash, about 1.7 times in the base case.** A plan that reports only cash understates the economic cost by that much.

## 8. What would change these conclusions

- V-6 finds no partner: the channel revenue assumptions fail and direct licensing applies (CAC $125k; ER-4).
- A partner demands vendor-run first-line support or 24x7 SLAs: support rises to 1-2 FTE ($0.1-0.2M a year).
- Sponsors' auditors require SOC 1 Type 2 for the fund ledger: add $20-120k a year plus its observation period (P3-GAP-AB005). TPSP status is not a contingency. Ratified CNV-PAY-001 makes Unbound a TPSP, so the annual Nacha Rules compliance audit and fraud monitoring belong in the base run. Counsel is still needed on the functions Unbound performs (P3-GAP-AB003).
  - **Revision 2 (2026-11-26; P3-CHL-REV3019, P3-CHL-REV1026):** this bullet previously read "Counsel finds the vendor is a Nacha TPSP in the partner-originated model and sponsors' auditors require SOC 1: add $70-170k a year".
- Insurance quotes for $5M limits come in above $160k a year (P3-GAP-AB001).
- Hardening turns out to be a material rebuild: S3 behaves like S2.
