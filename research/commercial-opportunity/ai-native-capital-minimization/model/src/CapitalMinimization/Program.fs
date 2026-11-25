/// Runs every analysis of the capital-minimization extension and writes Markdown and CSV. The only module with I/O.
module CapitalMinimization.Program

open System.IO
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Analysis
open ServicingEconomics.Parameters
open ServicingEconomics.Render
open CapitalMinimization.Design
open CapitalMinimization.Layers
open CapitalMinimization.Development
open CapitalMinimization.Designs
open CapitalMinimization.Sequences

/// Markdown table with pipes inside cells escaped (scenario names contain " | ").
let table headers rows = ServicingEconomics.Render.table headers (rows |> List.map (List.map (fun (c: string) -> c.Replace("|", "\\|"))))
let section title body = $"## {title}\n\n{body}\n"
let shape n b = equalSponsors n (sponsor "sponsor" 1000.0 b)
let optMonth = function Some m -> string m | None -> "not within horizon"
let optPct = function Some v -> pct v | None -> "n/a"

/// A stress that injects a fixed annual charge (layer allocation) as an extraordinary cost.
let charge amount = { noStress with Name = "layer charge"; ExtraordinaryCost = amount }

let evalD d target pr stress ss = (evaluateDesign d target pr stress ss).Base

// ---------------------------------------------------------------- 1 baseline (previous study, unchanged)

let baselineSection () =
    let fixedB = (evaluate modelB sponsorActivities AiNative (price 20.0) noStress []).TotalCost
    let fixedA = (evaluate modelA sponsorActivities AiNative (price 20.0) noStress []).TotalCost
    let be org = snd (assetsForMargin (fun ss -> evaluate org sponsorActivities AiNative (price 20.0) noStress ss) (shape 5 250000.0) 0.0)
    let plans =
        [ ServicingEconomics.Strategies.anchor
          ServicingEconomics.Strategies.anchorFounderLed
          ServicingEconomics.Strategies.unboundScaleBuild ServicingEconomics.Strategies.anchor ]
    let planRows =
        plans |> List.map (fun p ->
            let rows = ServicingEconomics.CashFlow.simulate p
            [ p.Name; money (ServicingEconomics.CashFlow.capitalRequired rows); optMonth (ServicingEconomics.CashFlow.monthsToProfit rows) ])
    section "1. Previous study baseline (reproduced, unchanged)"
        (table [ "Measure"; "Value" ]
            [ [ "Model A fixed annual cost (economic, no sponsors)"; money fixedA ]
              [ "Model B fixed annual cost (no sponsors)"; money fixedB ]
              [ "Model A break-even, 5 sponsors, $250k balance, 20 bps"; optMoney (be modelA) ]
              [ "Model B break-even, 5 sponsors, $250k balance, 20 bps"; optMoney (be modelB) ]
              [ "Model B fully loaded break-even"; optMoney (be (fullyLoaded modelB)) ] ]
         + "\n\n" + table [ "Previous plan"; "Capital required (cash)"; "Month profitable" ] planRows)

// ---------------------------------------------------------------- 2 designs

let designRows () =
    designs |> List.map (fun d ->
        let r = evaluateDesign d 50.0 (price 20.0) noStress []
        let one = evaluateDesign d 50.0 (price 20.0) noStress ((shape 5 250000.0).Build 1.0e9)
        d, r, one)

let designSection () =
    let rows =
        designRows () |> List.map (fun (d, r, one) ->
            [ d.Name; string (List.length d.People); money r.Base.CorePersonnel; money r.ContractedCost
              money (r.Base.NonPersonnelFixed - r.ContractedCost - r.PerPersonCost - r.CoordinationCost); money r.CoordinationCost
              money r.Base.TotalCost; num 1 one.Headcount; num 1 one.ContractedFte; money one.Base.TotalCost; pct one.Base.OperatingMargin
              (if one.ControlFeasible then "yes" else "NO") + ": " + one.ControlNote ])
    section "2. Outcome-designed organizations: fixed cost and control feasibility (50 min/account-year, $1B in 5 sponsors at $250k)"
        (table [ "Design"; "Core people"; "Core payroll (economic)"; "Contracted"; "Non-personnel"; "Coordination"; "Fixed total"; "Employees at $1B"; "Contracted FTE at $1B"; "Total cost at $1B"; "Margin at $1B"; "Separation of duties at $1B" ] rows)

