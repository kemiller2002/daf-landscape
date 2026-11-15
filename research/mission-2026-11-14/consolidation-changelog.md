# Consolidation changelog (2026-11-15)

**Scope.** Editorial consolidation of [`DAF-INDUSTRY-REPORT-2026-11.md`](../DAF-INDUSTRY-REPORT-2026-11.md) and [`strategic-synthesis.md`](strategic-synthesis.md). No web research was done and no new factual claims were added. Every figure below comes from an existing workstream document, a governing validation correction, or a validation register (`data/mission-2026-11-14/validation-register*.csv`).

**History preserved.** Verbatim copies of both files as they stood before consolidation:
- [archive/DAF-INDUSTRY-REPORT-2026-11.pre-consolidation.md](archive/DAF-INDUSTRY-REPORT-2026-11.pre-consolidation.md)
- [archive/strategic-synthesis.pre-consolidation.md](archive/strategic-synthesis.pre-consolidation.md)

**Rules applied.**
- No finding was deleted. Findings were moved into themes. Where a later validation wave superseded a figure, only the corrected figure is shown, and the superseded figure is recorded in §3 below with its replacement.
- All inline workstream links in the old §11 (38 distinct documents) and all URLs in the old synthesis G list were checked as still present after the rewrite.
- Report headers §1–§10 keep their numbering. Markdown tables were checked for consistent column counts.

---

## 1. Structural changes

### 1.1 Industry report

| # | Change | Where |
|---|---|---|
| S1 | §11 retitled from "Round-2 findings: failures, complaints, buyers, payments, contracts, mortality" to "Round-2 findings: thematic consolidation (validated through wave 12)" | §11 |
| S2 | The chronological list (15 topic blocks plus batch 23, 24, 25, 26 and 27 blocks and the "Vendor scope and the Give Interactive shift" block) was replaced by eight themes: 11.1 Market structure and data quality; 11.2 Vendors and platform shifts; 11.3 Payments and nonprofit-side economics; 11.4 Donor cost and portability; 11.5 AI and agentic controls; 11.6 Capital markets; 11.7 Customer experience; 11.8 Monitoring and open questions | §11 |
| S3 | An intro to §11 states the traceability and correction rules, links this changelog and the archive, and maps batches 23–27 to validation waves 8–12 | §11 intro |
| S4 | Consolidation note added under the version line | header |
| S5 | Wave-4 governing section at the end marked "Applied in §2.5" | end of report |
| S6 | New source-register entry for the first-party Fidelity Giving Report PDF (required by W4-14) | Source register |

**Where each old §11 block went.**

| Old block | New location |
|---|---|
| Failed and retreated ventures | 11.6 |
| User complaints | 11.7 |
| Who is interested in DAF organizations | 11.6 |
| Payments | 11.3 (policy bullets; nonprofit cost per $1,000; DAF Direct and Givinga) |
| Contracts, data rights and agent controls | 11.4 (vendor templates) and 11.5 (Daffy MCP and Louise merged into the agentic-controls table) |
| Assurance | 11.2 (SOC findings) and 11.8 (terms monitor) |
| Sponsor mortality | 11.6 |
| Analyst and education coverage | 11.1 |
| Sponsor cost structure from Form 990 | 11.1 (cost, scale, sensitivities) and 11.5 (effect on the AI-economics model) |
| Agentic donation controls and sponsor audits | 11.5 (controls table) and 11.6 (sponsor audits) |
| AI economics v2 | 11.5 |
| Bank-program terms and EFT providers | 11.3 (both tables) |
| Private equity across the DAF ecosystem | 11.6 (lender sentence merged into "Lenders and BDC marks") |
| Channel moves | 11.2 (Commonwealth, GiftingNetwork) and 11.1 (DAFgiving360 → Fidelity $976.6m line); the Give Interactive/CCT question went to 11.2 |
| Community-foundation rails and portals | 11.3 (rails table) and 11.2 (portal table) |
| Batch 23 (export, agentic products, nonprofit fees, credit, labour, DonorSphere) | 11.4; 11.5; 11.3; 11.6; 11.5; 11.2 |
| Batch 24 (sponsor terms, Candid, CF vendor map, credit fix) | 11.4; 11.4; 11.2; 11.6 (merged; superseded figures in §3) |
| Batch 25 (all-in cost, ledgers, CF switches, DAFpay access, credit) | 11.4; 11.2; 11.2; 11.3; 11.6 |
| Batch 26 (Ren attrition, net payout, adviser fees, NPact, not-yet-measurable) | 11.2; 11.1; 11.4; 11.2; 11.8 |
| Batch 27 (GivingPoint, Fidelity stack, nonprofit-side panel, ledger segment) | 11.2; 11.2; 11.3; 11.2 |
| Vendor scope and the Give Interactive shift | 11.2 |

