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

/// An account archetype: a slice of a sponsor's book with its own balance and workload.
type Archetype =
    { Name: string
      ShareOfAccounts: float
      AverageBalance: float
      GrantsPerYear: float
      ContributionsPerYear: float
      ContactsPerYear: float
      ComplexAssetsPerYear: float }

/// Unit of an activity's volume.
type Driver =
    | PerAccountYear
    | PerGrant
    | PerContribution
    | PerContact
    | PerComplexAsset
    | PerNewAccount
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
      ServicingHourlyLoaded: float
      DecemberShare: float
      PeakPremium: float }

/// Pricing offered to a sponsor.
type Price =
    { Bps: float
      MinimumAnnualFee: float
      ImplementationFeePerSponsor: float
      ExceptionalFeesPerAccountYear: float }

/// A sponsor book of business under administration.
type Sponsor =
    { Name: string
      Accounts: float
      Mix: Archetype list
      ComplexityMultiplier: float
      NewAccountRate: float
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
