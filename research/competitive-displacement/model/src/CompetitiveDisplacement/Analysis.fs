/// Analyses built from the pure model: grids, decompositions, sensitivities and Monte Carlo summaries.
module CompetitiveDisplacement.Analysis

open CompetitiveDisplacement.Inputs
open CompetitiveDisplacement.Events
open CompetitiveDisplacement.Enterprise

let bpsGrid = [ 5.0; 10.0; 15.0; 20.0; 25.0; 30.0 ]
let balances = [ 100000.0; 250000.0; 500000.0 ]

let modeById (inputs: Inputs) id = inputs.Modes |> List.find (fun m -> m.Id = id)

let baseVals (inputs: Inputs) = Sampling.atLevel Base inputs.Params

let withoutPrevention (m: Mode) = { m with UsesPrevention = false; Id = m.Id + "-noprev" }

let allEconomics (inputs: Inputs) (vals: Values) =
    inputs.Modes |> List.map (economics Base vals inputs.Events)

type BreakEvenRow = { ModeId: string; Bps: float; Balance: float; Assets: float option; Loaded: float option }

let breakEvenGrid (inputs: Inputs) (vals: Values) =
    let sponsors = v vals "sponsors"
    [ for m in allEconomics inputs vals do
        for bps in bpsGrid do
            for b in balances do
                yield { ModeId = m.Mode.Id; Bps = bps; Balance = b; Assets = breakEvenAssets bps b sponsors m
                        Loaded = breakEvenAssetsLoaded bps b sponsors m } ]

/// Monte Carlo break-even percentiles per mode and fee. "Never" is represented as +infinity.
type McRow = { ModeId: string; Bps: float; P10: float; P50: float; P90: float; NeverShare: float }

let lowIsAdverse = set [ "avg_balance"; "prevention_scale" ]

let monteCarlo (n: int) (seed: uint64) (rho: float) (inputs: Inputs) : McRow list =
    let ps = inputs.Params |> Map.add "fixed_quantile" { Low = 0.0; Base = 0.5; High = 1.0 }
    let draws = if rho <= 0.0 then Sampling.draws n seed ps else Sampling.drawsCorrelated n seed rho lowIsAdverse ps
    let perDraw =
        draws
        |> List.map (fun d ->
            let choose r = Sampling.triangular r (Map.find "fixed_quantile" d)
            inputs.Modes |> List.map (fun m -> economicsWith choose d inputs.Events m, d))
    [ for mi in 0 .. inputs.Modes.Length - 1 do
        for bps in bpsGrid do
            let xs =
                perDraw
                |> List.map (fun row ->
                    let m, d = List.item mi row
                    breakEvenAssets bps (v d "avg_balance") (v d "sponsors") m |> Option.defaultValue infinity)
            yield
                { ModeId = (List.item mi inputs.Modes).Id; Bps = bps
                  P10 = Sampling.percentile 0.1 xs; P50 = Sampling.percentile 0.5 xs; P90 = Sampling.percentile 0.9 xs
                  NeverShare = (xs |> List.filter System.Double.IsInfinity |> List.length |> float) / float n } ]

/// Event ranking by share of total per-account event cost (Pareto).
type ParetoRow = { ModeId: string; EventId: string; Name: string; CostPerAcct: float; Share: float; Cumulative: float }

let pareto (inputs: Inputs) (vals: Values) (modeId: string) : ParetoRow list =
    let m = economics Base vals inputs.Events (modeById inputs modeId)
    let accountsRef = 10000.0
    let rows =
        m.Events
        |> List.map (fun c -> c, perAccount c + c.PassThroughPerAcct + c.SponsorLevelCost * 5.0 / accountsRef)
        |> List.sortByDescending snd
    let total = rows |> List.sumBy snd
    rows
    |> List.scan (fun (_, cum) (c, x) -> Some(c, x), cum + x) (None, 0.0)
    |> List.choose (fun (o, cum) -> o |> Option.map (fun (c, x) -> { ModeId = modeId; EventId = c.EventId; Name = c.Name; CostPerAcct = x; Share = x / total; Cumulative = cum / total }))

