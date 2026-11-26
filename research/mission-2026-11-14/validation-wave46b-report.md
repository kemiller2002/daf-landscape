# Validation wave 46B: grant-count rates, in-portal data provider, tax pages 11–25, pass-through recipients

**Validator:** validator wave 46B · **Date:** 2026-11-20 · **Register:** [`validation-register-wave46b.csv`](../../data/mission-2026-11-14/validation-register-wave46b.csv) (53 rows, V46B-01 to V46B-53)

**Studies validated (pre-validation):**
1. [g1913-02-grant-count-denominators.md](g1913-02-grant-count-denominators.md), with its two CSVs and `scripts/mission_grant_count_rates.py`;
2. [b43n26-01-in-portal-data-provider.md](b43n26-01-in-portal-data-provider.md), with its CSV and script;
3. [b4142-04-tax-page-audit-11-25.md](b4142-04-tax-page-audit-11-25.md), with its CSV, `scripts/mission_tax_page_audit_11_25.py` and the engine `scripts/mission_tax_scenarios.py`;
4. [b39n6-03-pass-through-recipients.md](b39n6-03-pass-through-recipients.md), with its CSV and `scripts/mission_pass_through_recipients.py` (report stage only).

**How the checks were done.**
- **Scripts.**
  - Every script was run with `python3 -B` or `-I`.
  - Where a script writes into the repo, it was run in a scratch root, or with `--out` pointing to scratch.
  - The in-portal script could not be run, because a permission prompt blocked it. Its tallies were recomputed from the CSV with the csv module.
- **Recomputation.** Independent recomputations (Poisson intervals, 2026 tax arithmetic, 990 sums) used my own stdlib code, not the authors' functions.
- **Fetching.**
  - robots.txt was read first on every host, with ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot groups checked.
  - User agent `research-script/1.0`.
  - No foundant.com host, no fcsuite.com, no secure.ncfgiving.com, no crt.sh, certspotter or sec.gov.
  - congress.gov disallows Claude agents, so law text came from govinfo.gov and LII.
- No logins, forms or outreach. No repo file was edited except the two outputs. Nothing was committed.

---

## 1. Counts by study and result

| Study | Rows | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---:|---:|---:|---:|---:|
| 1. Grant-count denominators (g1913-02) | 11 | 10 | 1 | 0 | 0 |
| 2. In-portal data provider (b43n26-01) | 14 | 8 | 3 | 0 | 3 |
| 3. Tax-page audit 11–25 (b4142-04), incl. 5 law parameters | 15 | 11 | 2 | 1 | 1 |
| 4. Pass-through recipients (b39n6-03) | 13 | 9 | 4 | 0 | 0 |
| **Total** | **53** | **38** | **10** | **1** | **4** |

---

## 2. Findings

### 2.1 Grant-count denominators (g1913-02)

- **Reproduction.**
  - `mission_grant_count_rates.py`, re-run in a scratch root, produced a CSV byte-identical to the committed 66 rows.
  - A separate bisection on the Poisson CDF gives Fidelity n = 27 → [17.79, 39.28], as stated. Every other interval checked also matches.
- **Primary counts.** Fetched and matched:
  - Fidelity 2,664,446 (2025 Giving Report appendix);
  - Vanguard 221,825 in the FY2024 990 (period to 30 June 2024) against 240,064 in the CY2024 report;
  - GS "approximately 29,254" and RCF "over 160,000" (both CY2024 990s);
  - AEF's 51 state rows, which sum to 109,708 grants and $1,302,541,225 (marked estimated);
  - MS GIFT's 122,000.
- **The DAFgiving360 reprint is acceptable.** The NonProfit PRO page reproduces the release and is labelled "Source: DAFgiving360". Its period matches, and its $6.6bn implies about $6,000 per grant, in line with the study's $6,019. The 990 states no count.
- **The pooled rate is mostly Fidelity.** Fidelity supplies 27 of the 28 review-venue records and 57% of the 4.67m grants. Without the DAFgiving360 count the pooled rate would be 0.0133, not 0.0102.
- **AOGF bound.** At most 2.32 per 10,000 grants a year, on 40,985 Schedule I lines (counted in the XML). The bound is mechanically correct.
- **The 5.88-year vs one-year mismatch is real but small.** For Fidelity, summing yearly counts over the window gives 14.99m grant-years against the 15.67m assumed. That is +4.5% on the rate (0.0180 against 0.0172).

