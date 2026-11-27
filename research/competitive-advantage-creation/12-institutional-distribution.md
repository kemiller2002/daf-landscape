# 12 - Institutional distribution without a conventional sales organization

Status: research (2026-11-26). Track J. Agent key FGJ. Register rows: `data/fragments/FGJ/` (P3-CLM-FGJ008..010, 018, 020; P3-HYP-FGJ004..006; P3-ASM-FGJ001..009, 016, 017; P3-SEQ-FGJ004; P3-DEC-FGJ003; P3-XRI-FGJ001..002; P3-GAP-FGJ001, 002, 008). Builds on Phase II [11](../competitive-displacement/11-institutional-distribution.md) and [16](../competitive-displacement/16-commercial-entry-strategy.md) (HYP-001, HYP-010, CLM-017, CLM-018, CLM-025, CLM-036, CHL-084), under approved DEC-001 (partner-first) and DEC-006 (licensing-first). Public benchmarks: P3-SRC-FGJ005..010. This report proposes; it does not authorize outreach or contracts.

## Answer

1. **Partner-first does not reliably lower total acquisition cost. It mostly converts upfront CAC into deferred, revenue-contingent margin, and it buys access that money cannot buy at entry.** At base inputs the partner keeps about $75k over a sponsor's licence life (~$57k in present value). Add ~$15k of enablement per deal and the total is about $90k, against an assumed $125k direct CAC: about 28% cheaper undiscounted. But the break-even share swings from above 100% for small sponsors to about 15% for large ones (P3-CLM-FGJ009). Every input is an assumption or a secondary benchmark.
2. **The real case for partner-first is access, not cost.** An entrant has no SOC history, no vendor-viability record and no distribution, and buyers' procurement weighs all three (CLM-040, CHL-014/015). A partner removes those blockers; direct spending cannot buy them quickly at any CAC. **DEC-001 still stands**, but the business should be honest that it is paying for access with margin and with strategic control.
3. **Margin is not the main risk; control is.** Phase II found administrators acquire rather than license (CLM-025), purchase controllers are paid to stay (CLM-017), and distributors add providers rather than replace them (CLM-018). A partner that owns the customer, support and pricing can re-platform or acquire once Unbound is proven (CHL-084).
4. **Independence needs contract terms, a second partner and product features.** The contract terms are a walk-away floor (P3-DEC-FGJ003). The second partner should come before G2. The product needs a sponsor tenancy that survives a channel-partner exit (P3-XRI-FGJ001).

## 1. Public benchmarks for channel economics

| Mechanism | Share kept by intermediary | Source | Notes |
|---|---|---|---|
| Cloud marketplace transaction (AWS SaaS public offer) | 3% (private offers 3%/2%/1.5% by TCV) | P3-SRC-FGJ006 (2024-01) | Billing and procurement convenience; no selling |
| Microsoft commercial marketplace | 3% | P3-SRC-FGJ007 (2021-07) | Same |
| Platform ISV programme (Salesforce AppExchange) | 15% of net revenue (cut from 25% in 2017) | P3-SRC-FGJ005 | 2026 rate not confirmed (P3-GAP-FGJ008) |
| Referral / solutions partner (HubSpot) | 20% of recurring net revenue for up to 3 years; 12 months for providers; ends on customer churn | P3-SRC-FGJ008 | A useful template: capped and sunset |
| Reseller margin (new business) | ~15-30% off list; renewals ~5-15%; top tiers to ~40% | P3-SRC-FGJ009 (secondary, Low-Medium) | No primary survey located |
| Bank-core marketplace (Jack Henry FIN) | Entry fee model; no public revenue share | P3-SRC-FGJ010 | Access fee, not a seller (P3-CLM-FGJ010) |
| DAF precedent: sponsor-of-record to administrator | RCF passes ~98% of administration fees to Ren | CLM-017 | The administrator, not the brand holder, captures the economics |
| DAF precedent: adviser compensation | TIFIN pays advisers 0-100 bps; Morgan Stanley $4.24M as GIFT adviser | Phase II 11 | Adviser economics may be affected by proposed 4966 regulations (CHL-042) |
| Phase II stress assumption | 30% base; 40-50% stress | CHL-084 | No source beyond earlier assumption |

