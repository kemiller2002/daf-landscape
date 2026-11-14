# Sponsor data rights and agent controls (queue items Q-N04 and Q-N05)

**Date:** 2026-11-14 · **Queue items:** Q-N04 (entrant strategy), Q-N05 (AI governance), from `data/mission-2026-11-14/research-priority-queue.csv` · **Datasets:** `data/mission-2026-11-14/vendor-data-rights-matrix.csv`, `data/mission-2026-11-14/agentic-integration-controls.csv`

**How this was done.** Public documents only: published contract templates, terms of use, developer documentation and press releases. No account was created and no write call was made. Every contract below is a **public template or generic terms**. None is an executed customer contract. Each template lets a signed order form, work order, SOW or customer agreement override it, so a negotiated contract can differ. Clause quotes are verbatim and 40 words or fewer. "Not publicly documented" means the item was searched for and not found. It does not mean the item does not exist.

**Builds on:** `research/ren-legal-entities-public-msa-contract-portability-audit-2026-11-12.md`, `research/ren-iphi-platform-contract-architecture-integration-audit-2026-11-12.md`, `data/ren-public-contract-clauses-2026.csv`, `research/migration-runbook-2026.md`, `research/mission-2026-11-14/ai-native-entrant-simulation.md` (including its governing red-team corrections) and `research/mission-2026-11-14/ai-governance-failure-modes.md`.

---

## 1. Answers

### Q-N04: Do sponsor–vendor contracts give sponsors API access and data-portability rights?

**Answer (medium confidence): sponsors own their data, but no public incumbent template gives them a right to plug in a third-party operating layer. Live access needs the vendor's consent. Batch access through sponsor-run exports does not.**

1. **Ownership is usually with the sponsor.**
   - Ren's general MSA: "Customer will own the Customer Materials" (§5.1, [RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf)).
   - iPhi: "Customer owns all right, title, and interest in and to all Customer Content" ([iPhi MSA](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx)).
   - NPact: "Customer shall retain and own all right, title and interest in and to the Customer Data" (§6.2, [NPact Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/)).
   - TIFIN: Provided Content belongs to "Client or you" (§8, [TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)).