### 2.2 In-portal data provider (b43n26-01)

- **Confirmed verbatim:**
  - NPT's GivingPoint GuideStar quote, with dates 2021-07-29 and 2026-02-09;
  - AEF's platform "powered by Ren" and its name/EIN search;
  - the Giving Compass/Ren announcement, which is future tense;
  - the three CF portal guides (Tampa Bay, CNYCF, Santa Cruz);
  - NCF's own pre-screened list.
- **The NPT "ND" in [direction-charity-ratings-integrations.md](direction-charity-ratings-integrations.md) §3 should be corrected.**
  - NPT's own article names GuideStar as its search database.
  - The basis for the old code, "own due-diligence articles name no vendor", is also wrong. NPT's 2024 due-diligence article names Guidestar, Charity Navigator and BBB WGA.
  - The correction is written below.
- **MS GIFT does name a vendor, though not a data vendor.** The same How it Works PDF says "Back office administration provided by Ren". Under the study's own vendor-level logic for AEF, MS GIFT belongs with the Ren clients.
- **Charity Navigator "never in a portal" holds only as "not found".**
  - Giving Compass, which is announced as Ren's data layer, says its tools are "built in collaboration with … Charity Navigator".
  - So CN-linked data has a possible route into a portal, though none is shown live.
- **Stale and inconsistent items:**
  - The §0 script tallies predate the IPD-014 withdrawal. The CSV has 20 rows, embedded 6 and vendor-level 6, against 21, 7 and 7 in the text.
  - §3.7 still cites a foundant page ("700+ … per its own page").
  - IPD-015's Tech Impact quote names Charity Check, a status product, and GuideStar for Grant Applications, which serves applicants. By the study's own akoyaGO rule that is eligibility_only. The embedded reading rests on the CF guides.
- **Robots doubts:**
  - **donorportal.cct.org.** Its robots.txt is the single line `User-agent: * Allow: /index.html Disallow: /`. Parsers read it as no rules, but it evidently intends to block everything except /index.html. The CCT guide quote should be treated as doubtful. I did not fetch it.
  - **www.reninc.com.** It has an `Anthropic-AI` group that only allows /faqs/ and disallows nothing. Read literally, the Ren blog is permitted. I did not re-fetch it.
  - **jcfny.org.** It served a Cloudflare challenge, which I did not bypass, so the JCF rows are unverifiable here.

### 2.3 Tax-page audit, ranks 11–25 (b4142-04)

- **Reproduction.**
  - The audit script, re-run in a scratch root with `--write`, produced a CSV byte-identical to the committed one (58 rows; 18 correct, 13 outdated, 1 arithmetic error, 10 ambiguous).
  - The served JS bundle (same hash) gives the formulas stated in the study:
    - g = ⌊(c + other − std) × rate⌋, with v and b using 2c and 3c;
    - `std-married` = 32200;
    - r1–r4 routing as stated;
    - securities h = c(1 + rate).
- **The tax-calculator overstatements are confirmed by hand.** H3: $17,836 against $21,386 (+19.9%). H4: $220,234 against $372,886 (+69.3%). H2 bunched: $5,112 against $5,472 (+7.0%). H1's §170(p) saving is $720 (2,000 × 12% × 3, with no floor, because §170(p) disregards (b)(1)(I)).
- **Contradicted: the securities-calculator direction.** The figures reproduce, but the comparison is not like for like.
  - Fidelity's sell case donates the proceeds net of capital-gains tax. The repo's sell-then-give donates the full FMV.
  - On Fidelity's own counterfactual, 2026 law gives $5,448 (H2), $38,766 (H3) and $227,178 (H4). The calculator therefore **understates** by 18%, 15% and 3.5%, mainly because it omits the 3.8% NIIT.
  - The missing floor and cap matter little here: for H3, 37¢ against 35¢ on c is worth about $480.
- **BofA.**
  - The "0.05%" footnote is confirmed verbatim.
  - The $30M example cannot be reproduced from its stated inputs. The engine and my hand calculation give $2.84M against $4.09M.
  - The slide's ~$2.0M saving equals 20% of the $10M of gain avoided. That holds only if both cases get the same deduction. Here they do not: the in-kind business interest is limited to 30% of the $20M AGI ($6M in year 1), while the $10M cash gift after the sale fits within 60% of $30M.
