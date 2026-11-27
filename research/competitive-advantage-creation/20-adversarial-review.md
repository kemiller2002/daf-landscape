# 20 - Adversarial review

Status: research (2026-11-26). Reconciliation agent (RECON) with agent MOD. Rounds 1 and 2 are complete and reconciled. Register: [adversarial-challenges.csv](data/registers/adversarial-challenges.csv): P3-CHL-REV1001..REV3044 (round 1, 130 rows) and P3-CHL-REV4001..REV4020 (round 2, 20 rows). Disposition overlays: [RECON](data/fragments/RECON/adversarial-challenges-dispositions.csv), [MOD round 1](data/fragments/MOD/adversarial-challenges-dispositions.csv) and [MOD round 2](data/fragments/MOD/adversarial-challenges-dispositions-r2.csv). Full reviews: `data/evidence/adversarial/` (15 round-1 files and `REV4-round2.md`). This review is not independent external assurance.

## Answer in brief

1. **Round 1 changed the answer, not just the wording.** Before review, sequence A3 paid back at month 62, passed the kill rule in the base case, and needed about $1.24M of peak cash. After review and model revision 2:
   - no sequence pays back within 120 months in the base case, in either registry mode;
   - with the kill rule applied, every platform sequence pauses, mostly at month 24, and is worse than doing nothing on the Monte Carlo median (`sequences-ranking.md`).
2. **Round 2 confirmed the decision and corrected the economics.** Model revision 3 (CFO-corrected basis):
   - with the cost center at month 0, every configuration still pauses at month 24, and none beats doing nothing in the Monte Carlo;
   - the only payback is the partner-book sequence (SEQ-PB, P3-SEQ-MOD012), when the sponsor performs the deep review: +$4.18M at month 120, payback at month 76, peak $2.43M. Under M5 it pays back at month 80 (`bases.md`).
3. **The decisive uncertainties are now explicit:**
   - who performs the human deep review under licensing (P3-DEC-MOD005);
   - OD-CDD-02;
   - revenue per customer at a named size.

   Single-sponsor break-even, by who performs the review (`gate-break-even.md`):
   - Echelon performing M1: not reached;
   - risk-tiered attested review, subject to counsel and V-9: 5,202 accounts;
   - the sponsor performing it: 3,079 accounts ($175k net);
   - M5: 3,169 accounts.

   Only 17 plausible sponsors (non-captive, not donation processors) hold 2,646 accounts or more, and A3's reachable cap is 4 (`platform-classes.md`). Revision 2 had given 10,963 accounts ($622k) under M1 and 3,949 ($224k) under M5.
4. **Dispositions across both rounds (150 challenges):**
   - 93 accepted, 39 partly accepted, 17 deferred and 1 rejected;
   - round 1: 75 / 37 / 17 / 1 after the round-2 audit, which re-opened P3-CHL-REV1034 and relabelled P3-CHL-REV2029;
   - round 2: 18 accepted, 2 partly accepted;
   - no high-severity challenge was rejected;
   - the deferrals are effects the model does not yet represent: founder and delivery capacity, escalation, renewal leakage, OEM royalties and some cost lines.
5. **Sixteen round-1 challenges were plain factual, legal or text errors, and all were corrected.** Among them:
   - a misread Candid product: the "Nonprofit Eligibility API" is an Apple Pay enablement product;
   - a misattributed statute: 4966(d)(4) only defines a disqualified supporting organization;
   - an omitted statute: the 170(f)(18) acknowledgment;
   - a missing IRS revenue procedure on group exemptions: Rev. Proc. 2026-8;
   - a missing interagency proposal on bank third-party risk management: 91 FR 58536;
   - the Nacha TPSP audit treated as a contingency, although ratified CNV-PAY-001 makes it a base obligation.

## 1. Method

