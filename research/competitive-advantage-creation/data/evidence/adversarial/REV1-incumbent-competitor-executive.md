# REV1 - Incumbent competitor executive

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV1. Perspective: chief strategy officer at a national DAF technology and administration provider with a funded balance sheet, an installed base of national, faith and community-foundation sponsors, an existing white-label programme and an acquisitions team. Written independently of the other REV1 perspectives. Challenge IDs P3-CHL-REV1001..REV1008 in [adversarial-challenges.csv](../../fragments/REV1/adversarial-challenges.csv). "Factual" means a checkable error or inconsistency in the package; "judgment" means I disagree with a reasonable reading.

## Bottom line

I would not crush this. I would ignore it, and the package's own model explains why ignoring it is the cheapest response. The only sequence that pays back (A3) needs customers that are already mine, the kill rule removes the entrant in three of four modelled draws before I need to act, and if a partner ever looks like it is working I can buy the partner. Nothing in the advantage register requires me to rebuild anything.

## 1. Your payback case is my installed base (P3-CHL-REV1001, high, factual + judgment)

Report 14 says only A and A3 pay back ([14](../../../14-commercial-sequencing.md):7), and only because they use Phase II ER-7 revenue of $150k/$300k/$600k net per customer (P3-ASM-AB030; `sequence-values.csv` TPL-UNB-S2 `revenue_per_customer`). The ER-7 basis says that is "~$81 per account less a 30% channel share on 3-10k-account sponsors" (`../competitive-displacement/data/model-inputs/entry-routes.csv` line 8). $300k / ($81 x 0.7) is about 5,300 accounts per customer.

I counted those sponsors in your own panel (SRC-013, `data/mission-2026-11-14/daf-long-tail-sponsors-fy2021-2024.csv`, FY2024 accounts, 1,480 sponsors with an account count):
- 25 sponsors have 5,300 or more accounts: 15 national, 5 donation processors (Givinga, AOGF, PayPal Giving Fund and others with their own technology), 3 religious, 2 other. **Zero community foundations.**
- In the 2,650-10,600 band that the $150k-$600k range implies, there are 18 sponsors: 9 national, 3 religious, 2 community foundations, 2 processors, 2 other.
- The median sponsor has 30.5 accounts; the median community foundation 47.

