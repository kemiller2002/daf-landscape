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

let mixIds (p: Inputs) = p.Mixes |> List.filter (fun m -> not (m.Id.StartsWith "prior")) |> List.map (fun m -> m.Id)

type BreakEven =
    { Model: ModelId
      MixId: string
      Bps: float option
      CashCustomers: int option
      LoadedCustomers: int option
      CashAuaM: float option
      LoadedAuaM: float option }

/// First count from which revenue covers cost at every larger count up to the scan limit (ADV-A-03: persistent,
/// not first touch). Reported for every mix, because the order and size of customers drives the answer (ADV-A-02).
let persistentFrom (limit: int) (ok: int -> bool) =
    let flags = List.init limit (fun i -> i + 1, ok (i + 1))
    flags
    |> List.rev
    |> List.fold (fun (acc, holding) (n, f) -> if holding && f then (Some n, true) else (acc, false)) (None, true)
    |> fst

let breakEvenFor (p: Inputs) (mix: string) (m: ModelId) (bps: float option) =
    let rev (o: Outcome) = match bps with Some b -> revenueAt p m b o.Volume | None -> o.Revenue
    let outcomes = List.init scanLimit (fun i -> evaluate p m (sc (i + 1) mix baseFactors baseTier)) |> Array.ofList
    let at n = outcomes.[n - 1]
    let cash = persistentFrom scanLimit (fun n -> let o = at n in rev o >= o.EfCash)
    let loaded = persistentFrom scanLimit (fun n -> let o = at n in rev o >= o.FullyLoaded)
    { Model = m
      MixId = mix
      Bps = bps
      CashCustomers = cash
      LoadedCustomers = loaded
      CashAuaM = cash |> Option.map (fun n -> (at n).Volume.AuaM)
      LoadedAuaM = loaded |> Option.map (fun n -> (at n).Volume.AuaM) }

let breakEvens (p: Inputs) =
    [ for mix in mixIds p do
          for m in allModels do
              if m = F then
                  for b in bpsGrid do
                      yield breakEvenFor p mix m (Some b)
              else
                  yield breakEvenFor p mix m None ]

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

/// Break-even price at each count for the base mix: what every customer must pay for revenue to equal cost.
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

/// One year of a growth path: customers at year end, customers onboarded in the year, revenue and EF cash.
type PathYear = { Year: int; Customers: int; Added: float; Revenue: float; Cash: float; Cumulative: float }

/// Growth path from production qualification (ADV-A-01, ADV-A-08). Year 0 is the pre-revenue period: the zero-customer
/// platform for `months_to_first_revenue`, plus everything that must exist at go-live and precedes the first
/// invoice: first-customer onboarding and acquisition, prepaid assurance and insurance, and `go_live_lead_months`
/// of the first-customer run-rate (coverage retainers, compliance platform, observation-period controls). Then each
/// year adds `customers_added_per_year` customers along the mix and is charged their onboarding. The path runs until
/// cumulative cash stops falling for good, or 15 years.
let growthPath (p: Inputs) (mix: string) (m: ModelId) =
    let rate = max 1 (int (Math.Round(par p "customers_added_per_year")))
    let lag = par p ("collection_lag_months_" + modelCode m)
    let yearAt (n: int) (added: float) =
        let s = sc n mix baseFactors baseTier
        let v = { volume p m s with NewCustomers = (if m = M then float n else added) }
        evaluateVolume p m s v
    let o0 = evaluate p m (sc 0 mix baseFactors baseTier)
    let o1 = yearAt 1 1.0
    let ids0 = o0.Lines |> List.filter (fun l -> l.Bearer = EF) |> List.map (fun l -> l.Expense.Id) |> Set.ofList
    let prepaid = o1.Lines |> List.filter (fun l -> l.Bearer = EF && l.Expense.Prepaid && not (ids0.Contains l.Expense.Id)) |> List.sumBy (fun l -> l.Cash)
    let preRevenue = par p "months_to_first_revenue" * o0.EfCash / 12.0
    let goLive = par p "go_live_lead_months" * o1.EfCash / 12.0 + prepaid
    let year0 = { Year = 0; Customers = 0; Added = 0.0; Revenue = 0.0; Cash = preRevenue + goLive; Cumulative = -(preRevenue + goLive) }
    let years =
        List.init 15 (fun i -> i + 1)
        |> List.scan (fun prev y ->
            let n = rate * y
            let o = yearAt n (float rate)
            // Collection lag delays one lag-period of revenue into the next year in the first year only.
            let rev = if y = 1 then o.Revenue * (1.0 - lag / 12.0) else o.Revenue
            { Year = y; Customers = n; Added = float rate; Revenue = rev; Cash = o.EfCash; Cumulative = prev.Cumulative + rev - o.EfCash }) year0
    years

