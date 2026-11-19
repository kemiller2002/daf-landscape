# Validation wave 39A: grant remittance and portal features; sponsor-published grant statistics

**Validator:** independent-validation-agent-wave39a · **Date:** 2026-11-19 · **Register:** [`data/mission-2026-11-14/validation-register-wave39a.csv`](../../data/mission-2026-11-14/validation-register-wave39a.csv) (36 claims)

**Studies checked**
- Study 1 (V39A-01 to -18): [`b4013-02-b4222-02-remittance-and-portal-features.md`](b4013-02-b4222-02-remittance-and-portal-features.md), `grant-remittance-2026-11-19.csv`, `portal-features-2026-11-19.csv`, `scripts/mission_b4013_02_b4222_02_build.py`.
- Study 2 (V39A-19 to -36): [`b4013-b4428-sponsor-published-grant-stats.md`](b4013-b4428-sponsor-published-grant-stats.md), `sponsor-published-grant-stats-2026-11-19.csv`, `scripts/mission_b4013_b4428_sponsor_stats_build.py`.

**Rules followed.**
- No outreach, no logins, no forms.
- crt.sh, certspotter and sec.gov were not used.
- One stdlib fetcher (scratchpad `v39a/scripts/get.py`, user agent `research-script/1.0` throughout, never changed). It fetched a URL only if robots.txt allowed both `*` and that agent.
- 43 page requests were made, all allowed and all returned 200:
  - Study 1: 19 pages;
  - Study 2: 6 Fidelity reports, 3 Fidelity FAQ or guide pages, 3 NPT annual-report pages, 8 Vanguard releases and 3 Schwab pressroom releases.
- The Schwab pressroom sets crawl-delay 10, so its requests were spaced 11 s apart.
- robots.txt was re-checked for blocked hosts:
  - www.dafgiving360.org and www.schwabcharitable.org returned 403, so nothing was fetched;
  - gspf.goldman.com and rj.iphiview.com have `User-agent: *` / `Disallow: /`.
- Scratch: `scratchpad/v39a/`. Nothing was committed.

## Counts

| Result | Study 1 | Study 2 | Total |
|---|---|---|---|
| confirmed | 11 | 10 | 21 |
| partially_confirmed | 6 | 6 | 12 |
| contradicted | 1 | 1 | 2 |
| unverifiable | 0 | 1 | 1 |
| **Total** | 18 | 18 | 36 |

## Findings

### Study 1: remittance and portal features

1. **Reproducible.** The rerun to scratch gives byte-identical CSVs:
   - `grant-remittance` md5 `11809239…` (14 rows);
   - `portal-features` md5 `17629985…` (32 rows).
   All printed shares and feature counts match the note.
2. **Asset-share arithmetic holds.** I summed FY2024 `daf_assets_eoy` independently from the league table:
   - top 10: $222.51bn;
   - SEC code not stated: $104.86bn (47.1%);
   - no ACH: $64.07bn (28.8%);
   - blocked: $53.58bn (24.1%);
   - Ren rail: $23.40bn (10.5%).
   The out-of-band buckets (48.7 / 20.4 / 2.6 / 4.3 / 24.1%) also reproduce. **Interpretation (partial):** NPT is in the "email report" bucket only because of its wire route. Its grants up to $250,000 go by PayPal dashboard. Grouped by primary route, the split is 29.8% email and 39.3% portal or dashboard.
