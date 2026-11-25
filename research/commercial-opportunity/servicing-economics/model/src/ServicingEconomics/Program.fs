/// Runs every analysis and writes Markdown tables and CSV files. The only module with I/O.
module ServicingEconomics.Program

open System.IO
open ServicingEconomics.Domain
open ServicingEconomics.Economics
open ServicingEconomics.Analysis
open ServicingEconomics.Parameters
open ServicingEconomics.Render

let approaches = [ Conventional; AiEnhanced; AiNative; AiNativeWithElimination ]
let approachName = function
    | Conventional -> "conventional"
    | AiEnhanced -> "AI-enhanced"
    | AiNative -> "AI-native"
    | AiNativeWithElimination -> "AI-native + elimination"

let balances = [ 50000.0; 100000.0; 150000.0; 250000.0; 500000.0 ]
let scaleLevels = [ 100e6; 250e6; 500e6; 750e6; 1e9; 1.5e9; 2e9; 3e9; 5e9; 1e10 ]
let sponsorCounts = [ 1; 2; 5; 10; 20 ]
let margins = [ 0.0; 0.10; 0.20; 0.25; 0.30 ]

let eval org approach pr stress sponsors = evaluate org sponsorActivities approach pr stress sponsors

/// n equal sponsors with average balance b, scaled to total assets.
let shapeOf n b = equalSponsors n (sponsor "sponsor" 1000.0 b)

let section title body = $"## {title}\n\n{body}\n"

// ---------------------------------------------------------------- analyses

let h0Check () =
    let r = evaluate h0Org h0Activities Conventional (price 20.0) noStress [ uniformSponsor "H0" 1.0e9 200000.0 ]
    section "H0 reproduction (prior memo)"
        (table [ "Assets"; "Revenue"; "Cost"; "Profit" ] [ [ money r.AverageAssets; money r.Revenue; money r.TotalCost; money r.OperatingProfit ] ])

let archetypeEconomics () =
    let rows =
        [ for a in archetypeTable do
            for ap in approaches do
                let s = { (sponsor a.Name 1000.0 a.AverageBalance) with Mix = [ { a with ShareOfAccounts = 1.0 } ] }
                let minutes, ext = perAccount ap [] s
                let pay = a.Payments ap
                let labour = minutes / 60.0 * opsHourly
                let variable = labour + a.External ap + pay
                for bps in [ 10.0; 20.0; 30.0 ] do
                    let fee = a.AverageBalance * bps / 10000.0
                    yield [ a.Name; approachName ap; num 0 a.AverageBalance; num 0 bps; num 1 minutes; num 2 labour; num 2 (ext - pay); num 2 pay; num 2 variable; num 2 fee; num 2 (fee - variable) ] ]
    rows

let breakEvenRows () =
    [ for org in organizations do
        for ap in [ Conventional; AiEnhanced; AiNative ] do
            for n in [ 1; 5 ] do
                for b in balances do
                    for bps in pricePoints do
                        let shape = shapeOf n b
                        let cells =
                            margins |> List.map (fun m -> snd (assetsForMargin (eval org ap (price bps) noStress) shape m))
                        yield org.Name, ap, n, b, bps, cells ]

let scaleRows org ap b bps =
    [ for n in sponsorCounts do
        for a in scaleLevels do
            let r = eval org ap (price bps) noStress ((shapeOf n b).Build a)
            yield n, a, r ]

let minimumPriceRows () =
    [ for org in organizations do
        for ap in [ AiEnhanced; AiNative ] do
            for a in [ 500e6; 1e9; 2e9; 5e9 ] do
                for b in [ 100000.0; 150000.0; 250000.0 ] do
                    let ss = (shapeOf 5 b).Build a
                    let f m = minimumBps (fun p -> eval org ap p noStress ss) (price 20.0) m
                    yield org.Name, ap, a, b, f 0.0, f 0.20, f 0.30 ]

let stressRows org ap b bps assets n =
    let ss = (shapeOf n b).Build assets
    standardStresses |> List.map (fun st -> st, eval org ap (price bps) st ss)

let surviveRows () =
    [ for org in organizations do
        for st in standardStresses |> List.filter (fun s -> s.Name <> "base") do
            for target in [ 0.0; 0.10 ] do
                let shape = shapeOf 5 150000.0
                let first = snd (assetsForMargin (eval org AiNative (price 20.0) st) shape target)
                yield org.Name, st.Name, target, first ]

