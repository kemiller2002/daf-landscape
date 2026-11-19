# Validation wave 38B: escaped-error cost (P-G0403-04) and sponsor economics (P-B40N14-04, P-B44N27-02)

*Validated 2026-11-19 by independent-validation-agent-wave38b. Nothing was committed or pushed.*

**Studies under validation**
- [g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md), with [`escaped-error-cost-2026-11-19.csv`](../../data/mission-2026-11-14/escaped-error-cost-2026-11-19.csv) and `scripts/mission_escaped_error_cost.py`.
- [b4014-b4427-sponsor-economics.md](b4014-b4427-sponsor-economics.md), with [`dechomai-share-of-sponsor-contributions-2026-11-19.csv`](../../data/mission-2026-11-14/dechomai-share-of-sponsor-contributions-2026-11-19.csv), [`sponsor-fee-revenue-margin-2026-11-19.csv`](../../data/mission-2026-11-14/sponsor-fee-revenue-margin-2026-11-19.csv) and `scripts/mission_sponsor_economics.py`.

**Register:** [`validation-register-wave38b.csv`](../../data/mission-2026-11-14/validation-register-wave38b.csv). V38B-01 to V38B-17 cover the escaped-error study; V38B-18 to V38B-32 cover sponsor economics.

**Method**
- **Reruns.** Both scripts were rerun with their `--out` options pointed at scratch, so the committed CSVs were never overwritten. md5 sums of the committed CSVs were taken before and after the runs and did not change.
  - `mission_escaped_error_cost.py` (10,000 draws, about 4 minutes) wrote 1,446 rows, byte-identical to the committed CSV.
  - `mission_sponsor_economics.py`, run on the q1427 XML and text folders, wrote both CSVs byte-identical to the committed files.
- **Independent recomputation.**
  - Part A Schedule D values were re-parsed directly from the 32 primary-match XMLs.
  - Shares, pooled ratios, fee bps, DAF m cells, composite decomposition and per-SAR statutory shares were recomputed outside the scripts.
- **Re-fetched sources.**
  - Five FinCEN orders: BofA 2026-03, TD 2024-02, USAA 2022-01, CBOT 2021-03 and Canaccord 2026-01.
  - 26 U.S.C. §4966 and §4967 on LII.
  - Five audits: Fidelity FY6/24, RCF 2024, JCF FY6/24, Vanguard FY6/25 and NCF 2024.
- **Retrieval rules.**
  - Every fetch used the generic agent `research-script/1.0`, after reading each host's robots.txt with `urllib.robotparser`. All target paths were allowed.
  - LII's crawl-delay of 10 seconds was respected.
  - Nothing was fetched from sec.gov, crt.sh or certspotter, and there was no outreach.

## Counts

| Result | Escaped-error cost | Sponsor economics | Total |
|---|---:|---:|---:|
| confirmed | 12 | 8 | 20 |
| partially_confirmed | 3 | 7 | 10 |
| contradicted | 2 | 0 | 2 |
| unverifiable | 0 | 0 | 0 |
| **Total** | **17** | **15** | **32** |

## Findings: escaped-error cost

### Replication (V38B-01, -02): confirmed
- The rerun is byte-identical to the committed CSV.
- The route cells reproduce `ai-routing-variant-2026-11-19.csv`, for example route m = 1 at $1,364,949 and m = 5 at $1,062,284.

### FinCEN orders (V38B-03 to -06): confirmed
Every count, penalty and credit quoted in the study is in the order text.

| Order | Penalty | Credit | Count |
|---|---|---|---|
| BofA | $1.2bn | $750m OCC | "nearly 8,900" missed SARs; "over 8,000" filed in review |
| TD | $1.3bn | $543m (DOJ and OCC); $757m to Treasury | "over 6,000" late SARs |
| USAA | $140m | $60m OCC | "at least 3,873" SARs, averaging 226 days |
| CBOT | $8m | $1m OCC | "at least 17" SARs |

- The BofA order also states "800 consultants". The TD order also states $1.89bn DOJ, $123.5m FRB and $450m OCC.
- Per-unit arithmetic reproduces: $134,831, $216,667 (all agencies $536,750), $36,148, $1,556 per alert and $470,588.
- The TD order adds a fact the study does not quote: the late-reported activity "exceeded $500 million".

