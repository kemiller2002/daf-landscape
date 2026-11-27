# 27 — Final recommendations

All recommendations are research findings for owner decision; none authorises expenditure, launch or production implementation.

## 1. Enter through licensing with support, priced per account

Full administration has a cash floor of about **$1.8-2.2M a year** before the first sponsor reaches scale, and needs a first sponsor of roughly **$0.9-1.1B at 20 bps** (or $1.8-2.2M of fees) to cover it alone. Licensing with support (CFG-2) has a floor of about **$1.4M**, keeps operational and control seats with the sponsor, and breaks even at about **13,000-41,000 accounts at $250-150 per account**. Recommend CFG-2 (or CFG-6 through a channel partner) as the entry offer; full administration only with a single large sponsor or a contracted per-sponsor minimum (OD-ZB-03).

## 2. Price for sponsors, not only for assets

Each full-administration sponsor costs about **$145k a year** at the margin plus ~1,320 onboarding hours (~$160k). Use a per-sponsor annual minimum (~$185k) and implementation/migration fees; tier the AUA fee; avoid AUA-only pricing for retail and payroll programmes (OD-ZB-04).

## 3. Attack the floors, not the variable minutes

The variable economics (~$142 per account, ~58 minutes) already match a well-designed exception-driven operation. The money is in:

| Floor | Size | Action |
|---|---:|---|
| Platform engineering | ~$0.9M (4 FTE) | share with other Echelon products in production (OD-ZB-06); reduce custom integrations; certify counterparties once |
| Compliance staffed to December peak | ~$0.25M | tiered SLAs (OD-ZB-07); pre-peak list hygiene |
| Per-sponsor close and audit support | ~760 h per sponsor | continuous close; shared workbench; auditor reliance on automated controls |
| Assurance, insurance, counsel | ~$0.3M | combined SOC engagement; scope by reliance; broker quotes once OD-ZB-02 allows |

## 4. Redesign requirements that create recurring work (control objectives preserved)

P1: board delegation as activation gate (CNV-GRT-001); determination reuse and per-trigger calibration for Tier-2 review (CNV-GRT-011); auditor/board acceptance of deterministic release (CNV-GOV-003); notification-first contributions (UNB-GAP-013); continuous close (UNB-ACC-017/020); tiered compliance SLAs; validate the 0.5 FTE reserved-authority default (CNV-GOV-004). P2 list in [21](21-requirement-economic-impact.md).

## 5. Adopt hybrid charity vetting

Continuous monitoring + deterministic 180-day re-evaluation + human review of exceptions and the high-risk tier. It preserves the 180-day validity rule, has the fewest expected false negatives, and costs ~$74k at 10,000 active recipients against ~$634k for full manual review. Vet active recipients only.

## 6. Build Beneficium as a fractional, shared public-data capability

Directory plus continuous monitoring costs ~$93k a year with zero customers (0.46 FTE-equivalent). Its value compounds with sponsors (per-sponsor cost falls from $201k to $17k between 1 and 30 sponsors). Payment enrolment belongs with Transitus/payment providers. Create the repository (it does not exist) only when the owner decides.

## 7. Measure before scaling

Run the planned synthetic operating-year time study (OD-M-14), populate Praxis telemetry with human time and tokens, and instrument activity IDs in the case kernel. The top uncertainties (handling minutes, exception rates, engineering hours, small-sponsor close effort) each move annual cost by $0.2-0.5M.

## 8. Resolve the governance blockers

Founder allocation (OD-ZB-01); the DF-ASR-2026-0D0F conflict (OD-ZB-02); key-person concentration (one human holds every role; no Unbound entity or board). A regulated sponsor's due diligence will treat the last as a limitation regardless of cost.

## 9. Make economic impact part of requirements

Adopt the economic impact record for material requirements and the regression report as a research-backed standard; enforce through Praxis only after owner approval (OD-ZB-05).

## Proposed organisational structure (full administration, first large sponsor)

4 engineers (one security/on-call owner), 2 compliance staff, 2 operations staff with December surge, fractional accountant, fractional controller, fractional independent authorizer (or sponsor treasury), founder for commercial and executive work with fractional support, external counsel, SOC auditor, Nacha auditor, MDR provider. About 8 employees and 15 named persons. Under licensing with support: 4 engineers, 1 compliance owner plus backup, fractional support.
