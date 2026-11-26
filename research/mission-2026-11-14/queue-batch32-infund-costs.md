# In-fund cost per DAF dollar at the nationals (P-B31A-02), Fidelity CIAP adviser-fee rate (P-B31A-01), where MS GIFT's wrap fees sit (P-B31A-03), Schedule G platform screen (P-COST-05)

**Date:** 2026-11-15 · **Queue items:** P-B31A-02, P-B31A-01, P-B31A-03, P-COST-05 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs:**
- [`data/mission-2026-11-14/infund-expense-nationals-2026.csv`](../../data/mission-2026-11-14/infund-expense-nationals-2026.csv): 94 rows (N001–N094). It covers Fidelity pool-by-pool in-fund cost for FY2025 and FY2024, expense-ratio ranges for Vanguard, DAFgiving360 and NPT, Part IX operating cost, all-in sums, the Fidelity CIAP adviser-fee ratios, the MS GIFT fee-location rows, and a line-3 investment-income test on 13 returns.
- [`data/mission-2026-11-14/schedule-g-screen.csv`](../../data/mission-2026-11-14/schedule-g-screen.csv): 211 flagged returns (97 EINs) out of 5,272 screened.
- [`data/mission-2026-11-14/queue-proposals-batch32a.csv`](../../data/mission-2026-11-14/queue-proposals-batch32a.csv): P-B32A-01 to P-B32A-03.
- Scripts (stdlib, functional style): [`scripts/mission_infund_costs.py`](../../scripts/mission_infund_costs.py) and [`scripts/mission_schedule_g_screen.py`](../../scripts/mission_schedule_g_screen.py).

**Method and rules.**
- **Sources:** public PDFs and pages, plus IRS e-file XML from the GivingTuesday mirror. I did not log in, submit forms or contact anyone.
- **Arithmetic:** every number below comes from the two scripts.
  - Fidelity audit figures are transcribed into constants. `--verify-dir` checks that all 71 of them appear verbatim in the `pdftotext` output of the three audits; the result was 71/71, none missing.
  - Pool balances are asserted to sum to the audit total.
