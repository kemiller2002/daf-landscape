# REV2 - Bootstrapped business founder

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV2. Perspective: a founder who has built and sold a niche B2B software company without outside money, reading the package as advice to a solo founder. Written independently of the other REV2 perspectives. Challenge IDs P3-CHL-REV2020..REV2028 in [adversarial-challenges.csv](../../fragments/REV2/adversarial-challenges.csv).

## Bottom line

The genuinely bootstrappable part of this package is report [04](../../../04-low-cost-commercial-validation.md): $1-25k of cash and 150-300 founder hours to run the validation tests. Everything after that needs about $1-2M of somebody's cash, and four or more years of the founder working unpaid or underpaid. "Outside investment is not necessary if the owner can fund the peak" is true of any business. The plan also quietly assumes one person can do a whole company's work for 18 enterprise sponsors. My advice: stop at the named-partner test, and do not spend a DAF dollar before it passes.

## 1. "No outside investment needed" is circular (P3-CHL-REV2020, high, circular reasoning)

P3-CLM-MOD012 says outside investment is not necessary for A3's base case if the owner can fund the peak, and P3-GAP-MOD001 records that nobody knows whether the owner can. A3's peak is $1.24M of cash, and it starts from S3, which does not exist yet. From today (sequence A) the peak is $1.94M, and the base case is paused by the kill rule at month 24 after $1.14M. For a bootstrapper, money the founder does not have in the bank is outside capital, whatever it is called. Proposed change: state the cash required from today, and the founder's personal runway requirement, beside each sequence. Drop the "not necessary" claim until P3-GAP-MOD001 is answered.

## 2. The founder is the hidden company (P3-CHL-REV2021, high, hidden founder labour)

Founder cash is $0 before revenue and $60k once live (P3-ASM-AB018). Founder FTE is fixed at 1.0 for 120 months whatever the customer count. A3 reaches 18 live enterprise sponsors, roughly 95,000 accounts, by month 120. The model then has no hire. One person would be:
- seller and partner manager;
- implementation lead for each 5,000-account migration;
- second-line support (the $40k support line is a fraction of an FTE);
- named accountable owner for eligibility (0.15-0.5 FTE, report [10](../../../10-structural-cost-elimination.md) §10);
- SOC 2 control owner;
- product owner.

Phase II raised flat burn that ignores customer count (CHL-089), and it is unchanged. Adding even $30k a year per live customer for service raises A3's peak from $1.24M to $1.34M and moves payback from month 62 to 67. That is small in dollars, but it is the labour that runs out first. Proposed change: a capacity constraint (customers per founder) or a hiring trigger in model 8. Show months of unpaid founder work before the first $60k draw.

## 3. The build cost rests on unledgered agent productivity (P3-CHL-REV2022, high, unmeasured productivity)

Remaining development from S2 is $600k cash against a $1.94M market build (P3-ASM-AB002). The cash ratio of 0.31 used for other streams (P3-ASM-MOD022) is derived from that same AB figure, so it is circular. Agent AB notes that the owner has not ledgered actual spend (P3-ASM-AB001), and report 04 calls the productivity measurement (M-07) "moot once Unbound is built". Moot is exactly what it is not: it is the only way to know whether the S2-to-S3 number is $250k or $1.2M. Proposed change: start a time and cash ledger for Unbound work now (cost $0) and report actual against the AB002 range each month.

## 4. Ramen profitability is four-plus years away from today (P3-CHL-REV2023, medium, judgment)

"Sustainable from month 38" in A3 counts from S3. A from S2 is sustainable from month 47 in the base case, on a $60k founder draw, with a named partner by month 6. The founder's forgone salary at P3-ASM-AB018 ($190-273k a year) over that period is about $0.9M. The package prices it into fully loaded cost, which is right. It never compares the plan with the bootstrapper's real alternative: paid consulting or other Echelon revenue that funds the validation and keeps the founder solvent. Proposed change: add a "do nothing / consult" baseline at $0 DAF cash.

## 5. What can really be done without capital (P3-CHL-REV2024, medium, sequencing)

Without capital the founder can do report 04's $0-25k ladder: the V-3 replay (largely done), the V-5 desk calendar, the V-6 partner map and conversations, V-2 price questions inside V-6, and publishing commercial licence terms. The next step needs about $105k of one-time spend (SOC readiness and legal) and a $465k a year run. Report 16 §6, entry path step 1, instead says "finish Unbound to S3 inside existing Echelon operations". That spends development first and keeps it off the kill-rule clock. Proposed change: make a named partner with a non-binding price expression (V-6 plus V-2) the precondition for any further Unbound development beyond what Echelon would do anyway.

## 6. Implementation of a 5,000-account sponsor for $30k (P3-CHL-REV2025, medium, underestimated cost)

Later-customer implementation is $10-80k (P3-ASM-AB020, S6 with reusable packages). Phase II found 584-934 sponsor hours for a 10k-fund conversion and multiple rehearsals per migration (CHL-073, CHL-077). The vendor side of that work is the founder. Either implementation is underpriced, or it is founder labour that does not appear in cash. Proposed change: price later implementations from the Transitus rehearsal plan, and charge them (the customer-funded variant).

## 7. Side bets eat the critical path (P3-CHL-REV2026, medium, judgment)

Sequences B, C, D and F, the adjacent industries (report [08](../../../08-adjacent-financial-industries.md)) and component licensing (report [09](../../../09-independent-component-commercialization.md)) are each described as small founder fractions (P3-ASM-MOD024, MOD031). The model splits FTE but never delays A's signing month when time is diverted, so diversion looks free. At one FTE, every fraction comes off the partner search. Proposed change: model diversion as a delay to `first_signing_month`, or drop the side bets until a pilot is live.

## 8. Customer service labour is absent (P3-CHL-REV2027, low, omission)

No stream carries a per-customer service or account-management cost, apart from the share-of-revenue variable cost. See §2 for the re-run.

## 9. Component licences lose money per customer (P3-CHL-REV2028, low, factual)

Sequence F's support cost of $2,360 per customer-year exceeds its $2,000 revenue: gross margin -18% ([14](../../../14-commercial-sequencing.md) §3). Report 09 still recommends self-serve commercial licences. For a bootstrapper, a product that costs more to support than it earns is worse than no product. Proposed change: publish the terms (needed for Unbound anyway, CNV-GOV-007), with no support offer, or price at $5k or more.

## Factual and model errors versus judgment

- **Factual or model**: REV2021 (fixed founder FTE and flat run are model structure), REV2022 (circular derivation of P3-ASM-MOD022), REV2028.
- **Judgment**: REV2020, REV2023, REV2024, REV2025, REV2026, REV2027.
