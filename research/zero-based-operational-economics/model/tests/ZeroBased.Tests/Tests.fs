module ZeroBased.Tests

open System.IO
open Xunit
open CompetitiveDisplacement.Inputs
open ZeroBased.Domain
open ZeroBased.Volume
open ZeroBased.Simulation
open ZeroBased.Revenue

let root = Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", ".."))
let dataDir = Path.Combine(root, "data")
let baselineDir = Path.GetFullPath(Path.Combine(root, "..", "competitive-displacement", "data", "model-inputs"))

let inputs =
    lazy (match Program.loadInputs dataDir with Ok i -> i | Error es -> failwithf "%A" es)
let baseline =
    lazy (match Baseline.loadBaseline baselineDir with Ok b -> b | Error es -> failwithf "%A" es)

let near (tol: float) (expected: float) (actual: float) =
    Assert.True(abs (actual - expected) <= tol * abs expected, $"expected {expected} got {actual}")

// ------------------------------------------------------------------ baseline

[<Fact>]
let ``original model is reproduced: 1.92B break-even and 3.85M opex at 20 bps`` () =
    let r = Baseline.reconstruct baseline.Value "MD-5" 20.0
    near 0.005 1.92e9 r.BreakEvenAssets
    near 0.005 3.85e6 r.OpexAtBreakEven
    near 0.001 146.77 r.VariablePerAcct
    near 0.002 52.76 r.HumanMinutesPerAcct
    near 0.0001 2.5e6 r.Fixed
    near 0.005 2.33e9 r.FullyLoadedAssets

[<Fact>]
let ``baseline variable cost decomposes exactly into its components`` () =
    let r = Baseline.reconstruct baseline.Value "MD-5" 20.0
    let sum = r.LabourPerAcct + r.InfraPerAcct + r.ExternalPerAcct + r.AiPerAcct + r.PreventionPerAcct + r.FailurePerAcct
    near 1e-9 r.VariablePerAcct sum

// ------------------------------------------------------------------ inputs

let classes = set [ "ELIMINATED"; "PREVENTED"; "DETERMINISTIC"; "AUTO-EXCEPTION"; "AI-ASSISTED"; "HUMAN-JUDGMENT"; "INDEPENDENT-AUTHORIZATION"; "SPONSOR-OWNED"; "EXTERNAL-PROVIDER"; "SHARED-ECHELON" ]

[<Fact>]
let ``every activity has a valid classification, ordered ranges and an evidence class`` () =
    for a in inputs.Value.Activities do
        Assert.True(Set.contains a.Classification classes, $"{a.Id} classification {a.Classification}")
        Assert.True(a.Freq.Low <= a.Freq.Base && a.Freq.Base <= a.Freq.High, $"{a.Id} freq")
        Assert.True(a.Exception.Low <= a.Exception.Base && a.Exception.Base <= a.Exception.High, $"{a.Id} exception")
        Assert.True(a.Minutes.Low <= a.Minutes.Base && a.Minutes.Base <= a.Minutes.High, $"{a.Id} minutes")
        Assert.False(System.String.IsNullOrWhiteSpace a.EvidenceClass, $"{a.Id} evidence")

[<Fact>]
let ``activity identifiers are unique and every assumption range is ordered`` () =
    let ids = inputs.Value.Activities |> List.map (fun a -> a.Id)
    Assert.Equal(ids.Length, (ids |> List.distinct).Length)
    for ps in [ inputs.Value.Params; inputs.Value.Infra; inputs.Value.Beneficium ] do
        for KeyValue(k, r) in ps do
            Assert.True(r.Low <= r.Base && r.Base <= r.High, $"{k} range")

// ------------------------------------------------------------------ simulation

[<Fact>]
let ``weekend arrivals start their SLA clock on the next business day`` () =
    // day 5 is a Saturday in the model calendar; day 7 the following Monday
    Assert.True(isWeekend 5 && isWeekend 6 && not (isWeekend 7))
    Assert.Equal(1.0, businessAge 5 7)
    Assert.Equal(0.0, businessAge 7 7)

