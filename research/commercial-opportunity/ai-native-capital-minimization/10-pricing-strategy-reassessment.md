# 10: Pricing strategy reassessment

**Pass:** COM (part 1), integrated in model section 11. **Data:**
- [`sponsor-value.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/sponsor-value.csv) (5 archetypes + top 30 sponsors);
- [`pricing-structures.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/pricing-structures.csv) (210 rows: six structures).

**Integrator conclusions**
- **20 bps remains the working objective** for:
  - small and mid-balance books;
  - books already outsourced at 25-40 bps (e.g. the U.S. Charitable Gift Trust, where Ren earns about 40 bps);
  - high-volume, small-balance books such as National Christian Foundation;
  - sponsors that commit to retiring DAF staff and systems.
- **It is not value-defensible for books averaging $1M or more per account.** There, equivalent-scope value is about 5-10 bps.
  - The median value-based maximum across 24 winnable top-30 sponsors is 7.3 bps.
  - It reaches 19.3 bps only if sponsors cut staff.
- **$737 per account (Morgan Stanley GIFT) is not a market-wide ceiling.**
  - It buys a narrow scope: a 0-employee bank-channel programme where Morgan Stanley earns separately.
  - Observed per-account prices run from $429 to $1,198.
  - At high balances, though, the value limit is real.
- **Correction to the previous study:** its recommended tariff ($150 per account + 7.5 bps) leaves only 3 of 24 winnable sponsors better off. "$350 per account + 3 bps, capped at 20 bps" leaves 16, and a 50% value share leaves 22.
- **Asset-weighted, the accepted structures earn about 6-7 bps on top-30 assets, not 20.** In the model:
  - F5 at 7 bps never breaks even below $3.8B at any balance.
  - At $250k balances, $350 + 3 bps (cap not modelled) breaks even at $1.56B.
  - A $250 per-account floor on 20 bps lowers break-even to $0.93B.
- **Efficiency does not have to be passed through** where value supports the price. Service, reliability, transparency and portability are the competitive grounds.
- **Safeguards stay in every structure:**
  - payout-neutral fee base;
  - cost-based complex-gift and foreign-grant fees;
  - floors waived in wind-down;
  - payment rails passed through at cost.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## COM summary

**Group COM, 2026-11-25. Commercial: pricing, sponsor value, incremental offers, customer-funded development, incumbent replication.** Labels [S]/[A]/[D]/[E]; evidence EV-COM-001..045, assumptions A-COM-001..016. Same-model reasoning; not validated with any buyer.

**Five most consequential findings**
1. **$737/account (MS GIFT) is not a market-wide ceiling, but the previous verdict on high-balance books largely survives for a different reason.** MS GIFT's 18.5 bps buys a narrower scope (0-employee bank channel; MSSB separately earns 7 bps admin plus up to 1% advisory and owns the donor relationship), and observed per-account prices run $413-$1,198 (USCGT $429, Stifel stack $1,142, CAF America grant-admin-only $1,198) [S, EV-COM-001..005]. However, on **equivalent scope** the value a servicer delivers to a high-balance sponsor is about **$560-1,830 per account but only 5-10 bps**; median value-based maximum price across 24 buyable top sponsors is **7.3 bps (base)** and **19.3 bps** only if sponsors actually shed the assumed share of their own DAF opex [D].
2. **20 bps is defensible as value-based pricing in three places only:** (a) sponsors that already outsource at >=20 bps (USCGT 40, RCF-like 38; RJ ~18-20 borderline); (b) sponsors that will actually retire DAF staff/systems (faith federations and CFs whose DAF opex is 100-200 bps; value_high 40-68 bps) - i.e. a headcount decision, not a price decision; (c) small/mid-balance books ($100-400k) where per-account value is close to 20 bps x balance. For $1M+ balance books 20 bps flat ($1,500-5,000/acct) exceeds equivalent-scope value in every base case.
3. **Per-account-led and value-share structures dominate flat 20 bps, but they reveal that 20 bps is not the book-weighted value of the top market.** Value-share leaves 22/24 buyable top sponsors better off and covers servicer marginal cost in all; $350/account + 3 bps (capped at 20 bps) leaves 16/24 better off; flat 20 bps 1/24; the earlier $150 + 7.5 bps tariff only 3/24 (its bps component is too high at $1M+ balances). Book-weighted, the acceptable tariffs earn **6.3-7.3 bps** on top-30 assets, not 20. Keep 20 bps as the objective for small/mid-balance and already-outsourced books; it is not reachable across high-balance books without the sponsor retiring its own DAF staff.
4. **Incremental products mostly have potential, not demonstrated, demand; the demonstrated ones (verification data, disbursement, portals, migration) are contested or carry the highest disconnected-architecture risk.** Migration/onboarding tooling and eligibility services are the two that both have paid precedents and are components of the full platform.
5. **Incumbent replication: understanding is easy, enterprise implementation is not - but it is not impossible.** Individually, five of seven advantages are copyable within 6-24 months under conditions favourable to the incumbent. The conjunction (single ledger + evidence-by-default + portability + per-account pricing) is moderately durable against multi-lineage incumbents (48-72 months to transform an installed base) and **not durable** against a funded greenfield sub-brand or acquisition (18-30 months).

