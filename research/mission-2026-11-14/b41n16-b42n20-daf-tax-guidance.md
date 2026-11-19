# DAF tax guidance: pledge payments (P-B41N16-01) and the OBBBA non-itemizer deduction on sponsor pages (P-B42N20-03)

**Prepared 2026-11-19. Desk research only. NOT TAX OR LEGAL ADVICE.** No one was contacted, nothing was logged into, no form was submitted. Nothing was committed.

**Labels.** **[F]** first-party or primary text read in full. **[S]** search-engine text only, not checked against the page. **[R]** not read because of robots.txt. **[U]** nothing found, or not fetched for another stated reason. **[C]** our computation (script). **[I]** interpretation.

**Files written**
- This note.
- [`data/mission-2026-11-14/daf-pledge-policy-2026-11-19.csv`](../../data/mission-2026-11-14/daf-pledge-policy-2026-11-19.csv): 46 rows (30 recipients, 15 sponsors, 1 IRS reference row).
- [`data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv`](../../data/mission-2026-11-14/sponsor-obbba-tax-page-audit-2026-11-19.csv): 10 rows (top-10 sponsors by FY2024 DAF assets).
- [`scripts/mission_b41n16_b42n20_checks.py`](../../scripts/mission_b41n16_b42n20_checks.py): stdlib, pure functions. Ports the two sponsor calculators found, recomputes every sponsor worked example, and reads the repo's H1–H3 totals. Run with `python3 scripts/mission_b41n16_b42n20_checks.py .`
- [`data/mission-2026-11-14/queue-proposals-b41n16-b42n20.csv`](../../data/mission-2026-11-14/queue-proposals-b41n16-b42n20.csv): 5 proposals.

**Repo context read first**
- [direction-gift-office-daf-handling.md](direction-gift-office-daf-handling.md) and [`gift-office-daf-policies-2026.csv`](../../data/mission-2026-11-14/gift-office-daf-policies-2026.csv): the source of the 33-recipient universe, their ranks and FY2023–24 DAF dollars, and the earlier pledge readings carried forward here.
- [direction-donor-tax-scenarios-2026.md](direction-donor-tax-scenarios-2026.md) and [`donor-tax-scenarios-2026.csv`](../../data/mission-2026-11-14/donor-tax-scenarios-2026.csv): the H1–H3 results. That note's wave-27 corrections affect only H4/S3, not H1–H3.
- [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md): which sponsor sites' terms bar robots. This was used to decide which sites not to fetch (§1.2).
- [`daf-sponsor-league-table-fy2021-2025.csv`](../../data/mission-2026-11-14/daf-sponsor-league-table-fy2021-2025.csv): FY2024 `top50` rows ranked by DAF assets define "top 10" and "top 15".

---

## 0. Answers in brief

