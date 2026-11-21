# A. Donor acquisition and marketing

**Capabilities:** C1.3 (advisor and institution integration), C1.5 (discovery and education), C6.1 (philanthropic intelligence). **Outcomes:** O-09, O-13, O-14. **Accountable:** Head of Partnerships (distribution); Head of Philanthropic Intelligence (education content).
Labels: [V] validated, [I] inference, [A] assumption or design target, [S] scenario. Paths are relative to this file.

## 1 Existing industry operating model

- **Reported advertising is small at the nationals and concentrated at community foundations.** Pooled TY2021–24 Form 990 Part IX line 12 per dollar of new DAF money [C]:
  - affiliated-commercial nationals: 1.39 bps;
  - independent nationals: 0.41 bps;
  - digital-first: 1.70 bps;
  - community foundations: 18.4 bps whole-organisation (12.7 bps allocated to DAFs).
  - The median national sponsor reports $0 ([`direction-sponsor-marketing-spend.md`](../../../mission-2026-11-14/direction-sponsor-marketing-spend.md) §1).
- **One sponsor dominates the national figure.** Schwab Charitable is $20.3m of the affiliated group's $21.7m, about $390 per net new account. Fidelity Charitable reports $0 on line 12 in every year (same file).
- **Acquisition spend at affiliated and digital sponsors mostly sits off the 990.** The parent firm or the platform company pays for brand and adviser marketing (same file, §1 item 5). The true cost of acquisition is therefore **not observable** from public data (GAP: see [`../../00-research-inventory/`](../../00-research-inventory/)).
- **Advertising intensity does not go with growth in the cross-section.** The Spearman correlation is −0.25 across 55 community foundations and −0.34 across 99 sponsors, with no controls. The fastest-growing sponsors (Signatry, Daffy, Charityvest, Renaissance) are channel- or platform-led [C/I] (same file, §1 item 4; strategic synthesis §0 E).
- **Distribution runs through wealth firms.** About 11 wealth-firm programs run on RCF + Ren ([industry report §1, §2.2](../../../DAF-INDUSTRY-REPORT-2026-11.md)). TIAA, Temple and OneGive run on Charityvest/Foundation Source (§2.3). SEI uses both RCF/Ren and GiveClear/TIFIN (§2.4).
- **Tax-benefit messaging is common and often overstated.** For itemizers the tax result of a DAF gift and a direct gift is identical. For non-itemizers a DAF loses from 2026, because DAF gifts are excluded from the new nonitemizer deduction ([strategic synthesis §0 A](../../../mission-2026-11-14/strategic-synthesis.md); [`direction-donor-tax-scenarios-2026.md`](../../../mission-2026-11-14/direction-donor-tax-scenarios-2026.md); [industry report §6](../../../DAF-INDUSTRY-REPORT-2026-11.md) on OBBBA).
- **"Millions of DAF customers" is a denominator error.** 79.5% of 3.59m FY2024 accounts sit in 22 processors holding 0.9% of assets. The ongoing-advisory count is 2.59m, or 0.79m without Givinga and PayPal Giving Fund (strategic synthesis §0 A, G2).

## 2 Actual required business outcomes

1. Donors for whom a DAF is genuinely suitable learn about it and can open one through the channel they already use: advisor, wealth platform, employer or direct (O-14).
2. Donors for whom it is *not* suitable are told so (O-09, O-13). Examples: non-itemizers making small cash gifts in 2026, and donors who will grant everything within weeks.
3. The enterprise acquires accounts at a cost recoverable within the account's expected fee life (O-14).
4. Nothing the enterprise publishes is false or misleading (O-09).

## 3 Legal and risk constraints

- **Unfair and deceptive practice law** applies to claims, including state UDAP statutes and FTC-style standards as far as they reach the speaker. Applicability to the sponsor versus the distribution partner is mapped in [`../../08-governance-and-compliance/regulatory-applicability-map.md`](../../08-governance-and-compliance/regulatory-applicability-map.md).
- **No individualized tax advice.** The sponsor gives general information; a donor's specific situation goes to their own adviser (outcome model O-09).
- **Charitable solicitation registration.** Many states require it of organizations soliciting contributions ([`b50-02-state-registration.md`](../../../mission-2026-11-14/b50-02-state-registration.md)).
- **Advisor firms' own rules.** Reg BI and suitability obligations sit with the broker-dealer or RIA recommending the DAF, not the sponsor. Sponsor materials used by advisors must not undermine those obligations.
- **Privacy.** State privacy laws that cover nonprofits (the regulatory map lists which) limit purchased-data profiling and require notice and consent.
- **Risk.** Reputational exposure from "warehousing" narratives. Payout and transfer realities are in strategic synthesis §0 A.