/// Smallest contractual minimum annual fee at which one small sponsor stops losing money on its own
/// marginal contribution (one-time onboarding amortised over 5 years added to its annual cost).
let minimumFeeRows () =
    [ for accounts in [ 50.0; 150.0; 500.0; 1000.0; 2500.0; 5000.0 ] do
        for b in [ 50000.0; 150000.0; 500000.0 ] do
            let s0 = sponsor "small" accounts b
            let s = { s0 with AnnualSponsorCost = s0.AnnualSponsorCost + s0.OnboardingCost / 5.0 }
            let contribution p = let _, _, c = sponsorContribution modelB sponsorActivities AiNative p noStress s in c
            let assets = sponsorAssets 1.0 s
            yield accounts, b, assets, contribution (price 20.0), breakEvenMinimumFee contribution (price 20.0) ]


// ---------------------------------------------------------------- sponsor dataset (SPN pass) through this model

type SponsorRow = Map<string, string>

let readCsv (path: string) : SponsorRow list =
    use parser = new Microsoft.VisualBasic.FileIO.TextFieldParser(path)
    parser.SetDelimiters([| "," |])
    parser.HasFieldsEnclosedInQuotes <- true
    let header = parser.ReadFields()
    [ while not parser.EndOfData do
        let f = parser.ReadFields()
        yield Seq.zip header f |> Map.ofSeq ]

let field (r: SponsorRow) k = r |> Map.tryFind k |> Option.defaultValue ""
let numField (r: SponsorRow) k =
    match System.Double.TryParse(field r k, System.Globalization.NumberStyles.Float, inv) with
    | true, v -> Some v
    | _ -> None

/// Complexity multiplier on handling minutes: community foundations with material non-DAF funds and
/// sponsors flagged complex (international, faith, complex assets) 1.25; otherwise 1.0. [A]
let complexityOf (r: SponsorRow) =
    if field r "non_daf_assets_indicator" = "high" || (field r "complexity_flags").Length > 0 then 1.25 else 1.0

let sponsorEconomicsCsv (rows: SponsorRow list) =
    let header =
        [ "ein"; "name"; "segment"; "status"; "captive_status"; "recent_migration"; "avg_assets_proxy"; "accounts_for_cost"; "avg_balance_proxy"
          "complexity_multiplier"; "minutes_per_account_ai_native"; "annual_cost_ai_native_base"; "annual_cost_ai_native_high"; "annual_cost_ai_enhanced"
          "fee_10bps"; "fee_15bps"; "fee_20bps"; "fee_25bps"; "contribution_20bps_base"; "contribution_20bps_high"; "contribution_20bps_ai_enhanced"
          "breakeven_bps_base"; "breakeven_bps_high"; "minimum_fee_for_zero_contribution_20bps"; "covers_model_b_fixed_alone_20bps"; "basis" ]
    let modelBFixed = (evaluate modelB sponsorActivities AiNative (price 20.0) noStress []).TotalCost
    let body =
        [ for r in rows do
            match numField r "avg_assets_proxy", numField r "accounts_for_cost" with
            | Some assets, Some accounts when assets > 0.0 && accounts > 0.0 ->
                let b = assets / accounts
                let s0 = { (sponsor (field r "name") accounts b) with ComplexityMultiplier = complexityOf r }
                let s = { s0 with AnnualSponsorCost = s0.AnnualSponsorCost + s0.OnboardingCost / 5.0 }
                let contrib ap stress p = sponsorContribution modelB sponsorActivities ap p stress s
                let cost ap stress = let _, c, _ = contrib ap stress (price 20.0) in c
                let high = { noStress with MinutesFactor = minutesHighFactor }
                let con ap stress bps = let _, _, c = contrib ap stress (price bps) in c
                let beBps stress = [ for i in 1 .. 1000 -> float i / 10.0 ] |> List.tryFind (fun bps -> con AiNative stress bps >= 0.0)
                let minFee = breakEvenMinimumFee (fun p -> let _, _, c = contrib AiNative noStress p in c) (price 20.0)
                let minutes, _ = perAccount AiNative sponsorActivities s
                yield
                    [ field r "ein"; field r "name"; field r "segment"; field r "status"; field r "captive_status"; field r "recent_migration"
                      num 0 assets; num 0 accounts; num 0 b; num 2 s.ComplexityMultiplier; num 1 minutes
                      num 0 (cost AiNative noStress); num 0 (cost AiNative high); num 0 (cost AiEnhanced noStress)
                      num 0 (assets * 10.0 / 10000.0); num 0 (assets * 15.0 / 10000.0); num 0 (assets * 20.0 / 10000.0); num 0 (assets * 25.0 / 10000.0)
                      num 0 (con AiNative noStress 20.0); num 0 (con AiNative high 20.0); num 0 (con AiEnhanced noStress 20.0)
                      (match beBps noStress with Some v -> num 1 v | None -> ">100"); (match beBps high with Some v -> num 1 v | None -> ">100")
                      (match minFee with Some v -> num 0 v | None -> ">2000000")
                      (if con AiNative noStress 20.0 >= modelBFixed then "yes" else "no")
                      "marginal contribution: fees less vendor cost, servicing hours at $65.45/h, $12k sponsor cost and onboarding/5; fixed and step costs excluded; avg assets are the (BOY+EOY)/2 proxy" ]
            | _ -> () ]
    csv header body, modelBFixed


