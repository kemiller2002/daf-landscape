/// Package validation for Phase III: registers (IDs, prefixes, vocabularies, widths, headers), source and P3-ID
/// references, required deliverables 00-26 and their header convention, relative Markdown links, decision status,
/// quoted model-output blocks and the generated MOD fragments. Pure: takes file contents, returns errors and warnings.
module CompetitiveAdvantageCreation.Validate

open System.Text.RegularExpressions
open CompetitiveAdvantageCreation.Registers

type FileSet =
    { /// Package-relative path -> text, for CSV files.
      Csvs: (string * string) list
      Markdown: (string * string) list
      /// Package-relative path exists (file or directory).
      Exists: string -> bool
      /// Phase II source IDs (../competitive-displacement/data/registers/sources.csv).
      PhaseTwoSources: Set<string>
      /// Model output tables by name ("tables/x.md") and generated fragments ("fragment-*.csv").
      ModelOutput: string -> string option }

let evidenceClasses = set [ "VERIFIED-FACT"; "VENDOR-CLAIM"; "INFERENCE"; "ASSUMPTION"; "HYPOTHESIS"; "RECOMMENDATION"; "UNKNOWN" ]
let claimStatuses = set [ "confirmed"; "inferred"; "hypothesized"; "contradicted"; "unknown" ]
let confidences = set [ "High"; "Medium-High"; "Medium"; "Low-Medium"; "Low" ]
let workCategories = set [ "eliminated"; "automated"; "accelerated"; "transferred-to-customer"; "transferred-to-partner"; "deferred"; "mandatory" ]
let classifications =
    set [ "ordinary product capability"; "temporary execution advantage"; "cost advantage"; "architectural advantage"; "organizational advantage"
          "distribution advantage"; "learning economy"; "scale economy"; "genuine network effect"; "unproven hypothesis" ]
let failureBands = set [ "low"; "moderate"; "high"; "very high" ]
let newDecisionStatus = "proposed - owner decision required"
let agentKeys = [ "AB"; "CD"; "EK"; "FGJ"; "HI"; "MOD"; "CE"; "REV1"; "REV2"; "REV3"; "REV4"; "RECON" ]
let severities = set [ "high"; "medium"; "low" ]

let requiredReports =
    [ "00-executive-summary"; "01-approved-strategic-baseline"; "02-existing-unbound-economics"; "03-capital-requirements-reconstruction"
      "04-low-cost-commercial-validation"; "05-untapped-institutional-markets"; "06-customer-acquisition-without-displacement"
      "07-architectural-competitive-advantages"; "08-adjacent-financial-industries"; "09-independent-component-commercialization"
      "10-structural-cost-elimination"; "11-continuous-charity-intelligence"; "12-institutional-distribution"; "13-incumbent-response-model"
      "14-commercial-sequencing"; "15-shared-infrastructure-economics"; "16-capital-efficient-market-entry"; "17-clarity-and-edf-assessment"
      "18-economic-model-methodology"; "19-sensitivity-and-stress-analysis"; "20-adversarial-review"; "21-commercial-thesis-invalidation"
      "22-evidence-gaps"; "23-commercial-validation-roadmap"; "24-cross-repository-implications"; "25-executive-decision-register"
      "26-final-recommendations" ]
    |> List.map (fun s -> s + ".md")

/// Revision 2 (REV fix 15): suffixes of three or four digits (P3-CHL-REV1001), and the agent key may end in a digit.
let private p3Id = Regex(@"P3-(CLM|HYP|ASM|DEC|SEG|PRS|CMP|ADV|EV|CAP|SEQ|VAL|GAP|XRI|SRC|CHL)-[A-Z]+[0-9]?\d{3}(?!\d)")
let private phaseTwoSrc = Regex(@"(?<![A-Z0-9-])SRC-\d{3,4}")

