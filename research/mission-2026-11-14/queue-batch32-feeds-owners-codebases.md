# Queue batch 32 C: named DAF feeds in adviser systems (P-B31B-03), Clearlake's Blackbaud stake (P-PE-07), post-2022 fate of Philanthropi, Grapevine, Givinga and Groundswell (P-FAIL-06), acquired DAF codebases (P-FAIL-03)

**Date:** 2026-11-15.

**Method:**
- Public sources only, 2021 onward. No accounts, logins, form submissions or outreach.
- **SEC.** EDGAR submissions JSON, filing indexes, full-text search, 13F information tables and Form D XML. Requests used a generic client name.
- **IRS.** The IRS TEOS index files (`index_2025.csv`, `index_2026.csv`) were used to find e-filed returns. The XML was then read from the GivingTuesday mirror of IRS TEOS.
- **Codebase status.** DNS was checked over DoH (dns.google, cloudflare-dns.com). Registry data came from RDAP, certificate history from crt.sh, and live pages from plain HTTP status reads.
- **Directories.** Two public integration directories were read in full: Addepar's Integration Center (Next.js page data) and Orion's `/integrations` pages 0–10.
- **Exclusions.** fcsuite.com was not fetched. The Wayback CDX API reset connections from this environment, so it was not used.
- **robots.txt.** reninc.com's file gives AI-named agents an `Allow: /faqs/` line and no Disallow. Only the sitemap, one product URL check and two blog posts were read there.

**Builds on, and applies the governing corrections of:**
- [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md), including wave-4 W4-10/11, which do not touch these cases.
- [queue-batch31-filings-feeds.md](queue-batch31-filings-feeds.md), including wave-16 corrections 1–5: the eMoney post is dated 2023-04-17.
- [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md), including wave-7/8 corrections.
- [firms-interested-in-daf-organizations.md](firms-interested-in-daf-organizations.md), including wave-4 W4-6 to W4-9.
- [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md), including its wave-11 corrections.

**Evidence tags:**
- **[F]** fact from a primary source.
- **[C]** calculation.
- **[I]** inference.
- **[R]** search snippet or headline only; the page was not read.
- **[S]** secondary source.
- **[U]** not found.

---

## 0. Answers in brief

| Item | Answer |
|---|---|
| **P-B31B-03** | **Yes, as far as public directories show. Fidelity Charitable is still the only DAF sponsor with a named feed.**<br>• **Addepar:** its portfolio-feed directory holds 406 named entries. The only DAF sponsor is "Fidelity Investments: Charitable Gift Fund/Donor-Advised Fund" [F]. It lists Schwab, Vanguard, Goldman, Morgan Stanley, Merrill/BofA, UBS, JPM and Northern Trust only as brokerage, bank or custody feeds [F].<br>• **Orion:** its public integrations directory (about 110 partners) names no DAF sponsor [F]. It does not list GiftingNetwork either, even though Orion announced a GiftingNetwork partnership on 2025-08-18 [R].<br>• **eMoney:** names Fidelity Charitable sites (2023-04-17) and no other sponsor [F].<br>• **No public institution lists** were found for Black Diamond, Tamarac, Advyzon, Practifi, Plaid or Yodlee [U].<br>• **A competing route is emerging: sponsor-owned DAF accounts held at the adviser's custodian.** Two examples are Altruist/Endaoment (2026-10-06) and Foundation Source's multi-custodial DAF over BridgeFT (2025-09-23) [F]. Those accounts could reach Orion or Black Diamond through ordinary custodian feeds without any named sponsor feed [I]. No vendor document confirms that they do. |
| **P-PE-07** | **Clearlake holds 9,751,837 shares, unchanged since 2024-04, but its stake has risen to about 21.7% through Blackbaud's buybacks. No new take-private proposal is on record.**<br>• **Holding:** 13F for 2026-06-30, 9,751,837 shares, $288.8m [F].<br>• **Proxy:** the 2026 proxy shows 21.13% at 2026-04-13 [F].<br>• **Current share:** 21.68% on 44,978,875 shares outstanding at 2026-10-26 [C].<br>• **No new 13D/A:** Clearlake's last 13D/A on Blackbaud is still 2024-04-15. Its 2024–2025 13D filings concern Forward Air [F].<br>• **Rejection:** the board rejected the $80 indication on 2024-05-15 [F].<br>• **Bylaws:** amended 2025-12-17 to tighten advance-notice rules for stockholder nominations and proposals [F]. |
| **P-FAIL-06** | **None of the four has shut down. Their paths differ:**<br>• **Philanthropi is contracting and its site is dark.** Its sponsor's revenue fell from $2.13m (TY2021) to $0.35m (TY2024), and it has 0 employees [F]. The domain fails to resolve on 2026-11-15, yet certificates for "prd-v3" and "migrate" hosts were issued up to 2026-09 [F].<br>• **Givinga is still raising money.** Form D amendments show $10.77m sold from 15 investors in an offering opened 2023-09-26, signed 2026-09-09 [F].<br>• **Grapevine is flat at about $9–10m a year through its foundation** (TY2023–TY2025) [F]. No funding after the 2023 seed was found [U].<br>• **Groundswell is growing:** its sponsor's revenue rose to $11.9m in TY2024, with 12,808 DAF accounts [F]. It has filed no Form D since 2021 [F]. |
| **P-FAIL-03** | **Of five codebases, three are live, one is merged and one keeps only a brand site:**<br>• **Live, renamed:** DonorFirst/DFX, now Ren's "Giving Platform".<br>• **Live, no longer marketed by name:** iPhi, on 61 hosts. Its product page now returns 404.<br>• **Live under the acquirer:** Vennfi, which powers Charityvest and Foundation Source's private label.<br>• **Merged:** Amicus.io, inside TIFIN Give. amicus.io is orphaned hosting.<br>• **Brand site only:** Pinkaloo. Its sign-up host is NXDOMAIN.<br>• **Customer migration:** public only for iPhi (repo census). [`acquired-codebase-status-2026.csv`](../../data/mission-2026-11-14/acquired-codebase-status-2026.csv) |

