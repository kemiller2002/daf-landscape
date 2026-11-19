# Canada follow-ups: public-foundation donees, missing Schedule 8 rows, and CanadaHelps (P-B3946-01, -03, -04)

**Prepared 2026-11-19 (task b3946-010304). Desk research only: no outreach, no logins, no forms.** This is research, not legal or tax advice. It builds on [`b39n3-0406-canada-netting-dq.md`](b39n3-0406-canada-netting-dq.md) and its wave-38A corrections ([`validation-wave38a-report.md`](validation-wave38a-report.md)), the CSV [`canada-daf-netting-dq-2026-11-19.csv`](../../data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv) and [`scripts/mission_canada_netting_dq.py`](../../scripts/mission_canada_netting_dq.py).

**Labels.** **[F]** the source states it; **[C]** computed by `scripts/mission_canada_followups.py`; **[I]** inference.

**Outputs.**
- [`data/mission-2026-11-14/canada-followups-2026-11-19.csv`](../../data/mission-2026-11-14/canada-followups-2026-11-19.csv): 4,820 rows in four sections (§6).
- [`scripts/mission_canada_followups.py`](../../scripts/mission_canada_followups.py): stdlib, functional. It imports `mission_canada_daf_panel` and `mission_canada_netting_dq` without changing them and never calls their `main()`, so their CSVs are not rewritten. With `--check-parent` it rebuilds the parent's 1,710 sponsor rows in memory and confirms they are identical to the parent CSV (result: identical) [C].
- [`data/mission-2026-11-14/queue-proposals-b3946-010304.csv`](../../data/mission-2026-11-14/queue-proposals-b3946-010304.csv): 5 follow-ups.

Reproduce (same inputs as the parent; DIR = panel files, DIR2 = qualified-donee and Schedule 8 files):
`python3 scripts/mission_canada_followups.py . --data-dir DIR --extra-dir DIR2 --summary out.json --check-parent data/mission-2026-11-14/canada-daf-netting-dq-2026-11-19.csv`

---

## Headline findings

1. **Tier C's public-foundation money is mostly hospital and federation grants, not pass-through.** In the 2025 release, DAF sponsors gave C$445.5m to 2,075 public foundations that never answered 5860 = Y [C]:
   - hospital and health foundations: C$190.2m (42.7%);
   - federations and United Ways: C$76.3m (17.1%);
   - other education: C$49.7m (11.2%; CanEd Foundation alone C$36.0m);
   - university and college foundations: C$34.8m (7.8%);
   - giving platforms: C$10.5m (2.3%; almost all CanadaHelps);
   - community foundations: C$4.5m (1.0%); religious: C$4.2m (0.9%); other: C$75.4m (16.9%).
   The 2024 release is similar: hospital/health 41.8%, federations 23.9%, university 10.2%, platforms 0.1% [C].
2. **CRA category codes alone cannot type these donees.** 74.4% of 2025 public-foundation dollars go to category 0210 "Foundations" (sub-category 0001 "for specified community benefit" C$172.9m; 0002 "funding community benefit QDs in general" C$158.4m) [C; F codes_en.pdf]. Names and the donee's own T1236 gifts do most of the typing (§1.3).
3. **The rebuilt middle tier changes almost nothing.** Tier BP (tier B plus giving platforms) gives a 2025 aggregate payout on prior-year DAF assets of 12.04%, against 12.05% for tier B and 8.82% for tier C. The median is 4.84% (B 4.89%, C 4.18%) [C]. Adding community foundations gives 12.02%; adding federations as well gives 11.54% [C].
   - Of the 3.23-point gap between tier B and tier C in 2025, federations explain about 0.5 point, hospital, education and other public foundations about 2.1 points, and private foundations about 0.6 point [C, differences of §2.2 rows].
   - So tier C stays an upper bound driven by program grants, as the parent study inferred [I].
4. **Large returns without Schedule 8 almost all answered line 5850 = N.** In the 2025 release, 226 of 6,593 v27 returns with line 5900 above C$1m (3.4%) have no Schedule 8 row under any FPE. In 2024 it is 254 of 6,270 (4.1%) [C]:
   - by the line 5850 answer (2025): N 196 of 197 have no row; blank 14 of 14; Y 16 of 6,382;
   - by the line 5850 answer (2024): N 235 of 236; blank 17 of 17; Y 2 of 6,017 [C].
   Every return in both releases is form version 27, and the published Schedule 8 file has no filing-date column [C].
5. **JCF Montreal answered 5850 = N in both releases.** It did so while reporting line 5900 of C$1,850.5m (2024) and C$2,143.0m (2025) [C]. Applied to line 5900, the Schedule 8 formula gives a DQ of C$92.5m and C$107.1m. Its DAF disbursements (C$213.9m and C$236.9m) cover these even net of tier-B transfers [C].
6. **Neither paper filing nor processing lag fits the data** [C/I]:
   - The older 2024 release has the higher missing share.
   - Within each release, the latest fiscal quarter has the lowest missing share: in 2024, Q4 3.0% against Q1 5.8%; in 2025, 2.9% against 4.3%.
   - 133 of the 226 returns without Schedule 8 (2025) have T1236 rows, so the rest of the return was processed.
   - The dictionary's paper route covers old form versions (v23–v26), and none of these returns uses one.
   - What does fit: Schedule 8 follows the 5850 answer. That answer is often wrong. 173 sponsors without Schedule 8 (C$2.79bn of DAF assets) answered N although their year-end DAF assets alone exceed the threshold [C/I].
