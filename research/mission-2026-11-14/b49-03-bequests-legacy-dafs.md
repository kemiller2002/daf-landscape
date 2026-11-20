# b49-03: Bequests and estate flows into and out of DAFs, FY2024 top-20 sponsors

**Task:** b49-03 · **Date:** 2026-11-20 · **Status:** first pass on a new direction

**Outputs**
- Data: `data/mission-2026-11-14/bequests-legacy-dafs-2026-11-20.csv` (309 rows: 109 policy rows and 200 filing rows)
- Script: `scripts/mission_b49_03_estate_flows.py`
- Queue proposals: `data/mission-2026-11-14/queue-proposals-b49-03.csv`

Evidence labels:
- **[P]** a sponsor's own document. The quote is re-checked against the saved text by the script. All 93 quoted policy rows pass.
- **[F]** computed from Form 990 XML.
- **[R]** carried from an earlier repo file and not re-read in this pass.
- **[NF]** not found in the documents read.
- **[B]** blocked by robots.txt or by site terms.

---

## 1. Summary

1. **Every sponsor with a readable estate-gift document accepts bequests: 13 of 13 [P].** Of the top 20:
   - 13 state that they accept bequests;
   - 12 state that they accept retirement-plan or IRA beneficiary designations;
   - 11 state that they accept life insurance;
   - 8 state that they accept CRT or charitable-lead-trust remainders.

   No document read says any of these is refused. The gaps mean "not stated", or that no readable document exists. JCF, MS GIFT and FFTC repeat the tax point: an IRA can name the DAF as death beneficiary, but a lifetime QCD into a DAF is not allowed.
2. **Default when no successor is named: the sponsor's own pool, in 11 of the 15 sponsors whose default is known [P].** Fidelity, NPT, Vanguard, SVCF, MS GIFT, BofA CGF, CCT, ImpactAssets, FFTC, JCF and CJP send an un-planned balance to:
   - an unrestricted fund or general fund;
   - an endowment;
   - an "Undesignated" or "Giving" fund.

   The other four known defaults:
   - **Sponsor discretion:** 2. RCF uses "written instructions or its internal policies". GKCCF uses "charitable purposes".
   - **Granting history:** 2, both carried from the repo [R]. They are DAFgiving360 and NCF.

   Unknown for five sponsors:
   - **Not found:** AEF, Greater Horizons and Dechomai.
   - **Blocked:** GS DAF and Raymond James Charitable.

   **No top-20 sponsor uses a named-charity default.** A charity receives the balance only if the donor names one.
3. **Only four sponsors publish a cap on successor generations [P]:**
   - **SVCF:** at most three successor advisors in aggregate.
   - **CCT:** "maximum of two generations of successor advisors".
   - **FFTC:** one generation unless the opening donor authorises more in writing.
   - **CJP:** children and their spouses by default; further successors only at CJP's discretion.

   The other sponsors split as follows:
   - **Perpetual in so many words:** NPT ("continue in perpetuity"), Vanguard ("in perpetuity", "under present guidelines") and JCF ("no limit to succession").
   - **Reserves the right to cap without publishing a cap:** MS GIFT ("specific number of generations and/or years").
   - **Open-ended by structure:** Fidelity, RCF and BofA. A successor may name further successors.
4. **Fixed-term legacy programmes exist at two sponsors and endowment options at two more [P]:**
   - **Fixed-term:**
     - Fidelity Endowed Giving Program: at least five years after death, $100,000 minimum.
     - Vanguard Endowed Grant Plan: minimum term of five years, at least 5% a year.
   - **Spend-down endowment:** NPT's Endowment Program pays annual grants until the account is spent down. It needs $100,000 at activation and pays a lump sum once the balance reaches $25,000.
   - **Endow at succession:** FFTC lets donors endow the fund (perpetual) when successors take over.
   - **Dormancy rule rather than a programme:** at MS GIFT, named charities are paid automatically if successors make no grant for five consecutive years.
5. **Filings cannot measure bequest inflows [F].** Form 990 has no bequest line:
   - Part VIII line 1;
   - Schedule D Part I;
   - Schedule M.

   Bequests, IRA death benefits and CRT remainders mostly arrive as cash or listed securities, so they are indistinguishable from lifetime gifts. Schedule M shows only:
   - **Life insurance:** named "Other" lines at four sponsors, $1,567,325 in total. That is 0.002% of $85.9bn in contributions.
   - **Trust interests:** $2.54bn, 4.6% of Schedule M. This line is pooled with partnership and LLC interests and cannot be separated.

   Schedule B donor names are not in public XML, so "estate of" donors cannot be counted.
