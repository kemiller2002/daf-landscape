/// Typed zero-based model inputs and pure parsers. Reuses the baseline CSV reader and Range/Level types.
module ZeroBased.Domain

open CompetitiveDisplacement.Csv
open CompetitiveDisplacement.Inputs

/// What an activity's frequency is counted against.
type Driver =
    | PerAccount
    | PerNewAccount
    | PerContribution
    | PerGrant
    | PerSponsor
    | PerSponsorOnboarding
    | PerPlatform
    | PerActiveCharity

let parseDriver (s: string) : Result<Driver, string> =
    match s.Trim().ToLowerInvariant() with
    | "per_account" -> Ok PerAccount
    | "per_new_account" -> Ok PerNewAccount
    | "per_contribution" -> Ok PerContribution
    | "per_grant" -> Ok PerGrant
    | "per_sponsor" -> Ok PerSponsor
    | "per_sponsor_onboarding" -> Ok PerSponsorOnboarding
    | "per_platform" | "per_month" | "per_year" -> Ok PerPlatform
    | "per_active_charity" -> Ok PerActiveCharity
    | other -> Error $"unknown driver '{other}'"

/// Who bears an activity's labour under an operating configuration (see configurations.csv).
type Bucket =
    | Tech
    | Commercial
    | Support
    | AdminException
    | AdminJudgment
    | IndependentAuth
    | SponsorOwned
    | External
    | Shared
    | Eliminated

type Activity =
    { Id: string
      Domain: string
      Name: string
      Driver: Driver
      Freq: Range
      Seasonality: string
      Requirements: string list
      Responsible: string
      Classification: string
      Role: string
      Exception: Range
      Minutes: Range
      Independent: bool
      SlaHours: float
      ExternalCost: float
      LegallyRequired: string
      EvidenceClass: string
      Confidence: string }

/// Classification first, then responsible entity, then domain/role decide the bucket.
let bucket (a: Activity) : Bucket =
    match a.Classification, a.Responsible, a.Role with
    | ("ELIMINATED" | "PREVENTED"), _, _ when a.Exception.Base <= 0.0 -> Eliminated
    | "SPONSOR-OWNED", _, _ | _, ("sponsor" | "donor"), _ | _, _, "sponsor" -> SponsorOwned
    | "EXTERNAL-PROVIDER", _, _ | _, ("custodian" | "bank_or_payment_provider" | "external_professional"), _ -> External
    | ("SHARED-ECHELON", _, "engineering") | (_, "shared_echelon", "engineering") -> Tech
    | ("SHARED-ECHELON", _, ("implementation" | "sales" | "executive")) | (_, "shared_echelon", ("implementation" | "sales" | "executive")) -> Commercial
    | "SHARED-ECHELON", _, _ | _, "shared_echelon", _ -> Shared
    | "INDEPENDENT-AUTHORIZATION", _, _ -> IndependentAuth
    | _, _, "engineering" -> Tech
    | _ when a.Domain = "TECHOPS" -> Tech
    | _, _, ("sales" | "executive") -> Commercial
    | _ when a.Domain = "COMMERCIAL" -> Commercial
    | _, _, "support" -> Support
    | "HUMAN-JUDGMENT", _, _ -> AdminJudgment
    | _ -> AdminException

let private numOr (dflt: float) key row =
    match num key row with
    | Ok x -> x
    | Error _ -> dflt

let private rng prefix row =
    match num (prefix + "_low") row, num (prefix + "_base") row, num (prefix + "_high") row with
    | Ok l, Ok b, Ok h -> Ok { Low = l; Base = b; High = h }
    | Error e, _, _ | _, Error e, _ | _, _, Error e -> Error e

let private str key row = get key row |> Result.defaultValue ""

let private splitIds (s: string) =
    s.Split([| '|'; ';' |], System.StringSplitOptions.RemoveEmptyEntries ||| System.StringSplitOptions.TrimEntries)
    |> List.ofArray

let parseActivity (row: Row) : Result<Activity, string> =
    let id = str "activity_id" row
    match parseDriver (str "driver" row), rng "freq" row, rng "exception" row, rng "minutes" row with
    | Ok d, Ok f, Ok e, Ok m ->
        Ok
            { Id = id
              Domain = (str "domain" row).Trim().ToUpperInvariant()
              Name = str "activity" row
              Driver = d
              Freq = f
              Seasonality = (str "seasonality" row).Trim().ToLowerInvariant()
              Requirements = splitIds (str "unbound_requirements" row)
              Responsible = (str "responsible_entity" row).Trim().ToLowerInvariant()
              Classification = (str "classification" row).Trim().ToUpperInvariant()
              Role = (str "human_role" row).Trim().ToLowerInvariant()
              Exception = e
              Minutes = m
              Independent = (str "independent_authorization" row).Trim().ToUpperInvariant() = "Y"
              SlaHours = numOr 72.0 "sla_hours" row
              ExternalCost = numOr 0.0 "external_cost_per_event" row
              LegallyRequired = str "legally_required" row
              EvidenceClass = str "evidence_class" row
              Confidence = str "confidence" row }
    | Error e, _, _, _ | _, Error e, _, _ | _, _, Error e, _ | _, _, _, Error e -> Error $"{id}: {e}"

