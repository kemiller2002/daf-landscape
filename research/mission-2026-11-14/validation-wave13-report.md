# Validation wave 13: batch 28 claims and consolidation integrity

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave13.
**Register:** [`validation-register-wave13.csv`](../../data/mission-2026-11-14/validation-register-wave13.csv) (V13-01 to V13-05 for Part A; V13-B01 to V13-B07 for Part B).
**Method:** public sources only. No logins, outreach or form submissions.
- **Part A.** I formed each verdict from primary sources before opening `queue-batch28-ledgers-voids-cf-apps.md`. The sources were:
  - npact.com pages, read through their sitemap;
  - pittsburghfoundation.org/cio, read through WebFetch;
  - IRS TEOS XML zips (single members read with HTTP range requests) and the gt990datalake S3 mirror;
  - the App Store RSS and iTunes Search/Lookup APIs.
- **Part B.** I diffed both consolidated documents against their archives at three levels: numeric tokens, sentences and proper nouns, and links and URLs. I traced each changed figure to a register row or a workstream correction, and sampled 24 citations.

## Part A: batch 28 verdicts

| ID | Verdict | Key finding |
|---|---|---|
| V13-01 SVCF NetSuite + FIT | **Confirmed with nuance** (medium-high) | The case study is dated 2025-04-29 and quotes Sarah Valencia, SVP Finance, twice. It describes a custom application that would "layer on top of NetSuite" for the "investment administrative fee, income allocation, spending policy, and investment rebalancing calculations". It says FIT is "designed specifically to integrate with leading fund accounting solutions like NetSuite" and that "rebalancing can be done daily". It implies a live FIT–NetSuite integration at SVCF but never states one, and it names no CRM vendor, so it gives no support for Salesforce at SVCF. |
| V13-02 Pittsburgh CIO posting | **Confirmed; interpretation challenge** | The posting says "core ERP system encapsulated by NetSuite, Salesforce and a cloud-based data warehouse"; batch 28's quote drops the last part. The deadline is March 20, 2026. "Remediation" attaches to "the implementation of a technology plan", not to the ERP as such. |
| V13-03 NPact / DonorCentral | **Confirmed; wording fix** | The product page says "Built on NPact's cloud platform", "Cloud-hosted" and "Ongoing customer support from NPact". The 2022-09-12 release announces the acquisition from Blackbaud. The SaaS terms (2025-08-26) say "Manufacturer is Fusion Laboratories LLC / dba NPact". The direction is reversed in batch 28: Fusion Laboratories LLC *does business as* NPact. The Terms of Use (2025-07-15) say "a Delaware corporation", which conflicts with "LLC". |
| V13-04 Fidelity voids | **Confirmed for the three values; series incomplete** | Each figure is the Sch. O Part XI l.9 item "ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS". **TY2021 (FYE 6/2022): $16,130,006 = 0.141%** of $11.443bn; the original and amended returns agree. TY2022: $16,044,329 = 0.155%. TY2023: $16,590,356 = 0.131%. TY2024: $11,153,865 = 0.073%. Batch 28 marks TY2021 "n/s", but the harvest CSV lists that return (202430459349302913). The label covers voids only, of grants made in earlier years. |
| V13-05 App defects | **Confirmed** | There are 27 US written reviews dated 2021 or later. 18 describe defects in the strict sense, and 20 if the two feature regressions count. 10 describe login or authentication failures (2021-09 to 2023-11). The app has 24 ratings. Neither DAFgiving360 nor Vanguard Charitable has a standalone iOS app. |

After forming these verdicts I compared them with batch 28. Its own text (§1, §2, §3.2, §5.2) matches my figures, with three exceptions: TY2021 is shown as "n/s", the NPact dba direction is reversed, and the quote and scope of the Pittsburgh "remediation" are trimmed.

## Part B: consolidation integrity

**B1. Dropped findings.**
- **Report §11:** nothing was lost.
  - All 38 old workstream links are present.
  - Every number in the old §11 appears in the new §11.
  - The four figures that changed are logged in changelog §3: Bonterra 98.2→97.7%, S+5.00→S+4.75–5.00%, the New Mountain parser fix, and the Audax merge.
  - Sentence-level review found no other substantive drop.
- **Synthesis:** all links and URLs survive. Six items were dropped or softened without a changelog entry (V13-B04):
  - the 5.4% university/hospital payout counter-evidence;
  - the "in-kind transfer wedge; regulators have an easy target" implication;
  - the "[RT corrected from 49%]" marker;
  - "about three times earlier estimates";
  - the "EIN-match vendor client lists" next step;
  - the Schedule R "related partnership" wording.

