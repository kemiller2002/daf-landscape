# Evidence Quadrant v1.2: targeted re-score of bank programs and NCF

**Date:** 2026-11-14. **Method:** [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) v1.0 with the binding §7 v1.1 notes.
**Scope:** five provider rows only.
- A3: BofA Charitable Gift Fund, Morgan Stanley GIFT, Goldman Sachs Philanthropy Fund, NCF
- A1: NCF (sponsor-built, Salesforce)

**Trigger:** new primary evidence from [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md). It includes the public MS GIFT Donor Circular, the BofA 2024 guidelines and 2025 portal guide, the NCF live guide, and filed CY2024 990s. This counts as a Clarity reconsideration trigger under methodology §5.

**Files written:**
- `data/mission-2026-11-14/quadrant-scores-A3-v12a.csv`, `quadrant-scores-A1-v12a.csv` (pass 1)
- `quadrant-scores-A3-v12b.csv`, `quadrant-scores-A1-v12b.csv` (pass 2)
- `quadrant-calibration-criteria-v12a-vs-v12b.csv`, `quadrant-calibration-providers-v12a-vs-v12b.csv`
- `quadrant-scores-A3-v12consensus.csv`, `quadrant-scores-A1-v12consensus.csv` (these 5 rows only)
- `quadrant-positions.csv` and `quadrants/*.svg`, regenerated. The v11consensus rows were byte-checked as unchanged.

No outreach, logins or form submissions. The NCF donor login returned 401, and only its public login markup was read.

---

## 1. Positions: v11consensus compared with v12consensus

Bands are given as [low–high]. U criteria are set to 0 for the low end and 4 for the high end. Coverage is scored weight ÷ 1.0.

| Area | Provider | v11consensus | v12consensus X (band, cov) | v12consensus Y (band, cov) | v12consensus quadrant |
|---|---|---|---|---|---|
| A3 | BofA Charitable Gift Fund | X 2.18 / Y 1.00 (Y cov 0.15). **Insufficient evidence** | 2.47 [2.10–2.70], 0.85 | 1.18 [1.00–1.60], 0.85 | **Scale Operators** |
| A3 | Morgan Stanley GIFT | X 2.64 / Y 1.00 (Y cov 0.15). **Insufficient evidence** | 2.76 [2.35–2.95], 0.85 | 1.33 [1.00–2.00], 0.75 | **Scale Operators** |
| A3 | Goldman Sachs Philanthropy Fund | X 2.64 / Y 1.00 (Y cov 0.15). **Insufficient evidence** | 2.82 [1.55–3.35], 0.55 | 1.00 [0.15–3.55], 0.15 | **Insufficient evidence** (no change) |
| A3 | NCF | X 2.79 / Y 1.50 (Y cov 0.15). **Insufficient evidence** | 2.80 [2.80–2.80], 1.00 | 2.42 [1.45–3.05], 0.60 | **Proven Leaders** (Y band crosses 2.0) |
| A1 | NCF (sponsor-built, Salesforce) | X 2.55 / Y 1.00 (Y cov 0.15). **Insufficient evidence** | 2.00 [1.50–2.50], 0.75 | 2.17 [1.30–2.90], 0.60 | **Proven Leaders (boundary)** |

**How to read these:**
- **Four of five rows leave "insufficient evidence".** The cause is Y-axis coverage, which was 0.15 for every row under v11. All four now have Y coverage of at least 0.6.
- **GS PF stays insufficient.** Its only public terms date from 2008.
- **NCF A3: Proven Leaders, but treat as boundary in substance.** The script labels a row "boundary" only when the point is within 0.25 of a midline. Methodology §4 says a band that crosses a midline is "boundary", and NCF's Y band [1.45–3.05] crosses 2.0. Read it as Proven Leaders/Scale Operators boundary.
- **NCF A1 sits on both midlines.** X is exactly 2.0. The position is fragile.
- **MS GIFT's Y band only reaches 2.0 at the top** (Y1 is still U). It is Scale Operators with low forward capability.
- **BofA** is firmly Scale Operators. Its check-only rail and missing donor-elective outbound term hold Y near 1.

