# 23 - Strategic recommendations

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md. Every recommendation here is a RECOMMENDATION. None is an owner decision: the decisions that need the owner are registered as OD-CNO-01..13 in Unbound's open-question register.

## Summary

- **The question shifted during the research.**
  - The mission assumed that charity networks and onboarding are the incumbents' main barriers.
  - The evidence supports a narrower claim: they are real *switching costs* that slow a sponsor's move.
  - The adversarial review (ADVX-10, accepted as an unrefuted hypothesis) found no evidence that they are why sponsors choose or stay with a provider. Distribution and incentive alignment explain observed behaviour better:
    - white-label sponsor entities;
    - adviser and investment-manager economics, e.g. a $4.24M investment-adviser payment alongside $14.93M to RenPSG at MS GIFT;
    - fee carve-outs (98% of RCF fundholder fees go to Ren).
  - Only 1 of 26 national, faith and affinity sponsors left Ren's iPhi platform in 2023-2026, and none left for a new entrant.
- **What that means.**
  - Neutralising the charity network and onboarding barriers is *necessary but not sufficient*: it removes reasons a willing sponsor cannot move.
  - It does not create the reason to move. Unbound still needs a distribution and incentive answer (recommendation 10).
- **Track A, the charity network.**
  - The public directory is already commoditised.
  - What is reproducible: identity, status and monitoring, at about $316k a year to run under the full C0 cost model.
  - What is not quickly reproducible:
    - accumulated payee enrolments;
    - resolution of messy recipients;
    - audit-accepted decision history.
  - Strategy:
    - build the registry as a cost of doing business, staged to the recipients actually paid;
    - partner for rails, Chariot first;
    - keep destination evidence per sponsor in Release 1;
    - compete on correctness, provenance and charity convenience, not directory size.
- **Track B, onboarding.**
  - Migration is unavoidable for the ratified entry segment and is the largest variable cost: 46-58% of onboarding at 100k+ accounts, with a 2.5-6.2x swing from data quality.
  - Incumbents market migration but publish no outcomes.
  - Strategy:
    - make migration a deterministic, rehearsed, reconciliation-gated product capability;
    - publish per-migration outcome metrics;
    - offer exit terms that are better than incumbents'.
- **Economics.**
  - At 20 bps, onboarding can be included in the servicing fee for *added* sponsors: 10k accounts pays back in about 3.4 months on C0.
  - It cannot be included for the first sponsor, which does not pay back at P50 once platform fixed cost is carried.
  - 20 bps is a price *increase* against an incumbent taking 18.5 bps for staffed administration. Ren's self-staffed software is priced at about $81 per account and is not beatable at any modelled size.
  - So the first one to three sponsors need design-partner terms, and price positioning is unresolved.

## The ten decisions

Each entry gives the recommendation, the alternatives, the trade-offs, the evidence, the assumptions, reversibility and confidence.

### 1. Should Unbound maintain an independent charity registry?

**Recommendation: yes. Keep UNB-CHAR-DEC-001, but stage the scope to the recipients actually paid and treat the registry as mandated infrastructure, not a profit or moat lever.**

- **Alternatives:**
  - License Candid/GuideStar (from about $2,750 a year plus integration).
  - Rely on rail partners' directories.
  - Hybrid: own the identity and status core, and buy enrichment.
- **Trade-offs:**
  - Owning it costs about $316k a year at C0, range $107k-673k (20 rev 3). That is $5.42 per grant at 70k grants and $0.54 at 700k.
  - Licensing is cheaper at small scale. But Candid rests on the same IRS files, still cites superseded Rev. Proc. 2011-33, and would become a runtime dependency that a ratified decision rejects.
  - Owning it gives replayable, provenance-bound decisions. It also gives a §8.01 reliance report: Rev. Proc. 2018-32 lets a grantor rely on a third-party report that meets its conditions.
- **Evidence:**
  - Every incumbent's US directory rests on the IRS EO BMF (1,984,891 EINs) and Pub 78 (1,437,288) (02, 03, 04).
  - Public data is sufficient for status reliance but not for subordinates, church status, existence or bank ownership (04, 05).
  - ADVA and ADVX both tested the build-vs-buy question and the decision survived, with a cost caveat.
