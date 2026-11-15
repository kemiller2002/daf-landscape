# Queue batch 36 A: account metric on an "ongoing advisory privilege" basis, carry-forward variant for blank Schedule D returns, and dated panels of grant-rail shares and latency statements

**Date:** 2026-11-15 · **Agent:** batch36 A · **Queue items:** P-B35A-01, P-B33A-02, P-B35C-03, P-PAY-05 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs**
- [`data/mission-2026-11-14/dafrc-market-accounts-restated.csv`](../../data/mission-2026-11-14/dafrc-market-accounts-restated.csv): 696 rows. 112 market totals (7 variants × FY2021–24 × 4 metrics) and 584 sponsor-year adjustments that make each variant auditable (P-B35A-01, P-B33A-02).
- [`data/mission-2026-11-14/grant-rail-shares-panel-2026.csv`](../../data/mission-2026-11-14/grant-rail-shares-panel-2026.csv): 20 dated electronic-vs-check observations, 2021 baseline to 2026 (P-B35C-03).
- [`data/mission-2026-11-14/grant-latency-statements-2026.csv`](../../data/mission-2026-11-14/grant-latency-statements-2026.csv): 28 published turnaround statements by sponsor, rail and clock (P-PAY-05).
- [`data/mission-2026-11-14/queue-proposals-batch36a.csv`](../../data/mission-2026-11-14/queue-proposals-batch36a.csv): P-B36A-01 to P-B36A-03.
- **Script** (stdlib, functional style): [`scripts/mission_account_metric.py`](../../scripts/mission_account_metric.py), with tasks `accounts` and `rails`. It reuses the `mission_990_contractors` helpers. The rebuilt corrected totals match `dafrc-corrected-market-totals.csv` exactly (maximum absolute difference 0) for accounts, assets and grants in all four years [C].

**Conventions**
- FY = calendar year in which the tax period ends (DAFRC convention). **Recency:** FY2021–24 for the market variants, and 2021 onward for the rail statements. The only pre-2021 values used are last-filed values that bracket a blank, as in batch 33.
- **Labels:** **[F]** filed or published value; **[C]** script computation; **[I]** inference; **[S]** secondary or search-index text; **[U]** not found.
- **Governing corrections read first:**
  - wave 20, at the end of [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md) (the support-count wording; it does not touch §2 used here) and of [queue-batch35-agents-analysts-rails.md](queue-batch35-agents-analysts-rails.md) (wrapper and Every.org wording; it does not touch the Chariot 94.57% figure);
  - wave 19, at the end of [queue-batch34-pass-through-channels.md](queue-batch34-pass-through-channels.md). Item 2 applies: PPGF's and NFG's filed FY2024 values already replace DAFRC's imputations under R1, so nothing here re-adjusts them;
  - wave 18, at the end of [queue-batch33-panel-scans.md](queue-batch33-panel-scans.md). Item 1 applies: imputed totals are stocks, so they are not summed across years here.
  - [queue-batch34-netting-filings.md](queue-batch34-netting-filings.md) has no corrections section. Its R5 netting acts on grants and contributions, not on accounts or EOY value, so it does not interact with the variants below.
