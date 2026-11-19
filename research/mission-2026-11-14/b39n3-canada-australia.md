# Canada T3010 DAF panel and Australia giving-fund rules (P-B39N3-01, P-B39N3-02)

**Prepared 2026-11-19 (task b39n3). Desk research only: no outreach, no logins, no forms.** This is research, not legal or tax advice. It follows up [`direction-international-comparison.md`](direction-international-comparison.md) (N3) §4–§5 and its governing wave-24A corrections, none of which touch the Canadian figures or the Australian rules used here.

**Labels.** **[F]** the source states it; **[C]** computed by `scripts/mission_canada_daf_panel.py` or simple arithmetic on its output; **[I]** inference. Evidence grades in the Australia CSV: **P** primary fetched and read; **PS** primary seen only as a search snippet; **S** secondary; **R** validated repo finding.

**Outputs.**
- [`data/mission-2026-11-14/canada-daf-panel-2026-11-19.csv`](../../data/mission-2026-11-14/canada-daf-panel-2026-11-19.csv): 2,165 rows, one per charity and CRA release year (2023: 455; 2024: 846; 2025: 864) where T3010 line 5860 = Y.
- [`data/mission-2026-11-14/australia-ancillary-fund-rules-2026-11-19.csv`](../../data/mission-2026-11-14/australia-ancillary-fund-rules-2026-11-19.csv): 15 rows on rules, status, dates and statistics.
- [`scripts/mission_canada_daf_panel.py`](../../scripts/mission_canada_daf_panel.py): stdlib, functional; builds the panel and prints a JSON summary (all Canadian numbers below).
- [`data/mission-2026-11-14/queue-proposals-b39n3.csv`](../../data/mission-2026-11-14/queue-proposals-b39n3.csv): 5 follow-ups (P-B39N3-04 to -08).

Reproduce: download the CRA files listed in §1.2 into a directory `DIR` (named `{year}_{abc|ident|fin}_<original name>`), then
`python3 scripts/mission_canada_daf_panel.py . --data-dir DIR --blumberg-txt blumberg.txt --summary out.json`
(`blumberg.txt` = `pdftotext -layout` of the Blumberg–Pasha PDF).

---

## Headline findings

1. **The CRA open data reproduce Blumberg & Pasha's 2024 totals almost exactly.** The 2024 release has 846 charities answering line 5860 = Y and C$16.670bn of DAF assets. Blumberg & Pasha report 834 charities and C$16,644,279,820 [F]. 744 of our 755 rows with positive DAF assets carry a line-5862 value that appears verbatim in their PDF. Those rows sum to C$16.644bn [C]. The 11 unmatched rows (C$26.2m) are probably returns added after the report (10 Feb 2026): 9 of the 11 names do not appear in it, and 10 of the 11 have a 2024-12-31 year-end [I] [V wave 37B]
2. **Most reported Canadian DAF accounts are filing errors.** In the 2024 release, 14 returns with impossible account counts hold 126,002 of 186,421 accounts (68%). Examples: counts equal to dollar amounts on the same return (CCI Scholarship Fund reports 26,451 accounts and C$26,451 on every DAF line), and counts with no DAF dollars at all (38,980 and 25,781 accounts). Without them, 2024 has **60,419 accounts and an average of C$275,905** (Blumberg: 185,506 and C$89,724) [C].
3. **Latest year (2025 release, still incomplete): 864 sponsors, C$18.60bn of DAF assets, C$3.80bn in, C$2.09bn out, 70,757 clean accounts** [C]. 56 charities that held C$0.84bn of DAFs in 2024 have no 2025 return in the release yet, so the 2025 figures are a lower bound [C].
4. **Concentration is high and rising.** In 2025 the top 10 sponsors hold 68.1% of DAF assets and the top 5 hold 47.9% (2024: 63.8% and 44.2%). The HHI is 680. Charitable Gift Funds Canada is the largest (C$3.08bn, 16.6%) [C].
5. **Payout depends on the definition** [C]:
   - Same-year aggregate (line 5864 ÷ line 5862): 11.6% in 2024 and 11.2% in 2025. This is Blumberg's "12%".
   - Median sponsor: 10.6% (2024) and 12.2% (2025). Among sponsors with at least C$10m of DAF assets, the median is 8.4% (2024) and 7.3% (2025). These medians exclude sponsors with positive DAF assets and a blank line 5864 (155 in 2024, 241 in 2025). Counting blanks as zero, the medians are 5.4% and 4.0%, and 7.0% and 7.2% for sponsors with at least C$10m [V wave 37B]
   - US-comparable (disbursements ÷ prior-year DAF assets, matched sponsors): **13.3% in 2025** (586 sponsors) and 16.4% in 2024 (336 sponsors; the 2023 base is partial). The US figure is 22.8%, net of DAF-to-DAF transfers. The Canadian figure is gross of them, so the gap is if anything understated [I].