- **Assumptions:** registry engineering does not crowd out core servicing build (ADVX-08). Stewardship labour is as modelled.
- **Reversibility:** high for scope, which can be staged and widened. Moderate for the decision itself: the data model is built either way, but licensing later would add a dependency.
- **Confidence:** Medium.
- **Reconsideration trigger:** run cost per grant stays above about $2 after the first three sponsors, or engineering capacity becomes the binding constraint.

### 2. Should its public data be openly distributed?

**Recommendation: not in Release 1. Keep the public layer publication-ready: verbatim public facts only, with provenance and licence (UNB-CNET-024). Decide later (OD-CNO-09).**

- **Alternatives:** an open dataset now; a public API; a searchable directory; a commercial data service.
- **Trade-offs:**
  - Publishing changes little competitively, because the directory is already commoditised by the IRS, ProPublica and Candid.
  - It adds support burden, liability exposure (defamation risk if any judgment leaks in) and licence management.
  - The genuinely new public good would be an open, reliance-grade status and identity crosswalk with posting dates. That could also build credibility with sponsors and auditors.
- **Evidence:** licensing terms (04). ADVX-09 tested whether publication would erode incumbent advantage and found it would not; ADVX rejected the challenge.
- **Assumptions:** none material.
- **Reversibility:** high, since publishing later is always possible.
- **Confidence:** Medium-High.

### 3. Does the registry warrant a separate repository or product?

**Recommendation: no, not now. Keep it as a module of Unbound's component monolith (CNV-ARC-001). If anything becomes a reusable Echelon component, it should be the *provenance and temporal-claim engine*, not the data. No new repository without explicit owner approval.**

- **Alternatives:** a separate repository or product now; an Echelon component now.
- **Trade-offs:** separation adds release, contract and governance overhead before there is a second consumer. The engine has broader reuse value than the charity data.
- **Evidence:** 05 distribution analysis. No external demand evidence exists.
- **Reversibility:** high, because a module boundary can be extracted later.
- **Confidence:** Medium-High.

### 4. Build, buy or partner for electronic payments?

**Recommendation: partner for rails, buy verification signals, build the evidence and routing layer.**

- **Partner for rails:** Chariot first (ratified CNV-PAY-007 via OD-P-PAY cut B), then PayPal Grant Payments once its terms pass the CNV-PLT-012 gate, plus sponsor-originated ACH fallback.
- **Buy verification signals:** owner match from at least two vendors (UNB-CNET-017).
- **Build:** the evidence and routing layer, made up of the rail-class taxonomy (UNB-CNET-013), separated destination evidence and acceptance (UNB-CNET-014) and partner contract minimums (UNB-CNET-018).
- **Activate a second rail before scale** (UNB-CNET-026).
- **Alternatives:**
  - A proprietary network. This is excluded: CNV-LEG-001 forbids Unbound holding funds.
  - Pass-through intermediaries such as PayPal Giving Fund or Benevity. These are excluded as grant rails because they change the legal payee.
  - Sponsor ACH only.
- **Trade-offs:**
  - Chariot is the only partner with a public grantmaker API, and it keeps funds in transit in the sponsor's own account at Column N.A.
  - But it serves direct competitors (Daffy, Endaoment, TIFIN Give), depends on a single bank (FDIC cover $250k per depositor), and locks charities into a Chariot account.
  - A sponsor can still pay a Chariot-enrolled charity by its own ACH to that account, which caps Chariot's pricing power over sponsors.
- **Evidence:** 07, 08 and ADVA-01/-03/-12. The c10 amendment allows exactly two destination-evidence combinations, and Chariot's model fits neither without contract terms: this is OD-CNO-02.
- **Assumptions:** Chariot accepts the contract minimums; owner-match coverage of nonprofit accounts is adequate (unpublished).
- **Reversibility:** moderate. Rails sit behind a provider-neutral contract.
- **Confidence:** Medium-High for the shape; Low-Medium for the economics.

### 5. Can shared vetting neutralise incumbent network advantages?

**Recommendation: partly, for public facts only.**

- **Share across sponsors in Release 1:** identity, status and public-fact holds re-verified from primary sources (CNV-GRT-004), and group-roster evidence (UNB-CNET-006).
- **Do not share in Release 1:** bank-destination evidence or any private finding. That is deferred pending counsel on imputed awareness and loss allocation (OD-CNO-05).
- **Shared vetting is parity, not advantage.** CAF America validates once and reuses for 1-3 years. Chariot verifies once for all partners. Ren validates once.
- **What incumbents actually hold** is the accumulated *payee* layer and audit-accepted history, which public data cannot neutralise. Only time and charity convenience can.
- **Trade-offs:**
  - The benefit of sharing destination evidence is small: $1.35-4 per enrolment avoided.
  - The cost is correlated risk: one deception exposes every relying sponsor.