// ---------------------------------------------------------------- hybrid pricing and strategies

/// Five equal sponsors at $1.5B total and $150k average balance, AI-native, Model B, under pricing structures.
let hybridRows () =
    let structures =
        [ "flat 15 bps", price 15.0
          "flat 20 bps", price 20.0
          "flat 25 bps", price 25.0
          "20 bps, $250 per-account floor", { price 20.0 with PerAccountMinimum = 250.0 }
          "15 bps, $250 per-account floor", { price 15.0 with PerAccountMinimum = 250.0 }
          "20 bps, $150k sponsor minimum", { price 20.0 with MinimumAnnualFee = 150000.0 }
          "20 bps, payments passed through at cost", { price 20.0 with PaymentsPassThrough = true }
          "20 bps + $250 floor + payments passed through", { price 20.0 with PerAccountMinimum = 250.0; PaymentsPassThrough = true } ]
    [ for b in [ 75000.0; 150000.0; 300000.0 ] do
        for assets in [ 750e6; 1.5e9; 3e9 ] do
            for name, pr in structures do
                let r = eval modelB AiNative pr noStress ((shapeOf 5 b).Build assets)
                let shocked = eval modelB AiNative pr { noStress with AssetFactor = 0.7 } ((shapeOf 5 b).Build assets)
                yield [ money b; money assets; name; money r.Revenue; money r.OperatingProfit; pct r.OperatingMargin; money shocked.OperatingProfit; pct shocked.OperatingMargin ] ]

let strategyRows () =
    let plans =
        Strategies.strategies
        @ [ Strategies.delayed Strategies.anchor; Strategies.delayed Strategies.multipleSmaller
            Strategies.costlyBuild Strategies.anchor; Strategies.costlyBuild Strategies.softwareFirst
            Strategies.economicView Strategies.anchorFounderLed
            Strategies.aiEnhancedOnly Strategies.anchor; Strategies.aiEnhancedOnly Strategies.multipleSmaller
            Strategies.hybridPriced Strategies.multipleSmaller; Strategies.hybridPriced Strategies.adminFirst ]
    [ for p in plans do
        let rows = CashFlow.simulate p
        let cap = CashFlow.capitalRequired rows
        let at = CashFlow.cumulativeAt rows [ 6; 12; 18; 24; 36; 60 ] |> List.map (snd >> function Some v -> money v | None -> "n/a")
        let profitMonth = CashFlow.monthsToProfit rows |> Option.map string |> Option.defaultValue "not by month 60"
        let last = rows |> List.last
        yield [ p.Name; money cap; money (cap * 1.25) ] @ at @ [ profitMonth; money (last.AccruedProfit * 12.0) ] ]

// ---------------------------------------------------------------- render

