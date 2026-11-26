# P-G050303-02 and P-NPTREN-05: Assets Under Movement (Amalgamated Charitable Foundation) and NPT's $39.1m Europe line

**Date:** 2026-11-20 · **Task:** g050303-02 · **Queue items:**
- P-G050303-02, from [queue-proposals-g0503-03.csv](../../data/mission-2026-11-14/queue-proposals-g0503-03.csv);
- P-NPTREN-05, from [npt-ren-followups-2026-11-19.md](npt-ren-followups-2026-11-19.md) §3.3.

**Builds on:** [g0503-03-de-facto-fiscal-sponsors.md](g0503-03-de-facto-fiscal-sponsors.md). That note was being validated by another agent while this one was written; it was read but not edited. Its headline figures (5 added hosts, 190 lines, $114.6m; fiscal-sponsor share 0.47% / 2.06%) are reproduced exactly here (§2.3, row R/S0).

**Outputs**
- [`data/mission-2026-11-14/aum-npt-foreign-2026-11-20.csv`](../../data/mission-2026-11-14/aum-npt-foreign-2026-11-20.csv): 713 rows in long format (§6).
- [`scripts/mission_aum_npt_foreign.py`](../../scripts/mission_aum_npt_foreign.py): stdlib, functional style.
  - It imports `mission_de_facto_fiscal_sponsors.py`, `mission_exception_refined.py` and `mission_foreign_grants.py` unchanged. None of them was modified.
  - It rebuilds the refined and de facto flags with their own functions, exactly as `mission_de_facto_fiscal_sponsors.main` does.
  - Two runs gave byte-identical CSV and JSON summaries.
- [`data/mission-2026-11-14/queue-proposals-g050303-02.csv`](../../data/mission-2026-11-14/queue-proposals-g050303-02.csv): P-G05030302-01..06.

**Labels:** **[F]** filed value; **[C]** computed by the script; **[I]** inference or hand judgement.

**Framing.** As in the parent notes, a flag means a grant line would plausibly fall outside a sponsor's routine path. It does not mean the grant was improper.

---

## 0. Answers in brief

