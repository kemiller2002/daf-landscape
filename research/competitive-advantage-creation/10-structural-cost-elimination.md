# 10 - Structural cost elimination

Status: research (2026-11-26). Track H. Agent HI. Extends the Phase II event model ([09](../competitive-displacement/09-event-level-operating-model.md), [10](../competitive-displacement/10-zero-touch-administration-economics.md); inputs [events.csv](../competitive-displacement/data/model-inputs/events.csv), [parameters.csv](../competitive-displacement/data/model-inputs/parameters.csv)) and reuses the file-ingestion package ([08](../file-ingestion-and-straight-through-processing/08-STP-OPPORTUNITIES.md), [09](../file-ingestion-and-straight-through-processing/09-ECONOMIC-ANALYSIS.md)). Register fragments: `data/fragments/HI/operational-events.csv` (25 Phase II events plus 16 new P3-EV-HI events), `assumptions.csv`, `claims.csv`. Per-event decomposition for three scenarios: `data/evidence/HI/event-work-decomposition.csv`. Nothing here is measured from a live DAF operation; every figure is a recomputation of labelled Phase II inputs under a stricter accounting rule. Legal and regulatory references are research pointers, not legal conclusions; counsel confirms.

## Answer in brief

1. **Most of the removable work is automated, not eliminated.** Of about 183 conventional human minutes per account-year, the redesign in Phase II removes about 130 (base). Classified by what actually happens to the work: **automated ~82 min (range 29-112), eliminated ~37 min (25-47), accelerated by AI ~9 min (5-15), transferred to customers ~2 min (1-2), transferred to partners ~7 min (3-15)**; residual staffed work ~46 min (14-98), of which **~28 min (9-59) is mandatory** (P3-CLM-HI001). In labour dollars (Phase II rates, 75% utilisation): automated ~$121 ($44-165), eliminated ~$55 ($37-70), accelerated ~$14 ($8-23) per account-year.
2. **Automated work is not free.** It moves to compute, connectors, rule maintenance, model oversight and audit scope, which Phase II already carries as fixed cost (MD-5 fixed $2.5M). Only eliminated work leaves no ongoing cost other than its prevention mechanism (about $2.1 per account-year in Phase II prevention costs).
3. **Preserving the 180-day validity ceiling (DEC-003) turns charity re-vetting into automation, not elimination.** The renewal still happens every 180 days; a machine performs it (RR-REQ-X-007-r2 automatic renewal). What is genuinely eliminated in vetting is duplicate checking (evidence reuse across grants and sponsors; 64-72% reuse measured in the Unbound public-data replay) and document collection the IRS already publishes (P3-CLM-HI002).
4. **The largest single eliminable exception remains pooled-receipt attribution** (FIE finding 2): a notification-first contribution intent that generates the fund reference carried in the DTC note, wire memo or check memo makes matching deterministic. It is elimination only if the intent replaces the notification form sponsors already require; if it is an extra donor step it is a transfer (P3-CLM-HI003).
5. **Customer experience and economics improve together wherever the fix is upstream input design** (closed charity picker, rules at recommendation time, structured intents, IRS data instead of charity documents, self-service status). They pull apart where the control is a hold or step-up (bank-change holds, fail-safe stale-source holds, first-payment caps, sanctions potential matches).
6. **Several Phase II savings would be double counted if prevention and automation were both credited** (section 9): the registry run-cost model and EV-E08 vetting labour price the same work; change-driven monitoring appears in EV-E08 prevention and in the registry's 180-day comparison; E04 prevention and the FIE prevention scenario are the same mechanism; E07/E09/E10 credit one input-design change three times. Savings must be computed as sequential residuals and never summed across models (P3-CLM-HI004, P3-DEC-HI001).
7. **What cannot be eliminated**: sponsor reserved authority and section 4967 review on non-routine grants, sanctions potential-match disposition and blocking/reporting, identity proofing, qualified appraisal of complex assets, successor verification, audit preparation (held until an auditor walkthrough, V-9), controller sign-off on external reconciliation breaks, mandatory acknowledgment content, Nacha fraud monitoring, rail and transfer pass-through costs, first-time verification of recipients that public lists do not cover (churches, government units, subordinates; ~11% of Schedule I rows), and the named accountable owner for eligibility (section 10).

