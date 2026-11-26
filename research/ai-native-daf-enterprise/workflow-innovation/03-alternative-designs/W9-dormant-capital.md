# W9: dormant capital and inactivity

**Outcome (BO-53):** charitable assets reach working charities within a horizon consistent with donor intent and charitable purpose, without overriding legitimate advisory privileges.

**Evidence:**
- 22% of accounts made no grants in 2020–22, and the median three-year account payout is 9% (EV-015).
- The median sponsor's FY2024 payout is 12.7% against 25.9% aggregate (EV-014).
- No federal or state payout mandate exists (EV-093). The 2023 proposed regulations are not final (REG-021).
- Asset-based fee incentive: documented; effect on payout unsupported (industry report §3).

**Caution:** the repository establishes the *distribution* of payout, not its cause. Some low payout is deliberate (long-horizon funds, newly funded accounts). This workflow treats inactivity as a signal to engage, not a failure to punish.

## 1. First principles

| Necessary | Not necessary |
|---|---|
| Knowledge of the donor's intended horizon or plan | Annual generic "please grant" letters |
| A lawful default when advisory privileges lapse (death without successor, unresponsive) | Ad hoc staff judgment |
| A sponsor decision for any default distribution (variance or inactivity policy) | — |
| Respect for advisory privileges while they exist | Coercion |

## 2. Inversion
- **What if inactivity were impossible by design?** Every account carries a plan: a horizon, a recurring grant, or an explicit "endowment-style" election (D-W9-4).
- **What if the process began at account opening, not after years of silence?** Same.
- **What if an external partner carried it?** Community foundations or field experts curate default destinations (D-W9-5).

## 3. Competing designs

| ID | Type | Mechanism | Decides / when | Authoritative data | Humans | Controls | Cost | Experience | INN | Maturity |
|---|---|---|---|---|---|---|---|---|---|---|
| D-W9-1 | Conventional | Inactivity policy in the program circular (for example no grants for N years → outreach letters → sponsor may grant to a default fund) | Sponsor after years | Recordkeeper | Program staff | Policy text | Letters; staff | Rarely noticed | — | Observed (policy texts vary) |
| D-W9-2 | Automation-first | Automated inactivity stages, emails and dashboards | Sponsor rules | Ledger | Program officer at final stage | Stage records | Low | More reminders | — | L1 |
| D-W9-3 | AI-native | Engagement driven by the donor's stated goals; discovery agent offers relevant, evidence-graded recipients (INN-33); recurring-grant suggestions; inactivity stage machine with policy defaults (H for the final default) | Donor decides grants; sponsor policy for defaults | Ledger plus goals | Program officer | No sponsor-paid placement; fairness monitoring | Low | Helpful prompts | INN-33 | L1 |
| D-W9-4 | **Radical: plan-at-opening (granting horizon as an account attribute)** | At opening the donor elects a granting horizon (for example spend down in 10 years), a recurring plan, or an explicit long-horizon election with a stated purpose. The scheduler executes recurring grants as donor-pre-approved recommendations; deviations prompt re-election. Inactivity becomes "drift from your own plan", detected continuously. The default destination is chosen by the donor at opening | Donor at opening (*timing* moves from after-the-fact to the start); sponsor decides each grant as usual | Account plan attribute | Program officer for drift beyond tolerance | Plan changes require step-up; no penalty for changing the plan | Scheduler; little staff | One decision at opening; less nagging | INN-19 | L1 |
| D-W9-5 | Ecosystem: default-destination partners | When privileges lapse, assets go by policy to donor-selected or sponsor-curated field funds run by partners (community foundations, pooled funds) | Sponsor policy plus partner | Partner records | Partner staff | Partner due diligence | Partner fees | Local expertise | — | L1 |
| D-W9-6 | Contrarian: fee design aligned to granting | Fee charged partly on grants made, not only on assets held; or fee rebates for meeting the plan | Board fee policy | Fee engine | — | Fee schedule disclosure | Revenue volatility | Aligns incentives | — | L0 (no repository evidence of effect; revenue model risk) |

## 4. Constraint ledger

| Constraint | D-W9-4 radical | D-W9-6 contrarian |
|---|---|---|
| Legal | Survives: recurring grants are donor recommendations decided by sponsor policy. A default at lapse needs a policy basis in the program agreement. No law requires payout (EV-093) | Survives legally. Grant-based fees must not look like a benefit to the donor |
| Fiduciary | Survives | Board must ensure revenue sustainability |
| Accounting | Survives | Fee recognition changes |
| Privacy | Goals data is sensitive; consent needed | — |
| Economic | Reduces AUM-based revenue as capital leaves faster: incentive conflict with asset fees | Revenue less predictable; may favor larger grants |
| Operational | Scheduler exists in the parent design (`ScheduledGrantDue` event) | Fee engine change |
| Human acceptance | Some donors want long horizons, so the long-horizon election must be first-class, not stigmatized | Donors may find it odd; advisors paid on AUM resist |

**Survivors:** D-W9-3 plus D-W9-4 (opt-in plan with a first-class long-horizon option). D-W9-6 is held: evidence and revenue risk. D-W9-5 is held for sponsors with local partners.

## 5. Analogies
- **Retirement auto-enrollment and default funds** (behavioral defaults). Strong evidence in that domain that defaults shape behavior. Breaks: DAF donors are wealthier and choose deliberately, and the evidence does not transfer automatically.
- **Subscription plans.** Recurring schedules.
- **Endowment spending policies.** The long-horizon election.

## 6. Seven perspectives

| Perspective | Position |
|---|---|
| Inventor | Make the plan part of the account, not a reminder |
| Architect | Scheduler plus plan attribute plus drift monitor are small additions to the event model |
| Economist | Under asset-based fees, faster payout reduces sponsor revenue, so the incentive conflict is real. A mission-driven sponsor or a fee redesign is needed |
| Regulatory | No mandate. Defaults must be in the program agreement. Watch the pending §4966/6033 guidance (REG-022) |
| Adversarial | "Plans" could become sponsor pressure that weakens donor advisory privileges. Scheduled grants could hit recipients after their status changes; eligibility checks run at each execution |
| Customer advocate | Many donors want help and fewer letters. Avoid paternalism |
| Commercial | A differentiator for mission-oriented and community sponsors; less so for AUM-maximizers |

**Disagreement:** economist vs customer advocate on whether the sponsor should profit less to grant more. **Unresolved:** a measured behavioral effect. No repository data exists; a pilot is needed.

## 7. Experiments and recommendation
- No credible synthetic experiment can measure donor behavior. Classified as **needs field pilot** (roadmap Phase 5/6).
- E11 computes the revenue effect of faster payout under asset fees.
- **Recommendation:** adopt D-W9-3 plus D-W9-4 as opt-in, with measurement; hold D-W9-6.
