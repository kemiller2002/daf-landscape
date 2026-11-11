namespace EchelonFoundry.DafDecisionIntelligence

open System
open System.IO
open System.Text
open System.Text.Json
open System.Globalization
open System.Collections.Generic

type Issue = { Code: string; Location: string; Detail: string }

type Claim = {
    Id: string
    CaseId: string
    Status: string
    Sources: Set<string>
    Evidence: Set<string>
}

type Catalog = {
    Sources: Map<string, string>
    Evidence: Map<string, Set<string>>
    Claims: Map<string, Claim>
    Issues: Issue list
}

type Decision = {
    CaseId: string
    Title: string
    Claim: string
    ClaimStatus: string
    Conclusion: string
    Posture: string
    EdfLevel: string option
    DiagnosticSufficiency: string
    FrameworkReason: string
    Evidence: string list
    Sources: string list
    Supported: string list
    Limited: string list
    Rejected: string list
    Counterargument: string
    Action: string
    ReassessWhen: string
    Monitor: string list
    Owner: string
    CommittedInvestment: string
}

module Csv =
    /// Quoted CSV with escaped quotes. This data collection is line-oriented: no multiline fields.
    let fields (line: string) =
        let items = ResizeArray<string>()
        let value = StringBuilder()
        let mutable quoted = false
        let mutable i = 0
        while i < line.Length do
            let c = line.[i]
            if c = '"' then
                if quoted && i + 1 < line.Length && line.[i + 1] = '"' then
                    value.Append('"') |> ignore
                    i <- i + 1
                else
                    quoted <- not quoted
            elif c = ',' && not quoted then
                items.Add(value.ToString())
                value.Clear() |> ignore
            else
                value.Append(c) |> ignore
            i <- i + 1
        if quoted then failwith "Unclosed quoted CSV field"
        items.Add(value.ToString())
        List.ofSeq items

    let read (root: string) (path: string) : Map<string,string> list =
        let full = Path.Combine(root, path)
        let lines = File.ReadAllLines(full) |> Array.filter (fun s -> not (String.IsNullOrWhiteSpace(s)))
        if lines.Length < 2 then failwithf "Missing CSV header or rows in %s" path
        let header = fields lines.[0]
        if (Set.ofList header).Count <> header.Length then failwithf "Duplicate CSV column in %s" path
        lines.[1..]
        |> Array.mapi (fun i line ->
            let values = fields line
            if values.Length <> header.Length then
                failwithf "CSV field count mismatch in %s row %d (%d != %d)" path (i + 2) values.Length header.Length
            List.zip header values |> Map.ofList)
        |> Array.toList

    let required (row: Map<string,string>) (name: string) =
        match Map.tryFind name row with
        | Some value -> value
        | None -> failwithf "CSV column %s is missing" name

    let setOf (value: string) =
        value.Split(';', StringSplitOptions.RemoveEmptyEntries ||| StringSplitOptions.TrimEntries)
        |> Set.ofArray