## 2. Criteria that moved (v11consensus to v12consensus), with evidence

### BofA Charitable Gift Fund (A3)

| Criterion | v11 | v12 | Evidence |
|---|---|---|---|
| X2 | U | 2 | The portal notice "Balances ... are now available on MyMerrill and Private Bank Account Access" is delivered in the 9/2025 guide. That is the only testable announcement, so the record is thin ([portal](https://bofa.donorfirst.org/); [guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) |
| X4 | 2 | 3 | Five confirmed touchpoints: MyMerrill, Private Bank Account Access, the BofA Online hand-off, Merrill Edge clients (8/2024 sheet) and adviser registration through a Ren mailbox. It is not 4, because all belong to one banking group |
| X5 | 3 | 4 | The 990 gives formation year 1955; there are 17,840 DAF accounts and a bank corporate trustee. This meets "long operating history plus diversified customers" ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml)) |
| X6 | U | 2 (vendor_claim) | "95% of grants are mailed within 7-10 business days; among those, the average is 5 days" ([sheet](https://bofa.donorfirst.org/pdf/bofa/Making%20the%20Most%20of%20your%20CGF%20Account.pdf), read from rendered page) |
| Y1 | U | 1 | The contribution listing can be exported to Excel. There is no grant export, no API and no contractual right |
| Y2 | U | 1 | "Grants are issued via checks", sent by USPS first class only ([guidelines v3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf)) |
| Y4 | 1 | 2 | Merrill and Private Bank clients, plus Merrill Edge clients and online applicants "not affiliated with a Merrill or Bank of America Private Bank associate" |
| Y5 | U | 1 | An outbound DAF grant is allowed only "If a Donor's or Advisor's advisory rights are terminated ... by the Charitable Gift Fund". This is not a donor-elective outbound term |

### Morgan Stanley GIFT (A3)

| Criterion | v11 | v12 | Evidence |
|---|---|---|---|
| X2 | U | 2 | **Delivered:** recoverable grants, recurring grants and NextGen are documented in the Aug-2024 circular and the 2024 impact report (122,000 grants in 2024).<br>**Not matched:** the brochure's ACH claim. The 2022 grantee guidance still says check plus letter ([impact report](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf)) |
| X4 | 2 | 3 | The circular lets Financial Advisors and branch staff submit grants "upon the donor's ... verbal direction". The Ren portal and CapShift administration are also confirmed ([circular](https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf), read by OCR) |
| X5 | 3 | 4 | Formation year 2001; 21,800 DAFs |
| X6 | U | 2 (secondary) | One low-severity structural complaint in the repo corpus. No service metrics |
| Y2 | U | 2 (vendor_claim) | The circular sends grants using a "validated mailing address or banking details". The brochure claims "Rapid disbursement technology with ACH" |
| Y3 | U | 1 (vendor_claim) | The brochure claims "Charity Vetting — Automated with advanced tech". The circular keeps Board approval of every grant |
| Y5 | U | 1 | Inbound only: the portal offers to "transfer a private foundation to a simpler gifting solution". No outbound term (§7 cap) |

### Goldman Sachs Philanthropy Fund (A3)

| Criterion | v11 | v12 | Evidence |
|---|---|---|---|
| X5 | 3 | 4 | Formation year 2001; 4,134 DAFs; $5.83bn contributions in CY2024 ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml)) |
| X1 | 3 | 3 | Score unchanged. The evidence pointer now cites the filed CY2024 return ($12.64bn) instead of "no filed return" |

Y1, Y2 and Y5 stay U (see adjudication). The live donor web is Ren iPhi ("iPhi ... © 2001 - 2026 Stellar Technology Solutions"). That is an A1 Ren customer edge, not GS PF evidence.

### NCF (A3)

