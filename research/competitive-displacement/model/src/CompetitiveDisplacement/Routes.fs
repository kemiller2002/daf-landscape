/// Entry-route cash model (REV2): monthly cash flows with customer acquisition, churn, go-live/billing lag;
/// capital = deepest cumulative deficit over the horizon; payback = first month cumulative cash returns to zero.
module CompetitiveDisplacement.Routes

open CompetitiveDisplacement.Inputs

let horizon = 120

type RouteValues =
    { Build: float; Burn: float; FirstRevenueMonth: float; RevenuePerCustomer: float; CustomersPerYear: float }

type RouteResult =
    { RouteId: string
      Capital: float
      FirstPositiveMonth: int option
      PaybackMonth: int option
      CumulativeAt60: float
      CumulativeAt120: float
      CustomersAt60: float
      AnnualRevenueAt60: float }

let valuesAt (level: Level) (r: Route) =
    // adverse level: higher build, burn and delay; lower revenue and acquisition
    let inv l = match l with Low -> High | High -> Low | Base -> Base
    { Build = pick level r.Build; Burn = pick level r.Burn; FirstRevenueMonth = pick level r.FirstRevenueMonth
      RevenuePerCustomer = pick (inv level) r.RevenuePerCustomer; CustomersPerYear = pick (inv level) r.CustomersPerYear }

type private State = { Signed: float; Live: float; Pipeline: float list }

/// Monthly flows: (net cash, live customers, revenue) for months 1..horizon. Pure fold over months.
let flows (r: Route) (rv: RouteValues) : (int * float * float * float) list =
    let monthlyChurn = r.Churn / 12.0
    let lag = int (round r.GoLiveLag)
    let buildMonths = max 1.0 rv.FirstRevenueMonth
    let step (st: State) (m: int) =
        let mf = float m
        let signing = if mf > rv.FirstRevenueMonth then rv.CustomersPerYear / 12.0 else 0.0
        let pipeline = st.Pipeline @ [ signing ]
        let goingLive, pending = if pipeline.Length > lag then pipeline.Head, pipeline.Tail else 0.0, pipeline
        let live = st.Live * (1.0 - monthlyChurn) + goingLive
        let revenue = if r.Recurring then live * rv.RevenuePerCustomer / 12.0 else goingLive * rv.RevenuePerCustomer
        let buildSpend = if mf <= buildMonths then rv.Build / buildMonths else 0.0
        let net = revenue * (1.0 - r.VariableShare) - rv.Burn - buildSpend - signing * r.Cac
        (m, net, live, revenue), { Signed = st.Signed + signing; Live = live; Pipeline = pending }
    [ 1 .. horizon ] |> List.mapFold step { Signed = 0.0; Live = 0.0; Pipeline = [] } |> fst

let simulate (r: Route) (rv: RouteValues) : RouteResult =
    let fs = flows r rv
    let cumulative = fs |> List.scan (fun acc (_, net, _, _) -> acc + net) 0.0 |> List.tail
    let indexed = List.zip fs cumulative
    let trough = List.min (0.0 :: cumulative)
    let troughMonth = indexed |> List.tryFindIndex (fun (_, c) -> c = trough) |> Option.defaultValue 0
    let at m = indexed |> List.item (m - 1)
    let (_, _, live60, _), cum60 = at 60
    let (_, _, _, rev60), _ = at 60
    { RouteId = r.Id
      Capital = -trough
      FirstPositiveMonth = fs |> List.tryFind (fun (m, net, _, _) -> net >= 0.0 && float m > rv.FirstRevenueMonth) |> Option.map (fun (m, _, _, _) -> m)
      PaybackMonth = indexed |> List.skip troughMonth |> List.tryFind (fun (_, c) -> c >= 0.0) |> Option.map (fun ((m, _, _, _), _) -> m)
      CumulativeAt60 = cum60
      CumulativeAt120 = List.last cumulative
      CustomersAt60 = live60
      AnnualRevenueAt60 = rev60 * 12.0 }

let sampled (r: Route) (us: float list) =
    match us with
    | [ a; b; c; d; e ] ->
        { Build = Sampling.triangular r.Build a; Burn = Sampling.triangular r.Burn b
          FirstRevenueMonth = Sampling.triangular r.FirstRevenueMonth c
          RevenuePerCustomer = Sampling.triangular r.RevenuePerCustomer d
          CustomersPerYear = Sampling.triangular r.CustomersPerYear e }
    | _ -> valuesAt Base r
