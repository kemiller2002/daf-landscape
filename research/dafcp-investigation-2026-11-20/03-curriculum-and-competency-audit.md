# DAFCP curriculum and competency audit

**Date:** 2026-11-20. **Data:**
- [`curriculum-audit.csv`](../../data/dafcp-investigation-2026-11-20/curriculum-audit.csv) (CA01–CA17)
- [`legal-baseline.csv`](../../data/dafcp-investigation-2026-11-20/legal-baseline.csv) (LB01–LB20)

**Evidence:** [DE042–DE056].

**Limits.** Only public curriculum text was read: the programme page, the launch release, the checkout catalogue and the director's articles. No course or exam material was sought. Each judgement below therefore carries one of three labels:
- **public text supports**;
- **inferable**;
- **cannot assess**.

Most quality judgements fall in the third class. This is not legal advice.

## 1. What is public

**Overall structure.** The public outline is six modules. Each has a one-line description and four "you'll be able to understand" topic bullets. There are also five programme learning outcomes. Delivery is short videos, quizzes, a "comprehensive case study" and an unnamed required textbook [DE042, DE017]. The course code is "DAFCP 200" [DE025].

**Not public:**
- a syllabus;
- an exam blueprint;
- topic weights;
- the textbook title;
- a module-to-author mapping;
- a "law current as of" date.

| Module | Topic bullets (verbatim, shortened where marked) |
|---|---|
| 1 Fundamentals | terminology and structural definitions; history and evolution of DAFs; **Legal guardrails and prohibited transactions**; donor motivation and the DAF ecosystem |
| 2 Tax Fundamentals | deduction rules and bunching; **Prearranged sale doctrine, assignment of income, and unrelated business income tax**; valuation of complex assets and IRS forms; **The One Big Beautiful Bill Act and charitable giving** |
| 3 Gift Acceptance | asset types and valuation; complex assets in real estate; complex assets in business and alternative assets; business-owner exit planning and DAFs |
| 4 Investing and Grant Management | grantmaking rules and eligible recipients; **Gift agreements and IRS Notice 2017-73**; international grantmaking rules; traditional and alternative investment strategies |
| 5 Estate Planning and Planned Giving | estate planning and DAF succession; pairing DAFs with trusts; DAFs, private foundations and supporting organisations; multigenerational planning |
| 6 Ethics, Compliance and Technology | ethics in DAF management; DAF regulation landscape and court cases; **DAF technology tools**; applied compliance, judgment and the future of DAFs |

**Corrections to earlier readings [DE043]:**
- "Legal guardrails and prohibited transactions" belongs to Module 1, not Module 6.
- OBBBA belongs to Module 2. InvestmentNews placed it in the compliance module; the College's page governs.

**Self-description.** The programme says it is "not designed to provide legal or tax advice, but to prepare learners to recognize issues, understand trade-offs, and collaborate effectively with qualified advisors" [F]. It calls itself "comprehensive, neutral, and professionally rigorous" [DE048].

## 2. Legal baseline used for comparison

The full table, with authorities, status classes and URLs, is in [`legal-baseline.csv`](../../data/dafcp-investigation-2026-11-20/legal-baseline.csv). The categories are kept separate.

**Statute:**
- §4966: taxable distributions; expenditure responsibility for non-excepted grantees; DAF-to-DAF grants are excepted.
- §4967: prohibited benefits.
- §4958(c)(2): automatic excess benefit [DE054].
- §4943(e): excess business holdings for DAFs [DE055].
- §170(f)(18): acknowledgment.
- The OBBBA changes:
  - the 0.5% floor in §170(b)(1)(I) [LB06];
  - the non-itemizer deduction in §170(p), which **excludes gifts to DAFs** [DE052];
  - the §68 2/37 reduction, often taught loosely as a "35% cap" [DE053];
  - the corporate 1% floor [C22, agent C].

**Final regulations:** qualified appraisal and Form 8283.

**Proposed regulations:** REG-142338-07 (November 2023). These are **neither final nor withdrawn** [DE050]. The 2026–27 Priority Guidance Plan reframes the project as guidance on "certain donor advised fund arrangements", with no deadline [DE051].

