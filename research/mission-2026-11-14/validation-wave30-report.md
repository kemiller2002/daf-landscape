# Validation wave 30: new directions N31–N33 (foreign grants on Schedule F, recipient lobbying, the long tail of sponsors)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave30.
**Register:** [`validation-register-wave30.csv`](../../data/mission-2026-11-14/validation-register-wave30.csv), rows V30-01 to V30-38.
**Documents validated:**
- N31: [direction-foreign-grants-schedule-f.md](direction-foreign-grants-schedule-f.md), `daf-foreign-grants-schedule-f-2023-2024.csv` (3,199 rows) and `scripts/mission_foreign_grants.py`
- N32: [direction-recipient-lobbying.md](direction-recipient-lobbying.md), `daf-recipient-lobbying-2023-2024.csv` (18,441 rows) and `scripts/mission_recipient_lobbying.py`
- N33: [direction-long-tail-sponsors.md](direction-long-tail-sponsors.md), `daf-long-tail-sponsors-fy2021-2024.csv` (1,585 rows) and `scripts/mission_long_tail.py`

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching anything from it:
- `gt990datalake-rawdata.s3.amazonaws.com` returned 404 (`NoSuchKey`), so it has no rules;
- `www.irs.gov` was read, and `/pub/` is not disallowed. From it I fetched only `/pub/irs-pdf/f990ez.pdf` and HEAD requests for `/pub/irs-soi/eo1.csv`–`eo3.csv`;
- `apps.irs.gov/robots.txt` redirects to a 404 page. I made no other request to that host; the TEOS index files are the session's earlier copies.

**I did not use crt.sh.** For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The work was:
- **N31:**
  - a **re-run of the script** in a scratch copy of the repo with an **empty extract cache** and `--fetch`. All 100 sponsor returns and 18 intermediary returns were re-streamed from the mirror;
  - an **independent regex parse** of the XML for NPT (FY2023 and FY2024), SVCF (FY2023 and FY2024) and CAF America (FY2023 and FY2024);
  - my own aggregation of the `sponsor_year` rows.
- **N32:**
  - a **full re-run** with an **empty return cache**: 13,011 recipient returns were fetched from the mirror again;
  - an independent parse of **19 recipients' full returns** (Schedule C and Part IV), in a stratified random sample;
  - the Form 990-EZ PDF.
- **N33:**
  - a **re-run of the script**;
  - my own banding from the CSV;
  - the XML of Givinga (amended TY2024) and BNY Mellon CGF (TY2024);
  - the BMF file dates.

## Headline

The three documents hold up. Of 38 claims, 34 are confirmed and 4 partially confirmed. None is contradicted or unverifiable. **All three scripts reproduce from fresh primary data:**
- N31: every cell matches except the provenance column `via`;
- N32: the same rows as a set, and a JSON summary identical except `via`;
- N33: byte-identical.

**What holds independently:**
- **N31 foreign grants (Schedule F / Part IX line 3):**
  - **$1,890.8m of $98,265.4m = 1.92%** (main scope). FY2023 $845.0m (1.86%); FY2024 $1,045.8m (1.98%).
  - NPT holds 39.3%, SVCF 18.6% and GS DAPF 9.5%; the top 3 hold 67.4% and the top 10 96.1%.
  - Fidelity is 0.495% of its own grants. By sponsor type: national 1.75%, community foundations 2.60%, single-issue 1.98%.
  - Europe 49.6% and MENA 12.4% (NPT supplies 35.0% of the Europe dollars, SVCF 25.7%).
  - Named intermediaries received $215.6m gross, with about $164.7m estimated to pass abroad. CAF America's own foreign share is 36.06% in its XML. Friends-of recipients received $432.9m.
  - Part II line 2: 2,543 vs 672. SVCF's "other" counts are 231 and 308 in the XML.
- **NPT FY2024 column shift (V30-08): confirmed in the XML.**
  - None of the 488 Part II lines carries `PurposeOfGrantTxt`. The NTEE-style purpose labels ("HUMAN SERVICES", "CULTURE & ART", "RELIGION", "INTERNATIONAL") sit in `MannerOfCashDisbursementTxt`, and "WIRE TRANSFER" sits in `ValuationMethodUsedDesc`.
  - The lines sum to $410,303,258, against Part IX line 3 of $410,629,568. The script's repair is correct.