- **Recency:** all sources date from 2022–2026. One exception: an MS GIFT 2018 annual report surfaced in search and was not used.
- **Labels:** **[F]** first-party document or filing; **[R]** search-engine capture; **[3P]** third party; **[C]** my computation; **[I]** my inference.
- **Governing corrections from wave 16:** the audit-netting add-back is **Schedule D Part XII line 4a**, e-file tag `InvestmentExpensesNotIncld2Amt`. Part XII line 4b (`OtherExpensesNotIncludedAmt`) is "Other". Both scripts read these tags separately.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-B31A-02: asset-weighted in-fund expense per DAF dollar** | **Fidelity is the only large national that publishes pool assets, in Note 3 of its audit. Its asset-weighted pool expense ratio is 26.3 bps in FY2025 (27.4 bps in FY2024), on $42.1bn of pools.**<br>- **Per dollar of total investments:** that is 13.9 bps (15.0 bps in FY2024), because 47% of investments sit in CIAP accounts whose fund costs are not published.<br>- **Fidelity all-in:** adding Part IX operating cost including 11f (37.6 bps) gives at least **51.5 bps per invested dollar**. If CIAP mutual funds carry the pool-average ratio, the in-fund layer rises to 17.2 bps [C].<br>- **Why Fidelity's pool layer is low:** 20% of pool assets are in the 0.015% Total Market Index pool, and 25% are in the 0.14% money-market pool.<br>- **Vanguard, DAFgiving360 and NPT publish expense ratios but not pool assets,** so only bounds are possible:<br>  - Vanguard: 1–59 bps in-fund; all-in 19–77 bps.<br>  - DAFgiving360: 3–67 bps; all-in 37–100 bps.<br>  - NPT: 7–61 bps, plus a 10–15 bps advisory fee assumed to sit in 11f; all-in 40–94 bps.<br>- **Comparison with community foundations:** even the upper bounds stay below the 196 bps community-foundation median of Part IX operating cost. That median itself excludes the foundations' own pool fees. | High for Fidelity pools [F/C]; bounds only for the others |
| **P-B31A-01: Fidelity CIAP adviser-fee rate** | **The audited "Investment management fees" line equals 990 line 11f exactly: $84.3m in FY2025, $67.3m in FY2024 and $53.7m in FY2023.**<br>- **Rate:** divided by average CIAP advisor-managed investments ($32.3bn in FY2025), it is a stable **26.1 / 26.9 / 26.5 bps** [F/C].<br>- **With the line-24 item:** adding the 990 line-24 item "OTH CHARITABL INV ADVISOR PRGM" gives **30.9 bps (FY2025) and 35.2 bps (FY2024)**. That item reconciles to the audit's "Other expenses" line (FY2025 after removing $5.70m of tax payments).<br>- **No netting:** Fidelity books these fees gross. FY2025 Schedule D has no Part XI/XII, and FY2024 has no line 4a.<br>- **Against AEF:** this is about 60% of AEF's 0.40–0.46%. It is an average over all CIAP dollars, including accounts whose advisers bill outside the DAF. | Medium-high on the ratio [F/C]; medium on composition [I] |
| **P-B31A-03: where MS GIFT's advisory fee (cap 1.00%) and MSSB admin fee (0.07%) appear** | **They appear nowhere as expenses, in either the 990 or the reconciliation to the audit.**<br>- **Visible advisory-type lines:** 7.8 bps ($6.27m) against an $80.9m ceiling.<br>- **Reconciliation:** every Schedule D Part XI/XII line is zero, so the audit nets them the same way the 990 does.<br>- **Mechanism:** the current Select UMA wrap brochure (2026-11-04) describes the Morgan Stanley Advisory Fee as a wrap fee charged on the account, covering advice, custody, execution and FA pay. A 0.035% platform fee is added to it.<br>- **New signal:** MS GIFT's Part VIII line 3 investment income is **4–35 bps of average assets in TY2022–24**. Eleven peer nationals report **128–424 bps**. That fits fees being taken out of account income before it is reported [I].<br>- **Total-return proxy:** it does not separate MS GIFT from peers, so the size of the netted layer stays unmeasured.<br>- **No public MS GIFT audit was found for 2021–2025.** | High that the fees are off-statement [F]; medium on the mechanism [I] |
| **P-COST-05: Schedule G platform screen** | **Of 5,272 returns, 1,626 answer Yes on Part IV lines 17–19 and file Schedule G, and 302 list Part I line 2b fundraisers.**<br>**Three sponsors besides Givinga have the platform pattern:** sweepstakes or online agents collect gross receipts that become DAF contributions, the agent keeps 40–85%, and line 11e is 56–99% of operating cost.<br>- **Pledgeling Foundation:** Charitybuzz and Prizeo; $36.8–38.9m gross, about 62% of contributions; 20–23k DAF accounts.<br>- **Charities Aid Foundation America:** Omaze; $105.3m gross in 2022, of which Omaze kept $84.1m, with the agent controlling funds; $30.7m in 2023, then near zero.<br>- **Our Change Foundation:** Omaze, Jackpocket, Zeal and Fandiem online sweepstakes; $14.7m gross in 2025, about 63% of contributions.<br>**Two low-take pass-throughs, already known:** Network for Good (Bonterra, gross equal to 99–100% of contributions, 1.1–1.4% kept) and U.S. Charitable Gift Trust (Eaton Vance Distributors, 100%, 2.3–2.8% kept).<br>**Line-11e-heavy but no gross-receipt agent:** Barrow CF and Givio. | High on filings [F]; DAF-total impact [I] |

---

## 1. P-B31A-02: asset-weighted in-fund cost

### 1.1 Fidelity (pool assets published)