**Duplicates merged in §11.**

| Duplicate | Merged into |
|---|---|
| Three separate credit blocks (batches 23, 24, 25) and the PE map's lender sentence | One "Lenders and BDC marks" list (11.6) |
| "Fidelity's EFT-only policy is not in effect" (Payments) and "No sponsor requires EFT; Fidelity is transitioning" (batch 27) | Grant payment policy (11.3) |
| Daffy MCP / Louise bullets (Contracts block) and the agentic-controls table | One table (11.5) |
| NPact ownership (batch 26), NPact manufacturer (batch 25) and NPact owner/BroadWest (batch 27) | One NPact bullet (11.2) |
| NPT/J.P. Morgan/ICGF iPhi redirects (batch 26) and the GivingPoint white-label book (batch 27) | GivingPoint (11.2) |
| "Give Interactive has no live CF portals" (batch 24) and the Give Interactive shift block | Give Interactive (11.2) |
| Nonprofit-side DAF fees (batch 23) and the nonprofit-side panel (batch 27) | "What nonprofits pay" (11.3) |
| Arizona CF FIMS move (batch 25 and batch 27) | Kept in both ledger bullets because they come from two workstreams with different scope (portal-only foundations vs the Salesforce segment) |

### 1.2 Strategic synthesis

| # | Change |
|---|---|
| T1 | Date line: revised 2026-11-15, with links to this changelog and the archive |
| T2 | Validation line: adds waves 3–12 and points to report §11 |
| T3 | A1, A2, A4, A7, A8 and A10 gain "Round 2" evidence from validated workstreams |
| T4 | New rows A11 (adviser fees "capped and modest") and A12 ("AI agents can safely give today") |
| T5 | Clarity reading extended with two more denominator substitutions (gross vs net payout; admin fee vs all-in cost) |
| T6 | B: round-2 agentic-products bullet under "Market reality" and a "Contract allocation" bullet under "Risk" |
| T7 | C: GivingPoint added to the architectural row; lenders and PE map added to the organizational row; export and complaints added to the customer-experience row; new row "Client attrition at the long tail"; nonprofit-side fees added to the payments row; SOC finding added to the assurance row; Foundant measured share and Fidelity's FMR stack added to "not vulnerable" |
| T8 | D: new rows "Credential-based or scraping integrations" and "Holding donor funds"; gating condition gets a provisional round-2 answer |
| T9 | E1 adviser-fee figures corrected (see §2.2); E3 all-in pool evidence; E4 Candid licence constraint; E6 nonprofit-side fees |
| T10 | F: Ren row updated (NPT already counted; Fidelity FMR); portability row adds donor export and the terms monitor; four new rows (data/automation closed; Ren attrition; agentic products; net payout) |
| T11 | G rewritten and re-ranked (map below). Each entry now carries evidence, uncertainty, implication, next action and an EDF state with a Clarity posture |
| T12 | "Not in the top ten" list extended with capital markets, failures and mortality, assurance, complaints and analyst coverage |
| T13 | Source register: Fidelity Giving Report PDF added |

**Top-10 re-ranking (old → new).**