### Per-SAR statutory maximum (V38B-07): partially confirmed
- **The caps are those stated in each order**, and the arithmetic reproduces:
  - BofA $286,184: share 0.471;
  - TD $278,937: share 0.777;
  - USAA $250,759: share 0.144;
  - Canaccord $286,184: share 1.747.
- **CBOT is left blank but is computable.** Its order states a $236,071 cap after 2 November 2015, so 8,000,000 ÷ (17 × 236,071) = **1.99**. CBOT, like Canaccord, exceeds what SAR violations alone could carry.
- **Every share is a lower bound.** Each SAR is priced at the cap, but where a SAR's amount is below the cap the statutory maximum is the amount. TD's $500m over 6,000 SARs averages about $83k, so TD's true share could exceed 1.

### Handling units, lookback and statute (V38B-08 to -10): confirmed
- **Handling units.** $55.45/h and the P14 5 / 15 / 40 minutes come from `ai-process-economics.csv`. gap19 does not restate them; it inherits v2's minutes.
- **Lookback.** 374 / 748 / 1,496 units reproduce.
- **Statute.** The LII text confirms:
  - §4966: 20% on the sponsor; 5% on the fund manager, capped at $10,000.
  - §4967: 125% on the donor or advisor; 10% on the fund manager, capped at $10,000.

### P08 as a sponsor cost (V38B-11): contradicted
- §4967 imposes no tax on the sponsoring organization. Its (a)(2) tax falls on a fund manager who agreed "knowing" the benefit.
- The study excludes the §4966 manager tax as "not sponsor costs" but keeps the identical §4967 manager tax for P08.
- **Effect of applying the study's own rule:** the composite m falls from 2.42 to 2.20 (central) and from 106 to 88.5 (high).

### Central m = 2.4 (V38B-12, -13): arithmetic confirmed; framing partially confirmed
- **The arithmetic reproduces (V38B-12).** Every DAF m cell recomputes.
- **The decomposition of 2.419 shows it is assumption-led (V38B-13):**

  | Component | Contribution | Source |
  |---|---:|---|
  | Operational m = 2 on 50.7% of the weight | 1.01 | Unsourced |
  | Correction unit (compliance processes) | 0.49 | Model convention |
  | P07 excise | 0.43 | §4966 |
  | P08 excise | 0.22 | Manager-only §4967 tax |
  | Bank transfer | 0.26 | Unsourced |

- With operational m = 1 the composite is 1.91.
- The table in §4.3 calls 2.4 "the sourced central m", which overstates its basis. The study's own recommendation to report the process-specific variant is the right reading.

### Bank-to-DAF analogy and break-even (V38B-14, -15): confirmed
- The analogy is consistently labelled [I] (§5, bottom-line items 2, 4, 5 and 7).
- Break-even m reproduces: p05 11.30, p50 21.66, p95 199.2.
- The central m lies above break-even in 0% of draws, the high m in 89.7%.

### Rerun headlines (V38B-16): partially confirmed
- The pools reproduce: $1,259,839 at the central composite, $534,970 and $753,432 at the process-specific high setting, and $844,080 under full compliance re-review.
- **"C's mean rank-first probability is at most 0.032" holds only for the large national at the central or high setting.** It is:
  - 0.039 at the large national under the process-specific low setting;
  - 0.043 at the community-foundation archetypes (hybrid, m = 1 or process-specific low).

### Repo passages (V38B-17): contradicted
- FINAL-STATUS says routing helps "only when an escaped error costs about one case-handling's worth or less". The routing CSV contradicts this: at m = 5 the pool is $1.06m and at m = 10 it is $623k, both above the $445k assist pool.
- The routing note, the BD recut and synthesis §0 still call m unsourced. Corrections are given below.

## Findings: sponsor economics

### Replication and Part A (V38B-18 to -21)
- **Confirmed.**
  - Both CSVs are byte-identical on rerun.
  - The 32 Schedule D values match an independent XML parse to the dollar.
  - Every pooled share reproduces, including the EIN variant (AEF 4.11%, DAFgiving360 0.98%) and DAFgiving360's CY2022 share of 1.63%.
