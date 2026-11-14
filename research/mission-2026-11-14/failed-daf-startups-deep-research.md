# Failed, Acquired, Pivoted and Stalled DAF and Philanthropy-Fintech Ventures: Case Files and Cross-Case Patterns

**Research date:** 2026-11-14. **Status:** desk research using public sources only. No dockets, private filings or company data rooms were accessed.
**Dataset:** [`data/mission-2026-11-14/failed-daf-startups.csv`](../../data/mission-2026-11-14/failed-daf-startups.csv). It has 50 investigated cases: 35 with an observed outcome and 15 investigated where no adverse outcome was found or the entity could not be identified.
**Queue proposals:** [`data/mission-2026-11-14/queue-proposals-failed-startups.csv`](../../data/mission-2026-11-14/queue-proposals-failed-startups.csv)
**Builds on, does not repeat:** [technology audit and provider exits](../daf-technology-audit-and-provider-exits-2026-11-11.md) (cases X01–X11), [historical lifecycle ledger](../historical-daf-sponsor-technology-lifecycle-2011-2026.md) (EV01–EV24), [competitive history timelines](competitive-history-timelines.md), [startup scan](../startups-and-emerging-competitors-2026-11-12.md). Cases already documented there appear here only as reference rows, with their prior IDs. This file adds 25 new cases and extends Flipcause and The Giving Block with new primary evidence.
**Method rules** ([application guide](clarity-edf-application-guide.md)):
- EDF origin networks are drawn only for observed adverse outcomes such as a shutdown, an insolvency or a regulator order.
- Acquisitions and survivors are recorded without inventing causes.
- Each origin is marked **E:** (evidence: stated in a source) or **I:** (inference by this analyst).
- Clarity confidence labels are qualitative.

---

## 1. Executive summary

1. **Core DAF entities rarely fail visibly. When they do, it is a sponsor-governance event, not a technology failure.**
   - Across 50 investigated names, only two *core DAF sponsors* have an observed adverse outcome:
     - National Heritage Foundation: 2009 Chapter 11, 2011 IRS revocation, and a wind-down by 2022 (prior repo EV02–EV09).
     - **SDG Impact Fund** (new in this file). In 2026 the Georgia Secretary of State barred it from operating as a charity. The order alleges misappropriation and commingling, and it became final when no hearing was requested ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)). The Georgia AG then sued and is seeking a receiver ([WSB-TV, 2026-09-25](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)).
   - No venture-backed consumer DAF app was found to have shut down.
   - Confidence: Medium. This is likely to be partly a coverage artefact (see §6).