| Criterion | v11 | v12 | Evidence |
|---|---|---|---|
| X2 | U | 3 | The recurring-schedule feature (2023 story) and eGrants are live in the 2026 guide and on the EFT page |
| X5 | 3.5 | 4 | The audit was read: Capin Crouse, "present fairly, in all material respects", no going-concern doubt. NCF has operated "Since 1982" and holds 31,943 DAFs ([FY2025 audit](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf)). The v11 deduction for five-donor concentration (14% of support) was not applied, because the rubric names "single-customer dependence", not donor concentration |
| X6 | U | 2 (vendor_claim) | NCF states that most grants are processed in two or three business days. There are no severe service complaints in the corpus |
| Y2 | U | 3 | "Most grants are distributed electronically when possible", through in-house NCF eGrants. It stays below 4 because enrolment is manual (up to six weeks) and no state is shared with nonprofits ([guide](https://www.ncfgiving.com/guide-to-giving-at-NCF); [EFT](https://www.ncfgiving.com/eft-charity-sign-up)) |
| Y4 | 1.5 | 2 | "Individuals, families, businesses, and private foundations", plus collaborative church funds and advisers. All are faith-aligned |
| Y5 | U | 2 | Standard Giving Funds may grant to "other donor-advised fund sponsors"; succession funds may not. There is no history export |

X3 stays 3: the audited statements were read by pass 2 itself. X4 stays 2.

### NCF (sponsor-built, Salesforce) (A1)

| Criterion | v11 | v12 | Evidence |
|---|---|---|---|
| X1 | 3 | 2 | The platform serves one sponsor ($5.68bn, 31,943 DAFs). The A1 rubric reads this as a mid-tier footprint, not a dominant one |
| X2 | U | 3 | The MyGiving login is live on Salesforce/Skuid (`sfdc` and `skuid` resources); eGrants and recurring schedules are delivered |
| X4 | 1.5 | 1 | Captive: used only by NCF givers, advisers and affiliates |
| X5 | 3.5 | 2 | The operator is audited and keeps investing in the platform ($2.0m of capitalised software development in 2025). But the platform has one customer by design, which is a rubric-0 signal. **The two signals were netted to 2.** This is the largest judgment call in the re-score |
| Y2 | U | 3 | Same evidence as A3 Y2 |
| Y5 | U | 2 | EFT, check and wire rails; outbound grants to other sponsors are supported; no history export |

X3 stays U. The audit says "no such opinion is expressed" on internal control, and there is no SOC report. Under the entity-scope rule, the sponsor audit is not platform-control evidence. Stellar (Ren) received $2.50m for "software/consulting" in CY2024. Its scope is not visible, so under the §7 scope rule the row stays sponsor-built.

## 3. Agreement statistics (v12a compared with v12b)

| Measure | Value |
|---|---|
| Criterion pairs | 55 (5 providers × 11) |
| Both U | 16 |
| Both scored | 37 |
| Exact agreement when both scored | 26 of 37 (70%) |
| Within 1 point | 37 of 37 (100%) |
| Gap > 1 | 0 |
| One scorer U (flagged) | 2: GS PF Y2 and NCF X6 |
| Overall cell agreement, U counted as a value | 42 of 55 (76%) |
| Quadrant reproduced | 3 of 4 scoreable rows (BofA, MS GIFT, NCF A3). GS PF is insufficient for both |
| Quadrant disputed | 1: NCF A1. v12a gave Scale Operators (boundary) at Y 1.75; v12b gave Proven Leaders (boundary) at Y 2.17. The only difference is Y2 (2 compared with 3) |

### Adjudication of the flagged cells and the one-point gaps

| Cell | v12a | v12b | Consensus | Reason |
|---|---|---|---|---|
| GS PF Y2 | U | 1 | **U** | The only public circular is from Aug 2008. Since then the administrator role and platform changed (Ayco plus Ren iPhi, Goldman.com SSO). Under the bounded-truth rule an 18-year-old document cannot score a 2026 rail |
| NCF X6 | U | 2 | **2 (vendor_claim)** | The sponsor-stated processing time is admissible as vendor_claim, consistent with BofA X6 |
| BofA X2 | 3 | 2 | 2 | Only one announcement to test |
| BofA X4, MS GIFT X4 | 2 | 3 | 3 | Several confirmed touchpoints within one group |
| BofA, MS GIFT, GS PF X5 | 3 | 4 | 4 | The rubric's "long operating history plus diversified customers" is met: formation 1955 or 2001, thousands of accounts |
| BofA Y5 | 2 | 1 | 1 | The outbound clause applies only when CGF terminates advisory rights |
| MS GIFT Y4 | 1 | 2 | 1 | Entity-donor and NextGen accounts are account types inside the Morgan Stanley wealth channel |
| NCF A3 X4 | 2 | 3 | 2 | No third-party channel edges beyond Salesforce are confirmed |
| NCF A3 Y2, A1 Y2 | 2 | 3 | 3 | Primary text says "Most grants are distributed electronically". This is one of the three level-4 features |

**Effect of the A1 Y2 call:** setting NCF A1 Y2 to 3 moves the A1 row across Y = 2.0. The consensus therefore inherits the dispute. Report the A1 position as **boundary on both axes**, not as Proven Leaders.

## 4. AI overlay (v1.1 vocabulary)

| Provider | Overlay | Basis |
|---|---|---|
| BofA CGF | none evidenced | No automation or AI statement in the guidelines, guide or portal |
| Morgan Stanley GIFT | **AMBER (provisional)** | The brochure claims "Automated" charity vetting with "advanced tech", but limits and controls are undocumented. Board approval of each grant remains, per the Aug-2024 circular. It is not labelled AI. If the automation is rule-based only, the flag should drop to none |
| GS PF | none evidenced | — |
| NCF (A3 and A1) | none evidenced at v1.2; at the next re-score AMBER (low), provisional, under methodology §7a and §7b: NCF’s own “AI-powered search experience” (ncfgiving.com/ai-search, record dated 2026-08-12, record status field “private”; gap19-ai-coverage S18–S20), re-read 2026-11-20; a read-only search with undocumented controls, as Candid’s AMBER (low) (b4301-05) [V wave 43A] | — |

No row is RED. No evidence shows an automated process completing a money-moving or status-clearing action without sponsor or human approval. No row is GREEN, because none documents flag-only design or authority separation.

## 5. Caveats

- **Independence is weaker than the two-scorer rule intends.** One agent ran pass 1 and pass 2 in sequence. Pass 2 re-read the rubric and fetched primary sources itself:
  - the BofA guidelines, guide and sheet (the sheet was rendered to images);
  - the MS circular (OCR of 16 rendered pages), brochure, impact report and portal;
  - the GS circular and donor web;
  - the NCF guide, support page, EFT page, audit and login markup;
  - four 990 XMLs.

  Even so, pass 2 had seen the pass-1 numbers. The 70% exact agreement is therefore an upper bound on what two separate agents would reach. Under methodology §5 these positions remain **internal-demonstration** until a separate agent reproduces them.
- **The pass-1 evidence base was not blind to v11.** The input file it was told to use ([queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md), "Evidence for quadrant re-scoring") quotes v1.1 consensus values and recommended levels. Pass 1 opened no quadrant-scores, positions, calibration or quadrant-*.md file, but it did see those quoted values.
- **The X5 = 4 calls for three bank programs rest on 990 formation year and account counts.** No audit for those programs was read, and X3 stays U for all three.
- **Bounded truth:** BofA terms are v3.2024 (2025 and 2026 files return 404), MS GIFT terms are Aug 2024, and GS PF terms are Aug 2008. The live pages were retrieved on 2026-11-14.
- **Other providers are untouched.** All other A1 and A3 rows keep their v11consensus positions. A full-area chart now mixes scorer vintages only through the separate `A3-v12consensus.svg` and `A1-v12consensus.svg` files.

## 6. Follow-ups

1. **A separate agent should blind re-score the NCF A1 row**, given the disputed quadrant and the X5 judgment.
2. **MA AG registry retrieval of the BofA CGF audit** would unlock X3, the only X-axis U left for BofA.
3. **GS PF needs a current Program Circular** for Y1, Y2 and Y5. It cannot be obtained without client access, so the row stays insufficient.
4. **Record Ren A1 customer edges** for GS PF (iPhi donor web) and BofA CGF (DFX portal) at the next A1 re-score.
