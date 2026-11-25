module ServicingEconomics.Tests

open Xunit
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Analysis
open ServicingEconomics.CashFlow
open ServicingEconomics.Parameters

let close (tol: float) (expected: float) (actual: float) =
    Assert.True(abs (expected - actual) <= tol, $"expected {expected}, got {actual}")

let h0 assets b bps stress = evaluate h0Org h0Activities Conventional (price bps) stress [ uniformSponsor "H0" assets b ]

// ---------------------------------------------------------------- reproduction of the prior memo (regression)

[<Theory>]
[<InlineData(0.5e9, 1000000.0, 1365250.0)>]
[<InlineData(0.75e9, 1500000.0, 1459000.0)>]
[<InlineData(1.0e9, 2000000.0, 1552750.0)>]
[<InlineData(1.5e9, 3000000.0, 1740250.0)>]
[<InlineData(2.0e9, 4000000.0, 1927750.0)>]
let ``H0 reproduces the prior memo table`` (assets: float, revenue: float, cost: float) =
    let r = h0 assets 200000.0 20.0 noStress
    close 0.01 revenue r.Revenue
    close 0.01 cost r.TotalCost

[<Fact>]
let ``H0 30 percent asset shock at 1B loses 152,750 as in the prior memo`` () =
    let r = h0 1.0e9 200000.0 20.0 { noStress with AssetFactor = 0.7 }
    close 0.01 -152750.0 r.OperatingProfit

[<Fact>]
let ``H0 break-even matches the closed form F / (r - v/B) on the 10M grid`` () =
    let exact = 1177750.0 / (0.002 - 75.0 / 200000.0)
    let shape = { Name = "H0"; Build = fun a -> [ uniformSponsor "H0" a 200000.0 ] }
    let first, sustained = assetsForMargin (fun ss -> evaluate h0Org h0Activities Conventional (price 20.0) noStress ss) shape 0.0
    Assert.Equal(Some (ceil (exact / 1.0e7) * 1.0e7), first)
    Assert.Equal(first, sustained)

[<Fact>]
let ``H0 at B = 25k cannot break even at any scale`` () =
    let shape = { Name = "H0"; Build = fun a -> [ uniformSponsor "H0" a 25000.0 ] }
    let first, _ = assetsForMargin (fun ss -> evaluate h0Org h0Activities Conventional (price 20.0) noStress ss) shape 0.0
    Assert.Equal(None, first)

// ---------------------------------------------------------------- units and invariants

[<Fact>]
let ``revenue is linear in bps and in assets`` () =
    let r10 = (h0 1.0e9 200000.0 10.0 noStress).Revenue
    let r20 = (h0 1.0e9 200000.0 20.0 noStress).Revenue
    let r20x2 = (h0 2.0e9 200000.0 20.0 noStress).Revenue
    close 1e-6 (2.0 * r10) r20
    close 1e-6 (2.0 * r20) r20x2
    close 1e-6 2000000.0 r20

[<Fact>]
let ``minimum fee tops up only small sponsors`` () =
    let p = { price 20.0 with MinimumAnnualFee = 100000.0 }
    let small = sponsorRevenue p 1.0 (uniformSponsor "small" 20.0e6 100000.0)
    let large = sponsorRevenue p 1.0 (uniformSponsor "large" 200.0e6 100000.0)
    let a, t, _ = small
    close 1e-6 40000.0 a
    close 1e-6 60000.0 t
    let _, t2, _ = large
    close 1e-6 0.0 t2

[<Fact>]
let ``dropping the largest sponsor removes exactly one of identical sponsors`` () =
    let s = uniformSponsor "same" 100.0e6 100000.0
    let kept = stressedSponsors (price 20.0) { noStress with DropLargestSponsor = true } [ s; s; s ]
    Assert.Equal(2, List.length kept)

[<Fact>]
let ``an empty portfolio has zero revenue and pays fixed cost`` () =
    let r = evaluate h0Org h0Activities Conventional (price 20.0) noStress []
    close 1e-6 0.0 r.Revenue
    close 1e-6 1177750.0 r.TotalCost
    Assert.True(System.Double.IsNaN r.OperatingMargin)

[<Fact>]
let ``margin target assets increase with the target`` () =
    let shape = { Name = "H0"; Build = fun a -> [ uniformSponsor "H0" a 200000.0 ] }
    let f t = snd (assetsForMargin (fun ss -> evaluate h0Org h0Activities Conventional (price 20.0) noStress ss) shape t)
    let targets = [ 0.0; 0.1; 0.2; 0.25; 0.3 ] |> List.map f |> List.choose id
    Assert.Equal(5, List.length targets)
    Assert.True(targets |> List.pairwise |> List.forall (fun (a, b) -> a <= b))

[<Fact>]
let ``minimum bps for H0 at 1B and B=200k equals the analytic break-even price`` () =
    let s = [ uniformSponsor "H0" 1.0e9 200000.0 ]
    let bps = minimumBps (fun p -> evaluate h0Org h0Activities Conventional p noStress s) (price 20.0) 0.0
    // revenue = cost: bps = (1,177,750 + 75 * 5,000) / 1e9 * 1e4 = 15.5275 -> first 0.1 step is 15.6
    Assert.Equal(Some 15.6, bps |> Option.map (fun v -> System.Math.Round(v, 1)))

// ---------------------------------------------------------------- capacity and step costs

