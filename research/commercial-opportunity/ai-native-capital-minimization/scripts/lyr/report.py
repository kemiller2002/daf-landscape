"""report.jsonl, evidence.jsonl, assumptions.jsonl for LYR. Reads work/layer-summary.json (from build_layers.py)."""
import csv
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
S = json.loads((OUT / "work" / "layer-summary.json").read_text())
C = S["cases"]
m = lambda v: f"${v/1e6:.2f}M"
k = lambda v: ("-" if v < 0 else "") + f"${abs(v)/1e3:,.0f}k"
fa = lambda case, L: C[case]["fully_allocated"][L]
di = lambda case, L: C[case]["direct_incremental"][L]
st = lambda case, L: C[case]["standalone_total"][L]
grp = lambda case: C[case]["group_total"]
rng = lambda f: f"{m(f('base'))} ({m(f('lo'))}-{m(f('hi'))})"

ech_saving = {"lo": (600000 - 300000) + (59000 - 49000), "base": (1000000 - 920000) + (566874 - 521524), "hi": 0}
net_ech = {c: ech_saving[c] - S["T01_cost_plus_echelon"][c] for c in ech_saving}
funds_needed = (fa("base", "B") + S["T01_cost_plus_echelon"]["base"]) / 91
funds_needed_sales = (fa("base", "B") + S["T01_cost_plus_echelon"]["base"] + 250000) / 91

count = lambda f: sum(1 for _ in open(OUT / f)) - 1

sections = []
add = lambda title, md: sections.append({"section": title, "markdown": md.strip()})

add("LYR summary: three-layer economics, assumptions, requirements and the cost of being wrong", f"""
**Group LYR, 2026-11-25. Status: theoretical research; same-model reasoning, not independent validation. No legal or tax advice.**

**Reference scenario R** (used throughout): 5 sponsors, 10,000 accounts, $1.5B average assets ($150k balance), AI-native steady state, 20 bps = **$3.00M revenue**. The previous study's F# model, re-run here, gives a servicing operating cost of **$2,916,936** at R (profit $83,064) [M].

| Question | Answer (base, low-high) |
|---|---|
| Incremental cost of a servicing operation if Unbound exists | **{rng(lambda c: S['q1_servicing_given_unbound'][c])}/yr** fully allocated (direct + causal share of corporate cost) |
| Incremental cost of Unbound if Echelon exists | **{rng(lambda c: S['q2_unbound_given_echelon'][c])}/yr** (servicer is the only customer) |
| Echelon cost caused by Unbound's commercial reliance | {rng(lambda c: S['echelon_caused_by_B'][c])}/yr (second maintainer, component security, licence programme, licensor insurance) |
| Echelon's verified saving to Unbound | {k(ech_saving['base'])} ({k(ech_saving['hi'])}-{k(ech_saving['lo'])})/yr; **net of the cost-plus licence charge: {k(net_ech['base'])} base**, positive only in the low case ({k(net_ech['lo'])}) which needs measured >=2x agent throughput |
| Three-layer group cost at R | **{rng(grp)}** vs $3.00M revenue (base loss {m(grp('base')-3e6)}) |
| Group break-even at 20 bps (5 sponsors, captive platform) | **$2.3-2.8B** base by balance ($500k-$150k); $1.5-1.9B low; $4.3-5.1B high [M]. Previous study: $1.1-1.5B operating, $1.8-2.3B fully loaded |
| Founder opportunity cost inside the base | {k(S['cash_view']['base']['founder_opportunity_cost'])}/yr (economic, not cash) |

**Five most consequential findings**
1. **The servicing layer alone works at R; the stack does not.** Servicing's incremental cost ({m(S['q1_servicing_given_unbound']['base'])}) leaves ~{m(3e6-S['q1_servicing_given_unbound']['base'])} toward a platform and foundry whose fully allocated cost is {m(fa('base','B')+fa('base','A'))}. A captive platform needs ~{funds_needed:,.0f} funds at Unbound's $91/fund to cover its cost (~{funds_needed_sales:,.0f} with licence sales cost), i.e. ~19-21k external funds beyond the servicer's 10k.
2. **Shared Echelon resources cost more than they save on current evidence.** Production reliance on single-maintainer, PolyForm-NC, largely agent-authored components creates ~$0.27M/yr of Echelon cost (base) against ~$0.13M/yr of verified reuse saving. The sign flips only if agent-assisted throughput is measured at >=2x on the DAF codebase.
3. **The value of Unbound to servicing is the redesign, not the software.** Without a platform that supports board-delegated straight-through handling, the same servicer costs +$0.94M/yr (AI-enhanced) to +$2.70M/yr (conventional) at R [M]. That value rests on unmeasured levers (Unbound EV-02) and on sponsor boards and auditors accepting deterministic release.
4. **Most conventional assumptions are not the binding constraint.** Of 52 assumptions registered, 17 have a replacement judged better (mostly small: December deferral, EFT default, lazy renewal, generated evidence), 32 are unproven and 2 are worse. Legal obligations, independent assurance and SoD remain; the large swings are platform build/engineering staffing, delegation and measured minutes.
5. **Stage the investment.** A gate sequence (buyer + licence + counsel + auditor approach; then design partner + instrumented shadow replay + engineering spike; then build) lets the owner stop at ~$0.15M or ~$0.75M instead of the $2-3M+ sunk at a failed go-live. Every failure in the catalogue except security incidents and market falls has a detection point before build spend.

**Does a fundamentally different company emerge?** Not at R on present evidence. The AI-native servicing layer is materially cheaper than a conventional one (if measured), but once the platform and Echelon are charged at cost the group needs more assets than the previous study's fully loaded case. A different company emerges only if (a) Unbound earns external licence revenue on ~20k+ funds, or (b) measured agent productivity brings the platform to the low case (~$1.0M/yr fully allocated). Both are testable early and cheaply.
""")

