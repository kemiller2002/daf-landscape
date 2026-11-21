# Outcome-based organization model

**Question:** What is the smallest responsible human organization that can operate the enterprise?
**Basis:**
- [capability map](capability-map.md)
- [decision census](../01-enterprise-outcomes/activity-classification.md)
- staffing parameters in [`../09-financial-models/`](../09-financial-models/): assumptions, labeled as such.

## 1. Design rules

1. **Organize around accountable judgment, not task volume.** People own policies and make H decisions. Machines perform D decisions and prepare P analyses.
2. **Keep boundaries that exist for real reasons; remove the rest.** The real reasons are:
   - **Segregation of duties.** Whoever can create a payee cannot approve a payment to it, and whoever writes policy code cannot deploy it alone.
   - **Fiduciary separation.** Investment decisions are separate from grant decisions and from fee revenue.
   - **Independent assurance.** Internal audit reports to the audit committee.
   - **Legal privilege.** Counsel.
   - **Board oversight.**

   Departments that existed only to move paper between those points are removed.
3. **No one-for-one agent substitution.** Agents are not "virtual employees" in the old boxes. They are tools within capabilities, with authority bounded by the deterministic gates.
4. **Supervision is a first-class job.** Every agent family has a named human *agent owner* who answers for its evaluation results, permissions and incidents.
5. **Fractional and outsourced where accountability can be contracted.** Examples: an outsourced CIO, an external auditor, fractional CISO and general counsel at small scale, and custodians. Accountability for *selecting and supervising* them stays in-house.

## 2. Organizational chart (target state, around 10k–100k accounts)

```mermaid
flowchart TB
  Board[Board of Directors<br/>Audit & Risk Cttee · Investment Cttee · Governance Cttee]
  IA[Internal Audit<br/>independent, reports to Audit Cttee]
  CEO[CEO]
  Board --> CEO
  Board -.-> IA
  CEO --> CFO[CFO & Treasurer<br/>Controller · Fund accounting · Treasury · Filings]
  CEO --> CRCO[Chief Risk & Compliance Officer<br/>Sanctions/BSA officer · Fraud · Evidence]
  CEO --> GC[General Counsel<br/>law→policy · inquiries · contracts]
  CEO --> COO[COO<br/>Exception mgmt · Telemetry · Digital twin · Change Board chair · Vendors]
  CEO --> CTO[CTO<br/>Platform · Security (CISO) · Agent engineering & evaluation]
  CEO --> CPO[Head of Client & Partner Operations<br/>Service recovery · Complex servicing · Successors]
  CEO --> GCOMP[Head of Grants Compliance<br/>ER · foreign · benefit cases · post-grant]
  CEO --> PART[Head of Partnerships<br/>Advisor & institutional relationships]
  CEO --> PI[Head of Philanthropic Intelligence]
  CFO --> CAS[Complex Asset Specialists]
  Board --> OCIO[Outsourced CIO / Investment Consultant<br/>under Investment Cttee]
```

**Dual reporting for control functions:** the CRCO has a direct line to the Audit and Risk Committee. The CTO's agent-evaluation lead has a dotted line to the CRCO for model-risk sign-off.

## 3. Capability ownership and accountability matrix

The full matrix is in [`accountability-matrix.csv`](accountability-matrix.csv). The RACI columns are: **A** = accountable (one per row); **R** = responsible human; **S** = software executor (DET / agent); **C** = consulted; **I** = informed.

## 4. Minimum staffing by scale

*These are assumptions, not benchmarks.* The parameters, derivations and sensitivity analysis are in [`../09-financial-models/`](../09-financial-models/). Headcounts there come from the F# model, so this table shows only the structural minimum: roles that must exist at any scale for accountability, regardless of volume.

| Role | Why it must exist at any scale | Can be fractional at 1k accounts? |
|---|---|---|
| Board (≥5 independent majority) with Audit/Risk and Investment committees | Legal and fiduciary | No (volunteer or compensated) |
| CEO | Accountable executive | No |
| CFO / Treasurer / Controller function | Financial statements, filings, segregation from payments approval | Controller can be fractional; a second person is needed for SoD |
| CRCO incl. sanctions officer role | Clear true sanctions matches; own the control evidence | Can combine with GC at 1k |
| General Counsel | Law → policy; inquiries | Fractional / outside counsel |
| Grants compliance specialist | Non-routine grants (ER, foreign, benefit) | 1 person, or shared service |
| Complex asset specialist | Non-cash acceptance | Outsourced to a non-cash processor at small scale (repository: non-cash vendors in b40n14-03) |
| Client and partner operations (exceptions, service recovery, successors) | Human recourse | 1–2 people |
| Technology: platform plus agent evaluation plus security | Runs and supervises the system | At 1k, buy rather than build (see Model C) |
| Internal audit | Independence | Outsourced |

The structural minimum is about 8–10 people (FTE plus fractional) for a self-operated sponsor. Below that, segregation of duties cannot be maintained. **That floor binds at 1k accounts, and it is why a 1k-account sponsor is uneconomic on fees alone** (see 09-).

## 5. How work flows without departmental handoffs

1. A business event, such as `GrantRecommended`, enters the durable workflow for that outcome.
2. The workflow calls capabilities in order: resolve recipient, check eligibility, screen, evaluate policy. Each call returns a decision record.
3. If every gate is D-pass, the instruction is issued and the payment gate releases funds. No person touches it.
4. If any gate returns *flag* or *refer*, a single **exception case** is opened in C5.3. It goes to the skill-matched human, with the P dossier attached, and it carries an SLA timer.
5. The human decides within their delegated authority. Above that authority it escalates; it is not "sent to another department".
6. The decision is recorded with the evidence viewed, and the workflow resumes from the same durable state.

The consequence: the questions "who has it now?" and "what is it waiting for?" are always answerable from state. In the conventional model they are the main content of internal email and donor status calls.

## 6. Comparison with conventional staffing structures

The repository has **no published sponsor organization charts or headcount by function.** The evidence available is:
- whole-organization staff cost: Part IX lines 5–10 at 78.7 bps of DAF assets at community foundations, against 5.6–15.0 bps at self-staffed nationals ([strategic synthesis §0 G6](../../mission-2026-11-14/strategic-synthesis.md));
- executive compensation filings;
- the operating-efficiency series in [`b51-04-sponsor-operating-efficiency.md`](../../mission-2026-11-14/b51-04-sponsor-operating-efficiency.md).

The conventional *structure* below is therefore a typical-pattern description, labeled [I]:

| Conventional unit | Typical activities | Disposition in the redesign |
|---|---|---|
| Donor services / call center | Status, address changes, statements, how-to | Mostly removed by shared state and grounded answers; small recovery team |
| Operations (contributions, grants processing) | Data entry, matching, check runs, letters | Removed or automated; exceptions go to the specialist queue |
| Grants compliance / due diligence | Per-grant lookups plus exceptions | Per-grant lookups removed; exceptions remain (specialists) |
| Investment operations | Rebalancing, cash forecasting, advisor trade review | Deterministic; committee and OCIO remain |
| Finance and accounting | Reconciliation, close, fee calc, audit PBC | Continuous; controller function remains |
| Compliance | Manuals, attestations, registrations | Policy-as-code plus evidence; officers remain |
| Marketing and sales | Brand, wholesaling | Partnerships and API distribution |
| IT | Vendor management of a recordkeeping system | Platform engineering plus agent evaluation (a new competence) |

**New roles that do not exist conventionally:** agent owners, the evaluation lead, the policy engineer (counsel-adjacent), and a digital-twin and telemetry analyst.
