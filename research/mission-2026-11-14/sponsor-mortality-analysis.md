# DAF sponsor entry and exit ("mortality"), FY2019–FY2024

*Queue items P-FAIL-01 and P-FAIL-02. Prepared 2026-11-14. Script: `scripts/mission_sponsor_mortality.py` (stdlib only). Outputs: `data/mission-2026-11-14/sponsor-entry-exit-panel.csv`, `sponsor-mortality-summary.csv`, `sponsor-exit-verification.csv`.*

## 1. Bottom line

- **The DAFRC panel overstates sponsor deaths.** DAFRC marks 82 of its 1,594 sponsor EINs as "Assume Sponsor Closed" in FY2020–FY2023 ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Each was checked against IRS filings: the Business Master File ([IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv)), the auto-revocation list ([IRS revocations](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip)), the e-file index ([IRS TEOS index 2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv)) and the e-filed 990 XML itself. The results:
  - 10 of the 82 organisations actually ceased. They filed a final or terminated return with a Schedule N listing the transfer of assets.
  - 52 survive and still file a Form 990, but report no DAFs in Schedule D Part I.
  - 15 remain unresolved.
  - 5 are reporting artefacts: a later 990 still reports DAFs.
- **The verified annual exit rate is low, especially when weighted by assets.** Exposure is 5,746 sponsor-years (FY2020–FY2023):

  | Bound | Definition | Count-weighted / yr | Asset-weighted / yr |
  |---|---|---|---|
  | Lower | organisation ceased (tier A) | **0.19%** (11) | **0.21%** (0.023% excluding one $1.43bn case) |
  | Central | A + the organisation survives but reports no DAFs (tier B) | **1.20%** (69) | 0.24% (0.050% ex-JRCF) |
  | Upper | A + B + unresolved (tier C) | **1.48%** (85) | 0.25% (0.067% ex-JRCF) |
  | Naive (DAFRC "closed" only) | — | 1.43% (82) | 0.26% |

  Source: `verified` rows in `data/mission-2026-11-14/sponsor-mortality-summary.csv`.
- **Exits are concentrated among small sponsors.** Panel exit rates fall as size rises: 2.2%/yr below $1m, 1.3% at $1–10m, 0.7% at $10–100m and 0.2% at $100m–$1bn (prior-year DAF assets). Single-issue charities exit at 1.9%/yr, national sponsors at 1.4% and community foundations at 1.1%.
- **When the sponsor dies, donor money moved to another sponsor in every documented case.** All 11 ceased sponsors filed a final 990 with a Schedule N, and the named recipients are other charities: Fidelity Charitable, Schwab Charitable, RCF, United Charitable and community foundations (§5). No terminated sponsor in the panel was revoked by the IRS for non-filing.
- **Entries are mostly a coverage effect, not new sponsors.** Of 253 first appearances in FY2020–FY2024, 201 are organisations ruled exempt years earlier that are new to the panel. Examples are Vanguard Charitable (FY2020) and the BofA Charitable Gift Fund (FY2021). Only 38 (about 0.5% of the at-risk base per year) were ruled exempt within a year of entry, for example Daffy Charitable Fund, DonateStock Charitable and Endaoment.
- **SDG Impact Fund (P-FAIL-02) reported $10.1bn of DAF assets on Schedule D and does not appear in the DAFRC panel at all.** It is still on IRS Publication 78 and has no revocation (§6).

## 2. Data and method

### 2.1 Input panel
The input is `data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv`: 8,751 EIN×FY rows covering 1,594 EINs. EINs are zero-padded to 9 digits, and there are no duplicate EIN-FY pairs ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). Two structural facts drive the method:

- **The panel has no gaps.** DAFRC fills a missing year with an `Imputed` value instead of leaving a hole. Gaps therefore have to be found from the provenance flag (`source_eoy_daf_assets`), not from missing rows. There are 86 imputed rows sitting between two filed rows, across 59 EINs.
- **FY2024 is 30% imputed by assets.** 713 FY2024 rows are imputed carry-forwards, and 715 FY2024 rows repeat the FY2023 `end_of_tax_period`. That means 699 EINs have their last filed value in FY2023. Whether those sponsors exit in FY2024 cannot yet be observed, so **FY2024 exits are right-censored** and are not estimated. FY2019 is left-censored: 1,341 EINs appear in FY2019 and 1,447 in FY2020.

