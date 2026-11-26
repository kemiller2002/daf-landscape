"""Write ECH outputs. Run: python3 -I -B main.py <script_dir> <out_dir>"""
import csv
import io
import json
import sys
from collections import Counter

sys.path.insert(0, sys.argv[1])
from caps import CAPS, COLS  # noqa: E402
from procedure import STEPS, COLUMN_MAP, CREV, DREV  # noqa: E402
from template import ROWS  # noqa: E402

OUT = sys.argv[2]
ACC = "2026-11-25"
REV = {"clarity-framework": "200a9eb (200a9ebf029c051eac625bb5185929b20c8d5aed, 2026-11-16)",
       "echelon-diagnostic-framework": "710d54c (710d54c20e935db8b6f75f9c60ee7217f0cb0e32, 2026-11-17)",
       "Echelon-AI-Native-Enterprise-Design-Framework": "763ff8c (2026-11-20)",
       "AI-Engineering": "1bc519b (2026-09-30)", "unbound": "9b38de4 (2026-11-24)", "daf-landscape": "e1a3633 (2026-11-25)"}


def csv_text(cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cols)
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def jsonl_text(objs):
    return "".join(json.dumps(o, ensure_ascii=False) + "\n" for o in objs)


def money(x):
    return f"-${-x:,.0f}" if x < 0 else f"${x:,.0f}"


def md_table(header, rows):
    return "\n".join(["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] +
                     ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])



import re as _re
_UCP = "unbound:requirements/convergence/2026-11-24-master/"
_MAP = {"05": "05-ECONOMIC-VALIDATION.md", "13": "13-EVIDENCE-BACKLOG-RESULTS.md", "14": "14-PUBLIC-DATA-REPLAY.md",
        "07": "07-ECHELON-CAPABILITY-ASSESSMENT.md", "15": "15-SAVINGS-CLAIMS.md"}


def expand(text):
    t = _re.sub(r"(?<![\w./-])(05|13|14|07|15):(\d)", lambda m: _UCP + _MAP[m.group(1)] + ":" + m.group(2), text)
    t = t.replace("ME conclusion", "daf-landscape:research/commercial-opportunity/daf-servicing-20bps-market-entry-2026-11-25.md conclusion")
    t = t.replace("ME backlog", "daf-servicing-20bps-market-entry-2026-11-25.md research backlog")
    t = t.replace("ME:24", "daf-servicing-20bps-market-entry-2026-11-25.md:24")
    t = t.replace("ME table", "daf-servicing-20bps-market-entry-2026-11-25.md sponsor table")
    t = t.replace("(FM §3, [A])", "(financial-and-staffing-models.md §3, [A])")
    t = t.replace("(assumption-tests.md:", "(daf-landscape:research/commercial-opportunity/clarity-edf-analysis/assumption-tests.md:")
    t = t.replace("(daf-economics-and-distribution:26", "(daf-landscape:research/daf-economics-and-distribution-2026-11-11.md:26")
    return t


caps_rows = tuple(tuple(c) for c in CAPS)
status_counts = Counter(c[2] for c in CAPS)
effect_counts = Counter(c[4] for c in CAPS)
idx = {name: i for i, name in enumerate(COLS)}


def total(pred, col):
    return sum(c[idx[col]] for c in CAPS if pred(c))


verified_share_hi = total(lambda c: c[2] == "verified-existing" and c[4] == "share", "estimated_annual_effect_high")
all_share_hi = total(lambda c: c[4] == "share", "estimated_annual_effect_high")
elim_hi = total(lambda c: c[4] == "eliminate", "estimated_annual_effect_high")
adds_lo = total(lambda c: c[idx["estimated_annual_effect_low"]] < 0, "estimated_annual_effect_low")
net_lo = total(lambda c: True, "estimated_annual_effect_low")
net_hi = total(lambda c: True, "estimated_annual_effect_high")

# Development-cost scenarios (all inputs [A]; outputs [D]).
LOADED = 165000          # [A] unbound parameters.json loaded_cost_per_fte base
CONV_FTE = (4, 10)       # [A] daf-landscape FM §3 engineering 4/6/8/10 log scale
BUILD = (3e6, 5e6, 15e6)  # [A] parameters.json build_capex low/base/high
AMORT = 5                # [A] unbound VENDOR build_capex_amortisation_years


