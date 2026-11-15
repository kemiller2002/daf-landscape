# Validation wave 26: new directions N15–N18 (faith giving platforms, gift-office DAF handling, recipient compliance screen, corporate DAFs)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave26.
**Register:** [`validation-register-wave26.csv`](../../data/mission-2026-11-14/validation-register-wave26.csv), rows V26-01 to V26-37.
**Documents validated:**
- N15: [direction-faith-giving-platforms.md](direction-faith-giving-platforms.md) and `faith-giving-platform-daf-support-2026.csv` (23 rows)
- N16: [direction-gift-office-daf-handling.md](direction-gift-office-daf-handling.md) and `gift-office-daf-policies-2026.csv` (41 rows)
- N17: [direction-recipient-compliance-screen.md](direction-recipient-compliance-screen.md), `recipient-compliance-screen-top50.csv` (5,296 rows) and `scripts/mission_recipient_compliance.py`
- N18: [direction-corporate-dafs.md](direction-corporate-dafs.md), `corporate-daf-programs-2021-2026.csv` (49 CD + 5 SA rows) and `relationship-graph-edges-additions-24.csv` (25 rows)

**Method:** public sources only. I did not log in, submit forms, solve or bypass CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching any page on it, checking the `*`, ClaudeBot and anthropic-ai groups. Hosts whose robots.txt could not be read were not fetched. **I did not use crt.sh.** SEC EDGAR Archives and irs.gov bulk files were read with a generic User-Agent. For each claim I formed a verdict from the primary source first and compared it with the documents afterwards. The sources were:
- **N15:**
  - church platforms: the Pushpay digital-giving page; Overflow's launch post and DAF page; Subsplash's DAF guide and product post; Planning Center's 2024-09-12 post; Tithely (home and giving software); Givelify (home and giving); Ministry Brands Kindrid; ACST Realm giving; the Vanco–ACST release;
  - sponsors: NCF support and charities pages; the JCF NY Policy Guide (Aug 2024) and 2023 Giving Report (pdftotext); JCF LA grantmaking guidelines; the Fidelity Charitable 2026 Giving Report;
  - repo recompute: `daf-grant-recipient-sectors-top50.csv` and `nonprofit-donate-page-daf-scan-2026.csv`.
- **N16:**
  - recipients: Caltech Gift Policies 2024-10-01; Stanford Live guidelines (Cloudinary PDF); WashU DAF page; Chicago Booth how-to-give; Duke gift-planning DAF page; Ohio State Priority Points; Notre Dame's 2025-11-19 post; Yale DAF page; Columbia gift-planning DAF page;
  - sponsors: Fidelity's pledge and gala FAQs; the Vanguard Charitable P&G (January 2026); the live Daffy Member Agreement;
  - the scanned donate URLs for Notre Dame (`giving.nd.edu`) and WashU (`wustl.advancementform.com`), and the scan CSV rows.
- **N17:**
  - fresh downloads of the IRS Pub 78 and Auto-Revocation zips (sizes and Last-Modified identical to the doc), and a HEAD check of `eo1.csv` (Last-Modified 2026-11-09);
  - a **re-run of `mission_recipient_compliance.py`** in scratch, with OUT redirected and on the session's existing Schedule I line cache (94 files) and BMF copy. Its output CSV is **byte-identical** to the repo CSV;
  - a direct grep of 12 named hits in the revocation, Pub 78 and BMF files.
- **N18:**
  - EDGAR Archives: the Apollo 2026 proxy, Urban Outfitters FY2026 10-K, Cognizant 2023 proxy, Circle 2025 10-K and 2026 proxy, Braze FY2022 and FY2026 10-Ks, and Brilliant Earth 2025 10-K;
  - the SVCF FY2025 audited statements; the Fidelity 2026 Giving Report; the AOGF FYE 2026-03 990 XML (fresh fetch).

## Headline

The four documents hold up well. 31 of 37 claims are confirmed, 5 partially confirmed and 1 unverifiable. None is contradicted. **The compliance screen reproduces exactly**, and no wording in it calls any grant improper.

