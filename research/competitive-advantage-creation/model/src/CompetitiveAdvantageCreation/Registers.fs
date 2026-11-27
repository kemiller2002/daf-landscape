/// Register definitions (REGISTERS.md) and the deterministic fragment merge. Pure: takes fragment texts, returns
/// merged register texts or errors.
module CompetitiveAdvantageCreation.Registers

type RegisterDef = { File: string; Header: string list; Prefixes: string list }

let private h (s: string) = s.Split(',') |> List.ofArray

/// Exact headers from REGISTERS.md (Phase III register fragments).
let definitions : RegisterDef list =
    [ { File = "sources.csv"; Header = h "source_id,title,publisher,url,publication_date,access_date,evidence_class,confidence,limitations,used_in"; Prefixes = [ "P3-SRC-" ] }
      { File = "claims.csv"; Header = h "claim_id,claim,status,evidence_class,confidence,source_ids,report,notes"; Prefixes = [ "P3-CLM-" ] }
      { File = "hypotheses.csv"; Header = h "hypothesis_id,hypothesis,falsifier,test,confidence,source_ids,report"; Prefixes = [ "P3-HYP-" ] }
      { File = "assumptions.csv"; Header = h "assumption_id,parameter,unit,low,base,high,basis,evidence_class,source_ids,report"; Prefixes = [ "P3-ASM-" ] }
      { File = "decisions.csv"; Header = h "decision_id,decision,decision_status,options,recommendation,reversibility,evidence_needed,relates_to,source_ids,report"; Prefixes = [ "P3-DEC-" ] }
      { File = "market-segments.csv"; Header = h "segment_id,segment,can_sponsor_daf,needs_sponsoring_partner,why_not_offering_today,organizations_count_estimate,count_basis,source_ids,report"; Prefixes = [ "P3-SEG-" ] }
      { File = "institutional-prospects.csv"; Header = h "prospect_id,organization_or_category,segment_id,public_basis,current_daf_offering,qualification_notes,source_ids,report"; Prefixes = [ "P3-PRS-" ] }
      { File = "competitors.csv"; Header = h "competitor_id,name,category,relevant_capability,evidence_class,source_ids,report"; Prefixes = [ "P3-CMP-"; "CMP-" ] }
      { File = "competitive-advantages.csv"; Header = h "advantage_id,advantage,classification,customer_value,measurable,incumbents_provide,reproducible_by_configuration,needs_architectural_replacement,needs_organizational_change,persistence,willingness_to_pay,resilience_to_response,source_ids,report"; Prefixes = [ "P3-ADV-" ] }
      { File = "operational-events.csv"; Header = h "event_id,event,phase2_event_id,conventional_frequency,preventable_frequency,residual_frequency,processing_cost,prevention_cost,failure_cost,work_category,downstream_consequence,control_effectiveness,customer_experience,operational_risk,source_ids,report"; Prefixes = [ "EV-E"; "P3-EV-" ] }
      { File = "capital-requirements.csv"; Header = h "capital_id,state_or_stage,cost_category,cash_low,cash_base,cash_high,fully_loaded_low,fully_loaded_base,fully_loaded_high,removed_cost_replacement_mechanism,residual_risk,evidence_required,source_ids,report"; Prefixes = [ "P3-CAP-" ] }
      { File = "commercial-sequences.csv"; Header = h "sequence_id,sequence,steps,time_to_first_revenue_months,incremental_cash,fully_loaded_cost,failure_band,reversibility,dependencies,funding_route,source_ids,report"; Prefixes = [ "P3-SEQ-" ] }
      { File = "validation-experiments.csv"; Header = h "experiment_id,budget_tier,question,method,cost,evidence_obtainable,remaining_uncertainty,decision_gate,maps_to_v_test,value_of_information,source_ids,report"; Prefixes = [ "P3-VAL-" ] }
      { File = "evidence-gaps.csv"; Header = h "gap_id,gap,why_it_matters,how_to_close,cost_to_close,blocking,report"; Prefixes = [ "P3-GAP-" ] }
      { File = "cross-repository-implications.csv"; Header = h "implication_id,target_repository,target_area,proposed_change,type,rationale,proposal_status,source_ids,report"; Prefixes = [ "P3-XRI-" ] }
      // REGISTERS.md adversarial section (Revision 2)
      { File = "adversarial-challenges.csv"; Header = h "challenge_id,reviewer_perspective,round,target,challenge,severity,evidence,proposed_change,disposition,disposition_rationale,changed_artifacts"; Prefixes = [ "P3-CHL-" ] } ]

