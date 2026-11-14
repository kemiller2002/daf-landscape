# Evidence Quadrant A2 and A5: blind second-scorer rationale

**Date:** 2026-11-14. **Scorer:** `blind`. **Method:** [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) v1.0, applied as written.
**Status:** internal-demonstration. Adjudication against the primary scorer belongs in `quadrant-calibration.md`.

**Independence.** I did not open these files: the primary A2/A5 score files, `quadrant-positions.csv` (before my scores existed), `quadrant-A2-A5-rationale.md`, the quadrant SVGs, or the excluded research and data files. Those exclusions include the relationship graph edges and their additions, announced-vs-delivered, receipt cost by rail, the data-rights matrix, agentic controls, the complaints corpus and the queue-proposal files. As a result:
- **X2** (delivery) was scored from dated launches and follow-on customer use, not from `announced-vs-delivered.csv`.
- **X4** (channels) was scored from named partner pages, not from the edge graph.
- **Y1** (openness) was scored from public API docs only. Contractual export rights were not reviewed.
- **X6** (customer experience) is mostly **U**, because I excluded the complaint corpus.

Score files:
- `data/mission-2026-11-14/quadrant-scores-A2-blind.csv`
- `data/mission-2026-11-14/quadrant-scores-A5-blind.csv`

Rendered charts: `quadrants/A2-blind.svg` and `quadrants/A5-blind.svg`.

## Positions (from `scripts/mission_quadrants.py`)

| Area | Provider | X (band) | Y (band) | Coverage X/Y | Quadrant |
|---|---|---|---|---|---|
| A2 | Fidelity Charitable EFT (Stripe/ACH) | 3.06 | 1.59 | 0.85/0.85 | Scale Operators |
| A2 | PayPal Grant Payments | 2.83 | 2.53 | 0.90/0.85 | Proven Leaders |
| A2 | Chariot Disbursements | 2.44 (2.2–2.6) | 3.40 | 0.90/1.00 | Proven Leaders |
| A2 | Chariot DAFpay | 2.44 (2.2–2.6) | 3.00 | 0.90/1.00 | Proven Leaders |
| A2 | Every.org | 2.27 | 2.53 | 0.75/0.85 | Proven Leaders (weak; X near midline) |
| A2 | Ren Rapid Disbursement Engine | 2.17 | 2.15 | 0.90/1.00 | Proven Leaders (boundary) |
| A2 | DAF Direct | 1.73 (1.3–2.3) | 1.24 | 0.75/0.85 | Focused Specialists |
| A5 | IRS BMF/Pub 78/TEOS | 3.53 | 3.41 | 0.85/0.85 | Proven Leaders |
| A5 | Candid | 2.87 | 2.60 | 0.75/1.00 | Proven Leaders |
| A5 | Benevity validation | 2.73 | 2.31 | 0.75/0.80 | Proven Leaders |
| A5 | Goodstack | 2.65 | 2.62 | 1.00/0.80 | Proven Leaders |
| A5 | Chariot verification | 2.22 | 2.55 | 0.90/1.00 | Proven Leaders (boundary) |

Exact bands are in `quadrant-positions.csv` (rows where scorer is `blind`).

## A2 judgement calls

- **Fidelity EFT is a scale operator.** Its scale is primary evidence: more than $18.3bn granted to about 227,000 charities in 2025 ([Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)). The rail itself is closed:
  - It has no nonprofit API.
  - Remittance arrives only through a Stripe dashboard or emailed reports.
  - It serves a single sponsor.

  Fidelity's "digital-first" transition counts toward Y2 (3). Chariot reports that Fidelity planned an electronic-only switch in July 2026, but Fidelity's live FAQ does not confirm it, so X2 is held at 3.
- **PayPal Grant Payments.** It was announced in 2022 with NPT and Vanguard, and Vanguard went live in 2023 as planned, with more than $100M paid to over 400 charities. Two Y criteria score well:
  - **Y2 = 3:** the charity sees each grant's state (accept, decline, expired) along with the grant letter.
  - **Y5 = 3:** it is a multi-grantmaker rail.

  Two points limit the score:
  - **X3 = 2:** the only assurance evidence is PayPal's entity-level audited ICFR, with no product-scoped report.
  - **X5 = 3:** Charityvest moved from PayPal to Chariot in August 2026, the one observed churn in this area.
