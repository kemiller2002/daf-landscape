# Validation of the four provisional GREEN AI overlays (P-B43N25-01)

**Date:** 2026-11-20. Task ID b43n25-01. This is a second reader's independent re-rating of the four rows the census marked GREEN (provisional) in [direction-ai-product-census.md](direction-ai-product-census.md) and [`philanthropy-ai-products-2026.csv`](../../data/mission-2026-11-14/philanthropy-ai-products-2026.csv): AIP12, AIP13, AIP16 and AIP28. Nothing was committed or pushed, and no existing file was edited. Proposed changes to existing files are in [Exact corrections](#exact-corrections).

**Data:** [`green-overlay-validation-2026-11-20.csv`](../../data/mission-2026-11-14/green-overlay-validation-2026-11-20.csv) has 48 rows: 4 products × 12 rows (11 criteria plus an overall verdict). **Queue proposals:** [`queue-proposals-b43n25-01.csv`](../../data/mission-2026-11-14/queue-proposals-b43n25-01.csv) (5 rows).

## 1. Results in brief

| ID | Product | Census overlay | Re-rated overlay | Why |
|---|---|---|---|---|
| AIP12 | SmartSimple AI Application Analysis | GREEN (provisional) | **GREEN (provisional), confirmed** | First-party help states the full set of controls: flag and score outputs only, results are "not as final determinations", no external AI services, no training, model named, enabled by the vendor, and fields chosen by the admin. |
| AIP13 | Fluxx Finn | GREEN (provisional) | **GREEN (provisional), confirmed (weakest evidence)** | Off by default and "every decision stays with your team". The only evidence is a marketing page with an FAQ. The Fluxx MCP is bundled with Finn and stays AMBER (AIP14). |
| AIP16 | YourCause / Blackbaud Grantmaking AI Application Summaries and Form Intelligence | GREEN (provisional) | **GREEN (provisional), confirmed, with an opt-in correction** | Summaries "do not add new information", and the decision stays "with the grants team". The default is **not** simply off: organisations that used generative AI before 2026-01-07 "remain enabled", and opting in also opens external-connector access. GrantsConnect summaries still need Blackbaud to enable them (“Contact your Account Manager or CSM to enable it”), so grandfathering does not by itself switch them on [V wave 42A] |
| AIP28 | Givebutter Magic | GREEN (provisional); wave 28 called it a GREEN/AMBER boundary case | **AMBER (downgrade)** | Givebutter's AI Addendum (effective 2026-10-01) says "AI Features are enabled by default". It says AI-assisted fraud detection and Receipt Matching "cannot be disabled", and that observability-log data "may be used for AI model training". Stretch goals and suggested amounts change automatically. AI transaction review has undocumented limits. Only the flag-only failure and the undocumented review limits are binding under §7; the default-on and cannot-disable terms are supplementary (S2, S5) [V wave 42A] |

- **Census overlay counts after the change:** GREEN (provisional) 4 → **3**; AMBER 9 → **10**. RED stays 0.
- **First GREEN under §7 (§3 below): no.** None of the four products is a provider in areas A1–A5, where the overlay is reported. GREEN had also been used before: the v1.0 calibration gave GREEN to Fidelity Charitable and "GREEN / none" to Ren, RDE, RCF and AEF, and the v1.1 consensus overturned both. The v1.1 finding that no provider earns GREEN therefore stands. The accurate wording is "the first GREEN-eligible vendor AI products in the census".
- **Foundant overlay (§4 below): unchanged, AMBER.** One new fact changes the reasoning but not the result. SmartSimple's own FAQ says the Application Analysis service takes data "from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)". So the link to Foundant is first-party, not just shared ownership. The overlay stays AMBER because Fia's controls are still undocumented, and no source ties the feature to any sponsor's DAF program.

## 2. Method

1. **Locating the census and the rules.** Searched `research/` and `data/` for "AI product census", "GREEN", "methodology §7" and "AIP0". Read:
   - the census doc and CSV;
   - [evidence-quadrant-methodology.md](evidence-quadrant-methodology.md) §1 (areas, overlay rule), §3 (admissibility), §7 (entity scope rule, AI overlay vocabulary) and §8 (recency);
   - the wave 28 validation report and register rows V28-26 to V28-30;
   - the v1.0 overlay table in [quadrant-calibration.md](quadrant-calibration.md) and the v1.1 overlay adjudication in [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md) §6.
