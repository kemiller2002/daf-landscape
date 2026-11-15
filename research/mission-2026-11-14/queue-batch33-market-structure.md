# Queue batch 33 C: market structure (corporate exits, grant-software consolidation, faith platforms, Edward Jones and Goldman)

**Date:** 2026-11-15. **Agent:** batch33 C. **Recency rule:** 2021+ evidence. Older facts are labelled as dated context.
**Queue items:** P-FAIL-09, P-PE-05, Q-B08 + P-LSG-04, Q-B05 + Q-N08.
**Read first:** `failed-daf-startups-deep-research.md` (wave-4 corrections), `queue-batch32-feeds-owners-codebases.md` (wave-17 corrections), `queue-ledger-segment-npact-owner.md` (§8 and wave-12 corrections), `queue-all-in-cost-dafpay-access.md` (wave-10 corrections), `private-equity-daf-ecosystem-map.md`, `queue-bank-programs-and-eft-providers.md`, `../edward-jones-ren-second-pass-pricing-private-daf-2026-11-12.md`.
**New data:**
- [`faith-sponsor-platforms-2026.csv`](../../data/mission-2026-11-14/faith-sponsor-platforms-2026.csv) (37 rows)
- [`relationship-graph-edges-additions-18.csv`](../../data/mission-2026-11-14/relationship-graph-edges-additions-18.csv) (ER001–ER018)
- [`queue-proposals-batch33c.csv`](../../data/mission-2026-11-14/queue-proposals-batch33c.csv) (P-B33C-01 to -03)

Labels: **[F]** first-party document read this pass. **[X]** 990 filing. **[S]** secondary press. **[I]** inference. **[R]** search-index capture only.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-FAIL-09: why corporate giving products ended** | **The stated reasons are low adoption or impact, cost, or the loss of a parent's marketing purpose. None cited regulation or fraud.**<br>- AmazonSmile: "spread too thin" across more than 1m charities; US average $230 per charity in 2022. It closed amid 18,000 layoffs.<br>- Virgin Money Giving: needed "significant investment" to stay competitive and lost its London Marathon "brand exposure".<br>- Google One Today: donors "chose other products" (2020, dated context).<br>- GoFundMe Charity: folded into the parent to put personal and charity fundraising on one platform.<br>- **Meta (2023–24, not in the earlier set):** stopped absorbing fees, moved all US/UK/CA/AU giving to PayPal Giving Fund (a DAF-type sponsor) and switched charity fundraising off in the EEA.<br>**Lesson:** for a giant, giving is a marketing feature that is cut or handed off. Notice ran from 10 days to about 8 months. | High on stated reasons; Meta reasons not given |
| **P-PE-05: grant-management consolidation** | **One roll-up is complete; the other 2021-vintage holdings are unchanged.**<br>- **Completed:** L Squared's Foundant + SmartSimple (2024-08-13) + GivingData (May 2025), with one CEO and no product migration.<br>- **Unchanged since their deals:** Fluxx (Metamorph/ABS, 2021-10-20); Submittable (bought WizeHive/Bright Funds from LLR's portfolio, 2024-08-08); Instrumentl (Summit minority, 2025-04-23).<br>- **Bonterra (Apax)** is the active acquirer: OneCause 2025-10, Deed 2026-03, EBITDA ">$100 million".<br>- **Overlap with DAF ledgers** runs through two routes:<br>  - Foundant CommunitySuite: the CF back office, about $21.5bn implied.<br>  - Pass-through DAF charities tied to software owners (Blackbaud Giving Fund, Network for Good, CAF America, PayPal Giving Fund, AOGF/Benevity): about $4.4bn of FY2024 DAF grants. | High (deals); medium (overlap) |
| **Q-B08: do faith sponsors share platforms?** | **No single platform. The $20.2bn faith segment (186 sponsors, FY2024) splits into five vendor clusters plus one captive build.**<br>- **NCF:** Salesforce captive, $5.46bn.<br>- **Give Interactive:** $1.95bn confirmed (Signatry, WaterStone); $4.82bn if Jewish Communal Fund is confirmed.<br>- **Ren:** about $3.0bn (CJP Boston on DFX, Thrivent and CCF-LA on iPhi, JFGP/Seattle admin).<br>- **FidTech DonorSphere:** about $1.0bn, almost all Jewish federations and foundations.<br>- **akoyaGO:** $0.73bn (JCF Los Angeles).<br>- **Salesforce outside NCF:** JCF San Francisco and JCF San Diego. | Medium-high; 18% of segment unresolved |
| **P-LSG-04: size of the Salesforce-centred ledger route among faith sponsors** | **Salesforce touches about $7.1bn (35%) of faith DAF assets, but 77% of that is NCF alone. A Salesforce ledger is named for only $0.55bn (2.7%):** JCF San Diego (Fund 360) and Richmond Jewish Foundation (AccuFund + Salesforce), plus Catholic Foundation of Eastern Washington (not in DAFRC).<br>- Salesforce portal with the GL not named: NCF ($5.46bn) and JCF SF ($1.0bn).<br>- CRM-only: CCF Minnesota ($0.10bn).<br>- At Jewish federations, Salesforce displaces FidTech only where a Salesforce portal is now live (JCF SF). Pittsburgh pays both FidTech and Armanino. | Medium |
| **Q-B05 / Q-N08: Edward Jones private DAF and Goldman stack** | **Edward Jones private DAF: the sponsor, administrator and vendor are still not public** (release 2025-09-16, re-checked 2026-11-15). New first-party facts:<br>- The live EJ product page states RCF "manages and administers" the Charitable Gift Fund.<br>- Edward Jones' 2024 report gives the program as "nearly $535 million" assets under care and ">$90 million" granted in 2023.<br>**Goldman:** no 2021+ program document found. The newest public GSPF circular is dated **2017-12-05**, not 2008 as the repo states. It shows Ayco selecting the ETF options for a 50 bp fee. The live stack is unchanged: Ren iPhi donor web, Ayco admin, Goldman.com SSO. A new two-hop inference: GS Gives grant administration runs through CAF America, a Bonterra customer. | High (EJ text); GS stays "insufficient evidence" |

---

## 1. P-FAIL-09: why big-tech and corporate giving products closed

### 1.1 Shutdown notices and stated reasons