type Capital =
    { Model: ModelId
      Level: Level
      MixId: string
      QualificationCash: float
      QualificationFounderHours: float
      PreRevenueBurn: float
      GoLive: float
      DeepestDeficit: float
      DeficitYear: int
      /// Cumulative deficit at the end of year 5 (meaningful when the path never becomes self-sustaining).
      DeficitYear5: float
      SelfSustainingYear: int option
      CustomersAtSelfSustaining: int option
      MonthlyBurnZero: float
      MonthlyBurnOne: float
      FounderHoursYearOne: float }

let capitalFor (p: Inputs) (level: Level) (mix: string) (m: ModelId) =
    let qual = p.Qualification |> List.filter (fun (id, _, _, _, _, ms) -> ms.Contains m && not (id.StartsWith "VAL"))
    let path = growthPath p mix m
    let deepest = path |> List.minBy (fun y -> y.Cumulative)
    let sustaining = path |> List.tryFind (fun y -> y.Year > 0 && path |> List.filter (fun z -> z.Year >= y.Year) |> List.forall (fun z -> z.Revenue >= z.Cash))
    let y0 = List.head path
    let o0, o1 = evaluate p m (sc 0 mix baseFactors baseTier), evaluate p m (sc 1 mix baseFactors baseTier)
    { Model = m
      Level = level
      MixId = mix
      QualificationCash = qual |> List.sumBy (fun (_, _, _, c, _, _) -> c.Base)
      QualificationFounderHours = qual |> List.sumBy (fun (_, _, h, _, _, _) -> h.Base)
      PreRevenueBurn = par p "months_to_first_revenue" * o0.EfCash / 12.0
      GoLive = y0.Cash - par p "months_to_first_revenue" * o0.EfCash / 12.0
      DeepestDeficit = -deepest.Cumulative
      DeficitYear = deepest.Year
      DeficitYear5 = -(path |> List.filter (fun y -> y.Year <= 5) |> List.map (fun y -> y.Cumulative) |> List.min)
      SelfSustainingYear = sustaining |> Option.map (fun y -> y.Year)
      CustomersAtSelfSustaining = sustaining |> Option.map (fun y -> y.Customers)
      MonthlyBurnZero = o0.EfCash / 12.0
      MonthlyBurnOne = o1.EfCash / 12.0
      FounderHoursYearOne = o1.FounderHours }

let capital (inp: Inputs) =
    [ for l, p in leveled inp do
          for mix in mixIds p do
              for m in allModels do
                  yield capitalFor p l mix m ]

/// Annual run-rate surplus (revenue - EF cash) at 1..10 customers for every mix: can the first customer finance the next?
let selfFinancing (p: Inputs) =
    [ for mix in mixIds p do
          for m in allModels do
              for n in 1..10 do
                  let o = evaluate p m (sc n mix baseFactors baseTier)
                  yield mix, m, n, o.Revenue - o.EfCash, o.Revenue - o.EfCash - o.FounderNoncash ]

// ------------------------------------------------------------------------------------------------ deep-review allocation

