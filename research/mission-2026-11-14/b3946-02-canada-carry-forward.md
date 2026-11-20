# Canada: do carry-forwards cover the 22 DAF sponsors in disbursement-quota shortfall? (P-B3946-02)

**Prepared 2026-11-20 (task b3946-02). Desk research only: no outreach, no logins, no forms.** This is research, not legal or tax advice. It follows up [`b39n3-0406-canada-netting-dq.md`](b39n3-0406-canada-netting-dq.md) §3.3, which found 22 DAF sponsors (line 5860 = Y) in disbursement-quota (DQ) shortfall in the 2025 CRA release, 10 of them covered by an excess on their 2024-release return. It reads that doc's CSV ([`canada-daf-netting-dq-2026-11-19.csv`](../../data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv)) and imports its scripts without changing them.

**Labels.** **[F]** the source states it; **[C]** computed by `scripts/mission_canada_carry_forward.py`; **[I]** inference.

**Outputs.**
- [`data/mission-2026-11-14/canada-carry-forward-2026-11-20.csv`](../../data/mission-2026-11-14/canada-carry-forward-2026-11-20.csv): 129 rows. There is one row per sponsor × fiscal period in the chain (22 sponsors, FPE 2020 to 2025), and every row repeats that sponsor's coverage verdict.
- [`scripts/mission_canada_carry_forward.py`](../../scripts/mission_canada_carry_forward.py): stdlib, functional. It prints a JSON summary, and every number below comes from it.
- [`data/mission-2026-11-14/queue-proposals-b3946-02.csv`](../../data/mission-2026-11-14/queue-proposals-b3946-02.csv): 6 follow-ups.

To reproduce, place the files in §1.2 in folders named `{year}_{dq|fin|abc}_<original name>` and run:
`python3 scripts/mission_canada_carry_forward.py . --dq-dirs DQDIR --fin-dirs FINDIR --abc-dirs ABCDIR --summary out.json`

---

## Headline findings

1. **The filed data cover 13 of the 22 shortfalls (C$0.66m of C$2.49m) [C].** On top of the parent doc's 10 sponsors covered by a 2024-release excess, three more are covered:
   - Brampton and Caledon CF, by its 2023 excess (C$1.04m). This remains C$0.90m after its 2024 shortfall, against a 2025 shortfall of C$68k.
   - St. Kevin's Parish and Pemberton & District Health Care Foundation. Each filed line 5850 = N in 2024 (property below the C$100k / C$25k threshold), so its DQ was nil that year. Read literally, s.149.1(21) then makes all of that year's spending a disbursement excess [C/I].
   - Using Schedule 8 alone, without that reading, the count is 11 of 22 (C$0.62m).
2. **Nine sponsors stay uncovered on the filed data: C$1.83m of shortfall, C$1.81m net of partial pools [C].** They are Brandon University Foundation (C$911k), Fondation du Collège de l'Assomption (C$370k), Bierer Foundation (C$235k), Lithuanian Canadian Foundation (C$130k), Fredericton CF (C$76k), Fondation Pointe-à-Callière (C$64k), Caritas-Sherbrooke (C$27k), Rogan Foundation (C$14k) and Catholic Foundation of Manitoba (C$6k).
3. **Excesses from before 2023 could rescue three more, but only as a proxy [C/I].** Schedule 8 begins with fiscal periods starting on or after 2023-01-01 [F]; the 2019–2022 Schedule 8 files on open.canada.ca are header-only [C]. For FPEs 2020–2023, the pre-2023 DQ (3.5% of line 5900 above the threshold) was rebuilt from Schedule 6 as a proxy. With it, three more are covered: Fredericton CF, Fondation du Collège de l'Assomption and Bierer Foundation, all under the old 3.5% rate.
   - That gives **16 of 22 covered (C$1.34m)**.
   - **4 are uncovered:** Brandon, Lithuanian, Pointe-à-Callière and Rogan (C$1.12m).
   - **2 are partly covered:** Catholic Foundation of Manitoba (C$3.0k left) and Caritas-Sherbrooke (C$12.4k left).
   - Uncovered dollars total **C$1.13m**.
