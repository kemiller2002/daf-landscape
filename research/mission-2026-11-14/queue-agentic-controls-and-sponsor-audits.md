# Agent-initiated donation controls, gated SOC metadata and sponsor audits (P-QA3-05, P-ASR-05, P-ASR-07, P-QA3-01)

**Date:** 2026-11-14 · **Queue items:** P-QA3-05, P-ASR-05, P-ASR-07, P-QA3-01 (`data/mission-2026-11-14/research-priority-queue.csv`) · **Datasets:** `data/mission-2026-11-14/agentic-control-gap-matrix.csv` (40 rows), `data/mission-2026-11-14/sponsor-audit-notes.csv` (12 rows), `data/mission-2026-11-14/queue-proposals-agentic-audits.csv` (6 proposals)

**How this was done.** I used public documents only: contract and policy text, developer documentation, trust-center page content served to anonymous visitors, and audited financial statements that sponsors post publicly. I created no account, made no write call, requested no report and contacted nobody. Where a sponsor offers audited statements "on request", I recorded that and did not ask. Quotes are verbatim and 40 words or fewer. "Not publicly documented" means I searched for the item and did not find it. It does not mean the item does not exist.

**Builds on:** `research/mission-2026-11-14/queue-contract-data-rights-agent-controls.md` (§3 documented agent controls), `data/mission-2026-11-14/agentic-integration-controls.csv`, `research/mission-2026-11-14/queue-assurance-everyorg-givinga-monitoring.md`, `data/mission-2026-11-14/vendor-assurance-scope-2026.csv` and `research/mission-2026-11-14/ai-governance-failure-modes.md` (§5: governance model, asymmetric-permission rule).

---

## 1. Answers

### P-QA3-05 / P-ASR-05: What controls govern agent- or third-party-initiated donations?

**Answer (high confidence on what is documented; medium on TIFIN):** none of the four operators has a public contract that treats an AI agent as a distinct actor. Sponsor review after submission is the only control documented for all four, and it is weakest for TIFIN's Louise, where the action path itself is undocumented. Liability for an erroneous or hijacked agent action falls on the donor or customer in every public contract read.

Gap counts from `agentic-control-gap-matrix.csv` (10 control dimensions per operator):

| Operator | Meets | Partial | Gap | Unknown | Weakest points |
|---|---|---|---|---|---|
| Daffy (MCP, REST, CLI; Member Agreement) | 1 | 3 | 6 | 0 | Full-power credentials, no limits, client-side confirmation, no agent ID, member bears loss |
| TIFIN Give / GiveClear (Louise; Program Guidelines) | 0 | 1 | 1 | 8 | Louise's action path undocumented; terms cover AI "insights", not execution |
| Endaoment (OAuth API, partner API; T&C 2026-08-12) | 0 | 8 | 2 | 0 | No amount limits; partner grants carry no donor context; user bears loss |
| Chariot (DAFpay/Connect, core API; Nonprofit Terms 2026-10-14) | 3 | 5 | 2 | 0 | No initiator field; public terms put automation errors on the customer |

**Main findings**