def run_cost(fte):
    return fte * LOADED


scen = (
    ("S-conv: conventional enterprise build/run", CONV_FTE, 1.0, "Comparator from prior models; 4 FTE at 1k accounts, 10 at 1m [A]"),
    ("S0: Echelon reuse, no measured AI gain", (4, 6), 1.0, "Reuse limited to UI CSS, print markup, test conventions, requirements; all DAF-specific build remains"),
    ("S1: measured 1.5-2x agent-assisted throughput", (2, 4), 1 / 1.75, "4-6 FTE / 1.5-2x; requires measurement for >=6 months and independent review"),
    ("S2: lean budget (2 engineering FTE)", (2, 2), 0.5, "Requires >=2x throughput at the 4-FTE floor AND narrow servicing-only scope"),
)
scen_rows = tuple(
    (n, f"{f[0]}-{f[1]}", f"{money(run_cost(f[0]))}-{money(run_cost(f[1]))}",
     f"{money(BUILD[0] * k / AMORT)}-{money(BUILD[2] * k / AMORT)} (base {money(BUILD[1] * k / AMORT)})", note)
    for n, f, k, note in scen)
conv_lo, conv_hi = run_cost(4), run_cost(6)

caps_md = md_table(["ID", "Capability", "Status", "Effect", "Annual effect low/high [A]"],
                   [(c[0], c[1], c[2], c[4], f"{money(c[6])} / {money(c[7])}") for c in CAPS])

tmpl_cols = [c for c, _ in COLUMN_MAP]
tmpl_rows = tuple(tuple(expand(str(r.get(c, ""))) for c in tmpl_cols) for r in ROWS)
summary9 = md_table(["ID", "Assumption", "Claim state (EDF policy)", "Confidence", "Posture (Clarity)", "Commitment"],
                    [(r["assumption_id"], r["assumption_statement"][:90] + ("..." if len(r["assumption_statement"]) > 90 else ""),
                      r["claim_state"], r["confidence"], r["decision_posture"], r["recommended_commitment"]) for r in ROWS])

