# Validation wave 37B: Dechomai and DAFpay Network; Canada and Australia

**Validated 2026-11-19 by independent-validation-agent-wave37b.** Desk validation only: no outreach, no logins, no forms. crt.sh, certspotter and sec.gov were not used. Every live request used UA `research-script/1.0` after a robots.txt check.

**Studies validated:**
- [`b40n14-b38c-dechomai-dafpay.md`](b40n14-b38c-dechomai-dafpay.md), with its CSV and script
- [`b39n3-canada-australia.md`](b39n3-canada-australia.md), with its two CSVs and script

**Register:** [`validation-register-wave37b.csv`](../../data/mission-2026-11-14/validation-register-wave37b.csv), 37 claims: V37B-01 to -20 cover Dechomai and DPN, and V37B-21 to -37 cover Canada and Australia.

## Counts

| Result | Study 1 (Dechomai/DPN) | Study 2 (Canada/Australia) | Total |
|---|---|---|---|
| confirmed | 14 | 12 | 26 |
| partially_confirmed | 4 | 5 | 9 |
| contradicted | 2 | 0 | 2 |
| unverifiable | 0 | 0 | 0 |
| **Total** | 20 | 17 | 37 |

## Findings

### Study 1: Dechomai and DAFpay Network

**Reproducibility (V37B-01, -02): confirmed.**
- The script was re-run into scratch. It needs `--irs-dir` to hold the index files for 2021–2026, so the folder used was `scratchpad/irs`. It produced 1,226 rows from 9 Dechomai, 2 DPN and 34 sponsor filings, with none missing, and the file is **byte-identical** to the repo CSV.
- Pointed at a folder holding only `index_2025/2026`, the script silently writes 551 rows. A guard against this would help.
- DAT TY2023: a full diff of the XML leaves confirms that the amended return differs only in ReturnTs, `AmendedReturnInd` and net UBTI ($43,525,166 → $43,583,514).

**Schedule M (V37B-03, -04, -05): partially confirmed.** The XML was re-parsed independently.
- **Totals.** The 8 selected returns hold **842 gifts worth $3,274,159,669**, not 840 worth $3,272.9m.
  - The script keys works of art as `ArtWorksOfArtGrp`, but DF's 2022 and 2023 returns use `WorksOfArtGrp`.
  - Two gifts are therefore dropped: $998,400 and $300,000.
- **Classification.** DAT 2022 "Cyrptocurrency" (2 gifts, $2,092,368) is misspelled in the filing, so it misses the `crypto` substring rule and lands in Other.
  - Corrected crypto: $156,986,280 (4.79%, 130 gifts).
  - Corrected Other: $11,708,932 (0.36%, 12 gifts).
- **Unaffected:** the private-business, real-estate and public-securities classes match exactly, and so does 2024 crypto at 15.1%.
- **Effect on ratios:** all shifts are at most 0.001 points.

**Routing (V37B-06 to -09): confirmed.**
- An independent Schedule I aggregation (name first, then EIN) reproduces every figure: six groups $1,145,879,806 of $1,923,798,960 external (59.6%), all 24 group-year cells, and the intra-group transfers.
- The DF TY2023 line "SCHWAB CHARITABLE TRUST" ($76,391,938) under AEF's EIN 34-1747398 is the **only** EIN/name conflict.
  - Interpretation challenge: "Schwab Charitable Trust" is not the name used on Schwab's other lines ("Schwab Charitable Fund", "DAFgiving360", EIN 31-1640316), so either field could be the error.
  - The 2023 split is DAFgiving360 $76.4m and AEF $86.2m by name, or DAFgiving360 $0 and AEF $162.6m by EIN. The study flags this correctly.

**Reverse grants (V37B-10, -11): confirmed.** A scan of all 34 sponsor XMLs gives $137,961,324 (12.0% of the outbound flow):
- Fidelity's $56,727,821 is non-cash "SECURITIES".
- The superseded Fidelity FY6/22 original swaps name and EIN exactly as described.

