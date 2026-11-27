# 00 — Executive findings: zero-based operational economics of Unbound

Date: 2026-11-27. **Research, not legal, tax or investment advice; not a launch or expenditure authorisation.** Every number is a model result from labelled inputs. **Nothing is measured operational performance.** Reviews were adversarial agent exercises by the same model family, not professional assurance.

## The answer in one paragraph

The previous estimate (≈ $1.9B break-even at 20 bps; ≈ $3.8M opex) **was built wrongly but lands in roughly the right place for full administration**. Rebuilt from 183 activities, 63 control obligations, measured public-data sizes, published cloud prices, and a queue simulation — then corrected after 118 adversarial findings — full administration costs **$3.89M at the original's operating point (7,695 accounts, 5 sponsors) versus the original $3.85M**. The break-even is **≈ $1.85B** at $250k balances with $500M sponsors (Monte Carlo P50 $2.0B, P10-P90 $1.4-4.1B). The composition is different: the original's three salaried executives, flat $0.3M AI oversight, $25 "infrastructure" and double-counted build amortisation are replaced by a four-engineer platform team, peak-driven compliance, ~$145k of recurring work per sponsor, and fuller assurance and insurance. **A materially smaller operation is sustainable only as licensing priced per account, or with large sponsors, high balances and engineering shared across Echelon products.** An early draft of this research concluded the original was 2-3× too high; review overturned that, and the reversal is preserved.

## Headline numbers (PG-HNW programme, $250k mean balance, deployment C1)

| AUA | Licensing with support (CFG-2) cash | Full administration (CFG-5) cash / allocated / standalone | Dedicated FTE (CFG-5) |
|---|---:|---|---:|
| $100M (1 sponsor) | $1.40M | $1.83M / $2.02M / $2.81M | 5 |
| $250M (1 sponsor) | $1.42M | $2.00M / $2.19M / $2.98M | 6 |
| $500M (1 sponsor) | $1.44M | $2.20M / $2.39M / $3.18M | 8 |
| $1B (2 sponsors) | $1.62M | $2.86M / $3.05M / $3.84M | 13 |

## Answers to the required executive questions

**1. Why did the previous model estimate $3.8M?** $2.5M fixed (three salaried executives $606k, 31 non-personnel lines and contingency $646k, an "MSP platform charge" $680k that included $388k of build amortisation, $0.3M flat AI governance and oversight, and a $59k unexplained residual) + 5 sponsors × $43.7k + 7,696 accounts × $146.77 ([02](02-existing-model-reconstruction.md)).

**2. Which assumptions are defensible?** Loaded labour rates; event frequencies as anchors; the variable cost per account (independently corroborated: ~$142 and ~58 minutes at scale versus $146.77 and 52.8); the existence of SOC, insurance and audit costs; the total at its own operating point.

**3. Which should be rejected or revised?** Build amortisation in operating cost (double counted); flat $0.3M AI oversight; $25 "infrastructure" (an account-maintenance placeholder; real cloud cost ≈ $12.6k/yr floor + $0.10-0.20/account); 0.75 utilisation stacked on productive hours; Echelon share and licence as standalone costs; salaried controller double-counted with event minutes; the $316k registry's 1.0 FTE steward; equal per-sponsor cost regardless of size; the superseded MD-1 comparator ([03](03-cost-assumption-audit.md)).

**4. Minimum viable annual cash operating expenditure?** **≈ $1.40M** (licensing with support); **≈ $1.8-2.0M** for full administration of a first $100-250M sponsor. Plus one-time cash ≈ $0.57M and first-year capital of **$2.6-4.3M** ([17](17-revenue-models.md)).

**5. Minimum viable fully allocated economic expenditure?** ≈ $1.6M (licensing); ≈ $2.0-2.2M (full administration) — founder time at $200/h and Unbound's share of shared Echelon resources add ≈ $0.19M.

**6. Standalone replacement cost?** ≈ $2.4M (licensing); ≈ $2.8-3.2M (full administration, $100-500M); ≈ $3.8M at $1B.

**7. What cannot be automated?** Reserved sponsor decisions (Tier-2 grants, declines, delegations, policy, sign-offs); independent payment release and manual-journal approval; sanctions true-match disposition and OFAC reporting; death, incapacity and disputes; fraud investigation; complex gifts; external audit and SOC examinations; incident command; author-plus-two code approval. Agents prepare evidence; they are not controls ([05](05-activity-elimination-and-automation.md), [06](06-human-control-obligations.md)).

**8. Productive human hours by scale (full administration):** ≈ 5,100 vendor hours at 100 accounts; 6,100 at 1,000; 10,400 at 5,000; 15,600 at 10,000; 105,000 at 100,000; 971,000 at 1M ([10](10-workload-and-capacity-model.md)).

**9. When is the first dedicated employee required?** From the first sponsor: **engineers (4) and a compliance owner**, set by platform workload, change-approval control and on-call — not by volume. The first dedicated **operations** employees come at ≈ 2,000 accounts (≈ $500M at $250k) ([11](11-staffing-thresholds.md)).

**10. Each additional employee?** Operations 3/4 at 5,000/7,500 accounts; compliance 2/3/4 at 1,000/3,500/5,000; finance at 5,000 and 7,500; controller at 7,500; independent authorizer only at 100,000; commercial at 5,000. Totals: 6 FTE at 1,000 accounts, 13 at 5,000, 23 at 10,000, 152 at 100,000.

**11. Minimum independent control coverage?** Two named, trained persons in each of initiation, independent release, reconciliation and close sign-off; three engineers (author + two approvers); a compliance owner and backup. With sponsor personnel holding delegate, releaser and sign-off seats, Echelon needs no dedicated full-time *control* staff — but two-person payment authorization and independent reconciliation are auditor and contractual expectations, not law ([06](06-human-control-obligations.md)).