- **Columbus.** The "at least 1 percent … in order to qualify" wording is confirmed. `ambiguous` is fair.
- **CJP and DonorsTrust are outdated, as stated.** The DonorsTrust guide was "last revised June 2025", before the 4 July 2025 enactment. It is stale, not wrong when issued.
- **JCF.** The "35% of AGI" and corporate wording could not be re-read (Cloudflare).
- **2026 law: all five engine parameters confirmed in primary text.**
  - **0.5% floor.** P.L. 119-21 §70425, new §170(b)(1)(I), with ordering D, C, B, E, A, G and carryforward only from years with a percentage-limit excess.
  - **"35% cap".** §70111, new §68: 2/37 of the lesser of itemized deductions or taxable income above the start of the 37% bracket. It is not a cap on AGI, and it covers all itemized deductions.
  - **Non-itemizer deduction.** §70424, $1,000/$2,000. §170(p) excludes 509(a)(3) organisations and DAFs and disregards the floor.
  - **Corporate floor.** §70426: deductible above 1% and up to 10% of taxable income.
  - **Standard deduction.** Rev. Proc. 2025-32 §4.14: $32,200 MFJ. The 0%/15% maxima of $98,900/$613,700 and the 37% start of $768,700 also match.

### 2.4 Pass-through recipients (b39n6-03)

- **Reproduction.**
  - The pure `report` stage was re-run on the author's cached filings (output to scratch). Every dollar and 990 column matched for all 28 rows.
  - Population: $3,237,961,912, 4.14% / 4.29%. Core 10: $1,766,251,979, 2.26% / 2.33%. Within-set flow: $183,084,596.
  - The cache had no web.json, so the web columns could not be regenerated.
- **990 XML spot checks:**
  - Blue Meridian granted $792,472,499 against $470,245,855 contributed; net assets fell $344,125,454.
  - NVF granted $1,052,887,016 against $1,251,041,744 contributed; net assets fell $360.7m.
  - Climate Imperative paid Energy Foundation China $27.0m + $29.75m = $56.75m, and US EF $34.74m.
- **Individual shares and onward ratios recompute exactly.** Core 0.865 (0.828 net of intra-set flows); named 7 0.829 (0.807).
- **No-DAF route.** Spot checks agree: NVF `/donate` returns 404, and the Blue Meridian FAQ shows partner tiers ($50m/$15m) and no DAF text.
- **Scan artefacts confirmed.** UCLA Foundation returns a 301 to mygiving.ucla.edu, Bright Funds a 302 to hello.brightfunds.org, and Homewise has a `/donate/` page reading "Contact us to have a conversation".
- **Judgement: the core-10 hand classification is reasonable and conservative.** Edge cases:
  - Charter School Growth Fund filed a 990-PF for 2023;
  - Our American Future Foundation (a single-recipient conduit) and Bright Funds (a giving platform with no DAF on Schedule D) pass money on but are left out.
- **Judgement: grants-out ÷ contributions-in is a valid coarse indicator, not a DAF trace.**
  - It is an accrual measure: pledges are booked as contributions when made, and grants when committed.
  - Blue Meridian's 1.69 sits on $2.05–2.40bn of net assets, so it is a draw-down. Without Blue Meridian the core ratio is 0.78.
  - Grants ÷ expenses, which the study also reports, is steadier.
- **Labelling.** "Tax years 2023–2024" means period-end years. For Blue Meridian (FY to September) and Homewise (FY to March), the IRS TaxYr values are 2022–2023.

---

## 3. Accept / modify / reject