module Catalog =
    let private issue code location detail = { Code=code; Location=location; Detail=detail }

    let load (root: string) : Catalog =
        let problems = ResizeArray<Issue>()
        let sourcePaths = [
            "data/market-demand-evidence-sources-2026.csv"
            "data/audited-contract-evidence-sources-2026.csv"
            "data/charityvest-financial-and-tiaa-sources-2026.csv"
        ]
        let sources =
            sourcePaths
            |> List.collect (fun path ->
                Csv.read root path
                |> List.map (fun row -> Csv.required row "source_id", Csv.required row "url"))
        let sourceIds = sources |> List.map fst
        if sourceIds.Length <> (Set.ofList sourceIds).Count then
            problems.Add(issue "duplicate_source" "catalog" "Duplicate source ID in source registers")
        let sourceMap = Map.ofList sources

        let evidenceFromMetrics =
            Csv.read root "data/market-demand-observed-metrics-2026.csv"
            |> List.map (fun r ->
                let id = Csv.required r "metric_id"
                let sourceSet = Csv.setOf (Csv.required r "source_ids")
                for source in sourceSet do
                    if not (sourceMap.ContainsKey source) then
                        problems.Add(issue "missing_metric_source" id source)
                id, sourceSet)

        let proofRows = Csv.read root "data/decision-intelligence-evidence-crosswalk-v1.csv"
        let derived =
            proofRows |> List.map (fun row ->
                let id = Csv.required row "evidence_id"
                let datasetPath = Csv.required row "dataset_path"
                let keyCol = Csv.required row "key_column"
                let keyValue = Csv.required row "key_value"
                let valueCol = Csv.required row "value_column"
                let expected = Csv.required row "expected_value"
                let sourceSet = Csv.setOf (Csv.required row "source_ids")
                for source in sourceSet do
                    if not (sourceMap.ContainsKey source) then
                        problems.Add(issue "missing_crosswalk_source" id source)
                // The crosswalk cannot invent its own data. Verify the value in the referenced CSV.
                let matching =
                    Csv.read root datasetPath
                    |> List.filter (fun data -> Csv.required data keyCol = keyValue)
                match matching with
                | [ actual ] ->
                    let observed = Csv.required actual valueCol
                    if observed <> expected then
                        problems.Add(issue "financial_crosswalk_mismatch" id (sprintf "%s expected %s, actual %s" datasetPath expected observed))
                | _ ->
                    problems.Add(issue "financial_crosswalk_key" id (sprintf "Expected exactly one row %s=%s in %s" keyCol keyValue datasetPath))
                id, sourceSet)
        let eAll = evidenceFromMetrics @ derived
        if eAll.Length <> (eAll |> List.map fst |> Set.ofList).Count then
            problems.Add(issue "duplicate_evidence" "catalog" "Duplicate metric or derived evidence ID")

        let claimRows = Csv.read root "data/decision-intelligence-claims-2026.csv"
        let claims =
            claimRows |> List.map (fun row ->
                let id = Csv.required row "claim_id"
                let claim = {
                    Id=id
                    CaseId=Csv.required row "case_id"
                    Status=Csv.required row "support_status"
                    Sources=Csv.setOf (Csv.required row "source_ids")
                    Evidence=Csv.setOf (Csv.required row "evidence_ids")
                }
                for source in claim.Sources do
                    if not (sourceMap.ContainsKey source) then
                        problems.Add(issue "missing_claim_source" id source)
                for ev in claim.Evidence do
                    if not (Map.ofList eAll).ContainsKey ev then
                        problems.Add(issue "missing_claim_evidence" id ev)
                id, claim)
        if claims.Length <> (claims |> List.map fst |> Set.ofList).Count then
            problems.Add(issue "duplicate_claim" "catalog" "Duplicate claim ID")
        { Sources=sourceMap; Evidence=Map.ofList eAll; Claims=Map.ofList claims; Issues=List.ofSeq problems }

