# Validation wave 18: batch 33 claims (blank Schedule D panel, sweepstakes share, line-3 screen, DAF-to-DAF flows, uncashed-check rules, CF donor export, BofA/GivingPoint rails, corporate exits, grant-software consolidation, faith platforms, Edward Jones, and the Goldman Sachs circular conflict)

**Date:** 2026-11-15. **Validator:** independent-validation-agent-wave18.
**Register:** [`validation-register-wave18.csv`](../../data/mission-2026-11-14/validation-register-wave18.csv), rows V18-01 to V18-29.
**Method:** public sources only. I did not log in, submit forms, solve CAPTCHAs or contact anyone. I fetched no `*.fcsuite.com` page. I checked robots.txt before each scripted read and skipped hosts whose rules exclude me (details under Limits). I do not reproduce bank details or credentials. For each claim I formed a verdict from primary sources first and compared it with the batch-33 documents afterwards. The sources were:
- **Scripts re-run** in a scratch copy of the repo, so no repo file was overwritten.
  - `scripts/mission_panel_scans.py --task all --fetch` with a **new, empty** `extract990inv` cache (all 5,272 returns re-fetched, all `ok`) and the 12,257-return `extract990` cache. All three outputs (`blank-schedule-d-panel.csv`, `sweepstakes-receipts-dafrc-share.csv`, `low-investment-income-screen.csv`) are byte-identical to the repo.
  - `scripts/mission_daf_to_daf.py` against a `netpayout990` cache built in an earlier wave, not batch 33's own cache. `daf-to-daf-flows-top50.csv` is byte-identical.
- **IRS XML,** re-parsed with my own stdlib script from the GivingTuesday mirror:
  - Vanguard FYE 6/2024, SVCF CY2024 and NPT FYE 6/2024 (Schedule I lines);
  - GS Donor Advised Philanthropy Fund CY2024 (entity name and EIN);
  - Pledgeling TY2023 and TY2024 (Part III text and DAF count);
  - five sampled blank-Part-I returns;
  - Jewish Federations of Greater Pittsburgh (FYE 6/2025) and Philadelphia (FYE 8/2025), Part VII-B.
- **Goldman:** the FireAid/Latham investigative report PDF (39 pp.; pdftotext; Appendix B), plus `gspf.goldman.com/robots.txt`.
- **Uncashed-check rules:** the Fidelity returned-grant FAQ; the GiveClear and BlueGive Intercom articles; Vanguard Charitable's policies page; the PPGF Delivery Policies of 2025-01-01 and 2022-03-15 (PDFs); NPT's FY25 consolidated financials PDF.
- **Exports and rails:** the BofA CGF DFX guide (pdftotext, plus a 110-dpi render of p.28); the Columbus, Saint Paul & Minnesota and Minneapolis PDFs; the Omaha, OCCF, GWCF and GKCCF pages; the Foundant Idea Lab thread; the jpmgiving.org main bundle and the nptgivingpoint.org `chunk-GNPJY3AQ.js`.
- **Market structure:**
  - press: GBH/AP (AmazonSmile), Civil Society (Virgin Money Giving), Irish Times (Meta EEA);
  - deals: the L Squared 2024-08-13 page and the Foundant Compass GivingData post;
  - Edward Jones: the 2024 PIC report PDF, the DAF product page and the 2025 release;
  - repo data: the DAFRC FY2024 rows (faith segment and pass-through sponsors) and the batch-33 CSVs, recomputed.

## Conflict resolution: the Goldman Sachs circular (batch 30 vs batch 33C)

