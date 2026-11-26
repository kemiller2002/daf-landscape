"""CST group: cost register, role compensation and staffing models for a DAF servicing company.
Pure functions; run: python3 -I -B build.py <wages.json> <outdir>"""
import csv, json, sys, os

ACC = "2026-11-25"
ONET = "https://www.onetonline.org/link/localwages/{soc}.00"
ECEC_T04 = "https://www.bls.gov/news.release/ecec.t04.htm"
ECEC_T06 = "https://www.bls.gov/news.release/ecec.t06.htm"
ECEC_NR = "https://www.bls.gov/news.release/ecec.nr0.htm"
KFF = "https://www.kff.org/health-costs/annual-family-premiums-for-employer-coverage-rise-6-in-2025-nearing-27000-with-workers-paying-6850-toward-premiums-out-of-their-paychecks/"
BUDGET = "/home/user/daf-landscape/research/commercial-opportunity/daf-servicer-bottom-up-operating-budget-2026-11-25.md"
UNB_PARAMS = "/home/user/unbound/requirements/discovery/2026-11-24-simplification-economics/model/parameters.json"
UNB_05A = "/home/user/unbound/requirements/convergence/2026-11-24-master/05a-ECONOMIC-TABLES.md"

# ---------------------------------------------------------------- labour constants
SS_BASE = 184500          # [S-C] 2026 OASDI contribution base (search result citing ssa.gov; ssa.gov page itself 403)
PROD_HOURS = {"low": 1400, "base": 1520, "high": 1650}
# burden scenario parameters [A] except health anchors [D from KFF 2025]
HEALTH_SINGLE_ER = 9325 - 1440   # 7,885 [D] KFF 2025 single premium less worker share (single figures from KFF via search, family read directly)
HEALTH_FAMILY_ER = 26993 - 6850  # 20,143 [D] KFF 2025 family premium less worker share (read)
BURDEN = {
    "low":  {"health": HEALTH_SINGLE_ER, "ret": 0.02, "other": 0.005, "peo": 216, "suta": 300, "wc": 0.001},
    "base": {"health": 14000, "ret": 0.03, "other": 0.010, "peo": 948, "suta": 600, "wc": 0.002},
    "high": {"health": HEALTH_FAMILY_ER, "ret": 0.05, "other": 0.015, "peo": 1488, "suta": 1200, "wc": 0.004},
}

def employer_taxes(salary, p):
    return 0.062 * min(salary, SS_BASE) + 0.0145 * salary + 42 + p["suta"] + p["wc"] * salary

def benefits(salary, p):
    return p["health"] + p["ret"] * salary + p["other"] * salary + p["peo"]

def loaded(salary, p):
    return salary + employer_taxes(salary, p) + benefits(salary, p)

# ECEC June 2026 private industry ($/hour worked) [S] table 4 / table 6
ECEC = {
    "Management, professional, and related": dict(w=54.06, pl=7.37, sup=3.59, ins=5.87, ret=2.92, leg=5.07, tot=78.88),
    "Management, business, and financial": dict(w=59.85, pl=8.47, sup=4.89, ins=6.63, ret=3.23, leg=5.56, tot=88.63),
    "Professional and related": dict(w=50.98, pl=6.78, sup=2.90, ins=5.47, ret=2.75, leg=4.81, tot=73.69),
    "Office and administrative support": dict(w=25.22, pl=2.77, sup=1.06, ins=4.05, ret=1.05, leg=2.58, tot=36.73),
    "Financial activities industry": dict(w=43.23, pl=6.04, sup=3.78, ins=6.43, ret=2.44, leg=4.13, tot=66.05),
    "Information industry": dict(w=54.46, pl=8.63, sup=4.50, ins=8.06, ret=3.26, leg=5.38, tot=84.28),
    "Establishments 1-49 workers (all occupations)": dict(w=27.88, pl=2.34, sup=1.23, ins=2.35, ret=0.87, leg=2.97, tot=37.64),
    "All private industry": dict(w=32.82, pl=3.54, sup=1.88, ins=3.69, ret=1.57, leg=3.40, tot=46.89),
}

def ecec_mult(e, with_supplemental=False):
    """Burden on an annual salary that already pays for leave: (insurance+retirement+legally required[+supplemental]) / (wages+paid leave)."""
    add = e["ins"] + e["ret"] + e["leg"] + (e["sup"] if with_supplemental else 0)
    return 1 + add / (e["w"] + e["pl"])

def naive_mult(e):
    return e["tot"] / e["w"]

# ---------------------------------------------------------------- roles
# (key, role, soc, low, base, high, reason, qualifications, ecec_group, platform_or_staffed, extra_sources)
ROLES = [
    ("ceo", "Founder / CEO-managing director (sponsor relationships, sales, governance)", "11-1021|11-1011|11-2022", 130000, 165000, 215000,
     "11-1021 GM median $105,770 understates an executive selling to sponsor CFOs/boards; base set near 11-2022 sales-manager median $148,270 + premium; high = 11-1011 chief-executive median $213,990; existing hypothesis $130k used as low",
     "10+ yrs philanthropy/financial-services leadership; sponsor/board selling; contract negotiation", "Management, business, and financial", "shared", ""),
    ("cto", "CTO / technical lead (architecture, security, DR, AI controls)", "11-3021|15-1252", 165000, 185000, 220730,
     "11-3021 median $175,140, p75 $220,730; 15-1252 p75 $171,980; remote fintech senior-engineer posting $165-185k (Moov); existing $150k is below 11-3021 p25 $138,060-adjacent band for a lead who also owns security",
     "Senior engineer with payments/ledger, PostgreSQL, cloud security, SOC 2 control ownership", "Professional and related", "software platform", "EV-CST-060"),
    ("swe", "Senior software engineer (full-stack, ledger, integrations)", "15-1252", 135980, 155000, 171980,
     "15-1252 median $135,980 low, p75 $171,980 high; base between median and remote fintech posting band $165-185k",
     "5+ yrs; TypeScript/F#/Python, PostgreSQL, payments/ACH files, testing", "Professional and related", "software platform", "EV-CST-060"),
    ("sec", "Security / infrastructure engineer (DevSecOps, IAM, DR)", "15-1212|15-1244", 129180, 145000, 163500,
     "15-1212 median $129,180 to p75 $163,500", "Cloud IAM, logging/SIEM, incident response, SOC 2 evidence", "Professional and related", "software platform", ""),
    ("dba", "Database / data engineer (PostgreSQL, reconciliation data)", "15-1242", 104620, 115000, 135460,
     "15-1242 median $104,620 to p75 $135,460", "PostgreSQL HA/replication, backups, data migration", "Professional and related", "software platform", ""),
    ("ctrl", "Controller / head of financial operations", "11-3031|13-2011", 125490, 150000, 166570,
     "Role is a financial manager (11-3031 p25 $125,490, median $166,570), not an accountant (13-2011 p75 $109,810); existing $115k sits in the accountant band; nonprofit controller postings $108-144k (search, not verified)",
     "CPA preferred; fund accounting; cash/bank reconciliation; SOC 1 control ownership; nonprofit/DAF accounting", "Management, business, and financial", "staffed administration", ""),
    ("acct", "Fund / grant accountant (reconciliation, close)", "13-2011", 67020, 85000, 95000,
     "13-2011 p25 $67,020, median $83,680; remote nonprofit staff accountant posting $80,600-87,100 (NFF)",
     "BS accounting; fund accounting; bank and custodian reconciliation", "Professional and related", "staffed administration", "EV-CST-061"),
    ("gopsm", "Grant operations manager", "11-1021|11-3031|13-2099", 105770, 120000, 138000,
     "11-1021 median $105,770 low; remote DAF 'Officer, Grant Operations' posting $125-138k (ImpactAssets) high",
     "DAF grant operations, due diligence, payments, team supervision", "Management, business, and financial", "staffed administration", "EV-CST-062"),
    ("ops", "Grant & client operations specialist", "13-2099|43-3099", 62000, 75000, 90000,
     "13-2099 p25 $61,290, median $81,100; 43-3099 median $53,830; remote philanthropy analyst posting $100-104k (RPA) is above; existing $80k is inside range",
     "2+ yrs grants/donor services; payments; charity verification; careful written communication", "Office and administrative support", "staffed administration", "EV-CST-063"),
    ("comp", "Compliance officer (charity due diligence, sanctions, policy, audit liaison)", "13-1041", 80730, 95000, 109010,
     "13-1041 median $80,730 to p75 $109,010", "Sanctions/OFAC programs, charitable-purpose due diligence, SOC/control testing", "Management, business, and financial", "shared", ""),
    ("impl", "Implementation / client success analyst (sponsor onboarding, migration)", "13-1111", 85000, 100000, 115000,
     "13-1111 median $101,860, p25 $77,950, p75 $133,370", "Data migration, requirements, sponsor configuration, training", "Management, business, and financial", "staffed administration", ""),
    ("sales", "Sales / business development director", "11-2022", 120000, 148270, 180000,
     "11-2022 median $148,270 (p25 $100,360, p75 $207,340); variable commission excluded", "Selling to DAF sponsors, community foundations, advisor channels", "Management, business, and financial", "shared", ""),
    ("csr", "Donor / client service representative", "43-4051", 44770, 55000, 65000,
     "43-4051 median $44,770, p75 $51,780; DAF donor service needs higher skill so base above p75", "Phone/email donor service, DAF rules, escalation", "Office and administrative support", "staffed administration", ""),
    ("bk", "Bookkeeping / accounting clerk (alternative to outsourced bookkeeping)", "43-3031", 43520, 50670, 61470,
     "43-3031 p25/median/p75", "AP/AR, bank feeds", "Office and administrative support", "staffed administration", ""),
    ("gc", "General counsel (in-house; Model C trigger only)", "23-1011", 159670, 190000, 221370,
     "23-1011 median $159,670 to p75 $221,370", "Nonprofit/tax-exempt + financial services regulation", "Management, business, and financial", "shared", ""),
]

