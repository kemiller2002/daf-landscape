# 14 — Beneficium verification economics

Model: `Beneficium.fs`; parameters [`beneficium-parameters.csv`](data/model-inputs/beneficium-parameters.csv) (58 rows); outputs [`beneficium-scenarios.csv`](data/model-outputs/beneficium-scenarios.csv), [`beneficium-overlap.csv`](data/model-outputs/beneficium-overlap.csv). Engineering at $118/h; compliance at $120/h (blend of dedicated and fractional, raised after review ADV-CS-004).

## 1. Cost without customers

| Tier | Annual cost (0 recipients) | Of which labour | FTE equivalent |
|---|---:|---:|---:|
| Public directory only | $57.6k | ≈ $48k | ≈ 0.25 |
| + historical filings | $63.6k | | |
| + grant relationship intelligence | $66.6k | | |
| + continuous regulatory monitoring | $93.1k | $83k | 0.46 |
| + automated verification evidence / human exception verification / payment enrolment | $131.5k | $122k | 0.67 |
| Full service (commercial licence $15k; charity support desk $38.6k) | $185.0k | $122k | 0.67 |

## 2. Incremental cost with active grant recipients

| Active recipients | Continuous monitoring | + human exception verification | + payment enrolment | Full service |
|---:|---:|---:|---:|---:|
| 0 | $93k | $131k | $131k | $185k |
| 1,000 | $95k | $135k | $139k | $193k |
| 10,000 | $109k | $166k | $208k (1.1 FTE) | $262k |
| 50,000 | $171k | $306k | $514k (2.7 FTE) | $568k |
| 100,000 | $249k | $481k | $896k (4.8 FTE) | $950k |
| 500,000 | $873k | $1.88M | $3.96M (21 FTE) | $4.01M |

Drivers per active recipient-year (base): eligibility events 0.04 × 17 effective minutes; name-match alerts 0.01 × 10 min; new recipients 20% × 8% exceptions × 45 min; evidence expiry 0.5 × 10% human × 5 min; payment enrolment 20% new × 50% needing enrolment × 20 min + $1.50 bank verification (price UNKNOWN). **Payment enrolment is the largest recipient-driven cost** and belongs with Transitus/payment providers rather than Beneficium.

## 3. Multiple sponsors with overlapping recipients

With 20,000 recipients per sponsor and union exponent 0.5 (heavy overlap among large recipients):

| Sponsors | Unique recipients | Annual cost (human exception tier) | Per sponsor |
|---:|---:|---:|---:|
| 1 | 20,000 | $201k | $201k |
| 3 | 34,641 | $253k | $84k |
| 10 | 63,246 | $353k | $35k |
| 30 | 109,545 | $515k | $17k |

Shared public evidence is where Beneficium's economics work: verification done once serves many sponsors. **Sponsor-specific eligibility decisions are not shared** (each sponsor's policy and legal responsibility remain its own).

## 4. Where Beneficium's costs sit in Unbound

To avoid double counting, Unbound's model includes Beneficium's **zero-recipient continuous-monitoring upkeep** (connector and pipeline engineering hours into the engineering pool; data-quality and owner hours into compliance; infrastructure, fees and counsel as cash), while **recipient-driven verification** is costed in Unbound's own CHARITY activities (OA-CHR-001..010). Payment enrolment (OA-CHR-007) sits in Unbound operations.

## 5. Can public charity intelligence operate with no dedicated staff?

- **Directory and continuous monitoring: yes**, at 0.25-0.5 FTE-equivalent of fractional engineering and compliance work, provided breaking source changes (~3 a year) are repaired within days and the August revocation surge (≈ 39,000 rows in 2026) is absorbed.
- **Verification at scale: no.** Above ~10,000 active recipients with payment enrolment, or ~50,000 without, the work exceeds one FTE.
- The accountable-owner floor (100 h) does not disappear; someone must own source governance, disputes and appeals.
