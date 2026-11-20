# Validation wave 43B: OJC Fund audit, Groundswell accounts and de facto fiscal sponsors

**Date:** 2026-11-20 · **Validator:** validator wave 43B · **Corrections:** 23 exact corrections (§ Exact corrections) · **Register:** [`data/mission-2026-11-14/validation-register-wave43b.csv`](../../data/mission-2026-11-14/validation-register-wave43b.csv) (19 rows, V43B-01 to V43B-19)

**Studies validated**
1. [b4026-0601-01-p0503-ojc-groundswell.md](b4026-0601-01-p0503-ojc-groundswell.md), with its CSV and `scripts/mission_ojc_groundswell.py`. It proposes 12 corrections tagged [ojc-gs].
2. [g0503-03-de-facto-fiscal-sponsors.md](g0503-03-de-facto-fiscal-sponsors.md), with its CSV, `scripts/mission_de_facto_fiscal_sponsors.py`, its summary JSON and its 30-line hand-check sample. It proposes no exact corrections.

**Method**
- Both scripts were re-run from the caches, with output sent to the scratchpad (`--out`, `--sample-out`). No repo file was written by the re-runs; md5 checks before and after confirm this.
- Independent checks were written separately from the authors' code:
  - OJC: the two Schedule I line caches were read directly; recipient EINs were joined to the BMF; DAF and federation names were screened among FOUNDATION 10 recipients; the frame was rebuilt to type OJC's block lines on both filed and BMF names.
  - Groundswell: the amended TY2024 XML tags were read from the cached copy; the terms of use were re-fetched live.
  - Fiscal sponsors: the JSON, CSV and detections were re-tallied; hosts were checked against the keyed list, the cached directory page, the DAFRC dataset and the repo's DAF-to-DAF whitelist; four host home pages were read.
- **robots.txt** (user agent `research-script/1.0`, 2026-11-20): www.groundswell.io 200, `Disallow:` empty; assetsundermovement.org 200, `Disallow:` empty; possibilitylabs.org 200, `Disallow:` empty; www.commoncounsel.org 200, disallows /admin/ and /includes/ only, crawl-delay 10 respected; ctwo.org 200, no relevant Disallow; www.globalgiving.org 200 (not fetched beyond robots). web.archive.org gave no response, so no archived page was read. sec.gov, crt.sh and certspotter were not used.

## 1. Counts by study and result

| Study | Confirmed | Partially confirmed | Contradicted | Unverifiable | Total |
|---|---|---|---|---|---|
| OJC Fund and Groundswell (V43B-01 to 08) | 5 | 3 | 0 | 0 | 8 |
| De facto fiscal sponsors (V43B-09 to 19) | 8 | 3 | 0 | 0 | 11 |
| **Total** | **13** | **6** | **0** | **0** | **19** |

## 2. Findings

### 2.1 OJC Fund and Groundswell

1. **Reproduction.** A cache-only re-run gives a byte-identical CSV (md5 2e3b9e89…). The frame reproduces S2 0.33698, S3 0.30178 and OJC's block of $545,325,747 (V43B-01).
2. **Pass-throughs: confirmed.** Read straight from the line caches, OJC's two returns have 6,419 positive lines and $720,465,631. The 19 lines to DAF sponsors, panel members and federations total $2,154,670, which is 0.299%. None of the 11 recipient EINs is a church-block EIN. One nuance: USA Outreach Priority 1 (954118740, $21,936) is FOUNDATION 10 with filing code 06, but it is a DAFRC panel member, and the bucket order classifies it first as a DAF sponsor. A wider DAF and federation name screen over every FOUNDATION 10 recipient finds only one $10,307 hit, which is a school (V43B-02).
3. **"38.9% congregations": partially confirmed.**
   - The figure reproduces, but the script types recipients two ways without saying so. `ojc_rows` uses the filed Schedule I name, which gives 38.9% congregations. `share_rows` uses the BMF name, which gives 41.6%.
   - The faith-share variants use the BMF-name typing. That is why the congregations-only variant removes $318.5m of OJC block dollars, not the $333.0m implied by the fine-type table.
   - The base study's rule gives 44.7%, and 16–17% of dollars stay untyped. The defensible statement is "about two-fifths (38.9–41.6% by name rule)" (V43B-03).
