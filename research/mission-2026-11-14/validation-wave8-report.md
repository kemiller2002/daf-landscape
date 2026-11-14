# Validation wave 8: lenders, labour rates, DAFpay fees, agentic evidence, donor export, CF rails, DonorSphere

Validator: independent-validation-agent-wave8. Date: 2026-11-14.
Register: [`data/mission-2026-11-14/validation-register-wave8.csv`](../../data/mission-2026-11-14/validation-register-wave8.csv) (14 rows covering V8-01 to V8-10).

**Method.** I reached each verdict from primary sources first: SEC EDGAR filings (the full-text search API, then the schedule-of-investments tables in each filing), IRS e-file XML, and the sponsors' and vendors' own pages and PDFs. Only after that did I read the three queue documents and compare. For the labour-rate figures I re-ran `scripts/mission_labour_rate_check.py`, writing its output to the scratchpad so that the repo CSV was not overwritten, and recomputed three sponsors by hand from raw XML. I did no outreach, logins or form submissions.

## Verdicts

| Claim | Result | Confidence | One-line reason |
|---|---|---|---|
| V8-01 Audax / Foundation Source | **Confirmed** | high | The Q3-2026 10-Q (filed 2026-11-12) shows the term loan at $13.37m, the delayed-draw term loan (DDTL) at $4.21m and the revolver at $0.34m, all S+5.00% and marked at par. The term loan and DDTL mature 9/6/2030 and the revolver 9/6/2029. LP interests are at 1.38x cost (1.44x at 12/31/2025). Audax **is** a current lender, so wave-7 correction 5 was wrong. |
| V8-02 Bonterra 9/8/2027 loan: lenders, spread, 2022–23 marks | Partially confirmed | high | The lenders are right. The spread was L+6.50% only in 2021 and L+6.25% throughout 2022. Term-loan marks were 96.7–99.0%. The ~91.5% marks are on revolvers only. |
| V8-02 PIK amendment | Confirmed | high | An 8.00% PIK tranche was added in 2023 (dated 9/28/2023 at Monroe) and repriced to 7.75% PIK by 2024, maturing 9/27/2027. |
| V8-02 "~98.5–99% by late 2025" | **Refuted** | high | Those marks are **prior-year (2024) comparatives**. Golub, BlackRock (TCP and Direct Lending) and Monroe show no position in the 2027 loan at their 2025 period-ends. The loan was refinanced in 2025 into the S+5.00% facility maturing 3/5/2032. |
| V8-03 Bloomerang | Partially confirmed | high | SF+6.00% was the December 2023 pricing. By 12/2025 it was SF+6.50% with 3.50% PIK, and in 2026 it was repriced to SF+5.50% with 6.57% cash / 3.00% PIK. Golub marks it 99.0%; Monroe marks it **100.5%**. |
| V8-04 FS KKR Momentive 96.1% | Confirmed | high | FS KKR lists "Community Brands Inc" (Momentive Software) at SF+5.3%, maturing 07/2031: $50.8m par, $48.8m fair value (FV) = 96.1%. |
| V8-05 Labour rates | Confirmed | high | Reproduced exactly: 898 sponsors, median $38.87/h, $57.35 / $73.28 / $60.05 by band. DAFgiving360 is $86.35/h (FYE 6/2025) and $84.60/h (FYE 6/2024). The raw-XML recomputations for DAFgiving360, Vanguard Charitable and Tulsa CF match. |
| V8-06 DAFpay 2.9% rounding, Bloomerang 4.85%, Donorbox 4.5% | Confirmed | high | Chariot's Nonprofit Terms (2026-10-14) say "2.9% (rounded to the nearest whole dollar)". Bloomerang charges 2.9% + 1.95%; Donorbox charges 1.6% + 2.9%. |
| V8-06 DAF Direct / PayPal Giving Fund $0, Every.org For Good 1.5% | Partially confirmed | medium | The $0 figures are confirmed from the vendors' own pages. Every.org's 1.5% comes from a search-index read only (the live page returned HTTP 429), and Every.org currently absorbs that fee for bank-account gifts. |
| V8-07 Agentic products, Benevity | Confirmed | medium | No independent outcome evidence was found. Benevity's 30%→<3% applies to **one unnamed early-adopter partner**, not to the programme as a whole. |
| V8-08 Top-10 donor export | Partially confirmed | medium | Nothing is in public documentation. That is not proof that no export capability exists; logged-in views were not checked. |
| V8-08 SVCF clause | Partially confirmed | high | The clause is **purpose-limited**: it bars collecting portal information "for any purposes unrelated to" the advisor's grantmaking. It is not a blanket ban on automated collection. The binding limit is the clause on third-party portal access, which carries an indemnity. |
| V8-09 DonorSphere / FidTech | Confirmed | high | FidTech's site, `pgh.donorsphere.org` on jewishpgh.org, and the GHCF and HCF pages all confirm it. The six 990 payees are confirmed, including the Pittsburgh XML entry ($525,587, 1 Landmark Square, Stamford). |
| V8-10 Check-paying CFs | Confirmed | high | All five confirmed. SVCF says "generally" and GKCCF "in most cases", and Tulsa says grants are "mailed" (a check is implied). |

