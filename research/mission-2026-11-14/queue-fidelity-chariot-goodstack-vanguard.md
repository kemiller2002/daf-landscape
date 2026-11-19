# Queue items: Fidelity EFT and data export, DAFpay Donor Terms, Goodstack, Vanguard Charitable API hosts

Mission 2026-11-14. FCGV agent. Retrieved 2026-11-14.

Queue items covered: P-PAY-01 and P-QCAL-03 (Fidelity Charitable), P-NPT-04 (Chariot DAFpay Donor Terms), P-QA2-05 (Goodstack), P-WAT-03 (Vanguard Charitable `api-give` host).

**Recency rule.** Only 2021-and-later evidence is used for current-state findings. No pre-2021 source is relied on below.

**Evidence tags**
- [F] First-party: the entity's own page, document or server response.
- [S] Secondary: a third-party page, a forum post, or a search-engine summary.
- [I] Inference by this agent.

**Method limits**
- The Wayback Machine availability API (`archive.org/wayback/available`) answered. `web.archive.org` itself, including the CDX API and snapshot pages, reset the connection, and the fetch tool refused it. Snapshot timestamps are therefore known, but their text is not.
- Bogleheads returned HTTP 402 to the fetch tool.
- No log-ins, form submissions or authenticated calls were made. On Vanguard Charitable hosts, only unauthenticated `GET` requests to the root and to standard public paths were sent.

---

## 1. Summary of findings

