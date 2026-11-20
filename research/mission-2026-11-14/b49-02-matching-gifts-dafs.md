# Do corporate matching-gift programmes match DAF grants? (b49-02)

**Date:** 2026-11-20 · **Task:** b49-02 · **Answers queue item:** P-B39N4-03 (primary-source panel of DAF clauses for Fortune 100 matching programmes) · **Builds on:** [direction-recipients-impact-matching.md](direction-recipients-impact-matching.md) §3 and [`matching-gift-daf-policies-2026.csv`](../../data/mission-2026-11-14/matching-gift-daf-policies-2026.csv) (16 policies, MG01–MG16). This repo already covered the topic in part, so it is **not new**. That earlier pass picked companies wherever a DAF clause could be found. This pass draws a defined sample and codes every company in it.

**Outputs**
- [`data/mission-2026-11-14/matching-gifts-dafs-2026-11-20.csv`](../../data/mission-2026-11-14/matching-gifts-dafs-2026-11-20.csv): 104 rows.
  - MGD001–MGD100: the Fortune 500 2025 top 100 (the frame). `in_sample = 1` marks the 68 companies in the sample.
  - SP01–SP04: DAF sponsor policies.
- [`scripts/mission_b49_02_matching_gifts.py`](../../scripts/mission_b49_02_matching_gifts.py): computes every [C] figure from the CSV. Run `python3 -I scripts/mission_b49_02_matching_gifts.py .`
- [`data/mission-2026-11-14/queue-proposals-b49-02.csv`](../../data/mission-2026-11-14/queue-proposals-b49-02.csv): P-B4902-01 to -06.

**Labels:** [F] first-party document read this pass, either on the company's site or as a company-authored PDF hosted by Double the Donation (DtD) or a third party · [S] secondary source (DtD article or summary) · [R] search-index text only; the page was not fetched · [C] computed by the script · [I] inference.

**Rules followed.** robots.txt was checked on every host before fetching, with the AI-agent rule applied (§6). Pages were fetched with a generic user agent (`research-script/1.0`). There were no logins, forms or outreach, and nothing was fetched from sec.gov, fortune.com or crt.sh. Evidence older than 2021 is kept but flagged `recency_ok_2021plus = 0`, and every headline share is also given on 2021+ evidence alone. This is research, not legal or tax advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Do large employers match DAF grants?** | **Only a minority say so in writing. Most say nothing publicly.**<br>Sample: 68 of the Fortune 500 2025 top 100 that DtD lists as running a matching-gift programme [C]. Coding uses the best public evidence of any date [C]:<br>- **eligible: 10 (14.7%)**. 4 eligible outright and 6 with conditions;<br>- **excluded: 6 (8.8%)**;<br>- **silent: 12 (17.6%)**. A public guideline was read and it has no clause on DAF grants;<br>- **no public guideline text: 40 (58.8%)**. These programmes run through login portals (Benevity, YourCause, CyberGrants).<br>Among the **28 with readable text**: **35.7% eligible, 21.4% excluded, 42.9% silent** [C]. Coding Bank of America as excluded moves this to 35.7 / 25.0 / 39.3 [C]. | High for the coding of each document; medium for the shares (small n; the published-text group may not be representative) |
| **2021+ evidence only** | 10 companies have a readable document dated 2021 or later: **5 eligible (Boeing 2022, Disney 2021, RTX 2021, Humana live FAQ, Amex 2025 [S]), 1 excluded (Verizon 2024), 4 silent (Microsoft 2026, Merck 2021, Delta 2022, Bank of America 2025 [S])** [C].<br>5 of the 6 exclusions are pre-2021 or undated (JPMorgan 2014, IBM 2012, Travelers 2012, Lilly 2017, BMS ≤2020) [C]. So the recent documents lean permissive. With n = 10 this is suggestive, not a trend [I]. | Low–medium |
| **What conditions apply?** | Of the 10 eligible:<br>- **6 add an ownership condition.** The fund must be the employee's own: "in your name" (Apple), "set up by the employee in his or her name" (Amex), "established, and is named on" (Disney), "personal donor-advised fund" (RTX), "that the employee directs" (PepsiCo), or "directly funded by the employee … only" with a segregated account (Chevron).<br>- **4 add only proof or timing rules.** Proof from the administering institution (UnitedHealth), a donation receipt (Humana), a match at disbursement (Boeing), or a gift made directly to the charity (NVIDIA). | High |
| **Gifts *into* a DAF** | Of the 8 sample companies that address contributions into a DAF, **6 exclude them** (JPMorgan, Bank of America, Humana, Amex, Merck, BMS) [C].<br>**Verizon is the reverse case.** A direct donation *to* a DAF "may itself be eligible", but grants made *through* DAFs are not (rules updated 2024-12-27) [F].<br>**Disney** matches gifts into named community-impact, field-of-interest or special-interest funds only [F]. | High |
| **Are the aggregators reliable here?** | **DtD company pages: no.** None of the 68 DtD company summaries mentions DAFs [C], including the 16 sample companies whose documents carry a clause on DAF grants (10 eligible, 6 excluded).<br>**DtD's DAF article (2025-09-16)** quotes Chevron's clause exactly as in Chevron's 2014 form [F]. It also reads Bank of America's "gifts **to** … donor-advised funds" as an exclusion of gifts **from** DAFs, which the text does not say [S].<br>**Benevity** publishes no company-level DAF summaries. causes.benevity.org disallows ClaudeBot, and storage.benevity.com disallows all agents (§6). | High |
| **What do the big DAF sponsors say?** | **None of the three readable sponsors says DAF grants cannot be matched, and none gives the "donor already took the deduction" reason.**<br>- **Fidelity Charitable:** "Your employer is the best resource …". It provides a downloadable grant confirmation "as proof of your donation for your employer" [F].<br>- **Vanguard Charitable** (policies 2026-03-12) and **NPT** (DAF guide): no matching-gift statement. Both forbid grants that confer a "more than incidental" benefit [F].<br>- **DAFgiving360:** robots.txt returned 403, so not fetched. The search index showed no matching FAQ [R]. | High (three sponsors); none (DAFgiving360) |
| **What is the IRS position?** | **No primary IRS text addresses employer matching of DAF grants.**<br>- **§4967** taxes advice that produces a "more than incidental benefit" (125% of the benefit) [F].<br>- **Notice 2017-73** covers only event tickets (benefit) and pledges (no benefit if conditions are met), and contains no matching text [F].<br>- The **2023 proposed regulations** (88 FR 77922) would make "any use of donor advised fund assets that results in a more than incidental benefit" a deemed distribution. "Matching" appears 0 times [F].<br>[I] The employer pays the match from its own funds, not from DAF assets, so these rules do not reach a match on their face. The risk arises only if the match comes back to the employee, for example credited to the employee's own DAF. | High (text); [I] on application |
| **What does it mean for DAF donors?** | [I] At a Fortune 100 matching employer, a DAF donor can confirm from public documents that a DAF grant is matchable at **1 in 7** employers (10/68). They will find a written exclusion at **1 in 11** (6/68). **For about three in four (52/68) they must ask HR or the portal** [C].<br>The documented floor is **14.7%** and the ceiling (not documented excluded) is **91.2%** [C].<br>If the 40 portal-only programmes resemble the 28 readable ones, roughly a third match DAF grants and a fifth exclude them [I].<br>Where matching exists, it attaches to the **grant**, not the deductible contribution. Ownership conditions bar DAFs that were funded by others, including employer-funded employee DAFs (§4). | Medium on the counts; low on the extrapolation |

---

## 1. Method

