# REV2 - Venture investor

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV2. Perspective: partner at an early-stage software fund, reading the package as if it were the data room for a seed round. Written independently of the other REV2 perspectives. Challenge IDs P3-CHL-REV2011..REV2019 in [adversarial-challenges.csv](../../fragments/REV2/adversarial-challenges.csv).

## Bottom line

This is a careful, honest package about a business I would not fund, and it mostly says so itself. The only sequence that pays back (A3) gets there on a revenue-per-customer figure carried over untested from Phase II. That figure was challenged in Phase II (CHL-081, CHL-082). It describes sponsors that barely exist outside the national platforms. If it is replaced with Phase III's own sponsor-level price, the winning sequence loses money in 98% of draws. Even on the favourable input, the median outcome is a niche licensing business worth single-digit millions of cumulative cash over ten years. The founder should treat this as a capital-light niche business or a strategic-sale asset, not a venture story. The "externally funded" variant in the model does not describe any investor I know.

## 1. The winner is an artefact of one untested input (P3-CHL-REV2011, high, circular reuse)

A and A3 use $150k / $300k / $600k a year per customer, "net of 30% channel share", taken from Phase II ER-7 "unchanged; untested" (P3-ASM-AB030). The same package's channel work uses $25k / $60k / $150k per sponsor gross with a 15-40% partner share (P3-ASM-FGJ008, P3-ASM-FGJ001). Sequence H, the partner-embedded refinement of A, uses those values and loses $4.97M. The conflict is logged as a blocking gap (P3-GAP-MOD003), but the headline ranking, the key figures and the entry path in [16](../../../16-capital-efficient-market-entry.md) §6 are all built on the ER-7 value.

Re-run in a scratch copy, giving A and A3 H's revenue terms ($25k / $60k / $150k, 15 / 25 / 40% share, per-account variable cost):

| A3, base | Published | At agent FGJ's sponsor prices |
|---|---|---|
| Peak cash | $1.24M | $4.31M |
| Cumulative cash m120 | +$11.69M | -$4.31M |
| Monte Carlo, uninterrupted: share with no payback in 120 months | 5% | 98% |

Bisecting A3's revenue per customer with everything else at base: $100k gives no payback (m120 -$0.89M); $150k pays back in month 96 but stays negative fully loaded (-$0.53M); $200k pays back in month 79. Cash payback needs roughly $110-120k a year net per customer, which is about 2,000 licensed accounts at $56.7 net. Note also that [19](../../../19-sensitivity-and-stress-analysis.md) §5 says A3 has "no payback in ten years" at the low end of the range. At $150k cash does pay back, in month 96; only fully loaded does not.

## 2. The customers that make A3 work are a list of about 25-35 names, mostly captive (P3-CHL-REV2012, high, factual with repository data)

At $300k net, a customer is about 5,300 accounts. In the repository's FY2024 sponsor panel (`data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv`, 1,514 sponsors with account counts; my count), 25 sponsors have at least 5,300 accounts: 15 national, 5 donation processors, 3 religious, 2 single-issue, and no community foundation. At the roughly 2,000-account cash-payback threshold the count is 35, of which 2 are community foundations. A3 base signs 3 a year, about 30 over ten years with 18 live at month 120. Most of the pool runs proprietary or long-contracted platforms. Phase II found this segment "switches least" (CHL-082), and Phase III's own greenfield (report [05](../../../05-untapped-institutional-markets.md): 3,056 education and health institutions) pays $2-60k a year. The paying route is displacement of the least mobile installed base, which contradicts the Phase III premise of acquisition without displacement.

## 3. Not venture-scale, and no exit thesis (P3-CHL-REV2013, high, judgment)