**What holds independently:**
- **N15 faith platforms:**
  - Overflow's Chariot launch is dated Jun 29, 2023.
  - Pushpay shows "DAF Attribution — Coming soon" and lists "DAF/IRA Automation" as landing next ($62.9B cumulative).
  - Subsplash and Planning Center are record-only. Subsplash's guide (October 1, 2026) gives the legal-name/EIN/button/no-receipt advice and does not mention DAFpay or Chariot.
  - Tithely, Givelify, Kindrid and ACST Realm/Vanco have no DAF text on the pages read. Their scale figures are as quoted.
  - NCF pays "via ACH or electronic transfer when available", with a wire costing about $25.
  - JCF NY's grants go by "check or electronic funds transfer (ACH or wire) at the discretion of JCF staff". FY2023: $907.9M granted, Religion $81.4M, 77,364 grants, median $750 (average $11,639), 99% share fundholder details.
  - JCF LA: ACH in 24–48 hours; mailed checks up to four weeks.
  - Fidelity 2026: religion 27% of grants and 13.1% of dollars; $5,801 average; implied religion average $2,815.
  - Repo recompute: religion $10.55bn across 55,993 recipients (13.64%). The 22 top-300 recipients hold $1.580bn (14.98%); 14 scanned pages hold $0.838bn (7.94%), with 3 of 14 showing a DAF option and 0 DAFpay.
- **N16 gift offices:** the following are verbatim on the live pages or PDFs:
  - Caltech: pledge payment allowed if not mentioned; soft credit for DAFs; statement of intent.
  - Stanford Live: pledge clause, and the Bing Fling invitation withheld at $7,500+ (CDN stamp 2024-03-28).
  - WashU: "Under Internal Revenue Code regulations…"; DAF Direct with Fidelity, DAFgiving360 and BNY.
  - Booth: pledge bar; DAFpay.
  - Duke: "non-binding intention"; Iron Dukes.
  - Fidelity: "non-legally binding pledges" and the "Pledge (non-binding)" use code; no "split" gifts.
  - Vanguard: "Bifurcated grants" and "Fulfillment of legally binding pledges" are impermissible.
  - Daffy: "pre-existing, legally-binding" pledges barred; neither portion of a $200/$100 ticket payable; naming rights incidental.
  - Notre Dame's DAFpay post is dated November 19, 2025. Yale's DAF minimum is $5 million.
- **N17 compliance screen:** every figure checked reproduces to the dollar:
  - 604,915 lines, $91,020,008,186;
  - revocation hits 1,837 lines, $74,756,533 (0.0821%). Of these, $53,115,784 are back in the lists, $21,640,749 are not, and $10,477,177 are posted and unexplained;
  - Pub 78 absent $8,013,036,257, split into $3,649,597,540 in the BMF and $4,363,438,717 in neither;
  - unexplained absent-both $818,725,018 (6,338 EINs);
  - segment rates: national 0.074%, CF 0.112%, single-issue 0.094%; unexplained 0.97% / 0.87% / 0.54%.
  - All 12 spot-checked revocation hits match the IRS list on revocation date, posting date and today's Pub 78/BMF status. Per-EIN sums equal the doc's amounts.
- **N18 corporate DAFs:**
  - Fidelity 2025: 556 corporate DAFs, more than 550 companies, $539.8M, 26,036 grants, $20,732 average.
  - SVCF corporate-advised grants: about $153m (2025) and $189m (2024), against $2,051m and $3,077m of donor-advised grants (6.9% and 5.8%).
  - AOGF: 695 accounts, $1,390,021,897 of grants, $1,557,848,744 of contributions, $205,671,333 at EOY.
  - Apollo $200m in shares; Urban Outfitters $46.0m; Cognizant "In late 2022 … converted the Global Foundation into a donor-advised fund".
  - Circle Foundation is "a donor-advised fund housed with Fidelity" (2026 proxy).
  - Braze–Tides MOU (FY2022 10-K); Brilliant Earth–SVCF corporate advised fund.
  - CSV tallies: 49 programs, 26 with no sponsor named, Tides 8, SVCF 4, Fidelity 3.