- **Panels.** Fifteen adversarial perspectives in three panels of five, each reviewing the full package (reports 01-19, registers, model outputs):
  - **Panel REV1**, market and buyer: an incumbent competitor executive, a skeptical institutional buyer, a bank procurement executive, a DAF sponsor executive, and a customer unwilling to switch.
  - **Panel REV2**, economics and strategy: a CFO, a venture investor, a bootstrapped business founder, an economist skeptical of AI productivity, and a product strategist.
  - **Panel REV3**, operations, compliance and data: a financial systems architect, a nonprofit data specialist, a compliance specialist, a channel partner, and a professional services operator.
- **Rules.** Each reviewer cited the report line, register row or model file it challenged, gave evidence (repository paths, public URLs with access dates, or reproducible re-runs of the model), assigned a severity, and proposed a change. Reviewers did not edit artefacts.
- **Reconciliation.** Challenges were triaged into three classes:
  - model-related (63): agent MOD revised the model and reports 14-16, 18 and 19;
  - factual, legal or text errors (16): RECON corrected reports 02-13, 17 and 21 and the agent fragments;
  - judgment challenges (51): RECON decided each one.

  Every changed figure keeps its old value in a "Revision 2" note; no history was deleted. Disagreements are recorded rather than forced into consensus. RECON verified the new legal and regulatory facts against primary sources (26 USC 4966 and 170; Rev. Proc. 2026-8; the 91 FR 58536 notice; Candid's API page) before adding them.
- **Independence.** The authors, the model and all fifteen reviewers come from the same model family. EDF's calibration guidance treats several lenses from one source as non-independent ([17](17-clarity-and-edf-assessment.md)). This is structured self-challenge, **not independent external assurance** (P3-GAP-CE003). The reviewers' re-runs are reproducible, and several were confirmed by MOD's own fixes, each of which has a unit test ([18](18-economic-model-methodology.md) §8).

## 2. Counts by perspective, severity and disposition (round 1)

These counts are after the round-2 disposition audit.

| Panel | Perspective | Challenges | High | Medium | Low | Accepted | Partly accepted | Deferred | Rejected |
|---|---|---|---|---|---|---|---|---|---|
| REV1 | Bank procurement executive | 9 | 2 | 5 | 2 | 5 | 4 | 0 | 0 |
| REV1 | Customer unwilling to switch | 7 | 3 | 3 | 1 | 3 | 3 | 1 | 0 |
| REV1 | DAF sponsor executive | 8 | 3 | 4 | 1 | 5 | 2 | 0 | 1 |
| REV1 | Incumbent competitor executive | 8 | 3 | 4 | 1 | 6 | 2 | 0 | 0 |
| REV1 | Skeptical institutional buyer | 8 | 3 | 4 | 1 | 5 | 3 | 0 | 0 |
| REV2 | Bootstrapped business founder | 9 | 3 | 4 | 2 | 3 | 2 | 4 | 0 |
| REV2 | CFO | 10 | 3 | 6 | 1 | 10 | 0 | 0 | 0 |
| REV2 | Economist skeptical of AI productivity | 9 | 2 | 5 | 2 | 5 | 2 | 2 | 0 |
| REV2 | Product strategist | 9 | 3 | 5 | 1 | 5 | 3 | 1 | 0 |
| REV2 | Venture investor | 9 | 3 | 5 | 1 | 6 | 2 | 1 | 0 |
| REV3 | channel partner | 9 | 4 | 4 | 1 | 3 | 4 | 2 | 0 |
| REV3 | compliance specialist | 9 | 4 | 3 | 2 | 8 | 1 | 0 | 0 |
| REV3 | financial systems architect | 9 | 4 | 5 | 0 | 2 | 3 | 4 | 0 |
| REV3 | nonprofit data specialist | 9 | 2 | 5 | 2 | 5 | 4 | 0 | 0 |
| REV3 | professional services operator | 8 | 4 | 4 | 0 | 4 | 2 | 2 | 0 |
| **All** | | **130** | **46** | **66** | **18** | **75** | **37** | **17** | **1** |

| Severity | Accepted | Partly accepted | Deferred | Rejected | Total |
|---|---|---|---|---|---|
| high | 28 | 13 | 5 | 0 | 46 |
| medium | 32 | 23 | 10 | 1 | 66 |
| low | 15 | 1 | 2 | 0 | 18 |

By class:

| Class | Challenges | Accepted | Partly accepted | Deferred | Rejected |
|---|---|---|---|---|---|
| Model-related (MOD revised the model) | 63 | 38 | 11 | 14 | 0 |
| Factual, legal or text error | 16 | 16 | 0 | 0 | 0 |
| Judgment | 51 | 21 | 26 | 3 | 1 |

The CFO panel member's ten round-1 challenges were all accepted; P3-CHL-REV2029, from the AI-productivity economist, was relabelled partly accepted in round 2. Each was a reproducible model error or omission, among them a fractional pilot go-live (P3-CHL-REV2001), a tie at the named-partner threshold (P3-CHL-REV2002), inconsistent contingency (P3-CHL-REV2003), no wind-down (P3-CHL-REV2004) and no tax (P3-CHL-REV2005). The financial systems architect has the most deferrals (4 of 9). Its cost lines for event-store lifecycle, per-tenant releases, hardening scope and reconciliation per external feed are not yet in the model.

## 3. The most material challenges and what changed

| Challenge | Finding | What changed |
|---|---|---|
| P3-CHL-REV2001, REV2044 | The kill rule's "referenceable live pilot" was met by a fraction of a customer, or by a non-Unbound stream | The pilot now requires one whole live Unbound customer. A, A3, E, G and H pause at month 24 in the base case, and A3 passes only in the favourable case (P3-CLM-MOD006 revised) |
| P3-CHL-REV2011, REV2012, REV1001, REV3030 | A3's $300k net per customer implies sponsors of ~5,300 accounts, and few exist outside contracted incumbents | Revenue per customer is now tied to sponsor size, and customers are capped by the FY2024 panel times a reachable share. A3 and H are reconciled as one route at different sizes. Break-even sizes are reported, and A and A3 are labelled displacement sequences |
| P3-CHL-REV3010, REV3020 | The registry headline ($124k, M5) relied on automated renewal that UNB-CDD-CIV-008 does not adopt until OD-CDD-02 | M1 ($768k at 20k charities) is the governing mode and M5 is conditional; in revision 3, who bears M1 is a separate allocation (P3-DEC-MOD005) (P3-ASM-MOD049; P3-DEC-MOD004); [11](11-continuous-charity-intelligence.md) and [10](10-structural-cost-elimination.md) restated |
| P3-CHL-REV3019, REV1026 | Nacha TPSP audit and fraud monitoring were treated as a contingency | Base obligation under ratified CNV-PAY-001 (P3-ASM-MOD040); [02](02-existing-unbound-economics.md), [03](03-capital-requirements-reconstruction.md), [10](10-structural-cost-elimination.md), [11](11-continuous-charity-intelligence.md) and [21](21-commercial-thesis-invalidation.md) corrected |
| P3-CHL-REV3004, REV3022 | A one-founder operator cannot evidence two-approver change control or two-person break-glass | Control operations of $150-350k a year are now in the base run (P3-ASM-MOD041); 02 states that the lean run as published was not SOC-compliant |
| P3-CHL-REV3037, REV3038, REV3039 | First conversion assumed Transitus phase 1, which covers no incumbent source packages; go-live lag too short | First conversion is now $75-325k, the first three customers per incumbent cluster pay that rate, and the go-live lag is 6-12 months (P3-ASM-MOD042, P3-ASM-MOD043) |
| P3-CHL-REV1046, REV2038, REV3001 | A3 excluded the S2-to-S3 build from the kill-rule clock | New sequences A3B and A3X carry the build inside or outside the cost center. A3X shows that moving the build off the clock is not a saving. 02 adds testable S3 exit criteria |
| P3-CHL-REV2043, REV2018, REV2020 | The ranking had no do-nothing baseline, and the "no outside investment" claim was circular | The ranking is now against do-nothing on kill-rule Monte Carlo medians. P3-CLM-MOD012 is replaced: outside capital would finance a loss, not a path to self-sufficiency |
| P3-CHL-REV1008, REV1012, REV1033, REV2039 | The host-sponsor route (P3-DEC-CD001) was recommended though the model shows it never pays back | P3-DEC-CD001 is revised to an adoption and reference route with an owner-set loss budget, consistent with P3-DEC-CE002 |
| P3-CHL-REV1004, REV3005, REV3009 | Three inconsistent walk-away thresholds; the lean floor was founder subsidy | One walk-away table: $58.51 on MD-6, $27.86 on the revision-3 lean base, $30.35 with the founder at market (revision 2: $31.30 and $33.78) (`response-walk-away.md`). P3-DEC-EK001 restated |
| P3-CHL-REV3013, REV3023, REV3024, REV3012, REV1025 | Source and legal errors and omissions | Corrected and sourced: P3-SRC-HI013, P3-SRC-CD021, P3-GAP-HI011, P3-GAP-CD012 |

The effect on the owner's questions, on model revision 3 (CFO-corrected): from S3, cash to the first invoice is **$384k / $1.83M / $6.63M**, with Echelon performing M1 on demand, and $1.64M base under M5. A3's uninterrupted peak cash is **$547k / $8.26M / $31.49M**, with no base payback. Under the kill rule the base case pauses at month 24 with **$1.38M** at risk for A3 and **$1.33M** for A from today (`key-figures.md`, `sequences-kill-rule.md`). Revision 2 gave $542k / $2.12M / $7.12M, $1.81M (M5), $744k / $8.70M / $46.22M, and $1.81M / $1.46M at risk.

## 4. Recorded disagreements

Rejections and partial rejections, with reasons. Each is kept in the register so a later round or the owner can overturn it.

| Challenge | Proposed by | Decision | Reason |
|---|---|---|---|
| P3-CHL-REV1034 | DAF sponsor executive: label M1 (periodic human review) hypothetical, because sponsors do not perform it | **Rejected in round 1; partly accepted after the round-2 audit (P3-CHL-REV4013)** | The requirement stands: M1 is what the ratified CNV-GRT-003 wording requires until OD-CDD-02 (UNB-CDD-CIV-008). Labelling it hypothetical is still rejected. The substance, whether the review is a vendor cost, is accepted. Under licensing, a review the sponsor performs is sponsor labour, and the owner decides the allocation (P3-DEC-MOD005) |
| P3-CHL-REV1037 | DAF sponsor executive: remove EK010 (reproducible migration) from the strongest-candidate list | **Rejected** | [07](07-architectural-competitive-advantages.md) §5 lists candidates, not strengths, and already says that nothing is built and Transitus has no code. DEC-007 and DEC-011 depend on this hypothesis; removing it would hide what must be tested |
| P3-CHL-REV3018 | Nonprofit data specialist: restrict the shared layer to IRS, OFAC and CSL until counsel confirms other licences | **Partly rejected** | SAM exclusion facts and FAC data are now held pending counsel. The UK (OGL v3), UN and EU lists carry explicit open terms, so they stay shareable |
| P3-CHL-REV2024, REV2040 | Bootstrapped founder; product strategist: gate any further DAF-specific build on a named partner, a price expression and a large candidate sponsor | **Deferred to the owner** | This interacts with the owner's cost-center clock (OD-P3-03, OD-P3-04). It is now proposed as P3-DEC-MOD003, restated in revision 3 so that the size threshold follows P3-DEC-MOD005 ([25](25-executive-decision-register.md)); RECON does not decide it |
| P3-CHL-REV2037 | AI-productivity economist: have a human practitioner check key inputs | **Deferred** | Needs owner-approved contact; no outreach is authorized ([23](23-commercial-validation-roadmap.md)) |

**Deferred model limits.** These challenges were accepted in substance but are not yet modelled; [14](14-commercial-sequencing.md) §8 states the limits:
- founder capacity and hiring triggers (P3-CHL-REV1005 partly, REV2017 partly, REV2021);
- wage and price escalation (REV2033);
- delivery capacity and hypercare (REV3041, REV3042);
- renewal leakage (REV1042);
- incumbent price paths (REV2015);
- OEM royalties (REV3029);
- side-bet diversion (REV2026);
- a per-customer service line (REV2027);
- hardening scope (REV3003);
- event-store lifecycle (REV3006);
- per-tenant releases (REV3007);
- reconciliation per external feed (REV3008);
- partner first-line and availability SLA (REV3033).

Every one of these would worsen the economics. None could restore a base-case payback.

## 5. What the review did not test

- **Buyers and partners.** No buyer, partner, auditor or counsel was consulted. Every buyer-side premise is still untested ([22](22-evidence-gaps.md)).
- **Factual corrections still unverified:**
  - the Nacha 31 December audit deadline rests on secondary sources; Nacha's own page confirms only that the audit is annual;
  - the YourCause price is rounded to ~$157M, because the $157.7M filing figure was not re-read;
  - the status of the programmes BNY Mellon CGF hosted is unchecked (P3-GAP-CD005).

## 6. Round 2

### 6.1 Method

- **Panel REV4.** One reviewer, the panel, wrote five perspectives (CFO, bootstrapped founder, incumbent competitor executive, product strategist, and a disposition audit) and reviewed model revision 2 and the round-1 dispositions. It read reports 14, 16, 18, 19, 20 and 25 in full, and the relevant parts of 02, 07, 08 and 11, together with the model source, the inputs, all 130 round-1 dispositions and the cited Unbound requirement texts (`REV4-round2.md`).
- **Question.** Has revision 2 over-corrected into pessimism, and do the round-1 dispositions hold?
- **Same limits as round 1.** The reviewer is from the same model family. This is not independent external assurance.
- **Reconciliation.** MOD built model revision 3, which keeps the "revision 2 conservative" basis beside a "revision 3 CFO-corrected" basis (`bases.md`) and records its change notes in the round-2 overlay. RECON dispositioned all 20 challenges and corrected the round-1 dispositions the audit found wanting.

### 6.2 Verdict

The reviewer found that **revision 2 got the decision right but the economics wrong**. The base case stacked three adverse choices:
- Echelon paying for a twice-yearly human deep review of every charity out of an $81 licence;
- contingency on ten years of steady-state cost;
- control operations overlapping the maintenance approvers.

At the same time, revision 2 under-corrected demand: its population cap counted captive national sponsors and donation processors. Revision 3 corrects both. **The decision is unchanged:** gate and validate before any DAF cost center opens (P3-DEC-MOD003).

### 6.3 Counts

| Panel | Perspective | Challenges | High | Medium | Low | Accepted | Partly accepted | Deferred | Rejected |
|---|---|---|---|---|---|---|---|---|---|
| REV4 | CFO | 8 | 4 | 4 | 0 | 7 | 1 | 0 | 0 |
| REV4 | bootstrapped founder | 2 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| REV4 | disposition audit | 5 | 0 | 4 | 1 | 5 | 0 | 0 | 0 |
| REV4 | incumbent competitor executive | 2 | 1 | 1 | 0 | 2 | 0 | 0 | 0 |
| REV4 | product strategist | 3 | 2 | 1 | 0 | 2 | 1 | 0 | 0 |
| **All** | | **20** | **8** | **11** | **1** | **18** | **2** | **0** | **0** |

| Severity | Accepted | Partly accepted | Deferred | Rejected | Total |
|---|---|---|---|---|---|
| high | 8 | 0 | 0 | 0 | 8 |
| medium | 9 | 2 | 0 | 0 | 11 |
| low | 1 | 0 | 0 | 0 | 1 |

### 6.4 What changed in revision 3

| Challenge | Change |
|---|---|
| P3-CHL-REV4001, REV4012, REV4013, REV4018 | Review-performer allocation modelled; new owner decision P3-DEC-MOD005 (who performs and pays for the deep review). Vendor-borne M1 is structurally loss-making (P3-CLM-MOD017) |
| P3-CHL-REV4002 | Contingency limited to one-time, pre-revenue and the first 12 live months (revision 3 basis) |
| P3-CHL-REV4003, REV4004 | Demand-driven deep reviews (P3-ASM-MOD050); M1 risk-tiered attested configuration (P3-ASM-MOD055), subject to counsel and V-9 |
| P3-CHL-REV4005 | Control operations netted against the maintenance approvers; adverse TPSP overlap removed. The Nacha base is still unquoted (P3-GAP-RECON005) |
| P3-CHL-REV4006, REV4017, REV4007 | Sponsors classified by platform; cap on plausible sponsors only (17 at 2,646 accounts or more; A3 cap 4); cap on live customers plus pipeline. The panel is held static (stated limit) |
| P3-CHL-REV4008, REV4020 | Partner-book sequence SEQ-PB (P3-SEQ-MOD012); variants for sponsor-performed review, M5 after V-3/V-9, and large non-captive sponsors |
| P3-CHL-REV4009, REV4010 | Whole first signing. Kill timing reported by go-live lag and cost-center month (`kill-timing.md`): with the clock at month 0, A3 passes only if the go-live lag is 8 months or less; with the clock at month 6 or 12 and a whole first signing it passes. Wind-down at the pre-revenue run when nothing is live |
| P3-CHL-REV4011 | P3-DEC-MOD003 restated: the size threshold is set after P3-DEC-MOD005, in single-sponsor and partner-book accounts (`gate-break-even.md`) |
| P3-CHL-REV4014 | Deep review charged per sponsor-charity (no union sharing); marginal sponsor recomputed |
| P3-CHL-REV4016 | SEQ-H failure band set to high, consistent with P3-SEQ-FGJ004 |
| P3-CHL-REV4019 | Revision 3 CFO-corrected basis published beside revision 2 |

RECON restated reports 02, 04, 06, 11, 13, 17, 21 and 22-25 to revision 3, keeping earlier values in revision notes. It added P3-GAP-RECON001..005, P3-XRI-RECON005 and the critical-path marking in [25](25-executive-decision-register.md).

### 6.5 Disposition audit: results and corrections

The audit (P3-CHL-REV4013..REV4017) tested the round-1 dispositions against what was actually changed:

| Round-1 challenge | Audit finding | Correction |
|---|---|---|
| P3-CHL-REV1034 | The rejection defended the requirement but did not answer whether the review is a vendor cost | Changed from rejected to **partly accepted**; the allocation is modelled; P3-DEC-MOD005 |
| P3-CHL-REV2029 | Labelled accepted, but the platform residual was not carried into the base | Relabelled **partly accepted** |
| P3-CHL-REV3011 | The marginal-sponsor recompute "referred to MOD" was not done | Now done: review per sponsor-charity, no union sharing; rationale updated |
| P3-CHL-REV1001, REV2012 | The non-captive population check appeared only in a report table, not in the model cap | Cap now on plausible sponsors; rationales updated |
| P3-CHL-REV3028 | FGJ004 band raised, but the model's SEQ-H still said moderate | Model regenerated with high; rationale updated |
| P3-CHL-REV3010, REV3020 | (coordinator check) The allocation question was not modelled | Rationales updated to the revision-3 allocation and P3-DEC-MOD005 |

### 6.6 Remaining disagreements

- **P3-CHL-REV1037 (rejected)** stands. EK010 stays a candidate to test, not a strength.
- **P3-CHL-REV3018 (partly rejected)** stands. The UK, UN and EU lists stay shareable.
- **P3-CHL-REV1034** remains rejected in one respect: M1 is the ratified requirement, not a hypothetical.
- **The REV4 CFO's point estimates differ from revision 3.** The reviewer's CFO-corrected A3 under M2 paid back at month 83. Revision 3's A3 does not pay back in any single-sponsor configuration, because the plausible-sponsor cap (4 reachable) that the same review asked for (P3-CHL-REV4006) now binds. RECON reads this as the two round-2 corrections interacting, not as a disagreement to resolve. Both are reported (`bases.md`, `cap-sensitivity.md`).
- **Deferred model limits** from round 1 remain (section 4). Two round-2 limits are added: no panel growth (P3-CHL-REV4007) and no quote for the Nacha base (P3-CHL-REV4005).
