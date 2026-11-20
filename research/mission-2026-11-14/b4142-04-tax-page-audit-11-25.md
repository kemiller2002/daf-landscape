# OBBBA tax-page audit, part 2: sponsors ranked 11–25 and the Fidelity Charitable tools page (P-B4142-04)

**Prepared 2026-11-20. Desk research only. NOT TAX OR LEGAL ADVICE.** No one was contacted. Nothing was logged into, and no form was submitted. Nothing was committed. Errors found on sponsor pages are recorded here only as findings. No sponsor was told about them.

**Builds on:** [b41n16-b42n20-daf-tax-guidance.md](b41n16-b42n20-daf-tax-guidance.md), which covers the top 10. Its method (§1.5), its statute check (§4) and its list of errors (§5.4) are reused here. The H1–H4 profiles and the 2026 parameters come from [direction-donor-tax-scenarios-2026.md](direction-donor-tax-scenarios-2026.md), [`donor-tax-parameters-2026.csv`](../../data/mission-2026-11-14/donor-tax-parameters-2026.csv) and [`donor-tax-scenarios-2026.csv`](../../data/mission-2026-11-14/donor-tax-scenarios-2026.csv). The corporate floor follows [b41n18-02-corporate-floor-pull-forward.md](b41n18-02-corporate-floor-pull-forward.md) §1.

**Labels.**
- **[F]** page read in full this pass.
- **[C]** computed by the script.
- **[R]** not read because robots.txt did not return 200 or 404.
- **[U]** nothing found, or not requested for a stated reason.
- **[I]** interpretation.

**Files written**
- This note.
- [`data/mission-2026-11-14/tax-page-audit-11-25-2026-11-20.csv`](../../data/mission-2026-11-14/tax-page-audit-11-25-2026-11-20.csv): 58 rows. There are 42 classified findings: 8 calculator × profile rows, 19 worked examples and 15 statements. It also has 1 calculator that could not be ported and 15 coverage rows (ranks 11–25).
- [`scripts/mission_tax_page_audit_11_25.py`](../../scripts/mission_tax_page_audit_11_25.py): stdlib only, pure functions. It ports both Fidelity calculators and runs H1–H4 through them. It recomputes every worked example, using the repo engine `mission_tax_scenarios.py` where an example needs the full engine, and builds the CSV.
  - Run `python3 -I scripts/mission_tax_page_audit_11_25.py .` to print the JSON report.
  - Add `--write` to rewrite the CSV.
- [`data/mission-2026-11-14/queue-proposals-b4142-04.csv`](../../data/mission-2026-11-14/queue-proposals-b4142-04.csv): 6 proposals.

---

## 0. Answers in brief

