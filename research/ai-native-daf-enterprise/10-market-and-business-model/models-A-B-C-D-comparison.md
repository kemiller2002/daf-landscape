# Models A, B, C and D: a like-for-like comparison (addendum §25)

**Status:** decision analysis, 2026-11-20. **Labels:**
- **[V]** validated in the repository;
- **[S]** scenario figure from the repository's entrant model (`data/mission-2026-11-14/entry-strategy-comparison.csv`), not an estimate of any firm;
- **[I]** inference;
- **[A]** assumption new to this workstream.

**Reproduce:** `python3 -I scoring.py` in this directory. Inputs are [`model-scores.csv`](model-scores.csv) (every score has a written rationale) and [`weights.csv`](weights.csv); output is in [`scoring-output.txt`](scoring-output.txt).

**What this is not:** a market-sizing exercise or a valuation. The scores are structured judgments on repository evidence. Their purpose is to show which conclusions survive changes in what one cares about.

## 1. The models

| Model | Definition | Nearest observed analogue |
|---|---|---|
| **A**: Traditional sponsor with AI enhancements | A new sponsoring charity on a licensed recordkeeping platform. Conventional departments, with AI added to service, document handling and review triage. | Most sponsors' current direction. Ren markets instant approvals; TIFIN Give markets Louise and tax intelligence; Fidelity Charitable runs a virtual assistant (strategic synthesis §B "superficial productivity") |
| **B**: Fully redesigned AI-native sponsor | A new sponsoring charity *and* the AI-native operating model in this workstream: an event-sourced ledger, policy-as-code, exception-only human review, and the specialist-led organization. It owns charitable assets. | Partly Daffy (consumer sponsor plus own technology, MCP server). No sponsor has the full design |
| **C**: AI-native infrastructure sold to sponsors and financial institutions | No charitable assets. Sells the operating layer (policy-as-code decisioning, continuous eligibility, exception workbench, reconciliation, evidence, servicing) and APIs to existing sponsors, wealth platforms and banks. The sponsor keeps legal authority. | Entrant strategies S3 (operating layer) and S2 (modular APIs); Chariot (rails and eligibility); Candid Charity Check; Goodstack |
| **D**: Hybrid, infrastructure plus a partner sponsor-of-record operating slice | Model C, plus full outsourced administration of **one or more programs for a partner sponsor-of-record**, for example a new advisor-channel program. The infrastructure company administers; the partner charity is the legal sponsor, holds the assets at a qualified custodian, and keeps grant authority. The provider never holds funds. | RCF (sponsor) + Ren (administrator); GiveClear + TIFIN Give powering SEI Charitable Fund; Charityvest + Foundation Source; NPT GivingPoint on Ren technology [V] |
| **Dc**: Hybrid variant with a captive sponsor | As D, but the infrastructure company's founders form an affiliated sponsoring charity. Scored to test whether owning the sponsor adds value. | Signatry → Give Interactive (sponsor's trust controls the vendor) [V]; Charityvest's president paid by Foundation Source ($163,944 via Vennfi, 2024) [V] |

## 2. Criteria, applied consistently

| Criterion | Question asked of every model | Main evidence used |
|---|---|---|
| Economics | Can revenue exceed cost at a reachable scale? | Sponsor fee schedules: 0.60% first $500k (Fidelity, DAFgiving360, Charityvest); 0.65% RCF/Ren; 0.90% BofA. Community-foundation admin fees 1.7–4.7× the nationals'. Staff cost 78.7 bps (CFs) vs 5.6–15.0 bps (self-staffed nationals) [V]. RCF→Ren $19.23m FY2024 [V]. Named Ren receipts floor $44.98m (TY2024) [V]. Entrant break-even about 76k–369k grants/yr per customer at $120k/yr [S] |
| Capital | How much must be at risk before a decisive test? | S1 $8.8m / $17.0m / $29.4m; S2 $3.2m / $6.6m / $12.4m; S3 $2.3m / $5.0m / $9.7m to month 24 [S]. Daffy seed plus Series A $21.9m; Chariot Series A $11m [V] |
| Time to evidence | How soon does the model produce evidence that it is better? | S3 first paying customer at 4 / 6 / 9 months; S1 at 18 / 24 / 30 [S] |
| Regulatory burden | What legal exposure does the model take on? | §4966/4967/4958 attach to the sponsor and to knowing managers ([regulatory map](../08-governance-and-compliance/)); moving funds raises money-transmission questions |
| Operational feasibility | Can a small team execute it? | Organization floor of 8–10 people for a self-operated sponsor ([organization model §4](../02-business-capabilities/organization-model.md)) |
| Distribution | Who decides adoption, and can the model reach them? | Wealth firms buy sponsor-plus-technology bundles; RCF+Ren run about 11 wealth programs [V]. Consumer-direct CAC is unproven (failure pattern P3). Six of the top 20 sponsors restrict automated access; no executed contract with API rights has been seen (Q-N04) |
| Defensibility | Would the advantage persist once noticed? | PE consolidators buy plumbing (P2: six of six DAF-tech exits went to Ren, Foundation Source or TIFIN). Incumbents can match policy-as-code (entrant simulation, condition 5) |
| Philanthropic outcome potential | How much of the grant, recipient and donor-guidance experience does the model control? | Outcome O-13 and O-15 analysis; recipient-side costs (strategic synthesis §0 G4) |
| Reversibility | Can the bet be unwound? | Contributions are irrevocable; sponsors can only merge or affiliate (report §11.6) |
| Technical feasibility | How much must be production-grade before the first customer? | Entrant simulation implementation-effort row |

