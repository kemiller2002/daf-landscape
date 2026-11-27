# 15 — Charity vetting alternatives

The existing **180-day maximum validity requirement is preserved** (Unbound charity assurance decision record; no authorised decision changes it). Model: `Beneficium.vetting`; output [`vetting-alternatives.csv`](data/model-outputs/vetting-alternatives.csv). Presence in a public registry is **never** treated as authorisation to receive a grant: every approach keeps Unbound's deterministic transaction-time status check (OA-CHR-002) and sponsor-specific policy.

## 1. Distinctions

| Concept | Meaning in the model |
|---|---|
| Evidence freshness | age of the newest authoritative evidence for a charity |
| Policy re-evaluation | re-running the sponsor's eligibility rules against current evidence |
| Full manual investigation | a person reviews the charity end to end (15 min base, 5-30) |
| Automated renewal | deterministic re-evaluation that raises a human exception only on failure (3% base) |
| Material change detection | monitored feeds (BMF, Pub 78, revocations, OFAC, CA AG) produce change events (4% of active charities a year) |
| Payment verification | bank ownership verification at enrolment and on bank-detail change (independent authorization) |
| Sponsor-specific acceptance | the sponsor's policy overlay; never shared |

## 2. Exposure model (revised after review ADV-CS-001/002)

- Legal exposure starts at **publication** of a revocation, not at the underlying event: under Rev. Proc. 2018-32 a sponsor may generally rely on published IRS status. Exposure for monitored events is therefore the ingestion lag (15 days base) plus missed detections until the next check.
- Events outside monitored feeds (stale sources such as 990-N filers and state registries; 10% base) are caught only by periodic re-evaluation (90-day average window) or, without it, within about a year.
- False negatives cost $2,500 per ineligible grant (base; $500-25,000: recovery, possible 4966 first-tier tax — abatable for reasonable cause under 4962 — and reputational cost). False-positive holds cost 30 minutes each.

## 3. Results

**10,000 active recipients (35,000 grants a year):**

| Approach | Human hours | Labour | Expected false negatives | FN cost | Total | Meets 180-day rule |
|---|---:|---:|---:|---:|---:|---|
| Full manual review every 180 days | 5,000 | $600k | 12.1 | $30k | $634k | yes |
| Automated re-evaluation every 180 days | 150 | $18k | 10.0 | $25k | **$47k** | yes |
| Continuous monitoring only | 113 | $14k | 19.5 | $49k | $69k | **no** |
| Change-driven investigation | 100 | $12k | 20.0 | $50k | $68k | **no** |
| Grant-triggered review | 150 | $18k | 10.0 | $25k | $47k | yes |
| Risk-tiered review | 745 | $89k | 11.0 | $27k | $121k | yes |
| **Hybrid** (continuous + automated 180-day + human review of high-risk tier) | 375 | $45k | **9.0** | $22k | $74k | yes |

**100,000 active recipients:** full manual $6.34M; automated $468k; continuous $687k (fails rule); hybrid $737k with the fewest false negatives (90).

## 4. Active recipients versus the whole database

Reviewing every 501(c)(3) in the database (≈ 1.69M) every 180 days would need **845,000 hours ($101M) manually**, or $3.3M automated, against $0.47-0.74M for 100,000 active recipients. False negatives depend on grants, not on the population reviewed — so reviewing inactive charities buys nothing. **Vet only charities that receive or are about to receive grants**; keep the database current by monitoring, not by review.

## 5. Recommendation

Adopt the **hybrid**: continuous authoritative monitoring for change detection; deterministic 180-day re-evaluation (evidence refresh, policy re-run) for every active recipient, which satisfies the validity rule without a full human review; human investigation only for automated-renewal failures, change-driven exceptions and the high-risk tier (fiscal sponsors, new or foreign-facing organisations, flagged entities). Relative to the original registry design (1.0 FTE steward), this keeps the 180-day rule and the sponsor's control while cutting human hours by more than 90% against full manual review.

**What the model cannot settle:** whether an auditor and the sponsor's board accept deterministic renewal as satisfying "validity" (SPD-GRT-001 is open); the true stale-source share; and miss rates of human versus automated review. These are measurement items in [25](25-evidence-gaps-and-validation-plan.md).