- **Chariot Disbursements has the highest Y in A2 (3.40).** Its Y4 of 4 rests on named grantmakers across wealth, consumer, workplace, community-foundation and Founders Pledge channels. Its Y2 of 4 rests on electronic-first delivery with recipient verification and state shared with the nonprofit. X is held down by three things:
  - The SOC 2 claim is vendor-only, which caps X3 at 2.
  - It is a 2022-founded Series A company (X5 = 2).
  - Its strongest volume evidence is Daffy's figure of more than $380M paid electronically, which is a mid-tier footprint (X1 = 2).
- **Chariot DAFpay.** Its scale figures are vendor claims ("100,000+ nonprofits", "1,200+ DAFs"), so X1 is capped at 2. Y3 = 3 because sponsor authority over grants is set out in the provider addendum. Chariot screens eligibility and the sponsor decides, which matches the "flag, never clear" rule. One unresolved risk: when a nonprofit has not claimed its account, the DAFpay Network takes legal control of the funds.
- **Ren RDE.** Volume figures (about 1.7M grants a year) appear only on Ren's own page, so they are treated as vendor claims. X3 = 1 because Ren's own SOC 2 statements contradict each other: Type II in 2025, Type I in 2026. Bank-API automation is still listed as roadmap. Y1 = 1 because no public API schema exists. Its distinctive feature is paying from the sponsor's own bank account, which scores Y2 = 3.
- **Every.org.** X1 = 2 comes from its 990-PF: $47.3M in charitable disbursements for 2024. It has an open API (Y1 = 3), but disbursement is batched and slow (Y2 = 2). Its X sits barely above the midline, and its in-scope DAF function is thin. Treat its Proven Leaders placement as fragile.
- **DAF Direct.** It is a three-sponsor widget (Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable). The site footer still reads 2013, and the Chronicle reported in 2015 that adoption had stalled. Fidelity's 2026 FAQ still mentions it, so it is not scored as discontinued.

## A5 judgement calls

- **The IRS baseline leads on both axes, as a public statutory source should.** X6 = 2 and Y2 = 2 reflect real limits:
  - Churches are missing from Pub 78.
  - Listings use legal names, not DBAs.
  - Data is monthly snapshots, not events.
  - A negative lookup does not mean a charity is ineligible.
- **Candid.** X1 = 3 rests on RCF's policy that Charity Check is adequate for more than 98% of its grants (confirmed as V2A-23). X5 = 2 because the reported 2026 staff cuts cannot be verified. Y2 = 2 because Charity Check is a per-lookup snapshot with no field recording when the revocations file was last processed.
- **Benevity.** Y2 = 3 for daily watchlist screening, deactivation, and an appeals process during which disbursements are paused. Its AI evidence is a vendor claim (Y3 = 2), and Y5 is U.
- **Goodstack.** Google's own help page confirms Google uses it, which corroborates the vendor's 7.5M-verification claim to X1 = 3. It is not wired into DAF workflows (Y4 = 2).
- **Chariot verification.** Y3 = 3 because its screening is input only and the DAF provider makes the decision. Y5 = 2 because two of its six data sources are undisclosed. Y1 = 2 because no standalone verification API exists.

## Where I expect disagreement (>1 point risk)

- **X6 across all providers.** I scored U wherever I lacked complaint data. If the primary scorer used the complaint corpus, expect point differences but not unknown-versus-score conflicts.
- **X4 for Fidelity EFT (2) and Ren RDE (3).** Whether a captive rail with very many recipients counts as wide "channel reach" is a matter of interpretation.
- **Y3 for Chariot (3).** I counted documented authority separation as a control, even though Chariot has no AI in its payment path.
- **Every.org X.** Its placement depends on whether its 990-PF disbursements count as A2 activity.