**Revision 2 (2026-11-26; round-1 review).**
- **Baseline (P3-CHL-REV1003, P3-CHL-REV2032).** The 183-minute "conventional" baseline is a hypothetical, labour-intensive administrator. It is not a well-automated incumbent. In any competitive or sponsor-facing use, quote savings against the MD-3/MD-4 well-automated baseline, where the modelled gap is about $11-71 per account-year ([13](13-incumbent-response-model.md) §3.2). Most of that gap is process redesign and deterministic automation, which incumbents already claim; AI acceleration is ~9 minutes.
- **Measurement (P3-CHL-REV2031).** All minutes and savings here are conditional on V-7 and pilot measurement, and they should not feed price floors until measured (§11).
- **180-day renewal (P3-CHL-REV3020, P3-CHL-REV3010).** Item 3 describes machine renewal as the design, but it is **not adopted**. UNB-CDD-CIV-008 retains the deep review at the CNV-GRT-003 interval under the ratified wording until the owner decides OD-CDD-02. Until then, the compliant base for re-vetting is a human deep review every 180 days ([11](11-continuous-charity-intelligence.md) §5, M1). Machine renewal is conditional on OD-CDD-02, SPD-GRT-001, V-3 and V-9.
- **Customer-side switching cost (P3-CHL-REV1043, P3-CHL-REV3040).** The system-cost comparison leaves out the sponsor's one-time conversion labour: validation, re-keying, re-papering, training, parallel run, auditor time, communications, and any paid export or early termination. That labour runs to hundreds or 1,000+ hours for thousands of accounts, against a modelled $11-71 per account-year gap to automated incumbents. It is a transfer to the customer, and every sponsor value case must show it. V-1 stayer interviews should test it.

## 1. Method and definitions

The Phase II formula is unchanged ([09 §1](../competitive-displacement/09-event-level-operating-model.md)). What changes is how the removed minutes are classified. For each event *e*, at Phase II parameters:

```
C   = freq × p_conv × d_conv                                (conventional minutes)
N0  = freq × p_native × d_exception                         (exception design, no prevention, no AI)
N1  = N0 × (1 − prev_efficacy × prevention_scale)           (after upstream prevention)
N2  = N1 × ai_assist_duration_factor                        (after AI preparation)
automated + reclassified = C − N0;  eliminated += N0 − N1;  accelerated = N1 − N2;  residual = N2
```

Savings are taken **sequentially on the residual** of the previous step, so no minute is credited twice inside the event model. Categories (REGISTERS vocabulary):

| Category | Test applied | Ongoing cost that remains |
|---|---|---|
| eliminated | The work no longer arises for anyone (no exception, no review, no document) | Prevention mechanism cost |
| automated | The work still happens, performed by a deterministic rule or job | Compute, connectors, rule maintenance, audit scope |
| accelerated | A person still does it, faster (AI preparation) | Model cost, oversight, evaluation |
| transferred-to-customer | Donor, advisor or sponsor now does it | Customer effort; sponsor labour at lower efficiency in licensing (PAR-021 ×1.4) |
| transferred-to-partner | Bank, custodian, rail partner, advisor firm, central organisation or fiscal sponsor does it | Partner fees; dependency; concentration |
| deferred | Out of the initial scope or postponed (grant held, capability not offered) | Reappears later or is lost revenue |
| mandatory | Required by law, contract or an approved control; can be automated only in its preparation | Labour floor |

Reclassifications made here against Phase II's step labels (assumptions P3-ASM-HI020..HI024): half of the EV-E08 workflow saving is elimination (reuse, IRS data replaces letters; range 30-70%) and half automation (status checks and machine renewal); EV-E07 (closed picker) and EV-E20 (false-alert reduction by a tuned matcher) are elimination; EV-E16 is transferred to advisor firms (UNB-ONB-028); 80% of EV-E17 and 30% of EV-E01 removal is self-service or prefill performed by the customer; EV-E11/E12 residual is transferred to the networked rail partner that CNV-PAY-001 names for release 1 (payment execution itself is deferred, PAY-DEF-001).