- **International sector share: the 7.8% revision holds (V30-11).**
  - NTEE Q plus direct foreign grants = (4,315.2 + 1,890.8) ÷ (77,343.7 + 1,890.8) = **7.83%**, or 8.14% on the broad definition, against 5.58% for NTEE Q on Schedule I alone.
- **N32 recipient lobbying:**
  - Coverage is 71.15% of $77.34bn. 42.16% of covered dollars go to recipients reporting lobbying, with bounds of 30.0% and 58.8%. By count the share is 20.0%.
  - By sector: environment 61.0%, education 54.7%, health 50.5%, religion 6.9%. By sponsor type: national 45.9%, community foundations 34.7% (39.5% excluding SVCF), single-issue 31.0%.
  - The maximum lobbying intensity is 16.1%, and no recipient is above 20%.
  - Political campaign activity: 36 of 12,985 recipients, receiving $73.5m (0.133% of covered dollars).
  - Using the return-year alternative gives the same answer for 97.1% of dollars.
  - **All 19 spot-checked returns match** on status, lobbying amount, expenses and Part IV lines 3–4.
  - The 990-EZ note matches the form text: line 46 leads to Schedule C Part I, and line 47 to Part II.
  - **The language is neutral.** No recipient is described by viewpoint, recipients are not named in the findings, and the CSV carries EINs only.
- **N33 long tail:**
  - 1,240 of 1,514 sponsors, holding $9.18bn (2.84%). Under $10m: 947 sponsors (0.69%). Under $1m: 423 sponsors (0.04%). The top 50 hold 85.5%.
  - The tail holds 46.4% of accounts, but only 3.49% without Givinga and BNY. Givinga's amended return reports 1,421,011 DAFs on $1,949,239. BNY reports $725.6m of grants, including $619.8m to RCF, on $4.7m of assets.
  - Median age is 29. The median tail sponsor has 24 DAFs and a $133k average account, against 1,464 and $836k in the top 50.
  - Payout is 11.7% against 19.6%; 26.8% of the tail pay out under 5% (37.6% under $1m).
  - Entries 134 of 138 and exits 85 of 90, with tiers A 9, B 49, C 14 and D 13.
  - Foundant has 282 of the 351 identified tail CFs (80.3%), and 37.8% of tail CFs are unmapped.
  - §5 is labelled inference throughout.

**What needs correcting or qualifying:**
1. **N31 ED/ER scope label (V30-12).** §0 gives "41 of 70 sponsor-years, 94.7%" under the main-scope heading, but these are the all-top-50 figures. In the main scope it is 41 of 68 and 96.0%. §3.6 is labelled correctly.
2. **N31 size of the understatement (V30-11).** The gap is 2.2–2.6 points against the published 5.6%, or 2.4–2.7 points like-for-like (NTEE Q is 5.45% on the Schedule I + line 3 base). The document says 2.2–2.5.
3. **N32 intensity base (V30-22).** The printed quantiles (median 0.20%) are over **2,531** lobbying recipients with a computable ratio, 57 of them at 0, not the 2,474 with a positive ratio. Over the 2,474 the median is 0.21% (p25 0.041%, p75 0.79%). The "low intensity" reading is unaffected.
4. **N33 BMF copy date (V30-37).** The version (Last-Modified 2026-11-09) is right. But eo1–eo3, the files that hold most EINs, are copies saved on 2026-11-14 and symlinked into the BMF directory. Only eo4, eo_pr and eo_xx were saved on 2026-11-15.
5. **Minor wording:**
   - **N33 §3.6:** "a third of tail CFs" show no vendor; the figure is 37.8%.
   - **N33 exits:** the 85 exits under $50m include 4 whose last filed value was $0.
   - **N32 data file:** tied recipient rows are not in a stable order between runs. This is cosmetic.

## Limits

- **Not re-checked:**
  - N31: the Part V keyword flags were not re-read sponsor by sponsor. The purpose and region keyword tables were not re-derived. The friends-of regex was not audited name by name.
  - N32: the BMF classification of the 2,844 recipients with no return (churches, governmental units and so on) was not audited by hand. The 18 HTTP 404 returns were not looked for elsewhere.
  - N33: the vendor map and exit-verification tiers were taken from repo files without re-verifying websites. The Part VII-B lines were not re-read from XML.
