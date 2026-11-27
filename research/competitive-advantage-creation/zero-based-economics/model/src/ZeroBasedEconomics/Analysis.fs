/// Scenario grids, thresholds, break-even, pricing floors, capital, prior-estimate comparables, sensitivity. Pure.
module ZeroBasedEconomics.Analysis

open System
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Inputs
open ZeroBasedEconomics.Engine

let counts = [ 0; 1; 2; 5; 10; 25; 50; 100 ]
let bpsGrid = [ 5.0; 10.0; 15.0; 20.0; 25.0; 30.0 ]
let baseMix = "mixed"
let baseTier = 1
let scanLimit = 400

let sc n mix f tier = { Customers = n; MixId = mix; Factors = f; Tier = tier }
let baseSc n = sc n baseMix baseFactors baseTier

/// Point inputs at each level.
let leveled (inp: Inputs) = levels |> List.map (fun l -> l, realize (atOriented l) inp)

// ------------------------------------------------------------------------------------------------ growth

/// Base-mix, base-factor outcomes for every model, count and contract tier.
let headline (p: Inputs) =
    [ for tier in [ 0; 1; 2 ] do
          for m in allModels do
              for n in counts do
                  yield evaluate p m (sc n baseMix baseFactors tier) ]

/// Full independent-variation grid (tier 1): every count x mix x 81 factor combinations x model.
let grid (p: Inputs) =
    [ for n in counts do
          for mix in p.Mixes |> List.filter (fun m -> not (m.Id.StartsWith "prior")) do
              for f in allFactors do
                  for m in allModels do
                      yield evaluate p m (sc n mix.Id f baseTier) ]

/// Marginal annual EF cash of customer n+1 at each count (base mix).
let marginal (p: Inputs) (m: ModelId) (n: int) =
    (evaluate p m (baseSc (n + 1))).EfCash - (evaluate p m (baseSc n)).EfCash

/// Average incremental EF cash per customer between two counts (smooths steps).
let averageIncremental (p: Inputs) (m: ModelId) (a: int) (b: int) =
    ((evaluate p m (baseSc b)).EfCash - (evaluate p m (baseSc a)).EfCash) / float (b - a)

// ------------------------------------------------------------------------------------------------ thresholds

type Threshold = { Model: ModelId; MixId: string; What: string; Customers: int option; Detail: string }

let firstWhere (limit: int) (f: int -> bool) = List.init (limit + 1) id |> List.tryFind f

/// First customer count at which each role gets an employee, and at which any coverage alternative is needed.
let staffingThresholds (p: Inputs) =
    [ for mix in p.Mixes |> List.filter (fun m -> not (m.Id.StartsWith "prior")) do
          for m in allModels do
              let at n = evaluate p m (sc n mix.Id baseFactors baseTier)
              let firstHire = firstWhere 200 (fun n -> (at n).Employees > 0)
              let detail =
                  firstHire
                  |> Option.map (fun n ->
                      let o = at n
                      let hires = o.Roles |> List.filter (fun r -> r.Employees > 0) |> List.map (fun r -> $"{r.RoleId}x{r.Employees}")
                      let why = o.Coverage |> List.filter (fun c -> c.Choice = "hire") |> List.map (fun c -> c.CoverageId)
                      let reason = if List.isEmpty why then "workload" else "coverage " + String.Join("+", why)
                      $"""{String.Join(", ", hires)} ({reason})""")
                  |> Option.defaultValue "none within 200 customers"
              yield { Model = m; MixId = mix.Id; What = "first employee"; Customers = firstHire; Detail = detail }
              let firstAlt = firstWhere 200 (fun n -> (at n).Coverage |> List.exists (fun c -> c.Choice = "alternative"))
              let altDetail =
                  firstAlt
                  |> Option.map (fun n -> (at n).Coverage |> List.filter (fun c -> c.Choice = "alternative") |> List.map (fun c -> c.CoverageId) |> fun xs -> String.Join("+", xs))
                  |> Option.defaultValue "none"
              yield { Model = m; MixId = mix.Id; What = "first contracted coverage"; Customers = firstAlt; Detail = altDetail }
              let overFounder = firstWhere 200 (fun n -> let o = at n in o.FounderHours >= o.FounderCapacity - 1e-6)
              yield { Model = m; MixId = mix.Id; What = "founder fully utilised"; Customers = overFounder; Detail = "" } ]

