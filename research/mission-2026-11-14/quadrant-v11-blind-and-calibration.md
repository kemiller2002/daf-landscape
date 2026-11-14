# DAF Evidence Quadrant v1.1: blind second score, calibration and consensus (2026-11-14)

**Queue item:** Q-N14. **Method:** [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md), including the binding §7 v1.1 area notes. **Scorer label:** `v11blind`; consensus label `v11consensus`. Not affiliated with Gartner; not a Magic Quadrant.

**Independence.** The blind scores were written before any `quadrant-scores-*`, `quadrant-positions.csv`, `quadrant-calibration*`, `queue-proposals-quadrant-*`, `research/.../quadrant-*.md`, `quadrants/` or `mission_quadrant_v11_generator.py` file was opened, and the repo was not grepped for score values. Evidence came from the non-quadrant mission research and data files (vendor-assurance-scope-2026, sponsor-audit-notes, sponsor-governance-990-xml, agentic-control-gap-matrix, vendor-data-rights-matrix, sponsor-transfer-portability-terms, sponsor-grant-payment-policies, announced-vs-delivered, daf-user-complaints-corpus, form990 harvests, relationship-graph edges, ai-use-case-inventory, validation reports). The v11 files were opened only after `quadrant-scores-A{1..5}-v11blind.csv` existed and the engine had been run. During adjudication three items were checked on the live web: GiveClear's CY2024 audit PDF (Capin Crouse, unmodified, dated 2025-11-06), the Signatry Charitable Trust CY2024 Form 990 XML (Schedule R: Give Interactive LLC, `OwnershipPct` 0.99, share of income −$2,791,186), and RCF's Grantmaking Due Diligence Policy (Charity Check reliance; officer review above $500,000). The endaoment.org/institutions page was also fetched; it lists custodians that Endaoment supports, not named partners.

**Files written**
- `data/mission-2026-11-14/quadrant-scores-A{1..5}-v11blind.csv`: 462 rows (42 providers × 11 criteria), `scorer = v11blind`. Every non-U row has a `source_url`.
- `data/mission-2026-11-14/quadrant-calibration-criteria-v11-vs-v11blind.csv` and `quadrant-calibration-providers-v11-vs-v11blind.csv` (from `scripts/mission_quadrant_calibration.py . v11 v11blind`).
- `data/mission-2026-11-14/quadrant-scores-A{1..5}-v11consensus.csv`: 462 rows, `scorer = v11consensus`.
- `quadrant-positions.csv` and `quadrants/A{1..5}-v11blind.svg`, `A{1..5}-v11consensus.svg` (from `scripts/mission_quadrants.py .`).

## 1. How the blind scorer applied v1.1

- **Sponsor X1 (A3/A4):** FY2024 DAF assets, period-aligned. A filed Schedule D replaced the DAFRC value when one existed. Examples: AEF $8.38bn filed (DAFRC imputed $9.48bn), RCF $5.91bn, MS GIFT $9.11bn, NCF $5.68bn, BofA $4.73bn (so it scores 2), GiveClear $215m (imputed $33m), Daffy $334m. Fidelity ($66.2bn), NPT ($42.1bn), DAFgiving360 ($40.9bn) and Vanguard ($21.95bn) use June-2024 values.
- **Sponsor X3:** audited statements read with an opinion scored 3: Fidelity, Vanguard, RCF, NCF, Charityvest. A Form 990 audit indicator alone, NPT's two-page summary, and "on request" statements (AEF, Daffy) scored U. No SOC report covering a sponsor's DAF system is public, so no cell scored 4. Ren's contradictory Type 2 → Type 1 claims scored 1, with the v1.1 rule applied to the vendor too.
- **Sponsor Y5:** every sponsor publishes inbound-only transfer pages, or none at all, so the maximum is 1. AEF is capped at 1 by the two-year history window on its Ren migration. Daffy is held at 1 because tax summaries and receipts become inaccessible after an account closes.
- **Scope and entity rules:** NPT appears in A3 only, and its GivingPoint evidence counts toward Ren. Vendor APIs were not credited to sponsors. A sponsor's audit was not credited to a vendor's SOC. One caution: NCF pays Stellar (Ren) $2.50m for "software/consulting" (FY2024 990 VII-B), so the "sponsor-built" A1 row may partly belong to Ren.

## 2. Blind positions (v11blind)

Point (band). The band sets unknowns to 0 for the low bound and 4 for the high bound. "Boundary" means the point is within 0.25 of a midline.