| New rank | Title | Built from (old rank) |
|---|---|---|
| 1 | Donor data and automation are contractually closed | old #9 (portability) + D gating condition + batches 23–24 |
| 2 | Most "DAF accounts" aren't DAF customers, and headline totals need correction | old #1 + corrected totals + Givinga sensitivity |
| 3 | Ren's footprint is large but well below its claims; NPT GivingPoint is a Ren white-label book | old #3 + old #4 + batch 27 |
| 4 | Ren is losing smaller clients, mainly to Foundant, in a 2025–26 wave | new (batches 25–26; Give displacement) |
| 5 | The platform market is segmented, and a sponsor's trust owns the third white-label stack | old #2 + old #10 + CF vendor map + ledgers |
| 6 | Donor cost is set by pools and uncapped adviser fees, and fee flows reward retention | old #8 + batches 25–26 |
| 7 | Payout is lower net of DAF-to-DAF transfers and bimodal behind the average | old #7 + batch 26 |
| 8 | Agentic giving products are donor-side, unrecognised by contract and unproven | old #6 + batch 23 + agentic-controls workstream |
| 9 | The value pool for operations AI is thin; the buyer is an administrator or platform | old #5 + AI economics v2 |
| 10 | Nonprofits bear the cost of fragmented grant rails | new (payments, nonprofit-side panel, CF rails) |

Old entries were not dropped: every old entry is contained in a new one, and all its links and figures were carried over. Old #10's detail sits in new #5 under "Give Interactive detail retained"; old #3–#4 detail sits in new #3 under "Earlier evidence retained". The cite-check HTML comment from old #4 (V2B-05, $29.65bn = 9.04%) is restated as text in new #3; the same comment remains in A4.

---

## 2. Figures and statements updated outside §11

### 2.1 Industry report §1–§10

