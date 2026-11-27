# REV3 - Compliance specialist review

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV3, perspective 3 of 5. Challenges P3-CHL-REV3019..REV3027. Nothing here is legal advice. Where I say "fact", I cite the public source checked on 2026-11-26. Same model family as the authors; not independent validation.

## Position

The package labels most legal readings as research pointers (10:3, 08:3, 11:3). That is good practice. The problem is narrower and more serious. Several obligations that **Unbound's own ratified or proposed requirements already impose** are costed in the economics as contingencies, stresses or deferrals. Two control reductions that the owner has not authorized are built into the base case.

## Challenges

**19. The Nacha TPSP role and its annual Rules compliance audit are treated as contingent, but Unbound's ratified text makes them mandatory (high; fact, unfunded obligation).**
- Ratified Unbound text: CNV-PAY-001 says the sponsor is Originator and Unbound is a Third-Party Service Provider, and "Unbound SHALL accept TPSP obligations by contract, including Nacha risk-based fraud monitoring ... security and audit cooperation" (`unbound/requirements/DEFERRED-PAYMENTS-AND-REMAINING-GAPS.md:129`). The Stage I README repeats it: "CNV-PAY-001 names the sponsor as Originator and Unbound as a TPSP" (`.../2026-11-26-competitive-displacement-decisions/README.md:46`).
- Nacha's rule: under Article One, Subsection 1.2.2, a TPSP must complete an annual audit of its compliance with the Rules by 31 December, for the ACH functions it performs (https://nacha.org/rules/ach-rules-compliance-audit-requirements; https://nacha.org/content/third-parties-ach-network; both accessed 2026-11-26).
- How the package treats it:
  - 02:176 makes the TPSP finding conditional ("Counsel finds the vendor is a Nacha TPSP ...: add $70-170k");
  - 03:51 keeps it "if the vendor creates ACH files";
  - 11:142 assigns it "to the payments platform";
  - P3-ASM-AB013 places it only in the high case;
  - 19:10 and the extremes table make "Nacha TPSP audit and SOC 1 required" a stress scenario.

