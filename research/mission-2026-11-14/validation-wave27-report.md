# Validation wave 27: new directions N19–N22 (investment menus and pool performance, donor tax scenarios, grant geography, donor feature census)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave27.
**Register:** [`validation-register-wave27.csv`](../../data/mission-2026-11-14/validation-register-wave27.csv), rows V27-01 to V27-36.
**Documents validated:**
- N19: [direction-investment-menus-performance.md](direction-investment-menus-performance.md), `sponsor-investment-menus-2026.csv` (20 rows) and `sponsor-pool-returns-2021-2025.csv` (354 rows)
- N20: [direction-donor-tax-scenarios-2026.md](direction-donor-tax-scenarios-2026.md), `donor-tax-scenarios-2026.csv`, `donor-tax-scenarios-2026-sensitivity.csv`, `donor-tax-parameters-2026.csv` and `scripts/mission_tax_scenarios.py`
- N21: [direction-grant-geography.md](direction-grant-geography.md), `daf-grant-geography-state-2023-2024.csv` (3,907 rows), `daf-grant-geography-cf-local-share.csv` (48 rows) and `scripts/mission_grant_geography.py`
- N22: [direction-donor-feature-census.md](direction-donor-feature-census.md) and `donor-feature-census-2026.csv` (504 rows)

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching any page on it, checking the `*`, ClaudeBot and anthropic-ai groups, and honoured crawl delays (law.cornell.edu 10 s; growyourgiving.org and greaterhorizons.org 10 s). Hosts whose robots.txt could not be read were not fetched. **I did not use crt.sh.** For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The sources were:
- **N19:**
  - re-fetched sponsor documents: the Fidelity Pool Performance Summary (as of 2026-09-30) and CIAP page; the Vanguard Charitable performance page (parsed independently from HTML); the FFTC performance report and All Pool Sheets; the GKCCF Oct 2026, ESG Oct 2026 and Dec 2025 summaries and investing page; the Greater Horizons Oct 2026 and ESG Oct 2026 summaries; the CJP DAF report; the NCF Q3 2026 report; the NPT IDAP page; the AEF advisors FAQ; SVCF advisor investment options;
  - the third-party copy of the GS DAF Program Circular (FireAid report appendix; fireaidla.org robots.txt returns 404, so no rules).
- **N20:**
  - P.L. 119-21 (govinfo HTML), secs 70111, 70424, 70425 and a whole-Act search for "4940";
  - Rev. Proc. 2025-32 (Table 1, secs 4.03, 4.14); IR-2026-135; Pub. 6196 (10-2026);
  - LII text of IRC §§170, 63, 1411, 4940, 4942; eCFR 26 CFR 53.4940-1;
  - a **re-run of `mission_tax_scenarios.py`** to scratch, plus hand and independent-code recomputation of 8 scenario families.
- **N21:**
  - a fresh download of Census NST-EST2024-ALLDATA (byte-identical to the input; Last-Modified 2024-12-19);
  - a **re-run of `mission_grant_geography.py`** in scratch with outputs redirected, on the session's existing Schedule I line cache (94 files), BMF copy, ZIP cache and Census files;
  - an independent aggregation of ZIP 50037 (Boone, IA) lines.
- **N22:** 36 sponsor, help-centre and app-store pages re-fetched (Apple and Google Play detail pages are allowed; their search paths were not used).

## Headline

The four documents hold up well. 31 of 36 claims are confirmed and 5 partially confirmed. None is contradicted and none is unverifiable. **Both scripts reproduce:** the tax script byte-for-byte, and the geography script on every state row (one CBSA row differs immaterially).

**What holds independently:**
- **N19 investment menus and performance:**
  - Greater Horizons' summaries carry exactly GKCCF's figures. 162 and 384 numeric tokens match in order; only the phone numbers differ.
  - Vanguard: my own parse of the page gives a 5-year median of −0.04 pp (n=16) and a 1-year median of −0.04 (n=31). ESG options: −0.07 (5y, n=3) and −0.52 (1y, n=4). Global Positive Impact is −9.31.
  - Fidelity's 7 asset-allocation pools trail by −0.58 to −0.76 pp over 5 years. The PDF says "Pool results include a Fidelity Charitable annual administrative fee".
    - **New supporting evidence for the fee reading:** each asset-allocation pool trails its *own* underlying Asset Manager fund by 0.59–0.64 pp over 5 years, and the Money Market pool trails its benchmark by exactly 0.65 pp at 1, 3 and 5 years.
  - Fidelity's other medians: conventional pools −0.645 (1 of 20 positive); sustainable and impact pools −1.22 (5y).
  - GKCCF: impact pools and mixes −2.41 (n=10); core pools and mixes to 2025-12-31 −0.09, recomputed from the PDF.
  - FFTC Passive LTG calendar rows match the pool sheet. CJP: JCEP +2.8, Diversified +1.1, Equity −3.6 pp.
  - Adviser-programme minimums: AEF $25k, GKCCF $100k, SVCF $5m ($10m with alternatives) and GS IMAP $5m are verbatim.
  - NCF's pools relaunched on 2026-09-01, and the Q3 report is benchmark-only pro forma.
  - 26 return rows match the sources exactly.