**Sources:**
- Pool balances at 30 June 2025 and 2024 come from Note 3 of the [FY2025/24 audited consolidated financial statements](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf) [F]. There are 26 pools, totalling $42,093,730,030 and $33,968,194,205.
- Net and gross pool expense ratios come from the [What it costs](https://www.fidelitycharitable.org/giving-account/what-it-costs.html) page [F]. The page says the ratios "reflect the fees assessed by the underlying funds of the pools", and its pool data refers to 2026-09-30.
- Two pools are not on the expense-ratio page: Impact Investing ($220.7m) and Charitable Cash ($1.1m).

| Measure (rows) | FY2025 | FY2024 |
|---|---|---|
| Weighted net ER, priced pools (N027/N057) | **26.3 bps** ($110.0m) | 27.4 bps ($92.4m) |
| Gross-ER basis | in N027 notes | in N057 notes |
| All pools, unpriced pools at 0% or 0.93% (N028/N058) | 26.1–26.6 bps | 27.2–27.9 bps |
| Per dollar of total investments, CIAP in-fund cost = 0 (N029/N059) | **13.9 bps** | 15.0 bps |
| Sensitivity: CIAP mutual funds at the pool-weighted ER (N030/N060) | 17.2 bps | 18.9 bps |

**Reading [C/I]:**
- **Where the weight sits:** the largest pools are Money Market ($10.56bn at 0.14%) and Total Market Index ($8.44bn at 0.015%). Together they are 45% of pool assets and keep the average low. The asset-allocation pools ($11.8bn) cost 0.45–0.56%.
- **Timing mismatch:** the expense ratios are current (2026) while the assets are at June 2025. Applying 2026 ratios to the FY2024 weights assumes the funds have not changed.
- **CIAP is the blind spot:** CIAP holds $37.1bn, made up of $10.1bn mutual funds, $7.1bn alternatives and private equity, $15.6bn equities and $4.4bn fixed income. Its fund-level and alternative-fund fees sit inside NAV, and nothing published quantifies them. The 13.9 bps per-dollar figure is therefore a floor.

### 1.2 Sponsors without published pool assets

| Sponsor | Published pool cost | Source | Pool assets? |
|---|---|---|---|
| Vanguard Charitable | 70 expense-ratio entries "Last updated 09/30/2026", 0.01–0.59%. Index building blocks 0.01–0.11%, values-driven 0.09–0.59%. The fees page example shows an "Average investment fee" of 0.06% on a $750k account | [investments](https://www.vanguardcharitable.org/investments); [fees](https://www.vanguardcharitable.org/fees-and-expenses) [F] | Not published, and no audit found online |
| DAFgiving360 | SWTSX 0.03% to about 0.66–0.67% (JBALX, PAXIX/CBAIX) | repo rows in `queue-adviser-fees-pools-npact.md` §2 [R/3P]; dafgiving360.org returned 403 | Not published. The only audit found online is FY2020 |
| NPT | Weighted average management fee 0.07–0.61% across 7 portfolios, plus a "0.10% investment advisory fee" (0.15% for impact) and trading costs "up to 4 cents per share" | [Investment descriptions PDF, NPT FOR IDAP 0926](https://www.nptrust.org/investment-descriptions-and-performance-npt/) [F] | Not published. NPT's adviser-managed share is not estimable: segregated accounts need $500,000, and line 11f mixes model-portfolio advisory fees with segregated-account fees (g0702-b4531 §2.5) [V wave 35B] |

### 1.3 All-in per dollar (rows N064–N072)

| Sponsor | Part IX operating cost incl. 11f | In-fund | All-in |
|---|---|---|---|
| Fidelity FY2025 | 37.6 bps | 13.9 bps (floor) | **≥ 51.5 bps** |
| Vanguard FY2024 | 18.4 bps | 1–59 bps | 19–77 bps |
| DAFgiving360 FY2025 | 33.5 bps | 3–67 bps | 37–100 bps |
| NPT FY2025 | 32.7 bps | 7–61 bps | 40–94 bps |
| MS GIFT TY2024 | 28.1 bps | not published; up to 107 bps of advisory and MSSB fees sit off-statement (§3) | ≤ ~135 bps plus fund fees |

**Consequence for the cost-to-serve comparison:** the nationals-versus-community gap (18–66 bps against 196 bps) narrows once in-fund cost is added, but it does not close for the index-heavy nationals. The comparison is still biased toward the nationals in one respect: community-foundation pool fees (11f, plus in-fund fees such as the SFF Long-Term Pool's 1.02–1.10%) would also need adding to their side.

---

## 2. P-B31A-01: Fidelity CIAP adviser-fee rate

**Sources:**
- **Audits [F]:** [FY2025/24](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf), [FY2024/23](https://fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf) and [FY2023/22](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf).
- **990 XML [F]:** [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) and [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml).
- **Program terms [F]:** the [CIAP overview](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf) sets a $100,000 minimum and says "Advisors may assess a fee". Fidelity's admin fee on CIAP is 60/30/20/15 bps tiered, then flat at 19 down to 11.5 bps above $5m.

| FY (June) | CIAP investments at 30 June | Investment management fees (= 11f) | ÷ average CIAP | Line 24 "OTH CHARITABL INV ADVISOR PRGM" | (11f + line 24) ÷ average CIAP |
|---|---|---|---|---|---|
| 2022 | $18.11bn | $56.69m | — | — | — |
| 2023 | $22.43bn | $53.69m | **26.5 bps** | n/r (audit "Other expenses" $9.98m) | — |
| 2024 | $27.55bn | $67.31m | **26.9 bps** | $20.67m (= audit "Other expenses") | 35.2 bps |
| 2025 | $37.14bn | $84.32m | **26.1 bps** | $15.62m (= audit "Other expenses" $21.31m less "Federal & state tax payments" $5.70m) | 30.9 bps |

**Reconciliation [F/C]:**
- The Statement of Activities line "Investment management fees" equals 990 line 11f to the dollar in every year. It is all in the program column, and it is **booked as an expense in the audit, not netted**.
- FY2025 Schedule D has no Part XI/XII. FY2024's only Part XII item is line 4b "Other" at $16.59m, the difference between the 990 total ($12.922bn) and the audit total ($12.905bn); it has no line 4a.
- The audit notes do not describe either line. Note 7 says only that FMR is paid "amounts equal to the administrative fee", that Strategic Advisers is the investment adviser, and that pools hold mutual funds.

**Interpretation [I]:**
- **Pools pay no adviser fee.** Strategic Advisers is paid "out of the aggregate NCS administrative services fee" (2025 ADV, repo E-rows). CIAP guidelines say fees "cannot be assessed on Giving Account assets in the Fidelity Charitable investment pools" (repo). So the $84.3m is overwhelmingly CIAP-adviser compensation. It may include some access-pool sub-manager costs; access pools hold $1.64bn, so at most a few $m.
- **What 26 bps means:** it is the observed average adviser fee per CIAP dollar. If fee-paying CIAP accounts pay 1.00%, about 26% of CIAP assets are fee-paying; at 0.75% the share is about 35%. The rest are advisers who bill the household outside the DAF or charge nothing.
- **The line-24 item** is consistent with other CIAP-specific costs, such as custody or alternative-asset servicing. Its nature is not disclosed.
- **Against AEF:** Fidelity CIAP (26–27 bps) sits well below AEF (40–46 bps). AEF's 0.46% does not generalise as a sponsor-wide adviser rate. For an "average CIAP dollar" row, 0.26% (0.31% with line 24) is the observed figure.

---

## 3. P-B31A-03: where MS GIFT's fees sit

| Evidence | Finding | Label |
|---|---|---|
| [Donor Circular, Schedule C](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf) | "Fees and expenses attributed to creating and maintaining Accounts are absorbed by each Account". The MSSB Administrative Fee is "assessed a monthly fee paid to MSSB". The maximum Morgan Stanley Advisory fee is 1.00%, "A portion ... is shared with the applicable Financial Advisor"; fund, ETF and SMA fees are extra | F (OCR) |
| [Select UMA Wrap Fee Program Brochure, 2026-11-04](https://www.morganstanley.com/content/dam/msdotcom/en/wealth-investmentsolutions/pdfs/adv/adv_selectuma.pdf) | The Morgan Stanley Advisory Fee covers "investment advisory services, portfolio implementation services, custody ..., trade execution ... as well as compensation to your Financial Advisor ... This is referred to as a wrap fee. The maximum annual asset-based Morgan Stanley Advisory Fee is 2.0%". A "Platform Fee ... 0.035% annual asset-based fee ... charged quarterly in arrears" is added. The brochure does not name MS GIFT | F |
| [990 TY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml) Part IX | 11f "Morgan Stanley investment advisor" $4,237,948; line 24 "FA commissions and misc." $2,028,620; 11g $15,966,259, mostly RenPSG at $14,930,249. Visible advisory-type lines total **$6.27m = 7.8 bps** against a 1.00% ceiling of **$80.9m** (N078–N079). No line corresponds to the MSSB admin fee (≤ $5.7m, N080) | F / C |
| 990 TY2024 Schedule D Part XI/XII (N081) | Every line is **0**, including Part XII 4a, 4b and 2e. The audit's expense total equals the 990's, so whatever the audit nets inside investment return, the 990 nets too | F |
| Part VIII line 3, investment income ÷ average total assets (N082–N094) | **MS GIFT: 13.7, 35.2 and 4.2 bps (TY2022–24).**<br>Peers: Fidelity 273; Vanguard 306; NPT 269; DAFgiving360 128; GS DAF 316; BofA 260; AEF 259; RCF 353; USCGT 245; RJ 424. MS GIFT is lower by an order of magnitude | F / C |
| Total-return proxy (line 3 + 7d + Part XI line 5) ÷ average assets | MS GIFT 864 bps (TY2024), within the peer range of 404–1,250. A netted layer of 1 pp or less cannot be detected this way | C |
| MS GIFT audit | No 2021–2025 audit or annual report found. Annual-report URLs for 2021–2025 return 404; the only public one found is from 2018 and was not used. Schedule O has no fee text | F (absence) |

**Conclusion [I]:**
- **Where the fees sit:** at MSSB account level, deducted from each account's cash. They appear in neither Part IX nor the audit's expense lines; they reduce reported investment income.
- **What supports this:** the line-3 anomaly is the first filing-level evidence for that. It fits wrap fees debited against dividend and interest income, though the 990 does not say so.
- **How large the layer can be:** for TY2024 it is bounded above by about **$86.5m**, roughly 107 bps (the 1.00% advisory cap plus 0.07% MSSB admin, ignoring tier discounts), plus fund and SMA fees. Visible Part IX cost is 28 bps.
- **How large it actually is:** this needs the account-level fee distribution or MS GIFT's audit note, and neither is public. The broker-captive all-in row should stay a bound.

---

## 4. P-COST-05: Schedule G screen

**Method:**
- `mission_schedule_g_screen.py` streams each of the 5,272 parsed returns, the same object ids as `sponsor-cost-structure.csv`. It reads Part IV lines 17–19 and stops when all three are "No"; otherwise it parses Schedule G and stops.
- **Fields read:** Part I line 2b fundraisers (name, activity, gross receipts, amount retained, control of funds), Part II event names and Part III gaming.
- **Status:** all 5,272 fetched OK, and Schedule G was present for exactly the 1,626 Part IV "Yes" returns.
- **Flags:**
  - S1: line 11e above 25% of operating cost.
  - S2: keyword themes (gaming, sweepstakes, round-up, app, online, platform, named platforms), Part III gaming, fundraiser controls funds, or fundraiser gross at least 10% of DAF contributions.
- **Tiers:**
  - A: line 2b gross ≥ 10% of Part I total contributions, and fundraiser keeps ≥ 25%.
  - B: same gross test, keeps < 25%.
  - C: S1 only.
  - D: keyword, gaming or control flag only.
- **`daf_relevant`:** Schedule D DAF contributions are at least 50% of Part I contributions.

| Tier | Returns | DAF-relevant sponsors (tier A–C) |
|---|---|---|
| A: platform gross receipts, high take | 15 | **Givinga** (2022–23), **Pledgeling** (2023–24), **CAF America** (2022), **Our Change Foundation** (2022–25) |
| B: agent gross receipts, low take | 38 | **Network for Good** (2022–24), **U.S. Charitable Gift Trust** (2022–24), Entertainment Industry Foundation (2023–24; SU2C agents, 17–22% of contributions, 6–11% kept) |
| C: line 11e heavy, no gross-receipt agent | 6 | CAF America (2023), Barrow CF (2022–23; 11e 92–96% of operating cost, "First Community Development"), Givio (2023; 11e 32%, no line 2b detail) |
| D: keyword, gaming or control only | 152 | Event raffles, casino nights, online auctions (e.g. Brooklyn CF, Morton CF, Rio Verde CF "Charity Roundup"). None are platform patterns |

### 4.1 The platform-pattern sponsors (filings [F], ratios [C])

| Sponsor (EIN) | Year | DAF accounts | DAF contributions | Line 2b fundraisers | Gross | Kept | 11e ÷ operating cost | XML |
|---|---|---|---|---|---|---|---|---|
| Givinga (474172718) | 2022 | 1,543,203 | $34.5m | Golden Hearts Games; SoftGiving ("ON-LINE FUNDRAISING") | $25.2m | $18.6m (74%) | 92% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202420369349301017_public.xml) |
| Givinga | 2023 | 955,569 | $17.7m | Brandfluence; Golden Hearts Games | $7.8m | $5.2m (67%) | 80% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml) |
| Pledgeling Foundation (462440594) | 2023 | 20,270 | $59.0m | Charitybuzz; Prizeo ("INTERNET AND EMAIL SOLICITATIONS"; controls funds) | $36.8m | $15.8m (43%) | 99% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202422769349300502_public.xml) |
| Pledgeling | 2024 | 23,006 | $62.6m | Charitybuzz; Prizeo ("ONLINE FUNDRAISING") | $38.9m | $18.8m (48%) | 100% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542539349301674_public.xml) |
| Charities Aid Foundation America (431634280) | 2022 | 673 | $453.8m | Omaze ("FUNDRAISING", controls funds); Ascend ("CHARITABLE SWEEPSTAKES") | $105.6m | $84.1m (80%) | 84% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202320699349300532_public.xml) |
| CAF America | 2023 | 855 | $675.6m | Omaze; Ascend | $30.9m | $25.6m (83%) | 56% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202440679349300014_public.xml) |
| Our Change Foundation (863353394) | 2025 | 26 | $23.4m | Fandiem, Propeller, Zeal TN, Jackpocket Gives ("ONLINE SWEEPSTAKES"); Member For A Day ("GOLF EXPERIENCE") | $14.7m | $6.0m (41%) | 96% | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601809349300805_public.xml) |
| Our Change Foundation | 2022–24 | 32–36 | $1.8–8.9m | Omaze, Jackpocket, Zeal TN | $1.1–1.7m | 77–85% | 84–94% | in CSV |

