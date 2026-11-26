# Validation wave 25A: new directions N9–N11 (state DAF law, sponsor accessibility and service levels, CF consolidation and fees)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave25a.
**Register:** [`validation-register-wave25a.csv`](../../data/mission-2026-11-14/validation-register-wave25a.csv), rows V25A-01 to V25A-35.
**Documents validated:**
- N9 [`direction-state-daf-law-tracker.md`](direction-state-daf-law-tracker.md), with `state-daf-law-tracker-2021-2026.csv`;
- N10 [`direction-sponsor-accessibility-service.md`](direction-sponsor-accessibility-service.md), with `sponsor-a11y-axe-2026.csv`, `sponsor-service-levels-2026.csv` and `scripts/mission_sponsor_a11y_service.py`;
- N11 [`direction-cf-consolidation-fees.md`](direction-cf-consolidation-fees.md), with `cf-consolidation-2021-2026.csv`, `cf-daf-fee-census-2026.csv`, `scripts/mission_cf_fee_census.py` and `scripts/mission_cf_fee_data.py`.

**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, call keyed APIs or contact anyone. I read robots.txt on each host before fetching a page and treated any robots.txt status other than 200/404/410 as "do not fetch" (details under Limits). **I did not use crt.sh or fcsuite.com.** I used a generic browser User-Agent. For each claim I formed a verdict from primary sources first and compared it with the documents afterwards.
- **axe-core re-run (N10).** My own Playwright/Chromium script, not the author's: axe-core 4.9.1 from cdnjs, the same WCAG tag set (`wcag2a wcag2aa wcag21a wcag21aa wcag22aa`), 1366×900, network-idle plus 2.5 s, nothing clicked. **21 pages at 13 sponsors** (the doc scanned 37). Five more pages were loaded for text only.
- **Schedule N screen re-run (N11).** `mission_cf_fee_census.py --task schedn` ran in a scratch copy of `scripts/` and the input CSVs, with an **empty cache**, no local XML directory and a generic UA. All 2,795 returns were re-read from the GivingTuesday mirror. I also parsed six Schedule N XMLs myself.
- **Fee schedules (N11).** I fetched 14 of the 34 published schedules (robots permitting), read the tiers and minimums myself and recomputed the fee at $100k, $1m and $10m by hand arithmetic, then compared with the CSV.
- **Statutes and letters (N9).** I fetched the FPPC regulation and staff memo, Hawaii Acts 205 and 108, the Kansas Register, the LII copy of the Illinois rule, the NY Assembly page for A3632, the Prop 40 text, the Minnesota AG copy of the SPLC letter, the NY AG copy of the GoFundMe letter, the CA AG platform rulemaking and forms pages, the CA AG DAF report, FastDemocracy (AB 1353), Adler & Colvin (AB 2936) and MinistryWatch (AB 1712).

## Headline

**All three documents hold up.** Of 35 claims, 29 are confirmed, 5 partially confirmed and 1 unverifiable. None is contradicted outright.

1. **N10 reproduces exactly.** Every one of the 21 re-scanned pages returned the same axe rule IDs, impacts and element counts as `sponsor-a11y-axe-2026.csv` (for example NPT home: image-alt 9, label 4, color-contrast 3, target-size 1; AEF home: 19/2/1; CJP home: 16). The aggregates also recompute: critical failures on 7 of 37 pages (31 elements), serious on 22 pages (155 elements), 14 clean pages, 13 of 20 sponsors and $173.8bn (69.3%) covered. The service-level observations are verbatim:
   - Renaissance "Monday-Friday | 8AM – 5PM Eastern"; GKCCF and Greater Horizons "Monday-Friday, 8 a.m.-5:30 p.m. CT"; FFTC "during business hours".
   - Vanguard "we'll be in touch soon" (its contact form); Dechomai "we will respond right away".
   - Fidelity's "Virtual Assistant" link; FFTC's accessiBe script (acsbapp.com); AEF's placeholder statement ("See our Accessibility Tips for what to do for this page on your website.").
