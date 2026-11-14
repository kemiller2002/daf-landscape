# Validation wave 1: independent check of 22 claims

**Validator:** independent-validation-agent-wave1 | **Date:** 2026-11-14 | **Register:** `data/mission-2026-11-14/validation-register.csv`

## Method
- Input: `data/mission-2026-11-14/validation-claims-wave1.csv`. I did not open the repo research files until I had a verdict for each claim. After that I opened them only to compare source choice and wording.
- Primary sources used:
  - Audited statements: RCF, Fidelity Charitable and Vanguard Charitable PDFs.
  - IRS Form 990 e-file renders from ProPublica (`/nonprofits/full_text/{object_id}/{form}`). The PDF downloads were blocked by a security check.
  - Official press releases from Foundation Source, PR Newswire/TIAA, SEI, Daffy, Great Hill, AEF and NPT.
  - Live pages: the RCF FAQ, the donorfirstx and donorfirst portals, and Chariot's terms.
  - SEC IAPD Form ADV 2A brochures.
  - SEC EDGAR full-text search.
  - The DAF Research Collaborative (DAFRC) April 2026 updated memo.
- Arithmetic: I recomputed every YoY change and ratio myself.
- Limits:
  - The web-search budget ran out partway through. After that I fetched official sites directly.
  - web.archive.org could not be reached. This affected V1-05.

## Counts
| Result | n | Claims |
|---|---|---|
| confirmed | 17 | 01, 02, 03, 04, 06, 07, 09, 10, 11, 12, 14, 15, 17, 18, 19, 21, 22 |
| partially_confirmed | 3 | 08, 13, 16 |
| contradicted | 1 | 20 |
| unable_to_verify | 1 | 05 |

## Discrepancies (all)
- **V1-01:** RCF's 2021 payment to Ren is $10,880,690 in the audit and $10,880,689 on the 990. This is a $1 rounding difference with no effect.
- **V1-02:**
  - The fee basis is "administrative fee revenue earned ... from **individual fund holder accounts**", not all fundholder fees.
  - The 2023 audit confirms the 98% rate took effect in FY2023 (95% applied in FY2022).
- **V1-03:** The Edward Jones brochure names only "a third-party administrator". RCF's role comes from the donorfirstx portal ("partnered ... to manage and administer") and from RCF's own materials.
- **V1-04:** The claim drops the RCF FAQ phrase "**administrative infrastructure**". The audits also describe "administration services". Ren is an administrator, not only a technology vendor.
- **V1-05:**
  - The cited Ren PDF returns 404 and I found no archive copy.
  - The date (2021 vs 2022) is unresolved.
  - It is unclear whether the "$2.9bn" subject is Ren or RCF.
- **V1-06:** Giving Place is software for private foundations and family offices, bought "from Give, a TIFIN Company". It is not TIFIN's DAF platform.
- **V1-08:**
  - Kump's title in primary sources is "President, DAF Division" (FS team page) or "President of DAFs" (press release), not "DAF Technology President".
  - He is Charityvest's **President** (an officer, 40 hrs/week) as well as a director.
  - Charityvest's 990 Schedule O says management duties are delegated to Vennfi/Foundation Source and Kump is "compensated by Foundation Source" ($163,944 from Vennfi in 2024).
  - The $653,137 "platform fee" on the 990 does not name a payee.
  - Part VII-B lists **0** contractors over $100k, which does not fit with a payment to Foundation Source of that size.
- **V1-09:**
  - The source says "assets under management", not "assets".
  - These are company KPIs. The Form 990 for TY2024 shows contributions of **$111.9M**, against the company's 2024 figure of $99.2M.
  - 990 net assets at end-2024 were **$103.2M**, against an AUM of about $122.1M implied by $224.6M being up 84%. Do not mix the two sets of figures.
- **V1-11:** The release is dated Sept 30, 2026. "$720M in 2025" means year-end 2025. "Unaudited" refers to the 1/1/2026–8/31/2026 results.
- **V1-13:** **Misattributed.** Both SOC statements are in the "About Ren" boilerplate and are claims about Ren as a company (Type 2 in July 2025, Type 1 in April 2026). They are not AEF claims about "its Ren-powered platform".
- **V1-14:**
  - The NPT annual report says $6.44bn granted. The 990 for TY2024 (fiscal year ending 6/2025), line 13, shows $6,415,072,479, a gap of about $25m.
  - Implied FY24 grant count: 159,543/1.23 ≈ 129.7k.
- **V1-15:**
  - Note 7 ties FMR to the **administrative** fee ($179.9M), not to the $84.3M investment management fees.
  - The fiscal year ended 6/30/2025.
  - Note 2 refers readers to "Note 8", but the relevant text is in Note 7.
- **V1-16:** $4,014,052 is the **FY2025** comparative. The current FY2026 statements (posted 2026-11) show **$4,243,096**. The claim omits the fiscal year and is out of date.
- **V1-17:** Figures confirmed against the April 2026 memo. The original 2025 report figures (3.56m accounts, $326.45bn assets, $89.64bn contributions, $64.89bn grants) are superseded.
- **V1-20:**
  - EDGAR full-text search of Bank of America's filings (CIK 70858) found 0 hits for "Charitable Gift Fund", "RenPSG", "Renaissance Administration" and "Ren, Inc".
  - The Charitable Gift Fund's 990 does not mention Ren.
  - The only evidence of a Ren link is the live portal `bofa.donorfirst.org`: an advisor contact at `charitablegiftfund@reninc.com`, "DFX powered by Ren", and an HTML comment "Powered by Renaissance Administration LLC".