| Question | Finding | Label |
|---|---|---|
| **Fidelity Charitable "Tools and calculators": which tools compute tax?** | **Two tools compute tax:** the Charitable Giving Tax Savings Calculator and the Appreciated Assets Donation Calculator. The Pool Selector and the DAF quiz do not compute tax. | F |
| **Do the Fidelity calculators apply the 2026 law?** | **No.** Neither models the 0.5% floor, the 35% cap or §170(p), and **both pages say so** in their disclosures. The served JS confirms it:<br>– The tax calculator's savings figure is (contribution + other itemized − $32,200) × the selected rate.<br>– The securities calculator's figure is FMV × rate.<br>So the formulas are pre-OBBBA, and the disclosure is accurate. | F, C |
| **Fidelity tax calculator against the repo, H1–H4** | – **H1:** shows no saving. It never mentions that a direct cash gift would save $720 over 3 years under §170(p).<br>– **H2:** says $672 "this year". The repo's DAF figure is $312 a year ($936 over 3 years).<br>– **H2 bunched over 3 years:** $5,472 against the repo's $5,112 (+7.0%).<br>– **H3:** $21,386 against $17,836 (+19.9%).<br>– **H4:** $372,886 against $220,234 (+69.3%). | C |
| **Fidelity securities calculator against the repo** | The "extra" saving from giving stock in kind:<br>– **H1:** $806 against $0. The calculator offers no 0% capital-gains option, and H1's gains fall in the 0% band.<br>– **H2:** $4,464 against $4,541 (−1.7%).<br>– **H3:** $32,880 against $28,770 (+14.3%).<br>– **H4:** $219,200 against $191,157 (+14.7%). | C |
| **One outdated statement on a Fidelity results page** | r4.html says: "Charitable contributions can only reduce your tax bill if you choose to itemize your taxes." That has been false for direct cash gifts since 2026. It is still true for DAF contributions. | F |
| **Coverage of ranks 11–25** ($34.17bn of FY2024 DAF assets) | **9 of 15 sponsors were read** ($21.41bn), and 7 of them have 2026 OBBBA text.<br>– **[R], robots.txt 403 (3, $7.72bn):** CCT, Raymond James Charitable, US Charitable Gift Trust.<br>– **[U] (3, $5.03bn):** FFTC (not requested because of its site terms), NYCT (no OBBBA page found) and Ayco (no website found). | F/R/U |
| **Do the 11–25 pages state the four rules?** | Among the sponsors with OBBBA text (BofA, ImpactAssets, JCF, GKCCF, Greater Horizons, Columbus, DonorsTrust):<br>– **0.5% floor:** stated by all 7, with figures by 6 (DonorsTrust gives no figures).<br>– **35% cap:** stated by 5, though JCF misstates it as "35% of AGI". BofA describes it only as a "haircut" and, in a footnote, as a 2/37 reduction.<br>– **Non-itemizer deduction with the DAF exclusion:** stated by 5. BofA omits the DAF exclusion.<br>– **Corporate 1% floor:** stated by BofA, GKCCF and Greater Horizons correctly, and by Columbus and JCF with threshold wording that can be read as a cliff. | F |
| **Classified findings (42)** | **18 correct, 13 outdated (pre-OBBBA), 1 arithmetic error, 10 ambiguous.**<br>– **The arithmetic error:** BofA's footnote gives a "0.05% AGI floor"; the statute's rate is 0.5%.<br>– **Two ambiguous rows are wrong statements of law:** JCF's "35% of AGI", and the BofA business-sale example, which cannot be reproduced from its stated inputs (see §5). | C |

---

## 1. Method

### 1.1 Targets
- **Sponsors:** FY2024 `top50` rows of [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv), ranked 11–25 by `daf_assets_eoy`. The script re-derives this list (`league_11_25()`).
- **Fidelity Charitable "Tools and calculators":** https://www.fidelitycharitable.org/tools.html and every tax tool linked from it.

### 1.2 Access and discovery
- **robots.txt first.** For every host, robots.txt was fetched and parsed for `*`, `research-script/1.0`, ClaudeBot, Claude-User and anthropic-ai.
  - A page was fetched only if all five agents were allowed.
  - A 404 counted as no rules. Any other status meant the host was not fetched.
  - The fetcher was stdlib and curl, functional, with the generic user agent `research-script/1.0`. On a non-200 response it retried once with Python's stdlib client and the same user agent.
  - It made 72 logged requests to 21 hosts. Sub-sitemaps were fetched under the same check but not logged one by one. The per-request log is in the session scratchpad, not in the repo.
- **Excluded hosts.**
  - dafgiving360.org: skipped, per the task rule.
  - fftc.org: not requested, because the repo records that its site terms bar robots ([queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md)).
  - No crt.sh, certspotter, sec.gov or congress.gov.
- **Discovery.** Sitemaps came first, matched on tax, OBBB, bunch, calcul, 2026, law or deduct. Web search was used only to find URLs.
- **Not bypassed.** One www.donorstrust.org page served a JavaScript verification challenge, so it was not read. The Gift Illustrator calculator computes on the server, so running it would have meant submitting a form. It was not run.

### 1.3 Ports and runs
- **Ports.** Both Fidelity calculators were ported line by line from the served bundle `clientlib-site.lc-5e5c8d29…-lc.min.js` (functions `C()`, `T()` and the securities `addListener()`). The constants come from the calculator page: the hidden `std-married` value is 32200, and the rate menus are 10–37% for income and 15%/20% for capital gains.
- **H1–H4 inputs.**
  - These are the repo's `PROFILES`.
  - The rate a user would select is 12%, 24%, 37% or 37% [I]. For H4, 37% is the top bracket that applies to its taxable income, although its gift mostly offsets gains taxed at 20%.
  - The capital-gains rates are 15%, 15%, 20% and 20%, because the menu has no 0% option.
- **Comparator.** The repo's statute results (`donor-tax-scenarios-2026.csv`) were used for every profile. Where a calculator figure measures the value of all itemized deductions above the standard deduction (H3 and H4, results page r4), the script computes the same quantity with the repo engine (`statute_value_itemized_vs_std`).