**Batch 30 is right, and batch 33C is wrong on this point.**
- **The document exists.** FireAid's investigative report (PDF created 2025-09-26; "Investigative Report as of September 8, 2025", corrected 2025-09-26) reproduces as **Appendix B** a "GS Donor Advised Philanthropy Fund for Wealth Management (GS DAF) Program Circular" (circular pages on PDF pp. 18–39). Its ETF table footnote says expense ratios are "based on fund expense ratios in effect as of September 30, 2024". It is therefore a 2024-or-later document, well inside the recency rule.
- **It is the same sponsor.** The CY2024 990 for EIN 31-1774905 is filed as "GS DONOR ADVISED PHILANTHROPY FUND". The repo's "GS PF", "GS DAPF" and "GS DAF" are one entity.
- **Its terms (re-read):**
  - $20,000 opening minimum; $100 minimum grant;
  - grant proceeds sent "in the form of a check **or wire transfer**";
  - administration fee from 0.60% on the first $500,000 down to 0.03% above $25 million;
  - the passive ETF option is "selected by Goldman Sachs Wealth Services, L.P.", with "Up to 0.50% (50 bps) Goldman Sachs Wealth Services, L.P. fee".
- **What this overturns in batch 33C:**
  - "No 2021+ program document found";
  - "the newest public circular is dated 2017-12-05";
  - "Ayco selecting the ETF options";
  - check-only payment;
  - "GS PF stays insufficient evidence *because* no 2021+ source exists".
  The 2017 circular is at most dated context.
- **Caveats that remain** (as batch 30 and wave 15 already said):
  - the circular is undated and hosted by a third party;
  - the live login page binds donors to an unversioned "GS DAF's Program Circular".

  Whether GS PF can now be plotted is a decision for the quadrant agent, but the premise for "insufficient evidence" (no 2021+ source) no longer holds.
- **Process note.** `gspf.goldman.com/robots.txt` (read 2026-11-15) ends `User-agent: *` / `Disallow: /`, allowing only named search-engine crawlers. I therefore did **not** re-fetch the 2017 or 2008 circulars, and their dates are unverified by me. They do not affect the resolution, because the FireAid copy is newer either way. Later passes should not script-fetch that host.

## Verdicts

