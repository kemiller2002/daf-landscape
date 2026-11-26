# Market-validation interview programme and rejection criteria

**Date:** 2026-11-20. **Status:** design only.
- **No outreach has been made.**
- Contacting prospects needs explicit owner authorisation. In each conversation Echelon Foundry must say who it is and why it is asking.
- Treat every answer as a self-report, and corroborate it against public evidence where possible.

## 1. Purpose

The programme tests the opportunity hypotheses in [`service-offerings/offerings.md`](../service-offerings/offerings.md) against **behaviour** rather than opinion. The useful evidence is what buyers have done: what they spent, which vendors they evaluated, who signed, what triggered the purchase, and what they did not buy and why.

## 2. Sample

Target 15–20 conversations, chosen from the prospect hypotheses ([data](../../../data/commercial-opportunity/)) and stratified as follows.

| Stratum | Count | Example rows (hypotheses only) |
|---|---|---|
| Mid-size community foundations ($250m–$5bn DAF assets), including 2 that migrated recently and 2 still on Ren | 6 | PS05 Greater Horizons, PS07 Cleveland, PS14 Arkansas, PS12 Greater Washington, PS16 CF Texas, PS11 Minneapolis |
| Faith and single-issue sponsors | 2 | PS17 JCF, PS19 Thrivent Charitable |
| National or independent sponsors (niche work only) | 1–2 | PS01 NPT, PS02 AEF |
| Broker-dealer and bank programme owners | 3 | PW06 LPL, PW08 Stifel, PW07 Raymond James, PW24 Regions |
| RIA or aggregator philanthropic-services leads | 2 | PW11 Mercer Advisors, PW20 SEI |
| Investors and diligence practitioners | 2 | PV17 GTCR or PV15 Great Hill; one expert-network or commercial due-diligence partner |
| Vendors (product strategy; conflict rules apply) | 1–2 | PV03 Chariot, PV07 Foundant |

Each stratum needs at least 2 interviews before any conclusion is drawn about it.

## 3. Questions (behaviour first)

| # | Question | What it tests | Disconfirming answer |
|---|---|---|---|
| Q1 | Walk me through the last time you changed, renewed or seriously considered changing your DAF platform or grants system. What triggered it, and when? | Trigger events and timing | "We have never evaluated alternatives; renewal is automatic" |
| Q2 | Who took part in that decision, and who signed? Board, CEO, COO, CFO, IT, programme head, parent firm? | Buyer roles and authority | The decision sits at a parent firm Echelon cannot reach |
| Q3 | What did you spend outside your vendor contract on that project: consultants, staff time, temporary staff? Roughly how much? | Existing spending | No outside spending; done entirely in-house or by the vendor |
| Q4 | Which outside firms did you use (if any), and how did you find them? | Competitors and referral channels | A satisfied relationship with a generalist firm or the vendor's own services |
| Q5 | What data or evidence did you wish you had during the evaluation? | Value of independent comparative evidence | "Vendor demos and peer references were enough" |
| Q6 | How did you check vendors' claims (SOC reports, references, pilots)? What did you find? | Assurance gap | A robust existing assurance process |
| Q7 | Since go-live, what has actually improved and what got worse? How do you know? | Outcome measurement; features versus simplicity (assumption A6) | Clear improvements measured internally |
| Q8 | How long does a routine grant to a listed public charity take from recommendation to payment? How do you measure it? | Measured turnaround | Turnaround already measured and satisfactory |
| Q9 | What share of grant recommendations need human review beyond automated checks? Which kinds? | Exception rate (repo gap Q-N03) | Very low exceptions; no pain |
| Q10 | When did a grant or gift last go wrong (misdirected payment, ineligible grantee, valuation dispute)? What did it cost? | Cost of errors; risk appetite | No incidents; no perceived risk |
| Q11 | How are complex gifts (real estate, private stock, crypto) handled today? Who does it, and how long does it take? | Complex-asset pain (the AI fit, A2) | Outsourced to a noncash administrator and satisfactory |
| Q12 | If you could remove one recurring task entirely, which would it be, and what stops you? | Redesign versus automation demand | Nothing material |
| Q13 | Have you budgeted for any technology, AI or operations project in the next 12–18 months? At what stage? | Budget and urgency | No budget; no project |
| Q14 | What does your contract say about data export and transition at the end of the term? Have you tested it? | Portability, a renewal-benchmark need | Tested, satisfactory export rights |
| Q15 | (Wealth programmes) Who owns the economics of your DAF programme, and how do adviser fees on DAF assets work? | Adviser-controlled design (A4) | The programme is a referral only; there is no owner |
| Q16 | (Wealth programmes) When you chose your sponsor of record and vendor, what alternatives did you consider, and why did you reject them? | Market-entry and selection advisory | A single-option choice made by a parent or affiliate |
| Q17 | (Investors) On recent deals in philanthropy or wealth technology, who did your commercial and technical diligence? How was it scoped and priced? | Due-diligence route to market | Always done in-house or by incumbent firms only |
| Q18 | (Investors) What could you not find out about DAF businesses that you wanted to know? | Value of market intelligence | Information sufficient |
| Q19 | Do you pay for any market research or benchmarking today (associations, analysts, surveys)? Which, and at what price? | Subscription comparables | Nothing paid; only free association material |
| Q20 | Would you share anonymised operating metrics in exchange for a benchmark report? What would stop you? | Feasibility of a data cooperative or benchmark | Data sharing barred by policy or legal |
| Q21 | Does any professional credential (CAP, CFP, DAFCP) affect whom you hire or retain as an adviser or consultant? | Credential value (assumption A7) | A credential is required: this would upgrade DAFCP |
| Q22 | What would make you distrust an independent assessor? (Vendor payments, prior criticism, lack of operating experience) | Conflict-of-interest constraints | "Any vendor revenue disqualifies you" |