### 1.4 Classification
Every finding gets exactly one of the four required classes:
- **correct;**
- **outdated (pre-OBBBA):** the formula or statement matches pre-2026 law;
- **arithmetic error:** a wrong number on the page, whether a computation or a stated parameter;
- **ambiguous:** wording or inputs that allow a wrong reading, or figures that cannot be reproduced from what the page states.

Because the scheme has no class for a wrong statement of law that is not arithmetic, such rows are filed as `ambiguous` with an `error_kind` (P-B414204-03).

---

## 2. Coverage, ranks 11–25

| Rank | Sponsor (FY24 DAF assets $bn) | Status | 2026 page(s) read |
|---|---|---|---|
| 11 | Bank of America Charitable Gift Fund (4.73) | F (affiliate) | BofA Private Bank, which administers the fund: business-owner video (2026-07-21) and OBBBA summary video (July 2025). bofa.donorfirst.org has no tax page. |
| 12 | Chicago Community Trust (4.65) | **R** | robots.txt 403 |
| 13 | ImpactAssets (2.90) | F | "What the OBBBA means for 2026 charitable giving" |
| 14 | Jewish Communal Fund (2.87) | F | OBBBA blog post (2025-10-16), plus evergreen tax pages |
| 15 | Foundation For The Carolinas (2.62) | U | Not requested (site terms) |
| 16 | Greater Kansas City CF (2.57) | F | OBBBA article (2025-10-02). Its calculator was not ported (it computes on the server). |
| 17 | Greater Horizons (2.53) | F | Same article and calculator as GKCCF |
| 18 | CJP Boston (1.93) | F | DAF page only. No OBBBA page was found. |
| 19 | Raymond James Charitable (1.89) | **R** | robots.txt 403 |
| 20 | Dechomai (1.43) | F | A webinar notice only (2026-03-01). No tax figures. |
| 21 | New York Community Trust (1.25) | U | No OBBBA page was found. Guessed URLs returned 404. |
| 22 | Columbus Foundation (1.23) | F | "Important Tax Law Changes" and the bunching article |
| 23 | DonorsTrust (1.21) | F | Q4-2025 article and the guide revised June 2025 |
| 24 | US Charitable Gift Trust (1.19) | **R** | robots.txt 403 |
| 25 | Ayco Charitable Foundation (1.16) | U | No website found |

---

## 3. Calculators [C]

### 3.1 Fidelity Charitable Giving Tax Savings Calculator (port: `fidelity_tax_savings_calc`)

| Profile | Results page | Calculator output | Repo (statute) | Difference |
|---|---|---|---|---|
| H1 ($90k, 12%, $2k, other $12k) | r1 | No figure. Says contributions "may not significantly reduce your tax liability" and suggests bunching. | Direct cash $720 over 3 yrs (§170(p)); DAF $0 | Omits §170(p) |
| H2 ($300k, 24%, $10k, other $25k) | r3 | $672 this year. Bunching 3 years: $5,472. | DAF $312/yr ($936 over 3 yrs). Bunched $5,112. | +$360 (+7.0%) bunched; ×2.15 on the yearly figure |
| H3 ($1m, 37%, $50k, other $40k) | r4 | $21,386 "itemized deductions" saving this year | $17,836 (engine, same quantity) | +$3,550 (+19.9%) |
| H4 ($400k wages + $3m gain, $1m gift) | r4 | $372,886 | $220,234 (engine, same quantity). The repo's gift-only figure for 2026–31 is $218,599. | +$152,652 (+69.3%) |

**Why it differs [C/I]:**
- The formula has no 0.5% floor and no 2/37 reduction. It applies the selected 37% to the whole excess.
- For H4 it applies an ordinary rate to a deduction that mostly offsets gains taxed at 20%.
- There is no non-itemizer path at all.
- On the r3 page, the "this year" saving counts only the charitable part above the standard deduction. The r4 page labels its figure as "itemized deductions" saving, which includes non-charitable deductions. That label is accurate.

### 3.2 Fidelity Appreciated Assets Donation Calculator (port: `fidelity_securities_calc`)
- The calculator's "extra" saving is c × (1 + rate), where c = gain × CG rate. The repo figure is stock in kind minus sell-then-give, DAF vehicle, totals.
- **H1:** $806 against $0. Classed **ambiguous**: the menu forces 15% although H1's gains are in the 0% band.
- **H2:** $4,464 against $4,541.
- **H3:** $32,880 against $28,770.
- **H4:** $219,200 against $191,157.
- **Direction of the errors.** H3 and H4 are overstated because the calculator has no floor and no cap; omitting the 3.8% NIIT works in the opposite direction.
- **Its 2026 capital-gains table is correct.** The MFJ 15% band, $98,901–$613,700, matches the repo parameters from Rev. Proc. 2025-32.

