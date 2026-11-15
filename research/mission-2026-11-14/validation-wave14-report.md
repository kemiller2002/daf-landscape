# Validation wave 14: batch 29 claims (FIT ledgers, regulation and litigation, crypto, complaints and voids)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave14.
**Register:** [`validation-register-wave14.csv`](../../data/mission-2026-11-14/validation-register-wave14.csv), rows V14-01 to V14-30 (V14-27 is split into 27a and 27b).
**Method:** public sources only. I did not log in, submit forms or contact anyone. I formed each verdict from primary sources first and compared it with the batch-29 documents afterwards. The sources were:
- court PDFs in CourtListener RECAP storage (Docs 1, 32, 34, 39, 42, 45, 55, 58), with a 404 probe of Docs 47–70;
- statutes and IRS texts: Cal. Gov. Code §12599.9, 11 CCR 314, Rev. Proc. 2011-33 (IRB 2011-25) and Rev. Proc. 2018-32 (IRB 2018-23);
- the Candid licence and developer docs;
- SEC 10-Ks, Fidelity Charitable Giving Reports 2022–2026, and the CA AG and Alaska Dept. of Law releases;
- IRS e-file XML from the GivingTuesday mirror: Endaoment, GKCCF, AEF, Fidelity, ImpactAssets, NPT and BofA;
- vendor and sponsor pages: NPact, REPAY, BILL, Blackbaud help, GWCF, IRCF, Greater Horizons and JobTarget;
- dns.google.