**Fee measures (V37B-12, -13): the values are confirmed, but the headline is contradicted.**
- **Values:**
  - Charitable Solutions: $12,613,388 (0.39%).
  - Part IX management plus other fees: $19,920,332 (0.61%).
  - All non-grant expenses: $48,984,620 (**1.50%**).
- **Why the headline fails:** "Below the published 1–3% on every expense measure" is false for the study's own third measure. At 1.50% it sits *inside* the band, and in 2022 (2.04%) and 2024 (1.83%) it is above the FAQ's 1.2–1.4% average.
- **What the measures can show:** they are outflows, not the fee charged, and the study itself gives two reasons the fee take cannot be read from them.
  - The FAQ (Q8, verbatim in the cached page) says "at least 50% off all collected fees are used for operating reserves or unrestricted fund purposes". Retained fees never reach Part IX.
  - DAT's $344.5m Schedule R "reimbursement" (10.5%) is excluded as unreconciled.
- **Defensible statement:** fee and administrative *outflows* are below the band, all non-grant costs fall inside it, and the fee take is not measured.

**Schedule R (V37B-14): confirmed.**
- DAT's type-P transactions sum to $344,453,563.
- DF's type-Q receipts from DAT are $54,193, $58,886, $4,650 and $32,371.
- DAT's total expenses net of grants are only $4.5m–$14.0m a year, so the amount is not in Part IX. It remains unexplained.

**Form 8282 (V37B-15): partially confirmed.**
- `Form8282PropertyDisposedOfInd` is 0 on all 8 returns, no other "8282" string appears, and 420 Forms 8283 were received.
- The study argues that line 7c cannot see Dechomai's assets. That is too strong: Schedule M records tangible personal property received.
  - Works of art: $998,400 (DF 2022) and $300,000 (DF 2023).
  - Collectibles: $19 (DAT 2022).
  - Gold: $336,200 (DF 2024).
- For those gifts the "No" answers are a checkable assertion.

**DPN (V37B-16 to -20).**
- **TY2025 (IRS TEOS zip `2026_TEOS_XML_05B`): confirmed.**
  - "Fees for services – other" is $88,736 against contributions of $2,941,073 (3.017%). For comparison, 2.9% of contributions is $85,291.
  - Program-service revenue and other revenue are both 0. "Chariot" does not appear, and no contractors are listed.
  - Part IV line 6 is false; line 21 is false despite 104 Schedule I lines totalling $1,324,158 (TY2024 line 21 = 1). No Schedule D is filed.
- **Audit status: new finding.** `FSAuditedInd`, `IndependentAuditFinclStmtInd` and `AccountantCompileOrReviewInd` are false or 0 in both years. Batch 38's "DPN, the only audited slice" is therefore wrong.
- **Interpretation challenge:** the 2.9% fit rests on one year of arithmetic inside a ±0.5-point window, and the payee is unnamed.
- **Repo passages that say the fee is netted before receipt: superseded for TY2025.** The corrections are listed below.

### Study 2: Canada and Australia

**Reproducibility and totals (V37B-21, -22): confirmed.**
- The re-run gives a byte-identical CSV and summary JSON.
- An independent parse of the raw CRA files reproduces every release total.

**Blumberg & Pasha (V37B-23, -24).**
- **Report figures: confirmed.** All of them appear verbatim in the PDF text.
- **Verbatim match: confirmed.** 744 of 755 rows match (C$16,643,795,632); the 11 unmatched rows total C$26,180,849.
- **"Returns added after the report": partially confirmed.** This is labelled [C] but is an inference.
  - Nine of the 11 names are absent from the report; the other two have generic name prefixes and are inconclusive.
  - Ten of the 11 have an FPE of 2024-12-31.
  - That is plausible for late filers, but it is not proven.

