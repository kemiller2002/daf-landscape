# 03: Organization and budget

**Date:** 2026-11-25. **Passes:** CST (costs and staffing) and ECH (Echelon Foundry).

**Data:**
- [`cost-register.csv`](../../../data/commercial-opportunity/servicing-economics/cost-register.csv): 109 lines.
- [`role-compensation.csv`](../../../data/commercial-opportunity/servicing-economics/role-compensation.csv) and [`staffing-models.csv`](../../../data/commercial-opportunity/servicing-economics/staffing-models.csv).
- [`echelon-capabilities.csv`](../../../data/commercial-opportunity/servicing-economics/echelon-capabilities.csv): 22 capabilities.

## Integrator conclusions

1. **The $1,177,750 / 5-FTE budget is a low case, not a base.** Re-priced from BLS OEWS May 2025 wages (read via O*NET, grade B), BLS ECEC burden and public vendor prices, the same five roles cost **$1.66M a year (range $1.09-2.77M)**. The prior budget missed or understated:
   - market salaries for the CTO, engineer and controller;
   - security and assurance: SOC 1 and SOC 2 Type 2, penetration testing and a vCISO total about $166k, against $65k budgeted;
   - insurance: about $84k against $30k;
   - and it cannot sustain dual control.
2. **Three structures, as encoded in the model:**

   | Model | Core FTE | Fixed (economic) | Fixed (cash) | Live-operation minimum |
   |---|---:|---:|---:|---|
   | A founder-led | 3 | $1.31M | $1.12M | +2 ops staff for separation of duties (so about 5 people once live) |
   | B lean independent | 5 | $1.66M | $1.66M | +1 ops staff (second preparer/releaser) |
   | C established | 12 | $2.84M | $2.84M | none |

   Model A is a pre-launch structure. Once live it converges on Model B's headcount but keeps the founders' below-market cash pay. That is a cash, not an economic, saving of about $0.2M a year.
3. **Founder labour is not free.** Every model is shown at economic cost, with founders at market pay. Cash cost is shown separately, and the capital plans in report 06 use cash with an economic-cost variant.
4. **Echelon Foundry saves little on verified evidence.**
   - No DAF application or production infrastructure exists. Unbound is requirements only.
   - Verified reuse (framework code, design assets, the public-data replay tool, a single-VM PostgreSQL benchmark) cuts **$0-105k a year**, and it is shared cost, not eliminated cost.
   - Most of the stack is licensed PolyForm Noncommercial, so a commercial licence is a launch gate and a cost to the DAF business.
   - Engineering cost could be 33-50% lower only if agent-assisted throughput is measured at 1.5-2x and sustained for six months or more. Nothing measures that yet.
   - The prior budget also omitted the platform build itself: Unbound's own model assumes **$5M ($3-15M)**.
5. **Platform vs staffed business.** The CST cost-separation rules below are applied in the model: platform lines are in fixed cost; staffed-operations lines are in capacity and step costs; sponsor-retained decision costs ($42-43 per account) are excluded because the sponsor bears them; pass-throughs are optional.

> Research-pass content below was produced by a role-separated agent pass from the same model family as the integrator. It is not independent validation. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate.

## Summary and method

Scope: evidence-based fixed operating-cost rebuild for a US remote-first AI-native DAF servicing company (sponsor keeps legal ownership, reserved decisions and custody). Group CST. Access date 2026-11-25. Labels: [S] sourced, [A] assumption, [D] derived, [E] estimate; quality A-D per brief. Files: cost-register.csv (109 rows), role-compensation.csv (15 roles), staffing-models.csv, evidence.jsonl (78), assumptions.jsonl (17). Python build: scripts/build.py, scripts/report.py (re-runnable).

**Headline [D]:** the existing $1,177,750 / 5-FTE budget re-priced with public evidence is **$1,660,006** base (low $1,085,589, high $2,770,034) for the same five roles. Founder-led Model A: economic $1,308,094, cash $1,115,745. Established Model C (12 FTE): $2,839,696. The 1.25 burden multiplier is supported for professional roles by ECEC; the gap comes from (1) under-market salaries for CTO and controller, (2) security/assurance (SOC 1 + SOC 2 + pen test + vCISO) priced at ~3x the $65k line, (3) insurance at ~2.8x, (4) items absent from the budget (AI fixed, data subscriptions, recruiting, equipment, compliance tooling).

Same-model reasoning; no independent validation. Many non-labour lines are [A] because vendors do not publish prices.

## Labour market evidence

Source: BLS OEWS **May 2025** national, all-industry annual wages (latest release; supersedes May 2024), read via DOL O*NET OnLine national wage tables because bls.gov returned 403 and the BLS API was throttled for this client. Quality B (official data, secondary host). [S]

| SOC | Occupation | p10 | p25 | median | p75 | p90 | EV |
|---|---|---:|---:|---:|---:|---:|---|
| 15-1252 | Software Developers | 82,460 | 105,210 | 135,980 | 171,980 | 214,670 | EV-CST-018 |
| 11-3021 | Computer and Information Systems Managers | 107,550 | 138,060 | 175,140 | 220,730 | 297,510 | EV-CST-005 |
| 15-1212 | Information Security Analysts | 75,090 | 97,810 | 129,180 | 163,500 | 199,850 | EV-CST-014 |
| 15-1242 | Database Administrators | 60,230 | 79,610 | 104,620 | 135,460 | 163,320 | EV-CST-016 |
| 15-1253 | Software Quality Assurance Analysts and Testers | 61,440 | 80,310 | 104,300 | 133,180 | 167,010 | EV-CST-019 |
| 11-3031 | Financial Managers | 94,310 | 125,490 | 166,570 | 219,980 | 323,270 | EV-CST-006 |
| 13-2011 | Accountants and Auditors | 56,020 | 67,020 | 83,680 | 109,810 | 144,090 | EV-CST-011 |
| 43-3031 | Bookkeeping, Accounting, and Auditing Clerks | 36,000 | 43,520 | 50,670 | 61,470 | 74,550 | EV-CST-024 |
| 43-3099 | Financial Clerks, All Other | 40,360 | 47,510 | 53,830 | 62,310 | 76,290 | EV-CST-025 |
| 13-2099 | Financial Specialists, All Other | 48,460 | 61,290 | 81,100 | 110,410 | 151,490 | EV-CST-013 |
| 11-1021 | General and Operations Managers | 50,090 | 72,320 | 105,770 | 167,280 | 253,390 | EV-CST-002 |
| 11-1011 | Chief Executives | 75,700 | 129,540 | 213,990 | 356,200 | 507,730 | EV-CST-001 |
| 11-2022 | Sales Managers | 73,170 | 100,360 | 148,270 | 207,340 | 290,540 | EV-CST-004 |
| 13-1041 | Compliance Officers | 48,220 | 61,280 | 80,730 | 109,010 | 133,720 | EV-CST-007 |
| 13-1111 | Management Analysts | 60,640 | 77,950 | 101,860 | 133,370 | 171,640 | EV-CST-009 |
| 43-4051 | Customer Service Representatives | 31,750 | 36,870 | 44,770 | 51,780 | 63,590 | EV-CST-027 |
| 23-1011 | Lawyers | 78,360 | 102,990 | 159,670 | 221,370 | 351,600 | EV-CST-021 |
| 23-2011 | Paralegals and Legal Assistants | 44,740 | 50,340 | 62,890 | 80,080 | 101,500 | EV-CST-022 |
| 13-1071 | Human Resources Specialists | 47,180 | 58,610 | 75,940 | 99,380 | 128,720 | EV-CST-008 |
| 41-3091 | Sales Representatives of Services, Except Advertising, Insurance, Financial Services, and Travel | 37,980 | 47,670 | 69,990 | 100,480 | 148,840 | EV-CST-023 |
| 15-1232 | Computer User Support Specialists | 40,980 | 49,000 | 61,860 | 79,040 | 100,540 | EV-CST-015 |
| 15-1244 | Network and Computer Systems Administrators | 62,640 | 78,010 | 99,130 | 126,640 | 155,050 | EV-CST-017 |
| 15-2051 | Data Scientists | 67,240 | 85,660 | 120,230 | 158,880 | 199,130 | EV-CST-020 |
| 13-2051 | Financial and Investment Analysts | 63,720 | 79,290 | 102,740 | 133,340 | 180,860 | EV-CST-012 |
| 43-4011 | Brokerage Clerks | 50,260 | 58,620 | 65,750 | 79,800 | 102,010 | EV-CST-026 |
| 43-6011 | Executive Secretaries and Executive Administrative Assistants | 50,560 | 61,390 | 76,590 | 94,390 | 109,850 | EV-CST-028 |
| 11-2021 | Marketing Managers | 90,260 | 123,020 | 166,790 | 216,410 | 293,610 | EV-CST-003 |
| 13-1131 | Fundraisers | 46,630 | 57,480 | 72,550 | 92,180 | 115,820 | EV-CST-010 |

