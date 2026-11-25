# 01: Conventional assumption register

**Pass:** LYR (part 2), with OPS (overhead) and ADV2 challenges. **Data:** [`assumption-register.csv`](../../../data/commercial-opportunity/ai-native-capital-minimization/assumption-register.csv), 52 assumptions: previous study 28, Unbound 18, both 6.

**Integrator conclusions**
- Of 52 conventional assumptions, the pass judged 17 to have a better replacement, 32 unproven and 2 worse. The better replacements are mostly small: December deferral by sponsor policy, EFT by default, lazy charity re-verification, generated evidence.
- **The binding assumptions are not organisational habits.** They are legal and assurance obligations (sponsor reserved authority, OFAC, IRC 4966/4967, SOC 1 and SOC 2 reliance, CNV-GOV-003 three-person release before gate acceptance), the platform engineering floor, and buyer price.
- Three previous-study assumptions are **corrected** in this mission:
  - the $60k/month × 12 build (report 04);
  - ratio-based hiring triggers, which ignored December release capacity (report 06);
  - the 33.8-minute "elimination" scenario, which counted transferred work as eliminated (report 02).
- One previous-study assumption is **strengthened**: productive hours of 1,520 already deduct coordination. The integrated model counts coordination only beyond six pairs (ADV2-013).

> The research-pass content below was produced by a role-separated agent pass from the same model family as the integrator; it is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured (the pass ran it). Figures quoted inside pass sections are the pass's own; where the integrated model differs, the preface says so and the model ([`model/out/results.md`](model/out/results.md)) governs.

## Part 2: conventional assumption register

`assumption-register.csv`: **52 assumptions** (previous study 28, Unbound 18, both 6). Origin: evidence-based estimate 20, organisational habit 10, historical convention 9, economic necessity 7, legal obligation 6. Would exist if designed today: yes 18, partly 31, no 3. Assumes human work that technology could do: yes 12, partly 8.

**Verdicts:** replacement better 17, unproven 32, worse 2 (removing the fractional vCISO; raising queue utilisation), n/a 1.

| Assumption with a replacement judged better | Cost effect of replacement |
|---|---|
| AR-LYR-007: December needs ~3x average daily capacity, met with agency temporary staff ($34-49/h) and contr | lower (5.7 vs 10 ops FTE-equivalents at 5,000 accounts) |
| AR-LYR-008: A separate controller reviews and releases; controller hours are not preparation capacity | same |
| AR-LYR-010: Both SOC 1 Type 2 and SOC 2 Type 2 are required in steady state | lower preparation cost; fees unchanged |
| AR-LYR-018: Founder labour is shown at market (economic) while cash pay is below market | n/a |
| AR-LYR-019: 7.5% contingency on cash opex | similar |
| AR-LYR-022: Compliance consultant $25k/yr for sanctions programme and annual independent review | slightly lower |
| AR-LYR-023: Separate fractional CFO, outsourced bookkeeping and external audit of the company's own stateme | lower ($10-20k) |
| AR-LYR-029: Complex gift handling 12 h (Unbound) / 5 h (previous), now sold on receipt by an intermediary | lower to servicer; fee transferred to fund |
| AR-LYR-030: Checks are 33% of grants | lower ($4 vs $0.30) |
| AR-LYR-031: Scheduled 180-day deep charity review for every recipient | lower (~$1 vs $69 per account-year) |
| AR-LYR-035: Unbound licence = vendor cost at platform scale + 30% markup ($91/fund at 100k funds) | n/a |
| AR-LYR-036: Loaded cost $165k/FTE, 1,600 productive hours, staffing headroom 1.15 | higher cost estimate |
| AR-LYR-040: Customer acquisition $400 per new account (advisor channel) and 15% new accounts per year | n/a |
| AR-LYR-041: December surge: k=3x arrivals, seasonal premium 1.3x, contractor premium 1.3x | lower |
| AR-LYR-043: Insurance $150k, legal $200k and audit $120k base scaling with log(accounts) (Unbound sponsor m | lower for servicer |
| AR-LYR-044: Payment rails are passed through at cost (servicer does not bear them) | same (transfer) |
| AR-LYR-051: Annual manual vendor-assurance review task in release 1 (automated gap tracking deferred) | lower |

**What the register shows.** The conventional assumptions that matter most are not office lines or meetings (small) but: (1) development and operations as separate, sequenced organisations; (2) headcount-ratio step hiring rather than metered workload; (3) one-sponsor exclusivity of deciders; (4) the December bench; (5) per-sponsor onboarding with full parallel run; (6) generated evidence allowed only after auditor reliance; (7) two human approvers per control-relevant change. Items (6) and (7) are where an AI-native design is most constrained and least proven. Legal obligations (sponsor control, §4966 fund-manager status, sanctions, contribution substantiation, retention) and independent assurance are kept in every replacement.