| ID | Claim | Verdict | Key finding |
|---|---|---|---|
| V18-01 | Batch 33C: newest GS circular is 2017; GS stays insufficient evidence | **Contradicted** | FireAid App. B circular, ratios as of 2024-09-30, for the same EIN. Check **or wire**; ETFs selected by Goldman Sachs Wealth Services, not Ayco. Batch 30 / V15-09 stands. |
| V18-02 | 185 returns / 113 sponsors, line 6 "Yes" with Part I blank; 3.5% of 5,255 | **Confirmed** | Fresh re-run byte-identical. 5 sampled XMLs each show `DonorAdvisedFundInd` true/1 with no count or value. |
| V18-03 | Imputed: 78 returns / 62 sponsors, $1.60bn over FY2021–24 | **Confirmed** | $1,602,245,402. **It is a sum of year-end stocks over four years** (CFMT and Christian CF count twice), not a one-year gap. |
| V18-04 | Dropped as closed: 77 / 31; $41m / $78m / $172m / $151m; $183m once | **Confirmed** | $182.5m across the 31 EINs, each counted once. |
| V18-05 | Exit rate 1.20% → 0.91% (upper 0.99%; 0.80% / 0.89%) | **Confirmed** | 52 / 5,746 = 0.905%; $162.8m reclassified. |
| V18-06 | Sweepstakes share ≤ 0.17% (0.12 / 0.11 / 0.05%) | **Confirmed** | All amounts and shares exact. |
| V18-07 | Pledgeling accounts match "approximately 23,000 [20,000] organizations" | **Partially confirmed** | The quotes are exact but **crossed by year**: TY2023 has 20,270 accounts against "~23,000"; TY2024 has 23,006 against "~20,000". |
| V18-08 | Line-3 screen 467 / 247; MS GIFT the only captive under 50 bps; "every other captive 131–641 bps" | **Partially confirmed** | Counts exact. **DAFgiving360 is at 95.6 bps (FY2024) and 114.3 bps (FY2023)**, below the stated floor. |
| V18-09 | Top 50 → top 50: $3.39bn / $6.03bn (6.2% / 9.3%) | **Confirmed** | Byte-identical using an independent cache. |
| V18-10 | All panel → DAF-holding recipients: $5.24bn / $9.56bn | **Confirmed** | 9.58% / 14.80% of grants; 8.02% / 10.56% of contributions. |
| V18-11 | 436 pairs, 212 two-way; $8.45bn nets to $4.31bn | **Confirmed** | |
| V18-12 | NPT +$1.89bn, SVCF −$1.21bn; SVCF → NPT $1,591,322,838 | **Confirmed** | Filed line re-parsed: "General Nonprofit Support". |
| V18-13 | Vanguard → ImpactAssets $308,265,198 (FY2024) | **Confirmed** | Schedule I, FYE 2024-06-30. |
| V18-14 | 90-day void at Fidelity, GiveClear, BlueGive; Vanguard discretionary | **Confirmed** | GiveClear and BlueGive text identical. Fidelity words it as the "likely" reason for a return. |
| V18-15 | PPGF 2025 policy: removal and reassignment; 90 → 45 days | **Partially confirmed** | **The reassignment sentence is already in the 2022-03-15 policy.** Only delivery timing changed in 2025. |
| V18-16 | NPT FY25 statements: 2 pages; grants payable $300.6m vs $363.8m | **Confirmed** | |
| V18-17 | 6 CFs with grant-history export = 18.2%; 8 = 25.4% | **Confirmed** | 40 rows = the DAFRC top-40 CFs ($43.77bn). Quotes re-read except CCT (robots). |
| V18-18 | Foundant grant-history export added 2024-08-27 | **Confirmed** | Idea Lab: "Implemented". |
| V18-19 | BofA Grant Listing "Export to Excel" (p.28 screenshot) | **Confirmed** | Seen on the render. The text mentions export only on p.14. |
| V18-20 | J.P. Morgan GivingPoint: "NPT will issue a check"; no RDE enum; 17 export handlers | **Confirmed** | |
| V18-21 | AmazonSmile quotes and dates | **Confirmed** | Via GBH/AP. |
| V18-22 | Virgin Money Giving quotes and dates | **Confirmed** | Civil Society, 26 Aug 2021. |
| V18-23 | Meta → PPGF (US/UK/CA/AU 2023); EEA off 2024-07-01 | **Partially confirmed** | EEA quote confirmed (Irish Times). US half not re-read (Chronicle paywalled; robots). |
| V18-24 | Foundant–SmartSimple 2024-08-13; GivingData May 2025 | **Confirmed** | "nothing changes for you" verbatim. |
| V18-25 | Faith segment $20.18bn / 186 and platform splits | **Confirmed** | All family sums reproduce. NCF $5.46bn and Signatry are **DAFRC-imputed**; CJP is a paper submission. |
| V18-26 | Pass-through DAFs ~$4.4bn; PPGF 694,979 / $626.6m labelled [X] | **Partially confirmed** | Sum $4.378bn. **PPGF's (and NFG's) FY2024 values are imputed**, not 990. |
| V18-27 | Edward Jones "nearly $535 million" assets under care in 2023 | **Partially confirmed** | The same report also says "invested by clients … **since inception**", so $535m may be cumulative. |
| V18-28 | EJ page: RCF "manages and administers"; private DAF release 2025-09-16 | **Confirmed** | |
| V18-29 | Pittsburgh: FidTech $525,587 + Armanino $536,465; Philadelphia: Ren $500,842 | **Confirmed** | Re-parsed Part VII-B. The queue text's "JFGP" is wrong, as batch 33C says. |

**Totals:** 22 confirmed, 6 partially confirmed, 1 contradicted, 0 unverifiable.

## Exact corrections

### `research/mission-2026-11-14/queue-batch33-market-structure.md`
1. **§0, Q-B05 / Q-N08 row (Goldman).**
   - **Find:** "**Goldman:** no 2021+ program document found. The newest public GSPF circular is dated **2017-12-05**, not 2008 as the repo states. It shows Ayco selecting the ETF options for a 50 bp fee. The live stack is unchanged: Ren iPhi donor web, Ayco admin, Goldman.com SSO. A new two-hop inference: GS Gives grant administration runs through CAF America, a Bonterra customer. | High (EJ text); GS stays "insufficient evidence" |"
   - **Replace with:** "**Goldman:** a 2021+ program circular exists. FireAid's Sept 2025 investigative report reproduces the GS DAF Program Circular as Appendix B, with ETF expense ratios as of 2024-09-30 (batch 30; V15-09; re-confirmed wave 18). It sets a $20,000 minimum and $100 grants paid by check or wire, and the ETF option is selected by Goldman Sachs Wealth Services, L.P. (up to 50 bps). The 2017 and 2008 circulars on gspf.goldman.com are dated context only. Live stack: Ren iPhi donor web, Ayco/GS Wealth Services administration, Goldman.com SSO. A new two-hop inference: GS Gives grant administration runs through CAF America, a Bonterra customer. | High (EJ text; GS circular). GS PF's 'insufficient evidence' premise (no 2021+ source) no longer holds; re-scoring is for the quadrant agent [V wave 18] |"