"Filed" means `source_eoy_daf_assets` ∈ {IRS 990, NPT historical data, paper submission}; "imputed" means `Imputed`.

### 2.2 Event definitions (`sponsor_history()` in the script)
| Event | Rule |
|---|---|
| Entry | First panel FY > 2019 |
| Panel exit | Last panel FY < 2024; exit FY = last + 1. This matches DAFRC `operating_status` "Assume Sponsor Closed t" exactly (82 EINs) |
| Imputation-masked exit candidate | EIN stays in the panel to FY2024, but its last *filed* asset value is FY2022 or earlier, so all later rows are imputed (14 EINs). Exit FY = last filed + 1 |
| Zero-DAF terminal exit | Filed DAF assets fall to 0 and stay there through FY2024 after a positive year (4 EINs) |
| Never filed | Every row imputed (6 EINs). Not treated as an exit |
| Imputed gap | Imputed row between two filed rows. Counted as survival |
| Period carry-forward | `end_of_tax_period` repeats the prior FY (label lag) |

Survivorship is measured against an at-risk set. For FY *t*, the at-risk set is every EIN with a row in FY *t*−1 that has not already exited. Rates are computed two ways:
- **Count-weighted:** exits ÷ number at risk.
- **Asset-weighted:** the exiting sponsors' last positive *filed* DAF assets ÷ the at-risk set's FY *t*−1 DAF assets.

### 2.3 Verification of all 100 exit candidates
Every candidate (82 panel exits, 14 masked, 4 zero-DAF) was checked automatically against public IRS files, and the requested 50-case sample also against the ProPublica API:

