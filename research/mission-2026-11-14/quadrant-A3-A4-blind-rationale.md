# Quadrant A3 and A4: blind second-scorer rationale (2026-11-14)

**Scorer:** `blind`. **Scores:** [`quadrant-scores-A3-blind.csv`](../../data/mission-2026-11-14/quadrant-scores-A3-blind.csv) and [`quadrant-scores-A4-blind.csv`](../../data/mission-2026-11-14/quadrant-scores-A4-blind.csv). **Method:** [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) v1.0.

**Independence.** I did not open the primary A3/A4 score files, `quadrant-positions.csv`, the primary A3/A4 rationale or the `quadrants/` charts while scoring. Running `scripts/mission_quadrants.py` after my CSVs were written printed every area's positions to the console, including the primary ones. That happened only after scoring, and no score was changed afterwards. Adjudication belongs in `quadrant-calibration.md`, not here.

**Status.** These are *internal-demonstration* claims (Clarity/EDF). The positions are bands, not points.

## 1. How I read the criteria for sponsors

| ID | How I applied it to a DAF sponsor |
|---|---|
| X1 scale | DAF assets from period-aligned DAFRC FY2024 Schedule D (`dafrc-sponsor-schedule-d-fy2019-2024.csv`). The denominator is $327.87bn (V2B-02). For June-FYE sponsors, FY2024 means June-2024 values. Fidelity's FY2024 row shows a stale `end_of_tax_period` of 2023-06-30, but the $66.20bn value matches the audited 6/30/2024 net assets (V2B-01). Primary 990s replace imputed rows where validated (GS PF $12.64bn, V1-21; Daffy $334m, V1-10). **A3 bands:** 4 = ≥$20bn (≥6% share); 3 = $5–20bn; 2 = $0.5–5bn; 1 = <$0.5bn but verifiable. **A4** uses consumer footprint: accounts and grant counts plus assets. Entity totals are used where the channel split is not public (Fidelity, DAFgiving360, Charityvest). |
| X2 delivery | `announced-vs-delivered.csv` rows, plus sponsor-reported results confirmed in the validation registers. |
| X3 assurance | 4 = published audited statements with control-relevant notes (related-party administration, custody, fee formulas) that a validator confirmed. 3 = audited statements published. 2 = a financials page that could not be read, or a vendor SOC claim with no scope. 1 = only a Form 990 or a draft statement. I found no SOC report for any sponsor. |
| X4 channel | Confirmed distribution and white-label edges in `relationship-graph-edges*.csv`. A captive single-firm wealth channel (GS, MS, BofA) scores 2. |
| X5 durability | Audited statements or a long history plus a diversified donor base scores 4. I deducted for dependence on a related vendor (RCF pays 98% of its fee revenue to Ren) or for a young sponsor that depends on a vendor. |
| X6 experience | `daf-user-complaints-corpus.csv`, counting high and critical records against scale. A provider with ≤1 record scores U. |
| Y1 openness | Donor/adviser data export or APIs. A portal history or statement download with no API scores 1. A partner-only API or a sponsor-level contractual export scores 2. A public donor API plus CSV export scores 3. A 4 would also need documented portability and data-ownership terms, and nobody has them. Positive restrictions on export score 0 (TIFIN terms §5.3 for GiveClear). |
| Y2 redesign | Electronic grant rails (Stripe/PayPal/Chariot), the review model, and API grant flows. Every sponsor still issues checks, so the large sponsors score 2. |
| Y3 governed automation | Score only with evidenced automation. Absence of AI claims (V2A-09) scores U, not 0. |
| Y4 breadth | Segments: wealth/adviser, consumer, faith, corporate, institutional/education. |
| Y5 portability | `sponsor-transfer-portability-terms.csv`. Inbound-only terms score 1. Evidence that transfers do go out, or multi-sponsor interoperability (DAFpay inbound), scores 2. API entity transfers plus portable history score 3. Documented history loss (AEF migration kept 2 years) is a lock-in signal and holds AEF at 1. |

## 2. Positions (blind)

### A3 — adviser / wealth channel