4. **Brandon University Foundation decides the dollar answer [C].** It holds 37% of the total shortfall and is in shortfall in 2023, 2024 and 2025 (C$0.26m, C$0.90m, C$0.91m). Its pre-2023 proxy pool comes almost entirely from its 2020–2021 returns. Those returns report line 5900 of only C$2.4–2.5m, against C$73–74m in 2022–2023 and total assets of C$73–81m.
   - The script screens out these two implausible years. If they were kept, Brandon would be covered, and uncovered dollars would fall to C$0.22m (17 of 22 covered).
5. **Among the 7 repeat shortfalls (both releases) [C]:**
   - Brampton and Caledon CF is covered by filed data.
   - Fredericton CF and Collège de l'Assomption are covered only by the pre-2023 proxy.
   - Caritas-Sherbrooke is partly covered.
   - Brandon, Lithuanian Canadian Foundation and Rogan Foundation are not covered.
6. **There is no effect on the repo's Canada netted payout of 12.0% [C].** A carry-forward is a charity-level compliance offset. It changes neither line 5864 (DAF disbursements) nor prior-year DAF assets, so the 2025 tier-B netted payout stays **12.05%** (586 matched sponsors, C$15.39bn).
   - 17 of the 22 are in that base. They hold C$279m of prior DAF assets (1.8%) and pay out 3.7% net.
   - Dropping all 22 would raise the aggregate to 12.20%. Dropping the 6 uncovered or partly covered would raise it to 12.10%.
   - Even if every uncovered dollar (C$1.13m) had been paid as extra DAF grants, the aggregate would be 12.053%.
7. **There is no 2026 release yet.** A CKAN search on open.canada.ca returns "List of charities" datasets for 1990–2025 only (36 datasets, checked 2026-11-20) [C]. Carry-backs from FY2026 (s.149.1(20) allows one year back) therefore cannot be tested.

---

## 1. Method

### 1.1 Robots.txt and fetch log (UA `research-script/1.0`; checked 2026-11-20 before any fetch)

| Host | robots.txt | Use |
|---|---|---|
| open.canada.ca | 200; `Crawl-delay: 20`; `/data/` (including `/data/api/`) not disallowed | 2 CKAN API calls, 8 CSV downloads, ≥ 20 s apart (03:16–03:20 UTC) |
| laws-lois.justice.gc.ca | 404 (no robots = allowed) | ITA point-in-time index; ITA full text as of 2022-11-17 (one 10.8 MB page); one 404 probe for a section-level page |
| www.canada.ca | not contacted (unreachable in the parent pass) | — |

Fetch log: `fetchlog.tsv` in the session scratchpad (`b394602/`); URLs are in the source register.

### 1.2 Data

| File | Release | Rows | Origin |
|---|---|---|---|
| `schedule_8_dq_2023_updated.csv` | 2023 | 7,604 (FPE 2023-07-31 to 2023-12-31, all Form 27) | new download |
| `schedule_8_dq_2024_updated.csv`, `…_2025_updated.csv` | 2024, 2025 | 14,631; 14,852 | parent-pass cache (2026-11-19) |
| `schedule_8_dq_2019.csv`, `…_2020/2021/2022_updated.csv` | 2019–2022 | 0 (header only) | new download |
| `financial_d_and_schedule_6_{2020,2021,2022}_updated.csv` | 2020–2022 | 84,566; 84,636; 84,676 | new download |
| `financial_d_and_schedule_6_{2023,2024}_updated.csv`, `financial_section_a_b_and_c_{2023,2024}_updated.csv` | 2023–2024 | 84,410; 83,872 (fin) | panel cache (2026-11-19) |
| `canada-daf-netting-dq-2026-11-19.csv` | 2025 rows with route = SHORTFALL | 22 | repo |

**Release ≈ FPE calendar year.** Each Schedule 8 release holds FPEs from one calendar year only. The 2025 release, for example, runs from 2025-01-01 to 2025-12-31 [C]. A sponsor with a December year-end therefore has two filed Schedule 8 years before 2025 (2023 and 2024). A sponsor with any other year-end has one, because its FY2022-23 began before 2023-01-01 and is not covered by Schedule 8.

