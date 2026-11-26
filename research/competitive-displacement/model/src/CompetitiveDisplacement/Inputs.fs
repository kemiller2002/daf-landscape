/// Typed model inputs and their parsers. Parsers return Result; nothing throws.
module CompetitiveDisplacement.Inputs

open CompetitiveDisplacement.Csv

type Range = { Low: float; Base: float; High: float }

type Level = Low | Base | High

let pick level r = match level with Low -> r.Low | Base -> r.Base | High -> r.High

type EventDef =
    { Id: string; Name: string; Expertise: string; Structured: bool; PassThrough: bool
      Freq: Range; PConv: float; DConv: float; PNative: float; DNative: float
      SponsorMinConv: float; SponsorMinNative: float
      OnetimeMinConv: float; OnetimeMinNative: float
      OnetimePerAcctConv: float; OnetimePerAcctNative: float
      External: float; AiCostTouch: float; AiCostRoutine: float
      FailProb: float; FailMinutes: float; FailExternal: float; FailLoss: float
      Prevention: string; PrevEfficacy: float; PrevCost: float }

type Mode =
    { Id: string; Name: string; TouchRule: string; DurationRule: string; SponsorRule: string
      FailRule: string; UsesAi: bool; UsesPrevention: bool; OwnsPlatform: bool
      VendorEventShare: float; Fixed: Range; Build: Range }

type RegistryComponent =
    { Id: string; Name: string; Annual: Range; Classification: string; RemovableWhen: string }

type RegistryAlt =
    { Id: string; Name: string; Connectors: float; StateData: float; SupportFte: float
      CounselHours: float; TpspAudit: float; Insurance: float; DbShare: float; AutoResolve: float
      AiPerException: float; CommercialLicence: float; Shared: bool; StewardFloorFte: float
      StandaloneOverhead: float; EchelonConnectorSaving: float; EchelonReliance: float }

type Route =
    { Id: string; Name: string; Build: Range; Burn: Range; FirstRevenueMonth: Range
      RevenuePerCustomer: Range; Recurring: bool; CustomersPerYear: Range
      VariableShare: float; Cac: float; Custodial: bool }

/// Parameter values keyed by name, each with a range.
type Params = Map<string, Range>

let private range prefix row =
    match num (prefix + "_low") row, num (prefix + "_base") row, num (prefix + "_high") row with
    | Ok l, Ok b, Ok h -> Ok { Low = l; Base = b; High = h }
    | Error e, _, _ | _, Error e, _ | _, _, Error e -> Error e

let private yes key row = get key row |> Result.map (fun v -> v.Trim().ToUpperInvariant() = "Y")

