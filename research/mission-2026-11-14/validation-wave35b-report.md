# Validation wave 35B: Ren private-label defaults (P-B4428-02) and national 990 reads (P-G07-02, P-B45N31-02)

- **Validator:** independent-validation-agent-wave35b · **Date:** 2026-11-19
- **Register:** [`data/mission-2026-11-14/validation-register-wave35b.csv`](../../data/mission-2026-11-14/validation-register-wave35b.csv) (40 claims, V35B-01 to V35B-40).
- **Studies checked:**
  - [b4428-02-ren-private-label-defaults.md](b4428-02-ren-private-label-defaults.md), its CSV and `scripts/mission_b4428_02_ren_defaults_build.py`;
  - [g0702-b4531-national-990-reads.md](g0702-b4531-national-990-reads.md), its two CSVs and `scripts/mission_national_990_reads.py`;
  - the earlier [b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md), read with its wave-34A governing corrections ([validation-wave34a-report.md](validation-wave34a-report.md)).
- **Method.**
  - A separate robots-respecting fetcher (scratchpad `v35b/scripts/get.py`, UA `research-script/1.0`) fetched a URL only if robots.txt allowed both `*` and that UA; a 404 robots.txt counted as no rules.
  - 49 requests were made: 45 fetched, 1 allowed but 404 (Fidelity 2022-21 audit, as the study says), and 3 refused by robots (gspf.goldman.com and rj.iphiview.com `Disallow: /`; www.dafgiving360.org robots.txt 403).
  - Form 990 values were read from the XML with my own parser, not from the study's extract cache.
  - Both scripts were re-run into scratch. The Ren script rebuilt its CSV byte for byte. The 990 script, with a fresh extract cache, rebuilt both CSVs byte for byte (md5 `73ee9257…` and `3d83f7d2…`).
  - crt.sh, certspotter and sec.gov were not used. There was no outreach and no login, and the user agent was not changed.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| Ren private-label defaults (V35B-01 to -20) | 20 | 12 | 5 | 3 | 0 |
| National 990 reads (V35B-21 to -40) | 20 | 13 | 7 | 0 | 0 |
| **Total** | **40** | **25** | **12** | **3** | **0** |

## Findings: Ren private-label defaults

**Documents, dates and hashes: confirmed (V35B-01, -03 to -06).**
- All seven copies of the "Giving Platform Donor User Guide" re-fetched with SHA-1 `93d97b49e84a…`. The paths are on the rcf, ampf, rbcrcf, mdrt, rcfgivingfund, ubs and northwesternmutual portals. Each PDF is dated 2026-10-06 20:35:40 UTC, and each carries the "By default, this includes the grant advisor's name, email, and address" sentence verbatim.
- RCF's earlier guide is template `2309-RCF-FRM-DAF-DONORGUIDE` (© 2023). The TDA copy (SHA-1 `789efac9bf3b`, modified 2024-07-12) and the UBS copy (SHA-1 `0025f0fe726a`, modified 2024-06-14) both say "The default is “Fund Name Only”". The UBS portal links both guides.
- Eight other SHA-1 prefixes and thirteen document dates match.
- 31 of the 33 CSV quotes were re-matched verbatim. The remaining 2 come from pages that were not re-fetched.

**Who wrote the full-contact guide (V35B-02): partially confirmed.**
- The 2026-10 guide's text never names RCF or Renaissance. It names Ren once ("Note: Ren does not send any notification ..."), and it was produced with pdf-lib.
- The study calls it "RCF's newest guide". It is better described as a Ren-generic platform guide, shared verbatim by seven RCF tenants.

**Coding.**
- **Counts (V35B-07): confirmed.** 7 / 2 / 6 / 3 / 0 / 10.
- **The not-determinable split (V35B-08): contradicted.** It is 6 rows with no public text and 4 blocked, not 5 and 5.
- **CJP (V35B-09): partially confirmed.** §4.5 of the 2026-04-29 policies reads: "shall identify ... by the name of the Donor Advised Fund ... unless otherwise requested by the Donor". That is a formal floor, so the fund-name coding is defensible.
  - The same PDF's donor section lists details "each at your direction".
  - b44n28-01 still codes CJP as no default stated.
  - Recoding CJP there would move 0.77% of top-20 assets: withholding from 17.2% to 17.9%, and no stated default from 20.9% to 20.1%.