module Results =
    let private issue code location detail = { Code=code; Location=location; Detail=detail }

    let private property (node: JsonElement) (name: string) =
        let mutable value = Unchecked.defaultof<JsonElement>
        if node.ValueKind = JsonValueKind.Object && node.TryGetProperty(name, &value) then Some value
        else None

    let private string (problems: ResizeArray<Issue>) (location: string) (node: JsonElement) name =
        match property node name with
        | Some value when value.ValueKind = JsonValueKind.String ->
            let text = value.GetString()
            if String.IsNullOrWhiteSpace(text) then
                problems.Add(issue "required_text" location name)
                ""
            else text
        | _ ->
            problems.Add(issue "required_text" location name)
            ""

    let private strings (problems: ResizeArray<Issue>) (location: string) (node: JsonElement) name =
        match property node name with
        | Some value when value.ValueKind = JsonValueKind.Array ->
            let elements = value.EnumerateArray() |> Seq.toList
            let result =
                elements |> List.map (fun item ->
                    if item.ValueKind = JsonValueKind.String then
                        let s = item.GetString()
                        if isNull s then "" else s
                    else "")
            if result.IsEmpty || (result |> List.exists String.IsNullOrWhiteSpace) then
                problems.Add(issue "required_list" location name)
            if (Set.ofList result).Count <> result.Length then
                problems.Add(issue "duplicate_reference" location name)
            result
        | _ ->
            problems.Add(issue "required_list" location name)
            []

    let validate (catalog: Catalog) (json: string) : Issue list * Decision list =
        let problems = ResizeArray<Issue>(catalog.Issues)
        let mutable decisions = []
        try
            use doc = JsonDocument.Parse(json)
            let root = doc.RootElement
            if string problems "root" root "schema" <> "daf-decision-intelligence-v1" then
                problems.Add(issue "schema_mismatch" "root" "Expected daf-decision-intelligence-v1")
            let asOf = string problems "root" root "asOf"
            let mutable date = DateTime.MinValue
            if not (DateTime.TryParseExact(asOf, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, &date)) then
                problems.Add(issue "invalid_date" "root" asOf)
            let pins =
                match property root "pins" with
                | Some value when value.ValueKind = JsonValueKind.Object -> value
                | _ ->
                    problems.Add(issue "required_object" "root" "pins")
                    Unchecked.defaultof<JsonElement>
            for framework in ["clarity";"edf";"evidence"] do
                let item =
                    match property pins framework with
                    | Some found -> found
                    | None ->
                        problems.Add(issue "missing_pin" "root" framework)
                        Unchecked.defaultof<JsonElement>
                let sha = string problems ("pins." + framework) item "commit"
                if sha.Length <> 40 || sha |> Seq.exists (fun c -> not (Uri.IsHexDigit c)) then
                    problems.Add(issue "invalid_pin" ("pins." + framework) sha)

            let resultList =
                match property root "results" with
                | Some v when v.ValueKind = JsonValueKind.Array -> v.EnumerateArray() |> Seq.toList
                | _ ->
                    problems.Add(issue "required_list" "root" "results")
                    []
            for element in resultList do
                let id = string problems "result" element "caseId"
                let loc = if id = "" then "result" else id
                let title = string problems loc element "title"
                let claim = string problems loc element "claim"
                let status = string problems loc element "claimStatus"
                let verdict = string problems loc element "conclusionType"
                if not (Set.ofList ["investigate";"reject_invalid_inference";"withhold_comparison"]).Contains(verdict) then
                    problems.Add(issue "invalid_verdict" loc verdict)
                let conclusion = string problems loc element "conclusion"
                let counterargument = string problems loc element "counterargument"
                let action = string problems loc element "action"
                let reassess = string problems loc element "reassessWhen"
                let owner = string problems loc element "responsibleOwner"
                let commitment = string problems loc element "committedInvestment"
                let sourceIds = strings problems loc element "sourceIds"
                let evidence = strings problems loc element "evidence"
                let monitor = strings problems loc element "monitor"
                let claimsObj =
                    match property element "claimRoles" with
                    | Some value -> value
                    | None ->
                        problems.Add(issue "required_object" loc "claimRoles")
                        Unchecked.defaultof<JsonElement>
                let supported = strings problems loc claimsObj "supported"
                let limited = strings problems loc claimsObj "limited"
                let rejected = strings problems loc claimsObj "rejected"
                let framework =
                    match property element "frameworkUse" with
                    | Some value -> value
                    | None ->
                        problems.Add(issue "required_object" loc "frameworkUse")
                        Unchecked.defaultof<JsonElement>
                let posture = string problems loc framework "clarityPosture"
                let diagnosis = string problems loc framework "diagnosticSufficiency"
                let reason = string problems loc framework "reason"
                let edf =
                    match property framework "edfLevel" with
                    | Some p when p.ValueKind = JsonValueKind.Null -> None
                    | Some p when p.ValueKind = JsonValueKind.String -> Some(p.GetString())
                    | _ ->
                        problems.Add(issue "invalid_edf" loc "edfLevel must be null or EDF-0/1/2")
                        None
                if not (posture = "Experimental" || posture.StartsWith("Strategic") || posture.StartsWith("Guardrail") || posture.StartsWith("Fast")) then
                    problems.Add(issue "invalid_posture" loc posture)
                match edf with
                | None when diagnosis <> "not_applicable" -> problems.Add(issue "edf_sufficiency_conflict" loc "No EDF diagnosis but diagnostic sufficiency claimed")
                | Some level when not (Set.ofList ["EDF-0";"EDF-1";"EDF-2"]).Contains(level) ->
                    problems.Add(issue "invalid_edf" loc level)
                | Some _ when diagnosis = "not_applicable" -> problems.Add(issue "edf_sufficiency_conflict" loc "EDF diagnosis has not_applicable sufficiency")
                | _ -> ()
                if commitment <> "none" && (owner = "unassigned" || posture.StartsWith("Strategic")) then
                    problems.Add(issue "unowned_commitment" loc "Commitment requires named owner and further approval")
                for sid in sourceIds do
                    if not (catalog.Sources.ContainsKey sid) then
                        problems.Add(issue "unknown_source" loc sid)
                for ev in evidence do
                    match Map.tryFind ev catalog.Evidence with
                    | None -> problems.Add(issue "unknown_evidence" loc ev)
                    | Some sourceSet when (Set.intersect sourceSet (Set.ofList sourceIds)).IsEmpty ->
                        problems.Add(issue "source_evidence_mismatch" loc ev)
                    | _ -> ()
                let checkRole role acceptable (refs: string list) =
                    for claimId in refs do
                        match Map.tryFind claimId catalog.Claims with
                        | None -> problems.Add(issue "unknown_claim" loc claimId)
                        | Some c ->
                            if c.CaseId <> id then problems.Add(issue "cross_case_claim" loc claimId)
                            if not (acceptable c.Status) then
                                problems.Add(issue "claim_role_mismatch" loc (claimId + ": " + role + " versus " + c.Status))
                            if (Set.intersect c.Sources (Set.ofList sourceIds)).IsEmpty then
                                problems.Add(issue "claim_source_mismatch" loc claimId)
                            if (Set.intersect c.Evidence (Set.ofList evidence)).IsEmpty then
                                problems.Add(issue "claim_evidence_mismatch" loc claimId)
                checkRole "supported" (fun s -> s.StartsWith("supported_")) supported
                checkRole "limited" (fun s -> s = "provisional_hypothesis" || s = "insufficient") limited
                checkRole "rejected" (fun s -> s = "unsupported" || s = "contradicted_by_unit") rejected
                let allRoles = supported @ limited @ rejected
                if (Set.ofList allRoles).Count <> allRoles.Length then
                    problems.Add(issue "duplicate_claim_role" loc "A claim appears in more than one role")
                let expectedClaims =
                    catalog.Claims |> Map.toList |> List.choose (fun (id2,c) -> if c.CaseId=id then Some id2 else None) |> Set.ofList
                if not (Set.isEmpty expectedClaims) && expectedClaims <> Set.ofList allRoles then
                    problems.Add(issue "unclassified_claims" loc "Every claim in the case must be classified")
                decisions <- {
                    CaseId=id;Title=title;Claim=claim;ClaimStatus=status;Conclusion=conclusion
                    Posture=posture;EdfLevel=edf;DiagnosticSufficiency=diagnosis;FrameworkReason=reason
                    Evidence=evidence;Sources=sourceIds;Supported=supported;Limited=limited;Rejected=rejected
                    Counterargument=counterargument;Action=action;ReassessWhen=reassess
                    Monitor=monitor;Owner=owner;CommittedInvestment=commitment
                }::decisions
            let ids = decisions |> List.map (fun d -> d.CaseId)
            if (Set.ofList ids).Count <> ids.Length then
                problems.Add(issue "duplicate_result" "results" "Case IDs must be unique")
            if decisions.IsEmpty then problems.Add(issue "no_results" "results" "At least one case required")
        with
        | :? JsonException as ex -> problems.Add(issue "invalid_json" "root" ex.Message)
        | :? InvalidOperationException as ex -> problems.Add(issue "invalid_json_shape" "root" ex.Message)
        List.ofSeq problems, List.rev decisions

