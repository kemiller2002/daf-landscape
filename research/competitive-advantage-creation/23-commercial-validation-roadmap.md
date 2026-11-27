# 23 - Commercial validation roadmap

Status: research (2026-11-26). Reconciliation agent (RECON). This is a plan, not an authorization. **No outreach, spending or contract is authorized. Every step that contacts a buyer, partner, auditor, broker or counsel needs separate owner approval, even at $0 cash** (BRIEF; DEC-008; DEC-012). The roadmap builds on agent AB's ladder in [04](04-low-cost-commercial-validation.md), revised for model revision 2 ([14](14-commercial-sequencing.md), [16](16-capital-efficient-market-entry.md), [19](19-sensitivity-and-stress-analysis.md)). Every V-1..V-9 pass/fail rule from Phase II is kept unchanged ([22 of Phase II](../competitive-displacement/22-commercial-validation-plan.md)). Register rows: [validation-experiments.csv](data/registers/validation-experiments.csv).

## Answer in brief

1. **Learn four things before any DAF cost center opens.** Model revision 3 (CFO-corrected, after round 2) still finds that every configuration pauses at month 24 when the cost center opens at month 0, and that none beats doing nothing (`sequences-ranking.md`). Opening the cost center first would put $1.33-1.38M at risk ($1.46-1.81M in revision 2) to learn what the steps below can show for about $0-10k in cash. The four questions are:
   - **(Q0) Who performs and pays for the human deep review under licensing** (P3-DEC-MOD005; P3-GAP-RECON001). This is an owner decision, informed by what partners and sponsors expect. It sets the break-even size (`gate-break-even.md`):
     - Echelon performing M1: not reached;
     - the sponsor performing it: 3,079 single-sponsor accounts ($175k net), or a 12,457-account partner book;
     - M5: 3,169, or a 13,335-account book.

     Partner-book licensing pays back only with sponsor-performed review (month 76) or under M5 (month 80) (`bases.md`).
   - **(Q1) Revenue per customer at a named sponsor size.** Are there reachable customers or partner books at or above the break-even size for the allocation chosen in Q0? Plausible FY2024 sponsors (non-captive, not donation processors) number 17 at 2,646 accounts or more and 10 at 5,291 or more (`platform-classes.md`; P3-DEC-CE002; P3-GAP-RECON002). Revision 2 thresholds were 3,949 accounts (M5) and 10,963 (M1).
   - **(Q2) OD-CDD-02.** Will the owner let automated 180-day renewal count as the deep review, and will an auditor accept it (V-9)? With Echelon performing the review, M5 moves A3's peak from $8.26M to $2.52M (revision 3; revision 2: $8.70M to $3.46M). An attested risk-tiered review may stay within the ratified wording without OD-CDD-02, subject to counsel and V-9 (break-even 5,202 accounts; P3-GAP-RECON004) (P3-DEC-MOD004).
   - **(Q3) Named partner terms.** Is a partner willing to embed Unbound, on what share, with what exclusivity and continuity terms, and how soon (V-6; P3-DEC-EK002, P3-DEC-FGJ003)?
2. **Q0 and the first half of Q2 need no outreach.** The owner's decision on OD-CDD-02 is an internal decision. Desk replay evidence (V-3; P3-VAL-HI001, HI003, HI006) informs it; the auditor half needs the $1k tier.
3. **Q1 and Q3 cost about $0-1k in cash but need owner-approved founder conversations** (V-1, V-2, V-6). The constraint is approval, not budget.
4. **Recommended order:** $0 desk tier now, then the owner decisions, then the $1k tier with approval, then the $10k tier only if a named partner and a qualifying sponsor appear. The existing G0 budget ($150-350k) stays a ceiling, not a plan (P3-DEC-AB002).

## 1. What must be learned, mapped to tests

