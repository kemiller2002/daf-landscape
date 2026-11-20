# Validation wave 48A: BofA CGF conflict; Pledge MCP and Charity Navigator AI statements; Bright Funds and SVCF

**Validator:** validator wave 48A · **Date:** 2026-11-20 · **Register:** [`data/mission-2026-11-14/validation-register-wave48a.csv`](../../data/mission-2026-11-14/validation-register-wave48a.csv) (V48A-01 to V48A-32)

## Scope

1. BofA Charitable Gift Fund: Program Guidelines against the portal guide. Files: [b4428-04-bofa-cgf-conflict.md](b4428-04-bofa-cgf-conflict.md) and `data/mission-2026-11-14/bofa-cgf-conflict-2026-11-20.csv`.
2. The Pledge partner MCP server and Charity Navigator's AI statements. Files: [b43n26-03-0304-pledge-mcp-cn-ai.md](b43n26-03-0304-pledge-mcp-cn-ai.md) and `data/mission-2026-11-14/pledge-mcp-cn-ai-2026-11-20.csv`.
3. Bright Funds classification and SVCF grant-dollar reconciliation. Files: [b39n603-02-g191302-03-bright-funds-svcf.md](b39n603-02-g191302-03-bright-funds-svcf.md), `data/mission-2026-11-14/bright-funds-svcf-2026-11-20.csv` and `scripts/mission_bright_funds_svcf.py` (report stage only).

## Method

- **Client and fetching.** All fetches used `curl` with the user agent `research-script/1.0`, spaced 1–2 s apart, and robots.txt was read on each host first. Nothing was fetched from www.charitynavigator.org, www.ncfgiving.com or any known off-limits host. No logins, forms or outreach. The MCP endpoint was not called.
- **Robots, 2026-11-20.** No host named a Claude or Anthropic agent.

  | Host | robots.txt | Decision | Requests after robots |
  |---|---|---|---|
  | bofa.donorfirst.org | 404 | fetched | 2 PDFs |
  | www.bankofamerica.com | 200; `/philanthropic` not disallowed | fetched | 1 PDF |
  | developer.pledge.to | 404 | fetched | 4 (MCP guide, tool reference, `api.yaml`, point-redemption guide) |
  | www.pledge.to | 200; `*` disallows `/oauth`, `/organizations` | robots only | 0 |
  | givingcompass.org / www.givingcompass.org | 200; `*` Allow / | fetched | 4 (API release, sitemap index, sitemap-0, Horizon page) |
  | developer.charitynavigator.org | 200; `*` disallows `/signin`, `/checkout`, `/subscriptions` and similar | terms checked first (below); fetched | 5 (`/termsofuse`, then `/customerstory-givelink`, `/changelog`, `/plans`, `/datasharing`) |
  | www.charitynavigator.org | not requested | **not fetched (site-terms rule)** | 0 |
  | gt990datalake-rawdata.s3.amazonaws.com | 404 | fetched | 7 XML returns |
  | www.svcf.org | 200; `*` disallows `/cpresources/`, `/vendor/`, `/.env`, `/cache/` | fetched | audit PDF 2024; 2025-03-24 release |

- **Terms check for the developer portal.** I read `/termsofuse` first. It is a summary with three obligations: no sublicensing or redistribution, no competing service, and attribution. It has no clause on automated access, scraping or data mining, and it points to the full API Terms on www.charitynavigator.org, which I did not read. The developer portal is a separate host ("powered by Zuplo"). Its own terms do not ban extraction, and nothing I could read places it under the website Terms of Use. I therefore read four pages there, the minimum needed, and logged it here. If the owner holds that CN's website terms cover all CN hosts, these 5 requests fall under the same flag as the study's (see the CN compliance section).
- **BofA.** I re-downloaded the three PDFs and checked their SHA-1s against the study's CSV (all three match). The 2024 guidelines and the guide were read with `pdftotext -layout`. Version 8.2025 was OCR'd independently (`pdftoppm` at 300 dpi, then `tesseract`). Quotes were checked as exact substrings after whitespace normalisation. Similarity was measured with `difflib` in several ways.
- **Pledge.** The pages were converted to text with a stdlib helper. I extracted the tool names from the reference page by regex and keyword-searched all four sources.
- **Bright Funds / SVCF.**
  - I downloaded the 7 XMLs into scratch and ran the script's `report` stage with output sent to scratch. The CSV is byte-identical: md5 `11cdafee229d765d82abc5639c565f41`.
  - Separately, my own stdlib parser re-read the key 990 fields (Part IV line 6, Schedule D, the Schedule I recipient lines). The audit PDF and the release were read with `pdftotext` or as HTML text.
  - Repo shares were recomputed from `pass-through-recipients-2026-11-20.csv` and `donor-info-defaults-top20-2026-11-19.csv`.

