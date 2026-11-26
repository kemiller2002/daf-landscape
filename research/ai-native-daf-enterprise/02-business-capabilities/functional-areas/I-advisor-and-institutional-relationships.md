# I. Wealth advisor and institutional relationships

**Capabilities:** C1.3 Advisor and institution integration (primary), C1.2, C2.4, C4.3, C1.4 · **Outcomes:** O-09, O-14, O-04, O-02 · **Accountable:** Head of Partnerships · **Governing decision:** DD-010 (preserve the advisor relationship)

## 1. Existing industry operating model

Distribution of traditional invested DAFs runs largely through wealth channels.

**Channel evidence**
- **The RCF–Ren spine.** Renaissance Charitable Foundation sponsors branded programs for Edward Jones, Ameriprise, RBC, LPL and Commonwealth, Northwestern Mutual, UBS (one of four sponsors there), SEI, Fisher and MDRT. Ren supplies the "DFX powered by Ren" portals, and RCF paid Ren $19.23m in FY2024: 98% of individual-fundholder admin-fee revenue ([industry report §2.2](../../../DAF-INDUSTRY-REPORT-2026-11.md)).
- **Affiliate-integrated nationals** (Fidelity Charitable, DAFgiving360, Vanguard Charitable) combine brand, affiliated funds and administration (§2.1).
- **Other bank and wealth programs.** Morgan Stanley GIFT, the Bank of America Charitable Gift Fund (BofA N.A. sole trustee, administered by BofA Private Bank) and Goldman's two programs ([`goldman-sachs-two-daf-programs-2026-11-11.md`](../../../goldman-sachs-two-daf-programs-2026-11-11.md); report §11.27 wealth channels).
- **Multi-sponsor and new wealth programs.** SEI runs two DAFs (RCF/Ren and GiveClear/TIFIN Give). TIAA's 2026 program is sponsored by Charityvest, powered by Foundation Source and advised by a TIAA affiliate ([`charityvest-foundation-source-tiaa-financial-bridge-2026-11-11.md`](../../../charityvest-foundation-source-tiaa-financial-bridge-2026-11-11.md)).
- **Edward Jones' private DAF** has no public sponsor, administrator or vendor ([`gap19-edward-jones-wealth-channels.md`](../../../mission-2026-11-14/gap19-edward-jones-wealth-channels.md)).

**Economics**
- Adviser fees on DAF assets are the largest cost layer in adviser-led programs. Only MS GIFT, DAFgiving360 and TIFIN Give publish a 1.00% cap; Fidelity CIAP, NPT, AEF and RCF publish none, and observed RIA brochures charge 0–2.00% ([industry report §3](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`queue-adviser-fees-pools-npact.md`](../../../mission-2026-11-14/queue-adviser-fees-pools-npact.md)).
- Disclosed conflicts exist, for example OneGive's waivable 55 bps adviser fee and a fund's indirect equity interest in the technology vendor ([`oneascent-onegive-charityvest-disclosed-incentives-2026-11-11.md`](../../../oneascent-onegive-charityvest-disclosed-incentives-2026-11-11.md)).

**Integration practice**
- No open multi-sponsor grant-request standard exists. DAF Direct is closed, with three sponsors.
- Six of the top 20 sponsors (about $84bn) contractually limit automated or third-party access (strategic synthesis §0 D, G1).
- Advisor access is typically by limited power of attorney or letter of authorization forms, and advisor-managed accounts are reviewed after the fact [I] ([`pave-daf-adviser-managed-sponsor-access-2026-11-11.md`](../../../pave-daf-adviser-managed-sponsor-access-2026-11-11.md)).

**Advisor-retention hypothesis.** The repository's relationship-continuity study frames, but has not tested, the hypothesis that integrated philanthropic planning raises household retention ([`daf-wealth-management-relationship-continuity-study-2026-11-11.md`](../../../daf-wealth-management-relationship-continuity-study-2026-11-11.md)). Its counter-risks are stated in that study:
- contributions reduce personally owned AUM;
- some clients want philanthropic independence from their advisor.

## 2. Actual required business outcomes

- Advisors can open, view, service and (where the sponsor permits) manage DAF investments within mandates, without re-keying data and without weakening sponsor control (O-02, O-03, O-04).
- Institutions (broker-dealers, RIAs, custodians, wealth platforms, family offices, banks) can embed DAF capabilities in their own experiences (O-14).
- Fees paid to advisors are transparent, capped by policy and correctly computed (O-04, O-05).
- Donors keep control of which advisor sees what, and can revoke (O-17).

## 3. Legal and risk constraints

