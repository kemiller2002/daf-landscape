# AI in charity vetting and grant due diligence: landscape and evidence (as of 2026-11-21)

**Prepared:** 2026-11-21. Desk research only. This is not legal advice. No vendor, regulator or sponsor was contacted, and no product was tested.
**Companion file:** [`landscape-sources.csv`](landscape-sources.csv), with source IDs LS-001 to LS-087.
**Scope:** How AI is used, and not used, to (a) verify charity eligibility and identity, (b) screen grantees against sanctions and adverse media, and (c) support grant due diligence and review. The lens is a DAF sponsor's vetting design.

## Evidence classes used in this file

| Tag | Meaning |
|---|---|
| **[vendor claim]** | The vendor's own press release, product page, blog or help article. It shows what is marketed. It does not show that the product works. |
| **[independent/regulatory]** | A regulator, a statute or regulation, a standards body (NIST, OWASP, FATF), or a public body. |
| **[peer-reviewed]** | Published after peer review. Few sources in this file qualify. |
| **[preprint]** | arXiv papers, Federal Reserve staff working papers, and vendor-published benchmarks with a disclosed method. Not peer-reviewed. |
| **[survey: n, date]** | A survey, giving its sample size and date. |
| **[NGO report]** | A study by an NGO or advocacy group, including academic clinics working with NGOs. |
| **[secondary]** | Press coverage or a law-firm summary, used where the primary source was not read. |
| **[repo V]** | A finding from this repository's earlier research, which has been through repo validation waves. That research keeps its own [F]/[S]/[C]/[I] labels. |

**How each source was accessed.** "read" means the page was fetched and read for this file. "snippet" means only search-engine text was seen. The CSV `limitation` column records which. Where a figure comes only from a snippet, the text says so.

**Access note.** In earlier runs the repo treated candid.org as blocked, because its robots.txt returned 403. For this file, one Candid blog post (LS-024) was read with a web-fetch tool on 2026-11-21. That differs from the repo's earlier access rule. A validator may prefer to re-source that figure.

---

## 0. Bottom line

1. **The strongest evidence for AI in vetting is in sanctions name matching. None of it comes from charities.**
   - A Federal Reserve staff working paper found that LLMs cut sanctions-screening false positives by 92% and raised detection by 11% against the best fuzzy-matching baseline. The LLMs were "over four orders of magnitude slower", so the authors propose a cascade (LS-048) [preprint].
   - A public benchmark of 755,540 expert-labelled pairs gives GPT-4o an F1 of 99.0%, against 91.3% for a production rule-based matcher (LS-049) [preprint].
   - LSEG says its World-Check Resolve suppressed "an average of 74%" of false positives, with no loss of recall, in its own testing on 650,000 cases (LS-042) [vendor claim].
   - No study runs any of this on charity or DAF grantee populations. No result has been audited independently in production.
2. **AI for grant due diligence has spread, but its accuracy has not been shown.**
   - Grant Guardian (Patrick J. McGovern Foundation) scores grantee finances from 990s and audits. It reports 189 organisations "supported" and one user's claim of "two to three minutes per grantee". It publishes no accuracy data (LS-039) [vendor claim].
   - Benevity says more than 30% of its grantmaking clients used AI Grant Summaries within a week of launch (LS-033) [vendor claim].
   - SmartSimple, Fluxx Finn and Blackbaud/YourCause document flag-only or summary-only roles (LS-005) [repo V].
   - No vendor publishes accuracy, error or override rates.
3. **Funders rarely use AI to decide who gets money.**
   - In Candid's 2025 forecast survey, 1% of foundations said they use generative AI to screen applicants or decide whom to fund. 97% said no (LS-024) [survey: n=529, 2025].
   - MacArthur's policy lists "Using AI for grantmaking decisions or evaluation" as unacceptable (LS-078) [independent/regulatory: funder policy].
   - The repo found no DAF sponsor that documents AI in grant approval or eligibility (LS-005, LS-006) [repo V]. This file found nothing that contradicts that.
4. **Regulators encourage AI in AML, but the encouragement is aimed at banks, not charities.**
   - FinCEN's April 2026 proposed program rule names "machine learning, generative artificial intelligence (GenAI)". It says institutions that "responsibly experiment" will not face added enforcement risk "solely" for doing so (LS-057) [independent/regulatory].
   - The rule binds BSA financial institutions. A charity sponsor is not one (REG-038).
   - The 2026 interagency model-risk guidance that replaced the 2011 guidance puts generative and agentic AI **outside its scope** (LS-059) [independent/regulatory].
5. **Documented harm comes from over-screening, not from AI as such.**
   - De-risking is well documented. Two-thirds of U.S. nonprofits working abroad reported financial-access problems (LS-068) [NGO report; n=305 per secondary coverage].
   - In October 2026 FinCEN restated that "the vast majority of U.S.-based NPOs present a low risk" and asked banks to evaluate "each NPO individually" (LS-064) [independent/regulatory].
   - An AI that adds more adverse-media and fuzzy-match hits, with no calibrated way to clear them, repeats this harm mechanism faster.

