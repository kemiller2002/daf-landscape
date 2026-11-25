# 04: Activity cost and capacity

**Date:** 2026-11-25. **Pass:** ACT.

**Data:**
- [`activities.csv`](../../../data/commercial-opportunity/servicing-economics/activities.csv): 33 activities.
- [`approaches.csv`](../../../data/commercial-opportunity/servicing-economics/approaches.csv), [`capacity-model.csv`](../../../data/commercial-opportunity/servicing-economics/capacity-model.csv), [`staffing-steps.csv`](../../../data/commercial-opportunity/servicing-economics/staffing-steps.csv), [`verification-180.csv`](../../../data/commercial-opportunity/servicing-economics/verification-180.csv) and [`workload-tails.csv`](../../../data/commercial-opportunity/servicing-economics/workload-tails.csv).

**Regenerate:** `python3 -I -B research/commercial-opportunity/servicing-economics/scripts/activities/act_model.py .`

## Integrator conclusions

1. **No time study exists, so every handling minute is an assumption.** The activity model, Unbound's work inventory and daf-landscape's earlier process model share assumptions, so their agreement is not independent validation.
2. **Minutes per account-year (market mix):**

   | Approach | Minutes |
   |---|---:|
   | Conventional | 260 (109-692) |
   | Conventional + AI | 124 |
   | AI-native redesign | 51 (18-169) |
   | Redesign + elimination | 34 |

   Redesign and elimination create the advantage, and AI alone roughly halves conventional handling. The main levers are:
   - board-delegated approval;
   - reuse of eligibility determinations;
   - structured intake;
   - grants paid by EFT by default;
   - continuous charity monitoring.
3. **The $40 / 48-minute allowance holds only for a redesigned operation on typical, small and inactive accounts.** At the evidence-based loaded rate of **$65.45/h** (CST), $40 buys about 37 minutes, not 48. The $75 decomposition is mis-split:

   | Line | Budget | Activity model (AI-native) |
   |---|---:|---:|
   | Payments | $10 | $26 |
   | Data and identity | $10 | $2 |
   | Total | $75 | about $89 (about $65 with elimination) |

   Conventional handling costs about $217-262 per account, which is consistent with Ren's $390-815 per account price.
4. **Capacity.**
   - Each sponsor adds about 324 hours a year of sponsor-level work under AI-native handling.
   - December daily load runs about 3.1-3.3x average.
   - The core team's single operations person and single controller cannot carry December or absences.

   The F# model applies archetype December shares and buys excess December hours at the loaded rate.
5. **180-day charity re-verification.** Continuous monitoring, determination reuse and exception-only human review cost about **$1 per account-year**, against about $69 for scheduled human review. Approval-time and release-time checks remain unchanged. Recommended as requirement transfer RC-ACT-001 in report 09.
6. **How the model uses this.** Archetype minutes, external cost, payment cost and December shares feed `Parameters.fs` (`archetypeTable`, base values). The low and high cases enter as a minutes factor (0.35x / 3.33x).

> Research-pass content below was produced by a role-separated agent pass from the same model family as the integrator. It is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate.

## ACT-0 Summary and verdict

**Question.** Is $75 per account-year incremental cost, including $40 of labour (48 minutes at $50/h), realistic for an AI-native servicer administering DAFs for sponsors that keep reserved legal decisions?

**Answer (conditional; no time study exists anywhere in the evidence base, EV-ACT-029).**
1. **48 minutes is achievable only for an AI-native *redesigned* operation on a book dominated by typical and small accounts.** Modelled market-mix servicer labour [D from A]: conventional **260 min** (109-692), conventional+AI **124** (46-351), AI-native redesign **51** (18-169), redesign+elimination **34** (12-115). The base AI-native figure sits on the allowance; the plausible range spans 0.4x to 3.5x it.
2. **By archetype (AI-native base):** dormant 3 min, small recurring 22, typical 38, high-value 105, high-frequency grantmaker 134, complex-asset donor 359. The allowance holds for inactive, small and typical accounts and fails 2-7x for the other three. Workload follows grants, exceptions and complex gifts, not assets.
3. **The $75 total is wrongly allocated rather than simply too low or too high.** Market mix AI-native: labour $42, payments **$26** (vs $10: check grants at ~$4 and securities receipts dominate), data/identity **$2** (vs $10: per-account variable data cost is small; licences are fixed), cloud+AI **$4** (vs $5), other **$15** (vs $10: complex-asset intermediary fees and expected fraud loss). Total **$89** (AI-native) / **$65** (with elimination levers: EFT default, structured transfers, e-delivery). If bank and rail fees are sponsor pass-throughs (CNV-PAY-001: sponsor originates payments), the servicer's own incremental cost is ~$60-65.
4. **Conventional operation cannot be priced at $75.** Typical account conventional ~$217/yr; market mix ~$262 (labour 260 min). Cross-check: Vanguard Charitable staff intensity is ~413 min/account-year across all functions [D, EV-ACT-021]; Ren outsourced administration is priced at $413-745/DAF-year (EV-ACT-020).
5. **Step-fixed hiring arrives earlier than the budget says.** At 5,000 accounts and 5 sponsors (AI-native base): ~4,200 variable hours + ~1,600 sponsor-level hours; beyond core capacity that is **4 additional hires** (budget assumed ~2.5 FTE), **13 in the high case**. December at the same service levels needs **~10 ops FTE-equivalents** (~5.7 with a deferral policy).
6. **The 180-day charity re-verification is the hidden cost driver in conventional form** (~82 min/typical account-year if done by humans on a fixed schedule). Continuous monitoring, evidence reuse and exception-only human review bring it to **~1 min / ~$1.1 per account-year** without weakening the legally required checks, which happen at approval and release in every approach.
7. **Price mismatch.** At 20 bps a small recurring giver ($8k) yields $16 against ~$36 incremental cost (AI-native). A minimum fee or activity component is needed. High-value accounts subsidise everything else.

Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate. Every minute value is [A] unless noted. Same-model reasoning (this model, Unbound's inventory and daf-landscape's process model share assumption lineage) is **not independent validation**.

## ACT-1 Scope, method and boundaries