**Error flags (V37B-25, -26): confirmed.**
- The 7 listed rows sum to 125,986, and both the 60,419 clean accounts (2024) and the 28,181 accounts in flagged rows (2025) are reproduced.
- A broader rule of my own gives 60,405 and 70,746. The difference shows the flags are rule-dependent, as the study says.

**Concentration and aggregate payout (V37B-27, -28): confirmed.**
- Top-N shares and HHI (590 and 680) match exactly.
- Same-year payout is 11.56% and 11.21%; 5864 ÷ 5863 is 58.6% and 54.9%; prior-year payout is 16.4% and 13.3%. The 2025 n is 585, not 586, when prior-year assets must be positive.

**Medians (V37B-29): partially confirmed.** The medians are computed only over sponsors with a non-blank line 5864.
- The study drops 155 sponsors in 2024 (C$116.6m of DAF assets) and 241 in 2025 (C$213.6m) that have positive DAF assets but a blank line 5864.
- Counting blanks as zero:

| Measure | 2024 | 2025 |
|---|---|---|
| Median payout, all sponsors | 5.4% | 4.0% |
| Median payout, sponsors ≥ C$10m | 7.0% | 7.2% |
| Share of sponsors paying ≥ 5% | 50.5% | 45.6% |

- The study does not disclose this exclusion.

**WellFunded (V37B-30, -31).**
- **Page figures and methodology: confirmed.** The page was fetched live; robots.txt allows `/` and disallows only `/api/`.
  - Every headline number and the methodology text appear verbatim.
  - The top-5 bars match the 2025 CRA release exactly.
- **Bracketing: partially confirmed.**
  - The two replicas bracket assets, grants out, top-10 share and sponsor count.
  - They do **not** bracket donations in: C$3.62B is below both C$3.68bn and C$3.90bn.
  - Nor do they bracket the 82,611 accounts, which are above both clean replicas.

**Continuity (V37B-32): confirmed.** The splits 618, 56, 167, 5 and 246 all reproduce, as do the 2025 shares by designation.

**Australia (V37B-33 to -36).**
- **Act No. 86 of 2026 (C2026A00086): confirmed.** Royal Assent was given on 2026-09-15 and the Act was registered on 2026-09-17. Schedule 7 commenced on 2026-10-01, and items 17–18 appear verbatim.
- **Register queried live on 2026-11-19: confirmed.**
  - F2022L00184 is at compilation 0, the latest version.
  - F2019L01227's latest compilation is compilation 2 (F2022C00244), from 2022-02-25.
  - No title contains "Giving Fund", in any letter case.
  - No ancillary-fund title is dated after 2022, and no "Taxation Administration" title is dated 2026.
  - **No 6% instrument is registered.**
- **Sub-funds: confirmed.** The s15(1), s24(1) Note 2 and s27 readings and the ACF quote are all verbatim.
- **Philanthropy Australia statistics: partially confirmed.** "A$4.23bn opening net assets" is not on the page, which says "11.51 per cent of net assets". The A$4.23bn is a back-calculation.

**Repo passages (V37B-37).**
- No passage states the 6% rate as in force.
- Three passages can be read as if it were the floor or as current status, and the Canadian rows cite only Blumberg's 2024 totals. Both are corrected below.
- The main report's line on Canada and Australia ("C$16.6bn in DAFs at 834 charities … 6% decided on 2026-02-26") is accurate as far as it goes. It is updated through §11.43 rather than edited in place.

## Exact corrections

### `research/mission-2026-11-14/b40n14-b38c-dechomai-dafpay.md`

