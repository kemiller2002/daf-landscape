/// Command-line entry point. The only module with I/O.
module ZeroBasedEconomics.Program

open System
open System.IO
open ZeroBasedEconomics

let readInputs (dir: string) =
    let read name =
        let p = Path.Combine(dir, name)
        let p' = if File.Exists p then p else Path.Combine(dir, "..", "registers", name)
        if File.Exists p' then File.ReadAllText p' else failwithf "missing input %s" name
    Inputs.build read

let private fail (msg: string) =
    eprintfn "%s" msg
    1

let run (inDir: string) (outDir: string) =
    match readInputs inDir with
    | Error e -> fail e
    | Ok inp ->
        Directory.CreateDirectory outDir |> ignore
        Render.all inp |> List.iter (fun (name, text) -> File.WriteAllText(Path.Combine(outDir, name), text))
        printfn "run OK: %d outputs written to %s" 13 outDir
        0

let check (inDir: string) (outDir: string) =
    match readInputs inDir with
    | Error e -> fail e
    | Ok inp ->
        let diffs =
            Render.all inp
            |> List.filter (fun (name, text) ->
                let p = Path.Combine(outDir, name)
                not (File.Exists p) || File.ReadAllText p <> text)
            |> List.map fst
        if List.isEmpty diffs then
            printfn "check OK: outputs reproduce"
            0
        else fail ("check FAILED: outputs differ: " + String.Join(", ", diffs))

let validate (root: string) =
    match readInputs (Path.Combine(root, "data", "inputs")) with
    | Error e -> fail e
    | Ok inp ->
        let docs =
            Directory.GetFiles(root, "*.md", SearchOption.AllDirectories)
            |> Array.filter (fun p -> not (p.Contains $"{Path.DirectorySeparatorChar}bin{Path.DirectorySeparatorChar}" || p.Contains $"{Path.DirectorySeparatorChar}obj{Path.DirectorySeparatorChar}"))
            |> Array.sort
            |> Array.toList
            |> List.map (fun p -> Path.GetRelativePath(root, p), File.ReadAllText p)
        let exists (doc: string) (target: string) =
            let full = Path.GetFullPath(Path.Combine(root, Path.GetDirectoryName doc, Uri.UnescapeDataString target))
            File.Exists full || Directory.Exists full
        match Validate.all inp docs exists with
        | [] ->
            printfn "validate OK: %d expenses, %d activities, %d roles, %d coverage rules, %d sources, %d Markdown files" inp.Expenses.Length inp.Activities.Length inp.Roles.Length inp.Coverage.Length inp.Sources.Length docs.Length
            0
        | issues ->
            issues |> List.iter (Validate.format >> eprintfn "%s")
            fail $"validate FAILED: {issues.Length} issues"

[<EntryPoint>]
let main argv =
    match List.ofArray argv with
    | [ "run"; i; o ] -> run i o
    | [ "check"; i; o ] -> check i o
    | [ "validate"; root ] -> validate root
    | _ -> fail "usage: run <inputs> <outputs> | check <inputs> <outputs> | validate <package-root>"
