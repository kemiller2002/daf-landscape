# Adviser fees on DAF accounts with no published cap (P-ACC-03); DAFgiving360 pools after September 2026 (P-ACC-02); NPact ownership (P-LDG-01); DAFgiving360 grant payment rail (P-NPT-05)

**Date:** 2026-11-15 · **Queue items:** P-ACC-03, P-ACC-02, P-LDG-01, P-NPT-05 (`data/mission-2026-11-14/research-priority-queue.csv`)

**Outputs:**
- [`data/mission-2026-11-14/adviser-fees-observed-2026.csv`](../../data/mission-2026-11-14/adviser-fees-observed-2026.csv): 16 rows. These are program rules, RIA brochures, one firm program document and Form 990 proxies.
- [`data/mission-2026-11-14/queue-proposals-adviser-fees.csv`](../../data/mission-2026-11-14/queue-proposals-adviser-fees.csv): P-ADV-01 to P-ADV-05.

**Method and rules.**
- I used public pages, PDFs, SEC EDGAR (public full-text search and archive) and the repo's 990 extracts only.
- I logged in nowhere, submitted no forms, created no accounts and contacted no one. I made no authenticated API calls.
- Recency: every fee input is from 2023 to 2026. The one pre-2021 brochure found (ACM 2020) is not used.
- Labels: **[F]** first-party document; **[R]** search-index capture of a page I could not open; **[3P]** third-party data site; **[I]** my inference.