### 1.3 Law (primary text)

- **s.149.1(20)** (current to 2026-10-29; the same wording as of 2022-11-17) [F]: a charity that "has expended a disbursement excess for a taxation year" may count it towards "the immediately preceding taxation year of the charity and five or less of its immediately subsequent taxation years", up to "such portion of that disbursement excess as was not so included under this subsection for any preceding taxation year".
- **s.149.1(21)** [F]: the disbursement excess is the amount by which spending "on charitable activities carried on by it and by way of gifts made by it that are qualifying disbursements exceeds its disbursement quota for the year".
- **DQ before 2023** (ITA s.149.1(1) as of 2022-11-17) [F]: "A × B × 0.035/365", where B is the prescribed amount of property not used directly in charitable activities or administration if it is greater than C$100,000 (charitable organization) or C$25,000 (other charities), and nil otherwise.
- **DQ from 2023** (current text) [F]: 3.5% up to C$1m, then C$35,000 plus 5% above C$1m. CRA dictionary §1.4.5 says this applies to "fiscal periods beginning on or after January 1, 2023".
- **Line 5850** (CRA dictionary v2.0) [F] asks whether average property not used in charitable activities or administration over the prior 24 months exceeded C$100,000 (charitable organization) or C$25,000 (public or private foundation).

### 1.4 Chain construction

For each of the 22 BNs, one record per fiscal period (FPE). Where the same BN and FPE appear in more than one release, the later release wins.