---

## 1. Charity data and verification providers

| Provider | AI or automation claimed | What is evidenced | Class |
|---|---|---|---|
| **Candid (GuideStar)** | - Candid search (2026-01-15) "applies AI in practical ways".<br>- AI LOI drafts (2026-01-20).<br>- Claude MCP connector (2025-12-02).<br>- Fundraising assistant (2026-08-31).<br>- AI flagging of nonprofit-distress news (2026-06-30). Candid calls a flag "a 'signal' of distress, not a confirmed event". It reports 65 flagged articles for March–May 2026 (58 closures, 7 layoffs). | - Charity Check is a **deterministic** status product built on Pub 78, the BMF, the IRB, the Auto-Revocation list and the OFAC SDN list. It pings the IRS "every 20 minutes" (LS-008) [repo V].<br>- No AI is documented inside Charity Check.<br>- The Chronicle reports Candid "cuts staff, bets its future on AI" (LS-023) [secondary, snippet].<br>- The API licence bars mining Candid data for "A.I., large language models, machine learning" without written consent (LS-007) [repo V]. | [vendor claim] (LS-020–022); [repo V] |
| **Charity Navigator** | - Horizon AI Search (2025-11-24), built on Giving Compass's natural-language search API, gives "personalized recommendations".<br>- The search page is labelled Beta and says responses are AI-generated: "double-check for accuracy". | - No AI in the ratings themselves.<br>- Ratings cover about 17% of Pub 78 records. CN's 990 rules leave out 990-EZ and 990-N filers and churches (LS-008) [repo V].<br>- The API terms say ratings "may not be used in any other calculation" (LS-007) [repo V]. | [vendor claim] (LS-025, LS-026) |
| **NGOsource** (Council on Foundations and TechSoup) | **None found.** | - Equivalency determinations (EDs) are held in a central repository and reused across funders.<br>- An ED badge is tied to a specific funder and period (LS-028).<br>- No public AI feature was found for 2025–2026. Searches returned none [snippet]. | [vendor claim] (process only) |
| **Goodstack** (formerly Percent) | - KYNP ("Know Your Nonprofit"), 2026-08-03: tiered due diligence plus monitoring.<br>- Screening covers "130+ ... sanctions lists", "120+ law enforcement and financial crime watchlists" and adverse media from "11,000+ sources".<br>- A Goodstack blog says AI lets verification run "quickly and consistently across jurisdictions and languages". | - 7.5 million verifications claimed (LS-029; LS-008 [repo V]).<br>- No public document ties AI to a specific KYNP step (LS-030 [snippet]).<br>- No accuracy or false-positive data is published. | [vendor claim] |
| **TechSoup Validation Services** | - The validation page mentions "enterprise AI" and real-time "fraud defense". | - Verifies charitable status in the organisation's home country.<br>- Has about 70 partners and verifies about 150,000 NGOs a year, per a Devex op-ed (LS-031) [snippet].<br>- How AI is used in verification is not described. | [vendor claim] |
| **Benevity** | - "AI-native" platform (2026-06-04).<br>- AI Grant Summaries (2026-03-16).<br>- Grants Scoring "against each program's own evaluation rubric", where "administrators retain full decision-making control".<br>- Match Assurance: decline rate "30% to less than 3%". | - The due-diligence page says nonprofits are "continuously validated" by "in-house vetting experts". Sanctions watch-listing and adverse media are add-ons. **The page does not mention AI** (LS-034) [read].<br>- **The 30%→<3% figure is for employee match-request declines, not charity vetting.** A Benevity blog attributes it to "one of our global partners" (LS-032 [read]; LS-035 [snippet]). | [vendor claim] |
| **PayPal Giving Fund** | **None found.** | - The policy describes 501(c)(3) public-charity checks and removal of sanctioned charities.<br>- An older U.S. version cites "regular checks of GuideStar data". The Sept 2025 U.S. excerpt seen does not mention OFAC (LS-036) [snippet; version uncertain]. | [vendor claim] |
| **GlobalGiving** | **None.** It says the opposite. | - "Human-driven". Automated systems "complement human decision-making rather than replacing it".<br>- Due-diligence renewal every two years (LS-037) [snippet]. | [vendor claim] |
| **CAF America** | **None found.** | - Validation is risk-based, with an Enhanced Validation option that reviews board members and senior staff.<br>- It warns that an ED alone "is not sufficient" (LS-038) [snippet]. | [vendor claim] |
| **Chariot** | - Gift Processing AI agent; MCP server (LS-005) [repo V]. | - Its compliance checks (identity, gift eligibility, transaction monitoring) are not described as AI.<br>- Its contract leaves grant approval to the sponsor (LS-002) [repo V]. | [repo V] |
| **Every.org, Endaoment** | - Every.org: no AI vetting found; it runs a free charity API (LS-008).<br>- Endaoment: "None (watch)" (LS-005). | Not re-checked in this pass. | [repo V] |

