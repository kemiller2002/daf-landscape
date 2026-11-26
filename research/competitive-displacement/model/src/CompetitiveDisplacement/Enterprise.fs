/// Enterprise-level economics per operating mode: variable cost per account, sponsor-level cost,
/// vendor/sponsor split and break-even assets.
module CompetitiveDisplacement.Enterprise

open CompetitiveDisplacement.Inputs
open CompetitiveDisplacement.Events

type ModeEconomics =
    { Mode: Mode
      /// Vendor-borne variable cost per account-year (event cost x vendor share + infrastructure or licensed software).
      VendorVariablePerAcct: float
      /// Whole-system variable cost per account-year: vendor + sponsor-borne event labour + reserved decisions + pass-through rails.
      SystemVariablePerAcct: float
      HumanMinutesPerAcct: float
      VendorSponsorLevelCost: float
      SystemSponsorLevelCost: float
      VendorFixed: float
      Build: float
      OnetimePerSponsor: float
      OnetimePerAcct: float
      Events: EventCost list }

let economicsWith (choose: Range -> float) (vals: Values) (events: EventDef list) (mode: Mode) : ModeEconomics =
    let cs = costs mode vals events
    let eventPerAcct = cs |> List.sumBy perAccount
    let share = mode.VendorEventShare
    let infra = if mode.OwnsPlatform then v vals "infra_per_account_owned" else v vals "software_per_account_licensed"
    let reserved = v vals "sponsor_reserved_min_per_account" / 60.0 * v vals "rate_ops"
    let pass = cs |> List.sumBy (fun c -> c.PassThroughPerAcct)
    let sponsorLevel = cs |> List.sumBy (fun c -> c.SponsorLevelCost)
    { Mode = mode
      VendorVariablePerAcct = eventPerAcct * share + infra
      SystemVariablePerAcct = eventPerAcct + infra + reserved + pass
      HumanMinutesPerAcct = cs |> List.sumBy (fun c -> c.HumanMinutesPerAcct)
      VendorSponsorLevelCost = sponsorLevel * share
      SystemSponsorLevelCost = sponsorLevel
      VendorFixed = choose mode.Fixed
      Build = choose mode.Build
      OnetimePerSponsor = cs |> List.sumBy (fun c -> c.OnetimeCost)
      OnetimePerAcct = cs |> List.sumBy (fun c -> c.OnetimePerAcctCost)
      Events = cs }

let economics (level: Level) vals events mode = economicsWith (pick level) vals events mode

/// Break-even average billable assets for the vendor: A = (F + n*S) / (r - v/B). None when the
/// fee never covers variable cost at that balance.
let breakEvenAssets (bps: float) (balance: float) (sponsors: float) (m: ModeEconomics) : float option =
    let r = bps / 10000.0
    let margin = r - m.VendorVariablePerAcct / balance
    if margin <= 0.0 then None
    else Some((m.VendorFixed + sponsors * m.VendorSponsorLevelCost) / margin)

/// Fee (bps) at which the vendor breaks even at given assets.
let breakEvenBps (assets: float) (balance: float) (sponsors: float) (m: ModeEconomics) : float =
    let accounts = assets / balance
    (m.VendorFixed + sponsors * m.VendorSponsorLevelCost + accounts * m.VendorVariablePerAcct) / assets * 10000.0

/// Whole-system cost per account-year at a given number of accounts across n sponsors (vendor fixed spread).
let systemCostPerAccount (accounts: float) (sponsors: float) (m: ModeEconomics) : float =
    m.SystemVariablePerAcct + (m.VendorFixed + sponsors * m.SystemSponsorLevelCost) / accounts