**What needs correcting or qualifying:**
1. **Ohio State scope (N16, V26-16).** The FAQ says "Per Charles Schwab DAF giving 360, gifts from **this** Donor Advised Fund cannot count towards Priority Points …". Read as written, that is a DAFgiving360 rule. The doc generalises it to all DAF gifts in three places. The IRA exclusion is attributed separately ("Per IRS guidelines").
2. **"All five sponsors read" (N16, V26-19).** Only Fidelity, Vanguard and Daffy were read first-hand. NPT is [S] with its events rule "not read", and DAFgiving360 is [R].
3. **In-house DAF count (N16, V26-20).** The CSV tally of 12 is right. But 10 of the 12 rest on search text only, and 7 of the 33 recipients were not read, so it is a floor.
4. **Donate-page misses (N16, V26-21).** Chicago's scan row is `home_only_donate_robots_blocked`: `givetoday.uchicago.edu` disallows the form path, which I re-checked. Its 0 is therefore not a scan miss, so **four** recipients conflict, not five: Stanford, Columbia, Notre Dame and WashU. For Notre Dame and WashU, today's static HTML at the scanned URLs has no DAFpay, Chariot, donor-advised or DAF Direct string. The tools sit in checkout or on a separate DAF page, not on the scanned URL.
   - **On 41.2%:** it should **not** be revised. 75/182 is an accurate count of DAF options visible on the scanned donate URLs. It should be labelled a lower bound for large universities. Counting the four would give 79/182 = 43.4%.
5. **LLC label (N17, V26-26).** The $1.68bn is the whole LLC-name label (75 lines). The four CZ Biohub/Institute LLCs are $1,656.6m of it, and about $21m is other LLC-named recipients.
6. **AOGF Schedule O (N18, V26-34, confirmed with a note).** Schedule O also puts "various other fund structures that are consistent with conventional DAF models" in the DAF-model group, so the 695-account column may not be wholly corporate.
7. **EDGAR full-text counts (N18, V26-30).** `efts.sec.gov/robots.txt` returned 403 on 2026-11-15, so the counts were not re-run: 211 10-K documents and 100 filers, 146 proxy documents and 64 filers, and 33 of 100 10-K filers describing their own program. The Archives filings were checked instead.
8. **Circle (N18, V26-37).** Fidelity is named in the 2026 proxy only. The 2025 10-K says "a donor-advised fund" without naming the sponsor.

## Limits

- **Not fetched:**
  - `efts.sec.gov` (robots 403);
  - `givetoday.uchicago.edu` (the donation-form path is robots-disallowed for `*` and Claude agents).
- **N17 re-run inputs.** The re-run used the session's existing Schedule I line cache and BMF copy, so it is a reproduction of the computation, not an independent re-download of the 94 return XMLs. The IRS Pub 78 and revocation inputs were fresh downloads.
- **Static HTML only.** Platform and donate pages were read as static HTML, and client-rendered content could differ. The faith doc's `not_found` wording is appropriate for that reason.
- **Not re-checked in this wave:**
  - N15: the Chariot partner lists and Thrivent post; WaterStone; JUF; LDS; CCF Minnesota; Endaoment; Fidelity's nonprofit FAQ;
  - N16: the [S] recipients, Columbia's $1m minimum (not in static text), the NPT search text and Notice 2017-73;
  - N18: Tides and CAF America Schedule D, and most of the 49 individual filings (4 were spot-checked);
  - the 25 relationship edges, beyond EX001 (Circle → Fidelity).

## Exact corrections

### `research/mission-2026-11-14/direction-gift-office-daf-handling.md`
1. **§0, events row, Ohio State.**
   - **Find:** "Ohio State Athletics: DAF gifts do not count toward Priority Points or \"overall giving to the University/Athletics\" [F]. It attributes the rule to DAFgiving360."
   - **Replace with:** "Ohio State Athletics: gifts from DAFgiving360 do not count toward Priority Points or \"overall giving to the University/Athletics\" [F]. The page states the rule only for that sponsor (\"Per Charles Schwab DAF giving 360, gifts from this Donor Advised Fund cannot count\"). It is silent on DAF grants from other sponsors [V wave 26]."
2. **§0, events row, sponsors.**
   - **Find:** "All five sponsors read bar ticket benefits, and Fidelity, Vanguard and Daffy expressly bar bifurcation [F]."
   - **Replace with:** "The three sponsors read first-hand (Fidelity, Vanguard and Daffy) bar ticket benefits and expressly bar bifurcation [F]. NPT ([S]) and DAFgiving360 ([R]) were not read [V wave 26]."
3. **§0, recognition row.**
   - **Find:** "Ohio State Athletics excludes DAF gifts from priority credit [F]."
   - **Replace with:** "Ohio State Athletics excludes DAFgiving360 gifts from priority credit [F; scope per V wave 26]."