**B2. Changed figures.**
- Every figure changed in R1–R15 and Y1–Y6 traces to an existing register row or a workstream correction. I checked these: V5-01, V5-05, V9-09, V11-05a, V11-01a/h, V12-01/03, V6-06, V10-05d, V11-07a–d, V10-08b/c, V8-01, V8-08, V9-04/05, V11-08c and V3-05. Wave-4 row 14 is in validation-wave4-report.md.
- All new synthesis figures are present in their cited workstreams: A11, A12, the C and D rows, and G1–G10.
- Defects:
  - The "59–67%" range is paired with the FY2024 figure of 79.5% (V13-B01).
  - "W4-14" is not a literal label in the wave-4 report (V13-B06, cosmetic).

**B3. Citation sample (24).**

Passed (22):
- §11: 5,272 returns; ICGF/J.P. Morgan GivingPoint redirects; GKCCF/Greater Horizons and NRS; AEF Export; Candid licence dated 2026-09-14; 10,000 draws; 89 firms; 50 cases; 244 records; Edward Jones 404; Gulf Coast "launching soon"; FidTech.
- Synthesis G: the GWCF CSV export (G1); 5 of 28 and the Wilson 4.9–21.1% interval (G4); the 0.26–2.13% all-in costs (G6); 12.1% and 23.8→20.9% (G7); "no product touches sponsor approval" and Louise 8 of 10 (G8); 17% and 43% of draws (G9); $32 on DAFpay and "no SLA" (G10); 23.7%, 11.5%, 5.9% and 43% (G5).

Failed (2):
- G4 "every observed switch ends on Foundant" (V13-B02).
- §11.3 DAF Direct, where the cited document does not support the sentence (V13-B05).

Link checks:
- All 40 local links in §11 and all 59 in G resolve.
- External spot checks returned 200 for 5 of 6 URLs. aefonline returned 403 to scripts, as it did in earlier waves.

**B4. New unsupported claims.**
- One overstatement is new in the synthesis: V13-B02. "Every observed community-foundation vendor switch ends on Foundant" appears in C (lines 78, 84) and G4 (line 180). It contradicts the same bullet's "akoyaGO 1" and the source's "six dated or datable moves".
- G1 restates V8-08 without the AEF Export conflict (V13-B03), although changelog §4.1 says that conflict stays visible.
- Nothing else is new and unsupported.

## Exact corrections

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **Line 27 (§1 table, Reported accounts).**
   - Replace: "about 59–67% if Givinga, whose account unit is undefined, is excluded (§11.1)"
   - With: "about 66% (59.2% on corrected data) if Givinga, whose account unit is undefined, is excluded (§11.1)"
2. **Line 394 (§11.1).**
   - Replace: "from about 80% to about 59–67%"
   - With: "from 80.5/77.4/79.5% (FY2022/23/24) to 63.0/67.0/66.0% (59.2% for FY2024 on corrected data)"
3. **Line 435 (§11.2 heading).**
   - Replace: "**Community-foundation vendor switches all end on Foundant**"
   - With: "**All six dated community-foundation portal switches end on Foundant (Yakima, undated, went to akoyaGO)**"
4. **Line 530 (§11.3).**
   - Replace: "DAF Direct is a Fidelity-run recommendation router for three sponsors; no funds flow through it ([queue-payment-rails-cluster.md](mission-2026-11-14/queue-payment-rails-cluster.md))."
   - With: "DAF Direct is a recommendation router for three sponsors (Fidelity Charitable, DAFgiving360, BNY Mellon CGF). Its legal operator is DAF Direct Trust, and technical evidence suggests Fidelity runs it. No funds flow through it ([queue-infrastructure-nonprofit-costs-emerging.md](mission-2026-11-14/queue-infrastructure-nonprofit-costs-emerging.md) §Q-B18)."
5. **Line 474. Apply only once batch 28 is accepted.**
   - Replace: "A further $15.6bn possibly on NetSuite + Salesforce is low confidence."
   - With: "NetSuite is now confirmed at SVCF ($9.58bn, with NPact FIT; vendor case study, medium-high) and Pittsburgh ($0.53bn, with Salesforce; high). NCF ($5.46bn) is unresolved."

### `research/mission-2026-11-14/strategic-synthesis.md`
1. **Line 19 (A1) and line 165 (G2).**
   - Replace: "about 59–67%"
   - With: "about 66% for FY2024 (59.2% on corrected data; 63–67% across FY2022–24)"
2. **Line 78 (C, Client attrition row).**
   - Replace: "Every observed community-foundation vendor switch ends on Foundant **[V wave 10]**"
   - With: "All six dated community-foundation portal switches end on Foundant; Yakima (undated) went to akoyaGO **[V wave 10]**"
