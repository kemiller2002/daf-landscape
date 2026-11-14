# Validation wave 4: independent check of 13 claims

Validator: independent-validation-agent-wave4, 2026-11-14. Each verdict was formed from primary sources (SEC EDGAR, IRS e-file XML, first-party pages and documents, court opinions) before the repo text was read; the repo wording was then compared. Register: [`validation-register-wave4.csv`](../../data/mission-2026-11-14/validation-register-wave4.csv).

## Scorecard

| Result | Claims |
|---|---|
| Confirmed | V4-01, V4-03, V4-04, V4-05, V4-06, V4-09, V4-10, V4-11, V4-12 |
| Partially confirmed | V4-02 (Bain "majority" is stale), V4-07 ($1.45M is the debtor's figure), V4-08 (TIAA "244 accounts" misattached), V4-13 (TPI "advised" mislabel) |
| Contradicted | none |
| Unable to verify | none |

## Material findings

1. **TIAA Charitable (V4-08).** The final 990 (short year ending 2021-05-14) Schedule N shows **$138,461,300 to Renaissance Charitable Foundation on 2021-03-09**. The "244 separate donor advised fund accounts" refers to a **separate residual transfer of $354,551 on 2021-05-17** (part of $430,495; $75,944 went to a "TIAA Charitable Director's Fund"). TIAA held **1,548 DAFs** at end-FY2020. So 244 is not the size of the migration. ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml))
2. **Ren ownership (V4-02).** The Oct-2025 Great Hill release says Bain "acquired a majority stake in Ren in 2023" and "will remain a significant shareholder". After that round, a present-tense "Bain owns a majority" is not supported. ([Pulse 2.0 reprint of release](https://pulse2.com/great-hill-partners-announces-strategic-growth-investment-in-donor-advised-fund-platform-ren/))
3. **Flipcause reserve (V4-07).** $1.45M is the amount **Flipcause listed** in its bankruptcy filings. Stripe's objection puts the reserve at under $1M (about $790k at issue). The testimony that donations "belonged to the platform" was given by Executive Chairman and co-founder Emerson Ravyn at the 2025-12-22 hearing. It is the debtor's position, not a finding. ([Oakland Voices](https://oaklandvoices.us/2026/01/10/stripe-terminated-services-flipcause-bankruptcy-filings-reveal/))
4. **TPI 51% (V4-13).** The base is 103 HNW individuals ($5m+) "who participate in philanthropic activities". They were not screened for having an adviser; the report gives 84% vehicle use separately for those who discuss philanthropy with an adviser. ([TPI full report](https://www.tbf.org/-/media/tbf/reports-and-covers/2026/2026-tpi-study-of-the-philanthropic-conversation_full-report_final_apr-2026.pdf))
5. **Donors Fund Inc (V4-08).** 6,290 DAFs and $315,757,385 are confirmed, but they come from an **amended** TY2024 return (filed 2026-03-12). The original TY2024 and TY2023 returns have no Schedule D Part I, which probably explains DAFRC's flag "Assume Sponsor Closed 2023". DAFRC also imputes FY2022 DAF grants at $97.6m, against $266.7m on the 990.
6. **Exit dating (V4-09).** The rates reproduce exactly: 11, 69 and 85 exits over 5,746 sponsor-years, giving 0.191%, 1.201% and 1.479%. However, DAFRC's trailing imputed rows push A-tier exits one year late: Jasper Ridge (ceased TY2022) is dated FY2023, and TIAA (dissolved 2021-05) is dated FY2022. Dropping the 18 trailing-imputed rows changes the rates by less than 0.01 points.
7. **Jasper Ridge recipients (V4-08).** Of the roughly $1.32bn, Schwab received $750.6m and Fidelity $548.9m (about 98% between them), Dechomai $23.7m, and **Vanguard Charitable only $50,000**.
8. **Charityvest fee (V4-12).** The $653,138 in the audit note was paid to **Vennfi and Foundation Source combined**: Vennfi was acquired by Foundation Source during 2024 and the agreement was kept. Vennfi is described as "an affiliated for profit entity".

## Exact corrections

| # | File | Current wording | Replace with |
|---|---|---|---|
| 1 | `research/mission-2026-11-14/sponsor-mortality-analysis.md` (§ tier-A table, TIAA row) | "The narrative says 244 accounts were moved into new RCF DAFs" | "A separate 2021-05-17 residual transfer of $354,551 went into 244 new RCF DAF accounts (plus $75,944 to a 'TIAA Charitable Director's Fund'); TIAA held 1,548 DAFs at FY2020 year-end" |
| 2 | same file (line ~149) | "accounts were rebuilt one-for-one at the successor (244 accounts), recurring grants did not carry over, and a reserve was held" | "the bulk ($138.46m) moved to RCF on 2021-03-09; a residual $354,551 was placed in 244 new RCF accounts in May 2021, and an $86,511 reserve was held for wind-down costs" (keep "recurring grants did not carry over" only if a source is added; this validator did not verify it) |
| 3 | same file (headline, line ~12) | "Exposure is 5,746 sponsor-years (FY2020–FY2023)" | "Exposure is 5,746 sponsor-years at risk (panel rows FY2019–FY2022, for exits dated FY2020–FY2023); exit years for imputed-trailing cases lag cessation by about a year (e.g. JRCF ceased TY2022, dated FY2023)" |
| 4 | same file (JRCF bullet) | list of four recipients | add "(Schwab $750.6m, Fidelity $548.9m, Dechomai $23.7m, Vanguard $0.05m)" |
| 5 | same file (Donors Fund row) | "The FY2024 990 reports 6,290 DAFs and $315.8m" | "The amended FY2024 990 (filed 2026-03-12) reports 6,290 DAFs and $315.8m; the original TY2023/TY2024 returns omitted Schedule D Part I. DAFRC's flag is 'Assume Sponsor Closed 2023'" |
| 6 | `research/mission-2026-11-14/firms-interested-in-daf-organizations.md` line 27 | "**Bain Capital** owns a majority of Ren (2023)" | "**Bain Capital** (Tech Opportunities) took a majority of Ren in 2023 and remained a 'significant shareholder' after Great Hill's Oct-2025 round" |
| 7 | same file line 27 | "Envestnet chose **Foundation Source**, Ren's rival, as its philanthropy integration" | "Envestnet added **Foundation Source** (a Ren competitor) as a philanthropy integration covering foundations, DAFs and planned giving; Envestnet also lists GiftingNetwork" |
| 8 | same file lines 44, 104, 270, 303 | "Owns Ren majority" / "2023 majority deal" | "Took Ren majority in 2023; significant shareholder after 2025" |
| 9 | same file lines 40, 205, 267 | "$54m upfront … ([Payments Dive])" and "earnout write-down" | "$53.3m non-contingent consideration ($111.1m total including $57.8m contingent) … $(47.1)m fair-value reduction of the earnout liability in FY2022 ([Shift4 FY2022 10-K](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/four-20221231.htm))" |
| 10 | `research/mission-2026-11-14/failed-daf-startups-deep-research.md` line 243 | "in December 2025, **Stripe froze a $1.45M reserve**" | "in December 2025 Stripe terminated processing and held a reserve that Flipcause's filings list at $1.45M (Stripe's objection puts it below $1M, about $790k at issue)" |
| 11 | same file line 251 | "The founder testified that the donations belonged to Flipcause" | "Co-founder and Executive Chairman Emerson Ravyn testified at the 2025-12-22 bankruptcy hearing that donations belonged to Flipcause (the debtor's position, not a court finding)" |
| 12 | `research/mission-2026-11-14/analyst-and-education-landscape.md` line 107 and lines 111, 187 | "Advised HNW clients using a DAF … Advised and sponsor-linked sample" / "advised-client penetration (51% of TPI's HNW clients)" | "Philanthropically active HNW individuals ($5m+) using a DAF: 51% (TPI 2026, n=103; not screened for having an adviser)" |
| 13 | `research/mission-2026-11-14/industry-incentives-structural-analysis.md` line 143 | "Sixteen attorneys general asked them on May 22, 2026" | "Sixteen attorneys general, led by Minnesota, asked them in a letter dated May 21, 2026 (California release May 22)" |
| 14 | `research/DAF-INDUSTRY-REPORT-2026-11.md` line 96 | "About 67% of Fidelity grants already go by EFT ([Chariot …])" | cite first-party: "Fidelity's 2026 Giving Report: 'Today, 67% of our grants are distributed via EFT' ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf))" |
| 15 | `research/mission-2026-11-14/red-team-wave2b-graph-data-incentives.md` line 69 | "(about 1m checks in 2025)" | drop this, or mark it "[inference: about 33% of about 3m grants]"; the report does not state it |
| 16 | `research/mission-2026-11-14/daf-user-complaints-deep-research.md` line 31 | "Fairbairn lost at trial; Pinkert dismissed for standing" | "Fairbairn lost after a bench trial (N.D. Cal., 2021-02-26); Pinkert v. Schwab Charitable dismissed for lack of Article III standing, affirmed 48 F.4th 1051 (9th Cir. 2022)" |
| 17 | `research/mission-2026-11-14/quadrant-calibration.md` line 87 and any "Foundation Source fee" wording | "Vennfi / Foundation Source services agreement ($653,138 in 2024)" is correct | keep it; where elsewhere it is called a "Foundation Source fee", write "fee to Vennfi/Foundation Source (Vennfi acquired by FS in 2024)" |
| 18 | `research/mission-2026-11-14/queue-contract-data-rights-agent-controls.md` lines 24, 89 | "iPhi MSA" | add "(Ren published template, titled 'Final Draft 2023-06-20 v2'; executed customer terms may differ, and Order Forms prevail on conflict)" |

## Interpretation challenges worth carrying forward

- **Vanguard–Altruist:** the Endaoment launch came 41 days after the deal was signed and before it closed. The timing does not show Vanguard's preference about sponsor choice.
- **Daffy:** limits are *undocumented*, which is not the same as absent. Donations are capped by fund balance, MCP clients may prompt for approval, and `cancel_donation` works before payout. Frame this as a documentation and control-transparency gap.
- **NPact §2.4** is written as "does not authorize", not as an enumerated breach with remedies. Its force depends on the termination clauses.
- **Exit rates:** 1.20% (tiers A+B) is the more donor-relevant central rate. Exits hidden by DAFRC imputation (264 imputed rows in FY2019–22) can escape candidate generation, so 1.48% is not a hard ceiling.
- **SPLC letter:** advocacy by 16 Democratic AGs, not an enforcement action.
