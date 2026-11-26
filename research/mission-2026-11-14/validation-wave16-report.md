# Validation wave 16: batch 31 claims (adviser fees and hidden costs, Endaoment FY2025, Every.org reclassification, Fidelity Charitable feeds, Ren for Charities rail, NPact entity, Foundation Cloud GLs)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave16.
**Register:** [`validation-register-wave16.csv`](../../data/mission-2026-11-14/validation-register-wave16.csv), rows V16-01 to V16-30.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs or contact anyone. I fetched no `*.fcsuite.com` page. For each claim I formed a verdict from primary sources first and compared it with the batch-31 documents afterwards. I do not reproduce bank details or the NPact EIN seen on public pages. The sources were:
- **IRS XML:** re-parsed with a stdlib script, from the GivingTuesday mirror: AEF TY2022–24, RCF TY2024, MS GIFT, GS DAF and BofA CGF TY2024, Raymond James FY3/24, Endaoment FY6/24, Every.org 990-PF CY2023–24, Santa Barbara TY2024, Nevada FYE 6/25.
- **Endaoment FY2025:** pulled myself from the IRS zip `2026_TEOS_XML_05B.zip` by HTTP range request at the stated offset. I wrapped the local entry in a minimal zip and inflated the Deflate64 member with `unzip`. I also checked the 2026 index row.
- **IRS other:** the EO BMF (`eo_ca.csv`, Last-Modified 2026-11-09), the 990-PF instructions (2025), IRC §408 (Cornell LII), and Every.org's Letter 4422 (Drive PDF, 2 pp; my own tesseract OCR at 300 dpi).
- **ADV brochures** (pdftotext): Davenport (2024-03-25), Tolleson (2026-01-29), Hollencrest (2025), Strategic Advisers (IAPD), Waverly (2025-09-23). The BMO PDF and the Commonwealth page returned 403.
- **The GS DAF circular** (FireAid App. B, pp. 13–16).
- **Data-feed sources:** Addepar product pages and its portfolio-feed directory HTML, Fidelity Charitable's adviser page, the Empower and Every.org Zendesk JSON, the eMoney post (with page metadata) and the Intuit `fidir.txt`.
- **Ren:** the Ren `app.js` bundle (Last-Modified 2026-11-04), Ren Intercom articles, the Ren Giving Season FAQ and AEF charities page (both via WebFetch, because curl got 403 on the Ren FAQ).
- **NPact:** its WordPress media listing and both W-9 PDFs (pdftotext and OCR), its Terms of Use and Standard Terms, and the Texas Comptroller open data.
- **Santa Barbara Foundation:** its posting on nprnsb.org (WebFetch). The San Diego Workable posting returned 429.
- **Repo files:** `spectrumportal-portal-vs-ledger-v3.csv`, `dafrc-sponsor-schedule-d-fy2019-2024.csv` and the Oakland Voices article (WebFetch).

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V16-01 | AEF 11f = "Schedule D Part XII line 4b": $26.37m / $29.49m / $35.95m | **Partially confirmed** | Amounts and the $1,328.2m → $1,364.2m reconciliation are exact. **The add-back is Part XII line 4a** ("Investment expenses not included on Form 990, Part VIII, line 7b"; XML `InvestmentExpensesNotIncld2Amt`), not 4b. Line 4b is "Other": BofA CGF's own Schedule O puts "RECOVERIES … GRANT ADJ" under Part XII line 4b. |
| V16-02 | AEF bps, per-account, mean balance, sensitivity | **Confirmed** | 39.6/44.0/46.2 bps; $1,876/$2,005/$2,254; $443k/$483k/$525k; 92/62/46/37/31%. |
| V16-03 | RCF 11f $11.69m, 23.2 bps, $453 | **Confirmed** | Same line-number issue (4a, not 4b). |
| V16-04 | Davenport/RCF DAF wrap menu | **Confirmed** | Tiers are verbatim, and the RCF admin fee is "in addition". The minimums are simplified: the FundAdvisor/ETFAdvisor SMA models have a $50k minimum, and the $1m minimum applies only to Core Leaders, V&I, Equity Opportunities and Fixed Income SMAs. |
| V16-05 | Tolleson 0.40–1.00%, NPT engagement | **Confirmed** | Brochure dated 2026-01-29. |
| V16-06 | Hollencrest: NPT pays 5–25 bps | **Confirmed** | The fee base is assets "introduced to NPT by the third parties", so it is referral-like. |
| V16-07 | Strategic Advisers: CGF fund expenses "not separately itemized or billed" | **Confirmed** | |
| V16-08 | Waverly 2025-09-23 DAF section | **Confirmed** | |
| V16-09 | BMO 0.25% [R]; Commonwealth ≤5 bps [R] | **Unverifiable** | Both returned 403. The doc's [R] label is right. |
| V16-10 | MS GIFT 28.1 bps; 7.8% of the 1.00% ceiling; 0.07% = $5.7m | **Confirmed** | Recomputed 7.75%: ($4,237,948 + $2,028,620) / $80.86m. Treating "FA commissions and misc." as advisory-type is [I]. |
| V16-11 | GS DAF 28.7 bps; admin bound 26.4 bps ($28.6m); GSAM 0.62–0.67% | **Confirmed** | The marginal schedule at the $3,057,792 mean gives 26.35 bps. GGSIX and GOIIX are 0.62% and GIPIX 0.67% (FGTXX 0.18% sits outside the range). |
| V16-12 | BofA 11f $24.06m = 52.0 bps; "trustee fees" | **Confirmed** | Part III activity 2: "BANK OF AMERICA TRUSTEE FEES" $9,624,864. No Part XII investment add-back. |
| V16-13 | RJ Schedule O; 69.6 bps; add-back | **Confirmed** | |
| V16-14 | Oakland Voices: 274 platforms; Benevity, Blackbaud, PayPal | **Confirmed** | The article body says "as of Nov. 28" and the methodology says Nov. 30. |
| V16-15 | Endaoment object in 05B, not 05A; offset, Deflate64, sizes | **Confirmed** | Local header at 298,203,445: method 9, 14,650/105,932 bytes. |
| V16-16 | Endaoment FY2025: 1,213 DAFs / $25.03m / $18.68m / $18.9m; Part VIII $24.33m noncash; PSR identity | **Confirmed** | Exact. |
| V16-17 | Crypto 1,430 contributions; PRI split; Schedule I; self-grant; SingerLewak; PPA | **Confirmed** | The net-asset roll reconciles exactly. FY2024 and DAFRC rows match. |
| V16-18 | Letter 4422 (2025-10-23): 507(b)(1)(B), retroactive to 2020-01-01, 170(b)(1)(A)(vi) | **Confirmed** | My own OCR. "60-month" comes from the instructions, not the letter. |
| V16-19 | 990-PF filing rule; BMF codes; 4940 $891 / $9,853; Schedule B 248/530; no Item F | **Confirmed** | The privacy change is prospective only: the five filed 990-PF Schedules B stay public. I checked Item F for 2023–24 only. |
| V16-20 | QCDs into giving credit since 2026-09; "QCDs cannot go to a DAF (408(d)(8)(B)(ii))" | **Partially confirmed** | The facts are confirmed (articles created 2026-09-11). **The citation is wrong:** the 170(b)(1)(A)/509(a)(3)/4966(d)(2) limits are in **§408(d)(8)(B)(i)**. (B)(ii) is the age-70½ condition. |
| V16-21 | Help centre's "509(a)(2) and 170(b)(1)(A)(vi)" overstatement | **Confirmed** | |
| V16-22 | Addepar Fidelity CGF/DAF feed; G-Number; the only DAF feed | **Confirmed** | Last updated 09-09-2026. The directory has no other charitable or DAF product. |
| V16-23 | Fidelity Charitable G Number; Empower; eMoney | **Partially confirmed** | FC and Empower are verbatim (created 2024-04-03, updated 2025-12-06). **The eMoney post is dated 2023-04-17** in its page metadata. It is not undated. |
| V16-24 | Intuit `fidir.txt`: no Fidelity Charitable row; T. Rowe Price on `pcg.donorfirstx.com` | **Confirmed** | 16,460 lines, against the doc's 16,458 (cosmetic). |
| V16-25 | Ren `app.js` enum: RDE_ACH = "Ren for Charities ACH"; Legacy codes | **Confirmed** | The enum also has UNKNOWN. |
| V16-26 | Ren help (Legacy, "all ACH … DAF programs", "25+"); FAQ "updated 12/29"; AEF "Powered by Ren" | **Confirmed** | The FAQ 7 ACH instruction is general, as the doc says. MS GIFT stays "probable". |
| V16-27 | NPact W-9s: Dallas (PDF modified 2024-02-29) → Wakefield (uploaded 2025-07-23); both "P" | **Confirmed** | **The 2025 PDF was created 2025-07-08**, which tightens the bound. EIN not reproduced. |
| V16-28 | NPact terms (MA law, Boston venue, "Delaware corporation"); Texas BroadWest `X`/`U` | **Confirmed** | |
| V16-29 | Santa Barbara FE NXT posting; Fusion Labs "HOSTED INFRASTRUCTURE" $130,000 | **Confirmed** | Posted Nov 6, 2025. TY2024 VII-B is exact. |
| V16-30 | v3 split 52.5 / 37.0 / 10.4%; San Diego upgraded to medium | **Partially confirmed** | The arithmetic is exact ($2,459.6m). The San Diego posting could not be re-read (429), so the upgrade rests only on the doc's [R] capture. San Diego is $708m. |

