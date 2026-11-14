# Queue answers: Givinga / DAF Direct infrastructure (Q-B18), nonprofit receipt cost by rail (Q-B12), emerging-entrant funding and AI (Q-N09)

**Date:** 2026-11-14. **Status:** Desk research using primary filings (SEC Form D, IRS e-file XML), first-party pages, and labelled secondary press. No interviews and no authenticated platform access. Out of scope here: failed startups and user complaints, which other agents cover.

**Data files:**
- [data/mission-2026-11-14/nonprofit-receipt-cost-by-rail.csv](../../data/mission-2026-11-14/nonprofit-receipt-cost-by-rail.csv)
- [data/mission-2026-11-14/emerging-entrants-funding-ai.csv](../../data/mission-2026-11-14/emerging-entrants-funding-ai.csv)
- [data/mission-2026-11-14/queue-proposals-infrastructure.csv](../../data/mission-2026-11-14/queue-proposals-infrastructure.csv)

**Evidence tags:**
- **[F]** is a fact from a cited source.
- **[C]** is a calculation from cited inputs.
- **[A]** is an assumption, labelled.
- **[I]** is an inference.

---

## 0. Answers in brief

| Q | Answer | Confidence |
|---|---|---|
| **Q-B18 Givinga** | **No, as far as public evidence shows: one sponsor with many channel partners.** Every disclosed Givinga "giving account" sits at a single sponsor, Givinga Foundation (EIN 47-4172718). The Foundation has zero employees and names Givinga, Inc. as its "administrative provider". Givinga's technology reaches companies directly and through partner platforms (EarthShare, PlanSource, WeSpire, Double the Donation), but **no second DAF sponsor running on Givinga technology was found**. | Medium-high on the structure. Low on the client list. |
| **Q-B18 Givinga account count** | **Verified in IRS XML, with a caveat.** The CY2024 Schedule D reports **1,421,011 DAF accounts, $12,300,836 contributed, $12,417,069 granted and $1,949,239 at year end** (about $1.37 per account [C]). These figures come from an **amended** e-filed return (2025-11-13) that changed only Schedule D Part I. The original return (2025-08-25) carried no Schedule D DAF values. | High on the numbers. Low on what counts as an "account". |
| **Q-B18 DAF Direct** | **Yes, multi-sponsor, but sponsor-run and only three sponsors.** The legal operator named in its terms and privacy policy is **"DAF Direct Trust"**, governed by Massachusetts law. Fidelity operates it day to day, on technical evidence: fmr.com contact, Fidelity's metrics domain and analytics account, the same registrar and DNS as fidelitycharitable.org, and Fidelity Charitable led the 2013 launch. Connected sponsors are **Fidelity Charitable, DAFgiving360 and BNY Mellon Charitable Gift Fund** (BNY Charitable's site is live). DAF Direct only **initiates** a recommendation. The sponsor approves the grant and pays it on its own rail, and no money flows through DAF Direct. | High on the operator name and sponsors. Medium on the Fidelity attribution (inferred). |
| **Q-B12** | Ranges per $1,000 grant, and what drives them:<br>• **Electronic sponsor rails:** $0 in fees. All-in cost **about $1.2-$2.4** in the base case, almost all of it staff time (assumed).<br>• **Paper checks:** **about $5-$8 base, up to about $24**, from staff time plus float. The AFP benchmark of $1-$2 is a floor.<br>• **Chariot DAFpay at default terms:** **$29 fee**, about $32 all-in. Subscriptions and platform agreements can lower or remove it.<br>No published survey measures nonprofit staff minutes per DAF grant, so the staff-time inputs are labelled assumptions. | High on the fees. Low on staff time. |
| **Q-N09** | Funding is now **sourced for 10 entities**, 4 of them from SEC Form D. AI evidence is overwhelmingly **U (unverified vendor claims)**:<br>• Chariot's LLM gift coding is **D** (vendor-published customer case).<br>• The only **E** is a press report of Circle Foundation's internal agents.<br>• Fundraise Up "Agentic Giving" is **A** (announced only).<br>None of the DAF sponsors studied (Endaoment, Givinga, Every.org, Groundswell's sponsor) makes an AI claim about grant approval. | High on the rounds. Medium on the AI classification. |

---

## 1. Q-B18: Are Givinga and DAF Direct multi-sponsor infrastructure?

### 1.1 Givinga: one sponsor, a technology company, many channels

**Entity structure**
- **Givinga, Inc.** is a Delaware corporation with its business address at 711 Atlantic Ave, Boston. It is SEC filer CIK 0001720830. [F: [SEC EDGAR company record](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001720830&type=D)]
- **Givinga Foundation Inc** is a 501(c)(3) in Wellesley, MA, with ruling date 2015-08 and NTEE code T12. [F: [ProPublica API](https://projects.propublica.org/nonprofits/api/v2/organizations/474172718.json)]
- The Foundation describes itself as "the separate 501(c)(3) public charity that operates charitable accounts, sponsorship, and disbursements". It says Givinga, Inc. "builds Philantech… that powers every Givinga experience". [F: [givingafoundation.org](https://www.givingafoundation.org/)]

**What the CY2024 Form 990 shows** (IRS TEOS e-file XML, object 202503179349301975, amended; the original is object 202522379349301497). Both were extracted from the IRS bulk zips listed in the [IRS 2025 e-file index](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv); ProPublica rendering: [Sch D](https://projects.propublica.org/nonprofits/organizations/474172718/202503179349301975/IRS990ScheduleD).

| Field | Value |
|---|---|
| DAF accounts held (Sch D Part I col. a) | **1,421,011** [F] |
| Contributions to DAFs | **$12,300,836** [F] |
| Grants from DAFs | **$12,417,069** [F] |
| DAF value at year end | **$1,949,239** [F] |
| Total revenue / expenses | $13,144,583 / $12,679,753 [F] |
| Grants paid (Part I) | $11,091,205 [F] |
| Employees | **0** [F] |
| "Cost of service" | $1,123,082 [F] |
| "External bank fraud loss" | **$316,184** [F] |
| "Bank and credit card fees" | $84,552 [F] |
| Amendment reason | "THE 2024 990 RETURN IS BEING AMENDED DUE TO A CHANGE IN FINANCIAL INFORMATION… SCHEDULE D PART I" [F] |
| Self-description | "IN PARTNERSHIP WITH OUR ADMINISTRATIVE PROVIDER GIVINGA, INC. WE HAVE CREATED THE FIRST ZERO FEE STRUCTURE… NO START-UP FEE, NO FEES BASED ON ASSETS UNDER MANAGEMENT" [F] |

Notes on the table:
- **[C]** Average DAF value is $1.37 per account. The fraud loss is about 2.4% of total revenue.
- **[I]** The account count fits a structure where every enrolled employee of a client company holds a near-zero-balance account.
- **[I]** The original return omitted Schedule D values, so the earlier note in [regulation-market-structure-portability.md](regulation-market-structure-portability.md) needs care. DAFRC flags this count "paper submission", but both CY2024 returns are e-filed in the IRS index. The 1.42m figure enters the record only via the November 2025 amendment.
- Any processor-share statistic is highly sensitive to this one amended line (see that file's sensitivity analysis).

**Products and channels** (all first-party or press):
- **Givinga Foundation products:**
  - "Charitable Savings Account™" ("our modern Donor-Advised Fund")
  - "Charitable Foundation Account™"
  - ProjectFS fiscal sponsorship
  - a Nonprofit Portal
  - "Institutional solutions: charitable payment processing, grantmaking tools, and white-label giving accounts"

  [F: [givingafoundation.org](https://www.givingafoundation.org/)]
- **December 2025 corporate suite:** "Universal Sponsored Account (USA)", "Charitable Investment Account (CIA)" and "Charitable Foundation Account (CFA)", aimed at the 2026 deduction rules. The coverage names no clients and makes no AI claims. [F: [fundsforNGOs summary of Givinga release, 2025-12-12](https://news.fundsforngos.org/2025/12/12/givinga-launches-innovative-philanthropy-platform-for-companies-ahead-of-2026-giving-rules/); the original [Business Wire release](https://www.businesswire.com/news/home/20251211023148/en) returned 403]
- **Named corporate clients on givinga.com:** case studies for **Patch My PC** ("$162,000… donated to 116 charities during Giving Season 2023", 75% participation), **Gesmer Updegrove**, **THL Partners** and **Orinda Country Club**. The site also claims "Trusted by Fortune 500s" without naming them. It makes no AI claim and no DAF or white-label wording on the homepage. [F: [givinga.com](https://www.givinga.com/)]
- **Channel partners** (search-engine summaries of press releases; the originals on businesswire.com returned 403, so treat these as secondary):
  - EarthShare's workplace-giving platform runs on Philantech (April 2022). [[Business Wire 2022-04-05](https://www.businesswire.com/news/home/20220405005483/en/earthshare-unveils-modernized-platform-to-help-companies-drive-environmental-impact)]
  - PlanSource benefits-platform integration (August 2021). [[Business Wire 2021-08-12](https://www.businesswire.com/news/home/20210812005102/en)]
  - WeSpire uses Givinga as back-end financial processor (2019). [[CSRwire](https://csrwire.com/press-release/wespire-adds-employee-giving-matching-and-grants-management-to-award-winning-employee-experience-platform/)]
  - Double the Donation matching-gift integration (March 2023). [[Business Wire 2023-03-16](https://www.businesswire.com/news/home/20230316005178/en/Partnership-with-Double-the-Donation-to-Expand-Givinga%E2%80%99s-Philanthropic-Network)]

**Funding (new, from SEC Form D).** Six offerings, 2019-2026 (rows in the entrants CSV):

| First sale | Sold | Investors | Form D |
|---|---:|---:|---|
| 2019-11-15 | $185,000 (debt) | 4 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083019000001/primary_doc.xml) |
| 2020-11-10 | $2,422,149 | 17 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083020000002/primary_doc.xml) |
| 2021-07-07 | $267,500 | 5 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083021000002/primary_doc.xml) |
| 2021-10-14 | $3,777,625 | 11 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083021000003/primary_doc.xml) |
| 2022-10-27 | $4,999,999 | 11 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083022000001/primary_doc.xml) |
| 2023-09-26 (amended to 2026-09-09) | **$10,766,659** cumulative | 15 | [link](https://www.sec.gov/Archives/edgar/data/1720830/000172083026000001/primary_doc.xml) |

Notes on funding:
- **[C]** Total sold across offerings is **$22.42M**, assuming no overlap between offerings.
- **[I]** The aggregator headline "Givinga secures $6.35M seed" ([Signalbase, 2025-03-06](https://www.trysignalbase.com/news/funding/empowering-change-givinga-secures-635m-seed-round-to-revolutionize-corporate-philanthropy-with-philantech)) matches the 2025-02-25 Form D/A cumulative of **$6,345,366** for the 2023 offering. It is an amendment of an existing offering, not a new seed round.
- Investors are not named in the Form D filings. Signalbase names only Hasatano Capital (unverified).

**Verdict [I].** Givinga runs a "sponsor plus technology company" model, like Groundswell (Groundswell Charitable Foundation) and Benevity (AOGF). It does not look like Ren or Stellar, which license administration to many independent legal sponsors.
- Its "white-label giving accounts" appear to be accounts at Givinga Foundation branded for a client, not accounts at the client's own sponsor.
- No public document shows a community foundation or national sponsor licensing Philantech to hold DAFs under its own EIN.
- Givinga is therefore **concentrated infrastructure for one sponsor that serves many companies**. Its systemic weight comes from the 1.42m account line, not from other sponsors depending on it.
- The client list is incomplete (open question P-INF-02).

### 1.2 DAF Direct: a sponsor-owned trust, operated by Fidelity, with three sponsors

**Legal operator.** "The DAF Direct Website, which is operated by **DAF Direct Trust**". The terms are dated "As of January 27, 2015". "We own the Widget, including all associated intellectual property". The terms are governed by "the laws of The Commonwealth of Massachusetts". [F: [DAF Direct Terms of Use and Service Agreement](https://www.dafdirect.org/popups/userAgreementPopUp.html)]

The privacy policy names only DAF Direct Trust. It states "DAF Direct only shares your information with the participating sponsoring organizations… to facilitate grants recommended by a donor through the Widget". [F: [privacy policy](https://www.dafdirect.org/privacyPolicy.html)]

ProPublica's nonprofit search returns no organization named "DAF Direct". [F: [ProPublica API search](https://projects.propublica.org/nonprofits/api/v2/search.json?q=%22DAF%20Direct%22)] **[I]** The trust is probably not a separately filing exempt entity, or it files under another name. Unverified.

**Evidence that Fidelity operates it** (inferred; none of it is a direct ownership statement):
- **Contact address:** `DAFDirect@fmr.com`. FMR is Fidelity's corporate domain. [F: [dafdirect.org](https://www.dafdirect.org/)]
- **Analytics:** the widget registration page sets `measurementDomain = "metrics.fidelity.com"` and `s_account = "fddafdirectprod"`, and loads `fmrvs.js`. [F: page source of [dafdirect.org/DAFDirect/](https://www.dafdirect.org/DAFDirect/), fetched 2026-11-14]
- **Domain registration:** dafdirect.org was registered 2012-10-05 through **CSC Corporate Domains**, on **Akamai** name servers. That matches fidelitycharitable.org (CSC, Akamai a1-188/a2-65), while dafgiving360.org uses MarkMonitor and schwab.com name servers. [F: [PIR RDAP dafdirect.org](https://rdap.publicinterestregistry.org/rdap/domain/dafdirect.org); [PIR RDAP fidelitycharitable.org](https://rdap.publicinterestregistry.org/rdap/domain/fidelitycharitable.org); [PIR RDAP dafgiving360.org](https://rdap.publicinterestregistry.org/rdap/domain/dafgiving360.org)] RDAP shows no registrant organization (redacted).
- **Origin:** a "collaboration between donor-advised fund sponsors and nonprofit organizations, **led by Fidelity Charitable**". At launch it was connected to Fidelity Charitable and Schwab Charitable (2013-04-09). [F: [Fidelity Charitable release](https://fidelitycharitable.org/about-us/news/daf-direct-brings-new-giving-option-to-nonprofits.html)]

**Connected sponsors (2026).** "DAF Direct currently facilitates grant recommendations from donors of **Fidelity Charitable®, DAFgiving360®, and the BNY Mellon Charitable Gift Fund®**. More national and community foundation DAF sponsoring organizations may be added in the future." [F: [About DAF Direct](https://www.dafdirect.org/about-daf-direct/index.html)] The BNY link resolves to a live "BNY Charitable" site with donor login. [F: [bnycharitable.org/bny/](https://bnycharitable.org/bny/)] This answers the open question in [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §7: BNY is still active, under the "BNY Charitable" brand.

**Routing.**
- The widget or link lets a donor "initiate grant recommendations from their donor-advised fund… directly from your website". [F: [About](https://www.dafdirect.org/about-daf-direct/index.html)]
- "The DAF has sole authority to approve any such grant recommendation, and… may decline… or may alter the amount, purpose, or other terms." [F: [Terms §4](https://www.dafdirect.org/popups/userAgreementPopUp.html)]
- "After a DAF grant recommendation has been approved, 100% of the funds transfer to the recommended nonprofit, with no administration or transaction fees." [F: [About](https://www.dafdirect.org/about-daf-direct/index.html)]
- **[I]** The payment therefore uses the sponsor's own rail: Fidelity Stripe/ACH/check, or the DAFgiving360 and BNY methods, which are unverified.
- **[I]** DAF Direct is a recommendation-initiation layer, unlike Chariot, whose DAFpay Network can route funds.

**Adoption.** The only figure is 1,251 charities in 2015 ([Chronicle of Philanthropy, 2015](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/); already in the repo). The 2026 site lists 5 example users. No current count was found.

---

## 2. Q-B12: What do nonprofits pay to receive DAF grants?

### 2.1 Published fees by rail (all [F])

| Rail | Fee to nonprofit | Payout timing | Source |
|---|---|---|---|
| Fidelity Charitable EFT (Stripe or ACH) | "incur no cost or fee for your organization" | 1-2 days; Stripe notice weekly, ACH notice daily | [Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html) |
| Fidelity Charitable check | $0 from the sponsor. "Cannot reissue a grant check unless requested by the recommending donor." EFT "not currently require[d]" | Not stated. Fidelity says EFT is "up to 9x faster" | [Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html) |
| PayPal Grant Payments (Vanguard Charitable, NPT) | "There are currently no fees associated with receiving grants via PayPal." Standard withdrawal to bank is free; Instant Transfer costs 1.50% (min $0.50) | Funds available within one day of acceptance; grants expire | [PayPal help 883](https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883); [PayPal fees, updated 2026-11-04](https://www.paypal.com/us/business/paypal-business-fees); [Vanguard nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations) |
| Chariot DAFpay (default) | "2.9% (rounded to the nearest whole dollar)". Fundraising Platform agreements take precedence, and subscriptions can include volume "with no DAFpay Fees". Unpaid fees accrue 0.5%/month | Paid by the DAF provider by ACH or check; "only the DAF Provider… can guarantee your receipt" | [Chariot Nonprofit ToS §4.4, updated 2026-10-14](https://www.givechariot.com/legal-nonprofit) |
| Chariot Disbursements (receiving) | "at no cost" after claiming a free account; a Chariot Deposit Account is required; linking more payers needs Growth or Enterprise | Electronic; falls back to check | [Chariot, 2026-05-07](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors); [Chariot pricing](https://www.givechariot.com/pricing) |
| Chariot plans | Core 1% per donation; Growth $4,740/yr with 250 donations; Enterprise custom (an earlier capture; the live page now says "Talk to us") | — | [repo: challenger-economics](../challenger-economics-daffy-chariot-charityvest-2026-11-12.md); [Chariot pricing](https://www.givechariot.com/pricing) |
| DAF Direct | "no administration or transaction fees" | Sponsor's rail | [About DAF Direct](https://www.dafdirect.org/about-daf-direct/index.html) |
| Every.org | No platform fee. DAF and bank ACH listed as free. Card 2.2% + $0.30 (+1% non-US); Amex 3.5%; PayPal/Venmo 1.99% (+ $0.49 on the third-party fee page); crypto 1%. Disbursement via Stripe Connect or PayPal is free; via For Good 1.50% | Stripe Connect weekly | [Every.org blog, 2026-07-08](https://blog.every.org/how-does-every-org-work-your-top-10-pricing-questions-answered/); [every.org/pricing](https://every.org/pricing) (the live page returned 403/429, so values come from a search-index capture) |
| PayPal Giving Fund | "Without charging individual donors or charities for our services" | Enrolled: 15-45 days after donation, at month end. Unenrolled: check within about 45 days, after up to 90 days of enrollment attempts | [PPGF about](https://www.paypal.com/us/webapps/mpp/givingfund/about); [PayPal help 969](https://www.paypal.com/us/cshelp/article/how-does-paypal-giving-fund-grant-donations-to-charities-help969) |
| Stripe (benchmark, non-DAF) | Card 2.9% + $0.30; ACH Direct Debit 0.8% capped at $5; standard payouts free | — | [Stripe pricing](https://stripe.com/pricing) |
| PayPal charity rate (benchmark) | 1.99% + $0.49 (pre-approval required) | — | [PayPal fees](https://www.paypal.com/us/business/paypal-business-fees) |
| Bank lockbox | About $0.35-$0.65 per item plus $105-$125/month (BancFirst, Sunwest, First Horizon list prices) | — | Search-engine summaries of the banks' PDFs; the PDFs were not opened ([BancFirst](https://www.bancfirst.bank/BancFirst/media/Documents/NewDisclosureDocs/Lockbox.pdf), [Sunwest](https://www.sunwestbank.com/wp-content/uploads/2021/02/sunwest-fee-lockbox.pdf), [First Horizon](https://www.FirstTennessee.com/-/media/Files/Low-Volume-Lockbox-Matrix.pdf), which timed out) |
| Any check, generic | AFP 2022 median cost to receive a check is $1-$2; ACH is $0.26-$0.50 | — | [Flywire summary of the AFP 2022 survey](https://www.flywire.com/resources/3-must-see-receivables-stats-from-afps-2022-payments-cost-benchmarking-survey) |
| DAFgiving360 | **Unknown.** Nonprofit rail and fees were not verified | — | — |

### 2.2 Staff-time and attribution evidence (thin)

- **No survey measures minutes per DAF grant.**
  - The 2020 Lilly School study, funded by Schwab Charitable, reports that 60% of nonprofits had "some level of concern about their ability to communicate with donors who give through a DAF". [[IU news release, 2020-10-07](https://philanthropy.indianapolis.iu.edu/news-events/news/_news/2020/70-of-nonprofits-receive-grants-from-donor-advised-funds-but-gaps-in-understanding-of-popular-charitable-giving-method-remain-new-study-finds.html)]
  - A search summary attributes to the same study a finding that 24% of DAF recipients cited administrative burden. I did not find that on the fetched page.
- **Vendor time claims:**
  - Chariot says gift processing takes "millions of hours" across the sector. [[Chariot, 2026-01-28](https://www.givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits)]
  - In a No Kid Hungry case, three staff were reduced to "one person 30 minutes, twice a month", with about 25 hours per month gained and 75% of gifts auto-coded. [[Chariot customer story](https://givechariot.com/resources/customer-stories/how-no-kid-hungry-turned-gift-processing-into-a-strategic-superpower)]
  - Both are vendor anecdotes.
- **Rail delays:**
  - Chariot analysed one nonprofit's more than 2,000 DAFpay gifts from 34 providers. ACH-paying providers delivered in 1-2 days, while the **18 check-paying providers averaged 7-162 days**. Chariot also wrote that "even the largest national DAFs have struggled to get their ACH rates much higher than 50%". [[Chariot "All Checks, No Balance", Jan 2026](https://www.givechariot.com/post/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits)]
  - Chariot separately says Fidelity made about 3M grants in 2025, about **67% electronic** and 33% (about 1M) by check. [[Chariot, 2026-05-07](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors)] That is secondary and unconfirmed by Fidelity.
- **Fraud:** Fidelity cites "1 in 5 organizations reporting mail fraud". [[Fidelity FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)] No per-check loss rate was found.

### 2.3 Cost per $1,000 grant (base case; full low/base/high in the CSV)

The model is: Total = published fee + staff minutes × loaded hourly cost + $1,000 × 4% × (excess float days ÷ 365).

Assumptions:
- **[A]** Loaded staff cost is $35/hr in the base case, $25 low and $50 high. For reference, the BLS ECEC average total compensation for private industry is $46.89/hr (June 2026). [[BLS ECEC](https://www.bls.gov/news.release/ecec.nr0.htm)]
- **[A]** The 4% cost of float is an assumption.
- **[A]** All staff minutes are assumptions.

| Rail | Fee | Staff (min) | Float (days) | **Total, base** | Range |
|---|---:|---:|---:|---:|---|
| Fidelity ACH | $0.00 | 3 | 0 | **$1.75** | $0.83-$5.00 |
| Fidelity Stripe | $0.00 | 3 | 2 | **$1.97** | $0.83-$5.55 |
| PayPal Grant Payments (Vanguard/NPT) | $0.00 | 4 | 1 | **$2.44** | $0.83-$22.00 (high case uses Instant Transfer) |
| Chariot Disbursements (receive) | $0.00 | 2 | 0 | **$1.17** | $0.42-$4.39 |
| DAF Direct (on sponsor EFT) | $0.00 | 3 | 0 | **$1.75** | $0.83-$14.91 (high case if paid by check) |
| Every.org DAF donation, Stripe/PayPal payout | $0.00 | 2 | 4 | **$1.61** | $0.42-$4.94 |
| Every.org via For Good | $15.00 | 2 | 10 | **$17.27** | $15.42-$22.46 |
| PayPal Giving Fund, enrolled | $0.00 | 2 | 30 | **$4.46** | $2.06-$9.10 |
| PayPal Giving Fund, unenrolled (check) | $0.25 | 10 | 60 | **$12.66** | $7.01-$27.53 |
| Paper check, in-house (bottom-up) | $0.25 | 10 | 20 | **$8.27** | $2.63-$24.25 |
| Paper check via lockbox | $1.08 | 4 | 18 | **$5.38** | $2.04-$14.30 |
| Paper check, AFP all-in benchmark | $1.50 | — | — | **$1.50** | $1.00-$2.00 (floor; no DAF matching) |
| **Chariot DAFpay default 2.9%** | **$29.00** | 3 | 10 | **$31.85** | $29.42-$43.91 |
| Chariot Core 1% | $10.00 | 2 | 10 | **$12.27** | $10.42-$20.75 |
| Chariot Growth (at 250 gifts/yr) | $18.96 | 2 | 10 | **$21.23** | $19.38-$29.71 |
| Benchmark: card via Stripe | $29.30 | 2 | 2 | **$30.69** | — |
| Benchmark: card via PayPal charity rate | $20.39 | 2 | 1 | **$21.67** | — |
| Benchmark: card via Every.org | $22.30 | 2 | 4 | **$23.91** | — |
| Benchmark: ACH via Stripe | $5.00 | 2 | 4 | **$6.61** | — |

**Findings [C/I]:**
1. **Sponsor-paid electronic rails cost the nonprofit essentially nothing in fees.** That covers Fidelity, PayPal Grant Payments, Chariot Disbursements and PayPal Giving Fund. The sponsor or processor absorbs the cost, so the nonprofit's cost is **reconciliation labour**, which nobody has measured.
2. **Checks cost about 3-5× an electronic grant** in the base case. Float and handling dominate. The tail (60+ days, void and reissue) is where the cost sits, and the AFP $1-$2 figure understates DAF checks because it excludes grant-letter matching.
3. **DAFpay at default terms is priced like card processing:** $29 per $1,000, versus Stripe's $29.30. Yet the money still arrives on the sponsor's rail. **[I]** What the nonprofit buys is donor-intent capture and attribution, not payment, so DAFpay's fee is a fee for data and conversion. This matters for nonprofit bargaining power. Whether nonprofits actually pay 2.9% depends on platform agreements and subscriptions (open question P-INF-05).
4. **DAF Direct is the free, sponsor-run alternative** for intent capture, but it covers only three sponsors.

---

## 3. Q-N09: Funding and AI evidence for emerging entrants

AI classes, as in [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md) §5:
- **A** = announced only.
- **D** = demonstrated (public demo, or a vendor-published named customer case).
- **E** = deployed with independent evidence.
- **U** = unverified marketing.
- **—** = no AI claim found.

| Entity | Latest sourced funding | Investors | Scale claim (type) | AI claim → class |
|---|---|---|---|---|
| **Givinga** | Form D cumulative $10.77M (2023 offering, amended 2026-09-09); $22.42M across 6 offerings [C] ([SEC](https://www.sec.gov/Archives/edgar/data/1720830/000172083026000001/primary_doc.xml)) | Not disclosed | 1.42m accounts, $12.4M granted CY2024 (990) | None → **—** ([givinga.com](https://www.givinga.com/)) |
| **Endaoment** | $6.67M combined (donations plus investment), 2022-06-16 ([Endaoment blog](https://blog.endaoment.org/blog/announcing-endaoments-6-67m-capital)); $2.5M in 2021 ([Decrypt](https://decrypt.co/72524/on-chain-charity-endaoment-lands-2-5m-investment-led-framework-ventures)) | Shine Capital (lead), Coinbase Ventures, Coinbase Giving, Circle Ventures, Framework, Quiet, Hypersphere, Higher Ground Labs, angels | FY6/2025: 1,213 accounts, $18.9M ([990 Sch D](https://projects.propublica.org/nonprofits/organizations/844661797/202631359349315978/IRS990ScheduleD)) | None → **—** ([endaoment.org](https://endaoment.org/)) |
| **Goodstack** (ex-Percent) | $28M Series A, 2024-11-18 ([tech.eu](https://tech.eu/2024/11/18/goodstack-secures-28m-from-general-catalyst/)) | General Catalyst (lead), Morpheus, Repeat | Over $3bn facilitated expected in 2024; 215+ countries (company) | "AI-powered automation", "AI-powered reviews" in grants → **U** ([goodstack.io](https://goodstack.io/)) |
| **Every.org** | Philanthropic support, amounts not disclosed ([help page](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded)) | Camp.org, Fidelity Charitable Catalyst Fund, Gates Foundation | CY2024 990-PF: $50.46M received, $44.93M granted, $9.66M assets (IRS XML) | No product claim. Thought leadership only ([Candid blog](https://candid.org/blogs/ai-powered-relational-fundraising-engaging-everyday-donors/)) → **—** |
| **Groundswell** | Form D $13.21M sold, first sale 2021-11-23, 39 investors ([SEC](https://www.sec.gov/Archives/edgar/data/1899820/000189982021000001/primary_doc.xml)); press says $15M seed | GV (lead), Human Ventures, Felicis, Moonshots, Core Innovation ([Business Wire](https://www.businesswire.com/news/home/20211130005365/en/Groundswell-Announces-A-Total-of-15M-in-Seed-Funding-To-Democratize-Philanthropy)) | Groundswell Charitable Foundation CY2024: 12,808 accounts; $11.75M in; $4.46M out; 26,000+ grants to about 4,850 recipients (IRS XML) | "AI-powered application scoring" → **U** ([groundswell.io](https://www.groundswell.io/)) |
| **Instrumentl** | $55M growth, 2025-04-23 ([Summit Partners](https://www.summitpartners.com/news/instrumentl-raises-55m-from-summit-partners-to-accelerate-their-ai-grant-fundraising-platform)) | Summit Partners (minority) | 4,500+ customers (Apr 2025); 5,500+ (Nov 2026); "$1.1B+ grants managed" | AI matching, AI drafting, Match Insights, none labelled live or beta → **U** ([instrumentl.com](https://www.instrumentl.com/)) |
| **Grantable** | **No verified equity round.** Aggregators list $20k-$80k ([FundedIQ](https://fundediq.co/grantable-grantable-co-funding/)). A VIPC grant was reported, amount unverified | — | 30,000+ orgs; $0/$50/$150 per month plus $300 Agency Hub | Agent-style "desks"; only Agency Hub is labelled "Available now" → **U** ([grantable.co](https://www.grantable.co/)) |
| **Givefront** | $2M seed, 2025-12-18 ([TechCrunch](https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/)) | Script Capital (lead), YC, C3, Phoenix Fund, angels incl. the Chariot and Wealthfront CEOs | "Hundreds" of orgs; target 5,000 by mid-2026 | AI expense matching and fraud detection on the website; TechCrunch makes no AI claim → **U**; no DAF |
| **GivingIQ** | None found | — | "Thousands of organizations" | None → **—** ([press](https://givingiq.com/press/announce)) |
| **Chariot** (reference) | Form D $11.0M, first sale 2024-04-19, 59 investors ([SEC](https://www.sec.gov/Archives/edgar/data/2021660/000202166024000001/primary_doc.xml)) | Maveron (lead, per company) | DAFpay on 100,000+ forms; 1,200+ DAFs reconciled (company) | LLM donation coding; 75% auto-coded at No Kid Hungry → **D** (vendor-published case) |
| **Dataro** | $14.28M Series A, 2026-02-17 ([Pulse 2.0](https://pulse2.com/dataro-14-28-million-series-a-raised-for-ai-fundraising-platform/)) | Blueprint Equity (lead), Save the Children, Basis Set | 300+ orgs | Predictive donor models → **U** |
| **Avid** | $6.5M seed, 2025-10-16 ([Newswire](https://www.newswire.com/news/avid-secures-6-5m-seed-round-to-rebuild-fundraising-for-the-modern-22659220)) | Silverton Partners | Unnamed customers | AI campaign drafting with staff review → **U** |
| **Fundraise Up** "Agentic Giving" | Not in source | — | — | Category defined, no products or dates (2026-08-02) → **A** ([Pulse 2.0](https://pulse2.com/fundraise-up-introduces-agentic-giving-category-for-ai-powered-donations/)) |
| **Circle Foundation** (not a startup) | Funded with 1% of Circle IPO shares | — | DAF at Fidelity Charitable, possibly over $100M | Intake, chief-of-staff and operating agents in use → **E** (journalist report, no outcome data) ([Chronicle, 2026-11-06](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/)) |
| **Sage Future / AI Village** | Backed by Open Philanthropy | — | Agents raised $257 | **D** ([TechCrunch, 2025-04-08](https://techcrunch.com/2025/04/08/a-nonprofit-is-using-ai-agents-to-raise-money-for-charity)) |

**Excluded:** "GradRoots" (an "agentic operating core for philanthropy") appears only on a manus.space page, with no entity, funding or product evidence.

**Findings [I]:**
- **Venture capital in this adjacency goes to grant-seeker SaaS, corporate giving and payment rails, not to DAF sponsors.** Instrumentl ($55M), Goodstack ($28M), Dataro ($14.3M), Chariot ($11M) and Avid ($6.5M) raised the most recent rounds. The sponsors are nonprofits funded by philanthropy or by blended donations plus equity (Endaoment, Every.org), or sit beside a venture-backed technology company (Givinga, Groundswell).
- **"Agentic philanthropy" sits mostly at the announced or unverified stage.** The one E-class case is a grantmaker's internal desk work at a foundation whose DAF is at Fidelity Charitable. The DAF sponsor itself is not the agent.
- That agrees with the repo thesis that AI value sits in donor- and grantmaker-side workflow and exception handling, not in sponsor approval.

---

## 4. Corrections and updates to repo claims

1. **Givinga's 1.42m accounts** come from an e-filed **amended** return (2025-11-13), not a paper filing. The original e-file had no Schedule D values. Update [regulation-market-structure-portability.md](regulation-market-structure-portability.md) to note this.
2. **"Givinga $6.35M seed (2025)"** is a cumulative Form D/A for a 2023 offering. Do not record it as a new round.
3. **BNY Mellon Charitable** is still active, as "BNY Charitable", and is still listed on DAF Direct.
4. **DAF Direct's legal operator is "DAF Direct Trust".** The Fidelity link is now supported by technical evidence beyond the fmr.com address.
5. **Every.org filed Form 990-PF** for 2021-2024. The IRS BMF now shows public-charity code 15, with ruling 2025-10-01.
6. **Instrumentl's customer count** was 4,500+ in April 2025 and is 5,500+ on its site in November 2026.

## 5. Open questions (proposed to the queue as P-INF-01..09)

- What counts as a Givinga "account", and why was the CY2024 return amended?
- Which companies' employee programs sit at Givinga Foundation?
- What is the governance of DAF Direct Trust, and how many charities use DAF Direct in 2026?
- How many minutes per grant does each rail take? This needs a time-and-motion study.
- What DAFpay fee do nonprofits actually realize?
- What payment rail does DAFgiving360 use to pay nonprofits?
- What explains Every.org's 990-PF history?
- What do live agentic products show in practice?
- Processor fraud-loss lines, such as Givinga's $316k "external bank fraud loss".

---

## 6. Data dictionary

### nonprofit-receipt-cost-by-rail.csv (one row per rail; all money in USD per $1,000 grant)

| Column | Meaning |
|---|---|
| rail_id | R01-R19 |
| rail / sponsors_or_examples | Rail name and the sponsors or platforms that use it |
| fee_low/base/high_usd | Published fee per $1,000 (assumption where flagged in fee_status) |
| fee_basis, fee_source, fee_status | Quote or derivation, URL, and whether it is sourced or assumed |
| staff_minutes_low/base/high | **[A]** Nonprofit staff minutes to receive, match and acknowledge one grant |
| staff_cost_*_usd | Minutes × $25 / $35 / $50 per hour **[A]** |
| float_days_* | **[A]** Excess days in transit versus the fastest electronic rail |
| float_cost_*_usd | $1,000 × 4% × days ÷ 365 **[A]** |
| total_*_usd | fee + staff_cost + float_cost (low with low, base with base, high with high) |
| float_basis, timing_source | Basis and source for the timing |
| notes | Caveats |

### emerging-entrants-funding-ai.csv (one row per funding event or AI evidence item)

| Column | Meaning |
|---|---|
| entity, segment, daf_role | Who it is and how it relates to DAFs |
| event_date, event_type | Date of first sale or announcement, and the round type |
| amount_usd, amount_status | Amount, and its basis: `sec_form_d_sold` (or `sec_form_d_sold_cumulative`), `company_announced`, `press_secondary`, `not_found`, `not_disclosed` |
| investors_or_funders | As named in the source |
| funding_source_url, funding_source_type | Source URL and type |
| scale_claim, scale_claim_type, scale_source_url | `company_claim`, `sponsor_990`, `irs_990pf_xml` or `press` |
| ai_claim, ai_class, ai_source_url | AI claim and class: A / D / E / U / — (defined in §3) |
| notes | Caveats |

---

## 7. Source register

| ID | Source | Used for |
|---|---|---|
| S1 | SEC EDGAR Form D, Givinga Inc. (CIK 1720830): [2019](https://www.sec.gov/Archives/edgar/data/1720830/000172083019000001/primary_doc.xml), [2020](https://www.sec.gov/Archives/edgar/data/1720830/000172083020000002/primary_doc.xml), [2021a](https://www.sec.gov/Archives/edgar/data/1720830/000172083021000002/primary_doc.xml), [2021b](https://www.sec.gov/Archives/edgar/data/1720830/000172083021000003/primary_doc.xml), [2022](https://www.sec.gov/Archives/edgar/data/1720830/000172083022000001/primary_doc.xml), [2025 D/A](https://www.sec.gov/Archives/edgar/data/1720830/000172083025000001/primary_doc.xml), [2026 D/A](https://www.sec.gov/Archives/edgar/data/1720830/000172083026000001/primary_doc.xml) | Givinga funding |
| S2 | SEC Form D, [Groundswell Giving Inc. 2021](https://www.sec.gov/Archives/edgar/data/1899820/000189982021000001/primary_doc.xml); [Chariot Giving Inc. 2024](https://www.sec.gov/Archives/edgar/data/2021660/000202166024000001/primary_doc.xml) | Funding |
| S3 | [IRS e-file index 2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv) and [2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv); XML from `2025_TEOS_XML_09A/11A/10A.zip` and `2026_TEOS_XML_02A.zip` (objects 202522379349301497, 202503179349301975, 202502749349100700, 202640289349301029) | Givinga Foundation, Every.org, Groundswell CF 990 data |
| S4 | [ProPublica Givinga Foundation Sch D](https://projects.propublica.org/nonprofits/organizations/474172718/202503179349301975/IRS990ScheduleD); [ProPublica API 474172718](https://projects.propublica.org/nonprofits/api/v2/organizations/474172718.json); [API 611913297](https://projects.propublica.org/nonprofits/api/v2/organizations/611913297.json) | Entity metadata |
| S5 | [givinga.com](https://www.givinga.com/); [givingafoundation.org](https://www.givingafoundation.org/); [fundsforNGOs, 2025-12-12](https://news.fundsforngos.org/2025/12/12/givinga-launches-innovative-philanthropy-platform-for-companies-ahead-of-2026-giving-rules/) | Givinga products and clients |
| S6 | Givinga partner releases (search summaries only): [EarthShare](https://www.businesswire.com/news/home/20220405005483/en/earthshare-unveils-modernized-platform-to-help-companies-drive-environmental-impact), [PlanSource](https://www.businesswire.com/news/home/20210812005102/en), [WeSpire](https://csrwire.com/press-release/wespire-adds-employee-giving-matching-and-grants-management-to-award-winning-employee-experience-platform/), [Double the Donation](https://www.businesswire.com/news/home/20230316005178/en/Partnership-with-Double-the-Donation-to-Expand-Givinga%E2%80%99s-Philanthropic-Network); [Signalbase](https://www.trysignalbase.com/news/funding/empowering-change-givinga-secures-635m-seed-round-to-revolutionize-corporate-philanthropy-with-philantech) | Channels; seed headline |
| S7 | [dafdirect.org](https://www.dafdirect.org/); [About](https://www.dafdirect.org/about-daf-direct/index.html); [Terms](https://www.dafdirect.org/popups/userAgreementPopUp.html); [Privacy](https://www.dafdirect.org/privacyPolicy.html); [widget page](https://www.dafdirect.org/DAFDirect/) | DAF Direct |
| S8 | RDAP: [dafdirect.org](https://rdap.publicinterestregistry.org/rdap/domain/dafdirect.org), [fidelitycharitable.org](https://rdap.publicinterestregistry.org/rdap/domain/fidelitycharitable.org), [dafgiving360.org](https://rdap.publicinterestregistry.org/rdap/domain/dafgiving360.org); [Google DNS CNAME](https://dns.google/resolve?name=www.dafdirect.org&type=CNAME) | Operator inference |
| S9 | [Fidelity Charitable DAF Direct release, 2013](https://fidelitycharitable.org/about-us/news/daf-direct-brings-new-giving-option-to-nonprofits.html); [BNY Charitable](https://bnycharitable.org/bny/); [Chronicle 2015](https://www.philanthropy.com/news/effort-to-spur-giving-from-donor-advised-funds-online-appears-to-stall/) | DAF Direct history and sponsors |
| S10 | [Fidelity nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html); [Vanguard nonprofits](https://www.vanguardcharitable.org/nonprofit-organizations) | Sponsor rails |
| S11 | [PayPal Grant Payments help](https://www.paypal.com/us/cshelp/article/what-are-grant-payments-help883); [PPGF help](https://www.paypal.com/us/cshelp/article/how-does-paypal-giving-fund-grant-donations-to-charities-help969); [PPGF about](https://www.paypal.com/us/webapps/mpp/givingfund/about); [PayPal fees](https://www.paypal.com/us/business/paypal-business-fees) | PayPal rails |
| S12 | [Chariot Nonprofit ToS](https://www.givechariot.com/legal-nonprofit); [Chariot pricing](https://www.givechariot.com/pricing); [e-pay article](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors); ["All Checks, No Balance"](https://www.givechariot.com/post/all-checks-no-balance-a-report-on-the-state-of-check-payments-to-nonprofits); [Gift Processing launch](https://www.givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits); [No Kid Hungry story](https://givechariot.com/resources/customer-stories/how-no-kid-hungry-turned-gift-processing-into-a-strategic-superpower); [DAF gift processing article](https://givechariot.com/resources/insights/how-daf-gift-processing-sinks-nonprofit-efficiency.md) | Chariot fees, timing, time claims |
| S13 | [Every.org pricing blog](https://blog.every.org/how-does-every-org-work-your-top-10-pricing-questions-answered/); [every.org/pricing](https://every.org/pricing); [funding help page](https://support.every.org/hc/en-us/articles/360058165794-How-is-Every-org-funded) | Every.org |
| S14 | [Stripe pricing](https://stripe.com/pricing) | Benchmarks |
| S15 | [Flywire on AFP 2022](https://www.flywire.com/resources/3-must-see-receivables-stats-from-afps-2022-payments-cost-benchmarking-survey); lockbox PDFs ([BancFirst](https://www.bancfirst.bank/BancFirst/media/Documents/NewDisclosureDocs/Lockbox.pdf), [Sunwest](https://www.sunwestbank.com/wp-content/uploads/2021/02/sunwest-fee-lockbox.pdf), [First Horizon](https://www.FirstTennessee.com/-/media/Files/Low-Volume-Lockbox-Matrix.pdf)), values via search summary | Check costs |
| S16 | [BLS ECEC, June 2026](https://www.bls.gov/news.release/ecec.nr0.htm); [IU Lilly 2020](https://philanthropy.indianapolis.iu.edu/news-events/news/_news/2020/70-of-nonprofits-receive-grants-from-donor-advised-funds-but-gaps-in-understanding-of-popular-charitable-giving-method-remain-new-study-finds.html) | Labour anchor; survey |
| S17 | [Endaoment blog 2022](https://blog.endaoment.org/blog/announcing-endaoments-6-67m-capital); [Decrypt 2021](https://decrypt.co/72524/on-chain-charity-endaoment-lands-2-5m-investment-led-framework-ventures); [endaoment.org](https://endaoment.org/) | Endaoment |
| S18 | [tech.eu Goodstack](https://tech.eu/2024/11/18/goodstack-secures-28m-from-general-catalyst/); [goodstack.io](https://goodstack.io/) | Goodstack |
| S19 | [Summit Partners Instrumentl](https://www.summitpartners.com/news/instrumentl-raises-55m-from-summit-partners-to-accelerate-their-ai-grant-fundraising-platform); [instrumentl.com](https://www.instrumentl.com/); [grantable.co](https://www.grantable.co/); [FundedIQ Grantable](https://fundediq.co/grantable-grantable-co-funding/) | Grant SaaS |
| S20 | [TechCrunch Givefront](https://techcrunch.com/2025/12/18/these-21-year-old-dropouts-raised-2m-to-build-givefront-a-fintech-for-nonprofits/); [GivingIQ press](https://givingiq.com/press/announce); [groundswell.io](https://www.groundswell.io/); [Business Wire Groundswell 2021](https://www.businesswire.com/news/home/20211130005365/en/Groundswell-Announces-A-Total-of-15M-in-Seed-Funding-To-Democratize-Philanthropy) | Entrants |
| S21 | [Pulse 2.0 Dataro](https://pulse2.com/dataro-14-28-million-series-a-raised-for-ai-fundraising-platform/); [Newswire Avid](https://www.newswire.com/news/avid-secures-6-5m-seed-round-to-rebuild-fundraising-for-the-modern-22659220); [Pulse 2.0 Fundraise Up](https://pulse2.com/fundraise-up-introduces-agentic-giving-category-for-ai-powered-donations/); [Chronicle Circle Foundation](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/); [TechCrunch Sage](https://techcrunch.com/2025/04/08/a-nonprofit-is-using-ai-agents-to-raise-money-for-charity); [Candid blog](https://candid.org/blogs/ai-powered-relational-fundraising-engaging-everyday-donors/) | AI and agentic |

**Method notes:**
- SEC Form D values were parsed from `primary_doc.xml` (totalAmountSold, dateOfFirstSale, totalNumberAlreadyInvested).
- IRS XML was extracted with HTTP range reads of the IRS bulk zips, because ProPublica's XML download returned a security check.
- Several first-party pages returned 403 or 429 (businesswire.com, every.org/pricing). Those claims are marked as coming from search-index captures.
