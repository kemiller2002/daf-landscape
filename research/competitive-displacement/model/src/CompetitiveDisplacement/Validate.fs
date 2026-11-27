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
      "decisions.csv", "decision_id", "DEC-"; "open-questions.csv", "question_id", "OQ-"; "cross-repository-implications.csv", "implication_id", "XRI-"
      "decision-approvals.csv", "decision_id", "DEC-"; "xri-dispositions.csv", "implication_id", "XRI-" ]

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

/// Decision status ladder (owner approval 2026-11-26). Each stage is distinct; a later stage can be "yes"
/// only when every earlier stage is "yes", so approval never silently implies implementation or validation.
let ladderStages =
    [ "strategically_approved"; "requirements_incorporated"; "evidence_gate_satisfied"
      "implementation_authorized"; "implemented"; "validated" ]

let ladderValues = set [ "yes"; "no"; "partial"; "pending" ]

let dispositionClasses =
    set [ "Already satisfied"; "Requirements updated"; "New requirement added"; "Existing decision superseded"
          "Research-only"; "Deferred behind an explicit gate"; "Blocked by unavailable information"; "Requires a new owner decision" ]

/// Ladder errors for one decision row: unknown values, or a stage marked "yes" while an earlier stage is not.
let ladderErrors (row: Map<string, string>) : string list =
    let rid = Map.tryFind "decision_id" row |> Option.defaultValue "?"
    let values = ladderStages |> List.map (fun s -> s, Map.tryFind s row |> Option.defaultValue "")
    let unknown =
        values |> List.filter (fun (_, v) -> not (Set.contains v ladderValues))
        |> List.map (fun (s, v) -> $"decision-approvals.csv: {rid} {s}='{v}' not allowed")
    let premature =
        values
        |> List.indexed
        |> List.filter (fun (i, (_, v)) -> v = "yes" && (values |> List.take i |> List.exists (fun (_, p) -> p <> "yes")))
        |> List.map (fun (_, (s, _)) -> $"decision-approvals.csv: {rid} {s}=yes before an earlier stage is yes")
    unknown @ premature

/// Every ID in the source register must appear exactly once in the follow-up register.
let private coverage (name: string) (idCol: string) (expected: Set<string>) (text: string) : string list =
    let present = Csv.parse text |> snd |> List.choose (Map.tryFind idCol) |> Set.ofList
    Set.difference expected present |> Set.toList |> List.map (fun i -> $"{name}: no row for {i}")

/// Approval and disposition registers: coverage of every decision and implication, ladder order, disposition vocabulary.
let checkFollowUp (decisions: string) (implications: string) (approvals: string) (dispositions: string) : string list =
    let ids col text = Csv.parse text |> snd |> List.choose (Map.tryFind col) |> Set.ofList
    let approvalRows = Csv.parse approvals |> snd
    let dispositionRows = Csv.parse dispositions |> snd
    let badClass =
        dispositionRows
        |> List.choose (fun r ->
            let c = Map.tryFind "disposition_class" r |> Option.defaultValue ""
            let rid = Map.tryFind "implication_id" r |> Option.defaultValue "?"
            if Set.contains c dispositionClasses then None
            else Some $"xri-dispositions.csv: {rid} disposition_class='{c}' not allowed")
    coverage "decision-approvals.csv" "decision_id" (ids "decision_id" decisions) approvals
    @ coverage "xri-dispositions.csv" "implication_id" (ids "implication_id" implications) dispositions
    @ (approvalRows |> List.collect ladderErrors)
    @ badClass

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
    let followUpErrors =
        match find "decisions.csv", find "cross-repository-implications.csv", find "decision-approvals.csv", find "xri-dispositions.csv" with
        | Some(_, d), Some(_, x), Some(_, a), Some(_, r) -> checkFollowUp d x a r
        | _ -> [] // a missing register is already reported above
    registerErrors @ refErrors @ mdRefErrors @ reportErrors @ linkErrors @ followUpErrors