- **Find:** "2. **Asset mix, 2021–24** [C]. Across both entities' Schedule M there were **840 non-cash contributions worth $3,272.9m**, an average of $3.9m each."
- **Replace with:** "2. **Asset mix, 2021–24** [C]. Across both entities' Schedule M there were **842 non-cash contributions worth $3,274.2m**, an average of $3.9m each. The script reads 840 and $3,272.9m because it keys works of art as `ArtWorksOfArtGrp`, while DF's 2022 and 2023 returns use `WorksOfArtGrp` ($998,400 and $300,000, one gift each). In the table below, DAT 2022 “Cyrptocurrency” ($2,092,368, 2 gifts) is also misfiled under Other. Corrected: cryptocurrency $157.0m (4.8%, 130 gifts); Other $11.7m (0.4%, 12 gifts, including the two art gifts). Ratios move by at most 0.001 points [V wave 37B]"

- **Find:** "5. **Effective take is below the published 1–3% on every expense measure** [C]. As a share of Schedule M intake for 2021–24:"
- **Replace with:** "5. **Fee and administrative outflows are below the published 1–3%, but all non-grant expenses (1.50%) fall inside it** [C]. These are expense outflows, not the fee Dechomai charges. The FAQ says at least half of collected fees go to reserves or unrestricted funds, so they never reach Part IX. DAT's unreconciled $344.5m Schedule R “reimbursement” (10.5% of intake) is also excluded. The fee take itself is therefore not measured. As a share of Schedule M intake for 2021–24: [V wave 37B]"

- **Find:** "- These figures sit at or below the bottom of the published 1–3% band, and below the FAQ's 1.2–1.4% average."
- **Replace with:** "- The Charitable Solutions and Part IX fee measures (0.39–0.62%) sit below the published 1–3% band and below the FAQ's 1.2–1.4% average. All non-grant expenses (1.50%; 2.04% in 2022 and 1.83% in 2024) sit inside the band and above that average. None of these is the fee charged, because retained fees do not appear in Part IX [V wave 37B]"

- **Find:** "Form 8282 dispositions of those assets therefore cannot be seen on a 990 at all."
- **Replace with:** "Form 8282 dispositions of those assets therefore cannot be seen on a 990 at all. Line 7c is not empty of scope, though. Schedule M shows tangible personal property received: works of art of $998,400 (DF 2022) and $300,000 (DF 2023), collectibles of $19 (DAT 2022) and gold of $336,200 (DF 2024). For those gifts the “No” answers are a checkable assertion [V wave 37B]"

- **Find:** "That is consistent with the DAFpay fee being booked as an unnamed DPN expense [I]."
- **Replace with:** "That is consistent with the DAFpay fee being booked as an unnamed DPN expense [I]. The match rests on one year of arithmetic within a ±0.5-point window, and the payee is not named. DPN's statements are cash-basis and neither audited nor reviewed (`FSAuditedInd` and `AccountantCompileOrReviewInd` false in TY2025; 0 in TY2024) [V wave 37B]"

### `research/mission-2026-11-14/queue-batch38-closeout-checks.md`

- **Find:** "DPN, the only audited slice, books no fee revenue"
- **Replace with:** "DPN, the only slice with a public 990, books no fee revenue. Its 990 is not audited: `FSAuditedInd` is false or 0 in TY2024 and TY2025. Its TY2025 return books $88,736 of “fees for services – other” (3.02% of $2,941,073 contributions), an unnamed expense consistent with the 2.9% fee [V wave 37B]"

- **Find:** "  - It books no program-service revenue and only $18k of other fees. The 2.9% on DPN-routed gifts is therefore taken before DPN records the contribution, or outside DPN."
- **Replace with:** "  - In TY2024 it books no program-service revenue and only $18k of other fees (1.53% of contributions). The TY2025 return revises this. Its XML is public in IRS TEOS `2026_TEOS_XML_05B` and was read in wave 37B. DPN records contributions gross ($2,941,073) and books $88,736 of “fees for services – other” (3.02%). The 2.9% on DPN-routed gifts therefore appears as an unnamed DPN expense, not netted before receipt. TY2024's 1.53% remains unexplained [V wave 37B]"

