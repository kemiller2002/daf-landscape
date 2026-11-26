# DAFCP investigation: source and evidence register

**Date:** 2026-11-20. **Machine-readable register:** [`evidence-register.csv`](../../data/dafcp-investigation-2026-11-20/evidence-register.csv), 73 rows, DE001–[DE073]. **Validator:** `python3 -I scripts/dafcp_validate.py .`

## 1. Columns

| Column | Meaning |
|---|---|
| `evidence_id` | [DE001]… |
| `phase` | Investigation phase (1-institution, 1-dafcp, 2-relationships, 3-curriculum, 4-technology, 5-adoption, 5-credentials, 7-reception, reconciliation) |
| `claim` | The exact proposition supported |
| `source_url`, `publisher`, `source_date` | Primary location, publisher and publication date (blank if undated) |
| `observed_on` | Date read (2026-11-20) |
| `excerpt` | A quotation of 40 words or fewer, checked by the validator. No coursework is reproduced |
| `evidence_type` | e.g. programme page, Form 990 XML, statute, accreditor action, search snippet, negative search |
| `tag` | F, R, I, X, S or U (see [00-README](00-README.md)) |
| `epistemic_class` | verified-fact, strongly-supported-inference, working-hypothesis, unsupported-claim, unknown or negative-finding |
| `confidence` | EDF qualitative label |
| `contradictory_evidence`, `uncertainty` | As found |
| `strategic_relevance` | Why the finding matters |
| `checked_by` | The research agent, or `lead re-check 2026-11-20` where the lead re-read the primary source |
| `agent_ref` | Row ID in the agent working files (A/B/C/D/E series) |

## 2. Composition

| Breakdown | Counts |
|---|---|
| Tag | F 63 · R 5 · X 2 · U 2 · S 1 |
| Epistemic class | verified-fact 59 · negative-finding 7 · strongly-supported-inference 6 · working-hypothesis 1 |
| Confidence | High 50 · Medium-High 7 · Medium 15 · Low-Medium 1 |
| Phase | institution 15 · programme 10 · relationships 16 · curriculum 15 · technology 4 · adoption 4 · credentials 4 · reception 3 · reconciliation 2 |
| Distinct source URLs | 49 |

**What the counts show.** The register leans toward verified facts because the investigation concentrated on documented relationships. The decisive *interpretive* claims are in [08](08-clarity-assessment.md) and [09](09-edf-assessment.md), with lower claim states:
- whether sponsors influenced the content;
- whether DAFCP establishes competence;
- how widely it is adopted.

High counts here do not mean high confidence in those interpretations.

## 3. Primary sources the lead re-read directly (2026-11-20)

