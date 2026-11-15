# Queue batch 36 B: agent delegation in donor terms (P-B35C-01), delegation forms (P-B35B-03), DAFpay third-party clause (P-FCG-03), Louise controls (P-QA1-03), Benevity Match Assurance (P-QA2-06), Foundant and Foundation Source APIs (P-CON-07)

**Date:** 2026-11-15. Prepared by the batch 36 B agent. These are files only: no commit and no push.

**Method:** Desk research from public sources, 2021 onward. This is research, not legal advice.
- No accounts were created and nothing was logged in to.
- No forms were submitted, no one was contacted, and no API call needing a key was made.
- robots.txt was read on each host before fetching, and its rules were followed:
  - **www.foundant.com** disallows `anthropic-ai`, `ClaudeBot` and `Claude-Web`, so it was not fetched.
  - **foundationsource.com** disallows `*.pdf`, so the DAF OS tear sheet was not read. It is also hosted on HubSpot, outside the two allowed hosts.
  - **www.every.org** robots.txt could not be read (403 to curl, 429 to fetch), so the site was not fetched.
  - **sec.gov** robots.txt returned 403, so it was not used.
  - gspf.goldman.com and fcsuite.com disallow this agent and were not used.
- Pages that returned 403 to a plain request were not retried by other means. These were support.foundant.com and b-hive.benevity.com. Their content appears below only as search-index snippets, tagged [R].

**Read first (governing corrections included):**
- [queue-batch35-access-owners-faith.md](queue-batch35-access-owners-faith.md) §1
- [queue-batch35-agents-analysts-rails.md](queue-batch35-agents-analysts-rails.md) §1, including the wave-20 corrections. Composio and Corsair expose only gift creation, so they are not counted as documented fund debits.
- [ai-governance-failure-modes.md](ai-governance-failure-modes.md): F06, F16, §4.5 and §5. Its rule is "AI may add a flag, never clear one".
- [delegated-access-routes-2026.csv](../../data/mission-2026-11-14/delegated-access-routes-2026.csv) DA05–DA07
- [daf-agent-wrappers-2026.csv](../../data/mission-2026-11-14/daf-agent-wrappers-2026.csv) W01–W19

**Evidence tags:**
- **[F]** fact from a source read this batch.
- **[R]** search-index snippet; the page itself was not read.
- **[I]** inference.
- **[X]** carried from the repo.

**Outputs:**
- [`data/mission-2026-11-14/agent-delegation-terms-2026.csv`](../../data/mission-2026-11-14/agent-delegation-terms-2026.csv): 51 clause rows, AT01–AT51.
- [`data/mission-2026-11-14/queue-proposals-batch36b.csv`](../../data/mission-2026-11-14/queue-proposals-batch36b.csv): P-B36B-01 to P-B36B-03.

---

## 0. Answers in brief

