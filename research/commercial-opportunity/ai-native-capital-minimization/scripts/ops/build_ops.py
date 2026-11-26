"""OPS group generator: outcome-designed DAF servicing organization and residual human work.

Run: python3 -I -B build_ops.py <out_dir>
Every minute is an assumption [A] unless a source is named; no time study exists (CNV-EVB-001).
Functional style: data as tuples, pure functions, one write pass at the end.
"""
import csv
import json
import math
import sys
from functools import reduce

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ACT = "/home/user/daf-landscape/data/commercial-opportunity/servicing-economics/activities.csv"
CAP = "/home/user/daf-landscape/data/commercial-opportunity/servicing-economics/capacity-model.csv"
CLAUSES = "/home/user/unbound/requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl"
PARAMS = "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/model/src/ServicingEconomics/Parameters.fs"

# ------------------------------------------------------------------ constants (labelled)
PRODUCTIVE_H = 1520.0          # [S] Parameters.fs:145 (itself [D/A])
QUEUE_UTIL = 0.9               # [S] Parameters.fs:148 (itself [A])
QUEUE_MIN_PER_FTE_YR = PRODUCTIVE_H * QUEUE_UTIL * 60.0   # [D] 82,080
WORKDAYS = 250.0               # [A]
QUEUE_MIN_PER_FTE_DAY = QUEUE_MIN_PER_FTE_YR / WORKDAYS   # [D] 328.3
OPS_LOADED = 99478.0           # [S] role-compensation.csv (grant & client ops specialist)
USD_PER_MIN = OPS_LOADED / PRODUCTIVE_H / 60.0            # [D] 1.0908
MIX_REVENUE_PER_ACCT = 877.2   # [S] capacity-model.csv market_mix revenue_at_20bps
MIX_BALANCE = 438600.0         # [S] capacity-model.csv
MIX_VAR_TOTAL_AI_NATIVE = 88.78  # [S] capacity-model.csv market_mix ai_native incremental_total_usd_base
MIX_LABOUR_AI_NATIVE = 42.27     # [S] capacity-model.csv labour_usd_at_50h_base
FIXED_MODEL_B = 1.74e6           # [S] report 10 Q6 (Model B economic fixed cost)
DEC_SHARE_MIX = 0.265            # [S] capacity-model.csv market_mix ai_native december_share
DEC_WORKDAYS = 20.0              # [A]
SAMPLE_N_95_5 = math.ceil(math.log(0.05) / math.log(0.95))  # [D] zero-deviation attribute sample, 95% conf, 5% tolerable = 59


def r2(x):
    return round(x, 2)


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


ACTS = {r["activity_id"]: r for r in read_csv(ACT)}
CAPS = {(r["archetype"], r["approach"]): r for r in read_csv(CAP)}


def base_of(aid):
    r = ACTS[aid]
    return float(r["typical_min_per_acct_yr_ai_native"]) if aid.startswith("ACT-A") else float(r["minutes_ai_native_base"])


# ------------------------------------------------------------------ PART 2 work elimination
# (activity_id, method, after, eliminated, transferred, transferred_to, control_preserved, evidence, quality)
# Order applied: prevent > eliminate > consolidate > simplify > automate deterministically > AI > human.
W = [
    ("ACT-A01", "prevent: rely on custodian/advisor KYC under a written reliance agreement; successor designation captured at opening; simplify: one structured application; automate: deterministic OFAC + identity checks; AI: entity-document extraction; human: mismatches and entity donors only",
     0.24, 0.08, 0.04, "advisor/custodian (KYC reliance work they already perform; needs reliance agreement)", "OFAC screening at onboarding stays deterministic and fail-closed (CNV-GRT-006); identity proofing risk-based (CNV-PLT-003)", "activities.csv ACT-A01; CNV-PLT-003; CNV-GRT-006", "D"),
    ("ACT-A02", "prevent: structured fund reference at payment initiation (input design); automate: exact-match posting and four-date recording (CNV-FIN-003); human: unidentified/returned items",
     0.20, 0.08, 0.02, "donor (enters fund reference)", "return handling by reason code; contribution reversal rules (CNV-FIN-003)", "activities.csv ACT-A02 exception_rate 2-10% [A]", "D"),
    ("ACT-A03", "prevent: steer to ACH; automate: lockbox imaging and deterministic posting; AI: image reading of payer/memo; human: illegible/unidentified",
     0.45, 0.22, 0.08, "donor (re-initiates as ACH)", "dual custody of paper at lockbox vendor; positive deposit reconciliation", "activities.csv ACT-A03; lockbox $0.65 [S] Unbound parameters.json:320 via activities.csv", "D"),
    ("ACT-A04", "prevent: pre-announced transfers with structured fund reference (DTC memo); automate: custodian feed matching (CNV-FIN-013); human: unmatched deliveries",
     1.00, 0.80, 0.20, "donor and donor's broker (pre-announcement form, memo field)", "valuation source fixed by rule; unmatched deliveries queue (CNV-FIN-013)", "activities.csv ACT-A04 (unidentified securities a known pain point, anecdotal)", "D"),
    ("ACT-A05", "consolidate/transfer: agent-model intermediary for non-public assets (CNV-GRT-013); AI: appraisal/LP/8283 document reading; human: sponsor gift-acceptance decision (reserved) and Form 8283/8282 obligations",
     0.45, 0.15, 0.30, "external intermediary (fund-borne fee $150-1,500 [A]); appraiser (donor-borne)", "sponsor remains donee of record; gift acceptance reserved to sponsor (CNV-GRT-013)", "activities.csv ACT-A05; CNV-GRT-013", "C"),
    ("ACT-A06", "already self-service with Nacha authorization retention; no further elimination found", 0.03, 0.0, 0.0, "", "Nacha authorization retention (CNV-PAY-005)", "activities.csv ACT-A06", "D"),
    ("ACT-A07", "prevent: structured purpose and attestation at entry; eliminate: email/paper intake; automate: authority and duplicate checks",
     0.45, 0.30, 0.15, "donor/advisor (attestation fields at entry)", "recommender authority check; duplicate detection", "activities.csv ACT-A07 (2-10% touched)", "D"),
    ("ACT-A08", "automate: continuous charity-status subscription with source posting dates; reuse platform determinations within freshness window; human: list mismatches only",
     0.15, 0.12, 0.0, "", "check at approval and release; fail safe when stale (CNV-GRT-003)", "activities.csv ACT-A08 (11.2% of recipient rows route to a person, replay)", "B"),
    ("ACT-A09", "eliminate scheduled 180-day human re-review for unchanged evidence: continuous monitoring with event-triggered invalidation and refresh renews deterministically; human only when evidence changed/conflicts/missing (needs sponsor policy adoption)",
     0.40, 0.68, 0.0, "", "180-day default deep review and event invalidation retained (CNV-GRT-003); sampled independent check", "activities.csv ACT-A09; CNV-GRT-003", "B"),
    ("ACT-A10", "continuous monitoring detects MORE adverse events earlier (revocations median posting lag 89 days, replay); AI triages news and grades sources, may add flags never clear; human dispositions",
     0.25, -0.02, 0.0, "", "AI may add a flag, never clear one (EV-ACT-041 via activities.csv)", "activities.csv ACT-A10", "B"),
    ("ACT-A11", "prevent: structured entry and determination reuse cut first-time exceptions (replay 11.2% raw -> 4.0% within sponsor -> 3.1% platform); automate: board-delegated deterministic approval of conforming grants (CNV-GRT-001); AI: decision dossier; human: servicer reviews dossier, sponsor-appointed person decides (SPD-ADV-001)",
     9.50, 3.10, 0.0, "", "board delegation with expiry and quarterly report (CNV-GRT-001, CNV-GOV-008); dossier deterministic section AI cannot edit (CNV-AIO-002)", "activities.csv ACT-A11 exception rates (replay, EV-ACT-017/032)", "C"),
    ("ACT-A12", "prevent: structured no-benefit attestation and pledge-policy choice at entry; AI flags only; human clears every flag",
     1.80, 0.43, 0.20, "donor/advisor (attestation)", "AI adds flags only; human clears (CNV-GRT-009/010)", "activities.csv ACT-A12 (0.5-5% touched [A])", "D"),
    ("ACT-A13", "consolidate: route foreign grants via US intermediaries (CNV-GRT-008); reuse equivalency determinations across grants to the same recipient within validity; AI: document reading; human: qualified reviewer for ER/ED",
     2.20, 1.00, 2.20, "US intermediary / ED provider (fee borne by fund or charity)", "qualified reviewer; ER reporting follow-up; OFAC/FCPA diligence (CNV-GRT-007)", "activities.csv ACT-A13; RCF ~$4k international diligence [S] via simplification 07", "C"),
    ("ACT-A14", "automate: bank-originated account-owner match for destination; absorbs grants moved from checks (A15) so net minutes RISE",
     0.75, -0.15, 0.0, "", "account-owner match or document + independent callback (CNV-PAY-002)", "activities.csv ACT-A14", "C"),
    ("ACT-A15", "prevent: EFT default with charity self-enrollment; residual checks ~1/3 (Fidelity still 33% checks in 2025 per activities.csv)",
     1.20, 1.96, 0.40, "charity (EFT enrollment and bank-detail upkeep)", "positive pay daily issue file (CNV-PAY-002)", "activities.csv ACT-A15", "B"),
    ("ACT-A16", "automate callback scheduling and dual-authorization workflow; human release authorization stays", 0.25, 0.02, 0.0, "", "dual authorization; callback", "activities.csv ACT-A16", "D"),
    ("ACT-A17", "prevent: fewer checks (follows A15); automate void disposition rules (CNV-PAY-003)", 0.45, 0.89, 0.0, "", "duplicate-payment controls; unclaimed property rules (CNV-PAY-003)", "activities.csv ACT-A17 (3% of check grants [A])", "D"),
    ("ACT-A18", "prevent: structured references cut breaks; continuous reconciliation auto-passes exact matches (CNV-FIN-004); independent risk-stratified attestation retained",
     0.70, 0.45, 0.0, "", "reconciliation outside payment chain (CNV-GOV-003); monthly controller sign-off (CNV-FIN-004)", "activities.csv ACT-A18 breaks 1% (0.2-3%) [A]", "D"),
    ("ACT-A19", "automate: versioned fee basis computed daily (CNV-FIN-002)", 0.03, 0.02, 0.0, "", "versioned fee basis; reconciliation to GL", "activities.csv ACT-A19", "D"),
    ("ACT-A20", "automate: statements and acknowledgments generated from authoritative ledger; electronic default", 0.10, 0.10, 0.0, "", "content rules; correction alerts (CNV-PLT-005)", "activities.csv ACT-A20", "D"),
    ("ACT-A21", "prevent: proactive grant/contribution status projection (CNV-EXP-003) removes 'where is my grant' contacts; AI grounded answers; human by right on request, complaints and accessibility",
     1.20, 0.70, 0.10, "donor (self-service navigation effort)", "no misstatement; escalation to human; WCAG 2.2 AA (CNV-EXP-001)", "activities.csv ACT-A21", "D"),
    ("ACT-A22", "automate custodian/advisor feed normalization (CNV-FIN-013); relay allocation choices only", 0.15, 0.05, 0.0, "", "feed reconciliation; no advice (CNV-LEG-001)", "activities.csv ACT-A22", "D"),
    ("ACT-A23", "prevent: destination controls and cooling-off reduce successful fraud, NOT investigation volume; proactive anomaly detection adds alerts; human investigates", 0.24, 0.0, 0.0, "", "callback, cooling-off, destination-change notification (CNV-PLT-011)", "activities.csv ACT-A23", "C"),
    ("ACT-A24", "automate: token matcher (0.9 vs 10.5 alerts per 1,000 names, replay) already in baseline; reuse false-positive dispositions within sponsor", 0.15, 0.02, 0.0, "", "never auto-close true matches; dispatch fencing (CNV-GRT-006, CNV-ARC-003)", "activities.csv ACT-A24", "B"),
    ("ACT-A25", "simplify: self-service changes with step-up and old-channel notification", 0.20, 0.05, 0.05, "donor (self-service, step-up)", "notify previous channel; 72h successor restriction (CNV-PLT-011)", "activities.csv ACT-A25", "D"),
    ("ACT-A26", "prevent: successor designation at opening; human remains for verification and disputes", 0.60, 0.10, 0.0, "", "protective suspension; documentary evidence (CNV-ENT-001)", "activities.csv ACT-A26", "D"),
    # sponsor-level, minutes per sponsor-year (S06/S07 per event)
    ("ACT-S01", "automate: continuous reconciliation and generated close packages from the ledger (IPE-supported); human: controller monthly sign-off and break decisions", 6000, 3000, 0, "", "monthly controller sign-off (CNV-FIN-004)", "activities.csv ACT-S01", "D"),
    ("ACT-S02", "simplify: configuration over custom engineering; standard policy packs with versioning; sponsor adopts changes", 2400, 900, 300, "sponsor (policy-pack adoption review)", "affirmative sponsor adoption of material changes (CNV-GOV-005)", "activities.csv ACT-S02", "D"),
    ("ACT-S03", "automate: proactive problem detection and runbooks; human incident command remains", 1400, 400, 0, "", "incident runbooks; breach notification obligations", "activities.csv ACT-S03 (high 12,000)", "D"),
    ("ACT-S04", "automate: transaction-time audit evidence with IPE support, only after the user auditor confirms reliance (CNV-GOV-001); until then manual procedures continue", 2200, 1100, 300, "sponsor's external auditor (testing generated evidence, sponsor-borne)", "IPE support: query, parameters, population counts, hash, run log (CNV-GOV-001)", "activities.csv ACT-S04", "D"),
    ("ACT-S05", "automate: generated quarterly board report and sample selection; human: sample review and sign-off", 720, 720, 0, "", "board acknowledgment required to renew delegation (CNV-GOV-008)", "activities.csv ACT-S05", "D"),
    ("ACT-S06", "simplify: repeatable onboarding with standard packs and reusable adapters; learning curve applies only to repeat counterparties (value shown at roughly the 4th-6th sponsor)", 12000, 6000, 0, "", "acceptance tests; ProvisionalCalibration of new feeds (CNV-FIN-004)", "activities.csv ACT-S06", "D"),
    ("ACT-S07", "AI: mapping and validation of predecessor data; human: opening-balance reconciliation and parallel run", 7000, 2000, 0, "", "parallel run; reconciliation of opening balances (CNV-EXP-002)", "activities.csv ACT-S07", "D"),
]


