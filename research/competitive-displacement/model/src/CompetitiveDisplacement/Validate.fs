/// Package validation: register structure, controlled vocabularies, cross-references, required deliverables
/// and relative Markdown links. Pure: takes file contents, returns errors.
module CompetitiveDisplacement.Validate

open System.Text.RegularExpressions

type FileSet = { Csvs: (string * string) list; Markdown: (string * string) list; Exists: string -> bool }

let evidenceClasses = set [ "VERIFIED-FACT"; "VENDOR-CLAIM"; "INFERENCE"; "ASSUMPTION"; "HYPOTHESIS"; "RECOMMENDATION"; "UNKNOWN" ]
let claimStatuses = set [ "confirmed"; "inferred"; "hypothesized"; "contradicted"; "unknown" ]
let confidences = set [ "High"; "Medium"; "Low"; "Medium-High"; "Low-Medium" ]

let requiredReports =
    [ "00-executive-summary.md"; "01-existing-research-synthesis.md"; "02-charity-intelligence-sources.md"
      "03-charity-data-licensing-and-access.md"; "04-charity-intelligence-architecture.md"; "05-charity-registry-economics.md"
      "06-competitive-displacement.md"; "07-institutional-switching-incentives.md"; "08-frictionless-onboarding.md"
      "09-event-level-operating-model.md"; "10-zero-touch-administration-economics.md"; "11-institutional-distribution.md"
      "12-market-entry-segments.md"; "13-compounding-competitive-advantages.md"; "14-alternative-enterprise-models.md"
      "15-capital-and-break-even-reassessment.md"; "16-commercial-entry-strategy.md"; "17-unbound-implications.md"
      "18-transitus-implications.md"; "19-echelon-foundry-implications.md"; "20-adversarial-review.md"; "21-evidence-gaps.md"
      "22-commercial-validation-plan.md"; "23-executive-decision-register.md"; "24-final-recommendations.md" ]

/// Registers required in data/registers with their ID column and ID prefix.
let requiredRegisters =
    [ "sources.csv", "source_id", "SRC-"; "claims.csv", "claim_id", "CLM-"; "hypotheses.csv", "hypothesis_id", "HYP-"
      "competitors.csv", "competitor_id", "CMP-"; "charity-data-sources.csv", "source_key", ""; "operational-events.csv", "event_id", "EV-E"
      "economic-assumptions.csv", "assumption_id", "ASM-"; "market-segments.csv", "segment_id", "SEG-"
      "competitive-advantages.csv", "advantage_id", "ADV-"; "adversarial-challenges.csv", "challenge_id", "CHL-"
      "decisions.csv", "decision_id", "DEC-"; "open-questions.csv", "question_id", "OQ-"; "cross-repository-implications.csv", "implication_id", "XRI-" ]

let private checkRegister (name: string) (idCol: string) (prefix: string) (text: string) : string list =
    let header, rows = Csv.parse text
    let missingId = if List.contains idCol header then [] else [ $"{name}: missing id column {idCol}" ]
    let ids = rows |> List.map (fun r -> Map.tryFind idCol r |> Option.defaultValue "")
    let dupes = ids |> List.countBy id |> List.filter (fun (_, c) -> c > 1) |> List.map (fun (i, _) -> $"{name}: duplicate id {i}")
    let blanks = ids |> List.indexed |> List.filter (fun (_, i) -> i.Trim() = "") |> List.map (fun (n, _) -> $"{name}: row {n + 2} blank id")
    let badPrefix = ids |> List.filter (fun i -> prefix <> "" && i <> "" && not (i.StartsWith prefix)) |> List.map (fun i -> $"{name}: id {i} lacks prefix {prefix}")
    let vocab col allowed =
        if List.contains col header then
            rows |> List.choose (fun r ->
                let x = Map.find col r
                let rid = Map.tryFind idCol r |> Option.defaultValue "?"
                if x = "" || Set.contains x allowed then None else Some $"{name}: {rid} {col}='{x}' not allowed")
        else []
    let width = rows |> List.indexed |> List.choose (fun (n, r) -> if r.Count <> header.Length then Some $"{name}: row {n + 2} width" else None)
    missingId @ dupes @ blanks @ badPrefix @ width @ vocab "evidence_class" evidenceClasses @ vocab "status" claimStatuses @ vocab "confidence" confidences

/// Every SRC- reference anywhere in registers must exist in sources.csv.
let private checkSourceRefs (sources: Set<string>) (name: string) (text: string) =
    Regex.Matches(text, @"SRC-\d{3,4}")
    |> Seq.map (fun m -> m.Value)
    |> Seq.distinct
    |> Seq.filter (fun s -> not (Set.contains s sources))
    |> Seq.map (fun s -> $"{name}: unknown source reference {s}")
    |> List.ofSeq

let private checkLinks (exists: string -> bool) (name: string) (text: string) =
    Regex.Matches(text, @"\]\(([^)\s#]+)(#[^)]*)?\)")
    |> Seq.map (fun m -> m.Groups.[1].Value)
    |> Seq.filter (fun l -> not (l.StartsWith "http") && not (l.StartsWith "mailto:"))
    |> Seq.filter (fun l -> not (exists (System.IO.Path.Combine(System.IO.Path.GetDirectoryName name, l))))
    |> Seq.map (fun l -> $"{name}: broken link {l}")
    |> List.ofSeq

let validate (root: string) (fs: FileSet) : string list =
    let find n = fs.Csvs |> List.tryFind (fun (p, _) -> p.EndsWith("registers/" + n))
    let registerErrors =
        requiredRegisters
        |> List.collect (fun (n, idCol, prefix) ->
            match find n with
            | Some(_, text) -> checkRegister n idCol prefix text
            | None -> [ $"missing register {n}" ])
    let sources =
        find "sources.csv"
        |> Option.map (fun (_, t) -> Csv.parse t |> snd |> List.choose (Map.tryFind "source_id") |> Set.ofList)
        |> Option.defaultValue Set.empty
    let refErrors = fs.Csvs |> List.filter (fun (p, _) -> p.Contains "registers/") |> List.collect (fun (p, t) -> checkSourceRefs sources (System.IO.Path.GetFileName p) t)
    let mdRefErrors = fs.Markdown |> List.collect (fun (p, t) -> checkSourceRefs sources (System.IO.Path.GetFileName p) t)
    let reportErrors = requiredReports |> List.filter (fun r -> not (fs.Exists(System.IO.Path.Combine(root, r)))) |> List.map (fun r -> $"missing deliverable {r}")
    let linkErrors = fs.Markdown |> List.collect (fun (p, t) -> checkLinks fs.Exists p t)
    registerErrors @ refErrors @ mdRefErrors @ reportErrors @ linkErrors
