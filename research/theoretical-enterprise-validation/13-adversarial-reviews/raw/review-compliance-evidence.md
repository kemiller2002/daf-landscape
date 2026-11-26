# Role-separated review: compliance and evidence

**Subject:** `research/theoretical-enterprise-validation/` (all .md files, `16-registers/*.csv`, skim of `11-scenarios/scenarios.csv`).
**Reviewed against:** `docs/` (financial core v0.5, administration, assurance methodology) and `research/ai-native-daf-enterprise/` (regulatory map and matrix, controls.csv, control-framework, continuous-compliance, governance-architecture, identity federation, accountability matrix, DECISION-LOG, WF-01/WF-05/WF-09, executive report, 09 model, digital twin, experiments, adversarial review, failure modes).
**Date:** 2026-11-22.
**Independence:** this is critique by the same model family in a separate role and context. It is not independent validation. No counsel, CPA or auditor took part. Statements of law marked **[unverified]** come from background knowledge. Nothing was fetched from primary legal sources for this review.
**Snapshot caveat:** `16-registers/findings.csv`, `assumption-register.csv`, `owner-decisions.md` and `requirements.csv` appeared while this review was running. `LEDGER.md`, `13-adversarial-reviews/role-reviews.md` and `11-scenarios/scenario-library.md` were linked but did not exist at review time.

Severity scale: 5 means it could cause legal exposure or irreversible loss if relied on. 3 means a material misstatement or a build defect. 1 means editorial.

---

## Part A: Compliance reviewer

**A1. REG-001 is placed in class 1 ("verified legal requirement – design to them now") as a whole.** File: `08-compliance/compliance-and-controls.md` §1, class 1; `16-registers/contradiction-register.md` TVC-003.
- *Problem:* the [F] label on REG-001 covers the statutory text it read (20%/5% excise rates, the $10,000 cap, the exceptions). The row's design-implication and human-authority columns are the baseline author's interpretation: "sponsor-signed approval on every grant" and "approval authority cannot be vested in software or a vendor". The program puts the whole row in class 1. TVC-003 then treats the interpretive text as the legal side of a contradiction. §4966 does not on its face require a per-grant human signature **[unverified]**. The manager tax attaches only to a manager who *knowingly* agrees, and it is capped. Those facts cut both ways on DD-004, and the program does not discuss them.
- *Severity:* 4.
- *Correction:* split every REG row into (i) statutory or regulatory text [F/S/K] and (ii) design implication [I/C]. Restate TVC-003 as "statute silent on approval mechanism; baseline interpretation demands per-grant human approval; counsel required (OD-01)". Keep the DD-004 hypothesis status.

**A2. "Exclusive legal control" and "recommendation is a request" are cited as "§4966(d)(2) [V via REG-001]".** File: `02-ontology/enterprise-ontology.md` (Sponsoring organization row); `07-financial-invariants/financial-invariants.md` §1 fact 1; `03-organization/organization-and-authority.md` §5.1.
- *Problem:* the REG-001 row says nothing about §4966(d)(2). The phrase "exclusive legal control" is the §170(f)(18) acknowledgment wording (REG-008 [F]). The statute defines a DAF as owned and controlled by the sponsor, with donor "advisory privileges" **[unverified wording]**. That a recommendation is a request is a reasonable inference from that definition, not a validated quote. The [V] label is unsupported.
- *Severity:* 3.
- *Correction:* cite §170(f)(18) via REG-008 [F] for the exclusive-legal-control wording. Label the request-not-instruction reading of §4966(d)(2) as [I] with a [C] flag. The same mis-cite is inherited from DD-003 and the executive report l.72, and it should be flagged there too.