def we_row(t):
    aid, method, after, elim, trans, to, ctrl, ev, q = t
    base = base_of(aid)
    gap = r2(base - after - elim - trans)
    assert abs(gap) < 0.011, (aid, base, after, elim, trans, gap)
    unit = "min per typical account-year" if aid.startswith("ACT-A") else ("min per sponsor-year" if aid in ("ACT-S01", "ACT-S02", "ACT-S03", "ACT-S04", "ACT-S05") else "min per event (new sponsor / migration)")
    return {"activity_id": aid, "activity": ACTS[aid]["activity"], "unit": unit,
            "baseline_minutes_ai_native": base, "method": method, "minutes_after": after,
            "minutes_eliminated": elim, "minutes_transferred": trans, "transferred_to": to,
            "control_preserved": ctrl, "evidence": ev + "; minutes [A], no time study", "quality": q}


WE = [we_row(t) for t in W]
A_ROWS = [r for r in WE if r["activity_id"].startswith("ACT-A")]
TYP_BASE = sum(r["baseline_minutes_ai_native"] for r in A_ROWS)
TYP_AFTER = sum(r["minutes_after"] for r in A_ROWS)
TYP_ELIM = sum(r["minutes_eliminated"] for r in A_ROWS)
TYP_TRANS = sum(r["minutes_transferred"] for r in A_ROWS)
RATIO = {r["activity_id"]: (r["minutes_after"] / r["baseline_minutes_ai_native"] if r["baseline_minutes_ai_native"] else 1.0) for r in A_ROWS}
R_TYP = TYP_AFTER / TYP_BASE
# prior elimination scenario typical (for comparison)
PRIOR_ELIM_TYP = sum(float(ACTS[r["activity_id"]]["typical_min_per_acct_yr_elimination"]) for r in A_ROWS)


# ------------------------------------------------------------------ market-mix reconstruction [D]
def parse_top3(s):
    return dict((p.split("=")[0].strip(), float(p.split("=")[1])) for p in s.split(";"))


ARCH = ["inactive", "small_recurring", "typical", "high_frequency", "high_value", "complex_asset"]
SHARE = {"inactive": 0.2, "small_recurring": 0.2, "typical": 0.4, "high_frequency": 0.07, "high_value": 0.1, "complex_asset": 0.03}


def arch_after(a, col="servicer_min_per_acct_yr_base"):
    row = CAPS[(a, "ai_native")]
    total = float(row[col])
    if a == "typical":
        return total * R_TYP
    top = parse_top3(row["top3_activities_base"])
    scale = total / float(row["servicer_min_per_acct_yr_base"])
    known = sum(v * scale * RATIO.get(k, R_TYP) for k, v in top.items())
    rest = (total - sum(v * scale for v in top.values())) * R_TYP
    return known + rest


ARCH_BASE = {a: float(CAPS[(a, "ai_native")]["servicer_min_per_acct_yr_base"]) for a in ARCH}
ARCH_HIGH = {a: float(CAPS[(a, "ai_native")]["servicer_min_per_acct_yr_high"]) for a in ARCH}
ARCH_AFTER = {a: arch_after(a) for a in ARCH}
ARCH_AFTER_HIGH = {a: arch_after(a, "servicer_min_per_acct_yr_high") for a in ARCH}
MIX_BASE = sum(SHARE[a] * ARCH_BASE[a] for a in ARCH)
MIX_AFTER = sum(SHARE[a] * ARCH_AFTER[a] for a in ARCH)
MIX_TRANS = MIX_BASE * (TYP_TRANS / TYP_BASE)  # [E] transfer share of typical applied to mix

S_BASE_YR = sum(base_of(a) for a in ("ACT-S01", "ACT-S02", "ACT-S03", "ACT-S04", "ACT-S05"))
S_AFTER_YR = sum(r["minutes_after"] for r in WE if r["activity_id"] in ("ACT-S01", "ACT-S02", "ACT-S03", "ACT-S04", "ACT-S05"))

# ------------------------------------------------------------------ lower bound (irreducible) per account-year, market mix [A/D]
MIX_GRANTS = 0.2 * 0.5 + 0.2 * 4 + 0.4 * 9 + 0.07 * 40 + 0.1 * 15 + 0.03 * 10  # [A] grants per account-year by archetype
ACCTS_PER_SPONSOR_FLOOR = 4000.0  # [A] for allocating sponsor-level fixed control minutes
FLOOR = [
    # (component, servicer_min, sponsor_min, irreducible_class, basis, arithmetic)
    ("Exception grants: servicer review of AI dossier", MIX_GRANTS * 0.031 * 10, 0.0, "legal (s4966/4967 exclusive legal control requires a person to decide exceptions)", "CNV-GRT-001; CNV-AIO-002; replay 3.1% platform effective exception rate (activities.csv ACT-A11)", f"{MIX_GRANTS:.1f} grants x 3.1% x 10 min"),
    ("Exception grants: sponsor-appointed decision", 0.0, MIX_GRANTS * 0.031 * 5, "legal/contract (reserved authority, one-sponsor rule SPD-ADV-001)", "CNV-GOV-004; SPD-ADV-001 (unbound 23-EXECUTIVE-FINDINGS.md:13)", f"{MIX_GRANTS:.1f} x 3.1% x 5 min"),
    ("Prohibited-benefit flag clearing", MIX_GRANTS * 0.005 * 10, 0.0, "legal (s4967 penalties fall on donor/advisor and managers; AI may flag, never clear)", "CNV-GRT-009/010; CNV-AIO-001", f"{MIX_GRANTS:.1f} x 0.5% x 10 min"),
    ("Sanctions match disposition", 0.17, 0.0, "legal (31 CFR 501.603/604; never auto-close a true match)", "CNV-GRT-006; activities.csv ACT-A24", "0.0135 min x 12.5 screens"),
    ("Foreign/ER/ED grants qualified review (after intermediary routing)", MIX_GRANTS * 0.01 * 20, 0.0, "legal (s4966 ER/ED) and contracted-specialist reliance", "CNV-GRT-007/008/011", f"{MIX_GRANTS:.1f} x 1% x 20 min"),
    ("Complex-gift acceptance packet (intermediary does diligence)", 0.037 * 60, 0.037 * 30, "legal/contract (Form 8283/8282, s4943, sponsor gift acceptance reserved)", "CNV-GRT-013", "0.037 gifts/acct-yr (11.1/300 from capacity-model mix) x 60 min servicer + 30 min sponsor"),
    ("Fraud investigation", 0.002 * 120, 0.002 * 30, "uncertainty resolution / duty of care", "activities.csv ACT-A23", "0.002 x 120 min"),
    ("Succession, death, disputes", 0.02 * 35, 0.0, "contract (fund agreement) and documentary judgment", "CNV-ENT-001/002", "0.02 x 35 min"),
    ("Wire release dual authorization and callback", 0.06 * 4, 0.0, "control (dual authorization)", "activities.csv ACT-A16", "0.06 wires x 4 min"),
    ("Residual reconciliation breaks", 11.5 * 0.003 * 10, 0.0, "control (no silent write-offs)", "CNV-FIN-004", "11.5 tx x 0.3% x 10 min"),
    ("Independent sampling: delegated approvals + auto-passed reconciliation", (2 * 4 * SAMPLE_N_95_5 * 4) / ACCTS_PER_SPONSOR_FLOOR, 0.0, "independence (risk-stratified error-bound sampling; reviewer independent of preparer)", "CNV-GRT-011; CNV-FIN-004; CNV-GOV-003", f"2 populations x 4 quarters x n={SAMPLE_N_95_5} x 4 min / {ACCTS_PER_SPONSOR_FLOOR:.0f} accounts"),
    ("Controller monthly sign-off and unattributable-break decisions", (12 * 150) / ACCTS_PER_SPONSOR_FLOOR, 0.0, "control/ICFR (monthly completeness sign-off)", "CNV-FIN-004", "12 x 150 min / 4,000 accounts"),
    ("Board report preparation review (sponsor reviews separately)", 480 / ACCTS_PER_SPONSOR_FLOOR, 4 * 120 / ACCTS_PER_SPONSOR_FLOOR, "governance (delegation renewal needs board acknowledgment)", "CNV-GOV-008", "480 min servicer, 480 min sponsor per sponsor-year / 4,000"),
    ("Human service by right (complaints, requested human, vulnerable donors)", 0.1 * 8, 0.0, "policy/contract (complaint acknowledgment within 2 business days)", "CNV-PLT-005", "0.1 contacts x 8 min"),
    ("Accessibility accommodations (alternative channel, assisted completion)", 0.01 * 30, 0.0, "law/policy (accessible service must not be degraded to cut cost)", "CNV-EXP-001; CNV-ECO-002; CNV-GOV-006", "1% of accounts x 30 min"),
    ("Residual paper checks in and out (exceptions only)", 0.5, 0.0, "convention (donors/charities still use paper)", "activities.csv ACT-A03/A15", "[A]"),
]
FLOOR_SERVICER = sum(f[1] for f in FLOOR)
FLOOR_SPONSOR = sum(f[2] for f in FLOOR)
LEGAL_INDEP_KEYS = ("legal", "independence", "control")
FLOOR_LEGAL = sum(f[1] for f in FLOOR if f[3].startswith(LEGAL_INDEP_KEYS))