---

## 1. P-B31B-03: named DAF feeds in adviser portfolio and reporting systems

| System | What was checked | Finding | Label |
|---|---|---|---|
| **Addepar** | Full [portfolio-data-feeds directory](https://integrations.addepar.com/type/portfolio-data-feeds). The page's `__NEXT_DATA__` holds 406 distinct product names | **One DAF sponsor:** "Fidelity Investments: Charitable Gift Fund/Donor-Advised Fund" ([page](https://integrations.addepar.com/product/fidelity-investments-charitable-gift-fund-donor-advised-fund)).<br>**Brokerage, bank or custody feeds with no DAF type:** Charles Schwab Advisor Services, Vanguard Flagship Select, Goldman Sachs PWM, Morgan Stanley GWM, Merrill Lynch PWM, Bank of America Private Bank, UBS Wealth Management Americas, JP Morgan Private Bank, Northern Trust, BNY Mellon Wealth Management, Pershing and Raymond James.<br>"Charitable/foundation accounts" appears only inside a Canadian feed's account-type text | F |
| **Orion** | [orion.com/integrations](https://orion.com/integrations) pages 0–10 (robots.txt allows them), about 110 partner names | **No DAF sponsor, no GiftingNetwork, no Foundation Source.**<br>• Listed custodians include Charles Schwab, Fidelity, Fidelity Clearing & Custody, Goldman Sachs and BNY Mellon Pershing.<br>• Also listed: Altruist, Apex, Betterment Advisor Solutions and Vanguard.<br>• "Janus Henderson Investors" is listed, but the directory does not say whether this relates to its Givinga-powered Charitable Investment Accounts [U] | F |
| Orion + GiftingNetwork | [Business Wire, 2025-08-18](https://www.businesswire.com/news/home/20250818952704/en/Orion-and-GiftingNetwork-Partner-to-Enhance-Charitable-Giving-Solutions-for-Advisors-and-Clients) headline (white-labeled DAF for Orion advisers). The body returned 403 | A partnership, not a listed data feed | R |
| **eMoney** | [Connection update](https://blog.emoneyadvisor.com/best-practices/the-industry-leader-in-account-aggregation-emoney-connection-update/) (2023-04-17) and [new-connections release](https://prnewswire.com/news-releases/emoney-advisor-adds-new-aggregation-connections-and-apis-for-advisors-and-end-clients-301903655.html) (2023-08-17) | Fidelity Charitable sites are named. The 2023-08 additions name no DAF sponsor | F |
| SS&C Black Diamond | Search only; SS&C briefs describe Schwab integrations ([brief](https://www.sscblackdiamond.com/media/30ujzza4/black-diamond-plus-schwab-integrations-brief.pdf)) | No public custodian or institution list | U |
| Envestnet Tamarac / Yodlee, Advyzon, Practifi, Plaid | Search only | No public institution lists | U |
| Morningstar ByAllAccounts (sold to Pello, 2026) | Batch 30/31: 2023 notice moved FI 44892 "Fidelity Charitable Gift Fund (Investment)" to the Akoya Fidelity feed | No other DAF sponsor found | F (2023) |
| Intuit (Quicken) | Batch 31 `fidir.txt`: the only DAF programme row is "T. Rowe Price Program for Charitable" at `pcg.donorfirstx.com`, a Ren host | Consumer aggregator, not adviser | F (repo) |

**The custodial route (does a parent custodial feed carry sponsor-owned DAF accounts?)**
- **Altruist (2026-10-06).** Altruist added DAFs. "Endaoment, a 501(c)(3) public charity, will own the assets and is the customer of record on each account". Advisers "see the DAF next to a client's other holdings" ([InvestmentNews](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481)) [F].
  - Altruist's own data integration feeds Orion ([Orion directory](https://orion.com/integrations)).
  - Whether DAF accounts flow through that feed is not stated [I].
- **Foundation Source (2025-09-23).** Its turnkey DAF lets "advisors maintain their preferred custodian relationships". BridgeFT's "WealthTech API serves as the backbone" and adds "custodial data access via BridgeFT's API" ([BridgeFT release](https://www.bridgeft.com/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/); [InvestmentNews](https://www.investmentnews.com/fintech/foundation-source-expands-daf-platform-with-advisor-branded-multi-custodial-features/262225)) [F].
- **Wealth-captives.** These are unchanged from batch 31: MSO/3D, MyMerrill and Goldman.com integrate through their own portals and single sign-on. No third-party feed was found.

**Reading [I]:**
- Fidelity Charitable's named Addepar feed is still unique, but it may be losing strategic weight.
- New adviser-channel sponsors avoid needing a feed by holding DAF assets at the adviser's custodian, where existing custodian-to-reporting pipes already run. Examples are Endaoment via Altruist and Foundation Source via BridgeFT.
- **For A3 Y1/Y2:** keep Fidelity Charitable's feed credit. Add "custodial-account DAF, so visible through the custodian feed if mapped" as a pending, unconfirmed credit for Endaoment/Altruist and Foundation Source (see P-B32C-02).
- **Correction to batch 31 §4 (Ren row):** `reninc.com/dfx` now 301-redirects to [`/giving-platform`](https://www.reninc.com/giving-platform/). That page names only the "Giving Platform" and none of the DFX wording quoted in batch 31 [F].

---

## 2. P-PE-07: Clearlake and Blackbaud

| Date | Filing | Fact | Label |
|---|---|---|---|
| 2024-04-15 | [SC 13D/A](https://sec.gov/Archives/edgar/data/1280058/000114036124019714/ef20026924_sc13da.htm) and Blackbaud [8-K ex.99.1](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000028/blkbex991unsolicitedpropos.htm) | Unsolicited, non-binding $80.00/share proposal; 9,751,837 shares | F |
| 2024-05-15 | [8-K ex.99.1 (board letter)](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000040/blkbex991unsolicitedpropos.htm) | "significantly undervalues the Company and is not in the best interests of all Blackbaud stockholders" | F |
| 2024-03-18 | [8-K](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000020/blkb-20240318.htm) | Stockholder Rights Agreement of 2022-10-07 terminated | F |
| 2025-04-22 | [DEF 14A](https://www.sec.gov/Archives/edgar/data/1280058/000128005825000017/blkb-20250421.htm) | Clearlake 9,751,837 = 20.10% (2025-04-14), "based solely on" the 2024-04-15 13D/A | F |
| 2025-12-01 | [8-K](https://www.sec.gov/Archives/edgar/data/1280058/000128005825000053/blkb-20251201.htm) | Buyback capacity raised to $1bn. 2,707,953 shares repurchased in 2025 to 2025-12-01 | F |
| 2025-12-17 | [8-K 5.03](https://www.sec.gov/Archives/edgar/data/1280058/000128005825000057/blkb-20251217.htm) and [8-K 5.02](https://www.sec.gov/Archives/edgar/data/1280058/000128005825000060/blkb-20251217.htm) | Amended bylaws ("Enhance procedures with respect to stockholder nominations"). CEO Gianoni's employment agreement renewed from 2026-01-01 | F |
| 2026-04-21 | [DEF 14A](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000009/blkb-20260418.htm) | Clearlake 9,751,837 = **21.13%** of 46,152,006 (2026-04-13). BlackRock 12.02%; Morgan Stanley 9.78% | F |
| 2026-08-14 | [Clearlake 13F-HR, period 2026-06-30](https://www.sec.gov/Archives/edgar/data/1688282/000090514826003721/form13fInfoTable.xml) (CIK 1688282) | BLACKBAUD INC 9,751,837 shares, $288,849,412, sole discretion. This is the largest of five 13F positions | F |
| 2026-10-28 | [10-Q Q3-2026](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm) | 44,978,875 shares outstanding at 2026-10-26, so Clearlake holds **21.68%** | F / C |
| 2024-04 to 2026-11 | [Clearlake filer index](https://data.sec.gov/submissions/CIK0001688282.json) | 13D/13G filings after 2024-04-15: 2024-05-09 13G, 2024-08-14 13D and 2025-07-03 13D/A. All three concern Forward Air (CIK 912728), not Blackbaud | F |

**Reading [I]:**
- **No take-private is in motion on the public record.**
  - No 13D/A has been filed since 2024-04-15.
  - The 8-K items through 2026-10-28 cover only results, governance and buybacks (2.02, 5.02, 5.03, 5.07, 8.01).
  - Under Rule 13d-2, Clearlake would have to amend its 13D on any material change in its plans or proposals.
- **Clearlake's influence grows passively.** Buybacks of about 7% a year push its share up without any purchase. On the current pace it would pass 25% around 2028. This is an extrapolation [I].
- **Implications for DAF ledgers.**
  - A take-private would change who owns Blackbaud: the vendor of YourCause, the ledger behind Blackbaud Giving Fund disbursements, Financial Edge NXT and the vendor of many community foundations' general ledgers (EP001 etc.).
  - It would not change the charitable assets. Blackbaud Giving Fund is a separate 501(c)(3) (edge E159).
  - The risk is vendor-side: pricing, product rationalisation and data access. Fund custody is not at risk.
  - Clearlake's portfolio pattern in software (e.g., BlackLine, also in its 13F) supports watching for cost-led product consolidation. That is a pattern reading, not evidence.

---

## 3. P-FAIL-06: Philanthropi, Grapevine, Givinga and Groundswell after 2022

### 3.1 Philanthropi: contracting, site dark, engineering activity until at least 2026-09

- **2022 baseline.** About 25 staff, "mostly technologists", and $4m raised in 2021 led by Amex Ventures ([Technical.ly, 2022-06-27](https://technical.ly/startups/philanthropi-keith-leaphart/)) [S]. About $8.5m raised since 2018 ([Payments Dive, 2022-07-08](https://www.paymentsdive.com/news/fintech-philanthropi-taps-into-giving-surge-payments/626794/)) [S].
- **Sponsor charity: Philanthropi Charitable (EIN 45-5634144; formerly Giv2Giv, Inc., renamed 2019-02-19 per Schedule O).** Revenue by year ([ProPublica](https://projects.propublica.org/nonprofits/organizations/455634144); TY2024 [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202523219349326042_public.xml), filed 2025-11-17) [F]:

| TY | Revenue | Expenses | Total assets EOY |
|---|---|---|---|
| 2020 | $1,734,440 | $764,480 | $1,047,270 |
| 2021 | $2,131,591 | $2,232,360 | $994,404 |
| 2022 | $831,524 | $489,076 | $1,552,487 |
| 2023 | $828,711 | $812,221 | $1,400,870 |
| 2024 | $352,878 | $401,489 | $1,352,259 |

- **TY2024 Schedule D.**
  - 5,674 DAFs.
  - Contributions $85,210; grants $220,055; DAF value at year end $482,374.
  - **Average balance:** $85 per account [C].
- **TY2024 Part I and other schedules.**
  - 0 employees and $0 salaries. Management fees were $14,250.
  - A second programme: "financial assistance to employees" (employer hardship relief), $166,122 in grants.
  - **Schedule R:** related entity "PHILANTHROPOS LLC" (EIN 82-4732959), "IT SERVICE" [F].
- **Domain (2026-11-15).**
  - philanthropi.com is registered and was renewed (RDAP: last changed 2026-01-12, expires 2027-01-11) ([RDAP](https://rdap.verisign.com/com/v1/domain/philanthropi.com)) [F].
  - Its Route 53 name servers answer REFUSED, so the name does not resolve. Cloudflare DoH reports "No Reachable Authority" [F].
- **Certificate history.** [crt.sh](https://crt.sh/?q=%25.philanthropi.com) shows certificates issued 2026-05-18 for `app`, `api` and `prd-v3`. Certificates issued 2026-08-06 to 2026-09-04 cover `app-dev-migrate`, `app-stage-migrate`, `api-stage`, `stg-v3`, `sales` and `marketingproject` [F].
- **Reading [I].**
  - Someone was building a "v3" platform with "migrate" environments as late as September 2026. In November 2026, though, the public DNS zone is gone.
  - Possible explanations are a platform migration, a domain move or a wind-down. Public sources do not separate them.
  - Donor balances are small ($0.48m), and the charity still holds $1.35m of total assets.
- **Status:** "contracting / dark site". It is not classified as failed. No Form D was found under the Philanthropi name [U].

### 3.2 Grapevine: flat volume through its foundation

- **Seed.** $1.85m total seed, 2023-08-08 ([Business Wire](https://www.businesswire.com/news/home/20230808466348/en/Grapevine-Closes-1.85M-Total-Seed-Round-Delivers-25-Million-To-Nonprofits-To-Democratize-Philanthropic-Giving)) [F]. No later round was found [U].
- **Grapevine Giving Foundation (EIN 87-2389502).**

| TY | Revenue | Grants | Total assets EOY | Source |
|---|---|---|---|---|
| 2022 | $4,916,043 | n/a | $2,197,238 | [ProPublica](https://projects.propublica.org/nonprofits/organizations/872389502) |
| 2023 | $10,328,267 | n/a | $3,646,685 | ProPublica |
| 2024 | $10,084,366 | $8,102,321 | $4,065,834 | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503189349313790_public.xml) (filed 2025-11-14) |
| 2025 | $9,282,691 | $8,484,172 | $3,430,823 | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642379349300519_public.xml) (filed 2026-08-25) |

- **Schedule D, TY2025 [F].** Reports **1** DAF (a pooled fund) with $672,630 at year end and 0 employees.
- **Contractor [F].** Part VII-B lists **GoodMatch Inc**, New York, "SVCs" $601,139. Its link to the Grapevine company is not established [U].
- **Product focus.** Giving circles, matching and corporate circles. A 2026 Fidelity Charitable Catalyst Fund matching programme is reported on Grapevine's pages ([start.grapevine.org](https://start.grapevine.org/fidelity-charitable-catalyst-fund)) [R]. grapevine.org returned 403 to automated reads.
- **Reading [I].** Volume plateaued at about $9–10m a year (TY2023–TY2025) on a small seed, with no visible new equity. This is a lean, sustained niche, not a growth story.

### 3.3 Givinga: still raising

- **Form D ([filer index](https://data.sec.gov/submissions/CIK0001720830.json)).** One equity offering, first sale 2023-09-26, amended over time [F]:

| Signed | Total sold | Offering size | Investors |
|---|---|---|---|
| 2023-10-09 | $2,672,604 | $3,000,000 | 7 |
| 2025-02-25 | $6,345,366 | $8,154,522 | 13 |
| 2025-08-18 | $7,815,686 | $9,345,365 | 14 |
| 2026-09-09 | $10,766,659 | $11,016,659 | 15 |

- **Aggregators.** VCBacked's "$6.3M" and CB Insights' "$19.47M" are both superseded by the filing for this offering [I].
- **Givinga Foundation (EIN 47-4172718), amended TY2024 990** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml), filed 2025-11-13) [F]:
  - Revenue $13,144,583 (prior year $18,779,918). Grants $11,091,205.
  - 1,421,011 DAF accounts (unit undefined, per batch 30). DAF value $1,949,239.
  - Schedule R lists Givinga Inc.
- **Product focus.** API-first white label. Partners include Janus Henderson Charitable Investment Accounts and Ritmo (2026-06-22) (batch 30 §2.2).
- **Reading [I].** Givinga survived 2022–2026 on a slow, insider-heavy raise and a B2B2C API model. Foundation revenue fell 30% in TY2024.

### 3.4 Groundswell: growing on a single 2021 raise

- **Form D [F].** Groundswell Giving, Inc. has one Form D (2021-12-17): $13,214,985 equity sold, 39 investors, first sale 2021-11-23 ([filer](https://data.sec.gov/submissions/CIK0001899820.json)). No later Form D was found.
- **Groundswell Charitable Foundation (EIN 87-1530516; site groundswellcharitable.foundation).**
  - Revenue TY2022 $2,782,421 → TY2023 $4,931,666 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/871530516)) → **TY2024 $11,890,610** [F].
  - TY2024 grants $4,463,378 and total assets $11,049,807.
  - Its amended TY2024 return ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202640289349301029_public.xml), filed 2026-01-28) adds Schedule D: **12,808 DAFs**, contributions $9,691,912, value at year end $10,084,314 [F]. The original return ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349318726_public.xml)) left Schedule D blank.
  - Salaries $102,261 although the employee count is 0, as filed [F].
  - Schedule R: Groundswell Giving Inc, "developer and operator of proprietary software platform" [F].
- **Product focus.**
  - A CSR suite covering giving, volunteering, ERGs, grants and an employee assistance fund (repo CT193).
  - Chariot Disbursements partner (2026-05-07, repo CT160).
  - VolunteerMatch partnership (2024-08) [R].
- **Reading [I].** This is the strongest of the four on filings: DAF balances of $10.1m and revenue more than doubling. No funding after 2021 is visible. Either it is capital-efficient, or later money was raised without a Form D.

---

## 4. P-FAIL-03: what happened to acquired DAF codebases

Full rows: [`acquired-codebase-status-2026.csv`](../../data/mission-2026-11-14/acquired-codebase-status-2026.csv).

| Codebase | Acquirer, date | 2026 status | Key evidence |
|---|---|---|---|
| **Pinkaloo** | Ren, 2021-03-09 | **Brand site only; app front end retired [I]** | • [pinkaloo.com](https://www.pinkaloo.com/) says "Pinkaloo is Now Part of Ren", but its sign-up host `charitable.pinkaloo.com` is NXDOMAIN [F].<br>• App hosts (`connect`, `charities`, `setup`) have no named certificate after 2022 ([crt.sh](https://crt.sh/?q=%25.pinkaloo.com)) [F].<br>• `go.pinkaloo.com` redirects to reninc.com [F].<br>• Ren built its 2022 "Flex Giving Account" "through Pinkaloo" ([Ren, 2022-06-16](https://www.reninc.com/blog/rens-flex-giving-account-receives-2022-innovation-all-star-award-from-q2/)) [F] |
| **Amicus.io** | TIFIN, 2022-03 | **Merged; brand retired** | • `amicus.io` points at WP Engine/Flywheel: a certificate for `app.getflywheel.com`, and a 404 over HTTP [F].<br>• TIFIN Give is live: [ADV 2026-03-30](https://tifin.com/wp-content/uploads/Form-ADV-April-2026-1.pdf) shows $342.2m under advisement and $30.9m AUM at 2025-12-31, and `app.tifingive.com` redirects to `/auth` [F].<br>• Lineage: "powered by the acquisitions of Amicus.io and Giving Place" ([WealthManagement](https://www.wealthmanagement.com/philanthropy/assetmark-announces-strategic-collaboration-with-tifin-give)) [S] |
| **DonorFirst / DFX** (Crown) | Ren, 2016 | **Live core platform; renamed** | • 2026 certificates for `bofa`, `oak`, `boa-dr` and `metabase-dfx` under donorfirst.org, plus `*.donorfirstx.com` and `api-boa-prod` [F].<br>• Tenants include RCF, CFN, MS GIFT, BofA CGF and T. Rowe Price (repo).<br>• [`/dfx`](https://www.reninc.com/dfx) redirects to `/giving-platform` [F] |
| **iPhi** (Stellar) | Ren, 2023-01-20 | **Live separate stack; no longer marketed by name** | • 61 live `*.iphiview.com` hosts; 6 of 57 sponsors exited (10.5%) (repo census, reproduced in wave 11).<br>• [`/iphi-solution`](https://www.reninc.com/iphi-solution) returns 404 (2026-11-15), and the sitemap has no iPhi product page [F].<br>• Three NPT-family tenants moved within Ren to GivingPoint (repo) |
| **Vennfi** | Foundation Source, 2024-10-17 | **Live under the acquirer** | • Powers Charityvest and Foundation Source's turnkey private label ([release](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/)) [F].<br>• Certificates 2026-08 to 2026-10 for `portal.`, `*.p.platform.` and `guide.oneascent.` under charityvest.org ([crt.sh](https://crt.sh/?q=%25.charityvest.org)) [F].<br>• `vennfi.com` has no A record and no certificates [F] |

**Reading [I]:**
- The prior repo's worry about "acquisition for parts" holds only for the two consumer-channel startups, Pinkaloo and Amicus. Their brands and front ends are gone, and their code or teams were absorbed into the acquirer's bank and adviser products.
- The infrastructure buys survive as running stacks, in two cases still on their original hostnames: DonorFirst, iPhi and Vennfi.
- Ren runs at least three DAF stacks in 2026: DFX/"Giving Platform", iPhi, and the Ren-hosted GivingPoint/rengiving front end. It has stopped marketing two of the names. This is consistent with consolidation that has not yet happened in code.
- Customer migration is public only for iPhi. There, departures went mostly to other vendors (Foundant, akoyaGO, Give Interactive), not to DFX.

---

## 5. Limits

- Adviser-system lists for Black Diamond, Tamarac, Advyzon, Practifi, Plaid and Yodlee are not public. Absence there is not evidence.
- Orion's directory lists partners, not every custodial feed.
- Rule 13d-2 amendment duties were not tested against Clearlake's internal plans. "No proposal" means none on the public record.
- Philanthropi: the CT logs show certificate requests, not what was deployed. The DNS failure could be temporary.
- The Wayback Machine was unreachable, so the content of the last captured philanthropi.com page is unknown.
- Grapevine's site blocks automated reads. The role of GoodMatch Inc is unknown.
- Pinkaloo: a wildcard certificate valid 2025-04 to 2026-05 could have covered unnamed app hosts.

## 6. Source register

| ID | Source | Date | Used for |
|---|---|---|---|
| S1 | [Addepar portfolio-data-feeds directory](https://integrations.addepar.com/type/portfolio-data-feeds) | read 2026-11-15 | §1 |
| S2 | [Orion integrations](https://orion.com/integrations) (pages 0–10) | read 2026-11-15 | §1 |
| S3 | [eMoney connection update](https://blog.emoneyadvisor.com/best-practices/the-industry-leader-in-account-aggregation-emoney-connection-update/); [eMoney 2023-08-17 release](https://prnewswire.com/news-releases/emoney-advisor-adds-new-aggregation-connections-and-apis-for-advisors-and-end-clients-301903655.html) | 2023-04-17; 2023-08-17 | §1 |
| S4 | [InvestmentNews: Altruist adds DAFs](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481) | 2026-10-06 | §1 |
| S5 | [BridgeFT / Foundation Source release](https://www.bridgeft.com/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/); [InvestmentNews](https://www.investmentnews.com/fintech/foundation-source-expands-daf-platform-with-advisor-branded-multi-custodial-features/262225) | 2025-09-23 | §1 |
| S6 | [Business Wire: Orion and GiftingNetwork](https://www.businesswire.com/news/home/20250818952704/en/Orion-and-GiftingNetwork-Partner-to-Enhance-Charitable-Giving-Solutions-for-Advisors-and-Clients) (headline only) | 2025-08-18 | §1 [R] |
| S7 | Blackbaud EDGAR: [submissions](https://data.sec.gov/submissions/CIK0001280058.json); [DEF 14A 2026](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000009/blkb-20260418.htm); [DEF 14A 2025](https://www.sec.gov/Archives/edgar/data/1280058/000128005825000017/blkb-20250421.htm); [10-Q Q3-2026](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000032/blkb-20260930.htm); [8-K 2024-04-15](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000028/blkbex991unsolicitedpropos.htm); [8-K 2024-05-15](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000040/blkbex991unsolicitedpropos.htm); [8-K 2024-03-18](https://www.sec.gov/Archives/edgar/data/1280058/000128005824000020/blkb-20240318.htm); 8-Ks 2025-12-01/17 (links in §2) | 2024–2026 | §2 |
| S8 | Clearlake EDGAR: [submissions](https://data.sec.gov/submissions/CIK0001688282.json); [13F 2026-06-30](https://www.sec.gov/Archives/edgar/data/1688282/000090514826003721/form13fInfoTable.xml) | 2026-08-14 | §2 |
| S9 | IRS TEOS indexes [2025](https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv), [2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv); 990 XMLs (links in §3) | 2025–2026 | §3 |
| S10 | ProPublica API pages for EINs [45-5634144](https://projects.propublica.org/nonprofits/organizations/455634144), [87-2389502](https://projects.propublica.org/nonprofits/organizations/872389502), [87-1530516](https://projects.propublica.org/nonprofits/organizations/871530516) | read 2026-11-15 | §3 earlier years |
| S11 | Form D filer indexes: [Givinga](https://data.sec.gov/submissions/CIK0001720830.json), [Groundswell Giving](https://data.sec.gov/submissions/CIK0001899820.json), [Vennfi](https://data.sec.gov/submissions/CIK0001831751.json), [Pinkaloo](https://data.sec.gov/submissions/CIK0001793033.json) | 2019–2026 | §3, §4 |
| S12 | [Technical.ly: Philanthropi](https://technical.ly/startups/philanthropi-keith-leaphart/) | 2022-06-27 | §3.1 |
| S13 | crt.sh: [philanthropi.com](https://crt.sh/?q=%25.philanthropi.com), [pinkaloo.com](https://crt.sh/?q=%25.pinkaloo.com), [donorfirst.org](https://crt.sh/?q=%25.donorfirst.org), [donorfirstx.com](https://crt.sh/?q=%25.donorfirstx.com), [charityvest.org](https://crt.sh/?q=%25.charityvest.org) | read 2026-11-15 | §3.1, §4 |
| S14 | RDAP ([philanthropi.com](https://rdap.verisign.com/com/v1/domain/philanthropi.com), [vennfi.com](https://rdap.verisign.com/com/v1/domain/vennfi.com)); DoH lookups via [dns.google](https://dns.google/resolve?name=philanthropi.com&type=A) and cloudflare-dns.com | 2026-11-15 | §3.1, §4 |
| S15 | Ren: [Stellar acquisition](https://www.reninc.com/blog/ren-bolsters-philanthropic-tech-services-offerings-with-acquisition-of-stellar-technology-solutions/) (2023-01-20); [Flex Giving Account](https://www.reninc.com/blog/rens-flex-giving-account-receives-2022-innovation-all-star-award-from-q2/) (2022-06-16); [giving-platform](https://www.reninc.com/giving-platform/); [sitemap](https://www.reninc.com/sitemap_index.xml) | 2022–2026 | §4 |
| S16 | [Pinkaloo site](https://www.pinkaloo.com/); [amicus.io](http://amicus.io/); [charityvest.org](https://www.charityvest.org/); [app.tifingive.com](https://app.tifingive.com/) | read 2026-11-15 | §4 |
| S17 | [TIFIN Give Form ADV Part 2A](https://tifin.com/wp-content/uploads/Form-ADV-April-2026-1.pdf) | 2026-03-30 | §4 |
| S18 | [Foundation Source acquires Vennfi](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/) | 2024-10-17 | §4 |
| S19 | Repo: [queue-ren-iphi-attrition.md](queue-ren-iphi-attrition.md), [queue-vendor-channel-moves.md](queue-vendor-channel-moves.md), [queue-bank-programs-and-eft-providers.md](queue-bank-programs-and-eft-providers.md), [queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md) | 2026-11 | §3–4 |

## 7. Data dictionary

### `acquired-codebase-status-2026.csv` (one row per acquired codebase)

| Column | Meaning |
|---|---|
| `codebase_id` | AC01–AC05 |
| `codebase` | Product or platform name |
| `original_company` | Seller (SEC CIK where one exists) |
| `acquirer` | Buyer |
| `acquisition_date` | Closing or announcement date (ISO) |
| `acquisition_source_url` | Primary deal source |
| `status_2026` | One of:<br>• `live_core_platform_renamed`<br>• `live_separate_stack_marketing_retired`<br>• `live_under_acquirer`<br>• `merged_brand_retired`<br>• `brand_site_only_app_front_end_retired` |
| `successor_or_host` | Product or hosts it now runs as or inside |
| `evidence_summary` | What was observed (DNS, CT, HTTP, filings) |
| `evidence_urls` | Space-semicolon-separated URLs or repo paths |
| `evidence_date` | Observation date |
| `customer_migration_evidence` | Public evidence on client moves |
| `label` | F / I / S, per component |
| `confidence` | high / medium / low |
| `notes` | Caveats |

### `relationship-graph-edges-additions-17.csv`

These are the same columns as `relationship-graph-edges.csv`.
- IDs run EQ001–EQ015.
- `status` takes these values:
  - `confirmed`.
  - `rejected`, for a takeover proposal.
  - `reported`, for a headline only.

### `queue-proposals-batch32c.csv`

Format per `queue-proposals-README.md`. IDs are P-B32C-01 and P-B32C-02; `state` = open.
