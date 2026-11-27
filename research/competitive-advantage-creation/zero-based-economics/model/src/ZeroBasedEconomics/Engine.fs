/// Cost engine: volumes, expense activation, human workload, staffing and coverage, revenue. Pure.
module ZeroBasedEconomics.Engine

open System
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Inputs

// ------------------------------------------------------------------------------------------------ realization

/// A realizer turns every named range into a value (a level, a Monte Carlo draw, a tornado swing).
type Realizer = string -> Range -> float

let atLevel (level: Level) : Realizer = fun _ r -> pick level r

/// Inputs for which the low end is the adverse end (more founder time, higher prices and fees are favourable).
let lowIsAdverse (name: string) =
    [ "PAR:founder_hours_per_year"; "PAR:lic_"; "PAR:wl_"; "PAR:tops_"; "PAR:ci_"; "PAR:mig_fee"; "PAR:admin_bps_ref"; "PAR:qualification_amortization_years"; "PAR:contractor_counts_hours" ]
    |> List.exists (fun (p: string) -> name.StartsWith(p, StringComparison.Ordinal))

/// Oriented scenario: Low = every input at its favourable end, High = every input at its adverse end.
let atOriented (level: Level) : Realizer =
    fun key r ->
        match level with
        | Base -> r.Base
        | Low -> if lowIsAdverse key then r.High else r.Low
        | High -> if lowIsAdverse key then r.Low else r.High

/// Replace every cost-side range with a point value. Profiles stay ranges: volume levels are chosen per scenario by
/// the independent factors, not by the realizer.
let realize (f: Realizer) (inp: Inputs) : Inputs =
    let p key r = point (f key r)
    { inp with
        Expenses =
            inp.Expenses
            |> List.map (fun e ->
                { e with
                    MinAnnual = p $"EXP:{e.Id}:min" e.MinAnnual
                    Amount = p $"EXP:{e.Id}:amount" e.Amount
                    IncrementalShare = p $"EXP:{e.Id}:incremental" e.IncrementalShare
                    AllocationShare = p $"EXP:{e.Id}:allocation" e.AllocationShare })
        Activities =
            inp.Activities
            |> List.map (fun a ->
                { a with
                    Rate = p $"ACT:{a.Id}:rate" a.Rate
                    HumanShare = p $"ACT:{a.Id}:share" a.HumanShare
                    Minutes = p $"ACT:{a.Id}:minutes" a.Minutes })
        Roles =
            inp.Roles
            |> List.map (fun r -> { r with LoadedAnnual = p $"ROLE:{r.Id}:loaded" r.LoadedAnnual; ContractHourly = p $"ROLE:{r.Id}:hourly" r.ContractHourly })
        Coverage = inp.Coverage |> List.map (fun c -> { c with AltAnnual = p $"COV:{c.Id}:alt" c.AltAnnual })
        Params = inp.Params |> Map.map (fun k r -> p $"PAR:{k}" r)
        Qualification = inp.Qualification |> List.map (fun (id, n, h, c, ev, ms) -> id, n, p $"QUAL:{id}:hours" h, p $"QUAL:{id}:cash" c, ev, ms) }

/// Every named range in the inputs (for tornado and Monte Carlo), in a stable order.
let namedRanges (inp: Inputs) : (string * Range) list =
    [ for e in inp.Expenses do
          yield $"EXP:{e.Id}:min", e.MinAnnual
          yield $"EXP:{e.Id}:amount", e.Amount
          yield $"EXP:{e.Id}:incremental", e.IncrementalShare
          yield $"EXP:{e.Id}:allocation", e.AllocationShare
      for a in inp.Activities do
          yield $"ACT:{a.Id}:rate", a.Rate
          yield $"ACT:{a.Id}:share", a.HumanShare
          yield $"ACT:{a.Id}:minutes", a.Minutes
      for r in inp.Roles do
          yield $"ROLE:{r.Id}:loaded", r.LoadedAnnual
          yield $"ROLE:{r.Id}:hourly", r.ContractHourly
      for c in inp.Coverage do
          yield $"COV:{c.Id}:alt", c.AltAnnual
      for KeyValue(k, r) in inp.Params do
          yield $"PAR:{k}", r
      for (id, _, h, c, _, _) in inp.Qualification do
          yield $"QUAL:{id}:hours", h
          yield $"QUAL:{id}:cash", c ]
    |> List.filter (fun (_, r) -> r.High > r.Low)

