# Strategic synthesis: what the DAF evidence actually supports (A–G)

**Date:** 2026-11-14. **Status:** decision-oriented synthesis of this mission's workstreams and the prior repository. Claims carry an EDF claim-and-confidence label (`suggestive`, `unsupported`, `contradicted`, `internal-demonstration`; Low → High).

**Validation:** every factual anchor has been through independent validation (wave 1) or red-team review (waves 2A/2B). The results are in [`validation-register.csv`](../../data/mission-2026-11-14/validation-register.csv) and in [`red-team-wave2a-ai-and-entrant.md`](red-team-wave2a-ai-and-entrant.md) / [`red-team-wave2b-graph-data-incentives.md`](red-team-wave2b-graph-data-incentives.md). Where red-team findings changed a statement, the change is marked **[RT]**.

**Method:**
- **Clarity** governs how much reasoning each claim justifies (posture, reconsideration criteria, admissibility).
- **EDF** is used only where an outcome has actually been observed.
- Both are applied as pinned in [clarity-edf-application-guide.md](clarity-edf-application-guide.md).
- Scenario numbers from the AI-economics and entrant models are labelled **[S]**. They illustrate the logic and are not estimates of any firm's costs.

---

## A. What the DAF industry believes that may be wrong

| # | Widely repeated belief | Origin of the belief | What the evidence shows | State / confidence |
|---|---|---|---|---|
| A1 | "There are ~3.6 million DAF accounts, so the market is millions of donors to serve with software." | NPT/DAFRC headline account counts; vendor TAM decks | 79.5% of FY2024 accounts (2.85m of 3.59m) sit in 22 donation-processor sponsors holding 0.9% of assets. One processor (Givinga Foundation) reports 1.42m accounts holding $1.95m. Traditional invested accounts are **at most 737k**. ([regulation-market-structure-portability.md](regulation-market-structure-portability.md); [quantitative datasets](quantitative-datasets-and-data-dictionary.md)) | contradicted as stated; High on figures |
| A2 | "DAFs pay out ~25% a year, so warehousing is a myth." | DAFRC/NPT aggregate payout rates, used by defenders | The aggregate (23.7–28.4%, FY2020–24) is real but dominated by the largest nationals. The **median sponsor** with ≥$1m assets pays out about 11–12.5%, and **19–24% of such sponsors pay out under 5%**. Fund-level payout is not public. Both "myth" and "warehousing epidemic" exceed the evidence. | suggestive; Medium-High on distribution, Low on cause |
| A3 | "The DAF market is dominated by three commercial giants." | Fidelity/Schwab/Vanguard brand salience | On DAFRC's FY2024 sponsor panel, assets are only moderately concentrated: CR3 45.5%, HHI ≈ 830 (Fidelity 20.2%). Concentration rises sharply inside *national* sponsors (CR3 63.2%, HHI ≈ 1,566). **[RT] Wave 2B adjudication:** the graph workstream's CR3 ≈ 58% / HHI ≈ 1,289 divided June-2025 sponsor values by a DAFRC total holding the same sponsors at June-2024 values, inflating CR3 by about 12 points; 45.5% / 830 is correct. "Dominance" depends on which market is meant (assets, administration, software, custody or distribution). | partially contradicted; Medium |
| A4 | "Ren powers over half of US DAF assets." | Ren marketing (">60%", "approximately half / $175bn+", "$200bn") | Sponsors with public Ren evidence (RCF, AEF, MS GIFT, BofA CGF) hold about 8.7% of FY2024 DAF assets. **[RT]** Period-aligned, the four largest sponsors hold about 52%, leaving at most about 48% for all others. The "$200bn" figure covers "donor-advised funds and other charitable assets", so it is not a DAF share. Reaching "60%+" requires Ren to count NPT (via the Stellar/iPhi lineage, unverified) plus nearly all other sponsors. | unsupported on public evidence (disputed, not disproven); Medium |
| A5 | "Grant approval is the bottleneck, and AI can automate it." | Vendor positioning (Ren "instant approval", TIFIN AI) | Observable non-standard grants (foreign, fiscal-sponsor, non-501(c)(3)) are about 2.5–3% of dollars at large nationals and far less by count. Grants to listed public charities are excepted from §4966, and grantors may rely on IRS status data. The labor pool is thin: about $16k/yr at a 48,744-grant sponsor and about $975k/yr at Fidelity scale **[S]**. | suggestive; Medium |
| A6 | "Sponsors must review every grant manually because of legal liability." | Sponsor operating norms | Statutory liability is narrow for listed public charities. Blanket manual review is classified **mixed**. Edge-case review is structural. A counter-signal: sponsors exercised discretion beyond tax exposure in 2026. **[RT] confirmed:** the California AG's 2026-05-22 release records the April 21, 2026 SPLC indictment and names Fidelity Charitable, Vanguard Charitable and DAFgiving360 as having restricted grants. Whether the holds persist is unknown. **[RT]** The "leaning habit" qualifier is dropped; classification is **mixed**. | suggestive; Medium |
| A7 | "Paper checks persist because the law or sponsors require them." | Folk explanation | No rule requires checks. Fidelity Charitable "does not currently require EFT", calls EFT "up to 9x faster", says it is "transitioning grant payments to EFT" under a "digital-first policy", and asks nonprofits to change board policies that prohibit EFT. Chariot (Mar 2026) reports about 67% of Fidelity grants already by EFT. Chariot's claim of an electronic-only date of July 2026 is **not confirmed** by Fidelity's FAQ. **[RT]** The move is under way but not mandated. | mixed, leaning habit; Medium |
| A8 | "Donors can easily move a DAF if they're unhappy." | Sponsor marketing of inbound "closing grants" | None of 12 sponsors reviewed publishes an outbound transfer policy. Transfers are usually liquidated to cash, take 10 business days to 4 weeks, and carry **no grant-history portability** (AEF's own migration kept two years). About $7.5bn moved sponsor-to-sponsor in 2024, roughly 12% of grants. The legal right exists, but the operational friction is real. | suggestive; Medium-High |
| A9 | "The 2023 proposed DAF regulations will be finalized soon." | Practitioner commentary 2023–24 | Neither final nor withdrawn as of 2026-11-14. The 2026–27 Priority Guidance Plan reframes the project as "guidance under §§4966 and 6033 regarding certain DAF arrangements". California AB 1712, often cited as a DAF reporting law, **failed in 2020**. | High (Federal Register query) |
| A10 | "Challengers are cheaper by design." | Early Daffy/Charityvest positioning | Challengers repriced upmarket: Charityvest went from "zero fees" (2020) to 0.45% cap (2022) to 0.60% on the first $500k (2026), and Daffy added a $40 feature-triggered tier. Incumbents meanwhile removed minimums (Fidelity, Schwab 2020). The price gap has narrowed from both sides. | suggestive; Medium |

**Clarity reading:** most wrong beliefs come from **denominator substitution**: accounts for donors, aggregate for median, administered assets for vendor share, all grants for grants needing judgment. A false-precision flag (Constitution admissibility) applies to any TAM, payout or share claim that does not name its denominator.

---

## B. What AI actually changes

**Superficial productivity (speeds work up; does not change who is accountable or what work exists):** drafting donor and adviser communications, grant-status answers, document extraction for complex assets, reconciliation-break triage, and proposal generation. Incumbents already market these.

**Structural changes (alter operating economics only when paired with redesign):**
1. **Policy-as-code.** Sponsor grant policy becomes versioned, executable and back-testable against historical grants, so a final §4966 guidance change can be re-run across the book.
2. **Continuous eligibility monitoring.** Every active payee is checked against BMF/Pub 78/revocation/OFAC refreshes, replacing per-grant lookups. Diligence moves off the grant's critical path.
3. **Exception-only human review.** Each routing decision records which rule or person decided.
4. **Event-sourced ledger.** Grant status becomes one state machine shared by donor, adviser, sponsor and nonprofit, which also makes portability tractable.

**The economic finding [S] (internal-demonstration; the ranking is an artifact of assumptions, the mechanism is reasoned):**
- Applying AI to existing workflows (option C) ranked last of four interventions in all 16 modelled processes under base assumptions. **[RT] Wave 2A showed this ranking is fixed by the inputs:** with manual improvement set at 15% and AI-amenability capped at 0.45, C cannot beat A in any process (that would need amenability > 0.50). P07 non-standard diligence is effectively a tie with conventional automation ($512 apart). The ranking is **not evidence about AI performance**.
- What survives the red team: inference cost (≈$0.45 per heavy document review vs ≈$83 of reviewer time) is immaterial. **[RT] Correction:** QA/re-review intensity decides whether AI value is *positive* (at 25% re-review it is negative everywhere), but the *ranking* is driven by the unsourced amenability and redesign-share assumptions. With zero QA, C still ranks last in 12/16.
- The directional rule "prevent exceptions before automating their handling" rests on reasoning (redesign removes exception classes; AI only shortens handling), not on the model. AI is best placed after redesign, on the residual unstructured tail: complex assets, non-standard grantee diligence, succession documents.

**Market reality:**
- Of 30 AI use cases inventoried, 10 are DAF-direct, and only 2 of those have deployment evidence (a navigation assistant at Fidelity Charitable; a corporate grantmaker's agents on the donor side).
- **No public evidence of AI in sponsor-side approval or eligibility determination.** **[RT] Exception:** Daffy, which operates its own sponsor, announced back-end AI that unifies charity data and "flags issues for review" (2025-04-09; announced only). This is consistent with the flag-only rule below. Bonterra Que was missing from the inventory and has been added to the correction list.
- The agentic frontier is **donor-side**: TIFIN Give's Louise, and Daffy's MCP server exposing `make_donation`. Sponsors will receive agent-originated recommendations before they deploy agents themselves.

**Risk:**
- **Taken unconstrained,** AI creates risk in 13 of 16 failure modes and redistributes it in the other 3.
- **The one rule that turns AI from a risk creator into a risk reducer:** *AI may add a flag, never clear one.* The most dangerous failure is a missed sanctions hit or prohibited benefit, and this rule reduces that risk instead of adding to it.
- **Why this is a category error:** DAF law assigns liability to the sponsor and to knowing fund managers (§§4966, 4967, 4958). "AI approval" therefore misplaces accountability.

**Bottom line (Clarity posture: Guardrail for any AI touching status determination or money; Experimental for donor-facing assistants with spend limits; Fast for drafting):** AI changes DAF economics mainly by making redesign cheaper to specify, test and audit, not by accelerating the inherited workflow. Its economic case is strongest exactly where governance burden is highest (unstructured, judgment-heavy work). That tension, not model capability, is the binding constraint.

---

## C. Where incumbents are vulnerable

| Vulnerability type | Evidence | Who is exposed | Confidence |
|---|---|---|---|
| **Architectural: shared single points of failure** | Several wealth-firm programs use RCF as sponsor and Ren as technology (Edward Jones, Ameriprise, RBC, LPL/Commonwealth, Northwestern Mutual, UBS (one of four sponsors), SEI, Fisher, MDRT). Ren DFX also fronts MS GIFT, BofA CGF and AEF. Ren-owned iPhi still serves the Cleveland Foundation and ImpactAssets. One RCF–Ren contract and one portal family underpin many "independent" brands. | Ren/RCF and every channel on them | Medium-High (edges confirmed; contract terms private) |
| **Economic: fee-share pass-through** | RCF pays Ren 98% of individual-fundholder admin-fee revenue ($19.23m FY2024). The sponsor's margin to fund innovation is thin, and the vendor's economics are tied to asset retention rather than service quality. | RCF-type sponsors; Ren's pricing power if a channel re-bids | Medium-High on fact, Low on consequence |
| **Organizational: private-equity roll-ups** | Foundation Source (GTCR 2023): new CEO in six days, four acquisitions in about 17 months. Ren: Bain/Valeas 2023, Great Hill 2025. Integration debt and metric drift are visible (Ren's dates, scale claims, SOC 2 type). | Foundation Source, Ren customers | Medium on sequence; customer effects unknown |
| **Distribution: bundles can be unbundled** | SEI now runs **two** competing stacks (RCF/Ren SEI Giving Fund and GiveClear/TIFIN SEI Charitable Fund). A large channel can multi-source, so the channel is the buyer, not the captive. | Ren, TIFIN | Medium |
| **Customer experience: history and portability** | No outbound transfer policies; no history portability; separate logins (Edward Jones portal is distinct from the brokerage login); AEF kept two years of history after migration. | All sponsors on legacy portals | Medium |
| **Payments: fragmented rails** | Four rails (Fidelity EFT/Stripe, PayPal Grant Payments, Ren Rapid Disbursement, Chariot). Only one observed switch (Charityvest PayPal→Chariot). None of the three largest sponsors is a documented Chariot user. | Nonprofits bear the reconciliation cost; Chariot is gaining small and mid-size platforms | Medium |
| **Assurance credibility** | Ren's SOC 2 type stated as Type 2 (Jul 2025) then Type 1 (Apr 2026) in vendor boilerplate. No report seen. | Ren and dependent sponsors | Medium (statement inconsistency confirmed; underlying report unknown) |

**Where incumbents are *not* vulnerable (bounded truth):**
- The three affiliate-linked nationals (about 39% of period-aligned FY2024 assets **[RT]**; Vanguard is a hybrid: Vanguard Group is paid about a $4.0m service fee and the admin fee funds Vanguard Charitable's own operations) combine sponsor brand, custody, investment funds and administration under one corporate parent. Their technology is not the moat; the parent relationship is.
- Community foundations' long tail is anchored by Foundant CommunitySuite (claims 700+ CFs, 99% renewal) and is a partly separate market.

---

## D. What new entrants should avoid building

| Component | Avoid building because… | Instead | Evidence |
|---|---|---|---|
| A new sponsoring charity | Legal control and liability attach to the sponsor; trust is brand-borne; it takes years to accumulate | Partner with a sponsor-of-record (Endaoment publishes API tiers; white-label sponsors RCF, GiveClear, Charityvest, NPT, AEF exist) | entrant simulation; vendor graph |
| Custody and brokerage | Licensed, capital-intensive, insolvency risk | Custodian partners (Altruist, Schwab, Fidelity, BNY named on Endaoment's page) | entrant simulation [P1] |
| Payment rails / money transmission | Licensed; Chariot (Column N.A. accounts), PayPal Grant Payments and Ren's engine exist | Partner (Chariot Disbursements) or use the sponsor's bank | vendor graph; timelines |
| Charity master data | IRS BMF/Pub 78/revocations/OFAC are free and authoritative; every disclosed eligibility check sources from them | Subscribe and monitor continuously; add Candid only for enrichment | AI economics; breadth |
| A per-grant manual review queue | The labor pool is thin and the legal need is mostly edge-case | Exception-only review with policy-as-code | AI economics; incentives |
| A full system-of-record platform to displace Ren/FS/Give Interactive | About 3–4× the capital of an operating layer (base ≈ $17m vs $5m [S]); switching costs high; channels already multi-source | Integrate with incumbent ledgers; sell modules (eligibility monitor, reconciliation) as APIs | entrant simulation |
| Paper-check workflows and returned-check reconciliation | A process that should not exist; it generates its own exceptions | Electronic-only payee enrollment, with a manual tail for unbanked/foreign grantees | AI economics; incentives |

**Smallest commercially meaningful products** (from the entrant simulation; falsifiable within 6–12 months):
1. **Operating layer:** exception-only grant routing (routine tiers cleared by **deterministic, sponsor-approved rules only**; AI may add flags or evidence but never clear) plus a continuous eligibility monitor for 2–3 independent or community-foundation sponsors. **Signal:** measured exception rate, reviewer minutes and time-to-approve vs baseline. These are the data no incumbent publishes.
   - **[RT] Economic caveat:** on the repository's own parameters, a $120k/yr product needs ≈369k grants/yr from grant-review value alone. Even if it captured all redesign and AI value in scope, it needs ≈76k. Most independent and community-foundation sponsors are below both.
   - So Strategy 3 is a **conditional research probe**, not an unconditional recommendation. It must absorb reconciliation, servicing and monitoring value, sell to vendors or networks rather than single sponsors, or be priced well below $120k.
   - Its "lowest capital" advantage is a headcount assumption: it needs about 42 customers for $5m ARR, against 5 for a full platform.
2. **Modular infrastructure:** an eligibility-monitoring API and a reconciliation API. **Signal:** paid adoption by a platform that already has a sponsor.
3. **Complete platform:** only as S1-lite through a sponsor-of-record partner, after (1) produces data.

**Gating condition:** if sponsors' ledgers sit inside Ren, Foundation Source or Give Interactive systems with no contractual API rights, (1) has nothing to run on. This is the single most important question to answer before committing capital.

---

## E. What becomes more valuable as administration becomes cheaper

Administration is becoming cheaper through shared rails, continuous monitoring and AI-assisted servicing. Scarcity then moves to the assets that cannot be copied:

1. **Distribution access (most valuable).** Wealth platforms decide which DAF appears beside client accounts, as the SEI dual-stack, Edward Jones/RCF and TIAA/Charityvest/Foundation Source arrangements show. Adviser AUM on DAF assets (55 bps at OneGive; up to 1% elsewhere) is the incentive that keeps distribution loyal. *Medium-High.*
2. **Sponsor trust and legal standing.** Irrevocable gifts make the sponsor's governance the product. Discretion events (2026 SPLC-related restrictions **[RT]**) show the sponsor's judgment is visible and contested. *Medium.*
3. **Custody and affiliated investment economics.** At the affiliate-administered nationals, administration fees flow to the parent and 35 of 37 Vanguard Charitable pools are Vanguard funds. Cheap administration *raises* the relative importance of investment margin. *Medium-High.*
4. **Cross-sponsor data.** Eligibility outcomes, exception patterns, foreign-grantee equivalency determinations and recipient payment details are duplicated across about 1,500 sponsors. Whoever aggregates them (with consent) holds a compounding asset. No one does today; Chariot comes closest on the payment side. *Suggestive, Low-Medium.*
5. **Compliance evidence, not compliance labor.** As review labor shrinks, value moves to provable control: event-sourced audit trails, versioned policy, and attested SOC reports that match purchased scope. *Medium.*
6. **Nonprofit-side access.** Nonprofits bear reconciliation costs across 1,200+ DAF providers. The rail that nonprofits adopt (Chariot's DAFpay at a 2.9% default fee, or a sponsor-funded rail) gains network power. *Medium.*

**Less valuable:** standalone grant-approval software, generic donor portals, and per-grant charity lookups.

---

## F. What evidence would change our conclusions (falsification criteria and monitors)

| Conclusion | Would be revised if… | Monitor | Clarity posture |
|---|---|---|---|
| AI-on-existing-workflow is economically inferior (B) | Measured QA/re-review rates ≤5% with ≥40% handling-time saving at a real sponsor; or exception rates far above the 2.5–3% observable non-standard share | First sponsor time-and-motion study; vendor case studies with denominators | Experimental |
| Operating layer is the best *probe* (D) | Incumbent vendors gate ledger/API access; wealth buyers insist on bundles; incumbents ship policy-as-code within 12–18 months; measured cost pools below the ≈76k-grant break-even [RT] | Sponsor contract API clauses; Ren/FS/TIFIN release notes; SEI-type channel decisions | Strategic |
| Ren's share claim is unsupported (A4) | Evidence of Ren components inside Fidelity Charitable, DAFgiving360, Vanguard Charitable or NPT; or Ren defines its denominator | Ren disclosures; sponsor audited statements; Give Interactive/Vanguard scope | Guardrail (diligence) |
| Concentration is moderate (A3) | Census-level FY2025 DAFRC data shows CR3 above 55% on a consistent measure | DAFRC 2026 release | Fast |
| Manual review of listed public charities is habit (A6) | Final §4966/6033 guidance imposes per-grant diligence duties; enforcement actions against sponsors for grants to listed charities | Federal Register; IRS guidance plan; litigation | Guardrail |
| Fee incentives tilt toward retention (incentives) | Fund-level data showing no payout difference between AUM-fee and flat-fee sponsors after controlling for donor mix | DAFRC fund-level releases; Daffy/Charityvest payout vs nationals | Experimental |
| Portability is weak (A8) | A major sponsor publishes outbound transfer terms with history export; regulators require portability | Sponsor policy pages; guidance plan | Fast |
| Agentic risk is donor-side (B) | Sponsor discloses AI in approval/eligibility; an agent-originated erroneous grant is reported | Sponsor releases; incident reports; Daffy/TIFIN docs | Guardrail |

---

## G. The ten most important discoveries (ranked by strategic significance)

Each entry gives the evidence, the uncertainty, the implication and the next action. "[V]" marks independent validation or red-team confirmation.

1. **Most "DAF accounts" aren't DAF customers.** 79.5% of FY2024 accounts sit in donation processors holding 0.9% of assets, so traditional invested accounts number at most 737k.
   - **Uncertainty:** paper-filed and imputed processor counts; the lower bound is unknown.
   - **Implication:** every account-based TAM is overstated by 2–5×.
   - **Next:** extract sponsor-level account-size distributions from DAFRC; repeat for FY2025.

2. **The real software market is two markets plus a captive one.**
   - About 39% of period-aligned FY2024 assets sit at the three affiliate-linked nationals (Fidelity/FMR, Schwab; Vanguard hybrid) **[RT corrected from 49%]**.
   - Fully outsourced platform administration covers ≥6 sponsors holding 9.1% of assets.
   - Licensed software reaches 31–94% of sponsors (community foundations largely on Foundant).
   - **Uncertainty:** vendor counts are self-reported.
   - **Implication:** "DAF software TAM" must be segmented before any pricing or entry decision.
   - **Next:** EIN-match vendor client lists to the DAFRC panel.

3. **Apparently independent wealth-firm DAFs share one sponsor–vendor spine, and Ren's reach extends to community foundations.**
   - RCF + Ren underpin about 11 wealth programs.
   - Ren DFX fronts MS GIFT (new), BofA CGF and AEF.
   - Ren-owned iPhi serves the Cleveland Foundation and ImpactAssets.
   - **[V]** BofA evidence is portal-only, and the 10-K claim was contradicted.
   - **Uncertainty:** contract terms and scope (technology vs administration) per channel.
   - **Implication:** systemic SPOF and a single re-bid point for many brands.
   - **Next:** program circulars for each channel; RCF 990 Schedule O.

4. **Ren's ">half of DAF assets" claim is unsupported by public evidence.** Publicly evidenced Ren-linked sponsors hold about 8.7% of assets. **[RT]** The arithmetic ceiling outside the four largest sponsors is about 48%, and the "$200bn" figure includes non-DAF assets.
   - **Uncertainty:** undisclosed components at large sponsors are possible.
   - **Implication:** treat Ren's scale claims as unverified in any diligence.
   - **Next:** request Ren's denominator; check Give Interactive's scope at Vanguard Charitable.

5. **The economic value pool for DAF operations AI is thin, and redesign should precede it.**
   - **Evidence:** inference cost is immaterial (≈$0.45 vs ≈$83 per heavy review) **[V wave 2A]**. Grant-review value is ≈$16k/yr at a 48,744-grant sponsor **[S]**. An operating-layer product at $120k/yr needs ≈76k–369k grants/yr to break even **[RT]**.
   - **Uncertainty:** "AI ranks last" is an artifact of model inputs **[RT]**. No measured exception, QA or handling-time data exist anywhere in the market.
   - **Implication:** sponsors should fund continuous monitoring, electronic payee enrollment and policy-as-code first. AI economics work at vendor or network scale, not per sponsor.
   - **Next:** one real time-and-motion study at a sponsor, which is the gating evidence for every AI and entrant conclusion here.

6. **The agentic AI frontier is donor-side, and sponsors have no stated controls for it.** TIFIN's Louise executes donor requests; Daffy's MCP exposes `make_donation`; no spend limits are documented. No public evidence of AI in sponsor approval.
   - **Implication:** sponsors need agent-origin tagging and authority separation now.
   - **Next:** test Daffy MCP documentation; request TIFIN guardrail specifications.

7. **Payout is bimodal behind a reassuring average.** Aggregate 24–28%, but the median sponsor pays 11–12.5% and about one in five ≥$1m sponsors pays under 5%.
   - **Uncertainty:** sponsor-level, not fund-level; DAF-to-DAF transfers (10–18% of national sponsors' grants) inflate apparent payout.
   - **Implication:** the policy debate is about a long tail of sponsors, not the nationals.
   - **Next:** net out DAF-to-DAF transfers; segment by sponsor type.

8. **Fee economics reward retention, not grant-out, and the pass-through is near-total at RCF.** **[V]** RCF pays Ren 98% of individual-fundholder admin-fee revenue ($19.23m FY2024). Fidelity's admin fee is paid to FMR affiliates. 35 of 37 Vanguard pools are Vanguard funds.
   - **Uncertainty:** the causal effect on payout is unproven. **[RT] Counter-evidence:** DAFRC segment medians show national sponsors (AUM-fee, affiliate-linked) at about 20% median payout, versus about 11% for community foundations and about 5.4% for university/hospital sponsors. That runs against a simple "fees cause low payout" reading. Classification is downgraded to **mixed (incentive documented; effect unsupported)**.
   - **Implication:** incumbents' resistance to faster grant-out is predictable from incentives.
   - **Next:** compare payout at AUM-fee vs flat-fee sponsors.

9. **Portability is a legal right with operational lock-in.** No outbound policies, cash liquidation, no history portability, about $7.5bn/yr moving anyway.
   - **Implication:** an entrant offering portable history and in-kind transfer has a wedge; regulators have an easy target.
   - **Next:** a mystery-shop transfer at three sponsors (authorized test).

10. **A previously unknown vendor, Give Interactive, holds Vanguard Charitable's DAF recordkeeping** (press release Nov 4, 2025) and The Signatry's portal, and claims $40bn+ in assets.
    - **Uncertainty:** scope at Vanguard; client list.
    - **Implication:** the vendor landscape is less Ren/Foundation Source-dominated than assumed; a third white-label stack exists.
    - **Next:** add to the dependency graph; obtain the client list.

**Not in the top ten, but notable:**
- Regulatory reframing toward "certain DAF arrangements" (A9).
- Challenger fee drift (A10).
- The Kump/Foundation Source compensation link at Charityvest **[V]**: stronger than previously recorded.
