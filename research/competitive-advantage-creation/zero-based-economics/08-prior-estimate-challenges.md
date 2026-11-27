# 08. Prior estimates, reconstructed and challenged

Each prior estimate is rebuilt from its Phase II source and compared with a zero-based figure. Where Phase II defined a configuration, the comparison uses the same one: five sponsors × 2,000 accounts at $250k per account and 9 grants per account (mix `prior-5x2000`).

- **Register:** [`prior-estimates.csv`](data/inputs/prior-estimates.csv).
- **Computed comparables:** [`prior-estimates-revised.csv`](data/outputs/prior-estimates-revised.csv).
- **Ranges:** "low" means every input at its favourable end and "high" every input at its adverse end, so these are corners, not percentiles.

**The revised estimates were not forced lower.** Two priors survive close to intact: the registry cost and the pilot budget.

## PRI-01 — $2.5M annual administration fixed cost
- **Original assumptions:**
  - Phase II MD-5 fixed cost: a standing staffed team of ~$1.5M plus a $0.7M platform from PR #87, plus AI evaluation and governance, plus the revision-2 AI-oversight uplift.
  - Total with variable cost at 10k accounts: $2.5M + $147 × 10k = **$3.97M**.
- **Evidence quality:** inference built on assumptions. No line item was derived from an obligation.
- **Applicable obligations:**
  - SOC 1 Type II before the first staffed client;
  - two-deep on-call;
  - non-author change approval;
  - business-day operations continuity;
  - crime insurance.
- **Unnecessary conventional assumptions:** an organisation sized before any customer; AI oversight as a separate cost centre; a platform quoted rather than priced.
- **Replacement mechanisms:**
  - founder capacity first;
  - workload-derived staffing;
  - coverage through retainers until hiring is cheaper;
  - priced infrastructure (about $6k a year rather than $0.7M);
  - sponsor-reserved decisions left with the sponsor.
- **Revised:** total cash **$0.94M** ($0.20M–4.2M) at 5 × 2,000 accounts. Fully loaded: $1.29M ($0.43M–5.1M).
- **Remaining uncertainty:** exception intensity (unmeasured) and founder availability. The adverse corner exceeds the prior.

## PRI-02 — $1.8M annual licensing fixed cost
- **Original assumptions:** platform team $0.7–1.8M + CEO/CTO + SOC 2, pen test and insurance + sales + one support FTE. Total at 10k accounts: **$2.11M**.
- **Evidence quality:** assumption.
- **Applicable obligations:** SOC 2, pen test, insurance, change control, on-call; SOC 1 from the third customer.
- **Unnecessary conventional assumptions:** salaried executive and sales roles; a conventionally sized platform team.
- **Replacement mechanisms:** founder-held management, contracted reviewers and secondary on-call, workload-derived engineering.
- **Revised:** **$0.39M** cash ($0.08M–1.6M); fully loaded $0.75M ($0.29M–2.5M).
- **Remaining uncertainty:** maintenance hours, and whether buyers accept a vendor of one founder plus contractors. That is a commercial risk, not a cost.

## PRI-03 — $147 annual variable cost per account
- **Original assumptions:**
  - 53 human minutes per account-year at loaded rates (÷ 0.75 utilisation);
  - $25 per account of infrastructure (PAR-011 placeholder);
  - AI, external and failure costs.
- **Evidence quality:** inference on unmeasured touch rates. The $25 infrastructure figure is contradicted about seven-fold by the servicing-economics cloud line.
- **Applicable obligations:** exception preparation, reconciliation and donor support under full service.
- **Unnecessary conventional assumptions:** the infrastructure placeholder; all event minutes falling on the vendor even where the sponsor decides.
- **Replacement mechanisms:**
  - priced infrastructure (about $0.3–0.6 per account at scale);
  - sponsor-reserved work borne by the sponsor;
  - exception intensity varied independently.
- **Revised:** slope between 5 and 10 prior sponsors is **$64 per account** ($15–326) for Echelon Foundry, and **$94** including sponsor-borne work. This follows review finding ADV-A-09: the earlier $98 figure wrongly included first-customer step costs.
- **Remaining uncertainty:** exception intensity and donor contact rates. The adverse corner is twice the prior.

