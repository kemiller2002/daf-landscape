# DAFCP™ investigation (2026-11-20): package index and method

**What this is.** An evidence-based investigation of the Donor-Advised Fund Certified Professional (DAFCP™) designation, issued by The American College of Financial Services ("the College"). It covers the designation's origins, governance, commercial relationships, curriculum, technology coverage, adoption, incentives and strategic meaning for our DAF work.

**Date of observation:** 2026-11-20. **Branch:** `claude/dafcp-investigation-30gkcj`. This is desk research from public sources. It is not legal advice and makes no allegation of misconduct.

## Files

| # | Deliverable | File |
|---|---|---|
| 1 | Executive investigation report | [01-executive-investigation-report.md](01-executive-investigation-report.md) |
| 2 | Institutional governance and funding | [02-institutional-governance-and-funding.md](02-institutional-governance-and-funding.md) |
| 3 | Curriculum and competency audit | [03-curriculum-and-competency-audit.md](03-curriculum-and-competency-audit.md) |
| 4 | Industry relationships and influence map | [04-industry-relationships-and-influence-map.md](04-industry-relationships-and-influence-map.md) |
| 5 | Credential comparison | [05-credential-comparison.md](05-credential-comparison.md) |
| 6 | AI and technology gap analysis | [06-ai-and-technology-gap-analysis.md](06-ai-and-technology-gap-analysis.md) |
| 7 | Market adoption evidence | [07-market-adoption-evidence.md](07-market-adoption-evidence.md) |
| 8 | Clarity assessment | [08-clarity-assessment.md](08-clarity-assessment.md) |
| 9 | EDF assessment | [09-edf-assessment.md](09-edf-assessment.md) |
| 10 | Strategic scenarios and recommendations | [10-strategic-scenarios-and-recommendations.md](10-strategic-scenarios-and-recommendations.md) |
| 11 | Source and evidence register | [11-source-and-evidence-register.md](11-source-and-evidence-register.md) |
| 12 | Open questions and interview targets | [12-open-questions-and-interview-targets.md](12-open-questions-and-interview-targets.md) |

**Machine-readable data** are in [`data/dafcp-investigation-2026-11-20/`](../../data/dafcp-investigation-2026-11-20/):

| File | Rows | Content |
|---|---|---|
| [evidence-register.csv](../../data/dafcp-investigation-2026-11-20/evidence-register.csv) | 73 | Every material finding: claim, URL, publisher, dates, short excerpt, evidence type, tag, epistemic class, confidence, contradictions, uncertainty, strategic relevance |
| [faculty-affiliations.csv](../../data/dafcp-investigation-2026-11-20/faculty-affiliations.csv) | 22 | All 22 people named on the DAFCP page, with employer-published affiliations |
| [relationship-map.csv](../../data/dafcp-investigation-2026-11-20/relationship-map.csv) | 28 | Organization-to-programme relationships with a four-state status |
| [legal-baseline.csv](../../data/dafcp-investigation-2026-11-20/legal-baseline.csv) | 20 | Statute, regulation, guidance, case and practice baseline |
| [curriculum-audit.csv](../../data/dafcp-investigation-2026-11-20/curriculum-audit.csv) | 17 | Module-by-dimension findings with an assessability label |
| [ai-technology-coverage.csv](../../data/dafcp-investigation-2026-11-20/ai-technology-coverage.csv) | 16 | 15 technology capabilities plus a generic row, with coverage level and the repo benchmark |
| [credential-comparison.csv](../../data/dafcp-investigation-2026-11-20/credential-comparison.csv) | 20 | Comparison facts (DAFCP, CAP, CFP, CSPG, other training) |
| [adoption-evidence.csv](../../data/dafcp-investigation-2026-11-20/adoption-evidence.csv) | 9 | Enrollment, completion, holders, employer requirement, kept separate |
| [scenarios.csv](../../data/dafcp-investigation-2026-11-20/scenarios.csv) | 4 | Scenarios A–D with indicators and qualitative confidence |
| [open-questions.csv](../../data/dafcp-investigation-2026-11-20/open-questions.csv) | 11 | Prioritized unresolved questions and the route to answer each |

