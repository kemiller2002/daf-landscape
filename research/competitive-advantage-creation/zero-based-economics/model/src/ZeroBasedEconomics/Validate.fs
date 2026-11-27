/// Register gates. Pure: inputs and a list of (markdown file, text, existing-path predicate) in, issues out.
module ZeroBasedEconomics.Validate

open System
open System.Text.RegularExpressions
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Inputs

type Issue = { Gate: string; Subject: string; Message: string }

let issue g s m = { Gate = g; Subject = s; Message = m }
let format (i: Issue) = $"{i.Gate} {i.Subject}: {i.Message}"

let entities = set [ "E1"; "E3"; "E4"; "E5" ]
let answers = set [ "Y"; "N"; "U"; "partial" ]
let decisionHolders = set [ "sponsor"; "ef"; "none" ]

let requiredParams =
    [ "founder_hours_per_year"; "founder_fixed_hours"; "founder_hours_per_customer"; "founder_hours_per_new_customer"
      "founder_imputed_rate"; "sponsor_staff_rate"; "new_customer_share"; "months_to_first_revenue"
      "qualification_amortization_years"; "lic_platform_fee"; "lic_per_account"; "wl_platform_fee"; "wl_per_account"
      "tops_per_account"; "admin_bps_ref"; "ci_subscription"; "mig_fee_base"; "mig_fee_per_account" ]
    @ (allModels |> List.map (fun m -> "collection_lag_months_" + modelCode m))

/// V1: identifiers are unique across every register.
let gUnique (inp: Inputs) =
    [ yield! inp.Expenses |> List.map (fun e -> e.Id)
      yield! inp.Activities |> List.map (fun a -> a.Id)
      yield! inp.Roles |> List.map (fun r -> r.Id)
      yield! inp.Coverage |> List.map (fun c -> c.Id)
      yield! inp.Profiles |> List.map (fun p -> p.Id)
      yield! inp.Qualification |> List.map (fun (id, _, _, _, _) -> id)
      yield! inp.Priors |> List.map (fun p -> p.Id) ]
    |> List.countBy id
    |> List.filter (fun (_, n) -> n > 1)
    |> List.map (fun (id, n) -> issue "V1" id $"identifier used {n} times")

/// V2: every expense carries the ten required attributes (mission 2, "establish expense triggers").
let gExpenseFields (e: Expense) =
    [ if isBlank e.Id then yield "identifier"
      if isBlank e.Purpose then yield "purpose"
      if List.isEmpty e.EvidenceIds then yield "evidence source"
      if not (entities.Contains e.Entity) then yield $"accountable entity ('{e.Entity}' not in E1/E3/E4/E5)"
      if e.TriggerMetric <> Always && e.TriggerThreshold < 0.0 then yield "triggering condition"
      if e.MinAnnual.Low < 0.0 then yield "minimum cost"
      if e.Amount.Low < 0.0 then yield "likely cost range"
      if isBlank e.CapacityLimit then yield "capacity limit"
      if isBlank e.Alternative then yield "alternative approach"
      if isBlank e.Consequence then yield "consequence of not incurring" ]
    |> List.map (fun f -> issue "V2" e.Id $"missing or invalid {f}")

/// V3: every cited evidence identifier exists in the source register.
let gEvidence (inp: Inputs) =
    let known = inp.Sources |> List.map (fun s -> s.Id) |> Set.ofList
    let check subject ids = ids |> List.filter (known.Contains >> not) |> List.map (fun i -> issue "V3" subject $"unknown evidence id {i}")
    [ for e in inp.Expenses do yield! check e.Id e.EvidenceIds
      for a in inp.Activities do yield! check a.Id a.EvidenceIds
      for r in inp.Roles do yield! check r.Id r.EvidenceIds
      for c in inp.Coverage do yield! check c.Id c.EvidenceIds
      for p in inp.Profiles do yield! check p.Id p.EvidenceIds
      for (id, _, _, _, ev) in inp.Qualification do yield! check id ev ]

/// V4: every human activity answers the ten challenge questions; decisions reserved to the sponsor are never
/// performed by Echelon Foundry (CNV-GOV-004: vendor staff may not hold A3+ authority; UNB-CDD-CMF-002).
let gActivity (a: Activity) =
    [ if isBlank a.Why then yield issue "V4" a.Id "missing 'why the activity exists'"
      for (q, v) in [ "legally_required", a.LegallyRequired; "contractually_required", a.ContractuallyRequired; "preventable", a.Preventable
                      "deterministic", a.Deterministic; "ai_assist", a.AiAssist ] do
          if not (answers.Contains v) then yield issue "V4" a.Id $"{q}='{v}' not in Y/N/U/partial"
      if not (decisionHolders.Contains a.HumanDecision) then yield issue "V4" a.Id $"human_decision='{a.HumanDecision}' not in sponsor/ef/none"
      if a.Rate.High <= 0.0 then yield issue "V4" a.Id "frequency must be positive"
      if a.Minutes.High <= 0.0 then yield issue "V4" a.Id "duration must be positive"
      if isBlank a.StaffingNote then yield issue "V4" a.Id "missing staffing trigger note"
      if a.HumanDecision = "sponsor" && not a.EfModels.IsEmpty then
          yield issue "V4" a.Id "a sponsor-reserved decision cannot be borne by Echelon Foundry"
      if Set.intersect a.EfModels a.SponsorModels |> Set.isEmpty |> not then yield issue "V4" a.Id "an activity is borne by one party per model" ]

