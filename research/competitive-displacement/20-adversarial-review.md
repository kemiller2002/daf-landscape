# 20 - Adversarial review

Status: research (2026-11-26). Register: [adversarial-challenges.csv](data/registers/adversarial-challenges.csv) (CHL-001..110, each with evidence, proposed change, disposition, rationale and resulting change). Raw reviewer files: [data/evidence/adversarial/](data/evidence/adversarial/adv-cfo.csv) (SRC-074).

## 1. Method

Ten independent reviewers, one per required perspective, each read the drafts relevant to its seat and was told to **refute, not improve**. None saw another's output or the integrator's planned conclusions. The CFO and economist reran the F# model on copied inputs in scratch folders. All reviewers are the same model family as the authors, so this is structured self-criticism, not independent validation.

| Perspective | Challenges | High | Most consequential |
|---|---|---|---|
| Incumbent competitor executive | 12 | 5 | The "unbuyable" archive is downloadable (NCCS); the AI-native comparison is against a manual strawman |
| Institutional procurement executive | 11 | 5 | G1 timeline contradicts 9-24 month cycles; SOC 2 and vendor viability block an undercapitalised entrant |
| Skeptical CFO | 11 | 4 | Break-even omitted capital recovery; capital ignored churn and lag; tails understated |
| Compliance and regulatory specialist | 11 | 4 | 180-day re-review is policy, not law; free data does not cover the full determination; a platform creating ACH files is a TPSP |
| Nonprofit data specialist | 10 | 5 | Archive not unique; expiry rate inconsistent; Candid Charity Check from $2,750 commoditises the evidence product |
| Financial systems architect | 11 | 5 | Prevention double-counted; build budget thin for scope; licensing assumed equally efficient sponsor staff |
| Institutional migration specialist | 11 | 6 | Paid assessment has no buyer, no price and no platform at G1; synthetic rehearsal oversold; incumbent-controlled extract |
| Investor | 12 | 7 | No venture-scale outcome; headline capital was the optimistic band; partner would capture value; no exit analysis |
| Customer unwilling to switch | 10 | 6 | Validation sampled only movers; contract-end windows are renegotiation leverage; switching cost is people, not data |
| Economist skeptical of AI productivity | 11 | 4 | AI factor applied backwards (circular); 0.6 is a lab figure; correlated pessimism removes the AI edge |
| **Total** | **110** | **51** | |

Required challenge types were all exercised: unsupported assumptions (20), hidden dependencies (13), regulatory (13), underestimated labour (12), false differentiation (8), optimistic sizing (8), arithmetic (6), unverified weaknesses (5), overestimated automation (5), double counting (4), circular reasoning (3), underestimated CAC (2), data licensing (1), unjustified network effect (1), other (9).

## 2. Dispositions

| Disposition | Count |
|---|---|
| Accepted, model changed | 23 |
| Accepted, text changed | 70 |
| Partially accepted | 12 |
| Deferred and recorded | 4 |
| Rejected | 1 |

**Rejected (CHL-027)**: the CFO argued MD-5's fixed cost omits SOC 1/2 audits and insurance. The basis is PR #87's lower bound, whose $0.65M non-personnel floor already contains audit, SOC 1 and SOC 2, penetration testing and insurance; no change beyond citing it. The SOC 1 Type II need for a licensor is added to report 14.

**Partially accepted or deferred, with reasons**: build cost widened to $3.6M but bottom-up costing left to Unbound (CHL-057); FTE step functions approximated by a utilisation factor (CHL-109); incumbent comparator restated against MD-3 and MD-4 because the incumbents' true operating mode is unknown (CHL-003); registry run cost not itemised in mode fixed cost, adding about $0.08B to 20 bps break-even (CHL-031); sponsor-side P&L deferred to the price test (CHL-029); class-based exception model deferred to measurement (CHL-049); per-tenant infrastructure floors and contribution-channel touch rates recorded, not modelled (CHL-064, CHL-065); population cap not modelled (CHL-082); rebound effect covered only by the activity range (CHL-106).

## 3. Model changes (revision 2)

