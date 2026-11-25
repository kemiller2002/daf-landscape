"""Emit evidence.jsonl, assumptions.jsonl, report.jsonl for CST. Run: python3 -I -B report.py <scriptsdir> <outdir>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import build as B

OUT = sys.argv[2]
wages, roles, T, idx, rows = B.main(os.path.join(sys.argv[1], "wages.json"), OUT)
f = B.fmt
ACC = B.ACC

# ------------------------------------------------------------------ evidence
EV = []
def ev(claim, value, unit, src, stype, period, q, notes=""):
    EV.append({"evidence_id": f"EV-CST-{len(EV)+1:03d}", "claim": claim, "value": value, "unit": unit, "source_url_or_path": src,
               "source_type": stype, "filing_period": period, "accessed": ACC, "quality": q, "notes": notes})
    return EV[-1]["evidence_id"]

soc_ev = {}
for soc, w in sorted(wages.items()):
    soc_ev[soc] = ev(f"National wage percentiles p10/p25/p50/p75/p90, SOC {soc} {w['title']}", "/".join(str(x) for x in w["p"]), "USD/yr",
                     B.ONET.format(soc=soc), "BLS", "OEWS May 2025 (national, all industries)", "B",
                     "BLS OEWS data republished by DOL O*NET OnLine ('Source: Bureau of Labor Statistics 2025 wage data'); bls.gov tables and API were blocked/throttled for this client (403 / daily threshold).")
ec = {}
for grp, e in B.ECEC.items():
    src = B.ECEC_T06 if "Establishments" in grp else B.ECEC_T04
    ec[grp] = ev(f"ECEC private industry {grp}: wages, paid leave, supplemental, insurance, retirement, legally required ($/hour worked); total comp",
                 f"w={e['w']} pl={e['pl']} sup={e['sup']} ins={e['ins']} ret={e['ret']} leg={e['leg']} tot={e['tot']}", "USD/hour worked", src, "BLS", "June 2026 (released 2026-09-09)", "A")
EVX = {}
EVX["ecec_head"] = ev("ECEC private industry: wages 70.0% / benefits 30.0% of compensation; total $46.89/h", "70.0/30.0", "% of total compensation", B.ECEC_NR, "BLS", "June 2026", "A")
EVX["kff_family"] = ev("Average annual family premium employer-sponsored coverage; worker contribution", "26993; 6850", "USD/yr", B.KFF, "other", "KFF EHBS 2025 (released 2025-10-22)", "B", "Survey of firms with 10+ workers.")
EVX["kff_single"] = ev("Average single premium; worker contribution", "9325; 1440", "USD/yr", "https://www.kff.org/health-costs/2025-employer-health-benefits-survey/", "other", "KFF EHBS 2025", "C", "Figures from search result summary of KFF pages; family figures read directly.")
EVX["ss"] = ev("2026 OASDI contribution and benefit base", "184500", "USD", "https://www.journalofaccountancy.com/news/2025/oct/social-security-wage-base-and-cola-announced-for-2026/", "press", "2026", "C", "ssa.gov/oact/cola/cbb.html returned 403 to fetcher; value consistent across search results.")
EVX["anth"] = ev("Claude API prices per MTok input/output: Opus 5.5 $4/$20; Sonnet 5.5 $2/$10; Haiku 5.5 $0.10/$0.50 (<=100k prompt); batch -50%; cache hit 0.05x on 5.5 models; US-only inference 1.1x", "see claim", "USD/MTok", "https://platform.claude.com/docs/en/about-claude/pricing", "price-list", "current at access", "A")
EVX["oai"] = ev("OpenAI API standard prices per 1M tokens: gpt-6.2-sol $2/$10; gpt-6.1-terra $1/$5; gpt-6-luna $0.10/$0.50; batch -50%", "see claim", "USD/MTok", "https://developers.openai.com/api/docs/pricing", "price-list", "current at access", "A")
EVX["oai_seat"] = ev("ChatGPT business seat: Standard $20/month annual; Premium $100/month annual", "20; 100", "USD/user-month", "https://openai.com/api/pricing/", "price-list", "current at access", "A")
EVX["az"] = ev("Azure Database for PostgreSQL Flexible Server (eastus, retail): Ddsv5 2/4/8 vCore $0.178/$0.356/$0.712 per hour; storage $0.115/GB-mo; backup LRS $0.095/GB-mo", "see claim", "USD", "https://prices.azure.com/api/retail/prices", "price-list", "retail API at access", "A", "Official Azure Retail Prices API JSON.")
EVX["aws"] = ev("AWS RDS for PostgreSQL instance/storage prices", "not extracted", "", "https://aws.amazon.com/rds/postgresql/pricing/", "price-list", "", "D", "Tables collapsed behind JS; only snapshot-export example $0.013/GB visible. Gap.")
EVX["stripe"] = ev("Stripe: ACH debit 0.8% cap $5; payouts ACH next-day $0.50, same-day $1.00 (first 50/month included); Fedwire $25; RTP $2.50; card 2.9%+$0.30", "see claim", "USD", "https://stripe.com/pricing", "price-list", "current", "A")
EVX["increase"] = ev("Increase: ACH next-day $0.50, same-day $2.00; wire $15; RTP/FedNow $2.50; check print+mail $3.00 (+$1/page); monthly fees by use case (sales)", "see claim", "USD", "https://increase.com/pricing", "price-list", "current", "A")
EVX["lob"] = ev("Lob: plans $0/$260/$550 per month; checks from $1.19/$1.04/$1.04; first-class letters from $0.828/$0.658/$0.628", "see claim", "USD", "https://www.lob.com/pricing/print-mail", "price-list", "current", "A", "'Starting at' rates.")
EVX["mt"] = ev("Modern Treasury publishes no prices (usage-based, quote)", "n/a", "", "https://www.moderntreasury.com/pricing", "vendor-site", "current", "A")
EVX["persona"] = ev("Persona Essential plan $250/month annual contract, 500 services/month, $1.50 per additional service; Growth/Enterprise custom", "250; 1.50", "USD", "https://help.withpersona.com/articles/6oZbzp7jb7AWGClF5vpY3K/", "price-list", "current", "A", "withpersona.com/pricing returned 403.")
EVX["candid"] = ev("Candid API starting prices: Charity Check $2,750; Essentials $4,800; Premier $9,900; Nonprofit Eligibility $5,000; Grants $6,000; News $3,300; Demographics/Taxonomy no fee", "see claim", "USD (term not stated)", "https://candid.org/use-our-data/apis/", "price-list", "current", "B", "Term and call volume not published.")
EVX["irs"] = ev("IRS EO BMF extract offered as direct CSV downloads; posting date 11/10/2026", "free download (no fee shown)", "", "https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf", "other", "2026-11", "A")
EVX["ofac"] = ev("OFAC Sanctions List Service: lists ready for immediate download; no fee mentioned", "free (no fee shown)", "", "https://ofac.treasury.gov/sanctions-list-service", "other", "current", "A")
EVX["vanta"] = ev("Vanta and Drata do not publish prices (demo/quote)", "n/a", "", "https://www.vanta.com/pricing ; https://www.drata.com/pricing", "vendor-site", "current", "A")
EVX["gh"] = ev("GitHub Team $4, Enterprise $21 per user-month", "4; 21", "USD/user-month", "https://github.com/pricing", "price-list", "current", "A")
EVX["slack"] = ev("Slack Pro $7.25, Business+ $15 per user-month annual", "7.25; 15", "USD/user-month", "https://slack.com/pricing", "price-list", "current", "A")
EVX["gws"] = ev("Google Workspace Business Standard $14/user-month annual, $16.80 flexible", "14; 16.80", "USD/user-month", "https://knowledge.workspace.google.com/admin/billing/compare-flexible-and-annual-fixed-term-payment-plans", "vendor-site", "2026", "C", "From search summary; pricing page amounts not rendered to fetcher.")
EVX["dd"] = ev("Datadog: Infra Pro $15/host-mo annual ($18 on-demand); APM $31; logs ingest $0.10/GB; 15-day indexing $1.70/M events", "see claim", "USD", "https://www.datadoghq.com/pricing/", "price-list", "current", "A", "'Starting at'.")
EVX["twilio"] = ev("Twilio US SMS $0.0083/segment + carrier fees $0.0035-$0.005", "0.0083", "USD/segment", "https://www.twilio.com/en-us/sms/pricing/us", "price-list", "current", "A")
EVX["postmark"] = ev("Postmark 10k emails/month: Basic $15, Pro $16.50, Platform $18; overage $1.80/$1.30/$1.20 per 1,000", "see claim", "USD", "https://postmarkapp.com/pricing", "price-list", "current", "A")
EVX["justworks"] = ev("Justworks PEO Basic $79/employee-month; payroll $8/employee + $50/month; PEO Plus $124 (some sources $109)", "79", "USD/employee-month", "https://justworks.com/pricing", "vendor-site", "2026", "C", "Official page 403 to fetcher; from search summaries.")
EVX["soc2"] = ev("SOC 2 Type 2 audit fee ranges: specialist firms ~$15k-70k; Big Four $45k-430k; small-company all-in $30k-50k", "15000-70000", "USD/yr", "https://soc2auditors.org/insights/soc-2-type-2-audit-cost/ ; https://drata.com/blog/soc-2-audit-cost", "vendor-site", "2025-2026", "C", "Search summaries of vendor/directory content.")
EVX["soc1"] = ev("SOC 1 Type 2 fee: Schellman baseline $29k-44k; Thoropass $20k-120k", "20000-120000", "USD/yr", "https://schellman.com/blog/what-does-a-soc-audit-cost ; https://thoropass.com/blog/soc-1-audit-cost-a-guide", "vendor-site", "2025-2026", "C", "Schellman figures in a chart not visible in fetched text; from search summary.")
EVX["pentest"] = ev("Penetration test: commercial engagements $10k-35k; small SaaS with APIs $15k-20k+", "10000-35000", "USD", "https://www.blazeinfosec.com/post/how-much-does-penetration-testing-cost/ ; https://www.compassitc.com/blog/how-much-does-a-penetration-test-cost-for-a-small-business", "vendor-site", "2025-2026", "C")
EVX["cyber"] = ev("Small-business cyber insurance $1M limit ~$999-$1,740/yr", "999-1740", "USD/yr", "https://www.moneygeek.com/insurance/business/cyber/cost/ ; https://windes.com/?p=61510", "press", "2025", "C")
EVX["embroker"] = ev("Embroker 2021: tech E&O avg $5,285 (<$1M revenue) to $16,679 (>=$5M); D&O avg $4,782-$16,445; 2024 index: E&O/cyber -4%, D&O flat", "see claim", "USD/yr", "https://www.embroker.com/insurance-index/tech-business-insurance-index/", "press", "2021/2024", "C", "Dated; from search summary.")
EVX["clio"] = ev("Average lawyer billable rate $349 (Jan 2025), $362 (2026); corporate ~$461", "349; 362; 461", "USD/hour", "https://www.clio.com/blog/lawyer-statistics ; https://www.clio.com/state-rates-pages/", "press", "2025-2026", "C", "Clio pages 403 to fetcher; from search summaries.")
EVX["fcfo"] = ev("Fractional CFO: observed average $174/h (IQR $125-200); retainers $3k-10k/month", "174", "USD/hour", "https://gofractional.com/insights/rates/cfo ; https://www.nerdwallet.com/business/software/learn/fractional-cfo", "press", "2025-2026", "C")
EVX["shrm"] = ev("SHRM median cost-per-hire: non-executive $1,300 (2026), $1,200 (2025); executive $15,000 (2026)", "1300; 15000", "USD/hire", "https://www.shrm.org/topics-tools/research/recruiting-benchmarking/full-data-brief", "other", "2025-2026", "C", "From search summary.")
EVX["moov"] = ev("Job posting: Senior Software Engineer (payments), 100% remote US, $165k-185k + equity", "165000-185000", "USD/yr base", "https://www.purpose.jobs/discover/companies/moov-2-d419130a-1fa8-4687-8c0d-ebdcc6ffd18b/jobs/92366284-senior-software-engineer", "job-posting", "posted 2026-09-05 (closed)", "B", "Employer Moov; aggregator page; no personal data recorded.")
EVX["nff"] = ev("Job posting: Staff Accountant, Nonprofit Finance Fund, US remote, $80,600-87,100", "80600-87100", "USD/yr", "https://www.builtinnyc.com/job/staff-accountant/11249475", "job-posting", "reposted ~Oct 2026 (closed to new screening)", "B")
EVX["ia"] = ev("Job posting: Officer, Grant Operations (DAF grant operations, supervises associates), ImpactAssets, US remote, $125k-138k", "125000-138000", "USD/yr", "https://www.builtinaustin.com/job/officer-grant-operations/9929301", "job-posting", "removed 2026-07-23", "B")
EVX["rpa"] = ev("Job posting: Analyst, Sponsored Projects & Funds, Rockefeller Philanthropy Advisors, US remote, $100k-104k", "100000-104000", "USD/yr", "https://www.builtinla.com/job/analyst-sponsored-projects-funds/10050631", "job-posting", "removed 2026-11-13", "B")
EVX["budget"] = ev("Existing hypothesis: 5 FTE, salaries $595,000, loaded at 1.25 = $743,750; total fixed $1,177,750; $75/account incremental incl. $40 labour at $50/h", "1177750", "USD/yr", B.BUDGET + ":5-34", "repo", "2026-11-25", "D", "Analyst-selected assumptions per the document itself.")
EVX["unb"] = ev("Unbound parameters: loaded_cost_per_fte 165,000 (low 124,507 = Vanguard Charitable staff cost/employee; high 250,000); productive_hours 1,600 (1,400-1,600) [A]", "165000; 1600", "USD/FTE-yr; h", B.UNB_PARAMS + ":41-55", "repo", "2026-11-24", "B")
EVX["unb05a"] = ev("Unbound staffed admin cost $192/$299 per fund at 10k funds base/adverse; sponsor-retained ~$42-43; team floor 4 FTE; 15% supervision", "192; 299; 43", "USD/fund-yr", B.UNB_05A + ":379-393", "repo", "2026-11-24", "D", "Model output, not observation.")
EVX["unb_params_act"] = ev("Unbound activity parameters: exceptions 8% (2.8-17%) x 45 min; contacts 0.3/acct x 20 min; grants mult spans 6.2-13 grants/account; lockbox $0.65/check [S]; check $2-8, ACH $0.10-0.50 [A]", "see claim", "", B.UNB_PARAMS, "repo", "2026-11-24", "B")
EVX["jobs_unverified"] = ev("Search-only postings (not opened/verified): Schwab DAFgiving360 donor services $50-65k; Marguerite Casey Foundation accountant $118-130k; Disaster Philanthropy controller $108-121.5k", "see claim", "USD/yr", "web search 2026-11-25", "job-posting", "2026", "D", "NOT used as inputs; fetched pages either expired, 403, or showed estimates only.")

with open(os.path.join(OUT, "evidence.jsonl"), "w") as fh:
    for e in EV:
        fh.write(json.dumps(e) + "\n")

# ------------------------------------------------------------------ assumptions
AS = []
def asm(stmt, val, unit, lo, hi, basis, evs, sens):
    AS.append({"assumption_id": f"A-CST-{len(AS)+1:03d}", "statement": stmt, "value": str(val), "unit": unit, "low": str(lo), "high": str(hi), "basis": basis, "evidence_ids": evs, "sensitivity": sens})
asm("Productive hours per FTE per year", 1520, "hours", 1400, 1650, "2,080 - paid leave ~12% (ECEC MP&R paid leave $7.37 / (wages $54.06 + leave $7.37) = 12.0% => ~1,830 h worked) - training 40 h - internal meetings/admin ~15% of remainder", [ec["Management, professional, and related"], EVX["unb"]], "high")
asm("Employer health cost per enrolled employee", 14000, "USD/yr", 7885, 20143, "KFF 2025 premium minus worker share; base = blend of single and family", [EVX["kff_family"], EVX["kff_single"]], "medium")
asm("Retirement match", 0.03, "share of salary", 0.02, 0.05, "Common safe-harbor range; ECEC MP&R retirement 2.92/61.43 = 4.8% of salary incl. defined benefit", [ec["Management, professional, and related"]], "low")
asm("SUTA per employee", 600, "USD/yr", 300, 1200, "state-dependent new-employer rates x wage bases; not sourced", [], "low")
asm("Workers compensation rate (office/remote)", 0.002, "share of salary", 0.001, 0.004, "clerical class codes; not sourced", [], "low")
asm("PEO/payroll admin fee", 948, "USD/employee-yr", 216, 1488, "Justworks list price via search", [EVX["justworks"]], "low")
asm("Remote-first national pay; no metro premium", "national p50-p75", "", "p25", "p90", "OEWS national percentiles; remote fintech postings sit at/above p75 for engineers", [EVX["moov"]], "high")
asm("Founder cash salaries in Model A", "CEO 90,000; CTO 100,000", "USD/yr", "0", "market", "Founder choice; economic cost uses market rate", [], "medium")
asm("Annual turnover (replacement hires)", 0.15, "share of FTE", 0.08, 0.25, "not sourced", [EVX["shrm"]], "low")
asm("Contingency on cash opex", 0.075, "share", 0.05, 0.10, "existing used ~5.4%", [EVX["budget"]], "medium")
asm("Insurance programme for a payments-adjacent servicer (cyber $5M, tech E&O $5M, D&O, crime incl. third-party, EPLI, GL)", 84000, "USD/yr", 38000, 176000, "Scaled from small-business benchmarks; sponsors' contract minimums unknown", [EVX["cyber"], EVX["embroker"]], "high")
asm("Both SOC 1 Type 2 and SOC 2 Type 2 required once in steady state", "both", "", "SOC 2 only (software-only offer)", "SOC 1+2 + bridge letters", "Staffed administration affects sponsors' financial statements (SOC 1); platform security (SOC 2)", [EVX["soc1"], EVX["soc2"]], "high")
asm("Payments originate from sponsor-owned bank accounts (servicer has no custody)", "sponsor accounts", "", "servicer FBO account", "", "Mission scope: no custody; servicer bank fees then pass-through; regulatory opinion still required", [], "high")
asm("Seasonal December temp hours", "A 320 / B 480 / C 640", "hours", "", "", "4 weeks x 2-4 temps; volumes not measured; Unbound december_k 3 (2-5) [A]", [EVX["unb_params_act"]], "medium")
asm("Outside counsel hours per year", "A 60 / B 100 / C 160", "hours", "", "", "contract negotiations per sponsor, policy updates; not measured", [EVX["clio"]], "medium")
asm("AI tokens per grant screening call", "8k in / 1k out", "tokens", "4k/0.5k", "20k/3k", "prompt with charity record, grant purpose, policy; not measured", [EVX["anth"]], "low")
asm("Agency markup for seasonal temps", 1.6, "x hourly wage", 1.4, 2.0, "not sourced", [soc_ev["43-3031"]], "low")
with open(os.path.join(OUT, "assumptions.jsonl"), "w") as fh:
    for a in AS:
        fh.write(json.dumps(a) + "\n")

# ------------------------------------------------------------------ report
S = []
def sec(title, md):
    S.append({"section": title, "markdown": md})

# 0 summary
tb = T["B"]
sec("Summary and method", f"""Scope: evidence-based fixed operating-cost rebuild for a US remote-first AI-native DAF servicing company (sponsor keeps legal ownership, reserved decisions and custody). Group CST. Access date {ACC}. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate; quality A-D per brief. Files: cost-register.csv ({len(rows)} rows), role-compensation.csv ({len(roles)} roles), staffing-models.csv, evidence.jsonl ({len(EV)}), assumptions.jsonl ({len(AS)}). Python build: scripts/build.py, scripts/report.py (re-runnable).