| # | Location | Before | After | Governing source |
|---|---|---|---|---|
| R1 | §1 table, Reported accounts | "79.5% are in 22 donation-processor sponsors holding 0.9% of assets" | Same, plus "about 59–67% if Givinga, whose account unit is undefined, is excluded" | [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md), wave-5 corrections 1–2; V5-01 |
| R2 | §1 vendor footprint paragraph | 30 sponsors / $48.55bn (14.8%) any year; 18 / $30.18bn (9.2%) latest | Adds "GS DAPF ($11.84bn) appears in FY2022 only; on corrected FY2024 assets the cumulative share is 15.0%" | [full-universe-990-harvest-and-corrected-totals.md](full-universe-990-harvest-and-corrected-totals.md), wave-5 correction 7 |
| R3 | §1 concentration table, Software row | "Community foundations mostly on Foundant CommunitySuite (claims 700+)" | Vendor claim kept; adds the measured 361 of 803 (45%) and 32.7% of mapped CF DAF assets | [queue-cf-vendor-map.md](queue-cf-vendor-map.md); V9-09 |
| R4 | §1 Payout, transfers bullet | Transfers 10–18% of nationals' grants inflate payout | Adds pooled net payout 19.0–21.5% vs 23.9% gross | [queue-net-payout-fidelity-outliers.md](queue-net-payout-fidelity-outliers.md); V11-05a |
| R5 | §2.2 Ren beyond RCF | "Ren-owned iPhi still serves … ImpactAssets" | Adds that ImpactAssets is a late-stage Give Interactive migration and iPhi lost 6 of 57 sponsors | [queue-give-interactive-displacement.md](queue-give-interactive-displacement.md); [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md); V11-01a, V11-01h |
| R6 | §2.2 Wave-3 additions | GivingPoint on Ren infrastructure (hosting evidence) | Adds the wave-12 extension to 13 NPT-sponsored sites | [queue-npt-givingpoint-fidelity-stack.md](queue-npt-givingpoint-fidelity-stack.md); V12-01 |
| R7 | §2.5 Payment rails | "Charityvest from Aug 2026" | "Charityvest transitioning from Aug 2026" | [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md), wave-6 correction 7; V6-06 |
| R8 | §2.5 first bullet | "The only observed switch is Charityvest moving from PayPal to Chariot" | Adds that it is still in transition and Charityvest's own guide still describes PayPal | Same as R7 |
| R9 | §2.5 second bullet | "About 67% of Fidelity grants already go by EFT ([Chariot …])" | First-party quote and PDF, Chariot kept as secondary | [validation-wave4-report.md](validation-wave4-report.md) W4-14 |
| R10 | §3 Vendor economics, Ren bullet | Garbled trailing fragment "(Earlier estimates: 8.7% → 9.0% → 28% …) of assets (…" | Fragment repaired to "8.7% → 9.0% → 28% of assets"; no figure changed | Editorial |
| R11 | §3 Revenue model, adviser bullet | OneGive 55 bps only | Adds: 1.00% caps only at MS GIFT, DAFgiving360, TIFIN Give; no numeric cap at Fidelity CIAP, NPT, AEF, RCF; observed 0–2.00% | [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md), wave-11 note; [queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md), adviser-fee update; V10-05d, V11-07a–d |
| R12 | §8 gating question | Open question | Adds the partial round-2 answer (batch export yes, live integration no; no top-10 export; restrictive terms) | [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md); [queue-donor-export-cf-payments-donorsphere.md](queue-donor-export-cf-payments-donorsphere.md); [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) |
| R13 | §9 "Evidence that would most change this report" | List only | Adds a note that items 2–4 were partly answered and that waves 3–12 are reported per wave | Editorial cross-reference |
| R14 | §10 "What the quadrants show", bank programs | "Goldman, Morgan Stanley GIFT and BofA CGF cannot be placed on public evidence" | True only for v1.0–v1.1. v1.2 places MS GIFT and BofA CGF as Scale Operators; Goldman remains insufficient evidence | Same section's v1.2 table; [quadrant-v12-targeted-rescore.md](quadrant-v12-targeted-rescore.md); [validation-wave6-report.md](validation-wave6-report.md) |
| R15 | §10 "AI-governance overlay" (Benevity "Watch") | Unlabelled | Labelled "v1.0; superseded by the v1.1 overlay above" (v1.1 rates Benevity RED provisional) | Same section's v1.1 overlay; [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md) |

Figures checked and already correct (no change): Ren ~28% technology footprint and 9.2% latest-990 (§1, §3); Edward Jones "$2.9bn" marked unverifiable (§2.2, V1 register); corrected FY2024 totals $323.27bn (§1, V5-04); Vanguard related-party fee $4.24m FY2026 (§2.1); Bain "majority in 2023, significant shareholder after 2025" (W4-6).

### 2.2 Strategic synthesis

| # | Location | Before | After | Governing source |
|---|---|---|---|---|
| Y1 | A7 | "Chariot (Mar 2026) reports about 67% of Fidelity grants already by EFT" | Fidelity's own 2026 Giving Report (PDF), Chariot kept as secondary | W4-14 |
| Y2 | A4 | 14.8% any-year 990 share without the GS DAPF and corrected-asset qualifier | Adds GS DAPF FY2022-only and 15.0% on corrected assets | Wave-5 correction 7 (asks for the same qualifier in the synthesis) |
| Y3 | E1 | "Adviser AUM on DAF assets (55 bps at OneGive; up to 1% elsewhere)" | Caps of 1.00% only at MS GIFT, DAFgiving360, TIFIN Give; no numeric cap at Fidelity CIAP, NPT, AEF, RCF; observed 0–2.00%. "Up to 1% elsewhere" is superseded | Adviser-fee update in [queue-all-in-cost-dafpay-access.md](queue-all-in-cost-dafpay-access.md); wave-11 note in [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md); V11-07a–d |
| Y4 | C, payments row | "Only one observed switch (Charityvest PayPal→Chariot)" | "… still transitioning from Aug 2026" | Wave-6 correction 7; V6-06 |
| Y5 | F, Ren row | Revise if Ren components found inside "Fidelity Charitable, DAFgiving360, Vanguard Charitable or NPT" | NPT is already counted on hosting evidence; Fidelity shows FMR in-house | V3-05, V12-01, V12-03 |
| Y6 | Old G4 / new G3 | 14.8% presented as the 990 measure | 9.2% latest-990 and ~5% administration given equal weight with the 28% technology footprint | V5-05; wave-5 correction 7 |