**Takeaways [inference].**
- (a) The eligibility layer is deterministic everywhere: IRS lists plus OFAC.
- (b) AI appears around that layer, in search, recommendations, LOI drafting, distress signals and global KYB marketing. It does not appear in the status determination.
- (c) No provider publishes AI accuracy, false-positive or bias metrics.
- (d) The license terms of the two largest US data providers restrict using their data as model features (LS-007). That limits "AI vetting built on ratings" regardless of accuracy.

---

## 2. Grantmaking software: what the AI does

| Vendor and product | Function | Documented controls | Evidence |
|---|---|---|---|
| **SmartSimple** AI Application Analysis | Scores and flags applications | Results are "inputs to reviewer judgment and not as final determinations". No external AI services; no training; admins choose the fields analysed | GREEN (provisional) (LS-005) [repo V]; [vendor claim] |
| **Fluxx** Finn (2026-08-04) | Q&A, drafting, "real-time risk flags" grounded in the customer's grants data | Off by default; runs on AWS Bedrock in Fluxx's environment; "never trains on your data" | (LS-040) [vendor claim]; GREEN (provisional) in LS-005 [repo V]. **How risk flags are produced is not documented** |
| **Blackbaud / YourCause** Application Summaries, Form Intelligence | Summarises applications | Opt-in; "final evaluation and decision-making" stays "with the grants team" | GREEN (provisional) (LS-005) [repo V] |
| **Foundant** Fia | Knowledge base, agents, policy engine | Claimed but not documented | AMBER (LS-005) [repo V] |
| **Bonterra** Que | Drafting, scoring, agentic actions | "People always make the final decisions" | AMBER (GREEN-boundary) (LS-005) [repo V] |
| **Submittable** Automated Review; Smart Reviewer; Smart Summaries | Extracts and validates data, analyses essays and media, scores against a rubric. Smart Reviewer acts "as an AI reviewer right alongside your human team" | "without replacing human judgment" (video). No documentation found on how scores are validated or audited | (LS-041) [vendor claim; snippet]. AMBER (unverified) in LS-005 |
| **Benevity** Grants | Summaries and rubric scoring | "administrators retain full decision-making control" | (LS-032, LS-033) [vendor claim] |
| **CyberGrants** | Not found: searches returned unrelated results | — | Not evidenced |
| **Grant Guardian** (PJMF, free; runs on Claude) | Extracts and scores grantee financial health from 990s and audits; AI qualitative summary; foundation-set criteria | "a human in-the-loop at key steps"; uploaded data private to each foundation | (LS-039) [vendor claim]. **No accuracy validation published** |

**What is evidenced.** Adoption, and stated roles of summarising, scoring or flagging with a human decision.

**What is not evidenced.**
- Agreement with expert reviewers.
- Extraction error rates on 990s or audits.
- Bias across applicant types, such as small, faith-based or non-English applicants.
- The effect of AI scoring on who gets funded.

---

## 3. AML and sanctions screening AI, and the research literature

### 3.1 Vendor false-positive claims (none independently verified)

| Vendor | Claim | Basis stated | Class |
|---|---|---|---|
| LSEG World-Check Resolve (2026-09-28) | Suppressed "an average of 74%" of false positives with no loss of recall | Internal testing on 650,000 screening cases | [vendor claim] (LS-042) |
| LSEG World-Check Verify (2025-10-01), On Demand (2025-09-30) | "fewer false positives" | No figure given | [vendor claim] (LS-043) |
| Ripjar Screening Assistant (2025-09-11) | False positives cut by "up to 90%" | Not stated | [vendor claim] (LS-044) |
| Shield Alert Closure Agent (2026-06-29) | 77.3% fewer false positives; agent "close[s] compliance alerts autonomously" | "customer evaluations" | [vendor claim] (LS-045) |
| Sigma360, SymphonyAI, Flagright, Temenos | "up to 90%", ">90%", "up to 98%" fewer; "<2%" false positives | Case studies or none | [vendor claim] (LS-087) |
| Dow Jones Risk & Compliance | Generative AI in due diligence; "significantly reduces false positives" | No figure given | [vendor claim] (LS-047) |
| ComplyAdvantage, Moody's, Napier | No current false-positive figure was found in this pass | — | Not evidenced |

**Independent evaluation.** A press release dated 2026-09-23 reports an independent evaluation of Axle's KYC screening agent by FairPlay (LS-046). It was not read, so it is not relied on here. No published audit of any vendor's false-positive claim was found.

### 3.2 Research literature

- **LLMs versus fuzzy matching for sanctions screening.** Allen & Hatfield, FEDS 2025-092, September 2025 (LS-048) [preprint].
  - Four LLM families were tested on names and addresses.
  - Result: false positives −92% and detection +11% against the best fuzzy baseline, across realistic thresholds. Smaller models from the same families performed comparably.
  - Speed: the LLMs were more than 10⁴ times slower. A cascade (fuzzy or exact matching first, LLM for uncertain cases) is "nearly twice as fast" as LLM-only, with similar accuracy.
  - The page does not say whether the test data were synthetic or real. The paper gives the authors' views, not the Board's.