**Scripts re-run** in a scratch copy of the repo, so no repo data file was overwritten:
- `scripts/mission_complaint_rates.py`: its output is byte-identical to `complaint-rates-normalised.csv`.
- `scripts/mission_void_scan.py`: re-run with a fresh extract cache, fetching 581 returns from the mirror. The 837 rows and the summary CSV are identical to the repo files.
- **Recall check:** I also wrote my own check, which re-reads every `ExplanationTxt` in the 670 parsed returns of the 171 non-disclosing sponsors with a wider regex.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V14-01 | SVCF is the only NetSuite + FIT sponsor; no new family | **Confirmed with nuance** | The story implies, but never states, FIT running on NetSuite at SVCF. EN001 types FIT as `ledger_provider`, which contradicts the doc's own overlay rule. |
| V14-02 | CFGP FIT → FE NXT; FFTC tag-only on FE NXT | **Confirmed** | Quoted text matches. FFTC's story describes selection and transition but gives no go-live date. |
| V14-03 | AEF NPact "SOFTWARE DEVELOPMENT" $206,682 / $217,016 / $249,500 | **Confirmed** | TY2024 XML read directly. |
| V14-04 | GKCCF audit service income $1,806,759 / $1,915,649 / $3,035,924 | **Confirmed** | Back-office text and the 2025-11-12 signing date match. |
| V14-05 | GKCCF 990 SERVICE INCOME $5,562,451 / $6,127,929; 21 Sch. R orgs | **Confirmed** | The gap explanation is [I]. |
| V14-06 | IRCF is a GKCCF back-office client "confirmed by its tenant"; moved to Foundant | **Partially confirmed** | The first-party link proves IRCF used the donor-portal.org portal, not GKCCF accounting. Both the `ircf.donor-portal.org` and `indianriver.fcsuite.com` logins are still linked. |
| V14-07 | Greater Horizons on `gh.donor-portal.org` | **Confirmed** | |
| V14-08 | FFTC, GWCF and CFGP: Foundation Cloud + FE NXT, $3.37bn; spectrumportal.net not wildcard-hosted | **Confirmed with nuance** | NXDOMAIN for a random label; SOA is `fusdns03.fusionlabs.net`. GWCF's FE NXT is inferred, and the year of its portal launch comes from the FAQ. |
| V14-09 | REPAY (2023-11-15) → BILL (2026-09-29); "switch from REPAY to BILL"; GWCF Sept 2026 | **Confirmed** | BILL is still early-adopter only. Industry report §11.3 needs an update. |
| V14-10 | NYCT JobTarget 2026-08-01: Sage Intacct and Salesforce "preferred" | **Confirmed** | The ERP transition remains [S]/[R]. |
| V14-11 | Peterson v. WaterStone pending; MTD fully briefed 2026-05-26; stay denied 2026-06-11; productions due 2027-02-14 | **Confirmed** | Doc 45: "Motion to Stay at ECF No. 39 … DENIED". Doc 39 is a *partial* stay motion. Nothing in RECAP after Doc 58. |
| V14-12 | Greenleaf's "dismissed for standing" refers to Pinkert | **Confirmed** | Greenleaf (2026-02-26) treats Peterson as open. |
| V14-13 | Doc 1 fund balance $21,071,102 (2023-12-31) | **Confirmed** | Doc 1 ¶13. |
| V14-14 | AB 488: conditional DAF exclusion; vendor excluded only if it "solely" provides technical services; registration from 2024-06-12 | **Confirmed** | §12599.9(a)(2)(B) and (C) quoted. |
| V14-15 | Hawaii regime from 2026-07-01 | **Confirmed (secondary)** | |
| V14-16 | Only CT, NJ, OH, GA and IL tie counsel bond to custody | **Partially confirmed** | True within the 18-state sample. The same survey shows custody-triggered counsel bonds in MN, NH, RI and LA too. |
| V14-17 | CA AG v. Flipcause | **Confirmed** | Post-order status is unresolved: the CSV says bankruptcy, the .md says appeal. |
| V14-18 | Alaska v. six platforms | **Confirmed with wording fix** | The release says "Pledge to", not "Pledgeling". |
| V14-19 | Candid licence §4.c.v "cease … all use"; no retention carve-out; §10.l | **Confirmed with nuance** | Parallel cease clauses appear at §4.a.ii, §4.b.ii and §4.d.v(1). §3.f covers books of account only. |
| V14-20 | Rev. Proc. 2011-33 §4(2) is current law | **Contradicted (citation); substance confirmed** | Rev. Proc. 2018-32 superseded 2011-33 from 2018-05-16. The retention rule survives as §8.01(2): "retains a paper or electronic copy of the report". |
| V14-21 | §4966 regulations still proposed | **Confirmed (absence)** | |
| V14-22 | Fidelity crypto >$330M → $38M → $49M → $786M → $362M | **Confirmed** | −88.5% and −53.9%, computed. |
| V14-23 | TGB earnout $10.4M ($2.8M cash, $7.6M equity); max $246M; FV $57.8M | **Confirmed** | The FY2022 year-end liability is $10.9M in one note and $10.7M in another. |
| V14-24 | Endaoment FY6/24: 99.7% crypto; FY6/23 anomaly | **Confirmed** | 29,789,402 / 29,879,802. FY6/22 also shows Sch. D above Part VIII. The FY6/25 return is now indexed (202631359349315978) but not yet mirrored. |
| V14-25 | Complaint rates (Daffy 11.2, Vanguard 5.4, Fidelity 2.3/1.1, pooled 1.9/1.3) | **Confirmed with nuance** | The arithmetic is exact. "Most of the big three's high-severity weight is SPLC" is false for Fidelity on all venues (6 of 21). |
| V14-26 | Fidelity 204,614 accounts | **Confirmed** | |
| V14-27a | Void scan is reproducible | **Confirmed** | Identical output. The void-share n is 70, not 72, because of the redacted returns. |
| V14-27b | 29 sponsors (14.5%) disclose | **Contradicted (undercount)** | At least 5 sponsors are missed: Greater Houston, Maine, Fox Valley, the Fund for Charitable Giving and Vermont. That gives ≥34/200 = **17.0%** (16.5% without Vermont's "adjustments"). |
| V14-28 | ImpactAssets $7,441,360 (3.3%); BofA $125k | **Confirmed** | BofA's item is also described as "STOP PAYMENT ON GRANT". |
| V14-29 | ImpactAssets → NPT $160,826,426, a single line | **Confirmed with nuance** | A second NPT-EIN line ($10,000 FBO UBS Optimus) is also present. |
| V14-30 | NPT → ImpactAssets $22,856,124 / $40,638,414 | **Confirmed** | |

**Comparison with the batch-29 documents.** After forming these verdicts I compared them with the three documents. They match my figures except in five places:
- the superseded Rev. Proc. citation (V14-20);
- the void-scan undercount (V14-27b);
- the IRCF back-office overstatement and EN001 typing (V14-06, V14-01);
- the custody-trigger generalisation (V14-16);
- three wording points: "Pledgeling", "1 line" and the Fidelity SPLC weighting (V14-18, V14-29, V14-25).

The headline legal characterisations hold: Peterson is pending, the AB 488 DAF exclusion is conditional, and the Candid licence has no retention carve-out.

## Recall check detail (V14-27b)

These filed items carry a figure but sit outside the scan's hit rule:

| Sponsor (type, FY2024 rank) | Label | TY2021 | TY2022 | TY2023 | TY2024 |
|---|---|---|---|---|---|
| Greater Houston CF (CF, 33) | RECOVERY OF PRIOR YEAR GRANTS | 368,949 (0.22%) | 1,399,434 (0.31%) | 1,118,739 (0.52%) | 3,500,651 (1.38%) |
| Maine CF (CF, 88) | Recovery of prior year grants | 78,139 (0.18%) | 121,710 (0.22%) | 58,228 | 410,914 |
| CF for the Fox Valley (CF, 98) | GRANT RETURNS | 60,139 (0.29%) | 33,852 (0.11%) | 624,956 (2.64%) | — |
| The Fund for Charitable Giving (national, 130) | RECOVERY OF PRIOR YEAR GRANTS PAID | — | — | (1,700) | — |
| Vermont CF (CF, 152) | PRIOR YEAR GRANT ADJUSTMENTS | — | — | — | 307,453 (0.63%) |

The corrected floor:
- **Sponsors:** 34/200 = 17.0%.
- **By type:** nationals 10/43 = 23.3%; community foundations 21/113 = 18.6%; single-issue charities unchanged at 3/44.
- **Returns:** 85/785 = 10.8%.
- **Disclosers' share of DAF assets:** about 38.0%.

All other matches from my wider regex were "avoid", conflict-of-interest or policy text. The check covers only the non-disclosers' explanation text, so 17.0% is still a floor.

## Exact corrections

### `research/mission-2026-11-14/queue-batch29-regulation-litigation-crypto.md`
1. **Line 35 (§1, P-TRM-04).**
   - Replace: "**Rev. Proc. 2011-33 §4(2)** makes reliance on third-party BMF data conditional on the grantor retaining \"a copy of the report\"."
   - With: "**Rev. Proc. 2018-32 §8.01(2)** makes reliance on third-party BMF data conditional on the grantor retaining \"a paper or electronic copy of the report\". (Rev. Proc. 2018-32 superseded Rev. Proc. 2011-33, whose §4(2) is cited by Candid's FAQ, from 2018-05-16.)"
2. **Line 183 (§4.1 IRS).**
   - Replace the "Rev. Proc. 2011-33 §4" bullet with: "**Rev. Proc. 2018-32 §8.01** ([IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB)), which \"modifies and supersedes … Rev. Proc. 2011–33\" (effective May 16, 2018). Reliance on third-party EO BMF data requires two things. (1) The report must include name, EIN and foundation status, deductibility, \"the revision date of the EO BMF Extract containing the information\", and the date and time provided. (2) \"The grantor or contributor retains a paper or electronic copy of the report.\" Candid's FAQ still cites the superseded Rev. Proc. 2011-33."
3. **Line 197 (§4.2, Unknowns).** Replace "that §4(1)(B) requires" with "that Rev. Proc. 2018-32 §8.01(1)(b) requires".
4. **Line 283 (R26).** Replace the row with: "| R26 | [Rev. Proc. 2018-32, IRB 2018-23](https://www.irs.gov/irb/2018-23_IRB) (supersedes [Rev. Proc. 2011-33, IRB 2011-25](https://www.irs.gov/irb/2011-25_IRB)) | 2018-05-16 (current) | §4 |".
5. **Line 34 (§1, P-FAIL-08) and line 144 (§3.4 item 1).**
   - Replace: "only CT, NJ, OH, GA and IL tie the bond" / "in only about five of 18 states (CT, NJ, OH, GA, IL)"
   - With: "of the 18 states sampled, only CT, NJ, OH, GA and IL tie the bond … (the same 2023 survey shows custody-triggered counsel bonds in MN, NH, RI and LA, which are outside the sample, so this is not a national ratio)".
6. **Line 75 (§2.2 Alaska).** Replace "JustGiving, Pledgeling and Network for Good" with "JustGiving, Pledge (\"Pledge to\" in the release) and Network for Good".
7. **Line 215 (§5.1, Endaoment row, FY6/25 cell).** Append: "The FY6/25 990 (202631359349315978) is in the 2026 IRS index but not yet on the mirror. FY6/22 also shows Sch. D DAF contributions ($43.24M) above Part VIII ($41.34M)."

### `research/mission-2026-11-14/queue-batch29-complaints-voids.md`
1. **Line 31 (§1, P-B28-02).**
   - Replace: "**29 sponsors (14.5%) itemise at least one grant void, refund, rescission or reversal with a figure**, in 72 of 785 returns (9.2%). Those 29 hold **37.5%** of scanned top-200 DAF assets."
   - With: "**The scan's hit rule finds 29 sponsors (14.5%), in 72 of 785 returns; validation wave 14 found at least 5 more that it misses** (\"recovery of prior year grants\": Greater Houston, Maine, the Fund for Charitable Giving; \"grant returns\": Fox Valley; \"prior year grant adjustments\": Vermont). The floor is therefore **at least 34 sponsors (17.0%)** in 85 returns (10.8%), holding about 38.0% of scanned DAF assets."
   - Also replace "nationals 9 of 43 (20.9%), community foundations 17 of 113 (15.0%)" with "nationals at least 10 of 43 (23.3%), community foundations at least 21 of 113 (18.6%)".
2. **§3.1 Hit rule.** Append: "Known misses (wave 14): 'recovery of prior year grants', 'grant returns', 'prior year grant adjustments'."
3. **§3.2 table.** Add a footnote: "Rates are floors; see validation-wave14-report.md for 5 missed sponsors. Void-share statistics use n = 70 returns (two SVCF returns are redacted)."
4. **Lines 187–188 (§3.4).** Replace "Nationals: 21% disclose, median 0.15%." and "Community foundations: 15% disclose, median 0.28%." with "Nationals: at least 23% disclose, median 0.15%. Community foundations: at least 19% disclose, median about 0.28%."
5. **Line 30 (§1, P-QA3-04).**
   - Replace: "Most of the big three's high-severity weight comes from the six shared 2026 SPLC records (CMP-215–220)."
   - With: "The six shared 2026 SPLC records (CMP-215–220) supply most high-severity weight for Vanguard (6 of 8) and DAFgiving360 (6 of 9). For Fidelity they supply 6 of 21 on all venues (11 are App Store login reviews) and 6 of 10 without the App Store."
6. **Line 198 (§4 table).** Replace "1 line; the largest of 2,733 lines" with "the one general-support line (a second NPT-EIN line, $10,000 'FBO Friends of UBS Optimus Foundation', also appears); the largest of 2,733 lines".

### `research/mission-2026-11-14/queue-batch29-fit-ledgers.md`
1. **Line 43 (§0, P-LDG-02).**
   - Replace: "One former or current client is confirmed by its tenant (Indian River CF), and IRCF now appears to have moved to Foundant."
   - With: "One sponsor outside the GKCCF family, Indian River CF, is confirmed as a donor-portal.org portal tenant by its own site. Back-office accounting for IRCF is not shown. IRCF now links both `ircf.donor-portal.org` and Foundant's `indianriver.fcsuite.com`, so it is moving or running both."
2. **Line 64 (§1.1 table, SVCF row).** Replace "FIT layered on NetSuite instead of a custom app" with "FIT used instead of a custom app that 'would layer on top of NetSuite' (a FIT–NetSuite integration at SVCF is implied, not stated)".
3. **Line 138 (§2.3 Reading).** Replace "IRCF has moved, or is moving, from the GKCCF back office to Foundant CommunitySuite." with "IRCF has moved, or is moving, from the GKCCF donor portal to Foundant CommunitySuite. Its homepage still links both logins."

### `research/mission-2026-11-14/daf-user-complaints-deep-research.md`
1. **Line 238 (§5.5 Status).**
   - Replace: "**Status: sources conflict.** Foley (May 2026) describes the motion to dismiss as pending … A Greenleaf Trust note suggests dismissal for standing ([Greenleaf](…))."
   - With: "**Status: pending (D. Colo. No. 1:26-cv-00179-GPG-MDB).** The motion to dismiss the First Amended Complaint (Doc 34, 2026-04-21) has been fully briefed since 2026-05-26 (Doc 42). The court denied the motion for a partial stay of discovery on 2026-06-11 (Doc 45). Final productions are due 2027-02-14 (Doc 55). No ruling appears in RECAP through Doc 58 (2026-10-15). Greenleaf's 'dismissed for standing' refers to *Pinkert*, not Peterson [V wave 14]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **Line 517 (§11.3).**
   - Replace: "Outside the top 30, Greater Washington (#38) has used Blackbaud and REPAY (two separate firms) since Sept 2026 [V wave 7]."
   - With: "Outside the top 30, Greater Washington (#38) has paid grants through Blackbaud and REPAY since Sept 2026 [V wave 7]. REPAY is the embedded payments rail of Blackbaud Financial Edge NXT, and Blackbaud named BILL as its successor on 2026-09-29 (early adopters only) [V wave 14]."
2. **Line 671 (§11.6).** Append: "The earnout (maximum $246m; $57.8m fair value at acquisition) settled at $10.4m. Fidelity Charitable's crypto inflow fell 88% in 2022 and 54% in 2025 [V wave 14]."
3. **Line 588 (§11.4, Candid).** After "licensees must stop all use of the data", add: "The licence has no retention carve-out, while the IRS third-party reliance rule (Rev. Proc. 2018-32 §8.01(2)) requires grantors to retain the report [V wave 14]."
4. **Industry report block (new short paragraph for §11.7 or §11.8):**

   > **Batch 29 (validated, wave 14).** Peterson v. WaterStone is pending in discovery, with the MTD fully briefed and final productions due 2027-02-14. It is the first 2021+ successor-adviser suit to get this far; Pinkert and Fairbairn failed. California's AB 488 excludes a DAF sponsor only if it does not name charities to non-advisers, and excludes a vendor only if it "solely" provides technical services. Public complaint rates per 10,000 accounts (Daffy 11.2, Vanguard 5.4, Fidelity 2.3, DAFgiving360 1.3) measure venue coverage, not service quality. At least 17% of the top 200 sponsors itemise grant voids, refunds or recoveries on their 990s (median about 0.3% of grants). That reflects accounting presentation, not void incidence. ImpactAssets' $160.8m CY2024 line to NPT is most likely a donor-recommended DAF-to-DAF transfer; NPT sent $63.5m the other way over FY2024–25.

## Data-file notes (not .md; for the owning agent)

- **`relationship-graph-edges-additions-14.csv`:**
  - EN001: change `relationship_type` from `ledger_provider` to `technology_provider` and note "fund-accounting overlay on the NetSuite GL", per §1.3 of the batch doc.
  - EN011: change `status` from `historically_confirmed` to `reported`, with evidence "donor-portal.org portal tenant (first-party link); back-office service not shown".
- **`queue-proposals-batch29b.csv` P-B29B-03** (and its copies in `research-priority-inputs.csv` and `research-priority-queue.csv`): replace "Rev. Proc. 2011-33 sec. 4(1)" with "Rev. Proc. 2018-32 sec. 8.01(1)".
- **`daf-litigation-2021plus.csv` LIT-06:** the "Flipcause in bankruptcy (2025-12)" status conflicts with the .md's appeal of 2025-12-12. Neither was verified here; carry both, labelled [S].
- **`daf-grant-voids-top200*.csv`:** add the three missing labels to `VOID_RX` in `scripts/mission_void_scan.py` and re-run. The expected result is 34 disclosing sponsors (see the recall table).

## Limits

- **RECAP coverage.** A later order on the MTD may exist outside RECAP.
- **State law.** The state custody findings rest on the 2023 survey. The NY §171-a page returned 403 to scripts and was not re-read.
- **Recall check.** It used one alternative regex over explanation text only, so the 17.0% disclosure rate is a floor, not a census.
- **Not re-checked:** The Giving Block's 2021 volume ($69.6M, from a BusinessWire release that returned 403) and its 2026 report figures.