A3 base ends month 120 with 18.2 live customers after 8% churn at 3 signings a year ([14](../../../14-commercial-sequencing.md):73); that is roughly 25 signings, which is the entire population of sponsors at that size. Every one runs on an incumbent system today (mine or a peer's, or its own). So the "without displacement" framing of report 06 and the partner-module framing of DEC-001 do not describe the only sequence that works; A3 is a displacement campaign against my largest accounts, the segment Phase II already found switches least (1 of 26 national and faith sponsors left iPhi in 2023-26; Phase II [15](../../../../competitive-displacement/15-capital-and-break-even-reassessment.md):53, CHL-082). Report 16 then recommends exactly that: "Prefer channels whose customers pay at Phase II ER-7 scale" ([16](../../../16-capital-efficient-market-entry.md):246). P3-GAP-MOD003 flags the input conflict; it does not flag that the target population is roughly one sequence's worth of signings.

Proposed change: restate A3 as a displacement sequence; add a population check (sponsors by account band vs cumulative signings) to the model's validation; rerun A3 with revenue per customer drawn from the account distribution of sponsors not already on an incumbent platform.

## 2. I do not cut price; I buy your partner (P3-CHL-REV1002, high, judgment)

Report 16 says "the lean structure survives price responses that would sink the Phase II cost base" ([16](../../../16-capital-efficient-market-entry.md):11). Price is not my response. My precedent is acquisition: Ren-Pinkaloo, Ren-Stellar/iPhi, TIFIN-Amicus, Foundation Source-Vennfi (P3-CLM-EK009). Your extreme scenario "aggressive incumbent and partner acquired at month 36" gives A3 -$1.34M with no payback ([19](../../../19-sensitivity-and-stress-analysis.md):125). Your only protection is a change-of-control clause (P3-DEC-EK002), and report 12 concedes partners "will resist most of these terms" because "the leverage sits with them" ([12](../../../12-institutional-distribution.md):93). A partner that accepts change-of-control continuity for a single-founder vendor is a partner I can still outbid for the customer relationship. Judgment: the package should rank "loss of channel" as the base response, not a tail stress.

## 3. Nothing on your advantage list forces me to rebuild (P3-CHL-REV1003, medium, judgment; partly conceded by the package)

Report 07 finds zero architectural, organizational or distribution advantages and says every candidate is copyable in 6-30 months and none is built ([07](../../../07-architectural-competitive-advantages.md):9-21, 109). I agree, and I would go further on the economics built on top of it. The event model compares a 183-minute "conventional" account-year with the redesign ($267 vs $118 system cost per account-year, [18](../../../18-economic-model-methodology.md):87). That is not my baseline: my platform already auto-approves over half of grants and reuses vetting platform-wide (P3-CLM-EK002), and the package's own gap to a well-automated incumbent is $11-71 per account-year ([07](../../../07-architectural-competitive-advantages.md):94). Any sales material derived from the $267-to-$118 comparison would overstate the gap against me by roughly 2-13x. Proposed change: present event savings only against the MD-3/MD-4 "well-automated incumbent" baseline when the context is competitive.

## 4. Your walk-away price contradicts itself (P3-CHL-REV1004, medium, factual inconsistency)

Report 13 and P3-DEC-EK001 set the walk-away net price at about $73 per account-year on the Phase II MD-6 cost base ($1.81M fixed) ([13](../../../13-incumbent-response-model.md):7). Report 16 shows the lean licensor walk-away at $21.51 (five years) on $612k fixed and $12.15 variable ([16](../../../16-capital-efficient-market-entry.md):235). The decision register still carries $73 as the rule while the synthesis says MD-6 is a conventional-organization artefact. Either the decision should be restated on the lean base or the lean base is not believed. For me the practical point is different: a $21.51 floor is reached only because the founder takes $60k cash and the vendor variable cost is $12.15 against MD-6's $30.89 (P3-ASM-MOD003, P3-GAP-MOD004, unmeasured). I can match any price an entrant can survive at.

## 5. The founder is the whole company, and I will say so in every procurement (P3-CHL-REV1005, high, judgment)

`sequence-values.csv` sets `founder_fte` = 1 for every Unbound stream; report 14 shows 120 founder-months for A3 ([14](../../../14-commercial-sequencing.md):120). Over those months the founder is CEO, CTO, seller into partners, second-line support, compliance owner, registry accountable owner (0.15-0.5 FTE, [10](../../../10-structural-cost-elimination.md):186) and owner of 15+ other repositories ([09](../../../09-independent-component-commercialization.md):79). Report 08 calls it "a two-person company" ([08](../../../08-adjacent-financial-industries.md):54); the model has one. No capacity constraint is modelled, so the founder's time is priced (fully loaded) but never exhausted. In competitive deals I do not need a feature; I need the sentence "your donors' ledger depends on one person". Proposed change: add a founder-capacity constraint (hours per month across roles) and a key-person stress that pauses signings when it binds.

## 6. My cheapest response is to wait (P3-CHL-REV1006, medium, judgment)

With the kill rule applied, 75% of A3 Monte Carlo draws are paused and 76% have no payback within 120 months; the median economic result is -$765k ([19](../../../19-sensitivity-and-stress-analysis.md):93). The base-case statement that A3 "passes under every cost-center definition tested" ([14](../../../14-commercial-sequencing.md):264) is true of one path and false of three-quarters of the distribution. Report 16's answer-in-brief does not mention the paused share. Proposed change: put the paused share beside every A3 base figure.

## 7. Your time window is shorter than you think, and my funding is real (P3-CHL-REV1007, low, factual check - confirms the package)

The package states Bain Capital Tech Opportunities invested in Ren in 2023 and Great Hill in 2025 (P3-CLM-EK012). Both are confirmed: Bain-led strategic growth investment, July 2023 (https://www.businesswire.com/news/home/20230725652545/en/Ren-Secures-Strategic-Growth-Investment-Led-by-Bain-Capital-Tech-Opportunities, accessed 2026-11-26); Great Hill growth investment announced 2025-10-28 (https://www.businesswire.com/news/home/20251028702541/en/Great-Hill-Partners-Announces-Strategic-Growth-Investment-in-Philanthropy-Tech-Platform-Ren, accessed 2026-11-26). Blackbaud-EVERFI aggregate purchase price about $742.8M is confirmed by Blackbaud's FY2023 10-K (https://www.sec.gov/Archives/edgar/data/1280058/000128005824000013/blkb-20231231.htm, accessed 2026-11-26); YourCause appears in secondary sources as "$157 million", so the package's "$157.7M" ([13](../../../13-incumbent-response-model.md):19) should cite the 10-K figure or round. No change to conclusions.

## 8. The host-sponsor factory is a feature I already ship (P3-CHL-REV1008, medium, judgment)

P3-DEC-CD001 prefers new programmes hosted on an existing sponsor. Private label under an SLA (NPT, 14-16 weeks), turnkey launches (DAFtech 8 weeks, Givinga $12.5k base) and community-foundation hosting already exist ([06](../../../06-customer-acquisition-without-displacement.md):43; [07](../../../07-architectural-competitive-advantages.md):56-59). Report 06 lists "incumbents publish turnkey hosted-programme products" as a future condition that would change the conclusion ([06](../../../06-customer-acquisition-without-displacement.md):143), yet it is the present state. And your own model shows Sequence E never pays back (peak $4.46M, none in 120; [14](../../../14-commercial-sequencing.md):45).

## What I could copy, and how fast

| Claimed advantage | Already have | Copy time |
|---|---|---|
| Deterministic controls, automated vetting reuse (EK002, EK006) | Yes | 0 |
| Configuration onboarding, white label (EK004, EK019) | Yes | 0 |
| Published migration and exit commitments (EK021) | Contract clause | weeks |
| Replayable eligibility decisions (EK017) | Snapshot logging on existing vetting | 6-18 months, only if a deal is lost on it |
| Reconciliation-proved migration (EK010) | I control the export | n/a |
| Lean cost base (EK013-EK015) | No, but I do not need it: I respond with a renewal discount at the contested account | - |
