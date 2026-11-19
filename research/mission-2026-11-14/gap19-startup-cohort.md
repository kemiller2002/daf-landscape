# DAF startup cohort 2021–2026: a denominator for the failed-startup study

**Queue item:** P-GAP19-15. **Prepared:** 2026-11-19. **Status:** desk research from public sources only, with no outreach.
**Dataset:** [`data/mission-2026-11-14/daf-startup-cohort-2021-2026.csv`](../../data/mission-2026-11-14/daf-startup-cohort-2021-2026.csv). It has 36 rows: 18 cohort members (`in_cohort=yes`) and 18 screened-out candidates, each with a reason.
**Script:** [`scripts/mission_gap19_startup_cohort.py`](../../scripts/mission_gap19_startup_cohort.py). It uses only the standard library and is written in functional style. It re-derives Frame A from the DAFRC panel and prints every table in §4–§5.
**Queue proposals:** [`data/mission-2026-11-14/queue-proposals-gap19-15.csv`](../../data/mission-2026-11-14/queue-proposals-gap19-15.csv) (6 rows).
**Builds on:**
- [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md) (the "purposive-50");
- [sponsor-mortality-analysis.md](sponsor-mortality-analysis.md) (the DAFRC entry/exit panel);
- [startups-and-emerging-competitors-2026-11-12.md](../startups-and-emerging-competitors-2026-11-12.md).

---

## 1. Bottom line

1. **The cohort has 18 DAF and DAF-adjacent entities that entered between 2021 and 2026, and none has a documented shutdown.** As of 2026-11-19:
   - 10 are active;
   - 1 was acquired (Causeway, by Charity Navigator, 2023-08-22);
   - 1 pivoted (Uncommon Giving, from a consumer DAF wallet to an employer CSR suite);
   - **6 have unknown status**;
   - 0 are shut.

   Survival, counting a company as surviving if it still operates in any form:

   | Measure | Value |
   |---|---|
   | Among the 12 resolved cases | **12/12 (95% Wilson 75.7–100%)** |
   | Bounds over all 18, depending on how the unknowns resolve | **66.7% (43.7–83.7%) to 100% (82.4–100%)** |

   Exposure is 80.9 company-years with no observed shutdown. That still allows an annual shutdown hazard of up to **3.7%** (rule-of-three 95% bound, which assumes the 6 unknowns are still operating) [V wave 32A]. If every unknown turned out to be a closure, the crude annual rate would be 7.4%.
2. **The filing frame finds no deaths, and with this little exposure it could hardly have found one.** All 10 Frame A sponsors:
   - carry no DAFRC exit flag through FY2024. For 6 of the 10 (Daffy, AnonDo, Grapevine, GoodCoin, Matbia, Manifold) the FY2024 DAFRC row is imputed, not filed, so the ProPublica 2024-12 listing is the FY2024 evidence [V wave 32A];
   - have a tax-period 2024-12 return listed on ProPublica;
   - show no IRS revocation.

   The DAFRC panel's verified central sponsor exit rate is 1.2%/yr. At that rate, 23 sponsor-years would be expected to yield **0.28 exits**, and there is a 76% chance of seeing none even if these entrants were no healthier than the average sponsor. Zero observed exits is therefore *not* evidence that new sponsors outlive established ones.
3. **The purposive-50's failure mix does not describe the 2021–2026 generation.**
   - The purposive-50 recorded 17 adverse outcomes (11 voluntary shutdowns, 6 regulatory or insolvency events) and 12 acquisitions.
   - In `failed-daf-startups.csv`, only one of these 29 has a founding year of 2021 or later (FTX Future Fund, 2022). Thirteen have an unknown founding year, and the other 15 predate 2021 [V wave 32A]. Many are payments intermediaries or corporate-owned giving products.
   - The cohort, defined in advance, contains none of those failure types. Its weak points are **quiet fade**: a third of members are status-unknown small sponsors with no dated activity in the last year. The cohort also shows **channel pivots**.