**Reading [I]:**
1. **Givinga is not alone.** Pledgeling, CAF America (2022–23) and Our Change book sweepstakes or charity-auction receipts as contributions, with the operator's share as line 11e.
   - Where Schedule D DAF contributions are about 100% of total contributions (Pledgeling, Our Change), the DAF contribution totals include these gross receipts.
   - Pledgeling's 20–23k "accounts" look like platform-user or beneficiary records, not donor DAFs, the same issue as Givinga's 0.96–1.54 million.
2. **Scale.** CAF America's Omaze gross was $105.6m in 2022, about 14% of CAF America's contributions. If DAF-coded, it inflates national contributions by about $0.1bn in that year. Pledgeling and Our Change add about $40–55m a year in 2024–25.
3. **Network for Good and USCGT are a different pattern: pass-through distribution with a 1–3% take.**
   - Their gross equals contributions, so the receipts are real donor gifts routed through an affiliated agent.
   - NFG's single "account" is already flagged in the repo.
4. **No sponsor reports Part III gaming income tied to DAFs.** The 49 gaming flags are bingo, raffle and casino-night events at single-issue charities and community foundations.

---

## 5. Suggested repo updates (not applied)

1. **`all-in-cost-comparison-2026.csv`, Fidelity rows.**
   - Add a note: "Asset-weighted pool ER 0.263% (FY2025; audit Note 3 × What it costs). The 0.55% 60/40 pool used as 'typical' is above the asset-weighted average."
   - Add CIAP "average dollar" adviser cost of 0.26% (0.31% incl. line 24).