| Study | Verdict | What changes |
|---|---|---|
| 1. Grant-count denominators | **Accept** (minor additions) | Add that the pooled rate is mostly Fidelity, plus the without-DAFgiving360 figure (0.0133). Record why the reprint is acceptable. Size the window bias (+4.5% for Fidelity). |
| 2. In-portal data provider | **Modify** | Fix the §0 tallies (20 / 6 / 6). Add the MS GIFT–Ren link. Flag the CCT robots doubt and the Ren robots note. Re-ground the Foundant text on Tech Impact (IPD-015 supports eligibility_only on its own). Add the Giving Compass–Charity Navigator caveat. **Accept** the NPT correction to the direction memo §3 (written). |
| 3. Tax-page audit 11–25 | **Modify** | Reverse the securities-calculator direction: like for like, it understates by 3.5–18% because it omits NIIT. Explain the BofA $2.0M. Date the DonorsTrust guide. Record the law re-read. All other findings **accepted**, including H1–H4 for the tax calculator, the 0.05% footnote and all five law parameters. |
| 4. Pass-through recipients | **Accept** (with caveats) | Add the accrual and Blue Meridian caveat (core 0.78 without Blue Meridian). Add the tax-year labelling note and the CSGF 990-PF note. |
| Industry report | Add §11.68 | One paragraph (182 words), after 46A's §11.67. |

---

## 4. Limits of this validation

- **Not re-read:**
  - JCF pages (Cloudflare challenge, not bypassed);
  - the CCT guide (robots doubt);
  - the Ren blog (a conservative reading of its Anthropic-AI group);
  - DAFgiving360, Raymond James and the other hosts the authors could not read.
- **Pass-through web layer.** Its web columns could not be regenerated (no cached web.json). Two pages were re-checked directly.
- **Like-for-like securities figures.** These are my single-year federal calculations (2026 MFJ schedule, NIIT, floor, §68). Net proceeds are approximated as FMV − gain × (CG rate + 3.8%), and state tax is excluded.
- **Fidelity exposure estimate.** It assumes 2021 equals 2022 and uses the rounded "2.3 million" for 2023.

## 5. Source register (validator fetches, 2026-11-20, UA `research-script/1.0`)

| Source | URL | robots.txt |
|---|---|---|
| Fidelity 2025 Giving Report | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf | 200, path allowed |
| Fidelity calculator, methodology, r1/r3/r4, securities, JS bundle | https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator.html (and paths in register) | 200, allowed |
| Vanguard 2024 annual report | https://www.vanguardcharitable.org/2024annualreport | 200, allowed |
| FY2024 990 XML (Vanguard, GS, RCF, MS GIFT, AOGF, DAFgiving360) and recipient 990s (NVF, Blue Meridian, Climate Imperative, Homewise, CSGF, Bright Funds, OAFF) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml | 404 (no rules) |
| AEF impact map V3.4 | https://www.aefonline.org/wp-content/uploads/2025/10/AEF_DAFImpactMap_V3.4.pdf | 200, allowed |
| MS GIFT impact report; How it Works | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf ; …/ms-gift-how-it-works.pdf | 200; ClaudeBot / anthropic-ai / Claude-Web `Allow: /` |
| NonProfit PRO reprint | https://www.nonprofitpro.com/article/dafgiving360-donors-give-more-than-6-6b-to-charities-in-fiscal-year-2024/ | 200, allowed |
| NPT GivingPoint and due-diligence articles | https://www.nptrust.org/philanthropic-resources/philanthropist/how-npt-givingpoint-can-accelerate-your-online-giving/ | 200, allowed |
| AEF pilot page | https://engage.aefonline.org/?p=12588 | 200, allowed |
| Giving Compass / Ren | https://www.givingcompass.org/giving-compass-and-ren-accelerate-nonprofit-impact-discovery-for-daf-advisors/ | 200, allowed |
| CF guides | https://www.cftampabay.org/portal-guide ; https://cnycf.org/introducing-mygiving ; https://craft-cfscc-prod.s3.amazonaws.com/uploads/2025-CFSCC-Donor-Portal-Guide.pdf | 200 / 200 / 404 |
| NCF support | https://www.ncfgiving.com/support | 200, allowed |
| Tech Impact 2022 | https://techimpact.org/sites/default/files/2024-03/TECH%20IMPACT%20Integrated%20Software%20for%20Community%20Foundations.pdf | 200, allowed |
| CCT donor-portal robots | https://donorportal.cct.org/robots.txt | one-line file; guide not fetched |
| Ren robots | https://www.reninc.com/robots.txt | Anthropic-AI group: Allow /faqs/ only; blog not fetched |
| JCF pages | https://jcfny.org/philanthropic-resources/ ; https://jcfny.org/blog/charitable-giving-in-2025-what-the-new-tax-law-means-for-donors/ | 200; page served Cloudflare challenge |
| BofA Private Bank business-owner page | https://www.privatebank.bankofamerica.com/articles/charitable-giving-unlocked-for-business-owners-under-the-obbba.html | 200, allowed |
| Columbus Foundation | https://columbusfoundation.org/charitable-insights/important-tax-law-changes | 404 (no rules) |
| CJP DAF page | https://www.cjp.org/ways-to-give/donor-advised-funds | 200, allowed |
| DonorsTrust article and guide | https://www.donorstrust.org/a-smarter-way-to-navigate-2025s-final-giving-stretch/ ; https://consider.donorstrust.org/hubfs/DT%20Forms%20and%20Files/Donors%20Guide%20to%20DonorsTrust.pdf | 200, allowed |
| P.L. 119-21 | https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm | 200, allowed |
| 26 USC 170 | https://www.law.cornell.edu/uscode/text/26/170 | 200, allowed |
| Rev. Proc. 2025-32 | https://www.irs.gov/pub/irs-drop/rp-25-32.pdf | 200, allowed |
| NVF, Blue Meridian, Homewise, UCLA Foundation, Bright Funds | https://newventurefund.org/donate ; https://bluemeridian.org/frequently-asked-questions/ ; https://homewise.org/donate/ ; https://www.uclafoundation.org/ ; https://www.brightfunds.org/ | 200 each (no Claude-specific disallow) |
| congress.gov | — | disallows Claude agents; not used |