## Key finding: the Bonterra 2025 marks are prior-year comparatives

- **Golub Capital BDC FY2025 10-K (filed 2025-11-18).** The Bonterra rows ($92,893k par, $91,501k FV, SF+7.00%; plus 7.75% PIK, $3,836k) sit under the heading *"Consolidated Schedule of Investments – (continued) September 30, 2024"*. The XBRL contexts are 2024-09-30 only, and there is no Bonterra row in the September 30, 2025 schedule.
- **BlackRock TCP and BlackRock Direct Lending FY2025 10-Ks (filed 2026-02-27).** The rows appear only in the December 31, 2024 schedule, and the 2025 unfunded-commitment column reads "NA".
- **Monroe Capital FY2025 10-K.** The rows carry only 2024-12-31 contexts, and the revolver's 2025 unfunded amount is "n/a".
- **AB Private Credit Investors 10-Q, Q3 2025.** The new loan is "Bonterra LLC | Software & Tech Services | Term Loan S+5.00%, 0.75% floor, 3/5/2032", with par $9,852,086 and FV $9,778,195 (99.25%), plus a DDTL whose commitment expires 3/5/2027. This is the **same industry label AB used for the 2027 Apax loan**, which weakens the doubt in the queue document that this is a different borrower. FS KKR holds $133.4m par of the 3/5/2032 loan (99.5%).
- **Root cause.** `bdc-loans-daf-ecosystem.csv` assigns every row the filing's own `period_ending`. Rows from the prior-year comparative schedule in each 10-K are therefore labelled with the current year. The same problem probably affects other targets; for example, the BKCC FY2023 10-K repeats its 12/31/2022 rows under a period of 2023-12-31.

## Exact corrections

### `research/mission-2026-11-14/queue-pe-lenders-labour-rates.md`

