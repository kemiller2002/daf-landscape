# Realised volumes of non-cash intake vendors, and where DAFpay Network belongs in market totals (P-B40N14-03, P-B38C-03)

**Date:** 2026-11-20. **Task ID:** b40n14-03-b38c-03.
**Queue items:** P-B40N14-03 (from [direction-noncash-gift-infrastructure.md](direction-noncash-gift-infrastructure.md) and `queue-proposals-batch40-n14.csv`); P-B38C-03 (DPN classification, following [b40n14-b38c-dechomai-dafpay.md](b40n14-b38c-dechomai-dafpay.md) and its wave-37B corrections in [validation-wave37b-report.md](validation-wave37b-report.md)).
**Outputs:**
- Data: [`noncash-vendor-volumes-2026-11-20.csv`](../../data/mission-2026-11-14/noncash-vendor-volumes-2026-11-20.csv) (1,687 rows, 15 columns)
- Script: [`scripts/mission_noncash_vendors.py`](../../scripts/mission_noncash_vendors.py) (stdlib, functional; two runs give a byte-identical CSV, md5 `b9e8f49b…`)
- Queue proposals: [`queue-proposals-b40n14-03-b38c-03.csv`](../../data/mission-2026-11-14/queue-proposals-b40n14-03-b38c-03.csv) (6 rows)

**Read first:** the repo files that mention FreeWill, DonateStock, Shift4 or The Giving Block (chiefly [direction-noncash-gift-infrastructure.md](direction-noncash-gift-infrastructure.md), `noncash-gift-vendors-2026.csv` NCG-01 to NCG-06, [queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md) §5 and [firms-interested-in-daf-organizations.md](firms-interested-in-daf-organizations.md) W4-9); the classification rules in [b40n13-03-g1913-03-schema-and-processor-accounts.md](b40n13-03-g1913-03-schema-and-processor-accounts.md) with the wave-40A corrections in [validation-wave40a-report.md](validation-wave40a-report.md); and the DAFRC technical-appendix selection rule as recorded in [g1915b-04-line6-vs-schedule-d.md](g1915b-04-line6-vs-schedule-d.md) §1 item 4.

**Labels:** [F] read from a filing or first-party page this pass. [C] computed by the script from [F] values. [R] carried from a repo file. [I] inference. [U] unresolved. [B] blocked.

---

## 0. Answers

### (A) P-B40N14-03: what the vendors' charities actually filed

| Vendor (charity) | Claim tested | Filed dollars, latest year | What the filing supports |
|---|---|---|---|
| **FreeWill / Crypto for Charity** (FreeWill Impact Fund, EIN 86-1218871) | “over 55,000 nonprofits and cause funds that use our tool” [F] | **TY2024: $11,891,225**, all non-cash: crypto $7,628,569 in 648 gifts, public securities $4,262,656 in 338 gifts [F] | At least 263 and, at one charity per gift, about 986 organisations were paid in TY2024 (648 if only crypto is counted): **0.5–1.8% of 55,000** [C]. $5,430,494 (45.7% of intake) went in one grant to The Oregon Community Foundation, a DAFRC-listed sponsor [F/C] |
| **GivingIQ / DonateStock** (DonateStock Charitable Inc, EIN 87-1569770) | “thousands of organizations” / “thousands of nonprofits” [F] | **FY2025: $25,121,004** in 2,630 publicly traded securities gifts (FY2024 $12,778,129 in 1,565) [F] | At least 588 recipients in FY2025 [C], and the charity’s own Part III says “thousands of stock donations to over 350 organizations” [F]. “Thousands” fits the gift count, not the organisation count |
| **Engiven** (no affiliated charity; partner GVNGorg, EIN 81-2446261) | “Serving 10,000+ World-Changing Organizations”, and on the same page “1000+ Engiven customers” [F] | GVNGorg reports **no non-cash contributions** in TY2021–TY2024; contributions $1.0m–$2.4m, all cash [F] | Not testable from any 990. The named crypto partner shows no crypto at all, and Engiven’s own page carries counts that differ tenfold [C] |
| **GVNG** | (2021 DonateStock stock partner) | DonateStock Charitable granted GVNGorg $42,631 (FY2022), $113,657 (FY2023), $29,945 (FY2024) and $47,086 (FY2025) [F] | The partnership is visible only as these grants: 2.7%, 6.1% and 1.2% of GVNG’s FY2022–24 contributions [C]. GVNG now presents itself as a fiscal sponsor and corporate-giving platform [F] |
| **The Giving Block** (Shift4; Giving Block Foundation, EIN 92-3363254) | “approximately 2,400 charities” (Shift4 FY2025 10-K); “over $100 million” of 2025 crypto (own report) [F] | **No filing**: the foundation was ruled exempt in 2024-12 and has no indexed 990 [F]. Shift4 never gives a Giving Block figure [F] | Shift4 folds “stock donations” into total volume ($209bn in FY2025), so $100m would be 0.048% of it [C]. On the report page, 22,343 donations × $11,019 average = $246.2m, 2.46× the headline [C] |