- **AEF (V35B-10): partially confirmed.** "No default stated" holds for which name is used. But AEF's letter always carries a donor or account name and mentions no contact detail, so AEF's 29.8% should not be read as possible full contact.
- **Circular-based rows (V35B-11): partially confirmed.** MDRT, the RCF Giving Fund, Commonwealth and SEI carry the same circular sentence. MDRT and the RCF Giving Fund are coded full contact because they link the 2026 guide; Commonwealth and SEI are coded name only.
- **BofA (V35B-12): confirmed.** The guide says "The default is Fund Name Only". The V34A-30 conflict still applies.

**"Every pre-2026-10 document that states a default says fund name" (V35B-13): contradicted.**
- Four RCF letter-policy texts state what reaches the charity: "will acknowledge the fund and the grant advisor's involvement unless ... anonymous". They are the MDRT circular (2024-04-12), the Commonwealth circular (2024-12-13), the SEI brochure (2025-03-18) and the RCF Giving Fund circular (2025-06-28).
- BofA's 2024 Program Guidelines also name the account and the donor or advisor.
- The study itself codes Commonwealth and SEI "name only". The statement holds only for donor guides that describe the grant screen. The same over-reach is in the bottom line.

**Asset shares (V35B-14): confirmed against the league table.**
- The FY2024 top-50 `daf_assets_eoy` values for all eight sponsors were re-read.
- The implied market is $323.27bn.
- The recomputed shares match to 0.1 points: set A 49.2 / 21.0 / 29.8%; set B 13.1 / 34.9 / 19.9 / 32.1%; sensitivities 70.2% and 48.0%.

**Platform evidence (V35B-15 to -18): confirmed.**
- Seven of the 17 portals were re-checked, including BofA, MS GIFT and CJP. All serve `amplifyui/17570`, `mvc2?v=l-gBG9wYhAn3` and CSS `v=260210093200`.
- The Ren release note on emails (dated 2025-01-15) and the product description ("configurable interface", 2023-06-12) read as quoted.
- Both robots blocks were reproduced.
- The original access log has 177 lines, with the stated split.

**Is "neither sponsor setting nor platform limit is shown" fair? (V35B-19): partially confirmed. The verdict is fair.**
- Guide vintage explains every default stated in a guide, and no two sponsors are documented on the same guide version with different defaults.
- If anything, the lean toward a platform default is understated:
  - the full-contact text is a Ren-generic guide, shared verbatim by seven tenants;
  - it follows a Ren platform release that surfaced elected emails.
- It is still not proven. No non-RCF sponsor has yet published the new guide, and letter wording does vary by RCF template.
- What needs fixing is the supporting sentence (V35B-13), not the verdict.

**b44n28-01 §3.2 "configurable sponsor setting" (V35B-20): contradicted as an inference.**
- The section compares BofA's 2026-02 guide with the 2026-10 Ren platform guide. RCF's own 2024 guide matches BofA, so the comparison tests guide vintage, not sponsor.
- **Integrity problem: six wave-34A governing corrections (b3, b5, b6, b7, b8, b9) were applied truncated.** In each, the text was cut at the first double quote inside the replacement:
  - the §0 confidence cell ends "but says it ";
  - the DAFgiving360 row ends "would code ";
  - the RCF row reads "**Full contact including email:**  No";
  - the GKCCF row reads "name and email  Unknown";
  - the §3 sensitivity bullet ends "unless the ";
  - §3.1 reads "Recommended wording:  |".
- The corrections below restore that text. Every Find and Replace string in this report uses curly quotes (‘ ’) inside, never straight double quotes, so the same truncation cannot recur.

## Findings: national 990 reads

**Re-run (V35B-21): confirmed.**
- 21 returns, 0 failures, 0 EIN mismatches, 488 and 519 rows, and byte-identical CSVs.
- The FX means (1.2049, 1.2597, 1.2948) were recomputed from the saved H.10 page, which was not re-fetched.

**Fidelity (V35B-22 to -25).**
- **Audit Note 3: confirmed.** "Total Advisor-managed Investments at Fair Value" is $37,139,208,368, of "Total Investments at Fair Value" of $79,232,938,398 (46.87%). Pools ($42,093,730,030) plus CIAP add up to the total.
- **Earlier years: confirmed.** 2024: $27,546,211,645 of $61,514,405,850. 2023: $22,433,249,315 of $52,650,176,429. 2022: $18,112,561,857 of $44,823,238,524.
- **Line 11f: confirmed.** The XML `FeesForSrvcInvstMgmntFeesGrp` values (56,692,887; 53,687,639; 67,308,635; 84,317,489) equal the audits' "Investment management fees" to the dollar.
- **Schedule D: confirmed.** DAF value $85,481,718,948, so CIAP is 43.45% of it.
- **The fee reading: partially confirmed.** Note 7 names Strategic Advisers LLC as the Gift Fund's investment adviser, and the audit never describes the fee line. So the line may not be CIAP-only. The study's [I] flag is right, but this alternative reading should be stated.