- **Shared inputs:** all three scripts share the session's BMF, line cache and netpayout990 cache. My re-runs test reproducibility and the XML parse, not those upstream inputs, which earlier waves validated (24A, 27, 29).
- **Pages change.** The form text was read on 2026-11-15.

## Exact corrections

### `research/mission-2026-11-14/direction-foreign-grants-schedule-f.md`
1. **§0, ED vs ER row.**
   - **Find:** "**Part V narratives:** of the 70 sponsor-years with foreign grants, 41 describe ED and/or ER (31 ED, 27 ER). Together they hold 94.7% of the foreign dollars [C]."
   - **Replace with:** "**Part V narratives:** of the 70 top-50 sponsor-years with foreign grants (68 in the main scope), 41 describe ED and/or ER (31 ED, 27 ER). Together they hold 94.7% of all top-50 foreign dollars, or 96.0% in the main scope [C; V wave 30]."
2. **§0, comparison with the NTEE sector analysis.**
   - **Find:** "**International is therefore understated by about 2.2–2.5 points in the Schedule-I-only sector shares.**"
   - **Replace with:** "**International is therefore understated by about 2.2–2.6 points against the published 5.6% (2.4–2.7 points like-for-like, since NTEE Q is 5.45% on the Schedule I + line 3 base) in the Schedule-I-only sector shares** [C; V wave 30]."

### `research/mission-2026-11-14/direction-recipient-lobbying.md`
1. **§0, lobbying intensity row.**
   - **Find:** "Among recipients reporting lobbying with an amount: median **0.20%**, 75th percentile 0.76%, 90th 2.1%, 99th 7.0%, maximum 16.1%."
   - **Replace with:** "Among the 2,531 recipients reporting lobbying with a computable ratio (57 of them at $0): median **0.20%**, 75th percentile 0.76%, 90th 2.1%, 99th 7.0%, maximum 16.1%. Over the 2,474 with a positive amount the median is 0.21% [C; V wave 30]."
2. **§2.3, quantiles.**
   - **Find:** "- **Quantiles** among those 2,474: p10 0.006%, p25 0.036%, **median 0.20%**, p75 0.76%, p90 2.1%, p99 7.0%."
   - **Replace with:** "- **Quantiles** among the 2,531 lobbying recipients with a computable ratio (the 2,474 above plus 57 Part II-B filers reporting $0): p10 0.006%, p25 0.036%, **median 0.20%**, p75 0.76%, p90 2.1%, p99 7.0%. Over the 2,474 with a positive ratio: p25 0.041%, median 0.21%, p75 0.79% [C; V wave 30]."

### `research/mission-2026-11-14/direction-long-tail-sponsors.md`
1. **§1.2, BMF copy.**
   - **Find:** "  - The copy was saved earlier in this session on 2026-11-15 under the `/pub/irs-soi/` path, which earlier batches fetched after the robots check. This run made no request."
   - **Replace with:** "  - The copy was saved earlier in this session under the `/pub/irs-soi/` path, which earlier batches fetched after the robots check: eo1–eo3 on 2026-11-14 and eo4, eo_pr and eo_xx on 2026-11-15. Both dates postdate the files' Last-Modified of 2026-11-09, so the content is that version [V wave 30]. This run made no request."
2. **§3.6, reading.**
   - **Find:** "- A third of tail CFs, and two-thirds of those under $1m, show no vendor at all."
   - **Replace with:** "- Over a third of tail CFs (37.8%), and two-thirds of those under $1m, show no vendor at all [V wave 30]."
3. **§3.5, exits.**
   - **Find:** "**Exits (candidate exits dated FY2021–23: 90; 85 had less than $50m at the last filing):**"
   - **Replace with:** "**Exits (candidate exits dated FY2021–23: 90; 85 had less than $50m at the last filing, 4 of them $0):**"

### `research/mission-2026-11-14/direction-recipients-impact-matching.md`
1. **§0, sector row.**
   - **Find:** "- environment/animals 5.7%; arts 5.6%; international 5.6%;"
   - **Replace with:** "- environment/animals 5.7%; arts 5.6%; international 5.6% (Schedule I only; adding the top 50's direct foreign grants from Form 990 Part IX line 3 / Schedule F raises international to 7.8% of Schedule I + foreign grants, per direction-foreign-grants-schedule-f.md [V wave 30]);"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **§11.20, sector-share sentence (N1–N4 paragraph).**
   - **Find:** "and 13.6% to religion, with the top 100 recipients taking 24.3%."
   - **Replace with:** "and 13.6% to religion, with the top 100 recipients taking 24.3%. Schedule I shows international recipients (NTEE Q) at 5.6%, but direct foreign grants (Part IX line 3 / Schedule F, $1.89bn) sit outside Schedule I. Including them, international is 7.8% of Schedule I plus foreign grants [V wave 30]."