// ------------------------------------------------------------------------------------------------ break-even

type BreakEven =
    { Model: ModelId
      Bps: float option
      CashCustomers: int option
      LoadedCustomers: int option
      CashAuaM: float option
      LoadedAuaM: float option }

let breakEvenFor (p: Inputs) (m: ModelId) (bps: float option) =
    let rev (o: Outcome) = match bps with Some b -> revenueAt p m b o.Volume | None -> o.Revenue
    let at n = evaluate p m (baseSc n)
    let cash = firstWhere scanLimit (fun n -> n > 0 && let o = at n in rev o >= o.EfCash)
    let loaded = firstWhere scanLimit (fun n -> n > 0 && let o = at n in rev o >= o.FullyLoaded)
    { Model = m
      Bps = bps
      CashCustomers = cash
      LoadedCustomers = loaded
      CashAuaM = cash |> Option.map (fun n -> (at n).Volume.AuaM)
      LoadedAuaM = loaded |> Option.map (fun n -> (at n).Volume.AuaM) }

let breakEvens (p: Inputs) =
    [ for m in allModels do
          if m = F then
              for b in bpsGrid do
                  yield breakEvenFor p m (Some b)
          else
              yield breakEvenFor p m None ]

/// Assets a single customer needs for full-service administration to break even at a fee: the base-mix first
/// profile scaled until bps x AUA covers cost. Returns (cash AUA $M, fully loaded AUA $M).
let singleCustomerBreakEvenAua (p: Inputs) (bps: float) =
    let mix = p.Mixes |> List.find (fun m -> m.Id = baseMix)
    let prof = p.Profiles |> List.find (fun x -> x.Id = List.head mix.Pattern)
    let cv = customerVolume baseFactors prof
    let ks = List.init 400 (fun i -> 0.05 * Math.Pow(1.03, float i))
    let at k = let v = volumeOf p F [ scaleCustomer k cv ] in v, evaluateVolume p F (baseSc 1) v
    let find cost =
        ks |> List.tryFind (fun k -> let v, o = at k in revenueAt p F bps v >= cost o) |> Option.map (fun k -> (fst (at k)).AuaM)
    find (fun o -> o.EfCash), find (fun o -> o.FullyLoaded)

// ------------------------------------------------------------------------------------------------ pricing

type PriceFloor =
    { Model: ModelId
      Customers: int
      CashPerCustomer: float
      LoadedPerCustomer: float
      CashPerAccount: float
      LoadedPerAccount: float
      MarginalPerCustomer: float
      CashBps: float
      LoadedBps: float }

/// Break-even price at each count: what every customer must pay for revenue to equal cost.
let priceFloors (p: Inputs) =
    [ for m in allModels do
          for n in counts |> List.filter (fun n -> n > 0) do
              let o = evaluate p m (baseSc n)
              let acc = max 1.0 o.Volume.Accounts
              let aua = max 1.0 (o.Volume.AuaM * 1e6)
              yield
                  { Model = m
                    Customers = n
                    CashPerCustomer = o.EfCash / float n
                    LoadedPerCustomer = o.FullyLoaded / float n
                    CashPerAccount = o.EfCash / acc
                    LoadedPerAccount = o.FullyLoaded / acc
                    MarginalPerCustomer = marginal p m n
                    CashBps = o.EfCash / aua * 10000.0
                    LoadedBps = o.FullyLoaded / aua * 10000.0 } ]

// ------------------------------------------------------------------------------------------------ capital

type Capital =
    { Model: ModelId
      Level: Level
      QualificationCash: float
      QualificationFounderHours: float
      PreRevenueBurn: float
      Readiness: float
      WorkingCapital: float
      ExcludingQualification: float
      Total: float
      MonthlyBurnZero: float
      MonthlyBurnOne: float
      SurplusOne: float }