**Read first and built on:**
- `queue-all-in-cost-dafpay-access.md` and `queue-ledgers-behind-portals.md`, with the wave-10 corrections (V10-02 on NPact's entity form; V10-05 on the MS GIFT cap and the weak Edward Jones basis).
- `all-in-cost-comparison-2026.csv` and `sponsor-eft-providers-2026.csv`.

**Access limits this session:**
- dafgiving360.org and schwabcharitable.org return 403 on every path, including robots.txt.
- web.archive.org is unreachable: the proxy drops the tunnel and WebFetch refuses the host.
- broadwestpartners.com does not resolve; it is outside the session's allowed network.
- stockanalysis.com is readable only through WebFetch, because Cloudflare blocks curl.

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-ACC-03: adviser fees where no cap is published** | **No sponsor in scope caps the fee. Fidelity ties it to the firm's own standard schedule. Observed 2025–26 rates run from 0% to 2.00%, and the one sponsor-wide measure (AEF) averages about 0.46%.**<br>- **Fidelity CIAP:** the fee must be no higher than the firm charges similar clients, "and in no event in excess of the standard investment advisory fee schedule" ([agreement ¶19b](https://www.fidelitycharitable.org/docs/CIAP-Investment-Advisor-Agreement.pdf)). Fidelity also requires aggregate fees to be "reasonable" ([guidelines](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf)).<br>- **RIA disclosures:** IEQ charges up to 1% on Fidelity and Schwab DAF assets, waivable. ACM Wealth, a CIAP firm, has a general schedule of up to 1.50% on equity accounts. Winthrop Wealth, which uses AEF, charges 0.30–2.00%. FC Advisory charges 0% on non-discretionary DAFgiving360 assets. Waverly says its DAF fee "may be lower or higher" than its client fee. [F]<br>- **The only DAF-specific fee menu found** is Redhawk's for DAFgiving360: 0/0.25/0.50/0.75% advisory, plus a 0.25% Redhawk admin fee, with admin plus advisory capped at 1.0% [F].<br>- **AEF 990 proxy:** line 11f investment-management fees are 0.40–0.46% of average assets (TY2022–24). Every AEF fund must use an outside adviser, so this is a fair asset-weighted average adviser cost [I]. The RCF ratio (0.23%) is weaker.<br>- **NPT:** adviser-managed (segregated) accounts are available only above $500,000, and "a different fee schedule may apply". No rate is published.<br>- **Vanguard Charitable:** no adviser-managed option. | Medium on rules (first-party). Low to medium on typical rates: seven firm documents and one 990 ratio |
| **P-ACC-02: DAFgiving360 pools** | **Three of the core pools changed underlying fund effective 2026-09-24. All three moves cut or held cost. The Balanced Pool used as the "typical" pool in the all-in table was not among them.**<br>- Large Cap Equity Managed: PRILX 0.588% → FFICX 0.283%. Socially Responsible Balanced: PAXIX 0.669% → CBAIX 0.663%. Short-Term Income: PSHIX 0.407% → BSBIX 0.292%. Fund changes are [R]; expense ratios are [3P].<br>- The Balanced Pool's fund, JBALX, is 0.664% [3P], against the 0.65% in the table: +1.4 bps, which is immaterial.<br>- The Q3 2026 performance report still assumes a 0.60% admin fee [R]. | Medium (fund swaps [R]; expense ratios [3P]) |
| **P-LDG-01: NPact owner** | **BroadWest Partners is confirmed from a deal-party release. Its managing partners Jeff Conn and Brian Greeley bought Fusion Labs on 2020-12-30 and renamed it NPact. The release names no outside investors.**<br>- The CB Insights date (2021-04-28) is the release date, not the close.<br>- The 2022 FIMS/DonorCentral NXT purchase was for about **$6.4m in cash, paid by "Fusion Laboratories, LLC"** ([Blackbaud 10-Q](https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm)). Neither the 10-Q nor NPact's release names outside capital.<br>- **New lead:** [The Cambria Group](https://cambriagroup.com/portfolio?start=192), a search-fund and small-buyout investor, lists NPact among its portfolio companies. NPact's CEO is now Burt Hurlock, not David Rode. Current ownership may therefore include Cambria, or have changed (P-ADV-04). | High on 2020 close and 2022 buyer; low on 2026 owner |
| **P-NPT-05: DAFgiving360 ACH** | **No public evidence of ACH/EFT to charities. Every readable source points to checks with an award letter.**<br>- Chariot's help center says gifts from "Fidelity, Vanguard, and Schwab—will still be delivered the same way as before" ([F, Chariot](https://help.givechariot.com/llms-full.txt)). DAFgiving360 is not among Chariot's named disbursement partners.<br>- A search-index capture of DAFgiving360's grant page says the charity "will receive a grant award letter with a check" [R].<br>- The 2026 Program Policies page (web version dated 2026-08-07 [R]) could not be read. | Medium (absence of evidence; the 2026 policy text is unread) |

---

## 1. P-ACC-03: adviser fees on adviser-managed DAF accounts

### 1.1 What each sponsor's rules allow

| Sponsor / program | Cap? | Rule (quoted, ≤40 words) | Adviser option minimum | Source |
|---|---|---|---|---|
| **Fidelity Charitable CIAP** | No | "the Advisory Fee is charged at a rate no greater than that of other similarly situated clients/ investors of the CIAP Advisor Firm, and in no event in excess of the standard investment advisory fee schedule" | **$100,000** ("meets the program's $100,000 minimum balance requirement"; 2025 overview). The 2026 guidelines say minimums vary by investment option | [Agreement, PDF 2025-01](https://www.fidelitycharitable.org/docs/CIAP-Investment-Advisor-Agreement.pdf); [overview, PDF 2025-04](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf) [F] |
| | | "Fidelity Charitable requires that aggregate fees be reasonable". Fees "cannot be assessed on Giving Account assets in the Fidelity Charitable investment pools" | | [Guidelines, PDF 2026-07](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf) [F] |
| | | The application takes the fee in basis points: none, flat, blended or flat-by-band | | [Application, PDF 2026-07](https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/ciap-donor-application-form.pdf) [F] |
| **AEF** | No | "Professional investment management fees, commissions, transaction expenses, etc. are charged directly to the relevant funds." | An adviser is mandatory on every fund ("The donor must recommend a financial professional") | [2023 Program Description](https://air-original.imgix.net/678d90a0-ec95-45e2-9126-674089482adb.pdf?ixlib=react-9.5.4) [F] |
| **NPT** | No | "DAF accounts over $500,000 may recommend a financial advisor to propose a custom investment portfolio. A different fee schedule may apply." | **$500,000** (segregated account) | [NPT Guide 2024-09](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) [F] |
| | | NPT's FAQ lists "a fee to financial advisors for some DAF accounts" among other fees, apparently pooled accounts too | | [NPT FAQ](https://www.nptrust.org/donor-advised-funds/faq/) [R, search summary] |
| **RCF** (advisor-managed; private-label circulars) | No | Each DAF "may carry its own fees and underlying expenses". No adviser rate appears in the UBS (2024), Ameriprise (2025) or RBC (2025) circulars | Advisor-managed is the default channel | [UBS circular](https://www.reninc.com/wp-content/uploads/2025/08/UBS-Program-Circular-2.pdf); [RBC](https://rbcrcf.donorfirstx.com/pdf/RBC/Program%20Circular.pdf); [Ameriprise](https://ampf.donorfirstx.com/pdf/AMPF/RCF%20Program%20Circular%20for%20Ameriprise%20Clients.pdf) [F] |
| **Vanguard Charitable** | n/a | "Vanguard Charitable does not itself charge investment fees". The adviser role is an "interested party" with access only. 990 line 11f is $0 | None | [Policies & Guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) [F] |
| *(for comparison)* **DAFgiving360** | 1% (published) | A 2025 firm document stacks fees as "Advisory fee: 0.00%, 0.25%, 0.50%, or 0.75%" and "The Redhawk administration fee plus the advisory fee cannot exceed 1.0%." | $100,000 | [Redhawk 2025-05-21](https://advisor.redhawkwa.com/wp-content/uploads/2025/05/DAFgiving360-Process-05212025.pdf) [F, firm] |

**New finding on Fidelity CIAP admin fees.** CIAP assets held at an "Other Custodian" pay a **70 bps** first tier (70/30/20/15) instead of 60 bps ([guidelines](https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf)). The all-in table uses the 60 bps schedule throughout.

### 1.2 Fees observed in RIA disclosures (2025–2026)

| Firm (CRD / SEC no.) | Sponsor(s) | DAF fee disclosed | Date | Source |
|---|---|---|---|---|
| IEQ Capital (CRD 301819) | Fidelity Charitable, Schwab Charitable | "the Firm will charge an annual management fee equal to up to 1% of Charitable Platform assets, however, IEQ reserves the right to waive such fees" | 2025-10-30 | [ADV 2A](https://ieqcapital.com/wp-content/uploads/2025/10/ADV-2A-and-CRS-Combined-10.31.2025.pdf) |
| ACM Wealth (CRD 112266) | Fidelity CIAP | No CIAP-specific rate. Private accounts: "Equity Accounts Up to 1.50%"; fixed income up to 0.60%. Under the CIAP agreement this schedule is the ceiling [I] | 2026-03-29 | [ADV 2A](https://acmwealth.com/wp-content/uploads/2026/06/ADV-Part-2A-Disclosure-Brochure-March-2026-ACM-Wealth.pdf) |
| Winthrop Wealth (CRD 288178) | AEF (via LPL/Schwab) | DAF assets are under the general schedule: "This management fee varies between 30 and 200 basis points (0.30% – 2.00%)". AEF's fees "are not paid to WW" | 2026-08-17 | [ADV 2A](https://winthropwealth.com/wp-content/uploads/2026/08/Winthrop-Wealth-ADV-2A-8.17.2026.pdf) |
| Waverly Advisors (SEC 801-60741) | DAFgiving360, Fidelity Charitable, RCF, community foundations | DAF fee "may be lower or higher than" its client-asset fee. The DAF fee is set at application. The donor may pay it outside the fund. General schedule 0.25–1.5% | 2025-03-28 | [ADV 2A](https://waverly-advisors.com/wp-content/uploads/Waverly-ADV-Part-2A-Brochure-3-28-25-Final.pdf) |
| FC Advisory (CRD 170478) | DAFgiving360 | "We do not charge advisory fees to non-discretionary assets invested in donor-advised fund (DAF) accounts." | 2026-03 | [ADV 2A](https://www.thenewwealthproject.com/wp-content/uploads/2026/03/2026-FCADV-Form-ADV-Part-2A.pdf) |
| Redhawk Wealth Advisors | DAFgiving360 | 0 / 0.25 / 0.50 / 0.75% advisory, plus 0.25% Redhawk admin, plus 0.25% Redhawk portfolio management when its models are used | 2025-05-21 | [Program document](https://advisor.redhawkwa.com/wp-content/uploads/2025/05/DAFgiving360-Process-05212025.pdf) |

**Reading [I]:**
- Rates cluster at or below 1.00% where a DAF-specific figure is given (IEQ, Redhawk, FC Advisory).
- Where the DAF falls under a firm's general schedule (ACM, Winthrop, Waverly), the stated ceiling is 1.5–2.0%.
- Seven documents are not a sample, and ADV ranges are maxima. So the illustrative 1.00% is a plausible upper-middle value for a fee-charging account. It is not an observed typical rate.

### 1.3 Sponsor-wide measure from Form 990 (line 11f ÷ average total assets)

| Sponsor | TY | Line 11f | Avg total assets | Ratio | Usable as an adviser-fee measure? |
|---|---|---|---|---|---|
| **AEF** | 2024 | $35.95m | $7.78bn | **0.46%** | **Yes, with caveats.** AEF requires an outside adviser on every fund and runs no investment management itself. TY2023 0.44%; TY2022 0.40%. I re-checked TY2024 against the [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml) |
| RCF | 2024 | $11.69m | $5.05bn | 0.23% | Weak. Brokerage-level fees may never reach RCF's books, and donor-directed assets are mixed in |
| NPT | 2025 | $93.8m | $49.2bn | 0.19% | No. It includes NPT's pooled-portfolio advisory fee |
| Fidelity Charitable | 2025 | $84.3m | $76.5bn | 0.11% | No. No public figure for CIAP assets was found |
| Vanguard Charitable | 2024 | $0 | $19.6bn | 0 | Confirms there is no adviser layer |

Figures come from [`sponsor-cost-structure.csv`](../../data/mission-2026-11-14/sponsor-cost-structure.csv) (the 990 XML harvest).

**AEF caveats [I]:**
- The 0.46% is an asset-weighted average across all AEF funds. That includes zero-fee and commission-based accounts.
- It excludes fees that donors pay advisers personally, an option Waverly describes.
- A fee-charging AEF account therefore probably pays more than 0.46%. The average cost per AEF dollar, however, is well below 1.00%.

### 1.4 Effect on the all-in table (rows of `all-in-cost-comparison-2026.csv`; not edited)

Line numbers count the header as line 1.

| Rows | Sponsor | Change indicated | Material? |
|---|---|---|---|
| 2–4 | Fidelity Charitable | `adviser_option_eligible_at_balance`: change "unknown (minimum not published)" to **no** at $25k and **yes** at $250k and $2.5m ($100k minimum). Add a note that CIAP at other custodians pays a 70 bps first tier, which adds +0.10% at $250k. The 1.00% illustrative fee stays inside the observed 0–1.5% range | Eligibility: yes (the $25k "with adviser" figure is not available). Fee: no |
| 11–13 | NPT | Eligibility for a segregated (adviser-managed) account: **no** at $25k and $250k, **yes** at $2.5m ($500k minimum). The $25k and $250k "with adviser" totals (1.85% / 2.46%) model an option those balances cannot use. A pooled-account FA fee may still exist ([R] FAQ) | Yes |
| 23–25 | AEF | Basis could move from `illustrative_assumption` to an observed 990 average of about 0.46%. At $250k, with adviser excluding fund expenses: 0.70% + 0.46% = **1.16%**, against 1.70% now. At $2.5m: 0.36% + 0.46% = **0.82%**, against 1.36% | Yes, if the table models the average dollar. Keep 1.00% as a fee-charging-account case |
| 14–16 | RCF advisor-managed | 990 ratio 0.23%. Too weak to replace the illustrative 1.00%. Flag only | No |
| 8–10 | DAFgiving360 | Typical pool JBALX 0.664% against 0.65% (+1.4 bps). Low-cost pool SWTSX unchanged. Pools that changed are not the ones modelled. The Redhawk example shows third-party admin layers can sit inside the 1% cap | No |
| 5–7 | Vanguard Charitable | None (blank adviser layer confirmed) | No |

---

## 2. P-ACC-02: DAFgiving360 pools after the September 2026 change

- **Change:** search-index captures of DAFgiving360's advisor investment page and quarterly performance report say three core pool funds changed effective **2026-09-24** ([R](https://www.dafgiving360.org/investment-options-advisor); [R](https://www.dafgiving360.org/features/investment-options/quarterly-performance-report)). The snippet text reads "Changed the Large Cap Equity Managed Pool fund (PRILX to FFICX)".

| Pool | Old fund (expense ratio [3P]) | New fund (expense ratio [3P]) | Change |
|---|---|---|---|
| Large Cap Equity Managed | Parnassus Core Equity Inst PRILX 0.588% | American Funds Investment Co. of America F-3 FFICX 0.283% | −0.31 pp |
| Socially Responsible Balanced | Impax Sustainable Allocation Inst PAXIX 0.669% | Calvert Balanced I CBAIX 0.663% | ≈0 |
| Short-Term Income | Principal Short-Term Income Inst PSHIX 0.407% | Baird Short-Term Bond Inst BSBIX 0.292% | −0.12 pp |
| Balanced (typical pool in the table) | JBALX, unchanged | 0.664% | +0.014 pp vs 0.65% modelled |

- **Expense-ratio source:** stockanalysis.com fund pages ([PRILX](https://stockanalysis.com/quote/mutf/PRILX/), [FFICX](https://stockanalysis.com/quote/mutf/FFICX/), [PAXIX](https://stockanalysis.com/quote/mutf/PAXIX/), [CBAIX](https://stockanalysis.com/quote/mutf/CBAIX/), [PSHIX](https://stockanalysis.com/quote/mutf/PSHIX/), [BSBIX](https://stockanalysis.com/quote/mutf/BSBIX/), [JBALX](https://stockanalysis.com/quote/mutf/JBALX/)), read 2026-11-15. The ratios are undated on the page, and pool-level operating costs above the fund expense are not visible.
- **Admin fee:** a search-index capture of the Q3 2026 report says performance is net of "an assumed 0.60% annualized administrative fee" [R]. That matches the table.
- **Admin tiers above $5m:** the Redhawk document lists 0.13% for the next $5m, 0.12% for the next $5m and 0.10% above $15m [F, third-party firm]. The repo lists tiers only to $5m.
- **Not done:** the Q3 2026 PDF itself and the pool-level expense ratios (P-ADV-03).

---

## 3. P-LDG-01: NPact ownership

| Fact | Evidence | Source |
|---|---|---|
| BroadWest bought Fusion Labs; close **2020-12-30**; renamed NPact | "On December 30, 2020, investment firm BroadWest Partners completed its acquisition of Dallas, TX based Fusion Labs" | [Trident World Ventures release, 2021-04-28](https://www.einpresswire.com/article/539680979/trident-world-ventures-provides-sell-side-advisory-to-fusion-labs) [F, sell-side adviser] |
| Owners named | "BroadWest managing partners and new NPact co-owners Jeff Conn and Brian Greeley". Seller entity "Fusion Labs, Inc." No co-investors, lenders or price named | same |
| 2022 FIMS / DonorCentral NXT buyer and price | "sold our ... ("FIMS") and DonorCentral NXT solutions to Fusion Laboratories, LLC for cash proceeds of approximately $ 6.4 million". Dated 2022-09-09 | [Blackbaud 10-Q Q3 2022, Note 3](https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm) [F, SEC filing] |
| 2022 release | Quotes "NPact co-CEO Jeffrey Conn". No investor or financing named | [PR Newswire 2022-09-12](https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html) [F] |
| Second owner-type listing | Cambria's portfolio lists "NPact: Developer of grant management and donor-advised fund management software ... Dallas, TX". Cambria says it backs search funds and their acquired businesses | [Cambria portfolio](https://cambriagroup.com/portfolio?start=192); [Cambria search funds](https://cambriagroup.com/our-approach/search-funds) [F] |
| Current leadership | Leadership Team: "Burt Hurlock, Chief Executive Officer". Conn and Greeley are not listed | [npact.com/about](https://npact.com/about/) [F] |
| Aggregators | CB Insights: investors BroadWest and Riviera Capital. PitchBook: "Private Equity-Backed". privateequityinfo: owner "Cambria Group" | [CB Insights](https://www.cbinsights.com/company/fusion-labs) [R]; [PitchBook](https://pitchbook.com/profiles/company/64184-68) [R]; [privateequityinfo](https://privateequityinfo.com/directory/private-equity-portfolio-company/3/npact) [3P] |

**Reading [I]:**
- BroadWest is an operator-led partnership of two co-CEOs, which matches the search-fund model, and Cambria lists NPact as a portfolio company. Cambria was probably an equity investor alongside BroadWest, at the 2020 buyout or later.
- **Correction:** the 2022 FIMS purchase was a cash asset purchase by NPact's own entity. Neither the 10-Q nor NPact's release shows new outside capital. Funding of the $6.4m is not disclosed.
- The entity forms disagree across documents: "Fusion Labs, Inc." (2021 seller), "Fusion Laboratories, LLC" (2022 buyer; 2025 Standard Terms) and "a Delaware corporation" (Terms of Use, per V10-02). This fits a post-close conversion, but that is unverified.
- **Not done:** the BroadWest portfolio page (host not allowed here) and Texas/Delaware entity records (P-ADV-04).

---

## 4. P-NPT-05: DAFgiving360 grant payment rail

| Source | What it says | Date | Label |
|---|---|---|---|
| [2024 Program Policies PDF](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) | Checks issued directly to the charity (repo baseline) | 2024-12 | F |
| [How to recommend a grant](https://www.dafgiving360.org/content/how-to-recommend-grant) | "the charity will receive a grant award letter with a check" | undated | R |
| [FAQs](https://www.dafgiving360.org/features/faqs) | USPS delivery "typically takes seven to 10 business days" | undated | R |
| [Chariot help center](https://help.givechariot.com/llms-full.txt) | "Gifts from other grantmakers—such as Fidelity, Vanguard, and Schwab—will still be delivered the same way as before." | live 2026-11-15 | F (vendor) |
| [Chariot disbursements page](https://www.givechariot.com/disbursements); [Chariot e-pay article](https://givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors) | Partners shown: Daffy, Groundswell, Founders Pledge, DJCF and others. Fidelity is moving to electronic-only payment in July 2026. DAFgiving360 is not mentioned | 2026 | F (vendor) |
| [2025 year-end guidelines](https://s3.amazonaws.com/static.contentres.com/media/documents/c2152e0d-e88d-4387-a83c-a5cc42ca4496.pdf) | Covers contribution rails (wire/EFT in) and grant timing only. Nothing on how grants are paid out | 2025-09 | F |

**Conclusion:**
- No 2025–26 source shows DAFgiving360 paying charities by ACH/EFT.
- The `sponsor-eft-providers-2026.csv` DAFgiving360 row ("None documented; check") stands, still flagged "2026 status unverified".
- The 2026 Program Policies web page could not be read (P-ADV-05).

---

## 5. Corrections and additions to repo files (not applied)

1. **`all-in-cost-comparison-2026.csv`:** the eligibility and AEF basis changes in §1.4. Also add the Fidelity CIAP "Other Custodian" 70 bps tier as a note.
2. **`sponsor-eft-providers-2026.csv`, DAFgiving360 row:** append the Chariot help-center sentence as 2026 corroboration.
3. **`queue-ledgers-behind-portals.md`, line 26 ("Possible owner"):**
   - Replace with: "BroadWest Partners (Jeff Conn, Brian Greeley) closed the acquisition 2020-12-30 per the sell-side adviser's 2021-04-28 release. Cambria Group lists NPact as a portfolio company. The 2026 owner is unconfirmed."
   - Change EJ-edge status for BroadWest from `unknown` to `confirmed (2020)`.
4. **`queue-all-in-cost-dafpay-access.md`, line 124:** pool fund changes now identified (§2). The typical-pool figure stands.
5. **`sponsor-fee-schedules.csv`, DAFgiving360:** add tiers above $5m (0.13 / 0.12 / 0.10%), sourced to the Redhawk 2025 document.

---

## 6. Source register

| ID | Source | URL | Date | Label |
|---|---|---|---|---|
| A01 | Fidelity CIAP Investment Advisor Agreement | https://www.fidelitycharitable.org/docs/CIAP-Investment-Advisor-Agreement.pdf | PDF mod 2025-01-28 | F |
| A02 | Fidelity CIAP Investment Policies & Guidelines | https://www.fidelitycharitable.org/docs/ciap-investment-policies-guidelines.pdf | PDF mod 2026-07-10 | F |
| A03 | Fidelity CIAP overview | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/ciap-overview.pdf | PDF mod 2025-04-17 | F |
| A04 | Fidelity CIAP donor application | https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/ciap-donor-application-form.pdf | PDF mod 2026-07-28 | F |
| A05 | Fidelity Charitable Program Guidelines | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf | PDF mod 2026-09-11 | F |
| A06 | AEF 2023 Program Description | https://air-original.imgix.net/678d90a0-ec95-45e2-9126-674089482adb.pdf?ixlib=react-9.5.4 | 2023-12-22 | F |
| A07 | NPT Guide to your DAF | https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf | 2024-09 | F |
| A08 | NPT FAQ | https://www.nptrust.org/donor-advised-funds/faq/ | live | R (search summary) |
| A09 | RCF circulars (UBS, RBC, Ameriprise, LPL, RCF Giving Fund) | https://www.reninc.com/wp-content/uploads/2025/08/UBS-Program-Circular-2.pdf ; https://rbcrcf.donorfirstx.com/pdf/RBC/Program%20Circular.pdf ; https://ampf.donorfirstx.com/pdf/AMPF/RCF%20Program%20Circular%20for%20Ameriprise%20Clients.pdf ; https://www.reninc.com/wp-content/uploads/2025/09/2309-RCF-FRM-DAF-LPLCircular.pdf ; https://rcfgivingfund.donorfirstx.com/pdf/RCFGF/RCF%20Giving%20Fund%20Circular.pdf | 2023–2025 | F |
| A10 | Vanguard Charitable Policies & Guidelines | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines | live | F |
| B01 | IEQ Capital ADV 2A | https://ieqcapital.com/wp-content/uploads/2025/10/ADV-2A-and-CRS-Combined-10.31.2025.pdf | 2025-10-30 | F |
| B02 | ACM Wealth ADV 2A | https://acmwealth.com/wp-content/uploads/2026/06/ADV-Part-2A-Disclosure-Brochure-March-2026-ACM-Wealth.pdf | 2026-03-29 | F |
| B03 | Winthrop Wealth ADV 2A | https://winthropwealth.com/wp-content/uploads/2026/08/Winthrop-Wealth-ADV-2A-8.17.2026.pdf | 2026-08-17 | F |
| B04 | Waverly Advisors ADV 2A | https://waverly-advisors.com/wp-content/uploads/Waverly-ADV-Part-2A-Brochure-3-28-25-Final.pdf | 2025-03-28 | F |
| B05 | FC Advisory ADV 2A | https://www.thenewwealthproject.com/wp-content/uploads/2026/03/2026-FCADV-Form-ADV-Part-2A.pdf | 2026-03 | F |
| B06 | Redhawk DAFgiving360 process document | https://advisor.redhawkwa.com/wp-content/uploads/2025/05/DAFgiving360-Process-05212025.pdf | 2025-05-21 | F (firm) |
| C01 | AEF Form 990 TY2024 XML | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml | filed 2025 | F |
| C02 | Repo 990 cost extract | data/mission-2026-11-14/sponsor-cost-structure.csv | TY2022–2025 | F (derived) |
| D01 | DAFgiving360 advisor investment options (fund changes) | https://www.dafgiving360.org/investment-options-advisor | 403; search capture | R |
| D02 | DAFgiving360 quarterly performance report | https://www.dafgiving360.org/features/investment-options/quarterly-performance-report | 403; search capture | R |
| D03 | stockanalysis.com fund pages (7 tickers) | https://stockanalysis.com/quote/mutf/FFICX/ (etc.) | read 2026-11-15 | 3P |
| E01 | Trident World Ventures release (EIN Presswire) | https://www.einpresswire.com/article/539680979/trident-world-ventures-provides-sell-side-advisory-to-fusion-labs | 2021-04-28 | F |
| E02 | Blackbaud 10-Q Q3 2022 | https://www.sec.gov/Archives/edgar/data/1280058/000128005822000055/blkb-20220930.htm | 2022-11-03 | F |
| E03 | NPact release (PR Newswire) | https://www.prnewswire.com/news-releases/npact-acquires-fims-and-donorcentral-nxt-products-from-blackbaud-301622291.html | 2022-09-12 | F |
| E04 | NPact About page | https://npact.com/about/ | live | F |
| E05 | Cambria Group portfolio; search-fund page | https://cambriagroup.com/portfolio?start=192 ; https://cambriagroup.com/our-approach/search-funds | live | F |
| E06 | CB Insights; PitchBook; privateequityinfo | https://www.cbinsights.com/company/fusion-labs ; https://pitchbook.com/profiles/company/64184-68 ; https://privateequityinfo.com/directory/private-equity-portfolio-company/3/npact | live | R / 3P |
| F01 | Chariot help center (llms-full) | https://help.givechariot.com/llms-full.txt | live | F (vendor) |
| F02 | Chariot disbursements; e-pay article | https://www.givechariot.com/disbursements ; https://givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors | 2026 | F (vendor) |
| F03 | DAFgiving360 grant page; FAQ; Program Policies | https://www.dafgiving360.org/content/how-to-recommend-grant ; https://www.dafgiving360.org/features/faqs ; https://www.dafgiving360.org/features/program-policies | 403; search capture | R |
| F04 | DAFgiving360 2025 year-end guidelines | https://s3.amazonaws.com/static.contentres.com/media/documents/c2152e0d-e88d-4387-a83c-a5cc42ca4496.pdf | 2025-09 | F |

---

## 7. Data dictionary: `adviser-fees-observed-2026.csv`

| Column | Meaning |
|---|---|
| sponsor | DAF sponsor whose accounts the fee applies to (several separated by ";") |
| program | Sponsor program or account type (e.g. CIAP, segregated account) |
| adviser_firm | RIA or firm, with CRD/SEC number where shown. "(program rule)" = the sponsor's own rule for all firms. "(sponsor-wide)" = 990 aggregate |
| fee_schedule | The fee, range, cap or rule as disclosed (paraphrased; quotes ≤40 words in the report) |
| source_type | `ADV` (Form ADV Part 2A), `program page` (sponsor guideline, circular, agreement, form), `firm program document`, `990 proxy` (Part IX line 11f ÷ average total assets) |
| source_url | Primary URL(s), separated by " ; " |
| date | Document date (cover date, or PDF modification date where no cover date). For 990 rows, the tax year |
| evidence_label | F / R / 3P / I, as defined above. "F (filing) / I (interpretation)" = the number is first-party but its reading as an adviser fee is my inference |
| retrieved | Date the source was read |
| notes | Caveats, scope and cross-references |