add("Method, definitions and double-counting rules", f"""
- **Layers.** A Echelon Foundry (shared engineering, reusable components, governance tooling, dev infrastructure, component security, monitoring, organisational administration). B Unbound (DAF-specific build, maintenance, integrations, platform operations, platform assurance, licensing in and out). C DAF servicing (acquisition, sponsor relationships, financial operations, grant administration, service, servicing assurance).
- **Standalone** = annual cost if the layer existed alone and had to buy or build what the other layers supply, including its own corporate floor. Standalone figures are **not additive**: the difference between the sum of standalone costs and the group cost is the duplication a split would create.
- **Incremental** = annual cost the group incurs by adding the layer when the other two exist (avoidable cost). For A, incremental includes the cost caused by B's production reliance; for B, it is net of verified Echelon reuse; for C, it excludes the platform (B supplies it).
- **Fully allocated** = incremental direct cost + causal share of shared corporate cost (keys in layer-costs.csv) + pro-rata contingency. Fully allocated costs sum exactly to the group total (checked: residual $0).
- **No double counting.** (1) The principal who maintains Echelon cannot also be Unbound's full-time accountable technical lead: the group carries 1.5 senior technical FTE (A01 0.5 + B02 1.0). (2) Transfer charges (T01-T03) are shown for entity P&Ls but eliminate on consolidation. (3) The integration engineer step cost moves from C to B (B04) and is removed from C06. (4) Payment rails are passed through (transfer, not saving). (5) Sponsor-retained work and sponsor entity costs are excluded and never counted as eliminated.
- **Sources.** Previous study cost register, staffing models and F# model (re-run at R with `dotnet fsi` against the published DLL: `work/fsx/ref.fsx`, `work/fsx/be.fsx`) [M]; Unbound parameters and convergence clauses [S]; Echelon component repos measured with `git log`/`git ls-files` [M]. Numbers marked [A] are analyst placeholders.
- **Scripts:** `work/build_layers.py` (layer-costs.csv, summary), `work/registers.py` (other CSVs), `work/report.py` (this file).
""")

def layer_table():
    rows = []
    for L, name in (("A", "A Echelon Foundry"), ("B", "B Unbound"), ("C", "C DAF servicing")):
        rows.append(f"| {name} | {m(st('base',L))} ({m(st('lo',L))}-{m(st('hi',L))}) | {m(di('base',L))} ({m(di('lo',L))}-{m(di('hi',L))}) | {m(fa('base',L))} ({m(fa('lo',L))}-{m(fa('hi',L))}) |")
    return "\n".join(rows)

add("Part 1: layer cost structures at R", f"""
| Layer | Standalone | Incremental direct | Fully allocated |
|---|---|---|---|
{layer_table()}
| Shared corporate (audit/accounting, insurance, counsel, per-FTE, compliance tooling) | | {m(C['base']['shared_total'])} | allocated by key |
| Contingency 7.5% | | {m(C['base']['contingency'])} | pro rata |
| **Group** | (not additive) | | **{m(grp('base'))}** ({m(grp('lo'))}-{m(grp('hi'))}) |

**Layer A, Echelon Foundry.** Standalone ~$0.35M is mostly the principal's market cost ($222k, economic). Measured facts: 26 component repos, 9,045 commits since 2025-07-07, one human author plus AI agents (majority of commits carry Claude co-author trailers), ~833k lines in code-type files including tests and generated output; 22 repos PolyForm Noncommercial, 3 MIT, 2 without a licence file [M]. Nothing runs in production (ECH-21). Incremental cost rises to ~$0.40M because a regulated commercial dependant needs a second maintainer ($189k), component security review ($25k), a licence programme with escrow ($25k) and licensor insurance ($35k): **{m(S['echelon_caused_by_B']['base'])}/yr caused by B**.

**Layer B, Unbound.** Build amortisation dominates: $5M ($3-15M) over 5 years = $1.0M/yr standalone [S Unbound parameters]; base -8% with Echelon reuse ($0.92M), low $0.30M only if a 2x agent throughput gain is measured. Engineering run: technical lead + 3 engineers + 1 per-sponsor integration engineer (base). The previous study's Model B carried only a lead and one engineer, which report 03 already flagged as implying an existing platform. Hosting, assurance (SOC 2, pen test, vCISO, tech E&O) and data subscriptions are not reduced by any Echelon component.

**Layer C, servicing.** People are the cost: CEO/relationships, controller, core ops, 5 added ops FTE, ops manager, implementation analyst and fund accountant at R [M]. Plus SOC 1 Type 2, crime insurance, compliance consultant, sales ($250k), onboarding amortisation ($105k) and servicing-specific platform features ($60k/yr). Standalone (no Unbound) adds a platform ($0.32-1.29M: licensed incumbent software at $32-129 per DAF-year, or the previous study's in-house platform with a narrow $0.72M build) and, if that platform cannot support the redesign, a handling penalty of $0.94M (AI-enhanced) to $2.70M (conventional) [M].

**Cash vs economic.** Base group cash cost {m(S['cash_view']['base']['group_cash'])} vs economic {m(grp('base'))}: the {k(S['cash_view']['base']['founder_opportunity_cost'])} gap is founder opportunity cost (Echelon principal assumed unpaid; CEO at Model A cash $116,255 vs $200,142 market). Cash plans may use the lower figure; break-even and pricing must use the economic one.
""")

