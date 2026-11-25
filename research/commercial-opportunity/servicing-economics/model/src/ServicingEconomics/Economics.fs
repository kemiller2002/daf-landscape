/// Pure annual economics of a DAF servicing business. No I/O, no mutation.
module ServicingEconomics.Economics

open ServicingEconomics.Domain

let private ceilSteps (value: float) (free: float) (size: float) =
    if size <= 0.0 then 0.0 else ceil (max 0.0 (value - free) / size - 1e-9)

/// Average assets of a sponsor's book (sum over archetypes), after an asset factor.
let sponsorAssets (assetFactor: float) (s: Sponsor) =
    s.Mix |> List.sumBy (fun a -> s.Accounts * a.ShareOfAccounts * a.AverageBalance) |> (*) assetFactor

/// Annual occurrences of a driver for one sponsor.
let occurrences (volumeFactor: float) (s: Sponsor) (driver: Driver) =
    let perArchetype f = s.Mix |> List.sumBy (fun a -> s.Accounts * a.ShareOfAccounts * f a)
    match driver with
    | PerAccountYear -> s.Accounts
    | PerGrant -> volumeFactor * perArchetype (fun a -> a.GrantsPerYear)
    | PerContribution -> volumeFactor * perArchetype (fun a -> a.ContributionsPerYear)
    | PerContact -> volumeFactor * perArchetype (fun a -> a.ContactsPerYear)
    | PerComplexAsset -> volumeFactor * perArchetype (fun a -> a.ComplexAssetsPerYear)
    | PerNewAccount -> s.Accounts * s.NewAccountRate
    | PerSponsorYear -> 1.0

/// Human servicing hours a sponsor generates in a year.
let sponsorHours (approach: Approach) (stress: Stress) (activities: Activity list) (s: Sponsor) =
    activities
    |> List.sumBy (fun act -> occurrences stress.VolumeFactor s act.Driver * act.Minutes approach)
    |> fun minutes -> minutes * s.ComplexityMultiplier * stress.MinutesFactor / 60.0

/// External (vendor) cost a sponsor generates, excluding pass-through items billed at cost.
let sponsorExternalCost (stress: Stress) (activities: Activity list) (s: Sponsor) =
    activities
    |> List.filter (fun act -> not act.PassThrough)
    |> List.sumBy (fun act -> occurrences stress.VolumeFactor s act.Driver * act.ExternalCost)
    |> (*) stress.VendorFactor

/// Annual fee revenue from one sponsor: asset fee, top-up to the contractual minimum, per-account fees.
let sponsorRevenue (price: Price) (assetFactor: float) (s: Sponsor) =
    let assetFee = sponsorAssets assetFactor s * price.Bps / 10000.0
    let topUp = max 0.0 (price.MinimumAnnualFee - assetFee)
    let other = s.Accounts * price.ExceptionalFeesPerAccountYear
    assetFee, topUp, other

let private applyAccounts (stress: Stress) (s: Sponsor) = { s with Accounts = s.Accounts * stress.AccountFactor }

/// Sponsors after the stress: account factor applied and, if required, the largest sponsor removed.
let stressedSponsors (price: Price) (stress: Stress) (sponsors: Sponsor list) =
    let scaled = sponsors |> List.map (applyAccounts stress)
    if stress.DropLargestSponsor && List.length scaled > 1 then
        let fee s = let a, t, o = sponsorRevenue price stress.AssetFactor s in a + t + o
        let largest = scaled |> List.indexed |> List.maxBy (snd >> fee) |> fst
        scaled |> List.indexed |> List.filter (fun (i, _) -> i <> largest) |> List.map snd
    else
        scaled

let private stepValue (sponsors: Sponsor list) (assets: float) (addedFte: float) = function
    | Sponsors -> float (List.length sponsors)
    | Accounts -> sponsors |> List.sumBy (fun s -> s.Accounts)
    | AssetsUsd -> assets
    | ServicingFte -> addedFte

