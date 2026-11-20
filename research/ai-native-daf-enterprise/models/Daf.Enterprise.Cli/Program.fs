/// Regenerates the model outputs used by 09-financial-models and 11-scenarios-and-validation.
/// Usage: dotnet run --project Daf.Enterprise.Cli -- <workstream-dir>
open System.IO
open Daf.Enterprise.Economics
open Daf.Enterprise.Report

[<EntryPoint>]
let main argv =
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
    printfn "wrote outputs to %s and %s" out09 out11
    0