| Constraint | Source | Design response |
|---|---|---|
| The sponsor must retain exclusive legal control | §4966(d)(2) | Advisor instructions are *requests*. The mandate checker or the sponsor converts them into instructions (DD-003) |
| **Pending:** the 2023 proposed §4966 regulations would treat a donor's personal investment adviser who manages DAF assets as a donor-advisor | REG-142338-07 (still proposed, docket of 249 submissions; industry report §6; [`b39n1-01-docket-2026-submissions.md`](../../../mission-2026-11-14/b39n1-01-docket-2026-submissions.md)) | Model advisor status as policy data, not code. A final rule would make fee payments to such advisors potentially subject to §4958/§4967 analysis, so the fee engine must be able to re-classify by policy version without redeployment. **Current law vs proposed is labeled** |
| Advisor fees as potential excess or prohibited benefit | §4958(c)(2), §4967 | Fee caps and reasonableness tests in policy; fees paid only for investment management of charitable assets; disclosure |
| Advisor's own regulation | Investment Advisers Act fiduciary duty; Reg BI for broker-dealers recommending DAFs | The sponsor provides disclosures and data for the advisor's suitability process; it does not perform it |
| Data sharing with institutions | Privacy law; program agreement; GLBA at the institution's side | Donor-consented, scoped data-sharing grants; per-institution data contracts |
| Sponsor terms barring credential sharing (incumbents) | Strategic synthesis §0 D | API-only access with delegated tokens; no screen scraping (DD-017) |

## 4. Proposed AI-native operating model

**The advisor is a first-class party with delegated authority, not a form on file.**

1. **Delegated permission model (C1.2).** A donor grants an advisor (Party) scoped privileges: `view`, `recommend_grants`, `recommend_investments`, `manage_investments_within_mandate`, `receive_documents`, `open_accounts_for_client` (pre-fill only). Each grant is a `PrivilegeGranted` event with donor consent, expiry and limits. Revocation is immediate (`PrivilegeRevoked`, with token revocation confirmed).
2. **Institution integration layer (C1.3).** Institutions connect by API (OAuth client credentials, per-institution scopes) and by event webhooks. Three integration patterns:
   - **(a) Embedded:** the institution's UI renders DAF data and submits requests via `/v1/*`.
   - **(b) White-label portal:** the enterprise renders under the institution's brand.
   - **(c) Data-only:** positions and grant feeds into advisor performance and CRM systems.
3. **Investment servicing.** Advisor-managed accounts trade within a sponsor-approved mandate. `InvestmentRequested` goes through a pre-trade mandate check (D), then `TradeInstructed` to the custodian. This replaces after-the-fact review (ACT-034).
4. **Advisor copilot (AGT-A).** Inside the advisor's workflow it:
   - assembles a client's philanthropic summary;
   - drafts grant-recommendation options for the client to confirm;
   - explains DAF-versus-direct-gift trade-offs with citations;
   - prepares year-end contribution intent packages.

   It never submits on its own. The advisor submits, and the donor confirms where policy requires.
5. **Relationship-preserving economics.** Every partner-facing view shows advisor fees at the account level. The enterprise does not cross-sell investment management to an advisor's clients. Successor-advisor handling is a policy choice made explicit to donors (WaterStone litigation concerns successor advisers, report §11.9). Revenue share with institutions is computed by the fee engine and disclosed.

## 5. Eliminated activities

- ACT-056: paper advisor access forms, replaced by delegated grants.
- ACT-004: reduced wholesaling, replaced by a sandbox and documentation.
- ACT-034: after-the-fact trade review, replaced by pre-trade checks.
- ACT-057: manual advisor fee reconciliation, now done by the fee engine.
- Re-keying account-opening data from advisor CRMs (ACT-006).
- Quarterly advisor statement packs, replaced by feeds.

## 6. New workflows

- **WF-I1 Advisor-initiated account opening.** The advisor pre-fills via the API. The donor verifies identity and accepts the agreement in an authenticated step (`IdentityVerified`, `AgreementAccepted`). `AccountOpened` is followed by `PrivilegeGranted` (advisor scope).
- **WF-I2 Mandate trading.** `InvestmentRequested` → mandate check (asset menu, concentration, liquidity floor, excess business holdings) → `TradeInstructed` or a denial with reason → custodian → `PositionChanged` → reconciliation.
- **WF-I3 Advisor fee billing.** Period close → fee engine computes advisor fees under the cap policy version → `FeeAccrued`. A cap breach blocks the fee and opens a case → payment to the advisor firm.
- **WF-I4 Institution onboarding.** Contract (H) → sandbox credentials → conformance test suite against the [API contracts](../../04-enterprise-apis/) → production scopes granted by the Change Board (H) → monitoring.
- **WF-I5 Advisor change.** The donor revokes old advisor privileges and grants new ones. The mandate is reassigned by the sponsor (H if it is a manager change in the pool). Pending advisor requests are canceled.

