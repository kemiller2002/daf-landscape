# 04 - Low-cost commercial validation

Status: research (2026-11-26). Track B, agent AB. This is a plan only. **No outreach, spending or contracts were made or authorized** (owner brief). Every stage that involves contacting people needs a separate owner approval, even at $0 cash. DEC-012 adopts the existing plan and its gates. This report keeps every V-1..V-9 pass/fail rule unchanged. Where a cheaper method weakens the evidence, it says so. Register rows: [validation-experiments.csv](data/fragments/AB/validation-experiments.csv).

## 1. The existing budget, by component

| Component | Phase II cost | What the money buys | Cheaper method that keeps the rule | Cash at the cheaper method | Weakens the evidence? |
|---|---|---|---|---|---|
| V-1 win/loss, 5 switchers + ≥5 stayers | $10-30k | Interviewer time, recruiting, incentives, travel | Founder-led structured video interviews from professional networks. Pre-registered script and coding frame; recordings coded by a second coder | $0-2k (+ ~40-60 founder hours, ≈$5-7k economic) | **Somewhat.** Founder interviewer bias and less access to stayers. Mitigation: independent coding, a script that ranks "nothing" first (P3-HYP-AB005) |
| V-2 price test | $20-60k | 5-10 sponsors, structured price exercise | Ask within the V-1/V-6 conversations (Gabor-Granger ladder: $81/$120/$150; $25k subscription). Public 990 bands as priors ($32-129 per DAF-year at iPhi; Ren administration $413-745; Unbound report 13) | $0-1k | **Yes.** Stated willingness to pay is biased upward. The rule stays (≥3 accept ≥$100/account or ≥$25k), but count only answers backed by a **nonbinding expression of interest at a stated price** as a pass. **Revision 2 (P3-CHL-REV1036, P3-CHL-REV2036):** the model's A3 sequence assumes $81 gross per account less a 30% channel share (P3-ASM-AB030), which is below this pass threshold. A V-2 result between $81 and $100 therefore fails V-2 while still matching the A3 input; a pass sits above what A3 assumes. The model keeps A3's base price at $81 and extends the favourable range to $120 (`tornado-sequence-a3.md` shows the effect; in revision 2, $120 lowered the peak from $8.70M to $4.45M, still with no payback). The script should also ask the sponsor to compare its all-in cost: the licence plus the staffed residual work that licensing moves to the sponsor (~$67 per account-year in the event model, [10](10-structural-cost-elimination.md) §3) |
| V-3 public-data replay | $30-80k | Engineering + data | **Mostly done for $0**: Unbound report 14 ran 151,567 Schedule I rows over 20 sponsors (exception 11.2%, reuse 64.4%, effective 4.0%; P3-CLM-AB015). Remaining: change rate across 12 archived BMF releases from the free NCCS archive (SRC-068) plus CSL/OFAC history | $0-1k (compute, storage) | **No** for the rule as written. Limit: recipients above $5k only |
| V-4 authorised export rehearsal | $40-160k | Real incumbent export under NDA, reconciliation | Before a real export: Transitus public-specification adapters on synthetic exports (synthetic operating year, Unbound report 16) prove tool readiness. A real export can come only through a partner or prospect under NDA/DPA | $0 for readiness; $5-25k for the cheapest real export (NDA/DPA review, secure environment) | **Yes, decisively.** Synthetic data cannot show history depth, money tie-out against a real incumbent, or the freeze plan. The rule cannot be met below about $5-25k plus a cooperating sponsor |
| V-5 contract-end calendar | $5-15k | Desk research + confirmation calls | Public notices, 990 vendor payments, DNS/CNAME changes (prior repo methods), using agents | $0 | Desk part: no. "Active evaluation" still needs a contact (founder network, $0, needs approval) |
| V-6 channel-partner conversations (G0 exit) | $5-15k | Founder time, travel | Founder-led, using a public partner map (CF-software vendors, administrators, bank/trust distributors, data layers). Partner economics modelled from the partner's side at $0 | $0-5k; term-sheet legal review $5-15k only once talks reach a term sheet | **No.** The rule (a named partner in term-sheet talks with a pilot customer by month 6) is the same |
| V-7 AI handling-time study | $20-60k | 200 real or realistic exceptions, timed | Internal time study on the synthetic operating year (Unbound report 16; blind sample already generated) | $0-2k | **Yes.** It measures Unbound's own people on synthetic items, not a sponsor's staff. It is acceptable as a design check, not as the V-7 pass |
| V-8 charity evidence API willingness to pay | $10-30k | 10 prospects | Fold into V-1/V-6. Public prices are already known: Candid Charity Check from $2,750, covering IRS and state compliance with time-stamped audit documentation (verified 2026-11-26, P3-SRC-AB010) | $0 | The rule stays (≥3 of 10 at ≥$15k/yr). The bar is about 5.5x the Charity Check entry price, so **expect failure** (P3-CLM-AB020). Run it cheaply or not at all. **Revision 2 (P3-CHL-REV3013):** this row previously also cited Candid's "Eligibility API from $5,000" and put the bar at "3-5.5x". Candid describes that API as "For donation platforms to enable Apple Pay", so it is not a comparator |
| V-9 auditor walkthrough | $0-30k | A nonprofit audit firm reviews the evidence model | Informal conversation through a professional network, with a written evidence-model pack | $0 | **Yes.** An informal view is not reliance. A written position ($5-30k) is needed before a sponsor relies on it |
| Buyer-access line (implicit) | $80-120k | Founder selling, conferences, security and legal responses | Partner-led access; automated security evidence (SBOM, dependency scans, threat model with Tutela); one targeted conference only if V-6 needs it | $0-15k | Lower access to cold buyers. Partner-first makes cold access less important |
| PR #87 gates: licence terms, counsel opinion | $25-150k | Echelon licence terms; payments counsel | Licence: intra-owner draft term sheet, $0-7k. Counsel: a scoped question list at $0, then an opinion only when a partner model is known | $0-7k now; $15-100k later | Deferring is fine. A counsel opinion cannot be replaced, only postponed |
| PR #87 M-06 shadow replay; M-07 engineering spike | $100-300k; $150-450k | Partner data replay; productivity measurement | M-06: public replay done (above). M-07: replaced by a ledger of build hours and cash, started now at $0 (P3-GAP-AB002). **Until that ledger exists, M-07 stays open** and the S2→S3 cash figure is unmeasured | $0 | M-06 still needs real partner data. OD-M-14 records that no design partner is available (P3-CLM-AB017). **Revision 2 (P3-CHL-REV2022, P3-CHL-REV3002):** this cell previously read "moot once Unbound is built, if build hours are ledgered" |

