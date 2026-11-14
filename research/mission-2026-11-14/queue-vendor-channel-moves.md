# Vendor and channel moves: Commonwealth Charitable Fund after the LPL conversion, GiftingNetwork vs Give at FFTC and CCT, and DAFgiving360 → Fidelity (P-PRC-05, P-PRC-04, P-NPT-03)

**Date:** 2026-11-14, which is the day Commonwealth client accounts move to LPL. **Status:** public sources only. I logged in nowhere, submitted no forms, requested no documents and contacted no one.

**Evidence labels:**
- **[F] first-party or filing:** a live page or document from the entity itself, or an IRS e-file return.
- **[R] reported:** press, a third-party site, or a search-index summary I could not open first-hand.
- **[I] inference:** my reading of the evidence. Every inference is marked.
- **[U] unknown:** no evidence either way.

**Data written:**
- [`data/mission-2026-11-14/relationship-graph-edges-additions-6.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-6.csv): edges EF001–EF006.
- [`data/mission-2026-11-14/queue-proposals-vendor-channel.csv`](../../data/mission-2026-11-14/queue-proposals-vendor-channel.csv): proposals P-VCM-01 to P-VCM-05.
- [`data/mission-2026-11-14/watchlist.csv`](../../data/mission-2026-11-14/watchlist.csv): 11 new checks. Their baseline snapshots are in `data/watchlist-snapshots/2026-11-14/` (see §5).

---

## 0. Headline answers

| Item | Answer | Confidence |
|---|---|---|
| **P-PRC-05** Commonwealth Charitable Fund after the LPL conversion | **Unchanged on conversion day. The sponsor is now first-party confirmed as Renaissance Charitable Foundation (RCF), and the administrator as RenPSG.**<br>- The program circular hosted on the CFN portal says the Commonwealth Charitable Fund "is a donor-advised fund (DAF) program offered by Renaissance Charitable Foundation Inc." and that RCF "has retained RenPSG … to perform certain accounting and administrative functions".<br>- On 2026-11-14 the portal still uses Commonwealth branding with the LPL legend, program code `CFNDAF` (id 680).<br>- The LPL channel page at Ren still sends LPL advisers to the generic `rcf.donorfirstx.com` (program `RCF`, id 103). That page was refreshed with LPL forms from July to November 2026 and does not mention Commonwealth.<br>- There is no sign of a vendor move: both programs run on the same sponsor and the same Ren stack. A merge would be a program-code and branding change, and none has been announced. | Sponsor and administrator confirmed [F]. "No change yet" confirmed as of 2026-11-14 [F]. Future merge [U] |
| **P-PRC-04** GiftingNetwork vs Give at FFTC and CCT | **Neither foundation's latest 990 names either vendor.**<br>- FFTC CY2024 lists 5 contractors, the lowest at $101,200. Give appears only in CY2023, at $654,500.<br>- CCT FYE 9/2025 lists 5 contractors with a floor of $735,318, and reports 40 contractors above $100k.<br>- **Live portals: both run on GiftingNetwork.** These are `daf.fftc.org` (plus the affiliate `fcjc.fftc.org`) and `donorportal.cct.org`.<br>- CCT's GiftingNetwork portal documents were created 2025-12-02, after Give's CCT production host (2025-06-11). This argues against an imminent Give cut-over at CCT [I].<br>- No other top-40 community foundation reachable by script shows GiftingNetwork. | Payees and portals [F]. Give/GN role split at CCT [U] |
| **P-NPT-03** DAFgiving360 → Fidelity $976.6m (FY2025) | **Still not attributable from public data.** Four new facts narrow it:<br>(1) Fidelity's Schedule B is fully "RESTRICTED" in the public XML.<br>(2) DAFgiving360 grew its account count by 14.5% in FY2025, which rules out a wholesale programme closure [I].<br>(3) Fidelity's own reports confirm that "a limited number of accounts with significant transfer activity" exist and are excluded from its analyses.<br>(4) Fidelity's CY2024 "outlier grant of $430 million" can only sit in its FY2025 Vanguard line, so the parallel Fidelity → Vanguard spike was most likely **one grant** [I, strong].<br>By analogy, the DAFgiving360 → Fidelity jump is most consistent with one or a few very large account moves [I]. No press, policy change or channel event explains it. | Amounts [F]. Composition [I] |

---

## 1. P-PRC-05: Commonwealth Charitable Fund (CFNDAF, id 680)

### 1.1 What the live sources show on 2026-11-14

| Observation | Evidence |
|---|---|
| The portal is live and Commonwealth-branded | `cfndaf.donorfirstx.com` shows "Welcome to your login experience for your Commonwealth Charitable Fund." The logo `/images/isp/CFNDAF/CW_2C_Logo_Web.png` has alt text "Commonwealth". The legend reads "Securities and advisory services offered through LPL Financial … Commonwealth is a trade name of LPL Financial." The page config is `"program_code": "CFNDAF", "program_id": "680"` ([portal](https://cfndaf.donorfirstx.com/)) [F] |
| The maintenance notice is platform-wide, not a CFN migration | "Standard site maintenance will be performed starting Friday, November 13th between … 8:00PM EST to 11:00PM EST" appears on both [cfndaf](https://cfndaf.donorfirstx.com/) and [rcf](https://rcf.donorfirstx.com/) [F]. Read it as routine DonorFirstX maintenance, not a CFN merge [I] |
| **Sponsor confirmed: RCF** | The CCF Program Circular is served at [`/pdf/CFNDAF/Program Circular.pdf`](https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf) (Last-Modified 2024-12-13; page footers "Renaissance Charitable Foundation 2021"). It says: "The Commonwealth Charitable Fund (CCF) is a donor-advised fund (DAF) program offered by Renaissance Charitable Foundation Inc. … The Foundation becomes the exclusive legal owner of the funds and assets in CCF." The minimum DAF balance is $2,000 [F]. This upgrades graph edge E034 from inferred to confirmed (**EF001**) |
| **Administrator confirmed: RenPSG** | The same circular, under "Service Provider", says: "The Foundation has retained RenPSG of Indianapolis, Indiana, to perform certain accounting and administrative functions." (**EF002**) [F] |
| Old user guide | The [CFNDAF Donor User Guide](https://cfndaf.donorfirstx.com/pdf/CFNDAF/CFNDAF%20Donor%20User%20Guide.pdf) is dated "DFX User Guide CFN 5/2022", with footer "Commonwealth Financial Network(R) … commonwealth.com" (Last-Modified 2023-04-10). It has not been rebranded [F] |
| State registry alias | The West Virginia charity registry lists "Commonwealth Charitable Fund" among RCF's other names, alongside SEI Giving Fund, Franklin Templeton, Wells Fargo Philanthropy Fund and others ([WV SOS](https://apps.sos.wv.gov/business/charities/detail.aspx?OrgID=3767)) [F] |
| The LPL channel is separate and active | Ren's [LPL page](https://www.reninc.com/lpl-rcf-daf/), "How to Open an LPL Renaissance Charitable Donor-Advised Fund", sends advisers to `rcf.donorfirstx.com` and does not mention Commonwealth. Its links show recent refreshes: LPL account-application examples (uploads/2026/07), an RCF corporate resolution dated 6.16.26, Pershing and Schwab data-feed guides (2026/09), a "DAF to DAF Transfer" explainer (2026/11, PDF created 2026-10-29) and an online-application guide (PDF created 2026-11-13) [F] |
| The LPL circular is generic RCF | The [LPL DAF Program Circular](https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf) is byte-identical to the 2025/09 upload (PDF created 2023-10-11). It describes the "Renaissance Charitable Gift Fund", portal `rcf.donorfirstx.com`, with a minimum initial contribution of **$5,000**. It never mentions Commonwealth [F] |
| `rcf.donorfirstx.com` | Program `RCF`, id 103, RCF logo, and no Commonwealth or LPL text ([portal](https://rcf.donorfirstx.com/)) [F] |
| CT logs | `*.donorfirstx.com` is a wildcard certificate. The named hosts are only aef-stg, boa-*, msgift-uat, auth-*, cdn-* and help, so **CT cannot reveal a CFN or LPL tenant change** ([crt.sh](https://crt.sh/?q=%25.donorfirstx.com)) [F] |

### 1.2 Conversion timing and channel context

- One adviser's client roadmap says "November 13: Commonwealth and LPL formally integrate. November 14: Your accounts and assets move to LPL, and you will receive new account numbers" ([Pickler Wealth Advisors](https://www.picklerwealthadvisors.com/post/your-transition-roadmap)) [R]. Citywire reported the 14 November date from a document on 2026-08-24 (Google News item in snapshot `rss-lpl-commonwealth.json`) [R].
- LPL guided asset retention down to 83% on 2026-10-28 ([WealthManagement](https://www.wealthmanagement.com/ibd-news/lpl-lowers-commonwealth-asset-retention-to-83)) [R]. It said the conversion was about two weeks away and the builds were in final testing [R].
- None of the adviser conversion materials I could read mentions DAF, charitable or Renaissance accounts ([Pickler blog 8](https://www.picklerwealthadvisors.com/post/blog-8-how-will-i-see-my-accounts-online-after-november-14)) [R].
- Commonwealth's revenue-sharing disclosure is no longer reachable first-hand. `commonwealth.com/for-clients/disclosure/revenue-sharing` now 301-redirects to `lpl.com/commonwealth.html`, which returned 403. The Wayback API reports a 200 capture on 2026-09-09, but web.archive.org was unreachable from this sandbox. A search-index summary says it described RCF's "affiliated administrative entity" paying Commonwealth "up to 5 basis points … or $5 per quarter" [R, not verified].

### 1.3 Reading

- **Persist, merge or move vendor?**
  - **Persist (as of today) [F].**
  - **Move vendor: very unlikely [I].** The sponsor (RCF), the administrator (RenPSG) and the platform (DonorFirstX) are the same as LPL's own RCF channel. A vendor move would mean LPL replacing RCF/Ren for both channels, and nothing points that way: Ren refreshed LPL forms from July to November 2026.
  - **Merge into the RCF/LPL program: possible later [I].** The terms differ: a $2,000 minimum balance under CCF against a $5,000 minimum initial contribution under the LPL circular. Advisers are being moved off Advisor360° onto ClientWorks ([WealthManagement](https://www.wealthmanagement.com/advisor-support-platforms/lpl-to-move-commonwealth-advisors-to-clientworks)) [R]. A merge would most likely be a program-code and branding consolidation inside RCF, invisible in 990s.
- **What to watch:**
  - the CFN portal redirecting, or the `/pdf/CFNDAF/` assets disappearing (`http-cfn-portal`);
  - Ren's LPL page adding Commonwealth language (`http-ren-lpl`);
  - RCF's CY2025–CY2026 returns (`irs-rcf`). RCF's CY2025 return was not yet in the IRS index on 2026-11-14.
- **The real risk to Ren is attrition [I].** Commonwealth advisers who leave LPL may move clients' DAFs by account-closing grant (P-VCM-05).

---

## 2. P-PRC-04: GiftingNetwork vs Give Interactive at FFTC and CCT

### 2.1 Latest 990s, Part VII-B

| Filer | Latest return in IRS index (2026-11-14) | Contractors >$100k (count) | Listed contractors (lowest) | Give Interactive | GiftingNetwork | IT expense (Part IX line 11g) |
|---|---|---|---|---|---|---|
| **Foundation for the Carolinas** (EIN 56-6047886) | CY2024, object 202543219349306689 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349306689_public.xml); [ProPublica](https://projects.propublica.org/nonprofits/organizations/566047886/202543219349306689/full)) | 10 | 5 listed: James Cohan Gallery $265,000 … Loyd Visuals $101,200 | **absent** | **absent** | $1,918,972 (CY2023: $2,387,295) |
| FFTC, prior year | CY2023, 202433209349318318 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml)) | 14 | — | **GIVE INTERACTIVE LLC, Overland Park KS, "SOFTWARE", $654,500** | absent | $2,387,295 |
| **Chicago Community Trust** (EIN 36-2167000) | FYE 9/2025, 202632239349302058 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632239349302058_public.xml)) | **40** | Northern Trust $4,438,559 … JP Morgan Chase $735,318 | absent | absent | $1,782,037 |

Notes:
- **FFTC.** The return counts 10 contractors above $100k but lists 5, the lowest at $101,200. Strictly, that would put contractors 6–10 between $100,000 and $101,200, which is implausible. More likely the five listed are not a strict top five [I]. So FFTC's CY2024 return **does not rule out** a Give or GiftingNetwork payment above $100k. It only shows that none was among the five listed.
  - Give's FFTC tenants lapsed in Feb 2024 ([give-interactive-displacement §2](queue-give-interactive-displacement.md)).
  - The fall in IT spend from $2.39m to $1.92m fits the loss of a $654.5k software contract, but is not proof of it [I].
  - The GiftingNetwork go-live (2026-07-01) will first appear in the CY2026 return, due in 2027. The CY2025 return was not yet indexed (watch `irs-fftc`).
- **CCT.** With 40 contractors above $100k and a $735k listing floor, **Part VII-B cannot show either vendor at CCT.** Earlier repo work found RenPSG at CCT only in FY2018–FY2020, at $1.31m–$1.60m (edge EB004).

### 2.2 Live portal hosts

| Sponsor | Donor login | Platform evidence | Host age |
|---|---|---|---|
| FFTC | `fftc.org` links "MyFFTC Login", which goes to [daf.fftc.org](https://daf.fftc.org/) and then `/m/login` | Footer "Powered by GiftingNetwork", logo `/ma/images/logo_xs.png` [F]. GiftingNetwork release: running "since July 1, 2026" ([PRLog, 2026-09-23](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html)) [F, vendor] | First certified 2026-04-13 ([crt.sh](https://crt.sh/?q=daf.fftc.org)) |
| Foundation For The Charlotte Jewish Community (FFTC affiliate) | `fftc.org` links "MyFCJC login": [myfcjc.org](https://myfcjc.org/) redirects to `fcjc.fftc.org/m/login` | "Powered by GiftingNetwork" [F] | First certified 2026-04-13, the same day as daf.fftc.org ([crt.sh](https://crt.sh/?q=fcjc.fftc.org)) |
| CCT | [donorportal.cct.org](https://donorportal.cct.org/) → `/m/login` | "Powered by GiftingNetwork" [F]. The [FAQ](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf) and [User Guide](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-User-Guide.pdf) were created **2025-12-02** (PDF metadata) [F] | Host certified since **2023-10-06** ([crt.sh](https://crt.sh/?q=donorportal.cct.org)). Host age only: whether it ran GiftingNetwork from day one is [U] |
| CCT on Give | Tenant `cct`: sandbox 2024-08-12, production 2025-06-11, SFTP 2026-11-03 (repo CT work, [give-interactive-displacement §2](queue-give-interactive-displacement.md)) | No donor-facing link to Give was found [F] | — |

**Reading on CCT [I]:**
- CCT produced new GiftingNetwork donor documentation six months after its Give production host was certified, and Give's SFTP host for CCT was certified only in November 2026.
- **Coexistence** fits this better than an imminent replacement: Give as ledger or back office feeding a GiftingNetwork front end. GiftingNetwork advertises that it is "Compatible with FIMS, FoundationPower, and any third-party XML client" and that fund data "flow from your accounting system" ([GiftingNetwork portals](https://www.giftingnetwork.com/portals.html)) [F].
- **Replacement** is not ruled out. This is P-VCM-01.

### 2.3 Other large community foundations

- **990 contractor lines.** In the 1,512-sponsor harvest ([form990-contractors-harvest-full.csv](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv)) the vendors appear only as follows:
  - **Give Interactive:** FFTC CY2023 only.
  - **GiftingNetwork:** Jewish Community Foundation of San Diego only, FY6/2022–FY6/2025, at $171,500–$359,535 a year ("custodian for investments and back office"; [XML FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611349349307506_public.xml)) [F].
- **Portal crawl (2026-11-14).** I fetched the home pages of the 40 largest community foundations by DAFRC FY2024 DAF assets and followed their login links (script in the scratchpad; results summarised here).
  - **24 home pages were reachable.** Their donor or grant portals point to:
    - Foundant CommunitySuite (`*.fcsuite.com`: Columbus, CF Greater Atlanta, Tampa Bay, Greater Cincinnati, NH, Milwaukee) [F host; vendor name I];
    - Ren/Stellar iPhi (Minneapolis, Saint Paul & Minnesota, Cleveland) [F];
    - Salesforce Experience Cloud (Oregon CF, California CF, SVCF `donor.siliconvalleycf.org/s/`, Arizona) [F host; I platform];
    - Akoya GOfund (East Bay CF, `gofund.akoyago.com/eastbay`) [F];
    - Microsoft Power Pages (Seattle) [F host];
    - SmartSimple and other grant-only systems.
  - **15 returned 403 to scripts:** GKCCF, GHCF, CFNJ, Denver, San Diego, Tulsa, SFF, CFT, Pittsburgh, CFMT, OC-CF, Dallas, CICF, Kalamazoo and Greater Memphis.
  - **No GiftingNetwork signature** appeared outside CCT and FFTC/FCJC, and no reachable site linked to a Give Interactive host [F within coverage].
- **CT logs.** `giftingnetwork.com` certifies only `www` and `support` ([crt.sh](https://crt.sh/?q=%25.giftingnetwork.com)). GiftingNetwork portals sit on client domains, so CT search by vendor domain cannot enumerate its clients.
- **Vendor claims.** GiftingNetwork's own portal page shows only sample or mock sponsor names and gives no client count ([portals](https://www.giftingnetwork.com/portals.html)) [F].

**Bottom line [I]:**
- GiftingNetwork has two top-15 community foundations live (CCT $4.65bn, FFTC $2.95bn DAF assets, FY2024 DAFRC) and one 990-visible back-office client (JCF San Diego).
- Give holds the bigger national-sponsor pipeline (Vanguard, ImpactAssets, WaterStone and others) but has lost FFTC and has not displaced GiftingNetwork at CCT's front end.
- The two vendors meet at community foundations; elsewhere they are not substitutes.

---

## 3. P-NPT-03 (second attempt): DAFgiving360 → Fidelity $976.6m in FY2025

### 3.1 The facts as filed (both sponsors' fiscal years end 30 June)

| | DAFgiving360 FY2024 | DAFgiving360 FY2025 | Fidelity FY2024 | Fidelity FY2025 |
|---|---|---|---|---|
| Return (XML) | [202541069349300729](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml) | [202611199349300601](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml) | [202521349349310887](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml) | [202601389349301700](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) |
| DAF accounts (Sch D) | 112,188 | **128,497 (+14.5%)** | 204,614 | 224,884 (+9.9%) |
| Contributions (Part VIII 1h) | $9.31bn | $11.11bn | $15.93bn | $26.47bn |
| of which noncash | $6.27bn | $6.90bn | $9.97bn | $17.93bn |
| Grants (Part I line 13) | $6.62bn | $8.87bn | $12.69bn | $15.31bn |
| DAFgiving360 → Fidelity (Sch I) | $127.7m | **$976.6m** (one line, cash, "PUBLIC, SOCIETAL BENEFIT") | — | — |
| Fidelity → DAFgiving360 (Sch I) | — | — | $100.9m | $117.8m |
| Largest single Schedule I line | — | Fidelity $976.6m; next is Johns Hopkins $272.4m | JHU $273.1m | Vanguard Charitable $480.1m |

Derived:
- The FY2025 increment of $848.9m equals 37.7% of DAFgiving360's $2.25bn grant growth [F arithmetic].
- The $976.6m equals 2.4% of DAFgiving360's FY2024 year-end DAF value ($40.94bn) [F arithmetic].
- If Fidelity booked the inflow as a cash contribution, it would be 11.4% of Fidelity's FY2025 cash contributions of $8.54bn [I: booking treatment not disclosed].

### 3.2 Routes tried this pass

| Route | Result |
|---|---|
| Fidelity Schedule B in the public XML | Present but every field is `RESTRICTED`: contributor, amount and type (FY2024 and FY2025) [F]. **Dead end.** |
| Fidelity Schedule M (noncash) | DAF-to-DAF grants were cash on the grantor side, so Schedule M is not informative [I] |
| Fidelity giving reports | The [2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) (CY2024, p.19) says "One outlier grant of $430 million was removed …" and "A limited number of accounts with significant transfer activity were excluded from the analysis." The [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) (CY2025, p.12) says "Significant outlier granting totaling $727 million was removed …" [F]. Neither names inbound transfers |
| Locating the $430m outlier | It is CY2024, so it falls in Fidelity's FY2024 (Jan–Jun) or FY2025 (Jul–Dec). Fidelity aggregates Schedule I by recipient. The FY2024 maximum line is $273.1m, and the only FY2025 line ≥ $430m is **Vanguard Charitable, $480.1m** (FY2024 $21.7m). Schedule F's largest foreign grant is $10.05m [F]. **The outlier was therefore most likely a single Fidelity → Vanguard DAF-to-DAF grant in Jul–Dec 2024 [I, strong]** (edge EF005). It answers part of P-STF-02/P-STF-03 and shows that single-account moves of about $0.4–0.5bn occur between national sponsors |
| DAFgiving360 policy, fee or programme changes | The rebrand from Schwab Charitable took effect 2024-06-18, the eve of FY2025. Schwab said "no changes are being made to account structures" ([Schwab press release](https://pressroom.aboutschwab.com/press-releases/press-release/2024/Schwab-Charitable-Celebrates-25-Years-of-Donor-Advised-Giving-with-New-Brand/default.aspx)) [R via search summary]. I found no 2024–25 change to minimums or fees, and no programme closure. The account count rose 14.5%, which is inconsistent with a programme exit [I]. dafgiving360.org returns 403 to this sandbox |
| DAFgiving360 FY2025 results release | Headline "$8.9 billion in grants to charities" for FY2025 ([dafgiving360.org](https://dafgiving360.org/press-release/fiscal-year-2025-results), 403 here; [InvestmentNews](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994)) [R]. That is about Part I line 13 ($8.87bn), so the public "grants to charities" figure appears to **include** about $1.55bn of grants to other DAF sponsors [I]. Unlike Fidelity, no outlier exclusion is stated in the coverage I could reach [U] |
| Adviser-channel timing (Schwab–TD Ameritrade) | Schwab finished moving the last TD Ameritrade client group in Q2 2024, around May ([American Banker](https://www.americanbanker.com/list/charles-schwab-celebrates-successful-uneventful-1-3-trillion-td-ameritrade-account-transition); [Financial Advisor](https://www.fa-mag.com/news/schwab-execs-hail-success-of-td-integration-74523.html)) [R]. That would move assets **into** Schwab, not out to Fidelity. I found no link to DAF outflows [I] |
| Fidelity custody policy | Fidelity's $100m RIA custody minimum, with wind-down by 2027-06-30, was announced in 2026 ([InvestmentNews](https://www.investmentnews.com/ria-news/fidelitys-100m-ria-custody-minimum-impacts-almost-1000-firms/268505)) [R]. It postdates FY2025 and so cannot explain FY2025, but it is a natural experiment for the reverse flow (P-VCM-04) |
| Press on large account moves | The Chronicle (2026-03-06) covers 2023 flows only, and Fidelity's spokesman gives only generic reasons: local expertise, a values-based move, international grants ([Chronicle](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/)) [R]. **No press names the FY2025 transfer** |

### 3.3 Reading [I]

Three things make "one or a few very large accounts" the leading explanation:
- the steady ~$125m base in FY2022–FY2024;
- a single aggregated cash line, with no programme closure and with growing DAFgiving360 account counts;
- Fidelity's first-party admission that a "limited number of accounts with significant transfer activity" exist, plus the same-year $430m single grant out of Fidelity.

A custody-driven move is a plausible mechanism but unevidenced: an RIA leaving Schwab custody for Fidelity would take its DAF clients to Fidelity Charitable. "Many small donor moves" is the least likely explanation: it would need a roughly 7.6× jump in donor-initiated transfers in one year with no visible cause.

**Status:** answer remains [I], now with a first-party anchor for the outlier mechanism. The decisive test is DAFgiving360's FYE 6/2026 return (`irs-dafgiving360`). If the line reverts to about $125m, that supports a one-off.

---

## 4. Corrections and qualifications to repo statements

| Repo statement | Change |
|---|---|
| E034 "CFN sponsor = RCF (inferred)" | **Confirmed** by the CCF Program Circular (EF001). The administrator is RenPSG (EF002) |
| queue-processor-economics §6 "CFN … Both programs are Ren/RCF (CFN's sponsor is inferred)" | Sponsor now confirmed [F]. The programs differ in minimums ($2,000 CCF balance vs $5,000 RCF/LPL initial contribution) |
| queue-processor-economics §5 "FFTC and CCT returns after go-live are not yet filed" | Still true. The latest returns (FFTC CY2024, CCT FYE 9/2025) name neither vendor, and CCT's Part VII-B threshold makes absence uninformative |
| queue-state-filings §5.2 "I found no press or filing that names the FY2025 transfer" | Still true. Add: Fidelity's report language confirms the existence of large transfer accounts, and the Fidelity → Vanguard $480.1m line most likely contains a single $430m grant |

---

## 5. Watchlist additions (`data/mission-2026-11-14/watchlist.csv`)

The script was run with `--only` for the 11 new checks. All are baselines dated 2026-11-14 in `data/watchlist-snapshots/2026-11-14/` and the report `data/watchlist-snapshots/reports/2026-11-14.md`.

| check_id | Type | Baseline |
|---|---|---|
| http-cfn-portal | http | 200. Commonwealth welcome text, LPL legend, maintenance note, `/pdf/CFNDAF/` link |
| http-rcf-portal | http | 200. No Commonwealth or LPL text |
| http-ren-lpl | http | 200 (urllib). No Commonwealth text; 2026/07–2026/11 uploads listed |
| rss-lpl-commonwealth | rss | 16 items through 2026-11-13 ("LPL Financial Nears Commonwealth Platform Conversion") |
| irs-rcf | irs_index | Latest CY2024 (202543189349301959). CY2025 not yet indexed |
| http-cct-portal | http | "Powered by GiftingNetwork" |
| http-fftc-portal | http | "Powered by GiftingNetwork" |
| irs-fftc | irs_index | Latest CY2024. CY2025 not indexed |
| irs-cct | irs_index | Latest FYE 9/2025. FYE 9/2026 watched |
| irs-dafgiving360 | irs_index | Latest FYE 6/2025. FYE 6/2026 watched |
| irs-fidelity | irs_index | Latest FYE 6/2025. FYE 6/2026 watched |

---

## 6. Access log and dead ends

- **403 to curl/urllib:** `www.commonwealth.com` (redirects to `lpl.com/commonwealth.html`), `lpl.com`, `cct.org` home, `dafgiving360.org`, BusinessWire, and 15 community-foundation home pages (§2.3).
- **Reached by WebFetch:** `reninc.com/lpl-rcf-daf/`.
- **Unreachable:** web.archive.org (connection reset). Wayback availability API only.
- **Not attempted (out of scope or prohibited):** any login, NY AG registry search, document requests, contacting LPL, Ren, CCT, FFTC, GiftingNetwork or Give.

---

## 7. Source register

| # | Source | Date | Used for |
|---|---|---|---|
| S1 | [cfndaf.donorfirstx.com](https://cfndaf.donorfirstx.com/) | live 2026-11-14 | CFN branding, program code, legend |
| S2 | [CCF Program Circular](https://cfndaf.donorfirstx.com/pdf/CFNDAF/Program%20Circular.pdf) | modified 2024-12-13 | RCF sponsor; RenPSG administrator; $2,000 minimum |
| S3 | [CFNDAF Donor User Guide](https://cfndaf.donorfirstx.com/pdf/CFNDAF/CFNDAF%20Donor%20User%20Guide.pdf) | 5/2022 (modified 2023-04-10) | Not rebranded |
| S4 | [rcf.donorfirstx.com](https://rcf.donorfirstx.com/) | live 2026-11-14 | RCF program id 103 |
| S5 | [Ren LPL page](https://www.reninc.com/lpl-rcf-daf/) | © 2026, live | LPL channel; refreshed uploads |
| S6 | [LPL DAF Program Circular](https://www.reninc.com/wp-content/uploads/2026/05/2309-RCF-FRM-DAF-LPLCircular.pdf) | PDF 2023-10-11 | $5,000 minimum; generic RCF |
| S7 | [Ren DAF-to-DAF explainer](https://www.reninc.com/wp-content/uploads/2026/11/Client-Explainer-Transfer-Existing-DAF.pdf); [online application guide](https://www.reninc.com/wp-content/uploads/2026/11/Donor-Portal-DAF-Application.pdf) | 2026-10-29; 2026-11-13 | Channel activity |
| S8 | [WV SOS charity detail, RCF](https://apps.sos.wv.gov/business/charities/detail.aspx?OrgID=3767) | live 2026-11-14 | RCF alias list |
| S9 | [crt.sh %.donorfirstx.com](https://crt.sh/?q=%25.donorfirstx.com) | 2026-11-14 | Wildcard; no tenant names |
| S10 | [Pickler roadmap](https://www.picklerwealthadvisors.com/post/your-transition-roadmap); [Pickler blog 8](https://www.picklerwealthadvisors.com/post/blog-8-how-will-i-see-my-accounts-online-after-november-14) | 2026-09-22; 2026-11-04 | Conversion dates |
| S11 | [WealthManagement: 83% retention](https://www.wealthmanagement.com/ibd-news/lpl-lowers-commonwealth-asset-retention-to-83); [ClientWorks move](https://www.wealthmanagement.com/advisor-support-platforms/lpl-to-move-commonwealth-advisors-to-clientworks) | 2026-10-28; 2026-05-29 | Conversion context |
| S12 | FFTC 990 [CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543219349306689_public.xml), [CY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349318318_public.xml) | filed 2025, 2024 | Part VII-B; IT expense |
| S13 | CCT 990 [FYE 9/2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202632239349302058_public.xml) | filed 2026 | Part VII-B; IT expense |
| S14 | [daf.fftc.org](https://daf.fftc.org/); [myfcjc.org](https://myfcjc.org/); [fftc.org](https://www.fftc.org/) | live 2026-11-14 | GiftingNetwork portals |
| S15 | [donorportal.cct.org](https://donorportal.cct.org/); [CCT portal FAQ](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-FAQ.pdf); [User Guide](https://donorportal.cct.org/ma/docs/cct/CCT-Donor-Portal-User-Guide.pdf) | live; PDFs 2025-12-02 | CCT portal and timing |
| S16 | crt.sh: [daf.fftc.org](https://crt.sh/?q=daf.fftc.org), [fcjc.fftc.org](https://crt.sh/?q=fcjc.fftc.org), [donorportal.cct.org](https://crt.sh/?q=donorportal.cct.org), [%.giftingnetwork.com](https://crt.sh/?q=%25.giftingnetwork.com) | 2026-11-14 | Host ages |
| S17 | [PRLog: GiftingNetwork live at FFTC](https://www.prlog.org/13172546-giftingnetworks-donor-portal-live-at-foundation-for-the-carolinas.html); [GiftingNetwork portals](https://www.giftingnetwork.com/portals.html) | 2026-09-23; live | Vendor claims |
| S18 | [JCF San Diego 990 FY6/2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611349349307506_public.xml) | 2026 | GiftingNetwork payee |
| S19 | DAFgiving360 990s [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml), [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml) | filed 2025, 2026 | Sch D, Sch I, Sch O |
| S20 | Fidelity Charitable 990s [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml), [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) | filed 2025, 2026 | Sch B (restricted), D, F, I |
| S21 | [Fidelity 2025 Giving Report](https://fidelitycharitable.org/content/dam/fc-public/docs/insights/2025-giving-report.pdf) p.19; [2026 Giving Report](https://www.fidelitycharitable.org/content/dam/fc-public/docs/insights/2026-giving-report.pdf) p.12 | 2025-02; 2026-04 | Outlier and transfer-account language |
| S22 | [Schwab rebrand release](https://pressroom.aboutschwab.com/press-releases/press-release/2024/Schwab-Charitable-Celebrates-25-Years-of-Donor-Advised-Giving-with-New-Brand/default.aspx); [DAFgiving360 FY2025 results](https://dafgiving360.org/press-release/fiscal-year-2025-results); [InvestmentNews](https://www.investmentnews.com/practice-management/dafgiving360-donors-boost-2025-grants-to-nearly-10b/264994) | 2024; 2025-07-29 | Policy and headline grants (via search summaries; first-party pages 403) |
| S23 | [American Banker: TD Ameritrade transition](https://www.americanbanker.com/list/charles-schwab-celebrates-successful-uneventful-1-3-trillion-td-ameritrade-account-transition); [Financial Advisor](https://www.fa-mag.com/news/schwab-execs-hail-success-of-td-integration-74523.html) | 2024 | Channel timing |
| S24 | [InvestmentNews: Fidelity $100m RIA minimum](https://www.investmentnews.com/ria-news/fidelitys-100m-ria-custody-minimum-impacts-almost-1000-firms/268505); [FINTRX](https://www.fintrx.com/blog/the-fidelity-100m-threshold-by-the-numbers-which-independent-rias-are-affected) | 2026 | P-VCM-04 |
| S25 | [Chronicle of Philanthropy, 2026-03-06](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/) | 2026-03-06 | No FY2025 attribution |
| S26 | [daf-to-daf-flows-990.csv](../../data/mission-2026-11-14/daf-to-daf-flows-990.csv); [form990-contractors-harvest-full.csv](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv) | repo | Flow and payee baselines |

---

## 8. Data dictionary

### `relationship-graph-edges-additions-6.csv`
Same columns as `relationship-graph-edges.csv`.

| Field | Meaning |
|---|---|
| edge_id | `EF001`–`EF006` (this workstream) |
| source_entity / source_type, target_entity / target_type | Node names and types, reusing existing vocabulary (`daf_sponsor`, `technology_admin_vendor`, `technology_vendor`, `branded_daf_program`) |
| relationship_type | `sponsor_of`, `administers`, `technology_provider` or `grant_to` (a Schedule I aggregate from grantor to recipient) |
| status | `confirmed` only where a first-party document, live first-party page or IRS e-file states it. Inferences sit in `notes` and are marked [inference] |
| evidence_summary | Quote or filed figure |
| source_url | Primary source |
| source_date | Document or return date (PDF Last-Modified, release date or FYE) |
| accessed_date | 2026-11-14 |
| notes | Upgrades or links to earlier edges, host ages, and inferences |

### `queue-proposals-vendor-channel.csv`
The columns follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md): `question_id` (`P-VCM-NN`), question, area, importance/gap/commercial/availability/effort (1–5), p_change (0–1), depends_on, breadth_gap, state (`open`), assigned_to (blank), conclusion_affected, proposed_by, rationale and evidence_pointer.

### New `watchlist.csv` rows
The columns are as documented in `scripts/mission_watchlist.py`:
- `check_id`, `check_type` (`http`, `rss` or `irs_index`), `entity` and `queue_items`;
- `target`: a URL, RSS URL or EIN;
- `link_regex` and `watch_regex`, for the signals;
- `params`: for `irs_index`, `min_tax_period` and `types`;
- `notes`: the baseline and what counts as a change.