/// Parameter value (base of a realized input). Missing parameters are a programming error caught by validation.
let par (inp: Inputs) (name: string) =
    match Map.tryFind name inp.Params with
    | Some r -> r.Base
    | None -> failwithf "missing parameter '%s'" name

// ------------------------------------------------------------------------------------------------ volumes

/// Deterministic assignment of profiles to the first n customers by cycling the mix pattern.
let assign (mix: Mix) (n: int) : string list =
    match mix.Pattern with
    | [] -> []
    | pat -> List.init n (fun i -> List.item (i % List.length pat) pat)

let customerVolume (f: Factors) (p: Profile) : CustomerVolume =
    let acc = pick f.Acct p.Accounts
    let g = acc * pick f.Txn p.GrantsPerAccount
    let c = acc * pick f.Txn p.ContribsPerAccount
    { ProfileId = p.Id
      Accounts = acc
      AuaUsd = acc * pick f.Aua p.AuaPerAccount
      Grants = g
      Contribs = c
      Exceptions = (g + c) * pick f.Exc p.ExceptionRate }


/// Customers onboarded per year in a steady-state (run-rate) year: the expected value n x share, not rounded and
/// not forced to one (review findings ADV-A-05, ADV-O-11). Every model-M customer is a project in the year.
/// Growth years and the first customer's onboarding are costed explicitly in the capital path.
let newCustomers (inp: Inputs) (model: ModelId) (n: int) =
    if n = 0 then 0.0
    elif model = M then float n
    else float n * par inp "new_customer_share"

let volume (inp: Inputs) (model: ModelId) (sc: Scenario) : Volume =
    let mix = inp.Mixes |> List.find (fun m -> m.Id = sc.MixId)
    let profile id = inp.Profiles |> List.find (fun p -> p.Id = id)
    let per = assign mix sc.Customers |> List.map (profile >> customerVolume sc.Factors)
    let sum f = per |> List.sumBy f
    let g, c = sum (fun v -> v.Grants), sum (fun v -> v.Contribs)
    { Customers = sc.Customers
      PerCustomer = per
      Accounts = sum (fun v -> v.Accounts)
      AuaM = sum (fun v -> v.AuaUsd) / 1e6
      Grants = g
      Contribs = c
      Transactions = g + c
      Exceptions = sum (fun v -> v.Exceptions)
      NewCustomers = newCustomers inp model sc.Customers }

let metricValue (v: Volume) (m: Metric) =
    match m with
    | Always -> 1.0
    | Customers -> float v.Customers
    | Accounts -> v.Accounts
    | AuaM -> v.AuaM
    | Transactions -> v.Transactions
    | Exceptions -> v.Exceptions
    | NewCustomers -> v.NewCustomers

// ------------------------------------------------------------------------------------------------ expenses

type Bearer =
    | EF
    | Sponsor

type ExpenseLine =
    { Expense: Expense
      Bearer: Bearer
      Units: float
      Gross: float
      Cash: float
      Allocated: float }

let triggered (e: Expense) (v: Volume) =
    e.TriggerMetric = Always || metricValue v e.TriggerMetric >= e.TriggerThreshold

let units (e: Expense) (v: Volume) =
    match e.Driver with
    | Fixed -> 1.0
    | Per m -> metricValue v m
    | Step(m, cap) -> max 1.0 (ceil (metricValue v m / cap))

/// Annual gross cost of an active expense: at least its minimum, otherwise units x amount.
let gross (e: Expense) (v: Volume) = max e.MinAnnual.Base (units e v * e.Amount.Base)

let applies (tier: int) (e: Expense) = tierOf e.Obligation <= tier

let expenseLines (inp: Inputs) (model: ModelId) (sc: Scenario) (v: Volume) : ExpenseLine list =
    inp.Expenses
    |> List.filter (fun e -> applies sc.Tier e && triggered e v)
    |> List.collect (fun e ->
        let g = gross e v
        let line bearer =
            { Expense = e
              Bearer = bearer
              Units = units e v
              Gross = g
              Cash = (if bearer = EF then g * e.IncrementalShare.Base else g)
              Allocated = (if bearer = EF then g * max e.IncrementalShare.Base e.AllocationShare.Base else g) }
        [ if e.EfModels.Contains model then yield line EF
          if e.SponsorModels.Contains model then yield line Sponsor ])

// ------------------------------------------------------------------------------------------------ workload

/// Exception intensity of a volume: transaction-weighted mean multiplier (1.0 when there are no transactions).
let excMult (v: Volume) = if v.Transactions > 0.0 then v.Exceptions / v.Transactions else 1.0