Even on ER-7 revenue, the uninterrupted Monte Carlo gives A3 a P50 cumulative cash of $8.9M over ten years (P10 $1.3M, P90 $21.1M). With the kill rule applied, the P50 is -$226k, and 75% of runs pause. The favourable $88M needs every input at its favourable end at once. A rough licensing ceiling makes the same point. Phase II cites about 1.78M DAF accounts (CHL-083); at the $81 list price that is about $144M a year *if every account in the country were on third-party licensed software*. The nationals that hold most accounts are not buyers. Exits remain acquisition by Ren, TIFIN, Foundation Source or Foundant, who buy rather than license (CLM-025, CHL-087). Partner-first hands the likeliest acquirer the customer relationship. The externally funded variant prices equity as a 30% cost of capital (P3-ASM-MOD015). It ignores dilution, control and the fact that no fund would underwrite this distribution. Proposed change: drop "externally funded" as venture equity; model owner capital, revenue-based debt and partner funding only; add an explicit strategic-sale scenario.

## 4. The response model inherits the same input (P3-CHL-REV2014, medium, model)

"Years from first contract to break-even" for the lean licensor is 0.4-0.9 years under no response ([16](../../../16-capital-efficient-market-entry.md) §5). That follows from `Analysis.fs:152-153`, which converts ER-7 revenue into 15,873 newly licensed accounts a year. `Analysis.fs:162` also holds the lean cost base at base in every case. At FGJ's $60k at $81 gross (about 740 accounts per sponsor, 3 a year, 8% churn), my arithmetic puts no-response break-even nearer 4.6 years. Under the aggressive response, with half the wins, it is about 36 years. P3-CLM-MOD013 ("lean survives price responses") is conditional on AB030 and should say so.

## 5. Defensibility is conceded, but the sequence model ignores it (P3-CHL-REV2015, medium, inconsistency)

Report [07](../../../07-architectural-competitive-advantages.md) rates the largest economic item (EK002 deterministic controls) as ordinary with low persistence, and report [13](../../../13-incumbent-response-model.md) models price cuts of 5-50%. The sequence model holds price flat for ten years with 8% churn and no compression. Proposed change: feed the RS-1/RS-2 price paths into model 8, at least as a variant.

## 6. Channel control is the base case, not a tail (P3-CHL-REV2016, medium, judgment)

A3's dependency is a channel partner willing to embed Unbound (V-6). Yet its partner share is 0 (the revenue is already net), and partner churn of 5-25% (P3-ASM-FGJ016) is not applied. Partner acquisition appears only as an extreme: aggressive incumbent plus partner acquired at month 36 leaves A3 at -$1.34M with no payback. Phase II's evidence is that administrators acquire rather than license and that the one distributor precedent chose a competitor (CHL-084). Proposed change: carry partner termination as a base-case hazard in A, A3 and H.

## 7. Key-person risk (P3-CHL-REV2017, medium, judgment)

Every platform sequence consumes 120 founder-months. There is no hire in any sequence; one person carries sales, partner management, implementation oversight, compliance ownership and product. A bank's third-party-risk review (Phase II CHL-015) will see that before it sees the architecture. Proposed change: a staffing trigger (for example, a second FTE at the third live sponsor) in the model, plus a key-person mitigation in the plan.

## 8. Corners are not ranges (P3-CHL-REV2018, low, presentation)

Favourable and adverse move every input at once. For A3 that gives +$88M against -$17M: uninformative bounds. The kill-rule Monte Carlo is the decision-relevant distribution and should lead.

## 9. No addressable-market number for licensing (P3-CHL-REV2019, medium, gap)

Report 05 counts institutions. Nothing in Phase III states licensing TAM or SAM in accounts or dollars by sponsor size band, or how many non-captive sponsors exceed the roughly 2,000-account payback threshold. That is a $0 desk calculation from data already in the repository. Proposed change: add it before any ranking is shown to the owner.

## Factual and model errors versus judgment

- **Factual or model**: REV2011 (the ranking depends on an untested input that contradicts another agent's input, plus a small misstatement in 19 §5); REV2012 (population count); REV2014 (response conversion and fixed cost base).
- **Judgment**: REV2013, REV2015, REV2016, REV2017, REV2018, REV2019.
