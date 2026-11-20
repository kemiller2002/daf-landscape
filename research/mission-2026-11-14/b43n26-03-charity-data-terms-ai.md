# P-B43N26-03: Do charity-data terms permit AI use? Six providers plus the IRS baseline

**Task:** P-B43N26-03 (TASKID b43n26-03). **Date:** 2026-11-20.
**Context:** [queue-batch29-regulation-litigation-crypto.md](queue-batch29-regulation-litigation-crypto.md) §4 (Candid retention, P-TRM-04).
**Outputs:**
- [`data/mission-2026-11-14/charity-data-terms-ai-matrix-2026-11-20.csv`](../../data/mission-2026-11-14/charity-data-terms-ai-matrix-2026-11-20.csv): 28 rows, one per provider × use.
- [`scripts/mission_b43n26_03_terms_matrix.py`](../../scripts/mission_b43n26_03_terms_matrix.py): validation and tallies.
- [`data/mission-2026-11-14/queue-proposals-b43n26-03.csv`](../../data/mission-2026-11-14/queue-proposals-b43n26-03.csv)

Labels: **[F]** first-party text fetched in this run. **[C]** repo record, not re-fetched. **[I]** our inference. **[U]** unknown.

---

## 0. Summary

The four uses tested are:
- (a) showing ratings or profile data inside an AI chat or MCP tool response;
- (b) using the data as model or ranking features;
- (c) caching beyond 24 hours;
- (d) keeping the data after termination.

The six commercial providers give 24 provider × use cells. In those cells, no public term permits any of the four uses without conditions, with one exception: Charity Navigator allows caching for site speed, with no time limit.

| Provider | (a) AI/MCP display | (b) model / ranking features | (c) cache > 24 h | (d) retain after termination |
|---|---|---|---|---|
| Charity Navigator | requires-licence | **prohibited** | permitted (purpose-limited, ratings data) | prohibited (legal carve-out) |
| Candid | requires-licence | requires-licence (**AI/LLM/ML clause**) | requires-licence (no caching clause; general "store" ban) | prohibited |
| Every.org | silent (site terms not read: robots 429) | silent | silent | silent |
| Pledge | silent (API terms not public) | silent | silent | silent |
| Goodstack | requires-licence | silent | silent | prohibited [I] |
| Benevity | requires-licence | silent | silent | prohibited (backup/legal carve-out) |
| IRS EO BMF / TEOS (baseline) | permitted | permitted | permitted | permitted (and required for reliance) |

Script output for the 24 commercial cells: permitted 1, prohibited 5, requires-licence 6, silent 12. Of the 12 silent cells, 8 (all of Every.org and Pledge) mean not determinable, because the governing terms were blocked or are not public; only 4 (Goodstack and Benevity (b) and (c)) are silent in terms that were read. Express clauses back 11 of the 24, or 10 if Goodstack (d), an inference, is not counted. [V wave 44A] One cell, Candid (b), has AI/LLM/ML-specific wording.

**Headline [I].**
- **Raw ratings.** An AI DAF product cannot treat third-party *ratings* as free model inputs. Candid’s AI wording, quoted below, qualifies a ban on mining to build a non-internal database, to resell or to compete; it is not a stand-alone AI ban (§2.2). [V wave 44A] Charity Navigator forbids using its ratings "in any other calculation". Candid needs written consent before its data are mined for "artificial intelligence (“A.I.”), large language models, machine learning".
- **Display.** Every commercial licence that speaks to display ties it to the licensee's own site or app. That does not cover a third-party AI host receiving MCP tool output.
- **Retention.** Every licence that speaks to termination requires deletion or an end to use.
- **What is clean.** Only the IRS baseline is free of licence limits on all four uses. An AI product can rank and cache on IRS fields, and link out to or quote licensed ratings under attribution.

---

## 1. Method

1. **Scope.**
   - Providers: Charity Navigator, Candid, Every.org, Pledge, Goodstack, Benevity, plus IRS BMF/TEOS as a public-domain baseline.
   - Documents: the provider's current public API or data terms. Where no API terms are public, we used the general terms and developer docs.
   - The test is what the public text says. Order Forms, Service Orders and negotiated terms are not public and are not assessed.