4. **Acquisition is not the modal exit here.** It is 1 of 18 (5.6%, 95% CI 1.0–25.8%), against 12 of 50 in the purposive list. The one buyer was a nonprofit rater, not a DAF consolidator. The purposive-50's "consolidators buy the plumbing" pattern (P2) comes from deals made in 2016–2025 with older targets (Pinkaloo, Amicus, iPhi, Vennfi, Giving Place). None of those targets is in this cohort.
5. **The profiles differ, but n is too small to show cause.**
   - 7 of the 9 venture- or angel-backed members are active. The other two are one pivot (Uncommon Giving) and one unknown (Givepact).
   - Of the 7 members with no funding found, 5 are not active: 4 unknown and 1 acquired.
   - B2B members are more often active than B2C or community members (6/8 vs 4/8).
   - These differences are within sampling noise at n=18. They also partly reflect a measurement effect: funded B2B firms publish more dated news, so they meet the "active" evidence rule more easily (§6).

---

## 2. Method

### 2.1 Pre-registered inclusion rules

The rules below were written to the scratchpad at 17:11 UTC on 2026-11-19, before any outcome was looked up. They are reproduced here verbatim in substance.

- **Window.** The DAF-holding or DAF-operating unit's first observable entry event falls between 2021-01-01 and 2026-11-19. Entry events are a public launch, an incorporation, an IRS ruling or a first public funding round.
- **Unit of analysis.** Where a 501(c)(3) sponsor exists solely for the product, the unit is that sponsor EIN, and its IRS ruling date counts as entry. Otherwise the unit is the company. One consequence: companies older than 2021 that created a dedicated sponsor in the window are included, for example GivingTrax (2010) and in/PACT (2015). Uncommon Giving does not pass the window test. Its sponsor (84-3815117) has a FY2020 DAFRC row with 266 DAF accounts, and the product launched publicly on 2020-07-28. Its first observable entry event therefore predates the window, as Endaoment's does. It is in only because its ruling month reads 2021-01. Without it the cohort is 17 (active 10, acquired 1, pivoted 0, unknown 6), and the lower bound is 11/17 = 64.7% (41.3–82.7%) [V wave 32A] The **strict subset** (`strict_window_subset=yes`, n=8) keeps only companies founded in the window and is reported separately.
- **Product definition.** One of:
  - (i) a DAF or giving account sold to the public;
  - (ii) software, payments or an API built for DAFs or giving accounts;
  - (iii) a DAF-like giving account embedded in a fintech, employer or consumer product.
- **Exclusions.**
  - Subsidiaries or products of incumbents founded before 2021 (bank DAF programs, GoFundMe Giving Funds, Altruist DAFs, Telescope Fund). The rules do not define \"incumbent\". Telescope Fund (a dedicated sponsor ruled in 2023 inside an older network) is excluded, while dedicated in-window sponsors of older companies (GivingTrax, GoodCoin, Goodstack) are included. The strict subset is the only reading free of this choice [V wave 32A].
  - Community foundations and single-issue charities.
  - Fundraising SaaS with no giving-account feature.
  - Non-US entities that do not run a US sponsor.
- **Outcome classes.** `active`, `acquired`, `pivoted`, `shut`, `unknown`.
  - **`active` requires dated evidence no more than 12 months old** (on or after 2025-11-19). A copyright year of 2026 counts, and is labelled `weak`.
  - A live but undated site is `unknown`.
  - `pivoted` requires dated evidence of a change of core customer or product.
- **Evidence tiers.** (1) filing or regulator; (2) company or acquirer statement; (3) trade press; (4) live site or app-store check.

### 2.2 Frames