## Counts

| Study | Claims | Confirmed | Partially confirmed | Contradicted | Unverifiable |
|---|---:|---:|---:|---:|---:|
| 1. BofA CGF conflict (V48A-01 to 05) | 5 | 5 | 0 | 0 | 0 |
| 2. Pledge MCP and CN AI statements (V48A-06 to 17) | 12 | 8 | 2 | 0 | 2 |
| 3. Bright Funds and SVCF (V48A-18 to 32) | 15 | 13 | 0 | 1 | 1 |
| **Total** | **32** | **26** | **2** | **1** | **3** |

V48A-02 is counted as confirmed ("confirmed within OCR noise").

## Findings

### 1. BofA Charitable Gift Fund

1. **Version 8.2025 keeps the sentence (V48A-01).** The file is SHA-1 `eda15c55…`, created and modified 2025-09-08, with the footer "Version 8.2025". An independent OCR pass contains, verbatim: "Distributions are accompanied by information specifying the account name and the name of the Donor or Advisor, unless anonymity is requested". The anonymous-grants and modification clauses are also verbatim.
2. **Similarity (V48A-02).** I get 0.9845 at word level (difflib, autojunk off), 0.9843 with autojunk on, 0.9857 by quick_ratio and 0.9899 at character level.
   - The study's 0.986 is within this OCR-dependent range, but it is not reproduced exactly. Quote it as about 0.985.
   - The substantive diffs are as described: the principal-preservation objective text, and the paper-form line. The paper-form line changes from "may be faxed, scanned, or emailed" to "may be mailed or scanned and emailed".
3. **Portal guide (V48A-03).** "The default is Fund Name Only" is on p.23, the p.20 default-fund-name callout is on p.20, and "CGF Program Guidelines" appears in the forms list on p.34. The word govern* never appears in the guide.
4. **Which document governs (V48A-04).** The Program Guidelines govern, with only the Trust Document above them. This is confirmed from the guidelines' own p.1 and p.7 text.
   - **Interpretation.** Coding by the screen default is the b44n28-01 rule. It is a choice about what "default" measures, not a finding that the guide overrides the guidelines. The conflict note has to travel with the code wherever BofA is coded.
5. **Coding and shares (V48A-05).**
   - The withheld share recomputes to 17.16% of $250.63bn, and BofA is 1.889% of top-20 assets.
   - Recoding BofA to "name only" moves fund-name-only from 15.31% to 13.42% and name-only from 1.86% to 3.75%. The withheld share stays at 17.16%.
   - Keeping the screen coding at **medium** confidence is right.
   - Current repo text (b44n28-01 row 11 and §6; b4428-02 BOA-01) does not cite Version 8.2025 or the medium confidence. Corrections are below.

### 2. Pledge MCP

6. **17 tools (V48A-06).** The reference page carries exactly the 17 snake_case tool names the study lists.
7. **`create_donation` moves money (V48A-07).**
   - The tool description is verbatim on the reference page.
   - The OpenAPI Donations tag says Pledge will "batch the amount for all the donations and bill your payment method on file", "Once a month, or when a certain threshold is reached". It also says a payment method must be set up in the Impact Hub.
   - The tool-to-endpoint mapping is still an inference, as the study says.
