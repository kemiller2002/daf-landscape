# Schedule I grant-purpose panel: top-50 DAF sponsors, FY2024 (P-B40N13-01)

Date: 2026-11-19. Script: `scripts/mission_grant_purpose_panel.py`. Data: `data/mission-2026-11-14/grant-purpose-panel-2026-11-19.csv`. Queue proposals: `data/mission-2026-11-14/queue-proposals-b40n13-01.csv`.

Tags: [F] filed fact (read from the XML), [C] computed by the script, [I] inference.

## 0. Bottom line

- **Schedule I purpose text says almost nothing about donor restrictions [C].** Across the 48 top-50 sponsors that itemise FY2024 grants (322,773 lines, $49.49bn), 54.6% of lines (51.1% of dollars) carry generic boilerplate. Another 43.7% of lines (46.3% of dollars) carry a sector label such as "HUMAN SERVICES" or "RELIGION RELATED". Only **1.2% of lines (1.8% of dollars)** name a specific, restricted-sounding use. Blank purposes are negligible: 5 lines, although one blank Greater Horizons line holds $212.2m.
- **Each sponsor uses one of three regimes, and the regime fixes the answer [C].**
  - **One string on more than 90% of lines: 19 sponsors.** Fidelity Charitable uses "FOR GRANT RECIPIENT'S EXEMPT PURPOSES" on all 80,308 lines. Vanguard Charitable, Morgan Stanley GIFT, ImpactAssets, Raymond James, T. Rowe Price ("MULTIPLE"), the Chicago Community Trust and others do the same.
  - **A sector taxonomy: 20 sponsors,** including NPT, DAFgiving360, Goldman Sachs DAPF, SVCF and NCF.
  - **Mostly boilerplate plus some free text, or mixed free text: 9 sponsors.** Seven are mostly boilerplate (five community foundations, Donors Trust and Bessemer); two are mixed (NYCT and Stanford).
- **By sponsor type [C]:**
  - **Nationals (16):** 0.07% of lines have a specific purpose. The median national puts 97.2% of its lines under boilerplate.
  - **Community foundations (22):** 7.7% of lines and 4.3% of dollars have a specific purpose. Eight of the ten sponsors with at least 5% specific lines are community foundations.
  - **Single-issue sponsors (7):** 0.9% of lines, mostly sector labels.
- **The repo's restriction claims are neither supported nor contradicted by Schedule I [I].** Several sponsors say in their own Schedule I narratives that restricted grants exist, and NPT says unrestricted is its default. Their purpose columns still do not show which grants carry restrictions (§5).

## 1. Question and scope

The task was to build, for each top-50 DAF sponsor's latest return (FY2024), a profile of the Schedule I Part II column (h) "purpose of grant" (`PurposeOfGrantTxt`). The profile covers distinct strings, boilerplate share, specific/restricted share and blank share, by lines and by dollars. It is then reported by sponsor type and tested against the repo's claims about restricted grants and "general support".

## 2. Method

1. **Universe.** The universe is the one used in `scripts/mission_recipient_sectors.py`: the top 50 DAFRC sponsors by FY2024 DAF assets. Each sponsor has one FY2024 return, chosen by `mission_daf_to_daf.pick_returns` over the `netpayout990/` cache.
   - Two sponsors file no itemised Schedule I for FY2024: Bank of America Charitable Gift Fund and Renaissance Charitable Foundation. Each has one line, and both fail `mission_net_payout.itemized`.
   - That leaves **48 sponsors**.
2. **Re-parse.** The Schedule I line cache (`rcp/lines`, format `[ein, name, where, irc, cash, noncash]`) has no purpose field. The script therefore re-reads every `RecipientTable` in the same 48 e-file XMLs and keeps `PurposeOfGrantTxt`.
   - 21 XMLs were already on disk. The other 27 were downloaded from the GivingTuesday mirror of IRS TEOS (`gt990datalake-rawdata.s3.amazonaws.com`) into the session scratchpad. That host's robots.txt returns 404 (no rules); see §9.
   - **Check:** every one of the 48 re-parses matches the line cache on line count and on dollar total (`cache_check` = "yes" on all 48 rows).
   - The script also keeps every `SupplementalInformationDetail` narrative inside `IRS990ScheduleI` (Part I line 2 and Part IV) and flags any that mention restriction.
3. **Normalise.** Each purpose string is upper-cased, curly apostrophes are straightened, and whitespace is collapsed. "Distinct purposes" counts the distinct non-blank normalised strings per sponsor.
4. **Classify.** Each line is classified with the ordered keyword rules in §2.1; the first rule that fires wins. Line amount = cash + non-cash.
5. **Roll up.**
   - **boilerplate** = the four `boiler_*` classes. **specific** = `specific_capital` + `specific_program`.
   - **`boilerplate_incl_modal`** also counts any string carried by more than 90% of a sponsor's lines. In this panel every such string is already boilerplate, so the two measures are equal.
   - Shares are reported for each sponsor, for each segment (pooled lines) and as the median sponsor share.