- **Evidence:** 03, 05, 08, 09 and ADVA-13/-15.
- **Reversibility:** high, since sharing can be enabled later under a reliance policy.
- **Confidence:** Medium.

### 6. Should onboarding be a separately marketable capability?

**Recommendation: not as a standalone product. Market it as *verifiable outcomes* inside the servicing offer:**

- history depth imported;
- reconciliation proof;
- freeze length;
- login and enrolment carry-over;
- on-time delivery from receipt of a usable extract.

These go in a Migration Service Commitment limited to steps Unbound controls (UNB-ONB-030). Pair it with exit terms better than incumbents': self-service export, at least 90 days of read access, and no export fee (UNB-ONB-029).

- **Alternatives:**
  - A standalone migration service for other platforms' customers.
  - A switching guarantee modelled on CASS/ACATS. This was withdrawn: DAFs lack the regulatory compulsion, central utility and counterparty obligations those schemes rely on.
- **Trade-offs:** a standalone service competes with system integrators and adds delivery risk without the servicing revenue that pays for it.
- **Evidence:** 10, 11, ADVB-03/-12. Ren, akoyaGO, Give Interactive, Foundant and Salesforce partners already sell migration; none publishes outcomes.
- **Reversibility:** high.
- **Confidence:** Medium.

### 7. Should migration assessments be offered before contracting?

**Recommendation: yes, in exposure tiers (UNB-ONB-003).**

- **T0:** a questionnaire.
- **T1:** sponsor-side schema and statistics profiling, run on standard reports the sponsor can download itself, so no personal data leaves the sponsor and the incumbent is not alerted.
- **T2:** row-level data only under an NDA and DPA.
- **Classification:** each assessment classifies the migration as PlatformReplacement, ProgramTransfer or Greenfield (UNB-ONB-001).
- **Output:** a deterministic price band and time estimate (UNB-ONB-004).
- **Alternatives:** post-contract discovery (the industry norm); full-data assessment (privacy and signalling risk).
- **Trade-offs:**
  - Pre-contract work costs Unbound effort before revenue.
  - It also surfaces the data-quality swing (2.5-6.2x) before price is committed. That is what makes fixed pricing safe.
  - Requesting a paid incumbent export signals intent to leave, which is why T1 avoids it.
- **Evidence:** 13, 20, ADVB-14.
- **Reversibility:** high.
- **Confidence:** Medium-High.

### 8. Can onboarding be predictably priced?

**Recommendation: yes, inside a published data-quality and integration gate, for added sponsors.**

- **Added sponsors:** at 20 bps, a 10k-account sponsor pays back in about 3.4 months (P10-P90 3.9-6.6) on C0, so onboarding can be included in the fee.
- **First one to three sponsors:** these need design-partner terms. A first 10k-account sponsor nets about $63k a year against about $3.04M of platform fixed cost, which never pays back at P50.
- **Out-of-gate work:** quoted separately and charged up front.
- **Early exit:** recovery limited to the published straight-line unamortised balance.
- **Small sponsors:** need a minimum annual fee of about $220k at C0 for 1k accounts, or about $160k if the AI-native levers are proven.
- **Uneconomic cases:**
  - processor-like books (about $7k average balance) at any fee from 10 to 30 bps;
  - small sponsors with poor data, many integrations and high grant volume;
  - any size at Ren's roughly $81 per-account software price;
  - markets at 10-15 bps below about 10k accounts.
- **Evidence:** 20 rev 3, ADVX-03 to ADVX-07, ADVB-05/-13.
- **Assumptions:**
  - The 20 bps working scenario (a price increase against 18.5 bps incumbents).
  - Migration exception rates and minutes, which are unmeasured.
  - CNV-ECO-003 conformance is still partial: no adverse licence scale, no correlated draws, no measured levers.
- **Reversibility:** high until contracts are signed.
- **Confidence:** Low-Medium.

### 9. What must exist before the first institutional customer?

**Recommendation (subject to OD-CNO-01; the coordinator recommends option (a)).**

