/// Deterministic operating-year simulation: daily arrivals by seasonality, constrained human pools,
/// FIFO queues with ageing, absences and seeded incidents. Pure (generator state threaded explicitly).
/// This is a theoretical capacity model; nothing here is measured production performance.
module ZeroBased.Simulation

open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Workload

let days = 365

/// Day-of-year (0-based, non-leap) to month (1-12).
let monthOf (d: int) =
    let ends = [ 31; 59; 90; 120; 151; 181; 212; 243; 273; 304; 334; 365 ]
    (ends |> List.findIndex (fun e -> d < e)) + 1

let isWeekend (d: int) = d % 7 = 5 || d % 7 = 6

let private monthEnds = set [ 30; 58; 89; 119; 150; 180; 211; 242; 272; 303; 333; 364 ]

let private nearMonthEnd (d: int) = monthEnds |> Set.exists (fun e -> e - d >= 0 && e - d < 3)

/// Raw (unnormalised) weight of a day under a seasonality profile. Weights are ASSUMPTION (parameters.csv
/// documents the year-end concentration used); arrivals are spread across calendar days.
let rawWeight (vals: Values) (profile: string) (d: int) : float =
    let m = monthOf d
    match profile with
    | "year_end" -> (if m = 12 then v vals "season_dec_weight" elif m = 11 then v vals "season_nov_weight" else 1.0)
    | "month_end" -> if nearMonthEnd d then 6.0 else 1.0
    | "quarter_end" -> if (m = 3 || m = 6 || m = 9 || m = 12) && nearMonthEnd d then 20.0 else 1.0
    | "tax_season" -> if m <= 4 then 2.0 else 1.0
    | "annual_q1" -> if m <= 3 then 1.0 else 0.0
    | _ -> 1.0

let weights (vals: Values) (profile: string) : float[] =
    let raw = Array.init days (rawWeight vals profile)
    let s = Array.sum raw
    raw |> Array.map (fun w -> w / s)

/// Work arriving into a pool on a day: hours and the SLA (in days) it must be finished within.
type Arrival = { Day: int; Hours: float; SlaDays: float }

type PoolResult =
    { Pool: string
      Staff: float
      ArrivedHours: float
      DoneHours: float
      PeakQueueHours: float
      PeakQueueAgeDays: float
      BreachedHours: float
      Utilisation: float
      PeakWeekHours: float
      IncidentHours: float }

/// Seeded incidents (security, integration failures, recovery) that add urgent hours to a pool.
type Incident = { Day: int; Pool: string; Hours: float; Kind: string }

let private lcg (s: uint64) =
    let n = s * 6364136223846793005UL + 1442695040888963407UL
    float (n >>> 11) / float (1UL <<< 53), n

