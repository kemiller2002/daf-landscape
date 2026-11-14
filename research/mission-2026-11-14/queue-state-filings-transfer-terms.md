# State charity filings, outbound transfer terms, sponsor payment rails and DAF-to-DAF flows

**Queue items:** P-NPT-01, P-QA3-02, P-INF-06, P-NPT-03. Full text is in [`research-priority-queue.csv`](../../data/mission-2026-11-14/research-priority-queue.csv).

**Date:** 2026-11-14. **Method:** public sources only.
- **IRS filings:** I located returns through the IRS TEOS index (`index_2022.csv`–`index_2026.csv`; the 2026 index was last modified 2026-10-21). I read the XML from the GivingTuesday mirror, following [`scripts/mission_990_contractors.py`](../../scripts/mission_990_contractors.py). I parsed Schedule I Part II for 15 sponsors and 53 returns (FY2022–FY2025).
- **Web pages and PDFs:** fetched with curl or WebFetch, without logging in.
- **Limits:** no accounts, no contact with anyone, and no automated use of CAPTCHA-gated search tools.

**Quotes and labels:** quotes are verbatim and at most 40 words. Labels:
- **confirmed:** a first-party document or filing states it.
- **inferred:** convergent indirect evidence.
- **unknown:** no evidence either way.
- **secondary:** a third-party or search-summary source only.

**Files written:**
- [`data/mission-2026-11-14/daf-to-daf-flows-990.csv`](../../data/mission-2026-11-14/daf-to-daf-flows-990.csv): 2,020 grantor–recipient–year rows, 1,220 of them to national sponsors.
- [`data/mission-2026-11-14/sponsor-transfer-portability-terms-v2.csv`](../../data/mission-2026-11-14/sponsor-transfer-portability-terms-v2.csv): 17 rows. It keeps the original 13 rows, updates six and adds four. It is a new file; the original is unchanged.
- [`data/mission-2026-11-14/queue-proposals-state-filings.csv`](../../data/mission-2026-11-14/queue-proposals-state-filings.csv): P-STF-01 to P-STF-05.

---

## 1. Answers

| Item | Answer | Label |
|---|---|---|
| **P-NPT-01** State filings | **I could not retrieve any statements, so the item stays open.** What the research established:<br>- **NY and MA would hold the audits.** Both require audited statements above $1m revenue. **California does not collect audits**: its annual filing is the RRF-1 plus the Form 990 only.<br>- **DAFgiving360 and NPT are filed in NY.** Their own documents point readers to the NY Attorney General's registry for financial reports. Fidelity's guidelines carry a NY disclosure too.<br>- **The NY search cannot be used by an agent.** It moved to `charities-search.ag.ny.gov`, a single-page app whose API calls carry an `X-Recaptcha-Token`. I did not attempt it programmatically.<br>- **The MA filings hosts were unreachable** from this sandbox (proxy 502), and mass.gov returned 403. The CA search tool returned 404/503.<br>- **New evidence from the 990:** the BNY Mellon Charitable Gift Fund **terminated in December 2024** and granted $619.8m to RCF. | confirmed (filing rules, disclosures, access status); unknown (statement content) |
| **P-QA3-02** Transfer, closing and history terms | **Still no sponsor publishes an outbound transfer procedure**, but two published texts now mention outbound grants:<br>- **Fidelity's 2026 Program Guidelines** acknowledge grants to other DAF sponsors and exclude them from the activity test.<br>- **NCF's Guide to giving** bars "succession funds" from granting to other DAF sponsors and lets standard Giving Funds do so.<br><br>**BofA CGF** publishes explicit account-closing mechanics. **None of the eight sponsors** publishes a history-export clause. NPT comes closest: quarterly statements are "available for download".<br><br>**Not retrievable:** GS PF (no public circular), MS GIFT (its circular is not public), AEF's policy page (403) and DAFgiving360's live site (403). | confirmed |
| **P-INF-06** DAFgiving360 and BNY rails | **DAFgiving360:** the documented rail is **check plus award letter, with wire possible**. No EFT channel appears in its policies, in the DAF Direct guide or in PayPal's list of Grant Payments sponsors, and the EFT share is unknown.<br>**BNY Charitable:** the BNY Mellon Charitable Gift Fund was **wound into RCF at the end of 2024**, so its rail is now whatever RCF/Ren uses. Its legacy terms were check-based (secondary source).<br>**Other sponsors:**<br>- NPT pays by PayPal EFT up to $250,000.<br>- Vanguard pays through a third-party EFT provider.<br>- NCF pays by EFT or check.<br>- AEF prefers ACH.<br>- BofA CGF pays **by check only**. | confirmed (documents); unknown (DAFgiving360 2025–26 EFT) |
| **P-NPT-03** DAFgiving360 → Fidelity $976.6m | **The e-file cannot say how many transfers made up the figure.** DAFgiving360 files **one aggregated Schedule I line per recipient EIN**, with the generic purpose "PUBLIC, SOCIETAL BENEFIT". All of the $976.6m is cash.<br>The pattern points to a **few very large movements on top of a steady base [inference]**:<br>- **Steady base:** the line was $129.1m, $120.9m and $127.7m in FY2022–FY2024, then jumped by $848.9m.<br>- **Other one-year spikes of similar size:** Fidelity → Schwab $506.8m in FY2022 (including $271.4m in kind); Fidelity → Vanguard $480.1m in FY2025, against about $20m before; SVCF → NPT $1.59bn in CY2024; BNY → RCF $619.8m on termination.<br>- **Reverse flow:** Fidelity → DAFgiving360 was $117.8m in FY2025. | confirmed (amounts); inferred (composition) |