3. **Quotes re-read at source: all present.** The following were checked verbatim:
   - **NPT guide** (PDF created 2026-10-15): "At this time, NPT does not issue payments via ACH transfer", the PayPal-dashboard sentence and the separately emailed wire letter. pdftotext layout mode splits the columns, so raw mode is needed.
   - **Fidelity EFT form** (2025-12-02/18): "Each EFT is comprised of one or more donor-recommended grants", "A group shared inbox will not be accepted" and the GDR fields.
   - **Fidelity FAQ:** daily GDR, up to five addresses, the "Fidelity Charitable" and "Fidelity grant" bank lines, notices "emailed each Monday", and donor contact "not available in the dashboard". The last phrase sits in the raw HTML.
   - **Fidelity Stripe page:** "does not currently send an email". Its own wording is "not available in the transaction list online".
   - **Chariot llms-full.txt:** the 11 managed sources (paid plan), "its own unique account number", "Custom Payment Sources only automate the movement of funds" and "One deposit → many donations". "Some providers batch several gifts" is in the DAFpay doc, not llms-full.
   - **Chariot DAFpay doc:** the Tracking ID quotes.
   - **Ren charity-grants and overview:** the CSV export, "Match payments (Check/ACH)", "Grant ID, Amount, Acknowledgement" and "25+".
   - **NCF:** the donate button, "invite others", "ACH or electronic transfer when available" and the "about $25" wire fee.
   - **Foundant:** Giving Hub (modified 2026-04-22) and the idea-lab reply.
   - **Triangle:** the PDF of 2024-10-07.
   - **Others:** Vanguard, MS GIFT, AEF and CCT.
   Across all 19 pages, there are 0 hits for CCD, CTX, PPD, addenda or NACHA.
4. **SEC-code scope is too wide (partial).** "Not stated by any sponsor" holds only for the pages that could be read:
   - two sponsors (24.1%) are unreadable;
   - SVCF rests on a repo row (check by default, ACH only reserved);
   - AEF's ACH began in 2026;
   - nothing covers PayPal's own transfer to the charity's bank.
   The correctly scoped claim is that none of the public pages read for the eight readable top-10 sponsors states a code.
5. **"Two sponsors send no ACH at all" overstates Vanguard (partial).** Only NPT says it issues no ACH. Vanguard's page documents PayPal Grant Payments and is silent on ACH. The CSV row is worded correctly; §0 and the bottom line are not.
6. **Feature codings.**
   - **Fidelity (c) = N is contradicted.** The Gift4Giving page does not document that others cannot give to a Giving Account. Under the note's own definitions it is ND, so (c) becomes 2 Y, 3 P, 1 N, 4 ND.
   - **Foundant vendor (c) = Y is partial.** The Giving Hub text covers "any fund you make publicly available" and never mentions DAFs, yet §5 codes the same kind of text P for tenants.
   - **Triangle's N quote is confirmed**, but its Donate tab still sends fundholders to the Hub to give to "any listed funds". The CF-wide "policy" reading rests on one 2024 PDF.
   - **The bottom line's "iPhi DonorView" export** rests only on a 2022 Minneapolis FAQ (repo row). The iPhi sponsor hosts are robots-blocked.

### Study 2: sponsor-published grant statistics

1. **Reproducible.** The CSV is byte-identical (md5 `190c2c59…`, 66 rows). The asset shares recompute: 171.21 / 223.07 = 76.75% and 88.15 / 223.07 = 39.52%.
2. **Fidelity reports 2021–2026: every figure confirmed.**
   - "Where needed most": 60% (2019), then 63, 64, 63, 63, 64 and 64% (2020–2025).
   - Splits: 83/13/4, 82/14/4, 81/15/4, 81/15/4, 80/15/5, 80/15/5.
   - The 2024 report prints both 63% and "over two-thirds".
   - The footnote "recommendations, not restrictions" appears in the 2021–2025 reports. The 2026 report drops it.
   - The PDF dates match the source register.
3. **NPT.**
   - **Confirmed:**
     - FY25 105,909 of 159,543 (66.4%);
     - chart data 13 / 63 / 66;
     - FY24 47% of 130,875;
     - FY23 "more than half", with general operating support folded in.
   - **New finding.** The 2025 report restates every earlier grant count without a note: FY21 87,490 (was 88,289), FY22 102,745 (103,816), FY23 106,235 (107,385), FY24 129,575 (130,875). Its "+23%" fits the restated base. NPT's counting method therefore changed between reports. This supports the study's untested definition-change hypothesis for 47% against 66%. On the restated base, FY24 implies about 60,900 unrestricted grants, not 61,511.