**DAFgiving360 brackets (V35B-26, -27): partially confirmed. The arithmetic is right, but the labels overstate.**
- **The arithmetic.**
  - The FY2025 top-five "ASSET MANAGEMENT" firms come to $7,201,966: Graystone $2,922,086, Natural Investments $2,142,835, Cerity $1,137,435 and Baker Street $999,610.
  - Divided by 1%, that is 1.52% of $47,352,597,100.
  - Line 11f ($61,372,858) divided by 1% is 12.96%. At 26.49 bps it is 48.9%.
- **Why "hard floor" overstates.** The floor depends on name-based classes and on a 1.00% cap. The cap comes from the December 2024 policy, as quoted in the repo; it was not re-read, because robots.txt returns 403. It is also applied back to FY2021.
- **"Probably at least 13%"** turns a conditional bound into a likelihood without evidence.
- **The scenario** inherits Fidelity's own [I].

**Vanguard (V35B-28): confirmed.**
- Both policy quotes are verbatim ("Updated as of Jan. 9, 2026").
- Line 11f is a filed 0 in FY2021–24, and the FY2025 return has no line-11f group at all.
- No adviser appears in Part VII-B.

**NPT Schedule R (V35B-29, -30): partially confirmed. The values are right, but the line letters are wrong.**
- The script reads `GiftGrntOrCapContriToOthOrgInd`, which is 0 in all five years, and `GiftGrntCapContriFromOthOrgInd`, which is 1.
- These are the 2nd and 3rd of the 19 Part V line-1 indicators (a–s), so they are **lines 1b and 1c**. Line 1d is loans to related organisations (also 0).
- The line-2 type codes C, L and Q in the same returns match the indicators c, l and q, which confirms the mapping.
- No line-2 transaction names NPT UK or Transatlantic.

**NPT Transatlantic and NPT UK accounts (V35B-31 to -33): confirmed.**
- nptuk.org robots.txt allows all.
- The disregarded-entity quote is verbatim.
- **FY2024 grants: confirmed.** Transatlantic granted £47,490k. The material grantees run down to £1,257k, and NPT UK is not among them.
- **FY2023: confirmed.** "a further £68 million in grants in FY23".
- **FY2025 transfer: confirmed.** Note 19 reads: "NPT Transatlantic also granted £30.9m to National Philanthropic Trust UK Limited (NPT UK)". The grant table lists it at 30,939.
- **NPT UK note 14: confirmed.** "Contributions of £30.9M were received from NPT Transatlantic and £30.9M from National Philanthropic Trust".
- **New detail.** Only one FY2025 Part II line exceeds $16.8m (the $39.1m Europe line). So at most one £30.9m receipt can sit in Schedule F as a single line.
- **The upper bound** ($81.9m + $53.0m = $134.9m, 18.2%) recomputes.
  - It is loose. The FY2024 material grantee "Arc Research Institute" (£5,543k) is probably the US Arc Institute, which would make it a Schedule I grant [I].
  - Excluding it gives about $127.9m (17.2%). Either way the figure is still an upper bound.

**Schedule F totals and regions (V35B-34, -35): confirmed.**
- Line 3: $332,153,104 + $410,629,568 = $742,782,672.
- Part II: 413 and 488 lines, all counted on line 2.
- Every regional figure matches my own parse. One mapping call: FY2024's "LATIN AMERICA AND CARIBBEAN" ($31.5m) is placed under Central America and the Caribbean.

**"None of NPT's foreign grants went to related organisations, as filed" (V35B-36): partially confirmed.**
- "As filed" is accurate, but the filed test is weak in two ways:
  - Schedule R Part V covers only organisations listed in Parts II–IV, so Transatlantic is outside it by design;
  - NPT left line 1b at No in FY2025, although its disregarded entity granted £30.9m to NPT UK, a Part II related organisation.
- **FY2024's $0** is also supported by the affiliates' accounts.
- **FY2023's $0** rests on the filing alone, because no Transatlantic grantee list exists for FY2023. For that year $0 means "not reported", not "shown to be zero".

**Other claims (V35B-37 to -40).**
- **Schedule L, Wells Fargo: confirmed.** "WELLS FARGO PROVIDES INVESTMENT MANAGEMENT SERVICES WITH RESPECT TO CERTAIN DAFS AT NPT" appears in FY2023 and FY2024.
- **NPT minimums: partially confirmed.** The guide (PDF 2026-10-15) says "$500,000 for segregated accounts; $2 million for non-discretionary accounts". It does not label the $500k tier "discretionary".
- **Edward Jones: confirmed, but read it narrowly.** Edward Jones is absent from all four sponsors' top fives. That says nothing about Edward Jones adviser DAF assets: the Edward Jones Charitable Gift Fund is RCF's (b4428-02, RCF-14).
- **Downstream repo passages: partially confirmed.** The passages are listed in V35B-40 and corrected below.