- **Access.** robots.txt was read on every host before fetching. One site disallows Anthropic agents (fa-mag.com) and was not fetched. reninc.com allows the Anthropic-AI group only `/faqs/`, so its payments page was left alone. paypal.com policy pages returned 403 and were not retried. An Azure blob host (Truman Heartland's annual reports) failed at the session proxy (502). No logins, forms or contact.
- **This is research, not legal or tax advice.**

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B35A-01** account metric | **Definition:** count an account only when its donor or adviser holds *ongoing* advisory privileges (IRC 4966(d)(2)(A)(iii)). An account is excluded only on the sponsor's own filed statement. That makes the central rule exactly AOGF's FYE 2026 reclassification logic. No other sponsor's filing says its donors lack ongoing privileges [F].<br>**Central restatement (A1) [C]:** FY2021 1,122,971 · FY2022 2,495,659 · FY2023 2,352,992 · FY2024 **2,589,633** accounts. That is −40.5%, −23.4%, −22.4% and −21.8% against corrected totals. Grants fall only 1.2–1.3% ($0.62–0.78bn a year), and EOY value falls by under 0.03%.<br>**Upper exclusion (A2)**, which also drops all Givinga and PPGF accounts: 597,569 · 677,404 · 731,659 · **787,978**. On that basis the account count grows **9.7% a year (FY2021–24)**, against 20.6% on corrected totals and 32.1% on A1. Givinga's count moves from 42k to 1.5m between FY2021 and FY2022.<br>**Average EOY balance per account, FY2024:** $97,680 corrected; **$124,808** on A1; $410,174 on A2.<br>**TY2025 re-read:** index_2026 is still Last-Modified 2026-10-21. **No CY2025 return for PPGF, Givinga, NFG or Bright Funds is indexed** [F]. BBGF CY2025 is indexed, but its Schedule D count is blank and it reports no column move. Its Part III says CSRconnect employee gifts "should not be treated" as DAF contributions [F]. | High on filed values and arithmetic. The A1 back-cast to FY2021–23 is a scenario [I] |
| **P-B33A-02** blank-return variant | **Carry-forward (B1), FY2021–24 [C]:**<br>- "Closed" sponsors that still answer line 6 Yes add $41.3m, $78.4m, $171.8m and $151.1m of EOY value (6, 15, 27 and 26 sponsors) and 272, 748, 1,604 and 1,508 accounts.<br>- Replacing DAFRC imputations with the last filed value changes EOY value by −$58.6m, −$103.7m, −$2.2m and −$27.4m.<br>- **Net B1 effect on market assets:** −$17.3m, −$25.3m, **+$169.6m** and **+$123.8m** (at most 0.07%). Accounts change by +312, +776, +1,525 and +1,461.<br>**Interpolated (B2):** +$41.3m, +$75.7m, +$170.6m and +$125.1m.<br>**DAFRC's imputation for CF of Middle Tennessee FY2021–22 is a straight-line interpolation between its FY2019 and FY2023 filed values.** B2 reproduces it to the dollar ($333,251,148 and $364,652,428). The negative B1 deltas in FY2021–22 come from carrying CFMT's FY2019 value forward [C].<br>Audited statements were **not** obtained (§2.4), so every replacement is a proxy. | High on mechanics. Values are proxies [I] |
| **P-B35C-03** rail-share panel | **Only one sponsor publishes a first-party, dated share series: Fidelity Charitable**, by grant count [F]:<br>- **>50%** EFT (2023 Giving Report);<br>- **~54%** (2024 report);<br>- **>58%** (2025 report);<br>- **67%** (2026 report, 3m grants in 2025).<br>Fidelity's own EFT counts disagree with its shares in two reports: "950,000" at 54% of 2.3m (implied 1.24m), and "more than 750,000" at 58% of 2.7m (implied 1.57m) [C].<br>**Other sponsors:**<br>- **Vanguard** publishes PayPal dollar milestones only: $130m (May–Sep 2023), $460m (to Jan 2024), and "$1 billion" in FY2024 against FY2024 grants of more than $3bn (**at most about one third of dollars** [C/I]). In the three weeks after the 2023 Maui fires, 57% of $3.7m went electronically [F].<br>- **NPT** publishes only a 2021 baseline ("almost entirely by check", $6.4bn) and a one-third grantee eligibility figure at the 2022 launch [F].<br>- Every other share is a Chariot case study or recap: DJCF 0% (2022) → ~35% → **92% (Mar 2026)**; Founders Pledge **97%** of dollars in its first 4 months → **~98%** (Jul 2026); TIFIN Give **82%** of dollars in its first 4 months; Chariot pooled **94.57%** since launch [F, vendor]. | High that the quotes are as published. Low comparability: count, dollar and unstated bases are mixed |
| **P-PAY-05** latency | **No sponsor publishes an SLA or a latency distribution by rail.**<br>The 28 statements are mostly policy ranges on different clocks. Only **5 are measured**, all vendor figures with undisclosed or single-recipient samples:<br>- Charityvest: **"95% of checks are deposited … within 35 days of when they are sent"**. Re-verified live on 2026-11-15; the guide still predates Chariot.<br>- AssetMark Charitable: **median 2 days overall, 0 days electronic**, submission to funds. Re-verified; "updated this week"; no sample stated.<br>- Chariot's one-nonprofit sample: ACH 1–2 days on average for the three fastest providers; **7–162 days** average for 18 check-paying providers.<br>New statements found: TIFIN "T+4" (recommendation to funds); DJCF "within an hour" electronic, against checks 10–15 days after the weekly run and 60–90 days uncleared; Greater Houston CF ACH 1–2 business days against a check "a week or more". | High on quotes. A cross-sponsor P50/P90 dataset cannot be built from public sources [U] |

---

## 1. P-B35A-01: the account metric

### 1.1 Definition and rules
- **Basis.** An account counts when, at year end, a donor or a person the donor appoints has, or reasonably expects, **ongoing** advisory privileges over its distributions or investments. This is the IRC 4966(d)(2)(A)(iii) element read as a continuing right.
  - It excludes contributions where the donor names a charity at or near the time of giving and has no continuing say. Workplace micro-donations and checkout donations are the main case.
  - It does not judge whether the sponsor *legally* holds DAFs. It restates a count; the dollars move only where the sponsor's own filing moves them.
- **Evidence standard.** An account is excluded only on the sponsor's own filed statement (Part III, VI or Schedule O narrative together with a Schedule D column change). Structural or size signals are kept to sensitivity variants.
- **Rules** (script docstring; parameters in code):

| Rule | Scope | What changes | Basis |
|---|---|---|---|
| **A1 (central)** | AOGF, FY2021–24 | Accounts → 695 (its FYE 2026 DAF-column count, used as a constant proxy). Grants × 0.5977 and EOY value × 0.7674 (FYE 2026 DAF-column shares of DAF + other-funds grants and EOY value) | AOGF FYE 2026-03 Schedule O: corporate donors "provide ongoing advice"; individual donors "make micro-donations and recommend grants … at or near the time of donation, **without ongoing advisory privileges**" [F] |
| **A2 (upper)** | A1, plus Givinga and PPGF | Accounts → 0; grants and EOY value unchanged | The two named micro-account processors. Their own filings do **not** disclaim ongoing privileges (§1.2), so this is an exclusion bound, not a finding |
| **A3 (sensitivity)** | A1, plus any sponsor-year with ≥5,000 accounts and average EOY DAF value < $500 | Accounts → 0 | Size screen. Hits: Givinga (all years), PPGF (all years), Give Back Foundation FY2022–23, Pledgeling FY2022–24, Philanthropi FY2023–24, Matbia Charities FY2024 (8,576) [C] |
| B1, B2, C1 | §2 | | |

### 1.2 Filed evidence for the processors [F]

| Sponsor (return) | Schedule D DAF column | Other-funds column | Account-basis wording in the return |
|---|---|---|---|
| AOGF FYE 2026-03 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml)) | 695 accounts; grants $1,390.0m; EOY $205.7m | 751,746; $935.7m; $62.3m | "only with respect to its donor-advised funds, a sponsoring organization … without ongoing advisory privileges"; the workplace model includes "fund structures that are not conventional DAF models" |
| AOGF FYE 2025-03 amended ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml)) | 710,352; $2,124.1m; $160.3m | 1; $1.6m; $0 | Already says the workplace model includes "fund structures that are not conventional DAF models", but keeps them in the DAF column |
| PPGF CY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml)) | 380,644; $795.7m; $97.0m | blank | No advisory-privilege wording. Part III: makes it easy for donors to support charities "on the websites and apps they use every day" |
| Givinga CY2024 amended ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml)) | 1,421,011; $12.4m; $1.9m | blank | Describes "individual account holders" of DAFs. The amendment changes only "SCHEDULE D PART I" |
| Give Back Foundation CY2025 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202631669349300818_public.xml)) | 7,969; $43.6m; $12.0m | 1 | "Each member has the ability to direct the funds from their account" (ongoing) |
| Blackbaud Giving Fund CY2025 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml)) | count blank; $536.4m; $65.5m | blank | "employee donations made through CSRconnect should not be treated by BBGF as contributions to donor advised funds" |
| Network for Good CY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml)) | 1; $199.8m; $50.4m | 0 | Single pooled fund; no change needed |
| Philanthropi CY2024 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523219349326042_public.xml)) | 5,674; $0.22m; $0.48m | 19 | "Impact accounts that serve as donor advised account funds" |

