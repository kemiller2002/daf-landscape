/// Model 1: capital by Unbound state S1-S7, cash versus fully loaded, by cost category; minimum incremental cash to
/// commercialize a completed Unbound (to first referenceable invoice, and to self-sufficiency). Pure.
/// Inputs: data/model-inputs/capital-states.csv (agent AB's model-capital-states.csv, P3-ASM-AB001..AB029).
module CompetitiveAdvantageCreation.Capital

open CompetitiveAdvantageCreation.Domain
open CompetitiveAdvantageCreation.Cashflow

/// A cost line with a cash range and an economic (market-value) range.
type Line = { Cash: Range; Econ: Range; Ids: string list }

type StateInput =
    { StateId: string
      Name: string
      Sunk: Line
      Dev: Line
      Cac: Line
      Impl: Line
      ComplianceOnetime: Line
      Legal: Line
      WorkingCapital: Line
      PreRun: Line
      PreMonths: Range
      GoLiveMonths: Range
      Recurring: (string * Line) list
      FounderPre: Line
      FounderLive: Line }

type Globals =
    { Contingency: Range
      CapitalCharge: Range }

/// One category of the cost to first invoice, split into cash and non-cash.
type CategoryCost =
    { Category: string
      Cash: float
      NonCash: float }
    member x.FullyLoaded = x.Cash + x.NonCash

type FirstInvoice =
    { StateId: string
      Case: Case
      Months: float
      Categories: CategoryCost list }
    member x.Cash = x.Categories |> List.sumBy (fun c -> c.Cash)
    member x.NonCash = x.Categories |> List.sumBy (fun c -> c.NonCash)
    member x.FullyLoaded = x.Categories |> List.sumBy (fun c -> c.FullyLoaded)

let recurringCash (c: Case) (s: StateInput) = s.Recurring |> List.sumBy (fun (_, l) -> cost c l.Cash)

/// Revision 2 corrections to agent AB's first-invoice method. `asPublished` reproduces AB exactly.
type Corrections =
    { /// Added to the live run between go-live and first invoice (registry, Nacha TPSP obligations, control operations).
      ExtraLiveAnnual: float
      /// Added to the pre-contract run (control operations during the SOC 2 Type 2 observation).
      ExtraPreAnnual: float
      /// AB applied contingency to a subtotal that includes the founder's cash draw; Revision 2 excludes it so the
      /// contingency base is the same in every model (all Echelon cash cost except variable cost and founder draw).
      ContingencyOnFounder: bool
      /// Months of the period in which the founder's time is partly build work already inside development at market.
      DevOverlapMonths: float
      FounderBuildShare: float
      /// First-customer implementation and go-live lag replacing AB's values (REV3037, REV3039).
      Impl: float option
      GoLive: float option }

let asPublished = { ExtraLiveAnnual = 0.0; ExtraPreAnnual = 0.0; ContingencyOnFounder = true; DevOverlapMonths = 0.0; FounderBuildShare = 0.0; Impl = None; GoLive = None }