[<Fact>]
let ``queue conserves hours: completed plus carried equals arrived`` () =
    let vals = Analysis.baseVals inputs.Value
    let arr = [ for d in 0 .. 364 -> { Day = d; Hours = 3.0; SlaDays = 2.0 } ]
    let r = runPool vals "TEST" 0.5 arr []
    Assert.True(r.DoneHours <= r.ArrivedHours + 1e-6)
    Assert.True(r.PeakQueueHours >= 0.0)
    let full = runPool vals "TEST" 5.0 arr []
    near 1e-6 full.ArrivedHours full.DoneHours

[<Fact>]
let ``minimum staffing meets the SLA tolerance and one step fewer does not`` () =
    let vals = Analysis.baseVals inputs.Value
    let w = weights vals "year_end"
    let arr = [ for d in 0 .. 364 -> { Day = d; Hours = 3000.0 * w.[d]; SlaDays = 1.0 } ]
    let s, r = minimumStaff vals "TEST" arr []
    let tol = v vals "sla_breach_tolerance"
    Assert.True(r.BreachedHours <= tol * r.ArrivedHours + 1e-6)
    let fewer = runPool vals "TEST" (s - v vals "staff_step_fte") arr []
    Assert.True(fewer.BreachedHours > tol * fewer.ArrivedHours)

[<Fact>]
let ``seasonality weights sum to one`` () =
    let vals = Analysis.baseVals inputs.Value
    for p in [ "flat"; "year_end"; "month_end"; "quarter_end"; "tax_season"; "annual_q1" ] do
        near 1e-9 1.0 (Array.sum (weights vals p))

// ------------------------------------------------------------------ economics

let evalAt cfg accounts sponsors =
    let i = inputs.Value
    let vals = Analysis.baseVals i
    let p = Analysis.programme i "PG-HNW"
    Analysis.evaluate false Base vals (Analysis.infraVals i) i (Analysis.config i cfg) Infrastructure.C1 (Analysis.scenario vals p accounts sponsors p.DefaultBalance)

[<Fact>]
let ``cost views are ordered: incremental cash <= allocated <= standalone`` () =
    for a in [ 400.0; 4000.0; 40000.0 ] do
        let e = evalAt "CFG-5" a 2.0
        Assert.True(e.Views.View1 <= e.Views.View2 && e.Views.View2 <= e.Views.View3)

[<Fact>]
let ``total cost rises and cost per account falls with scale`` () =
    let costs = [ 500.0; 5000.0; 50000.0 ] |> List.map (fun a -> a, (evalAt "CFG-5" a 1.0).Views.View1)
    let totals = costs |> List.map snd
    Assert.True(List.pairwise totals |> List.forall (fun (x, y) -> y > x))
    let perAcct = costs |> List.map (fun (a, c) -> c / a)
    Assert.True(List.pairwise perAcct |> List.forall (fun (x, y) -> y < x))

[<Fact>]
let ``licensing configuration bears no administration labour`` () =
    let e = evalAt "CFG-1" 4000.0 2.0
    let adminVendor = e.Loads |> List.filter (fun l -> l.Bucket = AdminException || l.Bucket = AdminJudgment || l.Bucket = IndependentAuth) |> List.sumBy (fun l -> l.Minutes * l.VendorShare)
    Assert.Equal(0.0, adminVendor)

[<Fact>]
let ``sponsor-owned work is never vendor labour in any configuration`` () =
    for cfg in inputs.Value.Configs do
        let e = evalAt cfg.Id 2000.0 1.0
        let x = e.Loads |> List.filter (fun l -> l.Bucket = SponsorOwned) |> List.sumBy (fun l -> l.VendorShare)
        Assert.Equal(0.0, x)

[<Fact>]
let ``engineering always has at least three named persons (author plus two approvers)`` () =
    let e = evalAt "CFG-5" 1000.0 1.0
    let eng = e.Staffing.Pools |> List.find (fun p -> p.Pool = "ENG")
    Assert.True(eng.NamedPersons >= 3)