**Headline [D]:** the existing $1,177,750 / 5-FTE budget re-priced with public evidence is **${f(tb['econ_total'])}** base (low ${f(tb['low_total'])}, high ${f(tb['high_total'])}) for the same five roles. Founder-led Model A: economic ${f(T['A']['econ_total'])}, cash ${f(T['A']['cash_total'])}. Established Model C (12 FTE): ${f(T['C']['econ_total'])}. The 1.25 burden multiplier is supported for professional roles by ECEC; the gap comes from (1) under-market salaries for CTO and controller, (2) security/assurance (SOC 1 + SOC 2 + pen test + vCISO) priced at ~3x the $65k line, (3) insurance at ~2.8x, (4) items absent from the budget (AI fixed, data subscriptions, recruiting, equipment, compliance tooling).

Same-model reasoning; no independent validation. Many non-labour lines are [A] because vendors do not publish prices.""")

# 1 labour market
socs = ["15-1252", "11-3021", "15-1212", "15-1242", "15-1253", "11-3031", "13-2011", "43-3031", "43-3099", "13-2099", "11-1021", "11-1011", "11-2022", "13-1041", "13-1111", "43-4051", "23-1011", "23-2011", "13-1071", "41-3091", "15-1232", "15-1244", "15-2051", "13-2051", "43-4011", "43-6011", "11-2021", "13-1131"]
tbl = "| SOC | Occupation | p10 | p25 | median | p75 | p90 | EV |\n|---|---|---:|---:|---:|---:|---:|---|\n" + "\n".join(
    f"| {s} | {wages[s]['title']} | {f(wages[s]['p'][0])} | {f(wages[s]['p'][1])} | {f(wages[s]['p'][2])} | {f(wages[s]['p'][3])} | {f(wages[s]['p'][4])} | {soc_ev[s]} |" for s in socs)
sec("Labour market evidence", f"""Source: BLS OEWS **May 2025** national, all-industry annual wages (latest release; supersedes May 2024), read via DOL O*NET OnLine national wage tables because bls.gov returned 403 and the BLS API was throttled for this client. Quality B (official data, secondary host). [S]

