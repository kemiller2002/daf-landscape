# National Philanthropic Trust: FY2025 financial and technology diligence
**Date:** 2026-11-11. **Status:** Public evidence review, no vendor contract, independent software audit or operational testing.

## Executive findings
NPT (EIN 23-7825575) is a large independent DAF sponsoring charity, distinct from a bank-branded sponsor and from a commercial DAF technology supplier. Its FY2025 fiscal year ended June 30, 2025. Its IRS Form 990 Schedule D, tax year 2024 filing, reports **20,691 DAF accounts**, **$15,153,667,777 contributions**, **$6,415,072,479 grants** and **$55,895,378,438 year-end DAF value**. These are sponsor financial measures, not platform vendor revenue.

NPT's FY2025 annual report says it processed **159,543 grants**, a **23% year-on-year increase**, and granted **$6.44b**. The approximately $25m difference from Schedule D grant value may be due to classification, timing or presentation; the cause has not been established. Reconcile before analysis.

Its FY2025 Form 990 shows **$55,802,354,506 net assets**, **$56,096,033,883 total assets**, **$17,794,939,562 total revenue** and **$6,575,730,481 total expenses**. Large contribution and grant amounts dominate these accounting totals. Neither reported net surplus nor total expenses represent sponsor operating profit or platform spend.

NPT states it launched **NPT GivingPoint** in 2021 as a full-service online donor platform. This is a named platform and a possible basis for technology architecture/ownership diligence, not proof of fully proprietary code or lack of outside vendors. No confirmed Ren technology or administration relationship was found in this research pass; absence of evidence is not evidence of absence.

## FY2024 operating-cost leads (year ended June 2024)
The FY2024 Form 990 Part IX reports **$3,649,680 information technology**, **$74,179,211 investment management fees**, **$2,500,886 other service fees**, and **$25,051,026 other salaries and wages**. These are accounting expense categories, not all-in platform costs or payee-specific vendor amounts. The FY2025 versions require extraction and verification.

## First diagnostic comparisons
1. **Sponsor versus vendor:** NPT is a legal sponsor holding assets and processing grants. Ren is a commercial service supplier in other documented arrangements. Compare legal/economic functions, not total sponsor assets versus vendor revenue.
2. **Scale:** NPT's $55.9b year-end DAF assets exceed the specific Goldman Sachs PWM and Morgan Stanley GIFT sponsor totals reviewed previously, but differing fiscal periods and program definitions limit direct comparisons.
3. **Grant throughput:** 159,543 reported grants provide an operating-scale denominator; grant processing labor, failure rates, exception handling and payment settlement timing are unknown.
4. **Technology:** GivingPoint exists as an NPT-branded platform. Need determine IP ownership, hosting, vendor dependency, authoritative fund ledger, adviser integration, migration/export and SOC control scope.
5. **Payout:** $6.415b annual grants divided by $55.895b ending assets is about 11.5%, but this is **not** a standard cohort-based payout rate and is affected by contributions, market changes and timing.

## Clarity challenges
- **NPT generated $11.2b profit:** invalid. Form 990 revenue less expense reflects contributions, asset activity and grants of a charitable sponsor, not commercial operating earnings.
- **NPT IT spend is only $3.65m:** the line item is a partial expense classification from FY2024, not total technology ownership cost; staff, depreciation, outsourcing and embedded services may appear elsewhere.
- **GivingPoint is proprietary end-to-end:** branding and launch announcement do not establish source ownership or full-stack architecture.
- **NPT is a Ren customer:** not established by the sources examined.
- **Grant count establishes productivity:** no labor denominator or grant complexity adjustment.

## EDF proposed control chain
Contribution acceptance → sponsor ledger → custody and investments → GivingPoint donor/adviser interface → grant recommendation → approval → payment execution → recipient settlement and returns. Test authoritative state and actor at each boundary; do not assume a failure without evidence.

## Next evidence requests
- FY2025 original Form 990 and Schedule O/R, audited financial statements, named contractors, technology and investment expense allocations.
- GivingPoint vendor and integration stack, IP/licensing, hosting, operational resilience, backup and portability proof.
- Fund-level investment and adviser custody arrangements; NPT private-label or institutional partnership contracts.
- Grant lifecycle timestamp samples and staffing/exception cost by stage.
- Reconcile $6.44b annual-report grants with $6.415b Schedule D grants and distinguish approved versus paid versus settled.
- Compare NPT sponsor economics with RCF, MS GIFT, BofA CGF, and Goldman PWM on aligned years and denominators.

## Sources
- NPT FY2025 annual report: https://www.nptrust.org/annual-reports/npt-annual-report/
- NPT FY2024 annual report: https://www.nptrust.org/annual-reports/the-2024-annual-report/
- NPT organizational history / GivingPoint: https://www.nptrust.org/about-us/
- FY2025 Form 990 Schedule D: https://t.co/ND32SMgsMB
- ProPublica FY2025 990 extraction: https://projects.propublica.org/nonprofits/organizations/237825575
- FY2024 detailed 990: https://philanthropy.org/990/report/237825575/national-philanthropic-trust/2024