2. **§0, Edward Jones bullet.**
   - **Find:** "- Edward Jones' 2024 report gives the program as \"nearly $535 million\" assets under care and \">$90 million\" granted in 2023."
   - **Replace with:** "- Edward Jones' 2024 report says \"nearly $535 million\" invested by clients in the program and \">$90 million\" granted in 2023. One page calls the $535m \"assets under care\" in 2023; another says \"since inception\", so it may be cumulative investment rather than year-end assets [V wave 18]."
3. **§4.1, "What changed" second bullet.**
   - **Find:** "  - The program has a first-party size of about $535m (2023) (ER015)."
   - **Replace with:** "  - The program has a first-party size of \"nearly $535 million\" invested by clients (described both as 2023 assets under care and as \"since inception\"), with more than $90m granted in 2023 (ER015) [V wave 18]."
4. **§4.2, first bullet.**
   - **Find:** "- **No 2021+ program circular, donor guide or terms were found.**"
   - **Replace with:** "- **A 2021+ program circular exists, but not on Goldman's own public pages.** FireAid's investigative report ([PDF](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf), Appendix B) reproduces the GS DAF Program Circular, with ETF expense ratios \"in effect as of September 30, 2024\": $20,000 minimum, $100 minimum grant, payment \"in the form of a check or wire transfer\", admin fee 0.60% down to 0.03%, and ETFs selected by Goldman Sachs Wealth Services, L.P. (batch 30; V15-09; V18-01). No Goldman-hosted 2021+ circular was found."
5. **§4.2, second bullet lead-in.**
   - **Find:** "- **The newest public circular is dated 2017-12-05**, served from the donor-web domain"
   - **Replace with:** "- **The newest circular on Goldman's own domain is dated 2017-12-05** (dated context only, superseded by the FireAid-reproduced circular above; gspf.goldman.com's robots.txt disallows non-search crawlers, so it was not re-fetched in wave 18), served from the donor-web domain"
6. **§4.2, Quadrant status bullet.**
   - **Find:** "- **Quadrant status:** GS PF stays \"insufficient evidence\". The 2017 circular is pre-2021 and cannot score 2026 criteria under the bounded-truth rule."
   - **Replace with:** "- **Quadrant status:** the 2017 circular cannot score 2026 criteria, but the FireAid-reproduced circular (ratios as of 2024-09-30) is admissible 2021+ evidence for payment rail (check or wire) and terms. Caveats: it is undated, hosted by a third party, and the login page binds to an unversioned circular. Whether GS PF leaves \"insufficient evidence\" is for the quadrant agent [V wave 18]."
7. **§5, item 1.**
   - **Find:** "replace with \"The newest public Program Circular is dated 2017-12-05 ([PDF](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)); a 2008 version and an undated v6 are also served. All are pre-2021.\""
   - **Replace with:** "superseded by wave 18: see the governing text for `queue-bank-programs-and-eft-providers.md` in `validation-wave18-report.md` (newest known circular = FireAid App. B, ratios as of 2024-09-30; Goldman-hosted 2008, v6 and 2017 versions are dated context)."
8. **§5, item 3.**
   - **Find:** "Edward Jones' own figure for 2023 is \"nearly $535 million\" assets under care (ER015)."
   - **Replace with:** "Edward Jones' own figure is \"nearly $535 million\" invested by clients (worded both as 2023 assets under care and as since inception) (ER015) [V wave 18]."
