/// Domain types for the zero-based operating-economics model. Pure; no I/O.
module ZeroBasedEconomics.Domain

open System

type Level =
    | Low
    | Base
    | High

let levelCode l =
    match l with
    | Low -> "low"
    | Base -> "base"
    | High -> "high"

let levels = [ Low; Base; High ]

type Range = { Low: float; Base: float; High: float }

let pick (level: Level) (r: Range) =
    match level with
    | Low -> r.Low
    | Base -> r.Base
    | High -> r.High

let point (x: float) = { Low = x; Base = x; High = x }

/// The six commercial models modelled independently (mission 3).
type ModelId =
    | L // technology licensing
    | W // white-label platform licensing
    | T // technology plus limited operational support
    | F // full-service administration
    | C // shared charity intelligence
    | M // migration and onboarding services

let allModels = [ L; W; T; F; C; M ]

let modelCode m =
    match m with
    | L -> "L"
    | W -> "W"
    | T -> "T"
    | F -> "F"
    | C -> "C"
    | M -> "M"

let modelName m =
    match m with
    | L -> "Technology licensing"
    | W -> "White-label platform licensing"
    | T -> "Technology plus limited operational support"
    | F -> "Full-service administration"
    | C -> "Shared charity intelligence"
    | M -> "Migration and onboarding services"

let parseModel (s: string) =
    match s.Trim() with
    | "L" -> Ok L
    | "W" -> Ok W
    | "T" -> Ok T
    | "F" -> Ok F
    | "C" -> Ok C
    | "M" -> Ok M
    | x -> Error $"unknown model '{x}'"

/// Expense classes required by the mission. FounderLabor and FullyLoaded are produced by the engine for labour and
/// aggregates; the register may still carry them explicitly.
type Classification =
    | Unavoidable
    | Conditional
    | VolumeTriggered
    | Shared
    | FounderLabor
    | FullyLoaded
    | Discretionary

let classCode c =
    match c with
    | Unavoidable -> "unavoidable-cash"
    | Conditional -> "conditional-cash"
    | VolumeTriggered -> "volume-triggered"
    | Shared -> "shared-infrastructure"
    | FounderLabor -> "noncash-founder-labor"
    | FullyLoaded -> "fully-loaded-economic"
    | Discretionary -> "discretionary"

let parseClass (s: string) =
    [ Unavoidable; Conditional; VolumeTriggered; Shared; FounderLabor; FullyLoaded; Discretionary ]
    |> List.tryFind (fun c -> classCode c = s.Trim())
    |> function
        | Some c -> Ok c
        | None -> Error $"unknown classification '{s}'"

/// Why an expense exists. Mandatory obligations (tier 0) are separated from customer-specific contractual
/// expectations (tiers 1-2) and from discretionary spend (tier 3).
type Obligation =
    | Legal
    | Operational
    | ContractTypical
    | ContractDemanding
    | Optional

let obligationCode o =
    match o with
    | Legal -> "legal"
    | Operational -> "operational-mandatory"
    | ContractTypical -> "contract-typical"
    | ContractDemanding -> "contract-demanding"
    | Optional -> "discretionary"

let parseObligation (s: string) =
    [ Legal; Operational; ContractTypical; ContractDemanding; Optional ]
    |> List.tryFind (fun o -> obligationCode o = s.Trim())
    |> function
        | Some o -> Ok o
        | None -> Error $"unknown obligation '{s}'"

/// Contract tier at which an obligation applies: 0 mandatory, 1 typical institutional contract, 2 demanding
/// (bank-grade) contract, 3 discretionary (never included in a scenario's minimum configuration).
let tierOf o =
    match o with
    | Legal
    | Operational -> 0
    | ContractTypical -> 1
    | ContractDemanding -> 2
    | Optional -> 3

type Metric =
    | Always
    | Customers
    | Accounts
    | AuaM
    | Transactions
    | Exceptions
    | NewCustomers

let metricCode m =
    match m with
    | Always -> "always"
    | Customers -> "customers"
    | Accounts -> "accounts"
    | AuaM -> "aua_musd"
    | Transactions -> "transactions"
    | Exceptions -> "exceptions"
    | NewCustomers -> "new_customers"

let parseMetric (s: string) =
    [ Always; Customers; Accounts; AuaM; Transactions; Exceptions; NewCustomers ]
    |> List.tryFind (fun m -> metricCode m = s.Trim())
    |> function
        | Some m -> Ok m
        | None -> Error $"unknown metric '{s}'"

/// How an expense scales once triggered. Amounts are annual USD per unit.
type Driver =
    | Fixed
    | Per of Metric
    /// Capacity-limited step: one unit per `capacity` of the metric (at least one once triggered).
    | Step of Metric * float

type Expense =
    { Id: string
      Name: string
      Purpose: string
      Category: string
      Class: Classification
      Obligation: Obligation
      /// Accountable economic entity (E1 Echelon Foundry, E3 sponsor programme, E4 servicing organization, E5 shared).
      Entity: string
      EvidenceIds: string list
      TriggerMetric: Metric
      TriggerThreshold: float
      Driver: Driver
      MinAnnual: Range
      Amount: Range
      /// Share of the amount that is new cash for the DAF business (the rest already exists in Echelon Foundry).
      IncrementalShare: Range
      /// Share of the amount allocated to the DAF business in the fully loaded view.
      AllocationShare: Range
      CapacityLimit: string
      Alternative: string
      Consequence: string
      /// Paid annually in advance (affects working capital and pre-revenue capital).
      Prepaid: bool
      /// Models in which Echelon Foundry bears the cost.
      EfModels: Set<ModelId>
      /// Models in which the sponsor bears the cost instead (reported separately, never in EF cost).
      SponsorModels: Set<ModelId> }