2. **Criteria exactly as the methodology states them.**
   - §7 has one sentence for GREEN: "controls documented, including flag-only and authority separation."
   - §1 states the overlay rule: "AI may add a flag, never clear one."
   - §7 defines AMBER as "capability live with undocumented limits, but sponsor approval remains". It defines RED as "AI can complete a money-moving or status-clearing action without documented sponsor or human approval."
   - The binding criteria are therefore G1 (controls documented), G2 (flag-only), G3 (authority separation), R1 (the RED test is not met) and SC (area and entity scope).
   - The brief also names human review, no automated decision, data handling and model disclosure, and opt-in. **None of these appears in §7.** They are rated as supplementary criteria S1–S5 and do not decide the overlay.
   - S6 (audit trail) comes from the Y3 rubric in §2, not from the overlay.
   - A row is GREEN if G1–G3 are met and R1 holds. It is AMBER if a live capability has limits that are undocumented or not flag-only, while human approval of outputs remains. It is RED if R1 fails.
3. **Sources.** Only first-party pages dated 2025–2026 were used: help articles, FAQs, terms, privacy policies and product pages carrying FAQs.
   - Each page was fetched with a generic user agent (`research-script/1.0`) by a stdlib script. Stripped text was saved to the scratchpad.
   - Every quote in the CSV was checked by script against the saved text. 47 of 48 matched verbatim. The exception is AIP13 S6, which records an absence.
   - Two quotes needed normalising for extraction artefacts: Blackbaud's help renders "organization" with a span inside the word, and the Givebutter docs have Markdown `>` line prefixes.
4. **Search.** Web search was used only to discover first-party URLs: the Givebutter AI Addendum, the Blackbaud GrantsConnect help files and blackbaud.com/ai.

### robots.txt log (checked 2026-11-20 before any fetch)

| Host | Status | Result |
|---|---|---|
| supporthub.smartsimple.com | 200 | `*` disallows account, search and request paths only; `/hc/en-us/articles/` allowed |
| www.smartsimple.com | 200 | HubSpot preview paths only; not fetched (not needed) |
| fluxx.io / www.fluxx.io | 302 → 200 | ClaudeBot and anthropic-ai: `Allow: /` (preview paths excluded) |
| help.fluxx.io | no response (DNS/connection) | not fetched; no Fluxx help centre found |
| www.yourcause.com | 200 | only `/wp-content/uploads/*.pdf` disallowed |
| webfiles-sc1.blackbaud.com | 404 | no rules (repo convention: fetchable) |
| www.blackbaud.com | 200 | only `/wp-content/uploads/*.pdf` disallowed |
| givebutter.com | 200 | `Disallow:` (empty), so everything is allowed |
| help.givebutter.com | 200 | not-authorized and not-found paths only; Crawl-delay 1 respected |
| docs.givebutter.com | 200 | `/cdn-cgi/` and `/_next/` only |
| www.financialcontent.com | 404 | no rules; used only to re-check the Foundant Fia release as context for §4 |
| www.foundant.com | not re-checked | barred to ClaudeBot and anthropic-ai per the census (2026-11-15); not fetched |

## 3. Per-product, per-criterion ratings

Ratings: met, partly, not met, not documented. All pages were accessed on 2026-11-20. "Undated" means the page shows no date; each such page was current at access and mentions 2026 features.

### 3.1 AIP12 SmartSimple AI Application Analysis: GREEN (provisional), confirmed