| Question | Finding | Confidence |
|---|---|---|
| Has Notice 2017-73 §4 (a DAF grant may meet a pledge if the sponsor does not mention the pledge) been superseded or narrowed? | **No.** No later guidance supersedes or narrows it, as of 2026-11-19.<br>– The notice says taxpayers "may rely on the rules described in section 4 until additional guidance is issued" (§7) [F].<br>– The Nov 2023 §4966 NPRM (REG-142338-07) only recites §4 in its background. It leaves §4967 to "future guidance" [F].<br>– No final §4966 rule and no §4967 proposal appears in the Federal Register [F]. eCFR Part 53 has no §53.4966 or §53.4967 section [F].<br>**One risk [I]:** the NPRM's "deemed distribution" rule treats any DAF use that gives a more-than-incidental benefit as a distribution, and so as a taxable distribution. If a pledge payment were ever held to be such a benefit, the sponsor would face §4966 tax as well as §4967 tax. | High on the Federal Register and plans; the risk is [I] |
| Direction of travel | **The §4967 project that carried the pledge rule has left the plan.**<br>– "Regulations under §4967 regarding prohibited benefits" appears in the 2023-24 (Q4) and 2024-25 Priority Guidance Plans. It is gone from the 2025-26 plan (initial and year-end update) and from the 2026-27 plan [F].<br>– The 2026-27 plan adds a new item: "Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements" [F].<br>– Final §4966 regulations stayed on the 2025-26 plan with no "PUBLISHED" entry by 2026-09-30 [F]. | High |
| Top-30 university and AMC gift offices | **2 follow the notice and 8 forbid; 20 are unknown.**<br>– **Follow the notice:** Stanford and Caltech, $841.5m of FY23–24 DAF grants [F].<br>– **Forbid DAF payment of a personal pledge, or book DAF commitments only as non-binding intentions (8, $852.9m):** Penn [S], Chicago Booth [F], WashU [F], Michigan (binding pledges) [S], Duke [F], Northwestern [F, upgraded], USC [F, new], UW [S].<br>– **Not stated on the pages read:** 13 ($2,158.0m).<br>– **Not read:** 7 ($3,260.7m), mostly because of robots.txt. This group includes Johns Hopkins ($2,609.6m). | High on the [F] rows; the unknowns dominate the dollars |
| Top-15 sponsors | **2 follow the notice and 5 bar binding pledges; 8 are unknown.**<br>– **Follow the notice:** AEF [F] (its granting guidelines copy all three of the notice's conditions) and NPT [S].<br>– **Bar binding pledges (5):** Fidelity allows only non-binding pledges [F]. DAFgiving360 (2024 Program Policies) [F], Vanguard [F], MS GIFT [F] and NCF [F] bar binding pledges.<br>– **Not stated:** 4 (SVCF, BofA, CCT, JCF) [F].<br>– **Not read:** 4 (GS PF [R]; Renaissance, ImpactAssets and FFTC [U]). | High on the [F] rows |
| OBBBA statute (P.L. 119-21) | **Verified on govinfo, with LII for the amended Code.**<br>– **§70424:** §170(p) becomes $1,000 / $2,000. Effective for tax years beginning after 2025. **Not indexed.**<br>– **§170(p) excludes DAFs:** contributions "for the establishment of a new, or maintenance of an existing, donor advised fund" do not count, and neither do gifts to 509(a)(3) organizations. The deduction is computed without regard to (b)(1)(I), so the floor does not apply to it.<br>– **§70425:** 0.5% of contribution base floor (new §170(b)(1)(I)), with carryforward only from years with a percentage-limit excess (§170(d)(1)(C)).<br>– **§70111:** §68 reduces itemized deductions by 2/37. "35%" is the effective result of that reduction, not the statutory wording.<br>– congress.gov disallows Claude user agents, so it was not used [F]. | High |
| Do the top-10 sponsors' 2026 pages say DAF gifts do not qualify for the non-itemizer deduction? | **Mostly yes.**<br>– 6 of 10 say so on a page read in full [F]: Fidelity, DAFgiving360, Vanguard, SVCF, AEF and NCF. That is $161.8bn of $222.5bn top-10 DAF assets read [F].<br>– 2 say so on search text only [S]: NPT and Renaissance.<br>– MS GIFT says it only implicitly: "only available if you elect to itemize".<br>– GS PF was not read [R]. | High |
| Do they state the 0.5% floor and the 35% cap? | **Floor:** 7 of 10 [F] and 2 more [S].<br>**35% cap:** 6 [F] and 1 [S]. AEF's page does not mention the cap. | High |
| Calculators | **Two found in the top 10.**<br>– **Vanguard's Tax Calculator** models the 0.5% floor and the 35% cap. On H1 and H2 it reproduces the repo's results exactly [C].<br>– **DAFgiving360's bunching calculator** models neither the floor nor the cap. It overstates H2 annual savings ($2,016 against $936) and H3 savings ($55,500 against $47,250, +17.5%) [C].<br>– Vanguard's calculator overstates H3 for a different reason: it credits the gift with the excess of other itemized deductions over the standard deduction ($55,440 against $47,250) [C]. | High (code read and ported) |
| Errors on sponsor pages | **Three of the 7 fully read sponsors have a misstatement [C/F].**<br>– **Vanguard's bunching example:** the arithmetic is wrong. At its own stated 35% rate, the bunching gain is $2,450, not $655.<br>– **DAFgiving360:** says the $1,000/$2,000 comes "with inflation adjustments over time". The statute has no indexing.<br>– **MS GIFT's DAF article:** says amounts disallowed by the floor "carry over for up to five taxable years" with no condition. §170(d)(1)(C) limits this carryover.<br>– **AEF:** the arithmetic is right, but the annual baseline omits §170(p) for direct gifts. This overstates the bunching gain over direct annual giving: $4,872 against $3,432 [C]. | High |

---

## 1. Method

### 1.1 Access rules
- **robots.txt first.** Every host's robots.txt was fetched before any page and parsed for `*`, the script user agent (`research-script/1.0`), ClaudeBot, Claude-User and anthropic-ai. A page was fetched only when all five were allowed. A 404 counted as no rules. Any other status, or an unreachable robots.txt, meant the host was not fetched.
- **Fetcher.** The fetcher was `tools/fx.py` in the scratchpad: stdlib, functional, with a generic user agent. It made 102 requests to 50 hosts. Its log has one row per request (time, URL, robots status, verdicts, HTTP status, cache file). The host summary is in §7.
- **Excluded sources.** No crt.sh, certspotter or sec.gov. No logins or forms.
- **Search.** Search-engine results were used only to find URLs, and as [S] evidence where a fetch was barred.

### 1.2 Sites not fetched although robots.txt allowed them
- **NPT, Renaissance Charitable and Foundation For The Carolinas.** The repo records that their site terms bar robots or scraping for the whole website ([queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md)). Their rows here are [S] or [U].
- **One exception, disclosed:** one www.reninc.com URL was requested before this decision was applied. It returned 404 and no content was used.
- **Vanguard and NCF were fetched.** Their bot and scraping clauses cover the logged-in Secure Site only, per the repo's quotes.

### 1.3 Part A1: supersession check
- **Federal Register API**, document searches since 2021 and 2023:
  - "donor advised fund" (2023-01-01 on): 5 results.
  - "donor-advised" (2024-06-01 on): 4 results.
  - "4967" (IRS, 2023-01-01 on): 5 results.
  - "2017-73" (2021 on): 30 results, of which the only Treasury document is the NPRM.
- **Full texts read:** the NPRM (govinfo FR-2023-11-14 doc 2023-24982) and its 2024-01-09 comment extension (2024-00260).
- **Priority Guidance Plans:** all five 2024–2026 PDFs (§2.2).
- **eCFR:** Part 53 structure and a full-text search for "donor advised fund".
- **IRS DAF page** (last reviewed 2026-10-09).
- **The notice itself.**

### 1.4 Part A2: pledge rules
- **Recipients:** the 30 highest-ranked recipients in the repo's 33-recipient gift-office set, ranked by FY2023–24 DAF grants from top-50 sponsors.
  - Each carries its repo reading.
  - Rows were re-fetched or searched where the repo had [S], [R] or not_found.
- **Sponsors:** FY2024 ranks 1–15. Each sponsor's program policies, granting guidelines or FAQ was searched for "pledg".
- **Rule classes** (CSV `rule_class`):
  - `allowed_if_no_reference`: follows Notice 2017-73.
  - `forbids_any_personal_pledge`.
  - `forbids_binding_pledge`.
  - `non_binding_intention_only`: the recipient books DAF commitments as non-binding.
  - `non_binding_pledges_only`: the sponsor supports only non-binding pledges.
  - `not_stated`.
  - `not_read`.
- The last four forbidding classes all depart from the notice, which permits payment of a binding pledge too.

### 1.5 Part B: OBBBA audit
- **Statute:** read on govinfo PLAW-119publ21 (§§70111, 70424, 70425), with the amended §170 on LII.
- **Sponsor pages:** for each top-10 sponsor, 2026 tax pages were found by search restricted to the sponsor's domain and then fetched.
- **Claim tests:** `tools/claims.py` ran sentence-level regex tests for each claim (DAF exclusion, $1,000/$2,000, 0.5%, 35%, inflation, examples, calculators). The quotes were then read by hand.
- **Calculators:** the JS logic was read and ported faithfully in the script.
- **Inputs:** H1–H3 inputs come from the repo's tax note §2.1.

---

## 2. Part A1: Is Notice 2017-73 §4 still the rule?

### 2.1 What §4 says [F]
- A DAF distribution to a charity where the donor or advisor has a pledge is not a more-than-incidental benefit under §4967 if:
  1. the sponsor "makes no reference to the existence of a charitable pledge when making the DAF distribution";
  2. no donor or advisor gets any other more-than-incidental benefit; and
  3. no one claims a §170 deduction for the distribution.
- It applies "whether or not enforceable under local law", and "for purposes of § 4967 only".
- **§7:** "Taxpayers may rely on the rules described in section 4 until additional guidance is issued."
- Source: [Notice 2017-73, pp. 9–10, 14](https://www.irs.gov/pub/irs-drop/n-17-73.pdf).

### 2.2 Later guidance checked

| Item (date) | What it says on pledges or §4967 | Effect on §4 |
|---|---|---|
| [REG-142338-07 NPRM, 88 FR 77922](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm) (2023-11-14) | **Background only:** it recites that Notice 2017-73 said Treasury and the IRS "are considering developing proposed regulations under section 4967" under which pledge-related distributions "do not result in a more than incidental benefit ... if certain requirements are met".<br>**Footnote 4:** the non-§4966 comments "will be considered in the development of future guidance under other Code sections".<br>**Proposed §53.4966-1(e)(2):** "A distribution includes any use of donor advised fund assets that results in a more than incidental benefit (within the meaning of section 4967) ..."<br>**Applicability:** proposed to apply to tax years ending after final regulations are published. | **None.** §4 is neither withdrawn nor narrowed.<br>The deemed-distribution rule, if finalised, would make any benefit that is more than incidental under §4967 a taxable distribution as well [I]. |
| [Comment extension 2024-00260](https://www.federalregister.gov/api/v1/documents/2024-00260.json) (2024-01-09); hearing notices 2024-04262 and 2024-08419 | Procedural | None |
| [2023-24 PGP, 4th-quarter update](https://www.irs.gov/pub/irs-counsel/2023-2024-fourth-quarter-update.pdf) (2024-09-06) | §4966 regs "PUBLISHED 11/14/23". Item 7 still lists "Regulations under §4967 regarding prohibited benefits". | §4967 project still open |
| [2024-25 PGP, initial](https://www.irs.gov/pub/irs-counsel/2024-2025-priority-guidance-plan-initial-version.pdf) (2024-10-03) | Item 6: "Final regulations under §4966". Item 7: §4967 regulations. | Open |
| [2025-26 PGP, initial](https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf) (2025-09-30) | Item 35: final §4966 regulations. **No §4967 item.** | §4967 project dropped from the plan |
| [2025-26 PGP, year-end update to 9-30-26](https://www.irs.gov/pub/irs-counsel/2025-2026-pgp-year-end-update-thru-9-30-26.pdf) (2026-10-30) | Item 35 has no "PUBLISHED" entry. No §4967 item. | Final §4966 regs not issued |
| [2026-27 PGP, initial](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf) (2026-09-29) | Tax Exempt Organizations item 4: "Guidance under §§4966 and 6033 regarding certain donor advised fund arrangements". No §4967 item. The OBBBA section has no §170 item. | **New DAF item.** Its scope is not stated, so it is the one to watch (P-B4142-01). |
| Federal Register to 2026-11-19 | No Treasury final rule and no §4967 proposal. The "2017-73" search finds only the NPRM. | None |
| [eCFR Part 53, current](https://www.ecfr.gov/api/versioner/v1/structure/current/title-26.json?part=53) | Sections jump from §53.4965 to §53.4968. There is no §53.4966 or §53.4967. | None |
| [IRS "Donor-advised funds" page](https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds) (reviewed 2026-10-09) | No pledge text | None |

**Conclusion [F/I].** §4 is still reliance guidance and has not been narrowed. The only formal project that would have codified it (§4967 regulations) is no longer on the plan. Sponsors and recipients that forbid pledge payment do so as their own policy, not because later guidance requires it. Many cite "IRS regulations", but no regulation says this.

---

## 3. Part A2: Who follows the notice and who forbids pledge payment

### 3.1 Recipients (top 30 university and AMC; FY2023–24 DAF grants from top-50 sponsors)

| Class | n | FY23–24 DAF $m [C] | Who (label) |
|---|---|---|---|
| Follows Notice 2017-73 | 2 | 841.5 | Stanford (Stanford Live guideline) [F], Caltech gift policies 2024-10 [F] |
| Forbids paying any personal pledge | 3 | 337.2 | Penn policy 2217 [S] (fetch 403), Chicago Booth [F], WashU [F] |
| Forbids paying a binding pledge | 1 | 93.0 | Michigan [S] (fetch 403) |
| Books DAF commitments only as a non-binding intention | 4 | 422.7 | Duke [F]; **Northwestern [F]** (NBI transmittal: "donor-advised fund as legal donor"); **USC [F]** (policy: pledges likely paid by a DAF "should be written in the form of a non-binding statement of intention", last reviewed 2021-03-01); UW [S] |
| Not stated on the pages read | 13 | 2,158.0 | Harvard, Cornell, **UC Berkeley (FAQ) [F]**, **MIT [F]**, Yale, Dartmouth, Princeton, Columbia (external DAFs), Notre Dame, **St Jude [F]**, **Mayo [F]**, Georgetown, Ohio State |
| Not read | 7 | 3,260.7 | Johns Hopkins (robots 403), UCSF (robots unreachable), NYU (robots 403), Oregon, Lucile Packard, Rockefeller, Boston College |
| **Total** | **30** | **7,113.1** | |

**Bold** marks rows upgraded this pass:
- MIT, Mayo and St Jude moved from not_read or [S] to read [F]. MIT's robots.txt now returns 200.
- USC moved from not_found to non-binding intention [F].
- Northwestern moved from [S] to [F].
- Berkeley moved from [R] to not_stated [F].

**Reading [I].**
- Of the 10 recipients that state a rule, 8 depart from the notice. Most of these do not refuse DAF money outright. They turn pledges into non-binding intentions.
- Only 2 recipients, $841.5m (11.8% of the 30-recipient total), publish the notice's own rule.
- The unread group alone holds 45.8% of the dollars: $3,260.7m of $7,113.1m.

### 3.2 Sponsors (FY2024 ranks 1–15 by DAF assets)

| Class | n | Sponsors |
|---|---|---|
| Follows the notice | 2 | AEF [F] ("Donors may recommend a grant to fulfill a pledge ... provided ... AEF makes no reference to the existence of the pledge"), NPT [S] |
| Non-binding pledges only | 1 | Fidelity Charitable [F] ("Grant recommendations can be made in support of non-legally binding pledges"; "Pledge (non-binding)" grant-use code) |
| Bars binding pledges | 4 | DAFgiving360 [F, 2024 Program Policies: "No grant can be used to relieve an individual of a legally binding pledge"]; Vanguard [F, Jan 2026]; MS GIFT [F, grantmaking guide: "A grant to fulfill a legally binding pledge or other agreement" is impermissible, and "Pledge" is listed as language to avoid]; NCF [F, "Fulfillment of legally binding pledges"] |
| Not stated in documents read | 4 | SVCF (Advised Fund Agreement), BofA (DAF guide), CCT (portal FAQ), JCF (Aug 2024 Policy Guide) [F] |
| Not read | 4 | Goldman Sachs PF [R]; Renaissance [U: site terms; search found no rule]; ImpactAssets [U: circular 403, FAQ 404]; FFTC [U: site terms] |

**Product implication [I].** The two largest sponsors by assets that follow the notice, NPT and AEF, are the ones on which a pledge-matching feature could rest. At Fidelity, DAFgiving360, Vanguard, MS GIFT and NCF, a feature that pays pledges would need recipients to record the pledge as non-binding.

---

## 4. Part B step 1: OBBBA statutory text (P.L. 119-21), verified [F]

| Provision | Text read | Where |
|---|---|---|
| §70424 | "Section 170(p) is amended (1) by striking '$300 ($600' and inserting '$1,000 ($2,000', and (2) by striking 'beginning in 2021'." Effective for tax years beginning after Dec 31, 2025. | [govinfo PLAW-119publ21](https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm), 139 Stat. 235 |
| §170(p) as amended | Deduction "not in excess of $1,000 ($2,000 in the case of a joint return)" for cash contributions "(determined without regard to subsections (b)(1)(G)(ii), (b)(1)(I), and (d)(1)) to an organization described in section 170(b)(1)(A) and not (1) to an organization described in section 509(a)(3), or (2) for the establishment of a new, or maintenance of an existing, donor advised fund". **No inflation adjustment.** | [26 USC 170(p), LII](https://www.law.cornell.edu/uscode/text/26/170) |
| §70425(a) | New §170(b)(1)(I): contributions are deductible "only to the extent that the aggregate of such contributions exceeds 0.5 percent of the taxpayer's contribution base". The floor applies first to (D) contributions, then (C), (B), (E), (A) and (G). New §170(d)(1)(C) carries amounts disallowed by the floor forward only from years "from which an excess is carried forward ... under any carryover rule". §70425(a)(3) adds "(b)(1)(I)" to the §170(p) exclusions. | P.L. 119-21, 139 Stat. 235–236 |
| §70111 | New §68(a): itemized deductions "shall be reduced by 2/37 of the lesser of (1) such amount of itemized deductions, or (2) so much of the taxable income ... as exceeds the dollar amount at which the 37 percent rate bracket ... begins". §68(b) applies this after all other limits. | P.L. 119-21, 139 Stat. 164–165 |
| IRS restatement | IR-2026-135 (Nov 10, 2026): "Cash contributions made either to supporting organizations or to establish or maintain a donor advised fund do not qualify." Pub. 6196: "Donations made to donor-advised funds generally do not qualify for this deduction." | [IR-2026-135](https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize); [Pub. 6196](https://www.irs.gov/pub/irs-pdf/p6196.pdf) |

**Access.** congress.gov's robots.txt disallows ClaudeBot, Claude-User and anthropic-ai, so no congress.gov page was fetched. govinfo allowed all of them.

**Agreement with the repo.** All of these match the parameters in the repo's [`donor-tax-parameters-2026.csv`](../../data/mission-2026-11-14/donor-tax-parameters-2026.csv). No correction is needed.

---

## 5. Part B steps 1 and 2: The top-10 sponsors' 2026 pages

### 5.1 Summary (full quotes and URLs are in the CSV)

| # | Sponsor (FY24 DAF assets $bn) | DAF excluded from $1k/$2k | 0.5% floor | 35% cap | Calculator | Errors found | Label |
|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable (66.20) | yes | yes | yes | none found | none | F |
| 2 | NPT (42.12) | yes [S] | yes [S] | not verified | — | — | S |
| 3 | DAFgiving360 (40.94) | yes | yes | yes | bunching calculator: no floor, no cap, no §170(p) | "inflation adjustments over time" for the $1k/$2k | F |
| 4 | Vanguard Charitable (21.95) | yes | yes | yes | Tax Calculator: floor yes, cap yes | bunching example arithmetic | F |
| 5 | GS Philanthropy Fund (12.64) | not read | — | — | — | — | R |
| 6 | SVCF (9.58) | yes | yes | yes | none found | none (single-filer amount only) | F |
| 7 | MS GIFT (9.11) | implicit only | yes | yes | none found | floor carryover stated without the §170(d)(1)(C) condition | F |
| 8 | AEF (8.38) | yes (cites §70424) | yes | not on page | none found | baseline omits §170(p) | F |
| 9 | Renaissance (5.91) | yes [S] | yes [S] | yes [S] | not checked | — | S |
| 10 | NCF (5.68) | yes ("not to Giving Funds") | yes | yes | none found | none | F |

**Counts [C]:**
- **DAF exclusion stated:** 6 [F] + 2 [S]; 1 implicit; 1 not read.
- **Floor stated:** 7 [F] + 2 [S].
- **35% cap stated:** 6 [F] + 1 [S].
- **Coverage:** the 7 [F] rows hold $161.84bn of the top 10's $222.51bn FY2024 DAF assets.

### 5.2 Calculators compared with H1–H3 (3-year totals, cash, married filing jointly) [C]

Output of `scripts/mission_b41n16_b42n20_checks.py` (both ports are line-for-line copies of the sponsors' JS formulas):

| Profile | Repo: DAF annual | Repo: DAF bunched | Repo: direct cash annual | Vanguard calc, annual | Schwab calc, annual | Schwab calc, bunched |
|---|---|---|---|---|---|---|
| H1 ($90k AGI, 12%, $2k/yr, other $12k) | 0 | 0 | **720** | 0 | 0 | 0 |
| H2 ($300k, 24%, $10k/yr, other $25k) | 936 | 5,112 | 1,440 | **936** | 2,016 | 5,472 |
| H3 ($1m, 37%, $50k/yr, other $40k) | 47,250 | 50,750 | 47,250 | 55,440 | 55,500 | 55,500 |

**Reading:**
1. **Vanguard** reproduces the repo exactly for H1 and H2, where other itemized deductions are below the $32,200 standard deduction.
   - For H3 it reports (all itemized − standard deduction) × 35%. That credits the gift with ($40,000 − $32,200) × 35% = $2,730 a year that the donor would save without giving.
   - It also does not offer the §170(p) direct-gift alternative. That is correct for a DAF gift, but the calculator cannot show H1's $720 or H2's $1,440 direct-cash advantage.
2. **DAFgiving360's bunching calculator** has no AGI input, so it cannot apply the 0.5% floor. It uses 0.37 for the 37% bracket.
   - This overstates H2 annual savings 2.15× ($2,016 against $936).
   - It overstates H3 by $8,250, or 17.5%.
   - Its "addl tax saving from bunching" for H2 is $3,456. The repo's bunching gain is $4,176 against annual DAF gifts and $3,672 against annual direct cash.
3. **Neither calculator shows a non-itemizer that a direct cash gift beats a DAF gift.** That is the repo's H1 and H2 finding (H1: direct $720 against DAF $0). Only the sponsors' text pages say DAF gifts are excluded.

### 5.3 Worked examples on sponsor pages [C]

| ID | Sponsor | Stated | Recomputed under the sponsor's own assumptions | Verdict |
|---|---|---|---|---|
| VC-EX1 | Vanguard ($700k AGI, "35% bracket", $40k/yr) | $9,490/yr; $28,470 over 3 yrs; $29,125 bunched; "+$655" | (40,000 − 3,500) × 35% = **$12,775**/yr; **$38,325**; (120,000 − 3,500) × 35% = **$40,775**; **+$2,450** (= 2 × $3,500 floor × 35%) | **Wrong.** The stated figures imply 26% and 25% rates. |
| VC-EX2 / VC-EX3 | Vanguard | $640k AGI: floor $3,200, $9,000 bunched → $5,800 deductible; $2m AGI: floor $10,000, $25k → $15,000 | same | Correct |
| AEF-EX1 | AEF ($300k AGI, $18k other, $12k/yr, 24%) | itemized $52,500; totals $96,600 against $116,900; +$20,300; ≈$4,900 | $52,500; $96,600; $116,900; +$20,300; $4,872 | Correct, but the baseline omits §170(p). Against direct annual cash gifts the totals are $102,600 against $116,900: +$14,300, worth **$3,432**. |
| FC-EX1 | Fidelity | $1,000 → $350 (was $370) | 1,000 × 37% × (1 − 2/37) = $350 | Correct (same per-dollar value as repo H3) |
| FC-EX2 | Fidelity advisor deck ($2.5m AGI, $200k gift) | $187.5k deductible; $74k → $65.6k | $187,500; $74,000; $65,625 | Correct |
| SCH-EX1 | DAFgiving360 | $10,000 at 37% → $3,500, not $3,700 | $3,500 | Correct |
| FLOOR-EX | Fidelity, Fidelity.com, DAFgiving360, Vanguard, AEF, Renaissance [S] | Floors of $1,500 ($300k AGI), $1,000 ($200k), $5,000 ($1m), $2,500 ($500k) | same | Correct |

### 5.4 Misstatements of law [F]
- **DAFgiving360** (tax-law-changes page, and the same sentence on advisorservices.schwab.com): the $1,000/$2,000 deduction comes "with inflation adjustments over time".
  - §170(p) as amended contains no adjustment.
  - Fidelity's page states "This provision is not indexed for future inflation."
- **MS GIFT's DAF article**, footnote 4: "Amounts disallowed under this rule carry over for up to five taxable years."
  - §170(d)(1)(C) allows that only "from years in which limitation is exceeded".
  - Morgan Stanley's own parent-site article states the condition correctly.
- **Fidelity's "donor-advised fund sponsors" wording** is imprecise but not wrong [I]. The statute excludes gifts made to establish or maintain a DAF, not every gift to a sponsoring organization.

### 5.5 Answer to P-B42N20-03 [I]
- **Messaging is not misleading on eligibility.** On the text pages, small-donor messaging does not overstate eligibility: every fully read sponsor except MS GIFT says DAF gifts are outside the $1,000/$2,000 deduction.
- **Two tools overstate the tax benefit:**
  - DAFgiving360's bunching calculator ignores the floor and the cap.
  - Vanguard's worked bunching example has wrong arithmetic. Its stated gain ($655) understates the bunching gain, while its stated savings levels understate the 35%-bracket value.
- **One framing omits the direct-gift option.** AEF's example leaves out §170(p) for direct gifts, which inflates the case for DAF bunching against giving cash directly. This is the repo's H2 comparison.

---

## 6. Limits
- **Unread rows dominate.**
  - **Pledges:** 7 of 30 recipients (45.8% of the dollars) and 4 of 15 sponsors are unread. Johns Hopkins, the largest recipient, is behind a robots.txt that returns 403.
  - **OBBBA audit:** NPT and Renaissance are [S]; GS PF is [R].
- **"Not stated" is not "allowed".** The 13 not-stated recipients may record DAF pledges in internal policy that is not public.
- **Search-text rows ([S])** were not checked against the page. Search-tool summaries are paraphrases, so a direct page read could change these rows.
- **Schwab's pledge rule** comes from the 2024 Program Policies, on a third-party (Squarespace) copy that the repo had already used. The 2026 dafgiving360.org policies page loads no policy text.
- **MS GIFT's grantmaking guide** is undated.
- **Calculator ports.** The ports reproduce each tool's formula, not its user interface. A user who enters different inputs, such as the actual bracket for the Vanguard calculator, would get different outputs.
- **H1–H3 settings.** The H1–H3 comparison uses the repo's stylised households and 2026 parameters held flat. State tax is not modelled.
- **Dates.** Most sponsor pages are undated. The dates recorded are page metadata or upload paths where present. The USC policy was last reviewed 2021-03-01. Notice 2017-73 (2017) is the subject of the check, not evidence of current practice.
- **Not legal advice.** Whether a given pledge is "binding" depends on state law, and this was not examined.

---

## 7. Robots and access log (by host, 2026-11-19)

| Host | robots.txt | Verdict | Result |
|---|---|---|---|
| www.federalregister.gov, www.govinfo.gov, www.ecfr.gov, www.irs.gov (/pub/, /newsroom/, /charities-non-profits/, /privacy-disclosure/), www.law.cornell.edu (crawl-delay 10 s; 1 request) | 200 | allowed | 200 |
| www.congress.gov | 200 | **disallows ClaudeBot / Claude-User / anthropic-ai** | not fetched |
| www.fidelitycharitable.org, www.fidelity.com, www.dafgiving360.org, advisorservices.schwab.com, content.schwab.com, www.vanguardcharitable.org, www.svcf.org, www.morganstanley.com, www.aefonline.org, aefonline.org, advisorwelcome.aefonline.org, www.ncfgiving.com, site.ncfgiving.com, jcfny.org, donorportal.cct.org, www.goldmansachs.com, privatewealth.goldmansachs.com | 200 | allowed | 200 (some guessed URLs 404) |
| bofa.donorfirst.org, static1.squarespace.com | 404 | no rules | 200 |
| gspf.goldman.com | 200 | **disallows all** | not fetched |
| www.gspf.goldman.com, mail.aefonline.org, give.ucsf.edu | unreachable | treated as blocked | not fetched |
| giving.jhu.edu, www.nyu.edu | **403** | treated as blocked | not fetched |
| policies.osu.edu (gift-acceptance PDF path) | 200 | **disallowed** | not fetched |
| giving.mit.edu, plannedgiving.mayoclinic.org, www.stjude.org, www.bu.edu, www.northwestern.edu, policy.usc.edu, alumni.princeton.edu, give.berkeley.edu | 200 | allowed | 200 |
| giving.umich.edu, www.finance.upenn.edu | 200 | allowed | **HTTP 403** to the fetch |
| giving.uoregon.edu, www.lpfch.org, www.rockefeller.edu, www.bc.edu, planyourlegacy.berkeley.edu, impactassets.org, www.reninc.com | 200 | allowed | 404 (guessed URLs) |
| www.nptrust.org, renaissancecharitable.org, fftc.org | — | not requested: site terms bar robots or scraping (repo) | [S] or [U] |

The full per-request log is in the session scratchpad and is not in the repo.

---

## 8. Data dictionaries

### 8.1 `daf-pledge-policy-2026-11-19.csv` (46 rows)

| Column | Meaning |
|---|---|
| row_id | `PL-GO-xx` = recipient, carrying the repo `gift-office-daf-policies-2026.csv` row id; `PL-Sxx` = sponsor at FY2024 asset rank xx; `PL-R1` = the IRS reference row |
| side | recipient / sponsor / regulator |
| entity, ein | Name and EIN. Recipient EINs are carried from the repo; sponsor EINs come from the league table |
| rank_basis, rank | What the rank means. Recipients: rank among top-50-sponsor FY2023–24 DAF recipients. Sponsors: FY2024 DAF-assets rank |
| usd_m | Recipients only: FY2023–24 DAF grants received from top-50 sponsors, $m (repo) |
| rule_class | allowed_if_no_reference / forbids_any_personal_pledge / forbids_binding_pledge / non_binding_intention_only / non_binding_pledges_only / not_stated / not_read |
| follows_notice_2017_73_s4 | yes / no / unknown, derived from rule_class |
| forbids_daf_pledge_payment | no / yes_any_pledge / yes_binding_only (with qualifier) / unknown |
| rule_quote | Quoted rule text, or what was read and found silent |
| evidence_label | F / S / R / U as defined above |
| source_url | Primary URL(s), separated by ";" |
| page_date | Date on or in the document, where shown |
| accessed | Date read (2026-11-19 for this pass; the repo date for carried rows) |
| robots_or_access | robots verdict and HTTP result |
| carried_from | Repo row id, if any |
| change_vs_repo | Change made this pass |
| notes | Free text |

### 8.2 `sponsor-obbba-tax-page-audit-2026-11-19.csv` (10 rows)

| Column | Meaning |
|---|---|
| rank_fy2024, sponsor, ein, fy2024_daf_assets_usd_bn | From the league table (FY2024 `top50` rows, rank by DAF assets; $bn computed) |
| pages_read, page_dates, access_status | URLs read, dates shown, and robots or terms status |
| states_daf_excluded_from_nonitemizer | yes / yes [S] / implicit only / not read |
| daf_exclusion_quote | Supporting quote |
| states_0_5pct_floor, floor_quote | Whether the 0.5% floor is stated, and the quote |
| states_35pct_cap, cap_quote | Whether the 35% cap is stated, and the quote |
| nonitemizer_amounts_stated | Amounts as stated, including any indexing claim |
| calculator_url | Calculator found, or "none found" |
| calculator_models_floor / _cap / _nonitemizer_170p | From the calculator's JS code |
| worked_example_ids | Keys into the script's `worked_examples()` and §5.3 |
| worked_example_check | Result of the recomputation |
| errors_or_overstatements | Misstatements against the statute or arithmetic |
| vs_repo_H1_H3 | Comparison with `donor-tax-scenarios-2026.csv` |
| evidence_label, accessed | Label and access date |

---

## 9. Source register (primary URLs)

**Law and guidance**
- P.L. 119-21: https://www.govinfo.gov/content/pkg/PLAW-119publ21/html/PLAW-119publ21.htm
- 26 USC 170: https://www.law.cornell.edu/uscode/text/26/170
- Notice 2017-73: https://www.irs.gov/pub/irs-drop/n-17-73.pdf
- REG-142338-07 NPRM: https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm
- Comment extension: https://www.federalregister.gov/api/v1/documents/2024-00260.json
- Federal Register search API: https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=%22donor+advised+fund%22&conditions%5Bpublication_date%5D%5Bgte%5D=2023-01-01&per_page=50
- Priority Guidance Plans:
  - https://www.irs.gov/pub/irs-counsel/2023-2024-fourth-quarter-update.pdf
  - https://www.irs.gov/pub/irs-counsel/2024-2025-priority-guidance-plan-initial-version.pdf
  - https://www.irs.gov/pub/irs-counsel/2025-2026-initial-pgp.pdf
  - https://www.irs.gov/pub/irs-counsel/2025-2026-pgp-year-end-update-thru-9-30-26.pdf
  - https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf
  - Index page: https://www.irs.gov/privacy-disclosure/priority-guidance-plan
- eCFR Part 53: https://www.ecfr.gov/api/versioner/v1/structure/current/title-26.json?part=53
- IRS DAF page: https://www.irs.gov/charities-non-profits/charitable-organizations/donor-advised-funds
- IR-2026-135: https://www.irs.gov/newsroom/irs-reminder-permanent-charitable-contribution-deduction-begins-for-returns-filed-next-year-for-taxpayers-who-do-not-itemize
- Pub. 6196: https://www.irs.gov/pub/irs-pdf/p6196.pdf

**Sponsor tax pages and calculators.** Listed per row in `sponsor-obbba-tax-page-audit-2026-11-19.csv`. The key ones:
- https://www.fidelitycharitable.org/articles/obbb-tax-reform.html
- https://www.dafgiving360.org/tax-law-changes
- https://www.dafgiving360.org/maximize-your-impact/tax-calculator
- https://www.vanguardcharitable.org/charitable-tax-center
- https://www.vanguardcharitable.org/blog/charitable-bunching-under-obbba-when-it-makes-sense-and-when-it-doesnt
- https://www.svcf.org/about/news-media/blog/2026-tax-updates-what-advisors-should-know
- https://www.morganstanley.com/articles/donor-advised-funds-tax-benefits-for-charitable-giving
- https://www.aefonline.org/thought-leadership/charitable-bunching-for-financial-advisors/
- https://site.ncfgiving.com//wp-content/uploads/2026/08/OBBBA.pdf

**Pledge rules.** Listed per row in `daf-pledge-policy-2026-11-19.csv`. New this pass:
- https://www.fidelitycharitable.org/faqs/all/grant-pledge.html
- https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf
- https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf
- https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf
- https://www.ncfgiving.com/guide-to-giving-at-NCF
- https://policy.usc.edu/gift-acceptance-and-campaign-counting/
- https://www.northwestern.edu/financial-operations/policies-procedures/forms/pledgenon-binding-intent-transmittal.pdf
- https://giving.mit.edu/donor-advised-funds
- https://plannedgiving.mayoclinic.org/donor-advised-funds
- https://www.stjude.org/give/planned-giving/impact-major-gift/donor-advised-funds.html
- https://give.berkeley.edu/faq
- https://alumni.princeton.edu/princeton-university-gift-policies
- https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf
- https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf
- https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf
- https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf
