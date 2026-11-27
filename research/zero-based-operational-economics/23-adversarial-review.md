# 23 — Adversarial review

Ten perspectives reviewed the model, inputs and outputs in five independent agent contexts (two perspectives each). Raw findings: [`data/evidence/adversarial/`](data/evidence/adversarial/). Consolidated register with dispositions: [`adversarial-findings.csv`](data/registers/adversarial-findings.csv). **These are adversarial analytical exercises by the same model family, not independent professional assurance.**

## 1. Coverage

| Context | Perspectives | Findings (high) |
|---|---|---:|
| ops-controller | Experienced DAF operations executive; financial controller | 23 (9) |
| compliance-security | Compliance and risk specialist; security and resilience specialist | 23 (9) |
| buyer-investor | Institutional technology buyer; skeptical investor | 24 (12) |
| infra-maintenance | Cloud infrastructure economist; software maintenance engineer | 25 (6) |
| org-automation | Organisational design specialist; automation architect | 23 (7) |
| **Total** | 10 | **118 (43)** |

Directions: about 70% cost-up, 15% cost-down, the rest structural or neutral.

## 2. Dispositions

| Disposition | Count | High severity |
|---|---:|---:|
| Accepted (model or input changed) | 84 | 41 |
| Partly accepted | 10 | 1 |
| Noted (documented; no change justified) | 19 | 0 |
| Escalated to owner decision | 3 | 1 |
| Superseded | 1 | 0 |
| Rejected as base case | 1 | 0 |

## 3. Material findings and what changed

**Structural model defects (found independently by two reviewers):**
1. *Bucket order* (ADV-OC-001, ADV-OA-001): any sponsor-responsible activity went to the sponsor before its classification was checked, so "full administration" never performed independent authorization, close preparation or audit support, and CFG-4 = CFG-5. **Fixed:** classification first; SponsorReserved (vendor prepares) and SponsorDelegable (vendor performs under full administration) buckets.
2. *Review routing* (ADV-OA-002, ADV-IM-012, ADV-OC-002): every second-person minute went to the controller pool, including code review. **Fixed:** routed to the reviewed work's pool.

**Underestimated labour:** engineering keep-the-lights-on only (ADV-IM-025/015/016/017/018) → defect correction, shared integration upkeep, regulatory change, patching added; engineering rose from ~1,700 h (2 FTE) to ~4,100 h (4 FTE). Compliance had no backup (ADV-CS-005) → two named persons. No management time (ADV-OA-005) → 10% management ratio. Turnover and recruiting (ADV-OA-012).

**Hidden costs:** privileged-access review, MDR, on-call, breach cost, immutable backups, escrow, key-person continuity, entity bookkeeping, observability stack, higher insurance limits, SOC 1 for licensing configurations.

**Unjustified commercial framing** (ADV-BI-001/002/003/007/016): the first draft's headline ($0.5B) combined licensing at 20 bps, a single $500M sponsor, and View 1 against the original's full-administration figure. **Fixed:** break-even by sponsor size; licensing priced per account; onboarding per event; capital required; matching-view comparisons.

**Over-conservative items accepted:** least-cost fractional versus dedicated (ADV-OA-003, ADV-CS-006, ADV-OC-009); duplicated incident hours removed (ADV-OC-016, ADV-OA-017, ADV-CS-022); Beneficium upkeep absorbed by staffed pools instead of separate cash (ADV-OC-010); vetting exposure measured from publication (Rev. Proc. 2018-32) and including the grant-time check (ADV-CS-001/002).

**Rejected:** dropping Front Door Premium from the base (ADV-IM-004) — managed WAF on a financial application kept as base; Standard is the low case.

**Escalated:** founder allocation (OD-ZB-01); conflict with DF-ASR-2026-0D0F on counsel and independent-review spend (OD-ZB-02); sponsor-side reserved-authority floor of ~0.5 FTE per holder (OD-ZB-04 / REI-002).

## 4. Effect of the corrections

| Measure | First draft | After rounds A and B |
|---|---:|---:|
| View 1 at $500M, full administration | $1.03M | **$2.20M** |
| Vendor hours at $500M | 3,852 | 7,200 |
| Dedicated FTE at $500M | 3 | 8 |
| Break-even at 20 bps, $250k, full administration, $500M sponsors | ~$0.5B | **$1.85B** |
| Like-for-like with original at 7,695 accounts / 5 sponsors | $1.50M vs $3.85M | **$3.89M vs $3.85M** |

The first draft's conclusion that the original model was inflated by ~2-3× did not survive review. That reversal is preserved here as a finding.

## 5. Final synthesis review

A separate synthesis pass checked the reports against the regenerated outputs after corrections ([research-ledger.md](research-ledger.md) records its result and any fixes).

## 6. Remaining material disagreements

- Engineering at four FTE is a judgement from inventory plus review; an Echelon-method time record could move it ±1-2 FTE (±$0.2-0.5M).
- Exception rates borrowed from incumbent baselines may be conservative or optimistic for Unbound's design; only measurement resolves it.
- Whether small sponsors really need the same per-sponsor close and audit effort as large ones (the most consequential open assumption for minimum viable sponsor size).