1. **IRS EO BMF (Nov 2026 extract)**: is the EIN still listed? The check also reads its latest tax period and accounting-period month, which flags fiscal-year changes ([eo1.csv](https://www.irs.gov/pub/irs-soi/eo1.csv) to [eo4.csv](https://www.irs.gov/pub/irs-soi/eo4.csv)).
2. **IRS auto-revocation list.** A revocation counts only if it is dated after the sponsor's last filed period and has not been reinstated. Two candidates were revoked in 2019–2020, before their last DAFRC filing, so they had evidently been reinstated ([IRS revocations](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip)).
3. **IRS e-file index 2019–2026**: every 990, 990-EZ or 990-PF filed for a period after the last filed DAFRC period (`https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv`).
4. **The e-filed XML itself** (IRS TEOS XML as mirrored by the GivingTuesday data lake, e.g. [TIAA Charitable final 990](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml)). From each return the script parses:
   - Schedule D Part I (`DonorAdvisedFundsHeldCnt`, `DonorAdvisedFundsVlEOYAmt`);
   - the final-return and terminated flags (`FinalReturnInd`, `ContractTerminationInd`);
   - Schedule N transfer recipients with EIN and fair market value;
   - whether the narrative still mentions donor-advised funds.

   If the newest later return is not yet mirrored (16 cases returned HTTP 404, all 2026 filings), the next newest one is used.
5. **ProPublica Nonprofit Explorer API** for the sample: the top 25 by assets plus 25 drawn at random with `random.Random(20261114)` (e.g. [ProPublica API, TIAA Charitable](https://projects.propublica.org/nonprofits/api/v2/organizations/472199684.json)). All 50 EINs were found.

The rule-based outcomes are grouped into four evidence tiers, which give the bounds:

| Tier | Outcomes | n (all 100) | Last filed DAF assets |
|---|---|---|---|
| A: organisation ceased or converted | final or terminated return with Schedule N (11) | 11 | $1,602m |
| B: organisation survives, no DAFs reported | later Form 990 filed, with no Schedule D Part I DAF data and no DAF mention in the text | 58 | $211m |
| C: unresolved | later 990 has no Schedule D DAF data but the text still describes DAFs (12); no later return found (3); switched to 990-EZ (1) | 16 | $126m |
| D: reporting artefact | a later 990 *does* report DAFs (15) | 15 | $252m |

By sample stratum:
- Top 25: A 3, B 7, C 8, D 7.
- Random 25: A 5, B 16, C 1, D 3.

The top 25 contain far more artefacts. Large "exits" are disproportionately DAFRC processing gaps.

## 3. Entries

| FY | Entrants | Existing organisation new to panel | New organisation (ruling ≤1 yr before entry) | Ruling after entry (reinstated/reorganised) | Name match to an exiting EIN (lead) | Not in BMF |
|---|---|---|---|---|---|---|
| 2020 | 115 | 92 | 12 | 4 | 5 | 2 |
| 2021 | 41 | 34 | 6 | 1 | 0 | 0 |
| 2022 | 42 | 31 | 10 | 1 | 0 | 0 |
| 2023 | 36 | 28 | 7 | 1 | 0 | 0 |
| 2024 | 19 | 16 | 3 | 0 | 0 | 0 |

Source: `entrant_class` rows in the summary. Ruling dates come from the [IRS EO BMF](https://www.irs.gov/pub/irs-soi/eo1.csv).

- **FY2020 entrants are mostly a coverage effect.** They carry $15.9bn of DAF assets, including Vanguard Charitable at $10.7bn (NPT-sourced), Ayco, the Goldman Sachs Charitable Gift Fund, Donors Trust and T. Rowe Price. These are long-standing sponsors that the FY2019 file lacks.
- **BofA's FY2021 "entry" ($3.5bn) is the same kind of artefact.**
- **Genuine de novo sponsors are small.** Examples are GivingFund, Endaoment, Daffy Charitable Fund (ruled 2021-05), DonateStock Charitable, Telescope Fund, GoodCoin Giving Fund, Anondo Fund, GivingTrax and Matbia.
- **Name-match leads are only leads.** One is Omaha Community Foundation: EIN 470645958 enters in FY2020, while EIN 363789990 under the same name drops to imputation. The later FY2024 990 for 363789990 still reports 1,179 DAF accounts ([990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513169349307036_public.xml)), so both EINs were active and this is not a succession. Donors Trust / Donors Fund is a false match.
- **Implied gross de novo entry rate: about 0.5% a year** (38 over 7,210 at-risk sponsor-years). That is well below the 1.2% central exit rate. The rising sponsor count in DAFRC therefore reflects coverage, not net formation.

## 4. Exit rates

### 4.1 By year (`verified_by_year` rows)
| Exit FY | At risk | DAFRC "closed" | Central (A+B) | Lower (A) | Upper (A+B+C) | Central asset-weighted |
|---|---|---|---|---|---|---|
| 2020 | 1,341 | 9 (0.67%) | 8 (0.60%) | 0 | 10 (0.75%) | 0.005% |
| 2021 | 1,447 | 19 (1.31%) | 18 (1.24%) | 3 (0.21%) | 20 (1.38%) | 0.024% |
| 2022 | 1,469 | 22 (1.50%) | 19 (1.29%) | 3 (0.20%) | 22 (1.50%) | 0.11% |
| 2023 | 1,489 | 32 (2.15%) | 24 (1.61%) | 5 (0.34%) | 33 (2.22%) | 0.65% (JRCF) |

The rise in FY2023 may be partly a vintage effect. DAFRC drops a sponsor once a single return is missing, and late filers (990s with extensions or paper filing) show up as exits until they are processed. Tier B requires a *later* return, so it is not affected by this.

### 4.2 Count-weighted versus asset-weighted
- **The asset-weighted rate is 0.2–0.25% a year at every bound, and one sponsor drives it.** Jasper Ridge Charitable Fund (EIN 47-2088631) held $1.43bn of DAF assets in FY2021. In FY2022 it reported $1.32bn of grants, filed a return flagged terminated, and listed in Schedule N roughly $1.32bn of transfers, mostly partnership interests in Jasper Ridge Diversified, to:
  - Fidelity Charitable;
  - Schwab Charitable;
  - Dechomai Asset Trust;
  - Vanguard Charitable.

  Source: [FY2022 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml). It then filed a 990-PF for 2023 ([IRS index 2024](https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv)) and is not in the current BMF.
- **Excluding JRCF, verified exits move $0.17–0.51bn over four years**, out of roughly $190bn of average annual DAF assets. That is about 0.02–0.07% a year.
- **By count, exits are a small-sponsor phenomenon.** 62 of the 69 tier A+B exits held less than $10m. Among single-issue charities ("Other", "Universities and Healthcare", "Religiously-Affiliated"), the typical B case is a charity that stops administering a handful of DAFs.

### 4.3 Notable verified exits
| Sponsor (EIN) | DAFRC last filed DAF assets | IRS evidence | Tier |
|---|---|---|---|
| Jasper Ridge Charitable Fund (472088631) | $1,428m (FY2021) | FY2022 return flagged terminated; Schedule N transfers ≈$1.32bn to Fidelity/Schwab/Dechomai/Vanguard; FY2023 990-PF; not in BMF ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml)) | A |
| TIAA Charitable Inc (472199684) | $162m (FY2020) | Final 990 for the short period ending 2021-05-14. Schedule N: "Donor advised fund assets", $138.46m to Renaissance Charitable Foundation on 2021-03-09. The narrative says 244 accounts were moved into new RCF DAFs ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml)) | A |
| The Triskeles Foundation (753023740) | $7.6m | Final 990 FY2021-03. "Donor advised fund accounts", $8.08m to RSF (Rudolf Steiner Foundation) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202141209349300824_public.xml)) | A |
| Sunbury Area CF (240796877) | $0.7m | Final 990 FY2020-07: $6.7m to Community Giving Foundation ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202130889349300428_public.xml)) | A |
| Rusk County CF (260394674) | $0.4m | Final 990 FY2023-03: $2.14m to Eau Claire CF ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202303209349302295_public.xml)) | A |
| National Heritage Foundation (582085326) | $0.07m | Final 990 FY2022: $3.84m to United Charitable ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202343179349306884_public.xml)). This agrees with prior repo row FD02 | A |
| Donors Fund Inc (474844275) | $81m (FY2022) | **Artefact.** DAFRC: "closed 2023". The FY2024 990 reports 6,290 DAFs and $315.8m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202600719349301710_public.xml)) | D |
| Endaoment (844661797) | $15.3m (FY2022) | **Artefact.** Imputed since FY2023. The FY2024 (June) 990 reports 6,000 DAFs and $17.1m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202542899349300104_public.xml)) | D |
| Goldstein Foundation (270439529) | $72m (FY2021) | Still files 990. The FY2024 990 answers "No" to DAFs (`DonorAdvisedFundInd=false`) ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349302935_public.xml)) | B |
| Give2Asia (943373670) | $15.7m (FY2021) | The FY2024 990 has no Schedule D Part I data, but its program text says it "manages donor advised grants, donor advised funds" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513189349315366_public.xml)) | C |
| Kern CF (770555874) | $13.0m (FY2022) | The FY2022 990 reports 62 DAFs. The FY2023 and FY2024 990s include Schedule D but no Part I ([FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202342989349301759_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523219349312712_public.xml)) | B |

