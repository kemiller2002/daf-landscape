# 22 - Adversarial review

Status: research draft (2026-11-26). Not legal advice. Agent review is not independent assurance. Evidence classes per 01-research-methodology.md.

## Summary

- Three reviewers each worked independently and were asked to refute the drafts, not improve them:
  - ADVA: the charity network, drafts 02-09.
  - ADVB: onboarding and migration, drafts 10-19 and the onboarding parts of 20.
  - ADVX: economics and strategy across the package.
- They raised 56 challenges:
  - by severity: 3 critical, 32 major and 21 minor;
  - by verdict: 23 upheld, 27 partially upheld and 6 rejected.
  - Records are in `data/adversarial-findings-A.csv`, `-B.csv` and `-X.csv`.
  - Sources are in `data/sources-ADVA.csv`, `-ADVB.csv` and `-ADVX.csv`.
- **The factual base held up.** The reviewers spot-checked 40 claims or groups of claims against primary sources. 39 reproduced; one PDF could not be parsed and was marked unverified.
  - The IRS bulk-file counts re-ran from the scripts.
  - Rev. Proc. 2018-32 was checked verbatim.
  - Also confirmed: the Nacha 2026 rule text, Chariot's account terms, the FCA's TSB notice, the ACATS and CASS figures, the Form 990 payments and the RCF audit notes.
  - The weaknesses were in interpretation and design, not in the cited evidence.
- **The most important challenge goes to the premise of the mission.**
  - ADVX-10 (critical) argues that the binding competitive barrier is distribution and incentive alignment, not the charity network or onboarding friction.
  - Examples of that barrier: white-label sponsor entities, adviser and investment-manager economics, and fee carve-outs.
  - No public evidence shows a sponsor choosing or leaving a vendor because of its charity network or onboarding.
  - We accept the challenge as an unrefuted hypothesis. It reshapes the recommendations in 23 and becomes requirement UNB-ONB-033 (a register of remaining barriers). We do not treat it as proven: no win/loss evidence exists either way.
- **Ratified clauses already covered more than the drafts assumed.**
  - The round-2 amendments to CNV-PAY-002 and CNV-PLT-011 (c10, c11) already require callback contacts aged 30 days or more, CAL3 for charity submitters, holds on changes to charity contacts and signatories, and partner-contract equivalence for CNV-EXP-002.
  - The drafts were revised to refine those amendments rather than duplicate them (ADVA-02).
- **Four true conflicts remain and are escalated to the owner**, not resolved here:
  - migration in Release 1: ADVB-01 → OD-CNO-01;
  - a third destination-evidence class for partner-bank accounts: ADVA-03 → OD-CNO-02;
  - the scope of CNV-EXP-002's "full history": ADVB-04 and MIG → OD-CNO-07;
  - the rollback boundary: OD-CNO-08.
- **The economics changed the most.** On the C0 no-lever base with Track A run costs restored:
  - the registry costs about $316k a year to run;
  - modelled savings from moving grants to electronic payment are about zero on reconciled assumptions;
  - including onboarding in the servicing fee pays back only for added sponsors, not for the first one (ADVX-01, -03, -04, -13, -14; ADVA-07).
- **We did not manufacture agreement.**
  - Authors refuted parts of several challenges with evidence: ADVB-02, ADVA-01 and ADVA-08.
  - The reviewers rejected 6 of their own challenges after testing them.
  - Disagreements that remain are recorded below.

## Disposition of every material challenge

Disposition means what the package did. "Revised" points to the target file's own *Adversarial review response* section, which records the author's verdict and the change.