Scenarios: **base** = Phase II base; **pessimistic** = Phase II stress (touches ×1.5, minutes ×1.3, AI factor 0.88) with prevention at quarter efficacy and 30% of E08 as elimination; **optimistic** = touches ×0.6, minutes ×0.7, AI 0.75, full prevention efficacy, 70% of E08 as elimination.

## 2. Event-by-event (base, human minutes per account-year)

| Event | Conv. | Automated | Eliminated | Accelerated | To customer | To partner | Residual mandatory | Residual other | Main mechanism |
|---|---|---|---|---|---|---|---|---|---|
| E01 Account opening | 2.5 | 1.4 | 0.1 | 0.1 | 0.6 | 0 | 0 | 0.3 | Configuration, in-app agreement, prefill |
| E02 Identity verification | 0.5 | 0.3 | 0 | 0 | 0 | 0 | 0.1 | 0 | Vendor proofing; step-up |
| E03 Contribution posting | 12.0 | 10.2 | 0.3 | 0.2 | 0 | 0 | 0 | 1.3 | Structured bank/custodian feeds |
| E04 Attribution (pooled receipt) | 6.0 | 2.7 | 1.0 | 0.3 | 0 | 0 | 0 | 2.0 | Notification-first intent, unique reference |
| E05 Complex assets | 2.2 | 0.7 | 0 | 0.2 | 0 | 0 | 1.3 | 0 | Qualified appraisal stays |
| E06 Investment allocation | 1.5 | 1.2 | 0 | 0.1 | 0 | 0 | 0 | 0.3 | Model-portfolio constraints |
| E07 Charity discovery | 2.7 | 0 | 1.5 | 0.2 | 0 | 0 | 0 | 1.0 | Closed picker on shared public evidence |
| E08 Charity vetting | 50.0 | 22.3 | 23.7 | 0.6 | 0 | 0 | 0 | 3.4 | Reuse + IRS data (eliminated); machine renewal (automated) |
| E09 Recommendation intake | 9.0 | 7.5 | 0.4 | 0.2 | 0 | 0 | 0 | 1.0 | Validated forms, bulk API |
| E10 Grant approval | 55.8 | 21.8 | 4.3 | 4.5 | 0 | 0 | 25.3 | 0 | Rules at recommendation; reserved authority stays |
| E11 Payment processing | 12.7 | 5.2 | 1.1 | 0.9 | 0 | 5.4 | 0 | 0 | Networked rail partner (CNV-PAY-001) |
| E12 Payment failures | 2.7 | 0.5 | 0.6 | 0.3 | 0 | 1.4 | 0 | 0 | Verified destinations, positive pay |
| E13 Reconciliation | 10.0 | 5.8 | 1.0 | 0.5 | 0 | 0 | 0 | 2.7 | Continuous reconciliation (external breaks remain) |
| E14 Statements, acknowledgments | 4.0 | 3.6 | 0 | 0.1 | 0 | 0 | 0 | 0.4 | Generated 170(f)(8) acknowledgments |
| E15 Customer contacts | 5.0 | −1.7 | 1.0 | 0.8 | 0 | 0 | 0 | 4.8 | Self-service status; residual contacts are harder |
| E16 Advisor administration | 0.9 | 0 | 0 | 0.1 | 0 | 0.5 | 0 | 0.3 | Firm-managed provisioning |
| E17 Account changes | 1.8 | 0.3 | 0.1 | 0.1 | 1.0 | 0 | 0 | 0.4 | Self-service with step-up |
| E18 Succession | 1.2 | 0 | 0 | 0.2 | 0 | 0 | 1.0 | 0 | Human verification stays |
| E19 Fraud investigation | 0.4 | 0 | 0.1 | 0 | 0 | 0 | 0.2 | 0 | Callbacks, bank-change holds |
| E20 Sanctions exceptions | 2.0 | 0 | 1.8 | 0 | 0 | 0 | 0.2 | 0 | Tuned matcher (0.9 vs 10.5 alerts per 1,000 names) |
| E25 Account closure | 0.6 | 0.4 | 0 | 0 | 0 | 0 | 0.2 | 0 | Final distribution approval stays |
| **Total** | **183.3** | **82.2** | **36.9** | **9.3** | **1.7** | **7.3** | **28.3** | **17.7** | |

