# 00 - Executive summary: charity networks and frictionless onboarding

Status: research draft (2026-11-26). Not legal advice, independent assurance or regulatory certification. Evidence classes per 01-research-methodology.md. Requirements derived from this research are **proposed** in `kemiller2002/unbound` under `requirements/discovery/2026-11-26-charity-network-and-onboarding/`. None is implemented or validated.

## The answer in five sentences

1. **The charity directory is not a moat.** Every incumbent's US coverage rests on the same free IRS files: 1,984,891 EINs in the EO BMF and 1,437,288 in Pub 78. Unbound can reproduce identity, status and monitoring for about **$316k a year** of run cost. Its decisions can also be more provenance-bound and replayable than anything competitors document.
2. **The incumbent asset that is hard to copy is accumulated history:** payee enrolments, resolution of messy recipients, charity familiarity and audit-accepted decisions. It grows only with time, charity convenience and partner rails, and reaching two thirds of grants paid electronically takes roughly **2-5 years** at realistic conversion rates.
3. **Onboarding is unavoidable for the ratified entry segment and is the largest variable cost.** History import is 46-58% of onboarding cost at 100k+ accounts, and data quality swings the total 2.5-6.2x. Incumbents sell migration but publish no outcomes. Unbound can make it a deterministic, rehearsed, reconciliation-gated capability and compete on published, verifiable results and better exit terms.
4. **Neither barrier appears to be why sponsors choose or stay with a provider.** The independent adversarial review found that **distribution and incentive alignment** explain observed behaviour better: white-label sponsor entities, adviser and investment-manager revenue, and fee carve-outs. Only 1 of 26 national, faith and affinity sponsors left Ren's iPhi platform in 2023-2026, and none left for a new entrant. Neutralising these barriers is necessary but not sufficient.
5. **The economics work for added sponsors and do not work for the first one.** At the 20 bps working price, a 10k-account added sponsor pays back onboarding in about **3.4 months**. The first one to three sponsors need design-partner terms. 20 bps is a price *increase* against incumbents that take 18.5 bps for staffed administration, and Ren's roughly **$81 per account** software price is not beatable at any modelled size.

## Major findings

| # | Finding | Evidence |
|---|---|---|
| 1 | Ren's directory comes largely from IRS public data. The hypothesis is **supported for the directory and claim layer**: all claim routes key off IRS data, and Ren says it replaced GuideStar with its own IRS listing. It is **unresolved for vetting**: RCF's 2023 policy names GuideStar Charity Check as its "cornerstone" | INFERENCE, Medium-High (02) |
| 2 | Ren's four headline numbers measure four different things: 1.8M+ directory reach, 140k+ annual recipients, 93k Giving Compass scope, 25+ ACH programmes. No count of claimed profiles or verified bank accounts is published | VENDOR-CLAIM (02) |
| 3 | The real network is **reusable verified destinations**. Only Chariot and PayPal Grant Payments offer one to third-party grantmakers. Chariot verifies officer identity and opens a charity-titled account at Column N.A.; recipients cannot bring their own bank account | Vendor docs, VERIFIED-FACT for terms (03, 07) |
| 4 | Incumbents' moat is **annual recipients actually paid**: Fidelity about 227,000 (67% by EFT), DAFgiving360 about 141,000-170,000 (Low confidence), Vanguard 66,785, NPT more than 41,000, RCF more than 40,000 | Self-reports as VENDOR-CLAIM; Form 990 counts VERIFIED (03) |
| 5 | No single IRS file establishes current eligibility. All 237,380 group subordinates are absent from Pub 78 and excluded from reliance (Rev. Proc. 2018-32 §6.03). About 31,600 EINs are still listed after an unreinstated revocation; about 71% look re-recognised. Revocations post a median 88 days late, which is an August-batch artefact | VERIFIED-FACT, computed (04, 05, 06) |
| 6 | Material change is rare: one month showed 236,750 c3 changes, of which 405 were eligibility-relevant and about 90 adverse. Change-driven vetting can keep the 180-day maximum while cutting human review to about 5 per 1,000 grants (central estimate) | VERIFIED-FACT counts; INFERENCE rate, Low-Medium (06) |
| 7 | Actual losses come from **bank-detail substitution after account takeover**, not fake charities. Nacha's 2026 rules make False Pretenses monitoring, including misrepresented account ownership, a TPSP obligation | VERIFIED-FACT (09) |
| 8 | Ratified round-2 amendments already cover most destination controls: 30-day-aged callback contacts, CAL3 for charity submitters, charity contact holds and partner-contract equivalence. The remaining gap is a third evidence class for partner-bank accounts (OD-CNO-02) | Repo clauses (09, 22) |
| 9 | Grant-triggered enrolment is **parity**: Ren codes on checks, AEF QR codes and Chariot's 5-day claim window. Conversion per invitation, not partner pre-enrolment, dominates growth | VERIFIED-FACT; model INFERENCE (08) |
| 10 | Vendor launch times cover new programmes only: Ren 90-120 days and about $50k, NPT 14-16 weeks. Real conversions take 3-6 months at community foundations and about 8.5 months for AEF. They freeze operations (4 days to 5.5 weeks), force re-registration, and carry 2-26 years of history | Case studies, Form 990s (10) |
| 11 | Industries that made switching routine used a **standard, a guarantee and a clock** backed by regulation: ACATS and CASS. DAFs have no such compulsion, so Unbound can promise only what it controls. The costliest failures (TSB, Revlon) were governance and testing failures, not data-copy failures | VERIFIED-FACT (11) |
| 12 | Imported history can coexist with append-only records through a non-posting legacy partition, an opening-balance epoch and per-fund roll-forward proofs, with gaps disclosed and never plugged | RECOMMENDATION, High (14, 16) |

