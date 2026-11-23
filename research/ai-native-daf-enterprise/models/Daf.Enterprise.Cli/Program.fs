/// Regenerates the model outputs used by 09-financial-models and 11-scenarios-and-validation.
/// Usage: dotnet run --project Daf.Enterprise.Cli -- <workstream-dir>
open System.IO
open Daf.Enterprise.Economics
open Daf.Enterprise.Report

/// Public-data charity-vetting benchmarks (heavy; run separately):
///   dotnet run --project Daf.Enterprise.Cli -- --vetting <workstream-dir> <bmf-dir> <ofac-dir> <full-lines-csv>
let runVetting (root: string) (bmfDir: string) (ofacDir: string) (fullLines: string) =
    let outDir = Path.Combine(root, "charity-vetting-ai", "results")
    Directory.CreateDirectory outDir |> ignore
    let sample = Path.Combine(root, "..", "..", "data", "charity-vetting-ai", "resolution-eval-sample.csv")
    let (resCsv, consistency, ix) = Daf.Experiments.ExperimentReport.vettingResolution bmfDir sample
    File.WriteAllText(Path.Combine(outDir, "v1-resolution.csv"), resCsv)
    File.WriteAllText(Path.Combine(outDir, "v1-label-consistency.csv"), consistency)
    let (screenCsv, nEntries) = Daf.Experiments.ExperimentReport.vettingScreening ix ofacDir fullLines
    File.WriteAllText(Path.Combine(outDir, "v2-sanctions-screening.csv"), screenCsv)
    printfn "vetting outputs written to %s (OFAC entries incl. aliases: %d)" outDir nEntries
    0

[<EntryPoint>]
let main argv =
  if argv.Length >= 5 && argv.[0] = "--vetting" then runVetting argv.[1] argv.[2] argv.[3] argv.[4]
  else
    let root = if argv.Length > 0 then argv.[0] else ".."
    let out09 = Path.Combine(root, "09-financial-models", "outputs")
    let out11 = Path.Combine(root, "11-scenarios-and-validation", "outputs")
    Directory.CreateDirectory out09 |> ignore
    Directory.CreateDirectory out11 |> ignore
    let ps = defaults
    let baseScales = scales |> List.map baseScenario
    let smallBalance = scales |> List.map (fun n -> { baseScenario n with Label = $"{n:N0} accounts, $50k avg"; AvgBalance = 50000m })
    let largeBalance = scales |> List.map (fun n -> { baseScenario n with Label = $"{n:N0} accounts, $800k avg"; AvgBalance = 800000m })
    let write dir name text = File.WriteAllText(Path.Combine(dir, name), text)
    write out09 "parameter-register.csv" (parameterRegister ps)
    write out09 "scale-results.csv" (scaleResults ps (baseScales @ smallBalance @ largeBalance))
    write out09 "fte-by-role.csv" (fteByRoleTable ps baseScales)
    write out09 "cost-lines.csv" (costLines ps baseScales)
    write out09 "sensitivity-100k.csv" (sensitivityTable ps (baseScenario 100000m))
    write out09 "sensitivity-10k.csv" (sensitivityTable ps (baseScenario 10000m))
    write out09 "determination-reuse.csv" (reuseTable ps)
    write out09 "models-abcd.csv" (modelTable (modelGrid ps))
    let be label tmpl =
        match breakEvenAccounts ps tmpl with
        | Some n -> $"\"{label}\",{n}"
        | None -> $"\"{label}\",none <= 2000000"
    let beWith label ps' =
        match breakEvenAccounts ps' baseScenario with
        | Some n -> $"\"{label}\",{n}"
        | None -> $"\"{label}\",none <= 2000000"
    write out09 "break-even.csv"
        (String.concat "\n"
            [ "case,break_even_accounts"
              be "base: $300k avg balance" baseScenario
              be "$50k avg balance" (fun n -> { baseScenario n with AvgBalance = 50000m })
              be "$150k avg balance" (fun n -> { baseScenario n with AvgBalance = 150000m })
              be "$800k avg balance" (fun n -> { baseScenario n with AvgBalance = 800000m })
              beWith "base, CAC x2" { ps with CacPerNewAccount = { ps.CacPerNewAccount with Value = 800m } }
              beWith "base, loaded cost $250k per FTE" { ps with LoadedCostPerFteAiNative = { ps.LoadedCostPerFteAiNative with Value = 250000m } } ] + "\n")
    let (rampRows, peaks) = ramps ps
    write out09 "ramp-5yr.csv" rampRows
    write out09 "peak-capital.csv" peaks
    write out11 "twin-100k.csv" (twinTable ps (baseScenario 100000m) 42UL)
    write out11 "twin-10k.csv" (twinTable ps (baseScenario 10000m) 42UL)
    let outX = Path.Combine(root, "workflow-innovation", "08-experiments", "results")
    Directory.CreateDirectory outX |> ignore
    let seed = 20261120UL
    write outX "e1-verification.csv" (Daf.Experiments.ExperimentReport.e1 seed)
    write outX "e2-approval-architectures.csv" (Daf.Experiments.ExperimentReport.e2 seed)
    write outX "e3-disbursement.csv" (Daf.Experiments.ExperimentReport.e3 seed)
    write outX "e4-reconciliation.csv" (Daf.Experiments.ExperimentReport.e4 seed)
    write outX "e5-onboarding.csv" (Daf.Experiments.ExperimentReport.e5 ())
    write outX "e6-specialist-pooling.csv" (Daf.Experiments.ExperimentReport.e6 seed)
    write outX "e8-migration.csv" (Daf.Experiments.ExperimentReport.e8 ())
    write outX "e9-crash-recovery.csv" (Daf.Experiments.ExperimentReport.e9 ())
    write outX "e10-ai-triage.csv" (Daf.Experiments.ExperimentReport.e10 seed)
    let summaryPath = Path.Combine(root, "..", "..", "data", "workflow-innovation", "recipient-overlap-summary.csv")
    let (netCurve, netSens, infraModels, _) = Daf.Experiments.ExperimentReport.network summaryPath
    let out09wi = Path.Combine(root, "workflow-innovation", "09-economic-validation", "results")
    Directory.CreateDirectory out09wi |> ignore
    write out09wi "network-join-curve.csv" netCurve
    write out09wi "network-sensitivity.csv" netSens
    write out09wi "infrastructure-models.csv" infraModels
    let smallPath = Path.Combine(root, "..", "..", "data", "workflow-innovation", "small-sponsor-overlap-summary.csv")
    if File.Exists smallPath then
        write out09wi "small-sponsor-network.csv" (Daf.Experiments.ExperimentReport.smallNetwork summaryPath smallPath)
    printfn "wrote outputs to %s, %s, %s and %s" out09 out11 outX out09wi
    0
