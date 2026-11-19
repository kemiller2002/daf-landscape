# DAF complaints with denominators: BBB, Trustpilot and Google Play for the top-15 sponsors and five processors

**Queue item:** P-GAP19-13 | **Research date:** 2026-11-19 | **Builds on:** [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md) (coding scheme, §2) and [`scripts/mission_complaint_rates.py`](../../scripts/mission_complaint_rates.py) (P-QA3-04 rates; not modified)

**Files written**
- [`data/mission-2026-11-14/daf-user-complaints-corpus-additions-2026-11-19.csv`](../../data/mission-2026-11-14/daf-user-complaints-corpus-additions-2026-11-19.csv): 47 new records, same 21 columns as the corpus. 45 are complaints, 1 mixed, 1 praise.
- [`data/mission-2026-11-14/complaint-rates-2026-11-19.csv`](../../data/mission-2026-11-14/complaint-rates-2026-11-19.csv): 67 rows. There are 20 entities × 3 scopes, plus 1 venue-reported aggregate and 6 pooled rows. The data dictionary is in §8.
- [`scripts/mission_complaint_rates_gap19.py`](../../scripts/mission_complaint_rates_gap19.py): stdlib-only, functional style. It refuses to overwrite its output unless given `--force`.
- [`data/mission-2026-11-14/queue-proposals-gap19-13.csv`](../../data/mission-2026-11-14/queue-proposals-gap19-13.csv): 6 rows, P-G1913-01 to -06.

**Naming note:** the brief asked for `scripts/mission_complaint_rates.py`, but that file already exists (P-QA3-04, 16 sponsors, corpus only). The rule against overwriting files took precedence, so the new script uses the `_gap19` suffix.

**Method:** public pages only. We created no accounts, made no logins, posted nothing and contacted no one. We did not use crt.sh or certspotter. Every host's robots.txt was read before its first fetch (§3). We do not reproduce complainants' names, the names of the small nonprofits they work for, or staff names in business responses. Quotes are short fragments (25 words or fewer).

---

## 1. Summary

1. **On the three requested venues, only 3 of the 15 largest sponsors have any public complaint surface.**
   - Fidelity Charitable has a Google Play app. Ren (the administrator of Renaissance Charitable Foundation) has a two-review Trustpilot page. Silicon Valley Community Foundation has a Trustpilot page with 0 reviews.
   - The other 12 have no Trustpilot profile, no Google Play app that we could find, and no BBB profile that we could find (§3–§4).
   - For 13 of 15 sponsors, the review-venue numerator is therefore zero. That is a fact about venues, not about service.
2. **Processors are where the review venues bite.**
   - The five processors with the most FY2024 grants are AOGF (Benevity), PayPal Charitable Giving Fund, Blackbaud Giving Fund (YourCause), Dechomai and Network for Good (For Good).
   - 42 of the 46 new complaint or mixed records concern them, and 27 of the 46 come from nonprofits (including one volunteer).