**Bottom line (A) [C/I].**
- The three charities that file show **$24.7m of combined FY2024 intake** (FreeWill Impact Fund $11.9m, DonateStock Charitable $12.8m) and **$37.0m** once DonateStock’s FY2025 ($25.1m) replaces its FY2024. That is small next to one complex-asset intermediary (Dechomai Asset Trust took in $649.8m of Schedule M gifts in 2024 [R]).
- **Vendor organisation counts measure sign-ups, not recipients.** In the latest year, each charity paid hundreds of organisations, not tens of thousands.
- **Intake vendors also feed DAF sponsors.** FreeWill Impact Fund sent 49.6% of its TY2024 Schedule I dollars to DAFRC-listed sponsors, and DonateStock Charitable sent 3.3% in FY2025 [C]. If vendor intake is added to sponsor intake, these dollars are counted twice.
- **DonateStock’s FY2023 “zero” is a blank coded as 0** (§2.2). DAFRC’s FY2023 and FY2024 rows carry $0 of contributions and grants. The returns leave Schedule D lines 2–3 blank while Part VIII reports $5,078,851 and $12,778,129 [F]. In FY2025 DonateStock answered Part IV line 6 “No” and dropped Schedule D.

### (B) P-B38C-03: DAFpay Network in market totals

**Decision: neither sponsor totals nor processor totals.** Record DPN only as an intermediary memo line (DAF-grant disbursement) [C/I].

| Rule (repo source) | DPN TY2024 / TY2025 | Effect |
|---|---|---|
| R1 DAFRC selection: Schedule D Part I filed with DAF assets ≥ $1, then vetting ([g1915b-04](g1915b-04-line6-vs-schedule-d.md) §1.4, DAFRC technical appendix) | No Schedule D in either year [F] | DPN can never enter a DAFRC-based sponsor total; this matches the panel, which has no DPN row [C] |
| R2 Part IV line 6 | “No” in both years (`0`, `false`) [F] | Line-6 screens (SOI extract; P-MOR-01 outside-DAFRC scan) also exclude it |
| R3 Processor series (DAFRC “Donation Processor” type, paired with a unit screen; [b40n13-03-g1913-03](b40n13-03-g1913-03-schema-and-processor-accounts.md) §4.3 as corrected in wave 40A) | Not in the DAFRC panel, so not a processor [C] | The processor series is a subset of Schedule D filers. Its dollars stay in totals because they are DAF dollars, and DPN files none |
| R4 Own wording | “THE CHARITY OPERATES AS A SPONSOR TO DONOR ADVISED FUNDS…” (Part III / Schedule O) [F] | Self-description alone does not admit a filer under any repo rule. FreeWill Impact Fund (“OPERATES A DONOR ADVISED FUND”) is in the same position |
| R5 Double count | DPN’s receipts are DAF grants: it “facilitates … donations between Donor Advised Funds (DAFs) and the 1.5 million 501(c)3) nonprofit organizations” (site) [F] | Its $1,199,247 and $2,941,073 of contributions are already in sponsors’ grants out. Adding them as sponsor or processor inflows counts the same dollars twice |

**Scale:** DPN’s TY2025 contributions are 0.0044% of DAFRC’s corrected FY2024 DAF grants ($66.44bn) [C]. The decision matters for consistency, not for the totals.

**Where the repo counts DPN.** No data file feeding market totals carries EIN 93-1372175 [C: grep of `data/`]. The problems are in the text: one passage calls DPN a DAF sponsor, one still calls it audited, and one says its TY2025 data come only from ProPublica. Corrections are in §5.

---

## 1. Method

### 1.1 Filings
- **Index:** IRS TEOS `index_2019..2026.csv` (local copies of 2026-11-14/15, plus `index_2026.csv` re-downloaded 2026-11-20). The index was searched by EIN for the five charities, and by name for “FREEWILL”, “DONATESTOCK”, “GVNG”, “GIVING BLOCK”, “ENGIVEN”, “OVERFLOW”, “COCATALYST” and “SHIFT4”.
- **Scope (tax years 2021+):** 17 returns indexed and read; 15 selected after keeping the latest `ReturnTs` per EIN and tax period:
  - FreeWill Impact Fund: TY2021–24.
  - DonateStock Charitable: TY2021 (990-EZ), TY2022–25.
  - GVNGorg: TY2021–24. TY2021 and TY2024 each have an amended return, and the amended return is selected; TY2019–20 are out of window.
  - DPN: TY2024–25.
- **XML sources:**
  - The GivingTuesday mirror for 15 returns.
  - IRS TEOS zip range reads (`mission_batch35_screens.teos_fetch`) for two 2026 filings that are still not mirrored (both returned 404 on 2026-11-20): DonateStock FY2025 (`2026_TEOS_XML_10A`, member `202632859349300138_public.xml`) and DPN TY2025 (`2026_TEOS_XML_05B`).
- **EO BMF** (`eo1..eo4.csv`, IRS extract of 2026-11-14): ruling date, foundation code and latest revenue for each EIN.
- **DAFRC:** `dafrc-sponsor-schedule-d-fy2019-2024.csv` and `dafrc-corrected-market-totals.csv` [R].

### 1.2 Extraction (script)
For every return the script reads:
- Part VIII 1h and 1g, program-service revenue, Part IX line 1, management fees and other expenses, Part VII-B contractors;
- Part IV line 6, `FSAuditedInd`, Form 8282 count;
- Schedule D Part I; Schedule M categories (counts, values, methods; crypto from “Other” with a crypto description) and Forms 8283;
- every Schedule I line, tagged when the recipient EIN is in the DAFRC panel;
- Schedule A substantial-contributor amounts;
- text containing DAF, fiscal-sponsor or liquidation wording.

From these it derives:
- **Recipient floor** = Schedule I lines + ⌈(Part IX line 1 − Schedule I total) ÷ $5,000⌉. Unlisted recipients received at most $5,000 each.
- **Gift count** = the Schedule M count, an indicative ceiling at one designated charity per gift (§4).

