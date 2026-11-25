/// Outcome-designed, workload-driven organizations. Pure functions; no I/O, no mutation.
/// Replaces the previous study's ratio-based hiring triggers (operations manager after 4 added staff, integration
/// engineer and implementation analyst per 8 sponsors, fund accountant per 15,000 accounts, compliance officer
/// above 10,000 accounts) with skill pools whose capacity follows the hours the portfolio actually generates.
/// Every parameter is labelled where it is defined (Designs.fs). Research tool, not a forecast.
module CapitalMinimization.Design

open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Parameters

/// A skill pool. Work that needs the skill is a share of the servicing hours; people in the pool and added
/// capacity (employees, or fractional contractors at a premium) supply it.
type Pool =
    { Name: string
      /// Share of account-level and sponsor-level servicing hours that need this skill.
      Share: float
      LoadedHourly: float
      /// Premium on fractional contracted capacity over the employee loaded rate.
      ContractPremium: float
      /// Capacity floor in FTE regardless of workload (absence cover, independence).
      MinimumFte: float
      /// Capacity below one FTE may be bought fractionally (contract); otherwise whole employees are hired.
      Fractional: bool }

/// A person on the core payroll. QueueShare is the fraction of their productive hours available to the pool.
type Person =
    { Title: string
      LoadedCost: float
      CashCost: float
      Pool: string
      QueueShare: float
      StartMonth: int
      /// May prepare or release money movement (never the same item twice).
      MoneyAuthority: bool }

type Design =
    { Name: string
      People: Person list
      Pools: Pool list
      /// Fixed contracted specialists and assurance (audit, SOC, fractional review, security testing).
      Contracted: (string * float) list
      NonPersonnel: (string * float) list
      /// Per-person overhead (software seats, equipment, PEO, training, travel).
      PerPersonOverhead: float
      /// Sponsor-level human minutes per sponsor-year (close, reporting, configuration, incidents, audit support).
      SponsorMinutes: float
      /// Relationship and change-request hours per sponsor-year (pool: operations).
      RelationshipHours: float
      /// Integration upkeep hours of the first live sponsor in a year; later sponsors follow the learning curve.
      IntegrationFirstSponsorHours: float
      /// Hours multiplier per doubling of the number of integrated sponsors (1.0 = no learning).
      IntegrationLearningRate: float
      IntegrationPool: string
      /// Coordination hours per pair of people per week (meetings, handoffs, status).
      CoordinationHoursPerPairWeek: float
      ProductiveHours: float
      Utilisation: float
      DecemberShare: float
      PeakPremium: float
      /// A sponsor-appointed authority approves releases (work transferred to the sponsor, not eliminated).
      SponsorApprover: bool
      /// An independent contracted reviewer covers reconciliation review and absence of the releaser.
      ContractedIndependentReviewer: bool }

/// Account-level AI-native market-mix minutes per account-year in the previous study (50.7). [D]
let baseMarketMinutes =
    archetypeTable |> List.sumBy (fun a -> a.ShareOfAccounts * a.Minutes AiNative)

/// Rescale a sponsor's account minutes so that the market mix would generate `target` minutes per account-year
/// (AI-native approach). Tails keep their relative weight: a high-frequency account stays ~2.6x typical.
let withTarget (target: float) (s: Sponsor) =
    let k = target / baseMarketMinutes
    { s with Mix = s.Mix |> List.map (fun a -> { a with Minutes = (fun ap -> a.Minutes ap * k) }) }

/// Integration upkeep hours for n sponsors on a learning curve: h1 x i^(log2 rate), summed over sponsors.
let integrationHours (first: float) (rate: float) (n: int) =
    let b = System.Math.Log(rate, 2.0)
    [ 1 .. n ] |> List.sumBy (fun i -> first * (float i ** b))

type PoolResult =
    { Pool: string
      Hours: float
      CoreHours: float
      AddedFte: float
      /// Employees hired (the rest of AddedFte is fractional contracted capacity).
      Hires: float
      AddedCost: float
      PeakCost: float }