{tbl}

**Public job postings (openly accessible, no personal data) [S, quality B]:**
| Employer / role | Remote | Base range | Status | EV |
|---|---|---:|---|---|
| Moov, Senior Software Engineer (payments, Go) | 100% US | $165k-185k + equity | posted 2026-09-05, closed | {EVX['moov']} |
| Nonprofit Finance Fund, Staff Accountant | US remote | $80.6k-87.1k | reposted ~Oct 2026 | {EVX['nff']} |
| ImpactAssets, Officer, Grant Operations (DAF) | US remote | $125k-138k | removed 2026-07-23 | {EVX['ia']} |
| Rockefeller Philanthropy Advisors, Analyst, Sponsored Projects & Funds | US remote | $100k-104k | removed 2026-11-13 | {EVX['rpa']} |

Findings: (1) DAF/philanthropy operations postings ($100-138k for analyst/officer) sit well above the 43-xxxx clerk medians ($44-54k); a DAF grant-ops specialist is not a clerk. (2) Remote fintech senior engineers ($165-185k) sit at/above OEWS 15-1252 p75 ($171,980). (3) The existing $115k controller is an accountant-band salary (13-2011 p75 $109,810), not financial-manager (11-3031 p25 $125,490, median $166,570). Unverified search-only postings excluded ({EVX['jobs_unverified']}).""")

# 2 burden
rows_b = "\n".join(f"| {g} | {e['tot']} | {e['w']} | {e['pl']} | {e['ins']+e['ret']+e['leg']:.2f} | {B.naive_mult(e):.3f} | {B.ecec_mult(e):.3f} | {B.ecec_mult(e, True):.3f} | {ec[g]} |" for g, e in B.ECEC.items())
rc = roles
sec("Employer burden (ECEC-derived)", f"""BLS ECEC, June 2026 (released 2026-09-09), private industry, $ per hour worked [S, A-quality]. Headline: wages 70.0% / benefits 30.0% ({EVX['ecec_head']}).