/// Register-level errors for one merged register. requireDispositions: adversarial challenges must carry a
/// disposition (set after reconciliation).
let checkRegisterWith (requireDispositions: bool) (def: RegisterDef) (text: string) : string list =
    match Csv.parseRecords text with
    | [] -> [ $"{def.File}: empty (header required)" ]
    | header :: rows ->
        let hdr = header |> List.map (fun s -> s.Trim())
        if hdr <> def.Header then [ $"{def.File}: header differs from REGISTERS.md" ]
        else
            let idx name = List.tryFindIndex ((=) name) hdr
            let cell (r: string list) name = match idx name with Some k when k < r.Length -> r.[k] | _ -> ""
            let width = rows |> List.indexed |> List.choose (fun (n, r) -> if r.Length <> hdr.Length then Some $"{def.File}: row {n + 2} width {r.Length}, expected {hdr.Length}" else None)
            let ids = rows |> List.map (fun r -> List.head r)
            let dupes = ids |> List.countBy id |> List.filter (fun (_, c) -> c > 1) |> List.map (fun (i, _) -> $"{def.File}: duplicate id {i}")
            let blanks = ids |> List.filter (fun i -> i.Trim() = "") |> List.map (fun _ -> $"{def.File}: blank id")
            let prefixes = String.concat "/" def.Prefixes
            let prefix =
                ids |> List.filter (fun i -> i <> "" && not (def.Prefixes |> List.exists (fun p -> i.StartsWith p)))
                |> List.map (fun i -> $"{def.File}: id {i} lacks prefix {prefixes}")
            let agentForm =
                ids |> List.filter (fun i -> i.StartsWith "P3-" && not (Regex.IsMatch(i, @"^P3-[A-Z]+-(" + String.concat "|" agentKeys + @")\d{3}$")))
                |> List.map (fun i -> $"{def.File}: id {i} is not P3-<TYPE>-<agent key><3 digits>")
            let vocab col (allowed: Set<string>) =
                if List.contains col hdr then
                    rows |> List.choose (fun r ->
                        let x = cell r col
                        if x = "" || Set.contains x allowed then None else Some $"{def.File}: {List.head r} {col}='{x}' not allowed")
                else []
            let status = if def.File = "claims.csv" then vocab "status" claimStatuses else []
            let decisions =
                if def.File = "decisions.csv" then
                    rows |> List.choose (fun r -> let s = cell r "decision_status" in if s = newDecisionStatus then None else Some $"{def.File}: {List.head r} decision_status='{s}' (new decisions must be '{newDecisionStatus}')")
                else []
            let dispositions =
                if requireDispositions && def.File = "adversarial-challenges.csv" then
                    rows |> List.choose (fun r -> if (cell r "disposition").Trim() = "" then Some $"{def.File}: {List.head r} has no disposition" else None)
                else []
            width @ dupes @ blanks @ prefix @ agentForm @ vocab "evidence_class" evidenceClasses @ vocab "confidence" confidences @ status @ decisions
            @ vocab "work_category" workCategories @ vocab "classification" classifications @ vocab "failure_band" failureBands
            @ vocab "severity" severities @ dispositions

let checkRegister (def: RegisterDef) (text: string) = checkRegisterWith false def text

/// Warnings: assumption rows whose numeric low/base/high are not ordered (the model rejects such inputs).
let assumptionWarnings (text: string) : string list =
    let _, rows = Csv.parse text

    let num (s: string) =
        match System.Double.TryParse(s.Trim(), System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture) with
        | true, x -> Some x
        | _ -> None
    rows
    |> List.choose (fun r ->
        let g k = Map.tryFind k r |> Option.defaultValue ""
        match num (g "low"), num (g "base"), num (g "high") with
        | Some l, Some b, Some h when not (l <= b && b <= h) ->
            let id, lo, ba, hi = g "assumption_id", g "low", g "base", g "high"
            Some $"assumptions.csv: {id} low/base/high not ordered ({lo}, {ba}, {hi})"
        | _ -> None)

/// Relative path normalisation that keeps "../" outside the package (resolved by Exists against the package root).
let normalise (p: string) =
    let parts = p.Replace('\\', '/').Split('/') |> List.ofArray
    let folded =
        parts |> List.fold (fun acc x ->
            match x, acc with
            | ".", _ | "", _ -> acc
            | "..", y :: rest when y <> ".." -> rest
            | _ -> x :: acc) []
    folded |> List.rev |> String.concat "/"

let private checkLinksNorm (exists: string -> bool) (name: string) (text: string) =
    Regex.Matches(text, @"\]\(([^)\s#]+)(#[^)]*)?\)")
    |> Seq.map (fun m -> m.Groups.[1].Value)
    |> Seq.filter (fun l -> not (l.StartsWith "http") && not (l.StartsWith "mailto:"))
    |> Seq.filter (fun l ->
        let dir = match name.LastIndexOf '/' with -1 -> "" | k -> name.Substring(0, k)
        not (exists (normalise (if dir = "" then l else dir + "/" + l))))
    |> Seq.map (fun l -> $"{name}: broken link {l}")
    |> List.ofSeq

type Report = { Errors: string list; Warnings: string list; MissingDeliverables: string list }