### 1.3 Claims and Shift4
- Each vendor claim is checked against a cached copy of its page, after whitespace and quote-mark normalisation. All 11 quotes were found (`quote_found=True` in the CSV).
- **Shift4:**
  - 11 quotes were checked against `pdftotext` output of the 10-K/10-Q PDFs that investors.shift4.com serves (FY2022–FY2025 10-Ks and the Q3 2026 10-Q), and all 11 were found.
  - All 26 “announces … quarter results” press releases from 2020-Q2 to 2026-Q3 were scanned for “Giving Block”, “stock donation” and “crypto”.
  - sec.gov was not used.

### 1.4 Run
```
python3 -I scripts/mission_noncash_vendors.py . --irs-dir <scratch>/irs --irs-dir <scratch>/q1403/irs \
        --work-dir <scratch>/q1403/work --xml-dir <scratch>/q1403/xml \
        --web-dir <scratch>/q1403/web/cache --releases-dir <scratch>/q1403/web/s4 [--fetch]
```

### 1.5 Robots and access log (2026-11-20, UA `research-script/1.0`)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 18 XML × 200; 2 × 404 (2026 filings not mirrored) |
| apps.irs.gov | 302 → www.irs.gov/404 (no rules) | `index_2026.csv` 200; two TEOS zip range reads |
| projects.propublica.org | 200; `/nonprofits/api/` not disallowed | 4 API JSON × 200 (filing lists only) |
| investors.shift4.com | 200; disallows `/form-submit` only | sitemap; 29 press releases; financial-results page; 8 SEC-filing PDFs (all 200); one guessed URL 404 |
| d1io3yog0oux5.cloudfront.net (Shift4 shareholder letters) | **403** | **not fetched [B]** (unreadable robots counted as blocked) |
| www.shift4.com | **429** | not fetched [B] |
| thegivingblock.com | 200; `/annual-report/` allowed | 1 page |
| www.freewill.com | 200; `/learn/` allowed | 1 page |
| givingiq.com | 200; `Allow: /` | 2 pages |
| engiven.com | 200; no disallow | 2 pages |
| www.engiven.com | 200; no disallow (**checked after the fetch**; the page was a duplicate and is not used) | 1 page |
| gvng.org, www.gvng.org | 200; disallows `/promos/`, `/wp-admin/` | home page |
| cryptoforcharity.io | 301 | not fetched |

No logins, forms or outreach. sec.gov, crt.sh and certspotter were not used.

---

## 2. Results (A)

### 2.1 FreeWill Impact Fund (Crypto for Charity) [F/C]

| TY | Contributions (all non-cash) | Crypto (gifts) | Securities (gifts) | Crypto share | Grants (IX 1) | Sch I lines >$5k (share of grants) | Recipient floor | Processing fees | Form 8282 filed |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | $1,188,952 | $231,583 (6) | $782,514 (51) | 22.8%* | $1,152,131 | 24 (41.3%) | 160 | $36,921 (3.1%) | 29 |
| 2022 | $2,503,817 | $1,281,328 (1,051) | $1,222,489 (123) | 51.2% | $2,390,931 | 11 (13.3%) | 426 | $71,853 (2.9%) | 63 |
| 2023 | $5,675,000 | $930,078 (750†) | $4,744,922 (750†) | 16.4% | $5,607,138 | 107 (73.4%) | 406 | $67,938 (1.2%) | 84 |
| 2024 | **$11,891,225** | **$7,628,569 (648)** | $4,262,656 (338) | **64.2%** | $11,852,523 | 91 (92.7%) | 263 | $41,259 (0.35%) | 102 |

\* TY2021 Schedule M totals $1,014,097, which is 85.3% of Part VIII 1g; $174,855 is not itemised.
† The identical counts (750 and 750) look like placeholders [I] (P-B40N14-03-02).

- **This is the item’s “CY2024+ Schedule M crypto lines”**: $7.63m in 648 crypto gifts (average $11,772) [C]. No TY2025 return is indexed yet.
- **Concentration.** $5,430,494 went to The Oregon Community Foundation (EIN 23-7315673): 45.7% of TY2024 intake and 49.4% of Schedule I [C]. The TY2023 top line was AI4ALL ($1,005,179).
- **Not a DAF on its checkboxes.** Every year’s Part III says “FREEWILL IMPACT FUND OPERATES A DONOR ADVISED FUND”, yet Part IV line 6 is 0 and no Schedule D is filed [F]. This is the same pattern as DPN (§3).
- **“Zero-fee”.** The only fee lines are “PROCESSING FEES” of 0.35–3.1% of intake [F]. No payment to FreeWill Co. is listed (no contractor over $100k).
- **55,000 test.** In TY2024 the fund paid at least 263 organisations. At one charity per gift, at most about 986 received anything: **0.48% to 1.79% of 55,000**, or 1.18% on crypto gifts alone. That is $216 of filed intake per claimed nonprofit [C]. The claim describes organisations that can be selected in the tool, not organisations that receive money.

### 2.2 DonateStock Charitable (GivingIQ) and the FY2023 anomaly [F/C]