4. **§0, acceptance row.**
   - **Find:** "**12 of the 33 also run their own DAF**, with stated minimums from $100k (Cornell [S], Mayo [S]) to $5m (Yale [F])."
   - **Replace with:** "**At least 12 of the 33 also run their own DAF**, with stated minimums from $100k (Cornell [S], Mayo [S]) to $5m (Yale [F]). Ten of the 12 rest on search text only, and 7 of the 33 were not read [V wave 26]."
5. **§2, Ohio State row.**
   - **Find:** "| Priority Points and levels exclude DAF and IRA gifts |"
   - **Replace with:** "| Priority Points and levels exclude IRA gifts (\"Per IRS guidelines\") and DAFgiving360 gifts (\"Per Charles Schwab DAF giving 360\") [V wave 26] |"
6. **§4, Chicago bullet.**
   - **Find:** "- Chicago: DAFpay on Booth's form."
   - **Replace with:** "- Chicago: DAFpay on Booth's form. The scan's donate host (`givetoday.uchicago.edu`) was robots-blocked (`home_only_donate_robots_blocked`), so, as with Cornell, this 0 is not a scan miss [V wave 26]."
7. **§4, conclusion.**
   - **Find:** "For the other five, the scan's 0 conflicts with the giving pages. So the scan's DAF-option shares are probably a lower bound for large universities (P-B41N16-02)."
   - **Replace with:** "For the other four (Stanford, Columbia, Notre Dame and WashU), the scan's 0 conflicts with the giving pages. On 2026-11-15, the static HTML of the scanned Notre Dame and WashU URLs carried no DAFpay, Chariot, donor-advised or DAF Direct string, so the tools sit one step deeper or on a separate DAF page. The scan's DAF-option shares are therefore a lower bound for large universities (P-B41N16-02). The donate-page figure of 75/182 (41.2%) stays as a donate-URL measure. Counting these four would give 79/182 (43.4%) [V wave 26]."

### `research/mission-2026-11-14/direction-nonprofit-donate-pages.md`
1. **§5 Limitations, new bullet after the sample-definition bullet.**
   - **Find:** "- **Sample definition.** The sample follows filed Schedule I dollars (>$5,000 lines, domestic recipients) from the top-50 sponsors only. Government units and LLCs not in the BMF are excluded."
   - **Replace with:** "- **Sample definition.** The sample follows filed Schedule I dollars (>$5,000 lines, domestic recipients) from the top-50 sponsors only. Government units and LLCs not in the BMF are excluded.\n- **Depth (wave 26).** Four large universities scanned as 0 (Stanford, Columbia, Notre Dame and WashU) offer DAFpay or DAF Direct one step past the scanned URL, at checkout or on a separate DAF page. The 75/182 (41.2%) figure is correct for the scanned URLs and is not revised. It is a lower bound for any DAF option at the institution; counting the four gives 79/182 (43.4%) [V wave 26]."

### `research/mission-2026-11-14/direction-recipient-compliance-screen.md`
1. **§0, absent-both labels.**
   - **Find:** "- CZ Biohub/Institute LLCs (possible disregarded entities) **$1.68bn**;"
   - **Replace with:** "- LLC-named recipients (possible disregarded entities) **$1.68bn** (75 lines), of which the four CZ Biohub/Institute LLCs are $1.66bn [V wave 26];"
2. **§2.4, Fidelity EIN row.**
   - **Find:** "| That EIN was revoked 2019-11-15 |"
   - **Replace with:** "| That EIN was revoked 2019-11-15. The revocation record's name is \"Fidelity Investments Charitable Gift Fund Foundation Inc\" [V wave 26] |"

### `research/mission-2026-11-14/direction-corporate-dafs.md`
1. **§1 Method, EDGAR search.**
   - **Find:** "1. **EDGAR full-text search** (`efts.sec.gov/LATEST/search-index`), forms 10-K and DEF 14A, 2021-01-01 to 2026-11-15:"
   - **Replace with:** "1. **EDGAR full-text search** (`efts.sec.gov/LATEST/search-index`), forms 10-K and DEF 14A, 2021-01-01 to 2026-11-15. In wave 26, `efts.sec.gov/robots.txt` returned 403, so these counts could not be re-run under the robots convention. The program rows were checked in EDGAR Archives instead [V wave 26]:"