9. **§1.2, item 2 (PPGF label).**
   - **Find:** "PPGF FY2024: 694,979 DAF accounts, $626.6m grants ([DAFRC FY2024 row](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) [X]."
   - **Replace with:** "PPGF FY2024: 694,979 DAF accounts, $626.6m grants ([DAFRC FY2024 row](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv); DAFRC-imputed values, not a filed 990) [V wave 18]."
10. **§2.2, pass-through total.**
    - **Find:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC)."
    - **Replace with:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC; PPGF's $626.6m and NFG's $427.9m are imputed) [V wave 18]."
11. **§3.2 table, NCF row.**
    - **Find:** "| Salesforce captive portal (Stellar component behind it; GL inferred NetSuite) | NCF $5.46bn |"
    - **Replace with:** "| Salesforce captive portal (Stellar component behind it; GL inferred NetSuite) | NCF $5.46bn (DAFRC-imputed FY2024 value; The Signatry's $0.40bn is also imputed) [V wave 18] |"

### `research/mission-2026-11-14/queue-bank-programs-and-eft-providers.md`
1. **§0, P-QCAL-04 row, Goldman bullet.**
   - **Find:** "- **Goldman Sachs Philanthropy Fund (PWM):** the only public program document is a Program Circular **last revised August 2008** ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) [F]."
   - **Replace with:** "- **Goldman Sachs Philanthropy Fund (PWM; now GS Donor Advised Philanthropy Fund for Wealth Management):** the newest known Program Circular, with ETF ratios as of 2024-09-30, is reproduced in FireAid's Sept 2025 investigative report, Appendix B ([PDF](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf)) [F, third-party-hosted; V15-09, V18-01]. Goldman's own domain serves only 2008, ~2012 (v6) and 2017 versions, which are dated context."
2. **§0, Grant payment rails row.**
   - **Find:** "- **GS PF:** check, per the 2008 circular; the 2026 rail is unknown."
   - **Replace with:** "- **GS PF:** check or wire, per the circular with ratios as of 2024-09-30 (FireAid App. B) [V wave 18]."
3. **§0, P-STF-05 row.**
   - **Find:** "- **Check only:** BofA CGF, DAFgiving360 (as documented) and GS PF (2008)."
   - **Replace with:** "- **Check only:** BofA CGF and DAFgiving360 (as documented). GS PF pays by check or wire (2024-ratio circular) [V wave 18]."
4. **§0, Data export row.**
   - **Find:** "- **BofA:** the 2025 portal guide shows \"export to Excel\" on the **contribution** listing ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) [F]."
   - **Replace with:** "- **BofA:** the portal guide (modified 2026-02-23) says \"export to Excel\" on the contribution listing (p.14, text). The Grant Listing screenshot (p.28) also shows an \"Export to Excel\" button; whether it covers paid as well as pending grants is not stated ([guide](https://bofa.donorfirst.org/pdf/bofa/Guide%20to%20Navigating%20Your%20Donor%20Advised%20Fund.pdf)) [F; batch 33B; V wave 18]."
5. **§2, "Which document governs", first bullet.**
   - **Find:** "- **The only public Program Circular is dated 2008.** It ends \"Last Revised: August 2008\" and is served from the GS DAF donor-web domain ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)) [F]."
   - **Replace with:** "- **The newest known Program Circular is 2024 or later.** FireAid's investigative report ([PDF](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf), Appendix B) reproduces the GS DAF circular, with ETF ratios as of 2024-09-30. Its terms are $20,000 minimum, $100 grants, check or wire, admin fee 0.60%→0.03%, and Goldman Sachs Wealth Services, L.P. in Ayco's former role (V15-09; V18-01). Goldman's donor-web domain serves older versions: one ending \"Last Revised: August 2008\" ([circular](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=HLXWYjqZAGE%3D&mid=554&tabid=111)), an undated v6 (~2012) and a 2017-12-05 circular. These are dated context; the 2008 terms below are historical. (gspf.goldman.com's robots.txt disallows non-search crawlers; do not script-fetch it.)"