- **N20 donor tax scenarios.** Every parameter matches the primary text:
  - P.L. 119-21: §68 at 2/37, applied last; §170(p) $1,000/$2,000; the 0.5% floor ordered D, C, B, E, A, G; floor carryforward only from excess years; the 60% limit made permanent; all effective for tax years after 2025. "4940" appears in the Act only in new §4968(f).
  - Rev. Proc. 2025-32: Table 1, $32,200 and $98,900/$613,700. §4940(a) is 1.39%; 53.4940-1(f)(2)(i)(B) sets carryover basis.
  - IR-2026-135 (Nov. 10, 2026) says contributions "to establish or maintain a donor advised fund do not qualify".
  - **Hand recomputation** reproduces:
    - H1 $720 / $0;
    - H2 $1,440 / $936 / $5,112 (+$3,672);
    - H3 $47,250, the $0.35 cap and +$3,500 from bunching;
    - stock in kind $4,541 / $28,770;
    - PF $11,120 / $556 / $38,880.
  - **My own tax engine** gives H4 $218,598.57, sell-then-give $27,441.81 and in-kind advantage $191,156.76, all to the cent.
- **N21 grant geography:**
  - Top-five state shares: CA 20.0%, NY 13.6%, DC 6.4%, MA 6.0%, MD 4.7%. Top 5 is 50.7% of dollars against 21.4% of population; top 10 is 66.9%; HHI 783.
  - Per capita: $112.87 nationally, DC $3,550, MA $325, MD $292; MA/MS 13.1×.
  - Per 501(c)(3): $23,240.
  - Community-foundation local share: 60.0% pooled, median 71.2%, from 20.0% (Chicago Community Trust) to 91.7% (San Diego). National sponsors: 7.6% (median 4.6%).
  - Schedule I state matches BMF state for 94.4% of $73.27bn.
  - Iowa: $644m on the Schedule I basis vs $231m on the BMF basis. Cornell's ZIP 50037 lines total $193.8m and the Red Cross's $19.4m.
  - Census inputs match a fresh download, and the per-state populations in the CSV equal Census.
- **N22 donor feature census:**
  - 30 cells re-checked, all supported.
  - Section 2.1 counts recount exactly (U 267 of 476).
  - App ratings on 2026-11-15:
    - Fidelity: 3.6 from 24 iOS ratings; 3.8 from 29 Play reviews, 5K+ downloads, updated Nov 9, 2026.
    - Daffy: 4.9 from 560 ratings, v1.54.4. `com.daffy.app` belongs to "S&D Innovative Network (Pvt) Ltd".
  - Verbatim on the live pages: the Daffy MCP, Louise, Daffy for Work "No payroll integration" and Givinga "payroll integration" quotes.

**What needs correcting or qualifying:**
1. **"The other 11 publish no public pool returns" (N19, V27-01).** The menus CSV itself records search captures of CCT Growth Pool factsheets against a "Policy Index" and a DAFgiving360 quarterly performance report. Neither host's robots.txt could be read (403 again on 2026-11-15). Six is therefore a **verified floor**, and the 11 should be described as "no public returns found".
2. **Fidelity CIAP $100k (N19, V27-10).** The live CIAP page says only "a qualified minimum balance". The $100k figure rests on the repo's wave-11 row.
3. **Floor-on-carryover interpretation (N20, V27-24).** The §1 figures "$447k is never used at a $1.5m gift" and "$407k unused" at $2m depend on the two readings that §5 labels [I].
   - Under the alternative reading, the 0.5% floor is not applied to carryovers absorbed in later years. The figures would then be about **$437k and $397k**.
   - The $663k/$337k first-year split is statute-driven and unaffected.
4. **Disclaimer on the CSVs (N20, V27-25).** The doc and script are labelled "NOT TAX ADVICE", but the three CSVs carry no disclaimer. This is a data-file note.
5. **Population denominator (N21, V27-27).** The 21.4% top-5 population share uses the 50 states, DC and PR, matching the dollar denominator. It is 21.6% excluding PR. Worth one clause.
6. **Geography reproduction (N21, V27-26).** All state rows are identical. One CBSA row (Bangor, ME) differs by $0.95m and 70 BMF organisations because of the ZIP-to-CBSA cache state. That moves other CBSA shares only in the 4th decimal.
7. **Android wording (N22, V27-36).** The Fidelity Charitable and Donors' Fund Android apps are standalone sponsor apps, not "parent" apps. Only GoFundMe is a general app.

