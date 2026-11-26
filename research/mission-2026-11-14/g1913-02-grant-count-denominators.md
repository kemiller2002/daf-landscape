# Grant-count denominators for DAF complaint rates: top-15 sponsors and five processors

**Queue item:** P-G1913-02 | **Research date:** 2026-11-20 | **Builds on:** [gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md) §4 (numerators, per-account and per-$ rates; not modified)

**Files written**
- [`data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv`](../../data/mission-2026-11-14/grant-count-denominators-2026-11-20.csv): 43 rows. There are 23 source rows (stated counts, derived counts, recipient lower bounds, not-found records) and 20 Schedule I rows (one per entity). The data dictionary is in §7.1.
- [`scripts/mission_grant_count_rates.py`](../../scripts/mission_grant_count_rates.py): stdlib only, functional style. It reads the P-GAP19-13 rates CSV for the numerators and reuses that task's exact Poisson interval. It refuses to overwrite its output unless given `--force`.
- [`data/mission-2026-11-14/complaint-rates-per-grant-2026-11-20.csv`](../../data/mission-2026-11-14/complaint-rates-per-grant-2026-11-20.csv): 66 rows (20 entities × 3 scopes, plus 6 pooled rows). This is the script's output. The data dictionary is in §7.2.
- [`data/mission-2026-11-14/queue-proposals-g1913-02.csv`](../../data/mission-2026-11-14/queue-proposals-g1913-02.csv): 6 rows, P-G1913-02-01 to -06.

**Reproduction:** `python3 -B scripts/mission_grant_count_rates.py . --force`. The `-B` flag stops the import of `mission_complaint_rates_gap19.py` from writing bytecode.

---

## 1. Summary

1. **12 of the 15 largest sponsors have a usable FY2024 or CY2024 grant count (11 stated, 1 derived). None of the five processors states one.**
   - Stated counts: Fidelity Charitable 2,664,446 (CY2024); DAFgiving360 more than 1.1 million (FY2024); Vanguard Charitable 221,825 (FY2024); Renaissance Charitable Foundation more than 160,000; NPT 129,575 (FY2024); Morgan Stanley GIFT 122,000; Jewish Communal Fund 89,485 (FY2024); GS Philanthropy Fund about 29,254; Foundation For The Carolinas 16,531; SVCF more than 14,500 (preliminary); ImpactAssets 13,500+.
   - Derived: American Endowment Foundation 109,708. This is the sum of the 51 state rows (50 states plus DC) in AEF's own 2024 impact map, and covers US grants only.
   - Not found: BofA Charitable Gift Fund, The Chicago Community Trust and National Christian Foundation. NCF gives only a recipient count (36,000+), which is used as a lower bound.
   - Processors: only lower bounds. These are recipient counts (Blackbaud Giving Fund 123,000+; For Good 22,000+) or Schedule I recipient lines (AOGF 40,985; PPGF 14,871). Dechomai Asset Trust has no meaningful count.
2. **Fidelity Charitable, per grant:** 27 review-venue complaints over 5.88 years give **0.0172 per 10,000 grants per year [95% CI 0.0114–0.0251]**, or 0.101 per 10,000 grants over the whole window [0.067–0.147]. On all venues (50 records) the figure is 0.0319 [0.0237–0.0421] per 10,000 grants per year.
3. **Pooled top-15 sponsors with a count (12 sponsors, 4.67 million grants):** 28 distinct review-venue records give **0.0102 per 10,000 grants per year [0.0068–0.0147]**. Fidelity supplies 27 of the 28 records and 57.0% of the 4.67 million grants, so the pooled figure is close to Fidelity’s own rate. Without the DAFgiving360 reprint count (1.1 million) it is 0.0133. [V wave 46B] On all venues, 68 distinct records give 0.0248 [0.0192–0.0314].
4. **AOGF (Benevity) has only an upper bound per grant: at most 2.32 per 10,000 grants per year [1.76–3.02] on review venues, and at most 1.95 [1.43–2.59] on the strict scope.**
   - The denominator is 40,985 Schedule I recipient lines, which is a lower bound on grants.
   - For AOGF to have the same per-grant rate as Fidelity, it would need about **5.5 million grants a year** (4.6 million on the strict scope). Its filed account count is 720,545.
   - So the per-grant ranking cannot yet be settled. The per-$ ranking (AOGF about 13 times worse) and the per-account ranking (Fidelity worse) from P-GAP19-13 still bracket it.
