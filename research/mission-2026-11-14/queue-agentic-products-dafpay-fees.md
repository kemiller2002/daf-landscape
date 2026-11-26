# Agentic philanthropy products with outcome evidence (P-INF-08) and the DAFpay fee nonprofits actually pay (P-INF-05)

**Date:** 2026-11-14 · **Queue items:** P-INF-08, P-INF-05 (`data/mission-2026-11-14/research-priority-queue.csv`) · **Datasets:** `data/mission-2026-11-14/agentic-philanthropy-products-2026.csv` (21 rows), `data/mission-2026-11-14/nonprofit-daf-receipt-fees-2026.csv` (20 rows), `data/mission-2026-11-14/queue-proposals-agentic-fees.csv` (5 proposals)

**How this was done.** I used public web pages only: vendor product, help and pricing pages, partner-platform help centres, press releases, one earnings-call transcript and press coverage. I created no account, made no write call and contacted nobody. Evidence is from 2024–2026 unless marked otherwise; one 2025 experiment is included as the only third-party-checkable outcome. Quotes are verbatim and short. Where a page returned 403/429 and I relied on a search-engine summary, the row says so.

**Builds on:** `queue-infrastructure-nonprofit-costs-emerging.md` (Q-B12 receipt-cost table, Q-N09 AI classes), `ai-economics-replacement-analysis.md` §6 and its governing red-team section (Bonterra Que added), `ai-economics-v2-observed-costs.md`, `queue-agentic-controls-and-sponsor-audits.md` (control gaps for Daffy, TIFIN, Endaoment, Chariot), `data/mission-2026-11-14/ai-use-case-inventory.csv` and `agentic-control-gap-matrix.csv`.

---

## 1. Answers

| Item | Answer | Confidence |
|---|---|---|
| **P-INF-08** | **No 2024–2026 "agentic philanthropy" product has independent outcome evidence.** Of 21 products classified, 5 are announced, 8 demonstrated, 8 deployed (one a research experiment), and **0** deployed-with-independent-outcome-evidence. Every outcome metric found is reported by the vendor or the user organisation. The strongest vendor metrics are Benevity Match Assurance (external match decline rate 30% → under 3%, 500+ clients) and Blackbaud Development Agent (3.6% reply rate, ">$300K" attributed in six months). **No product touches sponsor approval.** Two touch DAF grant recommendation: Daffy's MCP server (demonstrated, write-capable) and TIFIN's Louise (announced). Circle Foundation's agents (deployed, self-reported) produce recommendations for a Fidelity Charitable DAF. | High on classification; medium on completeness |
| **P-INF-05** | **No source shows the realised DAFpay fee mix.** Every public figure is a list price. The default 2.9% applies on every partner platform found except Every.org, which says it absorbs the fee. Four platforms add their own fee: **Bloomerang 4.85%, Donorbox 4.5%, Funraise and BetterWorld 3.9%**, all above Stripe card pricing. Fee-free DAFpay is documented only for a Chariot "enterprise plan" and for unspecified subscription volume. On five platforms the donor can cover the fee, which then comes out of the DAF grant itself. Rounding to whole dollars pushes small gifts above 2.9% (a $25 gift pays $1, or 4%). DAF Direct and PayPal Giving Fund charge nonprofits nothing. Every.org charges nothing on DAF gifts but takes 1.5% on For Good disbursements. | High on list prices; low on realised share |

---

## 2. P-INF-08: agentic philanthropy products, 2024–2026

### 2.1 Evidence classes used here

The task's four classes are stricter than the repo's earlier `deployed-with-evidence` class (`ai-economics-replacement-analysis.md` §6.1), which admitted vendor metrics.

- **announced:** a launch, plan or availability statement with no inspectable interface or documentation.
- **demonstrated:** public, inspectable documentation, a connector listing or a product page shows the capability exists. No usage data.
- **deployed:** in production with named users, GA status, adoption counts or outcome metrics. All metrics found are **vendor- or self-reported**.
- **deployed-with-independent-outcome-evidence:** an outcome measured or verified by a party other than the vendor or user organisation (an academic, auditor, or journalist with their own measurement). **No product met this bar.**

### 2.2 Classification (summary; full rows in the CSV)

