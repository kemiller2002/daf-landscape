# DAF servicing market entry at 20 basis points
Date: 2026-11-25. Status: initial research synthesis and reproducible scenario analysis; not a validated price quote or business forecast.

## Decision and scope
Owner-supplied working assumption: outsourced administration earns 20 bps annually on average eligible assets under administration (AUA), not investment management revenue. Sponsor retains legal ownership and reserved decisions; software-only licensing is a separate offer. Test 10–30 bps. Established providers demonstrate market demand, not Unbound profitability. No confidential former-employer information used.

## Market evidence
Existing research documents TIFIN Give's March 2025 ADV service fee generally 30 bps for accounts up to $1m and 10–20 bps above $1m, separate investment fees; historical disclosure, not current negotiated full-service price. RCF audited FY2024 payments to Ren $19.2255m under 98% of individual fundholder fees, not Ren total revenue. Unbound evidence backlog finds two outsourced administration contractor-payment observations $413–745 per fund-year, approximately 33–37 bps in its economic report, with scope and average asset denominators unverified. These are not equivalent contracts. Sponsor retail administration fees are not servicer revenue. See sources below.

## Model
Revenue = average billable AUA × bps/10000. Cost = fixed annual overhead F + variable cost v × account count N + sponsor-specific costs + transaction/exception costs not already included. Simplified scenario uses N=AUA/B (B average account balance), F=$750k, v=$75/fund-year, no additional costs; all assumptions, not observed. Break-even AUA=F/(r-v/B); target margin m requires AUA=F/((1-m)r-v/B). Nonpositive denominator means scale alone cannot achieve target. Avoid double counting platform cost, retained sponsor costs and pass-throughs. Fixed costs must include engineering, assurance, sales, support, insurance and management; separate startup capital, implementation costs and working capital.

| Fee bps | Break-even AUA | AUA at 25% margin |
|---:|---:|---:|
| 10 | $1200M | $2000M |
| 15 | $667M | $1000M |
| 20 | $462M | $667M |
| 25 | $353M | $500M |
| 30 | $286M | $400M |

At 20 bps and $200k average balance, $1B AUA yields $2m revenue, 5,000 funds, $1.125m modeled cost and $875k surplus (43.75%). With a 30% full-year asset shock and unchanged accounts/costs, revenue $1.4m, surplus $275k (19.64%). At $50k average balance the same $1B implies 20k accounts and $2.25m cost, a loss of $250k. At $25k average balance variable cost alone exceeds revenue. These are scenarios, not forecasts.

## Challenge against existing model
Unbound report 05a section 8 estimates staffed administration cost $192/$299 per fund at 10k funds (base/adverse platform scale), $153/$260 at 50k and $150/$256 at 100k. At 20 bps, 10k base/adverse cost implies minimum average balance $96k/$149.5k at break-even, $128k/$199.3k at 25% margin before excluded vendor costs. At 50k base/adverse, target balances $102k/$173.3k. Sponsor-retained decision costs ~$42–43 per fund are separate. Report 05 notes sales, build capex and assurance costs sit in vendor P&L rather than the staffed cost figure. Reconcile those costs before calling these margins. The lean $750k/$75 scenario is a challenge hypothesis, not a replacement for the prior model.

## Illustrative sponsor scale screen
FY2025 Schedule D year-end assets and counts from existing league table; revenue is hypothetical annualized run rate on year-end assets, NOT realized fee or average billable assets. Full conversion assumed solely to compare scale; no qualified leads, willingness to pay or available mandate inferred.

| Sponsor | EOY DAF assets | Funds | EOY assets/fund | 20 bps run rate |
|---|---:|---:|---:|---:|
| Jewish Communal Fund | $3.405B | 5061 | $672,825 | $6.810M |
| Raymond James Charitable | $2.325B | 11262 | $206,425 | $4.650M |
| Combined Jewish Philanthropies | $2.146B | 791 | $2,712,669 | $4.291M |
| Servant Foundation | $0.782B | 463 | $1,689,582 | $1.565M |
| Boston Foundation | $1.403B | 822 | $1,707,419 | $2.807M |
| Marin Community Foundation | $1.033B | 490 | $2,108,913 | $2.067M |

Community foundations often require non-DAF functionality and shared staff; high average balances do not establish low service complexity. Raymond James and Jewish Communal Fund are useful national/single-issue scale cases, not sales recommendations. Servant Foundation has fewer accounts but substantial grant flows; asset volatility and concentration matter. Avoid captive providers and recent migrations without evidence of buying opportunity.

## Research backlog
1. Rebuild vendor P&L bottom-up: role, loaded compensation, hours, coverage, assurance, insurance, cloud, payments, sales, implementation, migration, legal and startup runway. Compare lean, base and adverse; distinguish software-only and staffed offers.
2. Extract full sponsor league table including FY2024 fallback, beginning/end assets, contributions, grants, account counts, current vendors and migration signals. Calculate average-asset proxies separately; rank by attainable contract contribution, not AUA alone.
3. Verify incumbent contracts/ADV and audited payee disclosures; normalize scope, denominator, fees, retained sponsor staff, pass-throughs, minimums and tiers.
4. Model 10–30 bps, sponsor minimums, account/transaction mix, asset shocks, outflows, concentration, churn, sales cycles, onboarding cash flow and capital runway. Test 25% margin as exploratory, not approved.
5. Calibrate activity costs using public replay (recipient-level, not grant-level) and actual time study when available; never lower screening safety to achieve cost targets.
6. Evaluate price versus sponsor retained margin and charitable outcomes; avoid incentives to delay grants or retain assets unnecessarily.
7. Apply Clarity and EDF formally when available; falsify lean staffing, low variable costs, full asset conversion and equivalent service assumptions. No formal framework execution claimed here.
8. Transfer supported requirements implications to Unbound only through its governance. Distinguish architecture/design evidence from commercial activation gates.

## Sources (existing repository evidence, not freshly reverified primary filings)
- [DAF economics and distribution](../daf-economics-and-distribution-2026-11-11.md)
- [Sponsor financial flows](../batch-1b-sponsor-financial-flows-2026-11-12.md)
- [FY2025 league table](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2025-refresh.csv)
- [Sponsor prospect notes](prospect-profiles/sponsors-notes.md)
- [Unbound economics](https://github.com/kemiller2002/unbound/blob/9b38de47437d2be1e86ded3db856aaf0eefc9fed/requirements/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md)
- [Unbound cost tables](https://github.com/kemiller2002/unbound/blob/9b38de47437d2be1e86ded3db856aaf0eefc9fed/requirements/convergence/2026-11-24-master/05a-ECONOMIC-TABLES.md)
- [Public replay](https://github.com/kemiller2002/unbound/blob/9b38de47437d2be1e86ded3db856aaf0eefc9fed/requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md)

Conclusion: 20 bps is a useful market-led design constraint. AUA, account mix, contract scope and fixed overhead jointly determine viability; a single anchor sponsor could theoretically support a lean operation, but acquisition and actual costs are not demonstrated.