---

## Exact corrections

### `research/mission-2026-11-14/g1913-02-grant-count-denominators.md`

**Find:** "28 distinct review-venue records give **0.0102 per 10,000 grants per year [0.0068–0.0147]**."
**Replace with:** "28 distinct review-venue records give **0.0102 per 10,000 grants per year [0.0068–0.0147]**. Fidelity supplies 27 of the 28 records and 57.0% of the 4.67 million grants, so the pooled figure is close to Fidelity’s own rate. Without the DAFgiving360 reprint count (1.1 million) it is 0.0133. [V wave 46B]"

**Find:** "They are marked `first_party = no`."
**Replace with:** "They are marked `first_party = no`. The NonProfit PRO page ends “Source: DAFgiving360” and “The preceding press release was provided by a company unaffiliated with NonProfit PRO”. So it carries the sponsor’s own release, and its period (FY to 30 June 2024) matches. It is acceptable as a stated count. The FY2024 990 itself states no count. [V wave 46B]"

**Find:** "That assumption is optimistic for fast growers: Fidelity went from 2.19m grants (CY2022, repo F1) to 3m (CY2025, repo panel S04) (P-G1913-02-06)."
**Replace with:** "That assumption is optimistic for fast growers: Fidelity went from 2.19m grants (CY2022, repo F1) to 3m (CY2025, repo panel S04) (P-G1913-02-06). For Fidelity the bias is small. Summing yearly counts over the window gives about 14.99m grant-years against the 15.67m assumed. The inputs are: 2021 set equal to CY2022’s 2,185,516; about 2.3m for 2023; 2,664,446 for CY2024; 3m for 2025; and the 2025 level for the 323 days of 2026. On that basis the review-venue rate is about 0.0180 rather than 0.0172 (+4.5%). [V wave 46B]"

### `research/mission-2026-11-14/b43n26-01-in-portal-data-provider.md`

**Find:** "- 21 rows, 0 errors."
**Replace with:** "- 20 rows, 0 errors (IPD-014 withdrawn; CSV recount by wave 46B). [V wave 46B]"

**Find:** "- Rows by mode: embedded 7, not_found 7, linked 3, eligibility_only 2, announced 1, vendor_claim 1."
**Replace with:** "- Rows by mode: embedded 6, not_found 7, linked 3, eligibility_only 2, announced 1, vendor_claim 1. [V wave 46B]"

**Find:** "- Rows by evidence scope: sponsor-specific 14, vendor-level 7."
**Replace with:** "- Rows by evidence scope: sponsor-specific 14, vendor-level 6. [V wave 46B]"