## Repo passages these findings change

- `grep -rn "adviser-managed"` in research/:
  - `queue-batch32-infund-costs.md` says "Most NPT assets are adviser-managed or segregated". No source supports this, and P-G07-02 finds the share not estimable.
  - The other hits (Fidelity 46.9%, DAFgiving360 77–78% adviser-*associated*, Vanguard has none, the NPT minimums) agree with the study.
- `grep -rn "Edward Jones"`:
  - `gap19-edward-jones-wealth-channels.md` §4.1 left the Fidelity–Wells Fargo payee to P-G07-02, which now answers it in part.
  - Nothing else conflicts.
- `grep -rn "NPT UK"`:
  - `direction-foreign-grants-schedule-f.md` limit 4 is now tested for NPT.
  - `direction-international-comparison.md` dates the "£84 million" press figure as "year not captured". It is very likely FY2023: Transatlantic's £68m plus NPT UK's £16m is £84m [I].
  - The other hits are unaffected.
- **Strategic synthesis.** `strategic-synthesis.md` §0 E repeats the top-20 full-contact share, which includes RCF on the Ren guide, so it gets a qualifier. No §0 line states an adviser-managed share or an NPT affiliate figure.
- **Related framing.** `gap19-clarity-edf-new-findings.md` §3 says "the default is a sponsor setting". That gets a qualifier.

**Follow-up that is not a Find/Replace.** The NPT CSV repeats the label "Schedule R Part V line 1d" in six rows. These rows are not unique, and the label is generated by the script (`scripts/mission_national_990_reads.py` lines 19, 636, 658 and 664). Relabel to "1b" in the script and rebuild the CSV. No values change.

**Note on §11.36.** Another validator (wave 35A) may insert §11.36 before this one. The Find anchor `\n---\n\n## Source register` occurs exactly once either way, and §11.37 goes immediately before it. The report currently has two identical "### 11.35" headings (wave 34B). They are left as found.

## Exact corrections
Each Find occurs exactly once in the current file (checked by script; see below). Trailing spaces inside Find strings are significant. Within one file, apply the items in the order listed.

### `research/mission-2026-11-14/b4428-02-ren-private-label-defaults.md`

**(§0 not-determinable split (V35B-08))**
- **Find:** "(5 have no public text; 5 are robots-blocked iPhi or GS hosts)"
- **Replace with:** "(6 have no public text: RCF-14 to RCF-17, GCCF-01 and OAK-01; 4 are robots-blocked: RCF-18, GS-01, RJ-01 and the IPHI-00 catch-all row) [V wave 35B]"

**(§0 sponsor-or-platform cell (V35B-13))**
- **Find:** "Every document that states a default *and* predates the 2026-10 guide says **fund name**."
- **Replace with:** "Every donor guide that states a grant-screen default *and* predates the 2026-10 guide says **fund name**. Letter-policy texts of the same period differ: the MDRT, RCF Giving Fund, Commonwealth and SEI circulars (2024–25) name the fund and the grant advisor, and BofA's 2024 Program Guidelines name the account and the donor or advisor [V wave 35B]."

**(Bottom line, guide attribution (V35B-02))**
- **Find:** "- RCF's newest guide moves its programs to **full contact including email**."
- **Replace with:** "- The newest guide on RCF's portals moves seven RCF programs to **full contact including email**. That guide is a Ren-generic ‘Giving Platform Donor User Guide’: its text never names RCF or Renaissance, and it says ‘Ren does not send any notification’ [V wave 35B]."

**(Bottom line, scope of the fund-name statement (V35B-13))**
- **Find:** "- Ren-platform defaults have been **fund name only** in every dated default statement through February 2026."
- **Replace with:** "- Ren-platform donor guides have stated a **fund name only** default in every dated guide through February 2026. RCF letter-policy circulars of 2024–25 instead name the fund and the grant advisor [V wave 35B]."

**(§3.4 suggested wording (V35B-02))**
- **Find:** "RCF's October 2026 'Giving Platform' guide states name, email and address."
- **Replace with:** "The Ren ‘Giving Platform’ guide of October 2026, linked unchanged from seven RCF portals, states name, email and address [V wave 35B]."