- **OpenSanctions Pairs.** arXiv 2603.11051, v2 2026-08-25 (LS-049) [preprint].
  - 755,540 expert-labelled pairs, over 1 million entities, 293 sources, 45 jurisdictions.
  - F1: rules 91.3%, GPT-4o 99.0%, and a locally deployable 14B open model 98.2%.
  - Failure modes differ: "rules tend to over-match", while LLMs "struggle with cross-script transliteration".
  - The authors argue that pairwise matching is nearing its ceiling. Gains now lie in blocking, clustering and "uncertainty-aware review".
- **OpenSanctions practitioner note** (2026-05-12) (LS-050).
  - In production, LLMs work *downstream* of classical matching. Two LLMs, an analyst and an adversarial "senior reviewer", must agree, and any disagreement goes to manual review, because the team does not "trust either model in isolation".
  - It warns that "a government biography could carry a planted prompt injection", and that internal KYC notes are "prone to amplifying bias".
- **Adverse media.**
  - Chernakov et al. (arXiv 2602.23373, December 2025) built an agentic RAG screener that produces an "Adverse Media Index". The abstract claims it separates high-risk from low-risk people but gives no metrics (LS-051) [preprint].
  - Taktile's KYBench (April 2026, updated 2026-09-07; 46–47 businesses; ground truth from AML-expert annotators) reports per-model "adjusted F1" and run-to-run consistency. Examples: GPT-5.2 Pro adjusted F1 90.3%, with precision 66.7% and recall 43.8% in a capped 15-step configuration; Claude Opus 4.6 consistency 83.3%. It reports a 0% hallucination rate among false positives, and attributes 69% of false positives to "real but marginal" evidence (LS-052) [preprint; vendor-published].
  - **Caution:** KYBench's "adjusted F1" is not defined in the text read, and it does not match the plain F1 of the stated precision and recall (about 0.53). The sample is very small.
- **LLM extraction from Form 990 and nonprofit documents.** **No peer-reviewed or preprint accuracy study on Form 990 extraction was found.**
  - The nearest work is on budget documents (arXiv 2511.10659, which validates extracted figures against reported totals) and corporate disclosures (LS-053) [preprint].
  - Vendor 990 parsers publish no benchmark (LS-054) [vendor claim].
  - Legal-domain RAG tools hallucinated on 17–33% of benchmark queries (LS-055, via LS-010) [preprint/repo V]. That suggests extraction and summaries need span-level citation checks.

---

## 4. Regulation and policy relevant to AI in screening and vetting

