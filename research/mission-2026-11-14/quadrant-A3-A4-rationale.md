# DAF Evidence Quadrant: A3 and A4 rationale (primary scorer, 2026-11-14)

**Status.** Internal demonstration. One scorer, not yet reproduced (see the two-scorer rule in [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §5). This is the repository's own method. It is **not** a Gartner Magic Quadrant.

**Files.**
- Scores: `data/mission-2026-11-14/quadrant-scores-A3-primary.csv` (12 sponsors × 11 criteria) and `quadrant-scores-A4-primary.csv` (7 × 11).
- Engine output: `data/mission-2026-11-14/quadrant-positions.csv`, plus charts in `research/mission-2026-11-14/quadrants/A3-primary.svg` and `A4-primary.svg`.
- Queue proposals: `data/mission-2026-11-14/queue-proposals-quadrant-A3A4.csv` (P-QA3-01 to 07).

**Scope.** Positions hold only within one area on this date. Never compare A3 positions with A4 positions. Fidelity Charitable, DAFgiving360 and Charityvest appear in both areas, scored separately.

## 1. Positions (engine output)

### A3: sponsors for the adviser / wealth channel

| Provider | X (execution) | X band | Y (forward) | Y band | Coverage X / Y | Quadrant |
|---|---|---|---|---|---|---|
| NPT | 3.64 | 2.00–3.80 | 1.92 | 1.15–2.75 | 0.55 / 0.60 | Scale Operators (boundary) |
| DAFgiving360 | 3.08 | 2.00–3.40 | 2.00 | 1.20–2.80 | 0.65 / 0.60 | Proven Leaders (boundary) |
| Fidelity Charitable | 3.05 | — | 1.75 | — | 1.00 / 1.00 | Scale Operators |
| Renaissance Charitable Foundation | 2.72 | 2.45–2.85 | 2.40 | 1.80–2.80 | 0.90 / 0.75 | Proven Leaders |
| AEF | 2.44 | 2.20–2.60 | 1.42 | 0.85–2.45 | 0.90 / 0.60 | Scale Operators |
| GiveClear | 2.17 | 1.95–2.35 | 2.33 | 1.75–2.75 | 0.90 / 0.75 | Proven Leaders (boundary) |
| Charityvest (adviser programs) | 1.95 | — | 2.50 | 1.50–3.10 | 1.00 / 0.60 | Forward Builders |
| Vanguard Charitable | 2.80 | — | 2.00 | 0.90–3.10 | 1.00 / 0.45 | insufficient evidence (Y) |
| Morgan Stanley GIFT | 2.64 | 1.45–3.25 | 2.00 | 0.30–3.70 | 0.55 / 0.15 | insufficient evidence |
| NCF | 2.29 | 0.80–3.40 | 1.00 | 0.15–3.55 | 0.35 / 0.15 | insufficient evidence |
| Goldman Sachs Philanthropy Fund | 2.27 | 1.25–3.05 | 1.00 | 0.15–3.55 | 0.55 / 0.15 | insufficient evidence |
| BofA Charitable Gift Fund | 2.18 | 1.20–3.00 | 1.00 | 0.15–3.55 | 0.55 / 0.15 | insufficient evidence |

### A4: consumer and digital-first sponsors

| Provider | X | X band | Y | Y band | Coverage X / Y | Quadrant |
|---|---|---|---|---|---|---|
| DAFgiving360 (direct) | 3.08 | 2.00–3.40 | 2.00 | 1.20–2.80 | 0.65 / 0.60 | Proven Leaders (boundary) |
| Fidelity Charitable (direct) | 3.05 | — | 1.75 | — | 1.00 / 1.00 | Scale Operators |
| Daffy | 2.82 | 2.40–3.00 | 2.65 | — | 0.85 / 1.00 | Proven Leaders |
| Charityvest (direct) | 2.00 | — | 2.50 | 1.50–3.10 | 1.00 / 0.60 | Proven Leaders (sits exactly on the X midline) |
| Endaoment | 1.55 | 0.85–2.65 | 2.47 | 2.10–2.70 | 0.55 / 0.85 | Forward Builders |
| Givinga consumer accounts | 1.36 | 0.75–2.55 | 2.00 | 0.80–3.20 | 0.55 / 0.40 | insufficient evidence |
| Every.org | — | 0–4 | 2.00 | 0.50–3.50 | 0 / 0.25 | insufficient evidence |

"—" in a band column means every criterion on that axis is scored, so there is no band. Charityvest (direct) has X = 2.00 exactly. The engine labels it Proven Leaders, but treat it as a midline case: a 0.05 change on any X criterion would move it.

## 2. How the criteria were read for sponsors

A sponsor is a charity, not a software vendor, so several criteria need a sponsor reading. Each reading is applied the same way to every provider.

| ID | Reading for sponsors | Calibration |
|---|---|---|
| X1 | Period-aligned DAFRC FY2024 Schedule D DAF assets and accounts ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Where DAFRC is *imputed*, the score uses `secondary` and the notes give the last filed value. A filed 990 or audited figure overrides an imputed DAFRC row (GS PF, RCF, Daffy). | **A3:** 4 ≥ $40bn; 3 = $7–40bn; 2 = $1–7bn; 1 = verifiable < $1bn. **A4:** 4 ≥ $40bn; 2 = verifiable $100M–$5bn; 1 = verifiable < $100M. Whole-entity figures stand in for the adviser or direct sub-channel. That is a known limitation (P-QA3-06). |
| X2 | Rows in `announced-vs-delivered.csv` for the sponsor. For an outsourced sponsor, this means the delivery record of its administrator (RCF ← Ren; GiveClear ← TIFIN Give; Charityvest ← Foundation Source). No rows → U. | |
| X3 | Audited financial statements whose related-party, administrator or custody notes the repo has read = 3. An inspected SOC 1/2 scope covering the sponsor's platform = 4. A vendor SOC claim with no report = `vendor_claim`, capped at 2. Contradictory claims push toward 0. A filed 990 alone is not assurance. | An affiliate's SOC is never imputed to the sponsor ([soc2-assessment](../soc2-assessment-2026-11-11.md)). |
| X4 | Confirmed distribution or white-label edges and rails in `relationship-graph-edges.csv`. A single captive channel = 1. | |
| X5 | Audited statements or long operating history, plus a diversified donor base = 4. Dependence on a single administrator (such as RCF's 98% fee share to Ren) or venture funding caps it lower. | |
| X6 | `daf-user-complaints-corpus.csv` (built concurrently, non-random, no denominators). A small sample with no severe complaints is not taken as positive evidence (held at 2). No records → U. | P-QA3-04 asks for a rate per 10,000 accounts. |
| Y1 | Donor- or adviser-facing data export, public APIs, and contractual export rights. A nonprofit-side export counts as partial (Fidelity = 1). | |
| Y2 | Electronic-first grant rails, recurring and continuous features, and review latency. Per-grant review with an optional EFT = 2. | |
| Y3 | Deployed automation with documented controls. RCF's published due-diligence policy (automated screening plus officer review above $500k) is non-AI automation with authority separation, so it scores 3. Act-capable AI with no documented controls = 1. | |
| Y4 | Segments with evidence: wealth/adviser, direct consumer, corporate/workplace, faith, institutional/university, international, crypto. | |
| Y5 | Published inbound and outbound transfer terms, closing terms, history export, and multi-rail or multi-custodian interoperability (`sponsor-transfer-portability-terms.csv`). Documented history loss (AEF portal migration) or a default-to-sponsor succession rule (NPT) are lock-in signals. | No reviewed sponsor publishes an outbound policy, so no one scores above 2 except on interoperability evidence. |

## 3. Per-provider justification

### A3

- **Fidelity Charitable.** X1 4: $66.20bn and 204,614 accounts (DAFRC FY2024). X3 3: audited FY2025 statements, Note 7 (fee formula paid to FMR; V1-15, V2B-09) ([audit](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)). X2 2: mixed record. DAF Direct had slow adoption. A third-party claim of electronic-only grants is contradicted by Fidelity's own FAQ ([FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html)). X4 3: UBS distribution ([UBS](https://advisors.ubs.com/mediahandler/media/662455/Donor%20Advised%20Fund%20FactSheet.pdf)), CIAP. X6 2: the complaint pattern is mostly fixable app-login failures plus structural disputes over discretion (SPLC 2026, which drew a 16-AG letter: [CA AG](https://oag.ca.gov/node/623769)). On Y it falls short: no public API (Y1 1), EFT is optional and grants take 10+ business days (Y2 2), and the only AI is a navigation-only assistant (Y3 1; [terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)). Result: Scale Operator.
- **DAFgiving360.** X1 4: $40.94bn and 112,188 accounts (filed FYE 2024-06). X5 4: long 990 history ([ProPublica](https://projects.propublica.org/nonprofits/organizations/311640316)). X2 and X3 are U. Audited content was not accessible, and the sponsor has no tracked announcements. Y2 2: 38% of grants are recurring ([2025 results](https://www.dafgiving360.org/press-release/2025-results), V2A-08). Y5 2 rests on IPS data showing it is the largest outbound DAF-to-DAF grantor ([IPS](https://inequality.org/article/daf-to-daf-giving-2024/)). It is on the boundary because Y = 2.00 with 40% of Y weight unknown.
- **Vanguard Charitable.** X2 3: the PayPal electronic-grants announcement was delivered at scale ([release](https://prnewswire.com/news-releases/vanguard-charitable-launches-electronic-granting-solution-surpassing-100-million-in-electronic-grants-to-more-than-400-charities-in-first-4-months-301932762.html)). X3 3: audited statements ([FY2025](https://www.vanguardcharitable.org/sites/default/files/2026-02/vanguard-charitable-2025-financial-statements.pdf)). Y1, Y3 and Y4 are U, so Y coverage is 0.45 and it is labelled insufficient evidence even though X is strong.
- **NPT.** X1 4: $42.12bn FY2024 and $56.4bn FY2025 AUM ([AR](https://www.nptrust.org/annual-reports/npt-annual-report/)). X4 3: private-label sponsor for J.P. Morgan, Wells Fargo and UBS ([JPM](https://www.jpmorgan.com/content/dam/jpm/securities/documents/DAFExecutiveSummary.pdf)). Y5 1: no transfer page, and abandoned accounts default to the NPT Giving Fund ([FAQ](https://www.nptrust.org/donor-advised-funds/faq/)). X2, X3 and X6 are U. That gives the widest X band of the plotted sponsors.
- **Renaissance Charitable Foundation.** It has the strongest evidence profile in A3. X4 4: about 15 white-label edges (Edward Jones, Ameriprise, RBC, LPL, NWM, UBS, SEI and others; [RCF DAF](https://www.reninc.com/rcf-daf/)). X3 3: audited statements FY2020–24 disclose the 98% fee share to Ren ($19.23m in FY2024; V1-01, V2B-10; [audit](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)). Y3 3: a published due-diligence policy with escalation thresholds ([policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)). X5 is held at 3 because it depends on a single administrator. X1 is only 2 ($5.90bn audited).
- **AEF.** X2 3: the Ren migration was delivered on its stated timeline ([timeline](https://engage.aefonline.org/upgrade-timeline/)). X3 1: AEF-hosted releases contradict each other on Ren's SOC type (V1-13). Y4 1: adviser-only ([AEF](https://www.aefonline.org/thought-leadership/recent-increase-daf-transfers-aef/)). Y5 1: the new portal kept only two years of history ([sunset notice](https://engage.aefonline.org/dc-sunset/)). Result: Scale Operator, low Y.
- **GiveClear.** X1 1 ($24.8M filed FY2023), but X2 3 (most TIFIN Give launches delivered, including SEI: [SEI](https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience)). X4 3: SEI, AssetMark, Zions, Blue Trust, Ingalls & Snyder. Y2 3: 48-hour review and 2–7-day electronic payment ([guidelines](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines)). Y3 1 because of Louise (see §4). It sits on the boundary on both axes.
- **Charityvest (adviser programs).** X4 3: TIAA (V1-07; [TIAA](https://www.tiaa.org/public/about-tiaa/news-press/press-releases/2026/09-28)), Temple and OneAscent. Y4 4: consumer, wealth, faith-based adviser, and university/nonprofit turnkey. X1 1: $98.6M filed, $224.6M in 2025. The audit is indexed but was not inspected (X3 2). Result: Forward Builder.
- **GS PF, MS GIFT, BofA CGF, NCF.** Each has scale evidence (GS PF $12.6bn TY2024, V1-21; [990](https://projects.propublica.org/nonprofits/organizations/311774905/202503109349303645/full)) and one or two channel edges. Y criteria are almost entirely U (Y coverage 0.15), so they cannot be plotted. That reflects missing evidence, not weakness.

### A4

- **Daffy.** It is the only A4 sponsor with full Y coverage. X2 4: 5 of 5 tracked announcements delivered. Y1 3: public REST API and MCP server ([docs](https://docs.daffy.org/)), but records are lost on closure ([help](http://help.daffy.org/en/articles/6520234-how-do-i-close-my-daffy-account)). Y2 3: Chariot is the default electronic rail ([Daffy](https://www.daffy.org/resources/electronic-donations-chariot)). Y3 2: MCP `make_donation` with no documented limits (V2A-11). X6 3: 38 corpus records, none high or critical. X1 2: $334.5M filed CY2024 (V1-10), which replaces the imputed DAFRC row. The $2bn figure for Sep 2026 is self-reported. X3 U: no audit or SOC evidence.
- **Fidelity Charitable (direct) and DAFgiving360 (direct).** Same evidence as A3. X4 is re-read for consumer channels. On X6, the Fidelity app's long run of login failures pulls toward 1 in a consumer area, but it is held at 2 because the sample is self-selected over 13 years.
- **Charityvest (direct).** Lower X4 (2: Chariot and Foundation Source only). The Chariot direct-account rollout is unconfirmed (AVD31). It sits exactly on the X midline.
- **Endaoment.** Y1 3: public partner API and tiers ([institutions](https://endaoment.org/institutions)). Y5 2 (`vendor_claim`): "the DAF follows the assets". X1 1: $18.9M, 1,213 accounts ([990](https://projects.propublica.org/nonprofits/organizations/844661797/202631359349315978/IRS990ScheduleD)). X4 2: Altruist launch ([InvestmentNews](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481)). Result: Forward Builder.
- **Givinga.** Vendor claims only, plus an anomalous Schedule D (1.42M accounts holding $1.95M; [990](https://projects.propublica.org/nonprofits/organizations/474172718/202503179349301975/IRS990ScheduleD)). Insufficient evidence.
- **Every.org.** Only Y1 is scored (2, [API docs](https://docs.every.org/docs/intro)). The site returned HTTP 429, and its EIN and DAF scale were not retrieved. Unplottable.

## 4. AI-governance overlay (flag, not axis)

Test: "AI may add a flag, never clear one" ([ai-governance-failure-modes.md](ai-governance-failure-modes.md)).

| Provider | Evidenced AI | Action authority | Controls documented | Flag |
|---|---|---|---|---|
| GiveClear (TIFIN Give Louise) | Announced; marketing only (U01, AVD12) | Acts: recurring grants, stock contributions | None stated. Boundary with GiveClear grant approval undocumented. | **RED**: act-capable without documented controls |
| Daffy (MCP server) | Deployed, public docs (U03, V2A-11) | Moves money (`make_donation`, `cancel_donation`) | Client-side permission prompt; OAuth/API key; no per-donation limits | **AMBER**: real money movement; approval delegated to the AI client |
| Daffy (charity-data unification) | Announced (U05) | Flags issues "for review" | Implied human review | Compliant in principle (flag only) |
| Fidelity Charitable | Virtual Assistant, navigation only (U07) | None | Accuracy disclaimer; account requests routed to phone | Compliant (no authority) |
| RCF | No AI. Automated Charity Check screening. | Screens; officer review above $500k | Published policy | Compliant; the model for "automation with authority separation" |
| All others | None evidenced | — | — | No flag. Absence ≠ no AI use. |

## 5. Unknowns that drive the bands

1. **Assurance (X3).** U for DAFgiving360, NPT, GS PF, MS GIFT, BofA and NCF. No sponsor-specific SOC report has been inspected for any sponsor in either area.
2. **Data rights (Y1).** Scored for only one of 12 A3 sponsors (Fidelity = 1). The wealth-captive sponsors' adviser data feeds are undocumented.
3. **Portability (Y5).** No sponsor publishes outbound or history-export terms. U for GS PF, MS GIFT, BofA and NCF.
4. **Customer experience (X6).** The corpus has no denominators and is dominated by Fidelity app-store reviews. U for NPT, RCF, AEF, GiveClear, GS PF, BofA, NCF, Endaoment, Givinga and Every.org.
5. **Channel split (X1).** Fidelity, DAFgiving360 and Charityvest scale is whole-entity in both areas.
6. **Period.** Several DAFRC FY2024 rows are imputed: AEF, MS GIFT, BofA, NCF, GiveClear and Daffy. Fidelity's FY2024 row has a lagging period_end.

## 6. What would move them

- **Vanguard → plottable.** Any evidence on Y1 (export or API), Y3 or Y4 (adviser program). With Y4 ≥ 2 it would likely sit as a Proven Leader or on the boundary.
- **Fidelity → Proven Leaders.** A documented donor data export or API (Y1 ≥ 2) plus mandatory EFT (Y2 3) would lift Y above 2.0.
- **NPT and DAFgiving360.** Inspected audited statements (X3), and published outbound/history terms (Y5) for NPT. Either could resolve the boundary label.
- **RCF.** An inspected Ren SOC 2 Type II covering RCF would lift X3 to 4. Evidence that Ren's Giving Compass or crypto items were delivered would lift X2.
- **AEF.** Evidence that full history can be exported after the migration would lift Y5. A reconciled SOC report would lift X3.
- **GiveClear.** Documented Louise controls (sponsor approval, limits, audit trail) would lift Y3 from 1 to 3 and clear the red flag.
- **Daffy.** Spend limits or sponsor-side confirmation for MCP donations would lift Y3. A published audit or SOC would score X3. A full-history export right would lift Y1 to 4.
- **GS PF, MS GIFT, BofA, NCF.** Program circulars or guidelines covering transfers, data feeds and grant rails would make them plottable (P-QA3-02 and P-QA3-03).
- **Re-scoring triggers.** New 990s or audits for FY2025, the outcome of the SPLC-halt dispute, the Vanguard–Altruist acquisition, and the GiveClear Direct launch.
