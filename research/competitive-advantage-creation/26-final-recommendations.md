# 26 - Final recommendations

Status: research (2026-11-26). This report gives the integrator's answers to the owner's twenty executive questions, after two adversarial review rounds (150 challenges; [20](20-adversarial-review.md)) and model revision 3 ([18](18-economic-model-methodology.md)).

**How to read the figures:**
- Every figure is conditional on labelled assumption ranges. Nothing is measured.
- Figures are favourable / base / adverse unless stated. "Governing" means the configuration today's ratified requirements imply: Echelon performs the 180-day human deep review (M1), on demand.
- Proposed decisions are P3-DEC-. They are not approved and are listed in [25](25-executive-decision-register.md).
- Research agents, reviewers and integrator are the same model family. Nothing here is independent assurance.

## Post-ratification update (2026-11-27)

After this package was written, the owner ratified the Stage I requirements (daf-landscape #93; unbound #22, merged). The ratification resolved **OD-CDD-02**: renewal triggered by detected changes, within the 180-day ceiling, with evidence-freshness checks and targeted review. This changes how the figures below should be read.

- **The governing registry configuration is now M5, not M1 performed by Echelon.** The revision-3 tables already show M5. The relevant figures are:
  - cash to first invoice from a completed Unbound: $371k / $1.64M / $5.57M;
  - the partner-book sequence pays back at month 80, on a peak of about $2.60M;
  - single-sponsor break-even is about 3,169 accounts, or about 13,335 across a partner's book ([16](16-capital-efficient-market-entry.md) §1b).
- **M1 results are superseded as the governing case.** Results where Echelon performs the full M1 deep review now apply only if renewals revert to manual review.
- **Who performs the deep review matters much less.** It remains open as Unbound OD-CDD-06 / P3-DEC-MOD005. While change-driven renewal holds, the zero-based package finds it barely matters. If renewals revert to manual and Echelon performs them, it adds about $210k a year at 10 customers.
- **The zero-based economics package** (daf-landscape #95, `research/competitive-advantage-creation/zero-based-economics/`) rebuilds costs from obligation, workload and capacity triggers. It replaces the Phase II fixed costs carried in this package's capital-state and shared-infrastructure inputs; see its report 08. Its results are lower than revision 3:
  - licensing at about $202k a year cash for the first customer and about $37k for each additional customer;
  - minimum credible licensing price of about $40-55 per account;
  - deepest cumulative deficit of $0.20-0.76M, depending on customer mix.
  - Where the two packages differ, #95's trigger-justified ledger supersedes this package's cost inputs. This package's sequencing, demand and kill-rule findings stand.
- **The decision is unchanged:** validate first, and open the DAF cost center only after the gate passes.

## The answer in one paragraph

A viable DAF technology business without outside capital is **not shown** on present evidence. It is also not ruled out. Its viability turns on three facts nobody has yet observed, and all three can be tested for little or no cash before any DAF cost center opens:

1. **Who performs and pays for the 180-day charity deep review under licensing** (P3-DEC-MOD005, Unbound OD-CDD-02).
2. **Whether a channel partner will license Unbound for its whole book of sponsors**, rather than Echelon selling to individual large sponsors.
3. **What net price per account such a partner will pay.**

If the sponsor performs the deep review, or automated renewal is allowed, the partner-book route pays back in the base case: peak cash about $2.4-2.6M, payback month 76-80 ([16](16-capital-efficient-market-entry.md) §1b). If Echelon must perform every deep review itself, no route pays back. No route beats doing nothing under the kill rule until a named partner exists. So the recommendation is to **validate first and spend nothing DAF-specific until the gate is passed** (P3-DEC-MOD003).

## Answers to the executive questions

**1. Minimum incremental cash to commercialize an already completed Unbound?**
- **To the first invoice from a referenceable customer:** $384k / $1.83M / $6.63M under the governing configuration. It falls to $1.63-1.64M base if the sponsor performs the deep review or automated renewal is allowed ([16](16-capital-efficient-market-entry.md) §1).
- **The irreducible floor** is funded obligations, not build: the Nacha third-party-provider audit and fraud monitoring, operating SOC 2 controls, insurance, and a realistic first conversion.
- **To self-sufficiency:** only the partner-book route reaches it in the base case, at a peak of about $2.4-2.6M, and only under the review allocations above.
- **Against Phase II:** Phase II's $6.5M overstated the build; its own capital route held about $1M of double counting ([03](03-capital-requirements-reconstruction.md)). The lean figures first produced in Phase III ($1.0M to first invoice, $1.24M peak) understated the funded obligations.

**2. Fully loaded economic cost?** To first invoice: $702k / $2.57M / $8.92M (governing). Fully loaded cost runs about 1.4-2 times cash, mostly because the founder's time is counted at market rate even when it is unpaid ([02](02-existing-unbound-economics.md), [16](16-capital-efficient-market-entry.md) §2).

**3. Can meaningful commercial validation occur without spending money?** Partly.
- **At $0:**
  - the public-data replay test (V-3) can run against its unchanged pass rule;
  - the desk layers of V-5 and V-6 can be done;
  - public price bounds can be gathered;
  - synthetic migration rehearsals can show Transitus readiness;
  - automated security evidence can be collected;
  - the IRS archive can be started.
- **About $10k plus founder time** captures most of the decision value: founder-led V-1 and V-6, and V-2 with non-binding price expressions.
- **What needs your approval:** any contact with buyers or partners, even when it costs nothing.
- **What stays expensive:** V-4 (an authorised incumbent export) cannot meet its rule below about $5-25k plus a cooperating sponsor ([04](04-low-cost-commercial-validation.md), [23](23-commercial-validation-roadmap.md)).

**4. Can Echelon Foundry establish a viable business without outside investment?** Not shown.
- Outside money would only change who funds a loss in every configuration where Echelon performs the deep review.
- Where the partner-book route pays back, the peak of about $2.4-2.6M has to be funded from your capacity, which is unknown (P3-GAP-MOD001), or from customer billing terms.
- Investment is not justified before the gate (P3-CLM-MOD012).

**5. Cheapest credible route to first revenue?** A channel partner licensing Unbound as a module inside its existing offering, paid per account across its book, with implementation fees billed to the partner or sponsor.
- The narrow products are not credible routes: component licences earn $0-50k a year with negative margin ([09](09-independent-component-commercialization.md)).
- Charity-intelligence subscriptions sit far below Candid's public prices ([11](11-continuous-charity-intelligence.md)).
- Paid migration assessments are a sales cost, not revenue ([06](06-customer-acquisition-without-displacement.md)).

**6. Which institutions are most likely to adopt a new DAF offering without switching providers?**
- **Most likely:** university and hospital foundations of $100M+ with no DAF of their own. Only 99 of 3,056 show any sign of one ([05](05-untapped-institutional-markets.md)).
- **Also:** institutions whose program a community foundation or national sponsor could host; faith foundations; credit-union league foundations, as a channel only.
- **Not candidates:** banks, RIAs, trust companies and fintechs cannot sponsor DAFs themselves.
- **The catch:** these adopters are small. The 134 university and hospital sponsors in the 2024 panel hold 2,882 DAF accounts between them. They are adoption and reference routes, not revenue routes (P3-DEC-CD001, P3-DEC-CE002).

**7. Which Unbound advantages would incumbents struggle to replicate?** None is structural today ([07](07-architectural-competitive-advantages.md); 0 of 22 candidates are architectural, organizational, distribution or network advantages). The strongest candidates, all copyable in about 6-30 months and none built yet:
- replayable, provenance-bound eligibility decisions;
- migrations proven by full reconciliation, which become a learning economy if migrations cluster on one source (DEC-007);
- a low cost floor from the single-application architecture and shared infrastructure, which helps survive a price war but does not deter one.

**8. Which proposed advantages are ordinary software capabilities?** Eight:
- append-only history;
- deterministic controls;
- configuration-driven onboarding;
- sponsor segregation;
- API-mediated operations;
- AI-readable documentation;
- event-level cost measurement;
- durable execution.

Build these to a basic standard and do not market them as differentiators (P3-DEC-EK003).

**9. Can charity intelligence become an independent commercial asset?** Not on current evidence.
- Candid's Charity Check is listed from $2,750 a year.
- Only the public-domain layer can be redistributed (DEC-004).
- A standalone service adds about $197k a year of overhead.
- Keep it as an Unbound component and a possible low-price partner add-on (P3-DEC-HI003). Its real value is cost: shared public-data monitoring is about 96% of the registry run cost, so the shared layer is cheap per added sponsor. Sponsor-specific deep reviews are counted per sponsor and are not shared (revision 3), so the full marginal cost depends on who performs them, P3-DEC-MOD005 ([11](11-continuous-charity-intelligence.md)).

**10. Can Transitus become a customer acquisition mechanism?** As a pre-sales tool, yes in principle; as revenue, no. The pre-contract assessment tiers (Transitus T0/T1) can show a sponsor its migration risk without data leaving the sponsor. Transitus has no code, though, and its phase-1 rules block the cheap reusable-package rate until real exports are reconciled. The kill rule does not stop it (OD-P3-02).

**11. Which Echelon Foundry components could generate early revenue?** Only the released developer tools (Strata, Limen, Forma and Folio, Aegis), on self-serve, no-SLA licences, at about $0-50k a year by month 24. That does not fund Unbound.
- **First, a licensing decision:** nearly every component is under PolyForm Noncommercial (P3-CLM-FGJ002; P3-DEC-FGJ001).
- **Product names that mislead:** Vigila is a task organizer, not audit logging, and echelon-assurance is at design stage ([09](09-independent-component-commercialization.md)).

**12. Which adjacent financial industries justify investigation?**
- **Investigate:** charitable gift administration (gift annuities, remainder trusts, pooled income funds), desk research only after a live Unbound pilot; and fiscal sponsorship, $0 desk research now.
- **Integrate, don't build:** grants and scholarships.
- **Treat as buyers of charity evidence, not markets:** employee giving platforms.
- **Do not pursue:** trust administration, escrow, custodial accounting and private-foundation administration ([08](08-adjacent-financial-industries.md)).

**13. What work can be eliminated rather than automated?** Of about 183 conventional minutes per account-year ([10](10-structural-cost-elimination.md)):
- about 37 are eliminated outright, through validated recommendation forms, contribution intents that carry references, verified destinations, canonical identifiers and pre-validated policy rules;
- about 82 are automated;
- about 9 are sped up by AI.

Transferred work is not counted as eliminated. Technology-only licensing moves about 53 minutes per account to the sponsor.

**14. What costs cannot realistically be eliminated?**
- The sponsor's reserved authority and section 4967 review.
- Sanctions-match disposition and reporting, and identity proofing.
- Appraisals, succession and fraud monitoring.
- First-time verification of recipients not on IRS lists.
- Audit preparation, until an auditor accepts continuous evidence (V-9).
- The Nacha audit, SOC control operations and insurance.
- A named eligibility owner, plus counsel.

**15. What is the smallest economically viable DAF program?**
- **For the sponsor** ([05](05-untapped-institutional-markets.md)), at a $133k average balance and 0.6-1.5% fees:
  - hosted by an existing sponsor: about 6-19 accounts;
  - an existing charity running its own: about 15-46 accounts;
  - a new sponsor: about 52-164 accounts.
- **For Echelon**, no single small program is viable. A program paying $10-25k a year never repays the cost of winning it. The viable unit is a partner's book: break-even is about 12,500-13,300 accounts across a partner's book, or about 3,100-3,200 accounts for a single sponsor, when the sponsor performs the deep review or automated renewal is allowed ([16](16-capital-efficient-market-entry.md) §1b).

**16. Does partner-first distribution remain the best entry strategy?** Yes, and more narrowly than Phase II framed it.
- The partner's whole book is the customer. Echelon does not sell to individual large sponsors through the partner: only about 10 plausible sponsors exceed 5,291 accounts.
- Partner-first trades margin for access more than it cuts acquisition cost ([12](12-institutional-distribution.md)).
- It only works under protective terms (P3-DEC-EK002, P3-DEC-FGJ003): non-exclusive; capped, declining revenue share; Echelon keeps the IP and data formats (OD-P3-01); termination if the partner changes control; and sponsors can keep running Unbound if the partner leaves.

**17. How should Echelon Foundry respond to aggressive incumbent competition?**
- Do not match price below the walk-away floor for the cost base actually achieved (P3-DEC-EK001; about $28-30 per account-year on the lean base).
- Compete on what is measured: published migration outcomes and replayable eligibility evidence.
- Keep a second partner, and the change-of-control protections, so a partner acquisition does not end the business ([13](13-incumbent-response-model.md)).
- Under a 30% price cut, licensing at Phase II's cost base fails. Only the lean cost base survives.

**18. What should we deliberately avoid building?**
- A custodial administrator (DEC-002).
- A proprietary charity payment network or charity portal (DEC-009).
- Standalone charity-intelligence or compliance products (P3-DEC-HI003).
- Vendor-specific migration packages before an authorised sample (DEC-011).
- Adjacent-industry modules before a live customer asks.
- Further DAF-specific Unbound build before the gate (P3-DEC-MOD003).
- Commercial versions of the components on the "do not commercialize now" list (P3-DEC-FGJ002).

**19. What evidence would cause us to abandon or materially change the strategy?** The conditions are in [21](21-commercial-thesis-invalidation.md). The most decisive:
- **Counsel or the auditor require Echelon to perform full human review** of every charity on behalf of every sponsor. This combines OD-CDD-02, P3-DEC-MOD005 and V-9.
- **No partner will license for its book**, or every engaged partner demands exclusivity, a right of first refusal, an acquisition option or more than 50% of revenue.
- **The net price per account is below the walk-away floor**, or the reachable book is under about 12,000 accounts.
- **No named partner** within six months of the cost center opening (the DEC-008 kill rule; OD-P3-03/04).
- **Your funding capacity is below the peak** of the surviving route.

**20. What should Echelon Foundry do next?** In order, all before any DAF cost center opens:
1. **Decide P3-DEC-MOD005 and OD-CDD-02:** who performs the deep review, and whether automated renewal is allowed. They set the threshold for the other gates.
2. **Approve founder-led, no-cost outreach** for V-6, partner conversations about licensing a whole book, and V-1/V-2, with pre-registered pass rules ([23](23-commercial-validation-roadmap.md)).
3. **Run the $0 validations now:** V-3 replay; IRS and sanctions archiving (P3-DEC-HI004); the V-9 preparation pack for an auditor; and the desk layer of V-5.
4. **Set the component licensing policy** (P3-DEC-FGJ001) and fix the copyright-holder TODO for counsel (OD-P3-01).
5. **Settle the remaining kill-rule details** (P3-DEC-CE001, P3-DEC-MOD001): whether completing Unbound counts toward the cost center, and whether the month-24 pilot clock also starts at the cost-center month.
6. **Ratify, amend or reject the Stage I proposed requirements** (Unbound OD-CDD-01..05; Transitus OD-TRN-P3-01, OQ-17).
7. **Recommended next initiative:** "Phase IV: gate evidence". Run the approved validation ladder and record results against the pass rules. Open the DAF cost center only if a named partner with a whole-book term sheet, a price at or above the walk-away floor, and a decided review allocation all exist.

## Cross-repository proposals

All proposals are listed in [24](24-cross-repository-implications.md); none is approved. The most material:

| Repository | Proposal |
|---|---|
| Unbound | Make the deep-review performer an explicit sponsor-policy setting (UNB-CDD-CIV-010; OD-CDD-02) and record its economic consequence |
| Unbound | Continuity on partner exit, so sponsors keep running Unbound without migration |
| Unbound | The TPSP base cost and the Rev. Proc. 2026-8 group-exemption change in 2027 |
| Transitus | Measure conversion hours and package reuse, because they set the implementation rate |
| Organization | The cost-center definition, the funding-capacity statement and the build gate |
