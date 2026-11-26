# Validation wave CO1: commercial-opportunity package

**Date:** 2026-11-20. **Validator:** independent, adversarial. **Scope:** 16 material claims from `research/commercial-opportunity/` and `data/commercial-opportunity/prospects-*.csv`, plus an overreach review of `executive-report.md` and `service-offerings/offerings.md`.

**Method:**
- Primary sources only: IRS e-file XML (fetched from gt990datalake for 4 returns; the others are from the repository harvest, which cites XML), issuer PDFs and press releases, and price pages.
- robots.txt was checked on every host before fetching.
- Pages behind Cloudflare challenges (lpl.com) were not bypassed. Trade-press and search-result evidence was used instead and is flagged.
- Row-level detail: `validation-wave-co1.csv`.

## Summary

| Result | Count | Claims |
|---|---|---|
| Confirmed | 12 | VCO-01, 02, 04, 05, 06, 09, 10, 11, 12, 13, 14, 15 |
| Partially confirmed | 3 | VCO-03 (stale), VCO-07 (vendors inferred), VCO-08 (stale range) |
| Contradicted | 0 | — |
| Not falsified | 1 | VCO-16 (5 searches; absence is weak evidence) |

**Material findings:**
1. **The LPL–Commonwealth conversion has already happened (VCO-03).** It completed on the weekend of about 2026-11-14/15. InvestmentNews (2026-11-16) quotes LPL: "The successful conversion of Commonwealth advisors, the largest in LPL's history". The package, dated 2026-11-20, still presents "Q4 2026" as a future dated trigger in the executive report, the wealth notes, the assumption tests and PW06. The Commonwealth Charitable Fund portal ("DFX powered by Ren") shows no sunset notice, so a DAF-programme decision may still be pending, but it is now undated.
2. **The 990 figures reproduce exactly** (VCO-04, 05, 06, 08, 09):
   - Stifel paid Ren $801,302 (CY2025) against $498,305 (CY2024).
   - Communities Foundation of Texas paid EPAM $1,608,933, then $1,263,366, then $388,305.
   - Cleveland Foundation paid Stellar $416,391.
   - The community-foundation medians are IT $454,619 and outside services $1,285,942, n=43.

   The labels matter, though. The IT median counts blank lines as zero; it is $467,616 if blanks are excluded. "Outside services" covers lines 11a–c, 11e and 11g, so it includes audit, legal and management fees. It is not a consulting budget.
3. **The Vanguard–Slalom range is stale (VCO-08).** The latest year (TY2024, FYE June 2025) is $3.74m. PS04 quotes TY2024 values but cites the TY2023 filing.
4. **The Arkansas vendors are inferred, not stated (VCO-07).** The ARCF blog names neither Ren nor Foundant. 2026-06-01 is the date login instructions were emailed, not a stated go-live date.
5. **All price anchors are exact (VCO-10), but some are weak comparators.** BerryDunn's anchors are a 2019 municipal ERP selection and a 2023 public-health EHR needs assessment, neither DAF-related.
6. **The no-RFP claim stands (VCO-16).** The nearest hits:
   - a community foundation strategic-planning RFP (Anne Arundel, 2026);
   - the Fidelity Charitable Catalyst grant RFP issued *to* community foundations;
   - technology RFPs from foundations that are not community foundations: Golden LEAF (grant-database consultant), Center for Disaster Philanthropy (IT assessment), Kauffman (ServiceNow and Salesforce), PHI (ERP, 2026-08) and UFW Foundation (CRM, 2026-08).

   These show that foundations in philanthropy do procure technology help through RFPs. That partly offsets the package's inference that the absence of community-foundation RFPs means low procurement activity.

**Searches run for VCO-16 (2026-11-20):**
1. community foundation "request for proposals" donor advised fund software 2025
2. community foundation RFP fund accounting / grants management / donor portal 2026
3. "community foundation" RFP technology assessment consultant "donor-advised" 2024
4. community foundation RFP CRM "donor advised funds" vendor selection (PDF)
5. foundation "request for proposal" fund-management / philanthropy software 2025–2026

## Overreach list (executive-report.md and offerings.md)