# ------------------------------------------------------------------ PART 3 handling targets
def fte_per_10k(m):
    return m * 10000 / QUEUE_MIN_PER_FTE_YR


def labour(m):
    return m * USD_PER_MIN


def breakeven_assets(var_per_acct):
    # A = F / (r - v/b); r = 0.002
    return FIXED_MODEL_B / (0.002 - var_per_acct / MIX_BALANCE)


NONLAB = MIX_VAR_TOTAL_AI_NATIVE - MIX_LABOUR_AI_NATIVE  # [D] 46.51 non-labour variable per account


def be_at(m):
    return breakeven_assets(NONLAB + labour(m))


PRE_DELEG_ADD = MIX_GRANTS * (1.0 + 3 * 0.1) + 2.0  # [A] batch review 1 min/grant + 3-person release 0.1 min x3 + manual NAV/ProvisionalCalibration 2 min
TARGETS = [
    (10, "infeasible at market mix without weakening control",
     "Only an inactive/small-recurring, digital-only book with no exception grants could reach it; at market mix it sits below the control floor",
     "Floor components alone (exception dossiers, flag clearing, ER review, complex gifts, sampling) exceed 10",
     "Would require auto-clearing flags or pooled reserved deciders: both prohibited (CNV-AIO-001, SPD-ADV-001)"),
    (20, "theoretically reachable, not demonstrable; needs every lever plus transfers",
     "All sponsors board-delegated (CNV-GRT-001) and auditor reliance on generated evidence (CNV-GOV-001); EFT >=95%; intermediaries for complex and foreign (a transfer to fee-bearing providers); measured exception rate <=3%; sponsors >=10,000 accounts each; mature year 3+",
     "A11 exception dossiers, A13 residual qualified review, A12 flag clearing, A21 human service, A05 acceptance packets",
     "Thin margin over the floor: any rise in exception rate (each +1 pt of 9.1 grants x 10 min = +0.9 min) or December backlog breaks it"),
    (30, "plausible steady-state design point after redesign (this pass)",
     "Board delegation in place, continuous charity monitoring, continuous reconciliation, proactive status, EFT default; sponsors >=4,000 accounts; independent sampling contracted",
     "A11 (about a third), A13, A21, A12, A05",
     "Depends on exception incidence that only a 90-day time study can measure (CNV-EVB-001)"),
    (50, "prior AI-native base (50.7); achievable without most transfers",
     "AI-native processes without input redesign or intermediary routing; board delegation in place",
     "A11, A05, A13, A15/A17 checks, A09 renewals", "Transfer-free; the honest planning case for year 2"),
    (75, "realistic during pre-delegation (year 1 of each sponsor)",
     "No board delegation yet: individual batch approvals on dossiers, three-distinct-person release (CNV-GOV-003), ProvisionalCalibration 100% review of non-exact recon items (CNV-FIN-004), manual NAV checks (CNV-ECO-005)",
     "per-grant batch approval, release, A11, recon calibration", "Every new sponsor passes through this phase; mixes with steady state in the book"),
    (100, "failure case: redesign not achieved (AI-enhanced is 124)",
     "AI-assisted conventional processes; scheduled 180-day human re-review retained; checks retained",
     "A09 scheduled re-review, A11, A05, A15/A17", "Economics revert to the prior AI-enhanced case (report 10 Q3: $1.02-1.95B one sponsor)"),
]


def target_row(t):
    m, feas, model, dom, risk = t
    return {"row_type": "target", "target_min_per_account_year": m, "feasibility": feas, "operating_model_required": model,
            "dominant_remaining_activities": dom, "risk_or_condition": risk,
            "fte_per_10k_accounts_queue": r2(fte_per_10k(m)), "labour_usd_per_account_year": r2(labour(m)),
            "labour_share_of_20bps_revenue_mix": r2(labour(m) / MIX_REVENUE_PER_ACCT),
            "breakeven_assets_usd_bn_modelB_fixed": r2(be_at(m) / 1e9),
            "servicer_min": "", "sponsor_min": "", "irreducible_class": "",
            "evidence": "[D] FTE = m x 10,000 / 82,080; labour = m x $1.0908; break-even A = 1.74M / (0.002 - (46.51 + labour)/438,600); minutes [A]",
            "label": "D from A"}


def floor_row(f):
    comp, sv, sp, cls, basis, arith = f
    return {"row_type": "floor_component", "target_min_per_account_year": "", "feasibility": "", "operating_model_required": comp,
            "dominant_remaining_activities": arith, "risk_or_condition": basis, "fte_per_10k_accounts_queue": r2(fte_per_10k(sv)),
            "labour_usd_per_account_year": r2(labour(sv)), "labour_share_of_20bps_revenue_mix": "", "breakeven_assets_usd_bn_modelB_fixed": "",
            "servicer_min": r2(sv), "sponsor_min": r2(sp), "irreducible_class": cls, "evidence": basis, "label": "A"}


SUMMARY_ROWS = [
    ("redesign_result_market_mix", MIX_AFTER, f"[D] archetype reconstruction: typical {TYP_BASE:.2f}->{TYP_AFTER:.2f} (ratio {R_TYP:.3f}); known top-3 activities scaled by own ratios"),
    ("redesign_transferred_market_mix", MIX_TRANS, "[E] typical transfer share applied to mix; NOT eliminated"),
    ("prior_ai_native_market_mix", MIX_BASE, "[S] capacity-model.csv market_mix ai_native"),
    ("prior_elimination_scenario_market_mix", 33.8, "[S] capacity-model.csv market_mix elimination (counts transfers as eliminated)"),
    ("lower_bound_servicer", FLOOR_SERVICER, "[D] sum of floor components; excludes sponsor-level onboarding, engineering, sales, management"),
    ("lower_bound_servicer_legal_independence_control_only", FLOOR_LEGAL, "[D] subset whose class is legal, independence or control"),
    ("lower_bound_sponsor_side", FLOOR_SPONSOR, "[D] sponsor-appointed minutes; not servicer cost but real cost to the buyer"),
    ("pre_delegation_addition", PRE_DELEG_ADD, "[A] batch review + three-person release + calibration"),
    ("sponsor_level_after_per_account_at_4000", S_AFTER_YR / 4000.0, f"[D] {S_AFTER_YR:.0f} min per sponsor-year / 4,000 accounts"),
    ("sponsor_level_after_per_account_at_10000", S_AFTER_YR / 10000.0, f"[D] {S_AFTER_YR:.0f} / 10,000"),
]


def summary_row(s):
    name, m, ev = s
    return {"row_type": "summary", "target_min_per_account_year": r2(m), "feasibility": name, "operating_model_required": "", "dominant_remaining_activities": "",
            "risk_or_condition": "", "fte_per_10k_accounts_queue": r2(fte_per_10k(m)), "labour_usd_per_account_year": r2(labour(m)),
            "labour_share_of_20bps_revenue_mix": r2(labour(m) / MIX_REVENUE_PER_ACCT), "breakeven_assets_usd_bn_modelB_fixed": "",
            "servicer_min": "", "sponsor_min": "", "irreducible_class": "", "evidence": ev, "label": "D"}


HT = [target_row(t) for t in TARGETS] + [summary_row(s) for s in SUMMARY_ROWS] + [floor_row(f) for f in FLOOR]

# ------------------------------------------------------------------ workload tails, segments, peaks
SEGMENTS = [
    # (name, share/frequency, unit, min_before, min_after, driver, irreducible_min, notes)
    ("routine accounts (inactive+small+typical)", 0.8, "share of accounts", sum(SHARE[a] * ARCH_BASE[a] for a in ARCH[:3]) / 0.8, sum(SHARE[a] * ARCH_AFTER[a] for a in ARCH[:3]) / 0.8, "grants x exception rate", 2.0, "[D] share-weighted archetype minutes"),
    ("high-frequency grantmakers", 0.07, "share of accounts", ARCH_BASE["high_frequency"], ARCH_AFTER["high_frequency"], "grants (about 40/yr [A]) x exception rate; checks", 8.0, "[D]; 18% of mix minutes on 7% of accounts"),
    ("high-value accounts", 0.10, "share of accounts", ARCH_BASE["high_value"], ARCH_AFTER["high_value"], "large/unusual grants -> Tier-2 triggers (CNV-GRT-011); relationship service", 6.0, "[D]"),
    ("complex contributions (per gift)", 0.037, "gifts per account-year (mix)", 300.0, 150.0, "gift acceptance, appraisal, 8283/8282, s4943", 90.0, "[A] per occurrence; intermediary does diligence (transfer)"),
    ("international / ER / ED grants (per grant)", 0.01, "share of grants", 60.0, 25.0, "ED/ER diligence, OFAC GL, FCPA", 20.0, "[A] per grant after ED reuse and intermediary routing"),
    ("accessibility accommodations (per case)", 0.01, "accounts per year", 30.0, 30.0, "alternative channel, assisted completion", 30.0, "[A]; NOT reduced: degrading accommodation to save minutes is prohibited (CNV-GOV-006 non-removable)"),
    ("fraud / compliance investigations (per case)", 0.002, "cases per account-year", 120.0, 120.0, "attempts, BEC, ATO, sanctions true match", 120.0, "[A] activities.csv ACT-A23; detection volume may rise with monitoring"),
    ("exceptional service requests (per case)", 0.05, "cases per account-year", 30.0, 25.0, "disputes, corrections, unusual instructions", 20.0, "[A]"),
]


def seg_row(s):
    name, freq, unit, b, a, drv, irr, notes = s
    return {"row_type": "segment", "name": name, "share_or_frequency": freq, "frequency_unit": unit, "minutes_before": r2(b), "minutes_after": r2(a),
            "contribution_min_per_mix_account_year": r2(freq * a), "human_irreducible_min": irr, "driver": drv, "fte_needed": "", "fte_available": "", "backlog_case_days": "", "legal_deadlines_at_risk": "", "notes": notes, "label": "D from A"}


# percentile accounts (archetype step distribution; within-archetype spread from capacity-model high column)
def cum_pct():
    order = sorted(ARCH, key=lambda a: ARCH_AFTER[a])
    acc = reduce(lambda l, a: l + [(a, (l[-1][1] if l else 0.0) + SHARE[a])], order, [])
    return acc


CUM = cum_pct()


def percentile_arch(p):
    return next(a for a, c in CUM if c >= p - 1e-9)


PCT = [("p50 account", 0.50), ("p90 account", 0.90), ("p99 account", 0.99)]


def pct_row(p):
    name, q = p
    a = percentile_arch(q)
    return {"row_type": "percentile", "name": name, "share_or_frequency": q, "frequency_unit": "account percentile by minutes", "minutes_before": r2(ARCH_BASE[a]),
            "minutes_after": r2(ARCH_AFTER[a]), "contribution_min_per_mix_account_year": "", "human_irreducible_min": "",
            "driver": f"archetype step distribution -> {a}; within-archetype high case after = {ARCH_AFTER_HIGH[a]:.1f}", "fte_needed": "", "fte_available": "", "backlog_case_days": "",
            "legal_deadlines_at_risk": "", "notes": "[D] archetype shares A-ACT-014 are assumptions; no account-level distribution observed", "label": "D from A"}


