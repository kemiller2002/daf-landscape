# P-B40N14-01 and P-B38C-01: Dechomai deep read and DAFpay Network fee booking

**Date:** 2026-11-19. **Task ID:** b40n14-b38c.
**Outputs:**
- Data: [`dechomai-dafpay-2026-11-19.csv`](../../data/mission-2026-11-14/dechomai-dafpay-2026-11-19.csv) (1,226 rows)
- Script: [`scripts/mission_dechomai_dafpay.py`](../../scripts/mission_dechomai_dafpay.py)
- Queue proposals: [`queue-proposals-b40n14-b38c.csv`](../../data/mission-2026-11-14/queue-proposals-b40n14-b38c.csv)

**Evidence tags:** [F] read from a filing or primary page; [C] computed by the script from [F] values; [I] inference; [U] unresolved.

---

## 1. Headlines

1. **Dechomai is a two-entity pipe, not one charity** [F]. Dechomai Asset Trust (DAT, EIN 26-0724604) is a Type I supporting organisation of Dechomai Foundation Inc (DF, EIN 06-1676688). DAT takes in most of the complex assets and pays its cash to DF: $365.2m (2021), $474.8m (2022), $315.3m (2023) and $448.9m (2024). DF then makes the grants to the sponsors (DAT/DF Schedule I and Schedule R).
2. **Asset mix, 2021–24** [C]. Across both entities' Schedule M there were **842 non-cash contributions worth $3,274.2m**, an average of $3.9m each. The script reads 840 and $3,272.9m because it keys works of art as `ArtWorksOfArtGrp`, while DF's 2022 and 2023 returns use `WorksOfArtGrp` ($998,400 and $300,000, one gift each). In the table below, DAT 2022 “Cyrptocurrency” ($2,092,368, 2 gifts) is also misfiled under Other. Corrected: cryptocurrency $157.0m (4.8%, 130 gifts); Other $11.7m (0.4%, 12 gifts, including the two art gifts). Ratios move by at most 0.001 points [V wave 37B] The FAQ says individual gifts "have averaged between $3-7 million". By value:

   | Asset class | Value | Share | Gifts |
   |---|---|---|---|
   | Private business interests (closely held stock; partnership, LLC and trust interests) | $2,704.5m | 82.6% | 480 |
   | Real estate | $306.7m | 9.4% | 211 |
   | Cryptocurrency | $154.9m | 4.7% | 128 |
   | Publicly traded securities | $94.3m | 2.9% | 9 |
   | Other | $12.5m | 0.4% | 12 |

   Crypto rose to 15.1% of value in 2024.
3. **Routing to the six national sponsor groups** [C].
   - Dechomai's Schedule I grants to DAFgiving360, Fidelity Charitable, AEF, Goldman Sachs (both funds), Morgan Stanley GIFT and NPT totalled **$1,145.9m in 2021–24, 59.6% of its $1,923.8m of named external grants**.
   - DAF sponsors of any kind on the DAFRC list received **$1,580.9m (82.2%)**.
   - By group: DAFgiving360 $443.2m (23.0%), Fidelity $234.7m (12.2%), AEF $200.5m (10.4%), Goldman $173.2m (9.0%), NPT $56.8m (3.0%), Morgan Stanley GIFT $37.5m (2.0%).
4. **The reverse flow is small** [C]. The sponsors' own Schedule I grants to either Dechomai entity total **$138.0m** over their FY2021–FY2025 returns, about 12% of what Dechomai paid them. Of that:
   - DAFgiving360 gave $73.3m;
   - Fidelity gave $57.2m, including $56.73m of **non-cash "SECURITIES"** in FY6/22;
   - AEF $4.8m, Goldman $2.0m, NPT $0.45m and Morgan Stanley $0.20m.

   [I] The visible pattern is that donors give assets to Dechomai directly, and Dechomai grants the sale proceeds to the donor's account at the sponsor. Sponsor-to-Dechomai grants are the exception.
5. **Fee and administrative outflows are below the published 1–3%, but all non-grant expenses (1.50%) fall inside it** [C]. These are expense outflows, not the fee Dechomai charges. The FAQ says at least half of collected fees go to reserves or unrestricted funds, so they never reach Part IX. DAT's unreconciled $344.5m Schedule R “reimbursement” (10.5% of intake) is also excluded. The fee take itself is therefore not measured. As a share of Schedule M intake for 2021–24: [V wave 37B]
   - payments to Charitable Solutions LLC: $12.6m (**0.39%**);
   - Part IX management plus other fees: $19.9m (0.61%);
   - all non-grant expenses: $49.0m (1.50%).

   Benchmarks on the same base:
   - published 1% to 3%: $32.7m to $98.2m;
   - FAQ average of 1.2–1.4%: $39.3m to $45.8m;
   - the $10,000 minimum across 840 gifts: $8.4m.

   The FAQ says "at least 50% off [sic] all collected fees are used for operating reserves or unrestricted fund purposes". Fees kept that way stay inside the entity and never appear as an expense [I].