- **PPGF policy text [S]:** search-index snippets of PayPal Giving Fund's US donor account policy say donors may recommend a charity "at donation or afterward" from an account balance, subject to a minimum annual distribution. That reads as ongoing privileges, which is why PPGF is not excluded in A1. The policy pages returned 403 to direct fetches, so the text is unverified (P-B36A-01).
- **TY2025 index check [F]:** index_2026.csv was re-downloaded on 2026-11-15 (Last-Modified still 2026-10-21; 472,357 rows). Filed returns and missing ones:
  - **Filed:** AOGF FYE 2025-03 and 2026-03, BBGF CY2025, Give Back CY2025 and FrontStream FYE 2025-06.
  - **Not filed:** PPGF, Givinga and NFG (EIN match), and "BRIGHT FUNDS" (name match). Bright Funds' EIN is not in the repo.

### 1.3 Results [C]

| FY | Corrected accounts | **A1 central** | A2 upper exclusion | A3 size screen | A1 grants (Δ) | Average EOY per account: corrected / A1 / A2 |
|---|---|---|---|---|---|---|
| 2021 | 1,888,462 | **1,122,971** (−40.5%) | 597,569 | 597,569 | $47.41bn (−$0.62bn, −1.3%) | $123,917 / $208,373 / $391,582 |
| 2022 | 3,258,113 | **2,495,659** (−23.4%) | 677,404 | 624,187 | $54.94bn (−$0.67bn, −1.2%) | $70,023 / $91,394 / $336,708 |
| 2023 | 3,030,383 | **2,352,992** (−22.4%) | 731,659 | 668,798 | $54.14bn (−$0.69bn, −1.3%) | $84,599 / $108,934 / $350,327 |
| 2024 | 3,309,483 | **2,589,633** (−21.8%) | 787,978 | 750,473 | $65.66bn (−$0.78bn, −1.2%) | $97,680 / $124,808 / $410,174 |