**Public job postings (openly accessible, no personal data) [S, quality B]:**
| Employer / role | Remote | Base range | Status | EV |
|---|---|---:|---|---|
| Moov, Senior Software Engineer (payments, Go) | 100% US | $165k-185k + equity | posted 2026-09-05, closed | EV-CST-070 |
| Nonprofit Finance Fund, Staff Accountant | US remote | $80.6k-87.1k | reposted ~Oct 2026 | EV-CST-071 |
| ImpactAssets, Officer, Grant Operations (DAF) | US remote | $125k-138k | removed 2026-07-23 | EV-CST-072 |
| Rockefeller Philanthropy Advisors, Analyst, Sponsored Projects & Funds | US remote | $100k-104k | removed 2026-11-13 | EV-CST-073 |

Findings: (1) DAF/philanthropy operations postings ($100-138k for analyst/officer) sit well above the 43-xxxx clerk medians ($44-54k); a DAF grant-ops specialist is not a clerk. (2) Remote fintech senior engineers ($165-185k) sit at/above OEWS 15-1252 p75 ($171,980). (3) The existing $115k controller is an accountant-band salary (13-2011 p75 $109,810), not financial-manager (11-3031 p25 $125,490, median $166,570). Unverified search-only postings excluded (EV-CST-078).

## Employer burden (ECEC-derived)

BLS ECEC, June 2026 (released 2026-09-09), private industry, $ per hour worked [S, A-quality]. Headline: wages 70.0% / benefits 30.0% (EV-CST-037).

| Group | Total comp | Wages | Paid leave | Ins+Ret+Legal | Naive total/wages | **Burden on salary** | incl. supplemental pay | EV |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Management, professional, and related | 78.88 | 54.06 | 7.37 | 13.86 | 1.459 | 1.226 | 1.284 | EV-CST-029 |
| Management, business, and financial | 88.63 | 59.85 | 8.47 | 15.42 | 1.481 | 1.226 | 1.297 | EV-CST-030 |
| Professional and related | 73.69 | 50.98 | 6.78 | 13.03 | 1.445 | 1.226 | 1.276 | EV-CST-031 |
| Office and administrative support | 36.73 | 25.22 | 2.77 | 7.68 | 1.456 | 1.274 | 1.312 | EV-CST-032 |
| Financial activities industry | 66.05 | 43.23 | 6.04 | 13.00 | 1.528 | 1.264 | 1.341 | EV-CST-033 |
| Information industry | 84.28 | 54.46 | 8.63 | 16.70 | 1.548 | 1.265 | 1.336 | EV-CST-034 |
| Establishments 1-49 workers (all occupations) | 37.64 | 27.88 | 2.34 | 6.19 | 1.350 | 1.205 | 1.246 | EV-CST-035 |
| All private industry | 46.89 | 32.82 | 3.54 | 8.66 | 1.429 | 1.238 | 1.290 | EV-CST-036 |

Method [D]: an annual salary already pays for leave, so burden on salary = (insurance + retirement + legally required) / (wages + paid leave). Naive total/wages (~1.46) double counts paid leave and bonuses and should not be used. Result: **1.226** for management/professional (bonus/supplemental adds ~5.8 pts), **1.274** for office/admin support, **1.205** for 1-49-worker establishments.

Role-level build [D]: employer taxes (OASDI 6.2% up to $184,500 [EV-CST-040], Medicare 1.45%, FUTA $42, SUTA $600 [A], workers comp 0.2% [A]) + health employer share $14,000 base ($7,885 single to $20,143 family, KFF 2025 [EV-CST-038]) + 3% retirement + 1% life/disability + PEO $948. Outcome: 1.203 (CTO $185k) to 1.326 (ops specialist $75k) and 1.402 (donor service $55k): health is a per-head fixed cost, so burden is regressive. **Existing 1.25 is supported for professionals (within ~2-3 pts) but understates lower-paid operations roles by 5-15 pts.** Excluded from multiplier and carried in the register: equity, bonus/commission, recruiting, equipment, SaaS, training, travel.

## Productive hours

[D/A] 2,080 paid hours - paid leave 12.0% (ECEC MP&R paid leave share of salary-paid hours, 7.37/61.43) = ~1,830 hours worked - training/CPE 40 h - internal meetings, supervision, admin ~15% => **~1,520 productive hours (range 1,400-1,650)**. Unbound uses 1,600 (1,400-1,600) [A] (EV-CST-075); existing budget uses 1,600 implicitly. At 1,520 h a $75k ops specialist costs **$65.45/productive hour** (range 46.54-89.98), not the $50/h in the existing $75/account decomposition. **$40 of labour buys ~37 minutes, not 48.** Founder/engineer time is $117-146/h loaded. December peak capacity cannot be bought by overtime of the same few people without breaking dual-control coverage; temps ($34-49/h bill rate [D]) can only prepare, not release.

## Model A budget: founder-led

**Model A founder-led (3 core + fractional + contractors + automation)** — core FTE 3

| Role | FTE | Base | Employer taxes | Benefits | Loaded (economic) | Loaded (cash) | P/S |
|---|---:|---:|---:|---:|---:|---:|---|
| Founder / CEO-managing director (sponsor relationships, sales, governance) | 1 | 165,000 | 13,594 | 21,548 | 200,142 | 116,255 | shared |
| CTO / technical lead (architecture, security, DR, AI controls) | 1 | 185,000 | 15,134 | 22,348 | 222,482 | 127,440 | software platform |
| Controller / head of financial operations | 1 | 150,000 | 12,417 | 20,948 | 183,365 | 183,365 | staffed administration |
| **Personnel** | 3 | | | | **605,989** | **427,060** | |

| Non-personnel & contracted by category | Low | Base | High |
|---|---:|---:|---:|
| assurance | 55,000 | 110,000 | 250,000 |
| insurance | 38,000 | 84,000 | 176,000 |
| security-testing | 34,000 | 68,000 | 131,000 |
| personnel | 31,865 | 60,030 | 116,030 |
| accounting | 30,500 | 56,200 | 117,200 |
| compliance | 18,000 | 45,000 | 90,000 |
| cloud | 18,336 | 35,336 | 83,996 |
| legal | 18,000 | 27,000 | 48,000 |
| sales | 9,500 | 26,000 | 54,000 |
| software | 6,027 | 14,027 | 40,118 |
| dr-bcp | 6,559 | 13,119 | 31,237 |
| ai | 3,000 | 12,000 | 36,000 |
| marketing | 2,500 | 10,000 | 30,000 |
| travel | 4,500 | 9,000 | 15,000 |
| data | 3,000 | 8,000 | 25,000 |
| database | 4,763 | 7,881 | 14,947 |
| incident-response | 0 | 7,500 | 25,000 |
| g&a | 1,000 | 7,200 | 23,600 |
| payments | 1,200 | 3,600 | 12,000 |
| identity | 3,000 | 3,000 | 3,000 |
| charity-verification | 2,750 | 2,750 | 9,900 |
| support | 600 | 1,200 | 3,000 |
| **Subtotal** | 292,100 | 610,843 | 1,335,028 |