report = (
    {"section": "ECH-0 Scope, method and revisions", "markdown":
        "Group ECH (Echelon capabilities + Clarity/EDF method). Read-only. Nothing committed.\n\n"
        "**Revisions read (git rev-parse --short HEAD, 2026-11-25):**\n\n" +
        md_table(["Repository", "Revision"], list(REV.items())) +
        "\n\n**What 'verified-existing' means here:** the artefact (code, test file, vendored package, measured result file, document) was opened and read in this session at the cited path. "
        "No build, test or CLI was executed: there is no .NET SDK in this session, so the Echelon F# test suite (87 test attributes counted statically) and the Unbound replay (20 test attributes) were NOT re-run; their pass status rests on each repo's own ledger. "
        "Forma, Limen, Folio, Aegis, Praxis, Conditor, Strata, Tutela and Fides upstream repositories are NOT among the local clones; statements about them come from two prior read-only inspections by agents of the same programme "
        "(daf-landscape `research/ai-native-daf-enterprise/07-technology-architecture/echelon-component-assessment.md`, 2026-11-20; unbound `07-ECHELON-CAPABILITY-ASSESSMENT.md`, 2026-11-24). Those are labelled described-not-verified unless a vendored copy exists locally. "
        "Same-model reasoning is not independent validation."},
    {"section": "ECH-1 What Echelon systems actually exist", "markdown":
        f"22 capabilities assessed (file `echelon-capabilities.csv`). Status counts: " +
        ", ".join(f"{k} {v}" for k, v in sorted(status_counts.items())) + ".\n\n" + caps_md +
        "\n\n**Key facts.**\n"
        "- **No DAF application exists.** Unbound is requirements-only: 'No application code' (unbound `requirements/convergence/2026-11-24-master/LEDGER.md:4`); charter principle 8 forbids implementation before the gate; readiness PASS for architecture, FAIL for production. The modular monolith on managed PostgreSQL is an owner-ratified *decision* (CNV-ARC-001, `AUTHORITATIVE-BASELINE.md:77`), and the database engine is 'not yet selected' in `architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md:20`.\n"
        "- **What is real and local:** the Echelon Enterprise Design Framework (F#, 3,749 lines in `src/Echelon.Enterprise`, 87 test attributes, CI workflow file); Unbound's requirements baseline, 140-screen experience specs and rendered mock-ups; Unbound's public-data replay tool (F#) with committed results; a measured single-VM PostgreSQL 16 benchmark (2,100-3,900 tx/s on 4 vCPU vs ~200 tx/s peak need); vendored Forma 1.0.2 and Folio 0.4.2 copies, both **PolyForm Noncommercial 1.0.0** (LICENSE files read).\n"
        "- **What does not exist:** runtime security (identity, access control, secrets: Aegis is a fault library, Fides is GitHub-only IdP, Tutela 0.1.0), monitoring/logging, a PDF render service (Folio has no renderer, no PDF/A or PDF/UA), production deployment pipeline, running production infrastructure (only static GitHub Pages sites), shared organisational administration, a second human maintainer, any external production user, and any commercial licence.\n"
        "- **Automated software development** is real as practice (Claude-authored commits outnumber human ones in 7 of 14 Echelon repos per the 2026-11-20 inspection) but its productivity is unmeasured: AI-Engineering `HANDOFF.md:12-13` 'No agent capability trial or independent replication is claimed'; Unbound `PRINCIPLES.md:19` the Echelon-advantage hypothesis 'is **not yet established**'.\n"
        "- The canonical Foundry engineering standard says 'No stack-specific standard is canonical in Phase 1 because the repository contains no implementation or supported stack evidence' (vendored copy `echelon-diagnostic-framework/docs/00-governance/Engineering-Standards.md:25`)."},
    {"section": "ECH-2 Effect on the DAF servicer budget: eliminate vs share vs transfer", "markdown":
        "Budget under test: 5 FTE, $1,177,750 fixed (`daf-servicer-bottom-up-operating-budget-2026-11-25.md`). Positive = annual reduction of the servicer's cost; negative = added cost. All per-capability values are [A] (analyst placeholders, no quotes); totals are [D] sums.\n\n" +
        md_table(["Measure", "Value"], [
            ("Capabilities with effect 'eliminate' / 'share' / 'transfer' / 'none'",
             f"{effect_counts['eliminate']} / {effect_counts['share']} / {effect_counts['transfer']} / {effect_counts['none']}"),
            ("Share, verified-existing only (high bound) [D]", money(verified_share_hi)),
            ("Share, all statuses (high bound) [D]", money(all_share_hi)),
            ("Eliminate, conditional on unverified AI productivity (high bound) [D]", money(elim_hi)),
            ("Added cost: security review of single-maintainer AI-authored deps + licence placeholder (low bound) [D]", money(adds_lo)),
            ("Net range across all rows [D]", f"{money(net_lo)} to {money(net_hi)}"),
        ]) +
        "\n\n**Reading.** On verified evidence today the defensible annual reduction to the $1.18m budget is **$0 to about $"
        f"{verified_share_hi/1000:.0f}k** (0-10%) [D], all of it 'share' (reused conventions, UI CSS, print markup, specifications, public-data screening reference). "
        "The only 'eliminate' line (one engineer, up to $150k) depends on measured AI-development productivity that no repository demonstrates. "
        "Two items could *add* cost (independent security review; commercial licence). **Transfers are not savings:** Echelon/founder engineering time, shared administration and Unbound IP licensing all move cost between related entities and must be charged at cost. "
        "Burden Externalization (Clarity Candidate concept) is the failure pattern if they are not."},
    {"section": "ECH-3 What must remain attributable to the DAF business", "markdown":
        "- Platform build amortisation and run cost. The budget states 'actual development scope ... not covered'. Unbound's own vendor model carries build capex $5m (range $3m-$15m) [A] (`unbound/.../simplification-economics/model/parameters.json:509-516`), amortised over 5 years = $1.0m/yr base ($0.6m-$3.0m) [D]. If the servicer uses an Unbound platform, a share of that (by funds or transactions) belongs in its P&L, either as amortisation or a licence fee; a licence fee **transfers**, it does not eliminate.\n"
        "- Every engineering, on-call and review hour on the DAF platform, whoever employs the person.\n"
        "- Security/assurance ($65k), SOC 1/SOC 2 scope, penetration testing, incident response: no Echelon component reduces them.\n"
        "- Cloud/monitoring ($36k): commodity; Echelon provides no running infrastructure.\n"
        "- Independent accounting/controls ($45k): cannot be supplied by a related party without losing independence.\n"
        "- Licence fees for PolyForm-NC components at arm's-length price, or the exit cost of replacing them.\n"
        "- Screening outcomes (eligibility, sanctions) and the cost of any miss; the reference matcher missed 12 of 100 perturbed listed names (unbound `14-PUBLIC-DATA-REPLAY.md:47`).\n"
        "- **Hidden assumption exposed:** the 2-engineer core implies that a working, maintained platform already exists. It does not. Prior daf-landscape modelling needs 4 engineering + 7 agent-ownership FTE at 1,000 accounts [A] (`research/ai-native-daf-enterprise/09-financial-models/financial-and-staffing-models.md:179-200`)."},
    {"section": "ECH-4 Could Unbound develop and maintain software materially cheaper than a conventional enterprise software company?", "markdown":
        f"Inputs [A]: loaded cost ${LOADED:,} per FTE (Unbound parameters base); conventional engineering 4-10 FTE (daf-landscape model, log scale); build capex $3m/$5m/$15m; 5-year amortisation. Outputs [D].\n\n" +
        md_table(["Scenario", "Engineering FTE", "Annual engineering run cost [D]", "Build amortisation/yr [D] (build x factor / 5)", "Condition"], scen_rows) +
        f"\n\n**Answer: conditional, not demonstrated.**\n"
        f"- S0 (what the evidence supports today): reuse removes front-end CSS, print markup, test conventions and requirements work only; DAF-specific ledger, payments, identity, tenancy, render service and security remain. Plausible reduction 0-16% of engineering run cost [D: verified share high bound ${verified_share_hi:,} / ${conv_lo:,}; low bound 0].\n"
        "- S1 (if agent-assisted throughput of 1.5-2x is measured and sustained): 33-50% lower engineering run cost [D: 1-1/1.5 to 1-1/2], i.e. about $0.22m (4 -> 2.67 FTE) to $0.50m (6 -> 3 FTE) a year less [D]. This would be material against a $1.18m budget. The S1 row rounds FTE to whole people.\n"
        "- S2 (the lean budget: technical lead $187,500 + engineer $150,000 = $337,500 loaded [D from budget]) requires S1 *and* a narrow servicing-only scope *and* bought-in identity, PDF, monitoring and payment services. No evidence supports it yet.\n"
        "- Offsetting costs specific to the Echelon route: single human maintainer (bus factor), 0.x churn (Praxis 11 minor releases in ~2 weeks; Forma namespace rename at 1.0), version drift between registry channel, tags and vendored copies, PolyForm NC licensing, and the need for independent review of AI-authored code.\n\n"
        "**Evidence that would prove lower cost:** (1) Praxis/agent telemetry on the DAF codebase: accepted changes per engineer-month, escaped defects, rework, human intervention minutes, against a pre-registered baseline, >=6 months; (2) cost per accepted requirement or story point vs a conventional comparator; (3) maintenance hours per month for 12 months after go-live; (4) an independent security review and a clean SOC 1 Type II on the first sponsor; (5) a second engineer becoming productive from AI-readable docs within a stated time (bus-factor test); (6) published commercial licence terms. "
        "**Evidence that would disprove it:** throughput gain <1.2x, defect or rework rates above baseline, or Echelon hours that cannot be charged without breaking the budget."},
    {"section": "EDF/CL-0 Framework sources and revisions", "markdown":
        md_table(["Framework", "Repository @ revision", "Files used"], [
            ("Clarity", f"/home/user/clarity-framework @ {CREV}", "rules.md (Constitution, admissibility lint, operational test); docs/assessor-guide.md; decision-posture-model.md; decision-record.md; docs/reconsideration-criteria.md; docs/progressive-commitment.md; docs/framework/concept-layers.md; docs/concepts/concept-maturity.md; docs/templates/clarity-result-template.md; docs/foundation/clarity-constitution.md; research/2026-framework-improvement/README.md and protocols/arm-D2-clarity-lean-1.1.md (experimental)"),
            ("EDF v0.3", f"/home/user/kemiller2002/echelon-diagnostic-framework @ {DREV}", "docs/edf/specification.md; docs/edf/templates/edf-1-standard.md (and edf-0/edf-2); docs/edf/diagnostic-calibration.md; docs/edf/operating-cycle.md; docs/framework-engineering/claim-and-confidence-policy.md v1.0"),
            ("Application notes", "daf-landscape @ e1a3633", "research/mission-2026-11-14/clarity-edf-application-guide.md (pinned to Clarity 8cd48019 / EDF 41fea6f); research/commercial-opportunity/clarity-edf-analysis/assumption-tests.md (Clarity 200a9eb / EDF 710d54c)"),
        ]) +
        "\n\nBoth local clones are shallow single-commit; the guide's older pinned commits are not present, so changes between them and the revisions used cannot be diffed here. "
        "**Rule IDs:** neither framework defines numbered rule IDs. Clarity's rules are the unnumbered 13-item admissibility list (rules.md:44-58), six commitments (rules.md:20-38) and the operational test (rules.md:86-90); 'CL-1'/'CL-1.1' are experiment-arm IDs for Clarity Lean, not rules. EDF has a nine-step required sequence and 15 required output elements. Step IDs in `framework-procedure.jsonl` (CL-xx, EDF-xx) are assigned by this group for traceability and are not framework identifiers."},
    {"section": "CL-1 Clarity procedure (as the documents define it)", "markdown":
        "Core questions: What is being treated as true? What currently justifies that? What would make us reconsider? (assessor-guide.md:17-21). Assessment depth: Level 0-3, smallest sufficient for the risk. Steps extracted (see `framework-procedure.jsonl` CL-01..CL-15):\n\n" +
        md_table(["Step", "Name", "Required outputs"], [(s["step_id"], s["name"], ", ".join(s["required_output_fields"])) for s in STEPS if s["framework"].startswith("Clarity") and s["step_id"] != "CL-L"]) +
        "\n\nConcept maturity matters: Core = Claim, Evidence, Assumption, Confidence, Ownership, Reassessment, Correctability, Proportional Certainty, Confidence Debt; Candidate = Burden Externalization, Governance Debt, Resolution Debt, Trigger Claim; Research = Trigger Drift, Signal Quality, Modes of Success, Calibration (concept-maturity.md). "
        "**Limits stated by Clarity itself:** 'The goal is not to complete a worksheet' (assessor-guide.md:5,156); its own 2026 benchmark found current Clarity 'no more accurate' than the same model with no method and much less useful, with one clear strength: making assumptions explicit (research/2026-framework-improvement/README.md). Clarity Lean (CL-1.1) is EXPERIMENTAL and is used here only as the source of 'strongest rival' (alternative explanations)."},
    {"section": "EDF-1 EDF procedure and where it does not apply", "markdown":
        "Required sequence (specification.md:39-54): System Context (Primary System, Context, Focus) -> Outcome (factual) -> Manifestations -> Origin Network (technical, human, organizational, environmental, financial, regulatory) -> Propagation (physical, informational, organizational, financial, human) -> Evaluate Evidence (observation vs inference) -> Control Points -> Rank (influence, controllability, cost, confidence) -> Diagnostic Sufficiency. Required outputs add Confidence, Unknowns, Next Responsible Action (specification.md:150-168). Claim policy: states internal-demonstration / suggestive / unsupported / contradicted / falsified / superseded / planned; confidence Low..High, qualitative (claim-and-confidence-policy.md:47-73).\n\n"
        "**Inapplicable steps.** The nine servicing assumptions are hypotheses about a company that does not exist; EDF step 2 requires a factual outcome, so EDF steps 2-5 and 7-9 cannot be applied to them. EDF was not executed on any assumption. Each template row instead names an *adjacent observed outcome* (e.g. RCF's FY2024 payments to Ren; 12/100 sanctions misses in the public replay; cost per grant $55-$419) on which an EDF-0/EDF-1 could be run. Only the claim-state/confidence vocabulary and the evidence-separation rule (step 6) are applied to the assumptions. "
        "Diagnostic Calibration is not applicable as evidence: lenses from one model are not independent replications (diagnostic-calibration.md). EDF's own README states it does not yet establish cross-executor reproducibility or incremental value."},
    {"section": "CL-2 Template columns and their provenance", "markdown":
        "File `assumption-challenge-template.csv`. Columns the mission requested but the frameworks do not define are marked; they are kept because the mission asked for them, not because the frameworks require them.\n\n" +
        md_table(["Column", "Source"], COLUMN_MAP)},
    {"section": "CL-3 Pre-filled challenges of the nine servicing assumptions (summary)", "markdown":
        "Ordinary adversarial analysis structured by Clarity fields and labelled with EDF claim states. It is **not** a formal Clarity review (no decision owner sign-off, no review cadence) and **not** an EDF diagnosis. Full rows in the CSV.\n\n" + summary9 +
        "\n\n**Cross-cutting reading.** None of the nine is supported for this servicer. Four are unsupported outright (AC-02 lean staffing, AC-03 $75/account, AC-06 anchor acquisition, AC-09 minimums). Five have support only for a narrower claim: AC-01 (a 10-37 bps market exists, not that this servicer can charge 20), AC-04 (eligibility component only, measured on public recipient rows, not grants), AC-05 (UI/print/test reuse, not cost reduction), AC-07 (year-end filings, not average billable), AC-08 (a design rule, not a legal conclusion). "
        "The assumptions are coupled: the 5-FTE core (AC-02) depends on automation (AC-04) and on an unpriced platform (AC-05); revenue depends jointly on price (AC-01), balances (AC-07) and minimums (AC-09). Burden Externalization (Candidate) is the most frequent failure pattern: leanness is partly produced by moving decision cost to sponsors and engineering cost to Echelon."},
    {"section": "ECH-9 Findings and evidence gaps", "markdown":
        "**Five most consequential findings.**\n"
        "1. No DAF application, production infrastructure, security layer, monitoring or shared administration exists in any Echelon or Unbound repository; only design artefacts, research tooling and vendored UI/print markup do.\n"
        f"2. On verified evidence the Echelon effect on the $1.18m servicer budget is 'share' of $0-${verified_share_hi/1000:.0f}k a year [D from A]; the only 'eliminate' candidate (AI-assisted development, up to $150k) is unmeasured; licence and security review may add cost.\n"
        "3. The 5-FTE budget hides a platform build: Unbound's own assumption is $5m ($3m-$15m) build capex, about $1.0m/yr amortised base, which is not in the $1,177,750.\n"
        "4. Nearly the whole Echelon UI/print stack is PolyForm Noncommercial; a commercial servicer is not obviously a 'charitable organization', so commercial licence terms ('forthcoming') are a launch gate and an attributable cost.\n"
        "5. Neither framework can formally test the servicing assumptions: EDF needs an observed outcome; Clarity is a reasoning discipline whose own benchmark shows no accuracy gain. The template is structured adversarial analysis, not framework validation.\n\n"
        "**Open gaps:** CI pass status of Echelon repos; package registry publication; Tutela/Fides/Arca inspection; agent-productivity measurement on a real codebase; commercial licence terms; money-transmission treatment of payment relay; any buyer evidence on price, minimums or switching; sponsor time study."},
)