| Group | Total comp | Wages | Paid leave | Ins+Ret+Legal | Naive total/wages | **Burden on salary** | incl. supplemental pay | EV |
|---|---:|---:|---:|---:|---:|---:|---:|---|
{rows_b}

Method [D]: an annual salary already pays for leave, so burden on salary = (insurance + retirement + legally required) / (wages + paid leave). Naive total/wages (~1.46) double counts paid leave and bonuses and should not be used. Result: **1.226** for management/professional (bonus/supplemental adds ~5.8 pts), **1.274** for office/admin support, **1.205** for 1-49-worker establishments.

Role-level build [D]: employer taxes (OASDI 6.2% up to $184,500 [{EVX['ss']}], Medicare 1.45%, FUTA $42, SUTA $600 [A], workers comp 0.2% [A]) + health employer share $14,000 base ($7,885 single to $20,143 family, KFF 2025 [{EVX['kff_family']}]) + 3% retirement + 1% life/disability + PEO $948. Outcome: {rc['cto']['burden_multiplier']} (CTO $185k) to {rc['ops']['burden_multiplier']} (ops specialist $75k) and {rc['csr']['burden_multiplier']} (donor service $55k): health is a per-head fixed cost, so burden is regressive. **Existing 1.25 is supported for professionals (within ~2-3 pts) but understates lower-paid operations roles by 5-15 pts.** Excluded from multiplier and carried in the register: equity, bonus/commission, recruiting, equipment, SaaS, training, travel.""")

# 3 productive hours
sec("Productive hours", f"""[D/A] 2,080 paid hours - paid leave 12.0% (ECEC MP&R paid leave share of salary-paid hours, 7.37/61.43) = ~1,830 hours worked - training/CPE 40 h - internal meetings, supervision, admin ~15% => **~1,520 productive hours (range 1,400-1,650)**. Unbound uses 1,600 (1,400-1,600) [A] ({EVX['unb']}); existing budget uses 1,600 implicitly. At 1,520 h a $75k ops specialist costs **${rc['ops']['loaded_hourly_rate']}/productive hour** (range {rc['ops']['loaded_hourly_range']}), not the $50/h in the existing $75/account decomposition. **$40 of labour buys ~{40/rc['ops']['loaded_hourly_rate']*60:.0f} minutes, not 48.** Founder/engineer time is $117-146/h loaded. December peak capacity cannot be bought by overtime of the same few people without breaking dual-control coverage; temps ($34-49/h bill rate [D]) can only prepare, not release.""")

# 4 models
def model_md(m):
    t = T[m]
    pl = "\n".join(f"| {p['role']} | {p['fte']:g} | {f(p['salary'])} | {f(p['fte']*p['tax'])} | {f(p['fte']*p['ben'])} | {f(p['econ'])} | {f(p['cash'])} | {p['pos']} |" for p in t["P"])
    grp = {}
    for n in t["N"]:
        grp.setdefault(n["category"], [0, 0, 0])
        grp[n["category"]] = [grp[n["category"]][0] + n["low"], grp[n["category"]][1] + n["base"], grp[n["category"]][2] + n["high"]]
    gl = "\n".join(f"| {k} | {f(v[0])} | {f(v[1])} | {f(v[2])} |" for k, v in sorted(grp.items(), key=lambda kv: -kv[1][1]))
    return f"""**{B.MODELS[m][0]}** — core FTE {t['fte']:g}