E15 shows negative automation: residual contacts take longer than average conventional contacts. Sponsor-level events (minutes per sponsor-year, conventional → AI-native): E13 close 28,800 → 9,000 (automated, residual controller sign-off and external breaks), E20 incidents 2,400 → 1,800 (mandatory), E21 reporting 4,800 → 2,640 (data assembly automated; reporting mandatory), **E22 audit 7,200 → 7,200 (mandatory; no reduction until V-9)**, E23 configuration upkeep 7,200 → 3,600 (automated by declarative configuration); E24 migration one-time 18,000 + 6/account → 9,000 + 2/account (automated by reproducible migration).

Per-event frequencies, preventable and residual touches, processing, prevention and failure costs, control effectiveness, customer experience and operational risk are in the fragment register. Units there: frequencies are human touches per account-year (sponsor-level rows in minutes per sponsor-year); processing cost is dollars per touched event (AI-native minutes per touch at loaded rate ÷ 0.75); prevention cost is dollars per account-year; failure cost is the AI-native failure lifecycle cost per failed event.

## 3. Totals per account-year

| Category | Minutes base (pess-opt) | Labour $ base (pess-opt) | Who carries it afterwards |
|---|---|---|---|
| Automated | 82 (29-112) | 121 (44-165) | Platform (fixed cost) |
| Eliminated | 37 (25-47) | 55 (37-70) | Nobody; prevention cost ~$2.1 |
| Accelerated (AI) | 9 (5-15) | 14 (8-23) | Staff, with model cost |
| Transferred to customer | 2 (1-2) | 2 (2-3) | Donor/advisor |
| Transferred to partner | 7 (3-15) | 11 (4-22) | Rail partner, advisor firm |
| Residual mandatory | 28 (9-59) | 42 (14-89) | Sponsor/administrator |
| Residual other | 18 (5-38) | 26 (7-56) | Sponsor/administrator |

**E07 (Revision 2, P3-CHL-REV3015).** E07 is not wholly eliminated. Identity resolution recurs at every recommendation: free text to an EIN and a payable entity, multi-unit EINs, DBA versus legal name, and ~9,200 ambiguous EINs (UNB-CNET-005). A closed picker that is too strict pushes this work to e-mail (§8). Treat the 1.5 minutes credited to elimination as an upper bound, and add a per-recommendation identity-resolution event (not modelled in model revision 2; open).

Two mode-level transfers dominate everything above and must be reported separately, never as savings:
- **Technology-only licensing (MD-6)** moves all residual minutes (~53) to the sponsor at ×1.4 efficiency (~74 sponsor minutes). Phase II's vendor variable cost of $31 per account is a transfer; the system cost rises to $197 against $167 for AI-native administration ([10 §1](../competitive-displacement/10-zero-touch-administration-economics.md)).
- **Payment execution** in Unbound release 1 is a rail-partner function (CNV-PAY-001, PAY-DEF-001); its labour and fees sit with the partner and the sponsor. Unbound itself is a Nacha Third-Party Service Provider under CNV-PAY-001. It carries the TPSP obligations (annual Rules compliance audit, risk-based fraud monitoring, audit cooperation) as a base cost of the platform, not of the partner (Revision 2, P3-CHL-REV3019).

## 4. New events (P3-EV-HI001..016)

Events Phase II did not model, mostly from Track I. Rates are per charity-year unless stated; conversion to per account-year uses 2 charities in use per account (P3-ASM-HI030; 20,000 charities for a 10,000-account sponsor).