// ---------------------------------------------------------------- 3 break-even by design and handling target

let breakEvenData () =
    [ for d in designs do
        for t in handlingTargets do
            let f m = snd (assetsForMarginDesign d t (price 20.0) noStress (shape 5 250000.0) m)
            let fl m =
                let c = servicingCost Standalone baseLayers (fun x -> fixedCost x) d - fixedCost d
                snd (assetsForMarginDesign d t (price 20.0) (charge c) (shape 5 250000.0) m)
            yield d.Name, t, f 0.0, f 0.2, fl 0.0, fl 0.2 ]

let breakEvenSection data =
    section "3. Break-even assets by design and handling target (20 bps, 5 equal sponsors, $250k average balance)"
        ("Operating = the design alone. Standalone = plus Unbound build amortisation, Echelon's Unbound share and maintenance not done by the design's own engineers (Layer views, section 7).\n\n"
         + table [ "Design"; "Minutes/account-yr"; "Operating break-even"; "Operating 20% margin"; "Standalone break-even"; "Standalone 20% margin" ]
            (data |> List.map (fun (n, t, a, b, c, e) -> [ n; num 0 t; optMoney a; optMoney b; optMoney c; optMoney e ])))

// ---------------------------------------------------------------- 4 handling targets at $1B

let targetSection () =
    let rows =
        [ for d in [ f3; f5; f8 ] do
            for t in handlingTargets do
                let r = evaluateDesign d t (price 20.0) noStress ((shape 5 250000.0).Build 1.0e9)
                yield [ d.Name; num 0 t; num 1 r.HumanMinutesPerAccount; num 0 r.Base.ServicingHours; num 2 r.Base.AddedServicingFte; num 1 r.Headcount; num 1 r.ContractedFte; money r.Base.PeakCost; money r.Base.TotalCost; pct r.Base.OperatingMargin ] ]
    section "4. Handling-time targets at $1B (5 sponsors, 4,000 accounts)"
        ("Human minutes per account include sponsor-level, relationship and integration hours spread over accounts.\n\n"
         + table [ "Design"; "Account minutes target"; "All human minutes/account"; "Hours"; "Added FTE"; "Employees"; "Contracted FTE"; "December peak cost"; "Total cost"; "Margin" ] rows)

// ---------------------------------------------------------------- 5 tails, peaks, simultaneous stress

let tailSection () =
    let stresses =
        [ noStress
          { noStress with Name = "exceptions/volume x1.5"; VolumeFactor = 1.5 }
          { noStress with Name = "handling minutes x2 (tail-heavy book)"; MinutesFactor = 2.0 }
          { noStress with Name = "December + $250k incident + absence (minutes x1.3, wages x1.1)"; MinutesFactor = 1.3; WageFactor = 1.1; ExtraordinaryCost = 250000.0 }
          { noStress with Name = "market -30%"; AssetFactor = 0.7 }
          { noStress with Name = "severe: -40% market, lose largest, minutes x1.5, incident $500k"; AssetFactor = 0.6; DropLargestSponsor = true; MinutesFactor = 1.5; ExtraordinaryCost = 500000.0 } ]
    let rows =
        [ for d in [ f3; f5 ] do
            for st in stresses do
                let r = evaluateDesign d 50.0 (price 20.0) st ((shape 5 250000.0).Build 1.5e9)
                yield [ d.Name; st.Name; money r.Base.Revenue; money r.Base.TotalCost; money r.Base.OperatingProfit; pct r.Base.OperatingMargin; num 1 r.Headcount ] ]
    let survive =
        [ for d in [ f3; f5 ] do
            for st in stresses |> List.tail do
                yield [ d.Name; st.Name; optMoney (snd (assetsForMarginDesign d 50.0 (price 20.0) st (shape 5 250000.0) 0.0)) ] ]
    section "5. Workload tails, seasonal peaks and simultaneous stresses ($1.5B, 5 sponsors)"
        (table [ "Design"; "Stress"; "Revenue"; "Cost"; "Profit"; "Margin"; "Headcount" ] rows
         + "\n\nAssets needed to break even under each stress (operating):\n\n"
         + table [ "Design"; "Stress"; "Break-even assets" ] survive)

