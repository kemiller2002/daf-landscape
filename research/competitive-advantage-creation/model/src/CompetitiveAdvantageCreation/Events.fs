/// Model 2: event-level operating cost by work category (agent HI's decomposition of the Phase II event model,
/// data/evidence/HI/event-work-decomposition.csv). Savings are sequential residuals (P3-DEC-HI001): each step
/// removes minutes from what the previous step left; transferred work is never a saving; automated and accelerated
/// work keep a residual cost. Pure.
module CompetitiveAdvantageCreation.Events

type EventWork =
    { EventId: string
      Event: string
      Scenario: string
      Conventional: float
      Eliminated: float
      Automated: float
      Accelerated: float
      ToCustomer: float
      ToPartner: float
      Mandatory: float
      ResidualOther: float }

/// Categories must account for every conventional minute (accounting identity).
let identityGap (e: EventWork) =
    e.Conventional - (e.Eliminated + e.Automated + e.Accelerated + e.ToCustomer + e.ToPartner + e.Mandatory + e.ResidualOther)

let validate (tolerance: float) (e: EventWork) : Result<EventWork, string> =
    let gap = identityGap e
    if abs gap > tolerance then Error $"{e.EventId} {e.Scenario}: categories differ from conventional minutes by {gap}"
    elif e.Conventional < 0.0 || e.Eliminated < 0.0 || e.Accelerated < 0.0 || e.ToCustomer < 0.0 || e.ToPartner < 0.0 || e.Mandatory < 0.0 || e.ResidualOther < 0.0
    then Error $"{e.EventId} {e.Scenario}: negative minutes outside the automated column"
    else Ok e

/// Cost rates applied to minutes per account-year.
type Rates =
    { LabourPerMinute: float
      /// Share of automated labour value that reappears as platform cost (compute, connectors, rule upkeep, audit scope).
      AutomationResidualShare: float
      /// Model and oversight cost as a share of the labour value of accelerated work.
      AiCostShare: float
      /// Efficiency multiplier on work transferred to customers or partners (PAR-021 analogue).
      TransferEfficiency: float }

/// Waterfall step: residual minutes before and after, and the system-cost saving of the step.
type Step =
    { Step: string
      MinutesBefore: float
      MinutesRemoved: float
      MinutesAfter: float
      ResidualCost: float
      Saving: float }

type Totals =
    { Scenario: string
      Conventional: float
      Eliminated: float
      Automated: float
      Accelerated: float
      ToCustomer: float
      ToPartner: float
      Mandatory: float
      ResidualOther: float }

let totals (scenario: string) (es: EventWork list) : Totals =
    let xs = es |> List.filter (fun e -> e.Scenario = scenario)
    let s f = xs |> List.sumBy f
    { Scenario = scenario
      Conventional = s (fun e -> e.Conventional); Eliminated = s (fun e -> e.Eliminated); Automated = s (fun e -> e.Automated)
      Accelerated = s (fun e -> e.Accelerated); ToCustomer = s (fun e -> e.ToCustomer); ToPartner = s (fun e -> e.ToPartner)
      Mandatory = s (fun e -> e.Mandatory); ResidualOther = s (fun e -> e.ResidualOther) }

/// Sequential waterfall per account-year: eliminate, then automate, then accelerate, then transfer.
/// Savings are measured on system cost (vendor + sponsor + customer + partner), so a transfer saves nothing and
/// costs extra when the recipient is less efficient.
let waterfall (r: Rates) (t: Totals) : Step list =
    let lab m = m * r.LabourPerMinute
    let steps =
        [ "eliminated", t.Eliminated, 0.0
          "automated", t.Automated, lab t.Automated * r.AutomationResidualShare
          "accelerated (AI)", t.Accelerated, lab t.Accelerated * r.AiCostShare
          "transferred to customer", t.ToCustomer, lab t.ToCustomer * r.TransferEfficiency
          "transferred to partner", t.ToPartner, lab t.ToPartner * r.TransferEfficiency ]
    steps
    |> List.mapFold
        (fun before (name, removed, residualCost) ->
            let after = before - removed
            { Step = name; MinutesBefore = before; MinutesRemoved = removed; MinutesAfter = after
              ResidualCost = residualCost; Saving = lab removed - residualCost },
            after)
        t.Conventional
    |> fst

/// System cost per account-year after all steps: residual staffed work plus the residual cost of each step.
let systemCost (r: Rates) (t: Totals) =
    let steps = waterfall r t
    let residualMinutes = (List.last steps).MinutesAfter
    residualMinutes * r.LabourPerMinute + (steps |> List.sumBy (fun s -> s.ResidualCost))

/// Who carries the cost afterwards (per account-year).
type ByParty = { Staffed: float; Platform: float; Ai: float; Customer: float; Partner: float }

let byParty (r: Rates) (t: Totals) : ByParty =
    { Staffed = (t.Mandatory + t.ResidualOther) * r.LabourPerMinute
      Platform = t.Automated * r.LabourPerMinute * r.AutomationResidualShare
      Ai = t.Accelerated * r.LabourPerMinute * r.AiCostShare
      Customer = t.ToCustomer * r.LabourPerMinute * r.TransferEfficiency
      Partner = t.ToPartner * r.LabourPerMinute * r.TransferEfficiency }

/// Combine savings claimed by several models on the same cost base without double counting: each claim is a
/// fractional reduction applied to the residual the previous claims left. The naive sum is returned for comparison.
let combineSequential (baseCost: float) (claims: (string * float) list) : (string * float) list * float * float =
    let steps, residual =
        claims
        |> List.mapFold (fun residual (name, fraction) -> let f = max 0.0 (min 1.0 fraction) in (name, residual * f), residual * (1.0 - f)) baseCost
    let naive = claims |> List.sumBy (fun (_, f) -> baseCost * f)
    steps, baseCost - residual, naive