1. **Daffy's contract has not caught up with its agent product, and in one place it cuts the other way.** The Member Agreement (updated 2025-11-11) has no agent, API or MCP clause. It states "An unlimited number of one-time or recurring donations may be recommended from a fund in any given month" ([Member Agreement](https://www.daffy.org/legal/agreement)). It puts unauthorized-use loss on the member: "Daffy is not responsible for any losses resulting from account fraud, theft, or any other unauthorized activity" (same source). Members must report errors "within 10 days", and "Donations that have already been approved and issued cannot be canceled by the member" (same source). Daffy's own docs say every agent route "acts as you, on your fund" ([agents](https://docs.daffy.org/agents)).
2. **Daffy has a contractual affirmation duty, but nothing documents how an agent path satisfies it.** "Members will be required to affirm that their donation recommendation adheres with this policy each time a donation recommendation is made" ([Member Agreement](https://www.daffy.org/legal/agreement)). On the MCP path, confirmation depends on clients that "honour tool annotations" ([agents](https://docs.daffy.org/agents)). The CLI prompt can be skipped with `--yes` ([CLI](https://docs.daffy.org/agents/cli)). The REST API documents no confirmation at all ([donations](https://docs.daffy.org/ref/donations)).
3. **Daffy's control that holds is sponsor discretion.** "Once approved by Daffy at its sole discretion" and "member recommendations are only advisory" ([Member Agreement](https://www.daffy.org/legal/agreement)). The MCP tool surface is limited to donor-side actions (search, read, make or cancel a donation). An agent therefore cannot reach the approval state through any documented tool. I count that as partial compliance with the repo's rule "AI may add a flag, never clear one" (`ai-governance-failure-modes.md` §5 item 3). Whether Daffy's own review uses AI is not documented.
4. **TIFIN Give / GiveClear: the sponsor's control is documented, the agent's is not.** The GiveClear Program Guidelines (updated 2025-08-12) state "Any grant recommendations are under the exclusive legal control of the DAF Sponsor, GiveClear". They also say grants "are reviewed for approval within 48 hours of submission unless additional due diligence is required" ([Program Guidelines](https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines)). The guidelines say nothing about AI, Louise as an assistant, or revoking an Advisor's authority. "Louise Giving Technologies LLC" appears only as the legal name of TIFIN Give. The TIFIN AI Assistant Addendum describes a tool that generates "insights" that "undergo a compliance check to ensure that they do not constitute investment advice" ([TIFIN Terms](https://intercom.help/give-ria/en/articles/10092486-terms-of-use)). The launch release, by contrast, says Louise will "execute real donor requests" ([PR Newswire, 2025-10-27](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)). The only documented AI check therefore screens for investment advice, not grant compliance. Liability: "You are solely responsible for all activity that occurs under your account" (TIFIN Terms).
5. **Endaoment's terms are the only public contract that names the channels.** The T&C (last updated 2026-08-12) cover "Partner Interfaces, and API Access". They state "OAuth consent, and API credential acceptance constitute valid assent for all purposes". They also bind anyone "exercising or purporting to exercise any advisory privilege" ([Endaoment T&C](https://docs.endaoment.org/governance/documentation/terms-and-conditions.md)). The same terms put credential risk on the user: "You are solely responsible for the security of your accounts, wallets, API credentials, OAuth tokens" (same source). The partner "Submit settled grant" call is "Authorized by the tech-platform API key alone — no donor bearer token or acting-user context required" ([submit settled grant](https://docs.endaoment.org/developers/api/partner-endpoints/submit-settled-grant.md)). That page describes no review step. Endaoment review is documented only for donor-recommended grants ([recommending grants](https://docs.endaoment.org/donors/getting-started/recommending-grants.md)). The partner agreement is not public; [Going to Production](https://docs.endaoment.org/developers/quickstart/going-to-prod.md) describes only a validation on a lower environment.
6. **Chariot is the reference pattern for confirmation and sponsor approval, but it has no agent identity.**
   - Confirmation happens in a Chariot-hosted session: "the user always has the ability to review their information and make changes before submission" ([Connect integration](https://docs.givechariot.com/guides/dafpay/integrating-dafpay/integration)).
   - A grant "must be captured within 15 minutes of authorization" or the call returns 410 ([Create Grant](https://docs.givechariot.com/api/grants/create)).
   - Grants enter the DAF provider's review: "Chariot does not bypass your compliance process" ([DAFpay endpoints](https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md)). `Canceled` covers grants where "the DAF provider did not approve it" ([Create Grant](https://docs.givechariot.com/api/grants/create)).
   - Create Grant's only identifying field is `workflowSessionId`. No field records whether a human or an agent drove the session.
   - The Nonprofit Terms' AI clause covers gift-processing automations: "You acknowledge that any automations or logic you establish may have errors and will not hold Chariot responsible" ([Nonprofit Terms](https://www.givechariot.com/legal-nonprofit)).
   - The terms incorporate a "DAFpay Provider Addendum", which is not public. The donor terms page did not render to automated fetch.

**Against the repo's governance rule** (`ai-governance-failure-modes.md` §5 items 2, 3 and 6):

| Rule element | Daffy | TIFIN/GiveClear | Endaoment | Chariot |
|---|---|---|---|---|
| Agent cannot approve or clear flags | Partial (tool surface) | Unknown | Partial (Recommendation split, optional) | Partial (approved_by recorded; creator≠approver not documented) |
| Sponsor approval between submission and payment | Meets | Partial (Louise path unknown) | Partial (partner path unknown) | Meets |
| Server-enforced donor confirmation | Gap | Unknown | Partial | Meets (human flow) |
| Per-agent limits | Gap | Unknown | Gap | Partial (balance only) |
| Agent identity on every recommendation | Gap | Unknown | Partial (partner-level) | Gap |
| Decision record / audit log | Partial | Unknown | Partial | Meets |

### P-ASR-07: What can be learned from public trust-center metadata?

**Answer (medium confidence):** report types and some auditors, but no observation periods, product scopes or carve-out decisions. The new items on 2026-11-14 are Blackbaud's dated incident notices and subprocessor-list update, and Chariot's pen-test statements. Bridge letters are not mentioned by any vendor. Details are in §3.

### P-QA3-01: What do sponsors' posted audited statements show?

**Answer (high confidence for the five statements read):**
- I read five sets of audited statements: Fidelity, Vanguard (FY2026, newly posted), RCF, NCF (new to the repo) and Charityvest (new to the repo).
- All five carry unmodified opinions, none has a going-concern paragraph, and none mentions a SOC report or service-organization reliance.
- Daffy and AEF offer audited statements only on request. Their Form 990s confirm an independent audit and an audit committee.
- NPT posts summary statements without the auditor's report.
- DAFgiving360's financials page returned 403.
- Goldman Sachs Philanthropy Fund, MS GIFT and BofA CGF post nothing.

Details are in §4.

---

## 2. Control-gap matrix (summary)

The full matrix, with verbatim clauses and URLs per cell, is `data/mission-2026-11-14/agentic-control-gap-matrix.csv`. Ratings: **meets** = documented and enforced by the server or sponsor; **partial** = some control documented but short of the repo benchmark; **gap** = documented absence, or a clause that runs against the benchmark; **unknown** = not publicly documented.

| Dimension | Daffy | TIFIN/GiveClear | Endaoment | Chariot |
|---|---|---|---|---|
| Authorization model | gap | unknown | partial | partial |
| Credential scoping | gap | unknown | partial | partial |
| Per-transaction limits | gap | unknown | gap | partial |
| Confirmation | gap | unknown | partial | meets |
| Sponsor approval | meets | partial | partial | meets |
| Authority separation / flag rule | partial | unknown | partial | partial |
| Liability allocation | gap | gap | gap | gap |
| Revocation | partial | unknown | partial | partial |
| Audit logging | partial | unknown | partial | meets |
| Agent identification | gap | unknown | partial | gap |

**Liability allocation is "gap" for all four operators.** Every public contract read puts loss from unauthorized or erroneous activity on the user, and none mentions an AI agent:
- Daffy, Member Agreement: "not responsible for any losses resulting from account fraud, theft, or any other unauthorized activity".
- TIFIN, Terms §1.6: "solely responsible for all activity".
- Endaoment, T&C: credential security; transactions "generally irreversible, final, and without refunds once completed".
- Chariot, Nonprofit Terms: automation errors.

Negotiated customer and partner agreements, which none of these public sources include, may differ.

---

## 3. Gated SOC reports: what public metadata shows (P-ASR-07)

These findings come from page content served to anonymous visitors and from vendor security pages. A query to a trust-center backend API was blocked by the session's permission policy and was not retried. Three trust centers (Give Interactive on Vanta, Chariot on Oneleet, Benevity on SecurityPal) render client-side and return almost no content without JavaScript.

| Vendor | Report types (public) | Dates | Auditor | Subprocessors | Pen test | Bridge letter | New on 2026-11-14 |
|---|---|---|---|---|---|---|---|
| Give Interactive | SOC 2 Type 2; SOC 3 (both gated) | Issued September 2025 per consultant ([BD Emerson](https://www.bdemerson.com/case-studies/give-interactive)) | Not named (BD Emerson was the program consultant) | Not visible | Not visible | Not mentioned | Nothing new; [trust center](https://trust.giveinteractive.com/) HTML is a Vanta shell |
| Chariot | SOC 2 Type II ("SOC 2 Type II compliant") | Report titles 2024-10 and 2025-12 (repo baseline) | Not named | AWS (US) hosting; Column N.A. bank program ([security](https://help.givechariot.com/onboarding/trust-and-safety/security)) | "undergoes regular penetration testing" (same source); a search summary also reports "two penetration tests", with the report available on request (page not reachable; unverified) | Not mentioned | Security page reconfirmed; [trust center](https://trust.givechariot.com/) shell only |
| Foundant | SOC 2 Type 2 (Foundant: Linford & Co LLP; GivingData: Pease Bell CPAs, LLC); SOC 1 Type 2, ISO 27001 (BSI) and "SOC 2/SOC 3 Report" (Deloitte) under SmartSimple only | Not public | As listed (from embedded `auditor` fields) | "Subprocessors" document item (gated); GivingData Azure, SmartSimple AWS | "Application Penetration Testing" and "Network Penetration Testing" controls marked maturity "full" | Not mentioned | Reconfirmed from [trust.foundant.com](https://trust.foundant.com/) HTML |
| Blackbaud | SOC 1 Type II, SOC 2 Type II badges (company-level) | Not public | Not named | Public subprocessor list link to docs.blackbaud.com/privacy/role/subprocessors; `subprocessorUpdatedAt` 2026-09-30 | "Annual third-party penetration testing"; Red Team statement | Not mentioned | Trust-center updates: "Klue Security Incident Update" 2026-07-22 and 2026-09-02; "Klue Security Incident Update - Conclusion" 2026-11-06; "Critical PHP Vulnerability Update" 2026-10-21 and 2026-10-22 ([trust.blackbaud.com](https://trust.blackbaud.com/)) |
| Benevity | "currently issues SOC 1 Type II and SOC 2 Type II reports" | "annual independent evaluations"; no dates | Not named | "up-to-date list of sub-processors" in DPA | "regular penetration testing of our applications, network and infrastructure" | Not mentioned | Program "based on" ISO/IEC 27001 (not certified); CSA STAR Level 1 ([security](https://benevity.com/security)); trust center offline in repo baseline |

**Reading.**
- None of the five vendors publishes observation periods, in-scope products or subservice-organization treatment, so carve-out versus inclusive cannot be determined from public metadata.
- Two pieces of metadata do help. Named auditors appear only at Foundant. Dated incident notices appear only at Blackbaud: the Klue incident notes say there is "no known impact to Blackbaud products".
- A sponsor's request for a vendor's SOC report should ask for the report period, the system description's product list, complementary user-entity controls (CUECs), carve-outs (AWS/Azure) and a bridge letter covering the time since period end.

---

## 4. Sponsor audited statements (P-QA3-01)

The full record is `data/mission-2026-11-14/sponsor-audit-notes.csv`.

| Sponsor | FY end | Status | Auditor | Opinion / date | Related-party or administrator note | Tech/service agreement | Concentration |
|---|---|---|---|---|---|---|---|
| Fidelity Charitable | 2025-06-30 | Read ([PDF](https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf)) | PricewaterhouseCoopers LLP (Boston) | Unmodified; 2025-10-29 | Note 7: FMR paid "amounts equal to the administrative fee the Gift Fund charged its donors, net of any tier price credits"; admin fees $179.9m | National Charitable Services LLC (administration, recordkeeping); Fidelity Brokerage Services (custody) | Mutual funds "primarily with Fidelity Investments" |
| Vanguard Charitable | 2026-06-30 | Read ([PDF](https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf)) | PricewaterhouseCoopers LLP (Philadelphia; signature image) | Unmodified; 2026-10-05 | Vanguard support fees $4,243,096 (FY2025 $4,014,052); in-kind $1.20m; interest-free facility up to $6.5m, undrawn | None named (Give Interactive not mentioned); software costs $0 | 35 of 37 pools are Vanguard funds |
| RCF | 2024-12-31 | Read ([PDF](https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf)) | Blue & Co., LLC (Seymour, IN) | Unmodified; 2025-09-05 | Ren fee "based on 98% of the value of administrative fee revenue"; $19.23m; two Ren employees on the board | Ren service agreement (processing, accounting, reporting, tax returns) | Cash and investments above insured limits only |
| NCF | 2025-12-31 | Read ([PDF](https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf)) | Capin Crouse LLP (Lawrenceville, GA) | Unmodified; 2026-07-08; relies on other auditors for four supporting organizations ($24.1m assets) | About $90.9m in donor-advised distributions to organizations where NCCF's co-founder, management or governance serve on boards | In-house; capitalized software $565k plus $2.0m development costs | Five donors gave 14% of support and revenue (about $624.5m) |
| Charityvest | 2024-12-31 | Read ([index](https://guide.charityvest.org/governance-and-legal/financial-reporting)) | Smith & Howard, P.C. (Atlanta) | Unmodified; 2025-12-01 | Services agreement with Vennfi, "an affiliated for profit entity", priced at an agreed percent; $653,138 (2024) | Vennfi "was acquired by Foundation Source Philanthropic Services Inc." in 2024 "and the agreement was maintained in place with Foundation Source" | Cash above insured limits |
| Daffy | 2024-12-31 | On request ([about](https://www.daffy.org/about)) | Not public | Form 990 (2024) Part XII: audited = Yes; audit committee = Yes | Member Agreement: "Daffy pays Aside, Inc. fair market value for its platform license and services" | Aside, Inc. | n/a |
| AEF | 2023-12-31 (990) | On request ([about](https://www.aefonline.org/about-aef/)) | Not public (RSM US LLP is the 990 preparer and an "accounting services" contractor) | Form 990 (2023) Part XII: audited = Yes, separate basis; audit committee = Yes | n/a | 990 Part VII-B lists NPACT "SOFTWARE DEVELOPMENT" $217,016 ([990](https://www.aefonline.org/wp-content/uploads/2025/01/2023-AEF-990-Public-Disclosure.pdf)) | n/a |
| NPT | 2025-06-30 | Summary only ([PDF](https://www.nptrust.org/fy25-ar-consolidated-financials-npt/)) | Not stated | No auditor's report in document | none | none | none |
| DAFgiving360 | 2025-06-30 (expected) | Not retrieved (HTTP 403) | — | — | — | — | — |
| Goldman Sachs Philanthropy Fund | — | Not public | — | — | — | — | — |
| MS GIFT | — | Not public | — | — | 2024 Impact Report: "Back-office administration provided by RenPSG, an unaffiliated charitable gift administrator" ([report](https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf)) | Ren | — |
| BofA CGF | — | Not public | — | — | — | — | — |

**Reading.**
1. **No sponsor's audited statements mention a SOC report.** That is normal for GAAP statements. It still means that, for X3, audited statements show related-party economics, not platform controls.
2. **Administrator economics are explicit where statements exist.** Fidelity pays FMR the full admin fee net of credits. RCF pays Ren 98%. Charityvest pays Foundation Source an agreed percent. Vanguard pays a fixed fee plus in-kind services. MS GIFT names Ren as its administrator only in a marketing report.
3. **New facts for the repo:**
   - Charityvest's technology provider has been Foundation Source since 2024, which links Charityvest's operations to the DAF OS vendor.
   - AEF paid NPact for software development in 2023, before its announced Ren migration.
   - NCF runs in-house with capitalized software.
   - Vanguard's FY2026 statements still name no technology vendor, a year after the Give Interactive announcement (2025-11-04).
4. **Implications for X3 scoring:**
   - NCF can move from U to 3 (audited statements with related-party notes).
   - Charityvest can move from 2 to 3 (statements now inspected).
   - Daffy and AEF can show only the Form 990 audit indicator.
   - GS Philanthropy Fund, MS GIFT, BofA CGF, DAFgiving360 and NPT stay U for statement content.

   These are suggestions for the quadrant scorer. This file does not change any scores.

---

## 5. Limitations

- The contracts read are public templates or generic terms. Executed customer, partner and DAF-provider agreements (TIFIN Software & Services Agreements, Endaoment partner agreements, Chariot's DAFpay Provider Addendum) may add controls or reallocate liability.
- TIFIN/GiveClear rows are mostly "unknown". Absence of public documentation is not evidence that controls are absent.
- ProPublica PDF downloads returned 403 and the web archive was blocked by egress policy, so Form 990 Part XII data could not be read for six sponsors (proposal P-AGA-01).
- The Vanguard FY2026 auditor was identified from a signature image. All other auditors come from text letterheads. NCF's other-auditor reliance limits the opinion's coverage for four supporting organizations.
- Trust-center findings exclude anything behind access requests by design.

---

## 6. Source register

| ID | Source | URL | Date / version |
|---|---|---|---|
| S01 | Daffy Member Agreement | https://www.daffy.org/legal/agreement (snapshot `data/terms-snapshots/daffy-member-agreement/2026-11-14.txt`) | Updated 2025-11-11 |
| S02 | Daffy agents overview, MCP, CLI | https://docs.daffy.org/agents ; https://docs.daffy.org/agents/mcp ; https://docs.daffy.org/agents/cli (snapshots in `data/terms-snapshots/daffy-*-docs/`) | accessed 2026-11-14 |
| S03 | Daffy donations API, auth | https://docs.daffy.org/ref/donations ; https://docs.daffy.org/auth | accessed 2026-11-14 (via repo) |
| S04 | Daffy about page (audited statements on request; 2024 Form 990) | https://www.daffy.org/about ; https://www.daffy.org/docs/daffy-charitable-fund-2024-form-990.pdf | accessed 2026-11-14 |
| S05 | TIFIN Terms and Conditions (AI Assistant Addendum) | https://intercom.help/give-ria/en/articles/10092486-terms-of-use (snapshot `data/terms-snapshots/tifin-give-terms-of-use/2026-11-14.txt`) | 2025-02-19 |
| S06 | TIFIN Give DAF Program Guidelines (GiveClear) | https://intercom.help/give-ria/en/articles/10924803-tifin-give-donor-advised-fund-program-guidelines | updated 2025-08-12 |
| S07 | TIFIN Give granting FAQ | https://intercom.help/give-ria/en/articles/10670838-granting-faqs | via repo |
| S08 | Louise launch release | https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html | 2025-10-27 |
| S09 | Endaoment Terms and Conditions | https://docs.endaoment.org/governance/documentation/terms-and-conditions.md (snapshot `data/terms-snapshots/endaoment-terms-and-conditions/2026-11-14.txt`) | last updated 2026-08-12 |
| S10 | Endaoment partner journey, settled grant, go-to-prod | https://docs.endaoment.org/developers/quickstart/partner-journey.md ; https://docs.endaoment.org/developers/api/partner-endpoints/submit-settled-grant.md ; https://docs.endaoment.org/developers/quickstart/going-to-prod.md | accessed 2026-11-14 |
| S11 | Endaoment recommending grants, login, errors | https://docs.endaoment.org/donors/getting-started/recommending-grants.md ; https://docs.endaoment.org/developers/quickstart/login-user.md ; https://docs.endaoment.org/developers/quickstart/error-handling.md | via repo |
| S12 | Chariot Terms of Service (nonprofit) | https://www.givechariot.com/legal-nonprofit (snapshot `data/terms-snapshots/chariot-nonprofit-terms/2026-11-14.txt`) | updated 2026-10-14 |
| S13 | Chariot Connect integration; Create Grant | https://docs.givechariot.com/guides/dafpay/integrating-dafpay/integration ; https://docs.givechariot.com/api/grants/create | API v2026-04-01 |
| S14 | Chariot DAFpay endpoints, OAuth, approve disbursement | https://docs.givechariot.com/v2026-04-01/guides/dafpay/oauth/api-endpoints.md ; https://docs.givechariot.com/v2026-04-01/guides/oauth.md ; https://docs.givechariot.com/v2026-04-01/api/disbursements/approve-disbursement.md | API v2026-04-01 |
| S15 | Chariot security page | https://help.givechariot.com/onboarding/trust-and-safety/security | accessed 2026-11-14 |
| S16 | Trust centers (public HTML) | https://trust.giveinteractive.com/ ; https://trust.givechariot.com/ ; https://trust.foundant.com/ ; https://trust.blackbaud.com/ ; https://trust.benevity.com/ | accessed 2026-11-14 |
| S17 | BD Emerson Give Interactive case study | https://www.bdemerson.com/case-studies/give-interactive | via repo and search 2026-11-14 |
| S18 | Benevity security page | https://benevity.com/security | accessed 2026-11-14 |
| S19 | Fidelity Charitable audited statements FY2025 | https://www.fidelitycharitable.org/content/dam/fc-public/docs/fc/audited-financial-statements-2025-2024.pdf | report 2025-10-29 |
| S20 | Vanguard Charitable financial statements FY2026 | https://www.vanguardcharitable.org/sites/default/files/2026-11/VCEP_Financial_Statements_2026.pdf | report 2026-10-05 |
| S21 | RCF audited statements 2024 | https://renaissancecharitable.org/wp-content/uploads/2026/01/2024RCFAuditedFinancialStatements.pdf | report 2025-09-05 |
| S22 | NCF consolidated statements 2025 | https://site.ncfgiving.com//wp-content/uploads/2026/07/NCF-25-Consolidated-FS-Final.pdf | report 2026-07-08 |
| S23 | Charityvest financial reporting page and FY2024 audit | https://guide.charityvest.org/governance-and-legal/financial-reporting | report 2025-12-01 |
| S24 | NPT FY25 consolidated financials (annual report) | https://www.nptrust.org/fy25-ar-consolidated-financials-npt/ | FY2025 |
| S25 | AEF about page and 2023 Form 990 | https://www.aefonline.org/about-aef/ ; https://www.aefonline.org/wp-content/uploads/2025/01/2023-AEF-990-Public-Disclosure.pdf | 990 for 2023 |
| S26 | MS GIFT 2024 Impact Report | https://www.morganstanley.com/content/dam/msdotcom/what-we-do/wealth-management/gift/ms-gift-impact-report.pdf | 2024 |
| S27 | DAFgiving360 financials page (403) | https://www.dafgiving360.org/about-dafgiving360/financials | attempted 2026-11-14 |
| S28 | ProPublica Nonprofit Explorer API (filing index, total assets) | https://projects.propublica.org/nonprofits/api/v2/organizations/{EIN}.json | accessed 2026-11-14 |

---

## 7. Data dictionary

**`agentic-control-gap-matrix.csv`** (one row per operator × control dimension)

| Column | Definition |
|---|---|
| row_id | `AGM-NN` |
| operator | Daffy; TIFIN Give / GiveClear; Endaoment; Chariot |
| agent_or_third_party_path | The interface through which an agent or third party can start a donation |
| control_dimension | One of: authorization_model, credential_scoping, per_transaction_limits, confirmation, sponsor_approval, authority_separation_flag_rule, liability_allocation, revocation, audit_logging, agent_identification |
| repo_benchmark | What the repo's governance model requires (`ai-governance-failure-modes.md` §4.5 and §5) |
| documented_control | What the operator's documentation says, or "not publicly documented" |
| enforcement_locus | server / client-side / agent instruction / sponsor (post-submission) / contract / none / not publicly documented |
| contract_or_policy_clause | Verbatim clause (≤40 words) from the public contract or policy, or "none" |
| doc_source_url, contract_source_url | Sources; snapshot paths given where the repo holds one |
| gap_rating | meets / partial / gap / unknown (defined in §2) |
| gap_note | Analyst reading (inference) |
| confidence | high / medium / low |

**`sponsor-audit-notes.csv`** (one row per sponsor)

| Column | Definition |
|---|---|
| sponsor, legal_entity | Brand and reporting entity |
| fiscal_year_end | Period of the most recent document found |
| document_status | read / summary_only / on_request (not posted) / not_public / not_retrieved |
| document_url | Where the document or the request route was found |
| auditor, auditor_evidence | Firm, and how it was identified (letterhead, signature image, 990) |
| opinion_type, report_date | As stated in the auditor's report |
| other_auditor_reliance | Components audited by other firms |
| related_party_administration_note | Note text on affiliated administrators or fees (verbatim fragments ≤40 words) |
| technology_service_agreements | Platform or service agreements disclosed |
| concentration_note | Concentration disclosures |
| going_concern | Whether a going-concern paragraph or emphasis exists ("none" = standard responsibility language only) |
| soc_report_reference | Any SOC 1/2/3 or service-organization reference in the statements |
| total_assets_usd | From the statements, or labeled as Form 990 / ProPublica figures |
| form990_audit_indicator | Form 990 Part XII answers where read |
| notes, retrieved_date, confidence | Caveats; retrieval date; high/medium/low |

**`queue-proposals-agentic-audits.csv`** follows `data/mission-2026-11-14/queue-proposals-README.md`, using prefix `P-AGA-`.
