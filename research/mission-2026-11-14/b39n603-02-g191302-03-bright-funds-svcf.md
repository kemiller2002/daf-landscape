# P-B39N603-02 and P-G1913-02-03: Bright Funds classification and SVCF grant-dollar reconciliation

**Date:** 2026-11-20 · **Task:** b39n603-02-g191302-03 · **Queue items:** P-B39N603-02, P-G1913-02-03

**Outputs**
- [`data/mission-2026-11-14/bright-funds-svcf-2026-11-20.csv`](../../data/mission-2026-11-14/bright-funds-svcf-2026-11-20.csv): 92 rows in long format, one metric per row (§6).
- [`scripts/mission_bright_funds_svcf.py`](../../scripts/mission_bright_funds_svcf.py): stdlib, functional style. `fetch` checks robots.txt and downloads seven 990 XML returns; `report` is pure: it parses them, reads repo CSVs, writes the CSV and prints a JSON summary. Two `report` runs gave byte-identical CSVs (md5 `11cdafee…`).
- [`data/mission-2026-11-14/queue-proposals-b39n603-02-g191302-03.csv`](../../data/mission-2026-11-14/queue-proposals-b39n603-02-g191302-03.csv): P-B39N60302-01..06.

**Labels:** **[F]** filed 990 value; **[Q]** quoted from audited statements or a release (URL given); **[C]** computed by the script; **[I]** judgement.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| **Bright Funds: DAF sponsor or processor?** | **A donation processor for workplace giving. It is not a DAF sponsor, and it does not belong on the DAF-to-DAF whitelist** [I].<br>Evidence:<br>- Part IV line 6 is "No" in both CY2023 and CY2024 [F].<br>- Schedule D is filed, but Part I is blank [F].<br>- Part III describes "a platform … to encourage and facilitate online giving … to the charity of their choice" [F].<br>- Schedule I has no Part II lines [F].<br>- It grants 91.8% of contributions onward [C].<br>- Schedule D Part X lists a liability called "payments received from BFI clients" [F].<br>- The site redirects to "Bright Funds is now Submittable! … corporate grants, employee giving, and employee volunteering software" [W]. |
| **Effect on repo figures** | - **Market totals (DAF grants, netting): $0.** It files no DAF grants, so nothing is double counted.<br>- Adding it to the whitelist would be wrong. It would remove up to $72.48m in the upper tier and $0 in the central tier, because its DAF share of assets is 0 [C].<br>- **Recipient frames:** $72,482,124 filed / $72,473,956 DAF-weighted, all FY2023–24, is counted as a final charity grant. That is **0.093% of $78.29bn** filed and **0.098% of $74.28bn** DAF-weighted [C].<br>- Retagging it as a processor conduit moves:<br>  - the 28-EIN pass-through share from 4.14% to **4.04%** filed (4.29% to 4.20% DAF-weighted);<br>  - the rule-based 18-EIN set from 2.97% to **2.87%** DAF-weighted (2.87% to 2.78% filed) [C] [V wave 48A];<br>  - the pooled DAF share of recipient revenue by under 0.01 point (§2.4). |
| **SVCF: why $3.06bn vs $1.54bn?** | **The release excludes transfers to other DAF sponsors, and in 2024 those were $1.67bn.**<br>- The release says: "Grantmaking figures exclude any distributions made from SVCF into donor advised funds at other institutions" [Q].<br>- The audit says $1,667,000,000 of 2024 grants expense "were transferred to other donor-advised fund sponsors" [Q].<br>- One CY2024 Schedule I line, $1,591,322,838 to National Philanthropic Trust, is 95.5% of that amount [F, C].<br>- Audited grants awarded, $3,187.08m, less $1,667m gives **$1,520.08m**. The preliminary release says $1.54bn, a residual of **+$19.92m (1.3%)** [C]. |
| **Other candidate explanations** | - **Fiscal year vs calendar year:** not a cause. SVCF files on a calendar year, and DAFRC's "FY2024" is the return for the year ending 2024-12-31 [F].<br>- **Scope (DAF vs all funds):** works against the gap. The release covers all funds, so it should exceed DAF-only dollars, not fall short of them [I].<br>- **CZ Biohub LLCs:** not a cause. Their $1,656.6m filed (the repo's $1,594.0m is DAF-weighted) is all CY2023. CY2024 has $0 to them [F].<br>- **Grants to other DAF sponsors or affiliates:** this is the cause (row above). |
| **Implied average grant (g1913-02 §4.3)** | - $3,064.39m ÷ 14,500 = $211,337 compares DAF dollars that include the NPT transfer with a count that excludes it.<br>- On an audited basis net of DAF transfers it is **$104,833**; on the release basis it is $106,207 [C].<br>- P-B39N60302-03 proposes changing that cell. |

