# 22 - Commercial validation plan

Status: research recommendation (2026-11-26). Each test names its hypothesis, method, cost, decision rule and the decision it informs. No outreach was performed in this initiative; outreach requires owner approval. Ordered by value of information per dollar.

## 1. Tests

| ID | Test | Hypotheses | Method | Cost | Duration | Pass / fail rule | Informs |
|---|---|---|---|---|---|---|---|
| V-1 | Win/loss interviews | HYP-001, HYP-002, HYP-003 | 10 sponsors that switched or evaluated vendors 2023-26 (start with the 6 iPhi exits, AEF, Vermont CF, CNY CF, Arizona CF); structured guide extending `commercial-opportunity/market-validation/interview-program.md` | $5-20k | 6-8 weeks | Thesis **falsified** if ≥6 of 10 name product capability (not incentives, scope or forced events) as decisive | DEC-001 |
| V-2 | Price test | DEC-006 | 5-10 sponsors: per-account licence ($81/$120/$150), service subscriptions, bps administration | $20-60k | 6-8 weeks | ≥3 accept ≥$100 per account or ≥$25k service subscription | DEC-006, DEC-008 |
| V-3 | Public-data replay harness | HYP-005, HYP-006, HYP-015 | 12 archived IRS releases + CSL/OFAC history against real Schedule I recipients; measure change rate, conflicts, auto-resolution | $30-80k | 8-10 weeks | Change rate ≤6%, auto-resolution ≥20% | DEC-003 |
| V-4 | Authorised incumbent export rehearsal | HYP-003, HYP-012 | One sponsor export under NDA through Transitus phase 1 with full per-fund reconciliation | $40-160k | 10-16 weeks | 100% money tie-out; history depth documented; freeze plan ≤5 business days | DEC-010 |
| V-5 | Contract-end calendar | HYP-011 | Public notices, 990 vendor payments, DNS changes for 50 sponsors | $5-15k | 4 weeks | ≥10 windows in 24 months | DEC-007 |
| V-6 | Channel-partner conversations | HYP-010, HYP-014 | 5 candidates: CF-software vendor, administrator, bank/trust distributor, multi-custodian data layer, league/CUSO | $5-15k | 8-12 weeks | ≥1 pilot term sheet | DEC-001, DEC-002 |
| V-7 | AI handling-time study | HYP-008 | 200 real or realistic exceptions with and without AI preparation | $20-60k | 6 weeks | Reduction ≥25% with no rise in errors | DEC-006 |
| V-8 | Charity evidence API willingness to pay | HYP-007 | 10 prospects across sponsors, administrators, CSR and payment platforms | $10-30k | 6 weeks | ≥3 of 10 at ≥$15k a year | DEC-004 |
| V-9 | Auditor walkthrough | HYP-005 | Evidence model and change-driven re-vetting reviewed by a nonprofit audit firm | $0-30k | 4 weeks | No requirement for full periodic re-review | DEC-003 |

**G0 total (V-1, V-2, V-3, V-5, V-6, V-9): about $0.07-0.25M**; with V-4, V-7, V-8: $0.15-0.5M. Combined with PR #87's gates (licence terms, counsel opinion) the evidence budget is **$0.35-0.75M**.

## 2. Evidence that would invalidate the commercial thesis (Q10)

The thesis "an AI-native entrant can win institutional DAF business through a licensed platform entered via migration and eligibility-evidence wedges" is **invalidated** if any of these holds:

1. **V-1 shows switching is driven by distribution economics only**, and no channel partner engages (V-6 fails): there is then no route to customers that technology can open.
2. **V-2 shows buyers will not pay more than ~$60 per account** for software, below MD-6's viable range at entry scale.
3. **Incumbents publish migration commitments and exit symmetry** before Unbound has a reference customer (HYP-013): the wedge disappears.
4. **V-4 shows incumbent exports cannot be obtained or cannot be reconciled** without incumbent cooperation: migration-as-a-product fails.
5. **V-3/V-9 show change-driven re-vetting is not acceptable**, and exception rates exceed ~8%: the cost advantage narrows to licensing price.
6. **Customer acquisition is slower than one customer a year** under every channel: capital exceeds $10M before cash-positive (ER-4 adverse $13.8M).

## 3. Sequencing

Weeks 0-12: V-1, V-5, V-6 in parallel (cheap, decisive), V-3 starts. Weeks 8-20: V-2, V-9, V-8. Weeks 12-28: V-4, V-7 with a design partner. Review at week 12 (DEC-001) and week 28 (DEC-002, DEC-008).