The pattern is consistent across these sources. Intermediaries that only **bill** take about 3%. Those that **refer** take 15-20%, usually time-limited. Those that **resell, implement and support** take 20-40%. An embedded DAF module where the partner owns the customer and first-line support (Phase II 16 G1) belongs in the last band. The working range is **15-40%, base 25%** (P3-ASM-FGJ001).

## 2. Does partner-first cut CAC or transfer margin?

Inputs (all ranges in `assumptions.csv`): annual licence revenue per sponsor R = $25k / $60k / $150k (P3-ASM-FGJ008); licence life L = 3 / 5 / 8 years (P3-ASM-FGJ009); partner share s = 15 / 25 / 40% (P3-ASM-FGJ001); direct CAC C = $40k / $125k / $200k (P3-ASM-FGJ007; no public CAC exists, CLM-026); enablement E = $10k / $30k / $75k per partner (P3-ASM-FGJ006); partner-sourced deals n = 0 / 1 / 3 per year (P3-ASM-FGJ005); discount rate 10% (P3-ASM-FGJ017).

Partner cost per sponsor = s x R x L + E / (deals over the agreement). Break-even share s* = (C - E/deals) / (R x L).

| Case | Margin transferred (undiscounted) | PV at 10% | Enablement per deal | Partner total | Direct CAC | Result | Break-even share |
|---|---|---|---|---|---|---|---|
| Small sponsor (R $25k, L 3, s 25%) | $18.8k | $15.5k | $15k (2 deals) | ~$34k | $40k-$125k | Partner cheaper | >100% at C $125k (partner always cheaper) |
| **Base** (R $60k, L 5, s 25%) | **$75k** | **$56.9k** | $15k | **~$90k (PV ~$72k)** | **$125k** | **Partner ~28% cheaper undiscounted, ~42% in PV** | **~37%** |
| Base at 40% share | $120k | $91k | $15k | ~$135k | $125k | Roughly equal | ~37% |
| Large sponsor (R $150k, L 8, s 25%) | $300k | $200k | $15k | ~$315k | $200k | **Partner far more expensive** | ~15% |
| Partner sources nothing (n = 0) | $0 | $0 | $30k-$75k sunk | $30k-$75k with no customer | n/a | Pure loss | n/a |

**Reading the table:**
- For **small and mid-size sponsors**, which are Phase III's likely early customers (Track C), partner-first is cheaper than an assumed direct CAC. It is not cheaper than **founder-led direct selling**, whose cash CAC is mostly founder time (Track A/B).
- For **large sponsors**, a perpetual share costs more than direct acquisition would. Shares must therefore **decline or sunset** (the HubSpot pattern), or large accounts must convert to direct contracts after an agreed period.
- The partner share is **revenue-contingent and deferred**. For a capital-constrained founder that is worth more than its present value suggests: no revenue means no payment. This is the strongest economic argument for partner-first.
- **Sales cycles do not obviously shorten.** Partner cycles inherit the partner's customer procurement (6-24 months; P3-ASM-FGJ004). Partners add a second procurement: the partner's own vendor review. P3-HYP-FGJ004 is untested.
- **Margin transfer understates the true cost.** It omits the partner's control over pricing, roadmap pressure, and the option to build or acquire (CHL-084).

**Verdict:** partner-first **transfers margin to buy access and defer cash**. It lowers CAC for small and mid-size sponsors only if partners actually source deals (P3-GAP-FGJ002), and it raises lifetime cost for large sponsors unless shares sunset.

## 3. Channel-by-channel evaluation

Scale: **H** high, **M** medium, **L** low. "Control" is Echelon's long-term strategic control.

