# Direction P-NEW-SEC-01: giving-technology patents (2021+) and security incidents affecting DAF sponsors, administrators and vendors

**Date:** 2026-11-15 · **Queue item:** P-NEW-SEC-01 (new direction from the owner)

**Outputs**
- [`data/mission-2026-11-14/giving-tech-patents-2021plus.csv`](../../data/mission-2026-11-14/giving-tech-patents-2021plus.csv): 146 publications from 2021 or later (80 US), with relevance tiers A/B/C and claim-theme tags.
- [`data/mission-2026-11-14/daf-security-incidents-2021plus.csv`](../../data/mission-2026-11-14/daf-security-incidents-2021plus.csv): 21 incident or enforcement rows (SI-01..SI-21).
- [`data/mission-2026-11-14/queue-proposals-batch39-n2.csv`](../../data/mission-2026-11-14/queue-proposals-batch39-n2.csv): P-B39N2-01..03.

**Rules applied**
- **Read first:**
  - [ai-governance-failure-modes.md](ai-governance-failure-modes.md), with its wave-2A correction 17: the failure-mode counts are rubric ratings, with no observed DAF AI incidents.
  - [private-equity-daf-ecosystem-map.md](private-equity-daf-ecosystem-map.md) and [firms-interested-in-daf-organizations.md](firms-interested-in-daf-organizations.md), with their governing wave-4/7/8/22 corrections.
  - [quadrant-A1-rationale.md](quadrant-A1-rationale.md), which uses Blackbaud breach notices.
  - None of those corrections touches the facts used here.
- **Recency:** every patent row was published in 2021 or later. Every incident row has an incident, disclosure or enforcement date in 2021 or later. The 2020 Blackbaud incident and Morgan Stanley's 2015–2020 disposal conduct appear only because their enforcement actions fall in 2022–2024.
- **robots.txt and access** (details in §5):
  - **Read and respected:** robots.txt was read on every host before fetching.
  - **Not fetched:**
    - crt.sh (excluded by instruction);
    - maine.gov and apps.web.maine.gov (robots.txt unreadable: CloudFront 403 and 404);
    - mass.gov (403);
    - Lens.org (AI agents disallowed);
    - Google Patents search pages (`Disallow: /*`, only `/patent/` allowed);
    - Justia and image-ppubs.uspto.gov (Cloudflare or 403; not circumvented).
  - **Not used:** search.patentsview.org was blocked at the network proxy. The USPTO Open Data Portal API needs a registered key, which this task could not obtain because logins are not allowed.
- **Personal data:** none reproduced. Individual inventors appear as "(individual inventor; name omitted)", and breach rows give organisations, dates and counts only.
- **No outreach, logins or forms.**
- **Labels:**
  - **[F]** primary document;
  - **[S]** secondary report;
  - **[C]** computed from the CSVs;
  - **[I]** inference;
  - **[U]** not found.
- **The patent sections are research, not a legal opinion or a freedom-to-operate clearance.**

---

## 0. Answers in brief

