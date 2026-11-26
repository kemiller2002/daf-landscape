# A1 Evidence Quadrant: blind second-scorer rationale (2026-11-14)

**Area:** A1, DAF platform and administration (system of record). **Scorer:** blind (second scorer, under the two-scorer rule in [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §5).
**Scores:** `data/mission-2026-11-14/quadrant-scores-A1-blind.csv` (132 rows, 12 providers × 11 criteria). **Chart:** `research/mission-2026-11-14/quadrants/A1-blind.svg`.

**Independence.** I did not open the primary A1 score file, the primary A1 rationale, `quadrant-positions.csv` or any file in `quadrants/`. I also skipped `queue-proposals-quadrant-A1.csv`, because it may carry the primary scorer's reasoning. The engine ran only after my scores were written. I filtered its console output to `A1 blind` rows, and I computed the bands below from my own file using the engine's functions.

**Status:** *internal-demonstration*. These scores are claims under EDF until they are reconciled with the primary scorer in `quadrant-calibration.md`. This is not a Gartner Magic Quadrant.

## Positions (blind)

| Provider | X point (band) | Y point (band) | Coverage X / Y | Quadrant |
|---|---|---|---|---|
| Ren (incl. iPhi/Stellar, DonorFirstX) | 2.94 (2.65–3.05) | 2.35 (2.35–2.35) | 0.90 / 1.00 | Proven Leaders |
| Give Interactive | 2.75 (2.20–3.00) | 2.15 (2.15–2.15) | 0.80 / 1.00 | Proven Leaders (boundary) |
| TIFIN Give | 2.44 (2.20–2.60) | 2.00 | 0.90 / 1.00 | Proven Leaders (boundary) |
| Foundant CommunitySuite | 2.11 (1.90–2.30) | 2.00 (1.10–2.90) | 0.90 / 0.55 | Proven Leaders (boundary) |
| Fidelity Charitable (in-house, FMR-administered) | 2.82 (2.40–3.00) | 1.40 | 0.85 / 1.00 | Scale Operators |
| NPT GivingPoint (sponsor-built) | 2.87 (2.15–3.15) | 1.85 (1.20–2.60) | 0.75 / 0.65 | Scale Operators (boundary) |
| Foundation Source (DAF OS / Vennfi) | 2.40 (1.80–2.80) | 1.88 (1.60–2.20) | 0.75 / 0.85 | Scale Operators (boundary) |
| Blackbaud Financial Edge NXT (foundations) | 1.64 (1.15–2.35) | 2.15 | 0.70 / 1.00 | Forward Builders (boundary) |
| Givinga | 1.55 (0.85–2.65) | 1.73 (0.95–2.75) | 0.55 / 0.55 | Focused Specialists |
| NPact (FIMS / DonorCentral) | 1.40 (1.05–2.05) | 0.83 (0.50–2.10) | 0.75 / 0.60 | Focused Specialists |
| NCF (sponsor-built, Salesforce) | 2.87 (2.15–3.15) | 1.00 (0.15–3.55) | 0.75 / 0.15 | insufficient evidence |
| SVCF (sponsor-built, Salesforce) | 2.54 (1.65–3.05) | 2.00 (0.30–3.70) | 0.65 / 0.15 | insufficient evidence |

**Read this table as bands, not ranks.** Six of the ten plotted providers are within 0.25 of a midline. Only Ren (Proven Leaders), Fidelity (Scale Operators), Givinga and NPact (Focused Specialists) sit clearly in one quadrant.

## Provider notes (what moves the score)

- **Ren.**
  - **X1 = 4 and X4 = 4** rest on filings and live portals, not on Ren's "60%+ / $200B" claim:
    - audited RCF fees of $19.2M;
    - a $14.9M RenPSG payment in the MS GIFT 990;
    - Ren payees in the Stifel and Thrivent 990s;
    - 20+ confirmed "DFX powered by Ren" or iPhi-hosted programs.
  - **X3 = 1:** the Type II (2025) and Type I (2026) claims conflict.
  - **Y5 = 1:** after AEF moved to Ren, its new portal keeps only two years of history (documented history truncation).
  - **Y2 = 3:** the Rapid Disbursement Engine, ACH onboarding through Ren for Charities, and nonprofit-shared grant data.
- **Give Interactive.**
  - **X3 = 3:** SOC 2 Type 2 and a public SOC 3 for its DAF platform (Sept 2025) are corroborated by the compliance firm's case study. This is the strongest assurance evidence in A1.
  - **X1 = 3:** anchored by Vanguard Charitable ($27B in DAF assets). Seven further tenants are inferred from certificate-transparency logs only.
  - **Y1, Y2, Y3 and Y5** are vendor claims, so they are capped at 2.
- **TIFIN Give.**
  - **X2 = 3:** the delivery record is good, with five of eight announcements delivered.
  - **Y1 = 1:** its public terms restrict downloading and automated access.
  - **Y3 = 1:** Louise executes donor transactions, and no control language is documented (V2A-10).
- **Fidelity Charitable.**
  - **X1 and X5 = 4:** it is the largest sponsor, with audited FMR administration.
  - **Y is low:** no public API or portability terms, a navigation-only AI assistant, and an EFT-only status that is still conflicting.
- **NPT GivingPoint.** The "sponsor-built" label is contested. Infrastructure evidence (EA016) shows GivingPoint is served from Ren-hosted iPhi. I scored NPT's own sponsor evidence, and calibration should decide whether this entity belongs under Ren.
- **Foundation Source.**
  - **The DAF footprint is mid-tier.** Its $55B and 5,600 private-foundation figures are mostly private-foundation administration.
  - **DAF OS has no named customers.**
  - **X3 = U:** no SOC evidence was found.
- **Foundant.**
  - **X1 is capped at 2:** "700+ CFs / $62B" is a vendor claim, and only Columbus (and the CFNCW case study) are confirmed.
  - **Y coverage is thin (0.55).**
- **Blackbaud FE NXT.** It is an adjacent G/L, not a DAF subledger (**X1 = 1, Y2 = 1**). Its public SKY API (**Y1 = 3**) lifts Y. **X3 = 2** because SOC reports exist alongside SEC and FTC enforcement over the 2020 breach.
- **NPact.**
  - **Y1 = 0:** positive evidence. §2.4 of its Standard Terms bars third-party access, and there is no export obligation.
  - **Y5 = 1:** data is deleted 10 business days after hosting ends.
  - **Its only confirmed DAF client (AEF) churned to Ren.**
- **NCF and SVCF.** Scale is strong in their 990s and both portals run on Salesforce (DNS). The builder, ledger, API, rails and portability are all unknown, so **Y coverage is 0.15** and both are labelled "insufficient evidence".

## Judgment calls the calibration should check

1. **Absence → U, even where the rubric's 0 anchor says "not documented".** I used 0 only for NPact Y1, where the contract text is positive evidence. Fidelity Y1 and Y5 = 1 reflect partial documented mechanisms (DAF Direct; an inbound-only transfer process), not absence.
2. **X4 for single-sponsor platforms (Fidelity, NPT, NCF, SVCF)** scores the sponsor's distribution channels, because the platform has no third-party customers.
3. **Blackbaud Y3 = 2** uses provider-level AI evidence (the Development Agent on Raiser's Edge NXT), not FE NXT-specific evidence.
4. **Ren X3 = 1, not 0:** the claims conflict on type, not on whether a SOC report exists.

## Web evidence added in this pass (cited in the CSV)
- Give Interactive SOC 2 Type 2 / SOC 3: https://www.bdemerson.com/case-studies/give-interactive
- Foundant SOC 2 Type 2 statement: https://www.foundant.com/blog/data-security-partnerships-and-practices-for-a-successful-quest
- Blackbaud trust center (SOC 1/2 Type II listed): https://trust.blackbaud.com/
- Blackbaud San Diego Foundation FE NXT case study: https://www.casestudies.com/company/blackbaud/case-study/the-san-diego-foundation-customer-case-study
- Givinga channel partnerships: https://www.businesswire.com/news/home/20210812005102/en ; https://www.businesswire.com/news/home/20251211023148/en
- No SOC evidence was found for Foundation Source, NPact or Givinga (web searches on 2026-11-14), so these are scored U.