| Instrument | What it says that matters here | Applies to a DAF sponsor? | Class |
|---|---|---|---|
| **OFAC Framework for Compliance Commitments** (2019-05-02) | Five components: management commitment, risk assessment, internal controls, testing/audit, training. Appendix A lists screening-software shortcomings among root causes, including "failing to update screening software" and missing identifiers. Strict liability; screening configuration is the organisation's responsibility | Yes, for every U.S. person (REG-036) | [independent/regulatory] (LS-056) |
| **OFAC recordkeeping** (31 CFR 501.601; 10-year rule, final 2025-03-21) | Screening logs, dispositions and blocked or rejected reports kept for 10 years | Yes (REG-037) | [repo V] (LS-011) |
| **FinCEN AML/CFT program NPRM** (91 FR, 2026-04-10; RIN 1506-AB72; docket FINCEN-2026-0034; comments closed 2026-06-09) | - Withdraws and supersedes the 2024 Program NPRM ("should be considered withdrawn and superseded").<br>- Names "machine learning, generative artificial intelligence (GenAI)".<br>- Responsible experimenters "will not incur any additional risk" of enforcement "solely based on the use of innovative technologies".<br>- "does not reference or require the use of any particular technology".<br>- Says MRM guidance may be "overly burdensome and ill-fitted" to illicit-finance risk.<br>- **Still a proposal. No final rule found.** | **No** directly: BSA program duties do not reach a charity (REG-038). Relevant to banks and MSB providers (REG-043) and as a signal of supervisory posture | [independent/regulatory] (LS-057) |
| **2018 Joint Statement on Innovative Efforts to Combat ML/TF** (FRB, FDIC, FinCEN, NCUA, OCC; 2018-12-03) | Supports banks piloting innovative approaches. Cited by the 2026 NPRM as "longstanding guidance" | Indirectly (banks) | [independent/regulatory] (LS-058; cited in LS-057, not separately read) |
| **SR 11-7 / OCC 2011-12 model risk guidance → replaced 2026-04-17** (OCC Bulletin 2026-13; Fed SR 26-2 per secondary sources) | - Rescinds OCC 2011-12, OCC 2021-19 (the 2021 BSA/AML model-risk statement) and the Comptroller's Handbook booklet.<br>- **"Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance."**<br>- Not enforceable.<br>- SR 11-7 itself appears only in a footnote of the OCC bulletin. Its rescission is reported by law firms [secondary]. | No (bank guidance). Useful as a voluntary control template, but it leaves GenAI uncovered | [independent/regulatory] (LS-059, LS-060); [secondary] |
| **NIST AI RMF 1.0** (AI 100-1) and **GenAI Profile** (AI 600-1, July 2024) | Voluntary. 12 GenAI risks including confabulation, information integrity, information security, data privacy and human-AI configuration | Voluntary baseline | [independent/regulatory] (LS-061, LS-062) |
| **FATF R8** (revised 2023-11-16) | "focused, proportionate and risk-based measures". Targets "misapplication" that led to overly broad measures and the "undue disruption or discouragement of legitimate charitable activities". NPOs need not be obliged entities | Binds countries; useful to push back on bank or partner over-screening (REG-040) | [independent/regulatory] (LS-063) |
| **FinCEN Notice FIN-2026-NTC2** (2026-10-30), key term "FIN2026NPO" | - "the vast majority of U.S.-based NPOs present a low risk ... the U.S. government does not view the NPO sector as a whole as presenting a uniform or unacceptably high risk".<br>- Asks banks to evaluate "each NPO individually".<br>- Cites 2025–2026 designations, including domestic "violent far-left" networks and Antifa-related groups, alongside Hamas-linked "sham charity" actions | Addressed to financial institutions. For sponsors it widens the set of designated parties a domestic grantee screen can hit, which raises the stakes of adverse-media and affiliation judgments | [independent/regulatory] (LS-064) |
| **2020 Joint Fact Sheet on BSA due diligence for charities** | Charities are not uniformly high risk | Indirect | [repo V] (REG-038; cited in LS-064) |
| **Rev. Proc. 2018-32 §8.01** | Reliance on IRS listings or third-party BMF data requires a retained, time-stamped copy with the BMF revision date | Yes (REG-019). An AI paraphrase of status is not a reliance record | [repo V] (LS-066) |
| **Equivalency determination / ER** (Treas. Reg. 53.4945-5; Notice 2006-109; 2023 proposed §4966 regulations) | Good-faith determination, which may rest on a qualified tax practitioner's written advice. For DAFs this rests on interim guidance | Yes; a human judgment (REG-020) | [repo V] |
| **Colorado** | SB 24-205 was repealed and replaced by the ADMT Act (SB 26-189), signed 2026-05-14 and effective 2027-01-01. It covers consumer "consequential decisions" in listed domains. Grant decisions about organisations are likely outside it | Unlikely (REG-060). Supersedes the repo's earlier "uncertain 2026-06-30" note in LS-010 | [repo V] (LS-067) |
| **No federal AI rule for DAF decisions** | Accountability runs through §4966/4967, OFAC and state AG oversight | (REG-063) | [repo V] |

---

## 5. Documented harms and failure evidence

1. **De-risking of charities by banks.**
   - Charity & Security Network, *Financial Access for U.S. Nonprofits* (February 2017) (LS-068) [NGO report; read summary page]. Two-thirds of U.S. nonprofits working abroad reported financial-access difficulties. 37% reported wire delays, "up to several months"; 15% have problems "constantly or regularly"; one-third saw fee increases; 26% got unusual documentation requests; 42% carried cash when transfers stalled. n=305 according to American Banker [secondary]. Account-closure percentages differ between secondary sources: Devex gives 6% closed and 10% refused, ACAMS ">15%". Not reconciled here.
   - Duke Law International Human Rights Clinic and the Women Peacemakers Program, *Tightening the Purse Strings* (March 2017) (LS-069) [NGO report; snippet]. Survey of about 60 women's rights organisations: 41.67% did not apply for needed funds and 16.67% refused grants they were offered, because of CFT constraints [figures from secondary descriptions].
   - UK Muslim Charities Forum (January 2025) (LS-071) [NGO report; advocacy; n=19; snippet]. 42% had been threatened with account closure, and 42% faced delays or freezes on international transfers. The sample is very small.
   - UN Special Rapporteur Ní Aoláin, A/78/520 (2023-10-10), drawing on the June 2023 Global Study (LS-070) [independent/regulatory; snippet]. Covers counter-terrorism measures that restrict civil society's access to funding. Its de-risking text was not read here.
   - Treasury's own position (2020 Fact Sheet; FinCEN Notice 2026; FATF R8) is that the sector is not uniformly high-risk (LS-063, LS-064).
   - **No source attributes a specific de-risking case to an AI or ML screening system.** The harm documented is from rules-based and judgment-based over-screening.
