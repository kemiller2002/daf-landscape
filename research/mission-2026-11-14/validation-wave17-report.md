# Validation wave 17: batch 32 claims (in-fund costs and Fidelity CIAP, MS GIFT fee location, Schedule G platform screen, Endaoment reconciliation, Every.org giving credit, tier-B DAF exits, Givinga fraud line, adviser-system feeds, Clearlake/Blackbaud, post-2022 fintech status, acquired codebases)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave17.
**Register:** [`validation-register-wave17.csv`](../../data/mission-2026-11-14/validation-register-wave17.csv), rows V17-01 to V17-26.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs or contact anyone. I fetched no `*.fcsuite.com` page. SEC requests used a generic client name. For each claim I formed a verdict from primary sources first and compared it with the batch-32 documents afterwards. I do not reproduce bank details or credentials. The sources were:
- **Scripts re-run.**
  - `scripts/mission_infund_costs.py --fetch` with a new cache: the output is byte-identical to `infund-expense-nationals-2026.csv`.
  - `scripts/mission_schedule_g_screen.py --fetch` with a fresh Schedule G extract cache (all 5,272 returns re-fetched, all `ok`): the output is byte-identical to `schedule-g-screen.csv`. Only the Part I line 8 input (`extract990cost`) came from the existing cache. I spot-checked it on six returns.
- **Fidelity Charitable:** the three audits (FY2023/22, FY2024/23, FY2025/24), via pdftotext, and the "What it costs" page HTML (pool ERs re-parsed).
- **IRS XML,** re-parsed with my own stdlib script from the GivingTuesday mirror:
  - Fidelity FY2024; MS GIFT TY2022–24;
  - Pledgeling 2023–24, CAF America FYE 4/2022 and 4/2023, Our Change 2025, Givinga 2022 and CY2024 (original and amended);
  - Endaoment FY2022–24;
  - Oracle Health, Goldstein (amended), Columbus CF, Arctic Slope CF;
  - Philanthropi TY2024, Groundswell TY2024 (original and amended), Grapevine TY2025.