/// Fragment file: (agent directory, file name, text).
type Fragment = { Agent: string; File: string; Text: string }

/// Files in fragment directories that are model working files, not registers.
let isModelFile (name: string) = name.StartsWith "model-"

let private ordinal (a: string) (b: string) = System.String.CompareOrdinal(a, b)

/// Merge one register. Header must equal the expected header exactly; every row must have the header's width;
/// IDs must be non-empty and unique across fragments. Rows are sorted by ID (ordinal), so the result is
/// independent of fragment order.
let mergeOne (def: RegisterDef) (frags: Fragment list) : Result<string * int, string list> =
    let parsed =
        frags
        |> List.sortWith (fun a b -> ordinal a.Agent b.Agent)
        |> List.map (fun fr ->
            match Csv.parseRecords fr.Text with
            | [] -> Ok []
            | header :: rows ->
                let hdr = header |> List.map (fun s -> s.Trim())
                if hdr <> def.Header then Error [ $"{fr.Agent}/{def.File}: header differs from REGISTERS.md" ]
                else
                    let widthErrs =
                        rows |> List.indexed |> List.choose (fun (k, r) -> if List.length r <> def.Header.Length then Some $"{fr.Agent}/{def.File}: row {k + 2} has {List.length r} fields, expected {def.Header.Length}" else None)
                    if List.isEmpty widthErrs then Ok rows else Error widthErrs)
    let errs = parsed |> List.collect (function Error e -> e | Ok _ -> [])
    if not (List.isEmpty errs) then Error errs
    else
        let rows = parsed |> List.collect (function Ok r -> r | Error _ -> [])
        let ids = rows |> List.map List.head
        let blank = ids |> List.filter (fun i -> i.Trim() = "") |> List.map (fun _ -> $"{def.File}: blank id")
        let dupes = ids |> List.countBy id |> List.filter (fun (_, n) -> n > 1) |> List.map (fun (i, _) -> $"{def.File}: duplicate id {i}")
        if not (List.isEmpty (blank @ dupes)) then Error(blank @ dupes)
        else
            let sorted = rows |> List.sortWith (fun a b -> ordinal (List.head a) (List.head b))
            Ok(Csv.write def.Header sorted, List.length sorted)

/// Disposition overlays: <agent>/adversarial-challenges-dispositions.csv with header
/// challenge_id,disposition,disposition_rationale,changed_artifacts. Applied in agent order onto the merged
/// adversarial-challenges register: empty fields leave the register unchanged; two different non-empty dispositions
/// for one challenge are an error; rationales and changed artifacts from several overlays are joined with " | ".
let overlayFile = "adversarial-challenges-dispositions.csv"
/// Any file named adversarial-challenges-dispositions*.csv is an overlay (e.g. a round-2 file).
let isOverlay (name: string) = name.StartsWith "adversarial-challenges-dispositions" && name.EndsWith ".csv"
let overlayHeader = [ "challenge_id"; "disposition"; "disposition_rationale"; "changed_artifacts" ]