| Item | Finding | Confidence |
|---|---|---|
| **P-PAY-01 / P-QCAL-03: EFT** | **No change on Fidelity's own pages.** On 2026-11-14 the nonprofit page still says Fidelity "does not currently require EFT enrollment". The FAQ still says never-enrolled nonprofits get "checks mailed to the addresses listed on your organization's IRS Form 990" [F]. **No Fidelity-hosted text with the July 1, 2026 date or the extension was found** in live pages, the EFT enrollment form PDF (modified 2025-12-18) or the Program Guidelines. The wording of the original notice is known only from forum extracts. The extension is known only from a forum extract, which a search summary dates to 2026-05-07, with no new date given [S]. Wayback holds the FAQ at 2026-01-16, 2026-02-17, 2026-05-13 and 2026-08-07, but those snapshots could not be read from here. | High on current text. Low on the wording and date of the original notice and the extension. |
| **P-QCAL-03: data export** | **No documented donor data export beyond per-document PDFs.** Fidelity's how-to (PDF, 2026-05-26) gives one route: History → "Statements & confirmations" → "Click the document name to view and download the PDF" [F]. The Program Guidelines give account holders the privilege "to view, but not necessarily modify" contribution and grant history [F]. No CSV, API or portability statement was found. Grants to other DAF sponsors are allowed but "do not qualify as grant activity" for the inactivity rule [F]. | Medium-high that nothing public exists. A logged-in view was not checked. |
| **P-NPT-04: DAFpay Donor Terms** | **Found.** The document is at [dafpay.com/donor-terms-of-use](https://www.dafpay.com/donor-terms-of-use), "Effective Date: September 24, 2025", not the 2025-01-01 date in the earlier search snippet. In a real browser, `givechariot.com/legal-donors` redirects to `/home`, so it is dead, not blocked. Chariot's Nonprofit Terms link to the dafpay.com URL [F]. Key points:<br>- the donor authorizes Chariot to use the donor's DAF Provider credentials<br>- Chariot may fill in grant purpose and allocation defaults<br>- Chariot's liability is capped at US$1,000<br>- the donor may not use DAFpay "on behalf of or to provide services to third parties"<br>- **there is no clause on automated or agent-driven sessions** | High (document read in full) |
| **P-QA2-05: Goodstack** | Named customers on its own site include **Google, LinkedIn, Canva, Atlassian, HSBC, ING, Asana, monday.com, Twilio, Hootsuite, Splunk and New Relic**. The KYNP post adds ElevenLabs. Coverage is "240+ countries and territories" (245 ISO codes in its docs). The registries it names include **IRS** and **UK Charity Commission**, and the API has a USA group-exemption flag [F]. **No US DAF sponsor or grant platform was found using Goodstack for eligibility.** **New fact:** Goodstack's donation rails run through its own DAF-style foundations. In the US this is **Percent Impact Foundation (EIN 87-3165286)**, now named "Goodstack Impact Foundation US" at ProPublica. The repo's own 990 harvest shows it reported **7,268 DAFs and $1.81m year-end DAF value for FY2024** [F]. | High (customers, registries). Medium (no DAF use, which is an absence). |
| **P-WAT-03: `api-give`** | `api-give.vanguardcharitable.org` is an **AWS API Gateway regional custom domain** (`d-s8mdizdfu5.execute-api.us-east-1.amazonaws.com`). It answers `403 {"message":"Forbidden"}` (`ForbiddenException`) on the root, `robots.txt` and common doc paths. Its certificate is Amazon-issued with a single SAN, valid 2026-07-28 to 2027-02-10. No public docs are exposed, so **what it carries is still unknown**. **New:** a sibling host, `api-tungsten.vanguardcharitable.org`, serves a public Swagger UI. It describes a "Tungsten API Gateway" connecting "KOFAX/Tungsten document capture with Salesforce FSC and Documentum ECM", with Auth0 JWT on protected endpoints. It does not mention Give. No new donor-facing host has appeared. The donor log-in is still `client.` → Salesforce SAML. | High on what is observable. Content of `api-give` is unknown. |

---

## 2. P-PAY-01 / P-QCAL-03: Fidelity Charitable EFT notices

### 2.1 Live first-party text, re-checked 2026-11-14

- **Nonprofit page.** "Fidelity Charitable does not currently require EFT enrollment but encourages enrolling for safer grantmaking." ([nonprofits.html](https://www.fidelitycharitable.org/nonprofits.html)) [F]
- **Nonprofit FAQ** ([nonprofits/faqs.html](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F]:
  - Under the question "Does Fidelity Charitable require Electronic Funds Transfer (EFT) to receive grants?", it says: "As Fidelity Charitable moves towards a digital-first policy we are transitioning grant payments to EFT".
  - "While we do not currently require EFT enrollment for nonprofit organizations, we encourage you to enroll for more secure grantmaking."
  - "Nonprofits that have never enrolled in our EFT program receive grants through checks mailed to the addresses listed on your organization's IRS Form 990."
  - Where board policy forbids EFT, it says: "We encourage you to work with your board to update your policy so you can continue receiving grants".
- **EFT page.** It sets no deadline ([nonprofits/eft.html](https://www.fidelitycharitable.org/nonprofits/eft.html)) [F].
- **EFT enrollment form** (PDF created 2025-12-02, modified 2025-12-18, `last-modified` 2025-12-22). It contains no date or EFT-only rule. "A VOIDED CHECK IS REQUIRED TO SIGN UP FOR EFT" refers to ACH enrollment ([form PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf)) [F]. [I] The form was revised in December 2025, the same month the forum thread says the notice appeared. The form itself carries no notice text.
- **Stripe grants page.** It has no date or requirement ([fidelity-grant.html](https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html)) [F].
- **Year-end deadlines page.** Its "EFT" row refers to donor contributions, not grants ([year-end deadlines](https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html)) [F].

### 2.2 Wording of the original notice and the extension (secondary only)

| Event | Text | Source | Tag |
|---|---|---|---|
| Original notice (thread opened Dec 2025) | "Beginning July 1, 2026, all Fidelity Charitable grants will be delivered exclusively through EFT and we will no longer issue grants through paper checks. To continue receiving grants after this date, enroll in EFT." | Bogleheads extract quoting Fidelity's FAQ, as returned by search ([thread](https://www.bogleheads.org/forum/viewtopic.php?t=464478)) | [S] |
| Chariot reading (May 2026) | Unenrolled organizations "will not be able to receive grants from Fidelity Charitable at all"; "June 30 Fidelity enrollment deadline" | [Chariot](https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors) | [S], from a vendor of a competing rail |
| Extension | "Fidelity Charitable has extended our EFT requirement date to allow organizations sufficient time to enroll". A search summary dates the post to 2026-05-07 and notes that a reply found no new date on the FAQ | Bogleheads page 5 ([p=8700839](https://www.bogleheads.org/forum/viewtopic.php?p=8700839)) | [S]. The date comes from a search summary, not the post |
| Current state | "not currently require"; checks go to the Form 990 address | Fidelity live pages (§2.1) | [F] |

**Archived snapshots that exist but could not be read** (from the Wayback availability API; the text was not retrieved):
- `nonprofits/faqs.html`: 20260116162819, 20260217233803, 20260513104410, 20260807223426.
- `nonprofits.html`: 20260224002738, 20260608193911, 20261014124128.
- `nonprofits/eft.html`: 20260131111617, 20260414031638.

[I] Comparing the 2026-05-13 FAQ snapshot with the 2026-08-07 one would bound the date of the extension wording. Comparing either with today's page would show when "not currently require" replaced the extension wording. That work is proposal P-FCG-01.

### 2.3 Status as of 2026-11-14

1. **The EFT-only rule is not in force on the public record.** Fidelity's own text describes checks as the live fallback [F].
2. **No new effective date was found** on any Fidelity page or PDF, or in any secondary source.
3. **Held versus mailed.** No Fidelity text says grants are held. The documented fallback is a mailed check [F].

### 2.4 Donor data export

- **How-to PDF** (created 2026-05-26). Steps: "Locate the 'History' tab … select 'Statements & confirmations.'" Document types are statements, contribution tax receipts, grant confirmations and Form 8283, and the last step is "Click the document name to view and download the PDF" ([how-to PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf)) [F].
- **Program Guidelines** (PDF created 2026-09-11). Account holders may "view, but not necessarily modify, all Giving Account information, including contribution and grant history, statements" ([guidelines](https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf)) [F]. That is a view right, not an export or portability right.
- **Transfers out.** The guidelines allow grants to other DAF sponsors, and say they "do not qualify as grant activity for the purposes of the minimum grant requirement" [F]. The FAQ index covers only inbound transfers ("Can I transfer my account with another donor-advised fund (DAF) sponsor to Fidelity Charitable?") ([FAQ index](https://www.fidelitycharitable.org/faqs/all.html)) [F].
- **Nonprofit side, for contrast.** Stripe-enrolled nonprofits can view and export grant details in their Stripe dashboard ([nonprofit FAQ](https://www.fidelitycharitable.org/nonprofits/faqs.html)) [F].
- **Searches found no** donor CSV export, API, advisor data-feed page or portability statement.

**Scoring implication** [I]. For Fidelity's A1 and A3/A4 Y (data portability), the evidence supports "PDF documents only; no machine-readable export documented". This does not support raising Y1 or Y2. For the A2 EFT score, the evidence does not support "EFT-only in force".

---

## 3. P-NPT-04: DAFpay Donor Terms of Use

**Location.**
- Chariot's [Nonprofit Terms](https://www.givechariot.com/legal-nonprofit) link to `https://www.dafpay.com/donor-terms-of-use` and `https://www.dafpay.com/privacy-policy` [F].
- In Playwright Chromium, `www.givechariot.com/legal-donors` and `givechariot.com/legal-donors` both end at `https://www.givechariot.com/home`. That is a redirect, not bot-blocking [F].
- `legal-donors` is not in [pages-sitemap.xml](https://www.givechariot.com/pages-sitemap.xml). The sitemap lists `legal-nonprofit`, `legal-nonprofit-enterprise`, `legal-daa`, `dafpay-provider-addendum`, `disbursements-addendum`, `digital-mailbox-addendum` and `privacy` [F].
- The DAFpay Provider Addendum (2026-10-14) says donors authorize Chariot "under the DAFpay Donor Terms of Use", but it does not link to them [F].

**Text** ([dafpay.com/donor-terms-of-use](https://www.dafpay.com/donor-terms-of-use), "Effective Date: September 24, 2025", © 2024 footer; rendered 2026-11-14) [F]:

| Question in the queue | What the terms say |
|---|---|
| Automated or agent-driven sessions | **Not addressed.** There is no mention of bots, agents, automation or AI. The nearest clauses: the donor must not "use DAFpay on behalf of or to provide services to third parties", must not "bypass or circumvent measures designed to prevent or limit access", and must not "access DAFpay for competitive purposes or publish any benchmark". A "DAF User" is "any individual who uses DAFpay on a nonprofit website". |
| Credential pass-through | The donor warrants "requisite authority to give to Chariot permission to use the DAF Provider credentials you supply to log into your DAF Provider account". The donor also consents to Chariot "triggering the transmission of any two factor authentication codes". The DAF Provider is defined as "accessed by user credentials supplied to Chariot by a DAF User". |
| Acts Chariot may take for the donor | Chariot may write in the grant acknowledgment or purpose, choose the funding source by pro-rata allocation, set the purpose to "Wherever it is needed most", and "Occasionally utiliz[e] the DAFpay Network to disburse funds". |
| Liability for erroneous grant requests | No clause addresses erroneous requests. Grant decisions rest "solely with the DAF Provider". Chariot is not responsible for "financial losses" and caps liability at "ONE THOUSAND U.S. DOLLARS (US $1,000)". The donor is "solely responsible" for the accuracy of credentials. |
| Data rights | Chariot gets a "worldwide, transferable, sublicensable, royalty-free" licence to User Information. |
| Disputes | Arbitration with class waiver. Opt-out is available to users who created accounts on or after 2022-07-18, within 30 days. |

**DAFpay Privacy Policy** ("Effective Date: Janurary 8th, 2025", spelled that way on the page) ([dafpay.com/privacy-policy](https://www.dafpay.com/privacy-policy)) [F]:
- **Credentials.** Donor credentials are "not stored and only used as a one time secure pass through". The same document also says: "We maintain segmented storage of all Credentials for an additional layer of security." [I] These two statements are in tension. The second may refer to nonprofit dashboard credentials, but the policy does not say which credentials it means.
- **Data requests.** On request, Chariot "can provide a CSV or Excel file" of the data it holds about a donor.
- **Retention.** Transaction information is kept "for five years after account closing" of the recipient nonprofit's account.

**Effect on repo rows** [I]
- `agentic-control-gap-matrix.csv`, Chariot `agent_identification`: the donor contract has no agent role. The "on behalf of … third parties" ban arguably excludes a third-party agent operating DAFpay for a donor. A donor's own agent is not addressed.
- Chariot `liability_allocation`: toward donors, the $1,000 cap and the disclaimer of financial losses complete the chain of authority (provider addendum → donor terms). Neither document allocates liability for agent-originated errors.

---

## 4. P-QA2-05: Goodstack

### 4.1 Customers named by Goodstack (2021+)

| Source | Customers named |
|---|---|
| [goodstack.io](https://goodstack.io/) logo strip (alt text) | Google, LinkedIn, Canva, Atlassian, HSBC, ING, Asana, Monday (monday.com), Twilio, HootSuite, Splunk, NewRelic [F] |
| Homepage testimonials | Asana: validation API "reduced our customer response by 11 days and increased our conversion rate by 10%". Atlassian, Splunk and monday.com ("27K nonprofits from 140 countries" on its plan) [F] |
| [Fundraising platforms page](https://goodstack.io/fundraising-platforms) | Millie, Catalyser, Selflessly. These are "top fundraising and impact platforms" using its "global donation rails" [F] |
| [KYNP post, 2026-08-03](https://goodstack.io/blog/7-5m-verifications-in-introducing-kynp-know-your-nonprofit) | "Google, Canva, and ElevenLabs"; 7.5 million verifications [F] |
| [Good2Give acquisition, 2025-11-04](https://goodstack.io/blog/goodstack-expands-apac-presence-with-acquisition-of-good2give) | Atlassian, Canva, Zoom, TikTok. Acquired Good2Give, which it calls the largest workplace-giving organisation in Australia and New Zealand. "In 2024 alone, Goodstack facilitated over $3 billion in donations" [F] |
| [2025 review, 2026-01-08](https://goodstack.io/blog/how-goodstack-has-powered-over-usd5b-in-donations-to-nonprofits) | LinkedIn, Adobe, Asana; "surpassing $5 billion in donations facilitated" (cumulative) [F] |
| Customer pages | [Google for Nonprofits](https://support.google.com/nonprofits/answer/12016036?hl=en): "Goodstack reviews your submission against official local government registries" [F, customer-side]. DocuSign's nonprofit FAQ is reported as using Goodstack ([DocuSign](https://support.docusign.com/s/articles/Docusign-for-Nonprofits-Support-Page-FAQ?language=en_US)) [S, search summary, not fetched] |
| Investor | General Catalyst (logo on [about](https://goodstack.io/about)). Its undated [story](https://www.generalcatalyst.com/stories/our-investment-in-goodstack) cites "compliant donor-advised funds" [F] |

### 4.2 Coverage and registries

- **Coverage.**
  - Goodstack claims "240+ countries and territories" ([about](https://goodstack.io/about); [2025-07-31 post](https://goodstack.io/blog/global-nonprofit-verifications)) [F].
  - Its docs list 245 ISO-3166 alpha-3 codes ([countries](https://docs.goodstack.io/docs/concepts/Platform/countries)) [F].
  - The `/v1/countries` endpoint's `hasRegistry=true` returns "the subset of Countries that Goodstack currently has nonprofit data for" ([list countries](https://docs.goodstack.io/docs/api/list-available-countries)) [F]. That subset was not retrieved because the API needs a key.
- **Database size.** The figures differ by page: "13.5M" (about), "over 9 million good causes" (verifications page), "over 12 million" (2026-01-08 post) [F].
- **Registries.**
  - The public OpenAPI ([openapi.json](https://reference.poweredbypercent.com/openapi.json), "Goodstack Services v1") gives `IRS` and `UK Charity Commission` as registry examples, plus `National Charities Registry` [F].
  - It has a `usaGroupExempt` flag ("USA-specific group exempt"), so IRS group exemptions are modelled [F].
  - Rejection reasons include `not_attributable_to_registry` [F].
  - The validation check uses "official registry websites from the nonprofit or institution's country" ([validations overview](https://docs.goodstack.io/docs/concepts/Verifications/Checks/validations-overview)) [F].
  - The donation policy names the "Charity Commission of England and Wales" and the "Australian Charities for Not-for-profits Commission" as data sources [F].
  - [I] The docs do not name the US source files (BMF, Pub 78 or the Auto-Revocation list).
- **Checks.** Validation, compliance (sanctions, warnings, adverse media, hate speech), eligibility tagging and "agent verification". Agent verification confirms that a human applicant is affiliated with the organisation; it is not about AI agents. Checks "typically take between 1 minute and 72h" [F].
- **Screening depth** (KYNP post) [F]: "130+ international and national sanctions lists", "120+ law enforcement and financial crime watchlists", and "11,000+ sources" for adverse media.

### 4.3 Is Goodstack used by a DAF sponsor or grant platform?

- **Third-party users: none found.**
  - Searches pairing Goodstack with Daffy, Endaoment, Every.org, Givinga, CAF America and "donor-advised fund" found no customer relationship.
  - [Benevity's 2026 grant-software roundup](https://benevity.com/blog/best-grant-management-software) lists Goodstack as a competitor [S], not as a supplier.
  - Goodstack sells its own grants-management product ([grants](https://goodstack.io/grants)) [F].
- **Goodstack runs DAF-style sponsors itself.** Its [Donation Delivery Policy](https://goodstack.org/legal/donation-delivery-policy) ("Effective Date: November 15, 2024") says donations go "exclusively" to one of three foundations [F]:
  - Intelligent Foundation (England and Wales, charity no. 1192508)
  - Intelligent Foundation (Australia, ABN 48156978613)
  - Percent Impact Foundation (US, EIN 87-3165286)

  Grant terms:
  - The donor is "recommending" a charity, and application of the funds is "at the discretion of the Foundation".
  - Grants are paid monthly by bank transfer, subject to a minimum. Funds still held after twelve months are paid out regardless of the minimum.
  - For charities that have not signed up, Goodstack attempts contact over "typically … a 30-day period", then tries "alternative methods, such as by cheque", then applies an "Undeliverable Donation Policy".
- **Scale of the US foundation.**
  - Repo file `data/mission-2026-11-14/non-dafrc-daf-filers-990.csv` already holds EIN 873165286 ("PERCENT IMPACT FOUNDATION", tax period 202412). It shows Schedule D: **7,268 DAFs, $2,945,016 contributions, $1,210,123 grants, $1,812,959 year-end value, total assets $1,984,371** [F, IRS XML via repo].
  - ProPublica now names the same EIN "Goodstack Impact Foundation Us" (ruling 2022-11, NTEE T12). Its CY2023 filing shows revenue of $268,231 ([ProPublica](https://projects.propublica.org/nonprofits/organizations/873165286)) [F].
- [I] Goodstack is therefore a small US DAF sponsor and an eligibility vendor at once. That is the same dual role as Chariot (DAFpay Network) and Every.org. For the A5 score, the execution evidence is large-scale corporate verification. Its DAF operation is minor in dollar terms.

---

## 5. P-WAT-03: `api-give.vanguardcharitable.org` and Vanguard Charitable hosts

### 5.1 `api-give`: public responses only

| Probe | Result |
|---|---|
| DNS | CNAME `d-s8mdizdfu5.execute-api.us-east-1.amazonaws.com`, which is an API Gateway regional custom domain [F] |
| TLS | Subject `CN=api-give.vanguardcharitable.org`. SAN contains only that name. Issuer Amazon RSA 2048 M04. Valid 2026-07-28 to 2027-02-10. Serial `0A59DD445ABC4073BC769DD61773C839` [F] |
| `GET /` | HTTP/2 403, `application/json`, `{"message":"Forbidden"}`, `x-amzn-errortype: ForbiddenException` [F] |
| `/robots.txt`, `/swagger`, `/swagger.json`, `/openapi.json`, `/docs`, `/api-docs`, `/health`, `/.well-known/security.txt` | All 403 `ForbiddenException` [F] |

[I] API Gateway returns `ForbiddenException` on the root when no route matches or when an API key or resource policy is required. Nothing public reveals what the API carries. The name, its CT co-issuance with `api-salesforce` and `auth0`, and the Give Interactive contract (2025-11-04) are still the only basis for reading it as the Give integration endpoint.

### 5.2 Hosts first certified in 2025 or later (from the watchlist snapshot `data/watchlist-snapshots/2026-11-14/ct-vanguardcharitable.json`, crt.sh; root probe 2026-11-14). First-cert dates are unverified leads; every host except `api-vgi` resolves in public DNS on 2026-11-19 [crt19]

| Host | First cert | Fronted by | Root response |
|---|---|---|---|
| portal | 2025-01-15 | Akamai | 301 to `vanguardcharitable.my.site.com/web/` (Salesforce Experience Cloud) |
| grantsmgmt | 2025-02-25 | API Gateway | 403 Forbidden |
| illiquid-assets | 2025-05-13 | API Gateway | 200: "Illiquid Assets Portal — Vanguard Charitable", log-in page |
| account-session | 2025-06-26 | API Gateway | 403 Forbidden |
| api-coreservices | 2026-02-24 | API Gateway | 500 Internal server error |
| **api-give** | 2026-02-25 | API Gateway | 403 Forbidden |
| api-salesforce | 2026-02-25 | API Gateway | 403 Forbidden |
| api-vgi | 2026-02-25 | n/a | No DNS answer seen from here; the proxy returned 502. 2026-11-19: dangling CNAME to `alb-temp-634758386.us-east-1.elb.amazonaws.com` (NXDOMAIN) [crt19] |
| auth0 | 2026-02-25 | API Gateway | 403 Forbidden |
| **api-tungsten** | 2026-03-04 | API Gateway | 200: public Swagger UI, see below |
| client | 2026-07-08 (latest cert run) | Akamai | Salesforce SAML; Issuer parameter `mygiving.vanguardcharitable.org/mygiving/` |
| url5422.transaction | 2026-09-18 | `click.sendgrid.net` | 404. A SendGrid link-branding host for transactional email |

**`api-tungsten`.** The root serves a Swagger UI with an embedded OpenAPI 3.0.3 spec [F]:
- Title "Tungsten API Gateway", version 2.5.2.
- Described as a "Serverless REST API connecting KOFAX/Tungsten document capture with Salesforce FSC and Documentum ECM. Auth0 JWT Bearer token required on all protected endpoints."
- Server base URLs are on a separate domain, `api-tungsten.vcapps.org`, with prd, dev, int and rgr stages.
- Operations cover grantee search, fund-account lookup (Salesforce `FinServ__FinancialAccount__c`), Salesforce Case read and create, and document upload.
- **No mention of Give.** No endpoint was called. The spec's contact address and sample identifiers are not reproduced here.

[I] Taken together:
- Vanguard Charitable's own integration layer is a set of API Gateway services around Salesforce Financial Services Cloud (the donor and case system of record), Documentum (document store), Kofax/Tungsten (mail and document capture) and Auth0 (identity).
- `api-give` sits next to these. That fits Give acting as the fund ledger behind a Salesforce front end, consistent with repo finding G10, but it does not prove it.
- **No new donor-facing host has appeared.** Donors still log in through `client.` → Salesforce.
- The `vcapps.org` domain is a new watch target.

---

## 6. Corrections and updates to existing repo text

1. `queue-npt-dafgiving360-misc.md` §5 says `legal-donors` "serves the homepage to automated fetch" and cites a "Donor Terms of Use effective January 1, 2025" snippet.
   - **Update:** the live Donor Terms are at dafpay.com, effective **2025-09-24**.
   - `legal-donors` redirects to `/home` in a real browser.
2. `queue-payment-rails-cluster.md` §2 says "Wayback … unreachable". **Update:** the availability API works, and snapshot timestamps are listed in §2.2 above. Snapshot content still cannot be fetched from this environment.
3. `queue-watchlist-and-vendor-moves.md` P-VEN-02 says `api-give` was "not probed". **Update:** it was probed (§5.1). It is API Gateway returning 403 and exposes no public docs. Add `api-tungsten` and `vcapps.org` as watch items.
4. Goodstack (A5) has DAF-sponsor execution evidence through Percent Impact Foundation, which is already in `non-dafrc-daf-filers-990.csv` under its old name. The two entities should be linked in the relationship graph.

---

## 7. Source register

| # | Source | Type | Date or version | Retrieved | URL |
|---|---|---|---|---|---|
| 1 | Fidelity Charitable nonprofit page | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits.html |
| 2 | Fidelity nonprofit FAQ | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/faqs.html |
| 3 | Fidelity EFT page | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/eft.html |
| 4 | Fidelity Stripe grants page | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/nonprofits/fidelity-grant.html |
| 5 | Fidelity EFT enrollment form PDF | sponsor | modified 2025-12-18 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/forms/charitable-organization-eft-enrollment-form.pdf |
| 6 | Fidelity year-end deadlines | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/giving-account/what-you-can-donate/charitable-year-end-tax-deadlines.html |
| 7 | Fidelity "How to view and download statements" PDF | sponsor | created 2026-05-26 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/resources/how-to-view-and-download-statement-confirmation-and-tax-forms.pdf |
| 8 | Fidelity Program Guidelines PDF | sponsor | created 2026-09-11 | 2026-11-14 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/programs/fidelity-charitable-program-guidelines.pdf |
| 9 | Fidelity FAQ index | sponsor | live | 2026-11-14 | https://www.fidelitycharitable.org/faqs/all.html |
| 10 | Wayback availability API (Fidelity pages) | archive index | n/a | 2026-11-14 | https://archive.org/wayback/available?url=fidelitycharitable.org/nonprofits/faqs.html |
| 11 | Bogleheads t=464478 (search extracts only; HTTP 402 on fetch) | forum | Dec 2025 to Oct 2026 | 2026-11-14 | https://www.bogleheads.org/forum/viewtopic.php?t=464478 ; https://www.bogleheads.org/forum/viewtopic.php?p=8700839 |
| 12 | Chariot "Not Enrolled for E-Pay" | vendor blog | "May 7" (2026) | earlier wave | https://www.givechariot.com/resources/insights/your-not-enrolled-for-e-pay-status-is-costing-you-donors |
| 13 | DAFpay Donor Terms of Use | vendor contract | effective 2025-09-24 | 2026-11-14 | https://www.dafpay.com/donor-terms-of-use |
| 14 | DAFpay Privacy Policy | vendor policy | effective 2025-01-08 | 2026-11-14 | https://www.dafpay.com/privacy-policy |
| 15 | Chariot Nonprofit Terms (links to #13) | vendor contract | updated 2026-10-14 | 2026-11-14 | https://www.givechariot.com/legal-nonprofit |
| 16 | Chariot legal-donors (redirects to /home) | vendor | n/a | 2026-11-14 | https://www.givechariot.com/legal-donors |
| 17 | Chariot pages sitemap | vendor | live | 2026-11-14 | https://www.givechariot.com/pages-sitemap.xml |
| 18 | DAFpay Provider Addendum | vendor contract | 2026-10-14 | 2026-11-14 | https://www.givechariot.com/dafpay-provider-addendum |
| 19 | Goodstack homepage, verifications, fundraising-platforms, about | vendor | © 2026 | 2026-11-14 | https://goodstack.io/ ; https://goodstack.io/verifications ; https://goodstack.io/fundraising-platforms ; https://goodstack.io/about |
| 20 | Goodstack KYNP post | vendor blog | 2026-08-03 | 2026-11-14 | https://goodstack.io/blog/7-5m-verifications-in-introducing-kynp-know-your-nonprofit |
| 21 | Goodstack 240+ countries post | vendor blog | 2025-07-31 | 2026-11-14 | https://goodstack.io/blog/global-nonprofit-verifications |
| 22 | Goodstack Good2Give acquisition | vendor blog | 2025-11-04 | 2026-11-14 | https://goodstack.io/blog/goodstack-expands-apac-presence-with-acquisition-of-good2give |
| 23 | Goodstack 2025 review ($5bn) | vendor blog | 2026-01-08 | 2026-11-14 | https://goodstack.io/blog/how-goodstack-has-powered-over-usd5b-in-donations-to-nonprofits |
| 24 | Goodstack docs: countries, validations, compliance, eligibility, agent verification | vendor docs | live | 2026-11-14 | https://docs.goodstack.io/docs/concepts/Platform/countries ; https://docs.goodstack.io/docs/concepts/Verifications/Checks/validations-overview |
| 25 | Goodstack OpenAPI ("Goodstack Services v1") | vendor docs | live | 2026-11-14 | https://reference.poweredbypercent.com/openapi.json |
| 26 | Goodstack Donation Delivery Policy | vendor policy | effective 2024-11-15 | 2026-11-14 | https://goodstack.org/legal/donation-delivery-policy |
| 27 | Google for Nonprofits: Get verified by Goodstack | customer help | live | 2026-11-14 | https://support.google.com/nonprofits/answer/12016036?hl=en |
| 28 | General Catalyst: Our investment in Goodstack | investor | undated | 2026-11-14 | https://www.generalcatalyst.com/stories/our-investment-in-goodstack |
| 29 | ProPublica: EIN 87-3165286 | 990 aggregator | CY2023, CY2024 filings | 2026-11-14 | https://projects.propublica.org/nonprofits/organizations/873165286 |
| 30 | Repo: Percent Impact Foundation Schedule D FY2024 | IRS XML (repo) | return 202522489349301512 | repo | data/mission-2026-11-14/non-dafrc-daf-filers-990.csv |
| 31 | Benevity grant-software roundup | competitor blog | 2026 | search only | https://benevity.com/blog/best-grant-management-software |
| 32 | `api-give.vanguardcharitable.org` (TLS, headers, public paths) | server response | cert 2026-07-28 | 2026-11-14 | https://api-give.vanguardcharitable.org/ |
| 33 | `api-tungsten.vanguardcharitable.org` Swagger UI | server response | spec v2.5.2 | 2026-11-14 | https://api-tungsten.vanguardcharitable.org/ |
| 34 | Vanguard Charitable CT snapshot | repo (crt.sh) | 2026-11-14T11:25Z | repo | data/watchlist-snapshots/2026-11-14/ct-vanguardcharitable.json |
| 35 | Vanguard Charitable `client.`, `portal.`, `illiquid-assets.` responses | server response | live | 2026-11-14 | https://client.vanguardcharitable.org/ ; https://portal.vanguardcharitable.org/ ; https://illiquid-assets.vanguardcharitable.org/ |

---

## 8. Data dictionary: `data/mission-2026-11-14/queue-proposals-fcgv.csv`

The columns follow `queue-proposals-README.md`.

| Column | Type | Meaning |
|---|---|---|
| question_id | string | `P-FCG-NN` |
| question | string | The research question |
| area | string | Repo area label |
| importance | int 1–5 | Value to the core conclusions |
| p_change | float 0–1 | Probability that the answer changes a repo conclusion |
| gap | int 1–5 | Size of the evidence gap |
| commercial | int 1–5 | Commercial relevance |
| availability | int 1–5 | How available the evidence is (5 = easy) |
| effort | int 1–5 | Effort (5 = high) |
| depends_on | string | Queue IDs it depends on |
| breadth_gap | yes/no | Whether it fills a coverage-breadth gap |
| state | string | Always `open` |
| assigned_to | string | Blank |
| conclusion_affected | string | Repo conclusion or score affected |
| proposed_by | string | `FCGV agent` |
| rationale | string | Why the question matters now |
| evidence_pointer | string | URL or repo path that starts the work |

## Validation corrections (wave 7, 2026-11-14) — governing
Source: [validation-wave7-report.md](validation-wave7-report.md). Where these conflict with the text above, these govern.

1. **Line 28**
   - Current: "Goodstack's donation rails run through its own DAF-style foundations."
   - Replace with: "Goodstack's donation rails run through partner foundations that its Donation Delivery Policy names as exclusive recipients. The US foundation describes itself as one of a 'stack of independent charitable foundations' that 'work with Goodstack, a technology company' ([giftall.org](https://www.giftall.org/))."
2. **Line 28**
   - Current: "reported **7,268 DAFs and $1.81m year-end DAF value for FY2024** [F]."
   - Replace with: "reported **7,268 DAFs and $1.81m year-end DAF value for FY2024**. Its FY2025 return (filed 2026-09-02) reports **$10,772,483 year-end DAF value, $11,582,483 DAF contributions, $1,660,000 DAF grants and 3 DAFs** (an apparent change in how accounts are counted), with total assets of $12,779,329 ([XML](https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/202602459349300235_public.xml)) [F]."
3. **Line 150**
   - Current: "**Goodstack runs DAF-style sponsors itself.**"
   - Replace with: "**Goodstack routes donations exclusively through affiliated DAF-style foundations, which present themselves as independent.**"
4. **Line 161.** After "revenue of $268,231", add: "CY2024 revenue was $3,116,428 and CY2025 revenue $16,344,032 (ProPublica)."
5. **Line 162**
   - Current: "Its DAF operation is minor in dollar terms."
   - Replace with: "Its DAF operation is small but grew about 6x in 2025 ($10.8m year-end DAF value)."
6. **Line 94 (agent row).** Append: "Note: the Terms do make Chariot itself the donor's authorized actor ('you hereby authorize Chariot to take the following actions on your behalf'). 'No agent clause' means no clause on third-party or AI agents."
7. **Line 27.** Add the privacy policy's effective date: "Privacy Policy effective 'Janurary 8th, 2025' (sic)."

## Compliance note (2026-11-15) — governing
crt.sh disallows all crawlers in its robots.txt. Any claim in this document that rests **only** on crt.sh certificate data is downgraded to an unverified lead until re-sourced. See [compliance-note-crtsh-robots.md](compliance-note-crtsh-robots.md).