Whether Unbound performs ACH processing functions is a counsel question. But the product requirement already accepts the role, the obligations and the Phase 2 fraud-monitoring rule (effective 19 June 2026, practically 22 June; https://www.nacha.org/rules/risk-management-topics-fraud-monitoring-phase-2). The base case must carry them. **Proposed change:** move the TPSP audit and the fraud-monitoring operating cost into the base recurring compliance line. Record an evidence gap for counsel to confirm the functions performed, not whether the role exists.

**20. The base registry case assumes a 180-day control reading that the owner has not adopted (high; removal of a mandatory control).**
- The owner brief says approval "does NOT authorize ... removal of mandatory controls" and preserves the 180-day validity.
- Ratified CNV-GRT-003 requires a deep review at 180 days. UNB-CDD-CIV-008 requires that it be performed "as RR-REQ-X-007-r1 specifies" until OD-CDD-02 is decided.
- Report 10:9 nevertheless states "The renewal still happens every 180 days; a machine performs it". Report 11:12 says M5 "stays inside DEC-003 / CNV-GRT-003", and the model defaults to M5.

Replacing a comprehensive human review with machine renewal is the substitution OD-CDD-02 asks the owner, counsel and sponsor compliance to approve. It cannot be assumed in the base case. **Proposed change:** relabel M3-M5 as "conditional on OD-CDD-02". Make M1 the base for compliance-bound figures. Remove "within CNV-GRT-003" from 11:12.

**21. SOC 1/SOC 2 "at the term sheet" conflicts with CNV-GOV-001 "from inception" and understates time to reliance (high; judgment, cross-repo).**
- 02:96 and 02:127 classify SOC 2 before a partner as "premature compliance". 16:244 binds SOC 2 at the term sheet.
- CNV-GOV-001 requires evidence engineering for SOC 1 (AT-C 320) and SOC 2 readiness "from inception". It also requires a written auditor planned approach before live reliance (`unbound/requirements/governance/SPONSOR-AUTHORITY-AND-AUTONOMOUS-OPERATIONS.md:81`).
- A Type 2 report needs an observation period of operating controls, which in practice runs several months (02:127 uses at least 3 months).
- echelon-assurance has "no control above Designed" (09:33).

So the term-sheet trigger starts a 6-15 month path (readiness, then Type 1, then observation, then Type 2), not a purchase. A partner's TPRM will not let a sponsor go live in the meantime. Report 14 models first revenue 7 months after signing. **Proposed change:** cost evidence engineering from inception, as CNV-GOV-001 requires. Add the Type 2 observation lag to the go-live distribution (P3-ASM-AB026) rather than to procurement prose only.

**22. Segregation of duties cannot be evidenced by a one-founder operator (high; unfunded obligation).** CNV-PLT-010 requires two approvers, neither the author, and two-person break-glass access. A SOC 2 CC (change management and logical access) or SOC 1 ICFR auditor will test that these controls operated. The lean run's maintenance line (P3-ASM-AB010) and "partial" second maintainer cannot evidence it. Neither can the claim that "December capacity ... not in licensing" (02:131). This is a mandatory control without a funded operator, not a conventional-organization artefact. **Proposed change:** cost a minimum control-operating team (at least three people with distinct roles available year-round) in the base case, and say plainly that the lean run is not SOC-compliant as modelled.

**23. Supporting-organization certification is attributed to 4966(d)(4), which only defines the category (medium; fact).** Report 10:145 cites "Section 4966(d)(4)" for "Supporting-organisation donor-control certification" and classifies it as transferred to the customer. Section 4966(d)(4) defines a "disqualified supporting organization" (any Type III that is not functionally integrated, and Type I/II controlled by the donor or advisor). Section 4966(c)(2)(A) excludes such organizations from the public-charity safe harbour, and (c)(1)(B)(ii) imposes expenditure responsibility under 4945(h). The statute does not itself require a donor certification (https://www.law.cornell.edu/uscode/text/26/4966, accessed 2026-11-26). Certification is an industry practice drawn from IRS notices and the proposed regulations, which remain proposed (05:208). The duty and the liability stay with the sponsor, so "transferred-to-customer" overstates what moves. **Proposed change:** cite 4966(c)(2)(A) and (d)(4) as defining the risk, with certification as a sponsor-chosen procedure. Classify the step as mandatory sponsor work, partly prepared by the advisor.

**24. The DAF acknowledgment rule is cited as 170(f)(8) only (low; fact).** Report 10:144 lists "Contemporaneous written acknowledgment, Section 170(f)(8)" as mandatory content, automated. DAF contributions also require the 170(f)(18) statement that the sponsor has exclusive legal control. Courts have applied strict compliance and denied a deduction where the letter omitted it (Keefer, N.D. Tex.; https://cof.org/content/substantiating-contributions-donor-advised-funds, accessed 2026-11-26). Unbound's own requirements cover 170(f)(18) (`requirements/discovery/2026-11-24-simplification-economics/01-REVERSE-REQUIREMENTS-ANALYSIS.md:705`). **Proposed change:** cite 170(f)(8) and 170(f)(18). Add template-assurance (legal review of every sponsor's acknowledgment template) as a mandatory, non-eliminable control.

**25. State charitable registration and fundraiser-status exposure of the partner and of Echelon are unanalysed (medium; legal assumption treated as fact).**
- Report 05:212 states that in hosted programmes "the sponsor carries the 4966/4967 responsibility, and the institution's role is marketing". 06 recommends white-label and host-sponsor programme factories (P3-DEC-CD001).
- Marketing a charity's DAF programme for compensation, or a revenue share tied to contributions, can create professional-fundraiser, fundraising-counsel or commercial-coventurer registration and contract-filing duties in several states for the partner, the institution or the vendor, depending on the facts.
- 11:34 defers state registration as sponsor discretion, and 04:60 mentions state solicitation only for counsel.

No report tests whether the revenue models in 12 (shares of 20-40%) create such status. **Proposed change:** add an evidence gap and a counsel question covering per-state fundraiser and coventurer status of partner, host and Echelon under each channel model. Exclude contribution-linked shares until it is answered.

**26. Record retention, privacy and unclaimed-property obligations are absent from the cost model (medium; omission).** The event catalogue (10 §2, §4) has no events for:
- retention and legal-hold management;
- breach notification;
- privacy requests (state privacy laws that reach nonprofits, and processor duties of the vendor);
- uncashed grant checks and escheat of stale items.

Unbound's administration requirements recognize dormancy and escheat (ADM-024; `unbound/requirements/administration/DAF-ADMINISTRATION-AND-SPONSOR-OPERATIONS.md:34`), and the check fallback is mandatory under CNV-PAY-001. Each obligation is small per account, but none is eliminable, and some fall on the vendor as processor. **Proposed change:** add mandatory events P3-EV for retention and legal hold, privacy requests, breach response and escheat, with owner (sponsor or vendor) and cost.

**27. "Identity proofing ($3 per account)" and the KYC posture are not grounded in any rule (low; legal assumption).** Report 10:13 and 10:183 treat identity proofing as a mandatory floor. A charitable sponsor is not a bank subject to CIP. The real drivers are OFAC strict liability, sponsor fraud policy and, for any partner bank or trust distributor, that institution's own KYC applied through TPRM (SEG-003 lists BSA/OFAC via the sponsor). The cost could be far higher for bank-distributed programmes, or lower for community foundations. **Proposed change:** state the legal basis per channel, and make identity proofing a channel-dependent parameter rather than a universal $3.

## Verdict

The package does not invent legal conclusions, but it prices obligations as if the friendliest reading were already settled. Two of them are not open readings at all: the TPSP role and the 180-day deep review are governed by Unbound text today. Correcting them moves the lean run up materially, by roughly the $70-170k a year the package itself attaches to TPSP plus SOC 1 (02:176), plus the M1-versus-M5 difference. The S3 base therefore comes nearer the payback edge that report 19 says it does not reach.