| ID | Event | Rate | Human share | Category | Basis |
|---|---|---|---|---|---|
| P3-EV-HI001 | First-time verification of a recipient not covered by IRS lists (church, government unit, subordinate, no EIN) | 0.035 (0.02-0.05) | 100%, 25 min | mandatory (once; then reused) | Unbound replay: first-time incidence 4.0% within sponsor, 3.1% platform |
| P3-EV-HI002 | Automated 180-day renewal of common verification | 2.0 | 1% fail to human (0.5-3%) | automated | DEC-003 ceiling; RR-REQ-X-007-r2; failure rate from charity-network 06 (ASSUMPTION) |
| P3-EV-HI003 | Adverse eligibility-relevant source change | ~0.003-0.005 | ~10%, 45 min | automated (deterministic hold) | 405 of 236,750 monthly c3 changes; revocations 1.7 per 1,000 rows a year |
| P3-EV-HI004 | Informational or neutral source change (financials, address, name) | ~1.4 | 0 | eliminated | Materiality table (UNB-CNET-007); a naive rule creates ~585× more work |
| P3-EV-HI005 | Sanctions and exclusion list update rescreen; potential matches | rescreen ~120 OFAC action days a year; alerts 0.005 | alerts 100%, 10 min | mandatory (disposition) | OFAC action dates 112-132 a year; replay 0.9 alerts per 1,000 names |
| P3-EV-HI006 | Statistical sample review of auto-renewed verifications | 3 strata × 149 a year per registry | 100%, 15 min | mandatory (new detective control) | Attribute sampling, [11 §6](11-continuous-charity-intelligence.md) |
| P3-EV-HI007 | Source ingest failure, schema drift, implausible-delta quarantine | 24 (12-48) a year per registry | engineering 3 h | mandatory | UK list replacement (Jan 2026), OFAC format retirements, IRS 990 bulk outage (Nov 2025) |
| P3-EV-HI008 | Charity payment-destination change request | 0.05 (0.02-0.1) ASSUMPTION | partner verifies | transferred-to-partner | CNV-PAY-001/002 |
| P3-EV-HI009 | Charity impersonation or fraudulent destination change | 0.001 ASSUMPTION | 100%, 3 h | mandatory | Nacha false-pretenses monitoring |
| P3-EV-HI010 | Conflicting identifiers, identity dispute, merger or successor | 0.003 (0.001-0.01) | 100%, 30 min | mandatory | 31,600 EINs revoked-but-listed, ~9,200 ambiguous (UNB-CNET-005) |
| P3-EV-HI011 | Fiscal-sponsor project attestation refresh (12 months) | share of recipients unknown (0.5-3%) | on failure | transferred-to-partner (fiscal sponsor attests) | CNV-GRT-008; no licensed public directory |
| P3-EV-HI012 | Group-subordinate inclusion roster refresh (12 months) | per GEN | on failure | transferred-to-partner (central organisation) | UNB-CNET-006; 237,380 c3 subordinates absent from Pub 78 |
| P3-EV-HI013 | Donor contribution intent submission | ~1.25 per account-year (securities and wires) | donor 2 min | transferred-to-customer (zero net if it replaces existing forms) | FIE-A-024, FIE-A-079 |
| P3-EV-HI014 | Supporting-organisation certification captured inline from advisor | ~0.09 per account-year (1% of rows) | advisor | transferred-to-customer | UNB-RCN-REG-002; 4966(d)(4) |
| P3-EV-HI015 | Fail-safe hold because a source release was not ingested within its freshness limit | per incident | n/a | deferred (grant delayed) | CNV-GRT-003; UNB-CNET-004 |
| P3-EV-HI016 | Human deep review of tier-3 (high-risk) charities every 180 days | 2% of charities × 2 a year | 100%, 15 min | mandatory | risk-tiered monitoring, [11 §5](11-continuous-charity-intelligence.md) |

## 5. Mechanisms

