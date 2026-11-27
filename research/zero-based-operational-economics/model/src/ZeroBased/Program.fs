/// I/O shell: loads inputs, runs the pure model, writes or checks outputs.
module ZeroBased.Program

open System.IO
open CompetitiveDisplacement.Inputs
open ZeroBased.Domain

let private rows (path: string) = File.ReadAllText path |> CompetitiveDisplacement.Csv.parse |> snd

let loadInputs (dataDir: string) : Result<Inputs, string list> =
    let mi f = Path.Combine(dataDir, "model-inputs", f)
    let rg f = Path.Combine(dataDir, "registers", f)
    let many f path = rows path |> List.map f |> collect
    match many parseActivity (rg "operational-activities.csv"), parseAssumptions (rows (mi "parameters.csv")),
          many parseRole (mi "roles.csv"), many parseConfig (mi "configurations.csv"), many parseFixed (mi "fixed-costs.csv"),
          many parseProgramme (mi "programmes.csv"), parseAssumptions (rows (mi "infrastructure-parameters.csv")),
          parseAssumptions (rows (mi "beneficium-parameters.csv")) with
    | Ok a, Ok p, Ok r, Ok c, Ok f, Ok pr, Ok i, Ok b ->
        Ok { Activities = a; Params = p; Roles = r; Configs = c; Fixed = f; Programmes = pr; Infra = i; Beneficium = b }
    | a, p, r, c, f, pr, i, b ->
        let errs x = match x with Error es -> es | Ok _ -> []
        Error(errs a @ errs p @ errs r @ errs c @ errs f @ errs pr @ errs i @ errs b)

[<EntryPoint>]
let main argv =
    match argv |> List.ofArray with
    | [ "run"; dataDir; baselineDir; outDir ] ->
        match loadInputs dataDir, Baseline.loadBaseline baselineDir with
        | Ok inputs, Ok baseline ->
            Directory.CreateDirectory outDir |> ignore
            Outputs.all inputs baseline |> List.iter (fun (name, content) -> File.WriteAllText(Path.Combine(outDir, name), content))
            printfn "wrote %d outputs to %s" (Outputs.all inputs baseline).Length outDir
            0
        | Error es, _ | _, Error es ->
            es |> List.iter (eprintfn "input error: %s")
            1
    | [ "check"; dataDir; baselineDir; outDir ] ->
        match loadInputs dataDir, Baseline.loadBaseline baselineDir with
        | Ok inputs, Ok baseline ->
            let diffs =
                Outputs.all inputs baseline
                |> List.filter (fun (name, content) ->
                    let p = Path.Combine(outDir, name)
                    not (File.Exists p) || File.ReadAllText p <> content)
            if diffs.IsEmpty then printfn "check OK: outputs reproduce"; 0
            else diffs |> List.iter (fun (n, _) -> eprintfn "differs: %s" n); 1
        | Error es, _ | _, Error es ->
            es |> List.iter (eprintfn "input error: %s")
            1
    | [ "validate"; packageDir ] ->
        let file f = Path.Combine(packageDir, f)
        let missing = Validate.deliverables |> List.filter (file >> File.Exists >> not) |> List.map (fun f -> $"missing deliverable {f}")
        let csvs = Directory.GetFiles(Path.Combine(packageDir, "data"), "*.csv", SearchOption.AllDirectories) |> Array.sort |> List.ofArray
        let widths = csvs |> List.collect (fun p -> Validate.csvWidths (Path.GetRelativePath(packageDir, p)) (File.ReadAllText p))
        let assumptionFiles = [ "parameters.csv"; "infrastructure-parameters.csv"; "beneficium-parameters.csv" ]
        let schema = assumptionFiles |> List.collect (fun f -> Validate.assumptions f (File.ReadAllText(Path.Combine(packageDir, "data", "model-inputs", f))))
        let mds = Directory.GetFiles(packageDir, "*.md", SearchOption.AllDirectories) |> Array.filter (fun p -> not (p.Contains "/bin/" || p.Contains "/obj/")) |> Array.sort |> List.ofArray
        let broken =
            mds |> List.collect (fun md ->
                Validate.links (File.ReadAllText md)
                |> List.filter (fun l -> let t = Path.GetFullPath(Path.Combine(Path.GetDirectoryName md, l)) in not (File.Exists t || Directory.Exists t))
                |> List.map (fun l -> $"{Path.GetRelativePath(packageDir, md)}: broken link {l}"))
        let disp = Validate.dispositions (File.ReadAllText(Path.Combine(packageDir, "data", "registers", "adversarial-findings.csv")))
        let errors = missing @ widths @ schema @ broken @ disp
        if errors.IsEmpty then
            printfn "validate OK: %d deliverables, %d CSV files, %d markdown files, links resolve, dispositions complete" Validate.deliverables.Length csvs.Length mds.Length
            0
        else
            errors |> List.iter (eprintfn "%s")
            1
    | _ ->
        eprintfn "usage: run|check <data-dir> <baseline-model-inputs-dir> <output-dir> | validate <package-dir>"
        2