| ID | Sev. | Reviewer verdict | Disposition |
|---|---|---|---|
| ADVX-10 | critical | upheld | Accepted as a hypothesis. 02 re-ranks Ren's barriers (platform integration and distribution first). 23 makes distribution and incentive design the lead strategic question. New requirement UNB-ONB-033. Still unproven: no win/loss data |
| ADVB-01 | critical | upheld | Escalated: OD-CNO-01. 10 and 17 restate it as a conflict with options (a)-(c). Coordinator recommends (a) |
| ADVB-02 | critical | upheld | Partly refuted. The sponsor usually owns its data and can pull reports repeatedly. Accepted: Extraction Plan, single-extract cutover (S11), legacy vault and cadence variants (13, 15, 17). UNB-ONB-002 and UNB-ONB-009 |
| ADVA-01 | major | upheld | Partly refuted. The Chariot-first order is ratified in CNV-PAY-007 via OD-P-PAY cut B (c8). The attribution in 07 is fixed and the debit-block approval added |
| ADVA-02 | major | upheld | Accepted. 09 reframes the gap as already ratified (c10, c11) and narrows PROP-SEC-02 to the residual risk of a public-source contact that has just changed |
| ADVA-03 | major | partial | Escalated: OD-CNO-02. Covered by UNB-CNET-014 |
| ADVA-07, ADVX-13, ADVX-14 | major/minor | upheld | Accepted. 20 now adopts 08's assumptions: about 8% partner coverage, p=0.10, and 37% checks at 36 months. Network e-payment savings fall to about $0 in the base case |
| ADVA-09 | major | partial | Accepted. In 02, Ren's sponsor-side platform integration is now the primary barrier and the payee layer is a secondary switching cost |
| ADVA-12 | major | partial | Accepted. Partner contract minimums (UNB-CNET-018) and a second rail before scale (UNB-CNET-026). Chariot stays first |
| ADVA-13 | major | partial | Accepted. Cross-sponsor sharing of destination evidence is deferred beyond Release 1 (05, 07, 08, 09). The counsel question on imputed awareness goes to OD-CNO-05 |
| ADVA-15, ADVX-11 | major/minor | partial | Accepted. 03 and 08 relabel parity features. Remaining hypotheses about differentiation are listed in 23 |
| ADVA-20 | major | partial | Accepted. 05, 06 and 08 split proposals into Release 1 and later. The Unbound package keeps 26 UNB-CNET records with release scopes |
| ADVB-03 | major | partial | Accepted. "Switching Guarantee" becomes "Migration Service Commitment", limited to Unbound-controlled steps (11). UNB-ONB-030 |
| ADVB-04 | major | partial | Accepted. Migration classes PlatformReplacement, ProgramTransfer and Greenfield (13, 10). UNB-ONB-001. OD-CNO-07 |
| ADVB-05, -06, -07, -13; ADVX-01, -16 | major | upheld/partial | Accepted. 20 adds buyer switching TCO, sponsor effort, rehearsals, legal, the failure reserve, CAC, history-depth scenarios and Track A run costs |
| ADVB-08 | major | partial | Accepted. Recognition-convention continuity and the cutoff register (14). UNB-ONB-014 |
| ADVB-09 | major | partial | Accepted. Semantic invariants, mutation tests and attribute sampling (gates G28-G29). UNB-ONB-005 |
| ADVB-10 | major | partial | Accepted. Auditor evidence plan with SOC 1 Type I at go-live (16, 17). UNB-ONB-015 |
| ADVB-11 | major | upheld | Accepted. Termination fee withdrawn; early-exit recovery limited to the straight-line unamortised balance (20). UNB-ONB-004 and UNB-ONB-029 |
| ADVB-12 | major | partial | Accepted. Differentiation rests on outcome metrics no vendor publishes (10). UNB-ONB-030 |
| ADVB-14 | major | upheld | Accepted. T1 runs on standard reports the sponsor can download; a paid export comes only after a letter of intent (13). UNB-ONB-003 |
| ADVX-03 | major | upheld | Accepted. First-sponsor and added-sponsor views (20). UNB-ONB-032; OD-CNO-10 |
| ADVX-04 | major | upheld | Partly accepted. 20 is rebased on C0 with P10-P90 ranges. Conformance with CNV-ECO-003 is **still partial**: no adverse licence scale, no correlated draws, no measured levers. Recorded as an evidence gap (24) |
| ADVX-05, -06, -07 | major | partial/upheld | Accepted. Price benchmarks show 20 bps is a price increase against an 18.5 bps incumbent and no size pays back at $81 per account. 23 treats price positioning as unresolved |
| ADVX-08 | major | partial | Accepted. Registry scope staged to the recipients actually paid (05). Reflected in UNB-CNET release scopes |
| ADVX-12 | major | upheld | Accepted. Remaining barriers are listed in 23 §10. UNB-ONB-033 |
| ADVX-15 | major | upheld | Accepted. The network is reframed as a cost of doing business and a switching-cost defence, not a margin lever (20, 23) |
| Minor findings | minor | various | Corrected where upheld: ADVA-04, -05, -06, -10, -11, -18, -19 and ADVB-15, -16, -17. The corrected counts are in 04, 05 and 06 (e.g. 237,380 subordinates; about 31,600 revoked-but-listed EINs, of which about 71% re-recognised) |
| Rejected after test | - | rejected | ADVA-16, -17; ADVB-18, -19; ADVX-09, -17: the reviewers found the drafts correct on these points |

## Disagreements that remain

- **Ren's moat.**
  - ADVX holds that distribution and incentives dominate.
  - REN accepts this for programmes on Ren's own sponsor entity (RCF white label), but holds that for self-administered sponsors (AEF, MS GIFT) migration cost is the barrier, and charities' re-enrolment adds to it.
  - Both positions fit the evidence. What would separate them is win/loss and switching-reason data, which is not public.
- **Whether a standard epoch is workable** for most sponsors given the recognition-point issue. MIG says yes; ADVB was sceptical. The answer depends on auditor acceptance (UNB-ONB-014, UNB-ONB-015).
- **The cost of the evidence pack.** MIG: the pack lowers the auditor's substantive work. ADVB: it cannot replace a Type II report. Both are recorded; neither is quantified.
- **Whether Unbound should build a registry at all.**
  - ADVA and ADVX: buying Candid is cheaper at small scale.
  - The package keeps UNB-CHAR-DEC-001 because Candid rests on the same IRS files and Rev. Proc. 2018-32 §8.01 lets Unbound issue its own reliance report.
  - The trade-off is cost: about $316k a year in run cost against a licence from about $2,750 a year plus integration (05, build/buy table).
  - Recorded as a reconsideration trigger in 23.

---

The three reviewer sections follow verbatim. Where they cite a draft, they cite it as it was **before** revision.

## Adversarial review: Track A (charity network) - agent ADVA

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Scope: drafts 02-09 and their data and scripts. The aim was to refute the drafts, not improve them. Each finding was checked against primary sources, the ratified CNV clauses and the session's IRS bulk files. Findings are in `data/adversarial-findings-A.csv` (ADVA-01..20); sources are in `data/sources-ADVA.csv` (ADVA-001..018). Re-derivation scripts: `scripts/adva_verify.py`, `scripts/adva_stale.py`. The draft scripts were also re-run unmodified.

### Summary