**Totals.** Phase II G0 is $150-350k. At the cheaper methods, the cash for the same G0 tests (V-1, V-2, V-3, V-5, V-6, V-9 and the buyer-access line) is **about $0-24k**. Adding every other cheaper-method cell in the table (V-7 design check, licence term sheet) gives about $0-33k. **Revision 2 (P3-CHL-REV1029):** this total previously read "about $1-25k", which did not match the component cells. The difference is founder time, about 150-300 hours or $20-40k economic, plus weaker evidence on V-2, V-7 and V-9.

## 2. Staged plans

EVOI below means the capital a failed test keeps from being committed, together with a qualitative band for how likely the test is to change the decision. Phase II and this track give the capital at stake:
- lean commercialization from S3: $1.0-1.5M cash base ([02](02-existing-unbound-economics.md); Revision 2: superseded by the model's figures in [16](16-capital-efficient-market-entry.md) §1);
- Phase II's staged path: $6.5M.

No precise probabilities are claimed.

| Tier | Answerable questions | Evidence obtainable | Remaining uncertainty | Decision gate | EVOI | Spend more only if |
|---|---|---|---|---|---|---|
| **$0, desk only (no contact)** | Is the eligibility cost lever real (V-3)? Where are the contract windows (V-5 desk)? Which partners exist, and what would partner economics look like from their side (V-6 desk)? What price bands do public filings show (V-2/V-8 priors)? Does Transitus handle public-spec exports (V-4 readiness)? Synthetic handling times (V-7 design check). Automated security evidence. Pre-registered decision rules | Measured public-data rates; a target list of 30-50 public organizations; a partner map; public price bounds; tool-readiness evidence; SBOM and scan reports | Everything about buyer and partner behaviour; real exports; auditor reliance | **Gate 0:** if V-3 fails (change rate >6% or auto-resolution <20%), drop change-driven re-vetting as a cost lever before talking to anyone | High per dollar. It protects against building on a false cost lever. It cannot answer the thesis | — |
| **$1k** (cash ≤$1k; outreach approved) | V-1 (≥10 interviews), V-6 first conversations, V-9 informal, V-8 folded in | Recorded interviews, coded independently; partner interest; informal auditor view | Price reality; partner terms; real data | **Gate 1:** ≥6 of 10 name product capability as decisive → OD-M-05 supported; stayers rank all hypotheses below "nothing" → wedge falsified; no partner interest at all → pause | **Highest.** V-6 + V-1 decide whether $1-6.5M is spent at all. Band of changing the decision: moderate to high (SEI chose TIFIN; administrators acquire; CHL-084) | V-1/V-6 are encouraging but ambiguous |
| **$5k** | As $1k, plus travel to 2-3 partner meetings and a demo environment on synthetic data (hosting + domain) | A partner sees a working demo; V-2 questions asked with a demo in hand | Signed terms | Partner asks for a term sheet → go to $10k | High | A partner requests a demo or a security questionnaire |
| **$10k** | V-2 with nonbinding EOIs; NDA/DPA templates reviewed; independent coder (contract) for V-1 | EOIs at a stated price; cleaner V-1 evidence | Export feasibility; counsel view; SOC | **Gate 2:** ≥3 EOIs at ≥$100/account or ≥$25k, **and** one named partner in term-sheet talks (V-6 rule) | High | A term sheet requires legal or security evidence |
| **$25k** | Term-sheet legal review; scoped payments/TPSP counsel memo (limited) | Partner term sheet drafted; counsel scoping | SOC 1 need; real export | Term sheet acceptable (share ≤40%, first line with the partner, no exclusivity without minimum volume) | Medium-high | A counsel opinion is needed to sign |
| **$50k** | Full payments counsel opinion ($15-40k); SOC 2 readiness gap ($10-20k); pen test of the demo ($5-15k); formal auditor walkthrough letter (V-9) | Written opinion; readiness report; auditor's written position | Real export; production SOC report | **Gate 3:** counsel finds no licensing barrier; auditor accepts change-driven re-vetting within the 180-day ceiling (DEC-003) | Medium | A partner has a named pilot customer |
| **$100k** | V-4 export rehearsal with the partner's pilot customer under NDA; SOC 2 Type 1 audit fee ($5-25k) and compliance automation ($8-40k/yr) | 100% money tie-out or failure; Type 1 report | Live operation; Type 2; scale economics | **Gate 4 (G1 entry):** V-4 passes; partner signs a pilot | Medium. This is the last spend before the lean commercialization budget | A signed pilot exists |
| **Existing G0 ($150-350k)** | All of the above, plus paid interviews, a conference presence and a buyer-access line | Stronger stated-preference evidence; more cold buyer access | Same as $100k | Same gates | **Lower marginal EVOI.** Most of the decision value is captured by $10k | Only if partner-first fails and direct access to cold buyers becomes necessary |

## 3. What can be validated for $0

Without any contact:
- V-3 in full;
- the desk layer of V-5;
- the desk layer of V-6 (partner map and partner-side economics);
- public price bounds for V-2 and V-8;
- V-4 tool readiness;
- a V-7 design check;
- automated security evidence (SBOM, scans, threat model);
- the existing-Unbound cost model (this track).

None of these answers whether anyone will buy. **The thesis gates (V-1, V-6) cost about $0-1k in cash but need owner-approved outreach and founder time.** That is the true price of meaningful validation: an approval, not a budget.

## 4. Conditions that genuinely require more spending

1. A real incumbent export for V-4: NDA/DPA, a secure environment and a cooperating sponsor.
2. A written counsel opinion on payments and Nacha TPSP status, and state charitable-solicitation exposure (CHL-037, CHL-043).
3. An auditor's written position before any sponsor relies on change-driven re-vetting (V-9; DEC-003 preserves the 180-day validity ceiling).
4. A SOC 2 Type 1/Type 2 report once a partner's procurement asks for it.
5. Insurance binding at a signed term sheet. Indicative quotes can be gathered first at $0.
6. Real-staff time studies (V-7) through a partner's pilot customer.

## 5. Recommended ladder

Run the $0 tier now; the cash cost is nil and it needs no approval. Ask the owner to approve founder-led outreach at the $1k tier, with pre-registered rules. Move up a tier only when the next gate's trigger occurs. The existing G0 budget ($150-350k) becomes a ceiling, not a plan (P3-DEC-AB002).