| Total (fixed, annual) | Low | Base | High |
|---|---:|---:|---:|
| Economic (founders at market) incl. 7.5% contingency | 820,070 | **1,308,094** | 2,298,388 |
| Cash (founder cash salaries) | | **1,115,745** | |

Excludes per-account variable costs, startup, sponsor-specific onboarding/migration. Roles, authority, SoD pairs, backup, December cover and hiring triggers: staffing-models.csv.

Assessment: cash saving vs B is $544,261 but economic saving only $351,913; ~$610,843 of non-personnel cost (assurance, insurance, legal, vCISO, retainers) does not shrink with headcount. Viable only for 1 sponsor / <~1,500-2,000 accounts and only if the sponsor co-approves payments (three-person team cannot otherwise sustain dual control during absence). Third core person is a controller-grade finance & grant operations lead at market pay. Founder unpaid market-value gap = $192,349/yr and is a real cost (opportunity cost / later catch-up).

## Model B budget: lean independent (5 core, existing structure re-priced)

**Model B lean independent (5 core)** — core FTE 5

| Role | FTE | Base | Employer taxes | Benefits | Loaded (economic) | Loaded (cash) | P/S |
|---|---:|---:|---:|---:|---:|---:|---|
| Founder / CEO-managing director (sponsor relationships, sales, governance) | 1 | 165,000 | 13,594 | 21,548 | 200,142 | 200,142 | shared |
| CTO / technical lead (architecture, security, DR, AI controls) | 1 | 185,000 | 15,134 | 22,348 | 222,482 | 222,482 | software platform |
| Senior software engineer (full-stack, ledger, integrations) | 1 | 155,000 | 12,810 | 21,148 | 188,958 | 188,958 | software platform |
| Controller / head of financial operations | 1 | 150,000 | 12,417 | 20,948 | 183,365 | 183,365 | staffed administration |
| Grant & client operations specialist | 1 | 75,000 | 6,530 | 17,948 | 99,478 | 99,478 | staffed administration |
| **Personnel** | 5 | | | | **894,424** | **894,424** | |

| Non-personnel & contracted by category | Low | Base | High |
|---|---:|---:|---:|
| assurance | 55,000 | 110,000 | 250,000 |
| insurance | 38,000 | 84,000 | 176,000 |
| security-testing | 34,000 | 68,000 | 131,000 |
| personnel | 26,295 | 47,970 | 90,770 |
| accounting | 23,500 | 45,000 | 92,000 |
| compliance | 18,000 | 45,000 | 90,000 |
| legal | 30,000 | 45,000 | 80,000 |
| sales | 15,500 | 42,000 | 86,000 |
| cloud | 20,088 | 37,088 | 86,144 |
| marketing | 5,000 | 20,000 | 60,000 |
| software | 9,417 | 19,817 | 52,882 |
| travel | 7,500 | 15,000 | 25,000 |
| dr-bcp | 6,559 | 13,119 | 31,237 |
| ai | 3,000 | 12,000 | 36,000 |
| g&a | 1,000 | 10,200 | 35,600 |
| database | 6,406 | 9,524 | 17,420 |
| data | 3,000 | 8,000 | 25,000 |
| incident-response | 0 | 7,500 | 25,000 |
| payments | 1,200 | 3,600 | 12,000 |
| identity | 3,000 | 3,000 | 3,000 |
| charity-verification | 2,750 | 2,750 | 9,900 |
| support | 600 | 1,200 | 3,000 |
| **Subtotal** | 309,815 | 649,768 | 1,417,953 |

| Total (fixed, annual) | Low | Base | High |
|---|---:|---:|---:|
| Economic (founders at market) incl. 7.5% contingency | 1,085,589 | **1,660,006** | 2,770,034 |
| Cash (founder cash salaries) | | **1,660,006** | |

Excludes per-account variable costs, startup, sponsor-specific onboarding/migration. Roles, authority, SoD pairs, backup, December cover and hiring triggers: staffing-models.csv.

Assessment: same roles as the existing hypothesis. Structural weakness: one ops specialist; controller backing ops collapses preparer/releaser separation on the same item, so a 2nd ops specialist (or sponsor co-approval) is needed for any absence >2 weeks; that is +$99k loaded and is the first hiring trigger, likely before 2,500 accounts.

## Model C budget: established (12 core)

**Model C established (12 core, specialization, redundancy)** — core FTE 12

| Role | FTE | Base | Employer taxes | Benefits | Loaded (economic) | Loaded (cash) | P/S |
|---|---:|---:|---:|---:|---:|---:|---|
| Founder / CEO-managing director (sponsor relationships, sales, governance) | 1 | 165,000 | 13,594 | 21,548 | 200,142 | 200,142 | shared |
| CTO / technical lead (architecture, security, DR, AI controls) | 1 | 185,000 | 15,134 | 22,348 | 222,482 | 222,482 | software platform |
| Senior software engineer (full-stack, ledger, integrations) | 2 | 155,000 | 25,619 | 42,296 | 377,915 | 377,915 | software platform |
| Security / infrastructure engineer (DevSecOps, IAM, DR) | 1 | 145,000 | 12,024 | 20,748 | 177,772 | 177,772 | software platform |
| Controller / head of financial operations | 1 | 150,000 | 12,417 | 20,948 | 183,365 | 183,365 | staffed administration |
| Fund / grant accountant (reconciliation, close) | 1 | 85,000 | 7,314 | 18,348 | 110,662 | 110,662 | staffed administration |
| Grant operations manager | 1 | 120,000 | 10,062 | 19,748 | 149,810 | 149,810 | staffed administration |
| Grant & client operations specialist | 2 | 75,000 | 13,059 | 35,896 | 198,955 | 198,955 | staffed administration |
| Compliance officer (charity due diligence, sanctions, policy, audit liaison) | 1 | 95,000 | 8,100 | 18,748 | 121,848 | 121,848 | shared |
| Implementation / client success analyst (sponsor onboarding, migration) | 1 | 100,000 | 8,492 | 18,948 | 127,440 | 127,440 | staffed administration |
| **Personnel** | 12 | | | | **1,870,392** | **1,870,392** | |

| Non-personnel & contracted by category | Low | Base | High |
|---|---:|---:|---:|
| assurance | 55,000 | 110,000 | 250,000 |
| personnel | 45,700 | 95,160 | 192,760 |
| insurance | 38,000 | 84,000 | 176,000 |
| sales | 30,500 | 82,000 | 166,000 |
| legal | 48,000 | 72,000 | 128,000 |
| cloud | 30,468 | 55,968 | 129,696 |
| marketing | 12,500 | 50,000 | 150,000 |
| software | 21,378 | 40,178 | 98,060 |
| travel | 18,000 | 36,000 | 60,000 |
| compliance | 12,000 | 30,000 | 60,000 |
| security-testing | 10,000 | 20,000 | 35,000 |
| g&a | 1,500 | 17,700 | 63,600 |
| dr-bcp | 6,559 | 13,119 | 31,237 |
| accounting | 6,500 | 13,000 | 26,000 |
| database | 9,693 | 12,811 | 22,366 |
| ai | 3,000 | 12,000 | 36,000 |
| data | 3,000 | 8,000 | 25,000 |
| incident-response | 0 | 7,500 | 25,000 |
| payments | 1,200 | 3,600 | 12,000 |
| identity | 3,000 | 3,000 | 3,000 |
| charity-verification | 2,750 | 2,750 | 9,900 |
| support | 1,200 | 2,400 | 6,000 |
| **Subtotal** | 359,948 | 771,186 | 1,705,619 |

| Total (fixed, annual) | Low | Base | High |
|---|---:|---:|---:|
| Economic (founders at market) incl. 7.5% contingency | 1,970,893 | **2,839,696** | 4,374,571 |
| Cash (founder cash salaries) | | **2,839,696** | |

Excludes per-account variable costs, startup, sponsor-specific onboarding/migration. Roles, authority, SoD pairs, backup, December cover and hiring triggers: staffing-models.csv.