# December stress on a 10,000-account, 4-sponsor book
BOOK_ACCTS, BOOK_SPONSORS = 10000.0, 4.0
ANNUAL_ACCT_MIN = BOOK_ACCTS * MIX_AFTER
AVG_DAY = ANNUAL_ACCT_MIN / WORKDAYS + BOOK_SPONSORS * S_AFTER_YR / WORKDAYS
BASE_FTE = max(2.0, math.ceil((ANNUAL_ACCT_MIN + BOOK_SPONSORS * S_AFTER_YR) * 1.15 / QUEUE_MIN_PER_FTE_YR))
SURGE_FTE = 2.0  # [A] pre-contracted prep-only surge reviewers (CNV-SVC-002)
AI_OUTAGE_MULT = 1.6     # [A] exception handling x2 on ~60% of work, from WE-2 'x2 during AI outage'
INCIDENT_CASES_MIN = BOOK_ACCTS * 0.02 * 20 / 5.0  # [A] 0.02 unknown-state cases/acct (WE-2) x 20 min spread over 5 days


PEAK_SHARE_LAST7 = 0.5   # [A] last 7 working days carry half of December volume
SPONSOR_DAY = BOOK_SPONSORS * S_AFTER_YR / WORKDAYS
DEC_TOTAL_ACCT = ANNUAL_ACCT_MIN * DEC_SHARE_MIX
JAN_DAY = ANNUAL_ACCT_MIN * (1 - DEC_SHARE_MIX) / (WORKDAYS - DEC_WORKDAYS) + SPONSOR_DAY  # [D] non-December average day


def december_loads(ai_outage_days=0, incident_days=0):
    """20 working days: 13 ordinary December days then 7 peak days (last week). Outage/incident hit the first peak days."""
    ordinary = DEC_TOTAL_ACCT * (1 - PEAK_SHARE_LAST7) / 13.0
    peak = DEC_TOTAL_ACCT * PEAK_SHARE_LAST7 / 7.0
    days = [ordinary] * 13 + [peak] * 7
    return [d * (AI_OUTAGE_MULT if 13 <= i < 13 + ai_outage_days else 1.0) + SPONSOR_DAY + (INCIDENT_CASES_MIN if 13 <= i < 13 + incident_days else 0.0)
            for i, d in enumerate(days)]


def capacity(core, surge, absent_peak_week):
    return [(core + surge - (absent_peak_week if i >= 13 else 0)) * QUEUE_MIN_PER_FTE_DAY for i in range(20)]


def run_december(loads, caps):
    return reduce(lambda b, lc: max(0.0, b + lc[0] - lc[1]), zip(loads, caps), 0.0)


def clear_days(backlog, core):
    spare = core * QUEUE_MIN_PER_FTE_DAY - JAN_DAY
    return float("inf") if spare <= 0 else backlog / spare


def core_needed(loads, surge, absent, within_days=10):
    return next(c for c in range(2, 100) if clear_days(run_december(loads, capacity(c, surge, absent)), c) <= within_days)


def stress(name, loads, core, surge, absent, deadlines, notes):
    caps = capacity(core, surge, absent)
    backlog = run_december(loads, caps)
    cd = clear_days(backlog, core)
    need = core_needed(loads, surge, absent)
    return {"row_type": "peak_scenario", "name": name, "share_or_frequency": f"core {core} + surge {surge} - absent {absent}", "frequency_unit": "10,000 accounts, 4 sponsors",
            "minutes_before": r2(sum(loads)), "minutes_after": r2(max(loads)), "contribution_min_per_mix_account_year": "", "human_irreducible_min": "",
            "driver": "December minutes total (minutes_before) and peak day (minutes_after)", "fte_needed": need, "fte_available": core,
            "backlog_case_days": f"backlog {backlog:,.0f} min at 31 Dec; {('never' if cd == float('inf') else f'{cd:.1f}')} January working days to clear",
            "legal_deadlines_at_risk": deadlines, "notes": notes + "; fte_needed = core FTE so the 31 Dec backlog clears within 10 January working days", "label": "D from A"}


AVG_FTE = (ANNUAL_ACCT_MIN + BOOK_SPONSORS * S_AFTER_YR) / QUEUE_MIN_PER_FTE_YR
PEAKS = [
    {"row_type": "peak_scenario", "name": "average working day (annual sizing)", "share_or_frequency": "", "frequency_unit": "10,000 accounts, 4 sponsors", "minutes_before": "", "minutes_after": r2(AVG_DAY),
     "contribution_min_per_mix_account_year": "", "human_irreducible_min": "", "driver": "minutes per working day", "fte_needed": r2(AVG_FTE), "fte_available": BASE_FTE, "backlog_case_days": "none",
     "legal_deadlines_at_risk": "none", "notes": f"[D] ({BOOK_ACCTS:.0f} x {MIX_AFTER:.1f} + 4 x {S_AFTER_YR:.0f}) / 82,080; annual sizing x1.15, floor 2 = {BASE_FTE:.0f}", "label": "D from A"},
    stress("December, no disruption", december_loads(), BASE_FTE, 0, 0, "service SLAs; donors expect grants paid before 31 Dec (expectation, not law)", "[D/A] December share 0.265; last 7 days carry 50% [A]"),
    stress("December with 2 prep-only surge", december_loads(), BASE_FTE, SURGE_FTE, 0, "as above", "[A] surge prep-only cannot release (report 03:111)"),
    stress("December + 2-day AI outage in peak week", december_loads(ai_outage_days=2), BASE_FTE, SURGE_FTE, 0, "complaint acknowledgment 2 business days (CNV-PLT-005)", "[A] outage multiplies load x1.6 (simplification WE-2 x2 on exception handling)"),
    stress("December + AI outage + one core ops absent for peak week", december_loads(ai_outage_days=2), BASE_FTE, SURGE_FTE, 1, "dual control at risk: second releaser must be pre-appointed", "[A]"),
    stress("December + AI outage + absence + 5-day feed incident", december_loads(ai_outage_days=2, incident_days=5), BASE_FTE, SURGE_FTE, 1,
           "OFAC reports within 10 business days if blocks occur (31 CFR 501.603/604); statements blocked for affected funds (CNV-FIN-004)", "[A] 0.02 unknown-state cases per account x 20 min (simplification WE-2) over 5 days"),
]

WT = [seg_row(s) for s in SEGMENTS] + [pct_row(p) for p in PCT] + PEAKS

# ------------------------------------------------------------------ PART 4 staffing capacity
# (role, required_activities, driver, frequency_basis, handling_time, units_per_hour_or_capacity, threshold_formula, peak_factor,
#  min_for_independence, absence_cover, authority, independence, sla, failure_consequence, basis, replaces_prior_trigger)
STAFF = [
    ("Grant & client operations specialist", "A01-A04, A07-A17 exception queue, A21 human service, A25-A26, payment release (one of two)",
     "account-level human minutes (mix) + sponsor configuration minutes", "per account-year and per sponsor-year", f"{MIX_AFTER:.1f} min/account-yr after redesign (mix) [D from A]",
     f"{QUEUE_MIN_PER_FTE_YR:.0f} queue min/FTE-yr ({QUEUE_MIN_PER_FTE_DAY:.0f}/day) [D]", "core FTE = max(2, ceil(annual x 1.15 / 82,080), smallest core whose 31 Dec backlog (with prep-only surge) clears within 10 January working days); annual = N x m_acct + S x s_cfg",
     "December peak-week day ~= 4.7x average account-level day (0.265 x 0.5 / 7 x 250) [D/A]; core sized so the 31 Dec backlog clears in 10 January working days", 2, "second trained releaser + pre-appointed backup releaser (controller cannot be the second releaser on payments it reconciles)",
     "prepare; release as one of two/three distinct persons; no reserved decisions", "preparer != releaser (CNV-GOV-003)", "exceptions within sponsor-set business days; complaints acknowledged in 2 business days (CNV-PLT-005)",
     "late grants, missed year-end dating, dual control collapse", "CNV-GOV-003; CNV-SVC-002; Parameters.fs:145-151", "none (prior: ops manager after 4 added ops staff)"),
    ("Sponsor-appointed decision-maker (sponsor staff or contracted, NOT servicer)", "A05 acceptance, A11 exception decisions, A12 flag clearing escalations, discretionary holds, delegation adoption",
     "exceptions x decision minutes per sponsor", "per sponsor", "5 min per exception decision; 30 min per complex gift [A]", "exclusive to one sponsor (SPD-ADV-001)",
     "per sponsor: >= 2 appointees (primary + backup) + pre-appointed December surge reviewer; capacity rarely binding", "December 2-3x on exception decisions", 2,
     "named backup appointee per decision class; double absence tested as December stress (CNV-GOV-004)", "reserved (A3+) by board resolution", "cannot be servicer staff (CNV-GOV-004: vendor staff SHALL NOT hold A3+)",
     "sponsor-set decision SLA", "grants stall Held; CoverageGap", "CNV-GOV-004; SPD-ADV-001; CNV-GRT-001", "new (not in prior model; a cost the buyer bears)"),
    ("Controller / head of financial operations", "S01 close and sign-off, unattributable-break decisions, tolerance approval for new sources, fee basis, Schedule D bridge",
     "sponsors (books) + new feed sources + break volume; NOT accounts", "per sponsor-month; per new source; per break", "150 min sign-off per sponsor-month; ProvisionalCalibration: 100% review one close cycle per new source [A]",
     "about 60-75 sponsor-books per controller-year at 1,000-1,300 min each before close work [E]", "add a senior accountant when S x 12 x (sign-off + close review) + new_sources x calibration + breaks x 10 > 0.8 x 82,080",
     "year-end + audit season 2x", 1, "fractional/contracted controller pre-appointed as backup; sign-off may wait <= sponsor-set days", "monthly completeness sign-off; tolerance approval", "outside payment chain (CNV-GOV-003)",
     "monthly", "statements blocked for affected funds; audit qualification", "CNV-FIN-004; CNV-FIN-009; CNV-GOV-003", "replaces part of 'fund accountant per 15,000 accounts'"),
    ("Fund / reconciliation accountant", "A18 break resolution, A19 fee posting checks, custodian/advisor feed exceptions, unknown payment outcomes (CNV-PAY-004)",
     "breaks = transactions x break rate + new sources x calibration items", "per transaction (break rate 0.3-1% [A]); per new source", "10 min per break; calibration 100% non-exact review for one cycle [A]",
     "about 8,000 breaks per FTE-year at 10 min [D]", "FTE = ceil((T x b x 10 + calibration_items x 5) / 82,080); 0 until > 0.5 FTE (controller or outsourced bookkeeping covers)",
     "feed incidents 3-5x for days", 0, "outsourced reconciliation provider as backup (CNV-GOV-003 allows internal or outsourced)", "prepare and resolve breaks; no payment rights", "must not prepare or release payments",
     "exception review within sponsor-set business days", "unexplained breaks block statements for affected funds", "CNV-FIN-004; CNV-GOV-003; CNV-PAY-004", "replaces 'fund accountant per 15,000 accounts': scales with transactions x break rate and sources, not accounts"),
    ("Compliance officer (sanctions, Tier-2, regulatory change)", "A24 match dispositions, OFAC blocking/reject reports, A10 adverse events, Tier-2 policy, fraud case oversight, regulatory change into policy packs",
     "alerts + Tier-2 triggers + regulatory change; a named owner from day 1", "per screened event; per adverse event; per regulatory change", "15 min per adverse event; 20-60 min per true-match case [A]",
     "about 3,000-5,000 adverse/match cases per FTE-year [E]", "named fractional owner from go-live; employ when compliance minutes > 0.5 x 82,080 or any sponsor contract requires an employee",
     "list-update days and December", 1, "contracted sanctions specialist pre-engaged", "disposition proposals; report filing preparation; reserved blocks via sponsor officer", "independent of grant preparation for dispositions",
     "OFAC reports within 10 business days (31 CFR 501.603/604 via CNV-GRT-006)", "regulatory penalty exposure; unblocked prohibited payment", "CNV-GRT-006; CNV-GRT-011", "replaces 'compliance officer above 10,000 accounts' (accounts are a poor proxy)"),
    ("Independent reviewer (decision-quality and reconciliation attestation)", "CNV-GRT-011 sampling of delegated approvals; CNV-FIN-004 attestation of auto-passed items; board-report samples",
     "sponsors x populations x quarters x sample size", "per sponsor-quarter", f"4 min per sampled item; n={SAMPLE_N_95_5} per population-quarter at 95%/5% zero-deviation [D]",
     "about 20,000 items per FTE-year [D]", f"minutes = S x 2 x 4 x {SAMPLE_N_95_5} x 4 = S x {2*4*SAMPLE_N_95_5*4} min; contracted until > 0.5 FTE; raise n after material errors",
     "after material error or policy change: n increases", 1, "second contracted firm/person", "attest; cannot fix what it samples", "independent of preparer, releaser and policy author",
     "quarterly", "delegation cannot be renewed without acknowledged report (CNV-GOV-008)", "CNV-GRT-011; CNV-FIN-004; CNV-GOV-008", "new (prior model had no independent reviewer line)"),
    ("Integration engineer", "bank/custodian/CRM/ERP adapters, feed maintenance, NOC/return-file changes",
     "distinct counterparties (banks, custodians, ERPs) and their change rate, not sponsors", "per new counterparty; per live adapter-year", "new adapter 160-400 h; upkeep 20-40 h per adapter-year [A]",
     "about 1,500 engineering hours per FTE-year", "FTE = (new_adapters x 280 + live_adapters x 30) / 1,520 h; a repeat counterparty costs ~configuration only",
     "rail/format change deadlines", 0, "contract engineering retainer (prior CST-C05)", "code changes via two-approver control (CNV-PLT-010)", "author cannot approve own control-relevant change",
     "adapter fixes before next file cycle", "feeds fail; ProvisionalCalibration restarts", "CNV-PAY-007; CNV-FIN-013; CNV-PLT-010", "replaces 'integration engineer per 8 sponsors': learning curve applies to counterparties"),
    ("Implementation analyst", "S06 onboarding, S07 migration, policy-pack adoption support",
     "new sponsors per year x onboarding minutes(n) with learning curve", "per new sponsor", "S06 18,000 min first sponsor -> floor ~9,000 [A]; S07 7,000 + 2 min/account",
     "82,080 queue min per FTE-year", "onboarding(n) = 9,000 + 9,000 x n^-0.234 (85% curve [A]); FTE = ceil(sum over new sponsors / 82,080); 0 until > 0.5 FTE (CTO/ops absorb)",
     "launch clustering (several sponsors in one quarter)", 0, "contracted implementation partner", "configure; sponsor adopts", "configuration change control (CNV-GOV-005)",
     "go-live date in contract", "delayed revenue; parallel run extended", "CNV-GOV-005; CNV-EXP-002; CNV-ECO-005", "replaces 'implementation analyst per 8 sponsors': driver is new sponsors, not live sponsors"),
    ("Security / platform engineer (on-call)", "S03 incidents, ITGCs, change approvals, break-glass, DR",
     "on-call rota and two-approver change control; volume-insensitive", "continuous", "n/a", "one sustainable rota needs >= 3 people [A]",
     ">= 3 people able to approve control-relevant changes (author + 2 approvers, CNV-PLT-010), employees or contracted", "incident", 3, "rota of 3 incl. contracted",
     "production change approval; break-glass two-person", "two approvers, neither the author", "incident response per runbook", "unreviewed control change; SOC exception", "CNV-PLT-010; CNV-PLT-007", "new: change control sets a 3-person engineering floor"),
    ("Operations manager", "rostering, coverage, escalations, people management, December readiness gate",
     "human headcount and coverage complexity, not ops count", "continuous", "about 15-20% of a manager per 4 direct reports [A]", "span 6-8 direct reports [A]",
     "dedicated manager when human ops + accounting + compliance headcount >= 7 or founder coordination time > 0.3 FTE; before that founder/controller", "December readiness gate (CNV-SVC-002)", 0,
     "controller covers", "roster and assignment; no release rights over own escalations", "n/a", "roster coverage by role and day (CNV-GOV-004)", "coverage gaps; burnout", "CNV-SVC-001; CNV-SVC-002; CNV-GOV-004", "replaces 'ops manager after 4 added ops staff'"),
    ("December surge reviewer (pre-contracted)", "prep-only queue work; or reserved decisions if appointed by one sponsor",
     "December peak minus core capacity", "seasonal", "same as ops", "prep-only temps cannot release (prior report 03:111)", "surge FTE = ceil((peak_day_load - core_FTE x 328) / 328) for last 7 working days",
     "5.3x average day", 0, "n/a", "prepare only unless appointed by a single sponsor", "one-sponsor exclusivity when reserved (CNV-GOV-004)", "activation lead time ~5 working days (CNV-SVC-002)", "year-end deadlines missed", "CNV-SVC-002; CNV-GOV-004", "replaces 'December temps' line"),
]
STAFF_COLS = ["role", "required_activities", "driver", "frequency_basis", "handling_time", "units_per_hour_or_capacity", "threshold_formula", "peak_factor",
              "min_for_independence", "absence_cover", "authority", "independence", "sla", "failure_consequence", "basis", "replaces_prior_trigger"]


