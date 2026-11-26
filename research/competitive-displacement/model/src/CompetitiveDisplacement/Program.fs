/// I/O shell: reads inputs, runs the pure model, writes outputs; or validates the research package.
module CompetitiveDisplacement.Program

open System.IO
open CompetitiveDisplacement.Inputs
open CompetitiveDisplacement.Analysis

let private readRows dir file = File.ReadAllText(Path.Combine(dir, file)) |> Csv.parse |> snd

let loadInputs (dir: string) : Result<Inputs, string list> =
    let rows = readRows dir
    let one f file = rows file |> List.map f |> collect
    match one parseEvent "events.csv", one parseMode "enterprise-modes.csv", parseParams (rows "parameters.csv"),
          one parseComponent "registry-components.csv", one parseAlt "registry-alternatives.csv",
          parseParams (rows "registry-parameters.csv"), one parseRoute "entry-routes.csv" with
    | Ok e, Ok m, Ok p, Ok c, Ok a, Ok rp, Ok r ->
        Ok { Events = e; Modes = m; Params = p; Components = c; Alts = a; RegistryParams = rp; Routes = r }
    | e, m, p, c, a, rp, r ->
        let errs x = match x with Error es -> es | Ok _ -> []
        Error(errs e @ errs m @ errs p @ errs c @ errs a @ errs rp @ errs r)

let seed = 20261126UL
let draws = 2000

/// All output files as (relative name, content). Pure given inputs.
let outputs (inputs: Inputs) : (string * string) list =
    let vals = baseVals inputs
    let be = breakEvenGrid inputs vals
    let mc = monteCarlo draws seed 0.0 inputs
    let mcc = monteCarlo draws seed 0.5 inputs
    let st = stress inputs
    let dec = decomposition inputs vals
    let prev = preventionVsSpeed inputs vals
    let tor = tornado inputs "MD-5" 20.0 @ tornado inputs "MD-6" 20.0
    let par1, par5 = pareto inputs vals "MD-1", pareto inputs vals "MD-5"
    let recon = Registry.reconstruction Base inputs.Components
    let baseDrivers = { Registry.CharitiesPerSponsor = 20000.0; Registry.Sponsors = 1.0; Registry.ChangeRate = 0.04; Registry.RefreshDays = None; Registry.GrantsPerYear = 70000.0 }
    let rpBase = registryVals inputs Base
    let regBase = inputs.Alts |> List.map (fun a -> a.Name, Registry.cost a rpBase baseDrivers)
    let regMc = inputs.Alts |> List.map (fun a -> a.Id, registryMc draws seed inputs a baseDrivers)
    let grid = registryGrid inputs
    let lowest =
        grid
        |> List.filter (fun r -> r.ChangeRate = 0.04 && r.Alt <> "RA-0" && r.Alt <> "RA-6")
        |> List.groupBy (fun r -> r.Charities, r.Sponsors, r.Refresh)
        |> List.map (fun (_, rs) -> rs |> List.minBy (fun r -> r.Result.Total))
        |> List.sortBy (fun r -> r.Charities, r.Sponsors, r.Refresh)
    let routes = routeCases inputs
    let rmc = routeMc draws seed 0.0 inputs @ routeMc draws seed 0.5 inputs
    let regGridCsv =
        Csv.write [ "alt_id"; "charities_per_sponsor"; "sponsors"; "change_rate"; "refresh"; "grants"; "charities_in_use"; "exceptions"; "human_hours"; "run_cost"; "per_grant"; "per_sponsor"; "establishment" ]
            (grid |> List.map (fun r -> [ r.Alt; Csv.fmt r.Charities; Csv.fmt r.Sponsors; Csv.fmt r.ChangeRate; r.Refresh; Csv.fmt r.Grants; Csv.fmt r.Result.Charities; Csv.fmt r.Result.ExceptionsPerYear; Csv.fmt r.Result.HumanHours; Csv.fmt r.Result.Total; Csv.fmt r.Result.PerGrant; Csv.fmt r.Result.PerSponsor; Csv.fmt r.Result.Establishment ]))
    let routesCsv =
        Csv.write [ "route_id"; "case"; "capital"; "first_cash_positive_month"; "payback_month"; "cumulative_cash_m60"; "cumulative_cash_m120"; "live_customers_m60"; "annual_revenue_m60" ]
            (routes |> List.map (fun r -> [ r.RouteId; r.Case; Csv.fmt r.Result.Capital; (r.Result.FirstPositiveMonth |> Option.map string |> Option.defaultValue "none"); (r.Result.PaybackMonth |> Option.map string |> Option.defaultValue "none"); Csv.fmt r.Result.CumulativeAt60; Csv.fmt r.Result.CumulativeAt120; Csv.fmt r.Result.CustomersAt60; Csv.fmt r.Result.AnnualRevenueAt60 ]))
        + "\n"
        + Csv.write [ "route_id"; "rho"; "capital_p10"; "capital_p50"; "capital_p90"; "share_no_payback_120m"; "payback_month_p50" ] (rmc |> List.map (fun r -> [ r.RouteId; Csv.fmt r.Rho; Csv.fmt r.P10; Csv.fmt r.P50; Csv.fmt r.P90; Csv.fmt r.NoPayback120; Csv.fmt r.PaybackP50 ]))
    [ "event-costs-by-mode.csv", Render.eventCostsCsv inputs vals
      "mode-summary.csv", Csv.write Render.modeSummaryHeader (Render.modeSummaryRows inputs vals)
      "break-even-grid.csv", Render.breakEvenCsv be mc mcc
      "stress.csv", Csv.write [ "mode_id"; "base_break_even_20bps"; "stress_break_even_20bps"; "base_min_per_acct"; "stress_min_per_acct" ] (st |> List.map (fun r -> [ r.ModeId; Csv.fmt r.BaseAssets; Csv.fmt r.StressAssets; Csv.fmt r.BaseMinutes; Csv.fmt r.StressMinutes ]))
      "saving-decomposition.csv", Csv.write [ "step"; "from"; "to"; "saving_per_acct"; "minutes_saved_per_acct" ] (dec |> List.map (fun d -> [ d.Step; d.FromMode; d.ToMode; Csv.fmt d.SavingPerAcct; Csv.fmt d.MinutesSaved ]))
      "prevention-vs-speed.csv", Csv.write [ "event_id"; "event"; "prevention"; "prevention_value_per_acct"; "ai_speed_value_per_acct" ] (prev |> List.map (fun p -> [ p.EventId; p.Name; p.Prevention; Csv.fmt p.PreventionValue; Csv.fmt p.SpeedValue ]))
      "event-pareto.csv", Csv.write [ "mode_id"; "event_id"; "event"; "cost_per_acct"; "share"; "cumulative" ] ((par1 @ par5) |> List.map (fun r -> [ r.ModeId; r.EventId; r.Name; Csv.fmt r.CostPerAcct; Csv.fmt r.Share; Csv.fmt r.Cumulative ]))
      "tornado.csv", Csv.write [ "mode_id"; "param"; "low"; "high"; "break_even_at_low"; "break_even_at_high" ] (tor |> List.map (fun t -> [ t.ModeId; t.Param; Csv.fmt t.LowValue; Csv.fmt t.HighValue; Csv.fmt t.AtLow; Csv.fmt t.AtHigh ]))
      "registry-alternatives-grid.csv", regGridCsv
      "entry-route-capital.csv", routesCsv
      "results.md", Render.resultsMarkdown inputs vals be mc mcc st dec prev tor par1 par5 recon regBase regMc lowest routes rmc ]

