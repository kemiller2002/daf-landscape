# REV3 - Professional services operator review

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV3, perspective 5 of 5. Challenges P3-CHL-REV3037..REV3044. Written in the voice of a fund-accounting and DAF conversion firm. Same model family as the authors.

## Position

We do conversions and implementations for community foundations and DAF sponsors. In the package, implementation is a one-time line of $35-150k for the first customer and $10-80k after that (P3-ASM-AB020; 02:76; 02:47-48). Onboarding is "configuration" and Transitus does the migration. In our experience, conversions are where these projects fail, and the people who do the work are the sponsor's staff and firms like ours. The package leaves both out of the cost.

## Challenges

**37. First-customer implementation of $35-150k assumes a migration tool that does not exist and is scoped not to cover the source system (high; judgment, cross-repo).**
- The basis for P3-ASM-AB020 is "Transitus phase 1 + partner first line".
- Transitus is at phase 0, with 171 proposed requirements and no production code (09:36; `transitus/requirements/REQUIREMENTS.md:37`).
- Phase 1 is limited to target-side and public-specification packages (IRS BMF, Nacha returns, one bank, Schwab, the Unbound canonical import) and only needs to be demonstrated "at least theoretically" (TRN-REQ-MP-006, MP-009; REQUIREMENTS.md:167, 170).
- Vendor-specific packages for the incumbent the customer is leaving (Ren/iPhi, FIMS lineage, Foundant, Blackbaud) are phase 3, gated by T3 and customer-authorized samples (TRN-REQ-ARC-009, MP-010).

So the first conversion is hand-mapped from an incumbent export. That means profiling, mapping, cleansing, opening-balance tie-out, historical grants and contributions, donor and advisor records, recurring grants, in-flight items and year-to-date tax receipts, with Transitus doing at most canonical loading. Phase II's own range was $35-325k (02:76; PR #86). The package keeps the low end and drops the upper half. **Proposed change:** use $75k / $150k / $325k for the first conversion, and state that Transitus phase 1 does not cover the source side.

**38. S6 "reusable onboarding packages" ($10-80k per customer) cannot exist under Transitus's own promotion rules until several customers of the same incumbent have converted (high; cross-repo).** TRN-REQ-MP-005 forbids promoting improvements from customer overlays into base packages without at least two independent customer samples and a vendor-licence review (REQUIREMENTS.md:166). TRN-REQ-MP-007 retires a vendor package if reuse stays low after three migrations (REQUIREMENTS.md:168). TRN-REQ-MP-002 requires a licence and contract clearance for anything derived from a vendor export. Yet the model charges later customers at the S6 rate from the second customer onward (P3-CLM-MOD005; sequence-values impl_later $10k / $30k / $80k). DEC-007 concentration helps only if the first 3-5 customers all leave the same incumbent, and V-5 has not been run. **Proposed change:** charge the first three customers per incumbent cluster at the first-customer rate, and make S6 conditional on a recorded selection (UNB-CDD-ONB-002) and two converted samples.

**39. A single rehearsal and a 2-4 month implementation are not a conversion plan (high; judgment).**
- Report 06:64 gives S1 implementation as 2-4 months. The go-live lag is 3-9 months (P3-ASM-AB026). Unbound requires "at least one migration rehearsal" (`unbound/requirements/discovery/2026-11-26-transitus-integration/02-REQUIREMENTS.md:208`).
- Conversions of fund ledgers with history normally need two or three mock conversions, each followed by a full reconciliation to the cent, then a parallel period through at least one month-end. Report 06:69 notes the cost of parallel running for pilots.
- Cutovers avoid November-January (year-end giving) and the sponsor's audit fieldwork, which removes about four months a year from the calendar.
- V-4 (a real export) has not been run, and OD-M-14 records that no design partner exists (04:20).