2. **Robots and fetching.**
   - Each host's robots.txt was checked by `urllib.robotparser` before each fetch, with user agent `research-script/1.0`. All 62 requests were logged (§1.1). The fetcher is in the session scratchpad, not the repo.
   - No logins, sign-ups or forms. No user-agent changes. No alternative fetch tools after a block.
3. **Coding.**
   - Each cell gets one value: **permitted**, **prohibited**, **requires-licence** or **silent**.
   - *Requires-licence* means the public text permits the use only if an Order Form, Service Order or written approval says so, or it bars the use "except as permitted" with no permission given.
   - *Silent* means no clause addresses the use. The CSV adds `express_clause` (yes/no), so a requires-licence cell that rests on a general clause, such as Candid (c), stays distinguishable.
4. **Quote check.** Every [F] quote in the CSV and the notes was matched verbatim, after whitespace and quote-mark normalisation, against the fetched text. All matched. The two [C] quotes come from the repo.
5. **Computation.** `python3 scripts/mission_b43n26_03_terms_matrix.py .` checks the schema, vocabulary and a complete 7 × 4 grid (0 errors) and prints the tallies used here.
6. **Repo links.** We searched research/ for "MCP", "Candid" and "Charity Navigator" (files matching: MCP 49, Candid 128, Charity Navigator 19). §5 uses the relevant ones.

### 1.1 Robots log (per host, 2026-11-20 UTC)

| Host | robots.txt status | Decision | Requests | Fetched 200 |
|---|---|---|---|---|
| www.charitynavigator.org | 200 | allowed (API terms, site ToU) | 3 | 3 |
| developer.charitynavigator.org | 200 | allowed (blocks only /signin, /checkout etc.) | 4 | 3 (llms.txt 404) |
| candid.org | **403** | robots unreadable; the pages also returned 403 | 2 | 0 |
| developer.candid.org | 200 | allowed | 3 | 3 |
| www.every.org | **429** | treated as disallowed after a retry; the first two requests also returned 429 | 3 | 0 |
| docs.every.org | 404 (none) | allowed | 6 | 6 |
| support.every.org | 200 | allowed | 3 | 1 |
| www.pledge.to | 200 | allowed | 9 | 7 (two terms URLs 404) |
| developer.pledge.to | 404 (none) | allowed | 6 | 5 |
| goodstack.org | 200 | allowed | 1 | 1 |
| goodstack.io | 200 | allowed | 4 | 4 |
| docs.goodstack.io | 404 (none) | allowed | 2 | 2 |
| benevity.com | 200 | allowed | 3 | 3 |
| go.benevity.com | 200 | allowed (MSA, SSI PDFs) | 5 | 5 |
| developer.benevity.org | 404 (none) | allowed | 2 | 2 |
| www.irs.gov | 200 | BMF page allowed; **TEOS paths disallowed** (`Disallow: /charities-non-profits/tax-exempt-organization-search`) | 2 | 1 |
| www.govinfo.gov | 200 | allowed (17 U.S.C. 105) | 1 | 1 |
| www.law.cornell.edu | 200 | allowed | 1 | 1 |
| uscode.house.gov | 200 | allowed (page 404) | 1 | 0 |
| api.github.com | 403 | not fetched | 1 | 0 |

**Logging note.** The first version of the fetcher treated any 4xx robots status as "allowed". It was corrected mid-run so that 401, 403 and 429 count as disallowed. The three requests logged "True" under the old rule (two to candid.org and two of the three to www.every.org, so four requests, not three) all returned 403 or 429, so no content was obtained from those hosts. The fetcher is not in the repo, so the log cannot be re-run; a 2026-11-20 re-check found the same robots statuses (candid.org 403, www.every.org 429). [V wave 44A]

---

## 2. Results by provider

### 2.1 Charity Navigator [F]