- **Servicer scope:** outsourced administration; the sponsor keeps legal ownership, variance power and reserved decisions (A3+ authority, CNV-GOV-004); no custody or investment management (budget doc line 4, EV-ACT-001). Servicer minutes = preparation, processing, exceptions handled up to the decision, service and controls. Sponsor-retained minutes (decisions on exceptions, gift acceptance, succession) are reported separately and **not** charged to the $40.
- **Unit:** expected servicer minutes per occurrence, averaged over all occurrences including zero-touch ones, x occurrences per account-year (activities.csv). Per-sponsor work (close, configuration, audit support, board reporting, incidents, onboarding, migration) is in hours per sponsor and **excluded** from per-account minutes, as the budget doc requires (line 34).
- **Approaches:** conventional (today's manual sponsor/administrator practice); conventional+AI (same workflow, AI assistance); AI-native redesign (structured intake, deterministic rules under board delegation, determination reuse, continuous monitoring, exception-only humans; AI prepares and may add flags, never clears them, EV-ACT-041); elimination (redesign plus removing work where legally and financially sound: EFT default, structured transfer references, e-delivery, intermediary routing, event-driven rather than scheduled re-verification).
- **Archetypes:** dormant, small recurring giver, typical, high-frequency grantmaker, high-value concentrated, complex-asset donor; market mix 20/20/40/7/10/3% [A-ACT-014].
- **Model:** `model/act_model.py` (pure functions; `python3 -I -B model/act_model.py .`), `model/gen_outputs.py`, `model/gen_report.py`. Arithmetic is reproducible; inputs are not measurements.
- **Public replay caution:** Unbound's replay (11.2% routed, 64%/72% reuse, 4.0%/3.1% effective) is **recipient-level Schedule I rows above $5,000**, not production grant automation and not handling time (EV-ACT-017). It is used only as a prior for eligibility-exception incidence.

## ACT-2 What is observed vs assumed

**Observed volume anchors (grants per account-year, [D] = stated grants / DAF accounts; periods differ by up to 12 months):**

| Sponsor | Grants | Accounts | Grants/account | Evidence |
|---|---:|---:|---:|---|
| Jewish Communal Fund | 89,485 | 4,842 | 18.5 | EV-ACT-011 |
| Fidelity Charitable | 2,664,446 (CY2024) | 204,614 | 13.0 | EV-ACT-003 |
| DAFgiving360 | 1,100,000 (FY2024) | 112,188 | 9.8 | EV-ACT-004 |
| Vanguard Charitable | 221,825 (FY2024) | 27,660 | 8.0 | EV-ACT-005 |
| National Philanthropic Trust | 129,575 (FY2024) | 17,940 | 7.2 | EV-ACT-006 |
| Goldman Sachs Philanthropy Fund | 29,254 | 4,134 | 7.1 | EV-ACT-010 |
| American Endowment Foundation | 109,708 (derived) | 15,947 | 6.9 | EV-ACT-007 |
| Renaissance Charitable Foundation | 160,000 | 25,824 | 6.2 | EV-ACT-008 |
| ImpactAssets | 13,500 | 2,197 | 6.1 | EV-ACT-012 |
| Morgan Stanley GIFT | 122,000 | 21,800 | 5.6 | EV-ACT-009 |

Other observed anchors: Fidelity ~13.2 grants per charity per year at its scale (3M grants / 226,823 charities, EV-ACT-013); ~500 complex gifts per year at Fidelity, ~0.0024 per account-year (EV-ACT-014); Fidelity EFT share 67% in 2025, 33% checks (EV-ACT-015); DAFgiving360 38% of grants recurring (EV-ACT-043); December: Schwab one-quarter of grants, Fidelity ~60% of contributions in Q4 (2015 press, grade C, EV-ACT-016); disclosed fraud losses $0.3-0.6m per event (EV-ACT-034); revocations 1.7 per 1,000 recipient rows per year, IRS posting lag median 89 days, sanctions alerts 0.9 vs 10.5 per 1,000 names depending on matcher (EV-ACT-018).

**Not observed anywhere public (all [A]):** contributions per account, human contact rates per account (searched; none, EV-ACT-042), handling minutes for any activity, per-grant exception rates (EV-ACT-029), break rates, ACH return and uncashed-check rates, complex-gift hours, sponsor-side payment rail prices.

## ACT-3 Activity inventory (typical account, minutes per account-year, base)

| ID | Activity | Typical conv | AI-enhanced | AI-native | Elimination | Legally required | Human judgment | Quality |
|---|---|---|---|---|---|---|---|---|
| ACT-A01 | Account opening (KYC, agreement, sanctions at onboarding) | 3.0 | 1.2 | 0.36 | 0.24 | partly | only for entity donors, nonstandard terms, identity mismatch | D |
| ACT-A02 | Contributions: cash/ACH/card | 3.0 | 1.0 | 0.3 | 0.2 | Y | unidentified or returned items only | D |
| ACT-A03 | Contributions: paper checks | 3.0 | 1.5 | 0.75 | 0.38 | Y (once accepted) | illegible/unidentified items | D |
| ACT-A04 | Contributions: publicly traded securities (DTC/ACATS) | 12.0 | 5.0 | 2.0 | 1.0 | Y | unidentified incoming transfers | D |
| ACT-A05 | Complex / noncash assets (private stock, LP, real estate, crypto) | 2.16 | 1.44 | 0.9 | 0.36 | Y (Form 8283/8282, s4943 holdings; sponsor gift-acceptance policy) | Y (gift acceptance is a reserved sponsor decision) | C |
| ACT-A06 | Recurring contribution set-up and changes | 0.4 | 0.15 | 0.03 | 0.03 | N | N | D |
| ACT-A07 | Grant recommendation intake | 9.0 | 3.6 | 0.9 | 0.45 | partly | N for structured entries | B |
| ACT-A08 | Charity verification at approval and release (transaction-time status check) | 9.0 | 2.7 | 0.27 | 0.18 | Y | Only on mismatch/absence from lists | B |
| ACT-A09 | 180-day charity re-verification (deep review renewal) | 82.12 | 27.38 | 1.08 | 0.67 | N (sponsor policy, not statute) | Only when evidence changed, conflicts or is missing | B |
| ACT-A10 | Event-driven charity monitoring (revocation, name/EIN change, list delta, adverse news) | 0.45 | 0.3 | 0.23 | 0.23 | partly | Y (adverse events need judgment) | B |
| ACT-A11 | Grant approval incl. eligibility exceptions (servicer prepares; sponsor decides reserved cases) | 42.3 | 24.3 | 12.6 | 12.6 | Y | Y for exceptions (reserved decision for sponsor) | C |
| ACT-A12 | Purpose / prohibited-benefit review (s4967, pledges, tickets) | 4.5 | 3.24 | 2.43 | 2.43 | Y | Y (judgment on flagged cases) | D |
| ACT-A13 | Non-standard grantee due diligence (foreign, expenditure responsibility, fiscal sponsors) | 9.0 | 6.3 | 5.4 | 1.8 | Y | Y | C |
| ACT-A14 | Payment processing: EFT/ACH grant | 2.99 | 1.8 | 0.6 | 0.85 | N (rail choice is policy) | only returns and destination changes | C |
| ACT-A15 | Payment processing: check grant (print, positive pay, mail) | 8.91 | 5.94 | 3.56 | 0.54 | N | N | B |
| ACT-A16 | Payment processing: wire (large / international) | 0.67 | 0.45 | 0.27 | 0.27 | N | Y (release authorisation) | D |
| ACT-A17 | Returned / uncashed / voided checks and reissue | 2.67 | 1.78 | 1.34 | 0.2 | partly | partly (escheat vs reissue decision) | D |
| ACT-A18 | Reconciliation (bank, custodian, ledger; break resolution) | 9.2 | 4.6 | 1.15 | 1.15 | Y (for audited financial statements; CNV-FIN-004) | breaks only | D |
| ACT-A19 | Fee calculation and billing | 1.0 | 0.3 | 0.05 | 0.05 | N (contractual) | N | D |
| ACT-A20 | Statements and contribution acknowledgments (s170(f)(8)/(18)) | 3.0 | 1.0 | 0.2 | 0.1 | partly | N | D |
| ACT-A21 | Donor / advisor service contacts (human-handled) | 5.0 | 2.98 | 2.0 | 2.0 | partly (complaint handling CNV-PLT-005) | partly | D |
| ACT-A22 | Investment interfaces (allocation changes, custodian/advisor feeds) | 1.5 | 0.6 | 0.2 | 0.2 | N | N | D |
| ACT-A23 | Fraud investigation (account takeover, payment redirection, BEC) | 0.36 | 0.3 | 0.24 | 0.24 | partly | Y | C |
| ACT-A24 | Sanctions screening alert disposition | 2.0 | 1.31 | 0.17 | 0.17 | Y | Y (match disposition) | B |
| ACT-A25 | Account changes (address, advisor, bank, contact channel) | 1.8 | 0.9 | 0.3 | 0.3 | partly | only on risk | D |
| ACT-A26 | Succession, death, successor advisors | 1.2 | 0.9 | 0.7 | 0.7 | Y | Y | D |

Per-occurrence minutes (low/base/high) for each approach, frequencies, legal basis, external cost, controls and evidence are in `activities.csv` (26 per-account + 7 per-sponsor activities). Biggest conventional items for a typical account: 180-day re-verification done by people (82 min), grant approval incl. exceptions (42), securities identification (12), grant intake (9), charity lookup (9), reconciliation (9), non-standard diligence (9), check grants (9). After redesign the residual is dominated by **exception decisions prepared for the sponsor (A11: 12.6 of 38 min)**, non-standard diligence (5.4) and check payments (3.6).

## ACT-4 Four approaches: where the structural advantage is

| Activity | Winner | Why | Elimination sound? |
|---|---|---|---|
| Grant intake (A07) | Redesign | Structured purpose/attestation removes re-keying and chasing; AI on email intake only speeds a bad channel | Yes, with accessible alternatives |
| Charity status at approval/release (A08) | Elimination of manual lookup | Exact-match deterministic check on a continuous subscription; AI adds nothing (P06 modal D, P=0.94) | Yes; check itself stays |
| 180-day re-verification (A09) | Redesign | Automated renewal on unchanged evidence; human only on change; ~98% fewer minutes | Partly: dropping the schedule only for IRS-listed public charities with clean evidence and counsel agreement |
| Grant approval/exceptions (A11) | Redesign + reuse; AI packets on exceptions | Board delegation (CNV-GRT-001) removes routine human approval; reuse cuts first-time exceptions from ~11% to ~4% (replay prior) | No: reserved decision |
| Non-standard diligence (A13) | AI-assisted (+ intermediary routing) | Document-heavy, low-volume: the one place AI is modal (P07) | Partly (route foreign grants via US intermediaries) |
| Complex assets (A05) | AI-assisted document reading | Judgment is the product; AI extracts appraisal/8283/LP terms | No; outsourcing to an intermediary is a cost transfer, not a saving (CNV-ECO-001) |
| Checks (A15/A17) | Elimination of the rail | Check ~$4 and 3-4 min incl. returns vs ACH ~$0.30 and ~0.1 min | Yes as policy (EFT default, checks on request) |
| Reconciliation (A18) | Deterministic redesign | Exact match auto-pass + sampled attestation | No: attestation required |
| Statements/receipts (A20) | Deterministic automation | Content rules; e-delivery default | Paper on request only |
| Service contacts (A21) | Redesign (proactive status) + AI assist | Removes 'where is my grant' contacts; humans for complaints and exceptions | No |
| Sanctions (A24) | Better deterministic matching | Token-weighted matcher cuts alerts ~12x at similar recall (replay) | No |

**Pattern:** conventional+AI captures roughly half the conventional minutes (124 vs 260 mix); the structural advantage (to ~51, then ~34) comes from **redesign and elimination, not AI**. AI's incremental contribution is concentrated in exceptions, non-standard diligence and complex assets, the same narrow set the repository's process model found (process-economics-summary.md:24-38). Full text per activity in `approaches.csv`.

## ACT-5 Per-account labour and $75 decomposition by archetype and approach

| Archetype | Approach | Servicer min/acct-yr base (low-high) | x 48-min | Labour $ @$50/h | Payments $ | Data/identity $ | Cloud+AI $ | Other $ | Incremental total $ | FTE per 1,000 accts | Sponsor-retained min | Revenue @20 bps $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| inactive | conventional | 15.8 (6.2-38.8) | 0.33 | 13.18 | 0.72 | 0.06 | 3.0 | 1.91 | 18.87 | 0.194 | 0.6 | 40.0 |
| inactive | ai_enhanced | 7.3 (2.7-18.4) | 0.15 | 6.05 | 0.72 | 0.06 | 3.04 | 1.91 | 11.79 | 0.089 | 0.6 | 40.0 |
| inactive | ai_native | 3.0 (1.1-9.2) | 0.06 | 2.54 | 0.72 | 0.06 | 3.04 | 1.91 | 8.27 | 0.037 | 0.4 | 40.0 |
| inactive | elimination | 2.6 (1.0-7.6) | 0.05 | 2.17 | 0.39 | 0.06 | 3.04 | 1.9 | 7.56 | 0.032 | 0.4 | 40.0 |
| small_recurring | conventional | 168.9 (68.0-407.4) | 3.52 | 140.77 | 11.08 | 1.55 | 3.0 | 2.08 | 158.48 | 2.07 | 4.9 | 16.0 |
| small_recurring | ai_enhanced | 70.5 (26.0-180.1) | 1.47 | 58.78 | 11.08 | 1.55 | 3.39 | 2.08 | 76.88 | 0.864 | 4.9 | 16.0 |
| small_recurring | ai_native | 21.5 (7.3-70.1) | 0.45 | 17.88 | 11.08 | 1.52 | 3.37 | 2.08 | 35.92 | 0.263 | 3.3 | 16.0 |
| small_recurring | elimination | 16.2 (5.3-51.4) | 0.34 | 13.47 | 6.57 | 1.51 | 3.37 | 1.94 | 26.86 | 0.198 | 3.3 | 16.0 |
| typical | conventional | 220.2 (90.6-590.6) | 4.59 | 183.54 | 25.43 | 1.85 | 3.0 | 3.31 | 217.13 | 2.699 | 7.6 | 300.0 |
| typical | ai_enhanced | 101.0 (35.8-291.0) | 2.1 | 84.13 | 25.43 | 1.85 | 3.91 | 3.31 | 118.63 | 1.237 | 7.6 | 300.0 |
| typical | ai_native | 38.0 (12.6-135.6) | 0.79 | 31.68 | 25.43 | 1.8 | 3.88 | 3.31 | 66.09 | 0.466 | 5.2 | 300.0 |
| typical | elimination | 27.3 (9.3-95.5) | 0.57 | 22.78 | 15.94 | 1.79 | 3.88 | 3.0 | 47.39 | 0.335 | 5.2 | 300.0 |
| high_frequency | conventional | 832.8 (346.2-2232.1) | 17.35 | 694.02 | 91.65 | 6.78 | 3.0 | 6.98 | 802.44 | 10.206 | 32.6 | 800.0 |
| high_frequency | ai_enhanced | 376.4 (132.9-1083.7) | 7.84 | 313.65 | 91.65 | 6.78 | 6.31 | 6.98 | 425.37 | 4.613 | 32.6 | 800.0 |
| high_frequency | ai_native | 133.6 (44.6-482.1) | 2.78 | 111.3 | 91.65 | 6.54 | 6.22 | 6.98 | 222.69 | 1.637 | 22.3 | 800.0 |
| high_frequency | elimination | 94.6 (32.2-335.5) | 1.97 | 78.87 | 50.04 | 6.5 | 6.22 | 5.64 | 147.27 | 1.16 | 22.3 | 800.0 |
| high_value | conventional | 464.3 (187.3-1331.5) | 9.67 | 386.91 | 54.21 | 2.71 | 3.0 | 19.99 | 466.83 | 5.69 | 16.0 | 6000.0 |
| high_value | ai_enhanced | 232.2 (83.5-714.1) | 4.84 | 193.49 | 54.21 | 2.71 | 5.58 | 19.99 | 275.99 | 2.845 | 16.0 | 6000.0 |
| high_value | ai_native | 105.0 (35.4-373.5) | 2.19 | 87.5 | 54.21 | 2.62 | 5.44 | 19.99 | 169.76 | 1.287 | 11.3 | 6000.0 |
| high_value | elimination | 74.7 (26.9-261.7) | 1.56 | 62.28 | 38.6 | 2.6 | 5.44 | 19.49 | 128.42 | 0.916 | 11.3 | 6000.0 |
| complex_asset | conventional | 1010.2 (482.7-2581.5) | 21.04 | 841.8 | 40.43 | 1.96 | 3.0 | 352.3 | 1239.48 | 12.379 | 68.7 | 3000.0 |
| complex_asset | ai_enhanced | 618.7 (291.4-1598.4) | 12.89 | 515.55 | 40.43 | 1.96 | 4.65 | 352.3 | 914.88 | 7.582 | 68.7 | 3000.0 |
| complex_asset | ai_native | 359.0 (140.8-918.4) | 7.48 | 299.13 | 40.43 | 1.9 | 4.44 | 352.3 | 698.18 | 4.399 | 51.0 | 3000.0 |
| complex_asset | elimination | 166.0 (77.2-506.7) | 3.46 | 138.3 | 30.0 | 1.89 | 4.44 | 351.96 | 526.59 | 2.034 | 51.0 | 3000.0 |
| market_mix | conventional | 260.1 (108.5-692.3) | 5.42 | 216.73 | 25.58 | 1.87 | 3.0 | 15.18 | 262.36 | 3.187 | 10.1 | 877.2 |
| market_mix | ai_enhanced | 124.1 (46.4-351.3) | 2.58 | 103.39 | 25.58 | 1.87 | 3.99 | 15.18 | 150.01 | 1.52 | 10.1 | 877.2 |
| market_mix | ai_native | 50.7 (17.6-168.7) | 1.06 | 42.27 | 25.58 | 1.81 | 3.95 | 15.18 | 88.78 | 0.622 | 7.0 | 877.2 |
| market_mix | elimination | 33.8 (12.2-114.9) | 0.7 | 28.14 | 16.03 | 1.8 | 3.95 | 14.87 | 64.79 | 0.414 | 7.0 | 877.2 |

Notes: payments include ACH $0.30, check grants $4 all-in, wires $25, securities receipt $10, lockbox $0.65 [A-ACT-016]. Other includes complex-asset intermediary fee $350/gift and expected fraud loss $1.20/account [A-ACT-017]. Conventional rows carry no AI cost. Revenue uses assumed average balances (market mix arithmetic mean $877k is pulled up by the 10% high-value accounts) and must not be read as an AUA forecast. FTE per 1,000 accounts = min x 1,000 / 60 / (1,600 h x 0.85).

## ACT-6 Verdict on the $40 / 48-minute allowance

| Archetype | Conventional | Conv.+AI | AI-native | +Elimination | Verdict |
|---|---|---|---|---|---|
| Dormant | 16 | 7 | 3 | 3 | Realistic in every approach |
| Small recurring | 169 | 71 | 22 | 16 | Realistic only redesigned; fails conventionally (12 ACH debits, 6 grants) |
| Typical | 220 | 101 | 38 (13-136) | 27 | Realistic redesigned at base; high case 2.8x |
| High-frequency grantmaker | 833 | 376 | 134 | 95 | Not realistic (2-3x even with elimination) |
| High-value concentrated | 464 | 232 | 105 | 75 | Not realistic; more Tier-2 triggers, wires, complex gifts |
| Complex-asset donor | 1,010 | 619 | 359 | 166 | Not realistic; 1 complex gift = 2-12 h |
| **Market mix** | **260** | **124** | **51 (18-169)** | **34 (12-115)** | **On the line only with redesign; plausible range 0.4-3.5x** |

**What moves the AI-native market-mix figure from 51 min (one-at-a-time):** complex-asset hours 12 instead of 5 -> 66; no determination reuse (8% x 30 min) -> 62; replay raw rate without reuse at 45 min (11.2% x 45) -> 87; Fidelity-level grant frequency (13 per typical account) -> 65; no contact deflection -> 53; fewer grants per recipient (2.5) -> 52. The figure is most sensitive to **exception incidence x minutes, complex-gift hours and grant frequency**, all unmeasured.

**Rate check.** $50/h is below the budget's own grant-ops loaded rate ($100k / 1,600 h = $62.50/h, EV-ACT-002), below compliance reviewer rates ($55-73/h, EV-ACT-023), and above the 990 median ($38.87/h). Queue utilisation of 85% makes the effective rate ~$59/h per worked minute. At $62.50/h, 48 minutes costs $50, not $40. **Recommendation:** keep 48 min as a *redesigned typical-account* target, not a portfolio average; budget $45-60 labour per mix account, add an activity charge for high-frequency, complex-asset and international work, and treat conventional operation (~$200+/account) as the failure case.

## ACT-7 Full $75 decomposition: realistic or not

| Line | Budget | AI-native mix [D] | Elimination mix [D] | Typical AI-native | Verdict |
|---|---:|---:|---:|---:|---|
| External payments | 10 | 25.6 | 16.0 | 25.4 | **Too low** unless checks fall to ~5% and securities receipt fees are custodian-absorbed; 9 grants x (67% ACH $0.30 + 33% check $4) alone is ~$14. Who pays: if the sponsor's bank originates (CNV-PAY-001) these are **sponsor pass-throughs**, not servicer cost |
| Data / identity | 10 | 1.8 | 1.8 | 1.8 | **Too high per account, but mis-specified:** variable cost is identity at onboarding ($3 x new share), screening and status feeds; enriched charity data and sanctions vendors are **fixed licences** per platform (Candid licence terms are a known constraint, Unbound SPT-008) |
| Cloud | 5 | 4.0 | 4.0 | 3.9 | **About right**; inference immaterial (<$1/account, EV-ACT-039; Unbound EV-09) |
| Labour | 40 | 42.3 | 28.1 | 31.7 | Right for redesigned typical/small books; **3-9x short** for high-frequency, high-value and complex-asset archetypes; conventional ~$217 |
| Other | 10 | 15.2 | 14.9 | 3.3 | **Too low for mixes with complex-asset donors** ($350/gift intermediary fees, often fund-borne under CNV-GRT-013); typical account ~$3 |
| **Total** | **75** | **88.8** | **64.8** | **66.1** | Plausible for a redesigned typical book; ~$89 for the assumed mix; $150-700 for heavy archetypes |

**Range (market mix):** AI-native total ~$62 (low minutes) to ~$187 (high minutes) holding external costs; conventional ~$135-$625.

## ACT-8 Capacity, step-fixed hiring and core vs additional staff

| Approach | Accounts | Sponsors | Case | Min/acct | Variable h | Sponsor-level h | Hours beyond core (1,600 h) | Step-fixed hires (1,360 h each) | Dec ops FTE same SLA | Dec ops FTE with deferral | Hours funded by $40/acct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| conventional | 1000 | 1 | base | 260.1 | 4335 | 800 | 3535 | 3 | 8.25 | 4.54 | 800 |
| conventional | 1000 | 1 | high | 692.3 | 11538 | 1720 | 11658 | 9 | 21.95 | 12.07 | 800 |
| conventional | 5000 | 1 | base | 260.1 | 21675 | 800 | 20875 | 16 | 41.24 | 22.68 | 4000 |
| conventional | 5000 | 1 | high | 692.3 | 57692 | 1720 | 57812 | 43 | 109.76 | 60.37 | 4000 |
| conventional | 5000 | 5 | base | 260.1 | 21675 | 4000 | 24075 | 18 | 41.24 | 22.68 | 4000 |
| conventional | 5000 | 5 | high | 692.3 | 57692 | 8600 | 64692 | 48 | 109.76 | 60.37 | 4000 |
| conventional | 10000 | 1 | base | 260.1 | 43350 | 800 | 42550 | 32 | 82.48 | 45.36 | 8000 |
| conventional | 10000 | 1 | high | 692.3 | 115383 | 1720 | 115503 | 85 | 219.53 | 120.74 | 8000 |
| conventional | 10000 | 5 | base | 260.1 | 43350 | 4000 | 45750 | 34 | 82.48 | 45.36 | 8000 |
| conventional | 10000 | 5 | high | 692.3 | 115383 | 8600 | 122383 | 90 | 219.53 | 120.74 | 8000 |
| conventional | 25000 | 1 | base | 260.1 | 108375 | 800 | 107575 | 80 | 206.19 | 113.41 | 20000 |
| conventional | 25000 | 1 | high | 692.3 | 288458 | 1720 | 288578 | 213 | 548.81 | 301.85 | 20000 |
| conventional | 25000 | 5 | base | 260.1 | 108375 | 4000 | 110775 | 82 | 206.19 | 113.41 | 20000 |
| conventional | 25000 | 5 | high | 692.3 | 288458 | 8600 | 295458 | 218 | 548.81 | 301.85 | 20000 |
| conventional | 50000 | 1 | base | 260.1 | 216750 | 800 | 215950 | 159 | 412.38 | 226.81 | 40000 |
| conventional | 50000 | 1 | high | 692.3 | 576917 | 1720 | 577037 | 425 | 1097.63 | 603.69 | 40000 |
| conventional | 50000 | 5 | base | 260.1 | 216750 | 4000 | 219150 | 162 | 412.38 | 226.81 | 40000 |
| conventional | 50000 | 5 | high | 692.3 | 576917 | 8600 | 583917 | 430 | 1097.63 | 603.69 | 40000 |
| ai_native | 1000 | 1 | base | 50.7 | 845 | 324 | 0 | 0 | 2.06 | 1.13 | 800 |
| ai_native | 1000 | 1 | high | 168.7 | 2812 | 830 | 2042 | 2 | 6.85 | 3.77 | 800 |
| ai_native | 5000 | 1 | base | 50.7 | 4225 | 324 | 2949 | 3 | 10.29 | 5.66 | 4000 |
| ai_native | 5000 | 1 | high | 168.7 | 14058 | 830 | 13288 | 10 | 34.24 | 18.83 | 4000 |
| ai_native | 5000 | 5 | base | 50.7 | 4225 | 1620 | 4245 | 4 | 10.29 | 5.66 | 4000 |
| ai_native | 5000 | 5 | high | 168.7 | 14058 | 4150 | 16608 | 13 | 34.24 | 18.83 | 4000 |
| ai_native | 10000 | 1 | base | 50.7 | 8450 | 324 | 7174 | 6 | 20.58 | 11.32 | 8000 |
| ai_native | 10000 | 1 | high | 168.7 | 28117 | 830 | 27347 | 21 | 68.48 | 37.67 | 8000 |
| ai_native | 10000 | 5 | base | 50.7 | 8450 | 1620 | 8470 | 7 | 20.58 | 11.32 | 8000 |
| ai_native | 10000 | 5 | high | 168.7 | 28117 | 4150 | 30667 | 23 | 68.48 | 37.67 | 8000 |
| ai_native | 25000 | 1 | base | 50.7 | 21125 | 324 | 19849 | 15 | 51.45 | 28.3 | 20000 |
| ai_native | 25000 | 1 | high | 168.7 | 70292 | 830 | 69522 | 52 | 171.21 | 94.16 | 20000 |
| ai_native | 25000 | 5 | base | 50.7 | 21125 | 1620 | 21145 | 16 | 51.45 | 28.3 | 20000 |
| ai_native | 25000 | 5 | high | 168.7 | 70292 | 4150 | 72842 | 54 | 171.21 | 94.16 | 20000 |
| ai_native | 50000 | 1 | base | 50.7 | 42250 | 324 | 40974 | 31 | 102.91 | 56.6 | 40000 |
| ai_native | 50000 | 1 | high | 168.7 | 140583 | 830 | 139813 | 103 | 342.41 | 188.33 | 40000 |
| ai_native | 50000 | 5 | base | 50.7 | 42250 | 1620 | 42270 | 32 | 102.91 | 56.6 | 40000 |
| ai_native | 50000 | 5 | high | 168.7 | 140583 | 4150 | 143133 | 106 | 342.41 | 188.33 | 40000 |
| elimination | 1000 | 1 | base | 33.8 | 563 | 324 | 0 | 0 | 1.3 | 0.71 | 800 |
| elimination | 1000 | 1 | high | 114.9 | 1915 | 830 | 1145 | 1 | 4.42 | 2.43 | 800 |
| elimination | 5000 | 1 | base | 33.8 | 2817 | 324 | 1541 | 2 | 6.5 | 3.57 | 4000 |
| elimination | 5000 | 1 | high | 114.9 | 9575 | 830 | 8805 | 7 | 22.09 | 12.15 | 4000 |
| elimination | 5000 | 5 | base | 33.8 | 2817 | 1620 | 2837 | 3 | 6.5 | 3.57 | 4000 |
| elimination | 5000 | 5 | high | 114.9 | 9575 | 4150 | 12125 | 9 | 22.09 | 12.15 | 4000 |
| elimination | 10000 | 1 | base | 33.8 | 5633 | 324 | 4357 | 4 | 13.0 | 7.15 | 8000 |
| elimination | 10000 | 1 | high | 114.9 | 19150 | 830 | 18380 | 14 | 44.18 | 24.3 | 8000 |
| elimination | 10000 | 5 | base | 33.8 | 5633 | 1620 | 5653 | 5 | 13.0 | 7.15 | 8000 |
| elimination | 10000 | 5 | high | 114.9 | 19150 | 4150 | 21700 | 16 | 44.18 | 24.3 | 8000 |
| elimination | 25000 | 1 | base | 33.8 | 14083 | 324 | 12807 | 10 | 32.49 | 17.87 | 20000 |
| elimination | 25000 | 1 | high | 114.9 | 47875 | 830 | 47105 | 35 | 110.45 | 60.75 | 20000 |
| elimination | 25000 | 5 | base | 33.8 | 14083 | 1620 | 14103 | 11 | 32.49 | 17.87 | 20000 |
| elimination | 25000 | 5 | high | 114.9 | 47875 | 4150 | 50425 | 38 | 110.45 | 60.75 | 20000 |
| elimination | 50000 | 1 | base | 33.8 | 28167 | 324 | 26891 | 20 | 64.98 | 35.74 | 40000 |
| elimination | 50000 | 1 | high | 114.9 | 95750 | 830 | 94980 | 70 | 220.89 | 121.49 | 40000 |
| elimination | 50000 | 5 | base | 33.8 | 28167 | 1620 | 28187 | 21 | 64.98 | 35.74 | 40000 |
| elimination | 50000 | 5 | high | 114.9 | 95750 | 4150 | 98300 | 73 | 220.89 | 121.49 | 40000 |
**Reading.** Core staff in the 5-FTE budget can absorb ~1,600 hours a year of variable and sponsor-level work (grant/client operations 960 h + controller 640 h [A-ACT-013]); the controller cannot approve their own preparation (budget doc line 31). Everything above that is **additional servicing capacity**, hired in steps of ~1,360 queue hours.
- **Per 1,000 accounts (market mix):** conventional 3.2 FTE, conv.+AI 1.5, AI-native 0.62 (0.21-2.07), elimination 0.41. Per typical account 0.47 FTE/1,000 redesigned.
- **Per sponsor (recurring, AI-native):** ~324 h/yr base (160-830) for close and controller sign-off, configuration, audit support, board reporting and incidents = **0.24 FTE per sponsor** (0.6 high); conventional 800 h (0.59 FTE). One-off onboarding ~300 h + migration ~150 h + 2 min/account. A 1,000-account sponsor carries ~324 sponsor-level hours against ~845 account-driven hours (+38%); ten such sponsors add ~3,200 hours (~2.4 FTE) that a single 10,000-account sponsor would not: small sponsors are capacity-expensive.
- **Budget comparison:** the budget says 5,000 funds -> 4,000 hours ~ 2.5 FTE. The model gives 4,225 variable hours at base AI-native (close to the allowance) but adds sponsor-level hours, so additional hires are **3-4 at base, 10-13 in the high case, 16-18 conventionally**. The organisation is not five people beyond ~2,500 accounts.
- **Hiring triggers (AI-native base, mix):** first additional ops hire at ~2,000-2,500 accounts with 1-5 sponsors; then roughly one per 1,600 accounts; first exception specialist (compliance-grade, $55-73/h) needed once exception preparation exceeds ~0.5 FTE, i.e. ~3,000-3,500 mix accounts (A11 ~13 min/account at 4% effective incidence x 30 min).

## ACT-9 December peak and absence capacity

**Seasonal profile [E].** December share of annual volume: grants ~25% (Schwab), contributions ~35% (Fidelity ~60% in Q4; BofA ~2/3 Nov-Dec), contacts ~25%, other ~10% (EV-ACT-016, 2015 press, grade C; A-ACT-011). December has ~20 of ~250 working days (8%), so December daily load is **~3.1-3.3x average for AI-native** (redesign removes deferrable work, so the remaining work is more seasonal) and ~2.6x conventionally (2.8x conv.+AI). Complex-asset donors run ~4x (late-December securities/complex gifts). **Peak week** (last ~4.5 working days) contribution intake is **~8x average daily** (5-12x) [E: 12-15% of annual contributions in 4.5 days, A-ACT-012].

**Capacity required (market mix, AI-native base, from staffing-steps.csv):** 5,000 accounts -> ~10 ops FTE-equivalents in December at year-round service levels vs ~3 average; 10,000 -> ~21; 25,000 -> ~51. With a **deferral policy** (grant SLA up to 10 business days in December, as Fidelity already discloses 10+ days; statements, schedule changes and scheduled renewals moved to January) -> ~5.7 / 11 / 28 [A-ACT-018].

**What is legally time-critical in December:** recording the completed-gift date and accepting contributions (donor deductions); sanctions screening before release; contemporaneous acknowledgments can follow in January (s170(f)(8) timing). DAF grant payment has **no December 31 legal deadline**; the December grant surge is a service-level choice. This is the main lever for avoiding a large seasonal bench.

**Absence.** The core budget has **one** grant/client operations person and one controller: a single absence in December removes most core variable capacity, and the controller cannot cover preparation they then review. Unbound requires roster coverage with a double-absence December stress test and a December readiness gate with pre-appointed qualified reviewers (CNV-GOV-004, CNV-SVC-002). The budget's $60k seasonal/backup line buys ~770 contractor hours at ~$78/h (30% premium [A]), about **6 December FTE-months**. At ~5,000 accounts the December surge above average staffing is ~2.6 FTE-months with deferral and ~7 at year-round SLAs, so the line covers the deferral case **only if** contractors are trained, pre-appointed and, under CNV-GOV-004, exclusive to one sponsor. With 5 sponsors the exclusivity rule can multiply the bench (RC-ACT-002). Unbound's pooled-queue simulation puts full December exception SLA for an administrator at ~2x base queue staff for ~+$5/fund-year (EV-ACT-030), which is consistent in order of magnitude but shares assumptions with this model.

## ACT-10 Workload tails

| Approach | Archetype | Share of accounts | Min/acct | Share of total minutes | Ratio to mix average |
|---|---|---|---|---|---|
| conventional | inactive | 0.2 | 15.8 | 0.012 | 0.06 |
| conventional | small_recurring | 0.2 | 168.9 | 0.13 | 0.65 |
| conventional | typical | 0.4 | 220.2 | 0.339 | 0.85 |
| conventional | high_frequency | 0.07 | 832.8 | 0.224 | 3.2 |
| conventional | high_value | 0.1 | 464.3 | 0.179 | 1.79 |
| conventional | complex_asset | 0.03 | 1010.2 | 0.117 | 3.88 |
| ai_native | inactive | 0.2 | 3.0 | 0.012 | 0.06 |
| ai_native | small_recurring | 0.2 | 21.5 | 0.085 | 0.42 |
| ai_native | typical | 0.4 | 38.0 | 0.3 | 0.75 |
| ai_native | high_frequency | 0.07 | 133.6 | 0.184 | 2.63 |
| ai_native | high_value | 0.1 | 105.0 | 0.207 | 2.07 |
| ai_native | complex_asset | 0.03 | 359.0 | 0.212 | 7.08 |
- **AI-native: 3% of accounts (complex-asset donors) consume ~21% of servicer minutes; 10% high-value consume ~21%; 7% high-frequency consume ~18%.** Together, 20% of accounts drive ~60% of the work. Conventionally the typical archetype dominates (34%) because routine work has not been removed. Redesign *concentrates* cost in the tails.
- **Per-event tails:** one complex gift 2-30 h (A05); one fraud investigation 1-8 h plus a potential $0.3-0.6m loss event (EV-ACT-034); one succession 15-120 min; one foreign/ER grant 30-240 min plus follow-up reporting.
- **Implications:** (1) price complex assets and international grants as activity fees or route them to intermediaries with fund-borne charges (a transfer, not a saving); (2) asset-based pricing partly tracks the high-value tail but **not** high-frequency grantmakers with moderate balances, or complex-asset donors whose assets have been liquidated and granted out; (3) the distribution of grants per account matters more than its mean, and no sponsor publishes it.

## ACT-11 180-day charity verification: continuous monitoring + reuse + exception-only review

| Policy | Grants per recipient | Renewals per account-yr | Human min per renewal | $ per verification | Min per account-yr | $ per account-yr |
|---|---|---|---|---|---|---|
| V1 conventional human deep review every 180 days (refresh 30 | 2.5 | 8.76 | 15 | 12.52 | 132.12 | 110.28 |
| V1 conventional human deep review every 180 days (refresh 30 | 4.0 | 5.47 | 15 | 12.52 | 82.58 | 68.92 |
| V1 conventional human deep review every 180 days (refresh 30 | 13.2 | 1.66 | 15 | 12.52 | 25.02 | 20.89 |
| V2 AI-assembled evidence packet, human signs each renewal | 2.5 | 8.76 | 5 | 4.19 | 44.28 | 37.08 |
| V2 AI-assembled evidence packet, human signs each renewal | 4.0 | 5.47 | 5 | 4.19 | 27.68 | 23.17 |
| V2 AI-assembled evidence packet, human signs each renewal | 13.2 | 1.66 | 5 | 4.19 | 8.39 | 7.02 |
| V3 continuous monitoring + automated renewal + exception-onl | 2.5 | 4.32 | 0.4 | 0.35 | 2.09 | 1.83 |
| V3 continuous monitoring + automated renewal + exception-onl | 4.0 | 2.7 | 0.4 | 0.35 | 1.31 | 1.14 |
| V3 continuous monitoring + automated renewal + exception-onl | 13.2 | 0.82 | 0.4 | 0.35 | 0.4 | 0.35 |
| V4 event-driven assurance + transaction-time critical checks | 2.5 | 3.6 | 0.3 | 0.27 | 1.44 | 1.27 |
| V4 event-driven assurance + transaction-time critical checks | 4.0 | 2.25 | 0.3 | 0.27 | 0.9 | 0.8 |
| V4 event-driven assurance + transaction-time critical checks | 13.2 | 0.68 | 0.3 | 0.27 | 0.27 | 0.24 |
**Can it be done without weakening compliance? Yes, under conditions; the legally load-bearing checks are not the scheduled review.**
- The legally relevant control is recipient eligibility **at approval and at release** (s4966 taxable-distribution rules; CNV-GRT-003 requires both, against the latest IRS releases, failing safe when stale). These stay in every approach (A08, deterministic, ~0.03 min/grant).
- The 180-day interval is a **sponsor policy proposal, not a statute or safe harbor** (decision record line 4, EV-ACT-033). Its purpose is a periodic comprehensive refresh of evidence beyond status (identity, aliases, payment destination, adverse facts).
- **Redesign:** continuous monitoring of IRS releases and sanctions deltas (event-driven invalidation, A10), automatic renewal when authoritative evidence is unchanged, human review only on change, conflict or missing evidence, plus 1% independent sampling. Lazy renewal (only recipients with pending or scheduled grants) cuts renewals from 2.43 to ~1.2 per recipient-year.
- **Cost:** conventional human review ~$12.50 per verification and **~$69 per typical account-year** (82 min) at 4 grants per recipient; AI-assisted ~$4.20 / ~$23; continuous + exception-only **~$0.35 / ~$1.14** (1.3 min); event-driven only ~$0.27 / ~$0.80. At Fidelity-like overlap (13.2 grants per recipient) all approaches fall about 3x; at small-platform overlap (2.5) they rise about 1.6x.
- **Conditions:** (1) sponsor counsel approves source hierarchy and that unchanged authoritative evidence renews without human sign-off (CA-180-08, CNV-GRT-001 delegation); (2) nonstandard classes (churches absent from lists, 6.6% of replay rows; Type I/II SOs; fiscal sponsors; foreign; ER) keep a scheduled human review, sponsor-configurable shorter cadence (CA-180-17); (3) payment destination verified separately (CNV-PAY-002); (4) stale/unavailable source means Unknown, not Eligible (fail safe); (5) sampling and false-clearance metrics are reported to the board (CNV-GOV-008).
- **Limits no approach removes:** IRS revocation posting lag (median 89 days, EV-ACT-018) bounds what any monitoring can see; 72 replay rows (0.5/1,000) went to recipients already revoked at year start; listed name with a clean public-charity EIN was caught 88/100 times in the replay safety test. These are **data-source and identity-matching limits**, not staffing limits. Human scheduled review does not fix them either.

## ACT-13 Cross-checks and independence

| Comparator | Value | Relation to this model | Independent? |
|---|---|---|---|
| Unbound simplification work inventory (143 activities) | 227.5 conventional / 33.1 minimum-touch min/account-yr [D, EV-ACT-026] | This model 260 / 34-51 | **No**: same assumption family (daf-landscape FSM volumes reused) |
| Unbound convergence E5 administrator cost | $192-299 per fund-yr staffed offer at 10k funds (EV-ACT-020 context) | This model's incremental $65-89 excludes fixed staff/platform | Partly (shared parameters) |
| Vanguard Charitable all-staff intensity | ~413 min/account-yr (119 employees, 27,660 accounts) [D, EV-ACT-021] | Above conventional servicer ops (260) as expected: includes investment, marketing, management | Yes (990 data), but all-function |
| AEF / NPT staff intensity | ~900 / ~1,530 min/account-yr | Higher-touch, larger accounts | Yes, all-function |
| Ren outsourced administration price | $413-745 per DAF-year (floors) | Conventional servicer cost ~$260 incremental + fixed + margin is consistent | Yes (990 contractor data) |
| Operating cost per grant | $55 (DAFgiving360) - $574 (GS) (EV-ACT-022) | All-in, not labour | Yes |

The model passes order-of-magnitude checks against public all-function data; it is **not validated** on the quantity that matters (minutes per activity). Agreement with Unbound reflects shared inputs.

## ACT-14 Limitations and measurements needed

**Limitations.** No time-and-motion study exists for any DAF sponsor or administrator (EV-ACT-029; Unbound CNV-EVB-001). Every minute value is [A]. Exception incidence is a recipient-level prior (replay), not per-grant production data; non-eligibility exceptions (purpose, benefit, s4958) are unmeasured. Contribution counts and contact rates per account have no public source (EV-ACT-042). December shares come from 2015 press. Payment and data unit prices are mostly assumptions; sponsor-side rail pricing is unverified. Archetype mix and balances are assumptions. Same-model reasoning; no independent reviewer.

**Measurements that would settle the $40 question (priority order):**
1. **Per-grant event log at 2-3 sponsors/administrators** (de-identified, 12 months): recommendation -> eligibility -> exception reason -> reviewer touches and active minutes -> approval authority -> payment rail -> return/reissue -> donor follow-ups (taxonomy N0-N8 in the exception doc). Yields exception incidence by class, minutes p50/p90/p99, reuse share.
2. **Grants and contributions per account distribution** (not means): counts by balance band and by month (December and peak-week shares).
3. **Contact log**: human contacts per account-year by reason and channel; deflectable share ('where is my grant').
4. **Complex-gift case files**: hours by asset class, intermediary fees, elapsed days.
5. **Payment rail costs and failure rates** from sponsor bank/rail invoices: ACH return, check void/uncashed, reissue, positive-pay exceptions, PayPal/Chariot sponsor-side fees.
6. **Charity registry churn**: distinct recipients per account, grants per recipient by platform size, adverse-event rate per recipient-year, share of renewals with changed evidence.
7. **Sponsor-level hours**: monthly close, audit support, configuration changes, incident hours per sponsor.
8. **December staffing actuals**: temporary staff, overtime, backlog age at 31 Dec and 15 Jan.
A 90-day study of 3-5 sponsors with stratified sampling (exception doc lines 56-59) would replace most [A] labels in `activities.csv`.

## ACT-15 Files, top findings and open gaps

**Files:** activities.csv (33 activities), approaches.csv (15), capacity-model.csv (28 archetype x approach rows), staffing-steps.csv (176 scenario rows), verification-180.csv (36), workload-tails.csv (24), requirements-candidates.jsonl (9), evidence.jsonl (44), assumptions.jsonl (18), report.jsonl, model/act_model.py, model/act_meta.py, model/gen_outputs.py, model/gen_report.py, model/activity-minutes-typical.csv.

**Most consequential findings:** (1) 48 min holds only for a redesigned operation on typical/small/dormant accounts; mix 51 min (18-169), conventional 260. (2) Redesign and elimination, not AI, create the advantage; AI matters on exceptions, non-standard diligence and complex assets. (3) The $75 split is wrong: payments ~$16-26 not $10; data ~$2 variable (licences are fixed); other ~$15 with complex assets; total ~$65-89 redesigned. (4) Additional hires begin at ~2,000-2,500 accounts; sponsor-level work (~0.24 FTE per sponsor) makes many small sponsors expensive; December needs ~3x average capacity unless grant SLAs are relaxed. (5) 180-day re-verification costs ~$69/account-yr by people vs ~$1 with continuous monitoring and exception-only review; the legal checks at approval/release are unchanged.

**Biggest open evidence gaps:** per-grant exception incidence and minutes; contact rates; contributions per account; complex-gift hours; December/peak-week shares newer than 2015; sponsor-side payment rail prices; grants-per-recipient overlap at servicer scale.