8. **Fees (V48A-08).** 5% Pledge fee; ACH 0.8%, capped at $5; card 2.9% + $0.30; a $5 disbursement fee for nonprofits; monthly disbursement. All verbatim from the point-redemption guide.
9. **No documented controls (V48A-09).**
   - "Confirm" appears only in the setup steps (e.g. "run /mcp to confirm pledge-developer appears").
   - There is no cap: `amount` has only the pattern `^\d+(\.\d+)?$`.
   - "Cancel" appears only as the `canceled` status. There is no refund endpoint, no OAuth and no tool annotations.
10. **Reading under §7 (V48A-10): partially confirmed. I recommend RED (provisional), not AMBER.**
    - The facts the study relies on all check out. Its reasoning for holding at AMBER does not fit the text of §7.
    - **The AMBER test is not met.** The §7 vocabulary defines AMBER as "capability live with undocumented limits, **but sponsor approval remains**". No sponsor or human approval is documented for Pledge. Daffy (AIP02) is AMBER on a documented sponsor "sole discretion", and Chariot (AIP07) on documented client confirmation. Pledge has neither.
    - **The RED test is met.** It turns on *documented* approval: "without documented sponsor or human approval".
    - **§7b.2 is not a cap.** It says how a counted component with unreadable controls enters a *provider* flag. It is a floor that stops GREEN on evidence nobody could read. It does not cap a product reading at AMBER when the product's public docs were read and document no approval. Unread endpoint metadata could only *lower* the reading later, and only if it showed a confirmation step.
    - **Recommendation.** RED (provisional; single scorer; endpoint auth and annotations unread), for owner or second-scorer adjudication under §5. The study's other two reasons (single scorer, Pledge's discretion unread) justify "provisional", not AMBER.

### 2b. Charity Navigator AI statements

11. **CNAI-04 (V48A-11): confirmed.** It is an exact substring of the developer-portal Givelink story ("Last modified on November 17, 2026"; "API user since spring 2026").
12. **CNAI-06 (V48A-12): confirmed.** The full quote is in the Giving Compass release, with datePublished 2026-01-20.
13. **CNAI-01 (V48A-13): partially confirmed.** Giving Compass's own page, "Published on November 24, 2025", corroborates the date and substance: Horizon AI Search is "powered by Giving Compass’s Natural Language Search API" and combines CN ratings with Giving Compass search technology. CN's verbatim wording ("The first phase of this collaboration…") is not on that page.
14. **CNAI-02, CNAI-03, CNAI-05 and the API Terms keyword count (V48A-14, V48A-16): unverifiable.** I did not fetch www.charitynavigator.org. The Giving Compass Horizon page does not carry the "word matching plus meaning matching" sentence.
15. **Developer portal "not found" claims (V48A-15): confirmed.**
    - The changelog has exactly 4 entries (04.07, 05.15, 08.15 and 10.07.2026), none mentioning AI, LLMs or MCP.
    - The plans and data-sharing pages carry the tiers as described, with no AI wording.
    - The terms summary carries the two quoted obligations.

### 3. Bright Funds and SVCF

16. **Reproduction (V48A-18).** The report stage re-run is byte-identical (md5 `11cdafee…`).
17. **Bright Funds filings (V48A-19 to 21).**
    - `DonorAdvisedFundInd` is false in TY2023 and TY2024. There are no Schedule D Part I elements and 0 Schedule I recipient lines.
    - Vanguard Charitable gave $24,558,662 (FYE 2023-06-30) and $47,880,713 (FYE 2024-06-30), which is 99.94% of $72,482,124.
    - The onward ratio is $101,994,960 / $111,122,714 = **0.917859**.
