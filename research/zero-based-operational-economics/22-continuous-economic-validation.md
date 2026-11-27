# 22 — Continuous economic validation (proposed standard)

**Status: research-backed proposal.** Not a portfolio-wide rule: governance implications must be evaluated and approved by the owner before Praxis enforces anything (OD-ZB-05).

## 1. Problem

Requirements evolve faster than economic models. During this research alone, the previous model's register drifted (MD-5 fixed shown as $2.3M after it became $2.5M), and two structural model defects were found only by adversarial review. A requirement that adds one independent human approval per grant can add hundreds of hours a year; nothing today flags it.

## 2. Mechanism

```
Unbound requirement change (PR)
   → requirement carries an economic_impact record (21 §3) when material
   → activity register row(s) created or updated (operational-activities.csv), each linked by requirement ID
   → zero-based model re-run (deterministic, < 1 minute)
   → economic regression report attached to the PR
   → material change ⇒ decision record required before merge (owner gate)
```

## 3. What the check detects

| Signal | Detection rule |
|---|---|
| New recurring human activity | new activity row, or exception rate / minutes increased |
| Increased approval requirements | `independent_authorization` changed to Y, or new INDEPENDENT-AUTHORIZATION row |
| New external dependency or subscription | new fixed-cost line or non-zero `external_cost_per_event` |
| Infrastructure requirement change | infrastructure parameter or deployment change (e.g., C1 → C3) |
| Event-frequency change | frequency or driver changed |
| Staffing-assumption change | roles, named-person minimums, fractional/dedicated thresholds |
| Sponsor-responsibility change | `responsible_entity` or configuration share changed |
| Development and maintenance change | TECHOPS rows, one-time lines |

## 4. Economic regression report (format)

```
Economic regression — <PR / requirement IDs> — <date>
Reference scenarios: $100M / $500M / $1B; CFG-2 and CFG-5; PG-HNW
                              previous     revised      Δ
View 1 cash ($500M, CFG-5)    $2.20M       $x.xxM       +$xk
Vendor hours                  7,200        x,xxx        +xxx
Dedicated FTE                 8            x
Break-even 20 bps ($250k)     $1.85B       $x.xxB
Changed assumptions:   [ids with old → new]
Changed requirements:  [ids]
New cost drivers:      [activities / lines]
Removed cost drivers:  [activities / lines]
Material?              yes if |Δ View 1| > 2% or Δ FTE ≥ 0.5 or break-even moves a grid step
Required decisions:    [owner decision IDs]
```

The model already produces every number except the diff; a `diff` command over two output directories is a small addition.

## 5. Integration with Praxis (proposals, see [24](24-cross-repository-implications.md))

- An `economic_impact` front-matter block in requirement records (optional unless material).
- A validator that fails when an activity row references an unknown requirement ID, or a material requirement has no activity link.
- An execution-telemetry hook to record the regression report as evidence on the work item.
- Unbound would first need Praxis installed (it is not today) and CI (absent).

## 6. Calibration loop once operations exist

Replace assumptions in order of economic leverage ([25](25-evidence-gaps-and-validation-plan.md)): handling minutes and exception rates of the top 15 activities; Tier-2 trigger incidence; engineering hours per accepted change; per-sponsor close hours; compliance alert rates; December peak shape. Each replaced value changes its evidence class to `MEASURED-FACT` with sample size and period.