evidence = (
    ("Unbound has no application code", "0", "application code files", "/home/user/unbound/requirements/convergence/2026-11-24-master/LEDGER.md:4", "repo", "2026-11-24", "A", "Also CHARTER.md principle 8."),
    ("Modular monolith on managed PostgreSQL is an owner-ratified requirement, not an implementation", "CNV-ARC-001", "clause", "/home/user/unbound/requirements/AUTHORITATIVE-BASELINE.md:77", "repo", "2026-11-24", "A", ""),
    ("Database engine not yet selected; no implementation before gate", "", "", "/home/user/unbound/architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md:20", "repo", "2026-11-24", "A", ""),
    ("PostgreSQL 16 single-VM benchmark capacity", "2,100-3,900", "tx/s on 4 vCPU vs ~200 tx/s need", "/home/user/unbound/requirements/discovery/2026-11-23-cross-industry/18-ARCHITECTURE-BENCHMARK.md:1-40", "repo", "2026-11-24", "B", "Measured, not production; client on same host."),
    ("Vendored Forma and Folio carry PolyForm Noncommercial 1.0.0", "PolyForm NC 1.0.0", "licence", "/home/user/unbound/requirements/ui/designs/vendor/forma-1.0.2/LICENSE; folio-0.4.2/LICENSE", "repo", "2026-11-24", "A", "Read 2026-11-25."),
    ("Folio has no renderer, no PDF/A or PDF/UA; 0.4.2 untagged", "", "", "/home/user/unbound/requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md:88-103", "repo", "2026-11-24", "B", "Secondary inspection by same programme; upstream not cloned locally."),
    ("Aegis is not security; Fides GitHub-only IdP; Tutela 0.1.0", "", "", "/home/user/unbound/requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md:122-124", "repo", "2026-11-24", "B", "Secondary inspection."),
    ("Identity, embed runtime, PDF production and provider virtualization are Unbound-owned work", "", "", "/home/user/unbound/requirements/convergence/2026-11-24-master/07-ECHELON-CAPABILITY-ASSESSMENT.md:162-164", "repo", "2026-11-24", "B", ""),
    ("No external production deployment of any Echelon component; one human maintainer", "", "", "/home/user/daf-landscape/research/ai-native-daf-enterprise/07-technology-architecture/echelon-component-assessment.md §1 cross-cutting obs. 2 and 4", "repo", "2026-11-20", "B", "Read-only inspection; absence of evidence."),
    ("Agent capability (productivity) not trialled", "none claimed", "", "/home/user/AI-Engineering/HANDOFF.md:12-13", "repo", "2026-09-30", "A", ""),
    ("Echelon-creates-enterprises-more-effectively hypothesis not established", "", "", "/home/user/unbound/requirements/PRINCIPLES.md:19", "repo", "2026-11-24", "A", ""),
    ("Echelon framework test attributes (static count)", "87", "tests", "/home/user/Echelon-AI-Native-Enterprise-Design-Framework/tests/Echelon.Enterprise.Tests/*.fs; progress/LEDGER.md:28", "repo", "2026-11-20", "B", "Not re-run: no .NET SDK in session."),
    ("Unbound build capex assumption", "5,000,000 (3,000,000-15,000,000)", "USD one-off [A]", "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json:509-516", "repo", "2026-11-24", "D", "Assumption, labelled A in source."),
    ("Loaded cost per FTE assumption", "165,000 (124,507-250,000)", "USD/FTE-yr [A]", "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json (params.loaded_cost_per_fte)", "repo", "2026-11-24", "D", ""),
    ("Prior AI-native model staffing at 1,000 accounts", "24 FTE incl. 4 engineering, 7 agent ownership", "FTE [A]", "/home/user/daf-landscape/research/ai-native-daf-enterprise/09-financial-models/financial-and-staffing-models.md:179-200", "repo", "2026-11-21", "D", "Model output from assumptions."),
    ("Public replay effective first-time eligibility exception incidence", "4.0% within sponsor; 3.1% platform", "of recipient rows >$5k", "/home/user/unbound/requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md:39", "repo", "TY2023-TY2024 990s", "B", "Recipient rows, not grants."),
    ("Reference sanctions matcher misses", "12 of 100", "perturbed listed names", "/home/user/unbound/requirements/convergence/2026-11-24-master/14-PUBLIC-DATA-REPLAY.md:47", "repo", "2026-11-25", "B", ""),
    ("Incumbent software price band", "$32-$129 (median ~$70)", "USD per DAF-year", "/home/user/unbound/requirements/convergence/2026-11-24-master/13-EVIDENCE-BACKLOG-RESULTS.md:26", "990", "TY2023-TY2024", "B", "Contractor payment floors / Schedule D counts."),
    ("Fully outsourced administration price points", "$413-$745", "USD per DAF-year", "/home/user/unbound/requirements/convergence/2026-11-24-master/13-EVIDENCE-BACKLOG-RESULTS.md:29", "990", "TY2023-TY2024", "B", "Two sponsors; scope unknown."),
    ("EDF requires factual outcome; nine-step sequence", "", "", "/home/user/kemiller2002/echelon-diagnostic-framework/docs/edf/specification.md:39-84", "repo", "v0.3 @710d54c", "A", ""),
    ("Clarity admissibility lint (13 rejection categories) and operational test", "", "", "/home/user/clarity-framework/rules.md:42-90", "repo", "@200a9eb", "A", ""),
    ("Clarity own benchmark: no more accurate than no method; less useful", "usefulness 2.2 vs 3.9 of 4", "judge score", "/home/user/clarity-framework/research/2026-framework-improvement/README.md", "repo", "2026-11-16", "B", "Synthetic cases, one model family, LLM judges."),
    ("EOY assets per account, top-50 sponsors with 1k-20k accounts", "median ~$406k; p25 ~$206k; p75 ~$673k (n=9)", "USD EOY", "/home/user/daf-landscape/data/mission-2026-11-14/daf-sponsor-league-table-fy2025-refresh.csv", "990", "FY2025 filed", "B", "[D] computed this session; year-end, not average billable."),
)
evidence_objs = tuple({"evidence_id": f"EV-ECH-{i+1:03d}", "claim": c, "value": v, "unit": u, "source_url_or_path": p,
                       "source_type": t, "filing_period": fp, "accessed": ACC, "quality": q, "notes": n}
                      for i, (c, v, u, p, t, fp, q, n) in enumerate(evidence))

