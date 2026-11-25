"""Write ADV2 outputs. Run: python3 -I -B build.py <outdir> (from any directory)."""
import csv, json, sys, io, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from findings_data import FINDINGS, HIDDEN
from framework_data import STEPS, DECISIONS, EDF, CLARITY_REV, EDF_REV
from review_data import PERSPECTIVES, FALSIFICATION, EVIDENCE, ASSUMPTIONS

OUT = sys.argv[1]

def write_csv(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return name, len(rows)

def write_jsonl(name, objs):
    lines = [json.dumps(o, ensure_ascii=False) for o in objs]
    for l in lines:
        json.loads(l)
    with open(os.path.join(OUT, name), "w") as f:
        f.write("\n".join(lines) + "\n")
    return name, len(lines)

def money(v):
    return f"${v/1e6:.2f}M" if abs(v) >= 1e6 else f"${v/1e3:.0f}k"

def md_table(header, rows):
    esc = lambda c: str(c).replace("|", "\\|").replace("\n", " ")
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows])

# HC-13 (labour while scope is deferred) and HC-12 (building the deferred scope) are alternatives: sum only HC-12.
# HC-10 (licence) is internal if the group shares owners: excluded from totals, shown separately.
EXCLUDED = {"HC-13", "HC-10"}
totals = {k: tuple(sum(r[i] for r in HIDDEN if r[6] == k and r[0] not in EXCLUDED) for i in (3, 4, 5)) for k in ("N", "partial", "Y")}
sponsor_side = tuple(sum(r[i] for r in HIDDEN if r[0] in {"HC-01", "HC-02", "HC-03", "HC-05", "HC-06"}) for i in (3, 4, 5))
sev = {s: sum(1 for f in FINDINGS if f[4] == s) for s in ("critical", "major", "minor")}

proc = ([{"record": "procedure_step", "framework": "Clarity" if s[0].startswith(("CL", "PRE")) else "EDF", "step_id": s[0], "step": s[1], "source": s[2], "performed": s[3], "note": s[4],
          "step_id_note": "Step IDs are ADV2 labels for traceability; neither framework numbers its rules or steps."} for s in STEPS]
        + [dict(record="clarity_decision_assessment", clarity_revision=CLARITY_REV, **d) for d in DECISIONS]
        + [dict(record="edf_application", edf_revision=EDF_REV, **e) for e in EDF])

files = [
    write_csv("model-findings.csv", ["id", "area", "finding", "reproduction", "severity", "effect", "fix"], FINDINGS),
    write_csv("hidden-costs.csv", ["id", "item", "where_it_moved", "annual_low_usd", "annual_base_usd", "annual_high_usd", "counted_in_model", "evidence"], HIDDEN),
    write_jsonl("framework-procedure.jsonl", proc),
    write_csv("nine-perspectives.csv", ["id", "perspective", "strongest_objection", "evidence_that_would_answer", "answered_by_current_research"], PERSPECTIVES),
    write_csv("falsification.csv", ["id", "claim", "falsifying_observation", "cheapest_way_to_obtain", "current_status"], FALSIFICATION),
    write_jsonl("evidence.jsonl", [{"evidence_id": e[0], "claim": e[1], "value": e[2], "unit": e[3], "source_url_or_path": e[4], "source_type": e[5], "filing_period": "n/a", "accessed": "2026-11-25", "quality": e[6], "notes": e[7]} for e in EVIDENCE]),
    write_jsonl("assumptions.jsonl", [{"assumption_id": a[0], "statement": a[1], "value": a[2], "unit": a[3], "low": a[4], "high": a[5], "basis": a[6], "evidence_ids": a[7], "sensitivity": a[8]} for a in ASSUMPTIONS]),
]

R = []
def sec(title, md): R.append({"section": title, "markdown": md})

