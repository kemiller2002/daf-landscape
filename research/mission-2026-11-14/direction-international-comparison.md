# DAF-like vehicles outside the US: UK, Canada, Australia, Europe and Israel (P-NEW-INT-01)

**Prepared 2026-11-15. Desk research only. No provider, regulator or charity was contacted, and nothing was logged into or submitted.** This is research, not legal or tax advice. Recency rule: current-state claims use 2021+ sources. Older rules are cited only where they are still in force (for example the 2019 and 2022 Australian guidelines).

**Labels.** **[F]** means the source states it directly. **[C]** is our own arithmetic on sourced figures. **[I]** is an inference or judgment. Evidence grades in the CSV: **P** = primary page fetched and read; **PS** = primary page seen only as a search-engine snippet; **S** = secondary (law firm, press, industry body); **R** = validated repo finding.

**Companion data.**
- [`data/mission-2026-11-14/international-daf-vehicles-2026.csv`](../../data/mission-2026-11-14/international-daf-vehicles-2026.csv): 34 rows covering market aggregates, rules, providers and cross-border networks, plus a US comparator row.
- [`data/mission-2026-11-14/queue-proposals-batch39-n3.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n3.csv): 3 follow-up questions (P-B39N3-01 to -03).

**Repo context and governing corrections.** We read `regulation-market-structure-portability.md` and `DAF-INDUSTRY-REPORT-2026-11.md` §6 and the governing corrections (waves 4 and 18–22). None of those corrections touch non-US vehicles. The US comparator figures used here are the validated batch-34 netted totals: FY2024 DAF grants $58.41bn and payout on prior-year corrected assets of 22.8% (report §11.14; wave 19). The NPT UK–Ren link is from report §11.2 (13 live program sites on one Ren build carry NPT or NPT UK sponsor text) (R01). On the US side, the 2023 proposed §4966 regulations are still neither final nor withdrawn, and the US has no DAF payout rule (report §6).

**Robots.txt compliance.** We read robots.txt on every host before fetching from it.
- **Not fetched; search snippets used instead:**
  - `kbs-frb.be` disallows ClaudeBot.
  - `globallawexperts.com` and `ynetnews.com` restrict Claude agents.
  - `ato.gov.au` returned 403 on robots.txt.
  - `canada.ca` and `acnc.gov.au` robots.txt timed out.
- **Allowed hosts where we read HTML only:** `cafonline.org` disallows `*.pdf`, so we read only its HTML pages.
- **Effect:** ATO and CRA rules are therefore cited through Treasury's own consultation paper (fetched) or through secondary summaries, and labelled as such.

---

## 1. Executive summary

1. **No other country studied has a statutory "DAF".** Everywhere, the vehicle is a donor-advised account inside a charity or foundation:
   - UK: an umbrella charity.
   - Canada: a registered charity, usually a public foundation.
   - Australia: a public ancillary fund, now officially called a "giving fund", which holds sub-funds.
   - Switzerland: an umbrella foundation (Dachstiftung) whose sub-funds have no legal personality.

   The legal mechanics match the US sponsor model: an irrevocable gift, a receipt, and advisory recommendations that the trustees can refuse [F: S01, S13, S29, S35].
2. **Payout floors exist abroad and are rising. The US has none.**
   - **Canada:** a charity-level disbursement quota of 3.5% on the first $1m of investment property and **5% above $1m**, for fiscal periods beginning on or after 2023-01-01 [S: S14].
   - **Australia:** public funds must distribute the greater of $8,800 or **4%**, and private funds the greater of $11,000 or **5%** [F: S23]. On 2026-02-26 the government decided to move both to **6%**, with 3-year smoothing [F: S25]. As at 2026-11-19 no amending guideline instrument is registered. F2022L00184 (4%) and F2019L01227 (5%, compilation 2) remain the operative texts, continued as giving-fund guidelines by Act No. 86 of 2026, Sch 7, items 17–18, from 2026-10-01. The 6% rate is decided, not drafted [V wave 37B]
   - **UK:** no payout rule [F: S01].
   - **The floor is never per account.** In Canada and Australia it applies at the sponsor or fund level; ACF states that its sub-fund holders have no individual minimum [F: S29].
3. **Market sizes (latest found):**

   | Market | Assets | Grants / gifts | Payout measure | Source |
   |---|---|---|---|---|
   | UK | £3.1bn (2024) | £787.7m | 28.3% (on prior year-end assets) | 10 sponsors [F: S01] |
   | Canada | C$16.64bn (2024; CRA open data C$16.67bn at 846 charities); C$18.60bn in the incomplete 2025 CRA release | C$1.92bn (2024); C$2.09bn (2025) | 12% of same-year DAF assets (11.2% in 2025; 13.3% on prior-year assets); 12.0% on prior-year assets net of gifts to other DAF sponsors [C: b39n3-0406] [V wave 38A] | 834 charities reporting DAFs on T3010 [F: S13]; 864 in the 2025 release [C: b39n3] [V wave 37B] |
   | Australia | A$10.7bn (2023) in private ancillary funds alone | n/a | n/a | 3,707 giving funds at 2025-03-03 [F: S23; S: S24] |
   | Switzerland | CHF 1.2bn (2023) of umbrella-foundation fund capital | n/a | n/a | [F: S35] |
   | US (comparator) | n/a | $58.41bn (FY2024, netted) | 22.8% | [R02] |

   - **No public asset total was found for Australian public ancillary funds or their sub-funds.**
   - **The payout definitions differ, so these rates are not like-for-like** [I].
4. **US vendors are already present abroad, but they do not dominate:**
   - **Ren:** NPT UK and the UK wealth-manager programs (R01).
   - **Foundant:** Australian Communities Foundation's fund portal, built in 2021 [F: S28].
   - **NPact:** Calgary Foundation's DonorCentral [F: S21].
   - **Blackbaud:** appears in the UK only as a processing route through Charities Trust [PS: S09].
   - **Benevity:** runs disbursing charities in the UK and Canada. It is Calgary-headquartered (Canadian, not US; repo funding data).
   - **Own platforms:** the largest consumer-facing providers run their own stacks or name no vendor. These are CAF, CHIMP, Canada Gives and APS Foundation [F/PS: S03, S19, S20, S26].
5. **The price model differs by country.**
   - **UK:** CAF charges on money *coming in*. From 2026-05-01 the example £1,000 contribution costs 4% plus 20% VAT, which is £48 [F: S03].
   - **Australia and Canada:** asset-based fees are the norm. Examples: APS 1% + GST; ACF 2.5% falling to 2.0%; Canada Gives 0.50–1.25% with a $1,500 minimum.
   - **CHIMP (Canada):** charges no account fee on cash and earns on investment accounts (0.50% / 0.25%) [F: S19, S20, S26, S30].
6. **Cross-border giving is the main source of friction.**
   - **UK:** limited UK tax reliefs to UK charities from April 2024 [F: S10].
   - **Canada:** opened grants to foreign "grantees", with accountability duties, through CRA guidance CG-032 (2023-12-19) [S: S15].
   - **Europe:** the dominant route is Giving Europe (formerly Transnational Giving Europe), with 19 countries and 12,749 donations in 2025 [F: S32].
   - **US-to-abroad:** goes through specialist sponsors such as CAF America and Myriad USA (formerly KBFUS) [S: S33].

---

## 2. Comparison table

| | **UK** | **Canada** | **Australia** | **EU / Switzerland** | **Israel** | **US (comparator)** |
|---|---|---|---|---|---|---|
| **Legal form** | Account or restricted fund inside a registered charity (umbrella charity); no statutory DAF category [F: S01] | Donor-advised accounts in a registered charity. CRA defines a DAF only for T3010 reporting: "segregated into donor accounts, owned and controlled by a registered charity" [F: S13] | Sub-fund of a Public Ancillary Fund (trust, item-2 DGR); the sub-fund is not a legal entity [F: S29, S23]. Private ancillary funds are the private-foundation analogue | Switzerland: umbrella foundation with sub-funds, no separate legal personality [S: S35, search]. Belgium: KBF holds named funds (not fetched) | Nonprofit holding DAFs; contribution receipted under Section 46 [S: S36] | Fund at a 501(c)(3) sponsor (IRC §4966) |
| **Payout rule** | None [F: S01] | Disbursement quota (DQ) on the charity: 3.5% up to $1m, 5% above $1m, from 2023 [S: S14] | Public fund: greater of $8,800 or 4%, none in the founding year and the next four years. Private fund: greater of $11,000 or 5% [F: S23]. Decided 2026-02-26: 6% for both, 3-year smoothing, 2-year grace; starts the first FY after the guidelines are amended [F: S25] | No statutory minimum payout found for Swiss umbrella foundations [I] | Not captured | None. Proposed §4966 regulations still pending [R02] |
| **Observed payout** | 28.3% (2024; grants ÷ prior year-end assets) [F: S01] | 12% (2024; DAF gifts ÷ DAF assets, same year) [F: S13] | Private funds: average 10.0% since establishment and 8.2% since 2009 (ATO data via JBWere) [S: S24] | n/a | n/a | 22.8% (FY2024, netted) [R02] |
| **Typical fees** | CAF: on contributions, 4% + VAT (example) [F: S03]. Prism: fixed quarterly fee, not published [PS: S07]. Charities Trust: 4% on card gifts plus 4% of Gift Aid [PS: S08] | CHIMP: no account fee on cash; 2.8% card fee [F: S19]. Canada Gives: 0.50–1.25% of assets, $1,500 minimum [F: S20] | APS: 1% + GST [F: S26]. ACF: 2.5% / 2.0% tiers [F: S30] | Not captured | Not captured | Mostly AUM tiers; see repo fee files |
| **Minimums** | CAF Premier DAF £50k (snippet); Charities Trust £10 a month | CHIMP $5 deposit; Gift Funds Canada $25k / $100k; Canada Gives $100k; TD PGF $10k | ACF $10k; APS $40k | Not captured | Not captured | $0 at several nationals |
| **Largest providers (size)** | CAF; NPT UK (Ren); Prism; Charities Trust. Sponsor-level sizes not captured | Charitable Gift Funds Canada $2.43bn; JCF Montreal $2.11bn; Winnipeg Fdn $1.00bn; TD PGF $0.97bn; Aqueduct (Scotia) $0.84bn; CHIMP $0.68bn (13,661 accounts) [F: S13] | APS Foundation: 725 funds, A$435m (FY2025) [F: S27]; ACF; Good2Give | Swiss Philanthropy Foundation: CHF 318m disbursed since 2006 [S]; KBF | Keshet: 183 DAFs [S: S36]; JGive | Fidelity, Schwab, NPT, Vanguard |
| **Tech vendors seen** | Ren (NPT UK); Blackbaud (via Charities Trust); Benevity (UKOGF / Charitable Giving) | NPact (Calgary Fdn); Benevity (Canadian Online Giving Foundation); proprietary (CHIMP, Canada Gives) | Foundant (ACF); Stripe (ACF cards); proprietary portal (APS) | Not identified | Not identified | Ren, Foundant, NPact, Blackbaud, CSuite, others |
| **Cross-border route** | Gift Aid only for UK charities since April 2024 [F: S10]; NPT Transatlantic and CAF American Donor Fund for US-UK dual taxpayers [S: S06; PS: S05] | Grants to "grantees" (non-qualified donees) under CG-032, reported on T1441 [S: S15] | Distributions only to item-1 DGRs (26,285 at 2025-03-03) [F: S23]; ACF pays non-DGR1 grants through a "Grants Plus" route for an extra fee [F: S30] | Giving Europe network (19 countries) [F: S32]; SPF European Cross-border Donations Fund [F] | US "friends of" charities or US DAFs [S] | Equivalency determination or expenditure responsibility; CAF America, Myriad USA |
| **Public data on DAFs** | Annual NPT UK report built from Charity Commission accounts [F: S01] | **DAF fields on the T3010 (lines 5860–5864: accounts, assets, inflows, disbursements), from 2023** [F: S13] | Treasury fund counts; ATO ancillary-fund statistics (not fetched) | CEPS umbrella-foundation survey [F: S35] | None found | Form 990 Schedule D; DAFRC report |

---

## 3. United Kingdom

**Legal form and regulation.**
- **Form:** a UK DAF is "a philanthropic fund established under an umbrella charity". The donor makes an irrevocable gift, gets immediate tax relief, and recommends grants. The sponsoring charity vets grantees and ensures compliance [F: [S01](https://www.nptuk.org/reports/daf-report/)].
- **No DAF-specific guidance:** we found no Charity Commission guidance that covers DAFs specifically.
- **General guidance does apply:**
  - The Commission's March 2024 guidance on accepting, refusing and returning donations.
  - Its grant-making due-diligence expectations.
  - A Birketts commentary stresses that host-charity trustees "retain ultimate legal control" over grant decisions [S: [S39](https://www.birketts.co.uk/legal-update/donor-advised-funds-under-pressure-lessons-from-a-us-dispute/)].
- **No payout rule** [F: S01].

**Gift Aid flows.**
- **How it works:** the charity claims an extra 25p for every £1 given. A higher-rate donor reclaims the difference through Self Assessment. Gifts qualify only up to four times the tax the donor paid [F: [S11](https://www.gov.uk/donating-to-charity/gift-aid)].
- **In a DAF:** the umbrella charity reclaims Gift Aid on the contribution. Prism illustrates £100,000 becoming £125,000 before fees [PS: [S07](https://prismthegiftfund.co.uk/faqs/)].
- **Workplace channel:** Benevity's UK partner Charitable Giving pays Gift Aid to charities quarterly, labelled "BENEVITY GIFT AID". Cross-border and unregistered recipients go through UKOGF instead [PS: [S12](https://causeshelp.benevity.org/hc/articles/31439675650196)].
- **Since April 2024:** non-UK charities are no longer eligible for UK charitable reliefs. Income Tax and CGT relief ran to 2024/25, and higher-rate relief on gifts to non-UK charities ended. About 20 EU/EEA charities were affected [F: [S10](https://gov.uk/government/publications/restriction-of-charitable-reliefs-to-uk-charities-and-community-amateur-sports-clubs/restriction-of-charitable-reliefs-to-uk-charities)].

**Market size** [F: S01; PS: [S02](https://nptuk.org/2024-uk-daf-report-ukn)]:

| Data year | Assets | Grants | Contributions | Payout | Sponsors in sample |
|---|---|---|---|---|---|
| 2023 | £2.8bn | £645.4m | £852.6m | 25.7% | 11 |
| 2024 | £3.1bn (+10.3%) | £787.7m (+22.1%) | £864.5m (+1.4%) | 28.3% | 10 |

2020–24 CAGRs: assets 13.2%, grants 16.0%. NPT UK does not name the sponsors in its sample.

**Providers.**
- **CAF Gift Aid Charity Account:**
  - **Fee basis:** fees fall on money coming in, not on grants. Fees are reviewed every 1 May.
  - **Change on 2026-05-01:** six bands became five, and CAF began charging VAT on its full fee. The £1,000 example went from 4.5% (£45) to 4% + VAT (£48). CAF says the overall cost to clients rises [F: [S03](https://www.cafonline.org/personal-giving/effective-ways-to-give/giving-account/changes-to-gift-aid-charity-account-fees-from-1-may-2026)].
  - **Comparison page:** lists 4.5% on the first £150,000 (GAYE 4%), charged on cumulative 12-month donations. Non-UK residents are not eligible. Overseas giving carries extra charges [F: [S04](https://www.cafonline.org/personal-giving/resources/compare-giving-vehicles)].
- **CAF Donor Advised Gift and Charitable Trust:**
  - Donor Advised Gift: 4% on the first £150,000 of each donation.
  - Charitable Trust: 1.4% on the first £100,000 of average daily balance. It is the only CAF vehicle that can invest, and it holds USD and EUR.
  - Minimum fee: £400 or £600. The page does not map each amount to a vehicle [F: S04].
  - CAF American Donor Fund: 4.5% on the first £50,000; Premier DAF minimum £50k, with a £2,000 a year minimum charge [PS: [S05](https://www.cafonline.org/cadf/fees)].
- **NPT UK and NPT Transatlantic:**
  - Grants: "£84 million" in grants "last year" (press-release headline; very likely FY2023, since NPT Transatlantic's £68m and NPT UK's £16m for FY23 in the 2023 grantmaking report sum to £84m [I]) [V wave 35B] [S: [S06](https://prnewswire.co.uk/news-releases/donors-made-84-million-in-grants-from-npt-uk-and-npt-transatlantics-donor-advised-funds-last-year-302071231.html)].
  - Technology: runs on Ren, as do the Rathbones and Cazenove Capital programs (R01).
- **Prism the Gift Fund:** charges a fixed quarterly fee set by the level of administration, plus an opening fee. Prices are not published [PS: S07].
- **Charities Trust:**
  - Payroll giving: 25p per donor per month.
  - Card donations: 4%, plus 4% of the Gift Aid claimed.
  - "My Giving Account": £10 a month minimum [PS: [S08](https://charitiestrust.org/services/all/donation-handling)].
  - Blackbaud link: a Blackbaud CSRconnect help page documents Charities Trust processing, with a 4.99% invoiced fee for one partner arrangement [PS: [S09](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/csrc-global-processing-charities-trust.html)].

---

## 4. Canada

**Legal form.**
- **Form:** there is "no such thing as an entity being a DAF in Canada", only registered charities that hold donor-advised accounts [F: [S13](https://carleton.ca/profbrouard/wp-content/uploads/sites/281/2026/10/reportBlumbergPasha2026DAFReportDonorAdvisedFundaccounts2024Final.pdf)].
- **CRA definition:** in the T3010 guide, a DAF is a fund segregated into donor accounts, owned and controlled by the charity. The charity has "sole responsibility" for payouts [F: S13].

**Rules.**
- **Disbursement quota (DQ):** the rate is 5% on investment property above $1m and 3.5% below it. It applies to fiscal periods beginning on or after 2023-01-01, and was enacted by Bill C-32 (Royal Assent 2022-12-15) [S: [S14](https://crowe.com/ca/crowemackay/insights/2022-federal-budget-summary); [pfc.ca](https://pfc.ca/new-disbursement-quota-is-now-law-and-in-force-what-you-need-to-know/)].
- **The DQ is charity-level** [I]. A sponsor can meet it in aggregate while individual accounts pay nothing.
- **Grantee regime:**
  - **What it allows:** since the 2022 amendments, charities can make "qualifying disbursements" to non-qualified donees ("grantees") if they meet accountability requirements. CRA's final guidance is CG-032 (2023-12-19), and these grants are reported on Form T1441.
  - **Purpose limit:** a charity whose only purpose is gifts to qualified donees must first amend its purposes [S: [S15](https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/policies-guidance/charities-making-grants-non-qualified-donees.html) (not fetched; robots.txt timed out); [Miller Thomson](https://www.millerthomson.com/en/insights/social-impact/cra-releases-final-guidance-on-qualifying-disbursements-an-in-depth-look-for-canadian-registered-charities)].
  - **Effect:** this is a direct cross-border route that US sponsors handle through equivalency determination or expenditure responsibility [I].

**Market size (T3010 v24, 2024)** [F: S13]:

| Measure | Value | Note |
|---|---|---|
| Charities reporting DAFs | 834 | |
| DAF assets | $16,644,279,820 | |
| Donations in | $3,280,632,301 | |
| Gifts out | $1,918,665,555 | 58% of donations |
| Gifts ÷ assets | 12% | |
| Accounts | 185,506 | Authors call this "highly exaggerated by transpositional errors" |
| Average account | $89,724 | Inflated denominator: the CRA 2024 release has 186,421 accounts as filed but 60,419 once 14 impossible returns are removed, giving an average of C$275,905 [C: b39n3] [V wave 37B] |

- **Other figures:**
  - The WellFunded database: **$17.3bn** across 205 sponsors on the "most recent" T3010s, with the top ten holding 66% [S: [S37](https://futureofgood.co/new-database-maps-canadas-17-3-billion-daf-landscape-and-where-philanthropic-wealth-is-concentrated/), 2026-08-10].
  - Veritas Foundation: top five hold 73% (search snippet, not fetched) [S: S41].
- **Our own check:** the top five by DAF assets in the Blumberg list hold $7.36bn, which is **44%** [C: S13]. The definitions clearly differ (P-B39N3-01).

**Providers** (2024 T3010 DAF figures [F: S13]; other details as cited):

| Provider | DAF assets | Accounts | Other details |
|---|---|---|---|
| Charitable Gift Funds Canada | $2.43bn | 3,306 | Minimum $25k (Classic) / $100k (Flex), from a development-subdomain FAQ [PS: S16] |
| Jewish Community Foundation of Montreal | $2.11bn | 2,275 | Faith community foundation |
| TD Private Giving Foundation | $0.97bn | 1,956 | Minimum $10k [PS: S17] |
| Aqueduct (Scotia Private Client Group) | $0.84bn | 645 | Minimum $250k in an article of unverified date [S: S18] |
| CHIMP (Charitable Impact) | $0.68bn | 13,661 | Average $49,518. Consumer model: no sign-up, transaction or balance fees; 2.8% card fee; investment account 0.50% on the first $1m and 0.25% above (page updated 2026-07-15) [F: [S19](https://help.charitableimpact.com/article/136-fees)] |
| Canada Gives | $0.33bn | 339 | Minimum $100k; 0.50–1.25% of assets with a $1,500 minimum; the adviser keeps the assets on book [F: [S20](https://canadagives.ca/wp-content/uploads/2025/11/CG-FAQs.pdf)] |
| Calgary Foundation | $0.57bn | not shown | Runs NPact [F: [S21](https://calgaryfoundation.org/giving/donor-central/)] |
| Canadian Online Giving Foundation (Benevity's disbursing charity) | $23.6m | 8,648 | Took in $173.2m and gave out $171.1m: a pure pass-through [F: S13; PS: [S22](https://causes.benevity.org/causes/124-862216165RR0001?lang=en)] |

---

## 5. Australia

**Legal form.**
- **What a giving fund is:** a giving fund ("ancillary fund" in tax law) is a trust that is an item-2 DGR. It exists solely to provide money to item-1 DGRs.
- **Two types:** public giving funds must solicit the public. Private giving funds are limited to founders and their associates [F: [S23](https://storage.googleapis.com/files-au-treasury/treasury/p/prj35cf5f03f7cd51c704285/page/c2025_667008_cp.pdf)].
- **The DAF analogue:** a sub-fund (APS "giving fund", ACF "Named Fund") inside a public fund. It "is not a legal entity, and the sub-fund holder is not the Trustee" [F: [S29](https://communityfoundation.org.au/giving/faqs)].

**Distribution rules.**
- **Current rules:**
  - Public fund: greater of $8,800 or 4% of prior year-end net assets. No distribution is required in the founding year or the following four years.
  - Private fund: greater of $11,000 or 5%. No distribution is required in the founding year [F: S23].
- **Reform timeline:**
  - **2024-12-05:** the government announced it would align and raise the rates, allow three-year smoothing and rename the funds "giving funds" [F: S23].
  - **2025-06-10:** Treasury opened consultation, which closed 2025-08-01 [F: [S38](https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/more-give-new-giving-fund-rules-aim-boost-charity)].
  - **2026-02-26:** Assistant Minister Leigh set the minimum annual distribution for public and private giving funds at **6% of net assets**, with three-year smoothing. Existing funds have two years before they must comply. The rule applies "from the first financial year following amendments to the giving fund guidelines" [F: [S25](https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/boosting-support-australian-charities)].
- **Status:** Philanthropy Australia treats the guideline amendments as still to come [S: [S40](https://www.philanthropy.org.au/explainer-changes-to-the-minimum-distribution-for-giving-funds/)]. We did not find the amended instrument (P-B39N3-02). This was confirmed on the Federal Register of Legislation on 2026-11-19: no title contains “Giving Fund”, and neither guideline has a compilation after 2022. Only the rename has commenced (C2026A00086, Sch 7, 2026-10-01) [V wave 37B]
- **Discrepancy:** the June 2025 paper said the higher rate would not apply for five years after amendment. The February 2026 release says two years [F: S23, S25].
- **Sub-funds:** sub-fund holders at ACF have no individual minimum. ACF must distribute 4% at the consolidated trust level [F: S29]. APS asks each giving fund to give 4% [F: [S26](https://www.australianphilanthropicservices.com.au/faqs-aps-foundation/)].

**Market size.**
- **Fund counts:** 3,707 giving funds at 2025-03-03 (2,292 private, 1,415 public) [F: S23].
- **Private funds:** net assets $10.7bn and cumulative distributions $6.8bn (2023). There were 2,388 PAFs at June 2025, all per JBWere citing ATO data [S: [S24](https://www.jbwere.com.au/content/dam/jbwere/documents/campaigns/JBWere-Submission-Giving-Fund-Reforms.pdf)].
- **Gaps:** no total for public-fund assets or sub-fund counts was found.

**Providers.**
- **APS Foundation:**
  - Terms: $40k minimum; 1% + GST (net 1.025%); its own online portal [F: S26].
  - Size: 725 giving funds and $435m under management, with 7,279 gifts in FY2025 [F: [S27](https://www.australianphilanthropicservices.com.au/giving-and-growth-snapshot-2025/)]. A later snippet says more than 845 funds and more than $512m (not fetched).
- **Australian Communities Foundation:**
  - Terms: Named Fund minimum $10k; fees 2.5% up to $100k and 2.0% from $100k to $1m [F: [S30](https://communityfoundation.org.au/giving/fees)].
  - Technology: the fund portal was built with **Foundant Technologies** (2021-08-02) [F: [S28](https://communityfoundation.org.au/article/introducing-a-new-portal-to-manage-your-fund/)].
- **Good2Give:** a workplace-giving intermediary and trustee of public ancillary funds. It reports $275m delivered since 2001 [S: [S31](https://good2give.ngo/about/news/good2give-and-workplace-giving-australia-merge-to-transform-australias-giving-landscape/)].

---

## 6. Europe, Switzerland and Israel

- **Giving Europe (formerly Transnational Giving Europe):**
  - **Rebrand and reach:** renamed 2026-02-10. It operates across 19 countries and lists more than 1,800 registered nonprofits.
  - **Activity in 2025:** 12,749 donations, supporting 512 organisations [F: [S32](https://giving.eu/)].
  - **Mechanism:** the donor gives to the network member in their own country and receives a home-country receipt; the member in the recipient's country then regrants.
  - **Fees:** not shown on the homepage.
- **King Baudouin Foundation / Myriad USA:**
  - KBF's US affiliate (formerly KBFUS) now operates as Myriad USA, an alliance with Give2Asia. It offers US DAFs and "Friends Funds" for overseas giving [S: [S33](https://kbfus.org/introducing-myriad-the-alliance-for-borderless-giving/)].
  - KBF helped found Transnational Giving Europe [S: [S34](https://www.influencewatch.org/non-profit/king-baudouin-foundation-united-states-kbfus/)].
  - KBF's own site was not fetched (robots.txt).
- **Swiss umbrella foundations:**
  - **Size:** cumulative fund capital of CHF 1.2bn in 2023, which is "just over one per cent" of Swiss foundation assets [F: [S35](https://ceps.unibas.ch/fileadmin/user_upload/ceps/1_Home/Philanthropie_Aktuell/PA_25_01_en_final.pdf), CEPS March 2025].
  - **Swiss Philanthropy Foundation:** describes itself as an umbrella foundation (donor-advised fund) and offers a European Cross-border Donations Fund [F: [swissphilanthropy.ch](https://www.swissphilanthropy.ch/en/our-foundation)]. A secondary source says it has disbursed CHF 318m since 2006 [S].
  - **Payout:** no statutory minimum payout was found [I].
- **Israel:**
  - Keshet (founded 2019; 183 DAFs) and JGive offer Israeli DAFs, with a Section 46 receipt issued on contribution [S: [S36](https://www.calcalistech.com/ctechnews/article/kl0b1eyki)].
  - Secondary sources describe a 35% credit capped at 30% of taxable income.
  - These are low-confidence secondary snippets. Israel matters to US providers mainly through US "friends of" charities and Jewish community foundations [I].

---

## 7. Lessons for a US AI-native entrant [I unless cited]

1. **Build payout analytics in from day one.** Every peer market studied has, or is adopting, a sponsor-level floor: Canada 5% above $1m, and Australia 4%/5% today, with 6% and smoothing decided but not yet in any registered instrument at 2026-11-19 [V wave 37B]. Canada's quota (3.5% to C$1m, 5% above, on a 24-month average) is charity-level and rarely binds on DAF sponsors: in the 2025 release 13 of the top-20 meet it from DAF disbursements net of sponsor transfers [V wave 38A] Smoothing, Commissioner reductions and a charity-level DQ create the same work a US rule would: account-level dormancy tracking and aggregate floor management. An entrant that can show per-account payout and simulate the floor is ready if the US moves.
2. **The large consumer models abroad ran their own stacks.**
   - **Own stacks:** CHIMP, Canada Gives, CAF and APS run their own platforms or name no vendor.
   - **Where US vendors appear:** Ren, Foundant and NPact are concentrated at adviser-channel and community-foundation sponsors (NPT UK, ACF, Calgary).
   - **Implication:** a US entrant could sell infrastructure abroad in two ways. It could go through community-foundation and wealth-manager channels, or partner with a local sponsor, since a local charity is legally required to hold the funds.
3. **Fee design.**
   - **Two dominant models:** the UK contribution-based model (charges at entry, plus VAT since May 2026) and the Australian and Canadian AUM model.
   - **The CHIMP alternative:** free on cash, with revenue from investment accounts. It has the most accounts in Canada (13,661) but a small average account [F: S13, S19].
   - **Implication:** there is no single "right" fee; the economics depend on channel.
4. **Cross-border compliance is a product opportunity.** Several jurisdictions now require accountability checks for cross-border giving:
   - the UK's territorial relief rule (2024);
   - Canada's grantee accountability regime (CG-032);
   - Australia's DGR-1-only distribution rule.

   Document collection, recipient vetting and reporting (T1441-style) can be automated. ACF already prices non-DGR1 grants as a premium service [F: S30].
5. **Canada now publishes DAF data comparable to the US.**
   - Since 2023, the T3010 asks every charity for its DAF accounts, assets, inflows and disbursements, which is broadly the same set as US Form 990 Schedule D Part I.
   - The UK and Australia have no equivalent return field. UK totals come from NPT UK reading annual accounts, and Australian sub-funds are invisible.
   - **Implication:** Canada is the one foreign market where the repo's 990-style sponsor benchmarking can be repeated (P-B39N3-01). Note that the account counts carry known filing errors [F: S13].
6. **Pass-through vehicles are a feature of corporate giving everywhere.** Examples include Benevity's Canadian Online Giving Foundation (99% gifts-to-donations) and its UK partners. They inflate account counts, as in the US repo finding that processors hold 79.5% of US accounts.
7. **Do not read across payout rates.** The UK 28.3%, Canadian 12% and US 22.8% figures use different numerators and denominators. Canadian figures also include DAF-to-DAF transfers, which the authors flag [F: S13]. Netting gifts to other line-5860 = Y sponsors lowers Canada's 2025 prior-year-asset payout from 13.3% to 12.0% [C: b39n3-0406] [V wave 38A]

---

## 8. Gaps and caveats

- **Not found:**
  - UK sponsor-level sizes (CAF, Prism, Charities Trust).
  - CAF's and Prism's technology vendors.
  - Australian public-fund asset totals and sub-fund counts.
  - Giving Europe fees and euro volumes.
  - KBF primary pages.
  - Israeli primary data.
- **CRA and ATO pages:** cited through summaries or Treasury's paper, because of robots.txt or connectivity.
- **Weakly sourced figures:**
  - The Charitable Gift Funds Canada minimums come from a development subdomain.
  - The Aqueduct $250k minimum comes from an article of unverified date.
- **Benevity** is Calgary-headquartered (repo funding data), so it is a Canadian rather than a US vendor.

---

## Source register

| ID | Source | URL | Grade | Accessed |
|---|---|---|---|---|
| S01 | NPT UK, The 2025 DAF Report (2024 data) | https://www.nptuk.org/reports/daf-report/ | P | 2026-11-15 |
| S02 | NPT UK, 2024 DAF Report page (2023 data) | https://nptuk.org/2024-uk-daf-report-ukn | PS | 2026-11-15 |
| S03 | CAF, changes to Gift Aid Charity Account fees from 1 May 2026 | https://www.cafonline.org/personal-giving/effective-ways-to-give/giving-account/changes-to-gift-aid-charity-account-fees-from-1-may-2026 | P | 2026-11-15 |
| S04 | CAF, compare giving vehicles | https://www.cafonline.org/personal-giving/resources/compare-giving-vehicles | P | 2026-11-15 |
| S05 | CAF American Donor Fund fees | https://www.cafonline.org/cadf/fees | PS | 2026-11-15 |
| S06 | PR Newswire UK, NPT UK/Transatlantic £84m grants | https://prnewswire.co.uk/news-releases/donors-made-84-million-in-grants-from-npt-uk-and-npt-transatlantics-donor-advised-funds-last-year-302071231.html | S (headline) | 2026-11-15 |
| S07 | Prism the Gift Fund FAQs / fee article | https://prismthegiftfund.co.uk/faqs/ ; https://prismthegiftfund.co.uk/?p=2460 | PS | 2026-11-15 |
| S08 | Charities Trust, donation handling | https://charitiestrust.org/services/all/donation-handling | PS | 2026-11-15 |
| S09 | Blackbaud CSRconnect help, Charities Trust processing | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/csrconnect-prod/content/csrc-global-processing-charities-trust.html | PS | 2026-11-15 |
| S10 | HMRC policy paper, restriction of charitable reliefs to UK charities (2023-03-15) | https://gov.uk/government/publications/restriction-of-charitable-reliefs-to-uk-charities-and-community-amateur-sports-clubs/restriction-of-charitable-reliefs-to-uk-charities | P | 2026-11-15 |
| S11 | GOV.UK, Gift Aid | https://www.gov.uk/donating-to-charity/gift-aid | P | 2026-11-15 |
| S12 | Benevity Causes help, Gift Aid / UKOGF | https://causeshelp.benevity.org/hc/articles/31439675650196 ; https://causeshelp.benevity.org/hc/en-gb/articles/360055709732 | PS | 2026-11-15 |
| S13 | Blumberg & Pasha, Blumbergs DAF Report: DAF accounts in 2024 (2026-02-10) | https://carleton.ca/profbrouard/wp-content/uploads/sites/281/2026/10/reportBlumbergPasha2026DAFReportDonorAdvisedFundaccounts2024Final.pdf | P | 2026-11-15 |
| S14 | Crowe MacKay, 2022 federal budget summary (DQ); PFC, new DQ in force | https://crowe.com/ca/crowemackay/insights/2022-federal-budget-summary ; https://pfc.ca/new-disbursement-quota-is-now-law-and-in-force-what-you-need-to-know/ | S | 2026-11-15 |
| S15 | CRA CG-032 grants to non-qualified donees; Miller Thomson summary | https://www.canada.ca/en/revenue-agency/services/charities-giving/charities/policies-guidance/charities-making-grants-non-qualified-donees.html ; https://www.millerthomson.com/en/insights/social-impact/cra-releases-final-guidance-on-qualifying-disbursements-an-in-depth-look-for-canadian-registered-charities | S | 2026-11-15 |
| S16 | Charitable Gift Funds Canada FAQ (dev subdomain) | https://giftfundsdev.garo.ca/resources/faqs | PS | 2026-11-15 |
| S17 | TD Private Giving Foundation brochure | https://www.td.com/ca/document/PDF/tdw-pgf-brochure.pdf | PS | 2026-11-15 |
| S18 | Aqueduct Foundation (CanadaHelps listing; Investment Executive snippet) | https://www.canadahelps.org/en/charities/aqueduct-foundation/ | S | 2026-11-15 |
| S19 | Charitable Impact, fees (updated 2026-07-15) | https://help.charitableimpact.com/article/136-fees | P | 2026-11-15 |
| S20 | Canada Gives FAQ PDF | https://canadagives.ca/wp-content/uploads/2025/11/CG-FAQs.pdf | P | 2026-11-15 |
| S21 | Calgary Foundation DonorCentral | https://calgaryfoundation.org/giving/donor-central/ | P | 2026-11-15 |
| S22 | Benevity cause page, Canadian Online Giving Foundation | https://causes.benevity.org/causes/124-862216165RR0001?lang=en | PS | 2026-11-15 |
| S23 | Treasury (AU), Giving fund reform: distribution rate and smoothing, consultation paper (June 2025) | https://storage.googleapis.com/files-au-treasury/treasury/p/prj35cf5f03f7cd51c704285/page/c2025_667008_cp.pdf ; https://consult.treasury.gov.au/c2025-667008 | P | 2026-11-15 |
| S24 | JBWere submission, Giving Fund Reforms (2025-07-31) | https://www.jbwere.com.au/content/dam/jbwere/documents/campaigns/JBWere-Submission-Giving-Fund-Reforms.pdf | S | 2026-11-15 |
| S25 | Assistant Minister Leigh, Boosting support for Australian charities (2026-02-26) | https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/boosting-support-australian-charities | P | 2026-11-15 |
| S26 | APS Foundation FAQ | https://www.australianphilanthropicservices.com.au/faqs-aps-foundation/ | P | 2026-11-15 |
| S27 | APS giving and growth snapshot 2025 | https://www.australianphilanthropicservices.com.au/giving-and-growth-snapshot-2025/ | P | 2026-11-15 |
| S28 | ACF, new portal to manage your fund (2021-08-02) | https://communityfoundation.org.au/article/introducing-a-new-portal-to-manage-your-fund/ | P | 2026-11-15 |
| S29 | ACF giving FAQs | https://communityfoundation.org.au/giving/faqs | P | 2026-11-15 |
| S30 | ACF fees | https://communityfoundation.org.au/giving/fees | P | 2026-11-15 |
| S31 | Good2Give merger news | https://good2give.ngo/about/news/good2give-and-workplace-giving-australia-merge-to-transform-australias-giving-landscape/ | S | 2026-11-15 |
| S32 | Giving Europe (formerly TGE) homepage | https://giving.eu/ | P | 2026-11-15 |
| S33 | Myriad USA introduction | https://kbfus.org/introducing-myriad-the-alliance-for-borderless-giving/ | S (snippet) | 2026-11-15 |
| S34 | InfluenceWatch, KBFUS | https://www.influencewatch.org/non-profit/king-baudouin-foundation-united-states-kbfus/ | S (snippet) | 2026-11-15 |
| S35 | CEPS Basel, Philanthropie Aktuell #01/25 (March 2025) | https://ceps.unibas.ch/fileadmin/user_upload/ceps/1_Home/Philanthropie_Aktuell/PA_25_01_en_final.pdf | P | 2026-11-15 |
| S36 | Calcalist, Keshet; Pearl Cohen on Israeli tax credit | https://www.calcalistech.com/ctechnews/article/kl0b1eyki ; https://www.pearlcohen.com/israel-tax-authority-clarify-a-long-awaited-position-tax-credit-that-also-benefit-u-s-person/ | S (snippet) | 2026-11-15 |
| S37 | Future of Good, $17.3bn DAF landscape database (2026-08-10) | https://futureofgood.co/new-database-maps-canadas-17-3-billion-daf-landscape-and-where-philanthropic-wealth-is-concentrated/ | S | 2026-11-15 |
| S38 | Assistant Minister Leigh, new giving fund rules consultation (2025-06-10) | https://ministers.treasury.gov.au/ministers/andrew-leigh-2025/media-releases/more-give-new-giving-fund-rules-aim-boost-charity | P | 2026-11-15 |
| S39 | Birketts, DAFs under pressure | https://www.birketts.co.uk/legal-update/donor-advised-funds-under-pressure-lessons-from-a-us-dispute/ | S (snippet) | 2026-11-15 |
| S40 | Philanthropy Australia explainer | https://www.philanthropy.org.au/explainer-changes-to-the-minimum-distribution-for-giving-funds/ | S | 2026-11-15 |
| S41 | Veritas Foundation annual DAF update | https://theveritasfoundation.com/resource/dm/203114603659182176 | S (snippet) | 2026-11-15 |
| R01 | Repo: DAF-INDUSTRY-REPORT-2026-11.md §11.2 (Ren build with NPT / NPT UK sponsor text) | ../DAF-INDUSTRY-REPORT-2026-11.md | R | 2026-11-15 |
| R02 | Repo: DAF-INDUSTRY-REPORT-2026-11.md §6 and §11.14 (netted FY2024 grants, 22.8% payout; §4966 status) | ../DAF-INDUSTRY-REPORT-2026-11.md | R | 2026-11-15 |

---

## Data dictionary

### `international-daf-vehicles-2026.csv`

| Column | Meaning |
|---|---|
| row_id | I01–I34 |
| country | Jurisdiction (UK, Canada, Australia, EU, EU/US, Switzerland, Israel, US (comparator)) |
| entity_or_rule | Provider, rule or market aggregate described |
| row_type | `market_aggregate`, `rule`, `provider` or `cross_border_network` |
| legal_form | Legal vehicle holding the donor-advised money |
| payout_rule | Minimum distribution rule that applies (and at what level) |
| payout_rule_status | In force, proposed or decided-not-yet-amended, with dates |
| fees | Published fees as stated; "not captured" if not found |
| minimum_to_open | Opening or balance minimum as stated |
| size_metric | Semicolon-separated list of measures reported in size_value |
| size_value | Values in the same order as size_metric; local currency unless size_currency says "count" |
| size_currency | GBP, CAD, AUD, CHF, USD or count |
| data_year | Year (or date) the size figures refer to |
| tech_vendor | Technology vendor named in a source; "not identified" if none found |
| us_vendor_present | Whether a US vendor (Ren, Foundant, NPact, Blackbaud) is evidenced; Benevity noted as Canadian |
| cross_border_route | How money can leave the jurisdiction or arrive from abroad |
| source_id | IDs in this document's source register |
| source_url | Main URL for the row |
| evidence_grade | P, PS, S, R (see header); "P/PS" means the size is P and other fields PS |
| notes | Caveats, definitions and conflicts |

### `queue-proposals-batch39-n3.csv`

Columns and scales follow [`queue-proposals-README.md`](../../data/mission-2026-11-14/queue-proposals-README.md). There are three rows, P-B39N3-01 to -03, all with state `open`.

## Validation corrections (wave 24A, 2026-11-15) — governing
Source: [validation-wave24a-report.md](validation-wave24a-report.md); register `data/mission-2026-11-14/validation-register-wave24a.csv`.

1. **§3, Gift Aid flows.**
   - **Find:** "Income Tax and CGT relief ran to 2024/25, and higher-rate relief on gifts to non-UK charities ended."
   - **Replace with:** "The measure applied from 15 March 2023 to charities not already recognised. For existing EU/EEA charities HMRC's transition ran \"until 1 April 2024\" for Corporation Tax, IHT, SDLT and other taxes and \"until tax year 2024/25\" for Income Tax and CGT; Gift Aid and higher-rate relief on gifts to non-UK charities then ended [V wave 24A]."
2. **§5, Market size.**
   - **Find:** "- **Fund counts:** 3,707 giving funds at 2025-03-03 (2,292 private, 1,415 public) [F: S23]."
   - **Replace with:** "- **Fund counts:** 3,707 giving funds at 2025-03-03 (2,292 private, 1,415 public) [F: S23]. JBWere's 2,388 PAFs (June 2025, S24) is a different date and source [V wave 24A]."
3. **§1 market table, Australia row.**
   - **Find:** "| Australia | A$10.7bn (2023) in private ancillary funds alone | n/a | n/a | 3,707 giving funds at 2025-03-03 [F: S23; S: S24] |"
   - **Replace with:** "| Australia | A$10.7bn (2023) in private ancillary funds alone [S: S24] | n/a | n/a | 3,707 giving funds at 2025-03-03 [F: S23] |"