| Question | Answer |
|---|---|
| What AUM's own returns say | It is a **hybrid**: a DAF sponsor and a fiscal sponsor in one EIN [F].<br>- Part IV line 6 = 1 in FY2022, FY2023 and FY2024.<br>- Schedule D Part I: **187 DAFs** (FY2023) and **269** (FY2024).<br>- Part III names two programs: "Grantmaking to public charities … Donor advised funds and ACF's unrestricted funds are the principal sources" and "**Fiscally sponsored projects**". |
| DAF share of the organisation [C] | It depends on the basis:<br>- **Assets** (Schedule D line 1 ÷ Part X line 16): **0.205** (FY2023), **0.211** (FY2024);<br>- contributions (Schedule D line 2 ÷ Part VIII 1h): 0.345 → 0.949;<br>- grants (Schedule D line 3 ÷ Part IX lines 1–3): 0.475 → 0.977. |
| Is Schedule D reliable here? | **Not for FY2024 flows.** Opening DAF value $47.29m + contributions $369.78m − grants $229.63m gives $187.44m, but the filed closing value is $76.02m: a **−$111.42m gap** [C]. The FY2022 return checks Part IV line 6 but leaves Schedule D Part I blank [F]. |
| The $58.0m of top-50 lines | 58 lines from 24 filers. GS DAPF $19.56m, Fidelity $13.35m and SVCF $8.63m make up 72% [C].<br>Read with the filers' own purpose text:<br>- **38 lines, $54.26m (93.5%) are generic** ("For grant recipient's exempt purposes", "PUBLIC, SOCIETAL BENEFIT", "COMMUNITY & HUMAN SERVICES");<br>- **$3.67m (6.3%) explicitly names a project, pooled fund or fiscal sponsorship**: 7 FBO lines $1.06m; 10 named-fund lines $1.62m; one Seattle Foundation line, $1.0m, "RESOURCE EQUITY FUNDERS COLLABORATIVE FISCAL SPONSORSHIP.";<br>- **$0.10m explicitly says "Transfer to DAF"** (Boston Foundation, 2 lines). |
| DAF / non-DAF split of the $58.0m [C] | Each line × AUM's DAF share for that year. DAF-attributable amount:<br>- **$12.1m on assets**;<br>- $44.1m on contributions;<br>- $47.6m on grants.<br>Non-DAF remainder: **$45.9m / $13.95m / $10.4m**. |
| **Whitelist decision** [I] | **Keep AUM off the DAF-to-DAF whitelist and keep it in the de facto fiscal-sponsor set.** Report a hybrid-adjusted range beside the headline.<br>- It fails the repo's own rule W2 (DAF share of assets ≥ 0.5) in both years, at 0.205 and 0.211. The whitelist CSV already records it as `exclude` / W2 at 0.21.<br>- The only bases that pass (FY2024 contributions and grants) rest on a Schedule D that does not roll forward.<br>- The filer self-describes a fiscal-sponsorship program. |
| Effect on the de facto addition ($114.6m) [C] | - Headline (AUM in full): **$114.6m, 0.124%** of proxy dollars;<br>- AUM apportioned (non-DAF remainder only): **$102.5m (0.111%)** on assets, $70.5m (0.076%) on contributions, $67.0m (0.072%) on grants;<br>- AUM dropped: **$56.6m (0.061%)**. |
| Effect on the proxy shares, all top-50 itemising [C] | Lines / dollars:<br>- **Fiscal sponsor:** 0.47 / 2.06 (published) → 0.46 / 2.00 without AUM;<br>- **core:** 7.79 / 11.73 → 7.78 / 11.67;<br>- **broad:** 24.82 / 19.97 → 24.81 / 19.90;<br>- **broad ex-DAF-to-DAF:** 25.03 / 22.88 → 25.02 / 22.82 if AUM is whitelisted (whether or not it stays a fiscal-sponsor host);<br>- **DAF-to-DAF dollars:** $12.73bn → $12.79bn (14.02% → 14.09% of Schedule I dollars) if whitelisted.<br>Every move is ≤ 0.07 pp. |
| P-NPTREN-05: top-50 foreign grants with and without NPT's $39.1m line [C] | - **FY2024, the latest complete year:** $1,060.3m Part IX line 3. **Unchanged** either way: the line is in NPT's **FY2025** return (tax period ending 2025-06), not FY2024.<br>- **FY2025, 21 top-50 sponsors with a parseable return:** **$678.8m → $639.7m** without it (the line is 5.8%). Foreign share of grants 1.65% → 1.55%.<br>- **Latest available** (FY2025 where filed, else FY2024): **$1,013.1m → $974.0m** (3.9%); share of grants 1.67% → 1.60%.<br>- **NPT itself:** the line is 12.6% of its FY2025 Part IX line 3 ($310.5m). |

---

## 1. Method

### 1.1 AUM's own returns (A1)

- **Returns.** These are the IRS TEOS e-file index rows for EIN 821517696 with RETURN_TYPE 990:
  - FY2023 (tax period 2023-12): object 202413159349300006, index_2024, batch 2024_TEOS_XML_11A;
  - FY2024 (tax period 2024-12): object 202543179349307759, index_2025, batch 2025_TEOS_XML_11B;
  - FY2022 (tax period 2022-12): object 202302999349302215, used only for the roll-forward.
