# Goldman Sachs DAF programs: legal entities, financial scale and technology questions
**Research date:** 2026-11-11. **Evidence status:** public official program documents, SEC proxy and secondary Form 990 extracts; no signed vendor contracts or system tests.

## Central finding: do not combine two separate charities
### GS Donor Advised Philanthropy Fund for Wealth Management, Inc.
- EIN **31-1774905**; described in Goldman Sachs Private Wealth Management July 2025 relationship guide as a separate independent 501(c)(3) public charity that administers PWM client DAFs, owns and controls contributed assets.
- Secondary source reporting **tax year 2024** Schedule D: **4,134 funds, $12.6 billion year-end DAF value, $5.8 billion contributions, $3.1 billion grants**. Verify exact numbers and year against original IRS XML (e-file object 202503109349303645) before modeling.
- Official Goldman FAQ describes $25,000 opening and $5,000 subsequent contribution minimums in the version retrieved; confirm current applicability.
- Sources: https://www.gsbrandguidelines.com/disclosures/customer-relationship-summary-form-crs/docs/pwm-relationship-guide.pdf ; https://nonprofitnewsfeed.com/daf/goldman-sachs-philanthropy-fund/ ; https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111

### The Goldman Sachs Charitable Gift Fund (Goldman Sachs Gives)
- EIN **11-3813663**; program for current and retired senior Goldman Sachs employees, not a substitute for the PWM client program.
- FY2024 (fiscal year ending June 2024) Form 990 Schedule D secondary extraction: **699 funds, $517.2m year-end DAF value, $223.1m grants**; FY2024 Part IX reports **$152k information technology** and **$258k accounting fees**, but neither is a named technology vendor payment.
- FY2025 Form 990 was filed May 4, 2026; later figures must not be mislabeled FY2024. Goldman Sachs' March 2026 proxy says firm contributions supported a **$164m 2025 GS Gives program**; do not conflate with charitable sponsor total contributions or grants.
- Sources: https://philanthropy.org/990/report/113813663/the-goldman-sachs-charitable-gift-fund/2024 ; https://www.goldmansachs.com/community-transformation/goldman-sachs-gives ; https://www.sec.gov/Archives/edgar/data/886982/000119312526117433/gs-20260319.htm

## Comparison to BofA and Morgan Stanley
- **Morgan Stanley GIFT:** Official Morgan Stanley page explicitly names RenPSG as back-office administrator. Confirmed functional relationship, not fee amount.
- **Bank of America CGF:** BofA donor portal provides reninc.com reactivation contact. Direct operational clue; supplier scope unverified.
- **Goldman Sachs PWM DAF and GS Gives:** No verified Ren relationship found in this research pass. Absence of located evidence is **not proof Ren is absent**. Keep administrator and software provider fields unknown until independently sourced.

## Clarity review
1. **Claim:** Goldman Sachs manages $13.1b in a single DAF platform. **Challenge:** distinct entities, constituencies, fiscal year ends and asset accounting. Do not publish summed AUM as one platform or one legal entity.
2. **Claim:** 10-K wealth-management revenue identifies DAF profitability. **Challenge:** no DAF-specific vendor revenue or cost center identified; Form 990 and supplier contracts are better units.
3. **Claim:** $152k information technology expense equals platform cost. **Challenge:** only one expense category at employee program, possibly excluding embedded service, in-kind or affiliate costs.
4. **Claim:** Goldman uses Ren. **Challenge:** no direct evidence found, unlike Morgan Stanley. Mark unknown.
5. **Claim:** Goldman Sachs Gives $2.9b lifetime grants equals current annual flow. **Challenge:** cumulative since inception; not an annual figure.

## EDF: testable system boundaries
- PWM client → wealth adviser → independent sponsor legal ownership → investment management → grant recommendation → approval → payment and nonprofit settlement.
- Employee philanthropy program has a different funding and recommendation population, and potentially different operational governance.
- Candidate controls: identity and authority; separate ledgers; affiliate transaction disclosure; fee pass-through; charity and donor benefit restrictions; grant settlement and audit evidence; migration/export proof. No observed operational failure established.

## Evidence acquisition
1. Download original 2024 and latest 2025 Form 990 XML/PDF for both EINs, reconcile Schedule D Part I, Part IX, Schedule O/R and independent contractor reporting.
2. Identify named administrator, donor portal vendor, custodian, investment adviser, software license and processor for **each** charity.
3. Review Goldman Sachs Group 2025 10-K and 2026 proxy for specific charitable program references; do not use aggregate segment data as DAF results.
4. Reconcile employee GS Gives $164m 2025 firm-supported program against sponsor fiscal-year contribution and grant disclosures.
5. Build normalized sponsor-year panel with fiscal year end, DAF fund count, assets, contributions, grants, admin and IT expense, payees and evidence grade.
6. Seek public program agreements, fee schedules, data ownership, exit/portability, and supplier statements. No unsupported vendor mapping.

## Source trail
- [Goldman Sachs Private Wealth Management relationship guide](https://www.gsbrandguidelines.com/disclosures/customer-relationship-summary-form-crs/docs/pwm-relationship-guide.pdf)
- [Goldman Sachs Gives](https://www.goldmansachs.com/community-transformation/goldman-sachs-gives)
- [Goldman Sachs 2026 proxy](https://www.sec.gov/Archives/edgar/data/886982/000119312526117433/gs-20260319.htm)
- [PWM DAF 2024 secondary Schedule D extract](https://nonprofitnewsfeed.com/daf/goldman-sachs-philanthropy-fund/)
- [Goldman Sachs Gives FY2024 990 extract](https://philanthropy.org/990/report/113813663/the-goldman-sachs-charitable-gift-fund/2024)
- [Goldman Sachs PWM DAF official FAQ](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)

## Validation correction (2026-11-14, independent validation wave 1)
Source: [validation-wave1-report.md](mission-2026-11-14/validation-wave1-report.md), register `data/mission-2026-11-14/validation-register.csv`. Original text above is preserved for traceability; where it conflicts with this note, this note governs.

- **V1-21 upgraded to confirmed:** IRS e-file 202503109349303645 (GS Donor Advised Philanthropy Fund for Wealth Management Inc, EIN 31-1774905), Schedule D Part I: 4,134 DAFs; contributions $5,833,783,136; grants $3,071,806,783; year-end value $12,640,914,117. The 'secondary source' caveat no longer applies.