3. **Rates depend on the denominator.** On review venues, 2021-01-01 to 2026-11-19 ([rates CSV](../../data/mission-2026-11-14/complaint-rates-2026-11-19.csv)):
   - **Fidelity Charitable:** 27 records. That is **1.32 per 10,000 FY2024 accounts [95% CI 0.87–1.92]**, or 2.13 per $1bn of FY2024 grants [1.41–3.10].
   - **AOGF/Benevity:** 56 records. That is **0.78 per 10,000 accounts [0.59–1.01]**, but **28.7 per $1bn of grants [21.7–37.3]**. The 56 include 9 added reviews from non-US reviewers (Benevity's other programmes). On the strict scope (47 records), the figures are 0.65 per 10,000 [0.48–0.87] and 24.1 per $1bn [17.7–32.0] [V wave 32B]
   - So per account, Fidelity ranks worse than AOGF; per grant dollar, AOGF is about 13 times worse on review venues and 11 times worse on the strict scope. Neither ranking is a prevalence estimate (§6) [V wave 32B]
4. **Network for Good has the highest rate per grant dollar, but its account count is unusable.**
   - It shows 40.0 complaints per $1bn [17.3–78.9] on review venues, from 8 records. One Trustpilot/BBB pair (-037/-040) is a single incident, so the distinct-incident rate is 35.0 per $1bn [14.1–72.2] from 7 [V wave 32B]
   - DAFRC's FY2024 account count for it is "1". DAFRC marks it imputed, and the filed 990 also shows 1, so we did not compute a per-account rate [V wave 32B]
   - BBB Wise Giving Alliance's own count is 2 complaints in 36 months, both about check disbursement. That gives 10.0 per $1bn over 3 years [1.2–36.2] ([give.org](https://give.org/charity-reviews/other/forgood-in-washington-dc-9999-1290)).
5. **Adding the new records changes the headline category.**
   - Across all 2021+ complaint and mixed records (123 old + 46 new = 169), **grant delay (33)** now leads, ahead of UX/app (25), discretion (20), and account access and receipt/attribution (18 each).
   - The original corpus led with UX/app and login. That came from the App Store. App-store records (104 App Store plus 6 Google Play) now make up 110 of 291 records (37.8%, down from 42.6%) [V wave 32B]
6. **The new processor complaints mostly describe rules, not one-off bugs.** Examples:
   - a $75 matched gift held about eight months because the charity is below a paper-check threshold (CMP-G1913-001);
   - a returned check that YourCause would not reissue until the charity registered, after which the gift went to an employer-chosen charity (CMP-G1913-034);
   - $6,400 held since 2024 over a tax issue (CMP-G1913-041);
   - checks reissued only after 45 days (CMP-G1913-043).
   All but one of the new records are coded fixable. The YourCause redirection is coded structural.
7. **Fidelity Charitable's Android app repeats the iOS pattern.** All three visible Google Play reviews (July–August 2026) say the app will not open or crashes on current phones. The listing shows 3.8 stars from 29 reviews, 5K+ downloads, updated 2026-11-09 ([Google Play](https://play.google.com/store/apps/details?id=com.fidelity.charitable)).

---

## 2. Scope and method

### 2.1 Entity frame (20 entities)

**Top-15 sponsors:** ranked by FY2024 corrected DAF assets in [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv) (`fiscal_year` 2024, `row_type` top50):
1. Fidelity Charitable
2. National Philanthropic Trust (NPT)
3. DAFgiving360
4. Vanguard Charitable
5. Goldman Sachs Philanthropy Fund (GS DAPF)
6. Silicon Valley Community Foundation (SVCF)
7. Morgan Stanley GIFT
8. American Endowment Foundation (AEF)
9. Renaissance Charitable Foundation (RCF)
10. National Christian Foundation (NCF)
11. BofA Charitable Gift Fund
12. The Chicago Community Trust
13. ImpactAssets
14. Jewish Communal Fund
15. Foundation For The Carolinas

**Five processors:** the five DAFRC `subtype = Donation Processor` sponsors with the largest FY2024 DAF grants after R1 corrections:
1. American Online Giving Foundation (AOGF; Benevity), $1.95bn
2. PayPal Charitable Giving Fund (PPGF), $0.80bn
3. Blackbaud Giving Fund (BGF; YourCause), $0.55bn
4. Dechomai Asset Trust, $0.55bn
5. Network for Good / For Good, $0.20bn

Mightycause ($0.10bn) is sixth. Givinga, which `mission_complaint_rates.py` includes, is outside the top five by grants ($12.4m).

### 2.2 Collection

| Venue | What was read | Unit kept |
|---|---|---|
| Trustpilot | `/review/<domain>` for 22 candidate domains (bare and `www.`). Each profile was read through its last page with `?page=N`. Data comes from the page's embedded JSON | Each giving-related review dated 2021 or later. Reviews about a vendor's unrelated software (CRM, school, tuition, UK donation forms) are excluded and counted in §3.2 |
| BBB | Profile `/complaints` pages, found only through a search engine (on-site search is robots-blocked, §3). Bonterra Tech (2 pages, all 17 complaints) and Blackbaud Inc (3 pages, 21 published of 24) | Each giving-related complaint. BBB itself caps the window at 3 years |
| Google Play | `/store/apps/details?id=…` for package ids found by search or redirect (Benevity's own download link). Only the reviews the details page renders are readable | All visible reviews (3 per app) plus the public rating, review count and download band |
| give.org (BBB Wise Giving Alliance) | Charity reports for For Good and PPGF, found through search | Government-action items and BBB complaint counts |

### 2.3 Coding and filters

**Coding** follows the corpus scheme exactly: the same category taxonomy, severity scale, structural/fixable rule and E1–E4 grades.
- Benevity records keep `organization` = Benevity, as in the corpus. The notes map them to AOGF (EIN 81-0739440) for the rates.
- `notes` carries machine-readable tokens: `country=XX` (Trustpilot reviewer country) and `dup_of=<record_id>` (the same incident in two venues).
- Record ids use the prefix `CMP-G1913-NNN` so they cannot collide with future `CMP-NNN` corpus rows.

**Window:** 2021-01-01 to 2026-11-19, which is 5.881 years (2,148 days ÷ 365.25) [V wave 32B] Records whose first year is before 2021 are excluded, as in `mission_complaint_rates.py`.

**Numerator scopes:**
- **all_venues:** every in-window complaint or mixed record, old corpus plus additions.
- **review_venues:** `venue_type` is `app_store` or `review_site` (App Store, Google Play, Trustpilot, BBB complaint pages). This is the scope the task targets.
- **strict:** review_venues, minus three groups:
  - attribution confidence starting with "low";
  - `dup_of` records;
  - reviewers whose country is known and not US. AOGF is the US entity, while Benevity's Trustpilot page also covers its Canadian, UK and other programs.

**Denominators:** FY2024 `number_of_daf_accounts` and `total_daf_grants` come from [`dafrc-sponsor-schedule-d-fy2019-2024.csv`](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv). The applied R1 "filed replaces imputed" corrections in [`dafrc-corrections-itemized.csv`](../../data/mission-2026-11-14/dafrc-corrections-itemized.csv) are layered on top, so the values match the league table. No other account source was used, and no count was estimated.
- Account counts below 10 are treated as implausible and not used (Network for Good: 1).
- Imputed counts are flagged (Blackbaud Giving Fund: 460).

**Rates:**
- n / accounts × 10,000 over the whole window;
- the same divided by 5.881 for a per-year rate [V wave 32B]
- n per $1bn of FY2024 grants.

**Intervals:** exact (Garwood) 95% Poisson intervals on n, scaled by the denominator. We used Poisson rather than Wilson because one account can generate several complaints and complaints are not Bernoulli trials over accounts. For zero counts we report only the upper bound (3.69 / denominator).

---

## 3. Robots and access log (2026-11-19, about 17:10 UTC)

Every robots.txt file was fetched before any other request to its host. Fetches identified as `Claude-User`, a user-directed agent. Where a robots group names Anthropic agents, that group was applied.

| Host | robots.txt result | What it allows / blocks for this task | Outcome |
|---|---|---|---|
| www.trustpilot.com | 200. `User-agent: *` → `Disallow: /`. Named groups for ClaudeBot, Claude-User and Claude-SearchBot allow `/review/<domain>` (they block `/reviews/`, `/review/*/transparency`, `/search`, `/api/*` and filtered query strings such as `?stars=`). `anthropic-ai` → `Disallow: /` | Profile pages and `?page=N` are **allowed** for Claude-User. **On-site search is blocked**, so profiles could only be found by trying domains | Read: benevity.com (87 listed, 5 pages), blackbaud.com (17), networkforgood.com (17, titled "Bonterra Guided Fundraising"), www.reninc.com (2), siliconvalleycf.org (0), www.bonterratech.com (0). **404 (no profile):** fidelitycharitable.org, nptrust.org, dafgiving360.org, schwabcharitable.org, vanguardcharitable.org, gsphilanthropyfund.org, svcf.org, aefonline.org, ncfgiving.com, cct.org, impactassets.org, jcfny.org, fftc.org, paypalgivingfund.org, yourcause.com, dechomai.org (bare and `www.`) |
| www.bbb.org | 200. The block for named AI agents (including ClaudeBot, Claude-User, Claude-SearchBot) is the same as for `*`: `Disallow: /*?` with `Allow: /us/*/*/profile/*/*?`; `/business-reviews/*` and `/file-a-complaint/*` disallowed | Profile and `/complaints` pages are **allowed**, including `?page=N` pagination. **BBB search (`/search?…`) is blocked.** BBB's `llms.txt` confirms that search results are not crawlable | Read: Bonterra Tech (Austin) complaints p.1–2; Blackbaud Inc (Daniel Island) p.1–3 (p.4 empty); a second Blackbaud (Austin) profile (1 tuition complaint, out of scope). A Network for Good (DC) profile URL from search returns 404. **No profile found** for the other 18 entities through the search engine. This is **not determinable** rather than "none": BBB's own search is blocked and we did not work around it. The sitemaps are allowed (580 files) but were not parsed (P-G1913-01) |
| play.google.com | 200. `User-Agent: *` allows `/store/apps/details`; disallows `/store/getreviews`, `/_` (data/batch endpoints), `/store/search`, `/store/apps/datasafety*` | Details pages are **allowed**. **The full review list is blocked**: it loads only through disallowed endpoints. **Store search is blocked** | Read: com.fidelity.charitable (3.8★, 29 reviews, 5K+), org.benevity.app (3.2★, 94 reviews, 50K+; id from Benevity's own download redirect). com.daffy.app is an unrelated app ("Daffy S&D", another developer), which confirms the corpus note that Daffy has no Android app. No apps found for the other 18 entities (NCF says to use its mobile website) |
| give.org | 200. Disallow `/` for ClaudeBot, anthropic-ai and Claude-Web (training). `User-agent: *` allowed, and the file names Claude-User as allowed | Charity reports **allowed** | Read: For Good (report issued Aug 2026) and PPGF (Jul 2026) |
| apps.apple.com / itunes RSS | Not re-fetched | No new App Store collection. The corpus's 104 App Store rows are reused | — |
| reddit.com | Not attempted | It was blocked on 2026-11-14 (corpus §3). Not retried | Blocked (carried) |

**Note on the earlier corpus.** Corpus §3 cites a `bbb.org/search?…` result from 2026-11-14. Under the robots.txt read today, BBB search URLs are disallowed for every agent. We did not use BBB search in this pass.

### 3.1 Records added, by venue and entity

| Venue | Entity | Read | Coded (2021+) | Excluded and why |
|---|---|---|---|---|
| Trustpilot | Benevity (→ AOGF) | 87 reviews | 27 (26 complaint, 1 of them low-attribution; 1 praise) | 38 matched to existing corpus records by date (3 corpus Benevity records no longer appear on the page). 21 webinar-feedback reviews (excluded as in the corpus). 1 personal attack naming an individual |
| Google Play | Benevity (→ AOGF) | 3 visible | 3 (2 complaint, 1 mixed) | — |
| Google Play | Fidelity Charitable | 3 visible | 3 complaint | — |
| Trustpilot | Blackbaud company profile | 17 | 2 (YourCause gift redirection; 1 low-attribution giving item) | 15 about school, CRM, tuition or UK form software, or dated 2020 |
| BBB | Blackbaud Inc | 21 published (24 counted) | 1 (employer-matched gift check lost, not reissued) | 20 about CRM contracts, tuition and billing |
| Trustpilot | Network for Good | 17 | 3 | 14 about CRM or fundraising software, billing or coaching |
| BBB | Bonterra Tech (Network for Good) | 17 | 5 (1 is `dup_of` the Trustpilot item) | 12 about CRM or political-software billing and auto-renewals |
| give.org | For Good; PPGF | 2 reports | 2 regulator items (the PPGF item is `dup_of=CMP-232`) | — |
| Trustpilot | Ren (reninc.com) | 2 | 1 (low attribution: product not stated) | 1 about a charitable remainder trust, not a DAF |
| **Total** | | | **47** | |

### 3.2 Why vendor profiles are filtered

Blackbaud, Bonterra/Network for Good and Ren are software or administration companies. Their Trustpilot and BBB pages mix complaints about the DAF or giving fund with complaints about CRM, tuition-payment, school and political software.

- Only items about the giving-fund function (disbursement, gift routing, nonprofit enrollment for payouts, donor gift records) are coded.
- 61 vendor-profile items were excluded on this test (15 + 20 + 14 + 12 in the table above).
- Including them would raise the Blackbaud and Network for Good counts from 11 to 72, about 6.5 times.

---

## 4. Rates

### 4.1 Entities with at least one record

All rates use FY2024 denominators and the 2021-01-01 to 2026-11-19 window. "n/c" means not computed (no usable account count).

| Entity | Scope | FY2024 accounts (quality) | FY2024 DAF grants | n | of which added | per 10k accounts [95% CI] | per 10k accounts per year | per $1bn grants [95% CI] |
|---|---|---|---|---|---|---|---|---|
| Fidelity Charitable | all_venues | 204,614 (filed) | $12.66bn | 50 | 3 | 2.444 [1.814–3.222] | 0.416 | 3.950 [2.932–5.208] |
| Fidelity Charitable | review_venues | 204,614 (filed) | $12.66bn | 27 | 3 | 1.320 [0.870–1.920] | 0.224 | 2.133 [1.406–3.104] |
| Fidelity Charitable | strict | 204,614 (filed) | $12.66bn | 27 | 3 | 1.320 [0.870–1.920] | 0.224 | 2.133 [1.406–3.104] |
| DAFgiving360 | all_venues | 112,188 (filed) | $6.62bn | 15 | 0 | 1.337 [0.748–2.205] | 0.227 | 2.266 [1.268–3.737] |
| Vanguard Charitable | all_venues | 27,660 (filed) | $3.06bn | 15 | 0 | 5.423 [3.035–8.944] | 0.922 | 4.907 [2.746–8.093] |
| GS Philanthropy Fund | all_venues | 4,134 (filed) | $3.07bn | 1 | 0 | 2.419 [0.061–13.478] | 0.411 | 0.326 [0.008–1.814] |
| Morgan Stanley GIFT | all_venues | 21,800 (filed) | $1.65bn | 1 | 0 | 0.459 [0.012–2.556] | 0.078 | 0.606 [0.015–3.379] |
| Renaissance Charitable Foundation | review_venues | 25,824 (filed) | $0.77bn | 1 | 1 | 0.387 [0.010–2.158] | 0.066 | 1.297 [0.033–7.229] |
| AOGF (Benevity) | review_venues (= all) | 720,545 (filed) | $1.95bn | 56 | 29 | 0.777 [0.587–1.009] | 0.132 | 28.715 [21.691–37.288] |
| AOGF (Benevity) | strict | 720,545 (filed) | $1.95bn | 47 | 20 | 0.652 [0.479–0.867] | 0.111 | 24.100 [17.708–32.048] |
| PayPal Charitable Giving Fund | all_venues | 380,644 (filed) | $0.80bn | 5 rows; 4 distinct (CMP-G1913-046 is dup_of CMP-232) | 1 | 0.131 [0.043–0.307]; distinct 0.105 [0.029–0.269] | 0.022; distinct 0.018 | 6.284 [2.040–14.665]; distinct 5.027 [1.370–12.871] [V wave 32B]
| Blackbaud Giving Fund (YourCause) | review_venues (= all) | 460 (imputed) | $0.55bn | 3 | 3 | 65.2 [13.4–190.6] (unreliable) | 11.090 | 5.429 [1.120–15.866] |
| Blackbaud Giving Fund (YourCause) | strict | 460 (imputed) | $0.55bn | 2 | 2 | 43.5 [5.3–157.1] (unreliable) | 7.393 | 3.619 [0.438–13.074] |
| Network for Good (For Good) | all_venues | 1 (implausible) | $0.20bn | 9 rows; 8 distinct (-040 is dup_of -037) | 9 | n/c | n/c | 45.053 [20.601–85.525]; distinct 40.047 [17.290–78.909] [V wave 32B]
| Network for Good (For Good) | review_venues | 1 (implausible) | $0.20bn | 8 rows; 7 distinct (-040 is dup_of -037) | 8 | n/c | n/c | 40.047 [17.290–78.909]; distinct 35.041 [14.088–72.199] [V wave 32B]
| Network for Good (For Good) | strict | 1 (implausible) | $0.20bn | 7 | 7 | n/c | n/c | 35.041 [14.088–72.199] |
| Network for Good (For Good) | BBB WGA 36-month count | 1 (implausible) | $0.20bn | 2 | — | n/c | n/c | 10.012 [1.212–36.166] (3-year window) |
| Pooled top-15 sponsors | review_venues | 230,438 (Fidelity + RCF) | $13.43bn | 28 | 4 | 1.215 [0.807–1.756] | 0.207 | 2.085 [1.386–3.014] |
| Pooled processors | review_venues | n/c | $2.70bn | 67 rows; 66 distinct | 40 | n/c | n/c | 24.791 [19.213–31.484]; distinct 24.421 [18.887–31.070] [V wave 32B]

DAFgiving360, Vanguard Charitable, GS DAPF, Morgan Stanley GIFT and PPGF have **zero** review-venue records. Their all-venue counts come entirely from forums, press, regulators and advocacy groups.

### 4.2 Zero-record entities: upper bounds only

These are strict-scope rows. The upper bound is only what a complete venue would allow; these venues are not complete (§6).

| Entity | FY2024 accounts | 95% upper bound per 10k accounts | 95% upper bound per $1bn grants |
|---|---|---|---|
| DAFgiving360 | 112,188 | 0.33 | 0.56 |
| Vanguard Charitable | 27,660 | 1.33 | 1.21 |
| NPT | 17,940 | 2.06 | 0.66 |
| NCF | 31,943 | 1.16 | 1.52 |
| AEF | 15,947 | 2.31 | 2.83 |
| BofA CGF | 17,840 | 2.07 | 3.82 |
| Morgan Stanley GIFT | 21,800 | 1.69 | 2.24 |
| GS DAPF | 4,134 | 8.92 | 1.20 |
| Jewish Communal Fund | 4,842 | 7.62 | 3.60 |
| ImpactAssets | 2,197 | 16.79 | 8.53 |
| Chicago Community Trust | 1,914 | 19.27 | 2.62 |
| SVCF | 1,011 | 36.49 | 1.20 |
| Foundation For The Carolinas | 1,047 | 35.23 | 5.11 |
| PPGF | 380,644 | 0.10 | 4.64 |
| Dechomai | 314 | 117.5 | 6.68 |

### 4.3 Denominator notes

- **Processor "accounts" are not sponsor DAF accounts.** AOGF's 720,545 (IRS 990) almost certainly counts workplace donor accounts. PPGF's 380,644 is a filed count that replaced DAFRC's imputed 694,979. These figures cannot be compared with Fidelity's 204,614 donor-advised accounts. This is the main reason the per-account and per-dollar rankings diverge (P-G1913-03).
- **Grant dollars are the more comparable denominator across sponsors and processors.** They are still a weak unit for delay complaints, which happen per gift.
- **Fidelity grant-count side calculation (not in the CSV).** The repository's [`grant-rail-shares-panel-2026.csv`](../../data/mission-2026-11-14/grant-rail-shares-panel-2026.csv) records Fidelity's "nearly 2.7 million grants in 2024". Dividing 27 review-venue complaints over 5.88 years by that one-year grant count gives **about 0.017 complaints per 10,000 grants per year**. No other entity in the frame has a grant count in the repo (P-G1913-02).
- **DAFRC FY2024 timing** means fiscal years ending in 2024 or early 2025 (AOGF's year ends 31 March). Complaints span about six years; the denominators are one year. The per-year column divides by 5.881 and assumes a stable account base, which is optimistic for growing sponsors [V wave 32B]

---

## 5. What the new records say

### 5.1 By category

The new records number 46 complaint/mixed plus 1 praise.

| Category | n | Where |
|---|---|---|
| grant_delay | 14 | Benevity 9, Network for Good 5 |
| nonprofit_receipt_attribution | 8 | Benevity 5, Blackbaud 1, regulator items 2 |
| ux_app | 8 | Fidelity Android 3, Benevity Android 3, Benevity web 2 |
| customer_service | 4 | Benevity 2, Blackbaud 1, Ren 1 |
| payment_rail_fees (EFT enrollment, checks) | 3 | Benevity 2, Network for Good 1 |
| grant_rejection_discretion | 3 | Benevity vetting, NfG Nonprofit Hub verification, YourCause redirection |
| account_access | 2 | Benevity 2FA and password reset |
| tax_receipt_documentation | 2 | Benevity, 2022 (one Canadian reviewer) |
| other; transfer_portability | 1 each | Benevity match misstatement; NfG recurring-donor data not exportable |

**Severity:** 27 high, 14 medium, 5 low.

**Complainants:**
- nonprofits (including one volunteer): 27;
- employee or individual donors: 15;
- state AG (via give.org): 2;
- unclear: 2.

### 5.2 Patterns, with record pointers

1. **Processor timing rules generate the delays.** Records:
   - payout deferred because the charity is below a paper-check threshold (CMP-G1913-001);
   - month-end payouts that slip to two or three months (-006, -009, -018);
   - "completed" gifts undelivered for 14 months (-027);
   - Network for Good holds pending compliance or tax issues (-037, -041).

   Benevity's own fee schedule and payment cadence are already in the repo ([queue-processor-economics-vendor-profiles.md](queue-processor-economics-vendor-profiles.md)). The complaints give the nonprofit-side cost of the same design.
2. **Lost checks become months-long cases.** Examples:
   - a check voided at 180 days and not reissued (-002);
   - a 45-day reissue (-043);
   - Blackbaud not reissuing a check for an employer-matched gift (-036).

   These match the corpus's paper-check root cause (corpus §1 item 5).
3. **EFT enrollment is itself a complaint source.** Examples:
   - bank letters rejected as "insufficient" (-007);
   - EFT setup taking more than six weeks (-012);
   - a bank-link tool that did not support the charity's bank, followed by AI-like email loops (-038);
   - verification rejections on Bonterra's Nonprofit Hub (-042).

   Moving everyone to EFT shifts the friction into vetting; it does not remove it.
4. **Donor intent versus processor policy.** YourCause redirected an undeliverable gift to an employer-chosen charity under an internal compliance process (-034). This is the processor-layer version of the sponsor-discretion complaints (SPLC, UNRWA) in corpus §5.3–5.4.
5. **Regulators.** BBB Wise Giving Alliance reports that Alaska sued both For Good and PPGF in March 2026 (Case No. 3AN-26-CI) over charity fundraising pages created without consent (-045, -046). CMP-232 already covers the PPGF part, so -046 is flagged `dup_of=CMP-232`.

---

## 6. Limits

- **Venue presence is the binding constraint.**
  - 12 of the 15 largest sponsors have no profile on any of the three target venues that we could find.
  - Zero counts are "not observed", not "none". The upper bounds in §4.2 would hold only if each sponsor's complainants used these venues, and they do not.
  - The two nationals with the largest review-venue counts (Fidelity Charitable and Daffy) are the two with consumer apps.
- **Discovery limits from robots.txt (respected, not worked around).**
  - BBB search and Trustpilot search are disallowed, so profiles were found only by trying domains or through a search engine.
  - Google Play's review list is disallowed, so only 3 reviews per app could be read, against 29 (Fidelity) and 94 (Benevity) reviews in total.
- **Unequal windows.**
  - BBB shows 3 years; give.org counts 36 months; Trustpilot shows full history; Google Play shows the 3 reviews the page features.
  - All are cut to 2021 or later, but effective coverage differs by venue. Rates are therefore not comparable across venues, only across entities on the same venue mix.
- **Convenience sample and selection.** Benevity's Trustpilot page draws nonprofit reviews invited after webinars (excluded) and nonprofit grievances. Fidelity's app reviews come mostly from donors whose app failed. The share of users who review is unknown and differs by brand (P-G1913-06).
- **Denominator quality.** Two of the five processor account counts are imputed or implausible. Processor accounts are a different unit from sponsor accounts (§4.3). All denominators come from the repo and none were invented.
- **Attribution.**
  - Benevity reviews span its Canadian, UK and other giving funds. The strict scope keeps US reviewers only.
  - Three new records have low attribution (Blackbaud product not named; Ren product not named; Benevity reviewer with no subject). Strict excludes them.
  - One BBB/Trustpilot pair is the same incident and is counted once in strict, but twice in review_venues and all_venues. CMP-G1913-046 and CMP-232 (the same Alaska suit) are likewise counted twice in PPGF all_venues [V wave 32B]
- **Allegations are not findings.** Reviews and BBB complaints are one-sided. Where the business responded (Bonterra), the response is summarized in `resolution`.
- **Earlier rates.** [`complaint-rates-normalised.csv`](../../data/mission-2026-11-14/complaint-rates-normalised.csv) (P-QA3-04) uses the same denominators but a different entity frame and no intervals. Fidelity's all-venue count rises from 47 there to 50 here: the 3 Google Play records.

---

## 7. Source register

| ID | Source | Read | URL |
|---|---|---|---|
| G1 | Trustpilot robots.txt | 2026-11-19 | https://www.trustpilot.com/robots.txt |
| G2 | BBB robots.txt; BBB llms.txt | 2026-11-19 | https://www.bbb.org/robots.txt ; https://www.bbb.org/llms.txt |
| G3 | Google Play robots.txt | 2026-11-19 | https://play.google.com/robots.txt |
| G4 | give.org robots.txt | 2026-11-19 | https://give.org/robots.txt |
| G5 | Trustpilot: Benevity (pp. 1–5) | 2026-11-19 | https://www.trustpilot.com/review/benevity.com |
| G6 | Trustpilot: Blackbaud | 2026-11-19 | https://www.trustpilot.com/review/blackbaud.com |
| G7 | Trustpilot: Network for Good (Bonterra Guided Fundraising) | 2026-11-19 | https://www.trustpilot.com/review/networkforgood.com |
| G8 | Trustpilot: Ren | 2026-11-19 | https://www.trustpilot.com/review/www.reninc.com |
| G9 | Trustpilot: SVCF (0 reviews) | 2026-11-19 | https://www.trustpilot.com/review/siliconvalleycf.org |
| G10 | BBB: Bonterra Tech complaints (p. 1–2) | 2026-11-19 | https://www.bbb.org/us/tx/austin/profile/computer-software/bonterra-tech-0825-1000223687/complaints |
| G11 | BBB: Blackbaud Inc complaints (p. 1–3) | 2026-11-19 | https://www.bbb.org/us/sc/daniel-island/profile/computer-software/blackbaud-inc-0663-34016127/complaints |
| G12 | Google Play: Fidelity Charitable | 2026-11-19 | https://play.google.com/store/apps/details?id=com.fidelity.charitable |
| G13 | Google Play: Benevity | 2026-11-19 | https://play.google.com/store/apps/details?id=org.benevity.app |
| G14 | give.org: For Good (formerly Network for Good) | 2026-11-19 | https://give.org/charity-reviews/other/forgood-in-washington-dc-9999-1290 |
| G15 | give.org: PayPal Charitable Giving Fund | 2026-11-19 | https://give.org/charity-reviews/other/paypal-charitable-giving-fund-in-washington-dc-9999-52179 |
| R1 | DAFRC FY2019–2024 sponsor dataset (repo) | — | data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv |
| R2 | R1 corrections (repo) | — | data/mission-2026-11-14/dafrc-corrections-itemized.csv |
| R3 | FY2024 league table (top-15 frame) | — | data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv |
| R4 | Fidelity 2024 grant count | — | data/mission-2026-11-14/grant-rail-shares-panel-2026.csv |
| R5 | Base corpus and method | — | data/mission-2026-11-14/daf-user-complaints-corpus.csv ; research/mission-2026-11-14/daf-user-complaints-deep-research.md |

Every added record carries its own URL and, for Trustpilot, the review id.

---

## 8. Data dictionary

### 8.1 `daf-user-complaints-corpus-additions-2026-11-19.csv`

The columns and definitions are identical to corpus §11, with these conventions:
- `record_id` is `CMP-G1913-NNN`.
- `access_date` is 2026-11-19.
- BBB complaint pages and Trustpilot use `venue_type` = `review_site`; Google Play uses `app_store`; give.org government-action items use `regulator`.
- `notes` tokens: `country=XX` (Trustpilot reviewer country code), `dup_of=<record_id>` (same incident already recorded). Each row also gives the Trustpilot review id or BBB complaint date, and the AOGF mapping for Benevity rows.

### 8.2 `complaint-rates-2026-11-19.csv`

| Column | Type | Definition |
|---|---|---|
| entity | text | Sponsor or processor (§2.1), or `POOLED <group>` |
| entity_group | enum | `top15_sponsor`, `processor` |
| rank_basis | text | FY2024 rank (assets for sponsors, grants among DAFRC Donation Processors) |
| ein | text | 9-digit EIN |
| fy2024_accounts | integer | FY2024 DAF accounts after R1 corrections (R1, R2) |
| accounts_source | text | `DAFRC FY2024 (<DAFRC source>)` or `R1 filed 990 (replaces DAFRC imputed)` |
| accounts_quality | enum | `filed or paper submission`, `imputed (DAFRC estimate)`, `implausible (not used)` (< 10 accounts); for pooled rows `sum` or `not computed …` |
| fy2024_daf_grants_usd | integer | FY2024 DAF grants after R1 corrections |
| grants_source | text | As for accounts |
| scope | enum | `all_venues`, `review_venues`, `strict` (§2.3), `venue_reported_aggregate` |
| window | text | `2021-01-01..2026-11-19`, or the aggregate's label and source URL |
| window_years | number | 5.881, or the aggregate's own window [V wave 32B]
| n_complaint_mixed | integer | Records in scope with valence complaint or mixed |
| n_high_critical | integer | Of which severity high or critical |
| n_from_additions | integer | Of which `CMP-G1913-*` records |
| rate_per_10k_accounts | number | n / accounts × 10,000 over the window; blank if no usable accounts |
| rate_per_10k_ci95_low / _high | number | Exact Poisson 95% bounds, same scaling |
| annual_rate_per_10k_accounts (+ _ci95_low / _high) | number | The above ÷ window_years |
| rate_per_1bn_grants (+ _ci95_low / _high) | number | n per $1bn of FY2024 DAF grants, with exact Poisson bounds |
| venue_coverage | text | `venue_type` values present among counted records |
| venues_checked_2026_11_19 | text | Trustpilot/BBB/Google Play status for the entity (§3) |
| record_ids | text | Counted record ids, separated by ";" |
| interpretable | text | `no (zero records …)`, `weak (<5 records)`, `weak (imputed account count …)`, `accounts denominator implausible …`, `descriptive only (convenience sample)` |

**Reproduction:** run `python3 scripts/mission_complaint_rates_gap19.py --force`. Inputs are the two corpus files, R1 and R2.
