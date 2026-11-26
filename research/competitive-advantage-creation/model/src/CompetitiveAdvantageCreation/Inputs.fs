/// Typed model inputs and their parsers. Parsers return Result and reject invalid assumptions (unordered or negative
/// ranges, unknown fields); nothing throws.
module CompetitiveAdvantageCreation.Inputs

open System
open System.Globalization
open CompetitiveAdvantageCreation.Domain
open CompetitiveAdvantageCreation.Csv

type PoolInput = { Id: string; Name: string; Annual: Range; AssumptionIds: string list }

type ScenarioInput =
    { Id: string
      Name: string
      PriceCut: Range
      WinRateReduction: Range
      PartnerShare: Range
      Termination: Range option
      AssumptionIds: string list }

type MvpInput =
    { Fixed: (string * (string * float) list) list
      Variable: (string * float) list
      Balances: float list
      Fees: float list }

/// Platform class of a sponsor (Revision 3, REV4006). Rule, from the panel's own fields (SRC-013):
/// donation processors -> "processor"; a third-party DAF administration vendor named in the sponsor's Form 990
/// vendor field (Ren, NPact, Gloo, TASC, Foundant, DonorFirst, FIMS) or a mapped community-foundation software family -> 
/// "third-party platform"; other national standard sponsors -> "own platform (presumed)"; everything else ->
/// "unknown". Absence of vendor evidence is not proof of an own platform; the presumption is reported as such.
type Sponsor = { Category: string; Platform: string; Accounts: float }

let adminVendors = [ "Ren"; "NPact"; "Gloo"; "Total Administrative Services"; "Foundant"; "DonorFirst"; "FIMS" ]

let platformClass (category: string) (vendors: string) (cfVendor: string) =
    if category = "donation_processor" then "processor"
    elif adminVendors |> List.exists (fun v -> vendors.Contains v) || (cfVendor.Trim() <> "" && cfVendor.Trim() <> "Unmapped") then "third-party platform"
    elif category = "national_standard" then "own platform (presumed)"
    else "unknown"

type Inputs =
    { Params: Params
      Settings: Map<string, string>
      States: Capital.StateInput list
      Events: Events.EventWork list
      RegistryComponents: Registry.Component list
      Routes: (Phase2Check.Route * float) list
      Mvp: MvpInput
      Pools: PoolInput list
      Products: SharedInfra.Product list
      Scenarios: ScenarioInput list
      Streams: Sequences.StreamInput list
      Metas: Sequences.SequenceMeta list
      /// FY2024 sponsor panel (SRC-013).
      Sponsors: Sponsor list }

let ids (s: string) = s.Split(';', StringSplitOptions.RemoveEmptyEntries ||| StringSplitOptions.TrimEntries) |> List.ofArray

let private numStr (s: string) =
    match Double.TryParse(s.Trim(), NumberStyles.Float, CultureInfo.InvariantCulture) with
    | true, x -> Some x
    | _ -> None

let private rangeOf (name: string) (allowNeg: bool) (lo: string) (b: string) (hi: string) : Result<Range, string> =
    match numStr lo, numStr b, numStr hi with
    | Some l, Some m, Some h -> validateRange name allowNeg { Low = l; Base = m; High = h }
    | _ -> Error $"{name}: non-numeric range ({lo}, {b}, {hi})"

let private col (row: Row) key = Map.tryFind key row |> Option.defaultValue ""

let private rangeCols (name: string) (allowNeg: bool) (prefix: string) (row: Row) =
    rangeOf name allowNeg (col row (prefix + "_low")) (col row (prefix + "_base")) (col row (prefix + "_high"))

let parseParams (rows: Row list) : Result<Params, string list> =
    rows
    |> List.map (fun r ->
        let name = col r "name"
        let allowNeg = col r "allow_negative" = "Y"
        rangeOf name allowNeg (col r "low") (col r "base") (col r "high")
        |> Result.bind (fun rg ->
            match col r "adverse" with
            | "high" -> Ok { Name = name; Range = rg; Unit = col r "unit"; Adverse = HighIsAdverse; AllowNegative = allowNeg; AssumptionIds = ids (col r "assumption_ids") }
            | "low" -> Ok { Name = name; Range = rg; Unit = col r "unit"; Adverse = LowIsAdverse; AllowNegative = allowNeg; AssumptionIds = ids (col r "assumption_ids") }
            | x -> Error $"{name}: adverse must be high or low, got '{x}'"))
    |> collect
    |> Result.bind (fun ps ->
        let dupes = ps |> List.countBy (fun p -> p.Name) |> List.filter (fun (_, n) -> n > 1) |> List.map (fun (n, _) -> $"duplicate parameter {n}")
        if List.isEmpty dupes then Ok(ps |> List.map (fun p -> p.Name, p) |> Map.ofList) else Error dupes)