18. **Classification (V48A-22): confirmed.** Bright Funds is a processor: not a DAF sponsor, not on the whitelist, and it should not be added.
    - The share moves reproduce: 28-EIN 4.136% → 4.043% filed and 4.293% → 4.196% DAF-weighted; the 18-EIN rule set 2.969% → 2.871% DAF-weighted.
    - The study omits the filed move for the 18-EIN set, 2.872% → 2.779%. Its "2.87%" end value equals the old filed figure, so both columns should be given.
19. **SVCF figures (V48A-23 to 29).**
    - Schedule D line 3, CY2024: $3,064,391,940.
    - Audit Note 2, verbatim: "included in grants expense are grants in the amount of $1,667,000,000 and $207,000,000, respectively, that were transferred to other donor-advised fund sponsors".
    - The release exclusion sentence is verbatim, as are $1.54bn, "over 14,500 grants" and $327m / $175m / $874m. That implies $164m abroad.
    - NPT line: $1,591,322,838, which is 95.46% of $1,667m.
    - Biohub group, CY2023: $1,656,553,619, with $0 in CY2024. The weight 0.96222 gives the repo's $1,594.0m.
    - Further Future Foundation: $1,309,000,000.
    - Reconciliation: 3,187.08 − 1,667 = 1,520.08, a residual of +19.92 (1.31%).
    - Naming nit: one of the four "Biohub" LLCs is **CZ Institute for Advanced Biological Imaging LLC**. "Four Chan Zuckerberg LLCs" is the accurate label.
20. **Average grant (V48A-30).** The arithmetic is confirmed ($211,337.4; $104,833.1; $106,206.9).
    - **Interpretation.** $106,207 should be the primary replacement. Its dollars and count come from the same release and share its scope. $104,833 divides audited dollars by a preliminary count.
    - Because "over 14,500" is a floor, both figures are upper bounds.
21. **SVCF figure elsewhere is wrong (V48A-31): contradicted.** `queue-state-filings-transfer-terms.md` §5.3 says the NPT line is "55% of SVCF's Schedule I". On the CY2024 Schedule I Part II total ($3,158,249,119 over 3,576 lines) it is **50.4%**: 51.9% of Schedule D line 3, and 50.3% of Part IX line 1. `breadth-community-faith-infrastructure-emerging.md` already says "about 50%". Every other SVCF figure found elsewhere matches the XML: $3,064,391,940, $9,578,124,315, 1,011 funds and $1,591.3m.
22. **Recipient-revenue effect (V48A-32): unverifiable.** The study could not reproduce the published 6.89% weighting. Its "under 0.01 point" should be read as an order of magnitude only.

## Accept / modify / reject

| # | Study proposal or conclusion | Claim(s) | Decision | Note |
|---|---|---|---|---|
| 1 | Version 8.2025 exists and does not resolve the BofA conflict | V48A-01, 02 | Accept | Quote similarity as about 0.985 |
| 2 | Program Guidelines govern; guide has no governing language | V48A-03, 04 | Accept | Conflict note must travel with the code |
| 3 | Keep BofA as "fund name only" at medium confidence; 17.2% unchanged | V48A-05 | Accept | Corrections to b44n28-01 and b4428-02 below |
| 4 | Separate `policy_text_bucket` column (P-B442804-02) | — | Accept (queue) | Same split exists at RCF |
| 5 | Pledge facts: 17 tools; money-moving `create_donation`; batch billing; fees; no confirmation, cap or cancel | V48A-06 to 09 | Accept | — |
| 6 | Pledge product reading AMBER (RED-boundary, provisional) held under §7b.2 | V48A-10 | Modify | RED (provisional); owner or second scorer to adjudicate (§5) |
| 7 | AIP31 row appended to the census | V48A-06 to 10 | Modify | Append only with the adjudicated overlay label |
| 8 | CN AI channel is partnership-led; no MCP, AI tier or AI terms on the developer portal | V48A-11, 12, 15 | Accept | Rests on developer-portal and Giving Compass pages |
| 9 | CNAI-01/02/03/05 quotes from www.charitynavigator.org | V48A-13, 14 | Flag (owner decides) | See CN terms compliance |
| 10 | Bright Funds is a processor, not a DAF sponsor, not whitelisted | V48A-19 to 22 | Accept | Add the filed 18-EIN move (2.78%) |
| 11 | SVCF gap explained by $1,667m of transfers to other sponsors | V48A-23 to 29 | Accept | Rename the "Biohub" group to four Chan Zuckerberg LLCs |
| 12 | Replace $211,337 in g1913-02 §4.3 with $104,833 | V48A-30 | Modify | Use $106,207 as primary; $104,833 as a check |
| 13 | Per-$ complaint denominator for SVCF about $1.52bn | V48A-30 | Accept (queue) | The CSV is not edited here; P-B39N60302-03 |
| 14 | Recipient-revenue effect under 0.01 point | V48A-32 | Modify | Label as approximate |
| 15 | (Found) "55% of SVCF's Schedule I" in queue-state-filings | V48A-31 | Reject current text | Correct to 50.4% |