---

## 2. P-NPT-01: what the state regulators hold, and what was reachable

### 2.1 Filing rules

| State | Do audited statements go to the regulator? | Evidence |
|---|---|---|
| **New York** (CHAR500) | Yes. An independent CPA audit is required above $1m in revenue and support (raised from $750,000 on 2021-07-01). A CPA review is required between $250k and $1m. | secondary: [Cogency Global](https://www.cogencyglobal.com/blog/new-york-audit-threshold-increasing-for-registered-charities/); [Lawyers Alliance (2022)](https://lawyersalliance.org/userFiles/uploads/legal_alerts/New_York_Charities_Filing_Requirements_Legal_Alert.pdf) |
| **Massachusetts** (Form PC) | Yes. Audited statements are required above $1,000,000 in gross support and revenue, and a review between $500,001 and $1m. The AG states that the Form PC and its attachments are public records. | search summary of [mass.gov FAQ](https://www.mass.gov/info-details/frequently-asked-questions-about-charitable-organizations) and [portal instructions (Nov 2024)](https://www.mass.gov/doc/november-2024-updated-portal-instructions/download). mass.gov returned 403 to direct fetch |
| **California** (RRF-1) | **No.** The required annual filing is "Form RRF-1 along with either: Copy of IRS Form 990, 990-EZ, or 990-PF as filed with the IRS". Also: "Other forms not specifically requested … are not required by the Registry." An audit is required at $2m or more of revenue, but it only has to be **available** to the AG. | confirmed: [oag.ca.gov/charities/renewals](https://oag.ca.gov/charities/renewals); [Nonprofit Integrity Act summary](https://www.oag.ca.gov/sites/all/files/agweb/pdfs/charities/pdf/nonprofit-integrity-act-nov04-auditreq.pdf) |

### 2.2 Which sponsors are on the NY and MA files

**DAFgiving360.** Its Program Policies (Dec 2024) say: "Information on charitable organizations and copies of their latest financial reports may be obtained from the New York Attorney General's Charities Registry" ([policies PDF](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf)). **Confirmed.**

**NPT.** Its donor guide says: "A copy of the latest annual report can be obtained from the organization or from the Office of the Attorney General by writing the Charities Bureau" ([NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf)). **Confirmed.**

**Fidelity Charitable.** The Program Guidelines carry a New York disclosure ([guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf)), and Fidelity is a Massachusetts trust. Fidelity already posts its audit, so the state filing adds nothing.

**BofA CGF.** Its CY2024 Schedule O, recorded in the repo, says its audited statements exist to satisfy the MA AG filing requirement ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349318170_public.xml)). **Confirmed** that the statements sit on the MA file.

**GS PF, MS GIFT, AEF and Daffy.** No state disclosure was found in their public material. Whether they are registered in NY or MA is **unknown**.

### 2.3 Access attempts (2026-11-14)

| Registry | Result |
|---|---|
| NY | `charitiesnys.com/RegistrySearch/...` redirects to `charities-search.ag.ny.gov/RegistrySearch`, a JavaScript app. Its bundle calls `charities-search-api.ag.ny.gov/api/FileNet/RegistrySearch` and `/FileNet/DocumentDetail?guid=` with an `X-Recaptcha-Token` header (reCAPTCHA site key embedded). **Gated; I did not attempt it programmatically.** |
| MA | `filings.ago.state.ma.us` and `charity.ago.state.ma.us`: proxy "connect_unreachable" (502). mass.gov pages: 403. |
| CA | The legacy tool (`rct.doj.ca.gov/Verification/Web/Search.aspx`) returned 404 to curl and 503 to WebFetch. The new portal (`ca-rcf.evokeplatform.com/app/publicPortal/verification`) is a JavaScript single-page app. CA would not hold the audits anyway (§2.1). |
| Sponsor sites | DAFgiving360 financials, giving-report, transfer and `/public/file/` URLs all returned 403. A Schwab-hosted FY2020 audit link (`schwab.com/public/file/P-6528471`) returned 404. |

**Effect on A3 X3:** no change. DAFgiving360, NPT, GS PF, MS GIFT and BofA CGF stay U for statement content. The cheapest route is a human retrieval from the NY registry, which holds DAFgiving360 and NPT, and from the MA registry, which holds BofA CGF (P-STF-01).

### 2.4 New: BNY Mellon Charitable Gift Fund termination (EIN 30-0748315)

The CY2024 return ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml)) shows:
- **Schedule I:** "RENAISSANCE CHARITABLE FOUNDATION INC" received $619,798,574, with the purpose "TO FURTHER THE ORGANIZATION'S EXEMPT PURPOSE".
- **Balance sheet:** total assets fell from $496.6m to $1.96m.
- **Schedule D:** DAF grants were $725.6m, and one DAF remained at year end.
- **Schedule O:** "DUE TO THE ONGOING TERMINAITON [sic], INFORMATION ON FINANCIAL STATEMENTS IS PRESENTED ON BOTH A GOING CONRCERN [sic] BASIS FOR THE PERION [sic] 1/1/24 THROUGH 12/23/24, AND A LIQUIDATION BASIS".