2. **The dominant exit for DAF *technology* startups is acquisition by a consolidator, usually for the plumbing.**
   - Six DAF-tech companies were bought by Ren, Foundation Source or TIFIN: Crown/DonorFirst, Pinkaloo, Amicus.io, Stellar/iPhi, Vennfi and Giving Place.
   - No public disclosure of what happened to the acquired codebases was found for any of them.
   - Amicus.io raised an $8.7M Series B in 2020 to embed DAFs in consumer banking apps ([Crunchbase News](https://news.crunchbase.com/news/making-philanthropy-as-easy-as-banking-amicus-io-raises-8-7m-series-b)). Sixteen months later TIFIN acquired it to provide a "modern set of pipes" for an advisor platform ([InvestmentNews, 2022-03](https://www.investmentnews.com/fintech/tifin-group-acquires-fintech-targeting-donor-advised-funds/218849)).
   - Confidence: Medium-High that acquisition is the modal outcome among *documented* DAF-tech exits.
3. **Where money was lost, the cause was in the payments or custody layer, not the DAF ledger.**
   - Ammado (2018 liquidation, about €3.8M in donations reported unaccounted for) ([UK Fundraising, 2018-02-01](https://fundraising.co.uk/2018/02/01/ammado-liquidation-e3-8bn-donations-unaccounted-for/)).
   - Flipcause (more than $29M owed to more than 3,200 organizations, $70k cash on hand) ([NPQ, 2026-03-13](https://nonprofitquarterly.org/nonprofits-in-limbo-as-flipcause-bankruptcy-unfolds/)).
   - SDG Impact Fund (alleged commingling).
   - In all three, a single operator controlled donor money that was not legally or operationally segregated.
   - Confidence: High for the observed cases. Their causes are not adjudicated.
4. **Crypto exposure behaves like a cyclical revenue line, not a moat.**
   - Shift4 bought The Giving Block with up to $246M of earnout. In FY2022 it recorded a **$(47.1)M** fair-value reduction to that earnout, attributed to lower projected revenue. The remaining liability was $10.9M at year-end 2022 ([Shift4 FY2022 10-K financial report, SEC](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/Financial_Report.xlsx)).
   - The Giving Block cut about 12% of staff after FTX collapsed ([The Block, 2023-01](https://www.theblock.co/post/203351/the-giving-block-cuts-about-12-of-its-workforce)).
   - Endaoment, the crypto-native DAF, survived and moved toward advisor distribution ([InvestmentNews, 2026-10-06](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481)).
   - Confidence: High for the facts, Medium for generalization.
5. **Giving products owned by large corporations die when the parent reprioritizes.** Five products closed between 2019 and 2023, each for reasons of adoption or strategy, not because of any failure in the giving itself:
   - Google One Today ([9to5Google, 2020-01-29](https://9to5google.com/2020/01/29/google-one-today-donation-killed/))
   - AmazonSmile ([GBH/AP, 2023-01-19](https://www.wgbh.org/news/national/2023-01-19/amazon-ends-its-charity-donation-program-following-other-cost-cutting-efforts))
   - GoFundMe Charity ([NonProfit Times, 2021-02-10](https://thenonprofittimes.com/technology/gofundme-charity-being-shut-down/))
   - Virgin Money Giving ([UK Fundraising, 2021-08-26](https://fundraising.co.uk/2021/08/26/virgin-money-giving-to-close-in-november/))
   - BT MyDonate ([UK Fundraising, 2019-01-21](https://fundraising.co.uk/2019/01/21/bt-mydonate-close-june/))
6. **The repeated strategic move is a channel pivot, not product death.** Startups move from consumer to employer to bank or advisor:
   - Pinkaloo (bank white-label pilot) ([Technical.ly, 2019-07-19](https://technical.ly/baltimore/2019/07/19/masschallenge-fintech-accelerator-pinkaloo-launches-charitable-giving-pilot-eastern-bank))
   - Philanthropi (employers to banks) ([Payments Dive, 2022-07-08](https://www.paymentsdive.com/news/fintech-philanthropi-taps-into-giving-surge-payments/626794/))
   - Bright Funds (consumer "charity mutual funds" to workplace giving) ([TechCrunch, 2012-11-26](https://techcrunch.com/2012/11/26/mutual-funds-for-non-profits-bright-funds-wants-to-be-the-vanguard-for-charitable-giving))
   - Groundswell (DAF-as-benefit to a CSR suite) (prior repo)
   - GoodWorld (hashtag donations to B2B software) ([GoodWorld site, reviewed 2026-11-14](https://goodworldnow.com/))
   - Confidence: Medium. Pivots are positioning changes, and their causes are mostly unstated.

**Implication for the repository's entrant strategy:** the evidence supports the [entrant simulation](ai-native-entrant-simulation.md)'s *partner-the-sponsor, never-hold-funds* posture and its preference for B2B distribution. It adds three tests that the simulation does not yet price:
- consolidator-acquisition as the likely exit;
- the legal title of in-flight donations;
- sponsor-governance due diligence on any partner sponsor.

See §7.

---

## 2. Scope, definitions and data dictionary summary

**Scope.** The study covers:
- DAF sponsors and DAF technology;
- payments and fundraising intermediaries that hold or route charitable money;
- consumer giving apps;
- corporate and workplace giving platforms;
- a small set of cause-branded consumer fintechs, used as economic comparators (Swell, Aspiration).

It excludes Givelify and Catchafire as out of scope (not DAF and not money-custodial in the relevant sense). It does not research them.

**Outcome groups** (column `outcome_group`):
| Group | Count | Meaning |
|---|---|---|
| regulatory_or_insolvency | 6 | Regulator order, court liquidation, bankruptcy, or board-ordered cessation with a trustee |
| voluntary_shutdown | 11 | Service or product closed by its owner without insolvency |
| acquisition | 12 | Company or product bought (includes merge-and-discontinue and acquire-then-retreat) |
| pivot_or_retreat | 5 | Still operating but repositioned, with layoffs or a status unknown after a pivot |
| survivor_control | 1 | Endaoment, a crypto-DAF survivor kept as a control |
| investigated_no_adverse_outcome_or_unidentified | 15 | Candidate checked; no adverse event found, or the entity could not be identified |

Full column definitions are in §10.

---

## 3. Case files: core DAF sponsors and DAF technology

### FD01: SDG Impact Fund (DAF sponsor). Regulatory shutdown order, then a receivership suit. *New.*

- **System context.**
  - SDG Impact Fund presented itself as a DAF network. It reportedly grew from a $117,000 charity in 2017 to a "$10 billion collection of 146 DAFs" about four years later ([Chronicle of Philanthropy, 2026-07-31](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/)).
  - It was first profiled as "the $10 billion charity no one has heard of" ([AP via News4Jax, 2023-12-15](https://www.news4jax.com/business/2023/12/15/the-10-billion-charity-no-one-has-heard-of/)).
- **Outcome (factual).**
  - In June 2026 the Georgia Secretary of State issued an emergency cease-and-desist order. The order:
    - barred the fund from operating as a charity in Georgia;
    - barred CEO Anthony Suber from charitable solicitation;
    - imposed a $100,000 penalty.
  - No hearing was requested, so the order became final ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)).
  - In September 2026 the Georgia AG sued in Fulton County, seeking a receiver and possibly the return of money to donors ([WSB-TV, 2026-09-25](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)).
- **Manifestations.**
  - The last public IRS filing (FY2022) reported more than $10B in assets. The fund paid out $8.5M that year, about 0.1% of assets ([Chronicle, 2026-07-31](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/)).
  - Donors complained in 2025 that their grant recommendations went unanswered ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)).
  - The AG complaint says 0.185% of claimed assets went to charity ([WSB-TV, 2026-09-25](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/)).
- **Stated reasons and the fund's position.** Suber wrote that the fund could collect 5% of AUM and that fees on $10B "exceeded $450 Million" ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)).
- **Origin network.**
  - *Financial:*
    - E: alleged commingling, and use of donor funds for tuition, real estate and travel (regulator findings, same source).
    - I: a self-valued illiquid asset base was used to justify fees on AUM.
  - *Distribution:* E: the fund kept soliciting through summer 2025 after telling some donors it was dissolving ([Chronicle](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/)).
  - *Regulatory:*
    - E: a state order and an AG suit.
    - E: a similarly named Wyoming entity received IRS exemption in February 2026, and its incorporation papers name no officers (same source).
    - I: weak coordination between states.
  - *Technical:* unknown.
  - *Organizational:* E: in the regulator's account, the CEO controlled both the fund's accounts and his personal accounts. No evidence of independent board control was found.
- **Assets and data.** The receiver request is pending. Final disposition is unknown.
- **Control points.** State registration and solicitation regulators, IRS Form 990 review, and the donors' own diligence on sponsor custody.
- **Diagnostic sufficiency.** The evidence is sufficient to say the *control failure was in sponsor governance and custody*. It is not sufficient to quantify losses. The allegations are not adjudicated.
- **Lesson for entrants.** A DAF technology vendor or partner inherits reputational exposure from its sponsor-of-record. Sponsor custody and governance attestation should be a precondition of partnering. A sponsor's self-reported asset values, especially for crypto or art, are not evidence.

### FD02: National Heritage Foundation. *Reference row* (prior repo EV02, EV04, EV05, EV09).

The case is unchanged from the [lifecycle ledger](../historical-daf-sponsor-technology-lifecycle-2011-2026.md):
- a 2009 Chapter 11 ([4th Cir., 2011-12-09](https://law.justia.com/cases/federal/appellate-courts/ca4/10-2015/102015.p-2011-12-09.html));
- a 2011 IRS revocation ([IRB 2011-47](https://www.irs.gov/irb/2011-47_IRB));
- zero assets in FY2022 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/582085326)).

### FD03: Pinkaloo. White-label giving accounts, acquired by RenPSG.

- **Founding and funding.** Pinkaloo is Baltimore-based. It reported $1.25M in 2019, led by Squadra, for a total of $1.8M including a $550k seed ([Technical.ly, 2019-12-05](https://technical.ly/baltimore/2019/12/05/pinkaloo-startup-raises-million-squadra-vc-guy-filippelli-mike-leffer/); [Finovate](https://finovate.com/pinkaloo-raises-1-25-million/)).
- **Distribution.** Its distribution included a MassChallenge-linked pilot with Eastern Bank ([Technical.ly, 2019-07-19](https://technical.ly/baltimore/2019/07/19/masschallenge-fintech-accelerator-pinkaloo-launches-charitable-giving-pilot-eastern-bank)).
- **Outcome.** Acquired on 2021-03-09 ([Pinkaloo blog](https://www.pinkaloo.com/blog/renpsg-acquires-pinkaloo)).
- **Not established.** No stated distress, and no product fate after the acquisition. The brand site was still live in 2026 (prior repo).
- **EDF.** Not applied; this is not an adverse outcome.

### FD04: Amicus.io ("DAF 2.0"). Acquired by TIFIN, now inside TIFIN Give. *New.*

- **Founding and funding.**
  - Founded in 2017 and based in Charlotte.
  - It raised an $8.7M Series B in November 2020 to embed DAFs in consumer banking apps ([Crunchbase News](https://news.crunchbase.com/news/making-philanthropy-as-easy-as-banking-amicus-io-raises-8-7m-series-b)).
  - Reported cumulative totals conflict: $17.5M per [Hypepotamus](https://www.hypepotamus.com/amicus-donor-advised-funds/), and lower figures in aggregators. The total is recorded as unresolved.
- **Outcome.** TIFIN acquired Amicus.io in March 2022 ([InvestmentNews](https://www.investmentnews.com/fintech/tifin-group-acquires-fintech-targeting-donor-advised-funds/218849); [TIFIN release](https://tifin.com/news/tifin-announces-the-expansion-of-its-fintech-platform-for-personalized-charitable-giving-to-democratize-access-to-donor-advised-funds/4961/)).
- **Later product history.** A 2024 trade article describes TIFIN Give as built on the platform previously known as Louise, "powered by the acquisitions of Amicus.io and Giving Place" ([WealthManagement.com](https://www.wealthmanagement.com/philanthropy/assetmark-announces-strategic-collaboration-with-tifin-give)).
- **Reading.**
  - The consumer-bank distribution thesis did not survive as an independent business. Its code was absorbed into an advisor- and enterprise-distribution strategy.
  - TIFIN later divested Giving Place in order to focus on DAFs (FD06).
  - This is not evidence of failure. It is evidence that **buyers valued the infrastructure over the consumer channel**.
  - Confidence: Medium.

### FD05–FD08: Vennfi, Giving Place, Stellar/iPhi, Crown/DonorFirst. *Reference rows.*

These are documented in the prior repo (X05, X06, EV06, EV10, EV12, EV14). One addition here:
- Charityvest's 2020 raise was reported at $3.7M ([Newswire, 2020-11-19](https://www.newswire.com/news/this-startup-raised-3-7m-to-let-anyone-donate-stocks-and-etfs-with-a-21260863)).
- The split of that raise between the for-profit Vennfi and the charity is not stated.

### FD09: Network for Good. Software merged into Bonterra; the DAF nonprofit continued. *New detail.*

- **The split.**
  - In January 2022 "Network for Good .COM", the donation software, joined Bonterra in a merger with CyberGrants, EveryAction and Social Solutions ([For Good site](https://www.forgood.org/landing-pages/our-donation-software-is-now-part-of-bonterra)).
  - The DAF nonprofit continued and was renamed **For Good** in May 2025 ([Business Wire, 2025-05-29](https://www.businesswire.com/news/home/20250529977479/en/Donor-Advised-Fund-Network-for-Good-Unveils-New-Name-For-Good)).
- **Related-party payment (unverified).**
  - An advocacy-oriented profile reports that the DAF paid Bonterra $4,765,096 in 2023 for "professional fundraising" services ([InfluenceWatch](https://www.influencewatch.org/non-profit/network-for-good/)).
  - **This has not been verified against the 990.**
- **Reading.**
  - This is the cleanest example of the *sponsor/vendor split* the prior repo recommends: charitable assets stayed with the charity, and the software was sold.
  - It also shows a continuing commercial dependency between the charity and its former affiliate. That dependency should be a diligence item.

### FD10: Philanthropi. A DAF-powered "giving-as-a-service" company that pivoted from employers to banks; current status unknown. *New.*

- **Founding and funding.**
  - Founded in 2018. It had raised about $8.5M by July 2022.
  - Its model: payroll-funded DAFs, plus APIs for financial-services partners. Named clients included Live Oak Bank and Bryn Mawr Trust.
  - Revenue came from gateway fees averaging about 3% charged to charities, plus setup and recurring fees ([Payments Dive, 2022-07-08](https://www.paymentsdive.com/news/fintech-philanthropi-taps-into-giving-surge-payments/626794/)).
  - It reported a $4M round led by Amex Ventures ([PR Newswire](https://prnewswire.com/news-releases/philanthropi-raises-4m-in-funding-to-power-the-charitable-giving-legacies-of-everyday-philanthropists-301445028.html)).
- **Status.**
  - No post-2022 primary evidence was found.
  - The Wayback availability API reports a capture of philanthropi.com on 2026-08-07. Its content could not be read from this environment, and the live site did not resolve.
  - **Status unknown.** It is not classified as failed.

### FD11: Bright Funds. Consumer charity "mutual funds", then workplace giving, then merged and resold. *New.*

- **Origin.** Bright Funds launched in November 2012 as "mutual funds for nonprofits" ([TechCrunch, 2012-11-26](https://techcrunch.com/2012/11/26/mutual-funds-for-non-profits-bright-funds-wants-to-be-the-vanguard-for-charitable-giving)).
- **Repositioning.** It later sold workplace giving and merged with WizeHive in November 2021 ([Business Wire, 2021-11-17](https://www.businesswire.com/news/home/20211117005215/en/WizeHive-Combines-Forces-with-Bright-Funds-to-Create-Comprehensive-Corporate-Giving-Solution)).
- **Resale.** WizeHive was acquired by Submittable in August 2024 ([LLR Partners, 2024-08-08](https://www.llrpartners.com/submittable-acquires-wizehive-cementing-its-leadership-in-social-impact-tech/)).
- **Funding and fees.**
  - Funding is listed as $2.1M by one aggregator ([CB Insights](https://www.cbinsights.com/company/bright-funds/financials)). This is unverified.
  - The Chronicle reported a take rate of about 7.5%, mostly paid by corporate clients ([Chronicle](https://www.philanthropy.com/news/mutual-funds-for-nonprofits-help-donors-diversify-giving/)).
- **Reading.** The consumer model gave way to an employer-paid B2B model. This matches the Philanthropi, Groundswell and Pinkaloo channel pattern.

### FD12: Groundswell. *Reference.*

- It began in 2021 as a DAF-as-employee-benefit with a $15M seed ([Business Wire, 2021-11-30](https://www.businesswire.com/news/home/20211130005365/en/Groundswell-Announces-A-Total-of-15M-in-Seed-Funding-To-Democratize-Philanthropy)).
- By 2026 it sold a full CSR suite ([Groundswell](https://www.groundswell.io/products/donor-advised-fund)).
- No layoffs or distress were found. It is classified as *repositioned*.

---

## 4. Case files: crypto exposure

### FD13: The Giving Block. Acquired by Shift4, then the earnout collapsed and staff were cut. *New primary evidence.*

- **Acquisition.**
  - The acquisition date was 2022-02-28.
  - Terms: $54M upfront plus up to $246M of earnout tied to revenue from March 2022 to February 2023 ([Payments Dive](https://www.paymentsdive.com/news/shift4-to-buy-2-companies-for-579m/619624/)).
  - Total purchase consideration net of cash was $106.9M ([Shift4 FY2022 10-K, SEC](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/Financial_Report.xlsx)).
- **Outcome (factual).**
  - Shift4 recognized a **$(47.1)M** fair-value adjustment to The Giving Block contingent liability for FY2022. The earnout liability stood at $10.9M at 2022-12-31.
  - The FY2023 report states that the cash portion was paid in 2023 ([Shift4 FY2023 10-K, SEC](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/Financial_Report.xlsx)).
  - Separately, about 12% of staff were laid off in three rounds after FTX collapsed. The company cited internal reorganization ([The Block, 2023-01](https://www.theblock.co/post/203351/the-giving-block-cuts-about-12-of-its-workforce)).
- **Origin network.**
  - *Financial:* E: the filing attributes the reduction to lower projected revenue. I: crypto price and volume collapse in 2022.
  - *Organizational:* E: layoffs.
  - *Technical:* E: Shift4 records crypto settlement assets held on behalf of platform users.
  - *Regulatory* and *distribution:* unknown.
- **Diagnostic sufficiency.** The evidence is sufficient to conclude that **crypto-denominated philanthropy revenue fell sharply within one year**. It does not establish platform failure; the business continues.
- **Lesson.** Crypto is an acquisition channel for high-value donors. It is not a stable revenue base for a startup.

### FD14: FTX Foundation / Future Fund. Shut down. *Adjacent; not a DAF.*

- The Future Fund said it could no longer "perform its work or process grants" after FTX collapsed, and its team resigned ([Decrypt, 2022-11](https://decrypt.co/114197/ftx-foundation-shutters-effective-altruism-fund-key-execs-resign)).
- Commentators flagged the risk to charities that hold crypto ([Fortune, 2022-11-14](https://fortune.com/2022/11/14/ftx-bankruptcy-puts-charitable-donations-in-doubt-and-some-blame-sam-bankman-frieds-effective-altruism-mindset-for-troubles/)).
- It is included to illustrate single-funder and single-asset dependency.

### FD15: Endaoment. Survivor control.

- It raised $2.5M in 2021, led by Framework Ventures ([Decrypt](https://decrypt.co/72524/on-chain-charity-endaoment-lands-2-5m-investment-led-framework-ventures)), and $6.67M in 2022 ([Endaoment blog](https://blog.endaoment.org/blog/announcing-endaoments-6-67m-capital)).
- In October 2026 Altruist launched Endaoment-sponsored DAFs for advisors ([InvestmentNews, 2026-10-06](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481)).
- A crypto-native sponsor survived 2022 by becoming a sponsor-of-record for partners. This is the posture the entrant simulation proposes to partner with.

**No crypto-native DAF sponsor closure after 2022 was found.** The closest case is SDG Impact Fund, whose reported assets were largely illiquid, digital assets and collectibles valued at fair market value ([WSB-TV, 2026-07-20](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/)).

---

## 5. Case files: payments intermediaries, donor apps, corporate products

### FD16: Flipcause. Extends prior X01 with the NPQ timeline.

- **Timeline** ([NPQ, 2026-03-13](https://nonprofitquarterly.org/nonprofits-in-limbo-as-flipcause-bankruptcy-unfolds/)):
  - complaints about slow, small payouts from 2024;
  - a class action in October 2025;
  - a California AG order in November 2025 ([CA AG](https://oag.ca.gov/news/press-releases/attorney-general-bonta-warns-fundraising-platform-flipcause-immediately-stop-its));
  - in December 2025, **Stripe froze a $1.45M reserve**;
  - Chapter 11 filed on 2025-12-19;
  - a single $400k bid for the software in March 2026;
  - conversion to Chapter 7 on 2026-04-28 ([Whiteford, 2026-05-07](https://www.whitefordlaw.com/news-events/client-alert-fundraising-platform-failures-and-increasing-government-scrutiny-highlight-need-for-)).
- **Financial position, from filings as reported by NPQ:**
  - more than $29M owed to more than 3,200 organizations;
  - $70k in cash;
  - more than $3.8M transferred to insiders and related parties.
- **Legal position.** The founder testified that the donations belonged to Flipcause, not to the nonprofits (same source).
- **New lesson.** The legal *title* to in-flight donations decides recovery. Nonprofits ended up as unsecured creditors.

### FD17: Ammado. Court-ordered liquidation, 2018. *New.*

- **Background.** Founded in 2005. It had raised €15.7M cumulatively by February 2012, including a €7M round ([TechCrunch, 2012-02-20](https://techcrunch.com/2012/02/20/ammado-raises-9m-to-solve-global-giving-problem/)).
- **Liquidation.** It was wound up by the Irish High Court on a petition from the Revenue Commissioners over about €400k of tax debt. About **€3.8M of donations was reported unaccounted for** ([UK Fundraising, 2018-02-01](https://fundraising.co.uk/2018/02/01/ammado-liquidation-e3-8bn-donations-unaccounted-for/)).
- **Early warning.** In April 2017 the IFRC had advised national Red Cross societies to suspend use of the platform over business conduct (same source).
- **Origin network.**
  - *Financial:* E: tax debt and missing donations.
  - *Organizational:* E: a conduct concern raised by a major user network a year earlier.
  - *Regulatory:* E: the court liquidation.
  - *Technical:* unknown.

### FD18: Giving Assistant. Board-ordered cessation and orderly payout. *New.*

- **Cessation.** The company stopped operating in November 2021 by board order, and all staff were released.
- **Payout.** Assets went to a San Francisco firm (Ueker and Associates) for liquidation. Claims were due by May 2022 and checks went out in August 2022.
- **Charities.** The trustee "settled all accounts with outstanding balances or undelivered funds" with charities.
- **Data and domain.** Personal data was destroyed, and the domain was sold to Upright Data ([Giving Assistant FAQ](https://givingassistant.org/insights/news/giving-assistant-frequently-asked-questions); [Doctor of Credit](https://www.doctorofcredit.com/giving-assistant-shopping-portal-shutting-down/)).
- **Cause.** Not stated.
- **Contrast with Ammado and Flipcause.** This orderly wind-down paid users and charities.

### FD22: ioby. Nonprofit crowdfunding and fiscal sponsor, closed in 2024. *New.*

- ioby said it "could not build a sustainable financial future".
- It moved about $1.4M in its final year and more than $21M over its history ([ioby closing notice](https://ioby.org/resources/closing/); [Chronicle op-ed](https://www.philanthropy.com/opinion/why-the-quiet-collapse-of-a-crowdfunding-platform-should-alarm-philanthropy/)).
- I: low-take, mission-priced intermediation that depended on subsidy.

### FD23–FD27: Corporate-owned giving products. *New.*

| Case | Closed | Stated reason | Source |
|---|---|---|---|
| GoFundMe Charity | 2021-09-30 | Unite charity and personal fundraising; API ended 2021-03-31; campaigns not migrated | [NPT, 2021-02-10](https://thenonprofittimes.com/technology/gofundme-charity-being-shut-down/) |
| Virgin Money Giving | 2021-11-30 | Heavy investment needed to stay competitive; London Marathon sponsorship ending; up to 26 roles | [UK Fundraising](https://fundraising.co.uk/2021/08/26/virgin-money-giving-to-close-in-november/); [Civil Society](https://www.civilsociety.co.uk/news/virgin-money-giving-will-close-this-year-as-london-marathon-partnership-ends.html) |
| BT MyDonate | 2019-06-30 | Many alternatives, including fee-free platforms | [UK Fundraising, 2019-01-21](https://fundraising.co.uk/2019/01/21/bt-mydonate-close-june/) |
| Google One Today | 2020-02-06 | "Donors choose other products" | [9to5Google](https://9to5google.com/2020/01/29/google-one-today-donation-killed/); [PYMNTS](https://www.pymnts.com/news/2020/google-to-shut-down-nonprofit-donation-app/) |
| AmazonSmile | 2023-02-20 | "Has not grown to create the impact that we had originally hoped"; three months' payment to charities | [GBH/AP](https://www.wgbh.org/news/national/2023-01-19/amazon-ends-its-charity-donation-program-following-other-cost-cutting-efforts); [Fortune](https://www.fortune.com/2023/01/19/amazon-smile-charity-ends-layoffs-tech-not-grown-impact/) |

### FD28–FD30, FD33–FD35: Acquisitions and retreats in corporate and fundraising software

- **Causecast.** America's Charities bought the platform in July 2019. It had used the platform since 2015 and wanted control of the product ([America's Charities](https://www.charities.org/news/americas-charities-acquires-causecast-giving-platform-further-strengthening-its-support-social/)).
- **Kindful.** Acquired by Bloomerang on 2021-01-07 ([Business Wire](https://www.businesswire.com/news/home/20210107005891/en/Bloomerang-Acquires-Kindful-to-Accelerate-Vision-of-Helping-Nonprofits-Fund-Their-Missions)). It is now listed as discontinued, with its features moved into Bloomerang ([TrustRadius](https://www.trustradius.com/compare-products/bloomerang-vs-kindful)).
- **GoodWorld.**
  - It began as hashtag giving on social media, keeping 7% of each donation ([Inside Philanthropy, 2017-03-01](https://insidephilanthropy.com/home/2017/3/1/this-startup-wants-to-make-donate-the-future-of-online-fundraising)).
  - It launched in Australia in 2020 ([FinTech Futures](https://www.fintechfutures.com/fintech/charity-donation-fintech-goodworld-launches-in-australia)).
  - In 2026 it markets workplace giving and CSR software ([GoodWorld](https://goodworldnow.com/)).
  - It is classified as a pivot. The date of the pivot is unknown.
- **Benevity.** In January 2023 it laid off 137 staff (14%), citing demand below expectations and saying it was "overbuilt" ([BetaKit](https://betakit.com/?p=352010); [CTV](https://calgary.ctvnews.ca/calgary-tech-firm-benevity-lays-off-137-workers-cites-poor-market-conditions-1.6237343)). The Alaya sunset is planned for 2026-12-15 (prior X04).
- **YourCause.** Acquired by Blackbaud in 2019 ([Business Wire](https://www.businesswire.com/news/home/20190102005635/en/Leading-Corporate-Social-Responsibility-Provider-YourCause-Acquired/)).
- **JustGiving.** Blackbaud completed the acquisition on 2017-10-03 ([Civil Society](https://www.civilsociety.co.uk/news/blackbaud-confirms-completion-of-justgiving-acquisition.html)).

### FD31–FD32: Cause-branded consumer fintech comparators

- **Swell Investing.**
  - An impact robo-adviser backed by Pacific Life, which reportedly committed about $30M ([Built In](https://builtin.com/articles/swell-announces-funding-expansion)).
  - It closed on 2019-08-30. Swell said it was "unable to achieve the necessary scale", and Pacific Life called it "not a long-term fit" ([InvestmentNews](https://www.investmentnews.com/fintech/pacific-life-shutters-esg-robo-adviser-swell-investing/80592); [Doctor of Credit](https://www.doctorofcredit.com/swell-investing-to-shut-down-on-august-30th-2019/)).
  - Its scale was reported at about $35M AUM and about 15,000 clients. This is the closest public analogue to small-balance consumer "giving account" economics.
- **Aspiration Partners.**
  - The climate-branded neobank filed for Chapter 11 on 2025-03-30.
  - Its co-founder agreed to plead guilty to wire fraud, and the DOJ said revenue was falsely inflated ([American Banker](https://www.americanbanker.com/news/aspiration-a-tree-planting-neobank-felled-by-investor-fraud); [Banking Dive](https://www.bankingdive.com/news/aspiration-co-founder-wire-fraud-plead-guilty/758787/)).
  - Mission branding did not protect against governance failure.

### FD36–FD50: Investigated, with no adverse outcome found or the entity not identified

None of the following was found to have shut down or retreated:
- **Givz** ($3M seed in 2021; a Shopify donation-marketing app) ([TechCrunch tag](https://techcrunch.com/tag/givz/)).
- **Charity Navigator Giving Basket** (powered by Give Lively, which charges a 2.5% platform fee) ([Give Lively](https://www.givelively.org/faqs/what-is-charity-navigators-giving-basket)).
- **Betterment Charitable Giving** (disclosure updated 2025-12-23) ([Betterment](https://www.betterment.com/legal/charitable-giving)).
- **Charitable Impact (CHIMP)** ([CanadaHelps](https://www.canadahelps.org/en/charities/id/97116/)).
- **Grapevine** ($1.85M seed in 2023) ([Business Wire](https://www.businesswire.com/news/home/20230808466348/en/Grapevine-Closes-1.85M-Total-Seed-Round-Delivers-25-Million-To-Nonprofits-To-Democratize-Philanthropic-Giving)).
- **Brightest** ([Brightest](https://www.brightest.io/donation-fundraising)).
- **Benevolent** ([Knight Foundation](https://knightfoundation.org/articles/crowd-funding-site-benevolent-expands-charlotte-silicon-valley)).
- **CommitChange** ([about](https://commitchange.com/about)).
- **Givinga** (aggregators disagree on its funding total) ([CB Insights](https://www.cbinsights.com/investor/givinga)).
- **ImpactAssets** (lowered fees and minimums in 2018) ([FA Mag](https://www.fa-mag.com/news/impactassets-lowers-fees-and-minimums-37664.html)).
- **Fidelity Charitable Giving Account** (no discontinued feature found; the minimum was removed in 2020) ([ThinkAdvisor, 2020-09-30](https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/)).
- **Engiven** ([Engiven, 2023-05-16](https://engiven.com/blog/engiven-brings-crypto-giving-to-pushpay)).

Three names could not be resolved:
- **"Humanitas"** and **"Raise Foundation"** could not be identified as DAF entities.
- **JustGive.org**'s status was not established ([Idealist](https://www.idealist.org/en/nonprofit/3c429efe4ade46f4934deb8703e40c3a-justgiveorg-san-francisco)). It is distinct from JustGiving.

Wealthfront, Robinhood and Altruist charitable features, and "Daffy competitors that closed": no closure evidence was found in the searches run. Altruist *added* DAFs in 2026 (FD15 source).

---

## 6. Cross-case pattern analysis

The patterns are stated with confidence labels. Each lists the cases that support it and the evidence that would overturn it.

### P1. Payments and custody are where charitable money is lost. *Confidence: High (observed), Medium (generalization).*

- **Supporting cases.** All three cases with reported missing or unremitted charitable money had one operator controlling unsegregated donor funds:
  - Ammado (€3.8M);
  - Flipcause (more than $29M owed);
  - SDG Impact Fund (alleged).
- **Contrast cases.** Vennfi, Network for Good and Giving Assistant changed hands or shut down without reported charity losses:
  - In Vennfi and Network for Good, the charity was a separate legal entity.
  - In Giving Assistant, the liquidation was orderly.
- **Mechanism (E).** In Flipcause, the operator claimed title to the donations, and a processor reserve was frozen ([NPQ](https://nonprofitquarterly.org/nonprofits-in-limbo-as-flipcause-bankruptcy-unfolds/)).
- **Would reconsider if** a case appears where a properly segregated sponsor-of-record structure still lost donor funds because a vendor failed.

### P2. Acquisition by an incumbent or consolidator is the modal DAF-tech exit, and buyers pay for plumbing. *Confidence: Medium-High.*

- **Supporting cases.**
  - Ren bought Crown, Pinkaloo and iPhi.
  - Foundation Source bought Vennfi and Giving Place.
  - TIFIN bought Amicus.io and Giving Place, then sold Giving Place.
  - Blackbaud bought YourCause and JustGiving.
  - Bloomerang bought Kindful.
  - Submittable bought WizeHive, which included Bright Funds.
- **Disclosure gap.** No acquirer published codebase or customer-migration outcomes.
- **Inference (I).** Exit values are probably modest. Amicus's terms were undisclosed, and Pinkaloo had raised only about $1.8M.
- **Would reconsider if** an independent DAF-tech vendor reaches scale and files or discloses a sustained standalone business, or if acquisition prices are disclosed and are large.

### P3. Distribution dependence: a borrowed channel can be withdrawn. *Confidence: Medium.*

- **Corporate owners withdrew their giving products:**
  - Virgin Money Giving closed when the marathon sponsorship ended (stated);
  - Google, Amazon and BT closed products for reasons of adoption or strategy;
  - GoFundMe folded its charity product into the parent.
- **Startups kept switching channels.** They moved repeatedly from consumer to employer to bank or advisor: Pinkaloo, Amicus, Philanthropi, Bright Funds and Groundswell.
- **Inference (I).** Direct consumer acquisition of DAF donors has not been shown to be viable for small startups in this sample. Daffy, the visible counterexample, reports $2B in assets, but its figures are unaudited (prior repo).
- **Would reconsider if** a consumer-direct DAF startup's CAC and retention data become public and show payback.

### P4. Flat-fee or low-take pricing versus customer acquisition cost. *Confidence: Low-Medium (mostly inference).*

- **Evidence (E).**
  - Swell failed on scale with about $35M AUM despite about $30M of parent capital.
  - ioby could not sustain itself on more than $21M of lifetime volume.
  - TakeCharge.io closed after processing $1.13M (prior HL22).
  - BT MyDonate and Virgin Money Giving were at-cost or commission-free.
- **Inference (I).** Small balances and low take rates do not fund acquisition costs. No case discloses actual CAC, so this pattern is labelled *suggestive*.
- **Would reconsider if** unit-economics disclosures from flat-fee DAF platforms (Daffy, Charityvest) show positive contribution margin at small balances.

### P5. Regulatory and charitable-solicitation exposure is real and growing for intermediaries. *Confidence: Medium-High.*

- **Enforcement cases:**
  - California AG against Flipcause;
  - other state AG suits;
  - Georgia Secretary of State and AG against SDG Impact Fund;
  - Ireland's Revenue Commissioners against Ammado.
- **Commentary.** The Whiteford alert frames this as "increasing government scrutiny" of fundraising platforms ([Whiteford](https://www.whitefordlaw.com/news-events/client-alert-fundraising-platform-failures-and-increasing-government-scrutiny-highlight-need-for-)).
- **Counterpoint.** SDG's apparent re-emergence in Wyoming shows that enforcement is fragmented ([Chronicle](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/)).

### P6. Crypto exposure is cyclical. *Confidence: High (facts), Medium (generalization).*

- The Giving Block's earnout was revalued down by $47.1M within a year.
- The Giving Block cut staff.
- The FTX Future Fund collapsed.
- SDG Impact Fund's illiquid asset claims drew scrutiny.
- Endaoment survived by moving to partner distribution.

### P7. Governance failure in mission-branded entities. *Confidence: Medium.*

- SDG Impact Fund, Aspiration and Flipcause each involve alleged insider misconduct, which is not adjudicated in every case.
- Ammado had a conduct warning from a major user network a year before it was liquidated.
- Mission branding did not lead to closer investor or donor scrutiny in these cases. This is stated cautiously, because it rests on three or four cases.

### Not supported by evidence

The following were checked and lack evidence in this sample:
- that **technology or code quality** caused any of the closures;
- that **AI** was a factor;
- that the **IRS DAF regulations** (proposed §4966 rules) caused any exit.

Do not cite this file for those claims.

---

## 7. Implications for the entrant strategy ([ai-native-entrant-simulation.md](ai-native-entrant-simulation.md))

1. **The "never hold funds" rule (R12) is the most strongly evidenced design choice.**
   - Every case of lost charitable money involved an operator holding donor funds (P1).
   - The rule should be extended. An entrant should also *contractually disclaim title* to in-flight donations, and should verify the processor-reserve terms of any payments partner (Flipcause and Stripe).
2. **Due diligence on the partner sponsor is a first-order risk, not paperwork.**
   - S1 (white-label through a sponsor partner) inherits the partner's governance.
   - Before signing, an entrant should require:
     - audited financials;
     - custody attestations;
     - a payout-ratio history;
     - state registration status.
   - SDG Impact Fund is the counterexample.
3. **Plan for consolidator acquisition as the base-case exit.**
   - Six of six documented DAF-tech exits went to Ren, Foundation Source or TIFIN (P2).
   - An entrant's architecture and contracts should be *acquirable*: clean data export, sponsor-owned records, assignable contracts.
   - Equally, the entrant should expect the consolidators to be both its competitors and its likely buyers.
4. **Do not rely on one distribution partner, and do not count on consumer-direct CAC.**
   - Corporate partners shut giving products for strategic reasons (P3).
   - Five startups in this sample moved from consumer to institutional channels.
   - This supports the simulation's B2B-first sequencing.
   - It also warns against tying any single bank or employer partner to the company's survival.
5. **Treat crypto as an optional intake feature, not a revenue base** (P6).
6. **Compete on resilience as a feature.**
   - The cases show what buyers lose in a failure: data deletion deadlines (Everfund, Kambeo, GoFundMe Charity), unmigrated campaigns, and frozen reserves.
   - A documented exit plan is a differentiator an entrant can sell. It should cover sponsor-owned export, escrowed code, and an attested segregation structure.
7. **Reconsideration criteria for these implications:**
   - a documented failure of a sponsor-of-record partner model in which the vendor did *not* hold funds, which would weaken item 1;
   - a disclosed independent DAF-tech vendor reaching profitable scale, which would weaken item 3;
   - public CAC and retention data for consumer DAFs showing payback, which would weaken item 4.

---

## 8. Survivorship-bias and coverage caveats

- **Visibility bias.** Failures that make the news involve money losses (Flipcause, Ammado), regulators (SDG Impact Fund), or large brands (Amazon, Google). Quiet closures of small DAF apps may leave no press trace. They may show up only as lapsed state registrations, abandoned app-store listings, or a sponsor terminating a partner, and none of these were searched systematically (queue P-FAIL-04).
- **Acquisition-press bias.** Acquirers publish deals but not product deaths. The fate of Pinkaloo, Amicus, iPhi and DonorFirst is unknown, and some "acquisitions" may in practice be acqui-hires or asset purchases for parts.
- **Denominator absent.** Fifteen investigated names showed no adverse outcome. That is *not* a survival rate: the candidate list was not a random sample.
- **Self-reported causes.** Several stated reasons are company statements and are not audited. Examples: Kambeo's "insufficient growth" and Amazon's "not grown to create the impact". Under Clarity, these are claims, not diagnoses.
- **Unadjudicated allegations.** The SDG Impact Fund, Flipcause and Aspiration facts are regulator findings, complaints or trade-press reports of filings.
- **Tooling limits.** web.archive.org content could not be fetched from this environment; only the availability API worked. Crunchbase and PitchBook were not accessed. Funding figures therefore come from press releases or aggregators and are labelled as such.
- **Geography.** The UK and Irish cases (Ammado, Virgin Money Giving, BT MyDonate) operate under different charity law. They are used as mechanism analogues only.

---

## 9. Open questions

The prioritized versions are in the [queue CSV](../../data/mission-2026-11-14/queue-proposals-failed-startups.csv).
1. What is the mortality base rate for DAF sponsors? This needs an EIN-year panel from 990 Schedule D (P-FAIL-01).
2. What is the custody, the asset reality and the receivership outcome for SDG Impact Fund (P-FAIL-02)?
3. What happened to the acquired DAF codebases and their customers (P-FAIL-03)?
4. Have consumer DAF apps closed quietly (P-FAIL-04)?
5. What were Flipcause's creditor recoveries, and was the question of title to donations resolved (P-FAIL-05)?
6. What is the post-2022 status of Philanthropi, Grapevine, Givinga and Groundswell (P-FAIL-06)?
7. How exposed are crypto DAFs and processors to drawdowns (P-FAIL-07)?
8. How do state solicitation and co-venturer rules apply to DAF vendors (P-FAIL-08)?
9. What do the closures of corporate giving products imply for distribution partnerships (P-FAIL-09)?
10. Can first-party founder post-mortems be collected to replace inferred causes (P-FAIL-10)?

---

## 10. Data dictionary: `data/mission-2026-11-14/failed-daf-startups.csv`

| Column | Definition |
|---|---|
| case_id | FD01–FD50 |
| name | Entity or product |
| category | Free-text business description |
| daf_proximity | One of: core_daf_sponsor, daf_tech, crypto, crypto_daf, payments_intermediary, payments_and_daf_sponsor, donor_app, corporate_giving, adjacent_philanthropy_software, adjacent_software, adjacent_cause_marketing, adjacent_fintech, adjacent_crypto_philanthropy, unknown |
| founding_year | As sourced; "unverified" or "unknown" where not sourced |
| funding_raised | Sourced amount with qualifier; "unknown" if none found; "n/a" for charities and corporate products |
| funding_source_url | URL backing funding_raised |
| outcome_class | Specific outcome label (for example court_ordered_liquidation, acquisition_by_incumbent, pivot) |
| outcome_group | Normalized group (see §2) used for counts |
| outcome_date | ISO date or month of the outcome event(s) |
| evidence_urls | Semicolon-separated sources for the outcome |
| evidence_dates | Dates of those sources, in the same order |
| stated_reasons | Reasons given by the company, regulator or acquirer, attributed |
| origin_financial / origin_distribution / origin_regulatory / origin_technical / origin_organizational | EDF origin network. "E:" means stated in a source and "I:" means analyst inference. Shown as "n/a (no adverse outcome observed; EDF not applied)" for non-adverse outcomes, and "unknown" where no evidence exists |
| donor_assets_and_data_disposition | What happened to charitable money, user balances and data |
| lessons_for_entrants | Analyst lesson (inference) |
| confidence | Clarity qualitative label |
| prior_repo_ids | IDs in earlier repository datasets (X, EV, HL, TA) |
| notes | Caveats |

## 11. Data dictionary: `data/mission-2026-11-14/queue-proposals-failed-startups.csv`

Columns follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md):
- importance, gap, commercial, availability and effort are scored 1–5;
- p_change is scored 0–1;
- state is `open`.

---

## 12. Source register (new sources used in this file; prior-repo sources are cited by ID)

| # | Source | Date | Used for |
|---|---|---|---|
| S01 | [Chronicle: $10B crypto DAF barred in Georgia](https://www.philanthropy.com/news/mysterious-10-billion-crypto-daf-barred-in-georgia-appears-to-re-emerge-in-wyoming/) | 2026-07-31 | FD01 |
| S02 | [WSB-TV: Georgia charity barred](https://www.wsbtv.com/news/local/georgia-charity-claiming-10b-assets-barred-after-donor-fund-misuse-allegations/5VZD65H5QNC3XLIGGPQWH6I6LM/) | 2026-07-20 | FD01 |
| S03 | [WSB-TV: AG sues charity](https://www.wsbtv.com/news/local/atlanta/where-did-money-go-ag-sues-charity-spotlighted-by-channel-2/76726H6FXFCW5JQXC2N2VOTEQQ/) | 2026-09-25 | FD01 |
| S04 | [AP/News4Jax: $10B charity no one has heard of](https://www.news4jax.com/business/2023/12/15/the-10-billion-charity-no-one-has-heard-of/) | 2023-12-15 | FD01 |
| S05 | [Technical.ly: Pinkaloo raise](https://technical.ly/baltimore/2019/12/05/pinkaloo-startup-raises-million-squadra-vc-guy-filippelli-mike-leffer/) | 2019-12-05 | FD03 |
| S06 | [Finovate: Pinkaloo $1.25M](https://finovate.com/pinkaloo-raises-1-25-million/) | 2019 | FD03 |
| S07 | [Technical.ly: Eastern Bank pilot](https://technical.ly/baltimore/2019/07/19/masschallenge-fintech-accelerator-pinkaloo-launches-charitable-giving-pilot-eastern-bank) | 2019-07-19 | FD03 |
| S08 | [Crunchbase News: Amicus Series B](https://news.crunchbase.com/news/making-philanthropy-as-easy-as-banking-amicus-io-raises-8-7m-series-b) | 2020-11 | FD04 |
| S09 | [Hypepotamus: Amicus](https://www.hypepotamus.com/amicus-donor-advised-funds/) | 2020 | FD04 |
| S10 | [InvestmentNews: TIFIN acquires Amicus](https://www.investmentnews.com/fintech/tifin-group-acquires-fintech-targeting-donor-advised-funds/218849) | 2022-03 | FD04 |
| S11 | [TIFIN release: Louise expansion](https://tifin.com/news/tifin-announces-the-expansion-of-its-fintech-platform-for-personalized-charitable-giving-to-democratize-access-to-donor-advised-funds/4961/) | 2022 | FD04 |
| S12 | [WealthManagement: AssetMark–TIFIN Give](https://www.wealthmanagement.com/philanthropy/assetmark-announces-strategic-collaboration-with-tifin-give) | 2024 | FD04 |
| S13 | [Newswire: Charityvest $3.7M](https://www.newswire.com/news/this-startup-raised-3-7m-to-let-anyone-donate-stocks-and-etfs-with-a-21260863) | 2020-11-19 | FD05 |
| S14 | [For Good: software now part of Bonterra](https://www.forgood.org/landing-pages/our-donation-software-is-now-part-of-bonterra) | reviewed 2026-11-14 | FD09 |
| S15 | [Business Wire: Network for Good renamed For Good](https://www.businesswire.com/news/home/20250529977479/en/Donor-Advised-Fund-Network-for-Good-Unveils-New-Name-For-Good) | 2025-05-29 | FD09 |
| S16 | [InfluenceWatch: Network for Good (advocacy source)](https://www.influencewatch.org/non-profit/network-for-good/) | undated | FD09 |
| S17 | [Payments Dive: Philanthropi](https://www.paymentsdive.com/news/fintech-philanthropi-taps-into-giving-surge-payments/626794/) | 2022-07-08 | FD10 |
| S18 | [PR Newswire: Philanthropi $4M](https://prnewswire.com/news-releases/philanthropi-raises-4m-in-funding-to-power-the-charitable-giving-legacies-of-everyday-philanthropists-301445028.html) | 2022 | FD10 |
| S19 | [TechCrunch: Bright Funds launch](https://techcrunch.com/2012/11/26/mutual-funds-for-non-profits-bright-funds-wants-to-be-the-vanguard-for-charitable-giving) | 2012-11-26 | FD11 |
| S20 | [Business Wire: WizeHive + Bright Funds](https://www.businesswire.com/news/home/20211117005215/en/WizeHive-Combines-Forces-with-Bright-Funds-to-Create-Comprehensive-Corporate-Giving-Solution) | 2021-11-17 | FD11 |
| S21 | [LLR: Submittable acquires WizeHive](https://www.llrpartners.com/submittable-acquires-wizehive-cementing-its-leadership-in-social-impact-tech/) | 2024-08-08 | FD11 |
| S22 | [CB Insights: Bright Funds financials](https://www.cbinsights.com/company/bright-funds/financials) | n.d. | FD11 |
| S23 | [Chronicle: mutual funds for nonprofits](https://www.philanthropy.com/news/mutual-funds-for-nonprofits-help-donors-diversify-giving/) | n.d. | FD11 |
| S24 | [Business Wire: Groundswell $15M seed](https://www.businesswire.com/news/home/20211130005365/en/Groundswell-Announces-A-Total-of-15M-in-Seed-Funding-To-Democratize-Philanthropy) | 2021-11-30 | FD12 |
| S25 | [Shift4 FY2022 10-K financial report (SEC)](https://www.sec.gov/Archives/edgar/data/1794669/000179466923000006/Financial_Report.xlsx) | 2023-02 | FD13 |
| S26 | [Shift4 FY2023 10-K financial report (SEC)](https://www.sec.gov/Archives/edgar/data/1794669/000179466924000007/Financial_Report.xlsx) | 2024-02 | FD13 |
| S27 | [Payments Dive: Shift4 buys two companies](https://www.paymentsdive.com/news/shift4-to-buy-2-companies-for-579m/619624/) | 2022-03 | FD13 |
| S28 | [The Block: Giving Block cuts 12%](https://www.theblock.co/post/203351/the-giving-block-cuts-about-12-of-its-workforce) | 2023-01 | FD13 |
| S29 | [Decrypt: FTX Future Fund shutters](https://decrypt.co/114197/ftx-foundation-shutters-effective-altruism-fund-key-execs-resign) | 2022-11 | FD14 |
| S30 | [Fortune: FTX bankruptcy and charity](https://fortune.com/2022/11/14/ftx-bankruptcy-puts-charitable-donations-in-doubt-and-some-blame-sam-bankman-frieds-effective-altruism-mindset-for-troubles/) | 2022-11-14 | FD14 |
| S31 | [Decrypt: Endaoment $2.5M](https://decrypt.co/72524/on-chain-charity-endaoment-lands-2-5m-investment-led-framework-ventures) | 2021-06 | FD15 |
| S32 | [Endaoment blog: $6.67M](https://blog.endaoment.org/blog/announcing-endaoments-6-67m-capital) | 2022-06 | FD15 |
| S33 | [InvestmentNews: Altruist adds DAFs](https://www.investmentnews.com/goria/custodian/altruist-adds-donor-advised-funds-with-no-minimums-for-advisors/268481) | 2026-10-06 | FD15 |
| S34 | [NPQ: Flipcause bankruptcy](https://nonprofitquarterly.org/nonprofits-in-limbo-as-flipcause-bankruptcy-unfolds/) | 2026-03-13 | FD16 |
| S35 | [UK Fundraising: Ammado liquidation](https://fundraising.co.uk/2018/02/01/ammado-liquidation-e3-8bn-donations-unaccounted-for/) | 2018-02-01 | FD17 |
| S36 | [TechCrunch: Ammado raises $9M](https://techcrunch.com/2012/02/20/ammado-raises-9m-to-solve-global-giving-problem/) | 2012-02-20 | FD17 |
| S37 | [Giving Assistant FAQ](https://givingassistant.org/insights/news/giving-assistant-frequently-asked-questions) | post-2022 | FD18 |
| S38 | [Doctor of Credit: Giving Assistant shutting down](https://www.doctorofcredit.com/giving-assistant-shopping-portal-shutting-down/) | 2021–2022 | FD18 |
| S39 | [ioby closing notice](https://ioby.org/resources/closing/) | 2024 | FD22 |
| S40 | [Chronicle op-ed: crowdfunding collapse](https://www.philanthropy.com/opinion/why-the-quiet-collapse-of-a-crowdfunding-platform-should-alarm-philanthropy/) | 2024–25 | FD22 |
| S41 | [NonProfit Times: GoFundMe Charity shut down](https://thenonprofittimes.com/technology/gofundme-charity-being-shut-down/) | 2021-02-10 | FD23 |
| S42 | [UK Fundraising: Virgin Money Giving to close](https://fundraising.co.uk/2021/08/26/virgin-money-giving-to-close-in-november/) | 2021-08-26 | FD24 |
| S43 | [Civil Society: VMG closes](https://www.civilsociety.co.uk/news/virgin-money-giving-will-close-this-year-as-london-marathon-partnership-ends.html) | 2021 | FD24 |
| S44 | [UK Fundraising: BT MyDonate to close](https://fundraising.co.uk/2019/01/21/bt-mydonate-close-june/) | 2019-01-21 | FD25 |
| S45 | [9to5Google: One Today killed](https://9to5google.com/2020/01/29/google-one-today-donation-killed/) | 2020-01-29 | FD26 |
| S46 | [PYMNTS: Google to shut donation app](https://www.pymnts.com/news/2020/google-to-shut-down-nonprofit-donation-app/) | 2020 | FD26 |
| S47 | [GBH/AP: Amazon ends AmazonSmile](https://www.wgbh.org/news/national/2023-01-19/amazon-ends-its-charity-donation-program-following-other-cost-cutting-efforts) | 2023-01-19 | FD27 |
| S48 | [Fortune: AmazonSmile ends](https://www.fortune.com/2023/01/19/amazon-smile-charity-ends-layoffs-tech-not-grown-impact/) | 2023-01-19 | FD27 |
| S49 | [America's Charities acquires Causecast](https://www.charities.org/news/americas-charities-acquires-causecast-giving-platform-further-strengthening-its-support-social/) | 2019-07-31 | FD28 |
| S50 | [Business Wire: Bloomerang acquires Kindful](https://www.businesswire.com/news/home/20210107005891/en/Bloomerang-Acquires-Kindful-to-Accelerate-Vision-of-Helping-Nonprofits-Fund-Their-Missions) | 2021-01-07 | FD29 |
| S51 | [TrustRadius: Kindful discontinued](https://www.trustradius.com/compare-products/bloomerang-vs-kindful) | n.d. | FD29 |
| S52 | [Inside Philanthropy: GoodWorld](https://insidephilanthropy.com/home/2017/3/1/this-startup-wants-to-make-donate-the-future-of-online-fundraising) | 2017-03-01 | FD30 |
| S53 | [FinTech Futures: GoodWorld Australia](https://www.fintechfutures.com/fintech/charity-donation-fintech-goodworld-launches-in-australia) | 2020-07-22 | FD30 |
| S54 | [GoodWorld current site](https://goodworldnow.com/) | reviewed 2026-11-14 | FD30 |
| S55 | [InvestmentNews: Swell shuttered](https://www.investmentnews.com/fintech/pacific-life-shutters-esg-robo-adviser-swell-investing/80592) | 2019-07 | FD31 |
| S56 | [Doctor of Credit: Swell closing date](https://www.doctorofcredit.com/swell-investing-to-shut-down-on-august-30th-2019/) | 2019-07 | FD31 |
| S57 | [Built In: Swell $30M](https://builtin.com/articles/swell-announces-funding-expansion) | 2018 | FD31 |
| S58 | [American Banker: Aspiration](https://www.americanbanker.com/news/aspiration-a-tree-planting-neobank-felled-by-investor-fraud) | 2025 | FD32 |
| S59 | [Banking Dive: Aspiration co-founder plea](https://www.bankingdive.com/news/aspiration-co-founder-wire-fraud-plead-guilty/758787/) | 2025 | FD32 |
| S60 | [BetaKit: Benevity layoffs](https://betakit.com/?p=352010) | 2023-01 | FD33 |
| S61 | [CTV: Benevity lays off 137](https://calgary.ctvnews.ca/calgary-tech-firm-benevity-lays-off-137-workers-cites-poor-market-conditions-1.6237343) | 2023-01-18 | FD33 |
| S62 | [Civil Society: Blackbaud completes JustGiving](https://www.civilsociety.co.uk/news/blackbaud-confirms-completion-of-justgiving-acquisition.html) | 2017-10-03 | FD35 |
| S63 | [TechCrunch: Givz tag](https://techcrunch.com/tag/givz/) | 2021-08-23 | FD36 |
| S64 | [Give Lively: Giving Basket FAQ](https://www.givelively.org/faqs/what-is-charity-navigators-giving-basket) | n.d. | FD37 |
| S65 | [Betterment charitable giving disclosure](https://www.betterment.com/legal/charitable-giving) | 2025-12-23 | FD38 |
| S66 | [Business Wire: Grapevine seed](https://www.businesswire.com/news/home/20230808466348/en/Grapevine-Closes-1.85M-Total-Seed-Round-Delivers-25-Million-To-Nonprofits-To-Democratize-Philanthropic-Giving) | 2023-08-08 | FD40 |
| S67 | [ThinkAdvisor: Fidelity Charitable ends minimums](https://www.thinkadvisor.com/2020/09/30/fidelity-charitable-ends-daf-account-minimums/) | 2020-09-30 | FD46 |
| S68 | [FA Mag: ImpactAssets lowers fees](https://www.fa-mag.com/news/impactassets-lowers-fees-and-minimums-37664.html) | 2018-03 | FD45 |

The remaining URLs for no-adverse-outcome checks are in the CSV `evidence_urls` column. Reused prior-repo sources: TA14–TA34, HL01–HL33, X01–X11, EV01–EV24.

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-10** (research/mission-2026-11-14/failed-daf-startups-deep-research.md line 243): replace "in December 2025, **Stripe froze a $1.45M reserve**" → "in December 2025 Stripe terminated processing and held a reserve that Flipcause's filings list at $1.45M (Stripe's objection puts it below $1M, about $790k at issue)"
- **W4-11** (same file line 251): replace "The founder testified that the donations belonged to Flipcause" → "Co-founder and Executive Chairman Emerson Ravyn testified at the 2025-12-22 bankruptcy hearing that donations belonged to Flipcause (the debtor's position, not a court finding)"