- **Endaoment FY2025:** my own HTTP range request into `2026_TEOS_XML_05B.zip` at offset 298,203,445 (method 9, 14,650/105,932 bytes), wrapped in a minimal zip and inflated with `unzip`.
- **Endaoment audits:** the FY2021 and FY2022–23 PDFs.
- **Every.org:** four Zendesk JSON articles.
- **Law and guidance:** 26 USC 408 (LII), 88 FR 77922 (govinfo HTML) and IRS Pub. 590-B (2025).
- **Morgan Stanley:** the Select UMA brochure (2026-11-04).
- **Addepar:** the portfolio-data-feed directory `__NEXT_DATA__`.
- **SEC EDGAR:** the Clearlake 13F information table and submissions JSON, plus the subject of each filing index; the Blackbaud 2026 DEF 14A and Q3-2026 10-Q; and the Givinga and Groundswell Form D XMLs (all ten Givinga filings).
- **Network checks:** RDAP, dns.google, crt.sh (philanthropi.com, charityvest.org, donorfirst.org), HTTP status of reninc.com `/dfx` and `/iphi-solution` (robots.txt allows both), and the TIFIN Give ADV.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V17-01 | Fidelity pool-weighted ER 26.3 / 27.4 bps | **Confirmed** | All 26 Note 3 balances and both totals match the audit. Recomputed 26.27 bps ($110.0m) and 27.40 bps ($92.4m). Money Market and Total Market Index together are 45.1% of pools. |
| V17-02 | 13.9 / 15.0 bps per invested dollar; all-in ≥ 51.5 bps | **Partially confirmed** | Arithmetic exact, and CIAP is 46.9% of investments. **The 51.5 bps adds 37.6 bps (over average total assets) to 13.9 bps (over year-end investments).** On one base the figure is 52.0 bps (average assets) or 50.2 bps (year-end investments). It should read "about 50–52 bps", not "≥ 51.5". |
| V17-03 | CIAP fee 26.1 / 26.9 / 26.5 bps; 30.9 / 35.2 bps with line 24 | **Confirmed** | Audit "Investment management fees" equals 11f to the dollar. FY2025 line 24 has $15,615,744 (CIAP) + $5,695,890 (tax) = audit "Other expenses" $21,311,634. The tax item is a 990 line, not an audit line. |
| V17-04 | Fidelity FY2024 Part XII: 4b only, $16.59m | **Confirmed** | 12,921,946,074 − 12,905,355,718 = 16,590,356. No 4a. |
| V17-05 | MS GIFT visible advisory lines 7.8 bps vs $80.9m ceiling | **Confirmed** | $4,237,948 + $2,028,620 = 7.75 bps of $8.086bn average assets. |
| V17-06 | MS GIFT Sched D: every line 0; "audit total equals the 990's" | **Partially confirmed** | Every Part XI/XII amount present is 0, **including line 5 "Total expenses per Form 990" = $0**. Line 1 (audit totals) is absent, and so is 4a. The parts were zero-filled, so they do not show audit/990 equality. No MS GIFT audit is public, so "nor the audit's expense lines" cannot be observed. |
| V17-07 | MS GIFT line-3 yield 4–35 bps vs peers 128–424 bps "fits fees netted" | **Partially confirmed** | The yields are exact: 13.7, 35.2 and 4.2 bps. **There are 10 peer returns, not eleven.**<br>The gap is 93–124 bps to the lowest peer and about 235–265 bps to the peer median, which exceeds the whole ~107 bps fee ceiling, so fee netting alone cannot explain it. Income booked in gains or Part XI line 5 fits at least as well: MS GIFT's total-return proxy is 864 bps, inside the peer range. |
| V17-08 | Select UMA brochure 2026-11-04, wrap fee, 0.035% platform fee | **Confirmed** | |
| V17-09 | Schedule G screen 5,272 / 1,626 / 302 / 211 (97 EINs); tiers 15/38/6/152 | **Confirmed** | Fresh re-run is byte-identical. |
| V17-10 | Pledgeling 2023–24 (Charitybuzz, Prizeo) | **Confirmed** | $36.8m / $15.8m (43%) and $38.9m / $18.8m (48%), both fundraisers controlling funds; 62.0% of contributions; 20,270 / 23,006 DAFs. |
| V17-11 | CAF America Omaze | **Confirmed** | FYE 4/2022: Omaze $105.35m gross and $84.09m kept; all fundraisers $105.61m. FYE 4/2023: Omaze $30.70m; all fundraisers $30.90m. FYE 4/2024 Omaze $0.55m, then $0.<br>The headline uses Omaze-only figures and the table uses all fundraisers. Neither is labelled, and the years are fiscal years ending April. |
| V17-12 | Our Change 2025; Givinga 2022 | **Confirmed** | $14.73m / $5.96m (40.5%), 62.8% of contributions. Givinga $25.20m / $18.64m. The headline "11e 56–99%" should be 56–100%: Pledgeling 2024 is 99.96%. |
| V17-13 | Endaoment FY2023 $4.20m vs audit $16.42m; FY2022 gap; FY2024 opens at audit | **Confirmed** | All exact. FY2024 BOY PRI $16,263,586 = DAF asset $15,568,573 + digital $695,013. **Not in the doc:** the FY2022 990 BOY ($1,147,782) also differs from the FY2021 audit close ($1,039,186) by $108,596. |
| V17-14 | "Audited: No" on all four returns | **Confirmed** | `FSAuditedInd` and `IndependentAuditFinclStmtInd` are false on FY2022–25. The audit report is dated 2025-03-07. |
| V17-15 | FY2025 PPA −$2,495,535; $1.39m self-grant; fees ≤ $311,959 | **Confirmed** | From my own range extraction. 2,495,535 − 2,478,379 = 17,156. |
| V17-16 | Every.org giving credit vs 408(d)(8)(B)(i) / 4966(d)(2) / 2023 proposed regs | **Confirmed** (as an [I] reading) | All help-centre, statute and FR quotes are verbatim. Pub. 590-B (2025) does not contain "donor advised", "4966" or "509(a)(3)". The doc rightly frames it as an open question, not non-compliance. |
| V17-17 | Tier-B 14/18/6/20 split | **Confirmed** | CSV counts and asset sums reproduce. |
| V17-18 | Exit rate 1.20% → 0.89% (0.78%, 0.44%) | **Confirmed** | 69, 51, 45 and 25 over 5,746. |
| V17-19 | Oracle Health, Goldstein, Columbus, Arctic Slope evidence | **Confirmed** | Oracle: 12 transfer grants; NPT $12,311,449 = 76.1% of $16,171,193. |
| V17-20 | Givinga "EXTERNAL BANK FRAUD LOS" $316,184 | **Confirmed** | Same in the original (2025-08-25) and amended (2025-11-13) returns. Diversion No; audited. |
| V17-21 | Addepar: 406 entries, only Fidelity Charitable | **Confirmed** | |
| V17-22 | Clearlake 9,751,837 shares; 21.13% → 21.68%; no Blackbaud 13D/A after 2024-04-15 | **Confirmed** | The three later 13D/13G filings all have Forward Air as subject. Blackbaud is the largest of five issuers. |
| V17-23 | Givinga Form D: "one equity offering"; $10.77m; CB Insights $19.47m "superseded" | **Partially confirmed** | The 2023 offering's rows are exact ($10,766,659, 15 investors). **Givinga Inc. has filed Form Ds for at least six offerings since 2019, including 2022-11 ($5.0m, 11 investors).**<br>The CB Insights $19.47m equals the cumulative sold across all of them through 2025-08-18 ($19,467,959), so it is not superseded. The cumulative to 2026-09-09 is $22.42m. |
| V17-24 | Groundswell $11.9m revenue; 12,808 DAFs; one Form D 2021 | **Confirmed** | |
| V17-25 | Philanthropi contracting and dark site; "someone was building v3 as late as 2026-09" | **Partially confirmed** | Filing, RDAP and DNS REFUSED all confirmed. The prd-v3 and stg-v3 certificates recur about every three months from at least 2026-02, a pattern consistent with automated renewal; only the "migrate" hosts are new (2026-08). The logs show maintained infrastructure, not active v3 building. |
| V17-26 | DonorFirst, iPhi, Vennfi live; Amicus merged; Pinkaloo brand only | **Confirmed** | `/dfx` 301 → `/giving-platform`; `/iphi-solution` 404; donorfirst.org and charityvest.org 2026 certificates; vennfi.com has no A record; Pinkaloo sign-up host NXDOMAIN; TIFIN ADV $342.2m / $30.9m. |

