"""Development investment scenarios for a minimum DAF servicing product (MSP). Pure functions; all inputs labelled."""
import csv, sys, math
RATE = 120.0          # [D] USD/h loaded: senior engineer CST-R03 $188,958 base / 1,600 productive h (A-ACT-002) = $118 -> $120
HPM = 1600/12         # [D] productive hours per person-month
C_SHARE = 0.70        # [A] share of conventional effort compressible by agents (code, tests, docs); rest = decisions, review, integration coordination, manual a11y/security verification
REUSE_CREDIT_PM = 4   # [E] Echelon reuse credit (Forma CSS/patterns, Folio print markup, Strata schema mgmt, Aegis fault handling); prior study bound 0-16% of eng run cost
# capability groups in delivery order: (key, label, conventional person-months [E], mandatory_for_live_money, unbound_ids)
GROUPS = [
 ("ARCH","Architecture, infra, CI/CD, observability, DR baseline",6,True,"CNV-ARC-001; UNB-DATA-001; UNB-IMM-001"),
 ("IAM","Identity (bought OIDC IdP), tenancy, roles, scoped advisor permissions",6,True,"UNB-TEN-001; UNB-ADV-001/002; CNV-PLT-003"),
 ("LEDGER","Append-only double-entry fund ledger, posting rules, bitemporal corrections",18,True,"ACC-MDL-001..; UNB-IMM-*; UNB-DATA-*"),
 ("CONTRIB","Contributions (cash/ACH via sponsor processor, manual securities receipt), gift-completion states, acknowledgments",8,True,"UNB-LS-001; UNB-DON-002; TVR-CON-*"),
 ("CHARDATA","Charity eligibility data: IRS EO BMF, Pub 78, auto-revocation, OFAC SDN screening",4,True,"UNB-EXT-001; UNB-CHAR-*; UNB-RULE-*"),
 ("GRANTS","Grant recommendation, eligibility, sponsor approval, maker-checker, disbursement file to bank/check vendor, exceptions",14,True,"UNB-GRANT-*; UNB-PAY-001/002; EXC-*; CNV-GRT-002"),
 ("RECON","Bank/custodian cash reconciliation and close",8,True,"UNB-ACC-*; ACC-MDL-*"),
 ("NAVMIN","Minimum investment valuation: periodic NAV/unit import from custodian statements",4,True,"UNB-NAV-001/002 (subset)"),
 ("STMT","Statements, tax receipts, sponsor reports (accessible HTML primary, tagged PDF)",8,True,"CNV-EXP-001; FOLIO gaps"),
 ("WORKFLOW","Work queues, audit log, segregation of duties evidence",8,True,"CNV-GOV-003; MON-001/002"),
 ("UI","Donor portal and operations console, WCAG 2.2 AA",16,True,"UNB-PLAT-002; INT-*; CNV-EXP-001"),
 ("SECCTL","Security engineering and SOC-relevant controls (logging, access review, change mgmt, secrets, remediation)",8,True,"SOC2-*; CNV-GOV-001"),
 ("PRODUCT","Requirements refinement, product decisions, acceptance",8,True,"REQ-*; CNV-* acceptance criteria"),
 ("NAVFULL","Full custodian feeds, multi-pool unitization, percentage grants",8,False,"UNB-CUST-*; UNB-NAV-*; UNB-GFUND-*"),
 ("MULTI","Multi-sponsor white-label configuration and tenant isolation profiles",6,False,"UNB-TEN-002; UNB-PLAT-*"),
 ("MIGR","Bulk migration/onboarding tooling",6,False,"ADM-*; implementation tooling"),
]
FIXED = dict(pentest=(10000,20000,35000), a11y_audit=(10000,25000,40000), soc_readiness=(10000,20000,40000),
             infra_per_month=(2000,3000,5000), vendor_sandboxes=(2000,5000,15000), sec_tooling=(0,5000,10000))
def eff(m): return C_SHARE/m + (1-C_SHARE)
def conv_pm(groups): return sum(g[2] for g in groups)
def fixed_cost(months, i=1): return sum(v[i] for k,v in FIXED.items() if k!='infra_per_month') + FIXED['infra_per_month'][i]*months
def agent_compute(conv_hours):
    # [E] measured ordo missions $12.66-$27.15 (EV-SDE-2026-0008) per ~640-1,180 added lines; assume 1 mission per 16 conventional
    # compressible hours, $20/mission, rework/retry factor 3 (range 1-10)
    return C_SHARE*conv_hours/16*20*3
