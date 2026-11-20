# Clarity and EDF: tests of conventional commercial assumptions

**Date:** 2026-11-20. **Frameworks:**
- Clarity, `kemiller2002/clarity-framework` at `200a9eb`: `rules.md`, `decision-posture-model.md`, `docs/reconsideration-criteria.md`, `docs/progressive-commitment.md`.
- EDF v0.3, `kemiller2002/echelon-diagnostic-framework` at `710d54c`: `docs/edf/specification.md`, `docs/framework-engineering/claim-and-confidence-policy.md`.
- Applied as specified in [clarity-edf-application-guide.md](../../mission-2026-11-14/clarity-edf-application-guide.md).

**Rules applied.**
- EDF is used only where an outcome has been observed (§2). Every other claim gets Clarity treatment only.
- Claim states (internal-demonstration, suggestive, unsupported, contradicted) and confidence labels follow the EDF policy. They are qualitative, not probabilities.
- Each conclusion separates five elements:
  - **O**bservation;
  - **E**vidence;
  - **A**ssumption;
  - **I**nference;
  - **R**ecommendation.

**Evidence references:**
- INV### refers to [phase0-repository-inventory.md](../evidence/phase0-repository-inventory.md) and [inventory.csv](../../../data/commercial-opportunity/inventory.csv).
- DS## refers to [demand-signals-and-process-economics.md](../market-validation/demand-signals-and-process-economics.md).
- PS/PW/PV rows are the prospect CSVs in [`data/commercial-opportunity/`](../../../data/commercial-opportunity/).

**Admissibility screen (Clarity Constitution).** Two moves are excluded:
- *Prescription without a signal.* Each recommendation is gated by an observable entry condition.
- *Motivation substituted for incentives.* Buyer behaviour is explained by budgets, fee structures and liability, not by attitudes.

---

## 1. The eight assumptions

### A1. "DAF administration must remain highly manual"

- **O:** Sponsor job postings still describe manual work: an inbox, cheque follow-up, reconciliation. Boston Foundation's grants processor pays $60–65k; ImpactAssets' grant operations officer $125–138k (DS hiring). Only 2 of 15 sponsor postings name AI (INV022).
- **E:**
  - Routine charity verification can be eliminated by a continuous status subscription. In the repository model this wins with P = 0.94 (process P06).
  - Exceptions are about 7.4–7.8% of recipient lines on the core definition (DS anchors).
  - The legal liability for these steps sits with the sponsor and with any manager who knowingly agrees: §§4966/4967 (DE054; [ai-governance-failure-modes.md](../../mission-2026-11-14/ai-governance-failure-modes.md)).
- **A:** Today's manual effort reflects what the law requires.
- **I:** This is **contradicted for routine work and supported for exceptions.** Most manual handling of standard grants to listed public charities is habit, not legal necessity. Exceptions such as foreign grantees, benefit risk and complex assets do need human judgement. This matches the existing structural-versus-habit result for grant review ([industry-incentives-structural-analysis.md](../../mission-2026-11-14/industry-incentives-structural-analysis.md) §6.2).
- **Claim state and confidence:** suggestive, Medium. No sponsor publishes its exception rate or reviewer minutes (INV018).
- **R:** Sell *redesign of the routine path* (structured intake, continuous eligibility data). Do not sell automation of the full manual workflow.
- **Would change if:** measured exception rates above about 25% of grants, or a regulator or court treating per-grant manual review as part of exercising control.

### A2. "AI is primarily valuable for grant vetting"

- **O:** In the calibrated model, AI wins only for:
  - complex-asset intake;
  - non-standard grantee due diligence;
  - sanctions screening, in one variant.

  Redesign has the highest probability of ranking first in every calibrated scenario (DS process economics). The AI value pool at a large national is about $445k a year as an assistant [S].
- **E:**
  - Routine vetting is deterministic: IRS BMF/Pub 78 plus OFAC lists.
  - The largest per-sponsor pool is non-standard verification, at about $1.25m on a 1M-grant scenario [S].
  - Complex-asset intake runs about 500 cases a year at Fidelity, with an average of 65 days to liquidity (INV113).
- **A:** Grant volume is where the value lies.
- **I:** **Contradicted as stated.** The AI value sits in *document-heavy, low-volume, high-value* work (complex gifts, equivalency evidence). Routine vetting of high-volume grants does not need AI.
- **Claim state and confidence:** suggestive, Medium-High on direction. The pool sizes are scenarios.
- **R:** If an AI product is pursued later, target complex-asset intake and non-standard due-diligence packets. **Reject** standalone AI grant-review software (§3).
- **Would change if:** observed review-time data show large routine-grant handling costs at a national; or a sponsor publishes AI vetting results with measured error rates.

### A3. "Larger technology platforms necessarily produce better economics"

- **O:**
  - Cost per grant ranges from $55 (DAFgiving360) and $68 (Fidelity) to $134 (Vanguard Charitable) and $419 (NPT) (INV006).
  - Community-foundation costs run at 127–177 bps against 32 bps at nationals (INV007).
  - Pass-through sponsors earn thin margins: RCF +0.8% (INV009).
  - Vendor payments by mid-sized community foundations run $118k–$416k a year, regardless of platform (INV032–INV033).
