# REV4 - Round 2 adversarial review

Status: adversarial review, round 2 (2026-11-26). Reviewer panel REV4. Five independent perspectives: CFO, bootstrapped founder, incumbent competitor executive, product strategist, and a disposition audit. Question: is model revision 2 right, or has it over-corrected into pessimism, and do the round-1 dispositions hold? Challenges: `data/fragments/REV4/adversarial-challenges.csv` (P3-CHL-REV4001..REV4020, round 2, dispositions empty).

Method. I read reports 14, 16, 18, 19, 20, 25 and the relevant parts of 02, 07, 08, 11. I read the model source (`Cashflow.fs`, `Sequences.fs`, `Registry.fs`, `Analysis.fs`), the inputs (`parameters.csv`, `sequence-values.csv`, `registry-components.csv`, `settings.csv`, `sponsor-sizes.csv`), the assumptions register, all 130 round-1 dispositions, and the Unbound requirement texts the dispositions cite (CNV-GRT-003; RR-REQ-X-007-r1; UNB-CDD-CIV-008; OD-CDD-02). I copied the package to the scratchpad. `check` reproduced the published outputs byte for byte. I then added experiment switches and a `rev4` command to the copy only. The package model is unchanged. Every number below is a base-case point value from that copy. None is a forecast.

## Verdict in one paragraph

Revision 2 gets the decision right. Do not spend on DAF commercialization until a named partner, a price and a candidate sponsor exist. The kill rule binds whichever cost assumptions are used. It gets the economics wrong by stacking adverse choices in the base case. "No sequence pays back in 120 months under any base" mostly comes from three choices:

- Echelon pays, out of an $81 software price, for a human deep review of every charity in use twice a year.
- A 25% contingency runs on steady-state live run and registry cost for ten years, on top of ranges that already carry that uncertainty.
- Control operations overlap the maintenance budget's code approvers.

Correct those three and A3 pays back in month 83 to 85 under M2 or M5, with a base peak of about $2.6M. Under M1 with demand-driven reviews it still loses about $1.5M by month 120. The demand side is under-corrected. The population cap counts captive national sponsors and donation processors, and the break-even gate is close to unreachable. On costs revision 2 is over-corrected. On demand it is under-corrected. On the decision it is right.

| Base point values (A3 from S3, uninterrupted) | Peak cash | m120 cash | Payback | Break-even accounts (FY2024 sponsors all / non-captive) |
|---|---|---|---|---|
| V0 revision 2 as published (M1) | $8.70M | -$8.70M | none | 10,963 (14 / 5) |
| V1 M5 (conditional on OD-CDD-02) | $3.46M | -$340k | none | 3,949 (28 / 11) |
| V2 M2 vendor cost: sponsor performs the deep review | $3.39M | +$21k | 120 | 3,848 (28 / 11) |
| V3 M1, demand-driven reviews (RCH-09 x0.6) | $5.20M | -$5.20M | none | 6,282 |
| V4 M1, risk-tiered human review (RCH-09 x0.4) | $4.26M | -$3.45M | none | 5,177 |
| V6 contingency on one-time and pre-revenue cost only once live | $5.25M | -$5.25M | none | 6,833 |
| V7 control operations net of the AB010 code-approver overlap ($150k) | $7.58M | -$7.58M | none | 9,937 |
| V13 CFO-corrected M1 (V3 + V6 + V7) | $3.47M | -$1.52M | none | 4,350 |
| V15 CFO-corrected with M2 | $2.58M | +$2.00M | 83 | 3,023 (31 / 13) |
| V15b CFO-corrected with M5 | $2.62M | +$1.78M | 85 | 3,077 |
| Sequence A from today, CFO-corrected with M2 | $3.35M | +$1.02M | 101 | - |

Under the kill rule every one of these variants still pauses A3 at month 24, with $1.5-1.8M spent. The pilot arrives at month 28. Only V12 passes: a whole first customer plus a go-live lag of 8 months gives a pilot at month 24 (section 2).

## 1. CFO

**Model errors and scope problems introduced or left by revision 2 (file:line in the package).**

1. **Contingency scope** (`Cashflow.fs:199`). 25% is applied to `run + registry` in every live month for 120 months. The basis of P3-ASM-AB027 is "contingency on one-time and pre-revenue cash". REV2003 asked for one base across models, which is a fair point for the capital model up to the first invoice. Ten years of contingency on steady-state cost double counts the uncertainty that the triangular ranges and the Monte Carlo already carry. Effect: about $3.45M of A3's $8.70M base deficit (V6). Break-even falls from 10,963 to 6,833 accounts. Fix: contingency on one-time and pre-revenue cost and the first 12 live months, or a separate reserve line (REV4002).
2. **Wind-down while nothing is live** (`Cashflow.fs:197`). At a pause with any fractional signing, the model charges $50k plus 6 months of the full *live* run, even when no customer has gone live (A3 pauses at 24 with the first go-live at 25). Effect: A3 cash at risk is overstated by about $280k ($1.81M against $1.53M, V8) (REV4010).
3. **TPSP counted twice in the adverse case.** P3-ASM-AB013 high ($180k) already contains the $50k TPSP audit. `tpsp_annual` adds $130k at the same end. The base case is clean (REV4005).

