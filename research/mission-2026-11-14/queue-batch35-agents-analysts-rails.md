# Queue batch 35 C: third-party agent wrappers on DAF APIs (P-CON-06), analyst client-only research (P-ANL-11), founder post-mortems (P-FAIL-10), Every.org's rail mix (P-ASR-06), PayPal Grant Payments expiry (P-PAY-06)

**Date:** 2026-11-15.

**Method:** Desk research from public sources, 2021 onward.
- No accounts were created and nothing was logged in to.
- No forms were submitted, no one was contacted, and no API call needing a key was made.
- No credentials found in public pages or packages were used or copied.
- robots.txt was checked for each site before fetching. Where a site barred Anthropic agents (Pinkaloo's blog), it was not fetched. Where it barred a path (Cerulli `/news/`, Google Drive downloads), that path was not used.
- Some pages carry text addressed to AI agents: Composio's toolkit HTML includes sign-up instructions "for AI agents". That text was treated as page content and ignored.

**Read first (including their governing corrections):**
- [ai-governance-failure-modes.md](ai-governance-failure-modes.md)
- [analyst-and-education-landscape.md](analyst-and-education-landscape.md)
- [failed-daf-startups-deep-research.md](failed-daf-startups-deep-research.md)
- [queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md)

Also used: [queue-contract-data-rights-agent-controls.md](queue-contract-data-rights-agent-controls.md) §3.1, [queue-assurance-everyorg-givinga-monitoring.md](queue-assurance-everyorg-givinga-monitoring.md) §2.2, [queue-payment-rails-cluster.md](queue-payment-rails-cluster.md) and [queue-batch33-voids-exports-rails.md](queue-batch33-voids-exports-rails.md).

**Evidence tags:**
- **[F]** fact from a cited source.
- **[C]** calculation from cited inputs.
- **[I]** inference.

**Outputs:**
- [data/mission-2026-11-14/daf-agent-wrappers-2026.csv](../../data/mission-2026-11-14/daf-agent-wrappers-2026.csv): 19 rows, W01–W19.
- [data/mission-2026-11-14/queue-proposals-batch35c.csv](../../data/mission-2026-11-14/queue-proposals-batch35c.csv): P-B35C-01..03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-CON-06** Wrappers | **Daffy is the only DAF platform whose money-moving API is wrapped by third parties.**<br>• Eight wrappers expose Daffy: Composio, Pipedream, Zapier, n8n (generic HTTP), Operator.io, Corsair, Metorial and Keystroke.<br>• At least five of them document a **write action that commits fund money** (Operator.io also re-exposes Composio's Create Gift):<br>  – Pipedream: `daffy-create-donation`, plus an API proxy that reaches any endpoint;<br>  – Zapier: Create Donation and Create Gift;<br>  – Composio: Create Gift;<br>  – Corsair: `gifts.create`;<br>  – Metorial: create and cancel donations.<br>• Each wrapper stores the donor's Daffy key. Daffy documents **no key scopes, no read-only keys, no expiry and no spend limit** [F].<br>• Daffy's own MCP and auth pages mention none of the wrappers. Daffy is demonstrably aware only of Zapier, which its staff built [F].<br>• No third-party wrapper holding credentials was found for Endaoment, Every.org (beyond a nonprofit-side Zapier trigger), Chariot or Givinga. | High on what each listing documents. Medium on absence (indexes searched only). |
| **P-ANL-11** Analysts | **There is client-only research, but none evaluates DAF technology.**<br>• Datos Insights (formerly Aite-Novarica) holds two relevant 2021+ titles:<br>  – *Expanding Delivery of Philanthropic Advisory Across Wealth Management* (2021-09-04), 33 pages, 18 executive interviews. It names Amicus.io, Charityvest, GiveClear, Pinkaloo, RenPSG and TIFIN among 44 firms.<br>  – *Wealth in America, Part 1: The UHNW* (2024-03-20). Its abstract says it sizes "the opportunities for advice and planning in the areas of philanthropy" [F].<br>• Cerulli: the only charity content in its 2024–2026 HNW and WealthTech report abstracts is the $18tn-to-charity projection [F].<br>• Celent's only title is from 2003. Forrester, Gartner and Javelin have none.<br>• Full sitemap enumeration found 1 philanthropy title among 2,509 Datos report URLs and 0 among 789 Cerulli URLs [C]. | High for Cerulli and Datos (sitemaps). Medium for Forrester and Gartner (search only). |
| **P-FAIL-10** Post-mortems | **No first-party founder post-mortem exists for any core DAF-technology exit**: Pinkaloo, Amicus.io, Vennfi, Giving Place and Stellar/iPhi are covered only by acquirer statements and press.<br>First-party accounts with stated reasons exist only in **adjacent** giving startups:<br>• Tyve (founder, 2022): CAC "pretty high"; a "nice to have" for employers; had to sell to both employer and employee.<br>• Momentum (co-founder, 2022): app "did not have PMF"; "struggling with donor acquisition".<br>• Kambeo (2026): "not growing and succeeding".<br>• ioby (board chair, 2024): could not build a sustainable financial future.<br>• Giving Assistant (successor operator, 2023): the cashback model was "not a sustainable or consistent way".<br>• GWWC (2025) retired Hosted Funds over "high operational costs" of grantmaking. | High that these are first-party. Low on generalising to DAFs. |
| **P-ASR-06** Every.org rails | **The fall of the ForGood rail is real, not an artefact of itemisation** [I].<br>• Network for Good is a single recipient. Its annual totals ($0.47m–$2.91m) are far above both itemisation thresholds ($5k and $25k), so threshold changes cannot hide it.<br>• Its share of grants fell from 73.9% (2020) to 1.1% (2024), while the dollar amount fell from $2.45m to $0.47m as grants rose 2.7x [C].<br>• Stripe Connect and PayPal Grants both pay the charity directly, so the 990-PF **cannot split them**. Together with unitemised lines they are 98.9% of 2024 grants [C].<br>• PayPal-family lines are tiny: PPGF $6,201 and "Hyperwallet activity" $283,570, both in 2023 [F].<br>• Every.org sends no checks itself. Checks happen only through ForGood [F]. | High on filings and rules. Stripe/PayPal split: unknown. |
| **P-PAY-06** PayPal expiry | **No sponsor, PayPal or PPGF document publishes how many Grant Payments expire.**<br>Published fallback rules:<br>• NPT: 14 days, then a check.<br>• Every.org: the expired grant returns to Every.org and is reissued on request; the window is not stated.<br>• PayPal: the grantmaker sets the expiry (search snippet; the page returns 403).<br>• PPGF 990 (CY2024): $797.9m in grants to 14,871 charities, with check-language for unenrolled charities but no rail split [F].<br>• Chariot (for comparison): a 5-business-day claim window, then a check. **"94.57% of grant payments made through Chariot are sent electronically" since launch**, which implies about 5.4% by check, all sponsors pooled [C]. | High on rules. No expiry data exists in public. |

---

## 1. P-CON-06: third-party agent wrappers on DAF APIs

### 1.1 What was searched

| Index | Method | Hits for target platforms |
|---|---|---|
| Composio toolkit sitemap ([sitemap](https://composio.dev/toolkits/sitemap.xml)) | Grepped for daffy, endaoment, chariot, every, givinga, donat, charit, candid | `daffy`; also `donately`, `givebutter` (fundraising, out of scope) and `candid_mcp` (read-only) |
| Pipedream app index ([llms.txt](https://pipedream.com/llms.txt), 3,233 lines) plus app slugs | grep; probed `/apps/<slug>` | Daffy only. Endaoment, Chariot, Every.org and Givinga return 404 |
| Zapier app slugs | HTTP status of `/apps/<slug>/integrations` | `daffy` 200, `everyorg` 200. Others 404 |
| n8n integration slugs | same | `daffy` 200 (generic HTTP page). Others 404 |
| Official MCP Registry ([API](https://registry.modelcontextprotocol.io/v0/servers?search=daffy)) | search: daffy, endaoment, every, chariot, givinga, charity, donation, donor | **None** for the five platforms. Daffy's own server is not registered either |
| npm registry search | daffy, endaoment, every.org, chariot, givinga, donor-advised, n8n-nodes-*, mcp-* | Daffy: Corsair, Metorial, Keystroke, Pipedream, `daffy-cli`. Endaoment: first-party CLI; Swear Jar. Every.org: maxnate adapter; GiveReady |
| PyPI | `daffy`, `<name>-mcp` | `daffy` is an unrelated DataFrame library |
| Web search | "daffy MCP", "Every.org MCP", "Endaoment MCP" | Glama results were unrelated (Little Green Light CRM). Vinkius Every.org listing not live |

### 1.2 Daffy: who holds a key and what it can do

| ID | Wrapper | Credential held | Write actions | Controls documented | Source |
|---|---|---|---|---|---|
| W01 | **Composio** | Donor's Daffy API key, pasted once and stored "encrypted". `is_composio_managed: false`, so it is the donor's own key | `DAFFY_CREATE_GIFT` (name, amount) among 12 tools. **No donation tool** | Claims SOC 2 Type II, RBAC, logs and an audit trail. Scope is "Whatever the credentials you connect allow inside Daffy". Advises users to "Keep an approval step in your prompt" | [Composio Daffy](https://composio.dev/toolkits/daffy) (createdAt 2025-12-04, updated 2026-11-06) |
| W02 | **Pipedream** | API key, "Pipedream-managed", sent as `X-Api-Key` | `daffy-create-donation` (amount, causeId, ein, note, privateMemo). The **API proxy** forwards any Daffy endpoint "with the connected user's credentials attached" | Labelled "(Write)" with hint "open-world" only. No limit or confirmation | [app page](https://pipedream.com/apps/daffy.md); [action](https://pipedream.com/apps/daffy/actions/create-donation.md); [source](https://raw.githubusercontent.com/PipedreamHQ/pipedream/master/components/daffy/daffy.app.mjs); [@pipedream/daffy](https://www.npmjs.com/package/@pipedream/daffy) (created 2023-05-25, v0.2.0 2026-06-25) |
| W03 | **Zapier** (built by Daffy staff) | Zapier connection; method not shown on the public page | **Create Donation** (Amount, EIN, notes, User ID); **Create Gift** (Amount, Name, Email, Message). Exposed via Zapier MCP and SDK | "you control which actions your AI can touch". But "Direct API calls to raw endpoints through fetch are not yet subject to org-level app and action restrictions" | [Zapier Daffy](https://zapier.com/apps/daffy/integrations); [Daffy Hackday post](https://www.daffy.org/resources/daffy-api-examples) (2023-06-12, updated 2026-02-20) |
| W04 | n8n | Generic credential in the HTTP Request node | Any method (Post, Delete…) | None | [n8n Daffy](https://n8n.io/integrations/daffy/) |
| W05 | Operator.io | Via "Composio MCP and Pipedream MCP" | Create Gift (same 12-action list) | None. Claims "no API keys to paste", which contradicts W01 | [Operator.io](https://operator.io/integrations/daffy) |
| W06 | Corsair | Developer-held [I] | `gifts.create` (risk "write") | Per-operation read/write label | [@corsair-dev/daffy](https://www.npmjs.com/package/@corsair-dev/daffy) (2026-10-20) |
| W07 | Metorial Slates | Not documented | "Create, list, retrieve, and cancel donations"; gifts | None | [@slates-integrations/daffy](https://www.npmjs.com/package/@slates-integrations/daffy) (2026-10-16) |
| W08 | Keystroke | Not documented | Unknown (no README) | — | [@keystrokehq/daffy](https://www.npmjs.com/package/@keystrokehq/daffy) |
| W09 | `daffy-cli` (Daffy-documented, published from an individual npm account) | Key in `~/.daffy/credentials` or `DAFFY_API_KEY` | donate, cancel, gift create | `[y/N]` prompt; `--yes` skips it. Daffy: use `--yes` "only once the member has explicitly confirmed" | [npm](https://www.npmjs.com/package/daffy-cli); [Daffy CLI docs](https://docs.daffy.org/agents/cli) |

**Daffy's side [F]:**
- Keys are created in profile settings, shown once, listed with "a fragment of each shown and the time it was last used", and revocable ([auth](https://docs.daffy.org/auth)).
- The auth page says nothing about scopes, read-only keys, expiry, OAuth or third parties.
- The MCP page warns that a key "can move money in your fund" and names no third-party connector ([MCP](https://docs.daffy.org/agents/mcp)).
- A gift needs `name` and `amount`, with a minimum of 18. The page does not say whether a gift debits the fund balance ([gifts](https://docs.daffy.org/ref/gifts)).

**Readings [I]:**
1. **A wrapper key is a full-power key.** Daffy keys carry no scope, so Composio's "least privilege" claim cannot apply below the key. The only narrowing is the wrapper's own tool list. Pipedream's proxy and n8n's HTTP node remove even that.
2. **Controls sit with the wrapper, not with Daffy.** The audit trail, RBAC and action allow-lists are the wrapper's. Daffy sees only a donation made with the member's key. Its donation body has no agent field ([prior batch §3.1](queue-contract-data-rights-agent-controls.md)).
3. **Second-order wrapping exists.** Operator.io reaches Daffy through Composio and Pipedream. So a donor's key can sit two vendors away from Daffy.
4. **The gift path is under-examined.** Composio and Operator expose only gifts, which are charity gift cards to a named person. They do not expose donations. A gift may draw on fund money [I], since the Daffy docs do not say.
5. **Sponsor awareness.** Daffy built the Zapier integration and endorses `daffy-cli`. No Daffy page acknowledges Composio, Pipedream, Operator, Corsair, Metorial or Keystroke. Whether Daffy knows of them cannot be seen from public sources; outreach is barred.

### 1.3 Other platforms

| Platform | Finding | Source |
|---|---|---|
| **Endaoment** | No third-party wrapper holds Endaoment credentials.<br>• First-party `ndao` CLI with an MCP mode: `grant_create` requires the `idempotencyKey` from `grant_preview` and `confirm: true`. Writes are declared to the MCP host. Non-terminal use needs `--yes`. A partner API key reads only partner-owned funds and receipts, and "nothing is stored".<br>• Swear Jar plugin: sends USDC automatically from a hook to an Endaoment community DAF address. Money flows **into** a DAF, with no Endaoment credential | [@endaoment/ndao-cli](https://www.npmjs.com/package/@endaoment/ndao-cli) (0.7.0, 2026-10-22); [Swear Jar](https://www.npmjs.com/package/@sammybauch/swear-jar) |
| **Every.org** | The API has no donation-initiating endpoint.<br>• Public keys allow GET only. Private keys are for privileged calls such as "creating nonprofit fundraisers" ([auth](https://docs.every.org/docs/endpoints/authentication)).<br>• Zapier: one nonprofit-side trigger, New Donation ([Zapier](https://zapier.com/apps/everyorg/integrations); [help](https://support.every.org/hc/en-us/articles/44982950472595-Connect-Every-org-to-your-favorite-tools-with-Zapier), 2025-09-25).<br>• maxnate adapter: redirects donors to hosted checkout ([npm](https://www.npmjs.com/package/@maxnate/provider-everyorg)).<br>• GiveReady: links only ([npm](https://www.npmjs.com/package/giveready-mcp)).<br>• Vinkius listing: "We haven't connected this one yet" ([Vinkius](https://vinkius.com/client/mastra-ai/connect/everyorg-mcp)) | as cited |
| **Chariot** | None found in any index searched. Its MCP server (nonprofit records) and OAuth API are first-party (prior batch) | §1.1 |
| **Givinga** | None found. API docs sit behind a login (batch 30) | §1.1 |

---

## 2. P-ANL-11: analyst client-only research, 2021+

| Firm | Title (date) | What is public | Client-only? | DAF tech evaluated? | Source |
|---|---|---|---|---|---|
| **Datos Insights** (Aite-Novarica) | *Expanding Delivery of Philanthropic Advisory Across Wealth Management* (2021-09-04; release 2021-09-08), author Wally Okby | Abstract: philanthropy "really can't be left out of wealth plans anymore"; the sector "lags in fintech investment".<br>Basis: 18 executive interviews in H1 2021; 33 pages, 11 figures, 5 tables.<br>Firms mentioned include Amicus.io, CharityVest, GiveClear USA, Grapevine, Growfund, JustFund, Pinkaloo, RenPSG, TIFIN, Uncommon Giving, Fidelity, Schwab and Vanguard | Yes: "Clients of Aite-Novarica Group's Wealth Management service can download" | Mentions vendors. No scoring visible | [Datos report page](https://datos-insights.com/reports/expanding-delivery-of-philanthropic-advisory-across-wealth-management/); vendor PR: [Amicus.io, PR Newswire 2021-10-28](https://www.prnewswire.com/news-releases/wealth-management-report-says-philanthropy-cant-be-left-out-of-wealth-plans-anymore-301410636.html) |
| **Datos Insights** | *Wealth in America, Part 1: The Ultra-High-Net-Worth* (2024-03-20) | Built on Survey of Consumer Finances data. Covers "the size of the opportunities for advice and planning in the areas of philanthropy, tax management, and passing wealth to their heirs" | Yes (Wealth Management clients) | No | [Datos](https://datos-insights.com/reports/wealth-in-america-part-1-the-ultra-high-net-worth/) |
| **Datos Insights** (whole catalogue) | 2,509 `/reports/` URLs in the sitemap | Only the 2021 title has a philanthropy, charity, donor or giving term in its URL [C] | — | — | [sitemap index](https://datos-insights.com/sitemap_index.xml) |
| **Cerulli** | *U.S. High-Net-Worth and Ultra-High-Net-Worth Markets* 2024 / 2025 / 2026 | 2024 abstract: "$124 trillion—$105 trillion is expected to flow to heirs, while $18 trillion will go to charity". The 2025 and 2026 abstracts have no charity terms | Yes (purchase) | No | [2024](https://www.cerulli.com/reports/us-high-net-worth-and-ultra-high-net-worth-markets-2024); [2025](https://www.cerulli.com/reports/us-high-net-worth-and-ultra-high-net-worth-markets-2025); [2026](https://www.cerulli.com/reports/us-high-net-worth-and-ultra-high-net-worth-markets-2026) |
| **Cerulli** | *State of U.S. Wealth Management Technology* 2024 / 2025 / 2026 | No philanthropy terms in the abstracts. 2026 note: 27% of independent RIA practices are heavy technology users | Yes | No | [2026](https://www.cerulli.com/reports/state-of-us-wealth-management-technology-2026); [2025](https://www.cerulli.com/reports/state-of-us-wealth-management-technology-2025) |
| **Cerulli** (whole sitemap) | 789 URLs, 66 reports | No URL contains philanthrop, charit, donor, giving or DAF. Endowment/OCIO press releases only [C] | — | — | [sitemap](https://www.cerulli.com/sitemaps-1-sitemap.xml) |
| **Celent** | *World of Philanthropy: Entering the Mainstream?* (2003-03-07) | Covers private foundations as "a viable alternative to donor-advised funds" and profiles Foundation Source. A search summary dated it 2011; the page says 2003 | Yes | No | [Celent](https://www.celent.com/en/insights/312707366) |
| **Forrester** | none found | Site-restricted search returned only ESG and investor pages | — | — | [Forrester ESG](https://go.forrester.com/about-us/esg/) |
| **Gartner** | none found | Site-restricted search returned only Gartner's own giving pages | — | — | [Gartner CR](https://www.gartner.com/en/about/corporate-responsibility) |

**Reading [I]:**
- The absence finding in [analyst-and-education-landscape.md §1](analyst-and-education-landscape.md) holds, now on firmer ground for Cerulli and Datos: those catalogues were enumerated in full, not just searched.
- The only analyst work touching DAF vendors is a 2021 interview study written before Amicus.io, Pinkaloo, Vennfi and Giving Place were acquired. Its vendor list is now mostly absorbed by Ren, TIFIN and Foundation Source.
- Requesting the briefing abstracts would need outreach, which is barred.

---

## 3. P-FAIL-10: first-party founder or operator accounts, 2021+

| Case | Who speaks, date | Outcome | Stated reasons (verbatim where quoted) | Numbers | Source |
|---|---|---|---|---|---|
| **Tyve** (UK payroll giving; adjacent to DAF-as-benefit) | Founder (Clifford), EA Forum, 2022-12-18 | For-profit ended. Remaining funds returned to investors. Now a volunteer-run nonprofit | "very much a 'nice to have' for these companies"; CAC "pretty high"; had to sell to employer and employee; "couldn't get enough workplaces to say yes"; HR did not see giving as a retention tool | £150k SEIS; about £630k lifetime; £15k/month from 150 users; about 25% enrolment; £75 average monthly gift | [EA Forum mirror](https://ea.greaterwrong.com/posts/Wj2Z2NXDZXiysnRv5/lessons-learned-from-tyve-an-effective-giving-startup) ([original](https://forum.effectivealtruism.org/posts/Wj2Z2NXDZXiysnRv5/lessons-learned-from-tyve-an-effective-giving-startup) returned 429) |
| **Momentum** (US donation app, pivoted to donation pages) | Co-founder replies (user ak2), thread on or before 2022-01-12 | Mobile app shut down; pivot | "I agree the mobile app did not have PMF (which is why we shut it down)"; "struggling with donor acquisition" | App moved about $100k (about $230k to recommended charities including later portal giving); pages: $10m+ from 40k donors, mostly one campaign | [EA Forum thread (mirror)](https://ea.greaterwrong.com/posts/W9rkBeXqKsoMaMLEQ/momentum-2022-updates-we-re-hiring). Post body not visible; comments only |
| **Kambeo** (fundraising SaaS) | Company notice, unsigned | Shutdown effective 2026-03-30 | "not growing and succeeding as we had hoped" | — | [Kambeo](https://kambeo.io/kambeo-for-non-profits/) |
| **Everfund** (fundraising SaaS) | Co-founders Christopher Burns and Will De Ath | Closure notice 2024-11-22 | None stated. Data deleted at close | — | [Everfund](https://everfund.com/) |
| **ioby** (crowdfunding and fiscal sponsor) | Board Chair Apollo Gonzales, for staff and board (undated; closure 2024-09) | Closed | "the current landscape for non-profit organizations is fraught with uncertainties, obstacles, and financial challenges"; could not secure a sustainable future | $21m+ lifetime, 3,800+ projects; final year about $1.4m, 234 projects, 72 fiscally sponsored | [ioby](https://ioby.org/resources/closing/); context: [SeedMoney repost of Chronicle op-ed, 2025-05-27](https://seedmoney.org/blog/quiet-collapse-crowdfunding-platform/) |
| **Giving Assistant** (cashback-to-charity) | Successor operator's editorial team (Upright Data, owner from 2022-05), 2023-01-23. **Not the founders** | Board-ordered cessation 2021-11; liquidation via Uecker & Associates | "the cashback model used by previous management is not a sustainable or consistent way of doing this" | — | [FAQ](https://givingassistant.org/insights/news/giving-assistant-frequently-asked-questions) |
| **Giving What We Can** (pledge org running a donation platform) | GWWC team, 2025-04-10 | Retired 10 initiatives, including Hosted Funds and the Donor Lottery | Hosted Funds: "high operational costs associated with the Hosted Fund grantmaking process". Donor Lottery does not fit the pledge focus | Donor Lottery: 16 lotteries, $4.7m since 2018 | [EA Forum mirror](https://ea.greaterwrong.com/posts/f7yQFP3ZhtfDkD7pr/gwwc-is-retiring-10-initiatives) |
| **Vennfi / Charityvest** (DAF tech) | Founder Stephen Kump, quoted in the acquirer's release, 2024-10-17 | Acquired by Foundation Source | "it became clear that, together, we can catalyze more giving". No economics | Terms undisclosed | [Foundation Source](https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/) |

**Not obtained:**
- Pinkaloo's own acquisition post: its robots.txt bars Anthropic agents.
- Bright Funds/WizeHive release: Business Wire returned 403.
- TakeCharge.io founder post: Medium returned 403, and it is pre-2021 (prior HL22).
- Amicus.io, Giving Place, Stellar/iPhi and Crown/DonorFirst: acquirer releases only.

**Readings [I]:**
1. **The causal gap stays open for core DAF technology.** Every core DAF-tech exit since 2021 was an acquisition, and none has a first-party account of unit economics.
2. **Both stated failure reasons are about customer acquisition.** Both first-party accounts with reasons (Tyve and Momentum) are workplace or consumer giving, and both name acquisition as the problem. This supports [failed-daf-startups-deep-research.md P4](failed-daf-startups-deep-research.md) (low take vs CAC) as **two first-party statements in adjacent segments**. It is still not DAF evidence.
3. **Fund-hosting cost is now first-party evidence.** GWWC dropped hosted-fund grantmaking for operational cost. This is relevant to entrants that would host funds rather than partner with a sponsor.

---

## 4. P-ASR-06: Every.org's disbursement rail mix

### 4.1 Rules as published [F]

All from the [Disbursements overview](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview) (updated 2026-10-23), unless noted.

| Rail | Who gets it | Frequency / fee | Ends in |
|---|---|---|---|
| Stripe Connect | Charities that connect a bank account | Weekly ("most commonly on a Monday or a Tuesday"); 0% | Stripe subaccount, then bank |
| PayPal Grants | Charities registered with PayPal and without Stripe | Every 4–5 weeks; 0% | PayPal account, once accepted. "The funds will not be delivered if you do not accept the grant, and they will be returned to us when the grant expires so that we can try to disburse to you again." Reissued on request |
| ForGood, Inc (Network for Good) | Charities with neither of the above | Batched monthly, paid on the 15th of the next month; $10 minimum; 1.50% (Every.org covers it for bank-funded gifts) | ForGood **check** (to the GuideStar address) or direct deposit |
| Fiscally sponsored projects | — | The sponsor's method | — |

- The timing article says: "On a monthly basis, we grant funds through PayPal Giving Fund where possible" ([timing](https://support.every.org/hc/en-us/articles/360059998673-How-long-does-it-take-for-my-donation-to-reach-the-nonprofit), 2026-10-02).
- Undeliverable gifts are refunded to the donor as gift-card credit ([undeliverable](https://support.every.org/hc/en-us/articles/360058165694-What-happens-if-Every-org-can-t-deliver-a-donation-to-a-nonprofit)).
- **Every.org issues no checks itself** [F].

### 4.2 Form 990-PF Part XV by recipient type [C]

Parsed from IRS XML on the GivingTuesday mirror: [2020](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202141729349100004_public.xml), [2021](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202201479349100500_public.xml), [2022](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202333179349100048_public.xml), [2023](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202423199349106002_public.xml), [2024](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202502749349100700_public.xml).

| CY | Grants paid | Network for Good (ForGood rail) | PayPal Giving Fund | "Hyperwallet activity" | Unitemised aggregate line | Named recipients (Stripe or PayPal Grants, not separable) |
|---|---|---|---|---|---|---|
| 2020 | $964,640 | $713,148 (73.9%) | — | — | — | $251,492 (26.1%), 9 rows |
| 2021 | $5,806,498 | $2,375,859 (40.9%) | — | — | $277,514 (4.8%) "all other" | $3,153,125 (54.3%), 50 rows |
| 2022 | $17,427,495 | $2,905,359 (16.7%) | — | — | $450,955 (2.6%) | $14,071,181 (80.7%), 96 rows |
| 2023 | $16,782,740 | $2,446,497 (14.6%) | $6,201 (0.04%) | $283,570 (1.7%) | $363,248 (2.2%) "under 5K" | $13,683,224 (81.5%), 219 rows |
| 2024 | $44,931,032 | $474,870 (1.1%) | — | — | $6,580,200 (14.6%) "under 25K" | $37,875,962 (84.3%), 208 rows |

**Is the NFG fall real or an itemisation artefact?**
- **Real [I]:**
  - NFG is one payee whose annual total is far above both thresholds, so the switch from $5k to $25k cannot remove it.
  - NFG fell in dollars ($2.45m to $0.47m) while grants rose 2.7x [C].
  - The bookkeeper is the same on all five returns (Jitasa, prior batch).
  - The fall matches the help centre's fee incentive: 0% for Stripe and PayPal against 1.5% for ForGood, with Every.org paying the ForGood fee for bank-funded gifts.
- **Residual risk:** if Every.org began booking ForGood-routed gifts under end-charity names, the NFG line would understate the rail. No source shows that.
- **Stripe vs PayPal:** both pay the named charity, so the return cannot split them. PayPal-family lines are tiny (PPGF $6,201; Hyperwallet $283,570, both 2023). Hyperwallet is a PayPal payout service ([PayPal, 2018-11-15](https://newsroom.paypal-corp.com/2018-11-15-PayPal-Completes-Acquisition-of-Hyperwallet)). What the 2023 line records is unknown (P-B35C-02).
- **Intermediaries among the named rows:** King Baudouin Foundation US ($7.80m, 2024) and Founders Pledge ($0.76m) are regranting intermediaries, not end charities. So 19.0% of 2024 grants passed through another grantmaker: KBF US alone is 17.4%, and Founders Pledge adds the rest [C: (7,798,492 + 757,630) / 44,931,032].
- **Next filing:** no CY2025 Form 990 is in the IRS 2026 index (last modified 2026-10-21) ([index](https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv)).

---

## 5. P-PAY-06: PayPal Grant Payments expiry and check fallback

| Payer | Electronic rail | Window before fallback | Fallback | Published expiry or fallback rate | Source |
|---|---|---|---|---|---|
| NPT | PayPal Grant Payments | 14 days | Reissued as a check | none | [NPT DAF Guide (2026-10-15)](https://www.nptrust.org/wp-content/uploads/2024/09/A-Guide-to-your-Donor-Advised-Fund-NPT.pdf) (prior batch) |
| NPT (volume) | PayPal Grant Payments | — | — | ">$65 million" since the Aug 2022 launch; "a majority" in the charity's account within 24h (2023). No count, no expiry rate | [NPT, 2023-05-31](https://www.nptrust.org/?p=8367) |
| Every.org | PayPal Grants | Not stated | Funds return to Every.org and are reissued on request; no automatic check | none | [Disbursements overview](https://support.every.org/hc/en-us/articles/360061887233-Disbursements-overview) |
| PayPal (product rule) | Grant Payments | "Expiration date set by the grantmaker" (search snippet; page returned 403) | per grantmaker | none | [PayPal FAQ4654](https://www.paypal.com/us/smarthelp/article/FAQ4654) |
| PayPal (2023 study) | — | — | — | Charities get "over half" of institutional contributions by check; grantmakers send ">2 million checks per year"; saving of $2.86 per grant | [PayPal newsroom, 2023-12-20](https://newsroom.paypal-corp.com/2023-12-PayPal-Grant-Payments) |
| PPGF (CY2024 990) | PPGF grants to enrolled charities | — | Checks to unenrolled charities (check language quoted in Schedule I) | $797,890,089 in grants; 14,871 501(c)(3) recipients. **No enrolled/check split** | [990 XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml) |
| Chariot | Chariot Deposit Account | 5 business days, 3 emails | Check with grant letter | **"Since launch, 94.57% of grant payments made through Chariot are sent electronically"** (about 5.43% check [C]; pooled; vendor figure) | [Tracking & Delivery](https://help.givechariot.com/disbursements/for-grantmakers/tracking-and-delivery.md); [Disbursements](https://givechariot.com/disbursements.md) |
| Fidelity Charitable (via Chariot) | EFT | — | Electronic-only from July 2026 | "In 2025, 67% of Fidelity Charitable's 3 million grants were already distributed electronically" (secondary) | [Chariot insight](https://givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors) |

**Readings [I]:**
- The share of PayPal Grant Payments that expire is **not public** anywhere searched.
- Two designs are visible:
  - **Automatic check reissue** (NPT): a non-acceptance becomes a check after 14 days.
  - **Return to payer** (Every.org): an expired grant goes back to Every.org and waits for the charity or another rail.
- The fallback rate therefore has to be measured per payer.
- Chariot's 5.43% is the only quantified fallback-type figure. It pools all sponsors since launch and counts checks sent, not checks after a failed claim.

---

## 6. Limits

- Wrapper listings describe capability, not usage. No install counts or connected-account numbers are public (npm weekly downloads were not used as a proxy).
- Wrapper controls were read from marketing pages and READMEs, not tested.
- Composio's tool list changes over time (page updated 2026-11-06).
- Absence findings cover only the indexes listed in §1.1.
- Analyst catalogues were enumerated by URL slug. A report whose title omits philanthropy terms but includes a philanthropy chapter would be missed. The Datos 2024 UHNW report was found only because its abstract was read.
- Post-mortem accounts are self-reported and unaudited. The Momentum post body was not visible.
- Every.org's Part XV recipient types are inferred from names. Stripe vs PayPal cannot be split from the filings.

---

## Source register

| # | Source | Type | Date | Accessed | URL |
|---|---|---|---|---|---|
| S1 | Composio Daffy toolkit | vendor | 2025-12-04 / 2026-11-06 | 2026-11-15 | https://composio.dev/toolkits/daffy |
| S2 | Composio toolkit sitemap | vendor index | — | 2026-11-15 | https://composio.dev/toolkits/sitemap.xml |
| S3 | Pipedream Daffy app and action | vendor | action v0.0.2 | 2026-11-15 | https://pipedream.com/apps/daffy.md ; https://pipedream.com/apps/daffy/actions/create-donation.md |
| S4 | Pipedream Daffy component source | open source | — | 2026-11-15 | https://raw.githubusercontent.com/PipedreamHQ/pipedream/master/components/daffy/daffy.app.mjs |
| S5 | Pipedream app index | vendor index | — | 2026-11-15 | https://pipedream.com/llms.txt |
| S6 | Pipedream MCP page | vendor | — | 2026-11-15 | https://mcp.pipedream.com/app/daffy |
| S7 | Zapier Daffy | vendor | — | 2026-11-15 | https://zapier.com/apps/daffy/integrations |
| S8 | Daffy Hackday post | sponsor | 2023-06-12 (upd. 2026-02-20) | 2026-11-15 | https://www.daffy.org/resources/daffy-api-examples |
| S9 | n8n Daffy | vendor | — | 2026-11-15 | https://n8n.io/integrations/daffy/ |
| S10 | Operator.io Daffy | vendor | — | 2026-11-15 | https://operator.io/integrations/daffy |
| S11 | npm packages (Corsair, Metorial, Keystroke, daffy-cli, @pipedream/daffy, ndao-cli, swear-jar, maxnate, giveready) | registry | 2023-05 to 2026-10 | 2026-11-15 | https://registry.npmjs.org/ (package pages linked in §1) |
| S12 | Daffy auth, MCP, CLI, gifts docs | sponsor | undated | 2026-11-15 | https://docs.daffy.org/auth ; https://docs.daffy.org/agents/mcp ; https://docs.daffy.org/agents/cli ; https://docs.daffy.org/ref/gifts |
| S13 | Daffy llms.txt | sponsor | — | 2026-11-15 | https://daffy.org/llms.txt |
| S14 | Official MCP Registry API | registry | — | 2026-11-15 | https://registry.modelcontextprotocol.io/v0/servers?search=daffy |
| S15 | Every.org API auth | platform | — | 2026-11-15 | https://docs.every.org/docs/endpoints/authentication |
| S16 | Zapier Every.org; Every.org Zapier help | vendor / platform | 2025-09-25 | 2026-11-15 | https://zapier.com/apps/everyorg/integrations ; https://support.every.org/hc/en-us/articles/44982950472595-Connect-Every-org-to-your-favorite-tools-with-Zapier |
| S17 | Vinkius Every.org listing | vendor | — | 2026-11-15 | https://vinkius.com/client/mastra-ai/connect/everyorg-mcp |
| S18 | Datos Insights report pages and sitemap | analyst abstract | 2021-09-04; 2024-03-20 | 2026-11-15 | https://datos-insights.com/reports/expanding-delivery-of-philanthropic-advisory-across-wealth-management/ ; https://datos-insights.com/reports/wealth-in-america-part-1-the-ultra-high-net-worth/ ; https://datos-insights.com/sitemap_index.xml |
| S19 | Amicus.io release on the Aite report | vendor PR | 2021-10-28 | 2026-11-15 | https://www.prnewswire.com/news-releases/wealth-management-report-says-philanthropy-cant-be-left-out-of-wealth-plans-anymore-301410636.html |
| S20 | Cerulli report pages and sitemap | analyst abstract | 2024–2026 | 2026-11-15 | https://www.cerulli.com/sitemaps-1-sitemap.xml ; report URLs in §2 |
| S21 | Celent World of Philanthropy | analyst abstract | 2003-03-07 | 2026-11-15 | https://www.celent.com/en/insights/312707366 |
| S22 | Tyve lessons learned | founder post | 2022-12-18 | 2026-11-15 | https://ea.greaterwrong.com/posts/Wj2Z2NXDZXiysnRv5/lessons-learned-from-tyve-an-effective-giving-startup |
| S23 | Momentum 2022 updates thread | founder comments | ≤2022-01-12 | 2026-11-15 | https://ea.greaterwrong.com/posts/W9rkBeXqKsoMaMLEQ/momentum-2022-updates-we-re-hiring |
| S24 | Kambeo shutdown notice | company | effective 2026-03-30 | 2026-11-15 | https://kambeo.io/kambeo-for-non-profits/ |
| S25 | Everfund closure page | founders | 2024-11-22 | 2026-11-15 | https://everfund.com/ |
| S26 | ioby closing letter; SeedMoney repost | org; op-ed | 2024; 2025-05-27 | 2026-11-15 | https://ioby.org/resources/closing/ ; https://seedmoney.org/blog/quiet-collapse-crowdfunding-platform/ |
| S27 | Giving Assistant FAQ | successor operator | 2023-01-23 | 2026-11-15 | https://givingassistant.org/insights/news/giving-assistant-frequently-asked-questions |
| S28 | GWWC retiring 10 initiatives | org | 2025-04-10 | 2026-11-15 | https://ea.greaterwrong.com/posts/f7yQFP3ZhtfDkD7pr/gwwc-is-retiring-10-initiatives |
| S29 | Foundation Source acquires Vennfi | acquirer PR | 2024-10-17 | 2026-11-15 | https://foundationsource.com/newsroom/press-releases/foundation-source-acquires-vennfi-the-fintech-powering-donor-advised-fund-charityvest/ |
| S30 | Every.org help centre (Zendesk JSON, 94 articles) | platform | 2020–2026 | 2026-11-15 | https://support.every.org/api/v2/help_center/en-us/articles.json |
| S31 | Every.org 990-PF XML CY2020–2024 | filing | 2021–2025 | 2026-11-15 | §4.2 links |
| S32 | IRS e-file index 2026 and 2025 | index | 2026-10-21 | 2026-11-15 | https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv ; https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv |
| S33 | PayPal completes Hyperwallet acquisition | company | 2018-11-15 (context) | 2026-11-15 | https://newsroom.paypal-corp.com/2018-11-15-PayPal-Completes-Acquisition-of-Hyperwallet |
| S34 | NPT PayPal $65m post | sponsor | 2023-05-31 | 2026-11-15 | https://www.nptrust.org/?p=8367 |
| S35 | PayPal Grant Payments newsroom | company | 2023-12-20 | 2026-11-15 | https://newsroom.paypal-corp.com/2023-12-PayPal-Grant-Payments |
| S36 | PayPal Charitable Giving Fund CY2024 990 | filing | ReturnTs 2025-11-03 | 2026-11-15 | https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202533079349301308_public.xml |
| S37 | Chariot tracking & delivery; Disbursements page; e-pay insight | vendor | 2026 | 2026-11-15 | https://help.givechariot.com/disbursements/for-grantmakers/tracking-and-delivery.md ; https://givechariot.com/disbursements.md ; https://givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors |

**Blocked or not used:**
- Returned errors: paypal.com smarthelp (403), businesswire.com (403), medium.com (403), forum.effectivealtruism.org (429, mirror used).
- Barred by robots.txt: pinkaloo.com (Anthropic agents), Cerulli `/news/`, Google Drive `/uc` downloads.

---

## Data dictionary

### `data/mission-2026-11-14/daf-agent-wrappers-2026.csv` (one row per wrapper, or per platform with none found)

| Column | Meaning |
|---|---|
| wrapper_id | W01–W19 |
| wrapper_name, wrapper_operator | Product and the company or person running it |
| party | `third-party`, `first-party`, `first-party-built on third-party platform`, `first-party-endorsed`, `first-party-documented on third-party platform`, `third-party (wrapper of wrappers)`, `none found` |
| wrapper_type | Hosted MCP/tool router, workflow automation, library, CLI, hook plugin, etc. |
| target_platform, target_role | DAF API wrapped and its role (donor-side sponsor, pass-through platform, payment infrastructure) |
| listing_url, secondary_url | Primary listing and supporting sources |
| auth_method_documented | How the wrapper authenticates to the target, as documented |
| credential_held_by_wrapper | Whether and how the wrapper stores the donor's credential |
| credential_scope_documented | Any documented scope limit (target or wrapper side) |
| read_tools_n | Count of read tools or actions, where listed |
| write_actions | Named write actions |
| moves_or_commits_money | Whether a write action creates a donation, gift or transfer ([I] where inferred) |
| documented_controls | Limits, confirmations, audit or allow-lists the wrapper or target documents |
| target_documents_wrapper | Whether the DAF platform's own pages mention the wrapper |
| first_seen, last_updated | Earliest and latest public dates found (npm created/modified, page metadata) |
| evidence_class | Kind and depth of source read |
| accessed | Access date |
| notes | Caveats |

### `data/mission-2026-11-14/queue-proposals-batch35c.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md):
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.
- `proposed_by` is `batch35 C agent`.
- `evidence_pointer` cites this note's sections or URLs.

## Validation corrections (wave 20, 2026-11-15) — governing
Source: [validation-wave20-report.md](validation-wave20-report.md); register `data/mission-2026-11-14/validation-register-wave20.csv`.

1. **§0, P-CON-06 row (money-moving wrappers).**
   - **Find:** "• At least five of them document a **write action that commits fund money** (Operator.io also re-exposes Composio's Create Gift):<br>"
   - **Replace with:** "• At least five of them document a **money-related write action** (Operator.io also re-exposes Composio's Create Gift). Three document **donation** creation (Pipedream, Zapier, Metorial). Composio and Corsair expose only **gift** creation, and Daffy's Gifts reference does not say whether a gift debits the fund balance [I; V wave 20]:<br>"
2. **§1.2, reading 4 (gift path).**
   - **Find:** "4. **The gift path is under-examined.**"
   - **Replace with:** "4. **The gift path is under-examined** (so W01 and W06 are not counted as documented fund debits; V wave 20)."
3. **§0, P-ASR-06 row (years).**
   - **Find:** "Its share of grants fell from 73.9% (2020) to 1.1% (2024), while the dollar amount fell from $2.45m to $0.47m as grants rose 2.7x [C]."
   - **Replace with:** "Its share of grants fell from 73.9% (2020) to 1.1% (2024). From 2023 to 2024 its dollar amount fell from $2.45m to $0.47m while total grants rose 2.7x ($16.78m → $44.93m) [C; V wave 20]."