| Role | FTE | Base | Employer taxes | Benefits | Loaded (economic) | Loaded (cash) | P/S |
|---|---:|---:|---:|---:|---:|---:|---|
{pl}
| **Personnel** | {t['fte']:g} | | | | **{f(t['pers_econ'])}** | **{f(t['pers_cash'])}** | |

| Non-personnel & contracted by category | Low | Base | High |
|---|---:|---:|---:|
{gl}
| **Subtotal** | {f(t['np_low'])} | {f(t['np_base'])} | {f(t['np_high'])} |

| Total (fixed, annual) | Low | Base | High |
|---|---:|---:|---:|
| Economic (founders at market) incl. 7.5% contingency | {f(t['low_total'])} | **{f(t['econ_total'])}** | {f(t['high_total'])} |
| Cash (founder cash salaries) | | **{f(t['cash_total'])}** | |

Excludes per-account variable costs, startup, sponsor-specific onboarding/migration. Roles, authority, SoD pairs, backup, December cover and hiring triggers: staffing-models.csv."""
sec("Model A budget: founder-led", model_md("A") + f"""

Assessment: cash saving vs B is ${f(T['B']['cash_total']-T['A']['cash_total'])} but economic saving only ${f(T['B']['econ_total']-T['A']['econ_total'])}; ~${f(T['A']['np_base'])} of non-personnel cost (assurance, insurance, legal, vCISO, retainers) does not shrink with headcount. Viable only for 1 sponsor / <~1,500-2,000 accounts and only if the sponsor co-approves payments (three-person team cannot otherwise sustain dual control during absence). Third core person is a controller-grade finance & grant operations lead at market pay. Founder unpaid market-value gap = ${f(T['A']['econ_total']-T['A']['cash_total'])}/yr and is a real cost (opportunity cost / later catch-up).""")
sec("Model B budget: lean independent (5 core, existing structure re-priced)", model_md("B") + """

Assessment: same roles as the existing hypothesis. Structural weakness: one ops specialist; controller backing ops collapses preparer/releaser separation on the same item, so a 2nd ops specialist (or sponsor co-approval) is needed for any absence >2 weeks; that is +$99k loaded and is the first hiring trigger, likely before 2,500 accounts.""")
sec("Model C budget: established (12 core)", model_md("C") + f"""

Assessment: specialised and redundant (two payment releasers, security engineer replaces vCISO, compliance officer replaces consultant, implementation analyst absorbs onboarding labour). Fractional/outsourced finance roles drop out. This is the structure sponsors' risk committees and SOC 1 auditors will most readily accept; its fixed cost alone equals revenue at ${T['C']['econ_total']/0.002/1e9:.2f}B average billable AUA at 20 bps, before variable costs and margin [D: total / 0.002].""")

# 5 contracted
ids = ["CST-C01", "CST-C02", "CST-C03", "CST-C04", "CST-C05", "CST-C06", "CST-C07", "CST-C08", "CST-C09", "CST-C10", "CST-P14", "CST-P21"]
ct = "\n".join(f"| {i} | {idx[i][2]} | {idx[i][4]} | {idx[i][5]:g} | {idx[i][6]:g} | {idx[i][7]:g} | {idx[i][11]} | {idx[i][12][:140]} |" for i in ids)
sec("Contracted and fractional services", f"""| ID | Service | Driver | Low | Base | High | Q | Note |
|---|---|---|---:|---:|---:|---|---|
{ct}

Observations: fractional CFO and outside counsel are the only contracted lines with any public rate evidence (C-quality aggregates). Bookkeeping, audit and tax fees have no public price lists; ranges are [A]. The single most important legal item is the regulatory opinion (CST-C08) on whether payment-processing as agent for sponsors triggers money-transmitter licensing; the answer changes the payments architecture and possibly the cost base materially.""")