let renderAll () =
    let be = breakEvenRows ()
    let beTable org ap n =
        table ("Average balance" :: "bps" :: (margins |> List.map (fun m -> $"AUA at {pct m} margin")))
            [ for (o, a, nn, b, bps, cells) in be do
                if o = org && a = ap && nn = n then
                    yield money b :: num 0 bps :: (cells |> List.map optMoney) ]
    let scaleTable org ap b bps =
        table [ "Sponsors"; "Average AUA"; "Accounts"; "Revenue"; "Total cost"; "Operating profit"; "Margin"; "Contribution margin"; "Added ops FTE"; "Step-fixed" ]
            [ for (n, a, r) in scaleRows org ap b bps -> [ string n; money a; num 0 r.Accounts; money r.Revenue; money r.TotalCost; money r.OperatingProfit; pct r.OperatingMargin; pct r.ContributionMargin; num 0 r.AddedServicingFte; money r.StepFixed ] ]
    let stressTable org ap b bps assets n =
        table [ "Stress"; "Revenue"; "Total cost"; "Operating profit"; "Margin" ]
            [ for (st, r) in stressRows org ap b bps assets n -> [ st.Name; money r.Revenue; money r.TotalCost; money r.OperatingProfit; pct r.OperatingMargin ] ]
    let mp = minimumPriceRows ()
    let optBps = function Some v -> num 1 v | None -> "> 100"
    let sv = surviveRows ()
    let mf = minimumFeeRows ()
    let arch = archetypeEconomics ()
    let md =
        [ yield "# Servicing economics model results\n\nGenerated by `dotnet run --project src/ServicingEconomics -c Release -- out`. Theoretical results from labelled assumptions (see `Parameters.fs` and the assumptions register); not forecasts. Assets are average billable assets under administration (AUA). Margins are operating margins before tax, interest, platform build amortisation and founder equity.\n"
          yield h0Check ()
          yield section "Unit economics per account-year by archetype (ops labour at $65.45/h)"
              (table [ "Archetype"; "Approach"; "Balance"; "bps"; "Minutes"; "Labour"; "Other external"; "Payments"; "Variable cost"; "Fee"; "Fee less variable" ] arch)
          for org in organizations do
              for ap in [ AiNative; AiEnhanced; Conventional ] do
                  yield section $"Break-even and target-margin AUA: {org.Name}, {approachName ap}, one sponsor" (beTable org.Name ap 1)
              yield section $"Break-even and target-margin AUA: {org.Name}, AI-native, five equal sponsors" (beTable org.Name AiNative 5)
          for org in organizations do
              yield section $"Scale: {org.Name}, AI-native, 20 bps, average balance $150k" (scaleTable org AiNative 150000.0 20.0)
          yield section "Scale: Model B, AI-enhanced, 20 bps, average balance $150k" (scaleTable modelB AiEnhanced 150000.0 20.0)
          yield section "Scale: Model B, AI-native, 20 bps, average balance $75k" (scaleTable modelB AiNative 75000.0 20.0)
          yield section "Minimum viable price (bps) for five equal sponsors"
              (table [ "Organization"; "Approach"; "AUA"; "Average balance"; "Break-even bps"; "bps for 20% margin"; "bps for 30% margin" ]
                  [ for (o, ap, a, b, z, t20, t30) in mp -> [ o; approachName ap; money a; money b; optBps z; optBps t20; optBps t30 ] ])
          for org in organizations do
              yield section $"Stress test: {org.Name}, AI-native, 20 bps, $1.5B AUA, five sponsors, average balance $150k" (stressTable org AiNative 150000.0 20.0 1.5e9 5)
          yield section "Starting AUA needed to stay at or above the margin after each stress (AI-native, 20 bps, five sponsors, $150k)"
              (table [ "Organization"; "Stress"; "Margin floor"; "Starting AUA" ] [ for (o, s, t, a) in sv -> [ o; s; pct t; optMoney a ] ])
          yield section "Pricing structures: Model B, AI-native, five equal sponsors (operating profit, and after a 30% asset fall)"
              (table [ "Average balance"; "AUA"; "Structure"; "Revenue"; "Operating profit"; "Margin"; "Profit after -30%"; "Margin after -30%" ] (hybridRows ()))
          yield section "Market-entry strategies: monthly cash flow over 60 months (capital = deepest cumulative cash trough; +25% buffer shown)"
              (table [ "Plan"; "Capital required"; "With 25% buffer"; "Cash at m6"; "m12"; "m18"; "m24"; "m36"; "m60"; "Month profit turns sustainably positive"; "Run-rate annual profit at m60" ] (strategyRows ()))
          yield section "Contractual minimum fee that stops a single sponsor losing money (Model B, AI-native, 20 bps, onboarding amortised over 5 years)"
              (table [ "Accounts"; "Average balance"; "AUA"; "Contribution at 20 bps"; "Break-even minimum annual fee" ]
                  [ for (n, b, a, c, m) in mf -> [ num 0 n; money b; money a; money c; (match m with Some v -> money v | None -> "> $2M") ] ]) ]
    String.concat "\n" md

[<EntryPoint>]
let main argv =
    let outDir = if argv.Length > 0 then argv.[0] else "out"
    Directory.CreateDirectory outDir |> ignore
    File.WriteAllText(Path.Combine(outDir, "results.md"), renderAll ())
    printfn "wrote %s" (Path.Combine(outDir, "results.md"))
    if argv.Length > 1 then
        let text, fixedCost = sponsorEconomicsCsv (readCsv argv.[1])
        File.WriteAllText(Path.Combine(outDir, "sponsor-model-economics.csv"), text)
        printfn "wrote sponsor-model-economics.csv (Model B fixed incl. minimum ops: %.0f)" fixedCost
    0