7. **CanadaHelps' products do not fit the C18 DAF definition** [F/I]:
   - Gifts are designated to a charity at the time of giving and sent weekly.
   - Cause Funds are curated pools that pay out evenly every quarter.
   - "Funds" are purpose designations set up by recipient charities.
   - No giving-fund, donor-account or pooled-portfolio product appears on the pages checked.
   - Charity gift cards are the only held balances with later direction. They sit inside C$11.0m of "designated cash" at 2025-06-30, against C$467.1m paid to charities in the year [F].
8. **Counting CanadaHelps as a DAF sponsor would distort the panel.** Use its designated cash as DAF assets and line 5050 as disbursements (2025) [C]:
   - It becomes the largest disburser, with 18.3% of panel disbursements, while ranking 76th by assets.
   - Panel same-year payout moves from 11.21% to 13.72%.
   - Payout on prior-year assets moves from 13.30% to 16.32% (12.05% to 14.94% net of tier B).
   Treating it as a tier-B donee instead moves 2025 netting by 0.01 point. 97% of what sponsors gave CanadaHelps (C$10.16m of C$10.45m) came from a hospital foundation whose line 5864 is blank, so that money is not counted as DAF disbursement [C].

---

## 1. Method

### 1.1 Robots.txt and fetch log (UA `research-script/1.0`; checked 2026-11-19 before any fetch)

| Host | robots.txt result | Use |
|---|---|---|
| open.canada.ca | 200; `Crawl-delay: 20`; `/data/` not disallowed | 2 downloads (codes_en.pdf, 2025 and 2024 releases), 23 s apart |
| www.canadahelps.org | 200; disallows `/wp-admin/`, `*/search/app/`, p2p donation/create paths, `*/givingbasket*`, one charity page | 16 pages/files, about 5 s apart, none disallowed |
| help.canadahelps.org | 200; `Allow: /` | 3 sitemaps and 1 article (the article is a JavaScript shell with no text, so not used) |
| canadahelps.org | 301 to www | none |
| www.canada.ca | HTTP/2 stream reset (INTERNAL_ERROR), as in the parent passes | **not fetched**; C18 quoted via Blumberg & Pasha |

- `/en/giftcards/orders/` returned 500 and `/en/giftcards/` returned 404, so the gift-card terms page was not read. Gift-card rules come from the audited statements and the refund policy.
- All other inputs are the parent passes' CRA downloads of 2026-11-19, reused unchanged.
- The two codes_en.pdf files are byte-identical (md5 `88037e01…`).

### 1.2 Data

- **Rebuilt parent rows.** The parent's sponsor rows and tier-C transfer edges (year, donor, donee, class, amount) are rebuilt by calling `mission_canada_netting_dq.build()` with the parent's inputs. The rebuilt rows are byte-identical to the parent CSV (1,710 rows) [C].
- **Donee attributes**, from the Identification files (2023–2025, later releases override):
  - category and sub-category code;
  - legal name;
  - designation.
- **The donee's own return** (latest FPE in the same release):
  - line 4700 (revenue);
  - line 5050 (gifts to qualified donees);
  - line 4200 (total assets);
  - line 5860;
  - number of T1236 rows;
  - the share of its own T1236 gifts that go to health-named or health-coded donees, and the share going to university/college-named donees.

### 1.3 Donee typing (P-B3946-01)

Rules apply in order; the first that matches wins (`type_rule` column):