## 5. What happens to donor assets on exit

- **Tier A (11 sponsors): the assets were transferred in every case with an itemised Schedule N.** Recipients:
  - National sponsors: Fidelity Charitable (EIN 11-0303001), Schwab Charitable (31-1640316), Vanguard Charitable, RCF (35-2129262) and United Charitable (20-4286082);
  - Mission-aligned sponsors: RSF and Dechomai;
  - A neighbouring community foundation: Community Giving Foundation, Eau Claire CF, Hamilton CF and Four County CF.

  Two cases differ:
  - Milbank Community Foundation transferred $0.55m to a school educational foundation, which is not a DAF sponsor, so the DAF character may have been lost.
  - Pittsburgh Leadership Fund lists only "ceased operation".

  TIAA Charitable shows the full mechanics: accounts were rebuilt one-for-one at the successor (244 accounts), recurring grants did not carry over, and a reserve was held for wind-down costs ([TIAA final 990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202111979349301206_public.xml)).
- **Tier B (58 sponsors): the disposition cannot be seen.** The organisation survives and stops reporting DAFs. The balances may have been granted out, moved to another sponsor (no Schedule N is required for a partial transfer below 25% of net assets), reclassified as designated or agency funds, or simply left unreported. The Give2Asia case shows that "no Schedule D Part I" does not always mean "no DAFs", which is why such cases are placed in tier C.
- **No case of donor assets being lost was found among panel exits.** The documented loss and misuse cases (SDG Impact Fund, Flipcause) lie *outside* the DAFRC sponsor universe (§6; `failed-daf-startups-deep-research.md`).

