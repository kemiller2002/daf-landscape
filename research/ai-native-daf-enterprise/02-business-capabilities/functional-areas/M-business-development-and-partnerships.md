# M. Business development and partnerships

**Capabilities:** C1.3 (primary), C4.3 (revenue share), C5.5 (partner risk), with the commercializable capabilities C3.1, C3.3, C3.4+C4.2, C4.5, C5.1, C2.1+C2.2, C6.1, C1.3 · **Outcomes:** O-14, O-11 · **Accountable:** Head of Partnerships · **Strategy and model selection:** [`../../10-market-and-business-model/`](../../10-market-and-business-model/). This file covers the *operating model* of the business development function, not which business model wins.

## 1. Existing industry operating model

DAF distribution is channel-led, and so is the infrastructure market.

**Distribution**
- The fastest-growing sponsors are channel- or platform-led [I]. Reported advertising is tiny at nationals: $21.7m at affiliated-commercial sponsors, of which Schwab is $20.3m. Community foundations spend about 18 bps of DAF contributions, and advertising intensity is not positively ranked with account growth (ρ −0.25, n=55) ([industry report §11.25](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`direction-sponsor-marketing-spend.md`](../../../mission-2026-11-14/direction-sponsor-marketing-spend.md)).
- **Institutional distribution sits on a few sponsor and infrastructure pairs:**
  - RCF/Ren: about 11 wealth-firm programs.
  - GiveClear/TIFIN Give: SEI, AssetMark, Zions Bank and others.
  - Charityvest/Foundation Source: TIAA, Temple, OneGive.
  - NPT private-label GivingPoint: a 13-site Ren white-label book.

  Sources: industry report §2; [`ren-distribution-network-institutional-program-comparison-2026-11-12.md`](../../../ren-distribution-network-institutional-program-comparison-2026-11-12.md).

**Sponsor-of-record APIs for developers**
- These exist: Endaoment, and Daffy for Developers. Chariot provides disbursement and DAFpay (report §8).
- Chariot's default nonprofit DAFpay fee is 2.9% absent other agreements (research README, revenue retention section).

**Contracts**
- Vendor contracts renew annually by default with 60-day notice (public Ren MSA template).
- Executed sponsor–vendor contracts remain unseen (Q-N04) ([`ren-contract-durability-concentration-2026-11-11.md`](../../../ren-contract-durability-concentration-2026-11-11.md)).

**Consolidation**
- Private equity rolls up quickly. GTCR named a new Foundation Source CEO six days after closing, followed by four acquisitions in about 17 months (report §5; [`private-equity-daf-ecosystem-map.md`](../../../mission-2026-11-14/private-equity-daf-ecosystem-map.md)).
- Customer effects are unobserved.

**Repository hypotheses about buyers**
- The repository's commercial agenda lists buyer segments (mid-sized sponsors and community foundations; wealth managers, RIAs and BDs; DAF technology vendors; banks and trust companies; PE and VC; nonprofits; education bodies) as **hypotheses, not validated demand** ([`commercial-opportunity/2026-11-20-research-agenda.md`](../../../commercial-opportunity/2026-11-20-research-agenda.md)).

## 2. Actual required business outcomes

- Distribution that brings appropriate donors through trusted intermediaries at a sustainable acquisition cost (O-14).
- Partner revenue (white-label, API licensing, infrastructure fees) priced to cover cost to serve, with transparent revenue sharing (O-14, O-05).
- Partners integrated without weakening sponsor control, compliance or security (O-03, O-11, O-17).
- Partner concentration kept within risk appetite (O-11). This is a lesson from RCF's 98% fee pass-through to Ren and Ren's 85.8% receipts from three customers (strategic synthesis §0 C).

## 3. Legal and risk constraints

