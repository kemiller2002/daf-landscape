# 21 - Competitive performance targets

Status: research draft (2026-11-26). Not legal advice. Evidence classes per 01-research-methodology.md.

Every target below is a **HYPOTHESIS** until validated. None is a commitment, service level or customer claim (CNV-ECO-003 bars customer-facing claims before evidence). Targets are set against what this package found incumbents publish. Where incumbents publish nothing, the target is set against what the evidence suggests is achievable.

## Summary

- **Correctness targets are gates.** Automation targets are subordinate to them.
  - No automation target counts in any period with a blocking reconciliation failure, a wrongful payment, or a missed adverse status change.
  - This prevents the failure mode the brief warns against: raising automation percentages at the expense of correctness.
- **Measure what customers can verify, not what vendors advertise.** The package found no vendor that publishes any of the following:
  - history depth carried over;
  - a reconciliation result;
  - how long participants are frozen out;
  - login and enrolment carry-over;
  - verified payee share.
  - These are therefore the targets with competitive value (10, 11, UNB-ONB-030).
- **Directory size is not a target.** Every incumbent rests on the same IRS files (02, 03, 04).
  - The charity-side targets are about *recipients actually paid*: resolution, payment readiness and correctness.
- **Each target names three measurement stages.**
  - (S) synthetic datasets;
  - (C) controlled simulation, including replay of archived IRS releases and real Schedule I recipient lists;
  - (P) eventual pilot sponsors.
  - Several targets can be measured at S/C now, with no customer.

## 1. Guardrails (must hold before any efficiency target is reported)

| ID | Guardrail | Target (hypothesis) | Measurement |
|---|---|---|---|
| G-1 | Wrongful-eligibility decisions: grants released to an organisation ineligible at release under the sponsor's policy | 0 known in any period; every case triggers a root-cause review | (C) replay of archived BMF/Pub 78/revocation releases against synthetic grants; (P) independent sample under UNB-XIN-CLM-005 |
| G-2 | Payments to an unverified or substituted destination | 0 released outside the CNV-PAY-002 combinations; diversion loss 0 | (C) red-team scenarios from data/charity-network-threat-model.csv; (P) incident log |
| G-3 | Adverse public status change missed | 100% of adverse changes in an ingested release evaluated before the next payment release | (C) fault injection with synthetic revocations, sanctions additions and subsection changes (06) |
| G-4 | Migration financial correctness | 0 unexplained differences at the blocking gates G01-G29; 0 plug entries | (S) synthetic legacy books with seeded errors; (C) mutation tests; (P) per-migration reconciliation report |
| G-5 | Duplicate external effects during transition | 0 duplicate grants, payments or acknowledgments | (C) cutover rehearsal with dual-system release attempts (17) |

## 2. Charity network targets

| ID | Metric | Hypothesis target | Basis | Measurement |
|---|---|---|---|---|
| A-1 | Authoritative freshness: lag from IRS file publication to Unbound release | ≤ 24 h for Pub 78, BMF and revocation; ≤ 6 h for OFAC | Candid reports roughly 20-minute polling (ADVA-15) and incumbents claim same-day revocation updates; matching them is parity | (C) ingestion logs against Last-Modified |
| A-2 | Coverage of recipients actually paid: share of a sponsor's trailing-12-month recipients, by count and by dollars, resolved to a canonical identity with recorded reliance basis | ≥ 99% of dollars; ≥ 97% of recipients | Ren-serviced Schedule I: up to about 7% of recipient EINs not in BMF (upper bound); 22,269 top-50 recipient EINs not in BMF in prior research | (C) replay of real FY2023 Schedule I lists (02, 08); (P) migrated grant history |
| A-3 | Identity-resolution accuracy on the hard cases | ≥ 99.5% precision on auto-resolved matches; 0 auto-merges of distinct EINs | After de-duplication, 235,926 c3 organisations share a normalised name with another and 317,386 share a street address (05, ADVA-04) | (S) data/identity-resolution-cases.csv extended to ≥ 1,000 labelled cases; (C) sample of real Schedule I recipients |
| A-4 | Routine vetting automation: share of 180-day renewals completed with no human touch | ≥ 95% | Material change is rare: about 405 eligibility-relevant changes in a month of 236,750 c3 changes (06) | (C) state-model replay over 12 monthly releases |
| A-5 | Human review rate | ≤ 5 cases per 1,000 grants; ≤ 2% of the review events a conventional 180-day cycle implies | 06 central scenario: about 5 per 1,000 grants and about 1.6% of a conventional cycle (Low-Medium confidence) | (C) replay; (P) case log by HumanInterventionClass |
| A-6 | False-hold rate: holds later cleared with no adverse finding | ≤ 0.5% of grants; median time to clear ≤ 1 business day | StatusConflict class of about 9,200 ambiguous EINs (04, 06) | (C) replay of conflict classes; (P) hold log |
| A-7 | Electronic payment share of grants (by count) at 12 / 36 months after go-live | 40% / 67% count; ≥ 85% of dollars at 12 months | Fidelity 67% EFT (VENDOR-CLAIM). 08 model: 67% takes 23-65 months at p=0.10 and 9-26 months at p=0.25 | (C) 08 growth model; (P) UNB-CNET-025 metering |
| A-8 | Invitation-to-enrolment conversion per grant-triggered invitation | ≥ 0.25 (planning value 0.10) | 08 calibration: real conversion about ≤ 0.10 | (P) only; cohort-tracked |
| A-9 | Charity steps to receive a first electronic grant / each later grant | ≤ 5-7 one-time / 0 per grant | 08 step counts. Partner deposit-account flows take about 8 one-time steps and 1-2 per grant | (S) usability test with charity staff |
| A-10 | Destination-fraud loss | 0; 100% of D1-D3 destinations under first-payment cap and probation | 09 threat model; c10 amendment | (C) red team; (P) incident log |

