# 09: Administrative overhead elimination

**Pass:** OPS (part 5), with ADV2-013. **Data:** [`overhead.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/overhead.csv) (13 categories).

**Integrator conclusions**
- Conventional coordination is about 12 hours per person-week; the AI-native residual is about 4.75. The integrated design assumes:
  - a shared case/event model;
  - generated status and management reporting;
  - no ticket routing;
  - no re-keyed data;
  - no interdepartmental reconciliation.
- **The real gain is small.** The previous study's 1,520 productive hours already deducted about 6 hours a week for meetings and administration. Against that baseline the gain is about 1.25 hours per person-week, **about 3% of capacity**.
- The integrated model costs coordination only beyond six pairs (ADV2-013) and gives the outcome-designed variant +3% capacity.
- **Governance overhead remains:**
  - board and sponsor reporting;
  - change approval;
  - the independent-review sample;
  - the SOC control calendar;
  - December readiness.
- These are obligations, not habits.
- The overhead sources are broad-population surveys (Microsoft 365 telemetry; an Asana survey reported in Computerworld), not small servicers.

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 5: Administrative overhead

**Conventional small-firm coordination overhead:** **12.0 h per FTE-week** [A, range 8-14], built up across 13 categories.

It is informed by two broader measures, neither of which is a small-firm overhead measure:
- Microsoft 365 telemetry: 57% of intentional app time spent communicating (23% meetings, 19% chat, 15% email) [S, quality C];
- Asana's 2023 survey: 58% 'work about work' and 2.8 h per week of unnecessary meetings [S via secondary, quality C].

**AI-native residual:** **4.75 h per FTE-week** [A, range 3-6]. What remains:
- SoD approvals (controls);
- risk, incident and ops reviews;
- control documentation and runbooks;
- escalations;
- independent sampling, which replaces the QA function.

**Removable by one authoritative record and case store:**
- status reports;
- performance and operational reporting;
- ticket routing;
- repeated data entry;
- interdepartmental reconciliation;
- most project tracking.

**Economic value:** 7.25 h per FTE-week x 46 weeks x $82/h is about $27,347 per FTE-year against a conventional firm.

**Against the prior model the gain is small.** The prior model already deducted about 6 h per week (15%) for meetings and admin (report 03:111), so the AI-native gain over it is only **about 1.2 h per FTE-week (about 3% of capacity)**. For a 7-person team that is roughly $33,005 a year, and it becomes cash only if it avoids a hire.

**Coordination cost is real but second-order** for a firm of 6-10 people, with 15-45 pairwise links. It matters more as the firm grows. 'Repeated data entry' overlaps with activity minutes; do not add it twice.

## Limitations and evidence gaps

**Limitations:**
- **No time study, no operating data, no sponsor input.** Every minute is [A]. Exception incidence and December arrivals are the two most consequential unknowns (CNV-EVB-001).
- **The market-mix reconstruction is approximate.** It uses archetype top-3 activities only, and the archetype mix (20/20/40/7/10/3) is itself an assumption.
- **The break-even figures are a one-line sensitivity** (Model B fixed $1.74M, market-mix balance). They do not re-run the F# model with sponsor-level costs; prior break-even ranges remain authoritative for levels.
- **Legal bases are cited through Unbound clauses and the prior register.** IRC 4966/4967, 31 CFR 501 and the NACHA rules were not re-read in primary form in this pass.
- **Coordination-overhead sources are vendor studies of large populations** (telemetry or survey), not small DAF servicers.
- **Learning-curve and adapter-effort parameters are generic assumptions.**
- **AI capability limits are design requirements, not tested behaviour.**
- **Same-model reasoning.** The integrator and adversarial reviewers should challenge A11 minutes, the floor composition and the December model independently.

**Highest-value evidence to collect:**
1. a 90-day time study on a real sponsor book;
2. a 12-month shadow replay of exceptions;
3. December interval arrivals;
4. an auditor's planned approach to generated evidence;
5. a sponsor's acceptance of board delegation and of a December deferral policy.
