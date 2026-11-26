/// Domain types for the DAF servicing economics research model.
/// Research tool only: theoretical scenarios from labelled assumptions, not forecasts or product code.
module ServicingEconomics.Domain

/// Evidence label carried by every parameter: S sourced, A assumption, D derived, E estimate.
type Basis =
    | Sourced of string
    | Assumption of string
    | Derived of string
    | Estimate of string

/// A labelled number.
type Param = { Value: float; Basis: Basis }

/// How much of an activity's human handling a servicer redesign removes.
type Approach =
    | Conventional
    | AiEnhanced
    | AiNative
    | AiNativeWithElimination

/// An account archetype: a slice of a sponsor's book with its own balance and workload.
/// Workload is per account-year by approach: servicer human minutes, external vendor cost
/// (excluding payment rails) and payment-rail cost (which a contract may pass through at cost).
type Archetype =
    { Name: string
      ShareOfAccounts: float
      AverageBalance: float
      Minutes: Approach -> float
      External: Approach -> float
      Payments: Approach -> float
      DecemberShare: float }

/// Unit of an activity's volume.
type Driver =
    | PerAccountYear
    | PerSponsorYear

/// A recurring servicing activity. Minutes are human handling time per occurrence by approach,
/// already including the expected share of exceptions; external cost is per occurrence.
type Activity =
    { Id: string
      Name: string
      Driver: Driver
      Minutes: Approach -> float
      ExternalCost: float
      PassThrough: bool }

/// A core role on the fixed payroll. ServicingShare is the fraction of productive hours
/// available for variable servicing work (the rest is management, engineering, sales, control).
type Role =
    { Title: string
      LoadedCost: float
      CashCost: float
      ServicingShare: float
      StartMonth: int }

/// A step-fixed cost: Cost per unit for each started block of Size driver units beyond Free units.
type StepDriver =
    | Sponsors
    | Accounts
    | AssetsUsd
    | ServicingFte

type StepRule =
    { Name: string
      On: StepDriver
      Free: float
      Size: float
      CostPerStep: float }

type Organization =
    { Name: string
      Core: Role list
      NonPersonnelFixed: (string * float) list
      StepRules: StepRule list
      ProductiveHours: float
      /// Share of productive hours usable for queue work (the rest is handoffs, training, idle between items).
      Utilisation: float
      /// Added operations staff required for separation of duties regardless of workload.
      MinimumAddedServicingFte: float
      ServicingHourlyLoaded: float
      DecemberShare: float
      PeakPremium: float }

/// Pricing offered to a sponsor.
type Price =
    { Bps: float
      MinimumAnnualFee: float
      ImplementationFeePerSponsor: float
      ExceptionalFeesPerAccountYear: float
      /// Per-account annual floor: each account pays the greater of its asset fee and this amount.
      PerAccountMinimum: float
      /// Buyer reference price as an average per account; 0 = none. A sponsor's asset fee is capped at accounts x this
      /// amount (e.g. Ren's $737 per account-year at MS GIFT).
      PerAccountMaximum: float
      /// Flat per-account annual fee added to the asset fee (hybrid pricing).
      PerAccountFee: float
      /// Payment-rail costs billed to the sponsor at cost (excluded from both revenue and cost).
      PaymentsPassThrough: bool }

/// A sponsor book of business under administration.
type Sponsor =
    { Name: string
      Accounts: float
      Mix: Archetype list
      ComplexityMultiplier: float
      AnnualSponsorCost: float
      OnboardingCost: float }

/// Adverse or alternative conditions applied to a base case.
type Stress =
    { Name: string
      AssetFactor: float
      AccountFactor: float
      MinutesFactor: float
      VolumeFactor: float
      WageFactor: float
      VendorFactor: float
      ExtraordinaryCost: float
      DropLargestSponsor: bool }

let noStress =
    { Name = "base"
      AssetFactor = 1.0
      AccountFactor = 1.0
      MinutesFactor = 1.0
      VolumeFactor = 1.0
      WageFactor = 1.0
      VendorFactor = 1.0
      ExtraordinaryCost = 0.0
      DropLargestSponsor = false }

/// Annual result for a portfolio.
type Result =
    { AverageAssets: float
      Accounts: float
      Sponsors: int
      Revenue: float
      AssetFeeRevenue: float
      MinimumFeeTopUp: float
      OtherRevenue: float
      ExternalVariableCost: float
      ServicingHours: float
      CoreServicingHours: float
      AddedServicingFte: float
      AddedServicingCost: float
      PeakCost: float
      CorePersonnel: float
      NonPersonnelFixed: float
      StepFixed: float
      SponsorCosts: float
      ExtraordinaryCost: float
      TotalCost: float
      OperatingProfit: float
      OperatingMargin: float
      ContributionMargin: float }
