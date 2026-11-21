# Business model options (mission brief §10)

**Status:** analysis, 2026-11-20. The six options below map onto the four comparison models in [`models-A-B-C-D-comparison.md`](models-A-B-C-D-comparison.md):
- option 1 is Models A and B;
- options 2–5 are variants of Model C;
- option 6 is Model D or Dc.

Evidence labels follow the [README](../README.md).

## Summary table

| # | Option | Legal status of the company | Holds charitable assets? | Capital intensity [S] | Who buys | Who resists, by incentive | Who prefers to outsource |
|---|---|---|---|---|---|---|---|
| 1 | Full DAF sponsoring organization | §501(c)(3) public charity, an IRS determination, state registrations | Yes, irrevocably | High: sponsor plus platform; S1 base $17.0m, plus distribution | Donors and advisors | Incumbent sponsors; affiliated managers; advisors whose AUM fees would move | — |
| 2 | Technology provider to sponsors (software licence) | For-profit vendor | No | Medium | Mid-size sponsors and community foundations replacing legacy systems | Incumbent vendors (Ren, Foundation Source, Foundant, Blackbaud) | Small CFs, which buy suites |
| 3 | White-label DAF administration platform (software plus operations) | For-profit administrator; contracts with a sponsor-of-record | No (the sponsor does) | Medium-high: needs a production ledger and operations | Wealth firms, banks, trust companies and RIAs wanting a branded DAF; sponsors wanting to outsource | Ren (RCF spine), NPT GivingPoint, TIFIN Give/GiveClear, Foundation Source/Charityvest | Banks and wealth firms (they buy bundles) |
| 4 | AI-native operating infrastructure (decisioning, eligibility, reconciliation, evidence, servicing) | For-profit infrastructure | No | Low-medium: S3 base $5.0m | Sponsors with in-house or mixed stacks that grant data access; administrators | Administrators whose fee share pays for the same work | Small sponsors (they prefer full outsourcing, not components) |
| 5 | Embedded philanthropy API (DAF accounts inside wealth, fintech and payroll platforms) | For-profit API company plus sponsor-of-record partner(s) | No (the partner sponsor does) | Medium | Wealth platforms, custodians, fintechs, employers | Platforms that already chose a sponsor bundle | Platforms (they will not run a charity) |
| 6 | Hybrid: infrastructure plus administration of programs for partner sponsors (D); or plus a captive sponsor (Dc) | For-profit infrastructure; partner charity or affiliated charity | No (D); via the affiliate (Dc) | Medium | Combination of 3 and 4 | As 3 | As 3 |

## Option 1: full DAF sponsoring organization

- **Regulatory:** the full sponsor regime:
  - exclusive legal control and acknowledgment duties (§170(f)(18));
  - taxable distributions and expenditure responsibility (§4966);
  - prohibited benefits (§4967);
  - automatic excess benefit (§4958(c)(2));
  - excess business holdings (§4943(e));
  - Schedule D DAF reporting (§6033(k));
  - state charitable registration (b50-02: most states require it, and CA, NY, PA, MA and WA registries are manual);
  - audit thresholds.

  The penalty taxes on managers are *personal*.
- **Capital:** the company needs operating capital, and must also be credible enough that donors entrust irrevocable gifts. The trust-building cost is unmeasured. Daffy, the closest venture-backed sponsor-plus-technology example, raised $21.9m across seed and Series A [V]. Its $2bn asset figure is company-reported; its FY2024 Form 990 shows $334.19m net assets [V].
- **Governance:** an independent board majority is needed. Any vendor relationship with founders is a related-party transaction (the Charityvest/Foundation Source precedent [V]).
- **Distribution:** the hardest part.
  - Wealth channels are already bundled: about 11 programs on RCF + Ren, plus GiveClear + TIFIN Give at SEI [V].
  - Five failed or pivoted startups moved from consumer to institutional channels (failure pattern P3).
  - The fastest-growing sponsors are channel- or platform-led [I].
- **Operational:** the minimum responsible organization is about 8–10 people, including fractional roles ([organization model §4](../02-business-capabilities/organization-model.md)).
- **Evidence of viability:** the 2021–2026 entrant cohort shows survival, not scale. Of 12 resolved cases, all 12 survive (Wilson interval 75.7–100%); six have unknown status ([gap19-startup-cohort.md](../../mission-2026-11-14/gap19-startup-cohort.md)).

## Option 2: technology provider (software licence)

- **Market reality:**
  - The community-foundation segment is held by Foundant: 361 of 803 CFs, 32.7% of mapped CF DAF assets [V wave 9]. All six dated CF portal switches ended on Foundant [V wave 10].
  - The tail is small. 1,240 sponsors under $50m hold 2.84% of assets, with a median of 24 DAFs each [V].
  - A standalone tail business is unlikely to work [I] (strategic synthesis §0 D).