- **Reading [I]:**
  - The account metric is not one number. Even on the strict filed basis, A1 still contains 1.80m Givinga and PPGF accounts (69.6% of A1 in FY2024), and those accounts hold 0.03% of market DAF assets.
  - Account growth is a reporting artefact on any basis that keeps Givinga, whose count rose 36-fold from FY2021 to FY2022.
  - For per-account averages and account growth, the repo should cite **A2 as "accounts excluding micro-account processors"** next to A1, and never the corrected total alone.
  - Grants and assets are robust: A1 moves grants by about 1.2% and assets by under 0.03%.
- A2 keeps AOGF's 695 corporate DAFs, so it is 695 above batch 35's "787,283 excluding all three".

## 2. P-B33A-02: carry-forward replacement of "closed" flags and imputations

### 2.1 Method
- **Input:** the 156 FY2021–24 rows of `blank-schedule-d-panel.csv` whose DAFRC treatment is `dafrc_no_row_sponsor_closed`, `dafrc_row_imputed` or `dafrc_row_value_blank`. Every one answers Part IV line 6 "Yes" with the Schedule D Part I DAF count and value blank (batch 33 §1).
- **B1 (carry-forward):**
  - "Closed" or blank rows get the sponsor's last filed DAF EOY value and count added.
  - Imputed rows have DAFRC's imputed values replaced with the last filed ones.
  - **Last filed value:** the 990 extract's `prior_reported_*`. Where that is missing (most "closed" sponsors), it falls back to DAFRC's last filed (non-imputed) row before the blank year: `dafrc_last_filed_daf_assets_before` for value, and the panel's filed count for accounts.
- **B2 (interpolated):** linear interpolation by fiscal year between the last and next filed values where a next filed value exists; otherwise the same as B1.
- **Guard:** a sponsor-year whose corrected value already comes from an applied R1–R4 row is left alone. This skips the two FY2023 and one FY2024 R4 "closed but filed" cases, which is why 27 rather than 29 closed sponsors are added in FY2023.
- **Grants and contributions are not touched.** They are flows and cannot be carried forward.

### 2.2 Results [C]

| FY | Closed rows added (sponsors): EOY value, accounts | Imputed rows replaced: Δ EOY value, Δ accounts | **B1 net Δ assets** (share) | B2 net Δ assets | B1 Δ accounts |
|---|---|---|---|---|---|
| 2021 | 6: +$41.3m, +272 | 10: −$58.6m, +40 | **−$17.3m** (−0.007%) | +$41.3m | +312 |
| 2022 | 15: +$78.4m, +748 | 14: −$103.7m, +28 | **−$25.3m** (−0.011%) | +$75.7m | +776 |
| 2023 | 27: +$171.8m, +1,604 | 8: −$2.2m, −79 | **+$169.6m** (+0.066%) | +$170.6m | +1,525 |
| 2024 | 26: +$151.1m, +1,508 | 31: −$27.4m, −47 | **+$123.8m** (+0.038%) | +$125.1m | +1,461 |