| # | Location | Overreach | Type |
|---|---|---|---|
| O1 | executive-report §2 Q1, §4 | "Dated programme decisions: LPL–Commonwealth (Q4 2026)". The conversion completed about 2026-11-14 | Stale data |
| O2 | executive-report §2 Q1; offerings OF1 | The median IT of $455k and outside services of $1.29m come from **$250m–1bn community foundations only** (n=43). They are used to support a $250m–$5bn segment that includes faith and single-issue sponsors. Both lines are whole-organisation totals; outside services includes audit, legal and management fees. The text calls this a "visible budget", which implies spend that is available for Echelon's services | Ability treated as willingness; scope stretch |
| O3 | executive-report §2 Q3 | McKinsey's $11.8m from Fidelity Charitable is listed under "generalist IT consultancies already paid by sponsors". The 990 service description is "PHIL. CONSULTING", not IT | Mislabelled evidence |
| O4 | executive-report §1, §4; offerings OF1 ROI | "Vendor fees of $118k–416k a year" is the **community-foundation Ren/Stellar** range (INV033). The package's own wealth notes give $118k–498k (median $218k, 18 sponsors), and Stifel pays $801k. The OF1 claim that "a 10% better contract outweighs the fee" works out to about $12k–42k a year against a $35k–90k fee. That is not self-evidently positive at the low end; it needs a 3-year horizon and is unflagged arithmetic | Inconsistent range; unflagged inference |
| O5 | executive-report §1 | "First market is roughly 40–60 mid-size community foundations and faith or single-issue sponsors". The count is not derived anywhere shown; the cost dataset has 43 community foundations in the $250m–1bn band alone | Unflagged inference |
| O6 | executive-report §4 (OF1 evidence) | "iPhi attrition 6/57" and peer exits are treated as demand. Exits already happened, and the package itself concedes "the recent migration wave is largely complete" | Signal timing |
| O7 | executive-report §2 Q6; offerings | "Highest-probability profitable revenue". The ranking rests on judgement scores with no willingness-to-pay data; sensitivity is tested only on the same judgements. The "Medium" confidence is generous; Low-Medium is more defensible | Over-confidence |
| O8 | executive-report §2 Q7 / §1 | "No analyst covers DAF platforms". True for the analyst firms named, but Tech Impact publishes community-foundation software-selection guidance (2024 PDF) and Kitces sells vendor selection for wealth tech. "No analyst" should not be read as "no neutral advice" | Framing |
| O9 | prospects PS16 (supports OF1 ranking) | CFT is called the "strongest mid-sized signal: high discretionary tech spend". EPAM spend fell 76% from TY2022 to TY2024 and CFT's operating cost fell $9m. This is equally consistent with a project wind-down | Ability treated as willingness; trend ignored |
| O10 | prospects PS01 | NPT CTO hired "to drive 'platform transformation'". That phrase is from his bio about past experience, not NPT's mandate | Misattributed quote |
| O11 | offerings OF1 price anchors | BerryDunn anchors ($117.7k from 2019; $175k NTE for an EHR assessment) are public-sector. The 2019 figure is seven years old with no inflation adjustment | Stale or non-comparable anchor |

## Recommended corrections (Find/Replace)

1. **File:** `research/commercial-opportunity/executive-report.md`
   - **Find:** `LPL–Commonwealth (Q4 2026)`
   - **Replace:** `LPL–Commonwealth (advisor conversion completed about 2026-11-14; the Commonwealth Charitable Fund's fate is unannounced)`
2. **File:** `research/commercial-opportunity/prospect-profiles/wealth-and-entrants-notes.md`
   - **Find:** `LPL–Commonwealth conversion due Q4 2026 [F]`
   - **Replace:** `LPL–Commonwealth conversion completed on or about 2026-11-14/15 [F InvestmentNews 2026-11-16]; CCF portal shows no sunset notice (2026-11-20)`
3. **File:** `research/commercial-opportunity/clarity-edf-analysis/assumption-tests.md`
   - **Find:** `the LPL–Commonwealth conversion in Q4 2026`
   - **Replace:** `the LPL–Commonwealth conversion (completed about 2026-11-14; the DAF-programme decision is still open)`