### `research/mission-2026-11-14/evidence-quadrant-methodology.md`
1. **§8, example.**
   - **Find:** "Example: Goldman Sachs Philanthropy Fund's 2008, 2012 and 2017 circulars cannot score its payment-rail or portability criteria, so GS PF stays \"insufficient evidence\" until a 2021+ source is found."
   - **Replace with:** "Example: Goldman Sachs Philanthropy Fund's 2008, 2012 and 2017 circulars cannot score its payment-rail or portability criteria. A 2021+ source has since been found: the GS DAF circular with ratios as of 2024-09-30, reproduced in FireAid's Sept 2025 report (V15-09, V18-01). Criteria it covers (for example, check or wire payment) may be scored from it; criteria it does not cover stay U."

### `research/mission-2026-11-14/queue-batch33-panel-scans.md`
1. **§0, P-B32B-01 row (imputed total).**
   - **Find:** "**$1.60bn summed over FY2021–24** ($0.49bn, $0.69bn, $0.22bn and $0.20bn)."
   - **Replace with:** "**$1.60bn summed over FY2021–24** ($0.49bn, $0.69bn, $0.22bn and $0.20bn). This is a sum of year-end stocks across four years, and some sponsors (CFMT, Christian CF) count twice; the largest single-year amount is $0.69bn [V wave 18]."
2. **§0, P-B32A-01 row (Pledgeling).**
   - **Find:** "**Pledgeling's \"accounts\":** its 20,270–23,006 accounts match its own Part III text, \"pass-through grants to approximately 23,000 [20,000] organizations\". So they look like per-beneficiary records, not donor DAFs [I]."
   - **Replace with:** "**Pledgeling's \"accounts\":** its 20,270–23,006 accounts fall in the same range as its Part III text, \"pass-through grants to approximately 23,000 [20,000] organizations\", but crossed by year: TY2023 reports 20,270 accounts against ~23,000 organisations, and TY2024 reports 23,006 against ~20,000. They may be per-beneficiary records rather than donor DAFs [I; V wave 18]."
3. **§2, Reading item 3.**
   - **Find:** "   - Its Part III narrative counts pass-through grantee organisations in exactly that range: \"approximately 23,000\" in the TY2023 return and \"approximately 20,000\" in TY2024"
   - **Replace with:** "   - Its Part III narrative counts pass-through grantee organisations in the same range, but crossed by year: \"approximately 23,000\" in the TY2023 return (20,270 accounts) and \"approximately 20,000\" in TY2024 (23,006 accounts) [V wave 18]"
4. **§3, broker and bank captives.**
   - **Find:** "Every other broker or bank captive is at 131–641 bps in every year: Fidelity, Vanguard, GS DAPF, BofA, Raymond James, Stifel, T. Rowe, BNY Mellon, Comerica, USCGT, AEF, RCF and NPT."
   - **Replace with:** "DAFgiving360 is at 95.6 bps (FY2024) and 114.3 bps (FY2023), with normal total returns. Every other broker or bank captive is at 131–641 bps in every year: Fidelity, Vanguard, GS DAPF, BofA, Raymond James, Stifel, T. Rowe, BNY Mellon, Comerica, USCGT, AEF, RCF and NPT [V wave 18]."
5. **§0, P-B32A-03 row.**
   - **Find:** "The next-lowest large captive is GS Charitable Gift Fund at 67 bps (FY2022); Bessemer is at 94–159. **No other broker captive shares the pattern.**"
   - **Replace with:** "The next-lowest large captive is GS Charitable Gift Fund at 67 bps (FY2022, a down year); Bessemer is at 94–159 and DAFgiving360 at 96–114. **No other broker captive is under 50 bps.** [V wave 18]"

### `research/mission-2026-11-14/queue-batch33-voids-exports-rails.md`
1. **§0, P-NPP-02 row (PPGF).**
   - **Find:** "**PayPal Giving Fund (policy updated 2025-01-01):** a check to an unenrolled charity that \"is not cashed within the time period specified on the check\" may lead PPGF to remove the charity and reassign the funds. The period itself is not published."
   - **Replace with:** "**PayPal Giving Fund (policy updated 2025-01-01):** a check to an unenrolled charity that \"is not cashed within the time period specified on the check\" may lead PPGF to remove the charity and reassign the funds. The same sentence is already in the 2022-03-15 policy, so this is a standing rule, not a 2025 change. The period itself is not published [V wave 18]."