[<Fact>]
let ``activation language`` () =
    let cfg = Analysis.config inputs.Value "CFG-5"
    let c = (evalAt "CFG-5" 1000.0 2.0).Counts
    let ctx: Costs.Ctx = { Cfg = cfg; Counts = c; VendorOriginatesPayments = true }
    Assert.True(Costs.active ctx "always")
    Assert.True(Costs.active ctx "vendor_controls & tpsp & sponsors>=2")
    Assert.False(Costs.active ctx "sponsors>=3")
    Assert.False(Costs.active ctx "config:CFG-1,CFG-2")
    Assert.True(Costs.active ctx "accounts>=1000 & not_standalone")

// ------------------------------------------------------------------ revenue

[<Fact>]
let ``tiered fee is marginal`` () =
    let fee = tiered [ 100.0, 20.0; 1e12, 10.0 ] 150.0
    near 1e-12 ((100.0 * 20.0 + 50.0 * 10.0) / 10000.0) fee

[<Fact>]
let ``sustained break-even ignores an early crossing followed by a loss`` () =
    let grid = [ 1.0; 2.0; 3.0; 4.0; 5.0 ]
    let profit x = match x with 2.0 -> 1.0 | 3.0 -> -1.0 | x when x >= 4.0 -> 1.0 | _ -> -1.0
    Assert.Equal(Some 4.0, sustainedBreakEven profit grid)

// ------------------------------------------------------------------ infrastructure and Beneficium

[<Fact>]
let ``infrastructure floor dominates small scale and per-account cost falls`` () =
    let iv = Analysis.infraVals inputs.Value
    let c1 = (evalAt "CFG-5" 1000.0 1.0).Counts
    let c2 = (evalAt "CFG-5" 100000.0 1.0).Counts
    let a = Infrastructure.cost iv Infrastructure.C1 c1 0.0 0.0 0.0
    let b = Infrastructure.cost iv Infrastructure.C1 c2 0.0 0.0 0.0
    Assert.True((a.FloorAnnual + a.NonProdAnnual) / a.Total > 0.95)
    near 0.05 12490.0 a.Total // independent cross-check: infrastructure-notes Azure C1 at 1k accounts
    Assert.True(b.Total / 100000.0 < a.Total / 1000.0)
    let dr = Infrastructure.cost iv Infrastructure.C2 c1 0.0 0.0 0.0
    Assert.True(dr.Total > a.Total)

[<Fact>]
let ``Beneficium tiers are cumulative and zero-customer cost is independent of recipients for directory tiers`` () =
    let bv = Analysis.benVals inputs.Value
    let costs = Beneficium.allScenarios |> List.map (fun s -> (Beneficium.cost bv s 10000.0).Total)
    Assert.True(List.pairwise costs |> List.forall (fun (x, y) -> y >= x))
    Assert.Equal((Beneficium.cost bv Beneficium.PublicDirectory 0.0).Total, (Beneficium.cost bv Beneficium.PublicDirectory 500000.0).Total)

[<Fact>]
let ``continuous monitoring alone does not satisfy the 180-day validity rule; hybrid does`` () =
    let bv = Analysis.benVals inputs.Value
    Assert.False((Beneficium.vetting bv Beneficium.Continuous 20000.0 70000.0).Meets180DayValidity)
    Assert.True((Beneficium.vetting bv Beneficium.Hybrid 20000.0 70000.0).Meets180DayValidity)
    let manual = Beneficium.vetting bv Beneficium.FullManualPeriodic 20000.0 70000.0
    let auto = Beneficium.vetting bv Beneficium.AutomatedPeriodic 20000.0 70000.0
    Assert.True(manual.LabourCost > auto.LabourCost)

[<Fact>]
let ``evaluation is deterministic`` () =
    let a = (evalAt "CFG-5" 3000.0 2.0).Views
    let b = (evalAt "CFG-5" 3000.0 2.0).Views
    Assert.Equal(a.View1, b.View1)
    Assert.Equal(a.View3, b.View3)
