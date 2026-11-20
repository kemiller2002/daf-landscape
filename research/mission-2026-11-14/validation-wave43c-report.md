# Validation wave 43C: lobbying (LDA 2021–26) and DAF-parent breach notices

Validator wave 43C, 2026-11-20. Study validated: [b39n1-03-b39n2-02-lobbying-and-breaches.md](b39n1-03-b39n2-02-lobbying-and-breaches.md) (queue items P-B39N1-03 and P-B39N2-02). Register: `data/mission-2026-11-14/validation-register-wave43c.csv` (23 rows, V43C-01 to V43C-23).

## Method

- **Re-run.** `scripts/mission_lda_breach.py . --cache <copy> --offline` was run in a scratch root, using a copy of the q0102 cache and the two input CSVs. All three output CSVs came out byte-identical to the repo copies.
- **Independent recomputation.**
  - I parsed the 2,100 unique cached filing records directly and applied my own latest-version rule. This gave 1,760 filings and 35 entities.
  - I recomputed every lobbying figure from the lobbying CSV, and all LD-203 totals from the LD-203 CSV.
  - I re-ran `pdftotext -layout` on the cached Massachusetts annual-report PDFs for 2021, 2023, 2024 and 2026.
- **Live spot checks.**
  - **lda.gov.** 8 API calls in total, at least 4.3 s apart. One 429 throttle came back and was retried after 30 s. I re-fetched the FMR 2026 Q3 filing, the two SIFMA §4966 filings and the Independent Sector filing count.
  - **GovInfo.** BILLSTATUS XML for H.R. 9173, H.R. 2891 and H.R. 3975. congress.gov returned a Cloudflare challenge (HTTP 403) and was not pursued.
  - **Vermont.** The AGO Security Breach Notices page was fetched live.
  - **Massachusetts.** www.mass.gov (robots.txt, and the 2021–2026 report downloads) returned HTTP 403 to the generic `research-script/1.0` client. The user agent was not changed, so the Massachusetts figures are checked against the cached PDFs the study fetched on 2026-11-20.
  - **Maine.** Not used.

## Counts by result

| Result | Count |
|---|---:|
| confirmed | 18 |
| partially confirmed | 3 |
| contradicted | 2 |
| unverifiable | 0 |
| **Total** | **23** |

## Findings

1. **Reproducibility (V43C-01, -02).**
   - The offline re-run is byte-identical.
   - My independent de-duplication of the raw cached API records also gives 1,760 filings and 35 entities, with the same counts by year (296 / 295 / 304 / 322 / 319 / 224).
   - The live lda.gov count for Independent Sector (69 rows) matches the cache.
   - 42 of the 1,760 are LD-1 registrations. The doc's "every 2021+ LD-2" is therefore loose.
2. **Policy tags (V43C-03).** The arithmetic holds: 509 filings carry a policy tag; 275 are adjacent and unnamed; 255 are new; together they total $43,292,360.
   - **The "DAF-adjacent" framing over-counts.** After removing the false QCD matches (finding 5), 86 of the 255 carry only the OBBBA tag. They total $29.6m, and 73 of them have no charity wording on the OBBBA line. They are mostly the parents', AICPA's, SIFMA's and KPMG's retirement and business-tax lines.
   - The charity-relevant core is the filings with a charitable-deduction, QCD or §4966 tag: **169 filings, $13.65m**.
3. **Unnamed charitable-deduction lobbying (V43C-04)** is confirmed exactly: 161 filings. Independent Sector has 45, AHA 29, Philanthropy Roundtable 19, CASE 15, AFP 13, United Philanthropy Forum 12 and Global Generosity 10.
4. **"No line cites 4966" is contradicted (V43C-05).**
   - Two SIFMA self-filed lines cite §4966 by number. I confirmed both live:
     - 2023 Q4 (filing 40873abc…): "Section 4966 Donor Advised Fund Regulations";
     - 2024 Q1 (filing 5e04be11…): "IRS proposed rule regarding Section 4966 Donor Advised Funds".
   - Both rows show `tag_s4966 = Y` in the CSV. The claim was apparently read from `line_text`, which is cut at 1,500 characters, and the matches sit past the cut. The repo's earlier direction-policy-lobbying-obbba.md already quotes the second line.
   - The substantive conclusion survives: every §4966-tagged filing also names DAFs.