- **Find:** "| Fees for services (other) | — | $18,345 | n/a"
- **Replace with:** "| Fees for services (other) | — | $18,345 | $88,736 (TY2025 XML, IRS TEOS `2026_TEOS_XML_05B`) [V wave 37B]"

- **Find:** "990, filed 2026-05-19 (summary only; XML not yet in the S3 mirror)"
- **Replace with:** "990, ReturnTs 2026-05-18T19:51:48-06:00 (XML public in IRS TEOS `2026_TEOS_XML_05B`; not in the S3 mirror at 2026-11-19) [V wave 37B]"

### `research/mission-2026-11-14/queue-batch36-anonymity-feeds-fees.md`

- **Find:** "and DAFpay Network-netted fees."
- **Replace with:** "and DAFpay Network-deducted fees. DPN's TY2025 990 books these as an unnamed “fees for services – other” expense of 3.02% of contributions, not netted before receipt [V wave 37B]"

### `research/mission-2026-11-14/b39n3-canada-australia.md`

- **Find:** "Those rows sum to C$16.644bn, and the 11 unmatched rows (C$26.2m) are returns added after the report (10 Feb 2026) [C]."
- **Replace with:** "Those rows sum to C$16.644bn [C]. The 11 unmatched rows (C$26.2m) are probably returns added after the report (10 Feb 2026): 9 of the 11 names do not appear in it, and 10 of the 11 have a 2024-12-31 year-end [I] [V wave 37B]"

- **Find:** "   - Median sponsor: 10.6% (2024) and 12.2% (2025). Among sponsors with at least C$10m of DAF assets, the median is 8.4% (2024) and 7.3% (2025)."
- **Replace with:** "   - Median sponsor: 10.6% (2024) and 12.2% (2025). Among sponsors with at least C$10m of DAF assets, the median is 8.4% (2024) and 7.3% (2025). These medians exclude sponsors with positive DAF assets and a blank line 5864 (155 in 2024, 241 in 2025). Counting blanks as zero, the medians are 5.4% and 4.0%, and 7.0% and 7.2% for sponsors with at least C$10m [V wave 37B]"

- **Find:** "| Share of sponsors with same-year payout ≥ 5% | 63.5% | 66.7% | —"
- **Replace with:** "| Share of sponsors with same-year payout ≥ 5% (blank 5864 excluded; 50.5% and 45.6% with blanks as zero) | 63.5% | 66.7% | — [V wave 37B]"

- **Find:** "- **Bracketing:** the two replicas bracket WellFunded's assets, flows and sponsor count."
- **Replace with:** "- **Bracketing:** the two replicas bracket WellFunded's assets, grants out, top-10 share and sponsor count. They do not bracket its donations in: C$3.62bn is below both C$3.68bn and C$3.90bn. Nor do they bracket its 82,611 accounts, which are above both clean replicas (69,324 and 72,900) [V wave 37B]"

- **Find:** "fall between our two replicas** [C]:"
- **Replace with:** "fall between our two replicas on assets, grants out and sponsor count; donations in (C$3.62bn) fall below both replicas** [C] [V wave 37B]"

- **Find:** "distributions of A$487m (11.51% of A$4.23bn opening net assets)"
- **Replace with:** "distributions of A$487m (11.51% “of net assets” per Philanthropy Australia; the implied opening base of about A$4.23bn is our back-calculation [C], not a published figure) [V wave 37B]"

### `research/mission-2026-11-14/direction-international-comparison.md`

- **Find:** "On 2026-02-26 the government decided to move both to **6%**, with 3-year smoothing [F: S25]."
- **Replace with:** "On 2026-02-26 the government decided to move both to **6%**, with 3-year smoothing [F: S25]. As at 2026-11-19 no amending guideline instrument is registered. F2022L00184 (4%) and F2019L01227 (5%, compilation 2) remain the operative texts, continued as giving-fund guidelines by Act No. 86 of 2026, Sch 7, items 17–18, from 2026-10-01. The 6% rate is decided, not drafted [V wave 37B]"