- **Buyers:** mid-size community foundations and faith or national sponsors leaving Ren iPhi. iPhi lost 6 of 57 sponsors in 2023–Nov 2026, 5 of them CFs [V wave 11].
- **Who resists:** incumbent vendors, through contract terms. Public templates allow batch export but not live integration ([industry report §8](../../DAF-INDUSTRY-REPORT-2026-11.md)).
- **Assessment:** competing on software features alone is the weakest form of Model C. The redesign value comes from operating-model change, and a licence does not deliver that unless the customer also changes its operations.

## Option 3: white-label administration platform

- **Observed structure:**
  - RCF paid Ren $19.23m in FY2024, equal to 98% of its individual-fundholder fees [V].
  - Named Ren receipts across sponsors total a $44.98m floor, 85.8% from three customers [V].
  - The model works economically, but it is concentrated and relationship-bound.
- **Buyers:** banks, trust companies, wealth platforms and RIAs. They buy *sponsor plus technology plus brand* bundles; a technology choice alone is rare.
- **Regulatory:** the administrator acts under contract. It must not hold funds, and custody and payments go through qualified institutions (DD-008). It inherits the partner sponsor's governance risk, which is why partner diligence is first-order (failure-pattern implication 2).
- **Assessment:** this is where the revenue is (Model D), but it is not where an unproven entrant can start without evidence.

## Option 4: AI-native operating infrastructure

- **Repository finding:**
  - This is the cheapest probe (S3), but it is conditional.
  - At $120k/yr, grant-review savings alone justify it only at about 76k–369k grants/yr per customer [S].
  - Fidelity Charitable made 3.0m grants in CY2025; Charityvest made 48,744 in 2025 [V].
  - So the scope must be the *whole operating burden*: decisioning, eligibility, reconciliation, servicing and evidence.
- **Gating constraint:** data and automation access (Q-N04, still open).
- **Assessment:** it is the fastest path to evidence and the most reversible (Model C), but weak on distribution and defensibility.

## Option 5: embedded philanthropy API

- **Observed:**
  - Endaoment publishes partner tiers: Growth setup $0–25k plus $2k–5k/month; Strategic setup $25k–100k plus $5k–15k/month [V].
  - Daffy for Developers has had open APIs since 2023 [V].
  - Altruist launched Endaoment-sponsored DAFs 41 days after Vanguard signed to acquire it [V].
  - Sponsor-of-record APIs therefore already exist and are being embedded.
- **Implication:** an entrant need not *be* the sponsor to embed DAFs. It can orchestrate over a sponsor-of-record API, or become one partner sponsor's operating layer. Embedding *its own* sponsor competes directly with Endaoment and Daffy.
- **Regulatory:** the platform must not hold funds or appear to be the donee. Disclosures and acknowledgments come from the sponsor.

## Option 6: hybrid

Evaluated as Models D and Dc in the [comparison](models-A-B-C-D-comparison.md). **D, a partner sponsor-of-record, dominates Dc, a captive sponsor.** Dc adds related-party governance exposure and irreversibility, and gains nothing in distribution or economics that D lacks.

## Who would buy, resist or outsource, by segment

| Segment | Likely stance | Why (incentive) | Evidence |
|---|---|---|---|
| Large affiliated nationals (Fidelity Charitable, DAFgiving360, Vanguard Charitable) | **Resist or build in-house** | Affiliates earn on assets and administration; in-house platforms | FMR administers Fidelity Charitable (990 shows $0 IT, no employees) [V]; Vanguard chose Give Interactive [vendor claim] |
| NPT, AEF and other independents on Ren | **Possible buyers of components** (eligibility, evidence, reconciliation) if contracts allow | Independents bear their own costs | NPT GivingPoint is Ren-hosted; AEF moved fully onto Ren in Apr 2026 [V] |
| RCF and other fee-share structures | **Resist** | 98% fee share to the administrator [V] | |
| Community foundations (top 100) | **Mixed. Buy suites, outsource components rarely** | Cost gap (admin fees 1.7–4.7× nationals [V]) creates pressure, but Foundant incumbency is strong | All six dated switches went to Foundant [V] |
| Tail CFs and single-issue sponsors | **Outsource entirely** (transfer DAFs to a larger sponsor, or use a white label) | Median 24 DAFs; they cannot staff the SoD floor [V/I] | |
| Wealth firms and RIAs | **Buy bundles; value advisor control** | AUM fees on DAF assets (55 bps OneGive; up to 1% caps; 0–2% observed) [V] | SEI/TIFIN/GiveClear; RCF + Ren programs |
| Banks and trust companies | **Buy white label** | Brand, compliance comfort | BofA CGF on Ren portal; BNY Mellon CGF ended its DAF program in Dec 2024 [V] |
| Nonprofits | **Benefit, but they are not payers of DAF administration** | Rails and remittance costs fall on them; weak leverage (structural) | Strategic synthesis §0 G4 |
| Fintechs and payroll platforms | **Buy embedded APIs** | Feature completeness | Altruist/Endaoment [V] |