| Question | Answer | Confidence |
|---|---|---|
| **Do named DAF incumbents hold 2021+ giving patents?** | **None found.** [C] Of the incumbents named in the brief, only TIFIN appears, and its patent is the giving-agnostic *Machine learning data anonymizer*, US12705394B2 (2026-08-11). No giving patent or application from 2021 or later was found for FMR/Fidelity, Schwab, Vanguard, Ren, Chariot, Daffy, Benevity, Blackbaud, Bonterra or PayPal. This is **absence in a citation crawl plus targeted web searches, not a clearance search** (§2.4). | Medium–low |
| **Who does patent giving technology?** | **Payments and card networks, and small specialists.** [C] Tier A/B (DAF-adjacent or core-function) assignees:<br>- **Card, bank and payment networks:** Mastercard, Block, Capital One, Wells Fargo, Early Warning (Zelle), IBM, ADP.<br>- **Brokerage:** Morgan Stanley, whose US20220292603A1 is abandoned per Google Patents.<br>- **Specialists:** Change Up, Gravvy, Idonate, Everest Effect, Impact Ventures, Kindmatch, Boodle, Olive Seed.<br>A long tail of CN/KR blockchain-donation filings sits in tier C. | Medium |
| **Claim themes** | [C] Tags across the 146 rows:<br>- payments or accounts: 91;<br>- blockchain or crypto: 48;<br>- rewards or merchant: 46;<br>- eligibility, verification or fraud: 29;<br>- AI/ML: 11.<br>The **AI claims are narrow and specific**:<br>- an NL-embedding match of a charity to article text (Mastercard US12136112B2);<br>- an ML-suggested charity project inside payroll self-service (ADP US11443391B2);<br>- PII pseudonymisation before a third-party LLM call (TIFIN US12705394B2). | Medium (tags are keyword-based) |
| **FTO implication for an AI-native entrant** | [I] No incumbent wall was found around DAF-specific workflows. The live exposure is narrower:<br>- **(a)** specific claim language on charity matching by embeddings, ML project suggestion and PII pseudonymisation for LLMs;<br>- **(b)** pooled-account allocation (Gravvy, pending);<br>- **(c)** payment-rail claims held by Early Warning, Block and Mastercard.<br>Design-arounds look feasible, but a counsel-led search is needed before launch. | Low–medium |
| **SEC Item 1.05 8-Ks** | **None by a DAF sponsor parent or vendor.** [F] 19 DAF-linked public companies were screened from 2023-12-18 to 2026-11-15. The only Item 1.05 filing is **Coinbase** (2025-05-15; estimated cost $180–400m), an adjacent crypto-donation rail. | Medium–high |
| **Biggest regulatory event** | **Blackbaud's 2020 ransomware**, which led to four resolutions:<br>- SEC $3m (2023-03-09);<br>- 49 AGs + DC $49.5m (2023-10-05);<br>- FTC order (final 2024-05-20, no money);<br>- California $6.75m (2024-06-13).<br>[F] Blackbaud's FY2025 10-K shows $3.1m of incident costs in 2025 and $13.7m in 2024, with two subrogation suits still open. | High |
| **Incidents at DAF-sponsor parents and distributors (2021+)** | [F] notices / [S] counts:<br>- Vanguard: 2026-07, notified 2026-11-11. National count not established; state registers give 94 VT residents (2026-11-04) and 1,224 MA residents (2026-11-12) [V wave 43C];<br>- Ameriprise (RCF white label): 2026-03, 47,876 (secondary, Maine-sourced, unverified; registers give 83 VT and 2,216 MA, both 2026-04-17) [V wave 43C];<br>- Fidelity Investments: 2024-08, 77,099 (secondary, Maine-sourced, unverified; MA register gives 2,768, 2024-10-09) [V wave 43C];<br>- Fidelity Life via Infosys McCamish: 2023-10;<br>- Bank of America via McCamish: 2023-11, 57,028;<br>- TD Ameritrade/Schwab via MOVEit: 2023-05;<br>- Schwab: 2021-22;<br>- PayPal: 2022-12, 34,942, plus NYDFS $2m in 2025-01;<br>- Morgan Stanley: vendor incident 2021, plus SEC $35m in 2022 (~15m customers, disposal).<br>**No notice names a DAF sponsor entity.** | Notices high; counts medium |
| **DAF administrators and giving vendors** | **No breach notice found** for any DAF recordkeeper (Ren, NPact, Foundant, Foundation Source) or for Chariot, Daffy, Benevity, Bonterra, Every.org or Endaoment. [U] Adjacent cases:<br>- **Planned-giving administrator:** TIAA Kaspick via the PBI/MOVEit breach (2023), 27,946 [S] affected.<br>- **Donor CRMs:** DonorPerfect (2024-02) and DonorView (948,029 records exposed, 2023-12).<br>- **Operational, not security:** Benevity's 2025-06-17 deactivation of ~108,000 private non-operating nonprofits through an IRS-data configuration error. [F] | Medium |

---

## 1. How the work was done

1. **Patents.** Snowball citation crawl on Google Patents publication pages (the only path robots.txt allows):
   - **Seeds:** nine on-topic documents (e.g. US20130151433A1 *System and method for charitable giving*, US7593881B2, US11544749B2, US11443391B2, WO2023012530A1), plus eleven more found by web search restricted to patents.google.com.
   - **Expansion:** forward citations ("cited by", original and family) and "similar documents" with a giving-related title (donat/charit/philanthrop/giving/donor/nonprofit/fundrais/crowdfund/grant/cause). Pre-2021 documents were expanded only as bridges.
   - **Output:** ~350 pages parsed at 1.5 s per request; 188 publications from 2021 or later. After removing blood, plasma, milk, food, goods, vehicle, venue and political-fundraising titles, **145** remain.
   - **Added:** TIFIN's US12705394B2, found by web search.
   - **Fields:** claim 1, status and assignee as shown by Google Patents. Status is Google's label, not a USPTO legal-status check.