| Product (owner) | Announced → end | Stated reason (quoted) | Context | Notice | Source |
|---|---|---|---|---|---|
| **AmazonSmile** (Amazon) | 2023-01-18/19 → 2023-02-20 | "After almost a decade, the program has not grown to create the impact that we had originally hoped"; "With so many eligible organizations — more than 1 million globally — our ability to have an impact was often spread too thin" | "Over $400 million to U.S. charities and more than $449 million globally". "In 2022, AmazonSmile's average donation per charity was $230 in the U.S." One-time payment equal to three months of 2022 earnings. Followed the 18,000-layoff announcement | ~1 month | [TechCrunch 2023-01-19](https://techcrunch.com/?p=2472470) [S]; [GBH/AP 2023-01-19](https://www.wgbh.org/news/national/2023-01-19/amazon-ends-its-charity-donation-program-following-other-cost-cutting-efforts) [S] |
| **Virgin Money Giving** (Virgin Money UK) | 2021-08-26 → 2021-11-30 | After a strategic review, "significant investment [is] required in the service for it to remain competitive", and it would lose the "brand exposure" of the London Marathon sponsorship. "It is the right time to bring the service to a close" (Helen Page, chief brand officer) | "Since its launch in 2009, it has helped 20,000 charities and raised over £900m". A "not-for-profit service"; about 26 roles cut | ~3 months | [Civil Society 2021-08-26](https://www.civilsociety.co.uk/news/virgin-money-giving-will-close-this-year-as-london-marathon-partnership-ends.html) [S]; [UK Fundraising 2021-08-26](https://fundraising.co.uk/2021/08/26/virgin-money-giving-to-close-in-november/) [S] |
| **GoFundMe Charity** (GoFundMe) | early 2021 → donations end 2021-09-30; platform off 2021-12-31 | Unite charity and personal fundraising on GoFundMe.com; campaigns not migrated; third-party integrations off 2021-03-31 | GoFundMe later bought Classy (now GoFundMe Pro). In Oct 2025 GoFundMe apologised after creating about **1.4 million nonprofit pages without consent** from IRS and partner data (including PayPal Giving Fund): "We are very sorry for this and take responsibility for missing the mark". Pages became opt-in and unclaimed pages are de-indexed. Default donor tip 16.5% | ~8 months | [NonProfit Times 2021-02-10](https://thenonprofittimes.com/technology/gofundme-charity-being-shut-down/) [S]; [Funraise timeline](https://funraise.org/blog/is-gofundme-charity-closing-what-do-i-do-about-it) [S]; [ABC7 2025-10-29](https://abc7news.com/post/gofundme-apologizes-creating-donation-pages-nonprofits-consent-vows-make-changes/18082313/) [S] |
| **Meta fundraising tools, US/UK/CA/AU** (Meta) | Aug 2023 email → 2023-10-31 | No reason given. A Meta spokesperson "would not comment further on that decision"; the email said fees "are a big change that can impact your nonprofit" | "All donations made on Facebook and Instagram will be processed through the PayPal Giving Fund". Fees of 1.99% + $0.49 now fall on nonprofits unless the donor covers them. Recurring donations ended. Meta reports $7bn raised since 2013 | ~2–3 months | [Chronicle of Philanthropy 2023-10-10](https://www.philanthropy.com/news/fees-to-return-on-facebook-and-instagram-donations/) [S] |
| **Meta fundraising tools, EEA** (Meta) | Apr 2024 → 2024-07-01 | No reason given; Meta's blog says "This year, we are evolving our approach to help more non-profits reach more donors" | EEA charities must send donors to their own sites. PayPal Giving Fund Ireland products affected | ~2 months | [Irish Times 2024-04-26](https://www.irishtimes.com/business/2024/04/26/facebook-and-instagram-pull-the-plug-on-charity-fundraising) [S] |
| *Google One Today* (Google), dated context | 2020-01-27 → 2020-02-06 | Usage declined; donors chose "other products" | Charities came from Google for Nonprofits | 10 days | [9to5Google 2020-01-29](https://9to5google.com/2020/01/29/google-one-today-donation-killed/) [S] |
| *BT MyDonate* (BT), dated context | 2019-01 → 2019-06 | (see FD25) | Commission-free | ~5 months | [UK Fundraising 2019-01-21](https://fundraising.co.uk/2019/01/21/bt-mydonate-close-june/) [S] |

No first-party notice was retrievable this pass. Amazon's `aboutamazon.com` update and Virgin Money's newsroom article both returned 404. The quotes above are as reproduced by the press.

### 1.2 Lessons for DAF entrants that partner with a distribution giant

1. **Giving is a feature at the giant, not the business.**
   - Every stated reason concerns the parent: impact per dollar, investment against return, loss of sponsorship exposure, or product consolidation.
   - Closures cluster with cost-cutting (Amazon, January 2023) or the end of a marketing contract (Virgin Money).
   - **[I]** A DAF partner embedded in a giant's checkout or app has no contractual protection against this unless the partnership agreement provides one.
2. **When the giant keeps giving, it hands processing to a DAF-type intermediary.**
   - Meta now routes all US/UK/CA/AU charitable giving through PayPal Charitable Giving Fund. PPGF FY2024: 694,979 DAF accounts, $626.6m grants ([DAFRC FY2024 row](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) [X].
   - Google Assistant donations went to Network for Good, a DAF (dated context).
   - The intermediary role is the durable position. The consumer brand is not.
3. **Fees move to the nonprofit when the giant stops subsidising.** Meta stopped covering fees in 2023 (1.99% + $0.49) and GoFundMe defaults a 16.5% tip. An entrant cannot assume subsidised economics will last.
4. **Notice periods are short and data does not migrate.**
   - Notice: Google 10 days, Amazon about 1 month, Meta EEA about 2 months, Virgin Money about 3 months.
   - GoFundMe Charity campaigns were not migrated, and FD23 records data-deletion deadlines.
   - **[I]** A DAF entrant needs donor-record portability written into any distribution deal.
5. **Scale without consent is a reputational risk.** GoFundMe's 1.4m auto-created nonprofit pages (2025) built a directory from IRS and PayPal Giving Fund data and was reversed within weeks after sector pushback. A DAF-based "give to any charity" directory needs charity opt-in.

---

## 2. P-PE-05: grant-management consolidation

### 2.1 Ownership and deals, 2021+

| Company | Owner / deal (date) | Later events | DAF-ledger overlap | Source |
|---|---|---|---|---|
| **Foundant Technologies** | L Squared Capital Partners, "Strategic Investment" (2023-02-15; William Blair says closed 2023-02-01) | Merged with SmartSimple (2024-08-13); GivingData joined (May 2025). Joint CEO Josh Mallamud: "nothing changes for you"; "You will continue to use the same products" | **Direct.** CommunitySuite is a CF DAF back office: about $21.5bn implied across 360 CFs (`queue-ledger-segment-npact-owner.md`); 2026-09 DAFpay API route | [L Squared 2023-02-15](https://www.lsquaredcap.com/2023/02/15) [F]; [L Squared 2024-08-13](https://www.lsquaredcap.com/2024/08/13) [F]; [Business Wire 2024-08-13](https://businesswire.com/news/home/20240813514222/en/Foundant-Technologies-and-SmartSimple-Software-Announce-Strategic-Merger-to-Revolutionize-Philanthropic-and-Grant-Management-Solutions) [F]; [Foundant Compass, May 2025](https://community.foundant.com/funders_community_foundations/discussion/2955/we-are-excited-to-announce-that-givingdata-is-joining-the-foundant-smartsimple-team) [F] |
| **SmartSimple** | Part of Foundant (L Squared) since 2024-08 | — | **Portal-side.** The Boston Foundation pays DAF grants "via Smart Simple portal" (EG012) | as above |
| **GivingData** | Part of Foundant (L Squared) since May 2025 | — | None found (private-foundation grant management) | as above |
| **Fluxx** | Metamorph Partners (lead) and ABS Capital Partners (2021-10-20, terms undisclosed) | Grantseeker add-on reported 2025-11 (aggregator grade A in `pe-ownership-by-company.csv`). No change of control found through 2026-11 | None found in the CF ledger maps | [Business Wire 2021-10-20](https://www.businesswire.com/news/home/20211020005559/en/Data-Driven-Grant-Management-Technology-Leader-Fluxx-Announces-Acquisition-by-Metamorph-Partners-and-ABS-Capital-Partners) [F] |
| **Submittable** | LLR Partners invested in **WizeHive** (2021-06-28), not in Submittable directly; Submittable bought WizeHive (with Bright Funds) 2024-08-08; LLR lists Submittable in its portfolio | — | Indirect: Bright Funds (workplace giving) | [LLR: WizeHive 2021](https://www.llrpartners.com/wizehive-secures-growth-capital-investment-from-llr-partners/) [F]; [LLR: Submittable acquires WizeHive 2024-08-08](https://www.llrpartners.com/submittable-acquires-wizehive-cementing-its-leadership-in-social-impact-tech/) [F] |
| **Instrumentl** | Summit Partners $55m minority growth (2025-04-23); 4,500+ customers | — | None (tool for grant seekers) | [Summit 2025-04-23](https://www.summitpartners.com/news/instrumentl-raises-55m-from-summit-partners-to-accelerate-their-ai-grant-fundraising-platform) [F] |
| **Bonterra** (CyberGrants, EveryAction, Social Solutions, Network for Good software) | Apax (CyberGrants 2021-06; combination 2021-08) | OneCause (2025-10-15); Deed (2026-03-05). Apax 2026-05-28: EBITDA "grown four-fold to over $100 million"; giving "c.$10bn per year"; "further M&A ambitions still to come" | **Pass-through DAFs as customers:** Network for Good DAF (FY2024 grants $428m); CAF America (grants $821m; EC003); CF of Western Massachusetts (EC005) | [Apax 2026-05-28](https://www.apax.com/news-views/how-an-apax-backed-tech-provider-is-transforming-charitable-giving/) [F] |
| **Blackbaud Grantmaking / YourCause** | Public (Clearlake 20.10% per 2025 proxy, batch 32 §2) | FIMS/DonorCentral sold to NPact 2022-09 (repo) | **Ledger:** Financial Edge NXT at CCF and Catholic Foundation of Greater Philadelphia. **Pass-through:** Blackbaud Giving Fund, "a 501(c)3 Public Charity … separate from and independent of Blackbaud", YourCause partner since 2020-08-01; FY2024 DAF grants $552.6m | [Blackbaud NPOconnect help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect-qa/content/npo-faq-about-blackbaud-giving-fund-bbgf.html) [F] |
| *Benevity*, dated context | Hg majority at a US$1bn valuation (2020-12-03) | US$90.1m equity issued to Dec 2025; CEO change Nov 2025 ([The Logic](https://thelogic.co/briefing/british-private-equity-firm-buys-majority-stake-in-calgary-startup-benevity/)) [S] | **Pass-through:** American Online Giving Foundation, FY2024 DAF grants $1.95bn (repo `aogf-benevity-reconciliation.csv`) | — |

### 2.2 Reading

- **The consolidation question is now about Fluxx and Submittable.**
  - Foundant/SmartSimple/GivingData is already a three-brand family under one CEO, with explicit no-migration promises.
  - Fluxx (Metamorph, 2021-10) and the WizeHive stake in Submittable (LLR, 2021-06) reach five years in 2026.
  - No sale process for either was found [F for absence through 2026-11-15; no claim of a process].
- **[I] Combination probability, 2026–28.** The repo's PE map rates an L Squared exit in 2027–29 "L–M" (line 239). Nothing found this pass changes that.
  - **For community-foundation DAF back offices, the risk sits with Foundant, not Fluxx.** Foundant is the only grant brand that is also a DAF ledger.
  - **An L Squared exit is a change of control over about $21.5bn of implied CF DAF ledgers.** A buyer that rationalises products would hit CommunitySuite users. The May 2025 "nothing changes" letter binds only the current owner.
- **The second overlap is the pass-through DAF charity.** Each large giving-software owner has a charity that legally receives and regrants the money:
  - Blackbaud → BBGF
  - Bonterra → NFG and CAF America (customer)
  - Benevity → AOGF
  - PayPal → PPGF (Meta's processor since 2023)
  - Submittable → Bright Funds (not sized)

  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC). A software sale or roll-up therefore also moves control of a DAF-sponsor relationship. P-B33C-02 proposes sizing this.

---

## 3. Q-B08 + P-LSG-04: faith and affinity sponsors

### 3.1 Method

- **Universe:** DAFRC FY2024 rows with subtype "Religiously-Affiliated", plus Servant Foundation and The Signatry Charitable Trust (typed National/Standard). That gives **186 sponsors, $20.18bn of DAF assets**.
- **Coverage:** `faith-sponsor-platforms-2026.csv` covers all faith sponsors at or above $100m, plus every smaller faith sponsor with platform evidence in the repo: **$18.10bn (90%)**.
- **Evidence sources:**
  - Existing edges (EA/EB/EC/EH/EJ/EK/EM/EN series).
  - The TY2021–25 990 Part VII-B harvest (`form990-contractors-harvest-full.csv`).
  - New live checks this pass of sponsor home pages, recording the host each "login" link points to. The checks were page fetches only, with no sign-in.

**New live evidence (2026-11-15) [F]:**
- **CJP Boston → Ren DFX.** [cjp.org DAF page](https://www.cjp.org/donor-advised-funds) links [cjp.donorfirstx.com](https://cjp.donorfirstx.com/), which carries "DFX powered by Ren" (ER002).
- **JCF Los Angeles → akoyaGO.** The Giving Portal links [gofund.akoyago.com/jcfla](https://gofund.akoyago.com/jcfla/) (ER004).
- **JCF San Francisco → Salesforce Experience Cloud.** It links [jewishfed.my.site.com/portal](https://jewishfed.my.site.com/portal/s/login/). The old `jewishfed.donorfirst.org` host no longer resolves (ER003).
- **NCF → Salesforce.** [secure.ncfgiving.com](https://secure.ncfgiving.com/) answers with `server: sfdcedge` (ER001).
- **Cleveland and Miami federations → DonorSphere.** [jewishcleveland.donorsphere.org](https://jewishcleveland.donorsphere.org/) and [jewishmiami.donorsphere.org](https://jewishmiami.donorsphere.org/login) (ER005, ER006).
- **Re-confirmed:** Signatry → Give Interactive; WaterStone → Give Interactive; Thrivent → iPhi; Associated (Baltimore) → DonorSphere.

### 3.2 Platform families by FY2024 DAF assets

| Family | Sponsors (FY2024 DAF assets) | $bn | Share of $20.18bn |
|---|---|---|---|
| Salesforce captive portal (Stellar component behind it; GL inferred NetSuite) | NCF $5.46bn | 5.46 | 27.1% |
| Give Interactive, confirmed | Servant Foundation + Signatry Charitable Trust $1.41bn (owns Give Interactive, EB001); WaterStone $0.54bn | 1.95 | 9.7% |
| Give Interactive, inferred | Jewish Communal Fund NY $2.87bn (staging tenants only; Ren portal support ended by FY6/2023) | 2.87 | 14.2% |
| Ren (DFX, iPhi, admin) | CJP $1.93bn (DFX); Thrivent $0.59bn, CCF-LA $0.35bn, Methodist/Catholic small (iPhi); JFGP $0.10bn and Seattle $0.02bn (admin) | 3.00 | 14.8% |
| FidTech DonorSphere | MetroWest NJ, Baltimore, Cleveland, Detroit, Pittsburgh, Colorado, Northern NJ, FUMF; Miami (DonorSphere portal + Ren admin) | 1.03 | 5.1% |
| Salesforce, other (portal or ledger) | JCF SF $1.00bn (portal); Richmond $0.01bn (AccuFund + SF) | 1.01 | 5.0% |
| Salesforce-native ledger (Fund 360) | JCF San Diego $0.54bn (GiftingNetwork portal) | 0.54 | 2.7% |
| akoyaGO (Dynamics 365) | JCF Los Angeles | 0.73 | 3.6% |
| Others with evidence | Charlotte JCF via Foundation For The Carolinas (GiftingNetwork) $0.17bn; KofC Charitable Fund, affiliate admin $0.13bn; CCF Minnesota, SF CRM only $0.10bn; Chicago JUF, Stellar 2021 only $0.31bn; Catholic Fdn Greater Philadelphia, Blackbaud FE + NPact $0.02bn | 0.74 | 3.7% |
| Unknown | Federation EIN 58-1021791; Christian Community Foundation EIN 62-1752885; Dallas JCF; Houston JCF; others below $100m not checked | 0.78 + ~2.1 not covered | ~14% |

### 3.3 Answers

- **Q-B08.** Faith sponsors do **not** share a common platform. Two patterns stand out:
  1. **Christian national sponsors are mostly vertically integrated.**
     - NCF built its own portal on Salesforce.
     - The Signatry owns its vendor (Give Interactive).
     - Thrivent pays Ren while carrying Give Interactive staging tenants.
     - WaterStone moved from iPhi to Give Interactive.
  2. **Jewish federations and foundations divide by size.**
     - Mid-size federations cluster on FidTech DonorSphere.
     - The largest have moved to separate stacks: CJP on Ren DFX, JCF LA on akoyaGO, JCF SF on Salesforce, JCF SD on Fund 360, JCF NY probably on Give Interactive.
- **P-LSG-04.** The Salesforce-centred route among faith sponsors is **$7.10bn (35%) if any Salesforce role counts**. That is $1.64bn without NCF. It is **$0.55bn (2.7%) with a named Salesforce ledger**.
  - Compared with the all-sponsor named route of about $3.5bn in `queue-ledger-segment-npact-owner.md`, faith sponsors contribute roughly one-sixth.
  - **Displacement of FidTech by Salesforce is shown at one federation only:** JCF SF, which paid Salesforce implementation consultants $724k in TY2023 and now runs a live Experience Cloud portal.
  - Pittsburgh pays FidTech ($525,587, FYE 6/2025) and Armanino ($536,465, "donor management software consultant") at the same time. Which CRM Armanino implements is not stated [I].
  - **Correction to the queue text:** the Armanino + FidTech facts belong to the **Jewish Federation of Greater Pittsburgh** (EIN 25-1017602), not "JFGP". The Jewish Federation of Greater Philadelphia (EIN 23-1500085) pays Ren ($500,842 "investment administrative srvcs", FYE 8/2025).

---

## 4. Q-B05 + Q-N08: Edward Jones private DAF and the Goldman Sachs stack

### 4.1 Edward Jones

| Fact | Source | Label |
|---|---|---|
| Release text: "A private Donor Advised Fund (DAF) designed for significant philanthropic contributions, giving donors greater flexibility and customization in pricing and investment options". Release dated 2025-09-16; supports "Edward Jones Generations®" (launched May 2025). No sponsor named | [Edward Jones release](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management) (page text retrieved 2026-11-15); [Pulse 2.0, 2025-09-24](https://pulse2.com/edward-jones-services-enhanced-for-high-net-worth-clients/) | F / S |
| Live DAF product page: "The Edward Jones Charitable Gift Fund is a donor-advised fund offered by Edward Jones in conjunction with Renaissance Charitable Foundation Inc., which manages and administers the Fund". The page does not mention a private DAF | [EJ DAF page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds) | F |
| "In 2023: Nearly $535 million of assets under care invested by Edward Jones clients in the Edward Jones Charitable Gift Fund"; "More than $90 million granted to charities" (p.27) | [Edward Jones 2024 Purpose, Inclusion and Citizenship Report](https://cdn-static.findly.com/wp-content/uploads/sites/1392/2024/04/12182652/2024-PIC-Full-Report.pdf) | F |
| The Generations Financial Planning brochure (LGL-19371) describes "charitable strategy analyses and scenario modeling" only. It names no DAF vehicle | [EJ Generations brochure](https://www.edwardjones.com/sites/default/files/dam/xrpw5j7lbt/lgl-19371-a-pb-fnl.pdf) | F |

**Conclusion.** The private DAF's legal sponsor, administrator and technology vendor remain **unknown**; E018 stands, restated as ER016.
- **What changed:**
  - RCF's administrator role for the standard program is now first-party text (ER014). This resolves the "search snippet only" caveat on S43 in `industry-incentives-structural-analysis.md`.
  - The program has a first-party size of about $535m (2023) (ER015).
- **[I]** Next checks: a separately sponsored private DAF should appear as a new program or fee line in RCF's FY2025 audit or 990, or in another sponsor's materials. P-B33C-01 proposes these checks.

### 4.2 Goldman Sachs

- **No 2021+ program circular, donor guide or terms were found.** The PWM philanthropy page (© 2026) says only that the "Goldman Sachs Donor Advised Philanthropy Fund for Wealth Management" is "one of the largest donor-advised funds in the US", available to Private Wealth clients ([pwm.gs.com](https://pwm.gs.com/nam/en-us/what-we-do/philanthropic-strategy)) [F].
- **The newest public circular is dated 2017-12-05**, served from the donor-web domain ([2017 circular](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)) [F, pre-2021]. An undated earlier version (doc 5665050v.6, with references to 2011–12) is also served ([circular v6](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=2PilKgnPYjA%3D&tabid=111&mid=554&forcedownload=true)). Dated-context terms in the 2017 circular:
  - **Ayco:** passive ETF options are "selected by The Ayco Company, L.P. ('Ayco'), a wholly-owned subsidiary of The Goldman Sachs Group, Inc." and carry a "0.50% (50 bps) Ayco fee".
  - **Admin fee:** 0.60% up to $500k, 0.30% to $1m, 0.20% to $2.5m, 0.10% to $10m, 0.05% above.
  - **Grants:** $250 minimum; paid "in the form of a check".
- **The 2021+ stack (repo, unchanged):**
  - Ren iPhi donor web: `gspf.goldman.com` footer "iPhi … Stellar Technology Solutions" (EA017).
  - Ayco "admin. services": $1,026,306 in CY2024 (EA018).
  - Goldman.com SSO button.
  - GS & Co "TECH & INV ADV FEES": $8.08m.
  - GS Gives: Stellar IT $172,604 and CAF America grant administration $875,665 in FY2025 (EA020, EA021).
- **New two-hop inference [I]:** CAF America is a Bonterra technology customer (EC003), so GS Gives' grant administration may run on Bonterra software (ER018, inferred).
- **Quadrant status:** GS PF stays "insufficient evidence". The 2017 circular is pre-2021 and cannot score 2026 criteria under the bounded-truth rule.

---

## 5. Corrections to existing repo text

1. **`queue-bank-programs-and-eft-providers.md` §2 line 51** ("The only public Program Circular is dated 2008"): replace with "The newest public Program Circular is dated 2017-12-05 ([PDF](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)); a 2008 version and an undated v6 are also served. All are pre-2021."
2. **`industry-incentives-structural-analysis.md` line 111 (S43):** the Edward Jones "in conjunction with" text is now read in full from the live page. Drop "search snippet only; unverified" and add "RCF … manages and administers the Fund" (ER014).
3. **Edward Jones "$2.9bn"** (marked unverifiable in `consolidation-changelog.md`): Edward Jones' own figure for 2023 is "nearly $535 million" assets under care (ER015). Any "$2.9bn" figure should not be attributed to the Charitable Gift Fund without a source.
4. **Research queue P-LSG-04 text:** "JFGP paying Armanino … while still on FidTech" should read "Jewish Federation of Greater **Pittsburgh** (EIN 25-1017602)". JFGP (Philadelphia) pays Ren (EC028).
5. **Research queue P-PE-05 text:** "Submittable (LLR 2021)" should read "WizeHive (LLR 2021-06-28), acquired by Submittable 2024-08-08". In the same text, "Foundant/SmartSimple/GivingData (L Squared 2023)" should read "Foundant (L Squared 2023-02); SmartSimple merger 2024-08-13; GivingData May 2025".
6. **E090 (Ren → Jewish Community Federation donorfirst.org portal, inferred):** that host no longer resolves (2026-11-15), and the live portal is Salesforce (ER003). Treat E090 as historical.
7. **EH013 (DonorSphere → Greater Miami Jewish Federation, inferred):** upgrade to confirmed per ER005.
8. **`failed-daf-startups-deep-research.md` corporate-exit table:** add Meta 2023 (fees and PayPal Giving Fund) and Meta EEA 2024 as partial exits. They are not closures, but the giant withdrew from processing.

---

## 6. Limitations

- **Faith segment:** 10% of faith DAF assets ($2.1bn, mostly sponsors under $100m) were not checked. A further $0.78bn of named sponsors has no platform evidence. Jewish Communal Fund ($2.87bn) sits behind a Cloudflare challenge and rests on staging-tenant CT logs.
- **Portal is not ledger.** A portal host shows the donor front end only; the ledger is named for very few sponsors (see `queue-ledger-segment-npact-owner.md` §5).
- **Corporate exits:** the quotes come via press reproductions because the first-party pages returned 404. Meta gave no reason for either change.
- **Grant-software deal values** are undisclosed throughout. Combination probabilities are judgment [I], not market evidence.

---

## Source register

| ID | Source | Date | Used for | Label |
|---|---|---|---|---|
| B33-01 | [TechCrunch: AmazonSmile ends](https://techcrunch.com/?p=2472470) | 2023-01-19 | §1 | S |
| B33-02 | [GBH/AP: Amazon ends AmazonSmile](https://www.wgbh.org/news/national/2023-01-19/amazon-ends-its-charity-donation-program-following-other-cost-cutting-efforts) | 2023-01-19 | §1 | S |
| B33-03 | [Civil Society: Virgin Money Giving to close](https://www.civilsociety.co.uk/news/virgin-money-giving-will-close-this-year-as-london-marathon-partnership-ends.html) | 2021-08-26 | §1 | S |
| B33-04 | [UK Fundraising: VMG to close](https://fundraising.co.uk/2021/08/26/virgin-money-giving-to-close-in-november/) | 2021-08-26 | §1 | S |
| B33-05 | [NonProfit Times: GoFundMe Charity shut down](https://thenonprofittimes.com/technology/gofundme-charity-being-shut-down/) | 2021-02-10 | §1 | S |
| B33-06 | [Funraise: GoFundMe Charity timeline](https://funraise.org/blog/is-gofundme-charity-closing-what-do-i-do-about-it) | 2021 | §1 | S |
| B33-07 | [ABC7: GoFundMe apology on 1.4m pages](https://abc7news.com/post/gofundme-apologizes-creating-donation-pages-nonprofits-consent-vows-make-changes/18082313/) | 2025-10-29 | §1 | S |
| B33-08 | [Chronicle: fees return on Facebook/Instagram](https://www.philanthropy.com/news/fees-to-return-on-facebook-and-instagram-donations/) | 2023-10-10 | §1, ER012 | S |
| B33-09 | [Irish Times: Meta ends EEA fundraising](https://www.irishtimes.com/business/2024/04/26/facebook-and-instagram-pull-the-plug-on-charity-fundraising) | 2024-04-26 | §1 | S |
| B33-10 | [9to5Google: One Today](https://9to5google.com/2020/01/29/google-one-today-donation-killed/) | 2020-01-29 | §1 (dated context) | S |
| B33-11 | [L Squared: Foundant investment](https://www.lsquaredcap.com/2023/02/15) | 2023-02-15 | §2, ER009 | F |
| B33-12 | [L Squared: Foundant–SmartSimple merger](https://www.lsquaredcap.com/2024/08/13) | 2024-08-13 | §2, ER007 | F |
| B33-13 | [Business Wire: Foundant–SmartSimple](https://businesswire.com/news/home/20240813514222/en/Foundant-Technologies-and-SmartSimple-Software-Announce-Strategic-Merger-to-Revolutionize-Philanthropic-and-Grant-Management-Solutions) | 2024-08-13 | §2 | F |
| B33-14 | [Foundant Compass: GivingData joining](https://community.foundant.com/funders_community_foundations/discussion/2955/we-are-excited-to-announce-that-givingdata-is-joining-the-foundant-smartsimple-team) | 2025-05 | §2, ER008 | F |
| B33-15 | [Business Wire: Fluxx acquisition](https://www.businesswire.com/news/home/20211020005559/en/Data-Driven-Grant-Management-Technology-Leader-Fluxx-Announces-Acquisition-by-Metamorph-Partners-and-ABS-Capital-Partners) | 2021-10-20 | §2 | F |
| B33-16 | [LLR: WizeHive growth investment](https://www.llrpartners.com/wizehive-secures-growth-capital-investment-from-llr-partners/) | 2021-06-28 | §2 | F |
| B33-17 | [LLR: Submittable acquires WizeHive](https://www.llrpartners.com/submittable-acquires-wizehive-cementing-its-leadership-in-social-impact-tech/) | 2024-08-08 | §2 | F |
| B33-18 | [Summit: Instrumentl $55m](https://www.summitpartners.com/news/instrumentl-raises-55m-from-summit-partners-to-accelerate-their-ai-grant-fundraising-platform) | 2025-04-23 | §2, ER010 | F |
| B33-19 | [Apax: Bonterra](https://www.apax.com/news-views/how-an-apax-backed-tech-provider-is-transforming-charitable-giving/) | 2026-05-28 | §2, ER011 | F |
| B33-20 | [Blackbaud NPOconnect: About BBGF](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect-qa/content/npo-faq-about-blackbaud-giving-fund-bbgf.html) | undated, live 2026-11-15 | §2, ER013 | F |
| B33-21 | [The Logic: Hg majority in Benevity](https://thelogic.co/briefing/british-private-equity-firm-buys-majority-stake-in-calgary-startup-benevity/) | 2020-12-03 | §2 (dated context) | S |
| B33-22 | [CJP DAF page](https://www.cjp.org/donor-advised-funds) → [cjp.donorfirstx.com](https://cjp.donorfirstx.com/) | live 2026-11-15 | §3, ER002 | F |
| B33-23 | [JCF LA Giving Portal](https://www.jewishfoundationla.org/giving-portal/) → [gofund.akoyago.com/jcfla](https://gofund.akoyago.com/jcfla/) | live 2026-11-15 | §3, ER004 | F |
| B33-24 | [jewishfed.org](https://www.jewishfed.org/) → [jewishfed.my.site.com](https://jewishfed.my.site.com/portal/s/login/) | live 2026-11-15 | §3, ER003 | F |
| B33-25 | [secure.ncfgiving.com](https://secure.ncfgiving.com/) (sfdcedge headers) | live 2026-11-15 | §3, ER001 | F |
| B33-26 | [jewishcleveland.org](https://www.jewishcleveland.org/) → DonorSphere | live 2026-11-15 | §3, ER006 | F |
| B33-27 | [jewishmiami.org](https://www.jewishmiami.org/) → DonorSphere | live 2026-11-15 | §3, ER005 | F |
| B33-28 | [thesignatry.com](https://thesignatry.com/); [waterstone.org](https://www.waterstone.org/); [thriventcharitable.com](https://www.thriventcharitable.com/); [associated.org](https://www.associated.org/) | live 2026-11-15 | §3 re-confirmations | F |
| B33-29 | [DAFRC FY2024 dataset (repo copy)](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv) | Spring 2026 edition | §3 sizing, §2 pass-through | X |
| B33-30 | [990 harvest TY2021–25 (repo)](../../data/mission-2026-11-14/form990-contractors-harvest-full.csv) | 2026-11 | §3 vendor payees | X |
| B33-31 | [Edward Jones release: elevated wealth management](https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/elevated-wealth-management) | 2025-09-16 | §4, ER016 | F |
| B33-32 | [Edward Jones DAF page](https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds) | live 2026-11-15 | §4, ER014 | F |
| B33-33 | [Edward Jones 2024 PIC report](https://cdn-static.findly.com/wp-content/uploads/sites/1392/2024/04/12182652/2024-PIC-Full-Report.pdf) | 2024-04 | §4, ER015 | F |
| B33-34 | [EJ Generations Financial Planning brochure](https://www.edwardjones.com/sites/default/files/dam/xrpw5j7lbt/lgl-19371-a-pb-fnl.pdf) | n.d. (2025) | §4 | F |
| B33-35 | [Pulse 2.0: EJ services for HNW](https://pulse2.com/edward-jones-services-enhanced-for-high-net-worth-clients/) | 2025-09-24 | §4 | S |
| B33-36 | [GSPF Program Circular 2017-12-05](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf) | 2017-12-05 | §4, ER017 | F (pre-2021) |
| B33-37 | [GSPF Program Circular v6](https://gspf.goldman.com/gspf/LinkClick.aspx?fileticket=2PilKgnPYjA%3D&tabid=111&mid=554&forcedownload=true) | undated (~2012) | §4 | F (pre-2021) |
| B33-38 | [GS PWM philanthropic strategy](https://pwm.gs.com/nam/en-us/what-we-do/philanthropic-strategy) | © 2026 | §4 | F |
| B33-39 | [GS Gives FY2025 990](https://projects.propublica.org/nonprofits/organizations/113813663/202611249349302616/full) | FY2025 | §4, ER018 | X |

---

## Data dictionary: `faith-sponsor-platforms-2026.csv`

| Column | Meaning |
|---|---|
| `ein` | Sponsor EIN, no hyphen (blank if not in DAFRC) |
| `sponsor_name` | Common name. Where DAFRC truncates, the name is kept truncated with the EIN, and no city is guessed |
| `faith_tradition` | Christian (with denomination where clear), Jewish (federation or foundation), or Catholic |
| `fy2024_daf_assets_usd` | DAFRC FY2024 `eoy_daf_assets` |
| `fy2024_daf_accounts` | DAFRC FY2024 `number_of_daf_accounts` |
| `donor_portal_platform` | Donor-facing platform and the observed host, or "Not checked" / "Not identified" |
| `portal_evidence_url` | Page whose login link or headers show the platform |
| `portal_evidence_date` | "live YYYY-MM-DD" for a page fetch, or the document date |
| `admin_or_ledger_vendor_evidence` | 990 Part VII-B payees (amount, description, year) or vendor case-study text on administration and ledger |
| `admin_ledger_source_url` | Filing XML, ProPublica page or case study for the previous column |
| `salesforce_route` | `SF_LEDGER` (named ledger in or synced from Salesforce); `SF_PORTAL` (Salesforce-hosted donor portal, GL not named); `SF_PORTAL_PLUS_REN_COMPONENT` (NCF); `SF_CRM` / `SF_CRM_POSSIBLE` (CRM role only); `NONE` (another vendor evidenced); `NONE_SEEN` (no Salesforce evidence, platform partly known); `UNKNOWN` |
| `platform_family` | `SF_CAPTIVE`, `SF_NATIVE`, `SF_OTHER`, `SF_UNCONFIRMED`, `GIVE_INTERACTIVE`, `GIVE_INTERACTIVE_OWNED`, `GIVE_INTERACTIVE_INFERRED`, `REN_DFX`, `REN_IPHI`, `REN_IPHI_HISTORIC`, `REN` (admin service), `FIDTECH`, `FIDTECH_PORTAL_REN_ADMIN`, `AKOYA`, `GIFTINGNETWORK_HOSTED_BY_CF`, `BLACKBAUD_FE_NPACT`, `AFFILIATE_ADMIN`, `UNKNOWN` |
| `confidence` | high / medium / low / none, split by portal and ledger where they differ |
| `edge_refs` | Edge IDs in `relationship-graph-edges*.csv` (ER = this batch) |
| `notes` | Caveats and inferences ([I]) |

Edges file `relationship-graph-edges-additions-18.csv` uses the columns of `relationship-graph-edges.csv`. Proposals file `queue-proposals-batch33c.csv` follows `queue-proposals-README.md`.

## Validation corrections (wave 18, 2026-11-15) — governing
Source: [validation-wave18-report.md](validation-wave18-report.md); register `data/mission-2026-11-14/validation-register-wave18.csv`.

1. **§0, Q-B05 / Q-N08 row (Goldman).**
   - **Find:** "**Goldman:** no 2021+ program document found. The newest public GSPF circular is dated **2017-12-05**, not 2008 as the repo states. It shows Ayco selecting the ETF options for a 50 bp fee. The live stack is unchanged: Ren iPhi donor web, Ayco admin, Goldman.com SSO. A new two-hop inference: GS Gives grant administration runs through CAF America, a Bonterra customer. | High (EJ text); GS stays "insufficient evidence" |"
   - **Replace with:** "**Goldman:** a 2021+ program circular exists. FireAid's Sept 2025 investigative report reproduces the GS DAF Program Circular as Appendix B, with ETF expense ratios as of 2024-09-30 (batch 30; V15-09; re-confirmed wave 18). It sets a $20,000 minimum and $100 grants paid by check or wire, and the ETF option is selected by Goldman Sachs Wealth Services, L.P. (up to 50 bps). The 2017 and 2008 circulars on gspf.goldman.com are dated context only. Live stack: Ren iPhi donor web, Ayco/GS Wealth Services administration, Goldman.com SSO. A new two-hop inference: GS Gives grant administration runs through CAF America, a Bonterra customer. | High (EJ text; GS circular). GS PF's 'insufficient evidence' premise (no 2021+ source) no longer holds; re-scoring is for the quadrant agent [V wave 18] |"
2. **§0, Edward Jones bullet.**
   - **Find:** "- Edward Jones' 2024 report gives the program as \"nearly $535 million\" assets under care and \">$90 million\" granted in 2023."
   - **Replace with:** "- Edward Jones' 2024 report says \"nearly $535 million\" invested by clients in the program and \">$90 million\" granted in 2023. One page calls the $535m \"assets under care\" in 2023; another says \"since inception\", so it may be cumulative investment rather than year-end assets [V wave 18]."
3. **§4.1, "What changed" second bullet.**
   - **Find:** "  - The program has a first-party size of about $535m (2023) (ER015)."
   - **Replace with:** "  - The program has a first-party size of \"nearly $535 million\" invested by clients (described both as 2023 assets under care and as \"since inception\"), with more than $90m granted in 2023 (ER015) [V wave 18]."
4. **§4.2, first bullet.**
   - **Find:** "- **No 2021+ program circular, donor guide or terms were found.**"
   - **Replace with:** "- **A 2021+ program circular exists, but not on Goldman's own public pages.** FireAid's investigative report ([PDF](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf), Appendix B) reproduces the GS DAF Program Circular, with ETF expense ratios \"in effect as of September 30, 2024\": $20,000 minimum, $100 minimum grant, payment \"in the form of a check or wire transfer\", admin fee 0.60% down to 0.03%, and ETFs selected by Goldman Sachs Wealth Services, L.P. (batch 30; V15-09; V18-01). No Goldman-hosted 2021+ circular was found."
5. **§4.2, second bullet lead-in.**
   - **Find:** "- **The newest public circular is dated 2017-12-05**, served from the donor-web domain"
   - **Replace with:** "- **The newest circular on Goldman's own domain is dated 2017-12-05** (dated context only, superseded by the FireAid-reproduced circular above; gspf.goldman.com's robots.txt disallows non-search crawlers, so it was not re-fetched in wave 18), served from the donor-web domain"
6. **§4.2, Quadrant status bullet.**
   - **Find:** "- **Quadrant status:** GS PF stays \"insufficient evidence\". The 2017 circular is pre-2021 and cannot score 2026 criteria under the bounded-truth rule."
   - **Replace with:** "- **Quadrant status:** the 2017 circular cannot score 2026 criteria, but the FireAid-reproduced circular (ratios as of 2024-09-30) is admissible 2021+ evidence for payment rail (check or wire) and terms. Caveats: it is undated, hosted by a third party, and the login page binds to an unversioned circular. Whether GS PF leaves \"insufficient evidence\" is for the quadrant agent [V wave 18]."
7. **§5, item 1.**
   - **Find:** "replace with \"The newest public Program Circular is dated 2017-12-05 ([PDF](https://gspf.goldman.com/gspf/Portals/29/docs/2017.11%20GSPF%20Program%20Circular.pdf)); a 2008 version and an undated v6 are also served. All are pre-2021.\""
   - **Replace with:** "superseded by wave 18: see the governing text for `queue-bank-programs-and-eft-providers.md` in `validation-wave18-report.md` (newest known circular = FireAid App. B, ratios as of 2024-09-30; Goldman-hosted 2008, v6 and 2017 versions are dated context)."
8. **§5, item 3.**
   - **Find:** "Edward Jones' own figure for 2023 is \"nearly $535 million\" assets under care (ER015)."
   - **Replace with:** "Edward Jones' own figure is \"nearly $535 million\" invested by clients (worded both as 2023 assets under care and as since inception) (ER015) [V wave 18]."
9. **§1.2, item 2 (PPGF label).**
   - **Find:** "PPGF FY2024: 694,979 DAF accounts, $626.6m grants ([DAFRC FY2024 row](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv)) [X]."
   - **Replace with:** "PPGF FY2024: 694,979 DAF accounts, $626.6m grants ([DAFRC FY2024 row](../../data/mission-2026-11-14/dafrc-sponsor-schedule-d-fy2019-2024.csv); DAFRC-imputed values, not a filed 990) [V wave 18]."
10. **§2.2, pass-through total.**
    - **Find:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC)."
    - **Replace with:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC; PPGF's $626.6m and NFG's $427.9m are imputed) [V wave 18]."
11. **§3.2 table, NCF row.**
    - **Find:** "| Salesforce captive portal (Stellar component behind it; GL inferred NetSuite) | NCF $5.46bn |"
    - **Replace with:** "| Salesforce captive portal (Stellar component behind it; GL inferred NetSuite) | NCF $5.46bn (DAFRC-imputed FY2024 value; The Signatry's $0.40bn is also imputed) [V wave 18] |"

## Validation corrections (wave 19, 2026-11-15) — governing
Source: [validation-wave19-report.md](validation-wave19-report.md); register `data/mission-2026-11-14/validation-register-wave19.csv`.

Batch 34 supersedes wave-18 correction 10 for this sentence. Apply this item instead of that one. Item 1's find text also appears in the file's own quoted correction list; apply it to the §2.2 body occurrence only.
1. **§2.2, pass-through total.**
   - **Find:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants (DAFRC)."
   - **Replace with:** "  Those five sponsors made about $4.4bn of FY2024 DAF grants as DAFRC publishes them, or **$4.32bn on filed returns** (PPGF $795.7m filed vs $626.6m imputed; NFG $199.8m filed vs $427.9m imputed; both already applied as R1 in the corrected totals). In the latest filed years they made $3.87bn in the DAF column, or $4.85bn with the AOGF and CAF America other-funds columns (batch 34B §1.1) [V wave 19]."
2. **§2.2, pass-through list, Bonterra line.**
   - **Find:** "  - Bonterra → NFG and CAF America (customer)"
   - **Replace with:** "  - Bonterra → NFG and CAF America (both vendor/customer links: Bonterra Tech $2.49m from NFG CY2024; CyberGrants $8.29m from CAF America FYE 2025-04). NFG has been controlled since 2024-06-07 by its sole member, Durable Capital for Sustainable Outcomes Inc. [batch 34B; V wave 19]"
