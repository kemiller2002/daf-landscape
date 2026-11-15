# Queue batch 34 B: pass-through channels (platform DAF sponsors, DAF Direct, Givinga clients, insurer channel, Jasper Ridge exit)

**Date:** 2026-11-15. **Agent:** batch34 B. **Recency rule:** 2021+ evidence. Older facts are labelled as dated context.
**Queue items:** P-B33C-02, P-INF-03, P-INF-02, P-BUY-07, P-MOR-06.
**Read first:** `queue-batch33-market-structure.md` (wave-18 corrections), `queue-batch30-everyorg-givinga-goodstack.md` (wave-15 corrections), `digital-sponsor-entities-2026.csv`.
**New data:**
- [`pass-through-sponsors-2026.csv`](../../data/mission-2026-11-14/pass-through-sponsors-2026.csv): 39 sponsor-year rows, 9 entities, FY2021 to the latest e-filed return.
- [`relationship-graph-edges-additions-19.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-19.csv): ES001–ES023.
- [`queue-proposals-batch34b.csv`](../../data/mission-2026-11-14/queue-proposals-batch34b.csv): P-B34B-01 to -03.

**Labels:**
- **[F]** first-party document read this pass. **[X]** e-filed 990 XML read this pass (GivingTuesday mirror of the IRS e-file data).
- **[S]** secondary source. **[R]** search-index capture only. **[I]** inference.

**Method.** Object IDs come from the IRS e-file indexes for 2021–2026 (local cache). Each XML was read for:
- Schedule D Part I, both columns (DAFs, and other funds or accounts);
- Part VII-B contractors and Part IX fee lines;
- Schedule R Parts II and V;
- Schedule O, Schedule A Part II, and Schedule N.

No logins, forms or outreach. dafdirect.org robots.txt disallows only `/cgi-bin`.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B33C-02: size the pass-through sponsors** | **About $3.9bn of latest-year DAF grants across the five large intermediaries, or $4.8bn counting the micro-donation funds AOGF has just moved out of the DAF column.** The latest filed years:<br>- AOGF (Benevity): $1.39bn DAF grants plus $0.94bn other funds (FYE 2026-03).<br>- CAF America: $947m (FYE 2025-04).<br>- PPGF (PayPal): $796m (CY2024).<br>- BBGF (Blackbaud): $536m (CY2025).<br>- NFG: $200m (CY2024).<br>**On filed FY2024 returns the five total $4.32bn, not DAFRC's $4.38bn.** DAFRC imputes PPGF $169m too low and NFG $228m too high.<br>**Who captures fees, per filed returns:**<br>- Benevity Inc: $54.7m a year (2.35% of AOGF grants).<br>- CyberGrants (Bonterra): $8.3m from CAF America.<br>- Bonterra Tech: $2.5m from NFG.<br>- PayPal: donates $9.0m of services to PPGF and takes no disclosed fee.<br>- Blackbaud: no payment disclosed.<br>**Two structural changes:**<br>- AOGF and BBGF are reclassifying employee and micro-donations as not DAF contributions.<br>- NFG has been controlled since 2024-06-07 by a new nonprofit parent (DCSO), not by Bonterra. | High (filed figures); medium (fee capture, since payees are not always named) |
| **P-INF-03: what is DAF Direct Trust** | **A Massachusetts-law trust that "operates" dafdirect.org and "own[s] the Widget". It has no IRS exemption record and files no 990.**<br>- The site's robots.txt, analytics and `@fmr.com` contact point to Fidelity.<br>- Listed participants: Fidelity Charitable, DAFgiving360 (Schwab) and BNY Mellon Charitable Gift Fund. BNY voted on 2024-12-24 to stop operating its DAF program. Vanguard is not a participant.<br>- **Not found:** the trustees, the governing instrument and any funding split. Neither Fidelity's nor Schwab's FY2024–25 990 mentions it.<br>- **Not available:** a 2021+ adoption count or a share of grants. The live terms are still dated 2015-01-27. | High on what is public; the governance questions stay open |
| **P-INF-02: Givinga clients versus own sponsor** | **No company can be named from filings.**<br>- Givinga Foundation's Schedule B is redacted.<br>- Its Schedule I (424 grantees, $8.5m, CY2024) shows employer-shaped clusters (Memphis civic groups; Red Wing/Goodhue County, MN) but no employer names.<br>- Partner pages (PlanSource, WeSpire) do not say which entity holds the accounts.<br>- **New:** Givinga Foundation makes grants to other intermediaries: Percent Impact Foundation (Goodstack US) $179,886 (CY2024), Blackbaud Giving Fund $431,671 (CY2023), GlobalGiving $160,637. Pass-through layers are stacked.<br>- No second DAF sponsor using Givinga technology was found (unchanged). | Medium (absence) |
| **P-BUY-07: insurer and benefits-broker channel** | **The channel splits two ways: fraternal insurers run their own sponsor, and commercial insurers and brokers white-label a third-party sponsor.**<br>- **Own sponsor:**<br>  - Thrivent Charitable (9,198 DAFs, $93.6m grants, $700m EOY, CY2025). Thrivent Financial is paid $6.0m for admin; Ren is paid $0.48m for technology.<br>  - Knights of Columbus Charitable Fund (665 DAFs, $80.7m, $126m, CY2024). Administered by Knights of Columbus Asset Advisors ($0.58m).<br>- **Third-party sponsor:**<br>  - Northwestern Mutual and MDRT's Global Gift Fund: RCF/Ren. The MDRT Foundation holds no DAFs itself.<br>  - Alera Group's "Alera Charitable" (2025-11): TIFIN Give. GiveClear is inferred as sponsor.<br>**No insurer acquisition or ownership of DAF technology was found.** | High (structure); medium (Alera sponsor) |
| **P-MOR-06: why Jasper Ridge terminated** | **No stated reason is public, but the filings show the mechanism: a failed public-support test, then dissolution, with the assets kept inside the adviser's fund.**<br>- **Support test:** public support fell from 50.4% (CY2020) and 45.2% (CY2021) to **13.15% in CY2022**, below the 33⅓% test. The CY2022 return qualified only on the prior-year test.<br>- **Transfers:** in 2022 the fund moved $1.319bn to Schwab Charitable ($746.5m) and Fidelity Charitable ($548.9m). $1.231bn of it went in kind as interests in Jasper Ridge Diversified (Tax Exempt) LP.<br>- **Dissolution:** the board adopted a plan of dissolution on 2022-12-08. The 2023 return is a final **990-PF** citing a §507(b)(1)(A) termination; final grants went to the same two sponsors and dissolution took effect 2023-12-31.<br>- **[I]** The 990-PF filing is consistent with the fund being treated as a private foundation for 2023 after failing the test in both CY2022 and the prior-year computation.<br>- No press coverage was found. | High (filings); medium (cause) |

---

## 1. P-B33C-02: the pass-through sponsors

### 1.1 Sizes, FY2021 to latest (Schedule D Part I, DAF column unless stated) [X]

| Sponsor (EIN) | FY2021 | FY2022 | FY2023 | FY2024 | Latest | DAFRC FY2024 | Return (latest) |
|---|---|---|---|---|---|---|---|
| **AOGF (Benevity)** 81-0739440, FYE Mar | $1,553.4m (766,186 DAFs) | $1,665.2m | $1,714.1m | $1,950.2m (FYE 2024-03) | FYE 2025-03: $2,124.1m (710,352)<br>**FYE 2026-03: DAF $1,390.0m (695) + other funds $935.7m (751,746)** | $1,950.2m (filed) | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml) |
| **CAF America** 43-1634280, FYE Apr | $231.1m (742) | $479.5m | $599.7m | $821.2m (FYE 2024-04) | FYE 2025-04: $947.4m (740); other funds $45.8m (235) | $821.2m (filed) | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610489349300906_public.xml) |
| **PPGF (PayPal)** 45-0931286 | $284.2m (483,095) | $342.8m | $495.9m | **$795.7m (380,644)** | CY2024 | **$626.6m (imputed)** | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml) |
| **BBGF (Blackbaud)** 46-0942102 | blank (org grants $631.8m) | $682.0m | $589.2m | $552.6m | CY2025: $536.4m (count blank) | $552.6m | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml) |
| **Network for Good** 68-0480736 | $547.4m (1) | $440.5m | $338.6m | **$199.8m** | CY2024 | **$427.9m (imputed)** | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml) |
| Bright Funds Foundation (Submittable) 46-2109112 | org grants $59.0m | $65.9m | $80.7m | $21.3m | CY2024 (no Sch D values in any year) | not in DAFRC | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503459349301950_public.xml) |
| Givinga Foundation 47-4172718 | $9.4m | $13.6m | $13.5m | $12.4m | CY2024 (amended) | $12.4m | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml) |
| Goodstack US (Percent Impact Fdn) 87-3165286 | — | — | no Sch D | $1.2m (7,268) | CY2025: $1.66m (3); org grants $6.9m | — | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml) |
| Every.org 61-1913297 (990-PF) | grants $5.8m | $17.4m | $16.8m | $44.9m | CY2024 | — | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml) |

**Totals for the five large intermediaries:**
- **FY2024 on filed returns: $4,319.4m.** DAFRC: $4,378.4m.
  - The net gap is small ($59m), but two entries are each wrong by about $0.2bn.
  - PPGF is +$169.1m on the filed return; NFG is −$228.1m.
- **Latest filed year: $3,869.3m in the DAF column.**
  - Adding AOGF's new "other funds" column ($935.7m) gives $4,805.0m.
  - Adding CAF America's other funds ($45.8m) gives $4,850.8m.

### 1.2 Reclassification: AOGF and BBGF move employee and micro-donations out of "DAF" [X]

- **AOGF, FYE 2026-03** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml)):
  - Schedule D DAF column: 695 accounts, $1,557.8m contributions, $1,390.0m grants.
  - Other funds column: **751,746 accounts, $937.3m contributions, $935.7m grants**.
  - Schedule O, Part VI line 4: "corporate donors can make donations into such donor-advised funds and provide ongoing advice … Individual donors may use the platform to make micro-donations and recommend grants … at or near the time of donation, without ongoing advisory privileges".
  - The previous year (FYE 2025-03) reported 710,352 DAF accounts and $2,124.1m of DAF grants. That return said AOGF's model includes "various fund structures that are not conventional DAF models" but still put them in the DAF column.
- **BBGF, CY2025** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml)):
  - Schedule O, Part III line 3: "BBGF determined that employee donations made through CSRconnect should not be treated by BBGF as contributions to donor advised funds."
  - **Yet Schedule D Part I still reports $543.8m of DAF contributions and $536.4m of DAF grants**, about 99.6% of total revenue. The note and the schedule do not reconcile in this return.
  - [I] The reclassification may first show in the CY2026 Schedule D.
- **Reading [I].**
  - The largest workplace intermediaries are reclassifying point-of-donation giving as not DAF.
  - Industry totals built from Schedule D, including DAFRC, will fall by about $0.9bn of grants and about 0.75m accounts on AOGF alone, with no change in money flow.
  - P-B34B-01 proposes tracking the TY2025 returns of the rest.

### 1.3 Control and who captures the fees [X]

| Sponsor | Controlling party (Schedule O / R) | Platform payee and amount (latest) | Other platform-economics lines |
|---|---|---|---|
| **AOGF** | Independent board. Benevity runs it under a "management services agreement" covering "planning or executing budgets" and "supervising exempt operations". Two listed individuals are paid by Benevity | **Benevity Inc $54,654,481** (FYE 2026-03). Earlier years: $29.6m, $29.3m, $33.5m, $46.0m, $54.5m from FYE 2021-03 to 2025-03 | Revenue "administrative service" $31.4m. Merchant fees $6.08m. BlueSnap $4.23m, PayPal $0.73m, Braintree $0.27m. Grant to Canadian Online Giving Foundation $5.9m |
| **CAF America** | Three members elect the board. UK subsidiary SRTL is managed by CAF (UK) | **CyberGrants LLC (Bonterra) $8,287,044, "grant processing"** (FYE 2025-04). $5,409,310 in FYE 2024-04. Not among the top-5 contractors in FYE 2021–23 | Management fees line $8.69m. Omaze professional-fundraising agreement ended 2022-12-31 |
| **PPGF** | **PayPal Inc is the sole member**; it appoints and may remove directors | **No fee to PayPal disclosed.** PayPal donates personnel ("PPGF HAS NO EMPLOYEES"): Schedule R code M $9,041,772 (CY2024) | "Transaction costs & service fees" **$12.6m CY2024, against $4.8m CY2023** (payee not named; [I] processing on Meta-routed gifts). Program revenue $1.9m |
| **BBGF** | Blackbaud is the Class A member and elects 2 of 5 directors. Majority independent. Blackbaud "oversight" under a service agreement | **No payment to Blackbaud disclosed** in Part VII-B or Schedule R | Credit-card fees $1.63m, banking/merchant $0.96m, vetting fees $0.47m (recovered from charities) |
| **NFG** | **Since 2024-06-07 its sole member is Durable Capital for Sustainable Outcomes Inc (DCSO, EIN 99-0468956)**, which elects all directors. NFG gave DCSO $27.5m (Schedule R code B) | **Bonterra Tech LLC $2,490,845, "professional fundraising"** (CY2024). $4,765,096 CY2023; paid to "Network for Good (C Corp)" in CY2021–22 ($5.8m, $4.8m) | Transaction processing $4.46m. Cumulative "$5.4 billion … close to 446,000 nonprofits"; "$202 million in donations in 2024" |
| **Bright Funds Fdn** | Officers only. WizeHive Inc (Submittable) is a related taxable corporation | WizeHive Schedule R code M $4,043,819 (CY2023); amount blank in CY2024 | Revenue fell from $85.7m (CY2023) to $25.6m (CY2024) after Submittable's 2024-08 purchase of WizeHive [I timing only] |

**Reading [I]:**
1. **Benevity is the only owner that takes a large disclosed fee from its intermediary: $54.7m a year, about 2.35% of grants.** AOGF also bills $31.4m of "administrative service" revenue. A sale of Benevity (Hg, 2020 vintage) carries this fee stream with it.
2. **PayPal subsidises PPGF.** Meta's 2023 routing (batch 33 §1) shows up as grants up 60% (CY2023 → CY2024) and transaction costs up 2.6×. The economics sit with the processor, not the DAF.
3. **Bonterra's link to NFG is a shrinking vendor contract,** not control. Batch 33's "Bonterra → NFG" should read as a vendor link. NFG DAF grants fell 63% from CY2021 to CY2024.
4. **Bonterra's CAF America contract is growing:** CyberGrants fees rose 53% in a year.

---

## 2. P-INF-03: DAF Direct Trust

| Question | Finding | Source |
|---|---|---|
| Legal entity | "the DAF Direct Website, which is operated by DAF Direct Trust ('DAF Direct,' 'we,' or 'us')". Terms are "As of January 27, 2015" (still the live version). Massachusetts law and courts | [Terms](https://www.dafdirect.org/popups/userAgreementPopUp.html) [F] |
| Ownership of the widget | "We own the Widget, including all associated intellectual property … and branding". The privacy policy says DAF Direct Trust "only shares your information with the participating sponsoring organizations" | [Terms](https://www.dafdirect.org/popups/userAgreementPopUp.html); [Privacy](https://www.dafdirect.org/privacyPolicy.html) [F] |
| Who runs it | Contact `DAFDirect@fmr.com` (FMR is Fidelity). robots.txt is headed "robots.txt file for Fidelity Charitable". The page loads Fidelity scripts (`fmrvs.js`) | [robots.txt](https://www.dafdirect.org/robots.txt); [home](https://www.dafdirect.org/) [F] |
| Participating sponsors | "currently facilitates grant recommendations from donors of Fidelity Charitable®, DAFgiving360®, and the BNY Mellon Charitable Gift Fund®. More … may be added in the future". **Vanguard is not listed** | [About](https://www.dafdirect.org/about-daf-direct/index.html) [F] |
| Is the BNY listing current? | **No.** BNY Mellon Charitable Gift Fund's CY2024 990, Schedule O: "On December 24, 2024, the board of directors voted to no longer operate the donor advised fund ('DAF') program"; dissolution certificate filed 2024-12-31; 1 DAF and $4.7m at year-end | [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml) [X] |
| Tax status and filings | Not in the IRS EO BMF and not in the e-file index under any "DAF Direct" name. No mention of DAF Direct, the trust or `dafdirect` in Fidelity Charitable's FY2024/FY2025 or Schwab Charitable's FY2024/FY2025 990 XMLs (including Schedule R) | IRS EO BMF, e-file index (local cache) [X]; [Fidelity FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml) [X] |
| Trustees, governing instrument, funding | **Not public.** The "DAF DIRECT" trademark application (serial 85779042, filed 2012-11-14) was filed by "The Trustees of Fidelity Investments Charitable Gift Fund" and is reported dead | [markinton.com](https://markinton.com/trademark/daf-direct-85779042) [S]; USPTO TSDR not checked |
| Fees | "Neither you nor your donors will incur any download or transaction fees"; "100% of the funds transfer … with no administration or transaction fees" | [home](https://www.dafdirect.org/); [About](https://www.dafdirect.org/about-daf-direct/index.html) [F] |
| Still promoted? | Yes. Fidelity Charitable's nonprofit FAQ: "consider adding the DAF Direct widget to your website and enrolling in Fidelity Charitable's EFT program" | [Fidelity FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html) [F] |
| Adoption or grant share | No 2021+ figure. The site lists five example users. The last count is still 1,251 charities in 2015 (dated context, Chronicle) | [Fundraising benefits](https://www.dafdirect.org/fundraising-benefits/index.html) [F] |

**Reading [I]:**
- DAF Direct is a Fidelity-run, sponsor-owned free widget. It has not been refreshed: the terms date from 2015, the copyright line reads "2013", and it still lists a sponsor that wound down in 2024.
- Of the three largest national sponsors, only Fidelity and Schwab are reachable through it. It does not compete on reach with DAFpay's multi-sponsor network, only on price (free against 2.9%).
- "Trust" here is probably a contractual or administrative trust, not an exempt entity. Its trustees cannot be identified without the governing instrument.

---

## 3. P-INF-02: Givinga client programs

- **Accounts.** Every disclosed program still sits at Givinga Foundation (batch 30 §2.2): PlanSource (2021 release), WeSpire (2019), EarthShare (2022), Janus Henderson CIA (2025).
  - The December 2025 "Universal Sponsored Account" suite (OBBBA-driven) is marketed for companies' employee accounts.
  - The Business Wire text returned 403. A search capture says the "Universal Sponsored Account (USA), a corporate charitable fund" is part of Givinga's suite ([Business Wire 2025-12-11](https://www.businesswire.com/news/home/20251211023148/en)) [R].
  - The PlanSource Givinga page names no sponsor ([PlanSource](https://plansource.com/wealth/givinga/)) [F].
- **Schedule I CY2024 (amended)** ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml)) [X]: 424 grantees, $8,509,507.
  - Largest: Together We Thrive Foundation $950,000.
  - Memphis cluster: Memphis-Shelby Crime Commission $252,000; Slingshot Memphis $172,675; Memphis Area Chamber $105,000; Memphis Tomorrow $50,000; National Civil Rights Museum $85,000.
  - Red Wing / Goodhue County, MN cluster: Red Wing Environmental Learning Center $265,900; Goodhue County Fair $100,000; United Way of Goodhue Wabasha & Pierce $84,025; Red Wing Youth Outreach $77,225.
  - **[I]** These look like two employer-hosted programs (one Memphis-headquartered, one Red Wing-headquartered), but the filing does not name them and this pass does not guess.
- **Intermediary-to-intermediary grants** [X]:
  - Percent Impact Foundation (Goodstack US) $179,886 (CY2024).
  - GlobalGiving $160,637 (CY2024).
  - "Givinga Foundation" $144,641 (CY2024, a self-named grantee).
  - The Blackbaud Giving Fund $431,671 (CY2023, [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml)).
  - Employee gifts to charities enrolled only on another processor are routed through that processor's DAF. **[I]** Pass-through layers stack: a donation can carry two intermediaries' processing.
- **Answer.** No company is identifiable from public filings as running its accounts at Givinga Foundation rather than at its own sponsor. No company was found running Givinga technology on its own sponsor. The question needs program terms or employer disclosures, which were not found.

---

## 4. P-BUY-07: insurer and benefits-broker channel

| Firm (type) | Program | Sponsor of record | Administrator / technology | Size (latest) | Source |
|---|---|---|---|---|---|
| **Thrivent** (fraternal insurer) | Thrivent Charitable DAF | Thrivent Charitable Impact & Investing (41-1802412), its own sponsor | **Thrivent Financial, "admin & management services" $6,017,074**. Schedule O: "delegates control over management duties to Thrivent Financial" and leases its employees. Renaissance Acquisition Co (Ren) technology $479,172 | CY2025: 9,198 DAFs; $132.0m contributions; $93.6m grants; $700.4m EOY. (CY2021: 3,978 / $50.0m / $426.9m) | [XML CY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202612669349300236_public.xml) [X] |
| **Knights of Columbus** (fraternal insurer) | Knights of Columbus Charitable Fund | KCCF (81-5466677), its own sponsor | **Knights of Columbus Asset Advisors LLC**, hired "to oversee its day-to-day operations", $576,772. iPhi portal (EK004) | CY2024: 665 DAFs; $73.7m contributions; $80.7m grants; $125.8m EOY (CY2021: 242 / $2.7m / $58.2m) | [XML CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349305000_public.xml) [X] |
| **Northwestern Mutual** (mutual insurer) | Northwestern Mutual DAF | Renaissance Charitable Foundation | Ren. Partner-specific fee schedule in the 2024-11 circular (E037/E038) | not disclosed separately | [NWM circular 11-24](https://www.reninc.com/wp-content/uploads/2025/08/NWM-Program-Circular-11-24.pdf) (repo) |
| **MDRT** (insurance-adviser association) | Global Gift Fund | Renaissance Charitable Foundation (E065) | Ren DFX (E066) | not disclosed. **MDRT Foundation (36-6080766) reports no Schedule D DAF values** in FY2024 or FY2025 | [MDRT Fdn FY2025 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202620409349301907_public.xml) [X] |
| **Alera Group** (P&C, benefits and wealth broker; "$1.5 billion in gross revenue") | "Alera Charitable", white-label, announced 2025-11-12 | Not named in the release. **[I] GiveClear Foundation**, because TIFIN Give says GiveClear "receives contributions, holds assets, and manages donor accounts" | TIFIN Give | not disclosed ("accessible minimums") | [syndicated release](https://windpress.info/es/press-release/945595/alera-group-partners-with-give-a-tifin-platform-to-launch-white-labeled-donor-advised-fund-platform-for-clients) [S]; [TIFIN Give help](https://intercom.help/give-ria/en/articles/10104394-the-relationship-with-giveclear) [F]; [Business Wire](https://www.businesswire.com/news/home/20251112726739/en/Alera-Group-Partners-with-Give-a-TIFIN-platform-to-Launch-White-Labeled-Donor-Advised-Fund-Platform-for-Clients) (403) |
| Ameriprise (RiverSource parent) | Ameriprise DAF Program | RCF (E019) | Ren | — | repo |

**Reading:**
- **Fraternal benefit societies run their own sponsor** and pay the insurer's own staff or advisory arm to administer it: Thrivent $6.0m, Knights of Columbus $0.58m. They buy only software (Ren, iPhi).
- **Commercial mutuals, associations and brokers rent a sponsor:** RCF for Northwestern Mutual, MDRT and Ameriprise; GiveClear via TIFIN Give for Alera.
- **[I]** For a DAF vendor the fraternal model is a software sale. The commercial model is a sponsor-plus-software bundle.
- No insurer acquisition, investment or build of DAF technology was found for 2021–2026. The search covered MassMutual, New York Life, Guardian, Modern Woodmen and Mutual of Omaha, and found no policyholder DAF programs [R].

---

## 5. P-MOR-06: Jasper Ridge Charitable Fund (47-2088631)

### 5.1 Timeline from filings [X]

| Date / year | Event | Source |
|---|---|---|
| CY2020 | 7 DAFs, $1,058.0m EOY. Public support 50.41% (33⅓% test met, current year) | [990 CY2020](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202133139349302898_public.xml) |
| CY2021 | 7 DAFs; $212.3m contributions; $45.0m grants; **$1,428.3m EOY**. Public support 45.20%. Officers are Jasper Ridge Partners (JRP) employees. JRCF paid JRP $1.30m for advice and Jasper Ridge Services $0.92m for administration, mostly indirectly through Jasper Ridge Diversified (Tax Exempt) LP | [990 CY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202213159349303326_public.xml) |
| 2022-03-31 to 2022-12-30 | Schedule N transfers totalling **$1,319,068,001**: Schwab Charitable $746,466,086; Fidelity Charitable $548,851,915; Dechomai Asset Trust $23,700,000 (GI Partners Feeder LP interest); Vanguard Charitable $50,000. **$1,231.1m was in kind, as interests in Jasper Ridge Diversified (Tax Exempt) LP** | [990 CY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml) |
| CY2022 | 0 DAFs at year-end; $1,318,968,752 DAF grants. **Public support 13.15%.** Qualified only via the prior-year 33⅓% test (`ThirtyThrPctSuprtTestsPY170Ind`). Directors Phipps (JRP), Brest, Hall and Harmon left on 12/31/22; JRP staff (Swaminathan, Tandon) joined the board | same |
| 2022-12-08 | "A plan of dissolution was adopted by the board of directors" | [990-PF 2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441279349102374_public.xml) |
| 2023 | **Form 990-PF, final return.** "the foundation terminated its activities in accordance with code section 507(b)(1)(A)". Final grants: Schwab $2,956,978 and Fidelity $1,249,438, "completed on 12/28/2023". Delaware dissolution effective 12/31/2023 | same |

### 5.2 Why it ended

- **Stated cause:** none. Neither the filings nor any public statement gives a reason, and searches found no press (aggregator profiles only).
- **Mechanism visible in filings:**
  1. **A support-test cliff.** A DAF sponsor with seven very large accounts relies on public support from gifts by other public charities and capped individual gifts.
     - The 5-year support base was $630.7m in CY2022. Contributions over the 2% cap were $449.4m of it.
     - Support fell to 13.15%, below 33⅓%.
     - **[I]** Large public-charity gifts from 2017 left the 5-year window in CY2022. An aggregator profile reports a $100m SVCF grant to JRCF in 2017 [S].
     - Failing both the current-year and the next prior-year test means private-foundation status for the following year. That fits the 2023 990-PF and the §507(b)(1)(A) termination, which is a private-foundation termination route.
  2. **The adviser kept the assets.** 93% of the transfers were the same Jasper Ridge Diversified LP interests, so the money stayed in JRP's commingled fund, now held by Schwab and Fidelity DAFs.
     - **[I]** The donors kept DAF treatment, and JRP probably kept the management mandate, without running a public charity.
- **Implication for the mortality metric:** this exit is a regulatory-structure exit by an adviser-affiliated single-family sponsor. It is not market failure or a loss of donors. It is still 79–89% of verified exit assets (sponsor-mortality analysis). P-B34B-02 proposes a support-test screen.

---

## 6. Corrections to existing repo text

1. **`queue-batch33-market-structure.md` §0 and §2.2 (wave-18 text) — "$4.4bn of FY2024 DAF grants (DAFRC; PPGF's $626.6m and NFG's $427.9m are imputed)".** Add: "On filed returns the FY2024 total is $4.32bn: PPGF $795.7m (380,644 DAFs; [XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml)) and NFG $199.8m ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml)) [batch 34 B]."
2. **Same file, §2.1 Bonterra row and §2.2 list ("Bonterra → NFG").** Add: "NFG is a Bonterra vendor customer (Bonterra Tech LLC $2.49m CY2024). Since 2024-06-07 NFG's sole member is Durable Capital for Sustainable Outcomes Inc."
3. **`sponsor-mortality-analysis.md` and `validation-wave4-report.md` (V4-08 "Schwab received $750.6m").** The line-item sum of Schedule N in the CY2022 XML is **$746,466,086** to Schwab. Total transfers are $1,319,068,001. Adding the 2023 990-PF final grant ($2,956,978) gives $749.4m, which is still not $750.6m.
4. **Research queue P-INF-03 text** ("funding by Fidelity Charitable / DAFgiving360 / BNY"; the brief also names Vanguard). Vanguard is not a DAF Direct participant. BNY Mellon CGF stopped operating its DAF program on 2024-12-24. Funding is not public.
5. **`dafrc-sponsor-schedule-d-fy2019-2024.csv` users.**
   - AOGF's FY2026 and BBGF's CY2025 returns change the DAF/non-DAF split (§1.2). Any forward series must say whether AOGF's "other funds" column is included.
   - BBGF FY2023–24 DAF counts are blank on the filings (DAFRC imputes 441 and 460).

---

## 7. Limitations

- PPGF CY2025, NFG CY2025, CAF America FYE 2026-04, and Bright Funds and Givinga CY2025 returns were not yet in the index read for this pass.
- Platform payees are named only when a vendor is in the top-5 contractors or on Schedule R. PPGF's $12.6m of transaction costs and BBGF's card fees have no named payee.
- Benevity's own revenue is not public, so the AOGF fee cannot be expressed as a share of Benevity.
- DAF Direct's governing instrument and trustees, Givinga's employer clients and Alera's sponsor of record were not found in public sources. Business Wire pages returned 403.

---

## Source register

| ID | Source | Date | Used for | Label |
|---|---|---|---|---|
| S1 | [AOGF 990 FYE 2026-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202642259349301349_public.xml) | filed 2026-08 | Sch D split, Benevity fee, Sch O | X |
| S2 | [AOGF 990 FYE 2025-03](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533509349301608_public.xml) (amended [202641969349302754](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202641969349302754_public.xml)) | 2025-12 / 2026-07 | prior-year DAF basis | X |
| S3 | [CAF America 990 FYE 2025-04](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202610489349300906_public.xml) | 2026-02 | CyberGrants fee, Sch D | X |
| S4 | [PPGF 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml) | 2025-11 | filed FY2024, control, donated services | X |
| S5 | [BBGF 990 CY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202622529349301602_public.xml) | 2026-09 | CSRconnect note, service agreement | X |
| S6 | [NFG 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202513039349301631_public.xml) | 2025-10 | DCSO control, Bonterra fee | X |
| S7 | [Bright Funds Fdn 990 CY2024 amended](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503459349301950_public.xml); [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202433209349327603_public.xml) | 2025-12 / 2024-11 | WizeHive services, revenue drop | X |
| S8 | [Givinga Fdn 990 CY2024 amended](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503179349301975_public.xml); [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202403139349303260_public.xml) | 2025-11 / 2024-11 | Sch I clusters and intermediary grants | X |
| S9 | [Goodstack US 990 CY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml) | 2026-09 | Sch D | X |
| S10 | Every.org 990-PF [CY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202201479349100500_public.xml), [CY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333179349100048_public.xml), [CY2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423199349106002_public.xml), [CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml) | 2022–2025 | grants paid | X |
| S11 | Earlier pass-through returns FY2021–23 (object IDs in the CSV) | 2022–2024 | time series | X |
| S12 | [DAF Direct terms](https://www.dafdirect.org/popups/userAgreementPopUp.html); [About](https://www.dafdirect.org/about-daf-direct/index.html); [home](https://www.dafdirect.org/); [privacy](https://www.dafdirect.org/privacyPolicy.html); [robots.txt](https://www.dafdirect.org/robots.txt); [benefits](https://www.dafdirect.org/fundraising-benefits/index.html) | terms 2015-01-27; live 2026-11-15 | entity, sponsors, fees | F |
| S13 | [Fidelity Charitable nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/nonprofits-frequently-asked-questions.html) | live 2026-11-15 | widget still promoted | F |
| S14 | [BNY Mellon CGF 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541919349300514_public.xml) | 2025-07 | program wind-down | X |
| S15 | [Fidelity Charitable 990 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202601389349301700_public.xml); [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202521349349310887_public.xml); Schwab Charitable [FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202611199349300601_public.xml), [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202541069349300729_public.xml) | 2025–2026 | absence of DAF Direct | X |
| S16 | [markinton.com DAF DIRECT mark 85779042](https://markinton.com/trademark/daf-direct-85779042) | updated 2026-01 | trademark applicant | S |
| S17 | [Thrivent Charitable 990 CY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202612669349300236_public.xml); [CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202512589349301891_public.xml) | 2026 / 2025 | insurer-run sponsor | X |
| S18 | [KCCF 990 CY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202503219349305000_public.xml) | 2025 | insurer-run sponsor | X |
| S19 | [MDRT Foundation 990 FY2025](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202620409349301907_public.xml); [FY2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202443519349300794_public.xml) | 2026 / 2024 | no DAFs held | X |
| S20 | [Alera release, syndicated](https://windpress.info/es/press-release/945595/alera-group-partners-with-give-a-tifin-platform-to-launch-white-labeled-donor-advised-fund-platform-for-clients); [Business Wire original](https://www.businesswire.com/news/home/20251112726739/en/Alera-Group-Partners-with-Give-a-TIFIN-platform-to-Launch-White-Labeled-Donor-Advised-Fund-Platform-for-Clients) (403) | 2025-11-12 | Alera Charitable | S |
| S21 | [TIFIN Give: relationship with GiveClear](https://intercom.help/give-ria/en/articles/10104394-the-relationship-with-giveclear) | live 2026-11-15 | sponsor role | F |
| S22 | Jasper Ridge 990s: [CY2020](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202133139349302898_public.xml), [CY2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202213159349303326_public.xml), [CY2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202313149349304316_public.xml); [990-PF 2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202441279349102374_public.xml) | 2021–2024 | timeline, support test, Sch N | X |
| S23 | [PlanSource Givinga page](https://plansource.com/wealth/givinga/); [Givinga Business Wire 2025-12-11](https://www.businesswire.com/news/home/20251211023148/en) | 2026 / 2025 | Givinga partner terms | F / R |
| S24 | [Jasper Ridge aggregator profile (intellispect)](https://www.intellispect.co/organizations/472088631-jasper-ridge-charitable-fund) | n/a | 2017 SVCF grant mention | S |

---

## Data dictionary: `pass-through-sponsors-2026.csv`

One row per sponsor and fiscal year. Where a year has an original and an amended return, the row uses the return whose object ID is shown; amended means AmendedReturnInd is set.

| Column | Meaning |
|---|---|
| sponsor_id | PT-01 … PT-09 (stable within this file) |
| legal_name, ein | As on the return (EIN hyphenated) |
| platform_owner_or_vendor | Company that controls or principally serves the charity, per Schedule O / R / VII-B |
| owner_relationship | Nature of the link (sole member, class member, vendor, related taxable corp) |
| fiscal_year_end, return_type, object_id, amended | Return identifiers (IRS e-file object ID) |
| daf_count, daf_contributions_usd, daf_grants_usd, daf_eoy_value_usd | Schedule D Part I, column (a) donor advised funds; blank = not reported |
| other_funds_count, other_funds_grants_usd | Schedule D Part I, column (b) funds and other accounts |
| org_grants_paid_usd | Form 990 Part I line 13 (990-PF: Part I line 25) |
| total_revenue_usd, program_service_revenue_usd | Part I lines 12 and Part VIII line 2 total |
| platform_payee, platform_payment_usd, platform_payment_basis | Platform company paid by the charity, amount and where disclosed (VII-B contractor or Schedule R Part V; code M = services performed by the related org) |
| processing_costs_usd | Sum of Part IX "other expenses" lines naming merchant, credit-card, bank or transaction costs (fraud losses excluded) |
| dafrc_daf_grants_usd, dafrc_grants_source | DAFRC 2025 dataset value and its source flag for the same fiscal year |
| filed_minus_dafrc_usd | Filed Schedule D DAF grants minus DAFRC value (blank if either missing) |
| source_url, accessed_date, notes | XML URL; 2026-11-15; caveats |

## Data dictionary: `relationship-graph-edges-additions-19.csv`

Same columns as `relationship-graph-edges.csv`. ES001–ES023:
- ES001–ES012: pass-through control, fee and intermediary-grant edges.
- ES013–ES016: DAF Direct.
- ES017–ES019: Jasper Ridge.
- ES020–ES023: insurer and broker channel.

## Data dictionary: `queue-proposals-batch34b.csv`

Format per `queue-proposals-README.md`. P-B34B-01 (workplace reclassification), P-B34B-02 (public-support cliff screen), P-B34B-03 (NFG/DCSO).