6. **No sponsor publishes a legacy-gift or succession figure in the reports read [NF].** None of the following gives such a figure:
   - Fidelity 2025 and 2026 Giving Reports and the 2026 impact snapshot;
   - NPT 2025 Annual Report;
   - Vanguard Charitable 2025 annual-report page;
   - SVCF annual-report page.

   The figure is not given as a dollar amount, as an account count or as a share. The flow therefore cannot be quantified from public sponsor data at present.

---

## 2. Method

1. **Sponsor list.** FY2024 top 20 by DAF assets, with EINs, from `data/mission-2026-11-14/sponsor-terms-census-top20-2026.csv`.
2. **Existing coverage.** Grepped `research/` and `data/` for successor, succession, bequest and legacy. Relevant prior work:
   - `donor-feature-census-2026.csv` (feature `family_successor_roles`, Y/U flags only);
   - `queue-state-filings-transfer-terms.md` (NCF succession-fund restriction, DAFgiving360 dormant-account rule);
   - `sponsor-transfer-portability-terms.csv` (NPT abandoned accounts go to the NPT Giving Fund).

   None recorded:
   - inflow acceptance;
   - default dispositions for most sponsors;
   - generation caps;
   - legacy-term programmes;
   - filing tests.

   This pass adds those and fills four `U` cells in the feature census: RCF, CCT, ImpactAssets and CJP.
3. **Documents.**
   - Fetched with a generic user agent (`research-script/1.0`) through a robots helper. The helper:
     - checks robots.txt for the groups ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot, `research-script/1.0` and `*`;
     - fetches only if all of them allow the path.
   - Text extraction:
     - **Text PDFs:** `pdftotext -layout`.
     - **Two PDFs with Type-3 fonts:** extracted by OCR (`tesseract`). These are the MS GIFT Donor Circular and the BofA CGF Guidelines v8.2025.
   - Discovery used web search, and only primary sponsor URLs were then fetched.
4. **Coding.**
   - Each sponsor is coded on these dimensions, with values Y / NS / NF / BLOCKED or a short description:
     - `inflow_bequest`
     - `inflow_retirement_beneficiary`
     - `inflow_life_insurance`
     - `inflow_crt_remainder`
     - `default_no_successor`
     - `named_charity_option`
     - `legacy_program_fixed_years`
     - `successor_generation_limit`
     - `successor_nonresponse_rule`
     - `succession_by_will`
     - `estate_gift_handling`
   - Quotes are stored in the script (`POLICY`).
   - `quote_ok()` normalises both the quote and the document to lowercase alphanumerics, and checks that each `...`-separated fragment occurs.
5. **Filings.**
   - Source: the latest Form 990 per EIN in the IRS TEOS indexes for 2021–2026 (tax periods 2024-12 to 2025-09).
   - XML comes from the GivingTuesday mirror. Its robots.txt returns 404, re-checked 2026-11-20. Eleven files were already cached and nine were fetched.
   - Extracted:
     - Part VIII lines 1g and 1h;
     - Schedule D Part I line 2;
     - every Schedule M line (count and amount);
     - Schedule M "Other" descriptions;
     - line 29 (Form 8283 count);
     - narrative elements (ExplanationTxt, Desc, mission and activity text) that mention bequest, estate, IRA, retirement, insurance, remainder, testamentary, legacy, split-interest or lead trust.
   - Name and address fields are excluded because recipient names such as "ESTATE" produced false hits.
6. **Run:**

   ```
   python3 -I scripts/mission_b49_03_estate_flows.py . --web-dir <scratch>/b49-03 --irs-dir <scratch>/irs \
     --irs-dir ~/.cache/daf-landscape/irs-index --xml-cache <cached xml dirs> --xml-dir <scratch>/b49-03/xml [--fetch]
   ```

   Consistency check: Schedule M totals equal Part VIII line 1g in aggregate ($55,399,640,814 both).

---

## 3. Results

### 3.1 Inflows: published acceptance of estate-type gifts [P]

