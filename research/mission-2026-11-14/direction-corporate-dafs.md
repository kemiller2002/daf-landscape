# Direction: corporate and employee DAFs, 2021–2026

**Date:** 2026-11-15 · **Agent:** batch41 N18 · **Queue item:** P-NEW-CORP-01 (owner direction, 2026-11-15)
**Read first:** [queue-batch34-pass-through-channels.md](queue-batch34-pass-through-channels.md) (wave-19 governing corrections) and [queue-batch35-panel-screens.md](queue-batch35-panel-screens.md) (wave-20 governing corrections). None of those corrections changes a figure used here. The AOGF split (695 DAF-column accounts, FYE 2026-03) is the batch-34/35 filed value.

**Outputs**
- [`data/mission-2026-11-14/corporate-daf-programs-2021-2026.csv`](../../data/mission-2026-11-14/corporate-daf-programs-2021-2026.csv): 49 company programs (CD01–CD49) and 5 sponsor aggregates (SA01–SA05).
- [`data/mission-2026-11-14/relationship-graph-edges-additions-24.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-24.csv): EX001–EX025.
- [`data/mission-2026-11-14/queue-proposals-batch41-n18.csv`](../../data/mission-2026-11-14/queue-proposals-batch41-n18.csv): P-B41N18-01 to -03.

**Labels:** **[F]** first-party document read this pass (SEC filing, sponsor report or page). **[X]** Form 990 value: from the repo harvest, or from the AOGF XML cached by batch 34/35. **[S]** secondary source. **[R]** search-index capture only (the page was not fetched). **[C]** computed here. **[I]** inference.

**Rules followed.** Recency 2021–2026; events from 2020 or earlier are flagged `dated_context` in the CSV. No logins, forms or contact. robots.txt was read on each host before fetching. dafgiving360.org and schwabcharitable.org returned 403 for robots.txt, so **they were not fetched**. crt.sh was not used. SEC EDGAR full-text search ran with a generic User-Agent. This is research, not legal or tax advice.

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Which companies run corporate or employee DAFs?** | **49 named programs, 2021–2026. 48 come from SEC filings and 1 (NVIDIA) from a sponsor page.**<br>- EDGAR full-text search for "donor advised fund" (2021-01-01 to 2026-11-15) returned **211 10-K documents from 100 filers** and **146 proxy documents from 64 filers**.<br>- About a third of the 10-K filers (33 of 100) describe their own company program. Most other hits are boilerplate: credit-agreement "permitted holder" definitions, insider-trading gift rules, late Form 4s and director biographies.<br>- Searching by sponsor name ("Tides Foundation", "Fidelity Charitable", "Silicon Valley Community Foundation", "Charities Aid Foundation", "Rockefeller Philanthropy Advisors") added PagerDuty, Rapid7 and Lam Research. | High (filed text); the list is a floor, since private companies do not file |
| **Which sponsors hold them?** | **26 of the 49 filings do not name the sponsor.** They say "an independent donor advised fund" (Twilio, Toast) or "a national donor-advised fund program" (IDEXX).<br>**Where a sponsor is named:**<br>- Tides Foundation: 8 (Braze, Okta, Olo, Zuora, Upwork, PagerDuty, Rapid7, Unity), plus Twilio from a 2019 secondary source;<br>- Silicon Valley CF: 4 (Brilliant Earth, Pluralsight, Lam, NVIDIA);<br>- Fidelity Charitable: 3 (Circle, Align, Steve Madden);<br>- one each at Rockefeller Philanthropy Advisors (Remitly), Renaissance Charitable (BNY), Community Foundation for Southeast Michigan (Huntington), NPT (Hyatt) and "Charities Aid Foundation" (CrowdStrike);<br>- one captive employee sponsor (Goldman Sachs Gives).<br>**Not found in any 2021–2026 filing:** a company naming DAFgiving360/Schwab, Vanguard Charitable, Givinga or Goodstack as its corporate DAF sponsor. | High |
| **How big is the segment?** | **Only three sponsors publish a corporate split.**<br>- **Fidelity Charitable 2025:** 556 corporate DAFs, more than 550 companies, **$539.8m of grants** (26,036 grants, average $20,732) [F]. That is 2.9% of Fidelity's $18.3bn of 2025 grants [C].<br>- **SVCF:** corporate advised funds granted about **$153m in 2025 and $189m in 2024** (audited statements) [F]. That is 6.9% and 5.8% of SVCF's combined advised plus corporate-advised grants [C]. SVCF’s audited series goes back to 2021: about $100m, $175m, $134m, $189m and $153m (2.8%–6.9% a year). Fidelity and SVCF together put corporate DAFs at 3.9% of grants in 2024 and 3.4% in 2025. Of 14 further sponsors checked (Tides, CAF America, RPA, NPT and the 10 largest community foundations), SVCF is the only one that publishes a split, and Form 990 has no corporate column ([b41n18-01](b41n18-01-corporate-daf-segment.md)) [V wave 36A]<br>- **AOGF (Benevity), FYE 2026-03:** Schedule D DAF column of **695 accounts, $1,390.0m of grants**, which Schedule O describes as corporate, with ongoing advice [X]. That is about $2.0m of grants per account [C].<br>- **Tides** (261 DAFs, $210.7m of grants, CY2024) and **CAF America** (740 DAFs, $947.4m, FYE 2025-04) do not separate corporate accounts [X]. | High (published); low on the rest of the market |
| **What are they for?** | **Five patterns, by count of programs:**<br>(1) **IPO equity pledges, usually Pledge 1%:** 15 programs fund the DAF with shares or warrants (Circle, Twilio, Toast, UiPath, Remitly, Braze, Rubrik, AvidXchange, Marqeta, Olo, Zuora, PagerDuty, Okta, Upwork, Unity).<br>(2) **Cash prefunding:** Urban Outfitters $46.0m (FY2026), Logitech $30m, lululemon $25.5m cumulative, Sirius XM $25m, PennyMac, NI, Synovus, Savers.<br>(3) **A "Foundation" brand on a DAF, in place of a private foundation:** Align, Steve Madden, CrowdStrike, Brilliant Earth, Payoneer, Trimble. Cognizant **converted its private foundation into a DAF in late 2022**.<br>(4) **Employee DAFs:** Macerich (company-matched employee DAF benefit), VICI (personal DAF accounts via Groundswell), Cullen/Frost (employees choose grantees), NVIDIA (employee-funded), GS Gives (senior employees), and Zuora's employee match from its DAF.<br>(5) **Deal and governance uses:** Huntington's $50m merger-commitment DAF; Apollo's $200m share-funded DAF with grant recommendations by the CEO; BNY's Executive-Committee "Impact DAF".<br>**Crypto:** Circle (a stablecoin issuer) is the only crypto company with a disclosed corporate DAF (Fidelity). Coinbase's Pledge 1% filings name no vehicle. | High (filed text); [I] on the grouping |
| **Why a DAF rather than a private foundation?** | **The reasons stated in filings and sponsor marketing:**<br>- lower administration ("streamlined administration and greater flexibility", Fidelity);<br>- the sponsor's independence and governance (Circle: "separately governed"; BNY: the sponsor "has no obligation to follow recommendations");<br>- no consolidation (Pluralsight: "we do not control … accordingly we do not consolidate");<br>- the ability to take appreciated or pre-IPO shares and warrants;<br>- a "Foundation" brand without a separate entity (Okta for Good is "not a separate legal entity").<br>**[I] Implied but not stated in any filing:** private-foundation excise tax, payout and public-disclosure obligations. | Medium (stated reasons are clear; their weight is not) |
| **What it means for an entrant** | **[I] A small, concentrated niche that runs on capital-markets workflows:** share issuance, Rule 144 restricted stock, warrants, 10-year installment schedules. Incumbents win on custody and liquidation of corporate stock, sponsor independence and an employee-giving layer. A credible entrant needs equity-gift operations and a sponsor whose independence an auditor can rely on (no consolidation), not just grant software. §5. | [I] |

---

## 1. Method

1. **EDGAR full-text search** (`efts.sec.gov/LATEST/search-index`), forms 10-K and DEF 14A, 2021-01-01 to 2026-11-15:
   - "donor advised fund" (10-K: 211 documents, 100 CIKs; DEF 14A: 146 documents, 64 CIKs);
   - each sponsor name ("Tides Foundation" 44 hits, "Fidelity Charitable" 84, "Silicon Valley Community Foundation" 40, "Schwab Charitable" 18, "DAFgiving360" 4, "National Philanthropic Trust" 80, "Charities Aid Foundation" 6, "Rockefeller Philanthropy Advisors" 6, "Benevity" 33, "Givinga" 0, "American Online Giving Foundation" 0);
   - "Pledge 1%" (10-K/DEF 14A, plus S-1/424B4: 13 documents from 4 issuers).
2. **Document reads.** Every hit document was fetched from `www.sec.gov/Archives` (robots.txt allows Archives). The text within 500 characters of each match was read, and the hits were classified by hand. A row enters the CSV only when the filing describes **the company's own** DAF or employee-DAF program. Insider gifts, director biographies and credit-agreement definitions are excluded.
3. **Sponsor pages and reports:**
   - Fidelity Charitable Giving Reports 2024–2026 and its corporate page;
   - SVCF FY2025 audited statements, its corporations page and its NVIDIA page;
   - Tides' corporations page;
   - search-index captures for CAF America, Pledge 1%, Givinga, Goodstack and DAFgiving360.
4. **Form 990:**
   - Schedule D values for Tides, CAF America, SVCF, CFSEM and GS Gives come from the repo harvest (`form990-returns-schedule-d-harvest-full.csv`).
   - AOGF's Schedule D and O text was read from the FYE 2026-03 XML cached by batch 34/35.
   - A fresh download of the Tides XML was refused by this session's permission policy and was not retried; the harvest values were used instead.

---

## 2. Programs by sponsor (CSV CD rows)

### 2.1 Named sponsors

| Sponsor | Company (fund) | Est. | Amount disclosed | Purpose | Source |
|---|---|---|---|---|---|
| **Tides Foundation** | Braze (Braze for Impact) | MOU 2022-03 | up to 964,647 shares through 2031 | Pledge 1% equity | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1676238/000167623826000013/brze-20260131.htm); [10-K FY2022](https://www.sec.gov/Archives/edgar/data/1676238/000167623822000005/brze-20220131.htm) [F] |
| Tides | Okta (Okta for Good Fund) | pre-IPO (2017) | 300,000 shares reserved | equity; "not a separate legal entity" | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1660134/000166013426000020/okta-20260131.htm) [F] |
| Tides | Olo (Olo for Good) | 2021 | $900,000 of grants by Tides in 2024 | Pledge 1% (1% of fully diluted equity) | [10-K 2024](https://www.sec.gov/Archives/edgar/data/1431695/000143169525000010/olo-20241231.htm) [F] |
| Tides | Zuora (Zuora Impact Fund) | pre-2021 | $0.5m cash, FY2024; matches employee gifts up to $1,000 | equity pledge plus employee match | [10-K FY2024](https://www.sec.gov/Archives/edgar/data/1423774/000142377424000079/zuo-20240131.htm) [F] |
| Tides | Upwork (Upwork Foundation) | 2018 | warrant for 500,000 shares at $0.01 | pre-IPO warrant | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1627475/000162747526000012/upwk-20251231.htm) [F] |
| Tides | PagerDuty (PagerDuty.org) | 2018 | ~$1.5m deployed FY2026 | Pledge 1% warrant | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1568100/000156810026000012/pd-20260131.htm) [F] |
| Tides | Rapid7 (Rapid7 for Good Fund) | n/s | ~$300,000 paid out 2021 | tech workforce diversity | [Proxy 2022](https://www.sec.gov/Archives/edgar/data/1560327/000156032722000042/rapid7-2021proxystatement.htm) [F] |
| Tides | Unity (Unity Charitable Fund) | 2020 (IPO) | 750,000 shares; $63.6m charge (2020) | IPO equity (dated context) | [10-K 2021](https://www.sec.gov/Archives/edgar/data/1810806/000181080622000004/unity-20211231.htm) [F] |
| Tides (secondary) | Twilio (Twilio.org Impact Fund) | pre-2021 | 88,408 shares a year; $9.9m (2025), $9.5m (2022) | Pledge 1%, 0.1% a year | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1447669/000144766926000021/twlo-20251231.htm) [F]; sponsor named by [Pledge 1%](https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/) (2019) [S] |
| **Fidelity Charitable** | Circle (Circle Foundation) | 2025-12 | 268,239 shares, $23.1m charge (2025); up to 2,682,392 reserved | Pledge 1%; crypto/fintech | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1876042/000187604226000062/crcl-20251231.htm); [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1876042/000187604226000112/crcl-20260401.htm) [F] |
| Fidelity Charitable | Align (Align Foundation) | 2020 | n/d | foundation brand on a DAF | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1097149/000109714926000023/algn-20260407.htm) [F] |
| Fidelity Charitable | Steven Madden (Steve Madden Corporate Foundation) | n/s | n/d | managed by Rockefeller Capital Management | [10-K 2025](https://www.sec.gov/Archives/edgar/data/913241/000162828026012995/shoo-20251231.htm) [F] |
| **SVCF** | Brilliant Earth (Brilliant Earth Foundation) | 2021 | $2m since 2021 | "a corporate advised fund with Silicon Valley Community Foundation" | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1866757/000162828026018794/brlt-20251231.htm) [F] |
| SVCF | Pluralsight (Pluralsight One Fund) | pre-2021 | founder equity | no consolidation | [10-K 2020](https://www.sec.gov/Archives/edgar/data/1725579/000172557921000010/ps-20201231.htm) [F] |
| SVCF | Lam Research (Lam Foundation) | n/s | n/d | "administered in partnership with" SVCF; the filing does not say DAF | [Proxy 2022](https://www.sec.gov/Archives/edgar/data/707549/000110465922103703/tm2219406-1_def14a.htm) [F] |
| SVCF | NVIDIA (NVIDIA Foundation) | n/s | n/d | "Only NVIDIA employees may contribute" | [svcf.org/nvidia](https://www.svcf.org/nvidia) [F] |
| **Rockefeller Philanthropy Advisors** | Remitly (Remitly Philanthropy Fund / Remitly Foundation) | 2021 | 181,961 shares a year, 2021–2025 | Pledge 1% | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1782170/000162828026009038/rely-20251231.htm) [F] |
| **Renaissance Charitable** | BNY (Impact DAF) | 2023 | $3.4m of giving supported, 2025 | Executive Committee recommendations | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1390777/000119312526092500/d52987ddef14a.htm) [F] |
| **CF for Southeast Michigan** | Huntington (Huntington DAF) | 2021 | $50m | TCF merger commitment; ex-TCF executives recommend over 7 years | [Proxy 2022](https://www.sec.gov/Archives/edgar/data/49196/000120677422000653/hban3983601-def14a.htm) [F] |
| **NPT** (via JP Morgan) | Hyatt (Hyatt Community Grants Fund) | 2007 | n/d | third parties donate; Hyatt recommends | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1468174/000110465926038759/tm264387-2_def14a.htm) [F] |
| **"Charities Aid Foundation"** | CrowdStrike (CrowdStrike Foundation) | n/s | n/d (>400 nonprofits, FY2026) | foundation brand; scholarships | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1535527/000110465926055599/tm2532333-4_def14a.htm) [F]; CAF America is [I] |
| **GS Gives** (EIN 11-3813663) | Goldman Sachs | pre-2021 | $164m 2025 program; sponsor FY6/2025: 763 DAFs, $237.1m grants, $636.4m EOY [X] | captive employee sponsor | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/886982/000119312526117433/gs-20260319.htm) [F] |

### 2.2 Sponsor not named in the filing (selected; all 26 are in the CSV)

| Company | Amount | Note | Source |
|---|---|---|---|
| Apollo (Apollo DAF) | **$200m** in shares (1,213,003 shares, Feb 2025) | Marc Rowan recommends grants "for the next four years" | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/1858681/000119312526177321/d948913ddef14a.htm); [10-K 2025](https://www.sec.gov/Archives/edgar/data/1858681/000185868126000013/apo-20251231.htm) [F] |
| Urban Outfitters | **$46.0m** (FY2026) | single prefunding contribution | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/912615/000119312526137916/urbn-20260131.htm) [F] |
| Logitech | $30m (FY2021) | "to support our social giving strategies" | [10-K FY2022](https://www.sec.gov/Archives/edgar/data/1032975/000103297522000012/logi-20220331.htm) [F] |
| lululemon | $25.5m cumulative toward a DAF | part of $71.0m Centre for Social Impact | [10-K FY2024](https://www.sec.gov/Archives/edgar/data/1397187/000139718725000013/lulu-20250202.htm) [F] |
| Zoom | $20.9m share donation (FY2026) | shares reserved FY2020; "unaffiliated nonprofit organization" | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1585521/000158552126000030/zm-20260131.htm) [F] |
| Toast | 0.5m shares a year 2021–23; 1m shares Sept 2023; 5.5m reserved | "independent donor advised fund", Toast.org | [10-K 2023](https://www.sec.gov/Archives/edgar/data/1650164/000165016424000084/tost-20231231.htm) [F] |
| UiPath | 0.3m shares a year: $4.2m / $6.6m / $4.2m (FY2026/25/24) | 2.8m reserved; Pledge 1% | [10-K FY2026](https://www.sec.gov/Archives/edgar/data/1734722/000173472226000012/path-20260131.htm) [F] |
| Aramark | $8.8m of Vestis shares (FY2024) | spin-off equity used to fund the DAF | [10-K FY2025](https://www.sec.gov/Archives/edgar/data/1584509/000158450925000219/cik0-20251003.htm) [F] |
| PennyMac Financial | $5.8m (2021), $2.5m (2024), $3.0m (2025) | lumpy, profit-linked | [10-K 2025](https://www.sec.gov/Archives/edgar/data/1745916/000110465926018142/pfsi-20251231x10k.htm) [F] |
| Cognizant | private foundation **converted to a DAF**, late 2022; the TY2022 990-PF of Cognizant US Foundation is a final §507(b)(1)(A) return with $35.6m to the BNY Mellon Charitable Gift Fund (b49-01) [V wave 49B] | "Our philanthropic focuses, goals and giving remain unchanged" | [Proxy 2023](https://www.sec.gov/Archives/edgar/data/1058290/000130817923000721/lctsh2023_def14a.htm) [F] |
| Macerich | "Company-matched donor advised fund" | listed as an employee benefit beside the 401(k), ESPP and 529 | [10-K 2025](https://www.sec.gov/Archives/edgar/data/912242/000091224226000016/mac-20251231.htm) [F] |
| VICI | personal DAF account for each employee, via Groundswell | matching through the DAF | [Proxy 2023](https://www.sec.gov/Archives/edgar/data/1705696/000119312523070714/d460951ddef14a.htm) [F] |
| Cullen/Frost | executive-funded DAF; employees choose the charities | "third-party administrator" | [Proxy 2026](https://www.sec.gov/Archives/edgar/data/39263/000003926326000023/cfr-20260320.htm) [F] |

---

## 3. Sponsor-side corporate programs (CSV SA rows)

| Sponsor | What is published | Figures | Source |
|---|---|---|---|
| **Fidelity Charitable: Corporate Giving Account** | counts and grants by year | 2023: 511 DAFs, $256m (2024 report), **restated as $237m in the 2025 report**.<br>2024: 518 DAFs, $525m, average grant $21,024.<br>2025: **556 DAFs, >550 companies, $539.8m, 26,036 grants, average $20,732**.<br>Gift4Giving: >4,000 e-gifts, $1.2m (2025). | [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf), [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf), [2026](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) Giving Reports [F] |
| Fidelity: terms | page | $100,000 initial contribution; admin fee "$10,000 plus 0.60%" (tiered); grants from $50; investment fees 0.015%–0.93%; guidance on "transitioning a private foundation" | [corporate-giving page](https://www.fidelitycharitable.org/corporate-giving.html) [F] |
| **SVCF: corporate advised funds** | audited grant totals | about **$153m (2025) and $189m (2024)** of grants; "one of the largest corporate-advised fund programs" | [FY2025 audited statements](https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf) [F] |
| **AOGF (Benevity)** | Schedule D column split | FYE 2026-03:<br>- **DAF column:** 695 accounts; contributions $1,557.8m; grants $1,390.0m; EOY value $205.7m.<br>- **Other-funds column:** 751,746 accounts; grants $935.7m.<br>- **Schedule O:** AOGF "efficiently works with corporate employee giving programs"; corporate donations are "consistent with conventional DAF models".<br>- **Fee:** Benevity Inc administrative services, $54.65m. | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml) [X] |
| **Tides Foundation** | Schedule D, and a web claim | CY2024 Schedule D: **261 DAFs**, $210.7m of grants, $324.5m EOY [X]. The web page says "over 400 donor advised funds".<br>Fees: "1% on standard donor advised funds to 5%"; minimum $100,000 committed. Named corporate partners: Sephora, Google, General Assembly. | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523189349301347_public.xml) (repo harvest); [corporations page](https://www.tides.org/partners/corporations/) [F] |
| **CAF America** | Schedule D only | FYE 2025-04: 740 DAFs, $947.4m of grants [X]. Business fund holders are allowed (DAF policies) [R]. | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610489349300906_public.xml); [DAF policies](https://cafamerica.org/daf-policies/) [R] |
| **DAFgiving360 (Schwab)** | not verified | robots.txt returned 403, so no fetch. The search index showed no business or corporate account type [R]. | [dafgiving360.org/donor-advised-funds](https://dafgiving360.org/donor-advised-funds) [R] |
| **Givinga / Goodstack** | no corporate DAF holder named | Givinga's corporate-DAF marketing is dated 2018 (DAFs "less expensive and time-consuming to maintain than private foundations"). Goodstack names LinkedIn, Adobe and Asana as platform users, not as DAF holders. | [Givinga blog (2018)](https://www.givinga.com/insights/blog/types-of-corporate-giving-valued-corporate-citizens) [F, dated]; [Goodstack 2025 review](https://goodstack.org/blog/how-goodstack-has-powered-over-usd5b-in-donations-to-nonprofits) [R] |
| **Pledge 1%** | channel to Tides | "preferred philanthropic partner for U.S. Corporate donor-advised funds is Tides (with the exception of Boston and Colorado)"; warrant deduction "when the warrant is exercised" | [Pledge 1% community, Unit 5](https://community.pledge1percent.org/t5/Make-an-Equity-Pledge/Unit-5-Choose-your-philanthropic-partner/ta-p/29428) [R]: returned 403 to fetch |

**Cross-checks [C]:**
- Fidelity's 2025 corporate grants average **$0.97m per corporate DAF** ($539.8m ÷ 556).
- AOGF's DAF column averages **$2.0m per account** ($1,390.0m ÷ 695).
- The repo's earlier line "Corporate DAFs (556 in 2025) average $20,732 a grant" (`direction-donor-behaviour-crises.md` §2.1) matches the 2026 report.

---

## 4. Why companies choose DAFs over private foundations

**Stated in filings [F]:**
1. **No separate entity, no consolidation.**
   - Okta: "Okta for Good is a part of our company and not a separate legal entity".
   - Pluralsight: "we do not control the Pluralsight One Fund sponsors, and accordingly we do not consolidate the donor advised fund's activities".
2. **Independence as a feature.**
   - Circle: "As a donor-advised fund housed with Fidelity, it is separately governed and focused entirely on mission-aligned giving. We cover the operational costs".
   - BNY: the sponsor "has no obligation to follow recommendations" and is "governed by a majority independent board".
3. **Equity in, cash out.** Shares or warrants go in, and the sponsor sells them:
   - 15 of the 49 programs are funded with shares or warrants;
   - Twilio and Toast record them as unregistered issuances "to an independent donor advised fund";
   - Axon's 2021 compensation committee let executives transfer vested shares to DAFs.
   The deduction and G&A charge are taken at fair value when the shares are issued: UiPath, Circle, Zoom.
4. **A "Foundation" brand without a foundation.**
   - Align Foundation, Steve Madden Corporate Foundation, CrowdStrike Foundation, Brilliant Earth Foundation, Payoneer Foundation and Circle Foundation are all DAFs.
   - Cognizant **converted** its US private foundation into a DAF in late 2022 (confirmed in filings: Cognizant US Foundation’s TY2022 990-PF is marked final and §507(b)(1)(A), and its one sponsor grant, $35.6m to the BNY Mellon Charitable Gift Fund, is described as a transfer to a newly created DAF; b49-01) [V wave 49B], with "goals and giving … unchanged".
5. **Employee engagement and brand.**
   - Upwork: the DAF "fosters workforce morale, enhances our community presence, and strengthens our brand".
   - Zuora, Macerich and VICI run employee matching or employee accounts through the DAF.
6. **Flexible commitments.** Huntington used a DAF to meet a merger community commitment, with named former executives recommending grants over seven years.

**Sponsor marketing [F]:**
- Fidelity: "an alternative or a complement to a corporate foundation, offering streamlined administration and greater flexibility" (2026 report). The corporate page adds time and money savings "compared to the reporting and management requirements of … foundations".
- Tides: helps companies "reduce the complexities of grantmaking".
- Givinga (2018, dated): DAFs "less expensive and time-consuming to maintain than private foundations".

**Not stated by any company, but implied [I]:**
- A private foundation's net-investment-income excise tax, 5% minimum payout and self-dealing rules (IRC §§4940, 4942, 4941) do not apply to a DAF holder.
- 990-PF grant lists are public, and PepsiCo's proxy notes that its foundation's grants "are publicly disclosed in its tax returns".
- **Counterpoint:** several companies run both vehicles: Truist (Truist Foundation plus Truist Charitable Fund), Rapid7 (DAF plus a 2021 foundation) and Goldman (Goldman Sachs Foundation plus GS Gives). The DAF is often a complement, not a replacement.

**Timing [I]:**
- The OBBBA 1% corporate floor applies to tax years beginning after 2025 (`direction-policy-lobbying-obbba.md`).
- Of the large 2025/FY2026 contributions, Apollo's $200m (Feb 2025) predates the floor's first bill text (2025-05-12), although its DAF is meant to fund about four years of grants, and Circle's $23.1m is its “first annual share contribution” under Pledge 1%, so neither is a floor pull-forward. Urban Outfitters' $46.0m fell in its last floor-free year (FY2026), and Zoom's $20.9m could not be re-read. No company read ties a DAF gift to the floor. Late-2025 gifts by BlackRock ($109m of appreciated Circle shares, 2025-12-10), Unum ($20.0m “accelerated”, recipient not named) and Live Oak fit the timing; only Community Financial System (about $0.6m, non-DAF, search-index text) names OBBBA as the reason ([b41n18-02](b41n18-02-corporate-floor-pull-forward.md)) [V wave 42B]

---

## 5. Implications for an entrant [I]

1. **The niche is small but concentrated.**
   - Published corporate grant flows: Fidelity $0.54bn, AOGF's DAF column $1.39bn and SVCF $0.15bn.
   - Against the repo's corrected FY2024 market of $66.4bn of DAF grants (batch 35), corporate is a low single-digit share. Where it is published, it is 3.4%–3.9% of grants (Fidelity and SVCF). It reaches 9.1% if AOGF’s DAF column is counted as wholly corporate, but that is a ceiling for that pool only [V wave 36A]
   - A corporate-only entrant would chase a few hundred to a few thousand accounts.
2. **Distribution runs through the Pledge 1%/Tides route and through employee-giving platforms (Benevity/AOGF, Groundswell), not through financial advisers.**
   - Tides is the most-named sponsor among IPO-equity filers.
   - Fidelity wins on "Foundation"-branded accounts and the crypto issuer (Circle).
3. **The product must handle restricted and unregistered stock, warrants (the deduction comes at exercise), 10-year installment schedules, lock-up timing (Circle re-issued its shares after lock-up expiry), and auditor-grade independence so the company need not consolidate.** These are custody and legal capabilities, not grant UX.
4. **The employee layer is the wedge.** Matching through the DAF (Zuora), employee personal DAFs (VICI/Groundswell), Fidelity's Gift4Giving ($1.2m, 2025) and the AOGF micro-donation column (751,746 accounts) all tie the corporate DAF to HR benefits. An entrant that pairs a corporate DAF with employee accounts competes with Benevity and Groundswell, not with Fidelity alone.
5. **Sponsor anonymity is the norm.** 26 of 49 filers do not name their sponsor, so brand matters less than the operating relationship. That helps a white-label entrant, but public-company evidence will not reveal its share.

---

## 6. Corrections and notes for existing repo text

- **No figure in the batch 34/35 governing corrections changes here.**
- **Fidelity 2023 corporate grants:** the 2024 report says $256m (511 DAFs) and the 2025 report says $237m. Cite the report year with the figure.
- **Tides DAF count:** the 990 shows 261 (CY2024) and 287 (CY2023) DAFs; the web page says "over 400". Use the 990 figure for counts.
- **`direction-donor-behaviour-crises.md` §2.1:** "Corporate DAFs (556 in 2025)" is confirmed; add "$539.8m of grants; >550 companies" [2026 report].

## 7. Limitations

- Only SEC filers are covered. Private companies, which are the main users of SVCF and Tides corporate funds, do not appear unless a sponsor names them. Sponsor pages name four such programs that are not in CD01–CD49: DoorDash and the eBay Foundation (SVCF), and the Bain Capital Relief Fund and Income Research + Management (Boston Foundation) [V wave 36A]
- Snippets were read within ±500 characters of each match. A filing that names the sponsor elsewhere in the document may be undercounted; a whole-document regex for 12 sponsor names was run on the filings of 12 issuers. It found a sponsor name only in Braze's FY2022 10-K (Tides).
- DAFgiving360/Schwab could not be checked (robots.txt 403). The Pledge 1% community page returned 403, and its text is a search-index capture.
- No 990 Schedule I or B can tie a grant to a corporate DAF. Sponsors do not disclose fund-level data.
- A fresh download of the Tides 990 XML was blocked by this session's permission policy. Tides values are from the repo harvest.

---

## Source register

| ID | Source | Date | Used for | Label |
|---|---|---|---|---|
| C1 | EDGAR FTS, "donor advised fund", 10-K and DEF 14A, 2021-01-01 to 2026-11-15 (`https://efts.sec.gov/LATEST/search-index?q=%22donor%20advised%20fund%22&forms=10-K&dateRange=custom&startdt=2021-01-01&enddt=2026-11-15`) | run 2026-11-15 | candidate list | F |
| C2 | EDGAR FTS by sponsor name and by "Pledge 1%" (same date range; forms 10-K, DEF 14A, S-1, 424B4) | run 2026-11-15 | sponsor matches | F |
| C3 | 49 company filings: URLs per row in the CSV `source_url` and `notes` | 2021–2026 | programs | F |
| C4 | [Fidelity Charitable 2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf); [2025](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf); [2024](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2024-giving-report.pdf) | 2024–2026 | SA01 | F |
| C5 | [Fidelity corporate-giving page](https://www.fidelitycharitable.org/corporate-giving.html) | live 2026-11-15 | terms, positioning | F |
| C6 | [SVCF FY2025 audited statements](https://www.svcf.org/assets/files/publications/SVCF-CFS-FY25_Updated-Financials.pdf); [corporations page](https://www.svcf.org/corporations); [NVIDIA page](https://www.svcf.org/nvidia) | 2026 | SA02, CD33 | F |
| C7 | [Tides corporations page](https://www.tides.org/partners/corporations/) | live 2026-11-15 | fees, partners | F |
| C8 | [AOGF 990 FYE 2026-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml) (cached XML) | filed 2026-08 | SA03 | X |
| C9 | Repo harvest `data/mission-2026-11-14/form990-returns-schedule-d-harvest-full.csv` (Tides 202523189349301347; CAF America 202610489349300906; GS Gives EIN 113813663) | FY2022–25 | SA04, SA05, CD03 | X |
| C10 | [Pledge 1% article (Forbes 2019 repost)](https://www.pledge1percent.org/pledging-1-percent-to-charity-made-easy-for-companies/) | 2019 / 2021 | Twilio at Tides | S |
| C11 | [Pledge 1% community, Unit 5](https://community.pledge1percent.org/t5/Make-an-Equity-Pledge/Unit-5-Choose-your-philanthropic-partner/ta-p/29428) | undated | Tides as preferred partner | R |
| C12 | [Givinga blog](https://www.givinga.com/insights/blog/types-of-corporate-giving-valued-corporate-citizens) | 2018-11-06 | marketing claim (dated) | F |
| C13 | [CAF America DAF policies](https://cafamerica.org/daf-policies/); [DAFgiving360](https://dafgiving360.org/donor-advised-funds); [Goodstack review](https://goodstack.org/blog/how-goodstack-has-powered-over-usd5b-in-donations-to-nonprofits) | live | context | R |
| C14 | [PepsiCo proxy 2023](https://www.sec.gov/Archives/edgar/data/77476/000130817923000279/pep4134371-def14a.htm) | 2023-03-21 | private-foundation disclosure contrast | F |

## Data dictionary: `corporate-daf-programs-2021-2026.csv`

| Column | Meaning |
|---|---|
| program_id | CDnn = company program; SAnn = sponsor aggregate |
| row_type | `company_program` or `sponsor_aggregate` |
| company, ticker, cik | Issuer as in EDGAR (CIK without leading zeros) |
| sponsor | DAF sponsor named in the source; `not named` when the filing does not name one |
| sponsor_basis | `named_in_filing`, `secondary`, `sponsor page`, `repo`, `not_named` |
| fund_name | Name used by the company for the fund |
| program_type | `corporate_daf`, `corporate_advised_fund` (community-foundation term), `employee_daf_benefit`, `employee_directed_daf`, `captive_employee_daf_sponsor`, `pf_to_daf_conversion`, `merger_commitment_daf`, `executive_recommended_corporate_daf`, `public_donation_corporate_daf`, `sponsor_corporate_program` |
| year_established | As stated in the filing; `not stated` / `pre-2021` otherwise |
| evidence_year | Fiscal year the disclosure covers |
| amount_usd | Disclosed dollar figure (blank if none); **not additive across rows** (mixes single-year, cumulative and grant figures) |
| amount_basis | What the amount measures, quoted or paraphrased from the source |
| shares | Shares or warrants reserved or contributed |
| purpose_tags | Free-text purpose (equity pledge, crypto, foundation alternative, employee, M&A) |
| pledge_1pct | Y if the filing ties the DAF to Pledge 1% |
| source_url, source_form, source_date | Primary source |
| label | F / X / S / R as above |
| recency_flag | `in_window`, `in_window_edge`, `dated_context_2020`, `dated_context_pre2021_est` |
| notes | Extra sources and quotes |

## Validation corrections (wave 26, 2026-11-15) — governing
Source: [validation-wave26-report.md](validation-wave26-report.md); register `data/mission-2026-11-14/validation-register-wave26.csv`.

1. **§1 Method, EDGAR search.**
   - **Find:** "1. **EDGAR full-text search** (`efts.sec.gov/LATEST/search-index`), forms 10-K and DEF 14A, 2021-01-01 to 2026-11-15:"
   - **Replace with:** "1. **EDGAR full-text search** (`efts.sec.gov/LATEST/search-index`), forms 10-K and DEF 14A, 2021-01-01 to 2026-11-15. In wave 26, `efts.sec.gov/robots.txt` returned 403, so these counts could not be re-run under the robots convention. The program rows were checked in EDGAR Archives instead [V wave 26]:"
2. **§0, AOGF.**
   - **Find:** "Schedule D DAF column of **695 accounts, $1,390.0m of grants**, which Schedule O describes as corporate, with ongoing advice [X]."
   - **Replace with:** "Schedule D DAF column of **695 accounts, $1,390.0m of grants**, which Schedule O describes as corporate, with ongoing advice [X]. Schedule O also places \"various other fund structures that are consistent with conventional DAF models\" in this group, so the column may not be wholly corporate [V wave 26]."
3. **§2.1, Circle row source.**
   - **Find:** "| **Fidelity Charitable** | Circle (Circle Foundation) |"
   - **Replace with:** "| **Fidelity Charitable** (named in the 2026 proxy only; the 10-K says \"a donor-advised fund\") [V wave 26] | Circle (Circle Foundation) |"