/// Decomposition of the conventional-to-AI-native saving per account into its sources.
type Decomposition = { Step: string; FromMode: string; ToMode: string; SavingPerAcct: float; MinutesSaved: float }

let decomposition (inputs: Inputs) (vals: Values) =
    let ev m = economics Base vals inputs.Events m
    let md id = modeById inputs id
    let eventCost (e: ModeEconomics) = e.Events |> List.sumBy perAccount
    let steps =
        [ "AI assistance on conventional touches", md "MD-1", md "MD-2"
          "Deterministic workflow on structured events", md "MD-1", md "MD-3"
          "Exception-only design for all events (no AI, no prevention)", md "MD-3", withoutPrevention (md "MD-4")
          "Prevention mechanisms (upstream input design)", withoutPrevention (md "MD-4"), md "MD-4"
          "AI on residual exceptions", md "MD-4", md "MD-5" ]
    steps
    |> List.map (fun (name, a, b) ->
        let ea, eb = ev a, ev b
        { Step = name; FromMode = a.Id; ToMode = b.Id
          SavingPerAcct = eventCost ea - eventCost eb
          MinutesSaved = ea.HumanMinutesPerAcct - eb.HumanMinutesPerAcct })

/// Per-event value of prevention versus faster processing in the AI-native mode.
type PreventionRow = { EventId: string; Name: string; Prevention: string; PreventionValue: float; SpeedValue: float }

let preventionVsSpeed (inputs: Inputs) (vals: Values) =
    let m5 = modeById inputs "MD-5"
    let m4 = modeById inputs "MD-4"
    inputs.Events
    |> List.map (fun e ->
        let c5 = cost m5 vals e |> perAccount
        let c5np = cost (withoutPrevention m5) vals e |> perAccount
        let c4 = cost m4 vals e |> perAccount
        { EventId = e.Id; Name = e.Name; Prevention = e.Prevention; PreventionValue = c5np - c5; SpeedValue = c4 - c5 })

/// Tornado: break-even assets of a mode at a fee and balance with each parameter at its low and high value.
type TornadoRow = { ModeId: string; Param: string; LowValue: float; HighValue: float; AtLow: float; AtHigh: float; Swing: float }

let tornado (inputs: Inputs) (modeId: string) (bps: float) =
    let vals = baseVals inputs
    let m = modeById inputs modeId
    let be (vs: Values) = breakEvenAssets bps (v vs "avg_balance") (v vs "sponsors") (economics Base vs inputs.Events m) |> Option.defaultValue infinity
    inputs.Params
    |> Map.toList
    |> List.map (fun (name, r) ->
        let lo = be (Map.add name r.Low vals)
        let hi = be (Map.add name r.High vals)
        { ModeId = modeId; Param = name; LowValue = r.Low; HighValue = r.High; AtLow = lo; AtHigh = hi
          Swing = (if System.Double.IsInfinity lo || System.Double.IsInfinity hi then infinity else abs (hi - lo)) })
    |> List.sortByDescending (fun t -> t.Swing)

// ------------------------------------------------------------------ registry

let registryVals (inputs: Inputs) level = Sampling.atLevel level inputs.RegistryParams

type RegistryRow = { Alt: string; Charities: float; Sponsors: float; ChangeRate: float; Refresh: string; Grants: float; Result: Registry.RegistryCost }

let registryGrid (inputs: Inputs) =
    let rp = registryVals inputs Base
    [ for alt in inputs.Alts do
        for nPer in [ 5000.0; 20000.0; 50000.0 ] do
            for s in [ 1.0; 3.0; 10.0; 30.0 ] do
                for cr in [ 0.02; 0.04; 0.08 ] do
                    for refresh in [ None; Some 90.0; Some 180.0; Some 365.0 ] do
                        let grants = nPer * 3.5 * s // ~3.5 grants per charity in use per sponsor-year (70k grants / 20k charities)
                        let d = { Registry.CharitiesPerSponsor = nPer; Registry.Sponsors = s; Registry.ChangeRate = cr; Registry.RefreshDays = refresh; Registry.GrantsPerYear = grants }
                        yield { Alt = alt.Id; Charities = nPer; Sponsors = s; ChangeRate = cr
                                Refresh = (match refresh with None -> "change-driven" | Some d -> $"periodic-{int d}d")
                                Grants = grants; Result = Registry.cost alt rp d } ]