/// Applicative-style collection of row results: all rows parse or every error is reported.
let collect (rows: Result<'T, string> list) : Result<'T list, string list> =
    let oks = rows |> List.choose (function Ok x -> Some x | _ -> None)
    let errs = rows |> List.choose (function Error e -> Some e | _ -> None)
    if List.isEmpty errs then Ok oks else Error errs

type ResultBuilder() =
    member _.Bind(r, f) = Result.bind f r
    member _.Return x = Ok x

let result = ResultBuilder()

let parseEvent (row: Row) : Result<EventDef, string> =
    result {
        let! id = get "event_id" row
        let! name = get "event" row
        let! expertise = get "expertise" row
        let! structured = yes "structured" row
        let! pass = yes "pass_through_external" row
        let! freq = range "freq" row
        let! pc = num "p_conv" row
        let! dc = num "d_conv" row
        let! pn = num "p_native" row
        let! dn = num "d_native" row
        let! smc = num "sponsor_min_conv" row
        let! smn = num "sponsor_min_native" row
        let! omc = num "onetime_min_conv" row
        let! omn = num "onetime_min_native" row
        let! opc = num "onetime_min_per_acct_conv" row
        let! opn = num "onetime_min_per_acct_native" row
        let! ext = num "external_cost" row
        let! act = num "ai_cost_touch" row
        let! acr = num "ai_cost_routine" row
        let! fp = num "fail_prob" row
        let! fm = num "fail_minutes" row
        let! fe = num "fail_external" row
        let! fl = num "fail_loss" row
        let! prev = get "prevention" row
        let! pe = num "prev_efficacy" row
        let! pcost = num "prev_cost" row
        return
            { Id = id; Name = name; Expertise = expertise; Structured = structured; PassThrough = pass
              Freq = freq; PConv = pc; DConv = dc; PNative = pn; DNative = dn
              SponsorMinConv = smc; SponsorMinNative = smn; OnetimeMinConv = omc; OnetimeMinNative = omn
              OnetimePerAcctConv = opc; OnetimePerAcctNative = opn; External = ext; AiCostTouch = act
              AiCostRoutine = acr; FailProb = fp; FailMinutes = fm; FailExternal = fe; FailLoss = fl
              Prevention = prev; PrevEfficacy = pe; PrevCost = pcost }
    }
    |> Result.mapError (fun e -> let id = Map.tryFind "event_id" row |> Option.defaultValue "?" in $"events.csv {id}: {e}")

let parseMode (row: Row) : Result<Mode, string> =
    result {
        let! id = get "mode_id" row
        let! name = get "mode" row
        let! tr = get "touch_rule" row
        let! dr = get "duration_rule" row
        let! sr = get "sponsor_level_rule" row
        let! fr = get "fail_rule" row
        let! ai = yes "uses_ai_cost" row
        let! pv = yes "uses_prevention" row
        let! op = yes "owns_platform" row
        let! share = num "vendor_event_share" row
        let! fixedR = range "fixed" row
        let! build = range "build" row
        return
            { Id = id; Name = name; TouchRule = tr; DurationRule = dr; SponsorRule = sr; FailRule = fr
              UsesAi = ai; UsesPrevention = pv; OwnsPlatform = op; VendorEventShare = share
              Fixed = fixedR; Build = build }
    }

let parseParams (rows: Row list) : Result<Params, string list> =
    rows
    |> List.map (fun row ->
        match get "name" row, num "low" row, num "base" row, num "high" row with
        | Ok n, Ok l, Ok b, Ok h -> Ok(n, { Low = l; Base = b; High = h })
        | _ -> let id = Map.tryFind "param_id" row in Error $"bad parameter row {id}")
    |> collect
    |> Result.map Map.ofList

let parseComponent (row: Row) : Result<RegistryComponent, string> =
    result {
        let! id = get "component_id" row
        let! name = get "component" row
        let! annual = range "annual" row
        let! cls = get "classification" row
        let! rem = get "removable_when" row
        return { Id = id; Name = name; Annual = annual; Classification = cls; RemovableWhen = rem }
    }

let parseAlt (row: Row) : Result<RegistryAlt, string> =
    result {
        let! id = get "alt_id" row
        let! name = get "alternative" row
        let! c = num "connectors" row
        let! sd = num "state_data_usd" row
        let! sf = num "support_desk_fte" row
        let! ch = num "counsel_hours_recurring" row
        let! tp = num "tpsp_audit_usd" row
        let! ins = num "insurance_usd" row
        let! db = num "db_share" row
        let! ar = num "auto_resolve" row
        let! ai = num "ai_cost_per_exception" row
        let! cl = num "commercial_licence_usd" row
        let! sh = yes "shared" row
        let! fl = num "steward_floor_fte" row
        let! so = num "standalone_overhead_usd" row
        let! es = num "echelon_connector_saving" row
        let! er = num "echelon_reliance_usd" row
        return
            { Id = id; Name = name; Connectors = c; StateData = sd; SupportFte = sf; CounselHours = ch
              TpspAudit = tp; Insurance = ins; DbShare = db; AutoResolve = ar; AiPerException = ai
              CommercialLicence = cl; Shared = sh; StewardFloorFte = fl; StandaloneOverhead = so
              EchelonConnectorSaving = es; EchelonReliance = er }
    }

let parseRoute (row: Row) : Result<Route, string> =
    result {
        let! id = get "route_id" row
        let! name = get "route" row
        let! b = range "build" row
        let! burn = range "monthly_burn" row
        let! fr = range "months_to_first_revenue" row
        let! rev = range "revenue_per_customer" row
        let! rec' = yes "recurring" row
        let! cust = range "customers_per_year" row
        let! vs = num "variable_cost_share" row
        let! cac = num "cac_per_customer" row
        let! cus = yes "custodial" row
        return
            { Id = id; Name = name; Build = b; Burn = burn; FirstRevenueMonth = fr; RevenuePerCustomer = rev
              Recurring = rec'; CustomersPerYear = cust; VariableShare = vs; Cac = cac; Custodial = cus }
    }

type Inputs =
    { Events: EventDef list; Modes: Mode list; Params: Params; Components: RegistryComponent list
      Alts: RegistryAlt list; RegistryParams: Params; Routes: Route list }