## CN terms compliance (owner decision)

**What happened.**
- The study made 27 scripted requests to www.charitynavigator.org (robots, sitemaps, 18 press releases and 4 pages), and all returned 200. It disclosed this itself (§1.1; §4 item 6).
- The shared rule names that host as one whose terms ban automated extraction ("do not script fetches; owner reads manually").
- The repo's quote of CN's site Terms of Use (2022-11-01) bars "data mining, robots, or similar data gathering and extraction methods".
- Robots permission does not satisfy the separate site-terms rule.
- The issue is wider than this study. The b43n26-03 batch and validation wave 44A also fetched that host by script.

**What depends on those reads.**
- **No independent support:**
  - CNAI-02 (the hybrid ranking sentence);
  - CNAI-03 (Allegory);
  - CNAI-05 (board);
  - the "0 AI matches" count for the API Terms;
  - the claim that none of the 18 releases outside the window mentions AI.
- **Partly supported:** CNAI-01 is corroborated in date and substance by Giving Compass's own page.
- **Independent of www:** CNAI-04 (developer portal) and CNAI-06 (Giving Compass).
- **Main conclusion unaffected:** "CN's AI channel is partnership-led; no MCP, AI tier or AI terms on the developer portal" rests on the developer portal and Giving Compass, not on the www reads.

**Recommendation: flag, do not withdraw yet.**
1. Keep the CNAI-01/02/03/05 rows and quotes in place, with a provenance flag: "obtained by scripted fetch contrary to the site-terms rule; pending the owner's manual read".
2. Until the owner has read the three release pages by hand (Horizon 2025-11-24, Allegory 2026-05-18, board 2025-07-15), do not carry those quotes into the industry report or other synthesis. The §11.71 paragraph proposed below uses none of them.
3. If the owner's manual read confirms the wording, swap the flag for "owner manual read, <date>". If the owner judges the scripted reads unacceptable in principle, withdraw CNAI-02, CNAI-03 and CNAI-05. CNAI-01 can then be re-sourced to Giving Compass's page.
4. Do not commit any cached copies of www.charitynavigator.org pages. Apply the same decision to b43n26-03 and V44A for consistency.

The only correction proposed for this issue is a provenance note. No quote is deleted.

## Limits

- **Pledge.** The MCP endpoint was not called, so tool annotations and the auth flow remain unknown. The RED recommendation is provisional for that reason.
- **BofA.** Only the PDFs in the study were re-read. The bankofamerica.com filename probes for other years were not repeated. The live screen behind the login was not seen.
- **CN.** www.charitynavigator.org was not fetched, so the full API Terms and the CN press releases were not re-read.
- **SVCF.** The audit figures were read with pdftotext. The 2023 audit PDF was not re-read; the 2024 audit's comparative column was used. The Schedule I remainder of about $76m beyond the NPT line was not matched.
- **Recipient revenue.** The weighting behind the published 6.89% was not reconstructed.

## Exact corrections

### `research/mission-2026-11-14/b44n28-01-donor-info-defaults.md`