6. **An unreconciled $344.5m** [F/U]. DAT's Schedule R reports "cash reimbursement for administrative services" paid to DF:

   | Year | Amount |
   |---|---|
   | 2021 | $60.6m |
   | 2022 | $115.1m |
   | 2023 | $87.8m |
   | 2024 | $80.9m |

   DF's own Schedule R shows only $4.7k–$58.9k of reimbursements from DAT. Neither return carries these amounts in Part IX. Read as a fee, the figure would be 10.5% of intake. It is reported here and not treated as a confirmed fee (P-B40N14-02).
7. **No Form 8282 trail is visible on the 990s** [F].
   - On all eight selected Dechomai returns, Part V line 7c (Form 8282 for tangible personal property) is "No", and no count is given.
   - The text "8282" appears nowhere in any return.
   - Schedule M reports 420 Forms 8283 received (2021–24, both entities), and both entities say they use third parties to sell.
   - Line 7c covers only *tangible personal* property, while Dechomai's assets are mostly business interests and real estate. Form 8282 dispositions of those assets therefore cannot be seen on a 990 at all. Line 7c is not empty of scope, though. Schedule M shows tangible personal property received: works of art of $998,400 (DF 2022) and $300,000 (DF 2023), collectibles of $19 (DAT 2022) and gold of $336,200 (DF 2024). For those gifts the “No” answers are a checkable assertion [V wave 37B]
8. **DAFpay Network TY2025 (filed 2026-05-19) is public in IRS TEOS** [F]. It is batch `2026_TEOS_XML_05B` (the index row says 05A) and is not yet in the GivingTuesday mirror.
   - DPN books **$0 program-service revenue** and **$0 other revenue**.
   - It books **$88,736 of "Fees for services – other", which is 3.02% of its $2,941,073 contributions** against 2.9% = $85,291. That is consistent with the DAFpay fee being booked as an unnamed DPN expense [I]. The match rests on one year of arithmetic within a ±0.5-point window, and the payee is not named. DPN's statements are cash-basis and neither audited nor reviewed (`FSAuditedInd` and `AccountantCompileOrReviewInd` false in TY2025; 0 in TY2024) [V wave 37B]
   - Chariot is not named anywhere in the return, and no contractor is listed (Part VII-B lists only payees over $100k).
   - TY2024 does **not** fit: other fees were $18,345 = 1.53% of $1,199,247.
9. **DPN calls itself a DAF sponsor, but its checkboxes disagree** [F].
   - Part I and Part III: "THE CHARITY OPERATES AS A SPONSOR TO DONOR ADVISED FUNDS… UPON CONTRIBUTION, THE DONOR CEDES ALL LEGAL TITLE TO THE CONTRIBUTED FUNDS TO THE CHARITY" (Schedule O).
   - Part IV line 6 (maintains DAFs) is "No" in both years, and no Schedule D is filed.
   - Its website says it "facilitates safe, easy and fast charitable donations between Donor Advised Funds (DAFs) and the 1.5 million 501(c)3) nonprofit organizations".

---

## 2. Method

### 2.1 Filings
- **Index.** The IRS TEOS indexes `index_2021..2026.csv` (local copies) were searched by EIN for DAT, DF, DPN and the seven sponsor EINs.
- **Sponsor EINs and groups:**
  - DAFgiving360 / Schwab: 31-1640316
  - Fidelity: 11-0303001
  - AEF: 34-1747398
  - Goldman Sachs: 31-1774905 (GS Donor Advised Philanthropy Fund for Wealth Management) and 11-3813663 (The Goldman Sachs Charitable Gift Fund)
  - Morgan Stanley GIFT: 52-7082731
  - NPT: 23-7825575
- **Scope:**
  - Dechomai Form 990s for tax years 2021–2024: 9 filings. DAT TY2023 has an original (202413199349316041) and an amended return (202403229349300510). The amended return is used; the only differences are the `AmendedReturnInd` flag and net UBTI ($43,525,166 → $43,583,514).
  - All DPN Form 990s: TY2024 and TY2025. TY2023 was a 990-N.
  - Every sponsor Form 990 with a tax period from 2021-06 to 2025-06: 34 filings, 33 selected after dropping Fidelity's superseded FY6/22 original.
- **Version rule.** One return is kept per EIN and tax period: the one with the latest `ReturnTs`. Object ids are not in filing order. For DAT TY2023 the amended return has the *smaller* object id.
- **Sources of XML:**
  - GivingTuesday mirror (`gt990datalake-rawdata`): everything except DPN TY2025.
  - DPN TY2025: a range read of member `202621389349300637_public.xml` (Deflate64, 11,074 → 83,034 bytes) from `https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip`, using `mission_batch35_screens.teos_fetch`. The mirror returned 404 on 2026-11-15 and again on 2026-11-19.