### 1.1 Sample (reproducible)
1. **Frame.** The 100 largest US companies by revenue in the Fortune 500 2025 list (mostly FY2024), taken from the table in [Wikipedia, "List of largest companies in the United States by revenue"](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue), revision **1354288064**, fetched 2026-11-20. The table cites Fortune.
   - fortune.com was **not** used: its terms of use bar "spidering, screen scraping, database scraping … or any other automatic means".
   - Wikipedia's `/w/` API path is disallowed for all agents, so only the `/wiki/` page was read.
2. **Programme screen.** For each frame company, the DtD company page `https://doublethedonation.com/matching-gifts/<slug>` was fetched. Slugs were built from the name plus listed aliases, for example `exxonmobil`, `the-cigna-group` and `merck-co`. Any slug with a "Matching gift eligible?" field was accepted.
   - Results: **68 Yes, 28 No, 4 with no page found** (Walmart, Berkshire Hathaway, UPS, Progressive) [C].
   - "No" covers discontinued, inactive or portal-only programmes, for example "Procter & Gamble … discontinued their matching gift program on June 30, 2016" and "ExxonMobil's matching gift program is currently inactive" [S].
   - **Sample = the 68 "Yes" companies.** DtD is used only to define the sample. It is never the source of a DAF coding.
3. Each DtD summary was also scanned for "donor-advised", "DAF" and related terms (gift fund, family fund, personal or private foundation, trust). There were 0 hits [C].

### 1.2 Evidence per company
- **One targeted web search per sample company** (company + "matching gift" + "donor advised"), plus three searches restricted to `files.doublethedonation.com`. That host serves company-authored guideline PDFs uploaded to DtD.
- Every candidate document was fetched, if robots allowed, and searched for DAF-related terms. **The clause in the CSV is extracted verbatim from the downloaded file** between fixed start and end anchors, never retyped.
- **Dating rule:**
  1. a date printed in the document ("Updated 12/27/24", "Revised 04/29/2014");
  2. else the PDF CreationDate;
  3. else the HTTP Last-Modified header (NVIDIA, BMS).
  4. Live web pages are dated by the access date.
- **Coding of `daf_grant_policy`, for grants *from* a DAF to a charity:**
  - `eligible`: matchable, with at most proof or timing rules;
  - `eligible_conditional`: matchable only if the DAF is the employee's own (named, sole-funded or employee-directed);
  - `excluded`: grants from DAFs are ineligible;
  - `silent`: a public programme guideline was read and it has no clause on DAF grants. A clause that covers only gifts *into* DAFs counts as silent on grants;
  - `no_public_text`: no readable public guideline was found. This is **"not found"**, not "silent".
  - `gift_into_daf_policy` is coded separately.
- **Precedence:** where several documents exist, the latest dated primary is used, and secondary quotes only where the primary was blocked or unreadable. This applied to Amex and Bank of America.