| # | Sponsor | Bequest / will | IRA or plan beneficiary | Life insurance | CRT remainder | Note | Doc |
|---|---|---|---|---|---|---|---|
| 1 | Fidelity Charitable | Y | Y | Y (fee clause) | NS ("Trusts" only) | Estate gifts go through intake via a "supporting organization" and may be "case-by-case"; a legal/admin fee may be charged | Program Guidelines 2026 |
| 2 | NPT | Y | Y (IRA, 401(k)) | Y | Y (CRT, CLT) | Also TOD accounts | Guide to your DAF 2026 |
| 3 | DAFgiving360 | B | B | B | B | dafgiving360.org on the blocked list | — |
| 4 | Vanguard Charitable | Y | Y | Y | Y (web page) | "Intent to Give" form | Policies & Guidelines Jan 2026; Deferred-giving page |
| 5 | GS DAF | B | B | B | B | gspf.goldman.com robots-disallowed | — |
| 6 | SVCF | Y (testamentary gift type) | NS | NS | NS | | DAF Agreement 2025 |
| 7 | AEF | Y ($25,000 DAF opened in advance) | Y | Y (complex asset) | NS (page 404) | | Giving Guide Booklet 2026; /bequests |
| 8 | MS GIFT | Y | Y | Y | Y (CRT, CLT) | | Donor Circular 2024 (OCR) |
| 9 | RCF | Y | Y | NS | Y | LPL-channel circular | 2309 circular (2026 upload) |
| 10 | NCF | B | B | B | B | site terms ban extraction | — |
| 11 | BofA CGF | Y | Y | Y | Y | | Program Guidelines v8.2025 (OCR) |
| 12 | CCT | Y | Y | Y | Y | Estate-plan checkboxes on DAF application | DAF Application (Feb 2024) |
| 13 | ImpactAssets | NS | NS | NS | NS | Circular returned 403 | — |
| 14 | FFTC | Y | Y | Y (≥$250k if premiums due) | Y (to endowed fund; FFTC as trustee; $250k minimum) | | Charitable Giving Guide (Oct 2026) |
| 15 | JCF | Y | Y | Y | Y | | Policy Guide Aug 2024 |
| 16 | GKCCF | Y | Y | Y | NS | 3% one-time fee on pass-through bequests | Online fund agreement |
| 17 | Greater Horizons | Y | Y | Y | NS | | Contribute page |
| 18 | Dechomai | NS | NS | NS | NS | Site lists CRT services for charities, not as a DAF inflow | Policies page |
| 19 | CJP | NS | NS | NS | NS | DAF policy silent on inflows | DAF Policies & Procedures 2026 |
| 20 | Raymond James Charitable | B | B | B | B | robots 403 / unreachable | — |

**Process details that matter:**
- **BofA:** the Charitable Gift Fund cannot honour succession plans written into a will, trust or other estate-planning document.
- **JCF:** a donor cannot establish a succession plan for an existing DAF through their will.
- **AEF:** to direct a bequest to a DAF, the donor must open the DAF in advance with $25,000.
- **Fidelity:** may charge "an additional fee for legal and other expenses" on testamentary transfers.
- **GKCCF:** charges 3% on bequests that are fully passed through to charities on receipt.

### 3.2 Outflows at death: default disposition, legacy options and generation limits [P]