| Type | Rule |
|---|---|
| giving_platform | CanadaHelps (BN 896568417), named; or any donee with ≥ 1,000 own T1236 rows and line 5050 ≥ 80% of line 4700 (catches PayPal Giving Fund Canada: 8,478 rows, ratio 0.94) |
| federation_united_way | name: United Way, Centraide, Federation CJA, United Jewish Appeal, Jewish Federation, ShareLife |
| hospital_health | name: hospital, health, santé, CHU, cancer, hospice, medical, mental, rehabilitation…; else category 0100–0140 (health); else ≥ 50% of own T1236 gifts to health donees (e.g. St. Paul's Foundation of Vancouver → Providence Health Care Society) |
| university_college | name: universit*, college, cégep, polytechni*, institute of technology, Technion, Weizmann, HEC; else ≥ 50% of own gifts to university/college donees |
| other_education | category 0010–0015 (education), not matched above |
| community_foundation | name: community foundation, fondation communautaire, community trust |
| religious | category 0030–0090 |
| other | residual |

- **Category codes** (codes_en.pdf §2.1–2.2): 0210 "Foundations" has only two sub-categories, 0001 "Foundations for specified community benefit" and 0002 "Foundations funding community benefit QDs in general" [F]. The Education (0015), Religion (0090) and Poverty (0002) foundation codes have the same split. Health has no foundation code [F], which is why hospital foundations sit mostly in 0210.
- **Tiers.** The nested middle tiers between parent tier B (any 5860 = Y donee) and tier C (B plus all private and public foundations) are:

| Variant | Transfers counted |
|---|---|
| tier_b | parent tier B |
| tier_b_ch | B + CanadaHelps only (the "if CanadaHelps were a sponsor" netting case) |
| **tier_bp** | **B + giving_platform (the rebuilt middle tier)** |
| tier_bp_cf | tier_bp + community_foundation |
| tier_bp_cf_f | tier_bp_cf + federation_united_way |
| tier_b_pub | B + all public foundations (C without private foundations) |
| tier_c | parent tier C |

- **Definitions** are as in the parent: transfers are capped at line 5864 (blank = 0); payout is net ÷ prior-release line 5862 for matched sponsors.

### 1.4 Schedule 8 coverage (P-B3946-03)

- **Universe.** Every return in the Section D / Schedule 6 file of each release, one row per BN × FPE (83,872 in 2024; 79,012 in 2025). "Large" means line 5900 > C$1m.
- **Match.** A Schedule 8 row is matched on BN and FPE. The script also checks any FPE of the same BN; no return was matched that way.
- **Breakdowns:**
  - form ID;
  - FPE month and quarter, because the published file has no filing date (§3.1);
  - the line 5850 answer;
  - designation;
  - line 5860;
  - Section used;
  - whether T1236 rows exist.
- **Panel sponsors without Schedule 8.** The DQ is imputed by applying the Schedule 8 formula (3.5% up to C$1m, then C$35,000 + 5% above) to line 5900. Spending is Schedule 6 lines 5000 + 5045 + 5050. The parent's route codes are then applied, with "net" meaning 5864 net of tier-B transfers.
- **Limits of the imputation.** Line 810 (accumulation) is unknown, so it is ignored. So are the A ÷ 365 pro-rating and the C$25k/C$100k de minimis.

### 1.5 CanadaHelps (P-B3946-04)

- **Products.** Read from CanadaHelps' own pages:
  - home and About;
  - Cause Funds, Our Fees and Donate Securities;
  - Terms of Use and the Donation Delivery and Refund Policy (last updated 2026-08-26);
  - the Gifts of Securities Policy and Corporate Giving;
  - the audited financial statements for FY2025 and FY2024 (years ending June 30).
- **Definition.** The C18 DAF definition is the T3010 guide text as quoted by Blumberg & Pasha (canada.ca unreachable).
- **Panel effect.** CanadaHelps is added to each release's 5860 = Y panel under two proxies for line 5862:
  - (a) designated cash, i.e. "contributions due to designated charities", from the audited statements;
  - (b) line 4200, total assets.
- **Disbursement proxy.** Line 5864 is proxied by its line 5050. Its own tier-B transfers (gifts to 5860 = Y sponsors) are netted for the tier-B case.

---

## 2. Results: public-foundation donees and the middle tier (P-B3946-01)

### 2.1 Tier-C public-foundation gifts by donee type [C]

| Type | 2025: C$m | 2025: share | 2025: donees | 2025: sponsor donors | 2024: C$m | 2024: share | 2024: donees |
|---|---|---|---|---|---|---|---|
| hospital_health | 190.2 | 42.7% | 622 | 137 | 168.5 | 41.8% | 649 |
| federation_united_way | 76.3 | 17.1% | 59 | 68 | 96.1 | 23.9% | 62 |
| other_education | 49.7 | 11.2% | 194 | 59 | 19.5 | 4.8% | 198 |
| university_college | 34.8 | 7.8% | 139 | 76 | 41.3 | 10.2% | 146 |
| giving_platform | 10.5 | 2.3% | 2 | 32 | 0.4 | 0.1% | 2 |
| community_foundation | 4.5 | 1.0% | 71 | 34 | 4.8 | 1.2% | 72 |
| religious | 4.2 | 0.9% | 72 | 42 | 5.0 | 1.2% | 70 |
| other | 75.4 | 16.9% | 916 | 149 | 67.2 | 16.7% | 950 |
| **Total** | **445.5** | 100% | 2,075 | | **402.7** | 100% | 2,149 |

**How the rules split 2025 dollars** [C]:
- hospital_health: by name C$170.3m; by the beneficiary rule C$18.2m; by category C$1.7m.
- federations: all by name.
- university_college: by name C$32.4m; by the beneficiary rule C$2.3m.
- giving_platform: CanadaHelps (named) C$10.45m. PayPal Giving Fund Canada (data rule) received C$1,000 from one sponsor.

**Largest donees by type, 2025** [C]:
- **Federations:** Federation CJA C$32.4m (8 sponsor donors), UJA of Greater Toronto C$30.9m (23), United Way of Winnipeg C$3.1m, Jewish Federation of Winnipeg C$2.4m.
- **Hospital/health:** Jewish General Hospital Foundation C$13.2m, VGH & UBC Hospital Foundation C$12.9m, Alberta Children's Hospital Foundation C$10.6m, Princess Margaret Cancer Foundation C$9.4m, St. Paul's Foundation of Vancouver C$6.6m (beneficiary rule).
- **University/college:** Canadian Associates of Ben-Gurion University C$13.3m, Canadian Friends of the Hebrew University C$1.8m, BCIT Foundation C$1.7m.
- **Other education:** CanEd Foundation C$36.0m, in a single gift from Private Giving Foundation (the parent's largest tier-C edge). CanEd's own T3010 shows C$21.3m revenue and C$17.9m of gifts to 9 qualified donees; the largest is Claireville Christian Education Trust (C$7.6m). Whether CanEd holds donor-advised balances is open (P-B3946-05) [C/I].
- **Platforms:** CanadaHelps C$10.45m, of which C$10.16m came from St Mary's General Hospital Foundation (Kitchener-Waterloo) (§4.4).
- **Other (residual):** Coast Conservation Endowment Fund C$4.0m, Youth With A Mission Foundation C$2.9m, BC Parks Foundation C$2.7m, Right To Food C$2.6m, CharityEx Foundation C$2.1m (own line 5050 = 102% of line 4700).

### 2.2 Payout on prior-year DAF assets under each tier [C]

**2025 release, all matched sponsors** (n = 586; base C$15.39bn; gross 13.30%):

| Variant | Transfers (capped) | Aggregate net | Median sponsor | Share < 5% |
|---|---|---|---|---|
| tier_b (parent) | C$192.9m | 12.05% | 4.89% | 50.9% |
| tier_b_ch | C$193.1m | 12.04% | 4.84% | 50.9% |
| **tier_bp (middle tier)** | **C$193.1m** | **12.04%** | **4.84%** | **50.9%** |
| tier_bp_cf | C$197.5m | 12.02% | 4.82% | 51.1% |
| tier_bp_cf_f | C$270.4m | 11.54% | 4.74% | 51.3% |
| tier_b_pub | C$594.1m | 9.44% | 4.18% | 53.8% |
| tier_c (parent) | C$689.2m | 8.82% | 4.18% | 53.8% |

**Other populations, aggregate net** (gross → B / BP / BP+CF+F / C):

| Population | Gross | B | BP | BP+CF+F | C |
|---|---|---|---|---|---|
| 2025 itemised only (n = 478) | 13.26% | 11.94% | 11.94% | 11.41% | 8.54% |
| 2025 top-20 (n = 20) | 11.34% | 10.15% | 10.15% | 9.60% | 6.78% |
| 2024 all matched (n = 336) | 16.41% | 14.28% | 14.28% | 14.01% | 10.74% |

In 2024 the medians under BP equal those under B (5.43%) [C].

**Reading** [I]:
- **The only DAF-like public-foundation donee by product is CanadaHelps (§4),** and the money sponsors send it is almost entirely non-DAF money, because the largest donor reports no 5864. Tier BP therefore equals tier B to within 0.01 point.
- **The B-to-C gap is mostly program grants.** Federations add 0.48 point. Hospital, university, education and other public foundations add 2.10 points (BP+CF+F to all public). Private foundations add 0.62 point (all public to C). Most of this is grants to institutional fundraising foundations whose own gifts go to a single hospital or university.
- **Federations are a judgment call.** They regrant (in 2025 their own line 5050 is 56% (Federation CJA) and 71% (UJA) of revenue [C]), but their allocations are campaign-driven, not donor-advised [I]. Counting them as transfers would make 11.5% the netted figure.
- **Recommended reporting.** Report tier B (12.0%) as the central netted figure. Show tier BP+CF+F (11.5%) as a high-netting sensitivity, and tier C (8.8%) only as an upper bound [I].

### 2.3 What category codes add

Codes split health (0100–0140) and education (0010–0015) charities from foundations. But 74.4% of 2025 public-foundation dollars go to code 0210, and the 0001/0002 sub-codes describe purpose breadth, not intermediary status. Hospital/health dollars split C$147.1m under 0210/0001 and C$21.5m under 0210/0002; federation dollars sit almost all under 0210/0002 (C$74.9m) [C]. Codes are therefore a weak typing signal on their own [I].

---

## 3. Results: why large DAF sponsors have no Schedule 8 row (P-B3946-03)

### 3.1 Counts [C]

| | 2024 release | 2025 release |
|---|---|---|
| Returns in Section D / Schedule 6 file | 83,872 (all Form ID 27) | 79,012 (all Form ID 27) |
| Schedule 8 rows | 14,631 | 14,852 |
| Returns with line 5900 > C$1m | 6,270 | 6,593 |
| … with no Schedule 8 row (any FPE of the BN) | **254 (4.1%)** | **226 (3.4%)** |
| … line 5900 total of those | C$5.46bn | C$5.30bn |
| … of which line 5850 = N | 235 of 236 N answers | 196 of 197 N answers |
| … of which line 5850 blank | 17 of 17 | 14 of 14 |
| … of which line 5850 = Y | 2 of 6,017 Y answers | 16 of 6,382 Y answers |
| … with T1236 rows for the same return | 140 | 133 |
| … by designation (A / B / C) | 49 / 41 / 164 | 47 / 38 / 141 |
| All returns: Schedule 8 present when 5850 = Y | 14,475 of 14,547 | 14,780 of 15,215 |
| All returns: Schedule 8 present when 5850 = N | 110 of 67,785 | 71 of 62,962 |

- **Filing date.** The dictionary lists a "Filing Date" field ("Date return was filed by the charity", Associated Form ID 27) for the Schedule 8 dataset [F, dictionary §3.19]. Neither published Schedule 8 CSV has that column (header: BN, FPE, Form ID, 805–890), and no other file carries a filing date [C]. Counts by filing date are therefore not possible from open data; FPE is used instead.
- **Form version.** Both releases' financial files contain only Form ID 27, so the breakdown by form version is a single cell [C]. (The 2023 release still has v26 returns, e.g. CanadaHelps' FPE 2023-06-30 return.)

**Missing share by FPE quarter, returns with 5900 > C$1m** [C]:

| Release | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 2024 | 5.8% (77 / 1,328) | 5.2% (46 / 885) | 5.0% (22 / 437) | 3.0% (109 / 3,620) |
| 2025 | 4.3% (64 / 1,491) | 4.0% (38 / 954) | 3.3% (16 / 484) | 2.9% (108 / 3,664) |

### 3.2 Testing the two explanations

- **Processing lag.** Not supported [C/I]:
  - If CRA posted Schedule 8 later than the rest of the return, the missing share should be higher in the newer release and for later FPEs. The opposite holds: 4.1% in the older 2024 release against 3.4% in 2025, and Q4 FPEs have the lowest share in both releases.
  - More than half of the returns without Schedule 8 do have T1236 rows posted.
  - One pattern is compatible with a small lag: the number of 5850 = Y returns without Schedule 8 rose from 72 (2024) to 435 (2025) across all returns, and from 2 to 16 among large ones [C]. This is a residual, not the main gap [I].
- **Paper filing.** Not testable directly, and not needed [F/I]:
  - The dictionary says old versions "(i.e. v23, 24, 25, 26) can still be entered into the system if they are received by paper, an adjustment to the old version is being processed" (§1.4.5) [F]. Every return here is v27, so the old-paper-form route does not apply [C].
  - No open-data field records the filing channel, so paper v27 returns cannot be identified [C]. The dictionary describes Schedule 8 as part of the v27 form (3 pages) [F].
- **The 5850 answer.** This is what predicts the gap [C/I]:
  - Line 5850 asks whether the 24-month average of property not used in charitable activities exceeded C$100,000 (charitable organizations) or C$25,000 (foundations) [F, dictionary §3.4].
  - With 5850 = Y, 99.7% of large returns have Schedule 8. With 5850 = N or blank, 1 of 211 does (2025) [C].
  - The dictionary does not state that 5850 = N skips Schedule 8. That is the inferred mechanism, and the T4033 guide on canada.ca could not be checked (P-B3946-06) [I].
  - The 5850 = N answers on these returns are internally inconsistent: line 5900 on the same return is the same 24-month average, and it exceeds C$1m [C].

### 3.3 DAF sponsors without Schedule 8 [C]

- **2025 release.** 489 panel sponsors (C$2.793bn of DAF assets) have no Schedule 8 row.
  - C$2.791bn of it sits with sponsors that answered 5850 = N.
  - 421 of them answered N and left line 5900 blank.
  - 173 (C$2.788bn) answered N although their own year-end DAF assets alone exceed the 5850 threshold.
- **2024 release.** 473 sponsors (C$2.489bn); 171 of them (C$2.482bn) above the threshold.
- **Sponsors with line 5900 > C$1m and no Schedule 8** (2025: 7; 2024: 5). Imputed DQ = formula on line 5900:

| Release | Sponsor | Desig. | 5850 | Line 5900 | DAF assets | 5864 | Imputed DQ | Sched. 6 spending | Imputed route |
|---|---|---|---|---|---|---|---|---|---|
| 2025 | Jewish Community Foundation of Montreal | A | N | C$2,143.0m | C$2,516.2m | C$236.9m | C$107.1m | C$241.3m | DAF_NET_COVERS |
| 2025 | Saskatoon Community Foundation | A | N | C$74.9m | C$23.5m | C$2.6m | C$3.7m | C$7.6m | NEEDS_NON_DAF |
| 2025 | Charities Aid Foundation Canada | C | N | C$20.0m | C$15.8m | C$11.3m | C$1.0m | C$34.2m | DAF_NET_COVERS |
| 2024 | Jewish Community Foundation of Montreal | A | N | C$1,850.5m | C$2,114.1m | C$213.9m | C$92.5m | C$220.6m | DAF_NET_COVERS |

The others (four in 2025, four in 2024) are small DAF holders (C$0.2m of DAF assets or less): churches, a museum and small charities. All are NEEDS_NON_DAF [C].

- **Imputed routes for the large no-Schedule-8 sponsors.** In 2025, 2 DAF_NET_COVERS (C$2.53bn of DAF assets) and 5 NEEDS_NON_DAF (C$0.02bn). None is in shortfall [C].
- **Effect on the parent's DQ table.** About C$2.53bn of the parent's C$2.79bn "NO_SCHEDULE8" DAF assets would sit in DAF_NET_COVERS. The C$2.79bn total is from the parent table; C$2.53bn is from this script, and the comparison is an inference [I]. JCF Montreal (2025 rank 2) joins the top-20 sponsors that meet the DQ from DAF disbursements alone, making 14 of 20 [C/I].

---

## 4. Results: CanadaHelps (P-B3946-04)

### 4.1 What CanadaHelps offers (its own pages, read 2026-11-19) [F]

- **Legal form of a gift.** Donations "are legally made to CanadaHelps CanaDon, a charity registered with the Canada Revenue Agency (Registration Number: 896568417RR0001), and CanadaHelps CanaDon issues the official tax receipt" (Terms of Use; refund policy).
  - CanadaHelps "acts on donations through an implied trust relationship, where donated funds are given to CanadaHelps to then be delivered to a final recipient charity or charities as identified by the donor".
  - It may redirect a gift at the donor's request, or when the charity refuses it, is suspended or revoked, or the funds are undeliverable.
  - After 18 months undeliverable gifts are "deemed 'undisbursable'" and used "in a charitable manner" (refund policy).
- **Single and monthly donations.** "Charities that have signed up for Electronic Funds Transfer (EFT) with CanadaHelps will receive donations weekly"; "Over 99% of donations made to CanadaHelps are delivered via EFT" (refund policy). Fees: 4.5% one-time, 4.0% monthly (Our Fees).
- **Cause Funds (pooled, curated).**
  - "Registered Canadian charities supporting a specific cause are hand picked, vetted, and invited to join the fund by our expert curators … Donations are then dispersed evenly amongst all charities included in the fund" (Cause Funds page).
  - They are "normally disbursed quarterly …. If disbursement minimums of at least $10 per charity recipient have not been met, the donations to the fund will roll over to the next quarter, to a maximum of two quarters" (refund policy). Fee 3.75%.
- **Charity "Funds" (designated funds).** "Charities may choose to offer Funds to which donors can recommend their gifts. If no Funds have been created, donations will be made to the charity's General Fund"; "Gifts made through CanadaHelps are unrestricted" (refund policy; Terms of Use).
- **Securities.** The tax receipt is issued when the securities are sold; the proceeds are disbursed "as part of our normal disbursement cycle" (refund policy). Fee 2–3%, with flat fees above C$250,000 (Our Fees).
- **Charity gift cards.** "You choose the design and the recipient chooses the charity" (home page).
  - The audited statements treat "gift cards that have not been redeemed after 18 months" as undisbursable, while "CanadaHelps will always honour and redeem any and all gift cards" (FY2025 statements, note 2).
  - The gift-card page itself was not reachable (500/404).
- **Other products.** Fundraising pages, eCards, charitable gifts, and corporate giving with matching (Corporate Giving page).
- **The audited statements' own list:** "single and monthly gifts, gifts of securities, charity gift cards, fundraising pages, cause funds, and more" (FY2025 statements, note 1).
- **Not found.** No giving fund, donor-advised account, donor balance held for later grants, or pooled investment portfolio appears on any page checked. The "CanadaHelps account" is described as a place to "track donations and get instant tax receipts" (About page) [F]. This is absence on the pages read, not proof of absence [I].

### 4.2 Fit to the T3010 C18 definition

**The definition (C18), as quoted by Blumberg & Pasha** [F, secondary; canada.ca unreachable]: "a DAF is a fund segregated into donor accounts, owned and controlled by a registered charity. Each account is comprised of contributions made by individual donors. Donors may provide ongoing non-binding suggestions on payouts from DAFs, but it is the charity's sole responsibility to make such decisions."

| Product | Segregated donor accounts? | Ongoing non-binding donor advice? | Fit [I] |
|---|---|---|---|
| Single/monthly donations | No: each gift names a charity at the time of giving and is sent weekly | No: one designation, with redirection only in exceptions | No |
| Cause Funds | No: one pool across donors | No: curators choose; equal split | No |
| Charity "Funds" | No: a purpose label at the recipient charity | No | No |
| Securities | No: sold and passed through | No | No |
| Charity gift cards | Closest: a per-card balance held until redeemed | One later choice by the recipient, not ongoing advice by the donor | Borderline at most |

- **Conclusion** [I]: CanadaHelps' 5860 = N answer is consistent with C18. CanadaHelps owns and controls the gifts, as C18 requires. But its products lack the account structure and ongoing advisory role that define a DAF.
- **Upper bound on DAF-like balances.** Gift-card balances are not shown separately. They are included in "designated cash … for immediate payment to charities": C$11,019,785 at 2025-06-30, against C$10,028,476 a year earlier and C$8,874,105 at 2023-06-30. C$8,942,124 of the 2025 balance was paid out in July 2025 [F, statements notes 6–7]. Undisbursable funds recognised as revenue were C$348,624 in FY2025 [F].

### 4.3 CanadaHelps in the T3010 open data [C]

| Release (FPE) | Form | 5850 | 5860 | Line 4700 | Line 5050 | Line 4200 | Line 5900 | T1236 rows | T1236 total | Schedule 8 |
|---|---|---|---|---|---|---|---|---|---|---|
| 2024 (2024-06-30) | 27 | Y | N | C$448.6m | C$426.3m | C$22.2m | C$4.5m | 35,989 | C$775.3m | yes |
| 2025 (2025-06-30) | 27 | Y | N | C$490.1m | C$467.1m | C$24.4m | C$5.25m | 31,844 | C$467.1m | yes |

- **Line 5050 against the audited statements.** Line 5050 equals the audited "Donations to charities" exactly in both years: C$467,074,451 and C$426,283,424 [C/F].
- **2024 worksheet anomaly.** The 2024-release T1236 total (C$775.3m) exceeds line 5050 by 82% [C]. The 2025 one matches (P-B3946-08).
- **Gifts to sponsors.** In 2025, CanadaHelps' own gifts to 5860 = Y sponsors were C$20.5m: C$5.5m to DAF-primary sponsors and C$15.0m to other sponsors [C].

### 4.4 Effect on the Canadian panel if CanadaHelps were counted [C]

Line 5862 proxy = designated cash (proxy b, line 4200, in brackets where it differs); line 5864 proxy = line 5050.

| Measure | 2025 release: baseline | 2025: with CanadaHelps | 2024 release: baseline | 2024: with CanadaHelps |
|---|---|---|---|---|
| Sponsors | 864 | 865 | 846 | 847 |
| DAF assets | C$18.60bn | C$18.61bn (C$18.62bn) | C$16.67bn | C$16.68bn (C$16.69bn) |
| DAF disbursements | C$2.086bn | C$2.553bn | C$1.927bn | C$2.353bn |
| Aggregate same-year payout (5864 ÷ 5862) | 11.21% | 13.72% (13.71%) | 11.56% | 14.11% (14.10%) |
| Aggregate on prior-year assets, matched | 13.30% | 16.32% (16.31%) | 16.41% | 22.19% (22.16%) |
| Same, net of tier-B transfers | 12.05% | 14.94% (14.93%) | 14.28% | 19.57% (19.54%) |
| CanadaHelps rank by 5864 / by 5862 | — | 1 / 76 (48) | — | 1 / 76 (53) |
| CanadaHelps share of panel 5864 | — | 18.3% | — | 18.1% |
| CanadaHelps own payout, same year | — | 42.4× (19.1×) | — | 42.5× (19.2×) |

- **Netting effect of treating CanadaHelps as a sponsor-type donee** (tier_b_ch): 2025 aggregate 12.05% → 12.04%; capped transfers rise by C$0.17m (2024: unchanged at 14.28%). The reason is that C$10.16m of the C$10.45m that sponsors gave CanadaHelps in 2025 came from St Mary's General Hospital Foundation, which answered 5860 = Y but left 5864 blank, so the cap is zero. The other 30 sponsor donors gave C$0.29m [C]. In 2024, 30 sponsors gave CanadaHelps C$0.39m [C].
- **Reading** [I]. Adding a C$467m-a-year pass-through with an C$11m float would raise Canadian "DAF payout" by about 2.5 to 3 points on the same panel. This would reflect a payment rail, not DAF behaviour. Keeping CanadaHelps out, as its own 5860 answer does, is the right default. If a "platform-inclusive" Canadian figure is ever needed, it should be shown separately, as the US work does for processors.

---

## 5. Limits

- **Typing.** Typing rests on names, category codes and the donee's own T1236 recipients; it is not a hand audit.
  - The beneficiary rule can mislabel a multi-purpose foundation whose largest gifts happen to go to a hospital.
  - The residual "other" type holds C$75.4m (2025), and "other_education" includes CanEd Foundation (C$36.0m), whose nature is not established (P-B3946-05).
  - Disease and research charities (e.g. cancer foundations) count as hospital/health.
- **Platform detection.** It uses a named list plus one data rule (≥ 1,000 T1236 rows and ≥ 80% pass-through). It found only CanadaHelps and PayPal Giving Fund Canada. Platforms that are charitable organizations (designation C) are outside tier C by construction and so outside this question.
- **T1236 coverage.** T1236 covers DAF and non-DAF gifts. Transfers stay capped at 5864, which is why a large gift by a sponsor with blank 5864 nets nothing (St Mary's GHF).
- **Schedule 8 data:**
  - No filing date or filing channel is published, so the paper and lag tests are indirect.
  - The 5850 → Schedule 8 skip is inferred from the data; the dictionary does not state it, and the T4033 guide was unreachable.
  - The imputed DQ ignores line 810, short-year pro-rating and the de minimis thresholds.
- **CanadaHelps:**
  - The product review covers the public pages listed in §1.1. The help-centre articles render only with JavaScript and were not read, and the gift-card page returned errors.
  - Designated cash is a June 30 snapshot. It mixes in-transit gifts, securities awaiting sale and gift-card balances.
  - C18 is a secondary quotation.
- **Recency.** All sources are 2021 or later. CanadaHelps pages were read 2026-11-19, and its refund policy is dated 2026-08-26.

---

## 6. Data dictionary: `canada-followups-2026-11-19.csv`

Long format; the `section` column says which columns are filled. Amounts are in C$ as filed. Ratios are fractions. Booleans are yes/no; blank means not applicable.

| Section | Rows | One row per |
|---|---|---|
| `pf_donee` | 4,224 | public-foundation donee × release that received tier-C gifts from 5860 = Y sponsors |
| `tier_payout` | 42 | release × population (all_matched, itemised_only, top20) × tier variant |
| `no_sched8_return` | 480 | v27 return with line 5900 > C$1m and no Schedule 8 row (254 in 2024, 226 in 2025) |
| `canadahelps` | 74 | release × scenario (baseline, designated_cash, total_assets_4200) × metric |

| Column | Sections | Meaning |
|---|---|---|
| section | all | See above |
| dataset_year | all | CRA release year (calendar year of the FPE) |
| bn, legal_name, designation, category_code, sub_category_code | pf_donee, no_sched8_return; bn in canadahelps | Identification file values (designation A public foundation, B private foundation, C charitable organization; codes per codes_en.pdf) |
| donee_type, type_rule | pf_donee | Type and the rule that assigned it (§1.3) |
| received_from_sponsors, n_sponsor_donors | pf_donee | Sum of T1236 gifts from 5860 = Y sponsors in the release; number of distinct sponsor donors |
| share_of_public_fdn_gifts | pf_donee | received_from_sponsors ÷ all public-foundation tier-C gifts in the release |
| own_revenue_4700, own_gifts_5050, own_total_assets_4200, own_t1236_rows | pf_donee | The donee's own return (latest FPE in the release) |
| own_pass_through | pf_donee | own_gifts_5050 ÷ own_revenue_4700 |
| own_share_to_health, own_share_to_univ | pf_donee | Share of the donee's own T1236 gifts to health-named/coded and university/college-named donees |
| own_5860 | pf_donee, no_sched8_return | Line 5860 answer on the donee's / return's Section C |
| fpe, form_id, fpe_quarter | no_sched8_return (fpe also canadahelps) | Fiscal period end, T3010 form ID, calendar quarter of the FPE |
| line_5850, line_5900 | no_sched8_return | Line 5850 answer; line 5900 (24-month average of property not used in charitable activities) |
| has_t1236 | no_sched8_return | T1236 rows exist for the same BN and FPE |
| panel_sponsor | no_sched8_return | BN is a 5860 = Y panel sponsor in the release |
| daf_assets_5862, daf_disbursements_5864 | no_sched8_return | Panel values for sponsors |
| imputed_dq_from_5900 | no_sched8_return | Schedule 8 formula applied to line 5900 |
| sched6_spending | no_sched8_return | Schedule 6 lines 5000 + 5045 + 5050 |
| imputed_route | no_sched8_return | Parent route code from imputed DQ, 5864, 5864 net of tier B, and spending (sponsors only) |
| variant, population | tier_payout | Tier variant (§1.3) and sponsor population |
| n_sponsors, prior_daf_assets, gross_5864, payout_gross | tier_payout | Matched sponsors, base, gross 5864, gross aggregate payout |
| transfers_capped, payout_net, median_net, share_lt_5pct | tier_payout | Variant transfers capped at 5864; aggregate net payout; median sponsor net payout; share of sponsors below 5% |
| scenario, note, value | canadahelps | Scenario; metric name (e.g. aggregate_same_year, ch_rank_by_5864, ch_net_5864_tier_b); its value |

## 7. Source register

| ID | Source | URL | Grade | Read |
|---|---|---|---|---|
| S01 | CRA, Charities codes list (codes_en.pdf), 2025 and 2024 List of charities releases (identical files) | https://open.canada.ca/data/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8/resource/f02a27ca-0abc-4af5-8b29-86e726896076/download/codes_en.pdf ; https://open.canada.ca/data/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8/resource/e9f81074-9fc7-456f-8ce1-6fd101b77963/download/codes_en.pdf | P | 2026-11-19 |
| S02 | CRA, List of charities data dictionary v2.0 (§1.4, §1.4.5, §3.4 line 5850, §3.19 Schedule 8 incl. "Filing Date") | https://open.canada.ca/data/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8/resource/5c37b152-9381-4a8c-a475-fc8a60c6512b/download/open-data-data-dictionary-v2.0_eng.pdf | P | 2026-11-19 (parent download) |
| S03 | CRA open data 2025 release: Identification, Sections A–C, Section D/Schedule 6, qualified donees, Schedule 8 | https://open.canada.ca/data/en/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 | P | 2026-11-19 (parent downloads) |
| S04 | CRA open data 2024 release: same files | https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 | P | 2026-11-19 (parent downloads) |
| S05 | CRA open data 2023 release: Identification, Sections A–C, Section D/Schedule 6 | https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6 | P | 2026-11-19 (parent downloads) |
| S06 | CanadaHelps, Donation Delivery and Refund Policy (last updated 2026-08-26) | https://www.canadahelps.org/en/donation-delivery-and-refund-policy/ | P | 2026-11-19 |
| S07 | CanadaHelps, Terms of Use | https://www.canadahelps.org/en/terms-of-use/ | P | 2026-11-19 |
| S08 | CanadaHelps, Cause Funds | https://www.canadahelps.org/en/cause-funds/ | P | 2026-11-19 |
| S09 | CanadaHelps, Our Fees | https://www.canadahelps.org/en/why-canadahelps/our-fees/ | P | 2026-11-19 |
| S10 | CanadaHelps, home page and About (Why CanadaHelps) | https://www.canadahelps.org/en/ ; https://www.canadahelps.org/en/why-canadahelps/ | P | 2026-11-19 |
| S11 | CanadaHelps, Donate Securities; Gifts of Securities Policy; Corporate Giving; Tax Receipts | https://www.canadahelps.org/en/donate/donate-securities/ ; https://www.canadahelps.org/en/gifts-of-securities-policy/ ; https://www.canadahelps.org/en/why-canadahelps/corporate-giving/ ; https://www.canadahelps.org/en/tax-receipts/ | P | 2026-11-19 |
| S12 | CanadaHelps CanaDon, audited financial statements, year ended June 30, 2025 (notes 1, 2, 7, 10) | https://www.canadahelps.org/media/2024-2025_CanadaHelps_CanaDon_FinancialStatement.pdf | P | 2026-11-19 |
| S13 | CanadaHelps CanaDon, audited financial statements, year ended June 30, 2024 (designated cash 2023-06-30) | https://www.canadahelps.org/media/2023-2024_CanadaHelps_CanaDon_FinancialStatement.pdf | P | 2026-11-19 |
| S14 | CanadaHelps sitemaps (index, static) and help-centre sitemaps | https://www.canadahelps.org/sitemap.xml ; https://help.canadahelps.org/s/sitemap.xml | P | 2026-11-19 |
| S15 | Blumberg & Pasha, *Blumbergs DAF Report: Donor Advised Fund accounts in 2024* (2026-02-10), quoting the CRA T3010 guide, C18 | https://carleton.ca/profbrouard/wp-content/uploads/sites/281/2026/10/reportBlumbergPasha2026DAFReportDonorAdvisedFundaccounts2024Final.pdf | S (quotes P) | 2026-11-19 (parent download) |
| S16 | Repo: parent netting and DQ study and wave-38A corrections | [b39n3-0406-canada-netting-dq.md](b39n3-0406-canada-netting-dq.md); [validation-wave38a-report.md](validation-wave38a-report.md) | R | 2026-11-19 |