| Item | Answer | Confidence |
|---|---|---|
| **P-B35C-01** Terms vs agents and wrappers | **No published term at Daffy, Endaoment or Chariot expressly permits or forbids giving a credential to a third-party tool router. All three put the loss from unauthorised use on the user.**<br>• **Daffy** sanctions agents the donor runs itself: every route "acts as you, on your fund" ([agents](https://docs.daffy.org/agents)). Its Member Agreement (2025-11-11) has no API or agent clause and says Daffy "is not responsible for any losses resulting from account fraud, theft, or any other unauthorized activity" ([agreement](https://www.daffy.org/legal/agreement)). Approved donations "cannot be canceled". **New finding:** a Daffy Financial Advisor "may be any individual, corporation, or trust" with its own login. That is a sanctioned entity delegate.<br>• **Endaoment** (T&C 2026-08-12) is the only one whose donor terms cover OAuth and API channels. It bars "API or Credential Abuse", makes the user "solely responsible" for API credentials and OAuth tokens, and makes transactions "without refunds". Its sanctioned third-party path is a **registered OAuth client**: Endaoment issues the client ID and secret after a joint validation.<br>• **Chariot**: there is no donor API. DAFpay terms are under P-FCG-03.<br>• **Every.org**: terms **not read**, because robots.txt could not be read. Its API has no donor write endpoint [X]. | High (texts read); not covered for Every.org |
| **P-B35B-03** Delegation forms | **None of the three routes admits a software service on its published terms.**<br>• **Vanguard: closed for entities.** The Policies & Guidelines say "Interested parties must be individuals; organizations and group names will not be accepted." The form (VCIP 081426, 2026-08-14) asks for a person's SSN digits or PIN, birth date and signature. It issues no credential; registration for online access is a separate step.<br>• **GS DAF: possible but unpublished.** The circular's only process is to contact the PWM team. No public form was found, and gspf.goldman.com is robots-disallowed.<br>• **SVCF: possible but unpublished.** The clause sits under the heading "THIRD-PARTY USE PROHIBITED". All three appointable roles are defined as "Individual", and no prior-approval form is public. | High (texts); [I] on feasibility |
| **P-FCG-03** DAFpay "on behalf of third parties" | **It bars an aggregator or agent service operating DAFpay for many donors. A donor's own agent is a grey zone.**<br>• Clause (c) bars using DAFpay "on behalf of or to provide services to third parties". The terms also forbid using "anyone else's DAF Provider accounts" and bypassing access controls.<br>• The terms define the user as "any individual who uses DAFpay on a nonprofit website". The 2FA consent assumes codes go to "your device(s)".<br>• The donor must also comply with the DAF provider's terms. So sponsor bot bans (batch 35B) also apply to DAFpay use.<br>• **OAuth flow:** the DAF-provider guides name **no different donor terms**. Chariot holds "scoped, revocable tokens — never donor credentials", and grants enter the sponsor's "normal review".<br>• **Credential storage:** the tension is unresolved. The privacy policy (2025-01-08) still says both "not stored" and "segmented storage of all Credentials". | High (texts); [I] on the own-agent reading |
| **P-QA1-03** Louise controls | **No public document states any Louise control.**<br>• The launch release says Louise can "execute real donor requests", for example setting up a recurring grant or contributing 100 NVDA shares. It states no limit, confirmation or audit log.<br>• The public help centre (36 articles) describes Louise only as a **support assistant**.<br>• What is documented is **GiveClear's** review: the IRS/OFAC check, the incidental-benefit check on grant notes, the funds check and a 48-hour review. A grant can be cancelled while pending.<br>• Nothing ties Louise-created actions to that path, though nothing suggests they bypass it [I].<br>• No SEC or FINRA record was found in the web index; sec.gov was not used. | High on absence in public docs |
| **P-QA2-06** Benevity Match Assurance | **On Benevity's own pages the AI does not approve. It extracts, checks and submits, and an admin decides. A separate rule-based auto-approval setting can remove the human, though.**<br>• Release: AI reads receipts, "verify eligibility, and auto-submit matching requests".<br>• Blog (2026-03-25): AI builds the submission "before it even reaches program administrators".<br>• Help-centre snippets [R]: AI validation "does not approve or decline", and the admin keeps final authority.<br>• Admins can separately auto-approve **all** requests, or those **under a threshold** [R].<br>• **The 30%→<3% figure is one client** ("one of our global partners"). It is a decline rate on submissions and measures errors caught earlier, not a false-approval rate [I]. | Medium-high (two key pages [R]) |
| **P-CON-07** Foundant / Foundation Source APIs | **Neither vendor publishes objects, auth, read/write scope or price on its public pages.**<br>• **Foundant** [R]: "API Connections" is an à la carte add-on announced in October 2025. Objects are documented inside CommunitySuite, and support does not answer technical API questions.<br>• **Foundant** [F, via Chariot]: one donor-consented write connection exists. DAFpay can show the fund, confirm funds, **submit grant recommendations** and check status. It "cannot move money and cannot act on its own".<br>• **Foundation Source:** "programmable" and "programmatic grantmaking" are claims only. The only API named on foundationsource.com is an **inbound** BridgeFT custodial-data feed. | Medium (Foundant [R]); high on FS absence |

---

## 1. P-B35C-01: do donor terms allow delegation to an AI agent or third-party automation?

### 1.1 Clause comparison

| Topic | Daffy | Endaoment | Chariot (DAFpay) | Every.org |
|---|---|---|---|---|
| Document read | [Member Agreement](https://www.daffy.org/legal/agreement), updated 2025-11-11; [Privacy](https://www.daffy.org/legal/privacy), 2021-09-30; [agent docs](https://docs.daffy.org/agents) | [T&C](https://docs.endaoment.org/governance/documentation/terms-and-conditions.md), 2026-08-12; [developer docs](https://docs.endaoment.org/developers/quickstart/overview.md) | [Donor Terms](https://www.dafpay.com/donor-terms-of-use), eff. 2025-09-24; [Privacy](https://www.dafpay.com/privacy-policy), eff. 2025-01-08 | **not read** (robots.txt unverifiable) |
| API or agent named in terms | **No.** No API, MCP or agent clause (AT01) | **Yes.** "API Access" includes "OAuth or similar authorized integrations"; "OAuth consent, and API credential acceptance constitute valid assent" (AT10) | No donor API. The user is an "individual" on a nonprofit website (AT19) | unknown |
| Donor's own agent | **Sanctioned in docs**: MCP, CLI, skill file, REST; "acts as you" (AT05) | Not addressed in the T&C. OAuth apps act for the user | Not addressed | — |
| Third-party app holding the credential | **Silent.** The docs say to keep the key in "the environment, the credentials file or your MCP client's configuration" (AT06). In 2023 Daffy invited outside apps to integrate (AT08) | **Registered apps only**: "Request OAuth credentials from us"; production secrets come after validation (AT14). Tokens "must stay on your server" (AT15) | **Barred for services**: (c) "on behalf of or to provide services to third parties" (AT20) | unknown |
| Entity delegate | **Yes.** Financial Advisor "may be any individual, corporation, or trust", with its own login (AT03) | Advisor collaboration; "All donation suggestions require client approval" (AT16) | No | — |
| Unauthorised-use loss | On the member (AT02) | On the user, including "credentials we do not issue" (AT12) | Liability capped at US$1,000; security failures excluded (AT24) | unknown |
| Reversal or refund | Issued donations "cannot be canceled"; report errors in 10 days (AT04) | "irreversible, final, and without refunds" (AT13) | none stated | — |

### 1.2 Readings [I]

1. **Wrapper use is unaddressed, not authorised.** No terms forbid a donor from pasting a Daffy key into Composio, Pipedream or Zapier. Daffy's own 2023 launch invited third-party apps.
   - The loss clause still means a donation made through a compromised wrapper is the member's loss.
   - So the F16 credential-compromise exposure rests on the donor, not on Daffy or the wrapper.
   - Whether a wrapper's own terms take on any liability was not examined.
2. **Endaoment's design is the cleanest delegation model.** Third-party software gets its own OAuth client registration. Endaoment validates it before production, and the donor consents to that client.
   - A generic router that relays a donor token without its own registration falls outside the documented path.
   - The published scopes are data scopes only. No scope narrows grant submission.
3. **Daffy's corporate Financial Advisor is the one entity-delegate route found in any donor contract read.** Two things weaken it:
   - Advisor actions "are represented as actions taken by the Organizer directly", so platform records would not separate the agent from the donor (F06).
   - Whether such an account can hold its own API key is not documented. See P-B36B-01.
4. **Every.org is not yet covered.** The open question matters only for web-login automation, because its API has no donor write path. See P-B36B-03.

---

## 2. P-B35B-03: the three top-20 delegation routes

| Route | Document read | Can an entity be named? | Data and actions | Credentials issued to appointee? | Change from batch 35 |
|---|---|---|---|---|---|
| **Vanguard Charitable**: Interested Party | [Form VCIP 081426](https://www.vanguardcharitable.org/sites/default/files/2026-08/vcip_interested_party_access_081426.pdf) (2026-08-14, 3 pp.); [Policies & Guidelines](https://www.vanguardcharitable.org/company-policies/policies-and-guidelines) (PDF 2026-03-12) | **No.** "Interested parties must be individuals; organizations and group names will not be accepted." The form asks for SSN last 4 or PIN, birth date and the appointee's signature | Five levels:<br>• Primary Contact<br>• Full: recommend grants and exchanges<br>• Read-only + Exchange<br>• Read-only<br>• Paper statement<br>Only Primary Contact appears to include "Permission to share account information to authorized 3rd parties" [I, from glyph layout] | Not by the form. Appointees "can register for online account access" separately. The User Agreement aggregator clause still applies to that person's own login [X] | Entity: **P → N**. Software route: aggregator use by an individual Authorized Person only |
| **GS DAF**: agent | Program Circular, App. B of the [FireAid report](https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf) (as of 2025-09-08, corrected 2025-09-26) | **Possibly.** "you can authorize your Goldman Sachs Private Wealth Management team (or another third party) to act as your agent" | "some or all of your advisory privileges and access to account information". The donor web is open to "donors (and their authorized agents)": grants, balances, recurring grants | Not stated. Process: "please contact your Goldman Sachs Private Wealth Management team" | Unchanged. **No public form**; gspf.goldman.com is robots-disallowed; search found only 2017-era circulars there |
| **SVCF**: prior approval | [DAF Agreement](https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf) (PDF modified 2025-08-22) | **Possibly**, by approval. The clause sits under "THIRD-PARTY USE PROHIBITED". All roles are defined as "Individual" | Only Fund and Secondary Advisors may recommend grants in the portal. Fund Representative: information only. Automated collection is allowed only for the advisor's own grantmaking purposes | Not stated. Unapproved access is "solely at the Authorized Advisor's risk", with indemnity | Unchanged. **No approval form or process published** |

**Reading [I]:**
- After this batch, **no top-20 route admits a software service on published terms.**
- Two routes remain possible: GS DAF and SVCF. Both depend on unpublished sponsor discretion, and checking them would need outreach, which is barred.
- Vanguard now joins Fidelity as "individuals only".
- Proposed changes to the agent-access matrix (not applied):
  - Vanguard: "human delegation only (individual); automated read via the individual's own login".
  - GS DAF: "agent appointment via PWM; mechanics unpublished".
  - SVCF: "third-party access by unpublished prior approval".

---

## 3. P-FCG-03: does the DAFpay third-party clause bar agent or aggregator use?

**The text** ([Donor Terms](https://www.dafpay.com/donor-terms-of-use), effective 2025-09-24) [F]:
- **Clause (c):** the donor agrees not to "rent, lease, provide access to or sublicense any elements of DAFpay to a third party or use DAFpay on behalf of or to provide services to third parties".
- **Clause (b):** the donor agrees not to "bypass or circumvent measures designed to prevent or limit access".
- **Other accounts:** "You must not (1) use or access anyone else's DAF Provider accounts or related data".
- **User definition:** "any individual who uses DAFpay on a nonprofit website to effect a donation through his or her DAF".
- **Consents:**
  - credential use ("permission to use the DAF Provider credentials you supply");
  - 2FA triggering ("two factor authentication codes sent to your device(s)").
- **Provider terms:** DAF Users must comply "with any terms applicable to their use of a DAF Provider, including the use of a DAF Provider with Chariot".
- **Liability:** capped at US$1,000.

**Readings [I]:**
1. **Aggregator or agent service: barred.** An operator that runs DAFpay sessions for several donors uses DAFpay "to provide services to third parties". It also handles "anyone else's" provider accounts.
2. **A donor's own agent: not clearly barred, but not clearly allowed.**
   - Against the bar: the agent acts for the donor, not "on behalf of" a third party.
   - Against allowing it: the defined user is an individual on a nonprofit website, and 2FA codes go to the donor's device, so an agent would need the code relayed.
   - The provider-terms clause brings in sponsor bot bans (NCF, Vanguard, NPT; batch 35B). Through that clause, a credential-pass-through agent session is likely non-compliant at those sponsors.
3. **OAuth flow:** the DAF-provider guides ([overview](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md), [security](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/security.md), [API endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md)) name **no separate donor terms**.
   - Chariot holds "scoped, revocable tokens — never donor credentials".
   - It stores refresh tokens "encrypted at rest (envelope encryption, per-token data keys)".
   - Create Grant "does not bypass your compliance process".
   - So the donor contract for an OAuth session is the same Donor Terms by default [I].
4. **"Not stored" vs "segmented storage":** both sentences remain in the [privacy policy](https://www.dafpay.com/privacy-policy).
   - The OAuth guide shows Chariot does store **tokens** for OAuth providers. "All Credentials" may mean tokens and nonprofit logins.
   - The policy does not say so, so the tension stands. Resolving it would need outreach.
5. **Nonprofit side:** Chariot's [Nonprofit Terms](https://www.givechariot.com/legal-nonprofit) (updated 2026-10-14) repeat clause (c). They let credentials go only to "agents of your organization", meaning staff.

---

## 4. P-QA1-03: what do Louise's controls enforce?

| Source | What it says | Tag |
|---|---|---|
| [Launch release, 2025-10-27](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html) | "execute real donor requests within the charitable experience". Examples: "Set up a monthly recurring $100 grant", "Contribute 100 shares of NVDA stock", "Add one of my children to my DAF". **No limit, confirmation, audit or GiveClear reference** | F |
| [TIFIN Give FAQs](https://intercom.help/give-ria/en/articles/9845503-tifin-give-faqs); [Granting FAQs](https://intercom.help/give-ria/en/articles/10670838-granting-faqs) | Louise is the "AI Assistant" for inquiries: "Please use the AI Assistant for all grant related questions!" No article describes Louise taking actions or its controls (36 articles in 6 collections enumerated) | F |
| [Granting FAQs](https://intercom.help/give-ria/en/articles/10670838-granting-faqs) | GiveClear reviews every grant recommendation: IRS and OFAC standing; no more than incidental benefit; available funds. Statuses run Submitted → Pending → Approved → Processed. A grant "in 'pending' status … you can still Cancel" | F |
| [Program Guidelines](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines) | Grants are "reviewed for approval within 48 hours of submission"; contributions are "reviewed prior to acceptance". TIFIN Give's entity is "Louise Giving Technologies LLC" | F |
| tifin.com Louise page | Returns 404. A search snippet says Louise helps donors "discover causes, move money, and manage family giving" | R |
| SEC / FINRA | sec.gov robots.txt returned 403, so it was not used. A web-index search for the entity found no ADV or CRD record | R |

**Reading [I]:**
- The public record supports **sponsor separation in general**: GiveClear review sits between submission and payment, and a pending grant can be cancelled.
- It shows **no Louise-specific control**: no per-action limit, no confirmation step, and no audit field identifying the agent.
- Y3 stays at 1 on public evidence. Documentation, a demo or customer material is still needed (P-QCAL-06).
- The release's examples include **adding a family member**. That is an account-permission change, not only a grant. It widens the F06 scope beyond money movement.

---

## 5. P-QA2-06: can Match Assurance AI approve eligibility without human review?

| Source | Statement | Tag |
|---|---|---|
| [Benevity Live! 2026 release](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026) (2026-06-04) | "uses AI to read employee donation receipts, verify eligibility, and auto-submit matching requests". External match decline rate "from 30% to less than 3%" | F |
| [Blog](https://benevity.com/blog/ai-corporate-giving-impact) (2026-03-25) | AI helps "build the submission before it even reaches program administrators". Submission checks "flag missing or inconsistent information". **"one of our global partners saw their match decline rates drop from roughly 30% to under three percent"** | F |
| [AI CSR platform page](https://benevity.com/solutions/ai-csr-platform) | AI "never takes an irreversible action without human confirmation" (product-wide principle) | F |
| [Responsible AI Policy](https://benevity.com/legal/responsible-ai-policy) (2026-01-26) | "decisions with material impact on individuals or organizations remain human-led"; §6.4 Human-in-the-Loop | F |
| [Release spotlight](https://community.benevity.com/product-updates/new-match-assurance-and-ai-grant-summaries-responsible-ai-policy-256) (2026-02-25) | Launch on March 3; AI extracts receipt data | F |
| [b-hive: Reviewing external match requests with AI insights](https://b-hive.benevity.com/hc/en-us/articles/50596192541588-Reviewing-external-match-requests-with-AI-insights) | AI validation highlights discrepancies and **does not approve or decline**. The admin keeps final authority; the reviewer needs the external match manager role. Not applied retroactively | R (403) |
| [b-hive: automatic approvals](https://b-hive.benevity.com/hc/en-us/articles/4402119509524) | Admins can choose no auto-approval, auto-approve all, or auto-approve at or below a threshold | R (403) |

**Readings [I]:**
1. **The AI does not hold approval authority.** It pre-fills the request, checks it and files it, which is the "add a flag" side of the rule. That fits the repo's add-only rule more closely than the provisional RED assumed.
2. **The no-human path is a company rule setting, not AI.** If a company turns on auto-approval for all requests or under a threshold, a request the AI built and checked can be approved with no admin. How the AI "Verified" flag interacts with that setting is not public. See P-B36B-02.
3. **The 30%→3% metric is weak evidence.** It comes from one early adopter and counts declined submissions. A falling decline rate could mean better submissions, laxer review, or both. There is **no false-approval rate**.
4. **Suggested overlay change (not applied):** move A5 Benevity from **RED (provisional) to AMBER**. The basis is that the AI does not approve and humans approve by default. Keep a note that rule-based auto-approval can remove human review.

---

## 6. P-CON-07: Foundant CommunitySuite API and Foundation Source DAF OS

| Vendor | What is public | Objects | Read/write | Auth | Price | Tag |
|---|---|---|---|---|---|---|
| **Foundant CommunitySuite**: "API Connections" add-on | Snippets from [Integrations](https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations) and the 2025 release notes: optional à la carte add-on with a Marketplace, announced October 2025. Docs sit in-app under System Data > Integrations. "Users will be responsible for setup", and support will not answer technical questions. New objects are added as the library grows. A 2024 note mentions a scholarship-ID endpoint and Power BI reporting | not published | not published | not published | not published | R |
| **Foundant CommunitySuite**: DAFpay connection | [Chariot article](https://www.givechariot.com/resources/insights/-dafpay-foundant-how-community-foundations-using-communitysuite-can-enable-dafpay-): the foundation enables DAFpay; each fund advisor consents to a connection. It can display the fund name, confirm available funds, **submit grant recommendations** and check their status. "DAFpay cannot move money and cannot act on its own." Free to foundations | fund, balance, grant recommendation, status | read + **write (recommendation)** | fundholder-authorised connection (method not named) | $0 to foundation | F |
| **Foundation Source DAF OS** | [Product brief](https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/) (2025-10-13; modified 2026-05-18): "a complete, programmable administration platform"; "automated money movement, programmatic grantmaking". No developer docs on foundationsource.com | not published | not published | not published | not published | F (absence) |
| **Foundation Source turnkey DAF** | [Release, 2025-09-23](https://foundationsource.com/?p=4768): "adds custodial data access via BridgeFT's API" | custodial data (inbound) | inbound read | — | — | F |

**Readings [I]:**
- **Foundant shows that its CommunitySuite DAF ledger can accept a donor-consented write from an outside app**, namely DAFpay grant recommendations, with staff review kept. That is the shape a compliant agent route would need.
- That capability is shown only for one named partner. The general API add-on's objects and scopes are not public, and www.foundant.com could not be read.
- **Foundation Source's "programmable" claim has no public technical substance** on its own site. The only API it names is an inbound custodial feed.

---

## 7. Limits

- The Every.org terms, the b-hive.benevity.com articles, support.foundant.com and www.foundant.com were not read (robots rules or 403). Rows from them are [R] or absent.
- The GS DAF circular is a third-party copy, undated, inside the FireAid report. It may lag the current Goldman-hosted version.
- The Vanguard access-level mapping for the "share with authorized 3rd parties" row is read from checkmark glyph positions in the PDF.
- Terms describe rights and allocation, not practice. No sponsor was asked how it treats agent sessions.
- The Louise and Match Assurance findings rest on public marketing and help pages; neither product was tested.

---

## Source register

| # | Source | Type | Date | Accessed | URL |
|---|---|---|---|---|---|
| S1 | Daffy Member Agreement | sponsor contract | 2025-11-11 | 2026-11-15 | https://www.daffy.org/legal/agreement |
| S2 | Daffy Privacy Policy | sponsor policy | 2021-09-30 | 2026-11-15 | https://www.daffy.org/legal/privacy |
| S3 | Daffy agent, auth, MCP, CLI docs; llms.txt | sponsor docs | undated | 2026-11-15 | https://docs.daffy.org/agents ; https://docs.daffy.org/auth ; https://docs.daffy.org/agents/mcp ; https://docs.daffy.org/agents/cli ; https://www.daffy.org/llms.txt |
| S4 | Daffy for Developers launch; developer page | sponsor blog | 2023-05-24 | 2026-11-15 | https://www.daffy.org/resources/api-for-developers ; https://www.daffy.org/developer |
| S5 | Endaoment Terms and Conditions | sponsor contract | 2026-08-12 | 2026-11-15 | https://docs.endaoment.org/governance/documentation/terms-and-conditions.md |
| S6 | Endaoment developer overview, production, integration patterns, advisor workflow | sponsor docs | undated | 2026-11-15 | https://docs.endaoment.org/developers/quickstart/overview.md ; https://docs.endaoment.org/developers/quickstart/going-to-prod.md ; https://docs.endaoment.org/developers/quickstart/integration-patterns.md ; https://docs.endaoment.org/advisors/collaboration/workflow.md |
| S7 | Every.org API authentication | platform docs | undated | 2026-11-15 | https://docs.every.org/docs/endpoints/authentication |
| S8 | DAFpay Donor Terms of Use | vendor contract | eff. 2025-09-24 | 2026-11-15 | https://www.dafpay.com/donor-terms-of-use |
| S9 | DAFpay Privacy Policy | vendor policy | eff. 2025-01-08 | 2026-11-15 | https://www.dafpay.com/privacy-policy |
| S10 | Chariot DAFpay OAuth guides (overview, requirements, security, checklist, endpoints) | vendor docs | API v2026-04-01 | 2026-11-15 | https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/overview.md (and sibling pages) |
| S11 | Chariot Nonprofit Terms | vendor contract | 2026-10-14 | 2026-11-15 | https://www.givechariot.com/legal-nonprofit |
| S12 | Vanguard Charitable Interested party access form VCIP 081426; forms index | sponsor form | 2026-08-14 | 2026-11-15 | https://www.vanguardcharitable.org/sites/default/files/2026-08/vcip_interested_party_access_081426.pdf ; https://www.vanguardcharitable.org/forms |
| S13 | Vanguard Charitable Policies & Guidelines | sponsor policy | 2026-03-12 | 2026-11-15 | https://www.vanguardcharitable.org/company-policies/policies-and-guidelines |
| S14 | GS DAF Program Circular (FireAid report App. B) | sponsor doc via third party | report 2025-09-08 / 2025-09-26 | 2026-11-15 | https://www.fireaidla.org/assets/press-releases/pdfs/fireaid_investigative_report_09-08-2025.pdf |
| S15 | SVCF Donor Advised Fund Agreement | sponsor contract | 2025-08-22 | 2026-11-15 | https://www.svcf.org/assets/img/media/svcf-donor-advised-fund-agreement.pdf |
| S16 | TIFIN Give Louise launch | vendor PR | 2025-10-27 | 2026-11-15 | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html |
| S17 | TIFIN Give help centre (collections; FAQs; Granting FAQs; Program Guidelines) | vendor/sponsor docs | undated | 2026-11-15 | https://intercom.help/give-ria/en/ ; https://intercom.help/give-ria/en/articles/9845503-tifin-give-faqs ; https://intercom.help/give-ria/en/articles/10670838-granting-faqs ; https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines |
| S18 | Benevity Live! 2026 release | vendor PR | 2026-06-04 | 2026-11-15 | https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026 |
| S19 | Benevity blog: AI corporate giving | vendor blog | 2026-03-25 | 2026-11-15 | https://benevity.com/blog/ai-corporate-giving-impact |
| S20 | Benevity AI CSR platform page; Responsible AI Policy | vendor | 2026-01-26 (policy) | 2026-11-15 | https://benevity.com/solutions/ai-csr-platform ; https://benevity.com/legal/responsible-ai-policy |
| S21 | Benevity community release spotlight | vendor | 2026-02-25 | 2026-11-15 | https://community.benevity.com/product-updates/new-match-assurance-and-ai-grant-summaries-responsible-ai-policy-256 |
| S22 | Benevity b-hive help articles (2) | vendor help (snippets) | undated | 2026-11-15 | https://b-hive.benevity.com/hc/en-us/articles/50596192541588-Reviewing-external-match-requests-with-AI-insights ; https://b-hive.benevity.com/hc/en-us/articles/4402119509524 |
| S23 | Foundant Integrations; CommunitySuite release notes 2025 | vendor help (snippets) | 2025 | 2026-11-15 | https://support.foundant.com/hc/en-us/articles/35148153853847-Integrations ; https://support.foundant.com/hc/en-us/articles/26781305176215-CommunitySuite-Release-Notes-2025 |
| S24 | Chariot: DAFpay + Foundant | vendor | undated | 2026-11-15 | https://www.givechariot.com/resources/insights/-dafpay-foundant-how-community-foundations-using-communitysuite-can-enable-dafpay- |
| S25 | Foundation Source DAF OS product brief | vendor | 2025-10-13 / 2026-05-18 | 2026-11-15 | https://foundationsource.com/resources/product-briefs/the-modern-operating-system-for-donor-advised-funds/ |
| S26 | Foundation Source turnkey DAF release | vendor PR | 2025-09-23 | 2026-11-15 | https://foundationsource.com/?p=4768 |

**Blocked or not used:**
- **robots.txt:** www.foundant.com (Anthropic agents barred), foundationsource.com `*.pdf`, gspf.goldman.com, fcsuite.com. Unreadable robots.txt: www.every.org and sec.gov.
- **HTTP 403:** support.foundant.com and b-hive.benevity.com.
- **HTTP 404:** tifin.com news pages and daffy.org/legal/terms.
- **Out of host scope:** the HubSpot-hosted DAF OS tear sheet.

---

## Data dictionary

### `data/mission-2026-11-14/agent-delegation-terms-2026.csv` (one row per clause or finding)

| Column | Meaning |
|---|---|
| term_id | AT01–AT51 |
| queue_item | Queue question the row answers |
| platform | Sponsor or vendor |
| document, document_date | Document title and its stated or metadata date |
| source_url | Primary URL |
| read_status | `read in full`, `read (targeted)`, `read (agent passages)`, or `not read: <reason>` |
| evidence_label | F, R, I, X (see tags above) |
| clause_topic | e.g. `agent_or_api_clause`, `unauthorized_loss`, `entity_delegate`, `third_party_services`, `credential_storage`, `sponsor_review`, `human_review`, `auto_approval`, `api_objects` |
| clause_present | Y, N, P (partial or ambiguous), unknown |
| key_quote | Verbatim quote, 40 words or fewer (blank for [R] rows, which are paraphrased in `reading`) |
| delegation_effect | Short effect on agent or third-party delegation (permits, silent, restricts, bars, unknown, etc.) |
| reading | Interpretation, tagged [F], [I] or [R] |
| retrieved | Access date |
| notes | Supporting passages and caveats |

### `data/mission-2026-11-14/queue-proposals-batch36b.csv`

Columns and scales follow [queue-proposals-README.md](../../data/mission-2026-11-14/queue-proposals-README.md):
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.
- `proposed_by` is `batch36 B agent`.
- `evidence_pointer` cites AT rows and URLs.