---

## 1. Method

1. **robots.txt first** for every host (§5.2). The user agent was `research-script/1.0`, 1–2 s between requests. Groups named for Claude/Anthropic agents were honoured where present. sec.gov, crt.sh and certspotter were not used. There was no login, form or outreach.
2. **Form 990 e-file XML** from the GivingTuesday mirror of IRS TEOS (`gt990datalake-rawdata.s3.amazonaws.com`; its robots.txt returns 404, so no rules apply). Object ids:
   - Bright Funds Foundation (46-2109112):
     - CY2023: 202433209349327603;
     - CY2024: 202543219349326714;
     - CY2024 amended: 202503459349301950. Its figures are identical to the original [C].
   - SVCF (20-5205488): CY2023 202413129349304911; CY2024 202543149349305759.
   - Vanguard Charitable (23-2888152): FY to 2023-06-30 202441359349309439; FY to 2024-06-30 202511349349313096. These were read for the lines to Bright Funds.
3. **Fields parsed by the script:**
   - Part IV line 6;
   - Schedule D Part I lines 1–4;
   - Part IX lines 1–3 and total expenses;
   - Part I line 13;
   - Part VIII 1h;
   - net assets;
   - Schedule I Part II lines (count, $ and recipient EIN);
   - the list of schedules filed.
4. **Read by hand:** Schedule O and Part III text for both filers, and Schedule D Parts X and XIII and Schedule R for Bright Funds.
5. **SVCF audited consolidated statements** (Crowe LLP, years to 31 December) for 2023 and 2024, and the SVCF release of 2025-03-24. Both were read as PDF or HTML and the figures are quoted, not parsed (constants in the script, with URLs).
6. **Repo inputs used unchanged:**
   - `pass-through-recipients-2026-11-20.csv` (Bright Funds dollars);
   - `daf-to-daf-recipient-whitelist.csv`;
   - `net-payout-by-sponsor.csv` (SVCF transfer tiers A/B/C);
   - the b39n6-03 denominators: $78,287,627,404 filed and $74,281,457,270 DAF-weighted.

---

## 2. Task 1: Bright Funds Foundation (P-B39N603-02)

### 2.1 Filings

| Item | CY2023 | CY2024 |
|---|---:|---:|
| Part IV line 6 (DAF indicator) [F] | No | No |
| Schedule D Part I (DAF counts and values) [F] | blank | blank |
| Schedules filed [F] | A, D, F, I, O, R | A, D, F, I, O, R (amended adds B) |
| Part VIII 1h contributions [F] | $85,621,078 | $25,501,636 |
| Part IX line 1, domestic organisations [F] | $64,122,540 | $14,358,691 |
| Part IX line 3, foreign [F] | $16,571,122 | $6,942,607 |
| Total functional expenses [F] | $83,907,973 | $22,261,639 |
| Schedule I Part II lines [F] | 0 | 0 |
| Net assets EOY [F] | $14,630,654 | $5,809,370 |
| Grants out ÷ contributions, pooled [C] | 0.918 | |

**Text in the filings** [F]:
- *Part III:* "The foundation provides a platform for supporting charitable programs, charitable initiatives, and charitable organizations … it will encourage and facilitate online giving opportunities to and for all 501(c)(3) charitable organizations … by providing the public with straightforward and secure ways to donate to, or volunteer for, the charity of their choice, and track their giving through state of the art internet-based tools."
- *Schedule O:* governance boilerplate only (Part VI 11b and 19). There is no mention of donor-advised funds, variance power or advisory privileges.
- *Schedule D Part X:* other liabilities include "Payments received from BFI clients" ($0 CY2023; $12,170 CY2024).
- *Schedule R:* Wizehive Inc (EIN 45-4503414, Submittable) is a related taxable C corporation that performs services for the foundation (code M; $4,043,819 in CY2023).
- *Schedule I:* only "grant records maintained = Yes", with no Part II lines. It is therefore not possible to see where the money goes.