| Constraint | Implication |
|---|---|
| Charitable solicitation and commercial co-venturer / professional fundraiser registration in some states when partners market a sponsor program | GC review per partner marketing arrangement; state registration tracking (C4.4) |
| California platform law reaches DAF technology vendors and white-label portals (Type A/E under 11 CCR 314) ([industry report §11.10](../../../DAF-INDUSTRY-REPORT-2026-11.md)) | Infrastructure offerings must be assessed for charitable fundraising platform registration |
| Revenue share with for-profit partners must be reasonable and not confer private benefit | Board-approved fee policy; disclosed |
| Payment facilitation for third parties (if infrastructure moves funds for other sponsors) | Possible money-transmission implications; rely on bank or licensed partner rails (DD-008; see the regulatory map) |
| Data rights and exit terms | Standard data-portability and API clauses in every contract (closing the Q-N04 gap from our side) |
| Licensing of any Echelon component used in a commercial offering | PolyForm Noncommercial may not permit commercial infrastructure use (DD-014) |

## 4. Proposed AI-native operating model

1. **Productized partnerships, not bespoke projects.** Each offering has a published API contract, sandbox, conformance test suite, price book and standard contract with data-portability and exit terms. Business development sells configurations of the same platform (DD-016: tenant = sponsor or program).
2. **Partner types and motions:**

| Partner type | Motion | What they get |
|---|---|---|
| Wealth firms, RIAs, BDs, banks (distribution) | Program launch (branded program under our sponsor, Model B) or infrastructure for their own sponsor (Model C) | Embedded DAF, advisor tools, data feeds |
| Existing sponsors (community foundations, nationals, faith, university) | Infrastructure subscription or capability APIs (eligibility, decisioning, disbursement and reconciliation, evidence) | Lower cost to serve; continuous compliance evidence |
| Fintech and embedded-philanthropy platforms | API licensing with our sponsor as sponsor of record | Account opening, grants and contributions by API |
| Data providers (Candid, ratings) | Licensed inputs | Respect license limits (for example Charity Navigator bars use of ratings "in any other calculation", report §11.25) |
| Rails and custodians | Supplier partnerships with redundancy | Integration and volume |

3. **AI in business development is preparation, not persuasion.** Agents assemble partner due-diligence packs (public filings, SOC reports, state registrations) and draft integration plans from partner API conformance results. There is no automated outreach without approval: the repository's guardrail on unsolicited outreach applies.
4. **Partner health is telemetry.** API usage, error rates, exception rates by partner, revenue, cost to serve and concentration share are monitored continuously, and renewal risk is visible early.
5. **Concentration limits.** No single partner should exceed a board-set share of revenue or assets without board approval and a mitigation plan.

## 5. Eliminated activities

- ACT-001: mass-market brand advertising, reduced to channel-embedded distribution.
- ACT-002: purchased wealth-data lead scoring, eliminated.
- ACT-004: wholesaling, reduced.
- Bespoke integration projects per partner, replaced by conformance-tested standard contracts.
- Manual partner revenue-share calculation, now done by the fee engine.

## 6. New workflows

- **WF-M1 Partner qualification.** Inbound interest leads to a due-diligence pack (agent-drafted from public sources), then qualification against the board-approved partner policy (fit, risk, concentration) as an H decision by the Head of Partnerships, then the term sheet.
- **WF-M2 Partner launch.** Contract (GC) → tenant or program configuration as policy objects (fees, menu, branding, data scopes) → sandbox → conformance suite pass → Change Board production approval → launch telemetry watch for 90 days.
- **WF-M3 Revenue share.** Period close → `FeeAccrued` by partner → revenue-share computation (schedule version) → statement → payment via the payment gate (a vendor payment, not a grant).
- **WF-M4 Partner offboarding and exit.** Notice → data export in open formats (the open grant record and full event history) → donor communications → account transfers if a program moves sponsors (WF-H6 at scale) → evidence of completion. This is designed in from the start, unlike the observed history loss in migrations.
- **WF-M5 Capability API customer onboarding** (eligibility or decisioning API for another sponsor; Model C). The customer's policy is translated into decision tables (with the policy engineer), back-tested on the customer's historical grants, and the customer's officers approve. They keep accountability for decisions under their own policy.

