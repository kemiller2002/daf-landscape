/// Model 7: incumbent response scenarios (none, moderate, aggressive, parity, partner dependency, consolidation) on
/// licensing break-even (agent EK's inputs P3-ASM-EK001..013, report 13 section 3). Pure.
module CompetitiveAdvantageCreation.Response

type CostBase =
    { Name: string
      FixedAnnual: float
      VariablePerAccount: float }

type Scenario =
    { Id: string
      Name: string
      PriceCut: float
      WinRateReduction: float
      PartnerShare: float
      /// Month at which licence revenue terminates (partner acquired, no change-of-control protection).
      TerminationMonth: float option }

type Result =
    { ScenarioId: string
      CostBase: string
      Headline: float
      NetPrice: float
      BreakEvenAccounts: float option
      AccountsPerYear: float
      YearsToBreakEven: float option
      ReachedBeforeTermination: bool option }

/// Net price to the vendor = headline x (1 - price cut) x (1 - partner share).
let netPrice (headline: float) (s: Scenario) = headline * (1.0 - s.PriceCut) * (1.0 - s.PartnerShare)

/// Break-even accounts = fixed / (net price - variable per account); None when the margin is not positive.
let breakEvenAccounts (cb: CostBase) (price: float) =
    let m = price - cb.VariablePerAccount
    if m > 0.0 then Some(cb.FixedAnnual / m) else None

/// accountsPerYearBase: accounts won per year with no response (customers per year x accounts per customer).
let evaluate (cb: CostBase) (headline: float) (accountsPerYearBase: float) (churn: float) (s: Scenario) : Result =
    let price = netPrice headline s
    let be = breakEvenAccounts cb price
    let perYear = accountsPerYearBase * (1.0 - s.WinRateReduction)
    // years until the installed base reaches break-even with annual churn: N(t) = a/c (1 - e^{-ct})
    let years =
        be
        |> Option.bind (fun n ->
            if perYear <= 0.0 then None
            elif churn <= 0.0 then Some(n / perYear)
            else
                let cap = perYear / churn
                if n >= cap then None else Some(-(log (1.0 - n / cap)) / churn))
    { ScenarioId = s.Id; CostBase = cb.Name; Headline = headline; NetPrice = price; BreakEvenAccounts = be
      AccountsPerYear = perYear; YearsToBreakEven = years
      ReachedBeforeTermination = s.TerminationMonth |> Option.map (fun t -> match years with Some y -> y * 12.0 <= t | None -> false) }

/// Lowest net price at which break-even is reachable at all within a horizon (years) at a given acquisition rate.
let walkAwayPrice (cb: CostBase) (accountsPerYear: float) (churn: float) (horizonYears: float) =
    let installed = if churn <= 0.0 then accountsPerYear * horizonYears else accountsPerYear / churn * (1.0 - exp (-churn * horizonYears))
    if installed <= 0.0 then None else Some(cb.VariablePerAccount + cb.FixedAnnual / installed)