add("Part 1: shared costs, allocation keys and why shared Echelon resources are not free", f"""
| Shared line | Base | Key | A / B / C share |
|---|---:|---|---|
| S01 audit, fractional CFO, bookkeeping, tax | $80,000 | transactions, entity complexity | 5% / 25% / 70% |
| S02 cyber $5M, D&O, EPLI, GL | $47,000 | records held, payments exposure, headcount | 5% / 35% / 60% |
| S03 outside counsel | $45,000 | matter coding | 15% / 25% / 60% |
| S04 per-FTE overhead | $64,067 | headcount A 1.5 / B 5 / C 11 FTE | 9% / 29% / 63% |
| S05 compliance automation, IR retainer, G&A | $37,700 | controls in scope | 10% / 45% / 45% |
| S06 contingency | $115,814 | direct cost | pro rata |

Keys are [A] causal drivers to be replaced by metered drivers (CNV-ECO-001: events, storage, compute, AI inference; work-item hours for people). **Echelon is charged by two keys:** dependency-caused cost goes 100% to B (A03, A05, A08, A09), and a usage share (base 40%, 20-80%) of Echelon running cost (principal time, agent compute, CI, entity admin) by work-item hours on components in B's SBOM. Leaving these out is the Clarity 'Burden Externalization' pattern the previous study warned about (ECH-01, ECH-19).
""")

add("Part 1: internal licence and service charges (transfer pricing, research level)", f"""
| Charge | Cost-plus | Market-based | Observation |
|---|---|---|---|
| T01 Echelon -> Unbound component licence | {rng(lambda c: S['T01_cost_plus_echelon'][c])}/yr (B-caused cost + 20/40/80% usage share, markup 5/8/10%) | none observable: commercial terms 'forthcoming' (forma README:162-164) | A licence of intangibles between commonly controlled parties should yield income 'commensurate with the income attributable to the intangible' (26 U.S.C. §482). |
| T02 Unbound -> servicing platform charge | {rng(lambda c: S['T02_cost_plus_unbound'][c])}/yr | T03: $0.49M / $0.91M / $2.29M (Unbound's own $49/$91/$229 per fund x 10,000) | Incumbent software band $32-129 per DAF-year (Unbound 05 §3a) is the external comparable; $0.32-1.29M at R. |

**Reading.** At R the servicer is the platform's only customer, so a cost-plus charge loads ~$2.8M onto a $3.0M revenue servicer; a market-based charge ($0.91M) leaves the loss in Unbound instead. **The transfer price moves the loss between entities; it does not change the group loss ({m(grp('base')-3e6)} base).** The services cost method (no markup) applies only to services that do not 'contribute significantly to key competitive advantages, core capabilities, or fundamental risks of success or failure' (26 CFR 1.482-9(b)); platform engineering and core IP licensing look unlikely to qualify, so a markup or a profit-split style method would be expected. This is a research reading of public text, not tax advice; counsel and a tax adviser must decide.

**External revenue.** Servicing fees $3.0M at R. Unbound external licence revenue is $0 at R; 25,000 external funds at $91 would add $2.28M but needs sales ($250k) and SOC 2 for licensees. Echelon external licence revenue: no terms, price or licensee observed ($0). Note: PolyForm NC permits use 'by any charitable organization ... regardless of the source of funding' (forma/LICENSE:65-70), so a DAF sponsor that self-hosts may not need a commercial Echelon licence at all; a commercial servicer is not obviously covered. That limits Echelon's own licence market [research reading].
""")