5. **The QCD tag over-counts (V43C-20, contradicted).**
   - The `qcd_bill` regex `(H.R.|S.) (2891|3975)` also matches **H.R. 3975, the Tax Fairness for Disaster Victims Act** (GovInfo BILLSTATUS). The QCD bill is S. 3975; H.R. 2891 is the "IRA Charitable Rollover Facilitation and Enhancement Act of 2025".
   - Six AICPA or KPMG filings carry the QCD tag only for this reason. The corrected figures are:
     - QCD-tagged filings: **126**, not 132 (2025: 18; 2026: 33);
     - new unnamed QCD filings: **34**, not 37;
     - AICPA's QCD filings in that group: **0**, not 3.
   - The 509 and the 255 are unchanged, because all six filings also carry the OBBBA tag.
6. **Parents (V43C-06, -07, -08)** are confirmed. FMR, Vanguard Group, Goldman Sachs and Morgan Stanley have 605 filings and $89.52m. None of their lines names donor-advised funds, DAFs, §4966, QCDs, IRA rollover or Legacy IRA.
   - Of the 605, 9 are LD-1 registrations, so there are 596 LD-2s.
   - The Vanguard Group total includes 7 filings ($0.42m) for the client named "VANGUARD", filed through Porterfield, Fettig & Sears.
   - The 42 OBBBA filings concern retirement, mutual-fund and financial-services tax, corporate and international tax, HSAs, student debt, escheatment and digital-asset tax. The only charity wording among them is Vanguard's 403(b) bill.
   - **H.R. 9173.** The live lda.gov record (FMR LLC, 2026 Q3, posted 2026-10-20, $600,000 expenses) lists "H.R. 9173, the Charitable Deductions for Digital Asset Donations Act". GovInfo confirms the bill number and title: 119th Congress, introduced 2026-06-08 and referred to Ways and Means. Its official title is to "except digital assets from the appraisal requirement applicable to certain charitable contributions".
7. **LD-203 (V43C-09, -10).**
   - Every total is confirmed: UBS $7,420,000; Morgan Stanley $6,523,951.51 ($4,335,201.51 honorary); Goldman Sachs $3,575,782.13; FMR $3,488,500.
   - **"No item goes to a DAF sponsor" is only partially confirmed.** No item names a national sponsor. But Morgan Stanley paid a **$75,000 honorary item to Arlington Community Foundation**, a community foundation, and community foundations as a class sponsor DAFs. I did not check whether this one does.
   - The doc's "six charity-type items" understates the nonprofit share. Morgan Stanley's 98 honorary items go mostly to nonprofits, such as housing groups, Goodwill and the American Red Cross. Only six have "charity" or "foundation" in the payee's name.
