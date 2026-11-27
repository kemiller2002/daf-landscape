# REV2 - Product strategist

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV2. Perspective: head of product strategy, asked whether the package gives the owner a coherent position, a focused product and a defensible sequence. Written independently of the other REV2 perspectives. Challenge IDs P3-CHL-REV2038..REV2046 in [adversarial-challenges.csv](../../fragments/REV2/adversarial-challenges.csv).

## Bottom line

The research is broad and mostly honest about each piece. The strategy that emerges from it is still not coherent. The approved direction is partner-first entry to sponsors that are not served today (DEC-001, Phase III's non-displacement theme). That direction loses money in every sequence that implements it (E, G, H). The one sequence that pays back (A3) does so by selling to large sponsors that are incumbents' customers. It also starts from a product state that does not exist, and it passes the kill rule only by moving spend off the clock. The owner needs a single positioning choice and a gate in front of further building, not nine ranked sequences.

## 1. A3 is a state, not a strategy, and the entry path moves the kill-rule clock (P3-CHL-REV2038, high, circular / governance)

A3 is sequence A with the S2-to-S3 build already done. Ranking it first beside sequences that start today compares a later state with present choices. The sequence it is the tail of (A) is paused by the kill rule in the base case. Report [16](../../../16-capital-efficient-market-entry.md) §6, entry path step 1, says to "finish Unbound to S3 inside existing Echelon operations ... the kill rule's 24-month pilot test is then a sales test". The kill-sensitivity table shows the mechanism. A goes from "paused at 24" to "passes" when the cost-center month moves from 0 to 12 or later, at the price of about $0.8M more cash before any test. Relabelling the build as "development" spends the money first and gates it afterwards. That inverts DEC-008. Proposed change: drop A3 from the ranking, or show it as "A conditional on S3" with the S2-to-S3 cost attached. Do not recommend completing S3 off-clock until P3-DEC-MOD001 is decided by the owner with this trade stated.

## 2. The approved positioning and the paying positioning are different businesses (P3-CHL-REV2039, high, positioning)

| Positioning | Sequences | Revenue per customer | Model result (base) |
|---|---|---|---|
| Partner-first to small and mid sponsors; new programmes (DEC-001; reports 05, 06) | E, G, H | $2-150k | no payback; -$4.5M to -$6.1M |
| Channel licensing to ER-7-scale sponsors (about 5,300 accounts) | A, A3 | $150-600k net | pays back (A paused by kill rule) |

The second row is a displacement play against the segment that switches least (Phase II CHL-082). In the FY2024 panel only about 25 sponsors are that large, none of them community foundations; see P3-CHL-REV2012. Report 16 §6, step 5, "prefer channels whose customers pay at Phase II ER-7 scale", silently swaps positioning. Proposed change: present the owner with the explicit choice between two options:
- (a) a niche licensing product for mid-to-large sponsors, reached through a partner that already serves them;
- (b) greenfield programme enablement priced to carry a licensor.

Either way, state that (a) is displacement.

## 3. Sequence logic: name the partner, then build to the partner (P3-CHL-REV2040, high, sequencing)

Partner-first means the partner's integration, tenancy, branding, single sign-on and data-rights requirements shape the product (report [12](../../../12-institutional-distribution.md) §4 already asks for tenancy that survives a partner exit). Finishing S3 before a named partner risks building the wrong S3. The cheapest test that discriminates between the two positionings is V-6 plus V-2: a named partner, with a non-binding price expression and a stated sponsor size. My re-run shows A3 needs about $110-120k a year net per customer for cash payback, roughly 2,000 accounts at $56.7. Proposed gate before any further DAF-specific build:
- a named partner;
- a price expression at or above that level;
- at least one candidate sponsor of at least 2,000 accounts.

## 4. Fragmentation (P3-CHL-REV2041, medium, focus)

The package carries:
- nine sequences and eight models;
- five economic entities;
- 19 shared-component repositories;
- two adjacent industries (report [08](../../../08-adjacent-financial-industries.md));
- a charity-intelligence product;
- Transitus services.

The model finds that B, C, D, F and G each fail on their own. Reports 08 and [09](../../../09-independent-component-commercialization.md) already say "not now". The product roadmap should say it too, as an explicit do-not-build list: B as a product, D, G, the adjacent industries, and component sales beyond published terms. Keep charity intelligence and Transitus as internal capabilities of Unbound.

## 5. Component commercialization is a distraction with negative margin (P3-CHL-REV2042, medium, factual)

Report 09 recommends self-serve commercial licences for developer components. Sequence F, which models exactly that, has -18% gross margin: support of $2,360 per customer-year against $2,000 revenue. Every support hour is founder time. Publishing commercial terms is needed for Unbound anyway (CNV-GOV-007); offering a supported product is not. Proposed change: publish terms with no support commitment, and remove F from the sequence ranking.

## 6. The ranking metric rewards doing nothing (P3-CHL-REV2043, medium, model presentation)

`Render.fs:254` ranks by cumulative cash at month 120. F ranks third because it spends almost nothing and never pays back. There is no $0 "do nothing" row, which would rank third, above every loss-making sequence. Under the kill rule, no sequence has a positive median outcome: A3's Monte Carlo P50 is -$226k with 75% of runs paused. Proposed change: add the do-nothing baseline, and rank on the kill-rule Monte Carlo.

## 7. The intelligence API is allowed to stand in for a DAF pilot (P3-CHL-REV2044, medium, model error)

`Sequences.fs:254-258` takes the first go-live of any dedicated stream as the "referenceable live pilot". B passes on a fraction of an $8k-a-year eligibility-API customer at month 22, then loses $5.78M. Report [14](../../../14-commercial-sequencing.md) notes this ("tests proof of demand, not economics"). But the kill rule was written to test the DAF thesis: a sponsor live on Unbound. Proposed change: the pilot test must be met by an Unbound (E2) sponsor stream. See also P3-CHL-REV2001.

## 8. The greenfield is not a software-addressable market (P3-CHL-REV2045, medium, positioning)

Report [05](../../../05-untapped-institutional-markets.md) finds 3,056 education and health institutions with no DAF signal. Its own barrier analysis says what keeps them out is demand, a free alternative and regulatory responsibility, "not technology". A software licence does not remove those barriers. What could remove them is a hosted programme service (E). E does not carry a licensor at $2-25k per programme. Proposed change: reframe report 05's market as a market for a service partner. Do not present it as evidence of demand for Unbound licences.

## 9. S7 is in the owner's table without a second product (P3-CHL-REV2046, low, presentation)

The capital-by-state tables show S7 ("operates on Echelon shared infrastructure") at $583k cash to first invoice. Report [15](../../../15-shared-infrastructure-economics.md) says that sharing lowers Unbound's cash only when another product earns revenue, and none does. Proposed change: mark S7 as hypothetical, or remove it from owner-facing tables.

## Factual and model errors versus judgment

- **Model or factual**: REV2042 (F margin against report 09's recommendation), REV2043 (ranking metric), REV2044 (pilot definition in code).
- **Circular or governance**: REV2038.
- **Judgment**: REV2039, REV2040, REV2041, REV2045, REV2046.