| # | Sponsor | Default with no successor and no charity named | Category | Named charity at death | Fixed-term or endowment legacy option | Successor generations |
|---|---|---|---|---|---|---|
| 1 | Fidelity | Unrestricted funds of Fidelity Charitable; also if no successor responds within 90 days | general fund | Y | Endowed Giving Program, ≥5 years after death, $100k minimum | No stated limit (successor becomes an Account Holder) |
| 2 | NPT | NPT Giving Fund ("default Legacy Plan option") | general fund | Y | Endowment Program, annual grants until spent down, $100k minimum | Perpetual ("continue in perpetuity") |
| 3 | DAFgiving360 [R] | Eligible charities by granting history (dormant, no plan) | granting history | — | — | — |
| 4 | Vanguard | "may be transferred to the Philanthropic Impact Fund" | general fund | Y | Endowed Grant Plan, minimum term 5 years, ≥5% a year | Perpetual "under present guidelines" |
| 5 | GS DAF | BLOCKED | — | — | — | — |
| 6 | SVCF | Community Endowment Fund | general fund | — | — | **Cap: 3 successor advisors in aggregate** |
| 7 | AEF | NF | — | Y ("terminate the accounts upon death and recommend granting out") | — | No stated limit ("generationally", fact sheet) |
| 8 | MS GIFT | Undesignated Fund at Board discretion | general fund | Y | Not a term programme. Named charities are paid automatically after 5 consecutive years with no successor grant | Allowed, but MS GIFT "reserves the right to limit … to [a] specific number of generations and/or years" |
| 9 | RCF | Written instructions or "its internal policies" | sponsor discretion | Y (lump sum or % annually; not combinable with individual successors) | Charity "percentage annually" | No stated limit |
| 10 | NCF [R] | Grantmaking history | granting history | — | — | Succession funds must stay within NCF |
| 11 | BofA CGF | General Fund (the CGF endowment fund) | general fund | Y | — | No stated limit (successor may name a subsequent Successor) |
| 12 | CCT | Converted to an unrestricted fund, or general endowment if below minimum | general fund | Y | (Case study only: endowed DAF for "next two generations") | **Cap: two generations** |
| 13 | ImpactAssets | Option 1, the ImpactAssets permanent fund ("default to Option (1)") | general fund | Y | — | NS (circular 403) |
| 14 | FFTC | FFTC policies for undirected Gift Funds | general fund | Y | Endow the fund when successors take over (perpetual, spendable amount only) | **One generation unless the opening donor authorises more** |
| 15 | JCF | JCF Special Gifts Fund; also if successors do not respond within 1 year | general fund | Y | — | None ("no limit to succession"); JCF may limit the number of successors |
| 16 | GKCCF | "use the principal and income from the Fund for charitable purposes" | sponsor discretion | — | — | NS |
| 17 | Greater Horizons | NF | — | — | — | NS |
| 18 | Dechomai | NF | — | — | — | NS |
| 19 | CJP | CJP Unrestricted Endowment Fund | general fund | Y | — | **Children and spouses by default; more at CJP discretion** |
| 20 | Raymond James | BLOCKED | — | — | — | — |

**Comparison: generations allowed against default disposition.** The figures below cover the 15 sponsors with a generation row: 12 with a published rule, NCF [R], and 2 where no rule is stated.

| Generation rule | Sponsors | Default when nothing is named |
|---|---|---|
| Perpetual, stated | NPT, Vanguard, JCF (3) | All 3 go to the sponsor's general fund |
| Open-ended, no explicit statement | Fidelity, RCF, BofA, AEF (4) | Fidelity and BofA: general fund. RCF: discretion. AEF: not found |
| Reserved right to cap | MS GIFT (1) | General fund (Undesignated) |
| Hard cap or one-generation default | SVCF (3 successors), CCT (2 generations), FFTC (1 unless authorised), CJP (children by default) (4) | All 4 go to the sponsor's general fund or endowment |
| Restricted by destination | NCF [R] (1) | Granting history [R] |
| Not stated | ImpactAssets, GKCCF (2) | ImpactAssets: permanent fund. GKCCF: discretion |

**Reading:**
- **Caps by type.** All four caps or one-generation defaults are at community or federation sponsors (SVCF, CCT, FFTC, CJP). The perpetual statements are at nationals (NPT, Vanguard) and at JCF.
- **Defaults by type.** National commercial sponsors default to their own pool, as community foundations do. The difference between them is in how far succession may run, not in the default.
- **Comparison with an earlier source.** The repo timeline (`competitive-history-timelines.md`) records Schwab Charitable's 2011 "Charitable Legacy" programme. That evidence is pre-2021, so it is not used here, and the current DAFgiving360 policy could not be re-read.

### 3.3 Filings: what Form 990 can and cannot show [F]

The aggregates cover the latest filing per sponsor, tax periods 2024-12 to 2025-09, so the 20 returns are not one common year.

| Measure | Value (20 sponsors) |
|---|---|
| Total contributions (Part VIII 1h) | $85,914,142,313 |
| Noncash contributions (1g) | $55,399,640,814 (64.5%) |
| Contributions to DAFs (Sch D I line 2) | $84,932,846,946 (98.9% of 1h) |
| Schedule M line 11, partnership/LLC/trust interests | $2,536,245,552 (4.6% of Schedule M) |
| Schedule M "Other" lines naming insurance | $1,567,325 across 11 gifts at 4 sponsors (all Life insurance unless noted):<br>– Fidelity: $816,122 (6)<br>– Vanguard: "INSURANCE", $620,945 (2)<br>– RCF: $86,605 (2)<br>– DAFgiving360: $43,653 (1) |
| Form 8283s received (line 29) | 587, across the sponsors that report the line |

