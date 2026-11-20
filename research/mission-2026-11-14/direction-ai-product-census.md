# AI products shipped by philanthropy-technology vendors, 2025–2026 (P-NEW-AIP-01)

**Date:** 2026-11-15. Prepared by the batch 43 N25 agent. Files only: no commit, no push.

**Data:** [`data/mission-2026-11-14/philanthropy-ai-products-2026.csv`](../../data/mission-2026-11-14/philanthropy-ai-products-2026.csv) (30 rows, one per product or product bundle). **Queue proposals:** [`queue-proposals-batch43-n25.csv`](../../data/mission-2026-11-14/queue-proposals-batch43-n25.csv).

**Read first (governing corrections applied):**
- [ai-governance-failure-modes.md](ai-governance-failure-modes.md). Its rule is "AI may add a flag, never clear one". Red-team correction 17 applies: its risk counts are rubric ratings, not observed incidents.
- [direction-news-hiring-signals.md](direction-news-hiring-signals.md), with the wave 24B corrections. The two TIFIN AI roles are group roles, not TIFIN Give roles. Hiring shows intent, not deployment.
- [queue-batch36-agent-terms-controls.md](queue-batch36-agent-terms-controls.md), with the wave 21 and 22 corrections:
  - Endaoment's T&C bars sharing credentials.
  - Endaoment documents two third-party tracks: a registered OAuth client and a Partner API.
  - Benevity's overlay is AMBER (provisional).