2. **§0, AOGF.**
   - **Find:** "Schedule D DAF column of **695 accounts, $1,390.0m of grants**, which Schedule O describes as corporate, with ongoing advice [X]."
   - **Replace with:** "Schedule D DAF column of **695 accounts, $1,390.0m of grants**, which Schedule O describes as corporate, with ongoing advice [X]. Schedule O also places \"various other fund structures that are consistent with conventional DAF models\" in this group, so the column may not be wholly corporate [V wave 26]."
3. **§2.1, Circle row source.**
   - **Find:** "| **Fidelity Charitable** | Circle (Circle Foundation) |"
   - **Replace with:** "| **Fidelity Charitable** (named in the 2026 proxy only; the 10-K says \"a donor-advised fund\") [V wave 26] | Circle (Circle Foundation) |"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after the last §11 subsection.** Add "### 11.23 New directions N15–N18 (validated, wave 26)", containing the paragraph below. If §11.23 is already taken, use the next free number.

   > **New directions N15–N18 (validated, wave 26).**
   > - **Faith giving.** Church giving platforms do not offer DAF grants at checkout.
   >   - Only Overflow does, through Chariot since June 2023. Pushpay lists DAF attribution as "coming soon".
   >   - Subsplash and Planning Center record DAF gifts after the fact. Tithely, Givelify, Kindrid and ACST/Vanco show nothing.
   >   - Faith sponsors pay congregations directly. NCF pays by ACH or electronic transfer, and JCF NY by check or ACH/wire at staff discretion. JCF NY's median grant is $750.
   >   - Religion is 27% of Fidelity's grant count but 13.1% of its dollars (implied average about $2,815). In the repo's Schedule I it is 13.6% of dollars across 55,993 recipients. The 22 top-300 religion recipients hold only 15% of religion's $10.55bn, and none of the scanned ones is a congregation.
   > - **Gift offices.** Recipients split on whether a DAF grant can pay a pledge.
   >   - Caltech and Stanford Live allow it if the sponsor does not mention the pledge. WashU and Chicago Booth bar it. Duke books only a "non-binding intention".
   >   - Fidelity accepts non-binding pledges. Vanguard and Daffy bar binding ones, and all three bar bifurcated event payments.
   >   - Ohio State Athletics excludes DAFgiving360 gifts from priority points.
   >   - At least 12 of the 33 largest university and AMC recipients run their own DAF.
   >   - Four large universities offer DAFpay or DAF Direct one step past the scanned donate URL. The donate-page share of 41.2% is therefore a lower bound (43.4% counting them).
   > - **Recipient compliance.** Screening 604,915 top-50 Schedule I lines ($91.02bn) against IRS lists finds:
   >   - 0.082% ($74.8m) went to EINs under a revocation in effect at the time. $53.1m of those recipients are listed again today, and only $10.5m is posted, unlisted and unexplained.
   >   - The $8.01bn absent from Pub 78 is mostly subordinates, churches, governmental units and CZ Biohub LLCs. $0.82bn (0.90%) is unexplained and most likely EIN error.
   >   - These are screening hits, not findings of improper grants. The script reproduces exactly.
   > - **Corporate DAFs.** 49 company programs appear in 2021–2026 filings. Tides is the most-named sponsor (8), then SVCF (4) and Fidelity (3), and 26 programs do not name a sponsor.
   >   - Published corporate splits: Fidelity, 556 corporate DAFs granting $539.8m in 2025; SVCF corporate-advised funds, about $153m (2025) and $189m (2024); AOGF/Benevity, 695 DAF-column accounts granting $1.39bn (FYE 2026-03).
   >   - Notable programs: Apollo's $200m share-funded DAF, Urban Outfitters' $46m prefunding, Cognizant's 2022 conversion of its foundation to a DAF, and Circle's Pledge 1% DAF at Fidelity.

## Data-file notes (not .md; for the owning agent)

- **`gift-office-daf-policies-2026.csv`:**
  - GO-24 (Ohio State): scope `membership_priority_naming` and `recognition_and_campaign_credit` to "DAFgiving360 gifts (as stated); IRA gifts per IRS".
  - GO-16 (Chicago): add to `notes` "donate host robots-blocked in scan; 0 is not a scan miss".
- **`recipient-compliance-screen-top50.csv`:** no change. The re-run output is byte-identical.
- **`corporate-daf-programs-2021-2026.csv` CD01 and `relationship-graph-edges-additions-24.csv` EX001:** add "Fidelity named in the 2026 proxy only; not in the 2025 10-K".
- **`faith-giving-platform-daf-support-2026.csv`:** no change.