Assessment: specialised and redundant (two payment releasers, security engineer replaces vCISO, compliance officer replaces consultant, implementation analyst absorbs onboarding labour). Fractional/outsourced finance roles drop out. This is the structure sponsors' risk committees and SOC 1 auditors will most readily accept; its fixed cost alone equals revenue at $1.42B average billable AUA at 20 bps, before variable costs and margin [D: total / 0.002].

## Contracted and fractional services

| ID | Service | Driver | Low | Base | High | Q | Note |
|---|---|---|---:|---:|---:|---|---|
| CST-C01 | Fractional CFO / controller review | per hour | 125 | 200 | 450 | C | Search summaries: GoFractional observed average $174/h, IQR $125-200; NerdWallet $150-500/h, retainers $3k-10k/month. Not read directly. |
| CST-C02 | Outsourced bookkeeping / monthly close | per month | 1000 | 2000 | 4000 | D | [A] no public price list read. Preserves separation: outsourced books, controller reviews. |
| CST-C03 | Fractional vCISO | per year | 24000 | 48000 | 96000 | D | [A] ~4-16 h/month at $250-500/h; replaced by security engineer in Model C. |
| CST-C04 | Compliance consultant (sanctions program, due-diligence policy, annual independent review) | per year | 10000 | 25000 | 50000 | D | [A] Replaced by compliance officer in Model C except independent review. |
| CST-C05 | Contracted engineering retainer (backup for sole technical lead) | per year | 15000 | 30000 | 60000 | D | [A] Model A only; key-person mitigation, documented runbooks required. |
| CST-C06 | Outside counsel (nonprofit/tax-exempt + financial services), hourly | per hour | 300 | 450 | 800 | C | Clio average lawyer rate $349 (Jan 2025) and $362 (2026); corporate practice ~$461 (search summaries; Clio pages 403 to fetcher). Specialist |
| CST-C07 | Startup legal: formation, sponsor MSA/SLA templates, privacy, data processing, employment | one-time | 40000 | 80000 | 150000 | D | [A] |
| CST-C08 | Regulatory opinion: money transmission / agent-of-payee, state charitable solicitation, UPMIFA/agency boundary | one-time | 15000 | 40000 | 100000 | D | [A] Critical: if the servicer moves sponsor funds through its own accounts, state money-transmitter licensing could apply; designing payment |
| CST-C09 | Independent audit of the company's own financial statements | per year | 20000 | 35000 | 60000 | D | [A] no public fee schedule; small private company audit. May be deferred to review engagement in year 1 if contracts allow. |
| CST-C10 | Corporate tax returns (federal + states) | per year | 5000 | 10000 | 20000 | D | [A] remote-first => multi-state payroll/nexus filings. |
| CST-P14 | Seasonal temporary grant processor (December peak), agency bill rate | per temp hour | 34 | 39 | 49 | D | [D] BLS 43-3031 median hourly $24.36 x agency markup 1.4/1.6/2.0 [A]. Requires training and restricted permissions; cannot approve payments. |
| CST-P21 | PEO admin fee (Justworks PEO Basic $79/employee-month) | per employee-year | 216 | 948 | 1488 | C | Already INCLUDED in loaded cost (benefits). Do not add again. Low = payroll-only $8/employee-mo + share of $50 base [C]; high = PEO Plus $12 |

Observations: fractional CFO and outside counsel are the only contracted lines with any public rate evidence (C-quality aggregates). Bookkeeping, audit and tax fees have no public price lists; ranges are [A]. The single most important legal item is the regulatory opinion (CST-C08) on whether payment-processing as agent for sponsors triggers money-transmitter licensing; the answer changes the payments architecture and possibly the cost base materially.

## Technology and vendor costs

Public price lists read 2026-11-25 (A unless noted).

