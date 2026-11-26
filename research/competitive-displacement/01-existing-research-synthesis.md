# 01 - Existing research synthesis and repository initialization

Status: research (2026-11-26). Not legal, tax or investment advice. Evidence classes and confidence follow [the charity-network methodology](../competitive-advantage/charity-network-and-onboarding/01-research-methodology.md): VERIFIED-FACT, VENDOR-CLAIM, INFERENCE, ASSUMPTION, HYPOTHESIS, RECOMMENDATION. Claim status uses confirmed / inferred / hypothesized / contradicted / unknown ([claims register](data/registers/claims.csv)).

## 1. Repository initialization

| Item | Finding |
|---|---|
| daf-landscape `main` | `f0d7047` (2026-11-26). Branch for this initiative: `claude/daf-landscape-phase-ii-5wdw1i`. |
| PR #87 (capital minimization) | **Merged** 2026-11-25. Incorporated as evidence (SRC-002). |
| PR #88 (charity network and onboarding) | **Merged** 2026-11-26. Incorporated (SRC-001). |
| PR #89 (migration and integration tooling) | **Merged** 2026-11-26. Incorporated (SRC-005). |
| PR #90 (file ingestion and STP) | **Merged** 2026-11-26 (landed through #91). Incorporated (SRC-004). |
| `kemiller2002/unbound` `main` | Read. Ratified convergence clauses (CNV-*), owner decision OD-M-05 on the entry segment, and the PR #88 discovery package (`requirements/discovery/2026-11-26-charity-network-and-onboarding/`). |
| `kemiller2002/transitus` | `main` holds only a README. The research and requirements sit on branch `claude/transitus-research-architecture-42a96z` (transitus PR #1, **open, not merged**). Used here as **provisional** evidence (SRC-006, XRI-014). |
| Praxis, EDF, Clarity | Read: Praxis Agent Startup Guide and authority contract (SRC-060); EDF framework (SRC-061); Clarity decision readiness and records (SRC-062). |
| Governance applied | Praxis authority contract: research proposes, it does not authorise. Every decision in [23](23-executive-decision-register.md) is a proposal. No Unbound or Transitus requirement was changed; [17](17-unbound-implications.md) and [18](18-transitus-implications.md) carry traceable proposals. |
| Tooling | .NET 10 SDK installed in the session so new modelling and validation are F# (Echelon standard). Existing Python research scripts were reused, not rewritten. No paid service, infrastructure or subscription was introduced. |

## 2. What the existing research already establishes (not repeated here)

| Topic | Established finding | Source | How Phase II uses it |
|---|---|---|---|
| Charity directory | Commoditised: every incumbent rests on free IRS files; a large directory is not a moat | SRC-001 (02, 04) | Track A extends sources and licensing; Track B challenges the cost |
| Registry run cost | ~$316k a year ($107k-673k), mostly people and compliance | SRC-001 (20 §2) | Reconstructed and challenged in [05](05-charity-registry-economics.md) |
| Network value | Electronic payment network is a mandated cost and switching defence, ~$0 margin lever | SRC-001 (20) | Classified in [13](13-compounding-competitive-advantages.md) |
| Why sponsors stay | Distribution and incentive alignment explain behaviour better than technology | SRC-001 (22, ADVX) | Tested with new switch evidence in [07](07-institutional-switching-incentives.md) |
| Onboarding | Largest variable cost; data quality swings it 2.5-6.2x; history import 46-58% at 100k+ accounts | SRC-001 (20) | Extended with cross-industry measured practice in [08](08-frictionless-onboarding.md) |
| Servicing economics | 20 bps break-even $1.1-1.5B lean, $1.8-2.3B fully loaded; 20 bps fits $250-400k balances only | SRC-003 | Re-derived bottom-up from events in [09](09-event-level-operating-model.md)-[10](10-zero-touch-administration-economics.md) |
| Capital | Minimum product $1.1-2.4M; $4.5M founder-led equity; nothing safe below ~$1.0M build | SRC-002 | Reassessed with entry routes in [15](15-capital-and-break-even-reassessment.md) |
| AI productivity | No demonstrated reduction in the cost of an accepted capability; handling minutes ~6% of revenue | SRC-002 | Decomposed per event in [10](10-zero-touch-administration-economics.md) |
| Ingestion | Attribution of pooled receipts, not parsing, is the main exception; prevention moves cost more than STP | SRC-004 | Modelled as event EV-E04 with a prevention lever |
| Migration tooling | Generic ELT is cheap; DAF migration needs domain loading, reconciliation and lineage | SRC-005 | Basis for [18](18-transitus-implications.md) |
| Entry segment (Unbound) | OD-M-05 ratified mid-size national and single-issue sponsors (5k-50k funds) and advisor-distributed sponsors; community foundations rejected as entry (median 46 DAFs) | SRC-008 | Re-tested in [16](16-commercial-entry-strategy.md) |

## 3. Contradictions found between existing research packages

| # | Contradiction | Resolution in this initiative |
|---|---|---|
| C-1 | PR #88 treats the registry as a fixed ~$316k "cost of doing business"; PR #86 assumed ~$1 per account-year for continuous re-verification | Both reconcile once stewardship is sized by workload rather than a 1 FTE ratio: [05](05-charity-registry-economics.md) finds ~$115-130k for one sponsor (CLM-004) |
| C-2 | PR #87 minimum capital $4.5M (founder-led) vs PR #86 $3-4.5M (small build) and $5-8M realistic | Different organisational and pay assumptions. This package states both and adds market-pay route results ([15](15-capital-and-break-even-reassessment.md), CLM-030) |
| C-3 | OD-M-05 ratified an entry segment that PR #88's adversarial review (ADVX) and this initiative's switch record show is the least mobile | Not resolved by research. Escalated as DEC-001 / XRI-001 |
| C-4 | Prior research recommended adding the UK "OFSI" list | OFSI's consolidated list closed 2026-01-28; replaced by the FCDO UK Sanctions List (CLM-009) |
| C-5 | Prior classification of the UBS DAF as NPT-sponsored | An RCF-sponsored UBS circular also exists; recorded as OQ-016, not resolved |
| C-6 | PR #86/#87 break-even lower bounds ($1.0-1.5B at 20 bps) vs this package's revision 2 ($1.9B operating, $2.3B fully loaded) | Revision 2 adds AI oversight, utilisation, field AI productivity and no automation failure benefit; prior lower bounds now look optimistic ([15](15-capital-and-break-even-reassessment.md) §1) |
| C-7 | The 2026-11-20 commercial-opportunity report recommended migration assurance for mid-size sponsors as a first offer | Consistent in spirit, but the adversarial review found no standalone buyer or price; reframed as pre-sales inside a partner pilot ([16](16-commercial-entry-strategy.md)) |

## 4. Method for Phase II

- **Parallel research agents** (Tracks A, C, D, F) worked from public sources only and wrote evidence files that are committed under `data/evidence/` (SRC-064 to SRC-067). They were told which prior files to read and not to repeat them.
- **Tracks B, E, H and capital** are modelled in one F# model ([model/](model/README.md)) whose inputs anchor to the existing activity register (ACT-A01..S07, SRC-003) and the registry components (SRC-001). Outputs are byte-identical on re-run and checked by `check`.
- **Ten independent adversarial reviewers**, one per required perspective, challenged the drafts without seeing each other ([20](20-adversarial-review.md)).
- **Limits.** The research agents, reviewers and integrator are the same model family, so nothing here is independent validation. No interviews, logins or outreach took place. Every economic figure is conditional on labelled inputs.

## 5. Research ledger

The running ledger is [research-ledger.md](research-ledger.md).