**Narrative hits.** These show sponsors' own split-interest activity, not DAF inflows:
- **Fidelity:** "remainder interest of pooled income fund" (a reconciliation line).
- **SVCF:** "Charitable Remainder Trusts Held for Others".
- **CCT:** gains on beneficial interests in charitable term and perpetual trusts.
- **GKCCF:** CRT obligations and life-insurance value change.
- **CJP:** "Provide annuities to donors and remainder gifts to CJP".
- **Raymond James:** CRT and CLT domiciles, and eight irrevocable trusts in which it holds more than 50% of the beneficial interest.
- **RCF:** "SPLIT INTEREST AGREEMENTS".

**Can be measured from public filings:**
- noncash gifts by asset type (Schedule M);
- life insurance, where a sponsor itemises it as "Other";
- whether a sponsor holds split-interest trusts;
- total contributions to DAFs.

**Cannot be measured:**
- bequest or estate dollars;
- IRA or retirement-plan death benefits;
- CRT remainders received in cash or securities;
- how many DAFs passed to successors, or how many passed to the sponsor's pool, and the dollar amounts in either case;
- outflows to the sponsor's general fund at death. These appear, if at all, as internal transfers, not grants.

Schedule B contributor names are withheld from public XML for 501(c)(3) public charities, so "Estate of …" contributors cannot be counted.

**Possible indirect route.** Some audited financial statements separate "bequests" or "planned gifts" in a revenue note. None of the top-20 audits was read in this pass (see the queue proposals).

---

## 4. Limits

- **Scope of each source.**
  - The RCF evidence comes from the LPL-channel circular. Other RCF and Ren private-label programmes may differ.
  - The CCT rules come from the DAF application terms of February 2024.
  - The GKCCF rules come from the online fund agreement page, which is undated.
- **OCR.** The MS GIFT and BofA texts were OCR'd. The quotes were checked against the OCR text, and BofA's v3.2024 text layer gives the same wording.
- **Untested or missing documents.**
  - The Fidelity, NPT, Vanguard and FFTC documents were read in full. For the others, an "NS" may mean only that the term is in a document that is not public.
  - The AEF default disposition and the Greater Horizons and Dechomai succession terms were not found.
  - The ImpactAssets programme circular returned 403.
- **Repo carry-overs.** DAFgiving360 and NCF rows are carried from repo files read on 2026-11-14 and were not re-verified.
- **Defaults.** "Default" means the published rule. Most rules say "may", and boards keep discretion (Vanguard, MS GIFT, FFTC).
- **Filings.**
  - The 20 returns have mixed fiscal years, so the aggregates are a cross-section, not a single-year market figure.
  - The Schedule M "trust interests" line also includes partnership and LLC interests.
- **Sponsor reports.** No sponsor published a legacy-flow figure in the reports read. Absence is "not found", not "not published anywhere".
- **Stray requests.** Two requests to a bare host root went out by error and did not connect. The robots helper was then patched so that an unreachable robots.txt blocks the fetch. The two hosts were:
  - `www.static1.squarespace.com/`;
  - `www.raymondjamescharitable.org/`.

  No content was obtained from either.

---

## 5. Robots and access log

| Host | robots.txt | Result |
|---|---|---|
| www.fidelitycharitable.org, fidelitycharitable.org | 200, allowed | Guidelines, FAQ and reports fetched |
| www.nptrust.org | 200, allowed | Guide and annual report fetched |
| www.vanguardcharitable.org | 200, allowed | Guidelines, deferred-giving page and annual report fetched |
| gspf.goldman.com | 200, **disallowed** for the circular path | Not fetched; no mirror used |
| www.svcf.org | 200, allowed | Fetched |
| aefonline.org, www.aefonline.org, advisorwelcome.aefonline.org | 200, allowed | Fetched. Two URLs returned 404 |
| mail.aefonline.org | unreachable | Not fetched |
| msgift.donorfirstx.com, bofa.donorfirst.org | 404 (no rules) | Fetched |
| www.bankofamerica.com | 200, allowed | v3.2024 guidelines fetched |
| donorportal.cct.org, www.cct.org | 200, allowed | Fetched |
| cct.org (DAF policy page) | 200, allowed | HTTP 403 on the page |
| impactassets.org | 200, allowed | Succession form fetched; circular 403 |
| www.fftc.org | 200, allowed | Fetched |
| jcfny.org | 200, allowed | Fetched; annual-report URL 404 |
| www.growyourgiving.org, www.greaterhorizons.org | 200, allowed | Fetched |
| dechomai.org | 200, allowed | Fetched |
| www.cjp.org | 200, allowed | Fetched |
| www.reninc.com, renaissancecharitable.org | 200, allowed | Fetched; three older circular URLs 404 |
| intercom.help | 200, allowed | 404s |
| www.raymondjames.com | 403 (treated as disallow) | Not fetched |
| raymondjamescharitable.org | unreachable | Not fetched |
| dafgiving360.org | Task blocked list | Not fetched (Squarespace-hosted policy PDF also not fetched) |
| www.ncfgiving.com, secure.ncfgiving.com | Terms ban / robots disallow all | Not fetched |
| gt990datalake-rawdata.s3.amazonaws.com | 404 (no rules) | 9 XML fetched |