## 7. Required data

Partner registry (contracts, fee and revenue-share schedules, data scopes, SLAs); pipeline (qualification decisions); partner telemetry; concentration metrics; cost-to-serve by partner (from C6.2 and 09-); state registration status per partner arrangement.

## 8. Required APIs

The externally exposed families and their product packaging (see the [API catalog](../../04-enterprise-apis/)): `/v1/accounts`, `/v1/recommendations`, `/v1/grants`, `/v1/recipients` and `/v1/eligibility`, `/v1/payments`, `/v1/reconciliation`, `/v1/evidence`, `/v1/policies` (customer policy hosting), `/v1/reports`, `/v1/events` (webhooks). Internal: `/v1/fees` (revenue share), `/v1/parties` (partner orgs).

## 9. Event triggers

`AccountOpened` and `ContributionSettled` (partner attribution), `FeeAccrued` (revenue share), `PolicyPublished` (partner configuration), `AgentRunCompleted` (due-diligence packs), `CustodianUnavailable` and rail outages (partner notifications), partner telemetry SLO breaches (`ExceptionCaseOpened`, type `partner.health`).

## 10. AI agent responsibilities

- **Partner due-diligence assistant** (Category 2): compiles public evidence with citations; flags governance or related-party concerns (feeds the related-party detector).
- **Integration assistant** (Category 2): explains conformance failures to partner engineers in the sandbox.
- **Proposal drafter** (Category 2): drafts proposals from the price book. Human-approved and never sent autonomously.

## 11. Deterministic automation responsibilities

Price-book application; revenue-share computation; conformance test execution; partner access scopes; concentration metric computation and threshold alerts; contract renewal calendar.

## 12. Human oversight requirements

Partner selection and termination (DEC-059); pricing and revenue-share schedules (board, DEC-066 for donor fees; CEO within board-approved bands for partner pricing); concentration exceptions (board); any arrangement touching charitable solicitation registration (GC).

## 13. Exception management

Case types: `partner.health` (SLO breach), `partner.concentration` (threshold), `partner.contract_dispute`, `partner.data_request_out_of_scope` (denied, then reviewed).

## 14. Security and compliance controls

Per-partner credentials and scopes; partner security attestations and SOC report review (SOC report analyzer); standard data-processing terms; no partner access to other tenants' data (cell isolation tests); marketing materials reviewed by GC for tax claims (no "DAF is tax-superior" claims, per strategic synthesis §0 D).

## 15. Estimated staffing implications

**Drivers:** the number of institutional partners and capability-API customers, the integration complexity mix, and renewal cadence.

**Direction:** a small partnerships team (relationship managers per N institutions plus solutions engineers), not a mass-market sales force. FTE in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Sandbox-to-production time for a standard partner | ≤ 8 weeks |
| Share of partners on standard contract terms (with data portability) | 100% |
| Largest single partner share of revenue | Board-set ceiling (illustrative 25%) |
| Partner gross margin after cost to serve | Positive at partner level within 12 months (validate) |

Customer acquisition cost is unknown and unbenchmarked in the repository; it must be measured in the pilots (gap).

## 17. Implementation dependencies

The commercial model choice (10-); API contracts and conformance suite (04-); multi-tenant cells (07-); the fee engine; legal templates; the state registration analysis for platform offerings; validated demand from interviews under the commercial agenda (not yet done).

## 18. Measurable success criteria

- At least 3 design-partner institutions in Phase 4 with signed standard contracts (see [`../../12-implementation-roadmap/`](../../12-implementation-roadmap/)).
- Zero partner launches without conformance pass.
- Concentration within the board ceiling.
- An exit-readiness export demonstrated for every partner annually.
- Measured CAC and cost to serve per partner reported quarterly.