### 3.3 Gift Illustrator "Outright Gifts Calculator" (GKCCF and Greater Horizons)
- The calculator is embedded from `calculator.giftillustrator.com/A0046063/outright-gift`, and its robots.txt allows fetching.
- The served JS sends the inputs to a server (`_sendRequest("outrightGift", …)`). The formula is therefore not in the page, and running the calculator would mean submitting a form.
- **Not ported.** It is unclassified in the CSV (P-B414204-01).

---

## 4. Worked examples [C]

| ID | Sponsor | Stated | Recomputed under the page's own assumptions | Class |
|---|---|---|---|---|
| GKCCF-EX1, GH-EX1 | GKCCF, Greater Horizons | $10,000 at 37% → $3,500, not $3,700 | $3,500 | correct |
| GKCCF-EX2, GH-EX2 | GKCCF, Greater Horizons | $500k AGI → first $2,500 not deductible | $2,500 | correct |
| COL-EX1, IA-FAQ1 | Columbus, ImpactAssets | $1m AGI → $5,000 floor | $5,000 | correct |
| IA-EX1a | ImpactAssets | $100k a year × 3 against $300k at once: about $10,000 more deductible | $10,000 | correct |
| IA-EX1b | ImpactAssets | Worth "up to about $3,500" at 35¢ | $3,500 on the floor alone. The repo engine, with other itemized of $40k (not stated on the page), gives $3,750, because bunching also shrinks the §68 reduction. | ambiguous |
| IA-EX2 | ImpactAssets | $4M of stock with a $200k basis: if sold first, the DAF gets about $3.1M | $3,095,600 (20% + 3.8%) | correct |
| BOFA-EX1 | BofA | Corporation with $10M taxable income gives $150k → $50k deductible | $50,000 | correct |
| BOFA-EX2 | BofA | $1m earner: SALT $10k + mortgage $10k + charity $15k less the $5k floor = $30k, which does not beat the standard deduction | $30,000 against $32,200 | correct |
| BOFA-FOOT | BofA | "0.05% AGI floor" | 0.5%. On the example's $30M that is $150,000, not $15,000. The narration says "a half of 1%". | **arithmetic error** |
| BOFA-EX3 | BofA | $30M sale, $10M gift: tax $4.2M against $6.2M, saving about $2.0M | Engine, with the slide's stated assumptions only: $2.84M against $4.09M, saving $1.25M. The stated levels equal gross 20% gains tax plus $0.2M. | ambiguous |
| JCF-LOU | JCF | $100k of stock with $8k cost → tax "around $15,000" | $13,800 at 15%; $17,296 at 18.8% | ambiguous |
| JCF-CAP | JCF | "value of all deductions is capped at 35% of AGI" | Read literally at H3's $1m that is a $350k cap. The statute sets a per-dollar value of 35¢: H3's $50k gift is worth $17,500. | ambiguous (misstated law) |
| COL-CORP, JCF-CORP | Columbus, JCF | The corporation must give "at least 1 percent … to qualify" / "more than 1% of income before deductions apply" | Test: $10M taxable income, $150k given. The statute allows $50k; a cliff reading gives $150k. | ambiguous |
| GKCCF-CORP | GKCCF | Deductions "only apply to giving above 1% of taxable income" | $50k on the same test | correct |

---

## 5. Statements tested against the four rules [F]