| Mechanism | Events | Category produced | Dependency | Evidence |
|---|---|---|---|---|
| Input design (closed picker, purpose taxonomy, validation at entry) | E07, E09, E10 | eliminated / automated | None external | Replay: 88.8% of rows straight-through on IRS lists |
| Upstream validation (rules at recommendation time) | E10 | automated; mandatory residual | Sponsor policy delegation | Phase II efficacy cut to 0.25 (CHL-102) |
| Canonical identifiers (EIN binding, fund reference, GEN) | E04, E07, P3-EV-HI012 | eliminated | Sending institutions carry free text | FIE-A-001, FIE-A-123 |
| Structured exchange (BAI2/camt, custodian files, CSV/API bulk) | E03, E06, E09 | automated | One mapping per institution | FIE 05; 75-85% routine STP first months, 90% calibrated |
| Customer incentives (faster crediting for intents; fee waiver for e-payment enrolment) | E04, E11 | eliminated (if adopted) | Sponsor pricing | Unmeasured (P3-HYP-HI005) |
| Configuration | E01, E23 | automated | Declarative package | UNB-ONB-023 |
| Integration (custodian, advisor firm, rail partner) | E01, E11, E12, E16 | transferred-to-partner | Contracts | CNV-PAY-001 |
| Automated reconciliation | E13 | automated | External breaks remain | CHL-059 |
| Preventive controls (callbacks, bank-change holds, positive pay) | E12, E17, E19 | eliminated (loss), mandatory (control) | Nacha rules | Phase II E19 |
| Continuous monitoring (materiality table) | E08, P3-EV-HI003/004 | automated; informational changes eliminated | IRS release cadence | 405 of 236,750 monthly changes relevant |
| Self-service | E15, E17 | eliminated / transferred-to-customer | Step-up authentication | Phase II efficacy 0.3 |
| Shared public evidence | E07, E08, P3-EV-HI001 | eliminated (duplicate verification) | Sharing terms (OQ-010; DEC-004) | Reuse 64.4% same sponsor; 72.3% across 20 sponsors |
| Removing redundant approvals | see §6 | eliminated where policy, mandatory where law | Counsel | §6 |

## 6. Approvals: which are redundant, which are not

Research references only; counsel confirms each before any change.

| Approval or step | Basis cited | Assessment |
|---|---|---|
| Collecting a charity's determination letter | Rev. Proc. 2018-32 permits reliance on TEOS/Pub 78 and the BMF absent knowledge of change | Collection is redundant for listed public charities: **eliminated** (FIE 08 §2). Not for subordinates (§6.03 excludes them), new organisations not yet listed, or governmental units |
| Charity W-9 for grants to listed public charities | Inferred (FIE 08 §2) | Likely redundant; counsel to confirm |
| Full 180-day re-review by a person | Sponsor/platform policy, not IRS rule (CHL-035); 180-day ceiling preserved by DEC-003 | Human sign-off removable only where the sponsor's delegated policy allows automatic renewal (RR-REQ-X-007-r2(1), owner decision SPD-GRT-001); the renewal itself remains (**automated**) |
| Per-grant re-vetting of a charity already verified | RR-REQ-X-007-r2(4); CNV-GRT-003 (reuse as input) | Duplicate: **eliminated**; per-grant reliance snapshot stays (automated) |
| Sponsor approval of each grant | Section 4966(d)(2) defines a DAF by donor advisory privileges over assets the sponsor owns and controls | Approval authority cannot be removed; routine approvals can be executed by a sponsor-approved rule. Non-routine grants (4967 benefit, supporting organisations, expenditure responsibility) stay human: **mandatory** |
| Dual release of payments | Internal control; Nacha TPSP obligations (Unbound is a TPSP under ratified CNV-PAY-001; Revision 2: previously "where applicable") | Keep: **mandatory** (segregation of duties) |
| Sanctions potential-match disposition | OFAC regulations (31 CFR Part 501 reporting); CNV-GRT-006 | **Mandatory**; only false-alert volume can be eliminated |
| Contemporaneous written acknowledgment | Section 170(f)(8); for DAF contributions also section 170(f)(18)(B): the acknowledgment must state that the sponsoring organization has exclusive legal control over the assets contributed (Revision 2, P3-CHL-REV3024) | **Mandatory content**, automated generation. Legal review of the templates is a mandatory control, because the deduction depends on the exact content |
| Supporting-organisation donor-control certification | Section 4966(c)(2)(A) excepts distributions to 170(b)(1)(A) organisations *other than a disqualified supporting organization*; section 4966(d)(4) only **defines** a disqualified supporting organization. The statute requires no donor certification. Avoiding a taxable distribution to such an organisation is the sponsor's duty (4966(c)(1)(B)(ii), with 4945(h) expenditure responsibility) | A donor-control certification is a **sponsor procedure** (UNB-RCN-REG-002) that an advisor may supply inline. The underlying determination is **mandatory sponsor work**, not a transfer to the customer. **Revision 2 (P3-CHL-REV3023):** this row previously cited "Section 4966(d)(4)" as the basis and classified the work as "transferred-to-customer" |
| Audit preparation | Sponsor audit; SOC 2 | Held at conventional minutes until an auditor walkthrough (V-9) |