### 2.2 Extraction (script, stdlib)
For each Dechomai and DPN return, the script reads:
- Part VIII: contributions, non-cash contributions, program-service revenue, other revenue, and line 7 sales of securities and other assets;
- Part IX: every "fees for services" line, other expenses, grants and total expenses;
- Part IV lines 6 and 21, and Part V line 7c/7d (Form 8282);
- Part VII-B contractors;
- Schedule M categories (count, amount, valuation method), line 30a (Forms 8283), lines 31–33 and the narratives;
- every Schedule I line;
- Schedule D Part I;
- Schedule R Part V transactions;
- all of Schedule O;
- whether Schedule B is redacted;
- every text leaf that mentions "8282" or "Chariot".

Sponsor returns are streamed (`iterparse`). Only Schedule I lines whose recipient EIN is DAT or DF, or whose text contains "Dechomai", are kept.

### 2.3 Derived measures (record types in the CSV)
- **`dechomai_year` (combined DAT+DF):**
  - *Intra-group* transfers are DAT↔DF Schedule I lines.
  - *External contributions* are DAT + DF contributions, minus the intra-group transfer only in years when DF booked it as revenue. DF did so in 2023 and 2024, when its contributions were at least the transfer. In 2021 and 2022 DF's contributions ($172.3m, $39.7m) were below the transfers, so nothing is netted.
  - *External grants* are Schedule I lines to non-Dechomai recipients.
- **`asset_mix`.** Schedule M categories are mapped to five classes:
  - private business interests: closely held stock, and partnership/LLC/trust interests;
  - real estate;
  - cryptocurrency, from the "Other" category with a crypto description;
  - public securities;
  - other.
- **`routing_dechomai_to_sponsor`.** Schedule I amounts (cash plus non-cash) by sponsor group, as a share of external Schedule I grants.
  - **Name overrides EIN** when the two point to different target groups. DF's TY2023 line "SCHWAB CHARITABLE TRUST" ($76,391,938) is filed under AEF's EIN 34-1747398, and the row is flagged `EIN/name conflict` in the CSV. Using the EIN alone would credit AEF with $162.6m in 2023 and DAFgiving360 with nothing.
  - "Other DAFRC-listed sponsors" uses the DAFRC sponsor file, matched by EIN.
- **`effective_take`.** Each measure is divided by the combined **Schedule M total**, not Part VIII line 1g. DF's TY2024 Part VIII non-cash figure ($504,655,205) includes the $448,854,853 cash transfer from DAT: it exceeds DF's own Schedule M total ($55,800,352) by exactly that amount. Benchmarks: 1%, 3%, 1.2%, 1.4% and $10,000 × the Schedule M count.
- **`routing_sponsor_to_dechomai_total`.** Sums of the sponsors' Schedule I lines to DAT or DF on the selected sponsor returns.
- **`dpn_fee_test`.** The verdict is decided by these rules, in order:
  1. "revenue" if program-service or other revenue is above 0;
  2. else "expense named to Chariot" if any contractor, Schedule I or text leaf names Chariot;
  3. else "unnamed expense about 2.9% of receipts" if Part IX "fees for services – other" is within ±0.5 percentage points of 2.9% of contributions;
  4. else "not visible at 2.9%".

### 2.4 Run
```
python3 scripts/mission_dechomai_dafpay.py . --irs-dir <IRS index dir> --work-dir <cache outside repo> \
        [--xml-dir <dir with {oid}.xml>] [--fetch]
```

### 2.5 Robots and access log (2026-11-19, UA `research-script/1.0`)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (none; S3 NoSuchKey) | XML mirror |
| apps.irs.gov | 503 on the first probe, 404 from the script run; no rules published | TEOS index and zip range reads (as in batches 31–38) |
| www.irs.gov | 200; disallows `/*/downloads/` and TEO search paths only | not fetched |
| www.dafpaynetwork.org | 200; `User-agent: *` → `Allow: /` (only PetalBot is blocked) | home page read |
| dechomai.org | 200; `Disallow:` (empty) | FAQ read |
| help.givechariot.com | 200 | not re-fetched; quotes from repo batch 38 |

No logins, forms or outreach. sec.gov, crt.sh and certspotter were not used.

---

## 3. Results: Dechomai (P-B40N14-01)

### 3.1 Return-level decomposition [F]

