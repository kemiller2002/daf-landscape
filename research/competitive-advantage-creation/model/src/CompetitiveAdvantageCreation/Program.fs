/// I/O shell: the only module that touches the file system. Commands: merge, run, check, validate, quote, fragments.
module CompetitiveAdvantageCreation.Program

open System.IO

let private readInputs (dir: string) = Inputs.load (fun f -> File.ReadAllText(Path.Combine(dir, f)))

let private write (dir: string) (rel: string) (text: string) =
    let p = Path.Combine(dir, rel)
    Directory.CreateDirectory(Path.GetDirectoryName p) |> ignore
    File.WriteAllText(p, text)

let run (inputDir: string) (outDir: string) =
    match readInputs inputDir with
    | Error es -> es |> List.iter (eprintfn "%s"); 1
    | Ok inputs ->
        let files = Render.outputs inputs
        files |> List.iter (fun (n, t) -> write outDir n t)
        printfn "wrote %d files to %s" files.Length outDir
        0

let check (inputDir: string) (outDir: string) =
    match readInputs inputDir with
    | Error es -> es |> List.iter (eprintfn "%s"); 1
    | Ok inputs ->
        let diffs = Render.outputs inputs |> List.filter (fun (n, t) -> let p = Path.Combine(outDir, n) in not (File.Exists p) || File.ReadAllText p <> t)
        diffs |> List.iter (fun (n, _) -> eprintfn "differs: %s" n)
        if List.isEmpty diffs then printfn "check OK: outputs reproduce byte for byte"; 0 else 1

let private fragmentDir root = Path.Combine(root, "data", "fragments")

let merge (root: string) =
    let frags =
        Directory.GetDirectories(fragmentDir root)
        |> Array.sort
        |> Array.collect (fun d ->
            Directory.GetFiles(d, "*.csv") |> Array.sort
            |> Array.map (fun f -> ({ Agent = Path.GetFileName d; File = Path.GetFileName f; Text = File.ReadAllText f }: Registers.Fragment)))
        |> List.ofArray
    match Registers.merge frags with
    | Error es -> es |> List.iter (eprintfn "%s"); eprintfn "%d merge errors" es.Length; 1
    | Ok regs ->
        regs |> List.iter (fun (f, t, n) -> write (Path.Combine(root, "data", "registers")) f t; printfn "%-36s %4d rows" f n)
        printfn "merge OK: %d registers from %d fragment files" regs.Length frags.Length
        0

let private rel (root: string) (p: string) = Path.GetRelativePath(root, p).Replace('\\', '/')

let private modelOutputLookup (root: string) =
    let outDir = Path.Combine(root, "data", "model-outputs")
    fun (name: string) -> let p = Path.Combine(outDir, name) in if File.Exists p then Some(File.ReadAllText p) else None

let validate (root: string) =
    let skip (p: string) = p.Contains "/bin/" || p.Contains "/obj/"
    let files ext = Directory.GetFiles(root, ext, SearchOption.AllDirectories) |> Array.filter (skip >> not) |> Array.sort |> Array.map (fun p -> rel root p, File.ReadAllText p) |> List.ofArray
    let phaseTwo =
        let p = Path.Combine(root, "..", "competitive-displacement", "data", "registers", "sources.csv")
        if File.Exists p then Csv.parse (File.ReadAllText p) |> snd |> List.choose (Map.tryFind "source_id") |> Set.ofList else Set.empty
    let fs: Validate.FileSet =
        { Csvs = files "*.csv"; Markdown = files "*.md"
          Exists = (fun p -> let full = Path.Combine(root, p) in File.Exists full || Directory.Exists full)
          PhaseTwoSources = phaseTwo; ModelOutput = modelOutputLookup root }
    let r = Validate.validate fs
    r.Warnings |> List.iter (eprintfn "warning: %s")
    r.Errors |> List.iter (eprintfn "%s")
    r.MissingDeliverables |> List.iter (eprintfn "missing deliverable %s")
    let total = r.Errors.Length + r.MissingDeliverables.Length
    if total = 0 then printfn "validate OK: %d CSV, %d Markdown files (%d warnings)" fs.Csvs.Length fs.Markdown.Length r.Warnings.Length; 0
    else eprintfn "%d validation errors (%d missing deliverables), %d warnings" total r.MissingDeliverables.Length r.Warnings.Length; 1

/// Fill quoted model-output blocks in every Markdown file at the package root.
let quote (root: string) =
    let lookup = modelOutputLookup root
    let results =
        Directory.GetFiles(root, "*.md") |> Array.sort
        |> Array.map (fun p ->
            let text = File.ReadAllText p
            let filled, missing = Quote.fill lookup text
            if filled <> text then File.WriteAllText(p, filled)
            Path.GetFileName p, filled <> text, missing)
    results |> Array.iter (fun (n, changed, missing) -> (if changed then printfn "updated %s" n); missing |> List.iter (eprintfn "%s: unknown model output %s" n))
    if results |> Array.exists (fun (_, _, m) -> not (List.isEmpty m)) then 1 else 0

/// Copy the generated MOD fragment rows from data/model-outputs into data/fragments/MOD.
let fragments (root: string) =
    let lookup = modelOutputLookup root
    let pairs = [ "capital-requirements.csv"; "commercial-sequences.csv" ]
    let missing = pairs |> List.filter (fun f -> (lookup ("fragment-" + f)).IsNone)
    if not (List.isEmpty missing) then missing |> List.iter (eprintfn "no generated fragment-%s (run first)"); 1
    else
        pairs |> List.iter (fun f -> write (Path.Combine(fragmentDir root, "MOD")) f (Option.get (lookup ("fragment-" + f))); printfn "wrote data/fragments/MOD/%s" f)
        0

[<EntryPoint>]
let main argv =
    match List.ofArray argv with
    | [ "run"; i; o ] -> run i o
    | [ "check"; i; o ] -> check i o
    | [ "merge"; root ] -> merge root
    | [ "validate"; root ] -> validate root
    | [ "quote"; root ] -> quote root
    | [ "fragments"; root ] -> fragments root
    | _ ->
        eprintfn "usage: run <inputs> <outdir> | check <inputs> <outdir> | merge <package-root> | validate <package-root> | quote <package-root> | fragments <package-root>"
        2
