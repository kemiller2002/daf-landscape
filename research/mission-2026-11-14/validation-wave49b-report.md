# Validation wave 49B: private-foundation-to-DAF flows; fraud and diversion controls

**Validator:** validator wave 49B · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave49b.csv`](../../data/mission-2026-11-14/validation-register-wave49b.csv) (33 rows, V49B-01 to V49B-33)

**Studies validated**
- b49-01, PF-to-DAF flows: [`b49-01-pf-to-daf-flows.md`](b49-01-pf-to-daf-flows.md), `pf-to-daf-flows-2026-11-20.csv`, `scripts/mission_pf_to_daf_flows.py`, and the build's summary JSON in the session scratchpad.
- b49-04, fraud and diversion controls: [`b49-04-fraud-diversion-controls.md`](b49-04-fraud-diversion-controls.md), `fraud-diversion-controls-2026-11-20.csv`, `scripts/mission_b49_04_fraud_controls_build.py`, `scripts/mission_b49_04_doj_scan.py`.

## 1. Method

- **b49-01 recompute.** Every headline figure was recomputed from the CSV with a separate script: tier totals by year, distinct PFs, shares of the DAFRC-corrected contribution totals, concentration, wind-down counts and dollars, the conversion-signature test and the per-sponsor numerators. The results were compared with the summary JSON and with the §3.4 table (30 rows parsed).
- **b49-01 raw XML.** 37 matched rows were re-read in the raw 990-PF XML from the GivingTuesday mirror. The sample was drawn with a new seed: 14 T1, 8 T2 and 10 T3 rows, plus the 4 largest T1 rows and the Cognizant row. Each recipient line was checked for name, address and amount. The 8 largest J.P. Morgan Charitable Giving Fund rows were also re-read for their filed address.
- **b49-01 recall.** The study's own `match_line` was re-run, read-only, over every cached candidate line for TY2022–24. Unmatched lines that carry a T1 brand word were then classified by hand rules. The harvest candidate filter keeps every line with a brand word, so the cache is complete for this test.
- **b49-04 rebuild.** The build script was run into a scratch root, not the repo. Its CSV is byte-identical to the committed CSV, and every printed share matches the note.
- **b49-04 sources.** The Fidelity security-code and nonprofit FAQ pages, the Vanguard security center, the Ren claim help page, the BofA Private Bank article, the IC3 2025 report (pdftotext) and PSA, and the FinCEN release were all fetched again.
- **DOJ method.** The DOJ API was queried at page 0, at the 2021 cutoff boundary (pages 2361 and 2362), and with a `keyword=` parameter. A binary search by date found the N.D. Tex. release; it is on page 110.
- **Constraints.** No commit or push. No fetch from sec.gov, donorportal.cct.org, ncfgiving.com, charitynavigator.org, or the Foundant and fcsuite hosts. User agent `research-script/1.0`. A path was fetched only when `*`, `research-script/1.0`, ClaudeBot, anthropic-ai, Claude-User, Claude-Web and Claude-SearchBot were all allowed.

### robots.txt log (2026-11-20)

| Host | robots.txt | Use |
|---|---|---|
| gt990datalake-rawdata.s3.amazonaws.com | 404 (NoSuchKey): no rules | 47 XML reads |
| www.justice.gov | 200; no Claude or Anthropic groups; `/api/` not disallowed | API pages 0, 2361, 2362, about 15 binary-search pages, one keyword test |
| www.fidelitycharitable.org | 200; all listed agents allowed | 2 pages |
| www.vanguardcharitable.org | 200; all allowed | 1 page |
| intercom.help | 200; all allowed | 1 page |
| www.ic3.gov | 200; all allowed | PSA and 2025 report |
| www.fincen.gov | 200; all allowed | 1 release |
| www.privatebank.bankofamerica.com | 200; all allowed | 1 article |

## 2. Counts

| Result | b49-01 | b49-04 | Total |
|---|---|---|---|
| Confirmed | 13 | 12 | 25 |
| Partially confirmed | 3 | 4 | 7 |
| Contradicted | 1 | 0 | 1 |
| Unverifiable | 0 | 0 | 0 |
| **Rows** | **17** | **16** | **33** |

## 3. Findings

### 3.1 b49-01, PF-to-DAF flows: accept, with recall, wording and privacy fixes

**Numbers reproduce exactly** (V49B-01 to -11).
- **Census.** The frame has 371,404 rows, which are 371,359 unique (EIN, period) returns. 371,358 were parsed.
- **T1 flow.** $2,550,316,657, $2,964,787,938 and $3,912,890,569; $9.43bn in all from 2,801 PFs.
- **Shares of DAF contributions.** 3.33%, 4.54% and 4.22%.
- **Concentration.** Top 10 hold 30.87% and top 100 hold 64.68%.
- **Wind-downs.** 8,020 flagged returns; 877 gave to sponsors; $1.220bn, which is 7.03% of T1-T3 (T1: 7.92%).
- **Conversion signatures.** 962 return-years meet the test, 524 flagged and 438 unflagged.
- **Per-sponsor shares.** 30 of 30 table rows match the JSON, and the numerators recompute from the CSV.
- **Robustness.** Alias/EIN-only matching keeps 80.0%, 80.9% and 81.4% of T1.

**Precision.** All 37 rows re-read in raw XML are correct (V49B-12), so the 95% lower bound on precision is about 91%.
- **Cognizant.** The TY2022 return carries both `FinalReturnInd` and `PFStatusTermSect507b1AInd`. Its line pays $35,591,821 to the BNY Mellon Charitable Gift Fund, with the purpose “transfer of funds to newly created DAF to finalize …”.
- **T2 is mixed,** as the study says. Sampled T2 recipients include Kiva Microfunds and a small fiscal-sponsor foundation.

**Wording: “largest single lines.”** $276.0m and $257.5m to NPT are return-sponsor rows, not single lines (V49B-06).
- The $276.0m row is two lines: $275.0m and $1.0m.
- The $257.5m row is three lines: $242.5m, $10m and $5m.
- The Schwab $218.0m and $220.7m figures are single lines.

**Recall is the weaker side** (V49B-13).
- **T1 brand misses.** About 565 cached lines name a T1 brand but miss the aliases through misspelling or abbreviation, for example “FIDELITY INV CHARITABLE GIFT FUND”, “GOLDMAN SACHS PHILANTHROPHY FUND”, “SCHWAB FUND FOR CHARITABLE GIVING” and “TROWE PRICE - DONOR ADVISED FUND”. They total $188.4m: $63.6m, $55.9m and $68.9m by year, about 2.0% of T1. T1 is therefore a floor.
- **T2 and T3 misses:**
  - Tides Foundation: lines with a NY address fail the state rule;
  - St Louis Community Foundation: two panel EINs share the name;
  - Community Foundation of Sarasota County: a $9.0m line sits in T0.

**T0** (V49B-03).
- **Concentration.** One foundation's two lines ($291.6m and $141.1m) are 47% of the $0.92bn.
- **Attribution.** A few T0 lines do name a sponsor. T0 is better read as “DAF-labelled, mostly unattributed”.

**T1 tier choice: reasonable, but it is material** (V49B-14).
- **Effect.** NCF, JCF and DonorsTrust add $1.13bn, which is 12% of T1. Thrivent adds $0.
- **Without them,** T1 is $8.29bn: 2.8%, 4.0% and 3.8% of contributions.
- **Reporting.** These sponsors are predominantly DAF administrators, so the choice is defensible, but the sensitivity should be shown.

**J.P. Morgan Charitable Giving Fund → NPT: confirmed** (V49B-15).
- **Filed addresses.** Six of the eight largest rows give NPT's Jenkintown, PA address. The $161.5m line writes “National Philanthropic Trust” in the address line.
- **Repo edges.** E095–E097 in the relationship graph cite J.P. Morgan's own statement that NPT administers the fund.

**Double counting: none against the DAF-to-DAF figures** (V49B-16).
- **No overlap.** The two files read different schedules: Schedule I of Form 990 for DAF-to-DAF, and Part XV of Form 990-PF here. A PF grant to a sponsor is correctly treated as a contribution into the DAF system, not as a DAF grant.
- **Edge case.** Two DAFRC-panel sponsors filed 990-PFs. Jasper Ridge's final §507(b)(1)(A) return sends $4.2m to Schwab and Fidelity, and Every.org sends $0.5m to processors. That $4.7m (0.03% of T1-T3) is sponsor-to-sponsor in substance.

**Privacy: contradicted** (V49B-17).
- **What leaks.** The CSV keeps names that lead the string, so cutting at the first separator does not remove them. Some `recipient_name_filed` values name individual account holders, such as a Fidelity giving account “of” a named couple and a Schwab fund with two named donors. Some `purpose_text` values name family DAFs and in-memory honourees.
- **Scale.** A tight heuristic flags 176 rows.
- **Foundation names** are organisations and are fine.
- **Fix.** Redact before wider use. The validator did not edit the CSV; the decision is listed for the owner.

### 3.2 b49-04, fraud and diversion controls: accept, with two stale figures and one interpretation note

**Shares reproduce** (V49B-18 to -20). Notices: 3 sponsors, 52.0%. MFA: 3, 52.0%. Bank-change verification: 2, 29.8% (26.41% + 3.35% = 29.76%).
- **Stale figure.** Two passages still say controls are published at sponsors holding **53.8%**. That is Fidelity + NPT + Vanguard + CCT, the figure from before FDC-24 was withdrawn (V49B-33).
- **NPT's MFA evidence.** It is a one-time code at online account opening, not login MFA. On login MFA alone the share is 2 sponsors, 35.2%.

**Quotes confirmed in fresh downloads:**
- Fidelity's step-up code for “setting up new bank instructions or modifying a user's contact information” (V49B-21);
- Vanguard's “MFA is now required for all web-registered Vanguard Charitable users” (V49B-22);
- Fidelity's FAQ, “a voided check or bank letter dated within the last 12 months”, against the PR01 form's voided-check requirement (V49B-23);
- the BofA Private Bank widget warning (V49B-29).

**Ren** (V49B-24). The three claim checks are confirmed. The page also lists a fourth route, a registration code printed on a grant check.

**Federal figures** (V49B-25 to -27).
- **IC3 2025:** Charity 662 complaints and $7,907,609, with 2023 and 2024 marked “*”. Complainants aged 60+: 126 and $3,474,668.
- **IC3 PSA:** “more than 4,500 complaints … approximately $96 million”.
- **FinCEN:** 15,417 reports from 841 institutions, more than $688 million.

**DOJ** (V49B-28, -30). The method is confirmed:
- `/api/` is robots-allowed;
- `keyword=` is ignored (identical results and count);
- page 2361 begins at 2020-12-31, so 2,361 pages × 50 = 118,050 releases cover the window.

The full scan was not re-run, so the zero is method-confirmed only.
- **N.D. Tex. 2026-08-14 indictment.** It alleges that an elected official who also served as trustee and executor diverted about $308,000, including $133,000 from a town community foundation. It has no DAF wording.
- **Minor.** The CSV FDC-46 note says “eight sponsor names”; the script screens ten sponsor or program names.

**Safety** (V49B-31, -32).
- **Schemes.** Only one-line labels appear, as the sources word them. Control gaps are stated at policy level.
- **Names.** No individual is named. The release URL gives role and town only.

## 4. Accept / modify / reject

| Study | Item | Decision | Reason |
|---|---|---|---|
| b49-01 | Census, tier totals, shares, concentration, wind-downs, 438 signatures | Accept | Recomputed exactly from the CSV |
| b49-01 | Cognizant row | Accept | Raw XML: final and §507(b)(1)(A); $35.6m to BNY Mellon CGF |
| b49-01 | Per-sponsor PF shares | Accept | 30/30 rows match; numerators recompute |
| b49-01 | Precision (“no false positive”) | Accept | 37/37 raw-XML re-reads correct |
| b49-01 | “Largest single lines” | Modify | $276.0m and $257.5m are multi-line rows |
| b49-01 | Recall | Modify | About $188m (2.0% of T1) of brand-named lines unmatched; T1 is a floor |
| b49-01 | T0 description | Modify | 47% from one PF; some lines name panel sponsors |
| b49-01 | T1 tier with NCF, JCF, DonorsTrust, Thrivent | Accept, with sensitivity | +$1.13bn (12%); show the $8.29bn figure |
| b49-01 | JPM CGF → NPT | Accept | Filed addresses and repo edges agree |
| b49-01 | Double counting vs DAF-to-DAF | Accept, with note | No overlap; $4.7m sponsor-filed 990-PF edge case |
| b49-01 | Privacy statement and CSV text fields | Reject as stated | Individual donor names remain in two text fields; redact |
| b49-04 | Coverage shares (52.0%, 52.0%, 29.8%) | Accept | Build re-run byte-identical |
| b49-04 | “53.8%” in §0 and §5 | Modify | Pre-withdrawal figure; should be 52.0% |
| b49-04 | MFA count including NPT | Accept, with note | NPT code is at registration; strict login MFA 35.2% |
| b49-04 | Fidelity, Vanguard, BofA quotes; voided-check conflict | Accept | Re-matched live |
| b49-04 | Ren “three checks” | Modify | Fourth route via grant-check code |
| b49-04 | IC3, PSA, FinCEN figures | Accept | Exact |
| b49-04 | DOJ screen and N.D. Tex. case | Accept | Method and boundary reproduced; case confirmed |
| b49-04 | No evasion methods; no individuals | Accept | Checked |

## 5. Limits

- The DOJ screen was not re-run end to end. Only its pages, boundary and filter behaviour were tested.
- The recall classification of brand-named lines uses hand rules. It may keep a few non-sponsor lines, such as bare “Charles Schwab” or “Bessemer Trust” lines that could be brokerage accounts, and it may drop a few NCF regional affiliates that are separate EINs.
- The individual-name count (176 rows) is a heuristic. It misses names without a middle initial, and it includes a few named programmes.
- The ml.com copy of the BofA article and Fidelity's security.html were not re-read. The CCT donor portal was not fetched, by rule.

## Exact corrections

### `research/mission-2026-11-14/b49-01-pf-to-daf-flows.md`

**Find:** "The largest single lines include:"
**Replace with:** "The largest return-sponsor rows (one PF return to one sponsor, filed lines summed; the largest single filed lines are $275.0m in TY2022 and $242.5m and $235.0m in TY2024, all to NPT) include: [V wave 49B]"

**Find:** "- $161.5m to the J.P. Morgan Charitable Giving Fund (NPT program)."
**Replace with:** "- $161.5m to the J.P. Morgan Charitable Giving Fund (NPT program; the filed address line reads National Philanthropic Trust, Jenkintown PA). [V wave 49B]"

**Find:** "Their sponsor grants, if any, are missed. [F]"
**Replace with:** "Their sponsor grants, if any, are missed. [F]\n\n**T0 concentration.** One PF’s two lines ($291.6m in TY2024 and $141.1m in TY2023) are 47% of T0, and a few T0 lines do name a panel sponsor (for example Community Foundation of Sarasota County, $9.0m), so T0 is mostly, not wholly, unattributed. [V wave 49B]"

**Find:** "These are flows into the DAF system from outside it, not double counts within it. [I]"
**Replace with:** "These are flows into the DAF system from outside it, not double counts within it. [I] Validator check: the DAF-to-DAF file reads Form 990 Schedule I and this file reads 990-PF Part XV, so no row is in both. Two DAFRC-panel sponsors filed 990-PFs: Jasper Ridge Charitable Fund (final §507(b)(1)(A) return, TY2023, $4.2m to Schwab and Fidelity) and Every.org (TY2024, $0.5m to T2 processors); those $4.7m are sponsor-to-sponsor transfers in substance (0.03% of T1-T3). [V wave 49B]"

**Find:** "  Together these come to about 2% of the T1-T3 total ($349m of $17.34bn)."
**Replace with:** "  Together these come to about 2% of the T1-T3 total ($349m of $17.34bn).\n- **Brand-name misses (validator).** Re-running `match_line` over every cached candidate line leaves about 565 lines and $188m over three years ($64m, $56m and $69m) that name a T1 brand in a misspelt or abbreviated form (for example “FIDELITY INV CHARITABLE GIFT FUND”, “GOLDMAN SACHS PHILANTHROPHY FUND”, “SCHWAB FUND FOR CHARITABLE GIVING”, “TROWE PRICE - DONOR ADVISED FUND”). That is about 2.0% of T1, so T1 is a floor. T2-T3 misses include Tides Foundation (state rule), St Louis Community Foundation (two panel EINs share the name) and Community Foundation of Sarasota County. [V wave 49B]"

**Find:** "which changed T1 by under 1.5%."
**Replace with:** "which changed T1 by under 1.5%. An independent re-read of 37 matched rows in raw XML (14 T1, 8 T2 and 10 T3 drawn with a new seed, the 4 largest T1 rows and the Cognizant row) found all 37 correct; the 95% lower bound on precision is about 91%. [V wave 49B]"

**Find:** "  - NCF, JCF and DonorsTrust also hold some non-DAF funds."
**Replace with:** "  - NCF, JCF and DonorsTrust also hold some non-DAF funds. Without the four judgment additions (NCF, JCF, DonorsTrust, Thrivent), T1 is $2.17bn, $2.61bn and $3.52bn ($8.29bn), or 2.8%, 4.0% and 3.8% of DAF contributions; Thrivent receives nothing in any year. [V wave 49B]"

**Find:** "No individual is profiled."
**Replace with:** "No individual is profiled. However, the cut keeps names that lead the string: the validator found individual donor or account-holder names in `recipient_name_filed` (named giving accounts and named funds) and in `purpose_text` (named family DAFs, in-memory purposes), about 176 rows on a tight name heuristic. Before wider use, blank `purpose_text` or replace it with a DAF flag, and cut `recipient_name_filed` to the matched sponsor brand. [V wave 49B]"

### `research/mission-2026-11-14/b49-04-fraud-diversion-controls.md`

**Find:** "those checks are published at sponsors holding 53.8% of top-20 assets"
**Replace with:** "those checks are published at sponsors holding 52.0% of top-20 assets (35.2% on login MFA alone, without NPT’s registration code) [V wave 49B]"

**Find:** "| Login MFA or one-time code published as required or prompted | 3 | 52.0% |"
**Replace with:** "| Login MFA or one-time code published as required or prompted | 3 | 52.0% |\n| … login MFA only (Fidelity, Vanguard; NPT’s code is at account opening) | 2 | 35.2% [V wave 49B]"

**Find:** "A charity is claimed through one of three checks: a postcard to its IRS-filed address, an automated call to the phone number on its latest e-filed Form 990, or an officer identity check through Stripe."
**Replace with:** "A charity is claimed through one of three checks: a postcard to its IRS-filed address, an automated call to the phone number on its latest e-filed Form 990, or an officer identity check through Stripe. The same help page also lists a fourth route: a registration code printed on a grant check. [V wave 49B]"

**Find:** "They are published at sponsors with 53.8% of top-20 assets."
**Replace with:** "They are published at sponsors with 52.0% of top-20 assets (53.8% was the figure before the CCT row was withdrawn). [V wave 49B]"

### `research/mission-2026-11-14/direction-corporate-dafs.md`

**Find:** "| Cognizant | private foundation **converted to a DAF**, late 2022"
**Replace with:** "| Cognizant | private foundation **converted to a DAF**, late 2022; the TY2022 990-PF of Cognizant US Foundation is a final §507(b)(1)(A) return with $35.6m to the BNY Mellon Charitable Gift Fund (b49-01) [V wave 49B]"

**Find:** "Cognizant **converted** its US private foundation into a DAF in late 2022"
**Replace with:** "Cognizant **converted** its US private foundation into a DAF in late 2022 (confirmed in filings: Cognizant US Foundation’s TY2022 990-PF is marked final and §507(b)(1)(A), and its one sponsor grant, $35.6m to the BNY Mellon Charitable Gift Fund, is described as a transfer to a newly created DAF; b49-01) [V wave 49B]"

### `research/mission-2026-11-14/direction-academic-literature.md`

**Find:** "The repo does not measure inflows from foundations."
**Replace with:** "The repo now measures inflows from foundations (b49-01): 990-PF grants to the core national sponsors were $2.55bn, $2.96bn and $3.91bn in TY2022–24 (3.3–4.5% of DAF contributions), and $4.88–7.05bn a year including other national sponsors and community foundations; about 7–8% comes from foundations in their final year. [V wave 49B]"

### `research/mission-2026-11-14/FINAL-STATUS.md`

**Find:** "- **Open owner decisions:**"
**Replace with:** "- **PF-to-DAF flows and fraud controls (validated, wave 49B; report §11.74).**\n  - 990-PF grants to core national sponsors: $2.55bn, $2.96bn and $3.91bn (TY2022–24), or 3.3%, 4.5% and 4.2% of DAF contributions; T1 is a floor (about 2% brand-name misses).\n  - Fraud controls: notices and MFA at 52.0% of top-20 assets (strict login MFA 35.2%), bank-change checks at 29.8%; no DOJ release from 2021 to 2026 describes a DAF diversion.\n  - Owner decision: redact individual donor names in the PF-flow CSV’s fund-name and purpose fields.\n- **Open owner decisions:** [V wave 49B]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.74 Private-foundation flows into DAFs; fraud and diversion controls (validated, wave 49B)\n\n**Private-foundation flows into DAFs; fraud and diversion controls** (validated, wave 49B). Recomputed from the 29,204-row CSV, core national sponsors (T1) received $2.55bn, $2.96bn and $3.91bn from 990-PF filers in TY2022–24 ($9.43bn from 2,801 foundations), or 3.3%, 4.5% and 4.2% of DAF contributions; the top 10 foundations gave 30.9%. All 37 matched rows re-read in raw 990-PF XML were correct, including Cognizant US Foundation’s final §507(b)(1)(A) return with $35.6m to the BNY Mellon Charitable Gift Fund. Recall is the weaker side: about $0.19bn of misspelt brand lines (about 2% of T1) went unmatched, so T1 is a floor, and without NCF, JCF, DonorsTrust and Thrivent it is $8.29bn. Wind-downs supply 7.9% of T1. The CSV still carries some donor names in fund-name and purpose fields. The fraud-control shares (52.0% notices and MFA, 29.8% bank-change checks) and the IC3, FinCEN and DOJ figures reproduce, but NPT’s code is at registration only, so strict login MFA is 35.2%, and two stale 53.8% figures should read 52.0% (repo [`validation-wave49b-report.md`](mission-2026-11-14/validation-wave49b-report.md)). [V wave 49B]\n\n---\n\n## Source register"
