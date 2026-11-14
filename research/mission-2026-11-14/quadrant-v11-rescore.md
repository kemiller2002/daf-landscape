# DAF Evidence Quadrant: v1.1 fresh re-score (queue item Q-N13)

**Date:** 2026-11-14. **Scorer:** `v11`, a fresh scorer working under methodology v1.1 ([evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §7).
**Scores:** `data/mission-2026-11-14/quadrant-scores-A{1..5}-v11.csv` (462 rows, 42 providers).
**Positions:** `quadrant-positions.csv` (rows with scorer `v11`). **Charts:** `quadrants/A{1..5}-v11.svg`.

This is the repository's own method. It is not a Gartner Magic Quadrant. Positions are bands, and they hold only within one area at this date. Under the EDF claim policy every position stays *internal-demonstration* until a second scorer reproduces it.

## 0. Summary

- **Agreement with v1.0.** 30 of 42 providers keep their v1.0 consensus quadrant, ignoring the "boundary" suffix. Of the 12 that change:
  - 7 are boundary-to-boundary moves where a point sits within 0.25 of a midline. Treat these as unchanged.
  - 5 are material: DAFgiving360 in A3 and A4, NPT (A3), Ren RDE (A2) and Givinga (A1). Four of the five come from v1.1 rules or from how unknowns are handled, not from new facts.
- **What the v1.1 rules changed.**
  - The X1 asset table and the rule that a filed return replaces an imputed value change several sponsor X1 scores: BofA drops to 2, GiveClear rises to 1 on filed data, Vanguard rises to 4.
  - The Y5 transfer-terms ladder caps every sponsor with only an inbound transfer page at 1.
  - The entity-scope rule removes vendor evidence (Chariot DAFpay, Ren MSAs, GivingPoint) from sponsor rows.
  - The NPT GivingPoint row is merged into Ren.
- **New evidence this pass.**
  - GiveClear's audited CY2024 statements were read: Capin Crouse, unmodified opinion dated 2025-11-06, giving A3 X3 = 3 ([PDF](https://irp.cdn-website.com/5c4108df/files/uploaded/GiveClear+24+Consolidated+FS+Final.pdf)).
  - Chariot's compliance documents name its sources: BMF, Pub 78, 990s, OFAC/AML and state checks ([Chariot](https://help.givechariot.com/onboarding/compliance-verification/organization-eligibility)).
  - Candid's Charity Check source list was confirmed: BMF, Pub 78, IRB, auto-revocation and OFAC SDN ([Candid FAQ](https://developer.candid.org/docs/faqs-charity-check)).
  - Benevity's validation scope: six countries, BMF good standing, periodic re-review ([Benevity](https://causeshelp.benevity.org/hc/en-us/articles/18579133440532-Benevity-s-validation-requirements-for-nonprofits)).
  - Goodstack's docs show SOC 2 and ISO badges but no data sources, re-validation or customers ([docs](https://docs.goodstack.io/docs/guides/Cause%20verification/)).
- **No provider in any area earns AI overlay GREEN.** One provider is RED (provisional, A5 adjacent): Benevity Match Assurance.

## 1. v1.1 positions

Format: point (low–high band). Coverage is the share of scored weight on X and Y. "b" = boundary (within 0.25 of a midline).

### A1 DAF platform and administration

| Provider | X | Y | Cov X/Y | Quadrant | v1.0 consensus |
|---|---|---|---|---|---|
| Ren (incl. iPhi/Stellar, DonorFirstX) | 3.05 (3.05–3.05) | 2.10 (2.10–2.10) | 1.0/1.0 | Proven Leaders b | Proven Leaders (2.81, 2.33) |
| Fidelity Charitable (in-house, FMR-administered) | 3.18 (2.7–3.3) | 2.07 (1.55–2.55) | 0.85/0.75 | Proven Leaders b | Scale Operators (3.06, 1.57) |
| TIFIN Give | 2.50 | 1.80 | 1.0/1.0 | Scale Operators b | Scale Operators b (2.44, 1.93) |
| Foundation Source (DAF OS / Vennfi) | 2.27 (1.7–2.7) | 2.25 (1.35–2.95) | 0.75/0.6 | Proven Leaders | Proven Leaders b (2.27, 2.03) |
| Blackbaud Financial Edge NXT (foundations) | 2.22 (2.0–2.4) | 2.15 | 0.9/1.0 | Proven Leaders b | Forward Builders b (1.88, 2.09) |
| Foundant CommunitySuite | 2.14 (1.5–2.7) | 2.00 (1.1–2.9) | 0.7/0.55 | Proven Leaders b | Scale Operators b (2.10, 1.90) |
| Give Interactive | 1.89 (1.7–2.1) | 2.25 (1.35–2.95) | 0.9/0.6 | Forward Builders b | Proven Leaders b (2.47, 2.08) |
| NPact (FIMS / DonorCentral) | 1.00 (0.7–1.9) | 0.92 (0.55–2.15) | 0.7/0.6 | Focused Specialists | Focused Specialists (1.50, 1.04) |
| Givinga | 1.36 | 2.00 | 0.55/0.15 | insufficient evidence | Focused Specialists b (1.77, 1.73) |
| NCF (sponsor-built, Salesforce) | 2.27 | 1.00 | 0.55/0.15 | insufficient evidence | insufficient evidence |
| SVCF (sponsor-built, Salesforce) | 2.09 | – | 0.55/0 | insufficient evidence | insufficient evidence |
| *(NPT GivingPoint, merged into Ren)* | – | – | – | – | v1.0 row retired per §7 |

### A2 Grant disbursement and nonprofit-side rails

| Provider | X | Y | Cov | Quadrant | v1.0 consensus |
|---|---|---|---|---|---|
| Chariot Disbursements | 3.10 | 3.65 | 1.0/1.0 | Proven Leaders | Proven Leaders (2.44, 3.17) |
| PayPal Grant Payments | 3.13 (2.35–3.35) | 2.42 (1.45–3.05) | 0.75/0.6 | Proven Leaders | Proven Leaders (2.72, 2.41) |
| Chariot DAFpay | 2.35 | 2.85 | 1.0/1.0 | Proven Leaders | Proven Leaders b (2.20, 2.88) |
| Every.org | 2.36 (1.3–3.1) | 2.82 (2.4–3.0) | 0.55/0.85 | Proven Leaders | Proven Leaders b (2.00, 2.24) |
| Fidelity Charitable EFT (Stripe/ACH) | 3.06 (2.6–3.2) | 1.83 (1.1–2.7) | 0.85/0.6 | Scale Operators b | Scale Operators b (2.90, 1.82) |
| DAF Direct | 1.87 (1.4–2.4) | 1.71 (1.45–2.05) | 0.75/0.85 | Focused Specialists b | Focused Specialists (1.53, 1.47) |
| Ren Rapid Disbursement Engine | 2.17 | 2.37 | 0.9/0.4 | insufficient evidence | Proven Leaders b (2.17, 2.15) |

### A3 Sponsors for the adviser / wealth channel

| Provider | X | Y | Cov | Quadrant | v1.0 consensus |
|---|---|---|---|---|---|
| Renaissance Charitable Foundation | 3.33 (3.0–3.4) | 2.10 | 0.9/1.0 | Proven Leaders b | Proven Leaders b (3.06, 2.15) |
| Vanguard Charitable | 3.25 | 2.08 (1.25–2.85) | 1.0/0.6 | Proven Leaders b | Scale Operators b (2.93, 1.83) |
| Fidelity Charitable | 3.15 | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders b | Scale Operators (3.12, 1.65) |
| Charityvest (adviser programs) | 2.50 | 2.58 (1.55–3.15) | 1.0/0.6 | Proven Leaders | Proven Leaders b (2.10, 2.21) |
| DAFgiving360 | 2.71 (2.3–2.9) | 1.25 (0.75–2.35) | 0.85/0.6 | Scale Operators | Proven Leaders b (3.18, 2.00) |
| AEF | 2.65 (2.25–2.85) | 1.67 (1.0–2.6) | 0.85/0.6 | Scale Operators | Scale Operators (2.47, 1.29) |
| GiveClear | 2.30 | 1.80 | 1.0/1.0 | Scale Operators b | Scale Operators b (2.06, 1.70) |
| NPT | 3.33 (2.5–3.5) | 3.00 (1.2–3.6) | 0.75/0.4 | insufficient evidence | Scale Operators b (3.11, 1.92) |
| NCF | 2.71 | 1.00 | 0.7/0.15 | insufficient evidence | insufficient evidence |
| Goldman Sachs Philanthropy Fund | 2.64 | 1.00 | 0.55/0.15 | insufficient evidence | insufficient evidence |
| Morgan Stanley GIFT | 2.64 | 1.00 | 0.55/0.15 | insufficient evidence | insufficient evidence |
| BofA Charitable Gift Fund | 2.18 | 1.00 | 0.55/0.15 | insufficient evidence | insufficient evidence |

### A4 Consumer and digital-first sponsors

| Provider | X | Y | Cov | Quadrant | v1.0 consensus |
|---|---|---|---|---|---|
| Fidelity Charitable (direct) | 3.15 | 2.07 (1.55–2.55) | 1.0/0.75 | Proven Leaders b | Scale Operators (3.23, 1.65) |
| Daffy | 2.53 (2.15–2.75) | 2.55 | 0.85/1.0 | Proven Leaders | Proven Leaders (2.76, 2.65) |
| Charityvest (direct) | 2.50 | 2.58 (1.55–3.15) | 1.0/0.6 | Proven Leaders | Proven Leaders b (2.15, 2.21) |
| Endaoment | 2.20 (1.65–2.65) | 3.12 (2.5–3.3) | 0.75/0.8 | Proven Leaders b | Proven Leaders b (2.17, 3.00) |
| DAFgiving360 (direct) | 2.71 | 1.25 | 0.85/0.6 | Scale Operators | Proven Leaders b (3.18, 2.00) |
| Every.org | 1.91 (1.05–2.85) | 2.38 (1.55–2.95) | 0.55/0.65 | Forward Builders b | Forward Builders b (1.55, 2.00) |
| Givinga consumer accounts | 1.36 | 2.00 | 0.55/0.15 | insufficient evidence | insufficient evidence |

### A5 Charity eligibility and verification data

| Provider | X | Y | Cov | Quadrant | v1.0 consensus |
|---|---|---|---|---|---|
| IRS BMF / Pub 78 / TEOS (public baseline) | 3.53 | 2.94 | 0.85/0.85 | Proven Leaders | Proven Leaders (3.45, 3.18) |
| Candid (GuideStar APIs / Charity Check) | 3.11 | 3.00 | 0.9/1.0 | Proven Leaders | Proven Leaders (3.03, 2.62) |
| Benevity validation | 2.70 | 2.31 | 1.0/0.8 | Proven Leaders | Proven Leaders b (2.53, 2.17) |
| Chariot verification | 2.65 | 2.65 | 1.0/1.0 | Proven Leaders | Proven Leaders b (2.22, 2.55) |
| Goodstack | 2.00 (1.4–2.6) | 2.12 (1.7–2.5) | 0.7/0.8 | Proven Leaders b | Proven Leaders (2.45, 2.47) |

## 2. Movement against the v1.0 consensus, with reasons

Each driver is tagged: **[R]** a v1.1 rule change, **[E]** new evidence, **[S]** a different scorer reading of the same evidence. **[U]** marks a move caused by scoring a criterion U rather than a low number. Point estimates renormalise over scored weight, so a U can raise a point while widening the band.

**Material moves (quadrant changes that are not boundary-to-boundary)**

1. **DAFgiving360, A3 and A4: Proven Leaders b → Scale Operators.** Y fell from 2.00 to 1.25.
   - [R] Entity scope: v1.0 credited Y1 = 2 and Y2 = 2 to DAFgiving360 from Chariot DAFpay endpoints. P-CON-04 found that no sponsor is publicly live on the provider API and that the named integrations come from integrator pages. Y1 is now U.
   - [R] Y5 ladder: the sponsor has an inbound transfer page only, so Y5 goes from 2 to 1.
   - [S] Y2 = 1: the only rail its 2024 Program Policies document is the mailed check.
   - X also fell, from 3.18 to 2.71. X5 went from 4 to 3 because no audit was read, and X2 from 3 to 2.
2. **NPT, A3: Scale Operators b → insufficient evidence.** Y coverage fell to 0.40.
   - [R] Under §7, GivingPoint is scored under Ren. The "modern APIs" GivingPoint evidence that supported Y1 = 1 now belongs to Ren's row, so Y1 is U.
   - [R] NPT's two-page financial summary scores X3 = U.
   - On the criteria that remain, NPT is strong: X = 3.33, and Y2 = 3 from PayPal electronic grants.
3. **Ren Rapid Disbursement Engine, A2: Proven Leaders b → insufficient evidence.**
   - [S/U] Y1, Y3 and Y5 are scored U. Nothing public documents an RDE API, controls or portability, and v1.0 had inferred these from Ren generally (entity scope).
   - X is unchanged at 2.17.
4. **Givinga, A1: Focused Specialists b → insufficient evidence.** [S/U] Y1, Y2, Y3 and Y5 are U because there are no official docs. X fell to 1.36 [E]: the CY2024 amended Schedule D shows $1.95m of DAF assets, and the foundation has zero employees.
5. **Fidelity Charitable, A1/A3/A4: Scale Operators → Proven Leaders b.** Y moved from about 1.6 to 2.07, but the band (1.55–2.55) still straddles the midline.
   - [S] Y2 = 3 rather than 2. Fidelity's own 2026 Giving Report puts 67% of grants on EFT, which this scorer reads as electronic-first.
   - [S] Y4 = 3.
   - [U] Y1 is U rather than 1. The only export evidence is nonprofit-side Stripe detail, which is not donor data rights.
   - [R] Y5 = 1 (inbound only).
   - Read this as unresolved, not as an upgrade.

**Boundary-to-boundary moves (treat as unchanged)**

- **Vanguard Charitable, A3: Scale Operators b → Proven Leaders b** (Y 1.83 → 2.08).
  - [R] X1 = 4: Schedule D for the year ending June 2024 shows $21.95bn.
  - [S] Y2 = 3 (PayPal electronic grants).
  - [R] Y5 = 1.
- **Give Interactive, A1: Proven Leaders b → Forward Builders b** (X 2.47 → 1.89).
  - [S] X1 = 2: the Vanguard go-live is not observed.
  - [E/V] X5 = 1: The Signatry owns 99% and the partnership lost $2.72m in CY2024.
  - [S] X3 = 2: the SOC 2 report is gated and has no scope.
- **Blackbaud FE NXT, A1: Forward Builders b → Proven Leaders b** (X 1.88 → 2.22). [S] X1 = 2 from 13 sponsors named in 990s. X6 is now U because one record is not a pattern.
- **Foundant, A1: Scale Operators b → Proven Leaders b** (Y 1.90 → 2.00, sitting exactly on the midline).

**Same quadrant, notable criterion shifts**

- **Ren, A1:**
  - [R] Merger: X1 = 4 (27.9% of FY2024 assets including NPT).
  - [S] X2 = 3: the AEF migration was delivered.
  - Y5 = 1: AEF's new portal keeps only two years of history.
- **Chariot Disbursements and Chariot verification:** X3 = 3, read as consistent dated SOC 2 Type 2 report titles. [E] Verification Y2 = 3 now that the sources are named.
- **Charityvest:** [E/S] X6 = 3, from the "95% of checks deposited within 35 days" metric. [S] Y2 = 3 from the Chariot switch. [R] Y5 = 1.
- **GiveClear:** [E] X3 = 3 (audit read). [R] X1 = 1, because the filed $215m replaces the imputed $33m.
- **Goodstack, A5:** [S] X1 and X3 are vendor claims capped at 2. X4 is now U because no customers are named. Still Proven Leaders b.
- **NPact:** Y5 = 0 from positive lock-in evidence (the §2.4 passthrough ban). X3 = 1 because NPact points customers to Azure's SOC reports.
- **A3 X1 under the v1.1 table** (filed returns replace imputed values):

  | Sponsor | FY2024 DAF assets | Basis | X1 |
  |---|---|---|---|
  | AEF | $8.38bn | filed | 3 |
  | MS GIFT | $9.11bn | filed | 3 |
  | RCF | $5.91bn | filed | 3 |
  | NCF | $5.68bn | filed | 3 |
  | BofA | $4.73bn | filed | 2 |
  | GS PWM | $11.84bn | imputed; program's own CY2024 Schedule D says $12.64bn | 3 |

**Calibration-script note.** `mission_quadrant_calibration.py` compares primary with blind only, so v11 does not enter its output. The comparison above was made by hand against the `consensus` rows of `quadrant-positions.csv`, after the v11 scores were written.

## 3. AI-governance overlay (v1.1 vocabulary)

**Vocabulary.**
- **GREEN:** controls documented, including flag-only and authority separation.
- **AMBER:** the capability is live with undocumented limits, but sponsor approval remains.
- **RED:** AI can complete a money-moving or status-clearing action without documented sponsor or human approval.
- **None:** no AI capability is evidenced.

| Area | Provider | Flag | Basis |
|---|---|---|---|
| A1 | TIFIN Give | **AMBER (RED-boundary)** | Louise is claimed to "execute real donor requests". Grants pass the 48-hour GiveClear review. The Louise path, contributions and recurring set-ups have no documented confirmation, limits or logging (AGM-11..20). |
| A1 | Foundant CommunitySuite | AMBER | Fia is in beta, with a "policy engine". It does not move money, and its limits are undocumented. |
| A1 | Blackbaud FE NXT | AMBER | AI agents exist in an adjacent CRM. FE NXT writes go through validate-then-post batches under admin-enabled connections. |
| A1 | Fidelity in-house | None (inform-only) | The website Virtual Assistant handles navigation only. |
| A1 | Ren | None | "Instant approval" is rules-based: RCF policy, with officer review above $500k. It is not AI. |
| A1 | Others | None | No AI capability evidenced. Foundation Source has AI ambitions only. |
| A2 | Chariot Disbursements / DAFpay | AMBER | LLM gift coding runs on the nonprofit side. The DAFpay grant "enters your normal review" (sponsor approval is preserved), but the data model cannot tell an agent-driven session from a human one. |
| A2 | Others | None | |
| A3 | GiveClear | AMBER (RED-boundary) | Same as TIFIN Give: Louise runs on GiveClear programs. |
| A3 | Fidelity Charitable | None (inform-only) | |
| A3 | Others | None | |
| A4 | Daffy | AMBER | The MCP `make_donation` tool is live. Daffy accepts or rejects each donation. There are no scopes, caps or agent identifier, and confirmation is client-side only. |
| A4 | Endaoment | None (AI); watch | No AI product. The API is agent-capable, and the partner "settled grant" path has no documented review step (P-AGA-03). |
| A4 | Every.org | None | The API excludes programmatic donations by design. |
| A5 | Benevity | **RED (provisional)** | Match Assurance uses AI to verify receipt eligibility and auto-submits match requests. No human or company approval step is documented. This is adjacent to, not inside, the validation product. |
| A5 | Candid | AMBER (low) | The MCP connector and AI assistant are read-only (Scalekit lists six read tools), so they cannot clear a status. Candid itself does not document the controls. |
| A5 | Goodstack | AMBER | It claims "AI-powered automation" in verification outcomes, with no documented limits or human step. |
| A5 | Chariot verification, IRS | None | |

## 4. Remaining unknowns (largest effect on positions first)

1. **Sponsor audits not yet read**, so X3 stays U under v1.1:
   - DAFgiving360: financials page returns 403.
   - NPT: only a summary is public.
   - AEF and Daffy: statements available on request only.
   - GS, MS GIFT, BofA: no audit posted.
   - Endaoment: SingerLewak audits FY2022–23 announced, opinion not seen.
   - Reading DAFgiving360's statements would move it within A3 and A4.
2. **No scoped SOC report exists publicly for any A1 vendor or sponsor DAF system.** No X3 = 4 was possible.
3. **Donor-side data rights and outbound transfer terms at every large sponsor.** These drive Y1 = U and Y5 ≤ 1 across A3/A4. They are the main reason Fidelity, Vanguard and DAFgiving360 sit near the Y midline.
4. **Vanguard go-live on Give Interactive.** This would raise Give's X1 to 3 and probably return it to Proven Leaders b.
5. **NCF's Stellar payments** ($2.50m, "software/consulting", FY2024) and the NCF Salesforce portal builder. Under the §7 scope rule, part of NCF's A1 row may belong to Ren at the next re-score.
6. **TIFIN Louise and Benevity Match Assurance action paths.** Documentation would settle AMBER versus RED.
7. **The number of live Chariot DAFpay OAuth or Donor Accounts providers.** None is named.
8. **The Every.org CY2025 Form 990.** It will be the first with Schedule D, giving DAF assets for A4 X1.
9. **A5:** Goodstack's data sources and customers, and Benevity's validation data lineage.

## 5. Independence and limits

- **Files not opened before scoring.** The v11 scores were written before any `quadrant-scores-*`, `quadrant-positions`, `quadrant-calibration*`, `quadrant-*.md` or `quadrants/` file was opened.
- **One exposure.** An early full-repo grep for Every.org scale evidence returned a few lines from `queue-proposals-quadrant-*.csv` and a calibration excerpt. Those lines showed v1.0 Every.org X1 values of 1 or 2 and X5 = 2. The scores here (A2 X1 = 2, A4 X1 = 1 under the v1.1 table, X5 = 2) rest on the 990-PF figures directly. A reviewer may still want to discount Every.org's reproduction.
- **Sources.** All scores cite one primary or validated URL per row. Repository CSV and analysis files are named in `notes` where they carry the reasoning.
- **Scale.** Scores are whole numbers. v1.0 consensus used half-points, so some small moves are rounding.