**Over-stated cost lines.**

- **Control operations $150-350k.** The P3-ASM-AB010 maintenance basis already includes "second maintainer/code approvers ... CNV-PLT-010 contracted approvers". Control operations then add "contracted senior reviewers for two-approver change control". The two-approver function is costed twice. Netting about $100k moves A3 by about $1.1M (V7) (REV4005).
- **Nacha $30-130k.** The base of $75k joins an unquoted $50k audit to $10-50k of fraud monitoring that partly overlaps P3-ASM-AB012 security tooling and the ODFI's own monitoring. The amount is plausible but unquoted. Get an accredited-auditor quote before keeping $75k as the base.
- **M1 registry $768k at 20k charities.** RCH-09 is 15 min × $67.69/h × 2 reviews for every union charity, every year. RR-REQ-X-007-r1 says "an expired deep review MUST hold new approvals". A review is therefore needed only when a charity receives a new approval after its last review has expired. A charity granted once a year needs about one review, not two. At 1.2 reviews per charity-year, A3's deficit falls by $3.5M (V3) (REV4003).
- **Tax** at 25% with full carry-forward is correct in direction. The post-2017 80% limit on NOL use is ignored, which understates tax slightly. This is immaterial now.

**Is M1 the right base?** The *requirement* reading of REV3010 and REV3020 is right: until OD-CDD-02, the deep review must be performed as r1 specifies. The *cost allocation* that follows from it is not. The requirement texts make the deep review a sponsor control:

- r1: "sponsor-configured deep-review interval (default 180 days, a sponsor policy and not a legal safe harbor)"; "each sponsor's reliance snapshot MUST be written to that sponsor's partition".
- CNV-GRT-003: "Cross-sponsor evidence SHALL be reused only as input".
- After REV3011, report 11 itself keeps "identity confirmations and eligibility decisions in the sponsor cell" (UNB-CDD-CIV-010).
- Echelon is a licensor (DEC-006). DEC-002 and the brief bar it from becoming an administrator.

Under licensing, the sponsor's compliance staff perform the deep review in Unbound, as sponsors on Ren-type software do today, and the $81 price evidence excludes vetting services. The vendor's registry cost is then M2-like, about $99k (V2: A3 m120 +$21k; break-even 3,848). If Echelon performs the reviews instead, that is a priced service worth the sponsor's EV-E08 labour ($677k at 10k accounts, `events-double-count`), not an unfunded cost. Two numbers show the M1-as-vendor-cost result is structural rather than empirical. M1 labour is about $70 per account at 2 charities per account, above the $56.70 net price. The model also shares the deep review across sponsors with the union exponent, which per-sponsor reliance arguably forbids. Without that sharing, M1 never breaks even at any size, and in the partner-book runs a bigger customer loses *more* (section 4) (REV4001, REV4018).

**A compliant hybrid without OD-CDD-02.** Within r1 a "comprehensive charity review" need not be a 15-minute manual review. One design: a machine-assembled evidence pack with a human attestation at about 4 minutes for low-risk charities, the full 15 minutes for the remaining 20%, and reviews performed on demand. That still has a human perform a comprehensive review at the interval. It does not rely on the r2 automated-renewal reading that OD-CDD-02 governs. P3-ASM-HI029's own low end is 5 minutes. Cost: RCH-09 × 0.24 gives A3 -$2.05M (V5) and break-even 4,538. Whether a 4-minute attested review is "comprehensive" is a counsel question to add to V-9. It should not be assumed in either direction (REV4004).

## 2. Bootstrapped founder

Low-cash paths the model now misses or understates:

1. **Software-only licensing with sponsor-performed vetting (M2 vendor cost).** This is the most material omission. It needs no owner decision on OD-CDD-02. It needs only a decision on who performs the deep review, which nobody has raised. CFO-corrected, A3 pays back at month 83 with a $2.58M peak, and A from today at month 101 (V15). That is still a thin business, but not "no payback".
2. **Partner or sponsor operating its own vetting or registry.** An administrator or large sponsor that already employs vetting staff takes the review labour. For Echelon this is the same as M2. There is no stream for it.
3. **M5 after the V-9 auditor walkthrough.** V-3 replay and V-9 sit on the $0-25k validation ladder. If both report well, M5 with the CFO corrections gives payback at month 85 (V15b). The cost of finding out is trivial next to the $7M swing between M1 and M5. Do it first, before any build.
4. **Licensing to one large non-captive sponsor directly.** Under M2 a 20,000-account customer pays back at month 85, with three such customers and implementation at A3 rates. Under M1-as-vendor-cost a larger customer only loses more.
5. **Operating inside existing Echelon operations** does not fix the economics. A3X is rightly shown as moving cost off the clock, not saving it. I agree with revision 2 here.