2. **`adviser-fee-evidence-2026.csv`.** Add Fidelity CIAP rows: 26.1/26.9/26.5 bps for FY2025/24/23, plus the line-24 reconciliation. Revise C04's "not separately itemized" note with the pool-weighted 26.3 bps.
3. **`sponsor-cost-structure.csv` and DAF-total corrections.** Flag Pledgeling, Our Change Foundation and CAF America 2022–23 alongside Givinga as "contributions include sweepstakes or auction gross receipts" (P-B32A-01).
4. **`queue-batch31-fees-costs.md` §3, MS GIFT row.** Add the line-3 investment-income anomaly (4–35 bps against 128–424 bps) as the filing evidence that fees are netted.

---

## 6. Source register

| ID | Source | URL | Date | Label |
|---|---|---|---|---|
| S01 | Fidelity Charitable audited consolidated FS FY2025/2024 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf | FY ended 2025-06-30 | F |
| S02 | Fidelity Charitable audited consolidated FS FY2024/2023 | https://fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2024-2023.pdf | FY ended 2024-06-30 | F |
| S03 | Fidelity Charitable audited consolidated FS FY2023/2022 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2023-2022.pdf | FY ended 2023-06-30 | F |
| S04 | Fidelity Charitable "What it costs" (pool expense ratios) | https://www.fidelitycharitable.org/giving-account/what-it-costs.html | live 2026-11-15; pool data 2026-09-30 | F |
| S05 | Fidelity CIAP overview | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf | live 2026-11-15 | F |
| S06 | Fidelity 990 FY2025 and FY2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml | filed 2026, 2025 | F |
| S07 | Vanguard Charitable investments page | https://www.vanguardcharitable.org/investments | ERs as of 2026-09-30 | F |
| S08 | Vanguard Charitable fees and expenses | https://www.vanguardcharitable.org/fees-and-expenses | live, undated | F |
| S09 | NPT investment descriptions and performance (PDF) | https://www.nptrust.org/investment-descriptions-and-performance-npt/ | NPT FOR IDAP 0926; as of 2026-06-30 | F |
| S10 | DAFgiving360 pool ERs (repo) | research/mission-2026-11-14/queue-adviser-fees-pools-npact.md §2 | 2026-11-15 reads | R/3P |
| S11 | MS GIFT Donor Circular (Schedule C) | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf | Aug 2024 | F (OCR) |
| S12 | MSSB Select UMA Wrap Fee Program Brochure | https://www.morganstanley.com/content/dam/msdotcom/en/wealth-investmentsolutions/pdfs/adv/adv_selectuma.pdf | 2026-11-04 | F |
| S13 | MSSB GIS ADV brochures (checked; no MS GIFT mention) | https://www.morganstanley.com/content/dam/msdotcom/en/wealth-investmentsolutions/pdfs/adv/gis_adv.pdf ; https://morganstanley.com/content/dam/msdotcom/en/wealth/investmentsolutions/pdfs/adv/mssb_gis_adv.pdf | 2026 | F (absence) |
| S14 | MS GIFT 990 XML TY2022–24 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202302999349301010_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403209349313980_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml | filed 2023–25 | F |
| S15 | Peer 990 XML for the line-3 test (10 returns) | listed per row in `infund-expense-nationals-2026.csv` N085–N094 | filed 2025–26 | F |
| S16 | Schedule G screen inputs: 5,272 990 XMLs | object ids and URLs per row in `schedule-g-screen.csv`; universe in `sponsor-cost-structure.csv` | TY2021–25 | F |
| S17 | Repo cost extract | data/mission-2026-11-14/sponsor-cost-structure.csv | TY2022–25 | F (derived) |