let driverUnits (v: Volume) (d: ActDriver) =
    match d with
    | PerGrantException -> v.Grants * excMult v
    | PerContributionException -> v.Contribs * excMult v
    | PerTransactionException -> v.Transactions * excMult v
    | PerGrant -> v.Grants
    | PerContribution -> v.Contribs
    | PerTransaction -> v.Transactions
    | PerAccount -> v.Accounts
    | PerException -> v.Exceptions
    | PerCustomer -> float v.Customers
    | PerNewCustomer -> v.NewCustomers
    | FixedYear -> 1.0

let activityHours (v: Volume) (a: Activity) =
    if v.Customers < a.MinCustomers then 0.0
    else
    driverUnits v a.Driver * a.Rate.Base * a.HumanShare.Base * a.Minutes.Base / 60.0

/// Hours per role borne by Echelon Foundry (EF) and by the sponsor for a model.
let hoursByRole (inp: Inputs) (model: ModelId) (v: Volume) : Map<string, float> * Map<string, float> =
    let total pick =
        inp.Activities
        |> List.filter pick
        |> List.map (fun a -> a.Role, activityHours v a)
        |> List.groupBy fst
        |> List.map (fun (r, xs) -> r, xs |> List.sumBy snd)
        |> Map.ofList
    total (fun a -> a.EfModels.Contains model), total (fun a -> a.SponsorModels.Contains model)

// ------------------------------------------------------------------------------------------------ staffing

type RoleOutcome =
    { RoleId: string
      Hours: float
      FounderHours: float
      Employees: int
      ContractHours: float
      Cash: float
      Noncash: float }

/// Staff one role: the founder takes what capacity allows (if eligible); the residual is contracted below the hire
/// threshold and employed above it, never below `minEmployees` (coverage).
let staffRole (founderRate: float) (overhead: float) (r: Role) (hours: float) (founderCap: float) (minEmployees: int) : RoleOutcome =
    // Employees forced by coverage absorb work before the founder (ADV-A-06), freeing founder hours for later roles.
    let forced = min hours (float minEmployees * r.ProductiveHours)
    let fh = if r.FounderEligible then min (hours - forced) (max 0.0 founderCap) else 0.0
    let residual = hours - fh
    // Whole employees for whole FTEs of residual work; a remainder above the hire threshold is one more employee,
    // a smaller remainder is contracted.
    let whole = int (floor (residual / r.ProductiveHours))
    let byLoad = if residual - float whole * r.ProductiveHours > r.HireThresholdHours then whole + 1 else whole
    let emp = max byLoad minEmployees
    let contract = max 0.0 (residual - float emp * r.ProductiveHours)
    { RoleId = r.Id
      Hours = hours
      FounderHours = fh
      Employees = emp
      ContractHours = contract
      Cash = float emp * (r.LoadedAnnual.Base + overhead) + contract * r.ContractHourly.Base
      Noncash = fh * founderRate }

/// Staff all roles in register order, threading the founder's remaining capacity.
let staffAll (founderRate: float) (overhead: float) (founderCap: float) (roles: Role list) (hours: Map<string, float>) (minEmp: Map<string, int>) =
    roles
    |> List.fold (fun (acc, cap) r ->
        let h = Map.tryFind r.Id hours |> Option.defaultValue 0.0
        let o = staffRole founderRate overhead r h cap (Map.tryFind r.Id minEmp |> Option.defaultValue 0)
        o :: acc, cap - o.FounderHours) ([], founderCap)
    |> fun (acc, cap) -> List.rev acc, cap

type CoverageChoice =
    { CoverageId: string
      RoleId: string
      Shortfall: int
      Choice: string
      Annual: float }