| Frame | Source | Rule | Hits | In cohort |
|---|---|---|---|---|
| A: filing | `sponsor-entry-exit-panel.csv` (DAFRC FY2019–FY2024, 1,594 EINs) | IRS ruling ≥ 2021-01 **and** (type National **or** subtype Other with ≥50 filed DAF accounts) | 11 | 10 (Telescope Fund screened out as an NVF-network subsidiary) |
| B: announcements | repo CSVs (`emerging-entrants-funding-ai.csv`; rows of `failed-daf-startups.csv` founded 2021 or later); ten fixed web queries (Q1–Q10: DAF startup raises 2021…2026, YC directory, app launches, crypto DAFs, workplace giving); YC public pages | product and window rules | — | 10 (3 overlap with A) |
| C: app store | Apple App Store listing pages found by web search restricted to apps.apple.com | product and window rules | — | 5 (4 overlap with A or B) |

The union is **18 members**. Frame A is mechanical and the script re-checks it: `Frame A consistency: OK`, meaning every rule hit is either in the cohort or screened out with a reason. Frames B and C depend on what search engines and press releases surface.

### 2.3 Robots.txt and access

- **Y Combinator** disallows `/companies?*`. Only allowed paths were read: `/companies/industry/Nonprofit` and the individual company pages `/companies/chariot-2` and `/companies/charityvest`.
- **Apple.** `itunes.apple.com/search*` and `/*/lookup?` are disallowed, so the iTunes Search and Lookup APIs were **not** used. Individual listing pages `apps.apple.com/us/app/id…` are allowed and were fetched; they were found through web search.
- **Google Play.** `/store/apps/details` is allowed, but no package IDs were found for cohort members, so Play was not checked.
- **ProPublica.** The Nonprofit Explorer API (`/nonprofits/api/v2/organizations/{EIN}.json`) is allowed. The name-search paths are disallowed and were not used.
- **Not used:** crt.sh and certspotter.
- **No outreach** of any kind.

### 2.4 State charity registries (attempted, not achieved)

- **California.** The AG's Registry Search Tool is linked from oag.ca.gov/charities at `rct.doj.ca.gov/Verification/Web/Search.aspx?facility=Y`. It returned HTTP 404 to scripted requests on 2026-11-19.
- **New York.** The Charities Bureau site returned HTTP 500 (robots.txt) and a 302 on its search page.

No state-registry lapse evidence is therefore in this file. IRS status from ProPublica (revocation date, latest return period) is used in its place. Queue P-GAP19-15-03 carries the manual check.

---

## 3. Cohort table (summary)

| ID | Entity | Frames | Category | Channel | Entry | Status | Status date | Evidence |
|---|---|---|---|---|---|---|---|---|
| SC01 | Daffy | A, B, C | core_daf_sponsor | B2C (+employer) | 2021-05 ruling; 2021-09-30 launch | active | 2026-09-30 | strong |
| SC02 | Groundswell | B, C | core_daf_sponsor | B2B employer | 2021-08 ruling; 2021-11-23 Form D | active | 2026-09-28 | moderate |
| SC03 | Chariot (DAFpay) | B, C | daf_payments_infrastructure | B2B nonprofits/platforms | 2022 (YC S2022) | active | 2026-01-28 | strong |
| SC04 | Causeway | B | daf_like_account | B2C | 2022 test launch | **acquired** | 2023-08-22 | strong |
| SC05 | Infinite Giving | B | daf_adjacent | B2B nonprofits | 2021-06 pre-seed | active | 2026-11-16 | moderate |
| SC06 | Daffodil | B | core_daf_sponsor | B2B2C | 2024 founded; 2025-06-18 launch | active | 2026 (©) | weak |
| SC07 | Givepact | B | daf_adjacent (crypto + DAF) | B2C | 2022 | **unknown** | — | weak |
| SC08 | Goodstack Impact Foundation US | B | daf_adjacent (pass-through) | B2B corporate | 2022-11 ruling | active | TY2025 990 | moderate |
| SC09 | Uncommon Giving | A, C | core_daf_sponsor | B2C, then B2B employer | 2021-01 ruling | **pivoted** | 2026-11-14 | moderate |
| SC10 | Silent Donor (AnonDo Fund) | A | daf_like_account | B2C | 2022-04 ruling | **unknown** | — | weak |
| SC11 | DonateStock / GivingIQ | A, B | daf_adjacent | B2B nonprofits | 2021-12 ruling | active | 2026-04-30 | moderate |
| SC12 | Grapevine | A, B | daf_like_account (giving circles) | B2C collective | 2022-07 ruling | active | 2026-06 | moderate |
| SC13 | Abundance Capital | A | core_daf_sponsor (impact investing) | B2C + CF partner | 2021-12 ruling | active | 2026 (©) | weak |
| SC14 | GoodCoin (in/PACT) | A | core_daf_sponsor (bank white-label) | B2B banks | 2022-06 ruling | **unknown** | — | weak |
| SC15 | Matbia | A | daf_like_account (tzedakah card) | B2C community | 2022 launch | active | 2026 (©) | weak |
| SC16 | Manifold for Charity | A | daf_adjacent | embedded in consumer app | 2022-10 ruling | **unknown** | — | weak |
| SC17 | GivingTrax Foundation | A | daf_adjacent (workplace pass-through) | B2B employer | 2023-07 ruling | **unknown** | — | weak |
| SC18 | iMaaser | C | core_daf_sponsor | B2C community | 2022-03 ruling | **unknown** | — | weak |