| FY | Contributions (all public securities; gifts) | Grants (IX 1) | Sch I lines (top line) | Recipient floor | Part IV line 6 / Schedule D | DAFRC contributions / grants | Paid to DonateStock Inc (share of intake) |
|---|---|---|---|---|---|---|---|
| 2021 (990-EZ) | — (gross receipts $4,529) | — | 0 | 0 | No / none | not in panel | — |
| 2022 | $9,372,727 (538) | $8,852,558 | 57 (World Central Kitchen $6,307,480 = 77.3%) | 197 | Yes / lines 2–3 = Part VIII and Part IX exactly | $9,372,727 / $8,852,558 | $119,000 mgmt fees (1.27%) |
| 2023 | $5,078,851 (203) | $5,334,774 | 108 (WCK $1,312,288) | 361 | Yes / 33 DAFs, EOY $112,983, **lines 2–3 blank** | **$0 / $0** | $102,784 (2.02%) |
| 2024 | $12,778,129 (1,565) | $10,585,357 | 215 (WCK $1,944,777) | 319 | Yes / 33 DAFs, EOY $2,162,863, **lines 2–3 blank** | **$0 / $0** | $275,686 (2.16%) |
| 2025 | **$25,121,004 (2,630)** | $23,298,501 | 384 (WCK $6,590,024 = 29.6%) | 588 | **No / no Schedule D** | (after DAFRC window) | **$709,796 (2.83%)**: contractor “DonateStock Inc” |

**The anomaly** [F/C]:
- DAFRC marks the FY2023 and FY2024 values “IRS 990”, but the XML has no `DonorAdvisedFundsContriAmt` or `DonorAdvisedFundsGrantsAmt`. The 0s are blanks coded as zero, and FY2024 is affected as well as FY2023.
- The Part VIII and Part IX proxies are $5.08m and $5.33m (FY2023) and $12.78m and $10.59m (FY2024). At most these are 0.008% and 0.014% of DAFRC’s corrected contributions for those years [C].
- The repo harvest already flags `sched_d_grants_missing` on both returns [R].

**What DonateStock Charitable is** [F]:
- It calls itself a “Fiscal sponsor”.
- Its Schedule I note says: “The organization receive stock and immediately liquidates the stock and contributes this cash to the recipient.” (FY2024 and FY2025)
- Schedule O for FY2025 says it has no employees: DonateStock, Inc. (“DSI”) provides management for $668,396, plus $41,400 of “software-as-a-service fees”.
- It is a pass-through. Its FY2022–24 Schedule D (10, then 33 “DAFs”) puts it in DAFRC as National/Standard [R], but in FY2025 it answered line 6 “No” and filed no Schedule D.

**Fee take vs the published price** [C/I]:
- Payments to DSI rose from 1.27% of intake (FY2022) to 2.83% (FY2025).
- Both figures are below the 3.9% Standard rate and the 2.5–2.9% Premium rates.
- Fees that nonprofits pay GivingIQ directly, outside the charity, would not show here.

**“Thousands of organizations”:**
- Recipients number at least 588 in FY2025 and at most 2,630 at one per gift [C].
- The charity itself says “over 350 organizations” [F].
- The FY2022–FY2024 narrative repeats “more than 300 charitable organizations in our first full year” word for word, so it is not a yearly count [F].

### 2.3 GVNGorg and Engiven [F/C]

| TY | Contributions | Non-cash (VIII 1g) | Grants (IX 1) | Line 6 | From DonateStock Charitable (Sch I) |
|---|---|---|---|---|---|
| 2021 (amended) | $999,268 | none | $1,234,395 | No | — (DSC’s first full year is 2022) |
| 2022 | $1,597,944 | none | $648,641 | No | $42,631 |
| 2023 | $1,860,462 | none | $267,578 | No | $113,657 |
| 2024 (amended) | $2,440,010 | none | $545,175 | No | $29,945 |
| 2025 | n/a (not filed yet) | | | | $47,086 (DSC FY2025) |

- GVNG’s TY2021 Schedule I sent $492,149 (78.4%) to the Edward Charles Foundation, a DAFRC-listed sponsor [F/C].
- Its expenses include “PROJECT COSTS FISCAL SPONSORS” ($199,123 in 2023 and $331,270 in 2024) and “PLATFORM EXPENSE”.
- Schedule O says a director “IS ALSO A DIRECTOR AND OFFICER OF A CORPORATION THAT LICENSES AND MANAGES THE PLATFORM USED BY GVNGorg” [F].
- **Engiven test.** Engiven names GVNG as a crypto partner (“Our partnership with Engiven makes donating crypto seamless for GVNG users”), but GVNG’s returns show **no non-cash contributions** in any year read [F]. Any Engiven crypto reaches GVNG as cash after conversion, or does not reach it at all [I].
- Engiven files no 990 of its own. Its “10,000+” sits beside “1000+ Engiven customers” on the same page [F]. Neither can be tested against filed dollars.

### 2.4 Shift4 and The Giving Block [F/C]

- **Charity count.** The 10-Ks say “over 2,000 charities” (FY2022–FY2024) and “approximately 2,400 charities” (FY2025).
- **Volume definitions.**
  - FY2022 10-K: volume includes “alternative payment methods, including cryptocurrency donations”.
  - FY2023 and FY2024 10-Ks: “including cryptocurrency and stock donations”.
  - FY2025 10-K and Q3 2026 10-Q: “including cryptocurrency, stored value, gift cards and stock donations”.
  - **None gives a Giving Block or stock-donation figure.** FY2025 volume was $209bn (FY2024 $165bn).