---

## 7. Data dictionary

### 7.1 `infund-expense-nationals-2026.csv`

| Column | Meaning |
|---|---|
| row_id | N001–N094 |
| sponsor, ein | Sponsor and EIN. EIN is blank on line-3 test rows; see source_url |
| fiscal_year | FY (June year-end for Fidelity, Vanguard, DAFgiving360 and NPT), tax year, or ER date |
| layer | `pool_in_fund` (one pool, a weighted average, or a range); `pool_in_fund_per_investment_dollar`; `part_ix_operating`; `all_in_per_dollar`; `ciap_adviser_fee`; `ms_gift_fee_location`; `investment_income_test` |
| item | What the row measures |
| assets_usd | Weighting base: pool assets, total investments, average CIAP or average total assets |
| rate_bps | Basis points. A range "a-b" is a bound |
| amount_usd | Dollar amount (in-fund $, fee $, or income $) |
| total_return_proxy_bps | Line-3 test rows only: (Part VIII line 3 + line 7d + Part XI line 5) ÷ average total assets |
| weighting | `pool`, `asset_weighted`, `asset_weighted_bounds`, `lower_bound`, `sensitivity`, `bounds_unweighted`, `observed_ratio`, `ceiling`, `observed`, `sum`, `bounds` |
| basis | Formula or filing lines used |
| source_url | Primary URL(s), separated by " ; " |
| evidence_label | F / R / 3P / C / I as above |
| retrieved | 2026-11-15 |
| notes | Caveats |