- **The factual core of Track A holds up.** Of the cited facts sampled, 18 groups reproduce:
  - IRS counts (BMF, Pub 78, revocation, 990-N);
  - Rev. Proc. 2018-32 sections 4.02, 4.04, 4.06, 6.01-6.03 and 8.01, checked verbatim;
  - Nacha Phase 2 dates and the False Pretenses definition;
  - Chariot's deposit-account and "no bring-your-own-account" terms;
  - IC3 2025 figures, Fidelity's 227,000 figure, CAF America's 1-3 year validation and Candid's 20-minute polling.
- **Two drafts misread ratified clauses (both major, upheld).**
  - 07 attributes "Chariot first, PayPal second" to CNV-PAY-007. That clause is about bank feeds and debit blocks (ADVA-01).
  - 09's headline "gap" (charity contact-change holds and the age of callback contacts) is already ratified. It sits in the round-2 amendments to CNV-PLT-011 (c11) and CNV-PAY-002 (c10) (ADVA-02).
- **The CNV-EXP-002 conflict is sharper than the drafts state (major).** The c10 amendment allows exactly two destination-evidence combinations, with a cooling-off floor of 1 business day. Chariot's model (officer identity check plus a bank-opened DDA in the charity's name) fits neither (ADVA-03).
- **The economic model and the growth model disagree (major, upheld).** 20 assumes 50% partner pre-enrolment and a 10% check share, anchored on Fidelity's proprietary EFT. 08's model gives 8-21% of grants at go-live and plans on a slow p=0.10 path (ADVA-07).
- **Ren is more defensible in Unbound's entry segment than 02 implies (major).** The stickiness is sponsor-side, across the whole platform. Only 1 of 26 national, faith or affinity iPhi sponsors left in 2023-2026, and no exit went to a new entrant (ADVA-09).
- **Shared destination (bank) evidence has a small, unsized benefit and a real correlated downside (major).** Defer it beyond Release 1 (ADVA-13).
- **Most of the proposed "differentiators" are parity features** (ADVA-15). Track A's requirement surface also needs a Release 1 / later split (ADVA-20).

### Material challenges

| ID | Challenge | Evidence (class) | Verdict |
|---|---|---|---|
| ADVA-01 | 07 cites CNV-PAY-007 for partner order | c1 clause text: CNV-PAY-007 = "Bank activity feeds, debit blocks and fee bearers". The order comes from SPD-CMP-003, an open decision (VERIFIED-FACT) | Upheld, major |
| ADVA-02 | 09: CNV-PLT-011 covers "donors only"; PROP-SEC-02 proposed | c11: "for charities, contact and authorised-signatory changes"; c10: callback contact must be verified ≥30 days earlier, "any contact or signatory change inside that period disqualifies the contact", CAL3 (VERIFIED-FACT) | Upheld, major |
| ADVA-03 | CNV-EXP-002 versus destination evidence | c10 says the combinations "SHALL be exactly" (a) or (b). Chariot "focuses on validating officer identities" [ADVA-004]; its DDA is "legally owned by your organization" [ADVA-003] (VERIFIED-FACT) | Partially upheld, major. Owner decision needed on a third evidence class |
| ADVA-07 | 08 versus 20 on partner coverage | ECO `partner_coverage` 0.3/0.5/0.7 anchored on Fidelity's 67%. Fidelity's enrolment is proprietary, with a queue that "may take several weeks" [ADVA-008]. PAY model tiers 2-45% (INFERENCE) | Upheld, major |
| ADVA-09 | Ren's moat is mislocated | Repo attrition census: 5 of 6 exits were community foundations; NPT, JPM and ICGF moved deeper into Ren; exits went to Foundant or akoya. No charity-side network-effect evidence is public (INFERENCE) | Partially upheld, major |
| ADVA-12 | Dependency on Chariot | Partners include Daffy, Endaoment and TIFIN Give [ADVA-005, ADVA-006]. VC-backed [ADVA-007]. FDIC cover is $250k per depositor at one bank, Column [ADVA-003]. Mitigant: the charity-owned DDA can receive any ACH (INFERENCE) | Partially upheld, major. Keep Chariot first, add contract protections |
| ADVA-13 | Shared verification and systemic risk | Verification costs $1.35-4 per enrolment (ECO). A bank-originated owner match costs the charity no effort. Loss allocation is undefined. The tripwire sends a signal across tenants. Rev. Proc. sections 4.04(3) and 5.02(2) "aware of" could impute knowledge to sharing sponsors (INFERENCE) | Partially upheld, major |
| ADVA-14 | Registry versus buying Candid | Registry costs ~$319k setup plus $75k a year (ECO), against Candid from $2,750 a year (vendor). Candid uses the same IRS files [ADVA-009] and still cites superseded Rev. Proc. 2011-33. Section 8.01 lets Unbound issue its own reliance report [ADVA-001]. Some sponsor policies name GuideStar [ADVA-017, ADVA-018] | Partially upheld, minor. DEC-001 survives; add a build/buy table |
| ADVA-15 | Parity, not advantage | Chariot "claim ... one time ... from all Chariot Disbursement partners" [ADVA-005]; Ren "validated once"; Fidelity ACH needs no portal; CAF America 1-3 years; Candid <24h | Partially upheld, major |
| ADVA-20 | Focus | 05 has 11 new requirements, 09 has PROP-SEC-01..15, plus the state model and the growth loop. 20: the network is a "sales/switching asset not margin lever" (HYPOTHESIS) | Partially upheld, major |
| ADVA-04 | 05 identity counts | Re-running `reg_source_change_volumes.py bmf-profile` on eo1-eo4 gives 237,380 / 235,926 / 317,386. Adding the eo_pr and eo_xx files reproduces 05's 237,858 / 244,845 / 326,159 exactly, because 5,060 rows are duplicates (VERIFIED-FACT) | Upheld, minor |

