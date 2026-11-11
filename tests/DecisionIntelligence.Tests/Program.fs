module EchelonFoundry.DafDecisionIntelligence.Tests

open System
open System.IO
open System.Text.Json.Nodes
open EchelonFoundry.DafDecisionIntelligence

[<EntryPoint>]
let main _ =
    let root = Directory.GetCurrentDirectory()
    let input = File.ReadAllText(Path.Combine(root, "data/decision-intelligence-results-v1.json"))
    let catalog = Catalog.load root
    let baselineIssues, baselineDecisions = Results.validate catalog input

    let issue code (problems: Issue list) = problems |> List.exists (fun i -> i.Code = code)
    let mutate (change: JsonObject -> unit) =
        let json = JsonNode.Parse(input).AsObject()
        change json
        Results.validate catalog (json.ToJsonString()) |> fst
    let result (node:JsonObject) index =
        node.["results"].AsArray().[index].AsObject()
    let put (node:JsonObject) key (value:string) =
        node.[key] <- JsonValue.Create(value)
    let replaceItem (node: JsonObject) index key value =
        put (result node index) key value
    let invalidate (code:string) (change: JsonObject -> unit) =
        issue code (mutate change)

    let cases: (string * (unit -> bool)) list = [
        "baseline validates with no issues", (fun () -> baselineIssues.IsEmpty)
        "three baseline decisions remain intact", (fun () -> baselineDecisions.Length = 3)
        "all three evidence classes resolve", (fun () ->
            catalog.Evidence.ContainsKey("M21")
            && catalog.Evidence.ContainsKey("2024_RCF_Ren_19225546")
            && catalog.Evidence.ContainsKey("Charityvest_non_grant_expenses_811940"))
        "valid Markdown includes disagreement and source citation", (fun () ->
            let output=Report.markdown catalog baselineDecisions
            output.Contains("Why and what remains uncertain")
            && output.Contains("Sponsor survey respondents self-rated grant review")
            && output.Contains("Strongest objection")
            && output.Contains("https://renaissancecharitable.org")
            && output.Contains("Reassess when"))
        "verdict inconsistent with declared evidence status rejected", (fun () ->
            invalidate "verdict_status_mismatch" (fun n ->
                replaceItem n 2 "claimStatus" "supported"))
        "wrong case verdict rejected", (fun () ->
            invalidate "verdict_status_mismatch" (fun n ->
                replaceItem n 1 "conclusionType" "investigate"))
        "invalid schema rejected", (fun () ->
            invalidate "schema_mismatch" (fun n -> put n "schema" "untrusted-model"))
        "invalid review date rejected", (fun () ->
            invalidate "invalid_date" (fun n -> put n "asOf" "later"))
        "bad Clarity commit pin rejected", (fun () ->
            invalidate "invalid_pin" (fun n ->
                put (n.["pins"].AsObject().["clarity"].AsObject()) "commit" "not-a-sha"))
        "missing EDF pin rejected", (fun () ->
            invalidate "missing_pin" (fun n ->
                n.["pins"].AsObject().Remove("edf") |> ignore))
        "duplicate conclusion id rejected", (fun () ->
            invalidate "duplicate_result" (fun n ->
                put (result n 1) "caseId" "DI-001"))
        "blank conclusion rejected", (fun () ->
            invalidate "required_text" (fun n -> replaceItem n 0 "conclusion" ""))
        "blank next action rejected", (fun () ->
            invalidate "required_text" (fun n -> replaceItem n 0 "action" " "))
        "missing counterargument rejected", (fun () ->
            invalidate "required_text" (fun n ->
                result n 2 |> fun o -> o.Remove("counterargument") |> ignore))
        "missing reassessment trigger rejected", (fun () ->
            invalidate "required_text" (fun n -> replaceItem n 1 "reassessWhen" ""))
        "empty monitoring list rejected", (fun () ->
            invalidate "required_list" (fun n -> result n 1 |> fun o -> o.["monitor"].AsArray().Clear()))
        "invalid claim role rejected", (fun () ->
            invalidate "claim_role_mismatch" (fun n ->
                let roles = result n 0 |> fun o -> o.["claimRoles"].AsObject()
                let supported = roles.["supported"].AsArray()
                supported.[0] <- JsonValue.Create("DI001-C02")))
        "unclassified case claim rejected", (fun () ->
            invalidate "unclassified_claims" (fun n ->
                let role = result n 0 |> fun o -> o.["claimRoles"].AsObject()
                role.["limited"].AsArray().Clear()))
        "duplicate claim in multiple roles rejected", (fun () ->
            invalidate "duplicate_claim_role" (fun n ->
                let role = result n 0 |> fun o -> o.["claimRoles"].AsObject()
                role.["limited"].AsArray().Add(JsonValue.Create("DI001-C01"))))
        "missing claim id rejected", (fun () ->
            invalidate "unknown_claim" (fun n ->
                let role = result n 1 |> fun o -> o.["claimRoles"].AsObject()
                role.["rejected"].AsArray().[0] <- JsonValue.Create("NOT-A-CLAIM")))
        "claim from another decision rejected", (fun () ->
            invalidate "cross_case_claim" (fun n ->
                let role = result n 0 |> fun o -> o.["claimRoles"].AsObject()
                role.["rejected"].AsArray().[0] <- JsonValue.Create("DI002-C02")))
        "source unknown rejected", (fun () ->
            invalidate "unknown_source" (fun n ->
                result n 0 |> fun o -> o.["sourceIds"].AsArray().[0] <- JsonValue.Create("B99")))
        "metric evidence unknown rejected", (fun () ->
            invalidate "unknown_evidence" (fun n ->
                result n 0 |> fun o -> o.["evidence"].AsArray().[0] <- JsonValue.Create("M99")))
        "financial evidence forgery rejected", (fun () ->
            invalidate "unknown_evidence" (fun n ->
                result n 2 |> fun o -> o.["evidence"].AsArray().[0] <- JsonValue.Create("2024_RCF_Ren_999999999")))
        "citation not supporting evidence rejected", (fun () ->
            invalidate "source_evidence_mismatch" (fun n ->
                let sources = result n 0 |> fun o -> o.["sourceIds"].AsArray()
                sources.Clear()
                sources.Add(JsonValue.Create("V03"))))
        "incorrect EDF level rejected", (fun () ->
            invalidate "invalid_edf" (fun n ->
                let fw = result n 0 |> fun o -> o.["frameworkUse"].AsObject()
                put fw "edfLevel" "EDF-9"))
        "EDF sufficiency without EDF diagnosis rejected", (fun () ->
            invalidate "edf_sufficiency_conflict" (fun n ->
                let fw = result n 2 |> fun o -> o.["frameworkUse"].AsObject()
                put fw "diagnosticSufficiency" "high"))
        "EDF diagnosis with not_applicable sufficiency rejected", (fun () ->
            invalidate "edf_sufficiency_conflict" (fun n ->
                let fw = result n 2 |> fun o -> o.["frameworkUse"].AsObject()
                put fw "edfLevel" "EDF-2"))
        "unowned investment rejected", (fun () ->
            invalidate "unowned_commitment" (fun n ->
                replaceItem n 2 "committedInvestment" "allocate_capital"))
        "source registry deletion invalidates decision", (fun () ->
            let altered = { catalog with Sources=catalog.Sources.Remove("B05") }
            let errors,_=Results.validate altered input
            issue "unknown_source" errors)
        "deleted financial evidence invalidates case", (fun () ->
            let altered = { catalog with Evidence=catalog.Evidence.Remove("2024_RCF_Ren_19225546") }
            let errors,_=Results.validate altered input
            issue "unknown_evidence" errors)
        "all 10 registered claims belong to 3 cases", (fun () ->
            catalog.Claims.Count=10
            && (catalog.Claims |> Map.forall (fun _ c ->
                baselineDecisions |> List.exists (fun d -> d.CaseId=c.CaseId))))
    ]
    let mutable failures=0
    for (name, check) in cases do
        let success =
            try check()
            with ex ->
                eprintfn "ERROR %s: %s" name ex.Message
                false
        if success then printfn "PASS %s" name
        else
            eprintfn "FAIL %s" name
            failures <- failures + 1
    printfn "Result: %d/%d cases passed" (cases.Length-failures) cases.Length
    if failures=0 then 0 else 1
