# 09 — Economic analysis

Research package: [file ingestion and straight-through processing](README.md) (2026-11-26). Model: [`scripts/fie_economics.py`](../../scripts/fie_economics.py); parameters (each labelled measured, sourced, assumed or scenario): [`economics-parameters.csv`](../../data/file-ingestion-2026-11/economics-parameters.csv); outputs: `economics-results.csv`, `economics-onboarding.csv`.

## 1. What the model does and does not claim

Version 2 (after adversarial review R3, recorded in the [research ledger](RESEARCH-LEDGER.md)). For one sponsor
administering 1,000 to 1,000,000 funds, the model converts the [inventory's](03-DAF-INGESTION-WORKFLOW-INVENTORY.md)
volume drivers into annual units — records for data files (or files when a workflow has no record driver), documents
for evidence — and splits human work into:

- **policy-mandated decisions** (`human_decision_floor`, e.g. complex assets, successions, manual journals) at
  conventional minutes, reduced by AI assistance where the workflow allows AI;
- **intrinsic investigations** — a class-specific share of automatable units (observation sets 0.2–1–3%, aligned with
  the repository's reconciliation-break rate; other records 1–2–5%) at 30–45–135 minutes each;
- **routine touches** — automatable units not processed straight through, at conventional minutes; the **routine STP
  rate** (50–99%) applies only to these; and
- **file-level exceptions** — late, missing, drifted or control-total failures, a separate 0.5–2–5% of data files.

Investigations fall only in an explicit **prevention scenario** (30–50–60% prevented, at $0.5–$1–$3 per fund per year),
never for free. A **dashboard STP** (units with no human action ÷ all units) is reported beside the routine rate: at a
routine rate of 99% it is only about 95–97%, because investigations and policy decisions remain.

Costs are labour for residual work, metered cloud costs (object storage for the retention period, malware scanning,
document AI), the prevention cost where applied, and fixed costs per sponsor in two variants: **pooled** (a
multi-tenant operator reusing mappings: run cost plus amortised reuse-onboarding) and **standalone** (bespoke
integrations for 4–8 institutions and a 0.5–1 FTE staffing floor, because dual control cannot be staffed below two
people). Migration is one-off and excluded. Revenue shares are reported for $50k, $150k and $300k books separately from
the cost case.

**Nothing here is measured for DAF ingestion** (gaps G1, G2); grants per fund is sourced, cloud prices are measured,
and everything else is a labelled assumption. Ingestion cost is a *slice* of a sponsor's operating cost: do not add it
to the staffing models in research/ai-native-daf-enterprise, which already include exception and reconciliation labour.
The fully manual reference (every record keyed) is a straw man, not current practice.

## 2. Results

<!-- BEGIN GENERATED: economics -->
**A. Share of 20 bps servicing revenue consumed by ingestion, at 90% routine STP, by book balance** (pooled = multi-tenant operator reusing mappings; standalone = sponsor alone with bespoke integrations and a 0.5–1 FTE staffing floor)

| Funds | Case | Prevention | $50k book | $150k book | $300k book | Standalone at $150k | Dashboard STP |
|---|---|---|---|---|---|---|---|
| 1,000 | low | none | 18.4% | 6.1% | 3.1% | 24.9% | 87.5% |
| 10,000 | low | none | 8.3% | 2.8% | 1.4% | 3.0% | 88.5% |
| 100,000 | low | none | 7.3% | 2.4% | 1.2% | 2.5% | 88.6% |
| 1,000,000 | low | none | 7.2% | 2.4% | 1.2% | 2.4% | 88.6% |
| 1,000 | low | scenario | 18.2% | 6.1% | 3.0% | 25.1% | 87.6% |
| 10,000 | low | scenario | 8.3% | 2.8% | 1.4% | 3.0% | 88.5% |
| 100,000 | low | scenario | 7.3% | 2.4% | 1.2% | 2.5% | 88.7% |
| 1,000,000 | low | scenario | 7.2% | 2.4% | 1.2% | 2.4% | 88.7% |
| 1,000 | mode | none | 55.7% | 18.6% | 9.3% | 44.9% | 87.2% |
| 10,000 | mode | none | 26.2% | 8.7% | 4.4% | 9.8% | 88.0% |
| 100,000 | mode | none | 23.2% | 7.7% | 3.9% | 7.8% | 88.1% |
| 1,000,000 | mode | none | 22.9% | 7.6% | 3.8% | 7.7% | 88.1% |
| 1,000 | mode | scenario | 48.3% | 16.1% | 8.1% | 45.2% | 87.7% |
| 10,000 | mode | scenario | 20.1% | 6.7% | 3.4% | 7.8% | 88.5% |
| 100,000 | mode | scenario | 17.2% | 5.8% | 2.9% | 5.9% | 88.6% |
| 1,000,000 | mode | scenario | 17.0% | 5.7% | 2.8% | 5.7% | 88.6% |
| 1,000 | high | none | 493.1% | 164.4% | 82.2% | 220.2% | 86.0% |
| 10,000 | high | none | 353.4% | 117.8% | 58.9% | 123.4% | 86.5% |
| 100,000 | high | none | 339.4% | 113.1% | 56.6% | 113.7% | 86.6% |
| 1,000,000 | high | none | 338.1% | 112.7% | 56.3% | 112.7% | 86.6% |
| 1,000 | high | scenario | 281.9% | 94.0% | 47.0% | 161.5% | 87.7% |
| 10,000 | high | scenario | 164.3% | 54.8% | 27.4% | 60.3% | 88.2% |
| 100,000 | high | scenario | 152.5% | 50.8% | 25.4% | 51.4% | 88.3% |
| 1,000,000 | high | scenario | 151.3% | 50.4% | 25.2% | 50.5% | 88.3% |

**B. Pooled ingestion cost per fund per year, mode case, no prevention**

| Funds | STP 50% | STP 75% | STP 90% | STP 95% | STP 99% |
|---|---|---|---|---|---|
| 1,000 | $77.58 | $63.90 | $55.70 | $52.96 | $50.77 |
| 10,000 | $44.31 | $32.98 | $26.18 | $23.91 | $22.10 |
| 50,000 | $41.35 | $30.23 | $23.56 | $21.33 | $19.55 |
| 100,000 | $40.98 | $29.89 | $23.23 | $21.01 | $19.23 |
| 500,000 | $40.69 | $29.61 | $22.97 | $20.75 | $18.98 |
| 1,000,000 | $40.65 | $29.58 | $22.93 | $20.72 | $18.95 |

**C. Same, mode case with the prevention scenario (50% of investigations prevented at $1 per fund)**

| Funds | STP 50% | STP 75% | STP 90% | STP 95% | STP 99% |
|---|---|---|---|---|---|
| 1,000 | $70.39 | $56.61 | $48.34 | $45.59 | $43.38 |
| 10,000 | $38.33 | $26.92 | $20.07 | $17.79 | $15.96 |
| 50,000 | $35.48 | $24.28 | $17.56 | $15.32 | $13.53 |
| 100,000 | $35.12 | $23.95 | $17.24 | $15.01 | $13.22 |
| 500,000 | $34.84 | $23.68 | $16.99 | $14.76 | $12.98 |
| 1,000,000 | $34.80 | $23.65 | $16.96 | $14.73 | $12.95 |

**D. Dashboard-definition STP (units with no human action ÷ all units), mode case, no prevention** — the model's routine STP rate excludes investigations and policy decisions; this is what a dashboard would show

| Funds | STP 50% | STP 75% | STP 90% | STP 95% | STP 99% |
|---|---|---|---|---|---|
| 1,000 | 48.5% | 72.7% | 87.2% | 92.1% | 96.0% |
| 10,000 | 48.9% | 73.4% | 88.0% | 92.9% | 96.8% |
| 50,000 | 48.9% | 73.4% | 88.1% | 93.0% | 96.9% |
| 100,000 | 49.0% | 73.4% | 88.1% | 93.0% | 96.9% |
| 500,000 | 49.0% | 73.4% | 88.1% | 93.0% | 97.0% |
| 1,000,000 | 49.0% | 73.5% | 88.1% | 93.0% | 97.0% |

**E. Fully manual reference (every record keyed) versus residual staff** — the manual reference is a straw man, not current practice at sponsors that already use reconciliation tools

| Funds | Conventional FTE (low / mode / high) | Residual FTE at 90% routine STP (low / mode / high) |
|---|---|---|
| 1,000 | 1.6 / 1.7 / 3.3 | 0.1 / 0.2 / 1.7 |
| 10,000 | 4.4 / 5.4 / 18.9 | 0.6 / 1.5 / 13.9 |
| 50,000 | 16.8 / 21.9 / 88.0 | 2.9 / 7.0 / 67.8 |
| 100,000 | 32.3 / 42.6 / 174.4 | 5.8 / 13.9 / 135.3 |
| 500,000 | 156.3 / 208.0 / 865.9 | 29.0 / 69.3 / 675.1 |
| 1,000,000 | 311.4 / 414.7 / 1730.2 | 57.9 / 138.6 / 1349.9 |

**F. Marginal onboarding cost of one more institution**

| Case | Bespoke (days / cost) | New mapping on shared infrastructure | Reuse of an existing mapping | Shadow run (business days elapsed) |
|---|---|---|---|---|
| low | 15 / $9,338 | 8 / $4,980 | 1 / $623 | 10 |
| mode | 30 / $24,750 | 15 / $12,375 | 3 / $2,475 | 20 |
| high | 50 / $71,429 | 25 / $35,714 | 6 / $8,571 | 40 |
<!-- END GENERATED: economics -->

## 3. Findings

1. **Under modal assumptions, routine ingestion is a modest slice of a ~20 bps price at scale — not a small one.** For a
   $150k book it takes about 8% of 20 bps revenue at 90% routine STP for sponsors of 10,000 funds or more, about 6%
   with the prevention scenario. Raising routine STP from 90% to 99% saves less than preventing investigations does.
2. **The intrinsic investigation rate × minutes per investigation dominates everything else.** The high case
   (3–5% of units investigated at 135 minutes) consumes more than the whole 20 bps at a $150k book, and about half of
   it even with prevention. The decisive unknown is therefore that product, which nobody publishes (G1, G2); the first
   measurement any operator should make is touches and minutes per exception type.
3. **Balance matters as much as scale.** A $50k book pays a quarter of the revenue of a $150k book for similar work:
   ingestion takes about 23% of 20 bps there under modal assumptions. A per-fund minimum fee or prevention is needed.
4. **Small sponsors are viable only on shared infrastructure.** At 1,000 funds the modal pooled share is about 19% of
   20 bps at $150k; standalone — bespoke integrations and a two-person staffing floor — about 45%. This supports buying
   operating infrastructure from a multi-tenant operator rather than building it, as the repository's earlier staffing
   models also concluded. Policy decisions cannot be pooled across sponsors where governance forbids shared deciders;
   only non-decision investigation work can.
5. **Routine STP targets should be modest.** Adjacent industries reach roughly 85–95% automated matching on structured
   data after calibration and less at cold start (FIE-B-012, FIE-B-015, FIE-B-066; vendor-reported); none supports 99%.
   Plan 75–85% in a new institution's first months, 90% after calibration, 95% as a stretch; treat 99% as a
   prevention scenario without adjacent-industry precedent.
6. **Metered cloud costs are small**: object storage, malware scanning and document AI together are about $4,600 a year
   at 100,000 funds in the mode case — not a reason to avoid scanning or AI-assisted review.
7. **Onboarding economics depend on reuse.** A second institution matching an existing mapping costs about 3
   engineer-days (mode) against about 30 for a bespoke integration and 15 for a new mapping on shared infrastructure —
   assumptions anchored on a vendor-reported EDI analogue (FIE-B-021), not measurements.

## 4. Alternative pricing structures

| Structure | Effect on ingestion economics | Evidence |
|---|---|---|
| Pure asset-based (~20 bps) | Revenue scales with balance, cost with activity; small balances under-recover | Fidelity Charitable tiers and $100 minimum (research/ai-native-daf-enterprise/09-financial-models) |
| Asset-based with per-fund minimum | Closes the small-balance gap in finding 3 | Minimums are standard at national sponsors ($100–$250) |
| Fixed onboarding and migration fees | Recovers lumpy costs that a small sponsor cannot amortise | Ren sells migration as a separate service (FIE-A-050) |
| Per-transaction fees | Aligns with activity but penalises active giving | Not common for DAF administration |

## 5. Sensitivity and evidence status

The dominant parameters are, in order: intrinsic investigation share × minutes per investigation; average balance;
loaded cost per FTE; STP rate. Storage, scanning and AI prices barely move the result. Everything above should be
replaced by measured values from a shadow pilot (touches per 1,000 records, minutes per exception type) before any
viability claim is made.