**Largest gaps:** no executed servicer contract or price sheet; no sponsor cost-by-activity data (value relies on [A] replaceable shares and an un-time-studied activity model); no observed design-partner fee in DAF; no buyer willingness-to-pay evidence.

## Part 1a: pricing logics distinguished

| Logic | What sets the price | DAF evidence | Fits a servicer at 20 bps? |
|---|---|---|---|
| **Cost-based** | Servicer cost + margin | Prior model: AI-native ~$89/acct market mix [D from A], conventional ~$262 | Gives ~3-8 bps at $400k balances: leaves value on the table and invites 'pass the savings' demands |
| **Competitive** | Incumbent price for same scope | Ren 18.5 bps/$737 (MS GIFT), 40 bps/$429 (USCGT), TIFIN 30 / 10-20 bps list | 20 bps = parity at ~$400k, discount below $250k, premium above $1M |
| **Value-based** | Buyer's avoided cost (equivalent scope only) + quality value | This study: 5-10 bps base at high balances; 18-40 bps where sponsor already outsources at that level | Defensible only where avoided cost is real (see 1c) |
| **Asset-based (bps)** | AUA | All donor schedules; MSSB 7 bps; USBFS tiers | Aligns with donor fee; mismatches account/transaction-driven cost; market risk |
| **Per-account** | Accounts | $100-360 donor minima; Ren $413-814/acct realised; NC ABLE $5/acct state fee [C] | Matches cost shape; can deter small accounts unless capped |
| **Activity-based** | Events (grants, complex gifts, wires, foreign DD) | MS GIFT 2019 $2,000-3,500 per 'other grantee'; NCF $25/wire; RCF extraordinary-service fees | Right for genuinely exceptional work; must not deter grants (charitable-purpose safeguard) |
| **Hybrid** | Per-account + low bps + activity fees, with floors/caps | Report 05 tariff $100-200 + 5-10 bps; USBFS bps + $60k minimum + CPI | Preferred form, but per-account-led (~$350 + 3 bps, cap 20 bps); report 05's bps share is too high for $1M+ books |
| **Value-share** | Share of measured avoided cost | No DAF precedent found; RCF->Ren 95-98% fee share is a related-party revenue share | Best alignment, but needs a measured baseline (time study) and audit rights |

**Safeguards preserved in every structure modelled:** payout-neutral base (approved-unpaid grants excluded from billable assets; RC-SE-002); complex gifts, foreign/ER grants and wires as cost-based activity fees, never inside the asset fee (RC-SE-007) and never applied in a way that deters an acceptable grant; per-account floors waived for accounts in wind-down after a final grant and capped so they never exceed the account's balance-based fee by more than the floor (RC-SE-001); payment rails passed through at cost (RC-SE-003); no fee on grant dollars.

## Part 1b: is $737/account a market-wide ceiling? (challenge)