| Entity / TY | Contributions | of which non-cash (VIII 1g) | Schedule M total (gifts) | Forms 8283 | DAF accounts (Sch D) | DAF value EOY | Grants (IX l.1) | Schedule I total (lines) |
|---|---|---|---|---|---|---|---|---|
| DAT 2021 | $985.9m | $957.3m | $957.3m (214) | 94 | 144 | $267.7m | $374.0m | $393.7m (22) |
| DAT 2022 | $524.7m | $489.2m | $489.2m (121) | 25 | 158 | $1,123.5m | $475.0m | $475.0m (3) |
| DAT 2023 (amended) | $960.6m | $903.6m | $896.3m (124) | 79 | 173 | $1,662.1m | $337.5m | $337.5m (3) |
| DAT 2024 | $674.6m | $649.8m | $649.8m (169) | 87 | 314 | $1,432.2m | $552.3m | $552.3m (6) |
| DF 2021 | $172.3m | $158.6m | $158.6m (49) | 22 | 54 | $163.5m | $126.8m | **$404.9m** (48) |
| DF 2022 | $39.7m | $36.8m | $35.8m (32) | 25 | 60 | $146.7m | $22.0m | **$507.0m** (79) |
| DF 2023 | $351.3m | $33.5m | $30.1m (28) | 19 | 88 | $102.4m | $359.7m | $359.6m (56) |
| DF 2024 | $511.8m | $504.7m* | $55.8m (103) | 69 | 80 | $105.9m | $498.1m | $498.0m (89) |

\* This includes the $448.9m cash transfer from DAT (§2.3).

Per-category Schedule M rows (category, count, value, valuation method) are in the CSV as `record_type = sched_m`.

**Part VII-B contractors** [F]: Charitable Solutions LLC, "administrative services", Jacksonville FL. It is the only contractor over $100k, and it appears on DF's return only:

| Year | Payment |
|---|---|
| 2021 | $1,384,387 |
| 2022 | $2,998,459 |
| 2023 | $3,805,114 |
| 2024 | $4,425,428 |

- DAT reports no contractor over $100k in any year. Its 2024 Schedule O says: "ADMINISTRATIVE SERVICES ARE PROVIDED TO DECHOMAI ASSET TRUST BY CHARITABLE SOLUTIONS, LLC UNDER A CONTRACT WITH THE SUPPORTED ORGANIZATION, DECHOMAI FOUNDATION INC."
- DAT's Part IX management fees were $3,370,830 in 2024, so DAT apparently pays under DF's contract without listing the payee [I].
- Bryan Clontz is DF's non-voting board secretary and both entities' "books in care of" contact. The FAQ (Q9) refers to Dechomai's "administrative service providers" without naming them.

**Form 8282** [F]: Part V line 7c is "No" on all eight returns, and `Form8282FiledCnt` is blank. The text "8282" appears nowhere. The Schedule M line 32b narratives (identical each year) read: "Local professionals are engaged to sell real property. Legal experts and financial professionals assist in the sale of securities and interests in partnerships, S corporations, and C corporations." The 2024 DAT narrative changes to "engages third-party service providers to assist in the solicitation, receipt, processing, and/or sale of noncash contributions".

Part VIII line 7 securities sales are small relative to grants:
- DAT: gross $9.1m / $48.2m / $89.2m / $37.3m, with gains of +$9.1m / −$78.4m / −$125.3m / −$219.7m;
- DF: gross $2.5m / $23.0m / $40.7m / $9.4m.

[I] Most asset sales are therefore not reported as Part VIII line 7 sales. They are probably booked as investment-value changes or realised inside holding entities. The 990s do not show disposition-level data.

**In-kind grants** [F]: DAT 2024 granted Legacy Housing (LEGH) shares in kind: $45,942,000 to AEF and $7,661,000 to the University of Texas Law School Foundation, both at FMV.

### 3.2 Routing through Dechomai (Schedule I, combined DAT+DF, external lines only) [C]

| Sponsor group | 2021 | 2022 | 2023 | 2024 | 2021–24 | Share of external grants |
|---|---|---|---|---|---|---|
| DAFgiving360 | $111.4m | $119.5m | $76.4m† | $136.0m | **$443.2m** | 23.0% |
| Fidelity Charitable | $91.3m | $89.2m | $24.4m | $29.8m | **$234.7m** | 12.2% |
| AEF | $13.3m | $50.8m | $86.2m | $50.2m‡ | **$200.5m** | 10.4% |
| Goldman Sachs | $86.2m | $24.8m | $40.3m | $21.9m | **$173.2m** | 9.0% |
| NPT | $12.3m | $5.9m | $7.4m | $31.2m | **$56.8m** | 3.0% |
| Morgan Stanley GIFT | $1.4m | $2.1m | $33.5m | $0.5m | **$37.5m** | 2.0% |
| **Six groups** | $315.9m (72.9%) | $292.4m (57.7%) | $268.2m (70.2%) | $269.4m (44.8%) | **$1,145.9m** | **59.6%** |
| Other DAFRC-listed sponsors | $75.0m | $131.6m | $71.1m | $157.4m | $435.0m | 22.6% |
| External Schedule I total | $433.4m | $507.2m | $381.8m | $601.5m | $1,923.8m | 100% |

† Filed as "SCHWAB CHARITABLE TRUST" under AEF's EIN (name used).
‡ Includes $45.9m in LEGH shares.

