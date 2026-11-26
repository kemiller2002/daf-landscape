/// Charity registry operating-cost model (Track B): reconstruction of the $316k estimate and alternatives.
module CompetitiveDisplacement.Registry

open CompetitiveDisplacement.Inputs

type Drivers =
    { CharitiesPerSponsor: float
      Sponsors: float
      ChangeRate: float
      RefreshDays: float option // None = change-driven monitoring; Some d = full periodic re-review every d days
      GrantsPerYear: float }

type RegistryCost =
    { AltId: string
      Charities: float
      ExceptionsPerYear: float
      HumanHours: float
      Lines: (string * float) list
      Total: float
      PerGrant: float
      PerSponsor: float
      Establishment: float }

let private p (rp: Map<string, float>) k = Map.find k rp

/// Charities actually in use: a shared registry covers the union across sponsors (heavy overlap).
let charitiesInUse (alt: RegistryAlt) (rp: Map<string, float>) (d: Drivers) =
    if d.Sponsors <= 1.0 then d.CharitiesPerSponsor
    elif alt.Shared then d.CharitiesPerSponsor * d.Sponsors ** p rp "union_exponent"
    else d.CharitiesPerSponsor * d.Sponsors // a per-sponsor registry repeats the work for each sponsor

/// Human minutes a year: change-driven = changes + new charities + evidence expiry; periodic = full re-review of every charity.
let workload (alt: RegistryAlt) (rp: Map<string, float>) (d: Drivers) (n: float) =
    let exc = p rp "exception_minutes"
    let newCh = n * p rp "new_charity_share" * p rp "new_charity_exception_rate"
    let changes = n * d.ChangeRate
    let expiry = n * p rp "evidence_expiry_share"
    let residual = 1.0 - alt.AutoResolve
    let alerts = n * p rp "name_match_alert_rate" * residual * p rp "alert_minutes"
    match d.RefreshDays with
    | None ->
        let exceptions = (changes + newCh) * residual
        exceptions, exceptions * exc + expiry * p rp "expiry_refresh_minutes" + alerts
    | Some days ->
        let reviews = n * 365.0 / days
        let exceptions = (changes + newCh) * residual
        exceptions, exceptions * exc + reviews * p rp "periodic_review_minutes" * residual + alerts

let establishment (alt: RegistryAlt) (rp: Map<string, float>) =
    // connector build ~160 h each, exception/hold tooling 400 h, entity resolution 800 h, productization 600 h if standalone
    let hours = alt.Connectors * 160.0 * (1.0 - alt.EchelonConnectorSaving) + 400.0 + 800.0 + (if alt.StandaloneOverhead > 0.0 then 600.0 else 0.0)
    hours * p rp "engineering_rate" + alt.CounselHours * p rp "counsel_rate"

let cost (alt: RegistryAlt) (rp: Map<string, float>) (d: Drivers) : RegistryCost =
    let n = charitiesInUse alt rp d
    let exceptions, minutes = workload alt rp d n
    let sponsorDecisionHours = if alt.Shared then d.Sponsors * p rp "sponsor_decision_hours" else 0.0
    let humanHours = minutes / 60.0 + sponsorDecisionHours
    let steward = max (alt.StewardFloorFte * 1800.0) humanHours * p rp "compliance_rate"
    let scale = n / 20000.0
    let lines =
        [ "storage and compute (RC-01/02/04)", (276.0 + 378.0 + 3600.0) * max 1.0 scale
          "registry database (RC-03)", 6237.0 * alt.DbShare
          "paid state data (RC-05)", alt.StateData
          "connector maintenance (RC-06)", alt.Connectors * p rp "connector_hours_per_year" * (1.0 - alt.EchelonConnectorSaving) * p rp "engineering_rate"
          "stewardship labour (RC-07)", steward
          "charity support desk (RC-08)", alt.SupportFte * p rp "support_fte_cost"
          "counsel (RC-09)", alt.CounselHours * p rp "counsel_rate"
          "TPSP audit, vendor minimums, rider (RC-10)", alt.TpspAudit + alt.Insurance
          "AI exception dossiers", exceptions * alt.AiPerException / max 0.01 (1.0 - alt.AutoResolve)
          "commercial data licence", (if alt.CommercialLicence > 0.0 then p rp "commercial_licence_usd" else 0.0)
          "standalone service overhead", alt.StandaloneOverhead
          "Echelon reliance", alt.EchelonReliance ]
    let total = lines |> List.sumBy snd
    { AltId = alt.Id
      Charities = n
      ExceptionsPerYear = exceptions
      HumanHours = humanHours
      Lines = lines
      Total = total
      PerGrant = if d.GrantsPerYear > 0.0 then total / d.GrantsPerYear else nan
      PerSponsor = total / max 1.0 d.Sponsors
      Establishment = establishment alt rp }

/// Reconstruction of the published $316k from its components at a level.
let reconstruction (level: Level) (cs: RegistryComponent list) =
    cs |> List.map (fun c -> c, pick level c.Annual), cs |> List.sumBy (fun c -> pick level c.Annual)