let requiredParams =
    [ "contingency"; "capital_charge"; "founder_econ"; "revenue_per_customer_channel"; "customers_per_year_channel"; "churn"
      "arrears_months"; "cac_later"; "impl_later"; "var_per_account"; "net_price_per_account_channel"; "ab_variable_share_as_published"
      "build_phase_burn_factor"; "labour_per_minute"; "automation_residual_share"; "ai_cost_share"; "transfer_efficiency"
      "accounts_per_sponsor"; "connectors"; "registry_charities"; "registry_engineering_absorbed"; "partner_share"
      "partner_sales_cycle"; "partner_deals"; "partner_enablement"; "direct_cac"; "revenue_per_sponsor"; "licence_life"
      "discount_rate"; "agreement_years"; "price_per_account"; "minimum_fee"; "migration_assessment_fee"; "headline_price"
      "md6_fixed"; "md6_variable"; "tax_rate"; "review_frequency"; "tiered_review_factor"; "partner_termination_rate"; "conventional_maintenance_extra"; "customer_impl_recovery"; "customer_advance_months"; "partner_funded_share"
      "partner_share_uplift"; "external_cost_of_capital"; "external_raise_cost" ]

let checkRequired (ps: Params) =
    requiredParams |> List.filter (fun n -> not (Map.containsKey n ps)) |> List.map (fun n -> $"missing parameter '{n}'")

let parseSettings (rows: Row list) = rows |> List.map (fun r -> col r "key", col r "value") |> Map.ofList

let parseStates (rows: Row list) : Result<Capital.StateInput list, string list> =
    let lineOf (r: Row) =
        let name = col r "state_id" + " " + col r "category"
        match rangeCols (name + " cash") false "cash" r, rangeCols (name + " econ") false "econ" r with
        | Ok c, Ok e -> Ok(col r "state_id", col r "state", col r "category", ({ Cash = c; Econ = e; Ids = ids (col r "assumption_ids") }: Capital.Line))
        | Error a, _ | _, Error a -> Error a
    rows
    |> List.map lineOf
    |> collect
    |> Result.bind (fun lines ->
        lines
        |> List.groupBy (fun (sid, _, _, _) -> sid)
        |> List.map (fun (sid, ls) ->
            let find k = ls |> List.tryFind (fun (_, _, c, _) -> c = k) |> Option.map (fun (_, _, _, l) -> l)
            let req k = match find k with Some l -> Ok l | None -> Error $"{sid}: missing category {k}"
            let name = ls |> List.head |> fun (_, n, _, _) -> n
            let recurring = ls |> List.choose (fun (_, _, c, l) -> if c.StartsWith "recurring:" then Some(c.Substring 10, l) else None) |> List.sortBy fst
            match req "sunk", req "dev", req "cac", req "impl", req "compliance_onetime", req "legal", req "working_capital", req "pre_run", req "pre_months", req "golive_months", req "founder_pre", req "founder_live" with
            | Ok su, Ok dv, Ok ca, Ok im, Ok co, Ok le, Ok wc, Ok pr, Ok pm, Ok gm, Ok fp, Ok fl ->
                Ok({ StateId = sid; Name = name; Sunk = su; Dev = dv; Cac = ca; Impl = im; ComplianceOnetime = co; Legal = le
                     WorkingCapital = wc; PreRun = pr; PreMonths = pm.Cash; GoLiveMonths = gm.Cash; Recurring = recurring
                     FounderPre = fp; FounderLive = fl }: Capital.StateInput)
            | rs ->
                let (a, b, c, d, e, f, g, h, i, j, k, l) = rs
                Error([ a; b; c; d; e; f; g; h; i; j; k; l ] |> List.choose (function Error x -> Some x | Ok _ -> None) |> String.concat "; "))
        |> collect)