- **XML.** Local cached copies of the GivingTuesday mirror files. Files of 5,000 bytes or less are skipped (cached S3 error stubs; one was found for Vanguard's FY2025 return).
- **Fields read:**
  - Part I lines 5, 8, 12 and 13;
  - Part III (mission, program descriptions, expense and grant amounts);
  - Part IV line 6 (`DonorAdvisedFundInd`);
  - Part VII-B (five highest-paid contractors and the count over $100k);
  - Part IX lines 1, 3, 7, 11g and 25; Part X line 16;
  - Schedule D Part I lines 1–4 and 5–6 (`DonorAdvisedFunds*`, `FundsAndOtherAccounts*`, `DisclosedOrgLegCtrlInd`, `DisclosedForCharitablePrpsInd`);
  - Schedule I: count, $, the 501(c)(3) / other counts, top purposes, and outbound lines to recipients with `decision = include` in `daf-to-daf-recipient-whitelist.csv`;
  - Schedule F Part II; Schedule R names.
- **Fiscal-sponsorship language:** every text node matching `FISCAL(LY)? SPONSOR`.
- **Derived [C]:**
  - DAF share of assets = Schedule D line 1 EOY ÷ Part X line 16;
  - DAF share of contributions = Schedule D line 2 ÷ Part VIII line 1h;
  - DAF share of grants = Schedule D line 3 ÷ Part IX lines 1 + 3;
  - roll-forward = prior Schedule D line 1 EOY + line 2 − line 3. Investment returns and fees, which Schedule D Part I does not report, are left out, so small gaps are expected and large ones are not.

### 1.2 Top-50 lines to the EIN (A2)

- **Lines:** `mission_exception_refined.load_screened` (the unchanged `mission_exception_load` pipeline). That is 604,913 Schedule I lines, $90.81bn, from 94 itemising top-50 sponsor-years, with totals rows dropped. The lines to EIN 821517696 are selected.
- **Purpose text:** read from each filer's own Schedule I XML (`PurposeOfGrantTxt`, `RecipientTable` rows with this EIN) and matched to the cached line by amount and name.
  - 53 lines came from local copies;
  - 5 lines (two filer returns) came from the mirror.
- **Evidence class**, first match wins:
  1. `project_style_fbo`: the line is a valid de facto detection (`mission_de_facto_fiscal_sponsors.detect`);
  2. `purpose_fiscal_sponsorship`: the purpose matches `FISCAL(LY)? SPONSOR`;
  3. `purpose_daf`: DONOR ADVISED or DAF;
  4. `purpose_named_fund`: FUND, COLLABORATIVE, INITIATIVE or PROJECT, after the generic phrases ANNUAL FUND / GENERAL FUND / PROJECT SUPPORT are removed;
  5. else `generic`.

### 1.3 Apportionment and scenarios (A3, A4)

- **Apportionment:** DAF-attributable $ = Σ line × AUM's DAF share for the filer's fiscal year, on each of the three bases. FY2023 lines use AUM's calendar-2023 return and FY2024 lines its calendar-2024 return. The remainder is non-DAF: fiscally sponsored projects, pooled funds and unrestricted funds.
- **Scenarios** re-cut the pooled tallies with `mission_exception_load.tally / add / shares`, Schedule F unchanged, proxy denominator 608,610 lines / $92.72bn:

  | Scenario | AUM fiscal-sponsor host? | AUM lines DAF-to-DAF? |
  |---|---|---|
  | R | no (refined flag as published in g0503-0501) | no |
  | S0 | yes (published de facto addition) | no |
  | S1 | no (the other 4 hosts stay added) | no |
  | S2 | no | yes |
  | S3 | yes (the Tides Foundation precedent: whitelisted and a fiscal-sponsor host) | yes |

- "Whitelisted" sets the line's `d2d` mark, exactly as an `include` row in the whitelist would through `annotate`.
- The dollar apportionment cannot be expressed in line counts, so it is reported only for the addition and for DAF-to-DAF dollars.

### 1.4 Foreign-grant totals (B)

- **FY2024:** the unchanged `scope_total / all_top50` row of `daf-foreign-grants-schedule-f-2023-2024.csv`.
- **FY2025:**
  - For each of the 50 top-50 EINs (`mission_daf_to_daf.top_n`), the latest-filed Form 990 with a tax period ending in calendar 2025 is taken from the IRS TEOS index files for 2025 and 2026.
  - Each is parsed with `mission_foreign_grants.load_extract / parse_return`: Part IX lines 1–3 and Schedule F Parts I–III.
  - Local copies are used first, then the mirror.
- **"Without the line":** $39,100,000 is subtracted from NPT's line 3 and Schedule F Part II. For shares of grants it is also subtracted from the denominator.
- The NPT line is verified in the parsed Part II: exactly one $39,100,000 row in FY2025, and none in FY2024.

## 2. Results: Assets Under Movement / Amalgamated Charitable Foundation

### 2.1 What its returns say [F unless marked]

| | FY2022 | FY2023 | FY2024 |
|---|---|---|---|
| Filer name (ReturnHeader) | Amalgamated Charitable Foundation Inc | same | same |
| Part IV line 6, DAF indicator | 1 | 1 | 1 |
| Schedule D Part I: DAFs held | **blank** | 187 | 269 |
| … aggregate contributions to DAFs | blank | $93,060,261 | $369,775,798 |
| … aggregate grants from DAFs | blank | $86,444,499 | $229,628,145 |
| … DAF value, end of year | blank | $47,293,434 | $76,017,807 |
| … other funds (lines 5–6 columns (b)) | — | blank | blank |
| Part VIII line 1h, contributions | — | $270,017,753 | $389,741,054 |
| Part IX lines 1 + 3, grants | — | $181,945,881 | $234,944,291 (of which foreign $456,000) |
| Part X line 16, total assets | $160,739,477 | $230,908,898 | $361,053,663 |
| Program expense excluding grants (Part III line 4a) [C] | — | $22,198,861 | $26,816,136 |
| Employees (Part I line 5) | — | 40 | 76 |
| Contractors over $100k (Part VII-B) | — | 29 | 52 |
| Schedule I lines (501(c)(3) / other) | — | 1,429 (1,413 / 16), $180.4m | 1,804 (1,786 / 18), $230.9m |
| … to DAF-to-DAF whitelist sponsors | — | 21 lines, $4.43m (Tides Foundation $3.14m) | 28 lines, $5.95m (Tides Foundation $3.66m; ImpactAssets $0.52m) |
| Schedule F Part II | — | none filed | 9 lines, $456,000 |
| **DAF share of assets** [C] | — | **0.205** | **0.211** |
| DAF share of contributions [C] | — | 0.345 | 0.949 |
| DAF share of grants [C] | — | 0.475 | 0.977 |
| Schedule D roll-forward gap [C] | — | n/a (FY2022 blank) | **−$111,423,280** |

**Fiscal-sponsorship language.** Part III, identical in both years: "Grantmaking to public charities: … Donor advised funds and ACF's unrestricted funds are the principal sources of grantmaking activity … **Fiscally sponsored projects:** These are engaged in furtherance of the mission through the following ways: social change, democracy, economic equality, and climate & sustainability."
- No other text node mentions fiscal sponsorship. Schedule O has no program note.
- The five highest-paid contractors are all described as "Project consulting" / "Project Consulting":
  - FY2023: Guidehouse Netherlands BV $3,844,135; AB Partners $1,180,600; Social Strategy Associates $769,873; Goldman-Fitzgerald LLC; Camber Collective LLC;
  - FY2024: RALLY $1,569,052; Nelson Mullins Riley & Scarborough LLP $1,254,697; Social Strategy Associates; Goldman-Fitzgerald; HR&A Advisors.

**Related organisations.** Schedule R lists Amalgamated Bank (EIN 13-4920330) in both years. Schedule D Part I line 5 (`DisclosedOrgLegCtrlInd`) = 1 and line 6 = 1 in both years: donors are told in writing that the organisation has legal control of the DAF assets and that they may be used only for charitable purposes.

**Reading [I]**
- On assets, about four-fifths of AUM's balance sheet sits outside DAFs in both years. That fits a host whose fiscally sponsored projects and pooled funds hold most of the money.
- On flows, FY2024 looks almost entirely DAF: 95% of contributions and 98% of grants. But the closing DAF balance is $111m below what those flows imply. This is consistent with DAF balances being moved to projects or pooled funds as internal transfers that Schedule D does not report as grants, or with a reclassification. The balance sheet points the same way: FY2024 net assets rose $130.8m while the filed DAF value rose $28.7m, so non-DAF net assets grew about $102.0m, against only $14.6m of non-DAF contributions less grants implied by Schedule D. Most of the gap therefore sits in non-DAF funds, which favours the assets basis. [V wave 44B] The returns do not say which (P-G05030302-01).
- Staff (40 → 76), program spending beyond grants ($22–27m) and project-consulting contracts show an operating fiscal-sponsorship business, not a pure grant pass-through.

### 2.2 The $58.0m of top-50 lines [C]

| Filer | Lines | $ | Purpose as filed (examples) |
|---|---|---|---|
| GS Donor Advised Philanthropy Fund | 2 | 19,559,700 | COMMUNITY & HUMAN SERVICES |
| Fidelity Charitable | 2 | 13,349,491 | For grant recipient's exempt purposes |
| Silicon Valley Community Foundation | 2 | 8,633,700 | General Nonprofit Support |
| NPT | 2 | 3,850,531 | PUBLIC, SOCIETAL BENEFIT |
| DAFgiving360 (Donor Advised Charitable Giving) | 2 | 3,257,474 | PUBLIC, SOCIETAL BENEFIT |
| Greater Houston CF | 2 | 2,161,856 | PUBLIC BENEFIT |
| ImpactAssets | 10 | 1,865,695 | 7 "AMALGAMATED … FBO <fund>" lines; THE KINDLE PROJECT; GENERAL SUPPORT |
| Seattle Foundation | 6 | 1,742,653 | RESOURCE EQUITY FUNDERS COLLABORATIVE FISCAL SPONSORSHIP.; HIGHER EDFORWARD FUND; IGNITE 2024 FUND; TEACHING EXCELLENCE FUND |
| New York Community Trust | 4 | 1,088,160 | FOR PROGRAM SUPPORT. |
| 15 other filers | 26 | 2,524,603 | e.g. "Transfer to DAF" (Boston Foundation); "The Emergent Fund" (Chicago CT); "KINDLE PROJECT / INDIGENOUS WOMEN'S FLOW FUND" (San Diego) |
| **Total** | **58** | **58,033,863** | |

| Evidence class | Lines | $ |
|---|---|---|
| generic | 38 | 54,259,515 |
| purpose_named_fund | 10 | 1,619,348 |
| project_style_fbo | 7 | 1,055,000 |
| purpose_fiscal_sponsorship | 1 | 1,000,000 |
| purpose_daf | 2 | 100,000 |

- None of the 58 lines is DAF-to-DAF today. None carries another refined exception flag, so all 58 enter the core union only through the de facto addition.
- The pooled funds named are Emergent Fund, Families and Workers Fund, Maui Just Recovery Fund, New Sheriff in Town Fund, Missouri Democracy Education Fund, Way to Rise, Resource Equity Funders Collaborative, Youth Power Fund / Way to Win Philanthropic Fund and others.
- These are funder collaboratives or projects hosted by AUM. Their legal form (fiscally sponsored project or donor-collaborative fund) is not stated in any filing [I].

### 2.3 Apportionment and effect on the proxy [C]

**DAF / non-DAF split of the $58,033,863:**

| Basis | DAF-attributable | Non-DAF remainder | De facto addition (4 hosts + remainder) | Share of proxy $ | DAF-to-DAF $ (share of Schedule I $) |
|---|---|---|---|---|---|
| Published (AUM in full as fiscal sponsor) | 0 | 58,033,863 | **114,592,875** | 0.124% | 12,732.4m (14.02%) |
| DAF share of assets (W2 basis) | 12,114,572 | 45,919,291 | **102,478,303** | 0.111% | 12,744.5m (14.03%) |
| DAF share of contributions | 44,082,463 | 13,951,400 | 70,510,412 | 0.076% | 12,776.5m (14.07%) |
| DAF share of grants | 47,593,379 | 10,440,484 | 66,999,496 | 0.072% | 12,780.0m (14.07%) |
| AUM dropped / fully whitelisted | 58,033,863 | 0 | **56,559,012** | 0.061% | 12,790.4m (14.09%) |

**Union re-cut, all top-50 itemising (94 sponsor-years), line / dollar shares in %:**

| Scenario | Fiscal sponsor | Core | Broad | Broad ex-DAF-to-DAF | DAF-to-DAF $ |
|---|---|---|---|---|---|
| R refined as published | 0.44 / 1.94 | 7.76 / 11.61 | 24.79 / 19.85 | 25.00 / 22.74 | 12,732.4m |
| **S0 published de facto** | **0.47 / 2.06** | **7.79 / 11.73** | **24.82 / 19.97** | **25.03 / 22.88** | 12,732.4m |
| S1 AUM dropped | 0.46 / 2.00 | 7.78 / 11.67 | 24.81 / 19.90 | 25.02 / 22.80 | 12,732.4m |
| S2 AUM whitelisted, dropped | 0.46 / 2.00 | 7.78 / 11.67 | 24.81 / 19.90 | 25.02 / 22.82 | 12,790.4m |
| S3 AUM whitelisted, kept | 0.47 / 2.06 | 7.79 / 11.73 | 24.82 / 19.97 | 25.02 / 22.82 | 12,790.4m |

**Fiscal-sponsor $ share by sponsor type, S0 → S1:**
- Big-4 nationals: 2.15 → 2.11;
- national: 2.24 → 2.17;
- community foundation: 1.77 → 1.69;
- faith: 2.02 → 2.02, since faith sponsors filed no line to AUM.

The full scenario × scope grid is in the CSV (`proxy_scenario` rows).

### 2.4 Decision [I]

1. **Not on the DAF-to-DAF whitelist.**
   - The whitelist rule W2 tests DAF share of assets against 0.5, and AUM's own returns give 0.205 and 0.211. The whitelist CSV already excludes it on that test (0.21).
   - Moving it would need a rule change for hybrids, not a correction of a misclassified sponsor. Several other W2 exclusions have the same profile: high DAF share of grants, low share of assets (P-G05030302-02).
   - The filer-side evidence does not support whitelisting either. Only $0.10m of the $58.0m is labelled "Transfer to DAF", against $3.67m that names projects, pooled funds or fiscal sponsorship.
2. **Keep it in the de facto fiscal-sponsor set**, now on three kinds of evidence: the filers' FBO lines, the filer's own Part III ("Fiscally sponsored projects"), and the Seattle Foundation purpose text ("… FISCAL SPONSORSHIP.").
3. **But report the hybrid range.** Under the EIN-keyed rule every AUM line counts as fiscal-sponsor flow, which overstates it. The defensible statement is:
   - de facto addition **$114.6m headline**;
   - **$102.5m on the assets basis**: AUM’s non-DAF remainder at its W2 share. The $67.0m and $70.5m flow-based variants rest on the FY2024 Schedule D that does not roll forward and are sensitivities only. All of these sit inside the validated wave-43B range of $35.1m–$114.6m, whose low end drops all three DAF-sponsor hybrids. The non-DAF remainder also holds AUM’s pooled and unrestricted funds, so it is an upper bound on fiscal-sponsorship flow. [V wave 44B] The assets basis is preferred because it is the W2 basis and does not depend on the broken FY2024 Schedule D flows;
   - **$56.6m floor** without AUM.
   - Every variant leaves the core union at 7.78–7.79% of lines and 11.67–11.73% of dollars.
4. The choice is **immaterial to the headline proxy**: ≤ 0.07 pp on every pooled share, and ≤ 0.09 pp on any sponsor-type share (the largest move is community foundations' broad ex-DAF-to-DAF dollar share).

## 3. Results: NPT's $39.1m Europe line (P-NPTREN-05)

### 3.1 The line, as filed [F/C]

- **NPT FY2025** (tax period ending 2025-06-30; object 202601289349302480; IRS TEOS index_2026, batch 2026_TEOS_XML_05A):
  - Part IX line 3: $310,506,570;
  - Schedule F Part II: 560 lines, $310,238,950;
  - Europe: 411 lines, $154,427,213.
- **The candidate:** exactly one Part II row of $39,100,000: "EUROPE (INCLUDING ICELAND AND GREENLAND) | ENVIRONMENT, ANIMALS | WIRE TRANSFER".
  - It is the largest line; the next are $16,770,000 (Middle East and North Africa) and $12,080,347 (Europe).
  - It is **12.59%** of line 3 [C], which matches §3.3 of the parent note.
- **Carried as:** a *flagged candidate affiliate transfer* (NPT → NPT UK, £30.939m), not proven. The parent's verdict and caveats stand: the return names no recipient and the purpose label fits poorly.
- **NPT FY2024** (tax period ending 2024-06; object 202511339349301311):
  - line 3 $410,629,568; Part II 488 lines, $410,303,258;
  - no $39.1m row;
  - largest Europe row $25,000,000 by wire. In this year NPT filed the purpose ("INTERNATIONAL") in the manner-of-disbursement field and "WIRE TRANSFER" in the valuation field. `mission_foreign_grants.py` already treats the manner as wire for NPT FY2024.
  - Read as a £30.939m transfer, $25.0m would imply 0.808 $/£ [C]. So the FY2024 return holds no single-line candidate either.

### 3.2 Top-50 foreign-grant totals with and without the line [C]

| Scope | Sponsors | Part IX line 3, with | without | Line's share | Schedule F Part II, with → without | Foreign share of grants, with → without |
|---|---|---|---|---|---|---|
| **FY2024, all top-50 (latest complete year)** | 50 | **$1,060,331,109** | **$1,060,331,109** | 0 (line is FY2025) | $1,059.9m → $1,059.9m | 1.957% → 1.957% |
| FY2025, top-50 with a parseable FY2025 return | 21 | **$678,845,354** | **$639,745,354** | 5.76% | $676.4m → $637.3m | 1.648% → 1.554% |
| Latest available (FY2025 for 21, FY2024 for 29) | 50 | **$1,013,139,699** | **$974,039,699** | 3.86% | $1,011.6m → $972.5m | 1.666% → 1.603% |

- **FY2025 coverage.** 24 of the 50 top-50 sponsors have a FY2025 Form 990 (tax period ending in 2025) in the TEOS index files for 2025–2026. The other 26 are mainly calendar-year filers whose returns for December 2025 are not yet posted.
- Three of the 24 returned HTTP 404 on the mirror: Boston Foundation, Jewish Community Federation of San Francisco and UCLA Foundation (P-G05030302-04). All three are in the IRS TEOS bulk file 2026_TEOS_XML_05B. Adding them gives 24 sponsors with $687.8m on line 3 with the NPT line and $648.7m without it (the line is 5.68%); the foreign share of grants is 1.634% with the line and 1.543% without. [V wave 44B]
- The same 21 sponsors filed $726.0m on line 3 in FY2024. Their FY2025 total is lower, even with the NPT line, mainly because NPT fell from $410.6m to $310.5m.
- The splice mixes years and is shown only because the task asks for the latest available data. The like-for-like figures are the FY2024 row and the FY2025 subset.

## 4. Limits

- **Schedule D is internally inconsistent for AUM.** The FY2024 roll-forward misses by $111.4m, and FY2022 Part I is blank despite Part IV line 6 = 1. The contributions and grants bases are therefore weak. The assets basis is a point-in-time stock and says nothing about which inflows went where.
  - The DAFRC panel values for AUM (e.g. FY2024 $63.1m and 195 accounts in `sponsor-cost-structure.csv`) differ from the filed Schedule D ($76.0m, 269). They were not used.
- **Apportionment is a proxy.** It assumes each inbound grant splits like AUM's aggregate flows or stocks. Grants from other DAF sponsors could be much more (DAF-to-DAF transfers) or much less (support for named pooled funds) DAF-bound than the average. Line purposes are generic for 93.5% of dollars, so they cannot settle it.
- **Purpose matching.** Lines were matched to the filers' `RecipientTable` rows by amount and name. All 58 matched; 5 purposes came from mirror copies of two filer returns.
- **Evidence classes** are keyword rules. "THE KINDLE PROJECT" (an ImpactAssets plain-name line, $457k) counts as named fund / project; "Operating Support/Annual Fund" counts as generic.
- **No AUM web pages, audited statements or Candid profile were read.** The name change to Assets Under Movement is taken from the 2026-11 BMF only, as in the parent note.
- **FY2025 foreign totals are partial**, 21 of 50 sponsors, and the splice mixes years.
- **The NPT line remains a candidate.** No document ties it to NPT UK (P-G05030302-06).
- All limits of the parent notes apply: recipient-level Schedule I and attachment-only sponsors.

## 5. Reproduction

```
python3 scripts/mission_aum_npt_foreign.py . --np-cache NPCACHE --lines-cache LINES --bmf-dir BMF \
    --pub78 data-download-pub78.txt --revocation data-download-revocation.txt --efile-index-dir IRS \
    --bmf-archive-dir ARCH --fsd-html all-fiscal-sponsors-alpha-ordered.html --extract-cache EC \
    --xml-dir DIR [--xml-dir DIR ...] --fetch [--out CSV]
```

- The inputs are those of `mission_de_facto_fiscal_sponsors.py`, plus:
  - `--extract-cache`: a scratch directory for `mission_foreign_grants` extracts;
  - `--xml-dir`: local copies of e-file XML;
  - `--fetch`: GivingTuesday mirror for files not held locally.
- Run time is about 3 minutes. The JSON summary on stdout holds every figure quoted here.
- **Web requests:** GivingTuesday mirror only (`gt990datalake-rawdata.s3.amazonaws.com`).
  - Its robots.txt returned HTTP 404 (NoSuchKey) on 2026-11-20, so no rules apply; this was logged.
  - User agent `research-script/1.0 (stdlib urllib)`.
  - sec.gov was not used.

## 6. Data dictionary: `aum-npt-foreign-2026-11-20.csv` (713 rows)

Long format: one value per row.

| Column | Meaning |
|---|---|
| row_type | `aum_return` (filed value from AUM's 990), `aum_fiscal_text` (text node mentioning fiscal sponsorship), `aum_derived` (computed share or roll-forward), `aum_whitelist` (AUM's row in the whitelist CSV), `aum_inbound_line` (one top-50 Schedule I line to EIN 821517696), `aum_inbound_summary`, `aum_inbound_by_class`, `aum_inbound_by_sponsor`, `aum_apportion`, `proxy_scenario`, `de_facto_addition`, `npt_sched_f`, `foreign_totals`, `foreign_fy2025_sponsor` |
| section | A1–A4 (AUM parts, §1) or B (foreign grants) |
| scope | `aum`, `npt`, a filer name (inbound lines), a sponsor scope (`all_top50_itemising`, `big4_nationals`, `national`, `community_foundation`, `faith`), a foreign-total scope (`all_top50`, `top50_with_fy2025_return`, `all_top50_latest_available`), an evidence class, or a sponsor EIN |
| fiscal_year | Fiscal year (calendar year in which the tax period ends), or a range / splice label |
| metric | Field name. In `proxy_scenario` rows it is `<scenario>__<measure>`, where measure is one of `mission_exception_load.shares` keys plus `d2d_usd`. In `de_facto_addition` rows: `<variant>__<measure>` or `apportioned__<basis>__<measure>`. Inbound lines: `line_<filer EIN>_<line index>` |
| value | The value. Shares are fractions (0.0206 = 2.06%); dollars are rounded to $1. Pipe-joined where the metric is pipe-joined (e.g. `lines\|usd`) |
| unit | usd, share, count, flag, text, date (pipe-joined to match `value` when needed) |
| detail | Notes. For `aum_inbound_line` a JSON object: filed_name, purpose (filer's PurposeOfGrantTxt), evidence_class, fbo_detection, d2d, refined_flags, purpose_via (local / mirror) |
| evidence | F filed, C computed, F/C both |
| source_url | GivingTuesday mirror URL of the return the value comes from (blank for repo-derived values) |

## 7. Source register

| ID | Source | Version / access | robots.txt |
|---|---|---|---|
| S1 | AUM Form 990s, e-file XML (IRS TEOS via the GivingTuesday mirror): [FY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413159349300006_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543179349307759_public.xml), [FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202302999349302215_public.xml) | cached copies (scratch), read 2026-11-20 | 404 (no rules), logged 2026-11-20 |
| S2 | IRS TEOS e-file indexes: [index_2024.csv](https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv), [index_2025.csv](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv), [index_2026.csv](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv); [IRS Form 990 series downloads](https://www.irs.gov/charities-non-profits/form-990-series-downloads) | cached copies used by earlier tasks | per parent notes |
| S3 | NPT Form 990s: [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml) | cached copies | as S1 |
| S4 | FY2025 Form 990s of 21 top-50 sponsors (URLs in `foreign_fy2025_sponsor` rows) | 13 local, 8 fetched from the mirror on 2026-11-20 | as S1 |
| S5 | Top-50 filers' FY2023–24 Schedule I XML, for purpose text on the 58 AUM lines (URLs in `aum_inbound_line` rows) | 53 lines local, 5 from the mirror | as S1 |
| S6 | Repo inputs, unchanged:<br>- line cache and DAFRC panel (`mission_exception_load` pipeline);<br>- `daf-to-daf-recipient-whitelist.csv`;<br>- `daf-foreign-grants-schedule-f-2023-2024.csv`;<br>- `sponsor-cost-structure.csv` (comparison only);<br>- EO BMF / Pub 78 / revocation / BMF archive / Fiscal Sponsor Directory cache, as in [g0503-03](g0503-03-de-facto-fiscal-sponsors.md) §6 | repo / scratch caches | per parent notes |
| S7 | IRS instructions for [Schedule D](https://www.irs.gov/pub/irs-pdf/i990sd.pdf) (Part I lines 1–6) and [Schedule F](https://www.irs.gov/pub/irs-pdf/i990sf.pdf) | referenced for field meanings; not re-fetched | — |