2. **N9's primary texts are exact.**
   - **FPPC Reg. 18424.3:** filed 11-22-2021, operative 12-22-2021; the memo figures (33 of 2,029, 1.63%, 8 of 33, $1,242,728) are verbatim.
   - **Hawaii:** Act 205 approved 2024-07-05 with the California-style DAF exclusion; Act 108 approved 2025-05-29, effective 2026-07-01, with section 10 on 2025-07-01.
   - **Credits:** Illinois "(v) is not a donor advised fund" (rule effective 2025-05-23); Kansas K.A.R. 92-12-152 quote verbatim, effective 2026-04-17.
   - **Wealth taxes:** NY A3632's DAF clause verbatim (in Ways and Means, re-referred 2026-01-07); Prop 40's post-2025-10-15 transfer and pledge rules verbatim; 52.8% "no" per KTVU.
   - **California bills and forms:** AB 1353 "Died at Desk" 2022-02-01; AB 2936 passed the Assembly and was held in Senate Judiciary; AB 1712 was Wicks's bill. No CT-DAF form exists: the rulemaking page and the forms page list no DAF form.
   - **SPLC letter:** dated 2026-05-21, 16 AG signatures, "We urge you to reconsider", no deadline; the CA release of 2026-05-22 says "a coalition of 16 attorneys general".
3. **N11's filed events and fee arithmetic are exact.**
   - **Schedule N:** Coastal → San Diego $10,072,419 (2024-07-15); Keweenaw → CFUP $10,546,465 (2021-09-01); Rusk → Eau Claire $2,144,330; Fairfield → Hamilton $4,458,882; White Bear Lake → CommunityGiving $4,965,262 (seven lines naming DAFs); Watertown $21,577,662.
   - **Screen re-run:** 2,795 returns and the same 5 flagged returns.
   - **Census:** 34 schedules / 43.0% of assets, medians 100 / 100 / 67.2 bps and the weighted means reproduce from the CSV; **all 14 schedules I re-read match** the transcribed tiers, minimums and bps.

**Partial confirmations:**
1. **V25A-16, GoFundMe letter signatories.** The letter is signed by **23 officials from 21 states: 19 attorneys general plus 4 secretaries of state** (MD, PA, SC, TN). "21 AGs" is wrong; "21 states" is right.
2. **V25A-25, Orange & Sullivan + Rockland.** The merger and NY AG approval are confirmed (Mid-Hudson News, 2026-01-30). The ~$71m and the 2026-01-01 date were not re-read, because radiocatskill.org's robots.txt returns 403.
3. **V25A-30, screen base rate.** The re-run reproduces 2,795 returns and 5 flags, but `cf-vendor-map-by-ein-v2.csv` holds **803** filers (803 rows, 803 distinct EINs), not 809. 5/803 = 0.62%, so "about 0.6%" stands.
4. **V25A-33, CF vs nationals at $10m.** The headline says "about 3.5–4.5x". The arithmetic (67.2/18.8 = 3.57; 67.2/14.3 = 4.70) gives **3.6–4.7x**, as §3.4 already says.
5. **V25A-35, minimums.** The three medians use different universes. The annual-fee median ($250, n=24) covers published schedules. The opening ($10,000, n=26) and grant ($250, n=10) medians pool all statuses. On published schedules alone the opening median is **$15,000** (n=19).

**Unverifiable:** V25A-17, the 50-state negative ("no state enacted a DAF payout, reporting or donor-intent mandate"). Nothing I read contradicts it, but I did not run a 50-state search, and the doc's own §5 says the CA, IL and CT negatives rest on search results.