**No.** The previous study used Ren at MS GIFT ($737, 18.5 bps) as the per-account anchor and concluded 20 bps is 2-7x too expensive at high-balance programs. Five corrections:
1. **Scope is narrower than a self-operated sponsor's.** MS GIFT has 0 employees; MSSB is paid a separate 7 bps admin/platform fee by donors and earns advisory fees up to 1.00% on the same assets; financial advisers own onboarding, donor relationship and much service [S, EV-COM-002]. Ren's $737 buys back-office administration for a channel that has already absorbed front-office cost.
2. **Concentration and scale.** $8.1B across 21,800 accounts from one contract; realised take below the donor TPA first tier (27 bps) implies custom deals on very large accounts [S/D]. A single-contract price for the largest outsourced book is a volume price, not a ceiling.
3. **Other observed per-account prices are higher:** Stifel full stack $1,142; Bradley $1,140; CAF America grant administration alone $1,198; GiveClear/TIFIN $815; RCF $814 [S]. And lower: USCGT $429. Per-account price is not stable either; it rises with balance and grant intensity.
4. **Sponsor revenue context.** Sponsors keep 30-54 bps of realised donor fees in most groups (Fidelity 22.9, JCF 42.2, RCF 38.7 realised; CFs ~30-60 estimated) [S/E]; a 20 bps servicer price is 40-65% of that revenue, which matters for affordability but is not itself evidence of value.
5. **Alternatives differ by buyer:** in-house (nationals spend 14-27 bps all-in), software-only (0.5-9 bps) plus own staff, BPO (Ren), or a channel owner absorbing cost. A buyer's reservation price is its best alternative, not MS GIFT's contract.

**But the conclusion largely survives on value grounds** (1c): the equivalent-scope work a servicer replaces at a $1M+ balance sponsor is worth roughly $600-1,800 per account, i.e. 5-10 bps. The defensible per-account price for high-balance books is therefore **above $737 (often $1,000-1,700)** but **well below 20 bps** ($1,500-5,000).

## Part 1c: sponsor value model and archetypes

**Method** (`scripts/sponsor_value.py`, reproducible). For each sponsor: donor-fee revenue (realised where audited; else schedule at mean balance x realisation 0.6, calibrated 0.38-0.68) [S/E]; DAF opex = 990 opex ex investment mgmt x DAF asset share, less advertising/professional fundraising [S/D]; **value delivered** = min(top-down: DAF opex x replaceable share [A-COM-001], bottom-up: accounts x conventional equivalent-scope cost by balance archetype x 1.35 overhead + $100k sponsor-level + avoided software [D from A]); `value_high` = top-down unbounded (only if the sponsor actually sheds that share). For 0-employee outsourced sponsors value = current vendor payment. Sponsor net value = value - oversight ($60k + $7.5/acct) - migration ((150k + $20/acct)/5) - price. Servicer contribution = price - AI-native marginal cost from the previous model (fixed company cost excluded).

| Archetype (median inputs) | Assets | Accts | Avg bal | Donor-fee rev (bps) | DAF opex (bps) | Value: base / high (bps) | Value $/acct base | Max value price base / high (bps) | 20 bps = $/acct | Sponsor net @20bps base / high | Net @$737 base | Net @$150+7.5bps base | Net @value-share | Servicer contribution @20bps |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ARCH-independent-national (median of n=5) | $2161.38M | 2266 | $953,830 | 36.0 | 22.1 | 7.2 / 12.1 | $684 | 6.6 / 11.6 | $1,908 | $-2.89M / $-1.82M | $-0.24M | $-0.53M | $0.60M | $4.00M |
| ARCH-faith-federation (median of n=9) | $647.34M | 1045 | $619,466 | 36.0 | 149.3 | 10.3 / 67.2 | $636 | 8.7 / 65.6 | $1,239 | $-0.73M / $2.95M | $-0.21M | $-0.08M | $0.04M | $1.08M |
| ARCH-large-CF (median of n=9) | $1250.27M | 1342 | $931,649 | 54.0 | 158.6 | 7.6 / 47.6 | $708 | 6.8 / 46.7 | $1,863 | $-1.66M / $3.34M | $-0.14M | $-0.29M | $0.22M | $2.25M |
| ARCH-mid-CF (median of n=43) | $439.52M | 557 | $789,080 | 54.0 | 140.9 | 10.2 / 42.3 | $803 | 8.0 / 40.1 | $1,578 | $-0.53M / $0.88M | $-0.06M | $-0.06M | $0.02M | $0.72M |
| ARCH-advisor-program (median of n=9) | $1105.13M | 4343 | $254,462 | 38.7 | 38.7 | 9.5 / 9.5 | $242 | 8.2 / 8.2 | $509 | $-1.30M / $-1.30M | $-2.29M | $-0.57M | $-0.65M | $1.64M |

Reading: the **base** case (bottom-up bound) says a CF or faith federation would be worse off at 20 bps; the **high** case says it would be better off **only if** it cut DAF operating staff and systems by the assumed share (30-45%) - an organisational choice the servicer cannot make for it. Advisor programmes (0-employee, median $1.1B, vendor median $1.05M, 9.5 bps) already buy cheaper than 20 bps; note many of them buy software-only and staff ops at an affiliate, whose cost is not visible on the 990 (gap). CF 'margin now' is negative under asset allocation because CF opex funds community work: fee revenue is not DAF-only profit.