## 7. Pooled-receipt attribution (reuse of the file-ingestion research)

FIE established that the industry's main ingestion exception is attribution, not parsing: gifts land in a pooled sponsor account and the fund key travels in free text that sending institutions do not reliably carry (FIE-A-001, FIE-A-123). The documented responses are notification-first, rejection, or hold-and-sweep (FIE-A-079). The redesign (FIE-A-135) issues a unique reference at intent capture and generates the transfer instructions containing it.

Classification: the **investigation** is eliminated; the **intent** is customer work. Many sponsors already require a notification form (NPT, GKCCF, The Signatry), so a structured intent that replaces that form adds no net donor work and improves the experience (immediate reference, confirmation, faster crediting). Where no form exists today it is a transfer to the donor and must be reported as such. Virtual accounts, where a bank provides them, transfer matching to the bank (partner fees). In the Phase II model E04 prevention removes ~1.0 minute and its residual is ~2.0 minutes per account-year at half efficacy; FIE's own model has investigations at 1-2-5% of records and 30-45-135 minutes as the decisive unknown, with prevention at 30-50-60% for $0.5-1-3 per fund. **Use one of the two, not both** (§9).

## 8. Where customer experience and economics improve together

| Together (upstream input design) | In tension (holds and friction) |
|---|---|
| Closed charity picker: instant search, no assisted searches (E07) | Bank-change holds and callbacks (E17, E19): delay, but prevent ~$20k losses |
| Rules evaluated at recommendation: instant answer instead of later rejection (E10) | Fail-safe holds when an IRS release is not ingested (P3-EV-HI015): delays grants for reasons the donor cannot see |
| IRS data instead of charity documents; no charity portal (E08, UNB-CNET-019) | Sanctions potential matches (E20): even tuned, Arabic-origin names alert at 0.3% vs 0.1% (replay) |
| Structured contribution intents with references (E04) | First-payment caps and probation for new destinations (UNB-CNET-015) |
| Self-service status and proactive notices (E15) | Step-up authentication on sensitive changes (E17) |
| Electronic payment enrolment: charities paid faster; fewer check failures (E11, E12) | Over-strict input validation that pushes advisors back to e-mail |

The pattern: when the mechanism **removes a reason for the exception**, both improve; when it **adds a gate in front of the exception**, safety improves and experience worsens, and the gate becomes a contact driver (E15). Holds should therefore carry donor-facing neutral reason codes and a published expected resolution time (charity-network 06, XID-CLM-003).

## 9. Double counting to avoid when prevention and automation are both credited