| Criterion | Rating | Quote | URL | Date |
|---|---|---|---|---|
| G1 Controls documented (§7) | met | "AI Application Analysis is designed to supplement human review." (section "Privacy, Data, and Design Details") | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| G2 Flag-only (§1, §7) | met | "Flag - The AI evaluates the application and flags items of note that may be worth a reviewer's attention, but are not given a numeric score." Scoring (1–10) and Yes/No criteria also exist, and the score can sort list views. No gating or status change is documented. | [Configure](https://supporthub.smartsimple.com/hc/en-us/articles/40249784423831-Configure-AI-Application-Analysis) | 2026-07-07 |
| G3 Authority separation (§7) | met | "All analysis results should be treated as inputs to reviewer judgment and not as final determinations." The FAQ adds that the service "is not accessed directly by the client user or their browser". | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| R1 Not RED (§7) | met | "the analysis runs automatically when the grant reaches the designated status". Status triggers the analysis, and nothing says the AI changes status. There is no money path. | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| S1 Human review | met | "Reviewer training on interpreting and applying AI-generated insights supports responsible use of this feature." | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| S2 No automated decision | met | "not as final determinations" | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| S3 Data handling / training | met | "runs within SmartSimple's own environment and does not send grant application data to external AI services. Grant application data is processed internally and is never used to train AI models." The FAQ says models are "specifically defined not to be used for LLM training purposes". This covers this feature only: the release notes describe other "AI expressions using newer Azure OpenAI models". | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview); [Release notes](https://supporthub.smartsimple.com/hc/en-us/articles/40168112536343-June-2026-Release-Notes) | 2026-06-22; 2026-11-02 |
| S4 Model disclosure | met | "Amazon Nova Pro is the AI model used for analysis." | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| S5 Opt-in | met | "SmartSimple must enable the feature for your organization before it can be configured." It is a paid add-on, and the admin picks the fields and roles. | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| S6 Audit trail (Y3) | partly | "Click View Details to see not only what score was assigned, but why, and how confident the AI was in its assessment." It has a timestamp and a scoring history, but no user-action log. | [Overview](https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview) | 2026-06-22 |
| SC Scope | not in A1–A5 | "Application Analysis only has access to data that the client configures to be sent to the service from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)." | [Configure](https://supporthub.smartsimple.com/hc/en-us/articles/40249784423831-Configure-AI-Application-Analysis) | 2026-07-07 |

### 3.2 AIP13 Fluxx Finn: GREEN (provisional), confirmed, weakest evidence

All rows cite [Fluxx AI page](https://www.fluxx.io/ai-grants-management-software). Its schema shows it published 2026-07-29 and modified 2026-08-03.

| Criterion | Rating | Quote | URL | Date |
|---|---|---|---|---|
| G1 Controls documented | met (weak) | "Opt-in Only AI is opt-in at the organization level, with profile-based permissions." The source is a product page with an FAQ. No Fluxx help-centre or terms page was found. | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| G2 Flag-only | met | "Nothing activates in the background — only when a user asks." Finn answers questions and surfaces "real-time risk flags". No record actions are described. | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| G3 Authority separation | met | "Finn keeps humans in the loop — it removes the friction of gathering and summarizing information, but every decision stays with your team." | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| R1 Not RED | met | "Access to the Fluxx MCP is included with Finn, so when you purchase Finn, you also receive access to the Fluxx MCP." Finn takes no actions. The bundled MCP lets agents "interact with your Fluxx data and workflows", with limits undocumented (AIP14, AMBER). | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S1 Human review | met | "Does Finn replace staff judgment? No." | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S2 No automated decision | met | "every decision stays with your team" | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S3 Data handling / training | met | "your data is never used to train any AI model — Fluxx's or a third party's." Also "sensitive fields are automatically masked". | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S4 Model disclosure | partly | "Finn runs on AWS Bedrock, inside Fluxx's own governed AWS environment — not a shared public model." The model is not named. | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S5 Opt-in | met | "Finn is off by default; your admins choose which capabilities to enable and for whom." | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| S6 Audit trail | not documented | The page makes no log or audit statement. | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |
| SC Scope | not in A1–A5 | "Grantelligence is a separate add-on with an annual subscription fee." Fluxx is a grantmaking vendor with no sponsor tie. | [Fluxx AI](https://www.fluxx.io/ai-grants-management-software) | 2026-07-29 / 08-03 |

### 3.3 AIP16 YourCause / Blackbaud Grantmaking: GREEN (provisional), confirmed, with an opt-in caveat

| Criterion | Rating | Quote | URL | Date |
|---|---|---|---|---|
| G1 Controls documented | met | "Do AI Application Summaries replace human review? No." (vendor FAQ), plus product help files | [YourCause post](https://www.yourcause.com/articles/new-and-now-ai-powered-grantmaking-with-yourcause) | 2026-07-16 |
| G2 Flag-only | met | "Summaries reflect application responses and do not add new information". The simple summary "Includes key signals such as eligibility". Form Intelligence changes apply only when a user selects "Apply updates". | [Summaries help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-applications-view-summaries.html); [Form Intelligence help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-forms-form-builder-ai-suggestions.html) | undated; release 2.148.0 scheduled 2026-06-15 ([release note](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-release-2.148.0.html)) |
| G3 Authority separation | met | "keeping final evaluation and decision-making with the grants team." AI roles are assigned in Role management. | [YourCause post](https://www.yourcause.com/articles/new-and-now-ai-powered-grantmaking-with-yourcause) | 2026-07-16 |
| R1 Not RED | met | "Your data remains unchanged unless you explicitly ask the AI feature to create or update something" | [Global opt-in help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html) | undated (cites 2026-01-07) |
| S1 Human review | met | "AI-generated summaries may contain errors. Always review the full application to confirm accuracy." | [Summaries help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-applications-view-summaries.html) | undated (2026) |
| S2 No automated decision | met | "This is not meant to replace human review or decision-making" | [YourCause post](https://www.yourcause.com/articles/new-and-now-ai-powered-grantmaking-with-yourcause) | 2026-07-16 |
| S3 Data handling / training | met (caveat) | "Blackbaud does not use customer or organizational data to retrain or improve the underlying model." Caveat: "When you enable generative AI features in your Blackbaud solutions, you are also enabling external connectors access to your data." Admins can clear this separately. | [Global opt-in help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html) | undated (cites 2026-01-07) |
| S4 Model disclosure | met | "For generative AI capabilities today, Blackbaud leverages models from OpenAI". This is a Blackbaud-wide statement. | [Blackbaud AI](https://www.blackbaud.com/ai) | undated (2026) |
| S5 Opt-in | partly | "If your organization used generative AI before January 7, 2026, your Blackbaud AI features will remain enabled to prevent any disruption." Otherwise the organisation "remains opted out by default". The opt-in covers "all current and future generative AI features". | [Global opt-in help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html) | undated (cites 2026-01-07) |
| S6 Audit trail | partly | "Each summary includes a generated date so you know when it was created." | [Summaries help](https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-applications-view-summaries.html) | undated (2026) |
| SC Scope | not in A1–A5 | "These complimentary features are available to customers who complete the required generative AI opt-in process". Blackbaud FE NXT (A1) keeps AMBER for its Development Agent and Chat. | [YourCause post](https://www.yourcause.com/articles/new-and-now-ai-powered-grantmaking-with-yourcause) | 2026-07-16 |

### 3.4 AIP28 Givebutter Magic: AMBER (downgraded)

| Criterion | Rating | Quote | URL | Date |
|---|---|---|---|---|
| G1 Controls documented | partly | "AI Features are enabled by default as part of the Services." The terms document defaults and non-optional features that the marketing pages do not mention. | [AI Addendum](https://givebutter.com/terms/ai-addendum) §8.1 | effective 2026-10-01 |
| G2 Flag-only | **not met** | "stretch goals that automatically increase as you raise more". Suggested amounts are also "automatically matched to your campaign type, cause, and donor's device". | [Recap](https://givebutter.com/blog/the-spread-2026-recap) | 2026-10-02 |
| G3 Authority separation | partly | "We may use AI-based tools to review transactions, detect fraud, and assess risk. These reviews may process personal information but are not visible to end users." Content still needs approval: "nothing gets sent or published without your approval" ([Recap](https://givebutter.com/blog/the-spread-2026-recap)). | [Privacy policy](https://givebutter.com/privacy) §6 | effective 2026-10-01 |
| R1 Not RED | met | "Givebutter Magic does not process payments." No evidence shows AI completing or clearing a payment. Fraud-review limits are undocumented, so the row is AMBER, not RED. | [Magic](https://givebutter.com/magic) | undated (2026) |
| S1 Human review | met | "AI-generated Content is provided as a suggestion only and is not a substitute for the User's independent judgment." | [AI Addendum](https://givebutter.com/terms/ai-addendum) §7.1 | effective 2026-10-01 |
| S2 No automated decision | **not met** | "certain features that are integral to core platform functionality (such as AI-assisted fraud detection and Receipt Matching) cannot be disabled." | [AI Addendum](https://givebutter.com/terms/ai-addendum) §8.2 | effective 2026-10-01 |
| S3 Data handling / training | partly | "in some cases, data captured by such services may be used for AI model training." This refers to the observability logs (Braintrust). Model providers are contractually barred from training. Homegrown Models train on de-identified data by default, and customers opt out through Support. | [AI Addendum](https://givebutter.com/terms/ai-addendum) §3, §8.3 | effective 2026-10-01 |
| S4 Model disclosure | met | "As of the Effective Date, these providers are Anthropic, Google, and OpenAI." | [AI Addendum](https://givebutter.com/terms/ai-addendum) §2 | effective 2026-10-01 |
| S5 Opt-in | **not met** | "AI Features are enabled by default as part of the Services." This contradicts the recap FAQ, which calls receipt matching "optional and only used when you choose to use them". Only AI Connectors "require affirmative opt-in". | [AI Addendum](https://givebutter.com/terms/ai-addendum) §8.1, §8.4; [Recap](https://givebutter.com/blog/the-spread-2026-recap) | effective 2026-10-01; 2026-10-02 |
| S6 Audit trail | partly | "We collect metadata about these connections (such as which user connected and connection timestamps)." The vendor keeps request logs, but customers get no audit log. | [Privacy policy](https://givebutter.com/privacy) §6 | effective 2026-10-01 |
| SC Scope | not in A1–A5 | "AI Connectors can only read your data. They can never create, edit, or delete anything in your account." Givebutter is a fundraising platform. | [Givebutter docs](https://docs.givebutter.com/ai-connectors/overview.md) | undated (2026) |

**Note on dates.** The recap post is dated 2026-10-02 in its byline and schema. The census CSV gives source_date 2026-10-01, which looks like the event date. The help article on AI connectors is dated 2026-10-14 ([help](https://help.givebutter.com/en/articles/15891040-how-to-connect-an-ai-assistant-to-your-account)).

## 4. Is any of the four the first GREEN under §7?

**No.** There are three separate reasons.

1. **Area scope.**
   - §1 says the AI overlay "is reported for every area", and its provider lists name who is in scope.
   - SmartSimple, Fluxx, YourCause grantmaking and Givebutter are not listed in A1–A5.
   - Blackbaud FE NXT and Foundant CommunitySuite are listed in A1, and both are AMBER.
   - The four rows use the §7 vocabulary on vendor products, as the census itself says ("The overlay vocabulary was written for DAF providers").
2. **Chronology.**
   - The v1.0 overlay in [quadrant-calibration.md](quadrant-calibration.md) gave **GREEN** to Fidelity Charitable and **"GREEN / none"** to Ren, Ren RDE, RCF and AEF.
   - [quadrant-v11-blind-and-calibration.md](quadrant-v11-blind-and-calibration.md) §6 replaced those with None (inform-only) and None, and concluded "No provider earns GREEN."
   - A GREEN label had therefore already been used and then withdrawn.
3. **Entity scope.** None of the four is tied by a source to a sponsor's DAF program, so none can move a sponsor's overlay.

The supportable claim is narrower. SmartSimple AI Application Analysis, Fluxx Finn and YourCause AI Application Summaries are the first vendor AI products in the repo whose first-party pages meet the §7 GREEN wording (flag-only plus authority separation). They are provisional and untested, and none sits in a DAF money path. Of the three, SmartSimple has the most complete documentation (help article, configuration article and FAQ). Fluxx has the least: one marketing page.

## 5. Does SmartSimple's GREEN change the Foundant-family overlay?

**No. Foundant stays AMBER. The census's reasoning needs one correction.**

- **New first-party tie.** The SmartSimple "Configure AI Application Analysis" FAQ (updated 2026-07-07, © Foundant Technologies) says the service takes data configured "from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)". It says the service is reached from those applications' backend services.
  - The Fia release (2026-09-02; context, [financialcontent mirror](https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations)) also says Foundant's AI strategy includes "AI features built directly into its products — such as AI-driven application analysis and scoring and AI summarization — and MCP Connectors".
  - So the census line "even though SmartSimple is in the Foundant family" understates the case. The evidence does reach Foundant the vendor, including CommunitySuite, which is in A1.
- **Why the overlay does not move.**
  1. **Foundant's AMBER rests on Fia.** Fia is in beta, and its agents and "policy engine" have claimed but undocumented controls. A documented GREEN component does not document Fia's limits. §7 has no rule for combining components, so a provider is GREEN only if every evidenced live AI capability meets the GREEN wording (rule inferred) [I].
  2. **No sponsor tie.** Under the entity scope rule, vendor evidence is not sponsor evidence. No source ties Application Analysis to any community foundation's DAF grant-recommendation workflow. The repo's one SmartSimple DAF edge (The Boston Foundation pays DAF grants "via Smart Simple portal", EG012) does not mention the AI feature.
  3. **Foundant MCP connectors** are named in the Fia release, but no controls were read for them (foundant.com is robots-barred).

## 6. Limits

- These are vendor statements read once more. Nothing was tested, and no demo, login or trial was used. Under §3, each claim is `vendor_claim` evidence.
- Fluxx publishes no help-centre or terms page that this reader could find. Finn's rating rests on one product page.
- Several Blackbaud and Givebutter pages are undated. They were treated as 2026 because they were current at access and describe 2026 features or cut-offs (2026-01-07; release 2.148.0).
- Absence of a log or audit statement (Fluxx S6) is not evidence that no log exists.
- §7 has no rules for scope (vendor products) or for combining components. §3 and §4 depend on inferences marked [I], proposed for clarification as P-B4301-05.
- The Givebutter downgrade relies on terms and privacy text. Those are legal documents and may describe the product more broadly than it behaves.
- Not re-rated: the other 26 census rows, including AIP14 Fluxx MCP and AIP18 Blackbaud Chat.

## Exact corrections

### `research/mission-2026-11-14/direction-ai-product-census.md`

- **Find:** "These are the first GREEN-eligible readings in the repo, marked provisional."
- **Replace with:** "These are the first GREEN-eligible readings of vendor AI products in the repo, marked provisional. None is the first GREEN under §7: none is an A1–A5 provider, and v1.0 calibration had already labelled Fidelity Charitable GREEN and Ren/RCF/AEF “GREEN / none” before v1.1 withdrew both [b43n25-01]"
- **Find:** "These are complimentary once the customer opts in."
- **Replace with:** "These are complimentary once the customer opts in. The default is not universal: organisations that “used generative AI before January 7, 2026” stay enabled, and enabling generative AI also enables “external connectors access to your data” unless an admin clears it [b43n25-01]"
- **Find:** "Under the entity scope rule (§7), they do not change any sponsor's overlay, or the Foundant overlay (AMBER, Fia beta), even though SmartSimple is in the Foundant family."
- **Replace with:** "Under the entity scope rule (§7), they do not change any sponsor's overlay. SmartSimple's own FAQ says the Application Analysis service takes data “from within the Foundant application (GLM/SLM, CommunitySuite, GivingData, SmartSimple)”, so the evidence does reach Foundant the vendor. The Foundant overlay still stays AMBER because Fia's agents and policy engine have undocumented limits and no source ties the feature to a sponsor's DAF program [b43n25-01]"
- **Find:** "**Givebutter Magic** (2026-10-01) is the strongest-documented fundraising row."
- **Replace with:** "**Givebutter Magic** (2026-10-01) is AMBER, not GREEN. Its AI Addendum (effective 2026-10-01) says “AI Features are enabled by default”, that AI-assisted fraud detection and Receipt Matching “cannot be disabled”, and that observability-log data “may be used for AI model training”. Its privacy policy says AI tools “review transactions, detect fraud, and assess risk” with undocumented limits [b43n25-01]"
- **Find:** "| approval before send or publish; read-only connectors; training limits | free; Plus $29/month | **GREEN (provisional)**"
- **Replace with:** "| approval before send or publish; read-only connectors; AI on by default; fraud and receipt AI cannot be disabled | free; Plus $29/month | **AMBER** [b43n25-01]"
- **Find:** "| GREEN (provisional) | 4"
- **Replace with:** "| GREEN (provisional) | 3 [b43n25-01]"
- **Find:** "| AMBER | 9"
- **Replace with:** "| AMBER | 10 [b43n25-01]"
- **Find:** "All four GREENs are provisional"
- **Replace with:** "Three GREENs remain, all provisional; Givebutter Magic moved to AMBER [b43n25-01]"
- **Find:** "(P-B43N25-01)."
- **Replace with:** "(P-B43N25-01). Validated 2026-11-20: SmartSimple, Fluxx Finn and YourCause hold as GREEN (provisional), and none is the first GREEN under §7 [b43n25-01]"
- **Find:** "| Opt-in, off by default | Blackbaud (global generative-AI switch); Fluxx Finn; SmartSimple (vendor must enable) | Bloomerang; Salesforce"
- **Replace with:** "| Opt-in, off by default | Blackbaud (global generative-AI switch; pre-2026-01-07 users stay enabled); Fluxx Finn; SmartSimple (vendor must enable) | Bloomerang; Salesforce; Givebutter (AI on by default; fraud and receipt AI cannot be disabled) [b43n25-01]"
- **Find:** "Givebutter (third-party models; own models de-identified only)"
- **Replace with:** "Givebutter (third-party models; own models de-identified only; observability and fraud-tool data “may be used for AI model training”) [b43n25-01]"

### `data/mission-2026-11-14/philanthropy-ai-products-2026.csv`

- **Find:** "most features free; AI custom reports need Givebutter Plus ('starts at $29/month'),GREEN (provisional)"
- **Replace with:** "most features free; AI custom reports need Givebutter Plus ('starts at $29/month'),AMBER [b43n25-01]"
- **Find:** "Documented approval-before-send, no payment processing, read-only connectors, training limits; untested"
- **Replace with:** "Approval before send or publish and read-only connectors are documented, but AI features are on by default; fraud-detection and Receipt Matching AI cannot be disabled; stretch goals and suggested amounts change automatically (not flag-only); AI transaction review has undocumented limits [b43n25-01]"
- **Find:** "connectors need team authorisation; contact summaries can be turned off"
- **Replace with:** "AI Features “enabled by default” (AI Addendum 8.1); fraud-detection and Receipt Matching AI “cannot be disabled” (8.2); connectors need affirmative opt-in (8.4); contact summaries can be turned off [b43n25-01]"
- **Find:** "some features send data to external providers"
- **Replace with:** "some features send data to external providers (Anthropic; Google; OpenAI); observability-log and fraud-tool data “may be used for AI model training” (AI Addendum s3; Privacy s6) [b43n25-01]"
- **Find:** "no: 'Givebutter Magic does not process payments'"
- **Replace with:** "no: 'Givebutter Magic does not process payments'; platform AI fraud tools review transactions (Privacy s6) [b43n25-01]"
- **Find:** "2026-10-01,2026-11-15"
- **Replace with:** "2026-10-02,2026-11-15 (re-read 2026-11-20) [b43n25-01]"
- **Find:** "yes: generative AI off until an org admin opts in; opt-out 'takes effect immediately'"
- **Replace with:** "yes for organisations that have not opted in: generative AI off until an org admin opts in; organisations that used generative AI before 2026-01-07 “remain enabled”; opt-in also enables external-connector access unless cleared; opt-out 'takes effect immediately' [b43n25-01]"
- **Find:** "Opt-in default off, no-training, human-decision statements documented first-party; summaries only"
- **Replace with:** "Opt-in default off, no-training, human-decision statements documented first-party; summaries only; re-confirmed GREEN (provisional) by a second reader 2026-11-20 with an opt-in grandfathering caveat [b43n25-01]"
- **Find:** "admin field control; untested; not in a DAF money path"
- **Replace with:** "admin field control; untested; not in a DAF money path; re-confirmed 2026-11-20; the same service is configured from Foundant GLM/SLM, CommunitySuite and GivingData (Configure article FAQ, 2026-07-07) but the Foundant overlay stays AMBER [b43n25-01]"
- **Find:** "Beta with controls claimed but not documented (v11 consensus); foundant.com barred to this agent by robots"
- **Replace with:** "Beta with controls claimed but not documented (v11 consensus); foundant.com barred to this agent by robots; Foundant's GREEN-eligible Application Analysis (AIP12) is a separate feature and does not document Fia's limits so AMBER stands [b43n25-01]"
- **Find:** "Documented opt-in, field control, no-training and human-decision statements; flags only; untested"
- **Replace with:** "Documented opt-in, field control, no-training and human-decision statements; flags only; untested; re-confirmed 2026-11-20 on the product page FAQ (published 2026-07-29); the Fluxx MCP bundled with Finn stays AMBER (AIP14) [b43n25-01]"

### `research/DAF-INDUSTRY-REPORT-2026-11.md`

- **Find:** "Givebutter Magic is a GREEN/AMBER boundary case."
- **Replace with:** "Givebutter Magic is AMBER: its AI Addendum turns AI features on by default and makes fraud-detection and Receipt Matching AI non-optional. None of the three GREENs is a DAF provider, so the v1.1 overlay still has no GREEN provider [b43n25-01]"

### `research/mission-2026-11-14/strategic-synthesis.md`

- **Find:** "Givebutter's stretch goals and suggested amounts change without per-action approval, so it is a GREEN/AMBER boundary case."
- **Replace with:** "Givebutter is AMBER: its stretch goals and suggested amounts change without per-action approval, its AI features are on by default, and its fraud-detection and Receipt Matching AI cannot be disabled [b43n25-01]"
- **Find:** "| Givebutter AI overlay | GREEN | **GREEN/AMBER boundary**"
- **Replace with:** "| Givebutter AI overlay | GREEN | **AMBER** (was GREEN/AMBER boundary in wave 28) [b43n25-01]"

Every Find string above was checked by script and occurs exactly once in its file. No Find contains a straight double quote. Where a replacement goes into an unquoted CSV field, it contains no commas.

## Data dictionary

### `data/mission-2026-11-14/green-overlay-validation-2026-11-20.csv` (one row per product × criterion; 48 rows)

| Column | Meaning |
|---|---|
| product_id | Census ID (AIP12, AIP13, AIP16, AIP28) |
| product | Product name as in the census |
| criterion_id | G1–G3 (§7 GREEN), R1 (§7 RED test), S1–S5 (supplementary criteria from the brief, not in §7), S6 (audit trail, from the Y3 rubric), SC (area and entity scope), V (overall overlay verdict) |
| criterion | Criterion text |
| criterion_basis | Where the criterion comes from, and whether it is binding for the overlay |
| rating | met; met (weak); met (caveat); partly; not met; not documented; not in scope; or, for V, the re-rated overlay |
| quote | Verbatim text from the source page, checked by script against the fetched text. AIP13 S6 records an absence. |
| source_url | First-party URL quoted |
| source_date | Date on the page (published, updated or effective), or "undated" with context |
| accessed | 2026-11-20 |
| note | Caveats, secondary quotes and contradictions |

### `data/mission-2026-11-14/queue-proposals-b43n25-01.csv`

Same header and format as `queue-proposals-gap19-13.csv`. It has five proposals, P-B4301-01 to -05:
- Foundant-wide Application Analysis in DAF workflows;
- Givebutter AI fraud review;
- Fluxx help, terms and MCP tool list;
- Blackbaud grandfathered AI defaults;
- §7 scope and aggregation rules.

## Source register

| ID | Source | Type | Source date | Accessed | URL |
|---|---|---|---|---|---|
| V1 | SmartSimple AI Application Analysis Overview | vendor help | 2026-06-22 | 2026-11-20 | https://supporthub.smartsimple.com/hc/en-us/articles/40255259635223-AI-Application-Analysis-Overview |
| V2 | SmartSimple Configure AI Application Analysis (with FAQ) | vendor help | 2026-07-07 | 2026-11-20 | https://supporthub.smartsimple.com/hc/en-us/articles/40249784423831-Configure-AI-Application-Analysis |
| V3 | SmartSimple June 2026 Release Notes | vendor help | updated 2026-11-02 | 2026-11-20 | https://supporthub.smartsimple.com/hc/en-us/articles/40168112536343-June-2026-Release-Notes |
| V4 | SmartSimple Configure AI Driven Application Summaries | vendor help | 2026-06-22 | 2026-11-20 (fetched; not cited in table) | https://supporthub.smartsimple.com/hc/en-us/articles/40796121577879-Configure-AI-Driven-Application-Summaries |
| V5 | Fluxx AI page (Finn, MCP, FAQ) | vendor product page | 2026-07-29 (modified 2026-08-03) | 2026-11-20 | https://www.fluxx.io/ai-grants-management-software |
| V6 | YourCause "New and Now: AI-Powered Grantmaking" (with FAQ) | vendor blog | 2026-07-16 | 2026-11-20 | https://www.yourcause.com/articles/new-and-now-ai-powered-grantmaking-with-yourcause |
| V7 | GrantsConnect help: AI-generated summaries | vendor help | undated | 2026-11-20 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-applications-view-summaries.html |
| V8 | GrantsConnect help: Form Intelligence | vendor help | undated | 2026-11-20 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-forms-form-builder-ai-suggestions.html |
| V9 | GrantsConnect Release 2.148.0 | vendor release note | 2026-06-15 (scheduled) | 2026-11-20 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/grantsconnect/content/gc-release-2.148.0.html |
| V10 | Blackbaud: Opt In to Generative AI Features Globally (FAQ) | vendor help | undated (cites 2026-01-07) | 2026-11-20 | https://webfiles-sc1.blackbaud.com/files/support/helpfiles/admin/content/bb-ai-global-opt-in.html |
| V11 | Blackbaud AI (FAQ) | vendor page | undated | 2026-11-20 | https://www.blackbaud.com/ai |
| V12 | Givebutter Spread 2026 recap (FAQ) | vendor blog | 2026-10-02 | 2026-11-20 | https://givebutter.com/blog/the-spread-2026-recap |
| V13 | Givebutter Magic page (FAQ) | vendor page | undated | 2026-11-20 | https://givebutter.com/magic |
| V14 | Givebutter AI Addendum | vendor terms | effective 2026-10-01 | 2026-11-20 | https://givebutter.com/terms/ai-addendum |
| V15 | Givebutter Privacy Policy §6 | vendor terms | effective 2026-10-01 | 2026-11-20 | https://givebutter.com/privacy |
| V16 | Givebutter help: connect an AI assistant | vendor help | 2026-10-14 | 2026-11-20 | https://help.givebutter.com/en/articles/15891040-how-to-connect-an-ai-assistant-to-your-account |
| V17 | Givebutter docs: AI Connectors | vendor docs | undated | 2026-11-20 | https://docs.givebutter.com/ai-connectors/overview.md |
| V18 | Foundant Fia release (context for §5) | vendor PR mirror | 2026-09-02 | 2026-11-20 | https://www.financialcontent.com/article/gnwcq-2026-9-2-foundant-introduces-fia-a-new-ai-platform-built-for-social-good-organizations |
| R1 | Methodology §1, §3, §7, §8 | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/evidence-quadrant-methodology.md |
| R2 | v1.0 AI overlay (Fidelity GREEN; Ren/RCF/AEF GREEN/none) | repo | 2026-11-14 | 2026-11-20 | research/mission-2026-11-14/quadrant-calibration.md |
| R3 | v1.1 overlay adjudication ("No provider earns GREEN") | repo | 2026-11 | 2026-11-20 | research/mission-2026-11-14/quadrant-v11-blind-and-calibration.md §6 |
| R4 | Wave 28 validation (V28-26 to V28-30) | repo | 2026-11-15 | 2026-11-20 | research/mission-2026-11-14/validation-wave28-report.md |
| R5 | Boston Foundation DAF grants via SmartSimple portal (EG012) | repo | — | 2026-11-20 | research/mission-2026-11-14/queue-batch33-market-structure.md |