**Find:** "We found no CN data inside a sponsor portal."
**Replace with:** "We found no CN data inside a sponsor portal. Giving Compass, the layer announced for Ren, says its tools are “built in collaboration with DAFGiving360, Fidelity Charitable, Vanguard, and Charity Navigator”. CN-linked data could therefore reach a portal through it, though none is shown live. [V wave 46B]"

**Find:** "- **Morgan Stanley.** MS GIFT markets automated vetting with no vendor named."
**Replace with:** "- **Morgan Stanley.** MS GIFT markets automated vetting with no data vendor named. But the same How it Works PDF says “Back office administration provided by Ren, an unaffiliated charitable gift administrator”, and the impact report credits its figures to Renaissance Administration LLC. The vendor-level Ren inference used for AEF (§3.5), and the Giving Compass announcement, would apply to MS GIFT on the same footing [I]. [V wave 46B]"

**Find:** "| donorportal.cct.org | 200 | allowed | 2 | 1 | 404"
**Replace with:** "| donorportal.cct.org | 200 | allowed on a literal parse only | 2 | 1 | 404. The file is a single line, `User-agent: * Allow: /index.html Disallow: /`. Parsers read that as no rules, but it evidently means to disallow everything except /index.html. IPD-013’s quote is robots-doubtful and should be relabelled [C] [V wave 46B]"

**Find:** "| www.reninc.com | 200 | allowed | 2 | 1 | 404"
**Replace with:** "| www.reninc.com | 200 | allowed | 2 | 1 | 404. Its robots.txt has an `Anthropic-AI` group that allows only /faqs/ and disallows nothing. Read literally, the blog is allowed; wave 46B did not re-fetch it [V wave 46B]"

**Find:** "- **Foundant.** CommunitySuite (700+ community foundation clients per its own page) markets Candid as a built-in integration for the donor portal."
**Replace with:** "- **Foundant.** With the foundant.com sources withdrawn, the vendor-level evidence is Tech Impact (July 2022): “Their integration with Candid provides access to Guidestar Charity Check and Guidestar for Grant Applications.” Charity Check is a status product and GuideStar for Grant Applications serves applicants. On its own, this supports eligibility_only, as for akoyaGO (IPD-020). The Candid search in Foundant donor portals rests on the CF guides (IPD-016, IPD-017). [V wave 46B]"

**Find:** "| Foundant (IPD-015; IPD-014 withdrawn) | Candid | embedded (vendor)"
**Replace with:** "| Foundant (IPD-015; IPD-014 withdrawn) | Candid | embedded (vendor). The quote alone supports only eligibility_only; the embedded reading rests on IPD-016 and IPD-017 [V wave 46B]"

### `research/mission-2026-11-14/direction-charity-ratings-integrations.md`

**Find:** "| NPT | ND (own due-diligence articles name no vendor) | ND | ND"
**Replace with:** "| NPT | **Embedded**, per NPT’s own GivingPoint article: “Partnering with GuideStar’s powerful search database, donors can search …” (published 2021-07-29, modified 2026-02-09; current portal not observed). Also linked in a 2024 due-diligence article | Linked (same 2024 article: “Candid’s Guidestar , Charity Navigator , or Better Business Bureau’s Wise Giving Alliance”) | BBB Wise Giving Alliance linked. See [b43n26-01-in-portal-data-provider.md](b43n26-01-in-portal-data-provider.md) [V wave 46B]"

### `research/mission-2026-11-14/b4142-04-tax-page-audit-11-25.md`

**Find:** "- **Direction of the errors.** H3 and H4 are overstated because the calculator has no floor and no cap; omitting the 3.8% NIIT works in the opposite direction."
**Replace with:** "- **Direction of the errors (corrected by wave 46B).** This comparison is not like for like. In the calculator’s sell case the donor gives the proceeds net of capital-gains tax (FMV − c), so its extra saving is c plus the deduction lost on c. The repo’s sell-then-give row gives the full FMV, which keeps the deduction nearly unchanged. On the calculator’s own counterfactual, 2026 law (floor, 2/37 and the 3.8% NIIT) gives about $5,448 (H2), $38,766 (H3) and $227,178 (H4). So the calculator understates by about 18%, 15% and 3.5%, mainly because it omits NIIT. The missing floor and cap move these figures only slightly. [V wave 46B]"