### 1.3 Sponsor side and IRS
- Fidelity Charitable FAQ and programme guidelines (PDF 2026-09-11); Vanguard Charitable FAQ and policies page; NPT donor guide PDF. Each was searched for "match" and "incidental".
- IRS and Treasury texts:
  - [Notice 2017-73](https://www.irs.gov/pub/irs-drop/n-17-73.pdf) (irs.gov);
  - the [2023 proposed regulations](https://www.govinfo.gov/content/pkg/FR-2023-11-14/pdf/2023-24982.pdf) (govinfo; FR document 2023-24982, located through the federalregister.gov API). federalregister.gov HTML is limited to API access for automated clients and was not scraped;
  - [26 U.S.C. §4967](https://www.law.cornell.edu/uscode/text/26/4967) (Cornell LII).
  - JCT's PPA explanation (jct.gov) was **not** used: its robots.txt disallows ClaudeBot.

---

## 2. Results

### 2.1 Shares [C]

| Basis | n | Eligible (any) | Excluded | Silent | No public text |
|---|---|---|---|---|---|
| A. All sample, any date | 68 | 10 (14.7%) | 6 (8.8%) | 12 (17.6%) | 40 (58.8%) |
| B. Readable text, any date | 28 | 10 (35.7%) | 6 (21.4%) | 12 (42.9%) | — |
| C. All sample, 2021+ only | 68 | 5 (7.4%) | 1 (1.5%) | 4 (5.9%) | 58 (85.3%) |
| D. Readable 2021+ text | 10 | 5 (50.0%) | 1 (10.0%) | 4 (40.0%) | — |
| E. B with Bank of America coded excluded | 28 | 10 (35.7%) | 7 (25.0%) | 11 (39.3%) | — |

Source types for the 28 texts [C]:
- 22 are company PDFs hosted by DtD;
- 3 are company sites (Verizon, Humana, Microsoft);
- 1 is a company form hosted by a school district (IBM);
- 2 are DtD article quotes (Amex, Bank of America).

### 2.2 Companies with a DAF clause

| Company (rank) | Grants from DAF | Date | Clause (abridged; full text in CSV) |
|---|---|---|---|
| Boeing (63) | eligible | 2022-07-08 | "…donor-advised funds can be matched at the time of disbursement to the eligible nonprofit." |
| Humana (39) | eligible | live 2026 | "contributions out of a Donor Advised Fund to an eligible organization … would be eligible for matching with donation receipt" |
| UnitedHealth (3) | eligible | 2020-12 | Proof for a gift "made through my charitable-gift, donor-advised or family fund" must come "from the financial institution that administers" the fund |
| NVIDIA (31) | eligible | ≤2020-04 | match for an external donation "through a donor advised fund made directly to a qualified charity" |
| Walt Disney (46) | conditional | 2021-02-03 | "donations from an Eligible Employee's donor advised fund … if the employee or the employee's family established, and is named on, the fund" |
| RTX (54) | conditional | 2021-03 | "employee charitable donations using a personal donor-advised fund maintained by a licensed financial institution" |
| American Express (58) | conditional | 2025 [S] | "…distributed from an established fund set up by the employee in his or her name" |
| Apple (4) | conditional | 2014 | "Made from your personal funds or a charitable gift fund in your name" |
| Chevron (16) | conditional | 2014 | "Donor Advised Funds must be directly funded by the employee, retiree or director only…" |
| PepsiCo (45) | conditional | 2016-04 | "Disbursals from Donor-Advised Funds … that the employee directs are eligible." |
| Verizon (30) | **excluded** | 2024-12-27 | "…donations … made indirectly via donor-advised funds are not eligible for a match" (but a direct donation *to* a DAF "may itself be eligible") |
| JPMorgan Chase (11) | excluded | 2014-04-29 | "Grants to or from a donor-advised fund…" |
| IBM (68) | excluded | 2012-07-01 | "Contributions from … donor advised funds…" |
| Eli Lilly (100) | excluded | 2017-07-31 | "Contributions from … donor advised funds, and family foundations" |
| Travelers (99) | excluded | 2012-08-23 | "made directly by you and not from a donor fund" |
| BMS (94) | excluded | ≤2020-02 | "Gifts made by or through … donor advised funds or family foundations". The form covers retirees, retired directors and Puerto Rico employees. |

**Silent on grants from DAFs (12).**
- **Exclude gifts *into* DAFs only (2):** Merck (2021: "Gifts to a third-party organization such as a donor advised fund") and Bank of America (2025 [S]: "gifts to … donor-advised funds").
- **No DAF wording at all (10):**
  - Microsoft CY25 deck (2026);
  - Delta education programme (2022);
  - Fannie Mae (2013/14), Dell (2013), MetLife (2013), NY Life (2013), Intel (2016), Deere (2014), Nike (2012), Coca-Cola (2010).

### 2.3 Sponsor side (SP01–SP04)

| Sponsor | Statement | Source |
|---|---|---|
| Fidelity Charitable | "Your employer is the best resource to reference when determining what their policy is on matching grants recommended from donor-advised funds. If your employer does match grants … you can … download a confirmation as proof of your donation for your employer." | [FAQ](https://www.fidelitycharitable.org/faqs/donor/grantmaking.html) (live 2026-11-20) [F] |
| Vanguard Charitable | No matching statement. "Grants … cannot result in more than incidental benefit accruing to any specific individual…"; the impermissible list includes "receipt of anything of value in return for the grants" | [Policies and guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) (PDF dated 031226) [F] |
| NPT | No matching statement. "grants cannot be used to provide any private benefit to donors, advisors or their family members that is more than incidental." "Matching or challenge grant provisions" appear only as grant-agreement terms. | [DAF guide PDF](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) [F] |
| DAFgiving360 | Not fetched (robots.txt 403). The search index showed FAQ and granting pages with no matching entry. | [R] |

**The premise "sponsors say DAF grants cannot be matched" is not supported** by the three readable sponsors. Fidelity explicitly supports matching with a confirmation document.

### 2.4 IRS position (primary texts)
- **§4967(a)(1):** a tax "equal to 125 percent of such benefit" on advice to make a distribution "which results in such person … receiving, directly or indirectly, a more than incidental benefit as a result of such distribution" ([LII](https://www.law.cornell.edu/uscode/text/26/4967)) [F].
- **Notice 2017-73 (pre-2021; cited because it is the governing notice):**
  - Treasury and the IRS "currently agree that the relief of the Donor/Advisor's obligation to pay the full price of a ticket … can be considered a direct benefit … that is more than incidental";
  - pledge fulfilment would not be a more-than-incidental benefit if "the sponsoring organization makes no reference to the existence of any individual's pledge when making the DAF distribution" (§4).
  - The word "match" does not appear in the notice [F].
- **2023 proposed regulations (§53.4966-1(e)(2), 88 FR 77922, 2023-11-14):** "A distribution includes any use of donor advised fund assets that results in a more than incidental benefit (within the meaning of section 4967) to a donor, donor-advisor, or related person." "Matching" appears 0 times [F].
- **[I] Reading.** A corporate match is the employer's own gift to the charity. It is not a use of DAF assets, and the employee's DAF grant is not changed by it. The texts read therefore give no basis for a blanket bar. The employer's own condition that the gift be the employee's personal money (sole-funder, named-fund clauses) is a programme design choice, not an IRS rule.
- The "deduction already taken" rationale appears in **none** of the sponsor, company or IRS documents read.

---

## 3. What this implies for DAF donors' matching [I unless marked]

1. **Ask, don't assume.** For 52 of 68 Fortune 100 matching employers (76.5% [C]), public documents do not settle the question: 12 are silent and 40 have no public text. The readable documents split roughly one-third eligible, one-fifth excluded and the rest silent (§2.1 B).
2. **The match follows the grant, not the deductible contribution.**
   - Six of eight companies that address gifts *into* DAFs exclude them [C], and Boeing matches "at the time of disbursement".
   - Programme caps are set per year and apply to the grant year. A donor who bunches contributions into a DAF and grants over several years can therefore match each year's grants up to the cap, whereas a single large direct gift would hit one year's cap.
3. **Ownership conditions screen out shared and employer-funded DAFs.** Six of the ten eligible clauses require the DAF to be the employee's own, and Chevron requires it to be "directly funded by the employee … only".
   - This excludes DAFs with joint funders.
   - It also excludes the employer-funded employee DAFs in [direction-corporate-dafs.md](direction-corporate-dafs.md) §4 and §5: Macerich's "company-matched donor advised fund", VICI's employee DAF accounts, and Fidelity Investments' Match Account (MG15 in the earlier CSV).
   - The effect is to prevent matching money that was itself an employer gift.
4. **Documentation is the friction.**
   - UnitedHealth requires proof "from the financial institution that administers" the DAF; RTX requires "backup documentation from your financial institution"; Humana requires a "donation receipt".
   - Fidelity Charitable already supplies a downloadable grant confirmation.
   - A sponsor's grant confirmation, carrying the donor's name, date, charity EIN and amount, is the artefact that unlocks matches. It is a cheap product feature.
5. **Recent documents lean permissive** (5 eligible against 1 excluded in 2021+ texts, against 5 eligible and 5 excluded in older ones [C]). The sample is too small to call a trend.

### 3.1 Link to the corporate-DAF direction
- **Matching programmes themselves pay through DAF sponsors.** This was verified in the documents read:
  - Disney returns unmatched money to "Disney's Donor Advised Fund at Charities Aid Foundation of America" (2021);
  - Verizon routes non-US matches through "an approved intermediary 501(c)(3) donor-advised fund managed by CAF America" (2024);
  - PepsiCo's 2016 FAQ names SVCF, "a 501(c)(3) Donor-Advised Fund", as the payer;
  - Intel's 2016 FAQ says portal receipts come from American Endowment Foundation, "which acts as a donor advised fund";
  - Apple's guide sends gifts through "a foundation fund based in the United States" administered by Benevity.
- These are the corporate and processor DAF columns sized in [direction-corporate-dafs.md](direction-corporate-dafs.md) §3: the AOGF DAF column ($1.39bn of grants, FYE 2026-03) and SVCF's corporate advised funds.
  - [I] The matching rail and the corporate DAF are often the same account.
  - So the "employee layer" wedge (§5 point 4 there) has two sides: matching an employee's personal DAF grant, and the employer's own match flowing out through a corporate DAF.
- **Correction to earlier repo text.** P&G (MG10 in `matching-gift-daf-policies-2026.csv`, a pre-2021 PDF, `accepts_with_condition`) describes a programme that DtD says was **discontinued on 2016-06-30** [S]. P&G is therefore outside the sample here.

---

## 4. Limits
- **Portal opacity dominates.** For 40 of 68 companies the guidelines sit behind employee logins. "No public text" is not "silent", and the true policy mix of these 40 is unknown.
- **Old documents.** 18 of 28 texts are pre-2021 or undated, so a company may have changed policy since; companies with old documents may also differ from those with new ones.
- **DtD-hosted PDFs.** DtD hosts the company-authored PDFs, and DtD's upload timestamps (filename epochs) postdate the documents. The documents are treated as company text, but a stale upload is possible.
- **Blocked or unreadable primaries.**
  - Amex Global Match guidelines and FAQ (assets.globalgiving.org, robots 403): the 2025 DtD quote is used [S].
  - Intel 2024 retiree guidelines (storage.benevity.com, all agents disallowed): not read. A search snippet said they exclude DAFs; that was not used.
  - ConocoPhillips (robots 403).
  - Bank of America's page renders through JavaScript and yielded no programme text.
  - The Microsoft, Nationwide and Wells Fargo forms seen in search now return 404.
- **Search coverage.** One search per company. A company PDF that exists but was not surfaced is coded `no_public_text`.
- **Sample definition.** It relies on DtD's programme flag. Companies DtD marks "No" may still match through a portal (General Motors: "only matches employee donations made through the General Motors Cares portal").
- **No dollar estimate.** No source gives DAF-funded match volumes, so none is made.
- **Sponsors.** Four were requested; DAFgiving360 could not be read.

---

## 5. Data dictionary: `matching-gifts-dafs-2026-11-20.csv`

| Column | Meaning |
|---|---|
| row_id | MGD + Fortune rank (frame companies); SP01–SP04 (sponsors) |
| record_type | `frame_company` or `daf_sponsor` |
| fortune500_2025_rank | Rank in the Fortune 500 2025 list (Wikipedia rev. 1354288064) |
| entity | Company or sponsor name as listed |
| in_sample | 1 if DtD lists "Matching gift eligible? Yes" (68 rows); 0 otherwise |
| dtd_status | `found` or `not_found` (DtD company page under the tried slugs) |
| dtd_matching_eligible | DtD "Matching gift eligible?" value (Yes or No) |
| dtd_url | DtD company page used |
| dtd_summary_mentions_daf | 1 if the DtD programme summary mentions DAFs (0 for all found rows) |
| daf_grant_policy | Companies: `eligible`, `eligible_conditional`, `excluded`, `silent`, `no_public_text` (definitions in §1.2). Sponsors: `employer_decides`, `silent`, `not_fetched` |
| gift_into_daf_policy | Contributions into a DAF: `eligible`, `eligible_conditional`, `excluded`, `not_stated` |
| public_text_found | 1 if a public guideline or statement was read |
| source_url | URL of the document coded |
| source_type | `company_site`, `company_doc_hosted_by_dtd`, `company_doc_hosted_by_third_party`, `secondary_dtd_article`, `sponsor_site`, `none` |
| doc_date | Document date (see `date_basis`) |
| date_basis | How the date was set: printed date, PDF CreationDate or ModDate, HTTP Last-Modified, article datePublished, or access date |
| recency_ok_2021plus | 1 if `doc_date` is 2021 or later; 0 otherwise |
| condition | Condition attached to eligibility, if any |
| clause_verbatim | Clause extracted verbatim from the downloaded file (whitespace normalised; curly quotes straightened) |
| robots | robots.txt result for the source host |
| accessed | Fetch date (2026-11-20) |
| notes | Caveats, blocked documents, related clauses |

---

## 6. robots.txt and terms log (2026-11-20)

The check treats a Disallow for ClaudeBot, anthropic-ai, Claude-User, Claude-Web or Claude-SearchBot as binding, as well as `*`.

| Host | Result | Used? |
|---|---|---|
| en.wikipedia.org `/wiki/` | allowed (`/w/` disallowed for all) | yes (`/wiki/` only) |
| fortune.com | robots allowed; **terms ban spidering and scraping** | **no** |
| doublethedonation.com | allowed (only `/api/360matchpro/` disallowed); master terms are a client contract with no website-scraping clause | yes, secondary and sample screen |
| files.doublethedonation.com | robots 404, treated as allowed | yes |
| benevity.com | allowed (ClaudeBot and anthropic-ai explicitly allowed); only API terms found | nothing to use |
| causes.benevity.org | **ClaudeBot, anthropic-ai and Claude-Web disallowed** | no |
| storage.benevity.com | **all agents disallowed** | no (Intel 2024) |
| assets.globalgiving.org | robots 403 | no (Amex) |
| www.conocophillips.com | robots 403 | no |
| www.dafgiving360.org | robots 403 | no |
| www.jct.gov | **ClaudeBot, anthropic-ai and Claude-Web disallowed** | no |
| www.federalregister.gov | robots allowed; HTML limited to API access for automated clients | API only (document lookup) |
| www.govinfo.gov, www.irs.gov, www.law.cornell.edu | allowed | yes |
| fidelitycharitable.org, vanguardcharitable.org, nptrust.org | allowed | yes |
| verizon.com, humanafoundation.org, about.bankofamerica.com, cdn-dynmedia-1.microsoft.com (404), hhes.srvusd.net (404) | allowed | yes |
| b-hive.benevity.com, yourcause.com, cybergrants.com | allowed (checked for follow-up; not used) | — |

---

## Source register

| # | Source | Date | Type |
|---|---|---|---|
| S1 | [Wikipedia list (Fortune 500 2025 top 100), rev. 1354288064](https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue) | fetched 2026-11-20 | frame |
| S2 | DtD company pages `doublethedonation.com/matching-gifts/<slug>` (96 found; URLs in CSV) | fetched 2026-11-20 | sample screen [S] |
| S3 | [DtD, "Are DAFs eligible for matching gifts?"](https://doublethedonation.com/matching-gifts-donor-advised-funds) | 2025-09-16 (modified 2025-11-20) | [S] |
| S4 | [Verizon Matching Incentive Program Rules](https://www.verizon.com/about/sites/default/files/Verizon-Matching-Incentive-Program-Rules.pdf) | 2024-12-27 | [F] |
| S5 | [Boeing Gift Match guidelines](https://files.doublethedonation.com/forms/Boeing-guidelines-1675958941.pdf) | 2022-07-08 | [F] |
| S6 | [RTX matching guidelines](https://files.doublethedonation.com/forms/Raytheon-Technologies-guidelines-1703107219.pdf) | 2021-03 | [F] |
| S7 | [Disney Matching Gifts terms](https://files.doublethedonation.com/forms/walt-disney-guidelines.pdf) | 2021-02-03 | [F] |
| S8 | [Merck Partnership for Giving guidelines](https://files.doublethedonation.com/forms/Merck---Co--guidelines-1686482653.pdf) | 2021-05-19 | [F] |
| S9 | [Humana Foundation FAQ](https://www.humanafoundation.org/faqs) | live, 2026-11-20 | [F] |
| S10 | [Microsoft CY25 Max the Match](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/CY25-Max-the-Match.pdf) | 2026-06-30 | [F] |
| S11 | [Delta matching guidelines](https://files.doublethedonation.com/forms/Delta-Air-Lines-guidelines-1664891658.pdf) | 2022-09-27 | [F] |
| S12 | Pre-2021 or undated company PDFs: [UnitedHealth](https://files.doublethedonation.com/forms/UnitedHealth-Group-Incorporated-guidelines-1680030612.pdf), [Apple](https://doublethedonation.com/forms/apple-guide.pdf), [JPMorgan](https://doublethedonation.com/forms/jp-morgan-chase.pdf), [Chevron](https://doublethedonation.com/forms/chevron.pdf), [NVIDIA](https://files.doublethedonation.com/forms/nvidia-guidelines.pdf), [PepsiCo](https://doublethedonation.com/forms/pepsico-guidelines.pdf), [IBM](https://hhes.srvusd.net/documents/Parents/Hawks-Ed-Fund/Fundraisers/FREE-Money/Corporate-Matching/IBM-Matching-Grants-Program-Form.pdf), [Lilly](https://doublethedonation.com/forms/eli-lilly-guidelines.pdf), [Travelers](https://doublethedonation.com/forms/travelers.pdf), [BMS](https://files.doublethedonation.com/forms/bms.pdf), [Fannie Mae](https://doublethedonation.com/forms/fannie-mae-mg.pdf), [Dell](https://doublethedonation.com/forms/dell.pdf), [MetLife](https://doublethedonation.com/forms/metlife.pdf), [NY Life](https://doublethedonation.com/forms/new-york-life-education.pdf), [Intel](https://doublethedonation.com/forms/intel-guidelines.pdf), [Deere](https://doublethedonation.com/forms/john-deere-guidelines.pdf), [Nike](https://doublethedonation.com/forms/nike-guidelines.pdf), [Coca-Cola](https://doublethedonation.com/forms/coke.pdf) | 2010–2020 | [F], flagged |
| S13 | [Fidelity Charitable grantmaking FAQ](https://www.fidelitycharitable.org/faqs/donor/grantmaking.html); [programme guidelines PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) | live; PDF 2026-09-11 | [F] |
| S14 | [Vanguard Charitable policies and guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines); [FAQ](https://www.vanguardcharitable.org/faqs) | 2026-03-12 | [F] |
| S15 | [NPT, A Guide to your Donor-Advised Fund](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) | PDF 2026-10-15 | [F] |
| S16 | [IRS Notice 2017-73](https://www.irs.gov/pub/irs-drop/n-17-73.pdf) | 2017 (pre-2021; governing notice) | [F] |
| S17 | [Proposed regs, Taxes on Taxable Distributions From DAFs Under Section 4966, 88 FR 77922](https://www.govinfo.gov/content/pkg/FR-2023-11-14/pdf/2023-24982.pdf) | 2023-11-14 | [F] |
| S18 | [26 U.S.C. §4967 (LII)](https://www.law.cornell.edu/uscode/text/26/4967) | current | [F] |
