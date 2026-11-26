# Validation wave 40C: b4427-03-b43n23 (ΔR1 retirement; who pays sponsor marketing)

**Date:** 2026-11-19. **Validator:** independent-validation-agent-wave40c. **Register:** [`validation-register-wave40c.csv`](../../data/mission-2026-11-14/validation-register-wave40c.csv) (23 claims).

**Study under test:** [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md), its CSV `proxy-reconciliation-parent-marketing-2026-11-19.csv`, and `scripts/mission_proxy_reconciliation.py`.

## 1. Counts

| Result | Claims |
|---|---|
| confirmed | 17 |
| partially_confirmed | 5 (V40C-06, -09, -10, -20, -21) |
| contradicted | 1 (V40C-22) |
| unverifiable | 0 |

**Proposed corrections (15):** 7 accept, 8 modify, 0 reject. All 15 Finds occur exactly once. None ended with `[V wave 40C]`, and four table-row items dropped the row's closing pipe; both problems are fixed in the final forms below. The study itself gets 9 corrections, and the industry report gets a new §11.53.

## 2. Method

- **Script re-run.** The script writes into the repo, so the repo CSV was backed up first and restored afterwards (md5 `ca63d67d…` before and after). The re-run output is byte-identical to the repo CSV: 569 rows, 0 unverified.
- **Independent recompute.** ΔR1, c1, c3 and the CJP Part V terms were recomputed for all 10 sponsor-years with my own XML parser, which shares no code with the study's script.
- **Part B.** I dumped the full text of Schedule O, R and L, and Part IX lines 11a/11f/11g/12/24 and the functional totals, for all 32 Part B returns.
- **Audits and XML.**
  - robots.txt was checked on every host and allows all paths used.
  - These were re-fetched live with a default client: JCF, RCF, NCF and CJP 2024, all three Fidelity PDFs, Vanguard FY2025, and XML 202543189349301959.
  - After pdftotext, every PDF is byte-identical to the cached text the study used, and the XML is byte-identical to the cache.
- **Not used:** sec.gov, crt.sh, certspotter. No outreach.

## 3. Findings

### 3.1 Part A (ΔR1)

1. **The arithmetic is exact.** ΔR1, c1 and c3 match to the dollar in all 10 sponsor-years.
   - The JCF, Fidelity and RCF identities close exactly.
   - The NCF identity closes to about $2.5k. NCCF net assets on the 990 differ from the audit's consolidating column by $2.7k.
2. **Retiring ΔR1 as a margin proxy is justified (V40C-12).** Two refinements:
   - At NCF the NCCF "Operating" class *is* inside R1. It is not absent, just swamped: −$4.80m against +$105.78m.
   - At JCF the audit's own policy would let a surplus into R1. "Not identifiable" should be read as "not separable using the 990".
3. **JCF overstatement (V40C-06).**
   - Note C (audit p. 15) says surplus above the $2,000,000 UJA grant "may be divided among grants to UJA, increases to JCF's Special Gifts Fund, and a reserve for capital projects". The Special Gifts Fund is the column (b) endowment, which is inside R1.
   - Note G's roll-forward shows no transfers in during FY2023–24. FY2024: 21,302,379 + 4,507,348 − 1,607,311 = 24,202,416.
   - So "never reaches R1" holds as a fact for these years, but not as a structural claim.
   - The reserve fund's +$122,690 in FY2024 is not explained.
4. **CJP Israel Emergency Fund (V40C-10).**
   - Of the $55,997k raised, Note 14 says "CJP distributed $30,810 in grants during FY24" (in thousands). That leaves about $25.19m retained, roughly half of the $49.82m residual, not "most".
   - The §2.2 anchor's "operations +47.10, of which Israel Emergency Fund receipts 56.00" is wrong as written, because the receipts exceed the total they are said to be part of.
5. **RCF (V40C-09).**
   - "0% from any of the four named items" is wrong for c4: +$279,805 (4.3% of ΔR1) and +$149,508 (0.3%).
   - The 0% is the c1–c3 share.

