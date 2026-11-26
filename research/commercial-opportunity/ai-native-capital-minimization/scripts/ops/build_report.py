"""OPS group: report.jsonl, evidence.jsonl, assumptions.jsonl from _metrics.json and the CSVs.
Run after build_ops.py: python3 -I -B build_report.py <out_dir>
"""
import csv
import json
import sys
from collections import Counter

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
M = json.load(open(f"{OUT}/_metrics.json"))
rd = lambda n: list(csv.DictReader(open(f"{OUT}/{n}")))
RM, WE, HT, WT, ST, OV, AI = (rd(n) for n in ("responsibility-matrix.csv", "work-elimination.csv", "handling-targets.csv", "workload-tails.csv", "staffing-capacity.csv", "overhead.csv", "ai-capabilities.csv"))
ACC = "2026-11-25"
SE = "/home/user/daf-landscape/data/commercial-opportunity/servicing-economics"
CL = "/home/user/unbound/requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl"
PF = "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/Parameters.fs"

EV = [
    ("AI-native typical-account baseline minutes per account-year (sum of ACT-A01..A26 typical_min_per_acct_yr_ai_native)", f"{M['typical_base']:.2f}", "min/account-yr", f"{SE}/activities.csv", "prior study register (assumption-derived)", "n/a", "B", "[M] summed by build_ops.py; underlying minutes are [A]"),
    ("Market-mix minutes per account-year: conventional 260.1, AI-native 50.7, elimination 33.8", "50.7", "min/account-yr", f"{SE}/capacity-model.csv", "prior study register", "n/a", "B", "[D from A] in prior study; elimination scenario counts transfers as eliminated"),
    ("Productive hours per FTE-year 1,520 and queue utilisation 0.9", "1520; 0.9", "h; ratio", f"{PF}:145,148", "prior model source", "n/a", "B", "itself [D/A]; derivation in report 03:111 deducts ~15% meetings/admin"),
    ("Prior hiring triggers: ops manager per 6 added ops beyond 4; integration engineer and implementation analyst per 8 live sponsors; fund accountant per 15,000 accounts; compliance officer above 10,000 accounts", "", "rule", f"{PF}:154-159,170", "prior model source", "n/a", "A", "read"),
    ("Grant & client operations specialist loaded cost", "99478", "USD/yr", f"{SE}/role-compensation.csv", "prior register citing BLS OEWS May 2025 + ECEC", "OEWS May 2025", "B", "$1.0908 per productive minute [D]"),
    ("SPD-ADV-001: no team may exercise legally reserved authority for more than one sponsor", "", "owner decision", "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/23-EXECUTIVE-FINDINGS.md:13", "Unbound owner decision (requirements)", "2026-11-24", "A", "contractual/design constraint, not law"),
    ("CNV-GOV-004: reserved (A3+) authority only by board-appointed persons; vendor staff SHALL NOT hold A3+; one-sponsor rule; double absence tested in December", "", "clause", f"{CL}:38", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-GRT-001: deterministic approval only after board delegation naming a delegate; otherwise individual batch decisions on AI-prepared dossiers", "", "clause", f"{CL}:20", "Unbound adopted clause", "2026-11-24", "A", "cites s4966(d)(3) fund managers"),
    ("CNV-GOV-003: three-distinct-person release until auditor and board accept deterministic gate; reconciliation outside payment chain", "", "clause", f"{CL}:37", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-FIN-004: continuous reconciliation; exact matches auto-pass; independent risk-stratified attestation; monthly controller sign-off; new sources 100% review for one close cycle", "", "clause", f"{CL}:4", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-AIO-001: AI may recommend and prepare, never execute reserved actions; release-1 agent-executable set only reversible internal actions at A2 or below; AI unavailability must not stop deterministic paths", "", "clause", f"{CL}:63", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-AIO-002: dossier deterministic section AI cannot edit; batch approval refused with unresolved trigger", "", "clause", f"{CL}:74", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-GRT-006: screening at onboarding, delta, release; true match never auto-closed; 31 CFR 501.603/604 report data within 10 business days; fail closed on stale list", "10", "business days", f"{CL}:25", "Unbound adopted clause citing 31 CFR 501", "2026-11-24", "B", "regulation not read directly in this pass"),
    ("CNV-GRT-011: Tier-2 triggers; decision quality by risk-stratified error-bound sampling with qualified independent reviewers", "", "clause", f"{CL}:30", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-PLT-010: two approvers on every control-relevant change, neither the author", "2", "approvers", f"{CL}:77", "Unbound adopted clause", "2026-11-24", "A", "implies >=3 qualified engineers (author + 2) [D]"),
    ("CNV-GOV-001: SOC 1 type 2 readiness before first staffed-administration client; manual procedures replaced by generated evidence only after auditor confirms reliance", "", "clause", f"{CL}:35", "Unbound adopted clause (AT-C 320)", "2026-11-24", "A", "read"),
    ("CNV-SVC-002: December surge plan with pre-contracted, pre-appointed reviewers; practical capacity by role; utilisation is not productivity", "", "clause", f"{CL}:58", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-EVB-001: exception incidence and handling time need a 90-day time study before values are treated as validated", "", "clause", f"{CL}:62", "Unbound adopted clause", "2026-11-24", "A", "every minute here remains a scenario assumption"),
    ("CNV-GOV-006: every mandatory human step records justification; accessibility, financial integrity, audit, compliance non-removable; never automatic bypass", "", "clause", f"{CL}:55", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-GOV-008: quarterly board report on delegated automation; delegation expiry <=12 months; renewal refused without acknowledgment", "12", "months", f"{CL}:67", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("Exception rates for grant approval: 11.2% raw recipient rows, 4.0% effective first-time within sponsor, 3.1% platform (public-data replay)", "3.1", "% of grants", f"{SE}/activities.csv (ACT-A11 exception_rate)", "prior register citing Unbound replay", "n/a", "B", "replay on public data, recipient-level, >$5k only; not a time study"),
    ("Microsoft 365 telemetry: average employee spends 57% of intentional M365 time communicating (23% meetings, 19% chat, 15% email); heaviest 25% spend 8.8 h/wk on email and 7.5 h/wk in meetings", "57", "% of M365 time", "https://www.microsoft.com/en-us/worklab/work-trend-index/will-ai-fix-work", "vendor research (telemetry)", "28 days to March 2023", "C", "measures M365 app time, not all work; not small firms; not overhead per se"),
    ("Asana Anatomy of Work 2023: 58% of workday on 'work about work', 33% skilled, 9% strategic; unnecessary meetings 2.8 h/wk (knowledge workers), 3.6 h/wk (senior leaders); n=9,615", "58", "% of workday", "https://www.computerworld.com/article/1620398/unnecessary-meetings-draining-employee-productivity-report.html", "secondary report of vendor survey", "survey published March 2023", "C", "self-reported, vendor-sponsored, broad definition; primary release (businesswire) returned 403"),
    ("Prior productive-hours derivation deducts ~15% for internal meetings, supervision, admin; December temps can only prepare, not release", "15", "%", "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/03-organization-and-budget.md:111", "prior study report", "n/a", "B", "[D/A] in prior study"),
    ("Echelon capability status: component monolith DAF application 'planned'; monitoring/logging 'absent'; shared engineering organisation 'absent'", "", "status", f"{SE}/echelon-capabilities.csv (ECH-08, ECH-13, ECH-01)", "prior register", "n/a", "A", "no case/event/control runtime exists"),
    ("Echelon component repositories are engineering tooling (repository OS, code quality, security discipline, UI, auth), not DAF operations software", "", "observation", "/home/user/echelon-components/{praxis,dokimos,tutela,vigila,summa,fides,arca}/README.md", "repository READMEs", "n/a", "A", "[M] README heads read 2026-11-25"),
    ("Simultaneous-failure worked example: exception handle time x2 during AI outage; 0.02 unknown-state cases per account in vendor outage; 2-FTE ops floor is the weakest point", "0.02", "cases/account", "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/07-THEORETICAL-COST-FLOOR.md (WE-2)", "Unbound simulation (assumption-driven)", "n/a", "C", "simulation, not observation"),
    ("December share of annual AI-native minutes, market mix", "0.265", "share", f"{SE}/capacity-model.csv", "prior register", "n/a", "C", "[D from A]; December interval arrivals unmeasured (CNV-EVB-001)"),
    ("Fidelity still issued 33% of grants by check in 2025 (as cited in prior register)", "33", "%", f"{SE}/activities.csv (ACT-A15 eliminable)", "secondary via prior register", "2025", "C", "not re-verified here"),
    ("Model B economic fixed cost incl. second ops person", "1740000", "USD/yr", "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/10-executive-findings.md (Q6)", "prior study", "n/a", "B", "[D/A]"),
    ("CNV-LEG-001: no custody, no unilateral payment control, no investment advice; sponsor delegates to external manager", "", "clause", f"{CL}:41", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-GRT-013: complex-asset gifts via agent intermediary; sponsor donee of record; fund-borne charges", "", "clause", f"{CL}:32", "Unbound adopted clause", "2026-11-24", "A", "title and opening read"),
    ("CNV-GRT-003: status at approval and release; deep review 180 days default; event-triggered invalidation; fail safe when stale", "180", "days", f"{CL}:22", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("CNV-ECO-005: economics must include a pre-delegation phase (no deterministic approval, three-person release, manual NAV checks)", "", "clause", f"{CL}:66", "Unbound adopted clause", "2026-11-24", "A", "read"),
    ("Zero-deviation attribute sample size at 95% confidence and 5% tolerable deviation", "59", "items", "n = ceil(ln 0.05 / ln 0.95)", "derived (standard binomial result)", "n/a", "A", "[D] computed in build_ops.py"),
]
EVJ = [{"evidence_id": f"EV-OPS-{i:03d}", "claim": c, "value": v, "unit": u, "source_url_or_path": s, "source_type": t, "filing_period": fp, "accessed": ACC, "quality": q, "notes": n}
       for i, (c, v, u, s, t, fp, q, n) in enumerate(EV, 1)]

AS = [
    ("Post-redesign minutes per activity in work-elimination.csv", "see CSV", "min", "", "", "Judgement applied to prior AI-native minutes; no time study", "EV-OPS-001;EV-OPS-018", "high: A11 alone is 9.5 of 23.1 typical minutes"),
    ("Grants per account-year, market mix", f"{M['mix_grants']:.1f}", "grants", "6", "13", "0.5/4/9/40/15/10 by archetype x prior shares", "EV-OPS-002", "floor scales linearly"),
    ("Platform-effective exception rate used for the floor", "3.1", "%", "2", "8", "public-data replay; core proxy 7.4-7.8%", "EV-OPS-021", "each +1 pt adds ~0.9 min servicer + 0.45 sponsor"),
    ("Servicer dossier review per exception / sponsor decision", "10 / 5", "min", "5 / 3", "30 / 15", "assumption", "EV-OPS-008", "high"),
    ("Accounts per sponsor for allocating sponsor-level control minutes", "4000", "accounts", "1000", "20000", "target segment 5,000-50,000 funds (CNV-ECO-004) discounted for early sponsors", "EV-OPS-007", "sponsor-level minutes per account vary 0.6-12.7"),
    ("Independent sampling handling time per item", "4", "min", "2", "10", "assumption", "EV-OPS-035", "low"),
    ("Share of December volume in the last 7 working days", "0.5", "share", "0.35", "0.65", "assumption; December interval arrivals unmeasured", "EV-OPS-028", "high for core headcount"),
    ("Load multiplier during AI outage", "1.6", "x", "1.3", "2.0", "WE-2 uses x2 on exception handling; deterministic paths continue", "EV-OPS-027", "medium"),
    ("January clearance window for December backlog", "10", "working days", "5", "40", "service expectation, not law (acknowledgments only need to precede filing)", "EV-OPS-017", "core 9 (10 days) / 8 (20) / 6 (40) at 10k accounts, 2 surge"),
    ("Pre-contracted prep-only surge in December", "2", "FTE", "0", "6", "CNV-SVC-002 surge plan", "EV-OPS-017;EV-OPS-024", "medium"),
    ("Conventional small-firm coordination overhead", f"{M['ovh_conv']:.1f}", "h/FTE/week", "8", "14", "category build-up informed by WTI telemetry and Asana survey (both broader measures)", "EV-OPS-022;EV-OPS-023;EV-OPS-024", "medium"),
    ("AI-native residual coordination overhead", f"{M['ovh_res']:.2f}", "h/FTE/week", "3", "6", "governance meetings, SoD approvals, documentation, escalations remain", "EV-OPS-019", "low vs prior model (6 h already assumed)"),
    ("Onboarding learning curve", "85% (b=0.234)", "Wright curve", "80%", "95%", "assumption; applies only to repeat counterparties and standard packs", "", "medium"),
    ("New counterparty adapter effort / upkeep", "160-400 / 20-40", "h / h per adapter-year", "", "", "assumption", "", "medium"),
    ("Engineering on-call and change-control floor", "3", "people", "2", "4", "CNV-PLT-010 author + 2 approvers", "EV-OPS-015", "fixed cost"),
    ("Manager span of control", "6-8", "direct reports", "5", "10", "assumption", "", "low"),
    ("Pre-delegation additional minutes per account-year", f"{M['pre_deleg_add']:.1f}", "min", "8", "25", "1 min batch review + 3 x 0.1 min release per grant + 2 min calibration/NAV", "EV-OPS-034", "high in year 1 of each sponsor"),
    ("Reconciliation break rate for recon FTE sizing", "0.5", "% of transactions", "0.2", "3", "activities.csv ACT-A18 1% (0.2-3%) reduced by structured references", "EV-OPS-010", "low (recon is <0.4 FTE even at 50k accounts)"),
    ("Accessibility accommodations", "1% of accounts x 30 min", "", "0.5%", "3%", "assumption", "EV-OPS-019", "low"),
    ("Average loaded cost per worked hour for overhead valuation", "82", "USD/h", "60", "110", "$150k / 1,830 worked h", "EV-OPS-005", "linear"),
]
ASJ = [{"assumption_id": f"A-OPS-{i:03d}", "statement": s, "value": v, "unit": u, "low": lo, "high": hi, "basis": b, "evidence_ids": e, "sensitivity": se}
       for i, (s, v, u, lo, hi, b, e, se) in enumerate(AS, 1)]


def tbl(head, rows):
    return "| " + " | ".join(head) + " |\n|" + "---|" * len(head) + "\n" + "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in rows)


perf = Counter(r["performer_type"] for r in RM)
human = sum(1 for r in RM if r["human_required"] == "y")
A = [r for r in WE if r["activity_id"].startswith("ACT-A")]
topA = sorted(A, key=lambda r: -float(r["minutes_eliminated"]))[:8]
grid = M["staff_grid"]
peaks = M["peaks"]
be = lambda k: f"${M[k]/1e9:.2f}B"

SECTIONS = [
    ("Summary", f"""**Group OPS. Question:** if the DAF servicer is designed from outcomes, with deterministic software and AI from day one, how much human work remains, and does that change the economics?

**Answer: the redesign removes about 40% of the remaining servicer minutes (about 31% eliminated, about 10% transferred to others). It does not produce a different kind of company.** Account-level minutes fall from 50.7 to about **{M['mix_after']:.0f} per account-year** at market mix [D from A]. That is **{M['mix_base']-M['mix_after']-M['mix_trans']:.1f} minutes eliminated plus {M['mix_trans']:.1f} transferred** to donors, charities, intermediaries and auditors; transfers are not counted as eliminated. The control floor is about **{M['floor_servicer']:.0f} servicer minutes** plus {M['floor_sponsor']:.1f} sponsor-appointed minutes, of which about {M['floor_legal']:.0f} are legal, independence or control work. Below roughly 15 minutes (floor plus sponsor-level work), control would have to be weakened.

**Why the economics barely move:**
- **Minutes are a small cost.** At market mix and 20 bps, labour at 50.7 minutes is about $55 of $877 revenue per account-year (6%) [D]. With Model B fixed cost, break-even assets move from {be('be_prior')} (50.7 minutes) to {be('be_after')} (redesign) and {be('be_zero')} at zero minutes (simplified one-line sensitivity, not a reproduction of the F# model). Fixed control, engineering, assurance and sales costs decide break-even, not handling time.
- **Indivisibility and independence set headcount at small scale.** Below about 3,000-5,000 accounts, the two-operations-person dual-control floor, a controller, three engineers for two-approver change control (CNV-PLT-010), an independent reviewer and named sponsor appointees are needed whatever the minutes.
- **Above about 5,000 accounts, December sets headcount, not the annual average.** With 26.5% of minutes in December, clearing the 31 December backlog within 10 January working days needs about {grid[2]['servicing_fte_december_sizing']} core servicing FTE at 10,000 accounts, against {grid[2]['servicing_fte_annual_sizing']} on annual sizing [D from A].
- **Every new sponsor starts in pre-delegation.** Without board delegation, three-person release and 100% calibration review apply, adding about {M['pre_deleg_add']:.0f} minutes per account-year. Year-1 reality is about 45-75 minutes, not 30.

**Verdict on the premise.** An outcome-designed servicer is a better-controlled, somewhat cheaper version of the same business. Its advantage over incumbents is evidence and control quality more than cost. Most of the levers (continuous charity monitoring, EFT default, proactive status, generated reports) are available to incumbents too.""")
    ,
    ("Method and labels", f"""- **Inputs:** prior ACT activity register (33 activities), prior capacity model, prior F# Parameters.fs, Unbound convergence clauses (82, read directly) and SPD-ADV-001.
- **Order of methods per activity:** prevent > eliminate > consolidate > simplify > deterministic automation > AI > human.
- **Typical-account recomputation:** each activity's AI-native minutes are re-estimated as after-minutes, eliminated minutes and transferred minutes. The script asserts that after + eliminated + transferred = baseline. Two activities (A10 monitoring, A14 EFT) **increase**.
- **Market mix:** reconstructed from archetypes. Known top-3 activities are scaled by their own ratios and the remainder by the typical ratio ({M['ratio_typical']:.3f}) [D].
- **Capacity:** {M['queue_min_fte_yr']:.0f} queue minutes per FTE-year (1,520 h x 0.9 x 60, prior model) and ${M['usd_per_min']:.4f} per minute.
- **Labels:** [S] sourced, [A] assumption, [D] derived, [E] estimate, [M] measured.
- **Time study:** none exists, so every minute is [A] (CNV-EVB-001).
- **Independence:** same model family as the prior study, so this is not independent validation.
- **Reproduce:** `python3 -I -B build_ops.py .`, then `python3 -I -B build_report.py .`.""")
    ,
    ("Part 1: Outcome register and responsibility matrix", f"""**{len(set(r['outcome_id'] for r in RM))} outcomes** and **{len(RM)} elements**, covering decisions, information, controls and actions. Of these, **{human} elements require a person**.

Elements by performer type:

{tbl(['performer type', 'elements'], sorted(perf.items(), key=lambda x: -x[1]))}

Added beyond the brief's list:
- audit and assurance;
- records retention and privacy;
- succession and disputes;
- sponsor governance (delegation);
- payment exceptions and unclaimed property;
- policy change control;
- vendor management;
- donor disclosures and communications;
- workforce coverage;
- the servicer's own billing.

**Human elements that cannot be removed, and why:**

| Element | Basis |
|---|---|
| Exception-grant decisions, gift acceptance, delegation adoption, block/reject, successor recognition | Sponsor-appointed authority: IRC 4966/4967 exclusive legal control via CNV-GRT-001; CNV-GOV-004 bars vendor staff from A3+ authority; SPD-ADV-001 makes appointees exclusive to one sponsor |
| Sanctions match disposition | 31 CFR 501.603/604 via CNV-GRT-006; never auto-closed |
| Clearing prohibited-benefit flags | AI may flag, never clear |
| Payment release | Three distinct persons until the auditor and board accept the deterministic gate (CNV-GOV-003) |
| Reconciliation attestation, decision-quality sampling, board-report samples | Independent reviewer (CNV-FIN-004, CNV-GRT-011, CNV-GOV-008) |
| Monthly completeness sign-off | Controller (ICFR/SOC 1 expectation) |
| Control-relevant code changes | Two approvers who are not the author (CNV-PLT-010) |
| ACH origination | The sponsor is Originator (NACHA, CNV-PAY-001); the servicer is a third-party service provider |

**Design consequence: the servicer cannot be 'AI plus a few staff'.** It is staff plus contracted specialists plus **sponsor-side appointees**, whose time is a real cost to the buyer ({M['floor_sponsor']:.1f} minutes per account-year at the floor).""")
    ,
    ("Part 2: Work elimination", f"""**Typical account:** {M['typical_base']:.2f} -> **{M['typical_after']:.2f}** minutes per account-year. Of the {M['typical_base'] - M['typical_after']:.2f} removed, **{M['typical_elim']:.2f} are eliminated** and **{M['typical_trans']:.2f} are transferred**.

The prior 'elimination' scenario reached {M['prior_elim_typical']:.2f} but booked check-to-EFT and foreign-grant routing as elimination.

**Market mix:** {M['mix_base']:.1f} -> **{M['mix_after']:.1f}**, with {M['mix_trans']:.1f} transferred [D/E].

Largest eliminations (typical account):

{tbl(['activity', 'baseline', 'after', 'eliminated', 'transferred', 'to'], [(r['activity_id'] + ' ' + r['activity'][:45], r['baseline_minutes_ai_native'], r['minutes_after'], r['minutes_eliminated'], r['minutes_transferred'], r['transferred_to'][:40]) for r in topA])}

**Evaluated levers:**
- **Continuous reconciliation** (A18): -0.45. It was already in the AI-native baseline; the independent sample stays.
- **Transaction-time audit evidence** (S04): -1,100 minutes per sponsor-year, **only after the auditor confirms reliance** (CNV-GOV-001), plus 300 minutes transferred to the sponsor's auditor.
- **Reports from authoritative records** (S01, S05, A20): -3,720 minutes per sponsor-year and -0.1 per account.
- **Prevented customer questions** (A21, proactive status): -0.7, with 0.1 transferred.
- **Input design** (A02, A04, A07, A12): -1.6, with 0.57 transferred to donors.
- **Continuous charity monitoring:** A09 -0.68 and A08 -0.12, **but A10 +0.02.** Earlier detection creates work.
- **Configuration over custom engineering** (S02): -900, with 300 transferred to sponsor adoption.
- **Proactive problem detection** (S03): -400. Incident variance dominates (high case 12,000).
- **Repeatable onboarding** (S06): 18,000 -> 12,000 per new sponsor, by about the fourth to sixth sponsor.

**The biggest single lever is A11** (exception reduction through determination reuse and structured entry), at -3.1 minutes. It rests on replay rates (11.2% -> 4.0% -> 3.1%), not on any time study.

**Transfers flagged:** A05 complex gifts (0.30) and A13 foreign grants (2.20) go to fee-bearing intermediaries, a cost to the fund or charity. A15 shifts 0.40 to charities (EFT enrollment). Donors pick up about 0.8 minutes in total (attestations, references, self-service). S02 and S04 shift 600 minutes per sponsor-year to sponsors and their auditors.""")
    ,
    ("Part 3: Handling-time targets, lower bound, tails and peaks", f"""Each target below uses Model B fixed cost and a simplified break-even sensitivity.

{tbl(['target min/acct-yr', 'feasibility', 'FTE per 10k accts', 'labour $/acct-yr', 'break-even (simplified)'], [(r['target_min_per_account_year'], r['feasibility'], r['fte_per_10k_accounts_queue'], r['labour_usd_per_account_year'], '$' + r['breakeven_assets_usd_bn_modelB_fixed'] + 'B') for r in HT if r['row_type'] == 'target'])}

**Theoretical lower bound (servicer):** about **{M['floor_servicer']:.1f} minutes per account-year at market mix** [D from A], plus sponsor-level work of 1.3-3.2 at 10,000-4,000 accounts per sponsor, and **{M['floor_sponsor']:.1f} sponsor-appointed minutes**.
- **Irreducible on legal, independence or control grounds:** about {M['floor_legal']:.1f}. This covers exception dossiers and decisions, flag clearing, sanctions dispositions, ER/ED review, complex-gift packets, dual authorization, break resolution, independent sampling and controller sign-off.
- **Irreducible because of uncertainty or service by right:** fraud, succession, complaints and requested human service, accessibility accommodations, residual paper.
- **Excluded:** engineering, sales, management and onboarding, which are fixed or per-event.

**Segments and tails (after redesign):**
- routine accounts: {[r for r in WT if r['name'].startswith('routine')][0]['minutes_after']} minutes;
- high-frequency grantmakers: {M['arch_after']['high_frequency']:.0f} (7% of accounts carry about 18% of minutes);
- high-value: {M['arch_after']['high_value']:.0f};
- complex contribution: 150 minutes per gift, of which 90 are irreducible;
- international/ER grant: 25 minutes per grant;
- accessibility accommodation: 30 minutes per case, **deliberately not reduced**;
- fraud/compliance investigation: 120 minutes per case, not reduced (monitoring raises detection volume).

**Workload percentiles:**
- **p50 account:** {M['arch_after']['typical']:.0f} minutes;
- **p90:** {M['arch_after']['high_value']:.0f} (within-archetype high {M['arch_after_high']['high_value']:.0f});
- **p99:** {M['arch_after']['complex_asset']:.0f} (high {M['arch_after_high']['complex_asset']:.0f}).

The archetype step distribution is assumed; no account-level distribution has been observed.

**December stress** (10,000 accounts, 4 sponsors, core {M['base_fte']} FTE sized on annual minutes x 1.15):

{tbl(['scenario', 'Dec minutes', 'peak-day minutes', 'core FTE needed (clear in 10 Jan days)', 'outcome at core ' + str(M['base_fte'])], [(p[0], p[1], p[2], p[3], p[5]) for p in peaks])}

**Annual-average sizing cannot absorb December.** The 31 December backlog would take months of January spare capacity to clear.

**Sensitivity at 10,000 accounts (core FTE needed):**

| Surge FTE | Clear in 10 days | Clear in 20 days | Clear in 40 days |
|---|---|---|---|
| 2 | 9 | 8 | 6 |
| 4 | 8 | 7 | 6 |
| 6 | 8 | 6 | 5 |

**What is legally time-critical:**
- sanctions reports (10 business days);
- complaint acknowledgment (2 business days);
- contemporaneous acknowledgments, which only need to precede the donor's filing.

Year-end grant payment is a service expectation, not a legal deadline. **A sponsor-agreed deferral policy** (for example, non-urgent exceptions and statements shifted into January) is therefore the main peak lever, and it is a service-level transfer that must be disclosed.

**Combined stress:** AI outage, absence and a vendor incident together raise December minutes by about 13% and break dual control unless a second releaser is pre-appointed.""")
    ,
    ("Part 4: Workload-driven staffing (replacing prior triggers)", f"""How each prior trigger is replaced:

| Prior trigger | Replacement |
|---|---|
| Ops manager after 4 added ops staff | Dedicated manager when human headcount across ops, accounting and compliance reaches 7 or more, or founder coordination time exceeds 0.3 FTE (span 6-8 [A]). Self-coordinating case workflows (assignment, clocks and escalation in the case kernel, CNV-SVC-001) remove status-chasing, **not** people management, rostering or the December readiness gate. |
| Integration engineer per 8 sponsors | Driven by **distinct counterparties** (banks, custodians, ERPs) and their change rate: FTE = (new adapters x 280 h + live adapters x 30 h) / 1,520 [A]. Integration work declines with reuse only when new sponsors share counterparties; a sponsor with a new bank resets the curve. |
| Implementation analyst per 8 sponsors | Driven by **new** sponsors per year with an 85% learning curve [A]: onboarding(n) = 9,000 + 9,000 x n^-0.234, plus 7,000 migration minutes. Live sponsors add little. |
| Fund accountant per 15,000 accounts | **Accounting scales with a combination:** sponsor books (monthly close and sign-off), new feed sources (100% calibration for one close cycle) and transactions x break rate. It does not scale with accounts. Break work is under 0.4 FTE even at 50,000 accounts [D from A]; the controller constraint is sponsor books (roughly 60-75 per controller-year [E]). |
| Compliance officer above 10,000 accounts | A **named fractional owner from go-live** (OFAC obligations do not wait for scale); employ when compliance minutes exceed 0.5 FTE or a contract requires it. |

**New lines the prior model lacked:**
- **independent reviewer:** S x {2*4*M['sample_n']*4} minutes per year at n={M['sample_n']};
- **three-person engineering change-control floor** (CNV-PLT-010);
- **pre-contracted December surge;**
- **sponsor-side appointees:** at least 2 per sponsor, exclusive, not servicer staff.

**Servicing FTE (all queue roles) by scale:**

{tbl(['accounts', 'sponsors', 'min/acct', 'annual sizing', 'December sizing', 'recon breaks FTE', 'independent review FTE', 'implementation FTE'], [(g['accounts'], g['sponsors'], g['min_per_acct'], g['servicing_fte_annual_sizing'], g['servicing_fte_december_sizing'], g['recon_break_fte'], g['independent_review_fte'], g['implementation_fte']) for g in grid])}

**Reading.**
- Below about 3,000 accounts, floors bind.
- From about 5,000 accounts, December sizing roughly doubles servicing headcount over annual sizing.
- The redesign (30 vs 50.7 minutes) saves about 3-13 servicing FTE between 5,000 and 20,000 accounts on December sizing. That is where minutes genuinely matter, but only well above the prior break-even scale (about 2,200-3,000 accounts).""")
    ,
    ("Part 5: Administrative overhead", f"""**Conventional small-firm coordination overhead:** **{M['ovh_conv']:.1f} h per FTE-week** [A, range 8-14], built up across 13 categories.

It is informed by two broader measures, neither of which is a small-firm overhead measure:
- Microsoft 365 telemetry: 57% of intentional app time spent communicating (23% meetings, 19% chat, 15% email) [S, quality C];
- Asana's 2023 survey: 58% 'work about work' and 2.8 h per week of unnecessary meetings [S via secondary, quality C].

**AI-native residual:** **{M['ovh_res']:.2f} h per FTE-week** [A, range 3-6]. What remains:
- SoD approvals (controls);
- risk, incident and ops reviews;
- control documentation and runbooks;
- escalations;
- independent sampling, which replaces the QA function.

**Removable by one authoritative record and case store:**
- status reports;
- performance and operational reporting;
- ticket routing;
- repeated data entry;
- interdepartmental reconciliation;
- most project tracking.

**Economic value:** {M['ovh_conv']-M['ovh_res']:.2f} h per FTE-week x 46 weeks x $82/h is about ${round((M['ovh_conv']-M['ovh_res'])*46*82):,} per FTE-year against a conventional firm.

**Against the prior model the gain is small.** The prior model already deducted about 6 h per week (15%) for meetings and admin (report 03:111), so the AI-native gain over it is only **about {6-M['ovh_res']:.1f} h per FTE-week (about 3% of capacity)**. For a 7-person team that is roughly ${round((6-M['ovh_res'])*46*82*7):,} a year, and it becomes cash only if it avoids a hire.

**Coordination cost is real but second-order** for a firm of 6-10 people, with 15-45 pairwise links. It matters more as the firm grows. 'Repeated data entry' overlaps with activity minutes; do not add it twice.""")
    ,
    ("Part 6: AI-native operating architecture and AI capabilities", f"""**Architecture: one operational model, not departments as agents.**

| Primitive | What it holds |
|---|---|
| Event | Immutable fact from a feed, user or rule |
| Case | Typed profile (CNV-SVC-001) with clock, assignment and deadline |
| Control | Rule or required human step with justification, owner and expiry (CNV-GOV-006) |
| Evidence | IPE-supported, hashed, retained (CNV-GOV-001, CNV-PLT-009) |
| Authority | One matrix: command class x actor type x level (CNV-GOV-010), so every command declares its authority |
| Policy version | Sponsor-adopted, effective-dated (CNV-GOV-005) |

Humans and agents act on cases under the authority matrix. 'Departments' become role sets over one queue. That removes handoffs and status reporting, but not segregation of duties, which the engine enforces.

**{len(AI)} AI capabilities** are specified (monitoring, exception detection, prioritisation, case assignment, customer service, control evidence, compliance monitoring, reporting, onboarding, policy configuration, learning, recurring-problem detection, dossiers, document extraction, fraud triage, reconciliation suggestions). **All are capped at recommend/prepare (A1)**, apart from reversible internal assignment (A2).

**Invariants:**
- AI never creates or alters financial figures;
- AI never clears flags or holds;
- AI never exercises or routes around reserved sponsor authority;
- AI cannot select samples to attest its own work;
- AI unavailability leaves deterministic paths running (CNV-AIO-001).

**Status: proposed.** No case, event, control or evidence runtime exists. The Echelon components are engineering tooling (repository OS, code quality, security discipline, UI, auth). The DAF application is 'planned' and monitoring is 'absent' (echelon-capabilities.csv). The architecture is a requirement set (Unbound), not a demonstrated system, and shared Echelon effort must be charged at loaded cost.""")
    ,
    ("Challenge to previous conclusions and to the new premise", f"""**Prior conclusions this pass supports:**
- **50 minutes AI-native is a defensible planning figure.** This pass reaches about 30 only with input redesign, determination reuse and board delegation, and only after a pre-delegation year at roughly 45-75.
- **5-6 people live** is right at break-even scale. Independence floors bind there.

**Prior conclusions this pass corrects:**
1. **The prior elimination scenario (33.8) counted transfers as elimination.** On a transfer-honest basis this pass's redesign eliminates about {M['mix_base']-M['mix_after']-M['mix_trans']:.0f} minutes and transfers about {M['mix_trans']:.0f}.
2. **Hiring triggers.** The prior triggers were proxies (accounts, sponsors, ops counts). The real drivers are:
   - December clearance;
   - counterparties;
   - new sponsors;
   - sponsor books and break rates;
   - fixed independence floors (engineering change control needs 3 people; independent reviewer; sponsor appointees).
3. **The December-temps line understates peak cost.** Temps cannot release, and core staff sized to annual minutes cannot clear December.
4. **Sponsor-side cost was omitted.** Appointees, board review and adoption work are a buyer cost that affects willingness to pay.

**On the new premise, there is no fundamentally different company.**
- Even zero human minutes would lower simplified break-even assets by about {100*(1-M['be_zero']/M['be_prior']):.0f}% at market mix.
- The cost structure is fixed-cost and control-floor dominated.
- AI changes the evidence and control quality and the marginal cost of an extra account. It does not change the floor.
- The exception is **small-balance, high-activity books**. There, minutes are a large share of revenue (typical archetype: $300 revenue at 20 bps against about $25 of redesigned labour; small-recurring: $16 revenue against about $15). Pricing per account, not the minutes, decides those.""")
    ,
    ("Limitations and evidence gaps", """**Limitations:**
- **No time study, no operating data, no sponsor input.** Every minute is [A]. Exception incidence and December arrivals are the two most consequential unknowns (CNV-EVB-001).
- **The market-mix reconstruction is approximate.** It uses archetype top-3 activities only, and the archetype mix (20/20/40/7/10/3) is itself an assumption.
- **The break-even figures are a one-line sensitivity** (Model B fixed $1.74M, market-mix balance). They do not re-run the F# model with sponsor-level costs; prior break-even ranges remain authoritative for levels.
- **Legal bases are cited through Unbound clauses and the prior register.** IRC 4966/4967, 31 CFR 501 and the NACHA rules were not re-read in primary form in this pass.
- **Coordination-overhead sources are vendor studies of large populations** (telemetry or survey), not small DAF servicers.
- **Learning-curve and adapter-effort parameters are generic assumptions.**
- **AI capability limits are design requirements, not tested behaviour.**
- **Same-model reasoning.** The integrator and adversarial reviewers should challenge A11 minutes, the floor composition and the December model independently.

**Highest-value evidence to collect:**
1. a 90-day time study on a real sponsor book;
2. a 12-month shadow replay of exceptions;
3. December interval arrivals;
4. an auditor's planned approach to generated evidence;
5. a sponsor's acceptance of board delegation and of a December deferral policy.""")
]

RJ = [{"section": s, "markdown": m} for s, m in SECTIONS]


def wjsonl(name, rows):
    with open(f"{OUT}/{name}", "w") as f:
        [f.write(json.dumps(r, ensure_ascii=False) + "\n") for r in rows]
    [json.loads(l) for l in open(f"{OUT}/{name}")]
    return name, len(rows)


print([wjsonl("report.jsonl", RJ), wjsonl("evidence.jsonl", EVJ), wjsonl("assumptions.jsonl", ASJ)])
