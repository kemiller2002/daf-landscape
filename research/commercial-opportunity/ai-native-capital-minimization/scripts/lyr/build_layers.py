"""Layer cost structures (LYR part 1). Functional style: data tables -> derived tables -> CSV + summary JSON.

Reference scenario R: 5 sponsors, 10,000 accounts, $1.5B average AUA ($150k), AI-native steady state, 20 bps,
Model B servicing organisation of the previous study. [M] values come from running the previous study's F# model
(work/fsx/ref.fsx). Every other value carries its own label.
"""
import csv
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
SE = "daf-landscape/data/commercial-opportunity/servicing-economics"
UNB = "unbound/requirements"

# (line_id, layer, line_item, cost_type, S(lo,base,hi), I(lo,base,hi), key, cash_or_economic, label, source, notes)
A = "A Echelon Foundry"
B = "B Unbound"
C = "C DAF servicing"
SH = "Shared (corporate)"
T = "Transfer (eliminates on consolidation)"
R = "Revenue"

lines = [
    # ---------------- Layer A
    ("A01", A, "Principal architect/maintainer of the 26 Echelon component repos and governance tooling (Praxis, Ordo, Dokimos, Conditor, registry)", "fixed people",
     (190356, 222482, 273473), (57107, 111241, 191431), "Praxis work-item telemetry hours by repo; the other ~0.5 FTE is Unbound technical-lead work charged to B02",
     "economic (founder opportunity cost; cash may be $0)", "S/A",
     f"{SE}/cost-register.csv CST-R02; measured: one human author plus AI agents across all component repos (git log, 2026-11-25)",
     "Standalone = 1.0 FTE at CTO market rate. Incremental = Echelon-only time (0.3/0.5/0.7 FTE) [A] once the same person also leads Unbound."),
    ("A02", A, "AI agent compute for component development (coding agents, reviews, evaluation runs)", "fixed",
     (6000, 24000, 60000), (3000, 12000, 36000), "agent tokens/work items by repo (Praxis telemetry)", "cash", "A",
     "no invoice observed; [A] analyst placeholder",
     "Heavy agentic use: 9,045 commits in 26 repos since 2025-07-07, majority with Claude co-author trailers [M]. Price not observed."),
    ("A03", A, "Second maintainer (bus-factor cover) required before any regulated commercial reliance; precondition for escrow/fork right", "fixed people",
     (0, 0, 94479), (79181, 188958, 219876), "100% caused by B production reliance (dependency-caused cost)", "cash", "S/A",
     f"{SE}/cost-register.csv CST-R03; {UNB}/AUTHORITATIVE-BASELINE.md CNV-GOV-009; {SE}/echelon-capabilities.csv ECH-01",
     "Standalone research Echelon does not need it; a DAF platform relying on single-maintainer code does."),
    ("A04", A, "Development infrastructure (GitHub org, CI minutes, package registry, docs hosting)", "fixed",
     (1500, 6000, 15000), (500, 2000, 6000), "CI minutes per repo", "cash", "A", f"{SE}/cost-register.csv CST-S03 (seat range)", ""),
    ("A05", A, "Component security and supply-chain assurance (independent review of AI-authored code, SBOM, signed releases, vulnerability response)", "fixed",
     (0, 5000, 15000), (10000, 25000, 60000), "components present in B's production SBOM", "cash", "A",
     f"{SE}/echelon-capabilities.csv ECH-11 (placeholder 0-40k)", "Cost is caused by production reliance, so it follows B."),
    ("A06", A, "Hosting/monitoring of shared Echelon services (registry, documentation sites)", "fixed",
     (0, 1000, 10000), (0, 0, 5000), "requests by consumer", "cash", "A", f"{SE}/echelon-capabilities.csv ECH-21 (static sites only)", ""),
    ("A07", A, "Entity administration for Echelon (books, tax, filings, bank)", "fixed",
     (8000, 20000, 50000), (0, 2000, 8000), "entity count; incremental shown for a single-entity group (separate-entity uplift in entity-options.csv)", "cash", "D",
     f"{SE}/cost-register.csv CST-C02, CST-C10, CST-G01, CST-G02", ""),
    ("A08", A, "Commercial licence programme: licence drafting, contributor/AI-provenance IP review, escrow agent (one-off annualised over 3 years + escrow fee)", "fixed",
     (7000, 25000, 60000), (7000, 25000, 60000), "100% to licensees (B is the first)", "cash", "A",
     "/home/user/echelon-components/forma/README.md:162-164 ('Commercial licensing information is forthcoming'); CNV-GOV-009", ""),
    ("A09", A, "Licensor insurance (technology E&O, D&O) once components are licensed commercially", "fixed",
     (0, 0, 20000), (15000, 35000, 70000), "100% to licensees", "cash", "D", f"{SE}/cost-register.csv CST-I03, CST-I04", ""),
    # ---------------- Layer B
    ("B01", B, "DAF platform build amortised over 5 years (ledger, payment gate, identity, tenancy, render, integrations, 140 screens)", "one-off annualised",
     (600000, 1000000, 3000000), (300000, 920000, 3000000), "direct to B; recovered from C and licensees by licence charge", "cash (timing: up-front capital)", "S/D",
     f"{UNB}/discovery/2026-11-24-simplification-economics/model/parameters.json build_capex 5,000,000 (3-15M); {SE}/echelon-capabilities.csv ECH-08; research report 03 ECH-4",
     "Incremental given Echelon: base -8% (S0 reuse 0-16%), low = $3M x 0.5 (S1 2x throughput, unmeasured), high = no saving. Narrow servicing-only scope ($0.72-1.8M, previous study) is a scope choice, not an Echelon effect."),
    ("B02", B, "Unbound accountable technical lead (architecture, security, AI controls, release approval)", "fixed people",
     (190356, 222482, 273473), (190356, 222482, 273473), "direct", "economic (cash lower if founder)", "S",
     f"{SE}/cost-register.csv CST-R02", "If the Echelon principal fills half of this role the group still needs 1.5 senior technical FTE (A01 + B02)."),
    ("B03", B, "Platform engineers (maintenance, on-call, feature change, regulatory change; excludes per-sponsor integration upkeep)", "step-fixed people",
     (158361, 566874, 1099380), (158361, 521524, 1099380), "direct", "cash", "S/A",
     f"{SE}/cost-register.csv CST-R03; research report 03 ECH-4 (conventional 4-10 FTE; S1 needs measured 1.5-2x)",
     "Base 3 engineers [A]; the previous Model B carried 1, which report 03 calls a hidden assumption. Low 1 engineer requires measured >=2x agent throughput."),
    ("B04", B, "Per-sponsor integration upkeep engineer (1 per 8 live sponsors beyond 4)", "step-fixed people",
     (188958, 188958, 188958), (188958, 188958, 188958), "live sponsor connections (bank, custodian feeds)", "cash", "M",
     "previous F# model Parameters.fs:155-157 step rule, run at R", ""),
    ("B05", B, "Hosting, database, DR and monitoring (production + non-production)", "fixed",
     (33053, 59731, 250000), (33053, 59731, 250000), "metered compute/storage by tenant (CNV-ECO-001)", "cash", "S/D",
     f"report 03 Model B categories cloud+database+dr-bcp; high = Unbound parameters infra_base 250,000", "No Echelon component reduces it (ECH-09, ECH-13, ECH-21)."),
    ("B06", B, "Per-sponsor sandbox and bank/custodian connection upkeep ($12k per sponsor-year)", "per sponsor",
     (30000, 60000, 120000), (30000, 60000, 120000), "live sponsors", "cash", "M/A", "previous F# model Parameters.fs annualSponsorCostBase 12,000 x 5", ""),
    ("B07", B, "Platform assurance and security: SOC 2 Type 2, penetration test, vCISO, technology E&O", "fixed",
     (59000, 128000, 251000), (49000, 128000, 251000), "direct (SOC 2 boundary = platform)", "cash", "S/D",
     f"{SE}/cost-register.csv CST-C11, C14, C03, I03", "Incremental low: Praxis change records accepted as ITGC evidence (ECH-12, unverified)."),
    ("B08", B, "Platform data subscriptions and AI fixed cost (sanctions/PEP, identity plan, charity APIs, evaluation suites)", "fixed",
     (11750, 25750, 73900), (11750, 25750, 73900), "screening calls by tenant", "cash", "S/D",
     f"{SE}/cost-register.csv CST-D03, D05, ID1, T14", ""),
    ("B10", B, "Software sales and implementation for external licensees", "fixed",
     (100000, 250000, 500000), (0, 0, 250000), "external licensees only", "cash", "S/A",
     f"{SE}/assumptions-register.csv A-ADV-004", "Zero at R: the servicer is a captive customer. Standalone Unbound must sell."),
    # ---------------- Layer C
    ("C01", C, "Sponsor relationships, acquisition and governance lead (founder/CEO)", "fixed people",
     (151768, 200142, 267264), (151768, 200142, 267264), "direct", "economic (cash $116,255 in founder mode)", "S",
     f"{SE}/cost-register.csv CST-R01; staffing-models.csv Model A cash", ""),
    ("C02", C, "Controller / head of financial operations (reconciliation sign-off, release review, close)", "fixed people",
     (146796, 183365, 213679), (146796, 183365, 213679), "direct", "cash", "S", f"{SE}/cost-register.csv CST-R06", ""),
    ("C03", C, "Core grant and client operations specialist", "fixed people",
     (76798, 99478, 125968), (76798, 99478, 125968), "direct", "cash", "S", f"{SE}/cost-register.csv CST-R09", ""),
    ("C04", C, "Added operations staff for account and sponsor workload (5 FTE at R)", "variable people",
     (198956, 497390, 1790604), (198956, 497390, 1790604), "minutes per account-year and per sponsor", "cash", "M",
     "previous F# model evaluate modelB AiNative at R; low/high = minutes x0.35 / x3.33", "Includes the model's minimum second operations person for dual control."),
    ("C05", C, "December peak hours above monthly capacity", "variable",
     (17738, 68704, 233198), (17738, 68704, 233198), "December minutes", "cash", "M", "previous F# model peakCost at R", ""),
    ("C06", C, "Step-fixed servicing roles at R: operations manager, implementation analyst, fund accountant", "step-fixed people",
     (238102, 387912, 687532), (238102, 387912, 687532), "added ops FTE, sponsors, accounts", "cash", "M",
     "previous F# model Parameters.fs:153-160 at R (integration engineer moved to B04)", ""),
    ("C07", C, "Servicing external variable cost (data, identity, per-account cloud/AI, other; payment rails passed through)", "variable",
     (54514, 72685, 109027), (54514, 72685, 109027), "accounts, grants", "cash", "M", "previous F# model ExternalVariableCost at R (vendor x0.75/x1.5)", ""),
    ("C08", C, "Servicing direct non-personnel: SOC 1 Type 2, crime insurance, compliance consultant, sales, marketing, bank treasury, helpdesk", "fixed",
     (57300, 143800, 361000), (57300, 143800, 361000), "direct (SOC 1 boundary = servicing processes + platform ITGCs)", "cash", "S/D",
     f"{SE}/cost-register.csv CST-C12, I05, C04, SM1, SM2, PY8, S07", ""),
    ("C09", C, "Sales and customer acquisition beyond the founder", "fixed",
     (100000, 250000, 500000), (100000, 250000, 500000), "new sponsors", "cash", "S/A", f"{SE}/assumptions-register.csv A-ADV-004", ""),
    ("C10", C, "Sponsor onboarding and migration ($105k per sponsor, $35-325k) amortised over 5 years, 5 sponsors", "one-off annualised",
     (35000, 105000, 325000), (35000, 105000, 325000), "per sponsor", "cash", "S/D", "previous F# model Parameters.fs:118-121 onboardingBase", ""),
    ("C11", C, "Servicing-specific platform features (administrator principal, federated queue, staff workbench, SOC 1 servicing controls), one-off $150k/300k/600k over 5 years", "one-off annualised",
     (30000, 60000, 120000), (30000, 60000, 120000), "direct to C (built by B, charged at cost)", "cash", "A",
     f"{UNB}/convergence/2026-11-24-master/data/convergence-clauses.jsonl CNV-TEN-001", ""),
    ("C12", C, "Platform capability a standalone servicer must buy or build (licensed incumbent software $32-129 per DAF-year, or the previous study's in-house platform with a narrow build)", "standalone only",
     (320000, 1017879, 1290000), (0, 0, 0), "n/a when B exists", "cash", "S/D",
     f"{UNB}/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md §3a (iPhi $32-129/DAF-yr); report 03 Model B platform lines",
     "Base = CTO 222,482 + engineer 188,958 + platform non-personnel 213,481 + integration engineer 188,958 + sponsor upkeep 60,000 + $0.72M build / 5."),
    ("C13", C, "Handling penalty if the platform does not support the redesign (AI-enhanced or conventional handling instead of AI-native)", "standalone only",
     (0, 943516, 2700995), (0, 0, 0), "n/a when B delivers the redesign", "cash", "M",
     "previous F# model at R: AI-enhanced 3,860,452 and conventional 5,617,931 vs AI-native 2,916,936",
     "Value of B to C is contingent on unmeasured levers (Unbound EV-02; CNV-ECO-003)."),
    # ---------------- Shared corporate
    ("S01", SH, "Audit of own financial statements, fractional CFO, bookkeeping, tax returns, accounting software", "fixed",
     (43500, 80000, 152000), (43500, 80000, 152000), "A 5% / B 25% / C 70% (transactions and entity complexity)", "cash", "S/D",
     f"{SE}/cost-register.csv CST-C09, C01, C02, C10, S06", ""),
    ("S02", SH, "Corporate insurance: cyber $5M, D&O, EPLI, general liability", "fixed",
     (23000, 47000, 96000), (23000, 47000, 96000), "A 5% / B 35% / C 60% (records held, payments exposure, headcount)", "cash", "S/D",
     f"{SE}/cost-register.csv CST-I02, I04, I06, I07", ""),
    ("S03", SH, "Outside counsel (nonprofit/tax-exempt, financial services, IP)", "fixed",
     (30000, 45000, 80000), (30000, 45000, 80000), "A 15% / B 25% / C 60% (matter coding)", "cash", "S", f"{SE}/cost-register.csv CST-C06", ""),
    ("S04", SH, "Per-FTE overhead: equipment, stipend, training, PEO, recruiting/turnover, security tooling, SaaS seats, travel", "fixed per FTE",
     (26892, 64067, 145132), (26892, 64067, 145132), "headcount: A 1.5 / B 5 / C 11 FTE at R", "cash", "D",
     "report 03 Model B categories personnel (ex December temps), software, travel", ""),
    ("S05", SH, "Compliance automation platform, incident-response retainer, corporate G&A", "fixed",
     (9000, 37700, 100600), (9000, 37700, 100600), "A 10% / B 45% / C 45% (controls in scope)", "cash", "S/D", f"{SE}/cost-register.csv CST-C15, C16, G01-G03", ""),
    ("S06", SH, "Contingency on cash opex (7.5%; 5-10%)", "fixed",
     (60212, 115814, 231238), (60212, 115814, 231238), "pro rata to each layer's direct cost", "cash", "M/A", "previous F# model modelB contingency", ""),
]