5. **Per grant, the sponsors with forum, press and regulator complaints separate a little.** On all venues per grant per year:
   - Vanguard Charitable 0.115 [0.064–0.190];
   - Fidelity 0.032 [0.024–0.042];
   - DAFgiving360 0.023 [0.013–0.038].
   Vanguard's 15 records come entirely from non-review venues. That makes this a venue-selection signal more than a service signal.
6. **The per-grant zero bounds are tight for large sponsors and loose for small ones.** The 95% upper bounds per 10,000 grants per year on review venues are:
   - DAFgiving360 0.0057, Vanguard 0.028, NPT 0.048, Morgan Stanley GIFT 0.051, AEF 0.057, JCF 0.070;
   - ImpactAssets 0.46, SVCF 0.43, FFTC 0.38.
   As in P-GAP19-13, these bounds hold only if complainants used the venues checked, and most sponsors have no venue presence.
7. **Dollar and count denominators disagree for SVCF.** DAFRC/R1 FY2024 DAF grants ($3.06bn) divided by SVCF's 14,500 grants implies an average grant of $211,337. SVCF's own $1.54bn implies $106,207. Resolved (b39n603-02-g191302-03): the release excludes distributions into DAFs at other institutions, and the 2024 audit counts $1,667m of grants expense as transfers to other DAF sponsors, $1,591.3m of it one Schedule I line to NPT. Use $106,207 (release dollars and count from the same document); audited grants net of those transfers ($1,520.08m) give $104,833. $211,337 is an artefact [V wave 48A]

---

## 2. Method

### 2.1 Entity frame

The frame is the same as [gap19-complaints-with-denominators.md](gap19-complaints-with-denominators.md) §2.1: the FY2024 top-15 sponsors by corrected DAF assets, and the five DAFRC Donation Processors with the largest FY2024 grants.

### 2.2 Search order for each entity

1. The sponsor's own giving report, annual report or impact report (web page or PDF).
2. The sponsor's own press release, read on a robots-permitted host (prnewswire.com). Where the first-party copy was blocked, a verbatim trade-press reprint was used and marked as such.
3. The FY2024 Form 990, read from the GivingTuesday mirror of IRS e-file XML. The mirror is `gt990datalake-rawdata.s3.amazonaws.com`, and the object ids come from the repo's [`form990-returns-schedule-d-harvest-full.csv`](../../data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv) (`fiscal_year` = 2024). The full XML was downloaded and searched for three things:
   - Part III, Schedule O and other narrative text with a number followed by "grants", "donations", "disbursements" or "gifts";
   - the number of Schedule I Part II `RecipientTable` lines;
   - the Schedule I line 2 counts.
4. Web search for anything missed. Search snippets were never used as evidence. Every number in the CSV was read on the source page itself.

### 2.3 Status codes

| Status | Meaning |
|---|---|
| `stated` | The sponsor states a count for the period, in its own words (quoted) |
| `derived` | Computed here from the sponsor's own table (AEF: sum of state rows; FFTC 990: sum of nine Part III category counts) |
| `lower_bound_recipients` | Only a recipient count is published. Every recipient got at least one grant, so the count is a lower bound on grants |
| `derived_lower_bound_schedule_i` | The number of Schedule I Part II lines. Schedule I lists **only US organizations that received more than $5,000 in the year**, one line per recipient, so a line can stand for many grants, and grants to recipients under the threshold are missing. It is a lower bound on grants, usually a very loose one: Fidelity has 80,308 lines against 2,664,446 grants (3.0%) |
| `schedule_i_not_itemised` | The e-file Schedule I has a single line (BofA CGF, RCF), so the recipient list is not in the XML |
| `schedule_i_not_meaningful` | Dechomai Asset Trust: 6 lines, of which one $448.9m line is a transfer to Dechomai Foundation Inc |
| `not_found` | No count or lower bound found. The row records what was checked |

### 2.4 Choosing one denominator per entity

- **Primary:** the row with `is_primary` = 1. Where both a fiscal-year and a calendar-year count exist (NPT, Vanguard), the period matching the DAFRC FY2024 return is primary, so that per-grant, per-account and per-$ rates refer to the same year.
- **Fallback:** for entities without a primary row, the script uses the largest lower bound. The resulting rate is an **upper bound** and is labelled as one in `rate_kind`.

### 2.5 Rates and intervals