**(§6 CJP recoding effect (V35B-09))**
- **Find:** "The same PDF has both texts."
- **Replace with:** "The same PDF has both texts: §4.5 (formal policy) states the fund-name rule, and the donor-facing notification section lists details ‘each at your direction’. Applied to b44n28-01, the recoding moves CJP's 0.77% of top-20 assets from no stated default (20.9% to 20.1%) to withholding (17.2% to 17.9%); that study has not been recoded [V wave 35B]."

### `research/mission-2026-11-14/b44n28-01-donor-info-defaults.md`

**(§3.2 heading)**
- **Find:** "### 3.2 A vendor platform shows two defaults"
- **Replace with:** "### 3.2 A vendor platform shows two defaults, by guide vintage [V wave 35B]"

**(§3.2 lead)**
- **Find:** "Both portals are Ren-administered, and their guides from 2025–26 give different defaults"
- **Replace with:** "Both portals run on Ren's platform (Ren's administration of BofA CGF is inferred, CE0076), and their guides from 2025–26 give different defaults (b4428-02 §3.2) [V wave 35B]"

**(§3.2 RCF bullet)**
- **Find:** "- RCF's DFX guide says the default"
- **Replace with:** "- The Ren ‘Giving Platform Donor User Guide’ on RCF's portal (the same file, SHA-1 93d97b49e84a, on seven RCF portals; its text names Ren, not RCF) says the default [V wave 35B]"

**(§3.2 new bullet)**
- **Find:** "- MS GIFT, also Ren back-office, states a fund-name default in its 2022 Grantee Guidelines."
- **Replace with:** "- MS GIFT, also Ren back-office, states a fund-name default in its 2022 Grantee Guidelines.\n- RCF's own earlier guide (template 2309-RCF-FRM-DAF-DONORGUIDE, ©2023; TDA PDF 2024-07-12, UBS PDF 2024-06-14) says ‘The default is Fund Name Only’, as BofA's does [V wave 35B]."

**(§3.2 verdict (V35B-20))**
- **Find:** "Under EDF this points to a **configurable sponsor setting, not a platform constraint** [I]."
- **Replace with:** "These documents do not show a configurable sponsor setting. BofA's 2026-02 guide and RCF's 2023–24 guide state the same fund-name default, and the full-contact text comes from a newer Ren platform guide, so the two defaults differ by guide vintage, not by sponsor. Whether the change is a sponsor setting or a platform release is unresolved. Under EDF the variation still points to organizational or platform origin, not law (P-B4428-02; b4428-02 §3.4) [V wave 35B]."

**(§0 reconsider-trigger paragraph)**
- **Find:** "and it now appears even within a single vendor platform (Ren; §3.2)."
- **Replace with:** "and it also appears on a single vendor platform (Ren; §3.2), where the stated default tracks guide vintage rather than sponsor (b4428-02) [V wave 35B]."

**(§3.1 RCF row)**
- **Find:** "RCF's own 2026-10 DFX guide defaults to **name, email and address**"
- **Replace with:** "The Ren ‘Giving Platform’ guide on RCF's portals (2026-10) defaults to **name, email and address**; RCF's 2023–24 guide said Fund Name Only (b4428-02) [V wave 35B]"

**(§8 S17)**
- **Find:** "| S17 | RCF, DFX Donor User Guide |"
- **Replace with:** "| S17 | RCF portal, Ren ‘Giving Platform Donor User Guide’ (same file on seven RCF portals, SHA-1 93d97b49e84a) [V wave 35B] |"

**(§2 RCF row: restores wave-34A (b6) text lost in application)**
- **Find:** "| 9 | RCF | 5.91 | **Full contact including email:**  No"
- **Replace with:** "| 9 | RCF | 5.91 | **Full contact including email:** ‘By default … name, email, and address’ (Ren ‘Giving Platform’ guide on RCF's portal, 2026-10-06). The RCF Program Circular (PDF modified 2026-07-23) lists options with no default, RCF's own 2023–24 guide says ‘The default is Fund Name Only’, and private-label programs such as TSA's carry their own defaults, so this is an upper bound for RCF's $5.91bn. Coded by the 2023–24 guide, top-20 full contact would be 30.9% and withholding 19.5% [V wave 34A] | No [V wave 35B]"

**(§0 confidence cell: restores wave-34A (b3) text)**
- **Find:** "Its 2024 policy lists options without a default, but says it "
- **Replace with:** "Its 2024 policy lists options without a default, but says it ‘does not release the account holder's name and contact information to any recipient charity without the account holder's explicit consent’, which leans toward withholding when no choice is made [V wave 34A] [V wave 35B]"

