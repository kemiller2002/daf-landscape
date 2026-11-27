# 11 — Staffing thresholds

Outputs: [`staffing-steps.csv`](data/model-outputs/staffing-steps.csv) and [`staffing-thresholds.csv`](data/model-outputs/staffing-thresholds.csv) (simulated, CFG-5 full administration, 18 account levels from 100 to 1M, three programmes; sponsors = one per $500M of assets). Staffing is a **step function**, not linear.

## 1. When each dedicated employee is needed (PG-HNW, $250k mean balance)

| Pool | 1st dedicated | 2nd | 3rd | 4th | Driver |
|---|---:|---:|---:|---:|---|
| Engineering | **from the first account** (4 engineers) | — | — | — | platform workload ~3,500-4,100 h/yr regardless of volume; author + two approvers; on-call |
| Compliance | **from the first account** (1) | 1,000 accounts | 3,500 | 5,000 | owner + backup; 24-48 h SLAs in the December peak |
| Operations | (fractional below) | 2,000 accounts (2) | 5,000 | 7,500 | account and grant exceptions; December surge |
| Finance (reconciliation) | 5,000 accounts | 7,500 | 15,000 | — | reconciliation breaks, unidentified receipts, sponsor count |
| Controller (CONTROL) | (fractional below) | 7,500 (2) | 15,000 | — | per-sponsor close and audit support |
| Independent authorizer (AUTH) | 100,000 accounts | 250,000 | 500,000 | 1,000,000 | payment release batches, manual journals |
| Commercial/executive (beyond founder) | 5,000 accounts | 7,500 | 15,000 | — | sponsor count, management overhead |

Total dedicated FTE: 5 at 100-500 accounts; 6 at 1,000; 8 at 2,000; 13 at 5,000; 23 at 10,000; 51 at 25,000; 152 at 100,000; ~1,020 at 1M accounts (plus fractional and surge hours).

## 2. What drives each threshold

| Threshold | Account count | Event volume | Sponsor count | Complexity | Contract/control |
|---|---|---|---|---|---|
| First engineers | — | — | — | — | **yes** (workload floor; change approval; on-call) |
| First compliance | — | — | — | — | **yes** (named owner + backup; SLAs) |
| First operations | yes | **yes** (contacts, breaks, enrolment) | — | — | — |
| Finance | yes | **yes** | yes | — | functional independence |
| Controller | — | — | **yes** | — | sign-off |
| Additional authorization | — | **yes** (release batches) | yes | — | **yes** (two-person release) |
| Additional management | — | — | **yes** | — | span of control |

Programmes differ: institutional books (few large, active accounts) reach operations and compliance thresholds at about half the account count of HNW; retail books reach engineering steps only beyond 175,000 accounts but operations and finance steps early because of contribution volume.

## 3. The first dedicated *operations* employee

Under full administration with the HNW profile, operations stays fractional until about **2,000 accounts (~$500M at $250k)**; the first dedicated operations hires come as a pair (primary and backup, surge for December). Under licensing (CFG-1/2) the vendor needs no operations employee until about 5,000-10,000 accounts (support desk only); the sponsor carries the operational hours instead (≈ 2,800 sponsor hours at 1,000 accounts; 13,600 at 10,000).

## 4. Founder

The founder's 400 hours are consumed by commercial and executive work before any engineering. At the reference scale commercial and executive demand is 935 hours, so the founder is already short of Unbound's own needs; a 1,200-hour founder allocation reduces cash cost by about $330k but is an owner decision (OD-ZB-01) with opportunity cost across 29 other initiatives.

## 5. Implications

- The **first hires are not operations staff**; they are engineers and a compliance owner. Automation removes operations headcount at small scale but not engineering or control seats.
- Staffing grows linearly only once account volume dominates (beyond ~10,000 accounts); until then it is governed by floors and sponsor count.
- Policy choices with step effects: SLA lengths on compliance work, the author-plus-two rule (non-binding at current engineering workload), one-sponsor-per-person reserved authority (sponsor side), and the December SLA policy.