// ---------------------------------------------------------------- 6 ratio-based vs workload-driven staffing

let ratioSection () =
    let rows =
        [ for accounts in [ 2500.0; 5000.0; 10000.0; 20000.0; 40000.0 ] do
            let ss = (shape 5 250000.0).Build (accounts * 250000.0)
            let prior = evaluate modelB sponsorActivities AiNative (price 20.0) noStress ss
            let now = evaluateDesign f5 50.0 (price 20.0) noStress ss
            yield [ num 0 accounts; money (accounts * 250000.0); num 1 (5.0 + prior.AddedServicingFte); money (prior.StepFixed); money prior.TotalCost; num 1 now.Headcount; money now.Base.TotalCost; money (prior.TotalCost - now.Base.TotalCost) ] ]
    section "6. Ratio-based (previous Model B) vs workload-driven (F5) staffing, 5 sponsors at $250k"
        ("Previous step rules add an operations manager, integration engineer, implementation analyst, fund accountant and compliance officer by ratio; F5 adds pool capacity only when hours require it. Both use the previous study's AI-native minutes (F5 at 50 min plus sponsor-level work).\n\n"
         + table [ "Accounts"; "Assets"; "Previous headcount (core + added ops)"; "Previous step-rule cost"; "Previous total cost"; "F5 headcount"; "F5 total cost"; "Difference" ] rows)

// ---------------------------------------------------------------- 7 three layers

let layerSection () =
    let ss = (shape 5 250000.0).Build 1.0e9
    let total d = (evaluateDesign d 50.0 (price 20.0) noStress ss).Base.TotalCost
    let revenue = (evaluateDesign f5 50.0 (price 20.0) noStress ss).Base.Revenue
    let rows =
        [ for d in [ f3; f5 ] do
            for v, name in [ Standalone, "standalone"; Incremental, "incremental (Unbound and Echelon exist anyway)"; FullyAllocated, "fully allocated (servicing share 100%)" ] do
                let c = servicingCost v baseLayers total d
                yield [ d.Name; name; money c; money (revenue - c); pct ((revenue - c) / revenue) ] ]
    let half = { baseLayers with ServicingShareOfUnbound = 0.5; UnboundExternalRevenue = 300000.0 }
    let rowsHalf =
        [ for d in [ f5 ] do
            let c = servicingCost FullyAllocated half total d
            yield [ d.Name; "fully allocated, servicing 50% of Unbound use, $300k external licence revenue"; money c; money (revenue - c); pct ((revenue - c) / revenue) ] ]
    let consolidatedRow =
        let costEx = total (servicingOnly f5)
        [ "Consolidated A+B+C (F5 servicing-only + Unbound + all of Echelon)"; money (consolidated baseLayers revenue costEx) ]
    let incrementalUnbound =
        [ [ "Incremental annual cost of Unbound if Echelon exists (no displaced Echelon work)"; money (unboundIncremental baseLayers false) ]
          [ "Incremental annual cost of Unbound if it displaces other Echelon work"; money (unboundIncremental baseLayers true) ]
          [ "Incremental annual cost of servicing if Unbound exists (F5, $1B)"; money (servicingCost Incremental baseLayers total f5) ]
          consolidatedRow ]
    section "7. Three economic layers at $1B (5 sponsors, 50 min/account-year)"
        ($"Layer inputs [A]: Echelon {money baseLayers.EchelonAnnual}/yr with {pct baseLayers.EchelonShareToUnbound} to Unbound; Unbound build {money baseLayers.UnboundBuild} over {num 0 baseLayers.UnboundLifeYears} years, maintenance {money baseLayers.UnboundMaintenance}, non-production {money baseLayers.UnboundPlatformOps}; servicing-specific platform {money baseLayers.ServicingSpecificPlatform}.\n\n"
         + table [ "Design"; "View"; "Servicing cost"; "Profit"; "Margin" ] (rows @ rowsHalf)
         + "\n\n" + table [ "Measure"; "Annual" ] incrementalUnbound)

// ---------------------------------------------------------------- 8 development investment and productivity