2. **Claim themes** are regex tags on title + abstract + claim 1 (dictionary in §4.1). **Tiers A/B** were assigned by hand after reading claim 1 (§2.2).
3. **Security.**
   - **California AG register:** the full export (`/privacy/databreach/list-export`, 5,440 rows) was searched for sponsors, parents, vendors and any organisation name containing foundation, charity, philanthropy, giving or donor (2021+). Sample notices were read for vector and dates; no personal data was copied.
   - **SEC EDGAR:** the submissions JSON gave the 8-K item codes for 19 DAF-linked issuers. Full-text search was run for "cybersecurity incident" 8-Ks at the six largest banks and brokers, whose submissions pages did not reach back to 2023.
   - **Enforcement:** primary releases from the SEC, FTC, the Minnesota and California AGs, and NYDFS (NYDFS URL from the search index only).
   - **Vendor pages:** Benevity status page; Blackbaud FY2025 10-K.
   - **Secondary sources:** used for counts that sit on blocked registers (Maine, Massachusetts) and labelled [S].

---

## 2. Patents (question 1)

### 2.1 Shape of the set [C]
- **Size:** 146 publications.
  - **By jurisdiction:** US 80, CN 32, KR 15, WO 8, JP 6, other 5.
  - **By year:** 2021: 27; 2022: 34; 2023: 31; 2024: 27; 2025: 19; 2026: 8. Later years are under-represented because citations lag.
- **US status per Google Patents:**
  - Active 36;
  - Abandoned 24;
  - Pending 12;
  - "Granted" (an A1 whose application later issued) 8.
- **Tiers:**
  - **A (DAF-adjacent account and grant structures):** 10;
  - **B (core functions an entrant would build: matching, verification, fraud, real-time payment, employer match, PII handling for AI):** 20;
  - **C (other giving technology):** 116, mostly merchant round-up, loyalty, blockchain tracking and crowdfunding.

### 2.2 Tier A and selected tier B [F: claim 1 read on Google Patents]