- **Partially confirmed: "pooled ratios move little".** This holds for June-year sponsors only (at most 0.14 points). For calendar-year sponsors the t−1 pools differ by up to 0.74 points: AEF 2.97% against 3.71%, and BofA 1.54% against 2.20%.

### Fidelity (V38B-22, -23): confirmed
- **Note 7** reads: the Gift Fund "paid FMR at amounts equal to the administrative fee the Gift Fund charged its donors".
- **Operating costs reproduce:**
  - administrative fees $121,190,522 and $139,686,600;
  - professional fees $1,308,861 and $1,216,669;
  - other expenses $9,982,465 and $20,670,116.
- **Effective fee.** 23.4 and 22.9 bps reproduce from Schedule D DAF values.
- **The tier-credit explanation is supported** by Note 2: a 0.60% base fee, quarterly tier price credits, and credits of $20,833,827 (2023) and $23,199,953 (2024).

### RCF (V38B-24): partially confirmed
- **Note 9 wording and the payments reproduce.** Ren is paid "98% of the value of administrative fee revenue earned by the Foundation from individual fund holder accounts": $19,225,546 (2024) and $15,543,682 (2023).
- **The 98% is not the share of the whole fee line in 2023.** The 2023 payment is 96.6% of the $16,097,870 fee line; the 2024 payment is 98.0%.

### JCF (V38B-25): partially confirmed
- **Note C wording, fees and operating costs reproduce.**
- **The UJA grant is not fixed.** The study says JCF "must grant $2.0m a year". Note C makes the grant conditional: fees and interest income in excess of operating expenses, "up to an amount of $2,000,000", are granted to UJA.

### Vanguard (V38B-26): confirmed
- Note 7 says the 0.60% base fee "is wrapped in with investment income".
- FY2024 operating costs total $36,812,064, and Vanguard's own service fee is $3,916,396.

### NCF (V38B-27, -28)
- **Confirmed: the figures.**
  - NCCF fees: $42,004k and $47,411k.
  - G&A plus fund-raising: $111,478k and $124,191k.
  - Eliminated fees: $55,165k and $61,122k.
- **Partially confirmed: the margin.**
  - The eliminations column removes $55.2m and $61.1m from G&A, so the column G&A includes fee payments between group entities.
  - The NCCF column's G&A plus fund-raising exceeds NCCF's own 990 operating cost ($71.8m and $80.8m) by $39.7m and $43.4m.
  - Against the 990 cost, the margin is about −71% and −70%, not −165% and −162%.

### Effective fee rates (V38B-29): partially confirmed
- **Fidelity, RCF and JCF are asset-based fees**, so their bps are comparable.
- **NCF's 89 bps is not an asset-based rate.** NCF says its fee is "typically based on a standard percentage of assets donated" and charges it on non-DAF charitable funds too.
- **CJP's 8.7–8.9 bps is not a donor fee.** It is an interfund fee from the DAF area to CJP Operations.

### 990 proxy against the resilience study (V38B-30, -31): partially confirmed
- **The numbers hold.** ΔR1 does not reproduce audited fee margins at Fidelity, RCF or NCF.
- **"Contradicts" overstates the case.** The resilience study already showed that Fidelity's R1 equals its "other funds", and it defined ΔR1 to include returns on own funds.
- **Two resilience claims are contradicted by the audits:**
  - §6: ΔR1 of about +0.4× operating cost at affiliated nationals shows "fees retained exceed costs";
  - §1: the fee transfer "never passes through Part VIII". RCF books it as revenue, as the resilience study's own §4 notes.
- **The JCF "close match" depends on using the pre-grant surplus.** The UJA grant leaves the operating fund. Against the post-grant surplus, ΔR1 is higher by $1.56m (FY2023) and $1.18m (FY2024).

### Coverage (V38B-32): confirmed
- 25 FY2024 statuses: 12 read, 1 summary only, 1 consolidated, 2 on request, 4 not posted and 5 blocked.
- Every FY2024 990 answers `FSAuditedInd` true or 1.
- The fee is disclosed at 5 sponsors.

## Exact corrections

### `research/mission-2026-11-14/g0403-04-escaped-error-cost.md`