**A3. Class 6 ("unverified assumption… not to be cited as obligations") treats an evidence label as a legal status.** File: `08-compliance/compliance-and-controls.md` §1, class 6.
- *Problem:*
  - REG-015 (§509 public support; losing it ends DAF sponsorship), REG-026 (§6001), REG-049 (state breach notification) and REG-064 (E-SIGN) are labelled [K] because they were not fetched. That does not make them assumptions. Telling `docs/` not to cite them risks dropping real obligations.
  - The bookkeeping is also wrong in four places:
    - the stated count is 11, but 9 IDs are listed;
    - REG-025 is in both class 4 and class 6;
    - REG-059 [K] is in class 4;
    - REG-045 [K] is in class 2.
- *Severity:* 3.
- *Correction:* classify by legal nature (statute / guidance / contract / convention) and carry the evidence label in a separate column. For a high-impact [K] row, the action is "verify now", not "suppress".

**A4. Retention is left without any period, although a verified period exists.** File: `08-compliance/compliance-and-controls.md` §1 "Retention"; ontology retention classes; TVC-016; TVA-023.
- *Problem:* the program places REG-037 in class 1 ("verified, design to it now"). REG-037 is [F] and states 10-year OFAC recordkeeping (31 CFR 501.601, as amended; baseline says published 2025-03-21 **[unverified date]**). The program still says "No requirement in this program states a period" and leaves R-OFAC to counsel. TVC-016 also labels the baseline's "10-year default driven by OFAC" as [S]. In fact REG-026 is [K], and its OFAC basis is REG-037 [F].
- *Severity:* 3.
- *Correction:* set R-OFAC to at least 10 years, citing REG-037 [F]. Leave R-TAX, R-CORP and R-PII to counsel. Fix the TVC-016 label.

**A5. OFAC blocking and reporting are treated as discretionary, and no blocked state exists.** File: `11-scenarios/scenarios.csv` TVS-024 ("Recall attempt; sanctions officer; reporting decision"); `06-state-models/state-models.md` §3 (Recall → Recalled → funds back); `08-compliance/compliance-and-controls.md` §4 ("TVCTL-04 for part of REG-037").
- *Problem:*
  - REG-037's design implication requires the ability to *block* funds in a segregated interest-bearing account, "rather than simply return funds".
  - Blocked-property and rejected-transaction reports are mandatory within 10 business days under 31 CFR 501.603/604 **[unverified as applied to a recalled in-flight grant]**.
  - The program inherits WF-09's "Any reporting to OFAC is decided by the sanctions officer and the GC" without challenge. A recalled payment in which a newly listed SDN has an interest may itself be blocked property **[unverified]**.
  - TVCTL-04 is a pre-submission gate. It files no report and keeps no blocked-funds ledger, so it covers none of REG-037's reporting.
- *Severity:* 4.
- *Correction:*
  - add `Blocked` as a payment-attempt outcome and a blocked-property ledger account;
  - make the reject/block report a mandatory obligation with a deadline, and limit officer discretion to *classification*;
  - remove the claim that TVCTL-04 covers REG-037;
  - mark the recall path [C].