# 6 tech
ids = ["CST-T01", "CST-T02", "CST-T03", "CST-T04", "CST-T05", "CST-T07", "CST-T08", "CST-T09", "CST-T10", "CST-T12", "CST-T13", "CST-D01", "CST-D02", "CST-D03", "CST-D04", "CST-D05", "CST-ID1", "CST-ID2", "CST-PY1", "CST-PY2", "CST-PY3", "CST-PY4", "CST-PY5", "CST-PY6", "CST-PY9", "CST-PY10", "CST-PY11", "CST-CM1", "CST-CM2", "CST-CM3", "CST-S01", "CST-S02", "CST-S03", "CST-S04"]
tt = "\n".join(f"| {i} | {idx[i][2][:70]} | {idx[i][8]} | {idx[i][5]:g} | {idx[i][6]:g} | {idx[i][7]:g} | {idx[i][3]} | {idx[i][11]} |" for i in ids)
grants = 10; ach = 0.9
var = [("Grant payments (9 ACH x $0.50 + 1 check x $3.00)", grants*ach*0.50 + grants*(1-ach)*3.00, "CST-PY1, PY5"),
       ("ACH returns (0.5% x 10 x $5)", 0.005*grants*5, "CST-PY7"),
       ("Identity verification (15% new/re-verified x $1.50)", 0.15*1.5, "CST-ID2"),
       ("AI inference all workflows", 0.75, "CST-T13"),
       ("SMS (10 segments) + email", 10*0.0128 + 0.05, "CST-CM2, CM1"),
       ("Paper statements/receipts (20% paper x 4 x $0.658)", 0.2*4*0.658, "CST-CM3"),
       ("Incremental cloud/storage [A]", 1.0, "Unbound infra_per_account 3.0 (0.5-6) [A]")]
vt = "\n".join(f"| {a} | {b:.2f} | {c} |" for a, b, c in var)
vsum = sum(v[1] for v in var)
sec("Technology and vendor costs", f"""Public price lists read {ACC} (A unless noted).

| ID | Item | Unit | Low | Base | High | Type | Q |
|---|---|---|---:|---:|---:|---|---|
{tt}

**Database sizing [D]:** Azure PostgreSQL Flexible Server 4 vCore Ddsv5 with zone-redundant HA ≈ ${f(idx['CST-T01'][6])}/yr + cross-region DR replica ${f(idx['CST-T02'][6])} + storage/backup ≈ $3.3k: a production-grade HA+DR database is **~$13k/yr**, ~one-third of the existing $36k cloud line. Compute is cheap; people, assurance and insurance dominate. AWS RDS equivalent not extracted (gap).

**AI [D]:** at current list prices a Sonnet-class screening call (8k in/1k out) is ~$0.026; Haiku-class batch ~$0.0007; Opus-class 20k/3k ~$0.14. Even at 10 grants/account-yr with Opus everywhere, AI is <$2/account-yr. AI is not a material cost line; its risk is quality/oversight labour, not tokens.

**Charity data:** IRS EO BMF and OFAC SLS are free downloads; Candid APIs start at $2,750-9,900 (term/volume unpublished). Persona identity: $3,000/yr plan + $1.50/verification. Commercial sanctions screening: no public price.

**Payments:** public per-item prices ACH $0.50 (same-day $1-2), wire $15-25, RTP $2.50, check print+mail $1.04-3.00. Modern Treasury: no public price. If grants are paid from the sponsor's own bank account, these are sponsor pass-through, not servicer cost.

**Indicative non-labour variable cost per account-year [D, A-inputs: 10 grants/account (Unbound range 6.2-13), 90% ACH]:**
| Component | $/account-yr | Source |
|---|---:|---|
{vt}
| **Total non-labour** | **{vsum:.2f}** | vs existing $35 non-labour ($10 payments + $10 data/identity + $5 cloud + $10 other) |

The existing $10 data/identity per account is overstated as a *variable* cost: the data/identity spend is mostly fixed subscriptions (~$14k/yr in Model B), already in the fixed budget here. Labour, not vendors, drives variable cost: at ${rc['ops']['loaded_hourly_rate']}/h every 10 minutes per account-year = ${rc['ops']['loaded_hourly_rate']/6:.2f}.""")

# 7 insurance & assurance
ids = ["CST-I01", "CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07", "CST-C11", "CST-C12", "CST-C13", "CST-C14", "CST-C15", "CST-C16", "CST-C17", "CST-C18"]
it = "\n".join(f"| {i} | {idx[i][2][:80]} | {idx[i][5]:,.0f} | {idx[i][6]:,.0f} | {idx[i][7]:,.0f} | {idx[i][3]} | {idx[i][11]} |" for i in ids)
ins = sum(idx[i][6] for i in ["CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07"])
insl = sum(idx[i][5] for i in ["CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07"])
insh = sum(idx[i][7] for i in ["CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07"])
sa = sum(idx[i][6] for i in ["CST-C11", "CST-C12", "CST-C14", "CST-C15", "CST-C16", "CST-C18"])
sec("Insurance and assurance", f"""| ID | Item | Low | Base | High | Type | Q |
|---|---|---:|---:|---:|---|---|
{it}

Insurance programme total [D]: **${f(insl)} / ${f(ins)} / ${f(insh)}** vs existing $30,000. Public benchmarks exist only for generic small businesses ($1M cyber ~$1-1.7k/yr; 2021 startup E&O/D&O averages $5-17k); a servicer processing charitable payments will face higher limits ($5M+) demanded by sponsors, crime/social-engineering cover and underwriting scrutiny. All programme figures beyond those benchmarks are [A].

Assurance/security recurring (SOC 2 T2 + SOC 1 T2 + pen test + compliance automation + IR retainer + DR test) base **${f(sa)}** before vCISO/security engineer, vs existing $65,000 for 'security/assurance'. A software-only licence needs SOC 2; staffed administration that touches sponsors' financial reporting needs SOC 1 (with bridge letters). Phasing [A]: year 1 SOC 2 Type 1 + SOC 1 Type 1 (~60% of Type 2 fees), Type 2 from year 2; sponsors may refuse go-live before a Type 2 report — a material sales-cycle risk.""")

