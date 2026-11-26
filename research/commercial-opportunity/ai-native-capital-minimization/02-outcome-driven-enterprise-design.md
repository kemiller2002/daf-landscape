# 02: Outcome-driven enterprise design

**Pass:** OPS (parts 1-2). **Data:**
- [`outcomes.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/outcomes.csv) (27 outcomes);
- [`responsibility-matrix.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/responsibility-matrix.csv) (83 elements, 39 needing a person);
- [`work-elimination.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/work-elimination.csv) (33 activities).

**Integrator conclusions**
- Designing from outcomes and applying prevent → eliminate → consolidate → simplify → automate → AI → human removes about **40%** of the previous AI-native servicer minutes: 50.7 → about 30.1 per account-year at market mix.
  - About 31 points of that is eliminated work.
  - About 10 points is **transferred** to donors, charities, intermediaries, sponsors or auditors (5.0 minutes per account and about 600 minutes per sponsor-year). Transferred work is not counted as eliminated.
- **Correction to the previous study:** its "AI-native + elimination" scenario (33.8 minutes) included transfers.
- The integrated model carries the outcome-designed variant (30.1 minutes; 12,720 sponsor-level minutes, from 19,440) **only as an unproven hypothesis**. Every minute rests on assumed exception rates; no time study exists.
- Responsibility assignments keep every legally or contractually human element human: sponsor reserved authority (SPD-ADV-001), OFAC dispositions, 4966 expenditure responsibility, release and independent review. AI is capped at recommend and prepare (report 08).

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Summary

**Group OPS. Question:** if the DAF servicer is designed from outcomes, with deterministic software and AI from day one, how much human work remains, and does that change the economics?

**Answer: the redesign removes about 40% of the remaining servicer minutes (about 31% eliminated, about 10% transferred to others). It does not produce a different kind of company.** Account-level minutes fall from 50.7 to about **30 per account-year** at market mix [D from A]. That is **15.6 minutes eliminated plus 5.0 transferred** to donors, charities, intermediaries and auditors; transfers are not counted as eliminated. The control floor is about **12 servicer minutes** plus 2.7 sponsor-appointed minutes, of which about 9 are legal, independence or control work. Below roughly 15 minutes (floor plus sponsor-level work), control would have to be weakened.

**Why the economics barely move:**
- **Minutes are a small cost.** At market mix and 20 bps, labour at 50.7 minutes is about $55 of $877 revenue per account-year (6%) [D]. With Model B fixed cost, break-even assets move from $0.98B (50.7 minutes) to $0.96B (redesign) and $0.92B at zero minutes (simplified one-line sensitivity, not a reproduction of the F# model). Fixed control, engineering, assurance and sales costs decide break-even, not handling time.
- **Indivisibility and independence set headcount at small scale.** Below about 3,000-5,000 accounts, the two-operations-person dual-control floor, a controller, three engineers for two-approver change control (CNV-PLT-010), an independent reviewer and named sponsor appointees are needed whatever the minutes.
- **Above about 5,000 accounts, December sets headcount, not the annual average.** With 26.5% of minutes in December, clearing the 31 December backlog within 10 January working days needs about 9 core servicing FTE at 10,000 accounts, against 5 on annual sizing [D from A].
- **Every new sponsor starts in pre-delegation.** Without board delegation, three-person release and 100% calibration review apply, adding about 14 minutes per account-year. Year-1 reality is about 45-75 minutes, not 30.

**Verdict on the premise.** An outcome-designed servicer is a better-controlled, somewhat cheaper version of the same business. Its advantage over incumbents is evidence and control quality more than cost. Most of the levers (continuous charity monitoring, EFT default, proactive status, generated reports) are available to incumbents too.

## Method and labels

- **Inputs:** prior ACT activity register (33 activities), prior capacity model, prior F# Parameters.fs, Unbound convergence clauses (82, read directly) and SPD-ADV-001.
- **Order of methods per activity:** prevent > eliminate > consolidate > simplify > deterministic automation > AI > human.
- **Typical-account recomputation:** each activity's AI-native minutes are re-estimated as after-minutes, eliminated minutes and transferred minutes. The script asserts that after + eliminated + transferred = baseline. Two activities (A10 monitoring, A14 EFT) **increase**.
- **Market mix:** reconstructed from archetypes. Known top-3 activities are scaled by their own ratios and the remainder by the typical ratio (0.608) [D].
- **Capacity:** 82080 queue minutes per FTE-year (1,520 h x 0.9 x 60, prior model) and $1.0908 per minute.
- **Labels:** [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured.
- **Time study:** none exists, so every minute is [A] (CNV-EVB-001).
- **Independence:** same model family as the prior study, so this is not independent validation.
- **Reproduce:** `python3 -I -B build_ops.py .`, then `python3 -I -B build_report.py .`.

## Part 1: Outcome register and responsibility matrix

**27 outcomes** and **83 elements**, covering decisions, information, controls and actions. Of these, **39 elements require a person**.

Elements by performer type:

| performer type | elements |
|---|---|
| deterministic_software | 23 |
| human_decision_maker | 23 |
| ai_agent | 14 |
| sponsor_appointed_authority | 10 |
| external_provider | 7 |
| contracted_specialist | 4 |
| independent_reviewer | 2 |

Added beyond the brief's list:
- audit and assurance;
- records retention and privacy;
- succession and disputes;
- sponsor governance (delegation);
- payment exceptions and unclaimed property;
- policy change control;
- vendor management;
- donor disclosures and communications;
- workforce coverage;
- the servicer's own billing.

**Human elements that cannot be removed, and why:**

| Element | Basis |
|---|---|
| Exception-grant decisions, gift acceptance, delegation adoption, block/reject, successor recognition | Sponsor-appointed authority: IRC 4966/4967 exclusive legal control via CNV-GRT-001; CNV-GOV-004 bars vendor staff from A3+ authority; SPD-ADV-001 makes appointees exclusive to one sponsor |
| Sanctions match disposition | 31 CFR 501.603/604 via CNV-GRT-006; never auto-closed |
| Clearing prohibited-benefit flags | AI may flag, never clear |
| Payment release | Three distinct persons until the auditor and board accept the deterministic gate (CNV-GOV-003) |
| Reconciliation attestation, decision-quality sampling, board-report samples | Independent reviewer (CNV-FIN-004, CNV-GRT-011, CNV-GOV-008) |
| Monthly completeness sign-off | Controller (ICFR/SOC 1 expectation) |
| Control-relevant code changes | Two approvers who are not the author (CNV-PLT-010) |
| ACH origination | The sponsor is Originator (NACHA, CNV-PAY-001); the servicer is a third-party service provider |

**Design consequence: the servicer cannot be 'AI plus a few staff'.** It is staff plus contracted specialists plus **sponsor-side appointees**, whose time is a real cost to the buyer (2.7 minutes per account-year at the floor).

## Part 2: Work elimination

**Typical account:** 38.03 -> **23.14** minutes per account-year. Of the 14.89 removed, **11.15 are eliminated** and **3.74 are transferred**.

The prior 'elimination' scenario reached 27.34 but booked check-to-EFT and foreign-grant routing as elimination.

**Market mix:** 50.7 -> **30.1**, with 5.0 transferred [D/E].

Largest eliminations (typical account):

| activity | baseline | after | eliminated | transferred | to |
|---|---|---|---|---|---|
| ACT-A11 Grant approval incl. eligibility exceptions ( | 12.6 | 9.5 | 3.1 | 0.0 |  |
| ACT-A15 Payment processing: check grant (print, posit | 3.56 | 1.2 | 1.96 | 0.4 | charity (EFT enrollment and bank-detail  |
| ACT-A13 Non-standard grantee due diligence (foreign,  | 5.4 | 2.2 | 1.0 | 2.2 | US intermediary / ED provider (fee borne |
| ACT-A17 Returned / uncashed / voided checks and reiss | 1.34 | 0.45 | 0.89 | 0.0 |  |
| ACT-A04 Contributions: publicly traded securities (DT | 2.0 | 1.0 | 0.8 | 0.2 | donor and donor's broker (pre-announceme |
| ACT-A21 Donor / advisor service contacts (human-handl | 2.0 | 1.2 | 0.7 | 0.1 | donor (self-service navigation effort) |
| ACT-A09 180-day charity re-verification (deep review  | 1.08 | 0.4 | 0.68 | 0.0 |  |
| ACT-A18 Reconciliation (bank, custodian, ledger; brea | 1.15 | 0.7 | 0.45 | 0.0 |  |

**Evaluated levers:**
- **Continuous reconciliation** (A18): -0.45. It was already in the AI-native baseline; the independent sample stays.
- **Transaction-time audit evidence** (S04): -1,100 minutes per sponsor-year, **only after the auditor confirms reliance** (CNV-GOV-001), plus 300 minutes transferred to the sponsor's auditor.
- **Reports from authoritative records** (S01, S05, A20): -3,720 minutes per sponsor-year and -0.1 per account.
- **Prevented customer questions** (A21, proactive status): -0.7, with 0.1 transferred.
- **Input design** (A02, A04, A07, A12): -1.6, with 0.57 transferred to donors.
- **Continuous charity monitoring:** A09 -0.68 and A08 -0.12, **but A10 +0.02.** Earlier detection creates work.
- **Configuration over custom engineering** (S02): -900, with 300 transferred to sponsor adoption.
- **Proactive problem detection** (S03): -400. Incident variance dominates (high case 12,000).
- **Repeatable onboarding** (S06): 18,000 -> 12,000 per new sponsor, by about the fourth to sixth sponsor.

**The biggest single lever is A11** (exception reduction through determination reuse and structured entry), at -3.1 minutes. It rests on replay rates (11.2% -> 4.0% -> 3.1%), not on any time study.

**Transfers flagged:** A05 complex gifts (0.30) and A13 foreign grants (2.20) go to fee-bearing intermediaries, a cost to the fund or charity. A15 shifts 0.40 to charities (EFT enrollment). Donors pick up about 0.8 minutes in total (attestations, references, self-service). S02 and S04 shift 600 minutes per sponsor-year to sponsors and their auditors.

## Challenge to previous conclusions and to the new premise

**Prior conclusions this pass supports:**
- **50 minutes AI-native is a defensible planning figure.** This pass reaches about 30 only with input redesign, determination reuse and board delegation, and only after a pre-delegation year at roughly 45-75.
- **5-6 people live** is right at break-even scale. Independence floors bind there.

**Prior conclusions this pass corrects:**
1. **The prior elimination scenario (33.8) counted transfers as elimination.** On a transfer-honest basis this pass's redesign eliminates about 16 minutes and transfers about 5.
2. **Hiring triggers.** The prior triggers were proxies (accounts, sponsors, ops counts). The real drivers are:
   - December clearance;
   - counterparties;
   - new sponsors;
   - sponsor books and break rates;
   - fixed independence floors (engineering change control needs 3 people; independent reviewer; sponsor appointees).
3. **The December-temps line understates peak cost.** Temps cannot release, and core staff sized to annual minutes cannot clear December.
4. **Sponsor-side cost was omitted.** Appointees, board review and adoption work are a buyer cost that affects willingness to pay.

**On the new premise, there is no fundamentally different company.**
- Even zero human minutes would lower simplified break-even assets by about 7% at market mix.
- The cost structure is fixed-cost and control-floor dominated.
- AI changes the evidence and control quality and the marginal cost of an extra account. It does not change the floor.
- The exception is **small-balance, high-activity books**. There, minutes are a large share of revenue (typical archetype: $300 revenue at 20 bps against about $25 of redesigned labour; small-recurring: $16 revenue against about $15). Pricing per account, not the minutes, decides those.