## PRI-04 — $90–170k annual charity registry cost
- **Original assumptions:** connector maintenance (400 h), part-FTE stewardship and optional licensed data, for a single sponsor (Phase II report 05).
- **Evidence quality:** inference.
- **Applicable obligations:** freshness limits (45 days for IRS, 24 h for OFAC) and the 180-day ceiling, using free federal sources.
- **Unnecessary conventional assumptions:** a dedicated stewardship FTE; licensed data treated as required.
- **Replacement mechanisms:** change-driven review; pipeline stewardship as engineering hours (80/150/300 h); licensed data discretionary.
- **Revised:** **$89k** ($22k–476k), including stewardship, as review finding ADV-A-12 required. **The prior is confirmed.**
- **Remaining uncertainty:**
  - ambiguous-case rates;
  - whether counsel adds screening lists;
  - the adverse corner, which shows manual-review exposure.

## PRI-05 — $125k customer acquisition cost
- **Original assumptions:** a conventional enterprise sales motion (PAR-023, untested, CLM-026).
- **Evidence quality:** untested assumption.
- **Applicable obligations:** none legal; procurement and security review are contractual.
- **Unnecessary conventional assumptions:** dedicated sales staff and a marketing budget.
- **Replacement mechanisms:** founder- and partner-led sales measured in hours. That is 240 h per won customer at a 25% win rate, plus contract counsel and travel.
- **Revised:** **$37k** ($14k–97k), mostly founder time. It is a cash cost only once founder capacity is exhausted.
- **Remaining uncertainty:** sales-cycle length and conversion are unknown. Founder hours, not cash, are the real constraint.

## PRI-06 — $1.94M development cost
- **Original assumptions:** a salaried team building the minimum product over 12–18 months (PR #87 build $1.1–2.4M).
- **Evidence quality:** inference.
- **Applicable obligations:**
  - independent review of control modules;
  - pre-launch pen test;
  - SOC 2 Type I readiness;
  - CPA ledger review;
  - counsel;
  - DR rehearsal.
- **Unnecessary conventional assumptions:** a salaried team; all effort treated as cash.
- **Replacement mechanisms:** the founder builds with AI assistance (noncash) and buys only independent assurance (cash).
- **Revised:** **$108k cash** ($47k–230k) plus **7,560 founder hours** (3,980–13,520). That is **$1.04M fully loaded** ($0.43M–2.33M).
- **Remaining uncertainty:** AI-assisted productivity is unmeasured. At 1,200 h a year the build takes about six years of founder time, so calendar time is the binding constraint ([09](09-cost-to-production-qualification.md)).

## PRI-07 — $150–350k commercial validation budget
- **Original assumptions:** a paid research and validation programme over six months.
- **Evidence quality:** assumption.
- **Applicable obligations:** none.
- **Unnecessary conventional assumptions:** paid research.
- **Replacement mechanisms:** founder-led interviews and partner discovery (400 h). None of this is authorised.
- **Revised:** **$15k cash**; $113k fully loaded.
- **Remaining uncertainty:** whether founder-only validation is credible to partners.

## PRI-08 — $1.0–1.5M partner pilot budget (cumulative)
- **Original assumptions:** capital to the first referenceable paying customer, including build, SOC 2 Type 1 and sales over 12–24 months.
- **Evidence quality:** inference.
- **Applicable obligations:** SOC 2, insurance, pen test, and onboarding before revenue.
- **Unnecessary conventional assumptions:** a staffed team burning cash through the sales cycle.
- **Replacement mechanisms:** the zero-customer burn of a running platform, go-live costs, and the deepest cumulative deficit along a growth path.
- **Revised:** like-for-like, this is validation + build cash + the deepest deficit to self-sustaining operation (review finding ADV-A-01). For licensing to mixed sponsors adding two customers a year, that is **$0.89M** ($0.08M at the favourable corner; never recovers at the adverse one). Excluding build it is **$0.76M**. **The prior range survives in the base case**, and the earlier "$133k" comparison was wrong.
- **Remaining uncertainty:** the pre-revenue period (6–24 months) and the size of the first customer. With a regional anchor first, the deficit falls to about $0.20M.
