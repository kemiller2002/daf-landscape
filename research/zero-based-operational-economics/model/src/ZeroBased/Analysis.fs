/// Analyses composed from the pure model: scenario evaluation, scale grids, staffing step functions,
/// break-even, Monte Carlo, Beneficium and baseline comparison. Pure.
module ZeroBased.Analysis

open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Workload
open ZeroBased.Simulation
open ZeroBased.Staffing
open ZeroBased.Infrastructure
open ZeroBased.Costs
open ZeroBased.Revenue

let seed = 20261127UL

let baseVals (inputs: Inputs) = CompetitiveDisplacement.Sampling.atLevel Base inputs.Params
let infraVals (inputs: Inputs) = CompetitiveDisplacement.Sampling.atLevel Base inputs.Infra
let benVals (inputs: Inputs) = CompetitiveDisplacement.Sampling.atLevel Base inputs.Beneficium

let config (inputs: Inputs) id = inputs.Configs |> List.find (fun c -> c.Id = id)
let programme (inputs: Inputs) id = inputs.Programmes |> List.find (fun p -> p.Id = id)

let scenario (vals: Values) (p: Programme) (accounts: float) (sponsors: float) (balance: float) : Scenario =
    { Id = $"{p.Id}-{accounts}-{sponsors}"
      Accounts = accounts
      Sponsors = sponsors
      NewSponsorsPerYear = sponsors * v vals "new_sponsor_share"
      MeanBalance = balance
      Programme = p
      ActivityMult = v vals "activity_mult" }

let incidentSpecs (vals: Values) (accounts: float) =
    // rates per year; integration failures scale weakly with sponsors/accounts via the multiplier
    let scale = max 1.0 (log10 (max 10.0 accounts) - 2.0)
    // REV-A (ADV-OC): security and integration incident hours are already in TECHOPS activities (OA-TEC-002/004/023),
    // so the simulation adds only events not in the inventory: operational recovery and automation mass remediation.
    // SLA in business days: recovery 3; mass remediation 10 (identify, correct, notify), engineering fix 5
    [ "operational failure / recovery", "FINANCE", v vals "inc_ops_failure_rate" * scale, v vals "inc_ops_failure_hours", 3.0
      "automation mass remediation (ops)", "OPS", v vals "inc_automation_rate", v vals "inc_automation_ops_hours", 10.0
      "automation mass remediation (engineering)", "ENG", v vals "inc_automation_rate", v vals "inc_automation_eng_hours", 5.0 ]

/// Full evaluation of one scenario under one configuration and deployment.
type Eval =
    { Scenario: Scenario
      Config: Config
      Counts: Counts
      Loads: Load list
      Totals: Totals
      Staffing: Staffing
      Infra: InfraCost
      Views: Views
      Incidents: Incident list }

let evaluate (simulate: bool) (level: Level) (vals: Values) (iv: Values) (inputs: Inputs) (cfg: Config) (dep: Deployment) (s: Scenario) : Eval =
    let c = counts vals s
    let ls = loads level vals cfg c inputs.Activities
    let t = totals ls
    let inc = incidents seed (incidentSpecs vals s.Accounts)
    // Public charity-dataset upkeep: engineering and compliance hours go into the staffed pools (REV-A: idle
    // engineers absorb them before cash is spent); infrastructure, fees and counsel remain cash.
    let bv = CompetitiveDisplacement.Sampling.atLevel level inputs.Beneficium
    let bc = ZeroBased.Beneficium.cost bv ZeroBased.Beneficium.ContinuousMonitoring 0.0
    let extra = Map.ofList [ "ENG", bc.ConnectorHours + bc.OpsHours; "COMPLIANCE", bc.ExceptionHours + bc.OwnerFloorHours ]
    let st = staffing simulate level vals inputs.Roles cfg ls inc extra
    let aiEx = ls |> List.filter (fun l -> l.Activity.Classification = "AI-ASSISTED") |> List.sumBy (fun l -> l.HumanEvents * l.VendorShare)
    let isolated = if s.Accounts / max 1.0 s.Sponsors >= v vals "isolated_db_accounts_threshold" then s.Sponsors else 0.0
    // infrastructure is borne by the platform owner in every configuration
    let infra = cost iv dep c t.Events aiEx isolated
    let originates = (Map.tryFind AdminException cfg.Shares |> Option.defaultValue 0.0) > 0.0 && not (cfg.Id = "CFG-1" || cfg.Id = "CFG-2" || cfg.Id = "CFG-6")
    let ctx = { Cfg = cfg; Counts = c; VendorOriginatesPayments = originates || v vals "platform_creates_ach_files" > 0.5 }
    // cash part of charity-dataset upkeep (labour is in the pools above); recipient-driven work is in activities
    let upkeep = bc.Infra + bc.ExternalFees + bc.Counsel
    let vw = views level ctx inputs.Fixed ls st.LabourCash st.BackupCash st.FounderImputed (infra.Total * v vals "infra_mult") upkeep (v vals "sponsor_labour_rate")
    let vw = { vw with View1 = vw.View1 + (vw.FixedIncremental * (v vals "fixed_mult" - 1.0))
                       View2 = vw.View2 + (vw.FixedIncremental * (v vals "fixed_mult" - 1.0))
                       View3 = vw.View3 + (vw.FixedIncremental * (v vals "fixed_mult" - 1.0)) }
    { Scenario = s; Config = cfg; Counts = c; Loads = ls; Totals = t; Staffing = st; Infra = infra; Views = vw; Incidents = inc }

