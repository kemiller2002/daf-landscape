/// Operating scenario and the annual driver counts it implies. Pure.
module ZeroBased.Volume

open ZeroBased.Domain

type Values = Map<string, float>

let v (vals: Values) key =
    match Map.tryFind key vals with
    | Some x -> x
    | None -> failwithf "parameter '%s' missing" key

/// One operating scenario: accounts, sponsors, programme and mean balance.
type Scenario =
    { Id: string
      Accounts: float
      Sponsors: float
      NewSponsorsPerYear: float
      MeanBalance: float
      Programme: Programme
      ActivityMult: float }

/// Normalise tier balances so the account-weighted mean equals the scenario mean balance.
let tierBalances (s: Scenario) : (Tier * float) list =
    let relMean = s.Programme.Tiers |> List.sumBy (fun t -> t.Share * t.BalanceRel)
    s.Programme.Tiers |> List.map (fun t -> t, s.MeanBalance * t.BalanceRel / relMean)

let assets (s: Scenario) = s.Accounts * s.MeanBalance

/// Account-weighted activity multiplier from the tier mix (dormant tiers pull it down).
let activityFactor (s: Scenario) =
    (s.Programme.Tiers |> List.sumBy (fun t -> t.Share * t.ActivityRel)) * s.ActivityMult

type Counts =
    { Accounts: float
      NewAccounts: float
      Contributions: float
      Grants: float
      Sponsors: float
      NewSponsors: float
      ActiveCharities: float }

/// Unique recipient charities: concave in grants (heavy overlap among large recipients), capped by the
/// population of grant-eligible organisations. Parameters are ASSUMPTION (see parameters.csv).
let activeCharities (vals: Values) (grants: float) =
    if grants <= 0.0 then 0.0
    else
        let g0 = v vals "recipients_ref_grants"
        let r0 = v vals "recipients_ref_charities"
        let e = v vals "recipients_exponent"
        min (v vals "recipients_cap") (r0 * (grants / g0) ** e)

let counts (vals: Values) (s: Scenario) : Counts =
    let af = activityFactor s
    let grants = s.Accounts * s.Programme.GrantsPerAcct * af
    { Accounts = s.Accounts
      NewAccounts = s.Accounts * s.Programme.NewAcctRate
      Contributions = s.Accounts * s.Programme.ContribPerAcct * af
      Grants = grants
      Sponsors = s.Sponsors
      NewSponsors = s.NewSponsorsPerYear
      ActiveCharities = activeCharities vals grants }

/// Annual driver units for an activity's driver.
let driverUnits (c: Counts) (d: Driver) : float =
    match d with
    | PerAccount -> c.Accounts
    | PerNewAccount -> c.NewAccounts
    | PerContribution -> c.Contributions
    | PerGrant -> c.Grants
    | PerSponsor -> c.Sponsors
    | PerSponsorOnboarding -> c.NewSponsors
    | PerPlatform -> 1.0
    | PerActiveCharity -> c.ActiveCharities
