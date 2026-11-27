/// Staffing derived from simulated workload, control coverage and founder capacity. Pure.
/// Order of preference (mission principle 3): automation (already in workload) -> sponsor / external
/// (config shares) -> founder and shared capacity -> fractional professionals -> dedicated employees.
module ZeroBased.Staffing

open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Workload
open ZeroBased.Simulation

let poolOf (roles: Role list) (role: string) =
    roles |> List.tryFind (fun r -> r.Id = role) |> Option.map (fun r -> r.Pool) |> Option.defaultValue "OPS"

let pools (roles: Role list) = roles |> List.map (fun r -> r.Pool) |> List.distinct

/// Pools whose work must be done by persons independent of payment initiation (segregation of duties).
let criticalPools = set [ "OPS"; "AUTH"; "FINANCE" ]

/// Minimum distinct named persons per pool when the pool has work: primary + trained backup for the
/// segregated control pools; author + two non-author approvers for engineering (Unbound CNV-PLT-010).
let minNamed (vals: Values) (pool: string) =
    match pool with
    | "OPS" | "AUTH" | "FINANCE" -> v vals "min_named_control_pool"
    | "ENG" -> v vals "min_named_engineering"
    | "COMPLIANCE" | "COMM" -> 1.0
    | _ -> 0.0

type PoolStaffing =
    { Pool: string
      Hours: float
      SimulatedFte: float
      FounderHours: float
      Mode: string
      DedicatedFte: float
      FractionalHours: float
      Cost: float
      FounderImputedCost: float
      NamedPersons: int
      Sim: PoolResult }

/// Hours-weighted member-role cost parameters of a pool.
let private poolRates (level: Level) (roles: Role list) (byRole: Map<string, float>) (pool: string) =
    let members = roles |> List.filter (fun r -> r.Pool = pool)
    let w (r: Role) = Map.tryFind r.Id byRole |> Option.defaultValue 0.0
    let total = members |> List.sumBy w
    let avg (f: Role -> float) =
        if total > 0.0 then (members |> List.sumBy (fun r -> f r * w r)) / total
        else members |> List.tryHead |> Option.map f |> Option.defaultValue 0.0
    avg (fun r -> pick level r.DedicatedCost),
    avg (fun r -> pick level r.FractionalRate),
    members |> List.sumBy (fun r -> r.MinFraction),
    (members |> List.tryHead |> Option.map (fun r -> r.DedicateThreshold) |> Option.defaultValue 0.6)

/// Founder hours offset commercial work first, then engineering (never the independent control pools).
let founderAllocation (vals: Values) (hoursByPool: Map<string, float>) : Map<string, float> =
    let avail = v vals "founder_hours_per_year"
    [ "COMM"; "ENG" ]
    |> List.fold (fun (left, acc) p ->
        let need = Map.tryFind p hoursByPool |> Option.defaultValue 0.0
        let taken = min left need
        left - taken, Map.add p taken acc) (avail, Map.empty)
    |> snd

let staffPool (simulate: bool) (level: Level) (vals: Values) (roles: Role list) (cfg: Config) (byRole: Map<string, float>)
              (founder: Map<string, float>) (arr: Arrival list) (inc: Incident list) (pool: string) : PoolStaffing =
    let dedicatedCost, fracRate, minFraction, threshold = poolRates level roles byRole pool
    let productive = productiveHoursPerFte vals
    let fHours = Map.tryFind pool founder |> Option.defaultValue 0.0
    let hours = (arr |> List.sumBy (fun a -> a.Hours)) + (inc |> List.filter (fun i -> i.Pool = pool) |> List.sumBy (fun i -> i.Hours))
    // founder-covered hours are removed proportionally from arrivals before the queue simulation
    let scale = if hours > 0.0 then max 0.0 (hours - fHours) / hours else 1.0
    let arr' = arr |> List.map (fun a -> { a with Hours = a.Hours * scale })
    let inc' = inc |> List.map (fun i -> if i.Pool = pool then { i with Hours = i.Hours * scale } else i)
    let simFte, sim =
        if simulate then minimumStaff vals pool arr' inc'
        else
            // analytic mode (Monte Carlo and break-even scans): average load x peak factor calibrated from the simulation
            let perFteYear = productive
            let h = max 0.0 (hours - fHours)
            let step = v vals "staff_step_fte"
            let fte = if h <= 0.0 then 0.0 else ceil (h * v vals "analytic_peak_factor" / perFteYear / step - 1e-9) * step
            fte, { Pool = pool; Staff = fte; ArrivedHours = h; DoneHours = h; PeakQueueHours = nan; PeakQueueAgeDays = nan
                   BreachedHours = nan; Utilisation = (if fte > 0.0 then h / (fte * perFteYear) else 0.0); PeakWeekHours = nan; IncidentHours = nan }
    let residualHours = hours - fHours
    let floorFte = if cfg.VendorRunsControls || pool = "ENG" then minFraction else 0.0
    // Average load decides whether a dedicated hire is justified; simulated peak concurrency decides how many
    // people must be available (named persons) and, once dedicated, the headcount needed to meet SLAs.
    let avgFte = max 0.0 residualHours / productive
    let mode, ded, frac, cost =
        if residualHours <= 0.0 && floorFte <= 0.0 then "none", 0.0, 0.0, 0.0
        elif max avgFte floorFte < threshold then
            let h = max residualHours (floorFte * productive)
            "fractional", 0.0, h, h * fracRate * v vals "fractional_availability_premium"
        else
            let step = v vals "hire_step_fte"
            let toStep x = ceil (x / step - 1e-9) * step
            let nPeak = toStep (max (avgFte / v vals "max_dedicated_utilisation") simFte)
            let nAvg = toStep (avgFte / v vals "max_dedicated_utilisation")
            // Surge option (operations and finance only): permanent staff sized to average load; hours that would
            // breach SLA at that headcount are bought from trained surge contractors at a premium.
            let surgeAllowed = (pool = "OPS" || pool = "FINANCE") && simulate && nAvg < nPeak
            let surgeHours = if surgeAllowed then (runPool vals pool nAvg arr' inc').BreachedHours else 0.0
            let surgeCost = nAvg * dedicatedCost + surgeHours * fracRate * v vals "surge_rate_multiplier" + (if surgeHours > 0.0 then v vals "surge_readiness_cost" else 0.0)
            if surgeAllowed && surgeCost < nPeak * dedicatedCost then "dedicated+surge", nAvg, surgeHours, surgeCost
            else "dedicated", nPeak, 0.0, nPeak * dedicatedCost
    let hasWork = not (residualHours <= 0.0 && floorFte <= 0.0 && fHours <= 0.0)
    let founderPerson = if fHours > 0.0 then 1.0 else 0.0
    let peakPersons = if mode = "fractional" then ceil (simFte - 1e-9) else 0.0
    let named = if hasWork then int (max (minNamed vals pool) (max (ceil ded + (if mode = "fractional" then 1.0 else 0.0) + founderPerson) peakPersons)) else 0
    { Pool = pool
      Hours = hours
      SimulatedFte = simFte
      FounderHours = fHours
      Mode = mode
      DedicatedFte = ded
      FractionalHours = frac
      Cost = cost
      FounderImputedCost = fHours * v vals "founder_opportunity_rate"
      NamedPersons = named
      Sim = sim }