def staffing_at(n_accts, n_sponsors, new_sponsors, m=None, surge=2):
    m = MIX_AFTER if m is None else m
    annual = n_accts * m + n_sponsors * S_AFTER_YR
    annual_fte = max(2, math.ceil(annual * 1.15 / QUEUE_MIN_PER_FTE_YR))
    dec = n_accts * m * DEC_SHARE_MIX
    sp_day = n_sponsors * S_AFTER_YR / WORKDAYS
    loads = [dec * 0.5 / 13 + sp_day] * 13 + [dec * 0.5 / 7 + sp_day] * 7
    jan_day = n_accts * m * (1 - DEC_SHARE_MIX) / (WORKDAYS - DEC_WORKDAYS) + sp_day

    def clears(c):
        b = reduce(lambda acc, l: max(0.0, acc + l - (c + surge) * QUEUE_MIN_PER_FTE_DAY), loads, 0.0)
        spare = c * QUEUE_MIN_PER_FTE_DAY - jan_day
        return spare > 0 and b / spare <= 10

    dec_fte = next(c for c in range(2, 200) if clears(c))
    tx = n_accts * 11.5
    recon = (tx * 0.005 * 10) / QUEUE_MIN_PER_FTE_YR
    indep = n_sponsors * 2 * 4 * SAMPLE_N_95_5 * 4 / QUEUE_MIN_PER_FTE_YR
    onboard = sum(9000 + 9000 * (k ** -0.234) + 7000 for k in range(1, new_sponsors + 1)) / QUEUE_MIN_PER_FTE_YR
    return {"accounts": n_accts, "sponsors": n_sponsors, "min_per_acct": r2(m), "servicing_fte_annual_sizing": annual_fte,
            "servicing_fte_december_sizing": max(annual_fte, dec_fte), "recon_break_fte": r2(recon), "independent_review_fte": r2(indep), "implementation_fte": r2(onboard)}


STAFF_GRID = [staffing_at(a, s, ns) for a, s, ns in ((3000, 2, 1), (5000, 3, 1), (10000, 4, 1), (20000, 6, 2), (50000, 10, 3))] + \
             [staffing_at(a, s, ns, MIX_BASE) for a, s, ns in ((5000, 3, 1), (10000, 4, 1), (20000, 6, 2))]

# ------------------------------------------------------------------ PART 5 overhead
OVH = [
    # category, why, driver, conv h/FTE/wk, residual, removable, residual governance, basis
    ("meetings", "information fragmentation and coordination; some governance (incident, risk, board prep)", "fragmentation+habit", 3.0, 1.5, "partly: status/info-sharing meetings replaced by shared case and control state", "weekly ops/risk review; incident reviews; 1:1s", "MS WTI 2023: meetings 23% of M365 intentional time (telemetry) [S]; small-firm figure [A]"),
    ("status reports", "managers cannot see work state", "fragmentation", 0.8, 0.1, "yes: generated from case/event state", "exception narrative only", "[A]"),
    ("internal approvals", "governance (SoD) plus habit (spend, document sign-off)", "governance+habit", 0.7, 0.5, "partly: habit approvals removed; SoD approvals are controls and stay", "SoD approvals in the authority matrix (CNV-GOV-010)", "[A]"),
    ("project management", "cross-team dependency tracking", "fragmentation", 0.8, 0.4, "partly: workflow state replaces tracking; onboarding projects still need an owner", "onboarding plan with activation gates (CNV-ECO-005)", "[A]"),
    ("performance reporting", "management information assembled by hand", "fragmentation", 0.4, 0.1, "yes: generated from metered events (CNV-ECO-001)", "review of metrics", "[A]"),
    ("coordination / handoffs (chat, email)", "work split across people and tools", "fragmentation", 2.0, 0.7, "partly: assignment and clocks in the case kernel (CNV-SVC-001)", "escalations and judgment discussions", "MS WTI 2023: chat 19% + email 15% of M365 time [S]; [A]"),
    ("internal documentation", "knowledge retention, audit, onboarding staff", "governance", 0.8, 0.6, "little: AI drafts, humans must review; SOC evidence needs it", "control narratives, runbooks, policy rationale (CNV-GOV-006)", "[A]"),
    ("QA / rework review", "errors caught after the fact", "habit+governance", 0.8, 0.4, "partly: input design prevents errors; replaced by independent sampling", "independent risk-stratified sampling (CNV-GRT-011)", "[A]"),
    ("manual compliance / operational reporting", "regulators, auditors, sponsors need reports", "governance", 0.6, 0.15, "mostly: generated with IPE support after auditor reliance", "sign-off and exception explanation", "CNV-GOV-001 [A]"),
    ("admin assistant support (per FTE share)", "scheduling, filing, travel", "habit", 0.3, 0.0, "yes for a remote small firm", "none", "[A]"),
    ("ticket routing / triage", "unstructured intake", "fragmentation", 0.4, 0.05, "yes: typed intake and rule routing", "routing rule changes", "[A]"),
    ("repeated data entry", "systems do not share records", "fragmentation", 0.8, 0.1, "yes: one authoritative record", "none; WARNING partly already counted in activity minutes", "[A]"),
    ("interdepartmental reconciliation", "separate ledgers/spreadsheets per team", "fragmentation", 0.6, 0.15, "yes: one ledger, one case store", "controller reconciles to bank/custodian (external)", "[A]"),
]
OVH_CONV = sum(o[3] for o in OVH)
OVH_RES = sum(o[4] for o in OVH)
PRIOR_OVH_H = 40.0 * 0.15  # [S] report 03:111 '~15% meetings, supervision, admin' of ~1,830 worked h approximated per 40h week
LIVE_TEAM = 7.0  # [A]
LOADED_HOURLY_AVG = 150000.0 / 1830.0  # [A] average loaded $150k over worked hours


def ovh_row(o):
    cat, why, drv, conv, res, rem, gov, basis = o
    return {"category": cat, "why_it_exists": why, "cause_class": drv, "conventional_hours_per_fte_week": conv, "conventional_label": "A (informed by S where named)",
            "ai_native_residual_hours_per_fte_week": res, "removable_by_integrated_systems": rem, "residual_governance_needed": gov,
            "annual_value_per_fte_usd_if_converted": round((conv - res) * 46 * LOADED_HOURLY_AVG), "basis": basis}


