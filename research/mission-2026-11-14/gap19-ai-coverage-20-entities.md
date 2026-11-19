# AI coverage for the 20 entities with an empty `ai` cell (P-G02-01)

Date: 2026-11-19. Queue item P-G02-01 ([queue-proposals-g02.csv](../../data/mission-2026-11-14/queue-proposals-g02.csv)).
Input: [coverage-matrix-entities-2026-11-19.csv](../../data/mission-2026-11-14/coverage-matrix-entities-2026-11-19.csv), `checklist_item=ai`, status NI.
Outputs:
- [`ai-coverage-20-entities-2026-11-19.csv`](../../data/mission-2026-11-14/ai-coverage-20-entities-2026-11-19.csv): one row per entity, with columns that can update the matrix. All rows are `validated=no`.
- [`queue-proposals-g02a.csv`](../../data/mission-2026-11-14/queue-proposals-g02a.csv): three proposals.

## 1. Method

- **Pages read.** For each entity I read first-party pages: the privacy policy and terms (looking for AI or automated-decision wording), the homepage or DAF program page, the careers page, press releases from 2024 to 2026, and SEC filings where a filer's own investor-relations host serves them. I also used web search to find first-party pages, and labelled anything known only from search **[R]**.
- **Full-text scans.** Where a site is small enough, I scanned every page in its sitemap for AI terms: Charityvest guide (62 pages), RCF (34), AEF engage (54), aefonline.org (211) and svcf.org (319). The terms were AI, artificial intelligence, machine learning, generative, GenAI, LLM, large language model, chatbot, ChatGPT, OpenAI, Copilot, agentic and automated decision.
- **Robots.** I read robots.txt before fetching any page on a host, and fetched nothing from a host whose robots.txt could not be read (non-200 or HTML). I did not change the user-agent to get past a server that refused this client. No logins, forms or outreach.
- **Reuse.** I did not re-fetch what the repo already has:
  - [direction-ai-product-census.md](direction-ai-product-census.md) and its wave-28 corrections: AIP01 TIFIN Louise, AIP04 Fidelity Virtual Assistant, AIP08 Ren and AIP09 Foundation Source.
  - [direction-news-hiring-signals.md](direction-news-hiring-signals.md): Schwab and NPT careers not collected.
  - [gap19-second-source-pass.md](gap19-second-source-pass.md) C05: NPT terms and grant review.
  - [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md): NCF, SVCF, Charityvest and RCF terms.