| ID | Quote (short) | Class | Why |
|---|---|---|---|
| FC-METH | The calculator "does not account for … the 0.5% … floor; the itemized deduction cap … 35%; … or the $1,000 … ($2,000 …) limit" | correct | Accurate disclosure |
| FC-SEC-DISC | "does not consider the new provisions … 0.5% floor … 35% limit" | correct | Accurate disclosure |
| FC-R4 | "Charitable contributions can only reduce your tax bill if you choose to itemize" | outdated | Ignores §170(p) for direct cash gifts |
| FC-R1 | "may not significantly reduce your tax liability … Consider … bunching" | outdated | Repo H1 lands here; §170(p) is not mentioned |
| GKCCF-NI | "above-the-line … cash donations made directly to operating charities … DAFs … don't qualify" | ambiguous | The amounts and the DAF exclusion are right. "Above-the-line" and "operating charities" are imprecise (same note as NCF in the top-10 audit). |
| IA-NI | Non-itemizer deduction excludes DAFs; floor carryover "only in limited cases" | correct | |
| JCF-NI | $1,000/$2,000, "cannot be made to a DAF"; 0.5% floor | correct | |
| JCF-EVERGREEN | "you can deduct the amount of money you gave to charity" | outdated | The evergreen pages have no floor or cap |
| COL-NI | $1,000/$2,000, DAFs ineligible; $0.35 per $1 | correct | |
| BOFA-NI | "deduct up to $1,000 of a cash gift to a public charity … $2,000 for a couple" | ambiguous | The DAF exclusion is not stated |
| BOFA-FLOORWORD | "the first half of 1% of charitable deductions" | ambiguous | Wrong base (should be AGI); the later example uses AGI |
| CJP-FULL | "immediate tax deduction of the full amount you donate!" | outdated | Ignores the floor |
| DT-GUIDE | "Your deduction is for the amount of your cash contribution, up to 60%" | outdated | Guide revised June 2025 |
| DT-2025 | "a new giving floor for itemizers and caps on deductions for high earners" | correct | No figures |
| IA-7BEN | Standard deduction "$12,000 to $24,000"; PF excise "Up to 2%" | outdated | The 2026 MFJ standard deduction is $32,200; no floor or cap |

**Not errors, for context [I].** Several 2025 pages (Columbus, JCF, DonorsTrust, BofA) urge giving "in 2025". That was correct when written. They are not classed as errors.

---

## 6. Limits
- **Unread rows.** 6 of 15 sponsors ($12.75bn, 37% of ranks 11–25 assets) have no read 2026 page: 3 are [R] and 3 are [U]. Of the 9 that were read, Dechomai and CJP have no OBBBA text.
- **BofA is read through its affiliate.** The BofA pages are Bank of America Private Bank pages. The fund's own donorfirst site has no tax content.
- **Client-dependent robots results.** Results for www.cct.org differed by HTTP client: curl got 403, while the stdlib client got 200 and then a 403 on the page. Both outcomes meant no read.
- **H4 rate input.** The rate a user would choose for H4 is an interpretation [I]. At 20%, the H4 figure would be $201,560 against $220,234.
- **"Ambiguous" covers two kinds of row:** wording problems, and wrong statements of law that the four-class scheme cannot express (JCF-CAP, BOFA-EX3).
- **Engine scope.** The repo engine is federal income tax only, with 2026 parameters held flat. IA-EX1b uses H3's other-itemized amount because the page does not state one.
- **Page dates.** Most pages are undated or 2025. The dates recorded are those shown on the page.
- **Video content.** The BofA quotes come from transcripts embedded in the page HTML.

---

## 7. Robots and access log (by host, 2026-11-20)

| Host | robots.txt | Verdict | Result |
|---|---|---|---|
| www.fidelitycharitable.org | 200 (403 to the stdlib client on the first try) | allowed | 200: tools page, calculator, methodology, results r1–r4, securities and asset calculators, site JS bundle |
| impactassets.org, jcfny.org, www.growyourgiving.org, www.greaterhorizons.org, www.cjp.org, dechomai.org, www.donorstrust.org, consider.donorstrust.org, www.privatebank.bankofamerica.com, calculator.giftillustrator.com | 200 | allowed | 200 (sitemaps and pages). One donorstrust page returned a JS challenge and was not bypassed. |
| bofa.donorfirst.org, columbusfoundation.org, www.columbusfoundation.org | 404 | no rules | 200 |
| www.nycommunitytrust.org | 200 | allowed | 404 on two guessed URLs |
| www.cct.org | 403 (curl); 200 (stdlib) | blocked | Page 403; not read |
| www.raymondjamescharitable.org | 403 (timeout on the first try) | blocked | Not fetched |
| www.uscharitablegifttrust.org | 403 | blocked | Not fetched |
| www.giveny.org | connection failed | blocked | Not fetched (wrong domain guess) |
| fftc.org, dafgiving360.org | — | not requested | Site terms per the repo / task rule |

---

## 8. Data dictionary: `tax-page-audit-11-25-2026-11-20.csv` (58 rows)