6. **WellFunded's figures (C$17.3bn in the August 2026 article; C$18.6bn, 205 sponsors and 82,611 accounts on its page today) fall between our two replicas on assets, grants out and sponsor count; donations in (C$3.62bn) fall below both replicas** [C] [V wave 37B]
   - On its stated rule (latest filing per charity, at least 10 accounts): 232 sponsors and C$19.40bn.
   - On the 2025 release only, with error rows removed: 203 sponsors, C$18.14bn and 69,324 accounts.
   - Its 82,611 accounts imply that it, too, drops the transposition rows [I].
7. **Australia has not amended the giving-fund guidelines as of 2026-11-19.** On legislation.gov.au, the 2022 public guidelines (F2022L00184) still have only their as-made version (4%), and the 2019 private guidelines (F2019L01227) have no compilation after 2022-02-25 (5%). No title containing "Giving Fund" exists, and no exposure draft was found [F]. Only the **rename** has happened: Act No. 86 of 2026 (C2026A00086), Schedule 7, commenced 2026-10-01. Its item 17 continues the existing guidelines as giving-fund guidelines [F]. The 6% rate with 3-year smoothing is therefore at the **decided, not drafted** stage [F/I].
8. **Australian sub-funds have no separate floor.** The guidelines mention sub-funds only in a note to s24 (a fund "may establish subfunds" and "cannot be under any obligation to comply with requests" from donors) and in s27 portability. The s15 minimum applies to "the fund's net assets". ACF confirms that sub-fund holders have no minimum and that the floor is computed "at the consolidated trust fund level" [F]. Public ancillary funds held A$4.7bn of net assets at 2022-23 (1,445 funds) [S]. **No national sub-fund count is published** in any source found.

---

## 1. Method

### 1.1 Robots.txt log (checked before any fetch; UA `research-script/1.0`)

| Host | Result | Use |
|---|---|---|
| open.canada.ca | 200; `Crawl-delay: 20`; `/data/` not disallowed | CKAN API + downloads, 20 s between requests |
| opencanada.blob.core.windows.net | 404 (no robots = allowed) | redirect target of downloads |
| www.canada.ca | connection reset / timeout twice | **not fetched** (T3010 guide T4033 quoted via Blumberg–Pasha) |
| api.prod.legislation.gov.au | 404 | titles, versions and document API |
| www.legislation.gov.au | 200; disallows `/assets/` only | links only |
| treasury.gov.au, ministers.treasury.gov.au | 200; disallows `/consultation`, `/publication` for all, and `/` for ClaudeBot and anthropic-ai | **not fetched**; repo-validated Treasury facts reused |
| consult.treasury.gov.au | 200; admin only disallowed | fetched; JavaScript app, no content |
| www.ato.gov.au | 403 on robots.txt | **not fetched** |
| data.gov.au | `Disallow: /` | **not fetched** |
| eprints.qut.edu.au | explicitly disallows Claude-User and ClaudeBot | **not fetched** |
| www.lexology.com | 403 | snippets only |
| www.acnc.gov.au | connection reset | not used |
| carleton.ca, futureofgood.co, www.wellfunded.io, www.philanthropy.org.au, communityfoundation.org.au | allowed | fetched |

### 1.2 Canada

- **Data.** These are CRA "List of charities" releases on open.canada.ca:
  - 2023: CKAN `05b3abd0-…`, modified 2026-11-15.
  - 2024: `80c00cdb-…`, modified 2026-11-15.
  - 2025: `4b60228a-…`, modified 2026-11-18.
  - Files used: Section A/B/C (lines 5860–5864), Identification, and Section D/Schedule 6 (line 4200 total assets, 4700 total revenue). They were downloaded 2026-11-19 20:58–21:01 UTC.
  - A release "year" is the calendar year of the fiscal period end (FPE). The 2024 release spans FPE 2024-01-31 to 2024-12-31 [C].