**Tally:** 25 confirmed, 4 partially confirmed, 0 contradicted, 1 unverifiable.

## Exact corrections

### `research/mission-2026-11-14/queue-batch31-fees-costs.md`
1. **Line 29 (§0, P-ADV-02).** Replace "Schedule D Part XII line 4b equals line 11f in every year" with "Schedule D Part XII line 4a ('investment expenses not included on Form 990, Part VIII, line 7b') equals line 11f in every year".
2. **Line 40 (§1.1 table header).** Replace "Sch D Part XII line 4b (netted in the audit)" with "Sch D Part XII line 4a (netted in the audit)".
3. **Line 93 (§1.4).** Replace "Schedule D Part XII line 4b nets the same amount" with "Schedule D Part XII line 4a nets the same amount".
4. **Line 175 (§5 item 1).** Replace "(Schedule D Part XII line 4b)" with "(Schedule D Part XII line 4a)". Part XII line 4b is "Other": BofA CGF's TY2024 Schedule O uses it for "RECOVERIES … GRANT ADJ" [V wave 16].
5. **Line 106 (§2, Davenport row).**
   - Replace: "Minimums: $50k (models), $1m (SMAs)."
   - With: "Minimums: $50k (allocation models and the FundAdvisor/ETFAdvisor SMA models), $1m (Core Leaders, Value & Income, Equity Opportunities and Fixed Income SMAs)."