shares = {
    "S01": {"A": .05, "B": .25, "C": .70},
    "S02": {"A": .05, "B": .35, "C": .60},
    "S03": {"A": .15, "B": .25, "C": .60},
    "S04": {"A": 1.5 / 17.5, "B": 5 / 17.5, "C": 11 / 17.5},
    "S05": {"A": .10, "B": .45, "C": .45},
}
# share of each shared line a standalone entity would still bear in full (its own corporate floor) [A]
standalone_floor = {
    "A": {"S01": 0.0, "S02": 0.0, "S03": 0.0, "S04": "own", "S05": 0.0},  # A07/A09 already carry A's entity floor
    "B": {"S01": .7, "S02": .8, "S03": .6, "S04": "own", "S05": .8},
    "C": {"S01": .9, "S02": .9, "S03": .8, "S04": "own", "S05": .8},
}

IDX = {"lo": 0, "base": 1, "hi": 2}
layer_code = {A: "A", B: "B", C: "C"}


def direct(layer, col, case):
    pos = 4 if col == "S" else 5
    return sum(l[pos][IDX[case]] for l in lines if l[1] == layer)


def shared_alloc(code, case, mode):
    """Allocated (mode='alloc') or standalone-floor (mode='standalone') shared cost for a layer, excl. contingency."""
    def one(l):
        sid = l[0]
        v = l[5][IDX[case]]
        if mode == "alloc":
            return v * shares[sid][code]
        f = standalone_floor[code][sid]
        return v * shares[sid][code] if f == "own" else v * max(f, shares[sid][code])
    return sum(one(l) for l in lines if l[1] == SH and l[0] != "S06")