- Overlay vocabulary: [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §7. The "None" labels follow [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md) §6.

**Method and compliance:**
- Desk research only. No accounts, logins, trials, form submissions, outreach or keyed API calls.
- Recency rule: 2025–2026 sources for current products. Items dated earlier are marked as context.
- robots.txt was read on every host before fetching. A 200 response was parsed for ClaudeBot, Claude-User, anthropic-ai, Claude-Web and `*`. A 404 means no rules, the repo convention. A 401 or 403 means unreadable, and the host was not fetched.
  - **Not fetched because robots.txt was unreadable (403):** candid.org, www.businesswire.com, investor.blackbaud.com and blackbaud.gcs-web.com.
  - **Not fetched because robots.txt disallows ClaudeBot and anthropic-ai:** www.foundant.com and www.citybiz.co.
  - **No robots.txt (404):** www.donorsearch.net, docs.daffy.org, tifin.com, webfiles-sc1.blackbaud.com and www.financialcontent.com. These were fetched where needed.
- **Pages that returned an error and were not retried by other means:**
  - 403: submittable.com/features/automated-review, the Submittable responsible-AI blog and the StreetInsider Fluxx release.
  - 404: the TIFIN Louise news page and two Endaoment release-note pages.
  - Too many redirects: the Foundant Fia release mirror.
  - Their content appears only as search-index text tagged **[R]**, or as evidence already in the repo.
- Tags: **[F]** primary page read on 2026-11-15, or read by an earlier batch and cited; **[R]** search-index snippet only; **[I]** inference.

---

## 1. Findings in brief

1. **Thirty products from 22 vendors were catalogued.** Overlay counts:

   | Overlay | Rows |
   |---|---|
   | GREEN (provisional) | 3 [V wave 42A] |
   | AMBER | 10 [V wave 42A] |
   | AMBER (low) | 9 |
   | AMBER (RED-boundary) | 1 |
   | AMBER (GREEN-boundary) | 1 |
   | AMBER (unverified) | 1 |
   | None | 5 |
   | RED | **0** |

   No product meets the §7 RED test: an AI that completes a money-moving or status-clearing action with no documented sponsor or human approval.
2. **Only two products can move DAF money through AI, and both are donor-side with sponsor approval downstream.**
   - TIFIN Louise claims to "execute real donor requests". Its examples are a recurring $100 grant, a contribution of 100 NVDA shares and adding a child to the DAF. No limit, confirmation or audit control is published. GiveClear reviews grants "within 48 hours of submission" ([release](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [guidelines](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines)).
   - Daffy's MCP server exposes `make_donation` ("Moves real money") and `cancel_donation` ("Permanent"). It documents no per-donation confirmation or cap. Assistant activity "shows up in the Daffy app" ([docs](https://docs.daffy.org/agents/mcp)).
   - Both keep their existing AMBER calls: TIFIN at the RED boundary, Daffy plain AMBER. This census adds nothing that moves either call.
3. **The large DAF platforms and sponsors ship no generative or agentic AI.**
   - Ren's giving-platform page uses no AI terms ([Ren](https://www.reninc.com/giving-platform/)). Givinga's homepage says only "Automate compliance, charity vetting, and tax documentation" ([Givinga](https://givinga.com/)). Foundation Source's homepage has no AI terms.
   - Fidelity Charitable's Virtual Assistant is an "automated natural language search engine" that asks users not to enter account information ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)).
   - Foundation Source's CEO (2026-10-28) says AI is used internally "as a development tool". He says the firm is "working toward embedding AI into the products", with a roadmap tool that would "surface the strongest candidates for review" among scholarship applicants ([interview](https://pulse2.com/foundation-source-profile-joe-mrak-interview/)). This is the first public sponsor-platform roadmap item that puts AI in **applicant screening**. It is framed as a flag for review.
   - Endaoment has no AI product. Its blog index lists an "AI & Discoverability" release-note section (2026-04) and an "Assistant guide": "A public description of Endaoment is available for assistants to read" (2026-10-28) [R; pages 404].
4. **Grantmaking software has the best-documented controls. These are the first GREEN-eligible readings of vendor AI products in the repo, marked provisional. None is the first GREEN under §7: none is an A1–A5 provider, and v1.0 calibration had already labelled Fidelity Charitable GREEN and Ren/RCF/AEF “GREEN / none” before v1.1 withdrew both [V wave 42A]**
   - **SmartSimple AI Application Analysis.** Results are "inputs to reviewer judgment and not as final determinations". It "does not send grant application data to external AI services", and data "is never used to train AI models". Admins choose which fields are analysed. It is a paid add-on ([help](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview)).
   - **Fluxx Finn.** It is off by default, with an organisation-level opt-in. Customer data is "never used to train" any AI model. It "keeps humans in the loop". Pricing is "1 credit per dollar" in credit bundles ([Fluxx AI](https://fluxx.io/ai-grants-management-software)).
   - **YourCause / Blackbaud Grantmaking AI Application Summaries and Form Intelligence.** These are complimentary once the customer opts in. The Blackbaud-wide default is not universal: organisations that “used generative AI before January 7, 2026” stay enabled, and enabling generative AI also enables “external connectors access to your data” unless an admin clears that box. GrantsConnect summaries still have to be switched on by Blackbaud (“Contact your Account Manager or CSM to enable it”). [V wave 42A] "Final evaluation and decision-making" stays "with the grants team" ([YourCause](https://www.yourcause.com/?p=12324)). Blackbaud's global generative-AI switch is off by default, and the FAQ says Blackbaud does not use customer data "to retrain or improve the underlying model" ([opt-in help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html)).
   - [I] None of these sits in a DAF grant's money path. Under the entity scope rule (§7), they do not change any sponsor's overlay. SmartSimple's own FAQ says the Application Analysis service takes data “from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)”, so it is a Foundant-wide service, but no source shows it in use in a community foundation's DAF workflow. The Foundant overlay stays AMBER because Fia's agents and policy engine have undocumented limits, and §7 has no rule for rating a provider from one GREEN component [V wave 42A]
5. **Fundraising CRM AI acts on outreach, not on money.**
   - **Blackbaud's Development Agent** "autonomously" runs email and SMS outreach. It claims "human oversight through visibility and escalation" and says "every interaction is logged in real time". Per-message approval is not stated, and pricing is not published ([product](https://www.blackbaud.com/products/blackbaud-development-agent)).
   - **Bloomerang Penny** (beta, 2026-03-31) lets fundraisers "launch campaigns, assign follow-ups, and create donor segments". The only control statement is "built-in guardrails" ([news](https://bloomerang.com/news/bloomerang-penny-ai-fundraising-strategist-nonprofits)).
   - **Bonterra Que.** The first-party principle is "People always make the final decisions" ([blog](https://www.bonterratech.com/blog/meet-bonterra-que)). The per-action rule that it does not send an email, save a record or submit a form without staff approval appears only in a press release this agent could not read [R].
   - **Salesforce Agentforce Nonprofit** (2025-12-02) launched four agents, including Donor Support self-service (beta in spring, GA in summer 2026). The launch post addresses no human-approval, audit or training controls. It offers 10 free licences under Power of Us ([Salesforce](https://www.salesforce.com/news/stories/agentforce-nonprofit-announcement/)).
   - **Givebutter Magic** (2026-10-01) is AMBER, not GREEN. Its stretch goals “automatically increase as you raise more” and its suggested amounts are “automatically matched”, so the AI is not flag-only, and its privacy policy says AI tools “review transactions, detect fraud, and assess risk” with undocumented limits. Its AI Addendum (effective 2026-10-01) also says “AI Features are enabled by default”, that AI-assisted fraud detection and Receipt Matching “cannot be disabled”, and that data captured by third-party AI infrastructure services “may be used for AI model training”. [V wave 42A] It says "nothing gets sent or published without your approval" and "Givebutter Magic does not process payments", and its connectors "can't create, edit, or delete". Most features are free, and AI custom reports need Givebutter Plus "starts at $29/month" ([recap](https://givebutter.com/blog/the-spread-2026-recap); [Magic](https://givebutter.com/magic)).
6. **Charity-data providers ship search and recommendation features with no documented ranking controls.**
   - Charity Navigator's Horizon AI Search (2025-11-24) gives "instant, personalized recommendations" ([release](https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search)).
   - Candid's Claude connector (2025-12) and its 2026 fundraising assistant ("find funders, check eligibility, and draft LOIs") could not be read first-hand because candid.org's robots.txt returned 403 [R].
   - [I] Ranking and eligibility hints that reach donors before a grant recommendation is made are where failure mode F05/F09-type errors would surface. No vendor publishes how its rankings are produced.
7. **Pricing is rarely published.**
   - Published or partly published: Givebutter Plus ($29/month), Fluxx credits (unit only), Salesforce (10 free licences; regional list prices only), the Instrumentl connector (included on every plan), YourCause summaries (complimentary) and Chat for Blackbaud AI (included for all RE NXT customers; [R]).
   - Not published: Blackbaud Development Agent, SmartSimple (add-on), Bloomerang Penny, DonorSearch, TIFIN Louise and Foundant Fia.
8. **Named items not found.**
   - **"Blackbaud Copilot":** no product by that name. The nearest are Chat for Blackbaud AI and the Blackbaud agent for Microsoft 365 Copilot (2026-08-10 [R]).
   - **"Classy" AI:** Classy became GoFundMe Pro on 2025-05-06. Its AI features are personalised ask amounts and nudges, and the release cites "AI-powered fundraising features used more than 35 million times" across GoFundMe ([newsroom](https://www.gofundme.com/c/newsroom/40-billion-raised-launches-gofundme-pro)).
   - **AI products from Ren, Givinga or Foundation Source:** none shipped.

---

## 2. Census (summary; full fields in the CSV)

| ID | Vendor | Product | Launch | Function | Money-moving? | Status-changing? | Documented controls | Pricing | Overlay |
|---|---|---|---|---|---|---|---|---|---|
| AIP01 | TIFIN Give / GiveClear | Louise | 2025-10-27 | recommend; agentic | yes (claimed) | yes (claimed: add family member) | none for Louise; GiveClear 48-h review | no | **AMBER (RED-boundary)** |
| AIP02 | Daffy | MCP server | undated | search; agentic | yes | yes (cancel) | OAuth or key; key revocation; activity in app; no limits or agent ID | free | **AMBER** |
| AIP03 | Daffy | Quick Donate | 2025-04-09 | parse request | yes (recommendation) | no | not stated | no | AMBER (low) |
| AIP04 | Fidelity Charitable | Virtual Assistant | undated | site search | no | no | asks users not to enter personal data; disclaimer | n/a | None (inform-only) |
| AIP05 | Endaoment | none ("Assistant guide") | 2026-04 / 2026-10 [R] | discoverability | no AI path | no | n/a | n/a | None (watch) |
| AIP06 | Chariot | Gift Processing AI agent | 2026-01-28 | codes gifts | no | yes (nonprofit records) | not described | n/a | AMBER |
| AIP07 | Chariot | MCP server | undated | read/write records | not documented | yes (create, delete, merge; reconcile) | client confirmation; destructiveHint; donation activity log | free; needs paid plan | AMBER |
| AIP08 | Ren | none found | — | — | — | — | — | — | None evidenced |
| AIP09 | Foundation Source | roadmap only | (2026-10-28 interview) | planned screening | no | no | principle: "human judgment at the center" | — | None evidenced |
| AIP10 | Givinga | none found | — | — | — | — | — | — | None evidenced |
| AIP11 | Foundant | Fia | 2026-09-02 | knowledge base, agents, policy engine | not documented | not documented | claimed, not documented | no | AMBER |
| AIP12 | SmartSimple | AI Application Analysis | help article updated 2026-06-22 | score and flag | no | no | supplements review; no external AI; no training; field control | add-on | **GREEN (provisional)** |
| AIP13 | Fluxx | Finn | 2026-08-04 [R] | Q&A; draft; flag risks | no | no | opt-in, off by default; no training; field control; humans decide | credits | **GREEN (provisional)** |
| AIP14 | Fluxx | Fluxx MCP | undated | external-agent workflows | not documented | not documented | not documented | included with Finn | AMBER |
| AIP15 | Submittable | Automated Review | undated | review/score | no evidence | unknown | marketing only | not read | AMBER (unverified) |
| AIP16 | Blackbaud / YourCause | Application Summaries, Form Intelligence | 2026-07-16 | summarise | no | no | opt-in, off by default (organisations using generative AI before 2026-01-07 stay enabled; summaries enabled by Blackbaud on request); no retraining; humans decide [V wave 42A] | complimentary | **GREEN (provisional)** |
| AIP17 | Blackbaud | Development Agent | 2026-03-17 GA | autonomous outreach | no | no | visibility and escalation; real-time log | no | AMBER |
| AIP18 | Blackbaud | Chat for Blackbaud AI; M365 Copilot agent; Claude connector | 2025-12-02; 2026-08-10 [R] | chat, draft, insights | no | unclear | opt-in, off by default; AI role; no retraining | Chat included [R] | AMBER |
| AIP19 | Bonterra | Que | 2025-10-01 | draft; score; agentic | no | prepares only (R) | "People always make the final decisions"; per-action approval [R] | promo only | AMBER (GREEN-boundary) |
| AIP20 | Instrumentl | MCP connector | 2026 (June / 10-08) | tracker writes | no | yes (own tracker) | preview for expenses only; no training | included | AMBER (low) |
| AIP21 | Instrumentl | Apply (beta) | undated | drafting | no | no | not stated | not stated | AMBER (low) |
| AIP22 | Candid | Claude MCP connector | 2025-12-02 | read | no | no | read-only per a third party | free tier | AMBER (low) |
| AIP23 | Candid | AI assistant; fundraising assistant | 2025-01; 2026-08-31 [R] | Q&A; eligibility check; LOI draft | no | no | not read | not read | AMBER (low) |
| AIP24 | Salesforce | Agentforce Nonprofit (4 agents) | 2025-12-02 | research; self-service; scheduling | not stated | not stated | none in launch source | Power of Us: 10 free licences | AMBER |
| AIP25 | Bloomerang | Penny (beta) | 2026-03-31 | recommend; draft; act | no | yes (segments, tasks, campaigns) | "built-in guardrails" only | not stated | AMBER |
| AIP26 | Bloomerang | Conversational Reporting (alpha); Dataro | 2026-04-27 | reports; lists | no | creates lists | none | not stated | AMBER (low) |
| AIP27 | DonorSearch (EverTrue) | DonorSearch Ai; Enhanced CORE | not stated | predictive scores | no | no | none | demo only | AMBER (low) |
| AIP28 | Givebutter | Givebutter Magic | 2026-10-01 | draft; suggest; filter | no ("does not process payments") | limited (auto stretch goals) | approval before send or publish; read-only connectors; AI on by default; fraud and receipt AI cannot be disabled | free; Plus $29/month | **AMBER** [V wave 42A] |
| AIP29 | GoFundMe Pro (ex-Classy) | AI ask amounts and nudges | 2025-05-06 | recommend | no | no | not stated | not stated | AMBER (low) |
| AIP30 | Charity Navigator | Horizon AI Search | 2025-11-24 | search; recommend | not stated | no | not stated | not stated | AMBER (low) |

**How the overlay was applied [I]:**
- **RED** requires an AI path that completes a money-moving or status-clearing action with no documented sponsor or human approval. None qualifies.
  - The two money-moving paths (AIP01, AIP02) end in sponsor review.
  - Status-changing paths (Chariot, Instrumentl and Bloomerang record writes) act on the customer's own operational records, not on grant eligibility or approval states.
- **GREEN** requires documented controls, including a flag-only role and authority separation, on a first-party page. Three GREENs remain, all provisional; Givebutter Magic moved to AMBER [V wave 42A]:
  - each rests on a single first-party page read once, with no testing;
  - none is a DAF sponsor or rail;
  - they should be validated before any report text says "first GREEN" (P-B43N25-01). Validated 2026-11-20: SmartSimple, Fluxx Finn and YourCause hold as GREEN (provisional), and none is the first GREEN under §7 [V wave 42A]
- **"AMBER (low)"** marks read, search, scoring or drafting features with undocumented controls. **"AMBER (unverified)"** marks a row whose primary pages could not be read.
- The overlay vocabulary was written for DAF providers. Autonomous **outreach** (Blackbaud Development Agent, Bloomerang Penny) is neither money-moving nor status-clearing in the §7 sense. It is AMBER because limits are undocumented. Its risk is reputational and privacy-related (F09-type), not 4966/4967-type.

---

## 3. Controls matrix (what is documented, by control type)

| Control | Documented on a first-party page | Not documented, among products with actions |
|---|---|---|
| Human approval before action | Givebutter Magic; SmartSimple; YourCause; Fluxx Finn; Bonterra Que (principle only; per-action wording [R]); Chariot MCP (client-side) | TIFIN Louise; Daffy MCP (per donation); Bloomerang Penny; Salesforce Agentforce; Fluxx MCP; Foundant Fia |
| Sponsor approval downstream of AI | GiveClear 48-h review (AIP01); Daffy approval "at its sole discretion" (AIP02) | — |
| Audit or activity log | Blackbaud Development Agent ("every interaction is logged"); Daffy (activity in app; CSV statement); Chariot (donation activity log) | TIFIN Louise; Bloomerang; Salesforce; Fluxx MCP |
| Agent identity on transactions | none | Daffy (no agent field: AGM-10); TIFIN |
| Opt-in, off by default | Blackbaud (global generative-AI switch; organisations that used generative AI before 2026-01-07 stay enabled; GrantsConnect summaries enabled by Blackbaud); Fluxx Finn; SmartSimple (vendor must enable) | Bloomerang; Salesforce; Givebutter (AI on by default; fraud and receipt AI cannot be disabled) [V wave 42A] |
| No training on customer data | Blackbaud; Fluxx; SmartSimple; Instrumentl; Givebutter (third-party models; own models de-identified only; observability and fraud-tool data “may be used for AI model training”) [V wave 42A] | TIFIN; Daffy; Bloomerang; Salesforce (not in launch source); DonorSearch (models train on the client's own data) |
| Data stays in vendor environment | SmartSimple (no external AI services; EU data stays in EU); Fluxx (AWS Bedrock; masking) | Givebutter: "Some built-in AI features send relevant personal data to external AI providers" |

---

## 4. Implications for the repo [I]

- **No change to sponsor or vendor overlays is proposed.** The census confirms the v11 calls: TIFIN AMBER (RED-boundary), Daffy AMBER, Chariot AMBER, Blackbaud AMBER, Foundant AMBER, Candid AMBER (low), Endaoment None (watch) and Fidelity None (inform-only).
- **Report §7 still holds.** No public evidence shows AI in sponsor-side approval or eligibility determination. One forward signal is new: Foundation Source's stated roadmap of AI screening for scholarship applicants (flag-for-review framing). Track it under P-B43N25-03.
- **Grantmaking vendors show what a GREEN control set looks like** (SmartSimple, Fluxx Finn, YourCause):
  - opt-in, off by default;
  - administrator control over which fields the AI sees;
  - no training on customer data;
  - output that scores, flags or summarises but makes no determination.

  This set could serve as the vendor due-diligence baseline in [ai-governance-failure-modes.md](ai-governance-failure-modes.md) §5. That doc asks: "Is customer data used for training?" and "Does any AI component change a grant's state?"
- **Hiring and product evidence now line up.** Blackbaud's "Agents for Good" roles match a GA product. Chariot's agentic-infrastructure roles match a live MCP server with record-writing tools. TIFIN's AI roles are group-level, not TIFIN Give ([news-hiring wave 24B correction](direction-news-hiring-signals.md)).

## 5. Limits

- Vendor pages describe intent and design. Nothing was tested, and no demo was seen.
- Absence of a control statement is not evidence that the control is absent.
- Dates:
  - Several launch dates are search-index only [R]: Fluxx Finn, the Blackbaud M365 agent, Candid's 2026 items, and the Endaoment release notes.
  - Instrumentl's page metadata conflicts (published 2026-10-08, modified 2026-04-23).
  - DonorSearch Ai shows no launch date and may predate the window.
- Salesforce list prices conflict across regional pages and were not verified for the US. Only the Power of Us 10-licence offer is cited.
- Products in the repo but outside this brief are not re-scored here: Benevity Match Assurance (AMBER provisional), Fundraise Up Agentic Giving, Grantable and Kindsight. See [agentic-philanthropy-products-2026.csv](../../data/mission-2026-11-14/agentic-philanthropy-products-2026.csv) and [ai-use-case-inventory.csv](../../data/mission-2026-11-14/ai-use-case-inventory.csv).

---

## Source register

| ID | Source | Type | Source date | Accessed | URL |
|---|---|---|---|---|---|
| S1 | TIFIN Give Louise launch | vendor PR | 2025-10-27 | 2026-11-14 (repo) | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html |
| S2 | TIFIN Give DAF Program Guidelines | sponsor guidelines | undated | 2026-11-14 (repo) | https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines |
| S3 | Daffy MCP docs | sponsor docs | undated | 2026-11-15 | https://docs.daffy.org/agents/mcp |
| S4 | Daffy Quick Donate | syndicated PR | 2025-04-09 | 2026-11-14 (repo) | https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/ |
| S5 | Fidelity Charitable Virtual Assistant terms | sponsor legal | undated (2026 page) | 2026-11-15 | https://www.fidelitycharitable.org/legal/virtual-assistant.html |
| S6 | Endaoment blog index | sponsor blog | 2026-04-10; 2026-10-28 | 2026-11-15 | https://blog.endaoment.org/ |
| S7 | Chariot Gift Processing launch | vendor release | 2026-01-28 | 2026-11-14 (repo) | https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits |
| S8 | Chariot MCP server help | vendor help | undated | 2026-11-15 | https://help.givechariot.com/account-management/chariot-mcp-server |
| S9 | Ren giving platform | vendor page | undated | 2026-11-15 | https://www.reninc.com/giving-platform/ |
| S10 | Foundation Source CEO interview | trade interview | 2026-10-28 | 2026-11-15 | https://pulse2.com/foundation-source-profile-joe-mrak-interview/ |
| S11 | Foundation Source homepage | vendor page | undated | 2026-11-15 | https://foundationsource.com/ |
| S12 | Givinga homepage | vendor page | undated | 2026-11-15 | https://givinga.com/ |
| S13 | Foundant Fia release | vendor PR | 2026-09-02 | 2026-11-14 (repo) | https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations |
| S14 | SmartSimple AI Application Analysis | vendor help | 2026-06-22 | 2026-11-15 | https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview |
| S15 | SmartSimple June 2026 release notes | vendor help | 2026-06 | search index only | https://supporthub.smartsimple.com/hc/en-us/articles/40168112536343-June-2026-Release-Notes |
| S16 | Fluxx AI page (Finn, MCP) | vendor page | undated | 2026-11-15 | https://fluxx.io/ai-grants-management-software |
| S17 | Fluxx Finn launch | PR (aggregator) | 2026-08-04 | 403; repo/search | https://www.streetinsider.com/Press+Releases/Fluxx+Redefines+AI-Powered+Grantmaking+with+Launch+of+Intelligent+Assistant+Finn/26862922.html |
| S18 | Submittable Automated Review; responsible-AI principles | vendor pages | 2025-10-22 (principles) | 403 | https://submittable.com/features/automated-review ; https://www.submittable.com/blog/responsible-ai-principles-blog |
| S19 | YourCause AI grantmaking post | vendor blog | 2026-07-16 | 2026-11-15 | https://www.yourcause.com/?p=12324 |
| S20 | Blackbaud generative-AI global opt-in | vendor help | undated | 2026-11-15 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html |
| S21 | Chat for Blackbaud AI overview | vendor help | undated | 2026-11-15 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/rex/content/bb-chat-bb-ai.html |
| S22 | Blackbaud Development Agent | vendor page | undated | 2026-11-15 | https://www.blackbaud.com/products/blackbaud-development-agent |
| S23 | Blackbaud Development Agent GA | PR | 2026-03-17 | 2026-11-14 (repo) | https://www.nasdaq.com/press-release/blackbaud-launches-new-category-ai-agent-general-availability-its-first-agent-goodtm |
| S24 | Claude for Nonprofits (Blackbaud, Candid connectors) | AI provider news | 2025-12-02 | 2026-11-14 (repo) | https://www.anthropic.com/news/claude-for-nonprofits |
| S25 | Bonterra Que blog | vendor blog | 2025-10-01 | 2026-11-15 | https://www.bonterratech.com/blog/meet-bonterra-que |
| S26 | Bonterra Que release | PR | 2025-10-01 | robots 403; search index only | https://businesswire.com/news/home/20251001579571/en/Bonterra-Launches-Que-The-First-Agentic-AI-Platform-for-Funders-Nonprofits-and-Supporters |
| S27 | Instrumentl ChatGPT/Claude plugin | vendor blog | 2026-10-08 (metadata conflict) | 2026-11-15 | https://www.instrumentl.com/blog/instrumentl-chatgpt-plugin |
| S28 | Instrumentl Apply (beta) | vendor help | undated | 2026-11-14 (repo) | https://intercom.help/instrumentl/en/articles/9903781-instrumentl-apply-ai-powered-grant-applications-in-beta |
| S29 | Candid–Anthropic partnership | vendor PR | 2025-12-02 | 2026-11-14 (repo) | https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/ |
| S30 | Anthropic help: Candid connector | AI provider help | 2026-03-16 | 2026-11-14 (repo) | https://support.claude.com/en/articles/12923235-using-the-candid-connector-in-claude |
| S31 | Candid AI notice; fundraising-assistant blog | vendor pages | 2026-05-05; 2026-08-31 | robots 403; search index only | https://candid.org/artificial-intelligence-notice/ ; https://candid.org/blogs/10-ways-to-use-candids-new-fundraising-assistant/ |
| S32 | Salesforce Agentforce Nonprofit | vendor news | 2025-12-02 | 2026-11-15 | https://www.salesforce.com/news/stories/agentforce-nonprofit-announcement/ |
| S33 | SiliconANGLE on Agentforce Nonprofit | trade press | 2025-12-02 | search index only | https://siliconangle.com/2025/12/02/salesforce-targets-nonprofits-agentic-enterprise-vision/ |
| S34 | Bloomerang Penny | vendor news | 2026-03-31 | 2026-11-15 | https://bloomerang.com/news/bloomerang-penny-ai-fundraising-strategist-nonprofits |
| S35 | Bloomerang Conversational Reporting | vendor news | 2026-04-27 | 2026-11-15 | https://bloomerang.com/news/bloomerang-launches-conversational-reporting |
| S36 | Dataro–Bloomerang | partner blog | 2026 | search index only | https://dataro.io/blog/dataro-bloomerang-predictive-donor-intelligence-2026 |
| S37 | DonorSearch Ai | vendor page | undated | 2026-11-15 | https://www.donorsearch.net/solutions/donorsearch-ai/ |
| S38 | EverTrue acquires DonorSearch | vendor news | 2025-10 [R] | search index only | https://www.donorsearch.net/resources/evertrue-acquires-donorsearch-to-give-fundraisers-more-intelligence-more-capacity-and-more-time-for-relationships/ |
| S39 | Givebutter Spread 2026 recap | vendor blog | 2026-10-02 (event 2026-10-01) [V wave 42A] | 2026-11-15 | https://givebutter.com/blog/the-spread-2026-recap |
| S40 | Givebutter Magic page | vendor page | undated | 2026-11-15 | https://givebutter.com/magic |
| S41 | GoFundMe Pro launch | vendor newsroom | 2025-05-06 | 2026-11-15 | https://www.gofundme.com/c/newsroom/40-billion-raised-launches-gofundme-pro |
| S42 | GoFundMe Pro homepage | vendor page | undated | 2026-11-15 | https://pro.gofundme.com/ |
| S43 | Charity Navigator Horizon AI Search | provider release | 2025-11-24 | 2026-11-15 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search |
| S44 | Endaoment T&C | sponsor terms | 2026-08-12 | 2026-11-14 (repo) | https://docs.endaoment.org/governance/documentation/terms-and-conditions.md |

---

## Data dictionary

### `data/mission-2026-11-14/philanthropy-ai-products-2026.csv` (one row per product or product bundle)

| Column | Meaning |
|---|---|
| product_id | AIP01–AIP30 |
| vendor | Company, with sponsor in brackets where relevant |
| segment | DAF platform/sponsor, payment rail, grantmaking software, grant-seeker software, fundraising CRM/platform, charity-data provider |
| product_name | Product or bundle name as the vendor uses it; "None found" where no AI product was evidenced |
| launch_date | Launch, GA or announcement date (ISO); "undated" or "not stated" where no date was found |
| launch_basis | Document the date comes from |
| status | announced, beta, alpha, GA, live or roadmap, as the vendor states |
| functions | One or more of: search, drafting, recommendations, eligibility/scoring, agentic actions |
| what_it_does | Short description, with quotes where load-bearing |
| money_moving | Whether the AI path can create or initiate a transfer of funds (grant, donation, contribution) |
| status_changing | Whether it can change a record's or grant's state (create, delete, cancel, approve, reconcile) |
| human_approval_documented | Approval or human-decision statement on a first-party page, with its scope |
| audit_log_documented | Logging or activity-record statement |
| data_training_statement | Customer-data training, external-provider and residency statements |
| admin_opt_in | Whether AI is off by default, or enabled by an admin or the vendor |
| pricing_published | Published price or packaging; "not published" where only a demo or contact path exists |
| ai_overlay | Methodology §7 vocabulary: GREEN, AMBER or RED, plus the repo's "None" labels. Qualifiers: provisional, low, RED-boundary, GREEN-boundary, unverified |
| overlay_basis | One-line reason for the overlay |
| evidence_tag | F = primary page read; R = search index only; repo = cited from an earlier batch |
| source_url, secondary_url | Primary and supporting URLs |
| source_date | Date of the source document |
| accessed | Access date, or the reason it was not fetched |
| repo_crossref | Matching IDs in agentic-philanthropy-products-2026.csv (AP), ai-use-case-inventory.csv (U), agentic-control-gap-matrix.csv (AGM) or other docs |

### `data/mission-2026-11-14/queue-proposals-batch43-n25.csv`

Columns are those in [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md). There are three proposals, P-B43N25-01 to -03: validate the provisional GREENs, resolve the unreadable rows, and track sponsor-side AI actions.

## Validation corrections (wave 28, 2026-11-15) — governing
Source: [validation-wave28-report.md](validation-wave28-report.md); register `data/mission-2026-11-14/validation-register-wave28.csv`.

1. **§1 item 4, Fluxx pricing.**
   - **Find:** "Pricing is \"1 credit per dollar\" in credit bundles"
   - **Replace with:** "Pricing is \"1:1 credit to dollar\", with credits \"purchased as bundles\" [V wave 28]"
2. **§1 item 5, Bloomerang quote.**
   - **Find:** "\"launch campaigns, assign follow-ups, and create donor segments\""
   - **Replace with:** "\"launch campaigns, assign follow-ups, or create donor segments\""
3. **§1 item 5, Givebutter boundary.**
   - **Find:** "Most features are free, and AI custom reports need Givebutter Plus \"starts at $29/month\""
   - **Replace with:** "Two AI outputs change without per-action approval: stretch goals \"automatically increase as you raise more\", and suggested amounts are \"automatically matched to your campaign type, cause, and donor's device\". The GREEN call is therefore a GREEN/AMBER boundary case under §7's \"flag-only\" test [V wave 28]. Most features are free, and AI custom reports need Givebutter Plus \"starts at $29/month\""
4. **§1 item 8, Blackbaud Copilot.**
   - **Find:** "**\"Blackbaud Copilot\":** no product by that name. The nearest are Chat for Blackbaud AI and the Blackbaud agent for Microsoft 365 Copilot (2026-08-10 [R])."
   - **Replace with:** "**\"Blackbaud Copilot\":** Blackbaud used this name for its generative-AI assistant: in Impact Edge (release 2024-07-29), as a technical preview in Raiser's Edge NXT and Financial Edge NXT (2024-10-07), and as \"an early look at Blackbaud Copilot\" for RE NXT (2025-05-06) [V wave 28]. The current RE NXT features found are Chat for Blackbaud AI and the Blackbaud agent for Microsoft 365 Copilot (2026-08-10 [R]). Whether Chat is a rename of Blackbaud Copilot was not established."
5. **§1 item 8, Classy.**
   - **Find:** "Its AI features are personalised ask amounts and nudges, and the release cites"
   - **Replace with:** "The release says GoFundMe Pro \"fuses AI innovation with millions of fundraising data points\". The personalised ask amounts and nudges are not in this release (secondary source only) [V wave 28]. It cites"
6. **§2, overlay notes.**
   - **Find:** "- **\"AMBER (low)\"** marks read, search, scoring or drafting features with undocumented controls."
   - **Replace with:** "- The sub-labels below and in the table are local to this census. evidence-quadrant-methodology.md §7 defines only GREEN, AMBER and RED [V wave 28].\n- **\"AMBER (low)\"** marks read, search, scoring or drafting features with undocumented controls."