**Totals:** 21 confirmed, 5 partially confirmed, 0 contradicted, 0 unverifiable.

## Exact corrections

### `research/mission-2026-11-14/queue-batch32-infund-costs.md`
1. **§0, P-B31A-02 row.**
   - **Find:** "gives at least **51.5 bps per invested dollar**"
   - **Replace with:** "gives **about 50–52 bps per invested dollar** (37.6 bps is over average total assets and 13.9 bps over year-end investments; on one base the floor is 52.0 bps over average assets or 50.2 bps over year-end investments) [V wave 17]"
2. **§1.3 table, Fidelity row.**
   - **Find:** "| **≥ 51.5 bps** |"
   - **Replace with:** "| **≈ 50–52 bps** (floor; mixed bases summed = 51.5) |"
3. **§0, P-B31A-03 row (reconciliation).**
   - **Find:** "every Schedule D Part XI/XII line is zero, so the audit nets them the same way the 990 does."
   - **Replace with:** "Schedule D Parts XI/XII are zero-filled: every amount present is 0, including line 5 'Total expenses per Form 990'. The audit totals on line 1 are absent, so the filing does not show how the audit treats the fees [V wave 17]."
4. **§0, P-B31A-03 row (line-3 signal).**
   - **Find:** "Eleven peer nationals report **128–424 bps**. That fits fees being taken out of account income before it is reported [I]."
   - **Replace with:** "Ten peer returns report **128–424 bps**. The gap (93–124 bps to the lowest peer, about 235–265 bps to the median) is larger than the whole ~107 bps fee ceiling. Fee netting may contribute, but it cannot explain the anomaly alone; income reported in gains or Part XI line 5 fits at least as well [I; V wave 17]."
5. **§3 table, Schedule D row.**
   - **Find:** "Every line is **0**, including Part XII 4a, 4b and 2e. The audit's expense total equals the 990's, so whatever the audit nets inside investment return, the 990 nets too"
   - **Replace with:** "Every amount present is **0**, including Part XII 4b, 2e and line 5 ('Total expenses per Form 990' = $0, although Part IX line 25 is positive). Line 1 (audit totals) and line 4a are not reported. The parts were zero-filled, so they say nothing about how the audit treats the fees [V wave 17]"
6. **§3 Conclusion, first bullet.**
   - **Find:** "They appear in neither Part IX nor the audit's expense lines; they reduce reported investment income."
   - **Replace with:** "They do not appear in Part IX. No MS GIFT audit is public, so their audit treatment is unobserved. They are probably netted against account values or income [I; V wave 17]."
7. **§3 Conclusion, second bullet.**
   - **Find:** "the line-3 anomaly is the first filing-level evidence for that. It fits wrap fees debited against dividend and interest income, though the 990 does not say so."
   - **Replace with:** "the line-3 anomaly is consistent with wrap fees debited against dividend and interest income, but it is too large for fees alone (see §0). The likelier main cause is classification of income into gains; the 990 does not say [I; V wave 17]."