### 3.2 Part B (marketing)

6. **Confirmed verbatim:**
   - Fidelity Schedule O "FUNDRAISING" / "NOT SEPARATELY STATED" (all four returns);
   - the Raymond James Schedule O service list;
   - DAFgiving360's line 12 ($2,651,087 → $6,877,640, all in the fundraising column) and its workforce passage;
   - Vanguard's related-party note: fees $3,916,396 and $4,014,052, in-kind services $788,129 and $1,000,342, and the $6.5m facility with no draws;
   - the GS, MS GIFT and BofA figures.
7. **Fidelity books every Part IX expense to the program column.** The fundraising and M&G totals are $0 in all four years, while Schedule O lists fundraising among FMR's services. The study does not say this.
8. **"No parent pays charity marketing on the record" (V40C-21) is literally true but mis-framed.**
   - No filing says a parent pays marketing on its own account.
   - But Fidelity's Schedule O says that the "SEPARATE COSTS BORNE BY FMR IN PROVIDING SERVICES UNDER THE SA … ARE NOT SEPARATELY STATED". The costs of the services, fundraising included, therefore fall on FMR first and are recovered through an aggregate payment equal to the donor fee. Whether that payment covers FMR's full cost is undisclosed.
   - Vanguard also carries an unspecified in-kind cost.
   - The headline should therefore say no filing *shows* a parent subsidy, not that none exists.
9. **The "only adviser line" claim is contradicted (V40C-22).**
   - Fidelity reports an other expense "OTH CHARITABL INV ADVISOR PRGM" of $8,178,569, $9,982,465, $20,670,116 and $15,615,744 (FY2022–25). That is larger than Morgan Stanley's FA commissions line.
   - DAFgiving360 reports "COMMISSIONS" of $0.47–0.60m.
   - Neither names a payee. The study's keyword list (admin, agency, commission, market, advert, promot, fundrais) misses "ADVISOR".
10. **Schedule R (V40C-20).**
    - Only 6 of the 8 filers file Schedule R; DAFgiving360 and BofA do not.
    - The GS Gift Fund names The Goldman Sachs Group Inc in all four years, as the direct controlling entity of the GS Foundation.
    - No filer lists its parent as a related organization or in a Part V transaction.
11. **Minor points.**
    - Fidelity's FY2022 return (202430459349302913) is an amended return filed 2024-02-14.
    - The GS Gift Fund's Schedule O says its statements are "AVAILABLE THROUGH PUBLICLY ACCESSIBLE STATE FILINGS". This parallels BofA and is not in the study's limits.
    - MS GIFT TY2021 has no FA commissions line; it shows "BANK/PROCESSING FEES" of $7,529,035 instead.

## 4. The 15 proposed corrections

| # | Target | Find (start) | Decision | Reason |
|---|---|---|---|---|
| 1 | resilience | "Fee reliance therefore has to be inferred…" | accept | Supported (V40C-12). Tag added |
| 2 | resilience | "6. **Operating surplus…" | accept | Supported. Tag added |
| 3 | resilience | ΔR1 glossary row | modify | Find re-cut to keep the row's closing pipe. Adds the sponsor's own operating fund, which is inside R1 at NCF |
| 4 | resilience | "Only at JCF is it within about $1.6m…" | accept | Supported (V40C-05). Tag added |
| 5 | resilience | "Its balance-sheet trace is ΔR1." | accept | Supported. Tag added |
| 6 | resilience | "Affiliated-commercial sponsors' staff…" | modify | Adds "not separately stated" and makes clear that any parent subsidy is undisclosed (V40C-21) |
| 7 | sponsor-economics | JCF "Because the UJA grant…" | modify | Adds the Note C policy and the Note G roll-forward (V40C-06). 104%/96% verified |
| 8 | sponsor-economics | "The audits show it mostly measures…" | modify | CJP is endowment returns *and* campaign receipts |
| 9 | sponsor-economics | JCF row of error table | modify | Find re-cut (pipe). "ΔR1 is endowment growth" becomes "mostly endowment growth (104% and 96%)" |
| 10 | sponsor-economics | RCF row "(R1 is negative throughout)…" | modify | Find re-cut (pipe). Substance accepted (V40C-08) |
| 11 | sponsor-economics | NCF row "…and annuity reserves" | modify | Find re-cut (pipe) to a unique longer string. $110.5m verified (V40C-07) |
| 12 | sponsor-economics | "without the decomposition…" | accept | Supported. Tag added |
| 13 | marketing-spend | "or recover it through administrator fees…" | modify | Adds Fidelity's "not separately stated" and its $0 fundraising column; advertising range stated |
| 14 | FINAL-STATUS | "The 990 non-DAF net-asset change…" | accept | Supported. Tag added |
| 15 | industry report | "The 990 balance-sheet proxy does not reproduce…" | accept | Supported. Tag added. Supplemented by new §11.53 |