---

## 3. Superseded figures dropped from §11 (with replacements)

| Superseded text (old §11) | Replacement used | Governing source |
|---|---|---|
| Batch 24 credit fix: "The Bonterra 2032 loan is held at 98.2–99.5%" | 13 holders marked 97.7–99.5% (KKR Enhanced Fund-L 97.71% at 2026-06-30) | [queue-bdc-coverage-migrations-goodstack.md](queue-bdc-coverage-migrations-goodstack.md), wave-10 correction §1 finding 2; V10-08b |
| Batch 24 credit fix: "Five New Mountain funds are missed by the parser (queued)" | The fixed parser now includes them among the 13 holders | Same; V10-08b |
| Batch 24 credit fix: "Audax holds Foundation Source's loans at par (Sept 2026)" | Merged into "Audax remains its first-lien lender (S+5.00%, 2030, at par)" | [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md), wave-8 correction 25; V8-01 |
| Batch 23 credit: "refinanced in 2025 into an S+5.00% loan due 2032" | "S+4.75–5.00% loan due 2032" | [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md), wave-8 correction 15; [queue-pe-lenders-labour-rates.md](queue-pe-lenders-labour-rates.md), wave-8 correction 10 |
| PE map: "No lenders were found for Ren, Bonterra or Benevity" | "No BDC lender for Ren or Benevity"; Bonterra lenders listed | Wave-8 corrections 15–16 in [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md); V10-08c |
| PE map: "Lenders found: Audax to Foundation Source (2020)" (read as historical only) | Audax recorded in 2020 and still the current lender | Wave-8 correction 25 (supersedes wave-7 correction 5) |
| Vendor-scope block heading "Credit data fix (superseded by batch 25 below)" | Removed as a heading; content merged | Editorial |

Qualifications added in §11 from governing corrections (wording only; no figure changed):

| Item | Qualification added | Governing source |
|---|---|---|
| Shift4 earnout cut $47.1m | "in FY2022" | [firms-interested-in-daf-organizations.md](firms-interested-in-daf-organizations.md) W4-9 |
| iPhi 15-day export window | Ren's published template; executed terms may differ | [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md) W4-18 |
| Fidelity cost per grant ~$68 | ~$59 excluding advisor program and taxes; ~$71 period-matched | [sponsor-cost-structure-and-sensitivities.md](sponsor-cost-structure-and-sensitivities.md) wave-5 correction 6 |
| "No donor export at the top 10" | Public material only; AEF's Export button covers only a legacy grants-paid list | V8-08; [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) wave-9 correction 5; V9-05 |
| SVCF clause | Adds the third-party-access indemnity | [queue-donor-export-cf-payments-donorsphere.md](queue-donor-export-cf-payments-donorsphere.md) wave-8 corrections 17–18 |
| Vanguard "Unauthorized Third Party" | Own aggregators permitted; read-only self-run is an inference | [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) wave-9 correction 1 |
| NPT terms | "any software, model or AI system" wording | Same, wave-9 correction 1 |
| Fidelity licence "may provide" export | Undated clause; no live feature found | Same, wave-9 correction 4 |
| Adviser fees "no cap" at Fidelity CIAP, NPT, AEF, RCF | "No numeric cap"; Fidelity caps relative to the firm's own schedule | [queue-adviser-fees-pools-npact.md](queue-adviser-fees-pools-npact.md) wave-11 note (P-ACC-03) |
| DAFpay 2.9% rounding | Applies only without a platform agreement; ~4% at $25 is the worst case | [queue-agentic-products-dafpay-fees.md](queue-agentic-products-dafpay-fees.md) wave-8 correction 23 |
| DAFgiving360 $50 minimum | From a 2024 policy document | [queue-nonprofit-side-panel.md](queue-nonprofit-side-panel.md) wave-12 note |
| "No sponsor requires EFT" | "No sponsor checked requires EFT today" | Same, wave-12 note |
| CCT "Check only" (rails table) | "Checks only documented (DAF grants)" | [queue-community-foundation-rails-portals.md](queue-community-foundation-rails-portals.md) wave-7 correction 4 |
| NPact in top-40 portal table | "Foundation Cloud on spectrumportal.net; NPact attribution from third-party sources" | Same, wave-7 correction 3 |
| Maine CF Fund 360 | On Salesforce; Accounting Seed not confirmed for Maine | [queue-ledgers-behind-portals.md](queue-ledgers-behind-portals.md) wave-10 correction (line 85) |
| Give Interactive at CCT | GiftingNetwork documented by Feb 2024; Dec 2025 refresh fits incumbency | [queue-vendor-channel-moves.md](queue-vendor-channel-moves.md) wave-6 correction 1 |
| NPact ownership | Cambria lists NPact as portfolio company; BroadWest right to transact not established | V11-08c; [queue-ledger-segment-npact-owner.md](queue-ledger-segment-npact-owner.md) wave-12 note |
| GivingPoint hosting | Global Accelerator pair attributed to Ren by inference | [queue-npt-givingpoint-fidelity-stack.md](queue-npt-givingpoint-fidelity-stack.md) wave-12 note |