2. **False sanctions hits and missed true matches.**
   - Name-matching false positives are endemic: LSEG's 2025 survey says 75% report "excessive false positives" from legacy systems (LS-043) [vendor survey; snippet].
   - The opposite failure is priced in the repo. In Amex 2022, one "high confidence" alert was "erroneously closed", followed by 214 violations and a $430,500 penalty (LS-009) [repo V].
   - No OFAC penalty against a charity, foundation, DAF sponsor or donor platform was found for 2021–2026 (LS-009) [repo V].
3. **Algorithmic or ratings bias.**
   - The 2013 "Overhead Myth" letter, from the CEOs of GuideStar, Charity Navigator and BBB Wise Giving Alliance, rejected the overhead ratio "as the sole measure of nonprofit performance" (LS-072) [NGO report].
   - Coverage bias is structural. CN rates about 17% of Pub 78 records and excludes 990-EZ and 990-N filers and churches. In the repo's top-50 Schedule I screen, $1.19bn of church-labelled grant dollars are in neither Pub 78 nor the BMF (LS-008) [repo V].
   - An AI ranker trained on rated or 990-rich organisations would inherit this skew [inference].
   - No published audit of bias in AI charity ranking was found.
4. **Prompt injection in agents that read web content.**
   - OWASP LLM01:2025 defines indirect prompt injection from "external sources, such as websites or files" (LS-073) [independent/regulatory: standards body].
   - Demonstrated attacks:
     - Greshake et al. 2023, indirect injection through retrieved content (LS-074) [preprint].
     - AgentDojo: attacks succeed against the best agents in <25% of cases, falling to 8% with a detector defence. Adaptive attackers do better, per later reports (LS-075) [preprint].
     - EchoLeak (CVE-2025-32711): a zero-click prompt injection in Microsoft 365 Copilot (LS-076) [secondary].
   - No attack on a charity-vetting system has been reported. Charity websites, bylaws, purpose fields and biographies are attacker-writable inputs (LS-010, LS-050).
5. **Confabulation risk in AI-generated charity descriptions.** Candid has a blog on "what generative AI says about your nonprofit" and minimising misrepresentation (LS-085) [vendor claim; snippet]. Charity Navigator's AI search tells users to "double-check for accuracy" (LS-026).

---

## 6. Funders using AI in grant review

| Item | Figure or position | Class |
|---|---|---|
| Candid 2025 Foundation Giving Forecast Survey (published 2025-11-20) | Currently use generative AI "to screen applicants or help make decisions about whom to fund": Yes 1%, No 97%, Don't know 2% (n=529). Next few years: Yes 3%, Maybe 19%, No 66% (text says 65%), Don't know 12% (n=528). Leans to larger foundations | [survey: n=529, 2025] (LS-024) |
| CEP, *AI With Purpose* (2025-09-30) | "the majority" of foundation and nonprofit leaders use AI, mainly for internal productivity and communications. 90% of foundations offer grantees no AI support. Report tables cite n=129 foundations and n=279 nonprofits [snippet]. No grant-review-specific figure in the summary read | [survey: n≈129 foundations / 279 nonprofits, 2025] (LS-077) |
| Secondary report of a CEP survey | 81% of foundations report some AI use, but 4% use it "systematically". Attributed to a CEP survey of 215 foundation leaders | [secondary; snippet; not verified] (LS-077) |
| MacArthur AI policy (adopted 2023-12-18; revisions 2025-06-02 and July 2026; approved 2026-09-23) | Unacceptable: "Using AI for grantmaking decisions or evaluation". Grantee financial information is "sensitive"; confidential data needs General Counsel pre-approval | [independent/regulatory: funder policy, read] (LS-078) |
| Guggenheim Foundation; Jerome Foundation | Bar AI in panel review, or bar entering applications into AI tools | [secondary; snippet] (LS-079) |
| Kauffman; Lever for Change | Kauffman adopted ChatGPT Enterprise and an AI policy. Lever for Change discloses its AI stance to applicants | [secondary; snippet] (LS-080) |
| PJMF Grant Guardian | 189 organisations "supported" (2025-07-22) | [vendor claim] (LS-039) |
| Benevity Grant Summaries | >30% of grantmaking clients in week one; >500 clients (with Match Assurance) by June 2026 | [vendor claim] (LS-032, LS-033) |
| Foundation Source (sponsor platform) | Roadmap: AI to "surface the strongest candidates for review" for scholarships | [repo V] (LS-005) |
| Hewlett, Gates, Ford | No published AI-in-grant-review policy was found in this pass | Not evidenced |

---

## 7. AI capability claimed vs evidenced, by provider