**Kill-rule timing is a knife edge, not a verdict.** A3 pauses because its pilot arrives at month 28, while the test falls at month 24. Fractional signing (0.25 of a customer a month) adds 3 months beyond a whole first signing (pilot 25, V10). With a whole first customer and a go-live lag of 8 instead of 9 months, A3 passes (V12). The clock also starts at month 0 only because pre-revenue run and half of control operations are spent from month 1. The recommended gate (P3-DEC-MOD003) would defer exactly that spend. Under kill-sensitivity, A3 passes with the cost center at month 6. "Every sequence pauses" should therefore read: "pauses if dedicated spend starts before a named partner, and passes or fails by 1-4 months on conventions" (REV4009).

## 3. Incumbent competitor executive

- **Gating build on a named partner, a price and a candidate sponsor (P3-DEC-MOD003) is sound.** It is cheap, reversible, and it denies me the easiest win: an entrant that builds ahead of demand and runs out of cash. Keep it.
- **But the gate as calibrated is a disguised stop.** "Candidate sponsor at break-even size" at M1 means 10,963 accounts. That is 14 FY2024 sponsors: 9 national standard, 3 donation processors, 1 religious, 1 single-issue. About two are plausible, and both are satisfied stayers. I would not worry about an entrant whose gate needs one of those two. Restate the gate in partner-book accounts, and after the allocation decision (M2 gives about 3,000 accounts) (REV4011).
- **Deciding OD-CDD-02 first is necessary but asks the second question first.** The first question is who performs and pays for the deep review. A partner reading revision 2 will see that Echelon expects to absorb $768k a year per sponsor and will either refuse or price that risk in. Raise the allocation decision alongside OD-CDD-02 (REV4012).
- **What I would actually do:** offer a renewal discount to the named candidate, or buy the partner. Revision 2 models partner acquisition and termination. It still defers renewal leakage (REV1042), and with only about 2-5 plausible targets that is the response that matters most. One leaked price quote can remove the only candidate sponsor.
- **Not self-defeating:** publishing "loss-making niche" internally costs nothing competitively. The risk is that the over-stated cost base becomes the owner's anchor and closes off the M2 and partner-vetting paths.

## 4. Product strategist

- **Population cap (`Sequences.fs:139`).** The cap uses `fst (eligible ...)`, which counts *all* FY2024 sponsors at or above the size, captive ones included, times the reachable share. The narrative and REV2012 say non-captive. The "non-captive" set also includes **donation processors**: 5 of the 10 non-captive sponsors at 5,291 or more accounts, and 3 of 5 at 10,963 or more. Their "DAF accounts" are workplace or payment giving funds, not buyers of a DAF platform. At 5,291 accounts the model allows 10 customers (25 × 0.4). Excluding national standard and processors leaves 5 candidates, which gives 2 at 0.4. This makes the upside and the favourable case optimistic. It is an *under*-correction (REV4006).
- **"Captive" is mis-specified the other way.** `national_standard` treats every national sponsor as running its own platform. Several bank- and brokerage-affiliated national sponsors outsource administration to third-party administrators. Those sponsors are the book a partner would bring, not captives. Classify sponsors by platform (own, third-party administrator, unknown) rather than by category (REV4006).
- **Cumulative cap and a static panel (`Cashflow.fs:139-140`).** The cap counts cumulative signings, so a churned customer is never replaced. A3 signs its 10th customer and live customers then decay to 6.1 by month 120. The FY2024 panel is also held fixed for ten years while sponsors grow into the size bands. Capping on live customers adds about $0.8M by month 120 (V9) (REV4007).
- **Partner book as the customer.** Accounts × price × (1 - share) is still the right *revenue* formula for a partner whose whole book is licensed. What changes is everything else. The cap becomes partners (a handful), not sponsors. CAC is paid per partner. Implementation and conversion are paid per sponsor in the book. Registry charities per account are higher for small sponsors. Charity overlap inside one book is high. Copy runs, 3 partners at 1 a year, base case:
  - 20,000-account book under M1: -$16.8M (worse than A3).
  - 20,000-account book under M2: +$1.5M, payback at month 85. With implementation ×5: -$0.2M.
  - 40,000-account book under M2: +$10.8M, payback at month 59. With implementation ×5: +$9.1M.

  Under M1-as-vendor-cost, scale makes the result worse, which confirms section 1. Add a partner-book stream with per-sponsor conversion inside it. Model H, as now set up, shows only small single sponsors with no book aggregation (REV4008).