sec("ADV2 summary verdict",
f"""**Group ADV2 (adversarial review), 2026-11-25.** I did not produce the work reviewed. Same model family as the producers, so this is **not independent validation**. Labels [S]/[A]/[D]/[E]/[M] as in the brief.

**Verdict: no fundamentally different company emerges. What emerges is a somewhat cheaper, better-instrumented version of the same business.** The model has pessimistic errors too (coordination counted twice, financing in the capital figure, a cancelled productivity gain), but they are smaller than the optimistic ones, so the net error is optimistic.

**Most of the improvement is assumption, not design.** About 75% of the cost reduction the model claims over the previous study (its own bridge: $0.81M of $1.08M at $1.5B) comes from replacing $1.0M/yr of build amortisation and $250k of sales with a 2x-productivity platform charge ($0.44M) and $62k of sales lines. Workload-driven staffing contributes $0.26M/yr, about $0.08B of break-even (ADV2-011).

**Corrected figures:**
- **Break-even.** The $1.2-1.4B headline is the floor of the plausible range. Restoring sales ($250k), an independent reconciler, turnover and churn onboarding, MSP at 1.5x with LYR's Echelon reliance cost, and half of December carried by employees moves F5 standalone from $1.39B to $1.57B, then $1.74B, then $1.99B [M, E14]. With LYR's platform team it is $2.73B. The previous study's fully loaded range was $1.8-2.3B, which overlaps.
- **Capital.** Two correlated failures (build x2 + sales 2x) take it to $7.7-11.7M (ADV2-027). Separately, $3.7-6.2M becomes $4.3-7.4M once the sequences carry the recurring platform costs the annual view already charges [M, E06], or $7.2-11.2M on LYR's platform. Without the 10% financing charge the equity need is 16-24% lower, so the capital figure is partly pessimistic (ADV2-009).
- **3-person organisation.** It conflicts with CNV-GOV-003: three distinct persons are required until the auditor and board accept the deterministic gate, and reconciliation must sit outside the payment chain. F3's third person is a sponsor appointee (a transfer), and F3 runs 4.2 contracted FTE at its break-even (ADV2-004, ADV2-021).
- **Hidden costs.** Costs outside the servicer's P&L total {money(totals['N'][1])}/yr at base ({money(totals['N'][0])}-{money(totals['N'][2])}) at a $1B / 5-sponsor / 4,000-account reference, plus {money(totals['partial'][1])} only partly counted. The largest items are sponsor oversight and appointees, sponsor migration, deferred scope and the labour it moves, Echelon reliance, and payment rails.

**Findings:** {len(FINDINGS)} model findings ({sev['critical']} critical, {sev['major']} major, {sev['minor']} minor). The model reproduces exactly (20/20 tests; results.md identical) [M]. Its arithmetic is mostly sound. The defects are in scope (what is charged where), in control feasibility, and in which pass's base is called the base.""")

sec("Method and reproduction",
"""- **Copy and run** [M]. The model and the previous model were copied to `adv/work/` and left unmodified. Commands: `dotnet test tests/CapitalMinimization.Tests` (20 passed) and `dotnet run --project src/CapitalMinimization -c Release -- adv/out`. `adv/out/results.md` is identical to `model/out/results.md` after the timestamp line.
- **Experiments** [M]. `adv/scripts/experiments.fsx` runs E01-E15 with `dotnet fsi`, referencing the copied Release DLLs; output is in `adv/work/experiments.out`. `adv/scripts/pay.fsx` computes the payment rails.
- **Adjustment assumptions** A-ADV2-001..007 are [A]. Each was chosen as plausible rather than worst case, and each is a switch the integrator can drop.
- **Inputs read.** Research pass outputs `dev/`, `ops/`, `com/`, `lyr/` (report.jsonl, assumptions, key CSVs); Unbound convergence clauses CNV-GOV-003, CNV-GOV-004 and CNV-PLT-010 (primary); the previous study's 08-adversarial-review.md and adversarial-findings.csv; Clarity and EDF docs at pinned revisions.
- **Mission sections read.** Section 19 (cost of being wrong: lines 657-680) and section 20 (Clarity/EDF, the nine perspectives, and cost transfer to less visible categories: lines 682-722). Section 20's investigation items (hidden assumptions, mechanisms, alternative explanations, incentives, feedback loops, dependencies, second-order effects, counterfactuals, falsification) are fields of each Clarity decision record.
- **Not done.** Primary Rehearsal 4 records (GitHub) were not read; the evidence-register cross-check of every cost line was not done.""")

sec("Model defects",
"Full table: `model-findings.csv`. Ordered by consequence.\n\n" + md_table(["ID", "Severity", "Area", "Finding (short)", "Effect"],
    [[f[0], f[4], f[1], f[2][:260] + ("..." if len(f[2]) > 260 else ""), f[5]] for f in FINDINGS])
+ "\n\n**Where the model is too pessimistic:**\n- coordination is counted on top of the productive-hours deduction (ADV2-013);\n- the financing charge inflates the equity need (ADV2-009);\n- the +3% productivity gain cancels itself (ADV2-014);\n- code approvers are duplicated across layers (ADV2-018);\n- LYR's 4-engineer team is sized for the full Unbound scope (ADV2-002).\n\nTogether these are worth roughly $0.05-0.1B of break-even and $0.6-2.8M of capital trough (the latter only if the capital is equity). They do not offset ADV2-001/003/006/007.")