Minor findings are in the CSV:
- ADVA-05: three different figures for revoked organizations still in Pub 78 (19,699 / 19,695 / 19,689).
- ADVA-06: 71% of the 31,616 have a BMF ruling date after their revocation, which points to re-recognition (s4.06).
- ADVA-08: the p≤0.10 calibration ignores evidence from Chariot and TIFIN on forced-claim designs.
- ADVA-10: "not proprietary" is an inference labelled VERIFIED-FACT.
- ADVA-11: the 7% "outside BMF" figure compares TY2024 recipients with a 2026 snapshot.
- ADVA-18: the Vanguard figure of 66,785 is not in its cited sources; press reports "nearly 67,000".
- ADVA-19: self-reported counts are classed VERIFIED-FACT, and Fidelity's discretionary callback is not mentioned.

### What survived

- **Public data is sufficient for legal status reliance and insufficient for everything else.** It does not cover subordinates (s6.03), existence, government EINs or bank ownership. 04, 05 and 06 state this correctly, and the counts reproduce: Pub 78 lists 0 of 237,380 c3 subordinates; the posting lag p50 is 88 days in 2026 and 89 in 2025; there are 122,787 retroactive reinstatements. One nuance for 04: the 88-day median is an artefact of the August batch. 39,415 of the 53,120 postings in 2026 fall at exactly 88 days (ADVA-16, rejected).
- **The Nacha Phase 2 dates and the False Pretenses definition are accurate** (ADVA-17, rejected).
- **"Directory size is no moat"** stands for the counts. Ren's 1.8M+ is within the IRS universe.
- **UNB-CHAR-DEC-001 survives.** Candid adds no data that Unbound could not get from the IRS. The question still open is auditor acceptance of an Unbound section 8.01 report.
- **Chariot-first for Release 1 survives**, conditional on ADVA-03 and ADVA-12. Because the charity owns its Column DDA, a Chariot change of control does not strand charities. This is rule R5 in 07; Column's participation in an owner-match network is still unconfirmed.

### Recommended revisions

1. **07:** remove the CNV-PAY-007 attribution and cite SPD-CMP-003. Add CNV-PAY-007's debit-block approval to the Chariot checklist. Add to the activation gate:
   - a change-of-control termination right;
   - export of enrolment status and control-change events;
   - an uninsured-balance cap within the CNV-PLT-012 limit;
   - a second rail before scale.
2. **09:** cite the c10 and c11 amendments. Narrow PROP-SEC-02 to poisoning of the IRS-of-record address or phone that the 02 claim routes use.
3. **Owner decision:** whether CNV-PAY-002 (c10) admits a "bank-opened, charity-titled account with partner-attested control events" class. Without it, CNV-EXP-002 cannot be met for Chariot or PayPal enrolments.
4. **20:** re-run with partner coverage from the 08 tiers (central about 0.10-0.20) and the check-share path from 08's p=0.10 case. Also model conversion by enrolment mechanism.
5. **02:** add a section on sponsor-side lock-in and rank the payee layer second. Reclassify "not proprietary" as INFERENCE. Split the non-BMF tail by cause, using a contemporaneous snapshot.
6. **05:** deduplicate BMF rows by EIN and re-run. Add a build/buy/hybrid table, including a Candid cross-check that never runs at decision time, if the licence permits. Plan auditor interviews.
7. **08 and 09:** keep bank-destination evidence per sponsor in Release 1. Share only control and claim evidence and public facts until the benefit is measured, loss allocation is written, and counsel has reviewed the s4.04/s5.02 imputation risk.
8. **Across Track A:** label parity features as parity, and tier proposals into a Release 1 minimum and later work.

### Open questions

- Chariot's contract terms: fees, change of control, export, and uninsured-balance handling. Whether Column takes part in EWS or another owner-match network.
- Real claim and conversion rates under hold-and-claim designs compared with opt-in forms.
- Auditor acceptance of a section 8.01 report not issued by Candid.
- Whether shared integrity flags impute "awareness" to sponsors under Rev. Proc. 2018-32 s4.04(3) and s5.02(2). This needs counsel.

## Track B adversarial review (agent ADVB)

Scope: drafts 10-19 and the onboarding parts of draft 20, with their data CSVs. Machine-readable findings are in `data/adversarial-findings-B.csv` (ADVB-01..19). Sources are in `data/sources-ADVB.csv` (ADVB-001..020). I did not edit any draft.

### Summary

- **2 critical, 12 major, 3 minor upheld or partially upheld; 2 challenges rejected.** The drafts' evidence base is sound. 12 cited claims were checked against primary pages and all matched. The weaknesses are in the *designs and economics built on that evidence*.
- **Critical 1: release-1 scope conflicts with ratified clauses (ADVB-01).**
  - CNV-EXP-002 has `release_scope: initial-implementation`.
  - The 2026-11-25 CNV-ECO-003 amendment requires a 12-month shadow replay of the first paying sponsor's own history.
  - CNV-ECO-004 targets sponsors that already run systems.
  - The proposed R1 scope says "no migration in R1".
  - Draft 10 calls this a "tension". It is a conflict that the owner must resolve.
- **Critical 2: the cutover designs assume the incumbent will cooperate, and public contract terms deny that (ADVB-02).** Draft 17's daily shadow deltas, 90+ days of legacy read-only, vendor-signed packages and repeated production extracts all depend on it. The terms that deny it:
  - NPact allows access by direct login only (§2.4). Export is a paid Professional Service. Data is deleted 10 business days after hosting ends.
  - TIFIN bars downloading.
  - Foundant exports data "as stored" at termination, with no further duty to keep it.
  - Nothing in DAF corresponds to FINRA 11870's "both members must".