type DesignResult =
    { Base: Result
      Pools: PoolResult list
      /// Employees (core plus hires); fractional contracted capacity is excluded.
      Headcount: float
      ContractedFte: float
      CoordinationCost: float
      ContractedCost: float
      PerPersonCost: float
      IntegrationHours: float
      HumanMinutesPerAccount: float
      ControlFeasible: bool
      ControlNote: string }

let private poolQueueHours (d: Design) = d.ProductiveHours * d.Utilisation

/// Whether the design can separate preparation from release and cover an absence without collapsing duties.
let controlCheck (d: Design) (addedOpsPeople: float) =
    let internalAuthority = (d.People |> List.filter (fun p -> p.MoneyAuthority) |> List.length |> float) + addedOpsPeople
    match internalAuthority with
    | n when n >= 3.0 -> true, "three or more authorised people: preparation, release and absence cover separable"
    | n when n >= 2.0 && d.ContractedIndependentReviewer -> true, "two authorised people plus a contracted independent reviewer; absence of either suspends release to the sponsor-appointed authority"
    | n when n >= 2.0 -> false, "two authorised people: separation holds only while both are present; no absence cover"
    | n when n >= 1.0 && d.SponsorApprover && d.ContractedIndependentReviewer ->
        false, "one authorised person; release depends on sponsor approval and a contractor (transferred, not eliminated); single point of failure"
    | _ -> false, "no separation of duties possible"