| ID | Item | Unit | Low | Base | High | Type | Q |
|---|---|---|---:|---:|---:|---|---|
| CST-T01 | Managed PostgreSQL primary, zone-redundant HA (Azure Flexible Server D | USD/yr | 3119 | 6237 | 12474 | fixed | A |
| CST-T02 | Cross-region PostgreSQL read replica for DR (same size, single instanc | USD/yr | 1559 | 3119 | 6237 | fixed | A |
| CST-T03 | PostgreSQL provisioned storage | USD/GB-month | 0.115 | 0.115 | 0.135 | variable | A |
| CST-T04 | PostgreSQL backup storage (LRS) | USD/GB-month | 0.095 | 0.095 | 0.2 | variable | A |
| CST-T05 | Application hosting, networking, WAF, KMS, object storage, egress (pro | USD/yr | 12000 | 24000 | 60000 | fixed | D |
| CST-T07 | Infrastructure monitoring (Datadog Infra Pro) | USD/host-month | 15 | 15 | 18 | step-fixed | A |
| CST-T08 | APM (Datadog, with infra) | USD/host-month | 31 | 31 | 36 | step-fixed | A |
| CST-T09 | Log ingest (Datadog) | USD/GB | 0.1 | 0.1 | 0.1 | variable | A |
| CST-T10 | Log indexing 15-day (Datadog) | USD/M events | 1.7 | 1.7 | 2.55 | variable | A |
| CST-T12 | AI inference per grant screening call | USD/grant | 0.00065 | 0.026 | 0.14 | transaction | A |
| CST-T13 | AI inference, all workflows (screening, donor support drafting, reconc | USD/account-yr | 0.1 | 0.75 | 4 | variable | D |
| CST-D01 | IRS EO BMF extract (and TEOS bulk data incl. Pub 78/auto-revocation) | USD/yr | 0 | 0 | 0 | fixed | A |
| CST-D02 | OFAC Sanctions List Service (SDN + consolidated) | USD/yr | 0 | 0 | 0 | fixed | A |
| CST-D03 | Candid Charity Check API | USD/yr (starting at) | 2750 | 2750 | 9900 | fixed | B |
| CST-D04 | Candid Nonprofit Eligibility API | USD/yr (starting at) | 5000 | 5000 | 15000 | fixed | B |
| CST-D05 | Commercial sanctions/PEP/adverse-media screening subscription | USD/yr | 3000 | 8000 | 25000 | fixed | D |
| CST-ID1 | Persona Essential plan (500 services/month included) | USD/yr | 3000 | 3000 | 3000 | fixed | A |
| CST-ID2 | Identity verification overage per service | USD/verification | 1 | 1.5 | 3 | transaction | B |
| CST-PY1 | ACH credit origination, next-day (grants out) | USD/payment | 0.1 | 0.5 | 0.5 | transaction | A |
| CST-PY2 | ACH same-day origination | USD/payment | 1 | 1.5 | 2 | transaction | A |
| CST-PY3 | Wire origination | USD/payment | 15 | 20 | 25 | transaction | A |
| CST-PY4 | RTP / FedNow origination | USD/payment | 2.5 | 2.5 | 2.5 | transaction | A |
| CST-PY5 | Check printing and mailing | USD/check | 1.04 | 3 | 8 | transaction | A |
| CST-PY6 | Lob plan fee (if Lob used) | USD/yr | 0 | 3120 | 6600 | fixed | A |
| CST-PY9 | Incoming check lockbox processing | USD/check | 0.65 | 0.65 | 1.5 | transaction | B |
| CST-PY10 | Card/ACH debit contribution acceptance (Stripe ACH 0.8% capped $5) | USD/contribution | 0 | 5 | 5 | pass-through | A |
| CST-PY11 | Modern Treasury payment operations platform | USD/yr | 0 | 0 | 0 | fixed | D |
| CST-CM1 | Transactional email (Postmark Pro, 10k/month incl.) | USD/month | 16.5 | 16.5 | 18 | variable | A |
| CST-CM2 | SMS (Twilio US outbound incl. carrier fee) | USD/segment | 0.0118 | 0.0128 | 0.0133 | transaction | A |
| CST-CM3 | Paper statements / tax receipts (Lob first-class letter) | USD/piece | 0.628 | 0.658 | 0.828 | transaction | A |
| CST-S01 | Google Workspace Business Standard | USD/user-yr | 168 | 168 | 202 | fixed | C |
| CST-S02 | Slack (Pro / Business+) | USD/user-yr | 87 | 87 | 180 | fixed | A |
| CST-S03 | GitHub (Team / Enterprise) | USD/user-yr | 48 | 48 | 252 | fixed | A |
| CST-S04 | AI assistant seats (ChatGPT Standard/Premium class; Claude plans compa | USD/user-yr | 240 | 240 | 1200 | fixed | A |

**Database sizing [D]:** Azure PostgreSQL Flexible Server 4 vCore Ddsv5 with zone-redundant HA ≈ $6,237/yr + cross-region DR replica $3,119 + storage/backup ≈ $3.3k: a production-grade HA+DR database is **~$13k/yr**, ~one-third of the existing $36k cloud line. Compute is cheap; people, assurance and insurance dominate. AWS RDS equivalent not extracted (gap).

**AI [D]:** at current list prices a Sonnet-class screening call (8k in/1k out) is ~$0.026; Haiku-class batch ~$0.0007; Opus-class 20k/3k ~$0.14. Even at 10 grants/account-yr with Opus everywhere, AI is <$2/account-yr. AI is not a material cost line; its risk is quality/oversight labour, not tokens.

**Charity data:** IRS EO BMF and OFAC SLS are free downloads; Candid APIs start at $2,750-9,900 (term/volume unpublished). Persona identity: $3,000/yr plan + $1.50/verification. Commercial sanctions screening: no public price.

**Payments:** public per-item prices ACH $0.50 (same-day $1-2), wire $15-25, RTP $2.50, check print+mail $1.04-3.00. Modern Treasury: no public price. If grants are paid from the sponsor's own bank account, these are sponsor pass-through, not servicer cost.

**Indicative non-labour variable cost per account-year [D, A-inputs: 10 grants/account (Unbound range 6.2-13), 90% ACH]:**
| Component | $/account-yr | Source |
|---|---:|---|
| Grant payments (9 ACH x $0.50 + 1 check x $3.00) | 7.50 | CST-PY1, PY5 |
| ACH returns (0.5% x 10 x $5) | 0.25 | CST-PY7 |
| Identity verification (15% new/re-verified x $1.50) | 0.22 | CST-ID2 |
| AI inference all workflows | 0.75 | CST-T13 |
| SMS (10 segments) + email | 0.18 | CST-CM2, CM1 |
| Paper statements/receipts (20% paper x 4 x $0.658) | 0.53 | CST-CM3 |
| Incremental cloud/storage [A] | 1.00 | Unbound infra_per_account 3.0 (0.5-6) [A] |
| **Total non-labour** | **10.43** | vs existing $35 non-labour ($10 payments + $10 data/identity + $5 cloud + $10 other) |

The existing $10 data/identity per account is overstated as a *variable* cost: the data/identity spend is mostly fixed subscriptions (~$14k/yr in Model B), already in the fixed budget here. Labour, not vendors, drives variable cost: at $65.45/h every 10 minutes per account-year = $10.91.

## Insurance and assurance

| ID | Item | Low | Base | High | Type | Q |
|---|---|---:|---:|---:|---|---|
| CST-I01 | Cyber liability $1M limit, generic small business (benchmark only) | 999 | 1,740 | 7,500 | fixed | C |
| CST-I02 | Cyber liability (1st+3rd party) $5M, payments-adjacent SaaS | 15,000 | 30,000 | 60,000 | fixed | D |
| CST-I03 | Technology E&O / professional liability $5M | 10,000 | 25,000 | 50,000 | fixed | C |
| CST-I04 | D&O $1-2M | 5,000 | 10,000 | 20,000 | fixed | C |
| CST-I05 | Commercial crime incl. third-party/client property, funds transfer fraud, social | 5,000 | 12,000 | 30,000 | fixed | D |
| CST-I06 | EPLI | 2,000 | 4,000 | 8,000 | fixed | D |
| CST-I07 | General liability / umbrella | 1,000 | 3,000 | 8,000 | fixed | D |
| CST-C11 | SOC 2 Type 2 examination (CPA firm) | 15,000 | 35,000 | 70,000 | fixed | C |
| CST-C12 | SOC 1 Type 2 examination (ICFR-relevant controls for sponsors' auditors) | 20,000 | 40,000 | 120,000 | fixed | C |
| CST-C13 | SOC readiness assessment + gap remediation support | 10,000 | 20,000 | 40,000 | startup | C |
| CST-C14 | Annual external penetration test (web app, API, cloud) + retest | 10,000 | 20,000 | 35,000 | fixed | C |
| CST-C15 | Compliance automation platform (Vanta/Drata class) | 8,000 | 20,000 | 40,000 | fixed | D |
| CST-C16 | Incident response retainer (often via cyber insurer panel) | 0 | 7,500 | 25,000 | fixed | D |
| CST-C17 | Breach / fraud incident response and notification (event) | 50,000 | 250,000 | 1,000,000 | extraordinary | D |
| CST-C18 | DR failover test + BCP tabletop facilitation | 5,000 | 10,000 | 25,000 | fixed | D |

Insurance programme total [D]: **$38,000 / $84,000 / $176,000** vs existing $30,000. Public benchmarks exist only for generic small businesses ($1M cyber ~$1-1.7k/yr; 2021 startup E&O/D&O averages $5-17k); a servicer processing charitable payments will face higher limits ($5M+) demanded by sponsors, crime/social-engineering cover and underwriting scrutiny. All programme figures beyond those benchmarks are [A].

Assurance/security recurring (SOC 2 T2 + SOC 1 T2 + pen test + compliance automation + IR retainer + DR test) base **$132,500** before vCISO/security engineer, vs existing $65,000 for 'security/assurance'. A software-only licence needs SOC 2; staffed administration that touches sponsors' financial reporting needs SOC 1 (with bridge letters). Phasing [A]: year 1 SOC 2 Type 1 + SOC 1 Type 1 (~60% of Type 2 fees), Type 2 from year 2; sponsors may refuse go-live before a Type 2 report — a material sales-cycle risk.

## Startup and one-time costs

**Model A founder-led (3 core + fractional + contractors + automation)**
| Item | Low | Base | High |
|---|---:|---:|---:|
| Incorporation/filings (ST1) | 500 | 2,000 | 5,000 |
| Startup legal (C07) | 40,000 | 80,000 | 150,000 |
| Regulatory opinion (C08) | 15,000 | 40,000 | 100,000 |
| SOC readiness (C13) | 10,000 | 20,000 | 40,000 |
| Initial pen test pre-launch (C14) | 10,000 | 20,000 | 35,000 |
| Brand/website (ST2) | 5,000 | 15,000 | 40,000 |
| Implementation/migration tooling (ST3) | 10,000 | 40,000 | 120,000 |
| Recruiting 3 initial hires (P16) | 3,900 | 45,000 | 135,000 |
| Equipment 3 FTE (3-yr laptops upfront) | 7,200 | 9,000 | 13,500 |
| One-time subtotal | 101,600 | 271,000 | 638,500 |
| Pre-revenue build/run at cash burn (9/12/18 months) [A] | 836,809 | 1,115,745 | 1,673,618 |
| Working capital (2/3/4 months fixed cash opex; billing in arrears) [A] | 185,958 | 278,936 | 371,915 |
| **Indicative capital need** | **1,124,366** | **1,665,682** | **2,684,033** |
Insurance binding: ~$84,000 first-year premiums payable upfront or in instalments (timing only).

**Model B lean independent (5 core)**
| Item | Low | Base | High |
|---|---:|---:|---:|
| Incorporation/filings (ST1) | 500 | 2,000 | 5,000 |
| Startup legal (C07) | 40,000 | 80,000 | 150,000 |
| Regulatory opinion (C08) | 15,000 | 40,000 | 100,000 |
| SOC readiness (C13) | 10,000 | 20,000 | 40,000 |
| Initial pen test pre-launch (C14) | 10,000 | 20,000 | 35,000 |
| Brand/website (ST2) | 5,000 | 15,000 | 40,000 |
| Implementation/migration tooling (ST3) | 10,000 | 40,000 | 120,000 |
| Recruiting 5 initial hires (P16) | 6,500 | 75,000 | 225,000 |
| Equipment 5 FTE (3-yr laptops upfront) | 12,000 | 15,000 | 22,500 |
| One-time subtotal | 109,000 | 307,000 | 737,500 |
| Pre-revenue build/run at cash burn (9/12/18 months) [A] | 1,245,005 | 1,660,006 | 2,490,010 |
| Working capital (2/3/4 months fixed cash opex; billing in arrears) [A] | 276,668 | 415,002 | 553,335 |
| **Indicative capital need** | **1,630,673** | **2,382,008** | **3,780,845** |
Insurance binding: ~$84,000 first-year premiums payable upfront or in instalments (timing only).

**Model C established (12 core, specialization, redundancy)**
| Item | Low | Base | High |
|---|---:|---:|---:|
| Incorporation/filings (ST1) | 500 | 2,000 | 5,000 |
| Startup legal (C07) | 40,000 | 80,000 | 150,000 |
| Regulatory opinion (C08) | 15,000 | 40,000 | 100,000 |
| SOC readiness (C13) | 10,000 | 20,000 | 40,000 |
| Initial pen test pre-launch (C14) | 10,000 | 20,000 | 35,000 |
| Brand/website (ST2) | 5,000 | 15,000 | 40,000 |
| Implementation/migration tooling (ST3) | 10,000 | 40,000 | 120,000 |
| Recruiting 12 initial hires (P16) | 15,600 | 180,000 | 540,000 |
| Equipment 12 FTE (3-yr laptops upfront) | 28,800 | 36,000 | 54,000 |
| One-time subtotal | 134,900 | 433,000 | 1,084,000 |
| Pre-revenue build/run at cash burn (9/12/18 months) [A] | 2,129,772 | 2,839,696 | 4,259,544 |
| Working capital (2/3/4 months fixed cash opex; billing in arrears) [A] | 473,283 | 709,924 | 946,565 |
| **Indicative capital need** | **2,737,955** | **3,982,620** | **6,290,109** |
Insurance binding: ~$84,000 first-year premiums payable upfront or in instalments (timing only).

Existing runway hypothesis: 12 months $1.178M + $250k launch reserve = $1.428M. Rebuilt Model B (12 months) is materially higher; sponsor-specific onboarding ($10-75k) and migration ($25-250k) per sponsor (CST-OM1/OM2) are customer-specific and additional. These are illustrative capital ranges, not a financing plan.

## Reconciliation against existing $1,177,750

Line-by-line, existing (EV-CST-074) vs rebuilt Model B (same 5 roles) [D].

| Existing line | Existing | Rebuilt low | Rebuilt base | Rebuilt high | Delta (base) | Finding |
|---|---:|---:|---:|---:|---:|---|
| Loaded personnel | 743,750 | 724,079 | 894,424 | 1,100,260 | 150,674 | UNDERSTATED. Salaries re-based on OEWS May 2025 + postings: CTO 150k->185k, engineer 120k->155k, controller 115k->150k, MD 130k->165k, ops 80k->75k. Burden 1.25 confirmed for professionals by ECEC (1.226) but ops role is ~1.33. |
| Legal/compliance | 60,000 | 48,000 | 90,000 | 170,000 | 30,000 | Roughly right in total but mixes items; regulatory (money-transmission) opinion is a startup cost not in the budget. |
| Independent accounting/controls | 45,000 | 43,500 | 80,000 | 152,000 | 35,000 | UNDERSTATED: audit + tax + outsourced books + CFO review; outsourced books preserves SoD for a single controller. |
| Seasonal/backup coverage | 60,000 | 16,320 | 18,720 | 23,520 | -41,280 | OVERSTATED for December temps (~$19k), but the real backup need (2nd ops FTE ~$99k loaded) is MISSING: the line cannot buy dual-control coverage. |
| Cloud/monitoring | 36,000 | 28,053 | 49,731 | 109,801 | 13,731 | Roughly right/slightly high at launch scale: HA+DR PostgreSQL ~$13k; hosting assumption dominates. |
| Security/assurance | 65,000 | 77,000 | 166,500 | 383,000 | 101,500 | MATERIALLY UNDERSTATED: SOC 2 T2 + SOC 1 T2 + pen test + vCISO + IR + DR test. |
| Insurance | 30,000 | 38,000 | 84,000 | 176,000 | 54,000 | UNDERSTATED: payments-adjacent servicer needs $5M cyber/E&O plus crime incl. third-party/social engineering. |
| Business software | 18,000 | 7,517 | 17,017 | 49,882 | -983 | Roughly right; per-user SaaS is small. |
| Sales/travel | 40,000 | 27,500 | 75,000 | 165,000 | 35,000 | Kept $40k conferences; adds marketing and remote-team travel. |
| General administration | 20,000 | 12,175 | 43,050 | 114,850 | 23,050 | UNDERSTATED: recruiting, equipment, training, filings, bank treasury fees were missing. |
| NOT IN EXISTING: AI fixed, charity data, identity, sanctions subscriptions | 0 | 11,750 | 25,750 | 73,900 | 25,750 | MISSING as fixed costs (existing put $10/account data/identity in variable). |
| Contingency | 60,000 | | 115,814 | | 55,814 | 7.5% (5-10%) of cash opex vs 5.4% |
| **Total** | **1,177,750** | **1,085,589** | **1,660,006** | **2,770,034** | **482,256** | |

Interpretation: the existing number sits near the rebuilt **low** case (all inputs at the favourable end simultaneously). The base case is ~41% higher. Break-even AUA at 20 bps scales proportionally: F/r alone moves from $589M to $830M before any variable cost [D]. Missing entirely from both: equity compensation, sales commission, sponsor onboarding/migration labour, and the second ops FTE needed for dual control.

$75/account placeholder: non-labour components re-estimated at ~$10/account-yr (vs $35); labour at $65.45/h (vs $50) so $40 buys ~37 min. Net effect on v depends on measured minutes/account (activity group).

## Cost separation: software platform vs staffed administration

Every register line is tagged platform / staffed / shared (column platform_or_staffed). Base annual fixed cost by tag (before contingency) [D]:

| Tag | Model A | Model B | Model C |
|---|---:|---:|---:|
| software platform | 421,909 | 584,262 | 925,255 |
| staffed administration | 285,645 | 391,362 | 871,192 |
| shared | 509,278 | 568,568 | 845,130 |

Rules to avoid double counting:
1. **One platform cost pool.** Engineering, cloud, SOC 2, pen test, AI fixed, monitoring, data subscriptions are incurred once. If the company also sells software-only licences, the staffed administration P&L should carry an internal platform charge = platform pool / total accounts on platform, not an external licence price on top of the fixed budget.
2. **Unbound 05a staffed cost ($192/$299 per fund at 10k funds) is computed at a stated platform-cost scale** (column 'Platform cost scale'), while the market-entry note says sales, build capex and assurance sit in the vendor P&L outside it. So it neither replaces this fixed budget nor can be added on top of it; reconcile component by component (platform operations vs assurance vs sales vs staffing).
3. **SOC 1, crime insurance, payment operations, charity verification labour, controller, ops staff** belong to staffed administration; a software-only business avoids most of them (but sponsor then bears them).
4. **Shared** (CEO, legal, D&O, cyber, E&O, G&A, compliance officer) must be allocated by an explicit key (e.g. revenue or headcount), never fully to both.
5. **Pass-through and sponsor-retained** (grant principal, investment fees, donor-facing fees, bank fees on sponsor-owned accounts, sponsor reserved-decision labour ~$42-43/fund) are excluded from servicer cost and revenue.
6. Data/identity subscriptions are fixed (here) and only overage is variable; do not also put $10/account in v.

## Evidence gaps

1. **BLS direct access**: bls.gov tables/API blocked or throttled; OEWS read via O*NET (same data, secondary host). ECEC tables read directly. Industry-specific OEWS (NAICS 5239/5242/8132) not extracted — national all-industry medians may understate fintech and overstate nonprofit pay.
2. **No public prices**: Vanta/Drata, Modern Treasury, commercial sanctions screening, bookkeeping, CPA audit/tax, e-signature, most insurance lines. Ranges are [A]. Broker quotes would require outreach (not permitted).
3. **Insurance**: only generic small-business and dated (2021) startup averages; sponsor-mandated limits unknown. Highest uncertainty non-labour line ($38,000-$176,000).
4. **SOC 1/SOC 2 fees**: vendor-blog ranges only (C); Schellman chart not machine-readable.
5. **Legal rates**: Clio aggregates (C); specialist exempt-org + money-transmission counsel rates and the regulatory conclusion itself are unknown and potentially decisive.
6. **AWS RDS / GCP prices** not extracted; Azure used as the cloud reference.
7. **Productive hours, minutes per activity, December peak multiple** unmeasured; 1,520 h is [D/A].
8. **Postings**: four verified; all closed/removed; no verified DAF-servicer (Ren, Stellar, TIFIN Give, Chariot) posting with pay range read. Search-only postings excluded.
9. **Equity compensation** for founders/early staff excluded; can materially change true economic cost of Model A/B.
10. Same-model analysis; no independent reviewer.

## ECH-0 Scope, method and revisions

Group ECH (Echelon capabilities + Clarity/EDF method). Read-only. Nothing committed.

**Revisions read (git rev-parse --short HEAD, 2026-11-25):**

| Repository | Revision |
|---|---|
| clarity-framework | 200a9eb (200a9ebf029c051eac625bb5185929b20c8d5aed, 2026-11-16) |
| echelon-diagnostic-framework | 710d54c (710d54c20e935db8b6f75f9c60ee7217f0cb0e32, 2026-11-17) |
| Echelon-AI-Native-Enterprise-Design-Framework | 763ff8c (2026-11-20) |
| AI-Engineering | 1bc519b (2026-09-30) |
| unbound | 9b38de4 (2026-11-24) |
| daf-landscape | e1a3633 (2026-11-25) |

**What 'verified-existing' means here:** the artefact (code, test file, vendored package, measured result file, document) was opened and read in this session at the cited path. No build, test or CLI was executed: there is no .NET SDK in this session, so the Echelon F# test suite (87 test attributes counted statically) and the Unbound replay (20 test attributes) were NOT re-run; their pass status rests on each repo's own ledger. Forma, Limen, Folio, Aegis, Praxis, Conditor, Strata, Tutela and Fides upstream repositories are NOT among the local clones; statements about them come from two prior read-only inspections by agents of the same programme (daf-landscape `research/ai-native-daf-enterprise/07-technology-architecture/echelon-component-assessment.md`, 2026-11-20; unbound `07-ECHELON-CAPABILITY-ASSESSMENT.md`, 2026-11-24). Those are labelled described-not-verified unless a vendored copy exists locally. Same-model reasoning is not independent validation.

## ECH-1 What Echelon systems actually exist

22 capabilities assessed (file `echelon-capabilities.csv`). Status counts: absent 6, described-not-verified 5, planned 2, verified-existing 9.

| ID | Capability | Status | Effect | Annual effect low/high [A] |
|---|---|---|---|---|
| ECH-01 | Shared engineering organisation (Echelon Foundry staff available to the DAF business) | absent | transfer | $0 / $0 |
| ECH-02 | Automated software development (AI coding agents with Praxis work protocol/provenance) | described-not-verified | eliminate | $0 / $150,000 |
| ECH-03 | Automated testing practice (xUnit/property tests, CI fail-on-empty) | verified-existing | share | $0 / $15,000 |
| ECH-04 | Deployment automation (GitHub Actions CI; Conditor repository bootstrap; Pages deploy) | described-not-verified | share | $0 / $10,000 |
| ECH-05 | Forma UI design system (CSS/HTML tokens, components) | verified-existing | share | $0 / $20,000 |
| ECH-06 | Limen browser kernel/engine boundary (TypeScript kernel, F# WASM seam) | described-not-verified | none | $0 / $0 |
| ECH-07 | Folio document generation (print web components) | verified-existing | share | $0 / $10,000 |
| ECH-08 | Component (modular) monolith DAF application | planned | none | $0 / $0 |
| ECH-09 | PostgreSQL system of record (managed PostgreSQL) | planned | none | $0 / $0 |
| ECH-10 | Strata schema governance (declarative PostgreSQL 16 DDL) | described-not-verified | share | $0 / $5,000 |
| ECH-11 | Runtime security (identity, access control, secrets, threat controls: Tutela/Fides/Aegis) | absent | none | -$40,000 / $0 |
| ECH-12 | SDLC governance and agent provenance (Praxis work protocol, records, telemetry) | described-not-verified | share | $0 / $10,000 |
| ECH-13 | Monitoring and logging | absent | none | $0 / $0 |
| ECH-14 | Data access: public-data eligibility and sanctions screening reference (Unbound replay, Screening.fs) | verified-existing | share | $0 / $25,000 |
| ECH-15 | UI and experience specifications (140 screens, rendered mock-ups, brand manifest) | verified-existing | share | $0 / $10,000 |
| ECH-16 | AI-readable documentation (AGENTS.md conventions, EKS export) | verified-existing | share | $0 / $10,000 |
| ECH-17 | Requirements, control register and governance baseline (Unbound) | verified-existing | share | $0 / $15,000 |
| ECH-18 | Echelon AI-Native Enterprise Design Framework (EEF) modelling | verified-existing | none | $0 / $0 |
| ECH-19 | Shared organisational administration (HR, payroll, finance, insurance, office) | absent | transfer | $0 / $0 |
| ECH-20 | Commercial licence for Echelon components (PolyForm NC across most of the stack) | absent | none | -$50,000 / $0 |
| ECH-21 | Running Echelon production infrastructure (hosting, on-call, environments) | absent | none | $0 / $0 |
| ECH-22 | Clarity and EDF methods | verified-existing | none | $0 / $0 |

**Key facts.**
- **No DAF application exists.** Unbound is requirements-only: 'No application code' (unbound `requirements/convergence/2026-11-24-master/LEDGER.md:4`); charter principle 8 forbids implementation before the gate; readiness PASS for architecture, FAIL for production. The modular monolith on managed PostgreSQL is an owner-ratified *decision* (CNV-ARC-001, `AUTHORITATIVE-BASELINE.md:77`), and the database engine is 'not yet selected' in `architecture/TENANT-AWARE-PERSISTENCE-DESIGN.md:20`.
- **What is real and local:** the Echelon Enterprise Design Framework (F#, 3,749 lines in `src/Echelon.Enterprise`, 87 test attributes, CI workflow file); Unbound's requirements baseline, 140-screen experience specs and rendered mock-ups; Unbound's public-data replay tool (F#) with committed results; a measured single-VM PostgreSQL 16 benchmark (2,100-3,900 tx/s on 4 vCPU vs ~200 tx/s peak need); vendored Forma 1.0.2 and Folio 0.4.2 copies, both **PolyForm Noncommercial 1.0.0** (LICENSE files read).
- **What does not exist:** runtime security (identity, access control, secrets: Aegis is a fault library, Fides is GitHub-only IdP, Tutela 0.1.0), monitoring/logging, a PDF render service (Folio has no renderer, no PDF/A or PDF/UA), production deployment pipeline, running production infrastructure (only static GitHub Pages sites), shared organisational administration, a second human maintainer, any external production user, and any commercial licence.
- **Automated software development** is real as practice (Claude-authored commits outnumber human ones in 7 of 14 Echelon repos per the 2026-11-20 inspection) but its productivity is unmeasured: AI-Engineering `HANDOFF.md:12-13` 'No agent capability trial or independent replication is claimed'; Unbound `PRINCIPLES.md:19` the Echelon-advantage hypothesis 'is **not yet established**'.
- The canonical Foundry engineering standard says 'No stack-specific standard is canonical in Phase 1 because the repository contains no implementation or supported stack evidence' (vendored copy `echelon-diagnostic-framework/docs/00-governance/Engineering-Standards.md:25`).

## ECH-2 Effect on the DAF servicer budget: eliminate vs share vs transfer

Budget under test: 5 FTE, $1,177,750 fixed (`daf-servicer-bottom-up-operating-budget-2026-11-25.md`). Positive = annual reduction of the servicer's cost; negative = added cost. All per-capability values are [A] (analyst placeholders, no quotes); totals are [D] sums.

| Measure | Value |
|---|---|
| Capabilities with effect 'eliminate' / 'share' / 'transfer' / 'none' | 1 / 10 / 2 / 9 |
| Share, verified-existing only (high bound) [D] | $105,000 |
| Share, all statuses (high bound) [D] | $130,000 |
| Eliminate, conditional on unverified AI productivity (high bound) [D] | $150,000 |
| Added cost: security review of single-maintainer AI-authored deps + licence placeholder (low bound) [D] | -$90,000 |
| Net range across all rows [D] | -$90,000 to $280,000 |

**Reading.** On verified evidence today the defensible annual reduction to the $1.18m budget is **$0 to about $105k** (0-10%) [D], all of it 'share' (reused conventions, UI CSS, print markup, specifications, public-data screening reference). The only 'eliminate' line (one engineer, up to $150k) depends on measured AI-development productivity that no repository demonstrates. Two items could *add* cost (independent security review; commercial licence). **Transfers are not savings:** Echelon/founder engineering time, shared administration and Unbound IP licensing all move cost between related entities and must be charged at cost. Burden Externalization (Clarity Candidate concept) is the failure pattern if they are not.

## ECH-3 What must remain attributable to the DAF business

- Platform build amortisation and run cost. The budget states 'actual development scope ... not covered'. Unbound's own vendor model carries build capex $5m (range $3m-$15m) [A] (`unbound/.../simplification-economics/model/parameters.json:509-516`), amortised over 5 years = $1.0m/yr base ($0.6m-$3.0m) [D]. If the servicer uses an Unbound platform, a share of that (by funds or transactions) belongs in its P&L, either as amortisation or a licence fee; a licence fee **transfers**, it does not eliminate.
- Every engineering, on-call and review hour on the DAF platform, whoever employs the person.
- Security/assurance ($65k), SOC 1/SOC 2 scope, penetration testing, incident response: no Echelon component reduces them.
- Cloud/monitoring ($36k): commodity; Echelon provides no running infrastructure.
- Independent accounting/controls ($45k): cannot be supplied by a related party without losing independence.
- Licence fees for PolyForm-NC components at arm's-length price, or the exit cost of replacing them.
- Screening outcomes (eligibility, sanctions) and the cost of any miss; the reference matcher missed 12 of 100 perturbed listed names (unbound `14-PUBLIC-DATA-REPLAY.md:47`).
- **Hidden assumption exposed:** the 2-engineer core implies that a working, maintained platform already exists. It does not. Prior daf-landscape modelling needs 4 engineering + 7 agent-ownership FTE at 1,000 accounts [A] (`research/ai-native-daf-enterprise/09-financial-models/financial-and-staffing-models.md:179-200`).

## ECH-4 Could Unbound develop and maintain software materially cheaper than a conventional enterprise software company?

Inputs [A]: loaded cost $165,000 per FTE (Unbound parameters base); conventional engineering 4-10 FTE (daf-landscape model, log scale); build capex $3m/$5m/$15m; 5-year amortisation. Outputs [D].

| Scenario | Engineering FTE | Annual engineering run cost [D] | Build amortisation/yr [D] (build x factor / 5) | Condition |
|---|---|---|---|---|
| S-conv: conventional enterprise build/run | 4-10 | $660,000-$1,650,000 | $600,000-$3,000,000 (base $1,000,000) | Comparator from prior models; 4 FTE at 1k accounts, 10 at 1m [A] |
| S0: Echelon reuse, no measured AI gain | 4-6 | $660,000-$990,000 | $600,000-$3,000,000 (base $1,000,000) | Reuse limited to UI CSS, print markup, test conventions, requirements; all DAF-specific build remains |
| S1: measured 1.5-2x agent-assisted throughput | 2-4 | $330,000-$660,000 | $342,857-$1,714,286 (base $571,429) | 4-6 FTE / 1.5-2x; requires measurement for >=6 months and independent review |
| S2: lean budget (2 engineering FTE) | 2-2 | $330,000-$330,000 | $300,000-$1,500,000 (base $500,000) | Requires >=2x throughput at the 4-FTE floor AND narrow servicing-only scope |

**Answer: conditional, not demonstrated.**
- S0 (what the evidence supports today): reuse removes front-end CSS, print markup, test conventions and requirements work only; DAF-specific ledger, payments, identity, tenancy, render service and security remain. Plausible reduction 0-16% of engineering run cost [D: verified share high bound $105,000 / $660,000; low bound 0].
- S1 (if agent-assisted throughput of 1.5-2x is measured and sustained): 33-50% lower engineering run cost [D: 1-1/1.5 to 1-1/2], i.e. about $0.22m (4 -> 2.67 FTE) to $0.50m (6 -> 3 FTE) a year less [D]. This would be material against a $1.18m budget. The S1 row rounds FTE to whole people.
- S2 (the lean budget: technical lead $187,500 + engineer $150,000 = $337,500 loaded [D from budget]) requires S1 *and* a narrow servicing-only scope *and* bought-in identity, PDF, monitoring and payment services. No evidence supports it yet.
- Offsetting costs specific to the Echelon route: single human maintainer (bus factor), 0.x churn (Praxis 11 minor releases in ~2 weeks; Forma namespace rename at 1.0), version drift between registry channel, tags and vendored copies, PolyForm NC licensing, and the need for independent review of AI-authored code.

**Evidence that would prove lower cost:** (1) Praxis/agent telemetry on the DAF codebase: accepted changes per engineer-month, escaped defects, rework, human intervention minutes, against a pre-registered baseline, >=6 months; (2) cost per accepted requirement or story point vs a conventional comparator; (3) maintenance hours per month for 12 months after go-live; (4) an independent security review and a clean SOC 1 Type II on the first sponsor; (5) a second engineer becoming productive from AI-readable docs within a stated time (bus-factor test); (6) published commercial licence terms. **Evidence that would disprove it:** throughput gain <1.2x, defect or rework rates above baseline, or Echelon hours that cannot be charged without breaking the budget.

## ECH-9 Findings and evidence gaps

**Five most consequential findings.**
1. No DAF application, production infrastructure, security layer, monitoring or shared administration exists in any Echelon or Unbound repository; only design artefacts, research tooling and vendored UI/print markup do.
2. On verified evidence the Echelon effect on the $1.18m servicer budget is 'share' of $0-$105k a year [D from A]; the only 'eliminate' candidate (AI-assisted development, up to $150k) is unmeasured; licence and security review may add cost.
3. The 5-FTE budget hides a platform build: Unbound's own assumption is $5m ($3m-$15m) build capex, about $1.0m/yr amortised base, which is not in the $1,177,750.
4. Nearly the whole Echelon UI/print stack is PolyForm Noncommercial; a commercial servicer is not obviously a 'charitable organization', so commercial licence terms ('forthcoming') are a launch gate and an attributable cost.
5. Neither framework can formally test the servicing assumptions: EDF needs an observed outcome; Clarity is a reasoning discipline whose own benchmark shows no accuracy gain. The template is structured adversarial analysis, not framework validation.

**Open gaps:** CI pass status of Echelon repos; package registry publication; Tutela/Fides/Arca inspection; agent-productivity measurement on a real codebase; commercial licence terms; money-transmission treatment of payment relay; any buyer evidence on price, minimums or switching; sponsor time study.