**(§2 DAFgiving360 row: restores wave-34A (b5) text)**
- **Find:** "and under §1.5 that text alone would code "
- **Replace with:** "and under §1.5 that text alone would code ‘no default stated’, as NPT is coded. It adds that DAFgiving360 ‘does not release the account holder's name and contact information ... without the account holder's explicit consent’ [V wave 34A] [V wave 35B]"

**(§2 GKCCF row: restores wave-34A (b7) text)**
- **Find:** "| 16 | GKCCF | 2.57 | **Fund name only:** name and email  Unknown"
- **Replace with:** "| 16 | GKCCF | 2.57 | **Fund name only:** name and email ‘encouraged’, donor decides. GKCCF also says the check stub ‘will likely include the donor's name and contact information (typically an email address)’. Coded the way CJP is, this would be ‘no default stated’, and the withheld share would fall to 16.1% [V wave 34A] | Unknown [V wave 35B]"

**(§3 sensitivity bullet: restores wave-34A (b8) text)**
- **Find:** "  - Either way, **no reading makes contact-withholding the asset-weighted majority** unless the "
- **Replace with:** "  - Either way, **no reading makes contact-withholding the asset-weighted majority** unless the ‘donor chooses’ sponsors effectively send no contact data. That condition is not remote. If DAFgiving360's explicit-consent clause means no contact without an election, and NPT, AEF and CJP likewise send none unless it is chosen, withholding when no choice is made would cover 33.5% + 20.9% = 54.4% of top-20 assets. The asset-weighted answer is therefore open, not settled against withholding [V wave 34A] [V wave 35B]"

**(§3.1 recommended wording: restores wave-34A (b9) text)**
- **Find:** "Recommended wording: "
- **Replace with:** "Recommended wording: ‘defaults vary. A documented full-contact default covers 33–50% of top-20 assets and a documented withholding default 17–34%; both ranges turn on DAFgiving360. The default is undocumented for the rest, and no top-20 sponsor defaults to anonymous’ [V wave 34A] [V wave 35B]"

**(§2 CJP row (V35B-09))**
- **Find:** "| 18 | CJP | 1.93 | **Donor chooses:**"
- **Replace with:** "| 18 | CJP | 1.93 | **Donor chooses** (but Policies §4.5 state a fund-name rule ‘unless otherwise requested’; coded by it, as in b4428-02, withholding would be 17.9% and no stated default 20.1%) [V wave 35B]"

### `research/mission-2026-11-14/g0702-b4531-national-990-reads.md`

**(§0 NPT row (V35B-29, -36))**
- **Find:** "**To NPT UK and other related organisations: $0 as filed.** Schedule R Part V line 1d"
- **Replace with:** "**To NPT UK and other related organisations: $0 as filed, within Schedule R Part V's scope (related organisations in Parts II–IV; disregarded entities such as NPT Transatlantic are outside it).** Schedule R Part V line 1b (XML GiftGrntOrCapContriToOthOrgInd; line 1d is loans) [V wave 35B]"

**(§0 FY2025 row)**
- **Find:** "NPT's FY2025 Schedule R line 1d is still"
- **Replace with:** "NPT's FY2025 Schedule R line 1b (not 1d) is still [V wave 35B]"

**(§1.6 step 1)**
- **Find:** "These are taken from Schedule R Part V line 1d and line 2 transactions naming NPT UK or Transatlantic."
- **Replace with:** "These are taken from Schedule R Part V line 1b (XML GiftGrntOrCapContriToOthOrgInd, labelled 1d elsewhere in this study) and line 2 transactions naming NPT UK or Transatlantic. Part V covers only related organisations listed in Parts II–IV, so transfers to or by a disregarded entity such as NPT Transatlantic never appear there [V wave 35B]."

**(§3.3 Schedule R bullet)**
- **Find:** "- **Part V line 1d** (gift, grant or capital contribution to a related organisation) = **No**. Line 1e, the same *from* a related organisation, = Yes."
- **Replace with:** "- **Part V line 1b** (gift, grant or capital contribution to a related organisation) = **No**. Line 1c, the same *from* a related organisation, = Yes. Line 1d (loans to related organisations) is also No [V wave 35B]."

**(§3.4 990 bullet)**
- **Find:** "- NPT's FY2025 Schedule R line 1d"
- **Replace with:** "- Because NPT Transatlantic is disregarded, its £30.9m grant is NPT's own grant to a Part II related organisation, so line 1b should read Yes; NPT's FY2025 Schedule R line 1b [V wave 35B]"