type ActDriver =
    | PerGrant
    | PerContribution
    | PerTransaction
    | PerAccount
    | PerException
    | PerGrantException
    | PerContributionException
    | PerTransactionException
    | PerCustomer
    | PerNewCustomer
    | FixedYear

let actDriverCode d =
    match d with
    | PerGrant -> "per_grant"
    | PerContribution -> "per_contribution"
    | PerTransaction -> "per_transaction"
    | PerAccount -> "per_account"
    | PerException -> "per_exception"
    | PerGrantException -> "per_grant_exception"
    | PerContributionException -> "per_contribution_exception"
    | PerTransactionException -> "per_transaction_exception"
    | PerCustomer -> "per_customer"
    | PerNewCustomer -> "per_new_customer"
    | FixedYear -> "fixed_year"

let parseActDriver (s: string) =
    [ PerGrant; PerContribution; PerTransaction; PerAccount; PerException; PerGrantException; PerContributionException; PerTransactionException; PerCustomer; PerNewCustomer; FixedYear ]
    |> List.tryFind (fun d -> actDriverCode d = s.Trim())
    |> function
        | Some d -> Ok d
        | None -> Error $"unknown activity driver '{s}'"

/// A human activity with the ten challenge answers (mission 2, "challenge human intervention").
type Activity =
    { Id: string
      Name: string
      Why: string
      LegallyRequired: string
      ContractuallyRequired: string
      Preventable: string
      Deterministic: string
      AiAssist: string
      HumanDecision: string
      Driver: ActDriver
      /// Occurrences per driver unit per year (or per year for fixed_year).
      Rate: Range
      /// Share of occurrences that still need a human after prevention, deterministic software and AI assistance.
      HumanShare: Range
      /// Minutes per human-handled occurrence.
      Minutes: Range
      /// Minutes per occurrence in a conventional administrator (for comparison only; never drives cost).
      ConventionalMinutes: float
      Role: string
      EfModels: Set<ModelId>
      SponsorModels: Set<ModelId>
      EvidenceIds: string list
      StaffingNote: string
      /// The activity exists only once at least this many customers are served (0 = also with no customers).
      MinCustomers: int }

type Role =
    { Id: string
      Name: string
      Purpose: string
      EvidenceIds: string list
      LoadedAnnual: Range
      ContractHourly: Range
      FounderEligible: bool
      ProductiveHours: float
      /// Residual hours above which an employee is cheaper and more reliable than contracting.
      HireThresholdHours: float
      Qualification: string
      Alternative: string
      Consequence: string }

/// Minimum distinct qualified people required regardless of workload (coverage, segregation of duties).
type Coverage =
    { Id: string
      Description: string
      Basis: string
      Obligation: Obligation
      Models: Set<ModelId>
      TriggerCustomers: int
      MinPeople: int
      Role: string
      AltAllowed: bool
      AltDescription: string
      AltAnnual: Range
      EvidenceIds: string list }

type Profile =
    { Id: string
      Name: string
      Accounts: Range
      AuaPerAccount: Range
      GrantsPerAccount: Range
      ContribsPerAccount: Range
      /// Exception intensity relative to the design's base touch rates (1.0 = base). Scales every exception-driven
      /// activity, independently of transaction volume.
      ExceptionRate: Range
      EvidenceIds: string list }

type Mix = { Id: string; Name: string; Pattern: string list }

/// Independent volume factors (mission 2: vary accounts, assets, transactions and exceptions independently).
type Factors = { Acct: Level; Aua: Level; Txn: Level; Exc: Level }

let baseFactors = { Acct = Base; Aua = Base; Txn = Base; Exc = Base }

let factorCode f = $"{levelCode f.Acct}/{levelCode f.Aua}/{levelCode f.Txn}/{levelCode f.Exc}"

let allFactors =
    [ for a in levels do
          for u in levels do
              for t in levels do
                  for e in levels do
                      yield { Acct = a; Aua = u; Txn = t; Exc = e } ]

type Scenario = { Customers: int; MixId: string; Factors: Factors; Tier: int }

type CustomerVolume =
    { ProfileId: string
      Accounts: float
      AuaUsd: float
      Grants: float
      Contribs: float
      Exceptions: float }

type Volume =
    { Customers: int
      PerCustomer: CustomerVolume list
      Accounts: float
      AuaM: float
      Grants: float
      Contribs: float
      Transactions: float
      Exceptions: float
      /// Customers onboarded this year (steady-state growth assumption; equals customers in the first year).
      NewCustomers: float }

type PriorEstimate =
    { Id: string
      Name: string
      Value: string
      Source: string
      OriginalAssumptions: string
      EvidenceQuality: string
      Obligations: string
      ConventionalAssumptions: string
      Replacements: string
      ComparableMetric: string
      Uncertainty: string }

type Source = { Id: string; Title: string; Location: string; EvidenceClass: string }

let isBlank (s: string) = String.IsNullOrWhiteSpace s