1. **Line 28.** Replace "was priced at L+6.50% with a 0.75% floor" with: "was priced at L+6.50% with a 0.75% floor at 9/30/2021, and at L+6.25% throughout 2022 (Golub 10-K FY2022; AB 10-K FY2022; BKCC 10-K FY2022)".
2. **Line 35.** After "the revolver at 91.75%", add: "(the revolver is on a commitment basis; term-loan marks across holders were 96.7–99.0% in 2022–23)".
3. **Line 37.** Replace the whole bullet with: "**Exited in 2025.** The SOFR+7.00% / 7.75% PIK marks of 98.5–99.1% are the **2024** comparatives (Golub 9/30/2024; BlackRock and Monroe 12/31/2024) printed in the FY2025 10-Ks. None of Golub, BlackRock TCP, BlackRock Direct Lending or Monroe shows the 9/8/2027 facility at its 2025 period-end (2025 unfunded commitments 'NA'/'n/a'). The facility was refinanced in 2025 into the S+5.00% loan maturing 3/5/2032 (AB PCI 10-Q Q3-2025; FS KKR 10-Q Q3-2026)."
4. **Line 38.** Delete "[I] The facility matures in about 10 months, so a refinancing or extension is imminent."
5. **Line 39.** Replace the heading with: "**The 3/5/2032 'Bonterra LLC' facility is most likely the 2025 refinancing of Apax's Bonterra.**"
6. **Line 42.** Replace "The 2027 Apax facility was also still held by Golub, BlackRock and Monroe at the same dates." with: "AB Private Credit Investors labelled the 3/5/2032 loan 'Software & Tech Services' at 9/30/2025, the same label it used for the 2027 loan. The 2027 holders had all exited by their 2025 period-ends."
7. **Line 50.** After "at SF+6.00%", add: "(origination; repriced to SF+6.50% with 3.50% PIK by 12/2025 and to SF+5.50% with 6.57% cash / 3.00% PIK in 2026)".
8. **Line 52.** Replace "marked 99.0%" with "marked 99.0% at Golub (6/30/2026) and ~100.5% at Monroe Capital Income Plus (9/30/2026)".
9. **Line 58.** After "**96.1%**", add: "(listed as 'Community Brands Inc'; FS KKR $50.8m par / $48.8m FV)".
10. **Line 204.** Replace "Bonterra: the Golub-led one-stop with Monroe, BlackRock and AB (9/8/2027; PIK amendment 2023)" with: "Bonterra: the Golub-led one-stop with Monroe, BlackRock and AB (9/8/2027; PIK amendment 2023; refinanced 2025), then the S+4.75–5.00% 3/5/2032 facility (FS KKR, KKR FS Income Trusts, Crescent, AB, CCS IX, New Mountain)".

### `data/mission-2026-11-14/bdc-loans-daf-ecosystem.csv`

11. Add a `row_period` column taken from the schedule heading or the XBRL context, not from the filing.
12. In the meantime, set `period_ending` to the prior year for these rows:
    - Golub Capital BDC filed 2025-11-18 (table rows 4047–4050): 2024-09-30.
    - Golub Capital Direct Lending filed 2025-12-04 (rows 2478–2481): 2024-09-30.
    - BlackRock TCP filed 2026-02-27 (rows 1164–1167, 1573): 2024-12-31.
    - BlackRock Direct Lending filed 2026-02-27 (rows 868–871, 1112): 2024-12-31.
    - Monroe Capital filed 2026-03-05 (rows 1299–1301): 2024-12-31.
    - Also check every `which_filing=latest` 10-K row for the same comparative-schedule problem.
13. For the 3/5/2032 Bonterra rows, change `identity_note` to "probable: 2025 refinancing of Apax Bonterra (AB 'Software & Tech Services' label; 2027 holders exited 2025)".

### `data/mission-2026-11-14/research-priority-inputs.csv`

14. **P-LND-01.** Change the description to: "Confirm the borrower identity of the 3/5/2032 Bonterra LLC facility (likely the 2025 refinancing of the 9/8/2027 Apax loan) and track its marks at FS KKR, KKR FS Income Trusts, Crescent, AB, CCS IX and New Mountain." Delete "track … 9/8/2027 … in Golub, Monroe and BlackRock BDC filings each quarter", since those lenders have exited.

### `research/mission-2026-11-14/private-equity-daf-ecosystem-map.md`

15. **Line 28 ("Not found: lenders to GTCR-era Foundation Source, Ren, Bonterra and Benevity").** Replace with: "Not found: lenders to Ren and Benevity. Foundation Source: Audax Private Credit Fund, S+5.00%, 9/6/2030, at par (10-Q filed 2026-11-12). Bonterra: Golub/Monroe/BlackRock/AB 9/8/2027 one-stop, refinanced 2025 into a 3/5/2032 S+4.75–5.00% facility (FS KKR lead holder)."
16. **Line 203.** Make the same change, and remove Bonterra and Foundation Source from the "Not found" list.
25. **Wave-7 correction 5.** Apply the queue document's own proposed replacement (§5 item 1). It is verified: Audax Private Credit Fund holds the term loan, DDTL and revolver at S+5.00% (9/6/2030; revolver 9/6/2029) at par, plus Class A and Class B LP interests at 1.38x cost (Q3-2026 10-Q).