2. **§1.2, item 2.**
   - **Find:** "2. **PPGF is the exception in design.** It sends no money back to a donor."
   - **Replace with:** "2. **PPGF is the exception in design** (unchanged since at least the 2022-03-15 policy; V wave 18). It sends no money back to a donor."

### `research/DAF-INDUSTRY-REPORT-2026-11.md`
1. **GS PF re-score note (after the v1.2 changes table).**
   - **Find:** "On Goldman Sachs PF, wave 6 found that its 2012 and 2017 circulars are also public. All of them state check payment, so a further re-score could place it."
   - **Replace with:** "On Goldman Sachs PF, wave 6 found that its 2012 and 2017 circulars are also public, and all of them state check payment. A 2021+ circular (ETF ratios as of 2024-09-30, reproduced in FireAid's Sept 2025 report) states check **or wire**, so a further re-score could place it (V15-09, V18-01)."
2. **Bank-programs table, BofA row.**
   - **Find:** "| BofA CGF | Check-only grants. Contributions (not grants) can be exported to Excel."
   - **Replace with:** "| BofA CGF | Check-only grants. Contributions can be exported to Excel (guide text), and the Grant Listing screenshot also shows an \"Export to Excel\" button (scope not stated; V18-19)."
3. **Bank-programs table, Goldman row.**
   - **Find:** "| Goldman Sachs PF | Circulars from 2008, 2012 and 2017 all state check payment. The live donor web runs on Ren iPhi. |"
   - **Replace with:** "| Goldman Sachs PF | Goldman-hosted circulars from 2008, 2012 and 2017 state check payment. The newest known circular (ratios as of 2024-09-30, FireAid App. B) states check or wire. The live donor web runs on Ren iPhi. |"