**Interpretation challenges** (not verdict-changing):
1. **Watertown (C019).** The transferee is "Watertown Community Foundation Inc" in the same town. Schedule N gives no EIN, and the filer did not file a final return. This looks like a transfer to a same-community successor or affiliate, not a combination of two CFs. It is still the largest filed transfer, but it should not be read as consolidation evidence until the transferee is identified.
2. **AB 2936.** "Not a reporting law" is true because it never passed. Adler & Colvin describe its purpose as "prodding the Attorney General to adopt regulations to require new reporting specifically from DAF sponsors".
3. **White Bear Lake.** 2025-01-31 is the first of seven distributions (to 2025-06-13), not the only date.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V25A-01 | AB 2936: passed Assembly June 2020, held in Senate Judiciary | **Confirmed** | Adler & Colvin verbatim; purpose was DAF reporting rules |
| V25A-02 | AB 1712 (Wicks) failed 2020 | **Confirmed** | MinistryWatch: Wicks; Judiciary 8–2; pulled; exact date not re-read |
| V25A-03 | AB 1353 died at desk 2022-02-01 | **Confirmed** | FastDemocracy actions verbatim; intent-only stays [S] |
| V25A-04 | No CT-DAF form | **Confirmed** | Rulemaking and forms pages list no DAF form |
| V25A-05 | CA AG 2022 DAF report: 57 sponsors, $105.3bn, 95/97/98% | **Confirmed** | PDF created 2022-05-18 |
| V25A-06 | AB 488 / §12599.9 dates; regs 2024–25 | **Confirmed** | All staged dates exact; CA wording not re-read (FindLaw robots 403) |
| V25A-07 | Hawaii Act 205 | **Confirmed** | Approved 2024-07-05; exclusion verbatim; original date 2026-01-01 |
| V25A-08 | Hawaii Act 108 | **Confirmed** | "undue burdens"; 2026-07-01; s.10 2025-07-01 |
| V25A-09 | FPPC Reg. 18424.3 | **Confirmed** | Filed 2021-11-22; operative 2021-12-22 |
| V25A-10 | FPPC memo: 33 of 2,029; $1,242,728 | **Confirmed** | Verbatim; dated 2024-11-08 |
| V25A-11 | Illinois Gives DAF exclusion | **Confirmed** | Rule text and 2025-05-23; P.A. number not re-read |
| V25A-12 | Kansas K.A.R. 92-12-152 | **Confirmed** | Verbatim; effective 2026-04-17 |
| V25A-13 | NY A3632 DAF clause; in committee | **Confirmed** | NY Assembly page; Ways and Means 2025-01-29 and 2026-01-07 |
| V25A-14 | Prop 40 transfer rule; rejected ~52.8% | **Confirmed** | Text verbatim; KTVU 2026-11-09 (unofficial) |
| V25A-15 | 16-AG SPLC letter 2026-05-21 | **Confirmed** | 16 signatures; no deadline; CA release 2026-05-22 |
| V25A-16 | GoFundMe letter; "21 AGs" | **Partially confirmed** | Quotes exact; 19 AGs + 4 secretaries of state, 21 states |
| V25A-17 | No state DAF mandate 2021–26 | **Unverifiable** | Negative over 50 states; not contradicted |
| V25A-18 | Coverage 13/20, $173.8bn, 37 pages | **Confirmed** | Recomputed; MS GIFT robots now 200 but page 502 |
| V25A-19 | Per-page axe counts | **Confirmed** | 21 of 21 re-scanned pages identical |
| V25A-20 | 7 critical pages / 31; 22 serious / 155; 14 clean | **Confirmed** | Recomputed from CSV |
| V25A-21 | Phone hours at 3 of 13; Vanguard no phone | **Confirmed** | Strings verbatim |
| V25A-22 | No quantified response time | **Confirmed** | Vanguard and Dechomai phrases verbatim |
| V25A-23 | No public chat; Fidelity Virtual Assistant | **Confirmed** | No chat-vendor script on 26 pages |
| V25A-24 | AEF placeholder statement; FFTC accessiBe; no WCAG claim | **Confirmed** | Verbatim; acsbapp.com script |
| V25A-25 | Orange & Sullivan + Rockland, 2026-01-01, ~$71m | **Partially confirmed** | Merger and AG approval confirmed; $71m and date not re-read |
| V25A-26 | Coastal → San Diego $10.07m | **Confirmed** | Schedule N $10,072,419; Coast News Aug. 26, brand kept |
| V25A-27 | Keweenaw $10.55m; Rusk $2.14m; Fairfield $4.46m | **Confirmed** | XML sums exact; headline rounds Keweenaw to $10.5m |
| V25A-28 | White Bear Lake → CommunityGiving $4.97m | **Confirmed** | Seven lines = $4,965,262; DAF wording verbatim |
| V25A-29 | Watertown $21.58m, 2025-12-18 as filed | **Confirmed** | Exact; likely same-community successor, not a merger |
| V25A-30 | 5 of 809 filers, 2,795 returns | **Partially confirmed** | Re-run gives 2,795 / 5; filer count is 803 |
| V25A-31 | 34 schedules, 43.0% of assets; status split | **Confirmed** | All counts and shares exact |
| V25A-32 | Medians 100/100/67.2; IQRs; weighted means | **Confirmed** | Exact (exclusive quartiles) |
| V25A-33 | Nationals 60/45/14–19; multiples | **Partially confirmed** | Headline 3.5–4.5x should be 3.6–4.7x |
| V25A-34 | 14 fee schedules spot-checked | **Confirmed** | 14 of 14 tiers, minimums and bps match |
| V25A-35 | Minimums $250 / $10,000 / $250 | **Partially confirmed** | Opening median is $15,000 on published schedules |