add("Part 1: incremental answers", f"""
**Incremental cost of a servicing operation if Unbound exists: {rng(lambda c: S['q1_servicing_given_unbound'][c])}/yr at R.** Composition (base): servicing people $1.44M (CEO, controller, core and 5 added ops staff, step roles, December peak), servicing non-personnel $0.14M, sales $0.25M, onboarding amortisation $0.105M, servicing platform features $0.06M, external variable $0.07M, causal share of corporate and contingency ~$0.22M. Against $3.0M revenue, servicing contributes ~{m(3e6-S['q1_servicing_given_unbound']['base'])}/yr toward platform and foundry. A standalone servicer (no Unbound) costs {m(st('base','C'))} base because it must buy or build a platform and may lose the redesign.

**Incremental cost of Unbound if Echelon exists: {rng(lambda c: S['q2_unbound_given_echelon'][c])}/yr at R.** Of this, build amortisation is $0.92M and engineering $0.93M (lead, 3 engineers, integration engineer). Echelon reduces it by {k(ech_saving['base'])} base ({k(ech_saving['lo'])} low, $0 high) and adds the T01 charge {k(S['T01_cost_plus_echelon']['base'])} base. **Net, Echelon makes Unbound {k(-net_ech['base'])}/yr more expensive at base** and {k(net_ech['lo'])}/yr cheaper in the low case.

**Break-even of the three-layer group at 20 bps** (previous model, Model B servicing, AI-native, 5 sponsors, plus the layer fixed extras over the model at R) [M]:

| Average balance | Operating (model only) | Previous fully loaded (+$1.25M) | Layers low (+$0.61M) | Layers base (+$2.07M) | Layers high (+$5.51M) |
|---|---|---|---|---|---|
| $150k | $1.46B | $2.29B | $1.90B | $2.82B | $5.08B |
| $300k | $1.20B | $2.08B | $1.62B | $2.50B | $4.54B |
| $500k | $1.14B | $1.83B | $1.50B | $2.29B | $4.29B |

Rule of thumb: each $100k/yr of fixed cost adds ~$65M of break-even assets at 20 bps (100,000 / (0.0020 x 76.7% contribution margin at R)) [D].
""")

eo_tbl = "\n".join(f"| {r['option_id']} | {r['structure']} | {r['added_admin_cost_annual_base']} | {r['assessment']} |" for r in csv.DictReader(open(OUT / 'entity-options.csv')))
add("Part 1: cost centre vs business unit vs separate legal entities", f"""
| Option | Structure | Added admin $/yr (base) | Assessment |
|---|---|---:|---|
{eo_tbl}

**Recommendation (research level, not legal advice).** Run Echelon, Unbound and servicing as **business units in one entity with priced internal charges now** (EO-LYR-02), so the economics are visible and a later split is cheap. **Ring-fence servicing in a subsidiary when the first staffed-administration sponsor signs** (EO-LYR-05): servicing is where instructions over charitable money, fraud exposure and the SOC 1 reliance sit, and Unbound's own perimeter (CNV-LEG-001: no custody, no payment execution) should be mirrored by the servicer. **Separate the Echelon IP company only when Echelon has a second commercial user** (EO-LYR-03). Three separate entities (EO-LYR-04) duplicate corporate floors (standalone sum {m(st('base','A')+st('base','B')+st('base','C'))} vs group {m(grp('base'))}, including the platform a standalone servicer would need) before any revenue justifies them. Criteria covered per option in entity-options.csv: liability ring-fencing, SOC 1 boundary (inclusive vs carve-out of Unbound as subservice organisation), PolyForm NC licensing, fundraising and transfer pricing/tax.
""")

ar = list(csv.DictReader(open(OUT / "assumption-register.csv")))
better = [r for r in ar if r["replacement_verdict"].startswith("better")]
add("Part 2: conventional assumption register", f"""
`assumption-register.csv`: **{len(ar)} assumptions** (previous study 28, Unbound 18, both 6). Origin: evidence-based estimate 20, organisational habit 10, historical convention 9, economic necessity 7, legal obligation 6. Would exist if designed today: yes 18, partly 31, no 3. Assumes human work that technology could do: yes 12, partly 8.

**Verdicts:** replacement better 17, unproven 32, worse 2 (removing the fractional vCISO; raising queue utilisation), n/a 1.

| Assumption with a replacement judged better | Cost effect of replacement |
|---|---|
""" + "\n".join(f"| {r['assumption_id']}: {r['assumption'][:95]} | {r['cmp_cost']} |" for r in better) + """

**What the register shows.** The conventional assumptions that matter most are not office lines or meetings (small) but: (1) development and operations as separate, sequenced organisations; (2) headcount-ratio step hiring rather than metered workload; (3) one-sponsor exclusivity of deciders; (4) the December bench; (5) per-sponsor onboarding with full parallel run; (6) generated evidence allowed only after auditor reliance; (7) two human approvers per control-relevant change. Items (6) and (7) are where an AI-native design is most constrained and least proven. Legal obligations (sponsor control, §4966 fund-manager status, sanctions, contribution substantiation, retention) and independent assurance are kept in every replacement.
""")