CONT = 0.075


def summary(case):
    dI = {code: direct(name, "I", case) for name, code in layer_code.items()}
    dS = {code: direct(name, "S", case) for name, code in layer_code.items()}
    sh_total = sum(l[5][IDX[case]] for l in lines if l[1] == SH and l[0] != "S06")
    cont_total = [l for l in lines if l[0] == "S06"][0][5][IDX[case]]
    tot_direct = sum(dI.values())
    alloc = {c: dI[c] + shared_alloc(c, case, "alloc") + cont_total * dI[c] / tot_direct for c in dI}
    standalone = {c: (dS[c] + shared_alloc(c, case, "standalone")) * (1 + CONT) for c in dS}
    group = sum(dI.values()) + sh_total + cont_total
    return {"direct_incremental": dI, "direct_standalone": dS, "shared_total": sh_total, "contingency": cont_total,
            "fully_allocated": alloc, "standalone_total": standalone, "group_total": group,
            "check_alloc_equals_group": round(sum(alloc.values()) - group, 2)}


cases = {c: summary(c) for c in IDX}

# Incremental answers. Q1: servicing given Unbound exists = C direct incremental + C's causal share of shared + contingency share.
def q1(case):
    s = cases[case]
    return s["fully_allocated"]["C"]

# Q2: Unbound given Echelon exists = B direct incremental + B's share of shared + contingency share.
def q2(case):
    return cases[case]["fully_allocated"]["B"]