### Rulings on the documents' proposals

- **N9 P-B40N9-01** (verify the CA, IL and CT negatives by a permitted route) is supported. V25A-17 stays unverifiable until it runs. The NY Assembly site (nyassembly.gov) is a permitted route for New York.
- **N9 P-B40N9-02 / -03** are supported. The CA/HI exclusion test is verbatim in Hawaii Act 205 (V25A-07), and the IL and KS exclusions are confirmed.
- **N10 P-B40N10-01..03** are supported. Same-day re-runs are deterministic (V25A-19), so the quarterly monitor in P-B40N10-03 is a sound design. MS GIFT's robots.txt was readable at re-check, so the monitor should retry robots outcomes each run.
- **N11 P-B40N11-02** (screen all CF-named filers) is supported. It should record the screened universe as 803 DAFRC filers, and treat Watertown-type transfers as reorganisations until the transferee is identified.

## Exact corrections

### `research/mission-2026-11-14/direction-state-daf-law-tracker.md`
1. **§2.6, GoFundMe letter (governing replacement).**
   - **Find:** "  - **Signatories:** reported as 21 AGs [S]."
   - **Replace with:** "  - **Signatories:** 23 officials from 21 states: 19 attorneys general (CA, DE, IL, KY, MD, MA, MI, MN, NH, NJ, NM, NY, NC, OK, OR, PA, VT, WA, WI) and 4 secretaries of state (MD, PA, SC, TN), per the letter's signature pages. Responses were requested within 14 days [F; V wave 25A]."

### `research/mission-2026-11-14/direction-cf-consolidation-fees.md`
1. **§0, national comparison row (governing replacement).**
   - **Find:** "and about 3.5–4.5x at $10m.**"
   - **Replace with:** "and about 3.6–4.7x at $10m (67.2 bps against 18.8 and 14.3 bps).** [V wave 25A]"
2. **§0, minimums row.**
   - **Find:** "Median opening minimum **$10,000** (n=26; range $0–$100k). Median minimum grant **$250** (n=10)."
   - **Replace with:** "Median opening minimum **$10,000** (n=26; range $0–$100k) and median minimum grant **$250** (n=10). Both pool all statuses, not just published schedules. On the 34 published schedules alone the opening median is $15,000 (n=19) and the grant median $250 (n=4) [V wave 25A]."
3. **§1.1, CF filers' returns.**
   - **Find:** "filed by the 809 CF filers in"
   - **Replace with:** "filed by the 803 CF filers (803 distinct EINs) in"
4. **§2, Findings, item 2 (governing replacement).**
   - **Find:** "Only 5 of the 809 DAFRC CF filers (2,795 returns for 2021+) set Part I line 2 or filed a final return in the window. That is about 0.6% of CF filers over roughly four years."
   - **Replace with:** "Only 5 of the 803 DAFRC CF filers (2,795 returns for 2021+) set Part I line 2 or filed a final return in the window. That is about 0.6% of CF filers over roughly four years. A wave-25A re-run with an empty cache reproduced the 2,795 returns and the same 5 flags (Rusk County, Keweenaw, Watertown Area, Coastal, Greater White Bear Lake) [V wave 25A]."