## 5. Disposition audit (34 sampled: both rejections, all 17 deferrals, 15 high-severity accepted or partly accepted)

| Challenge | Disposition | Holds? | Finding (artifact checked) |
|---|---|---|---|
| REV1034 | rejected | **No (partly)** | The rationale defends the *requirement* (UNB-CDD-CIV-008) but not *who pays*. r1 and CNV-GRT-003 make the deep review a sponsor control (REV4013) |
| REV1037 | rejected | Yes | 07:21 and section 5 list candidates, not strengths; Transitus is stated as having no code |
| REV1042, REV2015, REV2021, REV2033, REV3029, REV3041, REV3042 | deferred | Yes | Listed as stated limits in 14 section 8 |
| REV3003, REV3006, REV3007, REV3008, REV3033, REV2026, REV2027, REV2037 | deferred | Yes, weakly | Recorded only in 20 and the register, not in 22 gaps or 18 limits. All are cost increases, so they are a counterweight to the over-statements found here |
| REV2024, REV2040 | deferred | Yes | P3-DEC-MOD003 exists in 25:56; see REV4011 on its threshold |
| REV1001, REV2012 | accepted | **No (partly)** | The "check excluding captive" exists only in a report table. The model cap uses all sponsors (`Sequences.fs:139`), and processors count as non-captive (REV4006, REV4017) |
| REV2003 | accepted | Procedurally yes; the change goes beyond the AB027 basis | Contingency on 120 months of steady-state run and registry (`Cashflow.fs:199`); effect $3.45M (REV4002) |
| REV2029 | accepted | **No** | Only a conventional-maintenance stress was added. The event-model platform residual (about $30 per account) is not in the base. The label should be "partly accepted" (REV4015) |
| REV3010, REV3020 | accepted | Yes on wording; **no on implementation** | RCH-09 remains shared vendor labour on the union. That conflicts with REV3011 (decisions in the sponsor cell) and with DEC-006 and DEC-002 (REV4001) |
| REV3011 | partly accepted | **No** | 11 changed, but the "marginal-sponsor recompute referred to MOD" never happened: `registry-components.csv` is unchanged and RCH-09 still has union scaling (REV4014) |
| REV3028 | partly accepted | **No (partly)** | P3-SEQ-FGJ004 was raised to high, but the generated P3-SEQ-MOD009 and `sequence-meta.csv` SEQ-H still say "moderate" (REV4016) |
| REV3004, REV3022 | accepted | Yes, with overlap | Control operations added but not netted against the AB010 approvers (REV4005) |
| REV3019 | accepted | Yes | `tpsp_annual` in the base; double count only in the adverse case |
| REV2001 | accepted | Yes | One whole customer; but fractional signing delays the pilot by 3 months (REV4009) |
| REV2034 | accepted | Yes | `RegistryAnnualOf` uses live sponsors (`Cashflow.fs:187`) |
| REV1021 | accepted | Yes | SOC lag in `Sequences.fs:149`; not binding for A3 base |
| REV1046 | accepted | Yes | A3B and A3X present in the inputs and outputs |
| REV3030 | accepted | Yes | A3 and H share the template; they differ by size |
| REV3037, REV3039 | accepted | Yes | `impl_first` 75/150/325 ×3 customers; go-live lag 6/9/12 in `sequence-values.csv` |
| REV1005 | partly accepted | Yes | 08:54 corrected to one founder |
| REV3001 | partly accepted | Yes | 02:43 lists the S3 exit criteria |

Result: 26 hold. 6 fail wholly or partly: REV1034, REV1001/REV2012 (counted as one), REV2029, REV3011, REV3028, and the implementation of REV3010/REV3020. One is procedurally right but goes beyond its stated basis (REV2003).

## Recommended changes (for reconciliation)

1. Add an owner decision on who performs the deep review under licensing. Make the governing base the vendor cost under sponsor-performed review (M2-like). Show M1-as-vendor-service only with matching service revenue.
2. Limit contingency to one-time cost, pre-revenue cost and the first 12 live months. Net control operations against AB010. Make M1 reviews demand-driven. Fix the wind-down base.
3. Cap on live customers, use non-captive non-processor sponsors, classify sponsors by platform, and add a partner-book stream.
4. Report the kill-rule result as timing-sensitive (whole first customer; lag 8 or 9; cost center at the gate).
5. Restate P3-DEC-MOD003's threshold after item 1.

Keep the decision: gate the spend and run V-3, V-9 and V-6 first.