## Competitive assumptions: confirmed or disproven

| Assumption | Verdict |
|---|---|
| Ren's directory is mostly IRS public data plus submissions and enrichment | **Supported** for the directory and claim layer; **open** for the vetting source (test in 02 §2) |
| A large directory is a competitive advantage | **Disproven**: commoditised |
| A proprietary charity payment network is needed | **Disproven** for Unbound: CNV-LEG-001 bars holding funds, and partner rails plus sponsor ACH suffice |
| Supporting ACH implies a reusable charity network | **Disproven**: only partner-account rails offer reusable destinations, and pass-through intermediaries change the legal payee |
| Shared vetting can neutralise network advantages | **Partly**: for public facts. It is parity, not advantage. Sharing bank evidence across sponsors is low-benefit and carries correlated risk, so it is deferred |
| Onboarding friction is a key reason sponsors stay | **Not supported** by public evidence; distribution and incentives fit better (unproven either way) |
| Onboarding can be productised and predictably priced | **Supported** inside a data-quality gate, for added sponsors |
| The 20 bps servicing price | **Plausible only as staffed outsourcing**; it is a price increase against 18.5 bps incumbents |

## Remaining incumbent advantages

Listed in 23 §10 and maintained as requirement UNB-ONB-033:

1. distribution and incentive alignment;
2. sponsor-of-record control over vendor-charity programmes;
3. platform relationships;
4. accumulated payee enrolments;
5. audit history and SOC reports;
6. price at the software tier;
7. brand.

## Proposed Unbound advantages (hypotheses to validate)

- **Provenance-bound, replayable eligibility decisions** with three time axes and per-predicate source authority. No competitor documents this.
- **Correctness under change:**
  - conflict states, not guesses;
  - subordinate roster evidence;
  - reinstatement semantics;
  - informational changes never blocking payment.
- **Charity convenience:** a charity never has to become a software user to be paid, and is never forced into a partner account.
- **Partner-neutral rails** with sponsor-held destination evidence and contractual exit terms.
- **Migration as a product:**
  - pre-contract assessment that never takes personal data out of the sponsor;
  - deterministic, rehearsed runs;
  - exact reconciliation with no plugs;
  - published outcomes: history depth, freeze length, login and enrolment carry-over, verified payee share;
  - better exit terms.
- **Declarative sponsor configuration with machine-checked legal-perimeter validation.** Comparable tools elsewhere check syntax and diffs, not funds-flow or role rules.

## Economic implications (C0 no-lever base, 20 rev 3)

