# Vendor API assessment

**Status:** research input, not a procurement decision. **Evidence date:** all web sources accessed 2026-11-21. **Companion data:** [`vendor-api-assessment.csv`](vendor-api-assessment.csv) (one row per vendor, one column per criterion, with source URLs).

**Why this exists.** The owner's rule is: *APIs for everything; only select vendors with useful APIs.* Login must also federate with partner organizations that own the accounts (wealth firms, advisor platforms, institutional sponsors) and must support MFA. This file scores the vendors the platform would depend on against a fixed rubric, says which are usable, and names the categories where no vendor has a useful API and the design has to absorb that.

**Context used (not re-researched here):** integration patterns in [technology-architecture.md §5](technology-architecture.md#5-integration-architecture); token model in [api-catalog.md §3](../04-enterprise-apis/api-catalog.md#3-authentication-and-authorization-model); money-transmission models A/B/C in [regulatory-applicability-map.md §14](../08-governance-and-compliance/regulatory-applicability-map.md#14-money-transmission-implications-for-a-multi-sponsor-infrastructure-provider); charity-data and sanctions vendors in [landscape-and-evidence.md](../charity-vetting-ai/landscape-and-evidence.md); licence terms in [b43n26-03-charity-data-terms-ai.md](../../mission-2026-11-14/b43n26-03-charity-data-terms-ai.md); payment rails in [queue-payment-rails-cluster.md](../../mission-2026-11-14/queue-payment-rails-cluster.md) and the [industry report §2.5–2.7](../../DAF-INDUSTRY-REPORT-2026-11.md#25-payment-rails); exactly-once side effects in [framework-feedback FP-09 / experiment E9](../workflow-innovation/12-implementation-proposals/framework-feedback-proposals.md).

**Evidence labels.** Scores rest on the vendor's own documentation unless a note says otherwise. A vendor's description of itself (certifications, scale, "real-time") is a **vendor claim**. `[I]` marks an inference. `*` in the identity matrix marks a long-established product feature that was not re-fetched in this pass. Where a portal required login, the score is `N` for public documentation ("docs gated"), which is itself a negative signal under the rule. **Nothing here was scored from memory where a source was missing: those cells are `U`.** The assessor is an Anthropic model; the LLM-provider rows rest only on the cited pages.

---

## 1. Rubric (defined before scoring)

Each criterion is scored **Y** (yes, documented), **P** (partial, or documented with a material caveat), **N** (no, or documented as absent), **U** (unknown: no evidence found this pass) or **NA** (does not apply to this kind of service).

| # | Criterion | Y means | Why it matters here |
|---|---|---|---|
| C1 | Public API documentation | Reference docs readable without a login or NDA | The rule cannot be applied to docs nobody can read. Gated docs = `N` |
| C2 | API style | REST, GraphQL or ISO 20022 messages documented (`N` = files only) | Files force an adapter (§5) |
| C3 | Authentication | OAuth 2.0 client credentials, private_key_jwt or mTLS (`P` = API key or HTTP Basic only) | Institution tokens in the API catalog are mTLS-bound; agent tokens need delegation |
| C4 | Push / events | Webhooks or event streams, signed (`P` = polling or partial) | The platform is event-driven |
| C5 | Idempotency | Client-supplied idempotency key documented on writes | **Must-have for money movement and trading.** E9 showed exactly-once external effects need a durable outbox *and* counterparty idempotency (FP-09) |
| C6 | Sandbox | Self-serve or contract-free test environment (`P` = on request or paid) | Agent and workflow tests need a safe counterparty |
| C7 | Versioning / deprecation | Dated or numbered versions with a stated policy | Agents and adapters break silently on unversioned change |
| C8 | Rate limits documented | Published limits or 429 semantics | Capacity planning; agent back-off |
| C9 | Bulk export / portability | Bulk or batch export of the customer's data | Exit, migration by replay (XW-29), reconciliation |
| C10 | Security assurance | SOC 2 Type II or ISO 27001 published or stated by vendor | Sponsor auditors need SOC reports (Nacha TPSP duties, regulatory map §14) |
| C11 | Licence / AI constraints | `Y` = no restrictive clause found; `P` = limits that need a negotiated licence; `N` = terms bar the intended use | Charity-data licences restrict AI and calculation use (b43n26-03) |
| C12 | Fit with instruction-only model | `Y` = funds stay in sponsor-titled accounts and the vendor only instructs; `P` = possible with a named contractual control; `N` = vendor holds funds on the platform's behalf | Regulatory map §14: build on Model A (instruction-only) or B (licensed partner), never incidental Model C |

**Must-haves (M1–M6):** C1 ∈ {Y,P}; C3 ∈ {Y,P}; C4 ∈ {Y,P}; C5 = Y *for any API that moves money, trades or creates grants*; C6 ∈ {Y,P}; C12 ≠ N.

**Verdicts:**
- **SELECT-CANDIDATE**: every applicable must-have is met on public evidence and C11 is not `N`. Commercial and business-fit diligence still applies.
- **CONDITIONAL**: the API is useful, but one must-have is `U` or carries a named gap, or C11/C12 imposes a condition the contract must fix. The condition is stated.
- **UNVERIFIED**: documentation is gated or the evidence is too thin to score at least three must-haves. Not a rejection; it cannot be selected until the docs are read under NDA.
- **REJECT (APIs not useful)**: no API exists, or the terms or funds model fail a must-have outright (`N`).
- **EXCEPTION-FILES**: used only for authoritative government sources that no vendor can replace and that publish files, not APIs. The adapter in §5 is the platform's API.

---

## 2. Results at a glance

75 rows were scored: 23 SELECT-CANDIDATE, 28 CONDITIONAL, 18 UNVERIFIED, 4 REJECT, 2 EXCEPTION-FILES.

**Recommended shortlist (two per category where evidence allows):**

| Category | Primary | Second (redundancy) | Concentration and conditions |
|---|---|---|---|
| Custody for investment pools | **Apex** (SELECT-CANDIDATE: sandbox, idempotent transfers) | **IBKR** (CONDITIONAL: private_key_jwt; idempotency and sandbox unverified) | Large incumbents (Schwab, Fidelity, BNY Pershing) are UNVERIFIED (docs gated). Where a partner's accounts sit there, the file adapter in §5 is mandatory. Apex's fit for a charitable sponsor's entity accounts is unverified |
| Payment orchestration over sponsor accounts | **Modern Treasury** (bring-your-own-bank mode only) | Direct bank API: **Column** or **Increase**; **J.P. Morgan** is CONDITIONAL until GP2 idempotency is confirmed for ACH | Modern Treasury can also hold funds in FBO accounts; contract must exclude that mode |
| Charity-facing grant network | **Chariot** Disbursements API | Plain ACH CCD+/CTX from the sponsor's own ODFI (no network) | **Chariot runs on Column N.A.** If Column is also the ODFI, both rails share one bank. Pick a non-Column ODFI for redundancy. PayPal Grant Payments is UNVERIFIED (no public grantmaker API) |
| Bank account verification | **Plaid Auth** | **Mastercard Open Banking (Finicity)** or **MX** (CONDITIONAL) | Avoid relying on Plaid for both Auth and KYC unless accepted |
| KYC / identity verification | **Persona** | **Alloy** (orchestration) or **Entrust IDV** | All score `P` on auth (API keys) |
| Sanctions screening | **OpenSanctions** self-hosted yente + commercial data licence | **LSEG World-Check One** or **ComplyAdvantage** (CONDITIONAL) | OFAC files remain the authoritative baseline (EXCEPTION-FILES) |
| Charity eligibility data | **IRS bulk files** (EXCEPTION-FILES) | **Goodstack** for non-US verification (CONDITIONAL: internal-use licence) | Candid only with written AI-use consent; Charity Navigator rejected as a decision input; NGOsource is manual |
| Crypto donations | **Anchorage Digital** (CONDITIONAL) | **Coinbase Prime** (CONDITIONAL) | No SELECT-CANDIDATE. The Giving Block is a Model B pass-through for donor intake |
| Non-cash assets | — | — | **No vendor with an API.** Manual partner process (§5) |
| E-signature | **DocuSign** | **Dropbox Sign** | Adobe Acrobat Sign not scored (no evidence gathered) |
| Accounting / GL | **QuickBooks Online** (small sponsors) or **Dynamics 365 BC** (CONDITIONAL) | **NetSuite** / **Sage Intacct** (CONDITIONAL) | The event ledger stays the system of record; the GL receives journals |
| Advisor / wealth platforms | Integrate first where docs are public: **Addepar**, **Wealthbox**, **Salesforce FSC**, **Orion** | — | Envestnet, Black Diamond, Redtail, Morningstar are gated. Access must come through the partner |
| LLM providers | **Anthropic API** | **Amazon Bedrock** or **OpenAI API** | Two providers per agent family (technology-architecture §5) |
| Identity | See §4 | | |

**Rejected (APIs not useful under the rule):** Stripe Treasury/Connect for grant disbursement (funds held in Stripe balances; fine for donor-side card collection, which is out of scope); Charity Navigator API as a decision input (licence bars use "in any other calculation"); NGOsource (no API); non-cash asset processors (none found).

---

## 3. Scores by category

Column key: Docs=C1, Style=C2, Auth=C3, Push=C4, Idem=C5, Sbx=C6, Ver=C7, Rate=C8, Bulk=C9, Assur=C10, Licence=C11, Fit=C12. Source IDs resolve in §7.

#### 1 Custody/brokerage

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Charles Schwab (Advisor Services; OpenView Gateway via PTI) | N | U | U | U | U | U | U | U | Y | U | U | Y[I] | **UNVERIFIED** | S01, S02 |
| Fidelity Clearing & Custody (Wealthscape Integration Xchange) | N | U | U | U | U | P | U | U | U | U | U | Y[I] | **UNVERIFIED** | S03, S04 |
| BNY Pershing (NetXServices / NetX360+) | N | U | U | P | U | P | U | U | Y | U | U | Y[I] | **UNVERIFIED** | S05, S06 |
| Apex Fintech Solutions (Apex Ascend) | P | Y:REST | P | P | Y | Y | P | U | U | U | U | Y[I] | **SELECT-CANDIDATE** | S07, S08, S09 |
| Altruist | Y | P:REST+files | P | U | U | U | P | P | Y | U | U | Y[I] | **CONDITIONAL** | S10, S11 |
| Interactive Brokers (IBKR Web API) | Y | Y:REST | Y | U | U | U | P | U | U | U | U | Y[I] | **CONDITIONAL** | S12 |

- **Charles Schwab (Advisor Services; OpenView Gateway via PTI): UNVERIFIED.** Advisor API docs not public (page 403 to fetch; access via relationship manager and PTI); daily data files are the documented path. *Note:* Retail Trader API (OAuth 2.0) exists but is for individual brokerage accounts, not sponsor pools; not assessed as the institutional path.
- **Fidelity Clearing & Custody (Wealthscape Integration Xchange): UNVERIFIED.** API store limited to Fidelity custody/clearing clients; no public reference found; evidence is 2018-2021 press. *Note:* 2020 release claims self-service API testing (vendor claim).
- **BNY Pershing (NetXServices / NetX360+): UNVERIFIED.** API store with sandbox and streaming APIs reported in press; no public API reference found. *Note:* Batch processing offered alongside APIs (vendor page).
- **Apex Fintech Solutions (Apex Ascend): SELECT-CANDIDATE.** Sandbox before contract; SDKs; client-specified transfer ID documented as idempotency key; portal reference behind Okta sign-in. *Note:* Business fit for a charitable sponsor's entity/pooled accounts not verified; diligence required.
- **Altruist: CONDITIONAL.** Public portal; Open API is read-only prior-EOD; Realtime write API reported (third-party) to use OAuth password grant; idempotency unknown. *Note:* Password grant is deprecated in OAuth 2.1 security guidance; require client-credentials or private_key_jwt before write use.
- **Interactive Brokers (IBKR Web API): CONDITIONAL.** Public docs; OAuth 2.0 with private_key_jwt for organizations/advisors; idempotency and sandbox not verified this pass. *Note:* Web API products being consolidated (vendor docs).

#### 2 Banking/payments

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| J.P. Morgan Payments (Global Payments 2, ACH) | Y | Y:REST | Y | Y | P | Y | P | U | U | U | U | Y | **CONDITIONAL** | S13, S14, S15 |
| Column N.A. | Y | Y:REST | P | Y | Y | Y | U | U | U | U | U | Y | **SELECT-CANDIDATE** | S16, S17, S18 |
| Increase | Y | Y:REST | P | Y | Y | Y | P | P | U | Y | U | P | **SELECT-CANDIDATE** | S19, S20, S21 |
| Modern Treasury | Y | Y:REST | P | Y | Y | Y | P | P | U | Y | U | P | **SELECT-CANDIDATE** | S22, S23, S24, S25, S26 |
| Moov | Y | Y:REST | P | Y | Y | U | Y | U | U | U | U | P | **CONDITIONAL** | S27, S28 |
| Dwolla | Y | Y:REST | Y | Y | Y | Y | P | P | U | U | U | P | **CONDITIONAL** | S29, S30, S31 |
| Stripe (Treasury / Connect) | Y | Y:REST | P | Y | Y | Y | Y | U | U | U | U | N | **REJECT** | S32 |
| Chariot (Disbursements API; DAFpay) | Y | Y:REST | P | Y | Y | Y | Y | U | U | Y | U | P | **SELECT-CANDIDATE** | S33, S34, S35, S36, S37 |
| PayPal Grant Payments / PayPal Giving Fund | N | U | U | U | U | U | U | U | U | U | U | P | **UNVERIFIED** | S38, S39 |
| Wells Fargo (Gateway developer portal) | P | Y:REST | U | U | U | P | U | U | U | U | U | Y | **UNVERIFIED** | S40 |
| Bank of America (CashPro API) | P | Y:REST | U | P | U | P | U | U | U | U | U | Y | **UNVERIFIED** | S41, S42 |
| U.S. Bank (Treasury Builder APIs) | P | Y:REST | P | U | U | U | Y | U | U | U | U | Y | **UNVERIFIED** | S43 |

- **J.P. Morgan Payments (Global Payments 2, ACH): CONDITIONAL.** Strong auth (JWT/public key, mTLS + digital signature); GP2 supports idempotency keys but older GP API only business duplicate checks; ACH coverage of GP2 idempotency to confirm. *Note:* Requires onboarded client project; sponsor's own account (Model A).
- **Column N.A.: SELECT-CANDIDATE.** Public OpenAPI; idempotency on transfers (30-day keys); webhooks with signature; sandbox simulations; it is the bank (ODFI). *Note:* Auth = API key via HTTP Basic (no OAuth/mTLS documented); bank accounts are opened 'on behalf of your customers' (platform model) - direct sponsor account eligibility to confirm; Chariot also runs on Column (concentration).
- **Increase: SELECT-CANDIDATE.** Public docs; Idempotency-Key with replay header; webhooks; separate sandbox; SOC 2 Type 2 (Dec 2024-Nov 2025) published. *Note:* Bearer API key only; partner bank and account titling not stated on overview page - confirm accounts titled to sponsor.
- **Modern Treasury: SELECT-CANDIDATE.** Bring-your-own-bank orchestration over sponsor's accounts; Idempotency-Key (24h); signed webhooks; sandbox banks; annual SOC 1/SOC 2 Type II. *Note:* Use BYOB mode only: MT can also hold funds in FBO custodial accounts at its partner banks (Model B/C) - contractually exclude.
- **Moov: CONDITIONAL.** Required X-Idempotency-Key that never expires; transfer.updated webhooks; dated API versions; wallet-based flows. *Note:* Funds can sit in Moov wallets (provider ledger) - confirm a bank-to-bank path that never pools sponsor funds.
- **Dwolla: CONDITIONAL.** OAuth 2.0 client credentials; Idempotency-Key; sandbox; webhooks (unordered); Balance funding source can hold funds in the Dwolla network. *Note:* Use only bank-to-bank funding sources; exclude Balance holding.
- **Stripe (Treasury / Connect): REJECT.** APIs are excellent but Treasury/Connect hold funds in Stripe-managed balances/financial accounts on the platform's behalf; eligibility review applies; does not fit instruction-only grant disbursement. *Note:* Acceptable for donor-side card collection under Stripe's own licences (outside this assessment).
- **Chariot (Disbursements API; DAFpay): SELECT-CANDIDATE.** Dated API versions; disbursement create accepts Idempotency-Key (replay=409; lookup by key); approval objects; event subscriptions; sandbox simulations; SOC 2 Type II (vendor claim). *Note:* Chariot Deposit Account is a DDA at Column N.A. 'legally owned by your organization' (vendor claim) but no bring-your-own-bank; API keys only; single-bank concentration on Column.
- **PayPal Grant Payments / PayPal Giving Fund: UNVERIFIED.** Program exists for grantmakers but no public grantmaker API found; Braintree 'Grant API' is an unrelated payment-method sharing product. *Note:* Repo: NPT/Vanguard use it; integration method not public - negative signal under the rule.
- **Wells Fargo (Gateway developer portal): UNVERIFIED.** Portal and sandbox named; ACH API details only in third-party catalogs; idempotency not found. *Note:* Sponsor-titled operating account fits Model A.
- **Bank of America (CashPro API): UNVERIFIED.** Developer Studio and sandbox claimed; ACH credit and push notifications/webhooks listed in setup form; reference behind login.
- **U.S. Bank (Treasury Builder APIs): UNVERIFIED.** ACH Originations, RTP, Positive Pay APIs bundled; onboarding by access form; idempotency not found. *Note:* MFA on OAuth reported by a Microsoft connector page.

#### 3 Bank account verification

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Plaid Auth | Y | Y:REST | P | Y | NA | Y | Y | U | NA | Y | U | NA | **SELECT-CANDIDATE** | S44, S45, S46, S47 |
| Mastercard Open Banking (Finicity) - Account Owner Verification / ACH Details | Y | Y:REST | U | U | NA | U | U | U | NA | U | U | NA | **CONDITIONAL** | S48 |
| MX (Instant Account Verification) | Y | Y:REST | U | P | NA | U | Y | U | NA | U | U | NA | **CONDITIONAL** | S49, S50 |
| Trustly (AMER) | Y | Y:REST | P | U | NA | P | U | U | NA | U | U | NA | **CONDITIONAL** | S51, S52 |

- **Plaid Auth: SELECT-CANDIDATE.** Public docs; Auth webhooks; Sandbox; versioned API; SOC 2 Type 2 + ISO 27001/27701. *Note:* client_id/secret auth; webhook verification optional - make it mandatory.
- **Mastercard Open Banking (Finicity) - Account Owner Verification / ACH Details: CONDITIONAL.** Public product docs for premium AOV and ACH details endpoints; auth, webhooks and sandbox not verified this pass. *Note:* Per-call billing for premium endpoints.
- **MX (Instant Account Verification): CONDITIONAL.** Public docs; API-only verify flow relies on polling status; dated Platform API versions. *Note:* Chase OAuth connections return tokenized not real account numbers.
- **Trustly (AMER): CONDITIONAL.** Public Verify Account endpoint; HTTP Basic accessId/accessKey; sandbox credentials via support email.

#### 4 Identity (workforce + partner federation)

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Okta Workforce Identity | Y | Y:OIDC/SAML | Y | U | NA | U | U | U | U | U | NA | NA | **SELECT-CANDIDATE** | S53, S54, S55, S56 |
| Auth0 (Okta Customer Identity) | Y | Y:OIDC/SAML | Y | Y | NA | U | U | U | U | U | NA | NA | **SELECT-CANDIDATE** | S57, S58, S59 |
| Microsoft Entra ID / External ID | Y | Y:OIDC/SAML/WS-Fed | Y | U | NA | U | U | U | U | U | NA | NA | **CONDITIONAL** | S60, S61, S62 |
| Ping Identity (PingFederate / PingOne) | Y | Y:OIDC/SAML/WS-Fed | Y | U | NA | U | U | U | U | U | NA | NA | **SELECT-CANDIDATE** | S63, S64, S65, S66 |
| WorkOS | Y | Y:OIDC/SAML | P | Y | NA | U | U | U | U | Y | NA | NA | **SELECT-CANDIDATE** | S67, S68 |
| Stytch (Twilio) | Y | Y:OIDC/SAML | P | U | NA | U | U | U | U | U | NA | NA | **CONDITIONAL** | S69, S70, S71 |
| FusionAuth | U | U | U | U | NA | U | U | U | U | U | NA | NA | **UNVERIFIED** | S72 |
| Keycloak (open source; Red Hat build) | Y | Y:OIDC/SAML | Y | U | NA | Y[self-host] | Y | NA | Y[self-host] | NA | Y[Apache-2.0] | NA | **SELECT-CANDIDATE** | S73, S74, S75, S76 |

- **Okta Workforce Identity: SELECT-CANDIDATE.** Step-up via acr_values (RFC 9470 pattern); OBO token exchange; DPoP for all customers; ID-JAG for agent token exchange. *Note:* Staff/admin identity; token exchange needs API Access Management licence (Okta support article).
- **Auth0 (Okta Customer Identity): SELECT-CANDIDATE.** Organizations with per-org enterprise SAML/OIDC connections, per-org MFA and inbound SCIM; FAPI 2.0 Security Profile (private_key_jwt or mTLS) with HRI add-on. *Note:* HRI requires Enterprise plan; RFC 8693 token exchange and WebAuthn not re-verified this pass.
- **Microsoft Entra ID / External ID: CONDITIONAL.** SAML/WS-Fed federation with partner IdPs but each partner user still becomes a B2B guest; max 1,000 federations; can accept MFA claims from federated IdP; OBO is proprietary, not RFC 8693. *Note:* FAPI 2.0 support not found.
- **Ping Identity (PingFederate / PingOne): SELECT-CANDIDATE.** RFC 8693 token exchange (PingFederate; PingOne since Mar 2026); FAPI 1 Advanced certified (PingFederate 11.0); partner IdP federation core use case. *Note:* Passkey and SCIM details from third-party source only.
- **WorkOS: SELECT-CANDIDATE.** Per-organization SSO (SAML/OIDC), Directory Sync (SCIM), per-org MFA policy, passkeys, self-serve admin portal; SOC 2 Type 2. *Note:* Partner-onboarding broker, not a FAPI-grade authorization server; token exchange/DPoP/FAPI not found; third-party claim that its MFA is not enforced for SSO users.
- **Stytch (Twilio): CONDITIONAL.** B2B orgs, SAML/OIDC SSO, SCIM, per-org MFA incl. WebAuthn; acquired by Twilio (closed 2025-11-14). *Note:* Ownership change; token exchange/FAPI not found.
- **FusionAuth: UNVERIFIED.** Only third-party comparison pages found this pass. *Note:* Re-assess from vendor docs.
- **Keycloak (open source; Red Hat build): SELECT-CANDIDATE.** Standard Token Exchange (RFC 8693) supported 26.2; FAPI 2.0 Security Profile + Message Signing and DPoP supported 26.4; SCIM API supported 26.8. *Note:* Self-operated: the platform owns uptime, patching and assurance; project notes FAPI coverage has gaps.

#### 5 KYC / identity verification

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Persona | Y | Y:REST | P | Y | Y | Y | Y | U | U | Y | U | NA | **SELECT-CANDIDATE** | S77, S78, S79, S145 |
| Alloy | Y | Y:REST | P | Y | U | Y | U | U | U | U | U | NA | **SELECT-CANDIDATE** | S80, S81, S146 |
| Socure (ID+ / RiskOS) | Y | Y:REST | P | Y | U | Y | U | U | U | U | U | NA | **SELECT-CANDIDATE** | S82, S83 |
| Entrust Identity Verification (formerly Onfido) | Y | Y:REST | P | Y | U | Y | Y | U | U | U | U | NA | **SELECT-CANDIDATE** | S84, S85 |
| Plaid Identity Verification + Monitor | Y | Y:REST | P | Y | U | Y | Y | U | U | Y | U | NA | **SELECT-CANDIDATE** | S86, S87, S47 |

- **Persona: SELECT-CANDIDATE.** Idempotency-Key with parameter check; dated versions (Persona-Version); webhooks; sandbox keys; SOC 2 Type II + ISO 27001. *Note:* API key auth.
- **Alloy: SELECT-CANDIDATE.** Public docs; evaluations API; webhooks; per-request sandbox mode. *Note:* Basic auth (key/secret); orchestration layer over data vendors.
- **Socure (ID+ / RiskOS): SELECT-CANDIDATE.** Public developer portal; bearer keys per environment; webhooks retried up to 10 times; RiskOS sandbox. *Note:* Two product lines (ID+ and RiskOS) with different setups.
- **Entrust Identity Verification (formerly Onfido): SELECT-CANDIDATE.** Versioned API (v3.6) with published versioning policy; webhooks; sandbox with predetermined responses; regional hosts. *Note:* API token auth.
- **Plaid Identity Verification + Monitor: SELECT-CANDIDATE.** IDV links to Monitor watchlist screening; webhooks on new hits; sandbox. *Note:* Concentration if Plaid also used for Auth.

#### 6 Sanctions and charity data

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OpenSanctions (yente API, self-hosted, + data licence) | Y | Y:REST | P | U | NA | P | U | P | Y | U | P | NA | **SELECT-CANDIDATE** | S88, S89, S90 |
| ComplyAdvantage | P | Y:REST | P | Y | NA | U | U | U | U | U | U | NA | **CONDITIONAL** | S91, S92 |
| LSEG World-Check One API | Y | Y:REST | P | U | NA | P | U | U | U | U | U | NA | **CONDITIONAL** | S93, S94 |
| Dow Jones Risk & Compliance (Screening & Monitoring API) | U | U | U | U | NA | U | U | U | U | U | U | NA | **UNVERIFIED** | S95 |
| IRS EO BMF / Pub 78 / Auto-Revocation / TEOS bulk files | Y | N:files | NA | N | NA | NA | NA | NA | Y | NA | Y | NA | **EXCEPTION-FILES** | S96, S97 |
| OFAC sanctions lists | Y | N:files | NA | N | NA | NA | NA | NA | Y | NA | Y | NA | **EXCEPTION-FILES** | repo |
| Candid (Charity Check, Essentials APIs) | Y | Y:REST | P | U | NA | U | Y | U | U | U | N | NA | **CONDITIONAL** | S98, S99 |
| Charity Navigator API | Y | Y:GraphQL | P | U | NA | U | U | U | U | U | N | NA | **REJECT** | S100 |
| Every.org Charity API | Y | Y:REST | P | N | NA | U | P | Y | U | U | P | NA | **CONDITIONAL** | S101 |
| Pledge API | Y | Y:REST | P | U | P | U | U | U | U | U | U | NA | **UNVERIFIED** | S102 |
| Goodstack (nonprofit verification API) | Y | Y:REST | P | Y | U | Y | U | U | U | U | P | NA | **CONDITIONAL** | S103, S104 |
| NGOsource (equivalency determinations) | N | N:none | NA | NA | NA | NA | NA | NA | NA | U | U | NA | **REJECT** | S105 |

- **OpenSanctions (yente API, self-hosted, + data licence): SELECT-CANDIDATE.** Open-source (MIT) matching API self-hostable; bulk data downloadable; hosted /match metered EUR 0.10/query. *Note:* Commercial screening needs a data licence (CC BY-NC bulk); version-pin datasets per repo design.
- **ComplyAdvantage: CONDITIONAL.** Classic API with monitoring webhooks; migration to Mesh (OAuth2 bearer); Mesh webhooks may fire multiple times. *Note:* Two platforms in transition; official docs not fetched.
- **LSEG World-Check One API: CONDITIONAL.** Public developer portal; API key + HMAC request signing; pilot environment referenced in community threads. *Note:* Licence terms for AI use not reviewed.
- **Dow Jones Risk & Compliance (Screening & Monitoring API): UNVERIFIED.** Only third-party listings of developer.dowjones.com found.
- **IRS EO BMF / Pub 78 / Auto-Revocation / TEOS bulk files: EXCEPTION-FILES.** Authoritative and free; files only, no API. *Note:* Adapter: download -> diff -> CharityEligibilityChanged events; freshness SLO (tech architecture section 5).
- **OFAC sanctions lists: EXCEPTION-FILES.** Authoritative list downloads; repo design is version-pinned downloads. *Note:* Repo technology-architecture section 5; no OFAC API assessed this pass.
- **Candid (Charity Check, Essentials APIs): CONDITIONAL.** Public docs; Subscription-Key auth; versioned (Essentials v3/v4); licence bars data mining for AI/LLM/ML without written consent and limits display to the licensee site. *Note:* Repo b43n26-03; use Charity Check only as a deterministic status cross-check, with written consent before any model/agent use.
- **Charity Navigator API: REJECT.** Licence: ratings 'may not be used in any other calculation'; display only on licensee site; 30-day termination for any reason. *Note:* Repo b43n26-03; display-with-linkback only, never a decision input.
- **Every.org Charity API: CONDITIONAL.** Public docs; public API key; 500 req/min; free for non-commercial use, commercial plans by contact. *Note:* Site terms unread (robots 429) per repo; supplementary data only.
- **Pledge API: UNVERIFIED.** Public docs and partner MCP server, but API terms are not public; Idempotency-Key only for CSV batches (repo). *Note:* Pledge is itself a DAF sponsor; money-moving create_donation tool would not fit instruction-only; scored as a data API only.
- **Goodstack (nonprofit verification API): CONDITIONAL.** Public docs; validation submissions; HMAC-signed webhooks (4 retries over 14h); sandbox host. *Note:* Terms: internal business operations only; no display/transmission of Software (repo b43n26-03).
- **NGOsource (equivalency determinations): REJECT.** No API found; ED is a human process with a central repository shared with member funders. *Note:* Manual partner process; record ED receipt as an evidence event.

#### 7 Crypto donations

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| The Giving Block (Shift4) | Y | Y:REST | P | Y | U | U | U | U | U | U | U | P | **CONDITIONAL** | S106, S107 |
| Coinbase Prime | Y | Y:REST | U | U | Y | U | P | U | U | U | U | Y[I] | **CONDITIONAL** | S108, S109 |
| Anchorage Digital | Y | Y:REST | Y | Y | P | U | U | Y | U | U | U | Y[I] | **CONDITIONAL** | S110, S111 |
| Engiven | N | U | U | U | U | U | U | U | U | U | U | U | **UNVERIFIED** | S112 |

- **The Giving Block (Shift4): CONDITIONAL.** Public docs and partner API (crypto, stock, card); webhook notifications; auth via login endpoint. *Note:* TGB receives and converts gifts for the nonprofit (Model B pass-through) - diligence on funds flow and settlement to sponsor account.
- **Coinbase Prime: CONDITIONAL.** Public docs; withdrawal requests carry idempotency_key; API withdrawals need UI approval by default. *Note:* Sponsor-owned institutional account; auth and sandbox not verified this pass.
- **Anchorage Digital: CONDITIONAL.** 100+ operations; API key plus Ed25519 request signing; signed at-least-once webhooks (enabled on request); 20 rps limit; idempotency on certain endpoints. *Note:* Sandbox not verified.
- **Engiven: UNVERIFIED.** API used by partners (press) but no public reference, auth or sandbox found.

#### 8 Non-cash asset processors

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Non-cash processors (real estate, private equity, other illiquid) | N | N:none | NA | NA | NA | NA | NA | NA | NA | U | U | U | **REJECT** | S113, S114 |

- **Non-cash processors (real estate, private equity, other illiquid): REJECT.** No processor with a public API found; sponsors describe intermediaries and manual preapproval/appraisal. *Note:* Charitable Solutions LLC and NCF non-cash: no API evidence found - dropped as vendors.

#### 9 E-signature

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DocuSign eSignature API | Y | Y:REST | Y | Y | U | Y | U | U | U | U | U | NA | **SELECT-CANDIDATE** | S115, S116 |
| Dropbox Sign API | Y | Y:REST | P | Y | U | Y | U | U | U | U | U | NA | **SELECT-CANDIDATE** | S117 |
| Adobe Acrobat Sign API | U | U | U | U | U | U | U | U | U | U | U | NA | **UNVERIFIED** | repo |

- **DocuSign eSignature API: SELECT-CANDIDATE.** JWT grant for system integration; Connect webhooks with HMAC; free developer sandbox. *Note:* Developer blog sources; HMAC keys created only in admin UI.
- **Dropbox Sign API: SELECT-CANDIDATE.** Callbacks with hash verification and ~3-day retries; test_mode on requests.
- **Adobe Acrobat Sign API: UNVERIFIED.** Search returned no usable evidence this pass - dropped from scoring.

#### 10 Accounting / GL

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oracle NetSuite (SuiteTalk REST) | Y | Y:REST | Y | U | U | U | U | U | U | U | U | NA | **CONDITIONAL** | S118 |
| Sage Intacct (REST) | Y | Y:REST | Y | U | U | P | U | U | U | U | U | NA | **CONDITIONAL** | S119, S120 |
| QuickBooks Online Accounting API | Y | Y:REST | Y | Y | Y | Y | U | Y | U | U | U | NA | **SELECT-CANDIDATE** | S121, S122 |
| Microsoft Dynamics 365 Business Central | Y | Y:REST/OData | Y | Y | U | U | U | U | U | U | U | NA | **CONDITIONAL** | S123, S124 |

- **Oracle NetSuite (SuiteTalk REST): CONDITIONAL.** OAuth 2.0 client credentials with certificate-signed JWT for REST; webhooks and idempotency not found.
- **Sage Intacct (REST): CONDITIONAL.** OAuth 2.0; developer subscription via account manager; webhook support conflicting between sources; sandbox paid.
- **QuickBooks Online Accounting API: SELECT-CANDIDATE.** OAuth 2.0; requestid for idempotent retries; webhooks (separate sandbox set); sandbox companies; published limits. *Note:* Fits smaller sponsors; idempotency guidance from Intuit posts.
- **Microsoft Dynamics 365 Business Central: CONDITIONAL.** Entra ID OAuth; webhook subscriptions with 36h retries; idempotency not found. *Note:* Webhook pages partly older versions.

#### 11 Advisor/wealth platforms

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Orion | P | Y:REST | Y | U | U | P | U | U | U | U | U | NA | **CONDITIONAL** | S125 |
| Envestnet | N | U | U | U | U | U | U | U | U | U | U | NA | **UNVERIFIED** | S126 |
| Addepar | Y | Y:REST(JSON:API) | Y | U | U | U | U | U | P | U | U | NA | **CONDITIONAL** | S127, S128 |
| SS&C Black Diamond | N | Y:REST(OpenAPI 3) | Y | U | U | P | U | U | Y | U | U | NA | **UNVERIFIED** | S129, S130 |
| Morningstar | P | Y:REST | P | U | U | U | U | U | U | U | U | NA | **UNVERIFIED** | S131 |
| Salesforce Financial Services Cloud | Y | Y:REST | Y | U | U | U | Y | U | U | U | U | NA | **CONDITIONAL** | S132 |
| Redtail CRM | N | Y:REST | P | U | U | P | U | U | U | U | U | NA | **UNVERIFIED** | S133 |
| Wealthbox | Y | Y:REST | Y | U | U | U | U | U | U | U | U | NA | **CONDITIONAL** | S134 |

- **Orion: CONDITIONAL.** OAuth guide public; full API docs require credentials; staging host; sandbox by approval. *Note:* Integration target chosen by partners.
- **Envestnet: UNVERIFIED.** API reference and credentials gated behind portal credentials via account manager.
- **Addepar: CONDITIONAL.** Public docs; OAuth 2.0 auth code with 240-second tokens; Import API beta only.
- **SS&C Black Diamond: UNVERIFIED.** OAuth 2.0, OpenAPI 3 schema, sandbox with fabricated data and bulk Batch Module claimed; portal gated.
- **Morningstar: UNVERIFIED.** Several API families with different auth (token, IP allow-list, OAuth client credentials); access sales-gated.
- **Salesforce Financial Services Cloud: CONDITIONAL.** Public FSC Business APIs and Integrations API; events/sandbox not re-verified this pass.
- **Redtail CRM: UNVERIFIED.** Docs and dev environment via partner programme; API key per organisation.
- **Wealthbox: CONDITIONAL.** Public API docs; OAuth for partner apps by request to support; personal tokens reported deprecated Oct 2026.

#### 12 Communications

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Postmark | Y | Y:REST | U | Y | N | U | U | U | U | U | U | NA | **CONDITIONAL** | S135 |
| Twilio (SMS/voice) | U | U | U | U | U | U | U | U | U | U | U | NA | **UNVERIFIED** | repo |
| SendGrid (Twilio) | U | U | U | U | U | U | U | U | U | U | U | NA | **UNVERIFIED** | repo |

- **Postmark: CONDITIONAL.** Vendor states no idempotency-key support; at-least-once webhooks. *Note:* Dedupe in outbox; low criticality.
- **Twilio (SMS/voice): UNVERIFIED.** Not assessed in depth this pass (brief category).
- **SendGrid (Twilio): UNVERIFIED.** Not assessed in depth this pass; only an unreliable third-party claim of no idempotency.

#### 13 LLM/model providers

| Vendor | Docs | Style | Auth | Push | Idem | Sbx | Ver | Rate | Bulk | Assur | Licence | Fit | Verdict | Sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Anthropic API | Y | Y:REST | P | NA | NA | NA | U | U | NA | Y | Y | NA | **SELECT-CANDIDATE** | S136, S137, S138 |
| OpenAI API | Y | Y:REST | P | NA | NA | NA | U | U | NA | Y | Y | NA | **SELECT-CANDIDATE** | S139, S140 |
| Azure OpenAI (Azure AI Foundry) | Y | Y:REST | Y | NA | NA | NA | U | U | NA | U | P | NA | **CONDITIONAL** | S141 |
| Amazon Bedrock | Y | Y:REST | Y | NA | NA | NA | U | U | NA | U | Y | NA | **SELECT-CANDIDATE** | S142, S143 |
| Google Vertex AI | Y | Y:REST | Y | NA | NA | NA | U | U | NA | U | P | NA | **CONDITIONAL** | S144 |

- **Anthropic API: SELECT-CANDIDATE.** Terms: may not train on Customer Content; ZDR by arrangement; inference_geo=us residency; SOC 2 Type 2, ISO 27001/27017/27018 (vendor page). *Note:* Assessor is an Anthropic model; scores rest on cited pages only.
- **OpenAI API: SELECT-CANDIDATE.** No training on API data by default; ZDR for qualifying orgs; regional residency; SOC 2 Type 2 (vendor claim).
- **Azure OpenAI (Azure AI Foundry): CONDITIONAL.** Abuse monitoring stores prompts/completions up to 30 days unless an exemption is approved. *Note:* Entra ID auth.
- **Amazon Bedrock: SELECT-CANDIDATE.** Account-level retention modes incl. zero retention; zero operator access model with stated exceptions. *Note:* Bedrock-side inference_geo not available per third-party tracker.
- **Google Vertex AI: CONDITIONAL.** ZDR requires an abuse-monitoring exception and disabling caching.

---

## 4. Identity: fit for partner federation and MFA

**The requirement.** Partner organizations own the accounts and their users (advisors, wealth-firm staff, sponsor staff). The platform therefore needs to: (a) trust each partner's IdP over SAML 2.0 or OIDC, (b) take user lifecycle from the partner over SCIM 2.0, so a leaver loses access when the partner removes them, (c) keep partners isolated as organizations/tenants, (d) require MFA, including phishing-resistant WebAuthn/passkeys, (e) step up for risky actions (`acr`), (f) mint the agent-principal tokens in the API catalog with RFC 8693 token exchange (`act` claim), (g) sender-constrain tokens (mTLS or DPoP), and (h) meet FAPI 2.0 for institution-to-platform APIs.

| Vendor | Partner IdP federation | SCIM 2.0 inbound | Orgs / tenants | MFA incl. WebAuthn | Step-up (`acr`) | RFC 8693 token exchange | DPoP / mTLS | FAPI 2.0 | Sources |
|---|---|---|---|---|---|---|---|---|---|
| Auth0 (Okta CIC) | Y: per-org SAML/OIDC enterprise connections | Y: on SAML, OIDC, Okta, Entra connections | Y: Organizations | P: per-org MFA policy; WebAuthn not re-verified | U | U | mTLS Y (HRI); DPoP U | **Y**: FAPI 2.0 SP profiles (HRI add-on, Enterprise plan) | S57–S59 |
| Okta Workforce | Y* | U | U | U | **Y**: `acr_values` | **Y**: OBO token exchange; ID-JAG for agents | DPoP **Y** | U | S53–S56 |
| Microsoft Entra ID / External ID | Y: SAML/WS-Fed, but every partner user becomes a B2B guest; max 1,000 federations | U | P: tenant + guest model | P: can accept MFA claims from the federated IdP | U | P: proprietary OBO flow, not RFC 8693 | U | not found | S60–S62 |
| Ping (PingFederate / PingOne) | Y: partner IdP federation is a core use | P (third-party source) | U | P (third-party source) | U | **Y**: PingFederate; PingOne since Mar 2026 | U | P: FAPI 1 Advanced certified (PingFederate 11.0); FAPI 2.0 not found | S63–S66 |
| WorkOS | Y: per-org SAML/OIDC | Y: Directory Sync | Y | Y: MFA, passkeys | U | U | U | U | S67–S68 |
| Stytch (Twilio) | Y: SAML/OIDC per org | Y | Y | Y: incl. WebAuthn | U | U | U | U | S69–S71 |
| Keycloak (open source) | Y* (identity brokering) | **Y**: SCIM API supported in 26.8 | Y* | Y* | Y* | **Y**: supported since 26.2 | **Y**: DPoP supported 26.4; mTLS Y* | **Y**: FAPI 2.0 SP + Message Signing (26.4; project notes gaps) | S73–S76 |
| FusionAuth | U | U | U | U | U | U | U | U | S72 (third-party only) |

**Reading the matrix.**
1. **No single product is proven on every column.** The documented strengths split two ways. Partner-onboarding brokers (WorkOS, Stytch, Auth0 Organizations) are strong on per-partner SSO, SCIM and self-serve admin. Authorization servers (Keycloak, Auth0 with HRI, PingFederate, Okta) are strong on token exchange, DPoP/mTLS and FAPI.
2. **MFA under federation must be enforced by the platform, not assumed from the partner.** When a partner IdP authenticates the user, the partner performs MFA. Entra documents accepting MFA claims from a federated IdP (S61). A third-party review says WorkOS does not apply its own MFA enforcement to SSO users (LoginRadius summary; not confirmed in WorkOS docs). The platform should require `amr`/`acr` evidence of MFA in the partner assertion, and should run its **own** WebAuthn step-up before money-moving or privilege-changing actions (grant above `confirm_above`, payee changes, `privileges:manage`), whatever the partner IdP did.
3. **Token exchange is required, not optional.** The API catalog's agent-principal token uses RFC 8693 `act` (api-catalog §3). Products with documented RFC 8693 support: Keycloak (26.2+), PingFederate and PingOne, Okta (OBO, plus ID-JAG for agents). Entra's OBO is a different, proprietary grant.

**Recommendation.**
- **Authorization server for platform APIs and agent tokens:** **Keycloak** (self-hosted) is the only candidate with documented RFC 8693, DPoP, FAPI 2.0 and SCIM support, and it removes vendor lock-in. The cost is that the platform runs, patches and audits it. The commercial alternative is **Auth0 with the Highly Regulated Identity add-on** (FAPI 2.0, mTLS), subject to confirming RFC 8693 support and WebAuthn, or **PingFederate** (token exchange; FAPI 1 Advanced certified).
- **Partner federation and provisioning:** **Auth0 Organizations** (per-org SAML/OIDC connections, inbound SCIM and per-org MFA in one tenant) or **WorkOS** (per-org SSO, Directory Sync, admin portal, SOC 2 Type 2) as a broker in front of the authorization server.
- **Combination to test first:** Auth0 alone (Organizations + HRI) as the simplest commercial option; Keycloak + WorkOS as the open-standards option. Either way, step-up WebAuthn is the platform's own control.
- **Not recommended as the partner-facing layer:** Entra External ID (guest-account model, 1,000-federation cap, non-standard token exchange). Entra or Okta Workforce remain sensible for the platform's **own staff**.

---

## 5. Categories with no API-capable vendor, and the design consequence

| Gap | Evidence | Design consequence |
|---|---|---|
| **IRS eligibility data** (EO BMF, Pub 78, auto-revocation, TEOS) | Bulk files only (S96, S97) | EXCEPTION-FILES. Scheduled download → diff → `CharityEligibilityChanged` events, with a freshness SLO that blocks the deterministic path when stale (technology-architecture §5). The adapter is the platform's API |
| **OFAC lists** | List downloads (repo design) | Version-pinned downloads, re-screen on change; OpenSanctions yente self-hosted gives a matching API over the same data |
| **Incumbent custodians** (Schwab, Fidelity, BNY Pershing) | Docs gated; daily files and batch are the documented paths (S01–S06) | Custodian file adapter → position/transaction events → daily three-way reconciliation. Treat any API access obtained under NDA as an upgrade, not a dependency. Partners who hold accounts at these custodians bring this constraint with them |
| **Non-cash assets** (real estate, private equity, other illiquid) | No processor API found; sponsors describe intermediaries and manual preapproval and appraisal (S113, S114) | Manual partner process with structured case objects: the platform records `ContributionIntent`, appraisal evidence and liquidation proceeds as events entered by staff or uploaded documents. No agent may act on the processor's behalf |
| **Equivalency determinations** (NGOsource) | No API found (S105) | Manual request; record ED receipt, expiry and funder scope as evidence events; expiry drives re-review |
| **PayPal Grant Payments** | Grantmaker integration method not public (S38); Braintree "Grant API" is a different product (S39) | Do not depend on it. If a sponsor already uses it, treat it as a partner-operated rail reconciled from reports |
| **Engiven** | API used by partners (press) but no public reference (S112) | Prefer custody APIs (Anchorage, Coinbase Prime) for sponsor-owned crypto |

---

## 6. Concentration risks, conditions and open items

**Concentration.**
- **Chariot on Column N.A.** (industry report §2.7; Chariot states its deposit account is a Column DDA and says the organization cannot bring its own bank account; vendor help pages, S37). If the platform also picks Column as its ODFI, a Column outage or exit takes out both the network rail and the direct ACH rail. Use a different bank for direct ACH (J.P. Morgan, U.S. Bank, or the sponsor's existing treasury bank via Modern Treasury).
- **Plaid** for both account verification and KYC concentrates two controls on one vendor.
- **Stytch** is now owned by Twilio (closed 2025-11-14, S71); if Twilio also carries SMS, OTP delivery and identity share one parent.

**Conditions that must go into contracts.**
- Modern Treasury: bring-your-own-bank only; no FBO custodial accounts on the platform's behalf (S25).
- Dwolla, Moov: bank-to-bank funding sources only; no Dwolla Balance or Moov wallet holding sponsor funds (S27, S31).
- Chariot: confirm the deposit account is titled to the sponsor (vendor claim, S37); require idempotency keys on every disbursement call (optional in the API, S33); obtain the SOC 2 Type II report.
- Candid: written consent before any model, agent or ranking use of Candid data (b43n26-03).
- OpenSanctions: commercial data licence; compliance screening counts as commercial use (S90).

**Auth posture.** Most payment and data vendors offer only API keys or HTTP Basic (`P` on C3): Column, Increase, Modern Treasury, Chariot, Persona, Alloy, Plaid. Only J.P. Morgan (JWT with public key, mTLS + digital signature), Dwolla (OAuth 2.0 client credentials), IBKR (private_key_jwt) and Anchorage (Ed25519 request signing) document stronger client authentication. Compensating controls: per-environment keys in a secrets manager, egress allow-listing, key rotation, and the platform's own approval gate before any money-moving call.

**Open items (could change verdicts).**
1. Read Schwab, Fidelity and BNY Pershing API references under NDA (would move them out of UNVERIFIED).
2. Confirm J.P. Morgan GP2 idempotency covers ACH (CONDITIONAL → SELECT-CANDIDATE).
3. Confirm Column and Increase account eligibility and titling for a 501(c)(3) sponsor opening its own account (not as a fintech's end customer).
4. Confirm Apex supports charitable entity/omnibus accounts for DAF pools.
5. Confirm Auth0 RFC 8693 token exchange and WebAuthn, and WorkOS MFA behaviour for SSO users, from vendor docs.
6. Re-assess FusionAuth, Dow Jones, Adobe Acrobat Sign, Twilio and SendGrid from vendor documentation (no usable evidence this pass).
7. Mutual-fund omnibus options were not assessed: no evidence was gathered.

---

## 7. Sources

All accessed 2026-11-21. Several were read through search-result summaries rather than direct fetches; where a direct fetch failed (Schwab advisor page, IBKR OAuth page: HTTP 403) the score relies on search snippets of the official page. Column's OpenAPI file (S18) was downloaded and its `securitySchemes`, idempotency and sandbox text inspected directly.

**Repository sources:** [technology-architecture.md §5](technology-architecture.md#5-integration-architecture); [api-catalog.md §3](../04-enterprise-apis/api-catalog.md#3-authentication-and-authorization-model); [regulatory-applicability-map.md §14](../08-governance-and-compliance/regulatory-applicability-map.md#14-money-transmission-implications-for-a-multi-sponsor-infrastructure-provider); [landscape-and-evidence.md](../charity-vetting-ai/landscape-and-evidence.md); [b43n26-03-charity-data-terms-ai.md](../../mission-2026-11-14/b43n26-03-charity-data-terms-ai.md); [queue-payment-rails-cluster.md](../../mission-2026-11-14/queue-payment-rails-cluster.md); [DAF-INDUSTRY-REPORT-2026-11.md §2.5–2.7](../../DAF-INDUSTRY-REPORT-2026-11.md#25-payment-rails); [framework-feedback-proposals.md FP-09](../workflow-innovation/12-implementation-proposals/framework-feedback-proposals.md).

| ID | URL |
|---|---|
| S01 | https://advisorservices.schwab.com/managing-your-business/tech-integration/api-integration |
| S02 | https://advisorservices.schwab.com/whats-new/third-party-integration |
| S03 | https://clearingcustody.fidelity.com/app/item/RD_9883092/integration-xchange.html |
| S04 | https://www.businesswire.com/news/home/20200218005068/en/ |
| S05 | https://www.bny.com/pershing/us/en/about/news/press-release/pershing-reimagines-its-integration-portal.html |
| S06 | https://www.bny.com/pershing/us/en/solutions/wealth-technology/integrated-wealth-management-technology.html |
| S07 | https://apexfintechsolutions.com/developers/developer-portal/devex-and-sandbox/ |
| S08 | https://cdn.jsdelivr.net/npm/@apexfintechsolutions/ascend-sdk@1.8.4/docs/sdks/accounttransfers/README.md |
| S09 | https://cdn.jsdelivr.net/npm/@apexfintechsolutions/ascend-sdk@1.8.4/docs/sdks/authentication/README.md |
| S10 | https://developer.altruist.com |
| S11 | https://apis.io/providers/altruist/ |
| S12 | https://www.interactivebrokers.com/docs/web-api/authentication/oauth-2/introduction |
| S13 | https://developer.payments.jpmorgan.com/api/treasury/global-payments/overview |
| S14 | https://developer.payments.jpmorgan.com/api/mtls-with-digital-signature |
| S15 | https://developer.payments.jpmorgan.com/docs/treasury/global-payments/capabilities/global-payments-2/ach/how-to/initiate-ach-payment |
| S16 | https://docs.column.com/working-with-the-api/idempotency |
| S17 | https://docs.column.com/working-with-the-api/events-and-webhooks |
| S18 | https://docs.column.com/openapi.json |
| S19 | https://increase.com/documentation/api/overview |
| S20 | https://increase.com/documentation/idempotency-keys |
| S21 | https://increase.com/pdfs/System_and_Organization_Controls_2_Type_2_2025.pdf |
| S22 | https://docs.moderntreasury.com/reference/idempotent-requests |
| S23 | https://docs.moderntreasury.com/platform/reference/authentication |
| S24 | https://docs.moderntreasury.com/platform/docs/end-to-end-testing-in-the-mt-sandbox |
| S25 | https://moderntreasury.com/llms.txt |
| S26 | https://www.moderntreasury.com/legal/security-policy |
| S27 | https://docs.moov.io/guides/money-movement/idempotency/ |
| S28 | https://docs.moov.io/changelog/2026-01-13 |
| S29 | https://developers.dwolla.com/docs/api-reference/api-fundamentals/idempotency-key |
| S30 | https://developers.dwolla.com/llms.txt |
| S31 | https://developers.dwolla.com/docs/balance-funding-source.md |
| S32 | https://docs.stripe.com/treasury/connect/requirements |
| S33 | https://docs.givechariot.com/v2026-04-01/api/disbursements/create.md |
| S34 | https://docs.givechariot.com/v2026-04-01/api/authentication.md |
| S35 | https://docs.givechariot.com/v2026-04-01/guides/disbursements/how-it-works.md |
| S36 | https://docs.givechariot.com/v2026-04-01/llms.txt |
| S37 | https://help.givechariot.com/gift-processing/banking-and-data-security |
| S38 | https://www.paypal.com/us/smarthelp/article/FAQ4654 |
| S39 | https://developer.paypal.com/braintree/docs/reference/xml-api/grant-api/overview |
| S40 | https://www.wellsfargo.com/com/treasury-management |
| S41 | https://developer.bankofamerica.com/CPODevPortal/apidocs/cms-api/public/content/hero/APISetupForm.pdf |
| S42 | https://business.bofa.com/en-us/content/cashpro-api-integration.html |
| S43 | https://developer.usbank.com/products/treasury-builder/v1 |
| S44 | https://plaid.com/docs/api/products/auth/ |
| S45 | https://plaid.com/docs/api/webhooks/ |
| S46 | https://plaid.com/docs/api/versioning/ |
| S47 | https://support.plaid.com/hc/en-us/articles/16206114378775-Does-Plaid-regularly-undergo-compliance-audits-and-if-so-which-ones |
| S48 | https://developer.mastercard.com/open-finance-us/documentation/products/pay/ |
| S49 | https://docs.mx.com/use-cases/payment-verification |
| S50 | https://docs.mx.com/api-reference/platform-api-2026/reference/verify-member |
| S51 | https://amer.developers.trustly.com/api-reference/api/accounts/get-accounts-verify |
| S52 | https://amer.developers.trustly.com/integrate/get-started/overview-and-solutions |
| S53 | https://developer.okta.com/docs/guides/step-up-authentication/main/ |
| S54 | https://developer.okta.com/docs/guides/set-up-token-exchange/main |
| S55 | https://developer.okta.com/docs/guides/dpop/-/main/ |
| S56 | https://developer.okta.com/docs/guides/ai-agent-third-party-token-exchange/main/ |
| S57 | https://auth0.com/docs/get-started/b2b-connect-enterprise |
| S58 | https://auth0.com/docs/authenticate/protocols/scim/configure-inbound-scim |
| S59 | https://auth0.com/docs/get-started/applications/configure-fapi-compliance |
| S60 | https://learn.microsoft.com/en-us/entra/external-id/direct-federation-overview |
| S61 | https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-expected-inbound-assertions |
| S62 | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow |
| S63 | https://docs.pingidentity.com/pingfederate/13.1/introduction_to_pingfederate/pf_token_exchange_grant.html |
| S64 | https://docs.pingidentity.com/pingone/use_cases/p1_oauth_2_token_exchange.html |
| S65 | https://docs.pingidentity.com/pingfederate/12.3/release_notes/pf_release_notes_110.html |
| S66 | https://www.pingidentity.com/en/products/capabilities/federated-access-management.html |
| S67 | https://workos.com/authkit.md |
| S68 | https://workos.com/security |
| S69 | https://stytch.com/docs/get-started/guides/enterprise-ready |
| S70 | https://stytch.com/docs/api-reference/b2b/api/sso/overview |
| S71 | https://twilio.com/en-us/blog/company/news/twilio-to-acquire-stytch |
| S72 | https://www.loginradius.com/protocol/fusionauth |
| S73 | https://www.keycloak.org/2025/05/standard-token-exchange-kc-26-2 |
| S74 | https://www.keycloak.org/2025/09/keycloak-2640-released |
| S75 | https://www.keycloak.org/2026/10/keycloak-2680-released |
| S76 | https://www.keycloak.org/securing-apps/specifications |
| S77 | https://docs.withpersona.com/idempotence |
| S78 | https://docs.withpersona.com/versioning |
| S79 | https://withpersona.com/security |
| S80 | https://developer.alloy.com/public/docs/authentication-guide |
| S81 | https://developer.alloy.com/public/reference/sandbox-vs-production |
| S82 | https://developer.socure.com/ |
| S83 | https://help.socure.com/riskos/docs/troubleshoot-webhooks |
| S84 | https://documentation.identity.entrust.com/api/latest/ |
| S85 | https://documentation.identity.entrust.com/api/api-versioning-policy/ |
| S86 | https://plaid.com/docs/api/products/identity-verification/ |
| S87 | https://plaid.com/docs/api/products/monitor/ |
| S88 | https://www.opensanctions.org/docs/api/authentication |
| S89 | https://www.opensanctions.org/docs/self-hosted/ |
| S90 | https://www.opensanctions.org/docs/commercial/exemption/ |
| S91 | https://complyadvantage.com/blog/complyadvantage-releases-api-documentation |
| S92 | https://complyadvantage-knowledge-base.help.usepylon.com/articles/1901668528-mesh-api-faqs |
| S93 | https://developers.lseg.com/en/api-catalog/customer-and-third-party-screening/world-check-one-api/quick-start |
| S94 | https://developers.lseg.com/en/api-catalog/customer-and-third-party-screening/world-check-one-zero-footprint-screening-api |
| S95 | https://jentic.com/apis/dowjones.com/dowjones |
| S96 | https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads |
| S97 | https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf |
| S98 | https://developer.candid.org/docs/authentication |
| S99 | https://developer.candid.org/reference |
| S100 | https://www.charitynavigator.org/products-and-services/api/ |
| S101 | https://docs.every.org/docs/intro |
| S102 | https://developer.pledge.to/guides/mcp/ |
| S103 | https://docs.goodstack.io/docs/guides/Cause verification/verification-api |
| S104 | https://docs.goodstack.io/docs/api/goodstack-services |
| S105 | https://nonprofitlawblog.com/international-grantmaking-equivalency-determinations/ |
| S106 | https://docs.thegivingblock.com/llms.txt |
| S107 | https://thegivingblock.com/developer-resources/ |
| S108 | https://docs.cdp.coinbase.com/api-reference/prime-api/rest-api/transactions/create-withdrawal.md |
| S109 | https://docs.cdp.coinbase.com/prime/concepts/transactions/withdrawals.md |
| S110 | https://docs.anchorage.com/knowledge-base/api-reference/introduction.md |
| S111 | https://docs.anchorage.com/knowledge-base/porto/developers/webhooks/webhooks-delivery |
| S112 | https://engiven.com/ |
| S113 | https://www.schwab.com/learn/story/noncash-charitable-contributions |
| S114 | https://www.nptrust.org/donating-non-cash-assets-with-donor-advised-funds/ |
| S115 | https://www.docusign.com/blog/developers/docusign-esignature-integration-101-implementing-jwt-authentication |
| S116 | https://docusign.com/blog/developers/introducing-oauth-connect-enhanced-security-webhooks |
| S117 | https://developers.hellosign.com/api/manual-reference-pages/glossary/callbacks-events |
| S118 | https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_157780312610.html |
| S119 | https://developer.sage.com/intacct/docs/developer-portal/guides/oauth2 |
| S120 | https://developer.sage.com/intacct/docs/developer-portal/rest-api-faq |
| S121 | https://developer.intuit.com/app/developer/qbo/docs/develop/webhooks/configure-webhooks |
| S122 | https://developer.intuit.com/app/developer/qbo/docs/learn/rest-api-features |
| S123 | https://learn.microsoft.com/dynamics365/business-central/dev-itpro/api-reference/v2.0/dynamics-subscriptions |
| S124 | https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/webservices/authenticate-web-services-using-oauth |
| S125 | https://developers.orionadvisor.com/guides/oauth/ |
| S126 | https://developer.envestnet.com/products/envestnet/investor-experience |
| S127 | https://developers.addepar.com/docs/oauth |
| S128 | https://developers.addepar.com/docs/import-tool |
| S129 | https://www.sscblackdiamond.com/media/vvigpui2/ssc-black-diamond-product-brief-api.pdf |
| S130 | https://www.sscblackdiamond.com/discover/blog/the-need-for-apis-in-today-s-fintech-space/ |
| S131 | https://developer.morningstar.com/content/apis/market-data/overview/api-md-apis-overview.md |
| S132 | https://developer.salesforce.com/docs/industries/fsc/overview |
| S133 | https://corporate.redtailtechnology.com/api |
| S134 | https://www.wealthbox.com/api/ |
| S135 | https://postmarkapp.com/support/article/what-is-an-idempotency-key |
| S136 | https://www.anthropic.com/legal/commercial-terms |
| S137 | https://platform.claude.com/docs/en/manage-claude/data-residency |
| S138 | https://claude.com/regional-compliance |
| S139 | https://openai.com/business-data/ |
| S140 | https://openai.com/api-data-privacy |
| S141 | https://learn.microsoft.com/en-us/legal/cognitive-services/openai/data-privacy |
| S142 | https://aws.amazon.com/blogs/security/enforce-zero-data-retention-on-amazon-bedrock-with-bedrock-projects-and-service-control-policies/ |
| S143 | https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html |
| S144 | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance |
| S145 | https://docs.withpersona.com/webhooks |
| S146 | https://developer.alloy.com/public/docs/webhook-events |