assumptions = (
    ("Per-capability annual effects in echelon-capabilities.csv are analyst placeholders", "see CSV", "USD/yr", "-50000", "150000", "No quotes or measurements exist", ["EV-ECH-005", "EV-ECH-010"], "medium"),
    ("Loaded engineering cost for scenario arithmetic", "165000", "USD/FTE-yr", "124507", "250000", "Unbound parameters.json base", ["EV-ECH-014"], "high"),
    ("Conventional engineering team for a DAF platform", "4-10", "FTE", "4", "10", "daf-landscape model log scale [A]", ["EV-ECH-015"], "high"),
    ("Agent-assisted throughput multiplier (S1)", "1.5-2.0", "x", "1.0", "2.0", "Unmeasured; scenario only", ["EV-ECH-010", "EV-ECH-011"], "high"),
    ("Platform build capex", "5000000", "USD one-off", "3000000", "15000000", "Unbound parameters.json", ["EV-ECH-013"], "high"),
    ("Independent security review of Echelon-derived dependencies", "0-40000", "USD/yr", "0", "40000", "Placeholder; no quote", ["EV-ECH-007", "EV-ECH-009"], "low"),
    ("Commercial licence cost for PolyForm-NC components", "0-50000", "USD/yr", "0", "50000", "Placeholder; terms 'forthcoming'", ["EV-ECH-005"], "medium"),
    ("Public-data screening reuse reduces data/identity variable cost", "0-5", "USD/account-yr", "0", "5", "Placeholder", ["EV-ECH-016", "EV-ECH-017"], "low"),
)
assumption_objs = tuple({"assumption_id": f"A-ECH-{i+1:03d}", "statement": s, "value": v, "unit": u, "low": lo, "high": hi,
                         "basis": b, "evidence_ids": e, "sensitivity": se}
                        for i, (s, v, u, lo, hi, b, e, se) in enumerate(assumptions))

files = {
    "echelon-capabilities.csv": csv_text(COLS, caps_rows),
    "assumption-challenge-template.csv": csv_text(tmpl_cols, tmpl_rows),
    "framework-procedure.jsonl": jsonl_text(STEPS),
    "report.jsonl": jsonl_text(report + ({"section": "Framework revisions used", "markdown": md_table(["Repository", "Revision"], list(REV.items()))},)),
    "evidence.jsonl": jsonl_text(evidence_objs),
    "assumptions.jsonl": jsonl_text(assumption_objs),
}
for name, text in files.items():
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as fh:
        fh.write(text)

# validate
for name in files:
    path = f"{OUT}/{name}"
    if name.endswith(".jsonl"):
        n = sum(1 for line in open(path, encoding="utf-8") if json.loads(line) is not None)
    else:
        rows = list(csv.reader(open(path, encoding="utf-8")))
        assert all(len(r) == len(rows[0]) for r in rows), name
        n = len(rows) - 1
    print(name, n)