## Part 1d: named top sponsors (from sponsor-model-economics.csv / sponsor-economics.csv)

| Sponsor | Group | Avg bal | Fee rev bps (kind) | Current DAF vendor | Value base / high bps | Value $/acct | Max price base bps / $acct | Max price high bps | Net @20bps base / high | Net @$737 | Net @$150+7.5 | Net @tiered |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Morgan Stanley Global Impact Funding Tru | outsourced_0emp | $370,910 | 22.8 (pass_through_assumed) | $14.93M | 18.5 / 18.5 | $685 | 18.0 / $669 | 18.0 | $-1.58M / $-1.58M | $-1.48M | $5.26M | $8.14M |
| The Us Charitable Gift Trust | outsourced_0emp | $102,898 | 71.3 (pass_through_assumed) | $4.43M | 40.1 / 40.1 | $413 | 38.2 / $393 | 38.2 | $2.01M / $2.01M | $-3.70M | $1.78M | $1.53M |
| Raymond James Charitable Endowment Fund | affiliate_inhouse | $186,943 | 36.0 (schedule_estimated) | $0.00M | 19.2 / 21.4 | $358 | 18.1 / $339 | 20.3 | $-0.40M / $0.07M | $-4.49M | $0.54M | $0.95M |
| American Endowment Foundation | independent_national | $485,312 | 42.0 (schedule_estimated) | $1.08M | 10.4 / 16.1 | $506 | 10.1 / $489 | 15.8 | $-7.68M / $-3.27M | $-3.96M | $-0.40M | $1.55M |
| Jewish Communal Fund | faith | $620,010 | 37.6 (realised) | $0.42M | 9.0 / 11.5 | $560 | 8.6 / $531 | 11.0 | $-3.59M / $-2.81M | $-1.04M | $-0.43M | $-0.80M |
| Impactassetsinc | independent_national | $1,277,724 | 34.5 (schedule_estimated) | $0.23M | 8.3 / 48.9 | $1,059 | 7.9 / $1,007 | 48.5 | $-3.40M / $8.00M | $0.59M | $-0.22M | $-1.07M |
| Greater Horizons | independent_national | $707,489 | 36.0 (schedule_estimated) | $0.00M | 8.5 / 11.1 | $599 | 7.9 / $558 | 10.5 | $-2.62M / $-2.05M | $-0.55M | $-0.37M | $-1.19M |
| Greater Kansas City Community Foundation | community_foundation | $758,018 | 49.4 (schedule_estimated) | $0.00M | 8.1 / 18.8 | $614 | 7.6 / $573 | 18.3 | $-2.88M / $-0.40M | $-0.50M | $-0.44M | $-1.24M |
| The Chicago Community Trust | community_foundation | $2,279,115 | 31.8 (schedule_estimated) | $0.00M | 6.0 / 13.4 | $1,364 | 5.7 / $1,307 | 13.1 | $-6.49M / $-3.12M | $1.14M | $-1.10M | $-1.72M |
| Foundation For The Carolinas | community_foundation | $2,424,675 | 42.5 (schedule_estimated) | $1.15M | 7.5 / 29.5 | $1,828 | 7.1 / $1,731 | 29.1 | $-3.27M / $2.32M | $1.04M | $-0.25M | $-1.31M |
| Combined Jewish Philanthropies Of Greate | faith | $2,576,095 | 8.1 (realised) | $0.00M | 5.9 / 68.1 | $1,529 | 5.5 / $1,404 | 67.6 | $-2.96M / $9.70M | $0.53M | $-0.54M | $-1.71M |
| Natl Christian Charitable Fdn Inc | faith | $167,183 | 88.8 (realised) | $3.85M | 24.9 / 63.7 | $417 | 24.1 / $403 | 62.8 | $2.18M / $22.86M | $-10.68M | $4.06M | $4.87M |
| The New York Community Trust | community_foundation | $903,165 | 30.0 (schedule_estimated) | $0.00M | 7.7 / 21.3 | $700 | 6.9 / $621 | 20.4 | $-1.59M / $0.05M | $-0.16M | $-0.28M | $-1.02M |
| Columbus Foundation | community_foundation | $762,954 | 51.4 (schedule_estimated) | $0.34M | 8.5 / 17.9 | $648 | 7.6 / $578 | 17.0 | $-1.45M / $-0.36M | $-0.24M | $-0.22M | $-0.92M |