# 8 startup
def startup(m):
    t = T[m]; fte = t["fte"]
    items = [("Incorporation/filings (ST1)", idx["CST-ST1"][5:8]),
             ("Startup legal (C07)", idx["CST-C07"][5:8]),
             ("Regulatory opinion (C08)", idx["CST-C08"][5:8]),
             ("SOC readiness (C13)", idx["CST-C13"][5:8]),
             ("Initial pen test pre-launch (C14)", idx["CST-C14"][5:8]),
             ("Brand/website (ST2)", idx["CST-ST2"][5:8]),
             ("Implementation/migration tooling (ST3)", idx["CST-ST3"][5:8]),
             (f"Recruiting {fte:g} initial hires (P16)", tuple(fte * x for x in idx["CST-P16"][5:8])),
             (f"Equipment {fte:g} FTE (3-yr laptops upfront)", tuple(fte * 3 * x for x in idx["CST-P17"][5:8]))]
    one = [sum(x[1][i] for x in items) for i in range(3)]
    build = (0.75 * t["cash_total"], 1.0 * t["cash_total"], 1.5 * t["cash_total"])
    wc = tuple(mo / 12 * t["cash_total"] for mo in idx["CST-ST5"][5:8])
    prem = sum(idx[i][6] for i in ["CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07"])
    return items, one, build, wc, prem
blocks = []
for m in "ABC":
    items, one, bld, wc, prem = startup(m)
    li = "\n".join(f"| {a} | {f(b[0])} | {f(b[1])} | {f(b[2])} |" for a, b in items)
    blocks.append(f"""**{B.MODELS[m][0]}**
| Item | Low | Base | High |
|---|---:|---:|---:|
{li}
| One-time subtotal | {f(one[0])} | {f(one[1])} | {f(one[2])} |
| Pre-revenue build/run at cash burn (9/12/18 months) [A] | {f(bld[0])} | {f(bld[1])} | {f(bld[2])} |
| Working capital (2/3/4 months fixed cash opex; billing in arrears) [A] | {f(wc[0])} | {f(wc[1])} | {f(wc[2])} |
| **Indicative capital need** | **{f(one[0]+bld[0]+wc[0])}** | **{f(one[1]+bld[1]+wc[1])}** | **{f(one[2]+bld[2]+wc[2])}** |
Insurance binding: ~${f(prem)} first-year premiums payable upfront or in instalments (timing only).""")
sec("Startup and one-time costs", "\n\n".join(blocks) + "\n\nExisting runway hypothesis: 12 months $1.178M + $250k launch reserve = $1.428M. Rebuilt Model B (12 months) is materially higher; sponsor-specific onboarding ($10-75k) and migration ($25-250k) per sponsor (CST-OM1/OM2) are customer-specific and additional. These are illustrative capital ranges, not a financing plan.")

# 9 reconciliation
MAP = [("Loaded personnel", 743750, None),
       ("Legal/compliance", 60000, ["CST-C06", "CST-C04", "CST-C15"]),
       ("Independent accounting/controls", 45000, ["CST-C09", "CST-C10", "CST-C02", "CST-C01", "CST-S06"]),
       ("Seasonal/backup coverage", 60000, ["CST-P14"]),
       ("Cloud/monitoring", 36000, ["CST-T01", "CST-T02", "CST-T03", "CST-T04", "CST-T05", "CST-T06", "CST-T07", "CST-T08", "CST-T09", "CST-T10"]),
       ("Security/assurance", 65000, ["CST-C11", "CST-C12", "CST-C14", "CST-C03", "CST-C16", "CST-C18", "CST-T11"]),
       ("Insurance", 30000, ["CST-I02", "CST-I03", "CST-I04", "CST-I05", "CST-I06", "CST-I07"]),
       ("Business software", 18000, ["CST-S01", "CST-S02", "CST-S03", "CST-S04", "CST-S05", "CST-S07", "CST-S08", "CST-CM1", "CST-CM4", "CST-CM5"]),
       ("Sales/travel", 40000, ["CST-SM1", "CST-SM2", "CST-TR1"]),
       ("General administration", 20000, ["CST-G01", "CST-G02", "CST-G03", "CST-P16", "CST-P17", "CST-P18", "CST-P19", "CST-PY8"]),
       ("NOT IN EXISTING: AI fixed, charity data, identity, sanctions subscriptions", 0, ["CST-T14", "CST-D03", "CST-D05", "CST-ID1"]),
       ]
nb = {n["cost_id"]: n for n in T["B"]["N"]}
used = set()
lines = []
for name, old, idsx in MAP:
    if idsx is None:
        new = T["B"]["pers_econ"]; lo = T["B"]["pers_low"]; hi = T["B"]["pers_high"]
    else:
        new = sum(nb[i]["base"] for i in idsx if i in nb); lo = sum(nb[i]["low"] for i in idsx if i in nb); hi = sum(nb[i]["high"] for i in idsx if i in nb)
        used |= set(idsx)
    lines.append((name, old, lo, new, hi))