**Inflow from top-50 sponsors** [F]: Vanguard Charitable gave $24,558,662 (FY2023) and $47,880,713 (FY2024), both with purpose "FOR RECIPIENT'S EXEMPT PURPOSE". Those two lines are 99.9% of the $72.48m top-50 inflow.

### 2.2 Public pages
- `www.brightfunds.org`: robots allows everything except `/explore/find`. It redirects to `hello.brightfunds.org`, whose robots.txt has only a sitemap line.
- The homepage [W] reads: "Bright Funds | Workplace Giving and Volunteering Software. Bright Funds is now Submittable! Together, we're offering the most comprehensive and innovative corporate grants, employee giving, and employee volunteering software." It links "Nonprofit? Click here to Register a Nonprofit".
- The sitemap lists only the homepage.
- `/faq` and `/terms` redirect to `www.submittable.com/support/` and `/terms-and-conditions/`. Submittable's robots.txt explicitly allows ClaudeBot and anthropic-ai. However, every Submittable content page returned **403 with a Cloudflare "Just a moment…" challenge**, so it was **not read and not worked around**. That applies to `/for-nonprofits/`, `/solutions/corporate-giving-platform/`, `/terms-and-conditions/` and three blog posts.
- `submittable.help` (robots allows) has no Bright Funds article in its sitemap.

### 2.3 Classification [I]
- **Not a DAF sponsor.** The filer answers "No" to Part IV line 6 in both years and leaves Schedule D Part I blank. Nothing in Part III, Schedule O or the homepage mentions donor-advised accounts. It describes itself as a giving platform that routes donations "to the charity of their choice".
- **Donation processor.** It is a workplace-giving conduit run on a for-profit vendor's software (Bright Funds Inc, now Submittable/WizeHive), and it grants out about 92% of what comes in. That is the same functional role as the repo's processors (AOGF/Benevity, PayPal Charitable Giving Fund, Blackbaud Giving Fund, Network for Good).
  - The difference: those processors file Schedule D Part I and appear in the DAFRC panel as "Donation Processor". Bright Funds does neither, and its EIN is not in any DAFRC or Schedule D harvest file.
  - Proposed tag: `processor_non_daf`.
- **Not on the DAF-to-DAF whitelist.** The whitelist covers DAFRC panel sponsors (W1–W4) and is meant to stop DAF grants being counted twice in market totals. Bright Funds reports no DAF grants, so there is nothing to double count. It is also not in the whitelist CSV [C]. Even if it were added under W2 it would fail the DAF-share-of-assets test (filed share 0 < 0.5).
- **What stays unknown:** whether the Vanguard money is a corporate or employee programme run from Vanguard Charitable accounts through the Bright Funds platform. The 990s do not say, and the Submittable pages that might say were blocked (P-B39N60302-01).

### 2.4 Effect on repo figures [C]

| Repo figure | Current | If Bright Funds is retagged as a processor conduit |
|---|---|---|
| DAF market totals and DAF-to-DAF netting | Bright Funds not netted | **No change.** Whitelisting it would wrongly remove up to $72,482,124 in the upper tier ($0 in the central tier). |
| Top-50 recipient frame, net of DAF-to-DAF (sectors, lobbying, geography) | $72,482,124 filed / $72,473,956 DAF-weighted counted as final charity grants (T12, public/societal benefit) | 0.093% / 0.098% of the frame moves to a "processor, final recipient unknown" bucket. |
| Pass-through population, 28 EINs (b39n6-03) | 4.14% filed / 4.29% DAF-weighted | 4.04% / 4.20% |
| Rule-based pass-through set, 18 EINs | 2.97% DAF-weighted | 2.87% |
| DAF share of recipient revenue, pooled all (published 6.89%) | Bright Funds is a certainty-stratum respondent (weight 1; share 0.652) | Under 0.01 point lower. My reconstruction of the weighting gives 7.203% to 7.195% and does not reproduce the published 6.89%, so treat this as an order of magnitude. Within public/societal benefit the reconstruction falls by about 0.17 point. |
| Non-Q foreign spending | $19.79m abroad attributed to Bright Funds | Unchanged in dollars; it is a pass-through abroad (Part IX line 3 $23.51m over 2 years). |