/// Annual result for a portfolio of sponsors under one organization, price, approach and stress.
let evaluate (org: Organization) (activities: Activity list) (approach: Approach) (price: Price) (stress: Stress) (sponsors0: Sponsor list) =
    let sponsors = stressedSponsors price stress sponsors0
    let revenues = sponsors |> List.map (sponsorRevenue price stress.AssetFactor)
    let assetFee = revenues |> List.sumBy (fun (a, _, _) -> a)
    let topUp = revenues |> List.sumBy (fun (_, t, _) -> t)
    let other = revenues |> List.sumBy (fun (_, _, o) -> o)
    let revenue = assetFee + topUp + other
    let assets = sponsors |> List.sumBy (sponsorAssets stress.AssetFactor)
    let accounts = sponsors |> List.sumBy (fun s -> s.Accounts)
    let hours = sponsors |> List.sumBy (sponsorHours approach stress activities)
    let external = sponsors |> List.sumBy (sponsorExternalCost stress activities)
    let coreHours = org.Core |> List.sumBy (fun r -> r.ServicingShare * org.ProductiveHours)
    let addedFte = ceilSteps hours coreHours org.ProductiveHours
    let hourly = org.ServicingHourlyLoaded * stress.WageFactor
    let addedCost = addedFte * org.ProductiveHours * hourly
    // December: demand above one month of total capacity is bought at a premium (temporary staff or overtime).
    let decemberDemand = hours * org.DecemberShare
    let monthlyCapacity = (coreHours + addedFte * org.ProductiveHours) / 12.0
    let peakCost = max 0.0 (decemberDemand - monthlyCapacity) * hourly * (1.0 + org.PeakPremium)
    let corePersonnel = org.Core |> List.sumBy (fun r -> r.LoadedCost) |> (*) stress.WageFactor
    let nonPersonnel = org.NonPersonnelFixed |> List.sumBy snd |> (*) stress.VendorFactor
    let step =
        org.StepRules
        |> List.sumBy (fun r -> ceilSteps (stepValue sponsors assets addedFte r.On) r.Free r.Size * r.CostPerStep)
        |> (*) stress.WageFactor
    let sponsorCosts = sponsors |> List.sumBy (fun s -> s.AnnualSponsorCost)
    let total = external + addedCost + peakCost + corePersonnel + nonPersonnel + step + sponsorCosts + stress.ExtraordinaryCost
    let profit = revenue - total
    let contribution = revenue - external - addedCost - peakCost - sponsorCosts
    { AverageAssets = assets
      Accounts = accounts
      Sponsors = List.length sponsors
      Revenue = revenue
      AssetFeeRevenue = assetFee
      MinimumFeeTopUp = topUp
      OtherRevenue = other
      ExternalVariableCost = external
      ServicingHours = hours
      CoreServicingHours = coreHours
      AddedServicingFte = addedFte
      AddedServicingCost = addedCost
      PeakCost = peakCost
      CorePersonnel = corePersonnel
      NonPersonnelFixed = nonPersonnel
      StepFixed = step
      SponsorCosts = sponsorCosts
      ExtraordinaryCost = stress.ExtraordinaryCost
      TotalCost = total
      OperatingProfit = profit
      OperatingMargin = (if revenue > 0.0 then profit / revenue else nan)
      ContributionMargin = (if revenue > 0.0 then contribution / revenue else nan) }

/// Marginal annual contribution of one sponsor: its fees less its external cost, its hours at the
/// marginal loaded rate and its sponsor-specific cost (fixed and step costs excluded).
let sponsorContribution (org: Organization) (activities: Activity list) (approach: Approach) (price: Price) (stress: Stress) (s0: Sponsor) =
    let s = applyAccounts stress s0
    let a, t, o = sponsorRevenue price stress.AssetFactor s
    let hours = sponsorHours approach stress activities s
    let cost = sponsorExternalCost stress activities s + hours * org.ServicingHourlyLoaded * stress.WageFactor + s.AnnualSponsorCost
    a + t + o, cost, a + t + o - cost

/// Hours and external cost per account-year for a sponsor (diagnostic).
let perAccount (approach: Approach) (activities: Activity list) (s: Sponsor) =
    let hours = sponsorHours approach noStress activities s
    let ext = sponsorExternalCost noStress activities s
    (if s.Accounts > 0.0 then hours * 60.0 / s.Accounts else 0.0), (if s.Accounts > 0.0 then ext / s.Accounts else 0.0)