let run (inputDir: string) (outDir: string) =
    match loadInputs inputDir with
    | Error es -> es |> List.iter (eprintfn "%s"); 1
    | Ok inputs ->
        Directory.CreateDirectory outDir |> ignore
        outputs inputs |> List.iter (fun (n, t) -> File.WriteAllText(Path.Combine(outDir, n), t))
        printfn "wrote %d files to %s" (outputs inputs |> List.length) outDir
        0

/// Recompute and compare with committed outputs.
let check (inputDir: string) (outDir: string) =
    match loadInputs inputDir with
    | Error es -> es |> List.iter (eprintfn "%s"); 1
    | Ok inputs ->
        let diffs = outputs inputs |> List.filter (fun (n, t) -> let p = Path.Combine(outDir, n) in not (File.Exists p) || File.ReadAllText p <> t)
        diffs |> List.iter (fun (n, _) -> eprintfn "differs: %s" n)
        if List.isEmpty diffs then printfn "check OK: outputs reproduce"; 0 else 1

let validate (root: string) =
    let files ext = Directory.GetFiles(root, ext, SearchOption.AllDirectories) |> Array.filter (fun p -> not (p.Contains "/bin/" || p.Contains "/obj/")) |> Array.sort |> Array.map (fun p -> p, File.ReadAllText p) |> List.ofArray
    let fs = { Validate.Csvs = files "*.csv"; Validate.Markdown = files "*.md"; Validate.Exists = fun p -> File.Exists p || Directory.Exists p }
    match Validate.validate root fs with
    | [] -> printfn "validate OK: %d CSV, %d Markdown files" fs.Csvs.Length fs.Markdown.Length; 0
    | errs -> errs |> List.iter (eprintfn "%s"); eprintfn "%d validation errors" errs.Length; 1

[<EntryPoint>]
let main argv =
    match List.ofArray argv with
    | [ "run"; i; o ] -> run i o
    | [ "check"; i; o ] -> check i o
    | [ "validate"; root ] -> validate root
    | _ -> eprintfn "usage: run <inputs> <outdir> | check <inputs> <outdir> | validate <package-root>"; 2