- **Numerators:** `n_complaint_mixed` by entity and scope (`all_venues`, `review_venues`, `strict`), read from [`complaint-rates-2026-11-19.csv`](../../data/mission-2026-11-14/complaint-rates-2026-11-19.csv). The window is 2021-01-01 to 2026-11-19 (5.881 years), with `dup_of` records already removed.
- **Rates:**
  - window rate = n / G × 10,000;
  - annual rate = n / 5.881 / G × 10,000. The annual rate is the headline figure, because G is a one-year count.
- **Intervals:** exact (Garwood) two-sided 95% Poisson intervals on n, computed by `poisson_ci()` in `mission_complaint_rates_gap19.py`, then scaled. For zero counts only the upper bound is meaningful (3.689 / scale).
  - Spot check: for Fidelity, n = 27 gives the interval [17.79, 39.28], which matches standard tables.
- **Pooled rows:** each record id is counted once. A "big three" record matches three sponsors but is one complaint, so the pooled all-venue numerator is 68, not the sum of the entity rows (83).
- **Consistency check:** `implied_avg_grant_usd` = FY2024 DAF grant dollars (DAFRC with R1 corrections) ÷ G. It is shown only for stated or derived counts. It flags mismatches of scope or period; it is not a rate input.

---

## 3. Results: grant counts

| # | Entity | Status | Grant count | Period | Matches DAFRC FY2024? | Source |
|---|---|---|---:|---|---|---|
| 1 | Fidelity Charitable | stated | 2,664,446 | CY2024 | partial (FY ends 30 Jun) | 2025 Giving Report, appendix: "Total grant volume and dollars … 2,664,446 $14.9B" [S1] |
| 2 | National Philanthropic Trust | stated | 129,575 | FY to 30 Jun 2024 | yes | Annual report chart "Number of individual grants recommended" [S2]; 990: "MORE THAN 129,000 GRANTS" [X2] |
| 3 | DAFgiving360 | stated (reprint) | >1,100,000 | FY to 30 Jun 2024 | yes | "more than 1.1 million individual grants supporting 141,000 charities" [S3] |
| 4 | Vanguard Charitable | stated | 221,825 | FY to 30 Jun 2024 | yes | 990: "ISSUED 221,825 GRANTS TOTALING OVER $3 BILLION" [X4]. CY2024: 240,064 [S4] |
| 5 | GS Philanthropy Fund | stated | ~29,254 | CY2024 | yes | 990: "MADE APPROXIMATELY 29,254 GRANTS TOTALING APPROXIMATELY $3,072,946,000" [X5] |
| 6 | SVCF | stated | >14,500 | CY2024 (preliminary) | yes | "awarded over 14,500 grants totaling $1.54 billion" [S5]. All SVCF grants, not DAF-only |
| 7 | Morgan Stanley GIFT | stated | 122,000 | CY2024 | yes | "Through 122,000 grants in 2024" (figures from Renaissance Administration LLC) [S6] |
| 8 | AEF | derived | 109,708 | CY2024 | yes | Sum of 51 state rows, "Number of Grants to the State"; the state dollars sum to $1,302,541,225, matching the headline "Over $1.3 billion"; values marked estimated [S7] |
| 9 | Renaissance Charitable Foundation | stated | >160,000 | CY2024 | yes | 990 Schedule O: "made over 160,000 grants to over 40,000 charitable organizations" [X9] |
| 10 | NCF | lower bound | >36,000 recipients | CY2024 | yes | "sent $2.6 billion to more than 36,000 churches, ministries, and other charities" [S8] |
| 11 | BofA Charitable Gift Fund | not found | — | — | — | No count in the 990; Schedule I has 1 e-file line [X11] |
| 12 | The Chicago Community Trust | not found | (3,976 Schedule I lines) | FY to 30 Sep 2024 | — | The 990's "498 grants" are competitive grants only; cct.org robots.txt returned 403 [X12] |
| 13 | ImpactAssets | stated (reprint) | 13,500+ | CY2024 | yes | "facilitated 13,500+ grants valued at close to $400 million" [S9] |
| 14 | Jewish Communal Fund | stated | 89,485 | FY to 30 Jun 2024 | yes | "89,485 total grants distributed by Fundholders" [S10] |
| 15 | Foundation For The Carolinas | stated | 16,531 | CY2024 | yes | "16,531 grants awarded to nonprofits across the U.S." [S11]; the 990 Part III categories sum to 16,362 [X15] |
| P1 | AOGF (Benevity) | lower bound | 40,985 Schedule I lines | FY to 31 Mar 2024 | yes | [X16] |
| P2 | PayPal Charitable Giving Fund | lower bound | 14,871 Schedule I lines | CY2024 | yes | [X17]; the global PPGF letter is not used (§6) |
| P3 | Blackbaud Giving Fund | lower bound | >123,000 recipients | CY2024 | yes | "disbursed funds … to more than 123,000 nonprofits worldwide in 2024" [S12] |
| P4 | Dechomai Asset Trust | not meaningful | (6 Schedule I lines) | CY2024 | — | $448.9m of $498.7m goes to Dechomai Foundation Inc [X19] |
| P5 | Network for Good (For Good) | lower bound | >22,000 recipients | CY2024 | yes | 990: "RAISED $202 MILLION IN DONATIONS IN 2024 TO OVER 22,000 DIFFERENT NONPROFITS" [X20] |