6. **Regime** (per sponsor):
   - `single_string_*`: the top string is on more than 90% of lines;
   - `sector_taxonomy`: at least 60% of lines are sector labels;
   - `mostly_boilerplate_with_free_text`: at least 50% of lines are boilerplate;
   - `free_text_mixed`: anything else.

### 2.1 Published classification rules

The rules are applied in this order; the patterns are copied from `RULES` in the script.

| # | Class | Rollup | Fires when (regex on the normalised string) |
|---|---|---|---|
| 1 | `blank` | blank | `^(\|0\|N/?A\|NONE\|-+\|\.)$` |
| 2 | `boiler_unrestricted` | boilerplate | `\bUNRESTRICTED\b` |
| 3 | `boiler_aggregate` | boilerplate | `^(MULTIPLE\|VARIOUS)\b` (grouped grants) |
| 4 | `specific_capital` | specific | `SCHOLARSHIP\|FELLOWSHIP\|\bENDOW\|\bCAPITAL\b\|\bBUILDING (FUND\|CAMPAIGN\|PROJECT)\|\bCONSTRUCTION\b\|\bRENOVAT\|\bFACILIT(Y\|IES)\b\|\bEQUIPMENT\b\|\bPROFESSORSHIP\b\|\bCHAIR\b\|(?<!ANNUAL )\bCAMPAIGN\b\|\bTUITION\b\|\bPRESERVATION OF\b` |
| 5 | `boiler_general` | boilerplate | `\bGENERAL (SUPPORT\|OPERATING\|OPERATIONS?\|OPERATIONAL\|PURPOSES?\|FUND\|NONPROFIT\|USE\|CHARITABLE\|PHILANTHROPY\|GRANT)\b`, a bare "GENERAL" (optionally prefixed "DONOR-ADVISED,"/"DAF -"), `OPERATING`, `OPERATIONS?`, `OPERATIONAL`, `ANNUAL (FUND\|GIVING\|CAMPAIGN\|APPEAL\|SUPPORT\|GIFT)`, a bare "(FOR/TO) (PROVIDE) SUPPORT", `WHERE (MOST )?NEEDED`, `(HIGHEST\|GREATEST) NEED` |
| 6 | `boiler_exempt` | boilerplate | `EXEMPT`, `CHARITABLE (PURPOSE\|GIFT\|CONTRIBUTION\|DONATION\|GRANT\|USE\|ACTIVIT)`, a bare "(in/to) (support) (of) (the) (organization's) MISSION", `MISSION SUPPORT`, or a whole string equal to CHARITABLE / DONATION / CONTRIBUTION / GIFT / GRANT / DONOR ADVISED GRANT / DAF GRANT / PHILANTHROPIC / PUBLIC CHARITY |
| 7 | `category_label` | sector label | Split on spaces and `, / & ( ) - : ; .`. Drop the stop tokens {AND, OR, OF, THE, &, DAF, DONOR, ADVISED, DONOR-ADVISED, RELATED, NEC, N.E.C., N, E, C, GENERAL, TO, A, W} and NTEE-style codes (`X?\d+`). The rule fires if 1–10 tokens remain and **every** token is in the 276-word sector vocabulary `CATEGORY_WORDS` in the script (e.g. EDUCATION, RELIGION, HUMAN, SERVICES, HEALTH, ARTS, CULTURE, ENVIRONMENT, ANIMALS, MINISTRY, YOUTH, DEVELOPMENT …) |
| 8 | `specific_program` | specific | `PROGRAMS?`, `PROJECTS?`, `RESEARCH`, `INITIATIVE`, `EVENT`, `GALA`, `SPONSOR`, `TICKET`, `AUCTION`, `GOLF`, `TOURNAMENT`, `DINNER`, `LUNCHEON`, `RELIEF`, `EMERGENCY`, `HURRICANE`, `WILDFIRE`, `FIRE`, `EARTHQUAKE`, `UKRAINE`, `ISRAEL`, `GAZA`, `MEMORY`, `MEMORIAL`, `HONOR`, `TRIBUTE`, `FUND`, `^FOR THE`, `AWARD`, `PRIZE`, `TRIP`, `CAMP`, `CONFERENCE`, `EXHIBIT` |
| 9 | `other_descriptive` | other | no rule fired |

Design choices, and how each one moves the numbers:

- **`specific_capital` runs before `boiler_general`.** A string such as "GENERAL SUPPORT – SCHOLARSHIP" therefore counts as specific.
- **Sector labels run before `specific_program`.** Taxonomy codes such as "DISASTER RELIEF" (AEF) or "YOUTH DEVELOPMENT PROGRAMS" (Denver) are labels, not restrictions.
- **"FOR PROGRAM SUPPORT." is specific.** It is NYCT's largest string (1,317 lines); if it were treated as generic, NYCT's specific share would fall from 56.7% to about 8.8% of lines.
- **"CHARITABLE PROJECT" is specific.** Goldman Sachs DAPF and Ayco use it as a taxonomy code (88 lines). It is kept as specific, which slightly overstates the national specific share.
- **Upper bound.** If every `other_descriptive` line were also treated as specific, the pooled specific share would rise from 1.17% to 1.75% of lines.
- **Audit file.** Every (sponsor, string, class, lines, $) row is in the audit file the script writes with `--audit`, so any class assignment can be checked.