rc_rows = list(csv.DictReader(open(OUT / "requirements-candidates.csv")))
add("Part 3: requirements review against an outcome-designed, workload-driven company", f"""
`requirements-candidates.csv`: **{len(rc_rows)} candidates RC-AN-001..{len(rc_rows):03d}**, each traceable to Unbound IDs (convergence clauses and baseline rows) and to the previous study's RC-ACT/RC-SE candidates where they extend them. Scan basis: 1,653 baseline rows (1,583 normative) and 82 convergence clauses; keyword scan of non-superseded rows found 'manual' 32, 'dual/two-person' 68, 'sign-off/attest' 44, 'per sponsor/each sponsor' 44, 'configur' 118 [M].

| ID | Unbound IDs | Problem category | Replacement (short) |
|---|---|---|---|
""" + "\n".join(f"| {r['candidate_id']} | {r['unbound_ids']} | {r['problem_category']} | {r['proposed_replacement'][:120]}... |" for r in rc_rows) + """

**Highest economic effect:** RC-AN-001 (multi-sponsor deciders for routine classes), RC-AN-005 (no delegation cliff), RC-AN-017 (delegation as a priced contract term), RC-AN-014 (risk-tiered change approval: **unproven and possibly worse**), RC-AN-010 (design-partner contract before full measurement). **None removes a legal obligation**; RC-AN-002 and RC-AN-014 change control design and require external auditor acceptance; RC-AN-001 needs sponsor boards and counsel. All are proposals; Unbound is read-only and its owner ratifies.
""")

fcr = list(csv.DictReader(open(OUT / "failure-catalogue.csv")))
add("Part 4: failure catalogue (cost of being wrong) and staged investment", f"""
`failure-catalogue.csv`: **{len(fcr)} failure modes**, each with annual and capital consequence (arithmetic against the previous F# model re-run at R or its published capital plans), detection mechanism, leading indicator, contingency, recovery cost and stop option.

| Failure | Annual effect at R | Capital effect |
|---|---|---|
""" + "\n".join(f"| {r['failure_mode']} | {r['financial_consequence_annual_usd']} | {r['financial_consequence_capital_usd']} |" for r in fcr) + """

**Staged investment (option to stop cheaply)** [E]:

| Gate | Months | Work | Cumulative spend at stop | Stops these failures before build |
|---|---|---|---|---|
| G0 | 0-3 | Owner-led buyer price tests (bps vs $/fund), Echelon licence terms decision, payments/money-transmission counsel opinion ($15-100k, CST-C08), auditor planned-approach conversation | ~$0.06-0.15M | licensing, money transmission, buyers reject tariff, auditors reject deterministic release |
| G1 | 3-9 | Design-partner contract with price collar and stop-loss; 12-month shadow replay + instrumented time study; 3-month engineering spike on ledger and payment gate with agent-throughput telemetry | ~$0.4-0.75M | AI productivity, excessive exceptions, minutes 2x, customisation, partner withdrawal, acquisition delay |
| G2 | 9-18 | Narrow release-1 build ($0.7-1.8M), SOC readiness, second maintainer | ~$2-3M | development 2x, assurance cost |
| G3 | 18+ | Go-live with delegation package | as previous study ($2.7-3.6M trough minimum) | security incident, market fall (insure/reserve; not stoppable) |

Basis: G1 = 6 months of founder-led cash personnel (Model A cash $427k/yr) + 3 months of contract engineering at $60k + counsel and replay compute; G2 = previous study build variants. **The previous plan hires the full development organisation at month 0 (~$1.05M cumulative at month 6); staging defers that until G1 evidence exists.**
""")

add("Challenge to both the previous conclusions and the new premise", """
- **Against the previous study:** its fully loaded case ($1.8-2.3B) still treats the platform as $1.0M/yr of build and two engineers, carries no Echelon cost, and no onboarding amortisation or servicing-specific platform work. Charging those at cost moves break-even to $2.3-2.8B base. Its AI-native minutes (~50/account-year) remain unmeasured and are the single largest operating lever (minutes x2 = +$0.81M/yr at R).
- **Against the new premise ('an entirely different company'):** the outcome-designed view removes recurring human work mainly in the servicing layer, where the previous study had already assumed most of it away. The new costs it introduces (platform ownership, foundry reliance, second maintainer, assurance of agent-authored code) are fixed and front-loaded. Lower variable cost is not permission to be optimistic: at R the group loses ~$2.0M/yr base.
- **What would make it different:** (1) measured >=2x agent throughput with escaped defects at or below baseline over six months (moves B toward ~$1.0M); (2) external licensing of Unbound to ~20k+ funds; (3) auditors and boards accepting deterministic release and generated evidence from go-live. Each is testable at G0/G1 for well under $1M.
- **Transfers are not eliminations:** complex-gift fees to funds, payment rails to sponsors, deciders to sponsor boards and recertification to advisors are all shown as transfers in the registers.
""")

add("Limitations", """
- Same model family produced the previous study, Unbound's economics and this analysis; nothing here is independent validation.
- No buyer conversation, signed contract, time study, auditor letter, counsel opinion or Echelon licence terms exist. Every handling minute is an assumption inherited from the previous study.
- Layer line values marked [A] (Echelon reliance costs, engineering headcount, allocation keys, usage share, markup, servicing platform features, entity admin increments) are analyst placeholders; ranges are wide on purpose.
- Measured repository facts (commit counts, authorship trailers, line counts, licences) describe activity, not productivity or quality. Line counts include tests and generated files. Commit authorship trailers may under- or over-state AI contribution.
- The F# model was re-run with an extra fixed-cost line to compute break-even; layer extras were treated as fixed, though onboarding amortisation scales with sponsors.
- Transfer pricing, entity, licensing (PolyForm NC charitable carve-out) and money-transmission points are research readings of public text, not legal or tax advice.
- AI-native results are steady-state; pre-delegation periods (Unbound EV-08) are only in the failure catalogue.
""")