module Report =
    let private safe (text: string) =
        text.Replace("\r"," ").Replace("\n"," ").Replace("|","\\|").Trim()

    let markdown (catalog: Catalog) (results: Decision list) =
        let b=StringBuilder()
        let add (s:string) = b.AppendLine(s) |> ignore
        add "# DAF Decision Intelligence conclusions"
        add ""
        add "Generated from validated structured evidence and claim roles. This is deterministic presentation, **not AI-generated diagnosis or independent verification of the underlying source assertions**."
        add ""
        for r in results do
            add (sprintf "## %s: %s" (safe r.CaseId) (safe r.Title))
            add ""
            add (sprintf "**Current conclusion:** %s" (safe r.Conclusion))
            add ""
            add (sprintf "**Clarity posture:** %s. **EDF:** %s." (safe r.Posture) (r.EdfLevel |> Option.defaultValue "not applied"))
            add ""
            add (sprintf "**Supporting claim IDs:** %s" (String.concat ", " r.Supported))
            add (sprintf "**Provisional/insufficient claim IDs:** %s" (String.concat ", " r.Limited))
            add (sprintf "**Rejected claim IDs:** %s" (String.concat ", " r.Rejected))
            add ""
            add (sprintf "**Strongest objection:** %s" (safe r.Counterargument))
            add ""
            add (sprintf "**Next responsible action:** %s" (safe r.Action))
            add ""
            add (sprintf "**Reassess when:** %s" (safe r.ReassessWhen))
            add ""
            add "**Evidence and source provenance:**"
            for id in r.Sources do
                let url = catalog.Sources.[id]
                add (sprintf "- [%s](%s)" id url)
            add ""
        b.ToString()