**Charity network minimum:**
- Release-based ingestion with archive and freshness: UNB-CNET-003, -004.
- Three time axes and authority lattice: UNB-CNET-001, -002.
- Conflict and subordinate handling: UNB-CNET-005, -006.
- Materiality, sanctions polling and reinstatement: UNB-CNET-007, -008, -009.
- Universe-wide monitoring: UNB-CNET-010.
- Rail taxonomy, evidence separation and risk tiers: UNB-CNET-013, -014, -015.
- Legacy-imported destinations: UNB-CNET-016.
- Integrity gates and AI non-application: UNB-CNET-021, -022.
- Nacha programme: UNB-CNET-023.
- At least one certified rail with the contract minimums: UNB-CNET-018.
- Sponsor-originated ACH fallback plus positive-pay checks: ratified.

**Onboarding minimum:**
- Migration class and extraction plan: UNB-ONB-001, -002.
- Canonical package, legacy partition, epoch and history disclosure: UNB-ONB-006, -007, -008.
- Vault: UNB-ONB-009.
- Deterministic runs and rehearsal gate: UNB-ONB-010, -011.
- Reconciliation gates: UNB-ONB-013.
- Accounting continuity and auditor evidence: UNB-ONB-014, -015.
- Cutover rules, irreversibility boundary and in-flight ownership: UNB-ONB-016, -017, -018.
- Single statement issuer: UNB-ONB-019.
- Payee verification campaign: UNB-ONB-021.
- Configuration package and certification: UNB-ONB-023, -025.

**Can wait:**
- The public-layer publication: UNB-CNET-024.
- The charity-scoped vault: UNB-CNET-020.
- Self-service readiness: UNB-ONB-026.
- Federation reliance and SCIM: UNB-ONB-027, -028.
- Capacity scheduling: UNB-ONB-031.

**Trade-offs:** the migration minimum adds scope to Release 1. Omitting it means the first sponsor must be greenfield, which conflicts with the ratified entry segment (CNV-ECO-004) and with CNV-ECO-003's real-sponsor replay.

**Confidence:** Medium.

### 10. Which competitive barriers remain after these recommendations?

**Recommendation: maintain them in a register with owners (UNB-ONB-033) and treat items 1-3 as the main strategic problem.**

| # | Remaining barrier | Why the recommendations don't remove it | Possible response (hypothesis) |
|---|---|---|---|
| 1 | Distribution and incentive alignment: white-label sponsor entities, adviser and investment-manager revenue, fee carve-outs | Unbound is not a sponsor, holds no funds and gives no investment advice (CNV-LEG-001), so it cannot offer the same incentives | Neutrality on investments and custody (adviser-managed accounts, any custodian feed) as the pitch to advisor-distributed sponsors; partnerships with sponsors that need an administrator |
| 2 | The sponsor-of-record problem for vendor-charity programmes (RCF, NPT, Charityvest, GiveClear) | Moving means fund-by-fund grants approved by the old sponsor, with no history (UNB-ONB-001) | A sponsor-entity partner, or programmes that start on a sponsor Unbound serves |
| 3 | Incumbent platform integration and relationships (1 of 26 left Ren's iPhi; no exit to a new entrant) | Technology parity does not overcome relationship inertia | Win/loss research; design partners |
| 4 | Accumulated payee enrolments and charity familiarity | Takes 23-65 months to reach 67% electronic at realistic conversion | Charity convenience (no portal), targeted outreach to top recipients, partner rails |
| 5 | Audit-accepted history and SOC reports | A new entrant has no Type II report for the first sponsor's period | Evidence pack, Type I at go-live, auditor engagement (UNB-ONB-015) |
| 6 | Price | Ren self-staffed software at about $81 per account; 18.5 bps for staffed administration | Unresolved; price positioning needs the CNV-ECO-003 evidence |
| 7 | Brand and trust | Not addressable by product requirements | Out of scope |

## Implications for Unbound

- Requirements are proposed in `unbound: requirements/discovery/2026-11-26-charity-network-and-onboarding/`: 26 UNB-CNET and 33 UNB-ONB records, all proposed, none implemented or validated, plus 13 owner decisions.
- The most valuable next evidence is not more desk research but:
  1. win/loss and switching-reason interviews with sponsors that moved or considered moving;
  2. one authorised real export from an incumbent;
  3. a measured conversion rate for grant-triggered enrolment.

## Open questions / evidence gaps

See 24.