4. **DAFgiving360.**
   - **Confirmed** on the Schwab pressroom: 72% (FY2022, "not designated for a specific purpose"), 71% (CY2023) and 72% (FY2024, "did not specify a purpose").
   - **Unverifiable:** FY2025 "70%+". dafgiving360.org returns 403 on robots.txt.
5. **Vanguard.**
   - **Confirmed:** all eight releases and their dates; 48.3% and 51.7% of grant dollars; 4% and 5% anonymous on one live page.
   - **Upper bound:** the CY2025 headline says grants were "exceeding $3.9 billion", so 51.3% is an upper bound.
   - **Contradicted: "no sponsor publishes both bases".** The 2023-04-26 release (S24, in the study's own register) says unrestricted gifts were "more than 50% of total dollars granted and 70% of individual grants" in 2022. Restricted grants are then 30% of the count and under 50% of the dollars, so they are larger on average unless the unrestricted dollar share was 70% or more. The adjacent exact figures (42%, 48.3%, 51.7%) make that unlikely [I]. The CSV lacks a row for the 70%.
6. **Assessments.**
   - **Default-retention bounds [I]: confirmed as bounds.**
     - Fidelity: at most 80% kept the default, and at least 20% did not carry it. Part of that 20% reflects account defaults changed by phone, as the FAQ says.
     - Vanguard: at most 95–96% kept the default.
   - **"Anonymity insensitive to defaults" is not tested by these data (partial).** Both observed defaults are non-anonymous, so anonymity is the same opt-out under each, and no sponsor defaults to anonymous. The NPT leg is a snippet that §1.3 excludes from conclusions.
   - **"Unrestricted = no purpose entered" (partial).**
     - It is explicit at DAFgiving360 and at NPT (Schedule I narrative).
     - It is not explicit at Fidelity. The FAQ speaks of "Selecting 'Where It Is Needed Most' as the grant use", and a special purpose can be "in honor of a person", so the 36% is a designation rate, not a use-restriction rate.
     - NPT's FY23 text folds in general-operating designations.
     - So it is "two of four", not "three of four".
   - **The count range is 63–74%, not "two-thirds to three-quarters":** Fidelity's 64% is below two-thirds.
7. **Repo passages.** Three files carry DAFgiving360 "70%+ unrestricted" with the FY2025 release unread: `ai-economics-replacement-analysis.md` P05, `daf-grant-exception…-2026-11-12.md` l.10 and `b40n13-01` C1. Each should cite the first-party adjacent years and the sponsor's "did not specify a purpose" term. `b44n28-01` §3.3 and strategic-synthesis §0 hold up but omit the published outcome data. Fidelity's 2021–2023 splits are also missing from `b44n28-01`.

## Exact corrections

### `research/mission-2026-11-14/b4013-02-b4222-02-remittance-and-portal-features.md`

- **Find:** "**Not stated by any sponsor.** 0 of 14 rows name an SEC code [C]."
- **Replace with:** "**Not stated on any public page read.** 0 of 14 rows name an SEC code [C]. This covers the eight readable top-10 sponsors only: DAFgiving360 and GS DAPF (24.1%) could not be read, SVCF rests on a repo row, and no page describes the code of PayPal’s own transfer to the charity’s bank [V wave 39A]"

- **Find:** "Fidelity, SVCF, MS GIFT, AEF, RCF and NCF. Together they hold $104.86bn, 47.1% of top-10 FY2024 DAF assets [C]."
- **Replace with:** "Fidelity, SVCF, MS GIFT, AEF, RCF and NCF. Together they hold $104.86bn, 47.1% of top-10 FY2024 DAF assets [C]. SVCF pays by check by default and only reserves ACH (repo row), and AEF’s ACH began in 2026, with checks until a charity is verified [V wave 39A]"

- **Find:** "Vanguard documents only PayPal Grant Payments. Together: $64.07bn, 28.8% [C][F]."
- **Replace with:** "Vanguard documents only PayPal Grant Payments and says nothing about ACH either way, so only NPT states that it sends no ACH; PayPal itself moves accepted funds to the charity’s bank. Together: $64.07bn, 28.8% [C][F] [V wave 39A]"

- **Find:** "- **Email report plus dashboard or emailed letter, 48.7%.**"
- **Replace with:** "- **Email report plus dashboard or emailed letter, 48.7%.** NPT is in this group only because wires get an emailed letter; its grants up to $250,000 go by the PayPal dashboard, and grouping NPT by that route gives 29.8% email and 39.3% portal or dashboard [V wave 39A]"

- **Find:** "- Two of the top four sponsors do not use ACH at all (NPT and Vanguard use PayPal; NPT states it outright)."
- **Replace with:** "- Two of the top four sponsors document no ACH of their own: NPT states it outright, and Vanguard documents only PayPal Grant Payments [V wave 39A]"

- **Find:** "Grant-history export is shipped by GiftingNetwork, Foundant CommunitySuite, NPact Foundation Cloud and iPhi DonorView."
- **Replace with:** "Grant-history export is shipped by GiftingNetwork, Foundant CommunitySuite and NPact Foundation Cloud on 2025–2026 documents. iPhi DonorView rests only on Minneapolis’s 2022 FAQ (repo row), and the iPhi sponsor hosts are robots-blocked [V wave 39A]"

- **Find:** "Community foundations appear to keep DAFs off their public hubs as a matter of policy (Triangle)."
- **Replace with:** "One community foundation (Triangle, 2024 guide) declines to support fundraising for any of its funds, while its Donate tab still sends fundholders to the Giving Hub to give to listed funds. No page read shows whether CFs list DAFs on their hubs [V wave 39A]"

- **Find:** "- **Fidelity:** Gift4Giving runs the other way; the account holder lets someone else pick a charity (N)."
- **Replace with:** "- **Fidelity:** Gift4Giving runs the other way; the account holder lets someone else pick a charity. The page does not say that others cannot give to a Giving Account, so the code is ND, not N [V wave 39A]"

- **Find:** "- (c) public giving: 2 Y, 3 P, 2 N, 3 ND."
- **Replace with:** "- (c) public giving: 2 Y, 3 P, 2 N, 3 ND as coded; with Fidelity’s Gift4Giving row recoded from N to ND it is 2 Y, 3 P, 1 N, 4 ND [V wave 39A]"

- **Find:** "Giving to public funds is coded P for (c), because the question asks about a page others can use to give *to a DAF*."
- **Replace with:** "Giving to public funds is coded P for (c), because the question asks about a page others can use to give *to a DAF*. Foundant’s vendor row is coded Y on the same kind of public-fund text, so it records a capability, not a documented DAF giving page [V wave 39A]"

### `research/mission-2026-11-14/b4013-b4428-sponsor-published-grant-stats.md`

- **Find:** "That gap fits restricted grants being larger on average [I], but no sponsor publishes both bases, so this is not tested."
- **Replace with:** "That gap fits restricted grants being larger on average [I]. Vanguard publishes both bases for one year: its 2023-04-26 release says unrestricted gifts were “more than 50% of total dollars granted and 70% of individual grants” in 2022, so within Vanguard restricted grants are larger on average unless the 2022 unrestricted dollar share was 70% or more, which its 42%, 48.3% and 51.7% dollar figures make unlikely [V wave 39A]"

- **Find:** "On a grant-count basis it mostly sits around **two-thirds to three-quarters** (Fidelity 64%, NPT 66% in FY25, DAFgiving360 71–74%; NPT's FY24 47% is the exception), and **about half on a dollar basis** at the one sponsor that reports dollars (Vanguard 48–52%) [F]."
- **Replace with:** "On a grant-count basis it mostly sits at **63–74%** (Fidelity 64%, NPT 66% in FY25, DAFgiving360 71–74%, Vanguard 70% in CY2022; NPT’s FY24 47% is the exception), and **about half on a dollar basis** at the one sponsor that reports dollars (Vanguard 48–52%) [F] [V wave 39A]"

- **Find:** "No sponsor publishes both bases, so this is untested."
- **Replace with:** "Vanguard’s 2023-04-26 release gives both bases for 2022 (“more than 50% of total dollars granted” and “70% of individual grants”), so the pattern is observed at one sponsor for one year; the CSV has no row for the 70% count figure [V wave 39A]"

- **Find:** "It is not a measure of legally binding restrictions, and Fidelity says outright that its designations are not restrictions."
- **Replace with:** "It is not a measure of legally binding restrictions, and Fidelity says outright that its designations are not restrictions. At Fidelity it is not even a pure use rate: a special purpose can be “in honor of a person”, and the FAQ speaks of “Selecting” Where It Is Needed Most as the grant use, so a no-entry default is not shown. Only DAFgiving360 and NPT state the no-purpose rule, and NPT’s FY23 report folds “general operating support” designations into its majority claim [V wave 39A]"

- **Find:** "so **36% carry a donor-specified use** in 2025 [F/C]."
- **Replace with:** "so **36% carry a donor designation** in 2025, which includes honor dedications as well as uses [F/C] [V wave 39A]"

- **Find:** "That pattern fits anonymity being a stable preference that defaults barely move, with the default deciding mainly the full-contact vs fund-name margin, for which only Fidelity publishes data [I]."
- **Replace with:** "That pattern is consistent with a stable preference, but it does not test default sensitivity: anonymity is the same opt-out under both observed defaults, no sponsor defaults to anonymous, and the NPT figure is an unverified snippet [I] [V wave 39A]"

- **Find:** "Three different defaults give the same anonymous share."
- **Replace with:** "Three different defaults give the same anonymous share, but none of them is an anonymous default: under full contact and fund name only, anonymity is the same opt-out, and the NPT leg is a snippet that §1.3 excludes from conclusions. The comparison therefore cannot show that defaults do not move anonymity [V wave 39A]"

- **Find:** "FY24 is 19 points below FY25 [C] and 16 below FY20, and the snippet FY21 is 70%."
- **Replace with:** "FY24 is 19 points below FY25 [C] and 16 below FY20, and the snippet FY21 is 70%. The 2025 report also restates every earlier grant count without a note (FY21 87,490, FY22 102,745, FY23 106,235, FY24 129,575, against 88,289, 103,816, 107,385 and 130,875 in the 2024 report), and its “+23%” fits the restated base, so NPT’s counting method changed between reports [V wave 39A]"

- **Find:** "That implies about 61,511 grants [C]."
- **Replace with:** "That implies about 61,511 grants on the 2024 report’s count, or about 60,900 on the 2025 report’s restated FY24 count of 129,575 [C] [V wave 39A]"

- **Find:** "- Vanguard switches between count and dollar wording."
- **Replace with:** "- Vanguard switches between count and dollar wording. The 2023-04-26 release also gives a 2022 count share, “70% of individual grants issued as unrestricted”, beside “more than 50% of total dollars granted” [V wave 39A]"

- **Find:** "(51.3% computed from the rounded numbers)"
- **Replace with:** "(51.3% computed from the rounded numbers; the release headline says grants were “exceeding $3.9 Billion”, so this is an upper bound) [V wave 39A]"

### `research/mission-2026-11-14/ai-economics-replacement-analysis.md`

- **Find:** "sponsor-reported and not testable from Schedule I, where DAFgiving360's FY2024 return files 38 sector labels on 55,292 lines and no restricted or unrestricted text; P-B40N13-01) [V wave 35A]"
- **Replace with:** "sponsor-reported and not testable from Schedule I, where DAFgiving360's FY2024 return files 38 sector labels on 55,292 lines and no restricted or unrestricted text; P-B40N13-01) [V wave 35A]. The FY2025 release is robots-blocked and unread; first-party releases on the Schwab pressroom give 72% (FY2022), 71% (CY2023) and 72% (FY2024) of grants that “did not specify a purpose”, a no-purpose-entered share, not a measure of legal restrictions [V wave 39A]"

### `research/daf-grant-exception-unit-economics-evidence-and-sensitivity-2026-11-12.md`

- **Find:** "Different fiscal-year window from CY2025."
- **Replace with:** "Different fiscal-year window from CY2025. The FY2025 “70%+” is still unread at source (robots 403); first-party releases on the Schwab pressroom give 72% (FY2022), 71% (CY2023) and 72% (FY2024) of grants that “did not specify a purpose” [V wave 39A]"

### `research/mission-2026-11-14/b40n13-01-grant-purpose-panel.md`

- **Find:** "The FY2024 Schedule I neither supports nor contradicts 70%+. The press release could not be re-read (robots.txt 403, §9)."
- **Replace with:** "The FY2024 Schedule I neither supports nor contradicts 70%+. The press release could not be re-read (robots.txt 403, §9). Adjacent first-party releases on the Schwab pressroom give 72% (FY2022), 71% (CY2023) and 72% (FY2024) of grants that “did not specify a purpose”, so 70%+ is plausible for FY2025 but still unread, and it measures no purpose entered, not legal restriction (b4013-b4428) [V wave 39A]"

### `research/mission-2026-11-14/b44n28-01-donor-info-defaults.md`

- **Find:** "- No sponsor with a fund-name default publishes a disclosure split (P-B4428-03)."
- **Replace with:** "- No sponsor with a fund-name default publishes a disclosure split (P-B4428-03). The sponsor-stats pass confirms it: Vanguard publishes an anonymous share only. Fidelity’s 2022–2024 reports add 82/14/4 (2021), 81/15/4 (2022) and 81/15/4 (2023), so full contact eased from 83% to 80% over 2020–2025 while anonymity stayed at 4–5%. At most 80% of Fidelity’s 2025 grants kept the full-contact default; that is a bound, not a measured retention rate (b4013-b4428) [V wave 39A]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "the rest is undocumented ([b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md)) [V wave 34A]"
- **Replace with:** "the rest is undocumented ([b44n28-01-donor-info-defaults.md](b44n28-01-donor-info-defaults.md)) [V wave 34A]. Outcomes are published only by Fidelity (80% full contact, 15% fund name only, 5% anonymous in 2025) and, as an anonymous share alone, by Vanguard (4% and 5% on one page). On remittance, no public page read for the eight readable top-10 sponsors states an ACH SEC code or a grant ID in addenda; NPT pays by PayPal or wire rather than ACH, and every documented route carries grant detail out of band ([b4013-02-b4222-02-remittance-and-portal-features.md](b4013-02-b4222-02-remittance-and-portal-features.md)) [V wave 39A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "\n---\n\n## Source register"
- **Replace with:** "\n### 11.48 Grant remittance, portal features and sponsor-published grant statistics (validated, wave 39A)\n\n**Grant remittance, portal features and sponsor-published grant statistics** (validated, wave 39A). Both builds reproduce byte for byte, and every re-read quote is at source. No public page read for the eight readable top-10 sponsors states an ACH SEC code or a grant ID in addenda. DAFgiving360 and GS DAPF (24.1% of top-10 assets) are robots-blocked. NPT states that it issues no ACH and pays by PayPal or wire; Vanguard documents PayPal only. Every documented route carries grant detail outside the payment, by email report, dashboard, portal or letter. Of three portal features, grant-history export is shipped on 2025–2026 documents by GiftingNetwork, Foundant and NPact Foundation Cloud. NCF documents a donate button for others to give to a fund. No donor-level impact report was found. Fidelity, NPT, DAFgiving360 and Vanguard publish unrestricted shares: 63–74% of grants by count, against about half of dollars at Vanguard. Vanguard's 2022 release gives both bases, 70% of grants and more than half of dollars, so restricted grants are larger there. “Unrestricted” mostly means no purpose entered, not legal restriction. NPT restated its grant counts between reports. Only Fidelity publishes a full disclosure split (80/15/5 in 2025), which caps default retention at 80%. Flat 4–5% anonymity does not test default sensitivity [V wave 39A]\n\n---\n\n## Source register"