## 3. Onboarding targets

| ID | Metric | Hypothesis target | Basis | Measurement |
|---|---|---|---|---|
| B-1 | Time to production, from contract to first live grant (PlatformReplacement, in gate) | ≤ 16 weeks at 10k accounts (P50); ≤ 26 weeks P90 | Observed: community-foundation conversions 3-6 months; AEF about 8.5 months; vendor launch claims of 8-16 weeks are for new programmes only. 20 C0 model: 22-49 weeks | (C) rehearsal timings; (P) clock from usable extract (UNB-ONB-030) |
| B-2 | Sponsor configuration time: from completed questionnaire to a validated Sponsor Configuration Package | ≤ 10 business days | 12: the validation pipeline is automated; approvals bound the time | (S) synthetic sponsors |
| B-3 | Sponsor-specific code changes | 0 (release check enforced) | UNB-ONB-024 | (C) CI static check |
| B-4 | Migration automation: share of records reaching the canonical package with no manual intervention | ≥ 98% typical data; report the exception count by class E1-E8 | 15; no public benchmark | (S) synthetic legacy exports at clean/typical/poor quality |
| B-5 | History depth: share of predecessor-held history imported | 100% of what the predecessor holds and the sponsor may export; every shortfall disclosed | AEF: 33 months imported, 2 years visible; GWCF 7 years; Arizona 26 years | (P) completeness report |
| B-6 | Participant freeze | ≤ 3 business days with no lost recommendations; donor notice ≥ 30 days for longer freezes | Observed freezes 4 days to about 5.5 weeks | (C) rehearsal; (P) cutover log |
| B-7 | Login and delegation carry-over: share of active donors and advisors who regain access without re-registration | ≥ 90% via invitation plus proofing reuse; 100% of delegations carried as pending confirmations | All 6 observed donor notices forced re-registration or reset | (P) |
| B-8 | Verified payee share at cutover (by dollars) | ≥ 60% (sponsor-set minimum) | UNB-ONB-021; recipient concentration (08) | (C) bulk owner-match coverage test; (P) |
| B-9 | Customer employee effort per migration (10k accounts, typical data) | ≤ 0.5 FTE over the project and no external consultant | Evidence of ≥ 0.5 FTE plus $115k-724k a year in consultants at incumbents (10, 20) | (P) time logs |
| B-10 | Integration certification: share of certification tests automated | ≥ 75% fully automated (89-test catalogue currently 69 full, 13 partial, 7 manual) | data/integration-certification-suite.csv | (S) sandbox runs |
| B-11 | Onboarding cost per added 10k-account sponsor (Unbound side, in gate) | ≤ about $34 per account; payback ≤ 6 months at 20 bps | 20 C0: marginal payback 3.4 months (P10-P90 3.9-6.6) | (C) model; (P) metered actuals (CNV-ECO-001) |
| B-12 | Cost to serve: Unbound cost per grant including registry run cost | Report against $5.42 per grant at 70k grants and $0.54 at 700k (C0 base) | 20 rev 3 | (P) metering |

## 4. How targets are validated before any customer

1. **Synthetic legacy books.** Generate exports at three quality levels with seeded errors drawn from the exception classes. Measure B-4, G-4 and B-1 rehearsal durations. The synthetic operating year (`unbound: requirements/convergence/2026-11-24-master/16-SYNTHETIC-OPERATING-YEAR-AND-INTERNAL-TIME-STUDY.md`) supplies volumes.
2. **Public-data replay.** Replay 12 archived monthly IRS releases and the OFAC history against synthetic grant schedules built from real Schedule I recipient lists. Measure A-1 to A-6 and G-1/G-3. This also produces the shadow-replay evidence CNV-ECO-003 requires, though it does not replace the real-sponsor replay that clause mandates.
3. **Red-team scenarios.** Run the 22 threats in `data/charity-network-threat-model.csv` against the state model (G-2, A-10).
4. **Pilot sponsors.** Validate everything else, especially conversion (A-7, A-8), people effort (B-9) and auditor acceptance. CNV-ECO-003 requires a 12-month replay of a real sponsor's history and a 90-day time study before any economic claim.

## Implications for Unbound

- The targets with competitive value are the ones incumbents do not publish (A-2, B-5 to B-8). Unbound should commit to measuring them per migration and publishing them under UNB-ONB-030 once validated.
- Targets A-7/A-8 (electronic share, conversion) are where the evidence is weakest and the economic leverage strongest. They should be the first pilot measurements.

## Open questions / evidence gaps

- No measured exception rates exist for vetting renewal failure, sanctions false positives or migration. A-4 to A-6 and B-4 rest on assumptions.
- B-1 depends on incumbent export behaviour, which Unbound does not control. The clock starts at receipt of a usable extract.
- Auditor acceptance of the evidence pack and epoch design (B-1, G-4) can only be tested with a real auditor.