| Provider | Claimed AI capability | Evidenced to work? | Evidence of human or flag-only control | Overall |
|---|---|---|---|---|
| Candid | Search, LOI drafting, distress signals, MCP data feed | No accuracy data. Distress flags self-described as imperfect | Not applicable (inform-only) | Claimed, inform-only |
| Charity Navigator | AI search and recommendations | No; "double-check for accuracy" | — | Claimed, beta |
| NGOsource | None | — | Human ED process | None |
| Goodstack | AI-assisted global verification, sanctions and adverse media | No metrics | Not documented | Claimed |
| TechSoup | "enterprise AI", fraud defence | No | Not documented | Claimed, vague |
| Benevity | Grant summaries and scoring; match-receipt AI | Adoption only. The decline-rate figure is for matching, from one partner | "administrators retain full decision-making control" | Claimed plus adoption |
| GlobalGiving, CAF America, PayPal Giving Fund | None in vetting | — | Human-led | None |
| SmartSimple, Fluxx, YourCause | Summaries, scoring, risk flags | No accuracy data | Yes, documented flag-only / human decision | Controls evidenced; accuracy not |
| Submittable | Automated scoring and extraction | No | Marketing only | Claimed |
| Grant Guardian | Financial scoring from 990s and audits | One testimonial on time saved; no accuracy data | "human in-the-loop at key steps" | Claimed plus adoption |
| LSEG, Ripjar, Shield and other screening vendors | 74–98% false-positive reduction | Vendor testing only | Shield markets **autonomous** closure | Claimed |
| Research (Fed FEDS, OpenSanctions Pairs) | LLM name matching | **Yes, in controlled tests**, on non-charity data | Cascade and human review recommended | Strongest evidence, but off-domain |

---

## 8. What is NOT publicly evidenced

1. No DAF sponsor documents AI in eligibility determination, grant approval or sanctions disposition (LS-005, LS-006) [repo V]. Confirmed by absence in this pass.
2. **No accuracy, false-positive, false-negative or override metrics for any AI feature used in charity vetting or grant review**, from Candid, CN, Goodstack, Benevity, the grantmaking software vendors or Grant Guardian.
3. **No independent audit of any screening vendor's false-positive reduction claim.** A FairPlay/Axle evaluation (LS-046) exists but was not read.
4. **No study of LLM accuracy on Form 990 or 990-EZ extraction**, or on nonprofit audits, bylaws or foreign registration documents.
5. No AI in equivalency determinations: NGOsource and CAF America show none.
6. No bias audit of AI charity search or ranking. No study of how AI affects funding for small, faith-based or foreign organisations.
7. No documented prompt-injection incident against a philanthropy system. The risk is inferred from general demonstrations.
8. No case linking a specific de-risking or wrongful-denial event to an AI or ML screening model.
9. No final FinCEN AML/CFT program rule. No regulator guidance specific to charities on AI screening.
10. No sanctions-screening benchmark specific to charities or DAFs. The public benchmarks (OpenSanctions Pairs, KYBench) cover sanctions/OSINT entities and businesses.

---

## 9. Implications for a DAF sponsor's vetting design [inference unless tagged]

### 9.1 Where AI has evidence of helping, and how to use it

| Task | Evidence | Recommended role | Legal anchor |
|---|---|---|---|
| **Sanctions alert triage and name disambiguation** (grantees, key persons, foreign payees) | Strongest available: LS-048, LS-049 [preprint], plus vendor claims | Cascade: deterministic list match → documented threshold rules → LLM *ranking and evidence packet* for the analyst. An LLM may **lower queue priority** but not close an alert. Seed known true matches in regression tests | REG-036, REG-037 (10-year logs of list version, score, disposition, reviewer) |
| **Adverse-media triage** | Weak to moderate: KYBench [preprint, vendor], plus practitioner notes | Retrieval plus summary with source links and an evidence grade. Separate "allegation" from "finding" (Batch 2C G18). Never an automatic denial | REG-055 (discretion reviewed by AGs); FATF R8 proportionality (REG-040) |
| **Document extraction and summary** (990s, audits, foreign bylaws, ED files) | Adoption only (Grant Guardian, Benevity, SmartSimple) | Extract into a schema with span-level citations; checks against reported totals in the style of LS-053; human verifies material fields | REG-002, REG-020 (ED/ER judgment is human) |
| **Purpose and private-benefit flagging** | No direct evidence; consistent with the repo's add-only rule (LS-010) | Add flags with reasons; never remove a rule-based flag | REG-003, REG-004 |
| **Intake disambiguation** (donor names a charity) | General entity-resolution evidence | Suggest EIN or legal-entity matches **for donor confirmation** | REG-019 (status still from a retained IRS snapshot) |

### 9.2 Where AI is risky or brings no benefit

- **Eligibility determination itself.** IRS Pub 78, BMF and Auto-Revocation data plus OFAC are deterministic and reliance-grade only as a retained snapshot (REG-019). An LLM paraphrase adds error and no information (LS-010 F01) [repo V].
- **Clearing sanctions alerts with an LLM.** Vendors now market autonomous alert closure (Shield, LS-045). No independent validation exists. The Amex case prices one wrongly closed true match at $430,500 plus 214 violations (LS-009).
- **Ranking with licensed ratings.** CN and Candid terms bar using their data in calculations or as AI/ML inputs without consent (LS-007).
- **Agents reading charity web content while holding tools.** OWASP LLM01; the OpenSanctions warning about planted biography injections. Keep the repo's rule: document-reading steps get no tools, and tool-using steps get no untrusted text (LS-010; agent-architecture, LS-012).
- **Adverse media at scale without calibration.** It reproduces de-risking harm: wrongful holds of Muslim, international, small and church grantees (LS-068, LS-071; Batch 2C H5 and fairness metrics). The October 2026 FinCEN notice adds domestic politically designated groups to what screening can hit. That raises the risk of affiliation-by-association false positives for advocacy grantees, so human review of any such hit is essential.

