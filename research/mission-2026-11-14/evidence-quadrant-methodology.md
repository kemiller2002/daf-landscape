# DAF Evidence Quadrant: methodology (v1.0, 2026-11-14)

**Purpose.** Position providers within defined DAF market areas on two axes, using only cited public evidence. Every cell of the score traces to a source URL. Unknowns are shown as uncertainty, not guessed.

**Naming.** This is the repository's own method. It is **not** a Gartner Magic Quadrant, it is not affiliated with Gartner, and it does not use Gartner's criteria or labels. "Magic Quadrant" is a Gartner trademark. Analyst coverage of DAF platforms is surveyed separately in `analyst-and-education-landscape.md`.

**Frameworks.** The method follows Clarity and EDF as pinned in [clarity-edf-application-guide.md](clarity-edf-application-guide.md).
- **Clarity admissibility applies.** No false precision: positions are bands, not points. Scores are bounded truth: they hold within one market area and one date. Incentives are scored, not intent.
- **Scores are claims under the EDF claim policy.** A position is at most *internal-demonstration* until an independent scorer reproduces it (see the calibration section).
- **Positioning is a Clarity *Experimental* posture output.** It informs where to look. It is not a procurement verdict.

## 1. Market areas (each scored separately; never compare across areas)

| Area ID | Area | Who is in scope | Who is out of scope |
|---|---|---|---|
| A1 | DAF platform and administration (system of record) | Ren (incl. iPhi/DFX), Foundation Source (DAF OS / Vennfi), TIFIN Give, Give Interactive, Givinga, Foundant CommunitySuite, NPact (FIMS), Blackbaud Financial Edge NXT for foundations, sponsor-built platforms where evidenced (e.g. NCF/SVCF Salesforce, Fidelity in-house) | Pure CRMs with no DAF ledger |
| A2 | Grant disbursement and nonprofit-side DAF rails | Chariot (DAFpay, Disbursements), PayPal Grant Payments, Ren Rapid Disbursement Engine, Fidelity Charitable EFT, DAF Direct, Every.org, Stripe-based sponsor rails where evidenced | General card processors with no DAF function |
| A3 | DAF sponsors for the adviser / wealth channel | Fidelity Charitable, DAFgiving360, Vanguard Charitable, NPT, RCF, AEF, GiveClear, Charityvest, Goldman Sachs PF, MS GIFT, BofA CGF, NCF | Pass-through donation processors (scored in A3b only if needed) |
| A4 | Consumer and digital-first DAF sponsors | Daffy, Charityvest (direct), Endaoment, Fidelity Charitable (direct), DAFgiving360 (direct), Every.org, Givinga (consumer accounts) | Adviser-only programs |
| A5 | Charity eligibility and verification data | Candid (GuideStar APIs / Charity Check), IRS BMF/Pub 78/TEOS (public baseline), Goodstack, Chariot verification, Benevity validation, CharityCheck-type services | General KYC vendors |

An **AI-governance overlay** is reported for every area as a flag, not an axis. It records evidenced AI capabilities and whether they respect "AI may add a flag, never clear one" ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)).

## 2. Axes and criteria

Each criterion is scored **0–4** on the rubric below, or **U (unknown)** when no admissible evidence exists. Weights sum to 1.0 per axis and are the same across areas unless an area note overrides them.

### Axis X: Evidenced Execution (what the provider demonstrably does today)

| ID | Criterion | Weight | 0 | 2 | 4 |
|---|---|---|---|---|---|
| X1 | Evidenced scale | 0.25 | no verifiable customers/assets | verifiable mid-tier footprint (e.g. a few named customers, or <$5bn related assets) | dominant verifiable footprint in the area (named customers/assets from filings, portals, audits) |
| X2 | Delivery record | 0.20 | announcements mostly lack delivery evidence | mixed | announcements consistently followed by docs / customer use (`announced-vs-delivered.csv`) |
| X3 | Assurance and control evidence | 0.15 | none / contradictory | vendor-stated SOC 2 without scope | SOC report scope documented and consistent, or audited control disclosures |
| X4 | Distribution and channel reach | 0.20 | no confirmed channels | some confirmed channel edges | many confirmed channel / customer edges (`relationship-graph-edges.csv`) |
| X5 | Durability | 0.10 | distress signals, single-customer dependence | private, some funding/ownership clarity | audited financials or long operating history plus diversified customers |
| X6 | Customer experience signal | 0.10 | complaint pattern of severe, fixable failures | mixed | low severe-complaint rate relative to scale; documented service metrics |

### Axis Y: Evidenced Forward Capability (how well positioned for a redesigned, AI-era DAF stack)

| ID | Criterion | Weight | 0 | 2 | 4 |
|---|---|---|---|---|---|
| Y1 | Openness and data rights | 0.25 | no API / no export rights documented | partial API or contractual export | public API plus documented data-export/portability rights (`vendor-data-rights-matrix.csv`) |
| Y2 | Redesign capability | 0.25 | inherits per-grant manual, check-based workflow | some electronic or continuous features | continuous eligibility, electronic-first rails, event or state tracking shared with nonprofits |
| Y3 | Governed automation / AI | 0.15 | AI claims without controls, or none | evidenced automation; AI announced | deployed automation with documented controls (flag-only, authority separation, audit trail) |
| Y4 | Segment breadth | 0.15 | one narrow segment | two segments | serves several segments (wealth, community, faith, consumer, corporate) with evidence |
| Y5 | Interoperability and portability | 0.20 | lock-in signals (history loss, no transfer terms) | partial | documented migration/transition support; history export; multi-rail or multi-sponsor interoperability |