**Schedule I lines for comparison**, as a share of the stated count:
- Fidelity: 80,308 lines (3.0%);
- DAFgiving360: 55,292 (5.0%);
- Vanguard: 24,269 (10.9%);
- NPT: 18,583 (14.3%);
- MS GIFT: 19,253 (15.8%);
- GS: 7,424 (25.4%);
- JCF: 4,673 (5.2%);
- ImpactAssets: 2,733 (20.2%);
- FFTC: 1,605 (9.7%);
- SVCF: 3,576 (24.7%).

So Schedule I lines understate grants by about 4 to 33 times. Processor upper bounds built on them (AOGF, PPGF) are correspondingly loose.

**Terms-restricted rows re-read (2026-11-20).** Under the owner decision lifting the site-terms rule, b52-01 re-read rows 2 (NPT 129,575), 4 (Vanguard CY2024 240,064), 14 (JCF 89,485) and P3 (Blackbaud Giving Fund, more than 123,000 nonprofits; release dated 2025-10-20) at source, and wave 52A re-fetched them: all match. NPT’s FY25 report restates its earlier counts about 1% lower without a note; its FY24 report printed 130,875 grants and 41,879 recipients for FY2024. Row 2 keeps 129,575: it is NPT’s latest first-party figure and belongs to the same FY21–FY25 series as the dollars ($5.49bn) and international grants (406) the repo uses with it. [V wave 52A]

---

## 4. Results: complaint rates per 10,000 grants

All rates are from [`complaint-rates-per-grant-2026-11-20.csv`](../../data/mission-2026-11-14/complaint-rates-per-grant-2026-11-20.csv). "Annual" means per 10,000 grants per year, with the 95% exact Poisson CI. "UB" means the denominator is a lower bound, so the rate is an upper bound.

### 4.1 Entities with at least one record

| Entity | Scope | n | Grants G | Annual per 10k grants [95% CI] | Window per 10k grants | Kind |
|---|---|---:|---:|---|---:|---|
| Fidelity Charitable | all_venues | 50 | 2,664,446 | 0.0319 [0.0237–0.0421] | 0.188 | point |
| Fidelity Charitable | review_venues = strict | 27 | 2,664,446 | 0.0172 [0.0114–0.0251] | 0.101 | point |
| DAFgiving360 | all_venues | 15 | 1,100,000 | 0.0232 [0.0130–0.0382] | 0.136 | point |
| Vanguard Charitable | all_venues | 15 | 221,825 | 0.1150 [0.0644–0.1896] | 0.676 | point |
| GS Philanthropy Fund | all_venues | 1 | 29,254 | 0.0581 [0.0015–0.3239] | 0.342 | point |
| Morgan Stanley GIFT | all_venues | 1 | 122,000 | 0.0139 [0.0004–0.0777] | 0.082 | point |
| Renaissance Charitable Foundation | review_venues | 1 | 160,000 | 0.0106 [0.0003–0.0592] | 0.063 | point (low-attribution record) |
| AOGF (Benevity) | review_venues | 56 | ≥40,985 | ≤2.3233 [1.7550–3.0170] | ≤13.66 | UB |
| AOGF (Benevity) | strict | 47 | ≥40,985 | ≤1.9499 [1.4327–2.5930] | ≤11.47 | UB |
| PayPal Charitable Giving Fund | all_venues | 4 | ≥14,871 | ≤0.4574 [0.1246–1.1711] | ≤2.69 | UB |
| Blackbaud Giving Fund | review_venues | 3 | ≥123,000 | ≤0.0415 [0.0086–0.1212] | ≤0.244 | UB |
| Blackbaud Giving Fund | strict | 2 | ≥123,000 | ≤0.0276 [0.0033–0.0999] | ≤0.163 | UB |
| For Good | review_venues = strict | 7 | ≥22,000 | ≤0.5410 [0.2175–1.1147] | ≤3.18 | UB |
| POOLED top-15 (12 with counts) | all_venues | 68 | 4,670,824 | 0.0248 [0.0192–0.0314] | 0.146 | point |
| POOLED top-15 (12 with counts) | review_venues | 28 | 4,670,824 | 0.0102 [0.0068–0.0147] | 0.060 | point |
| POOLED top-15 (12 with counts) | strict | 27 | 4,670,824 | 0.0098 [0.0065–0.0143] | 0.058 | point |
| POOLED processors (4, lower bounds) | review_venues | 66 | ≥200,856 | ≤0.5587 [0.4321–0.7109] | ≤3.29 | UB |
| POOLED processors (4, lower bounds) | strict | 56 | ≥200,856 | ≤0.4741 [0.3581–0.6156] | ≤2.79 | UB |