let parseEvents (rows: Row list) : Result<Events.EventWork list, string list> =
    rows
    |> List.map (fun r ->
        let n k = numStr (col r k)
        match n "conventional_min", n "eliminated_min", n "automated_min", n "accelerated_min", n "transferred_to_customer_min", n "transferred_to_partner_min", n "residual_mandatory_min", n "residual_other_min" with
        | Some c, Some el, Some au, Some ac, Some tc, Some tp, Some md, Some ro ->
            Events.validate 0.01
                { EventId = col r "event_id"; Event = col r "event"; Scenario = col r "scenario"; Conventional = c; Eliminated = el
                  Automated = au; Accelerated = ac; ToCustomer = tc; ToPartner = tp; Mandatory = md; ResidualOther = ro }
        | _ -> Error $"""{col r "event_id"} {col r "scenario"}: non-numeric minutes""")
    |> collect

let parseComponents (rows: Row list) : Result<Registry.Component list, string list> =
    rows
    |> List.map (fun r ->
        let id = col r "component_id"
        let scaling =
            match col r "scaling" with
            | "registry" -> Ok Registry.PerRegistry
            | "connector" -> Ok Registry.PerConnector
            | "union" -> Ok Registry.PerUnionCharity
            | "sponsor" -> Ok Registry.PerSponsor
            | "sponsor_charity" -> Ok Registry.PerSponsorCharity
            | "floor" -> Ok Registry.OwnerFloor
            | "parameter" -> Ok Registry.Parameter
            | x -> Error $"{id}: unknown scaling '{x}'"
        let kind =
            match col r "kind" with
            | "engineering" -> Ok Registry.Engineering
            | "counsel" -> Ok Registry.Counsel
            | "labour" -> Ok Registry.SharedLabour
            | "deep_review" -> Ok Registry.DeepReview
            | "sponsor" -> Ok Registry.SponsorSpecific
            | "floor" -> Ok Registry.Floor
            | "driver" -> Ok Registry.Driver
            | x -> Error $"{id}: unknown kind '{x}'"
        match rangeCols id false "cost" r, scaling, kind with
        | Ok rg, Ok s, Ok k ->
            Ok({ Id = id; Name = col r "component"; Modes = col r "modes" |> ids; Cost = rg; Scaling = s; Kind = k; AssumptionIds = ids (col r "assumption_ids") }: Registry.Component)
        | Error e, _, _ | _, Error e, _ | _, _, Error e -> Error e)
    |> collect

let parseRoutes (rows: Row list) : Result<(Phase2Check.Route * float) list, string list> =
    rows
    |> List.map (fun r ->
        let n k = numStr (col r k)
        match n "build", n "burn", n "first_revenue_month", n "revenue_per_customer", n "customers_per_year", n "variable_share", n "cac", n "churn", n "golive_lag", n "channel_share" with
        | Some b, Some bu, Some f, Some rv, Some cu, Some vs, Some cac, Some ch, Some gl, Some cs ->
            Ok(({ Id = col r "route_id"; Build = b; Burn = bu; FirstRevenueMonth = f; RevenuePerCustomer = rv; CustomersPerYear = cu
                  Recurring = col r "recurring" = "Y"; VariableShare = vs; Cac = cac; Churn = ch; GoLiveLag = gl }: Phase2Check.Route), cs)
        | _ -> Error $"""{col r "route_id"}: non-numeric route value""")
    |> collect

let parseMvp (rows: Row list) : Result<MvpInput, string list> =
    let order = [ "low"; "base"; "high" ]
    let values (dim: string) =
        rows |> List.filter (fun r -> col r "dimension" = dim) |> List.sortBy (fun r -> List.findIndex ((=) (col r "key")) order)
        |> List.map (fun r -> col r "key", (numStr (col r "value") |> Option.defaultValue nan))
    let hosts = rows |> List.map (fun r -> col r "dimension") |> List.filter (fun d -> d.StartsWith "fixed:") |> List.distinct
    let m =
        { Fixed = hosts |> List.map (fun h -> h.Substring 6, values h)
          Variable = values "variable"
          Balances = values "balance" |> List.map snd
          Fees = values "fee" |> List.map snd }
    let all = (m.Fixed |> List.collect snd |> List.map snd) @ (m.Variable |> List.map snd) @ m.Balances @ m.Fees
    if all |> List.exists (fun x -> Double.IsNaN x || x < 0.0) then Error [ "mvp-grid.csv: non-numeric or negative value" ] else Ok m

let parsePools (rows: Row list) : Result<PoolInput list, string list> =
    rows
    |> List.map (fun r -> rangeCols (col r "pool_id") false "annual" r |> Result.map (fun rg -> { Id = col r "pool_id"; Name = col r "pool"; Annual = rg; AssumptionIds = ids (col r "assumption_ids") }))
    |> collect

