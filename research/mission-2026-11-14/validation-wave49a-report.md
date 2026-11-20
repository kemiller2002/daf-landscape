# Validation wave 49A: bequests and legacy, matching gifts, sponsor governance

**Validator:** validator wave 49A · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave49a.csv`](../../data/mission-2026-11-14/validation-register-wave49a.csv) (43 rows, V49A-01 to V49A-43)

**Studies validated**
- b49-03, bequests and legacy: [`b49-03-bequests-legacy-dafs.md`](b49-03-bequests-legacy-dafs.md), `bequests-legacy-dafs-2026-11-20.csv`, `scripts/mission_b49_03_estate_flows.py`.
- b49-02, matching gifts: [`b49-02-matching-gifts-dafs.md`](b49-02-matching-gifts-dafs.md), `matching-gifts-dafs-2026-11-20.csv`, `scripts/mission_b49_02_matching_gifts.py`.
- b49-05, sponsor governance: [`b49-05-sponsor-governance-quality.md`](b49-05-sponsor-governance-quality.md), `sponsor-governance-quality-2026-11-20.csv`, `scripts/mission_sponsor_governance.py`.

## 1. Method

- **Documents.** Every primary document named in the checklist was downloaded again with a fresh validator fetcher. The fetcher:
  - checks robots.txt for ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot, `research-script/1.0` and `*`, and fetches only if all of them allow the path;
  - treats a robots.txt 404 as "no rules" and any other failure as a disallow;
  - uses the generic user agent `research-script/1.0`.
- **Quotes.** Quotes were re-matched after normalising to lowercase alphanumerics:
  - b49-03: 20 key quotes;
  - b49-02: the clauses of 13 company documents, the Fidelity FAQ, the Vanguard and NPT texts, and the IRS texts.
- **Type-3-font PDFs.**
  - MS GIFT: page 9 of the circular was OCR'd independently (pdftoppm at 300 dpi, then tesseract).
  - BofA v8.2025: the re-download is byte-identical to the study copy. The BofA clause was also confirmed in the v3.2024 text layer.
- **Filings.**
  - **b49-03:** all 20 Form 990 XMLs were re-parsed with a separate script.
  - **b49-05:** all 449 returns were re-parsed. 296 came from local caches. The other 153 were streamed again from the GivingTuesday mirror, whose robots.txt returns 404.
  - Both sets of results were compared with the CSVs field by field.
- **Frame and terms.**
  - **Matching-gift frame:** the Wikipedia `/wiki/` page was re-read and its revision ID checked.
  - **Double the Donation:** robots.txt, the Master Terms and the privacy policy were read.
  - **P&G:** DtD's company page was read.
- **Constraints.** Nothing was fetched from sec.gov, fortune.com, dafgiving360.org, ncfgiving.com or any host on the blocked list. There were no logins, forms or outreach.

### robots.txt log (2026-11-20)

| Host | robots.txt | Fetched |
|---|---|---|
| www.fidelitycharitable.org, www.nptrust.org, www.vanguardcharitable.org, www.svcf.org, donorportal.cct.org, www.fftc.org, jcfny.org, www.bankofamerica.com | 200, allowed | Guidelines, FAQs and policies |
| bofa.donorfirst.org, msgift.donorfirstx.com | 404 (no rules) | BofA v8.2025, MS GIFT circular |
| doublethedonation.com | 200; `*` disallows only `/api/360matchpro/` and there is no AI-agent group | P&G page, DAF article, Master Terms, privacy policy, hosted PDFs |
| files.doublethedonation.com, cdn-dynmedia-1.microsoft.com | 404 (no rules) | Company PDFs |
| www.verizon.com, www.humanafoundation.org, en.wikipedia.org (`/wiki/`), www.irs.gov, www.govinfo.gov | 200, allowed | Rules, FAQ, frame page, Notice 2017-73, i990, 88 FR 77922 |
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 153 XML |

## 2. Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---|---|---|---|---|
| b49-03 Bequests and legacy | 16 | 15 | 1 | 0 | 0 |
| b49-02 Matching gifts | 16 | 14 | 2 | 0 | 0 |
| b49-05 Sponsor governance | 11 | 11 | 0 | 0 | 0 |
| **Total** | **43** | **40** | **3** | **0** | **0** |

The corrections in the final section cover 15 Find/Replace items in five files:
- 4 in b49-03;
- 4 in b49-02;
- 2 in direction-recipients-impact-matching.md (P&G);
- 4 in b49-05;
- 1 in the industry report (§11.73).

## 3. Findings

### 3.1 b49-03, bequests and legacy: accept with small edits

- **Primary terms are all confirmed verbatim against fresh downloads.**
  - **Fidelity:** the 90-day non-response rule and the default to unrestricted funds. The Endowed Giving Program requires $100,000 and runs "not less than five years following the Account Holder's death".
  - **NPT:** succession "can continue in perpetuity". The Endowment Program needs a $100,000 minimum and ends with a lump sum when the balance reaches $25,000.
  - **Vanguard:** "The minimum term for an EGP is five years". Succession runs "Under present guidelines ... in perpetuity", and assets "may be transferred to the Philanthropic Impact Fund". The last phrase is split across two layout columns in pdftotext, but the wording is exact in reading order.
  - **SVCF:** "a maximum of three successor advisors".
  - **CCT:** "maximum of two generations".
  - **FFTC:** no further successors "In the absence of written authorization by the opening donor(s)".
  - **JCF:** "no limit to succession", and no succession plan through a will.
  - **BofA:** "cannot honor succession or beneficiary plans outlined in a will, trust, or other estate[-planning document]", found in both v3.2024 and v8.2025.
  - **MS GIFT:** "reserves the right to limit overall succession on Accounts to a specific number of generations and/or years", confirmed by an independent OCR.
- **Counts are reproduced.**
  - Inflows: 13 bequest, 12 retirement-plan, 11 life-insurance and 8 CRT rows.
  - Defaults: 11 sponsor pool, 2 sponsor discretion, 2 granting history, 3 not found and 2 blocked.
  - No default names a charity. The 11 named-charity rows are all donor elections.
- **990 figures recompute exactly.**
  - Contributions $85,914,142,313, of which noncash $55,399,640,814 (64.48%).
  - DAF contributions $84,932,846,946 (98.86%).
  - Schedule M line 11 $2,536,245,552 (4.58% of Schedule M).
  - 587 Form 8283s across 17 returns.
  - Insurance "Other" lines $1,567,325 across 11 gifts at 4 sponsors (0.0018% of contributions).
  - The XML has no bequest or estate element in Part VIII line 1 or Schedule M, which supports the claim that bequests cannot be measured from the 990.
- **Issues found.**
  1. **"Fixed-term" overstates both programmes.** Fidelity's and Vanguard's programmes set a *minimum* term.
  2. **The summary list of open-ended sponsors leaves out AEF.** The §3.2 comparison counts four.
  3. **"13 of 13" is circular.** Documents were read for 16 sponsors. Three (ImpactAssets, Dechomai and CJP) are silent on inflows, and four are blocked.
- **Not re-verified.** The DAFgiving360 and NCF defaults were carried over from repo work of 2026-11-14 and were not re-checked. The validator respected the same blocks: dafgiving360.org robots.txt returns 403, and the ncfgiving.com terms ban automated extraction.

### 3.2 b49-02, matching gifts: modify the headline

- **The frame is confirmed.** Wikipedia revision 1354288064 is the current revision. Its first table has 100 ranked rows, and every one matches the CSV by rank.
- **Using Double the Donation is acceptable.**
  - Its robots.txt disallows only `/api/360matchpro/` and has no AI-agent group. The file host returns 404.
  - The privacy policy (updated 2025-10-21) names the Master Terms and Conditions as the Terms of Service. Those terms are a client contract: §6.2 binds "Client" use of the website and contains no robot, spider, scraping or automated-extraction clause.
  - The study keeps only a Yes/No flag and a URL per company. This is not use of the services as a client and does not reproduce DtD's database.
- **The headline split reproduces.** 10/6/12/40 (4 eligible plus 6 conditional) and rows B–E all match. The script re-run gives the same output, and a CSV recount agrees.
- **Thirteen company texts were re-read.**
  - The coding of Verizon, Boeing, Humana, Disney, RTX, JPMorgan, Lilly, Travelers, BMS, UnitedHealth, Microsoft, Delta and Merck is confirmed, as are all their dates.
  - Merck's "silent" is a close call. The same ineligible list also bars gifts "to or from an employee or family foundation or charitable trust".
- **The sponsor positions are confirmed.**
  - Fidelity's FAQ says the employer decides and offers a downloadable confirmation.
  - Vanguard (January 2026 PDF, live policies page and FAQ) and NPT use "match" only for investments, asset intake or grant-agreement terms.
- **The IRS texts are confirmed.**
  - Notice 2017-73 contains "match" 0 times.
  - FR 2023-24982 (88 FR 77922) contains "match" 0 times and does contain the deemed-distribution sentence.
- **Five of the six exclusions predate 2021, and this is confirmed.** The six are JPMorgan 2014, IBM 2012, Travelers 2012, Lilly 2017, BMS ≤2020 and Verizon 2024. 18 of the 28 readable texts are pre-2021 or undated.
- **Judgement on the 2021+ rule.**
  - Pre-2021 company guidelines are not evidence of current policy. Programmes change, and P&G's ended in 2016.
  - They may stay in the CSV as flagged context, but they should not drive the headline.
  - **The governing figure should be the 2021+ split: 5 eligible, 1 excluded, 4 silent of 10.**
  - On first-party text alone it is 4/1/3 of 8. This drops the DtD-article quotes for Amex and Bank of America.
  - Any-date shares (14.7% / 8.8%, and 35.7 / 21.4 / 42.9 of 28) should be labelled context.
  - With n = 8–10, "recent documents lean permissive" stays suggestive, as the study already says.
- **P&G (MG10).**
  - DtD's live company page says "Procter & Gamble used to match donations but discontinued their matching gift program on June 30, 2016", with "Matching gift eligible? No". This is confirmed, although the source is secondary.
  - MG10 in `matching-gift-daf-policies-2026.csv` is already flagged pre-2021. However, `direction-recipients-impact-matching.md` still lists P&G as a conditional acceptor. Corrections are given for that file; the CSV is not edited.

### 3.3 b49-05, sponsor governance: accept with notes

- **The XML recompute agrees with the CSV.** Twelve fields were compared across all 449 returns with 0 mismatches: 2a, 2b, 2c, 11a, 12a, 13, 14, 15a, 15b, 25a, Part I line 5 and the Schedule L row count.
- **Prevalence by band is confirmed.**
  - Audits: 128/150 overall; 50/50, 30/30 and 32/32 in the top 50, ≥ $1bn and $100m–$1bn groups; 29/31 in $10m–$100m; 37/57 in < $10m, where 3 have a compilation or review only and 17 have neither.
  - "No" answers on latest returns: COI 8, all sampled sponsors with < $10m; whistleblower 18, which is 17 of those plus American Gift Fund; retention 14, which is 13 plus American Gift Fund.
  - American Gift Fund answers "No" to both 13 and 14 in all three years.
- **Line 15a "No" and staffing.** All 11 top-50 sponsors answering 15a "No" report 0 employees. The i990 quote ("the organization (not a related organization or other third party)") is confirmed.
- **Fidelity's blank answer is confirmed.** Object 202601389349301700 has no `CompensationProcessCEOInd` or `CompensationProcessOtherInd` element. Both are blank in TY2022 and TY2023 as well.
- **Excess benefit.**
  - **NPT:** $131.58, repaid at $137.03 ($5.45 interest). Tax on Schedule L line 2 is $439 / $473 / $34 for TY2022–2024. All confirmed. The TY2024 Part I relationship is "son of donor".
  - **Servant Foundation:** $6,494 of tax is confirmed. Both Part I rows are filed with "transaction corrected" = No, which the note omits.
- **Schedule L.**
  - 20 sponsors (11 top-50, 9 sampled) and 138 rows are confirmed.
  - TY2024 Part IV amounts: Renaissance $19,225,546; Raymond James $14,501,160; DAFgiving360 with Charles Schwab & Co $11,431,175; Vanguard $4,017,439; US Charitable Gift Trust TY2022 $7,749,869.
  - Renaissance's counterparty is Renaissance Administration LLC. The filed relationship is a shared officer, not the founder.
- **The comparisons are confirmed.**
  - The `ctx_comp` values equal the compensation CSV for all 50: 9 at $0, 38 paid, 3 blank.
  - Among the 9 at $0, 15a is 6 No, 2 Yes and 1 blank.
  - R1 ≤ 0 holds at Greater Horizons, NPT, Renaissance, American Gift Fund and Morgan Stanley GIFT. All are audited and have an audit committee and a COI policy.
- **Masking holds.**
  - The validator searched the CSV and the md for:
    - all 4,063 multi-word `PersonNm` values in the 449 XMLs;
    - the person names typed into Schedule L business-name fields;
    - the names in NPT's Part V text.
  - **No natural person's name appears in either file, so no removal is needed.**
  - The masking errs the other way. 18 rows where a filer typed an organisation into the person-name field are masked and labelled `individual`, for example The Vanguard Group Inc, Renaissance Administration LLC and Raymond James Trust NA.

## 4. Accept / modify / reject

| Study | Item | Decision | Reason |
|---|---|---|---|
| b49-03 | Sponsor terms (Fidelity, NPT, Vanguard, SVCF, CCT, FFTC, JCF, BofA, MS GIFT) | Accept | All quotes re-matched in fresh downloads or independent OCR |
| b49-03 | Counts 13/12/11/8; defaults 11/2/2; no named-charity default | Accept, with clarification | Reproduced. "13 of 13" restated as 13 of 16 documents read |
| b49-03 | "Fixed-term" programmes | Modify | The text sets a minimum term |
| b49-03 | Open-ended list in summary | Modify | Add AEF, as in §3.2 |
| b49-03 | 990 figures; bequests unmeasurable | Accept | Recomputed exactly |
| b49-03 | DAFgiving360 and NCF defaults | Accept as carried [R] | Not re-verified (blocked by robots and terms) |
| b49-02 | Frame and DtD sample screen | Accept | Revision current; robots and terms permit |
| b49-02 | Company codings (13 re-read) | Accept | All confirmed; Merck is a close call |
| b49-02 | Headline using any-date evidence | Modify | 2021+ split governs (5/1/4 of 10; 4/1/3 first-party) |
| b49-02 | Sponsor positions; IRS texts | Accept | Confirmed |
| b49-02 / repo | P&G in direction-recipients-impact-matching.md | Modify | Programme discontinued 2016-06-30 (DtD) |
| b49-05 | Prevalence, "No" lists, 15a, Fidelity blank | Accept | 0 mismatches on recompute |
| b49-05 | Excess benefit (NPT, Servant) | Accept, with note | Servant rows filed as not corrected |
| b49-05 | Schedule L totals | Accept, with note | Renaissance is a shared-officer affiliate, not founder |
| b49-05 | Masking | Accept, with note | No names; organisations over-masked as `individual` |
| b49-05 | Comparisons with compensation and resilience | Accept | Reproduced |

## 5. Limits

- The DAFgiving360 and NCF rows, the GS DAF and Raymond James Charitable documents, and the ImpactAssets circular could not be read: they are blocked or return 403.
- IBM's school-district-hosted form and Amex's GlobalGiving documents were not re-read. The Amex host's robots.txt returns 403.
- The DtD company-summary claim (0 of 68 mention DAFs) was not re-checked across all 68 pages. Only P&G's page was re-read.
- The Vanguard policy text was checked against the January 2026 PDF and the live policies page, not the 2026-03-12 PDF the study cites.

## Exact corrections

### `research/mission-2026-11-14/b49-03-bequests-legacy-dafs.md`

**Find:** "1. **Every sponsor with a readable estate-gift document accepts bequests: 13 of 13 [P].**"
**Replace with:** "1. **Every sponsor with a readable estate-gift document accepts bequests: 13 of 13 [P].** That is 13 of the 16 sponsors whose documents were read; the ImpactAssets, Dechomai and CJP documents are silent on inflows, and four sponsors are blocked. [V wave 49A]"

**Find:** "   - **Open-ended by structure:** Fidelity, RCF and BofA. A successor may name further successors."
**Replace with:** "   - **Open-ended by structure:** Fidelity, RCF, BofA and AEF (AEF: no stated limit, “generationally” in its fact sheet), matching the four in the §3.2 comparison. A successor may name further successors. [V wave 49A]"

**Find:** "4. **Fixed-term legacy programmes exist at two sponsors and endowment options at two more [P]:**"
**Replace with:** "4. **Minimum-term legacy programmes exist at two sponsors and endowment options at two more [P]:** [V wave 49A]"

**Find:** "   - **Fixed-term:**"
**Replace with:** "   - **Minimum term (grants run for at least five years; not a fixed term):** [V wave 49A]"

### `research/mission-2026-11-14/b49-02-matching-gifts-dafs.md`

**Find:** "**Only a minority say so in writing. Most say nothing publicly.**"
**Replace with:** "**Only a minority say so in writing. Most say nothing publicly.** Under the repo’s 2021+ evidence rule the governing figure is the 2021+ split: of the 10 companies with a text dated 2021 or later, 5 eligible, 1 excluded and 4 silent (4 / 1 / 3 of 8 on first-party text, without the Amex and Bank of America DtD quotes). The any-date figures below rest mostly on 18 pre-2021 or undated texts and are context only. [V wave 49A]"

**Find:** "| D. Readable 2021+ text | 10 | 5 (50.0%) | 1 (10.0%) | 4 (40.0%) | — |"
**Replace with:** "| D. Readable 2021+ text (governing under the 2021+ rule) | 10 | 5 (50.0%) | 1 (10.0%) | 4 (40.0%) | — |\n| D1. Readable 2021+ first-party text (drops the Amex and Bank of America DtD quotes) | 8 | 4 (50.0%) | 1 (12.5%) | 3 (37.5%) | — [V wave 49A]"

**Find:** "They will find a written exclusion at **1 in 11** (6/68)."
**Replace with:** "They will find a written exclusion at **1 in 11** (6/68). On 2021+ texts alone the documented figures are 5/68 eligible and 1/68 excluded. [V wave 49A]"

**Find:** "5 of the 6 exclusions are pre-2021 or undated (JPMorgan 2014, IBM 2012, Travelers 2012, Lilly 2017, BMS ≤2020) [C]."
**Replace with:** "5 of the 6 exclusions are pre-2021 or undated (JPMorgan 2014, IBM 2012, Travelers 2012, Lilly 2017, BMS ≤2020) [C]. Under the repo’s 2021+ rule these five are context, not evidence of current policy, and the 2021+ split (5 / 1 / 4 of 10; 4 / 1 / 3 of 8 first-party) is the headline. [V wave 49A]"

### `research/mission-2026-11-14/direction-recipients-impact-matching.md`

**Find:** "- P&G (sole donor; 2014 PDF, stale)"
**Replace with:** "- P&G (sole donor; 2014 PDF, stale; DtD’s live company page says P&G discontinued its matching gift program on June 30, 2016, so MG10 in the CSV describes a closed programme and should not be counted) [V wave 49A]"

**Find:** "P&G (2014, stale)"
**Replace with:** "P&G (2014, stale; programme discontinued 2016-06-30 per DtD) [V wave 49A]"

### `research/mission-2026-11-14/b49-05-sponsor-governance-quality.md`

**Find:** "     - Renaissance: $19.2m;"
**Replace with:** "     - Renaissance: $19.2m, paid to Renaissance Administration LLC; the filed relationship is a shared officer (“An officer of RCF is also an officer of Renaissance Administration LLC”), not the founder; [V wave 49A]"

**Find:** "with $6,494 of tax reported."
**Replace with:** "with $6,494 of tax reported. Both Part I rows are filed with “transaction corrected” = No. [V wave 49A]"

**Find:** "A few business names, such as a law firm named after its partners, are therefore masked."
**Replace with:** "A few business names, such as a law firm named after its partners, are therefore masked. Organisation names that filers typed into Schedule L’s person-name field are also masked and labelled `individual`: the validator found 18 such Part I–IV rows (for example The Vanguard Group Inc, Renaissance Administration LLC and Raymond James Trust NA), so `sl_name_type = individual` overstates rows about natural persons. No natural person’s name appears in the CSV or this note. [V wave 49A]"

**Find:** "| `sl_name`, `sl_name_type` | Organisation name as filed, or `[individual]` (also when a person's name was typed in the business-name field) |"
**Replace with:** "| `sl_name`, `sl_name_type` | Organisation name as filed, or `[individual]` (also when a person's name was typed in the business-name field, and when an organisation was typed in the person-name field; see §5 item 6) | [V wave 49A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.73 Bequests, matching gifts and sponsor governance (validated, wave 49A)\n\n**Bequests, matching gifts and sponsor governance** (validated, wave 49A). Fresh downloads confirm the estate terms: Fidelity moves an unclaimed account to its unrestricted funds after 90 days and offers a $100,000 Endowed Giving Program lasting at least five years; NPT and Vanguard let succession run “in perpetuity”; SVCF caps successors at three and CCT at two generations; BofA and JCF refuse succession plans set by will. No top-20 default goes to a named charity, and the 990 figures recompute exactly ($85.91bn of contributions, 64.5% noncash, $2.54bn on Schedule M line 11). The 990 has no bequest line. The matching-gift split (10 eligible, 6 excluded, 12 silent, 40 without public text) reproduces, but 18 of the 28 texts predate 2021. Under the repo rule the governing figure is 5 eligible, 1 excluded and 4 silent of 10 texts dated 2021 or later (4/1/3 on first-party text). P&G ended its programme in 2016. The governance answers match the XML for all 449 returns, and no individual is named (repo [`validation-wave49a-report.md`](mission-2026-11-14/validation-wave49a-report.md)). [V wave 49A]\n\n---\n\n## Source register"