| ID | Product (owner) | Launch | Action | Class | Outcome metrics (measured by) |
|---|---|---|---|---|---|
| AP01 | Agentic grantmaking ops (Circle Foundation; DAF at Fidelity Charitable) | reported 2026-11-06 | recommend; humans decide | deployed | Intake work cut from "tens of hours of desk work into a couple of minutes" (foundation leaders, quoted by the [Chronicle, 2026-11-06](https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/)) |
| AP02 | Louise (TIFIN Give / GiveClear) | 2025-10-27 | act (claimed) | announced | none ([PR Newswire](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)) |
| AP03 | MCP server, `make_donation`/`cancel_donation` (Daffy) | undated docs | act (moves DAF money) | demonstrated | none ([docs](https://docs.daffy.org/agents/mcp)) |
| AP04 | Quick Donate (Daffy) | 2025-04-09 | act | announced | none ([FF News](https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/)) |
| AP05 | Chariot MCP server | undated help page | act on nonprofit records; no payment tool | demonstrated | none ([help](https://help.givechariot.com/account-management/chariot-mcp-server)) |
| AP06 | Gift Processing AI coding agent (Chariot) | 2026-01-28 | act on nonprofit data | deployed | No Kid Hungry: 75% auto-coded, about 25 h/month gained (vendor) ([story](https://givechariot.com/resources/customer-stories/how-no-kid-hungry-turned-gift-processing-into-a-strategic-superpower)) |
| AP07 | Agentic Giving (Fundraise Up) | 2026, "rolling out in stages" | act (checkout) | demonstrated | none ([product page](https://fundraiseup.com/ai/agentic-giving/)) |
| AP08 | Development Agent (Blackbaud) | GA 2026-03-17 | act (outreach) | deployed | 70K+ touchpoints; 3.6% reply rate vs "around 0.05%" industry (76x); ">$300K in donations… attributed in the last 6 months" (vendor; benchmark unnamed) ([product](https://www.blackbaud.com/products/blackbaud-development-agent); [blog, 2026-09-08](https://blog.blackbaud.com/human-led-approach-to-understanding-ai-agent-success/)) |
| AP09 | Data Health, Admissions, Digital Marketing, AP agents (Blackbaud) | announced 2026-07 | act | announced | none ([Q2 2026 call](https://www.fool.com/earnings/call-transcripts/2026/08/07/blackbaud-blkb-q2-2026-earnings-call-transcript/)) |
| AP10 | Raiser's Edge NXT Claude connector (Blackbaud) | 2025-12-02 | read | demonstrated | none ([Anthropic](https://www.anthropic.com/news/claude-for-nonprofits)) |
| AP11 | Bonterra Que (fundraising) | 2025-10-01 | prepare/recommend | deployed | "20 to 40 percent lifts" (executive interview, no method) ([Bonterra](https://www.bonterratech.com/blog/meet-bonterra-que); [interview](https://denver-frederick.com/2025/12/17/scott-brighton-on-how-agentic-ai-is-transforming-nonprofit-fundraising/)) |
| AP12 | Que for Apricot (Bonterra) | 2026-05-18 | assistive | deployed | 40% less reporting time, 35% less data entry (vendor; seen in search summary only, page 403) ([BusinessWire](https://www.businesswire.com/news/home/20260518336577/en/Bonterra-Launches-Que-for-Apricot-The-Intelligent-Assistant-for-Modern-Case-Management)) |
| AP13 | Match Assurance + Grant Summaries (Benevity) | 2026-03 | act (auto-submit) | deployed | 500+ clients; external match decline 30% → <3%; review 3–5 h/week → about 2 h (vendor) ([release, 2026-06-04](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)) |
| AP14 | AI grant scoring; Impact Workspace (Benevity) | 2026-06-04 | recommend / act | announced | none (same release) |
| AP15 | Nonprofit MCP connector (Benevity) | 2025-12-02 | read | demonstrated | none ([Anthropic help](https://support.claude.com/en/articles/12923227-using-the-benevity-connector-in-claude)) |
| AP16 | Candid MCP connector | 2025-12-02 | read | demonstrated | none ([Candid](https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/)) |
| AP17 | Instrumentl MCP plugin (ChatGPT/Claude) | Claude since June 2026; post dated 2026-10-08 | read + write | deployed | No plugin metrics; 6,000+ nonprofits; vendor survey: 69% of grant pros "not confident" AI output is accurate ([blog](https://www.instrumentl.com/blog/instrumentl-chatgpt-plugin)) |
| AP18 | Prospecting/Writing/Management "desks" (Grantable) | undated | recommend / generate | demonstrated | Testimonials only; $ figures on page are mock-ups ([grantable.co](https://www.grantable.co/)) |
| AP19 | Impala MCP server | 2026-08-19 | read | demonstrated | none ([Impala](https://impala.digital/blog/impala-launches-ai-native-mcp-server-for-the-philanthropic-sector)) |
| AP20 | Goodera MCP server | 2025-06-24 | read ("act" claimed) | announced | none ([Goodera](https://www.goodera.com/news/goodera-launches-mcp-server)) |
| AP21 | Agent Village fundraiser (Sage Future) | 2025-04 | act (ran campaign) | deployed (experiment) | $257 in about a week for Helen Keller International, "nearly all" from spectators (operator figure, reported by [TechCrunch, 2025-04-08](https://techcrunch.com/2025/04/08/a-nonprofit-is-using-ai-agents-to-raise-money-for-charity)) |

Counts: announced 5 · demonstrated 8 · deployed 8 (including AP21) · deployed-with-independent-outcome-evidence **0**.

### 2.3 Findings

1. **Journalism is not measurement.** The Circle Foundation case (the only "E" in the earlier Q-N09 work) is a journalist's report. The time-saving claim comes from foundation leaders, and the article reports no counts of proposals, grants or dollars. The foundation says it intends to track progress and share findings. The case is reclassified here from "E" to **deployed (self-reported)**.
2. **The best metrics sit in adjacent markets, not in DAFs.** Benevity (corporate matching) and Blackbaud (donor outreach) publish the most specific numbers, but both are vendor-measured. Blackbaud's 76x comparison uses an unnamed "industry" email benchmark. On the Q2 2026 call, management said guidance has no "meaningful revenue contribution" from its new AI products ([transcript](https://www.fool.com/earnings/call-transcripts/2026/08/07/blackbaud-blkb-q2-2026-earnings-call-transcript/)).
3. **Write-capable MCP is spreading, but not into sponsor approval.**
   - Instrumentl (grant pipeline records) and Chariot (donation records) now expose write tools.
   - Daffy's is the only documented agent tool that creates a DAF grant recommendation.
   - Chariot's MCP lists no grant- or payment-initiating tool. Benevity's connector is for research only, per [Anthropic's help page](https://support.claude.com/en/articles/12923227-using-the-benevity-connector-in-claude). Benevity's own help page, which returned 403, words it as "discover and donate".
   - [I] This confirms the repo's finding that the agentic frontier is on the donor side, upstream of sponsor approval.
4. **No official Every.org or Endaoment MCP server was found.** Third-party wrappers exist (e.g. Vinkius's "Every.org Charity" listing), and GiveReady, a third-party MCP project, offers USDC giving. None is published by the sponsor.
5. **Fundraise Up Agentic Giving moved from "A" to demonstrated.** The product page now documents admin enablement, Stripe Link checkout and a 25-campaign profile. It is "rolling out in stages", with no DAF path and no metrics.
6. **The only third-party-checkable agent outcome is tiny and from 2025.** Sage's Agent Village raised $257, mostly from spectators. [I] This marks the frontier of autonomous fundraising, not a market.

### 2.4 Does anything touch DAF grant recommendation or sponsor approval?

| Touchpoint | Products | Evidence |
|---|---|---|
| Donor/advisor creates a DAF grant recommendation | Daffy MCP (AP03), Daffy Quick Donate (AP04), TIFIN Louise (AP02), Circle Foundation agents (AP01, via human submission) | Demonstrated, announced, announced and self-reported respectively |
| Sponsor approval / eligibility | **None found** | Benevity Match Assurance (AP13) is the closest analogue: automated eligibility for corporate matches |
| Recipient-side processing of DAF gifts | Chariot Gift Processing (AP06), Chariot MCP (AP05) | Vendor case; demonstrated |

---

## 3. P-INF-05: what DAFpay costs nonprofits

### 3.1 The contract

Chariot's Nonprofit Terms (updated 2026-10-14), §4.4 ([legal-nonprofit](https://www.givechariot.com/legal-nonprofit)):

- **Rate:** "You will pay the applicable DAFpay Fees per your agreements with any Fundraising Platforms, or if no such agreements exist, you will pay 2.9% (rounded to the nearest whole dollar)".
- **Waiver:** a Chariot Subscription "can include DAFpay volume with no DAFpay Fees as governed by your Chariot Subscription Order Form".
- **Collection:** monthly invoice, a charge to a payment method, a debit of the Chariot Deposit Account, or "DAFpay Network deduct[s] DAFpay Fees… for payments to Non-User Nonprofits". Fees are due in 15 days, carry a 0.5% monthly finance charge, and can be debited after 45 days.

[I] A nonprofit that never signed up with Chariot still pays, because the fee is netted from the check. Chariot's FAQ confirms that platforms "activate DAFpay automatically for eligible nonprofits" ([FAQ](https://help.givechariot.com/dafpay/dafpay-faqs)).

### 3.2 List price by channel (per $1,000 gift, if the nonprofit pays)

| Channel | Chariot | Platform | Total | Donor can cover? | Source |
|---|---|---|---|---|---|
| Default / Givebutter / Give Lively / Giving Block / 4aGoodCause | 2.9% | 0 | **$29** | GL, TGB yes; Givebutter no | [Givebutter](https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method), [Give Lively](https://www.givelively.org/resources/understand-how-donors-can-cover-third-party-transaction-fees), [TGB](https://knowledge.thegivingblock.com/articles/knowledge/donor-advised-fund-daf-chariot-integration-faq), [4aGoodCause](https://help.4agoodcause.com/help/how-to-accept-dafpay-donations) |
| Fundraise Up | 2.9% | FRU standard rate (amount not stated) | $29 + FRU rate | yes | [FRU docs](https://fundraiseup.com/docs/dafpay/) |
| Funraise | 2.9% | 1% (assessed by Chariot) | **$39** | no | [Funraise](https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay) |
| BetterWorld | 2.9% | 1% | **$39** | yes | [BetterWorld](https://help.betterworld.org/en/articles/8558015-what-are-the-processing-fees-and-who-covers-them) |
| Donorbox | 2.9% | 1.6% | **$45** | yes | [Donorbox](https://donorbox.org/explore/donor-advised-fund-donations) |
| Bloomerang | 2.9% | 1.95% | **$48.50** | not stated | [Bloomerang, 2026-10-29](https://bloomerang.com/blog/dafpay) |
| GoFundMe Pro (beta) | Chariot rate, not stated | 0 in beta | not stated | not stated | [GoFundMe Pro](https://proinfo.gofundme.com/dafpay-early-access.html) |
| Every.org | absorbed by Every.org | 0 | **$0** | n/a | [every.org/daf-donations](https://www.every.org/daf-donations) (search-index capture; live page 403/429) |
| Chariot enterprise plan | 0 | custom | custom | n/a | [Fundraise Up blog](https://fundraiseup.com/blog/accept-daf-donations-with-fundraise-up/) |
| DAF Direct | — | 0 | **$0** | n/a | [DAF Direct](https://www.dafdirect.org/about-daf-direct/index.html) |
| PayPal Giving Fund | — | 0 | **$0** | n/a | [PPGF](https://www.paypal.com/us/webapps/mpp/givingfund/about) |
| Every.org via For Good disbursement | — | 1.5% | $15 | n/a | [Every.org blog, 2026-07-08](https://blog.every.org/how-does-every-org-work-your-top-10-pricing-questions-answered/) |
| Benchmark: Stripe card | — | 2.9% + $0.30 | $29.30 | — | [Stripe](https://stripe.com/pricing) |

### 3.3 Subscriptions: what is and is not public

- **Pricing page:** shows "DAFpay… Free to activate… + 2.9% fee per donation" and "Components $199/mo, billed annually" ([chariot-pricing](https://www.givechariot.com/chariot-pricing)). It does not say whether Components removes the per-gift fee.
- **Billing help:** subscriptions carry a "volume limit", and fees above it ("such as excess DAFpay volume") are billed monthly ([billing](https://help.givechariot.com/dafpay/dafpay-billing)).
- **Earlier repo capture:** Growth was $4,740/yr with 250 gift-processing donations and still carried a "2.9% initiation fee" on standalone DAFpay components (`research/challenger-economics-daffy-chariot-charityvest-2026-11-12.md` line 20).
- **Conclusion [I]:** the only tier publicly stated to remove the 2.9% fee is "enterprise". The volume at which a subscription pays for itself cannot be computed from public data.

### 3.4 Effective rate from whole-dollar rounding [S, arithmetic]

Calculated from the ToS rounding rule and Give Lively's $1 minimum:

| Gift | 2.9% | Fee charged | Effective rate |
|---|---|---|---|
| $25 | $0.73 | $1 | 4.0% |
| $50 | $1.45 | $1 | 2.0% |
| $100 | $2.90 | $3 | 3.0% |
| $300 (Give Lively median) | $8.70 | $9 | 3.0% |
| $500 | $14.50 | $15 | 3.0% |
| $1,000 (Give Lively average) | $29.00 | $29 | 2.9% |

### 3.5 What can be said about realised fees

- **Realised mix: not observable.** No Chariot disclosure, platform report or nonprofit filing found gives the share of DAFpay volume under each fee regime.
- **Scale anchors (vendor or platform figures, not fee data):**
  - Give Lively: about 20,000 nonprofits have DAFpay enabled. "A few hundred" received about 500 grants worth nearly $500,000, with an average of about $1,000 and a median of about $300 ([Give Lively, 2026-09-28](https://www.givelively.org/blog/daf-day-is-in-october-get-ready-for-it)). [S] At 2.9% that is up to about $14,500 in fees, before any donor cover.
  - Pan-Mass Challenge raised more than $5 million through DAFpay in 2025 ([Chariot, Jan 2026](https://www.givechariot.com/resources/insights/chariots-2025-year-in-review--whats-next)). [S] At the default rate that would be about $145,000. Its actual terms are unknown; an organisation of this size is the most likely enterprise customer.
- **Who bears a donor-covered fee [I]:** when the donor covers it, the DAF grant is grossed up ("the donation will be increased by that amount", [The Giving Block](https://knowledge.thegivingblock.com/articles/knowledge/donor-advised-fund-daf-chariot-integration-faq)). The fee is then paid from charitable DAF assets rather than by the nonprofit. Either way, about 2.9% of the gift leaves the charitable sector.
- **Stacking:** on Bloomerang, Donorbox, Funraise and BetterWorld, DAFpay costs nonprofits **more than card** processing. DAFpay money still moves on the sponsor's own rail. This supports the earlier inference that the fee buys intent capture and attribution, not payment.
- **Removal after the October 2026 terms:** no evidence found either way. Chariot runs a help article titled "Why did I receive an invoice from Chariot Giving Inc." (URL now 404), which suggests unexpected invoices are common enough to need an FAQ answer.

---

## 4. Implications for repo conclusions

- **`ai-use-case-inventory.csv` / Q-N09:** the Circle Foundation "E" should read **deployed (self-reported)**. The repo has no independent outcome evidence for any AI or agent product in the DAF or philanthropy-tech market.
- **Q-B12 receipt-cost table:** add the stacked rows ($39–$48.50 per $1,000) and the Every.org $0 DAFpay row. The "$29 default" is a floor on stacking platforms, not a ceiling.
- **Nonprofit bargaining power:** Chariot's terms let platforms set the fee, so the platform, not the nonprofit, holds the bargaining position. Nonprofits that never sign up with Chariot still pay through netted checks.

## 5. Limitations

- Several pages returned 403, 429 or 404: Every.org pages, Donorbox help, Benevity help, the BusinessWire Bonterra release, the Blackbaud IR release and two Chariot Intercom articles. These are marked as search-index captures in the CSVs.
- Executed platform–Chariot agreements and Chariot Order Forms are not public, so negotiated rates are unknown.
- "Not found" means searched and not found. It does not mean absent.
- The Blackbaud release's +39% gift size and +10-point open rate were seen only in search summaries. Fetched pages confirmed the 76x reply rate, the 3.6% vs 0.05% figures and ">$300K".

## 6. Source register

| ID | Source | URL | Date |
|---|---|---|---|
| S01 | Chariot Nonprofit Terms §4.4 | https://www.givechariot.com/legal-nonprofit | 2026-10-14 |
| S02 | Chariot pricing | https://www.givechariot.com/chariot-pricing | read 2026-11-14 |
| S03 | Chariot DAFpay FAQ; billing | https://help.givechariot.com/dafpay/dafpay-faqs ; https://help.givechariot.com/dafpay/dafpay-billing | undated |
| S04 | Givebutter DAFpay help | https://help.givebutter.com/en/articles/6764835-how-to-use-givebutter-s-dafpay-donation-method | 2026-10-06 |
| S05 | Fundraise Up DAFpay docs and blog | https://fundraiseup.com/docs/dafpay/ ; https://fundraiseup.com/blog/accept-daf-donations-with-fundraise-up/ | 2026-10-30 ; 2026-10-28 |
| S06 | Donorbox DAF page | https://donorbox.org/explore/donor-advised-fund-donations | read 2026-11-14 |
| S07 | Bloomerang DAFpay blog | https://bloomerang.com/blog/dafpay | 2026-10-29 |
| S08 | Funraise DAFpay help | https://help.funraise.io/en/articles/12142901-accept-daf-donations-with-dafpay | 2026-01-30 |
| S09 | BetterWorld fees help | https://help.betterworld.org/en/articles/8558015-what-are-the-processing-fees-and-who-covers-them | undated |
| S10 | Give Lively fee help; DAF Day blog | https://www.givelively.org/resources/understand-how-donors-can-cover-third-party-transaction-fees ; https://www.givelively.org/blog/daf-day-is-in-october-get-ready-for-it | c.2026 ; 2026-09-28 |
| S11 | The Giving Block Chariot FAQ | https://knowledge.thegivingblock.com/articles/knowledge/donor-advised-fund-daf-chariot-integration-faq | undated |
| S12 | 4aGoodCause DAFpay help | https://help.4agoodcause.com/help/how-to-accept-dafpay-donations | 2026-05-18 |
| S13 | GoFundMe Pro DAFpay | https://proinfo.gofundme.com/dafpay-early-access.html | undated |
| S14 | Every.org DAF page; pricing blog | https://www.every.org/daf-donations ; https://blog.every.org/how-does-every-org-work-your-top-10-pricing-questions-answered/ | capture ; 2026-07-08 |
| S15 | DAF Direct; PayPal Giving Fund | https://www.dafdirect.org/about-daf-direct/index.html ; https://www.paypal.com/us/webapps/mpp/givingfund/about | read 2026-11-14 |
| S16 | Chariot 2025 year in review | https://www.givechariot.com/resources/insights/chariots-2025-year-in-review--whats-next | 2026-01-05 |
| S17 | Inequality.org on Chariot fee | https://inequality.org/article/new-donor-advised-fund-tech-raises-old-concerns/ | 2024-08-09 |
| S18 | Chronicle: Circle Foundation | https://www.philanthropy.com/news/ai-recommends-humans-decide-circle-foundations-bet-on-agentic-philanthropy/ | 2026-11-06 |
| S19 | TIFIN Louise release | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html | 2025-10-27 |
| S20 | Daffy agents/MCP docs; FF News | https://docs.daffy.org/agents/mcp ; https://ffnews.com/newsarticle/paytech/daffy-is-using-ai-to-reshape-the-future-of-charitable-giving/ | undated ; 2025-04-09 |
| S21 | Chariot MCP; Gift Processing; No Kid Hungry | https://help.givechariot.com/account-management/chariot-mcp-server ; https://givechariot.com/resources/insights/chariot-launches-first-gift-processing-platform-for-nonprofits ; https://givechariot.com/resources/customer-stories/how-no-kid-hungry-turned-gift-processing-into-a-strategic-superpower | undated ; 2026-01-28 |
| S22 | Fundraise Up Agentic Giving; Pulse 2.0 | https://fundraiseup.com/ai/agentic-giving/ ; https://pulse2.com/fundraise-up-introduces-agentic-giving-category-for-ai-powered-donations/ | read 2026-11-14 ; 2026-08-02 |
| S23 | Blackbaud product page, blog, Q2 2026 call | https://www.blackbaud.com/products/blackbaud-development-agent ; https://blog.blackbaud.com/human-led-approach-to-understanding-ai-agent-success/ ; https://www.fool.com/earnings/call-transcripts/2026/08/07/blackbaud-blkb-q2-2026-earnings-call-transcript/ | 2026 ; 2026-09-08 ; 2026-08-07 |
| S24 | Bonterra Que; Apricot; interview | https://www.bonterratech.com/blog/meet-bonterra-que ; https://www.businesswire.com/news/home/20260518336577/en/Bonterra-Launches-Que-for-Apricot-The-Intelligent-Assistant-for-Modern-Case-Management ; https://denver-frederick.com/2025/12/17/scott-brighton-on-how-agentic-ai-is-transforming-nonprofit-fundraising/ | 2025-10 ; 2026-05-18 ; 2025-12-17 |
| S25 | Benevity Live 2026 release; Anthropic Benevity help | https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026 ; https://support.claude.com/en/articles/12923227-using-the-benevity-connector-in-claude | 2026-06-04 |
| S26 | Candid; Anthropic Claude for Nonprofits | https://candid.org/press/candid-partners-with-anthropic-to-bring-trusted-data-to-claude-for-nonprofits/ ; https://www.anthropic.com/news/claude-for-nonprofits | 2025-12-02 |
| S27 | Instrumentl MCP plugin; Apply beta | https://www.instrumentl.com/blog/instrumentl-chatgpt-plugin ; https://intercom.help/instrumentl/en/articles/9903781-instrumentl-apply-ai-powered-grant-applications-in-beta | 2026-10-08 |
| S28 | Grantable | https://www.grantable.co/ | read 2026-11-14 |
| S29 | Impala; Goodera MCP | https://impala.digital/blog/impala-launches-ai-native-mcp-server-for-the-philanthropic-sector ; https://www.goodera.com/news/goodera-launches-mcp-server | 2026-08-19 ; 2025-06-24 |
| S30 | TechCrunch: Sage Agent Village | https://techcrunch.com/2025/04/08/a-nonprofit-is-using-ai-agents-to-raise-money-for-charity | 2025-04-08 |

## 7. Data dictionary

### `agentic-philanthropy-products-2026.csv` (one row per product or feature)

| Column | Meaning |
|---|---|
| product | Product or feature name |
| owner | Vendor or operating organisation |
| launch_date | Announcement, GA or report date as stated; "undated" if none |
| action_capability | read / recommend / generate / act, with scope |
| evidence_class | announced / demonstrated / deployed / deployed-with-independent-outcome-evidence (§2.1). "deployed (experiment)" marks a research run |
| outcome_metrics | Metrics as published; "none" if none |
| measured_by | Who produced the metric (vendor, user organisation, journalist, third party) |
| source_url | Primary URL used for classification |
| product_id | AP01–AP21 |
| segment | Market segment |
| daf_touchpoint | Where the product meets DAF flows, if anywhere |
| touches_sponsor_approval | Whether the product acts in sponsor approval or eligibility |
| independent_outcome_evidence | yes/no |
| notes | Caveats and secondary URLs |

### `nonprofit-daf-receipt-fees-2026.csv` (one row per channel or plan)

| Column | Meaning |
|---|---|
| route_id | F01–F20 |
| route | Channel or plan |
| platform_or_channel | Platform or operator |
| chariot_dafpay_fee_pct | Chariot fee as stated |
| platform_fee_pct | Platform's added fee as stated |
| total_fee_pct_nonprofit_default | Sum when the nonprofit pays |
| fee_per_1000_usd_nonprofit_default | Same, per $1,000 gift (before whole-dollar rounding) |
| who_pays_by_default | Party bearing the fee if the donor does not cover it |
| donor_can_cover | Whether a donor-cover option exists |
| collection_method | Invoice, charge, debit or netting |
| waiver_or_subscription_terms | Documented ways to reduce or remove the fee |
| source_url / source_date | Primary source and its stated date |
| evidence_status | primary / search-index capture / repo capture |
| notes | Caveats |

### `queue-proposals-agentic-fees.csv`

Format per `data/mission-2026-11-14/queue-proposals-README.md`; prefix P-AGF-.

## Validation corrections (wave 8, 2026-11-14) — governing
Source: [validation-wave8-report.md](validation-wave8-report.md). Where these conflict with the text above (including the earlier wave-7 Audax note), these govern.

21. **Line 15 and line 47 (AP13).** Replace "external match decline 30% → <3%" with: "external match decline 30% → <3% at **one unnamed early-adopter partner** (vendor blog)". Keep "500+ clients" as a separate adoption figure, not an outcome.
22. **Line 109 (Every.org).** Add: "Every.org currently absorbs the For Good fee for bank-account gifts; nonprofits avoid it by linking Stripe or PayPal Grants (0%). The live pricing page was not re-read (HTTP 429) on 2026-11-14."
23. **§3.4.** Add: "The rounding applies only where no platform agreement sets the fee, and most platforms let donors cover the fee, so 4.0% at $25 is the nonprofit's worst case."