- Among the other sponsors, the largest 2021–24 recipients are Vanguard Charitable ($121.5m), Bank of America Charitable Fund ($74.4m), Santa Barbara Foundation ($72.3m), Edward Charles Foundation ($19.3m), Raymond James Trust ($18.8m) and ImpactAssets ($18.1m).
- **Scale against intake:** six-group grants equal 35.0% of the $3,272.9m of Schedule M intake over the same four years. Grants lag sales by months to years, so this is an order of magnitude and not a matched cohort [I].
- **Schedule I vs Part IX** [F/U]: DF's Schedule I exceeds its Part IX grants by $278.1m (2021) and $484.9m (2022), the same two years in which DF did not book DAT's transfers as revenue. The routing table uses Schedule I as filed (P-B40N14-03).

### 3.3 Sponsor-side view (sponsor Schedule I lines to DAT or DF) [F]

| Sponsor (return) | Lines to Dechomai |
|---|---|
| DAFgiving360 FY6/21–FY6/25 | to DAT: $753,882; $12,293,150; $25,501,739; $15,063,017; $19,483,763 (total $73.10m). To DF: $24,200 (FY6/23) and $150,990 (FY6/24) |
| Fidelity FY6/21–FY6/25 | to DAT: $190,000 (FY6/21); **$56,727,821 non-cash "SECURITIES"** (FY6/22); $117,000 (FY6/25). To DF: $197,000 (FY6/22). None in FY6/23 or FY6/24 |
| AEF CY2021–24 | to DAT: $4,800,731 (2022); $9,500 (2023) |
| Goldman Sachs PF CY2021–24; GS Charitable Gift Fund FY6/21–FY6/25 | PF to DAT: $750,000 (2023); $1,250,000 (2024). Gift Fund: none |
| Morgan Stanley GIFT CY2021–24 | to DAT: $115,000 (2023); $80,000 (2024) |
| NPT FY6/21–FY6/25 | to DF: $286,031 (FY6/24); $167,500 (FY6/25) |
| **Total** | **$137,961,324** |

- **Schedule B** is redacted ("RESTRICTED") on every public return read, so contributions *from* the sponsors cannot be seen in Dechomai's Schedule B.
- **Fidelity's original FY6/22 return** (202321309349304807) swapped the name and EIN on the $197,000 grant. It shows a "HILLSONG CHURCH USA INC" line with DF's EIN and a "DECHOMAI FOUNDATION INC" line with EIN 98-0670900. The amended return (202430459349302913) corrects this.

### 3.4 Effective take vs the published fee [C]

Each cell shows the amount and its share of combined Schedule M intake.

| Measure | 2021 | 2022 | 2023 | 2024 | 2021–24 |
|---|---|---|---|---|---|
| Charitable Solutions (VII-B) | $1.38m (0.12%) | $3.00m (0.57%) | $3.81m (0.41%) | $4.43m (0.63%) | **$12.61m (0.39%)** |
| Part IX management + other fees | $1.39m (0.12%) | $3.77m (0.72%) | $4.44m (0.48%) | $10.32m (1.46%) | $19.92m (0.61%) |
| All Part IX fees for services | $1.50m (0.13%) | $3.92m (0.75%) | $4.49m (0.48%) | $10.36m (1.47%) | $20.27m (0.62%) |
| All non-grant expenses | $15.64m (1.40%) | $10.70m (2.04%) | $9.72m (1.05%) | $12.92m (1.83%) | $48.98m (1.50%) |
| *DAT Sch R "admin reimbursement" (unreconciled)* | *$60.6m (5.4%)* | *$115.1m (21.9%)* | *$87.8m (9.5%)* | *$80.9m (11.5%)* | *$344.5m (10.5%)* |
| Published 1% / 3% | | | | | $32.7m / $98.2m |
| FAQ average 1.2% / 1.4% | | | | | $39.3m / $45.8m |
| $10,000 minimum × 840 gifts | | | | | $8.4m (0.26%) |

**Reading** [I]:
- On expense lines the take is 0.4–0.6% of intake for administration and up to 1.5% for all non-grant costs. Non-grant costs also include items that are not fees, such as the CGA programme's annuity death benefits ($361k in 2024) and insurance ($906k).
- The Charitable Solutions and Part IX fee measures (0.39–0.62%) sit below the published 1–3% band and below the FAQ's 1.2–1.4% average. All non-grant expenses (1.50%; 2.04% in 2022 and 1.83% in 2024) sit inside the band and above that average. None of these is the fee charged, because retained fees do not appear in Part IX [V wave 37B]
- The FAQ says at least half of collected fees go to "operating reserves or unrestricted fund purposes". A retained fee is a transfer from a donor's DAF account to Dechomai's own unrestricted funds, and it would not appear in Part IX. If half the fee is retained and the other half pays Charitable Solutions, the Charitable Solutions payments of 0.39% imply fee income of roughly 0.8% or more.
- The $10,000 minimum binds only for gifts under about $333k–$1m. With average gifts of $3.9m, it adds little in aggregate: $8.4m, or 0.26%, if every gift paid only the minimum.
- **Not resolved:** whether DAT's Schedule R reimbursements are fees, pass-through sale costs or misclassified grants. DF's own Schedule R does not show matching receipts.