**Notices and revenue procedures:**
- Notice 2017-73: pledge relief may be relied on; the bifurcation position was only previewed [DE056].
- Notice 2006-109 and Rev. Proc. 2017-53 (equivalency determinations).
- CCA 202302012 (crypto appraisal; non-precedential).

**Cases:**
- Pinkert v. Schwab Charitable: the donor lacked standing.
- Fairbairn v. Fidelity Charitable: the sponsor prevailed at trial.
- The prearranged-sale line of cases, through Hoensheid (2023).

**Industry practice:** sponsor inactivity and minimum-grant rules. These are voluntary, not legal mandates.

**State law:** UPMIFA. No enacted state DAF payout or reporting law was found.

## 3. Module audit across the ten dimensions

| Dimension | What public text shows | Label |
|---|---|---|
| 1. Legal and tax accuracy | Topic labels map to the correct authorities. Accuracy of content cannot be tested. **Legal-currency risk:** course access opened 2026-09-01, the 2026–27 PGP reframing followed on 2026-09-29, and no "current as of" date is given (CA11). Two test items for accuracy are the §170(p) DAF exclusion and the §68 mechanism (CA03) | cannot assess (accuracy); inferable (currency risk) |
| 2. Practical applicability to DAF operations | Strong for **advisers and gift officers** on asset suitability, bunching and exit planning. Weak for **operations staff**: no intake, eligibility-data, payment, reconciliation or exception workflows are named (CA04, CA06) | public text supports |
| 3. Complexity | About 30 hours across six modules, roughly 5 hours each. Advanced topics are named (UBTI, assignment of income, international grantmaking), so depth per topic must be limited (CA15) | inferable |
| 4. Controversial and unresolved issues | Named only generically ("regulation landscape and court cases"). **Payout, fees and adviser-managed DAF pay, DAF-to-DAF transfers, inactivity, anonymity and state oversight are absent** ([DE046], CA09). The director names payout, transparency, donor control and inactive accounts as "legitimate policy debates" outside the curriculum [DE047]. The 2025 predecessor had a session on handling critiques [DE023] | public text supports (absence) |
| 5. Operational workflows | Implied only: "readiness for contribution" and "eligible recipients" | inferable |
| 6. Technology architecture | "DAF technology tools" only (CA12). See [06](06-ai-and-technology-gap-analysis.md) | public text supports |
| 7. Compliance and auditability | "Applied compliance" and "prohibited transactions" are named. Form 990 Schedule D, Form 4720, internal controls, acknowledgments and audit trails are not named (CA13) | public text supports |
| 8. Donor experience | Donor motivation, bunching, succession and multigenerational planning are named | public text supports |
| 9. Financial adviser integration | Investment strategies and exit planning are named. **The adviser-managed DAF model, its fees, and the 2023 proposal's treatment of advisers as donor-advisors are not named** (CA08) | public text supports (absence) |
| 10. Future developments | "the future of DAFs" and the outcome "navigate DAF policy changes" are named; the content is unknown (CA17) | cannot assess |

## 4. Specific coverage checks

| Topic | Public outline | Label | Gap |
|---|---|---|---|
| Privately held business interests | Named (Module 3; prearranged sale in Module 2) | supports | §4943(e) excess business holdings not named |
| Real estate | Named | supports | Debt-financed property (UBTI), environmental review and carrying costs not named |
| Cryptocurrency | Not named; at most "alternative assets" | inferable (weak) | Appraisal requirement (CCA 202302012) not visible |
| Restricted securities / Rule 144 | Not named | cannot assess | — |
| Other noncash (art, LP/LLC interests) | "alternative assets"; "asset types" | inferable | — |
| Valuation, appraisal, Form 8283 | "Valuation of complex assets and IRS forms" | supports | Sponsor's Form 8283 duties not visible |
| Grant eligibility | Named | supports | — |
| Expenditure responsibility | Not named | inferable | Workflow absent |
| Equivalency determination | Not named; within "international grantmaking rules" at most | inferable | Rev. Proc. 2017-53 not visible |
| International grantmaking | Named | supports | — |
| Donor succession | Named | supports | — |
| Investment management | "Traditional and alternative investment strategies" | supports | Adviser-managed fees, UPMIFA and fiduciary standard not named |
| Private benefit and prohibited benefits | Named (Module 1) | supports | — |
| Conflicts of interest | "Ethics in DAF management" | inferable | Adviser-compensation conflicts not named |

