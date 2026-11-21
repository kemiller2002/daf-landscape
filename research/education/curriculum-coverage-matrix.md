# Curriculum coverage matrix: DAFCP compared with the daf-landscape research

**Date:** 2026-11-21. **Data:** [`data/education/curriculum-coverage-matrix.csv`](../../data/education/curriculum-coverage-matrix.csv), 57 topics.

**What the columns contain:**
- **DAFCP coverage** comes from the public programme page and the DAFCP 200 syllabus. The syllabus corrections ([dafcp-syllabus-findings.md](dafcp-syllabus-findings.md)) are applied.
- **Repository coverage** comes from a topic-by-topic read of the repository. Each topic is rated strong, moderate or thin. Repository files are listed per topic in the CSV.
- **Importance** columns rate regulatory, operational, technology and AI relevance (H/M/L). They are the repository's judgement [I].
- **Gap category:**
  - **1** marks the repository's own research gap.
  - **2** marks a gap in the curriculum's public text.
  - **3** marks a structural gap, where both education and research rest on assumptions or missing data.
- **Priority 1** marks the topics most worth more work.

**Caveat.** A topic that is "not in public text" may still be taught in the paid course content. A gap-2 entry means the public text does not show the topic; it does not prove the course omits it.

## 1. Summary counts

| Measure | Counts |
|---|---|
| DAFCP public coverage | 27 explicit · 1 explicit (generic) · 15 implied · 1 textbook theme only · 13 not in public text |
| Repository coverage | 29 strong · 13 moderate · 15 thin · 0 none |
| Gap category | 19 repository gaps (cat. 1) · 13 curriculum gaps (cat. 2) · 7 structural gaps (cat. 3) · 18 no gap |
| Priority 1 topics | 13 |

[S] counted from the CSV.

**The two bodies of knowledge are close to inverses of each other.**
- The curriculum is densest in tax, complex assets and estate planning. In 9 of the 15 topics where the repository is thin, the curriculum names the topic explicitly.
- The repository is densest in operations, payments, technology, data, governance and market structure. In 11 of the 13 curriculum gaps, the repository is strong.

## 2. Matrix

| ID | Topic | DAFCP | Repository | Gap | Priority |
|---|---|---|---|---|---|
| A01 | Historical development of DAFs | explicit | thin | 1 | 3 |
| A02 | Legal and organisational structures of sponsors | explicit | strong | — | 3 |
| A03 | Sponsoring-organisation landscape | implied | strong | — | 3 |
| A04 | Donor advisory privileges | implied | moderate | 1 | 2 |
| A05 | Sponsor exclusive legal control and fiduciary responsibility | implied | moderate | 3 | 2 |
| A06 | Donor motivations | explicit | moderate | 3 | 2 |
| A07 | DAFs compared with private foundations | explicit | moderate | 1 | 2 |
| A08 | Industry terminology | explicit | thin | 1 | 3 |
| A09 | Prohibited benefits and transactions (§§4967, 4958) | explicit | moderate | 1 | **1** |
| B01 | Federal charitable deductions | explicit | strong | — | 3 |
| B02 | AGI contribution limits | implied | strong | — | 3 |
| B03 | Five-year carryforward | not in public text | moderate | 2 | 3 |
| B04 | Appreciated securities | implied | strong | — | 3 |
| B05 | Closely held businesses | explicit | moderate | 1 | **1** |
| B06 | Real estate | explicit | thin | 1 | **1** |
| B07 | Complex and noncash assets, including crypto | implied | strong | — | 2 |
| B08 | Deduction timing | not in public text | thin | 1 | 2 |
| B09 | Bunching | explicit | strong | — | 3 |
| B10 | Tax reporting (Forms 8283 and 8282, acknowledgments, 990 Schedule D) | explicit | moderate | 1 | **1** |
| B11 | Legislation and proposed changes | explicit | strong | — | 2 |
| C01 | Gift acceptance policies | implied | moderate | 1 | 2 |
| C02 | Due diligence on contributed assets | implied | thin | 1 | **1** |
| C03 | Valuation and qualified appraisal | explicit | thin | 1 | **1** |
| C04 | Asset liquidation | not in public text | thin | 1 | 2 |
| C05 | Business sale transactions | explicit | moderate | — | 2 |
| C06 | Restricted gifts | not in public text | thin | 3 | 3 |
| C07 | Noncash processing operations | implied | strong | 2 | 2 |
| C08 | Sponsor-specific requirements | not in public text | moderate | 2 | 3 |
| C09 | Operational risk | not in public text | strong | 2 | 2 |
| D01 | Investment management and pools | explicit | strong | — | 3 |
| D02 | Custody | not in public text | thin | 3 | 2 |
| D03 | Adviser-managed assets | not in public text | strong | 2 | 2 |
| D04 | Grant recommendations | implied | strong | — | 2 |
| D05 | Charity eligibility verification | explicit | strong | 3 | **1** |
| D06 | Domestic and international grants | explicit | strong | — | 2 |
| D07 | Grant restrictions | explicit | strong | — | 2 |
| D08 | Compliance and approval workflows | explicit (syllabus CLO5) | strong | — | **1** |
| D09 | Grant payment processing | not in public text | strong | 2 | 2 |
| D10 | Reporting and reconciliation | not in public text | strong | 2 | 2 |
| E01 | Beneficiary designations | implied | moderate | 1 | 3 |
| E02 | Successor advisers | explicit | strong | — | 3 |
| E03 | Trusts (CRT/CLT with DAFs) | explicit | thin | 1 | 2 |
| E04 | Estate planning | explicit | thin | 1 | 3 |
| E05 | Family philanthropy | implied | thin | 1 | 3 |
| E06 | Multigenerational giving | explicit | thin | 1 | 3 |
| E07 | Business succession | explicit | thin | 1 | 2 |
| E08 | Donor legacy planning | explicit | moderate | — | 3 |
| E09 | Relationships with financial advisers | implied | strong | — | 3 |
| F01 | Regulatory obligations | explicit | strong | — | 2 |
| F02 | Sponsor governance | not in public text | strong | 2 | 3 |
| F03 | Fiduciary concerns | explicit (syllabus CLO4) | thin | 3 | 2 |
| F04 | Ethical conflicts (adviser fees, affiliated investments) | implied | strong | 2 | 2 |
| F05 | Technology infrastructure | explicit (generic) | strong | 2 | **1** |
| F06 | Data privacy | not in public text | strong | 2 | **1** |
| F07 | Automation | not in public text | strong | 2 | **1** |
| F08 | AI-assisted decision-making | textbook theme only | strong | 3 | **1** |
| F09 | Emerging operational risks | implied | strong | 2 | **1** |

The CSV records, for each row, the repository files, what the repository has, the missing research, and the four importance ratings.