| Area | Provider | X (band) | Y (band) | Cov X/Y | v11blind quadrant |
|---|---|---|---|---|---|
| A1 | Blackbaud Financial Edge NXT (foundations) | 2.29 (1.60–2.80) | 2.53 (1.90–2.90) | 0.7/0.75 | Proven Leaders |
| A1 | Fidelity Charitable (in-house, FMR-administered) | 3.05 (3.05–3.05) | 1.87 (1.40–2.40) | 1.0/0.75 | Scale Operators (boundary) |
| A1 | Foundant CommunitySuite | 2.64 (1.85–3.05) | 2.00 (0.80–3.20) | 0.7/0.4 | insufficient evidence |
| A1 | Foundation Source (DAF OS / Vennfi) | 2.40 (1.80–2.80) | 2.25 (1.35–2.95) | 0.75/0.6 | Proven Leaders |
| A1 | Give Interactive | 2.67 (2.40–2.80) | 2.12 (1.80–2.40) | 0.9/0.85 | Proven Leaders (boundary) |
| A1 | Givinga | 1.36 (0.75–2.55) | 2.00 (0.80–3.20) | 0.55/0.4 | insufficient evidence |
| A1 | NCF (sponsor-built, Salesforce) | 2.86 (2.00–3.20) | 1.00 (0.15–3.55) | 0.7/0.15 | insufficient evidence |
| A1 | NPact (FIMS / DonorCentral) | 1.00 (0.70–1.90) | 1.00 (0.45–2.65) | 0.7/0.45 | insufficient evidence |
| A1 | Ren (incl. iPhi/Stellar, DonorFirstX) | 2.85 (2.85–2.85) | 2.12 (1.80–2.40) | 1.0/0.85 | Proven Leaders (boundary) |
| A1 | SVCF (sponsor-built, Salesforce) | 2.27 (1.25–3.05) | – (0–4) | 0.55/0 | insufficient evidence |
| A1 | TIFIN Give | 2.50 (2.50–2.50) | 1.65 (1.65–1.65) | 1.0/1.0 | Scale Operators |
| A2 | Chariot DAFpay | 2.20 (2.20–2.20) | 3.00 (3.00–3.00) | 1.0/1.0 | Proven Leaders (boundary) |
| A2 | Chariot Disbursements | 2.50 (2.50–2.50) | 3.40 (3.40–3.40) | 1.0/1.0 | Proven Leaders |
| A2 | DAF Direct | 1.40 (1.05–2.05) | 1.33 (0.80–2.40) | 0.75/0.6 | Focused Specialists |
| A2 | Every.org | 2.00 (1.10–2.90) | 2.29 (1.95–2.55) | 0.55/0.85 | Proven Leaders (boundary) |
| A2 | Fidelity Charitable EFT (Stripe/ACH) | 2.82 (2.40–3.00) | 1.83 (1.10–2.70) | 0.85/0.6 | Scale Operators (boundary) |
| A2 | PayPal Grant Payments | 3.13 (2.35–3.35) | 2.42 (1.45–3.05) | 0.75/0.6 | Proven Leaders |
| A2 | Ren Rapid Disbursement Engine | 2.17 (1.95–2.35) | 1.67 (1.00–2.60) | 0.9/0.6 | Scale Operators (boundary) |
| A3 | AEF | 2.76 (2.35–2.95) | 1.67 (1.00–2.60) | 0.85/0.6 | Scale Operators |
| A3 | BofA Charitable Gift Fund | 2.18 (1.20–3.00) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence |
| A3 | Charityvest (adviser programs) | 2.11 (1.90–2.30) | 2.33 (1.40–3.00) | 0.9/0.6 | Proven Leaders (boundary) |
| A3 | DAFgiving360 | 3.69 (2.40–3.80) | 1.50 (0.90–2.50) | 0.65/0.6 | Scale Operators |
| A3 | Fidelity Charitable | 3.25 (3.25–3.25) | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders (boundary) |
| A3 | GiveClear | 1.91 (1.05–2.85) | 1.87 (1.40–2.40) | 0.55/0.75 | Focused Specialists (boundary) |
| A3 | Goldman Sachs Philanthropy Fund | 2.64 (1.45–3.25) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence |
| A3 | Morgan Stanley GIFT | 2.64 (1.45–3.25) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence |
| A3 | NCF | 2.86 (2.00–3.20) | 2.00 (0.30–3.70) | 0.7/0.15 | insufficient evidence |
| A3 | NPT | 4.00 (2.20–4.00) | 2.75 (1.10–3.50) | 0.55/0.4 | insufficient evidence |
| A3 | Renaissance Charitable Foundation | 3.43 (2.40–3.60) | 1.94 (1.65–2.25) | 0.7/0.85 | Scale Operators (boundary) |
| A3 | Vanguard Charitable | 3.25 (3.25–3.25) | 2.08 (1.25–2.85) | 1.0/0.6 | Proven Leaders (boundary) |
| A4 | Charityvest (direct) | 2.20 (2.20–2.20) | 2.33 (1.40–3.00) | 1.0/0.6 | Proven Leaders (boundary) |
| A4 | DAFgiving360 (direct) | 3.38 (2.20–3.60) | 1.50 (0.90–2.50) | 0.65/0.6 | Scale Operators |
| A4 | Daffy | 2.53 (2.15–2.75) | 2.40 (2.40–2.40) | 0.85/1.0 | Proven Leaders |
| A4 | Endaoment | 1.55 (0.85–2.65) | 3.12 (2.50–3.30) | 0.55/0.8 | Forward Builders |
| A4 | Every.org | 1.55 (0.85–2.65) | 2.38 (1.55–2.95) | 0.55/0.65 | Forward Builders |
| A4 | Fidelity Charitable (direct) | 3.25 (3.25–3.25) | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders (boundary) |
| A4 | Givinga consumer accounts | 1.36 (0.75–2.55) | 2.00 (0.80–3.20) | 0.55/0.4 | insufficient evidence |
| A5 | Benevity validation | 2.45 (2.45–2.45) | 2.00 (1.60–2.40) | 1.0/0.8 | Scale Operators (boundary) |
| A5 | Candid (GuideStar APIs / Charity Check) | 2.83 (2.55–2.95) | 2.40 (2.40–2.40) | 0.9/1.0 | Proven Leaders |
| A5 | Chariot verification | 2.00 (1.40–2.60) | 2.62 (1.05–3.45) | 0.7/0.4 | insufficient evidence |
| A5 | Goodstack | 2.00 (0.70–3.30) | 2.44 (1.95–2.75) | 0.35/0.8 | insufficient evidence |
| A5 | IRS BMF / Pub 78 / TEOS (public baseline) | 3.53 (3.00–3.60) | 3.18 (2.70–3.30) | 0.85/0.85 | Proven Leaders |