## Limits

- **Not fetched:**
  - cct.org and dafgiving360.org: robots.txt 403;
  - jct.gov and congress.gov: not needed, and the doc did not use them;
  - gsdaf.org: the GS circular was read from the third-party copy only.
- **N21 re-run inputs.** The re-run used the session's existing Schedule I line cache, BMF copy and ZIP cache. It reproduces the computation but does not re-download the 94 return XMLs or the BMF. The Census state file was freshly downloaded.
- **Not re-checked in this wave:**
  - N19: menu cells for MS GIFT, BofA, RCF, ImpactAssets, Dechomai and JCF; NPT return rows; the expense-ratio ranges.
  - N20: the 2027+ flat-parameter assumption, which the doc already flags.
  - N21: CBSA per-capita rankings beyond the top 10 and the sector mixes in §2.4.
  - N22: the 46 `C` (carried) cells and the 3 `S` cells.
- **ND cells cannot be falsified by fetching.** The 7 ND cells re-checked were not contradicted on the pages read.
- **App-store counts move daily.** They are as of 2026-11-15.

## Exact corrections

### `research/mission-2026-11-14/direction-investment-menus-performance.md`
1. **§0, "Who publishes pool returns against benchmarks?" row.**
   - **Find:** "**The other 11 publish no public pool returns**: SVCF and BofA only on request or in the portal"
   - **Replace with:** "**No public pool returns were found for the other 11**, so 6 is a verified floor [V wave 27]. CCT Growth Pool factsheets against a \"Policy Index\" and a DAFgiving360 quarterly report exist per search captures [R], but neither host's robots.txt could be read. Of the rest: SVCF and BofA only on request or in the portal"
2. **§0, adviser-managed minimums row.**
   - **Find:** "Fidelity CIAP $100,000 (varies by firm);"
   - **Replace with:** "Fidelity CIAP $100,000 (varies by firm; repo wave-11 row. The live CIAP page says only \"a qualified minimum balance\" [V wave 27]);"
3. **§2.3, fee-basis reading.**
   - **Find:** "That is about the size of its 0.60% first-tier admin fee."
   - **Replace with:** "That is about the size of its 0.60% first-tier admin fee. Two further signs support this: each asset-allocation pool trails its own underlying Fidelity Advisor Asset Manager fund by 0.59–0.64 pp over 5 years, and the Money Market pool trails its benchmark by exactly 0.65 pp at 1, 3 and 5 years [V wave 27]."

### `research/mission-2026-11-14/direction-donor-tax-scenarios-2026.md`
1. **§1, AGI limits row, PF.**
   - **Find:** "It is used up by 2031 at a $1m gift, but **$447k is never used at a $1.5m gift** [C]."
   - **Replace with:** "It is used up by 2031 at a $1m gift, but **$447k is never used at a $1.5m gift** [C]. This figure rests on the two floor/carryover readings in §5 [I]. If the 0.5% floor is not applied to carryovers absorbed in later years, it is about $437k [V wave 27]."
2. **§1, AGI limits row, DAF.**
   - **Find:** "nothing is left unused until the gift reaches $2m ($407k unused) [C]."
   - **Replace with:** "nothing is left unused until the gift reaches $2m ($407k unused; about $397k under the alternative floor reading in §5) [C/I; V wave 27]."
3. **§5, interpretations paragraph.**
   - **Find:** "These readings affect only H4 PF and the S3 rows."
   - **Replace with:** "These readings affect only H4 PF and the S3 rows. Under the alternative reading, the S3 unused amounts fall by about $10k each (PF $447k → about $437k; DAF $407k → about $397k). The $663k/$337k 2026 split does not change [V wave 27]."

### `research/mission-2026-11-14/direction-grant-geography.md`
1. **§0, State shares row.**
   - **Find:** "Top 5 states take 50.7% of dollars against 21.4% of population; top 10 take 66.9%."
   - **Replace with:** "Top 5 states take 50.7% of dollars against 21.4% of population (both measured over the 50 states, DC and PR; 21.6% of the 50 states and DC); top 10 take 66.9% [V wave 27]."
2. **§6, reproduction note.**
   - **Find:** "- Run time is about 65 s."
   - **Replace with:** "- Run time is about 65 s.\n- **Reproduction (wave 27).** A re-run on the same caches reproduced every state row exactly. One CBSA row (Bangor, ME) differed by $0.95m and 70 BMF 501(c)(3)s because of the ZIP-to-CBSA cache state, which moves other CBSA shares only in the 4th decimal. No headline figure changes [V wave 27]."