OV = [ovh_row(o) for o in OVH] + [{
    "category": "TOTAL", "why_it_exists": "", "cause_class": "", "conventional_hours_per_fte_week": r2(OVH_CONV), "conventional_label": "A (range 8-14)",
    "ai_native_residual_hours_per_fte_week": r2(OVH_RES), "removable_by_integrated_systems": "", "residual_governance_needed": "",
    "annual_value_per_fte_usd_if_converted": round((OVH_CONV - OVH_RES) * 46 * LOADED_HOURLY_AVG),
    "basis": f"[D] prior model already deducts ~{PRIOR_OVH_H:.0f} h/wk (15%, report 03:111); gain vs prior model = {PRIOR_OVH_H - OVH_RES:.2f} h/FTE/wk; team of {LIVE_TEAM:.0f}: ${round((OVH_CONV - OVH_RES) * 46 * LOADED_HOURLY_AVG * LIVE_TEAM):,} vs conventional, ${round(max(0, PRIOR_OVH_H - OVH_RES) * 46 * LOADED_HOURLY_AVG * LIVE_TEAM):,} vs prior model, cash only if a hire is avoided"}]

# ------------------------------------------------------------------ PART 6 AI capabilities
AIC = [
    ("monitoring (feeds, lists, queues, SLAs)", "recommend/prepare (A1)", "watch bank, custodian, IRS list, OFAC and queue events; open cases", "cannot clear a hold, change a status of record or suppress an alert", "event id, source posting date, hash, rule version", "stale source beyond bound; anomaly outside tolerance", "deterministic fail-safe: stale list -> block release (CNV-GRT-003/006)", "CNV-GRT-003; CNV-GRT-006; CNV-AIO-001"),
    ("exception detection", "recommend (A1)", "add flags (benefit signals, related parties, unusual purpose, Tier-2 triggers)", "may add flags, never clear; cannot reorder deterministic findings", "flag rationale quoted from sources as data", "any flag -> human queue; batch approval refused with unresolved trigger", "deterministic triggers still fire without AI", "CNV-AIO-002; CNV-GRT-011; EV-ACT-041"),
    ("prioritisation", "prepare (A1)", "order queues within deterministic constraints", "no opaque weighted score; cannot deprioritise statutory deadlines", "ordering explanation; deadline map", "deadline collision -> escalate", "deterministic deadline-first ordering (CNV-SVC-001)", "CNV-SVC-001"),
    ("case assignment", "execute reversible internal (A2)", "assign by skill/round-robin/cradle-to-grave per case kind", "cannot assign reserved decisions to a person without the sponsor's appointment; restricted routing for fraud", "assignment log with rule version", "no eligible assignee within SLA -> CoverageGap to manager and sponsor", "rule-based assignment", "CNV-SVC-001; CNV-GOV-004"),
    ("customer service (donor/advisor answers)", "prepare/respond informational (A1-A2)", "grounded answers from status projection and approved content", "no individualized tax/investment advice; no promises; cannot change records", "answer with citations to record and content version", "low confidence, complaint, requested human, accessibility need, vulnerability signal -> human", "status pages and human queue", "CNV-AIO-001; CNV-GRT-014; CNV-EXP-001; CNV-PLT-005"),
    ("control evidence", "prepare (A1)", "assemble IPE-supported evidence packs and sample populations", "cannot select its own samples for attestation of its own work without independent seed; cannot mark a control effective", "query definition, parameters, population counts, hash, run log", "missing evidence -> control exception", "evidence generated by deterministic queries", "CNV-GOV-001; CNV-PLT-009"),
    ("compliance monitoring", "recommend (A1)", "track regulatory change, adverse news, list deltas; draft policy-pack change", "cannot activate a policy change; cannot disposition a sanctions match", "source, effective date, owner", "material change -> compliance officer and sponsor adoption", "list ingestion and delta screening are deterministic", "CNV-GRT-006; CNV-GOV-005"),
    ("reporting (sponsor, board, management)", "prepare (A1)", "generate narrative around generated figures", "cannot create or alter figures; numbers come only from the ledger", "figure provenance links; narrative labelled AI", "figure/narrative mismatch -> block publication", "deterministic report without narrative", "CNV-GOV-008; CNV-AIO-002"),
    ("onboarding (sponsor and migration)", "prepare (A1)", "map predecessor data, draft configuration from standard packs, generate acceptance tests", "cannot activate configuration or post opening balances", "mapping diff, reconciliation report", "unmapped or unreconciled items -> implementation analyst", "manual mapping", "CNV-EXP-002; CNV-GOV-005"),
    ("policy configuration", "prepare (A1)", "draft policy-pack versions and impact analysis", "cannot publish; sponsor must adopt material changes; change to gate modules needs two approvers", "draft diff, impact analysis", "material change -> sponsor adoption and auditor notice", "previous version stays in force", "CNV-GOV-005; CNV-GOV-003; CNV-PLT-010"),
    ("learning (from decisions and outcomes)", "recommend (A1)", "propose rule refinements and new determinations for reuse", "no self-modification in production; no training on one sponsor's private investigations for another", "proposal with evidence set and backtest", "every proposal -> human review and versioned release", "current rules", "CNV-GRT-004; CNV-PLT-010"),
    ("recurring-problem detection", "recommend (A1)", "cluster exceptions, contacts and breaks to find root causes (input design, feeds)", "cannot change processes; findings only", "cluster, counts, examples", "recurrence above threshold -> improvement case to owner", "periodic manual review", "CNV-GOV-006"),
    ("decision dossier preparation", "prepare (A1)", "assemble exception packets for servicer review and sponsor decision", "deterministic section built from sources and hashes AI cannot edit; narrative labelled; untrusted text quoted as data", "dossier hash; source hashes", "unresolved trigger -> no batch approval", "deterministic section alone", "CNV-AIO-002"),
    ("document extraction (complex gifts, ED, entity KYC)", "prepare (A1)", "extract terms from appraisals, LP agreements, 8283, governing documents", "cannot accept a gift or determine equivalency", "extraction with page references", "low confidence or missing pages -> specialist", "manual review", "CNV-GRT-013; CNV-GRT-008"),
    ("fraud anomaly triage", "recommend (A1)", "score destination changes, login and instruction anomalies", "cannot release or permanently block; protective hold only under sponsor hold policy, time-bounded", "signal set and threshold version", "score above threshold -> restricted fraud queue and protective hold per CNV-PLT-007", "deterministic cooling-off and callback rules", "CNV-PLT-007; CNV-PLT-011"),
    ("reconciliation match suggestions", "recommend (A1)", "propose matches for non-exact items", "cannot auto-pass non-exact items; no silent write-offs", "proposed match with differences", "all non-exact items -> human; new sources at zero tolerance", "exact-match engine", "CNV-FIN-004"),
]
AIC_COLS = ["capability", "authority_level", "may_do", "limits_must_not", "evidence_requirements", "escalation_criteria", "failure_behavior", "basis"]


def aic_row(t):
    d = dict(zip(AIC_COLS[:5] + ["escalation_criteria", "deterministic_fallback", "basis"], t))
    return {"capability": d["capability"], "authority_level": d["authority_level"], "may_do": d["may_do"], "limits_must_not": d["limits_must_not"],
            "evidence_requirements": d["evidence_requirements"], "escalation_criteria": d["escalation_criteria"],
            "failure_behavior": "AI unavailable or wrong: deterministic path continues (CNV-AIO-001); work falls to human queue; " + d["deterministic_fallback"],
            "never": "invent financial records; bypass sponsor reserved authority; clear flags/holds; weaken or skip a control",
            "basis": d["basis"], "status": "proposed (no operational AI runtime exists in Echelon or Unbound; requirements only)"}


AI = [aic_row(t) for t in AIC]

# ------------------------------------------------------------------ PART 1 outcomes and responsibility matrix
OUTCOMES = [
    ("O01", "Accurate financial records", "sponsor, auditors, donors", "ledger agrees to bank/custodian; no unexplained breaks; audit without material adjustment", "recognition point; correction class; materiality", "bank/custodian feeds; four contribution dates; fee basis", "append-only ledger; server-side computation; daily external digest anchor", "post, correct in open period, close", "CNV-FIN-003/007/008/011; CNV-PLT-010; ICFR via SOC 1 (CNV-GOV-001)"),
    ("O02", "Timely, lawful grants", "donors, charities, sponsor", "grants paid within SLA; zero taxable distributions", "approve/decline/hold; rail choice", "recommendation, eligibility, sanctions, capacity", "board-delegated policy; SoD release; dispatch fencing", "intake, approve, reserve, release, pay", "IRC 4966/4967 via CNV-GRT-001; CNV-GOV-003; CNV-ARC-003"),
    ("O03", "Charity verification", "sponsor", "eligibility checked at approval and release with fresh sources", "eligible / Tier-2 / decline", "Pub 78, EO BMF, auto-revocation, CA registry", "fail safe when stale; AI flags never clear", "check, monitor, invalidate, review", "IRC 4966 (s170(b)(1)(A)); CNV-GRT-002/003/015"),
    ("O04", "Contribution processing", "donors, sponsor", "every gift recorded with four dates and acknowledged", "accept/return; complex gift acceptance", "ACH, check, DTC/ACATS, intermediary reports", "return handling; positive deposit reconciliation", "receive, match, post, acknowledge", "s170(f)(8)/(18) via activities.csv; CNV-FIN-003; CNV-GRT-013"),
    ("O05", "Customer service", "donors, advisors, charities", "questions prevented or answered correctly; complaints acknowledged in 2 business days", "escalate to human; complaint handling", "status projection; approved content", "no misstatement; no advice", "answer, escalate, resolve", "CNV-PLT-005; CNV-EXP-003; CNV-GRT-014"),
    ("O06", "Sponsor reporting", "sponsor management, board", "reports generated from authoritative records on time", "report content; narrative", "ledger, cases, controls", "IPE support", "generate, review, deliver", "CNV-GOV-001/008; CNV-FIN-009"),
    ("O07", "Regulatory compliance (tax, sanctions, communications)", "sponsor, regulators", "no prohibited transactions; reports filed on time", "match disposition; block/reject; Tier-2", "OFAC lists, IRS guidance, licences", "screen at onboarding, delta, release; fail closed", "screen, disposition, report", "31 CFR 501.603/604 via CNV-GRT-006; IRC 4967; CNV-PLT-001"),
    ("O08", "Reconciliation", "sponsor, auditor", "continuous; breaks resolved within sponsor-set days; monthly sign-off", "tolerances; unattributable-break publication choice", "feeds; ledger", "outside payment chain; independent attestation", "match, investigate, sign off", "CNV-FIN-004; CNV-GOV-003"),
    ("O09", "Investment and custody coordination", "sponsor, donors", "positions and NAV reconciled; allocation requests relayed", "NAV publication under delegation", "manager positions, valuations", "no advice; no custody", "ingest, reconcile, relay", "CNV-LEG-001; CNV-FIN-005/013"),
    ("O10", "Fraud prevention", "donors, sponsor", "no loss from takeover or redirection", "protective hold; investigation outcome", "login, destination, instruction anomalies", "callback; cooling-off; notify old channel", "detect, hold, investigate", "CNV-PLT-007/011; duty of care"),
    ("O11", "Security", "all", "no breach; ITGCs effective", "access grants; change approval", "access logs; change records", "two-approver changes; break-glass two-person", "provision, review, respond", "CNV-PLT-010; CNV-ARC-002; SOC 2 (CNV-GOV-001)"),
    ("O12", "Accessibility", "donors, advisors, staff", "WCAG 2.2 AA; accommodations without degraded service", "accommodation", "user needs", "accessibility non-removable", "design, test, accommodate", "CNV-EXP-001; CNV-GOV-006"),
    ("O13", "Business continuity", "sponsor", "service continues through outage, absence, peak", "invoke DR; suspension mode", "health, capacity", "roster coverage; surge plan before 1 Dec", "failover, surge, communicate", "CNV-SVC-002; CNV-GOV-004"),
    ("O14", "Customer acquisition", "servicer", "signed sponsors at cost-reflective tariff", "pursue/decline; price", "target list, pipeline", "concentration limit", "sell, contract", "CNV-ECO-004"),
    ("O15", "Sponsor onboarding and migration", "sponsor", "live with reconciled opening balances and activated gates", "configuration adoption; go-live", "predecessor data", "parallel run; activation gates", "map, configure, migrate, calibrate", "CNV-ECO-005; CNV-EXP-002"),
    ("O16", "Software maintenance", "all", "changes released safely; dependencies licensed", "release; materiality class", "changes, SBOM", "two approvers; signed builds", "build, review, release", "CNV-PLT-010; CNV-GOV-009"),
    ("O17", "Continuous improvement", "servicer, sponsors", "recurring problems removed at source", "which improvements", "case clusters, metrics", "versioned changes; justification per human step", "detect, propose, change", "CNV-GOV-006"),
    ("O18", "Audit and assurance (SOC 1/2, sponsor audits)", "sponsor auditors", "clean opinions; evidence on demand", "scope; reliance", "evidence store", "IPE; bridge letters", "prepare, support", "CNV-GOV-001/002; CNV-PLT-009"),
    ("O19", "Records retention and privacy", "sponsor, donors", "records kept 10 years where required; tenant isolation", "retention class; access", "records", "deny-by-default operator access", "retain, dispose, isolate", "CNV-PLT-004; CNV-ARC-002"),
    ("O20", "Succession, disputes and entitlements", "donors, families, sponsor", "correct successor; protected funds", "suspend; recognise successor", "death notice, documents", "protective suspension", "verify, suspend, transfer", "CNV-ENT-001/002; CNV-GRT-016"),
    ("O21", "Sponsor governance support (delegation)", "sponsor board", "delegation adopted, reported, renewed", "adopt/renew delegation", "quarterly report", "expiry <= 12 months", "prepare report, sample", "CNV-GRT-001; CNV-GOV-008"),
    ("O22", "Payment exceptions and unclaimed property", "charities, states", "voids and unknown outcomes resolved lawfully", "void disposition; escheat", "positive pay, traces", "no silent re-credit", "trace, decide, report", "CNV-PAY-003/004"),
    ("O23", "Policy configuration and change control", "sponsor", "policies versioned and adopted", "adopt change", "policy packs", "affirmative adoption; emergency path", "draft, adopt, activate", "CNV-GOV-005"),
    ("O24", "Third-party and vendor management", "sponsor, auditors", "vendor reports current; fallbacks exist", "accept vendor; fallback", "SOC reports, contracts", "integration register; bridge letters", "monitor, request, replace", "CNV-GOV-002; CNV-ECO-005"),
    ("O25", "Donor disclosures and communications compliance", "donors", "accurate tax content; consented messaging", "template classification", "templates, consent", "no individualized advice", "classify, send", "CNV-GRT-014; CNV-PLT-001"),
    ("O26", "Workforce capacity and coverage", "servicer, sponsor", "roster coverage by role and day incl. December double absence", "hire, contract, appoint backup", "workload, leave", "independence of roles", "forecast, roster, surge", "CNV-SVC-002; CNV-GOV-004"),
    ("O27", "Servicer's own finance and billing", "servicer", "sponsors billed per contract; company books closed", "invoice; collections", "metered events", "cost attribution reconciled to invoices", "bill, collect, close", "CNV-ECO-001"),
]
OUT_COLS = ["outcome_id", "outcome", "beneficiary", "success_measure", "decisions", "information", "controls", "actions", "basis"]