# Echelon cost caused by B (dependency-caused lines) and cost-plus licence charge.
caused_by_B = ["A03", "A05", "A08", "A09"]
def a_caused(case):
    return sum(l[5][IDX[case]] for l in lines if l[0] in caused_by_B)
def a_running(case):
    return sum(l[5][IDX[case]] for l in lines if l[1] == A and l[0] not in caused_by_B)
usage_share = {"lo": .2, "base": .4, "hi": .8}
markup = {"lo": .05, "base": .08, "hi": .10}
def cost_plus_echelon(case):
    return (a_caused(case) + usage_share[case] * a_running(case)) * (1 + markup[case])

# Unbound -> servicing charge: cost-plus = B fully allocated + Echelon licence charge, at R (captive customer, 10,000 funds)
def cost_plus_unbound(case):
    return (cases[case]["fully_allocated"]["B"] + cost_plus_echelon(case)) * (1 + markup[case])
market_unbound = {"lo": 49 * 10000, "base": 91 * 10000, "hi": 229 * 10000}  # Unbound 05 §1 licence $/fund at 250k/100k/25k platform funds
market_ipHi = {"lo": 32 * 10000, "base": 0, "hi": 129 * 10000}

transfer_rows = [
    ("T01", T, "Echelon -> Unbound commercial component licence, cost-plus (B-caused Echelon cost + usage share 20/40/80% of Echelon running cost, markup 5/8/10%)", "transfer-charge",
     tuple(round(cost_plus_echelon(c)) for c in ("lo", "base", "hi")), tuple(round(cost_plus_echelon(c)) for c in ("lo", "base", "hi")),
     "licence agreement; recorded as cost in B, revenue in A", "cash between entities; zero at group level", "D",
     "26 U.S.C. §482 (commensurate-with-income for licences of intangibles); 26 CFR 1.482-9(b) services cost method limits",
     "No market price exists: Echelon commercial terms 'forthcoming'. A licence of core intangibles is unlikely to qualify for the no-markup services cost method [research-level reading, not advice]."),
    ("T02", T, "Unbound -> servicing platform charge, cost-plus (B fully allocated + T01, markup 5/8/10%)", "transfer-charge",
     tuple(round(cost_plus_unbound(c)) for c in ("lo", "base", "hi")), tuple(round(cost_plus_unbound(c)) for c in ("lo", "base", "hi")),
     "per fund-year or per sponsor; recorded as cost in C, revenue in B", "cash between entities; zero at group level", "D",
     "this file B lines; T01", "At R the servicer is the only customer, so cost-plus loads 100% of B onto C."),
    ("T03", T, "Unbound -> servicing platform charge, market-based (Unbound's own licence $49/$91/$229 per fund-year x 10,000 funds)", "transfer-charge",
     tuple(market_unbound[c] for c in ("lo", "base", "hi")), tuple(market_unbound[c] for c in ("lo", "base", "hi")),
     "per fund-year", "cash between entities; zero at group level", "S/D",
     f"{UNB}/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md §1 (licence at 250k/100k/25k platform funds)",
     "Observed incumbent software band $32-129 per DAF-year (Unbound 05 §3a) is the external comparable; $229 is outside it."),
    ("R01", R, "Servicing fee revenue at R (20 bps on $1.5B)", "external revenue",
     (2100000, 3000000, 3000000), (2100000, 3000000, 3000000), "sponsors", "cash", "M", "previous F# model revenue at R; low = market -30%", ""),
    ("R02", R, "External Unbound licence revenue (scenario: 0 at R; high = 25,000 external funds at $91)", "external revenue",
     (0, 0, 2275000), (0, 0, 2275000), "external licensees", "cash", "D", f"{UNB}/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md §1", "Requires B10 sales cost and SOC 2 for licensees."),
    ("R03", R, "External Echelon commercial licence revenue", "external revenue",
     (0, 0, 0), (0, 0, 0), "external licensees", "cash", "A", "/home/user/echelon-components/forma/README.md:162-164", "No commercial terms, price or licensee observed."),
]