**12. Cost of administering $100M / $250M / $500M / $1B?** Full administration $1.83M / $2.00M / $2.20M / $2.86M cash; licensing with support $1.40M / $1.42M / $1.44M / $1.62M (sponsor carries 2,000-7,300 hours).

**13. Break-even at 20 bps?** Full administration, $250k balance, $500M sponsors: **≈ $1.85B cash and allocated; ≈ $2.85B standalone**; Monte Carlo P50 $2.0B. With $1B sponsors $1.6B; $250M sponsors $2.85B; sponsors of $100M or less never ([18](18-break-even-analysis.md)).

**14. How does it change with average balance?** $1.3B at $1M balances; $1.4B at $500k; $1.85B at $250k; ≈ $10B at $100k; never below ≈ $50k. Retail and payroll programmes cost 10-28× an AUA fee.

**15. Beneficium without customers?** ≈ $58k (public directory) to $93k (continuous monitoring) to $132k (automated verification), 0.25-0.67 FTE-equivalent; infrastructure under $3k ([13](13-beneficium-public-data-economics.md)).

**16. Beneficium supporting grant processing?** With human exception verification: $166k at 10,000 active recipients, $481k at 100,000; with payment enrolment $208k and $896k ([14](14-beneficium-verification-economics.md)).

**17. Can public charity intelligence run without dedicated staff?** Yes for directory and continuous monitoring (fractional, ≈ 300-450 h); no for verification above ≈ 10,000-50,000 active recipients.

**18. Which Unbound requirements create unnecessary recurring cost?** Pre-delegation batch approval (CNV-GRT-001); Tier-2 triggers without determination reuse (CNV-GRT-011); three overlapping sampling regimes; layered reconciliation attestation; daily NAV sampling of externally computed values (CNV-FIN-005); annual affiliation attestation; the default 72-hour hold (CNV-PLT-011); per-sponsor close and audit work without a shared workbench; 24-48 h compliance SLAs through December ([21](21-requirement-economic-impact.md)). No mandatory control is proposed for removal.

**19. Which responsibilities should remain with sponsors?** Reserved grant decisions, board delegations and policy adoption, reserved-authority appointments, payment release through the sponsor's bank, monthly close sign-off, Form 990/Schedule D signing, state registrations, investment policy, SOC report and complementary-control review, funding transfers.

**20. Which capabilities should be shared across Echelon?** Platform engineering (the largest saving if ≥ 2 products are in production), the assurance programme, observability, identity, charity intelligence (Beneficium), data integration (Transitus), entity accounting and legal administration. Today most of these do not exist; sharing is prospective.

**21. What economic advantage does Unbound actually possess?** Against conventional administration, about **2-3× lower cost per account at scale** ($142 vs ~$400), from workflow design and deterministic automation (97% of events complete without a person). Against the previous AI-native estimate, **no material advantage** except below ~4,000 accounts (≈ $0.6M lower overhead). AI assistance is net negative at small scale; cloud cost is immaterial.

**22. Which advantages are theoretical and which evidenced?** Evidenced: public-data sizes; cloud and AI prices; legal mandate classifications; Echelon output volumes (not effort). Theoretical: every exception rate and handling time, the 97% automation share, AI savings, shared components, migration speed.

**23. What could invalidate the model?** Exception rates or handling minutes 50% higher (≈ +$0.5M); engineering above four FTE; small sponsors needing full per-sponsor effort; fees below 20 bps; founder capacity; auditors refusing reliance on automated controls; key-person concentration in due diligence.

**24. Minimum commercially viable customer?** As a *first* customer: full administration fees of ≈ $1.8-2.2M a year (≈ $0.9-1.1B at 20 bps, single sponsor, balances ≥ $250k), or licensing revenue covering ≈ $1.4M a year (break-even ≈ 41,500 accounts at $150 per account, ≈ 13,200 at $250). As an *additional* customer on an established platform: ≈ $185k a year (≈ $95M at 20 bps, or a minimum fee).

**25. What to measure first?** Minutes and exception counts per activity ID for the top 15 activities; Tier-2 trigger incidence and review minutes; engineering hours per accepted change; per-sponsor close and audit hours; December queue age by pool; unidentified receipts and payment returns per 1,000 transactions ([25](25-evidence-gaps-and-validation-plan.md)).

## What would have to be true for the original $1.9B to remain correct

It is approximately correct **for full administration** if: mean balances ≈ $250k; sponsors average ≈ $500M; 20 bps is realised; exception rates and handling minutes hold at the inherited anchors; four engineers and a two-person compliance function are needed; and no engineering is shared across Echelon products. It would be wrong if any of those moves materially — and it was never right for its stated reasons.

## What would have to be true for a materially smaller operation to be sustainable

Any one of: **licensing priced per account** ($150-250) with the sponsor operating (break-even ≈ 13,000-41,000 accounts, ≈ $1.4M floor); **sponsors ≥ $1B with balances ≥ $500k** (full-administration break-even ≈ $1.3B); or a combination of **measured exceptions ≥ 40% lower, founder ≥ 1,200 h, low-end quotes and cheaper infrastructure** (≈ $1.39B), plus **platform engineering shared with other Echelon products in production** (a further ≈ −$0.3B, inference). Below about $1B AUA, full administration at 20 bps does not cover its own floor on any modelled combination.

## Repository

Reports [01](01-methodology.md)-[27](27-final-recommendations.md); registers in `data/registers/`; inputs in `data/model-inputs/`; generated outputs in `data/model-outputs/` (byte-reproducible); model and tests in `model/`. Ledger: [research-ledger.md](research-ledger.md).
