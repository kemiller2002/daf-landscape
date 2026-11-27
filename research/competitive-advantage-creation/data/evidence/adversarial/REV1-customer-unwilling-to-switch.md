# REV1 - Customer unwilling to switch

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV1. Perspective: COO of an established sponsor with several thousand DAF accounts, on an incumbent platform for eight years, three-year term with a 90-day notice window, satisfied with service and audit outcomes. Written independently of the other REV1 perspectives. Challenge IDs P3-CHL-REV1041..REV1047 in [adversarial-challenges.csv](../../fragments/REV1/adversarial-challenges.csv).

## Bottom line

Your best-performing plan needs me, and nothing in it gives me a reason to move. I would take your proposal to my incumbent at renewal, collect a discount, and stay. The package knows this (CHL-096) but does not model it.

## 1. You need sponsors like me, and you have spoken to none (P3-CHL-REV1041, high, factual + judgment)

The only sequence that pays back, A3, assumes 3 new customers a year paying $300k net, i.e. about 5,300 accounts each at $81 less 30% (P3-ASM-AB030; ER-7 basis "3-10k-account sponsors", `../competitive-displacement/data/model-inputs/entry-routes.csv` line 8). In the repository's own FY2024 panel (SRC-013) only 25 sponsors have 5,300 or more accounts, none a community foundation; every one runs on an established system. Phase II found 1 of 26 national and faith sponsors left iPhi in 2023-26 and that satisfied buyers stay for people, audit, board and vendor-viability reasons ([00](../../../../competitive-displacement/00-executive-summary.md):9, 26, 35). V-1, the stayer interviews that would test whether anyone like me would move, has not been run; the whole demand side of A3 rests on Phase II inputs reused "unchanged... untested" (P3-ASM-AB030). Proposed change: no sequence that depends on sponsors above ~2,500 accounts should be presented as "without displacement"; V-1 stayer evidence should be a precondition for quoting A3's payback.

## 2. Your proposal is my renewal discount (P3-CHL-REV1042, high, judgment)

Report 13 lists renewal concessions as the incumbent's highest-likelihood, lowest-cost response and says buyers use a competitor quote to renegotiate (CHL-096; [13](../../../13-incumbent-response-model.md):13). The model does not convert that into lost deals: `customers_per_year` is 1/3/5 independent of competitive response in every sequence, and the response model ([16](../../../16-capital-efficient-market-entry.md):191-226) adjusts only break-even accounts, not the signing rate or the sales cost of deals lost to renewal. The entrant's CAC therefore subsidizes the incumbent's retention. Proposed change: model a quote-to-renewal leakage rate (share of qualified opportunities that end in an incumbent concession) and charge the full CAC of those lost opportunities.

## 3. Your cost of switching me is mostly my cost, and it is not counted (P3-CHL-REV1043, medium, judgment)

Implementation is $35-150k vendor cash for the first customer and $10-80k later (P3-ASM-AB020). My side of a migration is staff time (E24 one-time 9,000 minutes plus 2 per account even in the redesigned model, [10](../../../10-structural-cost-elimination.md):70), parallel running, auditor re-familiarization, donor and advisor communication, a paid export from my incumbent (W04-W05) and early-termination exposure. None of these appears in any sponsor-side figure. For a sponsor with thousands of accounts this is a six-figure internal cost against a modelled operating saving that, against a well-automated incumbent, is $11-71 per account-year ([07](../../../07-architectural-competitive-advantages.md):94).

## 4. Contract windows decide timing, and they are not in the model (P3-CHL-REV1044, medium, judgment)

My contract renews on a fixed date with 90-day notice (the NPact 3-year + 90-day pattern, [13](../../../13-incumbent-response-model.md):16). A3's first signing is month 9/15/24 (`sequence-values.csv`) regardless of when any target's window opens; V-5 (contract-end calendar) has not been run even at its $0 desk layer. If the eligible accounts at 3-10k-account scale are ~20-25 sponsors with staggered 3-5 year terms, only a handful are even contestable in any given year. Proposed change: derive the signing rate from the number of contestable windows per year times a win rate, instead of an unconditioned 1-5 per year.

## 5. Architecture is not what I buy (P3-CHL-REV1045, medium, judgment; conceded in part)

The package agrees: "customers buy audit trails and SOC opinions, not storage models" ([07](../../../07-architectural-competitive-advantages.md):95). My auditor relies on my incumbent's SOC 1 and SOC 2 Type II history; you have none and plan to buy a Type 1 at term sheet (P3-DEC-AB004). Replayable eligibility decisions (EK017) answer a question my auditor has never asked. Report 07 already classifies nothing as architectural; reports 14 and 16 should not then lean on "a completed Unbound" as if completion itself creates preference. The A3 advantage over A is purely that the build cost is excluded from the cost-center clock (P3-DEC-MOD001, [16](../../../16-capital-efficient-market-entry.md):242), not that customers value anything more.

## 6. The kill-rule pass for A3 is an accounting choice (P3-CHL-REV1046, high, judgment - circular reasoning)

Report 14 says A3 passes the kill rule "under every cost-center definition tested" ([14](../../../14-commercial-sequencing.md):264). Every definition tested for A3 starts from a functionally complete Unbound; the remaining S2-to-S3 build (cash $0.6M base, economic $1.94M base, `sequence-values.csv` TPL-UNB-S2 `dev_cash`/`dev_econ`; [02](../../../02-existing-unbound-economics.md):44) never enters A3 under any variant, including "development counts" ([14](../../../14-commercial-sequencing.md):190). Report 16 then recommends finishing Unbound "inside existing Echelon operations" so that the kill rule becomes "a sales test" ([16](../../../16-capital-efficient-market-entry.md):242). The result is that the capital most at risk (the build, and the founder's 18 months of build labour) is excluded from the instrument designed to protect capital. From my side, it means the vendor arriving at my door has already sunk ~$2M of economic cost and has every incentive to keep selling past the point where the evidence says stop. Proposed change: show A3 with the S2-S3 build inside the clock as a mandatory comparison row and state, beside every "A3 passes" statement, that A3 assumes the build is done outside the cost center.

## 7. AI and automation claims will not move me (P3-CHL-REV1047, low, judgment)

AI decisions are advisory only (DEC-005) and Phase II attributes about 6% of the modelled saving to AI ([00](../../../../competitive-displacement/00-executive-summary.md):8). I agree with the package's restraint; the low severity is a reminder that any marketing that leads with "AI-native" works against a satisfied stayer, who hears "unproven".
