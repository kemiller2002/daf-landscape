# REV3 - Nonprofit data specialist review

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV3, perspective 2 of 5. Challenges P3-CHL-REV3010..REV3018. Same model family as the authors; not independent validation.

## Position

I work with IRS exempt-organization files, Pub 78, 990 e-file and the state registries. Report 11 is the strongest piece in the package: it reads the sources, separates shareable from segregated evidence, and cuts Phase II's inflated workload. My challenges are about four things:
- what the measurements can and cannot represent;
- a regulatory change the package missed;
- a misread competitor product;
- a sharing assumption that the new Unbound requirements now forbid.

## Challenges

**10. The headline registry cost ($124k, M5) uses a monitoring mode Unbound does not currently allow (high; fact, cross-repo).** Report 11 claims M5 "stays inside DEC-003 / CNV-GRT-003" (11:12, 11:96), and the model hard-codes `registry_mode,M5` (`data/model-inputs/settings.csv`). M3-M5 rely on automated 180-day renewal, under the RR-REQ-X-007-r2 item 1 reading (11:94). The Unbound Stage I requirement says the opposite: "Until the owner decides OD-CDD-02, the deep review MUST be performed as RR-REQ-X-007-r1 specifies; the reading under which a renewal ... counts as the deep review (RR-REQ-X-007-r2 item 1) is not adopted" (`unbound/requirements/discovery/2026-11-26-competitive-displacement-decisions/02-REQUIREMENTS.md`, UNB-CDD-CIV-008, lines 169-190; OD-CDD-02 in 04). The only compliant mode today is M1, at about $767k a year for 20k charities (11:92), or a reading not yet tested. Every capital figure that adds the registry (16:19, 16:25, 15:83-85) therefore assumes an unadopted control reduction. **Proposed change:** run the model with M1 as the governing case and M5 as conditional on OD-CDD-02, V-3 and V-9. State this in 11 §5 and in the key figures of 16.

**11. Cross-sponsor reuse of human verifications conflicts with UNB-CDD-CIV-010 and understates the marginal sponsor (high; cross-repo).** Report 11:49 treats "common verification built from public evidence (churches via public evidence, GEN-based subordinate rosters ...)" as shareable. The marginal sponsor cost of $3-24k depends on first-time verifications being done once for the union (11:157; 15:66-67). UNB-CDD-CIV-010 requires that "eligibility decisions, overrides, screening dispositions, match thresholds, identity confirmations and private submissions MUST live in the sponsor's cell". CNV-GRT-003 allows cross-sponsor evidence only "as input". Rev. Proc. 2018-32 §6.03 gives no reliance for group subordinates, and no IRS listing exists for churches. So for exactly the ~11% of rows that need a person (10:185), each sponsor must make its own determination. The human minutes for P3-EV-HI001 then scale with sponsors, not with the union. **Proposed change:** in 11 §8 and `registry-components.csv`, move first-time verification of non-listed recipients to the sponsor-specific layer (per sponsor, per recipient), and recompute the marginal sponsor cost.

**12. Rev. Proc. 2026-8 (group exemptions) is missing, and it lands inside the plan horizon (medium; factual omission).** Report 11 builds tier 2 on GEN-based subordinate rosters and the central organisation's status (11:66, 11:98; P3-EV-HI012; 237,380 c3 subordinates absent from Pub 78, 10:107). Rev. Proc. 2026-8 changes the group-exemption programme (https://www.irs.gov/pub/irs-drop/rp-26-08.pdf, accessed 2026-11-26):
- one group exemption letter per central organisation;
- a minimum of one subordinate;
- tighter affiliation and supervision rules;
- all subordinates under one 501(c) paragraph.

Its transition period for preexisting letters ends on **22 January 2027** (section 12.02(2)). Expect a wave of GEN consolidations, subordinate removals and new individual applications in 2027. That is the opposite of the low change rate assumed for tier 2 (P3-GAP-HI004) and for identity disputes (0.3% a year, 11:139). No report or register cites Rev. Proc. 2026-8 (grep of `competitive-advantage-creation` and `competitive-displacement`, 2026-11-26). **Proposed change:** add a source row and a P3-GAP. Stress tier-2 refresh, identity-dispute and subordinate-roster rates for 2027 at several times the base.

