# 05. Staffing derived from workload, coverage, qualifications and segregation of duties

Every role in [`roles.csv`](data/inputs/roles.csv) is justified by an activity workload or a coverage rule. Gate V6 rejects any other role, so there is no "conventional" headcount. Wages are BLS OEWS May 2025 medians (25th–75th percentile) × the BLS ECEC loading of 1.445, plus $6k a year of per-employee overhead (seats, devices, payroll provider, recruiting).

| Role | Loaded cost (base) | Contract rate (base) | Hire threshold (residual h/yr) | Why it exists |
|---|---|---|---|---|
| Management, sales and account management | $230k | $150/h | 1,400 | Founder overhead: 250 h fixed + 40 h per customer + 240 h per won customer (a 25% win rate on ~60 h pursuits) |
| Platform engineering | $197k | $120/h | 1,400 | Maintenance (500/900/1,800 h), security operations, data pipelines, incidents, restore tests; coverage rules CHG, BRK, ONC |
| Implementation | $140k | $110/h | 1,200 | Onboarding (120/300/600 h per new customer); migration projects (model M) |
| Support | $65k | $50/h | 1,300 | Sponsor-staff tickets; hypercare; donor contacts (full service only) |
| Charity and compliance analysis | $117k | $110/h | 1,000 | Eligibility exceptions, sanctions triage preparation, SOC evidence, auditor support |
| DAF operations analyst | $121k | $85/h | 1,300 | Limited operations and full service only: exception preparation, attribution, reconciliation, close, statements, December surge |

**Staffing rule:**
1. The founder (800/1,200/1,800 h a year available to the DAF business) fills eligible roles in the order above.
2. Residual work below the hire threshold is contracted. Thresholds are set near the cost-neutral point (loaded cost ÷ contract rate) with a modest reliability premium, following review findings ADV-O-07 and ADV-A-14.
3. Whole FTEs of residual work are employed, and a remainder above the threshold adds one more employee.

**Coverage rule.** A rule needing *k* distinct qualified people counts the following:
- the founder, only in a role the founder actually works;
- employees;
- one regular contractor with at least 400 h a year in the role.

Any shortfall is met by the cheaper of hiring and the rule's own retainer. A hire satisfies every rule on its role; a retainer satisfies only its own.

## Results (mixed sponsors, typical contracts, base)
| Customers | Licensing (L) | Full service (F) |
|---|---|---|
| 0 | Founder 1,180 h; nobody else | Same |
| 1 | Founder 1,200 h; contractors: engineering 870 h, implementation 90 h, compliance 120 h; one change-review retainer | Founder; contractors: engineering 870 h, operations 270 h, compliance 250 h; review retainer; operations backup retainer |
| 5 | **First employee: an engineer** | Engineer + operations analyst |
| 10 | 1 engineer; contractors 2,100 h (implementation 900 h, compliance 300 h, support 270 h) | 7 employees: 4 operations, 1 engineering, 1 implementation, 1 compliance |
| 25 | 3 employees (engineering, implementation and the **first sales/account-management hire**) plus about 3,200 contract hours | 15 employees, 9 of them operations |
| 100 | 16 employees | 67 employees, 38 of them operations |

**First employee by mix:**
- Licensing: about 5 customers, whatever the mix.
- White-label: 7.
- Limited operations: 5.
- Full service: 4, or the first customer when that customer is regional-scale.
- Migration services: 9–11 projects a year.
- Charity intelligence: none within 200 subscribers.

Source: [`staffing-thresholds.csv`](data/outputs/staffing-thresholds.csv).

## Why the Monte Carlo hires earlier
In the median draw an engineer is employed at the **first** customer: the P10–P90 range is 1–4 customers independently, and 1–5 when correlated. Two right-skewed inputs drive this:
- platform maintenance (500/900/1,800 h);
- founder availability (800/1,200/1,800 h).

When maintenance runs above its most likely value, or the founder has less time, residual engineering exceeds the 1,400 h threshold immediately. **Plan for a second qualified engineer from the first customer, contracted until the hours justify employment.**

## Hiring triggers
| Trigger | Mechanism |
|---|---|
| Founder capacity exhausted | Already at zero customers (keep-qualified work about 1,180 h); every further hour is contracted |
| Distinct-person controls | From the first customer: two non-author reviewers (retainer), two-deep on-call and break-glass (a regular contractor counts) |
| Residual engineering above 1,400 h | About 5 licensing customers (median: the first) |
| Exception preparation (limited operations, full service) | Residual operations above 1,300 h at about 4 full-service customers. Under full service, operations headcount grows about 0.4 FTE per average customer |
| Sales and account management above founder capacity | About 25 customers. At 100 customers, account management and sales need about 6 people |
| Qualifications | Fund accounting (operations) and charity/sanctions screening (compliance) can be contracted until volume justifies employment. No CPA is legally required; the controller sign-off is the sponsor's |

## What is not justified
These were not justified by any workload or rule, so they are absent:
- a salaried executive team;
- a dedicated security officer (the founder can be the designated officer; a vCISO is tier 2);
- a CFO (bookkeeping is outsourced);
- a separate support desk before about 50 licensing customers;
- product-enhancement engineering. That last one is discretionary: about 800 h, roughly $96k a year at contract rates, if pursued (review finding ADV-P-12, rejected as an obligation).