- **Line definitions** come from the CRA open-data dictionary v2.0 (rev. 2023-08-23), §1.4 "T3010 version (v27)", Section C questions C17/C18. They apply to "fiscal periods beginning on or after January 1, 2023" [F]:
  - 5860 Y/N: "Did the charity hold any donor advised funds (DAF) during the fiscal period?"
  - 5861 number: "Total number of accounts held at the end of the fiscal period"
  - 5862 amount: "Total value of all accounts held at the end of the fiscal period"
  - 5863 amount: "Total value of donations to DAF accounts received during the fiscal period"
  - 5864 amount: "Total value of qualifying disbursements from DAFs during the fiscal period"
  - The amounts are "Empty for exempt charities".
  - **T3010 guide (C18), as quoted by Blumberg–Pasha:** a DAF "is a fund segregated into donor accounts, owned and controlled by a registered charity. Each account is comprised of contributions made by individual donors. Donors may provide ongoing non-binding suggestions on payouts from DAFs, but it is the charity's sole responsibility to make such decisions" [F, secondary quotation; canada.ca not reachable].
- **Panel rules.**
  - The panel keeps one row per BN and release where 5860 = Y. No return answering N or blank carries DAF values in any release [C].
  - One 2024 BN filed two returns, and the later FPE is kept (`DUP_RETURN`).
  - Payout on prior-year assets is computed only when the same BN is a 5860 = Y filer in the previous release.
- **FY2023 is partial.** Only returns on form v27 (periods beginning in 2023) carry the DAF lines. That gives 455 filers and C$7.36bn, consistent with Blumberg's "roughly 400" for 2023 [F/C].
- **Error flags** (column `flags`). The four flags marked † make `accounts_clean = no`; the rest are informational.
  - `ACC_EQ_DOLLAR`† the account count equals a dollar line on the same return (5862, 5863, 5864, 4200 or 4700).
  - `ACC_GT_ASSETS`† more accounts than dollars of DAF assets, or negative DAF assets.
  - `AVG_LT_100`† average account below C$100.
  - `ACC_NO_DOLLARS_LARGE`† 100 or more accounts with no DAF dollars at all.
  - `ACC_NO_DOLLARS` (fewer than 100 accounts and no DAF dollars).
  - `DOLLARS_NO_ACC`, `ALL_BLANK`.
  - `ASSETS_GT_TOTAL` (DAF assets more than 105% of line 4200).
  - `PAYOUT_GT_100` (flow-through, not an error).
  - `DUP_RETURN`.
- **Reconciliation.**
  - **Blumberg:** every 2024 line-5862 value was searched verbatim (as `$1,234,567`) in the report text.
  - **WellFunded:** its published methodology was replicated (§2.4).

### 1.3 Australia

- **Register status:** the legislation.gov.au API was queried on 2026-11-19 for:
  - titles whose name contains "Ancillary Fund" or "Giving Fund";
  - the versions of F2022L00184 and F2019L01227.
- **Texts read:** the as-made texts of both guidelines and of Act C2026A00086, downloaded as Word documents from the API.
- **Searches:** web searches for an exposure draft and for ATO statistics.
- **Pages fetched:** Philanthropy Australia (explainer; tax-statistics article) and ACF FAQ.

---

## 2. Canada results

### 2.1 Totals by release [C]

| Release (FPE year) | Charities 5860=Y | DAF assets (5862) | Donations in (5863) | Disbursed (5864) | Accounts as filed | Accounts, clean | Avg account (clean) |
|---|---|---|---|---|---|---|---|
| 2023 (partial: v27 forms only) | 455 | C$7.358bn | C$1.825bn | C$1.056bn | 27,559 | 27,546 | C$267,113 |
| 2024 | 846 | C$16.670bn | C$3.288bn | C$1.927bn | 186,421 | 60,419 | C$275,905 |
| 2025 (incomplete) | 864 | C$18.600bn | C$3.802bn | C$2.086bn | 98,938 | 70,757 | C$262,925 |

- **By designation** (2025): public foundations hold C$16.91bn across 251 sponsors (91%). Private foundations hold C$0.86bn (42 sponsors) and charitable organizations C$0.82bn (571 sponsors) [C].
- **Small holders:** 571 of the 864 filers in 2025 are charitable organizations (churches, schools, service charities) holding 4.4% of DAF assets. Blumberg–Pasha warn that many such filers hold ordinary restricted gifts rather than DAFs in the usual sense [F; C].

