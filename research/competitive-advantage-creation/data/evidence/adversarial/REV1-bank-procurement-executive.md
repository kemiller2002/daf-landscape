# REV1 - Bank procurement executive

Status: adversarial review, round 1 (2026-11-26). Reviewer panel REV1. Perspective: head of third-party risk management (TPRM) and vendor procurement at a regional bank with a trust department, evaluating Unbound either directly or as a fourth party behind a sponsor or distributor the bank relies on. Written independently of the other REV1 perspectives. Challenge IDs P3-CHL-REV1021..REV1028 in [adversarial-challenges.csv](../../fragments/REV1/adversarial-challenges.csv).

## Bottom line

Under the package's own plan this vendor cannot clear my onboarding until well after the month in which the model books its first signing. It has no SOC report and plans none until a term sheet, no commercial licence for its own components, a single key person, no operating history and no continuity design for customers if its channel leaves. These are not price objections; they are pass/fail gates. The package treats them as costs to be bought "at the term sheet". In my process they are preconditions to a term sheet.

## 1. SOC timing is assumed away (P3-CHL-REV1021, high, judgment with external evidence)

P3-DEC-AB004 defers the SOC 2 Type 1 audit, insurance binding and production hardening until a partner term sheet names a pilot customer; the model pays compliance one-time costs 3 months before first signing (P3-ASM-MOD020). Report 02 notes that Type 2 needs at least 3 months of observation and that this can cause a 3-12 month procurement delay ([02](../../../02-existing-unbound-economics.md):127), but the delay is not in the cashflow: A3's first signing stays at month 15 base (`sequence-values.csv`, TPL-UNB-S3 `first_signing_month` 9/15/24). Financial-services buyers commonly do not accept a Type 1 in third-party review (vendor guidance, e.g. https://bastion.tech/learn/soc2/type1-vs-type2, accessed 2026-11-26; AICPA sets no minimum window, auditors typically use 3-12 months). Any bank, trust or bank-affiliated distributor route (and most national administrators acting as partners) adds the observation window plus my review cycle. Proposed change: model first signing for regulated buyers as max(sales cycle, SOC 2 Type 2 issue date + review time) and show the effect on A3 peak cash and the kill rule.

## 2. SOC 1 belongs in the base case for a fund ledger (P3-CHL-REV1022, medium, judgment)

Report 02 puts SOC 1 ($20-120k) only in the high compliance case ([02](../../../02-existing-unbound-economics.md):72). Unbound's ledger is the system of record for DAF balances, contributions and grants: it is relevant to the sponsor's internal control over financial reporting, and the sponsor's auditor will ask for a SOC 1 Type 2 or perform its own procedures at the vendor. Report 19 shows A3 survives +$170k a year for SOC 1 plus TPSP ([19](../../../19-sensitivity-and-stress-analysis.md):127), which I accept as a cash result; but the report treats it as a stress rather than the expected requirement, and the same timing problem as REV1021 applies to the SOC 1 observation period. Proposed change: SOC 1 Type 2 in base for any ledger-of-record deployment; Type 2 timing in the schedule.

## 3. Vendor viability, key person, licence and exit (P3-CHL-REV1023, high, factual + judgment)

- **Licence.** Almost every Echelon component Unbound depends on (Forma, Folio, Limen, Strata, Conditor, Aegis) is PolyForm Noncommercial 1.0.0 with commercial terms "forthcoming" (P3-CLM-FGJ002, VERIFIED-FACT; [09](../../../09-independent-component-commercialization.md):8, 15-37). I cannot approve a vendor whose product's dependencies cannot legally be used commercially today. The package treats the intra-owner grant as cash ≈ $0 ([02](../../../02-existing-unbound-economics.md):130); my requirement is an executed licence chain and source escrow, which carry legal cost and must exist before contract.
- **Key person.** One founder (`founder_fte` = 1 in every Unbound stream; report 08 says "a two-person company", [08](../../../08-adjacent-financial-industries.md):54 — the package should pick one). The second maintainer or code approvers (A03, $79-220k) sit inside a $120k maintenance base ([02](../../../02-existing-unbound-economics.md):70), so in base the second maintainer is at most partly funded.
- **Financial condition.** No revenue, no audited financial statements, funding capacity unknown (P3-GAP-MOD001, P3-GAP-AB006). TPRM due diligence on financial condition will fail or require a parent guarantee.
- **Exit.** Continuity for a sponsor if the channel partner exits is "missing in Unbound requirements" (P3-CLM-FGJ020, [12](../../../12-institutional-distribution.md):88). A tested exit plan is a standard TPRM expectation.
Proposed change: add a "procurement admissibility" gate before G1 listing executed licence chain, escrow, second maintainer under contract, financial-condition evidence and exit plan, each with cost and lead time; stop showing these as $0.