**Pricing-structure scoreboard across 24 buyable top-30 sponsors** (captives and the recently migrated excluded):

| Structure | Median price bps | Book-weighted bps | Median $/acct | Sponsors better off, base value (of 24) | ...if top-down value | Servicer covers marginal cost |
|---|---|---|---|---|---|---|
| S1_flat_20bps | 20.0 | 20.0 | $2,562 | 1 | 12 | 24 |
| S2_per_account_737 | 5.8 | 7.3 | $737 | 13 | 18 | 24 |
| S3_per_account_150_plus_7.5bps | 8.7 | 9.0 | $1,110 | 3 | 21 | 24 |
| S4_tiered_bps_floor | 13.8 | 9.0 | $1,610 | 3 | 20 | 24 |
| S5_value_share_50pct | 4.2 | 3.9 | $530 | 22 | 22 | 24 |
| S6_per_account_350_plus_3bps_cap20 | 5.7 | 6.3 | $734 | 16 | 22 | 24 |

Observations [D]: MS GIFT is better off switching only below ~18 bps ($669/acct after oversight/migration) - confirms parity, nothing more. USCGT (Ren at 40 bps) is the clearest 20-bps-value case (+$2.0M/yr net). AEF, JCF, Greater Horizons, GKCCF: base value 8-10 bps ($500-610/acct); 20 bps leaves each $2.6-7.7M/yr worse off; per-account $737 is near break-even; value-share leaves them +$0.8-3.2M. High-balance CFs (Chicago CT, FFTC, CJP): value $1,300-1,830/acct; $737/acct is affordable (+$0.5-1.1M), 20 bps ($4,500-5,200/acct) is not. NCF (custom in-house, 31,943 accounts, $167k balance) shows the opposite: 20 bps ($334/acct) is below base value ($417/acct) - small-balance high-volume books are where 20 bps is cheap.

## Part 1e: conclusions on 20 bps, passing efficiency, and competing on service

**Is 20 bps defensible as value-based pricing?** Yes, where avoided equivalent-scope cost >= 20 bps + oversight + migration: (1) currently outsourced books at 25-40 bps (USCGT-, RCF-, RJ-like; small/mid balances $100-250k); (2) high-volume, small-to-mid-balance in-house books (NCF-like, $150-400k balances) where per-account work is dense; (3) any sponsor that commits to retire DAF staff/systems (value_high median 19.3 bps). **No** for high-balance ($1M+) independent nationals, faith federations and CFs on equivalent scope (base 5-10 bps) - there 20 bps only works as a **book-level revenue objective delivered through a per-account tariff** ($1,000-1,700/acct) or a value share.

**Must we pass efficiency to customers?** Not by doctrine - value pricing captures the gap between our cost (~$89/acct AI-native, ~$170-220 high-value) and the buyer's avoided cost ($400-1,800). But three forces will push part of it through: (a) incumbent re-tiering at renewals (cheapest response, report 01 g); (b) charitable sponsors' boards owe donors reasonable fees and publish schedules - a sponsor that saves cost but keeps donor fees faces scrutiny; (c) the value-share floor/ceiling must be auditable. Plan for 30-50% of measured savings to reach sponsors (value-share 50% modelled) and protect margin through cost, not price.

**Competing on service, reliability, transparency, flexibility.** Where price parity holds (MS GIFT-like), switching gains are ~0 or negative after migration cost, so only non-price value moves buyers: measured grant turnaround, exception error rates, published control metrics, full-fidelity export, no termination fee, configurable policy without change orders. These are real but **unquantified** in public data; they cannot carry a price premium until measured at a design partner. The weakest claim is 'reliability': the entrant has no SOC history (incumbent-favoured).

**Recommended tariff (testable):** a **per-account-led hybrid** - about $350/account + ~3 bps, capped at 20 bps (S6; ~20 bps at $100-200k balances, ~10 bps at $500k, ~6 bps at $1-2M) - or a value share of measured savings for sponsors willing to baseline; this corrects report 05's $150 + 7.5 bps, whose bps component exceeds equivalent-scope value at $1M+ balances; activity fees at cost for complex gifts, foreign/ER grants and wires; optional value-share above a measured baseline with a cap at 20 bps; payout-neutral base; floors waived in wind-down. This keeps 20 bps as the working objective on the books where it is value-defensible and stops it from being the reason high-balance buyers say no.