| Question | V-test | Phase III experiments | Pass condition (unchanged rule, or the revision-2 threshold) | If it fails |
|---|---|---|---|---|
| Q0 who performs the deep review | V-6, V-2 | Owner decision P3-DEC-MOD005; V-6/V-2 conversations ask whether sponsors expect to perform the review themselves | A recorded allocation; partners or sponsors willing to perform the review in Unbound | Echelon-performed M1 never breaks even (P3-CLM-MOD017); price the review as a separate service or stop |
| Q1 revenue per customer at a named size | V-2, V-6, V-5 | P3-VAL-CE001 ($0 desk); P3-VAL-AB004 ($0 price bounds); P3-VAL-AB013 ($10k EOIs) | V-2: ≥3 nonbinding EOIs at ≥$100/account or ≥$25k. Plus at least one candidate customer, or partner book, at or above the break-even size for the review allocation and registry mode chosen (`gate-break-even.md`) | No modelled licensing route pays back. Do not open the cost center ([21](21-commercial-thesis-invalidation.md) TI-01) |
| Q2 OD-CDD-02 and auditor acceptance | V-3, V-9 | P3-VAL-AB001, P3-VAL-HI001, P3-VAL-HI003, P3-VAL-HI006 ($0); P3-VAL-AB010 ($1k informal); P3-VAL-AB015 ($50k written) | V-3: change rate ≤6% and auto-resolution ≥20%. V-9: the auditor accepts change-driven renewal within the 180-day ceiling (DEC-003) | M1 stays governing. If Echelon performs it, break-even is not reached (revision 3); if the sponsor performs it, 3,079 accounts |
| Q3 named partner and terms | V-6 | P3-VAL-AB003 ($0 partner map); P3-VAL-AB009 ($1k); P3-VAL-AB012 ($5k demo); P3-VAL-AB014 ($25k terms) | V-6: a named partner in term-sheet talks with a pilot customer by month 6 of the cost center (OD-P3-03, OD-P3-04). Terms meet the walk-away floor (share ≤40%, partner first line, no exclusivity without a minimum, change-of-control continuity) | The kill rule pauses at month 6; the route reverts to "supplier to an acquirer" or stops ([12](12-institutional-distribution.md)) |
| Is switching distribution-driven, and what do stayers value? | V-1 | P3-VAL-AB008 ($1k) | ≥6 of 10 name product capability as decisive (supports OD-M-05). Stayers rank all hypotheses below "nothing" (wedge falsified) | Reinforces partner-first; or falsifies the wedge |
| Can incumbent exports be reconciled? | V-4 | P3-VAL-AB005 ($0 readiness); P3-VAL-AB016 ($100k real export) | 100% money tie-out on a real export | Blocks any customer with an existing book; greenfield programmes are unaffected |
| Contract-end windows | V-5 | P3-VAL-AB002 ($0 desk) | Desk calendar of windows for the qualifying sponsors in Q1 | Signings cannot be timed; reachable share falls |
| AI handling time | V-7 | P3-VAL-AB006 ($0 design check only) | Real-staff timing through a partner's pilot (not before G1) | Savings stay unmeasured; they do not feed price floors ([10](10-structural-cost-elimination.md)) |
| Charity evidence willingness to pay | V-8 | P3-VAL-AB011, P3-VAL-HI008 ($0) | ≥3 of 10 at ≥$15k a year. Expect failure: the bar is ~5.5x Candid Charity Check's entry price | Confirms P3-DEC-HI003: no standalone product |

Experiments that do not map to a V-test: P3-VAL-AB007 (security evidence), P3-VAL-HI004 (connector hours), P3-VAL-HI002 and P3-VAL-HI005 (registry inputs), and P3-VAL-HI007 (double-count check). All cost $0 and sharpen inputs.

## 2. Ladder