## 4 Proposed AI-native operating model

**The conventional funnel (awareness → lead → nurture → conversion) is the wrong shape for this product.** [I] The evidence above shows acquisition is channel-led and that ad spend does not correlate with growth. The redesign replaces the funnel with three *intent-initiated* paths and an honest suitability step:

| Path | Who initiates | What the enterprise provides | Acquisition mechanism |
|---|---|---|---|
| **Advisor-embedded** | Advisor, in their own planning or custody platform | Account-opening, contribution-intent and suitability APIs; advisor copilot | Platform integration (C1.3); the relationship stays with the advisor (DD-010) |
| **Institution-embedded** | Wealth firm, bank, employer, platform (white-label or co-brand) | Embedded account capability under the institution's brand, with the sponsor of record disclosed | Partnership agreements (see area M) |
| **Donor-initiated** | A donor who arrives with a question ("should I give appreciated stock?") | Discovery and education agent producing a *suitability comparison*: DAF vs direct gift vs appreciated-stock gift direct to charity, using donor-supplied facts only | Educational content plus a transparent calculator; no tracking-based retargeting |

**Suitability before conversion.** Each path runs a deterministic suitability screen on donor-supplied facts:
- itemizing status;
- gift size relative to the OBBBA 0.5%-AGI floor;
- asset type (appreciated securities favour a DAF or a direct stock gift over cash);
- grant horizon.

The screen reports "a DAF adds little for you" when that is the result. **This is a deliberate trade:** fewer low-value accounts, higher trust, and alignment with the evidence that the median account pays out about 9% over three years ([industry report §1](../../../DAF-INDUSTRY-REPORT-2026-11.md)).

**AI identifying donor needs without intrusive profiling:**
- Needs are *elicited*, not *inferred from purchased data*. The discovery and education agent asks, explains and computes from what the donor or advisor provides in session.
- There is no third-party wealth-data enrichment (ACT-002 eliminated).
- The agent is constrained to approved educational content with clause-level citations, and it is barred from personalized tax conclusions. Its outputs are illustrative calculations with stated assumptions and a referral prompt.
- The donor's facts are stored only if they open an account and consent. Otherwise the session data expires.

## 5 Eliminated activities

- ACT-002: lead scoring from purchased third-party wealth data. **Eliminated.**
- ACT-003: generic tax-benefit marketing claims. **Transformed** into cited content that includes the direct-gift comparison.
- ACT-001: mass-market brand advertising. **Reduced**; spend is redirected to partner integrations.
- ACT-004: advisor wholesaling visits to explain features. **Reduced**, replaced by a sandbox, an API and embedded workflows. Human relationship managers remain for institutions.

## 6 New workflows

- **WF-A1 Advisor-embedded opening:**
  1. The advisor platform calls `POST /v1/accounts` with a donor consent token.
  2. Suitability API.
  3. Prefilled verified data (see area B).
  4. `AccountOpened`.
  5. The advisor gets a `PrivilegeGranted` of scope investment-recommend (if the program allows) and view.
- **WF-A2 Donor-initiated suitability session.** Discovery agent → deterministic suitability calculation → three-way comparison → optional hand-off to opening, or to "talk to your adviser".
- **WF-A3 Partner onboarding.**
  1. Institution signs.
  2. Sandbox credentials.
  3. Conformance test suite (deterministic).
  4. Production scopes are granted by an H decision of the Head of Partnerships with CRCO sign-off.
- **WF-A4 Content release.** Agent-drafted educational content → GC review (H) → published with clause IDs → used by the service and discovery agents.

## 7 Required data

- Donor-supplied suitability facts (ephemeral unless consented).
- Approved content corpus with clause IDs and review dates.
- Program definitions: fees, minimums, investment menus.
- Partner registry: scopes, brands, sponsor-of-record disclosures.
- Channel attribution per account: the partner ID only, not behavioural tracking.
- Acquisition cost per channel: partner revenue share plus integration cost.