4. **File:** `data/commercial-opportunity/prospects-wealth.csv` (PW06)
   - **Find:** `Commonwealth onboarding to LPL platform expected complete Q4 2026 [F LPL release]`
   - **Replace:** `Commonwealth advisor conversion to LPL completed weekend of 2026-11-14/15 [F InvestmentNews 2026-11-16]`
5. **File:** `research/commercial-opportunity/executive-report.md`
   - **Find:** `median IT spend of $455k and $1.29m in outside services for the $250m–1bn band, reproducible from 990s (DS spend)`
   - **Replace:** `median whole-organisation IT spend (990 line 14) of $455k and $1.29m in fees for services excluding investment management (lines 11a–c, e, g; includes audit and legal) for the 43 community foundations with $250m–1bn of DAF assets, FY2024, reproducible from 990s (DS spend). This shows capacity to spend, not a discretionary consulting budget`
6. **File:** `research/commercial-opportunity/executive-report.md`
   - **Find:** `vendor fees of $118k–416k a year;`
   - **Replace:** `Ren/Stellar platform fees of $118k–416k a year at community foundations (up to $801k at Stifel Charitable);`
7. **File:** `research/commercial-opportunity/executive-report.md`
   - **Find:** `Generalist IT consultancies already paid by sponsors (EPAM, Slalom, Clarity Partners, BCG, Accenture; McKinsey received $11.8m from Fidelity Charitable in FY2025, verified in the repository's 990 harvest)`
   - **Replace:** `Generalist IT and strategy consultancies already paid by sponsors (EPAM, Slalom, Clarity Partners, BCG, Accenture; McKinsey received $11.8m for "phil. consulting" from Fidelity Charitable in FY2025, verified in the repository's 990 harvest)`
8. **File:** `research/commercial-opportunity/competitive-landscape/competition-and-pricing.md`
   - **Find:** `| Vanguard Charitable | Slalom | 2021–23 | $2.1–3.4M a year | "TECH SERVICES" |`
   - **Replace:** `| Vanguard Charitable | Slalom | TY2021–24 | $2.06–3.74M a year (rising) | "TECH SERVICES" |`
9. **File:** `research/commercial-opportunity/buyer-segments/segment-analysis.md`
   - **Find:** `Slalom $2.1–3.4m a year at Vanguard Charitable`
   - **Replace:** `Slalom $2.06–3.74m a year at Vanguard Charitable (TY2021–24)`
10. **File:** `data/commercial-opportunity/opportunity-scores.csv` (OF8)
    - **Find:** `Vanguard Charitable paid Slalom $2.1-3.4m a year`
    - **Replace:** `Vanguard Charitable paid Slalom $2.06-3.74m a year (TY2021-24)`
11. **File:** `data/commercial-opportunity/prospects-sponsors.csv` (PS04 sources)
    - **Find:** `https://projects.propublica.org/nonprofits/organizations/232888152/202511349349313096/full`
    - **Replace:** `https://projects.propublica.org/nonprofits/organizations/232888152/202621329349306657/full (TY2024 values); https://projects.propublica.org/nonprofits/organizations/232888152/202511349349313096/full (TY2023)`
12. **File:** `data/commercial-opportunity/prospects-sponsors.csv` (PS14)
    - **Find:** `complete 2026-06-01 [X/F]`
    - **Replace:** `2026 transition (ARCF blog 2026-04-20; login instructions emailed 2026-06-01; Foundant inferred from arcf.fcsuite.com login domain, vendors not named) [F/I]`
13. **File:** `data/commercial-opportunity/prospects-sponsors.csv` (PS01)
    - **Find:** `new CTO hired from Vanguard to drive 'platform transformation' [F]`
    - **Replace:** `new CTO hired from Vanguard (release 2026-03-11) to 'advance NPT's enterprise solutions' [F]`
14. **Optional upgrades:** the deal-adviser evidence for Ren and Foundation Source (`[R]`) can be upgraded to `[F]`. Houlihan Lokey, Greenberg Traurig, Canaccord and Baird all publish tombstone or press pages.

**Sources not fetched directly:**
- lpl.com: a Cloudflare challenge blocked access. The LPL close date and Q4 2026 guidance come from GlobeNewswire search results, and the conversion from InvestmentNews.
- philanthropy.com (Arabella): search results only.
- The Vanguard TY2024 XML returned 404 on gt990datalake; the repository's harvest values were used.
