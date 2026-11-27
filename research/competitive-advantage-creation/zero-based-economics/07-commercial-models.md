# 07. Commercial models, modelled independently

The six models share one cost engine, but each model bears different expenses and activities. Prices are reference values only ([`parameters.csv`](data/inputs/parameters.csv)); break-even prices and fees are computed independently of them. Licensing prices are never derived from asset-based fees.

| Model | What Echelon Foundry bears | What the sponsor bears | Revenue basis (reference) |
|---|---|---|---|
| **L Technology licensing** | Platform, assurance (SOC 2; SOC 1 from customer 3), insurance, maintenance, tier-2 support, onboarding configuration | All DAF operations and decisions, payment rails, own audit, migration validation | $24k per customer + $40 per account per year |
| **W White-label** | As L. The partner takes front line and sales (fewer founder hours per new customer) | As L, through the partner | $12k + $25 per account (wholesale) |
| **T Technology + limited operational support** | L plus exception preparation, attribution, reconciliation investigation, close preparation and SOC 1 (from customer 2), plus an operations-continuity rule | Decisions, rails, donor support, statements, reporting | L + $30 per account |
| **F Full-service administration** | T plus donor support, statements, reporting, account changes, fraud investigation, crime insurance, SOC 1 before the first client | Reserved decisions only, plus rails and own audit | 5–30 bps of assets |
| **C Shared charity intelligence** | Registry pipeline and API, national change review, source-rights review, subscriber support, SOC 2 (no ledger controls) | Nothing beyond the subscription | $6k per subscriber per year |
| **M Migration and onboarding** | Migration projects (Transitus): fixed 80–300 h + 1–6 min per account | Sponsor-side validation | $40k per project + $5 per account |

## Results (base, typical contracts)
| Model | Monthly burn at 0 / 1 customer | Marginal per customer (10→25, base; median) | Persistent cash break-even (mixed / anchor-first / all mid-size) | Founder hours | First employee (mixed) |
|---|---|---|---|---|---|
| L | $0.6k / $16.8k | $37k; $47k | 7 / 1 / 211 customers | 1,200 (full from customer 1) | 5 |
| W | $0.6k / $16.3k | $27k | 17 / 11 / never | 1,200 | 7 |
| T | $0.6k / $23.6k | $82k | 17 / 11 / never | 1,200 | 5 |
| F at 20 bps | $0.6k / $27.0k | $89k; $122k | 2 / 1 / 5 customers | 1,200 | 4 |
| C | $1.4k / $12.1k | ~$1.2k | 31 / 32 / 28 subscribers | 1,200 | none within 200 |
| M | $0.3k / $2.4k | ~$30k per project | 1 / 1 / 1 project | 310 at 0; 1,200 by 10 projects | 9 |

## Full-service administration by fee (persistent cash break-even; mixed sponsors)
| Fee | Customers | Assets | Fully loaded customers |
|---|---|---|---|
| 5 bps | never (within 400) | — | never |
| 10 bps | 5 | $0.67B | 7 |
| 15 bps | 2 | $0.33B | 5 |
| 20 bps | 2 | $0.33B | 5 |
| 25 bps | 2 | $0.33B | 2 |
| 30 bps | 2 | $0.33B | 2 |

**With all mid-size foundations:** 10 bps never breaks even, 15 bps needs 10 customers ($0.6B) and 20 bps needs 5 ($0.3B). **With small foundations only, full service never breaks even, even at 20 bps.**

**Single customer:** the assets needed for cash break-even are $162M at 20 bps and $114M at 30 bps; fully loaded, $360M and $231M.

Full-service cash cost is about 7 bps of assets at 10–25 mixed customers. In the Monte Carlo it is 9 bps at the median and 10–13 bps at P90.

## Break-even prices (what each customer must pay; mixed sponsors)
| Customers | L cash per customer | L cash per account | L loaded per account | F cash bps | F loaded bps |
|---|---|---|---|---|---|
| 1 | $202k | $672 | $1,860 | 54 | 114 |
| 5 | $77k | $106 | $203 | 9.5 | 14.8 |
| 10 | $57k | $48 | $78 | 7.0 | 9.0 |
| 25 | $44k | $40 | $53 | 6.1 | 6.9 |
| 100 | $38k | $32 | $35 | 5.6 | 5.8 |

These figures are average cost for this mix (review finding ADV-A-21), not a price list. The minimum credible prices in [00](00-answers.md) use the 10–25-customer band. Floors: [`price-floors.csv`](data/outputs/price-floors.csv).

## Working capital and capital before revenue
- **Collection lag (months):**
  - licensing 0/1/3;
  - white-label 1/2/3;
  - full service 1/2/4 (quarterly in arrears on assets);
  - subscriptions 0/0/1.
  
  The lag delays first-year revenue in the growth path.
- **Go-live, before the first invoice:**
  - licensing about $170k;
  - full service about $269k;
  - charity intelligence about $121k;
  - migration about $23k.
  
  This covers onboarding and hypercare, acquisition, prepaid assurance and insurance, and six months of the first-customer run-rate.
- **Deepest cumulative deficit after production qualification:** see [10](10-sensitivity.md) and [`capital.csv`](data/outputs/capital.csv).

## Observations
1. **Licensing is the cheapest model to run but needs customer count or a large first customer.** Its cost is nearly independent of customer size, so revenue must come from accounts priced at about $40–55 per account in the 10–25-customer band.
2. **White-label and limited operations do not self-finance at the tested reference prices.**
   - White-label gives up price for distribution.
   - Limited operations adds EF exception work without the full-service fee.
   
   Both need higher prices than tested, or partner economics not modelled here.
3. **Full service is the only model that funds growth early, but only with larger sponsors and at 15 bps or more.**
   - It carries SOC 1 from the first client.
   - Its cost varies more than 4× with exception intensity.
   - It is not a release-1 offer: release 1 runs with no Unbound staff in sponsor workflows (UNB-CDD-CMF-002).
   - The DEC-002 anchor gate applies to it, per the owner's resolution of OD-CDD-04.
4. **Charity intelligence costs little to run once the pipeline exists, but needs about 30 paying subscribers at $6k.** It also depends on source rights, which remain an open counsel question.
5. **Migration services self-finance per project** and are the lowest-risk first revenue. They do not build recurring revenue on their own.