## 3. Decision matrix (scores 1–5, higher is better)

| Criterion | A | B | C | D | Dc |
|---|---|---|---|---|---|
| Economics | 2 | 3 | 3 | 4 | 4 |
| Capital | 2 | 2 | 4 | 3 | 2 |
| Time to evidence | 3 | 2 | 5 | 4 | 3 |
| Regulatory burden (inverse) | 2 | 1 | 4 | 3 | 2 |
| Operational feasibility | 4 | 2 | 4 | 3 | 3 |
| Distribution | 2 | 2 | 2 | 3 | 3 |
| Defensibility | 1 | 3 | 2 | 4 | 4 |
| Philanthropic outcome potential | 2 | 4 | 3 | 4 | 4 |
| Reversibility | 2 | 1 | 5 | 4 | 2 |
| Technical feasibility | 5 | 3 | 4 | 3 | 3 |

Rationale for each cell is in [`model-scores.csv`](model-scores.csv).

## 4. Results under five weight sets

| Weight set (intent) | 1st | 2nd | 3rd | 4th | 5th |
|---|---|---|---|---|---|
| W1 equal | **C** 3.60 | D 3.50 | Dc 3.00 | A 2.50 | B 2.30 |
| W2 investor (economics 25, defensibility 20, distribution 15, capital 15) | **D** 3.60 | C 3.20 | Dc 3.20 | B 2.35 | A 2.00 |
| W3 mission and risk (philanthropic 25, regulatory 20) | **C** 3.60 | D 3.55 | Dc 3.05 | B 2.40 | A 2.35 |
| W4 evidence first (time 20, reversibility 15, capital 15, regulatory 15) | **C** 4.00 | D 3.55 | Dc 2.75 | A 2.35 | B 1.95 |
| W5 distribution and moat (distribution 25, defensibility 25) | **D** 3.55 | Dc 3.25 | C 2.90 | B 2.35 | A 1.90 |

**Robustness to weights:** over 20,000 random weight vectors (Dirichlet(1,…,1), seed 20261120), the model ranked first is:

| Model | Share of draws ranked first |
|---|---|
| C | 63.4% |
| D | 36.5% |
| A | 0.1% |
| B | 0.0% |
| Dc | 0.0% |

**Robustness to single scores:**
- Changing any one cell by ±1 changes the winner only under W3. Ten cells flip it from C to D; they are C's or D's economics, regulatory, operational, philanthropic and reversibility scores.
- Under W1, a one-point cut to any C score produces a C–D tie.

## 5. What the analysis supports

1. **A and B are dominated.** This is the strongest conclusion, robust to weights and to single scores. Confidence: **Medium-High**.
   - **A** offers no structural difference. Incumbents already sell its AI enhancements, and the calibrated AI value pool at a large national is $445k [S].
   - **B** carries every sponsor burden at once: irrevocable assets, personal manager liability, distribution and a full build. Its evidence also arrives last. Its one advantage, philanthropic control, is also available in D for a program slice.
   - **Falsified if:**
     - a distribution channel appears that values an independent AI-native sponsor and gives it low-cost access to donors, for example a large wealth platform that wants a non-incumbent sponsor and will not accept a partner-sponsor structure; or
     - consumer-direct CAC data show payback (reconsideration criterion for failure pattern P3).
2. **Owning a captive sponsor (Dc) adds governance risk without adding value over D.** Dc never ranks first. The related-party pattern (RCF–Ren at 98% of individual-fundholder fees; Charityvest/Foundation Source) is legal but draws scrutiny, and it makes the bet irreversible. Confidence: **Medium**.
3. **C and D are not alternatives; they are a sequence.** Which ranks first depends on whether one weights *evidence speed and reversibility* (C) or *economics, distribution and moat* (D). Both rest on the same multi-sponsor codebase (DD-016). The derived recommendation is therefore a **staged hybrid: enter as C, earn the right to D**:
   - **Stage 1 (C).** Sell narrowly to sponsors willing to grant data access, starting with shadow-mode decisioning, continuous eligibility, reconciliation and evidence. This produces the measured exception, handling-time and break data the market lacks (Q-N03).
   - **Stage 2 (D).** Once a partner sponsor-of-record trusts that evidence, administer a whole program end to end, such as a new advisor-channel program. This captures administration economics and builds system-of-record switching costs. The provider never holds funds and never becomes the sponsor.

   Confidence that C→D beats every single-model choice: **Medium**. Confidence on which stage pays for the company: **Low**. The value pools that would pay for C beyond grant review (reconciliation, servicing, payee maintenance, evidence) are unmeasured.

