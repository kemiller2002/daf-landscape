/// Parsing of the machine-readable inputs into domain records. Pure: takes CSV text, returns Result.
module ZeroBasedEconomics.Inputs

open System
open ZeroBasedEconomics.Domain
open ZeroBasedEconomics.Csv

type Params = Map<string, Range>

type Inputs =
    { Expenses: Expense list
      Activities: Activity list
      Roles: Role list
      Coverage: Coverage list
      Profiles: Profile list
      Mixes: Mix list
      Params: Params
      Qualification: (string * string * Range * Range * string list) list
      Priors: PriorEstimate list
      Sources: Source list }

/// Collect a list of results into a result of list, keeping every error.
let sequence (xs: Result<'a, string> list) : Result<'a list, string> =
    let oks = xs |> List.choose (function Ok x -> Some x | Error _ -> None)
    let errs = xs |> List.choose (function Error e -> Some e | Ok _ -> None)
    if List.isEmpty errs then Ok oks else Error(String.concat "\n" errs)

type ResultBuilder() =
    member _.Bind(r, f) = Result.bind f r
    member _.Return x = Ok x
    member _.ReturnFrom r = r

let result = ResultBuilder()

let private s key row = get key row |> Result.map (fun v -> v.Trim())

let private split (v: string) =
    v.Split([| ';'; ' ' |], StringSplitOptions.RemoveEmptyEntries) |> Array.toList |> List.map (fun x -> x.Trim())

let private models key row =
    s key row
    |> Result.bind (fun v -> if v = "" || v = "-" then Ok Set.empty else split v |> List.map parseModel |> sequence |> Result.map Set.ofList)

let private range prefix row =
    result {
        let! lo = num (prefix + "_low") row
        let! b = num (prefix + "_base") row
        let! hi = num (prefix + "_high") row
        return! if lo <= b && b <= hi then Ok { Low = lo; Base = b; High = hi } else Error $"range '{prefix}' not ordered: {lo} {b} {hi}"
    }

let private yesNo key row =
    s key row |> Result.bind (fun v -> match v with "Y" -> Ok true | "N" -> Ok false | x -> Error $"'{key}' must be Y or N, got '{x}'")

let private withRow (id: string) (r: Result<'a, string>) = r |> Result.mapError (fun e -> $"{id}: {e}")

let parseDriver (kind: string) (metric: string) (capacity: string) =
    match kind.Trim() with
    | "fixed" -> Ok Fixed
    | "per" -> parseMetric metric |> Result.map Per
    | "step" ->
        parseMetric metric
        |> Result.bind (fun m ->
            match Double.TryParse(capacity, Globalization.NumberStyles.Float, Globalization.CultureInfo.InvariantCulture) with
            | true, c when c > 0.0 -> Ok(Step(m, c))
            | _ -> Error $"step driver needs a positive capacity, got '{capacity}'")
    | x -> Error $"unknown driver '{x}'"

let expense (row: Row) : Result<Expense, string> =
    let id = Map.tryFind "expense_id" row |> Option.defaultValue "?"
    withRow id (result {
        let! cls = s "classification" row |> Result.bind parseClass
        let! ob = s "obligation" row |> Result.bind parseObligation
        let! tm = s "trigger_metric" row |> Result.bind parseMetric
        let! tt = num "trigger_threshold" row
        let! dk = s "driver" row
        let! dm = s "driver_metric" row
        let! cap = s "capacity_per_unit" row
        let! drv = parseDriver dk dm cap
        let! mn = range "min" row
        let! amt = range "amount" row
        let! inc = range "incremental" row
        let! alloc = range "allocation" row
        let! pre = yesNo "prepaid" row
        let! ef = models "ef_models" row
        let! sp = models "sponsor_models" row
        let! name = s "name" row
        let! purpose = s "purpose" row
        let! cat = s "category" row
        let! ent = s "entity" row
        let! ev = s "evidence_ids" row
        let! capl = s "capacity_limit" row
        let! alt = s "alternative" row
        let! cons = s "consequence" row
        return
            { Id = id; Name = name; Purpose = purpose; Category = cat; Class = cls; Obligation = ob; Entity = ent
              EvidenceIds = split ev; TriggerMetric = tm; TriggerThreshold = tt; Driver = drv; MinAnnual = mn; Amount = amt
              IncrementalShare = inc; AllocationShare = alloc; CapacityLimit = capl; Alternative = alt; Consequence = cons
              Prepaid = pre; EfModels = ef; SponsorModels = sp }
    })

let activity (row: Row) : Result<Activity, string> =
    let id = Map.tryFind "activity_id" row |> Option.defaultValue "?"
    withRow id (result {
        let! d = s "driver" row |> Result.bind parseActDriver
        let! rate = range "rate" row
        let! share = range "human_share" row
        let! mins = range "minutes" row
        let! conv = num "conventional_minutes" row
        let! ef = models "ef_models" row
        let! sp = models "sponsor_models" row
        let! name = s "name" row
        let! why = s "why" row
        let! lg = s "legally_required" row
        let! ct = s "contractually_required" row
        let! pv = s "preventable" row
        let! dt = s "deterministic" row
        let! ai = s "ai_assist" row
        let! hd = s "human_decision" row
        let! role = s "role" row
        let! ev = s "evidence_ids" row
        let! note = s "staffing_note" row
        let! minc = num "min_customers" row
        return
            { Id = id; Name = name; Why = why; LegallyRequired = lg; ContractuallyRequired = ct; Preventable = pv
              Deterministic = dt; AiAssist = ai; HumanDecision = hd; Driver = d; Rate = rate; HumanShare = share
              Minutes = mins; ConventionalMinutes = conv; Role = role; EfModels = ef; SponsorModels = sp
              EvidenceIds = split ev; StaffingNote = note; MinCustomers = int minc }
    })

let role (row: Row) : Result<Role, string> =
    let id = Map.tryFind "role_id" row |> Option.defaultValue "?"
    withRow id (result {
        let! loaded = range "loaded_annual" row
        let! hourly = range "contract_hourly" row
        let! fe = yesNo "founder_eligible" row
        let! ph = num "productive_hours" row
        let! ht = num "hire_threshold_hours" row
        let! name = s "name" row
        let! purpose = s "purpose" row
        let! ev = s "evidence_ids" row
        let! q = s "qualification" row
        let! alt = s "alternative" row
        let! cons = s "consequence" row
        return
            { Id = id; Name = name; Purpose = purpose; EvidenceIds = split ev; LoadedAnnual = loaded; ContractHourly = hourly
              FounderEligible = fe; ProductiveHours = ph; HireThresholdHours = ht; Qualification = q; Alternative = alt
              Consequence = cons }
    })

let coverage (row: Row) : Result<Coverage, string> =
    let id = Map.tryFind "coverage_id" row |> Option.defaultValue "?"
    withRow id (result {
        let! ob = s "obligation" row |> Result.bind parseObligation
        let! ms = models "models" row
        let! tc = num "trigger_customers" row
        let! mp = num "min_people" row
        let! aa = yesNo "alt_allowed" row
        let! alt = range "alt_annual" row
        let! d = s "description" row
        let! b = s "basis" row
        let! r = s "role" row
        let! ad = s "alt_description" row
        let! ev = s "evidence_ids" row
        return
            { Id = id; Description = d; Basis = b; Obligation = ob; Models = ms; TriggerCustomers = int tc; MinPeople = int mp
              Role = r; AltAllowed = aa; AltDescription = ad; AltAnnual = alt; EvidenceIds = split ev }
    })

let profile (row: Row) : Result<Profile, string> =
    let id = Map.tryFind "profile_id" row |> Option.defaultValue "?"
    withRow id (result {
        let! a = range "accounts" row
        let! u = range "aua_per_account" row
        let! g = range "grants_per_account" row
        let! c = range "contribs_per_account" row
        let! e = range "exception_rate" row
        let! n = s "name" row
        let! ev = s "evidence_ids" row
        return { Id = id; Name = n; Accounts = a; AuaPerAccount = u; GrantsPerAccount = g; ContribsPerAccount = c; ExceptionRate = e; EvidenceIds = split ev }
    })

let mix (row: Row) : Result<Mix, string> =
    result {
        let! id = s "mix_id" row
        let! n = s "name" row
        let! p = s "pattern" row
        return { Id = id; Name = n; Pattern = split p }
    }

let param (row: Row) : Result<string * Range, string> =
    result {
        let! n = s "name" row
        let! r = range "value" row |> withRow n
        return n, r
    }

let qualification (row: Row) =
    result {
        let! id = s "item_id" row
        let! n = s "name" row
        let! h = range "founder_hours" row |> withRow id
        let! c = range "cash" row |> withRow id
        let! ev = s "evidence_ids" row
        return id, n, h, c, split ev
    }

let prior (row: Row) : Result<PriorEstimate, string> =
    result {
        let! id = s "prior_id" row
        let! n = s "name" row
        let! v = s "value" row
        let! src = s "source" row
        let! oa = s "original_assumptions" row
        let! eq = s "evidence_quality" row
        let! ob = s "applicable_obligations" row
        let! ca = s "unnecessary_conventional_assumptions" row
        let! rp = s "replacement_mechanisms" row
        let! cm = s "comparable_metric" row
        let! u = s "remaining_uncertainty" row
        return
            { Id = id; Name = n; Value = v; Source = src; OriginalAssumptions = oa; EvidenceQuality = eq; Obligations = ob
              ConventionalAssumptions = ca; Replacements = rp; ComparableMetric = cm; Uncertainty = u }
    }

let source (row: Row) : Result<Source, string> =
    result {
        let! id = s "source_id" row
        let! t = s "title" row
        let! l = s "location" row
        let! e = s "evidence_class" row
        return { Id = id; Title = t; Location = l; EvidenceClass = e }
    }

let rows (f: Row -> Result<'a, string>) (text: string) = text |> parse |> snd |> List.map f |> sequence

/// Build all inputs from a lookup of file name -> CSV text.
let build (read: string -> string) : Result<Inputs, string> =
    let r name f = rows f (read name) |> Result.mapError (fun e -> $"{name}:\n{e}")
    match
        r "expenses.csv" expense, r "activities.csv" activity, r "roles.csv" role, r "coverage.csv" coverage,
        r "profiles.csv" profile, r "mixes.csv" mix, r "parameters.csv" param
    with
    | Ok ex, Ok ac, Ok ro, Ok co, Ok pr, Ok mx, Ok pa ->
        match r "qualification.csv" qualification, r "prior-estimates.csv" prior, r "sources.csv" source with
        | Ok q, Ok pe, Ok so ->
            Ok
                { Expenses = ex; Activities = ac; Roles = ro; Coverage = co; Profiles = pr; Mixes = mx; Params = Map.ofList pa
                  Qualification = q; Priors = pe; Sources = so }
        | a, b, c -> [ a |> Result.map ignore; b |> Result.map ignore; c |> Result.map ignore ] |> sequence |> Result.bind (fun _ -> Error "unreachable")
    | a, b, c, d, e, f, g ->
        [ a |> Result.map ignore; b |> Result.map ignore; c |> Result.map ignore; d |> Result.map ignore
          e |> Result.map ignore; f |> Result.map ignore; g |> Result.map ignore ]
        |> sequence
        |> Result.bind (fun _ -> Error "unreachable")
