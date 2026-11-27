/// Research-package validation (pure checks over file contents; I/O in Program).
module ZeroBased.Validate

open System.Text.RegularExpressions

let deliverables =
    [ "00-executive-findings.md"; "01-methodology.md"; "02-existing-model-reconstruction.md"; "03-cost-assumption-audit.md"
      "04-operational-activity-inventory.md"; "05-activity-elimination-and-automation.md"; "06-human-control-obligations.md"
      "07-minimum-viable-organization.md"; "08-shared-echelon-resource-economics.md"; "09-operational-simulation-design.md"
      "10-workload-and-capacity-model.md"; "11-staffing-thresholds.md"; "12-infrastructure-economics.md"
      "13-beneficium-public-data-economics.md"; "14-beneficium-verification-economics.md"; "15-charity-vetting-alternatives.md"
      "16-software-development-economics.md"; "17-revenue-models.md"; "18-break-even-analysis.md"
      "19-sensitivity-and-stress-testing.md"; "20-competitive-comparison.md"; "21-requirement-economic-impact.md"
      "22-continuous-economic-validation.md"; "23-adversarial-review.md"; "24-cross-repository-implications.md"
      "25-evidence-gaps-and-validation-plan.md"; "26-decisions-and-open-questions.md"; "27-final-recommendations.md"
      "README.md"; "research-ledger.md" ]

/// Every record has the header's width.
let csvWidths (name: string) (text: string) : string list =
    match CompetitiveDisplacement.Csv.parseRecords text with
    | [] -> [ $"{name}: empty" ]
    | header :: rows ->
        rows
        |> List.mapi (fun i r -> i + 2, r)
        |> List.filter (fun (_, r) -> r.Length <> header.Length)
        |> List.map (fun (line, r) -> $"{name}: record {line} has {r.Length} fields, header {header.Length}")

let assumptionSchema = [ "id"; "key"; "definition"; "unit"; "low"; "base"; "high"; "source"; "evidence_class"; "confidence"; "rationale"; "dependencies"; "validation_method"; "last_reviewed" ]

let evidenceClasses = set [ "MEASURED-FACT"; "PUBLISHED-PRICE"; "VERIFIED-FACT"; "INFERENCE"; "ASSUMPTION"; "UNKNOWN" ]

/// Assumption registers carry the full schema and an allowed evidence class on every row.
let assumptions (name: string) (text: string) : string list =
    let header, rows = CompetitiveDisplacement.Csv.parse text
    let missing = assumptionSchema |> List.filter (fun c -> not (List.contains c header)) |> List.map (fun c -> $"{name}: missing column {c}")
    let bad =
        rows |> List.choose (fun r ->
            match Map.tryFind "evidence_class" r with
            | Some ec when Set.contains ec evidenceClasses -> None
            | Some ec ->
                let key = Map.tryFind "key" r |> Option.defaultValue "?"
                Some $"{name}: {key} evidence class '{ec}'"
            | None -> None)
    missing @ bad

/// Relative markdown links (not http, not anchors) whose targets must exist.
let links (markdown: string) : string list =
    Regex.Matches(markdown, @"\]\(([^)#\s]+)(#[^)]*)?\)")
    |> Seq.map (fun m -> m.Groups.[1].Value)
    |> Seq.filter (fun l -> not (l.StartsWith "http") && not (l.StartsWith "mailto:"))
    |> List.ofSeq

let dispositions (text: string) : string list =
    let _, rows = CompetitiveDisplacement.Csv.parse text
    rows |> List.choose (fun r ->
        match Map.tryFind "disposition" r with
        | Some d when d.Trim() <> "" && d <> "unreviewed" -> None
        | _ ->
            let id = Map.tryFind "finding_id" r |> Option.defaultValue "?"
            Some $"adversarial finding {id} has no disposition")