---

## 3. Task 2: SVCF grant dollars (P-G1913-02-03)

### 3.1 Filed figures (Form 990, calendar years) [F]

| Line | CY2023 | CY2024 |
|---|---:|---:|
| Schedule D Part I line 1, DAFs held | 1,031 | 1,011 |
| Line 2, DAF contributions | $1,112,533,200 | $2,835,073,665 |
| **Line 3, DAF grants (the DAFRC/R1 value)** | $4,889,252,836 | **$3,064,391,940** |
| Line 3, other funds' grants | $154,741,471 | $213,599,111 |
| Line 4, DAF EOY value | $7,476,276,516 | $9,578,124,315 |
| Part IX line 1, domestic organisations | $4,886,115,481 | $3,162,318,046 |
| Part IX line 2, individuals | $2,745,000 | $4,122,298 |
| Part IX line 3, foreign | $192,386,629 | $160,055,648 |
| **Part I line 13, total grants** | $5,081,247,110 | **$3,326,495,992** |
| Schedule I Part II, $ (lines) | $4,882,562,863 (3,316) | $3,158,249,119 (3,576) |

### 3.2 Audited and release figures [Q]

| Item | 2023 | 2024 | Source |
|---|---:|---:|---|
| Grants awarded (consolidated) | $4,655,917k | $3,187,080k | Audit 2024, statement of activities |
| Of which transferred to other DAF sponsors | $207,000,000 | **$1,667,000,000** | Audit 2024, Note 2 |
| Contributions transferred from other DAF providers | $325,000,000 | $500,000,000 | Audit 2024, Note 2 |
| Donor-advised funds granted (approximately) | $4,657,000,000 | $3,077,000,000 | Audit 2024, Note 1 |
| Corporate-advised funds granted (approximately) | $134,000,000 | $189,000,000 | Audit 2024, Note 1 |
| Grants payable, net, EOY | $2,067,074,776 | $1,753,467,922 | Audit 2024, Note 8 |
| Release: total grants (preliminary) | — | $1,540,000,000 ("over 14,500 grants", "more than 6,000 organizations") | Release 2025-03-24 |
| Release geography | — | Bay Area $327m; rest of California $175m; US outside California $874m. That leaves **$164m** implied for outside the US [C], close to Part IX line 3 ($160.1m) | Release |

The release says verbatim: "All figures are preliminary and unaudited. Grantmaking figures exclude any distributions made from SVCF into donor advised funds at other institutions."

### 3.3 Reconciliation, CY2024 [C]

| Step | $m |
|---|---:|
| DAFRC/R1 FY2024 DAF grants (Schedule D line 3) | 3,064.39 |
| + other funds' grants (line 3, column b) | 213.60 |
| = Schedule D grants, all funds | 3,277.99 |
| Part IX lines 1–3 (Part I line 13) | 3,326.50 |
| Audited grants awarded (consolidated) | 3,187.08 |
| − audited transfers to other DAF sponsors | −1,667.00 |
| **= audited grants net of DAF transfers** | **1,520.08** |
| Release (preliminary) | 1,540.00 |
| Release − audited net (unexplained; preliminary vs final) | +19.92 |

**Cross-checks** [C]:
- The single Schedule I line to NPT is $1,591.32m, which is 95.5% of the audited $1,667m.
- The repo's tier A (Schedule I lines to national DAF sponsors, `net-payout-by-sponsor.csv`) is $1,693.52m, $26.52m above the audited figure. Tier B, which adds processors, is $1,758.40m. Tier C, all DAF-sponsor recipients, is $1,854.22m.
- On the 990 basis, Part IX less tier A is $1,632.98m and less tier C is $1,472.27m. The release figure lies between them.
- On a DAF-only basis, Schedule D line 3 less tier A is **$1,370.87m**. This is the closest DAF-only analogue to the release, but the release covers all funds.