This confirms a search-summary report from a Ren help article (now 404) that BNY collapsed the fund into RCF. **It is a sponsor-initiated bulk DAF-to-DAF transfer**, the clearest example in the data. The DAF Direct guide still lists BNY Mellon as a participating sponsor (§4).

---

## 3. P-QA3-02: published outbound, closing and history terms

| Sponsor | Document (date) | Outbound DAF-to-DAF | Closing | History / export | Source |
|---|---|---|---|---|---|
| **Fidelity Charitable** | Program Guidelines (© 2026; PDF created 2026-09-11) | **Acknowledged:** "Grants made to other donor-advised fund sponsors do not qualify as grant activity for the purposes of the minimum grant requirement." No procedure, fee or in-kind option is stated. | No inactivity grants are made until two years without grants; privileges can be revoked | View privilege covers "contribution and grant history, statements". **No export clause** | [PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) |
| **DAFgiving360** | Program Policies (Dec 2024); live site 403 | None found | Dormant account with no succession plan: "the account will be closed and assets will be transferred to eligible charities based on the account granting history" | Online grant history and award letters. **No export clause** | [PDF](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) |
| **NPT** | Donor guide (uploaded 2024-09); MAAP | None found. The guide covers only inbound "Grants and Transfers from other DAFs". | After six inactive years, or the death of the last advisor with no successor, the balance goes to named charities, by granting history, or to the NPT Giving Fund | "A quarterly statement of your DAF account activity will be posted to GivingPoint, where it will be stored and will be available for download." File format not stated | [guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf); [MAAP](https://www.nptrust.org/wp-content/uploads/2020/10/Minimum-Account-Activity-Policy-MAAP-NPT.pdf) |
| **NCF** | Guide to giving at NCF (live, © 2026) | **Explicit, in succession:** "Succession funds are intended to continue your charitable legacy within NCF. So, they may not make grants to or transfer assets to another donor-advised fund sponsor or Giving Fund at NCF." Standard funds may do so. | Succession plan; otherwise distributed by grantmaking history | Quarterly and annual statements plus a secure online site. No export clause | [ncfgiving.com](https://www.ncfgiving.com/guide-to-giving-at-NCF) |
| **Vanguard Charitable** | Policies & Guidelines (updated 2026-01-09) | None found | One final grant below the $500 minimum is allowed for a closing account. An account below $250 at fee assessment "will be charged and the account will be closed" | Quarterly statement; the January statement summarises the prior calendar year. No export clause | [policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) |
| **BofA CGF** | Program Guidelines Version 3.2024 (no 2025 or 2026 file at that path) | None found. "A grant recommendation to distribute the entire balance of a donor-advised fund account may require additional processing time." | Residual cash over $250 goes to the last grant recipient; $250 or less goes to the General Fund. A month-end closing grant waits for that month's fees | "quarterly reports of account holdings, as well as confirmations". No export clause | [PDF](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) |
| **MS GIFT** | Grant-making do's and don'ts (Oct 2024) | None found; the document refers to "the Donor Circular and Disclosure Statement", which is not public | not found | not found | [PDF](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf) |
| **GS PF** | No public Program Circular found | unknown | unknown | unknown | [990 XML CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503109349303645_public.xml) |
| **AEF** | Granting Guidelines v1.6 (2025-03); policy-statements page 403 | None found (inbound-focused material only) | Dormant-fund review after 36 months without grants | not stated; a platform migration kept only two years of history (repo) | [PDF](https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf) |

**Findings**

1. **The repo statement "no sponsor publishes an outbound transfer policy" needs a qualification.** It still holds for *procedures*, but Fidelity and NCF now mention outbound grants to other sponsors in their published terms. NCF is the only sponsor that restricts them, and only for succession funds. Both texts treat a DAF-to-DAF grant as an ordinary grant to a public charity, not as a portability right.
2. **History export is not a published right at any of the eight sponsors.** Terms speak only of viewing (Fidelity, DAFgiving360) or of statements (NPT, Vanguard, BofA, NCF). NPT's "available for download" is the only download language found. **[I]** A3/A4 Y5 should stay at most 2 for all eight.
3. **Fidelity has made in-kind DAF-to-DAF grants.** Its FY2022 Schedule I shows $271.4m noncash to Schwab Charitable, on top of $235.3m cash ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430459349302913_public.xml)). AEF also labels some sponsor grants "IN KIND TRANSFER" while reporting them as cash: ImpactAssets $102.0m (CY2022), Bradley Impact Fund $25.6m (CY2023) and MS GIFT $9.7m (CY2023). The repo's "transfers are generally cash after liquidation" holds for most rows but not universally. **Confirmed (filing); the terms are silent.**

