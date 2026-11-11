# Public SOC 2 assurance assessment: DAF ecosystem

**Reviewed:** 2026-11-11. **Scope:** official, publicly accessible material concerning Ren, Chariot, TIFIN Give, AEF, Fidelity Charitable, National Philanthropic Trust, Schwab Charitable, Greater Horizons and Daffy.

**Bottom line:** We found specific SOC 2 claims for Ren, Chariot, and TIFIN Give. We have **not reviewed any independent SOC 2 report**, and therefore have **not established compliance** for any company. Lack of an accessible public report is not evidence of failed controls.

## Public evidence summary

| Entity | Functional category | Exact publicly documented assurance claim | Status | Critical missing evidence |
|---|---|---|---|---|
| Ren (`reninc.com`) | Platform, administration, services | Apr 8, 2026 AEF-hosted Ren announcement: SOC 2 **Type I** | Vendor/sponsor-published Type I claim | Current report, audited scope, period, opinion, exceptions; ask whether Type II now exists |
| Chariot | DAFpay, grants/connectivity, payment infrastructure | Chariot security page: SOC 2 **Type II** | Vendor-published Type II claim | Report, observation period, systems in scope, opinion, exceptions, third-party dependencies |
| TIFIN Give | White-label institutional DAF technology | TIFIN 2024 announcement: **SOC-2 security compliance** | Vendor-published type unspecified | Report type, period, scope, auditor, opinion, current coverage |
| American Endowment Foundation | DAF sponsoring charity | No AEF-specific SOC 2 report established; AEF uses Ren's DAF platform | Technology dependency; own assurance unverified | Sponsor controls and how Ren's scoped report applies |
| Fidelity Charitable | DAF sponsoring charity | No Fidelity Charitable system-specific report established | Not publicly verified in scoped review | Report existence, scope and entity identification; do not transpose coverage from Fidelity affiliates |
| National Philanthropic Trust | DAF sponsoring charity | No NPT GivingPoint-specific report established | Not publicly verified | Vendor/system map and report availability |
| Schwab Charitable | DAF sponsoring charity | No sponsor-system-specific report established | Not publicly verified | Sponsor versus Schwab affiliate control boundaries |
| Greater Horizons | DAF sponsoring charity | No report established | Not publicly verified | Portal operator, custody feeds, sponsor control coverage |
| Daffy | Digital-first DAF provider | No report established in scoped search | Not publicly verified | Current independent assurance, scope, API controls |

### Source evidence and limits