### 2.2 Reconciliation with Blumberg & Pasha (2024) [F: S01; C]

| Measure | Blumberg–Pasha (10 Feb 2026) | CRA 2024 release (Nov 2026) | Note |
|---|---|---|---|
| Charities | 834 (text also says 837) | 846 | +12 late or re-processed returns |
| DAF assets | C$16,644,279,820 | C$16,669,975,994 | 744 of 755 asset rows match verbatim (C$16,643,795,632); 11 unmatched rows = C$26.18m, largest TRU Charitable Foundation C$21.5m |
| Donations | C$3,280,632,301 | C$3,288,429,475 | |
| Gifts | C$1,918,665,555 | C$1,926,501,382 | |
| Accounts | 185,506 ("highly exaggerated by transpositional errors") | 186,421 as filed; 60,419 clean | |
| Gifts ÷ assets | 12% | 11.56% | same definition, rounded |

### 2.3 Account-count transposition errors (2024 release) [C]

| BN | Charity | Accounts (5861) | DAF assets (5862) | Other evidence | Flag |
|---|---|---|---|---|---|
| 763897907RR0001 | Conseil de Sauvegarde de l'Eglise Carillon | 38,980 | blank | total assets C$34,844 | ACC_NO_DOLLARS_LARGE |
| 827824251RR0001 | CCI Scholarship Fund | 26,451 | 26,451 | 5863 = 5864 = 26,451 | ACC_EQ_DOLLAR |
| 890360522RR0001 | Friends of the Naval Museum Inc | 25,781 | blank | total assets C$41,035 | ACC_NO_DOLLARS_LARGE |
| 889230637RR0001 | Comité des oeuvres charitables du Conseil Alm… | 13,256 | 13,256 | all DAF lines 13,256 | ACC_EQ_DOLLAR |
| 886204999RR0001 | Comité des oeuvres charitables de l'Assemblée… | 12,518 | blank | **total assets = 12,518** | ACC_EQ_DOLLAR |
| 119070639RR0001 | Osgoode Presbyterian Church | 6,000 | 1 | 5864 = 6,000 | ACC_EQ_DOLLAR |
| 765722889RR0001 | La Clairière Église Chrétienne | 3,000 | 3,410 | avg C$1 | AVG_LT_100 |

