# 24 - Final recommendations

Status: research recommendations (2026-11-26), reconciled with the adversarial review ([20](20-adversarial-review.md)). Proposals only; decisions are listed in [23](23-executive-decision-register.md) and none is approved.

## Part A. The ten research questions

| # | Question | Answer | Confidence | Where |
|---|---|---|---|---|
| 1 | Can Unbound deliver DAF administration at a fundamentally lower cost than incumbents? | **Variable cost, yes; total cost at entry scale, no.** Modelled vendor variable cost falls from ~$324 to ~$85 per account-year and human time from ~183 to ~26 minutes, but owning a controlled platform roughly doubles fixed cost, so break-even at 20 bps moves only from ~$2.1B to ~$1.5B (MC P50 $2.4B to $1.7B). Most of the saving is design and prevention, not AI (~10%). | Medium (direction); Low (levels) | [10](10-zero-touch-administration-economics.md) |
| 2 | Which costs are inherent, which are historical artefacts? | **Inherent**: sponsor reserved decisions, OFAC, 4966/4967 controls, acknowledgments, reconciliation and audit, fraud response, judgement in grant approval, rails. **Artefacts**: full periodic re-vetting (4x change-driven), staffing-ratio stewardship (39% of the $316k registry), charity portals and support desks, free-text attribution of pooled receipts, paper, re-keying between GL and portal, migration freezes and lost history. | Medium | [05](05-charity-registry-economics.md), [09](09-event-level-operating-model.md) |
| 3 | What would cause an institutional customer to leave Ren? | An **integration need** a DAF-only product cannot meet (CFs), a **vendor-forced migration**, or owning an alternative. Not observed: price, exit terms, lost history, SOC inconsistencies. Where Ren's economics are shared with the customer or its distributor, departures are rare (1 of 26 national/faith iPhi sponsors). | Medium | [07](07-institutional-switching-incentives.md) |
| 4 | What would cause a prospective customer to select Unbound? | **Unknown on evidence.** Candidates to test: verifiable full-history migration with a short freeze; licence-not-capture economics; replayable vetting for auditors; published price and symmetric exit. | Low | [07](07-institutional-switching-incentives.md), [22](22-commercial-validation-plan.md) |
| 5 | Which incumbent advantages are genuinely defensible? | Distribution and incentive alignment (RCF 98% pass-through; adviser compensation); sponsor-of-record control; accumulated payee enrolments and recipients paid; SOC and audit history; brand; scale price at the software tier; capital and acquisition velocity. | Medium-High | [06](06-competitive-displacement.md), [13](13-compounding-competitive-advantages.md) |
| 6 | Which can be neutralised? | Directory and eligibility evidence (public data); vetting cost (change-driven monitoring); onboarding risk (rehearsed, reconciliation-gated migration with adapters); reporting and audit evidence (generated); integration fragmentation (single ledger). **Not** distribution economics. | Medium | [02](02-charity-intelligence-sources.md), [08](08-frictionless-onboarding.md) |
| 7 | Can we enter without first operating a conventional servicing organisation? | **Yes.** Technology-only licensing (vendor variable ~$27 per account; ~30k accounts at $81 to break even) and non-custodial services need no custody, no payment origination and no operations team. | Medium | [14](14-alternative-enterprise-models.md) |
| 8 | Can our technology create an advantage that compounds with each customer? | **Not a network effect.** Learning economies (migration adapters per source, identity resolution, prevention rules), a scale economy (shared public evidence) and one time-based asset (a temporal archive that cannot be backfilled). All are modest and mostly replicable within 6-24 months. | Medium | [13](13-compounding-competitive-advantages.md) |
| 9 | Minimum viable commercial entry point? | **A paid migration assessment and reconciliation report bundled with a charity eligibility evidence feed, sold to sponsors already in a re-platforming or contract-end window**, leading to a licensed platform through a channel partner. | Low-Medium | [16](16-commercial-entry-strategy.md) |
| 10 | What evidence would invalidate the thesis? | Win/loss showing distribution-only switching **and** no channel partner; buyers paying < ~$60 per account; incumbents publishing migration and exit commitments first; incumbent exports unobtainable or unreconcilable; change-driven vetting rejected by auditors; acquisition slower than one customer a year. | — | [22](22-commercial-validation-plan.md) §2 |