- **Registry:** about $316k a year to run ($107k-673k): $5.42 per grant at 70k grants and $0.54 at 700k. Treat it as a cost of doing business.
- **Electronic payments:** savings are about $0 per sponsor at realistic coverage (about 8%) and conversion (p=0.10). The network defends against switching; it is not a margin lever.
- **Added sponsor, 10k accounts at 20 bps:** onboarding payback about 3.4 months (P10-P90 3.9-6.6).
- **First sponsor:** about $63k a year net against about $3.04M of platform fixed cost, so it does not pay back at P50.
- **Small sponsors (1k accounts):** need a minimum fee of about $220k.
- **Uneconomic:** processor-like books at any 10-30 bps fee, and any size at $81 per account.
- **Buyer switching cost:** $170k-$846k base, borne by the sponsor.
- **Model limits:** CNV-ECO-003 conformance is partial. Economic claims stay barred until a 12-month real-sponsor replay and a 90-day time study exist.

## Requirements added (proposed, in unbound)

- **26 UNB-CNET records:** charity network.
- **33 UNB-ONB records:** onboarding.
- **13 owner decisions:** OD-CNO-01..13.
- **14 requirement questions.**

The decisions and questions are registered in the authoritative open-question register: 343 questions total, 27 new and open. Every record refines named existing requirements or clauses and cites this package. No existing requirement or ratified clause was modified. Conflicts are escalated, not resolved. Trace tables: `01-TRACEABILITY.md` in the Unbound package.

## Architectural dependencies

- **Unbound-owned components on managed PostgreSQL (CNV-ARC-001, CNV-ARC-004):**
  - the temporal claim store;
  - append-only history and the legacy partition;
  - the migration pipeline;
  - the integration certification runner and readiness portal;
  - provider contracts and mocks.
- **What Echelon does and does not supply:**
  - Strata provides schema governance only. It does not provide append-only history or temporal queries, and its mock-interaction virtualization (STRATA-DIV-001) is proposed, not implemented.
  - Forma and Folio supply UI patterns and document rendering.
  - Dokimos supplies acceptance evidence.
  - Fides supports only GitHub as an identity provider, so it does not fit donors or sponsors.
  - Vigila is an untagged pilot.
- **Outside dependencies:**
  - one or more partner rails (Chariot first) under contract minimums;
  - two owner-match vendors;
  - the sponsor's ODFI.

## Outstanding owner decisions

Starred items in 24:

- **OD-CNO-01:** migration before the first institutional customer.
- **OD-CNO-02:** a third destination-evidence class.
- **OD-CNO-05:** cross-sponsor signals.
- **OD-CNO-07:** CNV-EXP-002 scope and "full history".
- **OD-CNO-10:** onboarding commercial model.

Counsel items: OD-CNO-11, -12 and -13.

## Evidence gaps that matter most

- **E1:** win/loss evidence.
- **E2:** real network counts.
- **E4:** a real incumbent export.
- **E12:** measured enrolment conversion.
- **E13:** migration exception rates.
- **E14:** auditor acceptance of the epoch design.

## Recommended next steps

1. Owner rulings on OD-CNO-01, -02 and -07. They decide Release 1 scope.
2. Run **win/loss interviews** with 5-10 sponsors that moved or evaluated vendors, to test the distribution hypothesis before investing further in either track.
3. Obtain **one authorised incumbent export** from a prospective sponsor under NDA and run the T1/T2 assessment end to end.
4. Build the **public-data replay harness**: 12 archived IRS releases plus OFAC history against real Schedule I recipients. It validates targets A-1 to A-6 and G-1/G-3 with no customer.
5. Open **partner contract discussions** with Chariot on the UNB-CNET-018 minimums and the evidence-class question.
6. Decide the **distribution and incentive answer** (23 §10): neutrality positioning for advisor-distributed sponsors, or a sponsor-entity partnership.

## Where things are

- **Research:** this folder.
  - Files 01-25.
  - `data/`: registers, models and adversarial findings.
  - `scripts/`: reproducible stdlib Python. Run `economic_model.py --check` and `merge_source_register.py --check`.
- **Requirements:** `unbound: requirements/discovery/2026-11-26-charity-network-and-onboarding/`. Validate with `python3 -I -B tools/reqaudit/validate_charity_onboarding.py . --check --research-root ../daf-landscape`.