let viewCost (view: int) (e: Eval) = match view with 1 -> e.Views.View1 | 2 -> e.Views.View2 | _ -> e.Views.View3

/// Revenue net of any channel-partner share.
let netRevenue (p: Pricing) (e: Eval) =
    let human = e.Totals.HumanEvents
    revenue p e.Scenario e.Counts human * (1.0 - e.Config.ChannelShare)

// ------------------------------------------------------------------ break-even

let breakEvenGrid = accountGrid 100.0 2000000.0 70

/// Smallest sustained account count (and assets) at which revenue covers a view's cost.
let breakEven (vals: Values) (iv: Values) (inputs: Inputs) (cfg: Config) (dep: Deployment) (p: Programme) (sponsors: float) (balance: float) (view: int) (pricing: Pricing) (amortised: float) =
    let profit accts =
        let e = evaluate false Base vals iv inputs cfg dep (scenario vals p accts sponsors balance)
        netRevenue pricing e - viewCost view e - amortised
    sustainedBreakEven profit breakEvenGrid |> Option.map (fun a -> a, a * balance)

// ------------------------------------------------------------------ Monte Carlo

/// Parameters for which a LOW value is adverse (so correlated draws push them down together).
let lowIsAdverse = set [ "productive_hours_per_day"; "founder_hours_per_year"; "ai_assist_duration_factor_inverse" ]

type McSummary = { Label: string; P10: float; P50: float; P90: float; Mean: float }

let summarise label (xs: float list) =
    { Label = label
      P10 = CompetitiveDisplacement.Sampling.percentile 0.1 xs
      P50 = CompetitiveDisplacement.Sampling.percentile 0.5 xs
      P90 = CompetitiveDisplacement.Sampling.percentile 0.9 xs
      Mean = (let fin = xs |> List.filter (fun x -> not (System.Double.IsInfinity x)) in if fin.IsEmpty then infinity else List.average fin) }

let draws n rho (ps: Params) =
    if rho <= 0.0 then CompetitiveDisplacement.Sampling.draws n seed ps
    else CompetitiveDisplacement.Sampling.drawsCorrelated n seed rho lowIsAdverse ps

/// Monte Carlo of annual View 1/2/3 cost at a fixed scenario (analytic staffing).
let mcCost n rho (inputs: Inputs) (cfg: Config) (dep: Deployment) (p: Programme) accounts sponsors balance =
    let iv = infraVals inputs
    let ds = draws n rho inputs.Params
    let es = ds |> List.map (fun d -> evaluate false Base d iv inputs cfg dep (scenario d p accounts sponsors balance))
    [ summarise "View 1 incremental cash" (es |> List.map (viewCost 1))
      summarise "View 2 allocated economic" (es |> List.map (viewCost 2))
      summarise "View 3 standalone" (es |> List.map (viewCost 3))
      summarise "Vendor human hours" (es |> List.map (fun e -> e.Totals.VendorHours))
      summarise "Dedicated FTE" (es |> List.map (fun e -> e.Staffing.DedicatedFte)) ]

/// Monte Carlo of break-even assets for a view (accounts and balance per draw).
let mcBreakEven n rho (inputs: Inputs) (cfg: Config) (dep: Deployment) (p: Programme) sponsors (view: int) (bps: float) =
    let iv = infraVals inputs
    let grid = accountGrid 100.0 2000000.0 28
    draws n rho inputs.Params
    |> List.map (fun d ->
        let balance = v d "mc_mean_balance"
        let profit accts =
            let e = evaluate false Base d iv inputs cfg dep (scenario d p accts sponsors balance)
            netRevenue (AumBps bps) e - viewCost view e
        match sustainedBreakEven profit grid with
        | Some a -> a * balance
        | None -> infinity)

/// One-at-a-time sensitivity of a view's annual cost at a scenario.
type TornadoRow = { Param: string; Low: float; High: float; AtLow: float; AtHigh: float; Swing: float }

let tornado (inputs: Inputs) (cfg: Config) (dep: Deployment) (p: Programme) accounts sponsors balance (view: int) =
    let b = baseVals inputs
    let iv = infraVals inputs
    let at (vs: Values) = evaluate false Base vs iv inputs cfg dep (scenario vs p accounts sponsors balance) |> viewCost view
    inputs.Params
    |> Map.toList
    |> List.filter (fun (k, r) -> r.Low <> r.High && k <> "mc_mean_balance")
    |> List.map (fun (k, r) ->
        let lo, hi = at (Map.add k r.Low b), at (Map.add k r.High b)
        { Param = k; Low = r.Low; High = r.High; AtLow = lo; AtHigh = hi; Swing = abs (hi - lo) })
    |> List.sortByDescending (fun t -> t.Swing)