### `research/mission-2026-11-14/direction-donor-feature-census.md`
1. **§4, white space (f).**
   - **Find:** "   - **(f) Android.** It is confirmed only where a parent app exists (Fidelity, GoFundMe, The Donors' Fund)."
   - **Replace with:** "   - **(f) Android.** It is confirmed for only three: two sponsor apps (Fidelity Charitable, The Donors' Fund) and one general app (GoFundMe). DAFgiving360's Android route rests on a search snippet [S] [V wave 27]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.23.** Add "### 11.24 New directions N19–N22 (validated, wave 27)", containing the paragraph below. If §11.24 is already taken, use the next free number.

   > **New directions N19–N22 (validated, wave 27).**
   > - **Investment menus and performance.** At least 6 of the top-20 sponsors publish pool returns against benchmarks: Fidelity, Vanguard Charitable, FFTC, GKCCF, Greater Horizons (identical figures to GKCCF) and CJP. NPT publishes returns without benchmarks. NCF relaunched its pools on 2026-09-01 and so far shows benchmark-only pro forma figures.
   >   - Index menus track within about 0.1 pp. Vanguard's 5-year median is −0.04 pp; GKCCF's is −0.09 pp to 2025-12-31.
   >   - Fidelity's 7 asset-allocation pools trail by 0.58–0.76 pp over 5 years. Fidelity's returns include its admin fee, and the gap matches it: each pool trails its own underlying fund by about 0.6 pp.
   >   - ESG and impact options trailed over trailing windows dominated by 2022–23: GKCCF −2.4 pp and Fidelity −1.2 pp.
   >   - Adviser-managed minimums run from $25k (AEF) and $100k (GKCCF; Fidelity CIAP per repo) to $5m (SVCF, GS IMAP).
   > - **Donor tax 2026 (illustrative, not tax advice).** Every parameter matches P.L. 119-21, Rev. Proc. 2025-32 and IRS guidance, and the script reproduces exactly.
   >   - A DAF never beats a direct gift of the same asset in the same year. It loses for non-itemizers, because DAF gifts are excluded from the $2,000 joint non-itemizer deduction (H1: $720 vs $0).
   >   - Bunching pays near the standard deduction (+$3,672 for H2).
   >   - The 35% cap holds the value of each deductible dollar to $0.35.
   >   - Giving stock in kind is the largest lever for any vehicle: $4.5k, $28.8k and $191k in the three profiles.
   >   - Private-foundation figures: $11,120 excise if the donated stock is sold. The "$447k never used" at a $1.5m gift depends on an interpretation of the 0.5% floor for carryovers (about $437k otherwise).
   > - **Grant geography (FY2023–24, top-50 sponsors, ex university/hospital).**
   >   - CA 20.0%, NY 13.6%, DC 6.4%, MA 6.0% and MD 4.7% of dollars. The top 5 hold 50.7% of dollars against 21.4% of population.
   >   - $113 per resident nationally and $3,550 in DC; $23,240 per registered 501(c)(3).
   >   - Community foundations keep 60% in state (median 71%; Chicago Community Trust 20%, San Diego 92%), against 7.6% for national sponsors.
   >   - Schedule I addresses match BMF states for 94.4% of dollars. Lockbox addresses inflate Iowa ($644m vs $231m).
   >   - The script reproduces on every state row.
   > - **Donor feature census.** Table stakes are stock, complex-asset and crypto acceptance, recurring grants, search and vetting, family roles and adviser access.
   >   - Differentiators sit with digital-first sponsors: Daffy's member MCP server, app, campaigns and CSV export; TIFIN Give's AI assistant; Endaoment's API.
   >   - Fidelity's app had 24 iOS ratings and Daffy's 560 on 2026-11-15.
   >   - 267 of 476 cells remain unassessed, so absences are "not found", not proven.

## Data-file notes (not .md; for the owning agent)

- **`donor-tax-scenarios-2026.csv`, `donor-tax-scenarios-2026-sensitivity.csv`, `donor-tax-parameters-2026.csv`:** add a "Illustrative modelling; not tax advice; federal only" note (for example, in the parameters file's first row or a `notes` field) so that the files carry the label when used on their own.
- **`sponsor-investment-menus-2026.csv`:**
  - row 1 (Fidelity) `adviser_program_minimum_usd`: append "(live CIAP page: 'qualified minimum balance'; figure from repo wave-11)";
  - rows 3 and 12 (DAFgiving360, CCT) `returns_published`: keep the [R] wording. These two are why 6 is a floor.
- **`sponsor-pool-returns-2021-2025.csv`:** no change. All 26 spot-checked rows match.
- **`daf-grant-geography-state-2023-2024.csv`:** no change to state rows. CBSA 12620 (Bangor, ME) differs on re-run ($18.63m published vs $19.57m re-run) and should be treated as ±$1m.
- **`donor-feature-census-2026.csv`:** no change.