/// Assumption-schema rows (id,key,definition,unit,low,base,high,...) keyed by `key`.
let parseAssumptions (rows: Row list) : Result<Params, string list> =
    rows
    |> List.map (fun r ->
        match get "key" r with
        | Ok k when k.Trim() = "" -> Error "empty key"
        | Ok k ->
            match num "low" r, num "base" r, num "high" r with
            | Ok l, Ok b, Ok h -> Ok(k.Trim(), { Low = l; Base = b; High = h })
            | _ -> Error $"{k}: low/base/high not numeric"
        | Error e -> Error e)
    |> collect
    |> Result.map Map.ofList

/// A role's cost and coverage rules (roles.csv).
type Role =
    { Id: string
      Name: string
      Pool: string
      DedicatedCost: Range
      FractionalRate: Range
      MinFraction: float
      DedicateThreshold: float
      IndependenceGroup: string }

let parseRole (row: Row) : Result<Role, string> =
    let id = str "role_id" row
    match rng "dedicated_cost" row, rng "fractional_rate" row with
    | Ok d, Ok f ->
        Ok
            { Id = id
              Name = str "name" row
              Pool = str "pool" row
              DedicatedCost = d
              FractionalRate = f
              MinFraction = numOr 0.0 "min_fraction_fte" row
              DedicateThreshold = numOr 0.6 "dedicate_threshold_fte" row
              IndependenceGroup = str "independence_group" row }
    | Error e, _ | _, Error e -> Error $"{id}: {e}"

/// Vendor share of each bucket's labour under an operating configuration.
type Config =
    { Id: string
      Name: string
      Shares: Map<Bucket, float>
      VendorRunsControls: bool
      Standalone: bool
      ChannelShare: float }

let bucketColumns =
    [ Tech, "tech"; Commercial, "commercial"; Support, "support"; AdminException, "admin_exception"
      AdminJudgment, "admin_judgment"; IndependentAuth, "independent_auth"; SponsorOwned, "sponsor_owned"
      External, "external"; Shared, "shared"; Eliminated, "eliminated" ]

let parseConfig (row: Row) : Result<Config, string> =
    let id = str "config_id" row
    let shares = bucketColumns |> List.map (fun (b, c) -> b, numOr 0.0 c row) |> Map.ofList
    Ok
        { Id = id
          Name = str "name" row
          Shares = shares
          VendorRunsControls = (str "vendor_runs_controls" row).Trim().ToUpperInvariant() = "Y"
          Standalone = (str "standalone" row).Trim().ToUpperInvariant() = "Y"
          ChannelShare = numOr 0.0 "channel_share" row }

/// A fixed (non-workload) cost line with an activation rule and an economic view.
type FixedCost =
    { Id: string
      Item: string
      Category: string
      Annual: Range
      Activation: string
      View: string
      AllocationShare: float
      OneTime: bool }

let parseFixed (row: Row) : Result<FixedCost, string> =
    let id = str "fc_id" row
    match rng "annual" row with
    | Ok a ->
        Ok
            { Id = id
              Item = str "item" row
              Category = str "category" row
              Annual = a
              Activation = str "activation" row
              View = (str "view" row).Trim().ToLowerInvariant()
              AllocationShare = numOr 1.0 "allocation_share" row
              OneTime = (str "one_time" row).Trim().ToUpperInvariant() = "Y" }
    | Error e -> Error $"{id}: {e}"

/// An account-balance tier inside a programme (balance and activity relative to the programme mean).
type Tier = { Name: string; Share: float; BalanceRel: float; ActivityRel: float }

/// A giving programme profile: activity per account and a heterogeneous tier mix.
type Programme =
    { Id: string
      Name: string
      GrantsPerAcct: float
      ContribPerAcct: float
      NewAcctRate: float
      Tiers: Tier list
      DefaultBalance: float }

/// tiers field: name:share:balance_rel:activity_rel|...
let parseTiers (s: string) : Result<Tier list, string> =
    s.Split('|', System.StringSplitOptions.RemoveEmptyEntries)
    |> List.ofArray
    |> List.map (fun t ->
        match t.Split(':') with
        | [| n; sh; b; a |] ->
            let p (x: string) = System.Double.Parse(x, System.Globalization.CultureInfo.InvariantCulture)
            Ok { Name = n.Trim(); Share = p sh; BalanceRel = p b; ActivityRel = p a }
        | _ -> Error $"bad tier '{t}'")
    |> collect
    |> Result.mapError (String.concat "; ")

let parseProgramme (row: Row) : Result<Programme, string> =
    let id = str "programme_id" row
    match parseTiers (str "tiers" row), num "grants_per_acct" row, num "contrib_per_acct" row, num "new_acct_rate" row, num "default_balance" row with
    | Ok t, Ok g, Ok c, Ok n, Ok b ->
        Ok { Id = id; Name = str "name" row; GrantsPerAcct = g; ContribPerAcct = c; NewAcctRate = n; Tiers = t; DefaultBalance = b }
    | Error e, _, _, _, _ -> Error $"{id}: {e}"
    | _, Error e, _, _, _ | _, _, Error e, _, _ | _, _, _, Error e, _ | _, _, _, _, Error e -> Error $"{id}: {e}"

type Inputs =
    { Activities: Activity list
      Params: Params
      Roles: Role list
      Configs: Config list
      Fixed: FixedCost list
      Programmes: Programme list
      Infra: Params
      Beneficium: Params }