/// P3-DEC-MOD005 / OD-CDD-06 (open): who performs the 180-day deep review. Re-run with ACT-CHV-04 (and the
/// change-driven re-vetting ACT-CHV-03) borne by Echelon Foundry in every platform model, or by the sponsor in every
/// model. Returns (allocation, model, customers, EF cash, sponsor cost).
let deepReviewAllocation (p: Inputs) =
    // `manual` removes the change-driven design: every 180-day renewal is a full human review (the conventional
    // 10 minutes per review), i.e. the value of the approved OD-CDD-02 direction.
    let alloc toEf manual =
        { p with
            Activities =
                p.Activities
                |> List.map (fun a ->
                    if a.Id = "ACT-CHV-03" || a.Id = "ACT-CHV-04" then
                        let a' = if manual && a.Id = "ACT-CHV-04" then { a with HumanShare = point 1.0 } else a
                        if toEf then { a' with EfModels = set [ L; W; T; F ]; SponsorModels = Set.empty }
                        else { a' with EfModels = Set.empty; SponsorModels = set [ L; W; T; F ] }
                    else a) }
    [ for name, q in [ "Echelon Foundry performs (change-driven)", alloc true false; "Sponsor performs (change-driven)", alloc false false
                       "Echelon Foundry performs (manual 180-day reviews)", alloc true true; "Sponsor performs (manual 180-day reviews)", alloc false true ] do
          for m in [ L; T; F ] do
              for n in [ 1; 10; 100 ] do
                  let o = evaluate q m (baseSc n)
                  yield name, m, n, o.EfCash, o.SponsorCost ]

// ------------------------------------------------------------------------------------------------ priors

/// Values comparable to each prior estimate, on the prior's own configuration and scope where it defined one.
let comparable (p: Inputs) (metric: string) : float =
    let starts (prefix: string) (id: string) = id.StartsWith(prefix, StringComparison.Ordinal)
    let prior n = sc n "prior-5x2000" baseFactors baseTier
    let ev m s = evaluate p m s
    let lineSum (o: Outcome) cat = o.Lines |> List.filter (fun l -> l.Bearer = EF && l.Expense.Category = cat) |> List.sumBy (fun l -> l.Cash)
    let rate = par p "founder_imputed_rate"
    let actHours (o: Outcome) (prefixes: string list) =
        p.Activities
        |> List.filter (fun a -> prefixes |> List.exists (fun pr -> starts pr a.Id) && a.EfModels.Contains o.Model)
        |> List.sumBy (activityHours o.Volume)
    let qsum f g = p.Qualification |> List.filter (fun (id, _, _, _, _, _) -> f id) |> List.sumBy g
    match metric with
    | "F_cash_5x2000" -> (ev F (prior 5)).EfCash
    | "F_loaded_5x2000" -> (ev F (prior 5)).FullyLoaded
    | "L_cash_5x2000" -> (ev L (prior 5)).EfCash
    | "L_loaded_5x2000" -> (ev L (prior 5)).FullyLoaded
    // ADV-A-09: the per-account slope between 5 and 10 prior sponsors, excluding first-customer step costs
    | "F_slope_per_account" -> ((ev F (prior 10)).EfCash - (ev F (prior 5)).EfCash) / ((ev F (prior 10)).Volume.Accounts - (ev F (prior 5)).Volume.Accounts)
    | "F_system_slope_per_account" ->
        let a, b = ev F (prior 5), ev F (prior 10)
        (b.EfCash + b.SponsorCost - a.EfCash - a.SponsorCost) / (b.Volume.Accounts - a.Volume.Accounts)
    // ADV-A-12: include data-pipeline stewardship, which the prior included
    | "registry_annual_5x2000" ->
        let o = ev F (prior 5)
        lineSum o "charity-data" + actHours o [ "ACT-CHV"; "ACT-PLT-09" ] * rate
    | "acquisition_per_customer" ->
        let o = ev L (baseSc 10)
        (lineSum o "acquisition" + lineSum o "legal-acquisition") / max 1.0 o.Volume.NewCustomers + parFor p "founder_hours_per_new_customer" L * rate
    | "qualification_cash" -> qsum (fun id -> not (starts "VAL" id)) (fun (_, _, _, c, _, _) -> c.Base)
    | "qualification_loaded" -> qsum (fun id -> not (starts "VAL" id)) (fun (_, _, h, c, _, _) -> c.Base + h.Base * rate)
    | "validation_cash" -> qsum (starts "VAL") (fun (_, _, _, c, _, _) -> c.Base)
    | "validation_loaded" -> qsum (starts "VAL") (fun (_, _, h, c, _, _) -> c.Base + h.Base * rate)
    // ADV-A-01: like-for-like with the prior pilot budget: validation, build cash and the deepest cumulative deficit
    | "capital_to_self_sustaining_L_incl_build" ->
        let c = capitalFor p Base baseMix L
        c.DeepestDeficit + c.QualificationCash + qsum (starts "VAL") (fun (_, _, _, c, _, _) -> c.Base)
    | "capital_to_self_sustaining_L_excl_build" -> (capitalFor p Base baseMix L).DeepestDeficit
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