- **Find:** "The FinCEN penalty was 47% of the statutory per-SAR maximum for BofA, 78% for TD and 14% for USAA. For Canaccord it was 175%, which exceeds what the SAR violations alone could carry [C]."
- **Replace with:** "The FinCEN penalty was at least 47% of the statutory per-SAR maximum for BofA, 78% for TD and 14% for USAA. These are lower bounds, because each SAR is priced at the order’s cap although the maximum is the transaction amount where that is lower; TD’s order puts its late-reported activity at “over $500 million” across the 6,000 SARs. For Canaccord it was 175%, and for CBOT 199% (17 SARs at its order’s $236,071 cap); both exceed what the SAR violations alone could carry [C]. [V wave 38B]"

- **Find:** "- The CBOT figure shows the small-count problem: 17 SARs against an $8m penalty for a five-year program failure."
- **Replace with:** "- The CBOT figure shows the small-count problem: 17 SARs against an $8m penalty for a five-year program failure. At the $236,071 per-SAR cap stated in the CBOT order, the penalty is 1.99× the SAR-only statutory maximum, so like Canaccord it cannot be carried by the SAR violations alone [C]. [V wave 38B]"

- **Find:** "- The 125% tax on the donor or advisor (§4967(a)(1)) and the 5% manager tax under §4966 are not sponsor costs, so they are excluded."
- **Replace with:** "- The 125% tax on the donor or advisor (§4967(a)(1)) and the 5% manager tax under §4966 are not sponsor costs, so they are excluded. By the same rule the §4967(a)(2) tax used for P08 is not a sponsor cost either: §4967 taxes only the advisor or related person and a fund manager who agreed “knowing” the benefit, and nothing falls on the sponsoring organization. P08 is kept only as a proxy for exposure through the sponsor’s managers. With P08 at its correction unit alone, the composite m is 2.20 (central) and 88.5 (high), not 2.42 and 106 [C]. [V wave 38B]"

- **Find:** "- **1–106, central 2.4** [I], resting on IRC §4966/§4967 rates [F], grant anchors [F in repo] and the model's handling costs [C]."
- **Replace with:** "- **1–106, central 2.4** [I], resting on IRC §4966/§4967 rates [F], grant anchors [F in repo] and the model's handling costs [C]. Of the central 2.42, only about 0.65 comes from the excise rates (0.43 from §4966 on P07, 0.22 from the manager-only §4967 tax on P08). The rest is 1.01 from the unsourced operational m = 2 on the 51% of weight outside compliance, 0.49 from correction units and 0.26 from the unsourced bank transfer. With operational m = 1 the composite is 1.91 [C]. [V wave 38B]"

- **Find:** "**Bounded.** The sourced central m (2.4) sits in the range where routing holds about 92% of its m = 1 pool at a large national."
- **Replace with:** "**Bounded.** The central m (2.4, mostly assumption-driven: §4.2) sits in the range where routing holds about 92% of its m = 1 pool at a large national. [V wave 38B]"

- **Find:** "C's mean rank-first probability is at most 0.032 (hybrid, process-specific central) [S]."
- **Replace with:** "C's mean rank-first probability is at most 0.032 at a large national under the process-specific central setting (hybrid). It is 0.039 there under process-specific low, and at most 0.043 at any archetype (hybrid, m = 1 or process-specific low, community foundations) [S]. [V wave 38B]"

### `research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md`

- **Find:** "m is the cost of an escaped error, in units of one case's handling time. It has no public source, so it is a sweep [I]."
- **Replace with:** "m is the cost of an escaped error, in units of one case's handling time. It has no direct public source, so it is a sweep [I]. The escaped-error study ([g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md)) bounds it at 1.0–106 from IRC §4966/§4967 rates and bank SAR penalties. Its central 2.4 is mostly assumption-driven, and at m = 2.42 the large-national routing pool is $1.26m [S]. [V wave 38B]"

- **Find:** "3. **m (the cost of an escaped error) is unsourced** and dominates the result (P-G0401-02)."
- **Replace with:** "3. **m (the cost of an escaped error) is only indirectly sourced** and dominates the result (P-G0401-02). Wave 38B bounds it at 1.0–106 (central 2.4), but detection probability, the bank-to-DAF transfer and operational rework remain unsourced (P-G0403-04). [V wave 38B]"