| Publication | Assignee | Status | What claim 1 covers (paraphrase) | Why it matters to a DAF entrant |
|---|---|---|---|---|
| [US20230237461A1](https://patents.google.com/patent/US20230237461A1/en) / [US20250252422A1](https://patents.google.com/patent/US20250252422A1/en) | Gravvy Inc | Abandoned / **Pending** | Several users deposit into a **shared donation funding account**. Each user has an allocation profile naming recipients and a share of the fund, and acknowledgments are generated automatically | Closest DAF-like structure in the set (pooled giving account + per-user advice + receipts) [I] |
| [US20220292603A1](https://patents.google.com/patent/US20220292603A1/en) | Morgan Stanley Services Group | Abandoned | A portfolio-optimiser network selects **non-cash assets from a donor's investment account** and transfers them to recipients on a recurring basis | Appreciated-stock contribution automation, a core DAF intake flow; abandoned, so no claim survives [I] |
| [US11544749B2](https://patents.google.com/patent/US11544749B2/en), [US11556965B2](https://patents.google.com/patent/US11556965B2/en), [US10991015B2](https://patents.google.com/patent/US10991015B2/en) (+ apps) | Change Up Inc | Active | Purchase-triggered provider contributions to a **user-selected portfolio of charities** | Portfolio-of-charities UX; merchant-funded, not donor-funded |
| [US20250299230A1](https://patents.google.com/patent/US20250299230A1/en) | Impact Ventures LLC | Pending | Takes an employee donation from an external donation form, collects the missing data, applies **rules to decide eligibility for a corporate match**, and submits it to the corporate vendor platform | Directly overlaps "DAF grant → employer match" automation |
| [US11443391B2](https://patents.google.com/patent/US11443391B2/en) | ADP Inc | Active | A **machine-learning model suggests charitable projects** from a self-service giving profile; payroll deduction follows | ML-recommendation + payroll; workplace-giving overlap |
| [US12136112B2](https://patents.google.com/patent/US12136112B2/en) | Mastercard | Active | A **pre-trained NL model** turns article text into sentence embeddings, which are compared with charity embeddings to pick the most relevant charity | Embedding-based charity matching, which any LLM-native recommender will resemble [I] |
| [US11893067B1](https://patents.google.com/patent/US11893067B1/en) | Block Inc | Active | Trending topics are mined from a dynamic feed and causes are suggested to a payment-app user | News/trend-driven giving prompts |
| [US20240362641A1](https://patents.google.com/patent/US20240362641A1/en) | Wells Fargo | Pending | A bank system uses third-party account and category data to **mitigate donation fraud** | Fraud screening on outbound charitable payments |
| [US11704704B2](https://patents.google.com/patent/US11704704B2/en) | Early Warning Services | Active | **Real-time donations** between tokenised donor and donee bank accounts | Instant-settlement grant payout rails |
| [US11935096B1](https://patents.google.com/patent/US11935096B1/en) | Idonate LLC | Active | An embeddable form captures "non-profit layer" metadata (fund designation, anonymity preference, tribute, campaign) with the payment token | Grant-purpose and anonymity metadata, as in DAFpay-type flows |
| [US12008605B2](https://patents.google.com/patent/US12008605B2/en) | IBM | Active | P2P donation with biometric donee authentication and transient accounts | Verification of individuals (not charities) |
| [US20210398179A1](https://patents.google.com/patent/US20210398179A1/en) | Everest Effect Inc | Pending | Disaster-event donor–donee matching with **donee validation and needs verification** | Verification of individuals; DAFs cannot grant to individuals (IRC 4966) |
| [US12705394B2](https://patents.google.com/patent/US12705394B2/en) | Tifin Group LLC (TIFIN Give's group) | Active (2026-08-11; priority 2024-06-26) | Sensitive entities are replaced with context-retaining placeholders before a **third-party ML/LLM call**, then mapped back | Generic LLM privacy pattern; any AI-native sponsor sending donor data to a model provider uses something similar [I] |

### 2.3 Claim themes [C]
- **Payments dominate.** 91 of 146 rows touch payment or account flows. Card networks, banks and payment apps patent the moment of giving (round-up, loyalty points, real-time rails), not the DAF ledger.
- **Eligibility and verification** (29 rows) mostly means verifying **individual** donees, blockchain traceability or fraud flags. **No row claims IRS Pub 78/BMF lookup, OFAC screening or 4966 supporting-organisation classification for a sponsor.** [C/I] This matches the governance finding that eligibility should be a deterministic lookup (F01), which is also hard to patent.
- **AI is thin:** 11 rows. Eight of the eleven are US. None claims LLM-generated grant recommendations from a DAF balance, agentic grant submission, or AI review of grant purpose (prohibited-benefit screening). [C/U]
- **Blockchain/crypto** (48) is mostly CN/KR university and bank filings for public-welfare donation tracing, with little US enforcement relevance. [I]

### 2.4 What was not established
- **Assignee-level negatives are weak.** Targeted web searches limited to patents.google.com and Justia found:
  - **Benevity:** nothing.
  - **Blackbaud:** only pre-2021 abandoned applications (e.g. US20050065809A1).
  - **PayPal:** pre-2021 donation patents (e.g. US8050987B2).
  - **FMR, Schwab, Vanguard, Chariot, Daffy:** nothing giving-related.

  None of this is a complete assignee search (see P-B39N2-01).
- **Unopened lead:** US 12,561,720, *Cryptographically attested, continuously self learning impact rating system for charitable organizations*, appeared as a USPTO PDF in search results. It could not be opened (Google Patents had no page; ppubs gave 403 and truncated downloads). It is not in the CSV. Assignee and claims: [U].
- **Not checked:**
  - **Unpublished applications:** applications filed in the last 18 months are not yet published.
  - **Trade secrets:** not covered by any patent search.
  - **Design patents:** not covered.
  - **Non-US equivalents** of US filings.

### 2.5 Freedom-to-operate reading for an AI-native entrant (research, not legal opinion) [I]
1. **No incumbent patent moat was observed.** The DAF incumbents compete on custody, brand and distribution, not patents. The one incumbent-group patent (TIFIN) is a generic LLM-privacy technique.
2. **Claim-level hazards to design around:**
   - **(a)** Embedding-similarity charity matching to content (Mastercard), which is narrow because it is tied to article text and a sentence tokenizer.
   - **(b)** ML project suggestion inside payroll (ADP).
   - **(c)** Pseudonymise → LLM → re-identify (TIFIN). Alternatives are data minimisation, on-premise models, or field-level redaction without a re-identification mapping.
   - **(d)** Rule-based employer-match eligibility with auto-submission (Impact Ventures, pending).
   - **(e)** Pooled account with per-user allocation profiles (Gravvy, pending). Watch its prosecution.
3. **Payment rails are licensed, not designed around.** Real-time donation (Early Warning) and tokenised flows are reached through the rail operator's commercial terms.
4. **Before launch:** counsel-led search of US grants and applications, then claim charts against the four or five closest active claims above. Monitor Gravvy and Impact Ventures continuations.

---

## 3. Security incidents (question 2)

### 3.1 SEC Item 1.05 (material cybersecurity incident 8-Ks) [F]
- **Rule:** the SEC adopted the rule on 2023-07-26 ([SEC 2023-139](https://www.sec.gov/newsroom/press-releases/2023-139)). Item 1.05 is due four business days after a materiality determination, with 8-K compliance from 2023-12-18.
- **Screen:** EDGAR item codes from 2023-12-18 to 2026-11-15 for 19 DAF-linked issuers:
  - Blackbaud, PayPal, Schwab, Envestnet, Morgan Stanley, LPL, Raymond James, Ameriprise, Goldman Sachs, Shift4, Stifel;
  - Bank of America, Wells Fargo, JPMorgan, Northern Trust, BNY, Fiserv, BlackRock, Coinbase.
- **Result:** the only Item 1.05 filing is **Coinbase**, 8-K filed 2025-05-15 ([8-K](https://www.sec.gov/Archives/edgar/data/1679788/000167978825000094/coin-20250514.htm)):
  - support contractors were bribed to take customer data;
  - the attacker demanded an extortion payment;
  - preliminary cost was estimated at **$180–400m**.
- **Coverage gap:** the large private DAF players are outside the 8-K regime entirely (Fidelity/FMR, Vanguard, Ren, Benevity, Bonterra, Daffy, Chariot, TIFIN). For them, state breach registers and FTC/AG actions are the only public channel.
- **Second regime:** amended Reg S-P (adopted 2024-05-16, [SEC 2024-58](https://www.sec.gov/newsroom/press-releases/2024-58)) requires customer notice within 30 days. It applies to the broker-dealer and RIA affiliates that distribute DAFs, not to the 501(c)(3) sponsors. [I]

### 3.2 Blackbaud: the reference enforcement case [F]

| Date | Body | Outcome | Source |
|---|---|---|---|
| 2023-03-09 | SEC | $3m civil penalty. Disclosures in July/Aug 2020 understated the theft of bank-account and SSN data; >13,000 customers affected | [SEC 2023-48](https://www.sec.gov/newsroom/press-releases/2023-48) |
| 2023-10-05 | 49 state AGs + DC (IN and VT co-led) | $49.5m. Required: full-database encryption, dark-web monitoring, segmentation, patching, pen testing, 7 years of third-party assessments; >400 TB stolen | [Minnesota AG](https://ag.state.mn.us/Office/Communications/2023/10/05_Blackbaud.asp) |
| 2024-05-20 (complaint 2024-02) | FTC | Consent order: delete unneeded data, retention schedule, security programme, notify the FTC of future reportable breaches; "millions of consumers" | [FTC](https://www.ftc.gov/news-events/news/press-releases/2024/05/ftc-finalizes-order-blackbaud-related-allegations-firms-security-failures-led-data-breach) |
| 2024-06-13 | California AG | $6.75m. Final judgment and permanent injunction under CA reasonable-security, UCL and FAL law | [CA AG](https://oag.ca.gov/news/press-releases/attorney-general-bonta-secures-675-million-settlement-against-blackbaud-over) |
| 2026-02-18 | Blackbaud FY2025 10-K | Incident costs: $3.1m in 2025 and $13.7m in 2024. ~260 reimbursement requests and ~400 reservations resolved or inactive; 2 subrogation suits open; class actions resolved | [10-K](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm) |

**Relevance [I]:**
- **Blackbaud's DAF links:** it ran DAF technology until 2011 (sold to Renaissance), sold FIMS/DonorCentral to NPact in 2022, and still sponsors Blackbaud Giving Fund ([competitive-history-timelines.md](competitive-history-timelines.md); [breadth-community-faith-infrastructure-emerging.md](breadth-community-faith-infrastructure-emerging.md)).
- **Community foundations** were among the customers that notified donors in 2020 ([quadrant-A1-rationale.md](quadrant-A1-rationale.md)).
- **The orders set the de facto control baseline** that a sponsor's due diligence can cite for any nonprofit-data vendor.

### 3.3 DAF-sponsor parents, distributors and adjacent vendors (2021+)
See the CSV for every row. Highlights:
- **No notice names a sponsor.** No breach notice in the California register (5,440 rows) names Fidelity Charitable, Schwab Charitable, Vanguard Charitable, NPT, GIFT, RCF, Daffy, Chariot, Benevity, Bonterra or a DAF-sponsoring community foundation. [F/U] Every 2021+ hit is at a **parent or affiliate**. Each sponsor is a legally separate 501(c)(3), but several run on the parent's infrastructure and staff [I]:
  - Vanguard, 2026-07 social engineering ([CA notice](https://oag.ca.gov/ecrime/databreach/reports/sb24-632773));
  - Fidelity Investments, 2024-08 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-593165));
  - Fidelity Life via Infosys McCamish, 2023-10 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-581779));
  - TD Ameritrade/Schwab via MOVEit, 2023-05 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-571503));
  - Schwab chat/email exposure, 2021 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-551924));
  - Morgan Stanley stock-plan vendor, 2021 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-542538));
  - Ameriprise, 2026-03 ([CA](https://oag.ca.gov/ecrime/databreach/reports/sb24-621953)).
- **Third-party vectors dominate** the parent-level incidents:
  - MOVEit (Schwab/TDA, TIAA Kaspick);
  - Infosys McCamish (Fidelity Life, Bank of America);
  - stock-plan vendor (Morgan Stanley);
  - social engineering or insiders (Vanguard, Coinbase);
  - credential stuffing (PayPal).

  This matches failure modes F09 and F16 in [ai-governance-failure-modes.md](ai-governance-failure-modes.md): new processors and credentials, not model behaviour, are the observed attack surface. [I]
- **Enforcement on affiliates:**
  - Morgan Stanley Smith Barney: **SEC $35m**, 2022-09-20, for disposal failures affecting **~15m customers** ([SEC 2022-168](https://www.sec.gov/newsroom/press-releases/2022-168)).
  - PayPal: **NYDFS $2m**, 2025-01-23, over the 2022-12 credential-stuffing exposure of 1099-K data (34,942 accounts [S]) ([NYDFS](https://www.dfs.ny.gov/reports_and_publications/press_releases/pr20250123), URL from the search index; [Hunton summary](https://www.hunton.com/privacy-and-cybersecurity-law-blog/nydfs-fines-paypal-2-million-for-cybersecurity-failures)).
- **Charitable administrators:** TIAA Kaspick (gift-annuity and planned-giving administration) lost participant files at its subcontractor PBI through MOVEit on 2023-05-29/30 ([Idaho AG letter](https://www.ag.idaho.gov/content/uploads/2023/07/7-27-2023-TIAA-Kaspick-LLC.pdf), 150 Idaho residents [F]; 27,946 total [S]). One client, the ACLU Foundation, reported 575 affected donors [S].
- **Donor CRMs:**
  - DonorPerfect hosted-file-storage incident, 2024-02 ([WFMJ](https://www.wfmj.com/story/50476495/fundraising-software-used-by-ysu-foundation-finds-suspicious-activity-affected-donors-notified)) [S];
  - DonorView unprotected database, 948,029 records ([SecurityInfoWatch](https://www.securityinfowatch.com/cybersecurity/press-release/53080665/giving-platform-for-nonprofit-organizations-exposed-donor-records-in-major-data-breach)) [S].
- **Eligibility-data failure (not security):** Benevity's status page records that on 2025-06-17 a stale configuration in an IRS data refresh **deactivated ~108,000 U.S. private non-operating nonprofits for ~30 hours** ([Benevity status](https://status.benevity.org/incidents/3qvv9npt296z)) [F]. This is the first observed public instance of failure modes F01/F02 (eligibility data) at a giving platform. It came from deterministic data plumbing, not AI.

### 3.4 Implications [I]
1. **Trust risk for DAFs sits in shared infrastructure.** For the three largest commercial sponsors, a breach is most likely to surface as a parent-company notice. Whether DAF donor data sits in the affected systems is not disclosed; P-B39N2-02 tests this.
2. **An AI-native entrant has no incident record either way**, so buyers will judge it on controls. The Blackbaud orders offer a ready checklist: encryption of whole databases, segmentation, retention schedules, 7-year assessments and prompt, accurate disclosure. It should be added to the vendor due-diligence questions in [ai-governance-failure-modes.md §5](ai-governance-failure-modes.md) (P-B39N2-03).
3. **The disclosure lesson is about accuracy, not speed.** The SEC case punished an understatement, not lateness. Any sponsor using LLM-drafted incident communications needs a human-verified fact base (F05/F11 analogue).
4. **Vendor concentration is a live risk.** MOVEit and Infosys McCamish each reached several DAF-adjacent firms at once. A sponsor's fourth-party map (vendors' vendors) matters more than its own perimeter.

---

## 4. Data dictionary

### 4.1 `giving-tech-patents-2021plus.csv` (one row per publication)

| Column | Meaning |
|---|---|
| publication_number | Google Patents publication number (kind code included) |
| jurisdiction | First two characters (US, WO, CN, KR, JP, EP, CA, GB, TW, IT, HU) |
| kind | `grant` if the kind code is B/B1/B2/C/T2, else `application` |
| title | Title as shown by Google Patents (English where provided) |
| assignee | Current or original assignee per Google Patents; individuals replaced by "(individual inventor; name omitted)" |
| publication_date, priority_date | ISO dates from the page |
| status_google_patents | Google's legal-status label (Active, Pending, Abandoned, Granted, Ceased, Expired, Withdrawn). Not a USPTO check |
| relevance_tier | A = DAF-adjacent account or grant structure; B = a core function an entrant would build (matching, verification, fraud, real-time payout, employer match, AI privacy); C = other giving technology. A and B are hand-assigned after reading claim 1 |
| claim_themes | Semicolon list of regex tags on title + abstract + claim 1: `ai_ml`, `recommendation_matching`, `payments_accounts`, `eligibility_verification_fraud`, `blockchain_crypto`, `rewards_merchant`, `investment_assets`, `fundraising_crowdfunding`, `privacy_security`. Keyword tags are indicative only |
| claim1_excerpt | First ~400 characters of the claims section |
| notes | Analyst note (tier A/B only) |
| source_url | Google Patents page |
| discovery_method | `citation_crawl` or `web_search_then_patent_page` |

**Exclusions:**
- **By title:** blood, plasma, milk, food, goods, clothing, material, vehicle, venue, bible, auction, advertising, political candidate, activity donation and kiosk titles.
- **Not reached:** 43 crawled 2021+ documents were dropped either by these exclusions or because they were not monetary giving.

### 4.2 `daf-security-incidents-2021plus.csv` (one row per incident or enforcement event)

| Column | Meaning |
|---|---|
| incident_id | SI-01..SI-21 |
| organisation | Entity named in the notice or action |
| role_in_daf_ecosystem | Why it matters to DAFs |
| daf_relevance | `direct_vendor`; `sponsor_parent_affiliate`; `sponsor_platform_affiliate`; `distributor_affiliate`; `adjacent_administrator`; `adjacent_vendor`; `adjacent` |
| event_type | breach_notice(_vendor/_software), enforcement_SEC/FTC/state_AG/state_regulator, issuer_disclosure_10-K, SEC_8-K_Item_1.05, vendor_incident, exposure_misconfiguration, operational_incident |
| incident_dates | As stated in the notice or source |
| disclosure_or_action_date | Register posting, filing or order date |
| records_affected, records_basis | Count and what it counts (customers, accounts, records, residents), with provenance |
| regulator_or_venue | Register or authority |
| penalty_or_cost_usd | Penalty, or disclosed cost, in USD |
| vector | Attack or failure path as described |
| primary_source_url, secondary_source_url | Links |
| evidence_grade | primary / secondary / mixed |
| notes | Caveats |

---

## 5. Source register (accessed 2026-11-15)

**Hosts and robots.txt**

| Host | robots.txt | Used for |
|---|---|---|
| patents.google.com | `Disallow: /*`, `Allow: /patent/` | Publication pages only (~350 fetched, 1.5 s spacing) |
| oag.ca.gov | Standard Drupal disallows; list and export allowed | Breach register export, detail pages, sample notices; press release |
| www.sec.gov, efts.sec.gov, data.sec.gov | /search/ disallowed; Archives allowed; EDGAR APIs used per SEC fair-access policy with a generic User-Agent | 8-K item screen, 10-K, 8-K, press releases |
| ag.state.mn.us | /Consumer/PressRelease/ disallowed; /Office/Communications/ allowed | Multistate settlement |
| www.ag.idaho.gov | `Disallow:` (open) | TIAA Kaspick letter |
| www.ftc.gov | No rules returned | Press release |
| status.benevity.org | Fetched via WebFetch | Incident page |
| maine.gov, apps.web.maine.gov, mass.gov | Unreadable / 403 | **Not fetched**; counts cited from secondary sources. The mass.gov annual PDFs were later read for b39n1-03-b39n2-02-lobbying-and-breaches.md; Maine is still blocked [V wave 43C] |
| patents.justia.com, image-ppubs.uspto.gov, lens.org, search.patentsview.org | Cloudflare / 403 / AI disallowed / proxy-blocked | **Not used** |

**Primary documents:**
- **SEC:** [2023-48](https://www.sec.gov/newsroom/press-releases/2023-48); [2022-168](https://www.sec.gov/newsroom/press-releases/2022-168); [2023-139](https://www.sec.gov/newsroom/press-releases/2023-139); [2024-58](https://www.sec.gov/newsroom/press-releases/2024-58).
- **Company filings:** [Blackbaud FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1280058/000128005826000006/blkb-20251231.htm); [Coinbase 8-K 2025-05-15](https://www.sec.gov/Archives/edgar/data/1679788/000167978825000094/coin-20250514.htm).
- **Enforcement releases:** [FTC Blackbaud](https://www.ftc.gov/news-events/news/press-releases/2024/05/ftc-finalizes-order-blackbaud-related-allegations-firms-security-failures-led-data-breach); [MN AG Blackbaud](https://ag.state.mn.us/Office/Communications/2023/10/05_Blackbaud.asp); [CA AG Blackbaud](https://oag.ca.gov/news/press-releases/attorney-general-bonta-secures-675-million-settlement-against-blackbaud-over); [NYDFS PayPal](https://www.dfs.ny.gov/reports_and_publications/press_releases/pr20250123) (URL from the search index).
- **Breach notices and incident pages:**
  - California AG register: [list export](https://oag.ca.gov/privacy/databreach/list-export) and the detail pages linked in §3.3;
  - [Idaho AG, TIAA Kaspick](https://www.ag.idaho.gov/content/uploads/2023/07/7-27-2023-TIAA-Kaspick-LLC.pdf);
  - [Benevity status](https://status.benevity.org/incidents/3qvv9npt296z).
- **Patents:** Google Patents pages linked in the CSV.

**Secondary (counts and context):**
- **Fidelity, Schwab/TDA:** [InvestmentNews: Fidelity](https://www.investmentnews.com/ria-news/fidelity-reports-data-breach-exposing-77000-customers-personal-data/257642); [InvestmentNews: Schwab/TDA](https://www.investmentnews.com/charles-schwab-announces-td-ameritrade-data-breach-239887).
- **Ameriprise, Vanguard:** [ThinkAdvisor: Ameriprise](https://www.thinkadvisor.com/amp/2026/04/20/ameriprise-data-breach-affected-nearly-48000/); [ThinkAdvisor: Vanguard](https://thinkadvisor.com/2026/11/11/vanguard-faces-class-actions-over-data-breach/) (page returned 403 to WebFetch; figures from search summary).
- **Bank of America, PayPal:** [FinTech Futures: Bank of America](https://www.fintechfutures.com/data-privacy-security/bank-of-america-customers-impacted-by-data-breach-through-infosys-mccamish-systems-hack); [The Record: PayPal](https://therecord.media/paypal-penalty-millions-data-breach); [Hunton: PayPal](https://www.hunton.com/privacy-and-cybersecurity-law-blog/nydfs-fines-paypal-2-million-for-cybersecurity-failures).
- **TIAA/PBI:** [DataBreaches.net](https://www.databreaches.net/teachers-insurance-and-annuity-association-of-america-notifying-2630717-after-pbi-alerts-them-to-moveit-breach).
- **Donor CRMs:** [WFMJ: DonorPerfect](https://www.wfmj.com/story/50476495/fundraising-software-used-by-ysu-foundation-finds-suspicious-activity-affected-donors-notified); [SecurityInfoWatch: DonorView](https://www.securityinfowatch.com/cybersecurity/press-release/53080665/giving-platform-for-nonprofit-organizations-exposed-donor-records-in-major-data-breach).
- **Blackbaud (other AG and secondary):** [Arizona AG](https://www.azag.gov/press-release/attorney-general-mayes-announces-495-million-settlement-software-company-blackbaud); [SecurityWeek](https://www.securityweek.com/blackbaud-settles-with-california-for-6-75-million-over-2020-data-breach/).

---

## 6. Reproduction and limits
- The crawler and parser were scratch scripts (citation BFS over `/patent/` pages; regex parser of `itemprop` fields). They were not committed because the method is described in §1 and the outputs carry their source URLs.
- **Re-running yields different counts**, because Google Patents citation lists change.
- **Status fields are Google's labels.** Abandoned or expired status should be confirmed in USPTO Patent Center before relying on it.

## Validation corrections (wave 24A, 2026-11-15) — governing
Source: [validation-wave24a-report.md](validation-wave24a-report.md); register `data/mission-2026-11-14/validation-register-wave24a.csv`.

1. **§0, DAF administrators row.**
   - **Find:** "**No breach notice found** for any DAF recordkeeper (Ren, NPact, Foundant, Foundation Source)"
   - **Replace with:** "**No 2021+ breach notice found** for any DAF recordkeeper (Ren, NPact, Foundant, Foundation Source). The California register does hold a pre-2021 notice from Renaissance Philanthropic Solutions Group (RenPSG), breach 2018-06-05/13, reported 2018-10-18, outside the recency window [V wave 24A]"
2. **§3.3, first bullet.**
   - **Find:** "Every 2021+ hit is at a **parent or affiliate**."
   - **Replace with:** "Every 2021+ hit is at a **parent or affiliate** (affected counts other than the primary notices are secondary and were not re-verified in wave 24A) [V wave 24A]."