Per-row evidence, URLs and notes are in the CSV.

**Screened out (18 rows in the CSV).**

*Entry before the window:*
- Endaoment (ruled 2020-05)
- Charityvest/Vennfi (sponsor ruled 2016; YC S2020, which YC now lists as "Acquired")
- Philanthropi (2018)
- Amicus.io (2017)
- Givinga (2015)
- Every.org (returns from tax period 2018-12)
- GiveClear/TIFIN Give (2016/2018)
- World Giving Foundation, Commonwealth Impact Foundation and Crewe Endowment Foundation (ruled 2020)

*Products of incumbents:*
- GoFundMe Giving Funds
- Altruist DAFs
- The Donors Fund app
- Telescope Fund

*Outside the product definition:*
- Grateful Giving
- YourChange
- Givefront
- Givz
- SpareChange (entity unresolved)

*Below the Frame A account threshold:*
- Possibility Labs
- Our Change Foundation

---

## 4. Survival analysis

### 4.1 Full cohort (n=18)

| Measure | Value |
|---|---|
| Status counts | active 10, acquired 1, pivoted 1, shut 0, unknown 6 |
| Not shut, among resolved (excludes unknown) | 12/12 = 100.0% (95% Wilson 75.7%–100.0%) |
| Operating in any form, unknown counted as failed (lower bound) | 12/18 = 66.7% (43.7%–83.7%) |
| Operating in any form, unknown counted as surviving (upper bound) | 18/18 = 100.0% (82.4%–100.0%) |
| Independent and operating (active + pivoted) | 11/18 = 61.1% (38.6%–79.7%) |
| Active with dated evidence ≤12 months | 10/18 = 55.6% (33.7%–75.4%) |
| Exit by acquisition | 1/18 = 5.6% (1.0%–25.8%) |
| Status unknown | 6/18 = 33.3% (16.3%–56.3%) |
| Company-years of exposure (entry to 2026-11-19) | 80.9 (median age 4.4 years, exactly 4.375; range 2.3–5.8) [V wave 32A] |
| Rule-of-three 95% upper bound on the annual shutdown hazard | 3.7% |
| Crude annual shutdown rate if every unknown were a shutdown | 7.4% |

### 4.2 Strict subset: companies founded in 2021 or later (n=8)

| Measure | Value |
|---|---|
| Status counts | active 5, acquired 1, pivoted 0, shut 0, unknown 2 |
| Not shut, among resolved | 6/6 = 100.0% (61.0%–100.0%) |
| Operating in any form, lower to upper bound | 75.0% (40.9%–92.9%) to 100.0% (67.6%–100.0%) |
| Exit by acquisition | 1/8 = 12.5% (2.2%–47.1%) |
| Company-years; rule-of-three hazard bound | 34.5; 8.7% |

### 4.3 Filing survival (Frame A, n=10) against the DAFRC base rate