### `research/mission-2026-11-14/g0401-0103-ai-bd-recut.md`

- **Find:** "m remains unsourced: the BofA order suggests escaped-error costs in compliance can be very large (P-G0403-04)."
- **Replace with:** "m is now bounded ([g0403-04-escaped-error-cost.md](g0403-04-escaped-error-cost.md)). Conditional on enforcement, a missed SAR at the four core depository banks cost $36k–$471k in FinCEN penalty (2,600–34,000 P14 handling units). The DAF excise regime gives 1–174 units per escaped P07/P08 error, and the composite central m is 2.4 [C/I]. [V wave 38B]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "raises the large-national pool to $1.06–1.36m if an escaped error costs 1–5 handling-times (an unsourced sweep [I]; $44k at 20)."
- **Replace with:** "raises the large-national pool to $1.06–1.36m if an escaped error costs 1–5 handling-times ($44k at 20). Wave 38B bounds m at 1.0–106 with a mostly assumption-driven central 2.4 ($1.26m). Bank-style AML enforcement (thousands of handling units per missed SAR) would rule out auto-closing wherever such errors can escape [C/I]. [V wave 38B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "Confidence-gated routing roughly triples intervention C's value pool, but only when an escaped error costs about one case-handling's worth or less."
- **Replace with:** "Confidence-gated routing roughly triples intervention C's value pool when an escaped error costs one case-handling's worth. It still beats assistance up to about ten, and the pool falls below assist near m = 20. Wave 38B's central m is 2.4, but bank-style compliance errors that escape would erase the gain. [V wave 38B]"

### `research/mission-2026-11-14/direction-sponsor-financial-resilience.md`

- **Find:** "- **[I]** ΔR1 is the preferred operating-result proxy. A DAF administrative fee moves value from DAF balances into sponsor-owned funds, and that transfer never passes through Part VIII."
- **Replace with:** "- **[I]** ΔR1 was proposed as the operating-result proxy, on the view that a DAF administrative fee moves value from DAF balances into sponsor-owned funds without passing through Part VIII. Audited statements do not support it as a margin ([b4014-b4427-sponsor-economics.md](b4014-b4427-sponsor-economics.md)). ΔR1 exceeds audited fee less operating expense by $47.6m and $70.7m at Fidelity, which pays its fee to FMR one for one; by $6.3m and $57.0m at RCF, which books its fee as Part VIII revenue; and by $129.3m and $182.6m at NCF. Only at JCF is it within about $1.6m. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B]"

- **Find:** "At affiliated nationals ΔR1 runs at about +0.4× operating cost each year, so fees retained exceed costs."
- **Replace with:** "At affiliated nationals ΔR1 runs at about +0.4× operating cost each year. That does not show that fees retained exceed costs. Fidelity pays FMR an amount equal to its fee, and its other costs exceed the fee by $11.3m (FY2023) and $21.9m (FY2024). RCF passes 98% of its fee from fund holder accounts to Ren, leaving a $0.15–0.28m surplus (audits read in wave 38B). [V wave 38B]"

- **Find:** "6. **Operating surplus: the 990 headline is uninformative, and the change in non-DAF net assets is the better signal [C].**"
- **Replace with:** "6. **Operating surplus: the 990 headline is uninformative. The change in non-DAF net assets is a better balance-sheet signal, but audits show it is not an operating margin [C].** [V wave 38B]"

### `research/mission-2026-11-14/b4014-b4427-sponsor-economics.md`

- **Find:** "3. **The fiscal-year choice moves single years a lot but pooled ratios little [C].**"
- **Replace with:** "3. **The fiscal-year choice moves single years a lot but pooled ratios little at June-year sponsors [C].** For calendar-year sponsors the three-year t−1 pools differ by up to 0.74 points (AEF 2.97% vs 3.71%; BofA 1.54% vs 2.20%). [V wave 38B]"

- **Find:** "- JCF must grant $2.0m a year from its operating fund to UJA."
- **Replace with:** "- Under Note C, fees and interest income in excess of operating expenses, up to $2,000,000, are granted to UJA; the operating fund granted $2.0m to UJA in each year (Note E). [V wave 38B]"

