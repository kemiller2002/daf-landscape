module CapitalMinimization.Tests

open Xunit
open ServicingEconomics.Domain
open ServicingEconomics.Parameters
open CapitalMinimization.Design
open CapitalMinimization.Layers
open CapitalMinimization.Development
open CapitalMinimization.Designs
open CapitalMinimization.Sequences

let close (tol: float) (expected: float) (actual: float) =
    Assert.True(abs (expected - actual) <= tol, $"expected {expected}, got {actual}")

let five b assets = (ServicingEconomics.Analysis.equalSponsors 5 (sponsor "s" 1000.0 b)).Build assets

// ---------------------------------------------------------------- baseline preserved

[<Fact>]
let ``previous study anchor plan still needs 3.56M (baseline unchanged)`` () =
    let rows = ServicingEconomics.CashFlow.simulate ServicingEconomics.Strategies.anchor
    close 10000.0 3.56e6 (ServicingEconomics.CashFlow.capitalRequired rows)

[<Fact>]
let ``market-mix AI-native minutes reproduce the previous 50.7`` () = close 0.05 50.72 baseMarketMinutes

// ---------------------------------------------------------------- handling targets and workload

[<Theory>]
[<InlineData(10.0)>]
[<InlineData(30.0)>]
[<InlineData(100.0)>]
let ``withTarget rescales the market mix to the target`` (t: float) =
    let s = withTarget t (sponsor "s" 1000.0 archetypeMixBalance)
    let minutes = s.Mix |> List.sumBy (fun a -> a.ShareOfAccounts * a.Minutes AiNative)
    close 0.01 t minutes

[<Fact>]
let ``integration hours without learning are linear and with learning sub-linear`` () =
    close 1e-9 900.0 (integrationHours 300.0 1.0 3)
    close 1e-9 (300.0 * 1.85) (integrationHours 300.0 0.85 2)

[<Fact>]
let ``empty portfolio has no revenue and only fixed cost`` () =
    let r = evaluateDesign f5 50.0 (price 20.0) noStress []
    close 1e-9 0.0 r.Base.Revenue
    let expected =
        (f5.People |> List.sumBy (fun p -> p.LoadedCost)) + (f5.Contracted |> List.sumBy snd) + (f5.NonPersonnel |> List.sumBy snd)
        + 5.0 * f5.PerPersonOverhead + 10.0 * 0.5 * 48.0 * (f5.Pools |> List.averageBy (fun p -> p.LoadedHourly))
        // named compliance owner floor: 0.25 FTE bought fractionally at the contract premium
        + 0.25 * f5.ProductiveHours * complianceLoaded / hours * 1.5
    close 1.0 expected r.Base.TotalCost

[<Fact>]
let ``coordination cost is zero for one person`` () =
    let r = evaluateDesign f1 50.0 (price 20.0) noStress []
    close 1e-9 0.0 r.CoordinationCost

[<Fact>]
let ``hiring waits until residual need reaches 0.75 FTE`` () =
    let one = { f5 with People = []; Pools = [ { (List.head (pools false)) with Share = 1.0 } ]; SponsorMinutes = 0.0; RelationshipHours = 0.0; IntegrationFirstSponsorHours = 0.0 }
    let q = one.ProductiveHours * one.Utilisation
    // one sponsor whose account hours equal x FTE of queue capacity
    let withFte x =
        let s = { (sponsor "s" 1000.0 archetypeMixBalance) with AnnualSponsorCost = 0.0 }
        let perAccount = (withTarget 60.0 s |> fun t -> ServicingEconomics.Economics.sponsorHours AiNative noStress [] t) / 1000.0
        [ { s with Accounts = x * q / perAccount } ]
    let at x = (evaluateDesign one 60.0 (price 20.0) noStress (withFte x)).Pools |> List.head
    Assert.Equal(0.0, (at 0.74).Hires)
    Assert.Equal(1.0, (at 0.76).Hires)
    close 1e-6 0.74 (at 0.74).AddedFte

