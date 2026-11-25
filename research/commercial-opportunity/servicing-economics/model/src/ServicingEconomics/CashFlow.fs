/// Monthly cash-flow and runway model. Pure functions; months are 0-based from company formation.
module ServicingEconomics.CashFlow

open ServicingEconomics.Domain
open ServicingEconomics.Economics

/// A customer in the plan: signed in SignMonth, live after OnboardingMonths.
type PlannedSponsor =
    { Sponsor: Sponsor
      SignMonth: int
      OnboardingMonths: int
      ImplementationFee: float }

type Plan =
    { Name: string
      Org: Organization
      Activities: Activity list
      Approach: Approach
      Price: Price
      Customers: PlannedSponsor list
      OneTime: (int * string * float) list
      /// Share of non-personnel fixed cost incurred before the first go-live.
      PreLaunchNonPersonnelShare: float
      /// Months between the end of a billing quarter and receipt of cash.
      CollectionLagMonths: int
      /// Annual interest rate charged on negative cash (financing cost).
      FinancingRate: float
      /// Use cash compensation (founders may be unpaid) instead of full economic cost.
      CashView: bool
      Months: int }

type MonthRow =
    { Month: int
      LiveSponsors: int
      AccruedRevenue: float
      CashIn: float
      CashOut: float
      Net: float
      Cumulative: float
      AccruedProfit: float }

let private goLive (c: PlannedSponsor) = c.SignMonth + c.OnboardingMonths

let private liveAt month (plan: Plan) = plan.Customers |> List.filter (fun c -> goLive c <= month)

/// Monthly accrued fee revenue of the sponsors live in a month.
let accruedRevenue (plan: Plan) month =
    liveAt month plan
    |> List.sumBy (fun c -> let a, t, o = sponsorRevenue plan.Price 1.0 c.Sponsor in (a + t + o) / 12.0)

/// Monthly variable, step and sponsor-specific cost of the live sponsors (core payroll and fixed excluded).
let private variableMonthly (plan: Plan) month =
    match liveAt month plan with
    | [] -> 0.0
    | live ->
        let r = evaluate plan.Org plan.Activities plan.Approach plan.Price noStress (live |> List.map (fun c -> c.Sponsor))
        (r.TotalCost - r.CorePersonnel - r.NonPersonnelFixed) / 12.0

let private payrollMonthly (plan: Plan) month =
    plan.Org.Core
    |> List.filter (fun r -> r.StartMonth <= month)
    |> List.sumBy (fun r -> (if plan.CashView then r.CashCost else r.LoadedCost) / 12.0)

let private fixedMonthly (plan: Plan) month =
    let launched = plan.Customers |> List.exists (fun c -> goLive c <= month)
    let share = if launched then 1.0 else plan.PreLaunchNonPersonnelShare
    (plan.Org.NonPersonnelFixed |> List.sumBy snd) * share / 12.0

let private onboardingMonthly (plan: Plan) month =
    plan.Customers
    |> List.filter (fun c -> month >= c.SignMonth && month < goLive c)
    |> List.sumBy (fun c -> c.Sponsor.OnboardingCost / float (max 1 c.OnboardingMonths))

let private implementationCash (plan: Plan) month =
    plan.Customers
    |> List.sumBy (fun c ->
        (if month = c.SignMonth then c.ImplementationFee / 2.0 else 0.0)
        + (if month = goLive c then c.ImplementationFee / 2.0 else 0.0))

/// Fees are billed quarterly in arrears from each sponsor's go-live and collected after a lag.
let private feeCash (plan: Plan) month =
    plan.Customers
    |> List.sumBy (fun c ->
        let live = goLive c
        let billMonth = month - plan.CollectionLagMonths
        let sinceLive = billMonth - live + 1
        if sinceLive >= 3 && sinceLive % 3 = 0 then
            let a, t, o = sponsorRevenue plan.Price 1.0 c.Sponsor
            (a + t + o) / 4.0
        else 0.0)

let private oneTime (plan: Plan) month =
    plan.OneTime |> List.filter (fun (m, _, _) -> m = month) |> List.sumBy (fun (_, _, v) -> v)

/// Month-by-month cash flow, including financing cost on negative balances.
let simulate (plan: Plan) =
    let step (prev: float) month =
        let costs = payrollMonthly plan month + fixedMonthly plan month + variableMonthly plan month + onboardingMonthly plan month + oneTime plan month
        let financing = if prev < 0.0 then -prev * plan.FinancingRate / 12.0 else 0.0
        let cashIn = feeCash plan month + implementationCash plan month
        let cashOut = costs + financing
        let net = cashIn - cashOut
        let accrued = accruedRevenue plan month
        { Month = month
          LiveSponsors = List.length (liveAt month plan)
          AccruedRevenue = accrued
          CashIn = cashIn
          CashOut = cashOut
          Net = net
          Cumulative = prev + net
          AccruedProfit = accrued - (payrollMonthly plan month + fixedMonthly plan month + variableMonthly plan month) }
    [ 0 .. plan.Months - 1 ]
    |> List.scan (fun (acc: MonthRow option) m -> Some (step (acc |> Option.map (fun r -> r.Cumulative) |> Option.defaultValue 0.0) m)) None
    |> List.choose id

/// Capital required: the deepest cumulative cash trough (positive number).
let capitalRequired (rows: MonthRow list) = rows |> List.map (fun r -> r.Cumulative) |> List.fold min 0.0 |> (~-)

/// First month from which accrued monthly profit stays non-negative to the horizon.
let monthsToProfit (rows: MonthRow list) =
    match List.tryLast rows with
    | Some r when r.AccruedProfit >= 0.0 ->
        rows |> List.rev |> List.takeWhile (fun r -> r.AccruedProfit >= 0.0) |> List.tryLast |> Option.map (fun r -> r.Month)
    | _ -> None

/// Cumulative cash position at given horizons (months 6, 12, 18, 24, 36 by convention).
let cumulativeAt (rows: MonthRow list) (horizons: int list) =
    horizons |> List.map (fun h -> h, rows |> List.tryFind (fun r -> r.Month = h - 1) |> Option.map (fun r -> r.Cumulative))