/// Retained persons who make up the minimum named coverage (backups, independent approvers) beyond staff
/// already counted: each costs a readiness retainer plus their share of review work is already in the hours.
let backupCost (vals: Values) (roles: Role list) (level: Level) (s: PoolStaffing) =
    if s.NamedPersons = 0 then 0.0
    else
        let counted = ceil s.DedicatedFte + (if s.Mode = "fractional" || s.Mode = "dedicated+surge" then 1.0 else 0.0) + (if s.FounderHours > 0.0 then 1.0 else 0.0)
        let missing = max 0.0 (float s.NamedPersons - counted)
        let _, rate, _, _ = poolRates level roles Map.empty s.Pool
        missing * v vals "backup_retainer_hours" * rate

type Staffing =
    { Pools: PoolStaffing list
      LabourCash: float
      BackupCash: float
      FounderImputed: float
      DedicatedFte: float
      FractionalHours: float
      NamedPersons: int
      IndependentPersons: int }

let staffing (simulate: bool) (level: Level) (vals: Values) (roles: Role list) (cfg: Config) (ls: Load list) (inc: Incident list) : Staffing =
    let byRole = hoursByRole true ls
    let pf = poolOf roles
    let ps = pools roles
    let incHours p = inc |> List.filter (fun i -> i.Pool = p) |> List.sumBy (fun i -> i.Hours)
    // analytic mode needs only hours per pool; daily arrivals are built only when simulating
    let arrByPool =
        if simulate then ps |> List.map (fun p -> p, arrivals vals pf p ls) |> Map.ofList
        else
            let byPool =
                ls |> List.collect (fun l -> [ pf l.Activity.Role, l.Minutes * l.VendorShare / 60.0; pf "authorizer", l.AuthMinutes * l.VendorShare / 60.0 ])
                |> List.filter (fun (_, h) -> h > 0.0)
                |> List.groupBy fst |> List.map (fun (p, xs) -> p, xs |> List.sumBy snd) |> Map.ofList
            ps |> List.map (fun p -> p, (match Map.tryFind p byPool with Some h -> [ { Day = 0; Hours = h; SlaDays = 365.0 } ] | None -> [])) |> Map.ofList
    let hoursByPool = ps |> List.map (fun p -> p, (arrByPool.[p] |> List.sumBy (fun a -> a.Hours)) + incHours p) |> Map.ofList
    let founder = founderAllocation vals hoursByPool
    let staffed = ps |> List.map (fun p -> staffPool simulate level vals roles cfg byRole founder arrByPool.[p] inc p)
    let backups = staffed |> List.sumBy (backupCost vals roles level)
    let independent =
        staffed |> List.filter (fun s -> Set.contains s.Pool criticalPools && s.NamedPersons > 0) |> List.sumBy (fun s -> s.NamedPersons)
    { Pools = staffed
      LabourCash = staffed |> List.sumBy (fun s -> s.Cost)
      BackupCash = backups
      FounderImputed = staffed |> List.sumBy (fun s -> s.FounderImputedCost)
      DedicatedFte = staffed |> List.sumBy (fun s -> s.DedicatedFte)
      FractionalHours = staffed |> List.sumBy (fun s -> s.FractionalHours)
      NamedPersons = staffed |> List.sumBy (fun s -> s.NamedPersons)
      IndependentPersons = independent }