def role_row(r, wages):
    key, role, socs, lo, ba, hi, reason, quals, grp, pos, extra = r
    primary = socs.split("|")[0]
    w = wages[primary]
    L = {k: loaded(s, BURDEN[k]) for k, s in (("low", lo), ("base", ba), ("high", hi))}
    mult = L["base"] / ba
    e = ECEC[grp]
    srcs = [ONET.format(soc=s) + " (BLS OEWS May 2025 national, via O*NET OnLine, accessed " + ACC + ")" for s in socs.split("|")]
    srcs += [ECEC_T04 + " (ECEC June 2026, table 4)", KFF + " (KFF EHBS 2025)"]
    return {
        "key": key, "role": role, "soc_code": socs, "occupation_title": w["title"],
        "bls_median_annual": w["p"][2], "p25": w["p"][1], "p75": w["p"][3], "p10": w["p"][0], "p90": w["p"][4],
        "period": "OEWS May 2025 (released 2026), national all-industry",
        "chosen_base_salary_low": lo, "chosen_base_salary_base": ba, "chosen_base_salary_high": hi,
        "salary_reason": reason,
        "employer_taxes_base": round(employer_taxes(ba, BURDEN["base"])), "benefits_base": round(benefits(ba, BURDEN["base"])),
        "burden_multiplier": round(mult, 3),
        "ecec_benchmark_multiplier": round(ecec_mult(e), 3), "ecec_group": grp,
        "loaded_cost_low": round(L["low"]), "loaded_cost_base": round(L["base"]), "loaded_cost_high": round(L["high"]),
        "productive_hours": PROD_HOURS["base"],
        "loaded_hourly_rate": round(L["base"] / PROD_HOURS["base"], 2),
        "loaded_hourly_range": f"{L['low']/PROD_HOURS['high']:.2f}-{L['high']/PROD_HOURS['low']:.2f}",
        "qualifications": quals, "platform_or_staffed": pos,
        "notes": "Loaded = salary + employer taxes (OASDI 6.2% to $184,500, Medicare 1.45%, FUTA $42, SUTA and workers comp [A]) + benefits (health employer share, retirement match, life/disability, PEO admin) [D]; excludes equity, bonus/commission, recruiting, equipment and SaaS (in cost register). Remote-first national pay; no geographic differential applied.",
        "sources": "; ".join(srcs) + ("; " + extra if extra else ""),
    }

# ---------------------------------------------------------------- cost register
# (id, category, item, cost_type, driver, low, base, high, unit, pos, source, quality, notes)
R = []
def add(*a): R.append(a)

PER = "per year"
# personnel rows are generated from roles (see build)
add("CST-P14", "personnel", "Seasonal temporary grant processor (December peak), agency bill rate", "step-fixed", "per temp hour", 34, 39, 49, "USD/hour", "staffed administration",
    ONET.format(soc="43-3031") + " (median $24.36/h)", "D", "[D] BLS 43-3031 median hourly $24.36 x agency markup 1.4/1.6/2.0 [A]. Requires training and restricted permissions; cannot approve payments.")
add("CST-P16", "personnel", "Recruiting cost per hire", "step-fixed", "per hire", 1300, 15000, 45000, "USD/hire", "shared",
    "https://www.shrm.org/topics-tools/research/recruiting-benchmarking/full-data-brief", "C",
    "Low = SHRM 2026 median non-executive cost-per-hire $1,300 (search summary, not read); base [A] ~10% of $150k salary; high [A] agency fee 20-25% of senior salary.")
add("CST-P17", "personnel", "Laptop/equipment amortised", "fixed", "per FTE-year", 800, 1000, 1500, "USD/FTE-yr", "shared", "assumption", "D", "[A] 3-year refresh of managed laptop + peripherals.")
add("CST-P18", "personnel", "Remote work stipend (internet/home office)", "fixed", "per FTE-year", 0, 600, 1200, "USD/FTE-yr", "shared", "assumption", "D", "[A]")
add("CST-P19", "personnel", "Training / CPE / certifications", "fixed", "per FTE-year", 1000, 2000, 4000, "USD/FTE-yr", "shared", "assumption", "D", "[A] includes CPA CPE, security certs, accessibility training.")
add("CST-P21", "personnel", "PEO admin fee (Justworks PEO Basic $79/employee-month)", "fixed", "per employee-year", 216, 948, 1488, "USD/employee-yr", "shared",
    "https://justworks.com/pricing (403 to fetcher; figures from search results citing it)", "C",
    "Already INCLUDED in loaded cost (benefits). Do not add again. Low = payroll-only $8/employee-mo + share of $50 base [C]; high = PEO Plus $124 (conflicting $109 reported) [C].")
