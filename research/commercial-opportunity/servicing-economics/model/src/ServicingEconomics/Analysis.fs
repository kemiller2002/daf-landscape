/// Searches and sweeps over the annual model. Pure functions.
module ServicingEconomics.Analysis

open ServicingEconomics.Domain
open ServicingEconomics.Economics

/// A portfolio shape: a function from total average assets to the sponsors that hold them.
type Shape = { Name: string; Build: float -> Sponsor list }

/// Scale a template portfolio so its total average assets equal the target, keeping its mix.
let scaleTo (template: Sponsor list) (assets: float) =
    let current = template |> List.sumBy (sponsorAssets 1.0)
    if current <= 0.0 then template
    else template |> List.map (fun s -> { s with Accounts = s.Accounts * assets / current })

/// n equal sponsors that share the given archetype mix and sponsor costs.
let equalSponsors (n: int) (template: Sponsor) =
    { Name = $"{n} x {template.Name}"
      Build = fun assets -> List.init n (fun i -> { template with Name = $"{template.Name} {i + 1}" }) |> fun ss -> scaleTo ss assets }

/// Asset grid for searches: $10M steps to $20B.
let assetGrid = [ for i in 1 .. 2000 -> float i * 1.0e7 ]

/// Smallest grid assets from which the margin target holds at every larger grid point (sustained
/// crossing), and the first grid point where it holds at all. None if never reached.
let assetsForMargin (eval: Sponsor list -> Result) (shape: Shape) (target: float) =
    let ok a = (eval (shape.Build a)).OperatingMargin >= target - 1e-12
    let flags = assetGrid |> List.map (fun a -> a, ok a)
    let first = flags |> List.tryFind snd |> Option.map fst
    let sustained =
        match List.tryLast flags with
        | Some (_, true) ->
            flags |> List.rev |> List.takeWhile snd |> List.tryLast |> Option.map fst
        | _ -> None
    first, sustained

/// Smallest price in 0.1 bp steps (0.1–100 bps) at which a portfolio reaches the margin target.
let minimumBps (evalAt: Price -> Result) (basePrice: Price) (target: float) =
    [ for i in 1 .. 1000 -> float i / 10.0 ]
    |> List.tryFind (fun bps -> (evalAt { basePrice with Bps = bps }).OperatingMargin >= target - 1e-12)

/// Smallest minimum annual fee (in $5k steps up to $2M) that brings a single sponsor's own
/// marginal contribution to zero, i.e. the contractual minimum that stops a small sponsor losing money.
let breakEvenMinimumFee (contribution: Price -> float) (basePrice: Price) =
    [ for i in 0 .. 400 -> float i * 5000.0 ]
    |> List.tryFind (fun m -> contribution { basePrice with MinimumAnnualFee = m } >= 0.0)

/// Apply named stresses to a base evaluation function.
let stressTable (evalUnder: Stress -> Result) (stresses: Stress list) =
    stresses |> List.map (fun s -> s, evalUnder s)

/// Minimum starting assets at which a portfolio stays at or above the margin target after the stress
/// (stress applied to the scaled portfolio).
let assetsToSurvive (evalUnder: Stress -> Sponsor list -> Result) (shape: Shape) (stress: Stress) (target: float) =
    assetsForMargin (evalUnder stress) shape target

/// Standard stress set (exploratory; factors are assumptions).
let standardStresses =
    [ noStress
      { noStress with Name = "market -10%"; AssetFactor = 0.9 }
      { noStress with Name = "market -20%"; AssetFactor = 0.8 }
      { noStress with Name = "market -30%"; AssetFactor = 0.7 }
      { noStress with Name = "market -40%"; AssetFactor = 0.6 }
      { noStress with Name = "market -50%"; AssetFactor = 0.5 }
      { noStress with Name = "net outflow -15% assets"; AssetFactor = 0.85 }
      { noStress with Name = "lose largest sponsor"; DropLargestSponsor = true }
      { noStress with Name = "automation 50% worse (minutes x1.5)"; MinutesFactor = 1.5 }
      { noStress with Name = "exceptions/volume x1.5"; VolumeFactor = 1.5 }
      { noStress with Name = "wages +15%"; WageFactor = 1.15 }
      { noStress with Name = "vendor prices +25%"; VendorFactor = 1.25 }
      { noStress with Name = "security incident $500k"; ExtraordinaryCost = 500000.0 }
      { noStress with Name = "combined: -30% market, minutes x1.5, wages +10%, vendors +25%"
                      AssetFactor = 0.7; MinutesFactor = 1.5; WageFactor = 1.1; VendorFactor = 1.25 }
      { noStress with Name = "severe: -40% market, lose largest, minutes x1.5, incident $500k"
                      AssetFactor = 0.6; DropLargestSponsor = true; MinutesFactor = 1.5; ExtraordinaryCost = 500000.0 } ]
