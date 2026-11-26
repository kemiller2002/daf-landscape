# NPT–Ren scope, DAFgiving360 evidence, sponsor 990 governance and miscellaneous queue items

**Queue items:** P-QCAL-01, P-QCAL-02, P-AGA-01, P-WAT-01, P-AGA-04, P-CMP-05, P-AGA-02. Full text is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

**Date:** 2026-11-14. **Method:** public sources only.
- **IRS filings:** IRS e-file returns were located through the TEOS index (`index_2024.csv`–`index_2026.csv`). The 2026 index was last modified 2026-10-21. The XML was read from the GivingTuesday data-lake mirror, following the access pattern in [`scripts/mission_990_contractors.py`](../../scripts/mission_990_contractors.py).
- **Web pages:** live first-party pages were fetched with curl.
- **Limits:** no log-ins, no accounts, no contact with anyone, no authenticated pages.

**Quotes and labels:** quotes are verbatim and at most 40 words. Evidence labels follow [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md):
- **confirmed:** a first-party page or filing states it.
- **inferred:** convergent indirect evidence.
- **unknown:** no evidence either way.

**Files written:**
- [`data/mission-2026-11-14/sponsor-governance-990-xml.csv`](../../data/mission-2026-11-14/sponsor-governance-990-xml.csv): 14 sponsor-years.
- [`data/mission-2026-11-14/relationship-graph-edges-additions-5.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-5.csv): EE001–EE012.
- [`data/mission-2026-11-14/queue-proposals-npt-misc.csv`](../../data/mission-2026-11-14/queue-proposals-npt-misc.csv): P-NPT-01 to P-NPT-06.

---

## 0. Answers

| Item | Answer (2026-11-14) | Label |
|---|---|---|
| **P-QCAL-01** NPT–Ren scope | **Most likely more than a front end.** Ren appears to supply the GivingPoint portal, its application/API layer and, on convergent evidence, the iPhi sub-ledger. NPT itself performs administration (310 staff).<br>New evidence:<br>(1) NPT's Terms of Use name a donor portal "DonorView", which is the iPhi donor-portal name.<br>(2) The Ren-built GivingPoint API serves fund activity, balances, grant payments, statements and investments.<br>(3) Ren's status page for NPT is named "iPhi".<br>No contract, fee or first-party statement exists. Recommendation: **merge the A1 "NPT GivingPoint (sponsor-built)" row into Ren for technology, but not for administration.** | inferred (ledger); confirmed (portal/hosting) |
| **P-QCAL-02** DAFgiving360 | (a) **Rail:** the latest readable Program Policies (Dec 2024) document **checks and wires only**. No EFT/ACH option for nonprofits was found, and every dafgiving360.org page returned 403.<br>(b) **Audited statements:** still not readable. The FY2025 990 confirms an audit on a separate basis and an audit committee, and states that the statements are posted on the website. The auditor is not named.<br>(c) **Transfers and history:** the policies contain no outbound DAF-to-DAF transfer clause and no export clause; grant history is viewable online. In practice, the FY2025 Schedule I shows **about $1.35bn granted to seven other DAF sponsors, including $976.6m to Fidelity Charitable**. | confirmed (policies, 990); unknown (2025–26 EFT) |
| **P-AGA-01** 990 XML governance | All seven sponsors file **audited** statements. Six report an audit committee; GS Gives' full board oversees the audit instead.<br>Auditor named:<br>- by service text only: **PwC** (GS Gives, "AUDIT SERVICES")<br>- inferred: **RSM** (NPT) and **EY** (MS GIFT)<br>- not named: DAFgiving360, GS PWM, BofA and AEF<br>Related-party administrators: **Schwab** (DAFgiving360, Schedule L "FOUNDER", $11.43m) and Goldman affiliates (GS PWM, via VII-B, no Schedule L). Unaffiliated administrators: **RenPSG** (MS GIFT) and **CAF America** (GS Gives). **No return names Ren, Stellar, NPact or Give Interactive at NPT, GS PWM or BofA.** | confirmed |
| **P-WAT-01** ImpactAssets → GiveClear $86.0m | **Still inferred; it cannot be confirmed from filings available today.** GiveClear's CY2025 990 is not in the IRS index. Two new facts complicate the reading:<br>(1) GiveClear reported **228 DAFs at both end-2023 and end-2024**, although DAF assets rose from $24.8m to $215.3m.<br>(2) DAFgiving360 also granted GiveClear **$29.7m** in FY2025.<br>The size of the AssetMark program remains **unknown**; the only bound is all of GiveClear ($215.3m at end-2024). | inferred / unknown |
| **P-AGA-04** Chariot terms | The **DAFpay Provider Addendum is now public** (updated 2026-10-14). Its key terms:<br>- providers authorize Chariot "acting on behalf of DAF Donors" to create and submit grant requests<br>- the provider "alone" reviews and approves each request<br>- Chariot disclaims donors' acts and errors<br>- it says nothing about automated or agent-driven sessions<br>The **Donor Terms** page still serves the homepage to automated fetch; only a search snippet (effective 2025-01-01) is available. | confirmed (addendum); unknown (donor terms text) |
| **P-CMP-05** adjacent rails | On published terms, workplace-giving intermediaries **deduct fees from the nonprofit side** and DAF sponsors do not:<br>- **Benevity:** 2.99% Cause Support Fee, plus a manual-check fee of the higher of $35 or 8% (cap $125) after two checks, and a $100 check threshold.<br>- **YourCause/Blackbaud Giving Fund:** timing "set by the client", "most" monthly or quarterly.<br>- **PayPal Giving Fund:** no fee, but 15–45 days.<br>- **Fidelity Charitable:** EFT at no fee.<br>- **DAFgiving360:** check in 7–10 business days, no fee.<br>In the repo corpus, Benevity has the most nonprofit grant-delay complaints (9 of the 10 nonprofit grant_delay records). | confirmed (terms); corpus counts (selection-biased) |
| **P-AGA-02** AI agent as a contract role | **No.** Re-checked on 2026-11-14:<br>- the Daffy Member Agreement is still dated 2025-11-11 with no agent or MCP clause<br>- the Endaoment T&C (2026-08-12) have no agent role<br>- the Chariot Provider Addendum has no agent role<br>- no sponsor policy found defines an AI agent<br>**New:** Chariot runs an MCP server for nonprofit Gift Processing data. It is OAuth-scoped to the organization's account, and its terms carry no agent role. | confirmed absence (documents read) |

---

## 1. P-QCAL-01: is Ren NPT's front end only, or also its ledger?

### 1.1 Evidence

| # | Test | Finding | Label | Source |
|---|---|---|---|---|
| 1 | NPT's own description of its portals | NPT's Terms of Use (last updated October 29, 2026) let users visit "one of our donor portal websites, NPT GivingPoint, GivingPoint or DonorView (collectively, 'Donor Portal') to manage your donor advised fund" | confirmed | [nptrust.org Terms/Privacy](https://www.nptrust.org/privacy-policy/) |
| 2 | Is "DonorView" an iPhi module name? | The Minneapolis Foundation's iPhi log-in (`tmf.iphiview.com`) links to a "DonorView" FAQ. That FAQ says grant status "is updated automatically in DonorView" and that statements are generated monthly, quarterly and annually. A search summary of Ren's (now 404) iPhi product sheet lists "DonorView" as the iPhi donor log-in module | confirmed (Minneapolis); search-summary only (Ren sheet) | [tmf.iphiview.com](https://tmf.iphiview.com/tmf/); [Minneapolis DonorView FAQ](https://www.minneapolisfoundation.org/donorview-faq/); [Ren iPhi product descriptions (404 on 2026-11-14)](https://www.reninc.com/wp-content/uploads/2023/09/Ren-iPhi-Product-Descriptions-v1.pdf) |
| 3 | What the Ren-built GivingPoint API serves | The production bundle and its lazy chunks call endpoints including `/api/DafAccounts/FundActivity`, `FundActivityBalance`, `GrantPayments`, `GetAccountStatements`, `DownloadStatement`, `AccountInvestments`, `ContributionActivity`, `CreateGrantRecommendation` and `/api/Party/AumTotalsForAccounts`. The version endpoint returns a build stamp (`"branch":"master"`, committed 2026-11-04). The bundle still links version tickets to `renpsg.atlassian.net` | confirmed (endpoint names); inferred (ledger-level data via Ren-hosted API) | [main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js); [version](https://www.nptgivingpoint.org/api/apistatus/version) |
| 4 | Ren's monitoring | `iphistatus.reninc.com` redirects to a private Atlassian Statuspage log-in titled "NPT iPhi Statuspage Status - Login". Components are not visible | confirmed (title) | [iphistatus.reninc.com](https://iphistatus.reninc.com/) |
| 5 | NPT's Form 990 (FY2024, FY2025) | No Ren, Stellar or iPhi string appears anywhere in either return (Part VII-B, Schedules I/L/M/O/R). Part IX information technology was $5,871,282 in FY2025, up from $3,649,680. Employees rose from 286 to 310 and other salaries were $26.47m. Schedule M 32b names only "third party consultants and outside legal counsel" for complex-asset diligence | confirmed absence | [NPT 990 FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml); [FY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml) |
| 6 | NPT's GivingPoint marketing page | Says the portal is "powering your charitable purpose with new technology". Names no vendor | confirmed (no vendor named) | [nptrust.org/nptgivingpoint](https://www.nptrust.org/nptgivingpoint/) |
| 7 | Historic link | Repo edge E091: a 2020 NPT donor application and account-management pages ran on Stellar iPhi | historically confirmed | [`relationship-graph-edges.csv`](../../data/mission-2026-11-14/relationship-graph-edges.csv) E091 |

### 1.2 Reading

- **Supported (inferred):** NPT's fund sub-ledger, meaning account balances, fund activity and statements, runs on **Ren's iPhi**, hosted by Ren, with GivingPoint as a Ren-built front end over it. Four separate pieces of evidence point to iPhi rather than a generic portal:
  - the "DonorView" name
  - the "NPT iPhi" status page
  - the iPhi-domain log-in redirect
  - an API that serves statements and fund activity
- **Not supported:** that Ren *administers* NPT. NPT employs 310 staff. Its 990 shows no administrator payee. Its IT line of $5.9m is the only plausible home for a Ren licence or hosting fee. **[Inference]** A licence or hosting fee of that kind would not appear in Part VII-B, which explains the absence. The fee amount is unknown.
- **Still unknown:**
  - whether iPhi is NPT's *book of record* for GAAP, or a sub-ledger reconciled to another general ledger
  - contract terms and fee
  - whether private-label programs (UBS, Wells Fargo) use the same stack (`ubs.iphiview.com` redirects to UBS)
- **A1 recommendation:** merge "NPT GivingPoint (sponsor-built)" into **Ren as technology provider (portal plus probable sub-ledger)**. Keep NPT as self-administering. On that basis Ren's X1 evidence can rise as the adjudicator proposed. The evidence tier stays "portal/DNS plus product-name convergence", not "990 payee". Validation-wave3's warning still governs: about 69% of Ren's numerator rests on observation, not on payments ([validation-wave3-report.md](validation-wave3-report.md)).

---

## 2. P-QCAL-02: DAFgiving360 forward-capability evidence

### 2.1 (a) Nonprofit payment rail

- **Program Policies (Updated December 2024):**
  - "DAFgiving360 makes grants by issuing checks bearing the name of our organization."
  - "on average, checks are generally mailed within seven to 10 business days … USPS delivery typically takes three to five business days".
  - "If a grant is time-sensitive, DAFgiving360 is able to wire grants, and certain fees may apply."

  Neither EFT nor ACH appears as a grant method; "electronic funds transfer" appears only as a way for donors to *contribute* ([2024 Program Policies PDF](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)).
- **Live site:** `dafgiving360.org` returned HTTP 403 to every fetch on 2026-11-14, including the home page, /charities, /program-policies and /about-dafgiving360/financials. A search summary of the donor page says DAFgiving360 will "send them each a check along with a personalized grant letter" ([search result: dafgiving360.org/donor-advised-funds](https://dafgiving360.org/donor-advised-funds)). That is a snippet only.
- **DAFpay:** Chariot's post "New Access Method for DAFgiving360 in DAFpay" is dated May 31, with no year shown on the page; repo edge E109 records it as 2026. Under it, first-time requests trigger a call from DAFgiving360, and "The DAFgiving360 team will then review, approve and disburse confirmed requests" ([Chariot](https://www.givechariot.com/post/new-access-method-for-dafgiving360-in-dafpay)). It does not say which rail carries the disbursement.
- **EFT share:** no source gives one. **Answer: the "only paper checks (plus wire on request)" reading is the documented position. A 2025–26 EFT programme is unknown, neither evidenced nor excluded.**

### 2.2 (b) Audited financial statements

The statements were not retrieved because the page returns 403. The FY2025 990 (FYE 2025-06-30) shows the following ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml)):
- **Part XII:** audited = yes, separate basis; audit committee = yes; compiled/reviewed = no.
- **Schedule O on the audit committee:** "the return preparer meets with the board's audit committee, along with management, to review the draft form". The audit committee also reviews conflict-of-interest questionnaires.
- **Schedule O on publication:** it "posts its most current Form 990 and audited financial statements to its public website". The statements are therefore public in principle.
- **Auditor:** not named. Deloitte Tax LLP is the paid preparer. Accounting fees were $440,674.
- **Related party:**
  - Schedule L Part IV lists CHARLES SCHWAB & CO, relationship "FOUNDER", "BROKERAGE & ADMINISTRATIVE SERVICES", $11,431,175 (FY2024 $9,178,403).
  - Schedule O: "THE WORKFORCE OF DONOR ADVISED CHARITABLE GIVING, INC. ARE EMPLOYEES OF CHARLES SCHWAB & CO. AS OUTLINED IN AN ADMINISTRATIVE SERVICES AGREEMENT".
- **Scale and expenses:** total assets $47.55bn. Part IX shows information technology $18,947,095 and "ADMINISTRATIVE FEE EXP" $10,879,472. Part VII-B lists 101 contractors paid more than $100k.

**For X3:** DAFgiving360 can show the Form 990 audit indicator plus a Schedule L related-party disclosure. That is the same level as Daffy and AEF in [sponsor-audit-notes.csv](../../data/mission-2026-11-14/sponsor-audit-notes.csv). Statement content stays U until P-NPT-01 or P-NPT-05 succeeds.

### 2.3 (c) Outbound transfer and history export

- **Terms:** the Dec 2024 policies have no clause on granting a DAFgiving360 balance to another DAF sponsor and no data-export clause. On history they say: "All account holders and additional account users have access to the account's grant history and grant award letters on the DAFgiving360 Client Center" ([policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)). The transfer page returns 403. The repo row in [sponsor-transfer-portability-terms.csv](../../data/mission-2026-11-14/sponsor-transfer-portability-terms.csv) stays "not_stated".
- **Practice (new):** the FY2025 Schedule I, summed by recipient EIN, shows grants to other DAF sponsors.

  | Recipient | FY2025 (FYE 6/2025) | FY2024 |
  |---|---|---|
  | Fidelity Investments Charitable Gift Fund | $976,570,217 | $127,700,997 |
  | National Philanthropic Trust | $161,539,525 | $249,117,686 |
  | Renaissance Charitable Foundation | $155,395,322 | $144,682,101 |
  | GiveClear Foundation | $29,739,069 | $316,109 |
  | American Endowment Foundation | $12,197,804 | $11,590,765 |
  | ImpactAssets | $9,524,655 | $30,234,867 |
  | Vanguard Charitable | $8,657,300 | $4,051,608 |
  | **Total, seven sponsors** | **$1,353.6m** (15.7% of $8.62bn Schedule I grants) | $567.7m |

  Sources: [FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml); [FY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml).

  **[Inference]** These are most likely donor-recommended DAF-to-DAF grants, so outbound transfer is possible in practice even though the policies are silent. The 7.6x jump to Fidelity is unexplained (P-NPT-03).

**Effect on the quadrant boundary:** nothing here moves a Y criterion *up* for forward capability. The rail is check/wire and export is undocumented. Outbound DAF-to-DAF volume is evidence of *permissive* portability, not of a capability. The adjudicator should keep A3/A4 Y at 2.00 unless P-NPT-05 finds EFT.

---

## 3. P-AGA-01: IRS e-file XML governance fields (Part XII, VII-B, Schedules L/O/M/R)

The full record is in [`sponsor-governance-990-xml.csv`](../../data/mission-2026-11-14/sponsor-governance-990-xml.csv). Latest year per sponsor:

| Sponsor (period) | Audited / basis | Audit committee | Auditor in return | Related-party or administrator | Ren/vendor named? |
|---|---|---|---|---|---|
| DAFgiving360 (FYE 6/2025) | Yes / separate | Yes | Not named (Deloitte Tax = preparer) | **Schwab & Co, Schedule L "FOUNDER", $11.43m**; workforce under Schwab ASA | No |
| NPT (FYE 6/2025) | Yes / consolidated | Yes | **RSM US LLP** (inferred: VII-B "AUDIT, TAX AND CONSULTING" $942,249) | Self-administered (310 staff); Schedule L only donor excess-benefit corrections | No |
| GS PWM DAF (CY2024) | Yes / separate | Yes (board members); "selection of an independent accountant is approved by the entire board" | Not named (PwC US Tax = preparer) | VII-B: GS Trust Co $14.60m, GS & Co "TECH & INV ADV FEES" $8.08m, Ayco "ADMIN. SERVICES" $1.03m; **no Schedule L**; Part IX "AGENCY FEE" $7.07m | No (Sapient $0.82m) |
| GS Gives (FYE 6/2025) | Yes / consolidated | **No:** "the full board of directors … assumes responsibility for oversight of the audit" | **PricewaterhouseCoopers LLP** (VII-B "AUDIT SERVICES" $303,392) | CAF America grant administration $875,665 | **Stellar** IT $172,604; Schedule M names Stellar among securities processors |
| MS GIFT (CY2024) | Yes / basis not ticked (CY2023 consolidated) | Yes | **Ernst & Young** (inferred: "Tax & Audit services" $185,460) | **RenPSG "ADMIN & LEGAL" $14.93m** (unaffiliated; no Schedule L); "4 board members are senior executives at Morgan Stanley" | Yes (RenPSG) |
| BofA CGF (CY2024) | Yes / consolidated; also compiled/reviewed = yes | Yes | Not named. Schedule O: audited statements prepared "to satisfy the MA Attorney General filing requirements" | Bank of America is corporate trustee (one voting member); no contractors | No (VII-B blank) |
| AEF (CY2024) | Yes / separate | Yes | Not named (RSM "accounting services" and preparer) | No administrator; NPact software development $249,500 | NPact (pre-Ren) |

Sources (XML): [DAFgiving360](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml); [NPT](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml); [GS PWM](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml); [GS Gives](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml); [MS GIFT](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml); [BofA CGF](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml); [AEF](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml).

**Readings.**
1. **Form 990 does not ask for the auditor's name.** It can be read only from Part VII-B service text. One case says "audit services" outright (GS Gives); two say "audit, tax and consulting" or "tax & audit" (NPT, MS GIFT). Four returns give no auditor at all.
2. **Part IV line 12a vs Part XII 2b:** NPT, MS GIFT and GiveClear answer "No" to Part IV 12a (separate independent audit) while answering "Yes" to XII 2b. These are recorded as filed. The likely cause is consolidated or combined audits, but that is not verified.
3. **Related-party classification differs.** Schwab appears on Schedule L as an interested person ("founder"). Goldman affiliates appear only in VII-B, and GS PWM files no Schedule L. Bank of America is trustee with no fee line except investment management. Morgan Stanley's link is board overlap only. For the A3 "captive administration" reading, DAFgiving360 is the only sponsor of the four bank or wirehouse programs whose return *labels* the administrator a related party.
4. **Ren and platform vendors are invisible in the returns of NPT, GS PWM and BofA.** All three are Ren-hosted per the repo. Absence from VII-B is uninformative for software and hosting, as already noted in [queue-vendor-scope-ren-denominator.md §4](queue-vendor-scope-ren-denominator.md).
5. **Give Interactive** appears in none of these returns.

---

## 4. P-WAT-01: ImpactAssets' $86.0m grant to GiveClear and AssetMark program size

| Evidence | Fact | Label | Source |
|---|---|---|---|
| Grant | ImpactAssets CY2024 Schedule I: GIVECLEAR FOUNDATION (EIN 81-3222963) $86,038,909, "GENERAL SUPPORT" | confirmed | [ImpactAssets CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml) |
| ImpactAssets DAFs | Count rose 2,083 → 2,197 and DAF value $2.72bn → $2.90bn (CY2023 → CY2024); DAF grants rose $155.7m → $432.5m | confirmed | as above; [CY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443189349305024_public.xml) |
| GiveClear CY2024 | 228 DAFs; contributions $210,026,838; grants $31,758,054; year-end value $215,283,755 | confirmed | [GiveClear CY2024 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml) |
| GiveClear CY2023 | **Also 228 DAFs**; contributions $25,498,763; year-end value $24,788,267 | confirmed | [GiveClear CY2023 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202412829349301586_public.xml) |
| Other inbound | DAFgiving360 granted GiveClear $29,739,069 in FYE 6/2025 and $316,109 in FYE 6/2024 | confirmed | [DAFgiving360 FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml) |
| Schedule B | Public XML shows contributors and amounts as "RESTRICTED" | confirmed (no data) | GiveClear XML above |
| GiveClear operations | Zero employees. Schedule O: "Attolero, LLC provides management and administrative services to GiveClear Foundation"; Attolero is owned by the Executive Director. Accounting is done by a firm owned by the CFO | confirmed | GiveClear CY2024 XML |
| CY2025 return | Not in the IRS TEOS index (last modified 2026-10-21) | confirmed absence | [IRS index 2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) |
| AssetMark size | No per-program figure found. AssetMark's 2024 network was "$116.9 billion in platform assets", which is platform AUM, not DAF balances | unknown | [Family Wealth Report](https://www.familywealthreport.com/printarticle.php?id=201546); [AssetMark guidelines](https://intercom.help/assetmark-help-center/en/articles/10924891-assetmark-charitable-program-guidelines) |

**Reading.** The timing fits the hypothesis. AssetMark's TIFIN hosts appeared in May 2024 and the old iPhi host redirects to TIFIN ([queue-watchlist-and-vendor-moves.md §4](queue-watchlist-and-vendor-moves.md)). Three facts cut against or complicate a clean "book transfer":
1. GiveClear's DAF count is unchanged at 228. Either the count was carried forward unchanged, or the $86m arrived as a few large accounts rather than an AssetMark book of many accounts.
2. ImpactAssets' own DAF count *rose* in CY2024.
3. A second sponsor (DAFgiving360) also moved about $30m to GiveClear.

**Verdict: keep "inferred". Program size is unknown, bounded above by $215.3m.** Next check: P-NPT-02, GiveClear's CY2025 990.

---

## 5. P-AGA-04: Chariot donor terms and DAFpay Provider Addendum

**Provider Addendum (public, "Updated: October 14, 2026")** ([givechariot.com/dafpay-provider-addendum](https://givechariot.com/dafpay-provider-addendum)):
- **Authorization:** "You hereby authorize Chariot, acting on behalf of DAF Donors and in accordance with the Integration Method in use, to exchange information with your systems and, where that Integration Method so provides, to create and submit grant requests within your systems".
- **Donor authority:** "DAF Donors authorize us to act on their behalf under the DAFpay Donor Terms of Use."
- **Provider control:** "You alone are responsible for reviewing, approving and executing each grant request, in accordance with your own policies and applicable law."
- **Disclaimer:** Chariot disclaims "(i) the acts and omissions of DAF Donors, including the accuracy of information they provide" and "(iv) the timing, amount or completion of any grant".
- **Agents and automation:** no clause on automated, scripted or agent-driven sessions, rate limits or initiator identity. A separately signed agreement prevails over the addendum.

**Donor Terms of Use.** `givechariot.com/legal-donors` returns HTTP 200 but serves the marketing homepage. That happened with curl and with WebFetch ([legal-donors](https://www.givechariot.com/legal-donors)). `llms.txt` lists no donor-terms entry ([llms.txt](https://www.givechariot.com/llms.txt)). A search snippet describes a "Donor Terms of Use" effective January 1, 2025, with arbitration and opt-out, under which Chariot can act for the donor. That is a snippet only and has not been verified.

**Credentials.** Chariot's help page says: "When a donor enters their account credentials in the modal, that information is fully encrypted and is not stored by Chariot at any time" ([DAFpay Security](https://givechariot.com/dafpay-security-standards)).

**Effect on [`agentic-control-gap-matrix.csv`](../../data/mission-2026-11-14/agentic-control-gap-matrix.csv):**
- The Chariot **liability_allocation** row is now evidenced as follows. Toward providers, Chariot disclaims donor errors, and the provider's own review is the control. This is still not agent-specific.
- The **agent_identification** row stays "gap".

---

## 6. P-CMP-05: workplace-giving and payment intermediaries vs DAF sponsors (nonprofit side)

| Operator | Fee borne by nonprofit | Cadence / delay (published) | Default if no electronic set-up | Source |
|---|---|---|---|---|
| **Benevity** (Foundations Fees Schedule, updated 2026-10-01) | "Cause Support Fee" of **2.99%** per donation (cap $500); manual check fee of the "Higher of $35 USD/CAD per check or 8% of the amount of the check", max $125, after two checks | Foundations "typically" disburse monthly (search summary only). Checks are sent only once the "Manual Check Threshold" of **$100** is met; smaller sums are "swept" annually if at least $20 | Check, with fee | [Benevity Fees Schedule](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf) |
| **YourCause / Blackbaud Giving Fund** | Client company chooses whether fees are covered (search summary); no public US fee schedule found | "The disbursement schedules are set by the client. Most client disburse monthly or quarterly." Pending timing: "we can't provide an exact timeline" | "Otherwise, a paper check will be mailed" | [How to receive donations](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-how-to-receive-donations.html); [Pending timeline](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-when-will-pending-donations-be-processed.html) |
| **PayPal Giving Fund** | None stated ("Without charging individual donors or charities for our services") | Paid 15–45 days after the donation at month end; unenrolled charities wait up to 90 days for enrolment, then receive a check | Check after enrolment window | Repo rows R14–R15 in [nonprofit-receipt-cost-by-rail.csv](../../data/mission-2026-11-14/nonprofit-receipt-cost-by-rail.csv) ([PayPal](https://www.paypal.com/us/webapps/mpp/givingfund/about)) |
| **Every.org** | DAF disbursements free via Stripe Connect or PayPal; 1.5% via For Good | Weekly Stripe payouts | — | Repo rows R12–R13 ([Every.org blog](https://blog.every.org/how-does-every-org-work-your-top-10-pricing-questions-answered/)) |
| **Fidelity Charitable** (DAF) | ACH/Stripe "incur no cost or fee for your organization" | 1–2 days after processing | Check; Fidelity announced an EFT-only switch for 2026-07-01, then extended it (see [daf-user-complaints-deep-research.md §5.8](daf-user-complaints-deep-research.md)) | Repo row R04 ([Fidelity FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) |
| **DAFgiving360** (DAF) | None | Check mailed 7–10 business days, plus USPS 3–5 days | Check (wire on request) | [2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) |

**Complaint signal** from the repo corpus ([daf-user-complaints-corpus.csv](../../data/mission-2026-11-14/daf-user-complaints-corpus.csv), n = 244):
- **Benevity, nonprofit complainants:** 9 grant_delay, 2 customer_service, 2 attribution and 1 fee record, mostly from [Trustpilot](https://www.trustpilot.com/review/benevity.com). Benevity also has 17 nonprofit *praise* records.
- **PayPal Giving Fund:** one nonprofit grant_delay record and attribution complaints, including state-AG matters, as recorded in the corpus.
- **National DAF sponsors:** no named sponsor has a nonprofit grant_delay record in the corpus. Nonprofit fee complaints about sponsors are one record each for Fidelity Charitable and for unnamed "large DAF providers".

**Reading.**
- The worst nonprofit-side experiences in the evidence sit with **workplace-giving intermediaries**. The reasons are structural: fees deducted from the gift, monthly or client-set batching, thresholds, and check fees that penalise organisations without EFT. Sponsors charge nonprofits nothing; their costs are delay and paper.
- **Caveat:** the corpus is selection-biased. Trustpilot draws Benevity complaints, and sponsor complaints surface on donor forums instead ([daf-user-complaints-deep-research.md §9](daf-user-complaints-deep-research.md)).

---

## 7. P-AGA-02: does any DAF contract define an AI agent as a role?

| Document | Date | Agent role? | Source |
|---|---|---|---|
| Daffy Member Agreement | "Updated November 11, 2025" (unchanged) | No. "agent" appears only for estate executors and crypto transfers | [daffy.org/legal/agreement](https://www.daffy.org/legal/agreement) |
| Endaoment Terms and Conditions | "Last updated August 12, 2026" | No. "agents" appears only in indemnity and liability boilerplate | [Endaoment T&C](https://docs.endaoment.org/governance/documentation/terms-and-conditions.md) |
| Chariot Nonprofit Terms | "Updated: October 14, 2026" | No. Credentials may go only "to those agents of your organization who agree to comply" (human staff). The AI clause covers Gift Processing automations, "which provide the ability to process Mail, automatically apply tags, transform data, or export data" | [legal-nonprofit](https://givechariot.com/legal-nonprofit) |
| Chariot DAFpay Provider Addendum | 2026-10-14 | No | §5 above |
| Chariot MCP Server (help page) | live | Not a contract. An MCP connector for Gift Processing customers: "Claude will prompt you to sign in with your Chariot credentials via OAuth. Once authorized, Claude can read and manage data scoped to your organization's account". Tools include `create_donation`, `delete_donation` and `reconcile_deposit` | [help.givechariot.com](https://help.givechariot.com/account-management/chariot-mcp-server.md) |
| Sponsor policies searched (Endaoment policies, JCF federation policies) | 2025–26 | No. Roles are person-typed, such as "Grant Representative" | [search, 2026-11-14](https://jewishfed.org/wp-content/uploads/2025-11-20-donor-advised-fund-policies-and-procedures.pdf) |

**Answer: no public DAF contract defines an AI agent as a role.**
- **New fact:** a second DAF-adjacent operator, Chariot, now ships an MCP server. Its scope is the nonprofit side (donation records and deposits), not grant initiation from DAFs.
- **Effect on the gap matrix:** the liability and authorization rows remain "gap" for all four operators.
- **Next check:** re-check Daffy quarterly, as the queue item requests.

---

## 8. Limitations

- dafgiving360.org returned 403 throughout, and reninc.com product pages returned 403/404. The Wayback Machine connection was reset by the proxy.
- Several facts rest on search summaries and are marked as such: the Ren iPhi product sheet's "DonorView", the Chariot donor-terms snippet and the Benevity monthly cadence.
- Schedule I sums include only grants itemised in the XML (over $5,000). Purposes are generic, so "DAF-to-DAF" is an inference.
- Part VII-B service text is the only route to auditor identity. An "audit, tax and consulting" payee may not be the signing auditor.

---

## Source register

| ID | Source | Used for |
|---|---|---|
| S1 | [NPT Terms of Use / Privacy (2026-10-29)](https://www.nptrust.org/privacy-policy/) | "DonorView" portal name |
| S2 | [NPT GivingPoint page](https://www.nptrust.org/nptgivingpoint/) | No vendor named |
| S3 | [GivingPoint main bundle](https://www.nptgivingpoint.org/main-OYPICD2D.js); [version endpoint](https://www.nptgivingpoint.org/api/apistatus/version) | API surface, Ren Jira, build stamp |
| S4 | [iphistatus.reninc.com](https://iphistatus.reninc.com/) | "NPT iPhi Statuspage" title |
| S5 | [tmf.iphiview.com](https://tmf.iphiview.com/tmf/); [Minneapolis DonorView FAQ](https://www.minneapolisfoundation.org/donorview-faq/) | DonorView = iPhi portal name |
| S6 | [Ren iPhi product descriptions (404)](https://www.reninc.com/wp-content/uploads/2023/09/Ren-iPhi-Product-Descriptions-v1.pdf) | Search summary only |
| S7 | IRS e-file XML (GivingTuesday mirror): [DAFgiving360 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml); [NPT FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601289349302480_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511339349301311_public.xml); [GS PWM CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202413109349303336_public.xml); [GS Gives FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611249349302616_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202511119349301416_public.xml); [MS GIFT CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503239349300435_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403209349313980_public.xml); [BofA CGF CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423209349309982_public.xml); [AEF CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513219349310376_public.xml); [ImpactAssets CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543169349307999_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443189349305024_public.xml); [GiveClear CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533199349302978_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202412829349301586_public.xml) | Governance CSV, Schedule I sums, GiveClear |
| S8 | [IRS TEOS index 2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | Object IDs; CY2025 GiveClear absence |
| S9 | [DAFgiving360 2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) | Rail, timing, history, no transfer clause |
| S10 | [Chariot: DAFgiving360 in DAFpay](https://www.givechariot.com/post/new-access-method-for-dafgiving360-in-dafpay) | DAFgiving360 review and disbursement |
| S11 | [DAFpay Provider Addendum](https://givechariot.com/dafpay-provider-addendum); [Nonprofit Terms](https://givechariot.com/legal-nonprofit); [legal-donors](https://www.givechariot.com/legal-donors); [llms.txt](https://www.givechariot.com/llms.txt); [DAFpay Security](https://givechariot.com/dafpay-security-standards) | P-AGA-04 |
| S12 | [Chariot MCP Server](https://help.givechariot.com/account-management/chariot-mcp-server.md) | P-AGA-02 |
| S13 | [Daffy Member Agreement](https://www.daffy.org/legal/agreement); [Endaoment T&C](https://docs.endaoment.org/governance/documentation/terms-and-conditions.md) | P-AGA-02 |
| S14 | [Benevity Fees Schedule](https://go.benevity.com/hubfs/website/en/Benevity-Fees-Schedule.pdf); [Blackbaud NPOconnect help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-how-to-receive-donations.html), [pending timeline](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect/content/npo-faq-when-will-pending-donations-be-processed.html) | P-CMP-05 |
| S15 | [AssetMark guidelines](https://intercom.help/assetmark-help-center/en/articles/10924891-assetmark-charitable-program-guidelines); [Family Wealth Report](https://www.familywealthreport.com/printarticle.php?id=201546) | P-WAT-01 |
| S16 | Repo: [queue-vendor-scope-ren-denominator.md](queue-vendor-scope-ren-denominator.md), [validation-wave3-report.md](validation-wave3-report.md), [queue-watchlist-and-vendor-moves.md](queue-watchlist-and-vendor-moves.md), [queue-agentic-controls-and-sponsor-audits.md](queue-agentic-controls-and-sponsor-audits.md), [queue-payment-rails-cluster.md](queue-payment-rails-cluster.md), [daf-user-complaints-deep-research.md](daf-user-complaints-deep-research.md) | Baseline |

---

## Data dictionary

### `sponsor-governance-990-xml.csv` (one row per sponsor-year return)

| Column | Meaning |
|---|---|
| sponsor, ein | Filer name as used in repo; 9-digit EIN |
| object_id | IRS e-file object ID (TEOS index) |
| tax_period_end, return_type | From the XML header |
| paid_preparer | Preparer firm name; "none (self-prepared)" when no firm group is present |
| fs_audited_xii_2b | Part XII line 2b (FSAuditedInd) |
| audit_basis | Part XII 2b basis box: Separate / Consolidated / not ticked |
| audit_committee_xii_2c | Part XII line 2c (AuditCommitteeInd) |
| compiled_or_reviewed_xii_2a | Part XII line 2a |
| independent_audit_part_iv_12a | Part IV line 12a (IndependentAuditFinclStmtInd), recorded as filed even when inconsistent with 2b |
| auditor_named / auditor_evidence / auditor_status | Auditor identity, the text supporting it, and one of `confirmed_by_VII-B_description`, `inferred_from_VII-B_description`, `unknown` |
| governing_body_voting, independent_voting | Part VI lines 1a/1b |
| family_or_business_rel_vi_2 | Part VI line 2 |
| schedule_l_filed | Whether Schedule L is present in the return |
| related_party_or_admin | Analyst summary of Schedule L, Part VII-B administrator lines and Schedule O/M statements |
| vii_b_top_contractors | Part VII-B Section B rows: name, service, compensation |
| contractors_over_100k | Part VII-B line 2 count |
| employees | Part I line 5 |
| part_ix_info_technology, part_ix_fees_management, part_ix_fees_other, part_ix_accounting_fees | Part IX line totals (USD; blank = line absent) |
| notes | Schedule O excerpts and caveats |
| xml_url, propublica_url | Source XML (GivingTuesday mirror) and ProPublica rendering |
| accessed_date | 2026-11-14 |

### `relationship-graph-edges-additions-5.csv`

Same columns as `relationship-graph-edges.csv`. `relationship_type` adds **`auditor`** (EE007–EE009) to the existing vocabulary. Edges with `grant_to` (EE003–EE006) are Schedule I sums by recipient EIN. EE001 refines EA016 (NPT scope). EE002 refines E108 (Schwab).

### `queue-proposals-npt-misc.csv`

Format per [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). There are six proposals, P-NPT-01 to P-NPT-06, all `open`.
