# Batch 1D: DAFgiving360 disclosure access, Vanguard embedded investment economics, NPT fee classification
**Date:** 2026-11-12. **Scope:** M01/M02/R04. **Status:** Partial; no fabricated affiliated fee totals.

## New verified findings
### Vanguard
Audited FY ended June 30, 2025: https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf
- Note 1 p6: 35 of 37 investment pools are made up of Vanguard mutual funds and ETFs; two other pools offered by RhumbLine and Hamilton Lane. Count of pools is **not** asset weighting.
- Note 1 p6: $4,014,052 in Vanguard-related investment recordkeeping and administrative service fees in FY2025 ($3,916,396 FY2024). Already included in functional expenses; do not add again.
- Note 3 pp10–11: Vanguard-labelled investment pools individually disclosed with year-end values. Total mutual funds/ETFs in fair value table **$25,099,507,281** at June 30 2025, but this line is NOT a verified sum of exclusively Vanguard products, and may include nonpooled investments; avoid calling all $25.1b Vanguard-affiliated AUM.
- Note 3 p11: separate Low Carbon Fund $854,094,551 and private equity contributed assets $1,134,555,339. These categories should not be included in a Vanguard mutual-fund fee estimate.
- Note 6 p13: unsecured, interest-free financing arrangement up to **$6.5m**, **zero balance** and **no draws** in FY2024 or FY2025. **Do not treat credit facility ceiling as outstanding subsidy or affiliate payment.**
- Note 7 p13: 0.60% base sponsor admin fee (discounts possible) is **embedded in investment income / pool NAV**, not a separately identifiable revenue line in statements. Underlying fund expense ratios also reduce NAV; public policy says Vanguard Charitable itself does not charge an investment fee. Thus the sponsor's functional expense total is **not** the total economic burden on DAF assets.
- Fund expense ratios vary by investment pool and share class; estimating Vanguard Group's actual fund fees requires holdings by underlying fund/share class and period-average balances. A year-end-balance × current expense-ratio exercise is only illustrative and cannot identify profit.
- Important asymmetry: Fidelity has documented administrative-fee contractual payments to FMR, while Vanguard discloses $4.014m service fees plus underlying affiliated fund exposure and NAV-embedded sponsor admin fee. Comparing these two direct fee figures alone is invalid.

Vanguard policy source: https://www.vanguardcharitable.org/company-policies/policies-and-guidelines

### NPT
FY2025 IRS Form 990 as shown by IRS-derived ProPublica and philanthropy.org:
https://projects.propublica.org/nonprofits/organizations/237825575
https://philanthropy.org/990/report/237825575/national-philanthropic-trust
- Ending net assets **$55,802,354,506**, total assets **$56,096,033,883**. Use these for the FY2025 990 basis; older figures in other notes may refer to a different population or report and require reconciliation.
- Investment-management expense **$93,771,463**, split **$93,512,965 program** and **$258,498 management**.
- Information technology **$5,871,282**, split $1,996,236 program / $2,348,513 management / $1,526,533 fundraising.
- Grants and similar amounts paid **$6,415,072,479**. FY2025 annual report says ~$6.44b grants and 159,543 grants processed; difference requires definition and period reconciliation, not automatic error designation.
- The 990 categories do not disclose which share of $93.77m went to outside RIAs, investment managers, NPT-affiliated service providers, or Ren. **Do not attribute it to Ren or any one payee.**
- Approximate beginning/end net assets average = ($41,882,463,155+$55,802,354,506)/2 = **$48,842,408,831**. $93,771,463 / that proxy = **19.20 basis points**. This is a rough **expense-to-balance proxy**, NOT a fee schedule, realized fee rate or margin; year-end balances are poor denominators for flows, changing investment pools and donor contributions.
- NPT FY2025 report: https://www.nptrust.org/annual-reports/npt-annual-report/

### DAFgiving360
Official financial disclosures portal: https://www.dafgiving360.org/about-dafgiving360/financials
- The portal provides a **Financial Statements** link which redirects to https://www.dafgiving360.org/resource/financial-statements ; in this research session the link resolves to a page without readable statement text. **No FY2025 audited related-party transaction amounts verified.**
- Record as a document access gap. Do not invent a Schwab affiliate payment amount from published sponsor fee schedules, 990 expense categories, or third-party guesses.
- Next retrieval: obtain the actual downloadable PDF or FY2025 Form 990 Schedule L/R/O and audited notes, identify legal vendor entity and transaction amount; compare current brand (DAFgiving360) to prior legal entity name Donor Advised Charitable Giving Inc.

## Clarity and EDF implications
1. **Affiliated distribution is documented** at Vanguard through 35 pools and related service contracts, but no actual fund-management profit is established.
2. **Accounting invisibility matters**: expenses assessed in underlying NAVs are not necessarily separate sponsor operating expense lines. Comparing sponsor Form 990 totals across business models understates fee layers.
3. **Related-party facility ≠ cash payment**: Vanguard's $6.5m facility had zero draw and balance in both years.
4. **NPT expense ≠ Ren revenue**. A $93.77m category cannot establish any named technology-vendor contract.
5. **Disclosure accessibility ≠ non-disclosure**: DAFgiving360 publicly links financial statements, but the audited content was not accessible in this session.

## Remaining tasks
- Retrieve DAFgiving360 full audited FY2025 PDF and related-party notes, cross-check Schedule L/R/O.
- Extract Vanguard Note 3 full underlying pool asset allocation and each current investment-option weighted expense ratio; construct a range explicitly labeled scenario, not affiliate revenue.
- Extract NPT audited FY2025 statements and named investment-manager / related-party notes; reconcile IRS and annual-report metrics.
- Build entity-by-entity affiliate fee beneficiary graph with service, actual amount, date, reporting basis and confidence.
- Separate client relationship retention, personal AUM retention, sponsor-owned external adviser mandate retention and nonprofit impact.

## Validation correction (2026-11-14, independent validation wave 1)
Source: [validation-wave1-report.md](mission-2026-11-14/validation-wave1-report.md), register `data/mission-2026-11-14/validation-register.csv`. Original text above is preserved for traceability; where it conflicts with this note, this note governs.

- **V1-16 partially confirmed (period):** $4,014,052 is FY2025. Vanguard Charitable FY2026 audited statements (FYE 2026-06-30, Note 1) report $4,243,096 related-party support fees for FY2026.