## 3. Results

### 3.1 Pooled and by sponsor type [C]

"Boilerplate" here includes the more-than-90% modal-string overlay, which adds nothing in this panel. "Distinct strings" is counted across sponsors after normalisation.

| Scope | Sponsors | Lines | $m | Distinct strings | Boilerplate lines | Boilerplate $ | Specific lines | Specific $ | Sector label lines | Other lines | Blank lines | Median sponsor boilerplate lines | Median sponsor specific lines |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all_top50_itemising | 48 | 322,773 | 49,494.6 | 3707 | 54.6% | 51.1% | 1.2% | 1.8% | 43.7% | 0.6% | 0.0% | 61.9% | 0.0% |
| all_ex_university_hospital | 46 | 322,579 | 48,977.0 | 3668 | 54.6% | 51.4% | 1.1% | 1.0% | 43.7% | 0.6% | 0.0% | 61.9% | 0.0% |
| community_foundation | 22 | 42,607 | 8,451.5 | 3138 | 45.8% | 59.2% | 7.7% | 4.3% | 42.6% | 4.0% | 0.0% | 49.6% | 0.0% |
| national | 16 | 252,323 | 35,489.3 | 114 | 58.6% | 51.4% | 0.1% | 0.1% | 41.4% | 0.0% | 0.0% | 97.2% | 0.0% |
| processor | 1 | 6 | 552.3 | 1 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% |
| single_issue | 7 | 27,643 | 4,483.7 | 471 | 32.0% | 30.8% | 0.9% | 1.7% | 66.6% | 0.5% | 0.0% | 57.8% | 0.0% |
| university_hospital | 2 | 194 | 517.6 | 43 | 58.2% | 20.2% | 29.4% | 77.5% | 2.6% | 9.8% | 0.0% | 67.4% | 22.8% |

Class mix, all 48 sponsors pooled (lines / dollars) [C]:

| Class | Lines | Share of lines | Share of $ |
|---|---|---|---|
| `boiler_exempt` ("exempt purpose", "charitable gift" …) | 117,946 | 36.5% | 35.0% |
| `boiler_general` ("general support", "operations" …) | 34,975 | 10.8% | 11.9% |
| `boiler_unrestricted` | 19,292 | 6.0% | 3.6% |
| `boiler_aggregate` ("MULTIPLE …") | 3,984 | 1.2% | 0.6% |
| `category_label` (sector code) | 140,947 | 43.7% | 46.3% |
| `specific_capital` | 1,175 | 0.36% | 1.04% |
| `specific_program` | 2,593 | 0.80% | 0.74% |
| `other_descriptive` | 1,856 | 0.58% | 0.34% |
| `blank` | 5 | 0.002% | 0.43% |

Taken together, 98.2% of lines and 97.9% of dollars carry text that cannot reveal a use restriction: boilerplate, sector labels, aggregates or blanks.

### 3.2 By sponsor [C]

Shares are line share / dollar share. Rank is the FY2024 DAF-asset rank; ranks 9 and 11 do not itemise.