**Checked by script:** every Find below occurs exactly once in its target file, both in isolation and when all items are applied in the order listed, file by file.

## Exact corrections

### `research/mission-2026-11-14/direction-sponsor-financial-resilience.md`

- **Find:** "Fee reliance therefore has to be inferred from the balance sheet (item 6) or read from audited statements (P-B44N27-02)."
- **Replace with:** "Fee reliance cannot be inferred from the balance sheet: at the five sponsors with audited fee data the fee surplus is not identifiable in ΔR1 (item 6). It has to be read from audited statements (P-B44N27-02; [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md)). [b4427-03] [V wave 40C]"

- **Find:** "6. **Operating surplus: the 990 headline is uninformative. The change in non-DAF net assets is a better balance-sheet signal, but audits show it is not an operating margin [C].** [V wave 38B]"
- **Replace with:** "6. **Operating surplus: the 990 headline is uninformative, and the change in non-DAF net assets (ΔR1) is a balance-sheet movement, not an operating signal. At the five sponsors with audited fee data it follows Schedule D other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis; the fee surplus is identifiable in it at none [C].** [V wave 38B] [b4427-03] [V wave 40C]"

- **Find:** "| **ΔR1** | R1(TY) − R1(TY−1). The sponsor's own balance-sheet surplus, including fees moved from DAF accounts and returns on its own funds"
- **Replace with:** "| **ΔR1** | R1(TY) − R1(TY−1). Change in non-DAF net assets: Schedule D column (b) funds, endowment returns, PP&E, donor-restricted and campaign funds, the sponsor’s own operating fund where it is not reported inside the Schedule D DAF value (as at NCF, not at JCF), and any gap between the Schedule D DAF value and the balance sheet. Not an operating result [b4427-03] [V wave 40C]"

- **Find:** "Only at JCF is it within about $1.6m. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B]"
- **Replace with:** "Only at JCF is it within about $1.6m, and that is coincidence: JCF’s R1 is its board-designated endowment plus its reserve fund, while the operating fund that receives the fee is reported inside the Schedule D DAF value. Treat ΔR1 as a non-DAF balance-sheet movement, not an operating result. [V wave 38B] [b4427-03] [V wave 40C]"

- **Find:** "Its balance-sheet trace is ΔR1."
- **Replace with:** "It has no reliable balance-sheet trace: the fee surplus is not identifiable in ΔR1 at any of the five sponsors with audited fee data. [b4427-03] [V wave 40C]"

- **Find:** "  - Affiliated-commercial sponsors' staff, technology and marketing are paid by the parent under services agreements (compensation direction §5; cost-structure §8)."
- **Replace with:** "  - Affiliated-commercial sponsors buy staff, technology and fundraising from the parent under services agreements (compensation direction §5; cost-structure §8). The filings that speak show the charity paying the parent: Fidelity’s payment to FMR equals its donor fee and covers services that include fundraising, though FMR’s own cost of those services is “not separately stated”; Raymond James’s service agreement covers fundraising; DAFgiving360 reimburses Schwab for its workforce and books its own advertising; and Vanguard Charitable books its own fundraising expense while receiving $0.8–1.0m a year of in-kind professional services from Vanguard. Whether any parent spends more than it recovers, and any brand marketing it bears on its own account, are not disclosed. [b4427-03] [V wave 40C]"