## 6. P-FAIL-02: SDG Impact Fund trace

**Identity.** SDG Impact Fund Inc, EIN 46-2368538, Cartersville GA. 501(c)(3), ruling 2014-08, foundation code 15 (public charity, 170(b)(1)(A)(vi)), NTEE P20 ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/462368538.json); [IRS EO BMF eo3](https://www.irs.gov/pub/irs-soi/eo3.csv)).

| Tax year | Source | DAF accounts (Sch D I-1) | DAF contributions | DAF grants | DAF EOY value | Total assets EOY | Asset composition / notes |
|---|---|---|---|---|---|---|---|
| 2017 | paper 990 (ProPublica extract) | n/a | — | — | — | $117,475 | revenue $117,475 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/462368538)) |
| 2018 | paper 990 (ProPublica extract) | n/a | — | — | — | $1,507,475 | revenue $1,390,000 ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/462368538.json)) |
| 2019 | e-file, filed 2021-05 | 78 | $12,985,087 | $1,010,652 | $13,074,272 | $15,095,576 | "Digital assets" $10.38m, intangibles $2.11m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202131389349300103_public.xml)) |
| 2020 | e-file, filed 2021-09 | 120 | $229,787,723 | $4,896,008 | $237,965,987 | $243,401,739 | "Digital assets" $222.5m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202122529349300217_public.xml)) |
| 2021 | e-file, filed 2022-08 | 152 | $9,860,933,786 | $4,322,184 | $10,098,899,773 | $10,098,941,206 | "Various digital and non cash assets" $10.077bn; cash $5.5m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202242139349301369_public.xml)) |
| 2022 | e-file, filed 2023-10 | 146 | $13,616,509 | $8,562,256 | $10,103,954,026 | $10,107,192,856 | Same $10.077bn non-cash line, unchanged; cash $7.5m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202342799349301349_public.xml)) |
| 2023 | — | — | — | — | — | — | No e-filed return in the IRS indexes for 2024–2026 ([2024](https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv), [2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv), [2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv)). ProPublica's latest is FY2022 |

