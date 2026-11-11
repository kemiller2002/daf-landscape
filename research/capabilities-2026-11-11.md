# DAF platform and sponsor capabilities, initial public-source matrix

**Reviewed:** November 11, 2026. **Legend:** **Documented** means described in a cited primary source; **Claimed** means a vendor markets it without hands-on verification; **Unassessed** does not mean absent.

## Segment before comparing

| Entity | Role in ecosystem | Publicly described offering | Sources |
|---|---|---|---|
| **Ren** | Technology provider + administrator | Institutional DAF and planned-giving technology, branded portals, contribution/grant services, charity screening, advisor-centric investing and complex contributions | [Ren FAQs](https://www.reninc.com/faqs/), [AEF transition](https://engage.aefonline.org/dc-sunset/) |
| **TIFIN Give** | White-label technology for wealth enterprises | Digital institutional DAF platform, multi-custody, investment customization, advisor relationships, marketed conversational AI and community giving | [TIFIN product](https://tifin.com/product/give/) |
| **Chariot** | API, grant initiation and payment/connectivity infrastructure | DAFpay donor-to-nonprofit experience; Connect widget; DAF-provider verification and grant decision APIs; event/webhook and transaction tracking | [DAFpay overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/overview), [Donor Accounts](https://docs.givechariot.com/guides/dafpay/donor-accounts/overview), [transactions](https://docs.givechariot.com/guides/dafpay/integrating-dafpay/transactions) |
| **Daffy** | Digital-first DAF offering and developer APIs | Online DAF, documented balance/contribution/donation REST APIs and developer/agent integrations | [docs](https://docs.daffy.org/), [donations](https://docs.daffy.org/ref/donations), [AI agents](https://docs.daffy.org/agents/mcp) |
| **Fidelity Charitable** | Large DAF sponsor | Giving Account, online/mobile grant recommendations, investments, complex gifts, qualified advisor access and programs | [Giving Account guide](https://www.fidelitycharitable.org/giving-account-guide.html), [advisor](https://www.fidelitycharitable.org/giving-account/working-with-advisor.html) |
| **National Philanthropic Trust** | Independent DAF sponsor | GivingPoint portal for grants, contributions, allocations, account and legacy-management; complex gifts, advisor support | [GivingPoint](https://www.nptrust.org/nptgivingpoint/), [DAFs](https://www.nptrust.org/donor-advised-funds/) |
| **Schwab Charitable** | DAF sponsor | Donor and advisor program with account, investments, grant recommendations; specific current digital/API features not evaluated here | [website](https://www.schwabcharitable.org/) |
| **American Endowment Foundation** | DAF sponsor relying on technology vendor | DAF accounts, donor/advisor portal and administration via Ren technology | [transition notice](https://engage.aefonline.org/dc-sunset/), [pilot FAQ](https://engage.aefonline.org/pilot-program-support-resources/) |
| **Greater Horizons** | Independent DAF sponsor | Giving portal for grants/history/statements, advisor-managed investments and pooled allocations, complex contributions and philanthropic advising | [advisor FAQ](https://www.greaterhorizons.org/professional-advisors/charitable-giving-solutions/daf-financial-advisor-managed-account-faqs/) |

## Focused capability comparison

| Dimension | Ren | TIFIN Give | Chariot |
|---|---|---|---|
| Branded DAF portal | **Documented** (AEF) | **Claimed** | **Unassessed** as full institutional portal |
| Grant recommendations | **Documented** | **Claimed** donor grant activity | **Documented** initiation and provider-facing grant requests |
| Sponsor-side grant vetting / decision | **Documented** as service | **Unassessed** operational authority | **Provider controls decision**, via integration |
| Custody / investment options | **Documented** advisor-centric solutions | **Claimed** multi-custody, models, alternatives | **Unassessed** as core investment service |
| Accounting / ledger functionality | **Documented** administration/service claims; details not verified | **Unassessed** | **Unassessed** as DAF general ledger |
| External APIs and webhooks | **Unassessed** publicly in this review | **Unassessed** publicly in this review | **Documented** APIs, lifecycle and webhooks |
| Payment orchestration | **Documented** Ren payment product marketing | **Unassessed** exact rails | **Documented** DAFpay transaction/processing integrations |
| Publicly marketed conversational AI | **Unassessed** | **Claimed** | **Unassessed** |
| SOC 2 assurance claim | **Type I**, public 2026 | **Unspecified SOC 2**, public 2024 | **Type II**, public trust material |
| Actual independent report inspected | **No** | **No** | **No** |

**Caution:** Sponsor-side authority to approve or disburse grants does not transfer automatically to an API integrator. Marketing says little about measured uptime, error rates, processing speed, cost per grant or total implementation complexity.

## Selection criteria by buyer

### Sponsoring organization / new DAF program
- Legal sponsor structure, grant decision independence, charitable asset policies, accepted assets.
- Accounting and investment subledgers, custody reconciliation, end-to-end controls and auditability.
- Portal experience, donor/advisor permissions, data portability and migration of grant history.
- Implementation lead time, SLAs, incident response, reporting and regulatory support.
- Applicable SOC 2 and SOC 1 assurance, subcontractor exposure, CUECs and financial correctness.

### Wealth manager / institution
- Custodian neutrality versus custody retention, advisor-managed investments, alternatives, house-brand experience.
- Advisor workflows and SSO, integration to investment accounts and CRM, allocation and reporting latency.
- Fees and revenue split, implementation/migration costs, sponsor relationships and client portability.

### Nonprofit / fundraising platform
- Breadth of supported DAF providers, donor experience, reconciliation, donor recognition.
- Grant initiation versus actual payment receipts, webhooks, status transparency, returns/cancellations.
- Security of donor sign-in, incident/availability performance, integration maintenance and pricing.

## What remains unverified

Actual API accessibility for Ren/TIFIN, independent demonstrations, tenant isolation, commercial prices, operational automation rates, program-wide security coverage and total-cost-of-ownership comparison. Investigate without implying a feature is missing just because we did not find public documentation.

For evidence grades and caveats, see [methodology](../docs/methodology.md).