let applyOverlays (registerText: string) (overlays: Fragment list) : Result<string, string list> =
    match Csv.parseRecords registerText with
    | [] -> Ok registerText
    | header :: rows ->
        let idx name = List.findIndex ((=) name) header
        let parsed =
            overlays
            |> List.sortWith (fun a b -> let c = ordinal a.Agent b.Agent in if c <> 0 then c else ordinal a.File b.File)
            |> List.map (fun o ->
                match Csv.parseRecords o.Text with
                | h :: rs when (h |> List.map (fun x -> x.Trim())) = overlayHeader ->
                    let bad = rs |> List.filter (fun r -> r.Length <> 4) |> List.map (fun r -> $"{o.Agent}/{overlayFile}: width error at {List.head r}")
                    if List.isEmpty bad then Ok(o.Agent, rs) else Error bad
                | _ -> Error [ o.Agent + "/" + overlayFile + ": header must be " + String.concat "," overlayHeader ])
        let errs = parsed |> List.collect (function Error e -> e | Ok _ -> [])
        if not (List.isEmpty errs) then Error errs
        else
            let known = rows |> List.map List.head |> Set.ofList
            let entries = parsed |> List.collect (function Ok(agent, rs) -> rs |> List.map (fun r -> agent, r) | Error _ -> [])
            let unknown = entries |> List.filter (fun (_, r) -> not (Set.contains (List.head r) known)) |> List.map (fun (a, r) -> $"{a}/{overlayFile}: unknown challenge {List.head r}")
            let merge (row: string list) =
                let id = List.head row
                entries
                |> List.filter (fun (_, r) -> List.head r = id)
                |> List.fold
                    (fun (acc: Result<string list, string>) (agent, r) ->
                        acc |> Result.bind (fun cur ->
                            let set (col: string) (v: string) (join: bool) (cur: string list) : Result<string list, string> =
                                let k = idx col
                                let old = cur.[k]
                                if v.Trim() = "" then Ok cur
                                elif old.Trim() = "" || old = v then Ok(List.updateAt k v cur)
                                elif join then Ok(List.updateAt k (old + " | " + v) cur)
                                else Error $"{agent}/{overlayFile}: {id} disposition '{v}' conflicts with '{old}'"
                            set "disposition" r.[1] false cur
                            |> Result.bind (set "disposition_rationale" r.[2] true)
                            |> Result.bind (set "changed_artifacts" r.[3] true)))
                    (Ok row)
            let merged = rows |> List.map merge
            let conflicts = merged |> List.choose (function Error e -> Some e | Ok _ -> None)
            if not (List.isEmpty (unknown @ conflicts)) then Error(unknown @ conflicts)
            else Ok(Csv.write header (merged |> List.choose (function Ok r -> Some r | Error _ -> None)))

/// Merge every register in REGISTERS.md (header-only where no fragment exists), then apply disposition overlays.
/// Unknown non-model CSVs are reported.
let merge (frags: Fragment list) : Result<(string * string * int) list, string list> =
    let known = definitions |> List.map (fun d -> d.File) |> Set.ofList
    let overlays = frags |> List.filter (fun f -> isOverlay f.File)
    let unknown =
        frags |> List.filter (fun f -> not (Set.contains f.File known) && not (isModelFile f.File) && not (isOverlay f.File))
        |> List.map (fun f -> $"{f.Agent}/{f.File}: not a register in REGISTERS.md (rename to model-*.csv or move to data/evidence)")
    let results = definitions |> List.map (fun d -> d, mergeOne d (frags |> List.filter (fun f -> f.File = d.File)))
    let withOverlays =
        results
        |> List.map (fun (d, r) ->
            match r with
            | Ok(t, n) when d.File = "adversarial-challenges.csv" && not (List.isEmpty overlays) -> d, applyOverlays t overlays |> Result.map (fun t2 -> t2, n)
            | _ -> d, r)
    let errs = unknown @ (withOverlays |> List.collect (fun (_, r) -> match r with Error e -> e | Ok _ -> []))
    if List.isEmpty errs then Ok(withOverlays |> List.choose (fun (d, r) -> match r with Ok(t, n) -> Some(d.File, t, n) | Error _ -> None))
    else Error errs