2. **Export rights are narrow, and none of these templates includes an API right.**
   - Ren returns only materials the customer *provided*, not records the platform generated (§4.5/§5.1, [RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf)).
   - iPhi makes Customer Content available for **15 days** after termination ([iPhi MSA](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx)).
   - NPact lists "data import and export" as a paid Professional Service and deletes hosted data **10 business days** after hosting ends (§1, §4.4(b), [NPact](https://npact.com/software-as-a-service-license-and-services-standard-terms/)).
   - TIFIN's generic terms bar users from archiving or downloading (§5.3, [TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)).
3. **Several templates actively restrict third-party access.**
   - **NPact §2.4 is an explicit ban.** It was added in August 2025 ([NPact](https://npact.com/software-as-a-service-license-and-services-standard-terms/)).
   - iPhi bars use "for the benefit of a third party" and competitive use ([iPhi MSA](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx)).
   - TIFIN bans robots and automated access, and bans publishing benchmarks (§5.3, §7(e), [TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)).
   - Foundation Source's site terms exclude competitors ([FS ToU](https://foundationsource.com/terms-of-use/)).
4. **Where incumbent APIs exist, the vendor gates them.**
   - Ren sells "API Integration Services" as a one-time add-on ([Ren Product Descriptions](https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf)).
   - Foundant's API is a purchased add-on ([Foundant Integrations](https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations), search-indexed text; the page returned 403 to automated fetch).
   - Give Interactive advertises an "open API platform" but publishes no documentation. Its client commitments sit in client MSAs ([Give Interactive](https://www.giveinteractive.com/); [ToS](https://www.giveinteractive.com/terms-of-service)).
   - Foundation Source calls DAF OS "programmable" but publishes no API documentation ([DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/)).
5. **API-first players publish full read/write APIs, but under their own terms.** These are Daffy ([docs](https://docs.daffy.org/getting-started)), Endaoment ([docs](https://docs.endaoment.org/llms.txt)) and Chariot ([docs](https://docs.givechariot.com/v2026-04-01/guides/oauth.md)). Access still needs Endaoment client registration or a partner contract, Chariot onboarding ("OAuth access is not self-service"), or a member's personal Daffy key.

**What this means for an entrant without vendor consent:**
- **Possible:** batch access. The sponsor exports its own data and hands it to the entrant. This rests on the sponsor's ownership, Ren's return-on-request right, and in-product exports such as Foundant's CSV.
- **Not possible:** live read/write integration into the grant queue on Ren, iPhi, NPact or TIFIN under their public templates. On NPact the terms expressly forbid it.

**Q-N04 changes the strategy:** S3, as currently framed, depends on vendor consent. See §5.

### Q-N05: What do TIFIN Louise and Daffy MCP actually enforce?

**Answer (high confidence on what is documented):**
- **Daffy documents:**
  - OAuth sign-in or a full-power API key
  - destructive-tool annotations that the client may or may not honour
  - a CLI `[y/N]` prompt that an agent can skip with `--yes`
  - a $10 minimum
  - activity visible in the app
  - key revocation
  - Daffy's own accept/reject step after submission
- **Daffy does not document:** spend limits, scopes, read-only keys, rate limits, server-side confirmation, or agent identity on donations ([MCP](https://docs.daffy.org/agents/mcp); [agents](https://docs.daffy.org/agents); [CLI](https://docs.daffy.org/agents/cli); [donations API](https://docs.daffy.org/ref/donations); [auth](https://docs.daffy.org/auth)).
- **TIFIN Louise:** TIFIN publishes no controls for Louise. The launch release says it is "designed to ... execute real donor requests" ([PR Newswire, 2025-10-27](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)). TIFIN's AI terms describe only "insights" ([TIFIN Terms §19](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)).
- **Sponsor approval survives in both cases.** Daffy accepts or rejects each donation. TIFIN Give grants are "reviewed and approved" before payment ([granting FAQ](https://intercom.help/give-ria/en/articles/10670838-granting-faqs)).
- **Better patterns already exist.** Endaoment's API requires idempotency keys, offers cancellation while a grant is pending, and keeps Endaoment's review in the loop. Chariot's disbursement approvals record `approved_by` and `approved_at`, and DAFpay leaves the sponsor's review in place. Every.org and Candid expose no money-moving tools.

---

## 2. Q-N04 vendor findings

### 2.1 Ren: general MSAs (RAC and RCF templates, June 2023, posted August 2025)

Source: [RAC MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf). The [RCF MSA](https://www.reninc.com/wp-content/uploads/2025/08/Online-RCF-MSA_v1.pdf) has the same §4.4, §4.5 and §5.1 structure with "RCF" in place of "Ren".

| Topic | Clause (verbatim, ≤40 words) | Reading |
|---|---|---|
| Ownership (§5.1) | "Any materials provided by Customer to Ren ('Customer Materials') will be used and disclosed solely as required to perform the Services. Customer will own the Customer Materials." | Ownership covers what the customer *provided*. The MSA is silent on records Ren generates, such as approvals, audit logs and reconciliations. |
| Return (§4.5) | "Upon the termination of this Agreement, or upon Customer's earlier request, Ren will deliver to Customer all Customer Materials … that are in Ren's possession or control." | A return-on-request right exists **before termination**. No format, schedule, fee or API is specified. |
| Transition (§4.4(a)) | "the parties will cooperate to effect an orderly, efficient, effective, and expeditious termination of the parties' respective activities under the terminated Work Order" | A general duty to cooperate. It does not require transition assistance or set a price for it. |
| Termination fee (§4.4) | "Customer will pay to Ren the amount of Services Fees, calculated through the end of the calendar quarter during which the Work Order is terminated" | Applies to customer termination other than for Ren's uncured breach. The cost is capped at the end of the quarter, but the template allows Work Order overrides. |
| Third-party access (§6) | "neither party shall use, disclose or allow any third-party access to any such confidential information, except as permitted by this Section 6." | Ren's confidential information explicitly includes "software/hardware … documentation, procedures". An entrant could therefore use exported customer data but not Ren's systems or documentation. |
| APIs | Not in the MSA. Ren's product descriptions list "API Integration Services- a one-time service to facilitate API setup between DFX and a compatible client platform" and a separate "Data Migration" add-on ([Ren Product Descriptions](https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf)). | API access is a paid professional service that Ren chooses whether to offer. |

*Naming caution:* a search for "Ren API" returns documentation for a different company, Ren Systems (news intelligence, hosted on Notion). Do not attribute it to Ren the DAF company.

### 2.2 Ren iPhi platform MSA (Final Draft 2023-06-20 v2, .docx; the earlier PDF URL now returns 404)

Source: [iPhi MSA .docx](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx). Section numbers follow the repo's prior audit.

| Topic | Clause (verbatim, ≤40 words) | Reading |
|---|---|---|
| Ownership (§3.2) | "As between Ren and Customer, Customer owns all right, title, and interest in and to all Customer Content." | Customer Content means "any information Customer enters or submits into, or transmits through, the Platform". |
| Ren's data rights (§3.2) | "Customer grants Ren a perpetual, irrevocable, worldwide, fully paid up, royalty-free right and license to access and use Customer Content in an Anonymized manner for any lawful purposes" | Ren can use anonymized data for benchmarking. |
| Third-party restriction (§3.4) | Customer shall not "permit or enable any third parties to … (c) use the Services for purposes of a third party or otherwise for the benefit of a third party; or (d) … creating a product or service commercially competitive" | **Directly limits an entrant.** A third-party operating layer using iPhi credentials risks breaching (c) and, if it competes, (d). |
| Termination data (§10.5) | "Ren will make available to Customer all Customer Content in an industry-standard format for fifteen (15) days, provided that after such period Ren shall have no obligation to continue to maintain Customer Content" | The only explicit export right is at exit. The format is unspecified. |
| Fees | "all Fees are non-cancelable and non-refundable" (fees clause); remaining-term fees fall due "if this Agreement is terminated by Ren pursuant to Section 10.2" | The cross-reference to §10.2 appears to point to the renewal clause, so its meaning needs legal reading. The template has no termination for convenience: "The Term may be terminated only as permitted in this Section 10." |
| Renewal | Order forms renew for 12 months unless notice is given "at least thirty (60) days prior" | This drafting inconsistency was already noted in the repo audit. |
| APIs | No API right. The product sheet lists a GuideStar API, DocuSign API, SSO and "Data exchanges with trust accounting systems" ([iPhi Product Descriptions](https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Product-Descriptions-v1.pdf)). | These are integrations into iPhi. None is an external access API. |

### 2.3 NPact (FIMS, DonorCentral, Foundation Cloud): Standard Terms, last updated 2025-08-26

Source: [NPact SaaS Standard Terms](https://npact.com/software-as-a-service-license-and-services-standard-terms/). The terms are "incorporated into and made part of each NPact Agreement to Purchase". They prevail over SOWs unless a section is expressly amended (§19).

| Topic | Clause (verbatim, ≤40 words) | Reading |
|---|---|---|
| Change note | "NPact does not authorize third parties to give donors access to our platform." | The August 2025 change summary on the same page. |
| **§2.4 External Passthrough** | "NPact does not authorize Customer or its … donors … vendors … or agents to access the Services or Software through third-party products or applications or initiate and/or authorize any actions including … donations, grants, transfers … or payments" | **The strongest anti-integration clause found.** It covers agent and third-party-initiated grants. |
| §2.4 continued | "NPact authorizes access to the Services or Software and any NPact product only by accessing such products by direct login through the NPact Software." | Screen-scraping or an agent driving a browser would also fall outside what NPact authorizes. |
| Ownership (§6.2) | "As between NPact and Customer, Customer shall retain and own all right, title and interest in and to the Customer Data." | Customer Data includes "all content, data and information recorded and stored by Software for Customer", which is broader than Ren's definition. |
| Data at exit (§4.4(b)) | "After the date NPact stops hosting Software for Customer, Customer Data is held for ten (10) business days, after which the Customer Data is deleted" | No export duty at exit. Export is a Professional Service (§1 definition). |
| Term (§8.1) | Three-year initial term, one-year renewals, notice "at least ninety (90) days prior" | |
| Fees on exit (§8.5) | On specified terminations, "all Fees that would have become payable had each outstanding Statement of Work remained in effect until expiration of its current Term will become immediately due" | Possibly a full remaining-term charge. |

### 2.4 TIFIN Give: TIFIN Terms and Conditions (dated 2025-02-19, published on the TIFIN Give help centre)

Source: [TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use). The older URL `tifin.com/terms-conditions/` cited in the repo now returns 404.

- **Ownership (§8):** "all right, title and interest in Provided Content belong to and are retained solely by Client or you, as applicable."
- **Download and automation (§5.3):** users "agree not to archive, download, reproduce, distribute …" and not to "use any robot, spider, scraper or other automated means to access the Services".
- **Benchmarks (§7(e)):** users may not "disclose to third parties any benchmark or competitive evaluation of the Services".
- **API:** "Services" includes "any application programming interface and related software" (§17.5(i)). No public API documentation was found.
- **Override:** a customer "Software & Services Agreement may supersede these Terms and Conditions" (§1). If it does, "such Software & Services Agreement shall govern" (§16.9).
- **Data loss:** "the Company Group has no responsibility or liability for the deletion or failure to store any data" (§13.1).
- **Transition and exit fees:** not publicly documented. The repo's migration runbook test M16 remains unexecuted (`research/migration-runbook-2026.md`).

### 2.5 Foundation Source (DAF OS)

- The [DAF OS brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/) describes "a complete, programmable administration platform for DAF-sponsoring public charities" with "automated money movement, programmatic grantmaking, and real-time fund visibility". **No public API documentation, sponsor contract, export clause or termination term was found.** "FundOS" in search results belongs to Superstate ([Markets Media](https://www.marketsmedia.com/superstate-introduces-fundos-to-bring-funds-onchain/)). The repo notes that Foundation Source's site uses the DAF OS and FundOS names inconsistently.
- **Inbound only:** custodial data arrives through BridgeFT's API ([BridgeFT release](https://www.bridgeft.com/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/)).
- **Site terms (2026-01-12):** users must "not [be] a competitor of Foundation Source and are not using the Services for reasons that are in competition with Foundation Source, unless otherwise explicitly authorized" ([FS ToU](https://foundationsource.com/terms-of-use/)).

### 2.6 Give Interactive

- **Marketing claim:** the site says "Our open API platform ensures your team can push and pull data to all your platform tools" ([Give Interactive](https://www.giveinteractive.com/)). The Vanguard Charitable release (2025-11-04) cites a "cloud-native, API-first architecture" ([PR Newswire](https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html)).
- **Site terms (updated 2026-07-23):** "Give Interactive's commitments to our clients and their donors are communicated through Service Level Agreements (SLAs) or Master Service Agreements (MSAs)" ([ToS](https://www.giveinteractive.com/terms-of-service)). No MSA is public.
- **Not publicly documented:** API documentation, data ownership, export and termination terms.

### 2.7 Foundant CommunitySuite

- **API:** an optional, purchased "API connections" add-on. Its documentation becomes visible in the product under System Data > Integrations, and an authorized user must be designated ([Foundant Integrations](https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations), from search-indexed text).
- **Exports:** CSV, PDF and Excel report exports are documented in the help centre ([CommunitySuite Reporting](https://support.foundant.com/hc/en-us/sections/4665468682263-CommunitySuite-Reporting)).
- **Not publicly documented:** license terms, ownership, termination and API object list.

### 2.8 Blackbaud Financial Edge NXT (SKY API)

- **Access:** "your organization's administrator must also perform an admin-level action within the system to enable this connector". The connector operates "in the context of your user account" ([Microsoft connector docs](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera)).
- **Write operations:** create, update, validate, post and delete journal-entry batches.
- **Throttle:** 100 calls per 60 seconds per connection (same source).
- **Relevance:** this is the most open documented path into a sponsor's **general ledger**, but it is not a DAF subledger. Community posts give conflicting figures for SKY API daily quotas ([Blackbaud Community](https://community.blackbaud.com/discussion/comment/279419)). Those figures are not verified.

### 2.9 API-first players: Chariot, Endaoment, Daffy, Givinga

- **Chariot**
  - Scopes are `resource:read` and `resource:write`, and "OAuth access is not self-service" ([Chariot OAuth](https://docs.givechariot.com/v2026-04-01/guides/oauth.md)).
  - Its FDX v6 API gives read-only account data for up to 24 months, with statements as PDF, CSV or BAI2. It requires credentials from support and IP allow-listing ([Chariot FDX](https://docs.givechariot.com/v2026-04-01/fdx/introduction.md)).
  - **DAFpay inverts the usual direction.** The DAF provider must expose Get Donor, List Funds, Create Grant (idempotent) and Get Grant Status, and "Chariot does not bypass your compliance process" ([DAFpay endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md)). This is a working, sponsor-controlled template for third-party grant initiation.
- **Endaoment**
  - Donors authorize through OAuth with PKCE. Server-to-server partners use API keys.
  - The partner "Submit settled grant" call is "Authorized by the tech-platform API key alone — no donor bearer token or acting-user context required" ([Endaoment docs index](https://docs.endaoment.org/llms.txt)).
  - Partner tiers are priced publicly ([Endaoment institutions](https://endaoment.org/institutions)).
- **Daffy**
  - Personal API keys let a member read and write their own fund ([Daffy getting started](https://docs.daffy.org/getting-started)).
  - Daffy is its own sponsor, so this is not a sponsor–vendor channel.
- **Givinga**
  - Only site terms are public, and they ban "robot, spider, scraper or other automated means" ([Givinga terms](https://www.givinga.com/terms-and-conditions)).
  - API claims appear only in third-party directories ([SourceForge](https://www.sourceforge.net/software/product/Givinga)).

### 2.10 Matrix summary

Full detail, with columns documented below, is in `data/mission-2026-11-14/vendor-data-rights-matrix.csv`.

| Vendor | Data owner | Export right | Public API | Third-party access | Exit fee (template) | Entrant access without vendor consent |
|---|---|---|---|---|---|---|
| Ren RAC/RCF | Customer (provided materials) | On request or at termination; scope narrow | No (paid add-on) | Confidentiality bars third-party access to Ren information | Through end of quarter | Batch only |
| Ren iPhi | Customer (content entered) | 15 days after exit | No | Bars third-party-benefit and competitive use | Non-cancelable fees | Batch at exit only |
| NPact | Customer (broad) | Paid SOW; deleted 10 business days after exit | No | **Express ban (§2.4)** | Remaining SOW fees on some exits | No |
| TIFIN Give | Client/user | Not documented; download restricted | No public docs | Ban on automated access; no benchmarks | Not documented | No (generic terms) |
| Foundation Source | Not documented | Not documented | No | Competitors excluded (site ToU) | Not documented | Unknown |
| Give Interactive | Not documented | Not documented | Claimed, undocumented | In client MSA | Not documented | Unknown |
| Foundant | Not documented | In-product CSV/PDF | Paid add-on | Not documented | Not documented | Batch yes; API if purchased |
| Blackbaud FE NXT | Not documented | API | Yes | Admin must connect | Not documented | Yes, once the sponsor's admin connects |
| Chariot / Endaoment / Daffy | Platform terms | API | Yes | Registration or partner contract | n/a | Through the vendor's own published terms |
| Givinga | Not documented | Not documented | No | Site bans scrapers | Not documented | Unknown |

---

## 3. Q-N05 agent-control findings

### 3.1 Daffy MCP server, CLI and REST API

| Control | What Daffy documents | Source |
|---|---|---|
| Write tools | `make_donation` ("Moves real money") and `cancel_donation` ("Permanent"), among 9 tools "scoped to your fund" | [MCP](https://docs.daffy.org/agents/mcp) |
| Authentication | "Sign in with Daffy" ("no key to paste") or an API key sent as `Authorization: Bearer daffy_production_...` | [MCP](https://docs.daffy.org/agents/mcp) |
| Key power | "Treat an API key like a password: it can move money in your fund." | [MCP](https://docs.daffy.org/agents/mcp) |
| Scopes / read-only keys / expiry | **Not documented** | [auth](https://docs.daffy.org/auth) |
| Spend limits | **Not documented.** The only bound is the fund balance ("how much you can donate right now"); the minimum is $10 | [MCP](https://docs.daffy.org/agents/mcp); [donations](https://docs.daffy.org/ref/donations) |
| Confirmation (MCP) | Money tools "are annotated as destructive, so clients that honour tool annotations ask you to approve them before they run." | [agents](https://docs.daffy.org/agents) |
| Confirmation (CLI) | Commands wait for a `[y/N]` answer. "Pass `--yes` to skip the prompt, and only once the member has explicitly confirmed." | [CLI](https://docs.daffy.org/agents/cli) |
| Confirmation (API) | None documented | [donations](https://docs.daffy.org/ref/donations) |
| Sponsor approval | Donations can be cancelled unless "accepted or rejected by Daffy". Statuses include `approved` and `rejected` | [donations](https://docs.daffy.org/ref/donations) |
| Audit | "anything your assistant does shows up in the Daffy app like any other activity"; the keys page shows "the time it was last used" | [MCP](https://docs.daffy.org/agents/mcp); [auth](https://docs.daffy.org/auth) |
| Agent identity | Only that "you'll usually see the name when it asks for permission". The donation body has no agent field | [MCP](https://docs.daffy.org/agents/mcp); [donations](https://docs.daffy.org/ref/donations) |
| Rate limits | **Not documented** | all pages above |
| Idempotency | Not documented. The CLI warns that timed-out writes "may or may not have gone through" | [CLI](https://docs.daffy.org/agents/cli) |
| Third-party wrappers | Daffy connectors are listed by Composio and Pipedream. These hold user keys outside Daffy's control | [Composio](https://mcp.composio.dev/daffy); [Pipedream](https://pipedream.com/apps/daffy.md) |

**Assessment.** All confirmation is enforced on the client side or by instructions to the agent. The server documents no limit, scope or step-up check. The control that remains is the sponsor's own accept/reject, which happens *after* the agent submits. This confirms failure modes F06 and F16 in `research/mission-2026-11-14/ai-governance-failure-modes.md`, with one refinement: Daffy's sponsor review does sit between agent submission and payment.

### 3.2 TIFIN Give Louise

- **Claimed capability:** "designed to drive actionability and execute real donor requests within the charitable experience". The release's examples include "Set up a monthly recurring $100 grant to the Wounded Warrior Project", "Contribute 100 shares of NVDA stock to my DAF" and "Add one of my children to my DAF" ([PR Newswire, 2025-10-27](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)). The release mentions no limits, confirmations, audit or approvals.
- **Terms:** §19 calls the AI Assistant a tool that "analyze[s] financial data and generate[s] insights", and says insights "undergo a compliance check" for investment advice. **No clause covers executing transactions** ([TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)). §1.6 makes users "solely responsible for all activity that occurs under your account".
- **Downstream controls that apply to all grants:**
  - minimum grant of $50
  - "Grant recommendations are reviewed for available funds"
  - pending grants can be cancelled, but a grant "may not be reversed once it's been approved and begun to process"

  Source: [granting FAQ](https://intercom.help/give-ria/en/articles/10670838-granting-faqs).
- **Gap:** no public documentation describes Louise's action path, confirmation step, limits or logs. Answering this needs a demo or customer documentation.

### 3.3 Other integrations

| Integration | Write capability | Key control evidence |
|---|---|---|
| Endaoment API | Yes: async grants, transfers, pledges, fund creation | Endaoment reviews grants and performs due diligence ([recommending grants](https://docs.endaoment.org/donors/getting-started/recommending-grants.md)). Grants can be cancelled while `PendingLiquidation`. `idempotencyKey` is required. A per-IP rate limit with a roughly 10-minute ban applies ([error handling](https://docs.endaoment.org/developers/quickstart/error-handling.md)). OAuth scopes are coarse ([login](https://docs.endaoment.org/developers/quickstart/login-user.md)). Separate *Recommendation* objects let a collaborator propose grants for the fund manager to act on ([docs index](https://docs.endaoment.org/llms.txt)), a native draft-then-approve split. |
| Chariot API | Yes: disbursements, grants, grant-request submit/reject | Disbursements can require approval and record `approved_by` and `approved_at` ([approve disbursement](https://docs.givechariot.com/v2026-04-01/api/disbursements/approve-disbursement.md)). Delegated tokens "loses any permission that user's role later loses" ([OAuth](https://docs.givechariot.com/v2026-04-01/guides/oauth.md)). Whether creator and approver must be different people is not documented. Chariot's MCP server is for its documentation ([docs index](https://docs.givechariot.com/llms.txt)). |
| Every.org API | No money movement | "At this time, Every.org does not provide programmatic donations or disbursements via API." ([Every.org docs](https://docs.every.org/docs/intro)) |
| Candid MCP | None | Six tools, all read-only ([Scalekit](https://docs.scalekit.com/agentkit/connectors/candidmcp.md)). Sign-in with a Candid account, free tier included ([Candid blog, 2025-12-02](https://candid.org/blogs/claude-for-nonprofits-candid-mcp-connector-access-nonprofit-data-ai-assistant/)). |
| Blackbaud FE NXT | Ledger writes (journal batches) | Admin enablement, the user's own permissions, validate-then-post steps, `added_by` on batches ([connector](https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera)) |

---

## 4. Implications for AI governance

1. **The only control documented across the market is the sponsor's post-submission approval.** Spend limits, scoped tokens and agent identity are absent from Daffy and undocumented for Louise. The repo's §4.5 state model (agent draft, then donor confirmation, then sponsor approval, then payment instruction, then settlement) is currently enforced only at the sponsor approval step.
2. **Confirmation enforced by the client is not a control a sponsor can audit.** Daffy's safeguards depend on the MCP client honouring annotations and on the agent not passing `--yes`. Due-diligence questions should ask for confirmation enforced on the server.
3. **There are reference designs to adopt:** Chariot's recorded approver and role-bound delegated tokens, Endaoment's idempotency keys, cancel window and Recommendation objects, and DAFpay's rule that the third party "does not bypass" sponsor compliance.
4. **NPact §2.4 is the first vendor term found that pre-emptively bans agent- or third-party-initiated grants.** Other vendors may copy it. That would protect sponsors, and it would also lock out entrants.

## 5. Implications for entrant strategy

1. **S3, the operating layer, is gated.** On iPhi and NPact the template terms prohibit the deep, live integration S3 needs. On Ren and TIFIN the templates are silent or restrictive. Every route goes through a vendor work order or customer agreement. This confirms the risk the simulation flagged ("Data access is gated by incumbent vendors"). Public contract evidence now supports it.
2. **Routes that work without vendor consent:**
   - (a) sponsor-run batch exports of data the sponsor owns, which suits periodic reconciliation and monitoring but not real-time grant queues
   - (b) a sponsor's own general ledger via Blackbaud SKY once the sponsor's admin connects the app
   - (c) public data such as IRS BMF and Candid.
3. **Routes that need consent but are documented and open:** Endaoment partner APIs, Chariot OAuth/DAFpay, and Daffy member keys. This supports the S1-lite fallback the simulation names: partner with an API-first sponsor.
4. **Use contract terms as a buying criterion.** Target sponsors whose renewal falls within 12 months. Ren's templates allow return of materials on request and end-of-quarter exit fees. iPhi offers a 15-day exit window. NPact has a three-year term and 90-day notice. Make "API access for a sponsor-designated agent" a clause the sponsor asks for at renewal (see the questionnaire in `research/ren-legal-entities-public-msa-contract-portability-audit-2026-11-12.md`).
5. **Watch the benchmarking bans.** TIFIN §7(e) and the iPhi competitive-use clause limit published head-to-head evidence. This matches the repo's migration-runbook caveat on TIFIN and Chariot terms.

## 6. Open questions

- Executed sponsor contracts (Ren work orders, TIFIN Software & Services Agreements, Give Interactive and Foundation Source MSAs): do they add API or export rights?
- Louise's action path: does it create grants directly or draft them for donor confirmation? What limits and logs apply?
- Daffy: are there undisclosed server-side limits, velocity checks or agent tagging?
- Chariot: can disbursement approval rules require an approver different from the creator?
- Foundant API object list and license terms. Whether NPact §2.4 has been negotiated away in any signed agreement.

## 7. Source register

| ID | Source | URL | Date / version |
|---|---|---|---|
| C01 | Ren RAC MSA (template) | https://www.reninc.com/wp-content/uploads/2025/08/Online-RAC-MSA_v1.pdf | June 2023; posted 2025-08 |
| C02 | Ren RCF MSA (template) | https://www.reninc.com/wp-content/uploads/2025/08/Online-RCF-MSA_v1.pdf | June 2023; posted 2025-08 |
| C03 | Ren iPhi Platform MSA .docx | https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Platform-MSA-Final-Draft-2023-06-20v2.docx | 2023-06-20 v2 |
| C04 | Ren Product Descriptions | https://www.reninc.com/wp-content/uploads/2025/08/Ren-Inc.-Product-Descriptions-v.1.pdf | v1 |
| C05 | Ren iPhi Product Descriptions | https://www.reninc.com/wp-content/uploads/2025/08/Ren-iPhi-Product-Descriptions-v1.pdf | v1 |
| C06 | Ren agreement library | https://www.reninc.com/master-service-agreements/ | accessed 2026-11-14 |
| C07 | NPact SaaS Standard Terms | https://npact.com/software-as-a-service-license-and-services-standard-terms/ | 2025-08-26 |
| C08 | TIFIN Terms and Conditions | https://intercom.help/give-ria/en/articles/10092486-terms-of-use | 2025-02-19 |
| C09 | TIFIN Give granting FAQ | https://intercom.help/give-ria/en/articles/10670838-granting-faqs | accessed 2026-11-14 |
| C10 | Louise release | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html | 2025-10-27 |
| C11 | Foundation Source DAF OS brief | https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/ | accessed 2026-11-14 |
| C12 | Foundation Source Terms of Use | https://foundationsource.com/terms-of-use/ | 2026-01-12 |
| C13 | Give Interactive home and ToS | https://www.giveinteractive.com/ ; https://www.giveinteractive.com/terms-of-service | ToS 2026-07-23 |
| C14 | Vanguard Charitable / Give Interactive release | https://www.prnewswire.com/news-releases/vanguard-charitable-partners-with-give-interactive-to-power-the-future-of-donor-advised-fund-administration-302602790.html | 2025-11-04 |
| C15 | Foundant Integrations / Reporting | https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations ; https://support.foundant.com/hc/en-us/sections/4665468682263-CommunitySuite-Reporting | search-indexed 2026 |
| C16 | Blackbaud FE NXT GL connector | https://learn.microsoft.com/en-us/connectors/blackbaudfenxtgenera | updated 2025-04-24 |
| C17 | Chariot OAuth, FDX, DAFpay, disbursements | https://docs.givechariot.com/v2026-04-01/guides/oauth.md ; https://docs.givechariot.com/v2026-04-01/fdx/introduction.md ; https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md ; https://docs.givechariot.com/v2026-04-01/api/disbursements/approve-disbursement.md | API v2026-04-01 |
| C18 | Endaoment developer docs | https://docs.endaoment.org/llms.txt ; https://docs.endaoment.org/developers/quickstart/error-handling.md ; https://docs.endaoment.org/developers/quickstart/login-user.md ; https://docs.endaoment.org/donors/getting-started/recommending-grants.md | accessed 2026-11-14 |
| C19 | Daffy MCP, agents, CLI, auth, donations | https://docs.daffy.org/agents/mcp ; https://docs.daffy.org/agents ; https://docs.daffy.org/agents/cli ; https://docs.daffy.org/auth ; https://docs.daffy.org/ref/donations ; https://docs.daffy.org/getting-started | accessed 2026-11-14 |
| C20 | Every.org docs | https://docs.every.org/docs/intro | accessed 2026-11-14 |
| C21 | Candid MCP | https://candid.org/blogs/claude-for-nonprofits-candid-mcp-connector-access-nonprofit-data-ai-assistant/ ; https://docs.scalekit.com/agentkit/connectors/candidmcp.md | 2025-12-02 |
| C22 | Givinga terms | https://www.givinga.com/terms-and-conditions | undated |
| C23 | BridgeFT / Foundation Source | https://www.bridgeft.com/foundation-source-elevates-turnkey-daf-platform-with-advisor-branded-multi-custodial-flexibility/ | 2025-09 |
| C24 | Endaoment institutions (partner pricing) | https://endaoment.org/institutions | accessed (repo) |

## 8. Dataset column dictionaries

**`vendor-data-rights-matrix.csv`**

| Column | Definition |
|---|---|
| vendor, product_or_document | Company, and the specific template or document reviewed |
| evidence_type | `unsigned_public_template`, `public_standard_terms_incorporated_in_each_ATP`, `public_terms_of_use`, `public_developer_docs`, `vendor_help_docs`, `marketing_claims_and_site_terms`, `site_terms_only` |
| document_date | Version or posting date stated on the document |
| primary_source_url | Main URL. The notes column may add more |
| data_owner, ownership_clause_ref | Who owns customer data under the document, and the clause |
| export_right, export_format, export_timing_window, export_fee | Contractual or documented export right, its format, when it is available, and any fee |
| public_api_docs, api_access_model | Whether public API documentation exists, and how access is granted |
| api_read_scope, api_write_scope, grant_submission_via_api | Documented API reach |
| third_party_or_automated_access_terms | Clauses permitting or restricting third-party or automated access |
| transition_assistance, termination_fees, renewal_and_notice | Exit terms |
| entrant_access_without_vendor_consent | Analyst judgment (INFERENCE) from the documented terms |
| confidence | high / medium / low, based on how primary and specific the evidence is |
| notes | Caveats and extra URLs |

**`agentic-integration-controls.csv`**

| Column | Definition |
|---|---|
| integration, operator, interface, primary_source_url | What was reviewed |
| auth_method, credential_scoping | How an agent authenticates, and how narrowly credentials can be scoped |
| write_capability, money_moving_actions | Whether writes exist, and which actions move funds |
| per_action_or_period_spend_limit, minimum_amount | Documented amount controls |
| confirmation_requirement, confirmation_enforced_where | The confirmation step, and whether it is enforced by the server, the client, or only by instructions to the agent |
| sponsor_approval_after_agent_submission, cancel_window | Downstream legal and operational checks |
| rate_limit, audit_trail, revocation, idempotency, agent_identity_recorded | Operational controls |
| third_party_wrappers | Non-vendor connectors observed (not reviewed) |
| confidence, notes | As above |

*Not publicly documented* in either file means the item was searched for in the vendor's own public materials on 2026-11-14 and not found.

## Validation corrections (wave 4, 2026-11-14) — governing
Source: [validation-wave4-report.md](validation-wave4-report.md). Where these conflict with the text above, these govern.

- **W4-18** (research/mission-2026-11-14/queue-contract-data-rights-agent-controls.md lines 24, 89): replace "iPhi MSA" → add "(Ren published template, titled 'Final Draft 2023-06-20 v2'; executed customer terms may differ, and Order Forms prevail on conflict)"