| Column | Meaning |
|---|---|
| finding_id | `FC-CALC-TAX-Hn` / `FC-CALC-SEC-Hn` = calculator × profile; worked-example IDs as in §4; statement IDs as in §5; `COV-nn` = coverage row for rank nn |
| rank_fy2024 | FY2024 DAF-assets rank (league table); "n/a (tools page)" for Fidelity |
| sponsor, ein, fy2024_daf_assets_usd_bn | From the league table ($bn computed). Fidelity rows give the name only. |
| item_type | calculator / worked_example / statement / coverage |
| item | Calculator name or finding ID |
| page_url | Page read (primary URL) |
| page_date | Date shown on the page, or "undated" |
| accessed | 2026-11-20 |
| evidence_label | F, F+C, F (affiliate), R or U |
| rule_tested | floor_0_5pct / cap_35pct / nonitemizer_170p / corporate_1pct_floor / other (";"-separated) |
| quote_or_output | Page quote, or the calculator output and repo figures |
| profile_or_inputs | H1–H4, or the example's inputs |
| stated_value | Figure on the page, or the calculator output (for H1 on page r1: 0) |
| recomputed_value | Repo-engine or statute figure under the page's assumptions |
| difference | stated − recomputed |
| classification | correct / outdated (pre-OBBBA) / arithmetic error / ambiguous. Blank for coverage rows and for the calculator that was not ported. |
| error_kind | no_floor_no_cap, omits_170p, omits_floor, omits_daf_exclusion, wrong_parameter, wrong_base, misstated_mechanism, threshold_wording, imprecise_term, unstated_inputs, not_reproducible, rate_menu_lacks_0pct, stale_figures, not_ported |
| note | Free text |

---

## 9. Source register (primary URLs)

**Law, as the repo has it:** P.L. 119-21, https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm (§§70111, 70424, 70425, 70426). 26 USC 170, https://www.law.cornell.edu/uscode/text/26/170. These were not re-read this pass; see [b41n16-b42n20 §4](b41n16-b42n20-daf-tax-guidance.md) and [b41n18-02 §1](b41n18-02-corporate-floor-pull-forward.md).

**Fidelity Charitable**
- https://www.fidelitycharitable.org/tools.html
- https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator.html
- https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator/charitable-tax-savings-methodology.html
- https://www.fidelitycharitable.org/tools/charitable-tax-savings-calculator/r1.html (also r2, r3, r4)
- https://www.fidelitycharitable.org/tools/securities-donation-calculator.html
- https://www.fidelitycharitable.org/tools/asset-donation-calculator.html
- https://www.fidelitycharitable.org/etc.clientlibs/fidelitycharitable/clientlibs/clientlib-site.lc-5e5c8d29c69fa8948eceeecc3a5eb7fc-lc.min.js

**Ranks 11–25**
- https://www.privatebank.bankofamerica.com/articles/charitable-giving-unlocked-for-business-owners-under-the-obbba.html
- https://www.privatebank.bankofamerica.com/articles/one-big-beautiful-bill-act-summary.html
- https://bofa.donorfirst.org/
- https://impactassets.org/what-the-one-big-beautiful-bill-act-means-for-2026-charitable-giving/
- https://impactassets.org/7-tax-benefits-of-the-impactassets-donor-advised-fund/
- https://jcfny.org/blog/charitable-giving-in-2025-what-the-new-tax-law-means-for-donors/
- https://jcfny.org/donor-advised-funds-tax-deductions/
- https://jcfny.org/donor-advised-funds-tax-deductions/tax-deductible-donations/
- https://www.growyourgiving.org/news/charitable-giving-under-the-new-tax-law-what-donors-and-their-advisors-should-know/
- https://www.growyourgiving.org/resources/gift-calculators/outright-gifts-calculator/
- https://www.greaterhorizons.org/news/charitable-giving-under-the-new-tax-law-what-donors-and-their-advisors-should-know/
- https://www.greaterhorizons.org/outright-gifts-calculator/
- https://calculator.giftillustrator.com/A0046063/outright-gift
- https://www.cjp.org/ways-to-give/donor-advised-funds
- https://dechomai.org/a-forensic-deconstructed-post-mortem-2025-noncash-activity-breakdown-with-2026-trends/
- https://columbusfoundation.org/charitable-insights/important-tax-law-changes
- https://www.columbusfoundation.org/charitable-insights/bunching-charitable-contributions-is-about-to-become-more-popular-than-ever
- https://www.donorstrust.org/a-smarter-way-to-navigate-2025s-final-giving-stretch/
- https://consider.donorstrust.org/hubfs/DT%20Forms%20and%20Files/Donors%20Guide%20to%20DonorsTrust.pdf
