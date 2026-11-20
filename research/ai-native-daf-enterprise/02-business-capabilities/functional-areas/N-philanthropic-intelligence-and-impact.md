# N. Philanthropic intelligence and impact

**Capabilities:** C6.1 Philanthropic intelligence (primary), C1.5 Discovery and education, C3.1 (recipient registry), C3.5 · **Outcomes:** O-13, O-09, O-15 · **Accountable:** Head of Philanthropic Intelligence

## 1. Existing industry operating model

Sponsors offer charity search (usually IRS-derived data plus Candid/GuideStar), curated lists, giving guides and annual impact reports built from grant totals.

What the repository shows:

**Ratings in grant flows**
- No top-20 sponsor shows Charity Navigator ratings in its grant flow. Where a search vendor is named, it is Candid/GuideStar.
- Charity Navigator rates 245,000+ charities (about 17% of Pub 78 records). Its API licence is non-sublicensable, requires a linkback, and bars using ratings "in any other calculation", which constrains AI rankers ([industry report §11.25](../../../DAF-INDUSTRY-REPORT-2026-11.md); [`direction-charity-ratings-integrations.md`](../../../mission-2026-11-14/direction-charity-ratings-integrations.md)).
- Only 72.66% of top-50 FY2023–24 DAF-weighted dollars went to recipients that were rating-eligible at grant time (§11.70). Ratings-based discovery would systematically under-serve the rest.

**Who is invisible to data-driven discovery**
- Church-status recipients with no e-filed 990 take 8.3% of top-50 DAF dollars, about half of it congregations. None of 14 congregation giving pages read showed a DAF option.
- Church grants in the BMF but not Pub 78 ($2.17bn in the top-50 sample) are mostly group-ruling subordinates: a ratings gap, not an eligibility gap (strategic synthesis §0 G4; report §11.25; [`b4026-06-church-daf-recipients.md`](../../../mission-2026-11-14/b4026-06-church-daf-recipients.md)).

**Local knowledge**
- Community foundations keep 60% of grant dollars in-state (median 71%), against 7.6% for national sponsors ([`direction-grant-geography.md`](../../../mission-2026-11-14/direction-grant-geography.md)).

**Payout and dormancy**
- The median account pays out about 9% over three years, and 22% of accounts made no grants in 2020–22, in voluntary samples.
- The literature finds that sponsor websites stressing donor benefits predict lower payout ([`direction-academic-literature.md`](../../../mission-2026-11-14/direction-academic-literature.md) F1–F2).

**Donor information reaching nonprofits**
- Only 36% of sponsors in the CF-weighted DAFRC survey default to sharing full contact data ([`direction-nonprofit-side-experience.md`](../../../mission-2026-11-14/direction-nonprofit-side-experience.md)).

**Impact claims**
- Annual reports conflate grant volume with impact [I].
- No repository source shows a sponsor publishing evidence-graded outcome data.

## 2. Actual required business outcomes

- Help donors act on their own charitable goals, including converting dormant balances into grants, without steering them for the sponsor's benefit (O-13).
- Give donors accurate, sourced, evidence-graded information about recipients, and never present outputs as demonstrated impact (O-09, O-13).
- Treat all eligible recipients fairly, including small, local, faith-based and newer organizations that are thin in data (O-13, O-15).
- Measure the enterprise's philanthropic value by observable outcomes it controls: time-to-grant, active-account share, recipient cost reduction and goal attainment. Leave recipients' impact to evidence the recipients or evaluators provide.

## 3. Legal and risk constraints

| Constraint | Implication |
|---|---|
| Sponsor neutrality and donor intent; no prohibited benefit through recognition-for-placement schemes | No paid placement in rankings; recipient-paid promotion is prohibited (§4967/§4958 risk if linked to donors or insiders) |
| Data licences (Charity Navigator, Candid) | Respect limits on display, caching and derived calculation; maintain a licence register |
| Privacy: donor goal profiling | Elicited, consented goals only; no covert inference from external wealth or behavioral data (ACT-002 eliminated) |
| Advice boundary | Information, not individualized investment or tax advice |
| Discrimination and fairness reputational risk; lobbying-related recipient issues | 42.2% of covered DAF dollars go to recipients that report any lobbying (strategic synthesis §0, notable). Lobbying status is information, not a negative signal by default |
| Discretionary sponsor policy (for example holds on recipients) | Board policy (L); the discovery agent must reflect holds consistently and explain them neutrally |