def assurance(i=1): return sum(FIXED[k][i] for k in ('pentest','a11y_audit','soc_readiness','vendor_sandboxes','sec_tooling'))
def plan(budget, m):
    done=[]; spent_h=0.0; conv_done=0.0
    def pm_of(g): return g[2] - (REUSE_CREDIT_PM*0.5 if g[0] in ("UI","STMT") else 0)
    def cost_of(h, conv_pm_):
        months = max(6, h/(2*HPM))          # [A] calendar ~ 2 FTE-equivalent team, minimum 6 months
        return h*RATE + agent_compute(conv_pm_*HPM) + FIXED['infra_per_month'][1]*months
    mand=[g for g in GROUPS if g[3]]
    for g in GROUPS:
        pm=pm_of(g); h=pm*HPM*eff(m)
        need_assure = assurance() if (g[3] and all(x in done or x is g for x in mand)) or (not g[3]) else 0
        if cost_of(spent_h+h, conv_done+pm) + need_assure <= budget: done.append(g); spent_h+=h; conv_done+=pm
        elif g[3]: break
    mand_done=all(g in done for g in mand)
    months=max(6, spent_h/(2*HPM)) if done else 0
    ac=agent_compute(conv_done*HPM); infra=FIXED['infra_per_month'][1]*months
    fx = infra + (assurance() if mand_done else 0)
    gaps=[g[0] for g in mand if g not in done]
    defer=[g[0] for g in GROUPS if not g[3] and g not in done]
    safe = "conditional" if mand_done else "N"
    conv_h = conv_done*HPM
    eng_low = 0.12*conv_h*eff(m)*RATE; eng_high=0.25*conv_h*eff(m)*RATE
    if mand_done: eng_low=max(eng_low, 1*188958); eng_high=max(eng_high, 2*188958)
    rec_low = 24000+10000 if mand_done else 0; rec_high = 60000+35000 if mand_done else 0
    total = spent_h*RATE+ac+fx
    full = len(done)==len(GROUPS)
    note = ("; unspent ${:,.0f} available for broader Unbound scope (1,185 initial-scope normative items) or runway".format(budget-total) if full and budget-total>50000 else "")
    return dict(scenario_usd=budget, productivity_multiple=m, effective_multiple=round(1/eff(m),2),
        human_hours=round(spent_h), loaded_human_cost=round(spent_h*RATE), agent_compute_cost=round(ac),
        infra_test_security_cost=round(fx), total_cost=round(total),
        conv_pm_delivered=round(conv_done,1), pct_mandatory_conv_pm=round(100*sum(pm_of(g) for g in done if g[3])/sum(pm_of(g) for g in mand)),
        deliverable_scope=("; ".join(g[0] for g in done) or "none beyond a spike/prototype") + note,
        deferrable_scope="; ".join(defer),
        gaps=("; ".join(gaps) + "; independent pen test, a11y audit, SOC readiness unfunded") if gaps else "none in MSP mandatory set; still open: SOC 1/2 Type II observation period, bank/custodian/processor agreements, counsel opinions, second maintainer",
        safe_to_operate_live_money=safe, annual_maintenance_low=round(eng_low+rec_low), annual_maintenance_high=round(eng_high+rec_high),
        basis=f"[D] from [E] MSP decomposition {conv_pm(GROUPS)} conventional person-months less {REUSE_CREDIT_PM} Echelon reuse credit; effective multiple 1/(0.7/m+0.3) [A]; ${RATE:.0f}/h [D CST-R03/A-ACT-002]; agent $20/mission x3 rework [E EV-SDE-2026-0008]; assurance CST-C13/C14 [C] + a11y audit [A]; maintenance 12-25%/yr of build [A] with 1-2 FTE floor once live [A]; SOC audit fees excluded (operating)")
def main(out):
    rows=[plan(b,m) for b in (100000,250000,500000,1000000,1800000,5000000) for m in (1,1.5,2,3,5,10)]
    with open(out,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    full_conv = conv_pm(GROUPS)-REUSE_CREDIT_PM; mand = sum(g[2] for g in GROUPS if g[3])-REUSE_CREDIT_PM
    for m in (1,1.5,2,3,5,10):
        print(f"m={m} eff={1/eff(m):.2f} MSP-mandatory human h={mand*HPM*eff(m):,.0f} cost=${mand*HPM*eff(m)*RATE:,.0f}; full MSP h={full_conv*HPM*eff(m):,.0f} cost=${full_conv*HPM*eff(m)*RATE:,.0f} agent=${agent_compute(full_conv*HPM):,.0f}")
    for r in rows: print(r['scenario_usd'],r['productivity_multiple'],r['human_hours'],r['total_cost'],r['pct_mandatory_conv_pm'],r['safe_to_operate_live_money'],r['deliverable_scope'][:90],'|',r['annual_maintenance_low'],r['annual_maintenance_high'])
if __name__=='__main__': main(sys.argv[1])