### 9.3 Legal and governance constraints to design around

1. **The sponsor signs.** §4966 and §4967 penalties attach to the sponsor and to managers who knowingly agree. AI produces evidence; a named human approves (REG-001, REG-003; LS-010).
2. **The flag-only rule for sanctions needs one clarification.** REG-036 allows that "automation may clear obvious false positives under a documented rule" and must not close a high-score match. The failure-modes register (LS-010) says AI "may add a flag, never clear one". These are consistent if "automation" means **deterministic, documented, tested rules** and "AI" means **probabilistic models**. Adopt that reading explicitly: rules may clear below-threshold false positives under a documented and audited rule, and LLMs may rank, explain and add, but not dispose.
3. **Records.** A 10-year OFAC log (REG-037). A Rev. Proc. 2018-32 status snapshot per grant (REG-019). Model and prompt version on each AI-assisted record (LS-010 F07, F13).
4. **No banking-style safe harbour.** FinCEN's 2026 "responsible innovation" language binds BSA institutions, not a charity sponsor (REG-038). A sponsor's protection is a documented, risk-based program under the OFAC Framework (LS-056). Bank partners may still ask how an AI screen is governed.
5. **Model risk.** No current U.S. supervisory guidance covers GenAI model risk: the 2026 interagency guidance excludes it (LS-059). Use NIST AI RMF and AI 600-1 as the voluntary baseline (LS-061, LS-062). Validate on public benchmarks (LS-049, LS-052) plus the synthetic cases in Batch 2C.
6. **Proportionality.** FATF R8 (2023) and FinCEN's 2026 notice support risk-based, individual assessment. Use them to resist one-size-fits-all screening thresholds imposed by partners (REG-040).
7. **Colorado ADMT** (effective 2027-01-01) is unlikely to reach organisational grant decisions. It may reach decisions about Colorado donors' accounts. Ask counsel (REG-060).

---

## 10. Where this file updates or contradicts the repository

1. **Benevity "30%→<3%" (LS-010 F02).** The repo uses it as evidence that "decline rates are material and movable" for false declines and holds. The source measures **employee match-request declines** under Match Assurance, and Benevity's blog attributes it to one partner (LS-032, LS-035). It is not evidence about charity-vetting decline rates. Re-label it in F02.
2. **Model-risk baseline.** SR 11-7 and OCC 2011-12 were replaced on 2026-04-17 (OCC Bulletin 2026-13). The 2021 BSA/AML model-risk statement was rescinded, and generative and agentic AI are excluded from scope (LS-059). Any repo text that assumes SR 11-7 as the model-risk template should change. No repo file currently cites SR 11-7.
3. **FinCEN program rule.** The 2024 Program NPRM is withdrawn and superseded by the 2026-04-10 NPRM (RIN 1506-AB72). It is still not final (LS-057). The repo does not yet record this.
4. **"No golden datasets exist publicly"** (agent-architecture §3, LS-012). That holds for DAF vetting. But public benchmarks now exist for sanctions entity matching (OpenSanctions Pairs, 755,540 labelled pairs, LS-049) and for adverse-media agents (KYBench, LS-052). They can seed the sanctions and adverse-media golden sets.
5. **FinCEN Notice FIN-2026-NTC2 (2026-10-30)** is new to the repo. It reaffirms REG-038 and REG-039 (NPO sector low-risk; individual evaluation). It also lists new domestic designations, which widen the screening scope for domestic grantees.
6. **Colorado.** LS-010 §2 still says "uncertain 2026-06-30". REG-060 (SB 26-189, effective 2027-01-01) already supersedes it inside the repo. Flagged for consistency.
7. **Consistent with the repo:** no sponsor-side AI in approval or eligibility (1% of foundations in Candid's survey; MacArthur's ban); Candid and CN AI is inform-only; grantmaking software has documented flag-only controls; licence limits on using ratings in AI.

---

## 11. Limits

- Many vendor facts come from search snippets only. The CSV `limitation` column flags each one.
- Figures for KYBench, LSEG and other vendors could not be checked against underlying data. Some model names in KYBench (for example "GPT-6 Astra") could not be verified.
- The Fed working paper's test-set composition was not read; only the abstract page was.
- Several NGO reports (C&SN, Duke/WPP, Muslim Charities Forum, A/78/520) were read only as summary pages or snippets. Their full methods were not reviewed.
- No product was tested. No claim here is a performance ranking.