## 4. Proposed AI-native operating model

1. **Goal discovery is a conversation the donor controls.**
   - The **discovery/education agent** helps the donor articulate goals: causes, geography, time horizon, a desired payout pace, and whether they want local or faith-community giving.
   - Goals are stored as donor-owned preferences, editable and deletable.
   - No external profiling is used.
2. **Recipient information with evidence grades.** Each recipient profile shows sourced facts (IRS status, filings, programs, geography, size) and a separate **impact-evidence grade** per claim:

   | Grade | Meaning |
   |---|---|
   | E0 | No outcome evidence |
   | E1 | Self-reported outputs |
   | E2 | Self-reported outcomes with method |
   | E3 | Independent evaluation |
   | E4 | Rigorous causal evidence |

   An output (meals served) is never labeled as impact. Grades come with their source and date.
3. **Responsible recommendation.**
   - The ranking criteria are disclosed and donor-selectable: relevance to the donor's stated goals, geography, recipient size, and evidence grade *when the donor chooses it*.
   - Defaults do not penalize missing data. Thin-data recipients such as congregations and small local organizations are shown with "data not available" rather than ranked lower.
   - Ratings are displayed under licence terms but are not fed into our own ranking calculation where the licence bars it.
4. **Dormant-capital engagement.** Deterministic, policy-approved triggers (DEC-065), for example no grant in 18 months, or a balance above the donor's own stated annual giving goal. These produce reminders that include the donor's own goals and the option to set up recurring grants. The engagement policy is approved by the board, because asset-based fees create a retention incentive [industry report §3]. The enterprise reports payout metrics publicly to counter it.
5. **Recipient-side value.** Machine-readable remittance (DD-018), donor information shared per the donor's choice, and an optional recipient portal to confirm details and report outcomes voluntarily, which raises evidence grades.
6. **Local and affinity knowledge as a partner capability.** Community foundations and faith networks can publish curated, sourced recipient information into the registry under their own attribution. This preserves their local-knowledge advantage instead of competing with it.

## 5. Eliminated activities

- ACT-066: impact reports built by hand, replaced by generation from the grant ledger with evidence grades.
- ACT-067: staff charity curation lists, transformed into transparent, sourced profiles with disclosed criteria.
- ACT-002: covert lead and wealth profiling, eliminated.
- ACT-003: generic tax-benefit marketing, transformed into cited education that includes the direct-gift comparison.

## 6. New workflows

- **WF-N1 Goal-to-grant.** The donor sets goals with the agent, which presents candidate recipients with sources and grades. The donor selects, the agent prepares a recommendation draft, the donor confirms, and `RecommendationSubmitted` enters the standard grant decision path (03-).
- **WF-N2 Annual philanthropic review.** A year-end deterministic summary from the ledger: grants by the donor's goals, payout pace against the donor's own target, recipients' evidence grades, and the donor-chosen next steps.
- **WF-N3 Evidence grade update.** A new source (recipient report, evaluation, filing) leads to an agent-extracted claim plus a proposed grade. A research analyst confirms grades E3 and above (H). The profile is updated with provenance.
- **WF-N4 Fairness audit (quarterly).** Exposure and selection rates are compared by recipient segment (size, geography, faith, data-thinness, newness) against a donor-goal-matched baseline. Disparities are investigated by a human and policy changes go through C6.4.
- **WF-N5 Partner-curated collections.** A community foundation or faith network publishes a collection with attribution. It is schema-validated and shown with the publisher's label.

## 7. Required data