/// Poisson-like draws per day via Bernoulli with p = rate/365 (rates are small). Deterministic for a seed.
let incidents (seed: uint64) (specs: (string * string * float * float) list) : Incident list =
    specs
    |> List.mapi (fun i (kind, pool, ratePerYear, hours) -> i, kind, pool, ratePerYear, hours)
    |> List.collect (fun (i, kind, pool, rate, hours) ->
        let p = rate / float days
        [ 0 .. days - 1 ]
        |> List.fold (fun (acc, st) d ->
            let u, st' = lcg st
            (if u < p then { Day = d; Pool = pool; Hours = hours; Kind = kind } :: acc else acc), st') ([], seed + uint64 (i * 7919))
        |> fst)

/// Arrivals for a pool from activity loads (vendor share only).
let arrivals (vals: Values) (poolOf: string -> string) (pool: string) (ls: Load list) : Arrival list =
    ls
    |> List.collect (fun l ->
        let primary = if poolOf l.Activity.Role = pool then l.Minutes * l.VendorShare / 60.0 else 0.0
        let auth = if poolOf "authorizer" = pool then l.AuthMinutes * l.VendorShare / 60.0 else 0.0
        let h = primary + auth
        if h <= 0.0 then []
        else
            let w = weights vals l.Activity.Seasonality
            // SLA hours are converted to business days (8 business hours per day), minimum one business day
            let sla = max 1.0 (l.Activity.SlaHours / 24.0)
            [ for d in 0 .. days - 1 do
                  if w.[d] > 0.0 then yield { Day = d; Hours = h * w.[d]; SlaDays = sla } ])
    |> List.groupBy (fun a -> a.Day, a.SlaDays)
    |> List.map (fun ((d, s), xs) -> { Day = d; SlaDays = s; Hours = xs |> List.sumBy (fun a -> a.Hours) })

let businessDays = [ 0 .. days - 1 ] |> List.filter (isWeekend >> not) |> List.length |> float

/// Productive hours per FTE-year (consistent with daily capacity).
let productiveHoursPerFte (vals: Values) = v vals "productive_hours_per_day" * (businessDays - v vals "absence_days")

/// Capacity of a pool on a day: staff x productive hours per business day, less absences.
/// Absence: each person is away `absence_days` business days a year, spread evenly (deterministic).
let capacity (vals: Values) (staff: float) (d: int) =
    if isWeekend d || staff <= 0.0 then 0.0
    else
        let perDay = v vals "productive_hours_per_day"
        let absent = v vals "absence_days" / businessDays
        staff * perDay * (1.0 - absent)

/// Cumulative business-day index: age in business days = bdIndex.[d] - bdIndex.[arrival].
/// Work arriving on a weekend starts its SLA clock on the next business day.
let bdIndex : int[] = [| 0 .. days - 1 |] |> Array.scan (fun acc d -> if isWeekend d then acc else acc + 1) 0 |> Array.tail

let businessAge (arrival: int) (d: int) = float (bdIndex.[d] - bdIndex.[arrival])

/// FIFO queue simulation. Queue items: (arrivalDay, slaDays, hours). Pure fold over days.
let runPool (vals: Values) (pool: string) (staff: float) (arr: Arrival list) (inc: Incident list) : PoolResult =
    let byDay = arr |> List.groupBy (fun a -> a.Day) |> Map.ofList
    let incByDay = inc |> List.filter (fun i -> i.Pool = pool) |> List.groupBy (fun i -> i.Day) |> Map.ofList
    let step (queue: (int * float * float) list, done_, peakH, peakAge, breached, weekly: float list) d =
        let newItems =
            (Map.tryFind d byDay |> Option.defaultValue [] |> List.map (fun a -> d, a.SlaDays, a.Hours))
            @ (Map.tryFind d incByDay |> Option.defaultValue [] |> List.map (fun i -> d, 1.0, i.Hours))
        // incidents are urgent: placed at the queue head
        let urgent, normal = newItems |> List.partition (fun (_, s, _) -> s <= 1.0)
        let q = urgent @ queue @ normal
        let cap = capacity vals staff d
        let rec serve (cap: float) items acc doneH brH =
            match items with
            | [] -> List.rev acc, doneH, brH
            | (ad, sla, h) :: rest when cap <= 0.0 -> serve 0.0 rest ((ad, sla, h) :: acc) doneH brH
            | (ad, sla, h) :: rest ->
                let take = min cap h
                let late = if businessAge ad d > sla then take else 0.0
                let rem = h - take
                let acc' = if rem > 1e-9 then (ad, sla, rem) :: acc else acc
                serve (cap - take) rest acc' (doneH + take) (brH + late)
        let q', doneH, brH = serve cap q [] 0.0 0.0
        let qh = q' |> List.sumBy (fun (_, _, h) -> h)
        let age = q' |> List.fold (fun m (ad, _, _) -> max m (businessAge ad d)) 0.0
        let arrivedToday = newItems |> List.sumBy (fun (_, _, h) -> h)
        (q', done_ + doneH, max peakH qh, max peakAge age, breached + brH, arrivedToday :: weekly)
    let q, doneH, peakH, peakAge, breached, dailyRev = [ 0 .. days - 1 ] |> List.fold step ([], 0.0, 0.0, 0.0, 0.0, [])
    // queue left at year end counts as breached if already past SLA
    let leftBreach = q |> List.sumBy (fun (ad, sla, h) -> if businessAge ad (days - 1) > sla then h else 0.0)
    let daily = dailyRev |> List.rev |> Array.ofList
    let peakWeek = [ 0 .. days - 7 ] |> List.fold (fun m s -> max m (Array.sum daily.[s .. s + 6])) 0.0
    let arrived = (arr |> List.sumBy (fun a -> a.Hours)) + (inc |> List.filter (fun i -> i.Pool = pool) |> List.sumBy (fun i -> i.Hours))
    let totalCap = [ 0 .. days - 1 ] |> List.sumBy (capacity vals staff)
    { Pool = pool
      Staff = staff
      ArrivedHours = arrived
      DoneHours = doneH
      PeakQueueHours = peakH
      PeakQueueAgeDays = peakAge
      BreachedHours = breached + leftBreach
      Utilisation = (if totalCap > 0.0 then doneH / totalCap else 0.0)
      PeakWeekHours = peakWeek
      IncidentHours = inc |> List.filter (fun i -> i.Pool = pool) |> List.sumBy (fun i -> i.Hours) }

/// Smallest staffing (in steps of `step` FTE) at which breached hours are within tolerance.
let minimumStaff (vals: Values) (pool: string) (arr: Arrival list) (inc: Incident list) : float * PoolResult =
    let step = v vals "staff_step_fte"
    let tol = v vals "sla_breach_tolerance"
    let arrived = (arr |> List.sumBy (fun a -> a.Hours)) + (inc |> List.filter (fun i -> i.Pool = pool) |> List.sumBy (fun i -> i.Hours))
    if arrived <= 0.0 then 0.0, runPool vals pool 0.0 arr inc
    else
        let ok s = (runPool vals pool s arr inc).BreachedHours <= tol * arrived
        // start from the average-load lower bound (fewer staff can never clear the year's work),
        // double until SLA tolerance is met, then bisect to the step resolution (breaches fall as staff rise)
        let perFteYear = [ 0 .. days - 1 ] |> List.sumBy (capacity vals 1.0)
        let lower = max step (floor (arrived / perFteYear / step) * step)
        let rec grow s = if ok s || s >= 400.0 then s else grow (s * 2.0)
        let hi = grow lower
        let rec bisect lo hi =
            // invariant: hi satisfies; lo does not (or lo = hi)
            if hi - lo <= step + 1e-9 then hi
            else
                let mid = lo + max step (floor ((hi - lo) / 2.0 / step) * step)
                if ok mid then bisect lo mid else bisect mid hi
        let s = if hi = lower then lower else bisect (hi / 2.0) hi
        s, runPool vals pool s arr inc