**Interview rules:**
- No leading pitch before Q13.
- Never ask "would you buy X".
- Ask for documents (public RFPs, board minutes) only where the interviewee volunteers them.

## 4. Desk validation alongside interviews

- Re-read the FY2025 Form 990 Part VII-B contractor lines for every interviewed sponsor ([`scripts/commercial_sponsor_spend_distribution.py`](../../../scripts/commercial_sponsor_spend_distribution.py) inputs).
- Monitor job postings, migration notices and conference agendas each quarter. Sources: [demand-signals-and-process-economics.md](demand-signals-and-process-economics.md) §1; the repo's [watchlist](../../../data/mission-2026-11-14/watchlist.csv).
- Use Reddit and forums for hypothesis generation only.

## 5. Rejection criteria

An opportunity is **rejected or paused** if any of the following holds after the stated evidence threshold.

| # | Criterion | Threshold |
|---|---|---|
| R1 | No buyer in the stratum reports outside spending (Q3/Q4) on a comparable problem in the last 3 years | 0 of at least 4 interviews in the stratum |
| R2 | The decision sits at a parent firm Echelon cannot reach (Q2) | At least 3 of 4 interviews |
| R3 | Buyers describe the problem but have no budget or project within 18 months (Q13) | At least 3 of 4 |
| R4 | A satisfied incumbent (generalist consultancy or vendor services) meets the need at a lower price | At least 2 named instances and no stated gap |
| R5 | Delivery depends on data buyers will not share (Q20) and no public substitute exists | Stated policy barriers at 2 or more sponsors |
| R6 | The offer creates an unmanageable conflict, for example paid vendor work that undermines independent ratings (Q22) | Any credible buyer states it would disqualify Echelon, and no barrier design satisfies them |
| R7 | Expected price below delivery cost: fee benchmark below 1.5× the estimated delivery cost | From the pricing benchmarks plus pilot data |
| R8 | Software opportunity: fewer than 3 independent buyers with the same repeated workflow pain and budget | Applies before any build |

## 6. Recording

Each interview produces a row (date, stratum, role, consent level, answers coded to Q1–Q22, evidence quality, follow-up). Interviewees' names are not recorded without consent. Store the rows in `data/commercial-opportunity/interview-log.csv`, which is not created until interviews begin.