### 4.2 What the per-grant view changes

- **Fidelity against AOGF.** Fidelity's review-venue rate per grant is 0.0172 per 10,000 per year. AOGF's is at most 2.32, a ratio of at most 135.
  - Parity would need AOGF to make 56 × 2,664,446 / 27 = **5,526,258** grants a year (strict: 4,638,110).
  - Benevity's micro-donation model (many small payroll gifts pooled into periodic disbursements) makes a large count plausible, but no count is published. So the per-grant ranking is **open**, not reversed (P-G1913-02-01).
- **Processors pooled.** A rate of at most 0.56 per 10,000 grants per year is at most 55 times the sponsor pool (0.0102). That ratio is a ceiling, for the same reason.
- **Sponsors.** On review venues only Fidelity and RCF have records. The per-grant figure for Fidelity (0.0172) is about 0.08 times its per-account annual rate (0.224 per 10,000 accounts per year, P-GAP19-13). That is simply 2,664,446 grants against 204,614 accounts, about 13 grants per account.

### 4.3 Zero-record upper bounds and the average-grant check

| Entity | Grants G (status) | 95% UB per 10k grants per year (review venues) | Implied average grant (DAFRC $ ÷ G) |
|---|---|---:|---:|
| DAFgiving360 | 1,100,000 (stated) | 0.0057 | $6,019 |
| Vanguard Charitable | 221,825 (stated) | 0.0283 | $13,782 |
| NPT | 129,575 (stated) | 0.0484 | $42,935 |
| Morgan Stanley GIFT | 122,000 (stated) | 0.0514 | $13,517 (report: "$11,000 average grant size") |
| AEF | 109,708 (derived) | 0.0572 | $11,898 |
| JCF | 89,485 (stated) | 0.0701 | $11,446 |
| NCF | ≥36,000 (recipients) | ≤0.1742 (loose) | — |
| GS Philanthropy Fund | 29,254 (stated) | 0.2144 | $105,005 |
| FFTC | 16,531 (stated) | 0.3794 | $43,661 (count covers all FFTC funds; DAFRC $ is DAF-only) |
| SVCF | 14,500 (stated) | 0.4326 | **$106,207** on SVCF’s own $1.54bn (release basis; $104,833 on audited grants net of $1,667m of DAF transfers). The DAFRC-dollar figure, $211,337, is an artefact of the $1,591.3m SVCF→NPT transfer (b39n603-02-g191302-03) [V wave 48A] |
| ImpactAssets | 13,500 (stated) | 0.4646 | $32,035 (release: "close to $400 million", which gives about $29,600) |
| PPGF | ≥14,871 (Schedule I lines) | ≤0.4218 (loose) | — |
| Chicago Community Trust | ≥3,976 (Schedule I lines) | ≤1.58 (loose) | — |
| BofA CGF; Dechomai | none | not computed | — |

Fidelity: $12.66bn of FY2024 DAFRC dollars ÷ 2,664,446 = $4,750. Fidelity's own CY2024 average is $5,422 (repo: queue-net-payout-fidelity-outliers.md). The difference is expected, because the FY dollars and the CY count cover different periods.

---

## 5. robots.txt and access log (2026-11-20, 03:54–04:00 UTC; user agent `research-script/1.0`)

Every robots.txt file was fetched before any other request to its host.