## 3. Agreement with v11 (from the calibration CSVs)

Cell-level figures come from `quadrant-calibration-criteria-v11-vs-v11blind.csv` (462 criterion pairs). "Both scored" means neither scorer used U. MAD is the mean absolute difference; bias is the mean of blind minus v11.

| Area | Pairs | Both scored | Both U | Exact | Within 1 | MAD | Bias | Flagged (gap>1 / one-U) |
|---|---|---|---|---|---|---|---|---|
| A1 | 121 | 76 | 36 | 58 (76%) | 76 (100%) | 0.24 | +0.11 | 9 (0 / 9) |
| A2 | 77 | 58 | 17 | 43 (74%) | 58 (100%) | 0.26 | −0.22 | 2 (0 / 2) |
| A3 | 132 | 79 | 44 | 60 (76%) | 78 (99%) | 0.25 | +0.05 | 10 (1 / 9) |
| A4 | 77 | 53 | 21 | 37 (70%) | 53 (100%) | 0.30 | −0.04 | 3 (0 / 3) |
| A5 | 55 | 41 | 7 | 28 (68%) | 41 (100%) | 0.32 | −0.17 | 7 (0 / 7) |
| **All** | **462** | **307** | **125** | **226 (74%)** | **306 (99.7%)** | **0.27** | **−0.03** | **31 (1 / 30)** |

U usage agrees in 432 of 462 cells (93.5%). Only one cell differs by more than 1 point: DAFgiving360 X4 in A3 (v11 2, blind 4).

**Provider level** (`quadrant-calibration-providers-v11-vs-v11blind.csv`, 42 providers):

| Status | Count | Providers |
|---|---|---|
| Reproduced (same base quadrant, both plottable) | **22** | A1: Blackbaud, Foundation Source, Ren, TIFIN Give. A2: Chariot DAFpay, Chariot Disbursements, DAF Direct, Every.org, Fidelity EFT, PayPal. A3: AEF, Charityvest, DAFgiving360, Fidelity, Vanguard. A4: Charityvest, DAFgiving360, Daffy, Every.org, Fidelity. A5: Candid, IRS |
| Disputed (different base quadrant) | **6** | A1 Fidelity in-house, A1 Give Interactive, A3 GiveClear, A3 RCF, A4 Endaoment, A5 Benevity |
| Insufficient evidence in at least one score set | **14** | Both scorers: A1 Givinga, NCF, SVCF; A3 BofA, GS PF, MS GIFT, NCF, NPT; A4 Givinga. One scorer only: A1 Foundant and NPact (blind), A2 Ren RDE (v11), A5 Chariot verification and Goodstack (blind) |

Of the 28 providers that both scorers could plot, 22 were reproduced (79%). Every one of the 6 disputes is a boundary case: at least one scorer placed the provider within 0.25 of a midline, and a single criterion decides each one.

**Sources of disagreement.**
1. **New evidence on the v11 side** that the blind pass did not have: GiveClear's audit, Give Interactive's Schedule R ownership and losses, Foundant's Fia AI beta, Benevity's re-validation help article, RCF's due-diligence policy, Goodstack's SOC 2 and ISO badges, and Chariot's compliance-status API.
2. **Entity-scope readings.** These cover Fidelity's and NCF's audits treated as platform X3, RCF's policy credited to Ren Y3, and the RDE customer base.
3. **Rubric granularity on X4 and Y4.** This is where most of the 1-point gaps sit.

The v1.1 sponsor rules worked. Across A3 and A4, every X1, X3 and Y5 cell matches exactly, except GiveClear X3, where v11 had read the audit and the blind pass had not.

## 4. Adjudications

The rule follows the v1.0 precedent ([quadrant-calibration.md](quadrant-calibration.md) §1):
- **Agreeing cells:** the consensus is the mean of the two effective scores, with the vendor cap applied first, rounded to 0.5.
- **Flagged cells, and every 1-point gap at a disputed or insufficient-evidence provider:** adjudicated on the evidence.

The result is 226 identical cells, 125 cells that both scorers left U, 57 cells set to the mean, and **54 adjudicated cells**.

### 4.1 Disputed providers

- **A1 Fidelity Charitable (in-house).** v11 placed it in Proven Leaders (b) and blind in Scale Operators (b). The decisive cell is Y4.
  - Y4 = 3: the Giving Report and site evidence direct consumers, advisers and corporate/foundation account holders.
  - X3 = U, conceded to v11. The PwC audit is of the Gift Fund, not the FMR platform (entity scope).
  - X2 = 3, conceded to v11. The unimplemented EFT-only date was a Chariot/forum report.
  - X6 = 2, blind. The rubric is relative to scale: about 29 high or critical records against about 3 million grants a year.
  - **Consensus: Proven Leaders (boundary), Y = 2.07.**