- **E:**
  - The large platforms' economics come from **grant volume and an affiliated-asset fee model**, not from platform size alone.
  - Vanguard Charitable and NPT are large but cost two to six times more per grant.
  - Ren's revenue is concentrated: 85.8% of named 990 receipts come from three customers (INV055–INV059).
- **I:** **Contradicted.** Unit economics follow grant volume per account and the fee model. Platform scale is not the driver.
- **Claim state and confidence:** internal-demonstration (the figures), suggestive (the attribution); Medium.
- **R:** In assessments, benchmark cost per grant and per account, not platform features.
- **Would change if:** like-for-like costs for one sponsor before and after a migration show scale effects.

### A4. "Wealth managers should outsource the entire DAF relationship"

- **O:**
  - The wirehouses keep the adviser on the account. Morgan Stanley GIFT caps adviser fees at 1% (INV060).
  - Fidelity's adviser-managed programme holds $37.1bn, 46.9% of its investments (PW notes).
  - Broker-dealers and regional banks rent a sponsor plus a vendor (Ren, TIFIN/GiveClear, Charityvest/Foundation Source).
  - Mercer Advisors launched an in-house Philanthropic Services unit on 2026-11-10 (PW11).
  - Vanguard's Altruist chose Endaoment over Vanguard Charitable (INV066).
- **E:**
  - Adviser fees on DAF assets range from 0 to 2% (INV060).
  - Regions' published guide shows 0.60% to the bank plus 0.65% to the sponsor on the first $500k (PW24).
  - Adviser economics depend on keeping the assets.
- **A:** Advisers want to hand off complexity.
- **I:** **Contradicted for firms with scale.** Advisers prefer models that keep the relationship and the assets: adviser-managed DAFs on a rented sponsor. Outsourcing the whole relationship applies only to small RIAs without scale.
- **Claim state and confidence:** suggestive, Medium. Retention effects are untested (INV073).
- **R:** The advisory offer should be **designing a programme the adviser controls** (sponsor of record, vendor, fee design, data flows), not referring clients to a national.
- **Would change if:** evidence that clients move assets to national sponsors despite adviser-controlled options; or the 2023 proposed rule treating advisers as donor-advisors becomes final, which would raise adviser compliance costs.

### A5. "Every sponsoring organisation needs a full administration platform"

- **O:**
  - The long tail: 1,240 sponsors hold under $50m.
  - A tail community foundation's median operating cost is $630k with 5 staff (INV039).
  - Community foundations under $10m report a median IT spend of $81. Those with $10–50m report $42k (DS spend table; reproducible with `scripts/commercial_sponsor_spend_distribution.py`).
  - Only 2.2% of tail sponsors disclose any DAF contractor (INV042).
- **E:**
  - Foundant's CommunitySuite serves 361 community foundations as a whole-organisation system (INV029).
  - DAF administration is a module inside general community-foundation software, not a standalone platform.
- **I:** **Contradicted.** Most small sponsors need a module inside existing community-foundation software, or a sponsor-of-record partner. A standalone DAF platform is uneconomic below roughly $250m in DAF assets. In that band, "no intervention" wins in 87–100% of model runs (DS process economics) [S].
- **Claim state and confidence:** suggestive, Medium-High.
- **R:** Do not target sponsors under about $250m with paid assessments. Serve them, if at all, through published research or association channels.

### A6. "Customers want more features rather than simpler operations"

- **O:**
  - Complaints are dominated by grant delay. 117 complaint types are fixable and 47 structural (DS complaints, repo summary).
  - Every migration observed froze grant processing for about 3–5 weeks.
  - AEF's migration kept only two years of history (INV026).
  - Vendors announce many features. TIFIN Give has the most announcements and the least evidence of delivery (INV079–INV080).
- **I:** **Suggestive that buyers value reliability, data continuity and speed over features.** No buyer interview confirms it.
- **Claim state and confidence:** suggestive, Low-Medium.
- **R:** Lead with outcome metrics (turnaround, exception handling, migration continuity) in assessments. Test the claim in interviews (questions Q7 and Q12 in [interview-program.md](../market-validation/interview-program.md)).

### A7. "Professional certification necessarily produces commercial credibility"

- **O:**
  - DAFCP: no holder data, no postings, no FINRA listing (DE061–DE064).
  - CAP, after 20 or more years, is "preferred" and never "required" in postings (DE063).
  - The trademark rules bar firm-level use ([dafcp-commercial-value.md](../certification/dafcp-commercial-value.md) §2).
- **I:** **Contradicted for 2026.** Credibility with sponsors, investors and vendors comes from evidence and delivery, not designations.
- **Claim state and confidence:** suggestive, Medium.
- **R:** Hold DAFCP for research access only (Experimental posture).

### A8. "The most attractive markets are the largest markets"