| Measure | Value |
|---|---|
| No DAFRC exit flag through FY2024 | 10/10 (72.2%–100.0%) |
| Tax-period 2024-12 return listed on ProPublica; no revocation | 10/10 (72.2%–100.0%) |
| Sponsor-years at risk, entry year to FY2024 | 23 |
| Expected exits at the verified lower rate (0.19%/yr, "organisation ceased") | 0.04 (P(0) = 0.96) |
| Expected exits at the verified central rate (1.20%/yr) | 0.28 (P(0) = 0.76) |
| Expected exits at the verified upper rate (1.48%/yr) | 0.34 (P(0) = 0.71) |
| Observed exits | 0 |

The verified rates come from `sponsor-mortality-summary.csv` (`verified` rows; see [sponsor-mortality-analysis.md](sponsor-mortality-analysis.md) §1).

**Reading.** The filing frame is right-censored at FY2024 and has little exposure. A sponsor that stopped operating in 2025 would not show as a DAFRC exit until a later panel. It would not show as an IRS auto-revocation until three missed annual filings, around 2028. Filing survival therefore says only that no cohort sponsor had **formally** ended by the end of 2024.

---

## 5. Failure causes: non-active cases against survivors

There are no shutdowns in the cohort, so the comparison is between the 8 members that are not active and the 10 that are.

| Case | Outcome | Mechanism, from evidence | Purposive-50 pattern it matches |
|---|---|---|---|
| Causeway | acquired 2023-08-22 | E: launched in 2022 as a test with about 100 donors; acquirer took IP, brand and other assets and relaunched the product in 2024-09. I: sub-scale consumer product with a soft landing at a mission-aligned nonprofit buyer | P2 (acquisition as exit), but the buyer is a rater, not a DAF consolidator |
| Uncommon Giving | pivoted | E: the 2020 release offered "Anyone can open an Uncommon Giving Wallet, a DAF, with as little as $10". In 2026 the product is an employer CSR suite (grants management from $2,400/yr; employee giving and volunteering from $5,000/yr) [V wave 32A]. Schedule D accounts fell from 306 (FY2022) to 1 (FY2023–FY2024). I: consumer customer acquisition did not pay; the company moved to employer sales | P3/§1.6 channel pivot (consumer to employer), as with Pinkaloo, Philanthropi and Bright Funds |
| Manifold for Charity | unknown | E (forum and wiki sources): a $10k monthly donation cap from 2024-01; only prize points redeemable from 2024-05; Sweepcash sunset 2025-03-28; the program was originally grant-funded. I: a giving feature inside a parent app depends on the parent's funding and regulatory choices | §1.5 corporate-owned products die when the parent reprioritizes; P3 borrowed channel |
| Givepact, Silent Donor, GoodCoin, GivingTrax, iMaaser | unknown | E: each has a TY2024 return or a live site or listing, but no dated activity on or after 2025-11-19. All are small: AnonDo Fund DAF assets $17,982 (FY2023, DAFRC); I Maaser total assets $319 (TY2022); GivingTrax Foundation total assets $78,774 (latest ProPublica filing with data). None has disclosed venture funding except Givepact (Outlier Ventures) | Visibility bias (§8 of the purposive-50): quiet closures leave no press trace |

**Survivors (10 active)** share three traits, all descriptive with n too small for inference:
- **Funding and dated output.** 7 of the 10 have disclosed venture, angel or Series A funding: Daffy, Groundswell, Chariot, Infinite Giving, Daffodil, Goodstack and Grapevine. They also publish frequent dated updates.
- **Distribution.** 6 of the 10 sell B2B or have institutional distribution: Groundswell (employers), Chariot (fundraising platforms), Infinite Giving and GivingIQ (nonprofits), Goodstack (corporates) and Daffodil (advisors and nonprofits).
- **Custody.** Every member that holds donor money does so through a dedicated 501(c)(3) sponsor. No member reported missing or unremitted donor funds. This does not test P1 (payments and custody as the loss layer), because the cohort's exposure is short and none of its members is a payments intermediary that holds funds in its own name.