8. **Breach registers (V43C-11 to -19)** are all confirmed.
   - **Vermont (live):** Vanguard Group, Inc.: 94, Social Security Numbers, 11-4-2026; Ameriprise: 83, 4-17-2026.
   - **Massachusetts (cached primary PDFs):**
     - Vanguard: 1,224 (12-Nov-26);
     - Ameriprise: 2,216 (#2026-604, 17-Apr-26);
     - Fidelity Investments: 2,768 (09-Oct-24);
     - TD Ameritrade/Schwab: 1,103 (#30224, 8-Aug-23);
     - Fidelity Investments Life / Empire Fidelity: 2,528 (#2024-428, 01-Mar-24);
     - Morgan Stanley: 407 (#21714, 7/2/2021);
     - Infosys McCamish: 72,858 (28-Jun-24).
   - No Vermont table row and no Massachusetts text names a DAF sponsor.
   - **Minor data issue:** the breach CSV's `entity_named` for the 2023 Schwab row keeps only the middle wrapped line ("Schwab & Co., Inc., a TD Ameritrade").
9. **Personal data (V43C-22, partially confirmed).**
   - The doc has no breach-victim details and reproduces no lobbyist-filed contribution names.
   - **Flags:**
     - (a) The entity table in A.3 names one private individual LDA client. The fix is to withhold the name.
     - (b) The LD-203 CSV column `honoree_name` holds about 100 rows of individual names. They are mostly members of Congress and agency officials, but some are agency staff and nonprofit board members, and one Senate staffer is entered as the payee.
   - These are public filings, but the repo is meant to stay aggregate. I recommend blanking `honoree_name` (and that one payee) or dropping the column at the next script run. I did not edit the CSV, because it is out of scope for this wave.
10. **Repo cross-check (V43C-23).**
    - All 359 earlier LDA filings are recovered, so earlier text citing "359 filings, 33 clients" stands.
    - direction-patents-security.md still says the Vanguard count was "not established". State-register counts now exist.
    - The 77,099 (Fidelity) and 47,876 (Ameriprise) figures remain secondary and Maine-sourced. I annotated them rather than replacing them.
    - The coverage limit in direction-policy-lobbying-obbba.md can now be quantified.
    - None of these changes touches earlier waves' §11 paragraphs.

## Study-implied corrections: accept / modify / reject

The study does not include a Find/Replace block. The changes it implies for other repo files are assessed below.

| # | Change implied by the study | Decision | Note |
|---|---|---|---|
| 1 | Replace "Vanguard … count not established" with register counts (94 VT, 1,224 MA) | **Accept** | Both confirmed (VT live; MA cached primary PDF) |
| 2 | Keep 77,099 (Fidelity) as secondary; add MA 2,768 | **Accept** | Maine blocked; MA confirmed |
| 3 | Keep 47,876 (Ameriprise) as secondary; add 83 VT and 2,216 MA | **Accept** | Confirmed |
| 4 | "§4966 is lobbied only with DAF naming; no line cites 4966" | **Modify** | First half holds; second half is wrong (two SIFMA lines) |
| 5 | 255 "DAF-adjacent, unnamed" filings ($43.3m) as the headline | **Modify** | Add the 86 OBBBA-only ($29.6m) versus 169-filing core ($13.65m) split |
| 6 | QCD counts (132; 37 new; AICPA 3) | **Modify** | 126; 34; AICPA 0 (H.R. 3975 false positive) |
| 7 | "No LD-203 item goes to a DAF sponsor" | **Modify** | Restrict it to national sponsors and note the Arlington Community Foundation item |
| 8 | Quantify the LDA keyword-coverage limit in the earlier lobbying doc | **Accept** | 169 charity-relevant unnamed filings |
| 9 | Name the individual LDA client in the entity table | **Reject** | Withhold the name; aggregate only |

## Exact corrections

### `research/mission-2026-11-14/b39n1-03-b39n2-02-lobbying-and-breaches.md`

**Find:** "This pass pulls **every** 2021+ LD-2 for the 33 clients"
**Replace with:** "This pass pulls **every** 2021+ LD-2, plus LD-1 registrations (42 of the 1,760), for the 33 clients [V wave 43C]"

**Find:** "Their whole-filing amounts total **$43.3m** (not issue-specific) [C]."
**Replace with:** "Their whole-filing amounts total **$43.3m** (not issue-specific) [C]. Of these, 86 filings ($29.6m) carry only the OBBBA tag once the H.R. 3975 false QCD matches are removed. They are mostly the parents’, AICPA’s, SIFMA’s and KPMG’s retirement or business-tax lines. The charity-relevant core, with a charitable-deduction, QCD or §4966 tag, is 169 filings ($13.65m) [V wave 43C]"

**Find:** "No 2021–26 line cites "
**Replace with:** "Two SIFMA self-filed lines do cite §4966 by number: “Section 4966 Donor Advised Fund Regulations” (2023 Q4) and “IRS proposed rule regarding Section 4966 Donor Advised Funds” (2024 Q1). The matches sit past the CSV’s 1,500-character `line_text` cut, and both lines also name DAFs. No other 2021–26 line cites [V wave 43C]"

**Find:** "All 73 filings tagged §4966 got the tag from DAF-plus-regulation wording, so they also name DAFs [C]."
**Replace with:** "71 of the 73 filings tagged §4966 got the tag from DAF-plus-regulation wording, and the two SIFMA filings from the section number. All 73 also name DAFs [V wave 43C]"

**Find:** "No line cites "
**Replace with:** "Apart from two SIFMA lines (2023 Q4 and 2024 Q1) that cite “Section 4966” beyond the CSV’s 1,500-character cut, no line cites [V wave 43C]"

**Find:** "qcd 132; charity_sector 576."
**Replace with:** "qcd 132; charity_sector 576. The qcd count falls to 126 (2025: 18; 2026: 33) once six AICPA and KPMG filings are removed. They were matched only on H.R. 3975, the Tax Fairness for Disaster Victims Act, not on the QCD bill S. 3975. The 509 and the 255 are unchanged, because all six also carry OBBBA [V wave 43C]"

**Find:** "The 37 new unnamed QCD filings are mostly Legacy IRA / IRA charitable-rollover lines: AHA 17, Independent Sector 11, AFP 4, AICPA 3"
**Replace with:** "The 37 new unnamed QCD-tagged filings include 3 AICPA filings tagged only because the bill pattern matches H.R. 3975 (a disaster-relief bill). The 34 genuine ones are mostly Legacy IRA / IRA charitable-rollover lines: AHA 17, Independent Sector 11, AFP 4 [V wave 43C]"

**Find:** "No LD-203 item is paid to or honours a DAF sponsor. The six charity-type honorary or meeting items go to unrelated charities and foundations [C]."
**Replace with:** "No LD-203 item is paid to or honours a national DAF sponsor. Most of Morgan Stanley’s 98 honorary items go to nonprofits, such as housing groups, Goodwill and the American Red Cross; six have ‘charity’ or ‘foundation’ in the payee name. One of them, $75,000 to Arlington Community Foundation, goes to a community foundation, a type that usually sponsors DAFs (not checked for this one) [V wave 43C]"

**Find:** "- None goes to a DAF sponsor [C]."
**Replace with:** "- None goes to a national DAF sponsor. The $75,000 Arlington Community Foundation item goes to a community foundation, a type that usually sponsors DAFs [V wave 43C]"

**Find:** "| [individual client name, withheld after application]"
**Replace with:** "| Individual client (name withheld) [V wave 43C]"

**Find:** "`obbba` on parent filings mostly reflects non-charitable titles of the law."
**Replace with:** "`obbba` on parent filings mostly reflects non-charitable titles of the law. The `qcd_bill` pattern also matches H.R. 3975 (six false positives), and the LD-203 CSV’s `honoree_name` column holds individual names that should be blanked at the next run [V wave 43C]"

### `research/mission-2026-11-14/direction-patents-security.md`

**Find:** "- Vanguard: 2026-07, notified 2026-11-11, count not established"
**Replace with:** "- Vanguard: 2026-07, notified 2026-11-11. National count not established; state registers give 94 VT residents (2026-11-04) and 1,224 MA residents (2026-11-12) [V wave 43C]"

**Find:** "- Ameriprise (RCF white label): 2026-03, 47,876"
**Replace with:** "- Ameriprise (RCF white label): 2026-03, 47,876 (secondary, Maine-sourced, unverified; registers give 83 VT and 2,216 MA, both 2026-04-17) [V wave 43C]"

**Find:** "- Fidelity Investments: 2024-08, 77,099"
**Replace with:** "- Fidelity Investments: 2024-08, 77,099 (secondary, Maine-sourced, unverified; MA register gives 2,768, 2024-10-09) [V wave 43C]"

**Find:** "| maine.gov, apps.web.maine.gov, mass.gov | Unreadable / 403 | **Not fetched**; counts cited from secondary sources"
**Replace with:** "| maine.gov, apps.web.maine.gov, mass.gov | Unreadable / 403 | **Not fetched**; counts cited from secondary sources. The mass.gov annual PDFs were later read for b39n1-03-b39n2-02-lobbying-and-breaches.md; Maine is still blocked [V wave 43C]"

### `research/mission-2026-11-14/direction-policy-lobbying-obbba.md`

**Find:** "3. **LDA keyword coverage.** Filings that do not name DAFs or the specific bills are missed."
**Replace with:** "3. **LDA keyword coverage.** Filings that do not name DAFs or the specific bills are missed. The full-pull follow-up (b39n1-03-b39n2-02-lobbying-and-breaches.md) found 255 such policy-tagged filings for the same clients plus four sponsor parents. 169 of them carry a charitable-deduction, QCD or §4966 tag, mostly from Independent Sector, AHA and other charity-side clients. None lobbied §4966 without naming DAFs [V wave 43C]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.62 Lobbying beyond DAF keywords; state breach counts (validated, wave 43C)\n\n**Lobbying beyond DAF keywords; state breach counts** (validated, wave 43C). A full pull of 1,760 LDA filings (2021–26) for the 33 earlier DAF-naming clients and four sponsor parents re-runs byte for byte. Of these, 509 carry a charitable-deduction, §4966, OBBBA or QCD tag, and 255 neither name DAFs nor appeared in the earlier file. But 86 of the 255 carry only the OBBBA tag, so the charity-relevant core is 169 filings, led by Independent Sector, the American Heart Association and Philanthropy Roundtable. §4966 is never lobbied without naming DAFs, though two SIFMA lines cite it by number. FMR, Vanguard Group, Goldman Sachs and Morgan Stanley filed 605 times ($89.5m, all issues) without naming DAFs, §4966 or QCDs. Their 42 OBBBA filings concern retirement and financial-services tax, and FMR’s only charitable line is H.R. 9173 on digital-asset gifts. The QCD count falls from 132 to 126, because the bill pattern also caught a disaster-relief bill. State registers confirm Vanguard (94 VT, 1,224 MA), Ameriprise (83 VT, 2,216 MA), Fidelity (2,768 MA) and Infosys McCamish (72,858 MA), and none names a DAF sponsor. Maine figures stay secondary. Sources: [b39n1-03-b39n2-02-lobbying-and-breaches.md](mission-2026-11-14/b39n1-03-b39n2-02-lobbying-and-breaches.md); [validation-wave43c-report.md](mission-2026-11-14/validation-wave43c-report.md).\n\n---\n\n## Source register"