sec("Hidden cost ledger",
f"""`hidden-costs.csv` has {len(HIDDEN)} items. Reference: $1B, 5 sponsors, 4,000 accounts, 50 minutes, unless an item says otherwise. 'Counted' means inside the model's servicer cost.

**Totals.** HC-13 is an alternative to HC-12 and HC-10 is internal if owners are common; both are excluded from the totals.
- Not counted (N): {money(totals['N'][0])} / {money(totals['N'][1])} / {money(totals['N'][2])} low / base / high per year.
- Partly counted: {money(totals['partial'][0])} / {money(totals['partial'][1])} / {money(totals['partial'][2])}.
- Sponsor-side subtotal (HC-01/02/03/05/06): {money(sponsor_side[0])} / {money(sponsor_side[1])} / {money(sponsor_side[2])}.
- Counted but invisible in the headcount label: {money(totals['Y'][1])} (F3's contracted queue FTE and agent compute).

""" + md_table(["ID", "Item", "Moved to", "Low", "Base", "High", "Counted"], [[h[0], h[1][:120], h[2], money(h[3]), money(h[4]), money(h[5]), h[6]] for h in HIDDEN])
+ """

**Reading. Does the AI-native organisation move conventional costs into less visible categories? Partly, yes.**
- **Sponsors are the main sink:** oversight and appointees ($0.33M base), migration ($0.17M), payment rails ($0.08M), the release third person, and audit evidence. COM puts sponsor-retained time at 7.0 min/account; OPS puts it at 2.7. The two passes have not reconciled this (ADV2-026).
- **Deferral is the second sink.** The 56% of the conventional scope not built in the MSP is worth $0.31-0.56M/yr. While deferred, the labour it would have automated returns to operations and sponsors ($0.1-0.33M).
- **Echelon is the third.** The model charges $45k; reliance costs $0.27M, plus a licence that does not yet exist.
- **Not hidden:** agent compute is small (<5% of build; $48k/yr assumed for operations), and contractors are costed, though the headcount label hides them.
- **Net.** Counting the base not-counted items as system cost would add more than the whole organisational saving ($0.26M) several times over. A large part of the leanness is relocation.""")

sec("Clarity procedure",
f"""**Revision:** {CLARITY_REV}. The procedure was extracted from rules.md, assessor-guide.md, decision-record.md and decision-posture-model.md. Step IDs (PRE-01, CL-01..CL-16) are mine; Clarity does not number them. Records are in `framework-procedure.jsonl` (procedure_step x{len(STEPS)}, clarity_decision_assessment x{len(DECISIONS)}).

| Step | Performed | Note |
|---|---|---|
""" + "\n".join(f"| {s[0]} {s[1]} | {s[3]} | {s[4][:160]} |" for s in STEPS) + "\n\n"
+ md_table(["Decision", "Level", "Posture", "Confidence", "Commitment"], [[d["id"] + " " + d["decision"][:90], d["level"], d["posture"], d["confidence"][:90], d["commitment"]] for d in DECISIONS])
+ """

**Could not be performed:**
- ownership acceptance (CL-11);
- decision date and review cadence (part of CL-14);
- outcome (CL-16);
- live monitoring for triggers (CL-12 partial).

By decision-record.md:7-17, a decision without an owner is not ready. **All five decisions are therefore 'not ready'** whatever the analysis says.

**Clarity's own limit:** its 2026 benchmark found it no more accurate than the same model with no method; its strength is making assumptions explicit (README:19-22). That is how it was used here. The value it added was surfacing shadow assumptions: the sponsor provides the third person; the owner's Echelon time is free; the founder can sell while building.""")

sec("EDF applicability",
f"""**Revision:** {EDF_REV}. The required sequence (specification.md:39-54) needs a factual outcome at step 2.

| Subject | Applicable | Outcome / reason | Claim state | Confidence | Next responsible action |
|---|---|---|---|---|---|
""" + "\n".join(f"| {e['id']} {e['subject']} | {e['applicable']} | {e['outcome'][:200]} | {e['claim_state'][:120]} | {e['confidence']} | {e['next_action'][:140]} |" for e in EDF)
+ """

**Prerequisites absent for the five decisions and the headline claims:** there is no factual outcome, so EDF steps 2-5 and 7-9 cannot run. Only step 6 (separating observation from inference) and the claim-state vocabulary are used.

Diagnostic Calibration does not apply: one model family and no cross-executor runs.

The EDF results relevant to D2 are:
- **EDF-A:** development cost reduction is unsupported; the control point is a timer plus independent acceptance.
- **EDF-B:** at least 5x autonomous construction is contradicted at n=1, from a secondary summary (primary not read).""")