**Pattern.** The curriculum's strongest visible content is complex-asset gift acceptance and tax doctrine. That matches the specialism of its largest faculty cluster, Charitable Solutions LLC, a noncash-gift administrator [DE026]. The match is consistent with faculty expertise shaping the emphasis. It does not show commercial steering.

## 5. What the curriculum teaches, assumes and omits

- **Teaches:**
  - the legal architecture of DAFs;
  - tax planning with DAFs, including post-OBBBA bunching;
  - how complex assets reach a DAF;
  - how DAFs fit estate plans.
- **Assumes:**
  - the DAF is a suitable vehicle once the donor is motivated (outcome: "Analysis on donor motivations and asset suitability");
  - the professional works inside an existing sponsor's rules and systems;
  - aggregate market statistics describe the experience of any individual account. The programme page uses $328bn in assets, 19% growth and $91bn in contributions; the director cites a 25.2% aggregate payout ([analyst file T1](../mission-2026-11-14/analyst-and-education-landscape.md); [DE047]).
- **Omits (visible):**
  - comparative sponsor economics: fees, investment menus, realised payout distribution;
  - portability and exit;
  - inactivity enforcement;
  - anonymity and data flows to grantees;
  - operational controls (payment redirection, fraud);
  - technology architecture;
  - any treatment of when a DAF is the wrong vehicle. A College CE module elsewhere does cover "when it is not" (EC05 in [adviser-curricula-daf-content-2026.csv](../../data/mission-2026-11-14/adviser-curricula-daf-content-2026.csv)).

The repository has documented evidence on most of these omissions; see [10 §3](10-strategic-scenarios-and-recommendations.md).

## 6. Does DAFCP establish professional competence?

- **Knowledge:** yes, at a moderate bar. The exam is proctored and the pass mark is 70% of the course grade. Exam length, item count and pass rates are not published [DE017].
- **Applied competence:** weakly. A case study is the only applied element. There is no supervised practice, no experience gate (the 2025 predecessor required three years, DE022), and no work-product review. CSPG's practicum is the comparator [DE067].
- **Operational competence** (running grant, gift-acceptance or compliance operations at a sponsor): no public evidence that it is assessed.

**Verdict:** DAFCP signals tested familiarity with DAF law and planning. It should not be read as certifying the ability to run or evaluate DAF operations. Claim state: *suggestive*; confidence Medium. Paid content could change the applied-competence reading but not the absence of an experience gate.

## 7. Unresolved, in priority order

1. How the 2023 proposed regulations and the 2026–27 PGP are taught (OQ05).
2. Whether the §170(p) DAF exclusion and the §68 mechanism are taught correctly.
3. Which modules the noncash-administrator and sponsor-employed faculty authored (OQ02).
4. What the case study requires.


---

## Syllabus corrections (2026-11-20) — governing

Source: [dafcp-syllabus-findings.md](../education/dafcp-syllabus-findings.md); evidence DE074–DE083. The syllabi were read under the [owner decision on robots.txt](../education/owner-decision-robots-2026-11-20.md).

- **Units per syllabus (DE077).** Unit 3 is Gift Acceptance and Investment Management. Unit 4 is Grantmaking and Grant Administration.
- **Learning objectives that change the audit (DE076):**
  - CLO4 covers impact investing and sponsors' regulatory and fiduciary standards. Fiduciary standards are therefore covered, not absent.
  - CLO5 covers operational policies and administrative best practices. Operational workflows move from "inferable" to **covered at objective level**.
  - CLO7 covers the responsible use of technology tools.
- **Assessment (DE078).** A case study develops across all six units. The final exam is 100 multiple-choice questions in 150 minutes, closed book, with no retakes. Applied competence is assessed through the case study, but only within multiple-choice quizzes and the exam.
- **Still unnamed in syllabus text:** payout distribution, fees and adviser-managed DAF pay, portability, inactivity, anonymity, and AI as a curriculum topic.
