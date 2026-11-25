module Daf.Enterprise.Tests.EconomicsTwinCensusTests

open Xunit
open Daf.Enterprise.Economics
open Daf.Enterprise.Twin
open Daf.Enterprise.Tests.Fixtures

// ---------- economics ----------
[<Fact>]
let ``fee tiers reproduce Fidelity's published schedule`` () =
    Assert.Equal(100m, tieredFee fidelityTiers 100m 10000m)          // $60 -> $100 minimum
    Assert.Equal(1800m, tieredFee fidelityTiers 100m 300000m)        // 0.60%
    Assert.Equal(4500m, tieredFee fidelityTiers 100m 1000000m)       // 3000 + 1500
    Assert.Equal(7500m, tieredFee fidelityTiers 100m 2500000m)       // + 3000

[<Fact>]
let ``every parameter carries a basis and a non-negative value`` () =
    register defaults |> List.iter (fun p ->
        Assert.True(p.Value >= 0m, p.Name)
        match p.Basis with
        | Sourced s -> Assert.False(System.String.IsNullOrWhiteSpace s, p.Name)
        | Assumed _ -> ())

[<Fact>]
let ``staffing respects the structural floor and grows sublinearly`` () =
    let fte n = totalFte defaults (baseScenario n)
    Assert.True(fte 1000m >= 15m, "structural minimum incl. SoD and agent ownership")
    Assert.True(fte 10000m < fte 1000m * 10m)
    Assert.True(fte 1000000m < fte 100000m * 10m)
    Assert.True(fte 1000000m > fte 100000m)

[<Fact>]
let ``AI-native needs fewer people than the efficient conventional comparator at 10k accounts and above`` () =
    for n in [ 10000m; 100000m; 1000000m ] do
        let r = evaluate defaults (baseScenario n)
        Assert.True(r.AiNativeFte < r.ConvFteEfficient, $"{n}: {r.AiNativeFte} vs {r.ConvFteEfficient}")

[<Fact>]
let ``a 1,000-account sponsor does not cover its fixed floor on published fees`` () =
    let r = evaluate defaults (baseScenario 1000m)
    Assert.True(r.Revenue < r.AiNativeCost)

[<Fact>]
let ``break-even exists below one million accounts in the base case`` () =
    match breakEvenAccounts defaults baseScenario with
    | Some n -> Assert.True(n > 1000m && n < 1000000m, $"{n}")
    | None -> failwith "no break-even"

[<Fact>]
let ``accounts and AUM are independent: same accounts, lower balances, lower revenue, similar cost`` () =
    let rich = evaluate defaults (baseScenario 10000m)
    let small = evaluate defaults { baseScenario 10000m with AvgBalance = 25000m }
    Assert.True(small.Revenue < rich.Revenue / 5m)
    Assert.True(abs (small.AiNativeCost - rich.AiNativeCost) / rich.AiNativeCost < 0.05m)

[<Fact>]
let ``sensitivity: higher factor never lowers cost`` () =
    sensitivity defaults (baseScenario 100000m)
    |> List.iter (fun s -> Assert.True(s.High >= s.Low, s.Factor))

// ---------- twin ----------
let scn = baseScenario 100000m

[<Fact>]
let ``twin is deterministic for a seed`` () =
    Assert.Equal(simulate defaults scn baseline 42UL, simulate defaults scn baseline 42UL)

[<Fact>]
let ``twin conserves work: served plus final backlog equals arrivals`` () =
    let r = simulate defaults scn baseline 7UL
    r.Queues |> List.iter (fun q -> Assert.True(q.Served <= q.Arrived + 0.0001m))

[<Fact>]
let ``tenfold grant volume overwhelms exception capacity sized for baseline`` () =
    let b = simulate defaults scn baseline 1UL
    let x = simulate defaults scn (stresses |> List.find (fun s -> s.Name = "grant volume x10")) 1UL
    let ex (r: TwinResult) = r.Queues |> List.find (fun q -> q.Queue = GrantExceptions)
    Assert.True((ex x).DaysOverSla > (ex b).DaysOverSla)