| Regime | When | Excess (+) / shortfall (−) |
|---|---|---|
| `NEW` | Schedule 8 row exists (2023–2025 releases) | filed line 865; if blank, 860 (else 845 + 850 + 855) − 840 (else the formula) |
| `NIL_DQ_5850N` | v27 return, no Schedule 8 row, line 5850 = N | DQ nil, so excess = Schedule 6 lines 5000 + 5045 + 5050 |
| `OLD_PROXY` | pre-v27 return (Form ID < 27), FPE 2020–2023 releases | 5000 + 5050 − 3.5% × 5900 (nil DQ at or below the threshold for the sponsor's designation); unknown if 5900 or both spending lines are blank |

**The 2025 (target) year** uses the shortfall in the parent CSV (`dq_excess_used`, i.e. spending − DQ).

### 1.5 Coverage tests (columns in the CSV)

1. `covered_prior_release_865`: the parent doc's test, where line 865 on the previous release's latest return is at least the shortfall. It reproduces **10 of 22** [C].
2. `covered_filed_gross`: the sum of positive `NEW` and `NIL_DQ_5850N` excesses in the five preceding taxation years is at least the shortfall.
3. `covered_filed_net`: a FIFO pool over the `NEW` and `NIL_DQ_5850N` years. It applies these rules:
   - Each excess enters the pool and expires after five subsequent years (31-day tolerance for changed year-ends).
   - Each intermediate shortfall first takes the next year's excess (carry-back) and then the oldest pool excess, so no excess is used twice.
   - The pool left at the 2025 year must be at least the shortfall.
4. `covered_proxy_net`: as 3, also using the `OLD_PROXY` years.
5. `covered_proxy_screened` (the headline): as 4, but an `OLD_PROXY` year counts as unknown if its line 5900 is below 25% of the sponsor's first Schedule 8 line 805. Only Brandon University Foundation's 2020 and 2021 returns are screened out (C$2.4m and C$2.5m against C$73.3m) [C].

**Verdict** (`verdict` column):
- `COVERED_FILED`: test 3 passes.
- `COVERED_ONLY_WITH_PRE2023_PROXY`: test 5 passes but test 3 fails.
- `PARTLY_COVERED`: the test-5 pool is positive but smaller than the shortfall.
- `UNCOVERED`: the test-5 pool is zero.

### 1.6 Payout effect

From the parent CSV, 2025 rows with prior-year DAF assets: tier-B net payout = Σ `net_5864_tier_b` ÷ Σ `prior_daf_assets_5862`. It is recomputed with and without the shortfall sponsors, and with uncovered shortfall dollars added to the numerator as an upper bound.

---

## 2. Results

### 2.1 Summary [C]

| Test | Covered (n of 22) | Shortfall covered | Uncovered dollars |
|---|---|---|---|
| Previous-release line 865 (parent doc) | 10 | C$556,228 | — |
| Filed Schedule 8 only (2023–2024 excesses, FIFO) | 11 | C$624,572 | — |
| Filed, gross (Schedule 8 + 5850 = N years) | 13 | C$662,419 | — |
| **Filed, net FIFO (Schedule 8 + 5850 = N years)** | **13** | **C$662,419** | **C$1,810,425** |
| + pre-2023 proxy, unscreened | 17 | C$2,253,114 | C$223,589 |
| **+ pre-2023 proxy, screened (headline)** | **16** | **C$1,342,412** | **C$1,134,291** |

Total 2025 shortfall of the 22 sponsors: **C$2,494,652** [C].

**Lookback depth** [C]:
- 13 sponsors have two filed prior years plus three proxy years.
- 8 have one filed prior year plus four proxy years.
- 1 (St. Kevin's Parish) has two 5850 = N years.

### 2.2 Per sponsor [C]

Shortfall = 2025 DQ − spending. "Prior 865" is the previous release's line 865. "Filed pool" and "Proxy pool" are the excess still available at the 2025 year under tests 3 and 5. All amounts are in C$.

| # | Sponsor | Des. | FPE | Shortfall | Prior 865 | Filed pool | Proxy pool (screened) | Uncovered | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Hamilton Community Foundation | A | 2025-03-31 | 279,041 | 973,348 | 973,348 | 24,015,955 | 0 | COVERED_FILED |
| 2 | Brandon University Foundation | A | 2025-12-31 | 910,702 | −898,637 | 0 | 0 | 910,702 | UNCOVERED |
| 3 | Brant Community Foundation | A | 2025-05-31 | 702 | 312,218 | 312,218 | 395,936 | 0 | COVERED_FILED |
| 4 | Fredericton Community Foundation | A | 2025-06-30 | 75,705 | −111,507 | 0 | 2,408,562 | 0 | COVERED_ONLY_WITH_PRE2023_PROXY |
| 5 | The Bierer Foundation | B | 2025-12-31 | 234,660 | 10,590 | 18,917 | 425,462 | 0 | COVERED_ONLY_WITH_PRE2023_PROXY |
| 6 | Fondation du Musée Pointe-à-Callière | A | 2025-12-31 | 63,794 | 58,008 | 0 | 0 | 63,794 | UNCOVERED |
| 7 | Lithuanian Canadian Foundation | A | 2025-12-31 | 130,356 | −140,574 | 0 | 0 | 130,356 | UNCOVERED |
| 8 | Fondation du Collège de l'Assomption | A | 2025-06-30 | 369,628 | −451,384 | 0 | 482,708 | 0 | COVERED_ONLY_WITH_PRE2023_PROXY |
| 9 | Brampton and Caledon Community Foundation | A | 2025-12-31 | 68,344 | −144,218 | 897,505 | 1,061,567 | 0 | COVERED_FILED |
| 10 | Cowichan District Hospital Foundation | A | 2025-09-30 | 50,527 | 251,587 | 251,587 | 623,590 | 0 | COVERED_FILED |
| 11 | Creston Valley Community Foundation | A | 2025-12-31 | 72,282 | 163,928 | 354,280 | 328,402 | 0 | COVERED_FILED |
| 12 | St. Kevin's Parish Inc. | C | 2025-12-31 | 36,518 | — | 182,129 | 182,129 | 0 | COVERED_FILED (5850 = N years) |
| 13 | The Rogan Foundation | B | 2025-12-31 | 13,983 | −52,265 | 0 | 0 | 13,983 | UNCOVERED |
| 14 | The Catholic Foundation of Manitoba | A | 2025-09-30 | 5,920 | 2,891 | 2,891 | 2,891 | 3,029 | PARTLY_COVERED |
| 15 | Fondation Donat Grenier | B | 2025-12-31 | 15,757 | 123,559 | 152,016 | 1,023,624 | 0 | COVERED_FILED |
| 16 | Legacy Private Trust Foundation | B | 2025-12-31 | 87,210 | 174,380 | 201,015 | 1,110,143 | 0 | COVERED_FILED |
| 17 | La Fondation Caritas-Sherbrooke | A | 2025-12-31 | 27,485 | −73,655 | 0 | 15,058 | 12,427 | PARTLY_COVERED |
| 18 | Barrie Community Foundation | A | 2025-03-31 | 15,154 | 334,151 | 334,151 | 1,003,489 | 0 | COVERED_FILED |
| 19 | Deep River and District Community Foundation | A | 2025-12-31 | 5,841 | 30,598 | 79,260 | 169,336 | 0 | COVERED_FILED |
| 20 | Fondation Annette Cimon Lebel | C | 2025-12-31 | 1,938 | 4,710 | 6,391 | 12,525 | 0 | COVERED_FILED |
| 21 | Northside/Harbourview Hospital Foundation | A | 2025-12-31 | 27,776 | 75,996 | 176,289 | 756,296 | 0 | COVERED_FILED |
| 22 | Pemberton & District Health Care Foundation | A | 2025-03-31 | 1,329 | — | 3,875 | 3,875 | 0 | COVERED_FILED (5850 = N year) |

**Reading** [C/I]:
- **Pointe-à-Callière.** Its 2024 excess (C$58k) is smaller than its 2025 shortfall (C$64k). The FIFO test also uses that excess first to cover the 2023 shortfall (C$80k) by carry-back, so nothing is left. Its pre-2023 proxy years are shortfalls too.
- **Creston Valley.** Adding proxy years slightly lowers its pool (C$354k → C$328k), because a proxy-year shortfall absorbs part of the 2023 excess by carry-back.
- **Brandon, Lithuanian and Rogan** run shortfalls in every filed year (2023–2025) with no usable excess.
- **Old-rate proxy rescues.** Fredericton, Assomption and Bierer are rescued only by excesses earned under the old 3.5% flat rate. Under the 2023 rule (5% above C$1m), the same spending falls short.

### 2.3 Effect on the Canada netted payout (12.0%) [C]

| Measure (2025 release, tier B) | Value |
|---|---|
| Netted payout, all matched sponsors (n = 586, base C$15.39bn) | **12.05%**, unchanged by any carry-forward |
| Shortfall sponsors in the matched base | 17 of 22; prior DAF assets C$279.2m; net 5864 C$10.3m; payout 3.69% |
| Netted payout excluding all 22 | 12.20% |
| Netted payout excluding the 6 uncovered or partly covered | 12.10% |
| Netted payout if uncovered shortfalls (C$1.13m in base) were paid as extra DAF grants | 12.053% |

**Interpretation** [I]:
- The carry-forward answers a compliance question, not a payout question. DQ shortfalls are a charity-level gap of C$2.5m, against C$1.85bn of tier-B net DAF disbursements in the matched base.
- The 12.0% figure needs no revision. Its known sensitivities remain the netting tier and coverage (parent doc §2.2), not DQ compliance.

---

## 3. Limits

- **Schedule 8 starts in 2023.** The 2019–2022 Schedule 8 files are header-only, so pre-2023 excesses are a proxy:
  - The proxy ignores designated gifts (s.149.1(1.1)(a)), short-year pro-rating, permissions to accumulate (lines 5500/5510) and Minister-approved reductions (line 5750).
  - It uses line 5000, which may include amounts the CRA would not treat as charitable activities.
  - Whether an excess earned under the old 3.5% DQ carries into post-2023 years unchanged is a reading of s.149.1(20)–(21) as worded in both versions, not confirmed CRA guidance [I].
- **Nil-DQ years (line 5850 = N).** Treating all spending in a nil-DQ year as an excess is the literal text of s.149.1(21). CRA guidance (www.canada.ca, unreachable) was not checked. Without this reading, St. Kevin's Parish (C$36.5k) and Pemberton (C$1.3k) are uncovered, and the filed count is 11 of 22 [I].
- **Missing years.**
  - Line 5900 is blank on 10 pre-v27 returns: Pemberton 2020–2023, Cowichan 2021–2023, Catholic Foundation of Manitoba 2022–2023 and Barrie 2020. Bierer 2021 and Caritas 2020 lack spending lines. These count as unknown, not zero.
  - The Catholic Foundation of Manitoba could be covered if its unknown 2022–2023 years had an excess.
- **Filing anomalies** [C]:
  - Caritas-Sherbrooke's 2025 line 865 is +C$27,485, although spending (C$82,500) is below the DQ (C$109,985). The script uses spending − DQ.
  - Northside/Harbourview's 2024 line 840 is blank and its line 865 equals its spending (C$75,996). Using a recomputed DQ would give C$53,070. Either value covers its shortfall.
- **The screening rule is a judgement.** A 25% threshold of line 805 removes only Brandon 2020–2021. The unscreened result is reported alongside.
- **No carry-back.** FY2026 returns (a 2026 release) are not published, so a FY2026 excess applied back to FY2025 cannot be tested.
- **Legal status.** Whether a sponsor actually designated an excess, or whether the CRA has accepted it, is not in the data. The verdict is arithmetic on public returns.
- **Scope.** Only the 22 sponsors in 2025 shortfall were chained. Non-DAF charities and the 489 sponsors without a Schedule 8 row are out of scope.
- **Recency.** All sources are 2021 or later, except ITA point-in-time text (2022-11-17), which states the pre-2023 rule.

---

## 4. Data dictionary: `canada-carry-forward-2026-11-20.csv`

One row per sponsor (22) × fiscal period in its chain (FPE 2020–2025), 129 rows. Amounts are in C$; booleans are yes/no; blank means not available. Sponsor-level columns repeat on every row of that sponsor.

| Column | Meaning |
|---|---|
| bn, legal_name, designation | BN; legal name; A public foundation, B private foundation, C charitable organization (parent CSV, 2025) |
| target_fpe, target_dq, target_spending, target_shortfall | 2025-release FPE; DQ (840 or recomputed); spending used; DQ − spending (positive) |
| fpe, release | Fiscal period end of this chain row; release it came from |
| regime | NEW (Schedule 8), NIL_DQ_5850N (v27, no Schedule 8, line 5850 = N), OLD_PROXY (pre-v27 Schedule 6) |
| form_id | T3010 form version (Form ID) |
| in_lookback_window | yes if among the five taxation years immediately preceding target_fpe (blank on the target row) |
| years_before_target | (target_fpe − fpe) in years |
| dq_840_or_proxy | NEW: line 840 (or the formula); NIL_DQ_5850N: 0; OLD_PROXY: 3.5% × 5900 above the threshold |
| spending_or_proxy | NEW: 860 (or 845 + 850 + 855); NIL_DQ_5850N: 5000 + 5045 + 5050; OLD_PROXY: 5000 + 5050 |
| line_865_filed | Schedule 8 line 865 as filed |
| excess_or_shortfall | Excess (+) or shortfall (−) used in the chain |
| excess_source | 865 / 860-840 / 5850=N: 5000+5045+5050 / proxy_5000+5050-3.5%x5900 / target_year |
| line_5900 | Schedule 6 line 5900 (OLD_PROXY and NIL rows) |
| proxy_base_check | OLD_PROXY: ok / no_5900 / suspect_low_5900 (5900 < 25% of first Schedule 8 line 805) |
| pool_after_year_filed_net, _proxy_net, _proxy_screened | Excess pool remaining after this year under tests 3, 4 and 5 |
| prior_release_865, covered_prior_release_865 | Previous release's line 865; test 1 |
| lookback_excess_filed_gross, covered_filed_gross | Sum of positive filed excesses in the window; test 2 |
| pool_at_target_filed_net, covered_filed_net | Pool available at the 2025 year; test 3 |
| pool_at_target_proxy_net, covered_proxy_net | Test 4 |
| pool_at_target_proxy_screened, covered_proxy_screened | Test 5 (headline) |
| uncovered_filed_net, uncovered_proxy_net, uncovered_proxy_screened | max(shortfall − pool, 0) under tests 3, 4 and 5 |
| n_new_regime_prior_years, n_old_proxy_prior_years | Filed (NEW or NIL) and proxy years among the five preceding years |
| verdict | COVERED_FILED / COVERED_ONLY_WITH_PRE2023_PROXY / PARTLY_COVERED / UNCOVERED (§1.5) |

## 5. Source register

| ID | Source | URL | Grade | Read |
|---|---|---|---|---|
| S01 | CRA, 2023 List of charities: Schedule 8 DQ (open data) | https://open.canada.ca/data/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6/resource/d98c8529-78a7-409b-b15f-296af52a43f1/download/schedule_8_dq_2023_updated.csv | P | 2026-11-20 |
| S02 | CRA, 2024 and 2025 List of charities: Schedule 8 DQ | https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 (resource d3c4db23-284f-49d7-9c86-6d8532f417bd); https://open.canada.ca/data/en/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 (resource 1e079ab4-59b2-4cd0-8af6-3531b36f0fbd) | P | 2026-11-19 (parent-pass download) |
| S03 | CRA, 2019–2022 Schedule 8 files (header-only) | https://open.canada.ca/data/dataset/21118663-1847-48ce-81ce-1ac7cff674c0/resource/8e4b08ec-cf46-40cd-b6fe-7875075e2716/download/schedule_8_dq_2019.csv ; …/5577f7aa-7a96-4c59-bc01-47ad54203930/resource/279ea0e0-56a0-4c38-b9a2-46ccc5410f10/… ; …/3e8a4d9f-9a12-4498-9a0b-a5c81d3281b4/resource/6a8fbe44-9d6f-4107-b453-7f342e7ac942/… ; …/b2acb3be-c720-4329-a8c0-d4d36c8db61e/resource/cea1f612-e919-4c3c-a401-21ca1a4ef415/… | P | 2026-11-20 |
| S04 | CRA, 2020–2022 Financial data (Section D / Schedule 6) | https://open.canada.ca/data/dataset/5577f7aa-7a96-4c59-bc01-47ad54203930/resource/9dfd020a-e5e5-49c7-a4ed-c9c8b54c8188/download/financial_d_and_schedule_6_2020_updated.csv ; https://open.canada.ca/data/dataset/3e8a4d9f-9a12-4498-9a0b-a5c81d3281b4/resource/93544c86-0458-448a-adac-fff195c4f42c/download/financial_d_and_schedule_6_2021_updated.csv ; https://open.canada.ca/data/dataset/b2acb3be-c720-4329-a8c0-d4d36c8db61e/resource/2436c7a6-7ad4-45d2-abea-62de613e6ef0/download/financial_d_and_schedule_6_2022_updated.csv | P | 2026-11-20 |
| S05 | CRA, 2023–2024 Financial data and Sections A–C (line 5850) | https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6 ; https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 | P | 2026-11-19 (panel cache) |
| S06 | CKAN package search, "List of charities" (no 2026 release) | https://open.canada.ca/data/api/3/action/package_search?q=%22List%20of%20charities%22&rows=50 | P | 2026-11-20 |
| S07 | CRA, List of charities data dictionary v2.0 (§1.4.5, §3.19, lines 5000/5050/5850/5900) | https://open.canada.ca/data/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6/resource/19375510-2919-480c-8f8c-e8721d285b72/download/open-data-data-dictionary-v2.0_eng.pdf | P | 2026-11-19 (cached copy) |
| S08 | Income Tax Act s.149.1(1), (1.1), (20), (21), current to 2026-10-29 | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/section-149.1.html | P | 2026-11-19 (parent cache) |
| S09 | Income Tax Act, point-in-time version 2022-11-17 to 2022-12-14 (pre-2023 DQ; (1.1), (20), (21)) | https://laws-lois.justice.gc.ca/eng/acts/I-3.3/20221117/P1TT3xt3.html | P | 2026-11-20 |
| S10 | Repo: parent netting and DQ analysis | [b39n3-0406-canada-netting-dq.md](b39n3-0406-canada-netting-dq.md); [canada-daf-netting-dq-2026-11-19.csv](../../data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv) | R | 2026-11-20 |