**Find:** "| BofA CGF | 4.73 | **Fund name only:**"
**Replace with:** "| BofA CGF | 4.73 | **Fund name only** (medium confidence: the governing Program Guidelines, Version 8.2025 of 2025-09-08, still say distributions carry ‘the account name and the name of the Donor or Advisor, unless anonymity is requested’; the portal guide’s screen default is coded, b4428-04) [V wave 48A]"

**Find:** "BofA's 2024 Program Guidelines would make it name only"
**Replace with:** "BofA's governing Program Guidelines, Versions 3.2024 and 8.2025 alike, would make it name only, with the withheld share unchanged [V wave 48A]"

**Find:** "BofA's two documents conflict; the newer portal guide was used."
**Replace with:** "BofA's governing Program Guidelines (Version 8.2025, September 2025) name the account and the donor or advisor; its portal guide (February 2026) defaults the check acknowledgement to the fund name only. The screen default is used at medium confidence; both withhold address and email, so the 17.2% withheld share is unchanged (b4428-04) [V wave 48A]"

**Find:** "https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |"
**Replace with:** "https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf |\n| S22a | BofA CGF, Program Guidelines Version 8.2025 (DonorFirst portal copy; grant-distribution text unchanged from Version 3.2024) | PDF 2025-09-08 | https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf [V wave 48A]"

### `research/mission-2026-11-14/b4428-02-ren-private-label-defaults.md`

**Find:** "The 2024 guidelines say account + donor/advisor name (V34A-30)"
**Replace with:** "The governing guidelines, Version 3.2024 and Version 8.2025 (portal copy, 2025-09-08) alike, say account + donor/advisor name (V34A-30; b4428-04), so this coding is medium confidence [V wave 48A]"

### `research/mission-2026-11-14/g1913-02-grant-count-denominators.md`

**Find:** "One of the dollar figures has a scope or period problem (P-G1913-02-03)."
**Replace with:** "Resolved (b39n603-02-g191302-03): the release excludes distributions into DAFs at other institutions, and the 2024 audit counts $1,667m of grants expense as transfers to other DAF sponsors, $1,591.3m of it one Schedule I line to NPT. Use $106,207 (release dollars and count from the same document); audited grants net of those transfers ($1,520.08m) give $104,833. $211,337 is an artefact [V wave 48A]"

**Find:** "**$211,337** (SVCF's own $1.54bn gives $106,207)"
**Replace with:** "**$106,207** on SVCF’s own $1.54bn (release basis; $104,833 on audited grants net of $1,667m of DAF transfers). The DAFRC-dollar figure, $211,337, is an artefact of the $1,591.3m SVCF→NPT transfer (b39n603-02-g191302-03) [V wave 48A]"

### `research/mission-2026-11-14/b39n6-03-pass-through-recipients.md`

**Find:** "  - Bright Funds, a giving platform;"
**Replace with:** "  - Bright Funds, a giving platform: per b39n603-02-g191302-03 a workplace-giving donation processor (Part IV line 6 No in both years, Schedule D Part I blank, no Schedule I Part II lines), tagged `processor_non_daf`, not a DAF sponsor and not for the DAF-to-DAF whitelist [V wave 48A]"

**Find:** "It takes $2.25bn, 2.87% / 2.97% [C]"
**Replace with:** "It takes $2.25bn, 2.87% / 2.97% [C]; without Bright Funds, a workplace-giving processor, 2.78% / 2.87%, and the 28-EIN share is 4.04% / 4.20% (b39n603-02-g191302-03) [V wave 48A]"

### `research/mission-2026-11-14/b39n603-02-g191302-03-bright-funds-svcf.md`

**Find:** "the rule-based 18-EIN set from 2.97% to **2.87%** DAF-weighted [C]"
**Replace with:** "the rule-based 18-EIN set from 2.97% to **2.87%** DAF-weighted (2.87% to 2.78% filed) [C] [V wave 48A]"