### `research/mission-2026-11-14/b4014-b4427-sponsor-economics.md`

- **Find:** "Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B]"
- **Replace with:** "Because the UJA grant leaves the operating fund, the like-for-like figure is the post-grant surplus, which ΔR1 exceeds by $1.56m and $1.18m [C]. [V wave 38B] The match is coincidental: JCF’s R1 equals its board-designated endowment (Schedule D column (b), the Special Gifts Fund) plus its reserve fund to the dollar, and the operating fund that receives the fee is reported inside the Schedule D DAF value. Endowment growth ($1.87m and $2.90m) is 104% and 96% of ΔR1 [C]. The audit’s Note C allows surplus above the $2.0m UJA grant to go to the Special Gifts Fund or a capital reserve, both inside R1, but the Note G roll-forward shows only investment return less appropriations in FY2023–24 [F]. [b4427-03] [V wave 40C]"

- **Find:** "The audits show it mostly measures other-fund and endowment movements [I]."
- **Replace with:** "The audits show it mostly measures other-fund and endowment movements; the b4427-03 decomposition confirms this at Fidelity and JCF, finds Schedule D reporting-basis gaps at RCF and NCF, and finds endowment returns and Israel Emergency Fund campaign receipts at CJP [C]. [b4427-03] [V wave 40C]"

- **Find:** "| JCF | −$0.4m | −$0.8m | Close: the operating fund is most of R1's movement"
- **Replace with:** "| JCF | −$0.4m | −$0.8m | Close by coincidence: R1 is the board-designated endowment (Schedule D column (b)) plus the reserve fund, and the operating fund sits inside the Schedule D DAF value, so ΔR1 is mostly endowment growth (104% and 96% of ΔR1) [C] [b4427-03] [V wave 40C]"

- **Find:** "(R1 is negative throughout), not by operations"
- **Replace with:** "(R1 is negative throughout), not by operations. R1 = (total assets − Schedule D DAF value) − liabilities; at end-2024 the Schedule D DAF value equals total assets to the dollar, so R1 equals minus liabilities [C] [b4427-03] [V wave 40C]"

- **Find:** "ΔR1 includes NCCF's non-DAF charitable funds and annuity reserves"
- **Replace with:** "ΔR1 includes NCCF's non-DAF charitable funds and annuity reserves. In 2024 NCCF’s audited operating net assets fell $4.8m while ΔR1 rose $105.8m; $110.5m of the rise is funds the audit counts as donor-advised or charitable beyond the Schedule D DAF value [C] [b4427-03] [V wave 40C]"

- **Find:** "without the decomposition in proposal P-B4427-03."
- **Replace with:** "at all: the decomposition in [b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md) finds the audited fee surplus identifiable in ΔR1 at none of the five sponsors. [b4427-03] [V wave 40C]"

### `research/mission-2026-11-14/direction-sponsor-marketing-spend.md`

- **Find:** "or recover it through administrator fees (line 11a; Fidelity $121–180m a year) or fund expense ratios."
- **Replace with:** "or recover it through administrator fees (line 11a; Fidelity $121–180m a year) or fund expense ratios. Filings settle part of this: Fidelity’s and Raymond James’s Schedule O list fundraising among the services bought from the parent under the services agreement, so that marketing is bought inside the administrator fee; but Fidelity’s Schedule O says FMR’s own costs of those services are “not separately stated” and Fidelity books $0 to its Part IX fundraising column, so whether the fee covers the full cost is undisclosed. DAFgiving360’s own advertising is on line 12 ($2.7–6.9m a year, FY2022–25) and its workforce is reimbursed to Schwab; Vanguard Charitable books its own fundraising and receives in-kind professional services from Vanguard; Goldman Sachs, Morgan Stanley and BofA file nothing on who pays ([b4427-03-b43n23-proxy-and-parent-marketing.md](b4427-03-b43n23-proxy-and-parent-marketing.md)). [b4427-03] [V wave 40C]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

