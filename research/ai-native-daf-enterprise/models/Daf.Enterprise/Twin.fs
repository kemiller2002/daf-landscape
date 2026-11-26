/// Enterprise digital twin (addendum §23): a deterministic, seeded daily simulation of
/// human work queues, capacity, SLA breaches and liquidity under stress scenarios.
/// It runs on ASSUMED parameters until measured telemetry exists; every output is labeled simulated.
module Daf.Enterprise.Twin

open System
open Daf.Enterprise.Economics

type Queue =
    | GrantExceptions
    | ComplexAssetAcceptance
    | ServiceRecovery
    | ReconciliationBreaks

type Stress =
    { Name: string
      VolumeMultiplier: decimal          // grant recommendations
      ComplexMultiplier: decimal         // complex asset gifts
      ExceptionRateMultiplier: decimal   // e.g. fewer manual reviews (<1) or a new rule (>1)
      CustodianOutageDays: (int * int) option   // [start, end) day index
      SurgeDays: (int * int * decimal) option   // year-end surge window and multiplier
      CapacityMultiplier: decimal }      // e.g. staff illness, hiring freeze

let baseline =
    { Name = "baseline (year-end surge only)"
      VolumeMultiplier = 1m; ComplexMultiplier = 1m; ExceptionRateMultiplier = 1m
      CustodianOutageDays = None; SurgeDays = Some(330, 365, 3m); CapacityMultiplier = 1m }

type QueueStats =
    { Queue: Queue
      Arrived: decimal
      Served: decimal
      MaxBacklog: decimal
      DaysOverSla: int
      MeanWaitDays: decimal }

type TwinResult =
    { Stress: Stress
      Queues: QueueStats list
      MinLiquidityBufferDays: decimal
      LiquidityExhausted: bool
      Provenance: string }

/// Deterministic pseudo-random multiplier in [0.8, 1.2] (pure LCG, explicit state).
let private lcg (seed: uint64) = seed * 6364136223846793005UL + 1442695040888963407UL
let private noise (seed: uint64) = 0.8m + 0.4m * decimal (float (seed >>> 33) / float (1UL <<< 31))

type private QState = { Backlog: decimal; Arrived: decimal; Served: decimal; MaxBacklog: decimal; Over: int; WaitSum: decimal }

let private slaDays =
    function
    | GrantExceptions -> 2m
    | ComplexAssetAcceptance -> 10m
    | ServiceRecovery -> 1m
    | ReconciliationBreaks -> 3m

