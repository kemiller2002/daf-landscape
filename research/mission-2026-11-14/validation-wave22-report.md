# Validation wave 22: batch 37 claims (Ren receipts floor, Chariot Form D, Foundation Source lenders, JMI and Bloomerang, the Goldman DAF stack, N-PORT lenders to Bonterra, line-6 false negatives, DAF-to-DAF disclosure, NPT's Wells Fargo channel, Fidelity CIAP share, FY2024 imputations, payment-redirection controls, DAFpay anonymity, Daffy delegates, SCF, adviser curricula) and the strategic-synthesis refresh

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave22.
**Register:** [`validation-register-wave22.csv`](../../data/mission-2026-11-14/validation-register-wave22.csv), rows V22-01 to V22-31.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs, make keyed API calls or contact anyone. I read robots.txt on each host before fetching a page (details under Limits). SEC requests used a generic User-Agent with no personal contact details. I do not reproduce credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-37 documents afterwards. The sources were:
- **Scripts, re-run** in a scratch copy of `scripts/` and `data/mission-2026-11-14/`, so that repo outputs were not overwritten, with the IRS EO BMF and index_2019–2026 files as inputs:
  - `scripts/mission_batch37_filings.py dafrc --fetch`. It rebuilt `dafrc-imputation-resolution-fy2024.csv` **byte-identical** (cmp) to the repo file.
  - `scripts/mission_batch37_filings.py line6 --fetch`, with a fresh work directory (it did not reuse batch 37's cache). It read all 9,566 returns (all parsed ok) and rebuilt `line6-no-daf-holders.csv` **byte-identical** (cmp).
  - The `texts` and `docs` tasks were not re-run; their key figures were checked against the filings and documents directly.
- **Independent arithmetic** from `form990-contractors-harvest-full.csv` (Ren and Goldman rows), `form990-returns-schedule-d-harvest-full.csv`, `vendor-lenders-nport-2026.csv`, `bdc-loans-latest-marks.csv`, `line6-no-daf-holders.csv` and `dafrc-imputation-resolution-fy2024.csv`.
- **IRS XML, re-parsed** with my own regexes (GivingTuesday mirror): RCF CY2024, GS DAPF CY2024, Ayco Charitable Foundation CY2024, Groundswell CY2024 (amended), NPT FY2024, DAFgiving360 FYE 2025-06. IRS `index_2025/2026.csv` (local copies) for GS DAPF, Ayco, MS GIFT and the Goldman Sachs Charitable Gift Fund.
- **SEC:** Chariot Form D and submissions JSON; Audax Private Credit Fund 10-Q (2026-09-30), schedule rows parsed from the HTML; N-PORT XML of Cliffwater Corporate Lending Fund and KKR US Direct Lending Fund-U (2026-06-30); six EDGAR full-text searches (five no-hit names and one positive control).
- **Documents and pages:** Fidelity Charitable audits FY2024/23 and FY2025/24 (`pdftotext`), ACH registration form (PDF, modified 2025-12-18), nonprofit FAQ and security-tips page; Commerce OIG Fraud Alert (July 2026); Chariot help pages (money movement, login and security, ownership transfers, verification, DAFpay Security); Daffy Member Agreement (updated 2025-11-11); SCF 2022 codebook; American College DAF Forum sponsors and sponsorship pages; JMI portfolio page; Bloomerang–Warburg release; Foundation Source CTO release; GTCR–Foundation Source release (PR Newswire); Kirkland release on GTCR Fund XIV; InvestmentNews (2026-01-27); Lilly School release (2025-01-29).

## Headline

Batch 37's filed numbers reproduce, and nearly all its quotes are verbatim. Six results hold independently:
- **Ren's named-receipts floor.** TY2024: $44,977,807 from 18 sponsors. RCF is 42.7% ($19,225,546) and the two Morgan Stanley programs 43.0% ($19,360,708), so three customers make up 85.8%.
- **Chariot's single Form D.** $10,999,978 of equity from 59 investors, first sale 2024-04-19, filed 2024-05-03. EDGAR shows no other filing.
- **Foundation Source's lender.** Audax holds the 1st-lien term loan and DDTL due 2030-09-06 and the revolver due 2029-09-06, all at par. Its LP equity is marked at 1.38x cost, against 1.44x at 2025-12-31. The `par_or_principal` values in `bdc-loans-latest-marks.csv` for these rows are unit counts.
- **Bonterra's registered-fund lenders.** They hold $212.2m of funded value at 97.71–98.34% of par: Cliffwater $140.7m, KKR Fund-U $60.7m, Capital Group KKR $10.9m.
- **Fidelity's CIAP share and DAF-to-DAF flows.** The CIAP shares are 42.6%, 44.8% and 46.9%. DAFgiving360's $976,570,217 grant to Fidelity is 3.7% of Fidelity's FY2025 contributions.
- **Groundswell and the imputations.** Groundswell's amended CY2024 return (12,808 DAFs, $10,084,314) still answers line 6 "No". The script re-run reproduces the FY2024 imputation resolution exactly: 48 asset rows ($593.5m) and 45 account rows (9,104 accounts) remain unresolved.

**One claim is contradicted, and it changes a §0 answer.** Fidelity Charitable *does* publish a callback. Its nonprofit FAQ says: "we may call your organization's publicly available phone number to verify banking and/or contact information. During these calls, we will request verification of bank details … submitted as part of your organization's request to enroll or update EFT information." This is discretionary ("may"), not every request, and uses a public number rather than a "previously established method of communication". It is therefore a partial form of the Commerce OIG's B1 control, not the full benchmark. Batch 37C's statements that no sponsor publishes a callback and that Fidelity states none need correcting.

**A second contradiction concerns the lender ranking.** On funded lines, Cliffwater ($140.7m) is not larger than every BDC position in the repo. FS KKR Capital Corp holds $150.4m par and $149.6m fair value of Bonterra debt at 2026-09-30 (`bdc-loans-latest-marks.csv`). Cliffwater is larger only if its roughly $47.8m of likely-unfunded or fee lines are counted ($187.7m).

**Four wording fixes:**
1. **Goldman stack.** "No Stellar line since CY2022" holds for GS DAPF and Ayco only. The separate Goldman Sachs Charitable Gift Fund (EIN 11-3813663) paid Stellar directly in every year from FYE 2022-06 to FYE 2025-06 ($172,604 in the latest year). It is one of batch 37A's own "12 others".
2. **NPT Schedule L.** The FY2024 return discloses **four** further excess-benefit transactions, after one reported in FY2023. The $2,144.17 was repaid by those four, and one of them was a Wells Fargo adviser who is a donor's son.
3. **Fidelity ACH verifiers.** The form also accepts a Fidelity Charitable reference number, and first-time grantees face unspecified "additional verification".
4. **GTCR Fund XIV.** The Kirkland release is dated 2023-05-31 and gives no 23 May closing date.

**§7 proposals.** Batch 37A's three proposals and batch 37C's five are supported, with the qualifications below. They are written out as governing text under Exact corrections.

**Strategic synthesis.** All 14 figures spot-checked in "Wave 14–21 additions (2026-11-15)" match their governing sources (V22-31). That section needs no change. It predates batch 37 and carries no batch-37 figure.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V22-01 | Ren floor $44.98m TY2024, 18 sponsors; RCF 42.7%; MS 43.0% | **Confirmed** | Harvest recomputed: 44,977,807; 19,225,546; 19,360,708. The "12 others" sum to 2,896,577. |
| V22-02 | RCF CY2024 Schedule L / O; 0 employees | **Confirmed** | Verbatim; one contractor over $100k. |
| V22-03 | Chariot Form D $10,999,978 / 59 investors / 2024-04-19 / filed 2024-05-03 | **Confirmed** | Submissions JSON shows only this filing; EDGAR full-text search returns 1 hit. |
| V22-04 | Audax 1L TL / DDTL due 2030-09-06 at par; revolver 2029-09-06 | **Confirmed** | 13,365,065 / 4,208,879 / 343,575; unfunded 2,233,237; 2025-12-31 balances as stated. |
| V22-05 | Audax equity 1.38x vs 1.44x; §7.2 units | **Confirmed** | 2,765,483 / 2,004,694 and 2,880,081 / 2,004,694. Data note on the ecosystem v1/v2 CSVs. |
| V22-06 | GTCR release; Fund XIV $11.5bn closed 2023-05-23 | **Partially confirmed** | Release and fund size confirmed. The Kirkland release is dated 2023-05-31, with no 23 May date. |
| V22-07 | Foundation Source CTO/product hires; 5,600+ PFs, 20,000 DAFs, $55bn+ | **Confirmed** | Verbatim, including "increased focus on AI". |
| V22-08 | JMI lists Bloomerang with no status line | **Confirmed** | Axonify and Blackbaud carry status lines; Benevity has none. |
| V22-09 | Warburg joins JMI on the Bloomerang board (2024-02-08) | **Confirmed** | Verbatim. |
| V22-10 | GS DAPF CY2024 top five, 13 contractors, Part IX, Schedule R | **Confirmed** | All amounts and labels exact. |
| V22-11 | Ayco CF one contractor $1,730,728; no GS DAPF CY2025 990 | **Confirmed** | index_2026 holds Ayco's FY6/2025 990 and no GS DAPF 202512 return. |
| V22-12 | "No Stellar line since CY2022" | **Partially confirmed** | True at GS DAPF and Ayco. The GS Charitable Gift Fund paid Stellar $139k–$173k a year to FYE 2025-06. |
| V22-13 | Registered funds about $212m funded at 97.71–98.34% | **Confirmed** | N-PORT re-parsed: 140,686,551 + 60,681,154 + 10.85m. |
| V22-14 | Cliffwater larger than any BDC position; "two" DDTL lines due 2032-10-08 | **Contradicted** | FS KKR Capital Corp holds $149.6m FV. Cliffwater has three 2032-10-08 lines. |
| V22-15 | No N-PORT hit for Ren, Foundation Source, Benevity, Chariot, Bloomerang … | **Partially confirmed** | 5 of 17 names re-queried, all 0 hits; the positive control returns 46. |
| V22-16 | Groundswell amended CY2024: 12,808 DAFs; line 6 "No" | **Confirmed** | Filed 2026-01-28; DonorAdvisedFundInd 0. |
| V22-17 | Line-6 screen (9,566 returns; 44 hits; 5 likely and 8 possible sponsors; $21.2m) | **Confirmed** | Fresh re-run byte-identical. Status counts 5,665 / 3,799 / 102 exact; likely sponsors' assets 21,197,631. |
| V22-18 | Fidelity CIAP 42.6% / 44.8% / 46.9% | **Confirmed** | Audit Note 3 exact; CIAP +65.6% vs pooled +39.3%. |
| V22-19 | DAFgiving360→Fidelity 3.7%; SVCF→NPT 11.0% / 10.5% | **Confirmed** | 976,570,217 / 26,464,117,648; 1,591.3m / 14.52bn and 15.15bn. |
| V22-20 | NPT Schedule L Wells Fargo; "five" transactions | **Partially confirmed** | Quote verbatim. Four transactions in FY2024, plus one in FY2023. |
| V22-21 | FY2024 imputations: 48 rows $593.5m unresolved, etc. | **Confirmed** | Script re-run byte-identical. |
| V22-22 | DAFgiving360 77% / 5,200; Lilly funded by DAFgiving360 | **Confirmed** | Verbatim. |
| V22-23 | Commerce OIG alert B1–B3 | **Confirmed** | One page, created 2026-07-27; verbatim. |
| V22-24 | Fidelity ACH document checks | **Partially confirmed** | All quoted controls verbatim. The verifier also accepts a reference number or a first-time path. |
| V22-25 | No sponsor publishes a callback; Fidelity states none | **Contradicted** | Fidelity FAQ: "we may call your organization's publicly available phone number to verify banking". |
| V22-26 | Chariot Owner-only bank changes; 2FA for all; identity checks | **Confirmed** | Verbatim. |
| V22-27 | DAFpay Security: nonprofit sees donor-provided data; some disallow anonymity | **Confirmed** | Verbatim. |
| V22-28 | Daffy "not responsible for reviewing the authority of designees …" | **Confirmed** | Verbatim (Agreement updated 2025-11-11). |
| V22-29 | SCF 2022 has no DAF item; X6830 code 10 excludes DAFs | **Confirmed** | Verbatim; only one "donor-advised" string in the codebook. |
| V22-30 | DAF Forum 2027 Premier Partners; tier floors | **Confirmed** | Four logos under "Premier Partners"; $15,000 / $5,000. |
| V22-31 | Synthesis Wave 14–21 numbers match governing sources | **Confirmed** | 14 figures checked; none differ. |

### Rulings on the batches' §7 proposals

- **Batch 37A §7:**
  - **Proposal 1** (`private-equity-daf-ecosystem-map.md` line 28): supported. Audax's GTCR-era loans are verified (V22-04), and the registered-fund Bonterra holders are verified (V22-13). Bonterra's BDC lenders were already found in wave 10. The text below adds FS KKR as the largest funded holder.
  - **Proposal 2** (`bdc-loans-latest-marks.csv`): supported. The rows are unit counts and the cost is $2,004,694 (V22-05). It is a data file, so it is listed under data notes.
  - **Proposal 3** (industry report line 146): supported (V22-01).
- **Batch 37C §7:**
  - **Proposals 1, 3, 4 and 5:** supported, on V22-30, V22-29, V22-27 and V22-28.
  - **Proposal 2** (11 outlines lack payout, fee, portability and inactivity items): not re-verified outline by outline. It is carried as batch 37C's reading, labelled accordingly.

## Exact corrections

### `research/mission-2026-11-14/queue-batch37-vendor-economics-owners.md`
1. **§0, P-VEN-09 row.**
   - **Find:** "but no Stellar line has appeared since CY2022, so it was paid under $824,200 or through another payee."
   - **Replace with:** "but no Stellar line has appeared at GS DAPF or Ayco since CY2022, so there it was paid under $824,200 or through another payee. The separate Goldman Sachs Charitable Gift Fund (EIN 11-3813663) still paid Stellar directly ($172,604, FYE 2025-06) [V wave 22]."
2. **§3 table, Fund vintage row.**
   - **Find:** "GTCR Fund XIV final close $11.5bn on 2023-05-23 ([Kirkland]"
   - **Replace with:** "GTCR Fund XIV closed at its $11.5bn hard cap (Kirkland release dated 2023-05-31, no closing day stated; [V wave 22]) ([Kirkland]"
3. **§5, first Reading bullet.**
   - **Find:** "- **Direct Ren payments dropped below disclosure thresholds from CY2023.** At GS DAPF they were under the $824k fifth-place line; at Ayco under $100k."
   - **Replace with:** "- **Direct Ren payments dropped below disclosure thresholds from CY2023 at GS DAPF and Ayco.** At GS DAPF they were under the $824k fifth-place line; at Ayco under $100k. This does not hold for every Goldman-branded sponsor. The Goldman Sachs Charitable Gift Fund (EIN 11-3813663; grant administration by CAF America) paid Stellar Technology Solutions directly $157,430, $150,924, $139,000 and $172,604 for FYE June 2022–2025. It is one of the \"12 others\" in §1.2 [V wave 22]."
4. **§6.1 table, Cliffwater row.**
   - **Find:** "13 lines: TL, DDTL (two due 2032-10-08), revolver; 2032-03-05"
   - **Replace with:** "13 lines: TL, DDTL (three due 2032-10-08, one of them a 1.0% likely-unfunded line), revolver; 2032-03-05 [V wave 22]"
5. **§6.1 Findings, first bullet.**
   - **Find:** "Cliffwater alone is the single largest identified Bonterra lender, larger than any BDC position in the repo files."
   - **Replace with:** "Cliffwater is the largest registered-fund holder. On funded lines ($140.7m) it is second to a BDC, FS KKR Capital Corp ($150.4m par, $149.6m fair value at 2026-09-30 in `bdc-loans-latest-marks.csv`). It is larger only if its roughly $47.8m of likely-unfunded or fee lines are counted ($187.7m) [V wave 22]."
6. **§7, status line (append after item 3).** "Validation wave 22: proposals 1–3 are supported (V22-01, V22-04, V22-05, V22-13). Proposal 1 is applied in `private-equity-daf-ecosystem-map.md` with FS KKR added as the largest funded Bonterra holder; proposal 3 is applied in the industry report."

### `research/mission-2026-11-14/queue-batch37-filing-questions.md`
1. **§0, P-GPT-03 row.**
   - **Find:** "It discloses five excess-benefit transactions, $2,144.17 repaid with interest"
   - **Replace with:** "It discloses four excess-benefit transactions beyond one reported in FY2023 (five in all). The four were repaid with interest ($2,144.17) [V wave 22]"
2. **§3 table, NPT FY2024 Schedule L row.**
   - **Find:** "five de-minimis excess-benefit payments by Wells Fargo to donor-advisers who were Wells Fargo advisers (2021–24), all repaid ($2,144.17 with interest)"
   - **Replace with:** "four further de-minimis excess-benefit transactions after one found in FY2023: Wells Fargo compensation to three donors who were Wells Fargo advisers and to one Wells Fargo adviser who is a donor's son (2021–24), all repaid ($2,144.17 with interest) [V wave 22]"

### `research/mission-2026-11-14/queue-batch37-controls-education.md`
1. **§0, P-PRC-06 row (lead sentence).**
   - **Find:** "**No sponsor publishes the main control in the federal benchmark: a callback to a known contact before a bank-detail change. Redirection risk is handled by keeping bank details out of the sponsor's hands.**"
   - **Replace with:** "**No sponsor publishes the full federal benchmark control: a mandatory callback to a known contact, by a previously established channel, before every bank-detail change. Fidelity Charitable publishes a discretionary version ("we may call your organization's publicly available phone number to verify banking and/or contact information") for enrolments and updates. Elsewhere, redirection risk is handled by keeping bank details out of the sponsor's hands** [V wave 22]."
2. **§0, Fidelity verifier bullet.**
   - **Find:** "&nbsp;&nbsp;– two prior grant IDs or check numbers from the last 3 years;"
   - **Replace with:** "&nbsp;&nbsp;– supporting information from the last 3 years: two prior grant IDs, two check numbers or a Fidelity Charitable reference number (first-time grantees face unspecified \"additional verification\") [V wave 22];"
3. **§0, Fidelity callback sentence.**
   - **Find:** "&nbsp;&nbsp;No callback is stated, and Stripe enrollees change bank details under Stripe's controls."
   - **Replace with:** "&nbsp;&nbsp;The nonprofit FAQ adds that Fidelity \"may call your organization's publicly available phone number\" to verify bank details submitted to enrol or update EFT. This is discretionary, and the number is public, not a previously established contact. Stripe enrollees change bank details under Stripe's controls [V wave 22]."
4. **§1.2 table, Fidelity Charitable (own ACH) row, B1 and B2 cells.**
   - **Find:** "| **Not stated** | Not stated. Two named contacts receive the Grant Details Report |"
   - **Replace with:** "| **Partial:** \"we may call your organization's publicly available phone number to verify banking and/or contact information\", for enrolments and updates ([FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)); discretionary, and to a public number [V wave 22] | Not stated. Two named contacts receive the Grant Details Report |"
5. **§1.2 table, same row, Other controls cell.**
   - **Find:** "• Two grant IDs or check numbers from the last 3 years"
   - **Replace with:** "• Two grant IDs, two check numbers or a reference number from the last 3 years (first-time grantees: unspecified additional verification) [V wave 22]"
6. **§1.3, reading 1.**
   - **Find:** "These defeat a pure email request but not an attacker who holds stolen grant letters. No callback is published."
   - **Replace with:** "These defeat a pure email request but not an attacker who holds stolen grant letters. Fidelity's FAQ adds a discretionary callback to the charity's publicly available number; whether it is applied to every bank change is not stated [V wave 22]."
7. **§7, status line (append after item 5).** "Validation wave 22: proposals 1, 3, 4 and 5 are verified and applied (V22-27 to V22-30). Proposal 2 is applied as batch 37C's reading; the 11 outlines were not re-read item by item."

### `research/mission-2026-11-14/private-equity-daf-ecosystem-map.md`
1. **Line 28** (batch 37A §7 proposal 1, validated).
   - **Find:** "   - **Not found:** lenders to GTCR-era Foundation Source, Ren, Bonterra and Benevity (P-PE-02)."
   - **Replace with:** "   - **Lenders found** (batch 37A; V wave 22):\n     - **GTCR-era Foundation Source:** Audax Private Credit Fund (1L term loan and DDTL due 2030-09-06, revolver due 2029-09-06, all at par at 2026-09-30; LP equity marked 1.38x cost).\n     - **Bonterra:** BDCs (largest funded holder FS KKR Capital Corp, $149.6m fair value at 2026-09-30) and registered funds (about $212m funded at 2026-06-30: Cliffwater, KKR US Direct Lending Fund-U, Capital Group KKR interval funds).\n   - **Not found:** lenders to Ren and Benevity (P-PE-02)."

### `research/mission-2026-11-14/analyst-and-education-landscape.md`
1. **§5.2, closing paragraph** (batch 37C proposal 1, validated).
   - **Find:** "The DAFCP has no named sponsor partner on its page ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)), but its director's public article reuses the aggregate payout claim."
   - **Replace with:** "The DAFCP has no named sponsor partner on its page ([DAFCP](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp)), but its director's public article reuses the aggregate payout claim. The same college's DAF Forum 2027 lists DAFgiving360, Fidelity Charitable, NPT and Vanguard Charitable as Premier Partners, and one DAFCP instructor is an NPT executive [batch 37C; V wave 22]."
2. **§5.2, T4 row, verdict** (batch 37C proposal 2).
   - **Find:** "| Kitces is **consistent** with the repo. Mainstream curricula have a **gap**: portability is not a visible teaching item. |"
   - **Replace with:** "| Kitces is **consistent** with the repo. Mainstream curricula have a **gap**: portability is not a visible teaching item. Batch 37C found no portability, fee, payout-distribution or inactivity item in 11 public outlines (CFP Board topics and objectives, DAFCP, CAP, two American College CE modules, Fidelity, NPT, NAPFA, CFP CE registry) [batch 37C; not re-read item by item in wave 22]. |"
3. **§4.2, after the "Reconciling these" paragraph** (batch 37C proposal 3, validated).
   - **Find:** "following synthesis §A's denominator-substitution warning."
   - **Replace with:** "following synthesis §A's denominator-substitution warning. No probability sample measures DAF holding. The 2022 SCF codebook excludes DAFs from its trust question (X6830 code 10, merged into X6828 in the public file) [batch 37C; V wave 22]."

### `research/mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md`
1. **§1.1, Reading** (batch 37C proposal 4, validated).
   - **Find:** "- **The anonymous case is undocumented.** It remains the open question (P-B36C-01)."
   - **Replace with:** "- **The anonymous case is undocumented.** It remains the open question (P-B36C-01). The `anonymous` flag is set by the nonprofit's own form in the same callback as the donor's name and email. Chariot's DAFpay Security page says the nonprofit \"can view the information provided by the donor (Name, Email, Address and Gift Size)\" and that \"Some nonprofits elect to disallow anonymous gifts through DAFpay\" [batch 37C; V wave 22]."

### `research/mission-2026-11-14/queue-batch36-agent-terms-controls.md`
1. **§1.2, reading 3** (batch 37C proposal 5, validated; applies on top of the wave-21 replacement of the bold lead).
   - **Find:** "   - Whether such an account can hold its own API key is not documented. See P-B36B-01."
   - **Replace with:** "   - Whether such an account can hold its own API key is not documented. See P-B36B-01.\n   - The Agreement also says \"Daffy is not responsible for reviewing the authority of designees for any corporation or trust\" [batch 37C; V wave 22]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **Line 146, Vendor economics** (batch 37A §7 proposal 3, validated).
   - **Find:** "Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL))."
   - **Replace with:** "Ren's corporate revenue, margins and customer concentration are not public ((source: repo inference — no primary URL)). Named Ren receipts in sponsor 990s total $44.98m in TY2024 (18 sponsors). RCF is 42.7% of that and the two Morgan Stanley programs 43.0% (batch 37A §1.2; V wave 22). This is a floor on receipts, not Ren revenue."
2. **New subsection after §11.16:** "### 11.17 Batch 37 (validated, wave 22)", containing:

   > **Batch 37 (validated, wave 22).** Ren's revenue is not public. Its named receipts in sponsor 990s, a floor limited to top-five contractor lines, were $44.98m in TY2024 from 18 sponsors. RCF (42.7%) and the two Morgan Stanley programs (43.0%) account for 85.8%. Chariot has filed one Form D ($10,999,978 from 59 investors, 2024), and nothing public points to a sale. Foundation Source's GTCR-era debt is held by Audax Private Credit Fund at par: a term loan and DDTL due 2030-09-06 and a revolver due 2029-09-06. Audax's small LP stake is marked at 1.38x cost, against 1.44x at end-2025. JMI still lists Bloomerang as a holding without an exit status. Goldman's flagship DAF paid its own affiliates (GS Trust, GS & Co), Oak Hill, Ayco and Sapient as its top five contractors in CY2024. Ren's Stellar unit no longer appears among them, although the separate Goldman Sachs Charitable Gift Fund still pays Stellar directly. Registered funds hold about $212m of funded Bonterra debt at 97.7–98.3% of par; a BDC, FS KKR Capital Corp, is the largest funded holder ($149.6m). No N-PORT holding names Ren, Foundation Source, Benevity, Bloomerang or Chariot. Fidelity Charitable's audited adviser-managed (CIAP) share of investments rose from 42.6% (2023) to 46.9% (2025); no sponsor publishes an adviser-managed account split. No sponsor reports DAF-to-DAF grants separately. DAFgiving360's $977m grant to Fidelity was 3.7% of Fidelity's FY2025 DAF contributions. NPT's 990 discloses a Wells Fargo-managed DAF channel only through excess-benefit corrections. The line-6 "No" false-negative tail adds a few small workplace-giving sponsors but not money: Groundswell's amended return reports 12,808 DAFs and $10.1m while still answering "No". Of DAFRC's FY2024 imputations, 48 asset rows ($593.5m) and 45 account rows remain unresolvable from filings. On payment redirection, the Commerce OIG's July 2026 benchmark asks for a callback, dual approval and sender checks. Fidelity documents verifier checks, a wet signature and a discretionary callback to the charity's public number. Vanguard and NPT avoid holding bank details by paying through PayPal. Chariot (and Daffy through it) restricts bank changes to the account Owner, with mandatory 2FA. On DAFpay the nonprofit sees what the donor provides, whatever the anonymity flag. Daffy disclaims reviewing the authority of corporate or trust designees. No probability survey measures DAF ownership: the 2022 SCF expressly excludes DAFs. The four largest national sponsors are the Premier Partners of the American College's DAF Forum 2027, and the adviser curricula outlines read contain no payout, fee or portability items [V wave 22]. Sources: [queue-batch37-vendor-economics-owners.md](mission-2026-11-14/queue-batch37-vendor-economics-owners.md), [queue-batch37-filing-questions.md](mission-2026-11-14/queue-batch37-filing-questions.md), [queue-batch37-controls-education.md](mission-2026-11-14/queue-batch37-controls-education.md), [validation-wave22-report.md](mission-2026-11-14/validation-wave22-report.md).

## Data-file notes (not .md; for the owning agent)

- **`payment-redirection-controls-2026.csv`:**
  - **Add PR26** (Fidelity Charitable, `bank_change_verification`, control_stated P, benchmark_control "out_of_band_verification (discretionary; public number)"). key_quote: "we may call your organization's publicly available phone number to verify banking and/or contact information". source_url: https://www.fidelitycharitable.org/nonprofits/faqs.html. The old `nonprofits-frequently-asked-questions.html` URL 301-redirects there.
  - **PR02 notes:** add the reference-number and first-time-grantee options.
- **`bdc-loans-latest-marks.csv`:** Foundation Source Class A/B equity rows, as batch 37A §7.2 says. `par_or_principal` holds unit counts, so set units_hint to `units` and blank `fv_pct_of_par`.
- **`bdc-loans-daf-ecosystem-v1.csv` / `-v2.csv`:** the Foundation Source equity rows with fair value 2,880 / 2,877,201 (table rows 1583–1584 of the 2026-11-12 10-Q) are the **2025-12-31 comparative**, not 2026-09-30, yet are tagged `latest`. Re-tag them as comparative.
- **`vendor-lenders-nport-2026.csv`:** no value change. The Cliffwater 1.0% DDTL line (40.2m balance, 39.5m value) has a near-par value despite the "unfunded" flag; keep the flag but note the ambiguity.
- **`relationship-graph-edges-additions-21.csv`:**
  - **EU013:** GS & Co's payee label is "TECH & INV ADV FEES", so `technology_provider` is a partial reading; add investment advisory to the notes.
  - **Possible addition:** an edge Stellar Technology Solutions → The Goldman Sachs Charitable Gift Fund (`technology_provider`, FYE 2022–2025).
- **`dafrc-imputation-resolution-fy2024.csv`:** no change (rebuilt byte-identical).

## Limits

- **Robots and access.**
  - robots.txt was read first on every host:
    - the GivingTuesday S3 mirror (404, no file), www.sec.gov (Archives allowed), data.sec.gov (NoSuchKey, no file) and efts.sec.gov (no robots file; JSON "Forbidden" on /robots.txt; search used as in earlier waves);
    - www.jmi.com, foundationsource.com, kirkland.com, www.prnewswire.com and bloomerang.com;
    - www.fidelitycharitable.org, www.oig.doc.gov (404) and www.federalreserve.gov (404);
    - help.givechariot.com and docs.givechariot.com, www.daffy.org;
    - events.theamericancollege.edu and partnership.theamericancollege.edu (sitemap only);
    - philanthropy.indianapolis.iu.edu and www.investmentnews.com (Claude-User allowed).
  - **Not fetched:** dafgiving360.org (blocked in batch 37) and paypal.com (403 in batch 37). Help-centre pages at help.givechariot.com carry embedded agent instructions; they were ignored, and the `?ask=` endpoint was not used.
- **Not re-run or not re-read:**
  - the `texts` and `docs` script tasks;
  - FFTC and FCJC audit figures and the Endaoment and MS GIFT line-3 rows (batch 37B §5);
  - Fidelity → Vanguard 8.3%;
  - NPT FY2025 consolidated statements;
  - 12 of the 17 N-PORT no-hit names and the 57 HTML-only hits;
  - the BlackRock CyberGrants rows and the Community Brands and Orion context;
  - Inside INdiana Business, Pulse 2.0 and the job-board figures ([X]);
  - Vanguard, NPT, PayPal and Daffy help pages (PR10–PR15, PR20–PR22);
  - the Chariot integration guide and Grant Request pages;
  - the 11 curricula outlines item by item;
  - the NBER PPS acknowledgement.
- **Interpretation.** These remain inferences, as batch 37 labels them:
  - Fund XIV as GTCR's vehicle;
  - "build phase" at Foundation Source;
  - the Goldman routes (a)/(b);
  - acquisition-capacity use from DDTL draws;
  - the line-6 manual verdicts;
  - the Endaoment crypto reading;
  - sponsor influence on curricula (n = 11).

This is research, not legal advice.