[<Fact>]
let ``higher handling minutes never lower the break-even`` () =
    let be t = snd (assetsForMarginDesign f5 t (price 20.0) noStress (ServicingEconomics.Analysis.equalSponsors 5 (sponsor "s" 1000.0 250000.0)) 0.0)
    let values = handlingTargets |> List.map (be >> Option.defaultValue infinity)
    Assert.True(values |> List.pairwise |> List.forall (fun (a, b) -> a <= b))

// ---------------------------------------------------------------- controls

[<Fact>]
let ``one founder cannot separate duties; three core with a reviewer can`` () =
    let ss = five 250000.0 1.0e9
    Assert.False((evaluateDesign f1 50.0 (price 20.0) noStress ss).ControlFeasible)
    Assert.False((evaluateDesign f2 50.0 (price 20.0) noStress ss).ControlFeasible)
    Assert.True((evaluateDesign f3 50.0 (price 20.0) noStress ss).ControlFeasible)
    Assert.True((evaluateDesign f5 50.0 (price 20.0) noStress ss).ControlFeasible)

// ---------------------------------------------------------------- development

[<Fact>]
let ``at 1x productivity the effective cost is the conventional cost`` () =
    close 1e-6 (5.0e6 * 0.35) (effectiveCost unboundBaseline 0.35 1.0)

[<Fact>]
let ``minimum servicing product at 1x matches the DEV bottom-up estimate of 2.43M`` () =
    close 1000.0 2.43e6 (minimumProductCost unboundBaseline 1.0)

[<Fact>]
let ``savings are bounded by the construction share (Amdahl)`` () =
    let b = unboundBaseline
    close 1e-9 (1.0 - ((1.0 - b.ConstructionShare) + b.ConstructionShare * b.ComputeShareOfReplaced)) (savingsCeiling b)
    Assert.True(effectiveCost unboundBaseline 1.0 1000.0 > 5.0e6 * (1.0 - savingsCeiling unboundBaseline) - 1.0)

[<Fact>]
let ``an investment below the safety floor delivers nothing safe`` () =
    Assert.Equal(0.0, deliverableScope unboundBaseline 100000.0 10.0)
    Assert.False(safeToOperate unboundBaseline 250000.0 10.0)

// ---------------------------------------------------------------- layers

[<Fact>]
let ``layer views order incremental below fully allocated below standalone`` () =
    let ss = five 250000.0 1.0e9
    let total d = (evaluateDesign d 50.0 (price 20.0) noStress ss).Base.TotalCost
    let inc = servicingCost Incremental baseLayers total f5
    let alloc = servicingCost FullyAllocated baseLayers total f5
    let alone = servicingCost Standalone baseLayers total f3
    Assert.True(inc < alloc)
    Assert.True(inc < alone)

[<Fact>]
let ``consolidated view counts all of Echelon once and no internal charge`` () =
    let lc = baseLayers
    let p = consolidated lc 2.0e6 1.0e6
    close 1e-6 (2.0e6 - 1.0e6 - unboundAnnual lc - lc.ServicingSpecificPlatform - lc.EchelonAnnual) p

// ---------------------------------------------------------------- sequences and failures

[<Fact>]
let ``every sequence needs capital`` () =
    sequences |> List.iter (fun s -> Assert.True(capitalRequired (simulate s) > 0.0, s.Name))

[<Fact>]
let ``lower productivity and longer sales cycles never reduce capital`` () =
    for s in sequences do
        let c0 = capitalRequired (simulate s)
        Assert.True(capitalRequired (simulate (productivityHalved s)) >= c0 - 1.0, s.Name)
        Assert.True(capitalRequired (simulate (acquisitionTwiceAsLong s)) >= c0 - 1.0, s.Name)

[<Fact>]
let ``economic view never needs less capital than cash view`` () =
    for s in sequences do
        Assert.True(capitalRequired (simulate (economic s)) >= capitalRequired (simulate s) - 1.0, s.Name)
