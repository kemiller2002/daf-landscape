# REV2 - Economist skeptical of AI productivity claims

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV2. Perspective: a labour and productivity economist. My prior is that measured AI productivity gains in operations are real but smaller and slower than projected. My other prior is that "AI savings" usually turn out to be process redesign, or work moved to someone else. Written independently of the other REV2 perspectives. Challenge IDs P3-CHL-REV2029..REV2037 in [adversarial-challenges.csv](../../fragments/REV2/adversarial-challenges.csv).

## Bottom line

To its credit, the package mostly does not claim AI productivity in operations. Report [10](../../../10-structural-cost-elimination.md) attributes only about 9 of roughly 130 removed minutes to AI acceleration. It treats transfers as costs to someone else and computes savings as sequential residuals. Where it does rely on unmeasured AI productivity, it does so quietly in capital, not in operations. Development is assumed at 31% of a market build, and maintenance of a production financial platform at $120k a year. The models are also internally inconsistent about where automated work goes. Three cost-side corrections, each defensible on the package's own numbers, are enough together to remove A3's base-case payback even at the contested $300k revenue per customer.

## 1. Automated work disappears between model 2 and model 8 (P3-CHL-REV2029, high, model inconsistency)

The event model charges automated work back as platform cost: 25% of its labour value, i.e. $30 per account-year, plus $3 for AI (events-by-party table). Report 10 says this cost is carried in platform fixed cost. The lean licensor run has no automation-upkeep line (P3-ASM-AB010..AB017). Sequences A and A3 charge $12.15 per account through `variable_share` 0.2143, which comes from Phase II ER-4's direct share (P3-ASM-MOD003). So the platform cost that model 2 says automation creates appears in neither the fixed nor the variable cost of model 8. I re-ran A3 with variable cost at about $33 per account (variable share 0.58 on $56.7 net):

| A3, base | Published | Event-consistent platform cost |
|---|---|---|
| Peak cash | $1.24M | $1.82M |
| Payback month | 62 | 96 |
| Economic net m120 | +$9.36M | -$0.34M |
| Monte Carlo (uninterrupted), share with no payback | 5% | 33% |

P3-GAP-MOD004 (variable cost per account) is marked non-blocking. On this evidence it is blocking.

## 2. The capital minimization is an AI-productivity bet (P3-CHL-REV2030, high, unmeasured productivity)