let parseProducts (rows: Row list) : Result<SharedInfra.Product list, string list> =
    rows
    |> List.map (fun r ->
        let drivers = [ "usage"; "revenue"; "standalone" ] |> List.map (fun k -> k, numStr (col r k))
        match Cashflow.parseEntity (col r "entity") with
        | Error e -> Error e
        | Ok _ when drivers |> List.exists (fun (_, v) -> match v with Some x -> x < 0.0 | None -> true) -> Error(col r "product_id" + ": missing or negative driver")
        | Ok e ->
            Ok({ Id = col r "product_id"; Name = col r "product"; Entity = e; RevenueBearing = col r "revenue_bearing" = "Y"
                 Drivers = drivers |> List.map (fun (k, v) -> k, Option.get v) |> Map.ofList }: SharedInfra.Product))
    |> collect

let parseScenarios (rows: Row list) : Result<ScenarioInput list, string list> =
    rows
    |> List.map (fun r ->
        let id = col r "scenario_id"
        let term =
            if col r "termination_month_base" = "" then Ok None
            else rangeCols (id + " termination") false "termination_month" r |> Result.map Some
        match rangeCols (id + " price_cut") false "price_cut" r, rangeCols (id + " win") false "win_rate_reduction" r, rangeCols (id + " share") false "partner_share" r, term with
        | Ok p, Ok w, Ok s, Ok t ->
            if p.High > 1.0 || w.High > 1.0 || s.High > 1.0 then Error $"{id}: shares must be <= 1"
            else Ok { Id = id; Name = col r "scenario"; PriceCut = p; WinRateReduction = w; PartnerShare = s; Termination = t; AssumptionIds = ids (col r "assumption_ids") }
        | Error e, _, _, _ | _, Error e, _, _ | _, _, Error e, _ | _, _, _, Error e -> Error e)
    |> collect

/// Streams with templates resolved (a template's values are inherited and overridden by the stream's own rows).
let parseStreams (streamRows: Row list) (valueRows: Row list) : Result<Sequences.StreamInput list, string list> =
    let known = Sequences.fields |> List.map fst |> Set.ofList
    let valuesFor sid =
        valueRows
        |> List.filter (fun r -> col r "stream_id" = sid)
        |> List.map (fun r ->
            let f = col r "field"
            if not (Set.contains f known) then Error $"{sid}: unknown field '{f}'"
            else rangeOf $"{sid}.{f}" false (col r "low") (col r "base") (col r "high") |> Result.map (fun rg -> f, rg, ids (col r "assumption_ids")))
        |> collect
    let byId = streamRows |> List.map (fun r -> col r "stream_id", r) |> Map.ofList
    let rec resolve (depth: int) (sid: string) : Result<Map<string, Range> * string list, string list> =
        if depth > 5 then Error [ $"{sid}: template chain too deep" ]
        else
            match Map.tryFind sid byId with
            | None -> Error [ $"unknown stream or template '{sid}'" ]
            | Some r ->
                let parent = if col r "template" = "" then Ok(Map.empty, []) else resolve (depth + 1) (col r "template")
                match parent, valuesFor sid with
                | Ok(pm, pids), Ok own ->
                    Ok(own |> List.fold (fun m (f, rg, _) -> Map.add f rg m) pm, (pids @ (own |> List.collect (fun (_, _, i) -> i))) |> List.distinct)
                | Error a, Error b -> Error(a @ b)
                | Error a, _ | _, Error a -> Error a
    streamRows
    |> List.filter (fun r -> col r "seq_id" <> "TEMPLATE")
    |> List.map (fun r ->
        let sid = col r "stream_id"
        match resolve 0 sid, Cashflow.parseEntity (col r "entity") with
        | Ok(values, aids), Ok e ->
            let reg = col r "uses_registry"
            if not (List.contains reg [ "N"; "live"; "all"; "all-conditional" ]) then Error [ $"{sid}: uses_registry must be N, live, all or all-conditional" ]
            else
                Ok({ SeqId = col r "seq_id"; StreamId = sid; Name = col r "stream"; Entity = e; Dedicated = col r "dedicated" = "Y"
                     KillExempt = col r "kill_exempt" = "Y"; Recurring = col r "recurring" = "Y"; UsesRegistry = reg
                     Values = values; AssumptionIds = aids }: Sequences.StreamInput)
        | Error es, _ -> Error es
        | _, Error e -> Error [ e ])
    |> List.fold (fun acc r -> match acc, r with
                               | Ok xs, Ok x -> Ok(xs @ [ x ])
                               | Error a, Error b -> Error(a @ b)
                               | Error a, _ | _, Error a -> Error a) (Ok [])