/// Simulate 365 days. Capacity per queue = FTE from the staffing model (Economics.fteByRole)
/// times productive hours per day, divided by handling time.
let simulate (ps: Parameters) (scn: Scenario) (stress: Stress) (seed: uint64) : TwinResult =
    let ftes = fteByRole ps scn |> Map.ofList
    let workDayHours = ps.ProductiveHoursPerFte.Value / 250m
    let perDay x = x / 365m
    let grantsPerDay = perDay (scn.Accounts * scn.GrantsPerAccount) * stress.VolumeMultiplier
    let contribPerDay = perDay (scn.Accounts * scn.ContributionsPerAccount)
    let arrivalsBase =
        Map.ofList
            [ GrantExceptions, grantsPerDay * scn.ExceptionRate * stress.ExceptionRateMultiplier
              ComplexAssetAcceptance, contribPerDay * scn.ComplexAssetShare * stress.ComplexMultiplier
              ServiceRecovery, perDay (scn.Accounts * ps.HumanContactsPerAccount.Value)
              ReconciliationBreaks, (grantsPerDay + contribPerDay) * ps.BreakRate.Value ]
    let capacity =
        let cap role handlingHours = ftes.[role] * workDayHours / handlingHours * stress.CapacityMultiplier
        Map.ofList
            [ GrantExceptions, cap Role.GrantsCompliance (ps.MinutesPerException.Value / 60m)
              ComplexAssetAcceptance, cap Role.ComplexAssets ps.HoursPerComplexAsset.Value
              ServiceRecovery, cap Role.ServiceRecovery (ps.MinutesPerHumanContact.Value / 60m)
              // one finance FTE is reserved for controller duties (SoD); the rest work breaks
              ReconciliationBreaks, (ftes.[Role.FinanceAndPaymentsOps] - 1m) * workDayHours / (ps.MinutesPerBreak.Value / 60m) * stress.CapacityMultiplier ]
    let queues = [ GrantExceptions; ComplexAssetAcceptance; ServiceRecovery; ReconciliationBreaks ]
    let inWindow day = function Some(a, b) -> day >= a && day < b | None -> false
    let surge day =
        match stress.SurgeDays with
        | Some(a, b, m) when day >= a && day < b -> m
        | _ -> 1m
    // Liquidity: cash buffer of 2% of AUM [A]; grants paid from cash; during custodian outage no liquidation refills it.
    let aumV = aum scn
    let dailyGrantDollars = aumV * 0.25m / 365m * stress.VolumeMultiplier   // ~25% aggregate payout (EV-014 order of magnitude)
    let refillPerDay = dailyGrantDollars   // normally liquidations keep the buffer level
    let step (states: Map<Queue, QState>, cash: decimal, minCash: decimal, seed: uint64) day =
        let seed' = lcg seed
        let k = noise seed'
        let outage = inWindow day stress.CustodianOutageDays
        let states' =
            queues
            |> List.fold (fun (m: Map<Queue, QState>) q ->
                let st = m.[q]
                let arrivals = arrivalsBase.[q] * k * (if q = GrantExceptions || q = ReconciliationBreaks then surge day else 1m)
                                * (if outage && q = ReconciliationBreaks then 3m else 1m)
                let avail = st.Backlog + arrivals
                let served = min avail capacity.[q]
                let backlog = avail - served
                let wait = if capacity.[q] > 0m then backlog / capacity.[q] else 999m
                m.Add(q, { Backlog = backlog; Arrived = st.Arrived + arrivals; Served = st.Served + served
                           MaxBacklog = max st.MaxBacklog backlog
                           Over = st.Over + (if wait > slaDays q then 1 else 0)
                           WaitSum = st.WaitSum + wait })) states
        let outflow = dailyGrantDollars * surge day * k
        let cash' = cash - outflow + (if outage then 0m else refillPerDay * surge day * k)
        (states', cash', min minCash cash', seed')
    let init = queues |> List.map (fun q -> q, { Backlog = 0m; Arrived = 0m; Served = 0m; MaxBacklog = 0m; Over = 0; WaitSum = 0m }) |> Map.ofList
    let buffer0 = aumV * 0.02m
    let (final, _, minCash, _) = [ 0 .. 364 ] |> List.fold step (init, buffer0, buffer0, seed)
    { Stress = stress
      Queues =
        queues |> List.map (fun q ->
            let st = final.[q]
            { Queue = q; Arrived = st.Arrived; Served = st.Served; MaxBacklog = st.MaxBacklog
              DaysOverSla = st.Over; MeanWaitDays = st.WaitSum / 365m })
      MinLiquidityBufferDays = if dailyGrantDollars = 0m then 0m else minCash / dailyGrantDollars
      LiquidityExhausted = minCash < 0m
      Provenance = "SIMULATED on assumed parameters (see 09-financial-models/parameter-register.csv); not measured behavior" }

let stresses =
    [ baseline
      { baseline with Name = "grant volume x10"; VolumeMultiplier = 10m }
      { baseline with Name = "complex asset gifts x2"; ComplexMultiplier = 2m }
      { baseline with Name = "custodian outage 5 business days during surge"; CustodianOutageDays = Some(340, 347) }
      { baseline with Name = "custodian outage 30 days during surge"; CustodianOutageDays = Some(335, 365) }
      { baseline with Name = "manual reviews halved (exception rate x0.5)"; ExceptionRateMultiplier = 0.5m }
      { baseline with Name = "new regulation doubles exceptions"; ExceptionRateMultiplier = 2m }
      { baseline with Name = "staff capacity -40% (illness/attrition)"; CapacityMultiplier = 0.6m } ]