| Change | Challenges | Effect at 20 bps, MD-5 |
|---|---|---|
| AI factor applied in the right direction (exception minutes are inputs; AI-native = exception × factor) | CHL-100 | AI step now responds to the factor |
| AI factor base 0.6 → 0.85 (field evidence) | CHL-101 | Minutes 26 → 43 |
| Prevention double counting removed (E08, E13 rebased; E10 efficacy 0.25) | CHL-033, 056, 102 | Prevention saving falls |
| Prevention at half efficacy until partners are signed | CHL-060 | |
| No assumed automation failure benefit | CHL-061, 107 | |
| AI oversight and model-risk cost (+$0.1-0.2M) | CHL-104 | Fixed $2.3M → $2.5M |
| Audit preparation held at conventional minutes | CHL-105 | |
| Labour utilisation 0.75 | CHL-034, 109 | All labour +33% |
| Licensing: sponsor efficiency ×1.4; vendor bears AI compute; TPSP audit in fixed | CHL-037, 058 | MD-6 $0.85B → $0.96B |
| Fully loaded break-even | CHL-024 | $2.33B |
| Correlated Monte Carlo (ρ=0.5) and named stress | CHL-026, 108 | P90 $4.25B → correlated $7.26B; stress $2.79B |
| Fixed cost in the tornado | CHL-028 | Second-largest driver |
| Routes: churn, go-live lag, 120-month horizon, payback month | CHL-025, 079, 080, 089 | ER-7 P50 $5.1M → $6.0M; 37% no payback in 10 years |
| Registry: expiry 0.5/yr, name-match alerts, Candid-anchored licence | CHL-047, 048, 052 | RA-1 $115k → $162k |

Net effect: MD-5 break-even at 20 bps $1.46B → **$1.92B operating / $2.33B fully loaded / P50 $2.48B**; human minutes 26 → **53**; AI share of saving ~10% → **~6%**; **exception-driven administration without AI (MD-4) now breaks even slightly below AI-native at entry scale**.

## 4. Conclusions that changed

| Revision 1 | Revision 2 | Driver |
|---|---|---|
| A provenance-bound temporal archive is the one advantage that cannot be bought later | **Parity**: NCCS and Candid already hold it | CHL-001, 046 |
| Minimum viable entry: paid migration assessment + charity evidence feed sold at windows | **Partner pilot**: Unbound as a module inside a channel partner's offering; assessment is free pre-sales CAC; evidence feed is a component | CHL-016, 051, 067, 068, 095 |
| Charity intelligence could be a product | **Component only** (Candid from $2,750) | CHL-051 |
| Lowest self-sustaining capital about $4-5M | **About $6.5M P50 (P90 ~$9M)**, with a 37% chance of no payback within ten years | CHL-078, 085 |
| AI-native lowers break-even from ~$2.1B to ~$1.5B | Roughly parity with a well-automated incumbent; licensing is the robust mode | CHL-003, 100-104 |
| 180-day re-vetting is a compliance cost to cut | A sponsor policy choice; savings are against self-imposed cost | CHL-035 |
| Free public data suffices for determinations | Suffices for status facts only | CHL-036, 050 |
| Licensor has low regulatory exposure | Moderate: TPSP, SOC 1 likely, bank third party in bank channels | CHL-037, 041, 066 |
| W07 (Ren losing CFs) and W09 (SOC inconsistency) are weaknesses | Normal churn; unexplained scope discrepancy | CHL-006, 007 |

## 5. Conclusions that survived

- The ratified entry segment is the least mobile; distribution and incentive alignment are the binding barrier (no reviewer contested this; the incumbent and customer reviewers reinforced it).
- Deterministic design and prevention, not AI, drive most of the cost difference.
- Licensing is the vendor mode least sensitive to productivity assumptions.
- Full-service administration is the highest-capital entry route.
- The registry is not a cost barrier.

## 6. Contradictions recorded, not resolved

- **OD-M-05 vs switching evidence** (DEC-001): owner decision.
- **Partner dependency**: the recommended route needs a partner, but the precedent is acquisition, not licensing (CLM-025; CHL-084). Tested by V-6; unresolved.
- **Incumbent operating mode**: whether incumbents run at MD-3 or MD-4 efficiency is unknown; the advantage ranges from about $11 to $71 per account-year.