**Fee sources** [F]:
- [dechomai.org/faqs](https://dechomai.org/faqs/), Q8 (read 2026-11-19): "Dechomai Foundation will charge between 1 and 3 percent for each donation (average fee is usually 1.2-1.4%), based on the size and complexity of the asset… Note that at least 50% off all collected fees are used for operating reserves or unrestricted fund purposes."
- Q7: "Dechomai does not have a minimum size donation (individual donations have averaged between $3-7 million each year), however, there is a minimum fee of $10,000".
- The undated one-pager in the repo (direction-noncash-gift-infrastructure §2.7) says "1-3% WITH MINIMUM FEE OF $10,000".

---

## 4. Results: DAFpay Network (P-B38C-01)

### 4.1 Return availability
- **TY2025** (period ending 2025-12-31; ReturnTs 2026-05-18T19:51:48-06:00; IRS index submission year 2026) is **public**. It is in IRS TEOS zip `2026_TEOS_XML_05B` (the index labels it 05A) and is not in the GivingTuesday mirror as of 2026-11-19.
- The return was read in full. Its header does not say "filed 2026-05-19" (the ReturnTs is 05-18 Mountain time, which is 05-19 UTC).

### 4.2 Parts VIII–IX, Schedule I, Schedule O [F]

| Line | TY2024 (202510729349301206) | TY2025 (202621389349300637) |
|---|---|---|
| Contributions (VIII 1h; all "all other") | $1,199,247 | $2,941,073 |
| Program-service revenue | $0 | $0 |
| Other revenue | $0 | $0 |
| Investment income | $4,123 | $11,137 (coded unrelated; UBI $11,137, net UBTI $0) |
| Grants to domestic orgs (IX l.1) | $831,404 | $2,178,671 |
| Fees for services – accounting | $6,000 | $400 |
| **Fees for services – other** | **$18,345 (1.53% of contributions)** | **$88,736 (3.02%)** |
| Information technology | — | $16,706 |
| Other: "Provision For Audit Fees" | — | $6,500 |
| Total expenses | $855,749 | $2,291,013 (all program) |
| Net assets EOY | $348,147 | $1,009,344 |
| Schedule I lines (≥$5,000) | 6 lines, $584,066 (70.3% of IX l.1) | 104 lines, $1,324,158 (60.8%) |
| Largest Schedule I recipients | Chai Lifeline $372,832; Effective Ventures Foundation $155,818 | MD Anderson Cancer Center $116,893; NoticeAbility $77,680; KLove $53,300; Jubilee Gift Galaxy $48,525 |
| Part VII-B contractors | none | none |
| "Chariot" anywhere in the return | no | no |
| Schedule A public support | n/a | 48.17%. Contributions over the 2% limit: $2,138,755 |

Schedule O (TY2025) has three entries: two boilerplate lines (Form 990 and documents available on request) and the continuation of the Part III mission (§4.3).

### 4.3 Where the 2.9% shows up [C/I]

| Test | TY2024 | TY2025 |
|---|---|---|
| As DPN revenue (PSR or other revenue > 0) | No | No |
| As an expense **named** to Chariot Giving Inc (contractor, Schedule I, any text) | No | No |
| 2.9% × contributions | $34,778 | $85,291 |
| "Fees for services – other" minus 2.9% | −$16,433 | **+$3,445** |
| Verdict (script rule) | not visible at 2.9% (netted before receipt, outside DPN, or covering only part of the year) | **unnamed expense of about 2.9% of receipts** |

**Interpretation** [I]:
- In TY2025 DPN appears to receive DAF grants gross and book the DAFpay fee as "fees for services – other". The payee is not disclosed (below the $100k Part VII-B threshold).
- This matches Chariot's nonprofit terms, which allow Chariot to "have DAFpay Network deduct DAFpay Fees as governed by its relationship with the DAFpay Network for payments to Non-User Nonprofits" (terms snapshot 2026-11-14).
- TY2024's 1.53% does not fit a full 2.9% fee. Possible explanations, which cannot be distinguished from the filing:
  - fee-free subscription volume;
  - the 5 Jewish-giving platforms' own fee agreements (the help page says platform agreements override 2.9%);
  - netting before receipt for part of the year.
- The batch-38 conclusion that DPN "books no fee revenue" still holds for revenue. Its corollary, that the fee is taken before DPN records the contribution, **is revised for TY2025**: an expense of about 2.9% is now on DPN's books.

**Self-description** [F]:
- Part I line 1 / Part III (Schedule O continuation): "THE CHARITY OPERATES AS A SPONSOR TO DONOR ADVISED FUNDS. FOR EACH FUND, THE FUND WILL BE SEPARATELY IDENTIFIED BY REFERENCE TO THE CONTRIBUTIONS OF SPECIFIED DONOR OR CLASSES OF DONORS, SUCH THAT IT IS DISTINGUISHABLE FROM THOSE FUNDS THAT MAY BE POOLED ANONYMOUSLY OR THE GENERAL FUND OF THE CHARITY. UPON CONTRIBUTION, THE DONOR CEDES ALL LEGAL TITLE TO THE CONTRIBUTED FUNDS TO THE CHARITY, WHICH MAINTAINS FULL DISCRETION AND CONTROL OVER THE FUNDS IN EACH DISTINGUISHABLE ACCOUNT."
- Against that:
  - Part IV line 6 (DAFs) is **No** in both years, and no Schedule D is filed.
  - Part IV line 21 (grants to organizations over $5,000) is "No" in TY2025 even though a 104-line Schedule I is attached.
- Other facts from the return:
  - Formed 2023, Iowa.
  - Three unpaid directors: Salomon Serfati (principal officer, 20 h/week), Yitzhak Moshe Bengualid Goldstein, Laivi Forta.
  - Cash-basis accounting, no audit or review.
  - Preparer field: "AT&F International INC" (TY2025), "JK ANF LLC" (TY2024).
- **Website** ([dafpaynetwork.org](https://www.dafpaynetwork.org/), read 2026-11-19): "DAFpay Network is a 501(c)3 nonprofit organization that facilitates safe, easy and fast charitable donations between Donor Advised Funds (DAFs) and the 1.5 million 501(c)3) nonprofit organizations… We enable nonprofits to easily receive more DAF gifts powering dedicated DAF fundraising solutions from Chariot."
- **Conclusion** [I]: legally, DPN describes itself as a sponsor that takes title. In practice it acts as a pass-through facilitator for Chariot, and its own Part IV answers say it holds no DAFs.

---

## 5. Limits
- **Fiscal-year mismatch.** Dechomai files on a calendar year. DAFgiving360, Fidelity, NPT and the GS Charitable Gift Fund file to June. The sponsor-side totals cover FY6/21–FY6/25 and are not matched to Dechomai years.
- **Schedule I covers only grants over $5,000 and records only what the filer typed.** One EIN error (Schwab under AEF's EIN) was corrected by name, and others may exist. Name matching is restricted to the six target groups.
- **Schedule M records gifts at FMV when received.** Grants follow sales by weeks to years (FAQ: a third sell within 6 months, a third in 6–24 months, a third after 24 months). Annual take ratios therefore mix cohorts; the four-year total is the better comparison.
- **No disposition-level data.** Neither Form 8282 nor Form 8283 is public. Part V line 7c covers tangible personal property only.
- **Unreconciled figures:** DAT's Schedule R reimbursements ($344.5m) and DF's Schedule I vs Part IX gaps in 2021–22. The consolidated audit was not obtained.
- **DPN fee payee** is not named. The 2.9% match is arithmetic. A single year fits and TY2024 does not.
- **Sources outside this pass:** the Chariot help-page quotes come from repo batch 38 (read 2026-11-15) and were not re-fetched. ProPublica was not used.

---

## 6. Data dictionary: `dechomai-dafpay-2026-11-19.csv`

| Column | Meaning |
|---|---|
| record_type | Row kind (see the table below) |
| entity | Filer name (Dechomai Asset Trust, Dechomai Foundation Inc, DAFpay Network Inc, a sponsor group name, or "Dechomai combined (DAT+DF)") |
| ein | Filer EIN, 9 digits (combined rows: `260724604;061676688`) |
| tax_year | First four digits of the IRS index TAX_PERIOD (sponsor June filers: the year the period ends). `2021-2024` / `FY2021-FY2025` for multi-year totals |
| tax_period_end | TaxPeriodEndDt from the XML (sponsor rows: index TAX_PERIOD yyyymm) |
| object_id | IRS e-file object id |
| selected | 1 = the version used (latest ReturnTs per EIN and tax period); 0 = superseded |
| item | Line or measure name (e.g. `noncash_contributions`, `part_ix_FeesForServicesOtherGrp`, Schedule M group tag, Schedule R type code, contractor service, Schedule I purpose) |
| category | Schedule M category label; for Schedule I rows, the recipient's DAFRC type (`DAFRC National` etc.) or `DECHOMAI_INTRA` |
| count | Number of items (Schedule M contributions, lines, gifts) |
| amount_usd | Main amount in USD (Schedule I: cash grant) |
| amount2_usd | Second amount (Schedule I: non-cash grant; effective_take: the denominator, the Schedule M total) |
| ratio | Computed share (definition in `text`) |
| counterparty | Recipient, contractor or related organisation; for Schedule M rows, the asset class |
| counterparty_ein | Recipient EIN as filed |
| sponsor_group | One of the six requested groups, if matched (name first, then EIN) |
| text | Free text from the filing (valuation method, non-cash description, narrative, mission, header JSON) or a computation note |
| source_url | XML URL (GivingTuesday mirror or IRS TEOS zip) |

**Record types:**

| Type | Content |
|---|---|
| return_line | Part VIII/IX/balance-sheet values, Schedule D Part I, Form 8283 count, Schedule I line count and total |
| return_flag | Header JSON, Part IV lines 6 and 21, mission, Schedule B redaction, schedules filed, mentions of "Chariot" |
| form8282 | Part V 7c flag and 7d count; mentions of "8282" |
| sched_m / sched_m_flag / sched_m_note | Schedule M categories; lines 31–33; narratives |
| sched_i | Every Schedule I line (Dechomai and DPN) |
| contractor | Part VII-B |
| sched_r_txn | Schedule R Part V transactions (type code in `item`) |
| sched_o | Schedule O entries |
| sponsor_scan / sponsor_to_dechomai | One row per sponsor return scanned, plus each Schedule I line to DAT or DF |
| dechomai_year | Combined yearly and four-year flows |
| asset_mix | Schedule M by asset class |
| routing_dechomai_to_sponsor | Grants by sponsor group |
| routing_sponsor_to_dechomai_total | Sponsor to Dechomai totals |
| effective_take | Take measures and published benchmarks |
| dpn_fee_test | DPN 2.9% tests and verdict |

---

## 7. Source register

| ID | Source | Date | Used in |
|---|---|---|---|
| S1 | IRS TEOS index: https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv (and index_2021..2025) | local copies, 2026-11-14/15 | §2.1 |
| S2 | DAT TY2021–24: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202243199349331259_public.xml ; …/202313199349315151_public.xml ; …/202403229349300510_public.xml (amended) ; …/202413199349316041_public.xml (original) ; …/202523159349304782_public.xml | filed 2022-11-15 to 2025-11-11 | §3 |
| S3 | DF TY2021–24: …/202223199349330962_public.xml ; …/202343179349310654_public.xml ; …/202403199349315905_public.xml ; …/202543159349304249_public.xml | filed 2022-11-15 to 2025-11-11 | §3 |
| S4 | DPN TY2024: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202510729349301206_public.xml | 2025-03-13 | §4 |
| S5 | DPN TY2025: member 202621389349300637_public.xml in https://apps.irs.gov/pub/epostcard/990/xml/2026/2026_TEOS_XML_05B.zip | ReturnTs 2026-05-18 | §4 |
| S6 | Sponsor returns (Schedule I), mirror URLs `…/XmlFiles/{oid}_public.xml`. Fidelity 202221339349302787, 202430459349302913 (amended FY6/22; original 202321309349304807), 202441369349301334, 202521349349310887, 202601389349301700. DAFgiving360 202230499349301028, 202201119349300745, 202330939349300403, 202411039349301716, 202541069349300729, 202611199349300601. AEF 202222949349301137, 202332499349300338, 202442479349301654, 202513219349310376. GS PF 202243089349301314, 202312859349302266, 202413109349303336, 202503109349303645. GS CGF 202201039349301630, 202311099349301951, 202421169349301122, 202511119349301416, 202611249349302616. MS GIFT 202203199349314745, 202302999349301010, 202403209349313980, 202503239349300435. NPT 202231339349309863, 202311359349313966, 202431429349301368, 202511339349301311, 202601289349302480 | 2021–2026 | §3.3 |
| S7 | Dechomai FAQs: https://dechomai.org/faqs/ (Q7, Q8, Q11) | read 2026-11-19 | §3.4 |
| S8 | DAFpay Network home page: https://www.dafpaynetwork.org/ | read 2026-11-19 | §4.3 |
| S9 | Chariot nonprofit terms, "DAFpay Fees": https://www.givechariot.com/legal-nonprofit (repo snapshot `data/terms-snapshots/chariot-nonprofit-terms/2026-11-14.txt`) | fetched 2026-11-14 | §4.3 |
| S10 | Chariot help, DAFpay Network: https://help.givechariot.com/dafpay/dafpay-network.md (quoted via repo batch 38) | read 2026-11-15 | §4.3 |
| S11 | DAFRC sponsor list (repo `dafrc-sponsor-schedule-d-fy2019-2024.csv`; original https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) | 2025 edition | §2.3 |
| S12 | Repo context: `g1913-processor-disbursement-rules.md` (DEC rows), `direction-noncash-gift-infrastructure.md` §2.7, `queue-batch38-closeout-checks.md` §4, `daf-to-daf-flows-990.csv` | 2026-11 | §1, §4 |

**Consistency with repo** [C]: every sponsor-to-Dechomai line in `daf-to-daf-flows-990.csv` is reproduced exactly. This pass adds two FY6/21 lines that file does not carry (DAFgiving360 $753,882; Fidelity $190,000) and the TY2021 Charitable Solutions payment ($1,384,387).