**Validation:** `python3 -I scripts/dafcp_validate.py .` checks unique IDs, required fields, controlled vocabularies, that every `evidence_ids` reference resolves, that [F]/[R] rows carry a URL, that excerpts stay at 40 words or fewer, and that every relative link in this folder resolves. The repository's mechanical citation screen (`scripts/mission_citation_audit.py`) was also run on this folder. After the fixes, the remaining 41 flagged lines are date or year mentions in prose and lists, such as "the 2025 certificate", not uncited figures.

## Method

**Research agents.** Five research agents ran in parallel: institution, programme and people, curriculum and law, credentials and adoption, and reception and technology. The lead analyst then reconciled conflicts between them and re-read the decisive primary sources directly (marked `lead re-check` in `checked_by`):
- the 2025 certificate release;
- the DAFCP page, including the 22-name contributor list;
- the DAF Forum "about" page;
- the MSCHE institution record;
- the Charitable Solutions team page;
- the College's welcome release for the programme director;
- Dechomai's home page;
- NPT's adviser page;
- the 2025 agenda PDF;
- the College's DAFpay FAQ.

**Rules followed** (the repository's mission rules):
- robots.txt was read before fetching a host.
- No logins, CAPTCHA or bot-challenge bypass, paywall bypass, form submission or outreach.
- LinkedIn was used only through search-engine snippets, tagged [R].
- Restricted course or exam material was not sought.
- Quotes are short.
- Archive.org snapshot bodies could not be loaded (proxy reset and HTTP 429). Archive.today was unreachable. Only Wayback availability metadata was used.

**Tags:**
- [F] first-party document read;
- [R] search snippet or secondary source;
- [I] inference;
- [X] carried from the repository;
- [S] computed here;
- [U] unknown.

**Epistemic classes in the register:**
- verified-fact;
- strongly-supported-inference;
- working-hypothesis;
- unsupported-claim;
- unknown;
- negative-finding (a documented search that found nothing).

**Confidence labels** follow the EDF claim-and-confidence policy: Low, Low-Medium, Medium, Medium-High, High. They are qualitative, not probabilities.

**Frameworks.** Clarity and EDF were read from the canonical repositories on 2026-11-20:
- Clarity `kemiller2002/clarity-framework` at `200a9eb`: `rules.md`, `decision-posture-model.md`, `docs/progressive-commitment.md`, `docs/reconsideration-criteria.md`, `docs/templates/clarity-result-template.md`.
- EDF `kemiller2002/echelon-diagnostic-framework` at `710d54c`: `docs/edf/specification.md` v0.3, `docs/edf/complexity-levels.md`, `docs/framework-engineering/claim-and-confidence-policy.md` v1.0.

These HEADs are newer than the commits pinned in [clarity-edf-application-guide.md](../mission-2026-11-14/clarity-edf-application-guide.md). The files used carry the same content as the guide describes: EDF is still v0.3 and the policy is still v1.0. The repository's application rules are followed: EDF only for observed outcomes; structural-versus-habit classification; EDF claim states for repository findings.

## Relationship to earlier repository work

This package extends and partly supersedes these earlier files:
- [analyst-and-education-landscape.md](../mission-2026-11-14/analyst-and-education-landscape.md) §5;
- [queue-batch37-controls-education.md](../mission-2026-11-14/queue-batch37-controls-education.md) §4–§5 (P-ANL-06, P-ANL-09);
- [queue-batch38-closeout-checks.md](../mission-2026-11-14/queue-batch38-closeout-checks.md) §1 (P-B37C-03).

The reconciliation is recorded in [01 §7](01-executive-investigation-report.md#7-what-changed-relative-to-earlier-repository-findings) and in evidence rows DE072–[DE073]. A pointer note has been appended to each of those files; their historical text is not rewritten.

**Status:** these findings come from the original research pass and have not yet been independently validated in a numbered validation wave. Under the repository convention, they become governing once a validation register confirms them.
