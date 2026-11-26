# Competitive analysis

**Status:** analysis, 2026-11-20. It positions the proposed enterprise against established and emerging participants, using repository evidence only.
- Market facts are cited to the [industry report](../../DAF-INDUSTRY-REPORT-2026-11.md) and the [strategic synthesis §0](../../mission-2026-11-14/strategic-synthesis.md).
- [I] marks inference.

## 1. The field, by layer

DAF competition happens in separate layers that are often owned by different parties (industry report §2). Competing "against Fidelity Charitable" and competing "against Ren" are different games.

| Layer | Established | Emerging or challengers | Concentration evidence |
|---|---|---|---|
| Sponsor of record (assets) | Fidelity Charitable (20.5–21.7% of corrected assets every year FY2021–24 [V]), NPT (#2 in FY2024), DAFgiving360, Vanguard Charitable, community foundations (about 803) | Daffy ($2bn company-reported; $334.19m FY2024 990 [V]), Charityvest, Endaoment, Groundswell, Givinga (processor) | CR3 45.5%, HHI ≈ 830 (unconcentrated) [V] |
| Administration and technology | FMR (Fidelity), affiliated stacks at Schwab and Vanguard; Ren (incl. iPhi/Stellar); Foundation Source (GTCR); TIFIN Give; Foundant (CFs); Blackbaud; Salesforce-based stacks | Give Interactive (controlled by The Signatry's trust [V]); NPact; akoyaGO; GiftingNetwork (Orion) | Ren confirmed-link floor 32.2% of assets [V wave 31A]; Foundant 361 of 803 CFs [V wave 9] |
| Rails | Fidelity EFT/Stripe; PayPal Grant Payments (NPT, Vanguard); Ren Rapid Disbursement Engine; checks | Chariot Disbursements (TIFIN/GiveClear, Daffy, Founders Pledge, Groundswell, Charityvest in transition) | Four camps [V]; one observed switch (Charityvest → Chariot) [V wave 6] |
| Eligibility data | IRS BMF / Pub 78 / revocation; OFAC | Candid Charity Check, Goodstack, Benevity, Chariot | IRS master file is a shared single point of failure [V] |
| Distribution | Wealth firms (Edward Jones, Morgan Stanley, UBS, LPL, Ameriprise, RBC, Goldman, J.P. Morgan via NPT) | Platforms (SEI multi-sourcing; Altruist with Endaoment; TIAA with Charityvest/Foundation Source) | About 11 wealth programs on RCF + Ren [V] |
| Agentic donor-side products | TIFIN Give Louise; Daffy MCP | 30 products censused; none meets the RED test; only two can move DAF money [V wave 28] | — |

## 2. Where the proposed enterprise would differ

| Dimension | Typical incumbent practice (public evidence) | Proposed design | Persistence condition |
|---|---|---|---|
| Grant decisions | Review norms vary; no sponsor publishes P50/P90 turnaround or exception rates [V]; no public evidence of AI in sponsor-side approval [V] | Deterministic approval of routine grants under versioned, back-tested policy; exception-only human review; published latency distribution | Persists only if incumbents' incentives keep them from publishing metrics; a well-run national could copy it within 1–2 years [I] |
| Eligibility | Per-grant lookup | Continuous monitoring with bitemporal evidence | Low persistence; easy to copy |
| Records | Mutable records; history lost in migrations (AEF kept two years [V]) | Event-sourced ledger; full-history export in an open schema | Medium. Incumbents' migration costs and vendor contracts slow copying [I] |
| Recipient experience | Grant detail out of band; no grant ID stated in ACH addenda at readable top-10 sponsors [V wave 39A] | Machine-readable remittance with grant ID; electronic by default | Medium. It requires rail and sponsor cooperation; the payoff accrues to nonprofits, who have weak leverage [V structural] |
| Transparency | All-in cost hidden in fund and adviser layers; adviser fees uncapped at Fidelity CIAP, NPT, AEF and RCF [V] | Published all-in cost per account; advisor fee caps enforced as code | High *if* the business model does not depend on undisclosed layers, which is precisely what incumbents cannot easily change |
| Agent access | Credential sharing barred; MCP without documented limits (Daffy) [V] | Delegated, scoped, capped agent principals (DD-017) | Medium. A standard could emerge and level this |
| Cost to serve | CF staff cost 78.7 bps of DAF assets vs 5.6–15.0 at self-staffed nationals [V] | Specialist-led organization (see 09- for modeled cost) | Depends on measured exception and handling data (Q-N03), not yet available |

## 3. Why technical superiority may not drive adoption

1. **Incentives favor assets, not speed** ([industry incentives §4–§5](../../mission-2026-11-14/industry-incentives-structural-analysis.md)).
   - Affiliated managers earn expense ratios.
   - Fee-share administrators receive about 98% of RCF's individual-fundholder fees [V].
   - Advisors earn on DAF AUM: 55 bps at OneGive; up to 1% where capped; 0–2% observed [V].
   - Faster grant-out shrinks all three bases.
   - Classification: structural (financial); confidence Low-Medium on the effect, documented on the incentive.
2. **Contracts close data and automation.**
   - Six of the top 20 sponsors (about $84bn) limit automated or third-party access [V wave 19].
   - Public vendor templates allow batch export but not live integration [V].
   - Executed contracts remain unseen (Q-N04).
3. **Buyers buy bundles.** Banks and wealth firms buy sponsor plus technology plus brand (SEI Charitable Fund = GiveClear + TIFIN Give [V]), so a superior component is not what they evaluate.
4. **PE consolidation absorbs challengers.**
   - Six of six documented DAF-tech exits went to Ren, Foundation Source or TIFIN (failure pattern P2).
   - GTCR made four acquisitions in about 17 months after buying Foundation Source [V].
   - Bonterra has stated "further M&A ambitions" [V].
   - A visible innovation is more likely to be bought than to displace anyone.
5. **Trust is not a software property.** Donors make irrevocable gifts. The sponsor's brand and governance carry that trust (entrant simulation §7.3).
6. **Unproven value pools.**
   - The calibrated AI value pool at a large national is $445k [S].
   - The operating-cost pools that a redesign would remove are not publicly measured.
   - A buyer cannot verify a claimed saving without its own time-and-motion data.

## 4. What would be structurally hard for incumbents to replicate

The honest list is short.

1. **A business model that does not depend on asset retention or hidden layers.**
   - Under D, revenue comes from administration fees on programs plus platform and usage fees.
   - Published all-in costs and grant-out tooling do not cut against the provider's own revenue as directly as they cut against an affiliated manager's [I].
   - Incumbents *can* adopt this. The barrier is their own P&L, not their technology.
2. **Cross-sponsor decision and evidence data.** A layer running for several sponsors accumulates a back-test corpus, eligibility history and exception statistics that no single sponsor has. Persistence requires sponsors' permission to pool de-identified data, which is unverified.
3. **Recipient-side network effects.** Verified payment profiles and remittance acknowledgments reused across sponsors lower each new sponsor's onboarding cost. Chariot is pursuing a similar network on the rails side [V], so this is contested.
4. **An organization designed for few people from the start.** Incumbents can automate, but reorganizing a staffed operation is slower than starting without the staff. *Counter-case:* the largest affiliated nationals already run with very low staff cost (2.9 bps at affiliated-commercial sponsors, whose staff sit at the parent [V]). The advantage over them is small; the advantage is over community foundations and independents.

**Counter-case to the whole section:**
- Ren, Foundation Source and TIFIN Give have distribution, data custody and capital.
- Ren already markets instant approvals.
- If any of them adopts policy-as-code with published metrics and open exports, the entrant's differentiation shrinks to execution quality.
- That is why the comparison treats acquisition by a consolidator as a realistic outcome, not a failure (P2).

## 5. Customers: who would buy, resist or prefer outsourcing

The segment table is in [business-model-options.md](business-model-options.md). In short:

| Group | Stance |
|---|---|
| Independent sponsors with in-house or mixed stacks; mid-size CFs under cost pressure; wealth platforms seeking multi-sponsor flexibility; nonprofits (as beneficiaries) | **Most likely buyers** |
| Affiliated nationals; fee-share structures; advisors who fear grant acceleration | **Most likely to resist** |
| Tail CFs (median 24 DAFs); banks and trust companies | **Most likely to outsource entirely** |