## 7. Required data

Party records for advisors and firms (CRD/IARD numbers where applicable); firm-level agreements (fee share, data contract version); PrivilegeGrants; mandates (allowed instruments, bands, manager); fee schedules and caps by policy version; positions per account; partner telemetry (API usage, errors, latency).

## 8. Required APIs

`/v1/parties` (advisor and firm), `/v1/privileges` (grant and revoke, scopes), `/v1/accounts` (open with pre-fill), `/v1/investment-requests`, `/v1/positions`, `/v1/fees`, `/v1/recommendations` (advisor-submitted, with a donor-confirmation flag), `/v1/documents`, `/v1/events` (webhooks per institution), `/v1/reports` (advisor book-level). Partner sandbox and conformance suite.

## 9. Event triggers

`PrivilegeGranted` / `PrivilegeRevoked`, `InvestmentRequested`, `TradeInstructed`, `PositionChanged`, `PolicyBandBreached`, `FeeAccrued`, `ContributionSettled` (advisor notified), `GrantApproved` and `PaymentSettled` (advisor visibility per scope), `PolicyPublished` (fee or mandate policy changes reach partners), `ComplianceObligationChanged` (for example a final §4966 rule).

## 10. AI agent responsibilities

| Agent | Role | Limits |
|---|---|---|
| Advisor copilot (Category 2/3) | Summaries, options, drafts, citations, year-end packages | No submit authority; no access beyond the advisor's privilege scope; no tax conclusions |
| Partner integration assistant (Category 2) | Helps partner engineers read contracts and conformance failures | Sandbox only |
| Related-party detector (Category 2) | Flags advisor relationships suggesting donor control or benefit, for example an advisor who is a family member or controls a recipient | Flag-only |

## 11. Deterministic automation responsibilities

Privilege enforcement on every call; the pre-trade mandate check; fee computation and cap enforcement; webhook delivery with retries and signatures; conformance test execution; per-institution rate limits; revocation propagation.

## 12. Human oversight requirements

- Approval of each institution's production access and data scopes (Change Board).
- Mandate design and manager approval (Investment Committee, DEC-022).
- Fee schedule and cap policy (board, DEC-066).
- Advisor-status reclassification if the final §4966 rule changes (GC → policy).
- Disputes between donor and advisor (client operations plus counsel).

## 13. Exception management

Exception case types:
- `advisor.mandate_breach`: a request denied repeatedly, or a breach detected post-trade.
- `advisor.fee_cap`.
- `advisor.related_party_flag`.
- `partner.integration_incident`: the partner's errors or latency exceed the SLO.
- `advisor.dispute`.

Partner incidents follow the incident runbook in K.

## 14. Security and compliance controls

- OAuth 2.0 with fine-grained scopes and per-institution client credentials (mTLS for server-to-server).
- Short-lived tokens; signed webhooks; per-partner rate limits.
- Field-level data minimization by scope; partner access logs available to donors ("who viewed my account").
- An annual partner security attestation plus continuous telemetry.
- No shared credentials (DD-017).

## 15. Estimated staffing implications

**Drivers:** the number of institutional partners (not advisors), integration complexity, mandate count, and dispute rate.

**Direction:** relationship managers scale with institutions, not with advisors. Integration engineers are front-loaded. FTE by scale is in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Time to onboard an institution (sandbox to production) | ≤ 8 weeks after contract |
| Pre-trade check latency | p95 < 500 ms |
| Advisor-managed trades executed outside mandate | 0 |
| Advisor fee calculation errors | 0 material (reconciled to invoice) |
| Partner API availability | ≥ 99.9% |

## 17. Implementation dependencies

Custodian integration with order and position APIs or files; the authorization model (C1.2); the fee engine; the policy registry (mandates as policy objects); the partner developer portal; legal templates for data contracts and revenue share; monitoring of the §4966 rulemaking (regulatory change monitor).

## 18. Measurable success criteria

- Advisor-initiated openings with zero re-keyed fields.
- Advisor fee transparency on 100% of advisor-managed accounts.
- Advisor-reported retention or NPS in the pilot institutions vs control (test the continuity hypothesis; do not assume it).
- Zero credential-sharing integrations.
- Revocation effective within 60 seconds end to end.