| Host | robots.txt | Decision / use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 20 full FY2024 990 XML files downloaded (about 236 MB in all) |
| www.fidelitycharitable.org | 200; disallows /retired/, /sample-email/, /nuance/, one /content/dam/…/vessel/ path | 2025 Giving Report PDF fetched |
| www.nptrust.org | 200; `User-agent: *` empty Disallow | Annual report page fetched |
| www.vanguardcharitable.org | 200; disallows /core/, /profiles/ (with asset Allows) | /2024annualreport fetched |
| www.dafgiving360.org | **403** | Treated as disallowed; not fetched |
| www.schwabcharitable.org | **403** | Not fetched |
| www.aboutschwab.com | **403** | Not fetched |
| pressroom.aboutschwab.com | 200; `Allow: /` | The page returned a Cloudflare "Just a moment…" challenge. Not retried and not worked around |
| www.businesswire.com | **no response** (HTTP/2 stream reset on robots.txt) | Not fetched (blocked) |
| www.prnewswire.com | 200; disallows /multivu/ | JCF and Blackbaud Giving Fund releases fetched |
| www.nonprofitpro.com | 200; disallows `/*?*`, /wp-json/ and others; article paths allowed | DAFgiving360 FY2024 reprint fetched |
| www.thinkadvisor.com / thinkadvisor.com | 301 / **403** | Not fetched |
| greenmoney.com | 200; empty Disallow | ImpactAssets 2025 Impact Report reprint fetched |
| business.mammothtimes.com | **no response** | Not fetched |
| www.svcf.org (www.siliconvalleycf.org → svcf.org) | 200; disallows /cpresources/, /vendor/, /.env, /cache/ | 2024 results blog post fetched |
| www.morganstanley.com | 200; `User-agent: *` disallows /content/ but allows /content/dam/msdotcom/ (the longer rule wins) | MS GIFT impact report PDF fetched |
| www.aefonline.org | 200; empty Disallow; crawl-delay 10 | Two impact-map PDFs, 11 s apart |
| www.reninc.com | 200; disallows /wp-admin/ | Not needed (the RCF count is in the 990) |
| www.ncfgiving.com | 200; empty Disallow | 2024 Impact Report story fetched; /impactreportpdf/ now redirects to the 2025 page |
| www.cct.org | **403** | Treated as disallowed; not fetched |
| impactassets.org (www → bare) | 200; disallows /wp-admin/ | /our-impact/ fetched (now shows 2025: 14,600+) |
| jcfny.org (www → bare) | 200; disallows /wp/wp-admin/ | Not needed |
| www.fftc.org | 200; disallows /core/, /profiles/, /admin/, /search/ and similar | 2024–2025 Annual Report PDF fetched |
| benevity.com (www → bare); www.aogf.org | 200; allow all | No page with an AOGF count found by search, so nothing fetched |
| www.paypalgivingfund.org → www.paypal.com | 301 to paypal.com; paypal.com robots 200 (no rule on /us/webapps/mpp/) | Nothing fetched (no US count found by search) |
| www.blackbaud.com, www.yourcause.com | 200; blackbaud.com disallows /wp-content/uploads/*.pdf | Nothing fetched |
| dechomai.org (www → bare) | 200; empty Disallow | Nothing fetched |
| www.forgood.org | 200; sitemap only | Nothing fetched |
| www.networkforgood.com | 301 to bonterratech.com | Nothing fetched |
| www.gsphilanthropyfund.org | no response (DNS/connection) | Not used (GS count from the 990) |

- crt.sh, certspotter and sec.gov were not used.
- There was no outreach, no login and no form.
- All evidence is 2024 or later.

---

## 6. Limits

- **Numerator and denominator years differ.** Complaints span 2021-01-01 to 2026-11-19; grant counts cover one year (FY2024 or CY2024). The annual rate divides by 5.881 and assumes a stable grant base. That assumption is optimistic for fast growers: Fidelity went from 2.19m grants (CY2022, repo F1) to 3m (CY2025, repo panel S04) (P-G1913-02-06). For Fidelity the bias is small. Summing yearly counts over the window gives about 14.99m grant-years against the 15.67m assumed. The inputs are: 2021 set equal to CY2022’s 2,185,516; about 2.3m for 2023; 2,664,446 for CY2024; 3m for 2025; and the 2025 level for the 323 days of 2026. On that basis the review-venue rate is about 0.0180 rather than 0.0172 (+4.5%). [V wave 46B]
- **Periods are mixed.** Fidelity is on a calendar year against a June fiscal year in DAFRC. AOGF's lower bound is for the year ended 31 March 2024. The other counts match the DAFRC FY2024 period.
- **Unit and scope differ across sources:**
  - "grants recommended" (NPT, DAFgiving360) versus "grants issued" (Vanguard) versus "grants distributed" (JCF);
  - SVCF and FFTC counts include non-DAF grants;
  - AEF covers US grants only and is marked "estimated";
  - SVCF's count is preliminary and unaudited.
- **Rounded counts.** DAFgiving360 ("more than 1.1 million"), RCF ("over 160,000"), MS GIFT (122,000), SVCF ("over 14,500") and ImpactAssets ("13,500+") are rounded floors. The script uses the stated figure, so these rates are slightly high.
- **Secondary carriers.** Two counts (DAFgiving360, ImpactAssets) come from verbatim trade-press reprints of sponsor releases, because the first-party copies were blocked (robots 403, Cloudflare challenge, or connection reset). They are marked `first_party = no`. The NonProfit PRO page ends “Source: DAFgiving360” and “The preceding press release was provided by a company unaffiliated with NonProfit PRO”. So it carries the sponsor’s own release, and its period (FY to 30 June 2024) matches. It is acceptable as a stated count. The FY2024 990 itself states no count. [V wave 46B]
- **Processor denominators are lower bounds only.**
  - The PPGF 2024 letter found by search (20.4 million donations, 226,000+ charities) is global across PPGF entities, counts inbound donations, and is hosted on a third-party mirror. It was not used.
  - Benevity platform figures cover all its granting foundations and countries.
- **Venue presence still dominates.** 13 of the 15 sponsors have no review-venue record (P-GAP19-13 §6). A per-grant zero is "not observed", not "none".
- **Allegations, not findings.** The numerators are unchanged from P-GAP19-13 and carry its caveats.

---

## 7. Data dictionaries

### 7.1 `grant-count-denominators-2026-11-20.csv`

| Column | Type | Definition |
|---|---|---|
| row_id | text | `GC-NNN` |
| entity | text | Entity name, spelled exactly as in `complaint-rates-2026-11-19.csv` |
| entity_group | enum | `top15_sponsor`, `processor` |
| ein | text | 9-digit EIN (join key to the rates CSV) |
| count_status | enum | `stated`, `derived`, `lower_bound_recipients`, `derived_lower_bound_schedule_i`, `schedule_i_not_itemised`, `schedule_i_not_meaningful`, `not_found` (§2.3) |
| is_primary | 0/1 | 1 = the denominator used for this entity's point rate |
| grant_count | integer | Count as stated or derived. For lower bounds, the bound. Blank if none |
| count_qualifier | text | `exact`, `approximately`, `over`, `more than`, `rounded`, or how it was derived |
| count_unit | text | What is counted (grants recommended / issued / distributed; recipients; Schedule I lines) |
| period_label, period_start, period_end | text / date | Period of the count |
| dafrc_fy2024_period_end | date | Year end of the entity's DAFRC FY2024 return |
| period_match | text | `yes`, `partial`, or blank |
| scope_note | text | Coverage caveats (non-DAF grants, US only, preliminary) |
| quote | text | The exact words at the source (capitals as in the 990) |
| source_class | enum | `sponsor_report`, `sponsor_blog`, `sponsor_press_release`, `trade_press_reprint`, `form_990_part_iii`, `form_990_schedule_o`, `form_990_schedule_i` |
| first_party | text | `yes`, `yes (filed)`, or `no (…)` |
| url | text | Primary URL read (990 rows: mirror XML URL with the IRS object id) |
| robots_result | text | robots.txt status for the host (§5) |
| retrieved | date | 2026-11-20 |
| notes | text | Free text |

### 7.2 `complaint-rates-per-grant-2026-11-20.csv`

| Column | Type | Definition |
|---|---|---|
| entity, entity_group, ein, scope | text | As in `complaint-rates-2026-11-19.csv`; pooled rows are `POOLED <group> (…)` |
| window_years | number | 5.881 |
| n_complaint_mixed | integer | Numerator (pooled: distinct record ids) |
| grant_count | integer | Denominator G chosen by §2.4 |
| denominator_status | text | `count_status` of the chosen row, or `not_found` |
| denominator_period, denominator_row_id | text | Period label and `row_id` in the denominators CSV |
| rate_per_10k_grants_window (+ window_ci95_low / _high) | number | n / G × 10,000 with exact Poisson 95% bounds |
| annual_rate_per_10k_grants (+ annual_ci95_low / _high) | number | The above ÷ window_years |
| rate_kind | text | `point estimate`, `upper bound (…)`, `zero records: upper bound only`, `not computed (…)` |
| fy2024_daf_grants_usd | integer | From the P-GAP19-13 CSV (DAFRC with R1 corrections) |
| implied_avg_grant_usd | number | fy2024_daf_grants_usd ÷ G (stated or derived G only); a consistency check |
| rate_per_1bn_grants_p_gap19_13, rate_per_10k_accounts_p_gap19_13 | number | Copied for side-by-side comparison |
| record_ids | text | Counted record ids from P-GAP19-13 |

---

## 8. Source register

| ID | Source | Used for | URL |
|---|---|---|---|
| S1 | Fidelity Charitable, *2025 Giving Report* (pp. 19 and appendix) | CY2024 2,664,446 grants | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf |
| S2 | NPT annual report (FY21–FY25 chart) | FY2024 129,575 | https://www.nptrust.org/annual-reports/npt-annual-report/ |
| S3 | NonProfit PRO reprint of the DAFgiving360 FY2024 release (2024-07-23) | FY2024 >1.1m | https://www.nonprofitpro.com/article/dafgiving360-donors-give-more-than-6-6b-to-charities-in-fiscal-year-2024/ (first-party copy, not fetched: https://www.dafgiving360.org/press-release/fiscal-year-2024-results) |
| S4 | Vanguard Charitable 2024 annual report | CY2024 240,064 (alternative) | https://www.vanguardcharitable.org/2024annualreport |
| S5 | SVCF blog, "SVCF granted $1.54 billion to nonprofits in 2024" | CY2024 >14,500 (preliminary) | https://www.svcf.org/about/news-media/blog/silicon-valley-community-foundation-granted-1.54-billion-to-nonprofits-in-2024 |
| S6 | Morgan Stanley GIFT impact report (2024 in review) | CY2024 122,000 | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf |
| S7 | AEF *DAFs: Impact by State*, V3.4 (2024 data) | 51 state grant counts → 109,708 | https://www.aefonline.org/wp-content/uploads/2025/10/AEF_DAFImpactMap_V3.4.pdf |
| S8 | NCF, "2024 Impact Report: Shining like stars" | >36,000 recipients | https://www.ncfgiving.com/stories/2024-impact-report-shining-like-stars |
| S9 | GreenMoney reprint of the ImpactAssets 2025 Impact Report release | CY2024 13,500+ | https://greenmoney.com/impactassets-2025-impact-report-15-years-of-driving-capital-for-real-world-impact/ |
| S10 | JCF release, 2024-08-22 (PR Newswire) | FY2024 89,485 | https://www.prnewswire.com/news-releases/jewish-communal-fund-donors-grant-record-breaking-1-billion-in-fiscal-year-2024-302227664.html |
| S11 | FFTC *2024–2025 Annual Report* | CY2024 16,531 | https://www.fftc.org/sites/default/files/2025-04/FFTC_2024-2025_Annual_Report.pdf |
| S12 | Blackbaud Giving Fund release, 2025-10-20 (PR Newswire) | >123,000 recipients | https://www.prnewswire.com/news-releases/the-blackbaud-giving-fund-surpasses-550m-in-charitable-giving-in-2024--reaching-2-75b-in-lifetime-giving-302588766.html |
| X1–X20 | FY2024 Form 990 e-file XML (IRS TEOS via the GivingTuesday mirror), `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`. Object ids: Fidelity 202521349349310887; NPT 202511339349301311; DAFgiving360 202541069349300729; Vanguard 202511349349313096; GS 202503109349303645; SVCF 202543149349305759; MS GIFT 202503239349300435; AEF 202513219349310376; RCF 202543189349301959; NCF 202513109349303201; BofA 202503219349318170; CCT 202512119349301861; ImpactAssets 202543169349307999; JCF 202500369349300210; FFTC 202543219349306689; AOGF 202530159349302758; PPGF 202533079349301308; Blackbaud GF 202542169349301664; Dechomai 202523159349304782; Network for Good 202513039349301631 | Part III / Schedule O counts; Schedule I lines | as listed |
| R1 | P-GAP19-13 complaint rates (numerators, $ and account rates) | Numerators | data/mission-2026-11-14/complaint-rates-2026-11-19.csv |
| R2 | Repo grant-rail panel (Fidelity 2.7m, CY2025 3m) | Cross-check | data/mission-2026-11-14/grant-rail-shares-panel-2026.csv |
| R3 | Repo per-grant work (Fidelity CY2022/CY2023 counts; earlier robots log) | Cross-check | research/mission-2026-11-14/g0401-g0502-ai-routing-and-per-grant.md §B2, §S1–S2 |