Other facts from the filings and registries:
- **No independent audit.** Every e-filed year answers "No" to audited financial statements (`IndependentAuditFinclStmtInd=0`). It reports 0–2 employees and 4 voting board members, all described as independent. Anthony Suber is principal officer (same XMLs).
- **Its reported DAF value is not reflected in grants.** Reported FY2021–FY2022 DAF value was about $10.1bn, while total DAF grants over 2019–2022 were $18.8m. Grants were 0.08% of the reported FY2022 DAF value.
- **IRS status (Nov 2026):**
  - Still in the BMF, with latest `TAX_PERIOD` 202412 and asset/income/revenue amounts of 0 ([eo3.csv](https://www.irs.gov/pub/irs-soi/eo3.csv)). Neither ProPublica nor the e-file index holds a FY2024 return, so it was presumably filed on paper or is not yet published.
  - **Still listed in Publication 78** as eligible to receive deductible gifts ([IRS Pub 78 data](https://apps.irs.gov/pub/epostcard/data-download-pub78.zip)).
  - **Not on the auto-revocation list** ([IRS revocations](https://apps.irs.gov/pub/epostcard/data-download-revocation.zip)).
  - "SDG Global Impact Fund", EIN 41-3966108, Sheridan WY, received a ruling in 2026-02 and is also on Pub 78 ([ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/413966108.json)). This is the Wyoming re-emergence the press reported ([Chronicle of Philanthropy](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/)).
- **State action** (repo FD01; not re-researched here):
  - Georgia Secretary of State cease-and-desist and $100k penalty ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)).
  - AG suit seeking a receiver ([WSB-TV, 2026-09-25](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)).
  - Earlier profile ([AP via News4Jax, 2023-12-15](https://www.news4jax.com/business/2023/12/15/the-10-billion-charity-no-one-has-heard-of/)).
- **Reported versus filed versus counted.** The filed Schedule D says $10.10bn. That would be 4.3% of DAFRC's FY2021 market total ($234.3bn) and 4.4% of FY2022 ($229.7bn). But **EIN 46-2368538 is absent from the DAFRC panel in every year** ([DAFRC dataset](https://www.dafresearchcollaborative.org/s/Annual-DAF-Report-2025-Updated-Analysis-Dataset.xlsx)). DAFRC's vetting therefore excluded it, either deliberately or by omission; the dataset does not say which. Its exclusion is the right call for market sizing, but it means **DAFRC-based mortality cannot see the one 2020s sponsor-integrity failure**. A sponsor-mortality monitor needs to cover the whole Schedule D universe (all 990s answering yes on Part IV line 6), not a vetted list.

## 7. Limitations

- **Six years and one vintage.** Sponsor exits FY2024 onward are right-censored by imputation. DAFRC's vetting decides the universe: 6 EINs are never filed, 1,011 rows are "Included but Unsure", and SDG Impact Fund is excluded.
- **Tier B mixes real DAF exits with reporting changes.** That is the reason for three bounds. The 12 tier C cases where the text still mentions DAFs were found by a simple regex (`donor[\s-]+advised|\bDAFs?\b`).
- **The XML mirror lags.** 16 newest-return XMLs were not yet mirrored, and an earlier later return was used instead. Paper filers (pre-2021 small organisations) are visible only through ProPublica PDFs and BMF `TAX_PERIOD`, so 3 cases remain unresolved.
- **Exit assets are the last *positive filed* Schedule D value.** They can be years stale, as with NHF ($70k in FY2021 against $3.84m transferred in FY2022). Schedule N fair market values include non-DAF assets for community foundations.
- **Fiscal-year changes** were flagged (8 candidates, `fiscal_year_change_flag`). None changed the outcome, because the classification uses later returns of any period.
- **The successor and name matching is heuristic** (§3).
- **No merger press search was needed for tier A**, because the Schedule N filings themselves name the counterparties. `MANUAL_EVIDENCE` in the script is therefore empty.
- **No-invent rule.** Every number above comes from a file named in the row or the cited URL. Where a field is unavailable it is left blank, not estimated.

## 8. Data dictionary

### `sponsor-entry-exit-panel.csv` (8,751 rows; one per EIN × FY)
| Column | Meaning |
|---|---|
| `ein`…`total_daf_contributions`, `source_eoy_daf_assets` | Copied from the DAFRC panel |
| `assets_filed` | 1 if `source_eoy_daf_assets` ∈ {IRS 990, NPT historical data, paper submission} |
| `size_band` | Row's DAF assets: a <$1m, b $1–10m, c $10–100m, d $100m–1bn, e ≥$1bn, z zero/missing |
| `is_entry_year` / `is_first_obs_left_censored` | First row when FY>2019 / first row in FY2019 |
| `is_last_panel_year`, `is_last_filed_year` | Last row present / last row with filed assets |
| `is_imputed_gap` | Imputed row between filed rows |
| `is_trailing_imputed` | Imputed row after the last filed row |
| `is_period_carry_forward` | `end_of_tax_period` equals the prior FY's |
| `sponsor_exit_kind`, `sponsor_exit_fy` | panel_exit / imputation_masked_candidate / zero_daf_assets_terminal / never_filed_all_imputed, and dated exit FY |
| `sponsor_first_fy`, `sponsor_last_fy`, `sponsor_last_filed_fy` | EIN-level span |
| `sponsor_entry_class`, `sponsor_irs_ruling` | Entrant classification (§3) and BMF RULING (YYYYMM). Filled only with `--irs-dir` |
| `sponsor_exit_outcome`, `sponsor_exit_outcome_tier` | From the verification file |

### `sponsor-mortality-summary.csv` (long format)
The columns are `dimension`, `group`, `fiscal_year`, `measure`, `value`, `numerator`, `denominator` and `definition`. Dimensions:
- `all`, `type`, `subtype` and `size_band_prior_year`, with measures `at_risk_n`, `at_risk_assets`, `entries_n`, `entries_first_row_imputed_n`, `entry_assets`, and for each exit kind `exits_*_n`, `exits_*_assets`, `exit_rate_*_count` and `exit_rate_*_asset_weighted`;
- `verified`: pooled FY2020–2023 bounds;
- `verified_by_year`;
- `verified_outcome` and `verified_outcome_sample`;
- `verified_tier_by_type`;
- `entrant_class`.

Every row carries its own definition.

### `sponsor-exit-verification.csv` (100 rows; every exit candidate)
| Column | Meaning |
|---|---|
| `sample_stratum` | `top25_by_assets`, `random25` (seed 20261114), or blank. Blank rows are not ProPublica-checked |
| `exit_ref_*` | Last positive filed DAFRC values |
| `in_irs_bmf_2026`, `bmf_*` | BMF presence, status, latest tax period, filing requirement, accounting-period month, foundation code |
| `irs_revocation_*` | Auto-revocation record, if any |
| `efile_returns_after_last_filed`, `latest_later_efile_*`, `latest_main_efile_object_id` | IRS e-file index evidence |
| `later_990_daf_accounts`, `later_990_daf_assets_eoy`, `later_990_daf_ind`, `later_990_text_mentions_dafs` | Parsed from the newest available later 990 XML |
| `final_return_or_termination_ind`, `schedule_n_recipients`, `schedule_n_fmv_total` | Final-return flags and Schedule N transfers (recipient, EIN, FMV, description) |
| `propublica_*` | API presence, latest tax period, periods after the last filed period |
| `outcome`, `outcome_tier`, `true_exit`, `reporting_artifact` | Rule-based classification (§2.3) |
| `possible_successor_ein` | Name-match lead (§3) |
| `source_urls` | Every URL used for the row |

### Reproduce
```
# IRS files (≈700 MB) into DIR: eo1-4.csv, data-download-revocation.txt (unzipped), index_2019..2026.csv
python3 scripts/mission_sponsor_mortality.py                                   # panel + summary, offline
python3 scripts/mission_sponsor_mortality.py --irs-dir DIR --cache-dir CACHE --fetch   # + verification
```

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-1** (research/mission-2026-11-14/sponsor-mortality-analysis.md (§ tier-A table, TIAA row)): replace "The narrative says 244 accounts were moved into new RCF DAFs" → "A separate 2021-05-17 residual transfer of $354,551 went into 244 new RCF DAF accounts (plus $75,944 to a 'TIAA Charitable Director's Fund'); TIAA held 1,548 DAFs at FY2020 year-end"
- **W4-2** (same file (line ~149)): replace "accounts were rebuilt one-for-one at the successor (244 accounts), recurring grants did not carry over, and a reserve was held" → "the bulk ($138.46m) moved to RCF on 2021-03-09; a residual $354,551 was placed in 244 new RCF accounts in May 2021, and an $86,511 reserve was held for wind-down costs" (keep "recurring grants did not carry over" only if a source is added; this validator did not verify it)
- **W4-3** (same file (headline, line ~12)): replace "Exposure is 5,746 sponsor-years (FY2020–FY2023)" → "Exposure is 5,746 sponsor-years at risk (panel rows FY2019–FY2022, for exits dated FY2020–FY2023); exit years for imputed-trailing cases lag cessation by about a year (e.g. JRCF ceased TY2022, dated FY2023)"
- **W4-4** (same file (JRCF bullet)): replace list of four recipients → add "(Schwab $750.6m, Fidelity $548.9m, Dechomai $23.7m, Vanguard $0.05m)"
- **W4-5** (same file (Donors Fund row)): replace "The FY2024 990 reports 6,290 DAFs and $315.8m" → "The amended FY2024 990 (filed 2026-03-12) reports 6,290 DAFs and $315.8m; the original TY2023/TY2024 returns omitted Schedule D Part I. DAFRC's flag is 'Assume Sponsor Closed 2023'"