| Rank | Sponsor | Segment | Lines | $m | Distinct | Top string (line share) | Boilerplate lines / $ | Specific lines / $ | Sector label lines | Blank lines | Regime |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Fidelity Investments Charitable Gift Fun | national | 80,308 | 12,514.5 | 1 | "FOR GRANT RECIPIENT'S EXEMPT PURPOSES" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 2 | National Philanthropic Trust | national | 18,583 | 5,143.0 | 8 | "HUMAN SERVICES" (22.6%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 3 | Donor Advised Charitable Giving Inc | national | 55,292 | 6,367.7 | 38 | "RELIGION RELATED" (31.6%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 4 | Vanguard Charitable Endowment Program | national | 24,269 | 2,982.4 | 1 | "FOR RECIPIENT'S EXEMPT PURPOSE" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 5 | Gs Donor Advised Philanthropy Fund | national | 7,424 | 2,957.5 | 7 | "COMMUNITY & HUMAN SERVICES" (39.4%) | 0.0% / 0.0% | 0.8% / 0.9% | 99.2% | 0.0% | sector_taxonomy |
| 6 | Silicon Valley Community Foundation | community_foundation | 3,576 | 3,158.2 | 20 | "EDUCATION" (17.6%) | 5.8% / 60.3% | 0.0% / 0.0% | 94.2% | 0.0% | sector_taxonomy |
| 7 | American Endowment Foundation | national | 14,380 | 1,258.1 | 44 | "RELIGION" (22.6%) | 13.2% / 8.3% | 0.1% / 0.1% | 86.7% | 0.0% | sector_taxonomy |
| 8 | Morgan Stanley Global Impact Funding Tru | national | 19,253 | 1,224.6 | 1 | "UNRESTRICTED GENERAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 10 | Natl Christian Charitable Fdn Inc | single_issue | 16,327 | 2,575.6 | 58 | "CHURCH" (23.6%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 12 | The Chicago Community Trust | community_foundation | 3,976 | 1,423.3 | 1 | "GENERAL SUPPORT FOR PROGRAMS, OPERATIONS AND " (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 13 | Impactassetsinc | national | 2,733 | 580.1 | 1 | "GENERAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 14 | Foundation For The Carolinas | community_foundation | 1,605 | 609.1 | 1 | "CHARITABLE GIFT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 15 | Jewish Communal Fund | single_issue | 4,673 | 953.3 | 1 | "IN FURTHERANCE OF GRANTEE'S TAX-EXEMPT PURPOS" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 16 | Greater Kansas City Community Foundation | community_foundation | 2,405 | 350.3 | 8 | "HUMAN SERVICES" (21.2%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 17 | Greater Horizons | national | 3,284 | 424.4 | 8 | "RELIGION-RELATED" (26.8%) | 0.0% / 0.0% | 0.0% / 0.0% | 99.9% | 0.1% | sector_taxonomy |
| 18 | Dechomai Asset Trust | processor | 6 | 552.3 | 1 | "UNRESTRICTED" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 19 | Combined Jewish Philanthropies Of Greate | single_issue | 1,105 | 322.3 | 70 | "DAF - EDUCATION" (17.3%) | 0.4% / 0.0% | 0.0% / 0.0% | 99.5% | 0.0% | sector_taxonomy |
| 20 | Raymond James Charitable Endowment Fund | national | 6,906 | 288.7 | 1 | "GENERAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 21 | The Ayco Charitable Foundation | national | 4,719 | 287.7 | 7 | "COMMUNITY & HUMAN SERVICES" (38.9%) | 0.0% / 0.0% | 0.6% / 0.7% | 99.4% | 0.0% | sector_taxonomy |
| 22 | The Us Charitable Gift Trust | national | 6,518 | 231.4 | 1 | "FOR RECIPIENT'S EXEMPT PURPOSE" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 23 | Columbus Foundation | community_foundation | 1,747 | 242.7 | 8 | "SOCIAL SERVICES" (27.2%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 24 | The New York Community Trust | community_foundation | 2,748 | 193.8 | 6 | "FOR PROGRAM SUPPORT." (47.9%) | 43.3% / 33.1% | 56.7% / 66.9% | 0.0% | 0.0% | free_text_mixed |
| 25 | The Oregon Community Foundation | community_foundation | 2,149 | 171.4 | 36 | "HUMAN SERVICES" (12.8%) | 0.0% / 0.0% | 0.0% / 0.0% | 99.9% | 0.1% | sector_taxonomy |
| 26 | Donors Trust Inc | single_issue | 919 | 282.1 | 324 | "FOR GENERAL OPERATIONS" (56.7%) | 57.8% / 71.6% | 27.3% / 26.3% | 0.0% | 0.0% | mostly_boilerplate_with_free_text |
| 27 | Boston Foundation Inc | community_foundation | 2,046 | 169.9 | 26 | "OPERATING SUPPORT/ANNUAL FUND" (74.3%) | 74.3% / 81.7% | 8.2% / 7.4% | 17.0% | 0.0% | mostly_boilerplate_with_free_text |
| 28 | California Community Foundation | community_foundation | 2,025 | 275.0 | 14 | "EDUCATION" (24.1%) | 0.0% / 0.0% | 0.0% / 0.0% | 97.4% | 0.0% | sector_taxonomy |
| 29 | The Community Foundation For Greater | community_foundation | 1,414 | 152.3 | 26 | "EDUCATION" (18.5%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 30 | Servant Foundation | national | 2,695 | 890.7 | 3 | "RELIGIOUS MINISTRY" (49.8%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 31 | Jewish Community Federation Of San | single_issue | 991 | 123.7 | 23 | "EDUCATION" (19.4%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 32 | The Bessemer Giving Fund | national | 1,653 | 138.5 | 16 | "GENERAL SUPPORT" (89.7%) | 94.3% / 91.8% | 4.5% / 6.3% | 1.0% | 0.0% | mostly_boilerplate_with_free_text |
| 33 | Greater Houston Community Foundation | community_foundation | 1,724 | 232.3 | 10 | "HUMAN SERVICES" (25.8%) | 0.0% / 0.0% | 0.0% / 0.0% | 100.0% | 0.0% | sector_taxonomy |
| 34 | Marin Community Foundation | community_foundation | 1,383 | 176.2 | 318 | "PROVIDE GENERAL OPERATING SUPPORT" (69.7%) | 77.4% / 61.3% | 10.8% / 28.9% | 0.8% | 0.0% | mostly_boilerplate_with_free_text |
| 35 | Community Foundation Of New Jersey | community_foundation | 1,321 | 93.8 | 53 | "RELIGION" (6.4%) | 7.6% / 6.1% | 6.4% / 6.5% | 84.0% | 0.0% | sector_taxonomy |
| 36 | American Gift Fund | national | 1,827 | 98.2 | 1 | "OPERATIONS" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 37 | Jewish Community Foundation Of Los Angel | single_issue | 1,063 | 142.2 | 1 | "GENERAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 38 | The Denver Foundation | community_foundation | 1,184 | 131.7 | 263 | "YOUTH DEVELOPMENT PROGRAMS" (3.8%) | 0.1% / 0.1% | 5.8% / 11.5% | 63.0% | 0.0% | sector_taxonomy |
| 39 | The San Diego Foundation | community_foundation | 1,040 | 102.3 | 460 | "FOR GENERAL SUPPORT" (54.4%) | 56.0% / 45.4% | 23.5% / 21.2% | 0.5% | 0.0% | mostly_boilerplate_with_free_text |
| 40 | Community Foundation | community_foundation | 806 | 114.6 | 1 | "GENERAL OPERATIONAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 41 | Tulsa Community Foundation | community_foundation | 1,066 | 158.6 | 2 | "GENERAL OPERATIONS" (97.5%) | 97.5% / 99.7% | 2.5% / 0.3% | 0.0% | 0.0% | single_string_boilerplate |
| 42 | Seattle Foundation | community_foundation | 5,379 | 177.9 | 996 | "TO PROVIDE GENERAL SUPPORT" (73.5%) | 75.0% / 46.6% | 11.2% / 28.3% | 0.9% | 0.0% | mostly_boilerplate_with_free_text |
| 43 | The Board Of Trustees Of The Leland | university_hospital | 127 | 74.6 | 41 | "GENERAL SUPPORT" (37.8%) | 37.8% / 46.5% | 44.1% / 38.2% | 3.9% | 0.0% | free_text_mixed |
| 44 | Ucla Foundation | university_hospital | 67 | 443.0 | 3 | "GENERAL SUPPORT" (97.0%) | 97.0% / 15.7% | 1.5% / 84.1% | 0.0% | 0.0% | single_string_boilerplate |
| 45 | The Minneapolis Foundation | community_foundation | 1,378 | 105.1 | 70 | "DONOR-ADVISED, GENERAL" (12.5%) | 20.2% / 22.9% | 0.0% / 0.0% | 79.4% | 0.0% | sector_taxonomy |
| 46 | T Rowe Price Program For Charitable | national | 2,479 | 101.8 | 1 | "MULTIPLE" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 47 | Thrivent Charitable Impact & Investing | single_issue | 2,565 | 84.6 | 1 | "GENERAL SUPPORT" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 48 | The San Francisco Foundation | community_foundation | 1,623 | 189.1 | 895 | "FOR GENERAL SUPPORT." (37.6%) | 65.9% / 53.8% | 23.7% / 40.8% | 0.1% | 0.0% | mostly_boilerplate_with_free_text |
| 49 | Community Foundation Of Tampa Bay Inc | community_foundation | 566 | 30.7 | 1 | "SUPPORT OF MISSION" (100.0%) | 100.0% / 100.0% | 0.0% / 0.0% | 0.0% | 0.0% | single_string_boilerplate |
| 50 | Saint Paul & Minnesota Foundation | community_foundation | 1,446 | 193.2 | 2 | "MULTIPLE GRANTS FOR MULTIPLE PURPOSES" (99.9%) | 99.9% / 99.7% | 0.1% / 0.3% | 0.0% | 0.0% | single_string_boilerplate |

### 3.3 Regimes by sponsor type [C]

| Segment | One string on >90% of lines | Sector taxonomy | Mostly boilerplate + free text | Free text, mixed |
|---|---|---|---|---|
| national (16) | 8 | 7 | 1 | 0 |
| community_foundation (22) | 6 | 10 | 5 | 1 |
| single_issue (7) | 3 | 3 | 1 | 0 |
| processor (1) | 1 | 0 | 0 | 0 |
| university_hospital (2) | 1 | 0 | 0 | 1 |
| **all (48)** | **19** | **20** | **7** | **2** |

- 16 of the 48 sponsors use exactly one purpose string on every line.
- 31 of 48 have no specific-purpose line at all.
- No national reaches 5% specific lines. The ten sponsors that do are NYCT, San Diego, SFF, Seattle, Marin, Boston, CFNJ and Denver (community foundations), plus Donors Trust and Stanford.
- Blank purposes occur at three sponsors only:
  - Greater Horizons: 2 lines with no name, EIN or purpose, one of them $212,187,406 [F];
  - Oregon CF: 2 lines reading "0";
  - Seattle Foundation: 1 line reading "NONE".

### 3.4 What the sponsors' own Schedule I narratives say [F]

The script flags Part I line 2 and Part IV narratives that mention restriction (`sched_i_note_mentions_restriction`). The result is yes for 11 sponsors, no for 34, and no narrative for 3. The relevant passages:

- **NPT (rank 2):** \
- **T. Rowe Price Program (rank 46):** "THE USE OF "MULTIPLE" FOR GRANT PURPOSE MEANS THAT MULTIPLE GRANTS WERE GIVEN TO THAT ORGANIZATION AND THEIR PURPOSE WAS A COMBINATION OF ENDOWMENT, GENERAL OPERATING AND/OR SPECIAL PROJECT". The filer states that grants of different purposes (endowment, general operating, special project) to the same organisation are combined under one word, and it uses that word on all 2,479 lines; that restricted and unrestricted grants are merged is the reading here [I] [V wave 35A]
- **Fidelity Charitable (rank 1):** "ALTHOUGH FOR SCHEDULE I PURPOSES A RECIPIENT ORGANIZATION IS ONLY LISTED ONCE, THE TOTAL AMOUNT GIVEN MAY REFLECT ADVISED DONATIONS FROM MANY GIVING ACCOUNTS". One line is the sum of many grants.
- **Greater Kansas City CF and Greater Horizons:** "GRANT DISBURSEMENTS SPECIFY GRANT PURPOSE … SIGNIFICANT RESTRICTED PURPOSE GRANTS ARE MONITORED". Both purpose columns are sector labels only.
- **CJP (rank 19):** "GRANTEES ARE EXPECTED TO ADHERE TO THE TERMS AND RESTRICTIONS AS OUTLINED IN THE GRANT LETTER".
- **SFF (rank 48):** \
- **California CF:** distinguishes "BOARD DISCRETIONARY GRANT, DONOR ADVISED FUND GRANT, SCHOLARSHIP GRANT OR RESTRICTED GRANT".

[I] Restrictions exist and are recorded in grant letters, but the filers do not carry them into column (h).

## 4. What Schedule I purpose text can and cannot tell us

**Can [C/F]:**

1. **The filer's reporting regime.** This is a stable, auditable property of each return, and it sorts sponsors cleanly (§3.3).
2. **For a minority of filers, a lower bound on specific uses.** These are mostly community foundations and Donors Trust, which write free text: scholarships, capital campaigns, named funds, programmes.
3. **The sector mix as the sponsor codes it.** NPT, DAFgiving360, GS DAPF, NCF and SVCF assign NTEE-like labels. These duplicate what an NTEE join already gives (cf. `mission_recipient_sectors.py`).
4. **Explicit "unrestricted" statements** at Morgan Stanley GIFT ("UNRESTRICTED GENERAL SUPPORT", 19,253 lines) and Dechomai.

**Cannot:**

1. **The share of grants that carry a donor restriction, for any national sponsor [I].**
   - The eight single-string nationals report one string whatever the donor chose. That covers Fidelity Charitable, whose donors can pick "Where It Is Needed Most" or a specific use ([Fidelity Charitable FAQ](https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html)).
   - The seven taxonomy nationals report a sector, not a use.
   - So the national figure of 0.07% specific lines measures reporting practice, not donor behaviour.
2. **Grant-level purpose.** Schedule I is one line per recipient with more than $5,000 in aggregate ([IRS Schedule I instructions](https://www.irs.gov/instructions/i990si)). Several grants of different purposes collapse into one line, as the Fidelity and T. Rowe notes say. The SFF strings "FOR GENERAL SUPPORT. FOR GENERAL SUPPORT." and the Minneapolis Foundation's multi-label strings show the same concatenation.
3. **DAF versus non-DAF grants.**
   - Schedule I covers all of a filer's grants. At community foundations, discretionary and field-of-interest grants are mixed in. Seattle Foundation strings such as "N2N SPRING 2024" and "CLIMATE JUSTICE IMPACT STRATEGY 2024" look like the foundation's own programmes [I].
   - The community-foundation specific share (7.7% of lines) is therefore an upper bound for DAF restrictions there.
4. **Whether a filer complies with the instructions.**
   - Column (h) instructions say: "Don't use general terms, such as charitable, educational, religious, or scientific. Use more specific descriptions, such as general support…" ([IRS](https://www.irs.gov/instructions/i990si)) [F].
   - 20 sponsors use exactly those general sector terms ("EDUCATION", "RELIGION"). Foundation For The Carolinas uses "CHARITABLE GIFT".
   - Under the IRS's own wording, \
5. **Foreign grants.** Schedule F is outside this panel.

## 5. Does it support the repo's claims?

Claims were found with `grep -rin "general support"` and `grep -rin "unrestricted"` over `research/`.

| # | Repo claim (file) | Verdict | Why |
|---|---|---|---|
| C1 | DAFgiving360 FY2025: "38% recurring, 70%+ unrestricted" (`ai-economics-replacement-analysis.md` P05; `daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md` l.10) | **Not testable from Schedule I** | DAFgiving360 (Donor Advised Charitable Giving Inc, rank 3) files 38 sector labels on 55,292 lines. 0 lines are boilerplate, 0 specific. The FY2024 Schedule I neither supports nor contradicts 70%+. The press release could not be re-read (robots.txt 403, §9). Adjacent first-party releases on the Schwab pressroom give 72% (FY2022), 71% (CY2023) and 72% (FY2024) of grants that “did not specify a purpose”, so 70%+ is plausible for FY2025 but still unread, and it measures no purpose entered, not legal restriction (b4013-b4428) [V wave 39A] |
| C2 | "a restricted grant purpose triggers manual inquiry … an unrestricted purpose expedites the grant" (`industry-incentives-structural-analysis.md` §6.2) | **Consistent but not evidenced by Schedule I** | The Fidelity FAQ still says "Where It Is Needed Most" "can also help expedite the processing" (re-read 2026-11-19). Fidelity's Schedule I shows one string on all lines, so the restricted share and its effect on processing cannot be seen in filings. |
| C3 | ImpactAssets "uses that purpose text ['GENERAL SUPPORT'] for nearly every grant, so it says nothing" (`queue-batch29-complaints-voids.md` P-WAT-02) | **Supported, and sharper** | It is every grant: 2,733 of 2,733 FY2024 lines, 1 distinct string [C]. \ The GiveClear "GENERAL SUPPORT" line ($86.0m, `queue-npt-dafgiving360-misc.md`) is therefore uninformative about restriction too. |
| C4 | Schedule F "purpose buckets": general support 22.1%; NPT's "INTERNATIONAL" 18.6%; single-issue "general support 96.0%" (`direction-foreign-grants-schedule-f.md` §3.4) | **Partly supported; the buckets need relabelling** | That doc already warns that the text is generic (§3.4 item 6). This panel shows the non-general buckets are mostly sponsor sector codes (NPT, GS DAPF), not uses, so "environment and animals 13.7%" describes recipients, not restrictions. The single-issue 96% "general support" bucket comes from boilerplate such as JCF's "IN FURTHERANCE OF GRANTEE'S TAX-EXEMPT PURPOSE" [I]. Proposed fix: P-B4013-04. |
| C5 | "Grant-purpose sensitivity … purpose fields that indicate benefit risk" as a triage input (`industry-incentives-structural-analysis.md`) | **Not supported by public filings** | Strings naming an event, gala, ticket, auction, golf outing, dinner, luncheon or sponsorship appear on 107 lines (0.03% of lines, $12.7m) [C]; e.g. San Diego "ANNUAL GALA" (4 lines). Public purpose text cannot supply a benefit-risk signal. Sponsors' internal recommendation fields might. |
| C6 | Every.org's statement that it issues "an unrestricted grant to the nonprofit" (`queue-batch32-filing-reconciliations.md`) | **Out of scope** | Every.org files Form 990-PF and is not in the top-50 panel. |

**Overall [I].** Schedule I purpose text does not support any quantitative claim about restricted versus "general support" shares for national DAF sponsors.

- What it does show is that most large sponsors choose not to disclose that split in column (h), even when their narratives confirm restrictions exist (§3.4).
- Repo statements of the form "X% of DAF grants are general support", where X comes from Schedule I or Schedule F purpose text, should be restated as \

## 6. Limits

- **One year.** FY2024 only, one return per sponsor. Regime stability over 2021–2025 is untested (P-B4013-02).
- **Hand-built rules.** The keyword rules were built by inspecting this panel's 3,880 sponsor-string pairs. They are transparent but not validated against an external coding, and a second coder could move borderline strings (e.g. "PROGRAM SUPPORT", "CHARITABLE PROJECT"). Class shares for nationals are insensitive to such moves, because nationals hardly use free text. Community-foundation shares are sensitive. A wave 35A audit of 60 random sponsor-string pairs (seed 2026111935) agreed with the assigned class on 40, was ambiguous on 3 and disagreed on 17 (97.6% agreement by lines). 16 of the 17 under-count specific use: free text with no keyword hit (e.g. \
- **Line shares are recipient-aggregate shares, not grant-count shares.** Schedule I omits recipients at or below $5,000 and all grants to individuals and foreign recipients (Parts III, Schedule F).
- **Grantmaking type.** Community-foundation Schedule I mixes DAF and discretionary grants; nationals' lines are almost all DAF grants [I].
- **University and hospital sponsors** (Stanford, UCLA) list grants to other organisations only. Their DAF programmes are a small part of their Schedule I, so they are shown but excluded from the "ex university_hospital" pool.
- **The restriction flag is a keyword hit, not a reading.** `sched_i_note_mentions_restriction` searches the Schedule I narratives for "restrict", "designat", "specific purpose", "grant purpose", "intended use" or "earmark". Some hits concern expenditure-responsibility rules rather than donor restrictions (Bessemer, Chicago).
- **Segment labels** come from the DAFRC panel (`segment_of`). Greater Horizons is classed national.

## 7. Data dictionary: `data/mission-2026-11-14/grant-purpose-panel-2026-11-19.csv`

The file has 55 rows: 48 with `scope_type` = sponsor, then 2 with `all` and 5 with `segment`. Shares are 0–1. "Lines" are Schedule I Part II `RecipientTable` rows.

| Column | Meaning |
|---|---|
| `scope_type` | `sponsor`, `all` (all 48, or all 46 excluding university/hospital) or `segment` (pooled lines of that segment's sponsors) |
| `rank_fy2024` | FY2024 DAF-asset rank in DAFRC (sponsor rows) |
| `ein` | Filer EIN (9 digits) |
| `sponsor` | DAFRC name (sponsor rows); a scope label otherwise |
| `segment` | DAFRC segment: national, community_foundation, single_issue, processor, university_hospital |
| `object_id` | IRS e-file object id of the FY2024 return |
| `tax_period_end` | Tax period end date of that return |
| `lines` | Schedule I Part II lines |
| `usd` | Sum of cash + non-cash on those lines (USD, rounded) |
| `distinct_purposes` | Distinct non-blank normalised purpose strings |
| `top_purpose` | Most frequent string, first 90 characters (sponsor rows) |
| `top_purpose_class` | Class of `top_purpose` under §2.1 |
| `top_purpose_line_share` | Share of lines carrying `top_purpose` |
| `modal_gt90` | yes if one string is on more than 90% of lines |
| `share_lines_boilerplate` / `share_usd_boilerplate` | Line / dollar share in the `boiler_*` classes |
| `share_lines_boilerplate_incl_modal` / `share_usd_boilerplate_incl_modal` | Same, plus lines carrying a string that is on more than 90% of the sponsor's lines (the headline boilerplate measure) |
| `share_lines_specific` / `share_usd_specific` | `specific_capital` + `specific_program` |
| `share_lines_category_label` / `share_usd_category_label` | Sector-taxonomy labels |
| `share_lines_other_descriptive` / `share_usd_other_descriptive` | No rule fired |
| `share_lines_blank` / `share_usd_blank` | Blank or placeholder purpose |
| `share_{lines,usd}_{boiler_unrestricted,boiler_aggregate,boiler_general,boiler_exempt,specific_capital,specific_program}` | Each individual class |
| `purpose_regime` | §2 step 6 (sponsor rows) |
| `sponsors` | Number of sponsors in the row |
| `median_sponsor_share_lines_boilerplate_incl_modal`, `median_sponsor_share_lines_specific` | Median across the row's sponsors (group rows) |
| `sched_i_note_mentions_restriction` | yes / no / no_note: whether the Schedule I narratives match the restriction regex in §6 |
| `sched_i_note_excerpt` | About 240 characters around the first hit, or the start of the narrative |
| `cache_check` | Whether line count and dollar total match the `rcp/lines` cache ("yes" for all 48) |
| `source_url` | The return's XML on the GivingTuesday mirror of IRS TEOS |

## 8. Reproduce

```
python3 scripts/mission_grant_purpose_panel.py . --np-cache $SCRATCH/npcache --lines-cache $SCRATCH/rcp/lines \
  --xml-list $SCRATCH/rcp/allxml.txt --xml-dir $SCRATCH/q1301/xml --purpose-cache $SCRATCH/q1301/purpose \
  --fetch --audit $SCRATCH/q1301/audit.csv --summary $SCRATCH/q1301/summary.json
```

The script is stdlib only. It imports the universe and return choice from `mission_daf_to_daf.py`, `mission_net_payout.py` and `mission_990_contractors.py`. With `--fetch`, a missing XML is downloaded from the mirror with User-Agent `research-script/1.0`.

## 9. Source register and robots log

| Source | URL | Use | Accessed |
|---|---|---|---|
| IRS e-file XML, FY2024 Schedule I, 48 returns (GivingTuesday mirror of IRS TEOS) | `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{object_id}_public.xml`; one URL per sponsor in CSV `source_url`, e.g. [Fidelity Charitable](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml), [NPT](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml), [DAFgiving360](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml), [Vanguard Charitable](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511349349313096_public.xml), [ImpactAssets](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml), [T. Rowe Price Program](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202401949349301515_public.xml), [Greater Horizons](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349309621_public.xml) | All purpose strings, amounts and narratives | 27 downloaded 2026-11-19; 21 local copies from earlier batches |
| IRS, Instructions for Schedule I (Form 990) (Rev. 12/2024) | https://www.irs.gov/instructions/i990si | Column (h) wording; the over-$5,000 aggregate rule | 2026-11-19; re-read 2026-11-19 by wave 35A (HTML and PDF). The revision is continuous-use from tax year 2024; 19 of the 48 returns end on or before 2024-06-30 (tax year 2023) and fell under the prior revision, which was not re-read [V wave 35A] |
| Fidelity Charitable, "How long will it take for the grant I recommended to be processed?" | https://www.fidelitycharitable.org/faqs/all/grant-processing-timeline.html | "Where It Is Needed Most" expedites (claim C2) | 2026-11-19 |
| DAFgiving360, FY2025 results press release (as cited in the repo) | https://www.dafgiving360.org/press-release/fiscal-year-2025-results | Claim C1, not re-read | robots.txt 403 |
| DAFRC panel and return choice (repo) | `data/` DAFRC CSV via `mission_990_contractors.DAFRC_CSV`; `scripts/mission_daf_to_daf.py` | Universe, ranks, segments | n/a |

Robots log (`$SCRATCH/q1301/robots/log.tsv`):

| Time (UTC) | Host | robots.txt status | Decision |
|---|---|---|---|
| 2026-11-19T19:24:05Z | gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | allowed; 27 XMLs fetched |
| 2026-11-19T19:29:17Z | www.irs.gov | 200; `/instructions/` not disallowed | allowed |
| 2026-11-19T19:29:40Z | www.fidelitycharitable.org | 200; `User-agent: *` disallows only /retired/, /sample-email/, /nuance/, a DAM path | allowed |
| 2026-11-19T19:29:39Z | www.dafgiving360.org | **403** | Treated as disallowed, but the page request was sent in the same command, before that decision could apply; it also returned 403 and nothing from it is used. RFC 9309 treats a 4xx robots.txt as no restriction, so this is a process lapse, not a breach [V wave 35A] |