/// V5: controls are not modelled away. A legally or contractually required activity that needs a human decision
/// keeps a positive human share at every level.
let gControls (a: Activity) =
    if (a.LegallyRequired = "Y" || a.ContractuallyRequired = "Y") && a.HumanDecision <> "none" && a.HumanShare.Low <= 0.0 then
        [ issue "V5" a.Id "required human control has a zero human share" ]
    else []

/// V6: no role exists without a workload or a mandatory-coverage justification (no conventional staffing).
let gRoles (inp: Inputs) =
    let byWork = inp.Activities |> List.map (fun a -> a.Role) |> Set.ofList |> Set.add "management"
    let byCov = inp.Coverage |> List.map (fun c -> c.Role) |> Set.ofList
    let known = inp.Roles |> List.map (fun r -> r.Id) |> Set.ofList
    [ for r in inp.Roles do
          if not (byWork.Contains r.Id || byCov.Contains r.Id) then
              yield issue "V6" r.Id "role has no workload and no coverage requirement: remove it"
          if r.ProductiveHours <= 0.0 then yield issue "V6" r.Id "productive hours must be positive"
      for a in inp.Activities do
          if not (known.Contains a.Role) then yield issue "V6" a.Id $"unknown role '{a.Role}'"
      for c in inp.Coverage do
          if not (known.Contains c.Role) then yield issue "V6" c.Id $"unknown role '{c.Role}'"
      if not (known.Contains "management") then yield issue "V6" "management" "the founder-overhead role 'management' must exist" ]

/// V7: shares and bearers are coherent.
let gShares (e: Expense) =
    let inUnit (r: Range) = r.Low >= 0.0 && r.High <= 1.0
    [ if not (inUnit e.IncrementalShare) then yield issue "V7" e.Id "incremental share outside [0,1]"
      if not (inUnit e.AllocationShare) then yield issue "V7" e.Id "allocation share outside [0,1]"
      if e.EfModels.IsEmpty && e.SponsorModels.IsEmpty then yield issue "V7" e.Id "borne by nobody"
      if Set.intersect e.EfModels e.SponsorModels |> Set.isEmpty |> not then yield issue "V7" e.Id "borne by both parties in one model"
      if e.Class = Shared && e.IncrementalShare.High >= 1.0 then yield issue "V7" e.Id "shared expense cannot be fully incremental"
      if e.Class <> Shared && e.IncrementalShare.Low < 1.0 then yield issue "V7" e.Id "only shared-infrastructure expenses may be partly non-incremental" ]

/// V8: parameters, mixes and profiles resolve.
let gParams (inp: Inputs) =
    [ for p in requiredParams do
          if not (inp.Params.ContainsKey p) then yield issue "V8" p "required parameter missing"
      let profiles = inp.Profiles |> List.map (fun p -> p.Id) |> Set.ofList
      for m in inp.Mixes do
          for p in m.Pattern do
              if not (profiles.Contains p) then yield issue "V8" m.Id $"unknown profile '{p}'"
      for req in [ "mixed"; "prior-5x2000" ] do
          if not (inp.Mixes |> List.exists (fun m -> m.Id = req)) then yield issue "V8" req "required mix missing" ]

/// V9: relative links in the package's Markdown resolve.
let linkRe = Regex(@"\]\(([^)#\s]+)(#[^)]*)?\)")
let gLinks (docs: (string * string) list) (exists: string -> string -> bool) =
    [ for (path, text) in docs do
          for m in linkRe.Matches(text) do
              let target = m.Groups.[1].Value
              if not (target.StartsWith "http" || target.StartsWith "mailto:") && not (exists path target) then
                  yield issue "V9" path $"broken link {target}" ]

let all (inp: Inputs) (docs: (string * string) list) (exists: string -> string -> bool) =
    gUnique inp
    @ (inp.Expenses |> List.collect gExpenseFields)
    @ gEvidence inp
    @ (inp.Activities |> List.collect gActivity)
    @ (inp.Activities |> List.collect gControls)
    @ gRoles inp
    @ (inp.Expenses |> List.collect gShares)
    @ gParams inp
    @ gLinks docs exists