- The closed-sponsor additions reproduce batch 33's carry-forward to the dollar ($41.3m, $78.4m, $171.8m and $151.1m) [C].
- **Largest single adjustments (B1, EOY value):**
  - CF of Middle Tennessee FY2022 −$94.2m and FY2021 −$62.8m (imputed $364.7m and $333.3m replaced by FY2019's $270.4m);
  - Truman Heartland FY2023–24 +$19.0m each;
  - CF of Snohomish County FY2021–23 +$18.4m each;
  - Jewish CF (47-0874376) FY2021–24 +$16.6m each;
  - an FY2022 replacement of −$16.7m at EIN 46-1566557.
- **DAFRC imputes by interpolation.** For CFMT, B2's straight line between FY2019 ($270,448,587) and FY2023 ($396,053,709) equals DAFRC's imputed values exactly. So B2 is the more faithful variant wherever a later filed value exists, and B1 understates growing sponsors [C/I].
- **Combined C1 (A1 + B1), FY2024:** 2,591,094 accounts, $323.33bn EOY value and $65.66bn grants.

### 2.3 Reading [I]
- Replacing "closed" flags matters for **mortality and exit statistics**: batch 33 found 10–11 tier-C exits that now look like reporting gaps. It does not matter for market size: at most 0.07% of assets and 0.05% of accounts in any year.
- The sign depends on the variant: B1 is negative in FY2021–22 and B2 positive. Without audits, the honest range for FY2021–22 is "−$25m to +$76m".

### 2.4 Audited statements (the queue's preferred source): not obtained
- Truman Heartland's annual reports (2023, 2024) sit on `stdidthcfprod.blob.core.windows.net`, and the session proxy refused the CONNECT (502).
- State charity registries need form searches, and ProPublica PDF images return a security check (batch 34 §3). Neither was attempted.
- So the queue's ask, turning proxies into measured balances, remains open (P-B36A-03).

## 3. P-B35C-03: dated panel of electronic-vs-check shares

### 3.1 Method
- Each row is a published statement transcribed verbatim, with its URL, as-of date, period covered, basis (grant count, dollars, or unstated) and source class:
  - `sponsor_report`, `sponsor_press_release`, `sponsor_article`: first party;
  - `vendor_case_study`, `vendor_webinar_recap`, `vendor_report`, `vendor_partner_post`, `vendor_secondary`;
  - `trade_press_reprint`, `vendor_press_release`.
- The script derives the implied check-or-other share (1 − electronic) and, for Fidelity, the implied EFT grant count (share × the report's total grants). It adds no other figures.
- **Fidelity Giving Reports 2023–2026** were downloaded as PDFs, converted with `pdftotext` and grepped. The PDF dates come from `pdfinfo`.

### 3.2 Panel (abridged; full rows in the CSV)

| Sponsor | As of | Electronic share | Basis | Source class |
|---|---|---|---|---|
| Fidelity Charitable | 2023 report (covers CY2022) | **> 50%** | count | first party ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf)) |
| Fidelity Charitable | 2024 report (created 2024-03-06) | **~54%** | count | first party ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf)) |
| Fidelity Charitable | 2025 report (created 2025-02-19) | **> 58%** | count | first party ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf)) |
| Fidelity Charitable | 2026 report (created 2026-04-21) | **67%** | count | first party ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf)) |
| Vanguard Charitable | 2023-09-20 | 57% of $3.7m (three weeks after the Maui fires) | dollars | first party ([PR](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html)) |
| Vanguard Charitable | 2023-09-20 / 2024-01-30 / 2024-09-06 | volumes only: $130m (2023-05-03 to 09-15), $460m (to Jan 2024), "$1 billion" in FY2024 | dollars | first party ([PR 2024](https://prnewswire.com/news-releases/vanguard-charitable-donors-granted-more-than-2-6-billion-to-charity-in-2023--302047196.html)); reprint ([NonProfit Pro](https://www.nonprofitpro.com/article/vanguard-charitable-donors-gave-more-than-3b-in-fiscal-year-2024/)) |
| NPT | 2022-08-25 | 2021 baseline "almost entirely by check" ($6.4bn); one third of grantees eligible at launch | dollars / grantees | PayPal release ([newsroom](https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers)); NPT ([article](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/)) |
| DJCF | 2022 / undated / Mar 2026 | 0% → ~35% → **92%** | unstated | vendor case study ([Chariot](https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office)) |
| Founders Pledge | first 4 months after Nov 2025 / 2026-07-15 | **97%** (dollars) / ~98% (count) | mixed | vendor case study ([Chariot](https://givechariot.com/resources/customer-stories/how-founders-pledge-doubled-its-grantmaking-volume--without-doubling-its-operational-risk)); webinar recap ([Chariot](https://givechariot.com/resources/webinars/-powering-modern-daf-grants)) |
| TIFIN Give | first 4 months (page images June 2026) | **82%** of $34.1m; 5,175 grants | dollars | vendor case study ([Chariot](https://givechariot.com/resources/customer-stories/tifin-give-moves-80-of-grant-volume-electronically-with-chariot-disbursements)) |
| Chariot, pooled | since launch, to 2026-11-15 | **94.57%** | count | vendor ([page](https://givechariot.com/disbursements.md)) |
| "Largest national DAFs" (unnamed) | 2026-01-20 | "struggled to get their ACH rates much higher than 50%" | count | vendor report ([Chariot](https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits)) |

### 3.3 Reading
- **Fidelity is the only first-party trend:** >50% → ~54% → >58% → 67%, about 4–9 points a year [F]. Even at 67% about 1m grants a year still go by check. That matches Chariot's "about 1 million by check" [C/S].
- **Fidelity's EFT counts do not reconcile with its shares.**
  - 2024 report: "950,000 grants" against 54% × 2.3m = 1.24m.
  - 2025 report: "more than 750,000" against 58% × 2.7m = 1.57m.
  - The counts may cover a partial period or a subset; the reports do not say [C/I] (P-B36A-02).
- **No sponsor confirms the July 2026 EFT-only date on its own pages** (unchanged from the repo's 2026-11-14 finding). The 2026 Giving Report states the 67% share but no date [F].
- **High electronic shares (92–98%) come only from Chariot customers,** measured over short windows and on mixed bases. They show what a claim-or-check rail can reach for a sponsor with few grantees. They do not show where the national sponsors stand [I].
- **Vanguard** has never published a share. "$1bn" against more than $3bn of FY2024 grants caps PayPal at about one third of FY2024 dollars, and less if the $1bn milestone is cumulative from May 2023 [C/I].

## 4. P-PAY-05: recommendation-to-deposit latency statements

### 4.1 Method
- Each statement is recorded with its **clock**: start (recommendation, approval, grant sent, charity accepts) and end (processed, mailed, delivered, deposited, cleared).
- It also gets a statistic type (`stated_range`, `stated_typical`, `stated_maximum`, `median`, `P95`, `provider_average_range`, `claim_window`, …) and an evidence type (`policy`, `claim_unmeasured`, `measured_vendor_undisclosed_sample`, `measured_vendor_n1_recipient`, `vendor_case_study`, `vendor_webinar_recap`).
- Business days are converted to an approximate calendar maximum (× 7/5).
- Rows marked "repo capture" were fetched on 2026-11-14 by the payment-rails agent ([queue-payment-rails-cluster.md](queue-payment-rails-cluster.md) §3). Fidelity, Charityvest and AssetMark were re-fetched on 2026-11-15.

### 4.2 Results (by rail; full rows in the CSV)

| Rail | Statement range (end-to-end where stated) | Measured? |
|---|---|---|
| Sponsor processing (all rails) | Fidelity "10 or more business days"; NPT due diligence "5 business days or less"; Vanguard "within a few days"; Daffy review "up to one week"; AssetMark verification 1–3 business days | No |
| ACH / Stripe | Fidelity "1-2 days" after processing; Greater Houston CF "1–2 business days"; BlueGive "within 3 business days" of approval; Chariot sample: the three fastest providers average 1–2 days from approval | Chariot sample only (n = 1 recipient) |
| PayPal Grant Payments | Vanguard "within one day" of acceptance, "minutes to hours"; NPT 14-day acceptance window, then a check | No |
| Chariot Deposit Account | AssetMark median **0 days** electronic and 2 days overall; DJCF "within an hour" of approval; TIFIN "T+4" from recommendation; 5-business-day claim window, then a check | AssetMark (sample undisclosed) |
| Mailed check | DAFgiving360 mailed in 7–10 business days, plus 3–5 for USPS; Charityvest about 10 business days in the mail and **95% deposited within 35 days of sending**; DJCF (before Chariot) 10–15 days after the weekly run, sometimes 60–90 days uncleared; Chariot fallback "~2-3 week delays"; Chariot sample: check payers average **7–162 days** | Charityvest (P95; sample undisclosed); Chariot sample |
| PPGF monthly payout | 15–45 days after the donation | No |

### 4.3 Reading
- **The queue's dataset (P50/P90 by rail across sponsors) does not exist in public form.**
  - Only AssetMark publishes a median, and only Charityvest a tail percentile, and the two use different clocks.
  - Fidelity's "nine times faster" is unmeasured in public.
- **A floor-to-tail range can be stated [I]:**
  - Electronic rails deliver in 0–2 days after approval once the charity is enrolled. Sponsor processing (up to 10+ business days at Fidelity) then dominates the end-to-end time.
  - Checks add 1–3 weeks to delivery and have a deposit tail to about 5 weeks at P95 (Charityvest). Chariot's one-recipient averages reach 162 days.
- Verifying the vendor medians would need recipient bank data from several nonprofits, which public sources do not offer.

## 5. Limitations
- **A1 back-cast.** AOGF's FYE 2026 basis (695 DAF-column accounts; grant and value shares) is applied to FY2021–24 as a scenario. AOGF's earlier corporate-DAF counts are not filed.
- **PPGF's donor policy** was seen only through search-index text (403 on direct fetch). If its accounts are in fact recommend-at-donation pass-throughs, the central count falls by a further 0.38m in FY2024 (towards A2).
- **The TY2025 re-read is incomplete:** the IRS index has not changed since 2026-10-21.
- **Thresholds.** The A3 thresholds (≥5,000 accounts, < $500 average) are judgement.
- **P-B33A-02.** Values are carry-forward or interpolation proxies with no audits. Accounts for "closed" sponsors use DAFRC's last filed count, which can be pre-2021 (FY2019–20).
- **Rail shares** mix count, dollar and unstated bases, and periods range from three weeks to "since launch". 15 of 20 rows are vendor-published or secondary. Fidelity's 2023 report PDF carries 2024 metadata (likely re-saved), so its as-of date is the report year, not a month.
- **Latency.** Most rows are policy statements, not measurements. Repo captures from 2026-11-14 were not all re-fetched.
- **Sites not used for access reasons:** fa-mag.com (disallows Anthropic agents), reninc.com payments (robots allows the Anthropic-AI group only `/faqs/`), paypal.com policies (403), and the Truman Heartland blob host (proxy 502).

## 6. Source register

| ID | Source | Accessed | Used in |
|---|---|---|---|
| S1 | DAFRC 2025 updated dataset ([xlsx](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)) via `dafrc-sponsor-schedule-d-fy2019-2024.csv`; `dafrc-corrections-itemized.csv`; `dafrc-corrected-market-totals.csv`; `blank-schedule-d-panel.csv` | repo | §1–2 |
| S2 | IRS e-file XML via the GivingTuesday mirror (eight returns, §1.2 links) | 2026-11-15 | §1 |
| S3 | IRS [index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) (Last-Modified 2026-10-21) | 2026-11-15 | §1.2 |
| S4 | PayPal Giving Fund US donor account policy ([page](https://paypal.com/us/webapps/mpp/givingfund/policies/donor-account-policy)); 403, search-index text only [S] | 2026-11-15 | §1.2 |
| S5 | Fidelity Charitable Giving Reports [2023](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2023-giving-report.pdf), [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf), [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), [2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf); [grant-processing timeline](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html) | 2026-11-15 | §3–4 |
| S6 | Vanguard Charitable releases: [2023-09-20](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html), [2024-01-30](https://prnewswire.com/news-releases/vanguard-charitable-donors-granted-more-than-2-6-billion-to-charity-in-2023--302047196.html); FY2024 reprint ([NonProfit Pro, 2024-09-06](https://www.nonprofitpro.com/article/vanguard-charitable-donors-gave-more-than-3b-in-fiscal-year-2024/)); FY2025 ([MyChesCo, 2025-08-27](https://www.mychesco.com/a/news/business/vanguard-charitable-donors-grant-record-3-5-billion-in-fiscal-2025/): 248,000 grants, no rail data) | 2026-11-15 | §3–4 |
| S7 | PayPal Grant Payments launch ([PayPal newsroom, 2022-08-25](https://newsroom.paypal-corp.com/2022-08-25-PayPal-Launches-Grant-Payments,-Enabling-Charities-to-Quickly-Receive-Funds-from-Grantmakers)); [NPT article, 2022-08-25](https://www.nptrust.org/philanthropic-resources/philanthropist/grant-payments-with-paypal-gets-grants-to-nonprofits-faster-than-ever/) | 2026-11-15 | §3 |
| S8 | Chariot: [Disbursements](https://givechariot.com/disbursements.md); case studies for [DJCF](https://givechariot.com/resources/customer-stories/how-djcf-modernized-grant-payments--freed-its-team-from-the-back-office), [Founders Pledge](https://givechariot.com/resources/customer-stories/how-founders-pledge-doubled-its-grantmaking-volume--without-doubling-its-operational-risk) and [TIFIN Give](https://givechariot.com/resources/customer-stories/tifin-give-moves-80-of-grant-volume-electronically-with-chariot-disbursements); [webinar recap](https://givechariot.com/resources/webinars/-powering-modern-daf-grants); [All Checks, No Balance](https://givechariot.com/resources/insights/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits); [Daffy partner post](https://givechariot.com/resources/insights/getting-to-know-daffy-a-chariot-disbursements-partner); [Charityvest partner post](https://www.givechariot.com/resources/insights/getting-to-know-charityvest-a-new-chariot-disbursements-partner) | 2026-11-15 | §3–4 |
| S9 | [Charityvest grant status guide](https://guide.charityvest.org/for-donors/getting-started/check-grant-status.md); [AssetMark help](https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check); [Greater Houston CF](https://ghcf.org/articles/why-ach-grant-payments-benefit-nonprofits/) (2026-04-17) | 2026-11-15 | §4 |
| S10 | Repo captures of 2026-11-14: `sponsor-grant-payment-policies.csv`, `nonprofit-receipt-cost-by-rail.csv`, [queue-payment-rails-cluster.md](queue-payment-rails-cluster.md) (DAFgiving360, NPT, BlueGive, Daffy, Chariot help, PPGF help969) | repo | §4 |

## 7. Data dictionary

### `dafrc-market-accounts-restated.csv`

| Column | Meaning |
|---|---|
| row_type | `total` (market sum for a variant) or `adjustment` (one sponsor-year-metric change) |
| fiscal_year | FY2021–24 (DAFRC convention) |
| variant | `V0_corrected`, `A1_advisory_filed_basis` (central), `A2_named_processors_excluded`, `A3_small_balance_screen`, `B1_blank_carry_forward`, `B2_blank_interpolated`, `C1_advisory_plus_blank_cf` |
| rules | Rules applied (A1, A2, A3, B1, B2; `A1+B1` etc.) |
| metric | `daf_accounts_eoy`, `daf_assets_eoy` (EOY value), `daf_grants`, `avg_assets_per_account` (EOY value ÷ accounts, whole dollars) |
| ein, sponsor_name | Adjustment rows only |
| value | Variant value (total) or new sponsor-year value (adjustment); whole units |
| corrected_value | V0 value (total) or the corrected value before adjustment (0 when DAFRC had no row) |
| delta, delta_pct | value − corrected_value; ÷ corrected_value |
| sponsors_adjusted | Totals: number of sponsors with an adjustment in that FY and metric |
| variant_description | Plain-language rule |
| note | Adjustment basis: AOGF FYE 2026 shares; screen values; DAFRC treatment, blank kind, last and next filed period |
| sources | DAFRC dataset, repo correction files, AOGF FYE 2026 XML |

### `grant-rail-shares-panel-2026.csv`

| Column | Meaning |
|---|---|
| obs_id | S01… |
| sponsor, rail | Grantmaker and the rail contrast described |
| as_of, period_covered | Publication date (or document metadata) and the period the figure describes |
| electronic_share | Fraction as published (blank when only volumes are published) |
| share_qualifier | `exact`, `more than`, `over`, `nearly`, `roughly`, `approximately`, `about (ceiling)` |
| share_basis | `count`, `dollars`, `grantees`, `unstated` |
| check_or_other_share_implied | 1 − electronic_share [C] |
| implied_electronic_count | Share × the report's total grant count (Fidelity, count basis only) [C] |
| volume_note | Volumes and caveats published alongside |
| quote | Verbatim text (ellipses mark omissions) |
| source_class, first_party | Source type; `yes` only for the sponsor's own report, release or article |
| url, retrieved | Source and access date |

### `grant-latency-statements-2026.csv`

| Column | Meaning |
|---|---|
| obs_id | L01… |
| sponsor, rail | As above |
| clock_start, clock_end | Start and end events of the stated interval |
| stat_type | `stated_range`, `stated_typical`, `stated_average`, `stated_minimum`, `stated_maximum`, `stated_approx`, `median`, `P95`, `provider_average`, `provider_average_range`, `benchmark`, `claim_window`, `acceptance_window`, `ratio` |
| low_days, high_days, day_unit | As published; `business`, `calendar` or `unstated` |
| high_days_calendar_approx | Business days × 7/5 [C] |
| evidence_type | `policy`, `claim_unmeasured`, `measured_vendor_undisclosed_sample`, `measured_vendor_n1_recipient`, `vendor_case_study`, `vendor_webinar_recap` |
| as_of, quote, url, retrieved | As above; "repo capture" rows were retrieved 2026-11-14 |

### `queue-proposals-batch36a.csv`
- Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md).
- P-B36A-01: PPGF and Givinga account basis, and a TY2025 re-run.
- P-B36A-02: first-party rail shares, and Fidelity's count reconciliation.
- P-B36A-03: measured balances for the largest blank-return cases.

## 8. Reproduction
```
python3 scripts/mission_account_metric.py accounts --work-dir WORK --index IRS/index_2026.csv --fetch
python3 scripts/mission_account_metric.py rails
```
- WORK receives `xml/` (eight cached returns). The `accounts` task prints a JSON summary: the rebuild check, every variant total, the A3 hits, B1 counts and largest adjustments, the processor evidence (Schedule D columns and matched narrative) and the TY2025 index hits. Every figure in §0–2 comes from it or from the CSV.
- The Fidelity PDF quotes were extracted with `pdftotext`, and their dates with `pdfinfo`.

## Validation corrections (wave 21, 2026-11-15) — governing
Source: [validation-wave21-report.md](validation-wave21-report.md); register `data/mission-2026-11-14/validation-register-wave21.csv`.

1. **§2.3 (accounts bound).**
   - **Find:** "It does not matter for market size: at most 0.07% of assets and 0.05% of accounts in any year."
   - **Replace with:** "It does not matter for market size: at most 0.07% of assets in any year under B1 or B2, and 0.05% of accounts under B1. B2 adds up to 4,360 accounts (0.14%, FY2023) [V wave 21]."
2. **§3.3, Fidelity counts.**
   - **Find:** "  - The counts may cover a partial period or a subset; the reports do not say [C/I] (P-B36A-02)."
   - **Replace with:** "  - The counts may cover a partial period or a subset; the reports do not say [C/I] (P-B36A-02). The 2026 report's \"more than 2 million\" does reconcile with 67% × 3m = 2.01m [C; V wave 21]."
3. **§5, rail-share limits.**
   - **Find:** "15 of 20 rows are vendor-published or secondary."
   - **Replace with:** "12 of 20 rows are vendor-published or secondary; 8 are first-party [V wave 21]."