**Conclusion** [I]:
- The $1.52bn gap between $3.06bn and $1.54bn is mostly one transfer: SVCF donors moving $1.59bn to NPT in 2024.
- Schedule D line 3 counts that transfer as a DAF grant. That is correct for a gross sponsor figure, and the repo's DAF-to-DAF netting already removes the NPT line (`daf-to-daf-flows-top50.csv`, FY2024, $1,591,322,838).
- SVCF's release leaves the transfer out by design.
- The remaining differences are small and of known kinds:
  - all-fund versus DAF-only scope;
  - gross 990 versus net audited grants;
  - preliminary versus final.

### 3.4 The 990 vs the audit
- Part IX lines 1–3 exceed audited grants awarded by **$139.42m** in CY2024 and by **$425.33m** in CY2023 [C].
- Possible causes:
  - the 990 covers the SVCF entity, while the audit is consolidated with supporting organisations;
  - Part XI line 9 lists "Grant Cancellations not offset", but the public XML masks the amount;
  - a present-value adjustment for grants (CY2024: $2,854,176);
  - refunds booked against grant expense in the audit.
- Schedule D Parts XII–XIII are blank because the audit is consolidated, so the 990 does not reconcile itself. Not decomposed here (P-B39N60302-04).

### 3.5 CY2023 and the Biohub grants
- CY2023 Schedule I has two very large recipient groups [F]:
  - four Chan Zuckerberg LLCs (CZ Biohub SF, CZ Biohub New York, CZ Biohub Chicago and CZ Institute for Advanced Biological Imaging), **$1,656,553,619** [V wave 48A] (586.0 + 576.0 + 248.0 + 246.5 $m);
  - **Further Future Foundation** (92-1117448), **$1,309,000,000** (purpose "Sciences").
- Together these are 58% of CY2023 grants.
- The 2023 annual-report page matches: "Health $1.6 Billion; Sciences $1.4 Billion" [W].
- The repo's $1,594.0m for the Biohub LLCs is the DAF-weighted value (×0.962) of the same lines.
- None of this falls in CY2024. CY2024 has **$0** of Biohub lines [F]. The Biohub grants therefore explain why CY2023 DAF grants ($4.89bn) exceed CY2024's, but not the CY2024 release gap.
- CY2023 audited grants net of DAF transfers are $4,448.92m [C]. No CY2023 SVCF release of total grants was found in the svcf.org sitemaps.
- Further Future Foundation's status was not checked here (P-B39N60302-05). Later waves resolved it: the same EIN (92-1117448) renamed itself Navigation Charitable Fund on 2023-11-01; its FY2023 990 is filed as “Navigation Charitable Fund (fka Further Future Foundation)”; BMF ruling 2023-03, NTEE U05, foundation code 15. [V wave 51B]

### 3.6 Consequence for g1913-02 §4.3
- The implied average grant of $211,337 should be read as an artefact.
- Use **$106,207** (release: dollars and count from the same preliminary document, same scope). $104,833 (audited net of DAF transfers, divided by the release count) is a cross-check; 14,500 is a floor, so both are upper bounds [V wave 48A]
- The per-$ complaint denominator for SVCF should likewise be about $1.52bn, not $3.06bn, if it is meant to measure grants that reach charities (P-B39N60302-03).

---

## 4. Limits
- **Bright Funds' final recipients are invisible.** It files no Schedule I lines, so it cannot be shown where the Vanguard money went.
- **Bright Funds' product terms were blocked.** The Submittable support and terms pages behind a Cloudflare challenge would say whether employee or employer accounts carry advisory privileges. "Not a DAF sponsor" rests on the filer's own Part IV and Schedule D answers.
- **The recipient-revenue effect is approximate.** I could not reproduce the published weighting (my reconstruction gives 7.20% against 6.89%). The direction and size (under 0.01 point) are robust because Bright Funds has weight 1.
- **The SVCF release is preliminary.** The +$19.9m residual is not explained.
- **The audit's $1,667m is rounded and not itemised.** The NPT line covers 95.5% of it. The other ~$76m was not matched line by line. The repo's tier A is $26.5m higher, perhaps from recipients the audit does not count as "DAF sponsors" or from timing.
- **Audit figures were read from PDF by hand** (pdftotext) and are quoted, not parsed by the script.
- **2021+ only:** all filings are 2023–2024 tax years; pages were read 2026-11-20.

---

## 5. Source register

### 5.1 Sources