- **Find:** "  - The 990 non-DAF net-asset change is not an operating margin."
- **Replace with:** "  - The 990 non-DAF net-asset change is not an operating margin and is retired as one: it tracks other-fund growth, endowment returns, campaign receipts and Schedule D reporting basis, and the fee surplus is identifiable in it at none of the five audited sponsors. [b4427-03] [V wave 40C]"

### `research/mission-2026-11-14/b4427-03-b43n23-proxy-and-parent-marketing.md`

- **Find:** "| RCF | 0% from any of the four named items. It is entirely the gap between Schedule D DAF value, total assets and liabilities"
- **Replace with:** "| RCF | 0% from c1–c3. The audited fee surplus (c4: +$0.28m and +$0.15m) is 4.3% and 0.3% of ΔR1; the rest is the gap between Schedule D DAF value, total assets and liabilities [V wave 40C]"

- **Find:** "and most of the rest is the Israel Emergency Fund campaign ($56.0m of receipts)"
- **Replace with:** "and about half of the rest is the Israel Emergency Fund campaign: $56.0m of receipts, of which $30.8m was granted out in FY2024 (audit Note 14), leaving $25.2m against a $49.8m residual [V wave 40C]"

- **Find:** "Audit non-DAF areas +74.77: operations +47.10, of which Israel Emergency Fund receipts 56.00; endowment and reserves +27.41"
- **Replace with:** "Audit non-DAF areas +74.77: operations +47.10 (Israel Emergency Fund receipts 56.00 less 30.81 granted in FY2024 = 25.19 retained); endowment and reserves +27.41 [V wave 40C]"

- **Find:** "So JCF's fee surplus is reported inside column (a) and never reaches R1."
- **Replace with:** "So JCF’s fee surplus is reported inside column (a) and did not reach R1 in FY2023–24. Note C (audit p. 15) allows surplus above the $2,000,000 UJA grant to go to the Special Gifts Fund (the column (b) endowment) or a capital reserve, but the Note G roll-forward shows only investment return less appropriations ($21,302,379 + $4,507,348 − $1,607,311 = $24,202,416 in FY2024), and the reserve fund rose only $122,690 [F/C]. [V wave 40C]"

- **Find:** "8. **No parent pays charity marketing on the record [F/I].** None of the eight filers states that the parent bears brand or adviser marketing for the charity. Where the filing speaks, the charity pays: through the fee (Fidelity, Raymond James), by reimbursement (Schwab staff), or on its own lines (Schwab and Vanguard advertising and fundraising). Brand-level advertising that the parent runs for its own business is outside every filing read."
- **Replace with:** "8. **No filing shows a parent paying for charity marketing beyond what the charity pays it [F/I].** None of the eight filers states that the parent bears brand or adviser marketing for the charity on its own account. Where the filing speaks, the charity pays the parent or pays directly: through the fee (Fidelity, Raymond James), by reimbursement (Schwab staff), or on its own lines (Schwab and Vanguard advertising and fundraising). Two qualifications. Fidelity’s Schedule O says the “SEPARATE COSTS BORNE BY FMR IN PROVIDING SERVICES UNDER THE SA … ARE NOT SEPARATELY STATED”, and Fidelity books $0 to its Part IX fundraising column, so whether the fee covers FMR’s full cost of fundraising is undisclosed. Vanguard Charitable receives $788,129 and $1,000,342 of in-kind professional services from Vanguard (FY2024–25), of unstated type. Brand-level advertising that the parent runs for its own business is outside every filing read. [V wave 40C]"