- **A1 Give Interactive.** v11 placed it in Forward Builders (b) and blind in Proven Leaders (b). Blind lacked the ownership evidence.
  - X5 = 1. Verified: 99% owned by The Signatry Charitable Trust, with partnership losses of $2.79m in CY2024.
  - X1 = 2: Vanguard's cut-over has not been observed.
  - X4 = 2: only 4 of 14 edges are confirmed.
  - X3 = 2.5: gated SOC 2/SOC 3 and no CPA firm named, set equal to Chariot.
  - Y2 = U: integrations are not evidence of rail redesign.
  - Y5 = 2.
  - **Consensus: Forward Builders (boundary), X = 1.97.** The provider turns to Proven Leaders if the Vanguard go-live is observed (X1 → 3).
- **A3 GiveClear.** v11 placed it in Scale Operators (b) and blind in Focused Specialists (b).
  - X3 = 3: the audit was read and verified (Capin Crouse, unmodified, 2025-11-06).
  - X5 = 3, X6 = 3 (AssetMark median of 2 days), Y4 = 3 (RIA, bank/trust, faith-wealth and single-charity programs), Y1 = 1 (TIFIN terms bind program users).
  - **Consensus: Scale Operators (boundary), X = 2.30, Y = 1.80.**
- **A3 RCF.** v11 placed it in Proven Leaders (b) and blind in Scale Operators (b).
  - Y3 = 3. Verified: RCF's own Grantmaking Due Diligence Policy relies on Charity Check (with OFAC) for routine grants and requires officer review above $500k. That is sponsor-documented automation with authority separation, so it is admissible for RCF but not for Ren.
  - X2 = 3: its partner programs are live.
  - **Consensus: Proven Leaders (boundary), Y = 2.10.**
- **A4 Endaoment.** v11 placed it in Proven Leaders (b) and blind in Forward Builders. The decisive cell is X4.
  - X4 = 2, blind. Altruist is the only confirmed channel edge. The institutions page fetched on 2026-11-14 lists supported custodians, not partners.
  - X2 = 3, Y1 = 3 (public API, no documented export or portability rights) and Y2 = 4 (onchain state tracking).
  - **Consensus: Forward Builders (boundary), X = 1.93.** It turns if a second named channel partner is documented.
- **A5 Benevity validation.** v11 placed it in Proven Leaders and blind in Scale Operators (b). The decisive cell is Y2.
  - Y2 = 3: a first-party help article documents periodic re-review and annual cross-border renewal.
  - X1 = 3, blind: large, but not shown to dominate the IRS baseline or Candid.
  - **Consensus: Proven Leaders, Y = 2.31.**

### 4.2 Providers that only one scorer could plot

- **Foundant:** v11's Fia AI beta (Y3 = 2 vendor_claim) lifts Y coverage to 0.55. **Proven Leaders (b).**
- **NPact:** NPact Y4 = 2 (community foundations plus AEF, historic) and Y5 = 0 (§2.4 ban, remaining-term fees, deletion after 10 days). **Focused Specialists.**
- **Ren RDE:** Y5 = 1, blind. The payments page shows RDE pays on each institution's own rails, so there is no shared nonprofit network. Y4 = 2 (entity scope). **Scale Operators (b).**
- **Chariot verification:** v11's first-party compliance docs, status API and AssetMark timing fill X2, X6, Y1, Y3 and Y5. **Proven Leaders.**
- **Goodstack:** product docs and badges fill X2 and X3. **Proven Leaders (b), low confidence**: X1 and X3 rest on vendor claims and X4 is U.

### 4.3 Every adjudicated cell