4. **New subsection after §11.12:** "### 11.13 Batch 33 (validated, wave 18)", containing:

   > **Batch 33 (validated, wave 18).** 185 returns from 113 DAFRC sponsors (3.5% of line-6 "Yes" returns, TY2021+) answer that they hold DAFs but leave Schedule D Part I blank. DAFRC imputes 78 of them ($1.60bn summed across four years' year-end values, at most $0.69bn in any one year) and drops 77 from 31 sponsors as "closed". Carrying those sponsors' last values forward puts $151–172m a year (≤0.07% of DAF assets) outside the totals. Treating reporting gaps as non-exits lowers the mechanical central exit rate from 1.20% to 0.91% a year (0.89% with manual coding). Sweepstakes and auction receipts inside DAF contributions are at most 0.17% of the market (FY2022), falling to 0.05% in FY2024. MS GIFT is the only broker or bank captive whose line-3 investment income is below 50 bps of assets; DAFgiving360 is next at 96–114 bps. Among the top 50 sponsors, grants to other top-50 DAF-holding sponsors were $3.39bn (FY2023) and $6.03bn (FY2024), or 6.2% and 9.3% of market grants. Panel-wide, lines to DAF-holding sponsors were $5.24bn and $9.56bn, an upper bound on double counting. About half of the gross top-50 pair flow nets out. NPT is the main net receiver (+$1.89bn over two years) and SVCF the main net sender (−$1.21bn, chiefly one $1.59bn CY2024 line); Vanguard sent ImpactAssets $308m in FY2024. Where a void window is published (Fidelity, GiveClear, BlueGive) it is 90 days, with funds returned to the donor account. PayPal Giving Fund instead may remove the charity and reassign funds, a rule unchanged since at least 2022; its 2025 policy only shortened check delivery to 45 days after month-end. No sponsor states an escheat treatment. Six top-40 community foundations (18.2% of top-40 CF DAF assets) publicly document a donor grant-history export, all on packaged portals, and Foundant added one on 2024-08-27. BofA's guide shows "Export to Excel" on the Grant Listing too. J.P. Morgan's GivingPoint code says "NPT will issue a check", and its payment enum has no Ren RDE value, so NPT pays on its own rails. Corporate giving products closed for parent-level reasons (AmazonSmile "spread too thin"; Virgin Money Giving's investment need and loss of marathon "brand exposure"), and Meta handed processing to PayPal Giving Fund. Foundant merged with SmartSimple (2024-08-13) and took in GivingData (May 2025). The $20.2bn faith segment (186 sponsors) has no common platform; NCF's $5.46bn Salesforce captive is a DAFRC-imputed value. Edward Jones reports "nearly $535 million" invested in its Charitable Gift Fund (described as both 2023 assets and since inception), administered by RCF; its private DAF's sponsor is still not public. **Goldman:** a 2021+ GS DAF circular (ETF ratios as of 2024-09-30; check or wire; Goldman Sachs Wealth Services, L.P. in Ayco's former role) is reproduced in FireAid's 2025 report, so batch 33C's "newest circular 2017" is superseded [V wave 18]. Sources: [queue-batch33-panel-scans.md](mission-2026-11-14/queue-batch33-panel-scans.md), [queue-batch33-voids-exports-rails.md](mission-2026-11-14/queue-batch33-voids-exports-rails.md), [queue-batch33-market-structure.md](mission-2026-11-14/queue-batch33-market-structure.md), [validation-wave18-report.md](mission-2026-11-14/validation-wave18-report.md).

## Data-file notes (not .md; for the owning agent)

- **`relationship-graph-edges-additions-18.csv`:**
  - **ER017** (Ayco → GS DAF, "historically_confirmed", 2017 circular): add to notes "superseded by the FireAid App. B circular (ratios as of 2024-09-30), which names Goldman Sachs Wealth Services, L.P. as ETF selector (up to 50 bps) and payment by check or wire; V18-01". Consider a new edge, Goldman Sachs Wealth Services, L.P. → GS DAF (administrator / investment selector, confirmed, FireAid App. B).
  - **ER015:** add "report wording varies: '$535 million … since inception' vs 'In 2023: … assets under care'; V18-27".
- **`faith-sponsor-platforms-2026.csv`:** add "DAFRC-imputed" to the notes for NCF and The Signatry, and "paper submission" for CJP.
- **`uncashed-grant-rules-2026.csv`:** on the PPGF 2025 row, note that the removal/reassignment sentence also appears in the 2022-03-15 policy (row S19); only the delivery timing changed.
- **`donor-export-evidence-cf-2026.csv`:** the CCT quote could not be re-fetched in wave 18 (robots.txt on donorportal.cct.org); keep it as an earlier read.
- **`blank-schedule-d-panel.csv`, `sweepstakes-receipts-dafrc-share.csv`, `low-investment-income-screen.csv`, `daf-to-daf-flows-top50.csv`:** reproduce byte-identically; no change.

## Limits

- **Robots exclusions honoured.** These pages were not re-fetched:
  - gspf.goldman.com (`User-agent: *` / `Disallow: /`): the 2008, v6 and 2017 circulars;
  - donorportal.cct.org (one-line robots file read as disallowing all but /index.html): the CCT FAQ;
  - techcrunch.com (disallows anthropic-ai and ClaudeBot);
  - philanthropy.com: the wildcard agent is grouped with blocked agents, and the article is paywalled.

  Batch 33's reads of gspf.goldman.com and donorportal.cct.org appear inconsistent with those files; later passes should not script-fetch them.
- **Not re-checked:**
  - GoFundMe Charity and Google One Today items;
  - the Fluxx, Submittable/WizeHive, Instrumentl and Bonterra/Apax pages;
  - the Blackbaud Giving Fund help page;
  - the CJP, JCF LA, JCF SF, NCF, Cleveland and Miami portal hosts (ER001–ER006);
  - Ren's reissue article, DAFgiving360, AEF, the MS GIFT brochure and the RCF DFX guide;
  - the Tampa, Atlanta, Denver, Seattle and JaxCF guides;
  - the GS Gives FY2025 990 (ER018).
- **The extract990 cache** (12,257 returns) was reused, not rebuilt; I validated it by sampling five returns. The `netpayout990` cache was an earlier wave's, not batch 33's.
- **Interpretation.** That a Schedule I line between sponsors is DAF money remains an inference, as batch 33 labels it.