- **The "Sponsor Switching Guarantee" is credible only for intervals Unbound controls (ADVB-03).** Donor-level transfers between sponsors are discretionary grants. Fidelity's guidelines say donors have "no legally enforceable right" to a recommended grant.
- **Automation moves work to the customer, and draft 20 undercounts that work (ADVB-06).**
  - The drafts assign the sponsor at least 10 approval and preparation duties.
  - Draft 20 models 530 sponsor hours (about $37k) at 10k accounts.
  - Case evidence points far higher: Hartford spent 4 months on clean-up plus 2 months of dual run, and large sponsors spend $115k-$724k a year on consultants.
- **Draft 20 leaves out material costs (ADVB-05).**
  - Missing items: incumbent tail and remaining-term fees, paid export, auditor uplift, legal, communications, rehearsals, service credits, a failed-migration reserve, and CAC.
  - This does **not** overturn INCLUDE_IN_FEE at 10k accounts or more. Revenue of $4.13M against about $480k in cost absorbs it, so that conclusion rests on the 20 bps revenue assumption (ADVB-13).
  - It does change the picture for small sponsors and for the buyer's total switching cost.
- **Accounting standardisation is feasible, with one gap (ADVB-08).** Draft 16's unit and fee design holds. CNV-FIN-007 grant recognition point has no epoch design, and changing it needs the external auditor's acceptance.
- **AI risk is narrower than feared (ADVB-09).** AI never enters the transform. The residual risk is a semantic mapping error that leaves totals unchanged, which round-trip control totals cannot catch.

### Verification of cited sources (sample of 12)

| Draft claim | Source | Result |
|---|---|---|
| Foundant: 30-day termination for convenience, pro-rata refund, CSV "as stored", custom export billable, client owns data | Foundant MSA v012024 §5.5-5.7, 6.1 [ADVB-001] | Confirmed. Nuance: data is returned only on written request "at the time of termination", and §11.3 adds a 1-year employee non-solicit |
| NPact: 10 business days then deletion; export is a PS; 3-year term, 90-day notice; §2.4 ban | NPact terms, 2025-08-26 [ADVB-002] | Confirmed. Customer owns data (§6.2) |
| Ren: 90-120 days, about $50k, switching "Not difficult at all" | Ren FAQ [ADVB-007] | Confirmed (VENDOR-CLAIM). Ren also says it has "transitioned many existing DAF programs" |
| AEF: 33 months of history (draft 13) against 2 years (drafts 10 and 11) | AEF FAQ [ADVB-005] | Both are correct: 33 months pulled, 2 years reviewable |
| GWCF: 7 years ported, re-registration, MFA, payee validation delays | GWCF post [ADVB-006] | Confirmed |
| NPT: 14-16 weeks | NPT page [ADVB-008] | Confirmed. The page covers new programs, not transfers |
| Foundation Source/Charityvest: "a few business days" | [ADVB-012] | Confirmed. Charityvest is the legal sponsor |
| akoyaGO: 85% on time; 15 days cut to 2-3 days; 32 go-lives | [ADVB-011] | Confirmed (VENDOR-CLAIM) |
| FINRA 11870: 1 and 3 business days; closed exception list | [ADVB-004] | Confirmed |
| CASS: 1.19m switches, 99.7% within 7 working days, 160.5m redirections | [ADVB-009] | Confirmed. 160.5m is cumulative |
| ERISA blackout: 30-60 days' notice; more than 3 business days | [ADVB-010] | Confirmed |
| Fidelity Charitable: about 5 minutes to open | [ADVB-013] | Confirmed (VENDOR-CLAIM) |

Not re-verified: the Foundant beginning-balance page returned 403 (MIG-001). The Nacha return windows (MIG-022) were not read directly.

### Material challenges and verdicts

**ADVB-01: R1 against ratified scope (critical, upheld).**
- Evidence: the clause metadata in `unbound:requirements/convergence/2026-11-24-master/clauses/` (c5 CNV-EXP-002; c10 CNV-ECO-003 amendment) and `17-RELEASE-1-SCOPE.md` line 108 [ADVB-019, ADVB-020].
- Unless the first paying sponsor is greenfield, which CNV-ECO-004 makes unlikely, the first contract needs at least:
  - history extraction;
  - a read-only history import;
  - the CNV-EXP-002 reconciliation report.

**ADVB-02: incumbent non-cooperation (critical, upheld).**
- Draft 10 documents the restrictive terms well. Drafts 11, 15 and 17 then design as if they did not exist.
- The data-ownership question itself is **rejected** for self-sponsored books: Foundant §6.1 and NPact §6.2 vest ownership in the customer.
- The barrier is the means, cadence, format, cost and timing of extraction, not ownership.

**ADVB-03: the Guarantee analogy (major, partially upheld).**
- What survives: rehearsal gates, the quiet period, queued recommendations, redirection from Unbound's own crosswalk, and exit symmetry.
- What does not: any implication that the source side is bound to a clock.

**ADVB-04: private-label and advisor-distributed programs (major, partially upheld).**
- When the legal sponsor is the vendor's charity (RCF, NPT, Charityvest), the distributing firm does not own the assets. Moving the program is fund-by-fund discretionary granting (CNV-ENT-002).
- Draft 14 separates `migration_kind`. Drafts 11 and 20 do not, yet CNV-ECO-004 names advisor-distributed sponsors as part of the entry segment.