### `research/mission-2026-11-14/queue-batch31-filings-feeds.md`
1. **Line 40 (§0, P-INF-07).** Replace "QCDs cannot go to a DAF (IRC 408(d)(8)(B)(ii))" with "QCDs cannot go to a DAF (IRC 408(d)(8)(B)(i), which excludes 'any fund or account described in section 4966(d)(2)')".
2. **Line 152 (§2.3 table, QCD row).** Replace "QCDs cannot go to non-operating PFs (408(d)(8)(B)(ii))" with "QCDs must go to a 170(b)(1)(A) organisation other than a 509(a)(3) supporting organisation or a DAF (408(d)(8)(B)(i)). Non-operating PFs not described in 170(b)(1)(F) do not qualify".
3. **Line 40 (§0, P-INF-07, item 3).**
   - Replace: "**Donor names stop being public.** Every 990-PF Schedule B named its ≥$5k contributors (530 in CY2024); Form 990 Schedule B names are not public [F]."
   - With: "**Donor names stop being public from CY2025 on.** Every 990-PF Schedule B named its ≥$5k contributors (530 in CY2024), and those five filed returns stay public. Form 990 Schedule B names are not public [F]."
4. **Line 41 (§0, P-B30A-01).** Replace "The post is undated, c.2023 [F; date I]." with "The post is dated 2023-04-17 (page metadata) [F]."
5. **Line 174 (§3 table, eMoney row).** Replace "| Undated; c.2023 (cites Q1 2023 and a TD Ameritrade conversion \"in September of 2023\") [I] |" with "| 2023-04-17 (page metadata `datePublished`) [F] |". In the S14 register row (line 235), replace "c.2023" with "2023-04-17". In `sponsor-data-feeds-2026.csv`, SDF-05 `evidence_date` should be "2023-04-17".