let capOrg =
    { h0Org with
        Name = "capacity test"
        Core = [ { Title = "ops"; LoadedCost = 100000.0; CashCost = 100000.0; ServicingShare = 0.5; StartMonth = 0 } ]
        NonPersonnelFixed = []
        ProductiveHours = 1600.0
        ServicingHourlyLoaded = 50.0
        StepRules = [ { Name = "supervisor"; On = ServicingFte; Free = 4.0; Size = 4.0; CostPerStep = 120000.0 } ] }

let minutesActivity minutes =
    [ { Id = "M"; Name = "per account"; Driver = PerAccountYear; Minutes = (fun _ -> minutes); ExternalCost = 0.0; PassThrough = false } ]

[<Fact>]
let ``servicing hours within core capacity add no staff`` () =
    // 800 core hours; 1,000 accounts x 48 min = 800 h
    let r = evaluate capOrg (minutesActivity 48.0) Conventional (price 20.0) noStress [ uniformSponsor "s" 1.0e8 100000.0 ]
    close 1e-6 800.0 r.ServicingHours
    close 1e-6 0.0 r.AddedServicingFte

[<Fact>]
let ``added staff are whole FTEs and supervisors step in after four`` () =
    // 10,000 accounts x 48 min = 8,000 h; minus 800 core = 7,200 h -> 4.5 -> 5 FTE; supervisor steps = ceil((5-4)/4) = 1
    let r = evaluate capOrg (minutesActivity 48.0) Conventional (price 20.0) noStress [ uniformSponsor "s" 1.0e9 100000.0 ]
    close 1e-6 5.0 r.AddedServicingFte
    close 1e-6 (5.0 * 1600.0 * 50.0) r.AddedServicingCost
    close 1e-6 120000.0 r.StepFixed

[<Fact>]
let ``december peak above monthly capacity is bought at a premium`` () =
    let org = { capOrg with DecemberShare = 0.25; PeakPremium = 0.5; StepRules = [] }
    let r = evaluate org (minutesActivity 48.0) Conventional (price 20.0) noStress [ uniformSponsor "s" 1.0e9 100000.0 ]
    // demand 2,000 h in December; capacity (800 + 5*1600)/12 = 733.33 h; excess 1,266.67 h at $75/h
    close 1e-6 ((2000.0 - 8800.0 / 12.0) * 75.0) r.PeakCost

// ---------------------------------------------------------------- cash flow

let plan customers =
    { Name = "test"
      Org = capOrg
      Activities = minutesActivity 0.0
      Approach = Conventional
      Price = price 20.0
      Customers = customers
      OneTime = [ 0, "setup", 50000.0 ]
      PreLaunchNonPersonnelShare = 1.0
      CollectionLagMonths = 1
      FinancingRate = 0.0
      CashView = false
      Months = 24 }

[<Fact>]
let ``with no customers capital equals payroll plus one-time costs`` () =
    let rows = simulate (plan [])
    close 1e-6 (100000.0 * 2.0 + 50000.0) (capitalRequired rows)

[<Fact>]
let ``quarterly-in-arrears billing collects a full year of fees over twelve months of service`` () =
    let s = uniformSponsor "s" 1.0e9 100000.0
    let rows = simulate (plan [ { Sponsor = s; SignMonth = 0; OnboardingMonths = 0; ImplementationFee = 0.0 } ])
    // live from month 0; quarters bill at months 2, 5, 8, 11 and are received one month later: 3, 6, 9, 12
    let received = rows |> List.filter (fun r -> r.Month >= 3 && r.Month <= 12) |> List.sumBy (fun r -> r.CashIn)
    close 1e-6 2000000.0 received

[<Fact>]
let ``implementation fee is received half at signing and half at go-live`` () =
    let s = uniformSponsor "s" 1.0e8 100000.0
    let rows = simulate (plan [ { Sponsor = s; SignMonth = 2; OnboardingMonths = 4; ImplementationFee = 100000.0 } ])
    close 1e-6 50000.0 (rows |> List.find (fun r -> r.Month = 2)).CashIn
    close 1e-6 50000.0 (rows |> List.find (fun r -> r.Month = 6)).CashIn

[<Fact>]
let ``per-account floor raises only accounts whose asset fee is below it`` () =
    // two archetypes: 500 accounts at $10k (fee $20 at 20 bps) and 500 at $1M (fee $2,000); floor $100
    let mix =
        [ { Name = "small"; ShareOfAccounts = 0.5; AverageBalance = 10000.0; Minutes = (fun _ -> 0.0); External = (fun _ -> 0.0); Payments = (fun _ -> 0.0); DecemberShare = 0.0 }
          { Name = "large"; ShareOfAccounts = 0.5; AverageBalance = 1.0e6; Minutes = (fun _ -> 0.0); External = (fun _ -> 0.0); Payments = (fun _ -> 0.0); DecemberShare = 0.0 } ]
    let s = { uniformSponsor "mixed" 1.0e8 100000.0 with Accounts = 1000.0; Mix = mix }
    let a, _, _ = sponsorRevenue { price 20.0 with PerAccountMinimum = 100.0 } 1.0 s
    close 1e-6 (500.0 * 100.0 + 500.0 * 2000.0) a

[<Fact>]
let ``asset shocks do not reduce revenue protected by a per-account floor`` () =
    let s = uniformSponsor "small" 1.0e7 10000.0
    let a1, _, _ = sponsorRevenue { price 20.0 with PerAccountMinimum = 100.0 } 1.0 s
    let a2, _, _ = sponsorRevenue { price 20.0 with PerAccountMinimum = 100.0 } 0.5 s
    close 1e-6 a1 a2
