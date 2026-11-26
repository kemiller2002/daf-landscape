# 50-state check of the "no state DAF mandate" negative (queue item P-GAP19-14)

**Prepared 2026-11-19. Desk research only. No legislator, regulator, sponsor or vendor was contacted. No logins, form submissions or API keys. This is research, not legal advice.**

Labels: **[F]** the source states it directly (official text read). **[S]** secondary source: an aggregator search hit, a search-engine snippet, or a repo tracker row. **[I]** our inference. Source IDs (G-S01…) point to the [source register](#source-register). The row-level data is in [`state-daf-law-50-state-check-2026-11-19.csv`](../../data/mission-2026-11-14/state-daf-law-50-state-check-2026-11-19.csv): 51 state rows (G001–G051) and 59 instrument rows (G052–G110). The script is [`scripts/mission_gap19_state_daf_check.py`](../../scripts/mission_gap19_state_daf_check.py).

**What this checks.** [`direction-state-daf-law-tracker.md`](direction-state-daf-law-tracker.md) §1 says no state enacted a DAF payout, account-level reporting or donor-intent mandate in 2021–2026, and that none was introduced apart from CA AB 1353, which had no operative text. Validation wave 25A marked this **unverifiable (V25A-17)** because no 50-state search had been run ([validation-wave25a-report.md](validation-wave25a-report.md)). The existing tracker CSV is unchanged. This file adds a new CSV.

---

## 1. Headline answer

| Question | Answer |
|---|---|
| **Does the negative hold?** | **Yes for 50 of 51 jurisdictions, with one qualification. Connecticut could not be checked.** No 2021–2026 bill or enacted text found in any state or DC imposes a payout, account-level reporting or donor-intent mandate on DAF sponsors. The CA AB 1353 exception (an intent-only bill) is confirmed. The pre-2021 CA bills AB 1712 and AB 2936 remain the only sponsor-reporting proposals found. |
| **Qualification (correction to "no state has")** | **New Jersey has an older, narrow rule that reaches assets held in a DAF.** Under P.L.2000 c.143, hospital-conversion assets that a charity moved "to a donor-advised fund" and has not spent count as "remaining charitable assets". The donor-advised-fund clause was added by P.L.2014 c.82 (approved 2014-12-26) and kept by P.L.2018 c.29 [V wave 32B] The Superior Court may reallocate them to a successor nonprofit hospital [F; G095, G097]. It covers one asset class and predates 2021. Read the tracker's negative as "no general DAF mandate". It is not true that no state law reaches DAF-held assets. |
| **Counts** | **checked-none 38, found 12, not checkable 1 (CT).** "Found" means DAF wording was found in a 2021–2026 bill or in enacted text in force during the window. **None of the 12 "found" states has a mandate of the three kinds.** |
| **What the DAF mentions are** | Of 37 in-window instrument rows with DAF wording, **16 are tax treatment** (credits or deductions that exclude or include DAF gifts, and wealth-tax bills that count DAF gifts in the base), 11 are regulatory exclusions or conditions (platform-law exclusions, credit-union DAF accounts, Alaska's PFD-program bar), 1 is a disclosure duty on officials (CA FPPC), 1 is an intent bill, 4 are descriptive wording (resolutions, a definition), 3 were not read, and 1 is the narrow NJ asset rule. The 37 rows are 34 distinct instruments: HI HB 992 and SB 1311 each have a 2025 and a 2026 row, and IL HB 4462 is the enactment of 205 ILCS 305/39. The regulatory exclusions are therefore 8 distinct instruments [V wave 32B] |

---

## 2. Method

1. **Uniform screen, all 50 states plus DC (Open States).** The public Open States full-text bill search page (`open.pluralpolicy.com/search/?query=…&state=xx`) was queried for `"donor advised"` and `"donor-advised"` separately. The site tokenises the two forms differently: the unfiltered totals were 70 and 27. All result pages were read. robots.txt for that host disallows only `/admin/`, `/api/v1/`, `/graphql` and `/get_district/`, so `/search/` is allowed; requests were 2 seconds apart. The API was not used: `/api/v1/` is disallowed and v3 needs a key.
   - **Reconciliation:** the per-state queries return 47 distinct bills. The unfiltered queries return the same 47 plus 23 federal (`/us/`) bills, and no other differences (G-S01).
   - **Text-index control:** for each state, the count of bills matching `"internal revenue code"` (all years) shows whether bill text is indexed. It runs from 16 (CT) and 37–103 (SD, WY, ME, NH, AR, DE, VT, ND, AK, NV) up to 3,851 (IL).
2. **Recall test against known positives.** Eight 2021–2026 bills were already known, from the tracker, to contain DAF wording: CA AB 488 and AB 1353; HI SB 2983 (2024) and SB 1048 (2025); NY A5092, S1570, A3252 and A3632. **Open States found 6 of the 8.** It missed both Hawaii acts.
   - The SB 1048 introduced and SD1 PDFs contain no DAF wording, while Act 108 has 4 mentions. So the wording was added in a later version that the index does not hold.
   - SB 2983's text did not match even other words from the Act.
   - **[I]** Open States indexes only some versions of each bill. A zero is a strong screen, but not proof.
3. **Official-site cross-checks where robots.txt allowed and the search worked by GET.**
   - **Florida:** flsenate.gov bill-text search, all versions and amendments, 2021 through 2026. Zero hits for both phrasings in every session; the control phrase matched 63–88 bills per session (G-S03). Crawl-delay 10 respected.
   - **Massachusetts:** malegislature.gov search, 194th Court. Zero hits for both phrasings; the control phrase gave 172 results (G-S04). Earlier courts could not be selected by URL.
4. **Text reading for every hit.** Each in-window hit was classified from official text where the host allowed it: NC, MO, MS, OH and HI PDFs, and the NJ chapter law. Otherwise it was classified from a search-engine snippet of the official page, labelled [S] (IL, WI, CA AB 576, AK). Hits seen only by title are marked "unclassified (text not read)".
5. **Instruments outside bill search.** Regulations and older statutes that a bill search cannot surface were added from the tracker: CA FPPC Reg. 18424.3, KS K.A.R. 92-12-152, the IL Illinois Gives rule and WA RCW 82.87.080. Also added: IL 205 ILCS 305/39, AK AS 43.23.130(k) and the NJ and MS enacted texts.
6. **Statute checks.**
   - No state offered a whole-code full-text search that was both reachable and allowed by robots.txt. Justia and FindLaw serve robots.txt behind Cloudflare, and the TX, AZ, ND and OK search paths are disallowed.
   - Three targeted negative checks were run on credit statutes: Iowa Code 15E.303 and 15E.305 (Endow Iowa) and N.D.C.C. ch. 57-38 contain no "donor" wording [F]. Washington RCW 82.87.080 contains none either, per the tracker (T22).
7. **Result rule.**
   - **found:** DAF wording in a 2021–2026 bill, or in enacted text in force during the window.
   - **checked-none:** zero hits in at least one full-text search covering 2021–2026, and no known in-window instrument.
   - **not checkable:** no usable full-text search. Only CT, where the text index is thin and the official host fails TLS.
   - Pre-2021 hits are kept as context only (in_window = N).

**robots.txt log, official legislature hosts (read 2026-11-19).** The CSV column `robots_official_host` gives each state's result.
- **Disallow `/` for all agents:** WA (app.leg.wa.gov), OK, RI, TN, DC (lims).
- **Bars Anthropic agents (ClaudeBot, anthropic-ai, Claude-Web):** AK (akleg.gov).
- **Robots unreadable:** CA and NY sit behind a Cloudflare challenge (nysenate.gov returned 403 today, although an earlier pass read it). IL, OH (main site), CT and WI fail TLS or reset the connection. NH returned an empty reply.
- **Search paths disallowed:** TX and AZ disallow `/Search/` and `/search/`; ND disallows `/search/`.
- **Missouri:** house.mo.gov disallows `/bill.aspx` and `/*?` (crawl-delay 120). One bill page was fetched before the full robots file was read. It was not used, and Missouri text came from documents.house.mo.gov (crawl-delay 20) instead.
- **Aggregators:** LegiScan, Justia and FindLaw serve robots.txt behind Cloudflare, so none was fetched. BillTrack50 disallows ClaudeBot and sets `ai-train=no`, so it was not fetched either.

---

## 3. Per-state table

OS = Open States hits for `"donor advised"` / `"donor-advised"` (all years, including pre-2021). IRC = control-phrase hits. In-window instruments are listed with what the DAF wording does.

| State | Result | OS hits | IRC | In-window instruments with DAF wording (what the wording does) | Official cross-check |
|---|---|---|---|---|---|
| AL | checked-none | 0 / 0 | 173 | — | none |
| AK | found | 1 / 0 | 96 | AS 43.23.130(k): community foundation may not put PFD-program gifts in a DAF [S]; HB 110 (33rd, died): text not read [S/I] | robots bars Anthropic agents |
| AZ | checked-none | 0 / 0 | 1103 | — | /search/ disallowed |
| AR | checked-none | 0 / 0 | 52 | — (thin index) | none |
| CA | found | 5 / 5 | 533 | AB 488 (enacted 2021): platform-law DAF exclusion; AB 1353 (died 2022): intent only; AB 576 (failed 2026): keeps the exclusion [S]; FPPC Reg. 18424.3: officials disclose DAF-sourced behested payments | leginfo robots unreadable |
| CO | checked-none | 2 / 0 | 191 | — (2017–18 endowment-credit bills only) | none |
| CT | **not checkable** | 0 / 0 | **16** | — | cga.ct.gov TLS failure |
| DE | checked-none | 0 / 0 | 55 | — (thin index) | none |
| DC | checked-none | 2 / 0 | 269 | — (2018 confirmation resolutions only) | lims disallows / |
| FL | checked-none | 0 / 0 | 690 | — | **flsenate.gov 2021–2026: 0** |
| GA | checked-none | 0 / 0 | 409 | — | none |
| HI | found | 4 / 0 | 1100 | Act 205 (SB 2983, 2024) and Act 108 (SB 1048, 2025): DAF-sponsor platform exclusion [F; both missed by OS]; HB 992 and SB 1311 (2025, carried over to 2026): same exclusion [F] | data.capitol.hawaii.gov PDFs |
| ID | checked-none | 0 / 0 | 184 | — | none |
| IL | found | 6 / 2 | 3851 | HB 3475 and SB 2121 (102nd, died) and SB 3778 (104th, pending): wealth tax counts DAF gifts [S]; HB 4462 = P.A. 102-0774 / 205 ILCS 305/39: credit-union DAF accounts [S]; Illinois Gives (35 ILCS 60, 86 IAC 1050): DAF excluded from credit; HB 5817, HB 5372: not read | ilga.gov TLS failure |
| IN | checked-none | 0 / 0 | 380 | — | none |
| IA | checked-none | 0 / 0 | 552 | — | Code 15E.303 and 15E.305: no DAF wording |
| KS | found | 0 / 0 | 485 | K.A.R. 92-12-152 (2026): no credit for gifts to a DAF [tracker T21] | none |
| KY | checked-none | 0 / 0 | 515 | — (SB 70 of 2024 has no DAF wording; tracker T23) | none |
| LA | checked-none | 1 / 1 | 130 | — (2019 commendation only) | none |
| ME | checked-none | 0 / 0 | 50 | — (thin index) | none |
| MD | checked-none | 0 / 0 | 626 | — | none |
| MA | checked-none | 0 / 0 | 604 | — | **malegislature.gov 194th: 0** |
| MI | checked-none | 0 / 0 | 692 | — | none |
| MN | checked-none | 2 / 2 | 2616 | — (2017–18 Endow Minnesota bills only) | revisor search is a JS app |
| MS | found | 7 / 6 | 1480 | Endow Mississippi credit (SB 2210, 2019; credit through 2023): DAFs count as endowed funds [F]; SC 555 (2023) and SR 17 (2025): honoree resolutions [F] | billstatus documents |
| MO | found | 2 / 0 | 813 | HB 1181 (2025) and HB 2216 (2026), not passed: credit-eligible fund "Is not a donor advised fund" [F] | documents.house.mo.gov PDFs |
| MT | checked-none | 0 / 0 | 252 | — | none |
| NE | checked-none | 0 / 0 | 295 | — | none |
| NV | checked-none | 0 / 0 | 103 | — | none |
| NH | checked-none | 0 / 0 | 51 | — (thin index) | robots unreadable |
| NJ | found | 2 / 2 | 1458 | P.L.2000 c.143 as amended by P.L.2014 c.82 (which added the DAF clause) and P.L.2018 c.29 (in force): court may reallocate undisbursed conversion assets held in a DAF [F] | pub.njleg.gov PDFs (PL14/82, PL18/29) [V wave 32B]
| NM | checked-none | 0 / 0 | 409 | — | none |
| NY | found | 8 / 0 | 1908 | A5092 and S4482 (2021), A3252 and S1570 (2023), A3632 and S165 (2025): billionaire mark-to-market tax counts DAF gifts in the base (S4482 and S165 inferred) | nysenate.gov 403 today |
| NC | found | 1 / 1 | 899 | SB 684 (2025, 1st reading): endowment credit; "endowed fund" includes donor-advised funds [F] | ncleg.gov PDF |
| ND | checked-none | 0 / 0 | 93 | — (thin index) | ch. 57-38: no DAF wording |
| OH | found | 2 / 2 | 580 | SB 309 (135th) and SB 12 (136th), in committee: "community foundation" definition lists DAFs [F] | search-prod.lis PDFs |
| OK | checked-none | 0 / 0 | 1512 | — | robots disallows / |
| OR | checked-none | 0 / 0 | 702 | — | none |
| PA | checked-none | 0 / 0 | 428 | — | none |
| RI | checked-none | 0 / 0 | 1183 | — | robots disallows / |
| SC | checked-none | 0 / 0 | 181 | — | none |
| SD | checked-none | 0 / 0 | 37 | — (thin index) | none |
| TN | checked-none | 0 / 0 | 278 | — | robots disallows / |
| TX | checked-none | 0 / 0 | 463 | — | /Search/ disallowed |
| UT | checked-none | 0 / 0 | 580 | — | none |
| VT | checked-none | 0 / 0 | 89 | — (thin index) | none |
| VA | checked-none | 1 / 0 | 1178 | — (2018 commending resolution only) | none |
| WA | checked-none | 0 / 0 | 728 | — (RCW 82.87.080 has no DAF wording; tracker T22) | robots disallows / |
| WV | checked-none | 0 / 0 | 930 | — | none |
| WI | found | 1 / 0 | 279 | AB 665 (2025, failed 2026-03-23): non-itemizer subtraction bars DAF gifts [S] | docs.legis unreachable |
| WY | checked-none | 0 / 0 | 38 | — (thin index) | none |

---

## 4. Findings

1. **The mandate negative now rests on a 51-jurisdiction search, not a sample.**
   - No 2021–2026 bill found in any state or DC would impose a payout, account-level reporting or donor-intent duty on DAF sponsors. The only DAF-titled bill in the window is CA AB 1353, which is intent-only and died at the desk on 2022-02-01 [G055].
   - Sponsor-reporting proposals exist only before 2021: CA AB 1712 and AB 2936 [G058–G059].
   - **V25A-17 can move from unverifiable to "checked, with limits"** (§5): CT is unchecked, and most checked-none rows rest on one aggregator screen.
2. **Correction: the blanket "no state has" wording is too broad.** New Jersey's hospital-conversion law (P.L.2000 c.143; the DAF clause was added by P.L.2014 c.82 and kept by P.L.2018 c.29) treats undisbursed conversion assets "transferred … to a donor-advised fund" as "remaining charitable assets". The Superior Court may reallocate them to the entity acquiring or operating an equivalent nonprofit hospital [F; G095] [V wave 32B] It protects charitable purpose for one asset class. It is pre-2021 and narrow, but it reaches DAF-held money. The tracker's §1 answer should be read as "no general DAF payout, reporting or donor-intent mandate".
3. **Tax treatment is the main way state law names DAFs, and it cuts both ways.**
   - **Excluded:** Illinois Gives (enacted) and Kansas K.A.R. 92-12-152 (in force) [tracker T20–T21]. Also the proposed Missouri Gives bills HB 1181 and HB 2216 ("Is not a donor advised fund") [F; G083–G084] and Wisconsin AB 665 [S; G110].
   - **Included:** Endow Mississippi (2019, through 2023) [F; G087] and North Carolina SB 684 (2025, proposed) [F; G093] define "endowed fund" to include donor-advised funds.
   - **Silent:** Endow Iowa and North Dakota's endowment credit say nothing about DAFs [F; G070, G094].
4. **Wealth-tax bills that count DAF gifts are wider than the tracker had.**
   - Beyond NY A5092, A3252/S1570 and A3632, the sweep adds **NY S4482 (2021) and S165 (2025)** [S/I] and **Illinois HB 3475 / SB 2121 (2021) and SB 3778 (2026, pending)** [S].
   - All count gifts to "any private foundation, donor advised fund" in a mark-to-market base. This is tax treatment, not a mandate.
5. **Platform-law DAF exclusions stayed in CA and HI.**
   - 2025–26 follow-up bills kept the "does not list or reference by name" exclusion: CA AB 576 (failed) [S] and HI HB 992 and SB 1311 (carried over) [F; G066–G069].
   - No third state's platform bill with DAF wording turned up.
6. **Other enacted DAF wording is regulatory, not a mandate on sponsors.**
   - Illinois lets credit unions give through DAF accounts on conditions (205 ILCS 305/39, P.A. 102-0774) [S; G072, G078].
   - Alaska bars community foundations from putting PFD-program gifts in a DAF (AS 43.23.130(k)) [S; G053].
   - California's FPPC rule binds officials, not sponsors [G054].
7. **Most other hits are descriptive.** They are honoree resolutions (MS 2023 and 2025; DC, LA and VA pre-2021) and Ohio's definition of a community foundation (SB 309, SB 12) [F].

## 5. Limits

1. **Aggregator recall is below 100%.** Open States found 6 of 8 known in-window positives. The two misses were Hawaii acts whose DAF wording sits in versions the index lacks (§2.2). So "checked-none" for the 36 states with no official bill-search cross-check is a strong screen, not proof. Florida and Massachusetts were cross-checked on official sites and both agreed. Proposal **P-G1914-02**.
2. **Nine jurisdictions have a thin text index** (control under 100: AK, AR, DE, ME, NH, ND, SD, VT, WY; NV is at 103). Eight of them are checked-none (AK is found), and those negatives are weaker, as the CSV notes record.
3. **Connecticut is not checkable** (P-G1914-01).
4. **Statute coverage is partial.** Whole-code search was not possible anywhere. Pre-2021 statutes with DAF wording surface only if a bill that amended them was indexed (as NJ's was), or if they were already known.
5. **Some texts were not read.** Eight in-window rows are classified from search-engine snippets of official or mirror pages (AK AS 43.23.130(k); CA AB 576; IL HB 3475, SB 2121, HB 4462, SB 3778 and 205 ILCS 305/39; WI AB 665), and three hits were not read at all (AK HB 110, IL HB 5817, IL HB 5372). Search snippets suggest IL HB 3039 (103rd) and SB 3884 (104th) may carry the same wealth-tax clause, but they were not verified and are not in the CSV (P-G1914-03).
6. **Phrasing.** Only "donor advised" and "donor-advised" were searched. A bill that says only "sponsoring organization" or "§4966" without the phrase would be missed [I: such drafting is rare in the hits read].
7. **Status** is as Open States or the official page showed it on 2026-11-19. Hawaii's carried-over bills show no action after 2025-12-08.

---

## 6. Data dictionary (`state-daf-law-50-state-check-2026-11-19.csv`)

| Column | Meaning |
|---|---|
| record_id | G001–G051 state rows; G052–G110 instrument rows |
| record_type | `state`; `bill`; `statute`; `regulation`; `statute+regulation`; `statute (negative)` (a statute read and found to have no DAF wording) |
| state, state_name | Two-letter code (DC included); full name |
| state_result | `checked-none`, `found` or `not checkable` (rule in §2.7); repeated on instrument rows |
| instrument_id | Bill number as Open States shows it, or act, statute or rule citation |
| session, year | Legislative session; year introduced or enacted (`n/a` if not verified) |
| title | Title as shown by the source |
| status | Status as of 2026-11-19 (from Open States latest action or the official text) |
| subject | `payout`, `reporting`, `donor intent`, `tax credit or deduction` or `other` (wealth-tax bases are `other`, with the tax role in `mention_type`) |
| mention_type | What the DAF wording does: `tax treatment`; `regulatory exclusion or condition`; `disclosure duty on officials (not sponsors)`; `intent bill (no operative text)`; `mandate (proposed, failed)`; `narrow asset rule`; `descriptive (resolution)`; `descriptive (definition)`; `unclassified (text not read)`; `none (negative check)` |
| daf_role | Plain description of the DAF wording, quoting it where load-bearing |
| is_daf_mandate | `N`, `proposed (failed)`, `narrow (…)` or `N (…)` with a qualifier |
| in_window_2021_2026 | `Y` if introduced or enacted 2021–2026, or in force during it; `N` for pre-2021 context |
| evidence_label | F, S, I or combinations |
| verification | How the text was checked (official text fetched / aggregator hit / search snippet / tracker row) |
| url | Instrument URL (official where read), or the Open States search URL on state rows. The 47 Open States bill-page URLs returned HTTP 404 on 2026-11-19; their status values come from the Open States search-result rows [V wave 32B]
| os_hits_donor_advised, os_hits_donor_hyphen_advised | State rows: Open States hit counts for each phrasing (all years) |
| os_control_hits_irc | State rows: Open States count for `"internal revenue code"` (text-index control, all years) |
| official_check | State rows: official-site search or document read, if any |
| robots_official_host | State rows: official legislature host and its robots.txt result on 2026-11-19 |
| notes | State rows: summary of in-window instruments, pre-2021 hits, mandate check and caveats. Bill rows: Open States latest action |
| check_date | 2026-11-19 |

---

## Source register

| ID | Source | Type | Date | URL |
|---|---|---|---|---|
| G-S01 | Open States full-text bill search, both phrasings × 51 jurisdictions, plus unfiltered runs and control phrase | aggregator [S] | run 2026-11-19 | https://open.pluralpolicy.com/search/?query=%22donor+advised%22 |
| G-S02 | open.pluralpolicy.com robots.txt | robots | read 2026-11-19 | https://open.pluralpolicy.com/robots.txt |
| G-S03 | Florida Senate bill-text search, 2021–2026, all versions and amendments | official [F] | run 2026-11-19 | https://www.flsenate.gov/Session/Bills/2025?chamber=both&searchOnlyCurrentVersion=False&isIncludeAmendments=True&SearchQuery=%22donor+advised%22 |
| G-S04 | Massachusetts Legislature search, 194th Court | official [F] | run 2026-11-19 | https://malegislature.gov/Bills/Search?SearchTerms=%22donor+advised%22 |
| G-S05 | NC SB 684 (2025) v1 | official [F] | 2025-03-25 | https://www.ncleg.gov/Sessions/2025/Bills/Senate/PDF/S684v1.pdf |
| G-S06 | MO HB 1181 (2257H.01I) and HB 2216 (4074H.01I) | official [F] | 2025; 2025-12 | https://documents.house.mo.gov/billtracking/bills251/hlrbillspdf/2257H.01I.pdf ; https://documents.house.mo.gov/billtracking/bills261/hlrbillspdf/4074H.01I.pdf |
| G-S07 | MS SB 2210 (2019, as sent to Governor); SC 555 (2023); SR 17 (2025) | official [F] | 2019; 2023; 2025 | https://billstatus.ls.state.ms.us/documents/2019/html/SB/2200-2299/SB2210SG.htm ; https://billstatus.ls.state.ms.us/documents/2023/pdf/SC/SC0555SG.pdf ; https://billstatus.ls.state.ms.us/documents/2025/pdf/SR/SR0017IN.pdf |
| G-S08 | OH SB 12 (136th) and SB 309 (135th), as introduced | official [F] | 2025; 2024 | https://search-prod.lis.state.oh.us/api/v2/general_assembly_136/legislation/sb12/00_IN/pdf ; https://search-prod.lis.state.oh.us/api/v2/general_assembly_135/legislation/sb309/00_IN/pdf |
| G-S09 | HI HB 992 (and HD1), SB 1311 (2025); SB 1048 and SD1 (2025); Acts 205 (2024) and 108 (2025) | official [F] | 2024–2025 | https://data.capitol.hawaii.gov/sessions/session2025/bills/HB992_HD1_.PDF ; https://data.capitol.hawaii.gov/sessions/session2025/bills/SB1311_.PDF ; https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2025/SLH2025_Act108.pdf ; https://data.capitol.hawaii.gov/sessions/sessionlaws/Years/SLH2024/SLH2024_Act205.pdf |
| G-S10 | NJ P.L.2018, c.29 | official [F] | 2018-05-30 | https://pub.njleg.gov/Bills/2018/PL18/29_.PDF |
| G-S11 | Iowa Code 15E.303, 15E.305; N.D.C.C. ch. 57-38 | official [F] | current | https://www.legis.iowa.gov/docs/code/15E.305.pdf ; https://ndlegis.gov/cencode/t57c38.pdf |
| G-S12 | IL HB 3475, SB 3778, HB 4462 / 205 ILCS 305/39 (search-engine snippets of ilga.gov pages) | official URL, snippet [S] | read 2026-11-19 | https://ilga.gov/legislation/102/HB/10200HB3475.htm ; https://ilga.gov/documents/legislation/104/SB/PDF/10400SB3778.pdf ; https://ilga.gov/legislation/ilcs/documents/020503050K39.htm |
| G-S13 | WI AB 665 (search-engine snippets; FastDemocracy listing) | snippet [S] | read 2026-11-19 | https://fastdemocracy.com/bill-search/wi/2025-2026/bills/WIB00015399 |
| G-S14 | CA AB 576 (search-engine snippets; Digital Democracy) | snippet [S] | read 2026-11-19 | https://calmatters.digitaldemocracy.org/bills/ca_202520260ab576 |
| G-S15 | AK AS 43.23.130(k) (FindLaw mirror via snippet) | snippet [S] | read 2026-11-19 | https://codes.findlaw.com/ak/title-43-revenue-and-taxation/ak-st-sect-43-23-130/ |
| G-S16 | State DAF law tracker (T01, T03, T06–T08, T12–T14, T20–T23) | repo [S] | 2026-11-15 | [direction-state-daf-law-tracker.md](direction-state-daf-law-tracker.md) |
| G-S17 | Validation wave 25A, V25A-17 | repo | 2026-11-15 | [validation-wave25a-report.md](validation-wave25a-report.md) |
| G-S18 | robots.txt of 51 official legislature hosts | robots | read 2026-11-19 | logged per state in the CSV column `robots_official_host` |

## 7. Queue proposals

See [`queue-proposals-gap19-14.csv`](../../data/mission-2026-11-14/queue-proposals-gap19-14.csv):
- **P-G1914-01:** check Connecticut by a permitted route.
- **P-G1914-02:** run official full-text searches for the large and thin-index states.
- **P-G1914-03:** read the in-window texts not yet read.
- **P-G1914-04:** inventory DAF treatment in state endowment credits, which runs both ways.
- **P-G1914-05:** check use of the NJ conversion-asset rule and any similar laws elsewhere.
