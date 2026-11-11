module EchelonFoundry.DafDecisionIntelligence.Program

open System
open System.IO
open EchelonFoundry.DafDecisionIntelligence

[<EntryPoint>]
let main argv =
    try
        let command = if argv.Length > 0 then argv.[0] else "validate"
        let root =
            if argv.Length > 1 then Path.GetFullPath(argv.[1])
            else Directory.GetCurrentDirectory()
        if command <> "validate" && command <> "render" then
            eprintfn "Usage: dotnet run --project src/DecisionIntelligence -- [validate|render] [repository-root]"
            2
        else
            let catalog = Catalog.load root
            let file = Path.Combine(root, "data/decision-intelligence-results-v1.json")
            let issues, decisions = Results.validate catalog (File.ReadAllText(file))
            if not issues.IsEmpty then
                for issue in issues do
                    eprintfn "FAIL %s [%s]: %s" issue.Code issue.Location issue.Detail
                eprintfn "Validation failed: %d issues" issues.Length
                1
            elif command = "render" then
                printf "%s" (Report.markdown catalog decisions)
                0
            else
                printfn "PASS: %d decisions; %d evidence records; %d verified citations; %d registered claims."
                    decisions.Length catalog.Evidence.Count catalog.Sources.Count catalog.Claims.Count
                for decision in decisions do
                    printfn "  %s: %s (EDF: %s)" decision.CaseId decision.Posture
                        (decision.EdfLevel |> Option.defaultValue "not used")
                0
    with ex ->
        eprintfn "Fatal input or execution error: %s" ex.Message
        1