| Provider | X (band) | Y (band) | Coverage X/Y | Quadrant |
|---|---|---|---|---|
| Fidelity Charitable | 3.20 (3.20–3.20) | 1.65 (1.40–2.00) | 1.0/0.85 | Scale Operators |
| Vanguard Charitable | 3.20 | 1.47 (1.25–1.85) | 1.0/0.85 | Scale Operators |
| NPT | 3.39 (3.05–3.45) | 1.92 (1.15–2.75) | 0.9/0.6 | Scale Operators (boundary) |
| AEF | 2.50 (2.25–2.65) | 1.29 (1.10–1.70) | 0.9/0.85 | Scale Operators |
| DAFgiving360 | 3.10 | 2.00 (1.70–2.30) | 1.0/0.85 | Proven Leaders (boundary) |
| Renaissance Charitable Foundation | 3.39 (3.05–3.45) | 2.00 | 0.9/1.0 | Proven Leaders (boundary) |
| GiveClear | 1.94 (1.75–2.15) | 1.18 (1.00–1.60) | 0.9/0.85 | Focused Specialists (boundary) |
| Charityvest (adviser programs) | 1.78 (1.60–2.00) | 1.65 (1.40–2.00) | 0.9/0.85 | Focused Specialists (boundary) |
| Goldman Sachs Philanthropy Fund | 2.43 | 1.00 | 0.7/0.15 | insufficient evidence |
| Morgan Stanley GIFT | 2.43 | 1.00 | 0.7/0.15 | insufficient evidence |
| BofA Charitable Gift Fund | 2.43 | 1.00 | 0.7/0.15 | insufficient evidence |
| NCF | 3.20 | 2.00 | 0.5/0.15 | insufficient evidence |

### A4 — consumer and digital-first

| Provider | X (band) | Y (band) | Coverage X/Y | Quadrant |
|---|---|---|---|---|
| Fidelity Charitable (direct) | 3.40 | 1.65 (1.40–2.00) | 1.0/0.85 | Scale Operators |
| DAFgiving360 (direct) | 3.10 | 2.00 (1.70–2.30) | 1.0/0.85 | Proven Leaders (boundary) |
| Daffy | 2.45 | 2.35 | 1.0/1.0 | Proven Leaders |
| Endaoment | 2.22 (2.00–2.40) | 2.85 | 0.9/1.0 | Proven Leaders (boundary) |
| Every.org | 1.43 (1.00–2.20) | 2.29 (1.95–2.55) | 0.7/0.85 | Forward Builders (the band touches the midline on both axes) |
| Charityvest (direct) | 1.95 | 1.65 (1.40–2.00) | 1.0/0.85 | Focused Specialists (boundary) |
| Givinga consumer accounts | 1.29 | 2.00 | 0.35/0.15 | insufficient evidence |

## 3. Main judgements

- **Forward capability is low for the large sponsors.** No public donor API was found for Fidelity, Vanguard, DAFgiving360 or NPT. Outbound transfer terms are not published either. Their electronic rails are optional, and checks remain (V2B-13). No sponsor-side AI controls are disclosed (V2A-09).
- **RCF has the most wealth-channel reach** of any A3 sponsor (Edward Jones, Ameriprise, Janney, SEI, Franklin, First Citizens, MDRT, Pershing). It also has the best audited control disclosure (V1-01, V2B-10). RCF Y3 = 2 rests on its published due-diligence thresholds (V2A-23). The "instant approval" share is a vendor claim and was not used.
- **AEF:** the Ren migration was delivered, but only two years of history carried over (`dc-sunset`). That sets Y1 and Y5 to 1. Its X3 rests only on Ren's inconsistent SOC 2 boilerplate (V1-13).
- **GiveClear Y1 = 0** is the only 0 in this scoring. TIFIN Terms §5.3 restrict archiving and downloading and ban automated access, which is positive evidence of the deficiency. A customer agreement may supersede those terms, and if one does, this score should be re-scored.
- **Daffy:** all five tracked announcements were delivered (AVD24–28). It has a public API, MCP and CSV export. Its MCP write tools have no documented caps, so Y3 = 2. Records stop being accessible after an account closes, so Y5 = 2.
- **Endaoment** scores highest on Y: a public OAuth API, async grant submissions held for Endaoment review, entity transfers and on-chain records. Its X1 is small ($19.6–23.8m assets).
- **Every.org:** its 990 for TY2024 (revenue $51.4m, net assets $9.0m) has no Schedule D DAF data, so X1 = 1.
- **Givinga:** the homepage is corporate-only, and the evidence base has nothing on consumer accounts.

## 4. AI-governance overlay (flag, not axis)

- **Daffy:** a deployed MCP server whose write tools move money, with consent prompts on the client side only. Its AI charity-data "flagging issues for review" is announced and flag-only, but no controls have been seen.
- **Endaoment:** API grant flows require sponsor review. That is consistent with "AI may add a flag, never clear one", though no AI is evidenced.
- **All other A3/A4 sponsors:** no AI evidenced.

## 5. Gaps that would move positions

- **GS PF, MS GIFT, BofA CGF, NCF:** their Y coverage is 0.15. Each needs donor-portal export, grant-rail and transfer terms.
- **DAFgiving360 and NPT:** their audited statements were not inspected.
- **Daffy and Charityvest:** no audit or SOC is public.
- **All sponsors:** outbound DAF-to-DAF and history-export terms are missing.