/// Registry Monte Carlo for one alternative at fixed drivers.
let registryMc (n: int) (seed: uint64) (inputs: Inputs) (alt: RegistryAlt) (d: Registry.Drivers) =
    Sampling.draws n seed inputs.RegistryParams
    |> List.map (fun rp -> (Registry.cost alt rp d).Total)
    |> fun xs -> Sampling.percentile 0.1 xs, Sampling.percentile 0.5 xs, Sampling.percentile 0.9 xs

// ------------------------------------------------------------------ routes

type RouteRow = { RouteId: string; Case: string; Result: Routes.RouteResult }

let routeCases (inputs: Inputs) =
    [ for r in inputs.Routes do
        for case, level in [ "favourable", Low; "base", Base; "adverse", High ] do
            yield { RouteId = r.Id; Case = case; Result = Routes.simulate r (Routes.valuesAt level r) } ]

type RouteMcRow = { RouteId: string; Rho: float; P10: float; P50: float; P90: float; NoPayback120: float; PaybackP50: float }

/// Route Monte Carlo. Quantile order: build, burn, first revenue month (high adverse); revenue, customers (low adverse).
let routeMc (n: int) (seed: uint64) (rho: float) (inputs: Inputs) : RouteMcRow list =
    inputs.Routes
    |> List.map (fun r ->
        let draw st =
            let uc, st0 = Sampling.next st
            let us, st' =
                [ false; false; false; true; true ]
                |> List.fold (fun (xs, s) lowAdverse ->
                    let pick, s1 = Sampling.next s
                    let own, s2 = Sampling.next s1
                    let common = if lowAdverse then 1.0 - uc else uc
                    (xs @ [ (if pick < rho then common else own) ]), s2) ([], st0)
            us, st'
        let results =
            List.unfold (fun (i, st) -> if i >= n then None else let us, st' = draw st in Some(Routes.simulate r (Routes.sampled r us), (i + 1, st'))) (0, seed)
        let caps = results |> List.map (fun x -> x.Capital)
        let noPayback = results |> List.filter (fun x -> x.PaybackMonth.IsNone) |> List.length
        let paybacks = results |> List.map (fun x -> x.PaybackMonth |> Option.map float |> Option.defaultValue infinity)
        { RouteId = r.Id; Rho = rho; P10 = Sampling.percentile 0.1 caps; P50 = Sampling.percentile 0.5 caps; P90 = Sampling.percentile 0.9 caps
          NoPayback120 = float noPayback / float n; PaybackP50 = Sampling.percentile 0.5 paybacks })

/// Named correlated stress (REV2, CHL economist): weaker AI, more and longer touches, no automation failure benefit, higher fixed cost.
type StressRow = { ModeId: string; BaseAssets: float; StressAssets: float; BaseMinutes: float; StressMinutes: float }

let stressOverrides =
    [ "ai_assist_duration_factor", 0.88; "touch_mult_native", 1.5; "duration_mult_native", 1.3
      "fail_mult_automated", 1.0; "fixed_cost_mult", 1.15 ]

let stress (inputs: Inputs) =
    let b = baseVals inputs
    let s = stressOverrides |> List.fold (fun acc (k, x) -> Map.add k x acc) b
    inputs.Modes
    |> List.map (fun m ->
        let eb, es = economics Base b inputs.Events m, economics Base s inputs.Events m
        let be (vs: Values) e = breakEvenAssets 20.0 (v vs "avg_balance") (v vs "sponsors") e |> Option.defaultValue infinity
        { ModeId = m.Id; BaseAssets = be b eb; StressAssets = be s es; BaseMinutes = eb.HumanMinutesPerAcct; StressMinutes = es.HumanMinutesPerAcct })