DS, AI_, HD, IR, CS, SA, EP = "deterministic_software", "ai_agent", "human_decision_maker", "independent_reviewer", "contracted_specialist", "sponsor_appointed_authority", "external_provider"
# (outcome_id, element_type, element, performer, authority, independence, evidence, escalation, failure, basis)
RM = [
    ("O01", "action", "post transactions and compute balances/fees server-side", DS, "A2 execute by rule", "n", "append-only entries, digest anchor", "invariant breach -> integrity hold", "fail closed; integrity hold never auto-releases", "CNV-PLT-010; CNV-PLT-007"),
    ("O01", "decision", "correction class and period", HD, "staff (controller approval for prior-period)", "y: approver != preparer", "correction record with relates_to_period", "material -> controller", "correction waits; no back-dating", "CNV-FIN-011"),
    ("O01", "decision", "recognition point and accounting treatment policy", SA, "sponsor CFO/board", "y", "effective-dated policy record", "auditor", "platform default applies", "CNV-FIN-007/008"),
    ("O01", "control", "ICFR evidence for user auditors", DS, "n/a", "n", "IPE-supported reports", "missing -> control exception", "manual procedures continue", "CNV-GOV-001"),
    ("O02", "information", "structured recommendation with purpose and attestations", DS, "n/a", "n", "recommendation record", "invalid -> donor correction", "rejected at entry", "CNV-AIO-001"),
    ("O02", "decision", "approve conforming grants under board delegation", DS, "delegated policy version under named delegate", "y: policy approved independently of authors", "policy version, inputs, outcome", "non-conforming -> exception queue", "without delegation: ApproveRecommended only", "IRC 4966/4967; CNV-GRT-001"),
    ("O02", "action", "prepare exception dossier", AI_, "A1 prepare", "n", "dossier with locked deterministic section", "unresolved trigger -> no batch", "human prepares from deterministic section", "CNV-AIO-002"),
    ("O02", "decision", "review dossier and recommend", HD, "staff A2 recommend", "y: not the decider", "review note", "doubt -> sponsor decider", "item stays Held", "CNV-GOV-010"),
    ("O02", "decision", "decide exception grants", SA, "reserved (A3+) by board resolution, one sponsor only", "y: exclusive to sponsor; not vendor staff", "signed decision with rationale", "sponsor board/committee", "Held; CoverageGap if no appointee within SLA", "SPD-ADV-001; CNV-GOV-004; IRC 4966(d)(3) managers"),
    ("O02", "control", "release payment batch", DS, "release gate counts as releaser only with auditor/board acceptance", "y: three distinct persons until accepted", "release log, fencing token", "gate failure -> human release", "three-distinct-person rule", "CNV-GOV-003; CNV-ARC-003"),
    ("O02", "action", "originate ACH/check/wire", EP, "sponsor is Originator; ODFI", "n", "bank files, positive pay", "returns -> case", "sponsor can pay via own bank channel", "NACHA via CNV-PAY-001/005"),
    ("O02", "control", "quarterly decision-quality sampling", IR, "attest only", "y: independent of preparer, releaser, policy author", "sample, findings", "material error -> increase n, notify board", "delegation not renewed", "CNV-GRT-011; CNV-GOV-008"),
    ("O03", "information", "status from IRS lists with posting dates", DS, "n/a", "n", "source, posting date, retrieval time", "stale -> block", "fail safe when stale", "CNV-GRT-003"),
    ("O03", "action", "continuous monitoring and event invalidation", DS, "A2", "n", "invalidation events", "adverse -> review case", "release blocked for affected recipient", "CNV-GRT-003"),
    ("O03", "action", "adverse-news triage", AI_, "A1 flag only", "n", "flag with quoted source", "flag -> compliance", "no flag cleared by AI", "CNV-AIO-001; CNV-GRT-004"),
    ("O03", "decision", "eligibility on mismatch/absence/group exemption", HD, "staff recommend; sponsor decides if exception", "y", "determination record", "-> sponsor decider", "grant held", "CNV-GRT-002/003"),
    ("O03", "decision", "equivalency determination / expenditure responsibility", CS, "qualified reviewer under sponsor reliance", "y: independent of donor", "ED/ER file", "-> sponsor decider", "route via intermediary or decline", "CNV-GRT-008; CNV-GRT-011"),
    ("O04", "action", "match and post contributions", DS, "A2", "n", "four dates, match evidence", "unmatched -> queue", "item queued, not posted", "CNV-FIN-003"),
    ("O04", "action", "read check images / transfer memos", AI_, "A1 suggest", "n", "extraction with image ref", "low confidence -> human", "human identification", "activities.csv ACT-A03"),
    ("O04", "action", "lockbox, custody of paper, DTC receipt", EP, "vendor contract", "n", "lockbox files, custodian feeds", "vendor SLA breach", "fallback provider", "CNV-PAY-007; CNV-FIN-013"),
    ("O04", "decision", "accept complex gift", SA, "reserved: gift acceptance policy", "y", "acceptance record, 8283 Part V", "board/committee", "gift declined", "CNV-GRT-013; Form 8283/8282"),
    ("O04", "action", "complex-asset diligence and liquidation", EP, "agent intermediary", "n", "intermediary report", "-> sponsor", "gift not credited", "CNV-GRT-013"),
    ("O04", "action", "issue s170(f)(8)/(18) acknowledgments", DS, "A2", "n", "acknowledgment with date", "correction -> alert", "manual issuance", "s170(f)(8)/(18) via activities.csv ACT-A20"),
    ("O05", "information", "status projection for every state combination", DS, "n/a", "n", "StatusProjection version", "unmapped state -> staff label", "generic status", "CNV-EXP-003"),
    ("O05", "action", "grounded answers", AI_, "A1 informational", "n", "answer with citations", "complaint/human request/low confidence -> human", "human queue", "CNV-AIO-001; CNV-GRT-014"),
    ("O05", "decision", "complaint handling and remedies", HD, "staff; sponsor for fund remedies", "y for complaints about own work", "complaint record, 2-day acknowledgment", "-> sponsor", "clock never pauses", "CNV-PLT-005; CNV-SVC-001"),
    ("O06", "action", "generate reports from ledger and cases", DS, "A2", "n", "IPE support", "mismatch -> block", "manual report", "CNV-GOV-001"),
    ("O06", "action", "draft narrative", AI_, "A1", "n", "labelled AI narrative", "figure mismatch -> block", "report without narrative", "CNV-AIO-002"),
    ("O06", "decision", "approve and deliver sponsor reports", HD, "controller", "y", "sign-off", "-> sponsor CFO", "delayed delivery with notice", "CNV-GOV-008"),
    ("O07", "action", "screen at onboarding, list delta and release", DS, "A2; fail closed", "n", "list version, fetch time", "match -> compliance", "block release when list stale", "31 CFR 501; CNV-GRT-006"),
    ("O07", "decision", "disposition of potential matches", HD, "compliance officer", "y: independent of grant preparer", "disposition with reasons", "true match -> sponsor officer", "never auto-closed", "CNV-GRT-006"),
    ("O07", "decision", "block/reject and OFAC report", SA, "sponsor officer files (servicer prepares)", "y", "501.603/604 report data within 10 business days", "counsel", "precautionary report default", "31 CFR 501.603/604 via CNV-GRT-006"),
    ("O07", "action", "regulatory change watch", AI_, "A1", "n", "source, effective date", "-> compliance owner", "manual watch", "CNV-GOV-005"),
    ("O07", "decision", "tax-content and legal interpretation", CS, "outside counsel", "y", "opinion memo", "-> sponsor", "content withheld", "CNV-GRT-014"),
    ("O08", "action", "continuous matching; exact matches auto-pass", DS, "A2", "n", "match log", "non-exact -> queue", "new source: zero tolerance", "CNV-FIN-004"),
    ("O08", "action", "suggest non-exact matches", AI_, "A1", "n", "proposal with differences", "all -> human", "human match", "CNV-FIN-004"),
    ("O08", "decision", "resolve breaks", HD, "reconciliation accountant (outside payment chain)", "y: no payment rights", "break resolution", "unattributable -> controller", "statements blocked for affected funds", "CNV-GOV-003; CNV-FIN-004"),
    ("O08", "control", "attest risk-stratified sample of auto-passed items", IR, "attest", "y", "sample workpapers", "error -> resample, controller", "sign-off withheld", "CNV-FIN-004"),
    ("O08", "decision", "monthly completeness sign-off; tolerance approval", HD, "controller", "y", "sign-off record", "-> sponsor CFO", "statements provisional/withheld per rule", "CNV-FIN-004"),
    ("O09", "action", "ingest positions/valuations; relay allocation choices", DS, "A2", "n", "raw feed + normalized", "unmatched -> queue", "relay paused", "CNV-LEG-001; CNV-FIN-013"),
    ("O09", "decision", "select manager, investment policy", SA, "sponsor board / investment committee", "y", "board minutes", "n/a", "n/a (servicer barred)", "CNV-LEG-001 (UPMIFA s5 interpretation)"),
    ("O09", "action", "investment management and custody", EP, "registered manager/custodian", "n", "statements", "-> sponsor", "n/a", "CNV-LEG-001"),
    ("O09", "decision", "publish out-of-tolerance NAV", HD, "per investment-committee delegation", "y", "NAV exception record", "-> committee", "NAV withheld", "CNV-FIN-005"),
    ("O10", "action", "anomaly triage", AI_, "A1", "n", "signals and threshold", "-> restricted fraud queue", "deterministic cooling-off/callback", "CNV-PLT-011"),
    ("O10", "action", "protective hold", DS, "sponsor-adopted hold policy, time-bounded", "n", "hold record actor/reason/expiry", "-> sponsor officer immediately", "converts to sponsor decision; sponsor can pay via own bank", "CNV-PLT-007"),
    ("O10", "decision", "investigate and conclude", HD, "staff (restricted routing)", "y", "investigation file", "-> sponsor, law enforcement", "hold remains", "CNV-SVC-001"),
    ("O11", "control", "two approvers on control-relevant change", HD, "engineers (not author)", "y", "PR approvals, signed build", "-> CTO/CISO", "change blocked", "CNV-PLT-010"),
    ("O11", "action", "access review and logging", DS, "A2", "n", "access logs", "anomaly -> CISO", "deny by default", "CNV-ARC-002"),
    ("O11", "control", "penetration test, vCISO review", CS, "contract", "y", "reports", "-> audit committee", "finding remediation", "CNV-GOV-003 (CISO access to audit committee)"),
    ("O12", "control", "WCAG 2.2 AA conformance testing", DS, "CI gate", "n", "test results", "fail -> release blocked", "release blocked", "CNV-EXP-001"),
    ("O12", "decision", "individual accommodation", HD, "staff", "n", "accommodation record", "-> manager", "alternative channel at no extra cost", "CNV-ECO-002; CNV-GOV-006"),
    ("O12", "control", "assistive-technology user testing", CS, "contract", "y", "audit report", "-> product owner", "remediation", "CNV-EXP-001"),
    ("O13", "decision", "invoke DR/suspension mode", HD, "incident commander (CTO)", "n", "incident record", "-> sponsors", "status-only channel; no unsafe promises", "CNV-SVC-002"),
    ("O13", "action", "surge activation before 1 December", HD, "ops manager/founder", "n", "December readiness gate record", "-> sponsors", "SLA floor breach notified", "CNV-SVC-002"),
    ("O13", "action", "pre-appointed surge reviewers", SA, "one sponsor each", "y", "appointment", "n/a", "backlog grows", "CNV-GOV-004"),
    ("O14", "decision", "pursue sponsor and price", HD, "founder", "n", "pipeline record", "-> board", "n/a", "CNV-ECO-004"),
    ("O14", "action", "prospect research and proposal drafting", AI_, "A1", "n", "drafts", "-> founder", "manual", "proposal"),
    ("O15", "action", "data mapping and validation", AI_, "A1", "n", "mapping diff", "unmapped -> analyst", "manual mapping", "CNV-EXP-002"),
    ("O15", "decision", "adopt configuration and activation gates", SA, "sponsor board/CFO", "y", "adoption records", "-> board", "pre-delegation operation", "CNV-ECO-005; CNV-GOV-005"),
    ("O15", "decision", "approve opening balances", HD, "controller", "y", "reconciliation report", "-> sponsor CFO", "go-live delayed", "CNV-EXP-002"),
    ("O16", "action", "build and test", AI_, "A1 prepare code", "n", "PR with provenance", "-> human approvers", "human authorship", "CNV-PLT-010"),
    ("O16", "decision", "approve and release", HD, "two engineers not author", "y", "approvals, release notice to sponsors", "material gate change -> sponsor acceptance", "revert to three-person rule for that sponsor", "CNV-PLT-010; CNV-GOV-003"),
    ("O17", "action", "recurring-problem detection", AI_, "A1", "n", "clusters", "-> owner", "periodic manual review", "CNV-GOV-006"),
    ("O17", "decision", "change process or human step", HD, "process owner; sponsor if policy", "n", "justification record", "-> sponsor", "step stays until reviewed (never auto-bypass)", "CNV-GOV-006"),
    ("O18", "control", "SOC 1 type 2 / SOC 2 examination", EP, "CPA firm", "y", "SOC reports", "-> sponsors' auditors", "bridge letter", "AT-C 320 via CNV-GOV-001"),
    ("O18", "action", "evidence assembly", AI_, "A1", "n", "IPE packs", "-> controller", "deterministic queries", "CNV-GOV-001"),
    ("O19", "action", "retention classes and disposal", DS, "A2", "n", "retention log", "legal hold -> counsel", "retain", "CNV-PLT-004"),
    ("O20", "decision", "recognise successor / dispute handling", SA, "sponsor (servicer prepares)", "y", "documents, decision", "-> counsel", "protective suspension", "CNV-ENT-001/002"),
    ("O20", "action", "verify documents", HD, "staff", "n", "verification record", "-> sponsor", "suspension continues", "CNV-ENT-001"),
    ("O21", "action", "generate quarterly board report and samples", DS, "A2", "n", "report with sampled reviews", "-> board", "delegation lapses", "CNV-GOV-008"),
    ("O21", "decision", "adopt/renew delegation", SA, "board or committee", "y", "resolution", "n/a", "recommend-only mode", "CNV-GRT-001; CNV-GOV-008"),
    ("O22", "decision", "void disposition / escheat", HD, "staff under state rule table; sponsor for re-credit", "y", "VoidDisposition record", "-> sponsor", "hold as payable", "CNV-PAY-003"),
    ("O22", "action", "bank traces for unknown outcomes", EP, "ODFI", "n", "trace response", "-> ops", "aging tier escalation", "CNV-PAY-004"),
    ("O23", "action", "draft policy-pack change and impact", AI_, "A1", "n", "diff, impact", "-> compliance", "no change", "CNV-GOV-005"),
    ("O23", "decision", "adopt material change", SA, "sponsor", "y", "adoption record", "deadline missed -> feature fails safe", "previous version", "CNV-GOV-008; CNV-GOV-005"),
    ("O24", "action", "vendor SOC gap monitoring", DS, "A2", "n", "gap computation", "-> request bridge letter", "manual tracking", "CNV-GOV-002"),
    ("O24", "decision", "accept vendor / fallback", HD, "CTO/controller", "n", "integration register", "-> sponsor", "activation not ready", "CNV-ECO-005"),
    ("O25", "action", "generate tax content from verified authority", DS, "A2 with owner/version", "n", "citations, effective dates", "-> counsel", "content withheld", "CNV-GRT-014"),
    ("O25", "control", "message classification before activation", HD, "compliance", "n", "template classification", "-> counsel", "template inactive", "CNV-PLT-001"),
    ("O26", "action", "forecast workload and roster coverage", DS, "A2", "n", "roster, forecast", "gap -> manager", "manual roster", "CNV-SVC-002; CNV-GOV-004"),
    ("O26", "decision", "hire/contract/appoint backup", HD, "founder/manager", "n", "staffing decision", "-> board", "coverage gap disclosed", "CNV-SVC-002"),
    ("O27", "action", "meter and bill", DS, "A2", "n", "metered events reconciled to invoices", "residual > tolerance -> controller", "manual invoice", "CNV-ECO-001"),
    ("O27", "action", "company bookkeeping and payroll", EP, "outsourced provider", "n", "books", "-> controller", "fallback provider", "prior cost register"),
]
RM_COLS = ["outcome", "element_type", "element", "performer_type", "authority", "independence_needed", "evidence_produced", "escalation", "failure_behavior", "basis"]
OUT_NAME = {o[0]: o[1] for o in OUTCOMES}