Recipient registry and EligibilityFacts (C3.1); filings-derived recipient attributes; licensed ratings (display-only where required); evidence claims with grades and sources; donor goals (donor-owned); grant ledger; engagement-trigger policy; fairness audit datasets; data licence register.

## 8. Required APIs

`/v1/recipients` (profiles, collections), `/v1/eligibility`, `/v1/recommendations` (draft), `/v1/grants` (history for reviews), `/v1/reports` (annual review, public payout metrics), `/v1/parties/{id}/preferences` (goals), `/v1/events`. External: data providers under licence.

## 9. Event triggers

`CharityEligibilityChanged` (profile update; pending grants re-evaluated elsewhere), `GrantApproved` and `PaymentSettled` (history), `AccountInactivityThresholdReached` (engagement), `ContributionSettled` (suggests a goal-setting session if no goals exist), `PolicyPublished` (engagement or ranking policy), `AgentRunCompleted` (grade proposals).

## 10. AI agent responsibilities

- **Discovery/education agent** (Category 2/3):
  - It does goal elicitation, sourced recipient summaries, and education with citations (including when a direct gift may be better than a DAF grant).
  - It prepares draft recommendations; it cannot submit.
  - It must show evidence grades and data gaps.
  - It is prohibited from ranking with licence-barred inputs, from paid placement, and from inferring protected or sensitive donor attributes.
- **Evidence extraction agent** (Category 2): extracts outcome claims and methods from recipient documents and proposes grades. A human confirms E3 and above.
- **Fairness monitor** (Category 2): computes and narrates segment disparities. Flag-only.

## 11. Deterministic automation responsibilities

Engagement triggers; annual review generation; public payout-metric computation (aggregate, net-of-DAF-transfers and median, defined explicitly to avoid the denominator problems documented in strategic synthesis §0 A); licence-compliance enforcement (display rules, caching limits); provenance stamping.

## 12. Human oversight requirements

The ranking and engagement policy is approved by the board or delegated committee. Research analysts confirm high evidence grades. Fairness audit findings are reviewed by the Head of Philanthropic Intelligence with GC. Partner collections are approved for publication.

## 13. Exception management

Case types: `intel.grade_dispute` (a recipient challenges a grade), `intel.fairness_disparity`, `intel.licence_conflict`, `intel.misinformation_report` (a donor or recipient reports an incorrect fact, which is corrected with provenance).

## 14. Security and compliance controls

- Donor goals are visible only to the donor and their delegated advisor scope.
- Analytics use pseudonymous keys.
- A licence register enforces display and caching rules.
- No sponsor commercial interest in rankings: recipients cannot pay for placement.
- Model-output validators require citations for every factual recipient claim.

## 15. Estimated staffing implications

**Drivers:** recipient universe coverage, evidence-grade review volume (E3+), and fairness audit cadence.

**Direction:** a small research team. Most profile assembly is automated, and humans focus on grading rigor and fairness. FTE in [`../../09-financial-models/`](../../09-financial-models/).

## 16. Cost and performance model

| Metric | Target [A] |
|---|---|
| Recipient profiles with sourced facts | 100% of the eligible US universe (IRS-derived baseline) |
| Factual claims with citation | 100% |
| Accounts with a grant in trailing 12 months | Above baseline (validate against DAFRC's 22% inactivity reference) |
| Median days from contribution to first grant | Measured; published |
| Segment exposure disparity vs goal-matched baseline | Within policy tolerance, investigated otherwise |

## 17. Implementation dependencies

Recipient registry and eligibility (C3.1); data licences; the grant ledger; the donor preference store; the evaluation datasets for agents (05-); board-approved ranking and engagement policies; partner collections schema.

## 18. Measurable success criteria

- No impact claims without an evidence grade.
- Zero licence violations.
- Published annual payout metrics with explicit definitions.
- Fairness audit performed quarterly, with disparities resolved or justified.
- Donor goal-attainment self-report improves year over year.
- Recipient-reported attribution success (the grant was identified and thanked) ≥ 95% for electronically paid grants.
