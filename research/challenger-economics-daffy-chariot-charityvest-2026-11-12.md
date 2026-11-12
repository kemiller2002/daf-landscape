# DAF Challenger Economics: Daffy vs Chariot vs Charityvest
Date: 2026-11-12
Status: sourced preliminary analysis; not audited operating-cost comparison.

## Executive finding
These three challengers occupy distinct layers. Daffy markets flat-fee donor DAF membership; Chariot monetizes DAF initiation, disbursement and nonprofit revenue operations; Charityvest sponsors DAFs with invested-account asset fees while Foundation Source provides software and services. The key hypothesis is cost shifting, not proven cost elimination.

## Daffy
- Membership (Aug 6 2026): free qualifying under-$100 account; $3/month Contributor, $5/month Family, $20/month Benefactor, $40/month Philanthropist. Tiers depend on annualized contributions and features, not solely account balance.
- No separate asset management fee claimed; underlying fund expense ratios apply; 2.9% surcharge on card contributions, waived for first card contribution up to $1,000.
- Illustrative $480/year at $40/month for a large account, **not** total revenue/cost of sponsor or related entities.
- IRS Form 990 Daffy Charitable Fund EIN 86-3177440: FY2024 net assets $334.19M; contributions $194.04M; expenses $40.20M. The latter includes charitable grants and cannot be interpreted as operating expense.
- Research: examine full Part IX and Schedule D for grants, service fees, vendor relationships, account counts, custody, noncash assets, operational costs, cross-subsidies.
Sources:
https://help.daffy.org/en/articles/6323771-what-are-daffy-s-membership-fees
https://help.daffy.org/en/articles/11730947-are-there-other-fees-besides-my-monthly-membership
https://projects.propublica.org/nonprofits/organizations/863177440

## Chariot
- Public pricing: Core 1% per donation for gift-processing product; Growth $4,740/year with 250 donations included; standalone DAFpay components 2.9% initiation fee on Growth; Enterprise custom. These are different product/contract fee contexts, do not collapse them into one price.
- DAFpay nonprofit terms default 2.9% fee rounded to nearest dollar absent other fundraising-platform agreement; subscriptions may remove fee on covered volume. On $10,000 gift: $290 illustrative fee at 2.9%.
- Chariot states sponsor/DAF provider, not Chariot, determines grant approval and ultimate receipt timing. Thus checkout convenience does not prove faster underlying approvals.
- DAFpay Network is a separate 501(c)(3) payment facilitator for unclaimed nonprofit accounts. Its published policy includes a check surcharge (lesser of $25 or 10%) and reassignment procedures if nonprofit cannot claim funds. Analyze legal/control implications carefully.
- Disbursements documentation says nonprofits not charged for Chariot Disbursements, while grantmakers pay transaction fees; distinguish from DAFpay initiation product.
- Research: quantify conversion uplift, net incremental grants, fee incidence, sponsor API dependencies, exception rates, settlement times, identity and CRM reconciliation, network effects.
Sources:
https://www.givechariot.com/chariot-pricing
https://www.givechariot.com/legal-nonprofit
https://help.givechariot.com/dafpay/dafpay-network
https://docs.givechariot.com/guides/disbursements/faq

## Charityvest
- Basic cash account: no admin fee; invested account: 0.60% first $500k, 0.30% next $500k, 0.20% $1M-$2.5M, 0.15% $2.5M-$5M, 0.10% $5M-$10M; invested advisor program minimum $100/year, subject to program terms.
- Advisor firms may assess their own advisory fees. Advisor partner guide says no firm setup fees in standard program, potential white-label minimums.
- Foundation Source acquired Vennfi in October 2024. Charityvest Inc remains independently governed 501(c)(3) sponsor; Foundation Source provides software/admin for a fee and has no legal claim on Charityvest DAF assets.
- Company-reported 2025: $265M+ contributions, $119.2M grants (48,744 grants), $224.6M assets. Approx $2,445 per grant is grant amount, **not** processing cost. 118% payout claim depends on denominator/method; independently reconstruct.
- FY2024 Form 990 (EIN 81-2771871) net assets $103.17M; expenses $52.60M include grants, not a measure of admin cost.
- Research: identify sponsor-vendor payments on 990, invested/cash mix, advisory fees, partner economics, post-acquisition service changes, distribution costs.
Sources:
https://guide.charityvest.org/for-donors/fees-and-expenses
https://advisorguide.charityvest.org/getting-started/how-client-fees-work
https://advisorpartnerguide.charityvest.org/fees
https://guide.charityvest.org/about-our-venture/charityvest-%2B-vennfi
https://news.charityvest.org/p/charityvest-just-got-stronger-a-key-partnership-announcement
https://foundationsource.com/newsroom/press-releases/charityvest-reports-record-2025-charitable-giving-more-than-doubling-contributions-and-grants/
https://projects.propublica.org/nonprofits/organizations/812771871

## Clarity / EDF interpretation
Claim: startups remove DAF admin costs. Status: unsupported. Alternative: they relocate cost to subscriptions, sponsor asset fees, service-provider fees, fundraising fees, investment expense ratios, or subsidies. Need total-system cost including sponsor, vendor, advisor, custodian, nonprofit and donor. Avoid confusing donor-visible price with unit economics.

## Next actions
- [ ] Extract 2024/2025 990 Part IX functional expenses, Schedule D and related-party/vendor payments for Daffy and Charityvest; reconcile grant amounts vs operating expense.
- [ ] Locate service contracts, Form 990 vendor disclosures and audited financials where available.
- [ ] Model per-account and per-grant economics by balance, activity, account type, donation size and payment method.
- [ ] Trace Chariot's two separate rails: DAFpay initiation vs disbursement, including DAFpay Network.
- [ ] Map advisor and nonprofit relationship retention and donor data portability.
- [ ] Evaluate credible evidence of time saved, higher conversion, fewer exceptions, and actual grant processing improvement.
- [ ] Compare failures, acquisitions and pivots among early-stage DAF entrants.
