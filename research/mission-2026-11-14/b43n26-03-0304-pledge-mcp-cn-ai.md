# Pledge partner MCP server and Charity Navigator's AI channel (P-B43N26-03-03, P-B43N26-03-04)

**Date:** 2026-11-20. TASKID b43n26-03-0304. Files only: no commit, no push. The census CSV was not edited.

**Outputs:**
- Data: [`data/mission-2026-11-14/pledge-mcp-cn-ai-2026-11-20.csv`](../../data/mission-2026-11-14/pledge-mcp-cn-ai-2026-11-20.csv). It has 7 rows: 1 proposed census row (AIP31, Pledge) and 6 Charity Navigator (CN) AI statement rows (5 CN first-party, 1 from the partner).
- Queue: [`data/mission-2026-11-14/queue-proposals-b43n26-03-0304.csv`](../../data/mission-2026-11-14/queue-proposals-b43n26-03-0304.csv) (6 rows).

**Builds on:**
- [b43n26-03-charity-data-terms-ai.md](b43n26-03-charity-data-terms-ai.md) §2.1, §2.4 and §5.2;
- [direction-ai-product-census.md](direction-ai-product-census.md) and its CSV `philanthropy-ai-products-2026.csv`;
- [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §7, §7a–§7c.

Tags: **[F]** primary page read on 2026-11-20; **[I]** inference; **[S]** secondary or repo-only.

---

## 1. Method

- **Desk reading only.** No logins, no forms, no outreach. No requests to the MCP endpoint `https://www.pledge.to/partner/mcp`: no `initialize`, no `tools/list` and no OAuth metadata probe. No keyed API calls.
- **Client.** `curl` with the generic user agent `research-script/1.0`. Pages were turned into text with a stdlib HTML-to-text helper kept in the session scratchpad, not in the repo.
- **Robots.** robots.txt was read on each host first. The 200 responses were parsed for ClaudeBot, anthropic-ai, Claude-User, Claude-Web, Claude-SearchBot and `*`. A 404 means no rules, the repo convention.
- **Pledge.** Pages were found through the developer site's own sitemap (`/sitemap-index.xml` → `/sitemap-0.xml`, 19 URLs). The REST API reference renders in the browser, so its source OpenAPI file `/api.yaml` (5,770 lines, `openapi: 3.1.1`, `info.version: 1.0.1`) was read directly. It sits on the documentation host, not on the MCP endpoint.
- **CN.**
  - The developer-portal sitemap was read. From it: changelog, customer stories (index plus 2 stories), plans/Usage & Quotas, pricing, overview, data-sharing, terms summary, support, alerts, ratings and home.
  - From the www sitemap: all 18 URLs under `/about-us/press-release/`, plus the press room, the GraphQL API product page, the API Terms page, one nonprofit-resources AI page and the True Impact blog.
  - Each text was searched for `AI`, artificial intelligence, LLM, language model, MCP, machine learning, agent, ChatGPT, Perplexity, Giving Compass and Horizon. Every quote in the CSV was checked by script as an exact substring of the fetched text (7 of 7 match).
- **Dates.** Press-release dates are the dates printed in the release text. The CN post sitemap gives `lastmod 2026-08-21` for 17 of 18 releases, which looks like a site migration, so it was not used.
- **Scoring.** Pledge receives a §7a.2 product-level reading, not an area overlay, because Pledge is not scored in A1–A5. There is one scorer, so the reading is provisional (§5).

### 1.1 Robots and fetch log (2026-11-20 UTC)

| Host | robots.txt | Claude agents named? | Decision | Requests | 200s |
|---|---|---|---|---|---|
| developer.pledge.to | 404 (none) | n/a | allowed | 15 | 11 (llms.txt, sitemap.xml, openapi.yaml, openapi.json: 404) |
| www.pledge.to | 200 | no; `*` disallows /oauth, /organizations (except exact) | allowed for pages read; `/partner/mcp` not requested by task rule | 4 | 4 |
| developer.charitynavigator.org | 200 | no; `*` disallows /signin, /checkout, /subscriptions etc. | allowed | 15 | 15 |
| www.charitynavigator.org | 200 | no; `*` disallows /search, /basket, /profile etc. | allowed by robots (see §4, terms) | 27 | 27 |
| www.givingcompass.org | 200 | no; `*` Allow / | allowed | 2 | 2 |

No host named a Claude or Anthropic agent, and no known off-limits host was contacted.

---

## 2. Task 1: Pledge partner MCP server (P-B43N26-03-03)

### 2.1 What the docs say [F]

- **Purpose and user.** From the [setup guide](https://developer.pledge.to/guides/mcp/): "The Pledge MCP server (pledge-developer) lets you connect AI coding assistants directly to your Pledge partner account using the Model Context Protocol. Once connected, your AI assistant can search nonprofits, manage fundraisers, create donations, and more." The endpoint is `https://www.pledge.to/partner/mcp`. Setup steps are given for six clients: Claude Code, Cursor, Codex, VS Code (Copilot Chat), Claude Desktop (via `mcp-remote`) and Windsurf.
- **Tools.** The [tool reference](https://developer.pledge.to/reference/mcp/) lists **17 tools in 6 groups**. The task named 3 of them.

  | Group | Tools |
  |---|---|
  | Account | `create_account` ("Create a new Pledge partner account") |
  | Nonprofits | `lookup_organization` ("Search nonprofits by name, EIN, country, or cause") |
  | Fundraisers | `create_nonprofit_fundraiser`, `create_crowdfund`, `get_fundraiser`, `update_fundraiser`, `upsert_fundraiser` |
  | Donations | `create_donation` ("Create a donation to a nonprofit through your account"), `get_donation`, `list_donations` |
  | Webhooks | `create_webhook`, `get_webhook`, `list_webhooks`, `delete_webhook` ("Remove a registered webhook endpoint") |
  | Developer utilities | `list_endpoints`, `explain_error`, `integration_checklist` ("Verify your API key and check how far along your integration is") |

  "Your AI assistant can call these tools directly — no manual API calls required."

### 2.2 Does `create_donation` move money? Yes [F]

- **The MCP description.** "Create a donation to a nonprofit through your account."
- **The REST operation it mirrors.** `POST /donations` (`createDonation`) in [api.yaml](https://developer.pledge.to/api.yaml). The required fields are `email`, `first_name`, `last_name` and `amount`, plus `organization_id` or `organization_ein`. `send_tax_receipt` optionally emails a receipt to the donor. [I] The tool-to-endpoint mapping is inferred from the shared name and description; the docs do not state it.
- **Flow of funds** (api.yaml, Donations tag): "Once a month, or when a certain threshold is reached, we will batch the amount for all the donations and bill your payment method on file." Also: "In order to process donations, you need to set up a payment method in the Impact Hub."
- **Point-redemption guide** ([source](https://developer.pledge.to/guides/point-redemption/)): "Pledge tracks this donation as pending. On a periodic basis, we will batch up all of the pending donations and charge them to a payment method provided to us in a single transaction." Also: "We disburse funds to nonprofits on a monthly basis."
- **Fees** (same guide): "Pledge takes a 5% fee from the donation." ACH costs 0.8% (capped at $5) and card costs 2.9% + $0.30. There is "a $5 disbursement fee for the nonprofits".
- **Reading [I].** One tool call creates a donation that is billed to the partner's stored payment method and later paid out to the nonprofit. No further documented step is needed. The `DonationStatus` enum includes `canceled`, but no cancel or refund endpoint and no cancel tool is documented.

### 2.3 Controls documented

| Control | Documented? | Evidence [F] |
|---|---|---|
| **Auth (REST)** | yes | "An API key is required in all API requests." Bearer token, key taken from the Impact Hub (api.yaml `securitySchemes.bearerAuth`; Getting Started). |
| **Auth (MCP)** | **not documented** | All six client configs give only the URL, with no key, header or OAuth step. `integration_checklist` says it verifies "your API key". [I] Either the client's MCP OAuth flow or an API key may apply. It could not be checked without calling the endpoint. |
| **Per-call confirmation or approval** | **none** | Neither MCP page nor the API reference mentions confirmation, approval or human review before a donation. No `readOnlyHint` or `destructiveHint` annotations are documented. [I] Annotations, if any, are visible only through `tools/list` on the endpoint. |
| **Limits** | **none for MCP** | No per-donation, per-day or per-session cap. `amount` has only a format pattern (`^\d+(\.\d+)?$`). The 50,000-row limit applies to REST CSV batches, which have no MCP tool. |
| **Idempotency** | batches only | An `Idempotency-Key` is required for CSV donation batches. None is documented for single `createDonation`. |
| **Sandbox** | REST only | "a completely isolated environment from production, with different databases, API keys". The MCP guide gives only the production URL, and no staging MCP endpoint is documented. |
| **Audit trail** | partial | `get_donation` and `list_donations` exist, and donations appear in the Impact Hub. The Donation schema has no field marking agent or MCP origin. |
| **Review step** | not for donations | The only review found is for receipts: "we can send a tax receipt to the user (once reviewed and approved by our compliance team)" (point-redemption guide). |
| **AI training or data-use statement** | none found | Neither page mentions training or retention. The governing API terms are private ([b43n26-03 §2.4](b43n26-03-charity-data-terms-ai.md)). |

### 2.4 Reading under §7a.2 [I]

**Product-level reading: AMBER (RED-boundary, provisional).** This is not an area overlay and not a first GREEN or first RED under §7c.

- **What points to RED.** The RED test is "AI can complete a money-moving or status-clearing action without documented sponsor or human approval". On the public docs this is met:
  - `create_donation` moves the partner's money through automatic billing;
  - no approval, confirmation or cap is documented;
  - unlike Daffy (AIP02) and TIFIN (AIP01), no downstream sponsor review is documented.
- **Why it is held at AMBER.**
  1. The MCP auth flow and any per-tool annotations are served only by the endpoint. The task barred calling it, so part of the control surface could not be read. §7b.2 says "A component whose controls could not be read counts as AMBER (unverified)".
  2. Only one scorer has read it (§5).
  3. Whether Pledge's charitable entity reserves discretion over API donations was not read (queue P-B43N26-0304-03).
- **Comparison with the census.**

  | Row | Money-moving AI tool | Documented controls | Downstream approval | Reading |
  |---|---|---|---|---|
  | AIP02 Daffy MCP | `make_donation` ("Moves real money") | OAuth or key; activity in app; no caps | sponsor "sole discretion" | AMBER |
  | AIP07 Chariot MCP | not documented | client confirmation; destructiveHint; log | n/a | AMBER |
  | **AIP31 Pledge MCP (proposed)** | `create_donation` | REST API key; no MCP auth, confirmation, cap or annotation documented | none documented | **AMBER (RED-boundary, provisional)** |

- **Intended user and scope.** It is aimed at partner developers in coding assistants, not donors. The person giving is the partner (marketplaces, reward platforms, memorial sites), and donors are named in the data. [I] So an assistant's mistake while coding, such as a test call sent to production, would create a real billed donation and possibly a tax receipt to a real email address. The docs offer a sandbox for REST, but none for MCP.
- **Entity scope.** Pledge is not a DAF sponsor scored in A1–A5. Under §7a.3 this reading enters no provider row unless a T1–T4 tie is shown, and none was found.

---

## 3. Task 2: Charity Navigator's AI channel (P-B43N26-03-04)

### 3.1 Statements found (2025–2026, quoted in full in the CSV)

| ID | Date | Source | Category | Verbatim (abridged here; full in CSV) |
|---|---|---|---|---|
| CNAI-01 | 2025-11-24 | [CN release: Horizon AI Search](https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/) | AI partner (Giving Compass) | "Powered by Giving Compass’s Natural Language Search API, the new Horizon AI Search experience lets donors describe what they care about to receive instant, personalized recommendations …" |
| CNAI-02 | 2025-11-24 | same | ranking method | "Giving Compass’s search engine uses a hybrid approach — word matching plus meaning matching — to rank nonprofits based on relevance, clarity, and donor intent." |
| CNAI-03 | 2026-05-18 | [CN release: Allegory](https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/) | AI partner (API licensee) | "… Allegory, the first AI-powered operating system for grant funding, announced the integration of Charity Navigator’s ratings API into Allegory’s platform." |
| CNAI-04 | undated (page modified 2026-11-17; "API user since spring 2026") | [Givelink customer story](https://developer.charitynavigator.org/customerstory-givelink) | customer AI use (roadmap) | "… is developing an AI-powered recommendation feature that will pull rating data in to surface highly rated nonprofits matching a donor's interests and location." |
| CNAI-05 | 2025-07-15 | [CN release: board](https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/) | AI governance context (not data use) | "Andrew’s deep understanding of leveraging technology and AI for social impact … are precisely the expertise we need." |
| CNAI-06 | 2026-01-20 | [Giving Compass release](https://www.givingcompass.org/giving-compass-launches-api-to-enable-smarter-philanthropy-where-giving-decisions-are-made/) | partner statement (not CN) | "Together, the organizations launched Horizon AI Search, powered by the Giving Compass API …" |

**Counts.**
- 5 CN-published statements in 2025–2026 mention AI. 3 tie AI to CN data or the API: CNAI-01/02 (one release), CNAI-03 and CNAI-04. CNAI-05 is about board expertise.
- 1 partner statement (CNAI-06) corroborates the Giving Compass collaboration.

### 3.2 Giving Compass collaboration [F]

- **CN's release (2025-11-24).** It calls Horizon "a strategic partnership to build a new intelligent nonprofit search experience" and "The first phase of this collaboration". The ranking is described as "word matching plus meaning matching".
- **What the release does not say.** It does not use the words LLM, model, generative or ranking controls. It does not say how CN ratings enter the ranking, or whether CN data is sent to Giving Compass or to any model provider.
- **Giving Compass's release (2026-01-20).** It says Horizon is "powered by the Giving Compass API". It also describes "AI-ready search" and "AI-extracted impact narratives" as Giving Compass products, not CN's.
- **[I] Direction of the data flow.** CN supplies ratings and Giving Compass supplies the search technology. The public record is silent on any licence covering CN ratings inside Giving Compass's systems.

### 3.3 Searched and not found [F]

- **MCP server.** None was found on the developer portal: no page, changelog entry or doc in its 70-URL sitemap. An earlier batch found `llms.txt` returned 404 ([b43n26-03 §1.1](b43n26-03-charity-data-terms-ai.md)).
- **AI-specific plan or terms.**
  - The [Usage & Quotas page](https://developer.charitynavigator.org/plans) defines the Startups, Small, Midsize and Enterprise plans plus Academics/Personal Use. Access is split into "Data Essentials" and "Premium Data" (`publishedAlerts`, Midsize and Enterprise only). There is a 1,000 requests-per-minute rate limit.
  - The [data-sharing page](https://developer.charitynavigator.org/datasharing) sets tiers by "Charities reached" (0–250 to 50,000+) or transaction volume (under $500K to $500M+). No tier mentions AI, LLMs or redistribution.
  - The developer [terms summary](https://developer.charitynavigator.org/termsofuse) says "You may not sublicense, sell, or redistribute API data." and "All derived products must include attribution to Charity Navigator."
  - The [API Terms](https://www.charitynavigator.org/products-and-services/api/) ("Last updated October 2026") contain 0 matches for AI, artificial intelligence, LLM, language model, machine learning or train. This agrees with b43n26-03 §2.1.
- **Changelog.** The [changelog](https://developer.charitynavigator.org/changelog) has 4 entries, from 2026-04-07 (beacons deprecated) to 2026-10-07 (alert fields). None mentions AI.
- **Customer stories.** Only Givelink (CNAI-04) mentions AI. The RoundUp story does not. The stories index names "Donor-advised fund platforms" as a target segment but lists no DAF customer.
- **Perplexity media mention.** It was not found on any page fetched. The press room's "Charity Navigator in the News" list is rendered by script and was empty in the static HTML. It stays [S] (queue P-B43N26-0304-05).
- **Pricing.** The [pricing page](https://developer.charitynavigator.org/pricing) is rendered by script, and its static HTML holds no plan text.

### 3.4 Excluded (outside scope or window)

- **Carefull release (2024-05-15).** It is outside 2025–2026. Its AI wording ("proprietary financial monitoring AI") is Carefull's boilerplate.
- **Anthem Awards release (2026-11-05).** "AI" appears only in the Webby Awards boilerplate.
- **"Getting Started With AI"** (nonprofit resources; page metadata datePublished 2026-06-11). It is generic advice to nonprofits about donor-prediction AI, not about use of CN data.

### 3.5 Reading [I]

- **CN's AI channel is partnership-led.** It runs through Giving Compass, which powers CN's own search, and through API licensees that are AI-branded (Allegory) or plan AI (Givelink).
- **CN has not published:**
  - an MCP server;
  - an AI-host distribution tier;
  - AI terms.
- **The (a) cell stays as it is.** The b43n26-03 matrix cell (a) (requires-licence) still stands, since no public CN statement licenses display in third-party AI hosts.
- **Contrast with peers.** Candid (AIP22) and Pledge (AIP31 proposed) run their own MCP channels, and CN does not.

---

## 4. Limits

1. **MCP endpoint not called.** Pledge's MCP auth method, tool input schemas, any `readOnlyHint`/`destructiveHint` annotations and any server-side confirmation are unknown. This is why the reading is provisional AMBER (RED-boundary) and not RED or a plain AMBER.
2. **Mapping inferred.** The link between MCP tools and REST operations is inferred from matching names and descriptions.
3. **Pledge's legal terms not read.** Pledge's API terms are private (b43n26-03 §2.4). Its charitable entity and any variance power were not read.
4. **Undated Pledge docs.** No launch date for the MCP server was found.
5. **Script-rendered CN pages.** The pricing page and the press-room news list are rendered by script and their content was not read.
6. **CN site terms (compliance note).** CN's website Terms of Use (2022-11-01, quoted in b43n26-03 §2.1) bar "data mining, robots, or similar data gathering and extraction methods". This run made 27 scripted requests to www.charitynavigator.org: robots, sitemaps, the 18 press releases and 4 pages. They were read as documentation, as earlier batches did, but the shared rule says to stop fetching where terms forbid automated extraction. No further requests were made, and the caller should decide whether these reads are acceptable. developer.charitynavigator.org is governed by the API terms, which have no such clause on reading docs.
7. **Single scorer, no second read.** The Pledge reading needs a blind re-score (§5).
8. **Window.** Only 2025–2026 statements were collected for CN. Earlier items are excluded or labelled as context.

---

## 5. Data dictionary: `pledge-mcp-cn-ai-2026-11-20.csv`

**Census columns.** The first 24 columns match `philanthropy-ai-products-2026.csv` exactly, so the Pledge row can be appended later. The census columns are `product_id` through `repo_crossref`. For the `cn_ai_statement` rows, census fields that do not apply are `n/a`.

| Column | Meaning |
|---|---|
| product_id | `AIP31 (proposed)` for Pledge. `CNAI-nn` for CN statement rows. |
| vendor | Vendor, partner or licensee named in the source. |
| segment | Market segment. |
| product_name | Product or item the statement concerns. |
| launch_date | Launch or statement date (YYYY-MM-DD), or `undated`. |
| launch_basis | Where the date comes from. |
| status | live, announced, roadmap, or n/a. |
| functions | Short function tags. |
| what_it_does | Summary. Quotes are in single quotes. |
| money_moving | Whether an AI-reachable action moves money, with evidence. |
| status_changing | Whether an AI-reachable action changes records or status. |
| human_approval_documented | Approval or confirmation step documented by the vendor. |
| audit_log_documented | Audit or activity trail documented. |
| data_training_statement | Model-training or data-use statement. |
| admin_opt_in | Admin enablement model. |
| pricing_published | Published pricing. |
| ai_overlay | §7a.2 product-level reading (census row only). |
| overlay_basis | Reason for the reading. |
| evidence_tag | F = primary page read on 2026-11-20. |
| source_url | Primary URL. |
| secondary_url | Further primary URLs, separated by ` ; `. |
| source_date | Date printed on the source, or `undated` with a note. |
| accessed | Date read. |
| repo_crossref | Related repo files and rows. |

**Extra columns:**

| Column | Meaning |
|---|---|
| record_type | `census_row` (Pledge) or `cn_ai_statement`. |
| first_party | `yes`; `yes (CN-published; customer's plan)`; or `no (partner)`. |
| ai_category | MCP server; AI partner; customer AI use; governance context. |
| statement_verbatim | Exact quote from source_url, checked by script. |
| tools_listed | All MCP tools in the tool reference, separated by `; ` (Pledge only; 17). |
| auth_documented | Authentication documented (Pledge only). |
| confirmation_documented | Per-call confirmation or idempotency documented (Pledge only). |
| limits_documented | Caps or limits documented (Pledge only). |
| intended_user | Intended user (Pledge only). |

**Queue file.** `queue-proposals-b43n26-03-0304.csv` uses the header of `queue-proposals-gap19-13.csv` and has 6 rows.

---

## 6. Source register

| ID | Source | Date | URL | Tag |
|---|---|---|---|---|
| S1 | Pledge MCP setup guide ("AI / MCP Integration") | undated | https://developer.pledge.to/guides/mcp/ | F |
| S2 | Pledge MCP Tool Reference | undated | https://developer.pledge.to/reference/mcp/ | F |
| S3 | Pledge API Reference, OpenAPI source (v1.0.1) | undated | https://developer.pledge.to/api.yaml (rendered at https://developer.pledge.to/api/) | F |
| S4 | Pledge Getting Started | undated | https://developer.pledge.to/guides/getting-started/ | F |
| S5 | Pledge Point Redemption guide (flow of funds, fees) | undated | https://developer.pledge.to/guides/point-redemption/ | F |
| S6 | PledgeAI product page (context; no MCP wording) | undated | https://www.pledge.to/solutions/pledge-ai | F |
| S7 | CN press release, Horizon AI Search | 2025-11-24 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-launches-ai-horizon-search/ | F |
| S8 | CN press release, Allegory | 2026-05-18 | https://www.charitynavigator.org/about-us/press-release/allegory-integrates-cn-api/ | F |
| S9 | CN press release, board expansion | 2025-07-15 | https://www.charitynavigator.org/about-us/press-release/charity-navigator-expands-board/ | F |
| S10 | CN developer portal, Givelink customer story | undated (modified 2026-11-17) | https://developer.charitynavigator.org/customerstory-givelink | F |
| S11 | CN developer portal, customer stories index | modified 2026-11-17 | https://developer.charitynavigator.org/customerstories | F |
| S12 | CN developer portal, changelog | 2026-04-07 to 2026-10-07 entries | https://developer.charitynavigator.org/changelog | F |
| S13 | CN developer portal, Usage & Quotas | modified 2026-11-17 | https://developer.charitynavigator.org/plans | F |
| S14 | CN developer portal, Data Sharing Requirements | modified 2026-11-17 | https://developer.charitynavigator.org/datasharing | F |
| S15 | CN developer portal, Terms of Use summary | modified 2026-11-17 | https://developer.charitynavigator.org/termsofuse | F |
| S16 | CN API Terms of Use | October 2026 | https://www.charitynavigator.org/products-and-services/api/ | F |
| S17 | CN press room (news list script-rendered) | n/a | https://www.charitynavigator.org/about-us/press-room/ | F |
| S18 | Giving Compass API launch release | 2026-01-20 | https://www.givingcompass.org/giving-compass-launches-api-to-enable-smarter-philanthropy-where-giving-decisions-are-made/ | F |
| S19 | CN press releases checked with no AI statement in window | 2022–2026 | 18 URLs under https://www.charitynavigator.org/about-us/press-release/ (from post-sitemap.xml) | F |