## 4. Insurance limits are guessed and unbound (P3-CHL-REV1024, medium, judgment)

$5M combined cyber, tech E&O, D&O and crime at $30k/$70k/$160k (P3-ASM-AB016) is an ASSUMPTION with no quote, bound only at term sheet (P3-GAP-AB001). For a vendor processing donor PII and grant payment instructions I would also require crime/funds-transfer-fraud and social-engineering coverage with the bank as additional insured, and limits set by my policy rather than the vendor's budget. The low case ($30k for four lines at $5M) looks implausible for a pre-revenue vendor with no SOC report. Proposed change: obtain indicative broker quotes ($0, as report 04 suggests) before any figure is reused, and carry the low case only if a quote supports it.

## 5. Regulatory reference is stale (P3-CHL-REV1025, medium, factual omission)

The package's TPRM treatment is inherited from Phase II ("TPRM 5/5", CLM-023; [05](../../../05-untapped-institutional-markets.md):63, 196) and nowhere cites the governing guidance. On 2026-09-11 the OCC, Federal Reserve, FDIC and NCUA proposed new third-party risk management guidance to replace the 2023 interagency guidance, published at 91 FR 58536 on 2026-09-15 with comments due 2026-11-16 (https://www.federalregister.gov/documents/2026/09/15/2026-18859/proposed-third-party-risk-management-guidance; https://www.federalreserve.gov/newsevents/pressreleases/bcreg20260911a.htm; accessed 2026-11-26), plus a companion community-bank guide. Neither document is in the source register. Whatever the final text says about due diligence, subcontractor (fourth-party) oversight and termination planning will set my questionnaire. Proposed change: add the proposal as a source and an evidence gap for any bank/trust route; do not cite "TPRM 5/5" without the guidance it rests on.

## 6. Payments role is undecided and its compliance unfunded (P3-CHL-REV1026, medium, judgment)

Payment execution is deferred to a rail partner (CNV-PAY-001, PAY-DEF-001; [10](../../../10-structural-cost-elimination.md):88), but the TPSP obligation is "kept if the vendor creates ACH files" ([03](../../../03-capital-requirements-reconstruction.md):51) and the counsel opinion is postponed until a partner model is known ([04](../../../04-low-cost-commercial-validation.md):19). The base live run carries no Nacha TPSP audit. If the vendor generates payment files or instructions that a bank originates, I will treat it as a TPSP regardless of what the partner contract says. Proposed change: decide and document the payments role before G1; cost TPSP audit in base when the product produces payment files.

## 7. Security programme sized for a startup, not for a ledger vendor (P3-CHL-REV1027, medium, judgment)

Security $20k/$50k/$120k a year including a fractional vCISO and pen test ([02](../../../02-existing-unbound-economics.md):71) does not fund 24x7 monitoring, incident response retainer, or the evidence I request (BCP/DR test results, vulnerability management SLAs, access reviews). RPO 0 in region is a requirement whose benchmark has not been run ([07](../../../07-architectural-competitive-advantages.md):29); continuous control monitoring is "design only" ([07](../../../07-architectural-competitive-advantages.md):32). The model gives security a low tornado rank ([19](../../../19-sensitivity-and-stress-analysis.md):30), but the issue for me is admissibility, not cost.

## 8. Concentration on one partner and one cloud (P3-CHL-REV1028, low, judgment)

The plan accepts a single selling partner above 50% of revenue until month 36 ([12](../../../12-institutional-distribution.md):90) and a single managed PostgreSQL provider. Vendor revenue concentration is a viability risk I score; cloud concentration is a fourth-party risk I need documented. Low severity because both are disclosed; the package should add them to the procurement-admissibility gate in REV1023.

## 9. The validation cash total does not match its components (P3-CHL-REV1029, low, factual)

Report 04 totals the cheaper G0 methods at "about $1-25k" ([04](../../../04-low-cost-commercial-validation.md):22). Its own component cells sum to about $0-33k (V-1 $0-2k, V-2 $0-1k, V-3 $0-1k, V-6 $0-5k, V-7 $0-2k, buyer-access $0-15k, licence term sheet $0-7k; V-4/V-5/V-8/V-9 $0). Small in money, but it is the figure an approver will quote; the total should be recomputed from the table.