---

## 4. Conflicts not resolved (left visible in the text)

1. **Donor export at the top 10.** The finding "none publishes a donor-side machine-readable export" (V8-08, partially confirmed) sits beside AEF's live "Export" button (V9-05) and Fidelity's permissive licence clause (V9-04). Both are reported, with the qualification that AEF's export is a legacy grants-paid list. Settling it needs logged-in access.
2. **Two attrition denominators for Ren iPhi.** Wave 11 gives 6 of 57 sponsors (10.5%; strict 8.8%). Wave 10 gives 4 of 8 flagged foundations in 2025–26. They use different bases, so both are kept.
3. **Base for Ren's share.** The 28% footprint uses DAFRC's $327.9bn. Only the any-year 990 share has been restated on corrected assets (15.0%), so the 28% and 9.2% figures have not been recomputed on $323.27bn.
4. **Transfer share at nationals.** The FY2025 range of 10–18% (four nationals' 990s) and the pooled FY2021–24 figure of 12.1% (to other nationals) differ in scope and period. Both are kept.
5. **Givinga's account unit.** Two candidate explanations (game or app-user records; employer-provisioned accounts) remain unresolved (V5-01).
6. **Bonterra 2032 spread.** S+4.75–5.00% per wave 8. FS KKR's 4.75% is not confirmed from its filings (wave-9 correction 2).
7. **§10 history.** The v1.0 quadrant table and overlays remain for history beside v1.1 and v1.2. They are now labelled but not removed.

## Validation corrections (wave 13, 2026-11-15) — governing
Source: [validation-wave13-report.md](validation-wave13-report.md).

1. **§3.** Add a sub-table, "Synthesis items dropped or reworded", that logs V13-B04 items (d), (e) and (f):
   - "about three times earlier estimates" → retained as "8.7% → 9.0% → 28%" (line 22);
   - "EIN-match vendor client lists to the DAFRC panel" → superseded by the EIN-level CF vendor map (V9-09);
   - the Schedule R "related partnership" wording → "held 99% since CY2020" (validation wave 3).
2. **R9 and Y1.** Replace "[validation-wave4-report.md] W4-14" with "[validation-wave4-report.md] row 14 (W4-14 in the report's governing wave-4 section)".
3. **"Rules applied", first bullet.** Append: "Wave-13 audit: six synthesis items were initially dropped without an entry; see validation-wave13-report.md."
