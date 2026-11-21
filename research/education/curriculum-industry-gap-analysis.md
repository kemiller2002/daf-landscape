# Curriculum-to-industry gap analysis

**Date:** 2026-11-21.

**Inputs:**
- [curriculum-coverage-matrix.md](curriculum-coverage-matrix.md) and its CSV (57 topics);
- [dafcp-syllabus-findings.md](dafcp-syllabus-findings.md);
- [AI readiness report](ai-readiness-of-daf-education.md);
- [assumption tests](professional-education-assumptions.md).

**Rule.** A topic missing from the public outline or syllabus is not proven missing from the paid course content. Gap-2 findings below are about **public text** only.

## Category 1: the repository's own research gaps

These are subjects that professional education covers and the repository investigates inadequately. There are 19 topics, 9 of them taught explicitly by DAFCP. The subjects are listed in order of priority.

| Priority | Topic (ID) | What the repository lacks | Action |
|---|---|---|---|
| 1 | Prohibited benefits (A09) | No analysis of the §4958(c)(2) automatic excess benefit rule or of §4943(e) excess business holdings | Covered in [knowledge guide](daf-professional-knowledge-guide.md) §A5. Add operational cases |
| 1 | Closely held business gifts (B05) | S-corporation UBTI, the timing of the Hoensheid case, and §4943 disposition periods | Knowledge guide §B4. Research how sponsors accept private-business interests |
| 1 | Real estate (B06) | Acceptance terms, debt-financed property, environmental review, bargain sales | Knowledge guide §B4. Run a census of real-estate acceptance policies at the top 20 sponsors |
| 1 | Tax reporting (B10) | Sponsor duties on Forms 8283 (Section B) and 8282; content of acknowledgments | Knowledge guide §B3 |
| 1 | Due diligence and valuation (C02, C03) | Qualified-appraisal and appraiser rules; the sponsor's sign-off workflow | Knowledge guide §C. This is the strongest AI use case and has no operational data |
| 2 | Liquidation (C04); gift acceptance policies (C01) | Liquidation policies and timing risk | Policy census |
| 2 | Deduction timing (B08) | When a gift is complete, and year-end cut-offs by type of asset and payment rail | Knowledge guide §B2 |
| 2 | Donor advisory privileges (A04); DAF compared with a private foundation (A07) | Investment-advisory privileges; a decision framework that goes beyond tax | Knowledge guide §A |
| 2–3 | Estate and planned giving (E01, E03–E07) | CRT and CLT gifts to DAFs; estate-tax treatment; family governance; business succession | One dedicated batch. This is the curriculum's core content and the repository's weakest domain |
| 3 | History and terminology (A01, A08) | A sourced history and a glossary | Knowledge guide §A1 and glossary |

## Category 2: gaps in the curriculum's public text

These are current or emerging industry subjects that neither the public DAFCP outline nor the syllabus names. There are 13 topics, and the repository has strong coverage of 11 of them.

| Topic (ID) | Repository evidence the curriculum's public text does not show |
|---|---|
| Technology infrastructure (F05), automation (F07), data privacy (F06) | Vendor architecture, payment rails, and APIs or MCP servers (Daffy, Chariot). Donor-data defaults to grantees. SOC scope gaps |
| AI-assisted decision-making (F08) | The governance rule "AI may add a flag, never clear one" and the AI product census (30 products). The AI economics show redesign beats AI in most processes ([AI readiness](ai-readiness-of-daf-education.md)) |
| Emerging operational risks (F09) | Payment redirection and BEC disclosed in sponsors' 990s. No sponsor publishes the federal benchmark call-back control |
| Grant payment processing and reconciliation (D09, D10) | Check, ACH, PayPal and Chariot rails; unclaimed grants; reconciliation economics |
| Adviser-managed assets and conflicts (D03, F04) | Adviser fees of 0–2% on DAF assets. The 2023 proposal treating advisers as donor-advisors. Affiliated-fund economics |
| Sponsor governance (F02); sponsor-specific requirements (C08) | Governance quality, related-party fees, minimums and fee schedules |
| Noncash processing operations (C07); operational risk (C09) | Noncash processors; vendor concentration; sponsor mortality |
| Five-year carryforward (B03) | Interaction with the new 0.5% floor |

The curriculum also omits payout distributions, fees, transfers between sponsors, inactivity enforcement and anonymity. The DAFCP investigation recorded these omissions (DE046), and they persist after the syllabus was read.

## Category 3: structural knowledge gaps

These are subjects where both traditional education and industry research rely on assumptions, incomplete data or outdated operating models.

| Topic (ID) | Why it is structural |
|---|---|
| Charity eligibility verification (D05) | Taught as a per-grant legal check, and modelled by the repository from 990 proxies. No sponsor publishes exception rates or reviewer time. The redesign case, a continuous status subscription, is tested only in models |
| AI-assisted decision-making (F08) | Education does not teach it. Research rests on scenario models and vendor claims. No observed error rates exist anywhere |
| Sponsor control and fiduciary duty (A05, F03) | The syllabus teaches sponsor fiduciary standards. Neither the curriculum nor the repository states which operational reviews are legally required and which are discretionary. Pinkert and Fairbairn leave donor standing narrow |
| Donor motivations (A06) | Evidence in both is mostly sponsor-commissioned surveys ([assumptions](professional-education-assumptions.md) H5) |
| Custody (D02) | Neither source documents custody architecture across sponsors |
| Restricted gifts (C06) | Exclusive-control doctrine against donor expectations of restrictions. There is no data on how sponsors handle requests for illiquid or restricted securities |

## What a genuinely comprehensive DAF industry report must contain

The report must combine both bodies of knowledge:
1. **The professional canon:**
   - the law;
   - tax planning;
   - complex assets;
   - estate integration;
   - ethics.

   The repository can now cite the [knowledge guide](daf-professional-knowledge-guide.md) for these.
2. **The operating reality:**
   - platforms;
   - payment rails;
   - data;
   - exceptions;
   - fees;
   - portability;
   - governance;
   - AI.

   This is the repository's strength.
3. **The structural unknowns,** made explicit:
   - measured exception rates and turnaround;
   - AI error rates;
   - custody architecture;
   - which reviews are legally required and which are habit.

Recommended follow-up batches are added to the research backlog (`data/mission-2026-11-14/research-priority-inputs.csv`, IDs P-EDU-01 to P-EDU-08).