// ------------------------------------------------------------------ staffing step functions

type StepRow = { Accounts: float; Pool: string; Mode: string; DedicatedFte: float; FractionalHours: float; Hours: float; SimFte: float }

let stepFunction (simulate: bool) (inputs: Inputs) (cfg: Config) (dep: Deployment) (p: Programme) (sponsorsFor: float -> float) (grid: float list) =
    let vals = baseVals inputs
    let iv = infraVals inputs
    grid
    |> List.collect (fun a ->
        let e = evaluate simulate Base vals iv inputs cfg dep (scenario vals p a (sponsorsFor a) p.DefaultBalance)
        e.Staffing.Pools
        |> List.map (fun ps -> { Accounts = a; Pool = ps.Pool; Mode = ps.Mode; DedicatedFte = ps.DedicatedFte; FractionalHours = ps.FractionalHours; Hours = ps.Hours; SimFte = ps.SimulatedFte }))

/// First grid account count at which a pool needs a dedicated employee (and each additional one).
let thresholds (rows: StepRow list) =
    rows
    |> List.groupBy (fun r -> r.Pool)
    |> List.collect (fun (pool, rs) ->
        let sorted = rs |> List.sortBy (fun r -> r.Accounts)
        sorted
        |> List.fold (fun (prevFte, acc) r ->
            if r.DedicatedFte > prevFte then r.DedicatedFte, (pool, r.DedicatedFte, r.Accounts) :: acc else max prevFte r.DedicatedFte, acc) (0.0, [])
        |> snd
        |> List.rev)

// ------------------------------------------------------------------ requirement economic impact

/// Vendor and sponsor hours per Unbound requirement (an activity's hours split evenly across its requirements).
let hoursByRequirement (ls: Load list) =
    ls
    |> List.collect (fun l ->
        let reqs = l.Activity.Requirements |> List.filter (fun r -> r <> "none-found" && r <> "")
        let h = (l.Minutes + l.AuthMinutes) / 60.0
        if reqs.IsEmpty then [ "(no requirement)", h * l.VendorShare, h * (1.0 - l.VendorShare), l.Activity.Id ]
        else reqs |> List.map (fun r -> r, h * l.VendorShare / float reqs.Length, h * (1.0 - l.VendorShare) / float reqs.Length, l.Activity.Id))
    |> List.groupBy (fun (r, _, _, _) -> r)
    |> List.map (fun (r, xs) ->
        r, (xs |> List.sumBy (fun (_, a, _, _) -> a)), (xs |> List.sumBy (fun (_, _, b, _) -> b)),
        (xs |> List.map (fun (_, _, _, id) -> id) |> List.distinct |> String.concat "|"))
    |> List.sortByDescending (fun (_, a, b, _) -> a + b)

// ------------------------------------------------------------------ unit costs

type UnitCosts = { PerAccount: float; PerGrant: float; PerContribution: float; PerSponsor: float; PerException: float }

/// Activity-based unit costs: each activity's vendor labour (at the pool's effective hourly cost) and external
/// cost assigned to its driver; fixed and infrastructure costs spread per account.
let unitCosts (e: Eval) =
    let labourHours = e.Staffing.Pools |> List.sumBy (fun p -> p.Hours - p.FounderHours) |> max 1e-9
    let hourly = (e.Staffing.LabourCash + e.Staffing.BackupCash) / labourHours
    let byDriver (d: Driver) =
        e.Loads |> List.filter (fun l -> l.Activity.Driver = d)
        |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * l.VendorShare / 60.0 * hourly + l.ExternalCost * l.VendorShare)
    let overhead = e.Views.View1 - (e.Loads |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * l.VendorShare / 60.0 * hourly + l.ExternalCost * l.VendorShare))
    let humanEx = e.Loads |> List.sumBy (fun l -> l.HumanEvents * l.VendorShare) |> max 1e-9
    let exLabour = e.Loads |> List.sumBy (fun l -> (l.Minutes + l.AuthMinutes) * l.VendorShare / 60.0 * hourly)
    { PerAccount = (byDriver Driver.PerAccount + byDriver Driver.PerNewAccount + overhead) / max 1.0 e.Counts.Accounts
      PerGrant = (byDriver Driver.PerGrant + byDriver Driver.PerActiveCharity) / max 1.0 e.Counts.Grants
      PerContribution = byDriver Driver.PerContribution / max 1.0 e.Counts.Contributions
      PerSponsor = (byDriver Driver.PerSponsor + byDriver Driver.PerSponsorOnboarding) / max 1.0 e.Counts.Sponsors
      PerException = exLabour / humanEx }