**(§3.3 answer (V35B-36))**
- **Find:** "- **To NPT UK and other affiliates:** $0 of FY2023–24's $742.8m, as filed and as far as the affiliates' accounts show."
- **Replace with:** "- **To NPT UK and other affiliates:** $0 of FY2023–24's $742.8m as reported. The filed test is weak: Schedule R Part V line 1b excludes disregarded entities, and NPT left it at No in FY2025 despite the £30.9m grant. FY2024 is also supported by the affiliates' accounts (NPT UK is not among Transatlantic's material grantees, and NPT UK's 2024/25 note 14 gives no 2023/24 comparative for affiliate contributions). FY2023 has no grantee list, so for that year $0 means not reported, not shown to be zero [V wave 35B]."

**(§0 DAFgiving360 (V35B-26))**
- **Find:** "- **hard floor 1.5%** of DAF value (FY2025)"
- **Replace with:** "- **floor 1.5%** of DAF value (FY2025), conditional on the name-based contractor classes and on the 1.00% cap (December 2024 policy, repo quote) applying in every year [V wave 35B]"

**(§2.4 best available statement (V35B-27))**
- **Find:** "DAFgiving360's adviser-managed share is at least 1.5% (hard floor) and probably at least 13% (if line 11f is adviser fees)."
- **Replace with:** "DAFgiving360's adviser-managed share is at least 1.5% if the identified firms' payments are adviser fees capped at 1.00%, and at least 13% only if line 11f is entirely such fees; neither condition is documented [V wave 35B]."

**(§2.3 readings (V35B-24))**
- **Find:** "This suggests many CIAP mandates are priced low, or that part of the adviser pay is billed outside the account [I]."
- **Replace with:** "This suggests many CIAP mandates are priced low, or that part of the adviser pay is billed outside the account [I]. A third possibility is that the line is not CIAP-only: the audit does not describe it, and Note 7 names Strategic Advisers LLC, a Fidelity company, as the Gift Fund's investment advisor [V wave 35B]."

**(§0 Part VII-B row (V35B-39))**
- **Find:** "**Edward Jones** appears in no sponsor's top five in any year [F]."
- **Replace with:** "**Edward Jones** appears in no sponsor's top five in any year [F]. This says nothing about Edward Jones adviser DAF assets: the Edward Jones Charitable Gift Fund is sponsored by RCF, outside these four sponsors (b4428-02 RCF-14) [V wave 35B]."

**(§3.3 table FY2024 (V35B-32))**
- **Find:** "£5.44m (EERC Inc. £3.339m; Brown University £2.102m)"
- **Replace with:** "£5.44m (EERC Inc. £3.339m; Brown University £2.102m). Arc Research Institute (£5.543m) is not excluded; if it is the US Arc Institute [I], the bound falls to about $46.0m and the pooled bound to about $127.9m (17.2%) [V wave 35B]"

**(§3.4 reading (V35B-33))**
- **Find:** "the size match is suggestive, not proof."
- **Replace with:** "the size match is suggestive, not proof. No other FY2025 Part II line exceeds $16.8m, so at most one of the two £30.9m receipts in NPT UK's note 14 can sit in Schedule F as a single line [V wave 35B]."

**(§0 NPT minimums (V35B-38))**
- **Find:** "$500k (discretionary) or $2m (non-discretionary)"
- **Replace with:** "$500k (segregated accounts) or $2m (non-discretionary accounts), in the DAF Guide's wording [V wave 35B]"

**(§2.5 NPT minimums (V35B-38))**
- **Find:** "- **Minimums:** $500,000 for discretionary accounts and $2 million for non-discretionary accounts."
- **Replace with:** "- **Minimums:** $500,000 for segregated accounts and $2 million for non-discretionary accounts; the guide does not call the $500k tier discretionary [V wave 35B]."

**(§0 Vanguard (V35B-28))**
- **Find:** "Line 11f is $0 in every year FY2021–25"
- **Replace with:** "Line 11f is $0 in FY2021–24 and blank (not reported) in FY2025 [V wave 35B]"

### `research/mission-2026-11-14/queue-batch32-infund-costs.md`

**(NPT row)**
- **Find:** "Most NPT assets are adviser-managed or segregated"
- **Replace with:** "NPT's adviser-managed share is not estimable: segregated accounts need $500,000, and line 11f mixes model-portfolio advisory fees with segregated-account fees (g0702-b4531 §2.5) [V wave 35B]"

### `research/mission-2026-11-14/gap19-edward-jones-wealth-channels.md`

**(§4.1 Wells Fargo)**
- **Find:** "This is most likely Fidelity's adviser-managed account programme. The return does not say so (P-G07-02)."
- **Replace with:** "This is most likely Fidelity's adviser-managed account programme. The return does not say so. P-G07-02 (g0702-b4531) finds that Fidelity's audited investment management fees equal line 11f to the dollar in FY2022–25 and that CIAP held 46.9% of investments at June 2025. That is consistent with this reading but does not name the payee programme [V wave 35B]."