The lean structure removes the "conventional organization" (report [02](../../../02-existing-unbound-economics.md) §3). It does so mainly by assuming that agents plus contractors deliver the following:
- development at 31% of market cash (P3-ASM-MOD022, itself derived from AB's own numbers);
- maintenance at $40-250k a year (base $120k) where 1-2 engineers cost $0.22-0.47M (P3-ASM-AB010).

Neither is measured: no ledger exists (P3-ASM-AB001), and M-07 is dropped. Replacing the maintenance base with about 1.5 engineers (+$230k a year on the live run) gives an A3 peak of $1.59M, payback in month 70, and no payback in 13% of uninterrupted draws.

**Stacking.** I combined three corrections:
- event-consistent platform cost (§1);
- conventional maintenance (this section);
- contingency on the run (CFO review, P3-CHL-REV2003).

The result: A3 base has **no payback in 120 months** (m120 cash -$1.03M, economic -$5.06M, peak $3.24M), and 67% of uninterrupted draws do not pay back. The revenue input is left at ER-7. Proposed change: present the AI-dependent cost lines as a named hypothesis with a measurement plan. Hours and cash ledgers cost $0.

## 3. The minutes are assumed, and automation is credited at 100% (P3-CHL-REV2031, medium, unmeasured productivity)

Report 10 §11 concedes that touch rates, minutes and efficacies are Phase II assumptions. The waterfall removes automated minutes entirely and charges back an unmeasured 10-50% (P3-ASM-MOD007). No exception tail is measured, while adjacent industries keep 5-15% after decades of automation (report 10 §10). The only measured input in the chain is the Schedule I replay. Proposed change: report the event saving as a range conditional on V-7, and do not let it feed the price floor until a pilot measures exceptions.

## 4. Attribution: the savings are redesign, not AI (P3-CHL-REV2032, medium, attribution)

AI-accelerated work is about 9 minutes, around 7% of removed work. Deterministic controls account for about $124 of the $194 Phase II saving (report [07](../../../07-architectural-competitive-advantages.md) §4). Ren already claims automated vetting with more than 50% instant approvals. The benchmark is a "conventional" administrator. Against a well-automated incumbent the gap is $11-71 per account-year (report 07, report [13](../../../13-incumbent-response-model.md)). Any owner-facing language about "AI-native" cost advantage overstates the AI contribution, and the AI cost share of 10-40% of labour value is itself unmeasured (P3-ASM-MOD008). Proposed change: report savings against the best-automated incumbent, split into redesign, deterministic automation and AI.

## 5. Baumol and the real-terms horizon (P3-CHL-REV2033, medium, judgment)

The ten-year model has no price or wage escalation. The residual work is mostly mandatory human judgment (about 28 minutes: 4967 review, sanctions disposition, audit preparation). So are the fixed lines: counsel, insurance, audit, security staff. These rise with skilled wages faster than general prices. Per-account software prices meanwhile face compression (report 13). A flat real-terms model hides a margin squeeze that compounds over ten years. Proposed change: a variant with residual labour and assurance costs escalating 2-3 points above licence price.

## 6. The registry is priced at one sponsor forever (P3-CHL-REV2034, medium, model error)

`Analysis.fs:18` computes the registry cost the lean licensor must add at one sponsor. `Sequences.fs:107` then adds that constant to the live run for the whole horizon. The registry's own union-of-charities scaling (`Registry.fs:60`) grows with sponsors: at 10 sponsors and 20k charities the average is about $26k a sponsor (registry-marginal table), roughly $260k in total, against the $87k addable. The cost grows with A3's 18 sponsors and is omitted. Proposed change: make `RegistryRunAnnual` a function of live sponsors.

## 7. The founder may be counted twice in fully loaded cost (P3-CHL-REV2035, medium, possible double count)

Development's economic value is the market cost of the build (P3-ASM-AB001/AB002: "founder time excluded (shown in economic)"). The engine also charges the founder at one FTE at market during the same development months (`Cashflow.fs:147` and `Cashflow.fs:161`). If the market build includes the engineering the founder performs, fully loaded cost is overstated: by about $111k for A3 (6 months) and $333k for A (18 months). The error runs in the conservative direction, but it distorts the cash-versus-fully-loaded comparison the owner is asked to use. Proposed change: state whether the founder's build hours are inside `dev_econ`, and net them out if so.

## 8. Transfers set the buyer's willingness to pay (P3-CHL-REV2036, low, judgment)

Under licensing, about 53 residual minutes move to the sponsor at 1.4 times the effort (report 10 §3). The sponsor's all-in cost is the licence plus about $67 per account of staffed residual work. Willingness to pay at $81-120 should be tested against that all-in comparison with an incumbent's full service. V-2 as redesigned in report 04 asks about the licence price alone.

## 9. Validation is not independent (P3-CHL-REV2037, low, process)

Report 02 itself notes that authors and reviewers come from the same model family. Nearly every productivity input is ASSUMPTION or INFERENCE. Proposed change: before the owner relies on any productivity-dependent figure, have one human practitioner check three inputs: maintenance FTE, implementation hours per 1,000 accounts, and exception rate.

## Factual and model errors versus judgment

- **Model errors or inconsistencies**: REV2029, REV2034, REV2035.
- **Unmeasured productivity, factual about the evidence base**: REV2030, REV2031.
- **Judgment**: REV2032, REV2033, REV2036, REV2037.