### 7.2 `schedule-g-screen.csv` (flagged returns only)

| Column | Meaning |
|---|---|
| ein, sponsor_name, category, fiscal_year, tax_period | Taken from `sponsor-cost-structure.csv` |
| operating_cost, l11e_prof_fundraising, l11e_share_of_opex | Part IX operating cost (lines 1–4 and 11f excluded), line 11e, and their ratio |
| daf_accounts, daf_contributions, daf_assets_eoy | Schedule D Part I |
| part_iv_l17_prof_fundraising / l18_events / l19_gaming | Part IV indicators as filed |
| sched_g_present | 1 if Schedule G was parsed |
| sg_fundraiser_count, sg_fundraisers | Part I line 2b rows: "name [activity] gross= retained= control=", truncated at 900 characters |
| sg_fundraiser_gross_total, sg_fundraiser_retained_total | Sums over line 2b rows |
| total_contributions_part_i | Part I line 8 (from the cost-structure extract cache) |
| daf_contrib_share_of_total_contrib, daf_relevant | DAF contributions ÷ total contributions; 1 if ≥ 0.5 |
| sg_gross_share_of_total_contrib, sg_retained_share_of_gross | Tier ratios |
| sg_events, sg_events_gross_receipts, sg_gaming_gross_income | Part II event names and gross; Part III gaming income where tagged |
| keyword_themes | Matched themes |
| flags | S1 / S2 flags (see §4) |
| tier | A / B / C / D (see §4) |
| xml_status, return_object_id, xml_url, source_url | Provenance |