---

## 6. Data dictionary: `bequests-legacy-dafs-2026-11-20.csv`

Long format: one row per sponsor and dimension.

| Column | Meaning |
|---|---|
| record_id | `B4903-Pnnn` (policy) or `B4903-Fnnn` (filing) |
| rank_fy2024 | FY2024 rank by DAF assets (repo top-20 list) |
| sponsor, ein | Sponsor name and 9-digit EIN |
| record_type | `policy` or `filing` |
| dimension | See the list below |
| value | Coded value. Policy: `Y`, `N`, `NS` (not stated in the doc read), `NF` (no doc found), `BLOCKED`, or a short description. Filing: a number or text |
| quote | Exact fragment(s) from the document; ` ... ` separates fragments |
| quote_verified | `yes` (all fragments found in the saved text), `no`, `doc_missing`, `n/a` (no quote), `repo` (carried) |
| source_url | Primary URL, or the 990 XML URL |
| source_date | Document date as shown, or tax period |
| robots | robots.txt status for the host |
| evidence_label | `primary_doc`, `carried_from_repo`, `not_found`, `blocked`, `computed_from_990_xml` |
| retrieved | 2026-11-20 |
| notes | Context and caveats |

**Policy dimensions:**

| Dimension | Meaning |
|---|---|
| inflow_bequest | Accepts gifts by will or bequest |
| inflow_retirement_beneficiary | Can be named beneficiary of an IRA or retirement plan |
| inflow_life_insurance | Accepts life insurance |
| inflow_crt_remainder | Can be the remainder beneficiary of a CRT |
| estate_gift_handling | Intake route or fee for estate gifts |
| default_no_successor | Where the balance goes if no successor or charity is named. Categories: `sponsor_general_fund`, `sponsor_discretion`, `granting_history` |
| named_charity_option | Donor may name charities to receive the balance at death |
| legacy_program_fixed_years | Post-death programme with a term or an endowment |
| successor_generation_limit | Cap on successor generations |
| successor_nonresponse_rule | Time before an unresponsive successor is bypassed |
| succession_by_will | Whether a will can set the DAF succession |
| successor_options | Combinations of successor types allowed |

**Filing dimensions:**

| Dimension | Meaning |
|---|---|
| f990_total_contributions_usd | Part VIII line 1h |
| f990_noncash_contributions_usd | Part VIII line 1g |
| f990_noncash_share_of_contributions | 1g / 1h |
| schd_daf_contributions_usd | Schedule D Part I line 2 col (a) |
| schm_total_reported_usd | Sum of Schedule M column (c) |
| schm_trust_interests_usd | Schedule M line 11 |
| schm_other_lines | Schedule M lines 25–28 (description, count, $) |
| schm_other_lines_estate_keyword_usd | "Other" lines whose description matches an estate keyword |
| schm_form8283_count | Schedule M line 29 |
| estate_keyword_text_hits | Count of matching narrative elements, with excerpts in `notes` |

---

## 7. Source register