sec("Nine perspectives",
"Full text: `nine-perspectives.csv`.\n\n" + md_table(["Perspective", "Strongest objection", "Evidence that would answer it", "Answered now?"], [[p[1], p[2], p[3], p[4]] for p in PERSPECTIVES])
+ "\n\n**Open objections:**\n- Fully unanswered: investor (P3), controller (P5), donor/advisor (P8) and auditor (P9). Each needs an external party: an auditor letter, a design-partner operating year, or a valuation.\n- Partly answered by modelling: P1, P2, P4, P6 and P7.")

sec("Falsification",
"Full text: `falsification.csv`.\n\n" + md_table(["Claim", "Falsifying observation", "Cheapest way to obtain it", "Status"], [[f[1], f[2], f[3], f[4]] for f in FALSIFICATION])
+ "\n\n**Cheapest decisive tests, in order:**\n1. Desk check of CNV-GOV-003 against F3. It is free and already done, and it contradicts the 3-person claim unless a sponsor appointee is counted.\n2. Owner-led quotes to 5-10 sponsors in bps and $/account side by side (low cost).\n3. The DEV measurement protocol on 3 capabilities (~$100-250k of build that is needed anyway).\n4. A 90-day shadow time study with December arrival data at one sponsor (~$25-60k [E]).\n5. The auditor's planned-approach letter, inside the planned $20k SOC readiness assessment.")

sec("Overall conclusion: does a fundamentally different company emerge?",
"""**No, on current evidence.** This is not pessimism for its own sake: the model's own numbers and the passes' own findings say so.

1. **Fixed control, assurance, platform and sales cost sets break-even, not handling time.**
   - Zero human minutes would lower break-even by ~7% (OPS).
   - 50 to 30 minutes moves F5 operating break-even by $0.07B (results.md section 3).
   - AI changes marginal cost (~$90 to ~$45 per account-year in the model) and evidence quality, not the fixed floor.
2. **The apparent step change is a build-cost assumption.** About 75% of the claimed reduction is the 2x MSP multiple and lower sales spend. 2x is unmeasured; the only end-to-end trial failed (1/108).
3. **The lean organisation is partly a relocation.** Sponsors (appointees, oversight, migration, rails, the third release person), deferred scope and its manual labour, and Echelon reliance absorb about $1.6M/yr at base that the servicer's P&L does not show (sponsor side alone about $0.6M).
4. **Controls bind exactly where AI-native design claims to save.** Three distinct persons until the gate is accepted; reconciliation outside the payment chain; per-sponsor exclusive appointees and surge reviewers; December sizing above ~5,000 accounts.

**What is genuinely different, and worth keeping:**
- workload-driven staffing instead of ratio triggers (~$0.1-0.4M/yr at scale; section 6);
- a single case/event/evidence model;
- per-account pricing logic;
- an explicit three-layer cost view;
- an honest Amdahl bound on build cost.

**What would change the verdict (falsifier F-06), all at once:** a measured >= 2x accepted-capability multiple with defect escape at or below baseline; auditor and board acceptance of the deterministic gate from go-live; <= 30 observed minutes after the pre-delegation year; platform recurring cost <= $0.4M/yr. None is evidenced today. All four can be tested for roughly $0.2-0.4M, mostly spend that is needed anyway.""")

sec("Files, row counts, top findings and gaps",
md_table(["File", "Rows/lines"], [[n, c] for n, c in files] + [["report.jsonl", len(R) + 1], ["work/experiments.out", "E01-E15 [M]"], ["scripts/experiments.fsx, pay.fsx, build.py, *_data.py", "sources"], ["out/ (re-run model outputs)", "results.md + 4 CSV"]])
+ """

**Top findings:**
1. **ADV2-001 (critical).** Adjusted F5 break-even is $1.6-2.0B, not $1.2-1.4B.
2. **ADV2-011.** About 75% of the improvement is the build/sales assumption; organisational design is worth ~$0.26M/yr.
3. **ADV2-004.** The 3-person design conflicts with CNV-GOV-003; its safety is borrowed from sponsors.
4. **ADV2-003.** The December capacity limit is absent (+$0.16-0.36B of break-even).
5. **ADV2-006/007/027.** Sequences omit recurring platform cost and use an unmeasured 2x build. Capital is $4.3-7.4M, not $3.7-6M, and two correlated failures double it ($7.7-11.7M).

**Largest gaps:**
- no time study or December arrival data;
- no measured accepted-capability rate or human time;
- no auditor view of the deterministic gate or of AI-authored code;
- no Echelon licence terms;
- no buyer price test;
- sponsor-retained time is unreconciled between OPS (2.7) and COM (7.0);
- primary Rehearsal 4 records were not read.""")

write_jsonl("report.jsonl", R)
print(json.dumps({"files": files, "report_sections": len(R), "hidden_totals": totals, "severity": sev}))