let capitalFor (p: Inputs) (level: Level) (m: ModelId) =
    let qCash = p.Qualification |> List.filter (fun (id, _, _, _, _) -> not (id.StartsWith "VAL")) |> List.sumBy (fun (_, _, _, c, _) -> c.Base)
    let qHours = p.Qualification |> List.filter (fun (id, _, _, _, _) -> not (id.StartsWith "VAL")) |> List.sumBy (fun (_, _, h, _, _) -> h.Base)
    let o0, o1 = evaluate p m (baseSc 0), evaluate p m (baseSc 1)
    let ids0 = o0.Lines |> List.filter (fun l -> l.Bearer = EF) |> List.map (fun l -> l.Expense.Id) |> Set.ofList
    // Paid before the first invoice: prepaid annual items that the first customer newly triggers.
    let readiness = o1.Lines |> List.filter (fun l -> l.Bearer = EF && l.Expense.Prepaid && not (ids0.Contains l.Expense.Id)) |> List.sumBy (fun l -> l.Cash)
    let lag = par p ("collection_lag_months_" + modelCode m)
    let wc = max 0.0 (lag * o1.EfCash / 12.0)
    let pre = par p "months_to_first_revenue" * o0.EfCash / 12.0
    { Model = m
      Level = level
      QualificationCash = qCash
      QualificationFounderHours = qHours
      PreRevenueBurn = pre
      Readiness = readiness
      WorkingCapital = wc
      ExcludingQualification = pre + readiness + wc
      Total = qCash + pre + readiness + wc
      MonthlyBurnZero = o0.EfCash / 12.0
      MonthlyBurnOne = o1.EfCash / 12.0
      SurplusOne = o1.Revenue - o1.EfCash }

let capital (inp: Inputs) = [ for l, p in leveled inp do for m in allModels do yield capitalFor p l m ]

/// Annual surplus (revenue - EF cash) at 1..10 customers: can the first customer finance the next?
let selfFinancing (p: Inputs) =
    [ for m in allModels do
          for n in 1..10 do
              let o = evaluate p m (baseSc n)
              yield m, n, o.Revenue - o.EfCash, o.Revenue - o.FullyLoaded ]

// ------------------------------------------------------------------------------------------------ priors

/// Values comparable to each prior estimate, computed on the same configuration where the prior defined one.
let comparable (p: Inputs) (metric: string) : float =
    let starts (prefix: string) (id: string) = id.StartsWith(prefix, StringComparison.Ordinal)
    let prior n = sc n "prior-5x2000" baseFactors baseTier
    let ev m s = evaluate p m s
    let lineSum (o: Outcome) cat = o.Lines |> List.filter (fun l -> l.Bearer = EF && l.Expense.Category = cat) |> List.sumBy (fun l -> l.Cash)
    let rate = par p "founder_imputed_rate"
    let actHours (o: Outcome) prefix =
        p.Activities |> List.filter (fun a -> starts prefix a.Id && a.EfModels.Contains o.Model) |> List.sumBy (activityHours o.Volume)
    match metric with
    | "F_cash_5x2000" -> (ev F (prior 5)).EfCash
    | "F_loaded_5x2000" -> (ev F (prior 5)).FullyLoaded
    | "L_cash_5x2000" -> (ev L (prior 5)).EfCash
    | "L_loaded_5x2000" -> (ev L (prior 5)).FullyLoaded
    | "F_incremental_per_account" -> ((ev F (prior 5)).EfCash - (ev F (prior 0)).EfCash) / (ev F (prior 5)).Volume.Accounts
    | "F_system_per_account" -> ((ev F (prior 5)).EfCash - (ev F (prior 0)).EfCash + (ev F (prior 5)).SponsorCost) / (ev F (prior 5)).Volume.Accounts
    | "registry_annual_5x2000" ->
        let o = ev F (prior 5)
        lineSum o "charity-data" + actHours o "ACT-CHV" * rate
    | "acquisition_per_customer" ->
        let o = ev L (baseSc 10)
        (lineSum o "acquisition" + lineSum o "legal-acquisition") / max 1.0 o.Volume.NewCustomers + parFor p "founder_hours_per_new_customer" L * rate
    | "qualification_cash" -> p.Qualification |> List.filter (fun (id, _, _, _, _) -> not (id.StartsWith "VAL")) |> List.sumBy (fun (_, _, _, c, _) -> c.Base)
    | "qualification_loaded" ->
        p.Qualification |> List.filter (fun (id, _, _, _, _) -> not (id.StartsWith "VAL")) |> List.sumBy (fun (_, _, h, c, _) -> c.Base + h.Base * rate)
    | "validation_cash" -> p.Qualification |> List.filter (fun (id, _, _, _, _) -> id.StartsWith "VAL") |> List.sumBy (fun (_, _, _, c, _) -> c.Base)
    | "validation_loaded" ->
        p.Qualification |> List.filter (fun (id, _, _, _, _) -> id.StartsWith "VAL") |> List.sumBy (fun (_, _, h, c, _) -> c.Base + h.Base * rate)
    | "capital_first_revenue_L_excl_qual" -> (capitalFor p Base L).ExcludingQualification
    | "pilot_cash_L" ->
        let c = capitalFor p Base L
        c.ExcludingQualification + (p.Qualification |> List.filter (fun (id, _, _, _, _) -> id.StartsWith "VAL") |> List.sumBy (fun (_, _, _, c, _) -> c.Base))
    | x -> failwithf "unknown comparable metric '%s'" x