**Find:** "– **H4:** $219,200 against $191,157 (+14.7%)."
**Replace with:** "– **H4:** $219,200 against $191,157 (+14.7%).<br>– These gaps come from a different counterfactual, not from the missing 2026 rules. Like for like, the calculator understates H2–H4 (§3.2). [V wave 46B]"

**Find:** "The stated levels equal gross 20% gains tax plus $0.2M."
**Replace with:** "The stated levels equal gross 20% gains tax plus $0.2M. The ‘about $2.0M’ saving is 20% of the $10M of gain avoided, which holds only if both cases get the same deduction. On the stated inputs they do not. The business interest given in kind is capital-gain property, deductible up to 30% of the $20M AGI ($6M in year 1). The $10M cash gift after the sale fits within 60% of $30M. [V wave 46B]"

**Find:** "These were not re-read this pass"
**Replace with:** "These were not re-read this pass by the author. Wave 46B re-read P.L. 119-21 §§70111 and 70424–70426 (govinfo), 26 USC 170(p) and 170(b)(1)(I) (LII) and Rev. Proc. 2025-32 §4.14. They confirm five parameters: the 0.5% floor; the 2/37 reduction of the lesser of itemized deductions or taxable income above the start of the 37% bracket; the $1,000/$2,000 non-itemizer deduction, with the DAF exclusion and no floor; the corporate band above 1% and up to 10% of taxable income; and the $32,200 MFJ standard deduction [V wave 46B]"

**Find:** "Guide revised June 2025"
**Replace with:** "Guide revised June 2025, before P.L. 119-21 was enacted on 4 July 2025, so it was right when issued. The 60% limit it states still applies [V wave 46B]"

### `research/mission-2026-11-14/b39n6-03-pass-through-recipients.md`

**Find:** "The ratio says the organisation as a whole passes money on."
**Replace with:** "The ratio says the organisation as a whole passes money on. It is also an accrual measure. Unconditional pledges are booked as contributions when made, and grants when committed, so multi-year pledges distort two-year ratios. Blue Meridian carried $2.05–2.40bn of net assets over these years (composition not read). Its 1.69 is therefore a draw-down of money booked earlier, not same-period pass-through. Without Blue Meridian the core-10 ratio is 0.78. [V wave 46B]"

**Find:** "- **2021+ only:** all filings are tax years 2023–2024; all pages were read 2026-11-20."
**Replace with:** "- **2021+ only:** all filings are tax years 2023–2024; all pages were read 2026-11-20. Here ‘tax year’ means the year in which the return period ends. For fiscal-year filers the IRS TaxYr is one earlier. Blue Meridian’s returns (years to 30 September 2023 and 2024) and Homewise’s (years to 31 March 2023 and 2024) are TaxYr 2022 and 2023. Charter School Growth Fund (Charter Fund Inc) filed a 990-PF for 2023 and a 990 for 2024, so its 2023 inflow is 990-PF Part I line 1. [V wave 46B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.68 Grant-count rates; in-portal data; tax pages 11–25; pass-throughs (validated, wave 46B)\n\n**Grant-count rates, in-portal data, tax pages 11–25, pass-through recipients** (validated, wave 46B). The grant-count and pass-through studies re-run exactly, and the sampled primary counts and 990 values match. Fidelity’s 27 review-venue complaints give 0.0172 per 10,000 grants a year, and Fidelity supplies 27 of the 28 records behind the pooled 0.0102. Allowing for yearly grant growth would raise its rate by only about 4.5%. NPT’s own GivingPoint article names GuideStar as its search database, so the ‘ND’ for NPT in the integrations matrix is corrected. MS GIFT’s own PDF names Ren as its back-office administrator. The Fidelity tax calculator overstates 2026 savings by 7.0% to 69.3%, as reported. The securities calculator’s apparent overstatement is a comparator artefact. On its own counterfactual (sell, then give the net proceeds), 2026 law gives more, because the calculator omits the 3.8% NIIT. All five 2026 parameters in the repo engine match P.L. 119-21 and Rev. Proc. 2025-32. Pass-through onward ratios are accrual measures. Blue Meridian’s 1.69 draws on about $2bn of net assets, and without it the core-10 ratio is 0.78 (repo [`validation-wave46b-report.md`](mission-2026-11-14/validation-wave46b-report.md)) [V wave 46B]\n\n---\n\n## Source register"