8. **§0, P-COST-05 row.**
   - **Find:** "line 11e is 56–99% of operating cost"
   - **Replace with:** "line 11e is 56–100% of operating cost"
9. **§0, P-COST-05 row (CAF America).**
   - **Find:** "$105.3m gross in 2022, of which Omaze kept $84.1m, with the agent controlling funds; $30.7m in 2023, then near zero"
   - **Replace with:** "Omaze $105.3m gross in the fiscal year ended April 2022 ($105.6m with Ascend), of which Omaze kept $84.1m, with the agent controlling funds; Omaze $30.7m in FYE April 2023 ($30.9m with Ascend); then $0.55m and $0"
10. **§5 item 4.**
    - **Find:** "Add the line-3 investment-income anomaly (4–35 bps against 128–424 bps) as the filing evidence that fees are netted."
    - **Replace with:** "Add the line-3 investment-income anomaly (4–35 bps against 128–424 bps) as an unexplained anomaly consistent with, but larger than, fee netting [V wave 17]."

### `research/mission-2026-11-14/queue-batch32-feeds-owners-codebases.md`
1. **§3.3, Form D lead-in.**
   - **Find:** "One equity offering, first sale 2023-09-26, amended over time [F]:"
   - **Replace with:** "Givinga, Inc. has filed Form Ds for at least six equity offerings since 2019:<br>- 2019-11: $185,000;<br>- 2020-11: $2,422,149;<br>- 2021-07: $267,500;<br>- 2021-10: $3,777,625;<br>- 2022-11, with a 2023-01 D/A: $4,999,999 from 11 investors, first sale 2022-10-27;<br>- the current offering, first sale 2023-09-26, amended over time [F; V wave 17]:"
2. **§3.3, Aggregators bullet.**
   - **Find:** "**Aggregators.** VCBacked's "$6.3M" and CB Insights' "$19.47M" are both superseded by the filing for this offering [I]."
   - **Replace with:** "**Aggregators.**<br>- CB Insights' "$19.47M" equals the cumulative amount sold across all six Form D offerings through the 2025-08-18 amendment ($19,467,959), so it is not superseded. The cumulative through 2026-09-09 is **$22.42m**.<br>- VCBacked's "$6.3M" is the 2025-02-25 amendment of the current offering [C; V wave 17]."
3. **§3.3, Reading.**
   - **Find:** "Givinga survived 2022–2026 on a slow, insider-heavy raise and a B2B2C API model."
   - **Replace with:** "Givinga survived 2022–2026 on two post-2022 offerings ($5.0m in 2022; $10.77m since 2023-09) and a B2B2C API model [V wave 17]."
4. **§0, P-FAIL-06 row.**
   - **Find:** "yet certificates for "prd-v3" and "migrate" hosts were issued up to 2026-09 [F]."
   - **Replace with:** "yet prd-v3 and stg-v3 certificates kept renewing about every three months to 2026-09, and new "migrate" hosts appeared in 2026-08 [F; V wave 17]."
5. **§3.1, Reading.**
   - **Find:** "Someone was building a "v3" platform with "migrate" environments as late as September 2026."
   - **Replace with:** "The v3 infrastructure was being maintained, with certificates renewing about every three months since at least 2026-02 (consistent with automated renewal), and "migrate" environments were created in August 2026 [V wave 17]."