Sources:
- [API Terms of Use](https://www.charitynavigator.org/products-and-services/api/), "Last updated October 2026". The `graphql-api/api-terms-of-use/` URL serves a byte-identical page (same sha256 prefix).
- [Attribution Guidelines](https://developer.charitynavigator.org/attribution) (“Last modified on November 17, 2026”). This page reads “Our ratings may not be used in any other calculation or manipulated.” The “Please remember, …” wording quoted below is the copy printed in the Attribution Requirements section of the API Terms page. [V wave 44A]
- [Developer terms summary](https://developer.charitynavigator.org/termsofuse), "Last modified on November 17, 2026".

| Use | Clause |
|---|---|
| (a) | s.1(c) licenses display "on the Licensee Site for End Users to access such data without charge for their own personal, non-commercial use". s.11(h) defines "Licensee Site" as "the website operated by You". The licence is "non-sublicensable" (s.1). s.2(b) bars any use "not expressly permitted" and bars making the Database available on a "service bureau" basis. Attribution: "A linkback to a Charity Navigator web page is required wherever our data is used." The developer summary adds: "You may not sublicense, sell, or redistribute API data." |
| (b) | Attribution guide: "Please remember, our ratings may not be used in any other calculation or manipulated." Terms s.4(a) makes binding the attribution requirements "issued by Charity Navigator from time to time". |
| (c) | s.1(d): "cache ratings data received through the API solely to improve the speed and functionality of the Licensee Site and/or for another purpose approved by Charity Navigator". No duration is stated. |
| (d) | s.6(c)(ii): "promptly delete all documents, computer files, cached data, and other materials containing any Confidential Information ... except as otherwise required by applicable law or regulation". Confidential Information includes "the API and the Charity Navigator Database" (s.11(c)). s.6(b)(iii) lets CN terminate "upon thirty (30) days' written notice for any reason or no reason". |

**AI language: none.** A keyword search of the API terms and the attribution guide found no AI, LLM, machine-learning or training wording.

**Website terms (context).** The [site Terms of Use](https://www.charitynavigator.org/about-us/financials-and-policies/terms-of-use/) are dated "Last updated November 1, 2022". They bar "data mining, robots, or similar data gathering and extraction methods" and bar "Republish[ing] or distribut[ing] information from the Website without Charity Navigator's express written consent". So scraping the website is not a route around the API licence.

**Readings [I].**
1. **(a) Own site vs third-party host.** An assistant embedded in a sponsor's own free website could fit s.1(c), provided each answer carries the required linkback and the "Powered by Charity Navigator" credit (s.4(b)). An MCP server whose output goes to a third-party AI host (Claude, ChatGPT, Copilot) is not the "Licensee Site". It also works as onward distribution under a non-sublicensable licence. That needs CN's approval.
2. **(a) Paid products.** The "without charge" and "personal, non-commercial use" limits are a second barrier for paid AI products.
3. **(b) Scope of the ban.** The calculation ban covers ratings (score and stars). It does not clearly reach EIN, cause or advisory fields.
4. **(c) What caching covers.** Caching for speed has no 24-hour cap. The grant names only "ratings data", and the cache must serve the Licensee Site.

### 2.2 Candid

Sources:
- **2026 API License Agreement** ([candid.org](https://candid.org/terms-of-service/api-license-agreement/), "Last updated September 14, 2026"). The host returned 403 to this run's client, so 2026 quotes come from the repo [C]: [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) §5; [queue-batch29](queue-batch29-regulation-litigation-crypto.md) §4; [validation wave 9](validation-wave9-report.md) V9-06.
- **Fetched [F]:**
  - [Candid API terms of service](https://developer.candid.org/page/candid-api-terms-of-service.md) (portal page updatedAt 2026-09-07);
  - [Candid License Agreement (APIs)](https://developer.candid.org/page/candid-license-agreement.md), "Last updated December 2023".

| Use | Clause |
|---|---|
| (a) | Permitted use: "Provide access to the Candid Data through the Licensee Site to Licensee Customers ... to learn about nonprofit organizations for the purpose of evaluating them as recipients of charitable donations". Licensee Customers must be bound by "a user agreement or other binding, enforceable agreement". No third-party access beyond those "specifically identified in the Order Form" (s.3.3). The Licensee Site is the website "located at the URL specified on the Order Form". |
| (b) | **AI-specific [F]:** "This prohibition expressly applies to data mining or extraction for use in artificial intelligence (“A.I.”), large language models, machine learning, or similar applications without Candid's express prior written consent." The portal TOS also bars "create any derivative product from the Candid Data" and "modify information from the Candid API" (s.3.2). The 2026 licence lets the licensee own Derivative Works "sufficiently distinct and different from Candid Data" [C]. |
| (c) | No caching clause in any version (2026: "No clause found" [C]). A general ban applies: "store, copy, reproduce ... other than as specifically permitted herein" (TOS s.3.2). |
| (d) | "Licensee shall cease, and shall cause its Authorized Users to cease, all use of the Candid Data" (TOS s.4.3; 2026 s.4.c.v [C]). No retention carve-out. The data-mining obligation "will survive the termination or expiration of this Agreement". |

**AI language: present, twice.**
1. **The data-mining sentence above.** It is in the December 2023 portal copy, and the repo records it in the 2026 licence. Validation wave 9 found that it qualifies a ban on mining for three purposes:
   - compiling a database "other than for Licensee's own internal business use";
   - resale;
   - building a competing service.

   It is not a stand-alone AI ban.
2. **An AI output disclaimer** (Dec 2023 copy, s.7): "We may use third-party machine learning or A.I. services to generate some results on the Candid Site (“Output”)".

**Wording variance [U].** The repo's 2026 quote reads "for use in or through the use of artificial intelligence". The fetched 2023 copy reads "for use in artificial intelligence (“A.I.”), large language models, machine learning, or similar applications". The 2026 text could not be re-read here (queue proposal P-B43N26-03-01).

**Readings [I].**
1. **(b) Narrow use is ambiguous.** Using Candid fields as ranking features inside the licensee's own product falls between "internal business use" (allowed for compilation) and "derivative product" and "modify" (barred in the TOS). Written consent is the safe reading.
2. **(c) Default rule.** Caching beyond 24 hours is not addressed. The default is the general store ban, so an Order Form term is needed.
3. **(d) Conflict with the IRS.** Unchanged from queue-batch29 §4: deletion conflicts with Rev. Proc. 2011-33 report retention.
4. **Candid's own AI channel.** Candid itself distributes data into Claude through its read-only MCP connector (repo AIP22). AI display is a channel Candid licenses on its own terms, not one it rules out.

### 2.3 Every.org [F, partial]

- **Site terms not read.** `www.every.org/terms` was not read: robots.txt returned 429 and was treated as disallowed. This repeats the 403/429 result of 2026-11-15 ([queue-batch30-everyorg-givinga-goodstack.md](queue-batch30-everyorg-givinga-goodstack.md)).
- **Developer docs** ([docs.every.org](https://docs.every.org/docs/endpoints/nonprofits), undated, ©2026):
  - "We strive to keep this API open and available for use without restrictions."
  - Rate limits apply (100–500 requests per minute per key).
  - Public keys are "suitable for use in both server-side and public-facing client side applications".
  - Keys may be blocked "if there is inappropriate usage".
  - The help-centre search for "api" returned 3 articles, none of them terms.
- **All four uses: silent.** The docs say nothing about AI, caching, model use or termination.
- **Reading [I].** The docs' openness is a stated intent, not a licence.

### 2.4 Pledge [F, partial]

- **Public terms.** The [Terms of Service](https://www.pledge.to/terms) are "Posted/Revised: January 15, 2025". They cover the website and forms, and say: "There is a separate Terms of Service (Terms of Service: Non-Public Services) that covers ... our application programming interfaces".
- **API terms are not public.** In the page HTML, the table-of-contents link to `/terms-services` is commented out. `/terms-services` and the sitemap-listed `/terms-services-non-public` both return 404.
- **Website licence.** "for the sole purpose of using the Services for your personal or internal business purposes". It bars scraping "data from any web pages contained in the Website". This does not govern API data.
- **AI in docs, not terms [F].** Pledge runs a partner MCP server ([guide](https://developer.pledge.to/guides/mcp/)). It "lets you connect AI coding assistants directly to your Pledge partner account ... your AI assistant can search nonprofits". The [tool reference](https://developer.pledge.to/reference/mcp/) lists `lookup_organization`, `create_nonprofit_fundraiser` and `create_donation`. PledgeAI markets "Pledge’s industry-leading charity database" for AI-generated campaigns.
- **All four uses: silent** in public terms.
- **Reading [I].** Pledge plainly endorses AI-assistant access to its nonprofit data for partners, but the governing terms are private. The MCP server's `create_donation` tool moves money. Pledge is not in the AI product census (§5.3).

### 2.5 Goodstack [F]

Source: the [Standard Terms and Conditions](https://goodstack.io/legal/standard-terms-and-conditions), "Effective Date: November 15, 2024". This is the live version on 2026-11-20, even though it predates 2025. The [Vetting & Validation](https://goodstack.io/legal/additional-terms-vetting-validation) and [Donation Service](https://goodstack.io/legal/additional-terms-donation-service) additional terms (same date) add nothing on these uses.

| Use | Clause |
|---|---|
| (a) | A right "without the ability to grant such right to third parties, to permit the Authorised Users to use the Services ... solely for the Client’s internal business operations". The client must not "display, transmit, or distribute all or any portion of the Software", and "Software" includes "any API". Requires-licence (Service Order). |
| (b) | Silent. "Goodstack and/or its licensors own all Intellectual Property Rights in the Platform, the Goodstack Data and the Services." The competing-product ban applies. |
| (c) | Silent. |
| (d) | On termination the client "shall immediately cease all use of the Platform and the Services" and must "return and make no further use of any ... property and other items (and all copies of them) belonging to the other party". Coded prohibited **[I]**, because Goodstack owns the Goodstack Data. |

**AI language: none.** "Automated scraping" appears only as a sign of unreasonable API use.

### 2.6 Benevity [F]

Sources:
- [Master Services Agreement](https://go.benevity.com/hubfs/website/legal/Master-Services-Agreement.pdf), "Updated: February, 2026";
- [Giving API SSI](https://go.benevity.com/hubfs/website/legal/Benevity-SSI-Giving-API.pdf), "Last Updated: April 2026";
- General Terms SSI (January 2026), Data Export API SSI (December 2025) and Premium Nonprofit Screening SSI (September 2025);
- [End User Terms](https://benevity.com/legal/end-user-terms-of-use), 2025-12-24.

| Use | Clause |
|---|---|
| (a) | Giving API SSI s.2: Giving API calls run "between Client’s own end-user-facing application(s) and the System". Under s.3, programmes not listed on the Order Document need "prior written approval of Benevity". MSA s.5.1(b): no sharing of "non-public System features or content with any third party". Requires-licence. |
| (b) | Silent. MSA s.5.1(c) bars only building "a competitive product or service". |
| (c) | Silent in all five documents. |
| (d) | MSA s.12.3: "upon termination of the MSA, the Client will cease all use of the System, subject to Section 12.4". s.12.4 allows termination assistance for up to six months. Under s.7 a recipient "may retain copies of Confidential Information to comply with applicable laws or during the course of routine backup". |

**AI language: none** in the MSA or the SSIs read. The End User Terms bar any "robot, spider, other automatic device or manual process to monitor, scrape, or copy the System".

### 2.7 IRS EO BMF / TEOS (baseline) [F]

- **No licence.** "Copyright protection under this title is not available for any work of the United States Government" ([17 U.S.C. 105](https://www.govinfo.gov/content/pkg/USCODE-2023-title17/html/USCODE-2023-title17-chap1-sec105.htm)).
- **BMF currency.** The [BMF page](https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf) shows "Updated data posting date: 11/10/2026" and "Record Count: 1,984,891".
- **Retention.** Rev. Proc. 2011-33 §4(2) *requires* retention for third-party reliance [C].
- **TEOS not fetched.** TEOS paths are robots-disallowed for generic agents. The baseline rests on the BMF page and the statute.

---

## 3. AI-, LLM- or ML-specific language

| Provider | AI wording in terms? | Where |
|---|---|---|
| Candid | **Yes** | Data-mining clause names "artificial intelligence (“A.I.”), large language models, machine learning"; an ML output disclaimer (Dec 2023 copy; 2026 per repo) |
| Charity Navigator | No | — (the ratings calculation ban is AI-neutral but bites on rankers) |
| Every.org | Not determinable | Site terms not read |
| Pledge | Not in public terms | AI appears only in product docs (MCP server, PledgeAI) |
| Goodstack | No | — |
| Benevity | No | — |

**Silence pattern.**
- *Caching* is silent at four of six providers. It is addressed only by CN (permitted) and, indirectly, by Candid's store ban.
- *Model or ranking use* is silent at four of six.
- *Retention* is the best-covered use: four of six have a stop-use or delete clause.
- Every.org and Pledge are silent on all four uses because their governing terms were not available: one blocked, one private.

---

## 4. Implications for AI DAF products that surface charity data [I]

1. **Two data layers.**
   - *Eligibility and identity* (EIN, status, Pub 78, revocation): build on IRS BMF/Pub 78. It is free to cache, rank on, show in any AI client and keep.
   - *Ratings and profiles* (stars, Encompass score, GuideStar profiles, seals): treat as display-only, link-out content governed by licence.
2. **No ratings in the score.** CN's calculation ban covers any ranker, recommender or "AI score" that takes CN ratings as inputs. This holds even if the stars are never shown. Candid needs consent for AI/ML extraction at scale. The repo already advises this ([strategic-synthesis.md](strategic-synthesis.md) l.556). This run confirms it from the current terms and adds Candid's explicit AI clause.
3. **MCP and third-party hosts are a distribution question.** Every licence that speaks to display binds it to the licensee's own site or app: CN "Licensee Site", Candid "Licensee Site … URL specified on the Order Form", Benevity "Client’s own end-user-facing application(s)", Goodstack "internal business operations".
   - **Own assistant vs third-party host.** A sponsor's in-app assistant is closest to the grant. A public MCP server that returns licensed ratings into Claude or ChatGPT is not covered without an Order Form or approval.
   - **Paid products.** CN's "without charge" and "non-commercial" limits add risk for paid AI tiers.
4. **Attribution must survive the model.** CN requires a linkback "wherever our data is used" and star images that link to the rating page. Candid requires "Powered by Candid" on pages that show its data. LLM paraphrase that drops the source or the link would breach these. Tool responses should carry structured attribution and URLs, and the client UI should render them.
5. **Caching.** Only CN expressly allows long-lived caches, and only of ratings and for site speed. A vector index or embedding store of CN or Candid content is a new copy for a new purpose. Under Candid it is "store … other than as specifically permitted". Under CN it is outside "speed and functionality of the Licensee Site". It needs written terms.
6. **Termination.** CN, Candid, Goodstack and Benevity all require deletion or an end to use. Embeddings, fine-tuned weights or cached tool outputs derived from licensed data are hard to purge. The only express carve-outs are CN's "required by applicable law", Benevity's "routine backup" and Candid's Derivative Works if "sufficiently distinct" [C]. Due-diligence records should be stored as the sponsor's own determinations, citing IRS evidence (queue-batch29 §4.2).
7. **Providers are moving into AI themselves.** Candid (Claude MCP connector, 2025-12-02) and Pledge (partner MCP server) put their data into AI hosts on their own terms. CN runs "Horizon AI Search" ([direction-charity-ratings-integrations.md](direction-charity-ratings-integrations.md)). The commercial pattern is "come through our channel", not "use our data in yours".

---

## 5. Links to the repo's AI overlay and quadrant work

### 5.1 A5 quadrant (charity eligibility data)

- **IRS baseline.** [quadrant-A2-A5-rationale.md](quadrant-A2-A5-rationale.md) §A5 scores the IRS baseline above every commercial provider on both axes. This matrix adds a rights dimension: the IRS is the only source with no licence friction for AI reuse (4 of 4 permitted).
- **Candid Y1.** Candid Y1 (openness and data rights) is 3. Queue-batch29 §4 already proposed 3 → 2 on portability. Two more public facts support that move [I]:
  - the AI/ML consent clause;
  - the general store ban, with no caching grant.
- **Benevity and Goodstack.** These A5 rows have no public AI-reuse rights either: (a) requires-licence, (b) and (c) silent. That is consistent with their current Y1 bands. No score change is proposed in this file; the methodology's two-scorer rule applies.
- **Method gap.** Y1 ([evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §Y1) asks for a "public API plus documented data-export/portability rights". It does not separately test *downstream AI reuse rights*. Queue proposal P-B43N26-03-05 suggests using this matrix as a Y1 sub-check for A5.

### 5.2 AI overlay (§7a/§7b)

- **What the overlay measures.** The overlay tests money-moving and status-clearing controls, not data rights. A licence breach is not RED or AMBER under §7. This matrix is a separate risk lens and should not be folded into overlay flags.
- **Candid MCP.** The connector (AIP22, AMBER low) is read-only, so it is not money-moving. Its terms question is who may relay Candid data, and the connector is Candid's own channel.
- **Pledge MCP (new to the repo).** `create_donation` is a money-moving AI-reachable tool, like Daffy's `make_donation` (AIP02, AMBER) and Chariot's MCP (AIP07). Under §7a.2, Pledge would receive a *product-level reading*, not an area overlay, because Pledge is not scored in A1–A5. Its controls were not read here (P-B43N26-03-03).

### 5.3 Confirmations and precision notes on existing repo text

| Repo text | This run |
|---|---|
| strategic-synthesis l.543: CN "API licence ... bars using ratings 'in any other calculation'" | **Confirmed.** The sentence is in the Attribution Requirements, which Terms s.4(a) makes binding. The API Terms page itself prints those requirements after s.12, with the sentence in the same words, so l.543 needs no correction. [V wave 44A] |
| direction-charity-ratings-integrations §2.1: CN "Caching allowed" | **Confirmed, with qualifiers.** The grant covers ratings data only, for Licensee Site speed or an approved purpose. No time limit. |
| queue-sponsor-terms-data-clauses §5: Candid "Caching and retention: No clause found" | **Consistent.** The portal TOS and the Dec-2023 copy also have no caching clause, but both have a general "store" ban. |
| queue-batch29 §4: Candid stop-use on termination | **Consistent.** The same words are in the 2026-09-07 portal TOS s.4.3. |
| philanthropy-ai-products-2026.csv (30 products) | **Gap.** The Pledge MCP server (with `create_donation`) is absent. |

---

## 6. Limits

- **Public terms only.** Order Forms, Service Orders and negotiated licences can override every cell. "Requires-licence" often means it is settled privately.
- **Candid 2026 text.** It was not re-read (candid.org returned 403, and the user agent was not changed). The 2026 quotes are [C], from earlier repo reads that were validated in wave 9. The fetched portal copies are older forms.
- **Every.org.** The site terms were unreadable (robots 429), so its four "silent" cells mean "not determinable", not "no restriction".
- **Pledge.** The API terms are not public. Its cells reflect missing terms, not permissive terms.
- **Goodstack.** The Standard Terms are dated 2024-11-15. They are the live version, but they predate the 2025–2026 window. The (d) value is an inference.
- **Benevity.** Only the MSA, SSIs and End User Terms were read. The Causes portal terms are an OneTrust shell (repo g1913) and were not read.
- **Legal interpretation.** "Display in an MCP response" and "use as a ranking feature" are not terms in any licence. Mapping them to clauses is our reading. It is not legal advice.
- **IRS.** TEOS is robots-disallowed, so the baseline rests on the BMF page and 17 U.S.C. 105.

---

## 7. Data dictionary: `charity-data-terms-ai-matrix-2026-11-20.csv`

| Column | Meaning |
|---|---|
| provider | Data provider. "IRS EO BMF / TEOS (baseline)" is the public-domain reference |
| use_code | a, b, c or d (see `use`) |
| use | a = display ratings/profile data in an AI chat or MCP tool response; b = use as model or ranking features; c = cache beyond 24 hours; d = retain after termination |
| value | permitted / prohibited / requires-licence / silent (coding rules in §1) |
| express_clause | yes if a clause addresses the use directly; no if the value rests on a general clause or on absence |
| ai_specific_language | yes if the governing clause names AI, LLMs or machine learning |
| clause_quote | Short verbatim quote; "(...)" placeholders mark the absence of a clause |
| clause_ref | Section reference and related clauses |
| document | Document title |
| url | Primary URL of the document |
| effective_date | Effective or last-updated date as printed (or the page metadata date) |
| evidence_label | F = fetched this run; C = repo record; I = inference from fetched text |
| evidence_status | read = governing text read; partial = governing terms unavailable (blocked or not public), so the coding uses docs or general terms |
| notes | Reading, caveats and AI-specific observations |

---

## 8. Source register

| ID | Source | Date | URL | Label |
|---|---|---|---|---|
| S1 | Charity Navigator API Terms of Use | Oct 2026 | https://www.charitynavigator.org/products-and-services/api/ | F |
| S2 | Charity Navigator Attribution Guidelines | undated | https://developer.charitynavigator.org/attribution | F |
| S3 | Charity Navigator developer terms summary | 2026-11-17 | https://developer.charitynavigator.org/termsofuse | F |
| S4 | Charity Navigator data-sharing page | undated | https://developer.charitynavigator.org/datasharing | F |
| S5 | Charity Navigator website Terms of Use | 2022-11-01 | https://www.charitynavigator.org/about-us/financials-and-policies/terms-of-use/ | F |
| S6 | Candid API License Agreement | 2026-09-14 | https://candid.org/terms-of-service/api-license-agreement/ | C (403 this run) |
| S7 | Candid API terms of service (portal) | 2026-09-07 | https://developer.candid.org/page/candid-api-terms-of-service.md | F |
| S8 | Candid License Agreement (APIs) (portal) | Dec 2023 | https://developer.candid.org/page/candid-license-agreement.md | F |
| S9 | Candid developer llms.txt | fetched 2026-11-20 | https://developer.candid.org/llms.txt | F |
| S10 | Every.org Charity API docs (intro, auth, nonprofits) | undated | https://docs.every.org/docs/endpoints/nonprofits | F |
| S11 | Every.org site terms | — | https://www.every.org/terms | not read (robots 429) |
| S12 | Pledge Terms of Service | 2025-01-15 | https://www.pledge.to/terms | F |
| S13 | Pledge Acceptable Use Policy | 2024-12-20 | https://www.pledge.to/acceptable-use-policy | F |
| S14 | Pledge MCP guide and tool reference | undated | https://developer.pledge.to/guides/mcp/ ; https://developer.pledge.to/reference/mcp/ | F |
| S15 | Pledge charity database, PledgeAI and API pages | undated | https://www.pledge.to/solutions/charity-database ; https://www.pledge.to/solutions/pledge-ai ; https://www.pledge.to/products/apis | F |
| S16 | Goodstack Standard Terms and Conditions | 2024-11-15 | https://goodstack.io/legal/standard-terms-and-conditions | F |
| S17 | Goodstack Vetting & Validation; Donation Service additional terms | 2024-11-15 | https://goodstack.io/legal/additional-terms-vetting-validation ; https://goodstack.io/legal/additional-terms-donation-service | F |
| S18 | Benevity Master Services Agreement | Feb 2026 | https://go.benevity.com/hubfs/website/legal/Master-Services-Agreement.pdf | F |
| S19 | Benevity SSI: Giving API | Apr 2026 | https://go.benevity.com/hubfs/website/legal/Benevity-SSI-Giving-API.pdf | F |
| S20 | Benevity SSI: General Terms; Data Export API; Premium Nonprofit Screening | Jan 2026; Dec 2025; Sep 2025 | https://go.benevity.com/hubfs/website/legal/Benevity-SSI-General-Terms.pdf (and sibling PDFs listed at https://benevity.com/software-and-service-information) | F |
| S21 | Benevity End User Terms of Use | 2025-12-24 | https://benevity.com/legal/end-user-terms-of-use | F |
| S22 | 17 U.S.C. 105 | 2023 ed. | https://www.govinfo.gov/content/pkg/USCODE-2023-title17/html/USCODE-2023-title17-chap1-sec105.htm | F |
| S23 | IRS EO BMF Extract page | data 2026-11-10 | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf | F |
| S24 | Rev. Proc. 2011-33 (IRB 2011-25) | 2011 | https://www.irs.gov/irb/2011-25_IRB | C |
| R1 | Repo: Candid licence clauses | — | [queue-sponsor-terms-data-clauses.md](queue-sponsor-terms-data-clauses.md) §5; [validation-wave9-report.md](validation-wave9-report.md) V9-06 | C |
| R2 | Repo: AI product census (AIP02 Daffy, AIP07 Chariot, AIP22 Candid) | — | [direction-ai-product-census.md](direction-ai-product-census.md) | C |
| R3 | Repo: A5 quadrant rationale; overlay methodology §7a/§7b | — | [quadrant-A2-A5-rationale.md](quadrant-A2-A5-rationale.md); [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) | C |
