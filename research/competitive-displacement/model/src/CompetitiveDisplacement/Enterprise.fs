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
      Cac: float
      AmortYears: float
      Events: EventCost list }

let economicsWith (choose: Range -> float) (vals: Values) (events: EventDef list) (mode: Mode) : ModeEconomics =
    let cs = costs mode vals events
    let eventPerAcct = cs |> List.sumBy perAccount
    let labour = cs |> List.sumBy (fun c -> c.LabourPerAcct)
    let ai = cs |> List.sumBy (fun c -> c.AiPerAcct)
    let share = mode.VendorEventShare
    // REV2 (CHL architect): in licensing modes the vendor runs the AI compute and sponsor staff are less efficient
    let sponsorPenalty = labour * (1.0 - share) * (v vals "sponsor_efficiency_multiplier" - 1.0)
    let vendorAi = ai * (1.0 - share)
    let infra = if mode.OwnsPlatform then v vals "infra_per_account_owned" else v vals "software_per_account_licensed"
    let reserved = v vals "sponsor_reserved_min_per_account" / 60.0 * v vals "rate_ops"
    let pass = cs |> List.sumBy (fun c -> c.PassThroughPerAcct)
    let sponsorLevel = cs |> List.sumBy (fun c -> c.SponsorLevelCost)
    { Mode = mode
      VendorVariablePerAcct = eventPerAcct * share + vendorAi + infra
      SystemVariablePerAcct = eventPerAcct + sponsorPenalty + infra + reserved + pass
      HumanMinutesPerAcct = cs |> List.sumBy (fun c -> c.HumanMinutesPerAcct)
      VendorSponsorLevelCost = sponsorLevel * share
      SystemSponsorLevelCost = sponsorLevel
      VendorFixed = choose mode.Fixed * v vals "fixed_cost_mult"
      Build = choose mode.Build
      Cac = v vals "cac_per_sponsor"
      AmortYears = v vals "amortisation_years"
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

/// Fully loaded break-even (REV2, CHL CFO): adds build, CAC and onboarding amortised over the amortisation period.
/// Onboarding scales with accounts (per-account migration) and sponsors (fixed onboarding).
let breakEvenAssetsLoaded (bps: float) (balance: float) (sponsors: float) (m: ModeEconomics) : float option =
    let r = bps / 10000.0
    let years = m.AmortYears
    let margin = r - (m.VendorVariablePerAcct + m.OnetimePerAcct / years) / balance
    if margin <= 0.0 then None
    else Some((m.VendorFixed + sponsors * m.VendorSponsorLevelCost + m.Build / years + sponsors * (m.Cac + m.OnetimePerSponsor) / years) / margin)

/// Fee (bps) at which the vendor breaks even at given assets.
let breakEvenBps (assets: float) (balance: float) (sponsors: float) (m: ModeEconomics) : float =
    let accounts = assets / balance
    (m.VendorFixed + sponsors * m.VendorSponsorLevelCost + accounts * m.VendorVariablePerAcct) / assets * 10000.0

/// Whole-system cost per account-year at a given number of accounts across n sponsors (vendor fixed spread).
let systemCostPerAccount (accounts: float) (sponsors: float) (m: ModeEconomics) : float =
    m.SystemVariablePerAcct + (m.VendorFixed + sponsors * m.SystemSponsorLevelCost) / accounts