**Known limits:**
- Keyword matching is coarse. "Spark Prize Breakfast" matches the raffle theme, which is why tier D is not treated as evidence.
- `sg_gaming_gross_income` is sparse because Part III tag names vary by schema year. Part IV line 19 is the reliable gaming flag.
- Returns filed without Part IV indicators but with a Schedule G would be missed. None were seen: Schedule G presence equals Part IV "Yes" exactly.

## Validation corrections (wave 17, 2026-11-15) — governing
Source: [validation-wave17-report.md](validation-wave17-report.md); register `data/mission-2026-11-14/validation-register-wave17.csv`.

1. **§0, P-B31A-02 row.**
   - **Find:** "gives at least **51.5 bps per invested dollar**"
   - **Replace with:** "gives **about 50–52 bps per invested dollar** (37.6 bps is over average total assets and 13.9 bps over year-end investments; on one base the floor is 52.0 bps over average assets or 50.2 bps over year-end investments) [V wave 17]"
2. **§1.3 table, Fidelity row.**
   - **Find:** "| **≥ 51.5 bps** |"
   - **Replace with:** "| **≈ 50–52 bps** (floor; mixed bases summed = 51.5) |"
3. **§0, P-B31A-03 row (reconciliation).**
   - **Find:** "every Schedule D Part XI/XII line is zero, so the audit nets them the same way the 990 does."
   - **Replace with:** "Schedule D Parts XI/XII are zero-filled: every amount present is 0, including line 5 'Total expenses per Form 990'. The audit totals on line 1 are absent, so the filing does not show how the audit treats the fees [V wave 17]."
4. **§0, P-B31A-03 row (line-3 signal).**
   - **Find:** "Eleven peer nationals report **128–424 bps**. That fits fees being taken out of account income before it is reported [I]."
   - **Replace with:** "Ten peer returns report **128–424 bps**. The gap (93–124 bps to the lowest peer, about 235–265 bps to the median) is larger than the whole ~107 bps fee ceiling. Fee netting may contribute, but it cannot explain the anomaly alone; income reported in gains or Part XI line 5 fits at least as well [I; V wave 17]."
5. **§3 table, Schedule D row.**
   - **Find:** "Every line is **0**, including Part XII 4a, 4b and 2e. The audit's expense total equals the 990's, so whatever the audit nets inside investment return, the 990 nets too"
   - **Replace with:** "Every amount present is **0**, including Part XII 4b, 2e and line 5 ('Total expenses per Form 990' = $0, although Part IX line 25 is positive). Line 1 (audit totals) and line 4a are not reported. The parts were zero-filled, so they say nothing about how the audit treats the fees [V wave 17]"
6. **§3 Conclusion, first bullet.**
   - **Find:** "They appear in neither Part IX nor the audit's expense lines; they reduce reported investment income."
   - **Replace with:** "They do not appear in Part IX. No MS GIFT audit is public, so their audit treatment is unobserved. They are probably netted against account values or income [I; V wave 17]."
7. **§3 Conclusion, second bullet.**
   - **Find:** "the line-3 anomaly is the first filing-level evidence for that. It fits wrap fees debited against dividend and interest income, though the 990 does not say so."
   - **Replace with:** "the line-3 anomaly is consistent with wrap fees debited against dividend and interest income, but it is too large for fees alone (see §0). The likelier main cause is classification of income into gains; the 990 does not say [I; V wave 17]."
8. **§0, P-COST-05 row.**
   - **Find:** "line 11e is 56–99% of operating cost"
   - **Replace with:** "line 11e is 56–100% of operating cost"
9. **§0, P-COST-05 row (CAF America).**
   - **Find:** "$105.3m gross in 2022, of which Omaze kept $84.1m, with the agent controlling funds; $30.7m in 2023, then near zero"
   - **Replace with:** "Omaze $105.3m gross in the fiscal year ended April 2022 ($105.6m with Ascend), of which Omaze kept $84.1m, with the agent controlling funds; Omaze $30.7m in FYE April 2023 ($30.9m with Ascend); then $0.55m and $0"
10. **§5 item 4.**
    - **Find:** "Add the line-3 investment-income anomaly (4–35 bps against 128–424 bps) as the filing evidence that fees are netted."
    - **Replace with:** "Add the line-3 investment-income anomaly (4–35 bps against 128–424 bps) as an unexplained anomaly consistent with, but larger than, fee netting [V wave 17]."