| ID | Source | URL |
|---|---|---|
| S1 | Bright Funds Form 990, CY2023 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349327603_public.xml |
| S2 | Bright Funds Form 990, CY2024 (original; amended identical) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349326714_public.xml ; …/202503459349301950_public.xml |
| S3 | SVCF Form 990, CY2023 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413129349304911_public.xml |
| S4 | SVCF Form 990, CY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml |
| S5 | Vanguard Charitable Form 990, FY2023 and FY2024 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441359349309439_public.xml ; …/202511349349313096_public.xml |
| S6 | SVCF audited consolidated financial statements 2024 (with 2023 comparatives) | https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2024.pdf |
| S7 | SVCF audited consolidated financial statements 2023 | https://www.svcf.org/assets/img/heroA/svcf-financial-statement-audit-2023.pdf |
| S8 | SVCF release, 2025-03-24, "Thanks to our donors, SVCF granted $1.54 billion to nonprofits in 2024" | https://www.svcf.org/about/news-media/blog/silicon-valley-community-foundation-granted-1.54-billion-to-nonprofits-in-2024 |
| S9 | SVCF 2023 and 2024 "By the Numbers" | https://www.svcf.org/annual-reports/2023/by-the-numbers ; https://www.svcf.org/annual-reports/2024/by-the-numbers |
| S10 | SVCF consolidated statements of financial position, web summaries | https://www.svcf.org/annual-reports/consolidated-statements-of-financial-position-2024 |
| S11 | Bright Funds homepage | https://hello.brightfunds.org/ (from https://www.brightfunds.org/) |

### 5.2 robots.txt log (2026-11-20, UA `research-script/1.0`)

| Host | robots.txt | Decision |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 | No rules; 7 XML files fetched |
| www.brightfunds.org | 200; `*` disallows /explore/find; no Claude groups | Homepage fetched (redirects to hello.); /faq and /terms redirect to submittable.com |
| brightfunds.org | 301 → www | — |
| hello.brightfunds.org | 200; sitemap line only | Homepage and sitemap fetched |
| www.submittable.com | 200; explicitly `Allow: /` for ClaudeBot and anthropic-ai | Content pages returned **403** (Cloudflare challenge). **Blocked**; not retried, UA not changed. Only the sitemap was read |
| submittable.help | 200; disallows /not-authorized, /not-found; crawl-delay 1 | Sitemap read; no relevant article |
| help.submittable.com | 404 (host page not found) | Not used |
| www.siliconvalleycf.org, siliconvalleycf.org | 301 → www.svcf.org | — |
| www.svcf.org | 200; `*` disallows /cpresources/, /vendor/, /.env, /cache/; no Claude groups | Release, sitemaps, annual-report pages and the two audit PDFs fetched |
| projects.propublica.org | 200; disallows /nonprofits/display_990*, download-xml* and others | Not used |

---

## 6. Data dictionary: `bright-funds-svcf-2026-11-20.csv`

| Column | Meaning |
|---|---|
| task | Queue item: P-B39N603-02 (Bright Funds) or P-G1913-02-03 (SVCF) |
| entity | Filer, or flow (e.g. "Vanguard Charitable -> Bright Funds") |
| ein | EIN without hyphen |
| period | Tax or calendar year (2023, CY2024), sponsor fiscal year (FY2024 = year to 30 June 2024 for Vanguard), a span (FY2023-24), or `-` |
| metric | Metric name, e.g.:<br>- Schedule D: `sched_d_l3_daf_grants`;<br>- Part IX: `part_ix_l1_domestic_org_grants`;<br>- quoted audit figures: `audited_*`;<br>- quoted release figures: `release_*`;<br>- repo values: `repo_transfers_tier_*`;<br>- derived reconciliation figures: `*_minus_*`, `avg_grant_*`, `share_*`. |
| value | USD unless the metric is a count (`*_count`, `*_lines`, `release_grant_count_floor`), a share or ratio (values under 10, 6 decimals), or text (indicators, schedules, classes) |
| basis | F filed 990; Q quoted (audit or release); C computed; C (repo) read from a repo CSV; I judgement |
| source | URL of the filing or document, or the repo file path |
| note | Line reference, quotation or caveat |

---

## 7. Reproduction

```
python3 scripts/mission_bright_funds_svcf.py fetch  . --cache <scratch>/xml
python3 scripts/mission_bright_funds_svcf.py report . --cache <scratch>/xml
```