3. **Line 84 (C, not vulnerable).**
   - Replace: "and every observed switch ends on Foundant"
   - With: "and all six dated portal switches end on Foundant (one undated exit went to akoyaGO)"
4. **Line 180 (G4).**
   - Replace: "Every observed community-foundation vendor switch ends on Foundant (Arkansas, Flint and Acadiana from iPhi; Winston-Salem from Blackbaud; Indian River from donor-portal.org)"
   - With: "All six dated community-foundation portal switches end on Foundant (Arkansas, Flint and Acadiana from iPhi; Tampa Bay; Winston-Salem from Blackbaud; Indian River from donor-portal.org). Ledger moves off FIMS (Arizona, Vermont, JCF San Diego) go elsewhere."
5. **Line ~155 (G1, first evidence bullet).**
   - Replace: "**[V wave 8]**"
   - With: "**[V wave 8, partial]**"
   - Then append: "AEF's live FAQ shows an 'Export' button, but it covers only a grants-paid list in legacy DonorCentral **[V wave 9]** ([queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md))."
6. **Line 196 (G6 Uncertainty).** After "about 11% for community foundations **[RT]**", insert: "and about 5.4% for university/hospital sponsors".
7. **Line 160 (G1 Implication).** Append: "An entrant offering portable history and in-kind transfer has a wedge."
8. **Line 187 (G5 Evidence).** After "about 39% of period-aligned FY2024 assets sit at three affiliate-linked nationals **[RT]**", insert: "(corrected from 49%)".

### `research/mission-2026-11-14/consolidation-changelog.md`
1. **§3.** Add a sub-table, "Synthesis items dropped or reworded", that logs V13-B04 items (d), (e) and (f):
   - "about three times earlier estimates" → retained as "8.7% → 9.0% → 28%" (line 22);
   - "EIN-match vendor client lists to the DAFRC panel" → superseded by the EIN-level CF vendor map (V9-09);
   - the Schedule R "related partnership" wording → "held 99% since CY2020" (validation wave 3).
2. **R9 and Y1.** Replace "[validation-wave4-report.md] W4-14" with "[validation-wave4-report.md] row 14 (W4-14 in the report's governing wave-4 section)".
3. **"Rules applied", first bullet.** Append: "Wave-13 audit: six synthesis items were initially dropped without an entry; see validation-wave13-report.md."

### `research/mission-2026-11-14/queue-batch28-ledgers-voids-cf-apps.md`
1. **§3.2 table, Fidelity row, TY2021 cell.** Replace "n/s" with "$16,130,006 (0.141%; amended return 202430459349302913, same as original 202321309349304807)".
2. **Line 52 (P-PAY-03).**
   - Replace: "**$16.04m (FY2023), $16.59m (FY2024), $11.15m (FY2025)**, equal to **0.155%, 0.131% and 0.073%**"
   - With: "**$16.13m (FY2022), $16.04m (FY2023), $16.59m (FY2024), $11.15m (FY2025)**, equal to **0.141%, 0.155%, 0.131% and 0.073%**"
3. **Line 51 (P-NPP-04).**
   - Replace: "NPact, which trades as Fusion Laboratories LLC,"
   - With: "NPact (the trade name of Fusion Laboratories LLC)"
4. **Line 50 (P-LSG-01).**
   - Replace: "**Pittsburgh: NetSuite + Salesforce is the current core ERP**, now under \"remediation\". The first-party CIO posting (deadline 2026-03-20) says \"core ERP system encapsulated by NetSuite, Salesforce\" [F]."
   - With: "**Pittsburgh: NetSuite + Salesforce is the current core ERP** (\"core ERP system encapsulated by NetSuite, Salesforce and a cloud-based data warehouse\"). A consultant is to \"assist in remediation of the implementation of a technology plan\" (CIO posting, deadline 2026-03-20) [F]."
5. **Line 54 and §5.2 (P-CMP-06).** After "20 of them describing defects", add: "(18 excluding 2 feature regressions)".

### `data/mission-2026-11-14/daf-grant-voids-disclosures.csv`
1. Add a row before V01 with these values:
   - `V00,FIDELITY INVESTMENTS CHARITABLE GIFT FUND,110303001,national,2021,2022-06-30,Form 990 Schedule O (Part XI line 9 reconciliation),"FORM 990, PART XI, LINE 9",ADJUSTMENT FOR PRIOR YEAR VOIDED GRANTS,16130006,11443494670,,0.141,`
   - The remaining columns follow V01. Use source_url `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430459349302913_public.xml` and set notes to "Amended return; original 202321309349304807 identical. Also at Sch D Part XII 4b."
2. **V03 notes.** Replace "Also reported at Schedule D Part XII line 4b in TY2022-23." with "Sch D Part XII 4b blank in TY2024 (reported TY2021–23)."