- **Find:** "| Canada | C$16.64bn (2024) | C$1.92bn | 12% of same-year DAF assets | 834 charities reporting DAFs on T3010 [F: S13]"
- **Replace with:** "| Canada | C$16.64bn (2024; CRA open data C$16.67bn at 846 charities); C$18.60bn in the incomplete 2025 CRA release | C$1.92bn (2024); C$2.09bn (2025) | 12% of same-year DAF assets (11.2% in 2025; 13.3% on prior-year assets) | 834 charities reporting DAFs on T3010 [F: S13]; 864 in the 2025 release [C: b39n3] [V wave 37B]"

- **Find:** "| Average account | $89,724 |"
- **Replace with:** "| Average account | $89,724 | Inflated denominator: the CRA 2024 release has 186,421 accounts as filed but 60,419 once 14 impossible returns are removed, giving an average of C$275,905 [C: b39n3] [V wave 37B]"

- **Find:** "We did not find the amended instrument (P-B39N3-02)."
- **Replace with:** "We did not find the amended instrument (P-B39N3-02). This was confirmed on the Federal Register of Legislation on 2026-11-19: no title contains “Giving Fund”, and neither guideline has a compilation after 2022. Only the rename has commenced (C2026A00086, Sch 7, 2026-10-01) [V wave 37B]"

- **Find:** "Canada 5% above $1m, and Australia moving to 6% with smoothing."
- **Replace with:** "Canada 5% above $1m, and Australia 4%/5% today, with 6% and smoothing decided but not yet in any registered instrument at 2026-11-19 [V wave 37B]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "Canada (5% above C$1m) and Australia (6% decided on 2026-02-26) set sponsor-level floors"
- **Replace with:** "Canada (5% above C$1m) and Australia (4%/5% in force; 6% decided on 2026-02-26, with no amending instrument registered at 2026-11-19) set sponsor-level floors [V wave 37B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

Wave 37A may insert §11.42 at the same anchor first. Apply this item after it. The anchor stays unique.

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.43 Dechomai, DAFpay Network, Canada and Australia (validated, wave 37B)\n\n**Dechomai, DAFpay Network, Canada and Australia** (validated, wave 37B). Dechomai's two entities sent $1,145.9m of their 2021–24 Schedule I grants (59.6% of $1,923.8m external) to the six national sponsor groups. That total credits DAFgiving360 with a $76.4m line filed under AEF's EIN. The sponsors granted $138.0m back. Schedule M intake was $3,274.2m in 842 gifts; the study's $3,272.9m drops two art gifts. Fee and administrative outflows were 0.39–0.62% of intake, below the published 1–3%. All non-grant expenses (1.50%) fall inside that band, and the fee charged is not measured: retained fees never reach Part IX, and DAT's $344.5m Schedule R “reimbursement” is unreconciled. DAFpay Network's unaudited TY2025 990 books $88,736 of other fees, 3.02% of $2,941,073 of contributions. The DAFpay fee now appears as an unnamed expense, not netted before receipt. Canadian CRA open data reproduce Blumberg–Pasha's C$16.64bn for 2024. The incomplete 2025 release shows C$18.60bn at 864 sponsors, a 68.1% top-10 share and 11.2% same-year payout. Australia's 6% minimum is decided but not registered at 2026-11-19; only the giving-fund rename has commenced (2026-10-01). [V wave 37B]\n\n---\n\n## Source register"

## Check

`v37b/bin/check_finds.py` (in the scratchpad) parses this section and counts each Find in its target file, with `\n` decoded. All 23 Finds occur exactly once, and no Find or Replace value contains a straight double quote. Every Replace ends with [V wave 37B], except the §11.43 item: that one ends with the restored `## Source register` anchor, as the item format requires.