/// Coverage and segregation-of-duties requirements: distinct qualified people beyond the workload-derived staff.
/// The founder counts as one person for a founder-eligible role. For each role, every option "hire k more people,
/// meet each requirement still short through its own permitted alternative" is costed and the cheapest feasible
/// option is chosen. A hire satisfies every requirement on its role; an alternative satisfies only its own
/// requirement (a contracted code reviewer is not on-call cover). A requirement without a permitted alternative
/// forces hiring.
let applyCoverage (inp: Inputs) (model: ModelId) (sc: Scenario) (founderRate: float) (founderCap: float) (hours: Map<string, float>) =
    let staffed0, _ = staffAll founderRate (par inp "employee_overhead") founderCap inp.Roles hours Map.empty
    let roleOf id = inp.Roles |> List.find (fun r -> r.Id = id)
    let cost0 = staffed0 |> List.sumBy (fun o -> o.Cash)
    let employees0 id = (staffed0 |> List.find (fun o -> o.RoleId = id)).Employees
    let shortfalls =
        inp.Coverage
        |> List.filter (fun c -> c.Models.Contains model && tierOf c.Obligation <= sc.Tier && sc.Customers >= c.TriggerCustomers)
        |> List.map (fun c ->
            // The founder counts only in a role the founder actually works (ADV-A-07, ADV-P-03); a regular contractor
            // with at least `contractor_counts_hours` a year counts as one person (ADV-O-02).
            let o = staffed0 |> List.find (fun o -> o.RoleId = c.Role)
            let founder = if (roleOf c.Role).FounderEligible && o.FounderHours > 0.0 then 1 else 0
            let contractor = if o.ContractHours >= par inp "contractor_counts_hours" then 1 else 0
            c, max 0 (c.MinPeople - (employees0 c.Role + founder + contractor)))
        |> List.filter (fun (_, s) -> s > 0)
    let plans =
        shortfalls
        |> List.groupBy (fun (c, _) -> c.Role)
        |> List.map (fun (roleId, reqs) ->
            let maxShort = reqs |> List.map snd |> List.max
            let option k =
                let still = reqs |> List.filter (fun (_, s) -> s > k)
                if still |> List.exists (fun (c, _) -> not c.AltAllowed) then None
                else
                    let hireCost =
                        if k = 0 then 0.0
                        else
                            let st, _ = staffAll founderRate (par inp "employee_overhead") founderCap inp.Roles hours (Map.ofList [ roleId, employees0 roleId + k ])
                            (st |> List.sumBy (fun o -> o.Cash)) - cost0
                    let alts = still |> List.map (fun (c, s) -> c, s - k, c.AltAnnual.Base * float (s - k))
                    Some(k, hireCost + (alts |> List.sumBy (fun (_, _, a) -> a)), hireCost, alts)
            let k, _, hireCost, alts =
                [ 0..maxShort ] |> List.choose option |> List.minBy (fun (k, total, _, _) -> total, k)
            let choices =
                [ if k > 0 then
                      let first = reqs |> List.maxBy snd |> fst
                      yield { CoverageId = first.Id; RoleId = roleId; Shortfall = k; Choice = "hire"; Annual = hireCost }
                  for (c, s, a) in alts do
                      yield { CoverageId = c.Id; RoleId = roleId; Shortfall = s; Choice = "alternative"; Annual = a } ]
            (roleId, employees0 roleId + k), choices)
    let minEmp = plans |> List.filter (fun ((_, n), _) -> n > 0) |> List.map fst |> Map.ofList
    let choices = plans |> List.collect snd
    let staffed, capLeft = staffAll founderRate (par inp "employee_overhead") founderCap inp.Roles hours minEmp
    let altCash = choices |> List.filter (fun ch -> ch.Choice = "alternative") |> List.sumBy (fun ch -> ch.Annual)
    staffed, choices, altCash, capLeft

// ------------------------------------------------------------------------------------------------ revenue

let revenueAt (inp: Inputs) (model: ModelId) (bps: float) (v: Volume) =
    let n = float v.Customers
    match model with
    | L -> n * par inp "lic_platform_fee" + v.Accounts * par inp "lic_per_account"
    | W -> n * par inp "wl_platform_fee" + v.Accounts * par inp "wl_per_account"
    | T -> n * par inp "lic_platform_fee" + v.Accounts * (par inp "lic_per_account" + par inp "tops_per_account")
    | F -> v.AuaM * 1e6 * bps / 10000.0
    | C -> n * par inp "ci_subscription"
    | M -> v.NewCustomers * par inp "mig_fee_base" + v.Accounts * par inp "mig_fee_per_account"

let revenue (inp: Inputs) (model: ModelId) (v: Volume) = revenueAt inp model (par inp "admin_bps_ref") v

// ------------------------------------------------------------------------------------------------ outcome

type Outcome =
    { Scenario: Scenario
      Model: ModelId
      Volume: Volume
      Lines: ExpenseLine list
      Roles: RoleOutcome list
      Coverage: CoverageChoice list
      EfHours: Map<string, float>
      SponsorHours: float
      EfNonLaborCash: float
      EfNonLaborAllocated: float
      LaborCash: float
      FounderHours: float
      FounderCapacity: float
      FounderNoncash: float
      EfCash: float
      FullyLoaded: float
      SponsorCost: float
      Revenue: float
      Employees: int
      ContractHours: float }