add("Largest evidence gaps", """
1. Agent-assisted development throughput and escaped-defect rate on a regulated codebase (decides B: $1.0M vs $2.3M+ per year).
2. Echelon commercial licence terms, escrow/fork right and second-maintainer plan (decides T01 and CNV-GOV-009).
3. External auditor acceptance of deterministic release and generated evidence from go-live (CNV-GOV-001, CNV-GOV-003).
4. Sponsor board willingness and time to delegate (CNV-GRT-001) and to appoint multi-sponsor deciders (RC-AN-001).
5. Measured handling minutes, exception incidence and December arrivals (CNV-EVB-001).
6. Whether any sponsor or administrator would license Unbound externally at ~$90/fund.
7. Counsel opinion on money transmission and on PolyForm NC for nonprofit vs commercial servicers; tax view on related-party pricing.
""")

with open(OUT / "report.jsonl", "w") as f:
    for s in sections:
        f.write(json.dumps(s, ensure_ascii=False) + "\n")

# ------------------------------------------------------------------ evidence
ACC = "2026-11-25"
ev = [
 ("Echelon component repositories: 26 repos, 9,045 commits, first commit 2025-07-07, last 2026-11-25", "9045", "commits", "/home/user/echelon-components/* (git rev-list --count HEAD; git log --format=%cs)", "measured", "2025-07..2026-11", "A", "[M] command: for each repo git rev-list --count HEAD; some repos were shallow at first read and later unshallowed; total from full histories"),
 ("All component repos have one human author plus AI agents/bots; Claude co-author trailers appear on a majority of commits in most repos (e.g. praxis 808/1379, limen 513/588)", "1", "human authors", "/home/user/echelon-components/* (git log --format=%an; grep -ci 'co-authored-by: claude')", "measured", "2025-07..2026-11", "A", "[M] authorship activity, not productivity"),
 ("Code-type files (.fs,.fsx,.ts,.tsx,.js,.mjs,.css,.py,.sh,.cs) across component repos total ~833k lines", "833344", "lines", "/home/user/echelon-components/* (git ls-files | xargs cat | wc -l)", "measured", "2026-11-25", "B", "[M] includes tests and generated files"),
 ("22 of 26 component repos carry PolyForm Noncommercial 1.0.0; echelon-foundry, echelon-registry, project-administration are MIT; causa and echelon-engineering-system have no LICENSE file", "22", "repos", "/home/user/echelon-components/*/LICENSE", "measured", "2026-11-25", "A", "[M] head -1 LICENSE"),
 ("Forma: 'Commercial use requires a separate license from Echelon Foundry' and 'Commercial licensing information is forthcoming'", "", "", "/home/user/echelon-components/forma/README.md:162-164", "primary", "2026-11-25", "A", "[S]"),
 ("PolyForm NC: use by any charitable organization ... is use for a permitted purpose regardless of the source of funding", "", "", "/home/user/echelon-components/forma/LICENSE:65-70", "primary", "1.0.0", "A", "[S] research reading only"),
 ("Previous model re-run at R (Model B, AI-native, 5 sponsors, $1.5B, $150k, 20 bps): revenue 3,000,000; total 2,916,936; external 72,685; added ops 5 FTE 497,390; peak 68,704; core personnel 894,425; non-personnel 746,862; step 576,870; sponsor costs 60,000", "2916936", "USD/yr", "work/fsx/ref.fsx against daf-landscape/.../model/src/ServicingEconomics/bin/Release/net10.0/ServicingEconomics.dll", "measured", "2026-11-25", "A", "[M] matches results.md stress table base $2.92M"),
 ("Same scenario AI-enhanced 3,860,452; conventional 5,617,931; elimination 2,637,368; minutes x2 3,731,199; minutes x3.33 4,674,264; volume x1.5 3,188,186; vendor x1.5 3,326,709; wages x1.15 3,222,544; incident $1M 3,916,936; 10 sponsors 3,079,555", "", "USD/yr", "work/fsx/ref.fsx", "measured", "2026-11-25", "A", "[M]"),
 ("Break-even AUA at 20 bps with layer fixed extras: base +$2.07M -> $2.82B/$2.50B/$2.29B at $150k/$300k/$500k; low +$0.61M -> $1.90B/$1.62B/$1.50B; high +$5.51M -> $5.08B/$4.54B/$4.29B", "", "USD AUA", "work/fsx/be.fsx", "measured", "2026-11-25", "A", "[M] model-only reproduces $1.46B/$1.20B/$1.14B"),
 ("Unbound build capex assumption $5,000,000 (3-15M)", "5000000", "USD", "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json build_capex", "primary", "2026-11-24", "A", "[S] labelled A by Unbound"),
 ("Unbound licence $49/$91/$229 per fund at 250k/100k/25k platform funds; vendor break-even $81-131 at 50-100k funds", "91", "USD/fund-yr", "/home/user/unbound/requirements/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md §1-2", "primary", "2026-11-24", "A", "[S] modelled"),
 ("Incumbent software $32-129 per DAF-year; outsourced administration $413-745", "", "USD/DAF-yr", "/home/user/unbound/requirements/convergence/2026-11-24-master/05-ECONOMIC-VALIDATION.md §3a", "secondary", "Form 990", "B", "[S] via Unbound report 13"),
 ("CNV-GOV-004: reserved-authority holders and December surge reviewers exclusive to one sponsor; owner kept the absolute rule for release 1 (OD-M-01)", "", "", "/home/user/unbound/requirements/convergence/2026-11-24-master/data/convergence-clauses.jsonl CNV-GOV-004", "primary", "2026-11-24", "A", "[S]"),
 ("CNV-GOV-001: manual review procedures replaced by generated evidence only after the auditor confirms reliance", "", "", "convergence-clauses.jsonl CNV-GOV-001", "primary", "2026-11-24", "A", "[S]"),
 ("CNV-AIO-001: release-1 agent-executable set only reversible internal actions at A2 or below", "", "", "convergence-clauses.jsonl CNV-AIO-001", "primary", "2026-11-24", "A", "[S]"),
 ("CNV-GOV-008: delegations expire no later than 12 months; renewal refused if last quarterly report unacknowledged", "12", "months", "convergence-clauses.jsonl CNV-GOV-008", "primary", "2026-11-24", "A", "[S]"),
 ("CNV-GOV-009: no release-1 production dependency under a non-commercial licence without executed commercial licence plus escrow or fork right", "", "", "convergence-clauses.jsonl CNV-GOV-009", "primary", "2026-11-24", "A", "[S]"),
 ("CNV-PLT-010: two approvers on every change to control-relevant modules, neither the author", "2", "approvers", "convergence-clauses.jsonl CNV-PLT-010", "primary", "2026-11-24", "A", "[S]"),
 ("UNB-XIN-IAM-004: access recertification quarterly for privileged/workforce roles, annually for delegated customer roles", "", "", "/home/user/unbound/requirements/baseline/baseline.jsonl UNB-XIN-IAM-004", "primary", "2026-11-24", "A", "[S]"),
 ("Unbound baseline: 1,653 rows, 1,583 normative; non-superseded keyword hits manual 32, dual/two-person 68, sign-off/attest 44, per sponsor 44, configur 118", "1653", "rows", "/home/user/unbound/requirements/baseline/baseline.jsonl", "measured", "2026-11-25", "A", "[M] regex scan"),
 ("26 U.S.C. §482: Secretary may allocate income among commonly controlled businesses; licence income from intangibles shall be commensurate with the income attributable to the intangible", "", "", "https://www.law.cornell.edu/uscode/text/26/482", "primary (secondary host)", "current", "B", "[S] fetched 2026-11-25; research reading, not advice"),
 ("26 CFR 1.482-9(b): services cost method prices at total services cost with no markup; covered services exclude those contributing significantly to key competitive advantages, core capabilities or fundamental risks", "", "", "https://www.law.cornell.edu/cfr/text/26/1.482-9", "primary (secondary host)", "current", "B", "[S] fetched 2026-11-25"),
 ("26 U.S.C. §4966: 20% tax on each taxable distribution, paid by the sponsoring organization", "0.2", "share", "https://www.law.cornell.edu/uscode/text/26/4966", "primary (secondary host)", "current", "B", "[S] fetched 2026-11-25"),
 ("Previous study capital: C anchor $3.56M; signings +6 months $4.39M; build x2.5 $4.82M; Unbound-scale build $8.51M; AI-enhanced only $3.68M; plan D $5.36M, AI-enhanced $7.63M", "3560000", "USD", "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/06-capital-and-runway.md §2", "primary", "2026-11-25", "A", "[S] modelled"),
 ("Previous study: verified Echelon reuse saves $0-105k/yr, all 'share'", "105000", "USD/yr", "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/03-organization-and-budget.md:539-545", "primary", "2026-11-25", "A", "[S] modelled"),
 ("CNV-LEG-001: Unbound shall not receive or hold donor or grant money and shall not be able to execute a payment", "", "", "convergence-clauses.jsonl CNV-LEG-001", "primary", "2026-11-24", "A", "[S]"),
 ("ECH-01: one human maintainer plus Claude; no second maintainer; Foundry intended users 'not yet established'", "1", "maintainers", "/home/user/daf-landscape/data/commercial-opportunity/servicing-economics/echelon-capabilities.csv ECH-01", "primary", "2026-11-25", "A", "[S]"),
 ("Sponsor-level work ~324 h/yr AI-native per sponsor (160-830); December daily load 3.1-3.3x", "324", "h/sponsor-yr", "/home/user/daf-landscape/research/commercial-opportunity/servicing-economics/04-activity-cost-and-capacity.md:269-277", "primary", "2026-11-25", "C", "[S] derived from assumptions; no time study"),
 ("Echelon Foundry pilot rule: do not infer it is a validated discipline, method or product", "", "", "/home/user/echelon-components/echelon-foundry/README.md (Pilot rule)", "primary", "2026-11-25", "A", "[S]"),
]
with open(OUT / "evidence.jsonl", "w") as f:
    for i, (claim, value, unit, src, stype, period, q, notes) in enumerate(ev, 1):
        f.write(json.dumps({"evidence_id": f"EV-LYR-{i:03d}", "claim": claim, "value": value, "unit": unit, "source_url_or_path": src,
                            "source_type": stype, "filing_period": period, "accessed": ACC, "quality": q, "notes": notes}) + "\n")