## 3. Evidence admissibility (a score needs at least one of these)

1. Primary sources: audited statements, IRS filings, statutes, contracts, official docs and API references, live portal footers or DNS (first-party "powered by").
2. Independent corroboration: validation-register rows marked `confirmed`.
3. Vendor self-claims are admissible **only** with `evidence_class = vendor_claim`. They cap the criterion at 2 unless corroborated.
4. Absence of evidence yields **U**, never 0. A score of 0 needs positive evidence of the deficiency (e.g. contradicted claims, documented history loss).

## 4. Computation (`scripts/mission_quadrants.py`)

- **Point estimate** per axis: the weighted mean of scored criteria, renormalized over scored weight.
- **Uncertainty band** per axis: unknown criteria are set to 0 for the lower bound and 4 for the upper bound, giving a box, not a point.
- **Evidence coverage** = scored weight ÷ total weight. Providers with coverage below 0.5 on either axis are plotted hollow and labelled "insufficient evidence".
- **Quadrants** (midline at 2.0 on each axis):
  - **Proven Leaders**: high execution, high forward capability.
  - **Scale Operators**: high execution, lower forward capability.
  - **Forward Builders**: lower execution, high forward capability.
  - **Focused Specialists**: lower on both.

  A provider whose band crosses a midline is reported as "boundary".

## 5. Calibration and independence

- **Two-scorer rule.** Each area is scored by one agent and re-scored blind by a second agent from the same evidence base. Disagreements of more than 1 point on any criterion are adjudicated in `quadrant-calibration.md`.
- **Independent status.** Scores are labelled *internal-demonstration* until a second scorer reproduces the quadrant assignment.
- **Re-scoring triggers** (Clarity reconsideration criteria):
  - new filings or audited statements;
  - a validation result changing an input;
  - a vendor publishing APIs or SOC scope;
  - a complaint-pattern change;
  - acquisition or ownership change.

## 6. Data files

| File | Purpose |
|---|---|
| `data/mission-2026-11-14/quadrant-scores-<area>.csv` | Scores. Columns: `area_id,provider,criterion_id,score,evidence_class,evidence_summary,source_url,source_date,scorer,notes`. `score` is 0–4 or U. `evidence_class` is one of primary, validated, vendor_claim, secondary. |
| `data/mission-2026-11-14/quadrant-positions.csv` | Output: point estimates, bands, coverage and quadrant per provider and area. |
| `research/mission-2026-11-14/quadrants/<area>.svg` | Rendered charts: point, uncertainty box, hollow marker when coverage is below 0.5. |

## 7. Version 1.1 area notes (2026-11-14, from calibration P-QCAL-07)

The calibration ([quadrant-calibration.md](quadrant-calibration.md)) showed that most one-point gaps between scorers came from different readings of the rubric, not from different evidence. The following notes are binding from v1.1 onward. They apply at the next re-score; the v1.0 consensus positions stand until then.

**Sponsor areas A3 and A4, X1 (evidenced scale).** Use FY2024 DAF assets, period-aligned: the DAFRC FY2024 row equals June-2024 values for sponsors with a June fiscal year end. Where a filed Form 990 Schedule D or an audit exists, it replaces the imputed DAFRC value.

| Score | FY2024 DAF assets |
|---|---|
| 0 | positive evidence of negligible scale |
| 1 | under $0.5bn |
| 2 | $0.5–5bn |
| 3 | $5–20bn |
| 4 | at least $20bn |

**Sponsor X3 (assurance and control).**
- A Form 990 alone, or a 2-page summary with no auditor's report, scores **U**.
- Audited financial statements with an auditor's opinion that the scorer has read score **3**.
- A scoped SOC 1 or SOC 2 report covering the sponsor's DAF system (sponsor's or administrator's, with scope matching) scores **4**.
- Contradictory vendor assurance statements score **1**.

**Y5 (interoperability and portability) for sponsors.**
- Published *inbound*-only transfer pages ("recommend a closing grant from your old sponsor") score at most **1**.
- Published *outbound* transfer terms score **2**.
- Outbound terms plus a history export score **3**.
- Documented in-kind transfer plus a history export scores **4**.
- Documented history loss on a platform migration (e.g. AEF's two-year window) caps the score at **1**.

**Scope rule for A1 sponsor-built platforms.** A platform evidenced as built or hosted by a vendor is scored under that vendor, not as "sponsor-built". Example: NPT GivingPoint runs on Ren iPhi ([validation wave 3](validation-wave3-report.md)). At the next re-score, merge the NPT GivingPoint row into Ren and record NPT as a Ren customer edge.

**Entity scope rule.** Evidence about a vendor is not evidence about a sponsor, and the reverse also holds, unless a source ties the capability to that sponsor's program. Examples: the vendor's API does not prove a sponsor offers donors data export; a sponsor's audit does not prove the vendor's SOC scope.

**AI overlay vocabulary.**
- **GREEN:** controls documented, including flag-only and authority separation.
- **AMBER:** capability live with undocumented limits, but sponsor approval remains.
- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval.