left = [i for i in nb if i not in used]
assert not left, left
sub_old = sum(l[1] for l in lines); sub_new = sum(l[3] for l in lines)
cont_new = T["B"]["econ_total"] - sub_new
COMM = {
 "Loaded personnel": f"UNDERSTATED. Salaries re-based on OEWS May 2025 + postings: CTO 150k->185k, engineer 120k->155k, controller 115k->150k, MD 130k->165k, ops 80k->75k. Burden 1.25 confirmed for professionals by ECEC (1.226) but ops role is ~1.33.",
 "Legal/compliance": "Roughly right in total but mixes items; regulatory (money-transmission) opinion is a startup cost not in the budget.",
 "Independent accounting/controls": "UNDERSTATED: audit + tax + outsourced books + CFO review; outsourced books preserves SoD for a single controller.",
 "Seasonal/backup coverage": "OVERSTATED for December temps (~$19k), but the real backup need (2nd ops FTE ~$99k loaded) is MISSING: the line cannot buy dual-control coverage.",
 "Cloud/monitoring": "Roughly right/slightly high at launch scale: HA+DR PostgreSQL ~$13k; hosting assumption dominates.",
 "Security/assurance": "MATERIALLY UNDERSTATED: SOC 2 T2 + SOC 1 T2 + pen test + vCISO + IR + DR test.",
 "Insurance": "UNDERSTATED: payments-adjacent servicer needs $5M cyber/E&O plus crime incl. third-party/social engineering.",
 "Business software": "Roughly right; per-user SaaS is small.",
 "Sales/travel": "Kept $40k conferences; adds marketing and remote-team travel.",
 "General administration": "UNDERSTATED: recruiting, equipment, training, filings, bank treasury fees were missing.",
 "NOT IN EXISTING: AI fixed, charity data, identity, sanctions subscriptions": "MISSING as fixed costs (existing put $10/account data/identity in variable).",
}
rt = "\n".join(f"| {n} | {f(o)} | {f(l)} | {f(b)} | {f(h)} | {f(b-o)} | {COMM[n]} |" for n, o, l, b, h in lines)
sec("Reconciliation against existing $1,177,750", f"""Line-by-line, existing ({EVX['budget']}) vs rebuilt Model B (same 5 roles) [D].

| Existing line | Existing | Rebuilt low | Rebuilt base | Rebuilt high | Delta (base) | Finding |
|---|---:|---:|---:|---:|---:|---|
{rt}
| Contingency | 60,000 | | {f(cont_new)} | | {f(cont_new-60000)} | 7.5% (5-10%) of cash opex vs 5.4% |
| **Total** | **1,177,750** | **{f(T['B']['low_total'])}** | **{f(T['B']['econ_total'])}** | **{f(T['B']['high_total'])}** | **{f(T['B']['econ_total']-1177750)}** | |

Interpretation: the existing number sits near the rebuilt **low** case (all inputs at the favourable end simultaneously). The base case is ~{(T['B']['econ_total']/1177750-1)*100:.0f}% higher. Break-even AUA at 20 bps scales proportionally: F/r alone moves from $589M to ${T['B']['econ_total']/0.002/1e6:,.0f}M before any variable cost [D]. Missing entirely from both: equity compensation, sales commission, sponsor onboarding/migration labour, and the second ops FTE needed for dual control.

$75/account placeholder: non-labour components re-estimated at ~${vsum:.0f}/account-yr (vs $35); labour at ${rc['ops']['loaded_hourly_rate']}/h (vs $50) so $40 buys ~{40/rc['ops']['loaded_hourly_rate']*60:.0f} min. Net effect on v depends on measured minutes/account (activity group).""")

# 10 platform vs staffed
def split(m):
    t = T[m]; d = {}
    for p in t["P"]:
        d[p["pos"]] = d.get(p["pos"], 0) + p["econ"]
    for n in t["N"]:
        d[n["pos"]] = d.get(n["pos"], 0) + n["base"]
    return d
spl = {m: split(m) for m in "ABC"}
keys = ["software platform", "staffed administration", "shared"]
st = "\n".join(f"| {k} | " + " | ".join(f(spl[m].get(k, 0)) for m in "ABC") + " |" for k in keys)
sec("Cost separation: software platform vs staffed administration", f"""Every register line is tagged platform / staffed / shared (column platform_or_staffed). Base annual fixed cost by tag (before contingency) [D]:

| Tag | Model A | Model B | Model C |
|---|---:|---:|---:|
{st}

Rules to avoid double counting:
1. **One platform cost pool.** Engineering, cloud, SOC 2, pen test, AI fixed, monitoring, data subscriptions are incurred once. If the company also sells software-only licences, the staffed administration P&L should carry an internal platform charge = platform pool / total accounts on platform, not an external licence price on top of the fixed budget.
2. **Unbound 05a staffed cost ($192/$299 per fund at 10k funds) is computed at a stated platform-cost scale** (column 'Platform cost scale'), while the market-entry note says sales, build capex and assurance sit in the vendor P&L outside it. So it neither replaces this fixed budget nor can be added on top of it; reconcile component by component (platform operations vs assurance vs sales vs staffing).
3. **SOC 1, crime insurance, payment operations, charity verification labour, controller, ops staff** belong to staffed administration; a software-only business avoids most of them (but sponsor then bears them).
4. **Shared** (CEO, legal, D&O, cyber, E&O, G&A, compliance officer) must be allocated by an explicit key (e.g. revenue or headcount), never fully to both.
5. **Pass-through and sponsor-retained** (grant principal, investment fees, donor-facing fees, bank fees on sponsor-owned accounts, sponsor reserved-decision labour ~$42-43/fund) are excluded from servicer cost and revenue.
6. Data/identity subscriptions are fixed (here) and only overage is variable; do not also put $10/account in v.""")

# 11 gaps
sec("Evidence gaps", f"""1. **BLS direct access**: bls.gov tables/API blocked or throttled; OEWS read via O*NET (same data, secondary host). ECEC tables read directly. Industry-specific OEWS (NAICS 5239/5242/8132) not extracted — national all-industry medians may understate fintech and overstate nonprofit pay.
2. **No public prices**: Vanta/Drata, Modern Treasury, commercial sanctions screening, bookkeeping, CPA audit/tax, e-signature, most insurance lines. Ranges are [A]. Broker quotes would require outreach (not permitted).
3. **Insurance**: only generic small-business and dated (2021) startup averages; sponsor-mandated limits unknown. Highest uncertainty non-labour line (${f(insl)}-${f(insh)}).
4. **SOC 1/SOC 2 fees**: vendor-blog ranges only (C); Schellman chart not machine-readable.
5. **Legal rates**: Clio aggregates (C); specialist exempt-org + money-transmission counsel rates and the regulatory conclusion itself are unknown and potentially decisive.
6. **AWS RDS / GCP prices** not extracted; Azure used as the cloud reference.
7. **Productive hours, minutes per activity, December peak multiple** unmeasured; 1,520 h is [D/A].
8. **Postings**: four verified; all closed/removed; no verified DAF-servicer (Ren, Stellar, TIFIN Give, Chariot) posting with pay range read. Search-only postings excluded.
9. **Equity compensation** for founders/early staff excluded; can materially change true economic cost of Model A/B.
10. Same-model analysis; no independent reviewer.""")

with open(os.path.join(OUT, "report.jsonl"), "w") as fh:
    for s in S:
        fh.write(json.dumps(s) + "\n")
print("ok", len(EV), len(AS), len(S))