- **Find:** "- NCCF's fee does not cover G&A plus fund-raising, which is funded otherwise [I]."
- **Replace with:** "- NCCF's fee does not cover G&A plus fund-raising, which is funded otherwise [I]. The NCCF column's G&A likely includes fee payments between group entities: the eliminations column removes $55.2m and $61.1m from G&A, and the column's G&A plus fund-raising exceeds NCCF's own 990 operating cost ($71.8m and $80.8m). Against that 990 cost the gap is −$29.8m (−71.0%) and −$33.4m (−70.4%). On the consolidated statement, all-entity fees of $55.2m and $61.1m compare with G&A plus fund-raising after eliminations of $117.5m and $106.1m [C]. [V wave 38B]"

- **Find:** "- **JCF** is the only close match: ΔR1 of +$1.8m and +$3.0m against a fee surplus of $2.2m and $3.8m (after the UJA grant, $0.2m and $1.8m)."
- **Replace with:** "- **JCF** is the closest match: ΔR1 of +$1.8m and +$3.0m against a fee surplus of $2.2m and $3.8m (after the UJA grant, $0.2m and $1.8m). Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B]"

- **Find:** "The audits show it mostly measures other-fund and endowment movements [I]."
- **Replace with:** "The audits show it mostly measures other-fund and endowment movements [I]. This qualifies the resilience study rather than contradicting it: that study already showed Fidelity’s R1 equal to its “other funds” and defined ΔR1 to include returns on own funds. What the audits do contradict is its reading that ΔR1 of about +0.4× operating cost at affiliated nationals means “fees retained exceed costs”: Fidelity retains none of its fee, and RCF retains 2%. [V wave 38B]"

- **Find:** "- **RCF.** Opex = M&G + fundraising."
- **Replace with:** "- **RCF.** Opex = M&G + fundraising. Note 9 bases Ren’s fee on 98% of administrative fee revenue “from individual fund holder accounts”. The FY2023 payment ($15,543,682) is 96.6% of the $16,097,870 fee line, and the FY2024 payment is 98.0% [C]. [V wave 38B]"

- **Find:** "  - `internal_fee_bps_of_avg_daf_value` = fee ÷ the mean of the BOY and EOY Schedule D DAF value."
- **Replace with:** "  - `internal_fee_bps_of_avg_daf_value` = fee ÷ the mean of the BOY and EOY Schedule D DAF value. The rates are not like-for-like across sponsors. NCF assesses ministry support fees on DAFs and other charitable funds, “typically based on a standard percentage of assets donated”, so its 89 bps is not an asset-based rate. CJP’s figure is an interfund fee from the DAF area to CJP Operations, not the donor fee. Compare bps only for Fidelity, RCF and JCF [I]. [V wave 38B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.46 Escaped-error cost and sponsor fee economics (validated, wave 38B)\n\n**Escaped-error cost and sponsor fee economics** (validated, wave 38B). Four FinCEN orders against depository banks that count missed or late SARs (Bank of America 2026, TD 2024, USAA 2022 and CommunityBank of Texas 2021) imply $36k–$471k of penalty per SAR, conditional on enforcement. That is 2,600–34,000 fifteen-minute AML handling units. CBOT’s and Canaccord’s penalties exceed the per-SAR statutory maximum, so penalties follow programme failure, not SAR counts. A DAF sponsor itself faces only IRC §4966’s 20% tax on a taxable distribution; §4967’s 10% falls on fund managers. The proposed escaped-error cost for the AI routing model is 1.0–106 handling units. Its central value of 2.4 rests mostly on assumed rework. At that value routing keeps a $1.26m large-national pool against $445k for assistance, and assistance is still the likely winner in no process. Dechomai’s 2021–24 grants equal 0.11–2.97% of eight sponsors’ Schedule D DAF contributions, or 4.11% at AEF if the $76.4m “Schwab” line follows its EIN. Audits show Fidelity passes its DAF fee to its administrator one for one and RCF passes on 98%, while JCF keeps 20–33% before its UJA grant. The 990 balance-sheet proxy does not reproduce these margins. [V wave 38B]\n\n---\n\n## Source register"