let validate (fs: FileSet) : Report =
    let find file = fs.Csvs |> List.tryFind (fun (p, _) -> p = "data/registers/" + file)
    let requireDispositions =
        fs.Csvs |> List.tryFind (fun (p, _) -> p = "data/model-inputs/settings.csv")
        |> Option.map (fun (_, t) -> Csv.parse t |> snd |> List.exists (fun r -> Map.tryFind "key" r = Some "require_dispositions" && Map.tryFind "value" r = Some "Y"))
        |> Option.defaultValue false
    let registerErrors =
        definitions |> List.collect (fun d -> match find d.File with Some(_, t) -> checkRegisterWith requireDispositions d t | None -> [ $"missing register data/registers/{d.File}" ])
    let registerIds =
        definitions
        |> List.collect (fun d -> match find d.File with Some(_, t) -> Csv.parseRecords t |> List.tail |> List.map List.head | None -> [])
        |> Set.ofList
    let p3Sources = registerIds |> Set.filter (fun i -> i.StartsWith "P3-SRC-")
    let srcErrors (name: string) (text: string) =
        let p2 = phaseTwoSrc.Matches(text) |> Seq.map (fun m -> m.Value) |> Seq.distinct |> Seq.filter (fun s -> not (Set.contains s fs.PhaseTwoSources)) |> Seq.map (fun s -> $"{name}: unknown Phase II source {s}")
        let p3 = Regex.Matches(text, @"P3-SRC-[A-Z]+\d{3}") |> Seq.map (fun m -> m.Value) |> Seq.distinct |> Seq.filter (fun s -> not (Set.contains s p3Sources)) |> Seq.map (fun s -> $"{name}: unknown Phase III source {s}")
        Seq.append p2 p3 |> List.ofSeq
    let registerTexts = fs.Csvs |> List.filter (fun (p, _) -> p.StartsWith "data/registers/")
    let inputTexts = fs.Csvs |> List.filter (fun (p, _) -> p.StartsWith "data/model-inputs/")
    let refErrors = (registerTexts @ inputTexts) |> List.collect (fun (p, t) -> srcErrors p t)
    let idErrors (name: string) (text: string) =
        p3Id.Matches(text) |> Seq.map (fun m -> m.Value) |> Seq.distinct
        |> Seq.filter (fun i -> not (i.StartsWith "P3-SRC-") && not (Set.contains i registerIds))
        |> Seq.map (fun i -> $"{name}: cites {i}, which is in no register") |> List.ofSeq
    let mdRefErrors = fs.Markdown |> List.collect (fun (p, t) -> srcErrors p t @ idErrors p t)
    let inputIdErrors = inputTexts |> List.collect (fun (p, t) -> idErrors p t)
    let missing = requiredReports |> List.filter (fun r -> not (fs.Exists r))
    let headerErrors =
        requiredReports
        |> List.choose (fun r -> fs.Markdown |> List.tryFind (fun (p, _) -> p = r))
        |> List.collect (fun (p, t) ->
            let lines = t.Split('\n') |> List.ofArray
            let nn = p.Substring(0, 2)
            let h1 = match lines with l :: _ when l.StartsWith("# " + nn + " - ") -> [] | _ -> [ $"{p}: first line must be '# {nn} - Title'" ]
            let st = if lines |> List.truncate 6 |> List.exists (fun l -> l.StartsWith "Status:") then [] else [ $"{p}: no 'Status:' line near the top" ]
            h1 @ st)
    let linkErrors = fs.Markdown |> List.collect (fun (p, t) -> checkLinksNorm fs.Exists p t)
    let quoteErrors = fs.Markdown |> List.collect (fun (p, t) -> Quote.check p fs.ModelOutput t)
    let fragmentErrors =
        [ "capital-requirements.csv"; "commercial-sequences.csv" ]
        |> List.collect (fun f ->
            match fs.ModelOutput("fragment-" + f), fs.Csvs |> List.tryFind (fun (p, _) -> p = "data/fragments/MOD/" + f) with
            | Some gen, Some(_, t) when gen <> t -> [ $"data/fragments/MOD/{f}: differs from the model's generated rows (run `fragments`)" ]
            | Some _, None -> [ $"data/fragments/MOD/{f}: missing (run `fragments`)" ]
            | _ -> [])
    let warnings = match find "assumptions.csv" with Some(_, t) -> assumptionWarnings t | None -> []
    { Errors = registerErrors @ refErrors @ mdRefErrors @ inputIdErrors @ headerErrors @ linkErrors @ quoteErrors @ fragmentErrors
      Warnings = warnings
      MissingDeliverables = missing }
