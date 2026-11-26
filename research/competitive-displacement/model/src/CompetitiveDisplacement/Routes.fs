/// Entry-route cash model: monthly cash flows over a horizon; capital = deepest cumulative deficit.
module CompetitiveDisplacement.Routes

open CompetitiveDisplacement.Inputs

type RouteValues =
    { Build: float; Burn: float; FirstRevenueMonth: float; RevenuePerCustomer: float; CustomersPerYear: float }

type RouteResult =
    { RouteId: string
      Capital: float
      FirstPositiveMonth: int option
      CumulativeAt60: float
      CustomersAt60: float
      RevenueMonth60: float }

let valuesAt (level: Level) (r: Route) =
    // adverse level: higher build, burn, delay; lower revenue and acquisition
    let inv l = match l with Low -> High | High -> Low | Base -> Base
    { Build = pick level r.Build; Burn = pick level r.Burn; FirstRevenueMonth = pick level r.FirstRevenueMonth
      RevenuePerCustomer = pick (inv level) r.RevenuePerCustomer; CustomersPerYear = pick (inv level) r.CustomersPerYear }

/// Monthly net cash flow for month m (1-based).
let monthly (r: Route) (rv: RouteValues) (m: int) : float * float =
    let mf = float m
    let buildMonths = max 1.0 rv.FirstRevenueMonth
    let buildSpend = if mf <= buildMonths then rv.Build / buildMonths else 0.0
    let active = max 0.0 (mf - rv.FirstRevenueMonth)
    let customers = rv.CustomersPerYear / 12.0 * active
    let newCustomers = if active > 0.0 then rv.CustomersPerYear / 12.0 else 0.0
    let revenue =
        if r.Recurring then customers * rv.RevenuePerCustomer / 12.0
        else newCustomers * rv.RevenuePerCustomer
    let net = revenue * (1.0 - r.VariableShare) - rv.Burn - buildSpend - newCustomers * r.Cac
    net, customers

let simulate (horizon: int) (r: Route) (rv: RouteValues) : RouteResult =
    let flows = [ 1 .. horizon ] |> List.map (fun m -> m, monthly r rv m)
    let cumulative = flows |> List.scan (fun acc (_, (net, _)) -> acc + net) 0.0 |> List.tail
    let firstPositive =
        flows |> List.tryFind (fun (m, (net, _)) -> net >= 0.0 && float m > rv.FirstRevenueMonth) |> Option.map fst
    let lastNet, lastCustomers = flows |> List.last |> snd
    { RouteId = r.Id
      Capital = - (List.min (0.0 :: cumulative))
      FirstPositiveMonth = firstPositive
      CumulativeAt60 = List.last cumulative
      CustomersAt60 = lastCustomers
      RevenueMonth60 = lastNet }

/// Draw route values from triangular ranges (customers and revenue use their own ranges directly).
let sampled (r: Route) (us: float list) =
    match us with
    | [ a; b; c; d; e ] ->
        { Build = Sampling.triangular r.Build a; Burn = Sampling.triangular r.Burn b
          FirstRevenueMonth = Sampling.triangular r.FirstRevenueMonth c
          RevenuePerCustomer = Sampling.triangular r.RevenuePerCustomer d
          CustomersPerYear = Sampling.triangular r.CustomersPerYear e }
    | _ -> valuesAt Base r