- **Classification.** I used the AI overlay of [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §7 (GREEN, AMBER, RED) plus the census's local labels ("None evidenced", "None (inform-only)", "None (watch)", "AMBER (low)"). Per wave 28, those sub-labels are local to the census.
- **Entity scope rule (§7).** AI at a parent firm, owner or vendor is recorded but is **not** counted as AI at the DAF program unless a source ties it to that program.
- **Status codes.**
  - **EC** means evidence collected. That covers an AI finding and also a documented absence, where first-party pages were read and showed none.
  - **DS** means discovery started: search only, because first-party pages could not be read under the rules above.
  - **IP** (insufficient public information) is not used. Blocked reading is not the same as information being absent.

## 2. Results

| Status | Count | Entities |
|---|---|---|
| EC: AI capability or claim found | 4 | NCF (AI site search), SEI (corporate agentic AI; TIFIN named), Pave (self-described AI platform), Give Interactive ("AI tools" integration) |
| EC: AI policy only | 1 | NPT (ban on using site or user data to train AI) |
| EC: parent-level AI only, none at the program | 3 | Morgan Stanley GIFT, BofA CGF, Edward Jones |
| EC: documented absence | 5 | AEF, RCF, SVCF, Charityvest, DAF Direct |
| DS: first-party pages blocked | 7 | DAFgiving360, Goldman Sachs, JCF, Stellar/iPhi, NPact, TIAA, OneAscent |

**Key findings**
1. **No entity documents AI in grant approval, eligibility or any money-moving action.** No overlay above AMBER (low) applies at program level. This extends the "no sponsor-side AI in approval" absence finding (report §7; gap19 C05) to 13 more entities. It is still an absence finding.
2. **NCF is the one sponsor with a live AI feature for donors:** an "AI search" over its own content.
   - The page is described as "Explore trusted NCF resources through an AI-powered search experience". Its embedded record is dated 2026-08-12.
   - No account access or money movement is evidenced. The vendor, model and controls are undocumented.
   - Overlay: **AMBER (low)**, on the boundary with None (inform-only).
3. **SEI is the entity closest to agentic AI in the DAF chain.**
   - The SEI Charitable Fund (2026-10-28) runs on TIFIN Give, whose Louise is AMBER (RED-boundary) (AIP01). The release does not say Louise is offered to SEI donors (proposal P-G02A-01).
   - Separately, SEI's CTO describes "our partnership with IBM Consulting to help us define and deploy the agents that will enable our operational workforce". That is corporate operations, not the DAF.
4. **AI at wealth-channel parents is advisor-facing and sits outside the DAF:**
   - Morgan Stanley Debrief (2024-06-26)
   - BofA Erica and Merrill tools [R]
   - Goldman GS AI Assistant (2025) [R]
   - Edward Jones' AI retirement-plan tool, planned "beginning in 2027"

   None is tied to the DAF program. Morgan Stanley's is the only one with a documented human step: the advisor edits the email and sends it "at their discretion".
5. **AI policies are mostly prohibitions or privacy-law rights.** NPT bans AI training on its site and user data. The privacy policies of AEF, Give Interactive, SEI and Pave list automated-decision rights. None says the organisation uses automated decisions.

## 3. Per-entity table

Accessed 2026-11-19 unless stated. Source IDs refer to §4.

| Entity | Status | Finding | Overlay | Pages checked (source IDs) |
|---|---|---|---|---|
| AEF | EC | None found. The privacy policy (last updated March 2024) lists the right "not to be subject to a decision based solely on automated processing, including profiling" but makes no use statement. The careers page and homepage have no AI terms. The full-text scan of 265 pages found one hit, a false positive (a guest author's "LLM" law degree). | None evidenced | S01–S03 |
| NPT | EC | AI policy only. The terms (last updated 2026-10-29) prohibit "using the Site Content or any user data for the development of any software program, model, algorithm or generative artificial intelligence ('AI') tool". A CIO article (2025-02-06) says NPT's IT and cybersecurity teams are "continually focused on monitoring … how AI developments are affecting various tech environments", which is monitoring, not deployment. The careers page has no AI terms. Grant review has no AI (gap19 C05). | None evidenced | S04–S06 |
| RCF | EC | None found. Privacy policy revised 2021-12-15; 34 of 34 sitemap pages have 0 AI terms. The administrator, Ren, also has none (AIP08). | None evidenced | S07–S08 |
| DAFgiving360 | DS | robots.txt on dafgiving360.org and aboutschwab.com returns 403, so nothing was fetched. Search shows no DAFgiving360 AI claim. Schwab's AI strategy appears only in secondary press and is out of scope. | None evidenced (unverified) | S09 |
| Morgan Stanley GIFT | EC | The GIFT page has AI terms only in site navigation. At parent level, "AI @ Morgan Stanley Debrief is an OpenAI-powered tool that, with client consent, generates notes", and drafts "an email for an Advisor to edit and send at their discretion" (2024-06-26). A Firmwide AI team page also exists. | None evidenced (program) | S10–S12 |
| Goldman Sachs | DS | gspf.goldman.com disallows robots (earlier audit). The goldmansachs.com homepage has no AI terms. The GS AI Assistant firmwide launch (June 2025) appears in secondary press only. The 10-K was not read. | None evidenced (unverified) | S13–S14 |
| BofA CGF | EC | The CGF overview has no AI. The 10-K for FY2025 (filed 2026-02-25, BofA IR host) mentions AI only as evolving "AI-related" laws, rules and regulations, and does not mention the CGF or Erica. Newsroom releases on Erica (2025-08-20) and Merrill's "AI-Powered Meeting Journey" (2026-03-26) are [R]: the pages redirect for a script client. | None evidenced (program) | S15–S17 |
| NCF | EC | An "AI search" page is live and linked from the Resources menu. Its record is dated 2026-08-12 and its embedded status field reads "private". The search snippet says "AI will search our site" [R]. The privacy policy and careers page have no AI terms. The Program Agreement bars third-party services and scraping (repo). | AMBER (low) | S18–S20 |
| JCF | DS | robots.txt allows fetching, but every page returns a 403 bot challenge. Search shows no JCF AI claim. | None evidenced (unverified) | S21 |
| SVCF | EC | None found. Privacy policy revised 2024-11-18; terms updated 2024-04-22. The full-text scan of 319 pages found AI only as a topic: grantee and donor stories (e.g. the Cadence Fem.AI initiative), a board Q&A, and the appointment of OpenAI's vice president of global policy, Ann O'Leary, to SVCF's board (2026). None describes SVCF using AI. | None evidenced | S22–S24 |
| Charityvest | EC | None found. 62 of 62 help-centre pages have 0 AI terms. The charityvest.org terms and privacy pages are script-rendered and returned no text. Search shows no claim. The owner, Foundation Source, has an AI roadmap (AIP09), which is out of scope here. | None evidenced | S25–S26 |
| Stellar / iPhi | DS | robots.txt disallows all paths on iphiview.com and stellartechsol.com. Search shows no claim. The owner, Ren, has none (AIP08). | None evidenced (unverified) | S27 |
| Give Interactive | EC | The homepage says the platform is "interconnected to top tools across the space including Sage Intacct, Salesforce, PowerBI, … Intercom, AI tools, etc.". No AI product is described. The privacy policy (effective 2025-04-01) lists a state-law right to opt out of automated decision-making. | None (watch) | S28–S29 |
| NPact | DS | npact.com refused this client: robots.txt allows all, but the connection was dropped or reset. The help-centre host loops on redirects. Search shows no AI claim (the 2022 FIMS/DonorCentral acquisition only). | None evidenced (unverified) | S30 |
| DAF Direct | EC | None found on the homepage, the About page or the privacy policy. The site is Fidelity-run (DAFDirect@fmr.com). | None evidenced | S31–S33 |
| Edward Jones | EC | No AI on the DAF page or the US state privacy notice (2025-09-26). At firm level: an "AI-powered solution for workplace retirement plan management beginning in 2027" (2026-09-30), Edward Jones Ventures "investing in AI-powered financial planning tools" (2026-02-03), and Morning Consult research on advisors' AI use (2026). The DAF sponsor is RCF (none found). | None evidenced (program) | S34–S38 |
| TIAA | DS | tiaa.org robots.txt timed out on 2026-11-19 (two retries). The TIAA gAIt launch (2024-07-17) is [R]. The platform is Charityvest (none found). | None evidenced (unverified) | S39 |
| OneAscent | DS | oneascent.com robots.txt could not be read. Search shows no OneGive AI claim. The platform is Charityvest. | None evidenced (unverified) | S40 |
| SEI | EC | The SEI Charitable Fund release (2026-10-28) mentions AI only in TIFIN's boilerplate: "a platform of products and companies that apply AI for financial services". At corporate level: an investment-manager AI release (2026-06-16) with "accuracy, control, and human oversight"; IBM agentic-AI work "with SEI's Investment Managers business"; and a CTO post (2026-05-19) on deploying agents for the operational workforce. The privacy notice lists automated-decision rights. | None evidenced (program); vendor AIP01 is AMBER (RED-boundary) | S41–S44 |
| Pave Finance | EC | Pave calls itself "the leading AI-powered portfolio management platform for financial advisors" (Series A, 2026-09-14). The homepage and capabilities pages have no AI terms. The privacy policy (effective 2026-02-13) mentions "predictive modeling for marketing" and an ADMT opt-out. No DAF product with AI is described. | None (watch) | S45–S48 |

**Hiring.** No new ATS feeds were scanned. The repo's 2026-11-15 snapshot covers none of these 20 entities. Schwab was blocked by robots and NPT has no careers board ([news-hiring](direction-news-hiring-signals.md)). On the careers pages read here, AEF, NPT, NCF and Pave list no AI, ML or LLM titles; Pave's engineering department page listed no roles.

## 4. Source register

| ID | Source | Date | URL |
|---|---|---|---|
| S01 | AEF privacy policy | last updated March 2024 | https://www.aefonline.org/data-protection-privacy-policy/ |
| S02 | AEF careers; homepage | accessed 2026-11-19 | https://www.aefonline.org/careers/ ; https://www.aefonline.org/ |
| S03 | AEF full-text scans (engage.aefonline.org, 54 pages; aefonline.org sitemap) | accessed 2026-11-19 | https://engage.aefonline.org/wp-sitemap.xml ; https://www.aefonline.org/sitemap_index.xml |
| S04 | NPT Privacy Policy & Terms of Use | 2026-10-29 | https://www.nptrust.org/privacy-policy/ |
| S05 | NPT, "AI, Disinformation & Due Diligence in Philanthropy 2025" (C. Adams, CIO) | 2025-02-06 | https://www.nptrust.org/philanthropic-resources/philanthropist/due-diligence-disinformation-ai-and-the-charitable-landscape-in-2025/ |
| S06 | NPT job listings | accessed 2026-11-19 | https://www.nptrust.org/contact-us/careers/ |
| S07 | RCF privacy policy | rev. 2021-12-15 | https://renaissancecharitable.org/privacy-policy/ |
| S08 | RCF full-text scan (34 pages) | accessed 2026-11-19 | https://renaissancecharitable.org/sitemap_index.xml |
| S09 | DAFgiving360 / aboutschwab.com robots.txt (403) | 2026-11-19 | https://www.dafgiving360.org/robots.txt |
| S10 | Morgan Stanley GIFT program page | accessed 2026-11-19 | https://www.morganstanley.com/what-we-do/wealth-management/gift |
| S11 | Morgan Stanley, Launch of AI @ Morgan Stanley Debrief | 2024-06-26 | https://www.morganstanley.com/press-releases/ai-at-morgan-stanley-debrief-launch |
| S12 | Morgan Stanley, Firmwide AI team | accessed 2026-11-19 | https://www.morganstanley.com/about-us/technology/artificial-intelligence-firmwide-team |
| S13 | Goldman Sachs homepage | accessed 2026-11-19 | https://www.goldmansachs.com/ |
| S14 | Fox Business, Goldman firmwide AI assistant [R, secondary] | 2025-06 | https://www.foxbusiness.com/technology/goldman-sachs-announces-firmwide-launch-ai-assistant |
| S15 | BofA Charitable Gift Fund overview | accessed 2026-11-19 | https://www.bankofamerica.com/philanthropic/gift-fund-overview/ |
| S16 | BofA Form 10-K FY2025 | filed 2026-02-25 | https://investor.bankofamerica.com/regulatory-and-other-filings/select-sec-filings/content/0000070858-26-000157/bac-20251231.htm |
| S17 | BofA newsroom: Erica 3bn interactions; Merrill AI-Powered Meeting Journey [R] | 2025-08-20; 2026-03-26 | https://newsroom.bankofamerica.com/content/newsroom/press-releases/2025/08/a-decade-of-ai-innovation--bofa-s-virtual-assistant-erica-surpas.html ; https://newsroom.bankofamerica.com/content/newsroom/press-releases/2026/03/merrill-and-bank-of-america-private-bank-launch-ai-powered-meeti.html |
| S18 | NCF AI search | record 2026-08-12 | https://www.ncfgiving.com/ai-search |
| S19 | NCF privacy policy | accessed 2026-11-19 | https://www.ncfgiving.com/privacy-policy/ |
| S20 | NCF careers | accessed 2026-11-19 | https://www.ncfgiving.com/careers/ |
| S21 | JCF homepage and privacy (403 challenge) | 2026-11-19 | https://jcfny.org/ |
| S22 | SVCF privacy policy | rev. 2024-11-18 | https://www.svcf.org/privacy-policy |
| S23 | SVCF terms of use | 2024-04-22 | https://www.svcf.org/terms-of-use |
| S24 | SVCF homepage and full-text scan (319 pages); board appointment release | accessed 2026-11-19 | https://www.svcf.org/ ; https://www.svcf.org/sitemaps-1-sitemap.xml ; https://www.svcf.org/about/news-media/press-releases/silicon-valley-community-foundation-welcomes-ann-oleary-and-kate-mitchell-to-board-of-directors |
| S25 | Charityvest Guide, full-text scan (62 pages) | accessed 2026-11-19 | https://guide.charityvest.org/ |
| S26 | Charityvest terms and privacy (script-rendered, no text) | accessed 2026-11-19 | https://www.charityvest.org/terms-of-use ; https://www.charityvest.org/privacy-policy |
| S27 | iPhi / Stellar robots.txt (disallow) | 2026-11-19 | https://www.iphiview.com/robots.txt ; https://www.stellartechsol.com/robots.txt |
| S28 | Give Interactive homepage | accessed 2026-11-19 | https://www.giveinteractive.com/ |
| S29 | Give Interactive privacy policy | effective 2025-04-01 | https://www.giveinteractive.com/privacy-policy |
| S30 | NPact (connection refused); help-centre host (redirect loop) | 2026-11-19 | https://npact.com/ ; https://npact.document360.io/ |
| S31 | DAF Direct homepage | accessed 2026-11-19 | https://www.dafdirect.org/ |
| S32 | DAF Direct About | accessed 2026-11-19 | https://www.dafdirect.org/about-daf-direct/index.html |
| S33 | DAF Direct privacy policy | accessed 2026-11-19 | https://www.dafdirect.org/privacyPolicy.html |
| S34 | Edward Jones DAF page | accessed 2026-11-19 | https://www.edwardjones.com/us-en/investment-services/investment-products/donor-advised-funds |
| S35 | Edward Jones US state privacy notice | 2025-09-26 | https://www.edwardjones.com/us-en/privacy/us-state-privacy-notice |
| S36 | Edward Jones, retirement plan management tech release | 2026-09-30 | https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/kicks-retirement-plan |
| S37 | Edward Jones Ventures AI investments release | 2026-02-03 | https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/edward-jones-ventures-invests-ai-driven-solutions-help-families-navigate-lifes-biggest-financial |
| S38 | Edward Jones / Morning Consult AI research release | 2026 (exact date not parsed) | https://www.edwardjones.com/us-en/why-edward-jones/news-media/press-releases/ai-future-financial-advisor-research-2026 |
| S39 | TIAA gAIt launch [R; tiaa.org robots.txt timed out] | 2024-07-17 | https://www.tiaa.org/public/about-tiaa/news-press/news/2024/07-17 |
| S40 | OneAscent (robots.txt unreadable) | 2026-11-19 | https://www.oneascent.com/ |
| S41 | SEI launches SEI Charitable Fund | 2026-10-28 | https://www.seic.com/about-sei/newsroom/sei-launches-sei-charitable-fund-bringing-charitable-giving-advisor-and-client-wealth-experience |
| S42 | SEI Introduces Technology and AI to Boost Investment Manager Efficiency | 2026-06-16 | https://www.seic.com/about-sei/newsroom/sei-introduces-technology-and-ai-boost-investment-manager-efficiency |
| S43 | SEI CTO, "From individual to enterprise: What IBM Think reinforced about AI at scale" | 2026-05-19 | https://www.seic.com/about-sei/thought-leadership/individual-enterprise-what-ibm-think-reinforced-about-ai-scale |
| S44 | SEI privacy notice | accessed 2026-11-19 | https://www.seic.com/ent/privacy-notice |
| S45 | Pave Finance announces Series A | 2026-09-14 | https://www.pavefinance.com/newsletter/series-a |
| S46 | Pave homepage; capabilities | accessed 2026-11-19 | https://www.pavefinance.com/ ; https://www.pavefinance.com/capabilities |
| S47 | Pave privacy policy | effective 2026-02-13 | https://www.pavefinance.com/privacy-policy |
| S48 | Pave careers | accessed 2026-11-19 | https://www.pavefinance.com/careers |

## 5. Limits

- **Absence is not proof.** Sponsors rarely announce internal AI used in operations, and a page can omit AI the organisation uses ([census](direction-ai-product-census.md): "Absence of a control statement is not evidence that the control is absent").
- **Script-rendered pages.** Charityvest's site, Edward Jones pages and BofA's newsroom returned little or no static text. I used the meta descriptions or treated the text as search-index only.
- **Not checked.** SEC EDGAR full-text search was not run, because EDGAR asks automated clients for contact details. Only BofA's 10-K was read, from its own IR host.
- **Domain confusion.** The `pave.finance` domain redirects to an unrelated company (pavefi.com, SMB lending). That company's AI pages were excluded.
- **Validation.** All rows are `validated=no`, pending the separate validation register.
