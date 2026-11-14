# AI governance, trust and failure modes in DAF operations

> **Red-team status (2026-11-14):** this document was independently reviewed in [red-team-wave2a-ai-and-entrant.md](red-team-wave2a-ai-and-entrant.md). The corrections in the final section govern where they conflict with the text.


**Date:** 2026-11-14. **Status:** desk research; regulatory text and public market evidence; no access to any sponsor's AI systems, model-risk documentation or incident data. **Data:** `data/mission-2026-11-14/ai-failure-mode-register.csv` (16 failure modes). **Companion:** `research/mission-2026-11-14/ai-economics-replacement-analysis.md` (process IDs P01–P16 used below). **Builds on:** decision state machine and adversarial cases in `research/batch-2c-grant-approval-decision-system-benchmark-2026-11-12.md`; failure mechanisms in `research/batch-2a-charity-vetting-grant-approval-2026-11-12.md`; responsibility map in `research/technology-control-map.md`.

Notation: **[F]** sourced fact; **[I]** inference; **[S]** scenario/judgment rating.

---

## 1. Executive findings

1. **The legal design of a DAF makes "AI approval" a category error.** [F] Penalties attach to the *sponsor* and to *fund managers who agree* to a distribution: 20% of a taxable distribution on the sponsor and 5% (capped at $10,000) on a knowing manager under IRC 4966; 125% of a prohibited benefit on the donor/advisor and 10% on a knowing manager under 4967; grants, loans and compensation to donors/advisors are automatic excess benefit transactions under 4958(c)(2) ([4966](https://www.law.cornell.edu/uscode/text/26/4966); [4967](https://www.law.cornell.edu/uscode/text/26/4967); [4958](https://www.law.cornell.edu/uscode/text/26/4958)). [I] Liability is framed around an accountable person agreeing with knowledge. A probabilistic system can inform that agreement; it cannot be the one who agrees. Governance should therefore be designed around **who signs**, with AI confined to producing evidence for the signer.

2. **AI mostly *creates* new risk in DAF operations unless it is restricted to additive roles.** [S] Of 16 failure modes in the register, AI in its unconstrained form creates risk in 13 and redistributes it in 3; it reduces risk only where it is permitted to *add* flags or evidence and never to remove them (F04 under that constraint). The asymmetric rule — **AI may add a flag, never clear one** — converts the most dangerous failure (missed sanctions hit or prohibited benefit) from "created" to "reduced". (Register: `data/mission-2026-11-14/ai-failure-mode-register.csv`.)

3. **The live agentic risk is upstream of the sponsor, not inside it.** [F] TIFIN Give's Louise is described as executing donor requests such as recurring grants and stock contributions, with no guardrails stated ([PR Newswire, 2025-10-27](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html)); Daffy's MCP server exposes `make_donation` ("moves real money") to external AI assistants with no documented per-donation limit ([Daffy docs](https://docs.daffy.org/agents/mcp)). [I] Sponsors will receive agent-originated recommendations before they deploy agents themselves. The control that matters is the **separation of a donor (or agent) recommendation from sponsor approval and from payment**, each with its own identity, timestamp and limits.

4. **Regulation is thin and moving; voluntary frameworks carry the load.** [F] Final DAF regulations have not been issued: proposed rules were published 2023-11-14 ([88 FR 77922](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)), and the 2026–2027 Priority Guidance Plan (released 2026-09-29) reframes the project as guidance under sections 4966 and 6033 for "certain" DAF arrangements rather than final 4966 regulations (secondary summary: [EY Tax News](https://taxnews.ey.com/news/2026-2213-2026-2027-priority-guidance-plan-includes-multiple-projects-affecting-tax-exempt-organizations)). The SEC withdrew its predictive-data-analytics conflicts proposal on 2025-06-12 ([Alston & Bird](https://www.alston.com/en/insights/publications/2025/06/sec-withdraws-multiple-rule-proposals)). FINRA's rules are technology-neutral ([RN 24-09, 2024-06-27](https://www.finra.org/rules-guidance/notices/24-09)) and its 2026 report is the first to address AI agents ([Debevoise summary, 2025-12-12](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued)). NIST AI RMF 1.0 ([NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1)) and the Generative AI Profile ([NIST AI 600-1, July 2024](https://doi.org/10.6028/NIST.AI.600-1)) are voluntary. [I] DAF sponsors cannot wait for an AI rule; their binding obligations are the existing excise-tax, sanctions, substantiation and privacy regimes.

5. **Trust risk is concentrated where AI talks to donors.** [F] A tribunal held Air Canada liable for its chatbot's misstatement ([Moffatt v. Air Canada, 2024 BCCRT 149, ABA summary](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)); commercial legal AI tools hallucinated on 17–33% of benchmark queries ([Magesh et al., 2024](https://arxiv.org/abs/2405.20362)); in a donor survey summarized on Fidelity Charitable's site, 93% rated transparency about AI use important and 39.8% were uneasy about data use ([Fidelity Charitable, survey Aug 2024](https://www.fidelitycharitable.org/articles/donor-perceptions-of-ai.html)). [I] A sponsor chatbot answering deductibility, QCD or 2026 tax-law questions is the single highest trust-risk AI use case; it is also among the most tempting economically (P11).

---

## 2. Regulatory and standards baseline

| Source | What it says (fact) | Relevance to AI | Status / uncertainty |
|---|---|---|---|
| Pension Protection Act of 2006, Pub. L. 109-280 ([Congress.gov](https://www.congress.gov/bill/109th-congress/house-bill/4)) | Created statutory DAF definitions and excise taxes (4966, 4967), extended 4958 and 4943 to DAFs, added 170(f)(18) acknowledgment of sponsor control | Fixes the legal accountability model AI must fit | In force |
| IRC 4966 ([26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966)) | 20% on sponsor; 5% on knowing manager (cap $10k); taxable if to a natural person, for non-170(c)(2)(B) purpose, or to non-public-charity without expenditure responsibility; disqualified supporting organizations (4966(d)(4)) | Eligibility (P06), non-standard DD (P07) | In force |
| IRC 4967 ([26 USC 4967](https://www.law.cornell.edu/uscode/text/26/4967)) | 125% of benefit on donor/advisor/related person; 10% on knowing manager (cap $10k) | Prohibited-benefit review (P08) | In force |
| IRC 4958(c)(2) | Grants, loans, compensation from a DAF to donors/advisors are automatic excess benefit transactions | P08 | In force |
| IRC 170(f)(18) ([26 USC 170](https://www.law.cornell.edu/uscode/text/26/170)) | Deduction requires the sponsor's written acknowledgment that it has exclusive legal control of contributed assets | Agentic flows must not blur sponsor control | In force |
| Proposed DAF regulations ([88 FR 77922, 2023-11-14](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm)) | Proposed definitions of donor, advisor, DAF; taxable distributions | Would change who counts as a "donor advisor" (relevant to agents acting for donors) | Not finalized; 2026–27 PGP reframes project (secondary source); timing unknown |
| OFAC Framework for Compliance Commitments ([OFAC, 2019-05-02](https://ofac.treasury.gov/media/16331/download)) | Risk-based program: management commitment, risk assessment, internal controls, testing/audit, training | Screening automation must be testable and tuned | Guidance, not rule |
| NIST AI RMF 1.0 and AI 600-1 | Govern/Map/Measure/Manage functions; GenAI risks incl. confabulation, data privacy, information security, human-AI configuration | Usable as sponsor AI control baseline | Voluntary; the executive order that commissioned AI 600-1 was revoked (reported by secondary sources, not verified here) |
| FINRA RN 24-09; 2026 Oversight Report | Rules apply to GenAI as to any tool; agents flagged for autonomy without human validation, exceeding authority, sensitive-data misuse, auditability | Applies to broker-dealer affiliates that distribute DAFs, not to sponsors as such [I] | Guidance; no new obligations |
| SEC PDA proposal withdrawal ([Alston & Bird, 2025-06](https://www.alston.com/en/insights/publications/2025/06/sec-withdraws-multiple-rule-proposals)) | Adviser AI-conflicts rule withdrawn 2025-06-12 | Adviser-facing charity/DAF recommendation tools face no AI-specific SEC rule; fiduciary duty remains [I] | Withdrawn |
| Oregon Consumer Privacy Act ([Oregon DOJ FAQ](https://www.doj.state.or.us/consumer-protection/for-businesses/privacy-law-faqs-for-nonprofits/)) | Applies to nonprofits meeting thresholds from 2025-07-01 | Donor data in AI pipelines at nonprofit sponsors | In force; threshold applicability per sponsor unknown |
| Colorado Privacy Act / Colorado AI Act (SB 24-205) ([GT Law, 2025-09](https://www.gtlaw.com/en/insights/2025/9/colorado-delays-comprehensive-ai-law-with-further-changes-anticipated)) | Colorado privacy law reported to cover nonprofits; AI Act effective date delayed to 2026-06-30 | "Consequential decision" coverage of charitable-grant decisions unclear | **Uncertain:** whether the 2026-06-30 date held was not verified in this pass |

**Key gap [I]:** whether a standalone DAF sponsor (not a bank or broker-dealer) is subject to BSA/AML program requirements was not established; OFAC obligations apply regardless.

---

## 3. Failure modes

Ratings are qualitative judgments [S]; mechanisms and evidence are in the CSV.

| ID | Failure mode | AI effect | Why |
|---|---|---|---|
| F01 | Incorrect eligibility (false approve) | **Creates** if AI replaces lookup; none if lookup stays deterministic | Monthly IRS/OFAC data is authoritative and machine-readable; an LLM paraphrase adds error without information |
| F02 | False decline/hold | **Redistributes** | Fewer manual misses, new model false positives; Benevity shows decline rates are material and movable (vendor-reported 30%→<3%; [Benevity, 2026-06-04](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026)) |
| F03 | False fraud/sanctions alerts | **Redistributes** | Triage faster; new class of triage errors |
| F04 | Missed sanctions hit / prohibited benefit | **Creates** if AI may clear; **reduces** if AI may only add | Asymmetric-permission rule decides the sign |
| F05 | Hallucinated legal/tax advice to donors | **Creates** | Moffatt liability ([ABA summary](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/)); 17–33% legal hallucination even with RAG ([Magesh et al., 2024](https://arxiv.org/abs/2405.20362)) |
| F06 | Unauthorized/erroneous agent grant action | **Creates** | Irreversible once paid; write tools already exposed (Daffy) |
| F07 | Model drift | **Creates** | Same model service changed materially within months ([Chen, Zaharia, Zou 2023](https://arxiv.org/abs/2307.09009)) |
| F08 | Biased/steered charity recommendations | **Creates** | Ranking from history, location, family activity (Louise) can concentrate giving; opaque |
| F09 | Sensitive donor data exposure | **Creates** | New processors, connectors and retention |
| F10 | Inadequate audit trail | **Creates** unless designed in | Multi-step agent chains hard to reconstruct (FINRA) |
| F11 | Unexplained approvals | **Creates** | Fluent rationales not tied to evidence |
| F12 | Automation bias / oversight failure | **Creates** | Systematic over-reliance on automated aids ([Goddard et al., JAMIA 2012](https://doi.org/10.1136/amiajnl-2011-000089)) |
| F13 | Third-party model dependency/provider change | **Creates** | Retirement with ≥60 days' notice; e.g., two models retired 2026-06-15 ([Anthropic deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)) |
| F14 | Vendor lock-in of decision history | **Redistributes** | Exists today for rules engines; AI adds prompts/model versions to what must be exported |
| F15 | Prompt injection via charity/donor data | **Creates** | Indirect prompt injection in retrieved content ([Greshake et al. 2023](https://arxiv.org/abs/2302.12173)); OWASP LLM01/LLM06 ([OWASP](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html)) |
| F16 | Agent credential compromise | **Creates** | Daffy: an API key "can move money in your fund" |

**Counts [S]:** in unconstrained form, creates 13 (F01, F04–F13, F15, F16) and redistributes 3 (F02, F03, F14). Under the constrained designs in Section 4, F01 becomes risk-neutral (AI kept off the lookup) and F04 becomes risk-reducing (add-only rule). Read this as "AI is a new risk source to be engineered down," not as "AI is net harmful": the economics document shows several places where it is worth that engineering.

### 3.1 DAF-specific mechanisms worth emphasizing

- **Prompt injection through charity data (F15).** [I] Charity websites, mission statements, determination letters, foreign grantee bylaws, grant purpose fields and remittance memos are all attacker-writable text. Any AI step that both reads such text and can call tools (change a status, send an email, initiate a payment) is exposed. Batch 2C already includes "prompt injection in charity web text" as an adversarial case; this register makes it a design constraint: **document-reading steps get no tools; tool-using steps get no untrusted text.**
- **Recommendation steering (F08).** [I] DAF sponsors and their technology vendors earn fees on assets, not on which charity is chosen, which limits direct steering incentives; but recommenders trained on giving history and partner data can still concentrate grants toward large, digitally visible charities. Louise ranks by past giving, family activity, location and mission statements (vendor description). No sponsor discloses recommender ranking factors.
- **Agent as advisor (F06).** [I] Under 4966(d)(2) a DAF is defined by a donor's (or appointee's) advisory privileges. An AI agent acting on a donor's OAuth token is exercising those privileges; the proposed regulations' definitions of donor and advisor were written before agentic access existed. Whether an agent operated by a third-party platform could ever be a "person appointed by a donor" is an open legal question, not addressed in any source found.
- **Stale evidence (F01, F07, F13).** Eligibility depends on dated data (monthly IRS files, [IRS bulk data](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)), dated policy (e.g., RCF's March 2023 policy, [RCF policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)) and now dated models. Each decision record must carry all three versions.

---

## 4. Control split for high-impact use cases

For each, the split names what must be **deterministic** (rules, lookups, limits), what **probabilistic AI** may do, and what an **authorized human** must decide. "Net effect" is the analytical judgment of whether AI, so constrained, reduces, redistributes or creates risk.

### 4.1 Routine charity eligibility (P06)
- **Deterministic:** EIN-keyed lookup against IRS bulk data (Pub 78 data, EO BMF, Auto-Revocation List; monthly per [IRS](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads)) and the OFAC list; 4966(d)(4) supporting-organization classification from structured fields; snapshot ID stored with the decision.
- **Probabilistic AI:** none on the decision path. Optional: name/EIN disambiguation suggestions at donor intake, shown to the donor for confirmation.
- **Human:** exceptions only (not found, conflicting, church/government unit lacking IRS listing — RCF policy accepts supplemental documentation for these).
- **Net effect:** AI on the decision path **creates** risk (F01) with no benefit. Correct design is **D** (continuous status subscription), per the economics document.

### 4.2 Non-standard grantee due diligence (P07)
- **Deterministic:** risk-tier routing (foreign, fiscal sponsor, 509(a)(3), non-listed domestic); required-document checklist by tier; amount thresholds (e.g., RCF's 2023 officer review above $500k, [RCF policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf)); expenditure-responsibility workflow steps under 4945(h) ([26 USC 4945](https://www.law.cornell.edu/uscode/text/26/4945)).
- **Probabilistic AI:** extract fields from documents (bylaws, financials, equivalency determinations) into a schema; highlight missing items; draft a cited summary where every claim links to a document span. Runs sandboxed without tools (F15).
- **Human:** legal determination (equivalency, ER sufficiency, disqualified-supporting-org conclusion); sign-off recorded with identity, policy version and evidence snapshot.
- **Net effect:** **redistributes** — reviewer reading time falls; new extraction-error and automation-bias risks need seeded-case QA. Analogue: McGovern's Grant Guardian keeps a human in the loop "at key steps" ([McGovern](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/)).

### 4.3 Prohibited-benefit / excess-benefit review (P08)
- **Deterministic:** structured donor attestation at intake (no tickets, dues, tuition, pledge-satisfaction terms per sponsor policy, no benefit to donor/advisor/family); keyword and category rules; recipient–donor relationship checks where data exist.
- **Probabilistic AI:** read free-text purpose and linked event pages and **add** a flag with a reason; never remove one.
- **Human:** every flagged case; every decline.
- **Net effect:** **reduces** risk under the add-only rule (catches benefit language rules miss) at the cost of more holds (F02). If AI is allowed to clear rule-based flags, it **creates** the highest-severity failure (F04).

### 4.4 Sanctions/fraud alert handling (P14)
- **Deterministic:** list screening with documented match thresholds; secondary identifiers; tuning tested per the OFAC Framework's testing/audit component.
- **Probabilistic AI:** assemble an evidence packet and narrative for the analyst; rank alerts by likely materiality.
- **Human:** disposition of every list-match alert; no auto-clear.
- **Net effect:** **redistributes**; ranking can bury true positives if not tested with seeded hits.

### 4.5 Agent-originated grant recommendations (donor side; P05/P09)
- **Deterministic:** distinct states — *agent draft → donor confirmation → sponsor approval → payment instruction → settlement*; per-agent spend and recipient limits; cancel window before payout; token scopes and revocation; agent identity recorded on the recommendation; no payment-instruction changes via agent channel.
- **Probabilistic AI:** parse the donor's request into a structured draft.
- **Human:** donor confirms each draft (or explicit standing instruction with limits); sponsor approval remains the legal decision.
- **Net effect:** **creates** risk relative to today (F06, F15, F16) in exchange for convenience. Mitigated to acceptable only if limits and state separation are enforced by the sponsor's platform, not by the external assistant. Daffy's documentation shows OAuth, revocation and activity visibility but no limits; TIFIN's release states none.

### 4.6 Donor/advisor service assistant (P11)
- **Deterministic:** account data retrieved via authenticated APIs (balances, grant status) and displayed verbatim; refusal templates for individualized tax/legal advice; human handoff.
- **Probabilistic AI:** retrieve-and-cite from an approved, versioned knowledge base; draft agent-assist responses for staff.
- **Human:** anything involving tax treatment of a specific gift, exceptions, complaints, bereavement.
- **Net effect:** **creates** (F05, F09) if customer-facing generative answers are allowed on tax topics; **reduces** handling time with limited risk as staff-facing agent-assist. Fidelity Charitable's current assistant is navigation-only, asks users not to enter personal information and disclaims accuracy ([terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html)) — a conservative pattern consistent with this analysis.

### 4.7 Complex-asset intake (P03)
- **Deterministic:** acceptance checklist (appraisal requirements per Form 8283, transfer restrictions, 4943 holdings tests, liquidity plan); dollar thresholds for committee review.
- **Probabilistic AI:** read operating agreements, cap tables, appraisals; extract restrictions and conflicts into a schema; draft a cited memo.
- **Human:** acceptance decision; valuation reliance; donor conversation.
- **Net effect:** **redistributes**; extraction errors on transfer restrictions could be material, so QA must be heavier than in P07.

### 4.8 Reconciliation and nonprofit-side attribution (P10/P16)
- **Deterministic:** structured remittance identifiers where they exist; exact-match first.
- **Probabilistic AI:** propose matches for unstructured remittances with confidence; code campaign/fund (Chariot's deployed pattern).
- **Human:** confirm low-confidence matches; anything affecting donor acknowledgment or anonymity.
- **Net effect:** **reduces** labor with modest risk (errors are correctable bookkeeping, except misattributed acknowledgments that break donor anonymity — F09).

---

## 5. Minimum governance operating model for a DAF sponsor using AI

Derived from NIST AI RMF functions and FINRA's agent observations, adapted to DAF law [I]:

1. **Inventory and tiering (Govern/Map).** Register every AI use with process ID, decision proximity (inform / recommend / act), data categories and model/provider. Prohibit AI on the decision path for P06 and on clearance in P08/P14.
2. **Decision record standard (Manage).** For every grant decision touched by AI: inputs, source snapshot IDs (IRS file date, OFAC list date), policy version, model ID and version, prompt/template version, AI output, human reviewer identity and action. Export in an open schema (F10, F14).
3. **Asymmetric permissions.** AI may add flags and evidence; only humans or deterministic rules may remove flags or approve.
4. **Evaluation before deployment and on every model change (Measure).** Labeled regression set drawn from the 20 synthetic cases in Batch 2C plus adversarial injection cases; pinned model versions; acceptance thresholds set by compliance (F07, F13).
5. **Oversight that measures itself (F12).** Seeded known-bad cases in live queues; track reviewer override rates (near-zero override is a warning sign, not success).
6. **Agent controls (F06, F16).** Scoped tokens, per-agent limits, mandatory donor confirmation, cancel window, agent identity on every recommendation; sponsor platform enforces all of these.
7. **Untrusted-content isolation (F15).** Separate extraction (no tools) from action (no untrusted text); validate outputs against schemas.
8. **Data minimization and contracts (F09).** No-training and retention terms with model providers; field-level redaction; privacy review under applicable state laws.
9. **Donor transparency.** Disclose where AI is used in donor-facing flows and how recommendations are ranked (responds to the 93% transparency finding, [Fidelity Charitable](https://www.fidelitycharitable.org/articles/donor-perceptions-of-ai.html)).
10. **Exit plan (F13, F14).** Manual fallback path and tested migration to an alternative model within the provider's notice window (≥60 days for Anthropic per its deprecation page).

**Vendor due-diligence questions** (add to `research/vendor-access-request-2026.md` scope): Does any AI component change a grant's state? Which model/provider and version, and how are changes evaluated? Is there an add-only constraint on screening? Are agent-originated recommendations labeled and limited? Can decision records including AI outputs be exported? Is customer data used for training? What happens on model retirement?

---

## 6. Does AI reduce, redistribute or create risk overall?

[I] For DAF sponsors in late 2026:
- **Reduces:** where AI adds detection to a rules baseline (benefit language, alert evidence packets) or does correctable bookkeeping (attribution/reconciliation).
- **Redistributes:** where AI speeds document review in judgment-heavy work (P03, P07, P13) — labor shifts from reading to verifying, and risk shifts from omission to automation bias.
- **Creates:** where AI touches status determination, donor-facing tax answers, or payment-capable actions. These include the market's most visible AI claims (agentic donor assistants).

The governance burden is therefore lowest exactly where the economics document finds the best non-AI alternatives (redesign), and highest where AI's economic case is strongest (unstructured, high-judgment work). That tension, not model capability, is the binding constraint on AI replacement in DAF operations.

---

## 7. Open questions

1. Will forthcoming 4966/6033 guidance define "donor advisor" in a way that reaches software agents or platforms acting under donor credentials?
2. Did Colorado's AI Act take effect on 2026-06-30, and would a sponsor's grant decline count as a "consequential decision"? (Not verified; delay to 2026-06-30 reported by [GT Law, 2025-09](https://www.gtlaw.com/en/insights/2025/9/colorado-delays-comprehensive-ai-law-with-further-changes-anticipated).)
3. Are any standalone DAF sponsors subject to BSA/AML program rules, which would bring model-risk expectations for monitoring systems?
4. What limits, confirmations and audit records do TIFIN (Louise) and Daffy (MCP) actually enforce? Requires demos or test accounts.
5. Has any sponsor experienced an AI-related incident (misstatement, injection, data exposure)? None found in public sources.

---

## Sources (accessed 2026-11-14 unless noted)

Statute and rules: [Pub. L. 109-280 (PPA 2006)](https://www.congress.gov/bill/109th-congress/house-bill/4); [26 USC 170](https://www.law.cornell.edu/uscode/text/26/170); [26 USC 4958](https://www.law.cornell.edu/uscode/text/26/4958); [26 USC 4966](https://www.law.cornell.edu/uscode/text/26/4966); [26 USC 4967](https://www.law.cornell.edu/uscode/text/26/4967); [Proposed DAF regs, 88 FR 77922](https://www.govinfo.gov/content/pkg/FR-2023-11-14/html/2023-24982.htm); [EY on 2026–27 PGP](https://taxnews.ey.com/news/2026-2213-2026-2027-priority-guidance-plan-includes-multiple-projects-affecting-tax-exempt-organizations); [IRS bulk data](https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads); [OFAC Framework](https://ofac.treasury.gov/media/16331/download).
AI governance: [NIST AI 100-1](https://doi.org/10.6028/NIST.AI.100-1); [NIST AI 600-1](https://doi.org/10.6028/NIST.AI.600-1); [FINRA RN 24-09](https://www.finra.org/rules-guidance/notices/24-09); [Debevoise on FINRA 2026 report](https://www.debevoise.com/insights/publications/2025/12/finras-2026-regulatory-oversight-report-continued); [Alston & Bird on SEC withdrawals](https://www.alston.com/en/insights/publications/2025/06/sec-withdraws-multiple-rule-proposals); [Oregon DOJ nonprofit privacy FAQ](https://www.doj.state.or.us/consumer-protection/for-businesses/privacy-law-faqs-for-nonprofits/); [GT Law on Colorado AI Act delay](https://www.gtlaw.com/en/insights/2025/9/colorado-delays-comprehensive-ai-law-with-further-changes-anticipated); [OWASP LLM06](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html).
Failure evidence: [Moffatt v. Air Canada (ABA)](https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/); [Magesh et al. 2024](https://arxiv.org/abs/2405.20362); [Chen, Zaharia, Zou 2023](https://arxiv.org/abs/2307.09009); [Greshake et al. 2023](https://arxiv.org/abs/2302.12173); [Goddard et al. 2012](https://doi.org/10.1136/amiajnl-2011-000089); [Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations).
Market: [TIFIN Louise](https://www.prnewswire.com/news-releases/tifin-give-launches-louise-ai-capabilities-for-philanthropy-302595069.html); [Daffy MCP docs](https://docs.daffy.org/agents/mcp); [Fidelity Charitable donor perceptions](https://www.fidelitycharitable.org/articles/donor-perceptions-of-ai.html); [Fidelity virtual assistant terms](https://www.fidelitycharitable.org/legal/virtual-assistant.html); [Benevity Live 2026](https://benevity.com/press-releases/ai-native-csr-platform-benevity-live-2026); [McGovern Grant Guardian](https://www.mcgovern.org/how-foundations-are-using-ai-to-vet-grantees/); [RCF Due Diligence Policy](https://renaissancecharitable.org/wp-content/uploads/2026/02/Grantmaking-Due-Diligence-Policy.pdf).

---

## Data dictionary

### `data/mission-2026-11-14/ai-failure-mode-register.csv` (one row per failure mode)

| Column | Meaning |
|---|---|
| fm_id, failure_mode | Identifier and name |
| affected_processes | Process IDs from `ai-process-economics.csv` |
| mechanism | How the failure arises |
| evidence_or_analogue, evidence_url | Public evidence or closest analogue (not necessarily DAF-specific) |
| regulatory_hook, regulatory_url | Main legal/standards hook |
| likelihood_scenario, impact, detectability | Qualitative judgments [S] |
| ai_effect_on_risk | creates / redistributes / reduces (with condition where relevant) |
| deterministic_controls | Rules, limits, lookups that must not be probabilistic |
| permitted_ai_role | What AI may do |
| human_decision_required | What an authorized person must decide |
| monitoring_metric | Metric that would reveal the failure |
| risk_owner | Suggested accountable function |

## Red-team corrections (wave 2A, 2026-11-14) — governing

17. **`ai-governance-failure-modes.md`, Exec #2.** Add:
    > "These counts are rubric ratings against unconstrained AI, with no observed DAF AI incidents and no baseline for human error rates."