- **V1-21:**
  - The **primary** IRS e-file (object 202503109349303645) confirms the figures exactly: 4,134 funds; $5,833,783,136 contributions; $3,071,806,783 grants; $12,640,914,117 year-end value.
  - The legal entity is GS Donor Advised Philanthropy Fund for Wealth Management Inc (DBA "GS DAF"), EIN 31-1774905.
- **V1-22:**
  - The brochure cover is dated Aug 11, 2026 and IAPD shows it submitted 8/14/2026. The same text appears in three OneAscent advisory firms' brochures (OAWM, OAFS, OAFO).
  - The claim omits the second disclosed conflict: OneAscent Investment Solutions (OAIS) model funds inside OneGive.

## Claims the repo overstates
1. **V1-20 (bofa-…-relationship):** The title and claim say 10-K/filings show the Ren link. They do not; only the portal does. Lower confidence on any contractual or economic inference.
2. **V1-13:** This is framed as a contradiction in AEF's assurance claims. It is actually inconsistent **vendor (Ren) boilerplate**, with no SOC report available. It is not evidence about AEF's own controls.
3. **V1-05:** The $2.9bn Edward Jones figure rests on a document that is no longer available. Mark it unverified or historical, low confidence.
4. **V1-08:** "Fee-paid" to Foundation Source is inferred, because the 990 payee is unnamed. However, the conflict is *understated* in another respect: the vendor pays the charity's president.
5. **V1-16:** The FY2025 figure is presented as current.
6. **V1-04:** "Technology" framing understates Ren's administrative role.

Understated (can upgrade): **V1-21**, whose primary source is now verified.

## Recommended corrections
- `research/bofa-charitable-gift-fund-10k-ren-relationship-2026-11-11.md` and any claim row: replace "Bank of America 10-K or filings evidence a Ren relationship" with: "No BAC SEC filing or BofA Charitable Gift Fund Form 990 (TY2023–24) mentions Ren; the only public evidence is the bofa.donorfirst.org portal (advisor contact charitablegiftfund@reninc.com; 'DFX powered by Ren'). Scope and economics unknown."
- `research/soc2-assessment-2026-11-11.md`: replace "AEF ... claimed SOC 2 Type II for its Ren-powered platform; April 2026 language said Type I" with: "AEF-hosted joint releases carry Ren's 'About Ren' boilerplate stating Ren 'holds a SOC 2 Type 2 certification' (2025-07-23) and 'SOC 2 Type 1 certification' (2026-04-08); no report seen; these are claims about Ren, not AEF."
- `research/edward-jones-ren-renaissance-charitable-relationship-2026-11-12.md` line 9:
  - Add: "Source PDF returned 404 on 2026-11-14 and no archive copy was retrieved; unverified, low confidence."
  - Line 7: change "Ren supplies technology and operational support" to "Ren supplies 'the institutional-grade platform, administrative infrastructure, and operational support'".
- `research/sponsor-governance-and-fee-transparency-2026-11-11.md` line 8:
  - Add: "Kump is Charityvest's President (990 TY2024, Part VII) and 'President, DAF Division' at Foundation Source; Schedule O states he 'is compensated by Foundation Source' ($163,944 via Vennfi, 2024)."
  - Change "fee-paid" to "paid a $653,137 'platform fee' (payee not named on the 990; Part VII-B lists no contractor >$100k)".
- `research/batch-1d-vanguard-npt-dafgiving360-fee-audit-2026-11-12.md` line 8: update to "$4,243,096 (FY2026, FYE 6/30/2026) and $4,014,052 (FY2025) per FY2026 audited statements, Note 1", and cite VCEP_Financial_Statements_2026.pdf.
- `research/goldman-sachs-two-daf-programs-2026-11-11.md` line 7: drop "Secondary source" and use: "IRS e-file 202503109349303645 Schedule D Part I: 4,134 DAFs; contributions $5,833,783,136; grants $3,071,806,783; year-end value $12,640,914,117 (verified)."
- `research/startups-and-emerging-competitors-2026-11-12.md` line 18: change "$224.6M AUM" context to add "company-reported; not comparable to 990 (TY2024 990 contributions $111.9M vs company $99.2M; net assets $103.2M)".
- `research/oneascent-onegive-charityvest-disclosed-incentives-2026-11-11.md`: note that the IAPD submission date is 8/14/2026, and that the same text is in the OAFS and OAFO brochures (OAFS = OneAscent Financial Services, OAFO = OneAscent Family Offices).
- `research/batch-1c-affiliated-provider-fee-tracing-2026-11-12.md`: no change needed; its caveat on the $84.3m is correct. The claim row in `validation-claims-wave1.csv` (V1-15) should read "Note 7 ties administrative fees ($179.9m FY2025) to FMR; $84.3m investment management fees are not attributed to FMR in the notes."
