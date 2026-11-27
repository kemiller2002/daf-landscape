/// Re-examination of the Phase II entry-route model for the double counts agent AB raised (report 03 section 3).
/// A faithful port of competitive-displacement/model/src/CompetitiveDisplacement/Routes.fs `flows` (base values),
/// with two optional corrections. The port must reproduce Phase II's ER-7 base capital exactly. Pure.
module CompetitiveAdvantageCreation.Phase2Check

type Route =
    { Id: string
      Build: float
      Burn: float
      FirstRevenueMonth: float
      RevenuePerCustomer: float
      CustomersPerYear: float
      Recurring: bool
      VariableShare: float
      Cac: float
      Churn: float
      GoLiveLag: float }

type Corrections =
    { /// Share of the monthly burn still paid during build months (1.0 = Phase II).
      BuildPhaseBurnFactor: float
      /// Replacement variable-cost share (None = Phase II value).
      VariableShare: float option }

let phaseTwo = { BuildPhaseBurnFactor = 1.0; VariableShare = None }

type private St = { Live: float; Pipeline: float list }

/// Deepest cumulative deficit over 120 months (Phase II "capital").
let capital (k: Corrections) (r: Route) : float =
    let lag = int (round r.GoLiveLag)
    let buildMonths = max 1.0 r.FirstRevenueMonth
    let vs = defaultArg k.VariableShare r.VariableShare
    let step (st: St) (m: int) =
        let mf = float m
        let signing = if mf > r.FirstRevenueMonth then r.CustomersPerYear / 12.0 else 0.0
        let pipeline = st.Pipeline @ [ signing ]
        let goingLive, pending = if pipeline.Length > lag then pipeline.Head, pipeline.Tail else 0.0, pipeline
        let live = st.Live * (1.0 - r.Churn / 12.0) + goingLive
        let revenue = if r.Recurring then live * r.RevenuePerCustomer / 12.0 else goingLive * r.RevenuePerCustomer
        let inBuild = mf <= buildMonths
        let buildSpend = if inBuild then r.Build / buildMonths else 0.0
        let burn = if inBuild then r.Burn * k.BuildPhaseBurnFactor else r.Burn
        revenue * (1.0 - vs) - burn - buildSpend - signing * r.Cac, { Live = live; Pipeline = pending }
    let nets = [ 1..120 ] |> List.mapFold step { Live = 0.0; Pipeline = [] } |> fst
    let cum = nets |> List.scan (+) 0.0 |> List.tail
    -(List.min (0.0 :: cum))

/// Variable share that keeps the direct route's variable cost per account when revenue is already net of a channel
/// share: directShare x (gross / net) = directShare / (1 - channelShare).
let perAccountEquivalentShare (directShare: float) (channelShare: float) = directShare / (1.0 - channelShare)