### `research/mission-2026-11-14/direction-foreign-grants-schedule-f.md`

**(Limit 4)**
- **Find:** "They are not netted here because Schedule F has no recipient name (P-B45N31-02)."
- **Replace with:** "They are not netted here because Schedule F has no recipient name (P-B45N31-02). For NPT, g0702-b4531 finds no filed related-organisation grant in FY2023–24 (Schedule R Part V line 1b = No). But Part V does not cover disregarded entities such as NPT Transatlantic, and in FY2025 Transatlantic granted £30.9m to NPT UK while line 1b stayed No [V wave 35B]."

### `research/mission-2026-11-14/direction-international-comparison.md`

**(NPT UK grants)**
- **Find:** "(press-release headline; year not captured)"
- **Replace with:** "(press-release headline; very likely FY2023, since NPT Transatlantic's £68m and NPT UK's £16m for FY23 in the 2023 grantmaking report sum to £84m [I]) [V wave 35B]"

### `research/mission-2026-11-14/gap19-clarity-edf-new-findings.md`

**(§3 organizational origin)**
- **Find:** "the default is a sponsor setting, and it varies widely under one federal regime (36/24/35/1)."
- **Replace with:** "the default is set by the sponsor or its platform vendor, and it varies widely under one federal regime (36/24/35/1). On Ren's platform the stated default tracks guide version, not sponsor (b4428-02) [V wave 35B]."

### `research/mission-2026-11-14/strategic-synthesis.md`

**(§0 E nonprofit identity bullet)**
- **Find:** "Full contact is documented for 33.2% of assets (Fidelity, RCF, NCF, ImpactAssets, FFTC) and withholding for 17.2%"
- **Replace with:** "Full contact is documented for 33.2% of assets (Fidelity, RCF, NCF, ImpactAssets, FFTC) and withholding for 17.2%. RCF's 2.4% rests on Ren's October 2026 ‘Giving Platform’ guide; RCF's own 2023–24 guide said Fund Name Only, which would make the split 30.9% and 19.5% (b4428-02) [V wave 35B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**(New §11.37)**
- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.37 Ren defaults and national 990 reads (validated, wave 35B)\n\n" + "**Ren defaults and national 990 reads** (validated, wave 35B). Of 28 Ren-linked programmes, 7 default to full contact including email, and all 7 rest on one Ren-generic ‘Giving Platform Donor User Guide’ (2026-10-06, SHA-1 93d97b49e84a) whose text never names RCF. RCF's own 2023–24 guide said ‘The default is Fund Name Only’, as BofA's 2026 guide does, so on Ren the stated default tracks guide vintage. That does not show a configurable sponsor setting, and it does not prove a platform default. On FY2024 assets, Ren-administered sponsors split 49.2% fund name only, 21.0% full contact (an upper bound) and 29.8% with no stated default. Fidelity's audited advisor-managed investments were $37.14bn of $79.23bn (46.9%, June 2025), and its investment management fees equal line 11f to the dollar. Vanguard Charitable has no adviser-managed option, and DAFgiving360's share is unpublished. NPT's $742.8m of FY2023–24 foreign grants include no filed grant to a related organisation (Schedule R line 1b, not 1d). In FY2025, however, NPT Transatlantic granted £30.9m to NPT UK while line 1b stayed No (repo [`validation-wave35b-report.md`](mission-2026-11-14/validation-wave35b-report.md)) [V wave 35B]" + "\n\n---\n\n## Source register"

The inline paragraph is 176 words, begins with **Ren defaults and national 990 reads** and ends with [V wave 35B].

## Find check

`scratchpad/v35b/build/check.py` reads every target file, counts each Find (`str.count`), and then applies the items in order within each file to confirm that each Find is still unique at its turn. Result on 2026-11-19: **43 items, every Find occurs exactly once, 0 failures.** Every Replace string ends with [V wave 35B], except the §11.37 insertion, which carries its tag at the end of the paragraph. No Find or Replace string contains a straight double quote inside its delimiters.

## Limits

- **Live screens.** No portal grant screen was observed. All defaults are as documented.
- **Coverage.** Seven of the 17 portal build markers were re-checked; the other ten were not.
- **Not re-fetched.** The T. Rowe Price brochure and the AEF charities page.
- **DAFgiving360.** All first-party terms stay unread: robots.txt returns 403.
- **Arc Research Institute.** It is identified as US by name only [I]. No registry was consulted, because sec.gov and outreach are out of scope.
- **NPT UK's note 14.** Whether it describes one transfer or two cannot be settled from the accounts.