- **Find:** "is the only line that may be adviser compensation borne by a charity.** It is $1.9–2.8m a year. The payee is not named, so this is not established (proposal P-B43N23-04)."
- **Replace with:** "may be adviser compensation borne by a charity, but it is not the only adviser-related line.** It is $1.9–2.8m a year (TY2022–24; TY2021 has no such line). The payee is not named, so this is not established (proposal P-B43N23-04). Fidelity Charitable reports an other expense described as “OTH CHARITABL INV ADVISOR PRGM” of $8.18m, $9.98m, $20.67m and $15.62m (FY2022–25, program column), and DAFgiving360 reports “COMMISSIONS” of $0.60m, $0.48m, $0.47m and $0.55m. Neither names a payee, and the keyword screen in §3.1 did not capture the Fidelity line. [V wave 40C]"

- **Find:** "- **Schedule R.** No filer lists its parent firm as a related organization, and none lists a Schedule R Part V transaction with it."
- **Replace with:** "- **Schedule R.** Six of the eight filers file Schedule R (DAFgiving360 and BofA do not). None lists its parent firm as a related organization or in a Part V transaction; the Goldman Sachs Charitable Gift Fund names The Goldman Sachs Group Inc only as the direct controlling entity of The Goldman Sachs Foundation. [V wave 40C]"

- **Find:** "- **Massachusetts Attorney General filings (BofA) were not consulted.** The public-charity search is a form interface, which the rules exclude."
- **Replace with:** "- **Massachusetts Attorney General filings (BofA) were not consulted.** The public-charity search is a form interface, which the rules exclude. The Goldman Sachs Charitable Gift Fund’s Schedule O likewise says its financial statements are “AVAILABLE THROUGH PUBLICLY ACCESSIBLE STATE FILINGS”; those were not consulted either. [V wave 40C]"

- **Find:** "| **Fidelity** (FY6/22–25) | $124.6m, $121.2m, $139.7m, $179.9m, all in the program column."
- **Replace with:** "| **Fidelity** (FY6/22–25) | $124.6m, $121.2m, $139.7m, $179.9m, all in the program column (FY2022 from amended return 202430459349302913; Fidelity books every Part IX expense to the program column, $0 to fundraising) [V wave 40C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "The 990 balance-sheet proxy does not reproduce these margins. [V wave 38B]"
- **Replace with:** "The 990 balance-sheet proxy does not reproduce these margins. [V wave 38B] It is retired as a margin measure: it is Schedule D other-fund growth at Fidelity, endowment growth at JCF, Schedule D reporting basis at RCF and NCF, and campaign and endowment gains at CJP. Parent-firm marketing is only partly visible: Fidelity and Raymond James list fundraising among the services bought under their administrator agreements, DAFgiving360 pays its own advertising and reimburses Schwab for its workforce, Vanguard Charitable books its own fundraising, and Goldman Sachs, Morgan Stanley and BofA file nothing on who pays. [b4427-03] [V wave 40C]"

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.53 Retiring the 990 margin proxy; who pays sponsor marketing (validated, wave 40C)\n\n**Retiring the 990 margin proxy; who pays sponsor marketing** (validated, wave 40C). The change in non-DAF net assets (ΔR1) was tested at the five sponsors with audited fee data. It is not an operating margin and is retired as one. At Fidelity it is Schedule D “other funds” growth to the dollar. At JCF it is the board-designated endowment plus a reserve fund, while the fund that receives the fee sits inside the Schedule D DAF value. At RCF it is the gap between total assets, liabilities and the Schedule D DAF value. At NCF the audited operating fund fell $4.8m in 2024 while ΔR1 rose $105.8m. At CJP it is endowment returns and Israel Emergency Fund receipts. On marketing, Fidelity and Raymond James list fundraising among the services bought from the parent, but FMR’s own costs are “not separately stated” and Fidelity books $0 to fundraising. DAFgiving360 books $2.7–6.9m of advertising and reimburses Schwab staff. Vanguard Charitable books $3.8–4.1m of fundraising and receives $0.8–1.0m of in-kind services from Vanguard. Goldman Sachs, Morgan Stanley and BofA disclose nothing on who pays. [V wave 40C]\n\n---\n\n## Source register"