| Channel | Incentive alignment | Revenue share (basis) | Customer ownership | Exclusivity pressure | Contractual dependency | Concentration risk | Channel conflict | Sales cycle | Implementation / support | Control |
|---|---|---|---|---|---|---|---|---|---|---|
| **CF-software or administrator partner embedding Unbound as a DAF module** (DEC-001 primary) | M: fills a gap in the partner's suite; but the partner may build or acquire later | 20-40% (reseller band) | Partner | H: partners ask for category exclusivity | H | H with one partner | Low at first; high if Echelon later sells direct to the partner's customers | 12-24 months (CF cycles) plus partner onboarding | Partner first line; Echelon second line and engineering | **L-M** without safeguards |
| **Custodians** (RIA/wealth custody) | L: custodians run their own DAFs or have partners (Phase II 11) | Unknown (P3-GAP-FGJ001) | Custodian | H | H | H | H with custodian DAFs | 12-24 | Custodian | L |
| **Technology partnerships / data layers** (wealth platforms, multi-custodian data) | M where no DAF partner exists (Addepar: open, untested) | 0-20% (integration or referral) | Shared | M | M | M | M | 6-18 | Echelon | M |
| **Bank-core / digital-banking marketplaces** | L-M: access fee, not a seller (P3-SRC-FGJ010) | Entry fee; no public share | Echelon (bank contracts directly) | L | M (API access) | M | L | 6-24 plus bank TPRM (5/5) | Echelon | M-H, but procurement cost is high |
| **Professional associations** (community-foundation and fiscal-sponsor networks) | H for neutral education; L for endorsement | Sponsorship or affinity fees (not priced) | Echelon | L | L | L | L | n/a (lead source) | Echelon | **H** |
| **Advisor networks** | M: advisers want client retention and compensation; pending 4966 rules may restrict adviser compensation from DAFs (CHL-042) | 0-100 bps precedent (TIFIN) | Shared or adviser | M | M | M | H with incumbent adviser programmes | 1-6 (RIAs) | Echelon | M |
| **Sponsor partnerships** (a public-charity sponsor offers a programme on Unbound, e.g. new-programme enablement) | H: sponsor gains a programme; Echelon avoids administration (DEC-002) | Licence or cost-share | Sponsor | M | H | H | L | 9-24 | Sponsor operates; Echelon supports software | M |
| **White-label** (partner's brand on Unbound) | M | 20-40% | Partner | H | H | H | M | As embedded | Partner | **L** unless "powered by" and reference rights |
| **Embedded integrations** (APIs into grants suites, CRMs) | H: complements, does not replace | 0-15% | Echelon | L | L-M | L | L | Short once built | Echelon | **H** |
| **Referrals** (counsel, accountants, consultants) | M: professional-conduct rules restrict referral fees for attorneys and CPAs (counsel to confirm) | 0-20% where permitted | Echelon | L | L | L | L | Varies | Echelon | **H** |
| **Open-source credibility** | H for engineering diligence; L as demand | 0 | Echelon | n/a | L | n/a | n/a | n/a | Issue support | **H** |
| **Public research** (this repository's method and findings) | H for category education | 0 | Echelon | n/a | n/a | n/a | n/a | n/a | n/a | **H** |
| **Technical demos** (synthetic-data Unbound, reproducible migration rehearsal) | H | 0 | Echelon | n/a | n/a | n/a | n/a | Shortens evaluation (hypothesis) | Echelon | **H** |
| **Design partnerships** | H if the sponsor gets influence and price | Discount, not share | Echelon | M (design partners ask for favoured terms) | M | H with one partner | L | 6-12 | Echelon, intensive | M-H |
| **Professional networks** (founder) | M | 0 | Echelon | n/a | L | Founder concentration | L | Unknown | Echelon | H |

**Pattern.** The channels that **sell** (embedded partners, custodians, white-label) give the most access and the least control. The channels that **build credibility** (associations, research, open source, demos, embedded integrations, referrals) keep control but sell nothing on their own. A workable distribution model combines **one or two selling partners** with **owned credibility channels**, so that Echelon's own reputation reaches end customers independently of any partner.

## 4. Keeping strategic independence

Business-plan principles already point this way: "reversible action before fixed cost, lock-in, rights transfer, or client dependence" and "minimum necessary dependence, substitution or exit paths" (P3-CLM-FGJ018). These need concrete terms (P3-DEC-FGJ003):

| Safeguard | Term | Why | Evidence/precedent |
|---|---|---|---|
| Non-exclusivity | No exclusivity; or exclusivity limited to one named segment, at most 12-24 months, and conditional on minimum committed volume | Keeps the second-partner route open | Distributors add providers (CLM-018); exclusivity is the partner's leverage |
| Capped, declining share | Share falls with volume and sunsets for directly-serviced or large accounts (e.g. referral-style 3-year term) | Large-sponsor economics (section 2) | HubSpot 20% for up to 3 years (P3-SRC-FGJ008) |
| IP retention | Echelon owns the platform, the canonical data model and the migration format; partner owns its own extensions | Prevents a partner from capturing core IP | Licensing-first (DEC-006) |
| No ROFR or acquisition option | No right of first refusal, no option to acquire, and no most-favoured-nation pricing | Acquisition is the likely partner move (CHL-084, CLM-025) | Phase II SEG-013 |
| Change-of-control termination | Echelon may terminate or reprice if the partner is acquired by a competitor | Consolidation is active (CLM-032) | |
| Direct-reference rights | Echelon may name customers (with their consent) and publish anonymized outcome evidence | Builds independent reputation | Public research and demos |
| Sponsor data portability | Sponsor has a contractual and technical right to full-history export in the published canonical format, not gated by the partner | Lock-in protection for customers and Echelon | Unbound exit exports (UNB-KNOW-038 lineage) |
| Continuity on partner exit | If the partner relationship ends, the sponsor may continue on Unbound directly or through a successor partner **without data migration** | Converts partner churn from loss into a direct customer | **Missing in Unbound requirements** (P3-CLM-FGJ020; P3-XRI-FGJ001) |
| Multi-partner by G2 | A second partner in a different segment (e.g. fiscal-sponsor or faith network) before G2 capital | Limits concentration | Phase II kill rule (CHL-022) |
| Concentration ceiling | Target: no partner above ~50% of revenue after month 36 (planning target, not evidence-based) | Bargaining power | |
| Owned evidence | Publish product evidence (reconciliation proofs, SOC reports when they exist, public specifications) directly to sponsors | Reputation independent of the partner | echelon-due-diligence approach |

**Trade-off.** Partners will resist most of these terms; Phase II found the leverage sits with them. If every engaged partner insists on exclusivity, a share above 40%, or an acquisition option (P3-HYP-FGJ005 falsified), the honest conclusion is that Echelon is a **supplier to an acquirer**. That outcome should be valued, and chosen deliberately, rather than drifted into.

**Revision 2 (P3-CHL-REV3028, P3-CHL-REV3034, P3-CHL-REV1023, P3-CHL-REV1028, P3-CHL-REV3025).**
- **These terms are a walk-away floor, not an expected outcome.** A partner can be expected to ask for non-solicit, segment exclusivity, escrow, step-in rights and MFN pricing. P3-SEQ-FGJ004 is therefore re-rated from failure band "moderate" to "high". Agent MOD is modelling H under partner-standard terms.
- **The partner inherits the entrant's gaps; it does not remove them.** Those gaps are one founder, no SOC report, design-stage controls, unpublished commercial terms and unbound insurance. A partner's TPRM review will test each one.
- **A minimum vendor-viability package is a precondition for term-sheet talks.** It needs:
  - executed commercial licence terms (Echelon Foundry owns the IP, OD-P3-01, so these are an owner act);
  - source escrow;
  - a contracted second engineer;
  - a SOC 2 Type 1 report and a committed Type 2 date;
  - an insurance certificate;
  - basic financial-condition evidence;
  - an exit plan.

  The same package should disclose the two concentration risks the package accepts: one selling partner above 50% of revenue until month 36, and a single managed PostgreSQL provider (a fourth-party risk). The package's costs and lead times are not yet priced. Model revision 2 includes control operations and TPSP obligations, but not escrow, the SOC 2 Type 1 fee as a separate gate, or financial-evidence costs.
- **Revenue shares linked to contributions** may trigger charitable-solicitation registration (professional fundraiser, fundraising counsel or commercial co-venturer). Until counsel answers per channel model, price partner shares on licence revenue, not on contributions (P3-GAP-CD013).

## 5. Sequence implication

P3-SEQ-FGJ004 refines Seq A under DEC-001. The steps are: a non-exclusive pilot partner with the safeguards above; a second partner before G2; then direct licensing to referenceable sponsors. Credibility channels (research, demos, open repositories, associations) run in parallel at near-zero cash. No conventional sales organization is needed before G2. Founder-led selling into partners and design partners is the sales function. The business plan rule of no high-powered close-revenue incentives (07.08) fits this model.

## 6. Gaps

Partner revenue-share terms in DAF and wealth channels (P3-GAP-FGJ001); partner-sourced deal rate and cycle (P3-GAP-FGJ002); current AppExchange share (P3-GAP-FGJ008). Referral-fee rules for attorneys and CPAs need counsel confirmation before any referral programme is designed.