let devData () =
    [ for inv in investmentScenarios do
        for m in productivityMultiples do
            yield inv, m, deliverableScope unboundBaseline inv m, safeToOperate unboundBaseline inv m, minimumProductCost unboundBaseline m ]

let devSection data =
    let ceilingRow = $"Savings ceiling as productivity → ∞: {pct (savingsCeiling unboundBaseline)} of conventional cost (construction share {pct unboundBaseline.ConstructionShare}, compute {pct unboundBaseline.ComputeShareOfReplaced} of replaced construction)."
    let minRows = productivityMultiples |> List.map (fun m -> [ num 1 m; money (minimumProductCost unboundBaseline m); money (effectiveCost unboundBaseline 1.0 m + unboundBaseline.SafetyFloor); money (annualMaintenance unboundBaseline 0.2 unboundBaseline.MinimumScopeShare m) ])
    section "8. Development investment scenarios and productivity sensitivity"
        (ceilingRow + "\n\n"
         + table [ "Productivity multiple"; "Minimum safe servicing product"; "Full Unbound scope"; "Annual maintenance (minimum scope, 20%)" ] minRows
         + $"\n\nSequences use the minimum safe product at {num 1 baseMultiple}x: {money minimumBuild}; narrow non-custodial service {money narrowBuild}; extension to administration {money extensionBuild}.\n\n"
         + table [ "Investment"; "Multiple"; "Share of full Unbound scope deliverable"; "Covers minimum safe product?" ]
            (data |> List.map (fun (i, m, s, ok, _) -> [ money i; num 1 m; pct s; (if ok then "yes" else "no") ])))

// ---------------------------------------------------------------- 9 sequences and 10 failures

let seqRow (s: Sequence) =
    let rows = simulate s
    let at h = rows |> List.tryFind (fun r -> r.Month = h - 1) |> Option.map (fun r -> money r.Cumulative) |> Option.defaultValue "n/a"
    [ s.Name; money (capitalRequired rows); optMonth (monthsToProfit rows); at 24; at 36; at 60; money (finalYearProfit rows); optPct (roic rows) ]

let seqData () = sequences |> List.map (fun s -> s, seqRow s, seqRow (economic s))

let seqSection data =
    section "9. Sequences A-G (60 months, cash view; economic view below)"
        (table [ "Sequence"; "Capital required"; "Month profitable"; "Cash month 24"; "Cash month 36"; "Cash month 60"; "Year-5 profit"; "Year-5 ROIC" ] (data |> List.map (fun (_, a, _) -> a))
         + "\n\nEconomic view (founders at market):\n\n"
         + table [ "Sequence"; "Capital required"; "Month profitable"; "Cash month 24"; "Cash month 36"; "Cash month 60"; "Year-5 profit"; "Year-5 ROIC" ] (data |> List.map (fun (_, _, e) -> e)))

let failureData () =
    [ for s in sequences do
        let baseRows = simulate s
        let cap0 = capitalRequired baseRows
        let m0 = monthsToProfit baseRows
        for f in failures do
            let s2 = f s
            let rows = simulate s2
            yield s.Name, s2.Name.Substring(s.Name.Length + 3), cap0, capitalRequired rows, m0, monthsToProfit rows, finalYearProfit rows ]

let failureSection data =
    let delta (a: int option) (b: int option) =
        match a, b with
        | Some x, Some y -> $"+{y - x}" |> fun t -> if y - x < 0 then string (y - x) else t
        | Some _, None -> "never (within 60)"
        | None, Some _ -> "improves"
        | None, None -> "n/a"
    section "10. Cost of being wrong: failure modifiers on each sequence"
        (table [ "Sequence"; "Failure"; "Base capital"; "Capital if wrong"; "Extra capital"; "Months to profit change"; "Year-5 profit if wrong" ]
            (data |> List.map (fun ((s: string), f, c0, c1, m0, m1, p) -> [ s.Split(':').[0]; f; money c0; money c1; money (c1 - c0); delta m0 m1; money p ])))

// ---------------------------------------------------------------- 11 pricing structures on F5