let priorComparables (inp: Inputs) =
    let ps = leveled inp
    inp.Priors
    |> List.map (fun pr ->
        let metrics = pr.ComparableMetric.Split([| ';' |], StringSplitOptions.RemoveEmptyEntries) |> Array.toList |> List.map (fun s -> s.Trim())
        pr, metrics |> List.map (fun mt -> mt, ps |> List.map (fun (l, p) -> l, comparable p mt)))

// ------------------------------------------------------------------------------------------------ sensitivity

let hireGrid = [ 0..30 ] @ [ 35..5..100 ] @ [ 120..20..200 ]

/// The headline quantities tracked by sensitivity analysis, computed by name (so a tornado computes one).
let metricNames =
    [ "L zero-customer annual cash"; "L first-customer annual cash"; "F first-customer annual cash"
      "L marginal cash per customer (10->25 avg)"; "F marginal cash per customer (10->25 avg)"
      "L first employee (customers)"; "F first employee (customers)"
      "F cash break-even bps at 10 customers"; "L cash break-even price per customer at 10" ]

let headlineMetric (p: Inputs) (name: string) : float =
    let o m n = evaluate p m (baseSc n)
    let hire m = hireGrid |> List.tryFind (fun n -> (o m n).Employees > 0) |> Option.map float |> Option.defaultValue 201.0
    match name with
    | "L zero-customer annual cash" -> (o L 0).EfCash
    | "L first-customer annual cash" -> (o L 1).EfCash
    | "F first-customer annual cash" -> (o F 1).EfCash
    | "L marginal cash per customer (10->25 avg)" -> averageIncremental p L 10 25
    | "F marginal cash per customer (10->25 avg)" -> averageIncremental p F 10 25
    | "L first employee (customers)" -> hire L
    | "F first employee (customers)" -> hire F
    | "F cash break-even bps at 10 customers" -> let x = o F 10 in x.EfCash / (x.Volume.AuaM * 1e6) * 10000.0
    | "L cash break-even price per customer at 10" -> (o L 10).EfCash / 10.0
    | x -> failwithf "unknown metric '%s'" x

let headlineMetrics (p: Inputs) = metricNames |> List.map (fun n -> n, headlineMetric p n)

type TornadoRow = { Name: string; Metric: string; Low: float; High: float; Base: float }

let tornado (inp: Inputs) (metricName: string) =
    let baseP = realize (atLevel Base) inp
    let get p = headlineMetric p metricName
    let b = get baseP
    namedRanges inp
    |> List.map (fun (key, _) ->
        let swing l = get (realize (fun k r -> if k = key then pick l r else r.Base) inp)
        { Name = key; Metric = metricName; Low = swing Low; High = swing High; Base = b })
    |> List.sortByDescending (fun r -> abs (r.High - r.Low))
    |> List.truncate 20

/// Monte Carlo over every named cost-side range at base volumes. Returns (metric, rho, p10, p50, p90).
let monteCarlo (inp: Inputs) (n: int) (seed: uint64) =
    let named = namedRanges inp
    let names = named |> List.map fst
    let ranges = Map.ofList named
    [ for rho in [ 0.0; 0.5 ] do
          let samples =
              Sampling.quantileDraws n seed rho lowIsAdverse names
              |> List.map (fun q ->
                  let f key r = if Map.containsKey key ranges then Sampling.triangular r (Map.find key q) else r.Base
                  headlineMetrics (realize f inp))
          let metricNames = samples |> List.head |> List.map fst
          for mn in metricNames do
              let xs = samples |> List.map (fun s -> s |> List.find (fun (k, _) -> k = mn) |> snd)
              yield mn, rho, Sampling.percentile 0.1 xs, Sampling.percentile 0.5 xs, Sampling.percentile 0.9 xs ]
