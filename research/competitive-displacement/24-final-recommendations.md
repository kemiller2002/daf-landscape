# 24 - Final recommendations

Status: research recommendations (2026-11-26), **reconciled with the adversarial review** ([20](20-adversarial-review.md); 110 challenges, 105 accepted in whole or part). Proposals only; decisions are in [23](23-executive-decision-register.md) and none is approved. Figures are model outputs from labelled assumptions, not measurements.

## Part A. The ten research questions

| # | Question | Answer | Confidence | Where |
|---|---|---|---|---|
| 1 | Can Unbound deliver DAF administration at a fundamentally lower cost than incumbents? | **Lower variable cost, yes; fundamentally lower total cost, no.** Against conventional administration, human time falls from ~183 to ~53 minutes and vendor variable cost from ~$397 to ~$147 per account-year. But a controlled platform doubles fixed cost: break-even at 20 bps is ~$1.9B operating / $2.3B fully loaded / P50 $2.5B (P90 $4.3B; correlated P90 $7.3B). **Against a well-automated incumbent the advantage is roughly $11-71 per account-year**, and AI is only ~6% of the saving. | Medium (direction); Low (levels) | [10](10-zero-touch-administration-economics.md), [15](15-capital-and-break-even-reassessment.md) |
| 2 | Which costs are inherent and which are artefacts? | **Inherent**: sponsor-reserved decisions, OFAC, 4966/4967 controls (including non-public evidence such as supporting-organization certifications), acknowledgments, reconciliation with custodians and banks, audit, mandatory Nacha fraud monitoring, judgement in grant approval, rails. **Artefacts**: full periodic re-vetting (a policy choice costing ~3x change-driven monitoring), staffing-ratio stewardship (39% of the $316k registry), charity portals and support desks, free-text attribution of pooled receipts, paper, internal re-keying, migration freezes and lost history. | Medium | [05](05-charity-registry-economics.md), [09](09-event-level-operating-model.md) |
| 3 | What would cause an institutional customer to leave Ren? | A scope need a DAF-only product cannot meet (stated publicly by three community foundations), a **vendor-forced migration**, or owning an alternative. Contract ends are mostly used to renegotiate. Where Ren's economics are shared with the customer or distributor, departures run about 1% a year. | Medium | [07](07-institutional-switching-incentives.md) |
| 4 | What would cause a prospective customer to select Unbound? | **Unknown.** Satisfied buyers see switching as a people, audit, board and vendor-viability problem; none of the product claims creates a decision. The most plausible route is through a **partner the buyer already trusts**, at a forced or integration-driven re-platforming. | Low | [07](07-institutional-switching-incentives.md), [16](16-commercial-entry-strategy.md) |
| 5 | Which incumbent advantages are genuinely defensible? | Distribution and incentive alignment (RCF ~98% fee pass-through; adviser compensation); sponsor-of-record control; repetition (Foundant 700+ foundations; Ren's absorbed books); payee enrolments and recipients paid; SOC and audit history; balance sheet and vendor viability; scale price ($81 per account); capital and acquisition velocity. | Medium-High | [06](06-competitive-displacement.md), [13](13-compounding-competitive-advantages.md) |
| 6 | Which can be neutralised? | Status and screening data (public); vetting cost (change-driven monitoring); onboarding *risk* (rehearsed, reconciliation-gated migration, though full history needs a contracted incumbent export); audit evidence (generated). **Not** distribution economics, vendor-viability objections or repetition. | Medium | [02](02-charity-intelligence-sources.md), [08](08-frictionless-onboarding.md) |
| 7 | Can we enter without first operating a conventional servicing organisation? | **Yes**, as a technology licensor, ideally inside a channel partner's offering. It is still a regulated activity: a platform creating ACH files is a Nacha TPSP, sponsors' auditors will want SOC 1 and SOC 2, and bank channels add third-party-risk examination. | Medium | [14](14-alternative-enterprise-models.md) |
| 8 | Can the technology create an advantage that compounds with each customer? | **No network effect.** Modest learning economies (adapters per incumbent source, identity resolution, prevention rules) where incumbents are ahead today, a scale economy in shared public evidence, and no time-based moat (the BMF archive already exists publicly). | Medium-High | [13](13-compounding-competitive-advantages.md) |
| 9 | Minimum viable commercial entry point? | **A partner pilot**: Unbound's DAF ledger, reconciliation-gated migration and eligibility evidence licensed as a module inside an established partner's offering, delivered to one of that partner's re-platforming customers. The free exit-readiness assessment is pre-sales, not a product. | Low-Medium | [16](16-commercial-entry-strategy.md) |
| 10 | What evidence would invalidate the thesis? | No partner engages by month 6; stayers rank every positioning claim below "nothing"; switchers and stayers say distribution economics alone decide; buyers pay < ~$60 per account; incumbents publish migration and exit commitments first or obstruct exports; acquisition slower than one customer a year. | — | [22](22-commercial-validation-plan.md) §2 |

## Part B. Final executive questions

**1. Are we building the right business?**
**No, not as the entry business.** A full-service displacing administrator in the least mobile segment is the most capital-intensive route (about $10M at market pay, ~22% chance of payback within ten years; $4.5M only with below-market founder pay and an anchor). Start as a **DAF technology licensor that enters through a channel partner**, and keep administration as an option behind a signed anchor.

**2. Are we building the right product?**
**Mostly, with re-ordered priorities.** Keep the single operational ledger, deterministic controls, provenance-bound vetting and reconciliation-gated migration (Transitus phase 1). Add a licensing operating mode where a partner or sponsor runs exceptions, a sponsor-scoped screening design, process-only SLAs, and prevention-first input design. Stop treating AI as the economic engine: in the model it is about 6% of the saving and costs more in oversight than it saves below ~26k accounts.

**3. What should we deliberately not build?**
A proprietary charity payment network; any requirement that charities log in; a standalone charity-intelligence or ratings product (Candid from $2,750 a year); a paid migration-assessment business; a generic ELT engine; vendor-specific migration packages before an authorised sample; a CF fund-accounting suite to fight Foundant; custodial operations before an anchor; advisor-platform integrations into slots incumbents hold.

**4. What can we do substantially better than Ren?**
Little that is *substantially* better and durable, on present evidence. Candidates, all hypotheses until tested with stayers and a live pilot: verifiable migrations with per-fund reconciliation and full history (when the incumbent export is contracted); replayable eligibility decisions from provenance-bound public evidence; a single operational ledger without internal re-keying; transparent licence pricing; a licence that leaves the sponsor's brand and economics with the sponsor.

**5. What can Ren do that we cannot readily replicate?**
Pay its distribution (sponsor-of-record and adviser economics); offer the balance sheet, SOC history and longevity buyers require; draw on years of repetition and 140k+ recipients paid; price software at about $81 per account at scale; and raise growth capital (Great Hill, 2025).

**6. What is our strongest defensible competitive advantage?**
**None yet.** The temporal archive turned out to be public (NCCS), migration commitments are copyable clauses, and incumbents lead on learning economies. The most defensible *position*, rather than asset, is **neutrality**: a licensed platform that does not capture sponsor-of-record or adviser economics, delivered through partners who want an alternative to incumbents that compete with them. That is a hypothesis for V-6.

**7. What is our cheapest credible route into the market?**
**G0 validation ($0.15-0.35M, 6 months) → a G1 partner pilot ($1.0-1.5M cumulative, 6-24 months) → licensing through that channel.** Kill rule: no named partner by month 6, or no referenceable pilot that has passed a buyer security review by month 24.

**8. How much capital would that route require?**
About **$6.5M (P50) to a self-sustaining business, P90 about $9M**, with a **37% chance of no payback within ten years**. Of that, **$0.15-0.35M** decides whether to spend the rest, and **$1.0-1.5M** reaches a live partner pilot. Even when it works, the base case reaches about $2.6M of annual revenue at month 60 and pays back around month 111: a sustainable niche software business, not a venture-scale outcome. Direct licensing without a channel: P50 $7.6M.

**9. What is the greatest threat to our success?**
**Distribution and buyer risk aversion.** Incumbent revenue is shared with purchase decision-makers, channels are being locked up now (SEI-TIFIN, TIAA-Foundation Source, Altruist-Endaoment), satisfied buyers treat a startup as a viability risk, and small DAF technology firms historically end as acquisitions. Second: incumbents copying the migration and transparency wedge, which needs no engineering.

**10. What should Echelon Foundry do next?**
1. Run **V-6 (channel partners)**, **V-1 (5 switchers and 5 stayers)** and **V-5 (active evaluations)** in the next 12 weeks. They are cheap and decide the thesis.
2. Ask the owner to reopen OD-M-05 (DEC-001) and to adopt the kill rule and gated funding (DEC-008).
3. Run V-3 (public-data replay) and settle the re-vetting policy question with counsel (DEC-003).
4. Keep Transitus to phase 1 and seek one export under MSA + DPA (V-4).
5. Defer custodial administration until a signed anchor exists (DEC-002). Do not raise platform capital before a partner is named.

## Part C. Is the existing commercial strategy wrong?

**The destination is defensible; the entry path is not supported, and the economic case for AI-native displacement is weaker than the earlier packages implied.** The alternative is in [16](16-commercial-entry-strategy.md): partner-first, licence before administration, with explicit kill rules. If V-6 finds no partner, the honest options are direct licensing at higher capital and risk, or pausing the thesis.