# contracted
add("CST-C01", "accounting", "Fractional CFO / controller review", "step-fixed", "per hour", 125, 200, 450, "USD/hour", "shared",
    "https://gofractional.com/insights/rates/cfo ; https://www.nerdwallet.com/business/software/learn/fractional-cfo", "C",
    "Search summaries: GoFractional observed average $174/h, IQR $125-200; NerdWallet $150-500/h, retainers $3k-10k/month. Not read directly.")
add("CST-C02", "accounting", "Outsourced bookkeeping / monthly close", "fixed", "per month", 1000, 2000, 4000, "USD/month", "shared", "assumption", "D",
    "[A] no public price list read. Preserves separation: outsourced books, controller reviews.")
add("CST-C03", "security-testing", "Fractional vCISO", "fixed", PER, 24000, 48000, 96000, "USD/yr", "software platform", "assumption", "D", "[A] ~4-16 h/month at $250-500/h; replaced by security engineer in Model C.")
add("CST-C04", "compliance", "Compliance consultant (sanctions program, due-diligence policy, annual independent review)", "fixed", PER, 10000, 25000, 50000, "USD/yr", "staffed administration", "assumption", "D", "[A] Replaced by compliance officer in Model C except independent review.")
add("CST-C05", "personnel", "Contracted engineering retainer (backup for sole technical lead)", "fixed", PER, 15000, 30000, 60000, "USD/yr", "software platform", "assumption", "D", "[A] Model A only; key-person mitigation, documented runbooks required.")
add("CST-C06", "legal", "Outside counsel (nonprofit/tax-exempt + financial services), hourly", "fixed", "per hour", 300, 450, 800, "USD/hour", "shared",
    "https://www.clio.com/blog/lawyer-statistics ; https://www.clio.com/state-rates-pages/", "C",
    "Clio average lawyer rate $349 (Jan 2025) and $362 (2026); corporate practice ~$461 (search summaries; Clio pages 403 to fetcher). Specialist exempt-org/financial-regulatory partners at national firms likely above $800 [A]. In-house lawyer comparator 23-1011 median $159,670.")
add("CST-C07", "legal", "Startup legal: formation, sponsor MSA/SLA templates, privacy, data processing, employment", "startup", "one-time", 40000, 80000, 150000, "USD", "shared", "assumption", "D", "[A]")
add("CST-C08", "legal", "Regulatory opinion: money transmission / agent-of-payee, state charitable solicitation, UPMIFA/agency boundary", "startup", "one-time", 15000, 40000, 100000, "USD", "staffed administration", "assumption", "D",
    "[A] Critical: if the servicer moves sponsor funds through its own accounts, state money-transmitter licensing could apply; designing payments to originate from sponsor-owned accounts avoids custody but must be confirmed by counsel.")
add("CST-C09", "assurance", "Independent audit of the company's own financial statements", "fixed", PER, 20000, 35000, 60000, "USD/yr", "shared", "assumption", "D", "[A] no public fee schedule; small private company audit. May be deferred to review engagement in year 1 if contracts allow.")
add("CST-C10", "accounting", "Corporate tax returns (federal + states)", "fixed", PER, 5000, 10000, 20000, "USD/yr", "shared", "assumption", "D", "[A] remote-first => multi-state payroll/nexus filings.")
add("CST-C11", "assurance", "SOC 2 Type 2 examination (CPA firm)", "fixed", PER, 15000, 35000, 70000, "USD/yr", "software platform",
    "https://soc2auditors.org/insights/soc-2-type-2-audit-cost/ ; https://drata.com/blog/soc-2-audit-cost", "C",
    "Vendor/directory content via search: specialist firms $15k-70k Type 2; Big Four $45k-430k. Excludes internal staff time.")
add("CST-C12", "assurance", "SOC 1 Type 2 examination (ICFR-relevant controls for sponsors' auditors)", "fixed", PER, 20000, 40000, 120000, "USD/yr", "staffed administration",
    "https://schellman.com/blog/what-does-a-soc-audit-cost ; https://thoropass.com/blog/soc-1-audit-cost-a-guide", "C",
    "Search summaries: Schellman baseline $29k-44k SOC 1 Type 2 (figure not visible in fetched text: chart), Thoropass $20k-120k. Combined SOC 1+2 from one firm often discounted [A 10-20%]. Staffed administration needs SOC 1; platform licensing needs SOC 2.")
add("CST-C13", "compliance", "SOC readiness assessment + gap remediation support", "startup", "one-time", 10000, 20000, 40000, "USD", "shared",
    "https://drata.com/blog/soc-2-audit-cost", "C", "Readiness $10k-25k cited in search summaries; remediation internal time excluded.")
add("CST-C14", "security-testing", "Annual external penetration test (web app, API, cloud) + retest", "fixed", PER, 10000, 20000, 35000, "USD/yr", "software platform",
    "https://www.blazeinfosec.com/post/how-much-does-penetration-testing-cost/ ; https://www.compassitc.com/blog/how-much-does-a-penetration-test-cost-for-a-small-business", "C",
    "Search summaries: $10k-35k standard commercial; small SaaS with APIs $15k-20k+. Payments + multi-tenant push to upper half.")
add("CST-C15", "compliance", "Compliance automation platform (Vanta/Drata class)", "fixed", PER, 8000, 20000, 40000, "USD/yr", "shared",
    "https://www.vanta.com/pricing ; https://www.drata.com/pricing", "D", "Prices NOT published (pages read 2026-11-25: demo/quote only). Range is [A].")