2. **New subsection after §11.26.** Add "### 11.27 New directions N31–N33 (validated, wave 30)", containing the paragraph below. If §11.27 is already taken, use the next free number.

   > **New directions N31–N33 (validated, wave 30).**
   > - **Foreign grants (Form 990 Part IX line 3 and Schedule F, top 50, FY2023–24; reproduced from a fresh download of all 118 returns).**
   >   - Direct foreign grants are **$1.89bn of $98.27bn, 1.92%** ($845m in FY2023, $1,046m in FY2024).
   >   - NPT gives 39% of the dollars, SVCF 19% and GS DAF 9.5%. Fidelity sends 0.5% of its grants abroad directly.
   >   - Community foundations 2.60%, nationals 1.75%. Europe takes 49.6% and the Middle East and North Africa 12.4%.
   >   - Narratives describing equivalency determination or expenditure responsibility cover 41 sponsor-years and about 95% of foreign dollars.
   >   - SVCF reports 539 of the 672 foreign recipients not shown to be 501(c)(3)-equivalent.
   >   - Nine US intermediaries received $216m, of which about $165m is estimated to have gone abroad. "Friends of" organisations received $433m.
   >   - NPT's FY2024 Schedule F has shifted columns ($410m, verified in the XML and repaired).
   >   - Adding direct foreign grants lifts the international share of DAF grants from 5.6% (Schedule I, NTEE Q) to 7.8%.
   > - **Recipient lobbying (Schedule C, top-50 recipients; reproduced from a fresh download of 13,011 returns; 19 returns hand-checked).**
   >   - Of $77.3bn of net DAF grants, 71.2% go to recipients with a parseable 501(c)(3) return. Of those covered dollars, **42.2% go to recipients that report any lobbying** (30.0–58.8% of all dollars). By count the share is 20%.
   >   - The share is highest for environment (61%), education (55%) and health (51%) recipients, and lowest for religion (7%, mostly uncovered churches). It is 45.9% at national sponsors and 34.7% at community foundations.
   >   - Lobbying is a small part of recipients' spending: median 0.20% of expenses, and none above 20%.
   >   - 36 of 12,985 recipients (0.13% of covered dollars) disclose political campaign activity. These are self-disclosures needing review.
   >   - Schedule C is self-reported. The measure describes recipients, not the use of DAF grants.
   > - **The long tail (corrected DAFRC panel, FY2021–24; reproduced exactly).**
   >   - 1,240 of 1,514 sponsors hold under $50m: $9.18bn, 2.84% of assets. 947 hold under $10m (0.69%) and 423 under $1m (0.04%). The top 50 hold 85.5%.
   >   - Without Givinga and the terminated BNY Mellon fund, the tail's 46.4% of accounts is 3.49%.
   >   - Half the tail sponsors are community foundations; the median tail sponsor is 29 years old.
   >   - The median tail sponsor has 24 DAFs averaging $133k (top 50: 1,464 and $836k). Its median payout is 11.7% (top 50: 19.6%), and 26.8% pay out under 5% (37.6% under $1m).
   >   - 134 of the 138 FY2021–24 entrants and 85 of the 90 candidate exits are in the tail.
   >   - Foundant serves 80% of tail CFs with an identified vendor, and 38% show none.
   >   - No tail sponsor has a published fee in the repo. AI-native implications are inference only.

## Data-file notes (not .md; for the owning agent)

- **`daf-foreign-grants-schedule-f-2023-2024.csv`:** no value changes. The `via` column depends on whether local XML copies are supplied, so it is run-specific provenance, not data.
- **`daf-recipient-lobbying-2023-2024.csv`:** no value changes. Consider sorting recipient rows by (net dollars desc, EIN) so that re-runs are byte-stable; 795 lines currently swap among ties.
- **`daf-long-tail-sponsors-fy2021-2024.csv`:** no value changes.