/// Incremental cost from a state to the first invoice of a referenceable paying customer (agent AB's definition:
/// one-time items, pre-contract run, live run between go-live and first invoice, founder cash draw, contingency;
/// economic adds development at market, founder time at market in place of the cash draw, and a capital charge on
/// half the cash deployed over the period), with the Revision 2 corrections applied when given.
let firstInvoice (g: Globals) (c: Case) (founderEcon: float) (k: Corrections) (s: StateInput) : FirstInvoice =
    let pre = cost c s.PreMonths
    let golive = defaultArg k.GoLive (cost c s.GoLiveMonths)
    let months = pre + golive
    let one (l: Line) = cost c l.Cash
    let impl = defaultArg k.Impl (one s.Impl)
    let devCash, devEcon = cost c s.Dev.Cash, cost c s.Dev.Econ
    let preRun = (cost c s.PreRun.Cash + k.ExtraPreAnnual) * pre / 12.0
    let liveRun = (recurringCash c s + k.ExtraLiveAnnual) * golive / 12.0
    let founderCash = cost c s.FounderPre.Cash * pre / 12.0 + cost c s.FounderLive.Cash * golive / 12.0
    let subtotal = devCash + one s.Cac + impl + one s.ComplianceOnetime + one s.Legal + one s.WorkingCapital + preRun + liveRun
    let contingency = cost c g.Contingency * (subtotal + (if k.ContingencyOnFounder then founderCash else 0.0))
    let cash = subtotal + founderCash + contingency
    let overlap = min months (max 0.0 k.DevOverlapMonths)
    let founderEconTotal = founderEcon * (months - overlap * k.FounderBuildShare) / 12.0
    let capitalCharge = cost c g.CapitalCharge * cash * months / 12.0 / 2.0
    { StateId = s.StateId
      Case = c
      Months = months
      Categories =
        [ { Category = "incremental development"; Cash = devCash; NonCash = devEcon - devCash }
          { Category = "customer acquisition"; Cash = one s.Cac; NonCash = 0.0 }
          { Category = "implementation"; Cash = impl; NonCash = 0.0 }
          { Category = "compliance (one-time)"; Cash = one s.ComplianceOnetime; NonCash = 0.0 }
          { Category = "legal and corporate (one-time)"; Cash = one s.Legal; NonCash = 0.0 }
          { Category = "working capital"; Cash = one s.WorkingCapital; NonCash = 0.0 }
          { Category = "pre-contract run"; Cash = preRun; NonCash = 0.0 }
          { Category = "live run to first invoice"; Cash = liveRun; NonCash = 0.0 }
          { Category = "founder compensation"; Cash = founderCash; NonCash = founderEconTotal - founderCash }
          { Category = "contingency"; Cash = contingency; NonCash = 0.0 }
          { Category = "economic opportunity cost (capital charge)"; Cash = 0.0; NonCash = capitalCharge } ] }

/// Revenue assumptions for the self-sufficiency run (Phase II ER-7 channel revenue, reused by AB as P3-ASM-AB030).
type Revenue =
    { RevenuePerCustomer: Range
      CustomersPerYear: Range
      Churn: Range
      VariableShare: Range
      ArrearsMonths: Range
      CacLater: Range
      ImplLater: Range }

/// The state's path to self-sufficiency as a cash-flow stream from month 0, on agent AB's assumptions (the
/// Revision 2 corrected path is the sequence model's A and A3). Working capital is produced by billing in
/// arrears in the engine, so AB's one-time working-capital line is not added again (no double count).
let toStream (c: Case) (g: Globals) (rev: Revenue) (founderFte: float) (extraLiveRunAnnual: float) (s: StateInput) : Stream =
    let pre = cost c s.PreMonths
    { Id = s.StateId
      Name = s.Name
      Entity = E2Unbound
      Dedicated = true
      KillExempt = false
      StartMonth = 0.0
      DevCash = cost c s.Dev.Cash
      DevEcon = cost c s.Dev.Econ
      DevMonths = max 1.0 (min pre 12.0)
      OnetimeCash = cost c s.ComplianceOnetime.Cash + cost c s.Legal.Cash
      OnetimeLeadMonths = 0.0
      PreRunMonthly = cost c s.PreRun.Cash / 12.0
      LiveRunMonthly = (recurringCash c s + extraLiveRunAnnual) / 12.0
      RegistryAnnualOf = (fun _ -> 0.0)
      RegistryTransferredOf = (fun _ -> 0.0)
      RegistryPreRevenue = false
      FounderFte = founderFte
      FounderBuildShare = 0.0
      FounderCashPreMonthly = cost c s.FounderPre.Cash / 12.0
      FounderCashLiveMonthly = cost c s.FounderLive.Cash / 12.0
      FirstSigningMonth = pre
      CustomersPerYear = gain c rev.CustomersPerYear
      MaxCustomers = infinity
      RevenuePerCustomer = gain c rev.RevenuePerCustomer
      Recurring = true
      PartnerShare = 0.0
      VariableShare = cost c rev.VariableShare
      VarPerCustomerYear = 0.0
      CacFirst = cost c s.Cac.Cash
      CacLater = cost c rev.CacLater
      ImplFirst = cost c s.Impl.Cash
      ImplLater = cost c rev.ImplLater
      ImplFirstCount = 1.0
      ImplRecovery = 0.0
      SponsorConversionPerCustomer = 0.0
      IncidentReserve = 0.0
      WindDownFixed = 0.0
      WindDownRunMonths = 0.0
      Churn = cost c rev.Churn
      GoLiveLag = cost c s.GoLiveMonths
      ArrearsMonths = cost c rev.ArrearsMonths
      Contingency = cost c g.Contingency
      Basis = revision2Basis }