/// Founder-only management hours: fixed, per customer and per new customer (sales, contracting, onboarding lead).
/// A parameter with an optional per-model override ("name_<model>").
let parFor (inp: Inputs) (name: string) (model: ModelId) =
    match Map.tryFind (name + "_" + modelCode model) inp.Params with
    | Some r -> r.Base
    | None -> par inp name

let founderOverhead (inp: Inputs) (model: ModelId) (v: Volume) =
    par inp "founder_fixed_hours"
    + parFor inp "founder_hours_per_customer" model * float v.Customers
    + parFor inp "founder_hours_per_new_customer" model * v.NewCustomers

/// Evaluate one scenario under one commercial model, on already-realized inputs.
let evaluateVolume (inp: Inputs) (model: ModelId) (sc: Scenario) (v: Volume) : Outcome =
    let lines = expenseLines inp model sc v
    let efHours0, spHours = hoursByRole inp model v
    let efHours = efHours0 |> Map.change "management" (fun h -> Some(Option.defaultValue 0.0 h + founderOverhead inp model v))
    let rate = par inp "founder_imputed_rate"
    let cap = par inp "founder_hours_per_year"
    let staffed, cov, altCash, capLeft = applyCoverage inp model sc rate cap efHours
    let ef = lines |> List.filter (fun l -> l.Bearer = EF)
    let nonLaborCash = ef |> List.sumBy (fun l -> l.Cash)
    let nonLaborAlloc = ef |> List.sumBy (fun l -> l.Allocated)
    let laborCash = (staffed |> List.sumBy (fun o -> o.Cash)) + altCash
    let founderNoncash = staffed |> List.sumBy (fun o -> o.Noncash)
    let qualAmort =
        // Only the build items a model needs are amortised to it (ADV-A-15); validation items are not build cost.
        let total =
            inp.Qualification
            |> List.filter (fun (id, _, _, _, _, ms) -> ms.Contains model && not (id.StartsWith("VAL", StringComparison.Ordinal)))
            |> List.sumBy (fun (_, _, h, c, _, _) -> c.Base + h.Base * rate)
        total / par inp "qualification_amortization_years"
    let spHoursTotal = spHours |> Map.toList |> List.sumBy snd
    { Scenario = sc
      Model = model
      Volume = v
      Lines = lines
      Roles = staffed
      Coverage = cov
      EfHours = efHours
      SponsorHours = spHoursTotal
      EfNonLaborCash = nonLaborCash
      EfNonLaborAllocated = nonLaborAlloc
      LaborCash = laborCash
      FounderHours = cap - capLeft
      FounderCapacity = cap
      FounderNoncash = founderNoncash
      EfCash = nonLaborCash + laborCash
      FullyLoaded = nonLaborAlloc + laborCash + founderNoncash + qualAmort
      SponsorCost =
        (lines |> List.filter (fun l -> l.Bearer = Sponsor) |> List.sumBy (fun l -> l.Gross))
        + spHoursTotal * par inp "sponsor_staff_rate"
      Revenue = revenue inp model v
      Employees = staffed |> List.sumBy (fun o -> o.Employees)
      ContractHours = staffed |> List.sumBy (fun o -> o.ContractHours) }

let evaluate (inp: Inputs) (model: ModelId) (sc: Scenario) : Outcome = evaluateVolume inp model sc (volume inp model sc)

/// A volume made of explicit customers (used for single-customer scaling and prior-estimate comparisons).
let volumeOf (inp: Inputs) (model: ModelId) (per: CustomerVolume list) : Volume =
    let sum f = per |> List.sumBy f
    let g, c = sum (fun v -> v.Grants), sum (fun v -> v.Contribs)
    { Customers = List.length per
      PerCustomer = per
      Accounts = sum (fun v -> v.Accounts)
      AuaM = sum (fun v -> v.AuaUsd) / 1e6
      Grants = g
      Contribs = c
      Transactions = g + c
      Exceptions = sum (fun v -> v.Exceptions)
      NewCustomers = newCustomers inp model (List.length per) }

let scaleCustomer (k: float) (cv: CustomerVolume) =
    { cv with Accounts = cv.Accounts * k; AuaUsd = cv.AuaUsd * k; Grants = cv.Grants * k; Contribs = cv.Contribs * k; Exceptions = cv.Exceptions * k }