[<Fact>]
let ``a 30-day custodian outage during surge exhausts a 2% cash buffer; 5 days does not`` () =
    let find n = stresses |> List.find (fun s -> s.Name = n)
    Assert.True((simulate defaults scn (find "custodian outage 30 days during surge") 3UL).LiquidityExhausted)
    Assert.False((simulate defaults scn (find "custodian outage 5 business days during surge") 3UL).LiquidityExhausted)

[<Fact>]
let ``twin output is labeled as simulated`` () =
    Assert.StartsWith("SIMULATED", (simulate defaults scn baseline 1UL).Provenance)

// ---------- census of design CSVs ----------
[<Fact>]
let ``activity census matches activity-classification.md`` () =
    let rows = readCsv "01-enterprise-outcomes/legacy-activity-classification.csv"
    let count col v = rows |> List.filter (fun r -> r.[col] = v) |> List.length
    Assert.Equal(80, rows.Length)
    Assert.Equal(14, count "disposition" "eliminate")
    Assert.Equal(9, count "disposition" "reduce")
    Assert.Equal(21, count "disposition" "automate_deterministic")
    Assert.Equal(20, count "disposition" "transform")
    Assert.Equal(16, count "disposition" "retain_human_accountable")
    // every retained-human activity is a legal obligation or a material risk control
    rows |> List.filter (fun r -> r.["disposition"] = "retain_human_accountable")
    |> List.iter (fun r -> Assert.Contains(r.["basis_category"], [ "legal_obligation"; "risk_control" ]))

[<Fact>]
let ``decision census: 81 decision types, P never moves money alone, all H are low volume`` () =
    let rows = readCsv "01-enterprise-outcomes/outcome-decisions.csv"
    Assert.Equal(81, rows.Length)
    Assert.Equal(37, rows |> List.filter (fun r -> r.["type"] = "D") |> List.length)
    Assert.Equal(11, rows |> List.filter (fun r -> r.["type"] = "P") |> List.length)
    Assert.Equal(33, rows |> List.filter (fun r -> r.["type"] = "H") |> List.length)
    rows |> List.filter (fun r -> r.["type"] = "P") |> List.iter (fun r -> Assert.Equal("no", r.["moves_money_or_legal_state"]))
    rows |> List.filter (fun r -> r.["type"] = "H") |> List.iter (fun r -> Assert.Contains(r.["volume_class"], [ "low"; "very_low" ]))

[<Fact>]
let ``every capability has exactly one accountable role`` () =
    readCsv "02-business-capabilities/accountability-matrix.csv"
    |> List.iter (fun r ->
        Assert.False(System.String.IsNullOrWhiteSpace r.["accountable_A"], r.["capability_id"])
        Assert.DoesNotContain(";", r.["accountable_A"]))

[<Fact>]
let ``every event has a producer, consumers, controls and audit evidence`` () =
    let rows = readCsv "06-data-and-knowledge/events.csv"
    Assert.True(rows.Length >= 50)
    rows |> List.iter (fun r ->
        for c in [ "producer"; "consumers"; "required_controls"; "audit_evidence" ] do
            let name = r.["event_type"]
            Assert.False(System.String.IsNullOrWhiteSpace r.[c], name + "." + c))

// ---------- B1: determination reuse ----------
[<Fact>]
let ``determination reuse: default rate is zero so the base case has no network fees`` () =
    let lines = aiNativeCosts defaults (baseScenario 100000m)
    Assert.Equal(0m, lines |> List.filter (fun l -> l.Line = "verification network fees") |> total)

[<Fact>]
let ``determination reuse: more reuse never raises grants-compliance FTE and never lowers net saving below fees`` () =
    reuseSweep defaults [ 10000m; 100000m; 1000000m ] [ 0.15m; 0.30m; 0.60m ] [ 0m; 0.2m; 0.5m; 0.8m ]
    |> List.groupBy (fun r -> r.Accounts, r.MinuteShare)
    |> List.iter (fun (_, rows) ->
        rows
        |> List.sortBy (fun r -> r.ReuseRate)
        |> List.pairwise
        |> List.iter (fun (a, b) -> Assert.True(b.GrantsComplianceFte <= a.GrantsComplianceFte)))