5. **§2, Findings, item 1.**
   - **Find:** "The largest filed transfer is $21.6m (Watertown), about 0.04% of top-100 CF DAF assets."
   - **Replace with:** "The largest filed transfer is $21.6m (Watertown), about 0.04% of top-100 CF DAF assets. Its transferee, 'Watertown Community Foundation Inc', is in the same town and has no EIN on Schedule N, and the filer did not file a final return. It may be a same-community successor or affiliate rather than a combination of two CFs [V wave 25A]."
6. **§4, Limitations, item 5.**
   - **Find:** "The Schedule N side covers only the 809 DAFRC CF filers"
   - **Replace with:** "The Schedule N side covers only the 803 DAFRC CF filers"
7. **§0, consolidation row.**
   - **Find:** "with about $71m of combined assets [F press]."
   - **Replace with:** "with about $71m of combined assets [F press]. The NY AG's approval is confirmed by Mid-Hudson News (2026-01-30); the $71m and the effective date were not re-read in wave 25A [V wave 25A]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.21:** "### 11.22 New directions N9–N11 (validated, wave 25A)". Renumber if another subsection lands first. It contains:

   > **New directions N9–N11 (validated, wave 25A).** No state has a DAF reporting, payout or donor-intent mandate found for 2021–2026. California's DAF bills all failed: AB 1712 and AB 2936 in 2020, and AB 1353, which died at the desk on 2022-02-01. The California AG has no DAF-specific registration form; its 2022 DAF report (57 sponsors, $105.3bn) created no filing duty. State rules that do name DAFs are narrower:
   > - **Platform laws.** California's AB 488 (Gov. Code §12599.9, in force from 2023; regulations 2024–25) and Hawaii's Act 205 as amended by Act 108 (effective 2026-07-01) treat a DAF sponsor as a regulated platform only if it names charities to people without advisory privileges.
   > - **Political disclosure.** California FPPC Reg. 18424.3 (operative 2021-12-22) makes officials name the sponsor, fund and donor behind DAF-sourced behested payments; 33 of 2,029 state reports used it, totalling $1,242,728.
   > - **Tax credits.** Illinois Gives and Kansas's pregnancy-resource credit (K.A.R. 92-12-152, effective 2026-04-17) exclude DAF gifts.
   > - **Wealth taxes.** New York's pending A3632 would count DAF gifts. California's Proposition 40, whose transfer rule would have done the same, was rejected (about 52.8% no, unofficial).
   > - **AG letters.** Sixteen attorneys general wrote to Fidelity Charitable, Vanguard Charitable and DACG on 2026-05-21 urging them to reconsider SPLC payment holds, with no legal demand. A 21-state letter to GoFundMe (19 AGs and 4 secretaries of state, 2026-03-03) demanded disclosure of "the role and nature of any DAF sponsor".
   >
   > Among the top-20 sponsors, 13 sites ($173.8bn of $250.6bn) could be scanned. Automated axe-core checks found critical WCAG failures on 7 of 37 pages, at NPT, Vanguard, SVCF and NCF, and serious failures (mostly colour contrast) on 22. A same-day re-scan of 21 pages reproduced every count. These are partial automated checks, not a ranking. No readable sponsor publishes a response-time promise, a public chat channel or a WCAG conformance claim. Three publish phone hours, AEF's accessibility statement is placeholder text, and FFTC relies on the accessiBe overlay.
   >
   > Community-foundation consolidation in 2021–2026 was small. No two top-100 CFs combined, and only 5 of 803 DAFRC CF filers reported a >25% disposition or final return. The largest events were Orange & Sullivan with Rockland (NY AG-approved; about $71m), Coastal CF into San Diego Foundation ($10.07m), Keweenaw into the CF of the Upper Peninsula ($10.55m) and a $21.6m Watertown transfer that may be a reorganisation. 34 top-100 CFs (43% of top-100 CF DAF assets) publish a full fee schedule. Their median admin fee is 100 / 100 / 67 bps at $100k / $1m / $10m, about 1.7x, 2.2x and 3.6–4.7x the national sponsors' 60 / 45 / 14–19 bps, before investment costs. [V wave 25A]