4. **Faith-share range: arithmetic confirmed, restatement not supported.**
   - All 16 variant values reproduce.
   - The block is defined by church status, and every OJC recipient has it. The 27.3% and 28.2% variants apply a congregation filter to OJC alone. The symmetric versions give 29.2% (dropping school and chesed-fund names for every sponsor) and 23.0% (congregations only, every sponsor).
   - So "27–30%" mixes definitions. The validated statement keeps **about 30% (30.2%) of church-status block dollars**, with sensitivities of 27–29% (OJC's non-congregation recipients discounted), 23% (congregations only, all sponsors) and 25.1% (without OJC) (V43B-04).
5. **Inflows: confirmed.** 19 lines total $54,043,136, which is 7.36% of $734,529,875 of DAF contributions. Reattributing that share gives S3 29.7% (V43B-05).
6. **Groundswell accounts: partially confirmed.**
   - The live terms (Last Updated July 6, 2026) say: "Your Contributions will be held by the Foundation in a Donor Advised Fund account for you".
   - The products page says "Groundswell offers each employee their own donor-advised fund (DAF)", and also sells "multiple corporate Donor-Advised Funds".
   - So the accounts are per-user DAFs in count terms. The filing does not separate corporate DAFs, the dollar split is unknown, "mostly employees" is inference, and the 2024 terms were not readable (V43B-06).
7. **Line 6: confirmed.** The amended XML has `DonorAdvisedFundInd` 0 alongside 12,808 DAFs in Schedule D Part I(a), with lines 5 and 6 both answered 1. That is internally inconsistent (V43B-07).
8. **Size ratios: confirmed.** EOY value is $787 per account, contributions $757 and grants $348. The average grant is at most $172, taking Part III's "OVER 26,000 INDIVIDUAL GRANTS" (V43B-08).

### 2.2 De facto fiscal sponsors

1. **Reproduction and baseline: confirmed.** The validator's JSON is identical to `final.json` (md5 29507c06…), and the CSV and sample are byte-identical. The baseline reproduces §11.50: fiscal sponsors 0.4407% / 1.9411%, core 7.760% / 11.610%, broad 24.794% / 19.850% (V43B-09).
2. **Eleven hosts, five on neither list: confirmed.** None of the five EINs is in the keyed list, and none of the five names appears anywhere in the cached directory page. One minor point: two of Common Counsel's "5 projects" are the same project ("Fund for the Movement 4 Black Lives" and "M4BL"), so it has 4 distinct projects, still at least 3 (V43B-10).
3. **ImpactAssets 284 / 346 (82.1%): confirmed** (V43B-11).
4. **"10 of 11 only via ImpactAssets": partially confirmed.**
   - Nine hosts are detected only through ImpactAssets lines.
   - Tides Foundation also has two US Charitable Gift Trust lines ("Tides Foundation For benefit of Movement Voter Fu"). They repeat an ImpactAssets project, so 10 of 11 reach three projects only through ImpactAssets.
   - The doc's own table shows Tides Foundation with 2 filers. Read literally, the "≥ 3 projects from ≥ 2 filers" sentence would keep Tides Foundation as well (V43B-12).
5. **Union re-cut: confirmed arithmetically.** The figures are 2,872 lines and $1,914.4m (0.472% / 2.065%), core 7.789% / 11.728% and broad 24.823% / 19.967%.
   - Assets Under Movement's 58 lines carry no other flag. Without it the figures are 0.462% / 2.002%, core 7.780% / 11.665% and broad 24.814% / 19.904% (V43B-13).
6. **201 directory EINs, $703.2m: confirmed** (V43B-14).
7. **Hand check: partially confirmed.**
   - Parse 29/30 is confirmed: #16 names Second Harvest on both sides.
   - On names alone the validator reads 19–21/30 as plausible sponsorship. #10 and #17 cannot be judged without host pages.
   - #26 repeats #20's project (AROC) in another year, so the sample holds 29 distinct projects.
   - 21/30 has a Wilson 95% interval of about 52–83% (V43B-15).
8. **New: three of the five added hosts are DAF sponsors.**
   - Assets Under Movement, Possibility Labs and Common Counsel are all DAFRC-vetted DAF sponsors ("Yes, DAF Sponsor"). Their DAF shares of grants in `sponsor-cost-structure.csv` are 0.73, 0.65 and 0.62.
   - The repo's DAF-to-DAF whitelist already excludes them, under W2 for AUM ("fiscal sponsor / processor inflows") and W4 for the other two.
   - Together they carry $79.4m of the $114.6m added. The study mentions AUM's DAFs but not that all three are vetted panel sponsors (V43B-16, V43B-17).

### 2.3 Questions put to the validator

- **Is the ImpactAssets concentration a fatal bias? No for the headline, yes for recall.**
  - The added dollars are keyed by EIN across all 48 itemising sponsors' lines, so the union re-cut does not inherit ImpactAssets' share of dollars.
  - The worst case moves the core by 0.03 pp of lines and 0.12 pp of dollars, so no plausible recall error at other filers could change the headline.
  - The bias is fatal to two other readings. The 11 hosts are a lower bound, not a census. And the 317 unseen directory EINs cannot be judged at all (V43B-18).
- **Does Assets Under Movement belong as a fiscal sponsor? Only as a hybrid, in a sensitivity.**
  - Its home page (read 2026-11-20) lists Donor Advised Funds and Collaborative or Pooled Funds and says it supports "collaborative funds, sponsored projects, and emerging initiatives". So hosting projects is real.
  - But it is a DAFRC-vetted DAF sponsor with 187 DAFs and $93.1m of DAF contributions in FY2023 (filed), and a 0.73 DAF share of grants.
  - Its FBO "projects" are pooled funds: Families and Workers Fund, Emergent Fund, Maui Just Recovery Fund and New Sheriff in Town Fund. Only $1.06m of its $58.0m arrives on FBO lines.
  - Counting all $58.0m as fiscal-sponsor dollars overstates. The validated statement gives the addition as a range of $35.1m–$114.6m (0.04%–0.12% of proxy dollars). The low end drops the three DAF-sponsor hybrids.
  - GlobalGiving is a giving platform, an intermediary rather than a fiscal sponsor in the narrow sense, as the authors note. Common Counsel and Possibility Labs both offer fiscal sponsorship on their own sites.
- **Should any headline change? No headline number changes.**
  - Exception proxy: the refined core 7.76% / 11.61% and broad 24.79% / 19.85% remain the governing figures. The de facto hosts add at most 0.03 pp / 0.12 pp, and that is recorded as an upper-bound note.
  - Faith share: "about 30%" of church-status block dollars stays the headline. The OJC composition is added as a qualifier: about two-fifths congregations, 23% on a congregations-only basis for every sponsor.
  - Groundswell: its accounts stay in DAF account totals, tagged as employer-platform micro-accounts.

## 3. Decisions on proposed corrections

### 3.1 The 12 [ojc-gs] corrections

| # | Target | Find (abridged) | Decision | Reason |
|---|---|---|---|---|
| 1 | b4026-06-01 | "76.4% … mostly Orthodox congregations, yeshivas and chesed funds." | **Modify** | Give congregations as 38.9% (filed names), 41.6% (BMF names) or 44.7% (base rule), not 38.9% alone |
| 2 | b4026-06-01 | "Without the OJC Fund the figures are 25.1% (S3)…" | **Modify** | Keep the variants as sensitivities; drop "27–30% is the defensible S3 range"; add the symmetric 23.0% |
| 3 | b4026-06-01 | "Any error in its Schedule I moves the faith share…" | **Modify** | State the basis of 42.4% (filed names; 41.3% on BMF names). Otherwise as proposed |
| 4 | b4026-06-church | "without it the all-panel share is 25.1% [V wave 42B]" | **Modify** | "only 38.9%" becomes "about two-fifths (38.9–41.6%)"; add the symmetric 23.0% |
| 5 | FINAL-STATUS | "(25% without the OJC Fund, a pass-through sponsor)" | **Modify** | Replace "27% if only its congregation-named recipients count" with 27–29% and the symmetric 23% |
| 6 | FINAL-STATUS | "its accounts average $787, which raises…" | **Accept** | Verified against the terms, the FAQ and the XML |
| 7 | FINAL-STATUS | "(average $787 per account)" | **Accept** | Verified |
| 8 | prop-0503-1915 | "Whether they are DAFs in the DAFRC sense is not settled here…" | **Accept** | Verified; terms re-fetched live |
| 9 | prop-0503-1915 | "**Groundswell's sponsor status is inference.**" | **Accept** | Verified against the XML and the terms |
| 10 | prop-0503-1915 | "as the only likely sponsor among the outside-panel rows [I]." | **Accept** | Verified |
| 11 | g1915b-04 | "Except for Groundswell and possibly Samaritan Bethany…" | **Accept** | Verified |
| 12 | queue-batch37 | "It does not quite: the average is above $500." | **Accept** | $4,463,378 / 26,000 = $171.7 verified |

**Tally: 7 accepted, 5 modified, 0 rejected.**

### 3.2 Fiscal-sponsor study

The study proposes no exact corrections; its proposals are queue items only. The validator adds seven corrections:
- five to the study itself: the ImpactAssets wording, the two-filer sentence, the Common Counsel project count, the hand-check caveat, and the DAF-sponsor caveat with the restated range;
- one to FINAL-STATUS: an upper-bound note on the fiscal-sponsor share;
- the new report §11.61.

### 3.3 Further validator corrections

- **OJC study:** the 38.9% bullet, the §0 reading and §5 are restated to match §2.1 above.
- **FINAL-STATUS:** the line 222 faith-share sentence gets the congregations-only qualifier.
- **Industry report:** a new §11.61 is added. The current last subsection is §11.60 (wave 43A), and no earlier §11 paragraph is edited.

## 4. Limits

- Name typing was not checked against recipients' websites or charters. The validator's sample reading of OJC names is impressionistic.
- The Groundswell 2024 terms could not be read (web.archive.org gave no response). Schedule B, which would give the employer and employee split, is not public.
- Of the four fiscal-sponsor host pages, ctwo.org's fetched pages did not mention fiscal sponsorship in their static HTML, so CTWO's sponsorship programme is not confirmed from a primary page. GlobalGiving's role was not re-read beyond robots.txt.
- The DAF-to-DAF share of the inflows to the three hybrid hosts is not measurable from Schedule I.

## 5. Source register

| Source | URL | Date | Used for |
|---|---|---|---|
| OJC Fund Form 990 FY2023 and FY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202411369349313111_public.xml ; https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521359349314057_public.xml | line caches 2026-11-19 | lines, buckets |
| Groundswell amended TY2024 Form 990 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml | ReturnTs 2026-01-28; cached 2026-11-20 | tags |
| Groundswell terms of use | https://www.groundswell.io/legal/terms | Last Updated 2026-07-06; re-fetched 2026-11-20 | DAF per user |
| Groundswell FAQ and products | https://www.groundswell.io/faq ; https://www.groundswell.io/products/giving | 2026-11-20 (author cache) | account model |
| IRS EO BMF | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | 2026-11 cache | FOUNDATION codes, AUM record |
| IRS Form 990 series downloads | https://www.irs.gov/charities-non-profits/form-990-series-downloads | FY2023–24 | top-50 Schedule I lines |
| DAFRC 2025 dataset | https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx | Spring 2026 | vetted DAF sponsor status of AUM, Possibility Labs and Common Counsel |
| Fiscal Sponsor Directory (cached) | https://fiscalsponsordirectory.org/all-fiscal-sponsors-alpha-ordered/ | cache 2026-11-19 | the five hosts are absent |
| Assets Under Movement home page | https://assetsundermovement.org/ | 2026-11-20 | services, sponsored projects, Amalgamated Foundation legacy |
| Common Counsel Foundation, Our Work | https://www.commoncounsel.org/our-work/ | 2026-11-20 | fiscal sponsorship, DAFs, pooled funds |
| Possibility Labs home page | https://possibilitylabs.org/ | 2026-11-20 | fiscal sponsorship, DAFs |
| Repo: DAF-to-DAF whitelist; sponsor-cost-structure | data/mission-2026-11-14/daf-to-daf-recipient-whitelist.csv | repo | W2 and W4 exclusions, DAF share of grants |

## Exact corrections

Apply in order within each file. Every Find was checked by script to occur exactly once, both on its own and after the earlier items in the same file have been applied.

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.61 OJC Fund audit, Groundswell accounts and de facto fiscal sponsors (validated, wave 43B)\n\n**OJC Fund audit, Groundswell accounts and de facto fiscal sponsors** (validated, wave 43B). Both studies re-run byte for byte. Of the OJC Fund’s $720.5m of FY2023–24 Schedule I dollars, 0.30% goes to DAF sponsors, other panel members or federations, and none of it reaches church-block recipients. Every block recipient is church-status, but by name only about two-fifths of OJC’s block dollars go to congregations (38.9% on filed names, 41.6% on BMF names); most of the rest goes to yeshivas and chesed funds. The all-panel faith share of church-status block dollars stays about 30% (30.2%). Discounting OJC’s non-congregation recipients gives 27–29%, and limiting every sponsor to congregation names gives 23.0%. Groundswell’s 12,808 accounts are per-user DAFs on its own terms and Schedule D, and its Part IV line 6 “No” contradicts both. Filers’ own “FBO” naming finds 11 de facto fiscal-sponsor hosts, 5 of them on neither list. But 82% of detections come from ImpactAssets, and three of the five are DAFRC-vetted DAF sponsors. Adding them moves fiscal sponsors from 1.94% to at most 2.06% of dollars and the core proxy from 11.61% to at most 11.73%, so the headline proxy stands (repo [`validation-wave43b-report.md`](mission-2026-11-14/validation-wave43b-report.md)) [V wave 43B]\n\n---\n\n## Source register"

### `research/mission-2026-11-14/b4026-06-01-faith-sponsors-outside-top50.md`

**Find:** "76.4% of its own DAF-weighted dollars go to the block, mostly Orthodox congregations, yeshivas and chesed funds."
**Replace with:** "76.4% of its own DAF-weighted dollars go to the block. Every block recipient is church-status in the BMF (FOUNDATION 10; filing-requirement code 06 for 99.6% of the dollars), but by name only about two-fifths of its block dollars go to congregations: 38.9% on filed Schedule I names, 41.6% on BMF names, 44.7% under this study’s own rules. On filed names, 25.9% go to yeshivas and schools, 16.5% to chesed or relief funds, 1.5% to communal umbrella bodies and 17.2% to names the rule cannot type. Its lines are not pass-throughs: 0.30% of its Schedule I dollars go to DAF sponsors, other DAFRC panel members or federations, none of them in the block (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

**Find:** "Without the OJC Fund the figures are 25.1% (S3) and 28.3% (S2) [F]."
**Replace with:** "Without the OJC Fund the figures are 25.1% (S3) and 28.3% (S2) [F]. These are sensitivities, not a new central figure, because the block is defined by church status and every OJC recipient has it. Keeping only the OJC Fund’s congregation-named recipients gives 27.3% (S3) and 30.7% (S2); dropping only its yeshiva and chesed-fund lines gives 28.2% and 31.6%. A congregations-only filter applied to every sponsor gives 23.0% (S3) and 25.8% (S2) (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

**Find:** "Any error in its Schedule I moves the faith share by up to about 5 points."
**Replace with:** "Any error in its Schedule I moves the faith share by up to about 5 points. An audit of all 6,419 lines (b4026-0601-01-p0503-ojc-groundswell.md) finds no pass-through to DAF sponsors or federations in the block. But 42.4% of its block dollars go to yeshiva/school and chesed-fund names on filed names (41.3% on BMF names). About 7.4% of its FY2023–24 DAF contributions arrive as grants from other panel sponsors, mainly PayPal Charitable Giving Fund ($44.4m); reattributing that share lowers the S3 faith share from 30.2% to 29.7% [V wave 43B]"

### `research/mission-2026-11-14/b4026-06-church-daf-recipients.md`

**Find:** "without it the all-panel share is 25.1% [V wave 42B]"
**Replace with:** "without it the all-panel share is 25.1% [V wave 42B]. Its Schedule I sends 0.30% to DAF sponsors, other panel members or federations, and none of that reaches the block. But only about two-fifths of its block dollars go to congregation-named recipients (38.9–41.6%). Limited to those, the all-panel share is 27.3%; a congregations-only filter on every sponsor gives 23.0% (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "(25% without the OJC Fund, a pass-through sponsor)"
**Replace with:** "(25% without the OJC Fund, a pass-through sponsor in the asset sense whose Schedule I goes to church-status Orthodox bodies, not to other DAF sponsors; 27–29% if its non-congregation recipients are discounted, 23% if every sponsor is limited to congregation names) [V wave 43B]"

**Find:** "its accounts average $787, which raises the same comparability caveat as processor accounts."
**Replace with:** "its accounts average $787, which raises the same comparability caveat as processor accounts. They are DAFs in the legal sense and meet DAFRC’s Schedule D Part I(a) rule: one DAF per user, mostly employees, funded by the user and by employer matches (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

**Find:** "(average $787 per account)"
**Replace with:** "(average $787 per account; per-employee DAFs funded by employees and employer matches, so DAFs, but processor-like in size) [V wave 43B]"

**Find:** "EIN-keyed fiscal sponsors account for 0.44% of lines and 1.94% of dollars; dropping large-programme hosts gives 1.68%."
**Replace with:** "EIN-keyed fiscal sponsors account for 0.44% of lines and 1.94% of dollars; dropping large-programme hosts gives 1.68%. Five de facto hosts found from filers’ own “FBO” naming (g0503-03-de-facto-fiscal-sponsors.md) would raise this to at most 0.47% / 2.06%, and the core to at most 7.79% / 11.73%. Three of the five are also DAFRC-vetted DAF sponsors and 82% of the detections come from one filer, so these are upper bounds and the headline stands [V wave 43B]"

**Find:** "about 30% across all itemising DAFRC panel sponsors (25% without the OJC Fund)"
**Replace with:** "about 30% across all itemising DAFRC panel sponsors (25% without the OJC Fund; about 23% if every sponsor is limited to congregation-named recipients) [V wave 43B]"

### `research/mission-2026-11-14/prop-0503-1915-propagation.md`

**Find:** "Whether they are DAFs in the DAFRC sense is not settled here (queue P-P0503-1915-02)."
**Replace with:** "P-P0503-1915-02 settles the DAF question. The accounts are individual DAFs (one per registered user, mostly employees of client companies), funded by the user’s ACH, card, payroll or DAF-to-DAF deposits and by employer matches or gifts. The Foundation’s terms say it operates all DAFs under IRC 4966 and 4967, and Schedule D lines 5 and 6 answer Yes. They meet DAFRC’s Schedule D Part I(a) selection rule and are processor-like in size, not employer or campaign funds (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

**Find:** "**Groundswell's sponsor status is inference.**"
**Replace with:** "**Groundswell's sponsor status is now documented** (b4026-0601-01-p0503-ojc-groundswell.md): its terms hold contributions “in a Donor Advised Fund account for you”, and its TY2024 Schedule D answers lines 5 and 6 Yes; only Part IV line 6 says No [V wave 43B]"

**Find:** "as the only likely sponsor among the outside-panel rows [I]."
**Replace with:** "as the only likely sponsor among the outside-panel rows [I]. P-P0503-1915-02 confirms it from the filing and the terms of use [V wave 43B]"

### `research/mission-2026-11-14/g1915b-04-line6-vs-schedule-d.md`

**Find:** "Except for Groundswell and possibly Samaritan Bethany, these are operating charities using the DAF column [I], as batch 38 found."
**Replace with:** "Except for Groundswell and possibly Samaritan Bethany, these are operating charities using the DAF column [I], as batch 38 found. Groundswell is a DAF sponsor on its own documents: one DAF per user, mostly employees, funded by the user and by employer matches, with Schedule D lines 5 and 6 answered Yes (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

### `research/mission-2026-11-14/queue-batch37-filing-questions.md`

**Find:** "It does not quite: the average is above $500."
**Replace with:** "It does not quite: the average is above $500. Its accounts are per-user DAFs under its terms of use, funded by employees and by employer matches; its TY2024 grants average at most about $172 (over 26,000 grants, $4.46m) (b4026-0601-01-p0503-ojc-groundswell.md) [V wave 43B]"

### `research/mission-2026-11-14/b4026-0601-01-p0503-ojc-groundswell.md`

**Find:** "  - **38.9%** to congregations (1,110 recipients);"
**Replace with:** "  - **38.9%** to congregations (1,110 recipients; 41.6% if recipients are typed by their BMF names, which is the basis the faith-share variants below use) [V wave 43B]"

**Find:** "A defensible range for the all-panel faith share of church-block dollars is **27–30%**."
**Replace with:** "The central figure for church-status block dollars stays 30.2%. The OJC-only variants filter one sponsor and not the others, so 27–30% is a sensitivity range, not a restatement; the symmetric congregations-only figure is 23.0% [V wave 43B]"

**Find:** "is an upper figure. Report **27–30%**, or 25.1% without OJC."
**Replace with:** "is the central figure for church-status recipients. Report about 30%, with 27–29% if OJC’s non-congregation recipients are discounted, 23% on a congregations-only basis for every sponsor, and 25.1% without OJC [V wave 43B]"

### `research/mission-2026-11-14/g0503-03-de-facto-fiscal-sponsors.md`

**Find:** "10 of the 11 de facto hosts are detected only through ImpactAssets lines; only Players Philanthropy Fund is seen across three sponsors [C]."
**Replace with:** "10 of the 11 de facto hosts reach three projects only through ImpactAssets lines. Tides Foundation also has a US Charitable Gift Trust detection, but it repeats an ImpactAssets project (Movement Voter Fund). Only Players Philanthropy Fund reaches three projects without ImpactAssets (three sponsors) [C] [V wave 43B]"

**Find:** "rule leaves only Players Philanthropy Fund."
**Replace with:** "rule, read as at least three projects outside ImpactAssets, leaves only Players Philanthropy Fund; Tides Foundation has two filers, but all eight of its projects come from ImpactAssets [V wave 43B]"

**Find:** "Without it, the ≥ 3 addition is $56.6m (0.061%) [C, from the per-EIN figures]."
**Replace with:** "Without it, the ≥ 3 addition is $56.6m (0.061%) [C, from the per-EIN figures]. None of its 58 lines carries another flag, so without it the fiscal-sponsor share is 0.46% / 2.00%, the core 7.78% / 11.67% and the broad union 24.81% / 19.90%. Assets Under Movement, Possibility Labs and Common Counsel are all DAFRC-vetted DAF sponsors (DAF share of grants 0.73, 0.65 and 0.62 in sponsor-cost-structure.csv; the DAF-to-DAF whitelist excludes them under rules W2 and W4), so part of their $79.4m may be DAF-to-DAF flow. Only $1.06m of Assets Under Movement’s $58.0m arrives on project-style lines. Its site offers DAFs and collaborative or pooled funds and supports “sponsored projects”, so it is a hybrid, not a pure fiscal sponsor. The ≥ 3 addition is best stated as $35.1m–$114.6m (0.04%–0.12% of proxy dollars); the lower end drops the three DAF-sponsor hybrids [V wave 43B]"

**Find:** "| Common Counsel Foundation | 5"
**Replace with:** "| Common Counsel Foundation | 5; 4 after merging “Fund for the Movement 4 Black Lives” and “M4BL” [V wave 43B]"

**Find:** "- **Sponsorship precision: 21 / 30 = 70%** over all classes; **19 / 21 = 90.5%** in `intermediary_other`. The 2 misses are #16 and #29."
**Replace with:** "- **Sponsorship precision: 21 / 30 = 70%** over all classes; **19 / 21 = 90.5%** in `intermediary_other`. The 2 misses are #16 and #29. A validator re-read reproduces parse 29 / 30. From names alone, sponsorship is 19–21 / 30, because #10 and #17 cannot be judged without host pages. #26 repeats #20’s project in another year, so the sample holds 29 distinct projects, and 21 / 30 has a Wilson 95% interval of about 52–83% [V wave 43B]"