## Part B. Final executive questions

**1. Are we building the right business?**
Not as the entry business. A full-service displacing administrator in the least mobile segment is the most capital-intensive route ($4.5M founder-led to $8.8M market-pay) into the segment with the least observed switching. The right business to start is a **DAF technology licensor with non-custodial wedges**, keeping administration as a later option behind an anchor.

**2. Are we building the right product?**
Mostly yes, with re-ordered priorities. The single ledger, deterministic controls, provenance-bound vetting and reconciliation-gated migration are sound. Priorities should move toward: (a) Transitus phase-1 migration assessment and reconciliation, (b) a public-data eligibility evidence layer with a temporal archive, (c) a licensing operating mode where a sponsor or partner runs exceptions, (d) prevention-first input design. Advisor-channel features and a CF fund-accounting suite should wait.

**3. What should we deliberately not build?**
A proprietary charity payment network; any requirement that charities log in to be paid; a charity ratings product; a generic ELT engine; vendor-specific migration packages before an authorised sample; a CF fund-accounting suite to fight Foundant; custodial operations before an anchor; integrations into advisor-platform slots that incumbents already hold.

**4. What can we do substantially better than Ren?**
Prove migrations (full history, measured freeze, per-fund reconciliation, published exit); make eligibility decisions replayable from public, provenance-bound evidence with change-driven monitoring; operate a single ledger without GL-portal reconciliation; price transparently; and run at lower variable cost through prevention. Each is a hypothesis about buyer value until V-1 and V-4 run.

**5. What can Ren do that we cannot readily replicate?**
Pay its distribution: sponsor-of-record and adviser economics (RCF passes ~98% of fundholder fees to Ren); 150+ platform relationships (claimed); 140k+ recipients paid and enrolment history; years of SOC and audit history; $81 per-account software pricing at scale; fresh growth capital.

**6. What is our strongest defensible competitive advantage?**
None is strong yet. The most durable candidate is the **combination of a temporal, provenance-bound eligibility evidence archive with a measured, reusable migration capability**: one cannot be backfilled by a later entrant, the other improves with every migration from the same source. Its value depends on buyers rewarding verifiable migration (HYP-003), which is unproven.

**7. What is our cheapest credible route into the market?**
Evidence gates first (G0: $0.15-0.35M), then the non-custodial wedge at contract-end windows (cumulative $0.7-1.2M), then **licensing through a channel partner** (ER-7). No route below about $4M reaches self-sustaining operation in the model.

**8. How much capital would that route require?**
About **$5.1M (MC P50; P10 $4.0M, P90 $6.8M)** to a cash-positive licensing business through a channel (base month 43), of which **$0.35-0.75M** is the evidence budget that decides whether to spend the rest. Direct licensing without a channel: $6.5M P50. Full administration: $4.5M founder-led (PR #87) to $8.8M market-pay base.

**9. What is the greatest threat to our success?**
**Distribution.** Incumbents' revenue is shared with the people who decide purchases, channels are being locked up now (SEI-TIFIN, TIAA-Foundation Source, Altruist-Endaoment), and small DAF technology firms historically end as acquisitions. Second: incumbents copying the migration and transparency wedge once buyers reward it.

**10. What should Echelon Foundry do next?**
1. Run V-1 (win/loss), V-5 (contract-end calendar) and V-6 (channel partners) in the next 12 weeks; they are cheap and decisive.
2. Start V-3 (public-data replay harness) and begin archiving every IRS and sanctions release now.
3. Ask the owner to re-open OD-M-05 (DEC-001) with this evidence, and to fund gates before platform capital (DEC-008).
4. Keep Transitus to phase 1 and pursue one authorised incumbent export (V-4).
5. Defer custodial administration until a signed anchor exists (DEC-002).

## Part C. Is the existing commercial strategy wrong?

**The destination is defensible; the entry path is not supported.** The evidence does not support entering by displacing incumbents at mid-size national and advisor-distributed sponsors with 20 bps administration. The proposed alternative is in [16](16-commercial-entry-strategy.md): evidence-first, channel-led, licence before administration.