asm = [
 ("Reference scenario R: 5 sponsors, 10,000 accounts, $1.5B, $150k balance, AI-native steady state, 20 bps", "1.5e9", "USD AUA", "", "", "previous study reference row", ["EV-LYR-007"], "all layer figures scale with it"),
 ("Group needs 1.5 senior technical FTE: Echelon principal 0.5 + Unbound technical lead 1.0", "1.5", "FTE", "1", "2", "one person cannot be full-time maintainer of 26 repos and accountable platform lead", ["EV-LYR-002", "EV-LYR-027"], "+/-$0.11-0.22M/yr"),
 ("Unbound platform engineers excluding per-sponsor integration upkeep", "3", "FTE", "1", "5", "report 03: conventional 4-10 FTE; prior Model B 1", ["EV-LYR-025"], "largest B lever: ~$0.19M per FTE"),
 ("Echelon reuse reduces build and engineering cost (S0)", "0.08", "share", "0", "0.5", "report 03 ECH-4: S0 0-16%; S1 33-50% if measured", ["EV-LYR-025"], "low case requires measured >=2x throughput"),
 ("Second maintainer needed once a regulated platform relies on Echelon components", "1.0", "FTE", "0.5", "1.0", "CNV-GOV-009 escrow/fork; single maintainer", ["EV-LYR-017", "EV-LYR-027"], "$79-220k/yr"),
 ("Component security and supply-chain assurance for production reliance", "25000", "USD/yr", "10000", "60000", "ECH-11 placeholder 0-40k", [], "small"),
 ("Licence programme (drafting, IP/AI-provenance review, escrow) annualised", "25000", "USD/yr", "7000", "60000", "no quotes", ["EV-LYR-005"], "small"),
 ("Licensor insurance once components are licensed commercially", "35000", "USD/yr", "15000", "70000", "CST-I03 + I04", [], "small"),
 ("Usage share of Echelon running cost borne by Unbound", "0.4", "share", "0.2", "0.8", "work-item hours on SBOM components (to be metered)", [], "T01 +/-$0.05M"),
 ("Related-party markup on cost-plus charges", "0.08", "share", "0.05", "0.10", "research reading of §482 / 1.482-9; no benchmark study", ["EV-LYR-021", "EV-LYR-022"], "T01/T02 only; zero at group level"),
 ("Shared corporate allocation keys (S01-S05 shares in report)", "", "shares", "", "", "causal drivers pending metering (CNV-ECO-001)", [], "moves cost between layers only"),
 ("Standalone corporate floor shares for B and C (S01 70/90%, S02 80/90%, S03 60/80%, S05 80/80%, per-FTE by own headcount)", "", "shares", "", "", "a standalone entity bears most corporate fixed cost itself", [], "standalone totals only"),
 ("Servicing-specific platform features one-off", "300000", "USD", "150000", "600000", "administrator principal, federated queue, workbench (CNV-TEN-001)", [], "$30-120k/yr amortised"),
 ("AI agent compute for Echelon development", "24000", "USD/yr", "6000", "60000", "no invoice observed", ["EV-LYR-001"], "small"),
 ("Added admin cost per extra legal entity", "", "USD/yr", "30000", "130000", "books/tax/filings + audit + insurance minimums + intercompany documentation", [], "entity options only"),
 ("Echelon principal cash compensation", "0", "USD/yr", "0", "222482", "owner time; economic cost shown at CTO market rate", [], "cash vs economic gap"),
 ("Staged gates G0/G1 cumulative spend at stop", "0.15/0.75", "USD M", "0.06/0.4", "0.15/0.75", "Model A cash personnel $427k/yr x 0.5 + 3 months contract engineering + counsel", ["EV-LYR-024"], "option value of staging"),
]
with open(OUT / "assumptions.jsonl", "w") as f:
    for i, (stmt, v, u, lo, hi, basis, evs, sens) in enumerate(asm, 1):
        f.write(json.dumps({"assumption_id": f"A-LYR-{i:03d}", "statement": stmt, "value": v, "unit": u, "low": lo, "high": hi,
                            "basis": basis, "evidence_ids": evs, "sensitivity": sens}) + "\n")

for fn in ("report.jsonl", "evidence.jsonl", "assumptions.jsonl"):
    n = sum(1 for line in open(OUT / fn) if json.loads(line) is not None)
    print(fn, n)