**Find:** "  - four CZ Biohub LLCs, **$1,656,553,619**"
**Replace with:** "  - four Chan Zuckerberg LLCs (CZ Biohub SF, CZ Biohub New York, CZ Biohub Chicago and CZ Institute for Advanced Biological Imaging), **$1,656,553,619** [V wave 48A]"

**Find:** "- Use **$104,833** (audited, net of DAF transfers, all funds) or $106,207 (release)."
**Replace with:** "- Use **$106,207** (release: dollars and count from the same preliminary document, same scope). $104,833 (audited net of DAF transfers, divided by the release count) is a cross-check; 14,500 is a floor, so both are upper bounds [V wave 48A]"

### `research/mission-2026-11-14/b43n26-03-0304-pledge-mcp-cn-ai.md`

**Find:** "**Product-level reading: AMBER (RED-boundary, provisional).**"
**Replace with:** "**Product-level reading: AMBER (RED-boundary, provisional).** Validator note: wave 48A recommends RED (provisional), for owner or second-scorer adjudication under §5. The §7 AMBER test needs sponsor approval to remain, and none is documented; §7b.2’s AMBER (unverified) rule sets how a counted component with unreadable controls enters a provider flag, and does not cap a product whose public docs were read and document no approval. Unread endpoint metadata could lower the reading later only if it shows a confirmation step [V wave 48A]"

**Find:** "| none documented | **AMBER (RED-boundary, provisional)**"
**Replace with:** "| none documented | **AMBER (RED-boundary, provisional)**; validator recommends RED (provisional) [V wave 48A]"

**Find:** "developer.charitynavigator.org is governed by the API terms, which have no such clause on reading docs."
**Replace with:** "developer.charitynavigator.org is governed by the API terms, which have no such clause on reading docs. Provenance note: CNAI-02, CNAI-03 and CNAI-05, the API Terms keyword count and the release screen rest only on these scripted www.charitynavigator.org reads, which the shared site-terms rule does not allow; they are flagged pending the owner’s manual read. CNAI-01’s date and substance are corroborated by Giving Compass’s own 2025-11-24 page; CNAI-04 (developer portal) and CNAI-06 (Giving Compass) were re-read and match. Keeping, flagging or withdrawing the www quotes is the owner’s decision (validation-wave48a-report.md) [V wave 48A]"

### `research/mission-2026-11-14/queue-state-filings-transfer-terms.md`

**Find:** "55% of SVCF's Schedule I"
**Replace with:** "50.4% of SVCF's CY2024 Schedule I Part II total ($3,158.2m over 3,576 lines) and 95.5% of the $1,667m that SVCF’s 2024 audit counts as transfers to other DAF sponsors [V wave 48A]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

**Find:** "\n---\n\n## Source register"
**Replace with:** "\n\n### 11.71 BofA terms conflict, Pledge MCP, Bright Funds and SVCF (validated, wave 48A)\n\n**BofA terms conflict, Pledge MCP, Bright Funds and SVCF** (validated, wave 48A). Bank of America Charitable Gift Fund’s governing Program Guidelines, Version 8.2025 (September 2025), still say grants carry the account name and the donor or advisor name unless anonymity is requested, while its February 2026 portal guide defaults to “Fund Name Only”. The repo keeps the screen coding at medium confidence, and the 17.2% withheld share does not change. Pledge’s partner MCP server lists 17 tools; `create_donation` creates a donation billed to the partner’s payment method in monthly or threshold batches, with no documented confirmation, cap or cancel. The validator reads that as RED (provisional) under §7, not AMBER, pending a second scorer. Bright Funds files as a non-DAF workplace-giving processor that passes on 91.8% of contributions, and stays off the DAF-to-DAF whitelist. SVCF’s $3.06bn of 2024 DAF grants and its $1.54bn release differ mainly because its audit counts $1,667m as transfers to other sponsors, $1,591.3m of it one grant to NPT, so its average grant is about $106,000, not $211,337 (repo [`validation-wave48a-report.md`](mission-2026-11-14/validation-wave48a-report.md)) [V wave 48A]\n\n---\n\n## Source register"