---

## 4. P-INF-06: nonprofit payment rails

| Sponsor | Documented rail to nonprofits | Remittance content stated | Source |
|---|---|---|---|
| **DAFgiving360** | "DAFgiving360 makes grants by issuing checks bearing the name of our organization." The award letter is attached. "Certain restrictions may apply to grants sent via wire." **No EFT or ACH clause** | Award letter: account holder name, special account name and/or address, or anonymous | [policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) |
| DAF Direct (Fidelity, DAFgiving360, BNY Mellon) | "Funds are usually paid by check and sent by first-class mail. Some sponsoring charitable organizations may offer Electronic Funds Transfer" | — | [DAF Direct guide](https://www.dafdirect.org/popups/DAF-Direct-User-Guide.pdf) (contact `dafdirect@fmr.com`) |
| PayPal Grant Payments (2023) | "Currently, National Philanthropic Trust (NPT), Vanguard Charitable, and CharityVest are using Grant Payments". **DAFgiving360 is not listed** | Dashboard shows "donor information, grant letters, and terms and conditions" | [PayPal paper](https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf) |
| **NPT** | "Grants of up to $250,000 will be processed via Grant Payments (electronic funds transfer via PayPal) or check." | PayPal notification with "all relevant donor and grant details" | [NPT guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) |
| **Vanguard** | "through a third-party electronic fund transfer provider or by a check" | not stated | [policies](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) |
| **NCF** | "Approved grants are usually distributed by electronic funds transfer or check" | Letter naming the Giving Fund and any purpose | [NCF guide](https://www.ncfgiving.com/guide-to-giving-at-NCF) |
| **AEF** | "AEF's preferred method of grant payment is also the quickest and most secure: ACH transfer." A nonprofit email address is used to facilitate ACH | not stated | [AEF guidelines](https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf) |
| **BofA CGF** | "Grants are issued via checks bearing the name of Bank of America Charitable Gift Fund." Sent by USPS first class only | Account name and donor/advisor name unless anonymous | [BofA guidelines](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) |
| **BNY Mellon CGF** | Fund terminated into RCF (Dec 2024; §2.4). Its legacy FAQ: "the Gift Fund staff will send a check" | — | secondary: [Pershing DAF FAQ via search](https://www.fortefoundation.org/wp-content/uploads/2025/11/Pershing-Donor-Advised-Funds-FAQ.pdf) |

**Answer.** DAFgiving360's documented rail is still check (plus wire), and its EFT enrolment share is **unknown**. Three independent documents are silent on DAFgiving360 EFT where they name other sponsors' EFT: the policies, PayPal's sponsor list and the DAF Direct guide. That supports the "check-based" reading. It is **not** evidence of absence for 2025–26, because the live site was unreadable (403). Among the national sponsors reviewed, BofA CGF is the only other one that is **check-only by its own terms**.

---

## 5. P-NPT-03: DAF-to-DAF flows in Schedule I

### 5.1 What the e-file can and cannot show

**Aggregation.** DAFgiving360 (64,697 Schedule I lines in FY2025) reports one line per recipient. Its Fidelity line is `RecipientEIN 110303001`, `CashGrantAmt 976570217`, `NonCashAssistanceAmt 0` and `PurposeOfGrantTxt` "PUBLIC, SOCIETAL BENEFIT" ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml)). The number of underlying grants or accounts is therefore not observable. Fidelity, NPT and Vanguard aggregate in the same way. MS GIFT, AEF and ImpactAssets sometimes split lines; MS GIFT's CY2023 lines to Fidelity were $120.2m, $20.6m, $6.5m and smaller.

**Gaps:**
- **Not itemised in XML:** RCF and BofA CGF file Schedule I as a single "See Attached" line.
- **Not mirrored:** Vanguard's FY2025 XML returns `NoSuchKey`.

**Cross-check:** the Chronicle of Philanthropy reported "$183 million migrated from Fidelity to DAFgiving360". That matches Fidelity's FY2023 line of $183,131,878. Its "$63 million moved from the National Philanthropic Trust to Fidelity Charitable" matches NPT FY2023 at $63,245,404 ([Chronicle, 2026-03-06](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/)).

### 5.2 Fidelity ↔ DAFgiving360 (USD m; fiscal years end June 30; cash + noncash)

| Flow | FY2022 | FY2023 | FY2024 | FY2025 |
|---|---|---|---|---|
| DAFgiving360 → Fidelity | 129.1 | 120.9 | 127.7 | **976.6** |
| Fidelity → DAFgiving360 | **506.8** (235.3 cash + 271.4 noncash) | 183.3 | 100.9 | 117.8 |
| Net to Fidelity | −377.7 | −62.4 | +26.8 | **+858.7** |

**Context, FY2025:**
- **DAFgiving360:** Schedule I grants rose $2.25bn, to $8.62bn. The Fidelity increment of $848.9m is 38% of that rise. Grants to all national sponsors reached $1,549.8m (18.0% of Schedule I).
- **Fidelity:** Schedule D contributions jumped from $15.91bn to $26.46bn. The DAFgiving360 inflow is 3.7% of that.
- **Fidelity's own outflows also spiked:** Vanguard $480.1m (FY2024 $21.7m), NPT $346.8m, ImpactAssets $203.7m and GS PF $159.9m. Its total to national sponsors was $1,713.6m.

**Reading [inference].** The FY2022–FY2024 base of about $125m a year looks like routine donor-initiated moves. The FY2025 increment is the size of a few very large accounts, or of one programme-level move. Comparable single-year spikes appear across this dataset, and two of them are documented as single events: BNY → RCF (termination) and Fidelity → Schwab FY2022 (with in-kind securities). I found no press or filing that names the FY2025 transfer. **Answer: unresolved by public data; most consistent with a small number of very large transfers.** P-STF-03 proposes the recipient-side test.

### 5.3 Largest sponsor-to-sponsor flows in the data (USD m)

| Grantor → recipient | Year | Amount | Note |
|---|---|---|---|
| Silicon Valley CF → NPT | CY2024 | 1,591.3 | One line, "General Nonprofit Support"; prior years $0.01m and $7.2m. 55% of SVCF's Schedule I |
| DAFgiving360 → Fidelity | FY2025 | 976.6 | §5.2 |
| BNY Mellon CGF → RCF | CY2024 | 619.8 | Sponsor termination |
| Fidelity → Schwab Charitable | FY2022 | 506.8 | $271.4m in kind |
| Fidelity → Vanguard | FY2025 | 480.1 | Up from $21.7m |
| Fidelity → NPT | FY2025 | 346.8 | |
| Vanguard → ImpactAssets | FY2024 | 308.3 | Prior years about $0 |

**Share of Schedule I going to national sponsors, latest year:**
- **Low:** MS GIFT 0.5% (CY2024), NCF 3.6%.
- **Mid:** NPT 10.7%, Fidelity 11.4%, Vanguard 14.0% (FY2024), GS PF 15.1%, DAFgiving360 18.0%.
- **High:** AEF 22.2%, ImpactAssets 46.9%, SVCF 55.0%.

The full matrix is in the CSV.

---

## 6. Caveats

- **Recipient classification uses the DAFRC 2025 sponsor list, by EIN.** "National" includes donation processors and multi-purpose charities such as CAF America and Rockefeller Philanthropy Advisors. Grants to them may fund programmes rather than DAFs. University and healthcare "sponsors" are excluded, and community and single-issue recipients are included only at ≥$1m.
- **Schedule I covers itemised grants over $5,000 only.** Purpose text is generic, so "DAF-to-DAF" means sponsor-to-sponsor money, not proven donor transfers.
- **Fiscal years differ:** Fidelity, DAFgiving360, NPT, Vanguard and JCF end in June; Chicago CT in September; the rest in December. Fidelity's FY2022 return is an amended return.
- **Term documents may lag practice.** BofA's guidelines are from 2024 and NPT's guide from 2024-09.

---

## 7. Source register

| ID | Source | Used for | Accessed |
|---|---|---|---|
| S1 | [IRS TEOS index 2022–2026](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv) | Object IDs | 2026-11-14 |
| S2 | GivingTuesday XML mirror `https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{OBJECT_ID}_public.xml`. Key files: [DAFgiving360 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml); [Fidelity FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml); [Fidelity FY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202430459349302913_public.xml); [BNY CGF CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml); [SVCF CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202543149349305759_public.xml); the full list is in the CSV `source` column | Schedule I flows | 2026-11-14 |
| S3 | [DAFRC 2025 updated dataset (repo copy)](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Recipient classification | repo |
| S4 | [CA AG annual renewal page](https://oag.ca.gov/charities/renewals); [CA NIA audit requirements](https://www.oag.ca.gov/sites/all/files/agweb/pdfs/charities/pdf/nonprofit-integrity-act-nov04-auditreq.pdf); [CA charities page](https://oag.ca.gov/charities) | CA filing scope; new portal URL | 2026-11-14 |
| S5 | [Cogency Global NY audit threshold](https://www.cogencyglobal.com/blog/new-york-audit-threshold-increasing-for-registered-charities/); [Lawyers Alliance NY alert (2022)](https://lawyersalliance.org/userFiles/uploads/legal_alerts/New_York_Charities_Filing_Requirements_Legal_Alert.pdf) | NY thresholds (secondary) | search 2026-11-14 |
| S6 | [mass.gov charity FAQ](https://www.mass.gov/info-details/frequently-asked-questions-about-charitable-organizations); [MA portal instructions Nov 2024](https://www.mass.gov/doc/november-2024-updated-portal-instructions/download); [MA public charities filing search](https://www.mass.gov/info-details/search-public-charities-filings) | MA thresholds and search (search summary; 403 to fetch) | 2026-11-14 |
| S7 | [NY charities search](https://charities-search.ag.ny.gov/RegistrySearch) and its JavaScript bundle | reCAPTCHA gating | 2026-11-14 |
| S8 | [Fidelity Charitable Program Guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf) | Outbound clause, history, NY disclosure | 2026-11-14 |
| S9 | [DAFgiving360 2024 Program Policies](https://static1.squarespace.com/static/557c669ae4b0e197d11bcb11/t/67c50d53d910296aef195450/1740967255089/DAFgiving360-2024-Program-Policies.pdf) | Rail, closing, history, NY disclosure | 2026-11-14 |
| S10 | [NPT donor guide](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf); [NPT MAAP](https://www.nptrust.org/wp-content/uploads/2020/10/Minimum-Account-Activity-Policy-MAAP-NPT.pdf) | Rail, statements, closing, NY disclosure | 2026-11-14 |
| S11 | [Vanguard Policies & Guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) | Rail, closing, statements | 2026-11-14 |
| S12 | [NCF Guide to giving](https://www.ncfgiving.com/guide-to-giving-at-NCF) | Succession-fund restriction, rail | 2026-11-14 |
| S13 | [BofA CGF Program Guidelines v3.2024](https://www.bankofamerica.com/philanthropic/Program_Guidelines_2024.pdf) | Check-only rail, closing | 2026-11-14 |
| S14 | [MS GIFT grant-making do's and don'ts](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-grantmaking.pdf) | Reference to the non-public circular | 2026-11-14 |
| S15 | [AEF Granting Guidelines v1.6](https://aefonline.org/wp-content/uploads/2025/03/AEF_05_GrantingGuidelines_V1.6.pdf); [AEF Maintain the Fund](https://advisorwelcome.aefonline.org/wp-content/uploads/2024/09/AEF_08_MaintainTheFund_V1.5.pdf) | ACH preference, dormant review | 2026-11-14 |
| S16 | [DAF Direct user guide](https://www.dafdirect.org/popups/DAF-Direct-User-Guide.pdf) | Participants; check default | 2026-11-14 |
| S17 | [PayPal Grant Payments paper (2023)](https://filecache.mediaroom.com/mr5mr_paypal/186631/PP_2023_GrantPayments.pdf) | EFT sponsors | 2026-11-14 |
| S18 | [Chronicle of Philanthropy, "Caught in a Web of DAF Transfers" (2026-03-06)](https://www.philanthropy.com/news/caught-in-a-web-of-daf-transfers/) | Cross-check of the $183m and $63m flows | 2026-11-14 |
| S19 | [Chariot, DAFgiving360 FY25 report breakdown](https://www.givechariot.com/post/breaking-down-the-dafgiving360-fy25-annual-report) | 1.4m grants in FY2025; no mention of transfers or rails | 2026-11-14 |
| S20 | [Pershing DAF FAQ](https://www.fortefoundation.org/wp-content/uploads/2025/11/Pershing-Donor-Advised-Funds-FAQ.pdf) (search summary only) | Legacy BNY check rail (secondary) | search 2026-11-14 |
| S21 | Repo baseline: [queue-npt-dafgiving360-misc.md](queue-npt-dafgiving360-misc.md), [queue-agentic-controls-and-sponsor-audits.md](queue-agentic-controls-and-sponsor-audits.md), [regulation-market-structure-portability.md](regulation-market-structure-portability.md), [sponsor-audit-notes.csv](../../data/mission-2026-11-14/sponsor-audit-notes.csv) | Prior findings | repo |

---

## 8. Data dictionary

### `daf-to-daf-flows-990.csv` (one row per grantor return × recipient EIN)

| Column | Meaning |
|---|---|
| grantor_sponsor / grantor_ein / grantor_filer_name | Filing sponsor: short name, 9-digit EIN, and the name as filed |
| recipient_sponsor / recipient_ein | Recipient name as written on Schedule I (first variant) and its EIN |
| recipient_class | `national_sponsor`, `community_foundation`, `single_issue_sponsor_religiously_affiliated` or `single_issue_sponsor_other`, from DAFRC type/subtype. University and healthcare recipients are excluded |
| recipient_dafrc_type / recipient_dafrc_subtype | DAFRC classification of the recipient EIN |
| fiscal_year / tax_period_end | Calendar year of the fiscal year-end; YYYYMM of period end |
| amount_usd | cash_usd + noncash_usd summed over all Schedule I lines to that EIN in the return |
| cash_usd / noncash_usd | CashGrantAmt and NonCashAssistanceAmt sums |
| schedule_i_lines / largest_line_usd | Number of Schedule I lines to that EIN and the largest single line. Most sponsors file one line, so this is **not** a grant count |
| purpose_text | Distinct PurposeOfGrantTxt values (truncated to 200 characters) |
| object_id / source / source_note | IRS e-file object ID, XML URL and method note |

**Inclusion:** all recipients classed national; other classes only at ≥$1m per row.

**Grantors:** Fidelity, NPT, DAFgiving360, Vanguard (FY2022–FY2024), GS PF, SVCF, AEF, MS GIFT, NCF, Chicago CT, ImpactAssets, JCF and BNY Mellon CGF (CY2023–CY2024).

**Excluded as grantors:** RCF and BofA CGF, because Schedule I is an attachment.

### `sponsor-transfer-portability-terms-v2.csv`

The columns of `sponsor-transfer-portability-terms.csv` are kept unchanged. For updated rows, `source_url` is extended with the new sources, separated by ` ; `. Three columns are added:

| Column | Meaning |
|---|---|
| outbound_policy_found | `explicit_acknowledged` (terms mention grants to other DAF sponsors), `explicit (...)` with a restriction noted, `none_found (document, date)`, `not_retrieved`, or `n/a` |
| history_export | What the published terms say about donor access to contribution and grant history: `view_only_online`, `downloadable_statements`, `quarterly_statements`, `lost_on_close`, `not_stated` or `not_retrieved`, with a short qualifier |
| outbound_observed_990 | Latest-year Schedule I flow to national DAF sponsors (from `daf-to-daf-flows-990.csv`), or why it is not measurable |

Rows marked "(prior pass)" were not re-checked in this pass. The four new rows are GS PF, MS GIFT, BofA CGF and BNY Mellon CGF (terminated).

### `queue-proposals-state-filings.csv`

The format follows [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md), with IDs P-STF-01 to P-STF-05.