**ADVB-05/06: omitted costs and customer-side work (major).**
- The model code (`scripts/economic_model.py`, `onboarding_economics`) has no line for any of:
  - incumbent fees (draft 10's own JCF $417,742 tail);
  - auditor or legal cost;
  - communications;
  - rehearsals;
  - a failure reserve;
  - CAC.
- Sponsor hours come from three ASSUMPTION parameters. The drafts' own duty list (A4 mapping confirmation, restriction classes, fix-in-source, explained differences, CFO dual approval, per-rehearsal controller approval, cutover signature, payee-risk acceptance) is not costed.

**ADVB-07: history depth (major, upheld).**
- Draft 20 says full history is the largest driver but models 7 years.
- Some predecessors cannot supply full history at all; the AEF platform held 33 months.
- CNV-EXP-002 needs a "history available at source" clarification tied to draft 14's `HistoryGap`.

**ADVB-08: CNV-FIN-007 at the epoch (major, partially upheld).**
- Standardised migration is not impractical. Unitized pools, fee accrual and fiscal year-ends are handled in drafts 16 and 17.
- A change of recognition convention at E is not handled. Its activation gate requires the external auditor's acceptance.

**ADVB-09: AI mapping (major, partially upheld).**
- The nondeterminism concern is rejected: draft 15 bars AI, the clock and the network from transforms, and draft 13 bars `Proposed` mappings from production.
- What stands: control totals do not change under role, status or restriction-class swaps. Semantic invariants and mutation tests are needed.

**ADVB-10: audit acceptance (major, partially upheld, INFERENCE).**
- The first sponsor's auditor will not have a SOC 1 Type II report from Unbound that overlaps the sponsor's audit period [ADVB-018].
- Expect more substantive testing and a higher audit fee for the sponsor.

**ADVB-11: lock-in inconsistency (major, upheld).**
- Draft 20 recommends a 36-60-month term with an onboarding-recovery termination fee.
- Draft 10 ranks exactly those mechanics as switching barrier #6, and the exit-symmetry pitch depends on Unbound not having them.

**ADVB-12: differentiation (major, partially upheld).**
- Migration services and tooling are already marketed by Ren, Give Interactive, akoyaGO, Foundant, the Salesforce ecosystem and TIFIN (VENDOR-CLAIM) [ADVB-007, 011, 014-017].
- No one publishes history depth, a reconciliation proof, freeze length or exit schemas. That is not publicly documented, which is not the same as absent.
- The differentiation claim should be about verifiable outcomes, not about "having onboarding".

**ADVB-13: confidence and time-to-production calibration (major, partially upheld).**
- Payback is driven by revenue, and 59 of the 91 parameters are ASSUMPTION.
- The 16-18 week low end is below every case in draft 10, and draft 20 says no benchmark exists even though draft 10 has several.

**ADVB-14: pre-contract data access (major, upheld).** Draft 13's T1 assumes the sponsor holds its data. Hosted incumbents gate exports.

**Minor: ADVB-15, ADVB-16, ADVB-17.**
- ADVB-15: numeric design parameters drift across drafts:
  - freeze of 2 or fewer against 3 or fewer business days;
  - at least 2 against at least 3 rehearsals;
  - different blackout calendars;
  - AEF history depth.
- ADVB-16: draft 11 claims AEF is "the only" public DAF platform-change evidence. Draft 10 documents others.
- ADVB-17: draft 17 applies the R10 60-day window, which covers unauthorized consumer debits, to grant credits.

### What I could not refute (findings that survived)

- The incumbent contract terms, timelines and case facts in draft 10. Every sampled claim matched its primary source.
- The core freeze evidence: the user-visible freeze (4 days to about 5.5 weeks) and credential re-registration are the documented friction. GWCF confirms re-registration and payee-validation delays.
- Draft 17's rejection of fund-cohort cutover within one sponsor (two writers on shared bank, pool and GL accounts), and its rollback boundary at the first irreversible external effect.
- Draft 16's "no plugs, exact units, deterministic residual allocation" approach.
- The economics at entry scale: at 10k accounts or more, onboarding cost (even several times higher) does not threaten payback at 20 bps. The live risk is whether sponsors will pay that revenue, not onboarding cost.
- Draft 15's determinism contract and the confinement of AI to proposals under CNV-AIO-001/002.
- Draft 14's opening-balance epoch plus a non-posting legacy-history partition. It is consistent with the append-only ledger and has vendor precedent.

### Recommended revisions (priority order)

1. Escalate ADVB-01 to the owner as a ratified-scope conflict. Decide whether migration (at least history extraction and read-only import with reconciliation) is an R1 or R1.x gate.
2. Add an incumbent **Extraction Plan** to drafts 13 and 15, covering:
   - contract end date and notice deadline;
   - export rights and the permitted export method;
   - cost and allowed cadence of extracts.

   Also:
   - Keep legacy read-only in Unbound's own L0 vault.
   - Make shadow-run cadence conditional on what the incumbent contract allows.
   - Start the Guarantee clock only on receipt of a conforming source package.
3. Re-scope draft 11's Guarantee to Unbound-controlled terms, drop the CASS/ACATS equivalence claim, and cost the service credits.
4. Split advisor-distributed programs on vendor sponsors out as sponsor-to-sponsor transfers in drafts 11, 13 (T0 question) and 20.
5. Extend draft 20 with:
   - a buyer switching-TCO table;
   - sponsor hours modelled duty by duty;
   - incumbent, audit, legal and communications costs;
   - rehearsals, a risk reserve and CAC;
   - history years by sponsor age;
   - time to production calibrated to draft 10's cases;
   - confidence lowered to Low.

   Then reconcile the termination-fee recommendation with exit symmetry.
6. Add a CNV-FIN-007 epoch gate (drafts 16 and 17), semantic mapping invariants and mutation tests (draft 13), and a SOC 1 timing plan (drafts 16 and 20).
7. Put the numeric design parameters in one table owned by draft 17. Fix the minor overclaims in ADVB-16 and ADVB-17.

## Adversarial review X: cross-cutting economics and strategic logic (ADVX)

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Machine-readable findings: `data/adversarial-findings-X.csv` (ADVX-01 to ADVX-17). Sources: `data/sources-ADVX.csv` (ADVX-001 to ADVX-010).

Sensitivity runs: `scripts/advx_sensitivity.py`. It loads `scripts/economic_model.py` read-only and overrides parameters in memory. Output: `data/advx-sensitivity-output.csv` (regenerated after the revision-3 model; numbers quoted in this section are from the revision-2 model the reviewer tested). No package file other than the two ADVX CSVs was written. `python3 -I scripts/economic_model.py --report` reproduces the tables in 20.

### Summary

- **Critical (ADVX-10, upheld, INFERENCE).** The package treats the charity network and onboarding friction as the binding barriers. No evidence in the package or the repo shows that a sponsor chose or left a vendor for either reason. The evidence points to distribution and incentive alignment instead:
  - MS GIFT's FY2024 990 pays Morgan Stanley $4.24M as "INVESTMENT ADVISOR" alongside RenPSG's $14.93M [ADVX-009].
  - Affiliated managers earn bundled fees of 23-93 bps (price-observations.csv).
  - TIFIN pays DAF advisers 0-100 bps subadvisory fees.
  - Ren distributes through its own charity, RCF, to wirehouse programmes.
  - Ren itself says switching is "Not difficult at all" [ADVX-003].
  - Only 1 of 26 faith or national iPhi sponsors left between 2023 and 2026.
  - So the moat is distribution and incentive alignment. The network and onboarding are necessary conditions that remove objections, not the reason a sponsor buys.
- **First-sponsor economics (ADVX-03, upheld).** INCLUDE_IN_FEE is computed on contribution *before* organisation fixed cost and build amortisation. Net of $1.66M org cost and $1.0M a year of build amortisation, a 10k-account sponsor pays back onboarding plus CAC in 6.8 months at 20 bps. At 15, 12.5 and 10 bps it never pays back, and in the high cost case it never pays back even at 20 bps. The rule is valid only as a marginal-sponsor test once fixed costs are covered.
- **Ratified-clause conflict (ADVX-04, upheld, VERIFIED-FACT).** 20 does not meet CNV-ECO-003 or CNV-ECO-005 in five ways:
  - its base case is the AI-native lever case, not C0;
  - it has no P10-P90 range;
  - it does not report viability at P90 cost;
  - it has no pre-delegation phase;
  - it has none of the clause's stress scenarios and does not apply the 25% concentration cap.
- **Track A is understated (ADVX-01, upheld).** The modelled $75k a year omits stewardship and disputes (CHAR-ADR-002/006/007), counsel review of every eligibility rule (CHAR-ADR-010), the Nacha TPSP annual Rules compliance audit and Phase 2 monitoring [ADVX-001, ADVX-002], verification vendor minimums, a charity support desk and a media-liability rider.
  - Adding these as ASSUMPTION ranges gives $176k / $316k / $509k a year.
  - At 70k grants, the per-grant cost moves from $1.98 to about $5.42.
- **Price (ADVX-05, 06 and 07).**
  - **20 bps is parity or slightly above** observed outsourced *staffed* administration: Ren takes 18.5 bps at MS GIFT and 13-14 bps at Stifel.
  - **20 bps is 2-6x the software lines** paid by self-staffed sponsors: Ren at NCF is 4.67 bps, or $81 per account.
  - **Who pays:** the servicer's fee comes out of donor-paid fee schedules. RCF pays Ren 98% of fundholder fees [ADVX-008]. Unbound therefore competes with the sponsor's retained margin.
  - **Onboarding in the fee survives a 10-15 bps market** only for 10k+ sponsors in the base cost case. In the high cost case it fails at 12.5 bps or less. At a software-like $81 per account, payback is 20.6 months in the base case and never in the high case.
- **Internal inconsistencies with 08 (ADVX-13 and 14, upheld).**
  - **Partner coverage.** 20 assumes 50%, anchored on Fidelity's own enrolment. 08 models 2-20% per recipient and 8-21% of grants at go-live.
  - **Check share.** 20 assumes 10%. 08 has 15-37% of grants still paper after 3 years.
  - **Effect.** With 08's values, e-pay value per 10k sponsor falls from $75k to $9.8k a year.
  - **Consequence (ADVX-15).** Measured network value is smaller than Track A run cost at entry scale. The registry is a mandated compliance cost (UNB-CHAR-DEC-001, CNV-GRT-003), not a value lever.
- **Rejected or confirmed.**
  - **Open data (ADVX-09).** 05 already defers it and concedes that it does not erode incumbents. ADVX agrees.
  - **Unit-cost quotes (ADVX-17).** The Stripe, Ren and balance inputs check out.
  - **Parity (ADVX-11).** Most proposed network capabilities are parity, and the package largely concedes this. Ren already offers "Charities sign up for ACH once ... for every DAF program we support" [ADVX-004].

### Sensitivity results (ADVX re-run; INFERENCE from package ASSUMPTION parameters)

Payback in months on onboarding plus CAC. **Marginal** is the package's sponsor-contribution view. **First sponsor** is net of $1.66M org fixed cost and $1.0M a year of build amortisation.

| Sponsor | Fee | Marginal, base | Marginal, high cost | First sponsor, base | First sponsor, high cost |
|---|---|---|---|---|---|
| 10k accounts | 20 bps | 1.9 | 10.7 | 6.8 | never |
| 10k accounts | 15 bps | 2.6 | 19.5 | never | never |
| 10k accounts | 12.5 bps | 3.2 | 33.0 | never | never |
| 10k accounts | 10 bps | 4.3 | 106.4 | never | never |
| 1k accounts | 15 bps | 19.9 | never | never | never |
| 10k accounts | $81 per account (Ren software at NCF) | 20.6 | never | n/a | n/a |
| 10k accounts | $250 per account | 3.3 | 37.0 | n/a | n/a |

Track A annual opex per grant. All columns add the base establishment cost ($319k) amortised over 5 years, as 20 does:

| Grants a year | 20 (package) | ADVX low | ADVX base | ADVX high |
|---|---|---|---|---|
| 70k (one 10k sponsor) | $1.98 | $3.42 | $5.42 | $8.18 |
| 700k | $0.20 | $0.34 | $0.54 | $0.82 |

### Remaining competitive barriers after the recommendations (ADVX-12)

Each barrier below is INFERENCE.

1. **Vendor-owned sponsor programmes.** Wirehouse and advisor programmes that sit on a vendor's own charity (RCF, NPT, Charityvest) move only fund by fund.
2. **Affiliated investment-fee economics.** These shape who the sponsor or its parent wants as administrator.
3. **Incumbent payment volume.** Ren claims 1.7M grants a year [ADVX-004], which keeps compounding its charity enrolment.
4. **Non-portable enrolments.** Ren RDE enrolments do not move to non-partner rails.
5. **Buyer switching cost.** The buyer's own switching TCO is $170k-846k in the base case, and the buyer needs project capacity.
6. **New-entrant risk.** Unbound has no references and no SOC 1 Type II, and early on it depends on its first sponsor, which runs against the 25% concentration cap.
7. **Incumbent exit terms.** Incumbents' contracts limit exit data.

### Claims verified (10 checked)

| Source | What was confirmed |
|---|---|
| ADVX-001 | Nacha: TPSPs must do an annual Rules compliance audit, Article One 1.2.2 |
| ADVX-002 | Nacha Phase 2: effective 2026-06-19, applies to TPSPs; "False Pretenses" includes misrepresenting account ownership (re-verifies PAY-026) |
| ADVX-003 | Ren: "90-120 days", "around $50,000", switching "Not difficult at all" (re-verifies ONB-020) |
| ADVX-004 | Ren: "1.8M+" charities, "1.7M" grants a year, "sign up for ACH once ... every DAF program" (re-verifies REN-002) |
| ADVX-005 | Stripe: $1.50 instant verification, $1.50 ownership, micro-deposits free (re-verifies ECO-003) |
| ADVX-006 | Fidelity: 67% of 3M grants electronic in 2025, via Chariot (re-verifies ECO-005) |
| ADVX-007 | Chariot deposit account "legally owned by your organization"; "cannot 'bring your own'" (re-verifies PAY-006) |
| ADVX-008 | RCF audited note 9: Ren receives 98% of fundholder fee revenue; $19,225,546 in 2024 |
| ADVX-009 | MS GIFT FY2024 990: RenPSG $14,930,249; Morgan Stanley $4,237,948; 21,800 DAFs; $9.11B at year end (re-verifies PRC-O-001) |
| ADVX-010 | **Not verified.** The MS GIFT donor circular downloaded, but its PDF text did not extract. The tiers rest on internal PRC-O-004 |

### Implications for Unbound

- **Lead the go-to-market with distribution fit.**
  - Neutrality on investment and custody: advisor-managed accounts, custodian feeds and the CNV-GRT-009 engaged-manager programme.
  - Sponsor-margin-preserving pricing.
  - Treat charity network breadth as a secondary message.
- **Price by buyer type.** Use servicing-economics' per-account plus low-bps tariff. Test it against the incumbent's *realised* take, not against donor list fees.
- **First-sponsor cost recovery.** Treat onboarding for the first sponsor as up-front or co-funded, not absorbed.
- **Stage the registry** to the first sponsor's real recipient set.

### Open questions / evidence gaps

- **Why sponsors choose and leave vendors.** There are no win/loss or switching-reason data for any national, faith or advisor-distributed sponsor. This is the largest gap.
- **Realised servicer take at self-staffed sponsors.** It is visible only as 990 top-5 contractor lines.
- **Cost of the Nacha TPSP audit and of verification vendor minimums.** No public quotes were found.
- **The real conversion rate p.** It must be measured in the CNV-ECO-003 shadow period.

### Candidate requirements

Each candidate is a RECOMMENDATION.

- **Refine CNV-ECO-003 conformance.** Sponsor economics SHALL report both a marginal and a first-sponsor (fixed-cost-bearing) view on the C0 base.
- **New: residual-barrier register.** A register with an owner per barrier, maintained alongside the CNV-ECO-004 target list.
- **Refine CNV-ECO-002.** Pricing SHALL show the sponsor's net margin change against the incumbent servicer's realised take.
- **Refine UNB-CHAR-DEC-001.** Sequence registry scope by recipients actually paid.