def rm_row(t):
    d = dict(zip(["outcome_id"] + RM_COLS[1:], t))
    return {"outcome_id": d["outcome_id"], "outcome": OUT_NAME[d["outcome_id"]], **{k: d[k] for k in RM_COLS[1:]},
            "human_required": "y" if d["performer_type"] in (HD, IR, CS, SA) else "n"}


RMX = [rm_row(t) for t in RM]


def out_row(o):
    d = dict(zip(OUT_COLS, o))
    perf = sorted({r["performer_type"] for r in RMX if r["outcome_id"] == d["outcome_id"]})
    human = [r["element"] for r in RMX if r["outcome_id"] == d["outcome_id"] and r["human_required"] == "y"]
    return {**d, "performer_types": ";".join(perf), "human_elements": "; ".join(human)}


OC = [out_row(o) for o in OUTCOMES]


# ------------------------------------------------------------------ writes
def write_csv(name, rows, cols=None):
    cols = cols or list(rows[0].keys())
    with open(f"{OUT}/{name}", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        [w.writerow(r) for r in rows]
    return name, len(rows)


WT_COLS = ["row_type", "name", "share_or_frequency", "frequency_unit", "minutes_before", "minutes_after", "contribution_min_per_mix_account_year", "human_irreducible_min",
           "driver", "fte_needed", "fte_available", "backlog_case_days", "legal_deadlines_at_risk", "notes", "label"]
STAFF_ROWS = [dict(zip(STAFF_COLS, s)) for s in STAFF]

WRITTEN = [
    write_csv("outcomes.csv", OC),
    write_csv("responsibility-matrix.csv", RMX),
    write_csv("work-elimination.csv", WE),
    write_csv("handling-targets.csv", HT),
    write_csv("workload-tails.csv", WT, WT_COLS),
    write_csv("staffing-capacity.csv", STAFF_ROWS),
    write_csv("overhead.csv", OV),
    write_csv("ai-capabilities.csv", AI),
]

METRICS = {
    "typical_base": TYP_BASE, "typical_after": TYP_AFTER, "typical_elim": TYP_ELIM, "typical_trans": TYP_TRANS, "prior_elim_typical": PRIOR_ELIM_TYP,
    "ratio_typical": R_TYP, "mix_base": MIX_BASE, "mix_after": MIX_AFTER, "mix_trans": MIX_TRANS,
    "arch_after": ARCH_AFTER, "arch_after_high": ARCH_AFTER_HIGH, "s_base_yr": S_BASE_YR, "s_after_yr": S_AFTER_YR,
    "floor_servicer": FLOOR_SERVICER, "floor_legal": FLOOR_LEGAL, "floor_sponsor": FLOOR_SPONSOR, "mix_grants": MIX_GRANTS,
    "pre_deleg_add": PRE_DELEG_ADD, "queue_min_fte_yr": QUEUE_MIN_PER_FTE_YR, "usd_per_min": USD_PER_MIN,
    "be_prior": be_at(MIX_BASE), "be_after": be_at(MIX_AFTER), "be_zero": be_at(0.0), "be_floor": be_at(FLOOR_SERVICER), "be_75": be_at(75),
    "peaks": [(p["name"], p["minutes_before"], p["minutes_after"], p["fte_needed"], p["fte_available"], p["backlog_case_days"]) for p in PEAKS],
    "base_fte": BASE_FTE, "staff_grid": STAFF_GRID, "ovh_conv": OVH_CONV, "ovh_res": OVH_RES, "sample_n": SAMPLE_N_95_5,
    "written": WRITTEN, "transfers": [(r["activity_id"], r["minutes_transferred"], r["transferred_to"]) for r in WE if r["minutes_transferred"]],
}
with open(f"{OUT}/_metrics.json", "w") as f:
    json.dump(METRICS, f, indent=1, default=str)
print(json.dumps(METRICS, indent=1, default=str))