**13. Candid's "Nonprofit Eligibility API" is misread as a DAF eligibility competitor (medium; fact).** Report 11:14 and 11:162 cite it as "real-time eligibility updates" from $5,000, evidence that Candid "already sells monitoring-style eligibility updates". Candid's own page describes it as "For donation platforms to enable Apple Pay ... Verify a nonprofit can receive mobile payment donations" (https://candid.org/explore-apis/, accessed 2026-11-26). The relevant comparator is Charity Check ($2,750), which advertises "state and federal regulation compliance" and "time-stamped documentation for auditing records". That strengthens 11's commercial conclusion, but it also undercuts the claim that state-registry coverage and audit-grade evidence are differentiators (11:34, 11:169). **Proposed change:** correct 11:14 and 11:162 and P3-SRC-HI003. Compare against Charity Check, and add state compliance to the "what Candid already offers" list.

**14. Measured rates come from Schedule I grants over $5,000, and that sample is biased (medium; judgment, data reality).** The 11.2% exception rate, 64-72% reuse, 3.1-4.0% first-time incidence and 1.7 revocations per 1,000 rows all come from the Unbound replay of 990 Schedule I (04:11, 10:96, 11:80). Schedule I lists only grants above $5,000, drawn from sponsors' filed returns, which become available as e-file XML one to two years after the grant year. DAF grant flows are dominated by small grants to congregations, schools, PTAs, chapters and local groups. Those are the recipients least likely to be on Pub 78, most likely to be subordinates or churches, and least likely to recur across sponsors. Report 04:11 notes the limit, but 10 and 11 use the rates as base values without adjustment. **Proposed change:** report the rates as a lower bound for exceptions and an upper bound for reuse. Add a sensitivity at 1.5-2× first-time incidence and 0.5× reuse, and get a sub-$5k sample only through V-4/V-6 partner data.

**15. Identity resolution is costed as a rare dispute, but it is a daily intake cost (medium; judgment).** Report 11 budgets 30 hours a year for identity disputes (11:139), and the closed picker "eliminates" charity discovery (10:53; E07). In practice the hard work is mapping donor free text ("St. Mary's", "the food bank") to an EIN and a payable entity:
- one EIN covers many units (universities, health systems, diocesan structures);
- one organisation holds many EINs;
- DBA names differ from the BMF legal name, and CNV-GRT-003 requires grants to the listed legal name;
- payee bank account names do not match.

UNB-CNET-005 counts about 9,200 genuinely ambiguous EINs and 31,600 revoked-but-listed. These cases surface at recommendation time, every time, not as yearly disputes. The closed picker either rejects them (pushing the work back to e-mail, the tension 10:163 itself lists) or queues them. **Proposed change:** add an intake-time identity-resolution event per grant recommendation, priced from the replay's unmatched-name rate, and stop classifying E07 as wholly eliminated.

**16. State registry data is treated as optional, but it is the input sponsor policies most often ask for (medium; judgment).** Report 11:34 classifies state AG registries as "mostly no" for monitoring and defers them (SPD-GRT-005). Many sponsor grant policies, and Candid's Charity Check, treat "not in good standing" or delinquency as a hold reason. California is a per-organisation lookup (11:34), and New York requires FOIL. A partner's sponsors will ask for this on day one. Its cost (per-state scraping, terms-of-use review, licence uncertainty CHL-055) is outside the $124k. **Proposed change:** add a priced optional line for state-registry checks for the top 5-10 states (connector, terms review, human follow-up), or state explicitly that sponsors must buy it from Candid. That last option weakens the "shared intelligence" cost advantage (EK006).

**17. "IRS overwrites history" is offered as a reason to archive, but the cost advantage then depends on an archive Echelon has not started (low; judgment).** Report 11:22 and 11:175 recommend archiving monthly releases now, at zero cost. Until that is done, the bitemporal "what a grantor could rely on" evidence (11:169) exists only from the archive's start date. NCCS archives (SRC-068) are irregular and are not a reliance-grade provenance chain. **Proposed change:** state that replay-grade reliance evidence starts at the archive start date, and that historical replay before it uses third-party archives of uncertain completeness.

**18. Data rights for redistribution are asserted from page readings, while the model's sharing economics depend on them (low; legal assumption).** Report 11:22-41 gives licence readings (17 USC 105 for IRS data, OGL v3, ODbL, CC BY-NC-ND) and correctly labels them as research, not advice (11:3). The marginal-sponsor economics, and the option to publish the public layer (UNB-CNET-024), still rely on them. Two details matter:
- the SAM.gov D&B field restriction (11:32) is a live contractual restriction on a public extract;
- FAC terms are marked "to review" (11:33).

**Proposed change:** keep the shared layer to IRS, OFAC and CSL only until counsel confirms the others, as UNB-CDD-CIV-005's open question already requires.

## Verdict

Report 11's direction is right: monitoring plus targeted refresh beats periodic manual review, and the materiality table is the real lever. Its cost headline, however, assumes a renewal reading that Unbound's own new requirement refuses for now. It understates per-sponsor human determinations, misses Rev. Proc. 2026-8, and mis-scopes Candid. Fix those before the registry run is used in any capital figure.