header = ["line_item", "layer", "cost_type", "standalone_low", "standalone_base", "standalone_high", "incremental_low",
          "incremental_base", "incremental_high", "allocation_key", "cash_or_economic", "source", "line_id", "label", "notes"]
rows = [[f"{l[0]} {l[2]}", l[1], l[3], *l[4], *l[5], l[6], l[7], l[9], l[0], l[8], l[10]] for l in lines + transfer_rows]
with open(OUT / "layer-costs.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    w.writerows(rows)

# cash vs economic: founder roles A01 (cash 0 assumed), C01 (cash 116,255), B02 (cash at market unless founder)
def cash_view(case):
    s = cases[case]
    a01 = [l for l in lines if l[0] == "A01"][0][5][IDX[case]]
    c01 = [l for l in lines if l[0] == "C01"][0][5][IDX[case]]
    return {"group_cash": s["group_total"] - a01 - (c01 - 116255), "founder_opportunity_cost": a01 + (c01 - 116255)}

summary_out = {
    "cases": cases,
    "q1_servicing_given_unbound": {c: q1(c) for c in IDX},
    "q2_unbound_given_echelon": {c: q2(c) for c in IDX},
    "echelon_caused_by_B": {c: a_caused(c) for c in IDX},
    "echelon_running": {c: a_running(c) for c in IDX},
    "T01_cost_plus_echelon": {c: cost_plus_echelon(c) for c in IDX},
    "T02_cost_plus_unbound": {c: cost_plus_unbound(c) for c in IDX},
    "T03_market_unbound": market_unbound,
    "cash_view": {c: cash_view(c) for c in IDX},
    "model_R_total": 2916936, "model_R_revenue": 3000000,
}
(OUT / "work" / "layer-summary.json").write_text(json.dumps(summary_out, indent=1))
print(json.dumps({k: v for k, v in summary_out.items() if k != "cases"}, indent=1))
for c in IDX:
    s = cases[c]
    print(c, {k: (round(v) if isinstance(v, (int, float)) else {kk: round(vv) for kk, vv in v.items()}) for k, v in s.items()})