### `research/mission-2026-11-14/queue-batch31-ren-npact-gl.md`
1. **Line 103 (§3, later W-9 row).** Replace "uploaded 2025-07-23 (scanned; read by OCR)" with "PDF created 2025-07-08, uploaded 2025-07-23 (scanned; read by OCR)".
2. **Line 103 (Reading cell).** Replace "| The move happened between 2024-02 and 2025-07, before the January 2026 privacy policy |" with "| The move happened between 2024-02-29 and 2025-07-08 (PDF creation date), before the January 2026 privacy policy |".
3. **Line 131 (§4, San Diego row).** Append: "Wave 16 could not re-read the posting (Workable 429). The medium grade rests on the [R] capture alone [V wave 16]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.10:** "### 11.11 Batch 31 (validated, wave 16)", containing:

   > **Batch 31 (validated, wave 16).** AEF's line 11f ($26.4m, $29.5m and $36.0m for TY2022–24; 0.40–0.46% of assets; $1,876–$2,254 per account) is exactly the investment expense its audit nets inside investment return. Schedule D Part XII line 4a adds it back. So 11f measures the average fund-borne adviser and manager cost per dollar, not what a fee-charging account pays. If fee-charging accounts pay 1.00%, they would hold about 46% of assets. Adviser brochures add two DAF-specific menus: Davenport's RCF private label charges a 1.00%→0.75% wrap on SMAs and 0.75% on models, with RCF's admin fee on top. NPT also pays an intermediary layer that donors do not see as adviser fees: Hollencrest receives 5–25 bps of assets introduced to NPT. Part IX understates all-in cost at the nationals. GS DAF's visible 28.7 bps is about its admin layer (a 26.4 bps bound), and the 0.62–0.67% GSAM fund expense ratios are off the 990. At MS GIFT the visible advisory-type lines are only about 7.8% of a 1.00% advisory ceiling. Endaoment's FY2025 990 (in IRS zip 05B) reports 1,213 DAFs, $25.03m in and $18.68m out; all $24.33m of Part VIII contributions were crypto. That makes FY2024's round 6,000 the outlier. Every.org filed 990-PF for CY2020–24 because it was in a 507(b)(1)(B) 60-month termination. Letter 4422 (2025-10-23) reclassified it as a 170(b)(1)(A)(vi) public charity as of 2020-01-01. Since 2026-09 it accepts IRA QCDs that can fund a "giving credit" balance, and §408(d)(8)(B)(i) bars QCDs to DAFs, so how those balances are classified now matters. Fidelity Charitable is the only DAF sponsor with a named Addepar feed, which requires a G-Number. Empower offers a separate "Fidelity Charitable" connection. Ren's own front-end code maps "Ren for Charities ACH" to its RDE rail, apart from "Legacy" third-party payments, but Ren still names none of its "25+" programs beyond AEF. NPact's W-9s show the same Fusion Laboratories LLC, taxed as a partnership, moving from Dallas to Wakefield, MA between 2024-02 and 2025-07; no sale is evidenced. Santa Barbara's own posting puts its GL on Blackbaud FE NXT. No Foundation Cloud tenant now shows an NPact-hosted ledger [V wave 16]. Sources: [queue-batch31-fees-costs.md](mission-2026-11-14/queue-batch31-fees-costs.md), [queue-batch31-filings-feeds.md](mission-2026-11-14/queue-batch31-filings-feeds.md), [queue-batch31-ren-npact-gl.md](mission-2026-11-14/queue-batch31-ren-npact-gl.md), [validation-wave16-report.md](mission-2026-11-14/validation-wave16-report.md).

## Data-file notes (not .md; for the owning agent)

- **`adviser-fee-evidence-2026.csv`:**
  - In E01–E03 and E11, change "line 4b" to "line 4a".
  - In E12, the minimums note should match fees-costs correction 5.
- **`sponsor-data-feeds-2026.csv`:** set SDF-05 (eMoney) `evidence_date` to 2023-04-17 and `evidence_label` to F.
- **`queue-proposals-batch31b.csv` / research-priority files:** if the P-B31B-01 text cites "408(d)(8)(B)(ii)", change it to "(B)(i)".
- **`relationship-graph-edges-additions-16.csv`:** EP001, EP002, EP005, EP006 and EP009–EP011 are consistent with the sources I re-read. EP003 (San Diego) stays `inferred`. No changes.
- **`spectrumportal-portal-vs-ledger-v3.csv`:** the figures reproduce. I suggest adding "posting not re-readable in wave 16" to the San Diego `basis`.

## Limits

- **Not re-read (blocked):** BMO's ADV (403), Commonwealth's disclosure (403), the San Diego Workable posting (429) and the career.com Santa Barbara copy (403).
- **Every.org:** Item F absence was checked only in the CY2023 and CY2024 990-PFs, and the CY2020–22 Schedule B counts were not recounted.
- **Endaoment:** the 05A member count (84,172) was not re-checked.
- **Not re-checked:** the U.S. Charitable Gift Trust, the GS Charitable Gift Fund, Fidelity Charitable 990 lines, Pathstone and the Bay Harbor summary; Tulsa, Kalamazoo, Amarillo, NW Minnesota and the Ventura and Greenville rows; and the Louisville and NPT PayPal pages.
- **Statute:** I read it through Cornell LII. QCD and DAF classification is legal analysis, not advice.