let parseMetas (rows: Row list) : Result<Sequences.SequenceMeta list, string list> =
    rows
    |> List.map (fun r ->
        let sid = col r "seq_id"
        let cc =
            match col r "cost_center" with
            | "none" -> Ok Sequences.NoCostCenter
            | "derived" -> Ok Sequences.Derived
            | x -> match numStr x with
                   | Some v when v >= 0.0 -> Ok(Sequences.Fixed(point v))
                   | _ -> Error $"{sid}: cost_center must be derived, none or a month"
        let band = col r "failure_band"
        if not (List.contains band [ "low"; "moderate"; "high"; "very high" ]) then Error $"{sid}: failure_band '{band}' not in vocabulary"
        else
            match rangeOf (sid + " named partner") false (col r "named_partner_low") (col r "named_partner_base") (col r "named_partner_high"), cc with
            | Ok np, Ok c ->
                Ok({ SeqId = sid; RegisterId = col r "register_id"; Label = col r "label"; Name = col r "sequence"; StartState = col r "start_state"
                     NamedPartnerMonth = np; CostCenter = c; FailureBand = band
                     Reversibility = col r "reversibility"; Optionality = col r "optionality"; Dependencies = col r "dependencies"
                     OpportunityCost = col r "opportunity_cost"; AssumptionIds = ids (col r "assumption_ids") }: Sequences.SequenceMeta)
            | Error e, _ | _, Error e -> Error e)
    |> collect

let parseSponsors (rows: Row list) : Result<Sponsor list, string list> =
    rows
    |> List.map (fun r ->
        match numStr (col r "daf_accounts_fy2024") with
        | Some a when a > 0.0 ->
            let cat = col r "sponsor_category"
            Ok { Category = cat; Platform = platformClass cat (col r "vendors_990_daf_relevant") (col r "cf_vendor_family"); Accounts = a }
        | _ -> Error("sponsor-sizes.csv: bad accounts for " + col r "ein"))
    |> collect

let inputFiles =
    [ "parameters.csv"; "settings.csv"; "capital-states.csv"; "event-work.csv"; "registry-components.csv"; "phase2-routes.csv"; "mvp-grid.csv"
      "shared-infra-pools.csv"; "shared-infra-products.csv"; "response-scenarios.csv"; "sequence-streams.csv"; "sequence-values.csv"; "sequence-meta.csv"; "sponsor-sizes.csv" ]

/// Parse every input file (given as name -> text).
let load (read: string -> string) : Result<Inputs, string list> =
    let rows f = read f |> parse |> snd
    let ps = parseParams (rows "parameters.csv")
    let req = match ps with Ok p -> checkRequired p | Error _ -> []
    let r =
        ps, parseStates (rows "capital-states.csv"), parseEvents (rows "event-work.csv"), parseComponents (rows "registry-components.csv"),
        parseRoutes (rows "phase2-routes.csv"), parseMvp (rows "mvp-grid.csv"), parsePools (rows "shared-infra-pools.csv"),
        parseProducts (rows "shared-infra-products.csv"), parseScenarios (rows "response-scenarios.csv"),
        parseStreams (rows "sequence-streams.csv") (rows "sequence-values.csv"), parseMetas (rows "sequence-meta.csv")
    let sponsors = parseSponsors (rows "sponsor-sizes.csv")
    match r, sponsors with
    | (Ok p, Ok st, Ok ev, Ok rc, Ok ro, Ok mv, Ok po, Ok pr, Ok sc, Ok sm, Ok me), Ok sp when List.isEmpty req ->
        let settings = parseSettings (rows "settings.csv")
        let missingSeq = me |> List.filter (fun m -> not (sm |> List.exists (fun s -> s.SeqId = m.SeqId))) |> List.map (fun m -> $"{m.SeqId}: no streams")
        if not (List.isEmpty missingSeq) then Error missingSeq
        else
            Ok { Params = p; Settings = settings; States = st; Events = ev; RegistryComponents = rc; Routes = ro; Mvp = mv; Pools = po
                 Products = pr; Scenarios = sc; Streams = sm; Metas = me; Sponsors = sp }
    | (p, st, ev, rc, ro, mv, po, pr, sc, sm, me), sp ->
        let e x = match x with Error es -> es | Ok _ -> []
        Error(req @ e p @ e st @ e ev @ e rc @ e ro @ e mv @ e po @ e pr @ e sc @ e sm @ e me @ e sp)