let pricingSection () =
    let prices =
        [ "20 bps", price 20.0
          "lesser of 20 bps or $737/account", { price 20.0 with PerAccountMaximum = 737.0 }
          "10 bps + $150/account", { price 10.0 with PerAccountFee = 150.0 }
          "20 bps, $250/account floor", { price 20.0 with PerAccountMinimum = 250.0 }
          "15 bps", price 15.0
          "25 bps", price 25.0 ]
    let rows =
        [ for name, p in prices do
            for b in [ 100000.0; 250000.0; 500000.0; 1000000.0 ] do
                let be = snd (assetsForMarginDesign f5 50.0 p noStress (shape 5 b) 0.0)
                let r = evaluateDesign f5 50.0 p noStress ((shape 5 b).Build 1.5e9)
                yield [ name; money b; optMoney be; money r.Base.Revenue; pct r.Base.OperatingMargin ] ]
    section "11. Pricing structures on F5 (50 min, 5 sponsors)"
        (table [ "Price"; "Average balance"; "Operating break-even"; "Revenue at $1.5B"; "Margin at $1.5B" ] rows)

// ---------------------------------------------------------------- outputs

let csvOut (be: (string * float * float option * float option * float option * float option) list) dev seqs fails =
    let o = function Some (v: float) -> num 0 v | None -> ""
    let om = function Some (v: int) -> string v | None -> ""
    [ "design-breakeven.csv",
      csv [ "design"; "minutes_per_account_year"; "operating_breakeven_assets"; "operating_20pct_margin_assets"; "standalone_breakeven_assets"; "standalone_20pct_margin_assets" ]
          (be |> List.map (fun (n, t, a, b, c, e) -> [ n; num 0 t; o a; o b; o c; o e ]))
      "development-scenarios-model.csv",
      csv [ "investment_usd"; "productivity_multiple"; "share_of_full_scope"; "covers_minimum_safe_product"; "minimum_safe_product_cost" ]
          (dev |> List.map (fun (i, m, s, ok, c) -> [ num 0 i; num 1 m; num 3 s; (if ok then "Y" else "N"); num 0 c ]))
      "sequences.csv",
      csv [ "sequence"; "view"; "capital_required"; "month_profitable"; "cash_m24"; "cash_m36"; "cash_m60"; "year5_profit"; "year5_roic" ]
          (seqs |> List.collect (fun (s: Sequence, _, _) ->
              [ s, "cash"; economic s, "economic" ] |> List.map (fun (x, v) ->
                  let rows = simulate x
                  let at h = rows |> List.tryFind (fun r -> r.Month = h - 1) |> Option.map (fun r -> num 0 r.Cumulative) |> Option.defaultValue ""
                  [ s.Name; v; num 0 (capitalRequired rows); om (monthsToProfit rows); at 24; at 36; at 60; num 0 (finalYearProfit rows); (match roic rows with Some r -> num 3 r | None -> "") ])))
      "failure-costs.csv",
      csv [ "sequence"; "failure"; "base_capital"; "capital_if_wrong"; "extra_capital"; "base_month_profitable"; "month_profitable_if_wrong"; "year5_profit_if_wrong" ]
          (fails |> List.map (fun (s, f, c0, c1, m0, m1, p) -> [ s; f; num 0 c0; num 0 c1; num 0 (c1 - c0); om m0; om m1; num 0 p ])) ]

[<EntryPoint>]
let main argv =
    let outDir = if argv.Length > 0 then argv.[0] else "out"
    Directory.CreateDirectory outDir |> ignore
    let be = breakEvenData ()
    let dev = devData ()
    let seqs = seqData ()
    let fails = failureData ()
    let md =
        String.concat "\n"
            [ "# Capital-minimization model results\n\nGenerated by `dotnet run --project src/CapitalMinimization`. Theoretical scenarios from labelled assumptions (Designs.fs, Sequences.fs); not forecasts. The previous study's model is reused unchanged as the baseline.\n"
              baselineSection ()
              designSection ()
              breakEvenSection be
              targetSection ()
              tailSection ()
              ratioSection ()
              layerSection ()
              devSection dev
              seqSection seqs
              failureSection fails
              pricingSection () ]
    File.WriteAllText(Path.Combine(outDir, "results.md"), md)
    csvOut be dev seqs fails |> List.iter (fun (n, t) -> File.WriteAllText(Path.Combine(outDir, n), t))
    printfn "wrote %s" outDir
    0