add("CST-C16", "incident-response", "Incident response retainer (often via cyber insurer panel)", "fixed", PER, 0, 7500, 25000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-C17", "incident-response", "Breach / fraud incident response and notification (event)", "extraordinary", "per incident", 50000, 250000, 1000000, "USD/incident", "shared", "assumption", "D", "[A] partly insurable; retention/deductible borne by company.")
add("CST-C18", "dr-bcp", "DR failover test + BCP tabletop facilitation", "fixed", PER, 5000, 10000, 25000, "USD/yr", "shared", "assumption", "D", "[A] plus internal time.")
# insurance
add("CST-I01", "insurance", "Cyber liability $1M limit, generic small business (benchmark only)", "fixed", PER, 999, 1740, 7500, "USD/yr", "shared",
    "https://www.moneygeek.com/insurance/business/cyber/cost/ ; https://windes.com/?p=61510", "C", "Search summaries; NOT adequate for a payments-adjacent servicer; shown to anchor the scale-up.")
add("CST-I02", "insurance", "Cyber liability (1st+3rd party) $5M, payments-adjacent SaaS", "fixed", PER, 15000, 30000, 60000, "USD/yr", "shared", "assumption", "D", "[A] sponsors likely require >=$5M; underwriting depends on controls (MFA, EDR, backups).")
add("CST-I03", "insurance", "Technology E&O / professional liability $5M", "fixed", PER, 10000, 25000, 50000, "USD/yr", "shared",
    "https://www.embroker.com/insurance-index/tech-business-insurance-index/", "C", "Embroker 2021 index (search summary): startup tech E&O avg $5,285 (<$1M revenue) to $16,679 (>=$5M revenue), limits unstated; scaled to $5M limit [A].")
add("CST-I04", "insurance", "D&O $1-2M", "fixed", PER, 5000, 10000, 20000, "USD/yr", "shared",
    "https://www.embroker.com/insurance-index/tech-business-insurance-index/", "C", "Embroker 2021: D&O average $4,782-$16,445 by stage (search summary).")
add("CST-I05", "insurance", "Commercial crime incl. third-party/client property, funds transfer fraud, social engineering", "fixed", PER, 5000, 12000, 30000, "USD/yr", "staffed administration", "assumption", "D",
    "[A] essential for payment-processing role even without custody; sub-limits for social engineering are often low.")
add("CST-I06", "insurance", "EPLI", "fixed", PER, 2000, 4000, 8000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-I07", "insurance", "General liability / umbrella", "fixed", PER, 1000, 3000, 8000, "USD/yr", "shared", "assumption", "D", "[A] workers comp in PEO/loaded cost.")
# technology
AZ = "https://prices.azure.com/api/retail/prices (Azure Database for PostgreSQL, eastus, retail consumption)"
add("CST-T01", "database", "Managed PostgreSQL primary, zone-redundant HA (Azure Flexible Server Ddsv5 2/4/8 vCore x2 for standby)", "fixed", PER, 3119, 6237, 12474, "USD/yr", "software platform",
    AZ, "A", "[D] $0.178/$0.356/$0.712 per hour x 8,760 h x 2 (HA standby billed as second instance [A on HA billing]). AWS RDS prices not extractable (JS-collapsed tables).")
add("CST-T02", "dr-bcp", "Cross-region PostgreSQL read replica for DR (same size, single instance)", "fixed", PER, 1559, 3119, 6237, "USD/yr", "software platform", AZ, "A", "[D] one instance of T01 size class.")
add("CST-T03", "database", "PostgreSQL provisioned storage", "variable", "per GB-month", 0.115, 0.115, 0.135, "USD/GB-month", "software platform", AZ, "A", "Premium SSD $0.115/GB-mo; Ultra $0.135.")
add("CST-T04", "database", "PostgreSQL backup storage (LRS)", "variable", "per GB-month", 0.095, 0.095, 0.2, "USD/GB-month", "software platform", AZ, "A", "Flexible Server backup LRS $0.095; Single Server GRS $0.20 used as geo-redundant high proxy.")
add("CST-T05", "cloud", "Application hosting, networking, WAF, KMS, object storage, egress (prod)", "fixed", PER, 12000, 24000, 60000, "USD/yr", "software platform", "assumption", "D", "[A] not priced line-by-line.")
add("CST-T06", "cloud", "Non-production environments (staging, test, sandbox per sponsor)", "step-fixed", PER, 3000, 8000, 20000, "USD/yr", "software platform", "assumption", "D", "[A]")
add("CST-T07", "cloud", "Infrastructure monitoring (Datadog Infra Pro)", "step-fixed", "per host-month", 15, 15, 18, "USD/host-month", "software platform", "https://www.datadoghq.com/pricing/", "A", "Annual $15, on-demand $18 'starting at'.")
add("CST-T08", "cloud", "APM (Datadog, with infra)", "step-fixed", "per host-month", 31, 31, 36, "USD/host-month", "software platform", "https://www.datadoghq.com/pricing/", "A", "")
add("CST-T09", "cloud", "Log ingest (Datadog)", "variable", "per GB", 0.10, 0.10, 0.10, "USD/GB", "software platform", "https://www.datadoghq.com/pricing/", "A", "")
add("CST-T10", "cloud", "Log indexing 15-day (Datadog)", "variable", "per million events-month", 1.70, 1.70, 2.55, "USD/M events", "software platform", "https://www.datadoghq.com/pricing/", "A", "Long-term audit log retention should go to cheap object storage/Flex ($0.05/M events).")
add("CST-T11", "software", "Security tooling (IdP/SSO, MDM, EDR, password manager, email security)", "fixed", "per FTE-year", 600, 1200, 2400, "USD/FTE-yr", "shared", "assumption", "D", "[A] vendor prices not read.")
add("CST-T12", "ai", "AI inference per grant screening call", "transaction", "per grant", 0.00065, 0.026, 0.14, "USD/grant", "software platform",
    "https://platform.claude.com/docs/en/about-claude/pricing", "A",
    "[D] low = Haiku 5.5 batch ($0.05/$0.25 per MTok) 8k in/1k out; base = Sonnet 5.5 standard ($2/$10) 8k/1k; high = Opus 5.5 standard ($4/$20) 20k/3k. OpenAI comparables gpt-6.1-sol $2/$10, gpt-6-luna $0.10/$0.50 (developers.openai.com pricing). Token counts are [A].")
add("CST-T13", "ai", "AI inference, all workflows (screening, donor support drafting, reconciliation triage, document extraction)", "variable", "per account-year", 0.10, 0.75, 4.00, "USD/account-yr", "software platform",
    "https://platform.claude.com/docs/en/about-claude/pricing", "D", "[A/D] 10 grants x T12 + contacts/exceptions; caching (0.05x on 5.5 models) and batch (50%) reduce. Model price cuts/rises are a sensitivity.")
add("CST-T14", "ai", "AI fixed: evaluation suites, red-teaming runs, development usage", "fixed", PER, 3000, 12000, 36000, "USD/yr", "software platform", "assumption", "D", "[A]")
# data / verification
add("CST-D01", "charity-verification", "IRS EO BMF extract (and TEOS bulk data incl. Pub 78/auto-revocation)", "fixed", PER, 0, 0, 0, "USD/yr", "software platform",
    "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf", "A", "Direct CSV downloads, no fee or login shown; data posting date 11/10/2026. Engineering to ingest is in personnel.")
add("CST-D02", "data", "OFAC Sanctions List Service (SDN + consolidated)", "fixed", PER, 0, 0, 0, "USD/yr", "staffed administration",
    "https://ofac.treasury.gov/sanctions-list-service", "A", "Downloads offered; no fee mentioned. Matching engine/false-positive review not included.")
add("CST-D03", "charity-verification", "Candid Charity Check API", "fixed", PER, 2750, 2750, 9900, "USD/yr (starting at)", "software platform",
    "https://candid.org/use-our-data/apis/", "B", "'Starting at $2,750'; term/volumes not published; high = Premier API starting at $9,900. Essentials $4,800; Nonprofit Eligibility $5,000.")
add("CST-D04", "charity-verification", "Candid Nonprofit Eligibility API", "fixed", PER, 5000, 5000, 15000, "USD/yr (starting at)", "software platform",
    "https://candid.org/use-our-data/apis/", "B", "'Starting at $5,000'; volume pricing unknown; high [A].")
add("CST-D05", "data", "Commercial sanctions/PEP/adverse-media screening subscription", "fixed", PER, 3000, 8000, 25000, "USD/yr", "staffed administration", "assumption", "D", "[A] no public price list read; OFAC-only screening is free but weaker on fuzzy matching and non-US lists.")
add("CST-ID1", "identity", "Persona Essential plan (500 services/month included)", "fixed", PER, 3000, 3000, 3000, "USD/yr", "software platform",
    "https://help.withpersona.com/articles/6oZbzp7jb7AWGClF5vpY3K/", "A", "$250/month on annual contract; unused services expire monthly. Whether servicer or sponsor performs donor identity verification is contract-specific.")
add("CST-ID2", "identity", "Identity verification overage per service", "transaction", "per verification", 1.00, 1.50, 3.00, "USD/verification", "software platform",
    "https://help.withpersona.com/articles/6oZbzp7jb7AWGClF5vpY3K/", "B", "$1.50 Essential overage (read); $1 startup-program figure (search, conflicting); high [A] for document+selfie+database bundles.")
# payments
add("CST-PY1", "payments", "ACH credit origination, next-day (grants out)", "transaction", "per payment", 0.10, 0.50, 0.50, "USD/payment", "staffed administration",
    "https://increase.com/pricing ; https://stripe.com/pricing", "A", "Increase $0.50; Stripe payouts $0.50 (first 50/month included). Low [A] bank-direct NACHA origination. If paid from sponsor's own bank account, cost is sponsor pass-through.")
add("CST-PY2", "payments", "ACH same-day origination", "transaction", "per payment", 1.00, 1.50, 2.00, "USD/payment", "staffed administration", "https://increase.com/pricing ; https://stripe.com/pricing", "A", "Stripe $1.00; Increase $2.00.")
add("CST-PY3", "payments", "Wire origination", "transaction", "per payment", 15, 20, 25, "USD/payment", "staffed administration", "https://increase.com/pricing ; https://stripe.com/pricing", "A", "Increase $15; Stripe Fedwire $25. International grants require separate equivalency/ER process (excluded).")
add("CST-PY4", "payments", "RTP / FedNow origination", "transaction", "per payment", 2.50, 2.50, 2.50, "USD/payment", "staffed administration", "https://increase.com/pricing", "A", "")
add("CST-PY5", "check-printing", "Check printing and mailing", "transaction", "per check", 1.04, 3.00, 8.00, "USD/check", "staffed administration",
    "https://increase.com/pricing ; https://www.lob.com/pricing/print-mail", "A", "Increase $3.00/check (+$1/extra page); Lob 'starting at' $1.04 (Startup/Growth plan) or $1.19 (Developer). High [A] incl. stop-pay, reissue, positive-pay handling (Unbound PREG $2-8).")
add("CST-PY6", "check-printing", "Lob plan fee (if Lob used)", "fixed", PER, 0, 3120, 6600, "USD/yr", "staffed administration", "https://www.lob.com/pricing/print-mail", "A", "Developer $0 (<=6,000 mailings), Startup $260/mo, Growth $550/mo.")
add("CST-PY7", "payments", "ACH return / exception handling (fees + staff time)", "transaction", "per return", 2, 5, 15, "USD/return", "staffed administration", UNB_PARAMS + " (ach_return_rate source note BNK:121)", "D", "Illustrative $2-5 + 10-20 min per return per Unbound; time valued separately at ops loaded rate.")
add("CST-PY8", "payments", "Bank treasury services (positive pay, ACH filters, account analysis)", "fixed", "per month", 100, 300, 1000, "USD/month", "staffed administration", "assumption", "D", "[A]")
add("CST-PY9", "payments", "Incoming check lockbox processing", "transaction", "per check", 0.65, 0.65, 1.50, "USD/check", "staffed administration", UNB_PARAMS + " (lockbox_check_cost [S] Sunwest)", "B", "Repo-sourced; high [A].")
add("CST-PY10", "payments", "Card/ACH debit contribution acceptance (Stripe ACH 0.8% capped $5)", "pass-through", "per contribution", 0, 5, 5, "USD/contribution", "shared", "https://stripe.com/pricing", "A",
    "Normally borne by sponsor/donor contribution flow; NOT servicer opex unless contract says so. Card 2.9%+$0.30.")
add("CST-PY11", "payments", "Modern Treasury payment operations platform", "fixed", PER, 0, 0, 0, "USD/yr", "staffed administration", "https://www.moderntreasury.com/pricing", "D", "No public prices (quote only). Not budgeted; Increase/bank-direct used as reference.")
# comms / docs
add("CST-CM1", "software", "Transactional email (Postmark Pro, 10k/month incl.)", "variable", "per month + per 1,000 over", 16.50, 16.50, 18.00, "USD/month", "software platform", "https://postmarkapp.com/pricing", "A", "Overage $1.30/1,000 (Pro). Negligible per account.")
add("CST-CM2", "software", "SMS (Twilio US outbound incl. carrier fee)", "transaction", "per segment", 0.0118, 0.0128, 0.0133, "USD/segment", "software platform", "https://www.twilio.com/en-us/sms/pricing/us", "A", "$0.0083 + carrier $0.0035-0.005.")
add("CST-CM3", "software", "Paper statements / tax receipts (Lob first-class letter)", "transaction", "per piece", 0.628, 0.658, 0.828, "USD/piece", "staffed administration", "https://www.lob.com/pricing/print-mail", "A", "'Starting at' per-piece rates by plan.")
add("CST-CM4", "software", "E-signature", "fixed", PER, 600, 3000, 10000, "USD/yr", "shared", "assumption", "D", "[A] vendor pricing not read.")
add("CST-CM5", "software", "Document generation (statements, receipts, reports)", "fixed", PER, 0, 2000, 10000, "USD/yr", "software platform", "assumption", "D", "[A] open-source PDF generation possible.")
# business SaaS
add("CST-S01", "software", "Google Workspace Business Standard", "fixed", "per user-year", 168, 168, 202, "USD/user-yr", "shared",
    "https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans", "C", "$14/user-mo annual, $16.80 flexible (search summary citing Google help pages; pricing page values not rendered to fetcher).")
add("CST-S02", "software", "Slack (Pro / Business+)", "fixed", "per user-year", 87, 87, 180, "USD/user-yr", "shared", "https://slack.com/pricing", "A", "$7.25 / $15 per user-month annual.")
add("CST-S03", "software", "GitHub (Team / Enterprise)", "fixed", "per user-year", 48, 48, 252, "USD/user-yr", "software platform", "https://github.com/pricing", "A", "$4 / $21 per user-month.")
add("CST-S04", "software", "AI assistant seats (ChatGPT Standard/Premium class; Claude plans comparable)", "fixed", "per user-year", 240, 240, 1200, "USD/user-yr", "shared", "https://openai.com/api/pricing/", "A", "Standard seat $20/mo annual; Premium $100/mo annual (page read).")
add("CST-S05", "software", "Other per-user SaaS (video, docs/wiki, project tracking, password vault)", "fixed", "per user-year", 600, 1200, 2400, "USD/user-yr", "shared", "assumption", "D", "[A]")
add("CST-S06", "accounting", "Accounting / expense / bill-pay software (company books)", "fixed", PER, 1500, 3000, 6000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-S07", "support", "Helpdesk / ticketing", "fixed", "per agent-year", 300, 600, 1500, "USD/agent-yr", "staffed administration", "assumption", "D", "[A]")
add("CST-S08", "sales", "CRM", "fixed", PER, 500, 2000, 6000, "USD/yr", "shared", "assumption", "D", "[A]")
# sales/marketing/travel/g&a
add("CST-SM1", "sales", "Sponsor-facing conferences, travel, events", "fixed", PER, 15000, 40000, 80000, "USD/yr", "shared", BUDGET + ":26", "D", "[A] existing $40k retained as base.")
add("CST-SM2", "marketing", "Marketing, website, content, brand", "fixed", PER, 5000, 20000, 60000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-SM3", "sales", "Sales commission on first-year contract value", "variable", "percent of first-year revenue", 0.05, 0.10, 0.15, "share", "shared", "assumption", "D", "[A] only when a sales hire exists.")
add("CST-TR1", "travel", "Team travel / in-person offsites (remote-first)", "fixed", "per FTE-year", 1500, 3000, 5000, "USD/FTE-yr", "shared", "assumption", "D", "[A]")
add("CST-G01", "g&a", "Corporate filings, registered agents, franchise taxes, multi-state registrations", "fixed", PER, 1000, 3000, 8000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-G02", "g&a", "Operating bank fees", "fixed", PER, 0, 1200, 3600, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-G03", "g&a", "Co-working / meeting space", "fixed", PER, 0, 6000, 24000, "USD/yr", "shared", "assumption", "D", "[A]")
add("CST-G04", "g&a", "Contingency / risk reserve on cash opex", "fixed", "percent of cash opex", 0.05, 0.075, 0.10, "share", "shared", "assumption", "D", "[A]")
# startup
add("CST-ST1", "g&a", "Incorporation, EIN, initial state filings", "startup", "one-time", 500, 2000, 5000, "USD", "shared", "assumption", "D", "[A]")
add("CST-ST2", "marketing", "Brand, website, sales collateral", "startup", "one-time", 5000, 15000, 40000, "USD", "shared", "assumption", "D", "[A]")
add("CST-ST3", "migration", "Implementation/migration tooling (ETL, mapping, parallel-run & reconciliation harness)", "startup", "one-time", 10000, 40000, 120000, "USD", "staffed administration", "assumption", "D", "[A] excl. staff time.")
add("CST-ST4", "insurance", "Insurance binding: first-year premiums/deposits paid upfront", "startup", "one-time (timing)", 0.25, 0.5, 1.0, "share of annual premium", "shared", "assumption", "D", "[A] cash timing only; not additional economic cost.")
add("CST-ST5", "other", "Working capital: fees billed quarterly in arrears on average AUA", "startup", "months of fixed cash opex", 2, 3, 4, "months", "shared", "assumption", "D", "[A]")
# customer-specific
add("CST-OM1", "onboarding", "Sponsor onboarding & configuration (contract, controls mapping, training, bridge letters)", "customer-specific", "per sponsor", 10000, 30000, 75000, "USD/sponsor", "staffed administration", "assumption", "D", "[A] mostly staff time at loaded rates.")
add("CST-OM2", "migration", "Sponsor data migration incl. parallel run and reconciliation", "customer-specific", "per sponsor", 25000, 75000, 250000, "USD/sponsor", "staffed administration", "assumption", "D", "[A] scales with accounts, history, open grants, data quality.")
add("CST-SR1", "other", "Sponsor-retained reserved decisions (grant approval, variance power, complex assets)", "sponsor-retained", "per account-year", 42, 43, 43, "USD/account-yr", "staffed administration", UNB_05A + ":383-393", "B",
    "Unbound 05a section 8 estimate (model output, not observed). NOT a servicer cost; listed to prevent double counting.")
add("CST-PT1", "other", "Grant principal, investment management fees, donor-facing admin fees", "pass-through", "n/a", 0, 0, 0, "USD", "shared", "brief rule", "D", "Excluded from servicer P&L entirely.")

# ---------------------------------------------------------------- staffing models
# (model, key, fte, cash_salary_or_None, responsibilities, authority, sod, backup, seasonal, trigger)
MODELS = {
 "A": ("Model A founder-led (3 core + fractional + contractors + automation)", [
   ("ceo", 1, 90000, "Sponsor relationships, sales, contracts, governance, vendor management, people", "Approves company spend >$10k; second approver on payment batches; signs sponsor contracts; cannot edit payee master data", "ctrl prepares payment batch / ceo approves; sponsor approves reserved decisions", "Fractional CFO for finance escalation; no sales backup", "Covers 1st-line approvals daily in December", "Hire sales director when >2 active RFPs or pipeline >$1B AUA"),
   ("cto", 1, 100000, "Platform build/run, security, DR, AI controls, SOC 2 control owner", "Production change approval (with PR review by retainer engineer); no bank or payment-release access", "Code author / independent reviewer (contract engineer); infra admin / access reviewer (fractional vCISO)", "Contract engineering retainer CST-C05; runbooks", "On-call; change freeze 15 Dec-5 Jan", "Hire senior engineer when >1 sponsor integration in flight or on-call >1 incident/week"),
   ("ctrl", 1, None, "Grant & finance operations lead: payment preparation, reconciliation, charity verification exceptions, company books review", "Prepares and releases payments only after CEO approval; reconciles; cannot approve own adjustments", "Prepares / CEO approves; outsourced bookkeeper records / ctrl reviews; fractional CFO reviews ctrl", "CEO (limited) + seasonal temp; UNACCEPTABLE single point of failure for daily ops above ~2k accounts", "Supervises 2 temps for 4 weeks", "Hire ops specialist at >1,500 accounts or >40 grants/business day sustained or 2nd sponsor"),
  ], {"CST-C01": 96, "CST-C02": 12, "CST-C03": 1, "CST-C04": 1, "CST-C05": 1, "CST-P14": 320, "CST-C06": 60}),
 "B": ("Model B lean independent (5 core)", [
   ("ceo", 1, None, "Sponsor relationships, sales, contracts, governance, people", "Company spend; contract signature; second approver for exceptional payments", "Exceptional payment approval with ctrl", "Controller for vendor/admin matters", "Approver pool in December", "Hire sales director at 3+ sponsors or pipeline >$2B"),
   ("cto", 1, None, "Architecture, security, DR, AI controls, SOC 2 owner", "Production change approval; no bank access", "Author/reviewer with swe", "SWE (mutual backup)", "Change freeze", "Hire security engineer when SOC 2 + SOC 1 both in scope or >3 sponsors"),
   ("swe", 1, None, "Integrations (sponsor, custodian, bank files), ledger, testing, support tooling", "Merge after review; no production data access without ticket", "Author/reviewer with cto", "CTO", "Second on-call", "Second engineer at >2 concurrent migrations"),
   ("ctrl", 1, None, "Financial operations: payment release, reconciliation, close, SOC 1 control owner, company finance", "Releases payment batches prepared by ops; approves adjustments prepared by others", "ops prepares / ctrl releases; bookkeeper records / ctrl reviews; ceo approves ctrl's own items", "Ops specialist for preparation only; CFO retainer", "Daily release windows", "Fund accountant at >5,000 accounts or >3 bank/custodian relationships"),
   ("ops", 1, None, "Grant processing, charity verification, donor/advisor service, exceptions", "Prepares payments; verifies charities; cannot release", "Prepares / ctrl releases", "Seasonal temps + ctrl (prep only). WEAK: ctrl backing ops collapses SoD on the same item", "Leads 3 temps x 4 weeks", "2nd ops specialist at >2,500 accounts or >60 grants/day or any absence >2 weeks"),
  ], {"CST-C01": 40, "CST-C02": 12, "CST-C03": 1, "CST-C04": 1, "CST-P14": 480, "CST-C06": 100}),
 "C": ("Model C established (12 core, specialization, redundancy)", [
   ("ceo", 1, None, "Strategy, sponsors, governance", "Company spend; contracts", "Exceptional approvals with ctrl", "COO-equivalent: grant ops manager for operations", "", "Sales director at pipeline >$3B or >5 RFPs/yr"),
   ("cto", 1, None, "Architecture, engineering management, AI governance", "Change approval", "Author/reviewer", "Security engineer + SWE", "", ""),
   ("swe", 2, None, "Product, integrations, migrations tooling", "Merge after review", "Mutual review", "Each other", "On-call rota", "+1 per 3 concurrent sponsor integrations"),
   ("sec", 1, None, "IAM, logging, vulnerability mgmt, IR lead, DR tests", "Access grants (approved by managers); no payment access", "Access grant / quarterly review by compliance", "CTO", "", ""),
   ("ctrl", 1, None, "Finance + SOC 1 owner, payment release", "Releases batches", "ops prepares / ctrl or gopsm releases", "Grant ops manager (release) + fund accountant", "", ""),
   ("acct", 1, None, "Reconciliations, close, sponsor fee billing", "Posts entries for review", "Prepares / ctrl approves", "Controller", "", "+1 at >15,000 accounts"),
   ("gopsm", 1, None, "Grant operations management, SLA, exceptions, temps", "Releases payments (alternate to ctrl); escalates to sponsor", "Alternate releaser", "Controller", "Runs December plan", ""),
   ("ops", 2, None, "Grant processing, verification, donor service", "Prepare only", "Prepare / release by ctrl or gopsm", "Each other + temps", "4 temps x 5 weeks", "+1 per ~2,500-4,000 accounts (activity-dependent)"),
   ("comp", 1, None, "Sanctions, charity due diligence policy, SOC liaison, complaints", "Clears/escalates screening hits; no payment release", "Screens / ops processes; tests controls independently", "Grant ops manager (temporary, documented)", "", ""),
   ("impl", 1, None, "Sponsor onboarding, migration, training", "Configuration changes with sponsor sign-off", "Configures / CTO or comp reviews", "Grant ops manager", "", "+1 per 2 concurrent onboardings"),
  ], {"CST-C01": 0, "CST-C02": 0, "CST-C03": 0, "CST-C04": 0.4, "CST-P14": 640, "CST-C06": 160}),
}

# Non-personnel fixed quantity per model: id -> (A, B, C); 'fte' means multiply by core headcount
NP = {
  "CST-C09": (1, 1, 1), "CST-C10": (1, 1, 1), "CST-C11": (1, 1, 1), "CST-C12": (1, 1, 1), "CST-C14": (1, 1, 1),
  "CST-C15": (1, 1, 1), "CST-C16": (1, 1, 1), "CST-C18": (1, 1, 1),
  "CST-I02": (1, 1, 1), "CST-I03": (1, 1, 1), "CST-I04": (1, 1, 1), "CST-I05": (1, 1, 1), "CST-I06": (1, 1, 1), "CST-I07": (1, 1, 1),
  "CST-T01": (1, 1, 1), "CST-T02": (1, 1, 1), "CST-T03": (256*3*12, 512*3*12, 1024*3*12), "CST-T04": (512*12, 1024*12, 2048*12),
  "CST-T05": (1, 1, 1.5), "CST-T06": (1, 1, 1.5), "CST-T07": (6*12, 8*12, 12*12), "CST-T08": (4*12, 6*12, 8*12),
  "CST-T09": (300*12, 500*12, 1000*12), "CST-T10": (20*12, 40*12, 80*12), "CST-T11": ("fte", "fte", "fte"), "CST-T14": (1, 1, 1),
  "CST-D03": (1, 1, 1), "CST-D05": (1, 1, 1), "CST-ID1": (1, 1, 1), "CST-PY8": (12, 12, 12),
  "CST-CM1": (12, 12, 12), "CST-CM4": (1, 1, 1), "CST-CM5": (1, 1, 1),
  "CST-S01": ("fte", "fte", "fte"), "CST-S02": ("fte", "fte", "fte"), "CST-S03": (3, 3, 5), "CST-S04": ("fte", "fte", "fte"), "CST-S05": ("fte", "fte", "fte"),
  "CST-S06": (1, 1, 1), "CST-S07": (2, 2, 4), "CST-S08": (1, 1, 1),
  "CST-SM1": (0.6, 1, 2), "CST-SM2": (0.5, 1, 2.5), "CST-TR1": ("fte", "fte", "fte"),
  "CST-G01": (1, 1, 1.5), "CST-G02": (1, 1, 1), "CST-G03": (0.5, 1, 2),
  "CST-P17": ("fte", "fte", "fte"), "CST-P18": ("fte", "fte", "fte"), "CST-P19": ("fte", "fte", "fte"),
  "CST-P16": ("turnover", "turnover", "turnover"),
}
TURNOVER = 0.15  # [A] annual replacement hires per FTE

def reg_index():
    return {r[0]: r for r in R}

def model_fte(m):
    return sum(x[1] for x in MODELS[m][1])

def np_lines(m, idx):
    i = "ABC".index(m)
    fte = model_fte(m)
    out = []
    items = {**{k: v[i] for k, v in NP.items()}, **MODELS[m][2]}
    for cid, qty in items.items():
        if qty is None or qty == 0:
            continue
        qty = fte if qty == "fte" else (TURNOVER * fte if qty == "turnover" else qty)
        r = idx[cid]
        out.append({"cost_id": cid, "category": r[1], "item": r[2], "qty": qty, "unit": r[8], "pos": r[9],
                    "low": qty * r[5], "base": qty * r[6], "high": qty * r[7]})
    return out

def personnel_lines(m, roles):
    out = []
    for key, fte, cash, resp, auth, sod, backup, seasonal, trig in MODELS[m][1]:
        ro = roles[key]
        sal = ro["chosen_base_salary_base"]
        tax = employer_taxes(sal, BURDEN["base"]); ben = benefits(sal, BURDEN["base"])
        cash_sal = sal if cash is None else cash
        cash_loaded = loaded(cash_sal, BURDEN["base"])
        out.append({"key": key, "role": ro["role"], "fte": fte, "salary": sal, "tax": tax, "ben": ben,
                    "econ": fte * (sal + tax + ben), "cash": fte * cash_loaded, "cash_salary": cash_sal,
                    "low": fte * ro["loaded_cost_low"], "high": fte * ro["loaded_cost_high"],
                    "resp": resp, "auth": auth, "sod": sod, "backup": backup, "seasonal": seasonal, "trig": trig, "pos": ro["platform_or_staffed"]})
    return out

def model_totals(m, roles, idx):
    P = personnel_lines(m, roles)
    N = np_lines(m, idx)
    pers_econ = sum(p["econ"] for p in P); pers_cash = sum(p["cash"] for p in P)
    np_base = sum(n["base"] for n in N); np_low = sum(n["low"] for n in N); np_high = sum(n["high"] for n in N)
    cont = idx["CST-G04"]
    cash_sub = pers_cash + np_base
    econ_sub = pers_econ + np_base
    return {"P": P, "N": N, "pers_econ": pers_econ, "pers_cash": pers_cash, "pers_low": sum(p["low"] for p in P), "pers_high": sum(p["high"] for p in P),
            "np_low": np_low, "np_base": np_base, "np_high": np_high,
            "cont_base": cont[6] * cash_sub, "cash_total": cash_sub * (1 + cont[6]), "econ_total": econ_sub * (1 + cont[6]),
            "low_total": (sum(p["low"] for p in P) + np_low) * (1 + cont[5]),
            "high_total": (sum(p["high"] for p in P) + np_high) * (1 + cont[7]),
            "fte": model_fte(m)}

# ---------------------------------------------------------------- helpers
def fmt(x):
    return f"{x:,.0f}"

def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(r)

def main(wjson, out):
    raw = json.load(open(wjson))
    wages = {r["soc"]: {"title": r["title"].replace(" Bright Outlook &nbsp;", "").strip(), "p": r["p10_p25_p50_p75_p90"]} for r in raw}
    roles = {r[0]: role_row(r, wages) for r in ROLES}
    # personnel register rows
    pers_rows = [(f"CST-P{n:02d}", "personnel", f"Loaded cost: {ro['role']}", "fixed" if k in ("ceo", "cto", "ctrl") else "step-fixed", "per FTE-year",
                  ro["loaded_cost_low"], ro["loaded_cost_base"], ro["loaded_cost_high"], "USD/FTE-yr", ro["platform_or_staffed"],
                  ONET.format(soc=ro["soc_code"].split("|")[0]) + " ; " + ECEC_T04 + " ; " + KFF, "B",
                  f"[D] salary {fmt(ro['chosen_base_salary_low'])}/{fmt(ro['chosen_base_salary_base'])}/{fmt(ro['chosen_base_salary_high'])} x burden (base {ro['burden_multiplier']}); see role-compensation.csv")
                 for n, (k, ro) in enumerate(roles.items(), start=1)]
    pers_rows = [(r[0].replace("CST-P", "CST-R"),) + r[1:] for r in pers_rows]  # R = role rows, avoid clash with P14+ ids
    V01 = ("CST-V01", "support", "Incremental operations labour, loaded rate (grant & client ops specialist)", "variable", "per hour",
           round(roles["ops"]["loaded_cost_low"] / PROD_HOURS["high"], 2), roles["ops"]["loaded_hourly_rate"], round(roles["ops"]["loaded_cost_high"] / PROD_HOURS["low"], 2),
           "USD/hour", "staffed administration", ONET.format(soc="13-2099") + " ; " + ECEC_T04, "D",
           "[D] vs existing $50/h placeholder (" + BUDGET + ":34). $40/account buys " + f"{40/roles['ops']['loaded_hourly_rate']*60:.0f}" + " min at base rate, not 48.")
    allrows = pers_rows + [V01] + R
    idx = {r[0]: r for r in allrows}
    hdr = ["cost_id", "category", "item", "cost_type", "driver", "unit_cost_low", "unit_cost_base", "unit_cost_high", "unit", "platform_or_staffed", "source_url_or_path", "quality", "notes"]
    write_csv(os.path.join(out, "cost-register.csv"), hdr, allrows)

    rc_hdr = ["role", "soc_code", "occupation_title", "bls_median_annual", "p25", "p75", "period", "chosen_base_salary_low", "chosen_base_salary_base", "chosen_base_salary_high",
              "salary_reason", "employer_taxes_base", "benefits_base", "burden_multiplier", "ecec_benchmark_multiplier", "ecec_group", "loaded_cost_low", "loaded_cost_base", "loaded_cost_high",
              "productive_hours", "loaded_hourly_rate", "loaded_hourly_range", "qualifications", "platform_or_staffed", "notes", "sources"]
    write_csv(os.path.join(out, "role-compensation.csv"), rc_hdr, [[ro[h] for h in rc_hdr] for ro in roles.values()])

    T = {m: model_totals(m, roles, idx) for m in "ABC"}
    sm_hdr = ["model", "row_type", "role_or_item", "responsibilities", "fte", "base_salary", "employer_taxes", "benefits", "loaded_cost_economic", "cash_salary", "loaded_cost_cash",
              "loaded_low", "loaded_high", "decision_authority", "separation_of_duties", "backup_coverage", "seasonal_december", "hiring_trigger", "platform_or_staffed", "notes"]
    sm_rows = []
    for m in "ABC":
        t = T[m]; name = MODELS[m][0]
        for p in t["P"]:
            note = "Founder market-rate shown as economic cost; cash salary below market [A]" if p["cash_salary"] != p["salary"] else ""
            sm_rows.append([name, "core", p["role"], p["resp"], p["fte"], p["salary"], round(p["fte"] * p["tax"]), round(p["fte"] * p["ben"]), round(p["econ"]), p["cash_salary"], round(p["cash"]),
                            round(p["low"]), round(p["high"]), p["auth"], p["sod"], p["backup"], p["seasonal"], p["trig"], p["pos"], note])
        for n in t["N"]:
            if n["category"] in ("personnel", "accounting", "legal", "compliance", "security-testing", "assurance") and n["cost_id"] in ("CST-C01", "CST-C02", "CST-C03", "CST-C04", "CST-C05", "CST-P14", "CST-C06", "CST-C09", "CST-C10", "CST-C11", "CST-C12", "CST-C14"):
                sm_rows.append([name, "contracted", f"{n['cost_id']} {n['item']}", "", "", "", "", "", round(n["base"]), "", round(n["base"]), round(n["low"]), round(n["high"]), "", "", "", "", "", n["pos"], f"qty {n['qty']:g} x {n['unit']}"])
        sm_rows.append([name, "summary", "Personnel subtotal", "", t["fte"], "", "", "", round(t["pers_econ"]), "", round(t["pers_cash"]), round(t["pers_low"]), round(t["pers_high"]), "", "", "", "", "", "", "core FTE only"])
        sm_rows.append([name, "summary", "Non-personnel + contracted subtotal", "", "", "", "", "", round(t["np_base"]), "", round(t["np_base"]), round(t["np_low"]), round(t["np_high"]), "", "", "", "", "", "", "see report for line detail"])
        sm_rows.append([name, "summary", "Contingency 7.5% (5-10%)", "", "", "", "", "", round(t["econ_total"] - (t["pers_econ"] + t["np_base"])), "", round(t["cont_base"]), "", "", "", "", "", "", "", "", ""])
        sm_rows.append([name, "summary", "TOTAL annual fixed operating cost (excl. variable, startup, customer-specific)", "", t["fte"], "", "", "", round(t["econ_total"]), "", round(t["cash_total"]), round(t["low_total"]), round(t["high_total"]), "", "", "", "", "", "", "economic = founders at market; cash = founder cash salaries"])
    BC = {"A": "Minimum: sponsor-approved payment release with 2 people + sponsor; documented runbooks; contract engineer with tested access; DR replica; RTO 24h/RPO 15m [A]; key-person insurance or escrowed credentials; written succession for each founder.",
          "B": "As A plus: mutual engineering backup; controller absence plan (CEO+fractional CFO release with sponsor co-approval); DR test annually; RTO 8h/RPO 5m [A].",
          "C": "Two people able to release payments; 24x7 on-call rota; quarterly DR/IR drills; RTO 4h/RPO <5m [A]; documented cross-training matrix."}
    for m in "ABC":
        sm_rows.append([MODELS[m][0], "continuity", "Business-continuity requirements", BC[m]] + [""] * 16)
    MO = {"A": "CEO ~25% on management/admin; CTO ~10%; ctrl ~10% supervising temps [A]",
          "B": "~0.5 FTE equivalent across CEO/CTO/ctrl on management, hiring, audits [A]",
          "C": "~1.3 FTE equivalent (CEO, CTO, gopsm, ctrl management time) [A]; supervision ratio ~1:5"}
    for m in "ABC":
        sm_rows.append([MODELS[m][0], "management-overhead", "Management overhead", MO[m]] + [""] * 16)
    write_csv(os.path.join(out, "staffing-models.csv"), sm_hdr, sm_rows)
    return wages, roles, T, idx, allrows

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