- **Earnings releases.** 26 releases (2020-Q2 to 2026-Q3) contain 0 mentions of “Giving Block”, “stock donation” or “crypto” [C].
- **What is disclosed:**
  - crypto settlement assets held for Giving Block users: $1.8m, $3.5m and $5.7m at year-ends 2022–24, no longer recognised from 2025 under SAB 122;
  - an earnout “calculated as a multiple of revenue earned by The Giving Block from March 1, 2022 to February 28, 2023”, settled at $10.4m;
  - “The acquisition of The Giving Block did not have a material impact on the Company's consolidated financial statements” (FY2023 10-K).
- **Self-reported 2025 figures** ([annual report](https://thegivingblock.com/annual-report/)):
  - “over $100 million” of crypto, “22,343 donations”, “average gift of $11,019”, and “One in five nonprofits on The Giving Block raised over $100,000”.
  - Count × average = **$246,197,517**, 2.46× the headline [C].
  - The one-in-five line implies at least $48m at about 2,400 charities [C].
  - The figures cannot all describe the same base. They are not resolved here (P-B40N14-03-04).
- **Affiliated charity.** Giving Block Foundation (EIN 92-3363254, Miami, care of “THE GIVING BLOCK - DAVID JOHNSON”) was ruled exempt in 2024-12 under foundation code 15. It has no indexed 990 [F: BMF, index], so no Giving Block dollars are filed anywhere yet.
- **Shareholder letters** (cloudfront host) were not read [B].

---

## 3. Results (B): DPN classification

### 3.1 The filings [F]

| | TY2024 (202510729349301206) | TY2025 (202621389349300637) |
|---|---|---|
| Contributions (VIII 1h) | $1,199,247 | $2,941,073 |
| Grants (IX 1) | $831,404 | $2,178,671 |
| Part IV line 6 | 0 | false |
| Schedule D | not filed | not filed |
| Mission / Schedule O | “THE CHARITY OPERATES AS A SPONSOR TO DONOR ADVISED FUNDS…” | same |
| Schedule A | — (first five years) | 3-year gifts $4,140,846; above the 2% per-contributor cap $2,138,755 (51.7%) |
| EO BMF (TY2025) | | revenue $2,952,210; assets $1,048,550; NTEE T12 |

The Schedule A line shows that a few contributors, each giving more than about $83,000 over three years, supplied about half of DPN’s receipts [C]. Their names are redacted in Schedule B.

### 3.2 Rule-by-rule result (CSV `dpn_classification`; the script applies the same rules to the comparators)

| Filer-year | R1 Sch D with DAF assets | R2 line 6 | R3 DAFRC processor | R4 DAF / fiscal-sponsor wording | R5 receipts are DAF grants | Bucket |
|---|---|---|---|---|---|---|
| DPN 2024, 2025 | no | No | no (not in panel) | yes | yes | **neither** (memo line) |
| FreeWill Impact Fund 2021–24 | no | No | no (not in panel) | yes | no | neither (memo line) |
| DonateStock Charitable 2022–24 | yes | Yes | no (DAFRC National/Standard) | yes (“fiscal sponsor”) | no | sponsor totals at Schedule D values (FY2023–24 lines 2–3 blank) |
| DonateStock Charitable 2025 | no | No | — | yes | no | neither (memo line) |

### 3.3 Why not sponsor totals, and why not processor totals [I, on [F] rules]
1. **Sponsor totals are Schedule D totals.** DAFRC selects on Schedule D Part I and vets the result; line 6 does not decide inclusion (g1915b-04 §1.4). DPN files no Schedule D, so there is no DAF value, account count, contribution or grant to add. Substituting Part VIII would break the rule the whole series rests on.
2. **The processor series is not a home for non-filers.** In b40n13-03-g1913-03, “processor” means a DAFRC panel member of type Donation Processor (AOGF, PPGF, Givinga, Blackbaud Giving Fund, For Good and 17 others). Their Schedule D dollars stay in contribution, grant and asset totals, and only their account counts are split off (§4.3 items 1 and 4, as corrected by wave 40A). DPN is upstream of none of this. It receives grants that donors recommend from accounts at sponsors, then regrants them to nonprofits that have not claimed a Chariot account.
3. **Double count.** DPN’s contributions are sponsor grants out. Counting them as inflows anywhere in the DAF totals would count the same dollars twice, once leaving the sponsor and once arriving at DPN.
4. **Self-description is not a test.** The repo already rejects the DAFRC type label alone as a unit test (wave 40A C08). Mission wording is weaker still, and FreeWill Impact Fund uses the same words with the same checkboxes.
5. **Treatment.** Report DPN, FreeWill Impact Fund and DonateStock FY2025 in an **intermediary memo line** of self-described DAF charities with no Schedule D. Show their contributions and grants with the note that they add no DAF dollars, and that DPN’s are already counted as sponsor grants.

---

## 4. Limits
- **Recipient counts are bounded, not counted.** Schedule I lists only recipients above $5,000. The floor assumes unlisted recipients got exactly $5,000. The gift-count “ceiling” assumes one charity per gift. It is not binding where Schedule M counts look incomplete or placeholder (FreeWill TY2021 and TY2023; DonateStock FY2023, where 203 gifts sit below a floor of 361), or where grants pay out prior-year gifts.
- **Affiliated charities see only part of each vendor’s volume.** Stock gifts that go straight to a nonprofit’s own brokerage account through the vendor’s widget never reach the charity. So the filed dollars are a floor on FreeWill’s and GivingIQ’s stock volume. They should be close to complete for Crypto for Charity, which routes every gift through the fund.
- **Fiscal years.** All four charities file on calendar years. Vendor claims are undated or current (read 2026-11-20).
- **Not available yet:** FreeWill Impact Fund TY2025 and GVNG TY2025 (not indexed); Giving Block Foundation (no return); Shift4 shareholder letters (robots 403).
- **DonateStock DAFRC impact** is computed against corrected panel totals and is not applied to them.
- **DPN R5** rests on DPN’s own site and Chariot’s help pages (repo batch 38). Schedule B is redacted, so the contributors are not named.

---

## 5. Exact corrections

### `research/mission-2026-11-14/b40n14-b38c-dechomai-dafpay.md`

- **Find:** "- **Conclusion** [I]: legally, DPN describes itself as a sponsor that takes title. In practice it acts as a pass-through facilitator for Chariot, and its own Part IV answers say it holds no DAFs."
- **Replace with:** "- **Conclusion** [I]: legally, DPN describes itself as a sponsor that takes title. In practice it acts as a pass-through facilitator for Chariot, and its own Part IV answers say it holds no DAFs. For market totals DPN belongs in neither sponsor nor processor totals. It files no Schedule D, so DAFRC’s Schedule D Part I selection rule never admits it, and its $1,199,247 (TY2024) and $2,941,073 (TY2025) of contributions are grants from DAF sponsors that are already counted in those sponsors’ grants out. It is reported only as an intermediary memo line (b40n14-03-b38c-03 §3) [b38c-03]"

### `research/mission-2026-11-14/queue-batch38-closeout-checks.md`

- **Find:** "  - DPN carries only unclaimed-nonprofit and five named Jewish-giving-platform flows, about $1.2m in TY2024 and $2.9m in TY2025."
- **Replace with:** "  - DPN carries only unclaimed-nonprofit and five named Jewish-giving-platform flows, about $1.2m in TY2024 and $2.9m in TY2025. These are DAF grants that DPN receives and regrants. It answers Part IV line 6 “No” and files no Schedule D, so its flows belong in neither sponsor nor processor totals; adding them would double-count sponsor grants (b40n14-03-b38c-03 §3) [b38c-03]"

- **Find:** "  - The only audited slice is DPN (§4)."
- **Replace with:** "  - DPN is the only slice with a public 990 (§4). That 990 is not audited: `FSAuditedInd` is false or 0 in TY2024 and TY2025 (wave 37B) [b38c-03]"

- **Find:** "- **DPN TY2025** comes from ProPublica's summary only, since its XML is not yet mirrored."
- **Replace with:** "- **DPN TY2025** was first read from ProPublica’s summary. Its XML is public in IRS TEOS `2026_TEOS_XML_05B` and was read in wave 37B and in b40n14-03-b38c-03; it was still not on the GivingTuesday mirror on 2026-11-20 [b38c-03]"

- **Find:** "| Grants paid | — | $831,404 (largest: Chai Lifeline $372,832; Effective Ventures Foundation $155,818) | n/a in summary"
- **Replace with:** "| Grants paid | — | $831,404 (largest: Chai Lifeline $372,832; Effective Ventures Foundation $155,818) | $2,178,671 (TY2025 XML, Part IX line 1; 104 Schedule I lines totalling $1,324,158) [b38c-03]"

### `research/mission-2026-11-14/queue-fidelity-chariot-goodstack-vanguard.md`

- **Find:** "That is the same dual role as Chariot (DAFpay Network) and Every.org."
- **Replace with:** "That is the same dual role as Every.org. Chariot’s DAFpay Network is not a comparable DAF sponsor: its mission text says it sponsors DAFs, but it answers Part IV line 6 “No”, files no Schedule D and regrants DAF grants it receives (b40n14-03-b38c-03 §3) [b38c-03]"

### `research/mission-2026-11-14/b40n13-03-g1913-03-schema-and-processor-accounts.md`

- **Find:** "4. **Dollars:** keep processors in contribution, grant and asset totals. Flag AOGF's FYE 2026 and BBGF's CY2025 basis changes as breaks in the series (P-G1913-03-03)."
- **Replace with:** "4. **Dollars:** keep processors in contribution, grant and asset totals. Flag AOGF’s FYE 2026 and BBGF’s CY2025 basis changes as breaks in the series (P-G1913-03-03).\n5. **Outside both series:** self-described DAF charities that answer Part IV line 6 “No” and file no Schedule D (DAFpay Network TY2024–25, FreeWill Impact Fund TY2021–24, DonateStock Charitable FY2025) hold no filed DAF accounts and add no DAF dollars. DPN’s receipts are grants from DAF sponsors and the other two pass gifts straight through, so they are shown only as an intermediary memo line, never in sponsor or processor totals (b40n14-03-b38c-03 §3) [b38c-03]"

### `research/mission-2026-11-14/direction-noncash-gift-infrastructure.md`

- **Find:** "    - FY2023: contributions and grants recorded as 0, probably missing data ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml))."
- **Replace with:** "    - FY2023 and FY2024: DAFRC records contributions and grants as 0 (source “IRS 990”), but both returns leave Schedule D Part I lines 2–3 blank. Part VIII reports $5,078,851 (FY2023) and $12,778,129 (FY2024) of contributions, all publicly traded securities, and Part IX line 1 reports $5,334,774 and $10,585,357 of grants, so the zero is a blank coded as 0. In FY2025 (return 202632859349300138, filed 2026-10-12) it answered Part IV line 6 “No”, filed no Schedule D, took in $25,121,004 in 2,630 gifts and paid DonateStock Inc $709,796 (2.83%) ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542229349300304_public.xml); b40n14-03-b38c-03 §2.2) [b38c-03]"

- **Find:** "   - Everything else is company claims, or small 990 figures such as FreeWill Impact Fund's $5.68m (CY2023)."
- **Replace with:** "   - Everything else is company claims, or small 990 figures. FreeWill Impact Fund took in $5.68m (CY2023) and $11.89m (CY2024, of which $7.63m was crypto in 648 gifts), and DonateStock Charitable $12.78m (FY2024) and $25.12m (FY2025). Each paid hundreds of organisations a year, not the tens of thousands its vendor claims (b40n14-03-b38c-03 §2) [b38c-03]"

- **Find:** "  - FreeWill Impact Fund's total contributions, all channels: CY2021 $1.19m, CY2022 $2.50m, CY2023 $5.68m ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json)) [F]."
- **Replace with:** "  - FreeWill Impact Fund’s total contributions, all non-cash: CY2021 $1.19m, CY2022 $2.50m, CY2023 $5.68m, CY2024 $11.89m. Schedule M for CY2024 shows crypto $7,628,569 in 648 gifts and securities $4,262,656 in 338. $5,430,494 (45.7%) went in one grant to The Oregon Community Foundation. Part IV line 6 is “No” and no Schedule D is filed, although Part III says it “OPERATES A DONOR ADVISED FUND” ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/861218871.json); TY2024 XML 202503189349308315; b40n14-03-b38c-03 §2.1) [b38c-03]"

- **Find:** "   - Engiven is GVNG's crypto partner."
- **Replace with:** "   - Engiven is GVNG’s crypto partner, but GVNGorg (EIN 81-2446261) reports no non-cash contributions in TY2021–TY2024. The DonateStock partnership is visible only as DonateStock Charitable’s grants to GVNG: $42,631 (FY2022), $113,657 (FY2023), $29,945 (FY2024) and $47,086 (FY2025) (b40n14-03-b38c-03 §2.3) [b38c-03]"

- **Find:** "It does not disclose a figure for The Giving Block alone."
- **Replace with:** "It does not disclose a figure for The Giving Block alone. None of its 26 earnings releases from 2020-Q2 to 2026-Q3 mentions The Giving Block, and its FY2025 10-K and 2026 10-Qs fold “stock donations” into total volume ($209bn in FY2025), of which The Giving Block’s self-reported “over $100 million” of 2025 crypto would be 0.048%. Giving Block Foundation (EIN 92-3363254, ruled 2024-12) has filed no Form 990 yet (b40n14-03-b38c-03 §2.4) [b38c-03]"

### `research/mission-2026-11-14/gap19-fy2025-refresh.md`

- **Find:** "DonateStock, which leaves the value blank"
- **Replace with:** "DonateStock, which answers Part IV line 6 “No” and attaches no Schedule D to its FY2025 return (202632859349300138), so it has no FY2025 DAF value and is not a DAF sponsor-year under DAFRC’s Schedule D selection rule; its $25,121,004 of contributions are pass-through stock gifts (b40n14-03-b38c-03 §2.2) [b38c-03]"

### `data/mission-2026-11-14/noncash-gift-vendors-2026.csv`

- **Find:** "CY2024 return filed, no extract"
- **Replace with:** "CY2024 $11.89m (Schedule M: crypto $7.63m in 648 gifts; securities $4.26m in 338 gifts; 45.7% granted to The Oregon Community Foundation) [b38c-03]"

- **Find:** "FY2023 33 DAFs, EOY $0.11m; FY2024 33 DAFs, EOY $2.16m"
- **Replace with:** "FY2023 33 DAFs, EOY $0.11m; FY2024 33 DAFs, EOY $2.16m; FY2023-24 Sch. D lines 2-3 blank (DAFRC codes 0) while Part VIII shows $5.08m and $12.78m; FY2025 no Sch. D and line 6 No, contributions $25.12m in 2,630 gifts, $0.71m paid to DonateStock Inc [b38c-03]"

---

## 6. Data dictionary

### 6.1 `noncash-vendor-volumes-2026-11-20.csv` (1,687 rows)

| Column | Meaning |
|---|---|
| record_type | Row kind (table below) |
| entity | Filer (FreeWill Impact Fund, DonateStock Charitable Inc, GVNGorg, DAFpay Network Inc, Giving Block Foundation), vendor name for claim rows, or Shift4 Payments |
| ein | 9-digit EIN (blank for Shift4 rows) |
| tax_year | First four digits of TaxPeriodEndDt (DAFRC rows: DAFRC fiscal year; claim rows: year of the return tested) |
| tax_period_end | TaxPeriodEndDt (BMF rows: TAX_PERIOD yyyymm) |
| object_id | IRS e-file object id |
| selected | 1 = version used (latest ReturnTs per EIN and tax period); 0 = superseded |
| item | Line or measure (e.g. `contributions_viii_1h`, `sched_d_DonorAdvisedFundsContriAmt`, `sched_m_crypto`, `recipient_count_bounds`, `claim_vs_filed_gifts`) |
| category | Schedule M class (crypto / public_securities / other); `DAFRC sponsor` on Schedule I lines to DAFRC-panel EINs; DAFRC type on `dafrc_compare`; bucket on `dpn_classification` |
| count | Count (gifts, lines, recipient floor, claimed organisations) |
| amount_usd | Main US$ amount |
| amount2_usd | Second amount (denominator, proxy, or gift-count ceiling; defined in `text`) |
| ratio | Computed share; definition in `text` |
| text | Filing text, quote with `quote_found` flag, or computation note |
| source_url | XML URL (mirror, or TEOS zip#member), first-party page, or IR-site PDF |

| record_type | Content |
|---|---|
| return_line / return_flag | Part VIII/IX, balance sheet, Schedule D Part I, Schedule A, Forms 8282/8283; header, line 6, Schedule D presence, audit flag, schedules filed |
| sched_m | Schedule M category rows |
| sched_i | Every Schedule I line (cash, non-cash, recipient, EIN) |
| narrative, contractor, other_expense | DAF / fiscal-sponsor / liquidation text; Part VII-B; Part IX other expenses |
| vendor_year | Per selected return: intake, crypto/securities split, average gift, Schedule I coverage and concentration, recipient bounds, grants to GVNG and to DAFRC sponsors, vendor or processing fee |
| dafrc_compare | DAFRC value vs Schedule D as filed vs 990 proxy, with share of DAFRC corrected totals |
| claim_test | Vendor claims vs filed gifts and recipients; Giving Block arithmetic |
| shift4_disclosure | Verified 10-K/10-Q quotes; FY2025 volume ratio; earnings-release scan |
| bmf | IRS EO BMF row per EIN |
| dpn_classification | R1–R5 per filer-year and resulting bucket |

### 6.2 `queue-proposals-b40n14-03-b38c-03.csv`
Same 17 columns and coding as `queue-proposals-gap19-13.csv`.

---

## 7. Source register

| ID | Source | Date | Used in |
|---|---|---|---|
| S1 | IRS TEOS index: https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv (and index_2021..2025) | local copies 2026-11-14/15; 2026 re-read 2026-11-20 | §1.1 |
| S2 | FreeWill Impact Fund TY2021–24 XML: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243189349310159_public.xml ; …/202333159349301513_public.xml ; …/202423189349311277_public.xml ; …/202503189349308315_public.xml | filed 2022-11-14 to 2025-11-14 | §2.1 |
| S3 | DonateStock Charitable TY2021–24 XML: …/202222099349200232_public.xml (990-EZ) ; …/202342659349300229_public.xml ; …/202413209349328306_public.xml ; …/202542229349300304_public.xml | filed 2022-07-28 to 2025-08-10 | §2.2 |
| S4 | DonateStock Charitable FY2025: member 202632859349300138_public.xml in https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_10A.zip | ReturnTs 2026-10-12 | §2.2 |
| S5 | GVNGorg TY2021–24 XML: …/202233199349322918_public.xml ; …/202341009349300129_public.xml (amended) ; …/202313199349319821_public.xml ; …/202413209349321456_public.xml ; …/202523189349316212_public.xml ; …/202640849349301639_public.xml (amended) | 2022-11-15 to 2026-03-25 | §2.3 |
| S6 | DPN TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202510729349301206_public.xml ; TY2025: member 202621389349300637_public.xml in https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip | 2025-03-13; 2026-05-18 | §3 |
| S7 | IRS EO BMF extract (eo1–eo4.csv): https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | 2026-11-14 | §2.4, §3.1 |
| S8 | ProPublica Nonprofit Explorer API: https://projects.propublica.org/nonprofits/api/v2/organizations/{861218871,871569770,812446261,923363254}.json | 2026-11-20 | §1.1 (filing lists) |
| S9 | FreeWill crypto page: https://www.freewill.com/learn/how-to-donate-crypto-to-charity | 2026-11-20 | §0, §2.1 |
| S10 | GivingIQ: https://givingiq.com/ ; https://givingiq.com/about | 2026-11-20 | §0, §2.2 |
| S11 | Engiven: https://engiven.com/ ; https://engiven.com/nonprofits | 2026-11-20 | §2.3 |
| S12 | GVNG: https://gvng.org/ | 2026-11-20 | §2.3 |
| S13 | The Giving Block 2026 annual report: https://thegivingblock.com/annual-report/ | 2026-11-20 | §2.4 |
| S14 | Shift4 10-K/10-Q PDFs on the IR site: https://investors.shift4.com/sec-filings/all-sec-filings/content/0001794669-23-000006/0001794669-23-000006.pdf (FY2022) ; …/0001794669-24-000007/… (FY2023) ; …/0001794669-25-000011/… (FY2024) ; …/0001794669-26-000010/… (FY2025) ; …/0001794669-26-000051/… (Q3 2026 10-Q); also …-22-000012, …-26-000020, …-26-000045 (scanned) | 2022–2026 | §2.4 |
| S15 | Shift4 press releases: https://investors.shift4.com/news-events/press-releases (26 results releases 2020-Q2..2026-Q3; detail/176 and detail/178 on The Giving Block) | 2020–2026 | §2.4 |
| S16 | DAFRC panel and corrected totals (repo `dafrc-sponsor-schedule-d-fy2019-2024.csv`, `dafrc-corrected-market-totals.csv`; original https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) | 2025 edition | §2.2, §3 |
| S17 | DAFRC technical appendix selection rule, via [g1915b-04-line6-vs-schedule-d.md](g1915b-04-line6-vs-schedule-d.md): https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Technical-Appendix.pdf | 2025 | §3.3 |
| S18 | DAFpay Network home page: https://www.dafpaynetwork.org/ (quoted via [b40n14-b38c-dechomai-dafpay.md](b40n14-b38c-dechomai-dafpay.md) §4.3) | read 2026-11-19 | §3 |