### `research/mission-2026-11-14/queue-batch32-filing-reconciliations.md`
1. **§1.2, Reading (after the "FY2022 990 understates in the same direction" sentence).**
   - **Append:** "The FY2022 990 also opens at $1,147,782, $108,596 above the FY2021 audited close of $1,039,186. No 990 year from FY2022 to FY2024 starts or ends on an audited figure except the FY2024 opening [V wave 17]."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **New subsection after §11.11:** "### 11.12 Batch 32 (validated, wave 17)", containing:

   > **Batch 32 (validated, wave 17).** Fidelity Charitable's audit Note 3 and its expense-ratio page give an asset-weighted pool expense ratio of 26.3 bps (FY2025; 27.4 bps FY2024). That is 13.9 bps per invested dollar, because 47% of investments sit in CIAP accounts whose fund costs are unpublished. With Part IX operating cost, Fidelity's all-in floor is about 50–52 bps. CIAP adviser fees, which the audit books gross and which equal line 11f, run at a stable 26.1–26.9 bps of average CIAP assets (31–35 bps with the line-24 CIAP item), about 60% of AEF's rate. MS GIFT's 1.00% advisory cap and 0.07% MSSB fee do not appear in Part IX (visible advisory-type lines are 7.8 bps), and its Schedule D reconciliation is zero-filled. Its line-3 investment income (4–35 bps against 128–424 bps at ten peers) is an anomaly too large for fee netting alone. A full Schedule G screen of 5,272 returns finds three sponsors besides Givinga whose DAF contributions include sweepstakes or auction gross receipts, with the agent keeping 40–85%: Pledgeling, CAF America (Omaze, FYE April 2022–23) and Our Change. Endaoment's FY2023 990 understated year-end net assets by $12.2m against its audit, and the FY2024 return silently reopened at the audited figure. All four returns answer "audited: No". The FY2025 −$2.50m prior-period adjustment and $1.39m self-grant are unexplained, and 1,213 (FY2025) is the best-evidenced DAF count. Every.org now lets IRA gifts fund "giving credit", which it calls its "DAF structure"; on the statute and the 2023 proposed regulations that balance looks like a 4966(d)(2) fund, which would put such IRA gifts outside the QCD exclusion. This is an open question, not a finding. Of 58 tier-B "exits", 14 are documented and 18 are not exits, so the central exit bound falls from 1.20% to 0.89% a year (0.44% documented only). Fidelity Charitable is still the only DAF sponsor named among Addepar's 406 feeds. Clearlake's unchanged 9,751,837 Blackbaud shares are now about 21.7% after buybacks, with no new proposal. Givinga has raised $22.4m across six Form D offerings since 2019 ($10.77m in the current one). Groundswell's sponsor reached $11.9m revenue and 12,808 accounts. Philanthropi's site is dark, while its infrastructure certificates still renew. DonorFirst/DFX, iPhi and Vennfi run on as acquirer stacks, and Amicus is merged into TIFIN Give [V wave 17]. Sources: [queue-batch32-infund-costs.md](mission-2026-11-14/queue-batch32-infund-costs.md), [queue-batch32-filing-reconciliations.md](mission-2026-11-14/queue-batch32-filing-reconciliations.md), [queue-batch32-feeds-owners-codebases.md](mission-2026-11-14/queue-batch32-feeds-owners-codebases.md), [validation-wave17-report.md](mission-2026-11-14/validation-wave17-report.md).

## Data-file notes (not .md; for the owning agent)

- **`infund-expense-nationals-2026.csv`:**
  - N069: change `weighting` note to "sum of ratios on different bases (avg total assets + year-end investments); single-base 50.2–52.0".
  - N081: change notes from "All zero: whatever the audit nets … the 990 nets the same way" to "Zero-filled: line 5 = 0 and line 1 absent; audit treatment unobserved".
  - The script output otherwise reproduces exactly. Change any text in `mission_infund_costs.py` that writes these notes the same way.
- **`schedule-g-screen.csv`:** reproduces exactly; no change.
- **`tier-b-daf-exit-reasons.csv`:** counts and sums reproduce; no change.
- **`acquired-codebase-status-2026.csv` and `relationship-graph-edges-additions-17.csv`:** EQ001–EQ015 and AC01–AC05 are consistent with what I re-read; no change.
  - If a Givinga funding edge or row is added later, use the cumulative $22.42m across six Form D offerings and do not call the CB Insights figure superseded.
- **`queue-proposals-batch32a.csv`:** if P-B32A-0x text calls the MS GIFT line-3 result "evidence that fees are netted", soften it to "anomaly consistent with but larger than fee netting".

## Limits

- **Cost-extract cache:** the Schedule G screen's Part I line 8 input came from the existing cost-extract cache. I spot-checked six returns, not all 5,272.
- **Not re-checked:**
  - Vanguard, DAFgiving360 and NPT expense-ratio ranges; the MS GIFT Donor Circular (OCR) and the CIAP overview PDF;
  - Orion's directory, the eMoney pages, the Altruist and BridgeFT articles;
  - the Gorge FY2025 05B member; most of the 58 tier-B rows beyond Oracle Health, Goldstein, Columbus and Arctic Slope;
  - the iPhi 61-host count, Pinkaloo CT history, Grapevine TY2022–23 ProPublica values, and Blackbaud 8-Ks other than the 2026 proxy and Q3 10-Q.
- **Every.org terms:** `www.every.org/terms` was not read.
- **Legal analysis:** the statute and proposed-regulation reading is legal analysis, not advice.
- **Certificate logs:** crt.sh shows issuance, not deployment. The automated-renewal reading is a pattern inference.