/// Annual result of a design for a portfolio at a handling-time target (account minutes per account-year).
let evaluateDesign (d: Design) (target: float) (price: Price) (stress: Stress) (sponsors0: Sponsor list) =
    let sponsors = stressedSponsors price stress (sponsors0 |> List.map (withTarget target))
    let revenues = sponsors |> List.map (sponsorRevenue price stress.AssetFactor)
    let assetFee = revenues |> List.sumBy (fun (a, _, _) -> a)
    let topUp = revenues |> List.sumBy (fun (_, t, _) -> t)
    let other = revenues |> List.sumBy (fun (_, _, o) -> o)
    let revenue = assetFee + topUp + other
    let assets = sponsors |> List.sumBy (sponsorAssets stress.AssetFactor)
    let accounts = sponsors |> List.sumBy (fun s -> s.Accounts)
    let n = List.length sponsors
    let accountHours = sponsors |> List.sumBy (sponsorHours AiNative stress [])
    let sponsorLevelHours = float n * d.SponsorMinutes / 60.0 * stress.MinutesFactor
    let servicingHours = accountHours + sponsorLevelHours
    let integration = integrationHours d.IntegrationFirstSponsorHours d.IntegrationLearningRate n
    let relationship = float n * d.RelationshipHours
    let decemberAccount = sponsors |> List.sumBy (sponsorDecemberHours 0.0 AiNative stress [])
    let external = sponsors |> List.sumBy (sponsorExternalCost AiNative price.PaymentsPassThrough stress [])
    let q = poolQueueHours d
    let pools =
        d.Pools
        |> List.map (fun p ->
            let extra = (if p.Name = d.IntegrationPool then integration else 0.0) + (if p.Name = "operations" then relationship else 0.0)
            let hours = servicingHours * p.Share + extra
            let corePeople = d.People |> List.filter (fun x -> x.Pool = p.Name)
            let coreFte = corePeople |> List.sumBy (fun x -> x.QueueShare)
            let coreHours = coreFte * q
            let needed = max (max 0.0 (hours - coreHours) / q) (max 0.0 (p.MinimumFte - coreFte))
            // Workload-driven hiring: an employee is hired once the residual need reaches 0.75 FTE; residual need
            // below that is bought fractionally (contractor, agency or overtime) at the contract premium. A pool
            // flagged Fractional hires no employees at all.
            let hires = if p.Fractional then 0.0 else floor (needed + 0.25)
            let residual = max 0.0 (needed - hires)
            let added = hires + residual
            let rate = p.LoadedHourly * stress.WageFactor
            let addedCost = (hires + residual * (1.0 + p.ContractPremium)) * d.ProductiveHours * rate
            let decDemand = (decemberAccount + sponsorLevelHours * d.DecemberShare) * p.Share + extra / 12.0
            let monthly = (coreHours + added * q) / 12.0
            let peak = max 0.0 (decDemand - monthly) * rate * (1.0 + d.PeakPremium)
            { Pool = p.Name; Hours = hours; CoreHours = coreHours; AddedFte = added; Hires = hires; AddedCost = addedCost; PeakCost = peak })
    let addedPeople = pools |> List.sumBy (fun p -> p.Hires)
    let addedOps = pools |> List.filter (fun p -> p.Pool = "operations") |> List.sumBy (fun p -> p.Hires)
    let headcount = float (List.length d.People) + addedPeople
    let pairs = headcount * (headcount - 1.0) / 2.0
    let avgRate =
        match d.Pools with
        | [] -> 0.0
        | ps -> (ps |> List.averageBy (fun p -> p.LoadedHourly)) * stress.WageFactor
    let coordination = pairs * d.CoordinationHoursPerPairWeek * 48.0 * avgRate
    let corePersonnel = d.People |> List.sumBy (fun p -> p.LoadedCost) |> (*) stress.WageFactor
    let contracted = d.Contracted |> List.sumBy snd |> (*) stress.VendorFactor
    let nonPersonnel = d.NonPersonnel |> List.sumBy snd |> (*) stress.VendorFactor
    let perPerson = headcount * d.PerPersonOverhead
    let addedCost = pools |> List.sumBy (fun p -> p.AddedCost)
    let peakCost = pools |> List.sumBy (fun p -> p.PeakCost)
    let sponsorCosts = sponsors |> List.sumBy (fun s -> s.AnnualSponsorCost)
    let total = external + addedCost + peakCost + corePersonnel + contracted + nonPersonnel + perPerson + coordination + sponsorCosts + stress.ExtraordinaryCost
    let profit = revenue - total
    let contribution = revenue - external - addedCost - peakCost - sponsorCosts
    let feasible, note = controlCheck d addedOps
    let baseResult =
        { AverageAssets = assets
          Accounts = accounts
          Sponsors = n
          Revenue = revenue
          AssetFeeRevenue = assetFee
          MinimumFeeTopUp = topUp
          OtherRevenue = other
          ExternalVariableCost = external
          ServicingHours = servicingHours + integration + relationship
          CoreServicingHours = pools |> List.sumBy (fun p -> p.CoreHours)
          AddedServicingFte = pools |> List.sumBy (fun p -> p.AddedFte)
          AddedServicingCost = addedCost
          PeakCost = peakCost
          CorePersonnel = corePersonnel
          NonPersonnelFixed = contracted + nonPersonnel + perPerson + coordination
          StepFixed = 0.0
          SponsorCosts = sponsorCosts
          ExtraordinaryCost = stress.ExtraordinaryCost
          TotalCost = total
          OperatingProfit = profit
          OperatingMargin = (if revenue > 0.0 then profit / revenue else nan)
          ContributionMargin = (if revenue > 0.0 then contribution / revenue else nan) }
    { Base = baseResult
      Pools = pools
      Headcount = headcount
      ContractedFte = pools |> List.sumBy (fun p -> p.AddedFte - p.Hires)
      CoordinationCost = coordination
      ContractedCost = contracted
      PerPersonCost = perPerson
      IntegrationHours = integration
      HumanMinutesPerAccount = (if accounts > 0.0 then (servicingHours + integration + relationship) * 60.0 / accounts else 0.0)
      ControlFeasible = feasible
      ControlNote = note }

/// Fixed annual cost of a design with no sponsors (people, contracted, non-personnel, per-person, coordination,
/// and any pool minimums).
let fixedCost (d: Design) = (evaluateDesign d baseMarketMinutes (price 20.0) noStress []).Base.TotalCost

/// Smallest grid assets (first, sustained) at which a design reaches a margin target (see Analysis.assetsForMargin).
let assetsForMarginDesign (d: Design) (target: float) (price: Price) (stress: Stress) (shape: ServicingEconomics.Analysis.Shape) (margin: float) =
    ServicingEconomics.Analysis.assetsForMargin (fun ss -> (evaluateDesign d target price stress ss).Base) shape margin