| Source | Used for |
|---|---|
| [DAFCP programme page](https://www.theamericancollege.edu/learn/professional-designations-certifications/dafcp) | Modules, rules, the 22-name list, no employers printed |
| [DAFCP launch release, 2026-07-30](https://www.theamericancollege.edu/knowledge-hub/press/new-designation-offers-expertise-in-donor-advised-funds) | Launch facts, "more than 20 experts", "critical knowledge gap" |
| [2025 DAF Professional Certificate release, 2025-01-02](https://www.theamericancollege.edu/knowledge-hub/press/new-donor-advised-fund-professional-certificate-program) | Co-development with four sponsors |
| [2025 certificate agenda PDF](https://www.theamericancollege.edu/sites/default/files/DAF-Agenda.pdf) | Sponsor-staff speakers including DAFgiving360's Maestas |
| [DAF Forum "about" page](https://events.theamericancollege.edu/daf-forum/about) | "every general session maps to one of the six sections of the DAFCP curriculum" |
| [MSCHE institution record](https://www.msche.org/institution/0593/) | 2022 probation, 2023 reaffirmation |
| [Charitable Solutions 2026 team page](https://charitablesolutionsllc.com/meet-the-team-2026/) | Six faculty, including the programme director |
| [College welcome release for the programme director](https://www.theamericancollege.edu/knowledge-hub/press/welcome-paul-caspersen) | "is an advisor with Charitable Solutions, LLC" |
| [Dechomai Foundation home page](https://dechomai.org/) | Day-to-day operations provided by Charitable Solutions |
| [NPT adviser page](https://www.nptrust.org/advisors-and-institutions/for-advisors/) | Lisa Barr, SVP |
| [College DAF gift FAQ PDF](https://www.theamericancollege.edu/sites/default/files/Donor-Advised-Funds-FAQS%20.pdf) | The College accepts DAFpay |

## 4. Other key sources (read by research agents)

- **Form 990 XML returns** for FY2020–FY2024 (EIN 23-1352008), from the public `gt990datalake-rawdata` mirror. Object IDs are in DE006.
- **Statutes** at LII: [§4966](https://www.law.cornell.edu/uscode/text/26/4966), [§4967](https://www.law.cornell.edu/uscode/text/26/4967), [§4958](https://www.law.cornell.edu/uscode/text/26/4958), [§4943](https://www.law.cornell.edu/uscode/text/26/4943), [§170](https://www.law.cornell.edu/uscode/text/26/170), [§68](https://www.law.cornell.edu/uscode/text/26/68).
- **IRS:** [Notice 2017-73](https://www.irs.gov/pub/irs-drop/n-17-73.pdf); [2026–27 Priority Guidance Plan](https://www.irs.gov/pub/irs-counsel/2026-2027-initial-pgp.pdf).
- **Federal Register:** [2023 proposed DAF regulations](https://www.federalregister.gov/d/2023-24982).
- **FINRA Professional Designations:** [CAP](https://www.finra.org/investors/professional-designations/cap); [D listing](https://www.finra.org/investors/professional-designations/D).
- **Trade press:**
  - [InvestmentNews, 2026-07-28](https://www.investmentnews.com/practice-management/dafcp-designation-launches-as-donor-advised-fund-giving-hits-record-pace/267580);
  - [Financial Planning, 2026-08-06](https://www.financial-planning.com/news/new-professional-designation-aims-to-build-daf-expertise);
  - [ThinkAdvisor, 2026-08-21](https://www.thinkadvisor.com/2026/08/21/with-261-designations-and-counting-how-many-are-worth-it/);
  - [WealthManagement.com, 2026-07-29](https://www.wealthmanagement.com/philanthropy/five-core-truths-about-donor-advised-funds).

The full agent registers (A01–A49, B01–B45, C01–C34, D01–D32, E01–E22) were working files. The rows material to conclusions were carried into `evidence-register.csv` with an `agent_ref`.

## 5. Negative findings and blocked sources

**Searched, nothing found:**
- College enrolment, completion or holder figures;
- DAFCP job postings or tuition reimbursement;
- a FINRA listing for DAFCP;
- a DAFCP syllabus, textbook title or exam blueprint;
- any Ren, TIFIN Give, Greater Horizons, Daffy or Foundation Source tie;
- comment from professional bodies or DAF critics;
- Reddit threads;
- a 2025 or 2026 DAF Forum (the 2027 Forum is the "inaugural" one);
- the funder of the Wallace Chair;
- sponsorship amounts;
- third-party accreditation of any College designation (ANAB and NCCA directories not queried);
- an enacted state DAF reporting or payout law.

**Blocked or limited:**
- **Archive.org:** snapshot bodies failed (proxy reset, HTTP 429); archive.today was unreachable.
- **Job boards and LinkedIn:** LinkedIn, Indeed, Glassdoor, ZipRecruiter and TheLadders were not opened, because they need a login or returned 403. Snippets only.
- **Paywalled pages:** the Financial Planning and ThinkAdvisor article bodies were partly paywalled.
- **Paid course:** content not accessed.

## 6. Source conflicts reconciled

| Conflict | Resolution |
|---|---|
| Faculty count 17 (agent D) vs 22 (page) | 22. The lead extracted the full HTML list [DE019] |
| "12 CE credits" (snippet) vs "30 College CE credits" (page) | 30, the first-party figure [DE018] |
| OBBBA in the compliance module (InvestmentNews) vs the Tax module (page) | Tax module; the first-party page governs [DE043] |
| Announcement date 2026-07-28 (InvestmentNews) vs 2026-07-30 (release) | Both recorded. The release date is used as the official launch [DE016] |
| Caspersen at Charitable Solutions: "advisor" (College) vs "Vice President" (firm) | Both recorded. The nature of the role is unresolved (OQ10) |
| CAP holders: "over 2,500" vs "over 1,900" | Both recorded as conflicting self-reports [DE015] |
| The 2025 sponsors described as DAFCP sponsors (one secondary summary) | Rejected. They are documented only for the 2025 certificate and the 2027 Forum |
| Batch 38C's 0-of-7 sponsor faculty vs 10 of 22 here | Different source rule: College-printed employers vs employer-published pages. The latter governs [DE072] |