- **2024 release:** these 7 rows alone account for 125,986 accounts.
- **2025 release:** the pattern repeats. Comité de Sauvegarde du Pont Couvert Drouin reports 12,161 accounts against total assets of 12,161, and the same Comité (886204999) reports 11,867 against total assets of 11,867. Selah Treatment Centre reports 4,140 accounts with no DAF dollars. In all, 28,181 accounts sit in 10 flagged rows [C].
- **Not errors:** two very large account counts are genuine high-volume programs:
  - Canadian Online Giving Foundation (Benevity's disbursing charity): 17,902 accounts in 2025, average C$1,566, pass-through.
  - CHIMP: 13,769 accounts, average C$51,768.
  - Together they hold **44.8% of clean 2025 accounts** (25.3% and 19.5%) but 4.0% of assets [C]. This parallels the US repo finding that processors dominate account counts.

### 2.4 Reconciliation with WellFunded / Future of Good

- **The article** (Future of Good, 2026-08-10): C$17.3bn across 205 sponsors on "most recent T3010 filings"; top ten hold 66% [F: S03].
- **The WellFunded page** (fetched 2026-11-19) [F: S04]:
  - Headline: 205 sponsors; 82,611 accounts; C$18.6B in assets; C$3.62B in; C$2.18B out; top 10 hold 68%.
  - Rule: "every active registered charity that reported holding donor-advised funds (line 5860) with at least ten fund accounts, using each charity's latest filing (fiscal years ending in 2024 or 2025)".
  - Payout is "line 5864 ÷ line 5862 in the same filing".
  - The difference between C$17.3bn and C$18.6bn is consistent with 2025 filings arriving between August and November [I].

| Replica [C] | Sponsors | Accounts | DAF assets | In | Out | Top-10 share |
|---|---|---|---|---|---|---|
| Stated rule (latest 2024/2025 filing, ≥10 accounts) | 232 | 198,280 | C$19.40bn | C$3.90bn | C$2.19bn | 65.3% |
| Same, account-error rows removed | 225 | 72,900 | C$19.40bn | C$3.90bn | C$2.19bn | 65.3% |
| 2025 release only, ≥10 accounts, clean | 203 | 69,324 | C$18.14bn | C$3.68bn | C$2.04bn | 69.9% |
| WellFunded page (Nov 2026) | 205 | 82,611 | C$18.6B | C$3.62B | C$2.18B | 68% |

- **Why the replicas differ from WellFunded** [I]: we cannot apply WellFunded's "active" filter (revoked status is not in these files), and its snapshot date differs.
- **Bracketing:** the two replicas bracket WellFunded's assets, grants out, top-10 share and sponsor count. They do not bracket its donations in: C$3.62bn is below both C$3.68bn and C$3.90bn. Nor do they bracket its 82,611 accounts, which are above both clean replicas (69,324 and 72,900) [V wave 37B]
- **Account counts:** WellFunded's 82,611 accounts are far below the 198,280 filed, so it must exclude or correct the transposition rows.
- **Repo's earlier check:** the N3 doc's "top five hold 44%" check (Blumberg list) matches our 2024 figure of 44.2%.

### 2.5 Top sponsors and concentration (2025 release; 2024 in brackets) [C]

| Rank | Sponsor (BN) | Type | Accounts | DAF assets | Payout same year | Payout on prior-year assets |
|---|---|---|---|---|---|---|
| 1 | Charitable Gift Funds Canada (896713500RR0001) | wealth/national | 3,739 | C$3,079.6m (2,434.7) | 8.7% | 11.0% |
| 2 | Jewish Community Fdn of Montreal (118974179RR0001) | faith CF | 2,445 | C$2,516.2m (2,114.1) | 9.4% | 11.2% |
| 3 | Private Giving Foundation (TD) (857210744RR0001) | bank | 2,244 | C$1,163.6m (972.3) | 15.5% | 18.6% |
| 4 | Winnipeg Foundation (119300960RR0001) | CF | 971 | C$1,094.0m (1,002.9) | 5.5% | 6.0% |
| 5 | BenefAction Foundation (804213759RR0001) | wealth | 1,742 | C$1,059.2m (792.0) | 8.8% | 11.7% |
| 6 | Aqueduct Foundation (Scotia) (866087034RR0001) | bank | 706 | C$910.7m (840.2) | 11.0% | 11.9% |
| 7 | Jewish Foundation of Greater Toronto (108155797RR0002) | faith CF | 1,516 | C$887.5m (719.2) | 7.0% | 8.7% |
| 8 | CHIMP (845528827RR0001) | online | 13,769 | C$712.8m (676.5) | 18.6% | 19.6% |
| 9 | Calgary Foundation (108074436RR0001) | CF | 685 | C$637.2m (570.8) | 7.2% | 8.0% |
| 10 | Strategic Charitable Giving Foundation (802678748RR0001) | wealth | 3,852 | C$613.2m (510.4) | 7.3% | 8.7% |

- **Type labels** are our shorthand, not a CRA field.
- **Not yet in the 2025 release:** Nicola Wealth Private Giving Foundation (C$364.5m in 2024), Edmonton Community Foundation (C$175.0m) and Ottawa Community Foundation (C$140.6m) have no 2025 return yet.

**Concentration [C].**

| Release | Top 1 | Top 3 | Top 5 | Top 10 | Top 20 | HHI |
|---|---|---|---|---|---|---|
| 2024 | 14.6% | 33.3% | 44.2% | 63.8% | 81.7% | 590 |
| 2025 | 16.6% | 36.3% | 47.9% | 68.1% | 83.6% | 680 |

**Payout on comparable definitions [C].**

| Definition | 2024 | 2025 | Comparable to |
|---|---|---|---|
| Aggregate 5864 ÷ 5862, same filing | 11.6% | 11.2% | Blumberg "12%", WellFunded "fund holder payout" |
| Median sponsor, same filing | 10.6% | 12.2% | WellFunded medians |
| Median sponsor with ≥ C$10m DAF assets | 8.4% | 7.3% | community-foundation spending policies |
| Aggregate 5864 ÷ prior-year 5862 (matched BNs) | 16.4% (n=336) | 13.3% (n=586) | US repo 22.8% (FY2024, DAF grants ÷ prior-year corrected assets, net of DAF-to-DAF) |
| 5864 ÷ 5863 | 58.6% | 54.9% | Blumberg "58%" |
| Share of sponsors with same-year payout ≥ 5% (blank 5864 excluded; 50.5% and 45.6% with blanks as zero) | 63.5% | 66.7% | — [V wave 37B] |

- **Canada vs the US** [I]: the Canadian disbursements line includes DAF-to-DAF and DAF-to-foundation transfers, which Blumberg–Pasha flag [F]. So the Canadian prior-year payout overstates net grants. Canada's ~13% against the US 22.8% is a conservative comparison: Canadian DAF payout is lower.
- **Not the disbursement quota:** none of these figures is the CRA disbursement quota. The DQ is a charity-level 3.5%/5% of average investment property, and a sponsor can meet it while individual accounts pay nothing [I; P-B39N3-06].

### 2.6 Panel continuity 2024 → 2025 [C]

- **Of 846 sponsors answering 5860 = Y in 2024:**
  - 618 (C$15.39bn) answered Y again in the 2025 release;
  - 56 (C$0.84bn) have no 2025 return yet;
  - 167 (C$0.44bn) answered **N** in 2025;
  - 5 left the question blank.
- **New in 2025:** 246 sponsors appear for the first time (C$0.21bn).
- **Interpretation** [I]: the Y/N churn is concentrated in small holders, which suggests that line 5860 is applied inconsistently to ordinary restricted funds.

---

## 3. Australia results

**Status timeline** (detail in the CSV):

| Date | Event | Status | Grade |
|---|---|---|---|
| 2024-12-05 | Government announces aligned, higher rates, smoothing and the rename to "giving funds" | announced | R (S23) |
| 2025-06-10 → 2025-08-01 | Treasury consultation c2025-667008 (paper: higher rate not to apply for 5 years after amendment) | consulted | R |
| 2026-02-26 | Decision: **6%** for public and private funds, **3-year smoothing**, existing funds have **2 years**, from "the first financial year following amendments to the giving fund guidelines" | decided | R (V24A-26) |
| 2026-09-15 | Act No. 86 of 2026 (C2026A00086) receives Royal Assent | enacted | P |
| **2026-10-01** | Schedule 7 commences: "ancillary" becomes "giving" in ITAA 1997 and TAA 1953. Item 17: existing PuAF guidelines "continue in force … as if they were public giving fund guidelines"; item 18 does the same for private funds | **commenced (rename only)** | P |
| 2026-11-19 | No amending instrument; F2022L00184 at compilation 0 (4%), F2019L01227 at compilation 2 of 2022 (5%); no exposure draft found | **6% not drafted or registered** | P (absence) |

- **Answer:** No. As of 2026-11-19, Australia has **not** amended the guidelines to 6% with smoothing.
  - The measure is at the "decided" stage. Only the rename has been legislated and has commenced.
  - The earliest start is the first financial year after an amending instrument is registered. Existing funds then have 2 more years before they must comply [F/I].
- **Commentary:**
  - Philanthropy Australia's undated explainer expects a further consultation and says the smoothing design "is not yet clear" [S].
  - A Lexology snippet on the rename is consistent with the Act (secondary, not fetched).
- **Sub-funds:**
  - The minimum applies to "the fund's net assets" (s15(1)).
  - Sub-funds appear only in s24(1) Note 2 and in s27(1)(a)(i), which allows a whole sub-fund's net assets to move to another ancillary fund with the Commissioner's agreement. Transfers must come after the year's s15 compliance and not involve assets received from another ancillary fund in the previous two years. Public money may not move to a private fund (s27(2)) [F].
  - ACF: "sub-fund holders are not required to make a minimum annual distribution"; the 4% is "calculated at the consolidated trust fund level" [F].
  - The 6% decision says nothing about sub-funds, as quoted in the repo [R]. A per-sub-fund floor would need new guideline text [I].
- **Statistics:**
  - **Public funds, 2022-23:** 1,445 PuAFs with net assets of A$4.7bn, distributions of A$487m (11.51% “of net assets” per Philanthropy Australia; the implied opening base of about A$4.23bn is our back-calculation [C], not a published figure) [V wave 37B] and donations of A$1.93bn.
  - **Private funds, 2022-23:** 2,196 PAFs with net assets of A$10,656.86m and distributions of A$799.34m (8.06%).
  - Both are from Philanthropy Australia (2025-07-11), citing ATO Taxation statistics 2022-23 [S].
  - The ATO's 2023-24 edition (published 2026-06-17) has a Table 4 on ancillary funds for 2000-01 to 2023-24, but it was not readable under robots rules (ato.gov.au 403; data.gov.au disallows all) [PS].
  - **Sub-fund counts:** no national figure found. Provider figures only, e.g. APS Foundation 725 giving funds and A$435m (FY2025) [R].

---

## 4. Limits

- **Canada.**
  - Line 5861 is unreliable; use the `accounts_clean` subset. The error flags are rule-based, so small mis-entries that look plausible are not caught.
  - Amounts are "as filed". CRA processing errors are possible, and Blumberg–Pasha note that CRA sometimes keys data incorrectly [F].
  - The 2025 release is incomplete (late filers). The 2023 release covers only v27 forms.
  - Fiscal year-ends vary (January to December), so "year" means FPE year, not calendar activity.
  - DAF-to-DAF flows are not netted (P-B39N3-04).
  - The charity "active" status is not in the files used. Revoked charities may remain in the panel.
  - The T3010 guide on canada.ca was not reachable. The C18 definition is quoted via Blumberg–Pasha.
- **Australia.**
  - "Not found" for the amendment and exposure draft is as at 2026-11-19. The Treasury consultation hub (JavaScript) and treasury.gov.au pages (robots) were not read in this pass.
  - The 2026-02-26 decision text relies on the repo's validated record (V24A-26), not a fresh fetch.
  - The ATO statistics are second-hand (Philanthropy Australia).
- **Recency:** all sources are 2021 or later. The 2019 private-fund guidelines are cited because they are still in force.

---

## 5. Data dictionaries

### 5.1 `canada-daf-panel-2026-11-19.csv` (one row per BN × release year with 5860 = Y; amounts in C$ as filed)

| Column | Meaning |
|---|---|
| dataset_year | CRA "List of charities" release year = FPE calendar year (2023 partial: v27 forms only) |
| bn | CRA business number (charity registration) |
| fpe | Fiscal period end of the return used |
| form_id | T3010 form version id (27 = T3010 E (24)) |
| legal_name, account_name | From the Identification file of the same release |
| designation, designation_label | A public foundation, B private foundation, C charitable organization |
| category_code | CRA charity category code |
| province | Province of the charity's address |
| line_5860 | Held a DAF during the period (always Y here) |
| accounts_5861 | Line 5861 number of DAF accounts at period end (as filed; see flags) |
| daf_assets_5862 | Line 5862 value of all DAF accounts at period end |
| daf_donations_5863 | Line 5863 donations to DAF accounts in the period |
| daf_disbursements_5864 | Line 5864 qualifying disbursements from DAFs in the period |
| total_assets_4200 | Line 4200 total assets of the charity (Section D/Schedule 6, same FPE) |
| total_revenue_4700 | Line 4700 total revenue |
| n_returns_in_year | Returns with an FPE in that year (latest kept) |
| avg_account | 5862 ÷ 5861 |
| payout_same_year | 5864 ÷ 5862 (same filing; WellFunded/Blumberg definition) |
| prior_fpe, prior_daf_assets_5862 | Same BN's previous-release FPE and 5862 (blank if not a 5860 = Y filer then) |
| payout_on_prior_assets | 5864 ÷ prior-release 5862 (US-comparable denominator; gross of DAF-to-DAF) |
| disbursements_to_donations | 5864 ÷ 5863 |
| daf_share_of_total_assets | 5862 ÷ 4200 |
| accounts_ge_10 | yes if 5861 ≥ 10 (WellFunded inclusion rule) |
| rank_assets_in_year | Rank by 5862 within the release |
| flags | Semicolon list; see §1.2 |
| accounts_clean | no if any of ACC_EQ_DOLLAR, ACC_GT_ASSETS, AVG_LT_100, ACC_NO_DOLLARS_LARGE |

### 5.2 `australia-ancillary-fund-rules-2026-11-19.csv`

| Column | Meaning |
|---|---|
| row_id | AU01–AU15 |
| item | Rule, event or statistic |
| fund_type | public giving fund (PuAF), private giving fund (PAF), or both |
| value_or_rule | The rule or figure |
| status | in force / announced / decided / consultation closed / enacted and commenced / not registered / published / not found |
| status_date | Date of that status (ISO) |
| instrument_or_doc | Instrument (with register id) or document |
| evidence_quote_or_basis | Verbatim quote or how the finding was established |
| source_url | Primary URL where possible |
| evidence_grade | P, PS, S, R (see top) |
| retrieved | Date read (2026-11-15 = repo validation; 2026-11-19 = this pass) |
| notes | Caveats, blocks |

---

## 6. Source register

| ID | Source | URL | Grade | Read |
|---|---|---|---|---|
| S01 | Blumberg & Pasha, *Blumbergs DAF Report: Donor Advised Fund accounts in 2024* (2026-02-10) | https://carleton.ca/profbrouard/wp-content/uploads/sites/281/2026/10/reportBlumbergPasha2026DAFReportDonorAdvisedFundaccounts2024Final.pdf | P | 2026-11-19 |
| S02 | CRA, 2023 / 2024 / 2025 List of charities (open data) and data dictionary v2.0 | https://open.canada.ca/data/en/dataset/05b3abd0-e70f-4b3b-a9c5-acc436bd15b6 ; https://open.canada.ca/data/en/dataset/80c00cdb-1358-415c-bb8b-0de7f12675b8 ; https://open.canada.ca/data/en/dataset/4b60228a-2b78-45d3-8e05-f7150b8fe8d8 | P | 2026-11-19 |
| S03 | Future of Good, "New database maps Canada's $17.3 billion DAF landscape…" (2026-08-10) | https://futureofgood.co/new-database-maps-canadas-17-3-billion-daf-landscape-and-where-philanthropic-wealth-is-concentrated/ | S | 2026-11-19 |
| S04 | WellFunded, Canadian DAF Data (methodology and totals) | https://www.wellfunded.io/daf-data?rank=receipted | P (vendor) | 2026-11-19 |
| S05 | Taxation Administration (Public Ancillary Fund) Guidelines 2022, F2022L00184 | https://www.legislation.gov.au/F2022L00184/latest/text | P | 2026-11-19 |
| S06 | Taxation Administration (Private Ancillary Fund) Guidelines 2019, F2019L01227 | https://www.legislation.gov.au/F2019L01227/latest/text | P | 2026-11-19 |
| S07 | Treasury Laws Amendment (Strengthening Accountability for Tax Adviser Misconduct and Other Measures) Act 2026, C2026A00086, Sch 7 | https://www.legislation.gov.au/C2026A00086/asmade/text | P | 2026-11-19 |
| S08 | legislation.gov.au API (titles/versions queries) | https://api.prod.legislation.gov.au/v1/titles ; https://api.prod.legislation.gov.au/v1/versions | P | 2026-11-19 |
| S09 | Assistant Minister Leigh, "Boosting support for Australian charities" (2026-02-26) | https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/boosting-support-australian-charities | R (V24A-26) | 2026-11-15 |
| S10 | Treasury, Giving fund reform consultation paper (June 2025) | https://storage.googleapis.com/files-au-treasury/treasury/p/prj35cf5f03f7cd51c704285/page/c2025_667008_cp.pdf | R | 2026-11-15 |
| S11 | Philanthropy Australia, Explainer: changes to the minimum distribution for Giving Funds | https://www.philanthropy.org.au/explainer-changes-to-the-minimum-distribution-for-giving-funds/ | S | 2026-11-19 |
| S12 | Philanthropy Australia, "What do the taxation statistics of giving reveal?" (2025-07-11) | https://www.philanthropy.org.au/news-and-stories/what-do-the-taxation-statistics-of-giving-reveal/ | S | 2026-11-19 |
| S13 | Australian Communities Foundation, FAQs | https://communityfoundation.org.au/giving/faqs | P | 2026-11-19 |
| S14 | ATO, Charity statistics for Taxation statistics 2023-24 (Table 4) | https://www.ato.gov.au/about-ato/research-and-statistics/in-detail/taxation-statistics/taxation-statistics-2023-24/statistics-in-taxation-statistics-2023-24/charity-statistics-for-taxation-statistics-2023-24 | PS (blocked) | 2026-11-19 |
| S15 | APS, Giving and growth snapshot 2025 | https://www.australianphilanthropicservices.com.au/giving-and-growth-snapshot-2025/ | R | 2026-11-15 |
| S16 | Lexology, "What's in a name? Ancillary funds become giving funds" | https://www.lexology.com/library/detail.aspx?g=dc37cae9-a94f-4227-a92e-69fd95020364 | S (snippet; robots 403) | 2026-11-19 |