DEC-010 rightly forbids process SLAs before rehearsals. The economics nevertheless assume a schedule that only a successful rehearsal could justify. **Proposed change:** model 2-3 rehearsals plus a parallel month, a calendar blackout window, and a go-live lag of 6-12 months for the first customer.

**40. The sponsor's own conversion labour is transferred work, and it is not counted anywhere (high; transferred versus eliminated).** Report 10 is careful to report transfers to customers and partners as costs (10:34-35, 10:86-88). Its event model covers operating events only (E24 migration at 9,000 minutes plus 2 per account, 10:70). During a conversion, the sponsor's finance and operations staff:
- validate mapped funds;
- resolve historical breaks;
- re-key what cannot be exported;
- re-paper fund agreements and policies;
- re-train advisors and donors;
- sign off reconciliations.

For a mid-size sponsor this is commonly hundreds to over a thousand staff hours, and it is the main reason stayers stay (CLM-017, CHL-096). It does not appear in the system-cost comparison that is meant to be "the test" (10:178). **Proposed change:** add a one-time sponsor conversion labour line (low / base / high hours) to the system-cost view. Run V-1 stayer interviews on it.

**41. "Partner first line, Echelon second line" leaves nobody owning implementation delivery (medium; judgment).** 02:77 and 03:67-68 put project management and first line with the partner and second line with Echelon. In practice somebody must own the conversion plan, the data-quality issue log, cutover go/no-go and hypercare. Under the lean run that is the founder: implementation cash of $75k buys contractors, not a delivery lead. 14:270 already notes that the platform sequences consume "essentially all founder months over ten years". Each concurrent implementation competes with selling and engineering for the same founder. The model's 3 customers a year (P3-ASM-AB030) imply 1-2 concurrent conversions at all times. **Proposed change:** add a delivery-capacity constraint (founder hours per conversion; a maximum of one concurrent conversion without a hired delivery lead) to the sequences engine.

**42. Hypercare and post-go-live support are missing (medium; omission).** The first 60-90 days after go-live bring heavy support (statement queries, grant-release exceptions, reconciliation questions, advisor access). In the lean run, support is $0-100k a year, flat (P3-ASM-AB015). Nothing scales with customers going live, apart from a revenue-share variable cost that the partner carries for first line. **Proposed change:** add a per-go-live hypercare cost (for example 150-400 hours) paid by Echelon or the partner, and say which.

**43. Programme configuration for hosted programmes ($5-12k) assumes templates that need policy, legal and donor-communication work every time (medium; judgment).** Report 05:93 and 05:124 put hosted-programme fixed cost at $5-15k a year and onboarding at 10-25% of $48k (P3-ASM-CD007). Each new institutional programme needs:
- a programme agreement between host and institution;
- host-share rules;
- fee schedules;
- a gift-acceptance and grant policy overlay;
- donor-facing documents with the 170(f)(18) wording;
- branding;
- advisor onboarding;
- a sponsor board approval.

Most of that is legal, governance and communications work, not configuration. **Proposed change:** split programme onboarding into configuration (templatable) and governance and legal (per programme, borne by host or institution), and price the second part from host-sponsor practice, or flag it as unknown.

**44. Who does the work: the AI-native and agent-assisted labour assumption extends to delivery without evidence (medium; circular).** The lean labour figures, including E24 migration halved by "reproducible migration" (10:70) and implementation at S6, are justified by the same unmeasured agent-productivity premise that underlies the build (P3-ASM-AB002, EK020 "unproven", 07:88). V-7, the only test of AI handling time, is allowed to run on synthetic data as a "design check" (04:15). **Proposed change:** treat agent-assisted delivery savings as zero until V-7 runs on a real conversion, and show the effect on A3 peak cash.

## Verdict

The package treats migration as Unbound's differentiator (EK010) and its cost as a small one-time line. Both cannot hold. A differentiating conversion capability is expensive to build, slow to make reusable, and paid for largely by the sponsor's own staff. Until V-4 runs, every implementation figure here should be read as the vendor-side cash floor, not the cost of the conversion.