1. **Ren:** [AEF April 8, 2026 announcement](https://www.aefonline.org/thought-leadership/ren-brings-american-endowment-foundation-fully-onto-its-technology-platform-powering-philanthropy-at-scale/) says Ren holds a “SOC 2 Type 1 certification” (publisher's wording). SOC 2 is an attestation, not literally a certification. Previous Ren announcements [also used Type I](https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/). **No valid Ren (`reninc.com`) Type II statement was substantiated in this review.**
2. **Chariot:** [official security statement](https://help.givechariot.com/onboarding/trust-and-safety/security) states “SOC 2, Type 2 Compliant” and that documents are available through its trust center on request. This is a vendor claim, not a report inspection.
3. **TIFIN Give:** [TIFIN announcement](https://tifin.com/news/tifin-give-expands-its-reach-as-a-leading-technology-powered-philanthropy-platform-for-wealth-enterprises-2/) describes multi-custodial DAF software and “SOC-2 security compliance” without type or report dates. The announcement is historical and cannot prove currency in 2026.
4. **AEF:** [AEF's transition notice](https://engage.aefonline.org/dc-sunset/) identifies Ren as the new DAF technology platform, but cannot establish how an audit applies to AEF's own people, processes, custody or vendor dependencies.
5. **Fidelity Charitable:** [Giving Account guide](https://www.fidelitycharitable.org/giving-account-guide.html) describes operating features, **not** SOC 2 attestation scope. Affiliate or parent financial-services reports should not be imputed to this nonprofit.
6. **NPT:** [GivingPoint platform](https://www.nptrust.org/nptgivingpoint/) documents donor-facing functions but no SOC 2 statement was verified here.
7. **Schwab Charitable:** Sponsor offering was identified, but a current applicable report and audited systems were not publicly established in this research.
8. **Greater Horizons:** [advisor/portal FAQ](https://www.greaterhorizons.org/professional-advisors/charitable-giving-solutions/daf-financial-advisor-managed-account-faqs/) documents technology and reconciliation but not a SOC 2 report.
9. **Daffy:** [public developer documentation](https://docs.daffy.org/) establishes API capabilities but not independent security attestation.

### Critical correction: two unrelated companies named Ren

Search results for [`tryren.com` SOC 2 Type II](https://tryren.com/blog/ren-achieves-soc-2-type-ii-compliance) concern an AI workplace coaching provider and are **not** applicable to philanthropic DAF administrator **`reninc.com`**. Incorrect name matching could create a materially false due-diligence conclusion.

## Deep dives

### Ren: platform and administration

**Documented service model.** Ren publicly describes supporting institutional donors, sponsoring programs, charitable trusts and advisor-centric DAFs. Its [FAQs](https://www.reninc.com/faqs/) describe advisor management, grant processing, multi-successor arrangements, complex contributions and administrative processes. AEF [confirmed the transition](https://engage.aefonline.org/dc-sunset/) from DonorCentral to a Ren-powered portal, including a past-history limitation visible to donors.

**Assurance.** The best 2026 primary public claim located is Type I. A Type II claim for another entity called Ren is inapplicable. Ask for: the legal reporting entity, in-scope DAF services and hosted platform(s), auditor opinion and periods, SOC 1 coverage for financial processes, and whether AEF is a user entity with complementary control obligations.

**Unanswered:** Current Type II status; distinct controls for fund accounting, grant approvals, identity, hosted portals, custody imports, subservice organizations, and ACH/payments.

### Chariot: connectivity and payments

**Documented service model.** [DAFpay overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/overview) covers donation initiation, Connect integration and associated API records. [Donor Accounts](https://docs.givechariot.com/guides/dafpay/donor-accounts/overview) describes verification and grant request decisions controlled by the DAF provider. [Transaction management](https://docs.givechariot.com/guides/dafpay/integrating-dafpay/transactions) makes clear that a grant can be *initiated* before a nonprofit has received funds.

**Assurance.** Type II claim is explicit, but applicable report and auditor findings remain unreviewed. Determine whether DAFpay, Donor Accounts, payment services, data processors, and banking partners are included in the report; review penetration testing and transaction controls.

**Unanswered:** End-to-end funds-flow ownership, provider responsibilities, cancellations, exception rates, reconciliation and nonincluded subservices. Do not call Chariot a full DAF accounting system without proof.

### TIFIN Give: white-label institutional stack

**Documented service model.** [Current product page](https://tifin.com/product/give/) advertises white-label digital experiences, multi-custody, advisor-managed portfolios, alternative investments, community campaigns and conversational AI. This confirms what the vendor *markets*, not an evaluated deployment. [2024 announcement](https://tifin.com/news/tifin-give-expands-its-reach-as-a-leading-technology-powered-philanthropy-platform-for-wealth-enterprises-2/) also mentions institutional deployments.

**Assurance.** The source states SOC 2 compliance without naming type or system; its age heightens the need for a current report.

**Unanswered:** Which legal entity and services are in scope, current Type II report availability, who serves as sponsor, fund accounting design, operating controls, production AI limitations, API access, integration cost, reconciliation and payment lifecycle.

## Preliminary comparative conclusion

It is **not defensible** to rank these as “Ren vs. TIFIN vs. Chariot” on one numeric axis. Ren publicly combines administration and platform services; TIFIN Give markets institutional platform capabilities; Chariot documents transaction connectivity. Their overlap depends on use case. No demonstrated relationship between the extent of their product features and their assurance maturity has been established.

For buyer selection, require separate security and capability evaluations. See [capability assessment](capabilities-2026-11-11.md) and [next steps](next-steps.md).