| # | Saving credited twice | Where | Rule |
|---|---|---|---|
| 1 | Charity vetting labour | EV-E08 MD-5 (3.36 min, ~$11.6 per account) **and** registry stewardship hours ([05](../competitive-displacement/05-charity-registry-economics.md); ~1,532 h at 20k charities) price the same work: for a 10k-account sponsor E08 implies ~560 h | Use the registry model for charity-level work and set E08 human minutes to release-time exceptions only, or vice versa |
| 2 | Change-driven monitoring | EV-E08 prevention (efficacy 0.5) **and** the registry's "180-day full review costs ~3× change-driven" (CLM-005) | One saving; and under DEC-003 the 180-day renewal is retained (automated), so the 3× comparison is against a conventional human review, not a removable cost |
| 3 | Attribution prevention | EV-E04 prevention (−60% at full efficacy) **and** FIE prevention scenario (30-50-60% of investigations at $0.5-3 per fund) | Same mechanism; FIE explicitly warns not to add ingestion cost to staffing models |
| 4 | One input-design change credited across three events | Closed picker and policy rules reduce E07 assisted searches, E09 intake touches and E10 approval exceptions on the same grant line | Acceptable only if each event's base rate excludes the others' effect; Phase II does not test this (unmeasured) |
| 5 | Single ledger | EV-E13 prevention 0.5 on a p_native already rebased once (CHL-056/102), plus MD-3 deterministic reconciliation | External breaks (bank, custodian) are not prevented (CHL-059) |
| 6 | Fraud controls | E17 step-up and E19 callbacks/holds are the same control family | Credit loss reduction once (E19) |
| 7 | AI on prevented work | If prevention is moved to full efficacy for a Phase III scenario while AI saving stays at the Phase II MD-4→MD-5 value | Recompute sequentially: AI saving falls as prevention rises |
| 8 | Transfer reported as saving | MD-6 vendor variable $31; E17 self-service; E11/E12 rail partner; inline certifications | Report vendor, sponsor and system cost; system cost is the test |
| 9 | Sponsor-level registry shared cost | Registry shared layer cost divided by sponsors **and** MD fixed cost that already includes a registry | Confirm whether MD-5/MD-6 fixed cost contains registry engineering before adding [11](11-continuous-charity-intelligence.md) run cost |

## 10. Costs that cannot realistically be eliminated

- **Legal and control floors**: sponsor reserved authority and 4967 review (~25 min per account-year residual in E10), sanctions disposition and reporting, identity proofing ($3 per new account; Revision 2, P3-CHL-REV3027: a charity sponsor is not bound by the bank CIP rule, so this is sponsor policy, not a legal floor; bank and trust distributors impose their own KYC through TPRM, so the cost depends on the channel), contemporaneous acknowledgments (content), dual release, controller sign-off, Nacha fraud monitoring, audit preparation (~7,200 min per sponsor-year until V-9).
- **External and pass-through costs**: securities transfer costs (~$10 per transfer), appraisals (~$350), rails (~$14.9 per account-year), fraud investigation costs, partner fees for virtual accounts and rail services.
- **Coverage gaps of public data**: first-time verification of churches, government units, subordinates and recipients without an EIN (~11% of Schedule I rows raw; ~3-4% first-time a year after reuse).
- **Accountable ownership**: a named owner for eligibility policy and the registry (0.15-0.5 FTE), counsel refresh of reliance and materiality rules.
- **Residual exception tail**: adjacent industries keep 5-15% exceptions after decades of automation (FIE B-005, B-009); 99% STP has no precedent.
- **Platform fixed cost of automation**: connectors, rules, evaluation, SOC 2 evidence; this is where automated minutes go.
- **Mandatory events not yet in the catalogue (Revision 2, P3-CHL-REV3026)**, each needing a named owner and a cost, which are not yet estimated:
  - record retention and legal hold;
  - privacy requests (access, correction, deletion within retention limits);
  - breach response and notification;
  - uncashed checks and state unclaimed-property (escheat) handling (ADM-024). The check fallback is mandatory under CNV-PAY-001, so this event exists from release 1.

## 11. Evidence, gaps and cheap tests

Nothing here is measured: touch rates, minutes and prevention efficacies are Phase II inputs (ASSUMPTION/INFERENCE). The classification shares (E08 split, customer and partner shares) are new assumptions (P3-ASM-HI020..024). The cheapest tests (P3-VAL-HI001..008; P3-VAL-HI007 tests the double counting) reuse the Unbound public-data replay harness (requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md) and synthetic operations; none needs outreach. The decisive unmeasured quantities are unchanged from Phase II and FIE: exception rates and handling minutes per event (P3-GAP-HI001), whether sponsors' existing notification forms make intents net-zero for donors (P3-GAP-HI002), and auditor acceptance of machine renewal (V-9; P3-GAP-HI003).