- **O:**
  - The largest sponsors make technology decisions at parent firms (FMR, Schwab, Vanguard) and use large consultancies: Vanguard Charitable paid UST Global and Slalom about $9.9m (DS spend).
  - The biggest addressable spend sits where Echelon has the least access.
  - The visible discretionary buyers are community foundations of $250m–1bn: median IT $455k, outside services $1.29m (DS spend table).
  - Platform decisions at broker-dealers are dated: the LPL–Commonwealth conversion in Q4 2026, Stifel's spend trend (PW06, PW08).
- **I:** **Contradicted.** The attractive market is **mid-sized buyers with discretionary budgets and a dated trigger**, not the largest asset pools.
- **Claim state and confidence:** suggestive, Medium.
- **R:** Prioritise roughly 40–60 mid-sized community foundations and faith sponsors, plus about 10 broker-dealer and bank programmes facing a platform decision.

---

## 2. EDF diagnoses of observed commercial outcomes

### Outcome C1 (EDF-1): no public market for independent DAF assessment

**Observed outcome.** No public RFP for DAF administration software or DAF consulting appears in 2024–26 (DS RFP searches). No analyst firm covers DAF platforms (INV094). Vendor selection happens through migrations and generalist IT consultancies (DS spend).

| EDF element | Diagnosis |
|---|---|
| System context | US DAF sponsors and wealth programmes buying technology and advice. Focus: how independent expertise is (not) procured |
| Manifestations | No RFPs; no analyst coverage; generalist consultancies named in 990s; vendor-led migrations; no published SOC scopes or turnaround metrics |
| Origin network | **Organisational:** small IT teams; vendor-led selection. **Financial:** IT budgets of $100k–500k at mid-sized community foundations; tail sponsors cannot pay. **Informational:** no comparative data exists, so buyers cannot specify what to buy. **Regulatory:** no rule requires independent assurance. **Human:** peer referral networks (CF peer groups) |
| Propagation | Informational (peer referral, vendor demos) → organisational (single-vendor evaluations) → financial (multi-year contracts) |
| Evidence | Direct: 990 contractor lines, migration notices, absence of RFPs. Inference: buyer preferences (no interviews yet) |
| Control points | (1) Published comparative evidence that lets buyers specify requirements. (2) Peer networks: CF associations and CF Insights. (3) Trigger timing: migrations, renewals, mergers. (4) Partnering with the generalist consultancies already paid |
| Ranking | (1) evidence publication: high influence, controllable by Echelon, low cost. (3) trigger timing: high influence, moderate controllability. (4) partnering: moderate on both. (2) peer networks: moderate influence, low controllability |
| Classification | **Mixed.** Structural on the financial side (small budgets); habit and informational on procurement practice (no comparative data) |
| Confidence | Medium |
| Diagnostic sufficiency | Sufficient for the next responsible action: publish evidence and run interviews. Not sufficient to price a service |
| Unknowns | Willingness to pay; who decides on purchases; contract renewal calendars |
| Next responsible action | 15–20 discovery interviews ([interview-program.md](../market-validation/interview-program.md)) plus one published benchmark |

### Outcome C2 (EDF-0): due-diligence advisers on DAF-ecosystem deals are banks and law firms

- **Observation.** Ren (2023, 2025), Foundation Source (2023), Envestnet (2024) and Deed (2026) name banks and law firms. No commercial or technical due-diligence firm is named in public releases (PV rows).
- **Origin.** Diligence firms are rarely named in releases. This is a disclosure habit, so absence is weak evidence.
- **Control point.** Expert networks and the generalist due-diligence firms' sector benches.
- **Confidence.** Low-Medium that no diligence firm was used. Medium that public data cannot show it.
- **Next action.** Test the expert-network and subcontract route in interviews with 2–3 diligence practitioners.

---

## 3. Second-order effects and feedback loops

1. **Publishing independent comparisons creates a credibility asset.** It may also strain vendor relationships and close off paid vendor work. That is a real tradeoff. Vendor-paid work and independent ratings cannot coexist without information barriers and disclosure (PV notes).
2. **Migration advisory has a self-limiting loop.** The recent wave of migrations is mostly complete (PS notes), so demand is lumpy and tied to renewal cycles. A recurring product, such as a renewal benchmark or monitoring, smooths it.
3. **Regulatory triggers cut both ways.** A final §4966 rule would create demand for compliance assessment. Continued delay preserves the status quo (INV023).
4. **Sponsor-funded education shapes buyer expectations.** Sponsors fund the CE (INV108, DE020), so buyer criteria may favour incumbent features. Independent evidence has to work against an established framing.

## 4. Posture summary for Echelon's decisions

| Decision | Impact if wrong | Correctability | Posture |
|---|---|---|---|
| Run discovery interviews and publish one benchmark | Low | High | **Fast** |
| Pilot a paid assessment with one mid-sized sponsor | Moderate | High | **Experimental** |
| Accept paid vendor work | Moderate–high (independence) | Low | **Guardrail** |
| Build software | High | Low | **Strategic**: defer until three or more paying customers show repeat demand |