| Tier | Cash | What runs | Evidence | Gate to move up |
|---|---|---|---|---|
| **$0, desk, no contact (now)** | $0 | P3-VAL-CE001 sponsor-size classification (captive vs non-captive; contracted platform where public); archive monthly IRS and sanctions releases (P3-DEC-HI004); V-3 replay (P3-VAL-AB001, HI001, HI003, HI006); V-5 desk calendar; V-6 partner map and partner-side economics; public price bounds; security evidence; start the build ledger (P3-DEC-AB003) | Count and names of public organizations at or above the break-even sizes in `gate-break-even.md` (about 3,079-5,202 single-sponsor accounts; partner books of 12,457 accounts or more); replay rates; a target partner list | **Gate 0.** If no plausible sponsor or partner book reaches the break-even size for the chosen review allocation, do not proceed to outreach on licensing; record the conclusion. If V-3 fails, drop change-driven re-vetting as a cost lever |
| **Owner decisions (no cash)** | $0 | Who performs the deep review (P3-DEC-MOD005); OD-CDD-02 (P3-DEC-MOD004); cost-center definition (P3-DEC-MOD001); the build gate (P3-DEC-MOD003); funding capacity (P3-GAP-MOD001); approval of founder-led outreach (P3-DEC-AB002) | Recorded owner rulings | Approval of the $1k tier |
| **$1k (outreach approved)** | ≤$1k | V-6 first partner conversations with a size question (P3-VAL-AB009); V-1 interviews coded by a second coder (P3-VAL-AB008); informal V-9 (P3-VAL-AB010); V-8 folded in (P3-VAL-AB011) | Partner interest and terms; named books and account counts; an informal auditor view | **Gate 1.** At least one partner willing to discuss terms that meet the walk-away floor, *and* at least one candidate customer or partner book at or above break-even size for the review allocation (P3-DEC-MOD005) and mode (OD-CDD-02) the owner chose. Otherwise stop |
| **$5k** | ≤$5k | Demo on synthetic data for 2-3 partners (P3-VAL-AB012) | Partner sees a working demo; V-2 questions asked with a demo in hand | Partner asks for a term sheet |
| **$10k** | ≤$10k | V-2 nonbinding EOIs at a stated price with account counts (P3-VAL-AB013); NDA/DPA template review; independent V-1 coder | EOIs at a named size and price | **Gate 2 (cost-center entry condition, proposed).** ≥3 EOIs at ≥$100/account or ≥$25k (V-2 rule), at least one from a customer at or above break-even size, and a named partner in term-sheet talks (V-6). Only then would opening the DAF cost center be consistent with the model; the owner decides (P3-DEC-MOD003, P3-DEC-CE001) |
| **$25k-100k (after Gate 2 only)** | per [04](04-low-cost-commercial-validation.md) | Term-sheet legal review (P3-VAL-AB014); payments counsel (P3-GAP-AB003); written V-9 (P3-VAL-AB015); real export rehearsal (P3-VAL-AB016) | Signed-quality terms; written opinions; reconciliation evidence | Gate 3 (counsel and auditor), then Gate 4 (G1 entry: V-4 passes and a pilot is signed) |

## 3. Decision gates and what each one decides

| Gate | Decides | Default if not met |
|---|---|---|
| Gate 0 (desk) | Whether licensing to sponsors of break-even size is plausible at all | No outreach on licensing; Unbound work continues only as owner-funded development outside the DAF cost center, if the owner so decides (P3-DEC-MOD001) |
| Owner decisions | Review allocation, registry mode, cost-center definition and build gate | M1 governing; the clock definition stays open |
| Gate 1 ($1k) | Whether a partner route exists at viable size | Stop DAF commercialization; keep Transitus (OD-P3-02) and the $0 archive |
| Gate 2 ($10k) | Whether to open the cost center | Do not open it |
| Gates 3-4 | Whether to sign a pilot (G1) | No pilot |

## 4. What remains uncertain after the ladder

Even with Gates 0-2 passed, these remain unmeasured:
- live run cost, variable cost per account and registry volume (charities in use per account, the top driver);
- go-live and SOC 2 Type 2 timing;
- churn;
- the incumbent response.

They are measured only in a live pilot. That is why the month-24 pilot test exists, and why the model pauses every platform sequence when the pilot is late ([14](14-commercial-sequencing.md) §6).