| ID | Source | URL | Date |
|---|---|---|---|
| S1 | Fidelity Charitable Program Guidelines | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf | 2026-09 |
| S2 | Fidelity Charitable FAQ, successors | https://www.fidelitycharitable.org/faqs/all/who-can-be-successor.html | live 2026-11-20 |
| S3 | Fidelity Charitable 2026 and 2025 Giving Reports; 2026 impact snapshot | https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf ; https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf ; https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-impact-snapshot.pdf | 2025–2026 |
| S4 | NPT, A Guide to your Donor-Advised Fund | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf | 2026-10 |
| S5 | NPT 2025 Annual Report | https://www.nptrust.org/annual-reports/npt-annual-report/ | 2026 |
| S6 | Vanguard Charitable Policies and Guidelines | https://www.vanguardcharitable.org/sites/default/files/2026-01/policies_and_guidelines_january_2026_011326_final_0.pdf | 2026-01 |
| S7 | Vanguard Charitable planned and deferred giving | https://www.vanguardcharitable.org/contributions/deferred-giving | live |
| S8 | Vanguard Charitable Annual Report 2025 | https://www.vanguardcharitable.org/2025annualreport | 2025 |
| S9 | SVCF Donor Advised Fund Agreement | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf | 2025 |
| S10 | AEF DAF Giving Guide Booklet | https://advisorwelcome.aefonline.org/wp-content/uploads/2026/01/AEF-DAF-Giving-Guide-Booklet_General_FINAL-1.pdf | 2026-01 |
| S11 | AEF Naming AEF as a Beneficiary | https://www.aefonline.org/bequests | live |
| S12 | AEF Difference Fact Sheet 2026 | https://www.aefonline.org/wp-content/uploads/2026/04/AEF_Difference_Fact-Sheet_2026.pdf | 2026-04 |
| S13 | AEF, successor advisors article | https://www.aefonline.org/?p=9817 | live |
| S14 | MS GIFT Donor Circular and Disclosure Statement | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Circular%20and%20Disclosure%20Statement.pdf | 2024-08 |
| S15 | MS GIFT Donor Contribution Agreement | https://msgift.donorfirstx.com/pdf/MSGIFT/Donor%20Contribution%20Agreement.pdf | 2024-07 |
| S16 | RCF DAF circular (LPL, 2309) | https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf | 2026-05 upload |
| S17 | RCF FAQs | https://renaissancecharitable.org/faqs/ | live |
| S18 | BofA CGF Program Guidelines v8.2025 | https://bofa.donorfirst.org/pdf/bofa/CGF%20Program%20Guidelines.pdf | 2025-08 |
| S19 | BofA CGF Program Guidelines v3.2024 | https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf | 2024-03 |
| S20 | CCT DAF Application | https://donorportal.cct.org/ma/docs/cct/CCT-DAF-Application.pdf | 2024-02 |
| S21 | CCT Intro to DAFs 2025 | https://www.cct.org/wp-content/uploads/2025/09/IntrotoDAFs_2025.pdf | 2025-09 |
| S22 | ImpactAssets Succession Plan form GE534A | https://impactassets.org/ge534a_ia_daf_succession-plan | 2025-03 |
| S23 | FFTC Charitable Giving Guide | https://www.fftc.org/sites/default/files/documents/charitable_giving_guide.pdf | 2026-10 |
| S24 | FFTC DAF Agreement | https://www.fftc.org/sites/default/files/documents/FFTC_DAF_Agreement_Fillable.pdf | 2026-11 |
| S25 | JCF Policy Guide | https://jcfny.org/app/uploads/2024/08/Policy-Guide-Aug-2024_SP.pdf | 2024-08 |
| S26 | GKCCF online DAF agreement | https://www.growyourgiving.org/open-a-donor-advised-fund/ | live |
| S27 | GKCCF Succession and Legacy Planning page | https://www.growyourgiving.org/documents/Your-Philanthropic-Legacy.pdf | live |
| S28 | Greater Horizons, Contribute to your fund | https://www.greaterhorizons.org/individual-family-giving/contribute-to-your-fund/ | live |
| S29 | Dechomai Policies and Procedures | https://dechomai.org/policies-and-procedures/ | live |
| S30 | CJP DAF Policies and Procedures | https://www.cjp.org/hubfs/DAF/DAF%20Policies%20and%20Procedures.pdf?hsLang=en | 2026-04 |
| S31 | Form 990 XML, 20 returns (object IDs in the CSV `source_url`) | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml | TP 2024-12 to 2025-09 |
| S32 | IRS TEOS e-file indexes 2021–2026 | https://apps.irs.gov/pub/epostcard/990/xml/{YYYY}/index_{YYYY}.csv (local copies) | 2026 |
| R1 | Repo: DAFgiving360 and NCF succession terms | research/mission-2026-11-14/queue-state-filings-transfer-terms.md | read 2026-11-14 |
| R2 | Repo: family_successor_roles census | data/mission-2026-11-14/donor-feature-census-2026.csv | 2026 |