**Not supported.** The cohort gives no evidence on fee-model failure (P4), crypto cyclicality (P6; Endaoment falls outside the window, and Givepact's status is unknown) or governance failure (P7). SDG Impact Fund, the only 2020s core-sponsor enforcement case, entered before 2021 (reported as a $117k charity in 2017), so it is outside the window.

---

## 6. Comparison with the purposive-50 findings

| Purposive-50 finding | What the cohort shows | Status |
|---|---|---|
| §1.1 Core DAF entities rarely fail visibly | 0 of 10 sponsors exited the filing frame; 0 of 18 cohort members shut | **Consistent, weakly.** The bound allows up to 3.7%/yr |
| §1.2/P2 Acquisition by a consolidator is the modal DAF-tech exit | 1 of 18 acquisitions, by a nonprofit rater | **Not reproduced** in the 2021–2026 generation. P2 describes older targets |
| §1.3/P1 Money is lost in the payments and custody layer | No loss events. Members use dedicated sponsors; Chariot routes grants and does not hold DAF assets | **Untested.** No payments-custody member failed, and exposure is short |
| §1.5 Corporate-owned giving products die on reprioritization | Manifold's charity program contracted with parent decisions | **Consistent**, with one weak case |
| §1.6/P3 Channel pivot, not death | Uncommon Giving moved from consumer to employer; Daffodil's homepage now addresses organizations [I] | **Consistent.** This is the most visible non-death outcome |
| §8 "Denominator absent" | 18-member cohort; unknowns are 33% | Denominator supplied, but wide: survival is 66.7–100% |

**How to read the two studies together.**
- The purposive-50 is a *catalogue of mechanisms*. Most of its cases are older, and many are payments intermediaries or corporate products.
- This cohort is a *rate frame* for the entities a 2026 entrant actually competes with.
- Survival to about 4 years looks high, and visible failure is rare. Whether the dominant failure mode turns out to be quiet fade among small, unfunded sponsors depends on how the 6 unknowns resolve (P-GAP19-15-02).

---

## 7. Sources of bias and limits

1. **Frame coverage.**
   - DAFRC misses some in-window DAF holders: Groundswell Charitable Foundation, Goodstack Impact Foundation US and I Maaser Inc all file returns but are absent from the panel. Frame A therefore undercounts entrants that report through 990-EZ/990-N or that DAFRC did not process (P-GAP19-15-01).
   - The panel ends at FY2024, so sponsors ruled in 2024–2026 cannot enter Frame A (for example, Daffodil Charitable).
2. **Discovery bias (survivorship).**
   - Frames B and C reach entities through search engines and press releases. Funded, surviving companies are over-represented.
   - Firms that died before generating press, and apps already delisted, are invisible: search returns only live listings, and the robots-compliant method cannot enumerate removed App Store IDs (P-GAP19-15-04).
   - The cohort is a census of *visible* entrants, not of all entrants.
3. **Right-censoring.** The median age is 4.4 years (4.375) and the maximum 5.8 [V wave 32A]. Venture-backed startups commonly fail later than that. The rule-of-three bound (3.7%/yr; 8.7%/yr for the strict subset) is the honest summary.
4. **Detection lag.** Closures surface in filings with a lag of one to three years: a final return or Schedule N, or auto-revocation after three missed returns. A 2025–2026 closure would currently appear as `unknown`, which is why unknown is never counted as surviving in the lower bound.
5. **Classification from weak signals.** Four "active" calls (Daffodil, Abundance Capital, Matbia, and Grapevine via search extracts) rest on copyright years, upload paths or search snippets. `evidence_strength` flags these. Under a stricter "active" rule, the active count falls to 6, and the 4 move to unknown.
6. **Unit-of-analysis choice.** Counting a dedicated sponsor's IRS ruling as entry admits older parent companies. The strict subset (n=8) removes them, and its rates are similar.
7. **Small n.** With 18 members, every subgroup difference is within sampling noise, and the Wilson intervals are wide.
8. **No state registries, Crunchbase, PitchBook or Wayback content** (§2.4). Funding figures come from press releases, Form D filings or aggregators, as labelled.
9. **Single analyst; no blind second coder.** Pivot and adjacent-product calls are marked [I] where they are inference.

---

## 8. Data dictionary: `data/mission-2026-11-14/daf-startup-cohort-2021-2026.csv`

| Column | Meaning |
|---|---|
| `cohort_id` | SC01–SC18 for members; SX01–SX18 for screened-out candidates |
| `in_cohort` | `yes` = meets the pre-registered rules; `no` = screened out |
| `exclusion_reason` | Rule failed (screened-out rows only) |
| `entity_name` | Product or company name as marketed |
| `daf_entity_legal_name` | Legal name of the sponsor or operating company that holds or routes DAF money |
| `ein` | Sponsor EIN where one exists (blank for for-profit-only units). Multiple EINs are separated by `;` |
| `frames` | A (DAFRC filing frame), B (announcements), C (app store); `;`-separated |
| `frame_source` | The specific source row, query or listing through which the entity entered |
| `product_category` | `core_daf_sponsor`, `daf_payments_infrastructure`, `daf_like_account`, `daf_adjacent` (with a qualifier in parentheses) |
| `channel` | Primary distribution channel |
| `entry_event` | Event used as entry (ruling, launch, founding, first funding) |
| `entry_date` | Date or dates of the entry event(s). The script uses the first year and month, or mid-year if the month is unknown |
| `parent_founded_pre2021` | Whether the parent company predates 2021 (`yes`/`no`/`unknown`, with a note) |
| `strict_window_subset` | `yes` if the company itself was founded or launched in the window |
| `funding_evidence` | Disclosed funding, with source type |
| `venture_backed` | `yes` / `no` / `unknown` (angel counts as yes and is noted) |
| `status` | `active` / `acquired` / `pivoted` / `shut` / `unknown`, as of 2026-11-19 |
| `status_date` | Date of the evidence supporting the status |
| `status_evidence` | Short factual statement of the evidence |
| `status_evidence_url` | URLs, `;`-separated |
| `evidence_tier` | 1 filing or regulator; 2 company or acquirer; 3 trade press or forum; 4 live site or app check (`;`-separated) |
| `evidence_strength` | `strong` / `moderate` / `weak` (weak = copyright year, upload path, search extract or undated page) |
| `last_990_period_propublica` | Latest tax period listed by the ProPublica API on 2026-11-19 |
| `in_dafrc_panel` | Whether the sponsor EIN appears in `sponsor-entry-exit-panel.csv` |
| `dafrc_exit_flag` | `none` if no `sponsor_exit_kind`; `n/a` if not in the panel |
| `app_store_id` | Apple App Store numeric ID, where checked |
| `app_listing_last_dated_item` | Latest `<time datetime>` on the listing page (version or review date), fetched 2026-11-19 |
| `notes` | Caveats; [I] marks analyst inference |

---

## 9. Source register

**Repository sources**
- `data/mission-2026-11-14/sponsor-entry-exit-panel.csv`, `sponsor-mortality-summary.csv` and `sponsor-exit-verification.csv` (from the [DAFRC 2025 dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx) and IRS files)
- `data/mission-2026-11-14/failed-daf-startups.csv`, `emerging-entrants-funding-ai.csv` and `pass-through-sponsors-2026.csv`
- `research/startups-and-emerging-competitors-2026-11-12.md`

**Filings and registries**
- ProPublica Nonprofit Explorer API, read 2026-11-19, for EINs 84-3815117, 86-3177440, 87-0879423, 87-1569770, 87-2389502, 87-2850443, 87-3265356, 87-3609845, 88-3668801, 92-1501329, 87-1530516, 87-3165286, 87-2258154, 86-2577635, 81-2771871, 84-4661797, 81-3222963 and 61-1913297: `https://projects.propublica.org/nonprofits/api/v2/organizations/{EIN}.json`
- Groundswell Form D: https://www.sec.gov/Archives/edgar/data/1899820/000189982021000001/primary_doc.xml
- Chariot Form D: https://www.sec.gov/Archives/edgar/data/2021660/000202166024000001/primary_doc.xml
- Goodstack Impact Foundation US TY2025 990 XML: https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml

**Accelerator and app directories**
- YC: https://www.ycombinator.com/companies/industry/Nonprofit ; https://www.ycombinator.com/companies/chariot-2 ; https://www.ycombinator.com/companies/charityvest
- App Store: https://apps.apple.com/us/app/daffy-save-invest-give/id1578035540 ; https://apps.apple.com/us/app/groundswell-giving-charity/id1597818417 ; https://apps.apple.com/us/app/uncommon-giving/id1612496578 ; https://apps.apple.com/us/app/dafpay/id6633440388 ; https://apps.apple.com/us/app/imaaser/id6572323213 ; also screened: id6471892001, id1626299652, id6794676186

**Company and press pages**
- Daffy $2B (2026-09-30): https://www.morningstar.com/news/business-wire/20260930616360/daffy-surpasses-2-billion-in-charitable-assets-5-years-after-launch
- Chariot gift processing: https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits
- Causeway (AP, 2023-08-23): https://www.clickondetroit.com/business/2023/08/23/causeway-part-stock-fund-part-donor-advised-fund-a-new-bid-for-young-donors/ ; Charity Navigator relaunch: https://prnewswire.com/news-releases/charity-navigator-launches-causeway---ahead-of-giving-season-2024-302246077.html
- Infinite Giving: https://www.infinitegiving.com/ ; https://infinitegiving.com/blog/infinite-giving-seed-round-announcement
- Daffodil: https://www.getdaffodil.com/ ; https://aijourn.com/fintech-platform-daffodil-accelerates-philanthropic-giving/ (2025-06-18)
- Givepact: https://givepact.io/ ; https://partners.circle.com/partner/givepact ; https://outlierventures.io/portfolio/givepact/
- Goodstack Series A: https://tech.eu/2024/11/18/goodstack-secures-28m-from-general-catalyst/
- Uncommon Giving: https://rss.globenewswire.com/news-release/2020/07/28/2068923/0/en/UNCOMMON-GIVING-CORPORATION-COMPLETES-13-5M-FOUNDERS-ROUND-TO-LAUNCH-DIGITAL-GIVING-PLATFORM.html ; https://uncommongiving.com/
- Silent Donor (Chronicle, 2024-02): https://www.philanthropy.com/news/silent-donor-platform-offers-anonymous-donations-to-the-mainstream-as-privacy-debate-rages/
- GivingIQ: https://givingiq.com/press/announce ; https://www.nonprofitpro.com/article/donatestock-rebrands-as-givingiq-expanding-options-for-non-cash-giving/
- Grapevine: https://www.grapevine.org/blog/grapevine-fidelity-grant-matching-campaigns/ ; https://www.businesswire.com/news/home/20230808466348/en/
- Abundance Capital: https://abundancecap.org/ ; https://scbiz.com/abundance-capital-kate-dabbs-chief-community-officer/
- GoodCoin Giving Fund: https://inpactsupport.groovehq.com/help/about-goodcoin-giving-fund
- Matbia: https://matbia.org/ ; https://www.jns.org/new-charity-card-is-upgrading-the-giving-experience-in-jewish-circles/
- Manifold charity program: https://forum.effectivealtruism.org/posts/ioHakR62Jbdgy4ig4/manifold-markets-charity-program-ending-march-1st ; https://www.longtermwiki.com/wiki/E546
- GivingTrax: https://workplacegiving.givingtuesday.org/vendor/givingtrax/

**Access logs (robots.txt, read 2026-11-19)**
- https://www.ycombinator.com/robots.txt
- https://itunes.apple.com/robots.txt
- https://apps.apple.com/robots.txt
- https://play.google.com/robots.txt
- https://projects.propublica.org/robots.txt
- https://oag.ca.gov/robots.txt