### `research/mission-2026-11-14/queue-donor-export-cf-payments-donorsphere.md`

17. **Line 38.** Replace "its DAF agreement bars advisors from collecting portal data 'through automated means or otherwise'" with: "its DAF agreement bars advisors from collecting website or portal information '(through automated means or otherwise) … for any purposes unrelated to' their grantmaking privileges, and puts third-party portal access without SVCF approval at the advisor's risk, with an indemnity".
18. **Line 86.** Replace "Its ban on automated collection is the only top-10 contractual limit" with: "Its purpose-limited bar on automated collection, together with the third-party-access indemnity, is the only top-10 contractual limit".
19. **Line 113 and the P-CFR-01 summary.** Replace "Check for DAF grants (5)" with "Check by default for DAF grants (5; SVCF 'generally', GKCCF 'in most cases', Tulsa 'mailed')".
20. **P-CFR-02, the "990 payees" bullet.** Add: "990 payee is not the same as a DonorSphere user. Baltimore books FidTech as 'accounting services' and JEWISHColorado as 'investment management', which points to back-office (FoundationHub) use."

### `research/mission-2026-11-14/queue-agentic-products-dafpay-fees.md`

21. **Line 15 and line 47 (AP13).** Replace "external match decline 30% → <3%" with: "external match decline 30% → <3% at **one unnamed early-adopter partner** (vendor blog)". Keep "500+ clients" as a separate adoption figure, not an outcome.
22. **Line 109 (Every.org).** Add: "Every.org currently absorbs the For Good fee for bank-account gifts; nonprofits avoid it by linking Stripe or PayPal Grants (0%). The live pricing page was not re-read (HTTP 429) on 2026-11-14."
23. **§3.4.** Add: "The rounding applies only where no platform agreement sets the fee, and most platforms let donors cover the fee, so 4.0% at $25 is the nonprofit's worst case."

### `data/mission-2026-11-14/agentic-philanthropy-products-2026.csv`

24. **Row 14 (Benevity).** Replace "external match decline rate 30% -> <3%" with "external match decline rate 30% -> <3% (one unnamed global partner, vendor blog)".

## Primary sources used

- EDGAR filings:
  - Audax Private Credit Fund 10-Q, filed 2026-11-12.
  - Golub Capital BDC: 10-K FY2022, 10-K FY2023 and 10-K FY2025, and the 10-Q filed 2026-08-03.
  - Monroe Capital: 10-K FY2023 and 10-K FY2025; Monroe Capital Income Plus 10-Q, filed 2026-11-06.
  - BlackRock Capital Investment 10-K FY2022; BlackRock TCP 10-K FY2022, 10-Q Q3-2023 and 10-K FY2025; BlackRock Direct Lending 10-K FY2025.
  - AB Private Credit Investors 10-K FY2022, 10-Q Q3-2023 and 10-Q Q3-2025; AB Private Lending Fund 10-Q, filed 2026-11-13.
  - FS KKR 10-Q, filed 2026-11-05.
- IRS e-file XML 202611199349300601, 202511349349313096, 202533219349318548 and 202601219349301200; ProPublica API for EINs 311640316, 232888152 and 731554474.
- Chariot Nonprofit Terms (2026-10-14), Chariot pricing page and DAFpay FAQ; Givebutter help (2026-10-06); Bloomerang blog (2026-10-29); Donorbox DAF page; dafdirect.org; PayPal help HELP207; Every.org pricing (search-index read).
- Benevity blog "ai-corporate-giving-impact".
- SVCF Advised Fund Agreement (©2025); GKCCF knowledge hub and sample check; San Diego Foundation Recommend-a-Grant; Omaha CF "How a Fund Works"; Tulsa CF Donor FAQ (2025-08).
- fidtechpartners.com; jewishpgh.org/changes-to-donorsphere; ghcf.org/access-donorsphere; hawaiicommunityfoundation.org/donorsphere; Fidelity Charitable statements how-to PDF.