| Area | Provider | Crit | v11 | v11blind | **Consensus** | Reason | Evidence |
|---|---|---|---|---|---|---|---|
| A1 | Blackbaud Financial Edge NXT (foundations) | X2 | 2 | U | **2** | Company-level delivery (Agents for Good GA 2026-03) admissible as mixed delivery record | [source](https://www.blackbaud.com/newsroom) |
| A1 | Blackbaud Financial Edge NXT (foundations) | Y2 | 1 | U | **1** | Connector docs show a ledger with no grant rails or eligibility features: positive evidence for 1 | [source](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera) |
| A1 | Fidelity Charitable (in-house, FMR-administered) | X2 | 3 | 2 | **3** | EFT program delivered (67% of grants); the unimplemented EFT-only date was reported by Chariot/forum, not by a Fidelity page | [source](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) |
| A1 | Fidelity Charitable (in-house, FMR-administered) | X3 | U | 3 | **U** | Entity scope: PwC audit covers the Gift Fund, not FMR/National Charitable Services' platform controls; no SOC public | [source](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf) |
| A1 | Fidelity Charitable (in-house, FMR-administered) | X6 | 1 | 2 | **2** | Rubric is relative to scale: ~29 high/critical records against ~3m grants/yr is a mixed signal, not a severe pattern | [source](https://apps.apple.com/us/app/fidelity-charitable/id552407907) |
| A1 | Fidelity Charitable (in-house, FMR-administered) | Y4 | 3 | 2 | **3** | Giving Report and site evidence direct consumers, Fidelity/UBS advisers and corporate/foundation account holders: three segments | [source](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) |
| A1 | Foundant CommunitySuite | Y3 | 2 | U | **2** | Fia AI platform beta (agents, policy engine) announced 2026-09; vendor_claim cap | [source](https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizatio) |
| A1 | Give Interactive | X1 | 2 | 3 | **2** | Only Signatry and WaterStone are observed live; Vanguard cut-over not observed and absent from FY2026 audit | [source](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html) |
| A1 | Give Interactive | X3 | 2 | 3 | **2.5** | Both SOC 2 Type 2 and SOC 3 gated; issuance corroborated by consultant BD Emerson but no CPA firm named; set equal to Chariot (dated titles, no auditor) | [source](https://trust.giveinteractive.com/resources) |
| A1 | Give Interactive | X4 | 2 | 3 | **2** | Only 4 of 14 edges confirmed | [source](https://api.certspotter.com/v1/issuances?domain=giveinteractive.com&include_subdomains=true&expand=dns_names) |
| A1 | Give Interactive | X5 | 1 | 2 | **1** | Verified in Signatry Charitable Trust CY2024 Schedule R XML: Give Interactive LLC 99% owned, share of income -$2,791,186 | [source](https://projects.propublica.org/nonprofits/organizations/825070897/202543189349315279/full) |
| A1 | Give Interactive | Y1 | 2 | 1 | **2** | Vendor self-claim of 'open API platform' admissible as vendor_claim (cap 2) | [source](https://www.giveinteractive.com/) |
| A1 | Give Interactive | Y2 | U | 2 | **U** | Integrations (Stripe, Plaid) do not evidence rails or eligibility redesign | [source](https://www.giveinteractive.com/) |
| A1 | Give Interactive | Y5 | 2 | 3 | **2** | Migrations onto Give documented, but no history-export or outbound transition terms | [source](https://waterstone.org/login/) |
| A1 | Givinga | Y2 | U | 2 | **U** | Prefunded wallets are not rails/eligibility redesign evidence | — |
| A1 | NCF (sponsor-built, Salesforce) | X3 | U | 3 | **U** | Entity scope, same treatment as Fidelity in-house | [source](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf) |
| A1 | NPact (FIMS / DonorCentral) | Y4 | 2 | U | **2** | Community foundations (FIMS lineage) plus a national sponsor (AEF, historic) | [source](https://www.aefonline.org/wp-content/uploads/2025/01/2023-AEF-990-Public-Disclosure.pdf) |
| A1 | NPact (FIMS / DonorCentral) | Y5 | 0 | 1 | **0** | §2.4 third-party ban, remaining-term fees on termination, deletion after 10 business days: lock-in signals | [source](https://npact.com/software-as-a-service-license-and-services-standard-terms/) |
| A1 | Ren (incl. iPhi/Stellar, DonorFirstX) | Y3 | 2 | U | **U** | Entity scope (v1.1): RCF's due-diligence policy is sponsor evidence and does not document Ren's automation controls | — |
| A2 | DAF Direct | Y1 | 1 | U | **1** | Terms assert widget ownership; no API: positive evidence | [source](https://www.dafdirect.org/popups/userAgreementPopUp.html) |
| A2 | Ren Rapid Disbursement Engine | Y4 | 3 | 2 | **2** | Entity scope: only AEF/RCF use of RDE is evidenced, not all Ren clients | [source](https://www.reninc.com/payments/) |
| A2 | Ren Rapid Disbursement Engine | Y5 | U | 1 | **1** | Payments page: RDE pays on each institution's own bank rails, so nonprofits enrol per sponsor (no shared network) | [source](https://www.reninc.com/payments/) |
| A3 | Charityvest (adviser programs) | X6 | 3 | U | **3** | Entity-level metric '95% of checks deposited within 35 days' applies to all Charityvest grants | [source](https://guide.charityvest.org/for-donors/getting-started/grants-to-charity.md) |
| A3 | DAFgiving360 | X2 | 2 | U | **2** | Rebrand delivered; no EFT option documented | [source](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) |
| A3 | DAFgiving360 | X4 | 2 | 4 | **3** | 7 confirmed graph edges incl. Schwab brokerage/RIA administration (Schedule L), DAF Direct and DAFpay: more than 'some' but fewer named channel partners than RCF/NPT | [source](https://www.dafdirect.org/about-daf-direct/index.html) |
| A3 | GiveClear | X2 | 2 | U | **2** | SEI launched; GiveClear Direct not yet launched | [source](https://www.giveclear.org/reports-and-financials) |
| A3 | GiveClear | X3 | 3 | U | **3** | Verified: Capin Crouse unmodified opinion on CY2024 consolidated statements dated 2025-11-06 (read) | [source](https://irp.cdn-website.com/5c4108df/files/uploaded/GiveClear+24+Consolidated+FS+Final.pdf) |
| A3 | GiveClear | X5 | 3 | 2 | **3** | Now audited; young but diversified programs | [source](https://irp.cdn-website.com/5c4108df/files/uploaded/GiveClear+24+Consolidated+FS+Final.pdf) |
| A3 | GiveClear | X6 | 3 | U | **3** | AssetMark Charitable median 2 days submission-to-funds (TIFIN/GiveClear-administered program) | [source](https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check) |
| A3 | GiveClear | Y1 | 1 | U | **1** | TIFIN terms on the program help center bind GiveClear program users and restrict downloads/automated access | [source](https://intercom.help/give-ria/en/articles/10092486-terms-of-use) |
| A3 | GiveClear | Y4 | 3 | 2 | **3** | Program list includes RIA, bank/trust (SEI, Zions), faith-based wealth (Blue Trust), single-charity funds | [source](https://www.giveclear.org/reports-and-financials) |
| A3 | NPT | X2 | 3 | U | **3** | PayPal Grant Payments (2022) delivered; GivingPoint live | [source](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf) |
| A3 | NPT | Y2 | 3 | 2 | **3** | PayPal electronic with 14-day check fallback, same treatment as Vanguard | [source](https://www.nptrust.org/wp-content/uploads/2022/08/Grant-Payments-NPT.pdf) |
| A3 | Renaissance Charitable Foundation | X2 | 3 | U | **3** | Programs announced with partners are live across 16+ channels | [source](https://www.reninc.com/rcf-daf/) |
| A3 | Renaissance Charitable Foundation | Y3 | 3 | U | **3** | Verified: RCF Grantmaking Due Diligence Policy relies on Charity Check (incl. OFAC) for routine grants; officer review above $500k (authority separation) | [source](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf) |
| A4 | DAFgiving360 (direct) | X2 | 2 | U | **2** | As A3 | [source](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) |
| A4 | Endaoment | X2 | 3 | U | **3** | Public API, partner tiers and Altruist program delivered | [source](https://docs.endaoment.org/llms.txt) |
| A4 | Endaoment | X4 | 3 | 2 | **2** | Only Altruist is a confirmed channel edge; endaoment.org/institutions (fetched 2026-11-14) lists supported custodians, not named partners | [source](https://altruist.com/donor-advised-funds/) |
| A4 | Endaoment | Y1 | 3 | 4 | **3** | Public API but no documented portability/export rights: 3 (as Chariot) | [source](https://docs.endaoment.org/llms.txt) |
| A4 | Endaoment | Y2 | 4 | 3 | **4** | Onchain recordkeeping gives state tracking visible beyond the sponsor | [source](https://docs.endaoment.org/advisors/about/platform-recordkeeping.md) |
| A4 | Givinga consumer accounts | Y2 | U | 2 | **U** | As A1 | — |
| A5 | Benevity validation | X1 | 4 | 3 | **3** | AOGF $1.39bn grants plus 2.5m validated nonprofits is large but not shown dominant over IRS/Candid | [source](https://benevity.com/press-releases/benevity-integrates-global-nonprofit-network-with-anthropics-claude) |
| A5 | Benevity validation | Y2 | 3 | 2 | **3** | First-party help centre documents periodic re-review and annual cross-border renewal | [source](https://causeshelp.benevity.org/hc/en-us/articles/18579133440532-Benevity-s-validation-requirements-for-nonprofits) |
| A5 | Chariot verification | X2 | 3 | U | **3** | Eligibility docs and statuses live | [source](https://help.givechariot.com/onboarding/compliance-verification/organization-eligibility) |
| A5 | Chariot verification | X3 | 3 | 2 | **2.5** | Same Chariot entity SOC 2 Type 2 titles as A2 | [source](https://trust.givechariot.com/) |
| A5 | Chariot verification | X4 | 3 | 2 | **3** | Applied across 18+ network partners | [source](https://help.givechariot.com/disbursements/for-nonprofits.md) |
| A5 | Chariot verification | X6 | 3 | U | **3** | Verification 1-3 business days; median 2 days (AssetMark) | [source](https://intercom.help/assetmark-help-center/en/articles/13931838-how-grant-payments-are-delivered-electronic-check) |
| A5 | Chariot verification | Y1 | 3 | U | **3** | Compliance statuses exposed via public API | [source](https://docs.givechariot.com/v2026-04-01/guides/oauth.md) |
| A5 | Chariot verification | Y3 | 2 | U | **2** | Automated screening evidenced; no AI in verification | [source](https://help.givechariot.com/onboarding/compliance-verification/organization-eligibility) |
| A5 | Chariot verification | Y4 | 3 | 2 | **3** | Partners span national, community, faith, consumer | [source](https://help.givechariot.com/disbursements/for-nonprofits.md) |
| A5 | Chariot verification | Y5 | 2 | U | **2** | Results consumable via API; proprietary database | [source](https://docs.givechariot.com/v2026-04-01/guides/oauth.md) |
| A5 | Goodstack | X2 | 2 | U | **2** | Verification product documented | [source](https://docs.goodstack.io/docs/guides/Cause%20verification/) |
| A5 | Goodstack | X3 | 2 | U | **2** | SOC 2 / ISO 27001 badges on docs, no scope (vendor_claim) | [source](https://docs.goodstack.io/docs/guides/Cause%20verification/) |
| A5 | Goodstack | Y2 | 2 | 3 | **2** | No continuous re-validation documented | [source](https://docs.goodstack.io/docs/guides/Cause%20verification/) |

## 5. v1.1 consensus positions (scorer = v11consensus)

Status definitions:
- **reproduced:** v11 and v11blind share the base quadrant and the consensus agrees.
- **adjudicated:** the consensus is plottable, but the scorers differed or one of them could not plot the provider.
- **insufficient evidence:** consensus coverage is below 0.5 on an axis.

Positions are bands, not ranks. They are internal-demonstration claims, bounded to each area and to 2026-11-14. Rows are sorted by X.

#### A1

| Provider | X (band) | Y (band) | Cov X/Y | v1.1 consensus quadrant | v11 / v11blind | Status | AI overlay |
|---|---|---|---|---|---|---|---|
| Fidelity Charitable (in-house, FMR-administered) | 3.29 (2.80–3.40) | 2.07 (1.55–2.55) | 0.85/0.75 | Proven Leaders (boundary) | Proven Leaders (boundary) / Scale Operators (boundary) | adjudicated | None (inform-only) |
| Ren (incl. iPhi/Stellar, DonorFirstX) | 2.95 (2.95–2.95) | 2.12 (1.80–2.40) | 1.0/0.85 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | reproduced | None |
| NCF (sponsor-built, Salesforce) | 2.55 (1.40–3.20) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| TIFIN Give | 2.50 (2.50–2.50) | 1.73 (1.73–1.73) | 1.0/1.0 | Scale Operators | Scale Operators (boundary) / Scale Operators | reproduced | AMBER (RED-boundary) |
| Foundant CommunitySuite | 2.39 (1.68–2.88) | 2.00 (1.10–2.90) | 0.7/0.55 | Proven Leaders (boundary) | Proven Leaders (boundary) / insufficient evidence | adjudicated | AMBER |
| Foundation Source (DAF OS / Vennfi) | 2.33 (1.75–2.75) | 2.25 (1.35–2.95) | 0.75/0.6 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | None |
| Blackbaud Financial Edge NXT (foundations) | 2.22 (2.00–2.40) | 2.15 (2.15–2.15) | 0.9/1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders | reproduced | AMBER |
| SVCF (sponsor-built, Salesforce) | 2.18 (1.20–3.00) | – (0–4) | 0.55/0 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| Give Interactive | 1.97 (1.78–2.18) | 2.25 (1.35–2.95) | 0.9/0.6 | Forward Builders (boundary) | Forward Builders (boundary) / Proven Leaders (boundary) | adjudicated | None |
| Givinga | 1.36 (0.75–2.55) | 2.00 (0.30–3.70) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| NPact (FIMS / DonorCentral) | 1.00 (0.70–1.90) | 0.92 (0.55–2.15) | 0.7/0.6 | Focused Specialists | Focused Specialists / insufficient evidence | adjudicated | None |

#### A2

| Provider | X (band) | Y (band) | Cov X/Y | v1.1 consensus quadrant | v11 / v11blind | Status | AI overlay |
|---|---|---|---|---|---|---|---|
| PayPal Grant Payments | 3.13 (2.35–3.35) | 2.42 (1.45–3.05) | 0.75/0.6 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | None |
| Fidelity Charitable EFT (Stripe/ACH) | 2.94 (2.50–3.10) | 1.83 (1.10–2.70) | 0.85/0.6 | Scale Operators (boundary) | Scale Operators (boundary) / Scale Operators (boundary) | reproduced | None |
| Chariot Disbursements | 2.80 (2.80–2.80) | 3.52 (3.52–3.52) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER |
| Chariot DAFpay | 2.28 (2.28–2.28) | 2.92 (2.92–2.92) | 1.0/1.0 | Proven Leaders | Proven Leaders / Proven Leaders (boundary) | reproduced | AMBER |
| Every.org | 2.18 (1.20–3.00) | 2.56 (2.17–2.77) | 0.55/0.85 | Proven Leaders (boundary) | Proven Leaders / Proven Leaders (boundary) | reproduced | None |
| Ren Rapid Disbursement Engine | 2.17 (1.95–2.35) | 1.67 (1.00–2.60) | 0.9/0.6 | Scale Operators (boundary) | insufficient evidence / Scale Operators (boundary) | adjudicated | None |
| DAF Direct | 1.63 (1.23–2.23) | 1.47 (1.25–1.85) | 0.75/0.85 | Focused Specialists | Focused Specialists (boundary) / Focused Specialists | reproduced | None |

#### A3

| Provider | X (band) | Y (band) | Cov X/Y | v1.1 consensus quadrant | v11 / v11blind | Status | AI overlay |
|---|---|---|---|---|---|---|---|
| NPT | 3.53 (2.65–3.65) | 3.19 (1.27–3.67) | 0.75/0.4 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| Renaissance Charitable Foundation | 3.33 (3.00–3.40) | 2.10 (2.10–2.10) | 0.9/1.0 | Proven Leaders (boundary) | Proven Leaders (boundary) / Scale Operators (boundary) | adjudicated | None |
| Vanguard Charitable | 3.25 (3.25–3.25) | 2.08 (1.25–2.85) | 1.0/0.6 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | reproduced | None |
| Fidelity Charitable | 3.20 (3.20–3.20) | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | reproduced | None (inform-only) |
| DAFgiving360 | 3.00 (2.55–3.15) | 1.38 (0.82–2.42) | 0.85/0.6 | Scale Operators | Scale Operators / Scale Operators | reproduced | None |
| NCF | 2.79 (1.95–3.15) | 1.50 (0.22–3.62) | 0.7/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| AEF | 2.71 (2.30–2.90) | 1.67 (1.00–2.60) | 0.85/0.6 | Scale Operators | Scale Operators / Scale Operators | reproduced | None |
| Goldman Sachs Philanthropy Fund | 2.64 (1.45–3.25) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| Morgan Stanley GIFT | 2.64 (1.45–3.25) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |
| Charityvest (adviser programs) | 2.35 (2.35–2.35) | 2.46 (1.48–3.08) | 1.0/0.6 | Proven Leaders | Proven Leaders / Proven Leaders (boundary) | reproduced | None |
| GiveClear | 2.30 (2.30–2.30) | 1.80 (1.80–1.80) | 1.0/1.0 | Scale Operators (boundary) | Scale Operators (boundary) / Focused Specialists (boundary) | adjudicated | AMBER (RED-boundary) |
| BofA Charitable Gift Fund | 2.18 (1.20–3.00) | 1.00 (0.15–3.55) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |

#### A4

| Provider | X (band) | Y (band) | Cov X/Y | v1.1 consensus quadrant | v11 / v11blind | Status | AI overlay |
|---|---|---|---|---|---|---|---|
| Fidelity Charitable (direct) | 3.20 (3.20–3.20) | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders (boundary) | Proven Leaders (boundary) / Proven Leaders (boundary) | reproduced | None (inform-only) |
| DAFgiving360 (direct) | 2.88 (2.45–3.05) | 1.38 (0.82–2.42) | 0.85/0.6 | Scale Operators | Scale Operators / Scale Operators | reproduced | None |
| Daffy | 2.53 (2.15–2.75) | 2.48 (2.48–2.48) | 0.85/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER |
| Charityvest (direct) | 2.35 (2.35–2.35) | 2.46 (1.48–3.08) | 1.0/0.6 | Proven Leaders | Proven Leaders / Proven Leaders (boundary) | reproduced | None |
| Endaoment | 1.93 (1.45–2.45) | 3.12 (2.50–3.30) | 0.75/0.8 | Forward Builders (boundary) | Proven Leaders (boundary) / Forward Builders | adjudicated | None (watch: agent-capable API) |
| Every.org | 1.73 (0.95–2.75) | 2.38 (1.55–2.95) | 0.55/0.65 | Forward Builders | Forward Builders (boundary) / Forward Builders | reproduced | None |
| Givinga consumer accounts | 1.36 (0.75–2.55) | 2.00 (0.30–3.70) | 0.55/0.15 | insufficient evidence | insufficient evidence / insufficient evidence | insufficient evidence | None |

#### A5

| Provider | X (band) | Y (band) | Cov X/Y | v1.1 consensus quadrant | v11 / v11blind | Status | AI overlay |
|---|---|---|---|---|---|---|---|
| IRS BMF / Pub 78 / TEOS (public baseline) | 3.53 (3.00–3.60) | 3.06 (2.60–3.20) | 0.85/0.85 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | None |
| Candid (GuideStar APIs / Charity Check) | 2.97 (2.68–3.08) | 2.70 (2.70–2.70) | 0.9/1.0 | Proven Leaders | Proven Leaders / Proven Leaders | reproduced | AMBER (low) |
| Chariot verification | 2.58 (2.58–2.58) | 2.65 (2.65–2.65) | 1.0/1.0 | Proven Leaders | Proven Leaders / insufficient evidence | adjudicated | None |
| Benevity validation | 2.45 (2.45–2.45) | 2.31 (1.85–2.65) | 1.0/0.8 | Proven Leaders | Proven Leaders / Scale Operators (boundary) | adjudicated | RED (provisional) |
| Goodstack | 2.00 (1.40–2.60) | 2.12 (1.70–2.50) | 0.7/0.8 | Proven Leaders (boundary) | Proven Leaders (boundary) / insufficient evidence | adjudicated | AMBER |

**Totals:** 22 reproduced, 11 adjudicated, 9 insufficient evidence (42 providers). Under the method's two-scorer rule, the 22 reproduced quadrant assignments are no longer single-scorer. They have been reproduced by an independent scorer, but they remain *internal-demonstration* claims under the EDF claim policy, because both scorers drew on the same evidence base.

## 6. AI-governance overlay (v1.1 vocabulary)

Flags:
- **GREEN:** controls documented, including flag-only and authority separation.
- **AMBER:** live capability with undocumented limits; sponsor approval remains.
- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval.
- **None:** no AI capability is evidenced. This is not evidence of absence.

The blind and v11 overlays agreed on TIFIN Give / GiveClear (AMBER, RED-boundary), Blackbaud (AMBER), Chariot (AMBER), Daffy (AMBER), Goodstack (AMBER) and Benevity (RED, provisional). Four differences were adjudicated:

| Provider | v11 | Blind | Consensus | Reason |
|---|---|---|---|---|
| Fidelity Charitable (A1, A3, A4) | None (inform-only) | GREEN | **None (inform-only)** | A navigation-only assistant with a disclaimer is not a documented flag-only or authority-separation control. |
| Candid | AMBER (low) | GREEN | **AMBER (low)** | Read-only is documented by a third party (Scalekit), not by Candid. |
| Endaoment | None (watch) | AMBER | **None (watch)** | No AI product. The agent-capable API, and a partner "settled grant" path with no documented review, are automation risks, not AI. |
| Foundant | AMBER | None | **AMBER** | Fia beta (agents, "policy engine") was not in the blind evidence. |

**No provider earns GREEN.** The only RED is Benevity Match Assurance: AI verifies receipt eligibility and auto-submits, and no approval step is documented. It is adjacent to the validation product, so the flag is provisional. TIFIN Louise is the main RED-boundary case: it "executes real donor requests", but GiveClear's 48-hour review remains.

## 7. Limits and reconsideration triggers

- **Shared evidence.** Both scorers drew on the same repository. Reproduction shows that the rubric readings are consistent, not that the facts are correct.
- **Most-sensitive cells.** These are the cells that could move a provider across a quadrant line:
  - Give Interactive X1: Vanguard go-live.
  - Endaoment X4: a second named partner.
  - Fidelity A1 Y4.
  - RCF Y3.
  - Benevity Y2.
  - GiveClear Y4.
- **Insufficient-evidence sponsors.** NPT, GS PF, MS GIFT, BofA and NCF need Y-axis evidence. Their sponsor Y1, Y2 and Y5 are mostly U under the entity-scope rule.
- **Re-score triggers** (methodology §5):
  - DAFgiving360, NPT, AEF or Daffy audited statements become readable (X3).
  - Vanguard's FY2026 990 shows Give Interactive.
  - Any sponsor publishes outbound transfer terms with a history export (Y5 > 1).
  - TIFIN or Benevity documents its AI action path (AMBER vs RED).