## 8 Required APIs

- `/v1/accounts`: open, with a partner consent token.
- `/v1/parties`: prefill from verified partner data.
- `/v1/privileges`: advisor scopes.
- `/v1/documents`: program disclosures.
- `/v1/policies`: read-only published fee and program policy.
- `/v1/reports`: partner book-of-business reports.
- Suitability calculator: a deterministic endpoint under `/v1/policies/{id}/evaluate`, with policy `suitability@vN`.

## 9 Event triggers

- `AccountOpened`: attribution to the partner and telemetry.
- `PrivilegeGranted`: the advisor relationship established.
- `PolicyPublished`: suitability or fee policy changed; content is re-validated.
- `ComplianceObligationChanged`: for example a tax-law change; all content citing the affected obligation is flagged for review.

## 10 AI agent responsibilities

| Agent | Category | Responsibility | Prohibited |
|---|---|---|---|
| Discovery and education agent | 2 (AI-assisted analysis) | Explain options; run the deterministic calculator on stated facts; cite approved clauses | Individualized tax conclusions; inferring wealth from outside data; steering to fee-maximizing choices |
| Advisor copilot | 2 | Inside the advisor platform: draft client explanations, prepare contribution intents for the advisor to confirm | Submitting instructions without advisor and donor confirmation |
| Policy drafting and impact agent | 2 | Draft content updates after law changes; list every content clause affected | Publishing |

## 11 Deterministic automation responsibilities

- Suitability calculation: versioned rules, auditable inputs and outputs.
- Partner conformance test suite.
- Channel attribution and revenue-share calculation (fee engine C4.3).
- Content expiry: clauses past their review date are withdrawn automatically from agent retrieval.

## 12 Human oversight requirements

- GC approves every content clause (H).
- Head of Partnerships and CRCO approve partner production access (H).
- The board approves fee schedules and revenue-share policy (H, O-14).
- Quarterly fairness review: are suitability outcomes consistent across channels, and is any partner steering?

## 13 Exception management

| Exception | Route |
|---|---|
| Suitability result disputed by an advisor | Partnerships case; the calculation inputs are shown, and the rule cannot be overridden for one client |
| Content complaint | Service recovery plus GC |
| A partner breaching brand or disclosure terms | Partnerships, which can suspend scopes |

## 14 Security and compliance controls

- Partner OAuth scopes per institution.
- Donor consent token required for any prefill.
- No pixel or retargeting trackers on education pages [A design rule].
- Content is versioned with approval evidence (C4.5).
- The sponsor of record is disclosed on all embedded surfaces.
- Agent output filters block personalized-advice patterns, and violations are logged as AgentRun flags.

## 15 Estimated staffing implications

**Drivers:**
- number of institutional partners (relationship managers per partner, about 1 per 10–20 active institutions [A]);
- content volume and legal review hours;
- integration engineering per new partner platform.

**Direction:** far smaller than a sales and marketing department. Wholesaling and generic campaign roles disappear, and partnership, integration and content-review roles remain. Numeric FTE comes from [`../../09-financial-models/`](../../09-financial-models/).

## 16 Cost and performance model

**Cost drivers:** partner revenue share, integration engineering, legal content review, the education agent's inference cost (immaterial per session; see [`ai-economics-replacement-analysis.md`](../../../mission-2026-11-14/ai-economics-replacement-analysis.md)).

**Design targets [A]:**
- blended acquisition cost per funded account below 12 months of expected account fee revenue;
- 100% of published claims cite an approved clause;
- suitability screen completed before 100% of openings.

## 17 Implementation dependencies

- Partner platform APIs and consent standards.
- The fee schedule and program definitions (board).
- Approved content corpus (GC).
- Sponsor-of-record arrangement (Models B, C or D; see [`../../10-market-and-business-model/`](../../10-market-and-business-model/)).
- Privacy notice and consent design.

## 18 Measurable success criteria

1. Share of accounts opened through embedded channels.
2. Funded-account conversion after a suitability screen, compared with the share told "a DAF adds little".
3. Acquisition cost per funded account, by channel.
4. 12-month activity rate: at least one grant or contribution after the first.
5. Number of content findings by GC or regulators. Target: zero material.
6. Advisor retention of client relationships, measured by account transfers *away from* the advisor caused by the sponsor. Target: zero.