`research/mission-2026-11-14/direction-sponsor-accessibility-service.md` needs no change.

## Data-file notes (not .md; for the owning agent)

- **`state-daf-law-tracker-2021-2026.csv`, T18:** replace "Signatory count reported as 21 AGs (secondary)" with "23 signatories from 21 states: 19 AGs + secretaries of state of MD, PA, SC, TN (letter signature pages)" and change the label to F.
- **`cf-consolidation-2021-2026.csv`:**
  - C019: add to the notes "transferee in same town, no EIN on Schedule N, filer not a final return; may be a successor/affiliate reorganisation".
  - C018: note that the $4,965,262 is seven distributions dated 2025-01-31 to 2025-06-13.
- **`queue-proposals-batch40-n11.csv`:** if any row or note says 809 filers, change it to 803.
- **`sponsor-a11y-axe-2026.csv`, `sponsor-service-levels-2026.csv`, `cf-daf-fee-census-2026.csv`:** no change. The re-scanned rows match exactly, and the census statistics and the 14 spot-checked rows reproduce.
- **Compliance check for the N11 owner.** At re-check, robots.txt on www.sacregcf.org and www.bcf.org returned 403 to a generic browser UA. Under the doc's own rule (403 means disallow all), confirm that the robots outcome recorded when the Sacramento page and the Baltimore PDF were fetched was 200/404. The outcome may depend on the UA.

## Limits

- **robots.txt read first** on every host fetched:
  - Allowed (200) and fetched: oag.ca.gov (with a delay of 11 s or more between fetches), fppc.ca.gov, data.capitol.hawaii.gov, sos.ks.gov, law.cornell.edu, nyassembly.gov, ag.state.mn.us, ag.ny.gov, fastdemocracy.com, adlercolvin.com, ministrywatch.com, sos.ca.gov, ktvu.com, midhudsonnews.com, rocklandtimes.com and thecoastnews.com.
  - Sponsor sites (200), fetched through Playwright: fidelitycharitable.org, nptrust.org, vanguardcharitable.org (and its go. subdomain), svcf.org, aefonline.org, renaissancecharitable.org, ncfgiving.com, impactassets.org, fftc.org, growyourgiving.org, greaterhorizons.org, cjp.org and dechomai.org.
  - CF fee hosts (200): donorportal.cct.org, thenytrust.org, oregoncf.org, cfgreateratlanta.org, ghcf.org, seattlefoundation.org, cfmt.org, oc-cf.org, desmoinesfoundation.org, racf.org and delcf.org. columbusfoundation.org returned 404, so it publishes no rules.
  - cdnjs.cloudflare.com and the GivingTuesday S3 mirror return 404 for robots.txt (no rules). morganstanley.com returned 200, but the GIFT page returned 502.
  - nysenate.gov allows `/legislation/`, but the bill page returned 403. pittsburghfoundation.org allows the page, but it returned 403.
- **Not fetched (robots.txt unreadable or 403):** codes.findlaw.com, radiocatskill.org, www.sacregcf.org, www.bcf.org, www.dafgiving360.org and www.raymondjamescharitable.org (timeout). Per the doc, leginfo, LegiScan, ilga.gov and cga.ct.gov were not tried. **crt.sh and fcsuite.com were not used.**
- **Not re-run or not re-read:**
  - axe on the other 16 of the doc's 37 pages; the axe "incomplete" counts; help-page question counts;
  - fee schedules other than the 14 listed (including Pittsburgh, Baltimore and Sacramento); the 56-quote verification step; the crawl and URL tasks;
  - the press-only consolidation rows (Lodi, Dunkirk, Idaho, Three Rivers, Leichtag, Berks, Maine Women's Fund, Teton Valley) and the local-XML Schedule N rows (Shelby, Milbank, Oracle Health);
  - the NY *Pennies for Charity* report, the Alaska suits, RCW 82.87.080, Kentucky SB 70 and the Massachusetts guidance;
  - the Illinois emergency rule, P.A. 103-592 and the credit start date; the certified Prop 40 result.
- **Scratch:** all downloads, caches and re-run outputs were kept in the session scratchpad and deleted after use. No repo file other than the two outputs named above was written.