**A6. TVR-SAN-001 ("donor or advisor listing freezes the fund… strict-liability compliance") is presented as law.** File: `16-registers/requirements.csv` TVR-SAN-001; TVF-027.
- *Problem:* whether an SDN donor or advisor has a blockable "interest" in sponsor-owned DAF assets through advisory privileges is a legal question **[unverified]**. The answer may be over-blocking (a policy choice) or blocking (which triggers A5's reporting). The requirement carries no [C].
- *Severity:* 3.
- *Correction:* label it [C]. Specify both branches: blocked, with report and blocked ledger; or policy freeze, with no report.

**A7. The sanctions contradiction (TVC-006 / TVF-048) is rated severity 5 when it is a wording issue.**
- *Problem:* REG-036 says "automation may clear obvious false positives under a documented rule". That is deterministic-rule clearing, which is the program's own recommended resolution (b). The qualifier "AI may never close a *high-score* match" is loose wording, not a licence for model clearing. REG-036 is also [R], not [F].
- *Severity:* 2. The underlying risk is real, but the contradiction is overstated.
- *Correction:* recast it as an ambiguity to tighten in text, at severity 3. Keep TVR-SAN-002.

**A8. Disqualified supporting organizations are missing from the routine path.** File: `05-workflows/workflow-catalog.md` CW-01 preconditions and decisions; ontology "Recipient status: IRS sources for reliance".
- *Problem:* the §4966 exception for §170(b)(1)(A) recipients excludes disqualified supporting organizations: Type III non-functionally-integrated, and Type I/II controlled by the donor or advisor (§4966(d)(4)) **[unverified detail]**. Donor control is not in Pub 78 or the BMF. The baseline 09 model explicitly notes that its proxy "misses donor-controlled supporting organizations". The program, which set out to find where the baseline is wrong, does not carry this forward.
- *Severity:* 4. Statutory exposure on the no-touch path.
- *Correction:*
  - CW-01 eligibility must classify supporting-org type from the BMF subsection or foundation code;
  - it must run a donor/advisor-control check against the related-party registry (REG-004 data);
  - any Type I/II/III supporting org goes to H unless policy proves it is not disqualified [C].

**A9. Rev. Proc. 2018-32 reliance is narrowed and its exceptions are omitted.** File: ontology §3 ("IRS sources for reliance… vendor data may add flags, not clear them"); TVS-023, TVS-026.
- *Problem:*
  - REG-019 says reliance is also available on third-party BMF reports that meet §8.01 content rules, provided a copy is retained.
  - REG-019 is [R], not re-read.
  - The reliance exceptions (grantor responsible for, or aware of, the loss of status) **[unverified]** are the ones that matter for the sham-charity and ATO scenarios, and they are not stated.
- *Severity:* 2.
- *Correction:* state the §8.01 retained-copy requirement as an invariant on EligibilityFact. Allow qualifying third-party reports. Add the knowledge exception to TVS-023 and TVS-026.

**A10. Excise-tax exposure is mis-stated in two places.**
- *Problem:*
  - FMEA-03 lists "§4966 exposure" for ATO-originated grants to a Pub 78-listed sham charity. Grants to §170(b)(1)(A) organizations are excepted from taxable distributions **[unverified for the sham case]**, so the exposure is loss, fiduciary and reputational.
  - `15-economics/economic-model.md` §5 says §4966 imposes "5% on approving managers". REG-001 says 5% on a manager who *knowingly* agrees, capped at $10,000 per distribution. A deterministic misconfiguration may involve no knowing manager.
- *Severity:* 2.
- *Correction:* restate both, citing REG-001 exactly.

**A11. The Nacha return rules are mis-applied and over-labelled.** Files: compliance §1 [V] paragraph; `06-state-models/state-models.md` §2 (`Final → Returned: late return (rail allows, e.g. unauthorized-debit class)`); TVF-002 ("ACH credits can return after settlement… Nacha return rules [V]").
- *Problem:*
  - (a) The verified fact concerns unauthorized **debits** (R10). Grant payments are outbound **credits**, and R10 does not apply to them. Late credit returns exist only in narrower forms, such as an ODFI-requested or permissible return with ODFI agreement **[unverified]**. The [V] source does not support TVF-002.
  - (b) The extended-return deadline is commonly stated as "opening of business on the second banking day following the 60th calendar day after settlement" **[unverified]**. The text says "banking day after the 60th".
  - (c) R10 applies to consumer accounts. Unauthorized debits to business accounts use R29 with the two-day window. CON-1 should be specific to SEC code and account type.
  - (d) The Nacha web summary pages are not the Operating Rules text. [V] should be [S], or the label should say it rests on secondary summaries.
- *Severity:* 3.
- *Correction:* separate a debit-contribution return model from a credit-grant return model. Re-label the source.

**A12. Contribution timing and acknowledgment claims.** File: `12-failure-analysis/failure-analysis.md` §4 ("contributions must be received by 12/31 [I]"); CON-2; TVC-023.
- *Problem:*
  - Deduction timing follows delivery rules (for example, a check is deemed delivered when mailed) **[unverified]**, not sponsor receipt.
  - A contemporaneous written acknowledgment only has to be in hand by the earlier of the filing date or the due date **[unverified]**, so CON-2's delay to `Final` is legally feasible.
  - The program leaves both [C] without stating the strongest available reading.
- *Severity:* 2.
- *Correction:* state the likely rule with [unverified], and keep counsel review for edge cases (debits reversed after the acknowledgment was issued).

**A13. The SOC framing does not distinguish sponsor from provider.** File: TVC-027; compliance §2 ("TSC = … common-criteria families" and then "TSC processing integrity").
- *Problem:*
  - SOC 1 and SOC 2 reports are issued about *service organizations*. A sponsor running its own platform is covered by a financial-statement audit, not a SOC 1. SOC 1 is relevant only where the operator serves other sponsors (Model C/D) **[unverified for edge structures]**.
  - Processing integrity is a separate TSC category, not a common-criteria family.
- *Severity:* 2.
- *Correction:* make the assurance target conditional on the operating model (TVR-CMP-003) and fix the TSC terminology. No compliance claims were found, which is correct.

**A14. "Independent verification: external auditor" is used as a control component.** Controls TVCTL-07, -08 and -11.
- *Problem:* the entity's control design cannot depend on its external auditor; auditor independence prevents it. Auditor testing is assurance over controls, not a control.
- *Severity:* 3. A skeptical auditor would reject this.
- *Correction:* assign independent verification to internal audit or a second-line function. List the external auditor only under "assurance".

**A15. The privacy-retention conflict is overstated, and roles are missing.** File: compliance §1; CW-35; TVF-074.
- *Problem:*
  - The REG-048 state laws generally exempt data kept to comply with legal obligations **[unverified]**, and many exempt 501(c)(3)s altogether.
  - The program does not distinguish sponsor-as-controller from provider-as-processor.
  - It does not carry GLBA (REG-047) for a for-profit provider.
- *Severity:* 2.
- *Correction:* model precedence as "statutory retention exemption first, then hold, then deletion". Add controller and processor roles per operating model.

**A16. The escheat and uncashed-check treatment presumes outcomes.** File: state models §2 ("Not drawn but required: `Escheated`"); FI-21.
- *Problem:*
  - REG-045 [K] says it is unsettled whether a voided DAF grant check is property owed to the grantee.
  - FI-21 ("issued-not-presented stays as a liability, not as fund cash") is an accounting conclusion that is not marked [C].
- *Severity:* 2.
- *Correction:* model `Escheated` as a conditional state pending counsel, and mark FI-21 [C].

**A17. The financial invariants omit when the grant liability is recognized.**
- *Problem:* the 12-fact table and FI-17 post journals only at settlement. Under ASC 958, an approved unconditional grant communicated to the grantee may be an expense and liability at approval **[unverified, CPA]**. The document disclaims accounting conclusions, but it never raises this question.
- *Severity:* 3.
- *Correction:* add an invariant or open item: "grant payable recognition event [C]". Tie it to the approval or notification design.

**A18. §4958 (REG-004) has no invariant or control.**
- *Problem:*
  - REG-004 requires a hard block on any payment from a DAF to a donor, advisor or related party, including fees to advisors' firms. The program never mentions it. Baseline CTL-007 blocks related *approvers*, not related *payees*.
  - FI-20 lists "excess benefit discovered" under recipient refunds. §4958 correction is a statutory process on the disqualified person, not a refund **[unverified detail]**.
  - REG-005 (investment advisors as disqualified persons) is in the ontology but is not linked to FEE or SPEND.
- *Severity:* 3.
- *Correction:*
  - add FI/TVCTL "payee ∉ related-party registry" at payment gate and fee posting;
  - separate §4958 correction from FI-20;
  - link REG-005 to FEE-12.

**A19. The unmapped-obligation list is inconsistent with the program's own classification.** File: compliance §4; TVF-045.
- *Problem:*
  - The list contains 28 IDs, while TVF-045 says "about 25".
  - It includes rows the program told `docs/` not to cite (REG-015, 026, 049, 050, 064).
  - It includes REG-042/043 without the operating-model condition (REG-042 is "applies_sponsor: no (inference)").
- *Severity:* 2.
- *Correction:* give the exact count, and condition each row by model and evidence status.

**A20. The TVCTL-12 mapping "REG-002 [K → C]" understates the obligation.**
- *Problem:* the ER obligation is statutory and [F]. Only the §53.4945-5 mechanics are [K], per the REG-002 verification note.
- *Severity:* 1.
- *Correction:* "REG-002 [F]; mechanics [K]".

---

## Part B: Independent evidence reviewer

**B1. "Cancellation after approval is missing from the baseline" is wrong.** Files: TVC-021, TVF-005, state models §2 bullet list and §10 ("Missing (baseline) … `Approved → Canceled`").
- *Problem:* the WF-01 mermaid diagram in `wf-contributions.md` contains `Approved --> Canceled: donor cancels before release`. The real defects are different: the baseline lets the *donor* cancel an approved grant (which the program elsewhere says should be a sponsor decision), and there is no cancel after `Released`.
- *Severity:* 3.
- *Correction:* restate the finding as "donor-initiated cancel of a sponsor-approved grant; no cancel or recall after release".

**B2. TVF-016 cites the wrong line.**
- *Problem:* it cites `governance-architecture:108`. Line 108 is the SPOF-register pointer. The ≤$250k routine row is at l.40.
- *Severity:* 1.
- *Correction:* fix the line.

**B3. E9 is mischaracterized.** File: `01-discovery/requirements-inventory.md` §3 item 9; TVC-024.
- *Problem:* the program says E9 "assumes bank-side ACH deduplication that ACH does not provide". `experiments.md` l.32 and l.194 say the opposite: "ACH has no end-to-end idempotency key, so deduplication depends on the originating bank's API", flagged as a load-bearing caveat. The baseline already disclosed the issue, so there is no internal contradiction.
- *Severity:* 2.
- *Correction:* reword it as "E9 shows exactly-once needs counterparty dedupe that ACH lacks; the core invariant 7 therefore depends on provider choice".

**B4. The third leg of TVC-017 ("tech-arch 10–30× vs twin ×3") is not a contradiction.** File: TVC-017; inventory item 8.
- *Problem:* `technology-architecture.md` l.20 states per-second throughput peaks. The program's own `economic-model.md` §3 says exactly this. The register contradicts the economics document.
- *Severity:* 2.
- *Correction:* drop that leg from TVC-017.

**B5. The economics claims agreement with the twin and understates the backlog.** File: `15-economics/economic-model.md` §3.
- *Problem:*
  - "This matches the twin's '34 days over SLA'" compares a backlog size (37 days of capacity) with a count of days over SLA.
  - The twin's surge runs to day 365 (`digital-twin.md` l.31), so its count is truncated at year end.
  - At average staffing, capacity is 256/day and post-surge arrivals are about 213/day. Net drain is about 43/day, so a 9,600-case backlog takes about 220 working days to clear.
  - The model's own arithmetic therefore implies a much worse outcome than "matches the twin".
- *Severity:* 3.
- *Correction:* report clearance time. Withdraw "matches".

**B6. TVC-006 is over-rated, and REG-036 is [R], not [F].** See A7.
- *Severity:* 2.

**B7. The coverage over-claim (TVC-015 / TVF-064) is partly overstated.**
- *Problem:*
  - "Obligation coverage is 100%" appears in `control-framework.md` l.31 under "Key invariant", which is a design target, not a measured claim. "45 controls" against 54 rows is accurately reported.
  - TVF-040 says no failure response or reviewer fields exist. `docs/administration` GOV-06 already requires "exception, remediation and reviewer signoff", which is relevant to TVF-030.
- *Severity:* 2.
- *Correction:* say "stated as an invariant with no measurement", and cite GOV-06.

**B8. TVC-016 has a wrong evidence label.** See A4.
- *Severity:* 2.

**B9. The charter count is wrong.**
- *Problem:* the charter scope says "50 controls". The program's own inventory and controls.csv say 54.
- *Severity:* 1.

**B10. Several cited artifacts do not exist.**
- *Problem:*
  - At review time, the charter and other files linked `LEDGER.md`, `13-adversarial-reviews/role-reviews.md` and `11-scenarios/scenario-library.md` §4 (saturation tracking), and none of them existed.
  - The charter's independence statement ("some passes ran in separate contexts") and the stopping rule ("saturation measured as new material findings per round") therefore rest on no artifact.
  - The inventory's "reports were checked against the source text for every item used" has no trail either.
- *Severity:* 3.
- *Correction:* create the artifacts, or remove the claims.

**B11. The experiment list in TVF-061 omits E10.**
- *Problem:* E10's flag-only arm hard-codes `EscapedDefects = 0` (adversarial review l.96). That is the experiment most relevant to DD-005, which the program keeps as a "baseline strength".
- *Severity:* 2.
- *Correction:* add E10, and note that DD-005's support is legal and design reasoning, not E10.

**B12. Some conclusions rest only on the program's own earlier artifacts.**
- *Problem:*
  - (a) The failure analysis §5 says "TVCTL-05's fallback keeps release safe… supports DD-002". The fallback (a keyword/rule screen) is undesigned and unmeasured.
  - (b) Organization §4: "graph-colouring gives at least 4" is asserted without the graph. It is then said to be "consistent with" the baseline 8–10 floor.
  - (c) The alternatives recommendations (1D sleeve, 3C provisional credit) are scored with the program's own [A] parameters (10 bps drag) and then cited back as OD-13 recommendations.
- *Severity:* 3.
- *Correction:* label these as [T]/[I] hypotheses, show the derivation in (b), and remove "supports DD-002".

**B13. Some labels are inflated.** File: economic-model §2 and §5.
- *Problem:*
  - "g 6.2–13.0 [V]" was computed by the baseline from a 990-derived dataset, not verified by the program.
  - "$4.5–6k average grant [V per baseline]" comes from `mission-2026-11-14/b51-03-grant-size-distribution.md`, which labels it [C] (computed), not [V].
- *Severity:* 2.
- *Correction:* use "[R: baseline-computed]".

**B14. FM-03 is mis-cited.**
- *Problem:* `alternatives.md` §7 cites FM-03 for correlated error "across sponsors". FM-03 concerns correlated errors across *agents* that share a base model.
- *Severity:* 1.

**B15. REG-042/043 are given the label "[I]".**
- *Problem:* compliance class 2 labels them "[I]". The map labels are [F] and [S].
- *Severity:* 1.

**B16. The novelty of the deprovisioning gap (WG-2 / TVC-032 / TVR-WID-006) is overstated.**
- *Problem:* the baseline already has federation-agreement deprovisioning timing (identity l.83), CTL-052 (latency monitored against the agreement) and a go-live conformance test (l.88).
- *Severity:* 2.
- *Correction:* reframe the gap as "no stated end-to-end maximum combining partner and platform latency".

**B17. A baseline section error was not caught.**
- *Problem:* DD-004 and WF-01 cite "§4966(c)(1) excepts grants to §170(b)(1)(A)". REG-002 in the same baseline places the exceptions in §4966(c)(2). The program inherits DD-004's grounding without noticing.
- *Severity:* 2.

---

## Checked and could not fault

- The contradiction-register status counts (7/12/10/5 = 34).
- TVC-004/005 thresholds (control-framework l.58–60; governance-architecture l.40–46).
- TVC-025 (identity l.61, l.72–73; $250k routine).
- TVC-018 "~20 at any scale" (clarity-edf l.246).
- TVC-027 quote (assurance-methodology l.28).
- TVC-034 (REG-007 cites REG-061).
- TVC-028 and TVF-041/042 against accountability-matrix C3.4, C4.2, C4.5 and C5.6.
- The REG-001 quotes used in TVC-003.
- The governance-architecture board column "—" for routine grants, and the map's reconciling "design rule" (l.207).
- WF-01: the 2-minute wait then proceed; post-payment review; `ContributionSettled` issues units; acknowledgment generated from the settlement event; `Reconciled (terminal)`; no Paid→Returned or Unknown.
- WF-05: "Approved grants earmark units"; no authority re-check (the eligibility-only paraphrase drops "and sanctions", but the point stands).
- DD-005 and CTL-008 wording.
- DD-014 contents.
- Financial core invariants 3, 7 and 10, "observation", and the event-sourcing quote.
- controls.csv: 54 rows and the column set as described.
- CTL-037 scope per continuous-compliance l.45 (`current_law` ∧ `sponsor=yes`).
- CTL-044 exists for escheat.
- 09 model l.18 (g range) and l.22 (staffing formula).
- Executive report: l.198 surge quote, 30 FTE, $272 and $790, R1 Low-Medium, 19 agents.
- E4 15.5-day age; E6 35/34/25/23.
- REG-020 "Notice 2006-109 UNVERIFIED"; REG-002 mechanics [K]; REG-045 [K].
- All class-1 example rows carry [F].
- Economic arithmetic (low/expected/high FTE and cost; peak/average ratios; $4 and $77 AI break-evens; $16m/day; 10 bps drag; 21 reconciliation FTE).
- Corpus counts (81 decisions, 24 WF, 58 events, 36 APIs, 40 gaps with 9 P0, 22 SC, 25 FM, 19 AC).
- The OPS-01 ID collision (widgets/05 and administration/03).
- AUTH-06 wording.
- The Nacha two-banking-day general return deadline (consistent with my understanding **[unverified]**).
- No SOC 1/SOC 2 compliance claim is made anywhere in the program.

---

## Citation check table

| # | Claim (program file) | Cited source | Verdict |
|---|---|---|---|
| 1 | Class 1 rows REG-001/003/004/008/009/011/013/024/037 are [F] (compliance §1) | regulatory map | accurate |
| 2 | REG-002 "ER mechanics [K]" (compliance §1) | REG-002 verification note | accurate (mechanics only) |
| 3 | REG-020 Notice 2006-109 UNVERIFIED | REG-020 note | accurate |
| 4 | REG-042/043 "[I]" | map labels [F]/[S] | inaccurate |
| 5 | REG-057 "[S]" | map [K][S] | accurate (partial) |
| 6 | Class 6: 11 [K] rows | 9 listed; REG-025 double-classed | inaccurate |
| 7 | TVC-003: REG-001 says "sponsor-signed approval on every grant … cannot be vested in software" | REG-001 row | accurate quote; wrongly treated as verified law (A1) |
| 8 | §4966(d)(2) exclusive legal control [V via REG-001] (ontology, FI §1) | REG-001 row | unsupported; wording is §170(f)(18), REG-008 |
| 9 | TVC-006 REG-036 qualifier vs DD-005/CTL-008 | REG-036 [R]; DECISION-LOG; controls.csv | quotes accurate; severity overstated |
| 10 | TVC-016 "10-year default driven by OFAC [S]" | REG-026 [K]; REG-037 [F] | inaccurate label |
| 11 | Retention basis "unverified" for all classes | REG-037 [F] 10 years | inaccurate for R-OFAC |
| 12 | Nacha R10 60-day window [V] (compliance §1) | nacha.org summary pages (not opened here) | label overstated; wording possibly off [unverified] |
| 13 | TVF-002 "ACH credits can return after settlement; Nacha [V]" | same Nacha source (debits) | unsupported |
| 14 | TVC-021/TVF-005: no cancel after approval in WF-01 | WF-01 diagram `Approved→Canceled` | inaccurate |
| 15 | WF-01 2-minute wait then proceed (TVC-007) | wf-contributions l.68 | accurate |
| 16 | WF-01 units on `ContributionSettled`; acknowledgment from settlement (TVC-023) | wf-contributions l.48–49 | accurate |
| 17 | WF-05 "earmark units" (TVC-022) | wf-grants l.31 | accurate |
| 18 | WF-05 re-check eligibility only (TVC-033) | wf-grants l.26 ("eligibility and sanctions") | accurate in substance; paraphrase incomplete |
| 19 | DD-004 text (TVC-003) | DECISION-LOG l.10 | accurate |
| 20 | DD-014 Limen no WASM, PolyForm, one maintainer (TVC-002) | DECISION-LOG l.20 | accurate |
| 21 | TVC-015 "45 controls" / "coverage 100%" | control-framework l.3, l.31 | accurate quotes; "asserted" overstates a stated invariant |
| 22 | CTL-037 tests only current_law ∧ sponsor=yes (TVC-029) | continuous-compliance l.45 (controls.csv text broader) | accurate |
| 23 | controls.csv lacks retention/failure/independent/REG/status fields (TVF-040) | controls.csv header | accurate; ignores GOV-06 |
| 24 | TVC-027 SOC 1 quote | assurance-methodology l.28 | accurate |
| 25 | TVC-017 exec "December surge … sizes" | exec l.198 | accurate |
| 26 | TVC-017 tech-arch 10–30× vs twin ×3 | tech-arch l.20 (per-second) | inaccurate as a contradiction |
| 27 | TVC-024 / inventory: E9 assumes ACH dedupe | experiments l.32, l.194 | inaccurate |
| 28 | TVF-061 experiments that encode conclusions | adversarial-review l.92–122 | accurate but omits E10 |
| 29 | TVF-016 governance-architecture:108 | l.108 is SPOF note | inaccurate line |
| 30 | TVF-017 authority-boundaries:35 | donor-agent row at l.33 | accurate (±2 lines) |
| 31 | TVF-060 09 l.22 vs exec l.198 | both lines | accurate |
| 32 | g 6.2–13.0 [V] (economics) | 09 l.18 (computed from dataset) | label overstated ([R]) |
| 33 | $4.5–6k average grant [V per baseline] | b51-03 marks it [C] | label overstated |
| 34 | Economics "matches twin 34 days over SLA" | digital-twin; exec l.198 | unsupported (different metric; truncation) |
| 35 | E6 35→25 [X]; E4 ~15 days [X] | experiments l.123–147 | accurate |
| 36 | TVC-018 "~20 at any scale" | clarity-edf l.246 | accurate |
| 37 | TVC-025 TOTP allowed for routine; $25k step-up | identity l.61, l.72–73 | accurate |
| 38 | TVC-028 Controller A for C3.4/C4.1/C4.2/C4.3 | accountability-matrix.csv | accurate |
| 39 | TVF-041 C4.5 owned by CRCO | accountability-matrix.csv | accurate |
| 40 | FM-03 for cross-sponsor correlated error (alternatives §7) | failure-modes.csv FM-03 (agents) | inaccurate |
| 41 | FM-15 135 min | failure-modes.csv | accurate |
| 42 | TVC-032 / WG-2 deprovisioning unspecified | identity l.83, l.88; CTL-052 | partially inaccurate (already specified) |
| 43 | REG-019 reliance attaches to IRS sources only (ontology) | REG-019 (third-party allowed) | inaccurate |
| 44 | Charter "50 controls" | controls.csv 54 | inaccurate |
| 45 | Charter / inventory independence and saturation evidence | role-reviews.md, scenario-library.md, LEDGER.md | unsupported (files absent) |
| 46 | Contradiction-register severity totals | register rows | accurate |
| 47 | TVC-034 REG-007 cites REG-061 | map l.65 | accurate |
| 48 | Financial core invariants 7, 10; "event sourcing not required" | core spec l.13, l.16, l.62 | accurate |