## 6. Falsification criteria for the staged C→D recommendation

| If this is observed… | …then |
|---|---|
| No sponsor grants read/write data access, or incumbent vendors block it, within 12 months (Q-N04) | C fails as an entry. Go directly to D through a sponsor-of-record API partner (Endaoment or Daffy for Developers are the public examples [V]), or stop |
| Measured operating cost pools at pilot sponsors are below the S3 price (exception rate around 0.5% and low minutes; the entrant model's lower-left cell is about $21.7k/yr per 1m grants [S]) | C is a feature, not a business. Only D (administration economics) or acquisition by a consolidator remains |
| A partner sponsor requires the provider to bear sponsor-level liability or to hold funds | D fails on the never-hold-funds rule (DD-008; failure pattern P1) |
| Ren, Foundation Source or TIFIN Give ship policy-as-code, continuous eligibility and evidence exports within 12–18 months and open their data | The defensibility scores for C and D fall by about one point. The winner becomes "sell to or partner with a consolidator", which is the modal exit anyway (P2) |
| Final §4966/6033 guidance makes system-of-record owners attest controls | D gains relative to C |

## 7. What the financial model must compute for this comparison

[`../09-financial-models/`](../09-financial-models/) should produce, for each of A, B, C and D at the same scenario grid (1k / 10k / 100k / 1m accounts, with assets modeled separately):
1. **Revenue by mechanism.**
   - A and B: sponsor admin bps on assets, net of the investment layer, which accrues to managers.
   - C: per-sponsor platform fee plus per-event fees.
   - D: C revenue plus an administration fee share on program assets.
2. **Cost to serve by outcome,** with headcount from the organization floor and volume drivers: grants, contributions by complexity, and exception rates. Inference cost should be shown separately.
3. **Break-even conditions:**
   - assets needed for A and B;
   - sponsors × grant volume for C;
   - program assets for D.
4. **Capital to first decisive evidence and to break-even.**
5. **Sensitivity** to exception rate, minutes per exception, complex-asset share and the fee-share percentage in D.

Until those outputs exist, the economics row above is qualitative. If it inverts, the C/D ordering may change; the dominance over A and B is less sensitive to it.

## 8. Reconciliation with the financial model (added 2026-11-20 after 09 outputs existed)

The F# economics model ([`../09-financial-models/financial-and-staffing-models.md`](../09-financial-models/financial-and-staffing-models.md); outputs in `../09-financial-models/outputs/`) now quantifies the economics row. The model rests mostly on assumed parameters (23 of 30 [A]), so these are scenarios [S].

| Question | Model result | Effect on §5 |
|---|---|---|
| Steady-state margin at published Fidelity tiers, $300k average balance | B 59% (10k accounts), 85% (100k), 88% (1m). A 30–32%. D 17%, 70%, 77% (50% fee share [A]). C at $150/account loses money until 1m accounts served | **B's steady-state economics are the best in the grid.** "B is dominated" holds on the non-financial criteria and on the calibrated growth path below, not on steady-state margin. §5 item 1 is softened accordingly: B is *dominated on risk-adjusted time-to-evidence*, not on terminal economics |
| Peak capital to reach scale over 5 years | B calibrated to observed challenger scale (~$2bn by year 5): **$14.8m**, still cumulatively negative at year 5. B optimistic (~$15bn by year 5, no precedent in the 2021–26 cohort): $2.9m. C at $300/account with 20k-account clients: **$7.4m**, positive cumulative by year 4 (only just: +$0.5m). C at $150/account: $38.3m and never positive. C with 5k-account clients: $17.7m | Supports C-first **only if** C can price near $300/account and win mid-size sponsors. The single observed reference is RCF→Ren at about $745/account (one related-party contract). Below about $200/account, C is a feature, not a business |
| Small sponsors | A self-built AI-native sponsor at 1k accounts costs $4.87m against $1.8m revenue | The long tail is a C *customer* segment only in aggregate, through a low-touch product. It is not a standalone business (consistent with strategic synthesis §0 D) |

**Net effect:**
- The staged C→D recommendation survives.
- Its weakest link is now explicit: **price per account served and the size of the first clients.**
- B remains an option to revisit at the Phase 6 gate if D's partner sponsor-of-record terms prove unworkable, or if a distribution partner offers low-CAC access. On the optimistic acquisition path, B is the most valuable business in the grid.
